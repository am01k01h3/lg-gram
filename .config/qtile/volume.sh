#!/bin/sh

#notify-send $( pactl list sinks | grep "^[[:space:]]Mute" )
	#notify-send $( pactl list sinks | grep "^[[:space:]]Volume" | awk '{print "Volume: " $5}' )
	#notify-send $( pactl list sinks | grep "^[[:space:]]Volume" | awk '{print "Volume: " $5}' )
	#notify-send "$( pactl list sinks | grep "^[[:space:]]Volume" ) "

STATUS=""

case $1 in
  "mute"|"0")
    pactl set-sink-mute @DEFAULT_SINK@ toggle
	STATUS="$( pactl list sinks | grep "^[[:space:]]Mute" | awk '{print "🔊" , $1 , $2}' )"
  ;;
  "up"|"+")
    pactl set-sink-mute @DEFAULT_SINK@ false ; pactl set-sink-volume @DEFAULT_SINK@  +5%
	STATUS="$( pactl list sinks | grep "^[[:space:]]Volume" | awk '{print "🔊 Volume: " $5}' )"
  ;;
  "down"|"-")
    pactl set-sink-mute @DEFAULT_SINK@ false ; pactl set-sink-volume @DEFAULT_SINK@ -5%
	STATUS="$( pactl list sinks | grep "^[[:space:]]Volume" | awk '{print "🔊 Volume: " $5}' )"
  ;;
  *)
	STATUS="$( pactl list sinks | grep "^[[:space:]]Volume" | awk '{print "🔊 Volume: " $5}' )"
  ;;
esac

notify-send -t 1000 "$STATUS"

