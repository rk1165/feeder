#!/usr/bin/env bash

gunicorn -w 1 'app:app' --access-logfile '/var/log/access.log' --error-logfile '/var/log/error.log'