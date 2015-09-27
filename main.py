#! /usr/bin/python
from __future__ import print_function
import db, os, sys, re
import argparse
import json
from collections import namedtuple

tf2_key = namedtuple('tf2_key', "server_account server_token steam_account host")

# Initial setup of DB
# We keep the connection & cursor seperate so we can do commits when we want
dbPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tf2_keys.db")
if not os.path.isfile(dbPath):
  db.createDB(dbPath)
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

parser = argparse.ArgumentParser(description='Manage TF2 keys')
parser.add_argument('-a', '--add', nargs=3,
	help="Add key, format: <server_account> <server_token> <steam_account>"
)
parser.add_argument('host', nargs='?', help="Host to retrieve keys for")
args = parser.parse_args()

if args.add:
  key = tf2_key(int(args.add[0]), args.add[1], args.add[2], args.host)
  db.addKey(dbcursor, key)
elif args.host:
	print(json.dumps(tf2_key(*key)))
  key = db.getKey(dbcursor, args.host)
else:
  sys.exit(1)
# Close the cursor & commit the DB one last time just for good measure
dbcursor.close()
dbconn.commit()
