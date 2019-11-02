---
title : HTTP 
tags:
- http
- http 0.9
- http 1.0
- http 1.1
- http 2.0
- http 3.0
---

## HTTP (HyperText Transfer Protocol)

HTTP는 WWW 상에서 정보를 주고받을 수 있는 프로토콜이다. 주로 HTML 문서를 주고받는 데에 쓰인다. TCP와 UDP를 사용하며, 80번 포트를 사용한다. 

## HTTP / 0.9

HTTP 초기 버전에는 버전 번호가 없었습니다. HTTP/0.9는 이후에 차후 버전과 구별하기 위해 0.9로 불리게 됐습니다. HTTP/0.9는 극히 단순합니다.

요청은 단일 라인으로 구성되며 리소스에 대한 (프로토콜, 서버 그리고 포트는 서버가 연결되고 나면 불필요로 하므로 URL은 아닌) 경로로 가능한 메서드는 GET이 유일했습니다.

> Request

```
GET /mypage.html
```

> Response

```
<HTML>
A very simple HTML page
</HTML>
```

## HTTP / 1.0

HTTP/0.9는 매우 제한적이었으며 브라우저와 서버 모두 좀 더 융통성을 가지도록 빠르게 확장되었습니다.

* 버전 정보가 각 요청 사이내로 전송되기 시작했습니다. (HTTP/1.0 이 GET 라인에 붙은 형태로)
* 상태 코드 라인 또한 응답의 시작 부분에 붙어 전송되어, 브라우저가 요청에 대한 성공과 실패를 알 수 있고 그 결과에 대한 동작(특정 방법으로 그것의 로컬 캐시를 갱신하거나 사용하는 것과 같은)을 할 수 있게 되었습니다.
* HTTP 헤더 개념은 요청과 응답 모두를 위해 도입되어, 메타데이터 전송을 허용하고 프로토콜을 극도로 유연하고 확장 가능하도록 만들어주었습니다.
* 새로운 HTTP 헤더의 도움으로, 평이한 HTML 파일들 외에 다른 문서들을 전송하는 기능이 추가되었습니다(Content-Type 덕분에).

> Request

```
GET /mypage.html HTTP/1.0
User-Agent: NCSA_Mosaic/2.0 (Windows 3.1)

200 OK
Date: Tue, 15 Nov 1994 08:12:31 GMT
Server: CERN/3.0 libwww/2.17
Content-Type: text/html

```

> Response

```
<HTML> 
A page with an image
  <IMG SRC="/myimage.gif">
</HTML>
```

## HTTP / 1.1

HTTP/1.1은 모호함을 명확하게 하고 많은 개선 사항들을 도입했습니다:

* 커넥션이 재사용될 수 있게 하여, 탐색된 단일 원본 문서 내로 임베드된 리소스들을 디스플레이하기 위해 사용된 커넥션을 다시 열어 시간을 절약하게 하였습니다.
* 파이프라이닝을 추가하여, 첫번째 요청에 대한 응답이 완전히 전송되기 이전에 두번째 요청 전송을 가능케 하여, 커뮤니케이션 레이턴시를 낮췄습니다.
* 청크된 응답 또한 지원됩니다.
* 추가적인 캐시 제어 메커니즘이 도입되었습니다.
* 언어, 인코딩 혹은 타입을 포함한 컨텐츠 협상이 도입되어, 클라이언트와 서버로 하여금 교환하려는 가장 적합한 컨텐츠에 대한 동의를 가능케 했습니다.
* Host 헤더 덕분에, 동일 IP 주소에 다른 도메인을 호스트하는 기능이 서버 코로케이션을 가능케 합니다.

> 단일 커넥션을 통한 요청의 전형적인 전체 흐름의 예시.

```
GET /en-US/docs/Glossary/Simple_header HTTP/1.1
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/en-US/docs/Glossary/Simple_header

200 OK
Connection: Keep-Alive
Content-Encoding: gzip
Content-Type: text/html; charset=utf-8
Date: Wed, 20 Jul 2016 10:55:30 GMT
Etag: "547fa7e369ef56031dd3bff2ace9fc0832eb251a"
Keep-Alive: timeout=5, max=1000
Last-Modified: Tue, 19 Jul 2016 00:59:33 GMT
Server: Apache
Transfer-Encoding: chunked
Vary: Cookie, Accept-Encoding

(content)


GET /static/img/header-background.png HTTP/1.1
Host: developer.cdn.mozilla.net
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/en-US/docs/Glossary/Simple_header

200 OK
Age: 9578461
Cache-Control: public, max-age=315360000
Connection: keep-alive
Content-Length: 3077
Content-Type: image/png
Date: Thu, 31 Mar 2016 13:34:46 GMT
Last-Modified: Wed, 21 Oct 2015 18:27:50 GMT
Server: Apache

(image content of 3077 bytes)
```

### HTTP 1.1 통신방식

![image](https://user-images.githubusercontent.com/44635266/68075479-a80bd380-fdeb-11e9-8dde-2372328eef4a.png)

![image](https://user-images.githubusercontent.com/44635266/68075480-a93d0080-fdeb-11e9-87ce-c00cd330f961.png)

![image](https://user-images.githubusercontent.com/44635266/68075481-a9d59700-fdeb-11e9-97cb-4ee4a1b6b8ea.png)

## HTTP / 2.0

* 텍스트 프로토콜이 아닌 이진 프로토콜을 사용한다.
* 병렬 요청이 동일한 커넥션 상에서 다루어질 수 있는 다중화 프로토콜로, 순서를 제거해주고 HTTP/1.x 프로토콜의 제약사항을 막아줍니다.
* 전송된 데이터의 분명한 중복과 그런 데이터로부터 유발된 불필요한 오버헤드를 제거하면서, 연속된 요청 사이의 매우 유사한 내용으로 존재하는 헤더들을 압축시킵니다.
* 서버로 하여금 사전에 클라이언트 캐시를 서버 푸쉬라고 불리는 메커니즘에 의해, 필요하게 될 데이터로 채워넣도록 허용합니다.

![image](https://user-images.githubusercontent.com/44635266/68075482-ab9f5a80-fdeb-11e9-8b37-0b829a795edb.png)

* HTTP2에서는 스트림이라는 단위로 요청과 응답이 묶일 수 있는 구조가 만들어졌다.
* HTTP2에서는 스트림 하나가 다수개의 요청과 응답을 처리

![image](https://user-images.githubusercontent.com/44635266/68075485-acd08780-fdeb-11e9-98dd-1b97dc618807.png)

* Server Push
  * 브라우저에서 필요한 리소스들을 서버가 알아서 찾아다가 내려주는 것을 의미
  * 캐싱되어 재사용되는 리소스를 PUSH하는 경우 비효율적

![image](https://user-images.githubusercontent.com/44635266/68075486-ae01b480-fdeb-11e9-8071-45c42cf6047f.png)

![image](https://user-images.githubusercontent.com/44635266/68075488-afcb7800-fdeb-11e9-8f20-603210017fbd.png)

## HTTP / 3.0

* QUIC라는 프로토콜 위에서 돌아가는 HTTP
* 스트림은 동일 QUIC 연결을 공유 하므로 새 스트림을 만들 때 추가적인 핸드쉐이크나 슬로우 스타트가 필요하지 않습니다
* QUIC 스트림은 독립적으로 전달되어 어떤 스트림에 패킷 손실이 있는 경우에도 다른 스트림에는 영향이 없습니다. 이는 QUIC 패킷이 UDP 데이터그램 위에 캡슐화되어 있기 때문
* QUIC은 TCP의 전형적인 3방향 핸드셰이크와 TLS 1.3의 핸드셰이크를 결합 합니다
