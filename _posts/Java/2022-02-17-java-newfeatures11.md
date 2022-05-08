---
title:  "Java 11 New Features"
excerpt: "Java 11 New Features"
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

새로운 LTS 버전인 JDK 11가 2018년 9월 25일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 11](https://openjdk.java.net/projects/jdk/11/)를 참고했습니다.

## Features

### JEP 181: Nest-Based Access Control

Java 프로그래밍 언어의 기존 중첩 유형 개념과 일치하는 액세스 제어 컨텍스트인 중첩을 도입합니다. 중첩을 사용하면 논리적으로 동일한 코드 엔터티의 일부이지만 별개의 클래스 파일로 컴파일되는 클래스가 컴파일러가 접근성 확장 브리지 메서드를 삽입할 필요 없이 서로의 개인 멤버에 액세스할 수 있습니다.

### JEP 309: Dynamic Class-File Constants

새로운 상수 풀 형식인 `CONSTANT_Dynamic`을 지원하도록 Java 클래스 파일 형식을 확장합니다. `CONSTANT_Dynamic`을 로드하면 `invokedynamic` 호출 사이트를 연결하면 부트스트랩 메서드에 연결이 위임되는 것처럼 생성이 부트스트랩 메서드에 위임됩니다.

#### GOals

우리는 새로운 형태의 구체화 가능한 클래스 파일 상수를 생성하는 비용과 중단을 줄이기 위해 노력하고 있으며, 이는 결국 언어 디자이너와 컴파일러 구현자에게 표현성과 성능을 위한 더 넓은 옵션을 제공합니다. 정적 인수가 있는 부트스트랩 메서드의 형태로 사용자 제공 동작으로 매개변수화할 수 있는 새로운 단일 상수 풀 형식을 생성하여 이를 수행합니다.

또한 `invokedynamic`이 사용하는 부트스트랩 API를 동적 상수에도 적용할 수 있도록 JVM과 부트스트랩 메서드 간의 링크 시간 핸드셰이크를 조정합니다.

`invokedynamic`에 대한 경험을 바탕으로 `invokedynamic` 및 `dynamic` 상수의 부트스트랩 핸드셰이크를 조정하여 부트스트랩 메서드에 대한 인수 목록 처리에 대한 특정 제한을 완화합니다.

이 작업에는 몇 가지 종류의 상수 유형, 특히 변수 핸들([JEP 193](https://openjdk.java.net/jeps/193))의 대표적인 샘플에 대한 JDK 라이브러리 지원의 일부 프로토타입이 필요합니다. 이러한 프로토타입 제작을 지원하기 위해 이 작업은 상수 표현식([JEP 303](https://openjdk.java.net/jeps/303))에 대한 기본 언어 지원에 대한 다른 작업과 조정됩니다.

### JEP 315: Improve Aarch64 Intrinsics

기존 문자열 및 배열 내장 함수를 개선하고 AArch64 프로세서에서 `java.lang.Math sin`, `cos` 및 `log` 함수에 대한 새 내장 함수를 구현합니다.

#### Description

`Intrinsics`는 성능을 향상시키기 위해 주어진 메소드에 대해 일반 Java 코드 대신 실행되는 CPU 아키텍처별 어셈블리 코드를 활용하는 데 사용됩니다. 대부분의 내장 함수는 이미 AArch64 포트에 구현되어 있지만 다음 `java.lang.Math` 메서드에 대해 최적화된 내장 함수는 여전히 누락되어 있습니다.

* `sin` (sine trigonometric function)
* `cos` (cosine trigonometric function)
* `log` (logarithm of a number)

이 JEP는 이러한 메서드에 대해 최적화된 내장 기능을 구현하여 이러한 격차를 해소하기 위한 것입니다.

동시에 대부분의 내장 함수는 이미 AArch64 포트에 구현되어 있지만 일부 내장 함수의 현재 구현은 최적이 아닐 수 있습니다. 특히, AArch64 아키텍처의 일부 내장 함수는 소프트웨어 프리페칭 명령어, 메모리 주소 정렬, 다중 파이프라인 CPU에 대한 명령어 배치, 특정 명령어 패턴을 더 빠른 패턴 또는 SIMD 명령어로 교체함으로써 이점을 얻을 수 있습니다.

여기에는 `String::compareTo`, `String::indexOf`, `StringCoding::hasNegatives`, `Arrays::equals`, `StringUTF16::compress`, `StringLatin1::inflate` 및 다양한 체크섬 계산과 같은 일반적인 작업이 포함되지만 이에 국한되지 않습니다.

내장 알고리즘, 가장 일반적인 내장 사용 사례 및 CPU 사양에 따라 다음 변경 사항을 고려할 수 있습니다.

* ARM NEON 명령어 세트를 사용합니다. 이러한 코드(만들어질 경우)는 기존 알고리즘에 NEON이 아닌 버전이 있는 경우 플래그(예: `UseSIMDForMemoryOps`) 아래에 배치됩니다.
* PRFM(프리페치 힌트 명령어)을 사용합니다. 이 명령의 효과는 CPU 하드웨어 프리페처 및 해당 기능, CPU/메모리 클록 비율, 메모리 컨트롤러 사양 및 특정 알고리즘 요구 사항과 같은 다양한 요인에 따라 달라집니다.
* 명령을 재정렬하고 데이터 종속성을 줄여 가능한 경우 비순차적 실행을 허용합니다.
* 필요한 경우 정렬되지 않은 메모리 액세스를 피하십시오. 일부 CPU 구현은 16바이트 경계, dcache-line 경계에 걸쳐 로드/저장 명령을 실행할 때 페널티를 부과하거나 다른 로드/저장 명령에 대해 서로 다른 최적 정렬을 갖습니다(예: Cortex A53 가이드 참조). 정렬된 내장 버전이 정렬 독립 CPU에서 코드 실행 속도를 늦추지 않는 경우 코드 복잡성을 크게 증가시키지 않는 한 약간의 불이익이 있는 CPU를 돕기 위해 주소 정렬을 개선하는 것이 도움이 될 수 있습니다.

### JEP 318: Epsilon: A No-Op Garbage Collector

메모리 할당을 처리하지만 실제 메모리 회수 메커니즘을 구현하지 않는 GC를 개발하십시오. 사용 가능한 Java 힙이 소진되면 JVM이 종료됩니다.

#### Goals

메모리 풋프린트와 메모리 처리량을 희생하면서 제한된 할당 제한과 가장 낮은 대기 시간 오버헤드로 완전히 수동적인 GC 구현을 제공합니다. 성공적인 구현은 격리된 코드 변경이며 다른 GC를 건드리지 않으며 나머지 JVM에서 최소한의 변경을 수행합니다.

#### Description

Epsilon GC는 `-XX:+UseEpsilonGC`로 활성화된 다른 OpenJDK GC처럼 보이고 느껴집니다.

Epsilon GC는 할당된 메모리의 단일 연속 청크에서 선형 할당을 구현하여 작동합니다. 이를 통해 GC에서 간단한 잠금 없는 TLAB(스레드 로컬 할당 버퍼) 발급 코드를 허용하고 기존 VM 코드에서 처리하는 잠금 없는 TLAB 내 할당을 재사용할 수 있습니다. TLAB를 발행하는 것은 또한 실제로 할당된 것에 의해 경계를 이루는 프로세스가 취한 상주 메모리를 유지하는 데 도움이 됩니다. 거대한/TLAB 외부 할당은 이 체계에서 TLAB 할당과 큰 개체 할당 사이에 차이가 거의 없기 때문에 동일한 코드로 처리됩니다.

Epsilon에서 사용하는 장벽 세트는 완전히 비어 있거나 작동하지 않습니다. GC는 GC 주기를 수행하지 않으므로 개체 그래프, 개체 표시, 개체 복사 등에 신경을 쓰지 않기 때문입니다. 새로운 장벽 집합 구현을 도입하는 것은 다음과 같습니다. 이 구현에서 가장 파괴적인 JVM 변경이 될 수 있습니다.

Epsilon에 대한 런타임 인터페이스의 유일한 중요한 부분은 TLAB를 발행하는 것이므로 대기 시간은 발행된 TLAB 크기에 크게 좌우됩니다. 임의로 큰 TLAB와 임의로 큰 힙을 사용하면 대기 시간 오버헤드를 임의로 낮은 양수 값으로 설명할 수 있으므로 이름이 지정됩니다.

Java 힙이 소진되면 할당이 불가능하고 메모리 회수가 불가능하므로 실패해야 합니다. 그 시점에서 몇 가지 옵션이 있습니다. 대부분은 기존 GC가 하는 일과 일치합니다.

* 설명 메시지와 함께 OutOfMemoryError를 발생시킵니다.
* 힙 덤프 수행(평소와 같이 `-XX:+HeapDumpOnOutOfMemoryError`로 활성화됨)
* JVM을 강제로 실패시키고 선택적으로 외부 조치(일반적인 `-XX:OnOutOfMemoryError=...`를 통해)를 수행합니다. 예를 들어 디버거를 시작하거나 외부 모니터링 시스템에 실패에 대해 알립니다.

메모리 회수 코드가 구현되지 않았기 때문에 `System.gc()` 호출에서 수행할 작업이 없습니다. 구현은 GC를 강제하려는 시도가 무의미하다고 사용자에게 경고할 수 있습니다.

프로토타입 실행은 작은 워크로드에서 살아남고 더 큰 워크로드에서 예측 가능한 실패를 통해 개념을 증명합니다. 프로토타입 구현 및 일부 테스트는 샌드박스 저장소에서 찾을 수 있습니다.

```bash
$ hg clone http://hg.openjdk.java.net/jdk/sandbox sandbox 
$ hg up -r epsilon-gc-branch
$ sh ./configure 
$ make images
```

다음을 사용하여 기준선과 패치된 런타임 간의 차이를 볼 수 있습니다.

```bash
$ hg diff -r default:epsilon-gc-branch
```

자동 생성된 webrev: https://builds.shipilev.net/patch-openjdk-epsilon-jdk/

샘플 바이너리 빌드: https://builds.shipilev.net/openjdk-epsilon-jdk/ 

Docker에서:

```bash
$ docker pull shipilev/openjdk-epsilon
$ docker run -it --rm shipilev/openjdk-epsilon java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -Xlog:gc -version
[0.006s][info][gc] Initialized with 2009M heap, resizeable to up to 30718M heap with 128M steps
[0.006s][info][gc] Using TLAB allocation; min: 2K, max: 4096K
[0.006s][info][gc] Using Epsilon GC
openjdk version "11-internal" 2018-03-20
OpenJDK Runtime Environment (build 11-internal+0-nightly-sobornost-builds.shipilev.net-epsilon-jdkX-b32)
OpenJDK 64-Bit Server VM (build 11-internal+0-nightly-sobornost-builds.shipilev.net-epsilon-jdkX-b32, mixed mode)
[0.071s][info][gc] Total allocated: 899 KB
[0.071s][info][gc] Average allocation rate: 12600 KB/sec
```

### JEP 320: Remove the Java EE and CORBA Modules

Java SE 플랫폼 및 JDK에서 Java EE 및 CORBA 모듈을 제거합니다. 이러한 모듈은 향후 릴리스에서 제거할 의도가 선언된 Java SE 9에서 더 이상 사용되지 않습니다.

#### Description

Java SE 9에서 Java EE 및 CORBA 기술을 포함하는 Java SE 모듈은 제거를 위해 더 이상 사용되지 않는 것으로 주석이 지정되어 향후 릴리스에서 제거할 의도를 나타냅니다.

* `java.xml.ws` (JAX-WS, plus the related technologies SAAJ and Web Services Metadata)
* `java.xml.bind` (JAXB)
* `java.activation` (JAF)
* `java.xml.ws.annotation` (Common Annotations)
* `java.corba` (CORBA)
* `java.transaction` (JTA)

Java SE 9의 관련 모듈도 제거를 위해 더 이상 사용되지 않습니다.

* `java.se.ee` (Aggregator module for the six modules above)
* `jdk.xml.ws` (Tools for JAX-WS)
* `jdk.xml.bind` (Tools for JAXB)

제거를 위해 모듈을 더 이상 사용하지 않으면 컴파일 시간 경고가 발생하기 때문에 JDK 9는 개발자가 향후 릴리스에서 이러한 모듈을 실제로 제거할 수 있도록 준비하는 보다 강력한 단계를 수행했습니다. 클래스 경로의 코드가 컴파일될 때 모듈은 JDK 9에서 해결되지 않습니다. 또는 실행. 이를 통해 JDK 9의 개발자는 JDK 8과 마찬가지로 클래스 경로에 독립 실행형 버전의 Java EE 및 CORBA 기술을 배포할 수 있습니다. 또는 JDK 9의 개발자는 명령줄에서 `--add-modules` 플래그를 사용하여 문제를 해결할 수 있습니다. JDK 런타임 이미지의 모듈.

이 JEP는 위에 나열된 9개의 모듈을 제거합니다.

* 해당 소스 코드는 OpenJDK 저장소에서 삭제됩니다.
* 해당 클래스는 JDK 런타임 이미지에 존재하지 않습니다.
* 도구는 더 이상 사용할 수 없습니다.
  * `wsgen` 및 `wsimport`(`jdk.xml.ws`에서)
  * `schemagen` 및 `xjc`(`jdk.xml.bind`에서)
  * `idlj`, `orbd`, `servertool` 및 tnamesrv(`java.corba`에서)
* JNDI CosNaming 공급자(`java.corba`에서)는 더 이상 사용할 수 없습니다.
* `--add-modules`가 JDK 9에서 수행하는 것처럼 명령줄 플래그는 이를 활성화할 수 없습니다.

`rmic` 컴파일러는 `-idl` 및 `-iiop` 옵션을 제거하도록 업데이트됩니다. 결과적으로, `rmic`은 더 이상 IDL 또는 IIOP 스텁 및 연결 클래스를 생성할 수 없습니다.

JDK 문서 및 매뉴얼 페이지는 이러한 모듈 및 도구에 대한 참조를 제거하고 `rmic` 변경 사항을 나타내기 위해 업데이트됩니다.

### JEP 321: HTTP Client (Standard)

[JEP 110](https://openjdk.java.net/jeps/110)을 통해 JDK 9에 도입되고 JDK 10에서 업데이트된 배양된 HTTP 클라이언트 API를 표준화합니다.

#### Goals

[JEP 110](https://openjdk.java.net/jeps/110)의 목표 외에도 이 JEP는 다음을 수행합니다.

* 인큐베이션된 API에 대한 피드백을 고려
* 인큐베이션된 API를 기반으로 `java.net.http` 패키지에 표준화된 API를 제공
* 배양된 API를 제거

#### Description

이 JEP는 JDK 9에서 인큐베이팅 API로 도입되고 JDK 10에서 업데이트된 HTTP 클라이언트 API를 표준화할 것을 제안합니다. 인큐베이팅 API는 상당한 개선을 가져온 여러 라운드의 피드백을 받았지만 높은 수준에서는 여전히 남아 있습니다. 대체로 동일합니다. API는 종속 작업을 트리거하도록 연결될 수 있는 `CompletableFutures`를 통해 비차단 요청 및 응답 의미 체계를 제공합니다. 요청 및 응답 본문의 역압 및 흐름 제어는 `java.util.concurrent.Flow` API에서 플랫폼의 반응 스트림 지원을 통해 제공됩니다.

JDK 9 및 JDK 10에서 배양하는 동안 구현이 거의 완전히 다시 작성되었습니다. 구현은 이제 완전히 비동기식입니다(이전 HTTP/1.1 구현은 차단됨). RX Flow 개념의 사용이 구현에 포함되어 HTTP/2를 지원하는 데 필요한 원래 사용자 정의 개념의 많은 부분이 제거되었습니다. 이제 사용자 수준 요청 게시자 및 응답 구독자에서 기본 소켓에 이르기까지 데이터 흐름을 보다 쉽게 추적할 수 있습니다. 이는 코드의 개념 수와 복잡성을 크게 줄이고 HTTP/1.1과 HTTP/2 간의 재사용 가능성을 최대화합니다.

표준 API의 모듈 이름과 패키지 이름은 `java.net.http`가 됩니다.

##### Changes over what was incubated in JDK 10

JDK 10에대한 변경 사항

1. 정적 팩토리 메소드를 통해 생성된 `BodyPublisher`, `BodyHandler` 및 `BodySubscriber`의 미리 정의된 구현은 복수화된 명명 규칙에 따라 별도의 인스턴스화할 수 없는 유틸리티 팩토리 클래스로 이동되었습니다. 이렇게 하면 상대적으로 작은 인터페이스의 가독성이 향상됩니다.
2. 정적 팩토리 메서드의 이름도 다음과 같은 광범위한 범주에 따라 업데이트되었습니다.
* `fromXxx`: 표준 가입자의 어댑터, 예: `Flow.Subscriber`는 `BodySubscriber`를 반환합니다.
* `ofXxx`: 응답 본문을 문자열로 처리하거나 본문을 파일로 스트리밍하는 것과 같은 유용한 일반 작업을 수행하는 미리 정의된 새 `Body[Publisher|HAndler|Subscriber]`을 만드는 팩토리입니다.
* `other`: `Combinator`(`BodySubscriber`가 `BodySubscriber`를 반환함) 및 기타 유용한 작업.
3. 일반적인 시나리오에서 사용성을 개선하기 위해 몇 가지 `BodyHandler` 및 해당 `BodySubscriber`가 추가되었습니다.
* `discard(Object replacement)` 결합된 응답 본문 폐기/무시 및 주어진 교체 허용. 피드백에 따르면 이것이 혼란스러워 보일 수 있습니다. 제거되고 두 개의 별도 처리기로 대체되었습니다. 1) `discarding()` 및 2) `replacing(Object replacement)`.
* `BodyHandler<Stream<String>>`을 반환하는 `ofLines()`를 추가하여 응답 본문의 스트리밍을 라인 단위로 스트림으로 지원합니다. `BufferedReader.lines()`와 유사한 의미 체계를 제공합니다.
* 문자열 라인의 `Flow.Subscriber`에 대한 응답 본문의 적응을 지원하는 `fromLineSubscriber` 가 추가되었습니다.
* 한 응답 본문 유형에서 다른 응답 본문 유형으로의 범용 매핑을 위해 `BodySubscriber.mapping`을 추가했습니다.
4. 푸시 약속 지원은 API에 대한 영향을 줄이고 일반 요청/응답과 더 일치하도록 재작업되었습니다. 특히 `MultiSubscriber` 및 `MultiResultMap`이 제거되었습니다. 푸시 약속은 이제 보내기 작업 중에 선택적으로 제공되는 기능 인터페이스인 `PushPromiseHandler`를 통해 처리됩니다.
5. `SAME_PROTOCOL` 및 `SECURE` 정책을 `NORMAL`로 대체하여 `HttpClient.Redirect` 정책이 단순화되었습니다. 이전에 명명된 SECURE는 실제로 적절하게 명명되지 않았으며 대부분의 일반적인 경우에 적합할 가능성이 있으므로 `NORMAL`로 이름을 변경해야 합니다. 위에서 언급한 새로 명명된 `NORMAL`을 감안할 때 `SAME_PROTOCOL`은 이름이 이상하고 혼동될 수 있으며 사용되지 않을 가능성이 높습니다.
6. `WebSocket.MessagePart`가 제거되었습니다. 이 열거형은 메시지 전달이 완료되었는지 여부를 나타내기 위해 수신 측에서 사용되었습니다. 이 목적을 위해 단순 부울을 사용하는 송신 측과 비대칭입니다. 또한 간단한 부울로 수신된 메시지를 처리하면 수신 코드 논리가 크게 줄어들고 단순화됩니다. 위에서 언급한 `MessagePart`의 이점이자 주요 목적 중 하나인 WHOLE로 전달되는 메시지의 결정은 자체 무게를 지탱하지 않는 것으로 판명되었습니다.

API에 대한 자세한 내용은 [JEP 110](https://openjdk.java.net/jeps/110), 최신 API `javadoc` 또는 네트워킹 그룹의 JDK HTTP 클라이언트 페이지에서 찾을 수 있습니다.

### JEP 323: Local-Variable Syntax for Lambda Parameters

암시적으로 형식이 지정된 람다 식의 형식 매개 변수를 선언할 때 `var`를 사용할 수 있습니다.

#### Goals

암시적으로 형식이 지정된 람다 식의 형식 매개 변수 선언 구문을 지역 변수 선언 구문에 맞춥니다.

#### Description

암시적으로 형식이 지정된 람다 식의 형식 매개변수의 경우 예약된 형식 이름 `var`를 사용하도록 허용하여 다음을 수행합니다.

```java
(var x, var y) -> x.process(y)
```

이는 아래와 같습니다.

```java
(x, y) -> x.process(y)
```

암시적으로 형식이 지정된 람다 식은 모든 형식 매개변수에 대해 `var`를 사용하거나 아무 매개변수에도 사용하지 않아야 합니다. 또한 `var`는 암시적으로 형식이 지정된 람다 식의 형식 매개변수에만 허용됩니다. `--- explicitly` 으로 형식이 지정된 람다 식은 모든 형식 매개변수에 대해 매니페스트 형식을 계속 지정하므로 일부 형식 매개변수에는 매니페스트 형식이 있는 반면 다른 형식 매개변수는 다음을 사용하는 것이 허용되지 않습니다. 변수 다음 예는 불법입니다.

```java
(var x, y) -> x.process(y)         // Cannot mix 'var' and 'no var' in implicitly typed lambda expression
(var x, int y) -> x.process(y)     // Cannot mix 'var' and manifest types in explicitly typed lambda expression
```

이론적으로 위의 마지막 줄과 같은 람다 식을 가질 수 있습니다. 이 표현식은 반명시적으로 입력됩니다(또는 관점에 따라 반암시적으로 입력됨). 그러나 형식 유추 및 과부하 해결에 큰 영향을 미치기 때문에 이 JEP의 범위를 벗어납니다. 이것이 람다 표현식이 모든 매니페스트 매개변수 유형을 지정하거나 지정하지 않아야 한다는 제한을 유지하는 주된 이유입니다. 또한 암시적으로 형식이 지정된 람다 식의 매개 변수에 대해 유추된 형식이 `var` 사용 여부에 관계없이 동일하도록 강제하고 싶습니다. 우리는 미래의 JEP에서 부분 추론의 문제로 돌아갈 수 있습니다. 또한 우리는 약식 구문의 간결함을 손상시키고 싶지 않으므로 다음과 같은 표현을 허용하지 않습니다.

```java
var x -> x.foo()
```

### JEP 324: Key Agreement with Curve25519 and Curve448

RFC 7748에 설명된 대로 Curve25519 및 Curve448을 사용하여 주요 을 구현합니다.

#### Goals

RFC 7748은 기존 ECDH(Elliptic Curve Diffie-Hellman) 방식보다 더 효율적이고 안전한 핵심 합의 방식을 정의합니다. 이 JEP의 주요 목표는 API와 이 표준을 구현하는 것입니다. 추가 구현 목표는 다음과 같습니다.

1. 동일한 보안 강도에서 기존 ECC(네이티브 C) 코드보다 더 나은 성능으로 플랫폼 독립적인 전체 Java 구현을 개발합니다.
2. 플랫폼이 일정한 시간에 64비트 정수 덧셈/곱셈을 수행한다고 가정할 때 타이밍이 비밀과 무관한지 확인합니다. 또한 구현은 비밀에 대해 분기하지 않습니다. 이러한 속성은 부채널 공격을 방지하는 데 유용합니다.

#### Description

X25519 및 X448 기능은 RFC 7748에 설명된 대로 구현되며 이러한 기능은 기존 SunEC 공급자에서 새로운 `KeyAgreement`, `KeyFactory` 및 `KeyPairGenerator` 서비스를 구현하는 데 사용됩니다. 구현에서는 부채널 공격을 방지하기 위해 RFC 7748에 설명된 일정 시간 몽고메리 래더 방법을 사용합니다. 구현은 RFC에 설명된 대로 결과를 0과 비교하여 기여 동작을 보장합니다.

새로운 모듈식 산술 라이브러리를 사용하여 큰 수의 산술을 수행합니다. 이 라이브러리는 `BigInteger`에 비해 두 가지 중요한 이점이 있습니다.

1. 대부분의 작업은 일정한 시간에 수행됩니다. 일부 연산은 해당 피연산자가 관련 알고리즘에서 비밀이 아닌 경우 피연산자의 크기에 따라 달라질 수 있습니다. 예를 들어, 지수의 타이밍은 지수의 크기에 따라 다르지만 지수 값은 RFC 7748에서 비밀이 아닙니다. 이 라이브러리의 API 문서는 각 연산의 타이밍 동작을 설명합니다.
2. 캐리 작업을 피하고 EC 작업에 사용되는 특정 유한 필드의 속성을 활용하여 성능이 향상됩니다.

이 새 라이브러리는 내부 JDK 패키지에 있으며 새 암호화 알고리즘에서만 사용됩니다. 가까운 장래에 EdDSA(Curve25519 및 Curve448을 사용하는 서명) 및 Poly1305(메시지 인증) 구현에서 이를 사용할 것으로 예상합니다. 라이브러리는 EdDSA 논문에서 영감을 받은 축소된 기수 표현을 사용합니다.

산술은 캐리 연산을 피하기 때문에 버그가 있거나 잘못 사용되면 오버플로되어 잘못된 결과를 생성할 수 있습니다. 예를 들어, 덧셈 연산은 수행되지 않으므로 각 곱셈 연산 전에 제한된 수(일반적으로 하나)의 덧셈 연산을 수행할 수 있습니다. 라이브러리는 오용에 대한 방어를 포함하며(예: 너무 많은 추가가 발생하면 예외 발생) 오버플로가 발생하지 않도록 주의 깊게 테스트해야 합니다.

##### API

RFC 7748용 JCA API는 "XDH"라는 이름을 사용하여 이 메커니즘과 관련된 모든 서비스(`KeyAgreement`, `KeyPairGenerator`, `KeyFactory` 등)를 식별합니다. 알고리즘 이름 "X25519" 및 "X448"도 Curve25519 및 Curve448을 사용하여 각각 XDH를 의미하도록 정의됩니다. 이렇게 하면 원하는 곡선을 지원하는 공급자를 더 쉽게 찾을 수 있는 편리한 약어(예: `KeyPairGenerator.getInstance("X448")` )가 허용됩니다. "X25519" 및 "X448"과 같은 이름은 단순히 "XDH"의 별칭이 아니어야 합니다. 이러한 이름에 대해 반환된 서비스는 올바른 곡선으로 초기화되어야 하며 다른 곡선을 사용하는 키를 거부할 수 있습니다.

`AlgorithmParameterSpec`: NamedParameterSpec이라는 새 클래스가 사용되는 곡선(X25519 또는 X448)을 지정하는 데 사용됩니다. 이 클래스는 매개변수 세트를 지정하기 위해 단일 표준 이름을 사용하며, 이름이 지정된 매개변수를 사용하는 다른 알고리즘에서 재사용하기 위한 것입니다. 예를 들어, (유한 필드) Diffie-Hellman의 명명된 그룹에 사용할 수 있습니다. `NamedParameterSpec`은 `ECGenParameterSpec` 위의 클래스 계층에 삽입되어 `ECGenParameterSpec`도 `NamedParameterSpec`이 됩니다.

KeySpec: 새로운 클래스 `XECPublicKeySpec`을 사용하여 공개 키를 지정할 수 있습니다. 이 클래스에는 점의 `u` 좌표를 보유하는 `BigInteger` 멤버가 있습니다. 새 클래스 `XECPrivateKeySpec`을 사용하여 개인 키를 지정할 수 있습니다. 이 클래스에는 RFC 7748에 설명된 X25519 및 X448 함수에 대한 (인코딩된) `k` 입력을 보유하는 바이트 배열 구성원이 있습니다. 이러한 두 KeySpec 클래스에는 곡선 및 기타 알고리즘 매개변수를 지정하는 `AlgorithmParameterSpec` 구성원이 있습니다.

기존 `X509EncodedKeySpec` 클래스는 공개 키에도 사용할 수 있습니다. 기존 `PKCS8EncodedKeySpec` 클래스는 개인 키에도 사용할 수 있습니다.

키 인터페이스: 새로운 인터페이스 `XECPublicKey` 및 `XECPrivateKey`가 추가되어 키 개체에 포함된 정보에 대한 액세스를 제공합니다. 이러한 인터페이스의 키 데이터 표현은 `XECPublicKeySpec` 및 `XECPrivateKeySpec`의 표현과 동일합니다. 두 인터페이스 모두 곡선 및 기타 알고리즘 매개변수를 정의하는 `AlgorithmParameterSpec`에 대한 액세스를 제공하는 새로운 인터페이스 `XECKey에`서 확장됩니다.

```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("XDH");
NamedParameterSpec paramSpec = new NamedParameterSpec("X25519");
kpg.initialize(paramSpec); // equivalent to kpg.initialize(255)
// alternatively: kpg = KeyPairGenerator.getInstance("X25519")
KeyPair kp = kpg.generateKeyPair();

KeyFactory kf = KeyFactory.getInstance("XDH");
BigInteger u = ...
XECPublicKeySpec pubSpec = new XECPublicKeySpec(paramSpec, u);
PublicKey pubKey = kf.generatePublic(pubSpec);

KeyAgreement ka = KeyAgreement.getInstance("XDH");
ka.init(kp.getPrivate());
ka.doPhase(pubKey, true);
byte[] secret = ka.generateSecret();
```

### JEP 327: Unicode 10

유니코드 표준 버전 10.0을 지원하도록 기존 플랫폼 API를 업그레이드합니다.

#### Description

주로 다음 클래스에서 최신 버전의 유니코드를 지원합니다.

* `java.lang` 패키지의 문자 및 문자열
* `java.awt.font` 패키지의 `NumericShaper`
* `java.text` 패키지의 `Bidi`, `BreakIterator` 및 `Normalizer`

### JEP 328: Flight Recorder

Java 애플리케이션 및 HotSpot JVM 문제 해결을 위한 오버헤드가 낮은 데이터 수집 프레임워크를 제공합니다.

#### Goals

* 데이터를 이벤트로 생성하고 소비하기 위한 API 제공
* 버퍼 메커니즘 및 바이너리 데이터 형식 제공
* 이벤트 구성 및 필터링 허용
* OS, HotSpot JVM 및 JDK 라이브러리에 대한 이벤트 제공

#### Description

[JEP 167](https://openjdk.java.net/jeps/167): 이벤트 기반 JVM 추적은 HotSpot JVM에 초기 이벤트 세트를 추가했습니다. Flight Recorder는 이벤트 생성 기능을 Java로 확장합니다.

[JEP 167](https://openjdk.java.net/jeps/167)은 또한 이벤트의 데이터가 stdout에 인쇄되는 기본적인 백엔드를 추가했습니다. Flight Recorder는 이벤트를 바이너리 형식으로 작성하기 위한 단일 고성능 백엔드를 제공합니다.

Modules:

* `jdk.jfr`
  * API 및 내부
  * `java.base`만 필요(리소스가 제한된 장치에 적합)
* `jdk.management.jfr`
  * JMX 기능
  * `jdk.jfr` 및 `jdk.management` 필요

Flight Recorder는 커맨드라인에서 시작할 수 있습니다.

```bash
$ java -XX:StartFlightRecording ...
```

bin/jcmd 도구를 사용하여 녹음을 시작하고 제어할 수도 있습니다.

```bash
$ jcmd <pid> JFR.start
$ jcmd <pid> JFR.dump filename=recording.jfr
$ jcmd <pid> JFR.stop
```

이 기능은 JMX를 통해 원격으로 제공되며 Mission Control과 같은 도구에 유용합니다.

##### Producing and consuming events

사용자가 자신의 이벤트를 생성할 수 있는 API가 있습니다.

```java
import jdk.jfr.*;

@Label("Hello World")
@Description("Helps the programmer getting started")
class HelloWorld extends Event {
   @Label("Message")
   String message;
}

public static void main(String... args) throws IOException {
    HelloWorld event = new HelloWorld();
    event.message = "hello, world!";
    event.commit();
}
```

`jdk.jfr.consumer`에서 사용 가능한 클래스를 사용하여 녹음 파일에서 데이터를 추출할 수 있습니다.

```java
import java.nio.file.*;
import jdk.jfr.consumer.*;

Path p = Paths.get("recording.jfr");
for (RecordedEvent e : RecordingFile.readAllEvents(p)) {
   System.out.println(e.getStartTime() + " : " + e.getValue("message"));
}
```

##### Buffer mechanism and binary data format

스레드는 스레드 로컬 버퍼에 잠금이 없는 이벤트를 씁니다. 스레드 로컬 버퍼가 가득 차면 가장 최근의 이벤트 데이터를 유지 관리하는 전역 메모리 내 순환 버퍼 시스템으로 승격됩니다. 구성에 따라 가장 오래된 데이터를 버리거나 디스크에 기록하여 이력을 계속 저장할 수 있습니다. 디스크의 이진 파일은 확장자가 `.jfr`이며 보존 정책을 사용하여 유지 관리 및 제어됩니다.

이벤트 모델은 리틀 엔디안 기반 128로 인코딩된 자체 설명 바이너리 형식으로 구현됩니다(파일 헤더 및 일부 추가 섹션 제외). 바이너리 데이터 형식은 변경될 수 있으므로 직접 사용해서는 안 됩니다. 대신 녹음 파일과 상호 작용할 수 있는 API가 제공됩니다.

예시적인 예로 클래스 로드 이벤트에는 발생한 시간을 설명하는 타임스탬프, 시간 범위를 설명하는 기간, 스레드, 스택 추적 및 세 가지 이벤트별 페이로드 필드, 로드된 클래스 및 관련 클래스 로더가 포함됩니다. 이벤트 크기는 총 24바이트입니다.

```
<memory address>: 98 80 80 00 87 02 95 ae e4 b2 92 03 a2 f7 ae 9a 94 02 02 01 8d 11 00 00
```

* Event size [98 80 80 00]
* Event ID [87 02]
* Timestamp [95 ae e4 b2 92 03]
* Duration [a2 f7 ae 9a 94 02]
* Thread ID [02]
* Stack trace ID [01]
* Payload [fields]
  * Loaded Class: [0x8d11]
  * Defining ClassLoader: [0]
  * Initiating ClassLoader: [0]

##### Configure and filter events

이벤트를 활성화, 비활성화 및 필터링하여 오버헤드와 스토리지에 필요한 공간을 줄일 수 있습니다. 다음 설정을 사용하여 수행할 수 있습니다.

* enabled - 이벤트가 기록되어야 함
* threshold - 이벤트가 기록되지 않는 기간
* stackTrace - `Event.commit()` 메서드의 스택 추적을 기록해야 하는 경우
* period - 이벤트가 발생하는 간격(주기적인 경우)

낮은 오버헤드의 즉시 사용 가능한 사용 사례에 대해 Flight Recorder를 구성하도록 조정된 두 가지 구성 세트가 있습니다. 사용자는 자신의 특정 이벤트 구성을 쉽게 만들 수 있습니다.

##### OS, JVM and JDK library events

다음 영역을 다루는 이벤트가 추가됩니다.

* OS
  * Memory, CPU Load 및 CPU Information, native libraries, process information
* JVM
  * Flags, GC configuration, compiler configuration
  * Method profiling event
  * Memory leak event
* JDK libraries
  * Socket IO, File IO, Exceptions and Errors, modules

### JEP 329: ChaCha20 and Poly1305 Cryptographic Algorithms

RFC 7539에 지정된 대로 ChaCha20 및 ChaCha20-Poly1305 암호를 구현합니다. ChaCha20은 이전의 안전하지 않은 RC4 스트림 암호를 대체할 수 있는 비교적 새로운 스트림 암호입니다.

#### Goals

* ChaCha20 및 ChaCha20-Poly1305 암호 구현을 제공합니다. 이러한 알고리즘은 SunJCE 제공자에서 구현됩니다.
* ChaCha20 및 ChaCha20-Poly1305 알고리즘에 적합한 키를 생성하는 KeyGenerator 구현을 제공합니다.
* ChaCha20-Poly1305 알고리즘과 함께 사용할 `AlgorithmParameters` 구현을 제공합니다.

#### Description

ChaCha20 및 ChaCha20-Poly1305 알고리즘은 SunJCE 제공자 내에서 `javax.crypto.CipherSpi` API를 구현합니다. 암호는 `Cipher.getInstance()` 메서드를 사용하여 다른 암호와 동일한 방식으로 인스턴스화됩니다. 두 암호 모두에 대해 두 가지 허용되는 변환이 허용됩니다. 단일 이름 변환은 인증 없는 단순 스트림 암호인 ChaCha20의 경우 `ChaCha20`이고 인증자로 Poly1305를 사용하는 AEAD 암호인 ChaCha20의 경우 `ChaCha20-Poly1305`입니다. `ChaCha20/None/NoPadding` 및 `ChaCha20-Poly1305/None/NoPadding`도 허용되는 변환 문자열이지만 `None` 및 `NoPadding` 외에 다른 모드 또는 패딩 값은 허용되지 않습니다. 다른 모드 또는 패딩 값을 사용하면 예외가 `throw`됩니다.

ChaCha20 암호의 초기화는 새로운 `AlgorithmParameterSpec` 구현인 `javax.crypto.spec.ChaCha20ParameterSpec`을 허용합니다.

```java
ChaCha20ParameterSpec(byte[] nonce, int counter);     // Constructor
public byte[] getNonce();     // Obtains a copy of the nonce value
public int getCounter();     // Obtains the initial counter value
```

nonce 값은 길이가 96비트(12바이트)여야 합니다. 다른 길이는 예외가 발생합니다. 정수 카운터 값은 부호 없는 32비트 값의 전체 범위를 허용하기 위해 모든 정수 값(심지어 음수)일 수 있습니다.

`ChaCha20ParameterSpec` 없이 이 알고리즘을 초기화하면 암호가 내부적으로 자체 12바이트 nonce를 생성하고 카운터 값을 1로 설정합니다. 카운터 바이트는 `Cipher.getIV()` 메서드를 호출하여 얻을 수 있습니다.

ChaCha20-Poly1305에 대한 초기화는 12바이트 nonce를 포함하는 현재 `javax.crypto.spec.IvParameterSpec` 클래스의 인스턴스를 제공하여 수행할 수 있습니다. `ChaCha20ParameterSpec`보다 `IvParameterSpec`을 사용하기로 결정하면 API 변경 없이 ChaCha20-Poly1305를 이전 릴리스로 백포트할 수 있습니다. `IvParameterSpec`은 보유하는 바이트에 대한 길이 요구 사항을 설정하지 않기 때문에 암호 개체 자체는 초기화 중에 12바이트 길이 요구 사항을 적용합니다.

ChaCha20과 마찬가지로 ChaCha20-Poly1305는 `IvParameterSpec` 없이 초기화될 수 있습니다. 이 경우 nonce는 무작위로 생성되고 `Cipher.getIV()`로 얻을 수 있습니다.

`init` 메소드를 통해 제공되는 키 객체는 `ChaCha20`의 알고리즘 유형을 가져야 합니다. 이를 지원하기 위해 새로운 `KeyGenerator` 구현이 생성됩니다. AES, RC2, ARCFOUR 및 HmacSHA2 제품군과 같은 다른 알고리즘에 대한 기존 `KeyGenerator` 구현과 마찬가지로 이 `KeyGenerator`는 `AlgorithmParameterSpec`으로 초기화되지 않을 수 있습니다. 조정 가능한 키 길이를 허용하는 `init` 메소드 형식이 호출되면 해당 매개변수를 256으로 설정해야 하며 그렇지 않으면 `InvalidParameterException`이 발생합니다.

ChaCha20 알고리즘의 사용은 다른 스트림 암호에 사용되는 기존 Cipher API를 따릅니다. 간단한 단일 부분 암호화는 다음과 같이 작성할 수 있습니다.

```java
// Get a Cipher instance and set up the parameters
// Assume SecretKey "key", 12-byte nonce "nonceBytes" and plaintext "pText"
// are coming from outside this code snippet
Cipher mambo = Cipher.getInstance("ChaCha20");
ChaCha20ParameterSpec mamboSpec
    = new ChaCha20ParameterSpec(nonceBytes, 7);   // Use a starting counter value of "7"
// Encrypt our input
mambo.init(Cipher.ENCRYPT_MODE, key, mamboSpec);
byte[] encryptedResult = mambo.doFinal(pText);
```

Poly1305 인증자를 사용하여 AEAD 모드에서 실행되는 ChaCha20의 경우 RFC 7539가 1에서 시작하는 데이터의 초기 카운터 값을 정의하기 때문에 nonce만 필요합니다. 이 Cipher 구현이 백포팅 가능하고 JSSE 제공자 내에서 사용을 용이하게 하기 위해, `javax.crypto.spec.IvParameterSpec`은 nonce를 제공하는 데 사용됩니다.

AEAD 모드에서 실행할 때 인증 태그 추가(암호화용) 또는 태그 소비 및 확인(복호화용)으로 인해 출력 크기가 입력과 다를 수 있습니다. 암호화/복호화 전에 출력 버퍼를 할당하려는 경우 `getOutputSize()` 메서드를 사용해야 합니다. 샘플 단일 부분 암호화는 다음과 같습니다.

```java
// Get a Cipher instance and set up the parameters
// Assume SecretKey "key", 12-byte nonce "nonceBytes" and plaintext "pText"
// are coming from outside this code snippet
Cipher mambo = Cipher.getInstance("ChaCha20-Poly1305");
AlgorithmParameterSpec mamboSpec = new IvParameterSpec(nonceBytes);

// Encrypt our input
mambo.init(Cipher.ENCRYPT_MODE, key, mamboSpec);
byte[] encryptedResult = new byte[mambo.getOutputSize(pText.length)];
mambo.doFinal(pText, 0, pText.length, encryptedResult);
```

ChaCha20 및 ChaCha20-Poly1305 암호 모두에 대한 중요한 요구 사항은 `doFinal()` 호출 다음에 현재 구성된 것과 다른 nonce를 제공하는 새로운 `init()` 호출이 이루어져야 한다는 것입니다. 이는 AES-GCM의 암호화 요구 사항과 유사하지만 이 두 암호의 경우 초기화 요구 사항은 암호화 및 암호 해독 작업 모두 후에 발생해야 합니다. 이전 `doFinal()` 이후에 `Cipher.update()`, `Cipher.updateAAD()` 또는 `Cipher.doFinal()`에 대한 후속 호출과 그 사이에 `init()` 호출이 없으면 `IllegalStateException`이 발생합니다.

### JEP 330: Launch Single-File Source-Code Programs

"shebang" 파일 및 관련 기술을 통해 스크립트 내에서 사용하는 것을 포함하여 Java 소스 코드의 단일 파일로 제공되는 프로그램을 실행하도록 Java 실행기를 향상시킵니다.

### JEP 331: Low-Overhead Heap Profiling

JVMTI를 통해 액세스할 수 있는 Java 힙 할당을 샘플링하는 오버헤드가 낮은 방법을 제공합니다.

#### Goals

다음과 같은 JVM에서 Java 객체 힙 할당에 대한 정보를 얻는 방법을 제공합니다.

* 기본적으로 지속적으로 활성화할 수 있을 만큼 오버헤드가 낮습니다.
* 잘 정의된 프로그래밍 방식의 인터페이스를 통해 액세스할 수 있습니다.
* 모든 할당을 샘플링할 수 있음(즉, 하나의 특정 힙 영역에 있거나 특정 방식으로 할당된 할당으로 제한되지 않음)
* 구현 독립적인 방식으로 정의할 수 있습니다(즉, 특정 GC 알고리즘 또는 VM 구현에 의존하지 않음).
* 라이브 및 데드 Java 개체에 대한 정보를 제공할 수 있습니다.

#### Description

##### New JVMTI event and method

여기서 제안하는 힙 샘플링 기능을 위한 사용자 대면 API는 힙 프로파일링을 허용하는 JVMTI 확장으로 구성됩니다. 다음 시스템은 다음과 같은 콜백을 제공하는 이벤트 알림 시스템에 의존합니다.

```java
void JNICALL
SampledObjectAlloc(jvmtiEnv *jvmti_env,
            JNIEnv* jni_env,
            jthread thread,
            jobject object,
            jclass object_klass,
            jlong size)
```

파라메터값은 다음과 같습니다.

* `thread`는 `jobject`를 할당하는 스레드
* `object`는 샘플링된 `jobject`에 대한 참조
* `object_klass`는 `jobject`의 클래스
* `size`는 할당의 크기

새 API에는 단일 새 JVMTI 메서드도 포함되어 있습니다.

```java
jvmtiError  SetHeapSamplingInterval(jvmtiEnv* env, jint sampling_interval)
```

여기서 `sampling_interval`은 샘플링 사이에 할당된 평균 바이트입니다. 방법의 사양은 다음과 같습니다.

0이 아니면 샘플링 간격이 업데이트되고 새로운 평균 샘플링 간격인 `sampling_interval` 바이트로 사용자에게 콜백을 보냅니다.
예를 들어 사용자가 메가바이트마다 샘플을 원하는 경우 샘플링 간격은 1024 * 1024가 됩니다.
메서드에 0이 전달되면 샘플러는 새 간격이 고려되면 모든 할당을 샘플링하며, 특정 수의 할당이 필요할 수 있습니다.
샘플링 간격은 정확하지 않습니다. 샘플이 발생할 때마다 다음 샘플이 선택되기 전의 바이트 수는 주어진 평균 간격으로 의사 난수입니다. 이는 샘플링 편향을 피하기 위한 것입니다. 예를 들어, 동일한 할당이 512KB마다 발생하는 경우 512KB 샘플링 간격은 항상 동일한 할당을 샘플링합니다. 따라서 샘플링 간격이 항상 선택된 간격은 아니지만 많은 수의 샘플 후에는 선택 간격으로 가는 경향이 있습니다.

##### Use-case example

이를 활성화하기 위해 사용자는 일반적인 이벤트 알림 호출을 사용하여 다음을 수행합니다.

```java
jvmti->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_SAMPLED_OBJECT_ALLOC, NULL)
```

할당이 초기화되고 올바르게 설정되면 이벤트가 전송되므로 실제 코드가 할당을 수행한 직후입니다. 기본적으로 평균 샘플링 간격은 512KB입니다.

샘플링 이벤트 시스템을 활성화하는 데 필요한 최소 요구 사항은 `JVMTI_ENABLE` 및 이벤트 유형 `JVMTI_EVENT_SAMPLED_OBJECT_ALLOC`로 `SetEventNotificationMode`를 호출하는 것입니다. 샘플링 간격을 수정하기 위해 사용자는 `SetHeapSamplingInterval` 메서드를 호출합니다.

시스템을 비활성화하려면

```java
jvmti->SetEventNotificationMode(jvmti, JVMTI_DISABLE, JVMTI_EVENT_SAMPLED_OBJECT_ALLOC, NULL)
```

이벤트 알림을 비활성화하고 샘플러를 자동으로 비활성화합니다.

`SetEventNotificationMode`를 통해 샘플러를 다시 호출하면 현재 설정된 샘플링 간격(기본적으로 512KB 또는 `SetHeapSamplingInterval`을 통해 사용자가 전달한 마지막 값)으로 샘플러를 다시 활성화합니다.

##### New capability

새 기능을 보호하고 VM 구현에 대해 선택 사항으로 만들기 위해 `can_generate_sampled_object_alloc_events`라는 새 기능이 `jvmtiCapabilities`에 도입되었습니다.

##### Global / thread level sampling

알림 시스템을 사용하면 특정 스레드에 대해서만 이벤트를 보내는 직접적인 수단을 제공합니다. 이것은 `SetEventNotificationMode`를 통해 수행되며 수정할 스레드와 함께 세 번째 매개변수를 제공합니다.

##### A full example

다음 섹션에서는 샘플러의 API를 설명하는 코드 조각을 제공합니다. 먼저 기능 및 이벤트 알림이 활성화됩니다.

```java
jvmtiEventCallbacks callbacks;
memset(&callbacks, 0, sizeof(callbacks));
callbacks.SampledObjectAlloc = &SampledObjectAlloc;

jvmtiCapabilities caps;
memset(&caps, 0, sizeof(caps));
caps.can_generate_sampled_object_alloc_events = 1;
if (JVMTI_ERROR_NONE != (*jvmti)->AddCapabilities(jvmti, &caps)) {
  return JNI_ERR;
}

if (JVMTI_ERROR_NONE != (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE,
                                       JVMTI_EVENT_SAMPLED_OBJECT_ALLOC, NULL)) {
  return JNI_ERR;
}

if (JVMTI_ERROR_NONE !=  (*jvmti)->SetEventCallbacks(jvmti, &callbacks, sizeof(jvmtiEventCallbacks)) {
  return JNI_ERR;
}

// Set the sampler to 1MB.
if (JVMTI_ERROR_NONE !=  (*jvmti)->SetHeapSamplingInterval(jvmti, 1024 * 1024)) {
  return JNI_ERR;
}
```

샘플러를 비활성화하려면(이벤트 및 샘플러 비활성화):

```java
if (JVMTI_ERROR_NONE != (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_DISABLE,
                                        JVMTI_EVENT_SAMPLED_OBJECT_ALLOC, NULL)) {
   반환 JNI_ERR;
}
```

1024 * 1024 바이트 샘플링 간격으로 샘플러를 다시 활성화하려면 이벤트 활성화를 위한 간단한 호출이 필요합니다.

```java
if (JVMTI_ERROR_NONE != (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE,
                                        JVMTI_EVENT_SAMPLED_OBJECT_ALLOC, NULL)) {
   반환 JNI_ERR;
}
```

##### User storage of sampled allocations

이벤트가 생성되면 콜백은 JVMTI `GetStackTrace` 메서드를 사용하여 스택 추적을 캡처할 수 있습니다. 콜백으로 얻은 `jobject` 참조는 JNI 약한 참조로 래핑되어 객체가 가비지 수집된 시기를 결정할 수도 있습니다. 이 접근 방식을 통해 사용자는 샘플링된 개체와 여전히 활성 상태로 간주되는 개체에 대한 데이터를 수집할 수 있으며 이는 작업의 동작을 이해하는 좋은 수단이 될 수 있습니다.

예를 들어 다음과 같이 할 수 있습니다.

```java
extern "C" JNIEXPORT void JNICALL SampledObjectAlloc(jvmtiEnv *env,
                                                     JNIEnv* jni,
                                                     jthread thread,
                                                     jobject object,
                                                     jclass klass,
                                                     jlong size) {
  jvmtiFrameInfo frames[32];
  jint frame_count;
  jvmtiError err;

  err = global_jvmti->GetStackTrace(NULL, 0, 32, frames, &frame_count);
  if (err == JVMTI_ERROR_NONE && frame_count >= 1) {
    jweak ref = jni->NewWeakGlobalRef(object);
    internal_storage.add(jni, ref, size, thread, frames, frame_count);
  }
}
```

여기서 `internal_storage`는 샘플링된 개체를 처리할 수 있는 데이터 구조입니다. 가비지 수집된 샘플 등을 정리해야 하는지 여부를 고려하세요. 해당 구현의 내부는 용도에 따라 다르며 이 JEP의 범위를 벗어납니다.

샘플링 간격은 프로파일링 오버헤드를 완화하는 수단으로 사용할 수 있습니다. 샘플링 간격이 512KB인 경우 오버헤드는 사용자가 기본적으로 시스템을 켜둔 상태로 둘 수 있을 만큼 충분히 낮아야 합니다.

### JEP 332: Transport Layer Security (TLS) 1.3

TLS(전송 계층 보안) 프로토콜 RFC 8446의 버전 1.3을 구현합니다.

#### Description

TLS 1.3은 버전 1.2(RFC 5246)를 포함한 이전 버전의 TLS를 대체하고 사용하지 않는 새로운 TLS 버전입니다. 또한 OCSP 스테이플링 확장(RFC 6066, RFC 6961), 세션 해시 및 확장 마스터 비밀 확장(RFC 7627)과 같은 다른 TLS 기능을 폐기하거나 변경합니다.

JDK의 JSSE(Java Secure Socket Extension)는 SSL, TLS 및 DTLS 프로토콜의 프레임워크 및 Java 구현을 제공합니다. 현재 JSSE API 및 JDK 구현은 SSL 3.0, TLS 1.0, TLS 1.1, TLS 1.2, DTLS 1.0 및 DTLS 1.2를 지원합니다.

이 JEP의 주요 목표는 최소한의 상호 운용 가능하고 호환 가능한 TLS 1.3 구현입니다. 최소한의 구현은 다음을 지원해야 합니다.

프로토콜 버전 협상

* Protocol version negotiation
* TLS 1.3 full handshake
* TLS 1.3 session resumption
* TLS 1.3 key and iv update
* TLS 1.3 updated OCSP stapling
* TLS 1.3 backward compatibility mode
* TLS 1.3 required extensions and algorithms
* RSASSA-PSS signature algorithms

최소한의 구현에는 새로운 공개 API가 필요하지 않습니다. 다음과 같은 새로운 표준 알고리즘 이름이 필요합니다.

* TLS protocol version name: TLSv1.3
* `javax.net.ssl.SSLContext` algorithm name: TLSv1.3
* TLS cipher suite names for TLS 1.3: `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`.

또한 KRB5 암호 제품군은 더 이상 사용하기에 안전한 것으로 간주되지 않으므로 JDK에서 제거됩니다.

이 JEP와 병행하여 다음과 같은 선택적 TLS 1.3 기능에 대한 암호화 알고리즘 지원을 개발할 것입니다.

* ChaCha20/Poly1305 암호 모음
* X25519/X448 타원 곡선 알고리즘
* edDSA 서명 알고리즘
시간이 허락한다면 이러한 기능이 이 JEP에 포함될 수 있습니다. 그렇지 않으면 별도의 기능으로 타겟팅되고 통합됩니다.

다음과 같은 중요한 기능은 이 JEP의 일부로 구현되지 않습니다.

* 0-RTT data
* Post-handshake authentication
* Signed certificate timestamps (SCT): RFC 6962

TLS 1.3은 이전 버전과 직접 호환되지 않습니다. TLS 1.3은 이전 버전과의 호환성 모드로 구현할 수 있지만 이 모드를 사용할 때 몇 가지 호환성 위험이 있습니다.

TLS 1.3은 절반 닫기 정책을 사용하는 반면 TLS 1.2 및 이전 버전은 이중 닫기 정책을 사용합니다. 이중 닫기 정책에 의존하는 애플리케이션의 경우 TLS 1.3으로 업그레이드할 때 호환성 문제가 있을 수 있습니다.

`signature_algorithms_cert` 확장을 사용하려면 사전 정의된 서명 알고리즘을 인증서 인증에 사용해야 합니다. 그러나 실제로 응용 프로그램은 지원되지 않는 서명 알고리즘을 사용할 수 있습니다.

DSA 서명 알고리즘은 TLS 1.3에서 지원되지 않습니다. 서버가 DSA 인증서만 사용하도록 구성된 경우 TLS 1.3으로 업그레이드할 수 없습니다.

TLS 1.3에 대해 지원되는 암호 제품군은 TLS 1.2 및 이전 버전과 동일하지 않습니다. 애플리케이션이 더 이상 지원되지 않는 암호 그룹을 하드 코딩하는 경우 애플리케이션 코드를 수정하지 않고는 TLS 1.3을 사용하지 못할 수 있습니다.

호환성 위험을 최소화하기 위해 이 TLS 1.3 구현은 기본적으로 이전 버전과의 호환성 모드를 구현하고 활성화합니다. 애플리케이션은 이전 버전과의 호환성 모드를 끄고 원하는 경우 TLS 1.3을 켜거나 끌 수 있습니다.

### JEP 333: ZGC: A Scalable Low-Latency Garbage Collector(Experimental)

ZGC라고도 하는 Z Garbage Collector는 확장 가능한 저지연 가비지 수집기입니다.

#### Goals

* GC 일시 중지 시간은 10ms를 초과해서는 안 됩니다.
* 비교적 작은 크기(수백 메가바이트)에서 매우 큰 크기(수테라바이트)에 이르는 힙을 처리합니다.
* G1 사용에 비해 15% 이하의 애플리케이션 처리량 감소
* 컬러 포인터 및 로드 배리어를 활용하여 향후 GC 기능 및 최적화를 위한 기반 마련
* 초기 지원 플랫폼: Linux/x64

##### Performance

SPECjbb® 2015를 사용하여 정기적인 성능 측정을 수행했습니다. 성능은 처리량과 대기 시간의 관점에서 모두 좋아 보입니다. 다음은 128G 힙을 사용하는 복합 모드에서 ZGC와 G1을 비교한 일반적인 벤치마크 점수(ZGC의 max-jOPS에 대해 정규화된 백분율)입니다.

```
ZGC
       max-jOPS: 100%
  critical-jOPS: 76.1%

G1
       max-jOPS: 91.2%
  critical-jOPS: 54.7%
```

다음은 동일한 벤치마크의 일반적인 GC 일시 중지 시간입니다. ZGC는 10ms 목표보다 훨씬 낮은 수준을 유지하고 있습니다. 정확한 숫자는 사용된 정확한 기계와 설정에 따라 다를 수 있습니다(위 및 아래 모두, 크게 다르지는 않음).

```
ZGC
                avg: 1.091ms (+/-0.215ms)
    95th percentile: 1.380ms
    99th percentile: 1.512ms
  99.9th percentile: 1.663ms
 99.99th percentile: 1.681ms
                max: 1.681ms

G1
                avg: 156.806ms (+/-71.126ms)
    95th percentile: 316.672ms
    99th percentile: 428.095ms
  99.9th percentile: 543.846ms
 99.99th percentile: 543.846ms
                max: 543.846ms
```

### JEP 335: Deprecate the Nashorn JavaScript Engine

Nashorn JavaScript 스크립트 엔진과 API, jjs 도구는 향후 릴리스에서 제거할 의도로 더 이상 사용되지 않습니다.

### JEP 336: Deprecate the Pack200 Tools and API

`java.util.jar`에서 `pack200` 및 `unpack200` 도구와 Pack200 API를 더 이상 사용하지 않습니다.

#### Description

`java.base` 모듈의 세 가지 유형은 최종적으로 더 이상 사용되지 않습니다. 즉, `@Deprecated(forRemoval=true)` 주석이 추가됩니다.

* `java.util.jar.Pack200`
* `java.util.jar.Pack200.Packer`
* `java.util.jar.Pack200.Unpacker`
  
`pack200` 및 `unpack200` 도구가 포함된 `jdk.pack` 모듈도 최종적으로 사용되지 않습니다.

`pack200` 또는 `unpack200`을 실행하면 계획된 도구 제거에 대한 경고가 표시됩니다. (아카이브를 정규화하기 위해) 하위 옵션 `n`과 함께 `jar -c`를 실행하면 하위 옵션의 계획된 제거에 대한 경고가 표시됩니다. 세 가지 도구 모두에 대한 문서는 사용 중단 및 계획된 제거를 나타냅니다.

향후 JDK 기능 릴리스에서 유형 및 모듈의 실제 제거를 위해 별도의 JEP가 제출됩니다.