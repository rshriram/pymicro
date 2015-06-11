# pymicro
Microservice-based sample application written in Python

This is a very rudimentary microservice image based on python's bottle.py, using zookeeper for service discovery.
There is a docker image associated with this service, hosted on the docker hub. This repository holds the source files related to this application.

Without Docker
--------------

Install zookeeper and change the ZOOKEEPER variable in the script below, before executing it. The script launches all processes in the localhost.

`./run_processes.sh`

With Docker
-----------

**Building from source**

`docker build -t rshriram/pymicro .` 

**Deploying the setup**

Start the microservices specifying zookeeper location and the service name. The names of services can be found in service_dict in the server.py file
 
`docker run -d -e SERVICE_NAME=serviceA -e ZOOKEEPER=host:2181 rshriram/pymicro`

**Testing**

`curl -o - http://127.0.0.1:9080/bottle/all/view`

You should receive a collated response from master, that contains responses from services A, B and C and their sub-services

