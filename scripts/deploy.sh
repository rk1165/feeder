#!/usr/bin/env bash

doctl compute droplet create \
--region sfo2 \
--image ubuntu-23-10-x64 \
--size s-1vcpu-1gb \
--ssh-keys 40809935 \
--enable-monitoring \
--user-data-file start.sh \
feeder