#!/usr/bin/env python

import gobject
import gtk
import appindicator
import pynotify
import json

PREFERENCES_FILENAME = "prefs.json"

class Preferences():
	def __init__(self):
		self.KEY_WORK_TIME = "WT"
		self.KEY_LONG_BREAK_TIME = "LT"
		self.KEY_SHORT_BREAK_TIME = "ST"
		self.DEFAULT_WORK_TIME = 25
		self.DEFAULT_LONG_BREAK_TIME = 15
		self.DEFAULT_SHORT_BREAK_TIME = 5

	def save_preferences(self, work_time, short_break_time, long_break_time):
		obj = {self.KEY_WORK_TIME: work_time, self.KEY_SHORT_BREAK_TIME: short_break_time, self.KEY_LONG_BREAK_TIME: long_break_time}
		dump = json.dumps(obj)
		file = open(PREFERENCES_FILENAME, "w")
		file.write(dump)
		file.close()

	def get_work_time(self):
		try:
			file = open(PREFERENCES_FILENAME, "r")
			dump = json.loads(file.read())
			file.close()
			return dump[self.KEY_WORK_TIME]
		except IOError:
			return self.DEFAULT_WORK_TIME

	def get_long_break_time(self):
		try:
			file = open(PREFERENCES_FILENAME, "r")
			dump = json.loads(file.read())
			file.close()
			return dump[self.KEY_LONG_BREAK_TIME]
		except IOError:
			return self.DEFAULT_LONG_BREAK_TIME

	def get_short_break_time(self):
		try:
			file = open(PREFERENCES_FILENAME, "r")
			dump = json.loads(file.read())
			file.close()
			return dump[self.KEY_SHORT_BREAK_TIME]
		except IOError:
			return self.DEFAULT_SHORT_BREAK_TIME

class OptionsWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title("Pumubuntu") # TODO: Set an icon for this window...
		self.prefs = Preferences()
		self.main_box = gtk.VBox()
		self.box1 = gtk.HBox()
		self.label1 = gtk.Label("Work time (in minutes):")
		self.entry1 = gtk.Entry()
		self.entry1.set_text(str(self.prefs.get_work_time()))
		self.box1.add(self.label1)
		self.box1.add(self.entry1)
		self.main_box.add(self.box1)
		self.box2 = gtk.HBox()
		self.label2 = gtk.Label("Short break time (in minutes):")
		self.entry2 = gtk.Entry()
		self.entry2.set_text(str(self.prefs.get_long_break_time()))
		self.box2.add(self.label2)
		self.box2.add(self.entry2)
		self.main_box.add(self.box2)
		self.box3 = gtk.HBox()
		self.label3 = gtk.Label("Long break time (in minutes):")
		self.entry3 = gtk.Entry()
		self.entry3.set_text(str(self.prefs.get_short_break_time()))
		self.box3.add(self.label3)
		self.box3.add(self.entry3)
		self.main_box.add(self.box3)
		self.box4 = gtk.HBox()
		self.button1 = gtk.Button(stock=gtk.STOCK_SAVE)
		self.button1.connect("clicked", self.options_event, "save")
		self.button2 = gtk.Button(stock=gtk.STOCK_QUIT)
		self.button2.connect("clicked", self.options_event, "quit")
		self.box4.add(self.button1)
		self.box4.add(self.button2)
		self.main_box.add(self.box4) # TODO: Add a restore values buttom...
		self.add(self.main_box)

	def options_event(self, button, event):
		if(event == "save"):
			if(self.entry1.get_text() != "" and self.entry2.get_text() != "" and self.entry3.get_text() != ""):
				try:
					values = map(int, [ self.entry1.get_text(), self.entry2.get_text(), self.entry3.get_text()])
					self.prefs.save_preferences(values[0], values[1], values[2])
				except ValueError:
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Please, just use entire numbers.")
					dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
					dialog.run()
					dialog.destroy()
		if(event == "quit"):
			self.destroy()


def menu_event(menu_item, event):
	if(event == "exit"):
		gtk.main_quit()
	if(event == "options"):
		OptionsWindow().show_all()

if __name__ == "__main__":
	if not(pynotify.init("Pumubuntu")):
		prit("[!] Error: Could not load pynotify...")
		exit()
	# Set an app indicator in system tray...
	ind = appindicator.Indicator("Pumubuntu", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS) # TODO: Need an icon...
	ind.set_status (appindicator.STATUS_ACTIVE)
	ind.set_attention_icon("indicator-messages") # TODO: Also need an icon...

	# Indicator menu...
	menu = gtk.Menu()
	menu_item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
	menu_item.connect("activate", menu_event, "options")
	menu_item.show()
	menu.append(menu_item)
	menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
	menu_item.connect("activate", menu_event, "exit")
	menu_item.show()
	menu.append(menu_item)
	ind.set_menu(menu)
	try:
		gtk.main()
	except KeyboardInterrupt:
		print("")
		exit()
