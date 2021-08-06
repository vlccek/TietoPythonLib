#!/bin/sh
apt-get install git -y
apt install python3-pip
apt-get -y install python3-pip
sudo apt-get -y install build-essential libssl-dev libffi-dev python3-dev cargo
yes | pip3 install setuptools
yes | pip3 install setuptools_rust
yes | pip3 install loguru 
yes | pip3 install -r requirements.txt

