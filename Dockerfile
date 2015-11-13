FROM ubuntu:14.04
MAINTAINER Shriram Rajagopalan <rshriram@gmail.com>
RUN apt-get update
RUN apt-get install python-pip python-dev -y
RUN pip install bottle json2html simplejson
RUN apt-get install -y python-kazoo supervisor
RUN mkdir -p /var/log/supervisor
ADD packetbeat_1.0.0~rc1_amd64.deb /tmp/
RUN dpkg -i /tmp/packetbeat_1.0.0~rc1_amd64.deb; apt-get -y install -f
RUN rm /tmp/*.deb
ADD packetbeat.yml /etc/packetbeat/packetbeat.yml
ADD packetbeat-supervisor.conf /etc/supervisor/conf.d/packetbeat.conf

RUN mkdir -p /opt/microservices
ADD server.py /opt/microservices/server.py
ADD discovery.py /opt/microservices/discovery.py
EXPOSE 9080
ADD pymicro-supervisor.conf /etc/supervisor/conf.d/pymicro.conf

CMD ["/usr/bin/supervisord", "-n"]
