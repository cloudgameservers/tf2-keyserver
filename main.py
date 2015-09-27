import db, os, sys, re
import argparse
from os.path import join
from collections import namedtuple
tf2_key = namedtuple('tf2_key', "server_account server_token steam_account host")

def hashAndAdd(file):
	# Check if it's a valid MP3 file first by trying to get the ID3 info
	try:
		title, artist, album = mp3.getid3(file)
	except Exception as e:
		# So far the only exception is an invalid ID3 header found, so not much to grab
		print(e)
		return
	mtime = os.path.getmtime(file)
	(exists,dbmtime) = db.checkIfExists(dbcursor, unicode(str(os.path.abspath(file)).decode('utf-8')))
	update = False
	# Gets back a tuple with (count of rows, mtime)
	# Check if the file has already been hashed
	if exists > 0:
		# If the file hasn't been modified since it was checked, don't bother hashing it
		if dbmtime >= mtime:
			return
		else:
			# Need to come up with an update statement...
			print("Updating", file)
			update = True

	tempfile = mp3.stripid3(file)
	strippedhash = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	originalhash = hash.sha512file(file)
	info = mp3info(title, artist, album, unicode(strippedhash), unicode(originalhash), unicode(str(os.path.abspath(file)).decode('utf-8')), mtime)
	if not update:
		print(info,"Ins")
		db.insertIntoDB(dbcursor, info)
	else:
		#print(info,"upd")
		db.updateDB(dbcursor, info)
	dbconn.commit()

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
