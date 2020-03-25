---
title : Scala Objects, Case Classes, and Traits
tags :
- Trait
- Object
- Scala
---

*이 포스트는 [Learning Scala](http://188.166.46.4/get/PDF/Jason%20Swartz-Learning%20Scala_125.pdf) 를 바탕으로 작성하였습니다.*

## Objects 

**객체(Object)** 는 하나 이상의 인스턴스를 가질 수 없는 형태의 클래스로, 객체지향 설계에서는 **싱글턴(Singleton)** 이라 합니다. `new` 키워드로 인스턴스를 생성하는 대신 이름으로 직접 해당 객체에 접근합니다.

객체는 실행 중인 JVM 에 최초로 접근할 때 자동으로 인스턴스화됩니다.

Java 와 다른 언어는 클래스의 특정 필드와 메소드를 Static / Global 로 지정할 수 있습니다. 이는 해당 필드와 메소드가 한 인스턴스의 데이터에 구속되지 않으므로 클래스를 인스턴스화하지 않고도 접근할 수 있음을 의미합니다.

객체는  비슷한 기능을 제공하지만, 그 필드와 메소드를 인스턴스화 가능한 클래스와 분리합니다. 이렇게 분리하여 전역 필드 / 메소드와 인스턴스 기반의 필드 / 메소드 간의 차이를 명확히 하고, 더 안전한고 이해하기 쉬운 설계를 제공하는 데 기여합니다.

객체는 키워드 `class` 대신 `object` 를 사용하여 정의합니다. 객체는 어떤 매개변수도 취하지 않지만, 일반 클래스로 정의할 수 있던 것과 동일한 필드, 메소드, 내부 클래스를 정의할 수 있습니다.

**Syntax: Defining an Object**

```scala
object <identifier> [extends <identifier>] [{ fields, methods, and classes }]
```

어떻게 객체가 자동으로 인스턴스화되는지 알아보겠습니다.

```scala
scala> object Hello { println("in Hello"); def hi = "hi" }
defined object Hello

scala> println(Hello.hi)
in Hello
hi

scala> println(Hello.hi)
hi
```

### Apply Methods and Companion Objects 

Future 객체는 함수 매개변수를 취하여 그 함수를 백그라운드 스레드에서 호출하는 `apply()` 를 사용합니다. 이는 객체지향 프로그래밍에서 **팩토리(Factory)** 패턴이라 하며, 객체의 `apply()` 메소드를 사용하는 가장 보편적인 용도입니다.

특히 팩토리 패턴은 클래스의 새로운 인스턴스를 동반 객체로부터 생성하는 일반적인 방식입니다. **동반 객체(Companion Object)** 는 클래스와 동일한 이름을 공유하며, 동일한 파일 내에서 그 클래스로 함께 정의되는 객체입니다.

클래스가 동반 객체를 가지는 것은 Scala 에선 보편적인 패턴입니다. 동반 객체와 클래스가 접근 제어 관점에서는 하나의 단위로 간주되기 때문에 각각의 `private` 그리고 `protected` 필드와 메소드에 서로 접근할 수 있습니다.
`apply()` 팩토리 패턴과 동반 객체 패턴을 동일 예제에서 사용해보겠습니다.

```scala
scala> :paste
// Entering paste mode (ctrl-D to finish)

class Multiplier(val x: Int) { def product(y: Int) = x * y }

object Multiplier { def apply(x: Int) = new Multiplier(x) }

// Exiting paste mode, now interpreting.

defined class Multiplier
defined object Multiplier

scala> val tripler = Multiplier(3)
tripler: Multiplier = Multiplier@5af28b27

scala> val result = tripler.product(13)
result: Int = 39
```

위 클래스는 `Multiplier` 클래스에 숫자를 취하고 그 숫자를 다른 수에 곱하는 메소드를 제공합니다. 이 클래스와 동일한 이름을 가지는 동반 객체는 인스턴스와 똑같은 메소드를 가지는 `apply` 메소드를 가지고 있어서 이 메소드가 클래스의 팩토리 메소드의 역할을 하고 있음을 알려줍니다.

동반 클래스와 공유하는 특별한 접근 제어에 대해 알아보겠습니다.

```scala
scala> :paste
// Entering paste mode (ctrl-D to finish)

object DBConnection {
    private val db_url = "jdbc://localhost"
    private val db_user = "franken"
    private val db_pass = "berry"

def apply() = new DBConnection
}


class DBConnection {
    private val props = Map(
        "url" -> DBConnection.db_url,
        "user" -> DBConnection.db_user,
        "pass" -> DBConnection.db_pass
    )
    println(s"Created new connection for " + props("url"))
}

// Exiting paste mode, now interpreting.

defined object DBConnection
defined class DBConnection

scala> val conn = DBConnection()
Created new connection for jdbc://localhost
```

`DBConnection` 객체는 데이터베이스 연결 데이터를 `private` 상수들에 저장하지만, 동일한 이름의 클래스는 연결을 생성할 때 이 상수들을 읽을 수 있습니다.

상수는 전역 범위를 가지는데, 그 설정이 어플리케이션 전반에서 변하지 않으며, 시스템의 다른 어떤 부분에서 읽더라도 안전하기 때문입니다.

### Command-Line Applications with Objects 

스칼라는 객체에 `main` 메소드를 사용하여 어플리케이션의 진입점으로 이 특징을 지원합니다. Command-Line 어플리케이션을 Scala 에서 생성하려면 입력 인수로 문자열 배열을 취하는 `main` 메소드를 추가하면 됩니다. 코드를 컴파일했다면 이제 객체 이름을 `scala` 명령어와 함께 실행하면 됩니다.

현재 날짜를 출력하는 간단한 Command-Line 어플리케이션을 만들어보겠습니다.

```scala
$ cat > Date.scala
object Date {
    def main(args: Array[String]) {
        println(new java.util.Date)
    }
}

$ scalac Date.scala

$ scala Date
Mon Sep 01 22:03:09 PDT 2014
```

`Date` 객체를 *.class* 파일로 컴파일한 후에 이 객체를 어플리케이션으로 실행할 수 있게 됩니다. 이 예제는 Command-Line 어플리케이션을 생성, 컴파일, 실행하는 기본을 보여주지만, 실제로 입력 인수의 사용을 보여주지는 않습니다.

다음은 유닉스 명령어 `cat` 을 모방한 예제로 콘솔에 파일의 내용을 출력합니다.

```scala
$ cat > Cat.scala
object Cat {
    def main(args: Array[String]) {
        for (arg <- args) {
            println( io.Source.fromFile(arg).mkString )
        }
    }
}

$ scalac Cat.scala

$ scala Cat Date.scala
object Date {
    def main(args: Array[String]) {
        println(new java.util.Date)
    }
}
```

이번에는 입력 인수를 사용하였습니다. `Scala` 라이브러리의 *io.Source* 객체에서 `fromFile` 메소드는 각 파일을 읽기 위해 컬렉션 메소드 `mkString` 는 출력을 위해 한 줄을 단일 String 으로 전환하는데 사용합니다.

## Case Classes 

**케이스 클래스(Case Class)** 는 자동으로 생성된 메소드 몇 가지를 포함하는 인스턴스 생성이 가능한 클래스입니다. 또한, 케이스 클래스는 자동으로 생성되는 동방 객체를 포함하는데, 이 동반 객체도 자신만의 자동으로 생성된 메소드를 가지고 있습니다.

클래스와 동반객체에 있는 이 메소드들은 모두 클래스의 매개변수 목록에 기반을 두며, 이 매개변수들은 모든 필드를 반복적으로 비교하는 `equals` 구현과 클래스명 및 그 클래스의 모든 필드 값을 깔끔하게 출력하는 `toString` 메소드 같은 메소드들을 만드는 데 사용됩니다.

케이스 클래스는 생성된 데이터 기반 메소드가 주어졌을 때 주로 데이터를 저장하는 데 사용되는 클래스인 데이터 전송 객체를 잘 지원합니다. 하지만, 계층적인 클래스 구조에서는 잘 동작하지 않습니다. 상속받은 필드는 그 유틸리티 메소드를 만드는 데 사용되지 않기 때문입니다. 

생성된 메소드는 서브 클래스에 의해 추가된 필드를 고려하지 않기 때문에 일반적인 클래스가 케이스 클래스를 확장하는 것은 그 생성된 메소드로부터 유효하지 않은 결과를 가져올 수 있습니다. 하지만 명확하게 정해진 필드들을 가진 클래스를 원하면 자동으로 생성된 이 메소드는 유용하며, 따라서 케이스 클래스가 적임일 것입니다.

케이스 클래스를 생성하려면 클래스 정의 앞에 `case` 키워드를 추가하면 됩니다.

**Syntax: Defining a Case Class**

```scala
case class <identifier> ([var] <identifier>: <type>[, ... ])
                         [extends <identifier>(<input parameters>)]
                         [{ fields and methods }]
```

아래는 케이스 클래스를 위해 자동으로 생성된 클래스와 객체 메소드를 보여줍니다.

|Name|Location|Description|
|:--|:--|:--|
|`apply`|Object|케이스 클래스를 인스턴스화하는 팩토리 메소드|
|`copy`|Class|요청받은 변경사항이 반영된 인스턴스의 사본을 반환함, 매개변수는 현재 필드값으로 설정된 기본값을 갖는 클래스의 필드임|
|`equals`|Class|다른 인스턴스의 모든 필드가 이 인스턴스의 모든 필드와 일치하면 참을 반환함. 연산자 == 로도 호출 가능|
|`hashCode`|Class|인스턴스의 필드들의 해시 코드를 반환|
|`toString`|Class|클래스명과 필드를 String 으로 전환|
|`unapply`|Object|인스턴스를 그 인스턴스의 필드들의 튜플로 추출하여 패턴 매칭에 케이스 클래스 인스턴스를 사용할 수 있도록 함|

케이스 클래스를 사용한 예제를 보겠습니다.

```scala
scala> case class Character(name: String, isThief: Boolean)
defined class Character

scala> val h = Character("Hadrian", true)
h: Character = Character(Hadrian,true)

scala> val r = h.copy(name = "Royce")
r: Character = Character(Royce,true)

scala> h == r
res0: Boolean = false

scala> h match {
 | case Character(x, true) => s"$x is a thief"
 | case Character(x, false) => s"$x is not a thief"
 | }
res1: String = Hadrian is a thief
```

두 번째 인스턴스는 두 번재 필드에 대해 동일한 값을 공유합니다. 따라서 `copy` 메소드에서 첫 번재 필드에만 새로운 값을 지정하면 됩니다.

예제에서 사용한 생성된 메소드들은 케이스 클래스 매개변수를 기반으로 하는 두 필드 `name` 과 `isThief` 를 가지는 케이스 클래스에 따라 달라집니다. 만약 이 케이스 클래스가 다른 클래스를 그 클래스만의 필드로 확장하면서 그 필드들을 케이스 클래스 매개변수로 추가하지 않는다면, 생성된 메소드는 그 필드들을 사용할 수 없을것입니다.

## Traits 

**트레이트** 는 다중 상속을 가능하게 하는 클래스 유형 중 하나입니다. 클래스, 객체, 트레이트 모두 하나 이상의 클래스를 확장할 수 없지만, 동시에 여러 트레이트는 확장할 수 있습니다. 하지만 다른 유형과 달리 트레이트는 인스턴스화 할 수 없습니다.

트레이트는 클래스 매개변수를 취할수 없습니다. 하지만, 객체와 마찬가지로 클래스 매개변수를 취할 수 없습니다.

트레이트는 다음과 같이 정의합니다.

**Syntax: Defining a Trait**

```scala
trait <identifier> [extends <identifier>] [{ fields, methods, and classes }]
```

```scala
 | def removeMarkup(input: String) = {
 |  input
 |      .replaceAll("""</?\w[^>]*>""","")
 |      .replaceAll("<.*>","")
 |  }
 | }
defined trait HtmlUtils

scala> class Page(val s: String) extends HtmlUtils {
 | def asPlainText = removeMarkup(s)
 | }
defined class Page

scala> new Page("<html><body><h1>Introduction</h1></body></html>").asPlainText
res2: String = Introduction
```

`Page` 클래스는 객체명을 지정하지 않고도 `removeMarkup` 메소드를 직접 사용할 수 있습니다. 꽤 잘 동작하지만, `HtmlUtils` 의 클래스 버전도 동일하게 작업을 할 수 있습니다. `with` 키워드를 사용하여 트레이트 확장해보겠습니다.

```scala
scala> trait SafeStringUtils {
 |
 | // Returns a trimmed version of the string wrapped in an Option,
 | // or None if the trimmed string is empty.
 |  def trimToNone(s: String): Option[String] = {
 |      Option(s) map(_.trim) filterNot(_.isEmpty)
 |  }
 | }
defined trait SafeStringUtils

scala> class Page(val s: String) extends SafeStringUtils with HtmlUtils {
 | def asPlainText: String = {
 |  trimToNone(s) map removeMarkup getOrElse "n/a"
 |      }
 |  }
defined class Page

scala> new Page("<html><body><h1>Introduction</h1></body></html>").asPlainText
res3: String = Introduction

scala> new Page(" ").asPlainText
res4: String = n/a

scala> new Page(null).asPlainText
res5: String = n/a
```
이제 `Page` 클래스는 2 개의 트레이트로 확장하여 null 또는 빈 문자열 메세지에 n/a 를 반환하여 처리할 수 있다.

JVM 클래스는 하나의 부모 클래스만 확장할 수 있습니다. 하지만, Scala 언어가 이론적으로 다중 상속을 지원하더라도, 실제로 컴파일러는 클래스와 트레이트의 긴 한 줄짜리 계층구조를 만들기 위해 각 트레이트의 사본을 만듭니다.

따라서 클래스 A 와 트레이트 B, C 를 확장한 클래스는 실제로 .class 바이너리 파일로 컴파일할 때 하나의 클래스를 확장하는데, 그 클래스가 다른 클래스를 확장하고, 또 다른 클래스를 또 확장합니다.

상속될 클래스와 트레이트의 수평적인 리스트를 받아서 한 클래스가 다른 클래스를 확장하는 수직적 체인으로 재구성하는 절차를 **선형화(Linearization)** 이라 합니다.

이는 단일 상속만을 지원하는 실행 환경에서 다중 상속을 지원하는 일종의 대처 방안입니다. JVM 이 단일 상속만 지원하는 사실이 모든 클래스 계층구조가 비결정적이며 경쟁 관계의 구성원을 가진 두 트레이트로 혼란을 일으킬 가능성을 배제하는것을 보장합니다.

선형화에 대해 이해해야 할 가장 중요한 점은 Scala 컴파일러가 서로 확장하기 위해 트레이트와 선택적인 클래스를 어떤 순서로 배치하는가 입니다. 다중 상속 순서, 가장 낮은 서브클래스로부터 가장 높은 기반 클래스까지, 오른쪽에서 왼쪽 순으로 배치합니다.

따라서 A 가 클래스이고 B 와 C 가 트레이트인 `class D extends A with B with C` 로 정의된 클래스는 컴파일러에 의해 `class D extends C extends B extends A` 로 재구현됩니다.

간단한 테스트를 해보겠습니다.

```scala
scala> trait Base { override def toString = "Base" }
defined trait Base

scala> class A extends Base { override def toString = "A->" + super.toString }
defined class A

scala> trait B extends Base { override def toString = "B->" + super.toString }
defined trait B

scala> trait C extends Base { override def toString = "C->" + super.toString }
defined trait C

scala> class D extends A with B with C { override def toString = "D->" +
 super.toString }
defined class D

scala> new D()
res50: D = D->C->B->A->Base
```

클래스 D, 트레이트 C, 트레이트 B, 클래스 A 그리고 마지막 공통의 베이스 클래스인 Base 가 차례대로 호출됩니다.

선형화의 도 다른 이점으로는 부모클래스의 행위를 재정의하기 위해 트레이트를 작성할 수 있다는 점입니다.

아래는 완전한 베이스 클래스에 서브클래스가 결합될 때 부가적 기능을 추가하는 트레이트를 더한 예제입니다. 부모 클래스와 이를 확장한 두 트레이트부터 보겠습니다.

```scala
scala> class RGBColor(val color: Int) { def hex = f"$color%06X" }
defined class RGBColor

scala> val green = new RGBColor(255 << 8).hex
green: String = 00FF00

scala> trait Opaque extends RGBColor { override def hex = s"${super.hex}FF" }
defined trait Opaque

scala> trait Sheer extends RGBColor { override def hex = s"${super.hex}33" }
defined trait Sheer
```

두 트레이트 `Opaque` 와 `Sheer` 는 `RGBColor` 클래스를 확장하고 그 부모의 RGB 색상에 불투명도를 추가합니다. 부가적인 바이트는 종종 컴퓨터 그래픽에서 알파 채너로 불리며, 트레이트는 RGB 색상값을 16 진수 형태의 RGBA 색상으로 바꿉니다.

새로운 트레이트를 사용해보겠습니다. 부모 클래스와 그 부모 클래스를 확장한 트레이트 중 하나를 확장하겠습니다. 만약 해당 트레이트만 확장하려면 클래스 매개변수를 `RGBColor` 로 전달할 방법이 없습니다. 따라서 우리는 부모 클래스와 기능을 추가한 트레이트를 모두 확장할 것입니다.

```scala
scala> class Paint(color: Int) extends RGBColor(color) with Opaque
defined class Paint

scala> class Overlay(color: Int) extends RGBColor(color) with Sheer
defined class Overlay

scala> val red = new Paint(128 << 16).hex
red: String = 800000FF

scala> val blue = new Overlay(192).hex
blue: String = 0000C033
```

트레이느 선형화는 오른쪽부터 왼쪽의 순서를 가지기 때문에 `Paint` 의 계층 구조는 `Paint` -> `Opaque` -> `RGBColor` 가 됩니다. `Paint` 클래스에 추가된 클래스 매개변수는 `RGBColor` 클래스를 초기화하기 위해 사용되지만, `Paint` 와 `RGBColor` 사이의 `Opaque` 트레이트는 부가적인 기능을 추가하기 위해 `hex` 메소드를 재정의합니다.

즉, `Paint` 클래스는 불투명 색상값을 출력하고, `Overlay` 는 반투명 색상값을 출력합니다.

### Self Types 

**셀프 타입(Self Type)** 은 트레이트 애너테이션으로 그 트레이트가 클래스에 추가될 때 특정 타입 또는 그 서브타입과 함께 사용되어야 함을 분명히 합니다.

셀프 타입을 가지는 트레이트는 지정된 타입을 확장하지 않는 클래스에 추가될 수 없습니다. 어떤 면에서 그 트레이트가 직접적으로 해당 타입을 확장하지는 않지만, 언제나 그 타입을 확장합니다.

셀프 타입의 보편적인 용도는 입력 매개변수가 필요한 클래스에 트레이트로 기능을 추가하는 것입니다.

셀프 타입은 트레이트 정의의 중괄호를 연 바로 다음에 추가되며, 식별자, 요청받은 타입 그리고 화살표(`=>`) 를 포함합니다. 셀프 타입을 가지는 트레이트는 마치 그 트레이트가 해당 타입을 명시적으로 확장한 것처럼 그 타입의 필드에 접근할 수 있습니다.

**Syntax: Defining a Self Type**

```scala
trait ..... { <identifier>: <type> => .... }
```

셀프 타입에 사용되는 표준 식별자는 `self` 이지만, 다른 식별자도 사용할 수 있습니다.

다음은 셀프 타입을 사용하는 트레이트에 대한 예를 보여줍니다. 이 트레이트가 클래스와 함께 사용될 때 언제나 지정된 타입의 서브타입이 될 것임을 보장합니다.

```scala
scala> class A { def hi = "hi" }
defined class A

scala> trait B { self: A =>
 | override def toString = "B: " + hi
 | }
defined trait B

scala> class C extends B
<console>:9: error: illegal inheritance; 
self-type C does not conform to B's selftype B with A
    class C extends B
                    ^

scala> class C extends A with B
defined class C

scala> new C()
res1: C = B: hi 
```

셀프 타입이 트레이트에 추가하는 제약사항을 보여줍니다. 그러나 이 예제에서는 셀프 타입이 중요한 특징으로 구별되지 않는데, 트레이트 B 는 A 를 직접 확장만 했을 수 있기 때문입니다.

셀프 타입의 이점을 보여주는 예제를 작성해보겠습니다. 매개변수를 필요로 하는 클래스를 정의하고, 클래스를 확장하기 위해서만 사용되어야 하는 트레이트를 생성하겠습니다.

```scala
scala> class TestSuite(suiteName: String) { def start() {} }
defined class TestSuite

scala> trait RandomSeeded { self: TestSuite =>
 | def randomStart() {
 |  util.Random.setSeed(System.currentTimeMillis)
 |  self.start()
 |  }
 | }
defined trait RandomSeeded

scala> class IdSpec extends TestSuite("ID Tests") with RandomSeeded {
 |  def testId() { println(util.Random.nextInt != 1) }
 |  override def start() { testId() }
 |
 |  println("Starting...")
 |  randomStart()
 | }
defined class IdSpec
```

셀프 타입으로, 트레이트는 입력 매개변수 지정하지 않고도 클래스를 확장할 수 있습니다. 이 방식은 여러분의 트레이트에 제약사항이나 요구사항을 추가할 때 특정 맥ㅁ락에서만 사용되는 것을 보장하는 안전한 방식입니다.

### Instantiation with Traits 

트레이트를 사용하는 다른 방식으로는 클래스가 인스턴스화될 때 클래스에 트레이트를 추가하는것입니다. 트레이트에 대해 알지 못한 상태에서 정의된 클래스도 트레이트의 기능을 사용할 수 있습니다. 

유의할 점은 클래스 인스턴스화 시점에 추가된 트레이트는 그 클래스를 확장하는 것입니다. 트레이트 선형와의 왼쪽부터 오른쪽으로의 순서는 그 순서로 인스턴스화된 클래스를 포함하므로 모든 트레이트는 해당 클래스를 확장합니다.

트레이트는 `with` 키워드를 이용해 클래스에 추가할 수 있습니다. `extends` 키워드는 사용할 수 없는데 트레이트를 **확장하는 것** 이 아니라 **확장되기** 때문입니다.

트레이트로 인스턴스화된 클래스가 해당 트레이트의 기반 클래스가 되는 것을 셀프 타입을 사용하여 확인해보겠습니다.

```scala
scala> class A
defined class A

scala> trait B { self: A => }
defined trait B

scala> val a = new A with B
a: A with B = $anon$1@26a7b76d
```

`$anon$1@26a7b76d` 는 `anonymous` 의 축약어에 숫자 기반으로 지어진 이름입니다. 인스턴스의 클래스는 익명 클래스인데, 이 클래스가 공식적으로 명명된 클래스 정의를 포함하지 않는 클래스와 트레이트 조합을 포함하기 때문입니다. 중요한 사항은 트레이트 `B` 가 클래스 `A` 를 확장하는 인스턴스를 만들었다는 것입니다.

트레이트로 인스턴스화하는 것의 실제 가치는 기존 클래스에 새로운 기능이나 설정을 추가하는 데, 이 특징은 일반적으로 **종속성 주입(Dependency Injection)** 이라 합니다. 부모 클래스가 의존하는 실제 기능이 클래스 정의 시점 이후까지 추가되지 않다가 클래스가 인스턴스화될 때 그 특징이 클래스에 주입되기 때문입니다.

종속성 주입에 대해 실험해보겠습니다.

```scala
scala> class User(val name: String) {
 |  def suffix = ""
 |  override def toString = s"$name$suffix"
 | }
defined class User

scala> trait Attorney { self: User => override def suffix = ", esq." }
defined trait Attorney

scala> trait Wizard { self: User => override def suffix = ", Wizard" }
defined trait Wizard

scala> trait Reverser { override def toString = super.toString.reverse }
defined trait Reverser

scala> val h = new User("Harry P") with Wizard
h: User with Wizard = Harry P, Wizard

scala> val g = new User("Ginny W") with Attorney
g: User with Attorney = Ginny W, esq.

scala> val l = new User("Luna L") with Wizard with Reverser
l: User with Wizard with Reverser = draziW ,L anuL
```

3 명의 새로운 사용자는 직함이나 이름을 출력하는 새로운 방식을 가지게 되었습니다. 접미사인 *Wizard* 와 *esq* 는 하드코딩했지만, 인스턴스화할 때 별개 사용자 인스턴스에 추가됩니다.

## Importing Instance Members 

`import` 키워드는 클래스와 객체의 **구성원(Member)** 을 현재 네임스페이스에 임포트하는 데 사용될 수 있습니다. 그래서 구성원을 감싸고 있는 인스턴스나 이름을 지정하지 않고도 구성원에 직접 접근하는 것이 가능합니다.

클래스와 객체 구성원을 임포트하는 구문은 패키징된 클래스를 임포트하는 구문과 동일합니다.

이름으로 클래스 인스턴스의 단일 구성원을 임포트하거나 밑줄 기호로 전체 필드와 메소드를 임포트할 수 있습니다. 

```scala
```

`latteReceipt` 라는 긴 이름을 가진 값으로부터 필드를 임포트하여 `println` 문장에서 훨씬 간단한 코드로 필드에 접근할 수 있게되었습니다.

객체 임포트의 예제로, *util.Random* 객체로부터 모든 메소드들을 추가해보겠습니다. 이 객체는 *util.Random* 객체를 확장하여 난수 생성에 있어 새로운 시드를 설정할 필요가 없을때 사용하기 유용한 단일 전역 인스턴스를 제공합니다.

```scala
```

인스턴스 구성원을 임포트하는 것은 코드를 간소화하는 훌룡한 방식입니다. 하지만, 이름 충돌을 피하고 코드의 가독성을 떨어트리지 않기 위해 주의해야합니다.