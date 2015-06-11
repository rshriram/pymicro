FROM ubuntu:14.04
MAINTAINER Shriram Rajagopalan <rshriram@gmail.com>
RUN apt-get update
RUN apt-get install python-pip python-dev -y
RUN pip install bottle json2html simplejson
RUN apt-get install -y python-kazoo
RUN mkdir -p /opt/microservices
ADD server.py /opt/microservices/server.py
ADD discovery.py /opt/microservices/discovery.py
EXPOSE 9080
ENTRYPOINT ["/usr/bin/python", "/opt/microservices/server.py", "9080"]
