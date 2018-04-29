#!/usr/bin/env python

import sqlite3 as lite
import sys
import SimpleMFRC522
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, url_for
import os

CHAIR_FOLDER = os.path.join('static','chair_photos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = CHAIR_FOLDER

GPIO.setwarnings(False)

reader = SimpleMFRC522.SimpleMFRC522()

@app.route("/")
def index():
	id,text = reader.read_no_block()
	stevensID = 0
	LEDStatus = "Space Available"
	#strips trailing characters
	if text != None:
		text = text.strip()
	#checks to see if stevens is written on the card
	if text == "Stevens":
		with lite.connect('RFID.db') as con:
			cur = con.cursor()
			cur.execute("SELECT FirstName,LastName,Year FROM Users WHERE Id=?",(id,))
			data = cur.fetchone()
			if data == None:
				stevensID = 2
				firstName = "N/A"
				lastName = "N/A"
				year = "N/A"
				LEDStatus = "NON STEVENS STUDENT"
			else:
				firstName = data[0]
				lastName = data[1]
				year = data[2]
				stevensID = 1
				LEDStatus = "Space occupied"
	elif text != "Stevens" and id != None:
		with lite.connect('RFID.db') as con:
			cur = con.cursor()
			cur.execute("SELECT FirstName,LastName,Year FROM Users WHERE Id=?",(id,))
			data = cur.fetchone()
			if data	 == None:
				stevensID = 2
				firstName = "N/A"
				lastName = "N/A"
				year = "N/A"
				LEDStatus = "NON STEVENS STUDENT"
			else:
				LEDStatus = "Error:Please visit the Stevens Card Center (No text written)"
	else:
		stevensID = 0
		firstName = "N/A"
		lastName = "N/A"
		year = "N/A"
	templateData = {
		'TITLE' : 'Data',
		'ID' : id,
		'TEXT' : text,
		'stevensID' : stevensID,
		'STATUS' : LEDStatus,
		'FIRSTNAME' : firstName,
		'LASTNAME' : lastName,
		'YEAR' : year,
	}
	return render_template('index.html', **templateData)

@app.route('/demo')
def demo():
	id, text = reader.read_no_block()
	image = [0,0,0,0]
	firstName = [" ", " ", " ", " "]
	lastName = [" ", " ", " ", " "]
	if text != None:
		text = text.strip()
	if text == "Stevens":
		with lite.connect('RFID.db') as con:
			cur = con.cursor()
			cur.execute("SELECT ChairNumber,Status FROM Chairs WHERE Id=?",(id,))
			data = cur.fetchone()
			if data == None:
				cur.execute("SELECT ChairNumber FROM Chairs WHERE Status='Available'")
				data = cur.fetchone()
				chairNumber = data[0]
				cur.execute("UPDATE Chairs SET Status='Unavailable', Id=? WHERE ChairNumber=?",(id,chairNumber))
			else:
				chairNumber = data[0]
				cur.execute("UPDATE Chairs SET Status='Available', Id=0 WHERE ChairNumber=?",(chairNumber,))
	with lite.connect('RFID.db') as con:
		cur = con.cursor()
		cur.execute("SELECT ChairNumber FROM Chairs WHERE Status='Available'")
		data = cur.fetchall()
		for i in range(len(data)):
			tempData=int(data[i][0])
			image[tempData-1] = os.path.join(app.config['UPLOAD_FOLDER'],'greenchair.jpg')
		cur.execute("SELECT ChairNumber FROM Chairs WHERE Status='Unavailable'")
		data = cur.fetchall()
		for i in range(len(data)):
			tempData=int(data[i][0])
			image[tempData-1] = os.path.join(app.config['UPLOAD_FOLDER'],'bluechair.jpg')
		cur.execute("SELECT Id FROM Chairs WHERE Status='Unavailable'")
		data = cur.fetchall()
		cur.execute("SELECT Id FROM Users")
		data2 = cur.fetchall()
		for i in range(len(data)):
			for j in range(len(data2)):
				if data[i] == data2[j]:
					tempid=data[i][0]
					cur.execute("SELECT FirstName, LastName FROM Users Where Id=?",(tempid,))
					data3 = cur.fetchone()
					cur.execute("SELECT ChairNumber FROM Chairs Where Id=?",(tempid,))
					data4 = cur.fetchone()
					k = data4[0]
					firstName[k-1]=data3[0]
					lastName[k-1]=data3[1]
	templateData = {
		'TITLE' : 'Demo',
		'IMAGE1' : image[0],
		'IMAGE2' : image[1],
		'IMAGE3' : image[2],
		'IMAGE4' : image[3],
		'FIRSTNAME1' : firstName[0],
		'FIRSTNAME2' : firstName[1],
		'FIRSTNAME3' : firstName[2],
		'FIRSTNAME4' : firstName[3],
		'LASTNAME1' : lastName[0],
		'LASTNAME2' : lastName[1],
		'LASTNAME3' : lastName[2],
		'LASTNAME4' : lastName[3],
	}
	return render_template('demo.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
