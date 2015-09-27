from __future__ import print_function
import sqlite3
import os

class tf2db(object):

  def __init__(self, dbPath="tf2_keys.db"):
    # probably should do a check for dbpath being non-absolute...
    self.dbPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dbPath)
    if not os.path.isfile(self.dbPath):
      self.createDB(self.dbPath)
    self.conn = sqlite3.connect(self.dbPath)
    self.conn.text_factory = unicode
    self.conn.row_factory = sqlite3.Row
    self.c = self.conn.cursor()
    self.checkDB()

  @staticmethod
  def createDB(dbPath):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute("""CREATE TABLE tf2_keys (
      "server_account" INTEGER PRIMARY KEY,
      "server_token" TEXT,
      "steam_account" TEXT,
      "host" TEXT)""")
    c.close()
    conn.commit()

  def checkDB(self):
    try:
      self.c.execute("SELECT * from tf2_keys limit 1")
    except sqlite3.OperationalError as e:
      print("SQLite3 Error : Operational Error", e.args[0])
    except sqlite3.DatabaseError as e:
      print("SQLite3 Error : Database Error", e.args[0])
    except sqlite3.Error as e:
      print("SQLite 3: Unknown Error", e.args[0])
    except:
      print("Unknown Error")

  def addKey(self, key):
    try:
      self.c.execute(u"INSERT into tf2_keys VALUES (?, ?, ?, ?)", key)
    except sqlite3.Error as e:
      print("SQLite 3: Unknown Error", e.args[0])

  def getKey(self, host):
    try:
      exists = self.c.execute(u"SELECT COUNT(*) from tf2_keys WHERE host = ?", [host]).fetchone()[0]
      if exists != 1:
        row = self.c.execute(u"SELECT server_account from tf2_keys WHERE host IS Null Limit 1").fetchone()
        self.c.execute(u"UPDATE tf2_keys set host = :host where server_account = :account",
          {"host": host, "account": row[0]})
      return self.c.execute(u"SELECT * from tf2_keys WHERE host = ?", [host]).fetchone()
    except sqlite3.Error as e:
      print("SQLite 3: Unknown Error", e.args[0])

  def close(self):
    self.c.close()
    self.conn.commit()