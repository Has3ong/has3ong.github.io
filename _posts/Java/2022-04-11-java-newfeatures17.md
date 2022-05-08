---
title:  "JDK 17 New Features"
excerpt: "JDK 17 New Features"
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

새로운 LTS 버전인 JDK 17이 2021년 9월 15일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 17](https://openjdk.java.net/projects/jdk/17/)를 참고했습니다.

## Features

### JEP 306:  Restore Always-Strict Floating-Point Semantics

엄격한 부동 소수점 체계(strict floating-point semantics)와 미묘하게 다른 기본 부동 소수점 체계(default floating-point semantics)를 둘다 사용하기보다는 엄격한 부동 소수점 체계를 일관되게 사용합니다. 

이렇게 하면 Java SE 1.2에서 strict 및 default 부동 소수점 모드가 도입되기 전의 의미 체계와 일치하여 기존의 부동 소수점 의미 체계를 language 및 VM으로 복원합니다.

#### Goals

* `java.lang.Math` 및 `java.lang.StrictMath` 를 포함하여 수치에 민감한 라이브러리를 쉽게 개발할 수 있습니다.
* 부동 소수점을 다루는 플랫폼의 까다로운 측면에서 더 많은 규칙을 제공할 수 있습니다.

### JEP 356:	Enhanced Pseudo-Random Number Generators

점프 가능한(jumpable) PRNG 및 추가 클래스의 분할 가능한 PRNG 알고리즘(LXM)을 포함하여 의사 난수 생성기(PRNG)에 대한 새로운 인터페이스 유형 및 구현을 제공합니다.

#### Goals

* 응용 프로그램에서 다양한 PRNG 알고리즘을 서로 바꿔서 사용하기 쉽게 만듭니다.
* PRNG 개체의 스트림을 제공하여 스트림 기반 프로그래밍을 더 잘 지원합니다.
* 기존 PRNG 클래스에서 코드 중복을 제거합니다.
* `java.util.Random` 클래스의 기존 동작을 조심스럽게 보존하십시오.

### JEP 382:	New macOS Rendering Pipeline

더 이상 사용되지 않는 Apple OpenGL API를 사용하는 기존 파이프라인 대신 Apple Metal API를 사용하여 macOS용 Java 2D 내부 렌더링 파이프라인을 구현합니다.

#### Goals

* macOS Metal 프레임워크를 사용하는 Java 2D API를 위한 완전한 기능의 렌더링 파이프라인을 제공합니다.
* Apple이 향후 macOS 버전에서 더 이상 사용되지 않는 OpenGL API를 제거하는 경우에 대비하십시오.
* Java 애플리케이션에 대한 새 파이프라인의 투명성을 보장합니다.
* 기존 OpenGL 파이프라인으로 구현의 기능적 패리티를 확인합니다.
* 일부 실제 애플리케이션 및 벤치마크에서 OpenGL 파이프라인과 같거나 더 나은 성능을 제공합니다.
* 기존 Java 2D 파이프라인 모델에 맞는 깔끔한 아키텍처를 만듭니다.
* 더 이상 사용되지 않을 때까지 OpenGL 파이프라인과 공존합니다.

### JEP 391:	macOS/AArch64 Port

JDK를 macOS/AArch64로 이식합니다.

### JEP 398:	Deprecate the Applet API for Removal

더 이상 사용하지 않는 Applet API를 제거합니다. 

아래 Java API의 클래스 및 인터페이스를 더 이상 사용하지 않아 제거합니다.

* `java.applet.Applet`
* `java.applet.AppletStub`
* `java.applet.AppletContext`
* `java.applet.AudioClip`
* `javax.swing.JApplet`
* `java.beans.AppletInitializer`

다음의 메서드 및 필드를 포함하여 위의 클래스 및 인터페이스를 참조하는 모든 API 요소를 제거하기 위해 사용 중단합니다.

* `java.beans.Beans`
* `javax.swing.RepaintManager`
* `javax.naming.Context`

### JEP 403:	Strongly Encapsulate JDK Internals

`sun.misc.Unsafe`와 같은 중요한 내부 API를 제외하고 JDK의 모든 내부 요소를 강력하게 캡슐화합니다. JDK 9 ~ JDK 16에서 가능했던 것처럼 단일 명령줄 옵션(single command-line option)을 통해 내부 요소의 강력한 캡슐화를 완화하는 것은 더 이상 불가능합니다.

#### Goals

* Project Jigsaw의 주요 목표 중 하나인 JDK의 보안 및 유지 관리성을 지속적으로 개선합니다.
* 개발자가 내부 요소를 사용하는 것에서 표준 API를 사용하는 것으로 마이그레이션하도록 권장하여 개발자와 해당 사용자 모두가 차후 Java 릴리스로 번거롭지 않게 업그레이드할 수 있습니다.

#### Examples 

* JDK의 내부 API에 직접 액세스하는 이전 버전으로 릴리스로 성공적으로 컴파일된 코드는 더 이상 작동하지 않습니다.

```java
System.out.println(sun.security.util.SecurityConstants.ALL_PERMISSION);

Exception in thread "main" java.lang.IllegalAccessError: class Test
  (in unnamed module @0x5e481248) cannot access class
  sun.security.util.SecurityConstants (in module java.base) because
  module java.base does not export sun.security.util to unnamed
  module @0x5e481248
```

* 내보낸 `java.*` API의 개인 필드에 액세스하기 위해 리플렉션을 사용하는 코드가 더 이상 작동하지 않습니다.

```java
var ks = java.security.KeyStore.getInstance("jceks");
var f = ks.getClass().getDeclaredField("keyStoreSpi");
f.setAccessible(true);

Exception in thread "main" java.lang.reflect.InaccessibleObjectException:
  Unable to make field private java.security.KeyStoreSpi
  java.security.KeyStore.keyStoreSpi accessible: module java.base does
  not "opens java.security" to unnamed module @6e2c634b
```

* 내보낸 `java.*` API의 보호된 메소드를 호출하기 위해 리플렉션을 사용하는 코드는 더 이상 작동하지 않습니다.
  
```java
var dc = ClassLoader.class.getDeclaredMethod("defineClass",
                                             String.class,
                                             byte[].class,
                                             int.class,
                                             int.class);
dc.setAccessible(true);

Exception in thread "main" java.lang.reflect.InaccessibleObjectException:
  Unable to make protected final java.lang.Class
  java.lang.ClassLoader.defineClass(java.lang.String,byte[],int,int)
  throws java.lang.ClassFormatError accessible: module java.base does
  not "opens java.lang" to unnamed module @5e481248
```

### JEP 406:	Pattern Matching for switch (Preview)

패턴 언어에 대한 확장과 함께 스위치 표현식 및 명령문에 대한 패턴 일치로 Java 프로그래밍 언어를 향상시키십시오. 패턴 일치를 `switch`로 확장하면 각각 특정 작업을 가진 여러 패턴에 대해 표현식을 테스트할 수 있으므로 복잡한 데이터 지향 쿼리를 간결하고 안전하게 표현할 수 있습니다.

#### Goals

* `case` 레이블에 패턴이 나타나도록 하여 `switch` 식과 문의 표현력과 적용 가능성을 확장합니다.
* 원하는 경우 스위치의 역사적 null 적대감을 완화할 수 있습니다.
* 두 가지 새로운 유형의 패턴, 즉 임의의 부울 표현식으로 패턴 일치 논리를 구체화할 수 있도록 하는 보호된 패턴과 일부 구문 분석 모호성을 해결하기 위해 괄호로 묶인 패턴을 도입합니다.
* 기존의 모든 스위치 표현식과 문이 변경 사항 없이 계속 컴파일되고 동일한 의미로 실행되는지 확인합니다.
* 기존 스위치 구성과 별개인 패턴 일치 의미 체계를 사용하여 새로운 스위치와 유사한 표현이나 문을 도입하지 마십시오.
* 케이스 레이블이 패턴일 때와 케이스 레이블이 기존 상수일 때 스위치 표현식 또는 문이 다르게 작동하도록 하지 마십시오.

#### Motivation

Java 16은 `instanceof` 연산자를 확장하여 유형 패턴을 취하고 패턴 일치를 수행합니다. 이 확장을 통해 `instanceof-and-cast` 관용구를 단순화할 수 있습니다.

```java
/ Old code
if (o instanceof String) {
    String s = (String)o;
    ... use s ...
}

// New code
if (o instanceof String s) {
    ... use s ...
}
```

우리는 자주 `o`와 같은 변수를 여러 대안과 비교하기를 원합니다. Java는 `switch` 문 및 Java 14 이후로 `switch` 식(JEP 361)과의 다방향 비교를 지원하지만 불행히도 `switch`는 매우 제한적입니다. 숫자 유형, 열거형 및 문자열과 같은 몇 가지 유형의 값만 켤 수 있으며 상수와 정확히 같은지 테스트할 수만 있습니다. 패턴을 사용하여 여러 가능성에 대해 동일한 변수를 테스트하고 각각에 대해 특정 조치를 취하고 싶지만 기존 스위치가 이를 지원하지 않기 때문에 다음과 같은 일련의 `if...else` 테스트로 끝납니다.

```java
static String formatter(Object o) {
    String formatted = "unknown";
    if (o instanceof Integer i) {
        formatted = String.format("int %d", i);
    } else if (o instanceof Long l) {
        formatted = String.format("long %d", l);
    } else if (o instanceof Double d) {
        formatted = String.format("double %f", d);
    } else if (o instanceof String s) {
        formatted = String.format("String %s", s);
    }
    return formatted;
}
```

이 코드는 패턴 `instanceof` 표현식을 사용하는 이점이 있지만 완벽하지는 않습니다. 또한 위의 코드는 최적화할 수 없습니다. 기본 문제가 O(1)임에도 불구하고 O(n) 시간 복잡도를 갖습니다.

하지만 스위치는 패턴 매칭에 딱! 모든 유형에서 작동하도록 `switch` 문과 표현식을 확장하고 상수가 아닌 패턴이 있는 케이스 레이블을 허용하면 위의 코드를 보다 명확하고 안정적으로 다시 작성할 수 있습니다.

```java
static String formatterPatternSwitch(Object o) {
    return switch (o) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        default        -> o.toString();
    };
}
```

이 스위치의 의미는 명확합니다. 값이 패턴과 일치하는 경우 패턴이 있는 케이스 레이블은 선택기 표현식 `o`의 값과 일치합니다. (간단함을 위해 `switch` 표현식을 표시했지만 대신 `switch` 문을 표시할 수 있습니다. 케이스 레이블을 포함한 `switch` 블록은 변경되지 않습니다.), 또한 최적화가 가능하여 O(1) 시간에 디스패치를 수행할 수 있습니다.

##### Pattern matching and null

일반적으로 선택기 식이 `null`로 평가되면 `switch` 문과 식은 `NullPointerException`을 `throw`하므로 `null` 테스트는 스위치 외부에서 수행해야 합니다.

```java
static void testFooBar(String s) {
    if (s == null) {
        System.out.println("oops!");
        return;
    }
    switch (s) {
        case "Foo", "Bar" -> System.out.println("Great");
        default           -> System.out.println("Ok");
    }
}
```

이는 스위치가 몇 가지 참조 유형만 지원했을 때 합리적이었습니다. 그러나 스위치가 모든 유형의 선택기 표현을 허용하고 케이스 레이블에 유형 패턴이 있을 수 있는 경우 독립형 `null` 테스트는 임의적인 구별처럼 느껴지고 불필요한 상용구와 오류 기회를 불러옵니다. `null` 테스트를 스위치에 통합하는 것이 좋습니다.

```java
static void testFooBar(String s) {
    switch (s) {
        case null         -> System.out.println("Oops");
        case "Foo", "Bar" -> System.out.println("Great");
        default           -> System.out.println("Ok");
    }
}
```

선택기 표현식의 값이 `null`일 때 스위치의 동작은 항상 케이스 레이블에 의해 결정됩니다. 케이스가 null인 경우(또는 전체 유형 패턴, 아래 4a 참조) 스위치는 해당 레이블과 관련된 코드를 실행합니다. 케이스 null이 없으면 스위치는 이전과 마찬가지로 `NullPointerException`을 발생시킵니다. (스위치의 현재 의미와 하위 호환성을 유지하기 위해 기본 레이블은 null 선택기와 일치하지 않습니다.)

다른 케이스 레이블과 같은 방식으로 `null`을 처리하고 싶을 수도 있습니다. 예를 들어 다음 코드에서 `null`인 경우 `String s`는 `null` 값과 모든 `String` 값 모두와 일치합니다.

```java
static void testStringOrNull(Object o) {
    switch (o) {
        case null, String s -> System.out.println("String: " + s);
    }
}
```

##### Refining patterns in switch

스위치에서 패턴을 실험해보면 패턴을 다듬고 싶어하는 것이 일반적이라는 것을 알 수 있습니다. Shape 값을 전환하는 다음 코드를 고려하십시오.

```java
class Shape {}
class Rectangle extends Shape {}
class Triangle  extends Shape { int calculateArea() { ... } }

static void testTriangle(Shape s) {
    switch (s) {
        case null:
            break;
        case Triangle t:
            if (t.calculateArea() > 100) {
                System.out.println("Large triangle");
                break;
            }
        default:
            System.out.println("A shape, possibly a small triangle");
    }
}
```

이 코드의 목적은 큰 삼각형(100개 이상의 면적)에 대한 특별한 경우와 다른 모든 것(작은 삼각형 포함)에 대한 기본 사례를 갖는 것입니다. 그러나 우리는 이것을 하나의 패턴으로 직접 표현할 수 없습니다. 먼저 모든 삼각형과 일치하는 케이스 레이블을 작성한 다음 해당 명령문 그룹 내에서 다소 불편하게 삼각형 영역 테스트를 배치해야 합니다. 그런 다음 삼각형의 면적이 100보다 작을 때 올바른 동작을 얻기 위해 폴스루(fall-through)를 사용해야 합니다. (`if` 블록 내부에 `break`를 조심스럽게 배치해야 합니다.)

여기서 문제는 단일 패턴을 사용하여 케이스를 구별하는 것이 단일 조건 이상으로 확장되지 않는다는 것입니다. 패턴을 세련되게 표현할 방법이 필요합니다. 한 가지 접근 방식은 케이스 레이블을 정제할 수 있도록 하는 것입니다. 이러한 개선을 다른 프로그래밍 언어에서는 가드라고 합니다. 예를 들어 케이스 레이블 끝에 표시할 새 키워드를 도입하고 부울 표현식이 뒤따를 수 있습니다(예: `case Triangle t where t.calculateArea() > 100`).

그러나 더 표현적인 접근 방식이 있습니다. 케이스 레이블의 기능을 확장하는 대신 패턴 자체의 언어를 확장할 수 있습니다. 임의의 부울 표현식 `b`에 의해 패턴 `p`를 정제할 수 있도록 하는 보호된 패턴이라고 하는 `p && b`로 작성된 새로운 종류의 패턴을 추가할 수 있습니다.

이 접근 방식을 사용하면 `testTriangle` 코드를 큰 삼각형의 특별한 경우를 직접 표현할 수 있습니다. 이렇게 하면 `switch` 문에서 폴스루(fall-through)를 사용하지 않아도 되므로 간결한 화살표 스타일(`->`) 규칙을 사용할 수 있습니다.

```java
static void testTriangle(Shape s) {
    switch (s) {
        case Triangle t && (t.calculateArea() > 100) ->
            System.out.println("Large triangle");
        default ->
            System.out.println("A shape, possibly a small triangle");
    }
}
```

`s` 값은 먼저 유형 패턴 `Triangle t`와 일치하는 경우 패턴 `Triangle t &&(t.calculateArea() > 100)`와 일치하고, 일치하는 경우 표현식 `t.calculateArea() > 100`이 `true`로 평가됩니다.

스위치를 사용하면 애플리케이션 요구 사항이 변경될 때 케이스 레이블을 쉽게 이해하고 변경할 수 있습니다. 예를 들어 기본 경로에서 삼각형을 분할하고 싶을 수 있습니다. 정제된 패턴과 정제되지 않은 패턴을 모두 사용하여 이를 수행할 수 있습니다.

```java
static void testTriangle(Shape s) {
    switch (s) {
        case Triangle t && (t.calculateArea() > 100) ->
            System.out.println("Large triangle");
        case Triangle t ->
            System.out.println("Small triangle");
        default ->
            System.out.println("Non-triangle");
    }
}
```

#### Description

우리는 두 가지 방법으로 `switch` 문과 표현식을 향상시킵니다.

* 상수 외에 패턴을 포함하도록 케이스 레이블을 확장합니다.
* 보호된 패턴과 괄호로 묶인 패턴의 두 가지 새로운 유형의 패턴을 도입합니다.

제안의 핵심은 새로운 케이스 p 스위치 레이블을 도입하는 것입니다. 여기서 p는 패턴입니다. 그러나 스위치의 본질은 변경되지 않습니다. 선택기 표현식의 값이 스위치 레이블과 비교되고 레이블 중 하나가 선택되고 해당 레이블과 연결된 코드가 실행됩니다. 차이점은 이제 패턴이 있는 케이스 레이블의 경우 해당 선택이 동등성 검사가 아닌 패턴 일치에 의해 결정된다는 것입니다. 예를 들어 다음 코드에서 `o` 값은 `Long l` 패턴과 일치하고 `Long l` 케이스와 관련된 코드가 실행됩니다.

```java
Object o = 123L;
String formatted = switch (o) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> o.toString();
};
```

케이스 레이블에 패턴이 있을 수 있는 경우 네 가지 주요 디자인 문제가 있습니다.

1. Enhanced type checking
2. Completeness of switch expressions and statements
3. Scope of pattern variable declarations
4. Dealing with null

위 사항은 [JEP 406](https://openjdk.java.net/jeps/406) 에서 확인할 수 있습니다.

### JEP 407:	Remove RMI Activation

RMI의 나머지 부분은 유지하면서 RMI(Remote Method Invocation) 활성화 메커니즘을 제거합니다.

* Java SE API 사양에서 `java.rmi.activation` 패키지 제거
* RMI 활성화에 대한 언급을 제거하도록 RMI Specification 업데이트
* RMI 활성화 메커니즘을 구현하는 JDK 라이브러리 코드 제거
* RMI 활성화 메커니즘에 대한 JDK 회귀 테스트 제거
* JDK의 rmid 활성화 데몬 및 해당 문서를 제거합니다.

### JEP 409:	Sealed Classes

자세한 사항은 [JDK 15](/programming/java-newfeatures15), [JDK 16](/programming/java-newfeatures16) 을 확인하면됩니다.

봉인된 클래스와 인터페이스로 Java 프로그래밍 언어를 향상시키십시오. 봉인된 클래스 및 인터페이스는 다른 클래스 또는 인터페이스가 확장하거나 구현할 수 있는 것을 제한합니다.

#### Goals

* 클래스 또는 인터페이스 작성자가 구현을 담당하는 코드를 제어할 수 있도록 합니다.
* 슈퍼클래스(Super Class)의 사용을 제한하기 위해 Access Modifier 보다 더 선언적인 방법을 제공합니다.
* 패턴의 철저한 분석을 위한 기반을 제공하여 패턴 매칭의 미래 방향을 지원합니다.

### JEP 410:	Remove the Experimental AOT and JIT Compiler

실험적인 Java 기반 AOT(Ahead-of-Time) 및 JIT(Just-In-Time) 컴파일러를 제거합니다. 이 컴파일러는 도입 이후 거의 사용되지 않았으며 유지 관리에 필요한 노력이 상당합니다. 개발자가 JIT 컴파일을 위해 외부 빌드 버전의 컴파일러를 계속 사용할 수 있도록 실험적인 Java 수준 JVM 컴파일러 인터페이스(JVMCI)를 유지합니다.

#### Description

3개의 JDK 모듈을 제거합니다.

* `jdk.aot` — the jaotc tool
* `jdk.internal.vm.compiler` — the Graal compiler
* `jdk.internal.vm.compiler.management` — Graal's MBean

JVMCI 모듈(`jdk.internal.vm.ci`, [JEP 243](https://openjdk.java.net/jeps/243)이 계속 빌드되도록 다음 두 개의 Graal 관련 소스 파일을 유지합니다.

* `src/jdk.internal.vm.compiler/share/classes/module-info.java`
* `src/jdk.internal.vm.compiler.management/share/classes/module-info.java`

AOT 컴파일과 관련된 HotSpot 코드를 제거합니다.

* `src/hotspot/share/aot` — dumps and loads AOT code
* Additional code guarded by `#if INCLUDE_AOT`

마지막으로 Graal 및 AOT 컴파일과 관련된 makefile의 코드와 테스트를 제거합니다.

### JEP 411:	Deprecate the Security Manager for Removal

향후 릴리스에서 제거하기 위해 Security Manager를 더 이상 사용하지 않습니다. Security Manager는 Java 1.0부터 시작되었습니다. 수년 동안 클라이언트 측 Java 코드를 보호하는 주요 수단이 아니었으며 서버 측 코드를 보호하는 데 거의 사용되지 않았습니다. Java를 발전시키기 위해 레거시 Applet API(JEP 398)와 함께 제거하기 위해 Security Manager를 더 이상 사용하지 않습니다.

#### Goals

* Java의 차기 버전에서 보안 관리자 제거를 위해 개발자를 준비하십시오.
* Java 애플리케이션이 Security Manager에 의존하는 경우 사용자에게 경고합니다.
* `System::exit` 차단과 같이 Security Manager가 사용된 특정 좁은 사용 사례를 해결하기 위해 새로운 API 또는 메커니즘이 필요한지 여부를 평가하십시오.

### JEP 412:	Foreign Function & Memory API (Incubator)

Java 프로그램이 Java Runtime 외부의 코드와 데이터와 상호 운용 할 수있는 API를 소개합니다. 외부 함수 (즉, JVM 외부의 코드)를 효율적으로 호출하고 외부 메모리 (즉, JVM에서 관리하지 않는 메모리)를 안전하게 액세스함으로써 Java 프로그램을 사용하여 JNI의 취성 및 위험 없이. 원시 라이브러리를 호출하고 기본 데이터를 처리 할 수 있습니다.

#### Goals

* Ease of use - 우수한 순수 Java 개발 모델로 Java 기본 인터페이스 (JNI)를 교체하십시오.
* Performance - JNI 및 `sun.misc.Unsafe`와 같은 기존 API와 비슷하지 않은 성능을 제공합니다.
* Generality - 다른 종류의 외부 메모리 (예 : 기본 메모리, 영구 메모리 및 관리 힙 메모리) 및 시간이 지남에 따라 다른 플랫폼 (예 : 32 비트 x86) 및 다른 언어로 작성된 외부 함수를 수용 할 수있는 방법을 제공합니다. C (예 : C ++, Fortran)보다.
* Safety - 기본적으로 안전하지 않은 작업을 비활성화하여 응용 프로그램 개발자 또는 최종 사용자에서 명시적으로 선택한 후에만 허용됩니다.

#### Description

외부 함수 및 메모리 API (FFM API)는 라이브러리 및 응용 프로그램의 클라이언트 코드가 아래 사항들을 할 수 있습니다.

* Allocate foreign memory (MemorySegment, MemoryAddress, and SegmentAllocator),
* Manipulate and access structured foreign memory (MemoryLayout, MemoryHandles, and MemoryAccess),
* Manage the lifecycle of foreign resources (ResourceScope), and
* Call foreign functions (SymbolLookup and CLinker).

FFM API는 `jdk.incubator.foreign` 모듈의 `jdk.incubator.foreign` 패키지에 있습니다.

##### Example

FFM API를 사용하는 간단한 예제에서는 C 라이브러리 함수 RadixSort에 대한 메소드 핸들을 얻은 Java 코드이며 Java 배열에서 수명을 시작하는 4 개의 문자열을 정렬합니다.

```java
// 1. Find foreign function on the C library path
MethodHandle radixSort = CLinker.getInstance().downcallHandle(
                             CLinker.systemLookup().lookup("radixsort"), ...);
// 2. Allocate on-heap memory to store four strings
String[] javaStrings   = { "mouse", "cat", "dog", "car" };
// 3. Allocate off-heap memory to store four pointers
MemorySegment offHeap  = MemorySegment.allocateNative(
                             MemoryLayout.ofSequence(javaStrings.length,
                                                     CLinker.C_POINTER), ...);
// 4. Copy the strings from on-heap to off-heap
for (int i = 0; i < javaStrings.length; i++) {
    // Allocate a string off-heap, then store a pointer to it
    MemorySegment cString = CLinker.toCString(javaStrings[i], newImplicitScope());
    MemoryAccess.setAddressAtIndex(offHeap, i, cString.address());
}
// 5. Sort the off-heap data by calling the foreign function
radixSort.invoke(offHeap.address(), javaStrings.length, MemoryAddress.NULL, '\0');
// 6. Copy the (reordered) strings from off-heap to on-heap
for (int i = 0; i < javaStrings.length; i++) {
    MemoryAddress cStringPtr = MemoryAccess.getAddressAtIndex(offHeap, i);
    javaStrings[i] = CLinker.toJavaStringRestricted(cStringPtr);
}
assert Arrays.equals(javaStrings, new String[] {"car", "cat", "dog", "mouse"});  // true
```

##### Memory Segments

메모리 세그먼트는 오프 힙 또는 온 힙에 위치한 인접 메모리 영역을 모델링하는 추상화입니다. 메모리 세그먼트는 아래 사항들을 할 수 있습니다.

* Native segments, allocated from scratch in native memory (e.g., via malloc),
* Mapped segments, wrapped around a region of mapped native memory (e.g., via mmap), or
* Array or buffer segments, wrapped around memory associated with existing Java arrays or byte buffers, respectively.

모든 메모리 세그먼트는 메모리 역참조 작업을 안전하게 만들기 위해 강력하게 시행되는 공간, 시간 및 스레드 제한 보장을 제공합니다. 예를 들어 다음 코드는 100바이트 오프 힙을 할당합니다.

```java
MemorySegment segment = MemorySegment.allocateNative(100, newImplicitScope());
```

세그먼트의 공간 경계는 세그먼트와 관련된 메모리 주소 범위를 결정합니다. 위 코드의 세그먼트 경계는 `MemoryAddress` 인스턴스로 표현되는 기본 주소 `b`와 바이트(100) 단위의 크기로 정의되며, 결과적으로 `b`에서 `b + 99`까지의 주소 범위가 생성됩니다.

세그먼트의 시간적 경계는 세그먼트의 수명, 즉 세그먼트가 할당 해제되는 시기를 결정합니다. 세그먼트의 수명 및 스레드 제한 상태는 아래에서 설명하는 `ResourceScope` 추상화에 의해 모델링됩니다. 위 코드의 리소스 범위는 `MemorySegment` 개체가 가비지 수집기에 의해 도달할 수 없는 것으로 간주될 때 이 세그먼트와 연결된 메모리가 해제되도록 하는 새로운 암시적 범위입니다. 암시적 범위는 또한 여러 스레드에서 메모리 세그먼트에 액세스할 수 있도록 합니다.

즉, 위의 코드는 `assignDirect` 팩토리로 할당된 `ByteBuffer`의 동작과 거의 일치하는 동작을 갖는 세그먼트를 생성합니다. FFM API는 아래에서 설명하는 결정적 메모리 해제 및 기타 스레드 제한 옵션도 지원합니다.

##### Dereferencing memory segments

세그먼트와 관련된 메모리의 역참조는 Java 9에서 도입된 데이터 액세스에 대한 추상화인 var 핸들을 얻어서 달성됩니다. 특히, 세그먼트는 `memory-access var handle`로 역참조됩니다. 이러한 종류의 var 핸들은 한 쌍의 액세스 좌표를 사용합니다.

* `MemorySegment` 유형의 좌표 — 메모리가 역참조되는 세그먼트
* `long` 유형의 좌표 — 역참조가 발생하는 세그먼트의 기본 주소로부터의 오프셋

메모리 액세스 var 핸들은 `MemoryHandles` 클래스의 팩토리 메서드를 통해 얻습니다. 예를 들어 이 코드는 기본 메모리 세그먼트에 `int` 값을 쓸 수 있는 메모리 액세스 var 핸들을 얻고 이를 사용하여 연속 오프셋에 25개의 4바이트 값을 씁니다.

```java
MemorySegment segment = MemorySegment.allocateNative(100, newImplicitScope());
VarHandle intHandle = MemoryHandles.varHandle(int.class, ByteOrder.nativeOrder());
for (int i = 0; i < 25; i++) {
    intHandle.set(segment, /* offset */ i * 4, /* value to write */ i);
}
```

`MemoryHandles` 클래스에서 제공하는 하나 이상의 결합자 메서드를 사용하여 메모리 액세스 var 핸들을 결합하여 고급 액세스 관용구를 표현할 수 있습니다. 이를 통해 클라이언트는 예를 들어 주어진 메모리 액세스 var 핸들의 좌표를 재정렬하고 하나 이상의 좌표를 삭제하고 새 좌표를 삽입할 수 있습니다. 이를 통해 플랫 오프 힙 메모리 영역이 지원하는 다차원 배열로 하나 이상의 논리적 인덱스를 허용하는 메모리 액세스 var 핸들을 생성할 수 있습니다.

FFM API를 보다 쉽게 ​​접근할 수 있도록 `MemoryAccess` 클래스는 메모리 액세스 var 핸들을 구성할 필요 없이 메모리 세그먼트를 역참조하는 정적 접근자를 제공합니다. 예를 들어, 주어진 오프셋에서 세그먼트의 int 값을 설정하는 접근자가 있어 위의 코드를 다음과 같이 단순화할 수 있습니다.

```java
MemorySegment segment = MemorySegment.allocateNative(100, newImplicitScope());
for (int i = 0; i < 25; i++) {
    MemoryAccess.setIntAtOffset(segment, i * 4, i);
}
```

##### Memory layouts

메모리 레이아웃(예: 위의 예에서 `i * 4`)에 대한 지루한 계산의 필요성을 줄이기 위해 `MemoryLayout`을 사용하여 메모리 세그먼트의 내용을 보다 선언적인 방식으로 설명할 수 있습니다. 예를 들어, 위의 예에서 기본 메모리 세그먼트의 원하는 레이아웃은 다음과 같은 방식으로 설명될 수 있습니다.

```java
SequenceLayout intArrayLayout
    = MemoryLayout.sequenceLayout(25,
        MemoryLayout.valueLayout(32, ByteOrder.nativeOrder()));
```

이것은 32비트 값 레이아웃(단일 32비트 값을 설명하는 레이아웃)이 25번 반복되는 시퀀스 메모리 레이아웃을 생성합니다. 메모리 레이아웃이 주어지면 코드에서 오프셋 계산을 피하고 메모리 할당과 메모리 액세스 var 핸들 생성을 단순화할 수 있습니다.

```java
MemorySegment segment = MemorySegment.allocateNative(intArrayLayout, newImplicitScope());
VarHandle indexedElementHandle =
    intArrayLayout.varHandle(int.class, PathElement.sequenceElement());
for (int i = 0; i < intArrayLayout.elementCount().getAsLong(); i++) {
    indexedElementHandle.set(segment, (long) i, i);
}
```

`intArrayLayout` 객체는 복잡한 레이아웃 표현식에서 중첩 레이아웃을 선택하는 데 사용되는 레이아웃 경로 생성을 통해 메모리 액세스 var 핸들 생성을 유도합니다. `intArrayLayout` 객체는 또한 레이아웃에서 파생된 크기 및 정렬 정보를 기반으로 하는 기본 메모리 세그먼트의 할당을 구동합니다. 이전 예제의 루프 상수인 25는 시퀀스 레이아웃의 엘리먼트 수로 대체되었습니다.

##### Resource scopes

이전 예에서 본 모든 메모리 세그먼트는 비결정적 할당 해제를 사용합니다. 이러한 세그먼트와 연결된 메모리는 메모리 세그먼트 인스턴스에 연결할 수 없게 되면 가비지 수집기에 의해 할당이 해제됩니다. 우리는 그러한 세그먼트가 암시적으로 할당 해제되었다고 말합니다.

클라이언트가 메모리 할당 해제가 발생하는 시기를 제어하려는 경우가 있습니다. 예를 들어 큰 메모리 세그먼트가 `MemorySegment::map`을 사용하여 파일에서 매핑된다고 가정합니다. 클라이언트는 가비지 수집기가 그렇게 할 때까지 기다리는 것보다 세그먼트가 더 이상 필요하지 않은 즉시 세그먼트와 연결된 메모리를 해제(즉, 매핑 해제)하는 것을 선호할 수 있습니다. 대기는 애플리케이션의 성능에 부정적인 영향을 미칠 수 있기 때문입니다.

메모리 세그먼트는 리소스 범위를 통해 결정적 할당 해제를 지원합니다. 리소스 범위는 메모리 세그먼트와 같은 하나 이상의 리소스와 연결된 수명 주기를 모델링합니다. 새로 생성된 리소스 범위는 활성 상태이므로 관리하는 모든 리소스에 안전하게 액세스할 수 있습니다. 클라이언트의 요청에 따라 리소스 범위를 닫을 수 있습니다. 즉, 해당 범위에서 관리하는 리소스에 대한 액세스가 더 이상 허용되지 않습니다. `ResourceScope` 클래스는 리소스 범위가 `try-with-resources` 문과 함께 작동하도록 `AutoCloseable` 인터페이스를 구현합니다.

```java
try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    MemorySegment s1 = MemorySegment.map(Path.of("someFile"), 0, 100000,
                                         MapMode.READ_WRITE, scope);
    MemorySegment s2 = MemorySegment.allocateNative(100, scope);
    ...
} // both segments released here
```

이 코드는 제한된 리소스 범위를 만들고 매핑된 세그먼트(`s1`)와 기본 세그먼트(`s2`)의 두 세그먼트를 만드는 데 사용합니다. 두 세그먼트의 수명 주기는 리소스 범위의 수명과 연결되어 있으므로 `try-with-resources` 문이 완료된 후 세그먼트에 액세스(예: 메모리 액세스 var 핸들로 역참조)하면 런타임 예외가 발생합니다.

메모리 세그먼트의 수명을 관리하는 것 외에도 리소스 범위는 세그먼트에 액세스할 수 있는 스레드를 제어하는 수단으로도 사용됩니다. 제한된 리소스 범위는 범위를 만든 스레드에 대한 액세스를 제한하는 반면 공유 리소스 범위는 모든 스레드에서 액세스를 허용합니다.

리소스 범위는 제한되거나 공유되는지 여부에 관계없이 클라이언트에서 닫기 메서드를 호출하기 전에 리소스 범위 개체에 연결할 수 없는 경우 암시적 할당 해제 수행을 처리하는 `java.lang.ref.Cleaner` 개체와 연관될 수 있습니다.

암시적 리소스 범위라고 하는 일부 리소스 범위는 명시적 할당 해제를 지원하지 않습니다. 닫기 호출은 실패합니다. 암시적 리소스 범위는 항상 클리너를 사용하여 리소스를 관리합니다. 암시적 범위는 이전 예제와 같이 `ResourceScope::newImplicitScope` 팩토리를 사용하여 생성할 수 있습니다

##### Segment allocators

클라이언트가 오프 힙 메모리를 사용할 때 메모리 할당은 종종 병목 현상이 될 수 있습니다. FFM API에는 메모리 세그먼트를 할당하고 초기화하는 유용한 작업을 정의하는 `SegmentAllocator` 추상화가 포함되어 있습니다. 세그먼트 할당자는 `SegmentAllocator` 인터페이스의 팩토리를 통해 얻습니다. 예를 들어 다음 코드는 아레나 기반 할당자를 만들고 이를 사용하여 Java `int` 배열에서 콘텐츠가 초기화된 세그먼트를 할당합니다.

```java
try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    SegmentAllocator allocator = SegmentAllocator.arenaAllocator(scope);
    for (int i = 0 ; i < 100 ; i++) {
        MemorySegment s = allocator.allocateArray(C_INT, new int[] { 1, 2, 3, 4, 5 });
        ...
    }
    ...
} // all memory allocated is released here
```

이 코드는 제한된 리소스 범위를 만든 다음 해당 범위와 연결된 무제한 할당자(`unbounded arena allocator`)를 만듭니다. 이 할당자는 특정 크기의 메모리 슬랩을 할당하고 사전 할당된 슬랩의 다른 조각을 반환하여 할당 요청에 응답합니다. 슬래브에 새 할당 요청을 수용할 충분한 공간이 없으면 새 슬래브가 할당됩니다. 아레나 할당자와 연결된 리소스 범위가 닫히면 할당자가 생성한 세그먼트(예: for 루프의 본문)와 연결된 모든 메모리가 원자적으로 할당 해제됩니다. 이 관용구는 `ResourceScope` 추상화에서 제공하는 결정적 할당 해제의 이점을 보다 유연하고 확장 가능한 할당 체계와 결합합니다. 많은 수의 오프 힙 세그먼트를 관리하는 코드를 작성할 때 매우 유용할 수 있습니다.

##### Unsafe memory segments

지금까지 메모리 세그먼트, 메모리 주소 및 메모리 레이아웃을 살펴보았습니다. 역참조 연산은 메모리 세그먼트에서만 가능합니다. 메모리 세그먼트에는 공간적 및 시간적 경계가 있으므로 Java 런타임은 항상 주어진 세그먼트와 연관된 메모리가 안전하게 역참조되도록 할 수 있습니다. 그러나 네이티브 코드와 상호 작용할 때 자주 발생하는 것처럼 클라이언트에 `MemoryAddress` 인스턴스만 있을 수 있는 상황이 있습니다. Java 런타임은 메모리 주소와 관련된 공간 및 시간 경계를 알 수 있는 방법이 없으므로 FFM API에서 메모리 주소를 직접 역참조하는 것을 금지합니다.

메모리 주소를 역참조하기 위해 클라이언트에는 두 가지 옵션이 있습니다.

* 주소가 메모리 세그먼트 내에 있는 것으로 알려진 경우 클라이언트는 `MemoryAddress::segmentOffset`을 통해 `rebase` 작업을 수행할 수 있습니다.
* 또는 그러한 세그먼트가 존재하지 않는 경우 클라이언트는 `MemoryAddress::asSegment` 팩토리를 사용하여 안전하지 않게 세그먼트를 생성할 수 있습니다.

##### Looking up foreign functions

외부 함수 지원의 첫 번째 요소는 네이티브 라이브러리를 로드하는 메커니즘입니다. JNI를 사용하면 `dlopen` 또는 이에 상응하는 호출에 내부적으로 매핑되는 `System::loadLibrary` 및 `System::load` 메서드를 사용하여 이 작업을 수행합니다. 이러한 메소드를 사용하여 로드된 라이브러리는 항상 클래스 로더(즉, 시스템 메소드를 호출한 클래스의 로더)와 연관됩니다. 라이브러리와 클래스 로더 간의 연결은 로드된 라이브러리의 수명 주기를 제어하기 때문에 중요합니다. 클래스 로더에 더 이상 연결할 수 없는 경우에만 해당 라이브러리의 모든 라이브러리를 안전하게 언로드할 수 있습니다.

FFM API는 네이티브 라이브러리를 로드하기 위한 새로운 방법을 제공하지 않습니다. 개발자는 `System::loadLibrary` 및 `System::load` 메서드를 사용하여 FFM API를 통해 호출될 네이티브 라이브러리를 로드합니다. 라이브러리와 클래스 로더 간의 연결이 유지되므로 라이브러리는 JNI와 동일한 예측 가능한 방식으로 언로드됩니다.

FFM API는 JNI와 달리 로드된 라이브러리에서 지정된 기호의 주소를 찾는 기능을 제공합니다. SymbolLookup 객체로 표시되는 이 기능은 Java 코드를 외부 기능에 연결하는 데 중요합니다(아래 참조). `SymbolLookup` 객체를 얻는 방법에는 두 가지가 있습니다.

* `SymbolLookup::loaderLookup` 은 현재 클래스 로더에 의해 로드된 모든 라이브러리의 모든 기호를 보는 기호 조회를 반환합니다.
* `CLinker::systemLookup` 은 표준 C 라이브러리에서 기호를 보는 플랫폼별 기호 조회를 반환합니다.

기호 조회가 주어지면 클라이언트는 `SymbolLookup::lookup(String)` 메서드를 사용하여 외부 함수를 찾을 수 있습니다. 명명된 함수가 기호 조회에 의해 표시되는 기호 사이에 있는 경우 메서드는 함수의 진입점을 가리키는 `MemoryAddress`를 반환합니다. 예를 들어 다음 코드는 OpenGL 라이브러리를 로드하고(현재 클래스 로더와 연결되도록 함) 해당 `glGetString` 함수의 주소를 찾습니다.

```java
System.loadLibrary("GL");
SymbolLookup loaderLookup  = SymbolLookup.loaderLookup();
MemoryAddress clangVersion = loaderLookup.lookup("glGetString").get();
```

##### Linking Java code to foreign functions

CLinker 인터페이스는 Java 코드가 네이티브 코드와 상호 운용되는 방식의 핵심입니다. CLinker는 Java와 C 라이브러리 간의 상호 운용성을 제공하는 데 중점을 두고 있지만 인터페이스의 개념은 향후 Java가 아닌 다른 언어를 지원하기에 충분히 일반적입니다. 인터페이스는 하향 호출(Java 코드에서 원시 코드로의 호출)과 상향 호출(기본 코드에서 Java 코드로 다시 호출)을 모두 가능하게 합니다.

```java
interface CLinker {
    MethodHandle downcallHandle(MemoryAddress func,
                                MethodType type,
                                FunctionDescriptor function);
    MemoryAddress upcallStub(MethodHandle target,
                             FunctionDescriptor function,
                             ResourceScope scope);
}
```

다운콜의 경우 `downcallHandle` 메소드는 외부 함수의 주소(일반적으로 라이브러리 조회에서 얻은 `MemoryAddress`)를 사용하고 외부 함수를 다운콜 메소드 핸들로 노출합니다. 나중에 Java 코드는 `invokeExact` 메소드를 호출하여 다운콜 메소드 핸들을 호출하고 외부 함수가 실행됩니다. 메서드 핸들의 `invokeExact` 메서드에 전달된 모든 인수는 외부 함수에 전달됩니다.

상향 호출의 경우 `upcallStub` 메소드는 메소드 핸들(일반적으로 하향 호출 메소드 핸들이 아닌 Java 메소드를 참조하는 핸들)을 가져와 메모리 주소로 변환합니다. 나중에 Java 코드가 다운콜 메소드 핸들을 호출할 때 메모리 주소가 인수로 전달됩니다. 실제로 메모리 주소는 함수 포인터 역할을 합니다. (업콜에 대한 자세한 내용은 아래를 참조하세요.)

Java에서 표준 C 라이브러리에 정의된 `strlen` 함수로 다운콜하기를 원한다고 가정합니다.

```cpp
size_t strlen(const char *s);
```

`strlen`을 노출하는 다운콜 메서드 핸들은 다음과 같이 얻을 수 있습니다(`MethodType` 및 `FunctionDescriptor`에 대한 자세한 내용은 곧 설명됨).

```java
MethodHandle strlen = CLinker.getInstance().downcallHandle(
    CLinker.systemLookup().lookup("strlen").get(),
    MethodType.methodType(long.class, MemoryAddress.class),
    FunctionDescriptor.of(C_LONG, C_POINTER)
);
```

다운콜 메소드 핸들을 호출하면 `strlen`이 실행되고 그 결과를 Java에서 사용할 수 있습니다. `strlen`에 대한 인수의 경우 도우미 메서드를 사용하여 Java 문자열을 오프힙 메모리 세그먼트로 변환하고 해당 세그먼트의 주소를 전달합니다.

```java
MemorySegment str = CLinker.toCString("Hello", newImplicitScope());
long len          = strlen.invokeExact(str.address());  // 5
```

JVM이 이미 네이티브 코드까지 메소드 핸들 호출을 최적화하기 때문에 메소드 핸들은 외부 기능을 노출하는 데 적합합니다. 메서드 핸들이 클래스 파일의 메서드를 참조할 때 메서드 핸들을 호출하면 일반적으로 대상 메서드가 JIT 컴파일됩니다. 이후 JVM은 대상 메소드에 대해 생성된 어셈블리 코드에 제어를 전송하여 `MethodHandle::invokeExact`를 호출하는 Java 바이트 코드를 해석합니다. 따라서 기존 메서드 핸들을 호출하는 것은 이미 준외부 호출입니다. C 라이브러리의 함수를 대상으로 하는 다운콜 메서드 핸들은 메서드 핸들의 좀 더 낯선 형태일 뿐입니다. 메서드 핸들은 또한 기본 인수를 사용하여 상자 없는 호출을 허용하는 서명 다형성이라는 속성을 즐깁니다. 요약하자면, 메서드 핸들을 사용하면 CLinker가 외부 기능을 자연스럽고 효율적이며 확장 가능한 방식으로 노출할 수 있습니다.

##### Describing C types in Java

다운콜 메서드 핸들을 생성하기 위해 FFM API는 클라이언트가 대상 C 함수의 두가지 측면을 제공해야 합니다. Java 객체(`MemoryAddress`, `MemorySegment`) 및 투명한 Java 객체(`MemoryLayout`)를 사용하는 저수준 서명.

* 상위 수준 서명인 `MethodType`은 다운콜 메서드 핸들의 유형으로 사용됩니다. 모든 메서드 핸들에는 강력한 형식이 지정되어 있어 `invokeExact` 메서드에 전달할 수 있는 인수의 수와 유형이 엄격합니다. 예를 들어, 하나의 `MemoryAddress` 인수를 사용하도록 생성된 메서드 핸들은 `invokeExact(<MemoryAddress>, <MemoryAddress>)` 또는 `invokeExact("Hello")`를 통해 호출될 수 없습니다. 따라서 `MethodType`은 클라이언트가 다운콜 메소드 핸들을 호출할 때 사용해야 하는 Java 서명을 설명합니다. 이것은 사실상 C 함수의 Java 보기입니다.
* 하위 수준 서명인 `FunctionDescriptor`는 `MemoryLayout` 개체로 구성됩니다. 이를 통해 CLinker는 C 함수의 인수를 정확하게 이해하여 아래 설명된 대로 적절하게 정렬할 수 있습니다. 클라이언트는 일반적으로 외부 메모리의 데이터를 역참조하기 위해 `MemoryLayout` 객체를 가지고 있으며 이러한 객체는 여기에서 외부 함수 서명으로 재사용될 수 있습니다.

예를 들어 `int`를 취하고 `long`을 반환하는 C 함수에 대한 하향 호출 메서드 핸들을 얻으려면 `downcallHandle에` 다음과 같은 `MethodType` 및 `FunctionDescriptor` 인수가 필요합니다.

```java
MethodType mtype         = MethodType.methodType(long.class, int.class);
FunctionDescriptor fdesc = FunctionDescriptor.of(C_LONG, C_INT);
```

(이 예는 Linux/x64 및 macOS/x64를 대상으로 합니다. 여기서 Java 유형 `long` 및 `int`는 각각 사전 정의된 CLinker 레이아웃 `C_LONG` 및 `C_INT`와 연관됩니다. Java 유형과 메모리 레이아웃의 연관은 플랫폼에 따라 다릅니다(예: Windows/x64에서). , Java `long`은 `C_LONG_LONG` 레이아웃과 연결됩니다.)

또 다른 예로 포인터를 사용하는 void C 함수에 대한 다운콜 메서드 핸들을 얻으려면 다음과 같은 MethodType 및 FunctionDescriptor가 필요합니다.

```java
MethodType mtype         = MethodType.methodType(void.class, MemoryAddress.class);
FunctionDescriptor fdesc = FunctionDescriptor.ofVoid(C_POINTER);
```

(C의 모든 포인터 유형은 Java에서 `MemoryAddress` 객체로 표현됩니다. 현재 플랫폼에 따라 크기가 달라지는 해당 레이아웃은 `C_POINTER`입니다. 클라이언트는 예를 들어 `int*`와 `char**`를 구분하지 않습니다. Java 유형과 메모리가 CLinker에 전달된 레이아웃에는 Java 인수를 C 함수에 올바르게 전달하기에 충분한 정보가 함께 포함되어 있습니다.)

마지막으로 JNI와 달리 CLinker는 구조화된 데이터를 외부 함수에 전달하는 것을 지원합니다. 구조체를 사용하는 void C 함수에 대한 하향 호출 메서드 핸들을 얻으려면 다음과 같은 `MethodType` 및 `FunctionDescriptor`가 필요합니다.

```java
MethodType mtype         = MethodType.methodType(void.class, MemorySegment.class);
MemoryLayout SYSTEMTIME  = MemoryLayout.ofStruct(
  C_SHORT.withName("wYear"),      C_SHORT.withName("wMonth"),
  C_SHORT.withName("wDayOfWeek"), C_SHORT.withName("wDay"),
  C_SHORT.withName("wHour"),      C_SHORT.withName("wMinute"),
  C_SHORT.withName("wSecond"),    C_SHORT.withName("wMilliseconds")
);
FunctionDescriptor fdesc = FunctionDescriptor.ofVoid(SYSTEMTIME);
```

(고수준 `MethodType` 서명의 경우 Java 클라이언트는 항상 C 함수가 값으로 전달된 구조체를 예상하는 불투명 유형 `MemorySegment`를 사용합니다. 하위 수준 `FunctionDescriptor` 서명의 경우 C 구조체 유형과 연결된 메모리 레이아웃은 복합 형식이어야 합니다. 네이티브 컴파일러가 삽입할 수 있는 패딩을 포함하여 C 구조체의 모든 필드에 대한 하위 레이아웃을 정의하는 레이아웃입니다.)

C 함수가 저수준 서명으로 표현되는 값별 구조체를 반환하는 경우 새로운 메모리 세그먼트는 오프 힙에 할당되고 Java 클라이언트에 반환되어야 합니다. 이를 달성하려면 `downcallHandle`에서 반환된 메서드 핸들에 추가 `SegmentAllocator` 인수가 필요합니다. 이 인수는 FFM API가 C 함수에서 반환된 구조체를 보유하기 위해 메모리 세그먼트를 할당하는 데 사용합니다.

##### Packaging Java arguments for C functions

다른 언어 간의 상호 운용에는 한 언어의 코드가 다른 언어의 함수를 호출하는 방법, 인수를 전달하는 방법 및 결과를 받는 방법을 지정하는 호출 규칙이 필요합니다. CLinker 구현에는 Linux/x64, Linux/AArch64, macOS/x64 및 Windows/x64와 같은 몇 가지 기본 호출 규칙에 대한 지식이 있습니다. Java로 작성되었기 때문에 호출 규칙이 HotSpot의 C++ 코드에 내장되어 있는 JNI보다 유지 관리 및 확장이 훨씬 쉽습니다.

`SYSTEMTIME` 구조체 및 레이아웃에 대해 위에 표시된 함수 설명자를 고려하십시오. JVM이 실행되는 OS 및 CPU의 호출 규칙이 주어지면 CLinker는 함수 설명자를 사용하여 `MemorySegment` 인수로 다운콜 메소드 핸들이 호출될 때 구조체의 필드가 C 함수에 전달되어야 하는 방법을 유추합니다. 하나의 호출 규칙에 대해 CLinker는 들어오는 메모리 세그먼트를 분해하고 일반 CPU 레지스터를 사용하여 처음 4개 필드를 전달하고 C 스택의 나머지 필드를 전달하도록 정렬할 수 있습니다. 다른 호출 규칙의 경우 CLinker는 메모리 영역을 할당하고 들어오는 메모리 세그먼트의 내용을 해당 영역으로 대량 복사하고 해당 메모리 영역에 대한 포인터를 C에 전달하여 FFM API가 구조체를 간접적으로 전달하도록 정렬할 수 있습니다. 기능. 이 가장 낮은 수준의 인수 패키징은 클라이언트 코드의 감독 없이 배후에서 발생합니다.

##### Upcalls

때로는 Java 코드를 외부 함수에 대한 함수 포인터로 전달하는 것이 유용합니다. 상향 호출에 대한 CLinker 지원을 사용하여 이를 달성할 수 있습니다. 이 섹션에서는 Java/Native 경계에서 코드와 데이터의 완전한 양방향 상호 운용을 통해 CLinker의 전체 기능을 보여주는 보다 정교한 예제를 하나씩 빌드합니다.

표준 C 라이브러리에 정의된 다음 함수를 고려하십시오.

```cpp
void qsort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
```

Java에서 `qsort`를 호출하려면 먼저 다운콜 메소드 핸들을 생성해야 합니다.

```java
MethodHandle qsort = CLinker.getInstance().downcallHandle(
    CLinker.systemLookup().lookup("qsort").get(),
    MethodType.methodType(void.class, MemoryAddress.class, long.class,
                          long.class, MemoryAddress.class),
    FunctionDescriptor.ofVoid(C_POINTER, C_LONG, C_LONG, C_POINTER)
);
```

이전과 같이 `C_LONG` 및 `long.class`를 사용하여 C `size_t` 유형을 매핑하고 첫 번째 포인터 매개변수(배열 포인터)와 마지막 매개변수(함수 포인터)에 대해 `MemoryAddess.class`를 사용합니다.

`qsort`는 함수 포인터로 전달된 사용자 정의 비교기 함수 `compare`를 사용하여 배열의 내용을 정렬합니다. 따라서 다운콜 메서드 핸들을 호출하려면 메서드 핸들의 `invokeExact` 메서드에 마지막 매개변수로 전달할 함수 포인터가 필요합니다. `CLinker::upcallStub`는 다음과 같이 기존 메서드 핸들을 사용하여 함수 포인터를 만드는 데 도움이 됩니다.

먼저, 간접적으로 `MemoryAddress` 객체로 표현되는 두 개의 긴 값을 비교하는 정적 메서드를 Java로 작성합니다

```java
class Qsort {
    static int qsortCompare(MemoryAddress addr1, MemoryAddress addr2) {
        return MemoryAccess.getIntAtOffset(MemorySegment.globalNativeSegment(),
                                           addr1.toRawLongValue()) -
               MemoryAccess.getIntAtOffset(MemorySegment.globalNativeSegment(),
                                           addr2.toRawLongValue());
    }
}
```

두 번째로 Java 비교기 메서드를 가리키는 메서드 핸들을 만듭니다.

```java
MethodHandle comparHandle
    = MethodHandles.lookup()
                   .findStatic(Qsort.class, "qsortCompare",
                               MethodType.methodType(int.class,
                                                     MemoryAddress.class,
                                                     MemoryAddress.class));
```

셋째, Java 비교기에 대한 메서드 핸들이 있으므로 `CLinker::upcallStub`를 사용하여 함수 포인터를 만들 수 있습니다. 다운콜의 경우와 마찬가지로 CLinker 클래스의 레이아웃을 사용하여 함수 포인터의 서명을 설명합니다.

```java
MemoryAddress comparFunc =
  CLinker.getInstance().upcallStub(comparHandle,
                                   FunctionDescriptor.of(C_INT,
                                                         C_POINTER,
                                                         C_POINTER),
                                   newImplicitScope());
);
```

마지막으로 메모리 주소 `comparFunc`가 있습니다. 이 주소는 Java 비교기 기능을 호출하는 데 사용할 수 있는 스텁을 가리키므로 이제 `qsort` 다운콜 핸들을 호출하는 데 필요한 모든 것이 있습니다.

```java
MemorySegment array = MemorySegment.allocateNative(4 * 10, newImplicitScope());
array.copyFrom(MemorySegment.ofArray(new int[] { 0, 9, 3, 4, 6, 5, 1, 8, 2, 7 }));
qsort.invokeExact(array.address(), 10L, 4L, comparFunc);
int[] sorted = array.toIntArray(); // [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
```

이 코드는 오프 힙 배열을 만들고 Java 배열의 내용을 복사한 다음 CLinker에서 얻은 비교기 함수와 함께 배열을 `qsort` 핸들에 전달합니다. 호출 후 오프 힙 배열의 내용은 Java로 작성된 비교기 기능에 따라 정렬됩니다. 그런 다음 정렬된 요소가 포함된 세그먼트에서 새 Java 배열을 추출합니다.

### JEP 414:	Vector API (Second Incubator)

VectorAPI에 대한 자세한 사항은 [JDK 16](/programming/java-newfeatures16)에서 확인 가능합니다.

지원되는 CPU 아키텍처에서 최적의 벡터 명령어로 런타임에 안정적으로 컴파일되는 벡터 계산을 표현하는 API를 도입하여 동등한 스칼라 계산보다 우수한 성능을 달성합니다.

##### Run-time compilation

Vector API에는 두 가지 구현이 있습니다. 첫 번째는 Java로 작업을 구현하므로 기능적이지만 최적은 아닙니다. 두 번째는 HotSpot C2 런타임 컴파일러에 대한 고유 벡터 연산을 정의하여 사용 가능한 경우 적절한 하드웨어 레지스터 및 벡터 명령어로 벡터 계산을 컴파일할 수 있도록 합니다.

C2 내장 함수의 폭발을 피하기 위해 수행할 특정 작업을 설명하는 매개변수를 사용하는 단항, 이진, 변환 등과 같은 다양한 종류의 작업에 해당하는 일반화된 내장 함수를 정의합니다. 약 20개의 새로운 내장 기능이 전체 API의 내장 기능을 지원합니다.

JEP 401(Primitive Objects)에서 Project Valhalla가 제안한 대로 궁극적으로 벡터 클래스를 기본 클래스로 선언할 것으로 예상합니다. 그동안 `Vector<E>` 및 해당 하위 클래스는 값 기반 클래스로 간주되므로 해당 인스턴스에서 ID에 민감한 작업은 피해야 합니다. 벡터 인스턴스는 추상적으로 레인의 요소로 구성되지만 이러한 요소는 C2에 의해 스칼라화되지 않습니다. 벡터의 값은 적절한 크기의 벡터 레지스터에 매핑되는 `int` 또는 `long`과 같은 전체 단위로 처리됩니다. 벡터 인스턴스는 탈출 분석의 한계를 극복하고 boxing을 피하기 위해 C2에서 특별히 처리됩니다.

##### Run-time compilation

Vector API에는 두 가지 구현이 있습니다. 첫 번째는 Java로 작업을 구현하므로 기능적이지만 최적은 아닙니다. 두 번째는 HotSpot C2 런타임 컴파일러에 대한 고유 벡터 연산을 정의하여 사용 가능한 경우 적절한 하드웨어 레지스터 및 벡터 명령어로 벡터 계산을 컴파일할 수 있도록 합니다.

C2 내장 함수의 폭발을 피하기 위해 수행할 특정 작업을 설명하는 매개변수를 사용하는 단항, 이진, 변환 등과 같은 다양한 종류의 작업에 해당하는 일반화된 내장 함수를 정의합니다. 약 20개의 새로운 내장 기능이 전체 API의 내장 기능을 지원합니다.

JEP 401(Primitive Objects)에서 Project Valhalla가 제안한 대로 궁극적으로 벡터 클래스를 기본 클래스로 선언할 것으로 예상합니다. 그동안 `Vector<E>` 및 해당 하위 클래스는 값 기반 클래스로 간주되므로 해당 인스턴스에서 ID에 민감한 작업은 피해야 합니다. 벡터 인스턴스는 추상적으로 레인의 요소로 구성되지만 이러한 요소는 C2에 의해 스칼라화되지 않습니다. 벡터의 값은 적절한 크기의 벡터 레지스터에 매핑되는 `int` 또는 `long`과 같은 전체 단위로 처리됩니다. 벡터 인스턴스는 탈출 분석의 한계를 극복하고 boxing을 피하기 위해 C2에서 특별히 처리됩니다.

##### Intel SVML intrinsics for transcendental operations

Vector API는 부동 소수점 벡터에 대한 초월 및 삼각 레인별 연산을 지원합니다. x64에서 인텔 SVML(Short Vector Math Library)을 활용하여 이러한 작업에 최적화된 내장 구현을 제공합니다. 내장 연산은 `java.lang.Math`에 정의된 해당 스칼라 연산과 동일한 수치 속성을 갖습니다.

SVML 작업을 위한 어셈블리 소스 파일은 OS별 디렉토리 아래에 있는 `jdk.incubator.vector` 모듈의 소스 코드에 있습니다. JDK 빌드 프로세스는 대상 운영 체제에 대한 이러한 소스 파일을 SVML 관련 공유 라이브러리로 컴파일합니다. 이 라이브러리는 메가바이트 미만으로 상당히 큽니다. jlink를 통해 빌드된 JDK 이미지가 `jdk.incubator.vector` 모듈을 생략하면 SVML 라이브러리가 이미지에 복사되지 않습니다.

구현은 현재 Linux 및 Windows만 지원합니다. 어셈블리 소스 파일에 필요한 지시문을 제공하는 것은 쉽지 않은 작업이므로 나중에 macOS 지원을 고려할 것입니다.

HotSpot 런타임은 SVML 라이브러리를 로드하려고 시도하고, 존재하는 경우 SVML 라이브러리의 작업을 명명된 스텁 루틴에 바인딩합니다. C2 컴파일러는 연산 및 벡터 종(즉, 앨리먼트 유형 및 모양)을 기반으로 적절한 스텁 루틴을 호출하는 코드를 생성합니다.

앞으로 프로젝트 파나마가 벡터 값을 지원하기 위해 기본 호출 규칙에 대한 지원을 확장하면 벡터 API 구현이 외부 소스에서 SVML 라이브러리를 로드하는 것이 가능할 수 있습니다. 이 접근 방식이 성능에 영향을 미치지 않으면 더 이상 SVML을 소스 형식으로 포함하고 JDK에 빌드할 필요가 없습니다. 그때까지는 잠재적인 성능 향상을 감안할 때 위의 접근 방식을 수용할 수 있는 것으로 간주합니다.

### JEP 415:	Context-Specific Deserialization Filters

애플리케이션이 각 개별 역직렬화 작업에 대한 필터를 선택하기 위해 호출되는 JVM 전체 필터 팩토리를 통해 컨텍스트별 및 동적으로 선택된 역직렬화 필터를 구성할 수 있도록 합니다.

#### Description

간단한 경우 필터 팩토리는 전체 애플리케이션에 대해 고정 필터를 반환할 수 있습니다. 예를 들어, 다음은 예제 클래스를 허용하고, java.base 모듈의 클래스를 허용하고, 다른 모든 클래스를 거부하는 필터입니다.

```java
var filter = ObjectInputFilter.Config.createFilter("example.*;java.base/*;!*")
```

여러 실행 컨텍스트가 있는 애플리케이션에서 필터 팩토리는 각각에 대한 사용자 정의 필터를 제공하여 개별 컨텍스트를 더 잘 보호할 수 있습니다. 스트림이 구성되면 필터 팩토리는 현재 스레드 로컬 상태, 호출자 계층, 라이브러리, 모듈 및 클래스 로더를 기반으로 실행 컨텍스트를 식별할 수 있습니다. 이때 필터를 생성하거나 선택하는 정책은 컨텍스트를 기반으로 특정 필터 또는 필터 구성을 선택할 수 있습니다.

여러 필터가 있는 경우 해당 결과를 결합할 수 있습니다. 필터를 결합하는 유용한 방법은 역직렬화를 거부하는 필터가 있는 경우 역직렬화를 거부하고, 허용하는 필터가 있으면 허용하고, 그렇지 않으면 결정되지 않은 상태로 유지하는 것입니다.

##### Command Line Use

`jdk.serialFilter` 및 `jdk.serialFilterFactory` 속성은 다음에서 설정할 수 있습니다. 필터 및 필터 팩토리를 설정하는 command line. 기존 `jdk.serialFilter` 속성은 패턴 기반 필터를 설정합니다.

`jdk.serialFilterFactory` 속성은 첫 번째 역직렬화 전에 설정할 필터 팩토리의 클래스 이름입니다. 클래스는 공용이어야 하며 애플리케이션 클래스 로더에 액세스할 수 있어야 합니다.

[JEP 290](https://openjdk.java.net/jeps/243)과의 호환성을 위해 `jdk.serialFilterFactory` 속성이 설정되지 않은 경우 필터 팩토리는 이전 버전과의 호환성을 제공하는 내장으로 설정됩니다.

##### API

JVM 전체 필터 팩토리를 설정하고 가져오기 위해 `ObjectInputFilter.Config` 클래스에 두 가지 메소드를 정의합니다. 필터 팩토리는 현재 필터와 다음 필터라는 두 개의 인수가 있는 함수이며 필터를 반환합니다.

```java
/**
 * Return the JVM-wide deserialization filter factory.
 *
 * @return the JVM-wide serialization filter factory; non-null
 */
public static BinaryOperator<ObjectInputFilter> getSerialFilterFactory();

/**
 * Set the JVM-wide deserialization filter factory.
 *
 * The filter factory is a function of two parameters, the current filter
 * and the next filter, that returns the filter to be used for the stream.
 *
 * @param filterFactory the serialization filter factory to set as the
 * JVM-wide filter factory; not null
 */
public static void setSerialFilterFactory(BinaryOperator<ObjectInputFilter> filterFactory);
```

##### Example

이 클래스는 현재 스레드에서 발생하는 모든 역직렬화 작업으로 필터링하는 방법을 보여줍니다. 스레드별 필터를 보유할 스레드 로컬 변수를 정의하고, 해당 필터를 반환하는 필터 팩토리를 정의하고, 팩토리를 JVM 전체 필터 팩토리로 구성하고, 특정 컨텍스트에서 `Runnable`을 실행하는 유틸리티 기능을 제공합니다. 스레드별 필터.

```java
public class FilterInThread implements BinaryOperator<ObjectInputFilter> {

    // ThreadLocal to hold the serial filter to be applied
    private final ThreadLocal<ObjectInputFilter> filterThreadLocal = new ThreadLocal<>();

    // Construct a FilterInThread deserialization filter factory.
    public FilterInThread() {}

    /**
     * The filter factory, which is invoked every time a new ObjectInputStream
     * is created.  If a per-stream filter is already set then it returns a
     * filter that combines the results of invoking each filter.
     *
     * @param curr the current filter on the stream
     * @param next a per stream filter
     * @return the selected filter
     */
    public ObjectInputFilter apply(ObjectInputFilter curr, ObjectInputFilter next) {
        if (curr == null) {
            // Called from the OIS constructor or perhaps OIS.setObjectInputFilter with no current filter
            var filter = filterThreadLocal.get();
            if (filter != null) {
                // Prepend a filter to assert that all classes have been Allowed or Rejected
                filter = ObjectInputFilter.Config.rejectUndecidedClass(filter);
            }
            if (next != null) {
                // Prepend the next filter to the thread filter, if any
                // Initially this is the static JVM-wide filter passed from the OIS constructor
                // Append the filter to reject all UNDECIDED results
                filter = ObjectInputFilter.Config.merge(next, filter);
                filter = ObjectInputFilter.Config.rejectUndecidedClass(filter);
            }
            return filter;
        } else {
            // Called from OIS.setObjectInputFilter with a current filter and a stream-specific filter.
            // The curr filter already incorporates the thread filter and static JVM-wide filter
            // and rejection of undecided classes
            // If there is a stream-specific filter prepend it and a filter to recheck for undecided
            if (next != null) {
                next = ObjectInputFilter.Config.merge(next, curr);
                next = ObjectInputFilter.Config.rejectUndecidedClass(next);
                return next;
            }
            return curr;
        }
    }

    /**
     * Apply the filter and invoke the runnable.
     *
     * @param filter the serial filter to apply to every deserialization in the thread
     * @param runnable a Runnable to invoke
     */
    public void doWithSerialFilter(ObjectInputFilter filter, Runnable runnable) {
        var prevFilter = filterThreadLocal.get();
        try {
            filterThreadLocal.set(filter);
            runnable.run();
        } finally {
            filterThreadLocal.set(prevFilter);
        }
    }
}
```

스트림별 필터가 이미 `ObjectInputStream::setObjectFilter`로 설정된 경우 필터 팩토리는 해당 필터를 다음 필터와 결합합니다. 두 필터 중 하나가 클래스를 거부하면 해당 클래스가 거부됩니다. 두 필터 중 하나가 클래스를 허용하면 해당 클래스가 허용됩니다. 그렇지 않으면 결과가 미정입니다.

다음은 `FilterInThread` 클래스를 사용하는 간단한 예입니다.

```java
// Create a FilterInThread filter factory and set
    var filterInThread = new FilterInThread();
    ObjectInputFilter.Config.setSerialFilterFactory(filterInThread);

    // Create a filter to allow example.* classes and reject all others
    var filter = ObjectInputFilter.Config.createFilter("example.*;java.base/*;!*");
    filterInThread.doWithSerialFilter(filter, () -> {
          byte[] bytes = ...;
          var o = deserializeObject(bytes);
    });
```