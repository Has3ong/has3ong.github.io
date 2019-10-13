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

### 직접전달 / 간접전달

<img width="526" alt="스크린샷 2019-10-08 오후 9 48 54" src="https://user-images.githubusercontent.com/44635266/66396792-76366580-ea15-11e9-8a15-5e0fd9188462.png">

직접전달의 뜻은 패킷의 목적지가 전달자와 같은 네트워크에 있는 경우를 직접전달이라 합니다.

즉, 패킷을 전달하려는 사람과 목적지가 같은 곳이면 직접 전달입니다.

<img width="601" alt="스크린샷 2019-10-08 오후 9 48 58" src="https://user-images.githubusercontent.com/44635266/66396794-76366580-ea15-11e9-95ad-556e5220a306.png">

송신자와 수신자가 다른 네트워크에 있으면 간접 전달을 합니다.
수신자의 라우터의 IP주소를 알아내야지 라우터의 물리주소를 알아낼 수 있을겁니다. 이것은 라우팅 테이블을 이용하여 찾죠.

목적지 IP주소를 주면, 라우팅 테이블에서 라우터의 IP주소를 알 수 있습니다. 그리고 IP주소를 알아내면 내부 메모리 또는 ARP를 이용하여 물리주소를 알아낼 수 있습니다.

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

