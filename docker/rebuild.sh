#!/usr/bin/env bash

set -e

if [ "$DEB_PATH" == "" ]; then
    echo "env var DEB_PATH must contain a path to redpanda deb file"
    exit 1
fi

docker-compose down || true
docker-compose rm -f || true

cp $DEB_PATH .

if [ ! -f id_ed25519 ]; then
    ssh-keygen -t ed25519 -f id_ed25519 -N ""
fi

rm -rf ./docker/bind_mounts

mkdir -p ./docker/bind_mounts/redpanda1/mnt/vectorized/redpanda/data
mkdir -p ./docker/bind_mounts/redpanda2/mnt/vectorized/redpanda/data
mkdir -p ./docker/bind_mounts/redpanda3/mnt/vectorized/redpanda/data
mkdir -p ./docker/bind_mounts/redpanda1/mnt/vectorized/redpanda/coredump
mkdir -p ./docker/bind_mounts/redpanda2/mnt/vectorized/redpanda/coredump
mkdir -p ./docker/bind_mounts/redpanda3/mnt/vectorized/redpanda/coredump

mkdir -p ./docker/bind_mounts/control/mnt/vectorized/experiments

mkdir -p ./docker/bind_mounts/client1/mnt/vectorized/workloads/logs

chmod a+rw -R ./docker/bind_mounts

docker-compose build --build-arg REDPANDA_DEB=$(basename $DEB_PATH) --build-arg USER_ID=$(id -u $(whoami))