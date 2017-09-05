#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-post-status
#  - posts a status message to your timeline
#-----------------------------------------------------------------------

from HTU21DF_ADMINCK import HTU21D
from twitter import *
import datetime
import time

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("/home/pi/git_code/python-twitter-examples/config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
twitter = Twitter(auth = auth)
stream = TwitterStream(domain = "userstream.twitter.com", auth = auth, secure = True)

# command list
cmd_post = "posttemp"

#-----------------------------------------------------------------------
# sleep for this number of seconds between tweets, to ensure we
# don't flood
#-----------------------------------------------------------------------
sleep_time = 5

#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.user()

for tweet in tweet_iter:
	#-----------------------------------------------------------------------
	# check whether this is a valid tweet
	#-----------------------------------------------------------------------
	if "entities" not in tweet:
		continue

	#-----------------------------------------------------------------------
	# do we have any new tweet commands we have not dispatched?
	#-----------------------------------------------------------------------
	cmd_check = tweet["text"].encode("ascii", "ignore")

	print "tweet to check: %s" % cmd_check

	if cmd_post in cmd_check:
		# reset time last command was performed
		print "---posting temp/humidity"

		#-----------------------------------------------------------------------
		# post temp/humidity.
		# use try/except to catch potential failures.
		#-----------------------------------------------------------------------
		try:
			obj = HTU21D()
			tweet_text = "Temp: %.2fF -- Humidity: %.2f%%rH" % (obj.read_tmperature(), obj.read_humidity())
			#-----------------------------------------------------------------------
			# post a new status
			# twitter API docs: https://dev.twitter.com/rest/reference/post/statuses/update
			#-----------------------------------------------------------------------
			results = twitter.statuses.update(status = tweet_text)
			# delete command tweet
			destroy_status = twitter.statuses.destroy._id(_id = tweet["id"])
			print "just destroyed: %s -- %s" % (destroy_status["text"], destroy_status["id_str"])
		except Exception, e:
			print " - failed (maybe a duplicate?): %s" % e
	else:
		print "check found no command"

	time.sleep(sleep_time)

