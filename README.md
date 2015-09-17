# pymicro
Microservice-based sample application written in Python

This is a very rudimentary microservice-based application written using python's bottle.py. It uses zookeeper for service discovery. The diagram below shows the high level structure of the application and its component microservices. If one or more services are not present, the subtree associated with it will not be called. Neither the server code (server.py) nor the service discovery code (discovery.py) is optimized. The service discovery code uses the python Kazoo client for zookeeper.

![alt tag](https://raw.github.com/rshriram/pymicro/master/application-topology.png)

There is a docker image associated with this service, hosted on the docker hub. This repository holds the source files related to this application.

In addition, each docker image is packaged with packetbeat agent, to emit summaries of HTTP traffic. Packetbeat's output is sent to a kafka container (spotify/kafka), that should be launched before the rest of the containers.

Without Docker
--------------

Install zookeeper and change the ZOOKEEPER variable in the script below, before executing it. The script launches all processes in the localhost.

`./run_processes.sh`

With Docker
-----------

**Building from source**

`docker build -t rshriram/pymicro .` 

**Deploying the setup**

The run_dockers.sh script is a good starting point to setup the entire environment. It starts spotify/kafka docker container (which also has zookeeper). It then creates a topic called "packetbeat" in Kafka, using the kafka command line tools. Tweak the script according to your environment. In my case, kafka cli tools were installed in kafka_2.10-0.8.2.0 folder. Make sure to change ADVERTISED_HOST to the IP of the docker0 interface on your host. And when launching the spotify/kafka container, don't forget to specify the ADVERTISED_HOST and ADVERTISED_PORT parameters. Here is how I started the kafka container:

`docker run -d -p 2181:2181 -p 9092:9092 --name=kafka -e ADVERTISED_HOST=<DOCKER0_IP> -e ADVERTISED_PORT=9092 spotify/kafka`

Once the kafka container has been started, the script starts the remaining microservices by specifying their service names, zookeeper location (which is ADVERTISED_HOST : 2181), PACKETBEAT_KAFKA_BROKERS (which is ADVERTISED_HOST : ADVERTISED_PORT) and PACKETBEAT_KAFKA_TOPIC.
The names of services can be found in service_dict in the server.py file

`docker run -d --name=view -e ZOOKEEPER=172.16.0.1:2181 -e SERVICE_NAME=view -e PACKETBEAT_KAFKA_BROKERS=172.16.0.1:9092 -e PACKETBEAT_KAFKA_TOPIC=packetbeat -p 9997:9080 rshriram/pymicro`

Only the view and auth services need their ports 9080 to be publicly exposed.

**Testing**

`curl -o - http://127.0.0.1:9180/bottle/all/view`
`curl -o - http://127.0.0.1:9280/bottle/all/auth`

