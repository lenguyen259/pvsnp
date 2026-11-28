#!/bin/bash
# wait for pid $1 then collect job $2
while [ -d /proc/$1 ]; do sleep 10; done; ./collect.sh $2
