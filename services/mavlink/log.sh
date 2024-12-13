#!/usr/bin/env bash

LOGFILE="/data/mavlink-$(date +%Y-%m-%d.%H-%M-%S.%Z).log"

echo "logging to $LOGFILE..."
nc 172.17.0.1 5790 > "$LOGFILE"
