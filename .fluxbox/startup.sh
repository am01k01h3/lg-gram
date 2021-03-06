#!/bin/sh


# Load SSH Keys
grep -l "BEGIN RSA PRIVATE KEY" ~/.ssh/* | while read file
do
  ssh-add "$file" &
done

# Load bitmap fonts
xset fp+ ~/.fonts/misc &

## Who don't love an eye candy shadow?? Launch compton
#compton -b --config ~/.config/compton.conf &


## Load settings
[ -f ~/.Xmodmap ] && xmodmap ~/.Xmodmap &
[ -f ~/.Xresources ] && xrdb ~/.Xresources

# Xdefaults is now deprecated in X11, and only .Xresources should be used
#[ -f ~/.Xdefaults ] && xrdb ~/.Xdefaults

# Turn off trackpad while typing 
syndaemon -d -i 0.5 &

## Generate Menus on startup
[ -f ~/.fluxbox/bin/generate_fluxbox_menu ] && ~/.fluxbox/bin/generate_fluxbox_menu &

## Restore Wallpaper
nitrogen --restore &

pulseaudio --start &

start-pulseaudio-x11 &

dbus-launch --exit-with-session &

[ -f /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 ] && /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

## System Tray Apps
nice conky -c /home/amol/.fluxbox/conky/bar.conkyrc &
#conky -c /home/amol/.fluxbox/conky/conky_maia &

nm-applet &
#xfce4-power-manager &
#pamac-tray &
#ff-theme-util &
#fix_xcursor &
#/usr/bin/python3 /usr/bin/blueman-applet >/dev/null &

#Battery Icon
~/.fluxbox/bin/batteryIcon.pl &

# Sound Icon in Systemtray
#volumeicon &
pasystray &

# Clipboard Systemtray
#qlipper &
clipit &

# Screen locking
xautolock -time 10 -locker blurlock &

## User Apps
#~/.fluxbox/bin/terminal &

# Start Terminal
#urxvt &
#sleep 1 && st -e bash -l &
#sleep 1 && st -T tty-clock -n tty-clock -g 36x10 -e tty-clock -B -C 8 -t &

#sleep 1 && alacritty -e bash -l &
#sleep 1 && alacritty -T tty-clock -n tty-clock -g 36x10 -e tty-clock -B -C 8 -t &

# Start Syncthing
nice syncthing -no-browser &

## Additional Eye Candy
#xcompmgr -c -C -t-5 -l-5 -r4.2 -o.55 &

#wmcalclock &
#wmfire &
#wmmoonclock &
#wmcpuload &
#wmmemload &

