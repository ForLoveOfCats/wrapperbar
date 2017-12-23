#Wrapperbar is a wrapper around Gtk3 HeaderBar for Python 3.x

##Why use it?

Gtk3 has a feature called HeaderBar which allows developers to place custom buttons, controls, and various widgets in the Titlebar of their applications. When running under Gnome Shell 3 this looks natural and fits in with the design philosophy of Gnome Shell. However under other Desktop Environments or Window Managers this looks very much out of place. Wrapperbar is a HeaderBar wrapper which allows for the user to toggle the use of HeaderBar without requiring developers to maintain duplicated code. With an API almost exactly like that of HeaderBar, wrapperbar does not require the learning of a new paradigm. See wrapper_example.py for usage example.