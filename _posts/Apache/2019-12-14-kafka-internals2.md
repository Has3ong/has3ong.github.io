---
title : Apache Kafka Internals -2-
tags :
- ISR
- Replica
- Kafka
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*


## Replication

**복제(Replication)** 은 Kafka 아키텍처의 핵심 입니다. 복제를 이용하여 서버 노드에 장애가 생길 때 Kafka 가 가용성과 내구성을 보장하는 방법입니다.

Kafka 는 데이터 토픽으로 구성되며, 각 토픽은 여러 파티션에 저장될 수 있다. 또한, 각 파티션은 다수의 리플리카를 가질 수 있습니다. 그리고 각 브로커는 서로 다른 토픽과 파티션에 속하는 수 백개의 복제본을 저장합니다.

### *Leader replica*

파티션은 리더로 지정된 하나의 리플리카를 갖는다. 일관성을 보장하기 위해 모든 프로듀서와 컨슈머의 클라이언트의 요청은 리더를 통해서 처리된다.

### *Follower replica*

각 파티션의 리더를 제외한 나머지 리플리카를 팔로워라고 한다. 팔로워는 클라이언트 요청을 서비스하지 않는다. 대신에 리더의 메세지를 복제하여 동일하게 유지한다. 그리고 특정 파티션의 리더 리플리카가 중단된 경우에 팔로워 리플리카 중 하나가 새로운 리더로 선출이됩니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/70807005-ee4b4e00-1dff-11ea-8683-61128c5d0b17.png)

리더는 팔로어 리플리카 중에 어느 것이 최신의 리더 메세지를 복제하는지 알아야한다. 팔로워들은 리더가 받는 모든 최신 메세지를 복제하려고 한다. 그러나 여러가지 이유로 동기화에 실패할 수도 있음.

리더와 동기화를 하기 위해 레플리카들은 리더에게 Fetch 요청을 전송합니다. 이것은 컨슈머가 메세지를 읽기 위해 전송하는 것과 같은 타입의 요청이다. 그리고 그런 요청의 응답으로 리더는 레플리카들에게 메세지를 전송합니다. Fetch 요청에 레플리카가 다음으로 받기 원하는 메세지의 오프셋이 포함되며, 항상 수신된 순서대로 처리가된다.

팔로어 레플리카가 요청한 마지막 오프셋을 살펴보면 복제가 얼마나 지연되고 있는지 리더가 알 수 있다. 만약 팔로어 레플리카가 10초 이상 메세지를 복제하지 못했다면, 해당 레플리카는 **동기화되지 않는것(out-sync)** 으로 간주가 됩니다. 이처럼 팔로어 레플리카가 리더를 복제하는 데 실패하면, 리더에 장애가 생겼을 때 해당 레플리카는 더 이상 새로운 리더가 될 수 없다.

이와는 반대로, 최신 메세지를 계속 요청하는 팔로어 레플리카를 **동기화 리플리카(in-sync-replica, ISR)** 라고 한다. 기존 리더가 중단되는 경우 동기화 레플리카만이 리더로 선출될 수 있다.

동기화되지 않는다고 간주되기 전에, 팔로어가 비활성 상태가 될 수 있는 지연 시간은 replica.lag.time.max.ms 매개변수로 제어할 수 있습니다.

### Preferred Leader

현재 리더에 추가하여 각 파티션은 선호 리더를 갖게된다. 이것은 토픽이 생성될 때 각 파티션의 리더엿던 레플리카들을 말합니다. 하나의 토픽은 여러 개의 파티션으로 구성 될 수 있으며, 파티션들을 처음 생성할 때는 여러 브로커가 고르게 파티션을 할당받아 리더가 되므로 이것이 선호되는 리더들이라고 합니다.

결론적으로 선호 리더들이 클러스터의 모든 파티션 리더들일 때는 브로커 간의 파티션 배분이 고르게 됩니다. Kafka 는 `auto.leader.rebalance.enable=true` 로 구성되며 선호 리더 레플리카가 현재 리더가 아닐 경우 동기화 레플리카인지 확인하며, 리더를 선출할 때 선호 리더를 현재 리더로 선출하게됩니다.

## ISR(In Sync Replica)

ISR 에 대해서 좀 더 자세히 알아보겠습니다.

토픽의 매개 변수중 `replication.factor` 라는게 있습니다. 이를 조정하여 replication 의 개수를 관리할 수 있습니다. 예제에서는 `topic1` 은 2로 설정하고 `topic2` 는 3으로 설정해 보겠습니다. 그러면 아래의 그림처럼 그려집니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/70806764-62d1bd00-1dff-11ea-9559-7336954f51dd.png)

여기서 ISR 이란 replication group이라고 생각하시면 될 것 같습니다. 위에서 replication factor를 설명드리면서, 복제본의 수를 2와 3으로 늘렸는데요 각각의 replication group이 바로 ISR입니다. 그림으로 설명드리겠습니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/70806768-649b8080-1dff-11ea-943d-ced8686f95f0.png)

또한, ISR 내에선 누구나 leader / follower 가 될 수 있습니다. 그림에서는 임의로 정했지만 누구나가 될 수 있습니다. 이 상황에서 Broker 1 이 down 됐다고 가정해보겠습니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/70806770-65ccad80-1dff-11ea-9972-2e44572172b8.png)

Broker 1 이 down 되면 ISR 내에 leader 가 없고 follower 가 아직 1개 남아있으니 follower 가 leader 로 변합니다. 추가적으로 Broker 2 도 down 이 되었다고 가정해보겠습니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/70806777-67967100-1dff-11ea-949a-f5c761002c45.png)

topic1의 경우 ISR 내 더 이상 남아 있는 follower가 없기 때문에 leader를 넘겨줄 수 없는 상황이 되었고, topic01는 leader가 없기 때문에 더 이상 read/write를 할 수 없습니다. 즉, topic01의 경우는 read/write가 불가능한 장애 상황이 된 것입니다. topic02의 경우 topic01과 달리 ISR 내 남아 있는 follower가 하나 있기 때문에 new leader로 변경되고, new leader를 통해 read/write가 가능합니다.

그럼 leader 와 follower 가 어떻게 작동하는지 알아보겠습니다.

먼저 leader의 입장에서 보겠습니다. leader는 ISR 내 follower들을 감시하고 자신보다 뒤처지는 follower는 leader가 될 자격이 없다고 판단하여, ISR에서 강제로 제외시키게 됩니다. 추가로 설명을 드리면, broker가 down 되는 경우 ISR 내 follower는 leader로부터 데이터를 가져오지 못하게 되고, 이러한 상황이 일정 시간 지속되면서 leader는 해당 follower가 뒤쳐졌기 때문에 해당 follower에게 leader를 넘길 수 없다고 판단하여, 해당 follower를 제외시키게 되고 ISR이 축소되는 것입니다.

이번에는 반대로, follower 입장에서 보겠습니다. ISR 내 follower는 누구라도 leader가 될 수 있다는 조건이 있기 때문에 follower는 leader와 동일한 데이터를 유지하는 것이 매우 중요합니다. 따라서 follower는 leader를 계속 바라보면서 consumer들이 Kafka 에서 데이터를 pull로 가져는 것과 동일한 방법으로 주기적으로 데이터를 pull 합니다. 매우 짧은 주기마다 leader가 새로운 데이터를 받았는지 계속 체크하면서 leader와 동기화를 하게 됩니다.

결국 동일한 ISR 내에서 leader와 follower는 데이터 정합성을 맞추기 위해 각자의 방식으로 서로를 계속 체크하고 있는 것입니다.