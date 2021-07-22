#!/bin/sh

STATUS=$( head -3 /proc/meminfo | awk '{print $1 , "\t" , $2/1024/1024 , " Gb "}' )

notify-send "$STATUS"
