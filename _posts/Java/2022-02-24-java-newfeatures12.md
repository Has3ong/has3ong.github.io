---
title:  "Java 12 New Features"
excerpt: "Java 12 New Features"
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

새로운 LTS 버전인 JDK 12가 2019년 3월 19일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 12](https://openjdk.java.net/projects/jdk/12/)를 참고했습니다.

### JEP 189:	Shenandoah: A Low-Pause-Time Garbage Collector (Experimental)

실행 중인 Java 스레드와 동시에 대피 작업을 수행하여 GC 일시 중지 시간을 줄이는 Shenandoah라는 새 가비지 수집(GC) 알고리즘을 추가합니다. Shenandoah의 일시 중지 시간은 힙 크기와 무관합니다. 즉, 힙이 200MB이든 200GB이든 동일한 일관된 일시 중지 시간을 갖게 됩니다.

### JEP 230:	Microbenchmark Suite

JDK 소스 코드에 마이크로벤치마크의 기본 제품군을 추가하고 개발자가 기존 마이크로벤치마크를 실행하고 새 마이크로벤치마크를 쉽게 만들 수 있도록 합니다.

#### Goals

* Java Microbenchmark Harness(JMH) 기반
* 지속적인 성능 테스트를 위한 안정적이고 조정된 벤치마크
  * 기능 릴리스의 기능 완료 이정표 이후 및 기능이 아닌 릴리스의 경우 안정적이고 움직이지 않는 제품군
  * 적용 가능한 테스트에 대해 이전 JDK 릴리스와 비교 지원
* 간소화
  * 새로운 벤치마크 추가 용이
  * API 및 옵션이 변경되거나 더 이상 사용되지 않거나 개발 중에 제거될 때 테스트를 쉽게 업데이트할 수 있습니다.
  * 구축 용이
  * 벤치마크를 쉽게 찾고 실행
* JMH 업데이트 지원
* 제품군에 약 100개의 벤치마크 초기 세트 포함

### JEP 325:	Switch Expressions (Preview)

`switch` 문을 확장하여 문이나 식으로 사용할 수 있고 두 형식 모두 "전통적인" 또는 "단순한" 범위 지정 및 제어 흐름 동작을 사용할 수 있습니다. 이러한 변경은 일상적인 코딩을 단순화하고 스위치에서 패턴 일치([JEP 305](https://openjdk.java.net/jeps/305))를 사용하는 방법도 준비합니다. 이것은 JDK 12의 미리보기 언어 기능입니다.

#### Description

"전통적인" 스위치 블록에 추가하여 새로운 "`case L ->`" 스위치 레이블과 함께 새로운 "단순화된" 형식을 추가할 것을 제안합니다. 레이블이 일치하면 화살표 레이블 오른쪽에 있는 표현식이나 명령문만 실행됩니다. 넘어짐이 없습니다. 예시를 알아보겠습니다.

```java
static void howMany(int k) {
    switch (k) {
        case 1 -> System.out.println("one");
        case 2 -> System.out.println("two");
        case 3 -> System.out.println("many");
    }
}
```

다음 코드는 아래와 같습니다.

```java
howMany(1);
howMany(2);
howMany(3);
```

결과는 다음과 같습니다.

```java
one
two
many
```

추가로 표현식으로 사용할 수 있도록 `switch` 문을 확장합니다. 일반적인 경우 `switch` 표현식은 다음과 같습니다.

`switch` 표현식은 폴리 표현식입니다. 대상 유형이 알려진 경우 이 유형은 각 암으로 푸시됩니다. `switch` 표현식의 유형은 알려진 경우 대상 유형입니다. 그렇지 않은 경우 각 케이스 암의 유형을 결합하여 독립형 유형을 계산합니다.

대부분의 `switch` 표현식에는 "`case L ->`" 스위치 레이블 오른쪽에 단일 표현식이 있습니다. 전체 블록이 필요한 경우 `break` 문을 확장하여 둘러싸는 `switch` 표현식의 값이 되는 인수를 취합니다.

```java
int j = switch (day) {
    case MONDAY  -> 0;
    case TUESDAY -> 1;
    default      -> {
        int k = day.toString().length();
        int result = f(k);
        break result;
    }
};
```

`switch` 문은 `switch` 문과 마찬가지로 "`case L:`" 스위치 레이블이 있는 "전통적인" `switch` 블록을 사용할 수도 있습니다(fall-through 의미론을 의미함). 이 경우 값은 `break with value` 문을 사용하여 생성됩니다.

```java
int result = switch (s) {
    case "Foo": 
        break 1;
    case "Bar":
        break 2;
    default:
        System.out.println("Neither Foo nor Bar, hmmm...");
        break 0;
};
```

두 가지 형태의 `break`(값 포함 및 없음)는 메서드의 두 가지 반환 형식과 유사합니다. 두 가지 형태의 반환 모두 메서드 실행을 즉시 종료합니다. `void`가 아닌 메서드에서는 메서드 호출자에게 제공되는 값을 추가로 제공해야 합니다. (`break expression-value`와 `break` 레이블 형식 사이의 모호성은 비교적 쉽게 처리될 수 있습니다.)

`switch` 식의 경우는 철저해야 합니다. 가능한 값에 대해 일치하는 `switch` 레이블이 있어야 합니다. 실제로 이것은 일반적으로 기본 절이 필요하다는 것을 의미합니다. 그러나 알려진 모든 경우를 포함하는 열거형 `switch` 표현식의 경우(결국 봉인된 유형에 대한 `switch` 표현식), 열거형 정의가 컴파일 타임과 런타임 사이에 변경되었음을 나타내는 기본 절을 컴파일러에서 삽입할 수 있습니다. (이것은 오늘날 개발자가 직접 수행하는 작업이지만 컴파일러를 삽입하는 것이 손으로 작성한 것보다 덜 방해가 되고 더 설명적인 오류 메시지를 가질 가능성이 높습니다.)

또한 `switch` 식은 값으로 정상적으로 완료되거나 예외가 발생해야 합니다. 이것은 여러 가지 결과를 낳습니다. 먼저 컴파일러는 모든 `switch` 레이블에 대해 일치하는 경우 값을 산출할 수 있는지 확인합니다.

```java
int i = switch (day) {
    case MONDAY -> {
        System.out.println("Monday"); 
        // ERROR! Block doesn't contain a break with value
    }
    default -> 1;
};
i = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY: 
        break 0;
    default: 
        System.out.println("Second half of the week");
        // ERROR! Group doesn't contain a break with value
};
```

또 다른 결과는 제어 문, `break`, `return` 및 `continue`가 다음과 같이 `switch` 식을 통해 이동할 수 없다는 것입니다.

```java
z: 
    for (int i = 0; i < MAX_VALUE; ++i) {
        int k = switch (e) { 
            case 0:  
                break 1;
            case 1:
                break 2;
            default: 
                continue z; 
                // ERROR! Illegal jump through a switch expression 
        };
    ...
    }
```

기회의 대상으로 `float`, `double` 및 `long`과 같이 이전에 허용되지 않았던 기본 유형(및 해당 상자 유형)에 대한 전환을 지원하도록 `switch`를 확장할 수 있습니다.

### JEP 334:	JVM Constants API

API를 도입하여 주요 클래스 파일 및 런타임 아티팩트, 특히 상수 풀에서 로드할 수 있는 상수에 대한 명목상의 설명을 모델링합니다.

#### Description

새로운 패키지 `java.lang.invoke.constant`에서 값 기반 기호 참조(JVMS 5.1) 유형 제품군을 정의하고 로드 가능한 각 종류의 상수를 설명할 수 있습니다. 기호 참조는 클래스 로딩 또는 접근성 컨텍스트와 별개로 순수한 명목 형태로 로드 가능한 상수를 설명합니다. 일부 클래스는 고유한 기호 참조로 작동할 수 있습니다(예: `String`). 연결 가능한 상수의 경우 이러한 상수를 설명하기 위한 명목상의 정보를 포함하는 기호 참조 유형(`ClassDesc`, `MethodTypeDesc`, `MethodHandleDesc` 및 `DynamicConstantDesc`) 패밀리를 정의합니다.

API 사양의 초안 스냅샷은 여기에서 찾을 수 있으며 [JEP 303](https://openjdk.java.net/jeps/303)의 기능과의 관계에 대한 자세한 정보는 이 동반 문서에서 찾을 수 있습니다.

### JEP 340:	One AArch64 Port, Not Two

32비트 ARM 포트와 64비트 `aarch64` 포트를 유지하면서 `arm64` 포트와 관련된 모든 소스를 제거합니다.

#### Description

JDK에는 2개의 64비트 ARM 포트가 있습니다. 주요 소스는 `src/hotspot/cpu/arm`, `open/src/hotspot/cpu/aarch64`에 대해 설명합니다. 두 가지 포트로 구성된 `aarch64` 구현을 구현함으로써 이 JEP를 위해 Oracle에서 제공한 전자를 `arm64`라고 하고 있습니다.

이 JEP의 일부로 사물은 다음과 같이 될 것입니다.

* `open/src/hotspot/cpu/arm`에서 64비트 및 32비트 빌드와 관련된 모든 `arm64` 및 `#ifdef`를 제거하세요.
* 이 포트와 관련하여 `#ifdef`에 대한 빠른 JDK 소스
* 이 포트를 만들기 위해 제작을 시작했습니다. `aarch64`는 64비트 ARM의 기본 빌드로 강력합니다.
* 전체 32비트 ARM JEP와 관련하여 이전에 보호되지 않았으며 이 테스트를 계속해서 실행하고 있습니다.

### JEP 341:	Default CDS Archives

64비트 플랫폼에서 기본 클래스 목록을 사용하여 클래스 데이터 공유(CDS) 아카이브를 생성하도록 JDK 빌드 프로세스를 개선합니다.

#### Goals

* 즉시 사용 가능한 시작 시간 개선
* CDS를 활용하기 위해 사용자가 `-Xshare:dump`를 실행할 필요가 없습니다.

#### Description

이미지를 링크한 후 `java -Xshare:dump`를 실행하도록 JDK 빌드를 수정합니다. (일반적인 경우에 대해 더 나은 메모리 레이아웃을 얻기 위해 GC 힙 크기 등을 미세 조정하기 위해 추가 명령줄 옵션이 포함될 수 있습니다.) 결과 CDS 아카이브를 `lib/server` 디렉토리에 남겨두십시오. 결과 이미지.

JDK 11의 서버 VM에 대해 `-Xshare:auto`가 기본적으로 활성화되어 있으므로 사용자는 자동으로 CDS 기능의 이점을 누릴 수 있습니다. CDS를 비활성화하려면 `-Xshare:off`로 실행하십시오.

고급 요구 사항(예: 응용 프로그램 클래스, 다른 GC 구성 등을 포함하는 사용자 지정 클래스 목록 사용)이 있는 사용자는 여전히 이전과 같이 사용자 지정 CDS 아카이브를 생성할 수 있습니다.

### JEP 344:	Abortable Mixed Collections for G1

일시 중지 대상을 초과할 수 있는 경우 G1 혼합 컬렉션을 중단할 수 있도록 합니다.

#### Decsription

컬렉션 세트 선택 휴리스틱이 반복적으로 잘못된 수의 영역을 선택한다는 것을 G1이 발견하면 혼합 컬렉션을 수행하는 더 증분 방식으로 전환합니다. 컬렉션 세트를 필수 부분과 선택 부분의 두 부분으로 분할합니다. 필수 부분은 G1이 점진적으로 처리할 수 없는 컬렉션 집합의 일부로 구성되지만(예: 젊은 영역) 효율성 향상을 위해 이전 영역도 포함할 수 있습니다. 이것은 예를 들어 예측된 컬렉션 집합의 80%일 수 있습니다. 이전 영역으로만 구성되는 예측 컬렉션 집합의 나머지 20%는 선택적 부분을 형성합니다.

G1이 필수 부분 수집을 마친 후 시간이 남아 있으면 G1은 훨씬 더 세분화된 수준에서 선택 부분 수집을 시작합니다. 이 선택적 부분의 수집 단위는 남은 시간에 따라 다르며 최대 한 번에 한 지역까지 내려갑니다. 선택적 수집 집합의 일부를 수집한 후 G1은 남은 시간에 따라 수집을 중단할 수 있습니다.

예측이 다시 더 정확해짐에 따라 필수 부분이 다시 한 번 모든 컬렉션 집합을 구성할 때까지 컬렉션의 선택적 부분이 점점 작아집니다(즉, G1이 발견적 방법에 완전히 의존함). 예측이 다시 부정확해지면 다음 컬렉션은 다시 필수 부분과 선택 부분으로 구성됩니다.

### JEP 346:	Promptly Return Unused Committed Memory from G1

유휴 상태일 때 Java 힙 메모리를 운영 체제에 자동으로 반환하도록 G1 가비지 수집기를 향상시킵니다.

#### Description

운영 체제에 최대 메모리 양을 반환하는 목표를 달성하기 위해 G1은 애플리케이션이 비활성 상태인 동안 주기적으로 계속 시도하거나 전체 Java 힙 사용량을 결정하기 위해 동시 주기를 트리거합니다. 이로 인해 Java 힙의 사용되지 않은 부분이 자동으로 운영 체제로 반환됩니다. 선택적으로 사용자 제어 하에 전체 GC를 수행하여 반환된 메모리 양을 최대화할 수 있습니다.

응용 프로그램은 비활성 상태로 간주되며 다음 두 가지 경우 모두 G1이 주기적인 가비지 수집을 트리거합니다.

* 이전 가비지 수집 일시 중지 이후 `G1PeriodicGCInterval` 밀리초 이상이 경과했으며 현재 진행 중인 동시 주기가 없습니다. 값이 0이면 메모리를 즉시 회수하기 위한 주기적인 가비지 수집이 비활성화됨을 나타냅니다.
* JVM 호스트 시스템(예: 컨테이너)에서 `getloadavg()` 호출에 의해 반환된 평균 1분 시스템 로드 값은 `G1PeriodicGCSystemLoadThreshold` 미만입니다. `G1PeriodicGCSystemLoadThreshold`가 0이면 이 조건은 무시됩니다.

이러한 조건 중 하나라도 충족되지 않으면 현재 예상되는 주기적 가비지 수집이 취소됩니다. 주기적인 가비지 수집은 다음에 `G1PeriodicGCInterval` 시간이 지나면 다시 고려됩니다.

주기적 가비지 수집 유형은 `G1PeriodicGCInvokesConcurrent` 옵션 값에 의해 결정됩니다. 설정하면 G1이 동시 주기를 계속하거나 시작하고, 그렇지 않으면 G1이 전체 GC를 수행합니다. 컬렉션이 끝나면 G1은 현재 Java 힙 크기를 조정하여 잠재적으로 운영 체제에 메모리를 반환합니다. 새 Java 힙 크기는 `MinHeapFreeRatio`, `MaxHeapFreeRatio`, 최소 및 최대 힙 크기 구성을 포함하되 이에 국한되지 않는 Java 힙 크기 조정을 위한 기존 구성에 의해 결정됩니다.

기본적으로 G1은 이 주기적인 가비지 수집 중에 동시 주기를 시작하거나 계속합니다. 이것은 응용 프로그램의 중단을 최소화하지만 전체 컬렉션에 비해 궁극적으로 많은 메모리를 반환하지 못할 수 있습니다.

이 메커니즘에 의해 트리거된 모든 가비지 수집에는 G1 주기적 수집 원인으로 태그가 지정됩니다. 이러한 로그가 표시되는 방식의 예는 다음과 같습니다.

```java
(1) [6.084s][debug][gc,periodic ] Checking for periodic GC.
    [6.086s][info ][gc          ] GC(13) Pause Young (Concurrent Start) (G1 Periodic Collection) 37M->36M(78M) 1.786ms
(2) [9.087s][debug][gc,periodic ] Checking for periodic GC.
    [9.088s][info ][gc          ] GC(15) Pause Young (Prepare Mixed) (G1 Periodic Collection) 9M->9M(32M) 0.722ms
(3) [12.089s][debug][gc,periodic ] Checking for periodic GC.
    [12.091s][info ][gc          ] GC(16) Pause Young (Mixed) (G1 Periodic Collection) 9M->5M(32M) 1.776ms
(4) [15.092s][debug][gc,periodic ] Checking for periodic GC.
    [15.097s][info ][gc          ] GC(17) Pause Young (Mixed) (G1 Periodic Collection) 5M->1M(32M) 4.142ms
(5) [18.098s][debug][gc,periodic ] Checking for periodic GC.
    [18.100s][info ][gc          ] GC(18) Pause Young (Concurrent Start) (G1 Periodic Collection) 1M->1M(32M) 1.685ms
(6) [21.101s][debug][gc,periodic ] Checking for periodic GC.
    [21.102s][info ][gc          ] GC(20) Pause Young (Concurrent Start) (G1 Periodic Collection) 1M->1M(32M) 0.868ms
(7) [24.104s][debug][gc,periodic ] Checking for periodic GC.
    [24.104s][info ][gc          ] GC(22) Pause Young (Concurrent Start) (G1 Periodic Collection) 1M->1M(32M) 0.778ms
```