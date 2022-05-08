---
title:  "Java 9 New Features"
excerpt: "Java 9 New Features"
categories:
  - Programming
tags:
  - Programming
  - Java
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

새로운 LTS 버전인 JDK 9가 2017년 9월 21일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 9](https://openjdk.java.net/projects/jdk/9/)를 참고했습니다.

## Features

### JEP 102: Process API Updates

운영 체제 프로세스를 제어하고 관리하기 위한 API를 개선합니다.

#### Description

Java SE는 기본 운영 체제 프로세스에 대한 제한된 지원을 제공합니다. 환경을 설정하고 프로세스를 시작하기 위한 기본 API를 제공합니다. 프로세스 스트림은 Java SE 7부터 파일, 파이프로 리디렉션되거나 상속될 수 있습니다. 일단 시작되면 API를 사용하여 프로세스를 파괴하거나 프로세스가 종료될 때까지 기다릴 수 있습니다.

`java.lang.Process` 클래스는 프로세스의 운영 특정 프로세스 ID, 인수를 포함하는 프로세스에 대한 정보, 명령, 프로세스 시작 시간, 프로세스의 누적 CPU 시간 및 사용자 이름을 제공하도록 향상되었습니다.

`java.lang.ProcessHandle` 클래스는 프로세스 ID, 인수(arguments), 명령(command), 시작 시간(star time) 등을 포함하여 운영 체제에서 제공하는 각 프로세스에 대한 정보를 반환합니다. `ProcessHandle`은 `ProcessHandles`의 스트림입니다.

`ProcessHandles`는 프로세스를 파괴하고 프로세스 활성을 모니터링하는 데 사용할 수 있습니다. `ProcessHandle.onExit`를 사용하면 `CompletableFuture`의 비동기 메커니즘을 사용하여 프로세스가 종료될 때 수행할 작업을 예약할 수 있습니다.

프로세스 및 프로세스 제어에 대한 정보에 대한 액세스는 보안 관리자 권한의 적용을 받으며 일반 운영 체제 액세스 제어에 의해 제한됩니다.

### JEP 110: HTTP 2 Client

HTTP/2 및 WebSocket을 구현하고 기존 `HttpURLConnection` API를 대체할 수 있는 새 HTTP 클라이언트 API를 정의합니다. API는 JDK 9와 함께 [JEP 11](https://openjdk.java.net/jeps/11)에 정의된 인큐베이터 모듈로 제공됩니다. 이는 다음을 의미합니다.

* API 및 구현은 Java SE의 일부가 아닙니다.
* API는 `jdk.incubtor` 네임스페이스 아래에 있습니다.
* 모듈은 기본적으로 컴파일이나 런타임에 해결되지 않습니다.

#### Goals

* 단순 차단 모드를 포함하여 일반적인 경우에 사용하기 쉬워야 합니다.
* "헤더 수신", 오류 및 "응답 본문 수신"과 같은 이벤트 알림을 제공해야 합니다. 이 알림은 반드시 콜백을 기반으로 하는 것은 아니지만 `CompletableFuture`와 같은 비동기 메커니즘을 사용할 수 있습니다.
* 애플리케이션 요구 사항의 80-90%를 충족하는 간단하고 간결한 API입니다. 이것은 아마도 프로토콜의 모든 기능을 반드시 노출하지는 않는 비교적 작은 API footprint를 의미할 것입니다.
* 서버에 대한 HTTP 프로토콜 요청의 모든 관련 측면과 서버의 응답(헤더, 본문, 상태 코드 등)을 노출해야 합니다.
* 표준 및 공통 인증 메커니즘을 지원해야 합니다. 처음에는 기본 인증으로만 제한됩니다.
* WebSocket 핸드셰이크를 쉽게 설정할 수 있어야 합니다.
* HTTP/2를 지원해야 합니다. (HTTP/2의 응용 프로그램 수준 의미는 유선 프로토콜이 완전히 다르지만 대부분 1.1과 동일합니다.)
* 1.1에서 2로의 업그레이드를 협상할 수 있어야 합니다(또는 그렇지 않음). 또는 처음부터 2를 선택할 수 있어야 합니다.
* 서버 푸시, 즉 클라이언트의 명시적인 요청 없이 클라이언트에 리소스를 푸시하는 서버의 기능을 지원해야 합니다.
* 기존 네트워킹 API와 일치하는 보안 검사를 수행해야 합니다.
* 람다 식과 같은 새로운 언어 기능에 친숙해야 합니다.
* 임베디드 시스템 요구 사항, 특히 영구적으로 실행되는 타이머 스레드 방지에 친숙해야 합니다.
* HTTPS/TLS를 지원해야 합니다.
* HTTP/1.1에 대한 성능 요구 사항:
  * 성능은 기존 `HttpURLConnection` 구현과 동등해야 합니다.
  * 성능은 Apache HttpClient 라이브러리와 동등해야 하며 클라이언트 API로 사용할 경우 Netty 및 Jetty와 동등해야 합니다.
  * 새 API의 메모리 사용량은 클라이언트 API로 사용할 때 `HttpURLConnection`, Apache HttpClient, Netty 및 Jetty와 같거나 낮아야 합니다.
* HTTP/2에 대한 성능 요구 사항:
  * 성능은 플랫폼 제한(예: TCP 세그먼트 승인 창)에도 불구하고 새 프로토콜에서 기대하는 방식(예: 확장성 및 대기 시간)에서 HTTP/1.1보다 우수해야 합니다.
  * HTTP/2용 클라이언트 API로 사용할 때 성능은 Netty 및 Jetty와 동등해야 합니다.
  * 새 API의 메모리 사용량은 `HttpURLConnection`, Apache HttpClient, Netty 및 Jetty를 클라이언트 API로 사용할 때보다 같거나 낮아야 합니다.
* 새로운 API는 가능한 모든 사용 사례를 다루는 것보다 단순성과 사용 용이성을 강조하기 때문에 성능 비교는 비교 가능한 작동 모드의 맥락에서만 이루어집니다.
* 이 작업은 JDK 9를 위한 것입니다. 일부 코드는 Servlet 4.0 API의 HTTP/2 구현에서 Java EE에 의해 재사용될 수 있으므로 JDK 8 언어 기능과 가능한 경우 API만 사용됩니다.
* JDK 9에서 API를 사용한 경험의 이점을 통해 JDK 10의 java.net 네임스페이스에서 Java SE의 API를 표준화하는 것이 가능합니다. 이러한 일이 발생하면 향후 JEP의 일부로 API, 더 이상 인큐베이터 모듈로 존재하지 않습니다.

#### Description

HTTP 클라이언트, 요청 및 응답에 대해 별도의 클래스가 정의된 JDK 9에 대해 일부 프로토타이핑 작업이 수행되었습니다. 빌더 패턴은 변경 불가능한 제품에서 변경 가능한 엔티티를 분리하는 데 사용되었습니다. 송수신을 위한 동기 차단 모드가 정의되어 있으며 `java.util.concurrent.CompletableFuture`에 구축된 비동기 모드도 정의되어 있습니다.

프로토타입은 선택기로 구현된 비동기 동작과 외부적으로 제공되는 ExecutorServices로 NIO SocketChannels에 구축되었습니다.

프로토타입 구현은 독립 실행형이었습니다. 즉, 호환성을 보장하고 모든 기능이 처음부터 지원되지 않아야 하는 단계적 접근을 허용하기 위해 기존 스택이 변경되지 않았습니다.

프로토타입 API에는 다음도 포함됩니다.

* Servlet 및 HTTP 서버 API와 같은 별도의 요청 및 응답
* 다음 이벤트에 대한 비동기식 알림:
  * Response headers received,
  * Response error,
  * Response body received, and
  * Server push (HTTP/2 only);
* HTTPS, via SSLEngine
* Proxying
* Cookies
* Authentication.

추가 작업이 필요할 가능성이 가장 높은 API 부분은 HTTP/2 다중 응답(서버 푸시) 및 HTTP/2 구성을 지원하는 것입니다. 프로토타입 구현은 거의 모든 HTTP/1.1을 지원하지만 아직 HTTP/2는 지원하지 않습니다.

HTTP/2 프록시는 다음 변경 사항에서 구현됩니다.

### JEP 143: Improve Contended Locking

경합하는 Java 개체 성능을 향상시킵니다.

#### Goals 

다음 벤치마크 및 테스트에 의해 측정된 경합 Java 개체 모니터의 전체 성능을 개선합니다.

* CallTimerGrid (though more of a stress test than a benchmark)
* Dacapo-bach (was dacapo2009)
* _avrora
* _batik
* _fop
* _h2
* _luindex
* _lusearch
* _pmd
* _sunflow
* _tomcat
* _tradebeans
* _tradesoap
* _xalan
* DerbyContentionModelCounted
* HighContentionSimulator
* LockLoops-JSR166-Doug-Sept2009 (was LockLoops)
* PointBase
* SPECjbb2013-critical (was specjbb2005)
* SPECjbb2013-max
* specjvm2008
* volano29 (was volano2509)

### JEP 158: Unified JVM Logging

JVM의 모든 구성 요소에 대한 공통 로깅 시스템을 도입합니다.

#### Goals

* 모든 로깅에 대한 공통 명령줄 옵션
* 로그 메시지는 태그를 사용하여 분류됩니다(예: 컴파일러, gc, classload, metaspace, svc, jfr, ...). 하나의 메시지에 여러 태그(태그 집합)가 있을 수 있습니다.
* 로깅은 `error`, `warning`, `info`, `debug`, `trace`, `develop`과 같은 다양한 수준에서 수행됩니다.
* 레벨에 따라 어떤 메시지를 기록할지 선택할 수 있습니다.
* 로깅을 콘솔 또는 파일로 리디렉션할 수 있습니다.
* 기본 구성은 경고 및 오류 수준을 사용하는 모든 메시지가 `stderr`로 출력되는 것입니다.
* 보관할 파일의 크기 및 수에 따른 로그 파일 회전(현재 GC 로그에 사용 가능한 것과 유사)
* 한 번에 한 줄씩 인쇄(같은 줄 내에서 인터리빙 없음)
* 로깅 메시지는 사람이 읽을 수 있는 일반 텍스트로 되어 있습니다.
* 메시지를 "장식(decorated)"할 수 있습니다. 기본 장식은 **uptime**, **level**, **tags** 입니다.
* 출력할 장식을 할수 있습니다.
* 기존 `tty->print...` 로깅은 통합 로깅을 출력으로 사용해야 합니다.
* 로깅은 jcmd 또는 MBean을 통해 런타임에 동적으로 구성할 수 있습니다.
* 테스트 및 지원됨 -- 사용자/고객이 활성화한 경우 충돌하지 않아야 함

Stretched goals:

* 여러 줄 로깅: 출력할 때 여러 줄을 함께(인터리브되지 않음) 유지하는 방식으로 기록할 수 있습니다.
* 개별 로그 메시지 활성화/비활성화(예: `__FILE__` / `__LINE__` 사용)
* `syslog` 및 `Windows` 이벤트 뷰어 출력 구현
* 장식을 출력할 순서를 구성할 수 있습니다.

#### Description

##### Tags

로깅 프레임워크는 JVM에서 태그 세트를 정의합니다. 각 태그는 이름으로 식별됩니다(예: gc, 컴파일러, 스레드 등). 태그 세트는 필요에 따라 소스 코드에서 변경할 수 있습니다. 로그 메시지가 추가되면 기록된 정보를 분류하는 태그 세트와 연결되어야 합니다. 태그 세트는 하나 이상의 태그로 구성됩니다.

##### Levels

각 로그 메시지에는 연결된 로깅 수준이 있습니다. 사용 가능한 수준은 `error`, `warning`, `info`, `debug`, `trace` 순서로 개발입니다. `develop` 수준은 제품이 아닌 빌드에서만 사용할 수 있습니다.

각 출력에 대해 로깅 수준을 구성하여 해당 출력에 기록되는 정보의 양을 제어할 수 있습니다. 대안으로 off는 로깅을 완전히 비활성화합니다.

##### Decorations

로깅 메시지는 메시지에 대한 정보로 장식됩니다. 다음은 가능한 장식 목록입니다.

* `time` -- ISO-8601 형식의 현재 시간 및 날짜
* `uptime` -- JVM 시작 이후의 시간(초 및 밀리초)(예: 6.567초)
* `timemillis` -- `System.currentTimeMillis()`에 의해 생성된 것과 동일한 값
* `uptimemillis` -- JVM이 시작된 후 밀리초
* `timenanos` -- `System.nanoTime()`에 의해 생성된 것과 동일한 값
* `uptimenanos` -- JVM이 시작된 이후의 나노초
* `pid` -- 프로세스 식별자
* `tid` -- 스레드 식별자
* `level` -- 로그 메시지와 관련된 레벨
* `tags` -- 로그 메시지와 연결된 태그 집합
  
각 출력은 사용자 지정 데코레이터 집합을 사용하도록 구성할 수 있습니다. 그래도 순서는 항상 위에 있습니다. 사용할 장식은 런타임에 사용자가 구성할 수 있습니다. 장식은 로그 메시지에 추가됩니다.

Example: `[6.567s][info][gc,old] Old collection complete`

### JEP 165: Compiler Control

JVM 컴파일러를 제어하는 개선된 방법을 제안합니다. 런타임 관리가 가능한 메서드 종속 컴파일러 플래그를 활성화합니다.

#### Goals

* JVM 컴파일러(C1 및 C2)의 세분화된 메서드 컨텍스트 종속 제어
* 런타임에 JVM 컴파일러 제어 옵션을 변경하는 기능
* 성능 저하 없음

### JEP 193: Variable Handles

개체 필드 및 배열 요소에 대한 다양한 `java.util.concurrent.atomic` 및 `sun.misc.Unsafe` 작업의 등가물을 호출하는 표준 수단, 세분화된 메모리 순서 제어를 위한 표준 펜스 작업 집합 및 표준 도달 가능성을 정의합니다. `-fence` 작업을 통해 참조된 개체가 강력하게 도달할 수 있는 상태로 유지됩니다.

#### Goals

* Safety. Java Virtual Machine을 손상된 메모리 상태에 두는 것이 불가능해야 합니다. 예를 들어, 개체의 필드는 필드 유형으로 캐스트 가능한 인스턴스로만 업데이트할 수 있으며, 배열 인덱스가 배열 범위 내에 있는 경우 배열 내에서만 배열 요소에 액세스할 수 있습니다.
* Integrity. 객체의 필드에 대한 액세스는 객체의 최종 필드를 업데이트할 수 없다는 제약 외에 getfield 및 putfield 바이트 코드와 동일한 액세스 규칙을 따릅니다. (참고: 이러한 안전 및 무결성 규칙은 필드에 대한 읽기 또는 쓰기 액세스 권한을 부여하는 MethodHandles에도 적용됩니다.)
* Performance. 성능 특성은 `sun.misc.Unsafe` 작업과 동일하거나 유사해야 합니다(특히 생성된 어셈블러 코드는 접을 수 없는 특정 안전 검사를 모듈로 거의 동일해야 함).
* Usability. API는 `sun.misc.Unsafe` API보다 우수해야 합니다.

API가 `java.util.concurrent.atomic` API만큼 좋은 것이 바람직하지만 필수는 아닙니다.

### JEP 197: Segmented Code Cache

성능을 개선하고 향후 확장을 가능하게 하려면 코드 캐시를 특정 유형의 컴파일된 코드를 포함하는 고유한 세그먼트로 나눕니다.

#### Goals

* 비 메소드, 프로파일 및 비 프로파일 코드 분리
* 비 메소드 코드를 건너 뛰는 특수 반복기로 인한 더 짧은 스윕 시간
* 일부 컴파일 집약적 벤치마크의 실행 시간 개선
* JVM 메모리 풋프린트의 더 나은 제어
* 고도로 최적화된 코드의 단편화 감소
* 동일한 유형의 코드가 제때에 액세스될 가능성이 높기 때문에 코드 지역성 향상
  * 더 나은 iTLB 및 iCache 동작
* 향후 확장 기반 구축
  * 이기종 코드 관리 개선 예를 들어 수마트라(GPU 코드) 및 AOT 컴파일 코드
  * 코드 힙당 세분화된 잠금 가능성
  * 코드와 메타데이터의 향후 분리

#### Description

단일 코드 힙 대신 코드 캐시가 고유한 코드 힙으로 분할되며 각 코드 힙에는 특정 유형의 컴파일된 코드가 포함됩니다. 이러한 디자인을 통해 다른 속성을 가진 코드를 분리할 수 있습니다. 컴파일된 코드에는 세 가지 다른 최상위 유형이 있습니다.

* JVM 내부(비메서드) 코드
* 프로파일링된 코드
* 프로파일링되지 않은 코드

해당 코드 힙은 다음과 같습니다.

* 컴파일러 버퍼 및 바이트 코드 인터프리터와 같은 비 메소드 코드를 포함하는 비 메소드 코드 힙. 이 코드 유형은 코드 캐시에 영원히 남습니다.
* 수명이 짧은 프로파일링된 메서드가 포함된 프로파일링된 코드 힙입니다.
* 잠재적으로 긴 수명을 가진 완전히 최적화되고 프로파일링되지 않은 메서드가 포함된 프로파일링되지 않은 코드 힙입니다.

비메서드 코드 힙은 VM 내부와 컴파일러 버퍼를 위한 추가 공간을 설명하기 위해 3MB의 고정 크기를 갖습니다. 이 추가 공간은 C1/C2 컴파일러 스레드 수에 따라 조정됩니다. 나머지 코드 캐시 공간은 프로파일링된 코드 힙과 프로파일링되지 않은 코드 힙 간에 균등하게 분배됩니다.

코드 힙의 크기를 제어하기 위해 아래 명령어가 도입되었습니다.

* `-XX:NonProfiledCodeHeapSize`: 프로파일링되지 않은 메소드를 포함하는 코드 힙의 크기를 바이트 단위로 설정합니다.
* `-XX:ProfiledCodeHeapSize`: 프로파일링된 메소드를 포함하는 코드 힙의 크기를 바이트 단위로 설정합니다.
* `-XX:NonMethodCodeHeapSize`: 비 메소드 코드를 포함하는 코드 힙의 크기를 바이트 단위로 설정합니다.

코드 캐시의 인터페이스와 구현은 여러 코드 힙을 지원하도록 조정되었습니다. 코드 캐시는 JVM의 중심 구성 요소이기 때문에 다음을 비롯한 많은 다른 구성 요소가 이러한 변경의 영향을 받습니다.

* 코드 캐시 스위퍼: 이제 메서드 코드 힙에 대해서만 반복됩니다.
* 계층형 컴파일 정책: 코드 힙의 여유 공간에 따라 컴파일 임계값을 설정합니다.
* JFR(Java Flight Recorder): 코드 캐시와 관련된 이벤트
* 간접 참조:
  * Serviceability Agent: 코드 캐시 내부에 대한 Java 인터페이스
  * DTrace ustack 도우미 스크립트(jhelper.d): 컴파일된 Java 메서드의 이름 확인
  * Pstack 지원 라이브러리(libjvm_db.c): 컴파일된 Java 메서드의 스택 추적

### JEP 199: Smart Java Compilation, Phase Two

JDK 빌드에서 기본적으로 사용할 수 있도록 `sjavac` 도구를 개선하고 JDK 이외의 대규모 프로젝트를 빌드하는 데 사용할 수 있도록 일반화합니다.

#### Goals

안정성 및 이식성과 관련된 다양한 문제로 인해 `sjavac`는 JDK 빌드 스크립트에서 기본적으로 사용되지 않습니다. 이 JEP의 첫 번째 목표는 이러한 문제를 해결하는 것입니다. 여기에는 도구가 항상 모든 소프트웨어/하드웨어 구성에서 신뢰할 수 있는 결과를 생성하는지 확인하는 작업이 포함됩니다.

가장 중요한 목표는 `sjavac`가 대규모 임의의 Java 프로젝트를 컴파일할 수 있는 범용 `javac` 래퍼 역할을 할 수 있을 정도로 `sjavac`의 품질을 향상시키는 것입니다.

후속 프로젝트는 `sjavac`가 JDK 도구 체인에 노출되는 방법을 탐구할 것입니다. 이것은 별도의 지원되는 독립 실행형 도구, 지원되지 않는 독립 실행형 도구, `javac`와의 통합 또는 다른 것일 수 있습니다.

#### Description

##### Current scheme

대부분의 JDK 소스 코드는 오늘날 대략 1997년으로 거슬러 올라가는 체계로 구성되어 있습니다. 축약 형식:

```
src/{share,$OS}/{classes,native}/$PACKAGE/*.{java,c,h,cpp,hpp}
```

where:

* `$OS` 디렉토리에는 운영 체제별 코드가 포함되어 있습니다. 여기서 `$OS`는 Solaris, Windows 등 중 하나입니다.
* 클래스 디렉토리에는 Java 소스 파일과 리소스 파일이 포함될 수 있습니다.
* 기본 디렉토리에는 C 또는 C++ 소스 파일이 포함되어 있습니다.
* `$PACKAGE`는 관련 Java API 패키지 이름이며 마침표는 슬래시로 대체됩니다.

간단한 예를 들자면, jdk 저장소의 `java.lang.Object` 클래스에 대한 소스 코드는 하나는 Java로, 다른 하나는 C로 두 개의 파일에 있습니다. 

```
src/share/classes/java/lang/Object.java
          native/java/lang/Object.c
```

덜 간단한 예에서 package-private `java.lang.ProcessImpl` 및 `ProcessEnvironment` 클래스의 소스 코드는 운영 체제에 따라 다릅니다. Unix 계열 시스템의 경우 세 파일에 있습니다.

```
src/solaris/classes/java/lang/ProcessImpl.java
                              ProcessEnvironment.java
            native/java/lang/ProcessEnvironment_md.c
```

`src/{share,$OS}` 아래에는 다음을 포함하여 현재 구조와 일치하지 않는 소수의 디렉토리가 있습니다.

```
Directory                     Content
--------------------------    --------------------------
src/{share,$OS}/back          JDWP back end
                bin           Java launcher
                instrument    Instrumentation support
                javavm        Exported JVM include files
                lib           Files for $JAVA_HOME/lib
                transport     JDWP transports
```

##### New scheme

JDK의 모듈화는 유지 관리를 더 쉽게 하기 위해 소스 코드를 완전히 재구성할 수 있는 드문 기회를 제공합니다. 핫스팟을 제외한 JDK 포리스트의 모든 리포지토리에서 다음 체계를 구현합니다.

```
src/$MODULE/{share,$OS}/classes/$PACKAGE/*.java
                        native/include/*.{h,hpp}
                               $LIBRARY/*.{c,cpp}
                        conf/*
                        legal/*
```

where:

* `$MODULE`은 모듈 이름(`예: java.base`)입니다.
* 공유 디렉토리에는 이전과 같이 플랫폼 간 공유 코드가 포함되어 있습니다.
* `$OS` 디렉토리에는 이전과 같이 운영 체제별 코드가 포함되어 있습니다. 여기서 `$OS`는 유닉스, Windows 등 중 하나입니다.
* 클래스 디렉토리에는 이전과 같이 API `$PACKAGE` 계층을 반영하는 디렉토리 트리로 구성된 Java 소스 파일과 리소스 파일이 포함되어 있습니다.
* 네이티브 디렉토리에는 이전과 마찬가지로 C 또는 C++ 소스 파일이 포함되어 있지만 다르게 구성되어 있습니다.
  * 포함 디렉토리에는 외부 사용을 위해 내보낼 C 또는 C++ 헤더 파일(예: jni.h)이 포함되어 있습니다.
  * C 또는 C++ 소스 파일은 컴파일된 코드가 링크될 공유 라이브러리 또는 DLL의 이름(예: libjava 또는 libawt)인 `$LIBRARY` 디렉토리에 위치합니다.
* `conf` 디렉토리에는 최종 사용자가 편집할 구성 파일(예: `net.properties`)이 포함되어 있습니다.
* 법적 디렉토리에는 법적 고지가 포함되어 있습니다.

이전 예제를 다시 변환하기 위해 `java.lang.Object` 클래스의 소스 코드는 다음과 같이 배치됩니다.

```
src/java.base/share/classes/java/lang/Object.java
                    native/libjava/Object.c
```

`package-private java.lang.ProcessImpl` 및 `ProcessEnvironment` 클래스의 소스 코드는 다음과 같이 배치됩니다.

```
src/java.base/unix/classes/java/lang/ProcessImpl.java
                                     ProcessEnvironment.java
                   native/libjava/ProcessEnvironment_md.c
```

현재 구조와 일치하지 않는 현재 `src/{share,$OS}` 아래의 디렉토리 내용이 이제 적절한 모듈에 있습니다.

```
Directory                     Module
--------------------------    --------------------------
src/{share,$OS}/back          jdk.jdwp.agent
                bin           java.base
                instrument    java.instrument
                javavm        java.base
                lib           $MODULE/{share,$OS}/conf
                transport     jdk.jdwp.agent
```

최종 사용자가 편집할 수 없는 현재 `lib` 디렉토리의 파일은 이제 리소스 파일입니다.

### JEP 200: The Modular JDK

JDK 빌드에서 기본적으로 사용할 수 있도록 `sjavac` 도구를 개선하고 JDK 이외의 대규모 프로젝트를 빌드하는 데 사용할 수 있도록 일반화합니

#### Goals

안정성 및 이식성과 관련된 다양한 문제로 인해 sjavac는 JDK 빌드 스크립트에서 기본적으로 사용되지 않습니다. 이 JEP의 첫 번째 목표는 이러한 문제를 해결하는 것입니다. 여기에는 도구가 항상 모든 소프트웨어/하드웨어 구성에서 신뢰할 수 있는 결과를 생성하는지 확인하는 작업이 포함됩니다.

### JEP 201: Modular Source Code

JSR 376에 의해 지정되고 [JEP 261](https://openjdk.java.net/jeps/261)에 의해 구현된 Java 플랫폼 모듈 시스템을 사용하여 JDK를 모듈화합니다.

#### Goals

JDK를 컴파일 시간, 빌드 시간 및 런타임에 다음을 포함하되 이에 국한되지 않는 다양한 구성으로 결합할 수 있는 일련의 모듈로 나눕니다.

### JEP 211: Elide Deprecation Warnings on Import Statements

Java SE 8부터 Java 컴파일러는 더 이상 사용되지 않는 유형을 이름으로 가져오거나 더 이상 사용되지 않는 멤버(메서드, 필드, 중첩 유형)를 정적으로 가져올 때 사용 중단 경고를 발행하기 위해 Java 언어 사양을 합리적으로 해석해야 합니다. 이러한 경고는 정보가 아니며 필요하지 않아야 합니다. 사용되지 않는 멤버의 실제 사용에 대한 사용 중지 경고는 그대로 유지되어야 합니다.

#### Goals

이 JEP의 목표는 큰 코드 기반에서 경고를 제거하는 것을 용이하게 하는 것입니다. 가져오기에 대한 사용 중단 경고는 코드에서 사용되지 않는 멤버를 사용하는 것과 달리 `@SuppressWarnings` 주석을 사용하여 억제할 수 없습니다. JDK와 같은 대규모 코드 기반에서 사용되지 않는 기능은 종종 일정 시간 동안 지원되어야 하며 사용되지 않는 구성의 모든 사용이 의도적이고 억제된 경우 사용되지 않는 구성을 가져오는 것만으로는 경고 메시지가 정당화되지 않습니다.

#### Description

사양 측면에서 필요한 변경 사항은 적습니다. JLS 8에서 `@Deprecated`에 대한 섹션은 다음과 같습니다.

Java 컴파일러는 선언에 `@Deprecated` 주석이 달린 유형, 메서드, 필드 또는 생성자가 명시적 또는 암시적으로 선언된 구성에서 사용(이름으로 재정의, 호출 또는 참조)될 때 사용 중단 경고를 생성해야 합니다.

* `@Deprecated` 주석으로 자체 주석이 달린 엔티티 내에서 사용됩니다.
* `@SuppressWarnings("deprecation")` 주석으로 경고를 표시하지 않도록 주석이 달린 엔티티 내에서 사용됩니다.
* 사용 및 선언은 모두 동일한 가장 바깥쪽 클래스 내에 있습니다.

사양 변경은 추가 제외를 나타내는 다른 글머리 기호를 추가하는 것과 같습니다.

* 사용은 `import` 문 내에서 이루어집니다.
  
`javac` 참조 구현에서는 사용 중단 경고를 찾을 때 `import` 문을 건너뛰는 간단한 검사가 있습니다.

### JEP 212: Resolve Lint and Doclint Warnings

JDK 코드 베이스에는 `javac`에서 보고한 수많은 `lint` 및 `doclint` 오류가 포함되어 있습니다. 이러한 경고는 최소한 플랫폼의 기본 부분에 대해 해결되어야 합니다.

### JEP 213: Milling Project Coin

JDK 7/Java SE 7의 일부로 Project Coin/JSR 334에 포함된 작은 언어 변경 사항은 사용하기 쉽고 실제로 잘 작동했습니다. 그러나 몇 가지 수정 사항을 통해 이러한 변경의 거친 부분을 해결할 수 있습니다. 또한, 식별자로 밑줄("`_`")을 사용하면 Java SE 8부터 경고가 발생하므로 Java SE 9에서는 오류로 전환되어야 합니다. 또한 인터페이스에 `private` 메서드를 허용하도록 제안합니다.

#### Description

Java 프로그래밍 언어에 대한 다섯 가지 작은 수정 사항이 제안됩니다.

* 개인 인스턴스 메소드에서 `@SafeVargs`를 허용하십시오.
* `try-with-resources` 문에서 효과적인 최종 변수를 리소스로 사용할 수 있습니다.
* 유추된 유형의 인수 유형이 표시 가능한 경우 익명 클래스가 있는 다이아몬드를 허용합니다.
* Java SE 8에서 시작된 법적 식별자 이름 집합에서 밑줄 제거를 완료합니다.
* 인터페이스에서 개인 메서드에 대한 지원은 Lambda 표현식에 대한 지원을 추가하기 위한 노력의 일환으로 Java SE 8에 포함하기 위해 잠시 고려되었지만 Java SE 8에 대해 더 높은 우선 순위 작업에 더 집중할 수 있도록 철회되었습니다. 이제 지원이 제안되었습니다. 개인 인터페이스 메서드를 수행하여 인터페이스의 비추상 메서드가 코드를 공유할 수 있도록 합니다.

### JEP 214: Remove GC Combinations Deprecated in JDK 8

[JEP 173](https://openjdk.java.net/jeps/173)을 통해 JDK 8에서 이전에 사용되지 않는 GC 조합을 제거합니다.

#### Description

JEP 173에서 더 이상 사용되지 않는 것으로 나열된 GC 조합을 제어하는 ​​플래그와 CMS 전경 수집기를 활성화하는 플래그(JDK-8027876의 일부로 사용되지 않음)가 코드 베이스에서 제거됩니다. 이는 더 이상 경고 메시지가 인쇄되지 않음을 의미합니다. 대신 이러한 플래그가 사용되는 경우 JVM이 시작되지 않습니다.

플래그가 제거되면 현재 죽은 코드는 GC 코드 기반에서 제거됩니다. 이 작업으로 인해 수행할 수 있지만 범위가 큰 코드 기반에 단순화가 있을 수 있습니다. 이러한 단순화는 별도의 변경으로 분리될 수 있습니다.

다음은 작동을 중지할 플래그 및 플래그 조합에 대한 자세한 요약입니다.

```
DefNew + CMS       : -XX:-UseParNewGC -XX:+UseConcMarkSweepGC
ParNew + SerialOld : -XX:+UseParNewGC
ParNew + iCMS      : -Xincgc
ParNew + iCMS      : -XX:+CMSIncrementalMode -XX:+UseConcMarkSweepGC
DefNew + iCMS      : -XX:+CMSIncrementalMode -XX:+UseConcMarkSweepGC -XX:-UseParNewGC
CMS foreground     : -XX:+UseCMSCompactAtFullCollection
CMS foreground     : -XX:+CMSFullGCsBeforeCompaction
CMS foreground     : -XX:+UseCMSCollectionPassing
```

ParNew + SerialOld 조합의 경우 이 JEP에 대한 작업에는 ParNew + SerialOld와 ParallelScavenge + SerialOld를 비교하는 성능 테스트도 포함됩니다. 그러면 ParNew + SerialOld에서 ParallelScavenge + SerialOld로 마이그레이션하기 위한 조정 제안이 나타납니다.

### JEP 215: Tiered Attribution for javac

인수 위치에서 폴리 표현식의 속성을 가속화하기 위해 `javac`에서 새로운 메소드 유형 검사 전략을 구현하십시오.

#### Goals

다음을 제공하는 TA(계층형 속성)인 유형 검사 폴리 표현식에 대한 새로운 접근 방식을 구현합니다.

주어진 표현식에 속성을 부여하는 데 필요한 (중복) 패스 수를 줄이는 접근 방식을 구현하여 성능을 개선하고,

현재 유형 검사 구현과 동일한 결과입니다.

### JEP 216: Process Import Statements Correctly

`import` 문의 순서에 관계없이 프로그램을 적절하게 수락 및 거부하도록 `javac`를 수정하고 절을 확장 및 구현합니다.

#### Description

`javac`는 클래스를 컴파일할 때 여러 단계를 사용합니다. 가져오기 처리를 고려할 때 두 가지 중요한 단계는 다음과 같습니다.

* 제공된 AST를 통해 클래스 및 인터페이스 선언을 찾는 유형 확인
* 다음을 포함하는 해결책
  * (1a) `T`가 최상위인 경우 `T`를 정의하는 소스 파일의 가져오기가 처리되고 가져온 멤버가 `T`의 범위에 추가됩니다.
  * (1b) `T`가 중첩된 경우 `T`를 직접 둘러싸는 클래스의 해상도(있는 경우)
  * (2) `T`의 확장/구현 절은 유형 검사됩니다.
  * (3) `T`의 유형 변수는 유형 검사됩니다.

위의 단계는 클래스의 상위 유형, 유형 변수 및 멤버를 결정하는 것을 포함하는 `javac`의 클래스 해석 프로세스의 일부입니다.

이 작업이 실제로 진행되는 것을 보려면 다음 코드를 고려하십시오.

```java
package P;

import static P.Outer.Nested.*;
import P.Q.*;

public class Outer {
    public static class Nested implements I {
    }
}

package P.Q;
public interface I {
}
```

유형 분석 단계에서 유형 `P.Outer`, `P.Outer.Nested` 및 `P.Q.I`가 존재하는 것으로 인식됩니다. 그런 다음 `P.Outer` 클래스를 분석해야 하는 경우 멤버 확인 단계는 다음과 같이 작동합니다.

```
1.	Resolution of P.Outer starts
2.	  Processing of the import static P.Outer.Nested.*; starts, per 1a, which means the members of P.Outer.Nestedand its transitive supertypes are looked up.
3.	    Resolution of the P.Outer.Nested class starts (the static imports can also import inherited types)
4.	      Triggers resolution of P.Outer, which is skipped as it is already in progress
5.	      Type checking of I(the implements clause) runs, but Icannot be resolved since it is not in the scope yet.
6.	    Resolution of import P.Q.*starts, which takes all member types of P.Q(including the interface I) and imports them into the current file's scope
7.	Resolution of P.Outerand other classes continues
```

위의 문제는 수입 처리와 관련된 유일한 문제가 아닙니다. 다른 알려진 문제는 클래스의 유형 매개변수 범위가 선언하는 클래스의 가능한 내부 클래스를 유효하게 참조할 수 있다는 것입니다. 어떤 경우에는 현재 해결할 수 없는 주기가 발생합니다. 예를 들면 다음과 같습니다.

```java
package P;

import static P.Outer.Nested.*;

public class Outer {
    public static class Nested<T extends I> {
        static class I { }
    }
}
```

이 문제에 대한 해결책은 `javac`의 멤버 확인의 기존 첫 번째 단계를 세 가지로 나누는 것입니다. 첫 번째 단계는 포함하는 파일의 가져오기를 분석하고 두 번째 단계는 유형 매개변수, 주석 등 없이 클래스/인터페이스 계층만 빌드합니다. 세 번째는 유형 매개변수를 포함하여 클래스 헤더를 적절하게 분석합니다.

이 변경을 통해 `javac`는 현재 거부된 프로그램을 수락할 수 있지만 현재 수락된 프로그램은 거부하지 않을 것으로 예상됩니다.

### JEP 217: Annotations Pipeline 2.0

주석을 처리하는 도구 및 주석의 요구 사항을 더 잘 처리할 수 있도록 `javac` 주석 파이프라인을 다시 설계하십시오.

#### Goals

* 컴파일러는 주석 및 유형 주석과 관련하여 올바르게 작동해야 합니다. 방출된 클래스 파일에는 모든 종류의 주석에 대해 올바른 형식의 속성이 있어야 합니다.
* 컴파일 타임 리플렉션(`javax.lang.model` 및 `javax.annotation.processing`)은 서명이 보이는 위치에 있는 모든 주석을 적절하게 처리해야 합니다.
* 런타임 리플렉션(Core Reflection)은 클래스 파일의 주석과 함께 제대로 작동해야 합니다.
* Checkers Framework는 계속 작동해야 합니다.
* Java Compiler API는 설계된 대로 계속 작동해야 합니다.

#### Description

`javac` 주석 파이프라인을 리팩토링하십시오. 이것은 버그를 수정하고 정확성을 개선하는 경우를 제외하고는 외부적으로 눈에 띄지 않아야 합니다. 첫 번째 단계는 종료 기준을 측정하고 평가할 수 있도록 테스트 범위를 개선하는 것입니다. 그 후 일련의 증분 리팩토링이 뒤따릅니다. 이 작업은 OpenJDK Annotations Pipeline 2.0 프로젝트에서 수행됩니다.

### JEP 219: Datagram Transport Layer Security (DTLS)

DTLS(Datagram Transport Layer Security) 버전 1.0(RFC 4347) 및 1.2(RFC 6347)용 API를 정의합니다.

### JEP 220: Modular Run-Time Images

JDK 및 JRE 런타임 이미지를 재구성하여 모듈을 수용하고 성능, 보안 및 유지 관리 가능성을 개선합니다. 이미지의 내부 구조나 형식을 드러내지 않고 런타임 이미지에 저장된 모듈, 클래스 및 리소스의 이름을 지정하기 위한 새로운 URI 체계를 정의합니다. 이러한 변경 사항을 수용하기 위해 필요에 따라 기존 사양을 수정합니다.

#### Goals

* 다음과 같은 저장 클래스 및 리소스 파일에 대한 런타임 형식을 채택합니다.
  * 옛날 ZIP 형식을 기반으로 하는 레거시 JAR 형식보다 시간 및 공간 효율성이 높습니다.
  * 모듈별로 클래스 및 리소스 파일을 찾고 로드할 수 있습니다.
  * JDK 모듈과 라이브러리 및 애플리케이션 모듈의 클래스 및 리소스 파일을 저장할 수 있습니다. 그리고
  * 미리 계산된 JVM 데이터 구조 및 Java 클래스용으로 미리 컴파일된 네이티브 코드와 같은 추가 데이터 종류를 수용하도록 확장할 수 있습니다.
* JDK 및 JRE 런타임 이미지를 재구성하여 개발자, 배포자 및 최종 사용자가 의존할 수 있는 파일과 적절한 경우 수정할 수 있는 파일을 명확히 구분합니다.
* 예를 들어, 오늘날 런타임 이미지의 내부 구조를 검사해야 하는 이미지에 있는 모든 클래스를 열거하는 것과 같은 일반적인 작업을 수행하는 지원되는 방법을 제공합니다.
* 현재 모든 보안 권한이 부여되지만 실제로 이러한 권한이 필요하지 않은 JDK 클래스의 선택적 권한 해제를 활성화합니다.
* 잘 작동하는 애플리케이션, 즉 JRE 및 JDK 런타임 이미지의 내부 측면에 의존하지 않는 애플리케이션의 기존 동작을 유지합니다.

### JEP 221: Simplified Doclet API

적절한 Java SE 및 JDK API를 활용하도록 Doclet API를 대체하고 새 API를 사용하도록 표준 doclet을 업데이트합니다.

#### Goals

오래된 API의 유지 관리 부담을 줄입니다.

* Java SE 6에 도입된 표준 언어 모델 API인 `javax.lang.model`을 위해 사용자 지정 언어 모델 API 사용을 제거합니다.
* JDK 8에 도입된 컴파일러 트리 API `com.sun.source.doctree`를 위해 문서 주석 분석에 대한 단순한 지원을 제거합니다.
* "template class" `com.sun.javadoc.Doclet`의 사용을 적절한 새 인터페이스 유형으로 교체합니다.

### JEP 222: jshell: The Java Shell (Read-Eval-Print Loop)

다른 애플리케이션이 이 기능을 활용할 수 있도록 API와 함께 Java 프로그래밍 언어의 선언, 명령문 및 표현식을 평가하는 대화형 도구를 제공합니다.

#### Goals

JShell API 및 도구는 JShell 상태 내에서 Java 프로그래밍 언어의 선언, 명령문 및 표현을 대화식으로 평가하는 방법을 제공합니다. JShell 상태에는 진화하는 코드와 실행 상태가 포함됩니다. 신속한 조사 및 코딩을 용이하게 하기 위해 명령문 및 표현식이 메소드 내에서 발생할 필요가 없으며 변수 및 메소드가 클래스 내에서 발생할 필요가 없습니다.

`jshell` 도구는 편집 기록, 탭 완성, 필요한 터미널 세미콜론 자동 추가, 구성 가능한 미리 정의된 가져오기 및 정의를 포함하여 상호 작용을 용이하게 하는 기능을 갖춘 커맨드라인 도구가 될 것입니다.

### JEP 223: New Version-String Scheme

메이저, 마이너, 보안 업데이트 릴리스를 쉽게 구분할 수 있는 버전 문자열 체계를 정의하고 JDK에 적용합니다.

#### Goals

사람이 쉽게 이해할 수 있고 프로그램으로 쉽게 구문 분석할 수 있습니다.

현재 업계 관행, 특히 시맨틱 버전 관리에 맞춰 조정합니다.

RPM, dpkg, IPS 및 JNLP(Java Network Launching Protocol)를 비롯한 기존 패키징 시스템 및 플랫폼 배포 메커니즘에서 채택할 수 있습니다.

버전 문자열의 한 요소(즉, 부 릴리스 번호와 보안 수준)에 두 가지 유형의 정보를 인코딩하는 현재 관행을 제거합니다. 이는 해독하기 어렵고 많은 버전 번호를 건너뛰는 결과를 초래합니다.

버전 문자열 구문 분석, 유효성 검사 및 비교를 위한 간단한 API를 제공합니다.

### JEP 224: HTML5 Javadoc

HTML5 마크업을 생성하도록 `javadoc` 도구를 향상시킵니다.

#### Goals

HTML 4 또는 HTML5 출력을 요청하는 옵션을 표준 `doclet`에 제공하십시오. HTML5 마크업은 의미론적입니다. 즉, 의미와 스타일 및 콘텐츠를 명확하게 구분합니다. HTML5 마크업을 사용하여 표준 `doclet`에 의해 생성된 페이지의 일부는 접근성 요구 사항을 충족합니다.

#### Description

* 특정 유형의 출력 마크업을 요청하기 위해 명령줄 옵션이 표준 `doclet`에 추가되었습니다. 현재 유형인 HTML4가 기본값이 됩니다. HTML5는 JDK 10에서 기본값이 됩니다.
* `header`, `footer`, `nav` 등의 구조적 HTML5 요소를 사용하여 생성된 HTML의 의미 값을 향상시킵니다.
* HTML5 마크업은 접근성을 위한 WAI-ARIA 표준을 구현합니다. 특정 역할은 역할 속성을 사용하여 HTML 문서의 요소에 할당됩니다.
* `-Xdoclint` 기능은 요청된 유형의 출력 마크업을 기반으로 일반적인 오류에 대한 문서 주석을 확인하도록 업데이트되었습니다.

### JEP 225: Javadoc Search

문서 내에서 프로그램 요소와 태그가 지정된 단어 및 구문을 검색하는 데 사용할 수 있는 표준 `doclet`에서 생성된 API 문서에 검색 상자를 추가하십시오. 검색 상자는 표준 `doclet`에 의해 생성된 모든 페이지의 헤더에 나타납니다.

#### Goals

검색 기능은 로컬로 구현되며 서버 측 계산 리소스에 의존하지 않습니다.

### JEP 226: UTF-8 Property Files

애플리케이션이 UTF-8로 인코딩된 속성 파일을 지정하는 수단을 정의하고 이를 로드하도록 ResourceBundle API를 확장합니다.

### JEP 227: Unicode 7.0

유니코드 표준 버전 7.0을 지원하도록 기존 플랫폼 API를 업그레이드하십시오.

#### Goals

주로 다음 클래스에서 최신 버전의 유니코드를 지원합니다.

* `java.lang` 패키지의 문자 및 문자열, 그리고
* `java.text` 패키지의 `Bidi`, `BreakIterator` 및 `Normalizer`.

### JEP 228: Add More Diagnostic Commands

Hotspot 및 JDK의 진단 가능성을 향상시키기 위해 추가 진단 명령을 정의합니다.

#### Description

* `print_class_summary`
  * 로드된 모든 클래스와 해당 상속 구조의 목록을 인쇄합니다.
  * 담당 그룹: 런타임
* `print_codegenlist`
  * C1 또는 C2(별도의 대기열)를 사용하여 컴파일을 위해 대기 중인 인쇄 메서드
  * 담당 그룹: 컴파일러
* `print_utf8pool`
  * 모든 UTF-8 문자열 상수를 인쇄합니다.
  * 담당 그룹: 런타임
* `datadump_request`
  * JVMTI에 대한 데이터 덤프 요청을 수행하도록 JVM에 신호를 보냅니다.
  * 책임 그룹: 서비스 가능성
* `dump_codelist`
  * 전체 서명, 주소 범위 및 상태(활성, 비진입 및 좀비)와 함께 n-메서드(컴파일됨)를 인쇄합니다.
  * `stdout` 또는 파일로의 인쇄 선택을 허용합니다.
  * XML 또는 텍스트 출력을 허용합니다.
  * 담당 그룹: 컴파일러
* `print_codeblocks`
  * 코드 캐시의 크기와 코드 캐시의 블록 목록을 주소와 함께 인쇄합니다.
  * 담당 그룹: 컴파일러
* `set_vmflag`
  * VM 또는 라이브러리에서 명령줄 플래그/옵션을 설정합니다.
  * 책임 그룹: 서비스 가능성

### JEP 229: Create PKCS12 Keystores by Default

기본 키 저장소 유형을 JKS에서 PKCS12로 전환합니다.

#### Goals

보안을 향상시킵니다. PKCS12는 JKS보다 강력한 암호화 알고리즘을 제공합니다.

순방향 및 역방향 호환성을 유지합니다. JKS 및 PKCS12 키 저장소에 액세스하는 애플리케이션은 JDK 릴리스에서 계속 작동해야 합니다.

### JEP 231: Remove Launch-Time JRE Version Selection

JRE 실행 시 실행 중인 JRE가 아닌 JRE 버전을 요청할 수 있는 기능을 제거합니다.

### JEP 232: Improve Secure Application Performance

보안 관리자가 설치된 상태에서 실행되는 애플리케이션의 성능을 향상시킵니다.

#### Goals 

성능 문제를 더 잘 이해하고 성능 향상을 위해 입증된 개선 사항을 구현합니다. 각 잠재적 개선 사항을 평가하고 추적하기 위해 하위 작업이 생성됩니다.

### JEP 233: Generate Run-Time Compiler Tests Automatically

테스트 케이스를 자동으로 생성하여 런타임 컴파일러를 테스트하는 도구를 개발합니다.

#### Goals

* 생성된 테스트는 `jtreg`와 호환되어야 합니다.
* 도구는 최종 결과의 언어(Java 소스 코드, Java 바이트 코드), 언어 구성의 사용, 제어 흐름 및 표현식 복잡성 등의 측면에서 구성 가능해야 합니다.
* 테스트는 무작위이지만 재현 가능하게 생성되어야 합니다.

### JEP 235: Test Class-File Attributes Generated by javac

`javac`에 의해 생성된 클래스 파일 속성의 정확성을 검증하는 테스트를 작성하십시오.

#### Goals

이러한 속성이 일반 컴파일 및 실행 시나리오에서 사용되지 않는 경우에도 모든 클래스 파일 속성이 올바르게 생성되었는지 확인하는 테스트를 만듭니다. 또한 기존의 그러한 테스트를 문서화하십시오.

#### Description

`javac`에 의해 생성된 파일을 테스트하는 일반적인 방법은 컴파일된 클래스를 실행하고 생성된 프로그램이 예상대로 작동하는지 확인하는 것입니다. 이 접근 방식은 선택적 클래스 파일 속성이나 VM에서 확인되지 않은 속성에 대해서는 작동하지 않으므로 이러한 두 종류의 속성은 다른 방법으로 테스트해야 합니다. Java 소스 코드를 입력으로 받아들이고, 소스를 컴파일하고, 컴파일된 클래스 파일의 클래스 파일 속성을 읽고, 정확성을 검증하는 테스트가 개발될 것입니다.

클래스 파일 속성은 JVMS에 따라 세 그룹으로 나뉩니다.

S* ourceFile
* SourceDebugExtension
* LineNumberTable
* LocalVariableTable
* LocalVariableTypeTable
* Deprecated

##### Optional attributes

이러한 속성은 javac, JVM 또는 클래스 라이브러리의 올바른 작동에 중요하지 않지만 도구에서 사용됩니다. 이러한 속성을 테스트하는 것은 JDK의 구성 요소에서 사용되지 않기 때문에 높은 우선 순위입니다.

##### Attributes not used by the JVM

이러한 속성은 JVM에서 사용되지 않지만 javac 또는 클래스 라이브러리에서 사용됩니다. 이러한 속성을 테스트하는 것은 중간 우선 순위입니다.

* InnerClasses
* EnclosingMethod
* Synthetic
* Signature
* RuntimeVisibleAnnotations
* RuntimeInvisibleAnnotations
* RuntimeVisibleParameterAnnotations
* RuntimeInvisibleParameterAnnotations
* RuntimeVisibleTypeAnnotations
* RuntimeInvisibleTypeAnnotations
* AnnotationDefault
* MethodParameters

##### Attributes are used by the JVM

이러한 속성은 JVM의 바이트 코드 검증기에 의해 확인됩니다. 더 이상의 테스트가 필요하지 않습니다.

* ConstantValue
* Code
* StackMapTable
* Exceptions
* BootstrapMethods

### JEP 236: Parser API for Nashorn

Nashorn의 ECMAScript 추상 구문 트리에 대해 지원되는 API를 정의합니다.

새로운 `jdk.nashorn.api.tree` 패키지의 제안된 인터페이스 및 클래스에 대한 문서가 포함되어 있습니다.

#### Goals

* Nashorn 구문 트리 노드를 나타내는 인터페이스 클래스를 제공합니다.
* API를 통해 Nashorn 명령줄 옵션을 전달하여 구성을 수행하여 구성된 파서 인스턴스를 생성하기 위한 팩토리를 제공합니다.
* AST 노드를 방문하기 위한 방문자 패턴 API를 제공합니다.
* API를 사용하기 위한 샘플/테스트 프로그램을 제공합니다.

### JEP 237: Linux/AArch64 Port

JDK 9를 Linux/AArch64로 포트합니다.

### JEP 238: Multi-Release JAR Files

JAR 파일 형식을 확장하여 여러 Java 릴리스별 클래스 파일 버전이 단일 아카이브에 공존할 수 있도록 합니다.

#### Goals

* 다중 릴리스 JAR 파일을 작성할 수 있도록 Java 아카이브 도구(jar)를 개선하십시오.
* 표준 클래스 로더 및 JarFile API 지원을 포함하여 JRE에서 다중 릴리스 JAR 파일을 구현합니다.
* 다중 릴리스 JAR 파일을 해석하기 위해 기타 중요한 도구(예: `javac`, `javap`, `jdeps` 등)를 향상합니다.
* 목표 1에서 3까지 다중 릴리스 모듈식 JAR 파일을 지원합니다.
* 성능 유지: 다중 릴리스 JAR 파일을 사용하는 도구 및 구성 요소의 성능은 크게 영향을 받지 않아야 합니다. 특히, 일반(즉, 다중 릴리스가 아닌) JAR 파일에 액세스할 때 성능이 저하되어서는 안 됩니다.

### JEP 240: Remove the JVM TI hprof Agent

JDK에서 `hprof` 에이전트를 제거합니다.

### JEP 241: Remove the jhat Tool

구식 `jhat` 도구를 제거하십시오.

### JEP 243: Java-Level JVM Compiler Interface

Java로 작성된 컴파일러를 JVM에서 동적 컴파일러로 사용할 수 있도록 하는 Java 기반 JVM 컴파일러 인터페이스(JVMCI)를 개발합니다.

#### Goals

* JVMCI에 대해 프로그래밍된 Java 구성 요소가 런타임에 로드되고 JVM의 컴파일 브로커에서 사용되도록 허용합니다.
* JVMCI에 대해 프로그래밍된 Java 구성 요소가 런타임에 로드되고 설치된 코드에 대한 Java 참조를 통해 호출될 수 있는 기계 코드를 JVM에 설치하기 위해 신뢰할 수 있는 Java 코드에 의해 사용되도록 허용합니다.

#### Description

JVMCI API는 다음을 위한 메커니즘으로 구성됩니다.

* 클래스, 필드, 메소드, 프로파일링 정보 등과 같은 바이트코드를 머신 코드로 최적화하는 컴파일러에 필요한 VM 데이터 구조에 액세스
* GC 맵 및 최적화 해제를 지원하는 정보와 같은 컴파일된 코드를 관리하기 위해 JVM에 필요한 모든 메타데이터와 함께 컴파일된 코드를 설치합니다.
* 메소드에 대한 기계어 코드를 생성하기 위해 JVM 요청 서비스를 처리하기 위해 JVM의 컴파일 시스템에 연결합니다.

JVMCI를 사용하여 JVM에서 고성능 컴파일러를 작성하고 배포하는 훌륭한 데모는 광범위한 벤치마크에서 C2와 동등한 최고 성능을 입증한 Graal에서 제공합니다.

### JEP 244: TLS Application-Layer Protocol Negotiation Extension

`javax.net.ssl` 패키지를 확장하여 TLS 연결을 위한 애플리케이션 프로토콜을 협상하는 수단을 제공하는 TLS ALPN(Application Layer Protocol Negotiation) 확장을 지원합니다.

### JEP 245: Validate JVM Command-Line Flag Arguments

충돌을 방지하기 위해 모든 JVM 명령줄 플래그에 대한 인수의 유효성을 검사하고 유효하지 않은 경우 적절한 오류 메시지가 표시되는지 확인합니다.

### JEP 246: Leverage CPU Instructions for GHASH and RSA

최근에 도입된 SPARC 및 Intel x64 CPU 명령어를 활용하여 GAS 및 RSA 암호화 작업의 성능을 개선합니다.

### JEP 247: Compile for Older Platform Versions

Java 프로그램을 컴파일하여 선택한 이전 버전의 플랫폼에서 실행할 수 있도록 `javac`를 향상시킵니다.

### JEP 248: Make G1 the Default Garbage Collector

32비트 및 64비트 서버 구성에서 G1을 기본 가비지 수집기로 설정합니다.

### JEP 249: OCSP Stapling for TLS

TLS 인증서 상태 요청 확장(RFC 6066의 섹션 8) 및 다중 인증서 상태 요청 확장(RFC 6961)을 통해 OCSP 스테이플링을 구현합니다.

#### Description

이 기능은 SunJSSE 공급자 구현에서 구현됩니다. 이러한 변경을 가능한 한 작게 유지하는 것을 목표로 사소한 API 변경이 계획되어 있습니다. 구현은 OCSP 특정 매개변수에 대해 합리적인 기본값을 선택하고 다음 시스템 속성을 통해 이러한 기본값의 구성을 제공합니다.

* `jdk.tls.client.enableStatusRequestExtension`: 이 속성은 기본적으로 `true`입니다. 이것은 `status_request` 및 `status_request_v2` 확장을 활성화하고 서버에서 보낸 `CertificateStatus` 메시지 처리를 활성화합니다.
* `jdk.tls.server.enableStatusRequestExtension`: 이 속성은 기본적으로 `false`입니다. 이렇게 하면 OCSP 스테이플링에 대한 서버 측 지원이 가능합니다.
* `jdk.tls.stapling.responseTimeout`: 이 속성은 캐시에서 또는 OCSP 응답자에 연결하여 서버가 OCSP 응답을 얻는 데 사용할 최대 시간을 제어합니다. 수신된 응답은 수행 중인 스테이플링 유형에 따라 해당되는 경우 `CertificateStatus` 메시지로 전송됩니다. 이 속성은 밀리초 단위의 정수 값을 사용하며 기본값은 5000입니다.
* `jdk.tls.stapling.cacheSize`: 이 속성은 항목의 최대 캐시 크기를 제어합니다. 기본값은 256개 개체입니다. 캐시가 가득 차서 새 응답을 캐시해야 하는 경우 가장 적게 사용된 캐시 항목이 새 항목으로 교체됩니다. 이 속성의 값이 0 이하이면 캐시에 포함될 수 있는 응답 수에 대한 상한이 없습니다.
* `jdk.tls.stapling.cacheLifetime`: 이 속성은 캐시된 응답의 최대 수명을 제어합니다. 값은 초 단위로 지정되며 기본값은 3600(1시간)입니다. 응답에 캐시 수명보다 빨리 만료되는 nextUpdate 필드가 있는 경우 응답의 수명이 이 속성으로 설정된 값보다 짧을 수 있습니다. 이 속성의 값이 0 이하이면 캐시 수명이 비활성화됩니다. 객체에 nextUpdate가 없고 캐시 수명이 비활성화된 경우 응답이 캐시되지 않습니다.
* `jdk.tls.stapling.responderURI`: 이 속성을 사용하면 TLS에 사용되는 인증서에 기관 정보 액세스 확장이 없는 경우 관리자가 기본 URI를 설정할 수 있습니다. `jdk.tls.stapling.responderOverride` 속성이 설정되어 있지 않으면 AIA 확장 값을 재정의하지 않습니다(아래 참조). 이 속성은 기본적으로 설정되어 있지 않습니다.
* `jdk.tls.stapling.responderOverride`: 이 속성을 사용하면 `jdk.tls.stapling.responderURI` 속성을 통해 제공된 URI가 AIA 확장 값을 재정의할 수 있습니다. 기본적으로 `false`입니다.
* `jdk.tls.stapling.ignoreExtensions`: 이 속성은 status_request 또는 `status_request_v2` TLS 확장에 지정된 OCSP 확장의 전달을 비활성화합니다. 기본적으로 `false`입니다.

클라이언트 및 서버 측 Java 구현은 `status_request` 및 `status_request_v2` TLS Hello 확장을 지원할 수 있습니다. `status_request` 확장은 RFC 6066에 설명되어 있습니다. 지원 서버에는 새 TLS 핸드셰이크 메시지(CertificateStatus)에서 서버를 식별하는 데 사용되는 인증서에 대한 단일 OCSP 응답이 포함됩니다. `status_request_v2` 확장은 RFC 6961에 설명되어 있습니다. 확장을 통해 클라이언트는 서버가 CertificateStatus 메시지에 단일 OCSP 응답을 제공하도록 요청하거나(`status_request`와 유사) 서버가 인증서 목록의 각 인증서에 대한 OCSP 응답을 가져오도록 요청할 수 있습니다. 인증서 메시지에서 제공됩니다(아래에서 `ocsp_multi` 유형으로 참조됨).

### JEP 250: Store Interned Strings in CDS Archives

인턴된 문자열을 클래스 데이터 공유(CDS) 아카이브에 저장합니다.

#### Goals

* 다른 JVM 프로세스 간에 `String` 객체와 기본 `char` 배열 객체를 공유하여 메모리 소비를 줄입니다
* G1 GC에 대한 공유 문자열만 지원합니다. 공유 문자열에는 고정 영역이 필요하며 G1은 고정을 지원하는 유일한 HotSpot GC입니다.
* 압축된 개체 및 클래스 포인터가 있는 64비트 플랫폼만 지원합니다.
* 일반적인 벤치마크를 사용하여 시작 시간, 문자열 조회 시간, GC 일시 중지 시간 또는 런타임 성능에 심각한 저하(< 2-3%)가 없습니다.

### JEP 251: Multi-Resolution Images

해상도 변형이 있는 이미지를 쉽게 조작하고 표시할 수 있도록 다중 해상도 이미지 API를 정의합니다.

#### Description

`java.awt.image` 패키지에 정의될 새 API는 해상도가 다른 이미지 세트를 단일 다중 해상도 이미지로 캡슐화할 수 있도록 합니다.

다중 해상도 이미지에 대한 기본 작업은 다음과 같습니다.

주어진 DPI 메트릭 및 이미지 변환 세트를 기반으로 해상도별 이미지 변형을 검색하고,

이미지의 모든 변형을 검색합니다.

이러한 작업을 제외하고 다중 해상도 이미지는 일반 이미지와 같은 방식으로 작동합니다. `java.awt.Graphics` 클래스는 현재 디스플레이 DPI 메트릭 및 적용된 변환을 기반으로 다중 해상도 이미지에서 필요한 변형을 검색합니다.

제안된 API 스케치

```java
package java.awt.image;

/**
 * This interface is designed to provide a set of images at various resolutions.
 *
 * The {@code MultiResolutionImage} interface should be implemented by any
 * class whose instances are intended to provide image resolution variants
 * according to the given image width and height.
 *
 * @since 1.9
 */
public interface MultiResolutionImage {

    /**
     * Gets a specific image that is the best variant to represent
     * this logical image at the indicated size.
     *
     * @param destImageWidth the width of the destination image, in pixels.
     * @param destImageHeight the height of the destination image, in pixels.
     * @return image resolution variant.
     *
     * @since 1.9
     */
    Image getResolutionVariant(float destImageWidth, float destImageHeight);

    /**
     * Gets a readable list of all resolution variants.
     * Note that many implementations might return an unmodifiable list.
     *
     * @return list of resolution variants.
     * @since 1.9
     */
    public List<Image> getResolutionVariants();
}
```

### JEP 252: Use CLDR Locale Data by Default

기본적으로 유니코드 컨소시엄의 CLDR(Common Locale Data Repository)에 있는 로케일 데이터를 사용합니다.

### JEP 253: Prepare JavaFX UI Controls & CSS APIs for Modularization

현재 내부 API를 통해서만 사용할 수 있으므로 모듈화로 인해 액세스할 수 없게 되는 JavaFX UI 컨트롤 및 CSS 기능에 대한 공개 API를 정의합니다.

#### Description

JavaFX의 UI 컨트롤 및 CSS 기능을 사용하는 많은 개발자는 역사적으로 내부 `com.sun.*` API를 피하기 위해 경고를 무시했습니다. 대부분의 경우 원하는 결과를 얻기 위해 개발자는 이러한 내부 API를 사용할 수 밖에 없습니다. 다가오는 Java 9 릴리스와 특히 Project Jigsaw의 모듈 사이에 강력한 경계가 도입됨에 따라 개발자는 `com.sun.*` 패키지에 더 이상 액세스할 수 없기 때문에 코드가 더 이상 컴파일되거나 실행되지 않는다는 것을 알게 될 것입니다. 이 JEP의 목표는 현재 내부 API에서 제공하는 기능에 대한 공개 API를 정의하는 것입니다.

##### Project One: Make UI control skins into public APIs

현재 모든 스킨은 `com.sun.javafx.scene.control.skin`에 있습니다. 이것은 추가 기능을 추가하거나, 기존 메서드를 재정의하거나, 컨트롤 스킨의 비주얼이나 동작을 수정하기 위해 스킨(예: TextFieldSkin)을 확장한 제3자가 JDK 9에서 작동하는 애플리케이션 없이 남게 된다는 것을 의미합니다. 물론 이것은 비공개 API에 의존하는 사용자의 잘못이지만, 우리는 UI 컨트롤의 제3자 수정을 더 잘 가능하게 하기 위해 이 API를 공개적으로 만드는 것에 대해 오랫동안 논의했습니다.

6월 중순 현재 이 프로젝트는 거의 모든 코드가 이동되고 정리되는 시점에 있습니다. 의도는 7월 중순에서 8월 초 사이에 JDK 9 빌드에서 이를 공개하는 것입니다. 다음은 공개 API로 `javafx.scene.control.skin`으로 이동한 모든 클래스 목록입니다.

* AccordionSkin
* ButtonBarSkin
* ButtonSkin
* CellSkinBase
* CheckBoxSkin
* ChoiceBoxSkin
* ColorPickerSkin
* ComboBoxBaseSkin
* ComboBoxListViewSkin
* ComboBoxPopupControl
* ContextMenuSkin
* DateCellSkin
* DatePickerSkin
* HyperlinkSkin
* LabelSkin
* LabeledSkinBase
* ListCellSkin
* ListViewSkin
* MenuBarSkin
* MenuButtonSkin
* MenuButtonSkinBase
* NestedTableColumnHeader
* PaginationSkin
* ProgressBarSkin
* ProgressIndicatorSkin
* RadioButtonSkin
* ScrollBarSkin
* ScrollPaneSkin
* SeparatorSkin
* SliderSkin
* SpinnerSkin
* SplitMenuButtonSkin
* SplitPaneSkin
* TabPaneSkin
* TableCellSkin
* TableCellSkinBase
* TableColumnHeader
* TableHeaderRow
* TableRowSkin
* TableRowSkinBase
* TableViewSkin
* TableViewSkinBase
* TextAreaSkin
* TextFieldSkin
* TextInputControlSkin
* TitledPaneSkin
* ToggleButtonSkin
* ToolBarSkin
* TooltipSkin
* TreeCellSkin
* TreeTableCellSkin
* TreeTableRowSkin
* TreeTableViewSkin
* TreeViewSkin
* VirtualContainerBase
* VirtualFlow

##### Project Two: Review and make public relevant CSS APIs

Project One과 마찬가지로 이 프로젝트는 현재 `com.sun.*` 패키지에 있는 공개 API로 가져오는 것과 관련이 있습니다. 다음은 공개 API로 `javafx.css`로 이동한 모든 클래스의 목록입니다.

```java
CascadingStyle.java:public class CascadingStyle implements Comparable<CascadingStyle> {
CascadingStyle.java:    public Style getStyle() {
CascadingStyle.java:    public CascadingStyle(final Style style, Set<PseudoClass> pseudoClasses,
CascadingStyle.java:    public String getProperty() {
CascadingStyle.java:    public Selector getSelector() {
CascadingStyle.java:    public Rule getRule() {
CascadingStyle.java:    public StyleOrigin getOrigin() {
CascadingStyle.java:    public ParsedValueImpl getParsedValueImpl() {

CompoundSelector.java:final public class CompoundSelector extends Selector {
CompoundSelector.java:    public List<SimpleSelector> getSelectors() {
CompoundSelector.java:    public CompoundSelector(List<SimpleSelector> selectors, List<Combinator> relationships)
CompoundSelector.java:    public Match createMatch() {

CssError.java:public class CssError {
CssError.java:    public static void setCurrentScene(Scene scene) {
CssError.java:    public final String getMessage() {
CssError.java:    public CssError(String message) {
CssError.java:    public final static class PropertySetError extends CssError {
CssError.java:        public PropertySetError(CssMetaData styleableProperty,

Declaration.java:final public class Declaration {
Declaration.java:    public ParsedValue getParsedValue() {
Declaration.java:    public String getProperty() {
Declaration.java:    public Rule getRule() {

Rule.java:final public class Rule {
Rule.java:    public final ObservableList<Declaration> getDeclarations() {
Rule.java:    public final ObservableList<Selector> getSelectors() {
Rule.java:    public Stylesheet getStylesheet() {
Rule.java:    public StyleOrigin getOrigin() {

Selector.java:abstract public class Selector {
Selector.java:    public Rule getRule() {
Selector.java:    public void setOrdinal(int ordinal) {
Selector.java:    public int getOrdinal() {
Selector.java:    public abstract Match createMatch();
Selector.java:    public abstract boolean applies(Styleable styleable);
Selector.java:    public abstract boolean applies(Styleable styleable, Set<PseudoClass>[] triggerStates, int bit);
Selector.java:    public abstract boolean stateMatches(Styleable styleable, Set<PseudoClass> state);
Selector.java:    public static Selector createSelector(final String cssSelector) {
Selector.java:    protected void writeBinary(DataOutputStream os, StringStore stringStore)

SimpleSelector.java:final public class SimpleSelector extends Selector {
SimpleSelector.java:    public String getName() {
SimpleSelector.java:    public List<String> getStyleClasses() {
SimpleSelector.java:    public Set<StyleClass> getStyleClassSet() {
SimpleSelector.java:    public String getId() {
SimpleSelector.java:    public NodeOrientation getNodeOrientation() {

Size.java:final public class Size {
Size.java:    public Size(double value, SizeUnits units) {
Size.java:    public double getValue() {
Size.java:    public SizeUnits getUnits() {
Size.java:    public boolean isAbsolute() {
Size.java:    public double pixels(double multiplier, Font font) {
Size.java:    public double pixels(Font font) {
Size.java:    public double pixels() {

Style.java:final public class Style {
Style.java:    public Selector getSelector() {
Style.java:    public Declaration getDeclaration() {
Style.java:    public Style(Selector selector, Declaration declaration) {

Stylesheet.java:public class Stylesheet {
Stylesheet.java:    public String getUrl() {
Stylesheet.java:    public StyleOrigin getOrigin() {
Stylesheet.java:    public void setOrigin(StyleOrigin origin) {
Stylesheet.java:    public List<Rule> getRules() {
Stylesheet.java:    public List<FontFace> getFontFaces() {
Stylesheet.java:    public static Stylesheet loadBinary(URL url) throws IOException {
Stylesheet.java:    public static void convertToBinary(File source, File destination) throws IOException {

CssParser.java:final public class CssParser {
CssParser.java:    public CssParser() {
CssParser.java:    public Stylesheet parse(final String stylesheetText) {
CssParser.java:    public Stylesheet parse(final URL url) throws IOException {
CssParser.java:    public Stylesheet parseInlineStyle(final Styleable node) {
CssParser.java:    public ParsedValueImpl parseExpr(String property, String expr) {
CssParser.java:    public static ObservableList<CssError> errorsProperty() {
```

### JEP 254: Compact Strings

문자열에 대해 보다 공간 효율적인 내부 표현을 채택하십시오.

#### Goals

대부분의 시나리오에서 성능을 유지하고 모든 관련 Java 및 기본 인터페이스에 대한 완전한 호환성을 유지하면서 `String` 클래스 및 관련 클래스의 공간 효율성을 개선합니다.

#### Description

`String` 클래스의 내부 표현을 `UTF-16 char` 배열에서 바이트 배열과 인코딩 플래그 필드로 변경할 것을 제안합니다. 새로운 `String` 클래스는 문자열의 내용을 기반으로 ISO-8859-1/Latin-1(문자당 1바이트) 또는 UTF-16(문자당 2바이트)으로 인코딩된 문자를 저장합니다. 인코딩 플래그는 사용되는 인코딩을 나타냅니다.

`AbstractStringBuilder`, `StringBuilder` 및 `StringBuffer`와 같은 문자열 관련 클래스는 HotSpot VM의 고유 문자열 작업과 마찬가지로 동일한 표현을 사용하도록 업데이트됩니다.

이것은 기존 공용 인터페이스에 대한 변경 없이 순전히 구현 변경 사항입니다. 새로운 공개 API 또는 기타 인터페이스를 추가할 계획은 없습니다.

현재까지 수행된 프로토타이핑 작업은 메모리 공간의 예상 감소, GC 활동의 상당한 감소, 일부 코너 경우에 약간의 성능 회귀를 확인합니다.

자세한 내용은 다음을 참조하십시오.

* [State of String Density Performance](https://cr.openjdk.java.net/~shade/density/state-of-string-density-v1.txt)
* [String Density Impact on SPECjbb2005 on SPARC](https://cr.openjdk.java.net/~huntch/string-density/reports/String-Density-SPARC-jbb2005-Report.pdf)

### JEP 255: Merge Selected Xerces 2.11.0 Updates into JAXP

JDK에 포함된 Xerces XML 파서의 버전을 Xerces 2.11.0의 중요한 변경 사항으로 업그레이드하십시오.

#### Description

Xerces 2.11.0에서 다음 범주의 변경 사항으로 JDK를 업데이트합니다.

* Datatypes
* DOM L3 Serializer
* XPointer
* Catalog Resolver
* XML Schema Validation (including bug fixes, but not the XML Schema 1.1 development code)

JAXP 공개 API에는 변경 사항이 없습니다.

이 업데이트는 일괄 처리됩니다. 모든 개정판을 개별적으로 테스트할 수 있는 것은 아닙니다.

### JEP 256: BeanInfo Annotations

`@beaninfo` Javadoc 태그를 적절한 주석으로 교체하고 런타임에 주석을 처리하여 `BeanInfo` 클래스를 동적으로 생성합니다.

#### Description

대부분의 `BeanInfo` 클래스는 런타임에 자동으로 생성되지만 많은 `Swing` 클래스는 여전히 컴파일 타임에 `@beaninfo` Javadoc 태그에서 `BeanInfo` 클래스를 생성합니다. `@beaninfo` 태그를 다음 주석으로 교체하고 기존 내부 검사 알고리즘을 확장하여 이를 해석할 것을 제안합니다. 

```java
package java.beans;
public @interface JavaBean {
    String description() default "";
    String defaultProperty() default "";
    String defaultEventSet() default "";
}

package java.beans;
public @interface BeanProperty {
    boolean bound() default true;
    boolean expert() default false;
    boolean hidden() default false;
    boolean preferred() default false;
    boolean visualUpdate() default false;
    String description() default "";
    String[] enumerationValues() default {};
}

package javax.swing;
public @interface SwingContainer {
    boolean value() default true;
    String delegate() default "";
}
```

자세한 내용은 `JavaBean`, `BeanProperty` 및 `SwingContainer에` 대한 Javadoc을 참조하십시오.

이러한 주석은 런타임 시 `BeanInfo` 생성 중에 해당 기능 속성을 설정합니다. 개발자가 모든 Bean 클래스에 대해 별도의 `BeanInfo` 클래스를 생성하는 것보다 Bean 클래스에서 직접 이러한 속성을 지정하는 것이 더 쉬울 것입니다. 또한 자동으로 생성된 클래스를 제거할 수 있으므로 클라이언트 라이브러리를 모듈화하기가 더 쉽습니다.

### JEP 257: Update JavaFX/Media to Newer Version of GStreamer

보안, 안정성, 성능 향상을 위해 FX/Media에 포함된 GStreamer 버전을 업데이트 합니다.

### JEP 258: HarfBuzz Font-Layout Engine

기존 ICU OpenType 글꼴 레이아웃 엔진을 HarfBuzz로 교체합니다.

### JEP 259: Stack-Walking API

스택 추적의 정보를 쉽게 필터링하고 액세스할 수 있도록 하는 스택 워킹을 위한 효율적인 표준 API를 정의합니다.

#### Description

JVM은 필요한 스택 프레임 정보를 트래버스 및 구체화하고 필요할 때 추가 스택 프레임에 대한 효율적인 지연 액세스를 허용하는 유연한 메커니즘을 제공하도록 향상됩니다. 기본 JVM 전환이 최소화됩니다. 구현은 스레드의 스택에 대한 안정적인 보기가 필요합니다. 제어되지 않은 방식으로 추가 조작을 위해 스택 포인터를 보유하는 스트림을 반환하는 것은 작동하지 않습니다. 스트림 팩토리가 반환되는 즉시 JVM이 제어를 재구성할 수 있기 때문입니다. 스택(예: 역최적화를 통해). 이것은 API의 정의에 영향을 미칩니다.

API는 보안 관리자와 함께 실행할 때 동작을 지정하므로 스택 프레임의 클래스 개체에 대한 액세스가 보안을 손상시키지 않습니다.

제안은 스택을 순회하기 위해 기능 기반 StackWalker API를 정의하는 것입니다. 각 StackWalker 개체는 사용할 때마다가 아니라 생성될 때 보안 권한 검사가 수행됩니다. 다음 메서드를 정의합니다.

```java
public <T> T walk(Function<Stream<StackFrame>, T> function);
public Class<?> getCallerClass();
```

`Walk` 메서드는 현재 스레드에 대해 StackFrame의 순차 스트림을 연 다음 StackFrame 스트림과 함께 함수를 적용합니다. 스트림의 스플리터는 스택 프레임 순회를 순서대로 수행합니다. `Stream<StackFrame>` 개체는 한 번만 통과할 수 있으며 도보 메서드가 반환될 때 닫힙니다. 스트림이 닫히면 사용할 수 없게 됩니다. 예를 들어, 구현 클래스의 알려진 목록을 필터링하는 첫 번째 호출자를 찾으려면:

```java
Optional<Class<?>> frame = new StackWalker().walk((s) ->
{
    s.filter(f -> interestingClasses.contains(f.getDeclaringClass()))
     .map(StackFrame::getDeclaringClass)
     .findFirst();
});
To snapshot the stack trace of the current thread,
```

현재 스레드의 스택 추적을 스냅샷하려면,

```java
List<StackFrame> stack =
     new StackWalker().walk((s) -> s.collect(Collectors.toList()));
```

`getCallerClass()` 메서드는 호출자의 프레임을 찾기 위한 편의를 위한 것으로 `sun.reflect.Reflection.getCallerClass`를 대체합니다. `Walk` 메서드를 사용하여 호출자 클래스를 가져오는 동일한 방법은 다음과 같습니다.

```java
walk((s) -> s.map(StackFrame::declaringClass).skip(2).findFirst());
```

### JEP 260: Encapsulate Most Internal APIs

기본적으로 대부분의 JDK 내부 API를 캡슐화하여 컴파일 시간에 액세스할 수 없도록 하고 런타임에 액세스할 수 없는 향후 릴리스를 준비합니다. 중요하고 널리 사용되는 내부 API가 캡슐화되지 않도록 하여 해당 기능의 전부 또는 대부분에 대해 지원되는 대체가 있을 때까지 액세스할 수 있도록 합니다.

### JEP 261: Module System

JSR 376에 지정된 대로 관련 JDK 관련 변경 사항 및 개선 사항과 함께 Java 플랫폼 모듈 시스템을 구현합니다.

#### Description

JSR 376(Java Platform Module System)은 Java 프로그래밍 언어, Java 가상 머신 및 표준 Java API에 대한 변경 및 확장을 지정합니다. 이 JEP는 해당 사양을 구현합니다. 결과적으로 javac 컴파일러, HotSpot 가상 머신 및 런타임 라이브러리는 모듈을 근본적으로 새로운 종류의 Java 프로그램 구성 요소로 구현하고 모든 개발 단계에서 모듈의 안정적인 구성과 강력한 캡슐화를 제공합니다.

이 JEP는 또한 컴파일, 링크 및 실행과 관련된 JSR 범위를 벗어나는 JDK 특정 도구 및 API를 변경, 확장 및 추가합니다. 다른 도구 및 API(예: javadoc 도구 및 Doclet API)에 대한 관련 변경 사항은 별도의 JEP의 주제입니다.

이 JEP는 독자가 최신 State of the Module System 문서와 다른 Project Jigsaw JEP에 익숙하다고 가정합니다.

* [JEP 200: The Modular JDK](https://openjdk.java.net/jeps/200)
* [JEP 201: Modular Source Code](https://openjdk.java.net/jeps/201)
* [JEP 220: Modular Run-Time Images](https://openjdk.java.net/jeps/220)
* [JEP 260: Encapsulate Most Internal APIs](https://openjdk.java.net/jeps/260)
* [JEP 282: jlink: The Java Linker](https://openjdk.java.net/jeps/282)

### JEP 262: TIFF Image I/O

TIFF 이미지 형식을 지원하도록 이미지 I/O 플러그인의 표준 세트를 확장합니다.

#### Description

Java로 완전히 작성된 적절한 TIFF 판독기 및 기록기 플러그인은 이전에 Java Advanced Imaging API 도구 프로젝트(javadoc)에서 개발되었습니다. 이를 기존 이미지 I/O 플러그인과 함께 JDK에 병합합니다. 패키지는 Java SE 사양의 표준 부분이 될 것이기 때문에 `javax.imageio.plugins.tiff`로 이름이 변경됩니다. XML 메타데이터 형식 이름도 비슷하게 변경됩니다.

### JEP 263: HiDPI Graphics on Windows and Linux

Windows 및 Linux에서 HiDPI 그래픽을 구현합니다.

### JEP 264: Platform Logging API and Service

플랫폼 클래스가 해당 메시지의 소비자를 위한 서비스 인터페이스와 함께 메시지를 기록하는 데 사용할 수 있는 최소 로깅 API를 정의합니다. 라이브러리 또는 애플리케이션은 플랫폼 로그 메시지를 선택한 로깅 프레임워크로 라우팅하기 위해 이 서비스의 구현을 제공할 수 있습니다. 구현이 제공되지 않으면 java.util.logging API를 기반으로 하는 기본 구현이 사용됩니다.

#### Goals

* `java.base` 모듈에서 정의 및 사용되므로 `java.util.logging` API에 의존할 수 없습니다.
* SLF4J 또는 Log4J와 같은 외부 로깅 프레임워크를 사용하는 애플리케이션에서 쉽게 채택할 수 있습니다.
* JDK 모듈 그래프를 단순화하기 위해 `java.logging` 모듈에 대한 종속성을 줄입니다.
* 로그 소비자가 초기화되기 전에 플랫폼 클래스가 메시지를 기록할 수 있도록 부트스트랩 문제를 처리합니다.
* 기본적으로 `java.logging` 모듈이 있을 때 `java.util.logging` API를 통해 메시지를 기록합니다.

#### Description

`java.util.ServiceLoader` API를 사용하여 시스템 전체의 LoggerFinder 구현을 찾고 시스템 클래스 로더를 사용하여 로드합니다. 구체적인 구현이 없으면 LoggerFinder 서비스의 JDK 내부 기본 구현이 사용됩니다. 서비스의 기본 구현은 java.logging 모듈이 있을 때 백엔드로 `java.util.logging`을 사용하므로 기본적으로 이전과 같이 로그 메시지가 `java.util.logging.Logger`로 라우팅됩니다. 그러나 LoggerFinder 서비스를 사용하면 `java.util.logging`과 해당 백엔드를 모두 구성할 필요 없이 애플리케이션/프레임워크가 자체 외부 로깅 백엔드를 연결할 수 있습니다.

LoggerFinder 서비스를 구현하면 시스템 로거(BCL(Bootstrap Class Loader)의 시스템 클래스에서 사용)와 응용 프로그램 로거(자체 사용을 위해 응용 프로그램에서 생성)를 구별할 수 있어야 합니다. 이 구분은 플랫폼 보안에 중요합니다. 로거 작성자는 로거가 생성된 클래스 또는 모듈을 LoggerFinder에 전달할 수 있으므로 LoggerFinder는 반환할 로거의 종류를 파악할 수 있습니다.

JDK의 클래스는 System 클래스의 팩토리 메소드를 호출하여 LoggerFinder에서 생성된 로거를 얻습니다.

```java
package java.lang;

...

public class System {

    System.Logger getLogger(String name) { ... }

    System.Logger getLogger(String name, ResourceBundle bundle) { ... }

}
```

JDK 내부 `sun.util.logging.PlatformLogger` API는 이러한 메서드에서 반환된 시스템 로거를 통해 로그 메시지를 내보내도록 수정됩니다.

### JEP 265: Marlin Graphics Renderer

Marlin 렌더러를 기본 그래픽 래스터라이저로 사용하도록 Java 2D를 업데이트합니다.

### JEP 266: More Concurrency Updates

상호 운용 가능한 게시-구독 프레임워크, CompletableFuture API의 개선 사항 및 기타 다양한 개선 사항.

### JEP 267: Unicode 8.0

유니코드 표준 버전 8.0을 지원하도록 기존 플랫폼 API를 업그레이드하십시오.

#### Goals

* Character and String in the java.lang package,
* NumericShaper in the java.awt.font package,
* Bidi, BreakIterator, and Normalizer in the java.text package.

### JEP 268: XML Catalogs

OASIS XML 카탈로그 표준 v1.1을 지원하는 표준 XML 카탈로그 API를 개발합니다. API는 리졸버를 허용하는 JAXP 프로세서와 함께 사용할 수 있는 카탈로그 및 카탈로그 리졸버 추상화를 정의합니다

### JEP 269: Convenience Factory Methods for Collections

Java 프로그래밍 언어에 컬렉션 리터럴이 없는 고통을 완화하기 위해 적은 수의 요소로 컬렉션 및 맵의 인스턴스를 편리하게 생성할 수 있도록 라이브러리 API를 정의합니다.

#### Goals 

컴팩트하고 수정할 수 없는 컬렉션 인스턴스를 생성하는 컬렉션 인터페이스에 대한 정적 팩터리 메서드를 제공합니다. API는 의도적으로 최소한으로 유지됩니다.

#### Description

이러한 컬렉션의 수정 불가능한 인스턴스를 생성하기 위해 `List`, `Set` 및 `Map` 인터페이스에 정적 팩토리 메서드를 제공합니다. (클래스의 정적 메서드와 달리 인터페이스의 정적 메서드는 상속되지 않으므로 구현 클래스나 인터페이스 유형의 인스턴스를 통해 호출할 수 없습니다.)

`List` 및 `Set`의 경우 이러한 팩토리 메서드는 다음과 같이 작동합니다.

```java
List.of(a, b, c);
Set.of(d, e, f, g);
```

여기에는 `varargs` 오버로드가 포함되므로 컬렉션 크기에 대한 고정된 제한이 없습니다. 그러나 이렇게 생성된 컬렉션 인스턴스는 더 작은 크기로 조정할 수 있습니다. 최대 10개의 요소에 대한 특수 케이스 API(고정 인수 오버로드)가 제공됩니다. 이것은 API에 약간의 혼란을 야기하지만 `varargs` 호출로 인해 발생하는 배열 할당, 초기화 및 가비지 수집 오버헤드를 방지합니다. 중요하게도 호출 사이트의 소스 코드는 `fixed-arg` 또는 `varargs` 오버로드가 호출되는지 여부에 관계없이 동일합니다.

`Maps`의 경우 고정 인수 메서드 집합이 제공됩니다.

```java
Map.of()
Map.of(k1, v1)
Map.of(k1, v1, k2, v2)
Map.of(k1, v1, k2, v2, k3, v3)
...
```

최대 10개의 키-값 쌍의 작은 맵을 지원하면 대부분의 사용 사례를 처리하기에 충분할 것으로 예상합니다. 더 많은 수의 항목에 대해 임의의 수의 키-값 쌍이 주어지면 `Map` 인스턴스를 생성하는 API가 제공됩니다.

```java
Map.ofEntries(Map.Entry<K,V>...)
```

이 접근 방식은 `List` 및 `Set`에 대한 동등한 varargs API와 유사하지만 불행히도 각 키-값 쌍을 boxing해야 합니다. 정적 가져오기에 적합한 boxing 키 및 값 방법을 사용하면 다음과 같이 더 편리하게 사용할 수 있습니다.

```java
Map.Entry<K,V> entry(K k, V v)
```

이러한 방법을 사용하여 임의의 수의 항목으로 맵을 생성할 수 있습니다.

```java
Map.ofEntries(
    entry(k1, v1),
    entry(k2, v2),
    entry(k3, v3),
    // ...
    entry(kn, vn));
```

### JEP 270: Reserved Stack Areas for Critical Sections

스택 오버플로가 발생하는 경우에도 완료할 수 있도록 임계 섹션에서 사용할 스레드 스택에 추가 공간을 예약합니다.

#### Goals

중요한 섹션에서 발생하는 `StackOverflowError`로 인해 발생하는 `java.util.concurrent` 잠금(예: `ReentrantLock`)과 같은 중요한 데이터의 손상으로 인한 교착 상태의 위험을 완화하는 메커니즘을 제공합니다.

솔루션은 `java.util.concurrent` 알고리즘이나 공개된 인터페이스, 기존 라이브러리 및 애플리케이션 코드를 수정할 필요가 없도록 대부분 JVM 기반이어야 합니다.

솔루션은 `ReentrantLock` 케이스로 제한되어서는 안 되며 권한 있는 코드의 모든 중요 섹션에 적용할 수 있어야 합니다.

### JEP 271: Unified GC Logging

JEP 158에 도입된 통합 JVM 로깅 프레임워크를 사용하여 GC 로깅을 다시 구현합니다.

### JEP 272: Platform-Specific Desktop Features

작업 표시줄 또는 도크와 상호 작용하거나 시스템 또는 애플리케이션 이벤트 수신과 같은 플랫폼별 데스크톱 기능에 액세스하기 위해 새로운 공개 API를 정의합니다.

##### API

기존 `java.awt.Desktop` 클래스에 이 두 가지 하위 작업에 대한 공개 API를 추가할 것을 제안합니다. 대상 지원 플랫폼은 Mac OS X, Windows, Linux입니다.

제안된 API 스케치:

```java
package java.awt;

public class Desktop {

    /* ... */

    /**
     * Adds sub-types of {@link AppEventListener} to listen for notifications
     * from the native system.
     *
     * @param listener
     * @see AppForegroundListener
     * @see AppHiddenListener
     * @see AppReOpenedListener
     * @see AppScreenSleepListener
     * @see AppSystemSleepListener
     * @see AppUserSessionListener
     */

    public void addAppEventListener(final AppEventListener listener) {}

    /**
     * Requests user attention to this application (usually through bouncing the Dock icon).
     * Critical requests will continue to bounce the Dock icon until the app is activated.
     *
     */
    public void requestUserAttention(final boolean critical) {}

    /**
     * Attaches the contents of the provided PopupMenu to the application's Dock icon.
     */
    public void setDockMenu(final PopupMenu menu) {}

    /**
     * Changes this application's Dock icon to the provided image.
     */
    public void setDockIconImage(final Image image) {}


    /**
     * Affixes a small system provided badge to this application's Dock icon. Usually a number.
     */
    public void setDockIconBadge(final String badge) {}

    /**
     * Displays or hides a progress bar or other indicator in
     * the dock.
     *
     * @see DockProgressState.NORMAL
     * @see DockProgressState.PAUSED
     * @see DockProgressState.ERROR
     *
     * @see #setDockProgressValue
     */
    public void setDockProgressState(int state) {}

    /**
     * Sets the progress bar's current value to {@code n}.
     */
    public void setDockProgressValue(int n) {}

    /**
     * Tests whether a feature is supported on the current platform.
     */

    public boolean isSupportedFeature(Feature f) {}

    /* ... */
}
```

### JEP 273: DRBG-Based SecureRandom Implementations

NIST 800-90Ar1에 설명된 세 가지 DRBG(결정적 랜덤 비트 생성기) 메커니즘을 구현합니다.

### JEP 274: Enhanced Method Handles

`java.lang.invoke` 패키지의 `MethodHandle`, `MethodHandles` 및 `MethodHandles.Lookup` 클래스를 향상하여 일반적인 사용 사례를 용이하게 하고 새로운 `MethodHandle` 결합기 및 조회 개선을 통해 컴파일러 최적화를 개선할 수 있습니다.

#### Goals

* `java.lang.invoke` 패키지의 `MethodHandles` 클래스에서 루프 및 `try/finally` 블록에 대한 새로운 `MethodHandle` 결합자를 제공하십시오.
* 인수 처리를 위한 새로운 `MethodHandle` 결합자로 `MethodHandle` 및 `MethodHandles` 클래스를 향상합니다.
* `MethodHandles.Lookup` 클래스에서 인터페이스 메서드 및 선택적으로 슈퍼 생성자에 대한 새로운 조회를 구현합니다.

### JEP 275: Modular Java Application Packaging

모듈 인식 및 사용자 정의 런타임 생성을 포함하여 Project Jigsaw의 기능을 Java Packager에 통합합니다.

### JEP 276: Dynamic Linking of Language-Defined Object Models

`INVOKEDYNAMIC` 호출 사이트에서 이름으로 표현되는 *read a property*, *write a property*, *invoke a callable object* 등과 같은 개체에 대한 상위 수준 작업을 연결하기 위한 기능을 제공합니다. 일반 Java 객체에서 이러한 작업의 일반적인 의미를 위한 기본 링커와 언어별 링커를 설치하는 기능을 제공합니다.

#### Goals

주요 목표는 컴파일 타임에 `INVOKEDYNAMIC` 명령어에 대해 알 수 없는 유형의 표현식에 대한 고급 개체 작업을 컴파일할 수 있도록 하는 것입니다(예: obj.color가 `INVOKEDYNAMIC` "dyn:getProp:color"가 됨). 제공된 인프라는 런타임에 이러한 호출 사이트에 대한 링크 요청을 특정 개체 유형에 대한 지식이 있는 링커 집합으로 전달하고 작업의 적절한 구현을 위한 메서드 핸들을 생성할 수 있습니다.

이러한 기능은 컴파일 시간에 유형을 알 수 없고 이러한 개체에 대한 일반적인 개체 지향 작업을 표현해야 하는 개체 식의 개념이 있는 언어로 작성된 프로그램의 런타임 구현을 위한 기반을 제공합니다.

다중 언어 런타임 링커를 구성하는 기능은 단일 JVM 프로세스에 공존하는 다중 언어 런타임 간에 적절한 양의 상호 운용성을 허용합니다. 한 언어의 컴파일러에서 내보낸 `INVOKEDYNAMIC` 호출 사이트는 한 런타임에 속한 개체가 다른 런타임으로 전달될 때 다른 언어의 링커에서 링크할 수 있어야 합니다.

#### Description

현재 JDK 8에서 Nashorn의 내부 종속성으로 제공되는 `jdk.internal.dynalink.*` 패키지의 코드에는 작동하는 구현이 포함되어 있습니다. 우리는 이를 `jdk.dynalink`라는 새 모듈에서 호스팅되는 `jdk.dynalink.*`라는 패키지 세트로 개선하고 노출하려고 합니다.

### JEP 277: Enhanced Deprecation

@Deprecated 주석을 개선하고 API 수명 주기를 강화하는 도구를 제공합니다.

#### Goals

* 사양에서 API의 상태 및 의도된 처리에 대한 더 나은 정보를 제공합니다.
* 더 이상 사용되지 않는 API의 애플리케이션의 정적 사용을 분석하는 도구 제공

### JEP 278: Additional Tests for Humongous Objects in G1

G1 Garbage Collector의 거대한 개체 기능에 대한 추가 화이트박스 테스트를 개발합니다.

### JEP 279: Improve Test-Failure Troubleshooting

테스트 실패 및 시간 초과 시 추가 문제 해결에 사용할 수 있는 진단 정보를 자동으로 수집합니다.

#### Goals

테스트 실패 및 시간 초과를 진단하는 데 도움이 되는 다음 정보를 수집합니다.

* 테스트 실패 또는 시간 초과 후에도 호스트에서 계속 실행 중인 Java 프로세스의 경우:
  * C and Java stacks
  * Core dumps (minidumps on Windows)
  * Heap statistics
* 환경 정보:
  * Running processes
  * CPU and I/O loads
  * Open files and sockets
  * Free disk space and memory
  * Most recent system messages and events

이 기능을 제공하는 라이브러리를 개발하고 라이브러리 소스를 제품 코드와 함께 배치합니다.

#### Description

현재 `jtreg` 테스트 하니스에는 두 개의 확장점이 있습니다. 첫 번째는 테스트 시간이 초과될 때 `jtreg`가 실행하는 시간 초과 처리기입니다. 두 번째는 관찰자 디자인 패턴을 구현하여 테스트 실행에서 다양한 이벤트를 추적하는 관찰자입니다. 우리는 이 확장점을 사용하여 진단 정보를 수집하고 `jtreg`에 대한 사용자 지정 관찰자 및 시간 초과 처리기를 개발할 것입니다.

환경 및 비Java 프로세스에 대한 정보는 플랫폼별 명령을 실행하여 수집됩니다. Java 프로세스에 대한 정보 수집은 [JEP 228](https://openjdk.java.net/jeps/228)에 의해 크게 확장된 사용 가능한 진단 명령(예: hs_err 파일과 유사한 정보를 수집하는 print_vm_state 명령)을 통해 수행됩니다. 수집된 정보는 테스트 결과와 함께 추후 검사를 위해 저장됩니다. 관찰자는 테스트가 실패할 때 `FinishedTest` 이벤트에 대한 정보를 수집합니다.

테스트는 다른 프로세스를 생성할 수 있으므로 테스트 프로세스 및 해당 하위 프로세스에 대한 정보가 수집됩니다. 이러한 프로세스를 찾기 위해 라이브러리는 루트에 원래 테스트 프로세스가 있는 프로세스 트리를 생성합니다.

라이브러리 소스는 최상위 리포지토리의 테스트 디렉토리에 배치되고 makefile이 업데이트되어 빌드하고 테스트 번들의 일부로 번들됩니다.

### JEP 280: Indify String Concatenation

JDK 라이브러리 함수에 대한 `invokedynamic` 호출을 사용하도록 `javac`에 의해 생성된 정적 문자열 연결 바이트 코드 시퀀스를 변경하십시오. 이렇게 하면 `javac`에서 내보낸 바이트코드를 추가로 변경할 필요 없이 문자열 연결의 향후 최적화가 가능해집니다.

#### Goals

Java-to-bytecode 컴파일러를 변경할 필요 없이 구현 가능한 최적화된 문자열 연결 핸들러를 구축하기 위한 토대를 마련합니다. 이 작업에 대한 동기 부여의 예로 여러 번역 전략을 시도해야 합니다. 최적화된 번역 전략을 생성(및 전환)하는 것이 이 JEP의 확장 목표입니다.

#### Description

`invokedynamic`의 기능을 사용할 것입니다. 초기 호출 중에 호출 대상을 한 번 부트스트랩하는 수단을 제공하여 지연 연결을 위한 기능을 제공합니다. 이 접근 방식은 새로운 것이 아니며 람다 식을 번역하는 현재 코드에서 광범위하게 차용합니다.

아이디어는 전체 `StringBuilder` 추가 댄스를 연결이 필요한 값을 수락하는 `java.lang.invoke.StringConcatFactory`에 대한 간단한 `invokedynamic` 호출로 대체하는 것입니다.

```java
String m(String a, int b) {
  return a + "(" + b + ")";
}
```

이는 다음과 같이 컴파일됩니다.

```java
java.lang.String m(java.lang.String, int);
       0: new           #2                  // class java/lang/StringBuilder
       3: dup
       4: invokespecial #3                  // Method java/lang/StringBuilder."<init>":()V
       7: aload_1
       8: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      11: ldc           #5                  // String (
      13: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      16: iload_2
      17: invokevirtual #6                  // Method java/lang/StringBuilder.append:(I)Ljava/lang/StringBuilder;
      20: ldc           #7                  // String )
      22: invokevirtual #4                  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
      25: invokevirtual #8                  // Method java/lang/StringBuilder.toString:()Ljava/lang/String;
      28: areturn
```

그러나 `-XDstringConcat=indy`를 통해 제안된 구현에서 사용할 수 있는 순진한 indy 번역을 사용하더라도 훨씬 더 간단할 수 있습니다.

```java
java.lang.String m(java.lang.String, int);
       0: aload_1
       1: ldc           #2                  // String (
       3: iload_2
       4: ldc           #3                  // String )
       6: invokedynamic #4,  0              // InvokeDynamic #0:makeConcat:(Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;)Ljava/lang/String;
      11: areturn

BootstrapMethods:
  0: #19 invokestatic java/lang/invoke/StringConcatFactory.makeConcat:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
```

박싱 없이 `int` 인수를 전달하는 방법에 주목하세요. 런타임에 부트스트랩 메서드(BSM)가 실행되고 연결을 수행하는 실제 코드에서 연결됩니다. 적절한 `invokestatic` 호출로 `invokedynamic` 호출을 다시 작성합니다. 이것은 상수 풀에서 상수 문자열을 로드하지만 BSM 정적 인수를 활용하여 이러한 상수와 다른 상수를 BSM 호출에 직접 전달할 수 있습니다. 이것은 제안된 `-XDstringConcat=indyWithConstants` 플레이버가 하는 일입니다:

```java
java.lang.String m(java.lang.String, int);
       0: aload_1
       1: iload_2
       2: invokedynamic #2,  0              // InvokeDynamic #0:makeConcat:(Ljava/lang/String;I)Ljava/lang/String;
       7: areturn

BootstrapMethods:
  0: #15 invokestatic java/lang/invoke/StringConcatFactory.makeConcatWithConstants:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #16 \u0001(\u0001)
```

동적 인수("a" 및 "b")만 BSM에 전달하는 방법에 주목하십시오. 정적 상수는 연결 중에 이미 처리됩니다. BSM 방법에는 동적 및 정적 인수를 연결하는 순서와 정적 인수가 무엇인지 알려주는 레시피가 제공됩니다. 이 전략은 null, 기본형 및 빈 문자열도 별도로 처리합니다.

어떤 바이트코드 풍미가 기본값이어야 하는지는 미해결 질문입니다. 바이트코드 모양, 연결 유형 및 성능 데이터에 대한 자세한 내용은 실험 노트에서 확인할 수 있습니다. 제안된 부트스트랩 메서드 API는 여기에서 찾을 수 있습니다. 완전한 구현은 샌드박스 분기에서 찾을 수 있습니다.

```bash
$ hg clone http://hg.openjdk.java.net/jdk9/sandbox sandbox 
$ cd sandbox/ 
$ sh ./common/bin/hgforest.sh up -r JDK-8085796-indyConcat
$ sh ./configure 
$ make images
```

다음을 사용하여 기준 런타임과 패치된 런타임 간의 차이를 확인할 수 있습니다.

```bash
$ hg diff -r default:JDK-8085796-indyConcat
$ cd langtools/
$ hg diff -r default:JDK-8085796-indyConcat
$ cd jdk/
$ hg diff -r default:JDK-8085796-indyConcat
```

벤치마크는 여기에서 찾을 수 있습니다: http://cr.openjdk.java.net/~shade/8085796/

제안된 구현은 JDK를 성공적으로 빌드하고 회귀 테스트(String concat을 테스트하는 새 테스트 포함)를 실행하고 모든 플랫폼에서 스모크 테스트를 통과합니다. 실제 연결에 여러 전략을 사용할 수 있습니다. 우리가 제안한 구현은 javac에 의해 생성된 바이트코드 시퀀스를 동일한 바이트코드를 주입하는 BSM으로 이동할 때 처리량 적중이 없음을 보여줍니다. 이는 접근 방식을 검증합니다. 최적화된 전략은 특히 기본 StringBuilder 길이가 충분하지 않거나 VM의 최적화가 실패한 경우 기준선과 같거나 더 나은 성능을 보이는 것으로 표시됩니다.

### JEP 281: HotSpot C++ Unit-Test Framework

HotSpot용 C++ 단위 테스트 개발을 활성화하고 장려합니다.

#### GOals

* 메서드, 클래스 및 하위 시스템에 대한 단위 테스트 작성 및 실행 지원
* 유닛만 테스트되고 다른 것은 실행되지 않는 유닛 테스트 지원
* VM 초기화가 필요한 테스트 지원
* 실행 시간이 밀리초 단위인 빠른 테스트 지원
* 양성 및 음성 테스트 모두 지원
* 테스트 격리 허용
* 제품 소스 코드와 함께 배치된 지원 테스트
* 현재 인프라와의 통합 지원
* 각 테스트에 대한 개별 결과 생성
* 개별 테스트를 쉽게 실행할 수 있습니다(명령줄에서).
* 테스트 실패에 대해 최소한의 재현자를 제공할 수 있어야 합니다.
* IDE 지원 제공
* 프레임워크에 대한 빠른 수정을 포함하여 프레임워크의 발전을 허용합니다.
* `jtreg`와 유사한 세분성으로 테스트 선택 및 테스트 그룹화 지원
* 모든 컴파일 대상, 제품 및 디버그 테스트 허용
* 플랫폼 종속 코드 테스트 허용
* 최소한의 문서 제공: 리포지토리의 방법 Wiki 및 예제
* 테스트 소스 또는 제외 목록과 같은 기타 파일을 수정하여 실행에서 테스트 제외 허용
* 모든 내부 테스트 변환 지원
* Oracle에서 지원하는 JDK 9 빌드 플랫폼 지원

### JEP 282: jlink: The Java Linker

[JEP 220](https://openjdk.java.net/jeps/220)에 정의된 대로 일련의 모듈과 해당 종속성을 사용자 지정 런타임 이미지로 조합하고 최적화할 수 있는 도구를 만듭니다.

#### Description

링커 도구인 `jlink`의 기본 호출은 다음과 같습니다.

```bash
$ jlink --module-path <modulepath> --add-modules <modules> --limit-modules <modules> --output <path>
```

* `--module-path`는 링커가 관찰 가능한 모듈을 발견하는 경로입니다. 이들은 모듈식 JAR 파일, JMOD 파일 또는 분해된 모듈일 수 있습니다.
* `--add-modules`는 런타임 이미지에 추가할 모듈의 이름을 지정합니다. 이러한 모듈은 전이적 종속성을 통해 추가 모듈이 추가되도록 할 수 있습니다.
* `--limit-modules`는 관찰 가능한 모듈의 범위를 제한합니다.
* `--output`은 결과 런타임 이미지를 포함할 디렉토리입니다.
* `--module-path`, `--add-modules` 및 `--limit-modules` 옵션은 [JEP 261](https://openjdk.java.net/jeps/261)에 자세히 설명되어 있습니다.

`jlink` 가 지원할 다른 옵션은 다음과 같습니다.

* `--help` 사용법/도움말 메시지 인쇄
* `--version` 버전 정보를 출력하는 버전

### JEP 283: Enable GTK 3 on Linux

JavaFX, Swing 또는 AWT를 기반으로 하는 Java 그래픽 애플리케이션을 활성화하여 Linux에서 GTK 2 또는 GTK 3을 사용합니다.

#### Goals

* 기본적으로 기본 GTK 2를 지원하고 GTK 3으로 페일 포워드합니다.
* 시스템 속성으로 표시되는 경우 GTK 3을 사용하십시오.
* 상호 운용성을 위해 GTK 3이 필요하고 이 요구 사항을 충분히 조기에 감지할 수 있는 경우 GTK 3을 자동으로 활성화하십시오.
* GTK 2 또는 GTK 3 중 하나 또는 둘 모두가 설치된 Linux 시스템에서 기존 애플리케이션을 수정하지 않고 실행할 수 있습니다.

### JEP 284: New HotSpot Build System

빌드 인프라 프레임워크를 사용하여 HotSpot 빌드 시스템을 다시 작성합니다.

#### Goals

* 이 프로젝트의 목표는 현재 빌드 시스템을 빌드 인프라 프레임워크를 기반으로 하는 새롭고 훨씬 단순화된 시스템으로 교체하는 것입니다. 더 구체적으로:
* 빌드 인프라 프레임워크에 있는 기능을 활용하여 코드 중복을 최소화합니다.
HotSpot 빌드 시스템을 단순화하여 유지 관리가 더 쉬운 코드 기반을 제공하고 향후 개선을 위한 임계값을 낮춥니다.

#### Description

HotSpot을 구축하는 것은 높은 수준에서 JDK에서 다른 기본 구성 요소를 구축하는 것과 크게 다르지 않습니다. 본질적으로 libjvm.so에 대한 빌드 인프라 함수 SetupNativeCompilation()을 호출해야 합니다. 실제로 HotSpot 빌드는 JDK 리포지토리의 기본 라이브러리와 다르게 발전했으므로 수행해야 할 몇 가지 조정이 있습니다.

기술적인 차이점의 몇 가지 예:

* HotSpot은 지원해야 하는 미리 컴파일된 헤더를 사용합니다.
* HotSpot은 제품의 나머지 부분에서 사용되는 것과 다른 자체 컴파일러 플래그 집합을 사용합니다.
* `libjvm.so`는 서버 및 클라이언트와 같은 다양한 변형에 대해 여러 번 빌드될 수 있습니다.
* HotSpot은 C1 및 JVMCI와 같이 활성화 또는 비활성화할 수 있는 여러 가지 기능을 사용합니다.
* 역사적 이유로 HotSpot은 플랫폼과 컴파일러에 대해 다른 이름을 사용합니다.
* `libjvm.so` 기본 라이브러리를 컴파일하는 것 외에도 다음과 같은 다른 사전/사후 빌드 작업이 필요합니다.

`adlc` 컴파일러와 같은 빌드 도구 만들기.

* adlc 및 JVMTI 도구를 사용하여 gensrc 만들기.
* Dtrace 지원에는 사전 및 사후 처리가 모두 필요합니다.
* `libjsig.so`와 같은 추가 라이브러리를 빌드해야 합니다.

### JEP 285: Spin-Wait Hints

Java 코드가 스핀 루프가 실행되고 있음을 암시하도록 API를 정의합니다.

#### Goals

Java 코드가 스핀 루프에 있음을 런타임 시스템에 알릴 수 있도록 API를 정의하십시오. API는 순수한 힌트가 될 것이며 의미론적 동작 요구 사항을 전달하지 않습니다(예: no-op는 유효한 구현임). JVM이 특정 하드웨어 플랫폼에서 유용할 수 있는 스핀 루프 특정 동작의 이점을 얻을 수 있도록 합니다. JDK에서 무작동 구현과 고유 구현을 모두 제공하고 하나 이상의 주요 하드웨어 플랫폼에서 실행 이점을 보여줍니다.

### JEP 287: SHA-3 Hash Algorithms

NIST FIPS 202에 지정된 SHA-3 암호화 해시 함수(BYTE 전용)를 구현합니다.

#### Description

FIPS 202는 SHA3-224, SHA3-256, SHA3-384 및 SHA3-512의 4가지 새로운 해시 함수를 정의합니다. 이들은 표준 이름 "SHA3-224", "SHA3-256", "SHA3-384" 및 "SHA3-512"로 `java.security.MessageDigest` API의 새로운 알고리즘으로 구현될 수 있습니다. 매개변수가 필요하지 않으므로 새 API가 필요하지 않습니다.

다음은 목록과 해당 알고리즘 개선 사항입니다.

* "SUN" provider: SHA3-224, SHA3-256, SHA3-384, and SHA3-512
* "OracleUcrypto" provider: SHA-3 digests supported by Solaris 12.0

### JEP 288: Disable SHA-1 Certificates

SHA-1 기반 서명으로 X.509 인증서 체인을 비활성화하는 보다 유연한 메커니즘을 제공하여 JDK의 보안 구성을 개선합니다.

#### Description

특히 공개적으로 신뢰할 수 있는 SSL/TLS 서버의 경우 SHA-1 인증서 사용이 계속 감소하고 있습니다. 그러나 많은 기업은 일반적으로 새로운 알고리즘 제한 사항에 적응하는 데 더 많은 시간이 필요한 사설 인증 기관을 사용합니다. 또한 SHA-1 인증서로 이전에 서명되고 타임스탬프가 지정된 코드는 앞으로도 한동안 계속 작동해야 합니다. 따라서 모든 SHA-1 인증서를 비활성화하면 많은 응용 프로그램이 중단될 수 있습니다. 따라서 이 JEP는 알고리즘 제약 메커니즘을 개선하여 보다 유연한 SHA-1 제한 정책을 구현할 수 있습니다.

특히 `jdk.certpath.disabledAlgorithms` 보안 속성의 사양이 다음과 같이 향상되었습니다.

1. `jdkCA`라는 새 제약 조건이 설정되면 JDK cacerts 키 저장소에 사전 설치된 트러스트 앵커에 의해 앵커된 인증서 체인에서 사용되는 경우 알고리즘을 제한합니다. 이 조건은 이후에 `cacerts` 키 저장소에 추가되는 인증서를 포함하여 다른 인증서에 의해 고정된 인증서 체인에는 적용되지 않습니다. 또한 트러스트 앵커 인증서는 직접 신뢰할 수 있으므로 제한 사항이 적용되지 않습니다.
2. `DenyAfter`라는 새 제약 조건이 설정되면 지정된 날짜 이후에 인증서 체인에서 사용되는 경우 알고리즘을 제한합니다. 트러스트 앵커 인증서는 직접 신뢰되기 때문에 제한 사항이 적용되지 않습니다. 또한 서명된 JAR에서 사용되는 코드 서명 인증서 체인은 다음과 같이 특별히 처리됩니다.
   1.  타임스탬프가 지정되지 않은 서명된 JAR과 함께 인증서 체인을 사용하는 경우 지정된 날짜 이후에 제한됩니다.
   2.  타임스탬프가 찍힌 서명된 JAR과 함께 인증서 체인을 사용하는 경우 지정된 날짜 이전에 타임스탬프가 찍힌 경우 제한되지 않습니다. JAR이 지정된 날짜 이후에 타임스탬프되면 제한됩니다.
3.  사용이라는 새 제약 조건이 설정되면 지정된 용도에 대한 인증서 체인에서 사용되는 경우 알고리즘을 제한합니다. TLS/SSL 서버 인증서 체인용 TLSServer, TLS/SSL 클라이언트 인증서 체인용 TLSClient 및 서명된 JAR과 함께 사용되는 인증서 체인용 SignedJAR의 세 가지 용도가 처음에 지원됩니다.

위의 개선 사항 이후의 `jdk.certpath.disabledAlgorithms` 보안 속성 사양은 다음과 같습니다(각 제약 조건의 정의는 `java.security` 파일 참조).

```
DisabledAlgorithms:
    " DisabledAlgorithm { , DisabledAlgorithm } "

DisabledAlgorithm:
    AlgorithmName [Constraint] { '&' Constraint }

AlgorithmName:
    (see below)

Constraint:
    KeySizeConstraint | CAConstraint | DenyAfterConstraint |
    UsageConstraint

KeySizeConstraint:
    keySize Operator KeyLength

Operator:
    <= | < | == | != | >= | >

KeyLength:
    Integer value of the algorithm's key length in bits

CAConstraint:
    jdkCA

DenyAfterConstraint:
    denyAfter YYYY-MM-DD

UsageConstraint: 
    usage [TLSServer] [TLSClient] [SignedJAR]
```

또한 j`dk.jar.disabledAlgorithms` 보안 속성의 사양이 다음과 같이 향상되었습니다.

1. `DenyAfter`라는 새 제약 조건이 설정되면 다음과 같이 지정된 날짜 이후에 서명된 JAR에서 사용되는 경우 알고리즘을 제한합니다.
   1. JAR에 타임스탬프가 없으면 지정된 날짜 이후에 제한됩니다(서명되지 않은 것으로 처리됨).
   2. JAR에 타임스탬프가 있는 경우 지정된 날짜 이전에 타임스탬프가 지정된 경우 제한되지 않습니다. JAR이 지정된 날짜 이후에 타임스탬프되면 제한됩니다.

위의 개선 사항 이후 `jdk.jar.disabledAlgorithms` 보안 속성의 사양은 다음과 같습니다(각 제약 조건의 정의는 `java.security` 파일 참조).

```
DisabledAlgorithms:
    " DisabledAlgorithm { , DisabledAlgorithm } "

DisabledAlgorithm:
    AlgorithmName [Constraint] { '&' Constraint }

AlgorithmName:
    (see below)

Constraint:
    KeySizeConstraint | DenyAfterConstraint

KeySizeConstraint:
    keySize Operator KeyLength

DenyAfterConstraint:
    denyAfter YYYY-MM-DD

Operator:
    <= | < | == | != | >= | >

KeyLength:
    Integer value of the algorithm's key length in bits
```

몇 가지 예가 있습니다.

`cacerts` 파일에 사전 설치된 신뢰 앵커에 연결된 SHA-1 인증서를 비활성화하려면 `jdk.certpath.disabledAlgorithms` 보안 속성에 "SHA1 jdkCA"를 추가합니다.

```
jdk.certpath.disabledAlgorithms=MD2, MD5, RSA keySize < 1024, \
        DSA keySize < 1024, EC keySize < 224, SHA1 jdkCA
```

`cacerts` 파일에 사전 설치된 앵커를 신뢰하는 TLS 서버 및 해당 체인의 인증에 사용되는 SHA-1 인증서를 비활성화하려면 `jdk.certpath.disabledAlgorithms` 보안 속성에 "SHA1 jdkCA & usage TLSServer"를 추가합니다.

```java
jdk.certpath.disabledAlgorithms=MD2, MD5, RSA keySize < 1024, \
        DSA keySize < 1024, EC keySize < 224, SHA1 jdkCA & usage 
```

2017년 1월 1일 이전에 타임스탬프가 찍힌 JAR을 제외하고 서명된 JAR에서 SHA-1을 비활성화하려면 "SHA1 usage SignedJAR & denyAfter 2017-01-01"을 `jdk.certpath.disabledAlgorithms` 보안 속성에 추가하고 "SHA1 denyAfter 2017-01- 01"에서 `jdk.jar.disabledAlgorithms` 보안 속성:

```
jdk.certpath.disabledAlgorithms=MD2, MD5, RSA keySize < 1024, \
        DSA keySize < 1024, EC keySize < 224, \
        SHA1 usage SignedJAR & denyAfter 2017-01-01

jdk.jar.disabledAlgorithms=MD2, MD5, RSA keySize < 1024, \
        DSA keySize < 1024, SHA1 denyAfter 2017-01-01
```

### JEP 289: Deprecate the Applet API

웹 브라우저 공급업체가 Java 브라우저 플러그인에 대한 지원을 제거함에 따라 빠르게 관련성이 없어지고 있는 Applet API를 더 이상 사용하지 않습니다. Java Web Start 또는 설치 가능한 응용 프로그램과 같은 대체 기술에 대해 개발자를 안내합니다.

#### Description

`@Deprecated(since="9")` 주석을 다음 클래스에 추가합니다.

* `java.applet.AppletStub`
* `java.applet.Applet`
* `java.applet.AudioClip`
* `java.applet.AppletContext`
* `javax.swing.JApplet`

다음 주요 릴리스에서는 Applet API를 제거할 계획이 없으므로 이러한 주석에서 `forRemoval = true`를 지정하지 않습니다. 나중에 이 API를 제거할 것을 제안한다면 사전에 최소한 하나의 주요 릴리스에 `forRemoval = true`를 이러한 주석에 추가할 것입니다.

애플릿 뷰어 도구도 더 이상 사용되지 않습니다. 도구가 시작되면 사용 중단 경고가 표준 오류 스트림에 인쇄됩니다.

### JEP 290: Filter Incoming Serialization Data

보안과 견고성을 모두 향상시키기 위해 개체 직렬화 데이터의 수신 스트림을 필터링할 수 있습니다.

#### Goals

* 응용 프로그램에서 사용할 수 있는 모든 클래스에서 컨텍스트에 적합한 클래스 집합으로 역직렬화할 수 있는 클래스의 범위를 좁힐 수 있는 유연한 메커니즘을 제공합니다.
* 일반 그래프 동작을 검증하기 위해 역직렬화 중에 그래프 크기 및 복잡성에 대한 메트릭을 필터에 제공합니다.
* 호출에서 예상되는 클래스의 유효성을 검사하기 위해 RMI 내보낸 개체에 대한 메커니즘을 제공합니다.
* 필터 메커니즘은 `ObjectInputStream`의 기존 서브클래스에 대한 서브클래싱 또는 수정을 요구하지 않아야 합니다.
* 속성 또는 구성 파일로 구성할 수 있는 전역 필터를 정의합니다.

#### Description

핵심 메커니즘은 직렬화 클라이언트에 의해 구현되고 `ObjectInputStream`에 설정된 필터 인터페이스입니다. 필터 인터페이스 메서드는 역직렬화 프로세스 동안 호출되어 역직렬화되는 클래스, 생성되는 배열의 크기, 스트림 길이, 스트림 깊이 및 스트림이 디코딩되는 동안 참조 수를 설명하는 메트릭을 확인합니다. 필터는 상태를 수락, 거부 또는 미정 상태로 두는 상태를 반환합니다.

##### ObjectInputFilter 인터페이스 및 API

객체 입력 필터 인터페이스는 RMI 및 직렬화 클라이언트에 의해 구현되며 프로세스 전반에 걸쳐 구성 가능한 필터의 동작을 제공합니다.

```java
interface ObjectInputFilter {
    Status checkInput(FilterInput filterInfo);

    enum Status { 
        UNDECIDED, 
        ALLOWED, 
        REJECTED; 
    }

   interface FilterInfo {
         Class<?> serialClass();
         long arrayLength();
         long depth();
         long references();
         long streamBytes();
   }

    public static class Config {
        public static void setSerialFilter(ObjectInputFilter filter);
        public static ObjectInputFilter getSerialFilter(ObjectInputFilter filter) ;
        public static ObjectInputFilter createFilter(String patterns);
    }   
}
```

##### ObjectInputStream 필터

`ObjectInputStream`에는 현재 필터를 설정하고 가져오는 추가 메서드가 있습니다. `ObjectInputStream`에 대해 설정된 필터가 없으면 전역 필터가 사용됩니다(있는 경우).

```java
public class ObjectInputStream ... {
    public final void setObjectInputFilter(ObjectInputFilter filter);
    public final ObjectInputFilter getObjectInputFilter(ObjectInputFilter filter);
}
```

### JEP 291: Deprecate the Concurrent Mark Sweep (CMS) Garbage Collector

CMS(Concurrent Mark Sweep) 가비지 수집기를 사용하지 않으며 향후 주요 릴리스에서 지원을 중단합니다.

#### Goals

HotSpot에서 다른 가비지 수집기의 개발을 가속화하십시오.

#### Description

`-XX:+UseConcMarkSweepGC` 옵션을 통해 명령줄에서 경고 메시지가 요청될 때 경고 메시지가 발행되도록 CMS를 더 이상 사용하지 않습니다.

이 JEP는 CMS에 대한 지원이 중단될 주요 릴리스를 지정하지 않습니다. 그렇게 할 시기에 대한 결정은 G1 수집기가 CMS를 대체하기에 적합한 것으로 입증되는 정도에 따라 결정됩니다. 그동안 CMS 사용자는 G1 수집기로 마이그레이션하는 것이 좋습니다(`-XX:+UseG1GC`).

### JEP 292: Implement Selected ECMAScript 6 Features in Nashorn

ECMAScript 6 또는 줄여서 ES6이라고도 하는 ECMA-262 6판에 도입된 여러 새로운 기능 중 선택된 집합을 Nashorn에서 구현합니다.

#### Goals

JDK 9의 Nashorn에서 상당수의 ES6 기능을 올바르게 구현합니다.

이 작업의 규모 때문에 JDK 9가 첫 번째 단계일 뿐인 여러 단계로 ES6을 제공해야 합니다. 나머지 ES6 기능은 JDK 9 업데이트 릴리스와 향후 주요 JDK 릴리스에서 제공될 것입니다.

#### Description

ECMAScript 6에는 다음과 같은 새로운 기능이 포함되어 있습니다.

* Arrow functions: `=>` 구문을 사용하여 함수를 정의하는 간결한 방법
* Classes: 상속, 생성자 및 메서드를 사용하여 클래스를 정의하는 방법
* Enhanced object literals: 특수 및 계산된 속성 키 지원
* Template strings: 동적으로 평가되는 여러 줄 문자열
* Destructuring assignment: 개체 또는 배열 구문을 사용한 할당 바인딩
* Default, rest, and spread parameters: 보다 유연한 인수 전달
* `let`, `const`, and block scope: 변수 및 상수의 블록 범위 선언
* Iterators and for..of loops: 임의의 객체를 반복하는 프로토콜
* Generators: 반복자를 생성하는 특별한 종류의 함수
* Unicode: 이전 버전과의 호환성을 통한 완전한 유니코드 지원
* Modules: 모듈 정의를 위한 언어 수준 지원
* Module loaders: 동적 로딩, 격리 및 컴파일 후크 지원
* `Map`, `Set`, `WeakMap`, `WeakSet`: 다양한 새 컬렉션 클래스
* Proxies: 특별한 동작을 가진 객체 생성 허용
* Symbols: 새로운 종류의 고유한 속성 키
* Subclassable built-ins: Array 및 Date와 같은 내장 기능을 서브클래싱할 수 있습니다.
* `Promises`: 비동기식 미래 완료를 위한 API
* Math, Number, String 및 Object API: 내장 객체에 대한 다양한 새 기능
* Binary and octal literals: 숫자 리터럴의 새로운 형식
* Reflection API: 메타 프로그래밍 작업을 수행하기 위한 API
* Tail calls: 무제한 스택 증가 없이 재귀 코드 허용

이러한 기능 중 JDK 8u40에서 [JEP 203](https://openjdk.java.net/jeps/203)으로 let, const 및 block 범위를 이미 구현했습니다. 다른 여러 기능이 프로토타입되었으며 JDK 9의 초기 릴리스에서 지원되는 ES6 기능 목록에 추가되어야 합니다. 여기에는 다음 항목이 포함됩니다. :

* Template strings
* `let`, `const`, and block scope
* Iterators and for..of loops
* `Map`, `Set`, `WeakMap`, and `WeakSet`
* Symbols
* Binary and octal literals

다른 기능은 부분적으로 프로토타입이 만들어졌으며 제한된 시간 안에 완성이 가능할 것 같습니다. 다음은 JDK 9 업데이트 릴리스에 포함될 후보입니다.

* Arrow functions
* Enhanced object literals
* Destructuring assignment
* Default, rest, and spread parameters
* Unicode
* Subclassable built-ins
* Promises
* Proxies
* Math, Number, String, and Object APIs
* Reflection API

나머지 기능은 더 복잡하며 구현하는 데 더 오래 걸릴 수 있습니다. JDK 9 업데이트 릴리스에 이들 중 일부를 포함하는 것이 가능할 수도 있지만 현재 향후 주요 JDK 릴리스를 대상으로 하고 있습니다. 이러한 기능은 다음과 같습니다.

* Classes
* Generators
* Modules
* Module loaders
* Tail calls

### JEP 294: Linux/s390x Port

JDK 9를 Linux/s390x로 포트합니다.

### JEP 295: Ahead-of-Time Compilation

가상 머신을 시작하기 전에 Java 클래스를 네이티브 코드로 컴파일하십시오.

#### Goals

* 최대 성능에 미치는 영향을 최소화하면서 소규모 및 대규모 Java 애플리케이션의 시작 시간을 개선합니다.
* 최종 사용자의 작업 흐름을 가능한 한 적게 변경하십시오.

### JEP 297: Unified arm32/arm64 Port

Oracle에서 제공한 arm32 및 arm64용 HotSpot의 통합 포트를 JDK에 통합합니다.

### JEP 298: Remove Demos and Samples

오래되고 유지 관리되지 않는 데모와 샘플을 제거하십시오.

#### Description

몇 가지 데모가 테스트에 사용되므로 jdk 저장소의 테스트 계층 구조에서 적절한 위치로 이동합니다.

* `demo/share/applets`
* `demo/share/java2d`
* `demo/share/jfc`

나머지 데모 및 샘플은 jdk 저장소에서 제거됩니다.

* `demo/share/jvmti`
* `demo/share/management`
* `demo/share/nbproject`
* `demo/share/scripting`
* `demo/solaris/jni`
* `sample/share/annotations`
* `sample/share/forkjoin`
* `sample/share/jmx`
* `sample/share/lambda`
* `sample/share/nio`
* `sample/share/scripting`
* `sample/share/try-with-resources`
* `sample/share/vm`
* `sample/solaris/dtrace`

해당하는 makefile 변경이 이루어집니다. 빌드된 JDK 이미지에는 더 이상 데모 또는 샘플 디렉토리가 포함되지 않습니다.

### JEP 299: Reorganize Documentation

소스 저장소와 생성된 문서 모두에서 JDK의 문서 구성을 업데이트하십시오.

#### Goals

* API 사양, "man page"(도구 사양으로 간주될 수 있음) 및 기타 JDK 사양을 포함하도록 생성된 "docs" 이미지의 조직을 공식적으로 정의합니다.
* `javadoc` 도구에 의해 생성된 현재 20개 이상의 문서 세트를 JDK 이미지에 대한 API 사양의 단일 컬렉션으로 통합합니다.
* 소스 코드와 함께 필요에 따라 업데이트할 수 있고 생성된 "문서" 이미지에 쉽게 포함될 수 있도록 소스 리포지토리에 비API 사양에 대한 조직을 정의합니다.