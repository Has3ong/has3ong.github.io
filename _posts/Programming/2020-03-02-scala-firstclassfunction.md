---
title : Scala First-Class Functions
tags :
- Higher-Order Function
- First-Class Functions
- Scala
---

Scala 에서는 다른 데이터 타입과 마찬가지로 식별자에 할당되지 않고도 리터럴 형태로 생성될 수 있으며, 값, 변수, 또는 데이터 구조처럼 컨테이너에 저장될 수 있는 **일급 함수(First-Class Function)** 이 있으며,

다른 함수를 매개변수로 받아들이거나 반환값으로 함수를 사용하는 함수를 **고차 함수(Higher-Order Function)** 가 있습니다.

## Function Types and Values 

함수의 타입은 함수의 입력 타입과 반환값 타입의 단순한 그룹으로, 입력 타입으로부터 출력 타입으로의 방향을 나타내는 화살표로 배열합니다.

**Syntax: A Function Type**

```scala
([<type>, ...]) => <type>
```

이 방법은 특정 이름을 사용하지 않고 함수를 실제로 묘사하는 방법입니다. 함수 시그니처는 이름, 입력, 출력 이므로 함수의 타입은 입력과 출력이어야합니다.

예를들어, 함수 `def double(x: Int): Int = x * 2` 는 함수 타입 Int => Int 를 가지며 이는 함수가 단일 Int 매개변수를 가지며 Int 를 반환함을 의미합니다.

함수의 본문, 입력값을 2 로 곱하는 단순 곱셈은 함수의 타입에 영향을 주지 않습니다. 이 정보 외의 나머지 입력 타입과 반환 타입이며, 따라서 디르이 함수 타입 자체를 이루게 됩니다.

REPL 에서 함수 타입을 이용해보게씃ㅂ니다. 다음 예제는 함수를 생성하고 이를 함숫값에 할당합니다.

```scala
scala> def double(x: Int): Int = x * 2
double: (x: Int)Int

scala> double(5)
res0: Int = 10

scala> val myDouble: (Int) => Int = double
myDouble: Int => Int = <function1>

scala> myDouble(5)
res1: Int = 10

scala> val myDoubleCopy = myDouble
myDoubleCopy: Int => Int = <function1>

scala> myDoubleCopy(5)
res2: Int = 10
```

`myDouble` 값의 명시적 타입은 이를 함수 호출이 아닌 함숫값으로 식별하는 데 필요합니다. 함수로 할당된 함수값을 정의하는 다른 방법은 와일드카드 연산자를 사용하는 것입니다.

**Syntax: Assigning a Function with the Wildcard Operator**

```scala
val <identifier> = <function name> _
```

`myDouble` 함수값을 가지고 이 구문을 사용해보겠습니다.

```scala
scala> def double(x: Int): Int = x * 2
double: (x: Int)Int

scala> val myDouble = double _
myDouble: Int => Int = <function1>

scala> val amount = myDouble(20)
amount: Int = 40
```

이때 `myDouble` 의 명시적 함수 타입은 함수 호출과 구별하기 위해 필요하지 않습니다. 언더스코어는 미래의 함수 호출에 대한 자리표시자 역할을 하며, `myDouble` 에 저장할 수 있는 함숫값을 반환합니다.

다중 입력값을 가지는 함수를 살펴보기 위해 명시적 함수 타입을 복습해보겠습니다. 다중 입력을 가지는 함수 타입은 입력 타입을 괄호로 명시적으로 묶어야 하며, 그 모습은 결국 매개변수 이름이 없는 함수 정의의 형태를 띠게 됩니다.

다음은 괄호로 감싼 다중 매개변수를 사용하는 명시적 함수 타입으로 정의된 함숫값의 예를 보여줍니다.

```scala
scala> def max(a: Int, b: Int) = if (a > b) a else b
max: (a: Int, b: Int)Int

scala> val maximize: (Int, Int) => Int = max
maximize: (Int, Int) => Int = <function2>

scala> maximize(50, 30)
res3: Int = 50
```

명시적인 타입 대신 와일드카드 연산자를 사용할 수 있지만, 다중 매개변수를 타입에 어떻게 기술하는지 보여주기 위한 것입니다.

마지막으로, 입력값이 없는 함수 타입을 보여주겠습니다. 빈 괄호는 값이 없음을 나타내는 Unit 타입의 리터럴 표현이기도 합니다.

```scala
scala> def logStart() = "=" * 50 + "\nStarting NOW\n" + "=" * 50
logStart: ()String

scala> val start: () => String = logStart
start: () => String = <function0>

scala> println( start() )
==================================================
Starting NOW
==================================================
```

## Higher-Order Functions 

**고차 함수(Higher-Order Function)** 는 입력 매개변수나 반환값으로 함수 타입의 값을 가지는 함수입니다.

```scala
scala> def safeStringOp(s: String, f: String => String) = {
 | if (s != null) f(s) else s
 | }
safeStringOp: (s: String, f: String => String)String

reverser: (s: String)String
scala> def reverser(s: String) = s.reverse

scala> safeStringOp(null, reverser)
res4: String = null

scala> safeStringOp("Ready", reverser)
res5: String = ydaeR
```

위 예제는 기존 함수를 고차 함수에 매개변수로 전달하는 방법입니다.

## Function Literals 

실제 동작하지만 이름이 없는 함수인 **함수 리터럴(Function Literal)** 을 생성하여 새로운 함숫값에 할당해보겠습니다.

```scala
scala> val doubler = (x: Int) => x * 2
doubler: Int => Int = <function1>

scala> val doubled = doubler(22)
doubled: Int = 44
```

함수 리터럴이 이름을 가지지 않은 함수이지만, 이 개념과 화살표 구문의 사용은 많은 이름을 가지고 있습니다.

**익명 함수(Anonymous Function)**

익명 함수는 함수 리터럴에 대한 Scala 언어의 공시적인 이름이다.

**람다 표현식(Lambda Expression), 람다(Lambda)**

수학에서의 람다 계산 구문에서 유래된 용어다.

**function0, function1, function2**

함수 리터럴에 대한 Scala 컴파일러의 용어로 인수의 개수를 기반합니다.

**Syntax: Writing a Function Literal**

```scala
([<identifier>: <type>, ... ]) => <expression>
```

함숫값을 정의하고 새로운 함수 리터럴에 할당해보겠습니다.


```scala
scala> val greeter = (name: String) => s"Hello, $name"
greeter: String => String = <function1>

scala> val hi = greeter("World")
hi: String = Hello, World
```

함수 리터럴은 근본적으로 매개변수화된 표현식입니다. 우리는 값을 반환하는 표현식에 대해서는 알지만, 이제 표현식의 입력값을 매개변수화하는 방법도 가지게 되었습니다.

`max()` 함수를 함숫값에 할당하고, 그 다음 함수 리터럴로 `max()` 함수를 재구현해보겠습니다.

```scala
scala> def max(a: Int, b: Int) = if (a > b) a else b
max: (a: Int, b: Int)Int

scala> val maximize: (Int, Int) => Int = max
maximize: (Int, Int) => Int = <function2>

scala> val maximize = (a: Int, b: Int) => if (a > b) a else b
maximize: (Int, Int) => Int = <function2>

scala> maximize(84, 96)
res6: Int = 96
```

함수 리터럴이  항상 입력 인수가 필요한건 아닙니다. 어떤 인수도 취하지 않는 함수 리터럴도 정의할 수 있습니다.

```scala

scala> def logStart() = "=" * 50 + "\nStarting NOW\n" + "=" * 50
logStart: ()String

scala> val start = () => "=" * 50 + "\nStarting NOW\n" + "=" * 50
start: () => String = <function0>

scala> println( start() )
==================================================
Starting NOW
==================================================
```

또한, 함수 리터럴은 고차 함수 호출 내부에 정의될 수 있습니다.

```scala
scala> def safeStringOp(s: String, f: String => String) = {
 | if (s != null) f(s) else s
 | }
safeStringOp: (s: String, f: String => String)String

scala> safeStringOp(null, (s: String) => s.reverse)
res7: String = null

scala> safeStringOp("Ready", (s: String) => s.reverse)
res8: String = ydaeR
```

함수 `safeStringOp()` 는 `f` 라는 이름의 함수값을 매개변수로 받고 조건에 따라 이 함숫값을 호출합니다. 예제에서 함수 매개변수 `f` 의 타입은 `String => String` 입니다. 이미 정의한 이 타입으로 우리는 함수 리터럴에서 명시적 타입을 제거할 수 있는데, 컴파일러가 그 타입을 쉽게 추론할 수 있기 때문입니다. 또한, 명시적 타입을 제거한다는 것은 우리가 함수 리터럴에서 괄호를 제거할 수 있다는것을 의미합니다. 즉, 타입이 지정되지 않은 단일 입력값이기 때문입니다.

좀더 단순한 구문으로 호출해보겠습니다.

```scala
scala> safeStringOp(null, s => s.reverse)
res9: String = null

scala> safeStringOp("Ready", s => s.reverse)
res10: String = ydaeR
```

이렇게 명시적 타입과 괄호를 제거한 함수 리터럴에는 함수의 기본적인 본질만 남게 됩니다. 함수 리터럴은 입력 매개변수를 받아 그 매개변수로 연산을 수행한 결괏값을 반환합니다.

함수 리터럴은 매우 간단한 함수의 표현식이지만, Scala 는 **자리표시자 구문(Placeholder Syntax)** 로 이보다 더 간단한 표현식을 지원합니다.

## Placeholder Syntax 

**자리표시자 구문(Placeholder Syntax)** 은 함수 리터럴의 축약형으로, 지정된 매개변수를 와일드카드 연산자로 대체한 형태를 가집니다. 이 구문은 함수의 명시적 타입이 리터럴 외부에 지정되어 있고 매개변수가 한 번 이상 사용되지 않는 경우에 사용합니다.

지정된 매개변수 자리에 와일드카드 연산자를 이용하여 두 배 함수 리터럴을 만들어 보겠습니다.

```scala
scala> val doubler: Int => Int = _ * 2
doubler: Int => Int = <function1>
```

자리표시자 구문은 입력 매개변수가 한 번만 사용되고, 리터럴의 타입이 외부에 명시적으로 정의되어 있기 때문에 유효합니다. 자리표시자 구문을 이용하여 `safeStringOp` 를 호출해보겠습니다.

```scala
scala> def safeStringOp(s: String, f: String => String) = {
 | if (s != null) f(s) else s
 | }
safeStringOp: (s: String, f: String => String)String

scala> safeStringOp(null, _.reverse)
res11: String = null

scala> safeStringOp("Ready", _.reverse)
res12: String = ydaeR
```

함수 리터럴의 본문은 기능적으로 `s => s.reverse` 와 같지만 자리표시자 구문으로 단순화하였습니다. 입력 매개변수 `s` 에 대한 참조는 함수에 첫 번째 입력 매개변수를 나타내는 와일드카드로 대체되었습니다. 근본적으로 와일드카드는 단일 `String` 입력 매개변수입니다.

2 개의 자리표시자를 가진 예제로 어떤 순서로 동작하는지 알아보겠습니다.

```scala
scala> def combination(x: Int, y: Int, f: (Int,Int) => Int) = f(x,y)
combination: (x: Int, y: Int, f: (Int, Int) => Int)Int

scala> combination(23, 12, _ * _)
res13: Int = 276
```

다음은 3 개로 올려보겠습니다.

```scala
scala> def tripleOp(a: Int, b: Int, c: Int, f: (Int, Int, Int) => Int) = f(a,b,c)
tripleOp: (a: Int, b: Int, c: Int, f: (Int, Int, Int) => Int)Int

scala> tripleOp(23, 92, 14, _ * _ + _)
res14: Int = 2130
```

자리표시자 구문은 특히 데이터 구조와 컬렉션으로 작업할 때 유용합니다. 수많은 정렬, 필터링, 그 외 다른 데이터 구조 메소드는 일급 함수를 사용하는 경향이 있으며, 자리표시자 구문은 이 메소드들을 호출하는 데 필요한 부가적인 코드의 양을 줄여줍니다.

## Partially Applied Functions and Currying 

함수를 호출하려면 전형적으로 호출문 내에 함수의 매개변수가 모두 지정되어 있어야합니다. 하지만, 다시 호출을 다시 사용하는데, 일부 매개변수를 그대로 유지하여 이를 다시 타이핑 하는것을 피하고 싶을때 어떻게 하는지 알아보겠습니다.

먼저 다른 값이 다른 숫자의 인수인지 검사하는 두 개의 매개변수를 가지는 하나의 함수를 살펴보겠습니다.


```scala
scala> def factorOf(x: Int, y: Int) = y % x == 0
factorOf: (x: Int, y: Int)Boolean
```

만일 어떤 매개변수도 유지하지 않고 함수를 호출하는 손쉬운 방법을 원한다면 도입부에서 다른 와일드카드 연산자를 사용할 수 있습니다.

```scala
scala> val f = factorOf _
f: (Int, Int) => Boolean = <function2>

scala> val x = f(7, 20)
x: Boolean = false
```

만약 매개변수 중 일부를 유지하기 원한다면, 매개변수 중 하나의 자리를 대신하는 와일드 카드 연산자를 사용하여 그 함수를 부분적으로 **적용(Partially apply)** 할 수 있습니다. 여기서 와일드카드 연산자는 명시적인 타입을 필요하는데, 이 명시적 타입이 선언된 입력 타입으로 함숫값을 생성하는 데 사용되기 때문입니다.

```scala
scala> val multipleOf3 = factorOf(3, _: Int)
multipleOf3: Int => Boolean = <function1>

scala> val y = multipleOf3(78)
y: Boolean = true
```

새로운 함수`multipleOf3` 은 부분 적용 함수인데, 이 함수가 `factorOf()` 함수의 매개변수 전부가 아니라 그 중 일부를 포함하기 때문입니다.

하나의 매개변수 목록을 적용 매개변수와 미적용 매개변수로 나누는 대신, 한 목록의 매개변수를 적용하고 다른 목록은 적용하지 않는 이 기법을 보고 함수를 **커링(Currying)** 한다고 합니다.

```scala
scala> def factorOf(x: Int)(y: Int) = y % x == 0
factorOf: (x: Int)(y: Int)Boolean

scala> val isEven = factorOf(2) _
isEven: Int => Boolean = <function1>

scala> val z = isEven(32)
z: Boolean = true
```

함수 타입 관점에서 다중 매개변수 목록을 가지는 함수는 다중 함수의 체인으로 간주합니다. 각 분리된 매개변수 목록은 별도의 함수 호출로 간주합니다.

예제 함수 `def factorOf(x: Int, y: Int)` 의 함수 타입은 `(Int, Int) => Boolean` 입니다. 하지만 업데이트된 예제 함수 `def factorOf(x: Int)(y: Int)` 의 함수 타입은 `Int => Int => Boolean` 입니다. 이 함수를 커링하면, 함수 타입은 함수 체인 중 2 번째 함수인 `Int => Boolean` 이 됩니다.

이를 활용하여 부분 적용 함수와 커링된 함수가 제공하는 작업을 처리하는 함수 리터럴을 작성할 수 있습니다.

## By-Name Parameters 

함수 타입 매개변수의 다른 형태로는 값이나 결국에는 값을 반환하는 함수를 취할 수 있는 **이름에 의한(by-name)** 호출 매개변수가 있습니다.

**Syntax: Specifying a By-Name Parameter**

```scala
<identifier>: => <type>
```

함수 내에서 이름에 의한 매개변수가 사용될 때마다 이 매개변수는 값으로 평가받습니다. 만약 함수에 값이 전달되면 아무런 영향이 없겠지만, 함수가 전달되는 경우 그 함수를 사용할 때마다 해당 함수를 호출하게 됩니다.

이름에 의한 매개변수를 사용하면 얻게되는 이점은, 값 / 함수 매개변수와는 반대로 유연성이 높아집니다.

이름에 의한 매개변수를 가지는 함수를 호출해보겠습니다.

```scala
scala> def doubles(x: => Int) = {
 | println("Now doubling " + x)
 | x * 2
 | }
doubles: (x: => Int)Int

scala> doubles(5)
Now doubling 5
res18: Int = 10

scala> def f(i: Int) = { println(s"Hello from f($i)"); i }
f: (i: Int)Int

scala> doubles( f(8) )
Hello from f(8)
Now doubling 8
Hello from f(8)
res19: Int = 16
```

## Partial Functions 

지금까지 본 함수는 **완전 함수(Total Function)** 로 알려져 있는데, 이 함수는 입력 매개변수의 타입을 만족하는 모든 가능한 값을 적절하게 지원하기 때문입니다. `def double(x: Int) = x * 2` 와 같은 단순 함수는 완전 함수로 볼 수 있는데 `double()` 함수가 처리하지 못하는 입력값 `x` 가 존재하기 때문입니다.

하지만 어떤 함수는 입력 타입을 만족하는 모든 가능한 값을 지원하지 않는 경우도 있습니다. 예를 들어, 입력 숫자의 제곱근을 반환하는 함수는 입력 숫자가 음수이면 확실히 동작하지 않습니다. 이와 비슷하게, 주어진 수로 나누는 함수도 그 수가 0 인경우 적용할 수 없습니다. 이러한 함수를 **부분 함수(Partial Function)** 라 부르는데, 자신의 입력 데이터 중 일부에만 적용할 수 있기 때문입니다.

Scala 의 부분함수는 일련의 `case` 패턴을 자신의 입력값에 적용하는 함수 리터럴로, 입력 값이 주어진 패턴 중 최소 하나는 일치할 것을 요구합니다. 이 `case` 패턴 중 하나도 만족하지 못하는 데이터로 부분 함수를 호출하면 Scala` 에러가 납니다.

```scala
scala> val statusHandler: Int => String = {
 | case 200 => "Okay"
 | case 400 => "Your Error"
 | case 500 => "Our error"
 | }
statusHandler: Int => String = <function1>
```

이제 200, 400, 500 을 가지는 정수에만 적용되는 함수 리터럴을 가지고 있습니다. 먼저 유효한 값을 가지고 시험해보겠습니다.

```scala
scala> statusHandler(200)
res20: String = Okay

scala> statusHandler(400)
res21: String = Your Error
```

case 패턴에 안맞는 경우 아래와 같이 컴파일 에러가 발생합니다.

```scala
scala> statusHandler(401)
scala.MatchError: 401 (of class java.lang.Integer)
 at $anonfun$1.apply(<console>:7)
 at $anonfun$1.apply(<console>:7)
 ... 32 elided
```

## Invoking Higher-Order Functions with Function Literal Blocks 

이 구문의 보편적인 용도는 표현식 블록으로 유틸리티 함수를 호출하는것입니다. 예를 들어, 고차 함수는 단일 데이터베이스 세션 또는 트랜잭션에 주어진 표현식 블록을 감쌀 수 있습니다.

```scala
scala> def safeStringOp(s: String, f: String => String) = {
 | if (s != null) f(s) else s
 | }
safeStringOp: (s: String, f: String => String)String

scala> val uuid = java.util.UUID.randomUUID.toString
uuid: String = bfe1ddda-92f6-4c7a-8bfc-f946bdac7bc9

scala> val timedUUID = safeStringOp(uuid, { s =>
 | val now = System.currentTimeMillis
 | val timed = s.take(24) + now
 | timed.toUpperCase
 | })
timedUUID: String = BFE1DDDA-92F6-4C7A-8BFC-1394546043987
```

위 예제에서 여러 줄의 함수 리터럴이 값 매개변수와 함께 함수에 전달됩니다. 이 방식도 제대로 동작하지만, 이들을 같은 괄호 안에 포함시키는 것은 다루기 불편합니다.

`safeStringOp` 의 매개변수를 2 개의 별도 그룹으루 구분함으로써 이를 개선할 수 있습니다.

```scala
scala> def safeStringOp(s: String)(f: String => String) = {
 | if (s != null) f(s) else s
 | }
safeStringOp: (s: String)(f: String => String)String

scala> val timedUUID = safeStringOp(uuid) { s =>
 | val now = System.currentTimeMillis
 | val timed = s.take(24) + now
 | timed.toUpperCase
 | }
timedUUID: String = BFE1DDDA-92F6-4C7A-8BFC-139454691501
```

괄호로 값 매개변수, 독립된 함수 리터럴 블록으로 함수 매개변수를 전달함으로써 `safeStringOp` 호출이 더 깔끔해졌습니다.

이름에 의한 매개변수 하나를 취하는 함수를 예로 들어보겠습니다. 이 함수를 이름에 의한 매개변수 반환 타입과 메인 함수의 반환 타입을 위해 사용될 타입 매개변수를 이용하여 더 일반적으로 만들것입니다.

```scala
scala> def timer[A](f: => A): A = {
 | def now = System.currentTimeMillis
 | val start = now; val a = f; val end = now
 | println(s"Executed in ${end - start} ms")
 | a
 | }
timer: [A](f: => A)A

scala> val veryRandomAmount = timer {
 | util.Random.setSeed(System.currentTimeMillis)
 | for (i <- 1 to 100000) util.Random.nextDouble
 | util.Random.nextDouble
 | }
Executed in 13 ms
veryRandomAmount: Double = 0.5070558765221892
```

이 방법으로 어떠한 코드 블록도 유틸리티로 감살 수 있는 함수는 고차 함수를 *표현식 블록* 형태로 호출하는 이점입니다. 이 호출 형태를 사용하는 다른 예시에는 다음도 포함됩니다.

* 데이터베이스 트랜잭션 관리에서 고차 함수는 세션을 열고, 함수 매개변수를 호출하고, **커밋(commit)** 또는 **롤백(rollback)** 하여 트랜잭션을 종료
* 오류를 내지 않을 때까지 횟수만큼 함수 매개변수를 호출함으로써 재시도로 예상한 오류 처리
* 지역, 전역 또는 외부 값에 기반하여 조건부로 함수 매개변수 호출

