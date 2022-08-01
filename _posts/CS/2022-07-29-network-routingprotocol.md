---
title : 라우팅 프로토콜 (Routing Protocol)
categories:
- Computer Science
tags : 
- Computer Science
- Routing
- Protocol
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## Routing Protocol 개념

라우팅 프로토콜(Routing Protocol)은 라우터 간 통신 방식을 규정하는 통신 규약입니다.

라우터는 OSI 7 Layer 중 3 Layer 즉, Network Layer에서 동작합니다. 패킷의 위치를 추출하여, 그 위치에 대한 최적의 경로를 지정하며, 이 경로를 따라 데이터 패킷을 다음 장치로 전송시키는 장치입니다. 

이것이 최단 거리 일수도 있지만, 돌아가는 경로라도 고속의 전송로를 통하여 전달이 되는 경로가 될 수 있습니다. 즉, 라우터는 네트워크와 네트워크 간의 경로(Route)를 설정하고 가장 빠른 경로로 트래픽을 이끌어주는 네트워크 장비입니다.

또한 라우터의 대표적인 기능은 네트워크와 네트워크를 연결하는 것이지만, NAT, 방화벽, VPN, QoS등 다양한 부가 기능을 함께 제공하기도 합니다.

## Routing Protocol 종류

라우팅 프로토콜의 종류를 간단히 도식화하여 살펴보고 하나하나 상세히 알아보겠습니다.

![image](/assets/images/cs/routingprotocol1.png)

> 이미지 참조 [라우팅 프로토콜(Routing Protocol)](https://needjarvis.tistory.com/159)

### AS(Autonomous System)

자율 시스템(AS)은 인터넷에 명확하게 정의된 공통 라우팅 정책을 제시하는 단일 관리 엔터티 또는 도메인을 대신하여 한 명 이상의 네트워크 운영자가 제어하는 ​​연결된 인터넷 프로토콜(IP) 라우팅 접두사의 모음입니다.

아래 이미지 참고하시면 됩니다.

### Static Routing

정적 라우팅은 라우터가 동적 라우팅 트래픽의 정보가 아닌 수동으로 구성된 라우팅 항목을 사용할 때 발생하는 라우팅의 한 형태입니다. 동적 라우팅과 달리 정적 경로는 고정되어 있으며 네트워크가 변경되거나 재구성되어도 변경되지 않습니다.

> 장점

* 정적 라우팅은 라우터의 CPU에 거의 부하를 일으키지 않습니다.
* 정적 라우팅을 사용하면 네트워크 관리자가 네트워크의 라우팅 동작을 완전히 제어할 수 있습니다.
* 정적 라우팅은 소규모 네트워크에서 구성하기가 매우 쉽습니다.

> 단점

* 많은 경우 정적 경로가 수동으로 구성됩니다. 이는 사람의 실수 가능성을 증가시킵니다. 관리자는 실수로 네트워크 정보를 잘못 입력하거나 실수로 잘못된 라우팅 경로를 구성할 수 있습니다.
* 정적 라우팅은 내결함성이 없습니다. 즉, 네트워크에 변경 사항이 있거나 두 개의 정적으로 정의된 장치 간에 장애가 발생하면 트래픽이 다시 라우팅되지 않습니다. 결과적으로 네트워크는 장애가 복구되거나 관리자가 수동으로 고정 경로를 재구성할 때까지 사용할 수 없습니다.
* 정적 경로는 일반적으로 동적 라우팅 프로토콜로 구성된 경로보다 우선합니다. 즉, 고정 경로는 라우팅 프로토콜이 의도한 대로 작동하지 않을 수 있습니다. 해결 방법은 관리 거리를 수동으로 수정하는 것입니다.
* 네트워크의 각 라우터에서 고정 경로를 구성해야 합니다. 라우터가 많은 경우 이 구성에 시간이 오래 걸릴 수 있습니다. 또한 재구성이 느리고 비효율적일 수 있음을 의미합니다. 반면에 동적 라우팅은 라우팅 변경 사항을 자동으로 전파하여 수동 재구성의 필요성을 줄입니다.

> 사용 예시

```bash
$ ip route add 10.10.20.0 via 192.168.100.1
```

### Dynamic Routing

적응형 라우팅이라고도 하는 동적 라우팅은 라우터가 시스템 내 통신 회로의 현재 조건에 따라 주어진 대상에 대해 다른 경로를 통해 데이터를 전달할 수 있는 프로세스입니다.

> 장점

* 동적 라우팅은 자동으로 네트워크 정보를 교환하여 최적의 경로를 설정하고, 라우팅 테이블을 유지하기 때문에 최적의 경로를 선택할 수 있습니다.
* 동적 라우팅은 네트워크를 구성하기 쉽습니다.

> 단점

* 동적 라우팅은 많은 CPU 부하와 시스템 메모리를 사용합니다.
* 동적 라우팅은 업데이트를 주고 받기 위하여 대역폭을 사용하는데, 이는 WAN 성능 하락의 원인이 됩니다.

### IGP(Internal Gateway Protocol)

내부 게이트웨이 프로토콜(IGP)은 자율 시스템(Autonomous System, AS) 내의 게이트웨이(일반적으로 라우터) 간에 라우팅 테이블 정보를 교환하는 데 사용되는 라우팅 프로토콜 유형입니다. 이 라우팅 정보는 IP와 같은 네트워크 계층 프로토콜을 라우팅하는 데 사용할 수 있습니다.

### EGP(Exterior Gateway Protocol)

외부 게이트웨이 프로토콜은 자율 시스템간에 라우팅 정보를 교환하는 데 사용됩니다.

### Distance-vector routing protocol

거리 벡터 라우팅 프로토콜은 거리를 기반으로 데이터 패킷에 대한 최적의 경로를 결정합니다. 거리 벡터 라우팅 프로토콜은 패킷이 통과해야 하는 라우터 수로 거리를 측정합니다. 하나의 라우터는 하나의 홉으로 계산됩니다. 일부 거리 벡터 프로토콜은 주어진 경로의 트래픽에 영향을 미치는 네트워크 대기 시간 및 기타 요인도 고려합니다. 

### Link-state routing protocol

링크 상태 프로토콜은 네트워크의 모든 스위칭 노드(즉, 패킷을 전달할 준비가 된 노드, 인터넷에서는 라우터라고 함)에서 수행됩니다. 링크 상태 라우팅의 기본 개념은 모든 노드가 네트워크에 대한 연결 맵을 그래프 형태로 구성하여 어떤 노드가 다른 노드에 연결되어 있는지 보여주는 것입니다. 그런 다음 각 노드는 해당 노드에서 네트워크의 모든 가능한 대상까지의 차선책 논리적 경로를 독립적으로 계산합니다. 최상의 경로의 각 컬렉션은 각 노드의 라우팅 테이블을 형성합니다.

거리벡터 라우팅 프로토콜과의 차이점은 아래 표를 확인하시면 됩니다.

|Distance Vector Routing|Link State Routing|
|:--|:--|
|No flooding, small packets and local sharing require less bandwidth.|More bandwidth required to facilitate flooding and sending large link state packets.|
|Uses Bellman-Ford algorithm.|Uses Dijkstra’s algorithm.|
|Less traffic.|More network traffic when compared to Distance Vector Routing.|
|Updates table based on information from neighbours, thus uses local knowledge.|It has knowledge about the entire network, thus it uses global knowledge.|
|Persistent looping problem exists.|Only transient loop problems.|
|Based on least hops.|Based on least cost.|
|Updation of full routing tables.|Updation of only link states.|
|Less CPU utilisation.|High CPU utilisation.|
|Uses broadcast for updates.|Uses multicast for updates.|
|Moderate convergence time.|Low convergence time.|

### 프로토콜 특징 정리

|프로토콜|특징|
|:--:|:--|
|RIP|<li> RIP는 소스에서 대상까지의 경로에서 허용되는 홉 수에 대한 제한을 구현하여 라우팅 루프를 방지</li><li>RIP에 허용되는 최대 홉 수는 15이며, 이는 RIP가 지원할 수 있는 네트워크 크기를 제한</li>|
|IGRP|<li>IGRP는 대역폭, 지연, 부하 및 안정성을 포함하여 각 경로에 대해 여러 메트릭을 지원</li><li>두 경로를 비교하기 위해 이러한 메트릭은 사전 설정된 상수를 사용하여 조정할 수 있는 공식을 사용하여 단일 메트릭으로 결합</li><li>기본적으로 IGRP 복합 메트릭은 세그먼트 지연과 가장 낮은 세그먼트 대역폭의 합계</li><li>IGRP 라우팅 패킷의 구성 가능한 최대 홉 수는 255(기본값 100)이며 라우팅 업데이트는 기본적으로 90초마다 브로드캐스트</li><li>IGRP는 클래스풀 라우팅 프로토콜로 간주</li>|
|EIGRP|<li>EIGRP는 라우팅 결정 및 구성을 자동화하기 위해 컴퓨터 네트워크에서 사용되는 고급 거리 벡터 라우팅 프로토콜</li><li>EIGRP는 라우터에서 동일한 자율 시스템 내의 다른 라우터와 경로를 공유하는 데 사용</li><li>EIGRP는 증분 업데이트만 전송하므로 라우터의 작업 부하와 전송해야 하는 데이터의 양이 감소</li><li>EIGRP는 DUAL(Diffusing Update Algorithm)(SRI International의 작업 기반)을 사용하여 프로토콜의 효율성을 개선하고 원격에 대한 최상의 경로를 결정할 때 계산 오류를 방지</li>|
|OSPF|<li>OSPF는 IP 네트워크용 라우팅 프로토콜입니다. LSR 알고리즘을 사용하며 단일 자율 시스템 내에서 작동하는 IGP 그룹에 속합니다.</li><li>OSPF는 사용 가능한 라우터에서 링크 상태 정보를 수집하고 네트워크의 토폴로지 맵을 구성</li><li>토폴로지는 대상 IP 주소로 패킷을 라우팅하기 위해 인터넷 계층에 대한 라우팅 테이블로 제공</li><li>OSPF는 IPv4 및 IPv6 네트워크를 지원하고 CIDR(Classless Inter-Domain Routing) 주소 지정 모델을 지원</li>|
|BGP|<li>BGP는 인터넷의 자율 시스템간에 라우팅 및 도달 가능성 정보를 교환하도록 설계된 표준화된 외부 게이트웨이 프로토콜</li><li>인터넷상에서 경로 교환 및 트래픽 전송은 외부 BGP(eBGP)를 이용</li><li>자율 시스템은 BGP의 내부 버전을 이용해 자체 내부 네트워크 내에서 라우팅할 수도 있는데, 이를 내부 BGP(iBGP)</li>|

![image](/assets/images/cs/routingprotocol2.jpeg)

> 출처 - https://www.9tut.com/border-gateway-protocol-bgp-tutorial/comment-page-4

### 참고자료

* [Wikipedia - Routing Protocol](https://en.wikipedia.org/wiki/Routing_protocol)
* [Wikipedia - OSPF](https://en.wikipedia.org/wiki/Open_Shortest_Path_First)
* [Wikipedia - RIP](https://en.wikipedia.org/wiki/Routing_Information_Protocol) 
* [Wikipedia - IGRP](https://en.wikipedia.org/wiki/Interior_Gateway_Routing_Protocol)
* [Wikipedia - BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)
* [Wikipedia - EGP](https://en.wikipedia.org/wiki/Exterior_Gateway_Protocol)
* [Wikipedia - IGP](https://en.wikipedia.org/wiki/Interior_gateway_protocol)
* [Wikipedia - EIGRP](https://en.wikipedia.org/wiki/Enhanced_Interior_Gateway_Routing_Protocol)
* [Wikipedia - Distance-vector routing protocol](https://en.wikipedia.org/wiki/Distance-vector_routing_protocol)
* [Wikipedia - Link-state routing protocol](https://en.wikipedia.org/wiki/Link-state_routing_protocol)
* [Dynamic routing](https://en.wikipedia.org/wiki/Dynamic_routing)
* [Static routing](https://en.wikipedia.org/wiki/Static_routing)
* [Border Gateway Protocol BGP Tutorial](https://www.9tut.com/border-gateway-protocol-bgp-tutorial/comment-page-4)