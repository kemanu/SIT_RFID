import sqlite3 as lite
import SimpleMFRC522
import sys

con = lite.connect('RFID.db')
reader = SimpleMFRC522.SimpleMFRC522()
id,text = reader.read_no_block()

with con:
	cur = con.cursor()
	cur.execute("SELECT FirstName,LastName,Year FROM Users WHERE Id=?",(id,))
	data = cur.fetchone()
	if data == None:
		firstName = "N/A"
		lastName = "N/A"
		year = "N/A"
	else:
		firstName = data[0]
		lastName = data[1]
		year = data[2]
	print(firstName)
	print(lastName)
	print(year)

