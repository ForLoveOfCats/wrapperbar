#!/usr/bin/env python3

'''
HeaderBar Example from pyGobject tutorial modified to use wrapperbar in place of stock HeaderBar.
Original source: http://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html#headerbar
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import wrapperbar

class HeaderBarWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="HeaderBar Demo") #Initialize window as though not using a HeaderBar
		self.set_border_width(10)
		self.set_default_size(400, 200)

		wrapperbar.make_wrapper(self) #Run once to initialize the wrapper

		contents = Gtk.Grid() #Grid instance for window content
		contents.attach(self.in_content_bar, 0, 0, 1, 1) #Packing the in_content_bar GtkBox.
				#This GtkBox was created by wrapperbar.make_wrapper() and is empty when HeaderBar is in use.
				#When the HeaderBar is disabled, the contents of said HeaderBar is placed in this GtkBox.
				#For best results ensure that this GtkBox is displayed, is the highest widget in the window, and spans the entire window width.

		#All other window contents can be added to the Grid, even in another Container
		entry_box = Gtk.TextView() #Such As this TextView
		entry_box.set_vexpand(True)
		contents.attach(entry_box, 0, 1, 1, 1)
		self.add(contents) #Shows window content Grid

		#Construction of buttons in HeaderBar
		#This section was changed very minimally from original. These changes are to use wrapperbar pack calls
		button = Gtk.Button()
		button.connect("clicked", self.toggle_headerbar)
		icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		wrapperbar.pack_end(self, button) #wrapperbar pack call in place of HeaderBar pack call

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box.get_style_context(), "linked")

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		box.add(button)

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		box.add(button)

		wrapperbar.pack_start(self, box) #wrapperbar pack call in place of HeaderBar pack call

	def toggle_headerbar(self, test): #Simple callback function with toggles the use of HeaderBar
		if self.bar_placement == 'Decoration':
			wrapperbar.use_header(self, False) #Disable HeaderBar
		elif self.bar_placement == 'InContent':
			wrapperbar.use_header(self, True) #Enable HeaderBar

win = HeaderBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()