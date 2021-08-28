FROM ubuntu:18.04
EXPOSE 8000

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install curl -y
RUN apt-get install python3.8 -y
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN apt-get install python3-pip -y
RUN apt-get remove python3-pip -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install fastapi uvicorn