#!/usr/bin/python

import time
import math
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import urllib2

from HTMLParser import HTMLParser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print "Encountered a start tag:", tag

	def handle_endtag(self, tag):
		print "Encountered an end tag :", tag

	def handle_data(self, data):
		print "Encountered some data  :", data
		if("Humidity" in data):
			

# class for text processing
class TextProcessor():

	def __init__(self, aDispText='Welcome', aFontName='visitor1.ttf', aFontSize=8):
		"""
		Subtract screen width by provided text, halve & return int part
		 if this neg # -> change font
		"""
		# the font to be used
		self.font = ImageFont.truetype(aFontName, aFontSize)
		# the font name & size to be used
		self.fontName = aFontName
		self.fontSize = aFontSize
		# the padding to center text
		self.pad = 0

		self.determineFont(aDispText)

	def determineFont(self, aDispTextRecur):
		"""
		call recursively to determine font size
		"""
		textWidth = draw.textsize(aDispTextRecur, font=self.font)[0]
		#width is width of screen - global
		self.pad = (width - textWidth)/2

		if(self.pad < 0):
			# reduce font size
			self.fontSize -= 2
			self.font = ImageFont.truetype(self.fontName, self.fontSize)

			# recursive call
			self.determineFont(aDispTextRecur)


def callback_rising(channel):
	"""
	callback when button pressed
	"""
	print '...RISING callback called on channel %s' % channel
	global mode
	mode += 1
	if(mode > max_modes):
		mode = 0

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

# this is going to determine what we display
mode = 0
max_modes = 2

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
#font = ImageFont.truetype('Minecraftia.ttf', 8)
#font = ImageFont.truetype('visitor1.ttf', 14)
#font = ImageFont.truetype('pixelmix.ttf', 14)
# -- top row of 16 px different colour
bottomfontName = 'visitor1.ttf'
topfontName = 'visitor1.ttf'
topfontSize = 18
bottomfontSize = 38

# GPIO setup
GPIO.setmode(GPIO.BCM)
print "GPIO.BOARD: %s" % GPIO.BOARD
print "GPIO.BCM: %s" % GPIO.BCM
print "GPIO mode: %s" % GPIO.getmode()
# Pin button tied to
pin_in = 18
GPIO.setup(pin_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	GPIO.add_event_detect(pin_in, GPIO.RISING, callback=callback_rising, bouncetime=300)  # add rising edge detection on a channel
	while True:
		# convert to F
		#bmp_temp = (pres_sensor.read_temperature() * 9)/5 + 32

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

		# <<< this is used if obtaning data from remote sensor
		response = urllib2.urlopen('http://rpi3:8088/')
		html = response.read()
		print html
		# >>>

		# instantiate the parser and fed it some HTML
		parser = MyHTMLParser()
		parser.feed(html)

		# write text
		if(mode == 0):
			title = "Humidity"
			data = "%.2f" % humidity
		elif(mode == 1):
			title = "Temperature"
			data = "%.2f" % temp
		elif(mode == 2):
			title = "Pressure"
			data = "%.2f" % pressure

		textProc = TextProcessor(title, topfontName, topfontSize)
		#draw.text((padForCenter(title, topfont), top), title, font=topfont, fill=255)
		draw.text((textProc.pad, top), title, font=textProc.font, fill=255)

		textProc = TextProcessor(data, bottomfontName, bottomfontSize)
		#draw.text((padForCenter(data, bottomfont), top+firstrow), data, font=bottomfont, fill=255)
		draw.text((textProc.pad, top+firstrow), data, font=textProc.font, fill=255)

		# Display image.
		disp.image(image)
		disp.display()
		time.sleep(1)

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"

	# Clear display.
	disp.clear()
	disp.display()

finally:
	GPIO.cleanup()
	print "\nBye"

