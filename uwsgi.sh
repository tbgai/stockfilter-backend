#!/bin/bash
nohup uwsgi --socket 0.0.0.0:8090 --protocol=http --processes 4 --threads 10 --master --max-request 1000 -w run:app > stf_`date +%Y-%m-%d`.log 2>&1 &


