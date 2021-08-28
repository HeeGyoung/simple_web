# Build a simple web server with Haproxy!

---
###1. Build web server image
_simple_web_ is going to be an image name and _0.1_ is a tag.  
So, you can change this to whatever you want.
```bash
docker build -t simple_web:0.1 .
```
<img width="344" alt="image_built" src="https://user-images.githubusercontent.com/89409087/131225225-4bba6b70-fdd6-4a6c-b996-62851bf90ab5.png">

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
<img width="146" alt="docker_inspect" src="https://user-images.githubusercontent.com/89409087/131225228-41148e91-de7b-4af1-becb-7950d53f2795.png">

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
https://user-images.githubusercontent.com/89409087/131225237-60b67c2d-b14f-46bd-b70f-7b865c6ce9ba.mov

