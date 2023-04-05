#!/bin/sh

./init-mssql.sh &

docker run \
  --rm \
  -p 1400:1433 \
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=DatabasePassword123" \
  -p 1433:1433 \
  --name policyapp_database \
 mcr.microsoft.com/mssql/server:2022-latest
