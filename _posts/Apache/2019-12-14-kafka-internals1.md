---
title : Apache Kafka Internals -1-
tags :
- Zookeeper
- Kafka
- Apache
---

*이 포스트는 [Kafka Definitive Guide](https://github.com/Avkash/mldl/blob/master/pages/docs/books/confluent-kafka-definitive-guide-complete.pdf)를 바탕으로 작성하였습니다.*

## Cluster Membership

Kafka에서 사용하는 Zookeeper 를 알아보겠습니다. 내부적으로 Zookeeper 는 표준 파일 시스템의 디렉토리처럼 계층적인 트리 구조로 데이터를 저장하고 사용한다. 데이터를 저장하는 노드를 znode라 하며, 각 znode 이름 앞에는 / 를 붙이고 디렉토리 경로를 사용해서 각 노드의 위치를 식별한다. 그리고 노드 관리는 Zookeeper 를 사용하는 클라이언트에서 한다.

각 노드에는 상태와 구성 정보 및 위치 정보등의 데이터만 저장이되어 크기가 **임시노드(ephermeral node)** 와 **영구노드(persistent node)** 로 구분이 된다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/70799570-593f5980-1ded-11ea-92ee-d8caa706d631.png)

임시노드는 노드를 생성한 클라이언트가 연결되어 있을 때 만 존재하며, 연결이 끊어지면 자동으로 삭제된다. 영구노드는 클라이언트가 삭제하지 않는 한 계속 보존이된다. 또한, 노드의 상태를 모니터링하는 Watch 기능이 존재한다. 즉, 클라이언트가 특정 노드의 Watch를 설정한 경우 해당 노드가 변경되면 콜백 호출을 통해 클라이언트에게 알려준다.

Kafka 에서도 Zookeeper 를 사용하여 클러스터 멤버인 브로커들의 메타데이터를 유지관리합니다. Kafka 클러스터가 사용하는 Zookeeper 의 최상위 노드가 `/kafka-main` 이라면 이 노드의 자식들로 `/kafka-main/controller`, `/kafka-main/brokers`, `/kafka-main/config`  가 생성이 됩니다.

그리고 이러한 노드 관리는 Zookeeper 를 사용하는 클라이언트에서 합니다. 예를들어, 노드 존재 여부 확인, 데이터 읽기 쓰기 등등

아래 `Example 2` 은 자식 노드들의 경로를 만든 예시 입니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/70797940-019eef00-1de9-11ea-9242-35cb376dd9c2.png)

각각 노드마다 저장하는 데이터가 다릅니다.`/kafka-main/controller` 에는 카프카 클러스터의 정보가 저장됩니다. `/kafka-main/brokers` 에는 브로커 관련 정보가 저장이 됩니다. `/kafka-main/config` 에는 토픽의 설정 정보가 저장이 됩니다.

모든 Kafka 브로커는 고유 식별자를 가지며, 이것은 브로커의 구성 파일에 설정되거나 자동으로 생성된다. 브로커 프로세스는 시작될때마다 Zookeeper 의 `/brokers/id` 에 임시 노드로 자신의 id를 등록합니다. 만일 중복되는 id를 가지는 브로커를 시작하려고하면 오류가 발생합니다.

그리고 브로커가 추가 혹은 삭제되거나 Zookeeper 와 연결이 끊어지면, 해당 브로커가 시작될 때 생성되었던 임시 노드는 자동으로 Zookeeper 에서 삭제됩니다.

## The Controller

컨트롤러는 카프카 브로커 중 하나이며, 일반 브로커의 기능에 추가하여 파티션 리더(Leader) 를 선출하는 책임을 갖는다. 클러스터에서 시작하는 첫 번째 브로커가 컨트롤러가 되며, 이 브로커는 Zookeeper 의 임시 노드인 `/controller` 를 생성한다. 그리고 다른 브로커들이 시작될 때도 `/controller` 를 생성하려고 시도한다. 그러나  *노드가 이미 존재한다* 라는 예외를 받으므로, `/controller` 노드가 있고 클러스터에도 컨트롤러가 있다는것을 알게되어 모든 브로커들은 `/controller` 노드에 Zookeeper 의 Watch 를 생성하여 이 노드에 변경이 생기는 것을 알 수 있다. 이런 방법을 통해 클러스터에는 항상 하나의 컨트롤러만 존재한다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/70804620-48491500-1dfa-11ea-9b5b-9351b736e749.png)

컨트롤러 브로커가 중단되거나 Zookeeper 와의 연결이 끊어지면 임시 노드인 `/controller` 가 삭제가 됩니다. 이때 해당 클러스터의 다른 브로커들이 주키퍼의 Watch를 통해 그 사실을 알게되고 `/controller` 노드의 생성을 시도합니다. 그리고 그 노드를 첫 번째로 생성한 브로커가 컨트롤러가 됩니다.

컨트롤러는 매번 선출될 때마다 Zookeeper 로부터 새로운 컨트롤러 세대 번호를 받으며, 나머지 브로커들은 현재의 컨트롤러 세대 번호를 알게됩니다. 따라서 변경 전의 컨트롤러 번호의 메세지는 받게되면 무시하게됩니다.

관련 Zookeeper 경로를 Watch 하여 특정 브로커가 클러스터를 떠났다는 것을 컨트롤러가 인지하면 브로커가 할당되었던 모든 파티션들에 새로운 리더가 필요하다는것을 알게된다. 그 다음에 컨트롤러는 새로운 리더가 필요한 파티션들을 점검하고 새로 리더가 될 브로커를 결정합니다. 그리고 컨트롤러는 파티션들의 새로운 리더들과 팔로워 들의 정보를 모든 브로커들에게 전송을 합니다.


