#!/usr/bin/python

from HTU21DF_ADMINCK import HTU21D
import Adafruit_BMP.BMP085 as BMP085
import time
import math
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def padForCenter(dispText, font):
	"""
	Subtract screen width by provided text, halve & return int part
	"""
	textWidth = draw.textsize(dispText, font=font)[0]
	#i, d = math.modf((width - textWidth)/2)
	pad = (width - textWidth)/2

	print "value: %s" % dispText
	print "textWidth: %.2f" % textWidth
	print "screen width: %.2f" % width
	print "pad: %.2f" % pad

	return pad

# -- create sensor read oject
temp_sensor = HTU21D()
pres_sensor = BMP085.BMP085()

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Height of 1st row (differnet colour)
firstrow = 16

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8) visitor1.ttf
font = ImageFont.truetype('visitor1.ttf', 14)
# -- top row of 16 px different colour
topfont = ImageFont.truetype('visitor1.ttf', 18)
bottomfont = ImageFont.truetype('visitor1.ttf', 48)

try:
	while True:
		# convert to F
		bmp_temp = (pres_sensor.read_temperature() * 9)/5 + 32

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

		temp = temp_sensor.read_tmperature()
		humidity = temp_sensor.read_humidity()
		pressure = pres_sensor.read_pressure()

		# write text
		title = "Humidity"
		data = "%.2f" % humidity
		draw.text((padForCenter(title, topfont), top), title, font=topfont, fill=255)
		draw.text((padForCenter(data, bottomfont), top+firstrow), data, font=bottomfont, fill=255)

		# Display image.
		disp.image(image)
		disp.display()
		time.sleep(1)

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"

	# Clear display.
	disp.clear()
	disp.display()
