#!/usr/bin/env bash

apt-get update
apt-get install git

git clone https://github.com/rk1165/feeder/tree/main.git

cd feeder || exit
python3 -m venv venv
source .venv/bin/activate
python3 pip install -r requirements.txt --break-system-packages

sleep 1

gunicorn --bind 0.0.0.0:8000 -w 1 'app:app' \
--access-logfile '/var/log/access.log' \
--error-logfile '/var/log/error.log' \
--daemon