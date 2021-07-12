---
title : Ubuntu Docker / Docker Compose Install
tags :
- Ubuntu
- Docker Compose
- Docker
- Install
- DevOps
categories:
- DevOps
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## Install Docker

기존에 설치된 Docker 엔진을 먼저 삭제합니다.

```
$ sudo apt-get remove docker docker-engine docker.i
```

의존성(depedencies) 패키지를 설치합니다.

```
$ sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
software-properties-common
```

Docker 레포지토리 GPG 키를 추가합니다.

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```
$ sudo add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) \
 stable"
```
 
Docker를 설치합니다.

```
$ sudo apt-get update
$ sudo apt-get install docker-ce
```

현재 사용자에게 Docker엔진 제어 권한을 부여하기 위해 docker 그룹에 포함시킵니다.

```
$ sudo usermod -a -G docker $USER
```

터미널/콘솔 재 로그인 후 도커가 정상적으로 설치되었는 지 확인합니다.

```
$ docker version
Client:
 Version:           18.09.2
 API version:       1.39
 Go version:        go1.10.6
 Git commit:        6247962
 Built:             Sun Feb 10 04:13:50 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.2
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.6
  Git commit:       6247962
  Built:            Sun Feb 10 03:42:13 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```

## Install Docker Compose

Docker Compose 파일을 /usr/local/bin 디렉토리에 다운로드 합니다.

```
$ sudo curl -L https://github.com/docker/compose/releases/download/1.23.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

Docker Compose 파일(docker-compose)에 실행권한을 설정합니다.

```
$ sudo chmod +x /usr/local/bin/docker-compose
```

Docker Compose가 정상적으로 설치되었는 지 확인 합니다.

```
$ docker-compose --version
docker-compose version 1.23.2, build 1110ad01
```

> Docker 에러 발생시

```
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/json: dial unix /var/run/docker.sock: connect: permission denied
```

**1번째 방법**

Create the docker group.

```
$ sudo groupadd docker
```

Add your user to the docker group.

```
$ sudo usermod -aG docker $USER
```

Logout and login again and run (that doesn't work you may need to reboot your machine first)

```
$ docker run hello-world
```

**2번째 방법**

```
sudo chmod 666 /var/run/docker.sock
```

