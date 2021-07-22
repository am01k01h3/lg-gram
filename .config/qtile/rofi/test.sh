

ls ~/.config/qtile/rofi/themes/* | while read theme
do
	#./rofi-notify.sh --theme $theme -e $( brightnessctl -m | awk 'BEGIN{FS=","}{print $2 ":" $4}' )
	echo $theme
	rofi -show combi -theme $theme 
done

