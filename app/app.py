# -*- coding:utf-8 -*-

import ConfigParser
import logging
import logging.config
import traceback
import hashlib

from producer import kinesis_producer

CONFIG_FILE = "etc/producer.conf"

logging.config.fileConfig('etc/producer_logging.conf')

config_parser = ConfigParser.ConfigParser({"type":"kinesis"})
config_parser.read(CONFIG_FILE)
producer_type = config_parser.get("producer", "type")

producerobj = None
try:
    if producer_type == "kinesis":
        producerobj = kinesis_producer.Producer(CONFIG_FILE)
except:
    print traceback.format_exc()
    raise

def application (environ, start_response):
    request_method = environ["REQUEST_METHOD"]
    path = environ['PATH_INFO']

    # print request_method, path

    status = "200 OK"
    response_headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", "2")
    ]
    response_body = "ok"

    if path == "/app" and request_method == "POST":
        process_post(environ)
        
        response_headers = [
            ("Content-Type", "text/plain"),
            ("Content-Length", "5")
        ]
        response_body = "appok"

        start_response(status, response_headers)
        return [response_body]

    start_response(status, response_headers)
    return [response_body]

def process_post(environ):
    """process post request"""

    if "CONTENT_LENGTH" in environ and environ["CONTENT_LENGTH"] != "":
        length = int(environ.get("CONTENT_LENGTH", "0"))
        content = environ['wsgi.input'].read(length).decode()
        hash_num = int(hashlib.md5(content).hexdigest(), 16)
        if producerobj is not None:
            producerobj.put_async_record(content, hash_num)
            #producerobj.put_sync_record(content, hash_num)
