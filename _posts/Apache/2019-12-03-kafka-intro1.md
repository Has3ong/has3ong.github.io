---
title : Kafka Introduction -1-
tags :
- Apache
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Publish / Subscribe System

Producer가 메세지를 구분해서 Pub/Sub 시스템에 전송하면 Consumer는 특정 부류의 메세지를 구독할 수 있게한다. 이 메세지를 저장하고 중계하는 역할을 브로커가 수행한다.

이런 Pub/Sub 시스템은 아래와 같이 다양한 방법이 있다.

> Example 1 - A single, direct metrics publisher

![image](https://user-images.githubusercontent.com/44635266/70034511-a6a11700-15f4-11ea-91cd-26ca31822975.png)

> Example 2 - A metrics publish/subscribe system

![image](https://user-images.githubusercontent.com/44635266/70034515-a86ada80-15f4-11ea-99c5-42aeb14c11c3.png)

로그 메세지도 `Example 2` 와 같이 유사하게 처리할 수 있다. `Example 3` 에서는 세 개의 Pub/Sub 시스템으로 구성된 아키텍쳐다.

> Example 3 -  Many metrics publishers, using direct connections

![image](https://user-images.githubusercontent.com/44635266/70034517-a99c0780-15f4-11ea-9136-af10688a616b.png)

위 시스템은 많은 기능이 중복되어 다수의 메세지 처리 시스템을 유지 관리해야하는 문제점이있다. 따라서 일반화된 유형의 메세지 데이터를 Pub/Sub 하는 하나의 중앙 처리 시스템을 만들 필요가 있다.

## Kaka

**Apache Kafka**가 그런 문제를 해결하기 위해 설계한 Pub/Sub 시스템이다. Kafka 는 '분산 커밋로그', '분산 스트리밍 플랫폼' 이라고도 한다.

카프카의 데이터를 지속해서 자장하고 읽을 수 있으며, 시스템 장애에 대비하고 확장에 따른 성능 저하를 방지하기 위해 데이터 분산 처리될 수 있따.

### Message / Batch

카프카에 데이터 기본단위는 **메세지(Message)** 이다. 카프카의 메세지 데이터는 **토픽(Topic)** 으로 분류된 **파티션(partition)** 에 수록된다.

카프카는 효율성을 위해 여러개의 메세지를 모아 **배치(Batch)** 형태로 파티션에 수록하므로 네트워크로부터 각 메세지를 받아서 처리하는 부담을 줄여준다. 즉, 배치의 크기가 클 수록 단위 시간당 처리될 수 있는 메세지는 많지만 각 메시지 전송 시간은 길어진다. 

이외에도 배치에는 데이터 압축이 적용되므로 더 효율적인 데이터 전송과 저장 능력을 제공한다.

### Schema

카프카는 메세지를 단순히 바이트 배열로 처리하지만, 내용을 이해하기 쉽도록 메시지의 구조를 나타내는 **스키마(Schema)** 를 사용할 수 있다. 간단한 방법으로 **JSON**, **XML** 이 있다.

하지만, 이러한 스키마들은 버전간의 호환성이 떨어진다. 그래서 카프카에서는 **아파치 Avro** 를 선호한다. 

### Topic / Partition

카프카의 메세지는 **토픽(Topic)** 으로 분류된다. 토픽은 데이터베이스 테이블이나 파일 시스템의 폴더와 유사한 개념이다. 하나의 토픽은 여러개의 **파티션(Partition)** 으로 구성될 수 있다.

메세지는 파티션에 추가되는 형태로만 수록되며, 맨 앞부터 제일 끝까지의 순서로 읽힌다. 하나의 토픽은 여러개의 파티션을 갖지만, 메세지의 처리 순서는 토픽이 아닌 파티션별로 유지관리된다. 

`Example 4` 예시를 통해 토픽과 파티션 구조를 알아보겠습니다.

> Example 4 - Representation of a topic with multiple partitions

![image](https://user-images.githubusercontent.com/44635266/70034524-ab65cb00-15f4-11ea-8db0-45ce92d9a625.png)

카프카와 같은 시스템의 데이터를 얘기할 때 **스트림(Stream)** 이라는 용어가 자주 등장한다. 대부분 스트림은 파티션의 개수와 상관없이 하나의 토픽 데이터로 간주된다.

데이터를 쓰는 프로듀서, 데이터를 읽는 컨슈머로 이동되는 연속적인 데이터를 나타낸다. 실시간으로 메세지를 처리할 때 주로 사용되는 방법이 스트림이다.

### Producer / Consumer

**프로듀서(Producer)** 는 새로운 메세지를 생성한다. 프로듀서는 기본적으로 메세지가 어떤 파티션에 수록되는지 관여하지 않는다. 하지만, 프로듀서가 특정 파티션에 메세지를 직접 쓰는 경우도 있다.

**컨슈머(Consumer)** 는 메세지를 읽는다. 하나 이상의 토픽을 구독하여 메세지가 생성된 순서로 읽으며, 메세지의 **오프셋(Offset)** 을 유지하여 메세지의 위치를 알 수 있다.

이 오프셋은 **주키퍼(Zookeeper)** 나 각 파티션에서 저장을 하기 때문에 컨슈머가 메세지 읽기를 중단하더라도 언제든 다음 메세지부터 읽을 수 있다.

컨슈머는 **컨슈머 그룹(Consumer Group)** 의 멤버로 동작한다. 컨슈머 그룹은 하나 이상의 컨슈머로 구성되며, 한 토픽을 소비하기 위해 같은 그룹의 여러 컨슈머가 등장한다. 

> Example 5 - A consumer group reading from a topic

![image](https://user-images.githubusercontent.com/44635266/70034528-ac96f800-15f4-11ea-9e69-cd6a7c65d9f3.png)

`Example 5` 에서는 하나의 토픽을 세개의 컨슈머를 갖는 그룹을 보여준다. 여기서는 두 컨슈머가 각각 한 파티션을 담당하며, 나머지 컨슈머는 두 개의 파티션을 담당한다. 이처럼 각 컨슈머가 특정 파티션에 대응하는것을 파티션 소유권이라 한다.

### Broker / Cluster

하나의 카프카 서버를 **브로커(Broker)** 라 한다. 브로커는 프로듀서로부터 메세지를 수신하고 오프셋을 지정한 후 해당 메세지를 디스크에 저장한다. 또한, 컨슈머의 파티션 읽기 요청에 응답하고 디스크에 수록된 메세지를 전송한다. 시스템 성능에 따라 다르지만 하나의 브로커는 초당 수천 개의 토픽과 수백만 개의 메세지를 처리할 수 있다.

카프카의 브로커는 **클러스터(Cluster)** 의 일부로 동작하도록 설계되었다. 즉, 여러개의 브로커가 하나의 클러스터에 포함될 수 있으며, 그 중 하나는 자동으로 선정되는 클러스터 컨트롤러의 기능을 수행한다.

컨트롤러는 같은 클러스터의 브로커에게 담당 파티션을 할당하고 브로커들이 정상적으로 동작하는지 모니터링한다.

각 파티션은 클러스터의 한 브로커가 소유하며, 그 브로커를 **파티션 리더(Leader)** 라고 한다. 떠한, 같은 파티션이 여러 브로커에 지정될 수 있다. 이 경우 해당 파티션이 **복제(replication)** 된다. 이 경우는 `Example 6` 에서 확인할 수 있다. 해당 파티션의 메세지가 중복으로 저장되지만, 관련 브로커에 장애가 생기면 다른 브로커가 소유권을 인계받아 그 파티션을 처리한다. 각 파티션을 사용하는 모든 컨슈머와 프로듀서는 파티션 리더에 연결되어야한다.

> Example 6 - Replication of partitions in a cluster

![image](https://user-images.githubusercontent.com/44635266/70034532-ae60bb80-15f4-11ea-87a4-7c4ce7895ab7.png)

카프카의 핵심 기능으로 **보존(retention)** 이 있다. 이것은 일정 기간 메세지를 보존하는데 보통 디폴트 값으로 7일이 설정되어있다.

### 카프카의 장점

* 다중 프로듀서
* 다중 컨슈머
* 디스크 기반의 구조
* 확장성
* 고성능
