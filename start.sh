#!/usr/bin/env bash

apt-get update
apt-get install -y git
apt-get install -y python3.11-venv
apt-get install -y python3-pip

git clone https://github.com/rk1165/feeder
cd feeder || exit

python3 -m venv .venv
source .venv/bin/activate
sleep 1
python3 -m pip install -r requirements.txt --break-system-packages
sleep 1

gunicorn --bind 0.0.0.0:8000 -w 1 'app:app' \
--access-logfile '/var/log/access.log' \
--error-logfile '/var/log/error.log' \
--daemon

echo "Successfully started feeder"