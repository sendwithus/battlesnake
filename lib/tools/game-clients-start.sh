:<<__

Run this from the root of the project

__

if [ "$1" == start ]; then

  for line in `cat lib/tools/teams/port_team001.txt`; do
    PORT=`echo $line |awk -F',' '{print $1}'` ;
    ID=`echo $line | awk -F',' '{print $2}'`;
    echo PORT: $PORT ID: $ID;
    (PORT=$PORT ID=$ID python lib/tools/app/main.py)&
  done

elif [ "$1" == stop ]; then

  kill `ps -eaf | grep lib/tools/app/main.py | grep -v grep | tr -s ' ' ' ' | cut -f3 -d' '`

else

  cat <<HELP
Usage: $0 [ start | stop ]
HELP

fi
