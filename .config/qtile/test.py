#!/usr/bin/python3

import json
from libqtile import widget

rofimenu    = "rofi"
Terminal1   = "alacritty"

def widget_quick_launch_app( name, command, comment, icon):
    var = '''widget.LaunchBar( progs=(('{}', {}, '{}'),), default_icon='{}', padding=0,)'''.format(name, command, comment, icon)
    #var = json.dumps(var)

    #var = eval( var )
    #var = json.loads( var )
    #print(type(var))
    return var

#l = []

#l.append( [ widget_quick_launch_app( "Menu", rofimenu, "Rofi Menu", "/home/amol/.config/qtile/icons/view-grid.png" ) ] )
#l.append( [ widget_quick_launch_app( "Show Desktop", rofimenu, "Show Desktop", "/home/amol/.config/qtile/icons/view-grid.png" ) ] )
#print( l )

print( type(widget_quick_launch_app( "Menu", rofimenu, "Rofi Menu", "/home/amol/.config/qtile/icons/view-grid.png" ) ) )
print( widget_quick_launch_app( "Menu", rofimenu, "Rofi Menu", "/home/amol/.config/qtile/icons/view-grid.png" ) )

