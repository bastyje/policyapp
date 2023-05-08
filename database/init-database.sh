#!/bin/sh

while true ; do
  sleep 5s
  docker exec policyapp_database /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P DatabasePassword123 -d master -Q "SELECT 1" && break
  echo 'not yet'
done

docker exec policyapp_database /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P DatabasePassword123 -d master -Q "CREATE DATABASE policyapp"
