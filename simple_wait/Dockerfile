FROM ubuntu:18.04
EXPOSE 8000
EXPOSE 15672
EXPOSE 11211

RUN apt-get update && apt-get upgrade
RUN apt-get install vim -y
RUN apt-get install curl -y
RUN apt-get install rabbitmq-server -y
RUN apt-get install python3.8 -y
RUN apt-get install memcached -y

RUN apt-get install python3-pip -y
RUN apt-get remove python3-pip -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
RUN pip3.8 install fastapi uvicorn jinja2 aiofiles pika python-memcached requests