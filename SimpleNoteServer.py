#!/usr/bin/python

"""How to use:

> python SimpleNoteServer.py 0.0.0.0 8001
serving on 0.0.0.0:8001

> python SimpleNoteServer.py 8080
Serving on localhost:8080

> python SimpleNoteServer.py
Serving on localhost:8000 """

import SimpleHTTPServer
import SocketServer
import logging
import cgi

import sys
import random as rnd

import DatabaseAccess as db

print db.noteNameList()

print db.getNote("10")



if len(sys.argv) > 2:
	PORT = int(sys.argv[2])
	I = sys.argv[1]
elif len(sys.argv) > 1:
	PORT = int(sys.argv[1])
	I = ""
else:
	PORT = 8000
	I = ""

notes = {
	"The Flight":"Here is a list of airlines that you can use to get to the island: \n * Delta\n * American",
	"The City":"The capital is known for its fine dining and white sandy beaches.",
	"The Island":"The permanent population of the island is 25,492. Many people visit the island in the summer.",
	"The Food":"Enjoy the island's unique culenary traditions."
	}

noteList = ""
noteListDirty = True

def getNoteListCached():
	global noteListDirty, noteList

	if noteListDirty:
		noteList = ""
	
		for name,id in db.noteNameList():
			noteList += """<li onclick="loadNote('""" + str(id) + """')">""" + name + """</li>"""
		noteListDirty = False
		return noteList
	else:
		return noteList

editorHTML="""<div>Name: <input type="text" id="Name" value="{name}" /></div>
            <div><textarea rows="20" cols="80" id="Content">{value}</textarea></div>
            
            <div >
                <button id="Save" onclick="saveNote({id})">Save</button>
                <button id="Delete" onclick="deleteNode({id})">Delete</button>
            </div>"""

def createNote(path, args):
	if "name" in args:
		global noteListDirty
		noteListDirty = True
		db.addNote(args["name"], "")
	
	return getNoteListCached()


def loadNote(path, args):
	if not "id" in args:
		return editorHTML.format(name="", value = "", id = "")
	nodeInfo = db.getNote(args["id"])
	
	return  editorHTML.format(name=nodeInfo[0], value = nodeInfo[1], id = args["id"])

def saveNote(path, args):
	
	if not "id" in args:
		return getNoteListCached()

	if "name" in args:
		name = args["name"]
	else:
		name = ""
	
	if "content" in args:
		content = args["content"]
	else:
		content = ""

	global noteListDirty
	noteListDirty = True
	db.updateNote(args["id"],name,content)
	
	return getNoteListCached()


def getNoteList(path,args): return getNoteListCached()


def deleteNote(path, args):
	if not "id" in args:
		return getNoteListCached()
	
	nodeId = args["id"]
	
	global noteListDirty
	noteListDirty = True
	db.deleteNote(nodeId)

	return getNoteListCached()

postInternals = {
	"/newNote":createNote,
	"/loadNote":loadNote,
	"/saveNode":saveNote,
	"/refreshNoteList":getNoteList,
	"/deleteNote": deleteNote		 
				 }

def getPostResoponse(path, args):
	if path in postInternals:
		return postInternals[path](path,args)
	return None

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	
	verbose = False

	def do_GET(self):
		
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })
		
		argsDict = {}
		for item in form.list:
			argsDict[item.name] = item.value
		
		RESPONSE = getPostResoponse(self.path, argsDict)
		if RESPONSE == None:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
			return
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-length", len(RESPONSE))
		self.end_headers()
		self.wfile.write(RESPONSE)
	
	def log_message(self, format, *args):
		if self.verbose == True:
			impleHTTPServer.SimpleHTTPRequestHandler.log_message(format, *args)
		else:
			return None

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()