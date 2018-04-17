#!/usr/bin/env python

import SimpleMFRC522
import RPi.GPIO as GPIO
from flask import Flask, render_template
app = Flask(__name__)
GPIO.setwarnings(False)

reader = SimpleMFRC522.SimpleMFRC522()

@app.route("/")
def index():
	id,text = reader.read()
	templateData = {
		'TITLE' : 'RFID Number',
		'ID' : id,
		'TEXT' : text,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
