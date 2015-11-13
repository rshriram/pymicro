# pymicro
Microservice-based sample application written in Python

This is a very rudimentary microservice-based application written using python's bottle.py. It uses zookeeper for service discovery. The diagram below shows the high level structure of the application and its component microservices. If one or more services are not present, the subtree associated with it will not be called. Neither the server code (server.py) nor the service discovery code (discovery.py) is optimized. The service discovery code uses the python Kazoo client for zookeeper.

![alt tag](https://raw.github.com/rshriram/pymicro/master/application-topology.png)

There is a docker image associated with this service, hosted on the docker hub. This repository holds the source files related to this application.

In addition, each docker image is packaged with packetbeat agent (1.0.0-rc1, golang 1.5.1), to emit summaries of HTTP traffic. Packetbeat's output is written to the console. You should be able to get the outputs using `docker logs` command. Alternatively, if you launch this container in the IBM Bluemix Container Cloud, you should be able to see the docker log output in the [logmet service](https://logmet.ng.bluemix.net).

Without Docker
--------------

Install zookeeper and change the ZOOKEEPER variable in the script below, before executing it. The script launches all processes in the localhost.

`./run_processes.sh`

With Docker
-----------

**Building from source**

`docker build -t rshriram/pymicro .` 

**Deploying the setup**

The run_dockers.sh script is a good starting point to setup the entire environment. The script starts the microservices by specifying their service names and zookeeper location.
The names of services can be found in service_dict in the server.py file

`docker run -d --name=view -e ZOOKEEPER=172.16.0.1:2181 -e SERVICE_NAME=view -p 9997:9080 rshriram/pymicro`

Only the view and auth services need their ports 9080 to be publicly exposed.

**Testing**

`curl -o - http://127.0.0.1:9080/bottle/all/view`
