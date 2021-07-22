#!/bin/sh

case $1 in
  "up"|"+")
    sudo brightnessctl s +5%
  ;;
  "down"|"-")
    sudo brightnessctl s 5%-
  ;;
  *)
    brightnessctl -m | awk 'BEGIN{FS=","}{print "Brightness " , $4}'
  ;;
esac


notify-send -t 1000 $( brightnessctl -m | awk 'BEGIN{FS=","}{print "Brightness " , $4}' )

