#!/usr/bin/env bash

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt-get install -y mysql-server mysql-client
sudo mysql -p12345 < schema.sql
sudo apt-get install -y python-pip python-dev libmysqlclient-dev
sudo pip install flask sqlalchemy MySQL-python requests
python test/test.py