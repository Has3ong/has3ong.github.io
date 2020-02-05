---
title : Apache Kafka Consumer -4-
tags :
- Consumer
- Kafka
- Apache
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

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
2. subscribe() 메소드를 호출할 때 RebalanceListener 인터페이스를 구현한 객체를 인자로 전달한다.

### Consuming Records with Specific Offsets

지금까지는 각 파티션의 마지막 커밋 오프셋부터 메세지를 읽고 처리하기 위해 poll() 메소드를 활용했습니다. 하지만, 다른 오프셋부터 읽기 시작하길 원할 때도 있습니다.

파티션의 맨 앞 오프셋부터 모든 메세지를 읽거나 파티션의 제일 끝 오프셋을 찾은 후 이후에 추가되는 메세지만 읽기 시작할때는 KafkaConsumer 클래스의 `seekToBeginning(Collection<TopicPartition> tp)` 와 `(seekToEnd(Collection<TopicPartition> tp)` 메소드를 사용할 수 있다.

Kafka에서 데이터를 처리한 후에 데이터 결과를 데이터베이스나 Hadoop에 저장할 때 어떤 데이터도 누락시키지 않아야 하고, 중복 저장되지 않게 해야한다고 가정해보겠습니다.

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

위 코드는 각 레코드를 처리할 때마다 오프셋을 커밋을 한다. 이렇게 하면 레코드는 데이터베이스에 확실하게 저장이 되지만 해당 레코드가 다시 처리되어 중복 데이터가 발생할 수 있습니다.

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

위 코드는 **ConsumerRebalanceListener** 와 `seek()` 를 사용해서 데이터베이스에 저장된 오프셋부터 처리하도록 한다.

1. `commitDBTransaction()` 메소드를 이용하여 데이터베이스 트랜잭션으로 오프셋을 커밋합니다. 리밸런싱이 시작되면 컨슈머가 현재 소비하던 파티션을 잃게 되므로 그 전에 오프셋을 저장해야 합니다.
2. `getOffsetFromDB(partition)` 에서는 데이터베이스에 저장된 오프셋을 가져오며, `seek()` 를 호출하여 새로 할당된 파티션의 오프셋들을 찾습니다.
3. 컨슈머를 처음 시작할 때 토픽 구독 요청 후 `poll()` 을 호출하여 컨슈머 그룹에 합류하고 파티션을 할당 받는다. 다음 `seek()` 메소드를 호출하여 할당된 파티션들의 오프셋을 찾는다.
4. `processRecord(record)` 는 데이터를 처리하며 `storeRecordInDB(record)` 는 데이터베이스에 데이터를 저장한다. 마지막으로 `storeOffsetInDB(record.topic(), record.partition(), record.offset());` 는 오프셋을 데이터베이스에 저장한다.

외부 저장소에 오프셋과 데이터를 저장하는 방법은 많습니다. 하지만, 오프셋이 저장되어 컨슈머가 그 오프셋으로부터 메세지를 읽을 수 있게 하려면, 모든 방법에서 ConsumerRebalanceListenr 와 seek() 를 사용해야 합니다.

### But How Do We Exit?

컨슈머는 스레드로 동작하며 무한 폴링루프를 실행합니다. 이 폴링 루프를 벗어나서 컨슈머를 종료시키는 방법을 알아보겠습니다.

폴링 루프를 벗어나 컨슈머 스레드가 정상적으로 종료되도록 하기 위해선 또 다른 스레드에서 KafkaConsumer 객체의 `wakeup()` 메소드를 호출해야 합니다. `wakeup()` 메소드를 호출하면 **WakeupException** 예외를 발생시켜 `poll()` 메소드가 중단됩니다.

하지만 컨슈머 스레드가 종료하기 전에는 반드시 `close()` 메소드를 호출하여 닫아야한다. 이 메소드에서는 필요하면 오프셋이 커밋되며, 현재의 컨수머가 그룹을 떠난다는 메세지가 GroupCoordinator 에게 전송된다. 그러면 세션은 타임아웃을 기다리지 않고 GroupCoordinator 는 곧바로 리밸런싱을 시작시키며, 현재의 컨슈머에게 할당된 파티션들이 그룹의 다른 컨슈머에게 재할당된다.

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