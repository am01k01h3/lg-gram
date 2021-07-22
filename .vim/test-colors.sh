
prompt_and_delete() {
  file=$1

  input=
  #echo "Delete $line? y/n"
  read -p "	Delete $file (y/n)? " input
  case $input in
    [yY])
      rm $file && echo "	deleted."
      ;;
    [nN])
      echo "	Skipping ..."
      ;;
    [q])
	  exit
      ;;
  esac
}

cd ~/.vim/colors
#for file in $(ls *candy*.vim *tango*.vim *gruvbox*.vim *monokai*.vim *monokai*.vim *onedark*.vim )
for file in $(ls *.vim)
do
  name=$( basename $file .vim )
  echo "colorscheme $name"
  #echo "	alacritty -e vim -c 'colorscheme '"$name"' ' ~/.vimrc ~/.config/qtile/config.py"
  alacritty -e vim -c 'colorscheme '"$name"' ' ~/.vimrc ~/.fluxbox/startup ~/.config/qtile/config.py
  #sakura -e vim -c 'colorscheme '"$name"' ' ~/.vimrc ~/.fluxbox/startup ~/.config/qtile/config.py
  prompt_and_delete $file
done

