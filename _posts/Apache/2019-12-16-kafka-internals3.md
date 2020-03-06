---
title : Apache Kafka Internals -3-
tags :
- Request Process
- Kafka
- Apache
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Request Processing

Kafka 브로커가 하는 일은 대부분 클라이언트와 파티션 레플리카 및 컨트롤러부터 파티션 리더에게 전송되는 request 를 처리하는 것이다. Kafka 는 TCP 로 전송되는 이진 프로토콜을 갖고 있다. 클라이언트부터 브로커에 전송된 모든 요청은 항상 수신된 순서로 처리된다. 따라서 Kafka 가 메세지 큐처럼 동작할 수 있어서 저장되는 메세지의 순서가 보장된다.

모든 Request 는 다음 내용을 포함하는 표준 헤더를 갖는다.

* Request Type
  * 16 bit 정수 형식의 고유 번호다. Kafka 메세지를 쓰는 요청은 Produce 라 하며 ID 값은 0이다.
  * 메세지 요청은 Fetch라 하며 이것은 ID 값은 1이다.
* Request Version
  * 프로토콜 API 버전을 나타내는 16 bit 정숫값이다.
  * 서로 다른 프로토콜 버전을 사용하는 Kafka 클라이언트를 브로커가 처리하고 그에 맞춰 응답할 수 잇다.
* Correlation ID
  * 사용자가 지정한 32 bit 정수값이다. 
  * 이 값은 응답과 에러 로그에도 표시된다.
* Client ID
  * 사용자가 지정한 문자열 형식의 값이다.
  * NULL 값이 될 수 있다.
  * 요청을 전송한 클라이언트 어플리케이션을 식별하는 데 사용할 수 있다.
  
표준 헤더에 추가하여 요청 타입마다 서로 다른 구조의 데이터를 같이 전송한다. 예를 들어, Kafka 에 메세지를 쓰는 Produce 요청의 경우에는 토픽 이름과 파티션 ID 및 데이터 등이 포함된다.

브로커는 자신이 listening 하는 포트에 대하여 acceptor 스레드를 실행하며, 이 스레드는 연결을 생성하고 processor 스레드가 그 다음을 처리하도록 넘겨준다. processor 스레드의 개수는 우리가 구성할 수 있다. processor 스레드는 클라이언트 연결로 부터 요청을 받고, 그것을 **요청 큐(request queue)** 에 넣으며, **응답 큐(response queue)** 로부터 응답을 가져와 클라이언트에 전송하는 일을 수행한다.

가장 많이 사용되는 요청타입이다.

* 쓰기 요청(Produce request)
  * 프로듀서가 전송하며 Kafka 브로커에게 쓰려는 메세지를 포함한다.
* 읽기 요청(Fetch request)
  * Kafka 브로커로부터 메세지를 읽을 때 컨슈머와 팔로어 레플리카를 전송한다.
  
> Example 1 - Request processing inside Apache Kafka

![image](https://user-images.githubusercontent.com/44635266/70858798-2495e400-1f4c-11ea-9550-bdbe22a5b7e8.png)

쓰기 요청과 읽기 요청은 모두 파티션의 리더 레플리카에게 전솓되어야 합니다. 특정 파티션의 리더를 갖고 있지 않은 브로커가 해당 파티션의 읽기 요청을 수신할 때도 같은 에러가 발생한다. Kafka 의 클라이언트들이 쓰기와 읽기 요청을 할 때는 요천 관련 파티션의 리더를 포함하는 브로커에게 요청을 전송해야 합니다.

Kafka 클라이언트는 **메타데이터 요청(metadata request)** 이라는 요청 타입을 사용하는데, 클라이언트가 관심을 갖는 토픽 내역을 포함한다. 메타데이터 요청에 대한 서버 응답에는 토픽에 존재하는 파티션들, 파티션의 레플리카, 어떤 레플리카의 리더인지 등의 정보가 포함된다. 메타데이터 요청은 어떤 브로커에도 전송이 가능합니다. 왜냐하면 모든 브로커가 메타데이터 캐시를 갖고 있기 때문입니다.

클라이언트는 정보를 캐시에 보존한 후 각 파티션의 올바른 브로커에게 쓰기와 읽기 요청을 전송하는 데 사용한다. 또한, 메타데이터 요청을 전송하여 정보를 새로 업데이트 해야한다.

그래야지 새로운 브로커가 추가되었을때처럼 토픽 메타데이터가 변경된 것을 알 수 있기 때문입니다.

> Example 2 - Client routing requests

![image](https://user-images.githubusercontent.com/44635266/70858867-79862a00-1f4d-11ea-98dc-4c0586158f65.png)

## Produce Requests

ack 구성 매개변수에는 메세지를 수신해야 하는 브로커의 수를 설정하며, 설정된 값의 브로커가 모두 메세지를 수신해야 쓰기 성공으로 간주한다. 프로듀서의 acks 매개변수는 다음 세 가지 중 하나로 설정할 수 있다.

* acks = 0
  * 브로커의 수신 응답을 기다리지 않음
* acks = 1
  * 리더만 메세지를 수신하면 됨
* acks = all
  * 모든 레플리카 메세지를 받아야함
  

특정 파티션의 리더 레플리카를 포함하는 브로커가 해당 파티션의 **쓰기 요청(Producer Request)** 을 받으면 다음 사항의 검사를 시작합니다.

1. 데이터를 전송한 하용자가 해당 토픽의 권한이 있나
2. 해당 요청에 지정된 acks 값
3. acks=all 인 경우 메세지를 안전하게 쓰는 데 충분한 동기화 레플리카들이 있나

파티션 리더에 메세지를 쓰면 브로커는 acks 매개변수를 확인하여 0 또는 1 이면 즉시 응답을 전송합니다. all 이면 팔로어 레플리카들이 해당 메세지를 복제했는지 리더가 확인할 때까지 **퍼거토리(purgatory)** 라고 하는 버퍼에 해당 요청을 저장한다.

## Fetch Requests

브로커는 쓰기 요청을 처리하는 방버과 매우 유사하게 **읽기 요청(Fetch Request)** 을 처리한다.클라이언트는 읽기를 원하는 토픽과 파티션 및 오프셋에 있는 메세지들의 읽기 요청을 브로커에게 전송한다.

클라이언트는 각 파티션마다 브로커가 반환할 수 있는 데이터 크기를 제한할 수 있다. 클라이언트는 브로커가 전송한 응답을 저장하는 메모리를 할당해야 하므로 크기 제한이 중요합니다.

각 요청은 파티션 리더에게 전송이 되어야 합니다. 읽기 요청이 올바르게 전송되도록 클라이언트는 메타데이터 요청을 합니다. 리더는 요청을 받은 후 적합한지 검사 후 응답합니다.

요청이 적합하면 클라이언트가 요청에 지정한 제한 크기까지의 메세지들을 브로커가 해당 파티션에서 읽은 후 클라이언트에게 전송합니다. 카프카는 **제로 카피(zero-copy)** 기법을 사용해서 클라이언트에게 메세지를 전송합니다.

Kafka 는 파일의 메세지를 중간 버퍼 메모리에 쓰지 않고 곧바로 네트워크 채널로 전송합니다. 데이터를 클라이언트에게 전송하기 전에 로컬 캐시 메모리에 저장하는 대부분의 데이터베이스와 다르다. 제로카피 기법은 메모리부터 데이터를 복사하고 버퍼를 관리하는 부담을 제거하므로 성능이 훨씬 더 향상된다.

브로커가 반환할 수 있는 데이터의 상한 크기를 설정하는 것과 더불어, 클라이언트는 반환 데이터의 하한 크기도 설정할 수 있습니다.

이를 통하여 클라이언트와 브로커 간에 데이터를 주고받는 횟수가 줄어들어 부담이 줄어준다.

> Example 3 - Broker delaying response until enough data accumulated

![image](https://user-images.githubusercontent.com/44635266/70859137-07fcaa80-1f52-11ea-9c89-1097dc3ad8a9.png)

파티션 리더에 존재하는 모든 데이터를 클라이언트가 읽을 수 있는것은 아니다. 대부분의 클라이언트는 동기화 레플리카에 쓴 메세지들만 읽을 수 있습니다. 그리고 파티션 리더는 어떤 메세지들이 어느 레플리카에 복제되었는지 알고있으며, 모든동기화 레플리카들이 메세지들을 쓸때까지 컨슈머에게 전송되지 않습니다.

레플리카에 복제되지 않은 메세지들은 '불안전한' 것으로 간주하기 때문에 위와같이 합니다. 리더가 중단되어도 다른 레플리카 리더가 선출되면, 모든 레플리카에 복제되지 않은 메세지들은 더 이상 Kafka 에 존재하지 않게됩니다. 또한 리더에만 존재하는 메세지들을 클라이언트가 읽게하면 일관성이 결여될 수 있습니다.

예를 들어 컨슈머가 아직 복제되지 않은 메세지를 읽은 후 리더가 중단이되면, 해당 메세지를 갖는 브로커가 없으므로 그 메세지는 사라집니다. 그리고 다른 컨슈머들도 그 메세지를 읽을 수 없어 컨슈머의 일관성이 결여됩니다.

따라서 `Example 4` 와 같이 모든 동기화 레플리카가 해당 메세지를 복제할ㄷ 때까지 기다렸다가 복제된 다음 컨슈머가 읽게 하는것이다.

> Example 4 - Consumers only see messages that were replicated to in-sync replicas

![image](https://user-images.githubusercontent.com/44635266/70859140-0e8b2200-1f52-11ea-9ea8-53705691c275.png)

