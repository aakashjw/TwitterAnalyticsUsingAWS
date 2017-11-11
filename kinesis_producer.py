import boto3
import json
from datetime import datetime
import calendar
import random
import time

my_stream_name = 'jishas-stream'

kinesis_client = boto3.client('kinesis', 
                                region_name='us-east-2',
                                aws_access_key_id='AKIAJD2XQ5P4X3U76GWA',
                                aws_secret_access_key='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')

print (kinesis_client.describe_stream(StreamName='twitter-stream'))

def put_to_stream(payload):


    #print (payload)

    put_response = kinesis_client.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey="shardId-000000000073")