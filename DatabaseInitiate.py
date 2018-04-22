import sqlite3 as lite
import sys

con = lite.connect('RFID.db')

with con:

	cur = con.cursor()
	cur.execute("CREATE TABLE Users(Id INT, FirstName TEXT, LastName TEXT, Year INT)")


