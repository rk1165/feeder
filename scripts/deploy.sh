#!/usr/bin/env bash

doctl compute droplet create \
--region sfo2 \
--image ubuntu-23-10-x64 \
--size s-1vcpu-1gb \
--ssh-keys "$YOUR_SSH_KEY_ID" \
--enable-monitoring \
--user-data-file start.sh \
feeder