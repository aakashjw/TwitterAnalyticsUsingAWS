import string
import pymysql
import ast
import sys
import boto3
import json
import time
import ast
import datetime

f = open("input.txt")
character_list = []
for text in f.readlines():
    character_list.append(text.strip())
print character_list

#handles datetime error
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

mydb = pymysql.connect(host='XXXXXXXXXXXX',
                                   port=XXXXX,
                                   user='XXXXXXX',
                                   passwd='XXXXXXXXX',
                                   db='XXXXXXXXX')
cur = mydb.cursor()

cur.execute("TRUNCATE TABLE TwitterDB.Tweets")

my_stream_name = 'XXXXXX'

kinesis_client = boto3.client('kinesis')

response = kinesis_client.describe_stream(StreamName=my_stream_name)


my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=2)

while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=2)
    
    #Extracting important fieds by parsing json
    json.dumps(record_response, indent = 2, default=datetime_handler)
    print record_response.keys()
    res = record_response['Records']
    tweet_ifo_table = {}
    for l in res:
      data = l['Data']
      twitter_data = data[1:-1]
      twitter_data = twitter_data.replace("\r\n", "")
      twitter_data = twitter_data.replace("\\/", "")
      twitter_data = twitter_data.replace("\\", "")
      twitter_data = twitter_data.replace("}rn", "}") 
      data = json.dumps(twitter_data)
      dict_data = ast.literal_eval(data)
      list_data = (dict_data[1:-1]).split(",")
      for l in list_data:
        if '"created_at":' in l:
          created_at = (l.split(":")[1]).replace('"', '')
          created_at = created_at.replace(" ", "_")
          tweet_ifo_table["created_at"] = created_at
        elif '"id":' in l:
          if "id" not in tweet_ifo_table.keys():
            tweet_ifo_table["id"] = (l.split(":")[1]).replace('"', '')
            print int(tweet_ifo_table["id"])
        elif '"text":' in l:
          tweet_ifo_table["text"] = (l.split(":")[1]).replace('"', '')
        elif '"lang":' in l:
          tweet_ifo_table["lang"] = (l.split(":")[1]).replace('"', '')
        elif '"location":' in l:
          location = (l.split(":")[1]).replace('"', '')
          location = location.replace(" ","")
          tweet_ifo_table["location"] = location

      #All the extracted fields stored in a dictionary
      print tweet_ifo_table



    request_items = record_response
    if(len(request_items['Records']) > 0):
        data = request_items['Records'][0];
        data = data['Data']
        tweetChrList = []

        for ch_str in character_list:
            if ch_str.lower() in data.lower():
                tweetChrList.append(ch_str)

        if len(tweetChrList)>0:
            for tweetChr in tweetChrList:
                #send over to AWS to populate Schema
                query = ("INSERT INTO TwitterDB.Tweets "
                "(Tweets.Character,Tweets.created_at,Tweets.language,Tweets.location) "
                "VALUES(%s,%s,%s,%s)")
                args = (tweetChr,str(tweet_ifo_table["created_at"]),str(tweet_ifo_table["lang"]),str(tweet_ifo_table["location"]))
                cur.execute(query, args)
                mydb.commit()           
    time.sleep(5)
cur.close()
print ("Done")
