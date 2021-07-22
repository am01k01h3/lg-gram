ps -ef | grep qtile | grep -v ssh | grep -v grep

#ps -ef | grep qtile | grep -v ssh | grep -v grep | awk '{print $2}' | xargs kill -9 && echo "killed"
PID=""

PID=$( ps -ef | grep qtile | grep -v ssh | grep -v grep | awk '{print $2}' )
[[ "$PID" -eq "" ]] || kill -9 $PID && echo "killed"

ps -ef | grep qtile | grep -v ssh | grep -v grep
