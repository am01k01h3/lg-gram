#!/bin/bash


## run (only once) processes which spawn with the same name
function run {
   if (command -v $1 && ! pgrep $1); then
     $@&
   fi
}

## run (only once) processes which spawn with different name
if (command -v gnome-keyring-daemon && ! pgrep gnome-keyring-d); then
    gnome-keyring-daemon --daemonize --login &
fi
if (command -v start-pulseaudio-x11 && ! pgrep pulseaudio); then
    start-pulseaudio-x11 &
fi
if (command -v /usr/lib/mate-polkit/polkit-mate-authentication-agent-1 && ! pgrep polkit-mate-aut) ; then
    /usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
fi
if (command -v  xfce4-power-manager && ! pgrep xfce4-power-man) ; then
    xfce4-power-manager &
fi

run xfsettingsd
run nm-applet
run light-locker
run xcape -e 'Super_L=Super_L|Control_L|Escape'
run thunar --daemon
run pa-applet
run pamac-tray

## The following are not included in minimal edition by default
## but autorun.sh will pick them up if you install them

if (command -v system-config-printer-applet && ! pgrep applet.py ); then
  system-config-printer-applet &
fi


## Who don't love an eye candy shadow??
run picom
run compton -b --config ~/.config/compton.conf
# run compton --shadow-exclude '!focused'
#run compton -b --config ~/.config/compton.conf
#xcompmgr -c -C -t-5 -l-5 -r4.2 -o.55 &


run blueman-applet
run msm_notifier

# Load SSH Keys
grep -l "BEGIN RSA PRIVATE KEY" ~/.ssh/* | while read file
do
  ssh-add "$file"
done &

# Load bitmap fonts
xset fp+ ~/.fonts/misc &

## Load settings
[ -f ~/.Xmodmap ] && xmodmap ~/.Xmodmap &
[ -f ~/.Xresources ] && xrdb ~/.Xresources &

# Turn off trackpad while typing
syndaemon -d -i 0.5 &

# Xdefaults is now deprecated in X11, and only .Xresources should be used
#[ -f ~/.Xdefaults ] && xrdb ~/.Xdefaults

## Generate Menus on startup
#[ -f ~/.fluxbox/bin/generate_fluxbox_menu ] && ~/.fluxbox/bin/generate_fluxbox_menu &

## Restore Wallpaper
run nitrogen --restore &

run dbus-launch --exit-with-session

# Sound Icon in Systemtray
run pasystray

run pulseaudio --start

# Start dunst Notification Daemon
dunst -conf ~/.config/qtile/dunstrc  &

#[ -f /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 ] && /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

## System Tray Apps
#conky -c /home/amol/.fluxbox/conky/bar.conkyrc &
#conky -c /home/amol/.fluxbox/conky/conky_maia &

#nm-applet &
#xfce4-power-manager &
#pamac-tray &
#ff-theme-util &
#fix_xcursor &
#/usr/bin/python3 /usr/bin/blueman-applet >/dev/null &

# Sound Icon in Systemtray
#volumeicon &

# Clipboard Systemtray
#qlipper &
#clipit &

# Screen locking
#xautolock -time 10 -locker blurlock &

## User Apps
#~/.fluxbox/bin/terminal &

# Start Terminal
#urxvt &
#sleep 1 && st -e bash -l &
sleep 1 && alacritty -e bash -l &
#sleep 1 && st -T tty-clock -n tty-clock -g 36x10 -e tty-clock -B -C 8 -t &

# Start Syncthing
syncthing -no-browser &

###############################################################################

