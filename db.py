from __future__ import print_function
import sqlite3

def createDB(dbPath):
  conn = sqlite3.connect(dbPath)
  conn.text_factory = unicode
  conn.row_factory = sqlite3.Row
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
    c.execute("SELECT * from tf2_keys limit 1")
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
    db.execute(u"INSERT into tf2_keys VALUES (?, ?, ?, ?)", key)
  except sqlite3.Error as e:
    print("SQLite 3: Unknown Error", e.args[0])

def getKey(db, host):
  try:
    exists = db.execute(u"SELECT COUNT(*) from tf2_keys WHERE host = ?", [host]).fetchone()[0]
    if exists != 1:
      row = db.execute(u"SELECT server_account from tf2_keys WHERE host IS Null Limit 1").fetchone()
      db.execute(u"UPDATE tf2_keys set host = :host where server_account = :account",
        {"host": host, "account": row[0]})
    return db.execute(u"SELECT * from tf2_keys WHERE host = ?", [host]).fetchone()
  except sqlite3.Error as e:
    print("SQLite 3: Unknown Error", e.args[0])
