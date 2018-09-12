#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import datetime
from Adafruit_BME280 import *
app = Flask(__name__)

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

@app.route("/")
def getSensorData():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")

	temp = sensor.read_temperature_f()
	humidity = sensor.read_humidity()
	pressure = sensor.read_pressure() / 100
	
	templateData = {
		'title' : 'SENSOR!',
		'time' : timeString,
		'temp' : temp,
		'humidity': humidity,
		'pressure': pressure
	}
	return render_template('sensor.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8088, debug=True)
