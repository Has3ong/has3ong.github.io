---
title : Kafka Consumers - Reading Data from Kafka
tags :
- Deserializers
- Consumer
- Apache
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

Kafka 로부터 데이터를 읽는 어플리케이션은 `KafkaConsumer` 를 사용해 Kafka 토픽을 읽고 메세지를 받습니다.

## Kafka Consumer Concepts 

Kafka 로부터 데이터를 읽는 방법을 이해하기 위해서는 우선 컨슈머와 컨슈머 그룹에 대해서 알아야합니다.

### Consumers and Consumer Groups 

어플리케이션에서는 컨슈머 객체를 생성하여 해당 토픽을 읽은 후 그것의 메세지들을 받아 검사하고 결과를 다른 파일에 저장할 것입니다.

만약 메세지들을 쓰는 속도를 어플리케이션에서 메세지를 처리하는 속도보다 빠르면 추가되는 메세지들의 속도를 따라갈 수 없어서 어플리케이션의 메세지 처리는 점점 늦어지게됩니다.

그러므로 토픽을 소비하는 컨슈머의 규모를 확장해야합니다. 즉 다수의 프로듀서들이 같은 토픽의 메세지들을 쓸 수 있는것과 마찬가지로 다수의 컨슈머들이 같은 토픽의 메세지들을 분담해서 읽을 수 있어야 합니다.

Kafka 컨슈머들은 컨슈머 그룹에 속합니다. 다수의 컨슈머가 같은 토픽을 소비하면서 같은 컨슈머 그룹에 속할 때는 각 컨슈머가 해당 토픽의 서로 다른 파티션을 분담해서 메세지를 읽을 수 있습니다.

4 개의 파티션을 가지는 T1 토픽이 있다고 가정하겠습니다. 여기에 새로운 컨슈머 C1 을 추가하면 아래와 같은 그림이 될것입니다. 그리고 C1 컨슈머는 4 개 파티션 모두에 있는 메세지들을 읽을것입니다.

> Example 1 - One Consumer group with four partitions

![image](https://user-images.githubusercontent.com/44635266/70437071-179d6e80-1ace-11ea-8bde-93b65cd0ec5a.png)

만약 컨슈머 그룹에 새로운 컨슈머를 추가한다면, 각 컨슈머는 두 개의 파티션에서만 메세지를 읽으면 됩니다. 예를 들어, `Example 2` 와 같이 C1 은 파티션 0 과 2 를 C2 는 파티션 1 과 3 의 메세지들을 읽습니다.

> Example 2 - Four partitions split to two consumer groups

![image](https://user-images.githubusercontent.com/44635266/70437074-18ce9b80-1ace-11ea-9bd0-24a41b82f402.png)

컨슈머의 개수와 파티션의 개수가 똑같으면 `Example 3` 처럼 각 컨슈머는 하나의 파티션에 있는 메세지들만 읽으면 됩니다.

> Example 3 - Four consumer groups to one partition each

![image](https://user-images.githubusercontent.com/44635266/70437075-19ffc880-1ace-11ea-9ede-7eab88a93c80.png)

만약 파티션의 개수보다 컨슈머의 개수가 많아지면 일부 컨슈머는 쉬면서 어떤 메세지도 읽지 않을것입니다.

> Example 4 - More consumer groups than partitions means missed messages

![image](https://user-images.githubusercontent.com/44635266/70437078-1bc98c00-1ace-11ea-8546-0a876e014751.png)

같은 토픽의 데이터를 다수의 어플리케이션이 읽어야 하는 경우도 매우 많습니다. 실제로 Kafka 의 주요 설계 목표 중 하나는, 생성된 데이터를 Kafka Topic(조직 전체에서 여러 용도로 사용한다.)으로 만드는것입니다.

같은 토픽의 데이터를 다수의 어플리케이션이 읽어야 할 때는 각 어플리케이션이 자신의 컨슈머 그룹을 갖도록 합니다.

> Example 5 - Adding a new consumer group ensures no messages are missed

![image](https://user-images.githubusercontent.com/44635266/70437248-7ebb2300-1ace-11ea-849b-3ba491a57cf2.png)

앞의 예에서, 한 개의컨슈머를 갖는 새로운 컨슈머 그룹을 추가하면 이 그룹의 컨슈머는 기존의 컨슈머 그룹과 무관하게 T1 토픽의 모든 메세지를 읽습니다.

### Consumer Groups and Partition Rebalance 

컨슈머 그룹의 컨슈머들은 자신이 읽는 토픽 파티션의 소유권을 공유합니다. 그리고 새로운 컨슈머를 그룹에 추가하면 이전에 다른 컨슈머가 읽던 파티션의 메세지들을 읽습니다.

특정 컨슈머가 문제가 생겨 중단될 때도 마찬가지입니다. 즉, 그 컨슈머가 읽던 파티션은 남은 컨슈머 중 하나가 재할당받아 읽게됩니다.

한 컨슈머로부터 다른 컨슈머로 파티션 소유권을 이전하는 것을 **리밸런싱(rebalancing)** 이라고 합니다. 리밸런싱은 컨슈머 그룹의 가용성과 확장성을 높여줍니다. 하지만, 리밸런싱을 하는동안에는 컨슈머들은 메세지들을 읽을 수 없으므로 해당 컨슈머 그룹 전체가 잠시나마 사용 불가능 상태가 됩니다. 또한, 한 컨슈머로부터 다른 컨슈머로 파티션이 이전될 때는 해당 컨슈머의 이전 파티션에 관한 상태 정보가 없어집니다. 따라서 캐시 메모리에 있던 데이터도 지워져 다시 설정될 때까지 어플리케이션 실행이 느려질 수 있습니다.

**그룹 조정자(Group Coordinator)** 로 지정된 Kafka 브로커에 컨슈머가 **하트비트(Heartbeat)** 를 전송하면 자신이 속한 컨슈머 그룹의 멤버십과 자신에게 할당된 파티션 소유권을 유지할 수 있습니다.

하트비트는 컨슈머의 상태를 알리기 위해 전송되는 신호입니다. 하트비트가 일정시간 간격으로 전송된다면 해당 컨슈머는 정상적으로 동작하며, 자신의 파티션 메세지를 처리 가능한 것으로 간주됩니다. 하트비트는 컨슈머가 **폴링(polling)** 할 때 또는 읽은 메세지를 커밋할 때 자동 전송됩니다.

만약 컨슈머가 세션 타임아웃 시간이 경과될 때 까지 하틥트 전송을 중단하면 GroupCoordinator 가 해당 컨슈머를 중단된것으로 간주하고 리밸런싱을 시작시킵니다. 리밸런싱하는 동안에는 중단된 컨슈머가 소유한 파티션의 메세지가 처리되지 않습니다. 컨슈머가 정상적으로 종료될 때는 GroupCoordinator 에게 떠나는것을 알려주며, 이때 GroupCoordinator 는 처리 공백을 줄이기 위해 곧바로 리밸런싱을 시작시킵니다.

## Creating a Kafka Consumer

메세지를 갖는 레코드를 읽기 시작하려면, 우선 컨슈머 클래스인 `KafkaConsumer`의 인스턴스를 생성합니다. 필수 속성으로는 `bootstrap.servers`, `key,deserializer`, `value,deserializer`가 필요합니다. 

* `bootstrap.servers` 는 카프카 클러스터에 연결하기 위한 문자열입니다.
* `key,deserializer`, `value,deserializer` 는 프로듀서에 정의되는 직렬처리기와 반대 기능을 수행하는 역직렬처리기를 지정합니다.

이외에도 `group.id` 속성이 필요합니다. 이 속성은 컨슈머가 속하는 컨슈머 그룹을 나타냅니다.

다음 코드는 컨슈머를 생성하는 코드입니다.

```java
Properties props = new Properties();

props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("group.id", "CountryCounter");
props.put("key.deserializer",
  "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer",
  "org.apache.kafka.common.serialization.StringDeserializer");

KafkaConsumer<String, String> consumer =
  new KafkaConsumer<String, String>(props);
```

## Subscribing to Topics

컨슈머를 생성한 다음에는 하나 이상의 토픽을 구독해야합니다. 이때 `subscribe()` 메소드를 이용하며, 이 메소드는 토픽 이름을 저장한 List를 매개변수로 받습니다.

```java
consumer.subscribe(Collections.singletonList("customerCountries"));
```

정규 표현식을 매개변수로 전달하여 `subscribe()` 메소드를 호출할 수 있습니다.

다수의 토픽에서 데이터를 읽고, 그 토픽들이 포함하는 서로 다른 타입의 데이터를 처리해야 하는 어플리케이션에서 정규 표현식을 사용하면 유용합니다. Kafka 와 다른 시스템 간에 데이터를 복제하는 어플리케이션에서 정규 표현식을 사용한 다수의 토픽 구독을 가장 많이 사용합니다.

예를 들어, 모든 `test` 토픽을 구독하려면 다음과 같이 사용합니다.

```java
consumer.subscribe("test.*");
```

## The Poll Loop

컨슈머 API의 핵심은 서버로부터 연속적으로 많은 데이터를 읽기 위해 폴링하는 루프에 있습니다. 컨슈머의 토픽 구독 요청이 정상적으로 처리되면 폴링 루프에서 데이터를 읽는데 필요한 모든 상세 작업을 처리합니다. 예를 들면 다음과 같습니다.

```java
try {
  while (true) {
    ConsumerRecords<String, String> records = consumer.poll(100);
    for (ConsumerRecord<String, String> record : records) {
      log.debug("topic = %s, partition = %s, offset = %d,
        customer = %s, country = %s\n",
        record.topic(), record.partition(), record.offset(),
        record.key(), record.value());
 
      int updatedCount = 1;
      if (custCountryMap.countainsValue(record.value())) {
        updatedCount = custCountryMap.get(record.value()) + 1;
      }
      
      custCountryMap.put(record.value(), updatedCount)
      JSONObject json = new JSONObject(custCountryMap);
      System.out.println(json.toString(4))
    }
  }
} finally {
  consumer.close();
}
```

위의 예처럼 폴링 루프는 `poll()` 호출이 포함된 무한 루프를 말하며, 컨슈머 클래스에서 스레드로 실행되는 `run()` 메소드에 포함됩니다. 폴링 루프에서는 `poll()` 호출로 데이터를 읽은 후 필요한 처리를 합니다. `poll()` 메소드에서는 데이터를 읽는 것 외에도 많은 일을 수행합니다. 즉, 새로운 컨슈머에서 최초로 `poll()` 을 호출할 때는 이 메소드에서 GroupCoordinator를 찾고 컨슈머 그룹에 추가시키며, 해당 컨슈머에게 할당된 파티션 내역을 받습니다.

이외에도 리밸런싱이 생길때 필요한 처리와 컨슈머가 계속 살아서 동작할 수 있게 해주는 하트비트 전송도 `poll()` 메소드에서 자동으로 수행됩니다. 그러나 때에 따라서는 폴링 루프 내부에서 수동으로 처리될 수 도 있습니다.

## Configuring Consumers 

컨슈머를 구성할 때 사용되는 중요한 매개변수를 알아보겠습니다.

#### fetch.min.bytes

레코드를을 가져올 때 브로커로부타 받기 원하는 데이터의 최소량을 설정하는 매개변수입니다. 브로커가 컨슈머로부터 레코드 요청을 받았지만 읽은 레코드들의 양이 `fetch.min.bytes` 에 지정된 것보다 작다면 브로커는 더 많은 메세지가 모일 때까지 기다렸다가 컨슈머에게 전송합니다.

#### fetch.max.wait.ms

`fetch.min.bytes` 를 설정하면 Kafka 는 설정값만큼 데이터가 모일 때까지 기다렸다가 컨슈머에게 전송합니다. 이와 더불어 `fetch.max.wait.ms` 를 설정하면 기다리는 시간을 제어할 수 있습니다.

디폴트 값은 500 ms 입니다.

#### max.partition.fetch.bytes

서버가 파티션당 반환하는 최대 바이트 수를 제어합니다. 

디폴트 값은 1 MB 입니다.

### session.timeout.ms

컨슈머와 브로커가 연결이 끊기는 시간입니다. 컨슈머가 GroupCoordinator 에게 하트비트를 전송하지 않으면서 이 매개변수의 값으로 설정한 시간이 경과되면 컨슈머는 실행 종료된 것으로 간주되고 GroupCoordinator 는 컨슈머의 파티션들을 해당 그룹의 다른 컨슈머에게 할당하기 위해 해당 컨슈머 그룹의 리벨런싱을 시작합니다.

디폴트 값은 10 s 입니다. 

#### auto.offset.reset

커밋된 오프셋이 없는 파티션을 컨슈머가 읽기 시작할 때, 또는 커밋된 오프셋이 있지만 유효하지 않을 때 컨슈머가 어떤 레코드를 읽게 할 것인지 제어하는 매개변수입니다.

기본 값은 유효한 오프셋이 없음을 의미하는 `latest` 이며, 이 경우 컨슈머는 가장 최근의 레코드들을 읽기 시작합니다. 다른 값으로는 `earliest` 가 있으며, 이 경우 컨슈머는 해당 파티션의 맨 앞부터 모든 데이터를 읽습니다.

#### enable.auto.commit

컨슈머의 오프셋 커밋을 자동으로 할것인지 제어합니다. `enable.auto.commit` 의 값이 true 이면 `auto.commit.interval.ms` 를 설정하여 자동으로 오프셋을 커밋하는 시간 간격을 제어할 수 있습니다.

디폴트 값은 true 입니다.

#### partition.assignment.strategy

컨슈머들과 그들이 구독하는 토픽이 지정되면, 각 컨슈머에게 할당될 파티션들을 이 클래스에서 결정합니다. Kafka 에는 두 가지 전략이 있습니다.

**1. Range**

모든 토픽의 파티션들을 각 컨슈머마다 연속적으로 할당합니다.

**2. RoundRobin**

구독하는 모든 토픽의 모든 파티션들을 컨슈머들에게 하나씩 번갈아 차례대로 할당합니다.

#### client.id

이 매개변수의 값은 어떤 문자열도 가능하며, 클라이언트로부터 전송된 메세지를 식벼랗기 위해 브로커가 사용합니다.

#### max.poll.records

한 번의 `poll()` 메소드 호출에서 반환되는 레코드의 최대 개수를 제어합니다. 어플리케이션이 처리해야 하는 데이터의 양을 제어할 때 이 매개변수가 유용합니다.

#### receive.buffer.bytes / send.buffer.bytes

데이터를 읽고 쓸 때 소켓이 사용하는 TCP 송수신 버퍼의 크기를 나타냅니다. 만약 **-1** 로 설정하면 운영체제의 디폴트값으로 사용됩니다.

## Commits and Offsets 

`poll()` 메서드를 호출될 때마다 그룹의 컨슈머들이 아직 읽지 않은 레코드들을 반환한다. 즉, 그룹의 각 컨슈머가 읽은 레코드들을 추적 및 관리하는 방법이 있다. Kafka 는 다른 JMS(Java Message System) 이 하는 것과 다른 방법으로 컨슈머가 읽는 레코드를 추적 관리합니다. Kafka 의 컨슈머는 파티션별로 자신이 있는 레코드의 현재 위치(Offset)을 추적 관리할 수 있습니다. 

파티션 내부의 현재 위치를 변경하는 것을 커밋(Commit) 이라고 합니다.

기존의 컨슈머가 비정상적으로 종료가 되거나, 새로운 컨슈머가 컨슈머 그룹에 추가가 된다면 오프셋 커밋은 **리밸런싱을 유발한다**. 그리고 리밸런싱이 끝나면 각 컨슈머는 종전과 다른 파티션들을 할당받게 된다. 따라서 어느 위치 부터 메세지를 읽어야 할지 알기 위해 컨슈머는 각 파티션의 마지막으로 커밋된 오프셋을 알아낸 후 해당 오프셋부터 계속 읽어나간다.

`Example 6` 경우 마지막으로 커밋된 오프셋이 컨슈머가 가장 최근에 읽고 처리한 메세지의 오프셋보다 작으면 메세지들이 두 번 처리가 됩니다.

> Example 6 - Re-processed messages

![image](https://user-images.githubusercontent.com/44635266/70606302-80582880-1c3f-11ea-9e6b-5c612d90d7fc.png)

`Example 7` 경우 마지막으로 커밋된 오프셋이 컨슈머가 가장 최근에 읽고 처리한 메세지의 오프셋보다 크면 메세지 누락이 생길 수 있습니다.

> Example 7 - Missed messages between offsets

![image](https://user-images.githubusercontent.com/44635266/70606305-81895580-1c3f-11ea-9b4d-79e2062d500e.png)

오프셋 관리는 컨슈머 클라이언트 어플리케이션에 큰 영향을 줍니다. 따라서 Kafka 컨슈머 API 에서는 오프셋을 커밋하는 여러 가지 방법을 제공합니다.

### Automatic Commit 

**자동 커밋(Automatic Commit)** 은 가장 쉬운 오프셋 커밋 방법입니다. KafkaConsumer 객체가 자동으로 커밋해줍니다. 이때 `enable.auto.commit=true`로 설정하면 `poll()` 메소드에서 받은 오프셋 중 가장 큰 것을 5 초 마다 한 번씩 커밋을 하게 됩니다.

자동 커밋의 기본 시간 간격은 5 s 이지만, `auto.commit.interval.ms` 를 설정하여 변경이 가능합니다. 

Kafka 컨슈머의 모든것이 그렇듯이, 자동 커밋도 폴링 루프에서 처리가 됩니다.  즉, 매번 폴링할 때마다 KafkaConsumer 객체가 커밋할 시간이 되었는지 확인하며, 만일 시간이 되었다면 마지막으로 호출된 `poll()` 메소드에서 반환된 오프셋을 커밋합니다.

하지만, 자동 커밋을 사용할 때도 중복 처리가 되는 경우가 있습니다. 가장 최근에 커밋을 진행 한 후 3 초 동안 추가로 레코드들을 읽고 처리하다가 리밸런싱이 되면 리밸런싱이 끝난 후 모든 컨슈머들은 마지막으로 커밋된 오프셋부터 레코드들을 읽게 됩니다. 이 경우 해당 오프셋은 3 초 이전의 것이므로, 3 초동안 읽었던 레코드는 모두 2번 처리가 됩니다.

오프셋 자동 커밋을 자주 사용하여 중복을 줄일 수 있지만 완전히 없애는것은 불가능합니다.

자동 커밋이 활성화된 상태에서 `poll()` 메소드를 호출하면, 항상 이전 호출에서 반환된 마지막 오프셋을 커밋합니다. 따라서 이후로 읽고 처리했던 메세지가 어떤 것인지는 모릅니다. 그러므로 `poll()` 메소드에서 반환된 모든 메세지는 `poll()` 을 호출하기 전에 처리가 끝나도록 하는 것이 중요합니다.

### Commit Current Offset 

`enable.auto.commit=false` 를 설정하면 어플리케이션이 요구할 때만 오프셋이 커밋이 됩니다. 이때 가장 간단하고 신뢰도가 높은 것이 `commitSync()` 입니다. 이 메소드는 `poll()` 메소드에서 반환된 마지막 오프셋을 커밋합니다.

`commitSync()` 는 `poll()` 에서 반환된 가장 최근의 오프셋을 커밋합니다. 따라서 `poll()` 에서 반환된 모든 레코드의 처리가 다 된 후에 `commitSync()` 를 호출해야 합니다.

가장 최근에 메세지 배치를 처리한 후에  `commitSync()` 를 사용해서 오프셋을 커밋하는 예는 다음과 같습니다.

```Java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf(
      "topic = %s, partition = %s, offset =
      %d, customer = %s, country = %s\n",
      record.topic(), record.partition(),
      record.offset(), record.key(), record.value());
  }
 try {
    consumer.commitSync();
  } catch (CommitFailedException e) {
    log.error("commit failed", e)
  }
}
```

해당 `while` 구문 안에서 각 레코드의 내용을 모두 출력하면 처리가 끝나는것으로 간주하며 처리가 끝난뒤 `commitSync()` 를 호출하는 모습을 볼 수 있습니다.

### Asynchronous Commit 

브로커가 커밋 요청에 응답할 때까지 어플리케이션이 일시 중지된다는것이 수동 커밋의 단점입니다. 이로 인해 어플리케이션이 처리량의 제한이 생기게 됩니다. 이를 보완하기 위한 또 다른 옵션으로 비동기 커밋이 있습니다.

**비동기 커밋(Asynchronous Commit)** 은 브로커의 커밋 응답을 기다리는 대신, 커밋 요청을 전송하고 처리를 계속할 수 있습니다. 코드를 통해 예를 알아보겠습니다.

```Java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf(
      "topic = %s, partition = %s,
      offset = %d, customer = %s, country = %s\n",
      record.topic(), record.partition(), record.offset(),
      record.key(), record.value());
  }
  consumer.commitAsync();
}
```

`commitAsync()` 메소드는 `commitSync()` 와 달리 커밋을 재시도하지 않습니다. 왜냐하면 비동기 처리에서는 서버의 응답을 받는 사이에 다른 커밋이 먼저 성공할 수 있기 때문입니다.

비동기 처리는 callback 을 사용하여 `commitAsync()`에 전달할 수 있습니다. callback 을 사용한 비동기 처리의 예는 아래 코드를 보시면 됩니다.

```Java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf(
      "topic = %s, partition = %s,
      offset = %d, customer = %s, country = %s\n",
      record.topic(), record.partition(), record.offset(),
      record.key(), record.value());
  }
  consumer.commitAsync(new OffsetCommitCallback() {
    public void onComplete(Map<TopicPartition,
      OffsetAndMetadata> offsets, Exception exception) {
    if (e != null)
      log.error("Commit failed for offsets {}", offsets, e);
    }
  });
}
```

위 코드에선 오프셋 커밋을 전송하고 다음 처리를 계속합니다. 그러나 커밋이 실패하면 callback 메소드인 `onComplete` 가 자동 호출되어 에러메세지와 해당 오프셋을 로깅합니다.

### Combining Synchronous and Asynchronous Commits 

루프의 실행이 끝나고 컨슈머를 종료하기 전 또는 리밸런싱이 시작되기 전의 마지막 커밋이라면 성공 여부를 추가로 확인해야 합니다.

이 경우 `commitSync()` 와 `commitAsync()` 를 같이 사용합니다. 아래 코드를 참고하시면 됩니다.

```Java
try {
  while (true) {
    ConsumerRecords<String, String> records = consumer.poll(100);
    for (ConsumerRecord<String, String> record : records) {
      System.out.printf(
        "topic = %s, partition = %s, offset = %d,
        customer = %s, country = %s\n",
        record.topic(), record.partition(),
        record.offset(), record.key(), record.value());
    }
    consumer.commitAsync();  // 1
  }
} catch (Exception e) {
  log.error("Unexpected error", e);
} finally {
  try {
    consumer.commitSync();  // 2
  } finally {
    consumer.close();
  }
}
```

1. 모든 처리가 정상적일 때 `commitAsync()` 를 사용하여 오프셋을 커밋합니다. 처리속도가 빠르고 하나의 커밋이 실패해도 다음 커밋이 재시도의 기능을 해주기 때문입니다.
2. 하지만 컨슈머를 종료시킬 때 `commitSync()` 를 호출합니다. 이 메소드는 커밋이 성공하거나 복구 불가능 에러가 될때가지 커밋을 재시도하게 됩니다.

### Commit Specified Offset 

특정 오프셋을 커밋하는 경우도 있습니다. 더 자주 커밋을 하고 싶거나 `poll()` 메소드에서 용량이 큰 배치를 반환할 때 배치 중간의 오프셋을 커밋하여 리밸런싱으로 인한 많은 메세지의 중복처리를 막고자 할때 사용이 됩니다. 코드로 알아보겠습니다.

```Java
private Map<TopicPartition, OffsetAndMetadata> currentOffsets =
  new HashMap<>();
int count = 0;

....

while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf(
      "topic = %s, partition = %s, offset = %d,
      customer = %s, country = %s\n",
      record.topic(), record.partition(), record.offset(),
      record.key(), record.value());
    
    currentOffsets.put(
      new TopicPartition(record.topic(),
      record.partition()), 
      new OffsetAndMetadata(record.offset()+1, "no metadata"));
      
  if (count % 1000 == 0)
    consumer.commitAsync(currentOffsets, null);
  count++;
  }
}
```

위의 예들과는 다르게 직접 오프셋을 추적, 관리하고 파티션과 오프셋을 저장한 Map 을 인자로 사용합니다.

또한 위 코드에서는 `if (count % 1000 == 0)` 를 이용하여 100 개의 레코드마다 한 번씩 현재 오프셋을 커밋하게 설정하였습니다.

## Rebalance Listeners

앞 포스트에서는 오프셋과 커밋에 관해 설명했듯이, 컨슈머는 종료되기 전이나 파티션 리밸런싱이 시작되기 전에 클린업하는 처리를 해야합니다.

예를 들어, 컨슈머가 파티션의 소유권을 잃게 되는것을 알게 된다면, 처리했던 마지막 메세지의 오프셋을 커밋해야하며, 사용하던 파일 핸들, 데이터베이스 연결 등도 닫아야합니다. Kafka 에서는 **ConsumerRebalanceListener** 인터페이스를 구현하여 사용할 수 있습니다.

ConsumerRebalanceListener 에는 두 가지 메소드가 있습니다.
 
**public void onPartitionsRevoked(Collection<TopicPartition> partitions)** 

리밸런싱이 시작되기 전에, 컨슈머가 메세지 소비를 중단한 후 호출이 된다. 오프셋을 커밋해야 하는곳이 이 메소드 입니다. 현재의 파티션을 이어서 소비할 다른 컨슈머가 해당 파티션의 어디서부터 메세지 소비를 시작할지 알 수 있습니다.

**public void onPartitionsAssigned(Collection<TopicPartition> partitions)** 

이 메소드는 파티션이 브로커에게 재할당된 경우와 컨슈머가 파티션을 새로 할당받아 메세지 소비를 시작하기전에 호출이 된다.

아래는 ConsumerRebalanceListener 인터페이스 구현의 예 입니다.

```java
private Map<TopicPartition, OffsetAndMetadata> currentOffsets =
  new HashMap<>();
private class HandleRebalance implements ConsumerRebalanceListener {
  public void onPartitionsAssigned(
    Collection<TopicPartition> partitions) {
    
  }
  public void onPartitionsRevoked(
    Collection<TopicPartition> partitions) {
    
    System.out.println(
      "Lost partitions in rebalance.
      Committing current
      offsets:" + currentOffsets);
    consumer.commitSync(currentOffsets);  // 1
  }
}
try {
  consumer.subscribe(topics, new HandleRebalance()); // 2
  while (true) {
    ConsumerRecords<String, String> records =
      consumer.poll(100);
    for (ConsumerRecord<String, String> record : records) {
      System.out.printf(
        "topic = %s, partition = %s, offset = %d,
        customer = %s, country = %s\n",
        record.topic(), record.partition(), record.offset(),
        record.key(), record.value());
        
      currentOffsets.put(
        new TopicPartition(record.topic(),
        record.partition()), new
        OffsetAndMetadata(record.offset()+1, "no metadata"));
    }
    consumer.commitAsync(currentOffsets, null);
  }
} catch (WakeupException e) {
 // ignore, we're closing
} catch (Exception e) {
  log.error("Unexpected error", e);
} finally {
  try {
    consumer.commitSync(currentOffsets);
  } finally {
    consumer.close();
    System.out.println("Closed consumer and we are done");
  }
}
```

1. 리밸런싱이 시작되면 컨슈머가 구독하던 파티션을 잃게 되므로 그 전에 오프셋을 커밋한다.
2. `subscribe()` 메소드를 호출할 때 RebalanceListener 인터페이스를 구현한 객체를 인자로 전달한다.

## Consuming Records with Specific Offsets

지금까지는 각 파티션의 마지막 커밋 오프셋부터 메세지를 읽고 처리하기 위해 `poll()` 메소드를 활용했습니다. 하지만, 다른 오프셋부터 읽기 시작하길 원할 때도 있습니다.

파티션의 맨 앞 오프셋부터 모든 메세지를 읽거나 파티션의 제일 끝 오프셋을 찾은 후 이후에 추가되는 메세지만 읽기 시작할때는 KafkaConsumer 클래스의 `seekToBeginning(Collection<TopicPartition> tp)` 와 `(seekToEnd(Collection<TopicPartition> tp)` 메소드를 사용할 수 있습니다.

Kafka 에서 데이터를 처리한 후에 데이터 결과를 데이터베이스나 Hadoop 에 저장할 때 어떤 데이터도 누락시키지 않아야 하고, 중복 저장되지 않게 해야한다고 가정해보겠습니다.

위 경우 컨슈머의 폴링 루프는 다음과 같이 구현할 수 있습니다.

```java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(100);
  for (ConsumerRecord<String, String> record : records) {
    
    currentOffsets.put(
      new TopicPartition(record.topic(),
      record.partition()),
      record.offset());
      
    processRecord(record);
    storeRecordInDB(record);
    consumer.commitAsync(currentOffsets);
  }
}
```

위 코드는 각 레코드를 처리할 때마다 오프셋을 커밋을 합니다. 이렇게 하면 레코드는 데이터베이스에 확실하게 저장이 되지만 해당 레코드가 다시 처리되어 중복 데이터가 발생할 수 있습니다.

그래서 레코드와 오프셋 모드를 하나의 트랜잭션으로 처리하여 데이터베이스 저장하는 방법이 있습니다. 이때, 레코드와 오프셋 모두가 커밋되었는지 다시 처리해야하는지 알 수 있기 때문입니다.

오프셋이 Kafka 가 아닌 데이터베이스에 저장된다면 한 가지 문제를 해결해야합니다. 데이터베이스에 저장된 오프셋을 어떻게 사용해야 하는가입니다. 이 경우에 `seek()` 메소드를 사용합니다. 컨슈머가 기존 파티션을 읽기 시작하거나 새로운 파티션이 할당될 때 데이터베이스에 저장된 오프셋을 가져온 후 `seek()` 메소드를 사용하여 찾으면 됩니다.

아래 코드를 통해 알아보겠습니다.

```java
public class SaveOffsetsOnRebalance implements ConsumerRebalanceListener {
  public void onPartitionsRevoked(
    Collection<TopicPartition>partitions) {
      
    commitDBTransaction(); // 1
  }
 
  public void onPartitionsAssigned(
    Collection<TopicPartition> partitions) {
  
    for(TopicPartition partition: partitions)
      consumer.seek(partition, getOffsetFromDB(partition)); // 2
  }
}

consumer.subscribe(topics, new SaveOffsetOnRebalance(consumer));
consumer.poll(0); // 3

for (TopicPartition partition: consumer.assignment())
  consumer.seek(partition, getOffsetFromDB(partition));
  
while (true) {
  ConsumerRecords<String, String> records =
    consumer.poll(100);
    
  for (ConsumerRecord<String, String> record : records) {
    processRecord(record);
    storeRecordInDB(record);
    storeOffsetInDB(record.topic(), record.partition(), record.offset()); // 4
  }
  commitDBTransaction();
}
```

위 코드는 **ConsumerRebalanceListener** 와 `seek()` 를 사용해서 데이터베이스에 저장된 오프셋부터 처리하도록 합니다.

1. `commitDBTransaction()` 메소드를 이용하여 데이터베이스 트랜잭션으로 오프셋을 커밋합니다. 리밸런싱이 시작되면 컨슈머가 현재 소비하던 파티션을 잃게 되므로 그 전에 오프셋을 저장해야 합니다.
2. `getOffsetFromDB(partition)` 에서는 데이터베이스에 저장된 오프셋을 가져오며, `seek()` 를 호출하여 새로 할당된 파티션의 오프셋들을 찾습니다.
3. 컨슈머를 처음 시작할 때 토픽 구독 요청 후 `poll()` 을 호출하여 컨슈머 그룹에 합류하고 파티션을 할당 받는다. 다음 `seek()` 메소드를 호출하여 할당된 파티션들의 오프셋을 찾는다.
4. `processRecord(record)` 는 데이터를 처리하며 `storeRecordInDB(record)` 는 데이터베이스에 데이터를 저장한다. 마지막으로 `storeOffsetInDB(record.topic(), record.partition(), record.offset());` 는 오프셋을 데이터베이스에 저장한다.

외부 저장소에 오프셋과 데이터를 저장하는 방법은 많습니다. 하지만, 오프셋이 저장되어 컨슈머가 그 오프셋으로부터 메세지를 읽을 수 있게 하려면, 모든 방법에서 ConsumerRebalanceListenr 와 seek() 를 사용해야 합니다.

## But How Do We Exit?

컨슈머는 스레드로 동작하며 무한 폴링루프를 실행합니다. 이 폴링 루프를 벗어나서 컨슈머를 종료시키는 방법을 알아보겠습니다.

폴링 루프를 벗어나 컨슈머 스레드가 정상적으로 종료되도록 하기 위해선 또 다른 스레드에서 KafkaConsumer 객체의 `wakeup()` 메소드를 호출해야 합니다. `wakeup()` 메소드를 호출하면 **WakeupException** 예외를 발생시켜 `poll()` 메소드가 중단됩니다.

하지만 컨슈머 스레드가 종료하기 전에는 반드시 `close()` 메소드를 호출하여 닫아야합니다. 이 메소드에서는 필요하면 오프셋이 커밋되며, 현재의 컨슈머가 그룹을 떠난다는 메세지가 GroupCoordinator 에게 전송됩니다. 그러면 세션은 타임아웃을 기다리지 않고 GroupCoordinator 는 곧바로 리밸런싱을 시작시키며, 현재의 컨슈머에게 할당된 파티션들이 그룹의 다른 컨슈머에게 재할당됩니다.

컨슈머 어플리케이션이 main 스레드로 실행 중일 때 폴링 루프를 벗어나서 종료되는 코드의 예를 보여드리겠습니다. 전체 코드는 http://bit.ly/2u47e9A 에서 확인하시면 됩니다.

```java
Runtime.getRuntime().addShutdownHook(new Thread() {
  public void run() {
    System.out.println("Starting exit...");
    consumer.wakeup();  // 1
    try {
      mainThread.join();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
});

...

try {
  // looping until ctrl-c, the shutdown hook will cleanup on exit
  while (true) {
    ConsumerRecords<String, String> records =
      movingAvg.consumer.poll(1000);
    System.out.println(System.currentTimeMillis() + "-- waiting for data...");
    
  for (ConsumerRecord<String, String> record : records) {
    System.out.printf(
      "offset = %d, key = %s, value = %s\n",
      record.offset(), record.key(), record.value());
  }
  
  for (TopicPartition tp: consumer.assignment())
    System.out.println(
      "Committing offset at position:" +  consumer.position(tp));
    movingAvg.consumer.commitSync();
  }
} catch (WakeupException e) {
  // ignore for shutdown  // 2  
} finally {
  consumer.close(); // 3
  System.out.println("Closed consumer and we are done");
}
```

1. 컨슈머 실행 중 `Ctrl + C` 키를 누르면 셧다운 후크로 등록한 스레드의 `run()` 메소드가 실행되어 `wakeup()`을 호출한다. 그 다음 폴링 루프의 `poll()`를 실행할 때 **WakeupException** 예외를 발생시켜 폴링 루프를 벗어난다.
2. 다른 스레드에서 `wakeup()` 을 호출하면 `poll()` 을 실행할 때 **WakeupException** 예외가 발생한다.
3. 컨슈머 스레드는 위에서 기술하듯이 종료 전에 반드시 닫아야 합니다.

## Deserializers

Kafka 프로듀서는 메세지 객체를 바이트 배열로 전환하는 **직렬처리기(Serializer)**가 필요하다. 이와 반대로 Kafka 컨슈머에서는 프로듀서로 부터 받은 바이트 배열을 Java 객체로 변환하는 **역직렬처리기(Deserializer)** 가 필요합니다.

이전에 사용한  Customer 클래스를 사용하겠습니다.

```java
public class Customer {
  private int customerID;
  prviate String customerName;
  
  public Customer(int ID, String name) {
    this.customerID = ID;
    this.customerName = name;
  }
  
  public int getID() {
    return customerID;
  }
  
  public String getName() {
    return customerName;
  }
}
```

커스텀 역직렬처리기의 사용 예를 코드로 나타내보겠습니다.

```java
import org.apache.kafka.common.errors.SerializationException;

import java.nio.ByteBuffer;
import java.util.Map;

public class CustomerDeserializer implements Deserializer<Customer> {
  
  @Override
  public void configure(Map configs, boolean isKey) {
    // nothing to configure
  }
 
  @Override
  public Customer deserialize(String topic, byte[] data) {
    int id;
    int nameSize;
    String name;
    
    try {
      if (data == null)
        return null;
      if (data.length < 8)
        throw new SerializationException("Size of data received by IntegerDeserializer is shorter than expected");
        
      ByteBuffer buffer = ByteBuffer.wrap(data);
      id = buffer.getInt();
      String nameSize = buffer.getInt();
      
      byte[] nameBytes = new Array[Byte](nameSize);
      buffer.get(nameBytes);
      
      name = new String(nameBytes, 'UTF-8');
      
      return new Customer(id, name);  // 1
      
    } catch (Exception e) {
      throw new SerializationException("Error when serializing Customer to byte[] " + e);
    }
  }
    
  @Override
  public void close() {
    // nothing to close
  }
}
```

1. 직렬처리기와는 반대로 역직렬처리 코드는 바이트 배열로부터 Java 객체를 반환해야 하므로 위 코드에서는 `return new Customer(id, name);` 를 반환한다.

### Using Avro deserialization with Kafka consumer

마지막으로 Avro를 사용한 역직렬처리기 예시를 보고 끝내겠습니다.

```java
Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("group.id", "CountryCounter");

props.put("key.serializer",
  "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.serializer",
  "io.confluent.kafka.serializers.KafkaAvroDeserializer");
props.put("schema.registry.url", schemaUrl);

String topic = "customerContacts"

KafkaConsumer consumer = 
  new KafkaConsumer(createConsumerConfig(brokers, groupId, url));
  
consumer.subscribe(Collections.singletonList(topic));
System.out.println("Reading topic:" + topic);

while (true) {
  ConsumerRecords<String, Customer> records =
  consumer.poll(1000);
  
  for (ConsumerRecord<String, Customer> record: records) {
    System.out.println("Current customer name is: " + record.value().getName());
  }
  consumer.commitSync();
}
```