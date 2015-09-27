#! /usr/bin/python
from __future__ import print_function
import argparse
import json
import sys
from collections import namedtuple

import tf2_db

tf2_key = namedtuple('tf2_key', "server_account server_token steam_account host")
db = tf2db()

parser = argparse.ArgumentParser(description='Manage TF2 keys')
parser.add_argument('-a', '--add', nargs=3,
  help="Add key, format: <server_account> <server_token> <steam_account>"
)
parser.add_argument('host', nargs='?', help="Host to retrieve keys for")
args = parser.parse_args()

if args.add:
  key = tf2_key(int(args.add[0]), args.add[1], args.add[2], args.host)
  db.addKey(key)
elif args.host:
  key = db.getKey(args.host)
  for entry in key:
    print(entry)
else:
  sys.exit(1)

db.close()
