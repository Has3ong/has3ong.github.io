---
title : Apache Kafka Producer -3-
tags :
- Serializer
- Producer
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## 직렬처리기, Serializers

프로듀서의 필수 구성에는 직렬처리기가 포함된다. 카프카에서 지원하는 기본적인 String 타입의 직렬처리기와 Int 타입을 [Apache Kafka Producer -1-](/kafka-producer1) 포스트에서 살펴봤습니다.

직렬처리기를 사용하는 이유를 다시 한번 얘기하자면, Kafka는 바이트 배열을 대기열에 전송하고 저장하기 때문에 프로듀서에서 브로커로 전송할 메시지를 준비하기 위해 Serializer를 사용합니다. 마찬가지로 바이트 배열을 객체로 다시 변환하기 위해 컨슈머가 Deserializer를 사용합니다.

이번 포스트에서는 Apache Avro 직렬처리기 예시를 보여드리겠습니다. 

Apache Avro는 Apache의 Hadoop 프로젝트에서 개발된 원격 프로시저 호출(RPC) 및 데이터 직렬화 프레임워크이다. 자료형과 프로토콜 정의를 위해 JSON을 사용하며 콤팩트 바이너리 포맷으로 데이터를 직렬화한다. 

주 용도는 Apache Hadoop에서 Client -> Hadoop 서비스에 대해 영구 데이터를 위한 직렬화 포맷과 Hadoop 노드 간 통신을 위한 와이어 포맷을 둘 다 제공하는 것이다.

> Example from Wikipedia

```
{
   "namespace": "example.avro",
   "type": "record",
   "name": "User",
   "fields": [
      {"name": "name", "type": "string"},
      {"name": "favorite_number",  "type": ["int", "null"]},
      {"name": "favorite_color", "type": ["string", "null"]}
   ]
 }
```

### Custom Serializers

우선 Customer를 나타내는 간단한 클래스를 정의해보겠습니다.

```
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

Customer 클래스의 간단한 직렬처리기를 만들겠습니다.

```
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
  4 byte int representing length of customerName in UTF-8 bytes (0 if name is
Null)
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
      
       ByteBuffer buffer = 
        ByteBuffer.allocate(4 + 4 + stringSize);
        
      uffer.putInt(data.getID());
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

직렬처리기를 사용할 대 두 가지 순서가 있습니다.

1. 프로듀서를 구성하고 생성한다.
2. ProducerRecord<String, Consumer>에 Customer 객체를 전달하여 객체를 생성한 후 프로듀서가 전송한다.

이 직렬처리기 코드는 간단하지만 문제점이 많습니다. 추가 확장을할 때 Customer 클래스에 필드를 추가하면 기존 메세지와의 호환성 문제가 발생합니다.

이런 이유로 JSON, Avro같은 범용 직렬처리기 사용을 권장합니다.

## Avro Serializers

Customer 클래스를 바탕으로 스키마를 JSON 형식으로 만들어보겠습니다.

```
{"namespace": "customerManagement.avro",
  "type": "record",
    "name": "Customer",
    "fields": [
      {"name": "id", "type": "int"},
      {"name": "name", "type": "string""},
    {"name": "faxNumber", "type": ["null", "string"], "default": "null"}
  ]
}
```

id 와 name 필드는 필수 필드이며,  faxNumber는 생략가능하고 디폴트가 null 이다.

현재 상황에서 faxNumber를 없애고 대신 email 필드를 추가하여 새로운 스키마를 만들려고 합니다.

그 결과 새로운 스키마는 다음과 같습니다.

```
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

이런 상황에 발생하는 문제점으로 faxNumber 레코드와 새로운 email 레코드에 getter(), setter()  함수를 사용할 때 문제가 발생할것이다.

이러한 문제점을 해결하기위해 Avro를 사용한다.

다음 포스트에서는 Avro를 활용해보겠습니다.