---
title:  "Java 15 New Features"
excerpt: "Java 15 New Features"
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

새로운 LTS 버전인 JDK 15가 2020년 9월 15일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 15](https://openjdk.java.net/projects/jdk/15/)를 참고했습니다.

### JEP 339:	Edwards-Curve Digital Signature Algorithm (EdDSA)

RFC 8032에 설명된 대로 EdDSA(Edwards-Curve Digital Signature Algorithm)를 사용하여 암호화 서명을 구현합니다.

#### Goals 

EdDSA는 JDK의 기존 서명 체계보다 몇 가지 장점이 있는 최신 타원 곡선 서명 체계입니다. 이 JEP의 주요 목표는 RFC 8032에서 표준화된 이 체계를 구현하는 것입니다. 이 새로운 서명 체계는 ECDSA를 대체하지 않습니다.

추가 구현 목표:

* 동일한 보안 강도에서 기존 ECDSA 구현(네이티브 C 코드 사용)보다 더 나은 성능으로 플랫폼 독립적인 EdDSA 구현을 개발합니다. 예를 들어, ~126비트 보안에서 Curve25519를 사용하는 EdDSA는 ~128비트 보안에서 곡선 secp256r1을 사용하는 ECDSA만큼 빨라야 합니다.
* 플랫폼이 일정한 시간에 64비트 정수 덧셈/곱셈을 수행한다고 가정할 때 타이밍이 비밀과 무관한지 확인합니다. 또한 구현은 비밀에 대해 분기하지 않습니다. 이러한 속성은 부채널 공격을 방지하는 데 유용합니다.

#### Description

새로운 서명, `KeyFactory` 및 `KeyPairGenerator` 서비스는 EdDSA를 지원하기 위해 SunEC 공급자에 추가됩니다. EdDSA 키를 나타내기 위해 새 클래스와 인터페이스가 API에 추가되고 EdDSA 서명 체계를 설명하기 위해 새 표준 알고리즘 이름이 추가됩니다. API 및 구현은 모든 EdDSA 변형(순수, 사전 해시 및 컨텍스트)을 지원합니다.

포인트 산술은 부채널 공격을 방지하기 위해 분기 없는 조건부 할당 작업과 함께 RFC 8032에 정의된 이중 및 더하기 작업을 사용합니다. 필드 산술은 XDH(JEP 324)용으로 개발된 모듈식 산술 라이브러리를 사용합니다. 결합된 구현은 JVM 및 하드웨어의 동작에 대한 합리적인 가정 하에서 타이밍 및 캐시 사이드 채널로 비밀을 누출하지 않습니다.

API는 곡선 도메인 매개변수 및 EdDSA 변형을 설명하기 위해 XDH용으로 개발된 `NamedParameterSpec` 클래스를 재사용합니다. Edwards 곡선 포인트, EdDSA 키 및 컨텍스트 정보를 포함하는 서명 매개변수를 위한 새로운 클래스와 인터페이스가 개발될 것입니다.

아래는 사용예시입니다.

```java
// example: generate a key pair and sign
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();
// algorithm is pure Ed25519
Signature sig = Signature.getInstance("Ed25519");
sig.initSign(kp.getPrivate());
sig.update(msg);
byte[] s = sig.sign();

// example: use KeyFactory to contruct a public key
KeyFactory kf = KeyFactory.getInstance("EdDSA");
boolean xOdd = ...
BigInteger y = ...
NamedParameterSpec paramSpec = new NamedParameterSpec("Ed25519");
EdECPublicKeySpec pubSpec = new EdECPublicKeySpec(paramSpec, new EdPoint(xOdd, y));
PublicKey pubKey = kf.generatePublic(pubSpec);
```

### JEP 360:	Sealed Classes (Preview)

봉인된 클래스와 인터페이스로 Java 프로그래밍 언어를 향상시키십시오. 봉인된 클래스 및 인터페이스는 다른 클래스 또는 인터페이스가 확장하거나 구현할 수 있는 것을 제한합니다.

#### Goals

* 클래스 또는 인터페이스 작성자가 구현을 담당하는 코드를 제어할 수 있도록 합니다.
* 수퍼클래스의 사용을 제한하기 위해 액세스 수정자보다 더 선언적인 방법을 제공합니다.
* 패턴의 철저한 분석을 뒷받침하여 패턴 매칭의 미래 방향을 지원합니다.

#### Description

Sealed class 또는 인터페이스는 허용된 클래스 및 인터페이스에 의해서만 확장되거나 구현될 수 있습니다.

클래스는 선언에 sealed modifier를 적용하여 봉인됩니다. 그런 다음, extends 및 Implements 절 뒤에, permits 절은 sealed class를 확장할 수 있는 클래스를 지정합니다. 예를 들어 다음 Shape 선언은 세 개의 허용되는 하위 클래스를 지정합니다.

```java
package com.example.geometry;

public abstract sealed class Shape
    permits Circle, Rectangle, Square { ... }
```

Permits에 의해 지정된 클래스는 동일한 모듈(수퍼클래스가 명명된 모듈에 있는 경우) 또는 동일한 패키지(수퍼클래스가 명명되지 않은 모듈에 있는 경우)와 같이 슈퍼클래스 근처에 있어야 합니다. 예를 들어 다음 Shape 선언에서 허용되는 하위 클래스는 모두 동일한 이름의 모듈의 서로 다른 패키지에 있습니다.

```java
package com.example.geometry;

public abstract sealed class Shape 
    permits com.example.polar.Circle,
            com.example.quad.Rectangle,
            com.example.quad.simple.Square { ... }
```

허용된 하위 클래스의 크기와 수가 작은 경우 봉인된 클래스와 동일한 소스 파일에서 선언하는 것이 편리할 수 있습니다. 이러한 방식으로 선언되면 봉인된 클래스는 permits 절을 생략할 수 있으며 Java 컴파일러는 소스 파일의 선언에서 허용된 하위 클래스를 유추합니다. (하위 클래스는 보조 또는 중첩 클래스일 수 있습니다.) 예를 들어, 다음 코드가 `Root.java`에서 발견되면 봉인된 클래스 `Root`는 세 개의 허용된 하위 클래스를 갖는 것으로 추론됩니다.

```java
abstract sealed class Root { ... 
    final class A extends Root { ... }
    final class B extends Root { ... }
    final class C extends Root { ... }
}
```

`permits` 지정된 클래스는 정식 이름을 가져야 합니다. 그렇지 않으면 컴파일 타임 오류가 보고됩니다. 즉, 익명 클래스와 로컬 클래스는 봉인된 클래스의 하위 유형으로 허용될 수 없습니다.

봉인된 클래스는 허용되는(permitted) 하위 클래스에 세 가지 제약 조건을 부과합니다.

1. 봉인된 클래스와 허용된 하위 클래스는 동일한 모듈에 속해야 하며, 이름이 없는 모듈에서 선언된 경우 동일한 패키지에 속해야 합니다.
2. 모든 허용된 하위 클래스는 봉인된 클래스를 직접 확장해야 합니다.
3. 모든 허용된 하위 클래스는 수정자를 사용하여 상위 클래스에 의해 시작된 봉인을 전파하는 방법을 설명해야 합니다.
   * 허용된 하위 클래스는 클래스 계층 구조의 해당 부분이 더 확장되는 것을 방지하기 위해 `final`로 선언될 수 있습니다. (레코드 클래스는 암시적으로 `final`로 선언됩니다.) 
   * 허용된 하위 클래스는 해당 계층의 일부가 봉인된 슈퍼클래스에서 예상한 것보다 더 확장될 수 있도록 봉인된 것으로 선언될 수 있지만 제한된 방식으로만 가능합니다.
   * 허용된 하위 클래스는 봉인되지 않은 것으로 선언되어 계층의 해당 부분이 알려지지 않은 하위 클래스에 의해 확장을 위해 열린 상태로 되돌아갑니다. 봉인된 클래스는 허용된 하위 클래스가 이 작업을 수행하는 것을 방지할 수 없습니다. (수식자 non-sealed는 Java용으로 제안된 첫 번째 하이픈 연결 키워드입니다.)

세 번째 제약 조건의 예로서 `Circle`과 `Square`는 `Rectangle`이 봉인된 동안 최종적일 수 있으며 봉인되지 않은 `WeirdShape`라는 새 하위 클래스를 추가합니다.

```java
package com.example.geometry;

public abstract sealed class Shape
    permits Circle, Rectangle, Square, WeirdShape { ... }

public final class Circle extends Shape { ... }

public sealed class Rectangle extends Shape 
    permits TransparentRectangle, FilledRectangle { ... }
public final class TransparentRectangle extends Rectangle { ... }
public final class FilledRectangle extends Rectangle { ... }

public final class Square extends Shape { ... }

public non-sealed class WeirdShape extends Shape { ... }
```

`WeirdShape`는 알려지지 않은 클래스에 의해 확장될 수 있지만 해당 하위 클래스의 모든 인스턴스는 `WeirdShape`의 인스턴스이기도 합니다. 따라서 `Shape`의 인스턴스가 `Circle`, `Rectangle`, `Square` 또는 `WeirdShape`인지 테스트하기 위해 작성된 코드는 여전히 철저합니다.

`final`, `sealing` 및 `non-sealed` 수정자 중 정확히 하나는 허용된 각 하위 클래스에서 사용해야 합니다. 클래스가 `sealed`(서브클래스를 암시)과 `final`(서브클래스가 없음을 암시), 또는 `non-sealed`(서브클래스를 암시)와 `final`(서브클래스가 없음을 암시), 또는 `sealed`(제한된 서브클래스를 암시)과 `non-sealed` 둘 다일 수는 없습니다. `non-sealed`(무제한 하위 클래스를 의미).

(최종 수식어는 확장/구현이 완전히 금지된 봉인의 특별한 경우로 간주할 수 있습니다. 즉, `final`은 개념적으로 `sealing`과 개념적으로 동일하며 그러한 허가 조항을 작성할 수는 없지만 아무 것도 지정하지 않는 허가 조항이 있습니다.)

봉인되거나 봉인되지 않은 클래스는 추상일 수 있으며 추상 멤버를 가질 수 있습니다. 봉인된 클래스는 추상적인 하위 클래스를 허용할 수 있습니다. 단, 최종적이 아니라 봉인되거나 봉인되지 않은 경우입니다.

클래스가 봉인된 클래스를 확장하지만 허용되지 않는 경우 컴파일 타임 오류입니다.

##### Sealed interfaces

클래스에 대한 이야기와 유사하게 인터페이스에 봉인된 수정자를 적용하여 인터페이스를 봉인합니다. 슈퍼인터페이스를 지정하기 위한 extends 절 뒤에는 구현 클래스와 서브인터페이스가 `permit` 절로 지정됩니다. 예를 들어:

```java
package com.example.expression;

public sealed interface Expr
    permits ConstantExpr, PlusExpr, TimesExpr, NegExpr {...}

public final class ConstantExpr implements Expr {...}
public final class PlusExpr     implements Expr {...}
public final class TimesExpr    implements Expr {...}
public final class NegExpr      implements Expr {...}
```

##### Sealed classes and Records

봉인된 클래스는 Java 15의 또 다른 미리보기 기능인 레코드([JEP 384](https://openjdk.java.net/jeps/384))와 잘 작동합니다. 레코드는 암시적으로 최종이므로 레코드가 있는 봉인된 계층 구조는 위의 예보다 약간 더 간결합니다. 

```java
package com.example.expression;

public sealed interface Expr
    permits ConstantExpr, PlusExpr, TimesExpr, NegExpr {...}

public final class ConstantExpr implements Expr {...}
public final class PlusExpr     implements Expr {...}
public final class TimesExpr    implements Expr {...}
public final class NegExpr      implements Expr {...}
```

봉인된 클래스와 레코드의 조합을 대수 데이터 형식이라고도 합니다. 레코드를 사용하면 제품 형식을 표현할 수 있고 봉인된 클래스를 사용하여 합계 형식을 표현할 수 있습니다.

##### Sealed classes in the JDK

JDK에서 봉인된 클래스를 사용하는 방법의 예는 JVM 엔터티에 대한 설명자를 모델링하는 `java.lang.constant` 패키지에 있습니다.

```java
package java.lang.constant;

public sealed interface ConstantDesc
    permits String, Integer, Float, Long, Double,
            ClassDesc, MethodTypeDesc, DynamicConstantDesc {...}

// ClassDesc is designed for subclassing by JDK classes only
public sealed interface ClassDesc extends ConstantDesc
    permits PrimitiveClassDescImpl, ReferenceClassDescImpl {...}
final class PrimitiveClassDescImpl implements ClassDesc {...}
final class ReferenceClassDescImpl implements ClassDesc {...} 

// MethodTypeDesc is designed for subclassing by JDK classes only
public sealed interface MethodTypeDesc extends ConstantDesc
    permits MethodTypeDescImpl {...}
final class MethodTypeDescImpl implements MethodTypeDesc {...}

// DynamicConstantDesc is designed for subclassing by user code
public non-sealed abstract class DynamicConstantDesc implements ConstantDesc {...}
```

##### Java Grammar

```java
NormalClassDeclaration:
  {ClassModifier} class TypeIdentifier [TypeParameters]
    [Superclass] [Superinterfaces] [PermittedSubclasses] ClassBody

ClassModifier:
  (one of)
  Annotation public protected private
  abstract static sealed final non-sealed strictfp

PermittedSubclasses:
  permits ClassTypeList

ClassTypeList:
  ClassType {, ClassType}
```

##### JVM support for sealed classes

Java Virtual Machine은 런타임 시 봉인된 클래스와 인터페이스를 인식하고 승인되지 않은 하위 클래스 및 하위 인터페이스에 의한 확장을 방지합니다.

Sealed는 클래스 수정자이지만 `ClassFile` 구조에는 `ACC_SEALED` 플래그가 없습니다. 대신, 봉인된 클래스의 클래스 파일에는 봉인된 수정자를 암시적으로 나타내고 허용된 하위 클래스를 명시적으로 지정하는 `PermittedSubclasses` 속성이 있습니다.

```java
PermittedSubclasses_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 number_of_classes;
    u2 classes[number_of_classes];
}
```

허용된 하위 클래스 목록은 필수입니다. 허용된 하위 클래스가 컴파일러에서 유추된 경우에도 해당 유추된 하위 클래스는 `PermittedSubclasses` 특성에 명시적으로 포함됩니다.

허용된 하위 클래스의 클래스 파일에는 새 속성이 없습니다.

JVM이 수퍼클래스 또는 수퍼인터페이스에 `PermittedSubclasses` 속성이 있는 클래스를 정의하려고 할 때 정의되는 클래스는 속성으로 이름을 지정해야 합니다. 그렇지 않으면 `IncompatibleClassChangeError`가 발생합니다.

##### Reflection API

다음 `public` 메소드가 `java.lang.Class`에 추가됩니다.

* `java.lang.constant.ClassDesc[]` `getPermittedSubclasses()`
* `boolean isSealed()`

`getPermittedSubclasses()` 메서드는 클래스가 봉인된 경우 허용된 모든 하위 클래스를 나타내는 `java.lang.constant.ClassDesc` 객체를 포함하는 배열을 반환하고 클래스가 봉인되지 않은 경우 빈 배열을 반환합니다.

`isSealed` 메소드는 주어진 클래스 또는 인터페이스가 봉인된 경우 `true`를 반환합니다. (`isEnum`과 비교)

### JEP 371:	Hidden Classes

다른 클래스의 바이트코드에서 직접 사용할 수 없는 클래스인 `hidden classes`를 도입합니다. 숨겨진 클래스는 런타임에 클래스를 생성하고 리플렉션을 통해 간접적으로 사용하는 프레임워크에서 사용하기 위한 것입니다. 숨겨진 클래스는 액세스 제어 중첩의 구성원으로 정의될 수 있으며 다른 클래스와 독립적으로 언로드될 수 있습니다.

##### Goals 

* 프레임워크가 클래스를 프레임워크의 발견 불가능한 구현 세부사항으로 정의하도록 허용하여 다른 클래스와 연결되거나 리플렉션을 통해 발견되지 않도록 합니다.
* 발견할 수 없는 클래스로 액세스 제어 중첩 확장을 지원합니다.
* 프레임워크가 필요한 만큼 정의할 수 있는 유연성을 갖도록 검색할 수 없는 클래스의 적극적인 언로드를 지원합니다.
* 비표준 API `sun.misc.Unsafe::defineAnonymousClass`를 더 이상 사용하지 않으며 향후 릴리스에서 제거할 예정입니다.
* 어떤 식으로든 Java 프로그래밍 언어를 변경하지 마십시오.

### JEP 372:	Remove the Nashorn JavaScript Engine

Nashorn JavaScript 스크립트 엔진과 API, `jjs` 도구를 제거하십시오. 엔진, API 및 도구는 향후 릴리스에서 제거할 명시적인 의도와 함께 Java 11에서 제거를 위해 더 이상 사용되지 않습니다.

#### Description

두 개의 JDK 모듈이 영구적으로 제거됩니다.

* `jdk.scripting.nashorn` -- `jdk.nashorn.api.scripting` 및 `jdk.nashorn.api.tree` 패키지를 포함합니다.
* `jdk.scripting.nashorn.shell` -- `jjs` 도구를 포함합니다.

### JEP 373:	Reimplement the Legacy DatagramSocket API

`java.net.DatagramSocket` 및 `java.net.MulticastSocket` API의 기본 구현을 유지 관리 및 디버그하기 쉬운 보다 간단하고 현대적인 구현으로 교체하십시오. 새로운 구현은 현재 Project Loom에서 탐색 중인 가상 스레드 작업에 쉽게 적용할 수 있습니다. 이것은 이미 레거시 소켓 API를 다시 구현한 [JEP 353](https://openjdk.java.net/jeps/353)의 후속 조치입니다.

#### Description

현재 `DatagramSocket` 및 `MulticastSocket` 클래스는 모든 소켓 호출을 `java.net.DatagramSocketImpl` 구현에 위임합니다. 여기에는 Unix 플랫폼의 `PlainDatagramSocketImpl` 및 Windows 플랫폼의 `TwoStackPlainDatagramSocketImpl` 및 `DualPlainDatagramSocketImpl`과 같은 플랫폼별 구체적인 구현이 존재합니다. JDK 1.1로 거슬러 올라가는 추상 `DatagramSocketImpl` 클래스는 매우 적게 지정되었으며 NIO를 기반으로 이 클래스의 구현을 제공하는 데 방해가 되는 몇 가지 구식 메서드를 포함합니다(아래에 설명된 대안 참조).

`SocketImpl`용 [JEP 353](https://openjdk.java.net/jeps/353)에서 수행된 것과 유사한 `DatagramSocketImpl` 구현에 대한 드롭인 대체를 제공하는 대신 이 JEP는 `DatagramSocket이` 모든 호출을 직접 위임하는 `DatagramSocket`의 다른 인스턴스를 내부적으로 래핑하도록 제안합니다. 래핑된 인스턴스는 NIO `DatagramChannel::socket(the new implementation)`에서 생성된 소켓 어댑터이거나, 레거시 `DatagramSocketImpl` 구현에 위임하는 레거시 `DatagramSocket` 클래스의 복제본(이전 버전과의 호환성 스위치 구현 목적)입니다. . `DatagramSocketImplFactory`가 애플리케이션에 의해 설치된 경우 이전 레거시 구현이 선택됩니다. 그렇지 않으면 기본적으로 새 구현이 선택되어 사용됩니다.

20년 이상 후에 구현을 전환할 위험을 줄이기 위해 레거시 구현은 제거되지 않습니다. JDK 관련 시스템 속성인 `jdk.net.usePlainDatagramSocketImpl`은 JDK가 레거시 구현을 사용하도록 구성하기 위해 도입되었습니다(아래 위험 및 가정 참조). 값 없이 설정하거나 시작 시 값 "`true`"로 설정하면 레거시 구현이 사용됩니다. 그렇지 않으면 새(NIO 기반) 구현이 사용됩니다. 향후 릴리스에서는 레거시 구현 및 시스템 속성을 제거할 것입니다. 어느 시점에서 우리는 `DatagramSocketImpl` 및 `DatagramSocketImplFactory`를 더 이상 사용하지 않고 제거할 수도 있습니다.

![images](https://bugs.openjdk.java.net/secure/attachment/87038/ReimplementDS.png)

새 구현은 기본적으로 활성화되어 있습니다. 선택기 공급자(`sun.nio.ch.SelectorProviderImpl` 및 `sun.nio.ch.DatagramChannelImpl`)의 플랫폼 기본 구현을 직접 사용하여 데이터그램 및 멀티캐스트 소켓에 대해 중단되지 않는 동작을 제공합니다. 따라서 사용자 지정 선택기 공급자를 설치해도 `DatagramSocket` 및 `MulticastSocket`에는 영향을 주지 않습니다.

### JEP 374:	Disable and Deprecate Biased Locking

기본적으로 편향된 잠금을 비활성화하고 모든 관련 커맨드라인 옵션을 사용하지 않습니다.

#### Description

JDK 15 이전에는 편향 잠금이 항상 활성화되어 사용 가능합니다. 이 JEP를 사용하면 명령줄에서 `-XX:+UseBiasedLocking`이 설정되지 않는 한 HotSpot이 시작될 때 편향 잠금이 더 이상 활성화되지 않습니다.

`UseBiasedLocking` 옵션 및 편향 잠금의 구성 및 사용과 관련된 모든 옵션을 더 이상 사용하지 않습니다.

* Product options: `BiasedLockingStartupDelay`, `BiasedLockingBulkRebiasThreshold`, `BiasedLockingBulkRevokeThreshold`, `BiasedLockingDecayTime` 및 `UseOptoBiasInlining`
* Diagnostic options: `PrintBiasedLockingStatistics` 및 `PrintPreciseBiasedLockingStatistics`

옵션은 계속 허용되고 조치되지만 사용 중단 경고가 발행됩니다.

### JEP 375:	Pattern Matching for instanceof (Second Preview)

자세한 사항은 [JEP 305](https://openjdk.java.net/jeps/305)에서 확인 가능합니다.

`instanceof` 연산자에 대한 패턴 일치로 Java 프로그래밍 언어를 향상시키십시오. 패턴 일치를 사용하면 프로그램의 공통 논리, 즉 개체에서 구성 요소의 조건부 추출을 보다 간결하고 안전하게 표현할 수 있습니다. 이것은 JDK 15의 미리보기 언어 기능입니다.

#### History

`instanceof`에 대한 패턴 일치는 2017년 중반에 [JEP 305](https://openjdk.java.net/jeps/305)에서 제안되었으며 2019년 말에 미리 보기 언어 기능으로 JDK 14를 대상으로 했습니다. 이 JEP는 추가 피드백을 수집하기 위해 JDK 14의 미리 보기와 관련된 변경 사항 없이 JDK 15의 기능을 다시 미리 볼 것을 제안합니다.

### JEP 377:	ZGC: A Scalable Low-Latency Garbage Collector

Z Garbage Collector를 실험 기능에서 제품 기능으로 변경합니다.

#### Description

ZGC는 오늘 `-XX:+UnlockExperimentalVMOptions` `-XX:+UseZGC` 명령줄 옵션을 통해 활성화됩니다. ZGC를 제품(비실험적) 기능으로 만드는 것은 `-XX:+UnlockExperimentalVMOptions` 옵션이 더 이상 필요하지 않음을 의미합니다.

ZGC를 제품(비실험) 기능으로 전환하는 것은 주로 UseZGC 명령줄 옵션 유형을 실험에서 제품으로 변경하는 문제입니다. 또한 현재 실험적으로 표시된 다음 ZGC 관련 옵션도 제품으로 변경할 예정입니다. 이러한 옵션의 기본값은 변경하지 않습니다.

* `ZAllocationSpikeTolerance`
* `ZCollectionInterval`
* `ZFragmentationLimit`
* `ZMarkStackSpaceLimit`
* `ZProactive`
* `ZUncommit`
* `ZUncommitDelay`

현재 실험적으로 표시된 다음 ZGC 관련 JFR 이벤트도 제품으로 변경됩니다.

* `ZAllocationStall`
* `ZPageAllocation`
* `ZPageCacheFlush`
* `ZRelocationSet`
* `ZRelocationSetGroup`
* `ZUncommit`

### JEP 378:	Text Blocks

자세한 사항은 [JEP 355](https://openjdk.java.net/jeps/355)에서 확인 가능합니다.

추가된 사항만 기술하겠습니다.

##### New escape sequences

줄 바꿈과 공백 처리를 더 세밀하게 제어할 수 있도록 두 개의 새로운 이스케이프 시퀀스를 도입했습니다.

첫째, `\<line-terminator>` 이스케이프 시퀀스는 줄 바꿈 문자의 삽입을 명시적으로 억제합니다.

예를 들어, 매우 긴 문자열 리터럴을 더 작은 하위 문자열의 연결로 분할한 다음 결과 문자열 표현식을 여러 줄로 하드 래핑하는 것이 일반적입니다.

```java
String literal = "Lorem ipsum dolor sit amet, consectetur adipiscing " +
                 "elit, sed do eiusmod tempor incididunt ut labore " +
                 "et dolore magna aliqua.";
```

`\<line-terminator>` 이스케이프 시퀀스를 사용하면 다음과 같이 표현할 수 있습니다.

```java
String text = """
                Lorem ipsum dolor sit amet, consectetur adipiscing \
                elit, sed do eiusmod tempor incididunt ut labore \
                et dolore magna aliqua.\
                """;
```

문자 리터럴 및 기존 문자열 리터럴이 포함된 개행을 허용하지 않는 단순한 이유 때문에 `\<line-terminator>` 이스케이프 시퀀스는 텍스트 블록에만 적용할 수 있습니다.

둘째, 새로운 `\s` 이스케이프 시퀀스는 단순히 단일 공백으로 변환됩니다(`\u0020`).

이스케이프 시퀀스는 우발적인 공백 제거가 끝날 때까지 변환되지 않으므로 `\s`는 후행 공백 제거를 방지하기 위해 울타리 역할을 할 수 있습니다. 이 예에서 각 줄 끝에 `\s`를 사용하면 각 줄의 길이가 정확히 6자임을 보장합니다.

```java
String colors = """
    red  \s
    green\s
    blue \s
    """;
```

`\s` 이스케이프 시퀀스는 텍스트 블록, 기존 문자열 리터럴 및 문자 리터럴에서 사용할 수 있습니다.

### JEP 379:	Shenandoah: A Low-Pause-Time Garbage Collector

Shenandoah 가비지 수집기를 실험 기능에서 제품 기능으로 변경합니다.

#### Description

JDK 12 이상에서 Shenandoah는 `-XX:+UnlockExperimentalVMOptions` `-XX:+UseShenandoahGC` 옵션을 통해 활성화됩니다. Shenandoah를 제품 기능으로 만드는 것은 `-XX:+UnlockExperimentalVMOptions`가 더 이상 필요하지 않다는 것을 의미합니다. 관련된 많은 Shenandoah 옵션이 검토 대상에서 "experimental"에서 "product"으로 바뀝니다. 옵션의 기본값은 변경되지 않습니다. 이 변경은 플래그 클래스에서 다소 외관상 변경됩니다.

JDK 12에 통합될 때 Shenandoah는 이미 Red Hat 8u 및 11u 다운스트림 릴리스에서 지원되는 가비지 수집기로 출하되었으며 RHEL 및 RHEL 다운스트림 사용자가 사용했습니다. 이 때문에 Shenandoah 8u 및 Shenandoah 11u는 이미 실험 단계가 아니므로 이 변경 사항의 영향을 받지 않습니다. 8u 및 11u 이외의 다른 것을 실행하는 사용자는 소수에 불과하므로 이 변경의 실제 영향은 미미할 것으로 예상합니다.

### JEP 381:	Remove the Solaris and SPARC Ports

Solaris/SPARC, Solaris/x64 및 Linux/SPARC 포트에 대한 소스 코드 및 빌드 지원을 제거합니다. 이러한 포트는 향후 릴리스에서 제거할 명시적인 의도로 JDK 14에서 제거를 위해 더 이상 사용되지 않습니다.

#### Goals

* Solaris 운영 체제와 관련된 모든 소스 코드 제거
* SPARC 아키텍처와 관련된 모든 소스 코드 제거
* 향후 릴리스에 대한 문서 및 소스 코드 주석 업데이트

#### Description

Solaris 및 SPARC 관련 코드, 빌드 시스템 논리 및 설명서를 모두 제거하거나 조정할 것입니다.

* 디렉토리 제거:
  * `src/hotspot/cpu/sparc`
  * `src/hotspot/os/solaris`
  * `src/hotspot/os_cpu/solaris`
  * `src/hotspot/os_cpu/linux_sparc`
  * `src/hotspot/os_cpu/solaris_x86`
  * `src/java.base/solaris`
  * `src/java.desktop/solaris`
  * `src/jdk.attach/solaris`
  * `src/jdk.crypto.cryptoki/solaris`
  * `src/jdk.crypto.ucrypto/solaris`
  * `src/jdk.management/solaris`
  * `src/jdk.net/solaris`
  * 다음 전처리기 정의 및 매크로로 보호되는 C/C++ 코드를 제거하거나 조정합니다.
  * `SPARC`, `__sparc__`, `__sparc`, `__sparcv9`
  * `SOLALRIS`, `__solaris__`
  * `SPARC_ONLY`, `NOT_SPARC`
  * `SOLARIS_ONLY`, `NOT_SOLARIS`
  * `SOLARIS_MUTATOR_LIBTHREAD`
  * `SPARC_WORKS`
* Solaris 또는 SunOS를 확인하는 Java 코드를 제거하거나 조정합니다. 예를 들면 다음과 같습니다.
  * `System.getProperty("os.name").contains("Solaris")`
  * `System.getProperty("os.name").startsWith("SunOS")`
* Solaris 관련 기능 제거:
  * `jdk.crypto.ucrypto` 모듈의 `OracleUcrypto` provider
  * `jdk.net` 모듈의 `jdk.net.SocketFlow` 소켓 옵션
* Solaris, SPARC 또는 Oracle Studio와 관련된 빌드 시스템(`automake` 등) 논리를 제거하거나 조정합니다. 특히 다음 변수 및 값:
  * `OPENJDK_{BUILD,TARGET}_OS = Solaris`
  * `OPENJDK_{BUILD,TARGET}_CPU_ARCH = sparc`
  * `TOOLCHAIN_TYPE = solstudio`
  * `is{Build,Target}Os = solaris`
  * `is{Build,Target}Cpu = sparcv9`
* Solaris 또는 `SPARC`에만 관련되거나 실행되는 테스트를 제거하거나 조정합니다. 예를 들면 다음과 같습니다.
  * 다음을 사용하여 `jtreg` 테스트
  * `@requires os.family == "solaris"`
  * `@requires os.arch == "sparc"`
  * `@requires os.arch == "sparcv9"`
  * `@requires(vm.simpleArch == "sparcv9")`
  * `Platform.isSolaris()` 또는 `Platform.isSparc()` 테스트 라이브러리 메서드 및 메서드 자체
* 문제 목록을 정리하여 솔라리스 또는 SPARC에 대한 참조를 제거하십시오.
* 주의해서 Solaris 또는 SPARC를 참조하는 소스 코드의 주석을 조정하십시오.
  * 대부분의 경우 주석은 간단히 제거할 수 있지만 Solaris 및 SPARC에 대한 일부 참조는 포트가 제거된 후에도 여전히 관련될 수 있습니다.
* Solaris devkit 작성자 스크립트를 제거합니다(make/devkit 아래).
* JIB 구성 파일에서 모든 Solaris 또는 SPARC 관련 논리를 제거합니다.

### JEP 383:	Foreign-Memory Access API (Second Incubator)

자세한 사항은 [JEP 370](https://openjdk.java.net/jeps/370)에서 확인 가능합니다.

##### Checked vs. unchecked addresses

역참조 작업은 확인된 메모리 주소에서만 가능합니다. 확인된 주소는 위 코드(`segment.baseAddress()`)의 메모리 세그먼트에서 얻은 주소와 같이 API에서 일반적입니다. 그러나 메모리 주소가 선택되지 않고 연결된 세그먼트가 없는 경우 런타임에서 주소와 연결된 공간적 및 시간적 경계를 알 수 있는 방법이 없기 때문에 안전하게 역참조될 수 없습니다. 확인되지 않은 주소의 예는 다음과 같습니다.

* NULL 주소(`MemoryAddress::NULL`)
* `Long` 값으로 구성된 주소(`MemoryAddress::ofLong` 팩토리를 통해)

확인되지 않은 주소를 역참조하기 위해 클라이언트에는 두 가지 옵션이 있습니다. 주소가 클라이언트가 이미 가지고 있는 메모리 세그먼트 내에 있는 것으로 알려진 경우 클라이언트는 소위 리베이스 작업(`MemoryAddress::rebase`)을 수행할 수 있습니다. 안전하게 역참조될 수 있는 새 주소 인스턴스. 또는 그러한 세그먼트가 존재하지 않는 경우 클라이언트는 특별한 `MemorySegment::ofNativeRestricted` 팩토리를 사용하여 안전하지 않게 세그먼트를 생성할 수 있습니다. 이 팩토리는 역참조 작업을 허용하기 위해 확인되지 않은 주소에 공간 및 시간 경계를 효과적으로 연결합니다.

그러나 이름에서 알 수 있듯이 이 작업은 본질적으로 안전하지 않으므로 주의해서 사용해야 합니다. 이러한 이유로 외부 메모리 액세스 API는 JDK 속성 `foreign.restricted`가 거부 이외의 값으로 설정된 경우에만 이 팩토리에 대한 호출을 허용합니다. 이 속성에 가능한 값은 다음과 같습니다.

* `deny` - 제한된 각 호출에 대해 런타임 예외를 발행합니다. 이것은 기본값입니다.
* `permit` - 제한된 통화를 허용합니다.
* `warn` - 허가와 유사하지만 제한된 각 호출에 대해 한 줄 경고도 인쇄합니다.
* `디버그`와 유사하지만 주어진 제한에 해당하는 스택도 덤프합니다.

앞으로 제한된 작업에 대한 액세스를 모듈 시스템과 더욱 통합할 계획입니다. 즉, 특정 모듈에는 제한된 기본 액세스가 필요할 수 있습니다. 상기 모듈에 의존하는 애플리케이션이 실행될 때, 사용자는 제한된 네이티브 작업을 수행하기 위해 상기 모듈에 권한을 제공해야 할 수도 있고, 그렇지 않으면 런타임이 애플리케이션의 모듈 그래프 빌드를 거부할 것입니다.

##### Confinement

공간 및 시간 경계 외에도 세그먼트에는 스레드 제한 기능도 있습니다. 즉, 세그먼트는 세그먼트를 만든 스레드가 소유하고 다른 스레드는 세그먼트의 내용에 액세스하거나 특정 작업(예: 닫기)을 수행할 수 없습니다. 스레드 제한은 제한적이지만 다중 스레드 환경에서도 최적의 메모리 액세스 성능을 보장하는 데 중요합니다. 스레드 제한 제한이 제거되면 여러 스레드가 동일한 세그먼트에 동시에 액세스하고 닫을 수 있습니다. 이는 매우 값비싼 잠금 형식이 도입되지 않는 한 외부 메모리 액세스 API에서 제공하는 안전 보장을 무효화할 수 있습니다. 접근을 방지하고 경쟁을 닫습니다.

외부 메모리 액세스 API는 스레드 제한 장벽을 완화하는 두 가지 방법을 제공합니다. 첫째, 스레드는 명시적 핸드오프 작업을 수행하여 협력적으로 세그먼트를 공유할 수 있습니다. 여기서 스레드는 주어진 세그먼트에 대한 소유권을 해제하고 이를 다른 스레드로 전송합니다. 다음 코드를 고려하십시오.

```java
MemorySegment segmentA = MemorySegment.allocateNative(10); // confined by thread A
...
var segmentB = segmentA.withOwnerThread(threadB); // confined by thread B
```

이 액세스 패턴은 직렬 제한이라고도 하며 한 번에 하나의 스레드만 세그먼트에 액세스해야 하는 생산자/소비자 사용 사례에서 유용할 수 있습니다. 핸드오프 작업을 안전하게 만들기 위해 API는 원래 세그먼트를 종료하고(닫기가 호출되었지만 기본 메모리를 해제하지 않은 것처럼) 올바른 소유자가 있는 새 세그먼트를 반환합니다. 구현은 또한 두 번째 스레드가 세그먼트에 액세스할 때 첫 번째 스레드의 모든 쓰기가 메모리로 플러시되도록 합니다.

둘째, 메모리 세그먼트의 내용은 여전히 병렬로 처리될 수 있습니다(예: Fork/Join과 같은 프레임워크 사용) — 메모리 세그먼트에서 `Spliterator` 인스턴스를 가져옴으로써. 예를 들어 메모리 세그먼트의 모든 32비트 값을 병렬로 합산하려면 다음 코드를 사용할 수 있습니다.

```java
SequenceLayout seq = MemoryLayout.ofSequence(1_000_000, MemoryLayouts.JAVA_INT);
SequenceLayout seq_bulk = seq.reshape(-1, 100);
VarHandle intHandle = seq.varHandle(int.class, PathElement.sequenceElement());    

int sum = StreamSupport.stream(MemorySegment.spliterator(segment, seq_bulk), true)
                .mapToInt(slice -> {
					int res = 0;
        			MemoryAddress base = slice.baseAddress();
        			for (int i = 0; i < 100 ; i++) {
            			res += (int)intHandle.get(base, (long)i);
        			}
        			return res;
                }).sum();
```

`MemorySegment::spliterator`는 시퀀스 레이아웃인 세그먼트를 가져와서 세그먼트를 제공된 시퀀스 레이아웃의 요소에 해당하는 청크로 분할하는 분할기 인스턴스를 반환합니다. 여기에서 백만 개의 요소를 포함하는 배열의 요소를 합산하려고 합니다. 이제 각 계산이 정확히 하나의 요소를 처리하는 병렬 합계를 수행하는 것은 비효율적이므로 대신 레이아웃 API를 사용하여 대량 시퀀스 레이아웃을 파생합니다. 벌크 레이아웃은 원본 레이아웃과 동일한 크기를 갖지만 요소가 100개 요소 그룹으로 배열되는 시퀀스 레이아웃으로 병렬 처리에 더 적합해야 합니다.

분할자가 있으면 이를 사용하여 병렬 스트림을 구성하고 세그먼트의 내용을 병렬로 합산할 수 있습니다. 여기에서 세그먼트는 여러 스레드에서 동시에 액세스되지만 액세스는 일반적인 방식으로 발생합니다. 원래 세그먼트에서 슬라이스가 생성되고 일부 계산을 수행하기 위해 스레드에 제공됩니다. 외부 메모리 액세스 런타임은 스레드가 현재 분할자를 통해 세그먼트 슬라이스에 액세스하고 있는지 알고 있으므로 동일한 세그먼트에서 병렬 처리가 발생하는 동안 세그먼트가 닫히지 않도록 하여 안전을 강화할 수 있습니다.

### JEP 384:	Records (Second Preview)

#### Description

`Records`는 Java 언어에서 새로운 종류의 클래스입니다. 레코드의 목적은 변수의 작은 그룹이 새로운 종류의 엔터티로 간주되도록 선언하는 것입니다. 레코드는 상태(변수 그룹)를 선언하고 해당 상태와 일치하는 API에 커밋합니다. 이것은 레코드가 클래스가 일반적으로 누리는 자유(클래스의 API를 내부 표현에서 분리하는 기능)를 포기하지만 그 대가로 레코드가 훨씬 더 간결해짐을 의미합니다.

레코드 선언은 이름, 헤더 및 본문을 지정합니다. 헤더는 상태를 구성하는 변수인 레코드의 구성 요소를 나열합니다. (구성 요소 목록을 상태 설명이라고도 합니다.) 예를 들면 다음과 같습니다.

```java
record Point(int x, int y) { }
```

레코드는 데이터에 대한 투명한 전달자라는 의미론적 주장을 하기 때문에 레코드는 많은 표준 멤버를 자동으로 획득합니다.

* 헤더의 각 구성 요소에 대해 두 개의 멤버: 구성 요소와 이름 및 반환 유형이 동일한 공개 접근자 메서드와 구성 요소와 유형이 동일한 비공개 최종 필드.
* 서명이 헤더와 동일하고 레코드를 인스턴스화하는 새 표현식의 해당 인수에 각 개인 필드를 할당하는 표준 생성자.
* 두 레코드가 동일한 유형이고 동일한 구성 요소 값을 포함하는 경우 동일하다고 말하는 `equals` 및 `hashCode` 메소드; 그리고
* 이름과 함께 모든 레코드 구성 요소의 문자열 표현을 반환하는 `toString` 메서드입니다.

즉, 레코드의 헤더는 상태(구성 요소의 유형 및 이름)를 설명하고 API는 해당 상태 설명에 대해 기계적으로 완전하게 파생됩니다. API에는 구성, 구성원 액세스, 동등성 및 표시를 위한 프로토콜이 포함됩니다. (향후 버전에서는 강력한 패턴 매칭이 가능하도록 해체 패턴을 지원할 예정입니다.)

##### Rules for Records

레코드 구성 요소에서 파생된 개인 필드를 제외하고 헤더에서 자동으로 파생된 모든 멤버는 명시적으로 선언할 수 있습니다. 접근자 또는 `equals/hashCode`의 명시적 구현은 레코드의 의미론적 불변성을 유지하기 위해 주의해야 합니다.

생성자에 대한 규칙은 레코드에서 일반 클래스와 다릅니다. 생성자 선언이 없는 일반 클래스에는 자동으로 기본 생성자가 제공됩니다. 대조적으로, 생성자 선언이 없는 레코드에는 레코드를 인스턴스화한 새 표현식의 해당 인수에 모든 개인 필드를 할당하는 정식 생성자가 자동으로 제공됩니다. 예를 들어, 이전에 선언된 레코드 -- `record Point(int x, int y) { }` --는 다음과 같이 컴파일됩니다.

```java
record Point(int x, int y) { 
    // Implicitly declared fields
    private final int x;
    private final int y;

    // Other implicit declarations elided ...

    // Implicitly declared canonical constructor
    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
```

정규 생성자는 위에 표시된 대로 레코드 헤더와 일치하는 형식 매개변수 목록을 사용하여 명시적으로 선언하거나 개발자가 매개변수를 할당하는 지루한 작업 없이 매개변수 유효성 검사 및 정규화에 집중할 수 있도록 보다 간결한 형식으로 선언할 수 있습니다. 필드에. 압축된 표준 생성자는 형식 매개변수 목록을 생략합니다. 암시적으로 선언되며 레코드 구성 요소에 해당하는 `private` 필드는 본문에 할당할 수 없지만 생성자의 끝에서 해당 형식 매개 변수(`this.x = x;`)에 자동으로 할당됩니다. 예를 들어, 다음은 (암시적) 형식 매개변수의 유효성을 검사하는 컴팩트 정규 생성자입니다.

```java
record Range(int lo, int hi) {
    Range {
        if (lo > hi)  // referring here to the implicit constructor parameters
            throw new IllegalArgumentException(String.format("(%d,%d)", lo, hi));
    }
}
```

기록 선언에는 여러 가지 제한 사항이 있습니다.

* 레코드에 `extends` 절이 없습니다. 열거형의 슈퍼클래스가 항상 `java.lang.Enum`인 것과 유사하게 레코드의 슈퍼클래스는 항상 `java.lang.Record`입니다. 일반 클래스가 암시적 수퍼클래스 `Object`를 명시적으로 확장할 수 있지만 레코드는 암시적 수퍼클래스 `Record`를 포함하여 어떤 클래스도 명시적으로 확장할 수 없습니다.
* 레코드는 암시적으로 최종적이며 추상화될 수 없습니다. 이러한 제한 사항은 레코드의 API가 상태 설명에 의해서만 정의되며 나중에 다른 클래스나 레코드에 의해 향상될 수 없다는 점을 강조합니다.
* 레코드는 인스턴스 필드를 명시적으로 선언할 수 없으며 인스턴스 이니셜라이저를 포함할 수 없습니다. 이러한 제한은 레코드 헤더만 레코드 값의 상태를 정의하도록 합니다.
* 레코드 클래스의 레코드 구성 요소에 해당하는 암시적으로 선언된 필드는 최종적이며 리플렉션을 통해 수정할 수 없습니다(이렇게 하면 `IllegalAccessException`이 발생함). 이러한 제한은 데이터 캐리어 클래스에 광범위하게 적용할 수 있는 기본적으로 변경할 수 없는 정책을 구현합니다.
* 그렇지 않으면 자동으로 파생될 멤버의 명시적 선언은 명시적 선언의 형식 주석을 무시하고 자동으로 파생된 멤버의 형식과 정확히 일치해야 합니다.
* 레코드는 네이티브 메서드를 선언할 수 없습니다. 레코드가 기본 메서드를 선언할 수 있는 경우 레코드의 동작은 정의에 따라 레코드의 명시적 상태가 아니라 외부 상태에 따라 달라집니다. 네이티브 메서드가 있는 클래스는 레코드로 마이그레이션하기에 적합하지 않습니다.

위의 제한 사항을 넘어서서 레코드는 일반 클래스처럼 작동합니다.

* 레코드는 `new` 키워드로 인스턴스화됩니다.
* 레코드는 최상위 수준으로 선언되거나 중첩될 수 있으며 일반일 수 있습니다.
* 레코드는 정적 메서드, 정적 필드 및 정적 이니셜라이저를 선언할 수 있습니다.
* 레코드는 인스턴스 메서드를 선언할 수 있습니다. 즉, 레코드는 구성 요소에 해당하는 공개 접근자 메서드를 명시적으로 선언할 수 있으며 다른 인스턴스 메서드도 선언할 수 있습니다.
* 레코드는 인터페이스를 구현할 수 있습니다. 레코드는 수퍼클래스를 지정할 수 없지만(헤더에 설명된 상태를 넘어서 상속된 상태를 의미하기 때문에) 레코드는 수퍼인터페이스를 자유롭게 지정하고 이를 구현하는 데 도움이 되는 인스턴스 메소드를 선언할 수 있습니다. 클래스와 마찬가지로 인터페이스는 많은 레코드의 동작을 유용하게 특성화할 수 있습니다. 동작은 도메인 독립적(예: 비교 가능)이거나 도메인 특정일 수 있으며, 이 경우 레코드는 도메인을 캡처하는 봉인된 계층 구조의 일부일 수 있습니다(아래 참조).
* 레코드는 중첩 레코드를 포함하여 중첩 유형을 선언할 수 있습니다. 레코드 자체가 중첩된 경우 암시적으로 정적입니다. 이것은 레코드에 상태를 자동으로 추가하는 인스턴스를 즉시 둘러싸는 것을 방지합니다.
* 레코드 및 해당 상태 설명의 구성 요소에 주석을 달 수 있습니다. 주석은 자동으로 파생된 필드, 메서드 및 생성자 매개변수로 전파됩니다. 레코드 구성 요소의 유형에 대한 유형 주석은 자동으로 파생된 멤버의 유형에도 전파됩니다.

##### Records and Sealed Types

레코드는 봉인된 유형([JEP 360](https://openjdk.java.net/jeps/360))에서 잘 작동합니다. 예를 들어, 레코드 패밀리는 동일한 봉인된 인터페이스를 구현할 수 있습니다.

```java
package com.example.expression;

public sealed interface Expr
    permits ConstantExpr, PlusExpr, TimesExpr, NegExpr {...}

public record ConstantExpr(int i)       implements Expr {...}
public record PlusExpr(Expr a, Expr b)  implements Expr {...}
public record TimesExpr(Expr a, Expr b) implements Expr {...}
public record NegExpr(Expr e)           implements Expr {...}
```

레코드와 봉인된 유형의 조합을 대수 데이터 유형이라고도 합니다. 레코드를 통해 제품 유형을 표현할 수 있고 봉인된 유형을 통해 합계 유형을 표현할 수 있습니다.

##### Local records

레코드를 생성하고 사용하는 프로그램은 그 자체가 단순한 변수 그룹인 많은 중간 값을 처리할 가능성이 높습니다. 이러한 중간 값을 모델링하기 위해 레코드를 선언하는 것이 편리한 경우가 많습니다. 한 가지 옵션은 오늘날 많은 프로그램이 도우미 클래스를 선언하는 것처럼 정적 및 중첩된 "도우미" 레코드를 선언하는 것입니다. 더 편리한 옵션은 변수를 조작하는 코드에 가까운 메소드 내부에 레코드를 선언하는 것입니다. 따라서 이 JEP는 로컬 클래스의 전통적인 구성과 유사한 로컬 레코드를 제안합니다.

다음 예에서는 판매자 및 월별 판매 수치의 집계가 로컬 레코드인 `MerchantSales`로 모델링됩니다. 이 레코드를 사용하면 다음과 같은 스트림 작업의 가독성이 향상됩니다.

```java
List<Merchant> findTopMerchants(List<Merchant> merchants, int month) {
    // Local record
    record MerchantSales(Merchant merchant, double sales) {}

    return merchants.stream()
        .map(merchant -> new MerchantSales(merchant, computeSales(merchant, month)))
        .sorted((m1, m2) -> Double.compare(m2.sales(), m1.sales()))
        .map(MerchantSales::merchant)
        .collect(toList());
}
```

로컬 레코드는 중첩 레코드의 특별한 경우입니다. 모든 중첩 레코드와 마찬가지로 로컬 레코드는 암시적으로 정적입니다. 이것은 자신의 메서드가 바깥쪽 메서드의 변수에 액세스할 수 없음을 의미합니다. 결과적으로 이것은 레코드에 상태를 자동으로 추가하는 즉시 둘러싸는 인스턴스를 캡처하는 것을 방지합니다. 로컬 레코드가 암시적으로 정적이라는 사실은 암시적으로 정적이 아닌 로컬 클래스와 대조됩니다. 사실 지역 클래스는 암시적이든 명시적이든 정적이 아니며 항상 둘러싸는 메서드의 변수에 액세스할 수 있습니다.

로컬 레코드의 유용성을 감안할 때 로컬 열거형과 로컬 인터페이스도 있으면 유용할 것입니다. 그것들은 의미론에 대한 우려 때문에 Java에서 전통적으로 허용되지 않았습니다. 특히, 중첩된 열거형 및 중첩된 인터페이스는 암시적으로 정적이므로 로컬 열거형 및 로컬 인터페이스도 암시적으로 정적이어야 합니다. 그러나 Java 언어의 지역 선언(로컬 변수, 지역 클래스)은 결코 정적이지 않습니다. 그러나 [JEP 359](https://openjdk.java.net/jeps/359)에 로컬 레코드가 도입되면서 이러한 의미론적 문제가 극복되어 로컬 선언이 정적이 되도록 하고 로컬 열거형 및 로컬 인터페이스에 대한 문을 열었습니다.

##### Annotaions on records

레코드 구성 요소에는 레코드 선언에서 여러 역할이 있습니다. 레코드 구성 요소는 일급 개념이지만 각 구성 요소는 동일한 이름 및 유형의 필드, 동일한 이름 및 반환 유형의 접근자 메서드, 동일한 이름 및 유형의 생성자 매개변수에도 해당합니다.

이것은 구성 요소에 주석을 달 때 실제로 무엇에 주석이 달려 있는지에 대한 질문을 제기합니다. 그리고 대답은 "이 특정 주석에 적용할 수 있는 모든 것"입니다. 이를 통해 필드, 생성자 매개변수 또는 접근자 메서드에 주석을 사용하는 클래스를 이러한 멤버를 중복 선언하지 않고도 레코드로 마이그레이션할 수 있습니다. 예를 들어 다음과 같은 클래스

```java
public final class Card {
    private final @MyAnno Rank rank;
    private final @MyAnno Suit suit;
    @MyAnno Rank rank() { return this.rank; }
    @MyAnno Suit suit() { return this.suit; }
    ...
}
```

동등하고 훨씬 더 읽기 쉬운 레코드 선언으로 마이그레이션할 수 있습니다.

```java
public record Card(@MyAnno Rank rank, @MyAnno Suit suit) { ... }
```

주석의 적용 가능성은 `@Target` 메타 주석을 사용하여 선언됩니다. 다음을 고려하세요:

```java
@Target(ElementType.FIELD)
    public @interface I1 {...}
```

이것은 주석 `@I1`을 선언하고 필드 선언에 적용 가능합니다. 주석이 둘 이상의 선언에 적용 가능하다고 선언할 수 있습니다. 예를 들어:

```java
@Target({ElementType.FIELD, ElementType.METHOD})
    public @interface I2 {...}
```

이것은 주석 `@I2`를 선언하고 필드 선언과 메소드 선언 모두에 적용할 수 있습니다.

레코드 구성 요소의 주석으로 돌아가면 이러한 주석이 해당하는 프로그램 지점에 표시됩니다. 즉, 전파는 `@Target` 메타 주석을 사용하여 프로그래머의 제어 하에 있습니다. 전파 규칙은 체계적이고 직관적이며 다음과 같이 적용됩니다.

* 레코드 구성 요소의 주석이 필드 선언에 적용 가능한 경우 주석은 해당 `private` 필드에 나타납니다.
* 레코드 구성 요소의 주석이 메서드 선언에 적용 가능한 경우 주석은 해당 접근자 메서드에 나타납니다.
* 레코드 구성 요소의 주석이 형식 매개 변수에 적용 가능한 경우 명시적으로 선언되지 않은 경우 표준 생성자의 해당 형식 매개 변수에 주석이 표시되고 명시적으로 선언된 경우 압축 생성자의 해당 형식 매개 변수에 주석이 나타납니다.
* 레코드 구성 요소의 주석이 유형에 적용 가능한 경우 주석이 선언이 아닌 해당 유형 사용에 표시된다는 점을 제외하고 전파 규칙은 선언 주석의 경우와 동일합니다.

공용 접근자 메서드 또는 (non-compact) 정식 생성자가 명시적으로 선언된 경우 직접 표시되는 주석만 있습니다. 해당 레코드 구성 요소에서 이러한 구성원으로 전파되는 것은 없습니다.

새 주석 선언 `@Target(RECORD_COMPONENT)`를 사용하여 레코드 구성 요소에 정의된 주석에서 주석이 생성되었음을 선언할 수도 있습니다. 이러한 주석은 아래의 리플렉션 API 섹션에 자세히 설명된 대로 리플렉션을 통해 검색할 수 있습니다.

##### Java Grammar

```java
RecordDeclaration:
  {ClassModifier} `record` TypeIdentifier [TypeParameters]
    RecordHeader [SuperInterfaces] RecordBody

RecordHeader:
 `(` [RecordComponentList] `)`

RecordComponentList:
 RecordComponent { `,` RecordComponent}

RecordComponent:
 {Annotation} UnannType Identifier
 VariableArityRecordComponent

VariableArityRecordComponent:
 {Annotation} UnannType {Annotation} `...` Identifier

RecordBody:
  `{` {RecordBodyDeclaration} `}`

RecordBodyDeclaration:
  ClassBodyDeclaration
  CompactConstructorDeclaration

CompactConstructorDeclaration:
 {Annotation} {ConstructorModifier} SimpleTypeName ConstructorBody
```

##### Class-file representation

레코드의 클래스 파일은 레코드 속성을 사용하여 레코드의 구성 요소에 대한 정보를 저장합니다.

```java
Record_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 components_count;
    record_component_info components[components_count];
}

record_component_info {
    u2 name_index;
    u2 descriptor_index;
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
```

레코드 구성 요소에 삭제된 설명자와 다른 일반 서명이 있는 경우 `record_component_info` 구조에 서명 속성이 있어야 합니다.

##### Reflection API

다음 `public` 메소드가 `java.lang.Class`에 추가됩니다.

* `RecordComponent[] getRecordComponents()`
* `boolean isRecord()`

`getRecordComponents()` 메소드는 `java.lang.reflect.RecordComponent` 객체의 배열을 반환합니다. 이 배열의 요소는 레코드 선언에 나타나는 것과 동일한 순서로 레코드의 구성 요소에 해당합니다. 이름, 주석 및 접근자 메서드를 포함하여 배열의 각 요소에서 추가 정보를 추출할 수 있습니다.

주어진 클래스가 레코드로 선언된 경우 `isRecord` 메서드는 `true`를 반환합니다. (`isEnum`과 비교)

### JEP 385:	Deprecate RMI Activation for Removal

제거를 위해 RMI 활성화 메커니즘을 더 이상 사용하지 않습니다. RMI 활성화는 Java 8 이후 선택 사항인 RMI의 더 이상 사용되지 않는 부분입니다. RMI의 다른 부분은 더 이상 사용되지 않습니다.

#### Description

RMI 활성화 메커니즘을 통해 RMI 기반 서비스는 유효성이 원격 객체 또는 이를 포함하는 JVM의 수명을 초과하는 스텁을 내보낼 수 있습니다. 기존(활성화 불가능) RMI를 사용하면 원격 개체가 파괴되자마자 스텁이 무효가 됩니다. 이 상황에서 복구하려면 클라이언트가 복잡한 오류 처리 논리를 구현해야 합니다. 클라이언트가 활성화 가능한 스텁에서 메소드를 호출하면 RMI 활성화 서비스가 요청 시 원격 객체를 인스턴스화하여 클라이언트가 유효하지 않은 스텁을 처리하는 부담을 덜어줍니다. 이것은 유용한 메커니즘처럼 보이지만 동기 섹션에서 설명한 것처럼 RMI 활성화의 실제 사용량은 거의 없습니다.

이 JEP는 향후 제거를 위해 RMI 활성화 메커니즘을 더 이상 사용하지 않습니다. 이를 위해서는 Java 플랫폼을 다음과 같이 변경해야 합니다.

* `java.rmi.activation` 패키지에 있는 모든 공용 클래스 및 인터페이스에 `@Deprecated(forRemoval=true)`를 추가하십시오.
* `@deprecated javadoc` 태그와 설명을 `java.rmi.activation` 패키지 선언에 추가하십시오.
* `java.rmi` 모듈 사양에 `Activation`의 사용 중단 알림을 추가합니다.
* RMI 사양의 RMI 활성화 장에 사용 중단 알림을 추가합니다.

JDK에도 다음 변경 사항이 적용됩니다.

* `@Deprecated(forRemoval=true)`를 `com.sun.rmi.rmid.ExecOptionPermission` 및 `ExecPermission` 클래스와 `com.sun.rmi.rmid` 패키지에 추가합니다.
* 사용 중단에 대한 경고 메시지를 표시하도록 `rmid` 도구를 변경합니다.
* `rmid` 도구 문서 페이지에 경고 알림을 추가하십시오. 여기에는 `rmid` 도구 자체의 사용 중단에 대한 알림이 포함됩니다. 또한 `com.sun.rmi.rmid`의 권한 클래스에 대한 사용 중단에 대한 알림도 포함될 것입니다. 이 페이지는 이러한 권한 클래스가 문서화된 JDK의 유일한 위치이기 때문입니다.

