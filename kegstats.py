#!/usr/bin/python

# -- poll to get keg stats to write to file

from HTU21DF_ADMINCK import HTU21D
import time

# -- create sensor read oject
obj = HTU21D()

outfile = "outfile.out"
sleep_value = 1*60

print "starting kegstatus..."

f = open(outfile,"w")

try:
	while True:
		outline = "%.2f,%.2f\n" % (obj.read_tmperature(), obj.read_humidity())
		f.write(outline)

		# sleep for a while
		time.sleep(sleep_value)

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"

except:
	print "Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1]
	print traceback.format_exc()
	raise

finally:
	print "finishing up..."
	f.close()
