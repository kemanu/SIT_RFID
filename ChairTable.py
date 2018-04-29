import sqlite3 as lite
import sys

con = lite.connect('RFID.db')

with con:

	cur = con.cursor()
	cur.execute("CREATE TABLE Chairs(ChairNumber INT, Id INT, Status TEXT)")
	cur.execute("INSERT INTO Chairs VALUES(1, 0, 'Available')")
	cur.execute("INSERT INTO Chairs VALUES(2, 0, 'Available')")
	cur.execute("INSERT INTO Chairs VALUES(3, 0, 'Available')")
	cur.execute("INSERT INTO Chairs VALUES(4, 0, 'Available')")
