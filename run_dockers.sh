#!/bin/bash
echo "starting zookeeper"
zookeeper=`docker run -d --name=zookeeper rshriram/zookeeper:3.4.6`
sleep 5
zooip=`docker inspect ${zookeeper}|grep -iw IPAddress|tr -d ' ",'|cut -d ':' -f2`
zoostr="${zooip}:2181"

docker run -d --name=view -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -p 9180:9080 rshriram/pymicro
sleep 1
echo "started view service"
docker run -d --name=auth -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -p 9280:9080 rshriram/pymicro
sleep 1
echo "started auth service"
sleep 1

for serv in serviceA serviceB serviceC serviceD serviceA1 serviceA2 serviceA3 serviceB1 serviceB2 serviceB3 serviceC1 serviceC2 serviceC3 serviceD1 serviceD2 serviceD3 serviceDB1 serviceDB2 serviceDB3
do
    docker run -d --name=${serv} -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=${serv} rshriram/pymicro
    echo "started service ${serv}"
    sleep 1
done
