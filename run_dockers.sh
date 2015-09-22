#!/bin/bash
DOCKER0=172.17.42.1
KAFKA_BASE=../kafka_2.10-0.8.2.0
echo "starting kafka"
kafka=`docker run -d -p 2181:2181 -p 9092:9092 --name=kafka -e ADVERTISED_HOST=${DOCKER0} -e ADVERTISED_PORT=9092 spotify/kafka`
sleep 5
kafkaip=`docker inspect ${kafka}|grep -iw IPAddress|tr -d ' ",'|cut -d ':' -f2`
kafkabroker="${kafkaip}:9092"
kafkatopic="packetbeat"
zoostr="${kafkaip}:2181"
${KAFKA_BASE}/bin/kafka-topics.sh --zookeeper ${DOCKER0}:2181 --create --replication-factor 1 --partitions 1 --topic ${kafkatopic}
sleep 3
docker run -d --name=view -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -e PACKETBEAT_KAFKA_BROKERS=${kafkabroker} -e PACKETBEAT_KAFKA_TOPIC=${kafkatopic} -p 9180:9080 rshriram/pymicro
sleep 1
echo "started view service"
docker run -d --name=auth -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -e PACKETBEAT_KAFKA_BROKERS=${kafkabroker} -e PACKETBEAT_KAFKA_TOPIC=${kafkatopic} -p 9280:9080 rshriram/pymicro
sleep 1
echo "started auth service"
sleep 1

for serv in serviceA serviceB serviceC serviceD serviceA1 serviceA2 serviceA3 serviceB1 serviceB2 serviceB3 serviceC1 serviceC2 serviceC3 serviceD1 serviceD2 serviceD3 serviceDB1 serviceDB2 serviceDB3
do
    docker run -d --name=${serv} -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=${serv} -e PACKETBEAT_KAFKA_BROKERS=${kafkabroker} -e PACKETBEAT_KAFKA_TOPIC=${kafkatopic} rshriram/pymicro
    echo "started service ${serv}"
    sleep 1
done
