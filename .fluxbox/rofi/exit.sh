#!/bin/bash

# small power menu using rofi, i3, systemd and pm-utils
# (last 3 dependencies are adjustable below)
# tostiheld, 2016

 Poweroff_command="systemctl poweroff"
 Reboot_command="systemctl reboot"
 Logout_command="bspc quit"
 Lock_command="i3lock"
 Cancel_command=""

# you can customise the rofi command all you want ...
rofi_command="rofi -theme themes/arc-red-dark.rasi -normal-window"

options=$' Poweroff\n Reboot\n Logout\n Lock\n Cancel'

# ... because the essential options (-dmenu and -p) are added here
eval \$"$(echo "$options" | $rofi_command -dmenu -p "")_command"

