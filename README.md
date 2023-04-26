# MFBotDocker

Docker ready installation for MFBot and Web interface.

# Instructions.

Prepare Acc.ini file on MFBot's Windows version. Go to the Settings > Network > Remote Access. Enable remote access - set IP to 127.0.0.1 and choose suitable port number, in my case it's 6969.

1. Clone repo

> git clone https://github.com/mangunowsky/MFBotDocker.git

2. Paste Acc.ini file into main repo folder

3. Build Docker image

> docker build -t mfbot -f Dockerfile .

4. Run Docker container

> docker run -dit mfbot

5. Get containers IP address

> docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \<container ID\>

6. Open web interface in you browser. User and password is "admin" by default.

> http://\<container IP\>:8050

7. Happy boting!

# Changing web interface listening port.

To change port on which web interface is listeing you need to edit globalVariables.py file located in Web/Functions/

> ADRESS = 'http://127.0.0.1:6969/' - change port to one set in Remote Access settings

> serverPort = 8050 - Web interface will be available at this port
