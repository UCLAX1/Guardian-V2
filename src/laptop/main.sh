#!/bin/bash

BINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

startBackend() {
    cd $BINDIR/backend/
    python3 server.py 1>$BINDIR/logs/pyStdout 2>$BINDIR/logs/pyStderr
}

startFrontend() {
    cd $BINDIR/frontend/
    sleep 5
    nohup npm start 1>$BINDIR/logs/jsStdout 2>$BINDIR/logs/jsStderr
}

stopAll() {
    pkill -9 -f server.py 1>/dev/null 2>/dev/null
    pkill -9 -f react-scripts 1>/dev/null 2>/dev/null
}

case "$1" in
    start)
      startBackend & startFrontend &
      ;;
    stop)
      stopAll
      ;;
    *)
      echo "usage: $0 start|stop" >&2
      exit 1
      ;;
esac
