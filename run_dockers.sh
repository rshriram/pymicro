#!/bin/bash
echo "starting kafka"
kafka=`docker run -d -p 2181:2181 -p 9092:9092 --name=kafka -e ADVERTISED_HOST=172.17.42.1 -e ADVERTISED_PORT=9092 spotify/kafka`
sleep 1
kafkaip=`docker inspect ${kafka}|grep -i IPAddress|tr -d ' ",'|cut -d ':' -f2`
kafkabroker="${kafkaip}:9092"
kafkatopic="packetbeat"
zoostr="${kafkaip}:2181"
pushd ../kafka_2.10-0.8.2.0/
bin/kafka-topics.sh --zookeeper ${kafkaip}:2181 --create --replication-factor 1 --partition 1 --topic ${kafkatopic}
popd

docker run -d --name=view -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=view -e PACKETBEAT_KAFKA_BROKERS=${kafkabroker} -e PACKETBEAT_KAFKA_TOPIC=${kafkatopic} -p 9997:9080 rshriram/pymicro
sleep 1
echo "started view service"
sleep 1
for serv in auth serviceA serviceB serviceC serviceD serviceA1 serviceA2 serviceA3 serviceB1 serviceB2 serviceB3 serviceC1 serviceC2 serviceC3 serviceD1 serviceD2 serviceD3 serviceDB1 serviceDB2 serviceDB3
do
    docker run -d --name=${serv} -e ZOOKEEPER=${zoostr} -e SERVICE_NAME=${serv} -e PACKETBEAT_KAFKA_BROKERS=${kafkabroker} -e PACKETBEAT_KAFKA_TOPIC=${kafkatopic} rshriram/pymicro
    echo "started service ${serv}"
    sleep 1
done
