# Build a simple web server with Haproxy!

---
###1. Build web server image
_simple_web_ is going to be an image name and _0.1_ is a tag.  
So, you can change this to whatever you want.
```bash
docker build -t simple_web:0.1 .
```
![alt text](/Users/heegyoung/Desktop/image_built.png?raw=true)

---
###2. Create network
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
![alt text](/Users/heegyoung/Desktop/docker_inspect.png?raw=true)

---
### 5. Run web server
In the simple_web container, activate fast API env and uvicorn
```bash
source venv/bin/activate
```
```bash
uvicorn main:app --reload --host {simple_web1 ip address} --port 8000
```
```bash
uvicorn main:app --reload --host {simple_web2 ip address} --port 8000
```
![alt text](/Users/heegyoung/Desktop/uvicorn.png?raw=true)

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
docker run -it --name {Haproxy image name} --net {network name} -p 80:80 {Haproxy image name}:{the tag}
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