---
title : Centos7 / Apache - Tomcat - JK Connector Load Balancing
tags :
- WEB
- WAS
- Load Balancing
- AJP
- Tomcat
- Apache
- Centos
categories:
- WEB / WAS
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

Load Balancing 에 대한 개념을 모르신다면 [Load Balancing](/loadbalancing) 포스트를 보시면 됩니다.

환경 구성은 아래 포스트에서 잡은 환경을 바탕으로 진행하겠습니다.

1. [[Centos7] Apache - Tomcat - JK Connector 연동하기](/web-apacheconnectortomcat) 

## Version

사용한 버전은 아래와 같습니다.

* **Vagrant** : 2.2.6
* **Java** : openjdk-1.8.0
* **Apache Tomcat** : 9.0.34
* **Apache httpd** : 2.4.43
* **Tomcat Connectors** : 1.2.48

## Setting Tomcat Multi Instances

하나의 VM 에서 여러개의 Tomcat 을 올려야 하기 때문에 Tomcat 에 있는 파일을 복사해 각각 instance1, instance2 를 만들어주겠습니다.

```shell
$ cd /opt/
$ ls
$ mkdir instance1
$ mkdir instance2
$ ls
instance1  instance2  tomcat
$ cp -r tomcat/ instance1
$ cp -r tomcat/ instance2
```

계층 구조를 보면 아래와 같습니다. 보통 모든 파일이 필요하지는 않지만 빠르게 구현하기 위해 통채로 복사했습니다.

```shell
$ tree . -L 2
.
├── instance1
│   └── tomcat
├── instance2
│   └── tomcat
└── tomcat
    ├── BUILDING.txt
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── NOTICE
    ├── README.md
    ├── RELEASE-NOTES
    ├── RUNNING.txt
    ├── bin
    ├── conf
    ├── lib
    ├── logs
    ├── temp
    ├── webapps
    └── work
```

포트는 아래와 같이 지정해주겠습니다.

* Tomcat
  * Server shutdown Port : 8005
  * HTTP Port : 8080
  * redirectPort : 8443
  * AJP Port : 8009
* instance1
  * Server shutdown Port : 18005
  * HTTP Port : 18080
  * redirectPort : 18443
  * AJP Port : 18009
* instance2
  * Server shutdown Port : 28005
  * HTTP Port : 28080
  * redirectPort : 28443
  * AJP Port : 28009

그리고 각 파일에 *server.xml* 과 *index.jsp* 를 아래와 같이 수정해줍니다.

> instance 1

```shell
$ vi /opt/instance1/tomcat/conf/server.xml
```

```xml
<Server port="18005" shutdown="SHUTDOWN">

<Connector port="18080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="18443" />

<Connector protocol="AJP/1.3"
            address="::1"
            port="18009"
            redirectPort="18443"
            secretRequired="false"/>
```

```shell
$ vi /opt/instance1/tomcat/webapps/ROOT/index.jsp
```

```jsp
<html>
  <head>
  </head>
  <body>
    <h1> Instance 1 Apache Tomcat </h1>
  </body>
</html>
```

> instance 2

```shell
$ vi /opt/instance2/tomcat/conf/server.xml
```

```xml
<Server port="28005" shutdown="SHUTDOWN">

<Connector port="28080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="28443" />

<Connector protocol="AJP/1.3"
               address="::1"
               port="28009"
               redirectPort="28443"
               secretRequired="false"/>
```

```shell
$ vi /opt/instance2/tomcat/webapps/ROOT/index.jsp
```

```xml
<html>
  <head>
  </head>
  <body>
    <h1> Instance 2 Apache Tomcat </h1>
  </body>
</html>
```

앞전과 마찬가지로 Tomcat 에 접속해야하는 18080 과 28080 포트를 열어줍니다.

```shell
$ firewall-cmd --permanent --zone=public --add-port=18080/tcp
success
$ firewall-cmd --permanent --zone=public --add-port=28080/tcp
success
$ firewall-cmd --reload
```

그리고 각각의 Tomcat 인스턴스를 시작시켜주고 종료시켜줄 Shell 파일을 만들어줍니다.

> startup.sh

```shell
$ vi /opt/instance1/tomcat/startup.sh
```

```shell
#!/bin/sh

export CATALINA_BASE=/opt/instance1/tomcat/
export TOMCAT_HOME=/opt/tomcat/
cd $TOMCAT_HOME/bin
./startup.sh

$ chmod +x starup.sh
```

> shutdown.sh

```shell
$ vi /opt/instance1/tomcat/shutdown.sh
```

```shell
#!/bin/sh

export CATALINA_BASE=/opt/instance1/tomcat/
export TOMCAT_HOME=/opt/tomcat/
cd $TOMCAT_HOME/bin
./shutdown.sh

$ chmod +x shutdown.sh
```

여기까지 설정이 완료되면 모든 Tomcat 인스턴스를 시작시켜서 8080, 18080, 28080 포트로 접속해서 정상적으로 작동하는지 확인해보겠습니다.

> 10.30.30.2:8080

![image](https://user-images.githubusercontent.com/44635266/80597912-80788980-8a63-11ea-8ee5-0bcdfe287087.png)

> 10.30.30.2:18080

![image](https://user-images.githubusercontent.com/44635266/80800469-847fe500-8be4-11ea-989c-e756a0423a9a.png)

> 10.30.30.2:28080

![image](https://user-images.githubusercontent.com/44635266/80800480-8e094d00-8be4-11ea-9871-fa431aa833e7.png)

각각의 주소에서 위와같이 화면이 보이면 정상적으로 설정이 완료된겁니다. 이제 Tomcat 과 Apache 를 모두 종료시킨 다음 Load Balancing 을 셋팅해보겠습니다.

## Setting JK Connector Load Balancing

먼저 *httpd.conf* 파일에 들어가서 아래와 같이 설정을 바꿔줍니다.

```shell
$ vi /usr/local/apache24/conf/httpd.conf
```

```conf
LoadModule jk_module modules/mod_jk.so
JkWorkersFile conf/workers.properties
JkLogFile logs/mod_jk.log
JkShmFile logs/mod_jk.shm
JkMount /* load_balancer
```

*workers.properties* 로 들어가서 아래와 같이 내용을 등록해줍니다.

```shell
$ vi /usr/local/apache24/conf/workers.properties
```

```shell
worker.list=load_balancer

worker.load_balancer.type=lb
worker.load_balancer.balance_workers=tomcat1,instance1,instance2

worker.tomcat1.port=8009
worker.tomcat1.host=localhost
worker.tomcat1.type=ajp13
worker.tomcat1.lbfactor=1

worker.instance1.port=18009
worker.instance1.host=localhost
worker.instance1.type=ajp13
worker.instance1.lbfactor=1

worker.instance2.port=28009
worker.instance2.host=localhost
worker.instance2.type=ajp13
worker.instance2.lbfactor=1
```

위 파일을 보면 각각 `load_balancer` 의 노드로 `tomcat1`, `instance1`, `instance2` 설정을 해놨고 AJP 프로토콜을 이용하여 미리 지정한 8009, 18009, 28009 포트로 접속하게 설정했습니다.

`worker.load_balancer.type=lb` 는 이 `load_balancer` 를 Load Balancing 하겠다는 의미입니다.

`lbfactor` 는 전부 1 로 설정해놨는데 Load Balancing 를 1 : 1 : 1 로 하겠다는 의미입니다.

이제 다시 재시작을해서 10.30.30.2 로 접속해보겠습니다.

> 10.30.30.2

![image](https://user-images.githubusercontent.com/44635266/80800682-0b34c200-8be5-11ea-917c-029f30bc32cf.png)

![image](https://user-images.githubusercontent.com/44635266/80800695-138cfd00-8be5-11ea-8df4-15053f848a8e.png)

![image](https://user-images.githubusercontent.com/44635266/80800709-1c7dce80-8be5-11ea-9abf-66cac349c067.png)

정상적으로 작동하는것을 확인할 수 있습니다.

만약 서버 접속이 안된다면 *httpd.conf* 접근 권한을 확인하면 됩니다.

```shell
<Directory /DOCUMENT_ROOT>
    Order allow,deny
    Allow from all
</Directory>
```

## JK Status Manager

마지막으로 JK Status Manager 설정까지 알아보고 마무리하겠습니다. 설정은 아래와 같이 하면 됩니다. 

현재 Web Server / WAS 의 상태를 알아볼 수 있습니다.

```shell
$ vi /usr/local/apache24/conf/httpd.conf
```

```shell
JkMount /jkmanager/* jkstatus

<Location /jkmanager/>
    JkMount jkstatus
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
</Location>
```

*workers.properties* 에서 맨 아래에 내용을 추가해줍니다.

```shell
$ vi /usr/local/apache24/conf/workers.properties
```

```
worker.list=jkstatus
worker.jkstatus.type=status
```

만약 `AH01797: client denied by server configuration:` 오류가 발생하면, 접근 권한이 막혀있을 수 있기 때문에 *httpd.conf* 파일에 아래 내용을 추가해주면 됩니다.

```shell
<Location /jkmanager/>
    JkMount jkstatus
    Require all granted
</Location>
```

10.30.30.2/jkmanager/ 로 접속하면 됩니다.

![image](https://user-images.githubusercontent.com/44635266/80800973-eb51ce00-8be5-11ea-8aab-6995ce08d7a0.png)

다음 포스트로는 Tomcat Session Clustering 을 해보겠습니다.