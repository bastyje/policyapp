#!/bin/bash

interface_name="wlp0s20f3"
ip_addr=$(ip -br a | grep $interface_name | awk '{ print $3 }' | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
abs_path="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
docker run --rm --add-host="localhost:$ip_addr" -it -v="$(echo $abs_path)":/database flyway/flyway:latest -configFiles="/database/flyway/conf/flyway.properties" -user=sa -password=DatabasePassword123 repair migrate