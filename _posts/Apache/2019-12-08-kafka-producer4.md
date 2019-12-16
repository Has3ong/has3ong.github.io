---
title : Apache Kafka Producer -4-
tags :
- Partition
- Avro
- Serializer
- Producer
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Avro Record

Kafka에서는 아키텍처 패턴에 나온 대로 스키마 레지스트리를 사용한다. 스키마 레지스트리는 아파치 카프카에 포함되지 않았지만 오픈 소스에서 선택할 수 있는것들이 있다. 위 포스트에서는 Confluent 스키마 레지스트리를 사용하겠습니다.

Kafka에 데이터를 쓰는 데 사용되는 모든 스키마를 레지스트리에 저장하는것이 스키마 레지스트리의 개념이다. 그리고 Kafka에 쓰는 레코드에는 스키마의 id만 저장하면 된다. 그러면 컨슈머는 해당 식별자를 사용하여 스키마 레지스트리의 스미카를 가져온 후 이 스키마에 맞춰 데이터를 역직렬화 할 수 있다.

아래는 Avro 레코드의 직렬화와 역직렬화의 처리다.

> Example 1 - Flow diagram of serialization and deserialization of Avro records

![image](https://user-images.githubusercontent.com/44635266/70387987-514b7800-19ef-11ea-8572-bc4b7cd0f377.png)

아래는 Avro 를 사용하여 Kafka에 전송하여 쓰는 방법이다.

```java
Properties props = new Properties();

props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer",
  "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer",
  "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", schemaUrl);

String topic = "customerContacts";
int wait = 500;

Producer<String, Customer> producer =
  new KafkaProducer<String, Customer>(props);
  
// We keep producing new events until someone ctrl-c
while (true) {
  Customer customer = CustomerGenerator.getNext();
  System.out.println("Generated customer " +
    customer.toString());
  ProducerRecord<String, Customer> record =
    new ProducerRecord<>(topic, customer.getId(), customer);
  producer.send(record);
}
```

일반화된 Avro 객체를 사용하고 싶다면 다음과 같이 스키마를 제공하여 사용하면된다.

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer",
  "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("value.serializer",
  "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", url);

String schemaString =
        "{\"namespace\": \"customerManagement.avro\",
          \"type\": \"record\", " +
          "\"name\": \"Customer\"," +
          "\"fields\": [" +
          "{\"name\": \"id\", \"type\": \"int\"}," +
          "{\"name\": \"name\", \"type\": \"string\"}," +
          "{\"name\": \"email\", \"type\": [\"null\",\"string
          \"], \"default\":\"null\" }" +
          "]}";
          
Producer<String, GenericRecord> producer =
  new KafkaProducer<String, GenericRecord>(props);
  
Schema.Parser parser = new Schema.Parser();
Schema schema = parser.parse(schemaString);

for (int nCustomers = 0; nCustomers < customers; nCustomers++) {
  String name = "exampleCustomer" + nCustomers;
  String email = "example " + nCustomers + "@example.com"
  
  GenericRecord customer = new GenericData.Record(schema);
  customer.put("id", nCustomer);
  customer.put("name", name);
  customer.put("email", email);
  
  ProducerRecord<String, GenericRecord> data =
    new ProducerRecord<String,
      GenericRecord>("customerContacts", name, customer);
  producer.send(data);
}
```

두 코드의 가장 큰 차이는 Avro 스키마를 어떻게 제공하냐 입니다.

## Partition

앞의 예에서 보았듯이, ProducerRecord 객체는 토픽 이름과 키와 값을 포함한다. Kafka 메세지는 키와 값의 쌍으로 구성되지만 기본값이 null로 설정된 키와 함께 토픽과 값만 갖는 ProducerRecord 객체를 생성할 수도 있다.

키는 두 가지 목적으로 생성이된다.

1. 메세지 식별
2. 메세지를 쓰는 토픽의 파티션 결정

같은키를 가지는 모든 메세지는 같은 파티션에 저장이된다. 즉, 하나의 프로세스가 한 토픽의 파티션 중 일부만 읽는다면, 하나의 키로 모든 레코드를 읽을 수 있다는 의미다.

쌍으로 된 레코드를 생성할 때는 다음과 같이 ProducerRecord 객체를 생성하면 된다.

```java
ProducerRecord<Integer, String> record =
  new ProducerRecord<>("CustomerCountry", "Laboratory Equipment", "USA");
```

또한, 키가 없는 메세지는 다음과 같이 키를 생략하고 생성하면 된다.

```java
ProducerRecord<Integer, String> record =
  new ProducerRecord<>("CustomerCountry", "USA"); 
```

키가 null 이면서 카프카의 기본 파티셔너로 설정되면 사용 가능한 토픽의 파티션 중 하나가 무작위로 선택되어 해당 레코드가 저장된다. 파티션 선택 알고리즘은 Round-Robin이다.

키가 있으면서 기본 파티셔너가 사용될 때는 카프카에서 키의 해시 값을 구한 후 그 값에 따라 특정 파티션에 메세지를 저장한다.

토픽의 파티션 개수가 변하지 않는다면, 같은 키의 데이터와 대응되는 파ㅣㅌ션 역시 변하지 않는다.