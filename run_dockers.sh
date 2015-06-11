#!/bin/bash

echo "starting zookeeper.."
zoo=`docker run -d --name=zookeeper rshriram/zookeeper:3.4.6`
sleep 1

zooip=`docker inspect ${zoo}|grep -i IPAddress|tr -d ' ",'|cut -d ':' -f2`
zoostr="${zooip}:2181"
echo "Zookeeper ip is ${zoostr}"
docker run -d --name=view -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -p 9997:9080 rshriram/pymicro
sleep 1
echo "started view service"
sleep 1
for serv in auth serviceA serviceB serviceC serviceD serviceA1 serviceA2 serviceA3 serviceB1 serviceB2 serviceB3 serviceC1 serviceC2 serviceC3 serviceD1 serviceD2 serviceD3 serviceDB1 serviceDB2 serviceDB3
do
    docker run -d --name=${serv} -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=${serv} rshriram/pymicro
    echo "started service ${serv}"
    sleep 1
done
