import sqlite3 as lite
import sys
import SimpleMFRC522

con = lite.connect('RFID.db')
reader = SimpleMFRC522.SimpleMFRC522()

with con:

	cur = con.cursor()
	id,text = reader.read()
	first = raw_input("What is your first name? ")
	last = raw_input("What is your last name? ")
	year = input("What year are you (number)? ")
	cur.execute("INSERT INTO Users (Id, FirstName, LastName, Year) VALUES(?,?,?,?)",(id,first,last,year))
