---
title : Zookeeper Introduction
tags:
- Apache
- Zookeeper
---

## Zookeeper

![](https://user-images.githubusercontent.com/44635266/66716447-b4ae9480-ee08-11e9-95f5-53f2e4cffdb5.png)

분산 시스템을 설계 하다보면, 가장 문제점 중의 하나가 분산된 시스템간의 정보를 어떻게 공유할것이고, 클러스터에 있는 서버들의 상태를 체크할 필요가 있으며 또한, 분산된 서버들간에 동기화를 위한 락(lock)을 처리하는 것들이 문제로 부딪히게 되는데 이러한 문제를 해결하는 시스템을 코디네이션 서비스 시스템 (coordination service)라고 하는데, Apache Zookeeper가 대표적이다.

주키퍼는(Zookeeper)는 분산 코디네이션 서비스를 제공하는 오픈소스 프로젝트입니다. 이러한 어플리케이션의 목적은 개발자가 코디네이션 로직보다는 비즈니스 핵심 로직에 집중하게끔 지원하는 역할을 합니다.

주키퍼는 Leader Follower로 구성되는 Master-Slave 아키텍처를 기반으로 구성되어 있습니다. 이것을 기반으로 여러 주키퍼 서버로 이루어진 앙상블(Ensemble), 앙상블 데이터의 불일치를 방지하고자 하는 쿼럼(Quorum) 그리고 분산 데이터 시스템인 znode로 이루어진 주키퍼 데이터 모델(zookeeper data model)이 주키퍼를 구성하게 됩니다.

## Zookeeper 기능

### 설정 관리(Configuration management)

클러스터의 설정 정보를 최신으로 유지하기 위한 조율 시스템으로 사용됩니다.

### 클러스터 관리(Cluster management)

클러스터의 서버가 추가되거나 제외될 때 그 정보를 클러스터 안 서버들이 공유하는 데 사용됩니다.

### 리더 채택(Leader selection)

다중 어플리케이션 중에서 어떤 노드를 리더로 선출할 지를 정하는 로직을 만드는 데 사용됩니다. 주로 복제된 여러 노드 중 연산이 이루어지는 하나의 노드를 택하는 데 사용됩니다.

### 락, 동기화 서비스(Locking and synchronization service) 

클러스터에 쓰기 연산이 빈번할 경우 경쟁상태에 들어갈 가능성이 커집니다. 이는 데이터 불일치를 발생시킵니다. 이 때, 클러스터 전체를 대상을 동기화해( 락을 검 ) 경쟁상태에 들어갈 경우를 사전에 방지합니다.

## Zookeeper Architecture

![](https://user-images.githubusercontent.com/44635266/66716557-e542fe00-ee09-11e9-91bd-492b996bfde0.png)

* zookeeper 서비스는 복수의 서버에 복제되며, 모든 서버는 데이터 카피본을 가지고 있습니다

* 리더는 구동 시 zookeeper 내부 알고리즘에 의해 자동 선정됩니다.

* Followers 서버들은 클라이언트로부터 받은 모든 업데이트 이벤트를 리더에게 전달한다.

* 클라이언트는 모든 주키퍼 서버에서 읽을 수 있으며, 리더를 통해 쓸 수 있고 과반수 서버의 승인(합의)가 필요하다.

만일 주키퍼 서버에 쓰기 동작을 할 경우에, 클라이언트는 특정 서버에 접속하여 그 서버의 데이터를 업데이트 합니다. 그리고 업데이트 된 서버는 leader의 역할을 맡은 주키퍼 서버에 그 데이터를 알리고 업데이트하죠. 이 업데이트를 감지한 leader 서버는 그 정보를 다른 곳에 브로드캐스트(Broadcast) 형식으로 알리게 됩니다. 그 업데이트 정보를 받은 나머지 Follower 주키퍼 서버들은 그 내용을 갱신하여 전체 서버들의 데이터들이 일관된 상태로 유지된 상태로 있게 됩니다.


## znode

![](https://user-images.githubusercontent.com/44635266/66716384-2fc37b00-ee08-11e9-8f1b-a9fac18c379e.png)

주키퍼는 znode로 이루어진 분산 데이터 모델을 지원하는 시스템이라고 해도 과언이 아닙니다. 이 데이터 모델은 리눅스(linux) 파일시스템과 유사한 시스템을 제공하고 이것이 주키퍼의 핵심입니다.

각각의 znode는 stat 구조를 유지하고 있습니다. 이 stat은 znode의 메타데이터(metadata)를 제공합니다. 이 메타데이터를 이루는 것은 버전 넘버(version number), ACL(Action control list), 타입스탬프(Timestamp), 그리고 데이터 길이(Data length)가 있습니다.

### 버전 넘버(version number)

모든 znode들은 버전 넘버가지고 있습니다. znode의 데이터가 업데이트 될 때마다 이 버전 넘버는 계속해서 업데이트됩니다. 이 정보는 다수의 주키퍼 클라이언트(client)들이 특정한 연산을 같은 znode에 수행할 때 꼭 필요한 정보입니다.

### ACL(Action control list)

ACL은 znode에 접근하기 위한 권한 획득 메커니즘입니다. 이 권한을 통해 znode의 읽기 쓰기 연산을 통제하죠.

### 타입스탬프(Timestamp)

znode는 타임스탬프 정보를 제공합니다. znode가 생성되고 나서 경과된 시간 및 업데이트된 시간이 그것이죠. 시간 단위는 보통 ms입니다. 주키퍼는 znode를 변경한 트랜잭션(Transaction)정보를 기록합니다. 이 트랜잭션 정보는 Zxid로 구분됩니다. 타임스탬프를 이용하면 어떤 연산이 얼마나 걸렸는지 얼마나 경과했는지 바로 알 수 있습니다.

### 데이터 길이(Data length)

주키퍼의 데이터 크기를 말합니다. 주키퍼의 데이터들은 최대 1MB까지 저장 가능합니다.

또한, znode는 3가지 종류가 있습니다.

### Persistence znode

Persistence znode는 이 znode를 만든 클라이언트의 접속이 끊어져도 계속 주키퍼 데이터 모델에 남아있습니다. znode가 만들어질 때 default로 이 Persistence znode가 만들어집니다. 이 Persistence znode는 클러스터 관리 로직을 구현할 때 중요한 역할을 하게 됩니다.

### Ephemeral znode

Ephemeral znode는 이 znode를 만든 클라이언트의 접속이 끊기면 데이터 모델 상에서 사라집니다. 이런 특징덕분에 Ephemeral znode는 자신의 자식 znode를 가질 수 없습니다. Ephemeral znode는 리더 선출을 구현할 때 요긴하게 사용됩니다.

### Sequential znode

Sequential znode는 영속적일 수도 임시적일 수도 있습니다. Sequential znode가 만들어 질 때 주키퍼 데이터 모델 상에서 이 znode는 10자리 연속된 숫자를 가지고 있는 이름을 가지고 만들어 집니다.

예를들어 /app 이라는 Sequential znode를 만들면 app0000000001 로 자동적으로 만들어지는 형식입니다. 그리고 다음에는 0000000002이 znode가 만들어 지죠. 이 두 znode들은 동시에 만들어지기 때문에 주키퍼는 똑같은 이름의 노드를 쓸 일이 없습니다. 이 Sequential znode는 lock을 구현하거나 글로벌 큐(global queue)를 구현할 때 요긴하게 사용됩니다.




