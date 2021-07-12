---
title : AJP Protocol
tags :
- Protocol
- AJP
- Network
- Computer Science
categories:
- Computer Science
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## AJP Protocol

AJP(Apache JServ Protocol)은 Web Server 에서 받은 요청을 WAS 로 전달해주는 프로토콜입니다.

해당 프로토콜은 Apache HTTP Server, Apahce Tomcat,  웹스피어, Web Logic, JBoss, JEUS, 등 다양한 WAS에서 지원합니다.

`mod_jk` 와 `mod_proxy` 로 구성되어 있습니다.

### mod_jk

mod_jk 는 Apache Web Server 뒤에 Tomcat 을 숨기고 URL 접근할 때 포트 번호를 제거하는데 유용합니다. mod_jk 모듈 실행을 위한 선언은 다음과 같습니다. *httpd.conf*

```shell
LoadModule jk_module modules/mod_jk.so 
# mod_jk 모듈 로딩

JkWordersFile conf/workers.properties 
# jk 모듈 실행을 위해 선언된 속성 값 (실행 대상 이름 등)

JkLogFile logs/mod_jk.log 
# mod_jk 모듈 실행중 발생하는 로그를 기록하는 파일 선언

JkLogLevel INFO 
# INFO 이상의 레벨에 대해 로깅

JkMount /* worker1  
# 도메인 / url로 접근한 경우 worker1 로 재전송
```

*workers.properties* 내용도 보겠습니다.

```shell
worker.list=worker1 
# 실행할 노드 서버 이름

worker.worker1.port=8009 
# Tomcat 에서 ajp 요청을 포트번호

worker.worker1.host=127.0.0.1 
# 톰캣 호스트 ip

worker.worker1.type=ajk13 
# 사용 중인 프로토콜 
```

### mod_proxy

mod_proxy는 Apache HTTP Server 를 위한 선택적 모듈입니다. 이 모듈은 Apache 용 프록시, 게이트웨이 또는 캐시를 구현합니다.

*httpd.conf* 에서 mod_proxy 모듈을 불러옵니다.

```shell
LoadModule proxy_module modules/mod_proxy.so
# mod_proxy 모듈 로딩

LoadModule proxy_http_module modules/mod_proxy_http.so
# mod_proxy_http 모듈 로딩
```

Apache 로 접근할 경우 프록시할 대상 Tomcat 서버에 정의합니다.

```xml
<VirtualHost *:80>
    ServerName helloworld.com
    ProxyRequests Off 
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8080/
    ProxyPassReverse / http://127.0.0.1:8080/
</VirtualHost>
```

### 동작 방식

1. Apache 웹서버의 httpd.conf 에 Tomcat 연동을 위한 설정을 추가하고 Tomcat 에서 처리할 요청을 지정한다.
2. 사용자의 브라우저는 Apache Web Server(포트 80)에 접속해 요청한다.
3. Apache Web Server 는 사용자의 요청이 Tomcat 에서 처리하도록 지정된 요청인지 확인 후, Tomcat에서 처리해야 하는 경우 Apache Web Server서버 는 Tomcat 의 AJP 포트(8009포트)에 접속해 요청을 전달한다.
4. Tomcat은 Apache Web Server 로부터 요청을 받아 처리한 후, 처리 결과를 Apache Web Server 에 되돌려 준다.
5. Apache Web Server 는 Tomcat으로부터 받은 처리 결과를 사용자에게 전송한다.

### Apache 와 Tomcat 을 연동 하는 이유

Tomcat 은 WAS 서버이지만 Web Server 의 기능도 갖추고 있는 WAS 서버입니다.

그러나 Tomcat 의 Web Server 기능은 Apache 보다 느린 속도처리를 보였고, 이로 인해 정적인 페이지는 Apache 가 처리하고, 동적인 페이지를 Tomcat 이 처리함으로써 부하를 분산하는 이유에서 Apache 와 Tomcat 을 연동하였습니다.

Tomcat 이 많이 발전해 Tomcat 내의 Web 서버가 Apache 에 절대 뒤쳐지지 않을만큼 역할을 수행합니다.

그럼에도 불구하고 아직도 Apache 와 Tomcat 을 연동하여 사용하는 이유는, Apache 내에서만 설정할 수 Load Balancing 이라는 부분이라던가 Apache 에서 제공하는 유용한 모듈들을 Tomcat 에서 사용할 수 없기 때문입니다.

### Packet Structure

> Request Packet

```
AJP13_FORWARD_REQUEST :=
    prefix_code      (byte) 0x02 = JK_AJP13_FORWARD_REQUEST
    method           (byte)
    protocol         (string)
    req_uri          (string)
    remote_addr      (string)
    remote_host      (string)
    server_name      (string)
    server_port      (integer)
    is_ssl           (boolean)
    num_headers      (integer)
    request_headers *(req_header_name req_header_value)
    attributes      *(attribut_name attribute_value)
    request_terminator (byte) OxFF
```

> Response Packet

```
AJP13_SEND_BODY_CHUNK := 
  prefix_code   3
  chunk_length  (integer)
  chunk        *(byte)


AJP13_SEND_HEADERS :=
  prefix_code       4
  http_status_code  (integer)
  http_status_msg   (string)
  num_headers       (integer)
  response_headers *(res_header_name header_value)

res_header_name := 
    sc_res_header_name | (string)   [see below for how this is parsed]

sc_res_header_name := 0xA0 (byte)

header_value := (string)

AJP13_END_RESPONSE :=
  prefix_code       5
  reuse             (boolean)


AJP13_GET_BODY_CHUNK :=
  prefix_code       6
  requested_length  (integer)
```

## References

http://tomcat.apache.org/connectors-doc/ajp/ajpv13a.html