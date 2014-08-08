#! /usr/bin/env python
# coding: utf-8


import sys, os
import tweepy
from datetime import datetime
import re

CONSUMER_KEY = 'dvcNxv04JRtsTpXdqsT4YNwoQ'
CONSUMER_SECRET = 'vZheuS46AYjue0sYPq9f02jCEEpBD6xbOLZteZv3hrp0q3kX3N'
ACCESS_FILEPATH = "/tmp/.access"


class StdOutListener(tweepy.StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
	
	
	def __init__(self, formater):	
		tweepy.StreamListener.__init__(self)
		self.formater = formater
	
	def on_status(self, status):
		print self.formater(status)
		print ""
		return True

	def on_error(self, status):
		pass


def save_key_secret(key, secret):
	acc = open(ACCESS_FILEPATH, "w+")
	acc.write("access_key=%s\n" % key)
	acc.write("access_secret=%s" % secret)
	acc.close()


def retrieve_access():
	acc = open(ACCESS_FILEPATH, "r+")
	access_key = acc.readline().split("=")[1]
	access_secret = acc.readline().split("=")[1]
	acc.close()
	return access_key.strip(), access_secret.strip()


def has_grant():
	if not os.path.isfile(ACCESS_FILEPATH):
		return False
	
	key, secret = retrieve_access()
	
	if not key or not secret:
		return False
	
	return True


def request_user_for_pin(url):
	print 'From your browser, please click AUTHORIZE APP and then copy the unique PIN: ' 
	print url
	verifier = raw_input('PIN: ').strip()
	auth.get_access_token(verifier)
	return auth.access_token.key, auth.access_token.secret


def start_listening(auth):
	l = StdOutListener(tt_formatter)
	stream = tweepy.Stream(auth, l)
	stream.userstream()

def tt_formatter(status):
	time = status.created_at.strftime("%H:%M")
	user = status.author.name.encode("utf-8")
	tt = status.text.strip("\n \t").encode("utf-8")
	tt = mark_tt_simbols(tt)
	out_string = template_string(spacer="\n").encode("utf-8")
	return out_string.format(user=user, time=time, text=tt)
	

def template_string(c_user="\033[1;37;44m", c_text="\033[0m", c_time="\033[2;37m", spacer=" "):
		return "{c_user}@{user}\033[0m{spacer}{c_text}{text}\033[0m{spacer}{c_time}{time}\033[0m".format(
				c_user=c_user,
				c_text=c_text,
				c_time=c_time,
				spacer=spacer,
				user="{user}",
				text="{text}",
				time="{time}"
				)

def mark_tt_simbols(text):
	formated_text = ""
	simbols = text.split()
	for simbol in simbols:
		if is_hash(simbol):
			simbol = "\033[1;35m%s" % simbol
		elif is_url(simbol):
			simbol = "\033[1;32m%s" % simbol
		elif is_usr(simbol):
			simbol = "\033[1;34m%s" % simbol
		simbol += "\033[0m"

		formated_text += " %s" % simbol
		formated_text = formated_text.strip()
	return formated_text

def is_hash(simb):
	reg = re.compile("\#\w+")
	return bool(reg.match(simb))

def is_url(simb):
	reg = re.compile("(http:\/\/)?([\w_-]+\.)+[\w]{2,3}(\/[^ \t]+)?")
	return bool(reg.match(simb))

def is_usr(simb):
	reg = re.compile("(http:\/\/)?([\w_-]+\.)+[\w]{2,3}(\/[^ \t]+)?")
	return bool(reg.match(simb))

if __name__ == "__main__":
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	
	if not has_grant():
		auth_url = auth.get_authorization_url()
		key, secret = request_user_for_pin(auth_url)
		save_key_secret(key, secret)
	else:
		key, secret = retrieve_access()
	
	auth.set_access_token(key, secret)
	start_listening(auth)
		
