
import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile.command.client import CommandClient
from libqtile import layout, bar, widget, hook
from libqtile import extension
from libqtile import qtile
from typing import List  # noqa: F401

##### VARIABLES #####
homedir             = os.path.expanduser('~')
configdir           = [ homedir + '/.config/qtile' ]

# My Programs
dmenu               = "dmenu_run -f -i -l 10 \
                        -nb '#151617' -nf '#d8d8d8' -sb '#a4bd00' -sf '#151617'\
                        "
rofi                = "rofi -show drun -modi drun,run,window -show-icons \
                        -sidebar-mode -fake-transparency -display-drun '' \
                        -theme ~/.config/qtile/rofi/themes/Siera-alt.rasi \
                        "

rofimenu            = "rofi -show drun -modi drun,run,window -show-icons \
                        -fake-transparency -display-drun 'Apps ' -display-run 'Cmds ' \
                        -display-window 'Windows ' -scroll-method 0 -sidebar-mode \
                        -lines 20 -columns 1 -terminal st \
                        -theme ~/.config/qtile/rofi/themes/arc-red-dark-menu.rasi\
                        "

rofiwindowswitcher  = "rofi -show window -modi window -cycle -show-icons \
                        -display-window 'Windows ' -window-format '{w} {c} {t} {n}' \
                        -scroll-method 0 -lines 10 -columns 10 -eh 2 \
                        -padding 2% -spacing 2% -fake-transparency \
                        -theme ~/.config/qtile/rofi/themes/arc-red-dark.rasi\
                        "

TerminalFirstChoice     = "alacritty -e bash -l"

TerminalSecondChoice    = "sakura -l"

# Backup option, one thats in the repos and launched with Ctrl + Alt + t
TerminalBackup      = "urxvt -e bash -l"

FileManager         = "pcmanfm"
#FileManager = "rox-filer -n"

#WebBrowser = "qutebrowser"
WebBrowser          = "firefox"

TextEditor          = "gedit"

VolumeMuteCmd       = "/home/amol/.config/qtile/volume.sh mute"
VolumeUnmuteCmd     = "/home/amol/.config/qtile/volume.sh mute"
VolumeUpCmd         = "/home/amol/.config/qtile/volume.sh up"
VolumeDownCmd       = "/home/amol/.config/qtile/volume.sh down"
#VolumeMuteCmd      = "pactl set-sink-mute @DEFAULT_SINK@ toggle"
#VolumeUnmuteCmd    = "pactl set-sink-mute @DEFAULT_SINK@ false"
#VolumeUpCmd        = "pactl set-sink-volume @DEFAULT_SINK@ +5%"
#VolumeDownCmd      = "pactl set-sink-volume @DEFAULT_SINK@ -5%"

BrightnessUpCmd     = "/home/amol/.config/qtile/brightness.sh up"
#BrightnessUpCmd     = [ homedir + '.config/qtile/brightness.sh up' ]
BrightnessDownCmd   = "/home/amol/.config/qtile/brightness.sh down"
#BrightnessUpCmd    = [ homedir + '/.config/qtile/brightness.sh up' ]
#BrightnessDownCmd  = [ homedir + '/.config/qtile/brightness.sh down' ]
#BrightnessUpCmd    = "sudo brightnessctl s +1%"
#BrightnessDownCmd  = "sudo brightnessctl s 1%-"


##### KEYBOARD SHORTCUTS #####
mod                 = "mod4"        # DO NOT REMOVE mod = "modkey"
Win                 = "mod4"        # Sets mod key to SUPER/WINDOWS
Control             = "control"
Alt                 = "mod1"
Shift               = "shift"

VolumeMuteKey       = "XF86AudioMute"
VolumeDownKey       = "XF86AudioLowerVolume"
VolumeUpKey         = "XF86AudioRaiseVolume"

BrightnessUpKey     = "XF86MonBrightnessUp"
BrightnessDownKey   = "XF86MonBrightnessDown"

#slash              = "/"


##### COLORS #####
color_black         = "#000000"
color_white         = "#ffffff"
color_silver        = "#888888"
color_grey1         = "#434752"
color_grey2         = "#404040"
color_yellow        = "#b4ff00"
color_green         = "#00ff00"
color_dull_green    = "#a4bd00"
color_orange        = "#ec883a"
color_red           = "#d33264"
color_red2          = "#ff4444"
color_teal          = "#298876"
color_blue          = "#5599cc"
color_purple        = "#A77AC4"

# COOL EMOJIS
# ⚡🔋 🔊  ☵ ↯ ⟳ ♫ 🕒 🔥 🗖 🗗 🗕


##### KEYBOARD FUNCTIONS #####
def window_to_previous_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    previous_group_name = qtile.current_group.get_previous_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(previous_group_name)
    elif layout.current == 0 and len(layout.cc) == 1:
        if group_index != 0:
            qtile.current_window.togroup(previous_group_name)
    else:
        layout.cmd_shuffle_left()


def window_to_next_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    next_group_name = qtile.current_group.get_next_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(next_group_name)
    elif layout.current + 1 == len(layout.columns) and len(layout.cc) == 1:
        if group_index + 1 != len(qtile.groups):
            qtile.current_window.togroup(next_group_name)
    else:
        layout.cmd_shuffle_right()


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


keys = [
    #Key([Control, Alt], "delete", lazy.shutdown()),
    Key([Win, Shift],   "q",    lazy.shutdown()),
    Key([Win, Control], "r",    lazy.restart()),

    Key([Win],          "q",    lazy.window.kill()),

    # Run Command
    Key([Win],          "r",    lazy.spawncmd()),
    Key([Win, Alt],     "r",    lazy.spawn(rofi)),

    Key([Win], "Return",        lazy.spawn(TerminalFirstChoice)),
    Key([Alt], "Return",        lazy.spawn(TerminalSecondChoice)),
    Key([Win], "space",         lazy.spawn(rofimenu)),
    Key([Alt], "space",         lazy.spawn(dmenu)),

    # Switch window focus to other pane(s) of stack
    Key([Win], "Tab",           lazy.layout.next()),
    Key([Win, Shift], "Tab",    lazy.layout.previous()),
    #Key([Alt], "Tab", lazy.spawn(rofiwindowswitcher)),

    # Workspace & Window switching
    Key([Win], "Left", lazy.screen.prev_group(skip_managed=True)),
    Key([Win], "Right", lazy.screen.next_group(skip_managed=True)),

    Key([Win, Shift], "Left", lazy.function(window_to_previous_column_or_group)),
    Key([Win, Shift], "Right", lazy.function(window_to_next_column_or_group)),

    Key([Win, Control], "Up", lazy.layout.grow_up()),
    Key([Win, Control], "Down", lazy.layout.grow_down()),
    Key([Win, Control], "Left", lazy.layout.grow_left()),
    Key([Win, Control], "Right", lazy.layout.grow_right()),

    Key([Win, Alt], "Left", lazy.prev_screen()),
    Key([Win, Alt], "Right", lazy.next_screen()),

    Key([Win, Shift, "mod1"], "Left", lazy.function(window_to_previous_screen)),
    Key([Win, Shift, "mod1"], "Right", lazy.function(window_to_next_screen)),

    Key([Win], "t", lazy.function(switch_screens)),

    Key([Win], "Up", lazy.group.prev_window()),
    Key([Win], "Down", lazy.group.next_window()),

    Key([Win, Shift], "Up", lazy.layout.shuffle_up()),
    Key([Win, Shift], "Down", lazy.layout.shuffle_down()),

    Key([Win], "n",             lazy.window.toggle_minimize()),
    Key([Win, Alt], "n",        lazy.layout.normalize()),
    Key([Win],      "o",        lazy.layout.maximize()),
    Key([Win], "m",             lazy.window.toggle_maximize()),
    Key([Win], "t",             lazy.window.toggle_floating()),
    Key([Win], "f",             lazy.window.toggle_fullscreen()),
    Key([Win], "g",             lazy.togroup()),
    Key([Win], "slash",         lazy.findwindow()),

    # Switch between windows in current stack pane
    Key([Win], "j",             lazy.layout.down()),
    Key([Win], "k",             lazy.layout.up()),
    Key([Win], "h",             lazy.layout.left()),
    Key([Win], "l",             lazy.layout.right()),

    # Move windows up or down in current stack
    Key([Win, Control], "j",    lazy.layout.shuffle_down()),
    Key([Win, Control], "k",    lazy.layout.shuffle_up()),
    Key([Win, Control], "h",    lazy.layout.shuffle_left()),
    Key([Win, Control], "l",    lazy.layout.shuffle_right()),

    # Grow windows
    Key([Win, Alt], "h",        lazy.layout.grow_left()),
    Key([Win, Alt], "l",        lazy.layout.grow_right()),
    Key([Win, Alt], "j",        lazy.layout.grow_down()),
    Key([Win, Alt], "k",        lazy.layout.grow_up()),

    # Flip windows
    Key([Win, Shift], "h",      lazy.layout.flip_left()),
    Key([Win, Shift], "l",      lazy.layout.flip_right()),
    Key([Win, Shift], "j",      lazy.layout.flip_down()),
    Key([Win, Shift], "k",      lazy.layout.flip_up()),

    # Swap panes of split stack
    Key([Win, "shift"], "space",    lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([Win, "shift"], "Return",   lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([Win, Control, Shift], "Tab",   lazy.next_layout()),

    #Special Keys
    Key([], VolumeMuteKey,      lazy.spawn(VolumeMuteCmd)),
    Key([], VolumeUpKey,        lazy.spawn(VolumeUpCmd)),
    Key([], VolumeDownKey,      lazy.spawn(VolumeDownCmd)),
    Key([], BrightnessUpKey,    lazy.spawn(BrightnessUpCmd)),
    Key([], BrightnessDownKey,  lazy.spawn(BrightnessDownCmd)),

    # My Apps
    Key([Win],          "e",    lazy.spawn(FileManager)),
    Key([Control, Alt], "i",    lazy.spawn(WebBrowser)),
    Key([Control, Alt], "t",    lazy.spawn(TerminalBackup)),
    Key([Control, Alt], "n",    lazy.spawn(TextEditor)),

    ## Workspace/Group Keys

    ## Switch to another group
    # Key([Win], "1", lazy.group["1"].toscreen()),

    ## Send current window to another group
    # Key([Win, "shift"], "1", lazy.window.togroup("1")),


]


##### GROUPS #####
#groups = [Group(i) for i in "12345678"]
#
#for i in groups:
#    keys.extend([
#        # mod1 + letter of group = switch to group
#        Key([mod], i.name, lazy.group[i.name].toscreen()),
#
#        # mod1 + shift + letter of group = switch to & move focused window to group
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
#    ])
#

# Start with no groups, prevents groups from appending in case of a qtile reload.
groups = []

group_names = [
	("1", {'layout': 'monadtall'}),
	("2", {'layout': 'tile'}),
	("3", {'layout': 'max'}),
	("4", {'layout': 'zoomy'}),
	("5", {'layout': 'zoomy2'}),
	("6", {'layout': 'ratiotile'}),
	("7", {'layout': 'stack'}),
	("8", {'layout': 'floating'}),
	]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group



##### THE LAYOUTS #####

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {
	"border_width": 2,
	"margin": 10,
	"max_border_width": 2,
	"border_focus": color_grey1,
	"border_normal": color_black,
	#"border_focus": "AD69AF", #Pink
	#"border_focus": "a4bd00", #Lime
	#"border_focus_stack": "888888",
	#"border_normal_stack": "1D2330",
	}

layouts = [
    layout.MonadTall(ratio=0.6,**layout_theme),
    layout.Tile(shift_windows=False, **layout_theme),
    layout.Floating(**layout_theme),
    layout.MonadTall(name='zoomy2',ratio=0.75,**layout_theme),
    layout.Columns(**layout_theme),
    layout.Zoomy(
        columnwidth = 250,
        **layout_theme
        ),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         #sections = ["FIRST", "SECOND"],
         section_fontsize = 11,
         #bg_color = color_black,
         active_bg = color_white,
         active_fg = color_black,
         inactive_bg = color_grey1,
         inactive_fg = color_white,
         padding_x = 16,
         padding_y = 16,
         section_top = 10,
         panel_width = 200,
         ),
    layout.Max(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.RatioTile(fancy=True,**layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Stack(num_stacks=2, autosplit=False,**layout_theme),
    #layout.Slice( **layout_theme),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
]



##### PROMPT #####
#prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
#prompt = "run: "
#prompt = "> "


##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    #font = 'DejaVu Sans',
    #font = 'Roboto Mono for Powerline',
    #font = "Ubuntu Mono",
    #font = "Awesome Font",
    font = "Ubuntu Bold",
    fontsize = 10,
    foreground = color_white,
    background = color_black,
    rounded = False,
    #rounded = True,
    linewidth = 0,
    padding = 5,
)
extension_defaults = widget_defaults.copy()

##### MOUSE CALLBACKS #####

def open_calendar():
    qtile.cmd_spawn('gsimplecal next_month')

def open_cpu_monitor():
    qtile.cmd_spawn('gsimplecal next_month')

def open_mem_monitor():
    qtile.cmd_spawn('/home/amol/.config/qtile/mem.sh')

def open_battery_monitor():
    qtile.cmd_spawn('/home/amol/.config/qtile/battery.sh')

# notify-send "$( head -3 /proc/meminfo )"

##### WIDGETS #####

#               widget.LaunchBar(
#                        #progs = ( (software_name, command_to_execute, comment),),
#                        progs = ( ('Menu', rofimenu, 'Rofi Menu'),),
#                        default_icon = "/home/amol/.config/qtile/icons/view-grid.png",
#                        padding = 0,
#                        ),

#def widget_quick_launch_apps():
#    apps_list =[
#        #[ software_name, command_to_execute, comment, default_icon ],
#        { "name": 'Menu',           "command": rofimenu,        "comment": 'Rofi Menu',     "icon": '/home/amol/.config/qtile/icons/view-grid.png' },
#        { "name": 'Firefox',        "command": 'firefox',       "comment": 'Firefox Web Browser', "icon": '/home/amol/.config/qtile/icons/firefox.png' },
#        { "name": 'Qutebrowser',    "command": 'qutebrowser',   "comment": '', "icon": '/home/amol/.config/qtile/icons/qutebrowser.png' },
#        { "name": 'File Manager',   "command": 'pcmanfm',       "comment": '', "icon": '/home/amol/.config/qtile/icons/pcmanfm.png' },
#        { "name": 'Text Editor',    "command": 'gedit',         "comment": '', "icon": '/home/amol/.config/qtile/icons/texteditor.png' },
#        { "name": 'Terminal',       "command": TerminalFirstChoice,       "comment": '', "icon": '/home/amol/.config/qtile/icons/terminal2.png' },
#        { "name": 'Cryptomator',    "command": 'cryptomator',   "comment": '', "icon": '/home/amol/.config/qtile/icons/cryptomator.png' },
#        { "name": 'KeePassXC',      "command": 'keepassxc',     "comment": '', "icon": '/home/amol/.config/qtile/icons/keepassxc.png' },
#        ]
#
#    widgets_list = ""
#    for app in apps_list:
#        widgets_item = "widget.LaunchBar( progs = ( ( '{}' , '{}', '{}' ), ), default_icon = '{}', padding = 0,),\n".format(app["name"], app["command"], app["comment"], app["icon"])
#        widgets_list = widgets_list + widgets_item
#
#    #print( widgets_list )
#    return widgets_list

def widget_separator_default():
    return widget.Sep( linewidth = 0, padding = 5,)

#def widget_quick_launch_app():
#    return widget.LaunchBar( progs=(('Menu', rofimenu, 'Rofi Menu'),), default_icon='/home/amol/.config/qtile/icons/view-grid.png', padding=0,)

#def widget_quick_launch_app( name, command, comment, icon):
#    return "widget.LaunchBar( progs=(('{}', '{}', '{}'),), default_icon='{}', padding=0,)".format(name, command, comment, icon)

#def widget_launchbar_firefox():
#		return widget.LaunchBar( progs=(('Firefox', 'firefox', 'Firefox Web Browser'),), default_icon='/home/amol/.config/qtile/icons/firefox.png', padding=0,)

quick_launch_bar_apps = '''
{
    "apps": [
        {
            "name"      : "Menu",
            "command"   : rofimenu,
            "comment"   : "Rofi Menu",
            "icon"      : "/home/amol/.config/qtile/icons/view-grid.png",
        },
        {
            "name"      : "Firefox",
            "command"   : "firefox",
            "comment"   : "Firefox Web Browser",
            "icon"      : "/home/amol/.config/qtile/icons/firefox.png",
        },
        {
            "name"      : "File Manager",
            "command"   : "pcmanfm",
            "comment"   : "",
            "icon"      : "/home/amol/.config/qtile/icons/pcmanfm.png",
        },
        {
            "name"      : "Text Editor",
            "command"   : "gedit",
            "comment"   : "",
            "icon"      : "/home/amol/.config/qtile/icons/texteditor.png",
        },
        {
            "name"      : "Terminal",
            "command"   : TerminalFirstChoice,
            "comment"   : "",
            "icon"      : "/home/amol/.config/qtile/icons/terminal2.png",
        },
        {
            "name"      : "Cryptomator",
            "command"   : "cryptomator",
            "comment"   : "",
            "icon"      : "/home/amol/.config/qtile/icons/cryptomator.png",
        },
        {
            "name"      : "KeePassXC",
            "command"   : "keepassxc",
            "comment"   : "",
            "icon"      : "/home/amol/.config/qtile/icons/keepassxc.png",
        },
    ]
}
'''


def init_widgets_list():
    widgets_list = [
                widget_separator_default(),
                #widget_quick_launch_app( "Menu", rofimenu, "Rofi Menu", "/home/amol/.config/qtile/icons/view-grid.png" ),
                #widget_launchbar_firefox(),
		widget.LaunchBar( progs=(('Menu', rofimenu, 'Rofi Menu'),), default_icon='/home/amol/.config/qtile/icons/view-grid.png', padding=0,),
                widget_separator_default(),
		widget.LaunchBar( progs=(('Firefox', 'firefox', 'Firefox Web Browser'),), default_icon='/home/amol/.config/qtile/icons/firefox.png', padding=0,),
                widget_separator_default(),
		#widget.LaunchBar( progs=(('Qutebrowser', 'qutebrowser', ''),), default_icon='/home/amol/.config/qtile/icons/qutebrowser.png', padding=0,),
		#widget_separator_default(),
		widget.LaunchBar( progs=(('File Manager', 'pcmanfm', ''),), default_icon='/home/amol/.config/qtile/icons/pcmanfm.png', padding=0,),
		widget_separator_default(),
		widget.LaunchBar( progs=(('Text Editor', 'gedit', ''),), default_icon='/home/amol/.config/qtile/icons/texteditor.png', padding=0,),
		widget_separator_default(),
		widget.LaunchBar( progs=(('Terminal', TerminalFirstChoice, ''),), default_icon='/home/amol/.config/qtile/icons/terminal2.png', padding=0 ,),
		widget_separator_default(),
		widget.LaunchBar( progs=(('Cryptomator', 'cryptomator', ''),), default_icon='/home/amol/.config/qtile/icons/cryptomator.png', padding=0,),
		widget_separator_default(),
		widget.LaunchBar( progs=(('KeePassXC', 'keepassxc', ''),), default_icon='/home/amol/.config/qtile/icons/keepassxc.png', padding=0,),
		widget_separator_default(),
		widget.TaskList(
                        linewidth = 10,
                        highlight_method = 'block' ,
                        #highlight_method = 'border' ,
                        #title_width_method = 'uniform',
                        max_title_width = 100,
                        border = color_grey1,
                        #fmt = 'center',
                        icon_size = 24,
                        txt_maximized = "🗖 ",
                        txt_minimized = "🗕 ",
                        txt_floating = "🗗 ",
                        #margin_y = 5,
                        borderwidth = 5,
                        padding = 8,
                        ),
		widget_separator_default(),
		widget.Prompt(
                        prompt="> ",
                        ignore_dups_history=True,
                        #font="Ubuntu Mono",
                        font="DejaVu Sans Mono",
                        foreground = color_red2,
                        padding=10,
                        ),
		widget_separator_default(),
		widget.CurrentLayout(
                        foreground = color_silver,
                        fontsize = 10,
                        padding = 1,
                        ),
		widget.CurrentLayoutIcon( scale = 0.6,),
		widget_separator_default(),
		widget.Clock(
                        foreground = color_dull_green,
                        format="%a %b %d %I:%M",
                        fontsize = 12,
                        mouse_callbacks = { 'Button1': open_calendar },
                        ),
		widget_separator_default(),
		widget.GroupBox(
                        #font="Ubuntu Bold",
                        #fontsize = 10,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 1,
                        #active = "a4bd00",
                        active = color_white,
                        inactive = color_white,
                        highlight_method = "block",
                        #this_current_screen_border = color_dull_green,
                        this_current_screen_border = color_grey1,
                        #this_screen_border = color_grey1,
                        #other_current_screen_border = color_black,
                        #other_screen_border = color_black,
                        #margin_y = 0,
                        #margin_x = 0,
                        ),
		widget_separator_default(),
		widget.Cmus(
                        max_chars = 40,
                        update_interval = 0.5,
                        play_color = color_white,
                        noplay_color = color_grey1,
                        ),
		widget_separator_default(),
               #widget.TextBox(
               #         text=" ⟳",
               #         foreground=color_white,
               #         fontsize=14
               #         ),
               #widget.Pacman(
               #         execute = "alacritty",
               #         update_interval = 1800,
               #         ),
               #widget.TextBox( text="TEMP", foreground = color_silver, background=color_black, fontsize = 12, padding = 0,),
		widget.ThermalSensor(
                        metric = True,
                        update_interval = 5,
                        foreground = color_red,
                        ),
               #widget.TextBox(
               #         #text="CPU",
               #         text="C",
               #         foreground = color_silver,
               #         fontsize = 12,
               #         padding = 0,
               #         ),
               #widget.CPU(
               #         fmt = '{}',
               #         ),
		widget.CPUGraph(
                        type = 'box',
                        line_width = 3,
                        fill_color = color_yellow,
                        graph_color = color_yellow,
                        border_width = 0,
                        width = 24,
                        margin_y = 6,
                        padding = 1,
                        ),
               #widget_separator_default(),
               #widget.TextBox(
               #         #text="Mem",
               #         text="M",
               #         foreground = color_silver,
               #         fontsize = 12,
               #         padding = 0,
               #         ),
		widget.Memory(
                        format = '{MemUsed}M',
                        foreground = color_orange,
                        mouse_callbacks = { 'Button1': open_mem_monitor },
                        ),
		widget.MemoryGraph(
                        type = 'box',
                        #type = 'linefill',
                        frequency = 5,
                        line_width = 1,
                        fill_color = color_orange,
                        graph_color = color_orange,
                        border_width = 0,
                        width = 24,
                        margin_y = 6,
                        ),
               #widget_separator_default(),
               #widget.TextBox(
               #         #text="Disk",
               #         text="D",
               #         foreground = color_silver,
               #         padding = 0,
               #         ),
		widget.DF(
                        format = '{uf}{m}',
                        measure = 'G',
                        update_interval	= 300,
                        foreground = color_red2,
                        ),
		widget.HDDBusyGraph(
                        type = 'box',
                        #type = 'linefill',
                        frequency = 1,
                        line_width = 1,
                        fill_color = color_red2,
                        graph_color = color_red2,
                        border_width = 0,
                        width = 24,
                        margin_y = 6,
                        ),
               #widget_separator_default(),

               #widget.TextBox(
               #         text='',
               #         background = color_blue,
               #         padding=0,
               #         fontsize=37
               #         ),
               #widget.TextBox(
               #         #text=" ↯",
               #         #text="Net",
               #         text="N",
               #         foreground = color_silver,
               #         background=color_black,
               #         fontsize = 12,
               #         padding = 0,
               #         ),
               #widget.Net(
               #         interface = "wlp2s0",
               #         update_interval = 3,
               #         foreground = color_teal,
               #         width = 80,
               #         fontsize = 8,
               #         ),
		widget.NetGraph(
                        interface = "auto",     #interface = "wlp2s0",
                        bandwidth_type = "down",
                        frequency = 3,
                        type = 'box',           # possible values = box|line|linefill
                        line_width = 3,
                        fill_color = color_white,
                        graph_color = color_teal,
                        border_width = 0,
                        margin_y = 6,
                        width = 16,
                        ),
		widget.NetGraph(
                        interface = "auto",     #interface = "wlp2s0",
                        bandwidth_type = "up",
                        type = 'box',           # possible values = box|line|linefill
                        line_width = 1,
                        fill_color = color_black,
                        graph_color = color_blue,
                        border_width = 0,
                        margin_y = 6,
                        width = 16,
                        ),
               #widget_separator_default(),
               #widget.TextBox(
               #         text='',
               #         foreground = color_blue,
               #         padding=0,
               #         fontsize=37
               #         ),
               #widget.TextBox(
               #         text=" ☵",
               #         foreground=color_white,
               #         background=color_blue,
               #         fontsize=14
               #         ),
               #widget.TextBox(
               #         text='',
               #         background = color_blue,
               #         foreground = color_black,
               #         padding=0,
               #         fontsize=37
               #         ),
               #widget_separator_default(),
               #widget.TextBox(
               #         text=" 🔊",
               #         padding = 0,
               #         fontsize=14
               #         ),
               #widget.PulseVolume(
               #         ),
               #widget.Volume(
               #         #get_volume_command = "",
               #         mute_command = "pactl set-sink-mute 0 true",
               #         volume_up_command = "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 +5%",
               #         volume_down_command = "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 -5%",
               #         foreground = "888888",
               #         ),
		widget.Systray(),
		widget.BatteryIcon(
                        #theme_path="/home/amol/.config/qtile/icons/laptop_battery.png",
                        mouse_callbacks = { 'Button1': open_battery_monitor },
                        update_interval=2,
                        padding = 0,
                        ),
		widget.Battery(
                        notify_below = 10,
                        mouse_callbacks = { 'Button1': open_battery_monitor },
                        #theme_path="/home/amol/.config/qtile/icons/laptop_battery.png",
                        #format="{char} {percent:2.0%}  {hour:d}:{min:02d} ",
                        format="{percent:2.0%}  {hour:d}:{min:02d} {char}",
                        #format="{percent:2.0%}  {hour:d}:{min:02d}",
                        charge_char="⚡", discharge_char="🔋",
                        full_char="⚡", unknown_char="⚡",
                        empty_char="⁉️ ", update_interval=2,
                        padding = 0,
                        ),
		widget_separator_default(),
		widget.LaunchBar( progs = ( ('Suspend', 'systemctl suspend', 'Sleep'),), default_icon="/home/amol/.config/qtile/icons/suspend.png", padding = 0,),
                widget_separator_default(),
		widget.LaunchBar( progs = ( ('logoff', 'qshell:self.qtile.cmd_shutdown()', 'logout from qtile'),), default_icon="/home/amol/.config/qtile/icons/logoff.png", padding = 0,),
                widget_separator_default(),
		widget.LaunchBar( progs = ( ('Exit Menu', '/home/amol/.config/qtile/rofi/rofi-exit.sh', 'Exit'),), default_icon="/home/amol/.config/qtile/icons/stock_exit.png", padding = 0,),
		widget_separator_default(),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.9, size=32)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.9, size=32)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.9, size=32))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list	= init_widgets_list()
    widgets_screen1	= init_widgets_screen1()
    widgets_screen2	= init_widgets_screen2()

##### DRAG FLOATING WINDOWS #####
mouse = [
    Drag([mod],		"Button1", lazy.window.set_position_floating(),	start=lazy.window.get_position()),
    Drag([mod],		"Button3", lazy.window.set_size_floating(),	start=lazy.window.get_size()),
    Click([mod],	"Button2", lazy.window.bring_to_front())
]

dgroups_key_binder	= None
dgroups_app_rules	= []  # type: List
main			= None
follow_mouse_focus	= True
bring_front_click	= False
cursor_warp		= False

##### FLOATING WINDOWS #####
floating_layout = layout.Floating(float_rules=[
    {'wmclass':	'confirm'},
    {'wmclass':	'dialog'},
    {'wmclass':	'download'},
    {'wmclass':	'error'},
    {'wmclass':	'file_progress'},
    {'wmclass':	'notification'},
    {'wmclass':	'splash'},
    {'wmclass':	'toolbar'},
    {'wmclass':	'confirmreset'},  # gitk
    {'wmclass':	'makebranch'},  # gitk
    {'wmclass':	'maketag'},  # gitk
    {'wname':	'branchdialog'},  # gitk
    {'wname':	'pinentry'},  # GPG key password entry
    {'wname':	'gsimplecal'},  # gsimplecal
    {'wmclass':	'ssh-askpass'},  # ssh-askpass
])

floating_layout			= layout.Floating()
auto_fullscreen			= True
focus_on_window_activation	= "smart"

##### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/startup.sh'])

#@hook.subscribe.startup
#def startup():
#    # bottom.show(False)
#    pass
#
#
#@hook.subscribe.startup_once
#def startup_once():
#    commands.reload_screen()
#
#
#@hook.subscribe.screen_change
#def restart_on_randr(qtile, ev):
#    commands.reload_screen()
#    qtile.cmd_restart()
#
#
#@hook.subscribe.client_new
#def floating_size_hints(window):
#    hints = window.window.get_wm_normal_hints()
#    if hints and 0 < hints['max_width'] < 1000:
#        window.floating = True

wmname = "Qtile"
