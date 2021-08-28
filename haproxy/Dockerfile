FROM ubuntu:18.04
EXPOSE 80
EXPOSE 8404

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install haproxy -y

COPY haproxy.cfg /etc/haproxy/haproxy.cfg

RUN mkdir /var/run/haproxy/ && chown haproxy:haproxy /var/run/haproxy/