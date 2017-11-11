#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import kinesis_producer as kinesis_client

#Variables that contains the user credentials to access Twitter API 
access_token = "1360471795-gdsbarUnPQf6augw4byhIjRlIX5K8SPklP4im1i"
access_token_secret = "bnP19PcntCOpHLw6k1LEQI04ObUIooFM671kuVkWu5dE4"
consumer_key = "EW0UCymc40M5jJgOW5gj9KZz2"
consumer_secret = "IzeALCcg3N2IyAAlCBtOKpfln1kkvVBfXi0w6DTWkIDYPmdfBs"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print (json.loads(data).get("text"))
        kinesis_client.put_to_stream(data)
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Javascript', 'Python', 'Ruby'])