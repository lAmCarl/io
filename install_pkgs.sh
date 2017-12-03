#!/bin/bash
echo Installing packages...

sudo apt-get -y update
sudo apt-get -y install python-pip python-dev build-essential libssl-dev libffi-dev
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
sudo apt-get -y install redis-server

echo Starting server...
sudo nohup redis-server &>/dev/null &
echo Starting frontend...
sudo nohup python frontend.py &>/dev/null &
exit

echo Done