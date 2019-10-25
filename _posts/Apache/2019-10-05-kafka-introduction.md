---
title : Apache Kafka Introduction
tags :
- Kafka
---

## Apache Kafka

![스크린샷 2019-10-02 오후 4 06 39](https://user-images.githubusercontent.com/44635266/66056360-f2dac700-e571-11e9-9758-2abb8105fc29.png)


아파치 카프카(Apache Kafka)는 아파치 소프트웨어 재단이 스칼라로 개발한 오픈 소스 메시지 브로커 프로젝트이다. 이 프로젝트는 실시간 데이터 피드를 관리하기 위해 통일된, 높은 스루풋의 낮은 레이턴시를 지닌 플랫폼을 제공하는 것이 목표이다. 
분산환경에 특화되어 설계되어 있다는 특징을 가짐으로써, 기존의 RabbitMQ와 같은 다른 메세지큐와의 성능 차이가 난다(훨씬 빠르게 처리한다). 그 외에도 클러스터 구성, fail-over, replication와 같은 여러 가지 특징들을 가지고 있다.


## Kafka Architecture

Kafka는 발행-구독(publish/subscribe) 모델을 기반으로 동작하며 크게 producer, consumer, broker로 구성된다.

[스크린샷 2019-10-02 오후 4 07 51](https://user-images.githubusercontent.com/44635266/66056393-fbcb9880-e571-11e9-905d-c71b612ddc63.png)

Kafka의 Broker는 topic을 기준으로 메시지를 관리한다. Producer는 특정 topic의 메시지를 생성한 뒤 해당 메시지를 broker에 전달한다. Broker가 전달받은 메시지를 topic별로 분류하여 쌓아놓으면, 해당 topic을 구독하는 Consumer들이 메시지를 가져가서 처리하게 된다. 이때 Consumer가 Broker로 부터 메세지를 직접 가져가는 PULL 방식으로 동작하기 때문에 Consumer의 처리 능력만큼 메세지를 가져와 최적의 성능을 낼 수 있다.

아래 그림은 Producer 와 Consumer의 성능을 다른 시스템과 비교한것이다.

![스크린샷 2019-10-03 오전 12 12 33](https://user-images.githubusercontent.com/44635266/66056712-857b6600-e572-11e9-99af-5ad6e19ea126.png)

Kafka는 확장성(scale-out)과 고가용성(high availability)을 위하여 Broker들이 클러스터로 구성되어 동작하도록 설계되어있다. 심지어 1개 밖에 없을 때에도 클러스터로써 동작한다. 클러스터 내의 Broker에 대한 분산 처리는 아래의 그림과 같이 `Apache ZooKeeper`가 담당한다.

[스크린샷 2019-10-02 오후 4 52 05](https://user-images.githubusercontent.com/44635266/66056397-fd955c00-e571-11e9-9ef1-9557898e710f.png)

---

[스크린샷 2019-10-02 오후 4 06 47](https://user-images.githubusercontent.com/44635266/66056412-02f2a680-e572-11e9-86db-6c81cb177b01.png)

### Topic / Partition

카프카에 저장되는 메시지는 topic으로 분류되고, topic은 여러개의 patition으로 나눠질수 있다. partition안에는 message의 상대적 위치를 내타내는 offset이 있는데 이 offet정보를 이용해 이전에 가져간 메시지의 위치 정보를 알 수 있고 동시에 들어오는 많은 데이터를 여러개의 파티션에 나누어 저장하기 때문에 병렬로 빠르게 처리할 수 있다.

위 그림에서는 Writes 가 Producer라고 생각하면된다.

[스크린샷 2019-10-02 오후 4 06 53](https://user-images.githubusercontent.com/44635266/66056413-02f2a680-e572-11e9-99ba-2e876dad5403.png)

아래의 그림은 Partition 개수 4에 10개의 데이터를 넣었을때 나오는 결과값이다.

[스크린샷 2019-10-03 오전 12 37 14](https://user-images.githubusercontent.com/44635266/66058988-43542380-e576-11e9-9edd-d6d55b93742d.png)

데이터 1, 2, 3, 4 가 Offset 0 다음에 나오는 5, 6, 7, 8 이 Offset 1 을 받는식으로 결과가 나왓다. 순서가 중요한 금융 시스템 같은 경우에는 파티션을 한개로만 사용해야한다. 이 결과는 추후 포스팅으로 다시 정리하겠습니다.

### Producer / Consumer

`Producer` 는 말 그대로 메세지를 만들어서(Write) 보내는 주체이다. 메세지를 만들고 Topic에 메세지를 쓴다. 특정 메세지들을 분류해서 특정 파티션에 저장하고 싶다면, key 값을 통해서 분류해서 넣을 수 있다. 

`Consumer`는 메세지를 소비(Read)하는 주체이다. topic을 구독하여 메세지를 소비한다. 소비를 했다는 표시는 해당 topic내의 각 파티션에 존재하는 offset의 위치를 통해서 이전에 소비했던 offset위치를 기억하고 관리하고 이를 통해서, 혹시나 Consumer가 죽었다가 다시 살아나도, 전에 마지막으로 읽었던 위치에서 부터 다시 읽어들일 수 있다. 그렇기 때문에 fail-over에 대한 신뢰가 존재한다.

### Consumer Group

producer에서 생산(Write)한 메시지는 여러개의 파티션에 저장을 하는데, 그렇다면 소비하는(consumer)하는 쪽에서도 여러 소비자가 메시지를 읽어가는것이 훨씬 효율적일 것이다. 하나의 목표를 위해 소비를 하는 그룹, 즉 하나의 topic을 읽어가기 위한 consumer들을 consumer group라고 한다.
consumer group을 구성하는 consumer의 수가 partition의 수보다 작으면 하나의 consumer가 여러 개의 partition을 소유하게 되고, 반대로 consumer의 수가 partition의 수보다 많으면 여분의 consumer는 메시지를 처리하지 않게되므로 partition 개수와 consumer 수의 적절한 설정이 필요하다.

[스크린샷 2019-10-02 오후 4 06 58](https://user-images.githubusercontent.com/44635266/66056419-06862d80-e572-11e9-9e47-ce1f0ac14c82.png)

위의 그림과 같이 consumer group에 다수의 consumer를 할당하면 각 consumer마다 별도의 partition으로부터 메시지를 받아오기 때문에, (producer가 각 partition에 메시지를 균등하게 분배한다고 가정할 경우) consumer group은 큐 모델로 동작하게 된다.
단일 consumer로 이루어진 consumer group을 활용하면 다수의 consumer가 동일한 partition에 동시에 접근하여 동일한 메시지를 액세스하기 때문에 발행-구독 모델을 구성할 수 있다.
그러나 다른 partition에 속한 메시지의 순차적 처리는 보장되어 있지 않기 때문에, 특정 topic의 전체 메시지가 발생 시간 순으로 처리되어야 할 경우 해당 topic이 하나의 partition만을 가지도록 설정해야 한다.

### Broker

broker는 카프카의 서버를 칭한다. broker.id=1..n으로 함으로써 동일한 노드내에서 여러개의 broker서버를 띄울 수도 있다. 

### Zookeeper

Zookeeper는 분산 코디네이션 시스템입니다. Kafka broker를 하나의 클러스터로 코디네이팅하는 역할을 하며 나중에 이야기할 kafka 클러스터의 리더(Leader)를 발탁하는 방식도 zookeeper가 제공하는 기능을 이용합니다.

## 파일 시스템을 활용한 고성능 디자인

Kafka는 기존 메시징 시스템과는 달리 메시지를 메모리대신 파일 시스템에 쌓아두고 관리한다.

기존 메시징 시스템에서는 파일 시스템은 메시지의 영속성을 위해서 성능 저하를 감수하면서도 어쩔 수 없이 사용해야하는 애물단지 같은 존재였다. 그러나 Kafka는 이런 편견을 깨고 파일 시스템을 메시지의 주 저장소로 사용하면서도 기존의 메시징 시스템보다 뛰어난 성능을 보여준다.

![image](https://user-images.githubusercontent.com/44635266/67582057-07cb0480-f784-11e9-8984-0fe349860317.png)

일반적으로 하드디스크는 메모리보다 수백-수천 배 이상 느리다. 그러나 특정 조건에서는 메모리보다 10배 이내로 느리거나 심지어는 빠를 수도 있다. ACM Queue에 게재된 The Pathologies of Big Data라는 글에 따르면 하드디스크의 순차적 읽기 성능은 메모리에 대한 랜덤 읽기 성능보다 뛰어나며 메모리의 순차적 읽기 성능보다 7배 정도 느리다.

![image](https://user-images.githubusercontent.com/44635266/67582060-08fc3180-f784-11e9-940f-76648182b588.png)

Kafka는 메모리에 별도의 캐시를 구현하지 않고 OS의 페이지 캐시에 이를 모두 위임한다. OS가 알아서 서버의 유휴 메모리를 페이지 캐시로 활용하여 앞으로 필요할 것으로 예상되는 메시지들을 미리 읽어들여(readahead) 디스크 읽기 성능을 향상 시킨다.

Kafka의 메시지는 하드디스크로부터 순차적으로 읽혀지기 때문에 하드디스크의 랜덤 읽기 성능에 대한 단점을 보완함과 동시에 OS 페이지 캐시를 효과적으로 활용할 수 있다.

Kafka에서는 파일 시스템에 저장된 메시지를 네트워크를 통해 consumer에게 전송할 때 zero-copy기법을 사용하여 데이터 전송 성능을 향상시켰다.

일반적으로 파일 시스템에 저장된 데이터를 네트워크로 전송할 땐 위와 같이 커널모드와 유저모드 간의 데이터 복사가 발생하게 된다.

![image](https://user-images.githubusercontent.com/44635266/67582064-0a2d5e80-f784-11e9-9597-9d3ac4fe7939.png)

유저모드로 카피된 데이터를 어플리케이션에서 처리한 뒤 처리된 데이터를 네트워크로 전송한다면 위의 그림과 같이 커널모드와 유저모드 간의 데이터 복사는 당연히 필요하다. 그러나 어플리케이션에서의 별도 처리 없이 파일 시스템에 저장된 데이터 그대로 네트워크로 전송만 한다면 커널모드와 유저모드 간의 데이터 복사는 불필요한 것이 된다.

Zero-copy 기법을 사용하면 위에서 언급한 커널모드와 유저모드 간의 불필요한 데이터 복사를 피할 수 있다. 이 기법을 사용하면 아래와 같이 파일 시스템의 데이터가 유저모드를 거치지 않고 곧바로 네트워크로 전송된다. 벤치마크 결과에 따르면 zero-copy를 사용한 경우가 그렇지 않은 경우보다 전송 속도가 2-4배 빠른 것으로 나타났다.

> Zero-Copy

Zero Copy는 디스크에서 소켓으로 데이터를 복사할때 커널레벨에서 데이터를 복사하는 방식으로 
CPU 사용율과 메모리 대역폭 사용도 줄이고 커널모드와 사용자모드간 컨텍스트 전환 비용도 줄일수 있기 때문에 성능이 좋아진다.

자바는 java.nio.channels.FileChannel.transperTo() 메소드를 통해 Zero Copy를 제공한다.
