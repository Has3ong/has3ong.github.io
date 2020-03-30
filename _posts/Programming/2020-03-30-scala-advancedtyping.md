---
title : Scala Advanced Typing
tags :
- Type
- Implicit Class
- Tuple
- Object
- Scala
---

*이 포스트는 [Learning Scala](http://188.166.46.4/get/PDF/Jason%20Swartz-Learning%20Scala_125.pdf) 를 바탕으로 작성하였습니다.*

처음으로 다룰 특징은 고수준의 튜플과 함수 리터럴이 일반 클래스로 구성된다는 점입니다.

```scala
scala> val t1: (Int, Char) = (1, 'a')
t1: (Int, Char) = (1,a)

scala> val t2: (Int, Char) = Tuple2[Int, Char](1, 'a')
t2: (Int, Char) = (1,a)

scala> val f1: Int=>Int = _ + 2
f1: Int => Int = <function1>

scala> val f2: Int=>Int = new Function1[Int, Int] { def apply(x: Int) = x * 2 }
f2: Int => Int = <function1>
```

다른 타입은 **묵시적(Implicit)** 클래스 입니다. 기존 클래스에 새로운 메소드와 필드를 적용하는 타입에 안전한 방식을 제공합니다. 기존 클래스를 새로운 클래스로 자동 변환하여 묵시적 클래스의 메소드와 필드는 원래의 클래스에서 클래스의 구조를 변경하지 않고도 직접 호출할 수 있습니다.

```scala
scala> object ImplicitClasses {
 |  implicit class Hello(s: String) { def hello = s"Hello, $s" }
 |  def test = {
 |      println( "World".hello )
 |  }
 | }
defined object ImplicitClasses

scala> ImplicitClasses.test
Hello, World
```

묵시적 매개변수는 묵시적 클래스와 비슷하게 묵시적 메소드에 추가될 로컬 네임스페이스에 제공합니다. 매개변수 중 일부를 묵시적으로 정의한 메소드는 묵시적 지역값을 가지는 코드에 의해 호출될 수 있지만, 명시적 매개변수로도 호출될 수 있습니다.

```scala
scala> object ImplicitParams {
 |  def greet(name: String)(implicit greeting: String) = s"$greeting, $name"
 |  implicit val hi = "Hello"
 |  def test = {
 |      println( greet("Developers") )
 |  }
 | }
defined object ImplicitParams

scala> ImplicitParams.test
Hello, Developers
```

마지막으로 타입 매개변수로 상한경계(`<:`) 와 하한 경계(`>:`) 를 알아보겠습니다.

```scala
scala> class Base { var i = 10 }; class Sub extends Base
defined class Base
defined class Sub

scala> def increment[B <: Base](b: Base) = { b.i += 1; b }
increment: [B <: Base](b: Base)Base
```

타입 매개변수는 새로운 인스턴스에 결합될 때에도 그와 호환되는 타입으로 변할 수도 있습니다.

타입 매개변수가 공변하는(covariant) 것으로 지정되면, 타입 매개변수는 호환되는 기본 타입으로 변할 수 있습니다. `List` 컬렉션은 공변하기 때문에 서브클래스의 리스트는 기본 클래스의 리스트로 전환될 수 있습니다.

```scala
scala> val l: List[Base] = List[Sub]()
l: List[Base] = List()
```

## Tuple and Function Value Classes 

튜플은 `TupleX[Y]` 케이스 클래스의 인스턴스로 구현됩니다. `X` 는 1 부터 22 까지 튜플의 입력 매개변수의 **개수(Arity)** 를 나타냅니다. 타입 매개변수 `Y` 는 `Tuple1` 을 위한 단일 타입 매개변수로부터 `Tuple22` 를 위한 22 개의 타입 매개변수까지 다양하게 지정할 수 있습니다.

`Tuple1[A]` 는 단일 필드 _1 을 가지며, `Tuple2[A, B]` 는 _1 과 _2 를 가지는 등 입력 매개변수 수가 늘어남에 따라 증가합니다. 괄호 구문(`(1, 2, true)`) 로 튜플을 생성할 때 동일 개수의 매개변수를 가지는 튜플 클래스가 그 값들로 인스턴스화 합니다. 즉, 튜플은 케이스 클래스라 생각하면 됩니다.

`TupleX[Y]` 케이스 클래스는 각각 동일한 수를 가지는 `ProductX` 트레이트를 확장합니다. 이 트레이트는 그 튜플의 입력 매개변수 개수를 반환하는 `productArity` 와 튜플의 `n` 번째 요소에 접근하는 타입에 안정적이지 않은 `productElement` 같은 연산을 제공합니다. 더불어 튜플에 패턴 매칭을 가능하게 하는 `unapply` 를 구현하는 동반 객체를 제공합니다.

괄호 구문이 아니라 `Tuple2` 케이스 클래스를 인스턴스화하여 튜플을 생성해보겠습니다.

```scala
scala> val x: (Int, Int) = Tuple2(10, 20)
x: (Int, Int) = (10,20)

scala> println("Does the arity = 2? " + (x.productArity == 2))
Does the arity = 2? true
```

튜플 케이스 클래스는 표현력 있는 구문을 데이터 중심으로 구현한 것입니다. 함숫값 클래스는 유사하지만, 로직 중심의 구현을 제공합니다.

함숫값은 함수의 매개변수 개수를 기반으로 0 부터 22 까지 번호가 붙는 `FunctionX[Y]` 트레이트의 인스턴스로 구현됩니다. 타입 매개변수 `Y` 는 `Function0` 를 위한 한 개의 타입 매개변수부터 `Function22` 를 위한 23 개의 타입 매개변수까지 다양합니다.

즉, Scala 컴파일러는 함수 리터럴을 `FunctionX` 를 확장하는 새로운 클래스의 `apply()` 메소드의 본체로 전환합니다. 이 메커니즘이 Scala 의 함숫값이 모든 함수가 클래스 메소드로 구현되도록 제한하는 JVM 과 호환되도록 해줍니다.

일반 구문으로 함수 리터럴을 작성하여 `FunctionX` 타입을 사용해보고, `FunctionX.apply()` 메소드로 확인해보겠습니다. 아래 예제는 `Function1[A, B]` 트레이트를 확장하는 익명 클래스를 만들 것입니다.

```scala
scala> val hello1 = (n: String) => s"Hello, $n"
hello1: String => String = <function1>

scala> val h1 = hello1("Function Literals")
h1: String = Hello, Function Literals

scala> val hello2 = new Function1[String,String] {
 |  def apply(n: String) = s"Hello, $n"
 | }
hello2: String => String = <function1>

scala> val h2 = hello2("Function1 Instances")
h2: String = Hello, Function1 Instances

scala> println(s"hello1 = $hello1, hello2 = $hello2")
hello1 = <function1>, hello2 = <function1>
```

`Function1` 트레이트는 `Function0` 나 다른 어떤 `FunctionX` 트레이트에도 없는 두 개의 특별한 메소드를 가지고 있습니다. 이 메소드를 사용하여 2 개 이상의 `Function1` 인스턴스를 새로운 인스턴스로 결합할 수 있으며, 새로운 인스턴스는 호출시 모든 함수를 순서대로 실행합니다.

유일한 제약사항은 첫 번째 함수의 반환 타입이 두 번째 함수의 입력 타입과 맞아야 하며, 실행 순서상 이전의 반환 타입과 그 다음의 입력 타입이 맞아야합니다.

메소드 `andThen` 은 두 함숫값으로부터 새로운 함숫값을 생성하며, 왼쪽 인스턴스 다음에 오른쪽에 있는 인스턴스를 실행합니다. 메소드 `compose` 는 반대 방향으로 동작합니다. 함수 리터럴로 확인해보겠습니다.

```scala
scala> val doubler = (i: Int) => i*2
doubler: Int => Int = <function1>

scala> val plus3 = (i: Int) => i+3
plus3: Int => Int = <function1>

scala> val prepend = (doubler compose plus3)(1)
prepend: Int = 8

scala> val append = (doubler andThen plus3)(1)
append: Int = 5
```

## Implicit Parameters 

만약 매개변수를 하나도 지정하지 않고 함수를 호출하면 누락된 매개변수는 함수가 올바르게 동작하게끔 어딘가로부터 값을 받아와야 합니다. 기본 매개변수를 지정하는것도 한 방법이지만, 이 경우 함수가 누락된 매개변수에 맞는 값이 무엇인지 알아야 합니다.

다른 방법으로 **묵시적 매개변수(Implicit Parameter)** 를 이용하는 것으로, 호출자는 자신의 네임스페이스의 기본값을 제공합니다. 호출자는 지역값을 묵시적으로 표시할 수 있어서 이를 묵시적 매개변수로 채우는 데 사용할 수 있습니다. 함수가 묵시적 매개변수를 위해 값을 지정하지 않고 호출되면, 묵시적인 지역값이 선택되어 함수 호출에 추가됩니다.

묵시적인 값, 변수, 함수 매개변수를 표시하려면 키워드 `implict` 를 사용하면 됩니다.

아래는 묵시적인 매개변수로 정의한 함수입니다. 함수를 객체의 메소드로 정의하여 그 함수의 네임스페이스를 호출자의 네임스페이스의 분리시킵니다.

```scala
scala> object Doubly {
 |  def print(num: Double)(implicit fmt: String) = {
 |      println(fmt format num)
 |  }
 | }
defined object Doubly

scala> Doubly.print(3.724)
<console>:9: error: could not find implicit value for parameter fmt: String
                Doubly.print(3.724)

scala> Doubly.print(3.724)("%.1f")
3.7
```

새로운 `print` 메소드는 묵시적 매개변수를 가지므로 네임스페이스에 묵시적 값 / 변수를 지정하거나 명시적으로 매개변수를 추가해야 합니다. 명시적 매개변수를 추가해도 잘 동작합니다.

묵시적 매개변수를 명시적으로 전달하지 않고 `print` 메소드를 호출하도록 묵시적인 지역값을 추가하겠습니다.

```scala
scala> case class USD(amount: Double) {
 |  implicit val printFmt = "%.2f"
 |  def print = Doubly.print(amount)
 | }
defined class USD

scala> new USD(81.924).print
81.92
```

묵시적 값은 명시적으로 전달할 필요 없이 `Doubly.print` 메소드를 위한 2 번째 매개변수 그룹으로 선택됩니다.

묵시적 매개변수는 Scala 라이브러리에 아주 많이 사용됩니다. 묵시적 매개변수는 주로 컬렉션 빌더나 기본 컬렉션 순서와 같이 호출자가 중복 정의하거나 그렇지 않으면 무시할 수 있는 기능을 제공합니다.

## Implicit Classes 

Scala 의 다른 묵시적 특징으로는 본질적으로만 묵시적 매개변수와 유사한 것으로 클래스를 이용한 묵시적 전환입니다. **묵시적 클래스(Implicit Class)** 는 다른 클래스로부터 자동 전환을 제공하는 유형의 클래스입니다. 타입 A 의 인스턴스를 타입 B 로 자동전환하여 타입 A 의 인스턴스는 마치 타입 B 의 인스턴스인 듯이 타입 B 의 필드와 메소드를 가진 것처럼 보일 수 있습니다.

Scala 컴파일러는 인스턴스에 접근하는 알려지지 않은 필드나 메소드를 발견하면 묵시적 전환을 사용합니다. 컴파일러는 현재의 네임스페이스에서 (1) 인스턴스를 인수로 받아 (2) 누락된 필드나 메소드를 구현하는 묵시적 전환을 찾습니다. 조건에 맞는것을 발견하면 컴파일러는 묵시적 클래스에 자동 전환을 추가하여 그 묵시적 타입상 필드나 메소드의 접근을 지원합니다. 조건에 일치하는 것을 발견하지 못하면 컴파일 에러가 발생합니다.

다음은 모든 정숫값에 `fishes` 메소드를 추가하는 묵시적 클래스를 보여줍니다. 묵시적 클래스는 정숫값을 취하고, 정수 타입에 추가하고자 하는 `fishes` 메소드를 정의합니다.

```scala
scala> object IntUtils {
 | implicit class Fishies(val x: Int) {
 |      def fishes = "Fish" * x
 |  }
 | }
defined object IntUtils

scala> import IntUtils._
import IntUtils._

scala> println(3.fishes)
FishFishFish
```

`Fishies` 는 정수를 자기 자신으로 묵시적으로 변환하여 `fishes()` 메소드가 모든 정수에 대해 정의되도록 합니다. 사용하기 전에 묵시적 클래스는 해당 네임스페이스에 추가되어 `fishes()` 메소드는 모든 정수에서 호출될 수 있습니다.

묵시적 클래스는 필드와 메소드를 이식할 수 있게 만들지만, 정의하고 사용하는 데에는 몇 가지 제약이 따릅니다.

1. 묵시적 클래스는 다른 객체, 클래스 또는 트레이트 안에 정의되어야만 한다.
2. 묵시적 클래스는 하나의 묵시적이지 않은 클래스 인수를 받아야 한다.
3. 묵시적 클래스명은 현재 네임스페이스의 다른 객체, 클래스, 트레이트와 충돌해서는 안된다.
   1. 케이스 클래스는 묵시적 클래스를 사용될 수 없는데, 자동으로 생성된 동반 객체가 이 규칙에 어긋나기 때문이다.

`scala.Predef Object` 객체 내의 묵시적 클래스가 아니라면 자동으로 묵시적 전환을 할 수 없습니다. Scala 라이브러리의 일부인 이 객체의 구성원은 자동으로 네임스페이스에 추가됩니다. 이 객체는 여러 타입 특징들 가운데 Scala 의 표현력 있는 구문 중 일부를 가능하게 하는 묵시적 전환을 가지고 있습니다.

아래는 화살표 연산자를 가능하게 하는 묵시적 클래스의 간략 버전입니다.

```scala
implicit class ArrowAssoc[A](x: A) {
    def ->[B](y: B) = Tuple2(x, y)
}
```

묵시적 클래스는 유용한 메소드를 기존 클래스에 추가하는 훌룡한 방법입니다. 

## Types 

클래스는 데이터와 메소드를 포함하는 항목이며, 단일의 구체적인 정의를 가집니다. 타입은 클래스 명세서로, 그 요건에 부합하는 단일 클래스 또는 여러 클래스와 일치합니다. 예를 들어 `Option` 클래스는 타입이지만 `Option[Int]` 도 타입입니다.

데이터와 메소드를 포함하면서 단일의 구체적인 정의를 포함할 수 있는 항목으로, 트레이트에 대해서도 동일하게 말할 수 있습니다. 타입은 클래스 명세서이지만 트레이트와 동일하게 동작합니다. 하지만 객체는 타입으로 간주하지 않습니다. 객체는 싱글턴이며, 타입을 확장할 수 있으나 타입 자체이지는 않습니다.

### Type Aliases 

**타입 별칭(Type Alias)** 은 기존의 특정 타입에 새롭게 명명한 타입을 생성합니다. 컴파일러는 이 새로운 타입 별칭을 일반 클래스에서 정의한 것처럼 처리합니다. 따라서 타입 별칭으로부터 새로운 인스턴스를 생성하고 이를 타입 매개변수에서 클래스 대신 사용하며, 값, 변수, 함수 반환 타입에서 지정할 수 있습니다.

별칭이 부여된 클래스가 타입 매개변수를 갖는다면, 타입 매개변수를 타입 별칭에 추가하거나 특정 타입으로 타입 매개변수를 고칠 수 있습니다.

새로운 타입 별칭을 정의하려면 `type` 키워드를 사용합니다.

**Syntax: Defining a Type Alias**

```scala
type <identifier>[type parameters] = <type name>[type parameters]
```

몇 가지 타입을 만들어 보겠습니다.

```scala
scala> object TypeFun {
 |  type Whole = Int
 |  val x: Whole = 5
 |
 |  type UserInfo = Tuple2[Int,String]
 |  val u: UserInfo = new UserInfo(123, "George")
 |
 |  type T3[A,B,C] = Tuple3[A,B,C]
 |  val things = new T3(1, 'a', true)
 | }
defined object TypeFun

scala> val x = TypeFun.x
x: TypeFun.Whole = 5

scala> val u = TypeFun.u
u: TypeFun.UserInfo = (123,George)

scala> val things = TypeFun.things
things: (Int, Char, Boolean) = (1,a,true)
```

예제에서 타입 `Whole` 은 추상 클래스 `Int` 의 별칭입니다. 또한, 타입 `UserInfo` 는 `Tuple2[Int, String]` 의 별칭입니다. `Tuple2` 는 인스턴스화될 수 있는 케이스 클래스이므로 타입 별칭 `UserInfo` 로 부터 직접 인스턴스화할 수 있습니다. 마지막으로 `T3` 타입은 매개변수를 고치지 않았으므로 어떤 타입으로도 인스턴스화 될 수 있습니다.

타입 별칭은 특정 지역 이름으로 기존 타입을 참조하는 유용한 방법입니다. `Tuple2[Int, String]` 은 `UserInfo` 로 명명되면 더 유용할 것입니다. 그러나 다른 고급 타입 특징들처럼 타입 별칭은 신중한 객체지향 설계를 대체해서는 안됩니다.

### Abstract Types

타입 별칭이 단일 클래스로 해석하는 반면, **추상 타입(Abstract Type)** 은 0, 하나, 다수의 클래스로 해석할 수 있는 명세서입니다. 추상 타입은 타입 별칭과 유사하지만, 인스턴스를 생성하는 데 사용할 수 없습니다.

추상 타입은 보편적으로 전달받을 수 있는, 허용 가능한 타입의 범위를 지정하기 위해 타입 매개변수로 사용됩니다. 또한, 추상 클래스에서 구체적인 서브클래스가 구현해야만 하는 타입을 선언하기 위해 사용할 수 있습니다.

트레이트는 지정되지 않은 타입을 가지는 타입 별칭을 포함할 수 있습니다. 타입 선언은 메소드 시그니처에서 재사용될 수 있으며, 서브클래스에 의해 채워져야만 합니다. 예제 트레이트를 생성해 보겠습니다.

```scala
scala> class User(val name: String)
defined class User

scala> trait Factory { type A; def create: A }
defined trait Factory

scala> trait UserFactory extends Factory {
 |  type A = User
 |  def create = new User("")
 | }
defined trait UserFactory
```

`Factory` 의 추상 타입 `A` 는 `create` 메소드의 반환 타입으로 사용됩니다. 구체적인 서브클래스에서 이 타입은 특정 클래스의 타입 별칭으로 재정의됩니다.

이 트레이트와 클래스를 작성하는 다른 방법은 타입 매개변수를 사용하는 것입니다. 이전 트레이트와 클래스를 타입 매개변수로 구현하면 다음과 같습니다.

```scala
scala> trait Factory[A] { def create: A }
defined trait Factory

scala> trait UserFactory extends Factory[User] { def create = new User("") }
defined trait UserFactory
```

추상 타입은 일반 클래스를 설계할 때 타입 매개변수 대신 사용할 수 있습니다. 매개변수화된 타입을 원한다면 타입 매개변수가 효과적입니다. 그렇지 않다면 추상 타입이 더 적합할 수 있습니다. `UserFactory` 예제에선 타입 별칭을 정의하는 대신 매개변수화가 가능한 타입과도 잘 동작합니다.

이 예제에선 `Factory` 트레이트의 서브클래스에서 허용되는 타입의 제한이 없습니다. 하지만, 타입의 경계를 지정할 수 있으면 더 유용합니다. 상한과 하한 경계는 어떤 타입의 구현도 특정 기준을 만족할 것을 보장합니다.

### Bounded Types 

경계가 있는 타입은 특정 클래스로 규정되거나 그의 서브타입이나 기본타입으로 제한됩니다.

**상한 경계(Upper Bound)** 는 타입을 해당 타입 또는 그 서브타입 중 하나로 제한합니다. 즉, 상한 경계는 타입이 무엇이어야 하는지를 정의하고 다형성을 통해 서브타입을 허용합니다. **하한 경계(Lower Bound)** 는 타입을 해당 타입 또는 그 타입이 확장한 기본 타입 중 하나로 제한합니다.

타입의 상한 경계는 상한 경계 관계 연산자(`<:`) 로 지정할 수 있습니다.

**Syntax: Upper Bounded Types**

```scala
<identifier> <: <upper bound type>
```

경계를 가지는 타입을 실습하기 전에 테스트를 위한 클래스를 정의하겠습니다.

```scala
scala> class BaseUser(val name: String)
defined class BaseUser

scala> class Admin(name: String, val level: String) extends BaseUser(name)
defined class Admin

scala> class Customer(name: String) extends BaseUser(name)
defined class Customer

scala> class PreferredCustomer(name: String) extends Customer(name)
defined class PreferredCustomer
```

상한 경계를 가지는 매개변수를 취하는 함수를 정의한다.

```scala
scala> def check[A <: BaseUser](u: A) { if (u.name.isEmpty) println("Fail!") }
check: [A <: BaseUser](u: A)Unit

scala> check(new Customer("Fred"))

scala> check(new Admin("", "strict"))
Fail!
```

타입 매개변수 `A` 는 `BaseUser` 타입과 동일하거나 이를 확장한 타입만으로 제한됩니다. 이는 매개변수 `u` 가 `name` 필드에 접근할 수 있게 해줍니다. 상한 경계 제약이 없다면 알려지지 않은 타입에서 `name` 필드에 접근하는 것은 컴파일 에러가 발생합니다. `u` 매개변수가 정확한 타입을 지켜야 이 `check` 함수의 미래 버전이 필요한 경우 올바른 타입으로 이를 반환할 것입니다.

상한 경계 연산자의 덜 제한적인 형태로는 **뷰 경계(View-Bound)** 연산자(`<%`) 가 있습니다. 상한 경계 연산자는 타입을 요구하지만, 뷰 경계 또한 그 타입으로 취급될 수 있는 모든것을 지원합니다. 따라서 뷰 경계는 묵시적 전환을 할 수 있으므로 요청받은 타입이 아닌 타입을 허용하지만, 요청 받은 타입으로 전활할 수 있습니다.

상한 경계는 더 제약이 따르는데, 타입 요건의 일부로 묵시적 전환을 고려하지 않기 때문입니다.

상한 경계의 반대는 하한 경계로, 허용 가능한 가장 낮은 클래스를 지정합니다. 하한 경계 관계 연산자(`>:`) 를 이용하여 타입의 하한 경계를 지정합니다.

****

```scala
<identifier> >: <lower bound type>
```

`Customer` 타입보다 더 낮지 않은 타입을 반환하는 함수를 생성해보겠습니다.

```scala
scala> def recruit[A >: Customer](u: Customer): A = u match {
 | case p: PreferredCustomer => new PreferredCustomer(u.name)
 | case c: Customer => new Customer(u.name)
 | }
recruit: [A >: Customer](u: Customer)A

scala> val customer = recruit(new Customer("Fred"))
customer: Customer = Customer@4746fb8c

scala> val preferred = recruit(new PreferredCustomer("George"))
preferred: Customer = PreferredCustomer@4cd8db31
```

새로운 `PreferredCustomer` 인스턴스가 반환되었지만, `preferred` 값의 타입은 반환 타입으로 설정되어 `Customer` 보다 낮지 않음을 보장합니다.

경계가 있는 타입은 추상 타입을 선언하고 이를 선언된 메소드에서 사용하는 추상 클래스입니다. 구체적인 서브클래스는 이 타입 선언을 타입 별칭으로 구현합니다. 그 타입 별칭을 정의된 메소드에서 사용합니다. 그 결과, 그 클래스의 구현이 메소드를 구현하지만 호환 가능한 타입만 사용됨을 보장합니다.

```scala
scala> abstract class Card {
 | type UserType <: BaseUser
 | def verify(u: UserType): Boolean
 |
 | }
defined class Card

scala> class SecurityCard extends Card {
 | type UserType = Admin
 | def verify(u: Admin) = true
 | }
defined class SecurityCard

scala> val v1 = new SecurityCard().verify(new Admin("George", "high"))
v1: Boolean = true

scala> class GiftCard extends Card {
 | type UserType = Customer
 | def verify(u: Customer) = true
 | }
defined class GiftCard

scala> val v2 = new GiftCard().verify(new Customer("Fred"))
v2: Boolean = true
```

### Type Variance 

상한 또는 하한 경계를 추가하면 타입 매개변수를 더 제한적으로 만들지만, 타입 가변성이 추가되어 타입 매개변수를 덜 제한적으로 만듭니다. **타입 가변성(Type Variance)** 은 타입 매개변수가 기본 타입 또는 서브타입을 만족하기 위해 조정할 수 있습니다.

기본적으로 타입 매개변수는 변하지 않습니다. 타입 - 매겨변수화된 클래스의 인스턴스는 그 클래스와 매개변수화된 타입에만 호환됩니다. 이는 타입 매개변수가 기본 타입인 값에 저장될 수 없습니다.

다음은 Scala 의 다형성을 잘 보여주는 예제인데, 더 낮은 타입이 더 높은 타입의 값에 저장 되는 것을 허용하는 것을 보여줍니다. 아래 예제는 두 부분으로 이루어진 자동차 클래스 계층 구조를 사용할 것입니다.

```scala
scala> class Car { override def toString = "Car()" }
defined class Car

scala> class Volvo extends Car { override def toString = "Volvo()" }
defined class Volvo

scala> val c: Car = new Volvo()
c: Car = Volvo()
```

그렇지만 동일한 다형성을 기반으로 하는 조정이 타입 매개변수에는 성립하지 않습니다.

```scala
scala> case class Item[A](a: A) { def get: A = a }
defined class Item

scala> val c: Item[Car] = new Item[Volvo](new Volvo)
<console>:12: error: type mismatch;
 found : Item[Volvo]
 required: Item[Car]
Note: Volvo <: Car, but class Item is invariant in type A.
You may wish to define A as +A instead. (SLS 4.5)
 val c: Item[Car] = new Item[Volvo](new Volvo)
 ```

`Volvo` 인스턴스는 타입 `Car` 의 값에 할당될 수 있지만, `Item[Volvo]` 인스턴스는 `Item[Car]` 값에 할당될 수 없습니다. 기본적으로 변하지 않는 타입 매개변수는 그 매개변수가 호환되는 경우라도 다른 타입에 맞출 수 없습니다.

이를 해결하기 위해 `Item` 의 타입 매개변수를 **공변(Covariant)** 하게 만들어야 합니다. 공변하는 타입 매개변수는 필요에 따라 자동으로 기본 타입중 하나로 변할 수 있습니다. 공변하는 타입 매개변수는 타입 매개변수 앞에 덧셈 기호(`+`) 를 붙여서 표시할 수 있습니다.

`Item[Volvo]` 타입이 `Item[Car]` 로 변할 수 있도록 `Item` 클래스를 공변 타입 매개변수로 재정의하겠습니다.

```scala
scala> case class Item[+A](a: A) { def get: A = a }
defined class Item

scala> val c: Item[Car] = new Item[Volvo](new Volvo)
c: Item[Car] = Item(Volvo())

scala> val auto = c.get
auto: Car = Volvo()
```

타입 매개변수 `A` 는 이제 공변하며, 서브타입으로부터 기본 타입으로 변할 수 있습니다. 즉, `Item[Volvo]` 의 인스턴스는 `Item[Car]` 타입을 가지는 값에 할당될 수 있습니다.

`Item.get()` 메소드는 비슷하게 타입 매개변수의 공변성을 지원합니다. 인스턴스가 `Item[Volvo]` 이고 실제 `Volvo` 를 포함하지만, 그 값의 타입은 `Item[Car]` 입니다. 따라서 `c.get` 의 반환 타입은 `Car` 가 됩니다.

입력 매개변수가 공벼넞ㄱ이라는 것은 서브 타입에 제한되지만, 기본 타입으로 호출할 수 있음을 의미합니다. 이것은 불가능한 변환인데, 기본 타입은 서브 타입으로 변환될 수 없기 때문입니다.

메소드의 입력 매개변수 타입으로 공변 타입 매개변수를 사용했을 때 Scala 컴파일러의 출력을 보겠습니다.

```scala
scala> class Check[+A] { def check(a: A) = {} }
<console>:7: error: covariant type A occurs in contravariant position in
    type A of value a
        class Check[+A] { def check(a: A) = {} }
```

Scala 컴파일러의 에러가 설명하는 대로, 메소드 매개변수에 사용된 타입 매개변수는 공변성을 띄는 것이 아니라 반공변성을 띕니다. **반공병성(Contravariance)** 은 타입 매개변수가 서브타입으로 변할 수 있는 것으로 서브타입이 기본 타입으로 변하는 다형성 변환의 정반대 방향을 이룹니다.

반공변적인 타입 매개변수는 빼기 기호(`-`) 를 타입 매개 변수 앞에 붙여서 표시합니다.

```scala
scala> class Check[-A] { def check(a: A) = {} }
defined class Check
```

이와 다른 방식으로, 타입 매개변수를 불변의 상태로 둘 수 있습니다. `check()` 메소드는 클래스의 타입 매개변수와 똑같은 타입의 입력 매개변수로만 호출할 수 있습니다.

```scala
scala> class Check[A] { def check(a: A) = {} }
defined class Check
```

반공변성과 공변성의 차이를 보여주는 더 나은 예제를 보겠습니다. 포괄적인 예제로 공변 그리고 반공변 타입 매개변수를 정의해보겠습니다.

`Car` 클래스의 서브클래스 `Volvo` 그리고 `Volvo` 의 새로운 서브클래스인 `VolvoWagon` 을 사용해보겠습니다.

공변성을 시험하기 위해 `Item` 을 사용하고, 반공변성을 시험하기 위해 `Check` 를 사용하겠습니다. 이 방식으로 서브클래스와 기본클래스로 실험하여 어느 것이 동작하는지 찾을 수 있습니다.

```scala
scala> class Car; class Volvo extends Car; class VolvoWagon extends Volvo
defined class Car
defined class Volvo
defined class VolvoWagon

scala> class Item[+A](a: A) { def get: A = a }
defined class Item

scala> class Check[-A] { def check(a: A) = {} }
defined class Check

scala> def item(v: Item[Volvo]) { val c: Car = v.get }
item: (v: Item[Volvo])Unit

scala> def check(v: Check[Volvo]) { v.check(new VolvoWagon()) }
check: (v: Check[Volvo])Unit
```

`Item` 클래스는 분명하게 공변 타입 매개변수가 필요합니다. `Item` 클래스가 타입 `Volvo` 에 한정되면, `get()` 메소드는 `Car` 타입의 값에 저장할 수 있어야 하는 `Volvo` 를 반환할 것입니다.

`Check` 클래스는 분명히 반공변 타입 매개변수를 필요로 합니다. `Check` 클래스가 타입 `Volvo` 에 한정되면 그 `check()` 메소드는 `Volvo` 를 취하고 `VolvoWagon` 의 인스턴스를 전달할 수 있어야 합니다.

두 번째 부분에서 기본 클래스, 정확히 일치하는 클래스, 서브클래스로 메소드를 호출할 것입니다.

```scala
scala> item( new Item[Car](new Car()) )
<console>:14: error: type mismatch;
    found : Item[Car]
    required: Item[Volvo]
        item( new Item[Car](new Car()) )
              ^

scala> item( new Item[Volvo](new Volvo) )

scala> item( new Item[VolvoWagon](new VolvoWagon()) )

scala> check( new Check[Car]() )

scala> check( new Check[Volvo]() )

scala> check( new Check[VolvoWagon]() )
<console>:14: error: type mismatch;
    found : Check[VolvoWagon]
    required: Check[Volvo]
        check( new Check[VolvoWagon]() )
```

공변성과 반공변성은 타입 매개변수를 덜 제한적으로 ㅁ나들지만, 어떻게 사용될 수 있는지에 대한 제약이 존재합니다. 만약 이들을 사용해야 할지 여부에 대한 확신이 들지 않는다면 타입 매개변수를 불변의 상태로 두는것을 고려해야합니다.

### Package Objects

묵시적 매개변수, 묵시적 전환, 타입 별칭과 같이 이 장에서 다루었던 고급 타입의 대부분은 다른 타입 내부에서만 정의될 수 있습니다. 이러한 제약을 둠으로써 대부분의 고급 타입은 명시적으로 임포트를 통해서만 네임스페이스에 추가될 수 있습니다.

한 가지 예외는 `scala.Predef` 객체로 그 내용은 Scala 네임스페이스에 자동으로 추가됩니다. 다른 예외는 패키지 객체를 통하는 것인데, 이는 각 패키지의 유일한 객체로 해당 패캐지 코드의 네임스페이스에도 임포트 됩니다.

**패키지 객체(Package Object)** 는 자신이 영향을 미치는 패키지에 위치한 파일 *package.scala* 에 정의됩니다. 패키지 객체는 키워드 `object` 안에 키워드 `package` 를 추가하여 정의할 수 있습니다.

다음은 새로운 타입 별칭 `Mappy` 를 정의한 패키지 객체입니다.

```scala
// located on com/oreilly/package.scala
package object oreilly {
 type Mappy[A,B] = collection.mutable.HashMap[A,B]
}
```

이 패키지에 정의된 어떤 클래스 트레이트, 객체도 `Mappy[A, B]` 타입 별칭을 가져오며, 직접 사용할 수 있습니다.