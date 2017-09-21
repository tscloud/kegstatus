#!/usr/bin/python

# -- poll to get keg stats to write to file

from HTU21DF_ADMINCK import HTU21D
from dropboxupload import TransferData
import Adafruit_BMP.BMP085 as BMP085
import time

# --load our API credentials
config = {}
execfile("/home/pi/git_code/python-twitter-examples/config.py", config)

# -- create sensor read oject
temp_sensor = HTU21D()
pres_sensor = BMP085.BMP085()

outfile = "outfile.out"
sleep_value = 1*60

print "starting kegstatus..."

f = open(outfile,"w")

try:
	while True:
		# convert to F
		bmp_temp = (pres_sensor.read_temperature() * 9)/5 + 32

		ts = int(time.time())
		temp = temp_sensor.read_tmperature()
		humidity = temp_sensor.read_humidity()
		pressure = pres_sensor.read_pressure()

		outline = "%d,%.2f,%.2f,%.2f,%.2f\n" % (ts, temp, bmp_temp, humidity, pressure)
		f.write(outline)
		print outline

		# sleep for a while
		time.sleep(sleep_value)

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"
	print "uploading file..."

    #----add access_token to above config file
    #access_token = 'W-PWCPYb80UAAAAAAAABTlqDbTSN9i-JpuldCmGGUgurUhGQo8Leq83agDQzqUyj'
    access_token = config["access_token"]

    transferData = TransferData(access_token)

    file_from = './outfile.out'
    file_to = '/kegstatus/outfile.out'  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

    print "...upload complete"

except:
	print "Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1]
	print traceback.format_exc()
	raise

finally:
	print "finishing up..."
	f.close()
