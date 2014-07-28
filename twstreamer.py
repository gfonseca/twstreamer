import tweepy
import webbrowser
import time
import sys
import pprint
import json

consumer_key = '***'
consumer_secret = '***'


## Getting access key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth_url = auth.get_authorization_url()
print 'From your browser, please click AUTHORIZE APP and then copy the unique PIN: ' 
print auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
access_key = auth.access_token.key
access_secret = auth.access_token.secret


## Authorizing account privileges
auth.set_access_token(access_key, access_secret)


## Get the local time
localtime = time.asctime( time.localtime(time.time()) )

class StdOutListener(tweepy.StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
	def on_status(self, status):
		print "\033[36m@%s\033[0m" % status.author.name
		print "\033[94m%s\033[0m" % status.text
		print "\n",
		return True

	def on_error(self, status):
		pass

if __name__ == '__main__':
	l = StdOutListener()

	stream = tweepy.Stream(auth, l)
	stream.userstream()
