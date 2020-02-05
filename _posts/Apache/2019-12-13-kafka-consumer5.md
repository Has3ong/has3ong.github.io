---
title : Apache Kafka Consumer -5-
tags :
- Consumer
- Kafka
- Apache
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

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