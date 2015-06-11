# pymicro
Microservice-based sample application written in Python

This is a very rudimentary microservice-based application written using python's bottle.py. It uses zookeeper for service discovery. The diagram below shows the high level structure of the application and its component microservices. If one or more services are not present, the subtree associated with it will not be called. Neither the server code (server.py) nor the service discovery code (discovery.py) is optimized. The service discovery code uses the python Kazoo client for zookeeper.

![alt tag](https://raw.github.com/rshriram/pymicro/master/application-topology.png)

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

For my own convenience, I packaged zookeeper in a docker container and run it like this:

`docker run -d rshriram/zookeeper`

**Testing**

`curl -o - http://127.0.0.1:9080/bottle/all/view`


