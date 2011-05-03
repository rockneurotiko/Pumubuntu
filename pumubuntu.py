#!/usr/bin/env python

import gobject
import gtk
import appindicator
import pynotify

def menu_event(menu_item, event):
	if(event == "exit"):
		gtk.main_quit()

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
	gtk.main()
