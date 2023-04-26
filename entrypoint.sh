#!/bin/bash

# Run bot
while true; do
    if ! ps -C MFBot_Konsole_x > /dev/null; then
        cd /mfbot/ || exit
        ./MFBot_Konsole_x86_64 >> botLog.txt &
    fi

    if ! ps -C python > /dev/null; then
        cd /mfbot/Web/ || exit
        source venv/bin/activate
        python MainProgram.py -a http://127.0.0.1:6969/ --remoteU="admin" --remoteP="admin" --webU="admin" --webP="admin" --debug=0 >> webLog.txt &
    fi

    sleep 10
done
