#!/usr/bin/python

# -- twitter-post-status
# -- - posts a status message to your timeline

from HTU21DF_ADMINCK import HTU21D
from twitter import *
import datetime
import time

# --load our API credentials
config = {}
execfile("/home/pi/git_code/python-twitter-examples/config.py", config)

# --create twitter API object
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
twitter = Twitter(auth = auth)
stream = TwitterStream(domain = "userstream.twitter.com", auth = auth, secure = True)

# command list
CMD_POST = "posttemp"
CMD_START_KEG = "startkeg"
CMD_STOP_KEG = "stopkeg"

# --sleep for this number of seconds between tweets, to ensure we
# --don't flood
SLEEP_TIME = 5

# -- iterate over tweets matching this filter text
tweet_iter = stream.user()

try:
	for tweet in tweet_iter:
		# -- check whether this is a valid tweet
		if "entities" not in tweet:
			continue

		# -- do we have any new tweet commands we have not dispatched?
		cmd_check = tweet["text"].encode("ascii", "ignore")

		print "tweet to check: %s" % cmd_check

		# -- create sensor read oject
		obj = HTU21D()

		if CMD_POST in cmd_check:
			print "---posting temp/humidity"

			# -- post temp/humidity.
			# -- use try/except to catch potential failures.
			try:
				tweet_text = "Kegstatus -- Temp: %.2fF -- Humidity: %.2f%%rH" % (obj.read_tmperature(), obj.read_humidity())

				# -- post a new status
				# -- twitter API docs: https://dev.twitter.com/rest/reference/post/statuses/update
				results = twitter.statuses.update(status = tweet_text)

				# delete command tweet
				destroy_status = twitter.statuses.destroy._id(_id = tweet["id"])
				print "just destroyed: %s -- %s" % (destroy_status["text"], destroy_status["id_str"])
			except Exception, e:
				print " - failed (maybe a duplicate?): %s" % e
		elif CMD_START_KEG in cmd_check:
			print "--starting kegstatus.py"
		elif CMD_STOP_KEG in cmd_check:
			print "--stopping kegstatus.py"
		else:
			print "no command found"

		time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"

except:
	print "Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1]
	print traceback.format_exc()
	raise

finally:
	print "finishing up..."
