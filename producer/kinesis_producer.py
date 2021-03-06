# -*- coding:utf-8 -*-

import ConfigParser
import time
import os
import hashlib
import traceback
import logging
import logging.config

import boto3
import gevent
from gevent.lock import BoundedSemaphore

logging.config.fileConfig('etc/producer_logging.conf')

class Producer(object):
    """ kinesis producer"""
    def __init__(self, config_file):
        self.cache = []
        self.current_time = int(time.time())
        self.config_file = config_file
        self.config_stat = os.stat(self.config_file)
        self.config_changed = False
        self.config_sem = BoundedSemaphore(1)
        self.cache_sem = BoundedSemaphore(1)
        self.readConfig()

        self.produce_gevent = gevent.spawn(self.produce)
        self.config_monitor_gevent = gevent.spawn(self.config_monitor)
        self.produce_gevent.start()
        self.config_monitor_gevent.start()

    def readConfig(self):
        default_value = {"stream_name" : "test",
                         "region_name" : "",
                         "endpoint_url" : "",
                         "batch_size" : 50,
                         "batch_interval" : 5,
                         "aws_access_key_id": "",
                         "aws_secret_access_key": "",}

        config_parser = ConfigParser.ConfigParser(defaults=default_value)
        config_parser.read(self.config_file)

        self.stream_name = config_parser.get("kinesis", "stream_name")
        self.region_name = config_parser.get("kinesis", "region_name")
        self.endpoint_url = config_parser.get("kinesis", "endpoint_url")
        self.aws_access_key_id = config_parser.get("kinesis", "aws_access_key_id")
        self.aws_secret_access_key = config_parser.get("kinesis", "aws_secret_access_key")
        self.batch_size = config_parser.getint("kinesis", "batch_size")
        self.batch_interval = config_parser.getint("kinesis", "batch_interval")

        if self.region_name == "":
            self.region_name = None
        if self.endpoint_url == "":
            self.endpoint_url = None
        if self.aws_access_key_id == "":
            self.aws_access_key_id = None
        if self.aws_secret_access_key == "":
            self.aws_secret_access_key = None

        self.client = boto3.client("kinesis",
                                   region_name=self.region_name,
                                   endpoint_url=self.endpoint_url,
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key,)

        kinesis_stream_info = self.client.describe_stream(StreamName=self.stream_name)
        self.kinesis_shared_num = len(kinesis_stream_info["StreamDescription"]["Shards"])

    def put_async_record(self, data, hash_num):
        """put record into cache"""
        self.cache_sem.acquire()
        part_num = hash_num % self.kinesis_shared_num
        partition_key = "partition_%03d" % (part_num,)
        self.cache.append({"Data": data, "PartitionKey": partition_key},)
        self.cache_sem.release()

    def put_sync_record(self, data, hash_num):
        """put record into kinesis directly"""
        self.config_sem.acquire()
        part_num = hash_num % self.kinesis_shared_num
        partition_key = "partition_%03d" % (part_num,)
        self.client.put_record(StreamName=self.stream_name,
                               Data=data,
                               PartitionKey=partition_key,)
        self.config_sem.release()

    def config_monitor(self):
        """check if config_file is modified"""
        while True:
            self.config_sem.acquire()
            if not self.config_changed:
                latest_stat = os.stat(self.config_file)
                if latest_stat.st_mtime != self.config_stat.st_mtime:
                    self.config_changed = True
            self.config_sem.release()
            time.sleep(10)

    def produce(self):
        """produce cache"""
        while True:
            try:
                # update config
                self.config_sem.acquire()
                if self.config_changed:
                    self.readConfig()
                    self.config_changed = False
                self.config_sem.release()

                # produce cache
                print "====kinesis_producer.Producer===="
                if self.cache:
                    self.cache_sem.acquire()
                    ###
                    # put_records api 每次最多发送500条记录，所以这里要做个处理，每批发200条
                    ###
                    cache_size = len(self.cache)
                    batch = cache_size / 200
                    for i in range(batch):
                        start = i * 200
                        end = (i + 1) * 200
                        end2 = end > cache_size and cache_size or end
                        print i, start, end, end2, cache_size, batch
                        self.client.put_records(Records=self.cache[start:end2],
                                                StreamName=self.stream_name)
                    self.cache = []
                    self.cache_sem.release()

                time.sleep(self.batch_interval)
            except:
                print traceback.format_exc()
