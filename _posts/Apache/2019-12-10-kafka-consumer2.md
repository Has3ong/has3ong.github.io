---
title : Apache Kafka Consumer -2-
tags :
- Consumer
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Creating a Kafka Consumer

메세지를 갖는 레코드를 읽기 시작하려면, 우선 컨슈머 클래스인 `KafkaConsumer`의 인스턴스를 생성합니다.

필수 속성으로는 `bootstrap.servers`, `key,deserializer`, `value,deserializer`가 필요합니다. 

* `bootstrap.servers` 는 카프카 클러스터에 연결하기 위한 문자열입니다.
* `key,deserializer`, `value,deserializer` 는 프로듀서에 정의되는 직렬처리기와 반대 기능을 수행하는 역직렬처리기를 지정합니다.

이외에도 `group.id` 속성이 필요합니다. 이 속성은 컨슈머가 속하는 컨슈머 그룹을 나타냅니다.

다음 코드는 컨슈머를 생성하는 코드입니다.

```
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

컨슈머를 생성한 다음에는 하나 이상의 토픽을 구독해야합니다. 이때 `subscribe()` 메소드를 이용하며, 이 메소드는 토픽 이름을 저장한 List를 매개변수로 받습니다.

```
consumer.subscribe(Collections.singletonList("customerCountries"));
```

정규 표현식을 매개변수로 전달하여 `subscribe()` 메소드를 호출할 수 있습니다.

다수의 토픽에서 데이터를 읽고, 그 토픽들이 포함하는 서로 다른 타입의 데이터를 처리해야 하는 어플리케이션에서 정규 표현식을 사용하면 유용합니다. Kafka와 다른 시스템 간에 데이터를 복제하는 어플리케이션에서 정규 표현식을 사용한 다수의 토픽 구독을 가장 많이 사용합니다.

예를 들어, 모든 test 토픽을 구독하려면 다음과 같이 사용합니다.

```
consumer.subscribe("test.*");
```

## The Poll Loop

컨슈머 API의 핵심은 서버로부터 연속적으로 많은 데이터를 읽기 위해 폴링하는 루프에 있습니다. 컨슈머의 토픽 구독 요청이 정상적으로 처리되면 폴링 루프에서 데이터를 읽는데 필요한 모든 상세 작업을 처리합니다. 예를 들면 다음과 같습니다.

```
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

### fetch.min.bytes

레코드를을 가져올 때 브로커로부타 받기 원하는 데이터의 최소량을 설정하는 매개변수입니다.

### fetch.max.wait.ms

`fetch.min.bytes` 를 설정하면 Kafka는 설정값만큼 데이터가 모일 때까지 기다렸다가 컨슈머에게 전송합니다. 이와 더불어 `fetch.max.wait.ms` 를 설정하면 기다리는 시간을 제어할 수 있습니다.

디폴트 값은 500ms 입니다.

### max.partition.fetch.bytes

서버가 파티션당 반환하는 최대 바이트 수를 제어합니다. 

디폴트 값은 1MB 입니다.

### session.timeout.ms

컨슈머와 브로커가 연결이 끊기는 시간입니다.

디폴트 값은 10초 입니다. 

만일 컨슈머가 GroupCoordinator에게 하트비트를 전송하지 않으며 이 매개변수의 값으로 설정한 시간이 경과되면 해당 컨슈머는 실행 종료된것으로 간주되며, GroupCoordinator는 그 컨슈머의 파티션들을 해당 그룹의 다른 컨슈머에게 할당하기 위해 해당 컨슈머 그룹의 리밸런싱을 시작합니다.

### auto.offset.reset

커밋된 오프셋이 없는 파티션을 컨슈머가 읽기 시작할 때, 또는 커밋된 오프셋이 있지만 유효하지 않을 때 컨슈머가 어떤 레코드를 읽게 할 것인지 제어하는 매개변수입니다.

### enable.auto.commit

컨슈머의 오프셋 커밋을 자동으로 할것인지 제어합니다.

디폴트 값은 true 입니다.

### partition.assignment.strategy

컨슈머들과 그들이 구독하는 토픽이 지정되면, 각 컨슈머에게 할당될 파티션들을 이 클래스에서 결정합니다. Kafka에는 두 가지 전략이 있습니다.

**1. Range**

모든 토픽의 파티션들을 각 컨슈머마다 연속적으로 할당한다.

**2. RoundRobin**

구독하는 모든 토픽의 모든 파티션들을 컨슈머들에게 하나씩 번갈아 차례대로 할당한다.

### client.id

어떤 클라이언트에서 전송된 메세지인지 식별하기 위해 브로커가 사용한다.

### max.poll.records

한 번의 `poll()` 메소드 호출에서 반환되는 레코드의 최대 개수를 제어합니다. 

### receive.buffer.bytes / send.buffer.bytes

데이터를 읽고 쓸 때 소켓이 사용하는 TCP 송수신 버퍼의 크기를 나타낸다. 만약 **-1**로 설정하면 운영체제의 디폴트값으로 사용된다.