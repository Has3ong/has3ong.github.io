---
title :Installing and Configuring Kafka -1-
tags :
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## OS 

```
MacOS Mojave Version 10.14.6
```

## Installing Java

```shell
$ brew tap adoptopenjdk/openjdk
$ brew cask install adoptopenjdk8
```

```shell
$ java -version
openjdk version "1.8.0_222"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_222-b10)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.222-b10, mixed mode)

$ javac -versionw
javac 1.8.0_222
```

## Installing Zookeeper / Kafka

Kafka는 Zookeeper를 사용한다. `Example 1` 과 같이 컨슈머 클라이언트와 카프카 클러스터에 관한 메타데이터를 저장하기 위해서다.

> Example 1 - Kafka and Zookeeper

![image](https://user-images.githubusercontent.com/44635266/70038753-21b9fb80-15fc-11ea-8612-f27dcc3fbfc2.png)

Brew 명령어를 이용하면 Kafka 설치할 때 Zookeeper 도 함께 설치가 된다.

```shell
$ brew install kafka

==> Installing dependencies for kafka: zookeeper
==> Installing kafka dependency: zookeeper
==> Downloading https://homebrew.bintray.com/bottles/zookeeper-3.4.12.high_sierra.bottle.tar.gz
######################################################################## 100.0%
==> Pouring zookeeper-3.4.12.high_sierra.bottle.tar.gz
==> Caveats
To have launchd start zookeeper now and restart at login:
  brew services start zookeeper
Or, if you don't want/need a background service you can just run:
  zkServer start
==> Summary
🍺  /usr/local/Cellar/zookeeper/3.4.12: 242 files, 32.9MB
==> Installing kafka
==> Downloading https://homebrew.bintray.com/bottles/kafka-2.3.0.high_sierra.bottle.tar.gz
######################################################################## 100.0%
==> Pouring kafka-2.3.0.high_sierra.bottle.tar.gz
==> Caveats
To have launchd start kafka now and restart at login:
  brew services start kafka
Or, if you don't want/need a background service you can just run:
  zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
==> Summary
🍺  /usr/local/Cellar/kafka/2.3.0: 160 files, 46.8MB
==> Caveats
==> zookeeper
To have launchd start zookeeper now and restart at login:
  brew services start zookeeper
Or, if you don't want/need a background service you can just run:
  zkServer start
==> kafka
To have launchd start kafka now and restart at login:
  brew services start kafka
Or, if you don't want/need a background service you can just run:
  zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
```

### Zookeeper Ensemble

Zookeeper는 Kafka와 같은 분산 처리 시스템의 서버들에 관한 메타데이터들을 통합 관리하는데 사용된다. 주키퍼의 클러스터를 앙상블이라고 하며, 하나의 **앙상블(ensemble)** 은 여러개의 서버를 멤버로 가질 수 있다.

Zookeeper에 문제가 생겨 서비스를 제공할 수 없을때 대기 중인 서버중에서 자동 선정하여 새롭게 선택된 서버가 해당 서비스를 이어받아 처리함으로 서버가 중단되지 않게 한다. 이를 **리더(Leader)** 라 하며, 나머지 대기 서버를 **팔로워(Follower)** 라고한다.

Zookeeper 서버를 앙상블로 구성할려면 `zookeeper.properties` 를 확인해보면 된다. 해당 파일은 `/usr/local/Cellar/kafka/2.3.0/libexec/config` 디렉토리에 있다.

```shell
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# the directory where the snapshot is stored.
dataDir=/usr/local/var/lib/zookeeper
# the port at which the clients will connect
clientPort=2181
# disable the per-ip l

# --------------------------------------------------------

# dataDir=/var/lib/zookeeper
# initTime=20
# tickTime=2000
# syncLimit=5
# server.1=zookeeper1.example.com:2888:3888
# server.2=zookeeper2.example.com:2888:3888
# server.3=zookeeper3.example.com:2888:3888
```

중간에 구분선을 아래에 있는 내용은 제가 임의로 작성한 내용입니다.

**initTime**

팔로워가 리더에 접속할 수 있는 시간이다. 이는 ticktime의 값을 기준으로 설정한다. 20 * 2000 ms 즉 40초가된다.

**syncLimit**

리더가 될 수 있는 팔로워들의 최대 개수다.

**server.1**

앙상블을 할 때 엮을 Zookeeper의 서버다.

### Start Kafka

```shell
$ zookeeper-server-start /usr/local/Cellar/kafka/2.3.0/libexec/config/zookeeper.properties

$ $ kafka-server-start /usr/local/Cellar/kafka/2.3.0/libexec/config/server.properties
```

서버를 실행시키는 로그가 엄청 깁니다. 로그를 확인해보고 싶으신분은 [여기](/kafka-logs)를 클릭해 주세요. *상당히 깁니다*

**Create Topic 1 Partitions**

```shell
$ kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic firstMytopic
Created topic firstMytopic.
```

**Topic List**

```shell
$ kafka-topics --list --zookeeper localhost:2181
firstMytopic
```

**Publish Message (Producer)**

```shell
kafka-console-producer --broker-list localhost:9092 --topic firstMytopic
```

**Subscribe Message (Consumer)**

```shell
$ kafka-console-consumer —bootstrap-server localhost:9092 —topic firstMytopic —from-beginning
```

아래 사진을 봤을때 왼쪽이 `Producer` 오른쪽이 `Consumer` 입니다. Producer에서 메세지를 치면 Consumer에서 받는것을 확인할 수 있습니다.

<img width="1208" alt="스크린샷 2019-10-05 오후 8 16 35" src="https://user-images.githubusercontent.com/44635266/66254141-438a3400-e7ad-11e9-833e-661e7ac826fd.png">


**Stop Kafka Server**

```shell
$ kafka-server-stop
```

**Stop Zookeeper Server**

```shell
$ zookeeper-srver-stop
```

Kafka 에서도 `server.properties` 를 확인해보면 반드시 검토해야하는 브로커 구성 매개변수들이 있습니다. 이는 내용이 길어질꺼 같으니 다음 포스트에 정리하겠습니다.