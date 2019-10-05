## RESTful API

월드 와이드 웹(World Wide Web a.k.a WWW)과 같은 분산 하이퍼미디어 시스템을 위한 소프트웨어 아키텍처의 한 형식으로 자원을 정의하고 자원에 대한 주소를 지정하는 방법 전반에 대한 패턴
`REST`란, REpresentational State Transfer 의 약자이다.
여기에 `~ful` 이라는 형용사형 어미를 붙여 ~한 API 라는 표현으로 사용된다. 즉, REST 의 기본 원칙을 성실히 지킨 서비스 디자인은 ‘RESTful’하다라고 표현할 수 있다.
REST가 디자인 패턴이다, 아키텍처다 많은 이야기가 존재하는데, 하나의 아키텍처로 볼 수 있다. 좀 더 정확한 표현으로 말하자면, REST 는Resource Oriented Architecture이다. API 설계의 중심에 자원(Resource)이 있고 HTTP Method 를 통해 자원을 처리하도록 설계하는 것이다.

1. *리소스*와*행위*를 명시적이고 직관적으로 분리한다.
* 리소스는URI로 표현되는데 리소스가 가리키는 것은명사로 표현되어야 한다.
* 행위는HTTP Method로 표현하고,GET(조회),POST(생성),PUT(기존 entity 전체 수정),PATCH(기존 entity 일부 수정),DELETE(삭제)을 분명한 목적으로 사용한다.


URI 

 [https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn](https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn) 




## URI — Uniform Resource Identifier

[Uniform Resource Identifier](https://en.wikipedia.org/wiki/Uniform_resource_identifier)
URIs are a standard for identifying documents using a short string of numbers, letters, and symbols. They are defined by [RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax](https://tools.ietf.org/html/rfc3986) . URLs, URNs, and URCs are all/types/of URI.

## URL — Uniform Resource Locator
위치가 변할 수 있음

[Uniform Resource Locator](https://en.wikipedia.org/wiki/Uniform_resource_locator)
Contains information about how to fetch a resource from its location. For example:
* http://example.com/mypage.html
* ftp://example.com/download.zip
* mailto:user@example.com
* file:///home/user/file.txt
* tel:1-888-555-5555
* http://example.com/resource?foo=bar#fragment
* /other/link.html(A relative URL, only useful in the context of another URL)
URLs always start with a protocol (http) and usually contain information such as the network host name (example.com) and often a document path (/foo/mypage.html). URLs may have query parameters and fragment identifiers.


## URN — Uniform Resource Name
위치와 독립적

[Uniform Resource Name](https://en.wikipedia.org/wiki/Uniform_resource_name)
Identifies a resource by a unique and persistent name, but doesn’t necessarily tell you how to locate it on the internet. It usually starts with the prefixurn:For example:
* urn:isbn:0451450523 to identify a book by its ISBN number.
* urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66a globally unique identifier
* urn:publishing:book- An XML namespace that identifies the document as a type of book.
URNs can identify ideas and concepts. They are not restricted to identifying documents. When a URN does represent a document, it can be translated into a URL by a “resolver”. The document can then be downloaded from the URL.



*REST 6 가지 원칙*

* Uniform Interface

RESTful 웹 서비스에서 URI를 사용한다. 자원 자체는 개념적으로 고객에게 반환되는 표현과 분리된다. 예를 들어, 서버는 HTML, XML 또는 JSON으로 데이터베이스로부터 데이터를 전송할 수 있다. 이 중 어떤 것도 서버의 내부 표현이 아니다.
히들 근래에 REST를 이야기 하면, HTTP + JSON을 쉽게 떠올리는데, JSON은 하나의 옵션일뿐, 메시지 포맷을 꼭 JSON으로 적용해야할 필요는 없다. 자바스크립트가 유행하기전에만 해도 XML 형태를 많이 사용했으며, 근래에 들어서 사용의 편리성 때문에 JSON을 많이 사용하고 있다.

REST 애플리케이션의 초기 URI에 액세스한 경우(웹 사이트의 홈 페이지에 액세스하는 개인 웹 사용자와 유사), REST 클라이언트는 서버 제공 링크를 동적으로 사용하여 필요한 모든 사용 가능한 작업과 리소스를 검색할 수 있어야 한다. 접속이 진행됨에 따라, 서버는 현재 이용 가능한 다른 작업에 대한 하이퍼링크를 포함하는 텍스트로 응답한다.

* Stateless


상태가 있다 없다는 의미는 사용자나 클라이언트의 컨택스트를 서버쪽에 유지 하지 않는다는 의미로,쉽게 표현하면 HTTP Session과 같은 컨텍스트 저장소에 상태 정보를 저장하지 않는 형태를 의미한다.
상태 정보를 저장하지 않으면 각 API 서버는 들어오는 요청만을 들어오는 메시지로만 처리하면 되며, 세션과 같은 컨텍스트 정보를 신경쓸 필요가 없기 때문에 구현이 단순해진다.


* Caching

HTTP 프로토콜 표준에서 사용하는 “Last-Modified” 태그나 E-Tag를 이용하면 캐슁을 구현할 수 있다.
아래와 같이 Client가 HTTP GET을 “Last-Modified” 값과 함께 보냈을 때, 컨텐츠가 변화가 없으면 REST 컴포넌트는 “304 Not Modified”를 리턴하면 Client는 자체 캐쉬에 저장된 값을 사용하게 된다.

이렇게 캐쉬를 사용하게 되면 네트웍 응답시간 뿐만 아니라, REST 컴포넌트가 위치한 서버에 트렌젝션을 발생시키지 않기 때문에, 전체 응답시간과 성능 그리고 서버의 자원 사용률을 비약적으로 향상 시킬 수 있다.



* Client-Server

근래에 들면서 재 정립되고 있는 특징 중의 하나는 REST가 클라이언트 서버 구조라는 것이다. (당연한 것이겠지만).
REST 서버는 API를 제공하고, 제공된 API를 이용해서 비즈니스 로직 처리 및 저장을 책임진다.
클라이언트의 경우 사용자 인증이나 컨택스트(세션,로그인 정보)등을 직접 관리하고 책임 지는 구조로 역할이 나뉘어 지고 있다. 이렇게 역할이 각각 확실하게 구분되면서, 개발 관점에서 클라이언트와 서버에서 개발해야 할 내용들이 명확하게 되고 서로의 개발에 있어서 의존성이 줄어들게 된다.


* Hierarchical system

계층형 아키텍쳐 구조 역시 근래에 들어서 주목받기 시작하는 구조인데, 클라이언트 입장에서는 REST API 서버만 호출한다.
그러나 서버는 다중 계층으로 구성될 수 있다. 순수 비즈니스 로직을 수행하는 API 서버와 그 앞단에 사용자 인증 (Authentication), 암호화 (SSL), 로드밸런싱등을 하는 계층을 추가해서 구조상의 유연성을 둘 수 있는데, 이는 근래에 들어서 앞에서 언급한 마이크로 서비스 아키텍쳐의 api gateway나, 간단한 기능의 경우에는 HA Proxy나 Apache와 같은 Reverse Proxy를 이용해서 구현하는 경우가 많다.


* Code on demand

[RestFul API :: 개인적인공간](https://brownbears.tistory.com/35)



MIME

*MIME 타입*이란 클라이언트에게 전송된 문서의 다양성을알려주기 위한 메커니즘입니다:웹에서 파일의 확장자는 별 의미가 없습니다. 그러므로,각 문서와 함께 올바른MIME 타입을 전송하도록,서버가 정확히 설정하는 것이중요합니다.브라우저들은 리소스를 내려받았을 때해야 할 기본 동작이 무엇인지를 결정하기 위해 대게 MIME 타입을 사용합니다.

Proxy

*프록시 서버*( [영어](https://ko.wikipedia.org/wiki/%EC%98%81%EC%96%B4) :proxy server프록시 서버[])는 [클라이언트](https://ko.wikipedia.org/wiki/%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8) 가 자신을 통해서 다른 네트워크 서비스에 간접적으로 접속할 수 있게 해 주는 [컴퓨터 시스템](https://ko.wikipedia.org/wiki/%EC%BB%B4%ED%93%A8%ED%84%B0_%EC%8B%9C%EC%8A%A4%ED%85%9C) 이나 [응용 프로그램](https://ko.wikipedia.org/wiki/%EC%9D%91%EC%9A%A9_%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4) 을 가리킨다. [서버](https://ko.wikipedia.org/wiki/%EC%84%9C%EB%B2%84) 와 클라이언트 사이에 중계기로서 대리로 통신을 수행하는 것을 가리켜 ‘프록시’, 그 중계 기능을 하는 것을 프록시 서버라고 부른다.


TDD

함수형 프로그래밍

[일급 객체( First Class Object ) :: victolee](https://victorydntmd.tistory.com/46)

GIt vs Githug vs GitLab
CI / CD

CI

 - 개발자를 위한 자동화 프로세스
 - 개발자간의 코드 충돌을 방지하기 위한 목적
 - 정기적인 빌드 및 테스트(유닛테스트 및 통합테스트)를 거쳐 공유 레포지터리에 병합되는 과정 -> Merge


CD

# 4. CD(1) - Continuous Delivery
 - 애플리케이션에 적용한 변경사항이 버그 테스트를 거쳐 레포지터리에 자동으로 업로드 되는 것
 - 운영팀은 언제든 실시간으로 이 레포지터리에서 실시간으로 프로덕션 환경으로 배포 가능


# 5. CD(2) - Continuous Deployment
 - 애플리케이션을 프로덕션 환경으로 배포하는 작업을 자동화 하는 것
 - 서버가 여러 대 일 경우 더욱 중요
 - Continuous Delivery로 통칭하여언급하기도 함

배포


# 이진트리 포화이진트리 편향트리 완전이진트리
