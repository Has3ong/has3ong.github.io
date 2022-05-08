---
title:  "Java 14 New Features"
excerpt: "Java 14 New Features"
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

새로운 LTS 버전인 JDK 14가 2020년 3월 17일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 14](https://openjdk.java.net/projects/jdk/14/)를 참고했습니다.

### JEP 305:	Pattern Matching for instanceof (Preview)

`instanceof` 연산자에 대한 `pattern matching`로 Java 프로그래밍 언어를 향상시키십시오. 패턴 일치를 사용하면 프로그램의 공통 논리, 즉 개체에서 구성 요소의 조건부 추출을 보다 간결하고 안전하게 표현할 수 있습니다. 이것은 JDK 14의 미리보기 언어 기능입니다.

#### Description

패턴은 (1) 대상에 적용할 수 있는 술어와 (2) 술어가 성공적으로 적용된 경우에만 대상에서 추출되는 바인딩 변수 집합의 조합입니다.

유형 테스트 패턴은 단일 바인딩 변수와 함께 유형을 지정하는 술어로 구성됩니다.

`instanceof` 연산자(JLS 15.20.2)는 유형 대신 유형 테스트 패턴을 사용하도록 확장되었습니다. 아래 코드에서 `String s` 구문은 유형 테스트 패턴입니다.

```java
if (obj instanceof String s) {
    // can use s here
} else {
    // can't use s here
}
```

`instanceof` 연산자는 대상 `obj`를 다음과 같이 유형 테스트 패턴에 "일치"합니다. `obj`가 `String`의 인스턴스이면 `String`으로 캐스트되고 바인딩 변수 `s`에 할당됩니다. 바인딩 변수는 `if` 문의 `false` 블록이 아니라 `if` 문의 `true` 블록 범위에 있습니다.

지역 변수의 범위와 달리 바인딩 변수의 범위는 포함하는 표현식 및 문의 의미 체계에 의해 결정됩니다. 예를 들어 이 코드에서:

```java
if (!(obj instanceof String s)) {
    .. s.contains(..) ..
} else {
    .. s.contains(..) ..
}
```

`true` 블록의 `s`는 둘러싸는 클래스의 필드를 참조하고 `false` 블록의 `s`는 `instanceof` 연산자에 의해 도입된 바인딩 변수를 참조합니다.

`if` 문의 조건이 단일 `instanceof`보다 복잡해지면 바인딩 변수의 범위도 그에 따라 커집니다. 예를 들어 이 코드에서:

```java
if (obj instanceof String s && s.length() > 5) {.. s.contains(..) ..}
```

바인딩 변수 `s`는 `&&` 연산자의 오른쪽 범위와 실제 블록에 있습니다. (우변은 `instanceof`가 성공하고 `s`에 할당된 경우에만 평가됩니다.) 반면에 이 코드에서:

```java
if (obj instanceof String s || s.length() > 5) {.. s.contains(..) ..}
```

바인딩 변수 `s`는 `||` 오른쪽의 범위에 없습니다. 연산자이며 실제 블록의 범위에 있지 않습니다. (이 지점에서 s는 둘러싸는 클래스의 필드를 나타냅니다.)

대상이 `null`일 때 `instanceof`가 작동하는 방식에는 변경 사항이 없습니다. 즉, 패턴은 일치만 하고 `obj`가 `null`이 아닌 경우에만 s가 할당됩니다.

`instanceof`에서 패턴 일치를 사용하면 Java 프로그램에서 전체 명시적 캐스트 수를 크게 줄일 수 있습니다. 게다가, 타입 테스트 패턴은 평등 메소드를 작성할 때 특히 유용합니다. Effective Java 책의 항목 10에서 가져온 다음 동등 방법을 고려하십시오.

```java
@Override public boolean equals(Object o) { 
    return (o instanceof CaseInsensitiveString) && 
        ((CaseInsensitiveString) o).s.equalsIgnoreCase(s); 
}
```

유형 테스트 패턴을 사용하면 더 명확하게 다시 작성할 수 있습니다.

```java
@Override public boolean equals(Object o) { 
    return (o instanceof CaseInsensitiveString cis) && 
        cis.s.equalsIgnoreCase(s); 
}
```

이에 따라 `instanceof` 문법이 확장됩니다.

```java
RelationalExpression:
     ...
     RelationalExpression instanceof ReferenceType
     RelationalExpression instanceof Pattern

Pattern:
     ReferenceType Identifier
```

### JEP 343:	Packaging Tool (Incubator)

자체 포함된 Java 애플리케이션을 패키징하기 위한 도구를 작성하십시오.

#### GOals

다음과 같은 JavaFX `javapackager` 도구를 기반으로 하는 간단한 패키징 도구를 만듭니다.

* 최종 사용자에게 자연스러운 설치 환경을 제공하기 위해 기본 패키징 형식을 지원합니다. 이러한 형식에는 Windows의 msi 및 exe, macOS의 pkg 및 dmg, Linux의 deb 및 rpm이 포함됩니다.
* 패키징 시 시작 시간 매개변수를 지정할 수 있습니다.
* 명령줄에서 직접 호출하거나 ToolProvider API를 통해 프로그래밍 방식으로 호출할 수 있습니다.

### JEP 345:	NUMA-Aware Memory Allocation for G1

NUMA 인식 메모리 할당을 구현하여 대형 시스템에서 G1 성능을 향상시킵니다.

### JEP 349:	JFR Event Streaming

지속적인 모니터링을 위해 JDK Flight Recorder 데이터를 노출합니다.

#### Goals

* in-process 및 out-of-process 애플리케이션 모두에 대해 디스크에서 JFR 데이터를 지속적으로 사용하기 위한 API를 제공합니다.
* 스트리밍이 아닌 경우와 동일한 이벤트 세트를 기록하고 가능하면 오버헤드가 1% 미만입니다.
* 이벤트 스트리밍은 디스크 및 메모리 기반의 비 스트리밍 녹화와 공존할 수 있어야 합니다.

#### Description

`jdk.jfr` 모듈의 `jdk.jfr.consumer` 패키지는 이벤트를 비동기식으로 구독하는 기능으로 확장되었습니다. 사용자는 녹음 파일을 덤프하지 않고 디스크 저장소에서 녹음 데이터를 직접 읽거나 스트리밍할 수 있습니다. 스트림과 상호 작용하는 방법은 이벤트 도착에 대한 응답으로 호출할 처리기(예: 람다 함수)를 등록하는 것입니다.

다음 예는 10ms 이상 경합하는 전체 CPU 사용량 및 잠금을 인쇄합니다.

```java
try (var rs = new RecordingStream()) {
  rs.enable("jdk.CPULoad").withPeriod(Duration.ofSeconds(1));
  rs.enable("jdk.JavaMonitorEnter").withThreshold(Duration.ofMillis(10));
  rs.onEvent("jdk.CPULoad", event -> {
    System.out.println(event.getFloat("machineTotal"));
  });
  rs.onEvent("jdk.JavaMonitorEnter", event -> {
    System.out.println(event.getClass("monitorClass"));
  });
  rs.start();
}
```

`RecordingStream` 클래스는 소스가 라이브 스트림이든 디스크의 파일이든 상관없이 이벤트를 필터링하고 소비하는 균일한 방법을 제공하는 `jdk.jfr.consumer.EventStream` 인터페이스를 구현합니다.

```java
public interface EventStream extends AutoCloseable {
  public static EventStream openRepository();
  public static EventStream openRepository(Path directory);
  public static EventStream openFile(Path file);

  void setStartTime(Instant startTime);
  void setEndTime(Instant endTime);
  void setOrdered(boolean ordered);
  void setReuse(boolean reuse);

  void onEvent(Consumer<RecordedEvent> handler);
  void onEvent(String eventName, Consumer<RecordedEvent handler);
  void onFlush(Runnable handler);
  void onClose(Runnable handler);
  void onError(Runnable handler);
  void remove(Object handler);

  void start();
  void startAsync();

  void awaitTermination();
  void awaitTermination(Duration duration);
  void close();
}
```

스트림을 생성하는 세 가지 팩토리 메소드가 있습니다. `EventStream::openRepository(Path)`는 디스크 저장소에서 스트림을 구성합니다. 이것은 파일 시스템에 대해 직접 작업하여 다른 프로세스를 모니터링하는 방법입니다. 디스크 저장소의 위치는 연결 API를 사용하여 읽을 수 있는 시스템 속성 `"jdk.jfr.repository"`에 저장됩니다. `EventStream::openRepository()` 메서드를 사용하여 프로세스 내 모니터링을 수행할 수도 있습니다. `RecordingStream`과 달리 녹음을 시작하지 않습니다. 대신 스트림은 예를 들어 JCMD 또는 JMX를 사용하여 외부 수단으로 녹화가 시작된 경우에만 이벤트를 수신합니다. `EventStream::openFile(Path)` 메서드는 녹음 파일에서 스트림을 만듭니다. 오늘날 이미 존재하는 `RecordingFile` 클래스를 보완합니다.

인터페이스를 사용하여 버퍼링할 데이터의 양과 이벤트를 시간순으로 정렬해야 하는지 여부를 설정할 수도 있습니다. 할당 압력을 최소화하기 위해 각 이벤트에 대해 새 이벤트 개체를 할당해야 하는지 또는 이전 개체를 재사용할 수 있는지 여부를 제어하는 옵션도 있습니다. 스트림은 현재 스레드에서 시작하거나 비동기적으로 시작할 수 있습니다.

스레드 로컬 버퍼에 저장된 이벤트는 1초에 한 번씩 JVM(Java Virtual Machine)에 의해 디스크 저장소로 주기적으로 플러시됩니다. 별도의 스레드는 데이터가 기록된 시점까지 가장 최근 파일을 구문 분석하고 이벤트를 구독자에게 푸시합니다. 오버헤드를 낮게 유지하기 위해 활성 구독 이벤트만 파일에서 읽습니다. 플러시가 완료되었을 때 알림을 받기 위해 `EventStream::onFlush(Runnable)` 메서드를 사용하여 핸들러를 등록할 수 있습니다. 이것은 JVM이 다음 이벤트 세트를 준비하는 동안 데이터를 집계하거나 외부 시스템으로 푸시할 수 있는 기회입니다.

### JEP 352:	Non-Volatile Mapped Byte Buffers

FileChannel API를 사용하여 비휘발성 메모리를 참조하는 `MappedByteBuffer` 인스턴스를 생성할 수 있도록 새로운 JDK 관련 파일 매핑 모드를 추가합니다.

#### Description

##### Preliminary Changes

이 JEP는 Java SE API에 대한 두 가지 관련 개선 사항을 사용합니다.

* 구현 정의 맵 모드 지원(JDK-8221397)
* MappedByteBuffer::범위를 지정하는 강제 메서드(JDK-8221696)

##### Proposed JDK-Specific API Changes

1. 새 모듈에서 공개 API를 통해 새 MapMode 열거 값 노출

새 모듈인 `jdk.nio.mapmode`는 동일한 이름의 단일 새 패키지를 내보냅니다. 공개 확장 열거형 `ExtendedMapMode`가 이 패키지에 추가됩니다:

```java
package jdk.nio.mapmode;
. . .
public class ExtendedMapMode {
    private ExtendedMapMode() { }

    public static final MapMode READ_ONLY_SYNC = . . .
    public static final MapMode READ_WRITE_SYNC = . . .
}
```

`FileChannel::map` 메서드를 호출하여 NVM 장치 파일에 매핑된 읽기 전용 또는 읽기-쓰기 `MappedByteBuffer`를 각각 만들 때 새 열거 값이 사용됩니다. NVM 장치 파일 매핑을 지원하지 않는 플랫폼에서 이러한 플래그가 전달되면 `UnsupportedOperationException`이 발생합니다. 지원되는 플랫폼에서는 대상 `FileChannel` 인스턴스가 NVM 장치를 통해 열린 파일에서 파생된 경우에만 이러한 새 값을 인수로 전달하는 것이 적절합니다. 다른 경우에는 `IOException`이 발생합니다.

2. 영구 MappedByteBuffer 통계를 추적하는 `BufferPoolMXBean` 게시

ManagementFactory 클래스는 매핑된 또는 직접 바이트 버퍼의 기존 범주에 대해 count, total_capacity 및 memory_used를 추적하는 BufferPoolMXBean 인스턴스 목록을 검색하는 데 사용할 수 있는 List<T> getPlatformMXBeans(Class<T>) 메서드를 제공합니다. 이름이 "매핑된 - '비휘발성 메모리'"인 추가의 새로운 BufferPoolMXBean을 반환하도록 수정되며, 현재 ExtendedMapMode.READ_ONLY_SYNC 또는 ExtendedMapMode.READ_WRITE_SYNC 모드로 매핑된 모든 MappedByteBuffer 인스턴스에 대한 위의 통계를 추적합니다. 이름이 매핑된 기존 BufferPoolMXBean은 현재 MapMode.READ_ONLY, MapMode.READ_WRITE 또는 MapMode.PRIVATE 모드로 매핑된 MappedByteBuffer 인스턴스에 대한 통계만 계속 추적합니다.

##### Proposed Internal JDK API Changes

1. `jdk.internal.misc.Unsafe` 클래스에 새 메소드 `writebackMemory` 추가

```java
public void writebackMemory(long address, long length)
```

이 메서드를 호출하면 `address`에서 시작하여 `address + length`까지 계속되는 주소 범위의 메모리에 대한 모든 수정 사항이 캐시에서 메모리로 다시 쓰여지는 것을 보장합니다. 구현은 i) 호출 지점에서 보류 중이고 ii) 대상 범위의 주소 메모리가 쓰기 되돌림에 포함되는 현재 스레드의 모든 저장소를 보장해야 합니다(즉, 호출자가 메모리 펜스를 수행할 필요가 없음). 호출 전 작업). 또한 반환되기 전에 주소 지정된 모든 바이트의 쓰기 저장이 완료되었음을 보장해야 합니다(즉, 호출자가 호출 후 메모리 펜스 작업을 수행할 필요가 없음).

쓰기 되돌림 메모리 작업은 JIT 컴파일러에서 인식하는 소수의 내장 함수를 사용하여 구현됩니다. 목표는 프로세서 캐시 라인 쓰기 저장 명령어로 변환되는 내장 함수를 사용하여 지정된 주소 범위에서 각 연속 캐시 라인의 쓰기 저장을 구현하여 데이터 유지 비용을 최소한으로 줄이는 것입니다. 계획된 디자인은 또한 사전 쓰기 저장 및 사후 쓰기 저장 메모리 동기화 고유 기능을 사용합니다. 이는 프로세서 쓰기 저장(x64에는 세 가지 가능한 후보가 있음)에 대한 특정 명령 선택과 선택에 수반되는 주문 요구 사항에 따라 메모리 동기화 명령 또는 무작동으로 변환될 수 있습니다.

주의 `Unsafe` 클래스에서 이 기능을 구현하는 좋은 이유는 비휘발성 메모리를 사용하는 대체 데이터 지속성 구현과 같이 더 일반적으로 사용될 가능성이 높기 때문입니다.

### JEP 358:	Helpful NullPointerExceptions

어떤 변수가 `null`인지 정확하게 설명하여 JVM에서 생성된 `NullPointerExceptions`의 사용성을 개선합니다.

#### Goals

* 프로그램의 조기 종료에 대해 개발자 및 지원 직원에게 유용한 정보를 제공합니다.
* 동적 예외를 정적 프로그램 코드와 보다 명확하게 연결하여 프로그램 이해를 향상시킵니다.
* 새로운 개발자가 종종 `NullPointerException`에 대해 갖는 혼란과 우려를 줄입니다.

##### Description

JVM은 코드가 `null` 참조를 역참조하려고 시도하는 프로그램의 지점에서 `NullPointerException(NPE)`을 발생시킵니다. 프로그램의 바이트코드 명령을 분석하여 JVM은 정확히 어떤 변수가 `null`인지 확인하고 NPE의 `null-detail` 메시지와 함께 변수(소스 코드 측면에서)를 설명합니다. 그러면 `null-detail` 메시지가 메서드, 파일 이름 및 줄 번호와 함께 JVM의 메시지에 표시됩니다.

> 참고: JVM은 예외 유형과 동일한 행에 예외 메시지를 표시하므로 행이 길어질 수 있습니다. 웹 브라우저의 가독성을 위해 이 JEP는 예외 유형 다음 두 번째 행에 null-detail 메시지를 표시합니다.

예를 들어, 할당문 `a.i = 99;`은 NPE 이 메시지를 생성합니다:

```java
Exception in thread "main" java.lang.NullPointerException: 
        Cannot assign field "i" because "a" is null
    at Prog.main(Prog.java:5)
```

더 복잡한 문장 `a.b.c.i = 99;` NPE가 발생하면 메시지는 명령문을 분석하고 `null`에 이르는 전체 액세스 경로를 표시하여 원인을 정확히 찾아냅니다.

```java
Exception in thread "main" java.lang.NullPointerException: 
        Cannot read field "c" because "a.b" is null
    at Prog.main(Prog.java:5)
```

전체 액세스 경로를 지정하면 특히 코드 줄이 같은 이름을 여러 번 사용하는 경우 개발자가 복잡한 소스 코드 줄을 탐색하는 데 도움이 되기 때문에 `null` 필드의 이름만 지정하는 것보다 더 유용합니다.

마찬가지로 배열 액세스 및 할당 문 `a[i][j][k] = 99;` NPE를 던집니다:

```java
Exception in thread "main" java.lang.NullPointerException:
        Cannot load from object array because "a[i][j]" is null
    at Prog.main(Prog.java:5)
```

유사하게 `a.i = b.j;`인 경우 NPE를 던집니다:

```java
Exception in thread "main" java.lang.NullPointerException:
        Cannot read field "j" because "b" is null
    at Prog.main(Prog.java:5)
```

모든 예에서 행 번호와 함께 `null` 세부 정보 메시지는 소스 코드에서 `null인` 표현식을 찾아내기에 충분합니다. 이상적으로는 `null-detail` 메시지가 실제 소스 코드를 보여주지만 소스 코드와 바이트코드 명령어(아래 참조) 간의 대응 특성을 고려할 때 이는 수행하기 어렵습니다. 또한 표현식에 배열 액세스가 포함되는 경우 `null-detail` 메시지는 `a[i][j]`일 때 `i` 및 `j`의 런타임 값과 같이 `null` 요소로 이어지는 실제 배열 인덱스를 표시할 수 없습니다. `null`입니다. 이는 배열 인덱스가 NPE가 `throw`될 때 손실된 메서드의 피연산자 스택에 저장되었기 때문입니다.

JVM에서 직접 생성 및 `throw`한 NPE에만 `null-detail` 메시지가 포함됩니다. JVM에서 실행되는 프로그램에서 명시적으로 생성 및/또는 명시적으로 던진 NPE는 아래에서 설명하는 바이트코드 분석 및 `null-detail` 메시지 생성의 대상이 아닙니다. 또한, 예를 들어 문자열 연결을 최적화하기 위해 JVM에서 생성 및 호출하는 특수 목적의 저수준 메서드인 숨겨진 메서드의 코드로 인해 발생하는 NPE에 대해서는 `null-detail` 메시지가 보고되지 않습니다. 숨겨진 메서드에는 NPE의 소스를 정확히 찾아내는 데 도움이 될 수 있는 파일 이름이나 줄 번호가 없으므로 `null` 세부 정보 메시지를 인쇄하는 것은 무의미합니다.

##### Computing the null-detail message

`a.b.c.i = 99;`와 같은 소스 코드는 여러 바이트 코드 명령어로 컴파일됩니다. NPE가 던져지면 JVM은 어떤 바이트코드 명령어가 어떤 메소드를 담당하는지 정확히 알고 이 정보를 사용하여 `null-detail` 메시지를 계산합니다. 메시지에는 두 부분이 있습니다.

첫 번째 부분(필드 "`c`"를 읽을 수 없음)은 NPE의 결과입니다. 바이트코드 명령어가 피연산자 스택에서 `null` 참조를 팝했기 때문에 수행할 수 없는 작업을 나타냅니다.

두 번째 부분("`a.b`"가 `null`이기 때문에)은 NPE의 이유입니다. `Null` 참조를 피연산자 스택에 푸시한 소스 코드 부분을 다시 만듭니다.

`null-detail` 메시지의 첫 번째 부분은 다음 표 1에 자세히 설명된 것처럼 `null`을 팝한 바이트코드 명령어에서 계산됩니다.

|bytecode|1st part|
|--:|:--|
|`aload`|"Cannot load from `<element type>` array"|
|`arraylength`|"Cannot read the array length"|
|`astore`|"Cannot store to `<element type>` array"|
|`athrow`|"Cannot throw exception"|
|`getfield`|"Cannot read field `<field name>`"|
|`invokeinterface`, `invokespecial`, `invokevirtual`|"Cannot invoke `<method>`"|
|`monitorenter`|"Cannot enter synchronized block"|
|`monitorexit`|"Cannot exit synchronized block"|
|`putfield`|"Cannot assign field `<field name>`"|
|Any other bytecode|No NPE possible, no message|

`<method>`는 `<class name>.<method name>(<parameter types>)`으로 나뉩니다.

`null-detail` 메시지의 두 번째 부분은 더 복잡합니다. 피연산자 스택에서 널 참조로 이어진 액세스 경로를 식별하지만 복잡한 액세스 경로에는 여러 바이트코드 명령어가 포함됩니다. 메서드의 일련의 명령어가 주어지면 이전 명령어가 `null` 참조를 푸시했는지 명확하지 않습니다. 따라서 모든 메서드의 명령에 대해 간단한 데이터 흐름 분석이 수행됩니다. 어떤 명령어가 어떤 피연산자 스택 슬롯에 푸시하는지 계산하고 이 정보를 슬롯을 팝하는 명령어에 전파합니다. (분석은 명령어의 수에서 선형입니다.) 분석이 주어지면 소스 코드에서 액세스 경로를 구성하는 명령어를 통해 뒤로 물러나는 것이 가능합니다. 메시지의 두 번째 부분은 표 2에 자세히 설명된 대로 각 단계에서 바이트코드 명령이 주어지면 단계별로 조합됩니다.

|bytecode|2nd part|
|--:|:--|
|`aconst_null`|`null`|
|`aaload`|compute the 2nd part for the instruction which pushed the array reference, then append `[`, then compute the 2nd part for the instruction that pushed the index, then append `]`|
|`iconst_*`, `bipush`, `sipush`|the constant value|
|`getfield`|compute the 2nd part for the instruction which pushed the reference that is accessed by this getfield, then append `.<field name>`|
|`getstatic`|`<class name>.<field name>`|
|`invokeinterface`, `invokevirtual`, `invokespecial`, `invokestatic`|If in the first step, the return value of `<method>`, else `<method>`|
|`iload*`, `aload*|`|For local variable 0, "this". For other local variables and parameters, the variable name if a local variable table is available, otherwise `<parameter i >` or `<local i >`.|
|Any other bytecode|Not applicable to the second part.|

액세스 경로는 임의의 수의 바이트코드 명령어로 구성될 수 있습니다. null-detail 메시지가 반드시 이들 모두를 포함하는 것은 아닙니다. 알고리즘은 출력의 복잡성을 제한하기 위해 지침을 통해 제한된 수의 단계만 수행합니다. 최대 단계 수에 도달하면 "..."와 같은 자리 표시자가 내보내집니다. 드문 경우지만 지침을 한 단계 더 나아가는 것이 불가능하고 null-detail 메시지에는 첫 번째 부분만 포함됩니다("Cannot ...", "because ..." 설명 없음).

null-detail 메시지 -- *Cannot read field "c" because "a.b" is null* -- JVM이 메시지의 일부로 `Throwable::getMessage`를 호출할 때 요청 시 계산됩니다. 일반적으로 예외가 전달하는 메시지는 예외 객체가 생성될 때 제공되어야 하지만 많은 NPE가 프로그램에 의해 포착되고 폐기되기 때문에 계산 비용이 많이 들고 항상 필요한 것은 아닙니다. 계산에는 NPE를 일으킨 메서드의 바이트코드 명령어와 `null`을 팝한 명령어의 인덱스가 필요합니다. 다행히도 `Throwable`의 구현에는 예외의 출처에 대한 이 정보가 포함되어 있습니다.

이 기능은 새로운 부울 명령줄 옵션 `-XX:{+|-}ShowCodeDetailsInExceptionMessages`로 전환할 수 있습니다. 이 옵션은 메시지가 인쇄되지 않도록 먼저 기본 '거짓'을 갖습니다. 이후 릴리스에서 기본적으로 예외 메시지의 코드 세부 정보를 활성화하기 위한 것입니다.

##### Example of computing the null-detail message

다음은 소스 코드의 다음 스니펫을 기반으로 한 예입니다.

```java
a().b[i][j] = 99;
```

소스 코드는 바이트코드로 다음과 같이 표현됩니다.

```java
5: invokestatic  #7    // Method a:()LA;
   8: getfield      #13   // Field A.b, an array
  11: iload_1             // Load local variable i, an array index
  12: aaload              // Load b[i], another array
  13: iload_2             // Load local variable j, another array index
  14: bipush        99
  16: iastore             // Store to b[i][j]
```

`a().b[i]`가 `null`이라고 가정합니다. 이로 인해 `b[i][j]`에 저장할 때 NPE가 `throw`됩니다. JVM은 `bytecode 16: iastore`를 실행하고 `bytecode 12: aaload`가 피연산자 스택에 `null`을 푸시했기 때문에 NPE를 발생시킵니다. `null-detail` 메시지는 다음과 같이 계산됩니다.

```java
Cannot store to int array because "Test.a().b[i]" is null
```

계산은 바이트코드 명령어와 바이트코드 인덱스 16을 포함하는 메서드로 시작됩니다. 인덱스 16의 명령어는 iastore이므로 메시지의 첫 번째 부분은 표 1에 따라 "Cannot store to int array"입니다.

메시지의 두 번째 부분에서 알고리즘은 `iastore`가 팝하기에 충분히 불행한 `null`을 푸시한 명령으로 되돌아갑니다. 데이터 흐름 분석은 이것이 `12: aaload`, 어레이 로드임을 나타냅니다. 표 2에 따라 배열 로드가 `null` 배열 참조를 담당할 때 배열 참조(배열 인덱스가 아닌)를 피연산자 스택인 `8: getfield`로 푸시한 명령으로 되돌아갑니다. 그런 다음 다시 표 2에 따라 `getfield`가 액세스 경로의 일부일 때 `getfield`, `5: invokestatic`에서 사용하는 참조를 푸시한 명령으로 다시 한 걸음 물러납니다. 이제 메시지의 두 번째 부분을 조합할 수 있습니다.

* For 5: `invokestatic`, emit "Test.a()"
* For 8: `getfield`, emit ".b"
* For 12: `aaload`, emit "[" and stepback to the instruction that pushed the index, 11: `iload_1`. Emit "i", the name of local variable #1, then "]".

알고리즘은 인덱스 `j`를 푸시하는 `13: iload_2` 또는 99를 푸시하는 `14: bipush`로 진행하지 않습니다. 이는 NPE의 원인과 관련이 없기 때문입니다.

`null-detail` 세부사항 메시지의 많은 예가 있는 파일이 이 JEP에 첨부됩니다. `output_with_debug_info.txt`는 클래스 파일에 로컬 변수 테이블이 포함된 경우 메시지를 나열합니다. 클래스 파일에 지역 변수 테이블이 없을 때 `output_no_debug_info.txt` 메시지가 표시됩니다.

### JEP 359:	Records (Preview)

레코드로 Java 프로그래밍 언어를 향상시키십시오. 레코드는 얕게 변경할 수 없는 데이터에 대한 투명한 보유자인 클래스를 선언하기 위한 간결한 구문을 제공합니다. 이것은 JDK 14의 미리보기 언어 기능입니다.

#### Description

`Records`는 Java 언어의 새로운 유형 선언입니다. `ennum`과 마찬가지로 레코드는 제한된 형식의 클래스입니다. 표현을 선언하고 해당 표현과 일치하는 API를 커밋합니다. `records`는 클래스가 일반적으로 누리는 자유, 즉 표현에서 API를 분리하는 기능을 포기합니다. 그 대가로 레코드는 상당한 정도의 정확성을 얻습니다.

레코드에는 이름과 상태 설명이 있습니다. 상태 설명은 레코드의 `components`를 선언합니다. 선택적으로 레코드에는 본문이 있습니다. 예를 들어:

```java
record Point(int x, int y) { }
```

레코드는 데이터에 대한 단순하고 투명한 보유자라는 의미론적 주장을 하기 때문에 레코드는 많은 표준 멤버를 자동으로 획득합니다.

* 상태 설명의 각 구성 요소에 대한 비공개 최종 필드입니다.
* 구성 요소와 이름 및 유형이 동일한 상태 설명의 각 구성 요소에 대한 공개 읽기 접근자 메서드입니다.
* 해당 인수에서 각 필드를 초기화하는 상태 설명과 서명이 동일한 공개 생성자.
* 두 레코드가 동일한 유형이고 동일한 상태를 포함하는 경우 동일하다고 말하는 `equals` 및 `hashCode`의 구현. 그리고
* 이름과 함께 모든 레코드 구성 요소의 문자열 표현을 포함하는 `toString`의 구현입니다.

다시 말해서, 레코드의 표현은 구성, 해체(처음에는 접근자, 패턴 일치가 있는 경우 해체 패턴), 평등 및 표시에 대한 프로토콜과 마찬가지로 상태 설명에서 기계적으로 완전하게 파생됩니다.

##### Restrictions on records

레코드는 다른 클래스를 확장할 수 없으며 상태 설명의 구성 요소에 해당하는 개인 최종 필드 이외의 인스턴스 필드를 선언할 수 없습니다. 선언된 다른 모든 필드는 정적이어야 합니다. 이러한 제한은 상태 설명만으로 표현을 정의하도록 합니다.

레코드는 암시적으로 최종적이며 추상적일 수 없습니다. 이러한 제한 사항은 레코드의 API가 상태 설명에 의해서만 정의되며 나중에 다른 클래스나 레코드에 의해 향상될 수 없다는 점을 강조합니다.

레코드의 구성 요소는 암시적으로 최종적입니다. 이 제한은 데이터 집계에 광범위하게 적용할 수 있는 `immutable by default` 정책을 구현합니다.

위의 제한 사항을 넘어서서 레코드는 일반 클래스처럼 작동합니다. 레코드는 최상위 수준으로 선언되거나 중첩될 수 있고, 제네릭일 수 있고, 인터페이스를 구현할 수 있으며, `new` 키워드를 통해 인스턴스화됩니다. 레코드의 본문은 정적 메서드, 정적 필드, 정적 이니셜라이저, 생성자, 인스턴스 메서드 및 중첩 유형을 선언할 수 있습니다. 기록과 상태 설명의 개별 구성 요소에 주석을 달 수 있습니다. 레코드가 중첩된 경우 암시적으로 정적입니다. 이것은 레코드에 상태를 자동으로 추가하는 인스턴스를 즉시 둘러싸는 것을 방지합니다.

##### Explicitly declaring members of a record

상태 설명에서 자동으로 파생되는 모든 멤버도 명시적으로 선언할 수 있습니다. 그러나 접근자 또는 `equals/hashCode`를 부주의하게 구현하면 레코드의 의미론적 불변성을 훼손할 위험이 있습니다.

표준 생성자(시그니처가 레코드의 상태 설명과 일치하는 생성자)를 명시적으로 선언할 때 특별히 고려해야 합니다. 생성자는 형식 매개변수 목록 없이 선언될 수 있으며(이 경우 상태 설명과 동일하다고 가정), 생성자 본문이 정상적으로 완료될 때 확실히 할당되지 않은 레코드 필드는 해당 형식 매개변수(`this.xml`)에서 암시적으로 초기화됩니다. `x = x`) 종료 시. 이를 통해 명시적 정식 생성자는 매개변수의 유효성 검사 및 정규화만 수행하고 명백한 필드 초기화를 생략할 수 있습니다. 예를 들어:

```java
record Range(int lo, int hi) {
  public Range {
    if (lo > hi)  /* referring here to the implicit constructor parameters */
      throw new IllegalArgumentException(String.format("(%d,%d)", lo, hi));
  }
}
```

##### Grammar

```java
RecordDeclaration:
  {ClassModifier} record TypeIdentifier [TypeParameters] 
    (RecordComponents) [SuperInterfaces] [RecordBody]

RecordComponents:
  {RecordComponent {, RecordComponent}}

RecordComponent:
  {Annotation} UnannType Identifier

RecordBody:
  { {RecordBodyDeclaration} }

RecordBodyDeclaration:
  ClassBodyDeclaration
  RecordConstructorDeclaration

RecordConstructorDeclaration:
  {Annotation} {ConstructorModifier} [TypeParameters] SimpleTypeName
    [Throws] ConstructorBody
```

##### Annotations on record components

선언 주석은 레코드 구성 요소, 매개 변수, 필드 또는 메서드에 적용 가능한 경우 레코드 구성 요소에 허용됩니다. 이러한 대상에 적용할 수 있는 선언 주석은 위임된 구성원의 암시적 선언으로 전파됩니다.

레코드 구성 요소의 유형을 수정하는 유형 주석은 필수 멤버의 암시적 선언(예: 생성자 매개변수, 필드 선언 및 메서드 선언)의 유형으로 전파됩니다. 필수 멤버의 명시적 선언은 유형 주석을 포함하지 않고 해당 레코드 구성 요소의 유형과 정확히 일치해야 합니다.

##### Reflection API

다음 공개 메소드가 `java.lang.Class`에 추가됩니다.

* `RecordComponent[]` `getRecordComponents()`
* `boolean isRecord()`

`getRecordComponents()` 메서드는 1 객체의 배열을 반환합니다. 여기서 `java.lang.reflect.RecordComponent`는 새 클래스입니다. 이 배열의 요소는 레코드 선언에 나타나는 것과 동일한 순서로 레코드의 구성 요소에 해당합니다. 이름, 유형, 일반 유형, 주석 및 접근자 메서드를 포함하여 배열의 각 `RecordComponent`에서 추가 정보를 추출할 수 있습니다.

`isRecord()` 메서드는 주어진 클래스가 레코드로 선언된 경우 `true`를 반환합니다. (`isEnum()`과 비교하십시오.)

### JEP 361:	Switch Expressions (Standard)

자세한 사항은 [JEP 354](https://openjdk.java.net/jeps/354)에서 확인 가능합니다.

#### History

스위치 표현식은 2017년 12월 [JEP 325](https://openjdk.java.net/jeps/325)에서 제안되었습니다. [JEP 325](https://openjdk.java.net/jeps/325)는 2018년 8월에 미리 보기 기능으로 JDK 12의 대상이 되었습니다. [JEP 325](https://openjdk.java.net/jeps/325)의 한 측면은 `switch` 식에서 결과 값을 반환하기 위해 `break` 문을 오버로드하는 것입니다. JDK 12에 대한 피드백은 이러한 `break` 사용이 혼란스럽다고 제안했습니다. 피드백에 대한 응답으로 [JEP 354](https://openjdk.java.net/jeps/354)는 [JEP 325](https://openjdk.java.net/jeps/325)의 진화로 만들어졌습니다. [JEP 354](https://openjdk.java.net/jeps/354)는 새로운 선언문, `yield`를 제안하고 `break`의 원래 의미를 복원했습니다. [JEP 354](https://openjdk.java.net/jeps/354)는 2019년 6월에 미리 보기 기능으로 JDK 13을 대상으로 했습니다. JDK 13에 대한 피드백은 스위치 표현식이 추가 변경 없이 JDK 14에서 최종적이고 영구적이 될 준비가 되었다고 제안했습니다.

### JEP 362:	Deprecate the Solaris and SPARC Ports

Solaris/SPARC, Solaris/x64 및 Linux/SPARC 포트를 더 이상 사용하지 않으며 향후 릴리스에서 제거할 예정입니다.

#### Goals

더 이상 사용되지 않는 포트 중 하나에 대한 빌드를 구성하려고 할 때 오류 메시지를 표시하도록 빌드 시스템을 개선합니다. 오류 메시지는 새 구성 옵션을 통해 표시되지 않습니다.

관련 JDK 문서에서 더 이상 사용되지 않는 포트 및 관련 포트별 기능을 표시합니다.

#### Description

##### Build-configuration changes

Solaris 및/또는 SPARC 빌드를 구성하려고 하면 다음 출력이 생성됩니다.

```bash
$ bash ./configure
...
checking compilation type... native
configure: error: The Solaris and SPARC ports are deprecated and may be removed in a future release. \
Use --enable-deprecated-ports=yes to suppress this error.
configure exiting with result code 1
$
```

새로운 빌드 구성 옵션 `--enable-deprecated-ports=yes`는 오류를 억제하고 계속 진행합니다.


```bash
$ bash ./configure --enable-deprecated-ports=yes
...
checking compilation type... native
configure: WARNING: The Solaris and SPARC ports are deprecated and may be removed in a future release.
...
Build performance summary:
* Cores to use:   32
* Memory limit:   96601 MB

The following warnings were produced. Repeated here for convenience:
WARNING: The Solaris and SPARC ports are deprecated and may be removed in a future release.
$
```

오류/경고는 Solaris 및 SPARC(Solaris/SPARC, Solaris/x64, Linux/SPARC 포함)용 빌드를 구성할 때 발행됩니다.

##### Solaris-specific features deprecated for removal

제거를 위해 더 이상 사용되지 않는 Solaris 관련 기능

* `jdk.crypto.ucrypto` 모듈의 `OracleUcrypto` JCE 공급자(8234870)
* `jdk.net.SocketFlow` 소켓 옵션(8234871)

### JEP 363:	Remove the Concurrent Mark Sweep (CMS) Garbage Collector

CMS(Concurrent Mark Sweep) 가비지 수집기를 제거합니다.

#### Description

이 변경 사항은 CMS 컴파일을 비활성화하고 소스 트리에서 gc/cms 디렉토리의 내용을 제거하며 CMS에만 관련된 옵션을 제거합니다. 설명서에서 CMS에 대한 참조도 삭제됩니다. CMS를 사용하려는 테스트는 필요에 따라 제거되거나 조정됩니다.

`-XX:+UseConcMarkSweepGC` 옵션을 통해 CMS를 사용하려고 하면 다음 경고 메시지가 표시됩니다.

```
Java HotSpot(TM) 64-Bit Server VM warning: Ignoring option UseConcMarkSweepGC; \
support was removed in <version>
```

VM은 기본 수집기를 사용하여 계속 실행됩니다.

### JEP 364:	ZGC on macOS

ZGC 가비지 수집기를 macOS로 이식합니다.

#### Description

ZGC의 macOS 구현은 두 부분으로 구성됩니다.

* **Support for multi-mapping memory on macOS**. ZGC 디자인은 컬러 포인터를 집중적으로 사용하므로 macOS에서 여러 가상 주소(알고리즘의 다른 색상 포함)를 동일한 물리적 메모리에 매핑하는 방법이 필요합니다. 이를 위해 mach microkernel mach_vm_remap API를 사용할 것입니다. 힙의 물리적 메모리는 개념적으로 파일 디스크립터와 유사하지만 (대부분) 인접한 가상 주소에 대신 상주하는 별도의 주소 보기에서 유지 관리됩니다. 이 메모리는 알고리즘의 다양한 포인터 색상을 나타내는 다양한 ZGC 메모리 보기로 다시 매핑됩니다.
* **Support in ZGC for discontiguous memory reservations**. Linux에서는 초기화 중에 16TB의 가상 주소 공간을 예약합니다. 이것이 작동하려면 공유 라이브러리가 원하는 주소 공간에 매핑되지 않는다고 가정합니다. 기본 Linux 구성에서 이는 안전한 가정입니다. 그러나 macOS에서 ASLR 메커니즘은 주소 공간에 침입하므로 ZGC는 힙 예약이 연속적이지 않도록 해야 합니다. 공유 VM 코드는 단일 연속 메모리 예약이 GC 구현에서 사용된다는 가정도 중지해야 합니다. 결과적으로 `is_in_reserved()`, `reserved_region()` 및 `base()`와 같은 GC API는 CollectedHeap에서 제거됩니다.

### JEP 365:	ZGC on Windows

ZGC 가비지 수집기를 Windows로 이식합니다.

#### Description

대부분의 ZGC 코드 기반은 플랫폼에 독립적이며 Windows 관련 변경 사항이 필요하지 않습니다. x64에 대한 기존 로드 배리어 지원은 운영 체제에 구애받지 않으며 Windows에서도 사용할 수 있습니다. 이식해야 하는 플랫폼별 코드는 주소 공간이 예약되는 방식과 물리적 메모리가 예약된 주소 공간에 매핑되는 방식과 관련이 있습니다. 메모리 관리를 위한 Windows API는 POSIX API와 다르며 어떤 면에서는 덜 유연합니다.

ZGC의 Windows 구현에는 다음 작업이 필요합니다.

* **Support for multi-mapping memory**. ZGC에서 컬러 포인터를 사용하려면 힙 다중 매핑에 대한 지원이 필요하므로 프로세스 주소 공간의 여러 다른 위치에서 동일한 물리적 메모리에 액세스할 수 있습니다. Windows에서 페이징 파일 지원 메모리는 매핑된 가상 주소와 관련이 없는 ID(핸들)가 있는 물리적 메모리를 제공합니다. 이 ID를 사용하면 ZGC가 동일한 물리적 메모리를 여러 위치에 매핑할 수 있습니다.
* **Support for mapping paging-file backed memory into a reserved address space**. Windows 메모리 관리 API는 POSIX의 mmap/munmap만큼 유연하지 않습니다. 특히 파일 지원 메모리를 이전에 예약된 주소 공간 영역으로 매핑할 때 그렇습니다. 이를 위해 ZGC는 Windows 개념의 주소 공간 자리 표시자를 사용합니다. 자리 표시자 개념은 Windows 10 및 Windows Server 버전 1803에서 도입되었습니다. 이전 버전의 Windows에 대한 ZGC 지원은 구현되지 않습니다.
* **Support for mapping and unmapping arbitrary parts of the heap**. 힙 페이지의 동적 크기 조정(및 크기 조정)과 함께 ZGC의 힙 레이아웃을 사용하려면 임의의 힙 그래뉼 매핑 및 매핑 해제에 대한 지원이 필요합니다. Windows 주소 공간 자리 표시자와 결합된 이 요구 사항은 자리 표시자가 운영 체제(Linux에서와 같이)에 의해 자동으로 분할/통합되는 것과는 반대로 프로그램에 의해 명시적으로 분할/통합되어야 하기 때문에 특별한 주의가 필요합니다.
* **Support for committing and uncommitting arbitrary parts of the heap**. ZGC는 Java 프로그램이 실행되는 동안 물리적 메모리를 동적으로 커밋 및 커밋 해제할 수 있습니다. 이러한 작업을 지원하기 위해 물리적 메모리는 여러 페이징 파일 세그먼트로 분할되고 지원됩니다. 각 페이징 파일 세그먼트는 ZGC 힙 그래뉼에 해당하며 다른 세그먼트와 독립적으로 커밋 및 커밋 해제될 수 있습니다.

### JEP 366:	Deprecate the ParallelScavenge + SerialOld GC Combination

Parallel Scavenge와 Serial Old 가비지 수집 알고리즘의 조합은 더 이상 사용되지 않습니다.

#### Description

`-XX:+UseParallelGC` `-XX:-UseParallelOldGC` 옵션 조합을 더 이상 사용하지 않는 것 외에도 `-XX:UseParallelOldGC` 옵션도 사용하지 않습니다. 유일한 용도는 병렬 구세대 GC를 선택 해제하여 직렬 구세대 GC를 활성화하는 것이기 때문입니다.

결과적으로 `UseParallelOldGC` 옵션을 명시적으로 사용하면 사용 중단 경고가 표시됩니다. 특히 경고는 `-XX:+UseParallelOldGC`를 독립형으로 사용하여(`-XX:+UseParallelGC` 없이) 병렬 Young 및 Old Generation GC 알고리즘을 선택하는 경우 표시됩니다.

사용 중단 경고 없이 병렬 Young 및 Old Generation GC 알고리즘을 선택하는 유일한 방법은 명령줄에서 `-XX:+UseParallelGC`만 지정하는 것입니다.

### JEP 367:	Remove the Pack200 Tools and API

`java.util.jar` 패키지에서 `pack200` 및 `unpack200` 도구와 Pack200 API를 제거하십시오. 이러한 도구와 API는 Java SE 11에서 제거하기 위해 더 이상 사용되지 않으며 향후 릴리스에서 제거할 예정입니다.

#### Description

이전에 `@Deprecated(forRemoval=true)` 주석이 달린 `java.base` 모듈의 세 가지 유형이 이 JEP가 궁극적으로 대상으로 하는 JDK 기능 릴리스에서 제거됩니다.

* `java.util.jar.Pack200`
* `java.util.jar.Pack200.Packer`
* `java.util.jar.Pack200.Unpacker`

`pack200` 및 `unpack200` 도구가 포함된 jdk.pack 모듈은 이전에 `@Deprecated(forRemoval=true)`로 주석 처리되었으며 이 JEP가 궁극적으로 대상으로 하는 JDK 기능 릴리스에서도 제거됩니다.

### JEP 368:	Text Blocks (Second Preview)

자세한 사항은 [JEP 355](https://openjdk.java.net/jeps/355)에서 확인 가능합니다.

#### History

텍스트 블록은 철회되고 JDK 12에 나타나지 않은 [JEP 326(Raw String Literals)](https://openjdk.java.net/jeps/326)에서 시작된 탐색의 후속으로 2019년 초 JEP 355에서 제안했습니다. [JEP 355](https://openjdk.java.net/jeps/355)는 2019년 중반에 JDK 13을 대상으로 미리보기 기능. JDK 13에 대한 피드백은 두 개의 새로운 이스케이프 시퀀스를 추가하여 JDK 14에서 텍스트 블록을 다시 미리 봐야 한다고 제안했습니다.

### JEP 370:	Foreign-Memory Access API (Incubator)

Java 프로그램이 Java 힙 외부의 외부 메모리에 안전하고 효율적으로 액세스할 수 있도록 하는 API를 도입하십시오.

#### Goals

외부 메모리 API는 다음 기준을 충족해야 합니다.

* **Generality**: 동일한 API가 다양한 외부 메모리(예: 기본 메모리, 영구 메모리, 관리되는 힙 메모리 등)에서 작동할 수 있어야 합니다.
* **Safety**: 작동 중인 메모리의 종류에 관계없이 API가 JVM의 안전을 훼손하는 것은 불가능해야 합니다.
* **Determinism**: 메모리 할당 해제 작업은 소스 코드에서 명시적이어야 합니다.

#### Description

외부 메모리 액세스 API는 `MemorySegment`, `MemoryAddress` 및 `MemoryLayout`의 세 가지 주요 추상화를 도입합니다.

`MemorySegment`는 주어진 공간 및 시간 경계를 가진 연속 메모리 영역을 모델링하는 데 사용됩니다. `MemoryAddress`는 세그먼트 내의 오프셋으로 생각할 수 있습니다. 마지막으로 `MemoryLayout`은 메모리 세그먼트의 내용에 대한 프로그래밍 방식의 설명입니다.

메모리 세그먼트는 기본 메모리 버퍼, Java 배열 및 바이트 버퍼(직접 또는 힙 기반)와 같은 다양한 소스에서 만들 수 있습니다. 예를 들어 기본 메모리 세그먼트는 다음과 같이 생성할 수 있습니다.

```java
try (MemorySegment segment = MemorySegment.allocateNative(100)) {
   ...
}
```

이렇게 하면 크기가 100바이트인 기본 메모리 버퍼와 연결된 메모리 세그먼트가 생성됩니다.

메모리 세그먼트는 공간적으로 제한됩니다. 즉, 하한과 상한이 있습니다. 세그먼트를 사용하여 이러한 경계 외부의 메모리에 액세스하려고 하면 예외가 발생합니다. `try-with-resource` 구성을 사용하여 입증된 것처럼 세그먼트도 시간적으로 제한됩니다. 즉, 생성되고 사용된 다음 더 이상 사용되지 않을 때 닫힙니다. 세그먼트를 닫는 것은 항상 명시적인 작업이며 세그먼트와 관련된 메모리 할당 해제와 같은 추가 부작용이 발생할 수 있습니다. 이미 닫힌 메모리 세그먼트에 액세스하려고 하면 예외가 발생합니다. 공간적 및 시간적 안전 검사는 함께 메모리 액세스 API의 안전을 보장하기 위해 중요하므로 예를 들어 하드 JVM 크래시가 없습니다.

세그먼트와 관련된 메모리를 역참조하려면 메모리 액세스 `var` 핸들을 얻을 수 있습니다. 이러한 특수 `var` 핸들에는 역참조가 발생하는 주소인 `MemoryAddress` 유형의 필수 액세스 좌표가 하나 이상 있습니다. `MemoryHandles` 클래스의 팩토리 메서드를 사용하여 가져옵니다. 예를 들어, 네이티브 세그먼트의 요소를 설정하기 위해 다음과 같이 메모리 액세스 var 핸들을 사용할 수 있습니다.

```java
VarHandle intHandle = MemoryHandles.varHandle(int.class,
        ByteOrder.nativeOrder());

try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    MemoryAddress base = segment.baseAddress();
    for (int i = 0; i < 25; i++) {
        intHandle.set(base.addOffset(i * 4), i);
    }
}
```

메모리 액세스 `var` 핸들은 다차원 인덱싱된 액세스와 같은 더 복잡한 주소 지정 체계를 지원하기 위해 `long` 유형의 하나 이상의 추가 액세스 좌표를 얻을 수도 있습니다. 이러한 메모리 액세스 var 핸들은 일반적으로 `MemoryHandles` 클래스에도 정의된 하나 이상의 결합자 메서드를 호출하여 얻습니다. 예를 들어, 네이티브 세그먼트의 요소를 설정하는 보다 직접적인 방법은 다음과 같이 구성된 인덱싱된 메모리 액세스 핸들을 사용하는 것입니다.

```java
VarHandle intHandle = MemoryHandles.varHandle(int.class, 
        ByteOrder.nativeOrder());
VarHandle intElemHandle = MemoryHandles.withStride(intHandle, 4);

try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    MemoryAddress base = segment.baseAddress();
    for (int i = 0; i < 25; i++) {
        intElemHandle.set(base, (long) i, i);
    }
}
```

이것은 플랫 메모리 버퍼의 풍부한 다차원 주소 지정을 효과적으로 허용합니다.

API의 표현력을 향상시키고 위의 예와 같은 명시적 숫자 계산의 필요성을 줄이기 위해 `MemoryLayout` API를 사용하여 메모리 세그먼트의 내용을 프로그래밍 방식으로 설명할 수 있습니다. 예를 들어, 위의 예에서 사용된 기본 메모리 세그먼트의 레이아웃은 다음과 같이 설명할 수 있습니다.

```java
SequenceLayout intArrayLayout
    = MemoryLayout.ofSequence(25,
        MemoryLayout.ofValueBits(32,
            ByteOrder.nativeOrder()));
```

이것은 주어진 요소 레이아웃(32비트 값)이 25번 반복되는 시퀀스 메모리 레이아웃을 생성합니다. 메모리 레이아웃이 있으면 다음 예제와 같이 코드에서 모든 수동 숫자 계산을 제거하고 필요한 메모리 액세스 `var` 핸들 생성을 단순화할 수 있습니다.

```java
SequenceLayout intArrayLayout
    = MemoryLayout.ofSequence(25,
        MemoryLayout.ofValueBits(32,
            ByteOrder.nativeOrder()));

VarHandle intElemHandle
    = intArrayLayout.varHandle(int.class,
        PathElement.sequenceElement());

try (MemorySegment segment = MemorySegment.allocateNative(intArrayLayout)) {
    MemoryAddress base = segment.baseAddress();
    for (int i = 0; i < intArrayLayout.elementCount().getAsLong(); i++) {
        intElemHandle.set(base, (long) i, i);
    }
}
```

이 예에서 레이아웃 인스턴스는 복잡한 레이아웃 표현식에서 중첩 레이아웃을 선택하는 데 사용되는 레이아웃 경로 생성을 통해 메모리 액세스 `var` 핸들 생성을 유도합니다. 레이아웃 인스턴스는 또한 레이아웃에서 파생된 크기 및 정렬 정보를 기반으로 하는 기본 메모리 세그먼트의 할당을 유도합니다. 이전 예제의 루프 상수는 시퀀스 레이아웃의 요소 수로 대체되었습니다.

외부 메모리 액세스 API는 처음에 동일한 이름의 패키지에 `jdk.incubator.foreign`이라는 인큐베이팅 모듈로 제공됩니다.