# Waiting Room Concept -!

### 0. Why I thought this concept?
I was just curious how can I control web traffic before WAS being collapsed.
And I thought If I could keep clients in a queue and check a WAS can afford, I can send clients to a WAS at a proper time.

![WaitingSystem](https://user-images.githubusercontent.com/89409087/132750309-af716385-98d0-48c9-b2c7-ca2c5ab7d59a.png)

---
### 1. Build web server image
_simple_web_ is going to be an image name and _0.1_ is a tag.  
So, you can change this to whatever you want.
```bash
docker build -t simple_web:0.1 .
```
<img width="344" alt="image_built" src="https://user-images.githubusercontent.com/89409087/131225225-4bba6b70-fdd6-4a6c-b996-62851bf90ab5.png">

---
### 2. Create network
If two or more containers have to connect, they have to be bind by the same network.  
So, before running a web server, create a network.  
_simple_network_ is just a name. You can change this to whatever you want.
```bash
docker network create --driver=bridge simple_network
```
---
### 3. Run docker web image
```bash
docker run -it --name simple_web1 --net simple_network -v {your_source_code_path}/simple_web/simple_web1:/{path_of_where_you_want_in_webserver} simple_web:0.1
```
```bash
docker run -it --name simple_web2 --net simple_network -v {your_source_code_path}/simple_web/simple_web2:/{path_of_where_you_want_in_webserver} simple_web:0.1
```
---
### 4. Check web server container's IpAddress
Ip address needs for Haproxy configuration
```bash
docker inspect simple_web1
```
```bash
docker inspect simple_web2
```
<img width="146" alt="docker_inspect" src="https://user-images.githubusercontent.com/89409087/131225228-41148e91-de7b-4af1-becb-7950d53f2795.png">

---
### 5. Run web server
In the simple_web container, activate uvicorn
```bash
uvicorn main:app --reload --host {simple_web1 ip address} --port 8000
```
```bash
uvicorn main:app --reload --host {simple_web2 ip address} --port 8000
```
<img width="669" alt="uvicorn" src="https://user-images.githubusercontent.com/89409087/131225231-c6cdf4e8-7675-4110-962d-054d021e06b6.png">

---
### 6. Build haproxy image
_simple_haproxy_ is just a name and _0.1_ is a tag. You can change this to whatever you want.
```bash
docker build -t simple_haproxy:0.1 .
```

### 7. Test Haproxy configuration file
```bash
docker run -it --rm --name simple_haproxy_check {Haproxy image name}:{image tag} haproxy -c -f /etc/haproxy/haproxy.cfg
```
The result will be like this
```bash
Configuration file is valid
```

---
### 8. Run proxy image
This container also has to be in the same network. 
```bash
docker run -it --name {Haproxy image name} --net {network name} -p 80:80 -p 8404:8404 {Haproxy image name}:{the tag}
```

---
### 9. Start haproxy service
After checking haproxy config one more, start service.
```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
```
```bash
service haproxy start
```
https://user-images.githubusercontent.com/89409087/131225237-60b67c2d-b14f-46bd-b70f-7b865c6ce9ba.mov

---
### 10. Build Web server image for waiting
```bash
docker build -t simple_wait:0.1 .
```

### 11. Run Waiting Web server
```bash
docker run -it --name simple_wait --net simple_network -p 8080:8000 -p 15672:15672 -v {your_source_code_path}/simple_web/simple_wait:/simple_wait simple_wait:0.1
```

### 12. Run memcache & rqbbitMQ
After starting the MQ server, you can enter the MQ admin site. But you need an admin account.
```bash
service memcached start
service rabbitmq-server start
rabbitmq-plugins enable rabbitmq_management
```

### 13. Create mq users
Now you can enter the MQ admin site with the below accounts.
```bash
rabbitmqctl add_user admin 12345
rabbitmqctl set_user_tags admin administrator
rabbitmqctl add_user {your_user_account} {your_user_password}
rabbitmqctl set_user_tags {your_user_account} administrator
rabbitmqctl list_users
```

### 14. Create Queue
To connect with the queue, you need a host and exchange.
You also can use the root host "/".
```bash
rabbitmqctl add_vhost {www.exampleq.com}
rabbitmqctl list_vhosts
rabbitmqctl set_permissions -p {www.exampleq.com} {your_user_account} ".*" ".*" ".*"
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
rabbitmqctl set_permissions -p {www.exampleq.com} admin ".*" ".*" ".*"
rabbitmqctl list_permissions -p {www.exampleq.com}
```
```bash
rabbitmqadmin declare exchange --vhost={www.exampleq.com} name={your_exchanger} type=direct durable=true -u {admin} -p {password}
rabbitmqctl list_exchanges -p simple.customer.wait
```
```bash
rabbitmqadmin declare queue --vhost={www.exampleq.com} name={your_queue} durable=true -u {admin} -p {password}
```
```bash
rabbitmqadmin declare binding --vhost={www.exampleq.com} source={your_exchanger} destination={your_queue} routing_key={whatever_your_key} -u {admin} -p {password}
```

### 15. Run uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

![WaitingSystem](https://user-images.githubusercontent.com/89409087/132750489-8a7de89a-c9b2-4f6f-a937-46768dc4d842.png)

