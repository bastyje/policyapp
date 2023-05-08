#!/bin/sh

./init-database.sh &

path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/docker/docker-compose.yml"

docker compose -f $path up

#docker run \
#  --rm \
#  -p 1400:1433 \
#  -e "ACCEPT_EULA=Y" \
#  -e "MSSQL_SA_PASSWORD=DatabasePassword123" \
#  -p 1433:1433 \
#  --name policyapp_database \
# mcr.microsoft.com/mssql/server:2022-latest
