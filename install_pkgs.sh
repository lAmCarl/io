#!/bin/bash
echo Installing packages...

sudo apt-get -y update
sudo apt-get -y install python-pip python-dev build-essential libssl-dev libffi-dev libev-dev pound
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
sudo apt-get -y install redis-server
sudo service redis-server stop
sudo cp -rf pound.cfg /etc/pound/pound.cfg
sudo cp -rf pound /etc/default/pound
sudo cp -rf dump.rdb /var/lib/redis/dump.rdb
sudo chown redis:redis /var/lib/redis/dump.rdb
sudo chmod 660 /var/lib/redis/dump.rdb

echo Starting load balancer...
sudo /etc/init.d/pound start
echo Starting server...
sudo nohup redis-server &>redis.out &
sleep 5
echo Starting frontend...
sudo nohup python frontend.py &>frontend.out &
exit

echo Done
