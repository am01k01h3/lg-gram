#!/bin/bash

exit_if_failed() {
  STATUS=$1
  echo "Something went wrong"
  if [ $STATUS -ne 0 ]; then
    echo $STATUS
	exit
  fi
}

#which pip3 && alias pip='pip3'
#exit_if_failed $?

pip3 install xcffib
exit_if_failed $?

pip3 install --no-cache-dir cairocffi
exit_if_failed $?

OS_TYPE=$( awk -F'=' '/^ID_LIKE/ {print $2}' /etc/*rel* )
exit_if_failed $?

case $OS_TYPE in
  "debian")
    PACKAGE_MANAGER_CMD="apt install "
  ;;
  "arch")
    PACKAGE_MANAGER_CMD="pacman -Ss "
  ;;
  *)
    echo "Error: unable to determine Package Manager"
    echo "Not sure how to handle $OS_TYPE"
  ;;
esac

echo "Package manager: $PACKAGE_MANAGER_CMD"
sudo $PACKAGE_MANAGER_CMD libpangocairo-1.0-0
exit_if_failed $?

cd ~/Downloads
git clone git://github.com/qtile/qtile.git
exit_if_failed $?

cd qtile
pip3 install .
exit_if_failed $?

pip3 install qtile
exit_if_failed $?

pip3 install psutil
exit_if_failed $?


