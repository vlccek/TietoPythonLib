#!/bin/sh
apt-get install git -y
apt install python3-pip
sudo apt-get -y install build-essential libssl-dev libffi-dev python3-dev cargo
pip3 -y install setuptools
pip3 -y install -r requirements.txt

#etc.