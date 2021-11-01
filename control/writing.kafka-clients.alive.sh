#!/bin/bash

set -e

if [ ! -f /mnt/vectorized/workloads/logs/kafka-clients.pid ]; then
    echo "NO"
    exit 0
fi

pid=$(cat /mnt/vectorized/workloads/logs/kafka-clients.pid)

if [ $pid == "" ]; then
    echo "NO"
    exit 0
fi

if process=$(ps -p $pid -o comm=); then
    if [ $process == "java" ]; then
        echo "YES"
        exit 0
    fi
fi

echo "NO"
exit 0