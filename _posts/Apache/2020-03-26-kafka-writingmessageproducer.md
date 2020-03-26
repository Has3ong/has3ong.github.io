---
title : Kafka Producers - Writing Messages to Kafka
tags :
- Serializer
- Producer
- Apache
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Producer Overview 

어플리케이션에서 Kafka 에 메세지를 쓰는 이유는 다양합니다. 향후 분석을 위한 웹 사이트의 사용자 활동 수집, 성능이나 상태를 모니터링하기 위한 메트릭 데이터 기록, 등등 다양합니다.

이처럼 서로 다른 용도와 요구사항은 Kafka 에 메세지를 쓰는 프로듀서 API 를 사용하는 방법과 구성에 영향을 줍니다.

프로듀서 API 는 간단하다. 그러나 프로듀서가 데이터를 전송할 때 내부적으로는 여러 단계로 처리된다 `Example 1`에서느 Kafka에 데이터를 전송할 때 프로듀서가 내부적으로 처리하는 작업을 보여준다.

> Example 1 - High-level overview of Kafka producer components

![image](https://user-images.githubusercontent.com/44635266/70225511-81e2a600-1792-11ea-8171-dfb658e1a6cb.png)

우선 카프카에 쓰려는 메시지를 갖는 `ProducerRecord`를 생성한다. `ProducerRecord`는 우리가 전송하기 원하는 토픽과 그것의 값을 포함해야 하며, 선택적으로 키와 파티션을 지정할 수도 있다. `ProducerRecord`를 Kafka로 전송할 때 프로듀서가 제일 먼저 하는일이 키와 값의 쌍으로 구성되는 메세지 객체들이 네트워크로 전송될 수 있도록 바이트 배열로 직렬화한다. 이것은 **직렬처리기(serializer)** 컴포넌트가 처리한다.

해당 데이터는 **파티셔너(partitioner)** 컴포넌트로 전달된다. 만일 `ProducerRecord`에 특정 파티션을 지정했다면 파티셔너는 특별한 처리를 하지 않고 지정된 파티션을 반환한다. 그러나 파티션을 지정하지 않았다면 `ProducerRecord`의 키를 기준으로 파티셔너가 하나의 파티션을 선택해준다.

그 다음에 같은 토픽과 파티션으로 전송될 레코드들을 모은 레코드 배치에 추가하며, 별개의 스레드가 개 배치를 카프카 브로커에 전송한다.

브로커는 수신된 레코드의 메세지를 처리한 후 응답을 전송한다. 이때 메세지를 성공적으로 쓰면 `RecordMetadata` 객체를 반환한다. 이 객체는 토픽, 파티션, 파티션 내부의 메세지 오프셋을 갖는다. 그러나 메세지 쓰기에 실패하면 에러를 반환하며, 에러를 수신한 프로듀서는 메세지 쓰기를 포기하고 에러를 반환하기 전에 몇번 더 재전송을 시도할 수 있다.

## Constructing a Kafka Producer 

`ProducerRecord` 의 메세지를 카프카에 쓰려면 제일 먼저 프로듀서의 기능을 수행하는 객체를 생성해야한다. 이때 이 객체의 우리가 원하는 구성을 속성으로 설정한다. Kafka 프로듀서 객체는 다음 3개의 필수 속성을 가진다.

#### bootstrap.servers

Kafka 클러스터에 최초로 연결하기 위해 프로듀서가 사용하는 브로커들의 `host:port` 목록을 이 속성에 설정한다. 단, 모든 브로커의 `host:port` 를 포함할 필요는 없다. 그러나 최소한 2 개의 `host:port` 를 포함하는것이 좋다. 한 브로커가 중단되는 경우에도 프로듀서는 여전히 클러스터에 연결될 수 있기 때문이다.

#### key.serializer

프로듀서가 생성하는 레코드의 메세지 키를 직렬화하기 위해 사용되는 클래스 이름을 이 속성에 설정합니다. Kafka 브로커는 바이트 배열로 메세지를 받습니다. 하지만 Kafka 의 프로듀서 인터페이스는 매개변수화 타입을 사용해 키와 값의 쌍으로 된 어떤 자바 객체도 전송할 수 있으므로 알기 쉬운 코드를 작성해야 합니다. 이때 객체를 바이트 배열로 변환하는 방법을 프로듀서가 알고 있어야 합니다.

`key.serializer` 에 설정하는 클래스는 `org.apache.kafka.common.serialization.Serializer` 인터페이스를 구현해야 합니다. 프로듀서는 이 클래스를 사용해서 키 객체를 바이트 배열로 직렬화합니다.

Kafka 클라이언트 패키지에는 세 가지 타입의 직렬화를 지원하는 `ByteArraySerializer`, `StringArraySerializer`, `IntegerArraySerializer` 가 포함되어 있습니다. 그리고 레코드의 키는 생략하고 값만 전송하고자 할 때도 `key.serializer` 를 설정해야 합니다.

#### value.serializer

레코드의 메세지 값을 직렬화하는 데 사용되는 클래스 이름을 이 속성에 설정합니다. 직렬화하는 방법은 `key.serializer` 와 같습니다.

다음 코드에서는 새로운 프로듀서를 생성하는 방법을 보여준다.

```shell
private Properties kafkaProps = new Properties();
kafkaProps.put("bootstrap.servers", "broker1:9092, broker2:9092");

kafkaProps.put("key.serializer", 
  "org.apache.kafka.common.serialization.StringSerializer");
kafkaProps.put("value.serializer", 
  "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = 
  new KafkaProducer <String, String> (kafkaProps);
```

이처럼 원하는 구성의 속성을 설정하여 프로듀서의 실행을 제어할 수 있다. 아파치 Kafka 에 문서에 모든 구성 옵션이 나와 있습니다.

프로듀서의 메세지 전송방법에는 다음 세 가지가 있습니다.

#### Fire-and-forget

`send()` 메서드로 메세지를 전송만 하고 성공 또는 실패 여부에 따른 후속 조치를 취하지 않는 방법이다.

Kafka 는 전송에 실패할 경우 프로듀서가 자동으로 재전송을 시도하므로 대부분의 경우에 성공적으로 메세지가 전송됩니다. 그러나 이 방법을 사용하면 일부 메세지가 유실될 수도 있습니다.

#### Synchronous send

`send()` 메소드로 메세지를 전송하면 자바의 Future 객체가 반환됩니다. 그 다음 Future 객체의 `get()` 메소드를 곧바로 호출하면 작업이 완료될 때까지 기다렸다가 브로커로부터 처리 결과가 반환되므로 `send()` 가 수행되었는지 알 수 있습니다.

#### Asynchronous send

`send()` 메소드를 호출할 때 콜백 메소드를 구현한 객체를 매개변수로 전달합니다. 이 객체에 구현된 콜백 메소드는 Kafka 브로커로부터 응답을 받을 때 자동으로 호출되므로 `send()` 가 성공적으로 수행되었는지 알 수 있습니다.

## Sending a Message to Kafka 

메세지를 전송하는 가장 간단한 방법이다.

```java
ProducerRecord<String, String> record = 
  new ProducerRecord<>("CustomerCountry", "Precision Products", "France");

try {
  producer.send(record);
} catch (Exception e) {
  e.printStackTrace();
}
```

`ProducerRecord` 객체를 생성하고 `send()` `send()` 메소드를 사용해서 레코드를 전송한다. 성공하면 `RecordMetadata` 를 반환하고, 이것을 받은 `sned()` 메소드는 자바의 Future 객체를 반환합니다. 여기서는 이 메소드의 성공 / 실패 여부를 알 수 없습니다.

메세지의 직렬화에 실패하면 `SerializationException` 에러가 발생하며, 버퍼가 가득차면 `BufferExhausted Exception` 이나 `TimeoutException` 예외가 발생합니다. 또한 메세지를 전송하는 스레드가 중단되면 `InterruptException` 이 발생합니다.

### Sending a Message Synchronously 

동기식으로 메세지를 전송하는 가장 간단한 방식이다.

```java
ProducerRecord<String, String> record = 
  new ProducerRecord<>("CustomerCountry", "Precision Products", "France");

try {
  producer.send(record).get();
} catch (Exception e) {
  e.printStackTrace();
}
```

이전 코드와 차이는 Future 객체의 `get()` 메소드를 사용해서 Kafka 의 응답을 기다리게 한다. 에러가 발생하면 예외를 발생시키고, 성공하면 `RecordMetadata` 객체를 받게되며, 이 객체를 사용해 Kafka 에 쓴 메세지의 오프셋을 알아낼 수 있습니다.

### Sending a Message Asynchronously 

먼저 어플리케이션과 Kafka 클러스터간의 **네트워크 왕복시간(roundtrip time, RTT)** 을 10ms 라 가정하자. 만일 각 메세지를 전송한 후 응답을 기다리면 100 개의 메세지를 전송하는데 약1 초가 걸린다. 만약, 비동기식으로 메세지를 전송하면 응답을 기다리지 않기 때문에 100 개의 메세지를 전송해도 거의 시간이 소요되지 않을것이다.

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

`send()` 메소드를 호출하여 메세지를 전송할 때 콜백 객체를 인자로 전달한다. 따라서 Kafka 가 메세지를 쓴 후 응답을 반환할 때는 이 객체의 `onCompletion()` 메소드가 자동으로 호출된다. 만약 Kafka 가 에러를 반환하면 `onCompletion()` 메소드에서 예외를 받게된다. 예외 처리는 위 두개의 예제와 동일하다.

## Configuring Producers 

추가로 프로듀서의 구성 매개변수를 알아보겠습니다.

#### acks

acks 매개 변수는 전송된 레코드의 수를 제어합니다. 이 매개변수는 메세지가 유실될 가능성에 큰 영항을 주며, 다음 3가지 값을 설정할 수 있습니다. 옵션에대해서 간략하게 설명하면 아래 표를 확인하시면 됩니다.

|Option|Message Loss|Speed|Description|
|:--:|:--:|:--:|:--:|
|0|High|High|프로듀서는 자신이 보낸 메시지에 대해 카프카로부터 확인을 기다리지 않습니다.|
|1|Medium|Medium|프로듀서는 자신이 보낸 메시지에 대해 카프카의 leader가 메시지를 받았는지 기다립니다.|
|all(-1)|Low|Low|프로듀서는 자신이 보낸 메시지에 대해 카프카의 leader와 follower까지 받았는지 기다립니다.|

**acks = 0**

프로듀서는 브로커의 응답을 기다리지 않습니다. 브로커가 메세지를 수신하지 못했을 경우 프로듀서는 알지 못하므로, 메세지가 유실이 됩니다.

네트워크가 지원하는 성능만큼 빨리 메세지를 전송할 수 있어서 매우 높은 처리량이 필요할 때 사용됩니다.

**acks = 1**

리더 리플리카가 메세지를 받는 순간 프로듀서는 브로커로부터 성공적으로 수신했다는 응답을 받는다. 만약 리더에서 메세지를 쓸 수 없다면, 프로듀서는 에러 응답을 받으며, 데이터 유실을 막기 위해 메세지를 다시 전송할 수 있다.

이때는 동기식이나 비동기식 중 어떤 방법으로 메세지를 전송했는가에 따라 처리량이 달라진다.

**acks = all(-1)**

동기화된 모든 리플리카가 메세지를 받으면 프로듀서가 브로커의 성공 응답을 받는다. 가장 안전한 형태다. 왜냐하면, 하나 이상의 브로커가 해당 메세지를 가지고 있으므로, 리더 리플리카에 문제가 생겨도 메세지가 유실되지 않기 때문이다.

#### buffer.memory

브로커들에게 전송될 메세지의 버퍼로 사용할 메모리의 양이다.

#### compression.type

기본적으로 메세지는 압축되지 않은 상태로 전송되지만, 이 매개변수를 설정하면 압축되어 전송한다. 예시 값중 하나로 snappy, gzip, lz4 다.

#### retries

프로듀서가 서버로부터 받는 에러는 일시적일 수 있다. 이 경우 retires 매개변수의 값을 설정하면, 메세지 전송을 포기하고 에러로 처리하기 전에 프로듀서가 메세지를 재전송하는 횟수를 제어할 수 있다.

디폴트로는 프로듀서는 각 재전송간에 100ms 동안 대기한다.

#### batch.size

같은 파티션에 쓰는 다수의 레코드가 전송될 때는 프로듀서가 그것들을 배치로 모은다. 이 매개변수는 각 배치에 사용될 메모리양을 제어한다. 그리고 해당 배치가 가득차면 그것의 모든 메세지가 전송된다.

하지만, 배치가 가득 찰 때까지 가디리는것은 아니다. 

#### linger.ms

현재의 배치를 전송하기 전까지 기다리는 시간(ms)을 나타는대. 그리고 현재의 배치가 가득 찼거나, linger.bs에 설정된 제한 시간이 되면 프로듀서가 메세지 배치를 전송한다.

#### client.id

어떤 클라이언트에서 전송된 메세지인지 식별하기 위해 브로커가 사용한다. 주로 로그 메세지와 메트릭 데이터의 전송에 사용된다.

#### max.inflight.requests.per.connection

서버의 응답을 받지 않고 프로듀서가 전송하는 메세지의 개수를 제어한다. 이 매개변수의 값을 크게 설정하면 메모리 사용량은 즈가하지만 처리량은 좋아진다.

하지만, 너무 큰 값으로 설정하면 메세지의 배치 처리가 비효율적으로 되므로 오히려 처리량이 감소할 수 있다.

#### timeout.ms, request.timeout.ms, metadata.fetch.timeout.ms

데이터를 전송할 때(request.timeout.ms) , 메타데이터를 요청할 때(metadata.fetch.timeout.ms) 프로듀서가 서버의 응답을 기다리는 제한 시간을 가진다.

timeout.ms는 동기화된 레플리카들이 메세지들을 인지하는 동안 브로커가 대기하는 시간을 제어한다.

#### max.block.ms

send() 메서드를 호출할 때 프로듀서의 전송 버퍼가 가득 차거나 사용할 수 없을 때 프로듀서가 max.block.ms의 시간동안 일시 중단된다. 그 다음에 max.block.ms의 시간이 되면 시간 경과 예외가 발생한다.

#### max.request.size

이 매개변수는 프로듀서가 전송하는 쓰기 요청의 크기를 제어한다. 전송될 수 있는 가장 큰 메세지의 크기와 프로듀서가 하나의 요청으로 전송할 수 있는 메세지의 최대 개수 모두를 이 매개변수로 제한한다.

#### receive.buffer.butes / send.buffer.bytes

데이터를 읽고 쓸 때 소켓이 사용하는 TCP 송수신 버퍼의 크기를 나타낸다. 만약 **-1**로 설정하면 운영체제의 디폴트값으로 사용된다.

## Serializers 

프로듀서의 필수 구성에는 직렬처리기가 포함된다. 카프카에서 지원하는 기본적인 String 타입의 직렬처리기와 Integer / ByteArray 타입을 위에서 살펴봤습니다. 하지만 이것들로 직렬화를 충족시킬 수 없으므로 또 다른 직렬처리기가 필요합니다.

직렬처리기를 알아본 후 Avro 직렬처리기를 살펴보겠습니다.

### Custom Serializers 

Kafka 로 전송해야 하는 객체가 단순한 문자열이나 정수가 아닐 떄는 Avro, Thrift, Protobuf 와 같은 범용 직렬화 라이브러리를 사용해 레코드를 생성하거나 사용중인 객체의 커스텀 직렬처리기를 만들 수 있습니다. 하지만, 범용 직렬화 라이브러리의 사용을 적극 권장합니다. 

먼저 커스텀 직렬처리기를 작성하는 법을 알아보겠습니다.

Custmomer 를 나타내는 클래스와 customerId 라는 식별번호와 customerName 이라는 이름을 가진 클래스를 만들겠습니다.

```java
public class Customer {
  private int customerID;
  private String customerName;

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

이 클래스의 커스텀 직렬처리기는 다음과 같이 생성할 수 있습니다.

```java
import org.apache.kafka.common.errors.SerializationException;
import java.nio.ByteBuffer;
import java.util.Map;

public class CustomerSerializer implements Serializer<Customer> {
  @Override
  public void configure(Map configs, boolean isKey) {
    // nothing to configure
  }
  
  @Override
  /**
  We are serializing Customer as:
  4 byte int representing customerId
  4 byte int representing length of customerName in UTF-8 bytes (0 if name is Null)
  N bytes representing customerName in UTF-8
  */
  public byte[] serialize(String topic, Customer data) {
    try {
       byte[] serializedName;
      int stringSize;
      if (data == null)
        return null;
      else {
        if (data.getName() != null) {
          serializeName = data.getName().getBytes("UTF-8");
          stringSize = serializedName.length;
        } else {
          serializedName = new byte[0];
          stringSize = 0;
        }
      }
    
    ByteBuffer buffer = ByteBuffer.allocate(4 + 4 + stringSize);
    buffer.putInt(data.getID());
    buffer.putInt(stringSize);
    buffer.put(serializedName);

    return buffer.array();
    } catch (Exception e) {
      throw new SerializationException(
      "Error when serializing Customer to byte[] " + e);
    }
  }

  @Override
  public void close() {
    // nothing to close
  }
}
```

이 직렬처리기를 사용할 때는 프로듀서를 구성하고 생성합니다. 그 다음에 `Producer Record<String, Customer>` 에 `Customer` 객체를 전달하여 `ProducerRecord` 객체를 생성한 후 이것을 프로듀서가 전송하면 됩니다.

이 직렬처리기에는 심각한 취약점이 있는데 새로운 필드를 추가하거나 필드 타입을 변경하면 기존 메세지와 새로운 메세지 간의 호환성 문제가 발생합니다.

이런 이유로 JSON, Avro, Thrift, Protobuf 같은 범용 직렬처리기와 역직렬처리기의 사용을 권장합니다. Avro 레코드를 직렬화하여 Kafka 에 전송해보겠습니다.

### Serializing Using Apache Avro 

Avro 는 언어 중립적인 데이터 직렬화 시스템입니다. Avro 는 독립적인 스키마로 데이터 구조를 표현하는 데 주로 JSON 형식으로 기술하며, 직렬화 역시 JSON 을 지원하지만 주로 이진 파일을 사용합니다. Avro 가 파일을 읽고 쓸 떄는 스키마가 있다고 간주합니다.

Avro 를 Kafka 와 같은 메세지 시스템에 사용하는 데 적합한 이유는 메세지를 쓰는 어플리케이션이 새로운 스키마로 전환하더라도 해당 메세지를 읽는 어플리케이션은 일체의 변경 없이 계속해서 메세지를 처리할 수 있습니다.

예를 들어, 기존 스키마가 다음과 같은 JSON 형식으로 되어 있었다고 해보겠습니다.

```json
{"namespace": "customerManagement.avro",
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "faxNumber", "type": ["null", "string"], "default": "null"}
  ]
}
```

`id` 와 `name` 은 필수 필드이며, `faxNumber` 는 생략 가능하고 기본값은 `null` 입니다.

이 스키마를 새로운 스키마로 변경하겠습니다. `faxNumber` 를 없애고 `email` 필드를 추가할 예정입니다.

```json
{"namespace": "customerManagement.avro",
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": "null"}
  ]
}
```

새로운 스키마를 사용하면 기존에 사용하던 `getFaxNumber()` 메소드를 사용했을 때 null 을 반환할 것이빈다. 또한, 구버전의 스키마를 사용해서 `getEmail()` 을 사용하면 null 을 반환합니다.

이 때 Avro 를 사용할 떄의 장점을 보여줍니다. 데이터를 읽는 모든 어플리케이션을 변경하지 않고 스키마를 변경하더라도 어떤 에러도 발생하지 않으며, 기존 데이터를 변경할 필요가 없습니다.

하지만 이런 시나리오에는 아래와 같은 두 가지 주의 사항이 있습니다.

* 데이터를 쓰는 데 사용하는 스키마와 읽는 어플리케이션에서 기대하는 스키마가 호환될 수 있어야 한다.
* 직렬화된 데이터를 원래의 형식으로 변환하는 역직렬처리기는 데이터를 쓸 떄 사용되었던 스키마를 사용해야 한다.

### Using Avro Records with Kafka 

Kafka 에서는 아키텍처 패턴에 나온 대로 스키마 레지스트리를 사용합니다. 스키마 레지스트리는 Kafka 에 포함되지 않았지만 오픈 소스에서 선택할 수 있는것들이 있습니다. 위 포스트에서는 Confluent 스키마 레지스트리를 사용하겠습니다.

Kafka 에 데이터를 쓰는 데 사용되는 모든 스키마를 레지스트리에 저장하는것이 스키마 레지스트리의 개념입니다. 그리고 Kafka 에 쓰는 레코드에는 스키마의 `id` 만 저장하면 됩니다. 그러면 컨슈머는 해당 식별자를 사용하여 스키마 레지스트리의 스미카를 가져온 후 이 스키마에 맞춰 데이터를 역직렬화 할 수 있습니다.

이때 모든 작업이 직렬처리기와 역직렬처리기에서 수행된다는 것이 중요합니다. 즉 Kafka 에 데이터를 쓰는 코드에서는 스키마 레지스트리 관련 코드를 추가하지 않고 종전처럼 직렬처리기를 사용하듯이 Avro 를 사용하면 됩니다. `Example 2` 에서는 어떻게 이런 처리가 되는지 보여줍니다.

> Example 2 - Flow diagram of serialization and deserialization of Avro records

![image](https://user-images.githubusercontent.com/44635266/70387987-514b7800-19ef-11ea-8572-bc4b7cd0f377.png)

아래는 Avro 를 사용하여 Kafka에 전송하여 쓰는 방법입니다.

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

여기서 `KafkaAvroSerializer` 를 이용해 객체를 직렬화 합니다. `schemaUrl` 는 스키마를 저장하는 곳입니다. `CustomerGenerator` 에서 생성되는 `Customer` 객체는 POJO(Plain Old Java Object) 가 아니고 Avro 에 특화된 `Customer` 클래스의 객체이며, Avro 코드 생성 기능을 사용해 스키마로부터 생성됩니다.

`ProducerRecord<>` 구문 에서 `Customer` 객체를 생성한 뒤 레코드를 전송합니다.

일반화된 Avro 객체를 사용하고 싶다면 다음과 같이 스키마를 제공하여 사용하면됩니다.

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

## Partitions 

`ProducerRecord` 객체는 토픽 이름과 키와 값을 포함합니다. Kafka 메세지는 키와 값의 쌍으로 구성되지만, 기본값이 null 로 설정된 키와 함께 토픽과 값만 가지는 `ProducerRecord` 객체를 생성할 수 있습니다.

키는 두 가지 목적으로 생성이됩니다.

1. 메세지 식별
2. 메세지를 쓰는 토픽의 파티션 결정

같은키를 가지는 모든 메세지는 같은 파티션에 저장이됩니다. 즉, 하나의 프로세스가 한 토픽의 파티션 중 일부만 읽는다면, 하나의 키로 모든 레코드를 읽을 수 있다는 의미다. 쌍으로 된 레코드를 생성할 때는 다음과 같이 ProducerRecord 객체를 생성하면 됩니다.

```java
ProducerRecord<Integer, String> record =
  new ProducerRecord<>("CustomerCountry", "Laboratory Equipment", "USA");
```

또한, 키가 없는 메세지는 다음과 같이 키를 생략하고 생성하면 됩니다.

```java
ProducerRecord<Integer, String> record =
  new ProducerRecord<>("CustomerCountry", "USA"); 
```

키가 null 이면서 카프카의 기본 파티셔너로 설정되면 사용 가능한 토픽의 파티션 중 하나가 무작위로 선택되어 해당 레코드가 저장됩니다. 파티션 선택 알고리즘은 Round-Robin 입니다.

키가 있으면서 기본 파티셔너가 사용될 때는 카프카에서 키의 해시 값을 구한 후 그 값에 따라 특정 파티션에 메세지를 저장합니다.

토픽의 파티션 개수가 변하지 않는다면, 같은 키의 데이터와 대응되는 파티션 역시 변하지 않습니다.