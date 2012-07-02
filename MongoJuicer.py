
import sublime, sublime_plugin
import json

from pymongo import Connection
from inspect import getmembers
from pprint import pprint

MongoViews = []

def dump(obj):
  '''return a printable representation of an object for debugging'''
  newobj=obj
  if '__dict__' in dir(obj):
    newobj=obj.__dict__
    if ' object at ' in str(obj) and not newobj.has_key('__type__'):
      newobj['__type__']=str(obj)
    for attr in newobj:
      newobj[attr]=dump(newobj[attr])
  return newobj

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global MongoViews
		connection = Connection('localhost', 27017)
		db = connection.UserControl
		collection = db.Users
		post = collection.find_one()
		thisWin = sublime.active_window()
		resultView = sublime.Window.new_file(thisWin)
		resultView.set_scratch(True)
		resultView.set_name('Funky Cold Medina')
		
		MongoViews.append(resultView.id())
		thisWin.focus_view(resultView)
		resultView.insert(edit, 0, str(post))
		# resultView.set_scratch(resultView, str(post), title="Mongo Items Output")

		# sublime_plugin.EventListener.on_pre_save(resultView)
		# self.view.insert(edit, 0, str(post))

class MongoJuicerListener(sublime_plugin.EventListener):
	def on_close(self, view):
		global MongoViews
		if ( view.is_scratch() and view.id() in MongoViews ):
			print 'view just closed was a mongo juice'
			answer = sublime.ok_cancel_dialog("Update Values?")
			if (answer):
				print "would be saving to mongo right here"
				print view.substr(sublime.Region(0, view.size()))
		# print view.isMongoJuice, ' mj?'
		# pprint(getmembers(view))

