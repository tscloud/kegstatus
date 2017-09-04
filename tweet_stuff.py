#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-post-status
#  - posts a status message to your timeline
#-----------------------------------------------------------------------

from twitter import *
from HTU21DF_ADMINCK import HTU21D

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("/home/pi/git_code/python-twitter-examples/config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
	auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

#-----------------------------------------------------------------------
# post a new status
# twitter API docs: https://dev.twitter.com/rest/reference/post/statuses/update
#-----------------------------------------------------------------------
obj = HTU21D()
tweet_text = "Temp: %.2fF -- Humidity: %.2f%%rH" % (obj.read_tmperature(), obj.read_humidity())
results = twitter.statuses.update(status = tweet_text)
print "updated status: %s" % tweet_text
