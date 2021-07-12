---
title : Docker와 Python Flask 를 이용한 카카오톡 플러스친구 개발 과 배포 -2-
tags:
- 챗봇
- Python
- Flask
- Docker
- 카카오톡 플러스친구
categories:
- DevOps
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

> 이전에 Goorm을 사용했는데 Docker를 보안상의 이유로 사용을 제한해 놨습니다. 그래서 부득이하게 Docker로 배포하는 부분만 AWS에서 작업하겠습니다. 

> 또한, 이 포스트를 진행하기전에 Docker Hub에 계정을 만드시면 됩니다.

이번 포스트에서는 Docker를 이용하여 배포를 해보겠습니다. Docker에 대해서 잘 모르시는 분들은 [Docker 포스트](/docker-introduction)을 보고 오시면 되겠습니다.

제일먼저 Docker를 설치해주셔야 합니다.

## 1. Docker Install

```
$ sudo apt-get remove docker docker-engine docker.i

$ sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

$ sudo add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) \
 stable"
 
$ sudo apt-get update
$ sudo apt-get install docker-ce

# 설치 되었는지 확인
$ docker version

Client: Docker Engine - Community
 Version:           19.03.4
 API version:       1.40
 Go version:        go1.12.10
 Git commit:        9013bf583a
 Built:             Fri Oct 18 15:53:51 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.4
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.10
  Git commit:       9013bf583a
  Built:            Fri Oct 18 15:52:23 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

### 1-1. Dockerfile 작성

그리고 빌드에 사용될 Dockerfile을 작성해줍니다.

```
FROM ubuntu:latest
MAINTAINER your_name "khsh5592"
RUN apt-get update -y
RUN apt-get install python3.6 -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /app
RUN ls -la /app/*
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["application.py"]
```

### 1-2. requirements.txt 작성

```
pip freeze > requirements.txt
```

명령어를 이용해서 python package 정보가 담겨있는 파일을 만들어줍니다. 그러면 쓸데 없는 package들이 많이 들어 있을텐데 Flask 제외하고 전부 지워버리겠습니다.

> requirements.txt

```
Flask==1.1.1
```

### 1-3. Docker 로그인

```
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: khsh5592
Password:
WARNING! Your password will be stored unencrypted in /home/vagrant/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

### 1-4. Docker Build

Build하기 전 파일 목록들

```
$ ls
Dockerfile  app.py  requirements.txt
```

Docker Build

```
$ docker build -t khsh5592/suwon-kakaoplus:0.0 .
```

만들어진 모습

```
$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED              SIZE
khsh5592/suwon-kakaoplus   0.0                 4671f6d943f4        43 seconds ago       547MB
```

### 1-5. Docker Push to Hub

```
$ docker push khsh5592/suwon-kakaoplus:0.0
```

> Docker Hub Repository

![image](https://user-images.githubusercontent.com/44635266/68525352-f05b5200-0313-11ea-9f31-cc2af1471933.png)

이 Docker Hub 에 올라간 image 는 아래 명령어를 통해 다시 다른환경에서 가져와서 사용할 수 있습니다.

```
docker pull khsh5592/suwon-kakaoplus:0.0
```

## 2. AWS Port 열기

이대로 Docker 를 실행시켜도 상관없지만 AWS에 EC2 포트는 막혀있기 때문에 열어 주어야 합니다.

해당 방법은 [AWS http 포트 열기](https://carfediem-is.tistory.com/9) 포스트를 참고하셔서 8888 포트를 열어주시면 되겠습니다.

## 3. Docker Container 배포

```
$ sudo docker run -p 8888:8888 khsh5592/suwon-kakaoplus:0.0
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8888/ (Press CTRL+C to quit)
 
$ docker ps
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS                    NAMES
b1be793e81aa        khsh5592/suwon-kakaoplus:0.0   "python3 application…"   2 seconds ago       Up 1 second         0.0.0.0:5000->5000/tcp   compassionate_gagarin
```

### 3-1. 작동 확인

http://52.78.63.229:8888/keyboard 먼저 GET을 확인하기 위해 AWS Instance 주소와 포트입력해서 접속해보겠습니다.

> Chrome

![image](https://user-images.githubusercontent.com/44635266/68695706-ddb87580-05be-11ea-8d01-cc3c8115d543.png)

정상적으로 작동합니다.

이제 카카오 플러스 친구와 연동을 해보겠습니다.

![image](https://user-images.githubusercontent.com/44635266/68695710-dee9a280-05be-11ea-9e6e-85e62ceeead5.png)

![image](https://user-images.githubusercontent.com/44635266/68695713-e01acf80-05be-11ea-8b3d-a05cea5fc86c.png)

잘 작동하네요. 여기서 마무리 지을게요.

> Log

```
sudo docker run -p 8888:8888 khsh5592/suwon-kakaoplus:0.0
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8888/ (Press CTRL+C to quit)
211.214.14.153 - - [12/Nov/2019 17:37:28] "GET /keyboard HTTP/1.1" 200 -
211.214.14.153 - - [12/Nov/2019 17:37:28] "GET /favicon.ico HTTP/1.1" 404 -
219.249.231.41 - - [12/Nov/2019 17:39:13] "POST /message HTTP/1.1" 200 -
```

구름에서 Docker 가 막혀있는걸 너무 늦게 깨달았습니다. 그래서 AWS로 변화해서 혼선을 주어 죄송합니다.

긴 포스트 읽어주셔서 감사합니다.

