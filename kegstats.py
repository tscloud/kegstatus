#!/usr/bin/python

# -- poll to get keg stats to write to file

from HTU21DF_ADMINCK import HTU21D
import Adafruit_BMP.BMP085 as BMP085
import time

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

except:
	print "Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1]
	print traceback.format_exc()
	raise

finally:
	print "finishing up..."
	f.close()
