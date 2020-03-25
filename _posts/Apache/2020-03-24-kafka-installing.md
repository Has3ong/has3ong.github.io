---
title : Installing Kafka
tags :
- Install
- Apache
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## First Things First 

Kafka 를 설치하고 사용하기 전에 우선해야할 일이 있습니다. 그것이 무엇인지 알아보겠습니다.

### Choosing an Operating System 

Kafka 는 자바 어플리케이션이므로 다양한 OS 에서 실행 될 수 있습니다. 위 포스트에선 Linux 에서 Kafka 를 설치하고 사용하는 데 초점을 두겠습니다. Kafka 가 많이 설치되고 권장되는 운영체제이기 때문입니다.

### Installing Java 

주키퍼와 Kafka 를 설치하기 전에 자바를 사용할 수 있도록 JDK(Java Development Kit) 를 설치해야 합니다. JDK 8 버전으로 사용할 것입니다.

### Installing Zookeeper 

Kafka 는 주키퍼를 사용합니다. `Example 1` 과 같이 컨슈머 클라이언트와 Kafka 클러스터에 관한 메타데이터를 저장하기 위해서입니다. 주키퍼는 Kafka 배포판에 포함되어 있으므로 스크립트를 사용해서 실행할 수 있습니다.

> Example 1 - Kafka and Zookeeper

![image](https://user-images.githubusercontent.com/44635266/77315776-7cae6480-6d4b-11ea-8f5a-d8452b66dbc8.png)

#### Standalone Serve

다음은 별도로 다운로드한 zookeeper-3.4.6.tar.gz 를 사용해 주키퍼를 */usr/local/zookeeper* 에 기본 설치하고 데이터는 */var/lib/zookeeper* 에 저장하는 예입니다.

```shell
$ tar -zxf zookeeper-3.4.6.tar.gz
$ mv zookeeper-3.4.6 /usr/local/zookeeper
$ mkdir -p /var/lib/zookeeper
$ cat > /usr/local/zookeeper/conf/zoo.cfg << EOF
> tickTime=2000
> dataDir=/var/lib/zookeeper
> clientPort=2181
> EOF
$ export JAVA_HOME=/usr/java/jdk1.8.0_51
$ /usr/local/zookeeper/bin/zkServer.sh start
JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
$
```

이제 클라이언트 포트로 주키퍼에 연결하여 `srvr` 명령어를 실행시키는 것입니다.

```shell
$ telnet localhost 2181
Trying ::1...
Connected to localhost.
Escape character is '^]'.
srvr
Zookeeper version: 3.4.6-1569965, built on 02/20/2014 09:09 GMT
Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: standalone
Node count: 4
Connection closed by foreign host.
$
```

#### Zookeeper ensemble

주키퍼는 Kafka 와 같은 분산처리 시스템의 서버들에 관한 메타데이터를 통합 관리하는 데 사용합니다. 주키퍼의 클러스트를 **앙상블(Ensemble)** 이라 하며, 하나의 앙상블은 여러 개의 서버를 멤버로 가질 수 있습니다.

이때 하나의 서버에만 서비스가 집중되지 않게 분산하여 동시에 처리하며, 한 서버에서 처리한 결과를 다른 서버와 동기화시켜 데이터의 안정성을 보장합니다. 또한, 클라이언트와 연결되어 현재 동작 중인 서비스에 문제가 생겨 서비스를 제공할 수 없을 때 대기중인 서버 중에 자동 선정하여 새로 선택된 서버가 해당 서비스를 이어받아 처리함으로써 서비스가 중단죄이 낳게 합니다.

이처럼 요청에 대한 응답을 항상 빠르고 안정적으로 하기 위해 앙상블은 홀 수 개의 서버를 멤버로 가집니다. 그래서 과반수가 작동가능하다면 언제든 요청 처리가 가능합니다.

주키퍼 서버를 앙상블로 구성하려면 각 서버가 공통된 구성파일을 가져야 합니다. 또한, 각 서버는 자신의 ID 번호를 지정한 `myid` 파일을 데이터 디렉터리에 갖고 있어야 합니다. 예를 들어 앙상블에 속한 서버들의 호스트 이름이 `zoo1.example.com`, `zoo2.example.com`, `zoo3.example.com` 이라면 구성 파일 내역은 다음과 같이 됩니다.

```shell
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=20
syncLimit=5
server.1=zoo1.example.com:2888:3888
server.2=zoo2.example.com:2888:3888
server.3=zoo3.example.com:2888:3888
```

`initLimit` 은 팔로어가 리더에 접속할 수 있는 시간이며, `tickTime` 의 값을 기준으로 설정됩니다. 따라서 여기선 `initTime` 이 20 * 2000 ms, 즉 40 초가 됩니다. `syncLimit` 은 리더가 될 수 있는 팔로어의 최대 개수를 나타냅니다.

구성 파일에는 앙상블의 모든 서버 내역도 지정하며 `server.X=hostanme:peerPort:leaderPort` 형식을 사용합니다.

* X
  * 각 서버의 ID 번호이며 정수다. 0 부터 시작되지 않고 순차적으로 부여하지 않아도된다.
* hostname
  * 각 서버의 호스트 이름이나 IP 주소
* peerPort
  * 앙상블의 서버들이 상호 통신하는 데 사용하는 TCP 포트 번호
* leaderPort
  * 리더를 선출하는 데 사용하는 TCP 포트 번호

주키퍼에 접속하는 클라이언트는 `clientPort` 에 지정된 포트 번호로 앙상블과 연결됩니다. 그러나 앙상블의 서버들은 세 가지 포트 모두를 사용해서 상호 통신합니다.

공통 구성 파일에 추가하며 각 서버는 `dataDir` 에 지정된 `myid` 라는 이름의 파일을 갖고 있어야 합니다. 이 파일은 구성 파일에 지정된 것과 일치되는 각 서버의 ID 번호를 포함해야하며, 모든것이 완료되면 앙상블의 모든 서버가 시작되고 상호 통신합니다.

## Installing a Kafka Broker 

자바와 주키퍼가 설치 및 구성되면 Kafka 를 설치할 준비가 된 것입니다.

아래 예는 */usr/local/kafka* 에 Kafka 를 설치하고 시작시킵니다. 앞에서 시작시킨 주키퍼를 사용하고 */tmp/kafka-logs* 에 로그 메세지를 저장하도록 Kafka 를 구성하였습니다.

```shell
$ tar -zxf kafka_2.11-0.9.0.1.tgz
$ mv kafka_2.11-0.9.0.1 /usr/local/kafka
$ mkdir /tmp/kafka-logs
$ export JAVA_HOME=/usr/java/jdk1.8.0_51
$ /usr/local/kafka/bin/kafka-server-start.sh -daemon
/usr/local/kafka/config/server.properties
$
```

이제 Kafka 브로커가 시작되었으니 `test` 라는 토픽을 생성하고 몇가지 메세지를 쓰기한 후 읽기해보겠습니다.

```shell
$ /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 \
--replication-factor 1 --partitions 1 --topic test 
Created topic "test".

$ /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 \
--describe --topic test

Topic:test PartitionCount:1 ReplicationFactor:1 Configs:
 Topic: test Partition: 0 Leader: 0 Replicas: 0 Isr: 0
$
```

다음으로 `test` 토픽에 메세지를 써보겠습니다.

```shell
$ /usr/local/kafka/bin/kafka-console-producer.sh --broker-list \
localhost:9092 --topic test

Test Message 1
Test Message 2
^D
$
```

또한, `test` 토픽에 메세지를 읽어보겠습니다.

```shell
$ /usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper \
localhost:2181 --topic test --from-beginning

Test Message 1
Test Message 2
^C
Consumed 2 messages
$
```

Kafka 콘솔 컨슈머 스레드로 계속 실행되므로 `Ctrl + C` 키를 눌러 중단시켜야 합니다.

## Broker Configuration 

특정 상황에 맞게 Kafka 브로커를 조정해야 할 때는 해당 설정을 변경해야 합니다.

### General Broker 

Kafka 를 설치할 때 반드시 검토해야 하는 브로커 구성 매개변수들이 있습니다. 브로커의 핵심 구성을 처리하며, 여러 브로커로 실행되는 클러스터에서 제대로 실행하려면 대부분 변경해야합니다.

#### broker.id

모든 Kafka 브로커는 `broker.id` 에 설정하는 정수로 된 번호를 가져야합니다. 기본 값은 0 이지만 다른 값도 가능합니다. 하지만, 하나의 Kafka 클러스터 내에서는 고유한 값이어야 합니다. 임의로 선택이 가능하며 유지보수 작업에 필요하다면 브로커 간에 바꿀 수 있습니다.

하지만, 브로커 호스트가 가지는 본질적인 값으로 설정하는 것이 좋습니다. 예를 들어 `host1.example.com` 이나 `host2.example.com` 등과 같이 호스트 이름의 고유번호가 있다면 이것을 `broker.id` 로 사용하는게 좋습니다.

#### port

Kafka 의 실행에 사용되는 TCP 포트입니다. 디폴트 값은 9092 로 설정되어 있습니다.

#### zookeeper.connect

브로커의 메타데이터를 저장하기 위해 사용되는 주키퍼의 위치를 나타냅니다. 기본 구성 값은 `localhost:2181` 설정되었습니다. `hostname:port/path` 의 형식으로 지정할 수 있습니다.

* **hostname**, the hostname or IP address of the Zookeeper server.
* **port**, the client port number for the server.
* **/path**, an optional Zookeeper path to use as a chroot environment for the Kafka cluster. If it is omitted, the root path is used.

*chroot* 가 지정되었지만, 존재하지 않으면 브로커가 시작될 때 자동으로 생성됩니다.

> *chroot* 경로를 사용하는 것이 좋습니다. Kafka 클러스터와 어플리케이션이 상호 충돌 없이 주키퍼 앙상블을 공유할 수 있기 때문입니다. 

#### log.dirs

Kafka 는 모든 메세지를 로그 세그먼트 파일에 모아 디스크에 저장합니다. 이 파일은 `log.dirs` 에 지정된 디렉토리에 저장됩니다. 이때 여러 경로를 쉼표로 구분하여 지정할 수 있습니다.

두 개 이상의 경로가 지정되면 해당 브로커가 모든 경로에 파티션을 저장합니다. 이때 사용 빈도가 가장 적은 데이터를 교체하는 방식으로 한 파티션의 모든 로그 세그먼트를 같은 경로에 저장합니다. 그리고 브로커가 새로운 파티션을 저장할 때는 가장 적은 디스크 용량을 사용하는 경로가 아닌 가장 적은 수의 파티션을 저장한 경로를 사용한다.

즉, 여러 디렉터리에 걸쳐 데이터가 항상 고르게 분산되는 것이 아닙니다.

#### num.recovery.threads.per.data.dir

Kafka 는 구성 가능한 스레드 풀을 사용해 로그 세그먼트를 처리합니다. 스레드 풀은 다음의 경우에 사용됩니다.

* 브로커가 정상적으로 시작될 때는 각 파티션의 로그 세그먼트 파일을 열기 위해 사용됩니다.
* 장애 발생 이후 다시 시작될 때는 각 파티션의 로그 세그먼트를 검사하고 불필요한 부분을 삭제하기 위해 사용
* 종료될 때는 로그 세그먼트 파일을 정상적으로 닫기 위해 사용

기본적으로 로그 디렉토리당 하나의 스레드만 사용합니다. 이 스레드들은 브로커의 시작과 종료시에만 사용되므로 병행 처리를 하도록 많은 수의 스레드를 설정하는 것이 좋습니다.

그리고 이 매개변수에 설정하는 스레드의 수는 `logs.dirs` 에 지정된 경로가 3 개일 때 `num.recovery.threads.per.data.dir` 를 8 로 설정하면 24 개가 됩니다.

#### auto.create.topics.enable

Kafka 의 기본 설정에는 이 값이 `true` 로 되어있습니다. 따라서 다음 경우에 브로커는 자동으로 하나의 토픽을 생성합니다.

* 프로듀서가 토픽에 메세지를 쓸 때
* 컨슈머가 토픽의 메세지를 읽기 시작할 때
* 클라이언트에서 토픽의 메타데이터를 요청할 때

Kafka 에서는 토픽을 생성하지 않고 존재 여부를 검사할 수 있는 방법이 없으므로 이렇게 합니다. 하지만 이것이 바람직하지 않은 경우가 많습니다. 그럴 때는 별도의 시스템을 사용하거나 `auto.create.topics.enable` 의 값을 `false` 로 지정하면 됩니다.

### Topic Defaults 

Kafka 서버의 구성에는 토픽의 생성에 관한 기본 설정 매개변수가 많이 있습니다. 그 중 파티션 개수나 메세지 보존 설정과 같은 매개변수들은 관리 도구를 사용해서 토픽마다 설정할 수 있으며, 클러스터의 대다수 토픽에 적합하도록 기본값이 설정되어 있습니다.

#### num.partitions

`num.partitions` 매개변수는 새로운 토픽이 몇 개의 파티션으로 생성되는지를 나타내며, 주로 자동 토픽 생성이 활성화(`auto.create.topics.enable=true`) 될 때 사용됩니다. 이것은 기본값은 1 입니다.

토픽의 파티션 개수는 증가만 가능하고 감소될 수 없습니다. 따라서 생성할 토픽이 `num.partitions` 의 값보다 작은 수의 파티션을 필요로 한다면 직접 토픽을 생성하는 것을 고려해야 합니다.

Kafka 클러스터 내에서 토픽의 크기가 확장되는 방법이 파티션입니다. 따라서 브로커가 추가될 때 클러스터 전체에 걸쳐 메세지가 고르게 저장되도록 파티션 개수를 설정하는 것이 중요합니다. 많은 사용자가 클러스터의 브로커 수와 같게 하거나 배수로 토픽의 파티션 개수를 설정합니다. 이렇게 하면 브로커마다 파티션이 고르게 분산될 수 있으며, 저장 메세지도 고르게 분산될 것입니다. 하지만, 토픽을 여러개 생성해도 저장 메세지를 고르게 분산시킬 수 있습니다.

#### log.retention.ms

Kafka 가 얼마 동안 메세지를 보존할 지 구성 파일에 설정할 때는 시간 단위인 `log.retention.hours` 매개변수를 주로 사용하며, 이것의 기본값은 1 주일인 168 시간 입니다. 그러나 이외에도 다른 2 개의 매개변수인 `log.retention.minutes` 와 `log.retention.ms` 를 사용할 수 있습니다. 3 개의 매개변수는 모두 지정된 시간이 지난 메세지는 삭제될 수 있다는 의미입니다.

가급적 `log.retention.ms` 를 사용하는게 낫습니다. 만약 2 개 이상 같이 지정되면 더 작은 시간 단위의 매개변수 값이 사용되므로 항상 `log.retention.ms` 이 사용됩니다.

#### log.retentions.bytes

저장된 메세지들의 전체 크기를 기준으로 만기를 처리할 때는 `log.retentions.bytes` 매개변수를 사용합니다. 이 값은 모든 파티션에 적용됩니다. 예를 들어 하나의 토픽이 8 개의 파티션으로 되어 있고, `log.retention.bytes` 의 값이 1 GB 로 설정되면 해당 토픽에 보존되는 메세지들의 전체 크기는 8 GB 가 됩니다.

이러한 메세지 보존은 토픽이 아닌 각 파티션별로 처리됩니다.

#### log.segment.bytes

앞에서 설명한 메세지 보존 설정은 개별적인 메세지가 아닌 로그 세그먼트 파일을 대상으로 처리됩니다. 메세지가 Kafka 브로커에 생성될 때는 해당 파티션의 로그 세그먼트 파일 끝에 추가됩니다.

이때 `log.segment.bytes` 매개변수에 지정된 크기가 되면 해당 로그 세그먼트 파일이 닫히고 새로운 것이 생성되어 열립니다. 그리고 닫힌 로그 세그먼트 파일은 만기가 된 것으로 간주할 수 있습니다. 따라서 로그 세그먼트의 크기를 더 작은 값으로 지정하면 더 빈번하게 파일이 닫히고 새로 생성되므로 전반적인 디스크 쓰기 효율을 감소시키게 됩니다.

#### log.segment.ms

`log.segment.ms` 매개변수를 사용해 시간을 지정해도 로그 세그먼트 파일이 닫히는것을 제어할 수 있습니다. `log.retention.bytes` 와 `log.retention.ms` 처럼 `log.segement.bytes` 와 `log.segment.ms` 는 상호 연관되어 있습니다.

즉 Kafka 는 `log.segment.bytes` 에 지정된 크기가 되거나 `log.segment.ms` 에 지정된 시간제한에 해당할 로그 세그먼트 파일을 닫습니다. 

#### message.max.bytes

Kafka 브로커는 쓰려는 메세지의 최대 크기를 제한할 수 있습니다. 이때 기본값이 1000000 (1 MB) 인 `message.max.bytes` 매개변수를 지정하면 됩니다. 그러면 이 값보다 큰 메세지를 전송하려는 프로듀서에게는 브로커가 에러를 보내고 메세지를 받지 않습니다.

## Hardware Selection 

Kafka 에 전체적인 성능에 영향을 주는 요소는 디스크 처리량 / 용량 / 메모리 / 네트워크 / CPU 를 고려해야합니다.

## Kafka Clusters 

Kafka 로 내부 개발이나 테스트할 때 하나의 Kafka 서버를 사용해도 잘 동작합니다. 하지만 `Example 2` 와 같이 다수의 브로커 서버를 하나의 클러스터로 구성하면 장점이 많습니다. 우선 다수의 서버로 처리량을 분산시켜 확장할 수 있다는 것이 가장 큰 장점입니다. 그리고 서버장애에 따른 데이터 유실을 막기 위해 복제를 할 수 있습니다.

> Example 2 - A simple Kafka cluster

![image](https://user-images.githubusercontent.com/44635266/77396092-60133a80-6de6-11ea-9804-5347efd15ba6.png)

복제를 사용하면 현재 사용중인 Kafka 시스템을 중단시키지 않고 유지보수 작업을 수행할 수 있습니다.

### How Many Brokers? 

Kafka 클러스터의 적합한 크기는 다음 몇 가지 요소로 결정됩니다.

첫 번째로 메세지를 보존하는데 필요한 디스크 옹량과 하나의 브로커에 사용 가능한 스토리지 크기 입니다. 하나의 클러스터에 10 TB 데이터를 보존해야 하고, 하나의 브로커가 2 TB 까지 사용하면, 이 클러스터는 최소 5 개의 브로커가 필요합니다.

두 번째는 클러스터 용량입니다. 네트워크 인터페이스의 처리 능력이 어떤지, 그리고 데이터의 컨슈머가 여럿이거나 데이터가 보존된 기간에 클라이언트 트래픽이 일정하지 않더라고 모든 클라이언트의 트래픽을 처리할 수 있는지 입니다.

### Broker Configuration 

하나의 클러스터에 다수의 브로커를 사용할 수 있도록 브로커를 구성할 때는 두 가지만 고려하면 됩니다.

첫 번째로, 모든 브로커의 구성 파일에 있는 `zookeeper.connect` 매개변수의 설정 값이 같아야 하는지 입니다. 이 매개변수에는 주키퍼 앙상블과 경로를 지정합니다.

두 번재로, `broker.id` 매개변수에는 클러스터의 모든 브로커가 고유한 값을 갖도록 지정되어야 합니다. 만일 같은 클러스터의 두 브로커가 같은 `broker.id` 값을 가진다면 두 번째 브로커는 에러가 생겨 시작되지 않을것입니다.