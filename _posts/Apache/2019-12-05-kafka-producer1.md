---
title : Apache Kafka Producer -1-
tags :
- Producer
- Kafka
- Apache
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Kafka Producer

프로듀서 API 는 간단하다. 그러나 프로듀서가 데이터를 전송할 때 내부적으로는 여러 단계로 처리된다 `Example 1`에서느 Kafka에 데이터를 전송할 때 프로듀서가 내부적으로 처리하는 작업을 보여준다.

> Example 1 - High-level overview of Kafka producer components

![image](https://user-images.githubusercontent.com/44635266/70225511-81e2a600-1792-11ea-8171-dfb658e1a6cb.png)

우선 카프카에 쓰려는 메시지를 갖는 `ProducerRecord`를 생성한다. `ProducerRecord`는 우리가 전송하기 원하는 토픽과 그것의 값을 포함해야 하며, 선택적으로 키와 파티션을 지정할 수도 있다. `ProducerRecord`를 Kafka로 전송할 때 프로듀서가 제일 먼저 하는일이 키와 값의 쌍으로 구성되는 메세지 객체들이 네트워크로 전송될 수 있도록 바이트 배열로 직렬화한다. 이것은 **직렬처리기(serializer)** 컴포넌트가 처리한다.

해당 데이터는 **파티셔너(partitioner)** 컴포넌트로 전달된다. 만일 `ProducerRecord`에 특정 파티션을 지정했다면 파티셔너는 특별한 처리를 하지 않고 지정된 파티션을 반환한다. 그러나 파티션을 지정하지 않았다면 `ProducerRecord`의 키를 기준으로 파티셔너가 하나의 파티션을 선택해준다.

그 다음에 같은 토픽과 파티션으로 전송될 레코드들을 모은 레코드 배치에 추가하며, 별개의 스레드가 개 배치를 카프카 브로커에 전송한다.

브로커는 수신된 레코드의 메세지를 처리한 후 응답을 전송한다. 이때 메세지를 성공적으로 쓰면 `RecordMetadata` 객체를 반환한다. 이 객체는 토픽, 파티션, 파티션 내부의 메세지 오프셋을 갖는다. 그러나 메세지 쓰기에 실패하면 에러를 반환하며, 에러를 수신한 프로듀서는 메세지 쓰기를 포기하고 에러를 반환하기 전에 몇번 더 재전송을 시도할 수 있다.

## Constructing a Kafka Producer

`ProducerRecord` 의 메세지를 카프카에 쓰려면 제일 먼저 프로듀서의 기능을 수행하는 객체를 생성해야한다. 이때 이 객체의 우리가 원하는 구성을 속성으로 설정한다. Kafka 프로듀서 객체는 다음 3개의 필수 속성을 가진다.

### bootstrap.servers

Kafka 클러스터에 최초로 연결하기 위해 프로듀서가 사용하는 브로커들의 `host:port` 목록을 이 속성에 설정한다. 단, 모든 브로커의 `host:port` 를 포함할 필요는 없다. 그러나 최소한 2 개의 `host:port` 를 포함하는것이 좋다. 한 브로커가 중단되는 경우에도 프로듀서는 여전히 클러스터에 연결될 수 있기 때문이다.

### key.serializer // value.serializer

프로듀서가 생성하는 레코드의 메세지 키를 직렬화 하기 위해 사용되는 클래스 이름을 이 속성에 설정한다.

다음 코드에서는 새로운 프로듀서를 생성하는 방법을 보여준다.

```shell
private Properties kafkaProps = new Properties();
kafkaPropsput("bootstrap.servers", "broker1:9092, broker2:9092");

kafkaPropsput("key.serializer", 
  "org.apache.kafka.common.serialization.StringSerializer");
kafkaPropsput("value.serializer", 
  "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = 
  new KafkaProducer <String, String>(kafkaProps);
```

이처럼 원하는 구성의 속성을 설정하여 프로듀서의 실행을 제어할 수 있다.

## Sending a Message to Kafka

가장 간단한 방법이다.

```java
ProducerRecord<String, String> record = 
  new ProducerRecord<>("CustomerCountry", "Precision Products", "France");

try {
  producer.send(record);
} catch (Exception e) {
  e.printStackTrace();
}
```

`ProducerRecord` 객체를 생성하고 `send()` 메소드를 사용해서 레코드를 전송한다. 만약 에러가 발생하면 간단한 스택 기록을 출력한다.

## Sending a Message Synchronously

동기식으로 메세지를 전송하는 가장 간단한 방식이다. 이전 코드와 차이는 `ProducerRecord` 객체의 `get()` 메소드를 사용해서 카프카의 응답을 기다리게 한다.

```java
ProducerRecord<String, String> record = 
  new ProducerRecord<>("CustomerCountry", "Precision Products", "France");

try {
  producer.send(record).get();
} catch (Exception e) {
  e.printStackTrace();
}
```

## Sending a Message Asynchronously

먼저 어플리케이션과 Kafka 클러스터간의 네트워크 왕복시간(roundtrip time, RTT)을 10ms 라 가정하자. 만일 각 메세지를 전송한 후 응답을 기다리면 100개의 메세지를 전송하는데 약 1초가 걸린다. 만약, 비동기식으로 메세지를 전송하면 응답을 기다리지 않기 때문에 100개의 메세지를 전송해도 거의 시간이 소요되지 않을것이다.

하지만 메세지 전송에 실패할 경우 에러 내용을 알아야 하기 떄문에 예외를 발생시키거나, 에러 로그에 적는다.

비동기식으로 메세지를 전송하고 이때 발생할 수 있는 에러를 처리하기 위해 프로듀서에 콜백(callback)을 추가할 수 있다. 예제를 통해 보겠습니다.

```java
private class ProducerCallback implements Callback {
  @Override
  public void onCompletion(RecordMetadata recordMetadata, Exception e) {
    if (e != null) {
      e.printStackTrace();
    }
  }
}

ProducerRecord<String, String> record =
  new ProducerRecord<>("CustomerCountry", "Precision Products", "France");
producer.send(record, new ProducerCallback());
```

`send()` 메소드를 호출하여 메세지를 전송할 때 콜백 객체를 인자로 전달한다. 따라서 Kafka가 메세지를 쓴 후 응답을 반환할 때는 이 객체의 `onCompletion()` 메소드가 자동으로 호출된다. 만약 kafka가 에러를 반환하면 `onCompletion()` 메소드에서 예외를 받게된다. 예외 처리는 위 두개의 예제와 동일하다.

다음 포스트에서는 `bootstrap.servers`, `key.serialzer.value`, `value.serializer` 외에 프로듀서 구성 매개변수를 알아보겠습니다.