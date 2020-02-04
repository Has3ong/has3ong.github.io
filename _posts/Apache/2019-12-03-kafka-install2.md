---
title : Installing and Configuring Kafka -2-
tags :
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Kafka server.properties

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

# see kafka.server.KafkaConfig for additional details and defaults

############################# Server Basics #############################

# The id of the broker. This must be set to a unique integer for each broker.
broker.id=0

############################# Socket Server Settings #############################

# The address the socket server listens on. It will get the value returned from
# java.net.InetAddress.getCanonicalHostName() if not configured.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
#listeners=PLAINTEXT://:9092

# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
#advertised.listeners=PLAINTEXT://your.host.name:9092

# Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
#listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

# The number of threads that the server uses for receiving requests from the network and sending responses to the network
num.network.threads=3

# The number of threads that the server uses for processing requests, which may include disk I/O
num.io.threads=8

# The send buffer (SO_SNDBUF) used by the socket server
socket.send.buffer.bytes=102400

# The receive buffer (SO_RCVBUF) used by the socket server
socket.receive.buffer.bytes=102400

# The maximum size of a request that the socket server will accept (protection against OOM)
socket.request.max.bytes=104857600


############################# Log Basics #############################

# A comma separated list of directories under which to store log files
log.dirs=/usr/local/var/lib/kafka-logs

# The default number of log partitions per topic. More partitions allow greater
# parallelism for consumption, but this will also result in more files across
# the brokers.
num.partitions=1

# The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.
# This value is recommended to be increased for installations with data dirs located in RAID array.
num.recovery.threads.per.data.dir=1

############################# Internal Topic Settings  #############################
# The replication factor for the group metadata internal topics "__consumer_offsets" and "__transaction_state"
# For anything other than development testing, a value greater than 1 is recommended for to ensure availability such as 3.
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

############################# Log Flush Policy #############################

# Messages are immediately written to the filesystem but by default we only fsync() to sync
# the OS cache lazily. The following configurations control the flush of data to disk.
# There are a few important trade-offs here:
#    1. Durability: Unflushed data may be lost if you are not using replication.
#    2. Latency: Very large flush intervals may lead to latency spikes when the flush does occur as there will be a lot of data to flush.
#    3. Throughput: The flush is generally the most expensive operation, and a small flush interval may lead to excessive seeks.
# The settings below allow one to configure the flush policy to flush data after a period of time or
# every N messages (or both). This can be done globally and overridden on a per-topic basis.

# The number of messages to accept before forcing a flush of data to disk
#log.flush.interval.messages=10000

# The maximum amount of time a message can sit in a log before we force a flush
#log.flush.interval.ms=1000

############################# Log Retention Policy #############################

# The following configurations control the disposal of log segments. The policy can
# be set to delete segments after a period of time, or after a given size has accumulated.
# A segment will be deleted whenever *either* of these criteria are met. Deletion always happens
# from the end of the log.

# The minimum age of a log file to be eligible for deletion due to age
log.retention.hours=168

# A size-based retention policy for logs. Segments are pruned from the log unless the remaining
# segments drop below log.retention.bytes. Functions independently of log.retention.hours.
#log.retention.bytes=1073741824

# The maximum size of a log segment file. When this size is reached a new log segment will be created.
log.segment.bytes=1073741824

# The interval at which log segments are checked to see if they can be deleted according
# to the retention policies
log.retention.check.interval.ms=300000

############################# Zookeeper #############################

# Zookeeper connection string (see zookeeper docs for details).
# This is a comma separated host:port pairs, each corresponding to a zk
# server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
# You can also append an optional chroot string to the urls to specify the
# root directory for all kafka znodes.
zookeeper.connect=localhost:2181

# Timeout in ms for connecting to zookeeper
zookeeper.connection.timeout.ms=6000


############################# Group Coordinator Settings #############################

# The following configuration specifies the time, in milliseconds, that the GroupCoordinator will delay the initial consumer rebalance.
# The rebalance will be further delayed by the value of group.initial.rebalance.delay.ms as new members join the group, up to a maximum of max.poll.interval.ms.
# The default value for this is 3 seconds.
# We override this to 0 here as it makes for a better out-of-the-box experience for development and testing.
# However, in production environments the default value of 3 seconds is more suitable as this will help to avoid unnecessary, and potentially expensive, rebalances during application startup.
group.initial.rebalance.delay.ms=0%
```

### broker . id

default = 0

어떤 값도 사용이 가능하다. 단, 하나의 카프카 클러스터 내에서는 고유한 값이어야한다. 브로커 호스트가 갖는 본질적인 값으로 설정하는것이 좋다. 예를들어 `kafka1.example.com`, `kafka2.example.com` 등과 같이 호스트 이름에 고유번호가 포함되어 있으면 이것을 broker .id 로 사용해도 좋다.

### port

default = 9092

카프카의 실행에 사용되는 TCP 포트를 나타낸다. 1024 보다 작은 값으로 설정하면 카프카가 root 권한으로 시작되어야한다.

### zookeeper.connect

default = localhost:2181

브로커의 메타데이터를 저장하기 위해 사용되는 Zookeeper의 URL을 나타낸다. **호스트이름:포트/경로** 형식으로 지정할 수 있다.

### log.dirs

default = /usr/local/var/lib/kafka-logs

Kafka는 모든 메세지를 로그 세그먼트 파일에 모아서 디스크에 저장된다. 그리고 이 파일은 log.dirs에 지정된 디렉토리에 저장된다. 이때 여러 경로를 쉼표로 구분하여 지정할 수 있다.

### num.recovery.threads.per.data.dir

default = 1

Kafka는 구성 가능한 스레드 풀을 사용해서 로그 세그먼트를 처리한다. 스레드 풀은 다음 경우에 사용된다.

1. 브로커가 정상적으로 시작될 때는 각 파티션의 로그 세그먼트 파일을 열기 위해 사용한다.
2. 장애 발생 이후 다시 시작될 때는 각 파티션의 로그 세그먼트를 검사하고 불필요한 부분을 삭제하기 위해 사용한다.
3. 종료될 때는 로그 세그먼트 파일을 정상적으로 닫기 위해 사용된다.

이 매개변수에 설정하는 스레드의 수는 log.dirs에 지정된 로그 디렉토리마다 다르게 적용된다. 예를 들어 log.dirs에 지정된 경로가 3개일 때 num.recovery.threads.per.data.dir 값이 8이면 스레드는 24개가된다.

### auto.create.topics.enable

default = true

다음의 경우에 브로커는 자동으로 토픽을 생성한다.

1. 프로듀서가 토픽에 메세지를 쓸 때
2. 컨슈머가 토픽의 메세지를 읽기 시작할 때
3. 클라이언트에서 토픽의 메타데이터를 요청할 때

### num.partition

default = 1

새로운 토픽이 몇 개의 파티션으로 생성되는지 나타내며 `auto.create.topics.enable=true` 일 때 사용된다. 토픽의 파티션 개수는 증가만 가능하고 감소 될 수는 없다.

### log.retention.ms

default = 168 ( 168 hours = 7days )

카프카가 얼마동안 메세지를 보존할 지 정하는 매개변수다. 보통 `log.retention.hours` 를 사용하며 이외에도 다른 두 개의 매개변수인 `log.retention.minutes` 와 `log.retention.ms` 를 사용할 수 있다.

만약 두 개 이상이 같이 지정되면 더 작은 시간 단위의 매개변수 값이 사용된다.

### log.retention.bytes

default = 1073741824

저장된 메세지들의 전체 크기를 기준으로 처리하는 방법이다. 이 값은 모든 파티션에 적용된다.

예를 들어, 하나의 토픽이 8개의 파티션으로 구성되어 있고 이 값이 8GB로 설정되면 해당 토픽에 보존되는 메세지들의 전체 크기는 최대 8GB가 된다.

### log.segment.bytes

default = 1073741824

앞에서 설명한 메세지 보존 설정은 개별적인 메세지가 아닌 로그 세그먼트 파일을 대상으로 처리된다. 메세지가 카프카 브로커에 생성될 때는 해당 파티션의 로그 세그먼트 파일 끝에 추가된다.

이때 `log.sement.bytes` 매개변수에 지정된 크기가 되면 해당 로그 세그먼트 파일이 닫히고 새로운 것이 생성된다.

### log.segment.ms

default = NULL

시간을 지정해서 로그 세그먼트 파일이 닫히는것을 제어 할 수 있다.

### message.max.bytes

default = NULL

Kafka 브로커는 쓰려는 메세지의 최대 크기를 제한 할 수 있다. 이 값보다 큰 메세지를 전송할려면 프로듀서에게는 ㅡㅂ로커가 에러를 보내고 메세지를 받지 않는다.