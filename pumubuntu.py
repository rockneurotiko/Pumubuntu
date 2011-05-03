#!/usr/bin/env python

import gobject
import gtk
import appindicator
import pynotify

class OptionsWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title("Pumubuntu")
		self.main_box = gtk.VBox()
		self.box1 = gtk.HBox()
		self.label1 = gtk.Label("Work time (in minutes):")
		self.entry1 = gtk.Entry()
		self.box1.add(self.label1)
		self.box1.add(self.entry1)
		self.main_box.add(self.box1)
		self.box2 = gtk.HBox()
		self.label2 = gtk.Label("Short break time (in minutes):")
		self.entry2 = gtk.Entry()
		self.box2.add(self.label2)
		self.box2.add(self.entry2)
		self.main_box.add(self.box2)
		self.box3 = gtk.HBox()
		self.label3 = gtk.Label("Long break time (in minutes):")
		self.entry3 = gtk.Entry()
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
		self.main_box.add(self.box4)
		self.add(self.main_box)

	def options_event(self, button, event):
		if(event == "save"):
			print "Save data..."
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
	ind = appindicator.Indicator("Pumubuntu", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status (appindicator.STATUS_ACTIVE)
	ind.set_attention_icon("indicator-messages")

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
