#!/usr/bin/env python3

'''
Simple wrapper around Gtk3 HeaderBar when using pyGobject allowing for a the HeaderBar to be enabled/disabled
while running without losing access to buttons placed in the HeaderBar. See wrapper_example.py for a usage example.

Works by wrapping HeaderBar pack_start and pack_end to pack to two separate GtkBox instances.
When enabling HeaderBar the GtkBox instances get packed on the HeaderBar and the HeaderBar is set as titlebar.
When disabling HeaderBar the GtkBox instances get packed in a GtkBox placed on the main content window.
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

def internal_set_titlebar(self, titlebar): #Gets passed either a None or a HeaderBar instance.
	position = self.get_position() #Get window position
	self.set_titlebar(titlebar) #Sets titlebar. If passed a None Server Side Decorations are used, otherwise the HeaderBar is loaded.
	self.move(position[0], position[1]) #As window position is lost this moves the newly reinitialized window to original position.

def make_wrapper(self):
	self.wrapperbar_start = Gtk.Box(spacing=6) #Initialize wrapperbar left container
	self.wrapperbar_end = Gtk.Box(spacing=6) #Initialize wrapperbar right container
	self.in_content_bar = Gtk.Box() #Initialize in_content_bar GtkBox
	self.in_content_bar.set_hexpand(True) #Allows the in_content_bar to maximize horizontally when placed in a Grid instance

	self.bar_placement = 'Decoration' #Variable tracking where bar is currently "placed"

	self.headerbar = Gtk.HeaderBar() #Creates the HeaderBar object
	self.headerbar.set_show_close_button(True) #Configures it
	self.headerbar.props.title = Gtk.Window.get_title(self) #Configures it

	self.headerbar.pack_start(self.wrapperbar_start) #Places wrapperbar contents in HeaderBar
	self.headerbar.pack_end(self.wrapperbar_end) #Places wrapperbar contents in HeaderBar

	self.set_titlebar(self.headerbar) #Set titlebar to use HeaderBar (HeaderBar is enabled by default)

def pack_start(self, widget): #wrapperbar replacement for the HeaderBar pack_start function
	self.wrapperbar_start.pack_start(widget, False, True, 0)

def pack_end(self, widget): #wrapperbar replacement for the HeaderBar pack_end function
	self.wrapperbar_end.pack_end(widget, False, True, 0)

'''
Enabling and disabling the HeaderBar throws a Gtk-WARNING.
This warning states that the window will be reinitialized by Gtk internally.
This has no side effects barring a slight delay and can be ignored or filtered out.
'''
def use_header(self, switch): #If switch is True HeaderBar will be enabled; if False HeaderBar is disabled
	if switch == True and self.bar_placement == 'InContent': #Ensure that if enabling HeaderBar the HeaderBar is not already enabled
		Gtk.Container.remove(self.in_content_bar, self.wrapperbar_start) #Remove wrapperbar contents from in_content_bar
		Gtk.Container.remove(self.in_content_bar, self.wrapperbar_end) #Remove wrapperbar contents from in_content_bar

		self.headerbar.pack_start(self.wrapperbar_start) #Places wrapperbar contents in HeaderBar
		self.headerbar.pack_end(self.wrapperbar_end) #Places wrapperbar contents in HeaderBar

		self.headerbar.props.title = Gtk.Window.get_title(self) #Set HeaderBar title to title of window
		internal_set_titlebar(self, self.headerbar) #Set titlebar to use HeaderBar

		self.bar_placement = 'Decoration' #Set tracking variable

	elif switch == False and self.bar_placement == 'Decoration': #Ensure that if disabled HeaderBar the HeaderBar is not already disabled
		Gtk.Container.remove(self.headerbar, self.wrapperbar_start) #Remove wrapperbar contents from HeaderBar
		Gtk.Container.remove(self.headerbar, self.wrapperbar_end) #Remove wrapperbar contents from HeaderBar

		self.in_content_bar.pack_start(self.wrapperbar_start, True, True, 0) #Places wrapperbar contents in in_content_bar
		self.in_content_bar.pack_end(self.wrapperbar_end, True, True, 0) #Places wrapperbar contents in in_content_bar

		internal_set_titlebar(self, None) #Set titlebar to use system titlebar

		self.bar_placement = 'InContent' #Set tracking variable