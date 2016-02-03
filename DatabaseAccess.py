#!/usr/bin/python

"""
Database Manipulation!
"""

import os
import sqlite3

_db_filename = 'notes.db'
_schema_filename = 'notes_schema.sql'

# See if there is a database already

_db_is_new = not os.path.exists(_db_filename)


# Create one if there isn't 

with sqlite3.connect(_db_filename) as conn:
	if _db_is_new:
		print 'Creating database schema'
		with open(_schema_filename, 'rt') as f:
			_schema = f.read()
		conn.executescript(_schema)

		print 'Inserting some test data'
		
		conn.execute("""
		insert into notes (name, content)
		values ('The Flight', 'Here is a list of airlines that you can use to get to the island: \\n * Delta\\n * American');
		""")

		conn.execute("""
		insert into notes (name, content)
		values ('The City', 'The capital is known for its fine dining and white sandy beaches.');
		""")

		conn.execute("""
		insert into notes (name, content)
		values ('The Island', 'The permanent population of the island is 25,492. Many people visit the island in the summer.');
		""")

		conn.execute("""
		insert into notes (name, content)
		values ('The Food', "Enjoy the island's unique culenary traditions.");
		""")
	else:
		print "Using Existing Database"

def noteNameList():
	"""returns a list of (name,id) tuples. Covers every note in the database."""
	with sqlite3.connect(_db_filename) as conn:
		conn.text_factory = str
		cursor = conn.cursor()

		cursor.execute("""
		select name,id from notes;
		""")

		return [(row[0],row[1]) for row in cursor.fetchall()]


def addNote(name, content):
	"""Adds note to data base and returns the id of the new note"""
	with sqlite3.connect(_db_filename) as conn:
		conn.text_factory = str
		cursor = conn.cursor()

		query = """insert into notes (name, content) values (?, ?);"""

		cursor.execute(query, (name, content))
		return cursor.lastrowid
	return None

def getNote(id):
	"""Returns a (name, content) tuple for the given id."""
	with sqlite3.connect(_db_filename) as conn:
		conn.text_factory = str
		cursor = conn.cursor()

		query = u"""select name, content from notes where id = ?;"""

		cursor.execute(query, (id, ))

		data = [(row[0],row[1]) for row in cursor.fetchall()]

		if len(data) == 0:
			return []
		return data[0]
	return None

def updateNote(noteId, newName, newContent):
	"""Updates the note at the given ID, does nothing for an invalid id"""
	with sqlite3.connect(_db_filename) as conn:
		conn.text_factory = str
		cursor = conn.cursor()

		query = u"""update notes set name = :name,content = :content where id = :id"""

		cursor.execute(query, dict(id=noteId, name=newName, content=newContent))

def deleteNote(noteId):
	"""Deletes the note with the given ID"""
	with sqlite3.connect(_db_filename) as conn:
		conn.text_factory = str
		cursor = conn.cursor()

		query = u"""DELETE FROM notes where id = :id"""
		
		cursor.execute(query, dict(id=noteId))
		