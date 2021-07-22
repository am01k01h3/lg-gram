#!/bin/bash

# small power menu using rofi, i3, systemd and pm-utils
# (last 3 dependencies are adjustable below)
# tostiheld, 2016

# Poweroff_command="systemctl poweroff"
# Reboot_command="systemctl reboot"
# Logout_command="bspc quit"
# Lock_command="i3lock"
# Cancel_command=""

args=$0

# you can customise the rofi command all you want ...
rofi_command="rofi -theme ~/.config/qtile/rofi/themes/notify.rasi -normal-window"
#rofi_command="rofi -theme ~/.config/qtile/rofi/themes/arc-red-dark.rasi -normal-window"
#rofi_command="rofi -normal-window"

menu_items=$' Shutdown\n Restart\n Logout\n Lock\n Cancel'

# ... because the essential options (-dmenu and -p) are added here
#eval \$"$(echo "$options" | $rofi_command -dmenu -p "")_command"

echo "$args"
user_selected_option=$( echo "$menu_items" | $rofi_command -dmenu -p "" )

echo "$user_selected_option"

case "$user_selected_option" in
	" Poweroff_command")	poweroff;;
	" Reboot_command")		systemctl restart;;
	" Logout_command")		qtile-cmd -o cmd -f shutdown ;;
	" Lock_command")		systemctl suspend;;
	" Cancel_command")		;;
esac

