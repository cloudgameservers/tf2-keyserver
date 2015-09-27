import sqlite3

def createDB(dbPath):
	conn = sqlite3.connect(dbPath)
	conn.text_factory = unicode
	c = conn.cursor()
	c.execute("""CREATE TABLE tf2_keys (
    "server_account" INTEGER PRIMARY KEY,
    "server_token" TEXT,
    "steam_account" TEXT,
    "host" TEXT)""")

def startDB(dbPath):
	try:
		conn = sqlite3.connect(dbPath)
		conn.text_factory = unicode
		c = conn.cursor()
		c.execute("SELECT * from tf2_keys")
	except sqlite3.OperationalError as e:
		print("SQLite3 Error : Operational Error", e.args[0])
	except sqlite3.DatabaseError as e:
		print("SQLite3 Error : Database Error", e.args[0])
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	except:
		print("Unknown Error")
	return conn

def addKey(db, key):
	try:
		db.execute(u"INSERT into tf2_keys VALUES (Null, ?, ?, ?, ?)", key)
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info

def getUnassignedKey(db):
	try:
		return db.execute(u"SELECT * from tf2_keys WHERE host IS Null Limit 1")
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])

def assignHost(db, host, account_id):
	try:
		db.execute(u"UPDATE tf2_keys set host = :host where server_account = :account",
			{"host":host, "account":account_id})
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info
