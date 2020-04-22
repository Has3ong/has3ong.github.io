---
title : Kafka Building Data Pipelines
tags :
- Connect
- Pipeline
- Apache
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

데이터 파이프라인은 서로 다른 여러 시스템 간의 데이터 이동 / 흐름을 말하며, 파이프라인을 효율적으로 구축하면 서로 다른 시스템을 어렵게 통합하지 않고 시스템 간의 데이터 전달과 통합을 효율적으로 할 수 있습니다.

Kafka 를 사용한 데이터 구축에는 2 가지 사례가 있습니다. 하나는 Kafka 가 두 개의 엔드포인트 중 하나가 되는 데이터 파이프라인 구축입니다. 다른 하나는 서로 다른 두 개의 시스템 중간에서 Kafka 를 중계 역할로 사용하는 파이프라인 구축입니다.

파이프라인에서 데이터를 생성하는 프로듀서와 소비하는 컨슈머를 효과적으로 분리함으로써 Kafka 는 여러 단계 간에 크고 신뢰성 있는 버퍼 역할을 합니다. 따라서 대부분의 데이터 파이프라인에 Kafka 를 적합하게 사용할 수 있습니다.

## Considerations When Building Data Pipelines 

데이터 파이프라인 구축으로 다수의 시스템을 통합하고자 한다면 소프트웨어 아키텍처를 설계할 때 아래와같이 고려해야할 사항이 있습니다.

### Timeliness 

Kafka 는 실시간 파이프라인부터 시간 단위의 배치 파이프라인까지 모든것을 지원하는 버퍼로 사용할 수 있습니다. 이때 프로듀서와 컨슈머 모두 배치 형태로 데이터를 읽고 쓸 수 있습니다.

데이터의 쓰기와 읽기가 분리되어 있기 때문이빈다.

### Reliability 

신뢰성을 높이기 위해서는 **단일 장애점(Single Point of Failure)** 을 피하고 모든 종류의 장애 발생 시에 신속하고 자동화된 복구를 할 수 있어야 합니다.

데이터 파이프라인은 중요한 데이터가 전달되는 경로를 제공합니다. 따라서 장애가 발생하면 전체 시스템에 큰 지장을 줄 수 있습니다. 또한, 신뢰성의 또 다른 중요한 고려 사항은 데이터 전달 보장입니다. 

즉, 시스템에 따라 다르지만 **최소 한 번(at-least-once)** 의 데이터 전달 요구사항을 가지는 시스템이 있을 수 있습니다. 반대로 **정확히 한 번(excatly-once)** 전달을 요구사항으로 가지는 시스템도 많습니다.

Kafka 는 이 *최소 한 번* 데이터 전달과 *정확히 한 번* 데이터 전달도 가능합니다.

### High and Varying Throughput 

데이터 파이프라인은 높은 처리량(Throughput) 을 갖도록 확장될 수 있어야 하며, 불시에 처리량이 증가하더라도 조정할 수 있어야 합니다.

Kafka 는 데이터를 쓰는 프로듀서와 읽는 컨슈머 간의 버퍼 역할을 하므로 컨슈머의 처리량을 프로듀서의 처리량과 연관시키지 않아도 됩니다. 프로듀서의 처리량이 컨슈머의 처리량을 초과하면, 프로듀서가 쓴 데이터는 컨슈머가 읽을 수 있을때까지 Kafka 에 보존되므로 복잡한 메커니즘이 필요 없습니다. 그리고 Kafka 는 컨슈머나 프로듀서를 별도로 확장할 수 있습니다. 따라서 파이프라인의 어느 쪽이든 동적으로 확장하기 쉬우며, 요구사항의 변화에 독립적으로 맞출 수 있습니다.

Kafka 는 높은 처리량의 분산 시스템입니다. 고성능의 하드웨어 사양이 아닌 평범한 클러스터에서도 많은 데이터를 처리할 수 있는 성능을 갖기 때문입니다. 또한, Kafka 커넥트 API 를 사용하면 확장은 물론 다중 스레드를 사용한 병행 처리도 가능합니다.

Kafka 는 여러 가지 데이터 압축 형식을 지원하므로 처리량이 증가할 때 사용자와 관리자가 네트워크와 스토리지 자원의 사용을 제어할 수 있게 해줍니다.

### Data Formats

데이터 파이프라인에서 가장 중요하게 고려할 것 중 하나가 서로 다른 데이터 형식을 조회하는 것입니다.

Kafka 와 커넥트 API 는 데이터 형식에 구애받지 않습니다. 프로듀서와 컨슈머는 다양한 직렬처리기를 사용하여 원하는 어떤 형식의 데이터도 Kafka 에 읽고 쓸 수 있습니다. Kafka 커넥트는 데이터 형식과 스키마를 포함하는 메모리 객체들을 가지며, 변환기를 사용해 어떤 형식으로도 데이터를 저장할 수 있게 해줍니다. 따라서 Kafka 에 사용하는 데이터 형식은 제약을 받지 않습니다.

Kafka 로부터 외부 시스템에 데이터를 쓸 때는 **싱크 커넥터(Sink Connector)** 가 데이터 형식에 맞게 처리하는 책임을 가지며, 일부 커넥터에서는 형식을 선택할 수 있습니다.

하지만, 범용적인 데이터 파이프라인을 제공하는 통합프레임워크에서는 다양한 소스와 싱크의 서로 다른 동작에 따른 차이점도 처리할 수 있어야합니다.

예를 들어, 데이터 소스인 Syslog 는 파이프라인에 데이터를 쓰는 반면, RDB 는 데이터를 읽을 수 있어야 합니다. 또 다른 예로, HDFS 는 새로운 데이터를 추가할 수 있지만, 이외의 대다수 시스템은 새로운 데이터추가와 기존 데이터 변경 모두 가능합니다.

### Transformations 

**변환(Transformation)** 은 데이터 파이프라인 구축의 다른 고려사항에 비해 추가로 알아야 할 사항이 있습니다. 파이프 라인 구축에는 ETL 과 ELT 두 가지 유형이 있습니다.

ETL 은 **추출-변환-적재(Extract-Transform-Load)** 를 의미하며, 서로 다른 소스 시스템에서 데이터를 가져와 적절한 형식이나 구조로 변환한 후, 다른 시스템으로 저장하는 것을 말합니다. 이 경우 데이터 파이프라인을 거쳐가는 데이터를 파이프라인에 변환할 책임이 있습니다. 파이프 라인에서 데이터를 계속 보존할 필요 없이 변환한 후 전달하면 되므로 시간과 스토리지를 절약할 수 있습니다.

ETL 의 문제점은 소스 데이터의 형식이나 구조가 파이프라인에서 변환되어 전달하므로 파이프라인에 연결된 대상 시스템의 더 아래 단에서 데이터를 처리하는 사용자나 어플리케이션의 유연성을 떨어뜨립니다.

ELT 는 **추출-적재-변환(Extract-Load-Transform)** 을 의미하며, 대상 시스템에 전달하는 데이터가 가능한 한 소스 데이터와 유사하게 되도록 하기 위해 데이터 파이프라인에서는 최소한의 변환만 수행합니다. 따라서 대상 시스템에는 raw 데이터를 받게되고 모든 변환도 수행합니다. 이 경우 대상 시스템의 사용자에게 최대한의 유용성을 제공할 수 있습니다.

하지만, 변환에 필요한 대상 시스템의 CPU 와 스토리지가 부담되는 단점이 있습니다. 예를 들어 대용량의 데이터를 축적하고 조회나 분석할 수 있는 데이터 웨어하우스의 경우가 특히 그렇습니다.

### Security 

파이프라인의 관점에서는 다음 사항이 중요합니다.

* Can we make sure the data going through the pipe is encrypted? This is mainly a concern for data pipelines that cross datacenter boundaries.
* Who is allowed to make modifications to the pipelines?
* If the data pipeline needs to read or write from access-controlled locations, can it authenticate properly?

데이터 소스로부터 Kafka 로 데이터를 전송할 때와 Kafka 의 데이터를 싱크로 전송할 때 Kafka 는 암호화된 데이터의 네트워크 전송을 허용하며 **SASL(Simple Authentication and Security Layer)** 인증을 지원합니다. 따라서 민감한 정보가 Kafka 토픽에 포함된다면, 인증되지 않은 누군가에 의해 보안이 미비한 시스템으로 전달될 수 없습니다.

### Failure Handling 

Kafka 는 모든 데이터를 긴 시간 동안 저장하므로 필요하다면 에러가 발생한 해당 시점에 맞게 이전으로 돌아가서 에러를 복구할 수 있습니다.

### Coupling and Agility 

데이터 파이프라인의 가장 중요한 목표 중 하나는 데이터를 제공하는 소스와 데이터를 받아 사용하는 대상을 분리하는 것입니다.

#### Ad-hoc pipelines

연결을 원하는 어플리케이션을 사용해 커스텀 파이프라인을 구축하는 조직이 있습니다. Logstash 를 사용해 로그 데이터를 ElasticSearch 에 넣거나 Flume 의 로그 데이터를 HDFS 에 넣는 경우입니다.

위 경우 데이터 파이프라인의 역할을 수행하는 커스텀 어플리케이션들이 특정 엔드포인와 강하게 결합하고, 설치와 유지보수 및 모니터링에 큰 노력이 요구됩니다. 또한 새로운 시스템이 생길 때마다 파이프라인을 추가로 구축해야하며, 새로운 테크놀로지의 적응에 따른 비용이 증가합니다.

#### Loss of metadata

만일 데이터 파이프라인이 스키마 메타데이터를 보존하지 않고 스키마의 진화를 허용하지 안흔다면, 소스 시스템에서 데이터를 생성하는 소프트웨어와 대상 시스템에서 그 데이터를 사용하는 소프트웨어를 강하게 결합합니다.

그리고 스키마 정보가 없으므로 두 소프트웨어를 모두 데이터를 분석하고 해석하는 방법에 관한 정보를 가지고 있어야 합니다. 예를 들어, 스키마 정보를 보존하고 진화가 되지 않는데 오라클 DB 로 부터 HDFS 로 데이터가 이동되고 새로운 필드를 추가하면, HDFS 로부터 데이터를 읽는 모든 어플리케이션이 중단되거나 개발자가 어플리케이션을 동시에 업그레이드 해야합니다.

위 같은 경우 파이프라인에서 스키마 진화를 지원한다면 시스템의 중단을 우려하지 않고 어플리케이션을 변경할 수 있습니다.

#### Extreme processing

파이프라인에서 너무 많은 처리를 하면 후속으로 개발되는 시스템들이 다음 사항과 결속됩니다. 예를 들어, 어떤 필드를 보존할지, 데이터 집계를 어떻게 할지 등이며, 이것들은 파이프 라인을 구축할 때 결정되어야 합니다.

또한 이후의 어플리케이션 요구사항이 변경될 때마다 파이프라인도 변경되어야 하므로, 신속성과 효율성 및 안정성이 떨어집니다. 따라서 가능한 원시 데이터의 형태로 많이 보존하고, 후속 어플리케이션에서 스스로 결정하여 데이터 처리와 집계를 하는것이 더 빠르고 좋습니다.

## When to Use Kafka Connect Versus Producer and Consumer 

Kafka 클라이언트는 Kafka 프로듀서와 Kafka 컨슈머를 포함합니다.

Kafka 클라이언트 어플리케이션을 연결하기 원하는 외부 어플리케이션 코드를 변경할 수 있거나, Kafka 에 데이터를 쓰거나 읽기를 원할 때 Kafka 클라이언트를 사용하면 됩니다.

코드를 작성하지 않고 변경도 할 수 없는 모든 외부 시스템(예를 들어, HDFS, S3) 에 Kafka 를 연결할 때는 Kafka 커넥터를 사용합니다. 외부 시스템의 데이터를 읽어서 Kafka 에 쓰거나 Kafka 데이터를 읽어서 외부 시스템에 쓰는 데 사용하는 컴포넌트 클래스가 커넥터입니다.

만약 Kafka 를 특정 데이터스토어에 연결해야 하는데 사용할 수 있는 커넥터가 없다면, Kafka 클라이언트나 커넥트 API 중 하나를 사용해서 어플리케이션을 작성할 수 있습니다.

## Kafka Connect 

Kafka 커넥트는 아파치 Kafka 의 일부로 포함되어 있으며, Kafka 와 다른 데이터스토어 간에 데이터를 이동하기 위해 확장성과 신뢰성 있는 방법을 제공합니다.

Kafka 커넥트는 여러 개의 **작업 프로세스(Worker Process)** 들로 실행됩니다. 커넥터 플러그인을 작업 프로세스에 설치한 후 REST API 를 사용해서 특정 구성으로 실행하는 커넥터를 구성하고 관리합니다. 커넥터는 대용량 데이터를 병행처리로 이동시키고, 작업 프로세스 노드의 사용 가능한 리소스를 더 효율적으로 사용하기 위해 **태스크(Task)** 들을 추가로 시작시킵니다.

커넥터에는 소스 커넥터와 싱크 커넥터 두 종류가 있습니다. 소스 커넥터의 태스크들은 소스 시스템으로부터 데이터를 읽어서 커넥트 데이터 객체로 작업 프로세스에 제공합니다. 반면에, 싱크 커넥터의 태스크들은 작업 프로세스로부터 커넥트 데이터 객체를 받아서 대상 시스템에 쓰는 책임을 가집니다. 이때 컨버터를 사용하여 다양한 형식의 데이터 객체들을 Kafka 에 저장합니다.

JSON 형식은 Kafka 의 일부로 지원되며 컨플루언트 스키마 레지스트리는 Avro 컨버터를 제공합니다.

### Running Connect 

여러가지 커넥트를 실행할 때는 하나 이상의 별도 서버에서 커넥트 작업 프로세스를 실행해야합니다. 이때 모든 서버에 아파치 Kafka 를 설치한 후 일부 서버에서는 브로커를 시작시키고, 나머지 다른 서버에서는 커넥트 작업 프로세스를 실행시킨다.

커넥트 작업 프로세스는 브로커와 매우 유사하게 시작합니다. 아래와 같이 속성 파일을 전달하여 시작 스크립트를 실행하면 됩니다.

```shell
$ bin/connect-distributed.sh config/connect-distributed.properties
```

속성 파일에 설정하는 커넥트 작업 프로세스의 핵심 매개변수는 다음과 같습니다.

* `bootstrap.servers` 
  * 커넥트와 함께 동작하는 Kafka 브로커의 리스트입니다. 여기서 Kafka 클러스터의 모든 브로커를 지정할 필요가 없지만 최소 3 개는 지정할 것을 권장합니다. 이 속성에 지정된 브로커에 데이터를 전달하는 일은 커넥터가 수행합니다.
* `group.id`
  * 같은 그룹 ID 를 가지는 모든 커넥트 작업 프로세스는 같은 커넥트 클러스터의 일부가됩니다.
* `key.converter` / `value.converter`
  * 커넥트는 Kafka 에 저장된 여러가지 형식의 데이터를 처리할 수 있습니다. 이 두 가지 속성에는 Kafka 에 저장되는 메세지의 Key 와 Value 부분에 대한 컨버터를 설정합니다.
  * 기본값은 Kafka 에 포함된 JSONConverter 이며, 이 컨버터는 JSON 형식을 사용합니다.

일부 컨버터는 컨버터 특유의 구성 매개변수를 포함합니다. 예를 들어, JSON 메세지는 Key 컨버터와 Value 컨버터에 대해 스키마의 포함 여부를 설정할 수 있습니다.

Key 컨버터의 경우 `key.converter.schemas.enable=true` 또는 `false` 로 설정합니다. Value 컨버터의 경우 `value.converter.schemas.enable=true` 또는 `false` 를 설정합니다.

Avro 메세지도 스키마를 포함합니다. 그러나 이때는 `key.converter.schema.registry.url` 과 `value.converter.schema.registry.url` 을 사용해서 Key 와 Value 의 스키마 레지스트리 위치를 설정해야 합니다.

일반적으로 커넥터는 Kafka 커넥터의 REST API 를 통해 구성 및 관리됩니다. 이때 REST API 에서 사용할 REST 호스트와 포트를 `rest.host.name` 과 `rest.port` 매개변수에 설정합니다. `rest.host.name` 의 기본값은 없으며, `rest.port` 의 기본값은 8083 입니다.

예를 들어 다음과 같이 REST API 를 사용할 수 있습니다.

```shell
$ curl http://localhost:8083/
{"version":"0.10.1.0-SNAPSHOT","commit":"561f45d747cd2a8c"}
```

또한 다음과 같이 어떤 커넥터 플러그인을 사용할 수 있는지도 확인할 수 있습니다.

```shell
$ curl http://localhost:8083/connector-plugins
[{"class":"org.apache.kafka.connect.file.FileStreamSourceConnector"},
{"class":"org.apache.kafka.connect.file.FileStreamSinkConnector"}]
```

위에선 Kafka 를 기본 설치할 때 사용할 수 있는 두 개의 커넥터 플러그인을 보여줍니다. `FileStreamSourceConnector` 는 파일 소스 커넥터고, `FileStreamSinkConnector` 는 파일 싱크 커넥터입니다.

### Connector Example: File Source and File Sink 

Kafka 의 일부로 포함된 파일 커넥터와 JSON 컨버터를 사용하는 예를 알아보겠습니다. 먼저 주키퍼와 Kafka 를 실행해야합니다.

분산 모드의 커넥트 작업 프로세스를 시작시키겠습니다. 실제 업무 환경에서는 높은 가용성을 제공하기 위해 최소 2 ~ 3개 작업 프로세스를 실행하지만 여기선 하나만 실행하겠습니다.

```shell
$ bin/connect-distributed.sh config/connect-distributed.properties &
```

다음은 Kafka 구성 파일을 읽어 토픽으로 쓰도록 파일 소스 커넥터를 생성 및 구성하고 시작하겠습니다.

```shell
echo '{"name":"load-kafka-config", \
"config":{"connector.class":"FileStreamSource", \
"file":"config/server.properties", \
"topic":"kafka-config-topic"}}' \
| curl -X POST -d @- http://localhost:8083/connectors \
--header "contentType:application/json"

{
  "name":"load-kafka-config",
  "config":{
    "connector.class":"FileStreamSource",
    "file":"config/server.properties",
    "topic":"kafka-configtopic",
    "name":"load-kafka-config"
  },
  "tasks":[]
}
```

위에선 커넥터를 생성하기 위해 JSON 형식을 사용했습니다. 이때 커넥터 이름이 `load-kafka-config` 를 지정하였으며, 커넥터 클래스, 읽을 파일 이름, 파일 데이터를 쓸 토픽 이름을 커넥투 구성 Map 인 `config` 에 포함했습니다.

앞의 `echo` 명령이 끝나면 Kafka 구성 파일의 `kafka-config-topic` 이라는 토픽에 저장되었을 것입니다. 다음과 같이 Kafka 콘솔 컨슈머를 사용해 제대로 저장되었는지 확인해보겠습니다.

```shell
$ bin/kafka-console-consumer.sh --new \
--bootstrap-server=localhost:9092 \
--topic kafka-config-topic --from-beginning \
```

출력 결과는 아래와 같습니다.

```shell
{"schema":{"type":"string","optional":false},"payload":"# Licensed to the
Apache Software Foundation (ASF) under one or more"}
{"schema":{"type":"string","optional":false},"payload":"############################# Server Basics
#############################"}
{"schema":{"type":"string","optional":false},"payload":""}
{"schema":{"type":"string","optional":false},"payload":"# The id of the broker.
This must be set to a unique integer for each broker."}
{"schema":{"type":"string","optional":false},"payload":"broker.id=0"}
{"schema":{"type":"string","optional":false},"payload":""}
```

Kafka 구성 파일인 *config/server.properties* 의 내용 그대로이며, JSON 형식으로 변환하고 커넥터에 의해 `kafka-config-topic` 에 저장된 것입니다. 기본적으로 JSON 컨버터는 각 레코드에 스키마를 포함합니다. 여기서는 스키마가 매우 간단하여 String 타입인 `palyload` 라는 이름의 열이 하나만 있습니다. 스키마 다음에는 파일의 한 줄을 하나의 레코드로 포함합니다.

아래는 파일 싱크 커넥터를 사용해 토픽의 내용을 파일로 쓴겁니다. 결과로 생성되는 파일은 Kafka 구성 파일인 *config/server.properties* 의 내용과 완전히 같을 것입니다. JSON 컨버터가 각 JSON 레코드를 일반 텍스트의 한 줄로 변환하기 때문입니다. Kafka 토픽의 데이터를 파일로 쓰도록 다음과 같이 파일 싱크 커넥터를 생성 및 구성하고 시작시킵니다.

```shell
echo '{"name":"dump-kafka-config", \
"config": {"connector.class":"FileStreamSink",\
"file":"copy-of-serverproperties",\
"topics":"kafka-config-topic"}}' \
| curl -X POST -d @- http://localhost:8083/connectors
--header "content-Type:application/json"

{
  "name":"dump-kafka-config",
  "config": {
    "connector.class":"FileStreamSink",
    "file":"copy-of-serverproperties",
    "topics":"kafka-config-topic",
    "name":"dump-kafka-config"
  },
  "tasks":[]
}
```

이전 소스와 비교해보겠습니다. 우선 커넥트 클래스를 `FileStreamSource` 가 아닌 `FileStreamSink` 로 사용합니다. 파일 속성은 포함되지만 여기서는 데이터를 쓰는 대상 파일을 나타냅니다.

또한 토픽의 경우에 커넥터 구성 Map 의 Key 로 단수형의 `topic` 대신 복수형의 `topics` 를 지정합니다. 또한 싱크 커넥터는 Kafka 토픽의 데이터를 읽어서 싱크 포인트로 쓰는 것이므로 여러 토픽의 데이터를 읽을 수 있기 때문입니다. 반면에, 소스 커넥터는 Kafka 토픽에 데이터를 쓰는것이므로 하나의 토픽만 지정할 수 있습니다.

커넥터를 삭제할 때는 다음과 같이 하면 됩니다.

```shell
$ curl -X DELETE http://localhost:8083/connectors/dump-kafka-config
```

커넥터가 삭제된 후 커넥트 작업 프로세스 로그를 보면 자른 모든 커넥터가 자신들의 태스크를 다시 시작하는것을 알 수 있습니다. 작업 프로세스들 간에 남은 태스크들의 작업량을 균등하게 재조정하기 위해서입니다.

### Connector Example: MySQL to Elasticsearch 

Mac OSX 에서 MySQL 테이블의 데이터를 읽어서 Kafka 토픽의 쓰고, 그 데이터를 Elasticsearch 에 인덱스에 써보겠습니다.

먼저 설치를 하겠습니다.

```shell
$ brew install mysql
$ brew install elasticsearch
```

다음은 커넥터가 있는지 확인해야 합니다. Confluent OpenSource 가 실행되어 있다면, 해당 커넥터들이 플랫폼의 일부로 이미 생성되어 있을 것입니다. 그렇지 않다면 다음과 같이 깃헙에서 다운로드하여 생성할 수 있습니다.

1. Go to https://github.com/confluentinc/kafka-connect-elasticsearch
2. Clone the repository
3. Run mvn install to build the project
4. Repeat with the JDBC connector

다음은 각 커넥터가 생성된 `target` 디렉토리에 `jar` 파일들을 Kafka 커넥트 클래스가 있는 디렉터리로 복사합니다.

```shell
$ mkdir libs
$ cp ../kafka-connect-jdbc/target/kafka-connect-jdbc-3.1.0-SNAPSHOT.jar libs/
$ cp ../kafka-connect-elasticsearch/target/kafka-connectelasticsearch-3.2.0-
SNAPSHOT-package/share/java/kafka-connect-elasticsearch/* libs/
```

만약 Kafka 커넥트 작업 프로세스들이 아직 실행중이 아니면 다음과 같이 시작시키면 됩니다.

```shell
$ bin/connect-distributed.sh config/connect-distributed.properties &
```

그리고 커넥터 플러그인들의 내역을 확인합니다.

```shell
$ curl http://localhost:8083/connector-plugins
[{"class":"org.apache.kafka.connect.file.FileStreamSourceConnector"},
{"class":"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector"},
{"class":"org.apache.kafka.connect.file.FileStreamSinkConnector"},
{"class":"io.confluent.connect.jdbc.JdbcSourceConnector"}]
```

이제 커넥터 플러그인들을 갖게 되었습니다. MySQL 에 JDBC 소스 커넥터를 사용하려면 MySQL 드라이버가 필요합니다. 오라클 웹 사이트에서 MySQL 의 JDBC 드라이버를 다운로드 하고 압출을 풀어 커넥터를 복사했던 *libs/* 디렉토리에 *mysql-connector-java-5.1.40-bin.jar* 을 복사하면됩니다.

다음은 JDBC 커넥터를 사용해서 Kafka 로 쓸 데이터를 저장할 MySQL 의 테이블을 생성하고 데이터도 추가합니다.

```sql
$ mysql.server restart

mysql> create database test;
Query OK, 1 row affected (0.00 sec)

mysql> use test;
Database changed

mysql> create table login (username varchar(30), login_time datetime);
Query OK, 0 rows affected (0.02 sec)

mysql> insert into login values ('gwenshap', now());
Query OK, 1 row affected (0.01 sec)

mysql> insert into login values ('tpalino', now());
Query OK, 1 row affected (0.00 sec)

mysql> commit;
Query OK, 0 rows affected (0.01 sec)
```

여기서는 데이터베이스와 테이블을 생성하고 두 개의 데이터를 추가하였습니다.

JDBC 소스 커넥터를 구성하는 것이 다음으로 할 일입니다. 다음과 같이 REST API 를 사용해서 알 수 있습니다.

```shell
$ curl -X PUT -d "{}" localhost:8083/connector-plugins/JdbcSourceConnector/ \
config/validate --header "content-Type:application/json" | python -m json.tool

{
  "configs": [
    {
      "definition": {
        "default_value": "",
        "dependents": [],
        "display_name": "Timestamp Column Name",
        "documentation": "The name of the timestamp column to use to detect new or modified rows. This column may not be nullable.",
        "group": "Mode",
        "importance": "MEDIUM",
        "name": "timestamp.column.name",
        "order": 3,
        "required": false,
        "type": "STRING",
        "width": "MEDIUM"
      },
 <more stuff>
```

커넥터의 구성 옵션을 확인하기 위해 REST API 를 요청했습니다. 그리고 모든 사용 가능한 구성 옵션들을 JSON 형식의 응답으로 받습니다. 이때 JSON 형식의 결과를 알기 쉽도록 Python 으로 출력했습니다.

구성 옵션 정보를 생가갛면서, 아래와 같이 JDBC 소스 커넥터를 생성하고 시작하겠습니다.

```shell
echo '{
  "name":"mysql-login-connector",
  "config":{
    "connector.class":"JdbcSourceConnector",
    "connection.url":"jdbc:mysql://127.0.0.1:3306/test?user=root",
    "mode":"timestamp",
    "table.whitelist":"login",
    "validate.non.null":false,
    "timestamp.column.name":"login_time",
    "topic.prefix":"mysql."
  }
}' | curl -X POST -d @- http://localhost:8083/connectors --header \
"content-Type:application/json"


{
  "name":"mysql-login-connector",
  "config":{
    "connector.class":"JdbcSourceConnector",
    "connection.url":"jdbc:mysql://127.0.0.1:3306/test?user=root",
    "mode":"timestamp",
    "table.whitelist":"login",
    "validate.non.null":"false",
    "timestamp.column.name":"login_time",
    "topic.prefix":"mysql.",
    "name":"mysqllogin-connector"
  },
  "tasks":[]
}
```

앞의 `echo` 명령 실행이 끝나면 MySQL 의 데이터가 `mysql.login` 이라는 토픽에 저장되었을 것입니다. 다음과 같이 Kafka 콘솔 컨슈머를 사용해 이 토픽의 데이터를 읽고 확인해보겠습니다.

```shell
$ bin/kafka-console-consumer.sh --new \
--bootstrap-server=localhost:9092 -- \
topic mysql.login --from-beginning

<more stuff>

{
  "schema":{
    "type":"struct",
    "fields": [{
      "type":"string",
      "optional":true,
      "field":"username"
    },
    {
      "type":"int64",
      "optional":true,
      "name":"org.apache.kafka.connect.data.Timestamp",
      "version":1,
      "field":"login_time"
    }],
    "optional":false,
    "name":"login"
  },
  "payload":{
    "username":"gwenshap",
    "login_time":1476423962000
    }
}

{
  "schema":{
    "type":"struct",
    "fields":[{
      "type":"string",
      "optional":true,
      "field":"username"
    },
    {
      "type":"int64",
      "optional":true,
      "name":"org.apache.kafka.connect.data.Timestamp",
      "version":1,
      "field":"login_time"
    }],
    "optional":false,
    "name":"login"
    },
  "payload":{
    "username":"tpalino",
    "login_time":1476423981000
  }
}
```

만약 토픽이 없다는 에러 메세지를 받거나 데이터가 보이지 않으면, 커넥트 작업 프로레스의 에러 로그를 확인합니다. 예를 들면 다음과 같습니다.

```shell
[2016-10-16 19:39:40,482] ERROR Error while starting connector mysql-login-connector (org.apache.kafka.connect.runtime.WorkerConnector:108)
org.apache.kafka.connect.errors.ConnectException: java.sql.SQLException: Access denied for user 'root;'@'localhost' (using password: NO)
       	at io.confluent.connect.jdbc.JdbcSourceConnector.start(JdbcSourceConnector.java:78)
```

커넥터를 시작할 때 에러가 생긴것을 볼 수 있습니다. 데이터베이스에 JDBC 경로가 없거나 데이터베이스 테이블을 읽기 위한 권한이 없어서 발생할 수 있습니다.

커넥터가 실행 중일 때 `login` 테이블에 새로운 행을 추가하면 *mysql.login* 토픽에도 바로 반영이 됩니다.

엘라스틱서치 싱크 커넥터를 이용하여 *mysql.login* 토픽의 데이터를 엘라스틱 서치에 써보겠습니다.

엘라스틱서치 서버를 시작시키고 로컬 포트로 접속하여 제대로 동작하는지 확인해보겠습니다.

```shell
$ elasticsearch &
$ curl http://localhost:9200/
{
  "name" : "Hammerhead",
  "cluster_name" : "elasticsearch_gwen",
  "cluster_uuid" : "42D5GrxOQFebf83DYgNl-g",
  "version" : {
    "number" : "2.4.1",
    "build_hash" : "c67dc32e24162035d18d6fe1e952c4cbcbe79d16",
    "build_timestamp" : "2016-09-27T18:57:55Z",
    "build_snapshot" : false,
    "lucene_version" : "5.5.2"
  },
  "tagline" : "You Know, for Search"
}
```

커넥터를 생성 및 구성하고 시작시키겠습니다.


```shell
echo '{"name":"elastic-login-connector", "config":{"connector.class":"ElasticsearchSinkConnector", \
"connection.url":"http://localhost:9200","type.name":"mysql-data","topics":"mysql.login","key.ignore":true}}' \
| curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"

{
  "name":"elastic-login-connector",
  "config":{
    "connector.class":"ElasticsearchSinkConnector",
    "connection.url":"http://localhost:9200",
    "type.name":"mysql-data",
    "topics":"mysql.login",
    "key.ignore":"true",
    "name":"elastic-login-connector"
  },"tasks":[{
    "connector":"elastic-login-connector",
    "task":0
  }]
}
```

위에서 `connection.url` 은 방금 전에 실행시킨 로컬 엘라스틱서치 서버의 URL 입니다. Kafka 의 각 토픽은 별개의 엘라스틱서치 인덱스가 되며, 인덱스는 토픽과 같은 이름으로 생성됩니다.

여기서는 *mysql.login* 토픽 데이터만 엘라스틱서치에 씁니다. 인덱스에 쓰는 토픽 데이터의 타입은 `type.name` 에 지정하며, 여기서는 `mysql-data` 로 설정하였습니다. 그리고 MySQL 데이터베이스에 테이블을 정의할 때 기본미를 지정하지 않았으므로 *mysql.login* 토픽의 데이터는 null 키를 갖습니다.

따라서 `key.ignore` 를 true 로 설정했습니다. 이 경우 엘라스틱서치 커넥터에서는 토픽 이름과 파티션 ID 및 오프셋이 각 데이터의 키로 사용됩니다.

이제 *mysql.login* 토픽의 데이터를 가지는 엘라스틱서치 인덱스가 생성되었는지 다음과 같이 확인해보겠습니다.

```shell
gwen$ curl 'localhost:9200/_cat/indices?v'
health status index       pri rep docs.count docs.deleted store.size pri.store.size
yellow open   mysql.login   5   1          3            0     10.7kb         10.7kb
```

만약 인덱스가 생성되지 않았다면 커넥트 작업 프로세스 로그의 에러를 살펴봅니다. 구성 옵션이나 라이브러리 지정이 누락되어 에러가 생기는 경우가 많습니다. 성공되었다면 다음과 같이 데이터의 인덱스를 검색할 수 있습니다.

```shell
gwen$ curl -s -X "GET" "http://localhost:9200/mysql.login/_search?pretty=true"
{
  "took" : 29,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 3,
    "max_score" : 1.0,
    "hits" : [ {
      "_index" : "mysql.login",
      "_type" : "mysql-data",
      "_id" : "mysql.login+0+1",
      "_score" : 1.0,
      "_source" : {
        "username" : "tpalino",
        "login_time" : 1476423981000
      }
    }, {
      "_index" : "mysql.login",
      "_type" : "mysql-data",
      "_id" : "mysql.login+0+2",
      "_score" : 1.0,
      "_source" : {
        "username" : "nnarkede",
        "login_time" : 1476672246000
      }
    }, {
      "_index" : "mysql.login",
      "_type" : "mysql-data",
      "_id" : "mysql.login+0+0",
      "_score" : 1.0,
      "_source" : {
        "username" : "gwenshap",
        "login_time" : 1476423962000
      }
    } ]
  }
}
```

만일 MySQL 테이블에 새로운 레코드를 추가하면 Kafka 의 *mysql.login* 토픽 및 이와 연관된 엘라스틱 인덱스 모두에 자동으로 추가됩니다.

이제 JDBC 소스 커넥터와 엘라스틱 싱크 커넥터를 생성하고 사용하는 방법을 알았습니다. 소스와 싱크 커넥터는 용도에 맞게 짝을 이루어 생성하고 구성한 후 사용할 수 있습니다.

### A Deeper Look at Connect 

커넥트가 어떻게 동작하는지 이해하려면 세 가지 기본적인 개념과 그 개념들이 어떻게 상호작용하는지 알아야합니다. 앞에서 설명했듯이 커넥터를 사용하기 위해서는 작업 프로세스들과 커넥터를 실행시켜야합니다.

위에서 설명하지 않았지만 컨버터는 MySQL 데이터베이스 테이블의 각 행을 JSON 레코드로 변환하는 컴포넌트이며, 커넥터가 Kafka 에 쓰는것이 JSON 레코드입니다. 지금부터는 커넥터의 각 구성 요소와 상호 작용에 관해 알아보겠습니다.

#### CONNECTORS AND TASKS

커넥터 플러그인에서는 커넥터 API 를 구현하며, 커넥터와 태스크를 포함합니다.

* Connector
  * 커넥터에서 얼마나 많은 태스크가 실행되어야 하는지 결정한다.
  * 데이터 복사 작업을 각 태스크에 어떻게 분ㄷ마할지 결정한다.
  * 작업 프로세스로부터 구성 정보를 얻는다.

예를 들어 JDBC 소스 커넥터는 데이터베이스에 연결하고 복사할 기존 테이블들을 찾은 후 그 결과에 기반하여 몇 개의 태스크가 필요한지 결정합니다. 이때 `tasks.max` 구성 옵션의 하한 값과 테이블 개수를 선택합니다. 그리고 몇 개의 태스크를 실행할지 결정하면 각 태스크의 구성 내역을 생성하며, 커넥터 구성과 각 태스크에서 복사하기 위해 할당된 테이블 리스트를 같이 사용합니다.

다음에 작업 프로세스들이 태스크들을 시작시키며, 이때 각 태스크가 자신에 할당된 테이블을 복사할 수 있도록 고유한 구성을 전달합니다. REST API 를 사용하여 커넥터를 시작시킬 때는 어떤 노드에서도 시작시킬 수 있으며, 이후에 시작시키는 태스크들도 같습니다.

* Task 
  * Kafka 의 데이터를 실제로 입출력하는 책임을 가진다.
  * 모든 태스크는 관련 작업 프로세스로부터 컨텍스트를 받아 초기화한다.

태스크는 Kafka 의 데이터를 실제로 입출력하는 책임을 갖습니다. 모든 태스크는 관련 작업 프로세스로부터 컨텍스트를 받아 초기화됩니다. 소스 컨텍스트는 하나의 객체를 포함하며, 이 객체는 소스 태스크가 소스 레코드의 오프셋을 저장할 수 있게 해줍니다.

싱크 커넥터의 컨텍스트는 메서드들을 포함하며, 이 메소드들은 Kafka 로부터 받은 레코드들을 커넥터가 제어할 수 있게 해줍니다. 싱크 커넥터의 컨텍스트는 정확히 한 번 데이터 전달을 위해 오프셋 커밋의 재시도와 저장 등의 작업을 처리하는데 사용합니다.

초기화된 태스크들은 Properties 객체를 전달받아 시작됩니다. 이 객체는 커넥터가 태스크를 위해 생성한 구성 정보를 갖습니다. 그 다음 시작된 소스 태스크는 외부 시스템의 데이터를 읽어서 레코드들의 리스트를 반환합니다. 이것이 작업 프로세스가 Kafka 브로커에게 전송할 데이터입니다.

반대로, 시작된 싱크 태스크는 작업 프로세세를 통해 Kafka 의 레코드들을 받아서 외부 시스템에 쓰는 작업을 수행합니다.

#### WORKERS

Kafka 커넥트의 작업 프로세스는 커넥터와 태스크를 실행하는 컨테이너 프로세스이며, 커넥터와 커넥터의 구성을 정의하는 HTTP 요청을 처리하는 책임을 가집니다. 커넥터 구성을 저장하고, 커넥터와 태스크를 시작시킵니다. 만약 특정 작업 프로세스가 중단되면 커넥트 클러스터의 다른 작업 프로세스들이 그 사실을 알게되며, 중단된 작업 프로세스에서 실행되던 커넥터와 태스크들이 나머지 작업 프로세스들에게 재할당됩니다.

만약 새로운 작업 프로세스가 커넥트 클러스터에 합류하면 다른 작업 프로세스들이 그 사실을 알게되며, 모든 작업 프로세스의 작업량이 균등하게 조정되도록 새로 합류한 작업 프로세스에게 커넥터와 태스크가 할당됩니다.

또한, 작업 프로세스들은 소스와 싱크 커넥터 모두 오프셋을 자동으로 커밋하고 에러가 생길 때 재시도를 처리하는 처리하는 책임을 가집니다.

커넥터와 태스크는 데이터 통합의 이동되는 데이터 부분만을 처리합니다. 반면 작업 프로세스는 REST API, 구성관리, 신뢰성, HA, 확정성, 로드밸런싱 등의 모든 작업을 처리하는 책임을 가집니다.

#### CONVERTERS AND CONNECT’S DATA MODEL

커넥트 API 에 관해 마지막으로 알아볼 것은 커넥트 데이터 모델과 컨버터입니다. Kafka 의 커넥트 API 에는 데이터 객체와 기 객체의 구조를 나타내는 스키마 모두를 가지는 데이터 API 가 포함되어 있습니다.

JDBC 소스 커넥터는 데이터베이스에서 반환된 칼럼의 데이터 타입을 기반으로 한 커넥트 스키마 객체를 구성합니다. 그 다음 스키마를 사용하여 데이터베이스 레코드의 모든 필드를 포함하는 구조체를 구성하며, 각 칼럼에 대해 이름과 갑승ㄹ 저장합니다. 모든 소스 커넥터가 이와 유사한 일을 수행합니다.

즉, 소스 시스템으로부터 데이터를 읽어서 한 쌍의 스키마와 값을 생성합니다. 싱크 커넥터는 이와 반대의 일을 수행합니다. 스키마와 값을 읽은 후 해당 스키마를 사용해 값은 분석한 뒤 시스템에 씁니다.

데이터 API 를 기반으로 데이터 객체를 생성하는 방법은 소스 커넥터가 알고 있습니다. 그러나 이 객체를 Kafka 에 저장하는 방법을 커넥트 작업 프로세스가 알아야 합니다. 컨버터가 개입되는 곳이 바로 여깁니다. 컨버터는 작업 프로세스를 구성할 때 선택하며, Kafka 에 데이터를 저장하기 위해 사용합니다. 커넥터가 작업 프로세스에 데이터 API 레코드를 반환하면, 작업 프로세스는 사전 구성된 컨버터를 사용해 Avro, JSON, 문자열 중 하나로 레코드를 반환합니다. 그 다음에 변환된 레코드가 Kafka 에 저장합니다.

싱크 커넥터는 소스 커넥터와 반대로 처리됩니다. 즉, 커넥트 작업 프로세스가 Kafka 로부터 레코드를 읽으면 사전 구성된 컨버터를 사용하여 Kafka 의 형식으로된 해당 레코드를 커넥트 데이터 API 레코드로 변환합니다. 그 다음 해당 레코드를 싱크 커넥터에 전달하며, 싱크 커넥터는 그 레코드를 대상 시스템에 씁니다.

커넥터 API 는 커넥터 구현과는 무관하게 Kafka 에 저장된 서로 다른 형식의 데이터를 지원해줍니다. 따라서 사용 가능한 컨버터만 있다면, 어떤 커넥터도 레코드 형식에 구애받지 않고 사용될 수 있습니다.

#### OFFSET MANAGEMENT

오프셋 관리는 작업 프로세스가 커넥터를 위해 수행하는 편의 서비스 중 하나입니다. 커넥터는 자신이 이미 처리했던 데이터가 어떤 것인지 알아야 합니다. 이때 Kafka 가 제공하는 API 를 사용해 이미 처리된 데이터에 관한 저옵를 유지 관리할 수 있습니다.

소스 커넥터의 경우 커넥터가 커넥트 작업 프로세스에게 반환하는 레코드에 논리 소스 파티션과 소스 오프셋이 포함됩니다. 이것들을 Kafka 의 파티션과 오프셋이 아니며, 필요에 따라 소스 시스템에 사용하는 파티션과 오프셋입니다.

예를 들어 파일 소스에서는 하나의 파티션이 하나의 파일이 될 수 있으며, 하나의 오프셋은 파일의 줄 번호, 문자 위치 번호가 될 수 있습니다. JDBC 소스의 경우 하나의 파티션이 하나의 데이터베이스 테이블이 되며, 오프셋은 테이블의 레코드 ID 가 됩니다. 소스 커넥터를 작성할 때는 소스 시스템의 데이터를 파티션으로 분할하고 오프셋을 추적하는 방법을 결정해야 합니다.

소스 파티션과 오프셋을 포함하는 레코드들을 커넥터가 반환하면, 작업 프로세스는 해당 레코드들을 Kafka 브로커에 전송합니다. 그리고 브로커가 해당 레코드들을 쓰면, 작업 프로세스가 그 레코드들의 소스 오프셋을 저장합니다. 이때 Kafka 의 다른 토픽에 저장합니다.

이렇게 하여 커넥터가 다시 시작되거나 중단된 이후에도 가장 최근에 저장되었던 오프셋부터 소스 시스템의 데이터를 읽을 수 있습니다. 싱크 커넥터는 소스 커넥터와 반대지만 처리 절차는 유사합니다. 즉 싱크 커넥터는 Kafka 에 저장된 레코드들을 읽습니다. 이 레코드들은 Kafka 의 토픽과 파티션 및 오프셋을 가집니다. 그 다음 싱크 커넥터는 커넥터 객체의 `put()` 메소드를 호출하여 해당 레코드들을 대상 시스템에 저장합니다.

이 작업이 성공적일 경우 싱크 커넥터는 Kafka 로부터 받았던 오프셋을 커밋합니다. 이때는 평상시에 컨슈머가 커밋하는 메소드들을 사용합니다.

## Alternatives to Kafka Connect 

Kafka 데이터를 읽고 쓰는 방법은 커넥터만 있는것이 아닙니다.

### Ingest Frameworks for Other Datastores 

Hadoop 이나 ElasticSearch 를 이용하여 데이터 아키텍처를 구축할 수 있습니다. 이런 시스템은 나름의 데이터 처리 도구를 가지고 있습니다. 예를 들어 Hadoop 에 Flume, ElasticSearch 의 Logstash, Fluentd 등입니다.

Kafka 가 아키텍처의 핵심 부분이면서 대량의 소스와 싱크를 연결하는게 목적이라면, Kafka 커넥트 API 를 사용하는것을 권합니다.

### GUI-Based ETL Tools 

Informatica, Talend, NiFi 모두 Kafka 를 지원합니다. GUI 기반 방법을 사용해 ETL 파이프라인을 구축하는 경우에 이 시스템을 사용하는게 바람직합니다. 하지만 복잡한 작업 흐름을 가지며 무겁다는 단점이 있습니다. 데이터를 입출력하는 것이 요구사항이라면 복잡한 솔루션이 될 수 있습니다.

데이터 통합과 어플리케이션 통합 및 스트림 프로세싱을 처리할 수 있는 플랫폼으로 Kafka 를 고려할 것을 권장합니다. 데이터스토어만 통합하는 ETL 도구의 성공적인 대체 시스템으로 Kafka 를 사용할 수 있습니다.

### Stream-Processing Frameworks

대부분의 스트림 프로세싱 프레임워크에서는 Kafka 로부터 데이터를 읽어서 다른 대상 시스템에 쓸 수 있습니다. 만약 대상 시스템이 Kafka 를 지원하고, Kafka 의 데이터 처리를 위해 스트림 프로셋싱 프레임워크를 사용할 의향이 있다면, 데이터 통합도 같은 프레임 워크를 사용하는것이 바람직합니다.

위와같이 하면 스트림 프로세싱 워크플로에서 한 단계를 줄일 수 있습니다.

