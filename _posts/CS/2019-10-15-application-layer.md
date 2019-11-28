---
title : Application Layer
---

## 응용 계층(Application Layer)

컴퓨터 네트워크 프로그래밍에서 인터넷 프로토콜(IP) 컴퓨터 네트워크를 통하는 프로세스 간 통신 접속을 위해 설계되어 통신 프로토콜과 방식을 위해 보유된 추상 계층이다. 응용 계층 프로토콜은 기반이 되는 전송 계층 프로토콜을 사용하여 호스트 간 연결을 확립한다.

OSI 모형에서 이 응용 계층의 정의는 범위가 더 좁다. OSI 모형은 응용 계층을 사용자 인터페이스로 정의한다. OSI 응용 계층은 사람이 인식하고 응용 계층 아래의 표현 계층과 상호 작용할 수 있는 데이터와 그림을 사용자에게 보여주는 역할을 맡는다.

## DHCP (동적 호스트 구성 프로토콜, Dynamic Host Configuration Protocol)

호스트 IP 구성 관리를 단순화하는 IP 표준이다. 동적 호스트 구성 프로토콜 표준에서는 DHCP 서버를 사용하여 IP 주소 및 관련된 기타 구성 세부 정보를 네트워크의 DHCP 사용 클라이언트에게 동적으로 할당하는 방법을 제공한다.

### DHCP 동작원리

![Uploading 스크린샷 2019-10-10 오전 11.20.37.png…](https://user-images.githubusercontent.com/44635266/66534066-0d073d00-eb50-11e9-9c20-b35a5bcaf11a.png)

1. *DHCP Discover*
메시지 방향: Client -> DHCP 서버 로 이루어 지며 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 를 통해서, Client가 DHCP 서버에게 아이피 주소를 할당을 요청하는것이다

2. *DHCP Offer*
메시지 방향: DHCP 서버 -> Client로 이루어진다. 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF)이거나 유니캐스트를 통해서 이루어지며, Client에서 요청을 한 아이피 주소 정보를 포함한 네트워크 정보의 할당 요청을, DHCP 서버가 받아서 이것에 대해서 응답을 하는것이며, 이때 아이피 주소 정보 와 Client의 MAC 주소 정보 등을 네트워크 정보와 함께 같이 전송한다.

3) *DHCP Request*
메시지 방향: Client -> DHCP 서버 로 이루어진다. 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 로 Client이 받은 아이피 주소 정보를 사용하겠다는 것을 서버로 보내서, 확정을 받기 위한 메시지 이다.

4) *DHCP Ack*
메시지 방향: DHCP 서버 -> Client 로 이루어 진다 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 혹은 유니캐스트일수 있다. Client에서 보낸 DHCP Request 메시지 내의 Broadcast Flag=1이면 DHCP 서버는 DHCP Ack 메시지를 Broadcast로, Flag=0 이면 Unicast로 보내주며, Client의 MAC 어드레스에 매칭이 되는 IP 주소와 게이트웨이 주소를 확정하여 주는 것이다.


### 특징

* PC의 수가 많거나 PC 자체 변동사항이 많은 경우 IP 설정이 자동으로 되기 때문에 효율적으로 사용 가능하고, IP를 자동으로 할당해주기 때문에 IP 충돌을 막을 수 있습니다.
* DHCP 서버에 의존되기 때문에 서버가 다운되면 IP 할당이 제대로 이루어지지 않습니다.


