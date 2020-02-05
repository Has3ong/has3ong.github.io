---
title : Network Layer
tags:
- Network Layer
- IP
- ICMP
- IGMP
- IPSec
- ARP
- RARP
- Routing
- Subnet
- Computer Science
---

## 네트워크 계층(Network Layer)

네트워크 계층(영어: network layer)은 컴퓨터 네트워킹의 7계층 OSI 모형 가운데 제3계층이다. 네트워크 계층은 중간 라우터를 통한 라우팅을 포함하여 패킷 포워딩을 담당한다.


## IP (인터넷 프로토콜,  Internet Protocol address)

> IP 패킷 구조

![IP패킷](https://user-images.githubusercontent.com/44635266/66534563-89e6e680-eb51-11e9-9c99-2c5f6af5f8c4.png)

컴퓨터 네트워크에서 장치들이 서로를 인식하고 통신을 하기 위해서 사용하는 특수한 번호이다. 네트워크에 연결된 장치가 라우터이든 일반 서버이든, 모든 기계는 이 특수한 번호를 가지고 있어야 한다.

이 번호를 이용하여 발신자를 대신하여 메시지가 전송되고 수신자를 향하여 예정된 목적지로 전달된다. IP 주소를 줄여서 IP라고 부르기도 하나 ip는 인터넷 규약 자체를 가리키는 말이기 때문에 엄밀하게는 구별해야 한다.

오늘날 주로 사용되고 있는 IP 주소는 IP 버전 4(IPv4) 주소이나 이 주소가 부족해짐에 따라 길이를 늘린 IP 버전 6(IPv6) 주소가 점점 널리 사용되는 추세이다.

> IPv4 Example

```
211.214.14.153
```

> IPv6 Example

아래는 전부 같은 주소다.

```
2001:0DB8:0000:0000:0000:0000:1428:57ab
2001:0DB8:0000:0000:0000::1428:57ab
2001:0DB8:0:0:0:0:1428:57ab
2001:0DB8:0::0:1428:57ab
2001:0DB8::1428:57ab
```

### IPv4

IPv4의 주소체계는 총 12자리이며 네 부분으로 나뉜다. 각 부분은 0~255까지 3자리의 수로 표현된다. 총 32bit로 구성이 되어있다.

> 구성단위

![IP 클래스](https://user-images.githubusercontent.com/44635266/66534836-7b4cff00-eb52-11e9-8b24-3bb268767671.png)

> 특수 용도 주소

![IP 특수용도주소](https://user-images.githubusercontent.com/44635266/66534883-9d468180-eb52-11e9-95ac-5b896c45be06.png)

### 사설 네트워크 주소

IPv4의 주소 부족을 지연시킬 목적으로 정의됨. 사설주소가 할당된 컴퓨터는 인터넷에 직접적으로 액세스 할 수 없다.

##  서브넷 (Subnet)

부분망(Subnetwork) 또는 부분망 마스크(IP Subnet Mask, IP 서브넷 마스크), IP 서브넷은 인터넷 프로토콜 스위트의 가시적인 부분이다.

서브넷은 브로드캐스트 영역을 나누고 IP를 아끼기 위해 사용된다. 

B클래스 기준 `150.150.0.0`의 브로드캐스트 호스트 주소는 약 6만개가 되는데 서브넷으로 나누어 `150.150.1.0`과 `150.150.2.0`으로 나누게 되면 255개로 줄어들게된다. 나눠진 서브넷은 라우터를 통하여 통신하게 됩니다.

### 디폴트 서브넷 마스크

* A 클래스의 디폴트 서브넷 마스크 `255.0.0.0`
* B 클래스의 디폴트 서브넷 마스크 `255.255.0.0`
* C 클래스의 디폴트 서브넷 마스크 `255.255.255.0`

### 변형된 서브넷 마스크

![](https://user-images.githubusercontent.com/44635266/66755241-8bf2d180-eed2-11e9-828d-05039f86ce46.png)


IP주소는 IP 클래스에 의해 분리되는 Network Prefix와 나머지 Host Number로 분리되게 됩니다. 서브넷 마스크에 의해 이루어지는 서브넷팅은 이 Host Number를 Subnet Number와 서브넷안에서 식별되는 Host Number로 다시 분리합니다.

### IPv4 서브넷 구하기

부분망을 구하는 과정은 한 주소의 네트워크 및 부분망 부분과 호스트 식별자를 구분하는 일을 포함한다. 이는 IP 주소 및 (부분)망 마스크 간 AND 비트 연산을 통해 수행한다. 이를 통해 네트워크 주소나 접두사(prefix)가 만들어지며 나머지는 호스트 식별자가 된다.

다음은 192.168.5.130이라는 주소와 이와 연계된 /24 네트워크 마스크 (255.255.255.0)으로부터 네트워크 접두사와 호스트 식별자를 구분하는 예이다. 이 연산은 이진 주소 형식을 사용하여 아래의 표로 나타나 있다.

![](https://user-images.githubusercontent.com/44635266/66756338-c65d6e00-eed4-11e9-8824-e83dfe458b25.png)

### IP주소 / 서브넷 마스크 / 네트워크 주소

![](https://user-images.githubusercontent.com/44635266/66756339-c65d6e00-eed4-11e9-8b1c-b6eb9e0db330.png)

### 서브넷과 브로드캐스트 주소 / 호스트 수 

![](https://user-images.githubusercontent.com/44635266/66756342-c6f60480-eed4-11e9-83b7-00b62a1df03f.png)

![](https://user-images.githubusercontent.com/44635266/66756353-cf4e3f80-eed4-11e9-800a-73924ab9f74c.png)

### 직접전달 / 간접전달

<img width="526" alt="스크린샷 2019-10-08 오후 9 48 54" src="https://user-images.githubusercontent.com/44635266/66396792-76366580-ea15-11e9-8a15-5e0fd9188462.png">

직접전달의 뜻은 패킷의 목적지가 전달자와 같은 네트워크에 있는 경우를 직접전달이라 합니다.

즉, 패킷을 전달하려는 사람과 목적지가 같은 곳이면 직접 전달입니다.

<img width="601" alt="스크린샷 2019-10-08 오후 9 48 58" src="https://user-images.githubusercontent.com/44635266/66396794-76366580-ea15-11e9-95ad-556e5220a306.png">

송신자와 수신자가 다른 네트워크에 있으면 간접 전달을 합니다.
수신자의 라우터의 IP주소를 알아내야지 라우터의 물리주소를 알아낼 수 있을겁니다. 이것은 라우팅 테이블을 이용하여 찾죠.

목적지 IP주소를 주면, 라우팅 테이블에서라우터의 IP주소를 알 수 있습니다. 그리고 IP주소를 알아내면 내부 메모리 또는 ARP를 이용하여 물리주소를 알아낼 수 있습니다.

## Routing

Routing이란 패킷(Packet)을 전송하기 위한 수많은 경로 중에서 한 가지 경로를 결정하는 것이다.

라우팅에는 동적 라우팅(Dynamic Routing)과 정적 라우팅(Static Routing)으로 나누는데 정적 라우팅은 주로 사람이 수동으로 미리 경로를 지정하는 방식이고, 동적 라우팅은 변화하는 상황에 맞추어 라우터가 경로를 재설정하는 방식으로 이루어진다.

Routing Table의 업데이트는 서로의 라우트 테이블을 공유하면서 이루어집니다.

### Routing Table Format

1) Routing Table
- 패킷을 목적지로 라우팅 할 때 참조하는 테이블
- 목적지 주소, Output I/F, Metric 값

2) Message
- 라우터 간 라우팅을 위해 교환하는 메세지
- 이웃 도달 메세지, 라우팅 정보

3) Metric
- 라우팅 테이블 생성 및 업데이트 시 최적의 경로를 결정하는 기술
- 경로 길이, 홉(Hop) 수, 대역폭, 비용, 신뢰성

아래 몇 가지 예제를 살펴보겠습니다.

> Example 1

![](https://user-images.githubusercontent.com/44635266/66773641-6f6a8f80-eefa-11e9-99d6-31644a00f388.png)

> Routing Table Result

![](https://user-images.githubusercontent.com/44635266/66773642-6f6a8f80-eefa-11e9-845b-0807a43f9236.png)

> Example 2

![](https://user-images.githubusercontent.com/44635266/66773643-6f6a8f80-eefa-11e9-851d-e6b2f820d2e3.png)

> Routing Table Result

![](https://user-images.githubusercontent.com/44635266/66773644-70032600-eefa-11e9-9431-e752696ca848.png)

## Routing Protocol

![](https://user-images.githubusercontent.com/44635266/66770926-c6209b00-eef3-11e9-923a-9b1eb804ff61.png)


### Static / Dynamic

### Static Routing Protocol

- 수동식, 사람이 일일이 경로를 입력, 라우터 부하경감, 고속 라우팅 가능

- 관리자의 관리부담 증가 및 정해진 경로 문제 발생시 라우팅 불가능


### Dynamic Routing Protocol

- 라우터가 스스로 라우팅 경로를 동적으로 결정

- RIP, IGRP, OSPF, EIGRP

### Interior / Exterior

### Interior Gateway Protocol

- AS 내에서의 라우팅을 담당하는 라우팅 프로토콜

- RIP, IGRP, OSPF, EIGRP

### Exterior Gateway Protocol	

- 서로 다른 AS사이에서 사용되는 라우팅 프로토콜

- BGP, EGP

### Distance Vector / Link State

### Distance Vector Algorithm

- 라우팅 Table에 목적지까지 가는데 필요한 거리와 방향만을 기록 (인접 라우터)

- RIP, IGRP

### Link State Algorithm

- 라우터가 목적지까지 가는 경로를 SPF(Shortest Path First) 알고리즘을 통해 모든 라우팅 테이블에 기록해 두는 것 (모든 라우터)

- OSPF

> 주요 프로토콜 비교

![](https://user-images.githubusercontent.com/44635266/66771981-92934000-eef6-11e9-870b-49112620efd4.png)

## ARP  / RARP

![ARP/RARP](https://user-images.githubusercontent.com/44635266/66535265-04b10100-eb54-11e9-9093-069bbbc3d5f2.png)

### ARP(주소 결정 프로토콜, Address Resolution Protocol)

논리적인 IP주소를 물리적인 MAC주소로 바꾸어 주는 역할을 하는 주소 해석 프로토콜입니다. 3계층 프로토콜이지만 ip하위에서 동작하는 2.5계층 프로토콜이라고도 말합니다.
RARP는 ARP의 반대로 물리적인 MAC주소를 논리적인 IP주소로 알아낼 때 사용합니다

> ARP 구조

![](https://user-images.githubusercontent.com/44635266/66535338-3de97100-eb54-11e9-8b25-308f9ffadad2.png)

### 동작방식

![](https://user-images.githubusercontent.com/44635266/66535634-2a8ad580-eb55-11e9-8374-70e65dcaa5f9.png)

1. 송신자는 목적지 IP주소는 알고 있으나, 물리주소는 모름

2. 물리주소를 알아내기 위해 ARP 요청 메시지 생성
ARP 요청 메시지 (송신자 물리주소, 송신자 IP주소, 00-00-00-00-00, 수신자 IP주소)

3. 요청메시지를 데이터링크 계층으로 전달, 프레임 생성
송신자 물리주소를 발신지 주소, 수신자 물리주소를 브로드캐스트 주소로 지정

4. 모든 호스트나 라우터는 이 프레임을 수신하여 자신의 ARP로 전달

5. 요청 메시지에 해당되는 호스트나 라우터만 ARP응답 메시지 생성
자신의 물리주소를 포함하는 응답 메시지

6. ARP 응답메시지를 유니캐스트로 ARP 요청 메시지를 보낸 송신자에게 전송
유니캐스트를 이용하는 이유는 송신자가 요청메시지에 물리주소를 포함했기 때문

7. 송신자는 ARP 응답메시지를 받고 목적지 물리주소를 획득
 
8. 목적지에게 전송할 IP데이터그램을 획득한 물리주소를 이용해 프레임으로 캡슐화

9. 캡슐화된 프레임을 유니캐스트로 목적지로 전송

## NAT (네트워크 주소 변환, Network Address Translation)

내부가 사설 IP로 구축이 될때 가장 큰 문제가 사설 IP는 라우팅이 되지 않는것입니다. 그래서 정상적인 Network 서비스를 제공받을 수 없습니다. 이러한 문제를 해결하기 위한 것이 바로 NAT입니다.

![stati1c](https://user-images.githubusercontent.com/44635266/66758072-86988580-eed8-11e9-9c9e-36f75e10b98a.png)

위 그림과 같이 사설 IP를 공인 IP로 변경해줍니다. 쉽게 설명하면 전송되는 패킷의 IP 정보를 변경하는 기술입니다.

### 기능

* 공인 IP의 부족 문제를 해결

* 외부로부터 내부망을 보호
 
* ISP 변경에 따른 내부 IP 변경 최소화

## ICMP / IGMP

### ICMP(인터넷 제어 메시지 프로토콜, Internet Control Message Protocol)

![](https://user-images.githubusercontent.com/44635266/66715708-6b0e7b80-ee01-11e9-905a-6abdb88fa4c7.png)

네트워크 컴퓨터 위에서 돌아가는 운영체제에서 오류 메시지(Requested service is not available 등)를 전송받는 데 주로 쓰이며 인터넷 프로토콜의 주요 구성원 중 하나로 인터넷 프로토콜에 의존하여 작업을 수행한다.

ICMP 메시지들은 일반적으로 IP 동작(RFC 1122에 규정)에서 진단이나 제어로 사용되거나 오류에 대한 응답으로 만들어진다. ICMP 오류들은 원래 패킷의 소스 IP 주소로 보내지게 된다.

### IGMP(인터넷 그룹 관리 프로토콜, (Internet Group Management Protocol)

![](https://user-images.githubusercontent.com/44635266/66715759-fab42a00-ee01-11e9-9ca8-9346f9f021c2.png)

IGMP는 호스트가 멀티캐스트 그룹 구성원을 인접한 스위치 및 라우터로 광고할 수 있게 해주는 프로토콜입니다. IGMP는 TCP/IP 프로토콜 집합이 동적 멀티캐스팅을 수행하기 위해 사용하는 표준 프로토콜입니다.

서브넷(로컬 네트워크) 상의 멀티캐스팅 멤버십 제어(그룹 관리)를 위한 프로토콜이며, 하나의 라우터와 여러 호스트로 구성되는 서브 네트워크(Sub-Network) 상에서 호스트들이 어떤 멀티캐스트 그룹에 속하는 가를 라우터가 알도록 하기위한 일종의 그룹 관리용 신호프로토콜(Signaling Protocol)역할도 합니다.

### 기타 기능 

#### IGMP Snooping

IGMP Snooping은 라우터와 호스트 사이에 있는 스위치가 IGMP 메세지들을 들을 수 있게 하는 기능을 말함

#### IGMP Querier Election

동일 LAN에 여러 멀티캐스트 라우터가 있으면, IPv4 주소 중 가장 낮은 주소를 갖는 라우터가 Querier 역할을 집중하게 함

## IPsec (Internet Protocol Security)

보안에 취약한 구조를 가진 IP의 보안을 위하여 국제 인터넷 기술 위원회(IETF)에서 설계한 표준(RFC2401)입니다. IPv4에선 보안이 필요한 경우에만 선택적으로 사용하였지만 IPv6부턴 기본 스펙에 포함됩니다.

전송계층 아래에서 구현되며, 운영체제에서 IPsec을 지원함. 네트워크계층(IP 계층) 상에서 IP 패킷 단위로 인증,암호화,키관리 VPN을 구현하기 위한 프로토콜입니다. 

키관리를 통해 캡슐화 및 디캡슐화를 진행합니다.

### 보안구조

#### 인증 헤더(Authentication Header, AH)

* 메세지 인증 코드(MAC)를 이용하여 무결성과 인증을 제공
* 암호화는 제공되지 않음

#### 보안 페이로드 캡슐화 (Encapsulating Security Payload, ESP)

* AH가 가진 무결성과 인증을 제공하며, 추가적으로 대칭키 암호화를 이용하여 기밀성 제공


#### 보안 연관 (Security Association, SA)

* 데이터의 안전한 전달을 위해 통신의 쌍방 간의 약속
* 암호 알고리즘, 키 교환 방법, 암호화 키 교환 주기 등에 대한 합의


### 터널모드 / 전송모드

#### 터널모드

> AH

![](https://user-images.githubusercontent.com/44635266/66538015-9ffaa400-eb5d-11e9-9227-6d3d14295169.png)

> ESP

![](https://user-images.githubusercontent.com/44635266/66538016-9ffaa400-eb5d-11e9-9ec9-1b778adb4961.png)

IP 패킷 전체를 보호한다. 암호화된 패킷에 IPSec 헤더를 추가하여 라우팅을 수행한다. IPSec 헤더는 구간 간 이동에 대한 정보만 있으므로 종단 정보(출발지, 목적지)와 트래픽 경로는 보호된다.

일반적으로 터널/보안 게이트웨이 구간 또는 종단 노드와 터널/보안 게이트웨이 구간의 IP 패킷 보호를 위해 사용한다.

#### 전송모드

> AH 

![](https://user-images.githubusercontent.com/44635266/66538017-a0933a80-eb5d-11e9-83cc-d7256ab9884e.png)


> ESP 

![](https://user-images.githubusercontent.com/44635266/66538018-a0933a80-eb5d-11e9-989b-532af4473f08.png)

IP 패킷 전체를 보호하는것이 아니라 IP 헤더를 제외한 IP 패킷의 페이로드(Payload)만 보호한다. IP 헤더는 암호화하지 않으므로 트래픽 경로는 노출됩니다.

일반적으로 End Node구간의 IP 패킷 보호를 위해 사용된다.

