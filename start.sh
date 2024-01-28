#!/usr/bin/env bash

source .venv/bin/activate

sleep 1

gunicorn --bind 0.0.0.0:8000 -w 1 'app:app' \
--access-logfile '/var/log/access.log' \
--error-logfile '/var/log/error.log' \
--daemon