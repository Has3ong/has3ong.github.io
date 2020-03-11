---
title : Scala Class
tags :
- Package
- Anonymous Class
- Abstract Class
- Class
- Scala
---

*이 포스트는 [Learning Scala](http://188.166.46.4/get/PDF/Jason%20Swartz-Learning%20Scala_125.pdf) 를 바탕으로 작성하였습니다.*

**클래스(Class)** 데이터 구조와 함수의 조합으로 객체지향 언어의 핵심 구성 요소입니다.

클래스는 **상속(Inheritance)** 으로 다른 클래스를 확장할 수 있어 서브클래스가 부모 클래스를 대신하여 작업하는 것이 가능하게합니다. **다형성(Polymorphism)** 은 서브클래스가 부모 클래스를 대신하여 작업하는것을 가능하게합니다. **캡슐화(Encapsulation)** 는 클래스의 외관을 관리하는 프라이버시 제어를 제공합니다.

가장 간단한 클래스를 정의하고 인스턴스를 만들어보겠습니다. 

```scala
scala> class User
defined class User

scala> val u = new User
u: User = User@7a8c8dcf

scala> val isAnyRef = u.isInstanceOf[AnyRef]
isAnyRef: Boolean = true
```

`u: User = User@7a8c8dcf` 에서 `7a8c8dcf` 는 해당 인스턴스에 대한 JVM 내부 참조입니다.

`User` 클래스를 재설계 해보겠습니다. 여기에 값과 그 값에서 동작하는 메소드를 추가해보겠습니다. 또한, 기본 `toString` 메소드를 재정의하여 더 유용한 정보를 제공하는 버전을 제공하겠습니다.

```scala
scala> class User {
 | val name: String = "Yubaba"
 | def greet: String = s"Hello from $name"
 | override def toString = s"User($name)"
 | }
defined class User

scala> val u = new User
u: User = User(Yubaba)

scala> println( u.greet )
Hello from Yubaba
```

`name` 필드를 고정값에서 매개변수화된 값으로 바꿔서 이 클래스를 좀 더 유용하게 만들어보겠습니다. Scala 에서 클래스 매개변수는 함수 정의에서 함수 이름 뒤에 나오는 함수의 매개변수와 마찬가지로 클래스 이름 뒤에서 지정합니다.

```scala
scala> class User(n: String) {
 | val name: String = n
 | def greet: String = s"Hello from $name"
 | override def toString = s"User($name)"
 | }
defined class User

scala> val u = new User("Zeniba")
u: User = User(Zeniba)

scala> println(u.greet)
Hello from Zeniba
```

클래스 매개변수는 `n` 은 `name` 값을 초기화하기 위해 사용했습니다. 하지만 이 매개변수는 메소드 내부에서 사용될 수 없습니다. 클래스가 생성이되고 나면 그 매개변수를 사용할 수 없습니다.

초기화를 위해 클래스 매개변수를 사용하는 대신 필드 중 하나를 클래스 매개변수로 선언할 수 있습니다. 클래스 매개변수 앞에 `val` 또는 `var` 키워드를 추가하면 클래스 매개변수가 클래스의 필드가 됩니다. `name` 필드에 클래스 매개변수로 옮겨서 확인해보겠습니다.

```scala
scala> class User(val name: String) {
 | def greet: String = s"Hello from $name"
 | override def toString = s"User($name)"
 | }
defined class User
```

이번에는 클래스와 리스트를 함께 사용해보겠습니다.

```scala
scala> val users = List(new User("Shoto"), new User("Art3mis"),
 new User("Aesch"))
users: List[User] = List(User(Shoto), User(Art3mis), User(Aesch))

scala> val sizes = users map (_.name.size)
sizes: List[Int] = List(8, 7, 5)

scala> val sorted = users sortBy (_.name)
sorted: List[User] = List(User(Aesch), User(Art3mis), User(Shoto))

scala> val third = users find (_.name contains "3")
third: Option[User] = Some(User(Art3mis))

scala> val greet = third map (_.greet) getOrElse "hi"
greet: String = Hello from Art3mis
```

Scala 클래스는 `extends` 키워드를 이용하여 다른 클래스로 확장할 수 있으며, `override` 키워드로 상속받은 메소드의 행위를 재정의할 수 있습니다. 클래스에서 필드와 메소드는 `this` 키워드를 이용하여 접근할 수 있습니다.

클래스의 부모 클래스의 필드와 메소드는 `supre` 키워드를 이용하여 접근할 수 있습니다. `super` 키워드는 메소드가 자신이 대체한 부모클래스와 유사한 메소드에 여전히 접근해야 할 필요가 있을 때 유용합니다.

이를 부모 클래스 `A` 서브 클래스 `B`, `C` 를 이용해보겠습니다.

```scala
scala> class A {
 | def hi = "Hello from A"
 | override def toString = getClass.getName
 | }
defined class A

scala> class B extends A
defined class B

scala> class C extends B { override def hi = "hi C -> " + super.hi }
defined class C

scala> val hiA = new A().hi
hiA: String = Hello from A

scala> val hiB = new B().hi
hiB: String = Hello from A

scala> val hiC = new C().hi
hiC: String = hi C -> Hello from A
```

클래스 `B` 는 `A` 와 동일한 메소드 `hi()` 를 공유하는걸 알 수 있습니다. 또한 메소드의 결과도 일치합니다. 하지만, 클래스 `B` 에 상속된 `C` 의 메소드 `hi()` 는 오버라이드 되어 메소드의 결과는 다른걸 확인할 수 있습니다.

다음은 Scala 의 다형성을 알아보겠습니다. 다형성은 클래스가 호환되는 다른 클래스의 모양새를 띄게 해주는 능력이라고 말합니다.

호환되는 말의 뜻은 서브클래스의 인스턴스가 그 부모 클래스의 인스턴스를 사용할 수 있지만, 그 반대로는 가능하지 않음을 의미합니다. 서브클래스는 자신의 부모 클래스를 확장하므로 부모의 필드와 메소드를 100% 지원하지만 그 역은 성립하지 않을 수 있습니다.

`A`, `B`, `C` 클래스를 이용하여 이 내용을 확인해보겠습니다.


```scala
scala> val a: A = new A
a: A = A

scala> val a: A = new B
a: A = B

scala> val b: B = new A
<console>:9: error: type mismatch;
 found : A
 required: B
 val b: B = new A
 ^

scala> val b: B = new B
b: B = B
```

`B` 클래스는 `A` 의 확장버전으로 `A` 필드와 메소드는 `B` 의 하위집합이지 그 반대로는 성립하지 않습니다. `B` 가 실제로 고유의 필드나 메소드를 추가하지 않더라도 이 상황은 달라지지 않습니다.

리스트가 확실히 그 클래스 각각의 인스턴스를 포함할 수 있도록 하기 위해 우리는 그 리스트를 `List[A]` 로 정의하여 모든 클래스와 호환되게 해야 합니다.

```scala
scala> val misc = List(new C, new A, new B)
misc: List[A] = List(C, A, B)

scala> val messages = misc.map(_.hi).distinct.sorted
messages: List[String] = List(Hello from A, hi C -> Hello from A)
```

## Defining Classes

클래스는 타입의 정의로 핵심 타입이나 다른 클래스의 필드를 포함합니다. 클래스는 그 필드에 동작하는 함수인 메소드와 중첩된 클래스 정의도 포함합니다.

**Syntax: Defining a Simple Class**

```scala
class <identifier> [extends <identifier>] [{ fields, methods, and classes }]
```

클래스 필드를 위한 저장소를 제공하는 메모리 할당인 클래스 **인스턴스(Instance)** 에서 클래스의 메소드를 호출하거나 그 필드에 접근할 수 있습니다. 클래스의 내용을 할당하기 위해 메모리에 적재하는 작업을 **인스턴스화(Instantition)** 또는 인스턴스 생성이라 합니다. `new` 키워드를 사용하면 이름으로 클래스의 인스턴스를 생성할 수 있으며, 이때 이름에는 괄호는 상관없습니다.

클래스가 좀 더 유용하려면 클래스의 다른 필드와 메소드를 초기화하거나 클래스의 필드로 동작하기 위해 사용되는 입력값인 **클래스 매개변수(Class Parameter)** 를 취해야 합니다. 클래스 매개변수는 함수의 입력 매개변수와 동일한 형태로 이름과 타입을 콤마로 구분한 리스트입니다.

**Syntax: Defining a Class with Input Parameters**

```scala
class <identifier> ([val|var] <identifier>: <type>[, ... ])
    [extends <identifier>(<input parameters>)]
    [{ fields and methods }]
```

입력 매개변수가 있는 클래스는 프로그래머가 여러 인스턴스를 생성해야 하는 이유를 제공하는데, 각 인스턴스는 자신만의 고유 내용을 가질 수 있기 때문입니다.

```scala
scala> class Car(val make: String, var reserved: Boolean) {
 | def reserve(r: Boolean): Unit = { reserved = r }
 | }
 defined class Car

scala> val t = new Car("Toyota", false)
t: Car = Car@4eb48298

scala> t.reserve(true)

scala> println(s"My ${t.make} is now reserved? ${t.reserved}")
My Toyota is now reserved? true
```

클래스의 필드와 메소드는 인스턴스와 그 필드, 메소드를 점(.) 으로 구분하는 표준 삽입점 표기법으로 접근할 수 있습니다.

함수처럼 클래스 매개변수는 이름으로 매개변수를 지정하여 호출이 가능합니다. 예로 `Car` 클래스 정의에서 매개변수 위치와 반대되는 순서로 인스턴스를 만들어 보겠습니다.

```scala
scala> val t2 = new Car(reserved = false, make = "Tesla")
t2: Car = Car@2ff4f00f

scala> println(t2.make)
Tesla
```

위에서 정의한 클래스가 매개변수를 취하는 클래스를 확장한 것이라면, 클래스의 정의에 매개변수가 포함되어 있는지 확인해야 합니다. `extends` 키워드 다음에 정의된 클래스는 필요에 따라 자신만의 입력 매개변수를 가질 수 있습니다.

`Car` 의 새로운 서브클래스로 `Lotus` 라는 클래스를 정의하는데, 여기에는 부모의 입력 매개변수를 지정합니다.

```scala
scala> class Car(val make: String, var reserved: Boolean) {
 | def reserve(r: Boolean): Unit = { reserved = r }
 | }
defined class Car

scala> class Lotus(val color: String, reserved: Boolean) extends
 Car("Lotus", reserved)
defined class Lotus

scala> val l = new Lotus("Silver", false)
l: Lotus = Lotus@52c46334

scala> println(s"Requested a ${l.color} ${l.make}")
Requested a Silver Lotus
```

새로운 서브클래스인 `Lotus` 는 자신만의 새로운 필드인 `color` 를 가지며, 부모 클래스인 `Car` 를 초기화하기 위해 필드가 아닌 입력 매개변수를 취합니다.

입력 매개변수와 함께 클래스 매개변수가 함수로부터 빌려온 다른 특징으로는 매개변수의 기본값을 정의하는것이 있습니다. 이것은 호출자가 클래스의 모든 매개변수를 지정하지 않고도 인스턴스를 생성할 수 있게 해줍니다.

**Syntax: Defining a Class with Input Parameters and Default Values**

```scala
class <identifier> ([val|var] <identifier>: <type> = <expression>[, ... ])
    [extends <identifier>(<input parameters>)]
    [{ fields and methods }]
```

`Car` 클래스를 `reserved` 필드에 기본값을 사용하여 다시 정의함으로써 `make` 필드만 지정되면 클래스의 인스턴스를 생성할 수 있도록 만들어보겠습니다.

```scala
scala> class Car(val make: String, var reserved: Boolean = true,
 | val year: Int = 2015) {
 | override def toString = s"$year $make, reserved = $reserved"
 | }
defined class Car

scala> val a = new Car("Acura")
a: Car = 2015 Acura, reserved = true

scala> val l = new Car("Lexus", year = 2010)
l: Car = 2010 Lexus, reserved = true

scala> val p = new Car(reserved = false, make = "Porsche")
p: Car = 2015 Porsche, reserved = false
```

다음은 클래스 정의 구문을 클래스에서 하나 이상의 타입 매개변수를 지원하도록 바꿔보겠습니다.

**Syntax: Defining a Class with Type Parameters**

```scala
class <identifier> [type-parameters]
    ([val|var] <identifier>: <type> = <expression>[, ... ])
    [extends <identifier>[type-parameters](<input parameters>)]
    [{ fields and methods }]
```

우리만의 컬렉션을 만들고 타입 안전성이 보장되도록 타입 매개변수를 사용해보겠습니다.

```scala
scala> class Singular[A](element: A) extends Traversable[A] {
 | def foreach[B](f: A => B) = f(element)
 | }
defined class Singular

scala> val p = new Singular("Planes")
p: Singular[String] = (Planes)

scala> p foreach println
Planes

scala> val name: String = p.head
name: String = Planes
```

좀 더 많은 객체지향 스칼라의 클래스 타입들에대해 알아보겠습니다.

## More Class Types

기본 클래스외 클래스를 정의하고 생성하는 방법에 대해 알아보겠습니다.

### Abstract Classes

**추상 클래스(Abstract Class)** 는 다른 클래스들에 의해 확장되도록 설계되었으나 정작 자신은 인스턴스를 생성하지 않는 클래스입니다. 추상 클래스는 정의할 때 `class` 키워드 앞에 `abstract` 키워드를 두어 표시합니다.

추상 클래스는 구현되지 않은 필드와 메소드를 정의하지 않고 선언하여 제공합니다. 선언된 필드와 메소드는 각각 이름과 매개변수를 포함하지만, 시작값이나 구현은 포함하지 않습니다. 선언된 필드와 메소드를 가지는 추상 클래스를 확장하면서 그 자체가 추상 클래스로 표시되지 않은 클래스로 그 구현을 제공해야 합니다.

또한, 추상 클래스는 서브클래스에서 구현할 필요가 없는 자신만의 구현된 필드와 메소드를 가질 수 있습니다. 추상 클래스를 만들고 구현해보겠습니다.

```scala
scala> abstract class Car {
 | val year: Int
 | val automatic: Boolean = true
 | def color: String
 | }
defined class Car

scala> new Car()
<console>:9: error: class Car is abstract; cannot be instantiated
 new Car()

scala> class RedMini(val year: Int) extends Car {
 | def color = "Red"
 | }
defined class RedMini

scala> val m: Car = new RedMini(2005)
m: Car = RedMini@5f5a33ed
```

추상 클래스 `Car` 가 독자적으로 인스턴스를 생성할 수 없습니다. 

`Car` 를 확장하고 `color` 메소드의 값 매개ㅐ변수와 구체적인 구현을 추가한 서브클래스를 생성하여 이 문제를 해결할 수 있습니다. `RedMini` 클래스는 그 부모인 추상 클래스를 성공적으로 구현하여 `year` 만 매개변수로 받아 인스턴스를 생성할 수 있습니다.

더 나은 서브클래스를 만들기 위해 `color` 을 입력 매개변수로 취하여 새로운 서브클래스를 만들어보겠습니다.

```scala
scala> class Mini(val year: Int, val color: String) extends Car
defined class Mini

scala> val redMini: Car = new Mini(2005, "Red")
redMini: Car = Mini@1f4dd016

scala> println(s"Got a ${redMini.color} Mini")
Got a Red Mini
```

### Anonymous Classes 

부모 클래스의 메소드를 구현하는 덜 공식적인 방법은 재사용할 수 없고 이름도 없는 클래스 정의인 **익명 클래스(Anonymous Class)** 를 사용하는 것입니다.

일회적 익명 클래스를 정의하기 위해 부모 클래스의 인스턴스를 생성하고, 클래스 명과 매개변수 다음의 중괄호 안에 구현 내용을 포함하면 됩니다. 그 결과로 일회성 구현으로 해당 부모 클래스를 확장하는 인스턴스를 가지게 되지만, 전통적인 클래스 정의로부터 생성된 인스턴스처럼 사용할 수 있습니다.

Java 보편적으로 사용되는 알림을 전송하는 디자인 패턴인 `Listener` 클래스로 확인해 보겟습니다.

```scala
scala> abstract class Listener { def trigger }
defined class Listener

scala> val myListener = new Listener {
 | def trigger { println(s"Trigger at ${new java.util.Date}") }
 | }
myListener: Listener = $anon$1@59831016

scala> myListener.trigger
Trigger at Fri Jan 24 13:08:51 PDT 2014
```

`myListener` 값은 클래스 인스턴스지만, 그 클래스 정의는 자신의 인스턴스를 생성하는 동일한 표현식의 이룹입니다. 새로운 `myListener` 를 생성하려면 익명 클래스를 다시 재정의해야합니다.

다음은 익명 클래스로 만드는 것이 유용한 예제입니다. 한 줄에 익명 클래스의 인스턴스를 생성하고 이를 다른 줄에 있는 등록 함수에 전달하는 대신, 메소드 호출의 일부로 익명 클래스를 정의하는 하나의 단계로 결합할 수 있습니다. 이는 JavaScript 가 비슷한대, 특히 jQuery 형태의 이벤트 핸들러랑 비슷합니다.

```scala
scala> abstract class Listener { def trigger }
defined class Listener

scala> class Listening {
 | var listener: Listener = null
 | def register(l: Listener) { listener = l }
 | def sendNotification() { listener.trigger }
 | }
defined class Listening

scala> val notification = new Listening()
notification: Listening = Listening@66596c4c

scala> notification.register(new Listener {
 | def trigger { println(s"Trigger at ${new java.util.Date}") }
 | })

scala> notification.sendNotification
Trigger at Fri Jan 24 13:15:32 PDT 2014
```

익명 클래스에서 클래스 정의는 안정적이거나 재사용 가능할 필요가 없습니다. 서브클래스가 한 번만 필요한 상황이라면 익명 클래스 구문이 코드를 단순화하는 데 도움이 됩니다.

## More Field and Method Types

클래스에 사용할 수 있는 추가적인 필드와 메소드에 대해 살펴보겠습니다.

### Overloaded Methods

**중복 정의된 메소드(Overloaded Method)** 는 호출자에게 선택권을 제공하는 전략입니다. 클래스는 동일한 이름과 반환값을 가지지만, 다른 입력 매개변수를 가지는 둘 또는 그 이상의 메소드를 가질 수 있습니다. 하나의 메소드 이름에 여러 구현을 중복 정의하여 특정 이름으로 메소드를 호출하는 방법을 사용할 수 있습니다.

아래는 메소드를 중복 정의한 예제입니다. 메소드들은 동일한 이름을 가지고 있지만 다른 매개변수를 취합니다.

```scala
scala> class Printer(msg: String) {
 | def print(s: String): Unit = println(s"$msg: $s")
 | def print(l: Seq[String]): Unit = print(l.mkString(", "))
 | }
defined class Printer

scala> new Printer("Today's Report").print("Foggy" :: "Rainy" :: "Hot" :: Nil)
Today's Report: Foggy, Rainy, Hot
```

동일한 이름과 입력 매개변수를 가지면서 다른 반환값을 내는 두 개의 메소드가 존재할 수 없습니다. 그렇게 하는 것은 Scala 컴파일러 에러를 발생시키는데, 컴파일하는 동안 그 메소드 중 하나만 명확하게 선택할 수 있는 방법이 없기 때문입니다.

### Apply Methods

`apply` 메소드는 기본 메소드 또는 인젝터 메소드로 불리며, 메소드 이름 없이 호출될 수 있습니다. `apply` 메소드는 근본적으로 메소드 이름 없이 괄호를 사용하여 적용할 수 있는 기능을 제공하는 간단한 방법입니다. 미리 정의된 수로 숫자를 곱하는 클래스를 확인해보겠습니다.

```scala
scala> class Multiplier(factor: Int) {
 | def apply(input: Int) = input * factor
 | }
defined class Multiplier

scala> val tripleMe = new Multiplier(3)
tripleMe: Multiplier = Multiplier@339cde4b

scala> val tripled = tripleMe.apply(10)
tripled: Int = 30

scala> val tripled2 = tripleMe(10)
tripled2: Int = 30
```

`tripleMe` 인스턴스는 지정된 숫자를 3 으로 곱할 때 `apply` 이름이 없어도 사용될 수 있습니다.

```scala
scala> val l = List('a', 'b', 'c')
l: List[Char] = List(a, b, c)

scala> val character = l(1)
character: Char = b
```

`List.apply(index)` 메소드는 인덱스로 요소에 접근할 수 있게 해줍니다.

### Lazy Values

지금까지 사용한 클래스에 필드값은 모두 클래스가 처음 인스턴스를 생성할 때 만들어졌습니다. 하지만 **지연 값(Lazy Value)** 은 자신이 처음 인스턴스화될 때에만 생성됩니다. 지연값은 값을 정의할 때 val 키워드 앞에 lazy 키워드를 추가하여 만들 수 있습니다.

일반 클래스 값을 초기화하는 데 사용되는 표현식은 인스턴스 생성 시점에 한 번만 실행되는 반면에 메소드를 만드는 표현식은 메소드가 호출될 때마다 실행됩니다. 하지만 지연값을 초기화하는 표현식은 그 값이 최초로 호출될 때에만 실행됩니다.

이렇게 하여 지연값은 일종의 캐시에 저장된 함수 결과가 됩니다. 아래 예제는 일반값과 지연값이 계산되는것을 비교해서 보여줍니다.

```scala
scala> class RandomPoint {
 | val x = { println("creating x"); util.Random.nextInt }
 | lazy val y = { println("now y"); util.Random.nextInt }
 | }
defined class RandomPoint

scala> val p = new RandomPoint()
creating x
p: RandomPoint = RandomPoint@6c225adb

scala> println(s"Location is ${p.x}, ${p.y}")
now y
Location is 2019268581, -806862774

scala> println(s"Location is ${p.x}, ${p.y}")
Location is 2019268581, -806862774
```

일반값인 `x` 필드는 인스턴스 `p` 가 생성될 때 초기화합니다. 지연값인 `y` 필드는 우리가 그 값에 처음 접근할 때 초기화됩니다. 2 번째 출력에서야 두 값은 초기화되고 고정됩니다.

지연값은 클래스 수명 내에 실행 시간과 성능에 민감한 연산이 한 번만 실행될 수 있음을 보장합니다. 지연값은 데이터베이스 커넥션 열기와 같은 경우에 사용이 됩니다.

## Packaging 

패키지는 Scala 의 코드 쳬게를 위한 시스템입니다. 패키지는 Scala 코드를 점으로 구분된 경로를 사용하여 디렉터리별로 정리할 수 있게 해줍니다. Scala 소스 파일 맨 위에서 `package` 키워드를 사용하여 그 파일의 모든 클래스가 패키지에 포함됨을 선언하면 됩니다.

**Syntax: Defining the Package for a Scala File**

```scala
package <identifier>
```

Scala 패키지 명명법은 Java 표준을 따르며, 조직이나 업무 도메인을 거꾸로 작성한 후에 분류된 체계를 경로에 추가하면 됩니다. 예를 들어 Netflix 에서 개발된 utility 메소드를 제공하는 Scala 클래스는 *com.netflix.utilities* 에 패키징됩니다.

Scala 소스 파일은 그 패키지와 일치하는 디렉터리에 저장되어야 합니다. 예를 들어, *com.netflix.utilities* 패키지의 *DateUtilities* 클래스는 *com/netflix/utilities/DateUtilities.scala* 에 저장되어야 합니다. Scala 컴파일러는 생성된 `.class` 파일을 그 패키지에 일치하는 디렉터리 구조에 저장할 것입니다.

패키지로 소스 파일을 생성하고 컴파일하여 테스트해보겠습니다. `scalac` 명령어를 사용하여 소스 파일을 컴파일하고, 현재 디렉터리에 포함된 클래스를 생성하겠습니다.

```shell
$ mkdir -p src/com/oreilly

$ cat > src/com/oreilly/Config.scala
package com.oreilly
class Config(val baseUrl: String = "http://localhost")

$ scalac src/com/oreilly/Config.scala

$ ls com/oreilly/Config.class
com/oreilly/Config.class
```

*src* 디렉터리는 현재 디렉터리의 다른 항목들과 소스 코드를 구분하는 좋은 방법이지만, 실제로 컴파일러가 사용하지는 않습니다. 컴파일러는 소스 파일까지의 상대 경로를 가져와 컴파일하고, 컴파일러를 실행한 디렉터리로부터 상대 경로로 클래스 파일을 생성합니다.

### Accessing Packaged Classes

패키징된 클래스는 점으로 구분된 전체 패키지 경로와 클래스 이름으로 접근할 수 있습니다. 앞의 `Config` 예제에서 `Config` 라는 이름의 클래스는 *com.oreilly.Config* 로 접근할 수 있습니다.

*java.util* 패키지에 있는 JDK 의 `Date` 클래스에 접근해보겠습니다.

```scala
scala> val d = new java.util.Date
d: java.util.Date = Wed Jan 22 16:42:04 PDT 2014
```

다른 패키지의 클래스에 접근하는 더 편리한 방식으로는 패키지를 현재 네임스페이스에 **임포트(import)** 하는 것입니다.

**Syntax: Importing a Packaged Class**

```scala
import <package>.<class>
```

네임스페이스에 임포트한 뒤에 새로운 `Date` 를 만들어 보겠습니다. 이렇게 하면 클래스를 이름으로만 참조할 수 있습니다.

```scala
scala> import java.util.Date
import java.util.Date

scala> val d = new Date
d: java.util.Date = Wed Jan 22 16:49:17 PDT 2014
```

`Date` 클래스는 *java.util* 패키지에 존재하지만, 이제는 현재 네임스페이스의 일부이기도 합니다.

`import` 명령어는 값을 반환하지 않는 문장입니다. `import` 는 코드에서 문장을 사용할 수 있는 곳이라면 어디서나 사용할 수 있습니다.

`println` 함수 중간에 Java 의 `UUID` 클래스를 `import` 문을 추가해보겠습니다.

```scala
scala> println("Your new UUID is " + {import java.util.UUID; UUID.randomUUID})
Your new UUID is 47ba6844-3df5-403e-92cc-e429e614c9e5
```

전체 패키지와 클래스를 임포트하는것과 달리 패키지 일부를 임포트하면, 클래스를 임포트하는 것만큼은 아니지만 전체 패키지를 참조할 필요가 줄어듭니다. Scala 의 임포트는 **누적되는(Accumulative)** 구조이기 때문입니다.

부분 패키지 경로를 이용하여 `Date` 에 접근해보겠습니다.

```scala
scala> import java.util
import java.util
scala> val d = new util.Date
d: java.util.Date = Wed Jan 2229 06:18:52 PDT 2014
```

Scala 에서는 `_` 연산자를 이용하여 패키지 전체 내용을 한 번에 임포트할 수 있습니다. 그러면 그 패키지의 모든 클래스가 네임스페이스에 추가됩니다.

현재 네임스페이스에 가변적인 컬렉션을 모두 임포트하고, 그 패키지의 `ArrayBuffer` 와 `Queue` 컬렉션을 시험해보겠습니다.

```scala
scala> import collection.mutable._
import collection.mutable._

scala> val b = new ArrayBuffer[String]
b: scala.collection.mutable.ArrayBuffer[String] = ArrayBuffer()

scala> b += "Hello"
res0: b.type = ArrayBuffer(Hello)

scala> val q = new Queue[Int]
q: scala.collection.mutable.Queue[Int] = Queue()

scala> q.enqueue(3, 4, 5)

scala> val pop = q.dequeue
pop: Int = 3

scala> println(q)
Queue(4, 5)
```

패키지의 모든 클래스와 하위 패키지를 임포트 하는데 잠재적인 문제가 있습니다. 임포트한 패키지가 네임스페이스에 이미 있는 이름과 중복되는 클래스 이름을 가지고 있다면, 네임스페이스에 있던 클래스에 접근이 불가능합니다.

예를들어 *collection.mutable* 패키지에 `Map` 과 동일한 이름을 가진 가변적인 `Map` 이 있으면 전체 *mutable* 패키지를 임포트한 후에 우리가 생성한 `Map` 은 가변적이 될것입니다.

전체 패키지를 임포트하는 대신 **임포트 그룹(Import Group)** 을 사용할 수 있습니다. 이 특징을 사용하면 전체 패키지 대신 임포트할 여러 클래스의 이름을 나열할 수 있습니다.

**Syntax: Using an Import Group**

```scala
import <package>.{<class 1>[, <class 2>...]}
```

임포트 그룹을 사용하여 `Map` 을 임포트하지 않고 직접 `Queue` 와 `ArrayBuffer` 를 임포트할 수 있습니다.

```scala
scala> import collection.mutable.{Queue,ArrayBuffer}
import collection.mutable.{Queue, ArrayBuffer}

scala> val q = new Queue[Int]
q: scala.collection.mutable.Queue[Int] = Queue()

scala> val b = new ArrayBuffer[String]
b: scala.collection.mutable.ArrayBuffer[String] = ArrayBuffer()

scala> val m = Map(1 -> 2)
m: scala.collection.immutable.Map[Int,Int] = Map(1 -> 2)
```

가변적인 `Map` 과 불변의 `Map` 컬렉션을 이름 충돌 없이 네임스페이스에 추가할 방법이 있습니다. **임포트 별창(Import Alias)** 을 사용하면 됩니다.

**Syntax: Using an Import Alias**

```scala
import <package>.{<original name>=><alias>}
```

*collection.mutable.Map* 컬렉션을 표준 불변의 `Map` 과 충돌하지 않게 별칭을 사용해보겠습니다.

```scala
scala> import collection.mutable.{Map=>MutMap}
import collection.mutable.{Map=>MutMap}

scala> val m1 = Map(1 -> 2)
m1: scala.collection.immutable.Map[Int,Int] = Map(1 -> 2)

scala> val m2 = MutMap(2 -> 3)
m2: scala.collection.mutable.Map[Int,Int] = Map(2 -> 3)

scala> m2.remove(2); println(m2)
Map()
```

### Packaging Syntax

패키지를 지정하는 덜 보편적인 형태는 `packaging` 구문을 사용하는 것입니다. 여기서 패키지는 중괄호로 그 클래스들을 감싼 블록이 됩니다. 이 형태에서는 패키지 블록 내의 클래스들만이 해당 패키지의 멤버들로 지정됩니다. 

이는 동일한 파일이 서로 다른 패키지의 구성원이 되는 클래스들을 포함할 수 있게 해줍니다.

**Syntax: Packaging Classes**

```scala
package <identifier> { <class definitions> }
```

```scala
scala> :paste -raw
// Entering paste mode (ctrl-D to finish)

package com {
 package oreilly {
 class Config(val baseUrl: String = "http://localhost")
 }
}

// Exiting paste mode, now interpreting.

scala> val url = new com.oreilly.Config().baseUrl
url: String = http://localhost
```

## Privacy Controls 

코드 패키징은 결국 패키지 접근을 관리하기 위해 **프라이버시 제어(Privacy Control)** 를 사용할 수 있습니다. 

프라이버시 제어 중 하나는 필드와 메소드를 `protected` 로 표시하는 것으로, 그 필드와 메소드의 접근을 동일 클래스 또는 그 클래스의 서브클래스의 코드에서만 가능하도록 제한합니다.

`val`, `var`, `def`, 키워드 앞에 `protected` 키워드를 사용하여 해당 항목이 보호받고 있음을 표시합니다.

외부 클래스의 접근으로부터 필드를 보호하는 예제입니다. 하지만 서브클래스에서는 그 필드에 여전히 접근할 수 있습니다.

```scala
scala> class User { protected val passwd = util.Random.nextString(10) }
defined class User

scala> class ValidUser extends User { def isValid = ! passwd.isEmpty }
defined class ValidUser

scala> val isValid = new ValidUser().isValid
isValid: Boolean = true
```

좀 더 엄격한 수준의 보호가 필요한 경우 `private` 으로 표시하면 됩니다. 이는 필드와 메소드의 접근을 정의한 클래스에서만 가능하도록 제한합니다.

`private` 을 사용한 예제를 보겠습니다.

```scala
scala> class User(private var password: String) {
 | def update(p: String) {
 | println("Modifying the password!")
 | password = p
 | }
 | def validate(p: String) = p == password
 | }
defined class User

scala> val u = new User("1234")
u: User = User@94f6bfb

scala> val isValid = u.validate("4567")
isValid: Boolean = false

scala> u.update("4567")
Modifying the password!

scala> val isValid = u.validate("4567")
isValid: Boolean = true
```

## Privacy Access Modifiers

키워드 `private` 과 `protected` 는 클래스 - 계층구조 제약을 제공하지만, 클래스 항목들에까지 세밀하기 접근 제어가 필요할 때가 있습니다. 예를 들어, 퍼시스턴스 패키지의 클래스는 버그를 줄이고 단일 접근점을 보장하기 위해 그 데이터베이스 레벨의 메소드 중 일부만 동일 패키지의 다른 클래스에 드러내기를 원할 수 있습니다.

`private` 와 `protected` 지정에 더하여 **접근 변경자(Access Modifier)** 를 기술하여 이 수준의 제어를 추가할 수 있습니다. 접근 변경자는 패키지, 클래스 또는 인스턴스와 같이 주어진 지점까지만 유효함을 명시하고 그 지점 이내에서는 비활성화 됩니다.

예를 들어, 메소드가 패키지 외부의 호출자에게만 `private` 한다면 패키지 내부에서는 자유롭게 접근할 수 있습니다. 어떤 필드가 패키지 내부에서가 아니라 동일 클래스의 다른 인스턴스로부터 `private` 한다면, 그 필드는 동일 인스턴스 내에 있는 코드에서만 접근할 수 있습니다.

접근 변경자를 명시하기 위해서는 키워드 `private` 또는 `protected` 다음에 꺽쇠 괄호 안에 패키지나 클래스 이름을 작성하거나 `this` 를 사용하면 됩니다.

```scala
scala> :paste -raw
// Entering paste mode (ctrl-D to finish)
package com.oreilly {
    private[oreilly] class Config {
        val url = "http://localhost"
    }
 
    class Authentication {
        private[this] val password = "jason" // TODO change me
        def validate = password.size > 0
    }

    class Test {
        println(s"url = ${new Config().url}")
    }

 // Exiting paste mode, now interpreting.

scala> val valid = new com.oreilly.Authentication().validate
valid: Boolean = true

scala> new com.oreilly.Test
url = http://localhost
res0: com.oreilly.Test = com.oreilly.Test@4c309d4d

scala> new com.oreilly.Config
<console>:8: error: class Config in package oreilly cannot be
 accessed in package com.oreilly 
    new com.oreilly.Config
                    ^
```

## Final and Sealed Classes 

**종단 클래스(Final Class)** 구성원은 서브 클래스에서 재정의할 수 없습니다. 값, 변수, 메소드를 `final` 키워드로 표시하면 그 구현은 모든 서브클래스에서 사용할 구현임을 보장합니다.

클래스 전체를 `final` 키워드로 표시할 수 있는데, 이 경우에는 해당 클래스의 서브 클래스를 만들 수 없도록 방지합니다.

만약 종단 클래스가 요구사항에 비해 너무 제한적이라면, 대신 **봉인 클래스(Sealed Class)** 사용을 고려하면 됩니다. 봉인 클래스는 클래스의 서브클래스가 부모 클래스와 동일한 파일에 위치하도록 제한합니다. 

클래스를 봉인하여 클래스의 계층 구조에 대해 안전하게 가정하는 코드를 작성 할 수 있습니다. 클래스 정의앞에 `sealed` 키워드를 붙이면 됩니다.

