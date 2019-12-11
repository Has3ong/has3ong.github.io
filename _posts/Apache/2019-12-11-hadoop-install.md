---
title : Installing Hadoop on macOS
tags :
- macOs
- Install
- Hadoop
---

> Java Version

```shell
$ java -version

openjdk version "1.8.0_232"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_232-b09)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.232-b09, mixed mode)
```

## Install Hadoop

```shell
$ brew install hadoop

==> Downloading https://www.apache.org/dyn/closer.cgi?path=hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz
==> Downloading from http://apache.mirror.cdnetworks.com/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz
######################################################################## 100.0%
```

## Configuration

하둡 관련 설정을 위하여 4가지 파일을 수정해야합니다. 파일에 위치는 `/usr/local/Cellar/hadoop/3.2.1/libexec/etc/hadoop` 에 있습니다.

1. hadoop-env.sh
2. core-site.xml
3. mapred-site.xml
4. hdfs-site.xml

### 1. hadoop-env.sh

```
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"
```

을 아래와같이 변경시켜줍니다.

```
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true -Djava.security.krb5.realm= -Djava.security.krb5.kdc="
```

### 2. core-site.xml

HDFS 주소와 포트 넘버를 설정해줍니다. 아래 내용을 추가시켜줍니다.

```
<!-- Put site-specific property overrides in this file. --><configuration>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/usr/local/Cellar/hadoop/hdfs/tmp</value>
    <description>A base for other temporary directories</description>             
  </property>
  <property>
    <name>fs.default.name</name>
    <value>hdfs://localhost:8020</value>
  </property>
</configuration>
```

### 3. mapred-site.xml

아래 내용을 추가시켜줍니다.

```
<configuration>
  <property>
    <name>mapred.job.tracker</name>
    <value>localhost:8021</value>
  </property>
</configuration>
```

### 4. hdfs-site.xml

아래 내용을 추가시켜줍니다.

```
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
```

## Start Hadoop

하둡을 실행하기 전에, 하둡 파일 시스템으로 포맷을 해야 한다. 아래와 같이 입력하여 하둡 파일 시스템으로 포맷한다.

```shell
$ hdfs namenode -format
```

위의 명령어로 하둡 파일 시스템으로 포맷을 해 주고, 아래와 ssh key를 생성하고 사용한다.

```shell
$ ssh-keygen -t rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

마지막으로 맥북에 시스템 환경설정 공유에가서 원격 로그인을 체크해줍니다.

![image](https://user-images.githubusercontent.com/44635266/70542642-6d484880-1bac-11ea-8d6e-c4b8f02c0542.png)

이제 하둡을 실행해보자. 아래와 같이 실행하면 하둡을 실행시킬 수 있습니다.

```shell
$ /usr/local/Cellar/hadoop/3.2.1/sbin/start-dfs.sh

Starting namenodes on [localhost]
Starting datanodes
Starting secondary namenodes [gimhaseong-ui-MacBookPro.local]
2019-12-11 00:20:00,613 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
```

localhost로 하둡을 띄운 것이기 때문에, localhost로 접속해서 하둡의 상태를 체크할 수 있다. hadoop의 상태를 체크할 수 있는 주소는 아래와 같다.

- Cluster status: http://localhost:8088
- HDFS status: http://localhost:9870 ( 3.x는 9870, 2.x는 50070)
- Secondary NameNode status: http://localhost:9868 ( 3.x는 9868, 2.x는 50090)

![image](https://user-images.githubusercontent.com/44635266/70542647-6e797580-1bac-11ea-84aa-2df8617587e2.png)

![image](https://user-images.githubusercontent.com/44635266/70542652-6faaa280-1bac-11ea-8c3a-dbe25c3ba68b.png)

