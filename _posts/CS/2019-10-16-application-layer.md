---
title : Application Layer
tags:
- DNS
- DHCP
- HTTP
- Application Layer
- Network
- Computer Science
---  

## 응용 계층 (Application Layer)

응용 계층(영어: application layer)은 컴퓨터 네트워크 프로그래밍에서 인터넷 프로토콜(IP) 컴퓨터 네트워크를 통하는 프로세스 간 통신 접속을 위해 설계되어 통신 프로토콜과 방식을 위해 보유된 추상 계층이다. 응용 계층 프로토콜은 기반이 되는 전송 계층 프로토콜을 사용하여 호스트 간 연결을 확립한다.

OSI 모형에서 이 응용 계층의 정의는 범위가 더 좁다. OSI 모형은 응용 계층을 사용자 인터페이스로 정의한다. OSI 응용 계층은 사람이 인식하고 응용 계층 아래의 표현 계층과 상호 작용할 수 있는 데이터와 그림을 사용자에게 보여주는 역할을 맡는다


## HTTP (HyperText Transfer Protocol)

HTTP는 WWW 상에서 정보를 주고받을 수 있는 프로토콜이다. 주로 HTML 문서를 주고받는 데에 쓰인다. TCP와 UDP를 사용하며, 80번 포트를 사용한다. 

HTTP는 클라이언트와 서버 사이에 이루어지는 요청/응답(request/response) 프로토콜이다. 예를 들면, 클라이언트인 웹 브라우저가 HTTP를 통하여 서버로부터 웹페이지나 그림 정보를 요청하면, 서버는 이 요청에 응답하여 필요한 정보를 해당 사용자에게 전달하게 된다. 이 정보가 모니터와 같은 출력 장치를 통해 사용자에게 나타나는 것이다.

HTTP를 통해 전달되는 자료는 http:로 시작하는 URL(인터넷 주소)로 조회할 수 있다.

### HTTP Method

클라이언트가 웹서버에게 사용자 요청의 목적/종류를 알리는 수단

![스크린샷 2019-10-05 오후 5 38 32](https://user-images.githubusercontent.com/44635266/66252476-05821580-e797-11e9-95ed-c7d841edc1d0.png)

* GET

 요청받은 URI의 정보를 검색하여 응답한다.

* HEAD

GET방식과 동일하지만, 응답에 BODY가 없고 응답코드와 HEAD만 응답한다.
웹서버 정보확인, 헬스체크, 버젼확인, 최종 수정일자 확인등의 용도로 사용된다.

* POST

요청된 자원을 생성(CREATE)한다. 새로 작성된 리소스인 경우 HTTP헤더 항목 Location : URI주소를 포함하여 응답.

* PUT

요청된 자원을 수정(UPDATE)한다. 내용 갱신을 위주로 Location : URI를 보내지 않아도 된다. 클라이언트측은 요청된 URI를 그대로 사용하는 것으로 간주함.

* DELETE

요청된 자원을 삭제할 것을 요청함.  (안전성 문제로 대부분의 서버에서 비활성)

* CONNECT

 동적으로 터널 모드를 교환, 프락시 기능을 요청시 사용.

* OPTIONS

 웹서버에서 지원되는 메소드의 종류를 확인할 경우 사용

* TRACE

 원격지 서버에 루프백 메시지 호출하기 위해 테스트용으로 사용.

* PATCH

PUT과 유사하게 요청된 자원을 수정(UPDATE)할 때 사용한다. PUT의 경우 자원 전체를 갱신하는 의미지만, PATCH는 해당자원의 일부를 교체하는 의미로 사용.

### 메세지 포멧

클라이언트와 서버 사이의 소통은 평문(ASCII) 메시지로 이루어진다. 클라이언트는 서버로 요청메시지를 전달하며 서버는 응답메시지를 보낸다.

> Client request

```
GET /index.html HTTP/1.1  //요청 URL정보 (Mehotd /URI HTTP버젼)
user-agent: MSIE 6.0; Window NT 5.0 //사용자 웹 브라우져 종류
accept: test/html; */*  //요청 데이터 타입 (응답의 Content-type과 유사)
cookie:name=value //쿠키(인증 정보)
refere: http://abc.com  //경유지 URL
host: www.abc.com //요청 도메인
```

> Server response

```
HTTP/1.1 200 OK //프로토콜 버젼 및 응답코드
Server: Apache  //웹 서버 정보
Content-type: text/html //MIME 타입
Content-length : 1593 //HTTP BODY 사이즈
<html><head>.....</head></html> //HTTP BODY 컨텐츠
```

### HTTP 응답 코드

클라이언트가 서버에 접속하여 어떠한 요청을 하면, 서버는 세 자리 수로 된 응답 코드와 함께 응답한다. 대표적인 HTTP의 응답 코드는 다음과 같다.


```
200 // OK // 오류없이 전송 성공
304 // Not Modified // 클라이언트의 캐시에 이 문서가 저장되었고 선택적인 요청에 의해 수행됨
404 // Not Found // 문서를 찾을 수 없음. 서버가 요청한 파일이나 스크립트를 찾지 못함.
500 // Internal Server Error	 // 서버 내부 오류.
```

### HTTP vs HTTPS

HTTPS(HyperText Transfer Protocol over Secure Socket Layer, HTTP over TLS, HTTP over SSL, HTTP Secure)

월드 와이드 웹 통신 프로토콜인 HTTP의 보안이 강화된 버전이다. HTTPS는 통신의 인증과 암호화를 위해 넷스케이프 커뮤니케이션즈 코퍼레이션이 개발했으며, 전자 상거래에서 널리 쓰인다.

HTTPS는 소켓 통신에서 일반 텍스트를 이용하는 대신에, SSL이나 TLS 프로토콜을 통해 세션 데이터를 암호화한다. 따라서 데이터의 적절한 보호를 보장한다. HTTPS의 기본 TCP/IP 포트는 443이다.

보호의 수준은 웹 브라우저에서의 구현 정확도와 서버 소프트웨어, 지원하는 암호화 알고리즘에 달려있다.

HTTPS를 사용하는 웹페이지의 URI은 `http://`대신 `https://`로 시작한다.

![](https://user-images.githubusercontent.com/44635266/66919128-b6bc6180-f05b-11e9-99df-46897cac8620.png)

위 그림과같이 HTTPS를 사용하면 우리는 웹 서버와 통신을 할 때 `Client -> SSL`와 `SSL -> Server` 이렇게 중간에 SSL을 사이에 두고 통신을 하게 됩니다. 

SSL과 TLS는 다른 보안쪽 포스트에서 자세히 다루겠습니다. [여기](/SSL)를 누르시면 따로 정리한 포스트에서 알려드리겠습니다.

### HTTP 1.0 2.0 3.0

내용이 길어지는 관계로 [여기](/http) 를 누르시면 따로 정리한 포스트에서 알려드리겠습니다.

## DHCP (동적 호스트 구성 프로토콜, Dynamic Host Configuration Protocol)

![](https://user-images.githubusercontent.com/44635266/66919769-f2a3f680-f05c-11e9-861d-032992674b72.png)

동적 호스트 구성 프로토콜(Dynamic Host Configuration Protocol, DHCP)은 호스트 IP 구성 관리를 단순화하는 IP 표준이다. 동적 호스트 구성 프로토콜 표준에서는 DHCP 서버를 사용하여 IP 주소 및 관련된 기타 구성 세부 정보를 네트워크의 DHCP 사용 클라이언트에게 동적으로 할당하는 방법을 제공한다.

쉽게 말해 가정에서 흔히 볼 수 있는 공유기라고 생각하면 됩니다.

백문불여일견이라고 저희집 DHCP를 확인해 보았습니다. 컴퓨터와 노트북을 연결시켜놓은 뒤에 노트북에 IP를 확인해보았습니다.

![](https://user-images.githubusercontent.com/44635266/66919771-f2a3f680-f05c-11e9-9a51-e1fdc0b7f7d7.png)

> 작업중인 `ifconfig`
```
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether a4:83:e7:21:99:fe
	inet6 fe80::46c:3ecd:9e93:9f7a%en0 prefixlen 64 secured scopeid 0xa
	inet 192.168.35.132 netmask 0xffffff00 broadcast 192.168.35.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```

노트북에 ip는 `192.168.35.132`이고 데스크탑은 `192.168.35.75` 입니다. 자세히 보면 `ether` 뒤에 MAC 주소도 정확하게 일치하는것을 볼 수 있습니다.

### 동작원리

![](https://user-images.githubusercontent.com/44635266/66919768-f2a3f680-f05c-11e9-91f7-91a7d31bb25f.png)

DHCP 동작 원리는 크게 네단계로 단말과 서버간에 통신이 이루어 진다.

1. DHCP Discover :

메시지 방향: 단말 -> DHCP 서버 로 이루어 지며 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 를 통해서, 단말장비가 DHCP 서버에게 아이피 주소를 할당을 요청하는것이다

2. DHCP Offer :

메시지 방향: DHCP 서버 -> 단말로 이루어진다. 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF)이거나 유니캐스트를 통해서 이루어지며, 단말에서 요청을 한 아이피 주소 정보를 포함한 네트워크 정보의 할당 요청을, DHCP 서버가 받아서 이것에 대해서 응답을 하는것이며, 이때 아이피 주소 정보 와 단말의 MAC 주소 정보 등을 네트워크 정보와 함께 같이 전송한다.

3. DHCP Request:

메시지 방향: 단말 -> DHCP 서버 로 이루어진다. 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 로 단말이 받은 아이피 주소 정보를 사용하겠다는 것을 서버로 보내서, 확정을 받기 위한 메시지 이다.

4. DHCP Ack:

메시지 방향: DHCP 서버 -> 단말 로 이루어 진다 브로드캐스트 메시지 (Destination MAC = FF:FF:FF:FF:FF:FF) 혹은 유니캐스트일수 있다. 단말에서 보낸 DHCP Request 메시지 내의 Broadcast Flag=1이면 DHCP 서버는 DHCP Ack 메시지를 Broadcast로, Flag=0 이면 Unicast로 보내주며, 단말의 MAC 어드레스에 매칭이 되는 IP 주소와 게이트웨이 주소를 확정하여 주는 것이다.

### 특징

* PC의 수가 많거나 PC 자체 변동사항이 많은 경우 IP 설정이 자동으로 되기 때문에 효율적으로 사용 가능하고, IP를 자동으로 할당해주기 때문에 IP 충돌을 막을 수 있습니다.

* DHCP 서버에 의존되기 때문에 서버가 다운되면 IP 할당이 제대로 이루어지지 않습니다.

* 공유기에 연결하는 컴퓨터에 IP 주소를 지정하는 경우에 DHCP에서 할당한 MAC주소와 IP주소가 다르면 인터넷 연결이 안됩니다.

> Example

```
Computer IP = 192.168.35.1
Computer MAC = a4:83:e7:21:99:fe

DHCP IP = 192.168.35.2
DHCP MAC = a4:83:e7:21:99:fe
```

## DNS (도메인 네임 시스템, Domain Name System)

![](https://user-images.githubusercontent.com/44635266/66923033-1c601c00-f063-11e9-96bb-2b73b84779aa.png)

도메인 네임 시스템(Domain Name System, DNS)은 호스트의 도메인 이름을 호스트의 네트워크 주소로 바꾸거나 그 반대의 변환을 수행할 수 있도록 하기 위해 개발되었다. 특정 컴퓨터(또는 네트워크로 연결된 임의의 장치)의 주소를 찾기 위해, 사람이 이해하기 쉬운 도메인 이름을 숫자로 된 식별 번호(IP 주소)로 변환해 준다. 도메인 네임 시스템은 흔히 "전화번호부"에 비유된다. 인터넷 도메인 주소 체계로서 TCP/IP의 응용에서, `www.example.com`과 같은 주 컴퓨터의 도메인 이름을 `192.0.2.44`과 같은 IP 주소로 변환하고 라우팅 정보를 제공하는 분산형 데이터베이스 시스템이다.

인터넷은 2개의 주요 이름공간을 관리하는데, 하나는 도메인 네임 계층, 다른 하나는 인터넷 프로토콜(IP) 주소 공간이다. 도메인 네임 시스템은 도메인 네임 계층을 관리하며 해당 네임 계층과 주소 공간 간의 변환 서비스를 제공한다. 인터넷 네임 서버와 통신 프로토콜은 도메인 네임 시스템을 구현한다. DNS 네임 서버는 도메인을 위한 DNS 레코드를 저장하는 서버이다. DNS 네임 서버는 데이터베이스에 대한 쿼리의 응답 정보와 함께 응답한다.
