#!/bin/bash

# Run bot
cd /mfbot/
./MFBot_Konsole_x86_64 >> botLog.txt &

# Run web panel
cd /mfbot/Web/
source venv/bin/activate
python MainProgram.py -a http://127.0.0.1:6969/ --remoteU="admin" --remoteP="admin" --webU="admin" --webP="admin" --debug=0 >> webLog.txt &

# Keep container alive
while true; do sleep 1000; done