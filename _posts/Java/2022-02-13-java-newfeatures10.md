---
title:  "Java 10 New Features"
excerpt: "Java 10 New Features"
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

새로운 LTS 버전인 JDK 10가 2018년 3월 20일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 10](https://openjdk.java.net/projects/jdk/10/)를 참고했습니다.

## Features

### JEP 286: Local-Variable Type Inference

이니셜라이저를 사용하여 지역 변수 선언에 대한 유형 추론을 확장하도록 Java 언어를 향상시킵니다.

#### Goals

우리는 개발자가 종종 불필요한 지역 변수 유형 선언을 생략할 수 있도록 함으로써 정적 유형 안전에 대한 Java의 약속을 유지하면서 Java 코드 작성과 관련된 의식을 줄임으로써 개발자 경험을 개선하고자 합니다. 이 기능은 예를 들어 다음과 같은 선언을 허용합니다.

```java
var list = new ArrayList<String>();  // infers ArrayList<String>
var stream = list.stream();          // infers Stream<String>
```

이 처리는 이니셜라이저가 있는 지역 변수, 향상된 for 루프의 인덱스 및 전통적인 for 루프에서 선언된 지역으로 제한됩니다. 메서드 형식, 생성자 형식, 메서드 반환 형식, 필드, catch 형식 또는 다른 종류의 변수 선언에는 사용할 수 없습니다.

### JEP 296: Consolidate the JDK Forest into a Single Repository

개발을 단순화하고 간소화하기 위해 JDK 포리스트의 수많은 리포지토리를 단일 리포지토리로 결합합니다.

#### Description

이러한 문제를 해결하기 위해 통합 숲의 프로토타입이 개발되었습니다. 프로토타입은 다음에서 사용할 수 있습니다.

```
http://hg.openjdk.java.net/jdk10/consol-proto/
```

프로토타입을 만드는 데 사용된 지원 변환 스크립트 중 일부는 unify.zip으로 첨부되어 있습니다.

프로토타입에서. 8개의 리포지토리는 JDK 프로모션을 표시하는 데 사용되는 태그에서 동기화되는 통합 포리스트와 함께 파일별 수준에서 기록을 보존하는 자동화된 변환 스크립트를 사용하여 단일 리포지토리로 결합되었습니다. 변경 집합 설명과 생성 날짜도 보존됩니다.

프로토타입에는 다른 수준의 코드 재구성이 있습니다. 통합 포리스트에서 Java 모듈용 코드는 일반적으로 단일 최상위 src 디렉토리 아래에 결합됩니다. 예를 들어, 오늘날 JDK 포리스트에는 다음과 같은 모듈 기반 디렉토리가 있습니다.

```
$ROOT/jdk/src/java.base
...
$ROOT/langtools/src/java.compiler
...
```

통합 상황에서는 이 코드는 다음과 같이 구성됩니다.

```
$ROOT/src/java.base
$ROOT/src/java.compiler
...
```

결과적으로 리포지토리의 루트에서 모듈에 있는 소스 파일의 상대 경로는 통합 및 src 디렉토리 조합 후에 유지됩니다.

유사하지만 덜 공격적인 재구성이 테스트 디렉토리에서 수행됩니다.

```
$ROOT/jdk/test/Foo.java
$ROOT/langtools/test/Bar.java
```

다음과 같이 변경됩니다.

```
$ROOT/test/jdk/Foo.java
$ROOT/test/langtools/Bar.java
```

노력은 현재 프로토타입이기 때문에 모든 부분이 완전히 완성된 것은 아니며 일부 영역에서는 적합성과 마감이 개선될 수 있습니다. HotSpot C/C++ 소스는 모듈화된 Java 코드와 함께 공유 src 디렉토리로 이동됩니다.

회귀 테스트는 프로토타입의 현재 상태로 실행되지만 jtreg 구성 파일의 추가 통합이 가능하며 향후 수행될 수 있습니다.

### JEP 304: Garbage-Collector Interface

성능이 탁월한 GC(가비지 수집기) 인터페이스를 도입하여 다양한 가비지 수집기의 소스 코드 격리를 개선합니다.

#### Goals 

* HotSpot 내부 GC 코드를 위한 더 나은 모듈성
* 현재 코드 기반을 교란하지 않고 HotSpot에 새 GC를 더 간단하게 추가
* JDK 빌드에서 GC를 더 쉽게 제외

#### Description

GC 인터페이스는 모든 가비지 수집기가 구현해야 하는 기존 클래스 `CollectedHeap`에 의해 정의됩니다. `CollectedHeap` 클래스는 가비지 수집기와 나머지 HotSpot 간의 상호 작용의 대부분을 구동합니다(`CollectedHeap`이 인스턴스화되기 전에 몇 가지 유틸리티 클래스가 필요함). 보다 구체적으로, 가비지 수집기 구현은 다음을 제공해야 합니다.

* `CollectedHeap`의 하위 클래스인 힙
* 런타임에 대한 다양한 장벽을 구현하는 `BarrierSet`의 하위 클래스인 장벽 세트
* `CollectorPolicy`의 구현
* 인터프리터용 GC에 대한 다양한 장벽을 구현하는 `GCInterpreterSupport` 구현(어셈블러 명령어 사용)
* C1 컴파일러용 GC에 대한 다양한 장벽을 구현하는 `GCC1Support` 구현
* C2 컴파일러용 GC에 대한 다양한 장벽을 구현하는 `GCC2Support` 구현
* 최종 GC 특정 인수의 초기화
* `MemoryService`, 관련 메모리 풀, 메모리 관리자 등의 설정

여러 가비지 수집기 간에 공유되는 구현 세부 정보에 대한 코드는 도우미 클래스에 있어야 합니다. 이렇게 하면 다양한 GC 구현에서 쉽게 사용할 수 있습니다. 예를 들어, 카드 테이블 지원을 위한 다양한 장벽을 구현하는 도우미 클래스가 있을 수 있으며 카드 테이블 사후 장벽이 필요한 GC는 해당 도우미 클래스의 해당 메서드를 호출합니다. 이러한 방식으로 인터페이스는 완전히 새로운 장벽을 구현할 수 있는 유연성을 제공하는 동시에 기존 코드를 믹스 앤 매치 스타일로 재사용할 수 있습니다.

### JEP 307: Parallel Full GC for G1

전체 GC를 병렬화하여 G1 최악의 경우 지연 시간을 개선합니다.

#### Description

G1 가비지 수집기는 전체 수집을 방지하도록 설계되었지만 동시 수집이 메모리를 충분히 빠르게 회수할 수 없는 경우 대체 전체 GC가 발생합니다. G1용 전체 GC의 현재 구현은 단일 스레드 마크 스윕 컴팩트 알고리즘을 사용합니다. Mark-sweep-compact 알고리즘을 병렬화하고 Young 및 Mixed 컬렉션과 동일한 수의 스레드를 사용하려고 합니다. 스레드 수는 -XX:ParallelGCThreads 옵션으로 제어할 수 있지만 이는 Young 및 Mixed 컬렉션에 사용되는 스레드 수에도 영향을 미칩니다.

### JEP 310: Application Class-Data Sharing

시작 및 설치 공간을 개선하려면 기존 클래스 데이터 공유("CDS") 기능을 확장하여 애플리케이션 클래스를 공유 아카이브에 배치할 수 있도록 합니다.

#### Goals

* 다양한 Java 프로세스에서 공통 클래스 메타데이터를 공유하여 공간을 줄입니다.
* 시작 시간을 개선합니다.
* JDK의 런타임 이미지 파일(`$JAVA_HOME/lib/modules`)과 애플리케이션 클래스 경로의 아카이브된 클래스를 내장 플랫폼 및 시스템 클래스 로더에 로드할 수 있도록 CDS를 확장합니다.
* 아카이브된 클래스를 사용자 정의 클래스 로더에 로드할 수 있도록 CDS를 확장합니다.

### JEP 312: Thread-Local Handshakes

전역 VM safepoint를 수행하지 않고 스레드에서 콜백을 실행하는 방법을 소개합니다. 모든 스레드 또는 없음이 아닌 개별 스레드를 중지하는 것이 가능하고 저렴합니다.

#### Description

핸드셰이크 작업은 해당 스레드가 safepoint 안전 상태에 있는 동안 각 JavaThread에 대해 실행되는 콜백입니다. 콜백은 스레드 자체 또는 VM 스레드에 의해 실행되고 스레드는 차단된 상태로 유지됩니다. Safepointing과 핸드셰이킹의 가장 큰 차이점은 스레드별 작업이 가능한 한 빨리 모든 스레드에서 수행되고 자체 작업이 완료되는 즉시 계속 실행된다는 것입니다. JavaThread가 실행 중인 것으로 알려진 경우 해당 단일 JavaThread로도 핸드셰이크를 수행할 수 있습니다.

초기 구현에서는 주어진 시간에 비행 중 최대 한 번의 핸드셰이크 작업으로 제한됩니다. 그러나 작업에는 모든 JavaThreads의 하위 집합이 포함될 수 있습니다. VM 스레드는 VM 작업을 통해 핸드셰이크 작업을 조정하여 사실상 핸드셰이크 작업 중에 전역 안전점이 발생하는 것을 방지합니다.

현재 safepointing 체계는 단일 스레드의 실행이 보호 페이지에서 강제로 트랩되도록 허용하는 스레드별 포인터를 통해 간접 참조를 수행하도록 수정되었습니다. 기본적으로 항상 두 개의 폴링 페이지가 있습니다. 하나는 항상 보호되고 다른 하나는 항상 보호되지 않습니다. 스레드가 양보하도록 하기 위해 VM은 보호된 페이지를 가리키도록 해당 스레드에 대한 스레드별 포인터를 업데이트합니다.

스레드 로컬 핸드셰이크는 초기에 x64 및 SPARC에서 구현됩니다. 다른 플랫폼은 일반 safepoint로 대체됩니다. 새로운 제품 옵션인 `-XX:ThreadLocalHandshakes`(기본값 `true`)를 통해 사용자는 지원되는 플랫폼에서 일반 safepoint를 선택할 수 있습니다.

### JEP 313: Remove the Native-Header Generation Tool (javah)

JDK에서 `javah` 도구를 제거합니다.

#### Description

제거 구현에는 문서 파일을 포함하여 `Mercurial` 저장소에서 영향을 받는 파일을 제거하고 `makefile` 변경을 지원하는 작업이 포함됩니다.

### JEP 314: Additional Unicode Language-Tag Extensions

`java.util.Locale` 및 관련 API를 향상하여 BCP 47 언어 태그의 추가 유니코드 확장을 구현합니다.

#### Goals

BCP 47 언어 태그에 대한 지원은 처음에 Java SE 7에 추가되었으며 유니코드 로케일 확장에 대한 지원은 달력 및 숫자로 제한되었습니다. 이 JEP는 관련 JDK 클래스에서 최신 LDML 사양에 지정된 더 많은 확장을 구현합니다.

#### Description

Java SE 9부터 지원되는 BCP 47 U 언어 태그 확장은 `ca` 및 `nu`입니다. 이 JEP는 다음과 같은 추가 확장에 대한 지원을 추가합니다.

* `cu` (currency type)
* `fw` (first day of week)
* `rg` (region override)
* `tz` (time zone)

이러한 추가 확장을 지원하기 위해 다음 API가 변경됩니다.

* `java.text.DateFormat::get*Instance`는 확장자 `ca`, `rg` 및/또는 `tz`를 기반으로 인스턴스를 반환합니다.
* `java.text.DateFormatSymbols::getInstance`는 확장 `rg`를 기반으로 인스턴스를 반환합니다.
* `java.text.DecimalFormatSymbols::getInstance`는 확장 `rg`를 기반으로 인스턴스를 반환합니다.
* `java.text.NumberFormat::get*Instance`는 확장자 `nu` 및/또는 r`g`를 기반으로 인스턴스를 반환합니다.
* `java.time.format.DateTimeFormatter::localizedBy`는 확장자 `ca`, `rg` 및/또는 `tz`를 기반으로 DateTimeFormatter 인스턴스를 반환합니다.
* `java.time.format.DateTimeFormatterBuilder::getLocalizedDateTimePattern`은 `rg` 확장을 기반으로 패턴 문자열을 반환합니다.
* `java.time.format.DecimalStyle::of`는 `nu` 및/또는 `rg` 확장을 기반으로 `DecimalStyle` 인스턴스를 반환합니다.
* `java.time.temporal.WeekFields::of`는 `fw` 및/또는 `rg` 확장을 기반으로 WeekFields 인스턴스를 반환합니다.
* `java.util.Calendar::{getFirstDayOfWeek,getMinimalDaysInWeek}`는 `fw` 및/또는 `rg` 확장을 기반으로 값을 반환합니다.
* `java.util.Currency::getInstance`는 `cu` 및/또는 `rg` 확장을 기반으로 `Currency` 인스턴스를 반환합니다.
* `java.util.Locale::getDisplayName`은 이러한 `U` 확장에 대한 표시 이름을 포함하는 문자열을 반환합니다.
* `java.util.spi.LocaleNameProvider`에는 이러한 `U` 확장의 키 및 유형에 대한 새 SPI가 있습니다.

### JEP 316: Heap Allocation on Alternative Memory Devices

HotSpot VM이 사용자가 지정한 NV-DIMM과 같은 대체 메모리 장치에 Java 개체 힙을 할당할 수 있도록 합니다.

#### Description

일부 운영 체제는 이미 파일 시스템을 통해 비 DRAM 메모리를 노출합니다. 예로는 NTFS DAX 모드와 ext4 DAX가 있습니다. 이러한 파일 시스템의 메모리 매핑된 파일은 페이지 캐시를 우회하고 가상 메모리를 장치의 물리적 메모리에 직접 매핑합니다.

이러한 메모리에 힙을 할당하기 위해 `-XX:AllocateHeapAt=<path>`라는 새 옵션을 추가할 수 있습니다. 이 옵션은 파일 시스템에 대한 경로를 취하고 메모리 매핑을 사용하여 메모리 장치에 개체 힙을 할당하는 원하는 결과를 얻습니다. JEP는 실행 중인 여러 JVM 간에 비휘발성 영역을 공유하거나 추가 JVM 호출을 위해 동일한 영역을 재사용하지 않습니다.

`-Xmx, -Xms` 등과 같은 기존 힙 관련 플래그 및 가비지 수집 관련 플래그는 이전과 같이 계속 작동합니다.

애플리케이션 보안을 보장하려면 구현에서 파일 시스템에서 생성된 파일이 다음과 같은지 확인해야 합니다.

* 다른 사용자가 액세스하는 것을 방지하기 위해 올바른 권한으로 보호됩니다.
* 가능한 모든 시나리오에서 응용 프로그램이 종료되면 제거됩니다.

### JEP 317: Experimental Java-Based JIT Compiler

Java 기반 JIT 컴파일러인 Graal을 Linux/x64 플랫폼에서 실험적 JIT 컴파일러로 사용할 수 있습니다.

#### Description

Linux/x64 플랫폼부터 Graal을 실험적 JIT 컴파일러로 사용하도록 설정합니다. Graal은 JDK 9에 도입된 JVMCI(JVM 컴파일러 인터페이스)를 사용합니다. Graal은 이미 JDK에 있으므로 이를 실험적 JIT로 활성화하려면 주로 테스트 및 디버깅 노력이 필요합니다.

Graal을 JIT 컴파일러로 사용하려면 java 명령줄에서 다음 옵션을 사용하세요.

* `-XX:+UnlockExperimentalVMOptions -XX:+JVMCICompiler`

### JEP 319: Root Certificates

JDK에서 루트 인증 기관(CA) 인증서의 기본 세트를 제공하십시오.

#### Goals

OpenJDK 빌드를 개발자에게 더 매력적으로 만들고 해당 빌드와 Oracle JDK 빌드 간의 차이를 줄이기 위해 Oracle의 Java SE 루트 CA 프로그램에서 루트 인증서를 공개합니다.

#### Description

`cacerts` 키 저장소는 Oracle Java SE 루트 CA 프로그램의 CA에서 발급한 루트 인증서 세트로 채워집니다. 전제 조건으로 각 CA는 Oracle에 인증서를 공개할 수 있는 권한을 부여하기 위해 Oracle Contributor Agreement(OCA) 또는 이에 상응하는 계약에 서명해야 합니다. 다음은 필수 계약에 서명한 CA와 각 CA에 대해 포함될 루트 인증서(고유 이름으로 식별됨) 목록입니다. 이 목록에는 현재 Oracle의 Java SE 루트 CA 프로그램의 구성원인 대부분의 CA가 포함되어 있습니다. 계약서에 서명하지 않은 사람들은 현재 포함되지 않습니다. 처리하는 데 시간이 더 오래 걸리는 항목은 다음 릴리스에 포함될 것입니다.

### JEP 322: Time-Based Release Versioning

현재 및 미래의 시간 기반 릴리스 모델에 대한 Java SE 플랫폼 및 JDK의 버전 문자열 체계와 관련 버전 정보를 검토합니다.

#### Goals

* [JEP 223](https://openjdk.java.net/jeps/223)에 의해 도입된 버전 번호 체계를 재구성하여 새로운 기능을 포함할 수 있는 기능 릴리스와 버그만 수정하는 업데이트 릴리스를 정의하는 시간 기반 릴리스 모델에 더 잘 맞도록 합니다.
* 현재 모델이 아닌 시간 기반 릴리스 모델, 다른 주기 또는 임시 릴리스가 기능 릴리스보다 작지만 업데이트 릴리스보다 큰 것을 허용합니다.
* 전체 [JEP 223](https://openjdk.java.net/jeps/223) 버전 문자열 체계와의 호환성을 유지합니다.
* 개발자나 최종 사용자가 릴리스가 얼마나 오래된 것인지 쉽게 파악할 수 있도록 하여 최신 보안 수정 사항 및 추가 기능이 포함된 최신 릴리스로 업그레이드할지 여부를 판단할 수 있습니다.
* 구현자가 릴리스가 구현자가 장기 지원을 제공하는 일련의 릴리스의 일부임을 표시하는 방법을 제공합니다.
* 관련 제품과 릴리스를 맞추기 위해 구현자가 추가 구현자별 버전 문자열을 포함하고 표시할 수 있는 방법을 제공합니다.
