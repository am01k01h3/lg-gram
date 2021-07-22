#!/bin/sh

STATUS=$( acpi )

notify-send -t 3000 "$STATUS"
