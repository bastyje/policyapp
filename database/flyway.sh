#!/bin/bash

rel_path="/flyway.sh"
file=$0
abs_path="$(pwd)${file:1}"
db_dir="${abs_path::$((-"${#rel_path}"))}"
docker run --rm --add-host="localhost:192.168.0.108" -it -v="$(echo $db_dir)":/database flyway/flyway:latest -configFiles="/database/flyway/conf/flyway.properties" -user=sa -password=DatabasePassword123 repair migrate