
---
title : Kafka Install
sidebar_main : true
use_math : true
header:
  # teaser :
  # overlay_image :

---


### Version

 * OS 
 
```
MacOS Mojave Version 10.14.6
```

* Java 

```
$ java -version
openjdk version "1.8.0_222"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_222-b10)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.222-b10, mixed mode)

$ javac -versionw
javac 1.8.0_222
```


###  Install Kafka

```
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


Kafka 를 실행하기 위해선 반드시 Zookeeper를 먼저 실행시켜주어야 한다.

#### Zookeeper Server Start

```
$ zookeeper-server-start /usr/local/Cellar/kafka/2.3.0/libexec/config/zookeeper.properties
```

#### Kafka Server Start

```
$ kafka-server-start /usr/local/Cellar/kafka/2.3.0/libexec/config/server.properties
```

서버를 실행시키는 로그가 엄청 깁니다. 로그를 확인해보고 싶으신분은 [여기](/kafka-logs)를 클릭해 주세요. *상당히 깁니다* 

### Demo - Create Topic, Using Producer / Consumer

*Create Topic* 1 Partitions

```
$ kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic firstMytopic
Created topic firstMytopic.
```

*Topic List*

```
$ kafka-topics --list --zookeeper localhost:2181
firstMytopic
```

*Publish Message (Producer)*

`kafka-console-producer --broker-list localhost:9092 --topic firstMytopic`

*Subscribe Message (Consumer)*

`$ kafka-console-consumer —bootstrap-server localhost:9092 —topic firstMytopic —from-beginning`

아래 사진을 봤을때 왼쪽이 `Producer` 오른쪽이 `Consumer` 입니다. Producer에서 메세지를 치면 Consumer에서 받는것을 확인할 수 있습니다.

<img width="1208" alt="스크린샷 2019-10-05 오후 8 16 35" src="https://user-images.githubusercontent.com/44635266/66254141-438a3400-e7ad-11e9-833e-661e7ac826fd.png">


*Stop Kafka Server*

```
$ kafka-server-stop
```

*Stop Zookeeper Server*

```
$ zookeeper-srver-stop
```


앞전에서 `partition` 개수를 여러개로 늘려서 병렬 처리를 하는 경우에는 순서가 보장 안된다고 했습니다. 해당 예제를 시험해 본 결과를 `Kafka Tools`로 확인해 보겠습니다.

<img width="958" alt="스크린샷 2019-10-03 오전 12 37 14" src="https://user-images.githubusercontent.com/44635266/66254139-41c07080-e7ad-11e9-9675-458477ea8289.png">

1, 2, 3, 4 / 5, 6, 7, 8 / 9, 10 데이터로 저장이되며 파티션의 개수대로 offset은 정해지지만 세부적으로는 순서가 보장이 안되는것을 확인하실 수 있습니다.

