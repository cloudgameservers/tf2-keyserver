import db, os, sys, re
import argparse
from os.path import join
from collections import namedtuple
tf2_key = namedtuple('tf2_key', "server_account server_token steam_account host")



# Initial setup of DB
# We keep the connection & cursor seperate so we can do commits when we want
dbPath = os.path.abspath("tf2_keys.db")
if not os.path.isfile(dbPath):
	db.createDB(dbPath)
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

parser = argparse.ArgumentParser(description='Manage TF2 keys')
parser.add_argument('-a', '--add', nargs=3,
	help="Add key, format: <server_account> <server_token> <steam_account>"
)
parser.add_argument('hosts', nargs='+', help="Hosts to retrieve keys for")
# Close the cursor & commit the DB one last time just for good measure
dbcursor.close()
dbconn.commit()
