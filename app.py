#!/usr/bin/env python

import sqlite3 as lite
import sys
import SimpleMFRC522
import RPi.GPIO as GPIO
from flask import Flask, render_template
app = Flask(__name__)
GPIO.setwarnings(False)

reader = SimpleMFRC522.SimpleMFRC522()

@app.route("/")
def index():
	id,text = reader.read_no_block()
	stevensID = 0
	LEDStatus = "Space available"
	if text != None:
		text = text.strip()
		LEDStatus = "Space available"
	if text == "Stevens":
		stevensID = 1
		LEDStatus = "Space occupied"
	elif text == None:
		stevensID = 0
	else:
		stevensID = 2
	with lite.connect('RFID.db') as con:
		cur = con.cursor()
		cur.execute("SELECT FirstName,LastName,Year FROM Users WHERE Id=?",(id,))
		data = cur.fetchone()
		if data == None:
			stevensID = 2
			firstName = "N/A"
			lastName = "N/A"
			year = "N/A"
		else:
			firstName = data[0]
			lastName = data[1]
			year = data[2]
	templateData = {
		'TITLE' : 'RFID Number',
		'ID' : id,
		'TEXT' : text,
		'stevensID' : stevensID,
		'STATUS' : LEDStatus,
		'FIRSTNAME' : firstName,
		'LASTNAME' : lastName,
		'YEAR' : year,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
