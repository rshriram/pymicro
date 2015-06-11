#!/bin/bash
export ZOOKEEPER=localhost:2181
PORT=9996
for serv in view auth serviceA serviceB serviceC serviceD serviceA1 serviceA2 serviceA3 serviceB1 serviceB2 serviceB3 serviceC1 serviceC2 serviceC3 serviceD1 serviceD2 serviceD3 serviceDB1 serviceDB2 serviceDB3
do
    export SERVICE_NAME=${serv}
    PORT=$((${PORT}+1))
    nohup ./server.py ${PORT} >${serv}.out 2>&1 &
    sleep 1
    echo "started service ${serv}"
done
