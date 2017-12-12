#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import boto3

#Variables that contains the user credentials to access Twitter API 
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX"

my_stream_name = 'XXXXXXXXXX'

kinesis_client = boto3.client('kinesis')

print (kinesis_client.describe_stream(StreamName=my_stream_name))

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        #print json.dumps(data)
        
        self.put_to_stream(data)
        return True

    def on_error(self, status):
        print(status)

    def put_to_stream(self, data):
        #print (payload)
        put_response = kinesis_client.put_record(
                            StreamName=my_stream_name,
                            Data=json.dumps(data),
                            PartitionKey="shardId-000000000000")


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    f = open("input.txt")
    text_filter = []
    for text in f.readlines():
        text_filter.append(text.strip())
    print text_filter
    stream.filter(track=text_filter)