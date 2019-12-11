---
title : Install MongoDB on Ubuntu 18.04
tags :
- Ubuntu18.04
- Install
- MongoDB
---

**public key 임포트**

PMS(Package Management System)의 일종인 Ubuntu 패지키 관리 툴(dpkg 그리고 apt)은 package 의 일관성(consistency)과 진위여부(authenticity)를 판별합니다. 이때 배포자(distributor, MongoDB Inc)로 하여금 GPG 키로 패키지들을 서명하기를 요구합니다.

이를 임포트하여 패키지 관리 툴에게 키 정보를 입력합니다.

```shell
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```

**list 파일 생성**

apt 명령어를 사용하여 패키지 설치 시 패키지 명령어를 받아올 장소를 알고 있어야 합니다. 따라서 list 파일을 만들어 둡니다.

만약에 `apt-get update` 명령 상에 문제가 발생하는 경우 이는 list 파일의 문제입니다.

아래의 명령어를 입력하여 리스트 파일을 생성합니다.

```shell
$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```

Local 의 패키지 DB 를 리로드합니다.

```shell
$ sudo apt-get update
```

MongoDB 설치
  
```shell
$ sudo apt-get install -y mongodb-org
```

정상적으로 설치된 모습

```shell
$ sudo systemctl status mongod
● mongod.service - MongoDB Database Server
   Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset:
   Active: active (running) since Thu 2019-11-28 04:32:47 UTC; 1h 38min ago
     Docs: https://docs.mongodb.org/manual
 Main PID: 1761 (mongod)
   CGroup: /system.slice/mongod.service
           └─1761 /usr/bin/mongod --config /etc/mongod.conf

Nov 28 04:32:47 ip-172-26-8-131 systemd[1]: Started MongoDB Database Server.
Nov 28 04:45:05 ip-172-26-8-131 systemd[1]: mongod.service: Current command vani
lines 1-10/10 (END)
```

```shell
$ mongo
MongoDB shell version v4.0.13
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("ffe96d9e-624a-420f-8b1a-c0fd688c0625") }
MongoDB server version: 4.0.13
Server has startup warnings:
2019-11-28T04:32:47.661+0000 I STORAGE  [initandlisten]
2019-11-28T04:32:47.661+0000 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2019-11-28T04:32:47.661+0000 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2019-11-28T04:32:48.838+0000 I CONTROL  [initandlisten]
2019-11-28T04:32:48.838+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2019-11-28T04:32:48.838+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2019-11-28T04:32:48.838+0000 I CONTROL  [initandlisten]
---
Enable MongoDB's free cloud-based monitoring service, which will then receive and display
metrics about your deployment (disk utilization, CPU, operation statistics, etc).

The monitoring data will be available on a MongoDB website with a unique URL accessible to you
and anyone you share the URL with. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command: db.enableFreeMonitoring()
To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---

>
```