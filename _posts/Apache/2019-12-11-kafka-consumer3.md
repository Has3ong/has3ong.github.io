---
title : Apache Kafka Consumer -3-
tags :
- Offset
- Commit
- Consumer
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Commits and Offsets

poll() 메서드를 호출될 때마다 그룹의 컨슈머들이 아직 읽지 않은 레코드들을 반환한다. 즉, 그룹의 각 컨슈머가 읽은 레코드들을 추적 및 관리하는 방법이 있다. Kafka의 컨슈머는 파티션별로 자신이 있는 레코드의 현재 위치(Offset)을 추적 관리할 수 있습니다.

파티션 내부의 현재 위치를 변경하는 것을 커밋(Commit) 이라고 합니다.

기존의 컨슈머가 비정상적으로 종료가 되거나, 새로운 컨슈머가 컨슈머 그룹에 추가가 된다면 오프셋 커밋은 **리밸런싱을 유발한다**. 그리고 리밸런싱이 끝나면 각 컨슈머는 종전과 다른 파티션들을 할당받게 된다. 따라서 어느 위치 부터 메세지를 읽어야 할지 알기 위해 컨슈머는 각 파티션의 마지막으로 커밋된 오프셋을 알아낸 후 해당 오프셋부터 계속 읽어나간다.

`Example 1` 경우 마지막으로 커밋된 오프셋이 컨슈머가 가장 최근에 읽고 처리한 메세지의 오프셋보다 작으면 메세지들이 두 번 처리가 된다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/70606302-80582880-1c3f-11ea-9e6b-5c612d90d7fc.png)

`Example 2` 경우 마지막으로 커밋된 오프셋이 컨슈머가 가장 최근에 읽고 처리한 메세지의 오프셋보다 크면 메세지 누락이 생길 수 있다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/70606305-81895580-1c3f-11ea-9b4d-79e2062d500e.png)

### Automatic Commit

**자동 커밋(Automatic Commit)** 은 가장 쉬운 오프셋 커밋 방법이다. KafkaConsumer 객체가 자동으로 커밋해준다. 이때 `enable.auto.commit=true`로 설정하면 poll() 메소드에서 받은 오프셋 중 가장 큰 것을 5초마다 한 번씩 커밋을 하게 된다.

자동 커밋의 기본 시간 간격은 5s 이지만, `auto.commit.interval.ms` 를 설정하여 변경이 가능합니다. 

Kafka 컨슈머의 모든것이 그렇듯이, 자동 커밋도 폴링 루프에서 처리가 됩니다.  즉, 매번 폴링할 때마다 KafkaConsumer 객체가 커밋할 시간이 되었는지 확인하며, 만일 시간이 되었다면 마지막으로 호출된 poll() 메소드에서 반환된 오프셋을 커밋합니다.

하지만, 자동 커밋을 사용할 때도 중복 처리가 되는 경우가 있습니다. 가장 최근에 커밋을 진행 한 후 3초 동안 추가로 레코드들을 읽고 처리하다가 리밸런싱이 되면 리밸런싱이 끝난 후 모든 컨슈머들은 마지막으로 커밋된 오프셋부터 레코드들을 읽게 됩니다. 이 경우 해당 오프셋은 3초 이전의 것이므로, 3초동안 읽었던 레코드는 모두 2번 처리가 됩니다.

오프셋 자동 커밋을 자주 사용하여 중복을 줄일 수 있지만 완전히 없애는것은 불가능합니다.

### Commit Current Offset

`enable.auto.commit=false` 를 설정하면 어플리케이션이 요구할 때만 오프셋이 커밋이 됩니다. 이때 가장 간단하고 신뢰도가 높은 것이 `commitSync()` 입니다. 이 메소드는 poll() 메소드에서 반환된 마지막 오프셋을 커밋합니다.

`commitSync()` 는 poll() 에서 반환된 가장 최근의 오프셋을 커밋합니다. 따라서 poll() 에서 반환된 모든 레코드의 처리가 다 된 후에 `commitSync()` 를 호출해야 합니다.

가장 최근에 메세지 배치를 처리한 후에  `commitSync()` 를 사용해서 오프셋을 커밋하는 예는 다음과 같습니다.

```java
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

```java
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

비동기 처리는 callback을 사용하여 `commitAsync()`에 전달할 수 있습니다. callback을 사용한 비동기 처리의 예는 아래 코드를 보시면 됩니다.

```java
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

```java
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

특정 오프셋을 커밋하는 경우도 있습니다. 더 자주 커밋을 하고 싶거나 poll() 메소드에서 용량이 큰 배치를 반환할 때 배치 중간의 오프셋을 커밋하여 리밸런싱으로 인한 많은 메세지의 중복처리를 막고자 할때 사용이 됩니다. 코드로 알아보겠습니다.

```java
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
      record.partition()), new
      OffsetAndMetadata(record.offset()+1, "no metadata"));
      
  if (count % 1000 == 0)
    consumer.commitAsync(currentOffsets, null);
  count++;
  }
}
```

위의 예들과는 다르게 직접 오프셋을 추적, 관리하고 파티션과 오프셋을 저장한 Map 을 인자로 사용합니다.

또한 위 코드에서는 `if (count % 1000 == 0)` 를 이용하여 100개의 레코드마다 한 번씩 현재 오프셋을 커밋하게 설정하였습니다.