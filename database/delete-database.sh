#!/bin/sh

path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/docker/docker-compose.yml"

docker compose -f $path down -v