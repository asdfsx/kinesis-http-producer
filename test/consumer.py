"""
consume kinesis
"""
import time
import boto3

def main():
    """test"""
    client = boto3.client("kinesis")
    stream_info = client.describe_stream(StreamName="test")
    shard_id = stream_info["StreamDescription"]["Shards"][0]["ShardId"]
    iterator = client.get_shard_iterator(StreamName="test",
                                         ShardId=shard_id,
                                         ShardIteratorType="AT_TIMESTAMP",
                                         Timestamp=time.time()-3600,)
    records = client.get_records(ShardIterator=iterator["ShardIterator"])
    print records

if __name__ == "__main__":
    main()
