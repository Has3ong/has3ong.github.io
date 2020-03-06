---
title : Scala Functions
tags :
- Function
- Scala
---

*이 포스트는 [Learning Scala]() 를 바탕으로 작성하였습니다.*

Scala 에서 함수는 이름을 가진 재활용가능한 표식입니다.

표준 함수형 프로그래밍의 방법론을 따르면 가능한 **순수 함수** 를 구성하면 훌룡한 이점을 얻을 수 있다고 합니다. 순수 함수는 다음과 같은 특징을 가집니다.

* Has one or more input parameters
* Performs calculations using only the input parameters
* Returns a value
* Always returns the same value for the same input
* Does not use or affect any data outside the function
* Is not affected by any data outside the function

순수 함수는 근본적으로 수학에서 함수의 정의와 동일하게 입력 매개변수로만 유도되는 계산을 의미하며, 함수형 프로그래밍에서 프로그램의 구성 요소가 됩니다.

**Syntax: Defining an Input-less Function**

```scala
def <identifier> = <expression>
```

가장 기본적인 형태로, `Scala` 함수는 표현식을 감싼 이름이 부여된 **wrapper** 입니다. 아래는 입력값이 없는 함수를 정의하고 호출하는 예제를 보겠습니다.

```scala
scala> def hi = "hi"
hi: String

scala> hi
res0: String = hi
```

함수의 반환 타입은 값이나 변수의 타입과 마찬가지로, 명시적으로 정의되지 않더라도 존재합니다. 값과 변수처럼 명시적 타입을 지정해야 가독성이 좋습니다.

**Syntax: Defining a Function with a Return Type**

```scala
def <identifier>: <type> = <expression>
```

```scala
scala> def hi: String = "hi"
hi: String
```

전체 함수 정의를 알아보겠습니다.

**Syntax: Defining a Function**

```scala
def <identifier>(<identifier>: <type>[, ... ]): <type> = <expression>
```

기본적인 곱셈 연산을 수행하는 함수를 만들어 보겠습니다.

```scala
scala> def multiplier(x: Int, y: Int): Int = { x * y }
multiplier: (x: Int, y: Int)Int

scala> multiplier(6, 7)
res0: Int = 42
```

함수의 본문은 표현식 또는 표현식 블록으로 구성되어 있으며, 마지막 줄은 표현식과 함수의 반환값이 됩니다. 함수의 마지막줄에는 키워드 `return` 을 사용하여 반환값을 명시적으로 지정하고 종료할 수 있습니다.

```scala
scala> def safeTrim(s: String): String = {
 | if (s == null) return null
 | s.trim()
 | }
safeTrim: (s: String)String
```

## Procedures 

**프로시저(Procedure)** 는 반환값을 가지는 함수입니다. `println()` 호출과 같은 문장으로 끝나는 모든 함수 또한 프로시저입니다. 만일 문장으로 끝나는 명시적인 반환 타입이 없는 단순 함수를 사용한다면, Scala 컴파일러는 함수의 반환 타입을 값이 없는 `Unit` 타입으로 추론할 것입니다.

한 줄 이상의 포로시저에 대해 명시적으로 타입을 Unit 으로 지정하면, 코드를 읽는 사용자에게 반환값이 없다는 것을 분명하게 나타날 것입니다.

다음은 간단한 **로깅(Logging)** 프로시저로, 각각 묵시적 반환 타입과 명시적 반환 타입으로 정의 되었습니다.

```scala
scala> def log(d: Double) = println(f"Got value $d%.2f")
log: (d: Double)Unit

scala> def log(d: Double): Unit = println(f"Got value $d%.2f")
log: (d: Double)Unit

scala> log(2.23535)
Got value 2.24
```

지금은 비공식적으로 deprecate 되었지만, 프로시저를 정의하는 다른 방식으로는 `Unit` 반환 타입과 프로시저 본문 앞의 등호를 사용하지 않고 정의하는 방법입니다. 이 구문을 이용하면 `log()` 메소드를 다음과 같이 작성할 수 있습니다.

```scala
scala> def log(d: Double) { println(f"Got value $d%.2f") }
log: (d: Double)Unit
```

## Functions with Empty Parentheses 

입력 매개변수가 없는 함수를 정의하고 호출하는 다른 방법으로는 빈 괄호를 사용하는 것입니다. 이 스타일이 더 좋은 방식일 수 있는데, 함수와 값을 분명하게 구분해 주기 때문입니다.

**Syntax: Defining a Function with Empty Parentheses**

```scala
def <identifier>()[: <type>] = <expression>
```

이러한 함수는 빈괄호를 사용하거나 괄호를 빼고도 호출할 수 있습니다.

```scala
scala> def hi(): String = "hi"
hi: ()String

scala> hi()
res1: String = hi

scala> hi
res2: String = hi
```

하지만 그 반대로는 성립하지 않습니다. 이 규칙은 괄호 없이 함수를 호출하는 것을 함수로 그 함수의 반환값을 호출하는 것과 혼동하는 것을 방지합니다.

## Function Invocation with Expression Blocks 

단일 매개변수를 사용하여 함수를 호출할 때, 괄호 안에 값을 넣는 대신 중괄호 안에 표현식 블록을 사용하여 매개변수를 전달할 수 있습니다. 함수 호출을 위해 표현식 블록을 사용하면 연산 또는 다른 행위를 처리하고 그 블록의 반환값으로 함수를 호출할 수 있습니다.

**Syntax: Invoking a Function with an Expression Block**

```scala
<function identifier> <expression block>
```

함수 호출을 위해 표현식 블록을 사용하는 것이 더 나은 경우는 함수에 계산된 값을 전달해야 할 때 입니다. 값을 계산하고 그 값을 함수에 전달할 지역값에 저장하는 대신, 표현식 블록 내에서 연산을 할 수 있습니다. 표현식 블록은 함수를 호출하기 전에 평가되며, 그 블록의 반환값은 함수 인수로 사용됩니다.

함수 호출을 위해 사용되는 함수 블록 내부에서 값을 계산하는 예제는 아래와 같습니다.

```scala
scala> def formatEuro(amt: Double) = f"€$amt%.2f"
formatEuro: (amt: Double)String

scala> formatEuro(3.4645)
res4: String = €3.46

scala> formatEuro { val rate = 1.32; 0.235 + 0.7123 + rate * 5.32 }
res5: String = €7.97
```

## Recursive Functions 

**재귀 함수(Recursive Function)** 는 자기 자신을 호출하는 함수로, 특정 타입의 매개변수 또는 함수 호출이 무한 루프에 빠지는 것을 피하고자 검사할 외부 조건과 함께 호추랗ㅂ니다. 재귀 함수는 함수형 프로그래밍에서 보편적으로 사용하는데, 데이트 구조 또는 계산을 가변적인 데이터를 사용하지 않고 반복하는 방법을 제공하기 때문입니다. 그리고 이것이 가능한 이유는 각 함수 호출이 함수 매개변수를 저장하기 위한 자신만의 **스택(Stack)** 을 가지기 때문입니다.

다음은 재귀 함수의 예로, 주어진 양의 지수만큼 정수를 거듭제곱합니다.

```scala
scala> def power(x: Int, n: Int): Long = {
 | if (n >= 1) x * power(x, n-1)
 | else 1
 | }
power: (x: Int, n: Int)Long

scala> power(2, 8)
res6: Long = 256

scala> power(2, 1)
res7: Long = 2

scala> power(2, 0)
res8: Long = 1
```

재귀 함수를 사용할 때 조심해야하는 문제는 **Stack Overflow** 입니다. 재귀 함수를 많이 호출하여 스택 공간을 모두 소진하면서 발생합니다.

이를 예방하기 위해 Scala 컴파일러는 재귀적 호출이 추가적인 스택 공간을 사용하지 않도록 **꼬리-재귀(Tail-Recursion)** 을 사용하여 일부 재귀 함수를 최적화 할 수 있습니다.

꼬리-재귀를 사용하면 새로운 스택 공간을 생성하지 않는 대신 현행 함수의 스택 공간을 사용합니다. 마지막 문장이 재귀적 호출인 함수만이 Scala 컴파일에 의해 꼬리-재귀를 위해 최적화될 수 있습니다. 만일 자기 자신을 호출한 결과가 직접적인 반환값 외의 다른 것을 위해 사용된다면, 최적화될 수 없습니다.

꼬리-재귀를 위해 최적화될 함수를 표시하는 **함수 어노테이션(Function Annotation)** 이 존재합니다. 함수 어노테이션은 Java 에서 가져온 특별한 구문입니다.

함수가 꼬리-재귀를 사용할것이라는 점을 표시하기 위해 함수 정의 앞 또는 그 전 줄에 텍스트 `@annotation.tailrec` 를 추가하면 됩니다. 만약 최적화할 수 없다면 컴파일러 에러가 출력됩니다.

```scala
scala> @annotation.tailrec
 | def power(x: Int, n: Int): Long = {
 |  if (n >= 1) x * power(x, n-1)
 |  else 1
 | }
<console>:9: error: could not optimize @tailrec annotated method power:
it contains a recursive call not in tail position
 if (n >= 1) x * power(x, n-1)
```

`if` 와 `else` 조건문을 바꾸고 다시 해보겠습니다.

```scala
scala> @annotation.tailrec
 | def power(x: Int, n: Int): Long = {
 |   if (n < 1) 1
 |   else x * power(x, n-1)
 | }
<console>:11: error: could not optimize @tailrec annotated method power:
it contains a recursive call not in tail position
 else x * power(x, n-1)
```

재귀적 호출의 결과를 취하고 값으로 곱하게 되어 마지막 문장이 재귀적 호출이 아니라 곱셈이 되었습니다.

이를 고치기 위해 함수의 결과를 곱하는 대신 곱셈을 함수의 시작 부분으로 옮기겠습니다.

```scala
scala> @annotation.tailrec
 | def power(x: Int, n: Int, t: Int = 1): Int = {
 |  if (n < 1) t
 |  else power(x, n-1, x*t)
 | }
power: (x: Int, n: Int, t: Int)Int

scala> power(2,8)
res9: Int = 256
```

`tailrec` 어노테이션과 함께 컴파일이 성공한 모습입니다. 이를 통해 최적화되어 뒤에 따라오는 호출이 더 많은 스택 프레임을 추가하지 않습니다.

## Nested Functions 

함수는 이름을 가진 매개변수화된 표현식 블록이며, 표현식 블록은 중첩이 가능합니다.

메소드 내에 반복되어야 할 필요가 있는 로직을 가지고 있으나, 외부 메소드로 추정되어 득이 되지 않는 경우 함수 내부에 존재하는 내부 함수를 정의하여 사용할 수 있습니다.

```scala
scala> def max(a: Int, b: Int, c: Int) = {
 | def max(x: Int, y: Int) = if (x > y) x else y
 | max(a, max(b, c))
 | }
max: (a: Int, b: Int, c: Int)Int

scala> max(42, 181, 19)
res10: Int = 181
```

중첩 함수인 `max(Int, Int)` 내부의 로직은 한 번 정의되었지만, 외부 함수 내에서 두 번 사용함으로 중복된 로직을 줄이고 전체 함수를 단순화 시킵니다.

위에서 중첩된 함수는 이름만 같지 매개변수가 다르기 때문에 두 함수 사입의 충돌은 없습니다.

## Calling Functions with Named Parameters 

함수를 호출할 때에는 원래 함수가 정의될 때의 순서대로 매개변수가 지정되어야 하는 것이 관례입니다. 하지만 Scala 에서는 이름으로 매개변수를 호출할 수 있으므로 매개변수 순서와 상관없이 지정하는것이 가능합니다.

**Syntax: Specifying a Parameter by Name**

```scala
<function name>(<parameter> = <value>)
```

아래 예제에선 두 개매의 매개변수를 가지는 함수가 호출됩니다.

```scala
scala> def greet(prefix: String, name: String) = s"$prefix $name"
greet: (prefix: String, name: String)String

scala> val greeting1 = greet("Ms", "Brown")
greeting1: String = Ms Brown

scala> val greeting2 = greet(name = "Brown", prefix = "Mr")
greeting2: String = Mr Brown
```

## Parameters with Default Values 

함수를 정의할 때 맞이하는 보편적인 문제는 재사용을 극대화하기 위해 어떤 입력 변수를 사용할것인지 결정하는 것입니다. Scala 와 Java 에서는 함수의 이름은 갖지만 매개변수가 다른 동일한 함수를 여러버전으로 제공하는 기능이 있습니다.

이 기법은 함수명이 다른 ㅇ비력값에 대해 재사용되기 때문에 **함수 오버로딩(Function Overloading)** 이라고 합니다.

Scala 에선 어떤 매개변수에도 기본값을 지정하고, 호출자가 해당 매개변수를 선택적으로 사용할 수 있도록 합니다.

**Syntax: Specifying a Default Value for a Function Parameter**

```scala
def <identifier>(<identifier>: <type> = <value>): <type>
```

```scala
scala> def greet(prefix: String = "", name: String) = s"$prefix$name"
greet: (prefix: String, name: String)String

scala> val greeting1 = greet(name = "Paul")
greeting1: String = Paul
```

꼭 필요한 매개변수를 먼저 오도록 재구조화하면, 매개변수 이름을 사용하지 않고도 함수를 호출할 수 있습니다.

```scala
scala> def greet(name: String, prefix: String = "") = s"$prefix$name"
greet: (name: String, prefix: String)String
scala> val greeting2 = greet("Ola")
greeting2: String = Ola
```

표현상 기본값을 가지는 매개변수가 필수 매개변수 다음에 오도록 함수 매개변수를 구조화하는것이 좋습니다.

## Vararg Parameters 

Scala 는 **가변 매개변수(Vararg Parameter)** 를 지원함으로써 정해지지 않은 개수의 입력 인수들로 함수를 정의할 수 있도록 합니다. 가변 매개변수는 **불변 매개변수(Nonvararg Parameter)** 앞에 놓일 수 없는데, 이는 둘을 구분할 수 없기 때문입니다.

가변 매개변수를 표시하려면 함수 정의에서 매개변수 타입 뒤에 * 을 추가하면 됩니다.

```scala
scala> def sum(items: Int*): Int = {
 | var total = 0
 | for (i <- items) total += i
 | total
 | }
sum: (items: Int*)Int

scala> sum(10, 20, 30)
res11: Int = 60

scala> sum()
res12: Int = 0
```

## Parameter Groups 

매개변수 리스트를 괄호로 묶어 매개변수화한 함수 정의를 알아봤습니다. Scala 는 매개변수 리스트를 어려 그룹의 매개변수로 나누는 방식을 제공하며, 각 매개변수 그룹은 괄호로 구분됩니다.

아래 예제는 `max` 함수 예제의 두 입력 매개변수를 각각 별도의 그룹으로 나누었습니다.

```scala
scala> def max(x: Int)(y: Int) = if (x > y) x else y
max: (x: Int)(y: Int)Int

scala> val larger = max(20)(39)
larger: Int = 39
```

## Type Parameters 

Scala 에선 값 매개변수를 보완하기 위해 값 매개변수 또는 반환값에 사용될 타입을 지시하는 **타입 매개변수(Type Parameter)** 를 전달할 수 있습니다. 타입 매개변수를 사용하면 이러한 타입들이 고정되어 있던 상태에서 함수 호출자에 의해 설정될 수 있는 상태로 바뀜에 따라 함수의 유연성과 재사용성이 높아질 수 있습니다.

타입 매개변수로 정의하는 구문은 다음과 같습니다.

**Syntax: Defining a Function’s Type Parameters**

```scala
def <function-name>[type-name](parameter-name>: <type-name>): <type-name>...
```

이 타입 매개변수로 어떻게 사용할 수 있는지 알아보겠습니다. 입력값을 그대로 반환하는 간단한 함수(항등함수) 를 만들어보겠습니다. 이 경우에는 String 으로 정의된 함수입니다.


```scala
def identity(s: String): String = s
```

이 함수는 유용할 수 있지만 String 만 호출이 가능하고 Int 로는 호출될 수 없습니다. 그렇다면 모든 타입에 동작하는 루트타입 Any 를 사용해보겠습니다.

```scala
scala> def identity(a: Any): Any = a
identity: (a: Any)Any

scala> val s: String = identity("Hello")
<console>:8: error: type mismatch;
 found : Any
 required: String
 val s: String = identity("Hello")
 ^
```

우리는 결괏값을 String 에 할당하기 기대하지만 함수의 반환 타입이 Any 이므로 컴파일 에러가 발생합니다.

해결책으로는 타입을 매개변수화하면 호출자가 사용하는 어떤 타입에도 맞게됩니다.

```scala
scala> def identity[A](a: A): A = a
identity: [A](a: A)A

scala> val s: String = identity[String]("Hello")
s: String = Hello

scala> val d: Double = identity[Double](2.717)
d: Double = 2.717
```

이 항등함수의 매개변수는 A 이며, 값 매개변수 a 처럼 유일한 식별자 입니다. A 는 값 매개변수 a 와 함수의 반환 타입을 정의하기 위해 사용됩니다.

컴파일러가 타입 매개변수를 추론할 수 있음을 보여주기 위해 이전 예제의 두 함수 호출에서 타입 매개변수를 제거해보겠습니다.

```scala
scala> val s: String = identity("Hello")
s: String = Hello

scala> val d: Double = identity(2.717)
d: Double = 2.717
```

정상적으로 작동합니다. Scala 컴파일러는 타입 매개변수의 타입과 반환값이 할당되는 값의 타입을 추론할 수 있습니다.

```scala
scala> val s = identity("Hello")
s: String = Hello

scala> val d = identity(2.717)
d: Double = 2.717
```

## Methods and Operators 

**메소드(Method)** 는 클래스에서 정의된 함수로, 클래스의 모든 인스턴스에서 사용할 수 있습니다. Scala 에서 메소드를 호출하는 표준 방식은 메소드 이름 앞에 인스턴스의 이름과 점 구분자를 붙이는 **삽입점 표기법(infix dot notation)** 을 사용하는 것입니다.

**Syntax: Invoking a Method with Infix Dot Notation**

```scala
<class instance>.<method>[(<parameters>)]
```

String 타입에 적용하는 메소드 중 하나를 호출하겠습니다.

```scala
scala> val s = "vacation.jpg"
s: String = vacation.jpg

scala> val isJPEG = s.endsWith(".jpg")
isJPEG: Boolean = true
```

객체의 메소드를 연산자 표기법으로 호출하려면 단일 매개변수를 취하려는 메소드를 선택해서, 객체, 메솓, 단일 매개변수를 공백으로 구분하면됩니다.

**Syntax: Invoking a Method with Operator Notation**

```scala
<object> <method> <parameter>
```

이 표기법을 정확한 용어로 말하면 **중위 연산자 표기법(Infix Operator Notation)** 이 됩니다.

```scala
scala> d compare 18.0
res17: Int = 1

scala> d + 2.721
res18: Double = 68.363
```

## Writing Readable Functions

가독성있는 함수를 만들기위한 방법으로 함수 적절한곳에 주석을 추가하는 것입니다.

많은 방법 중 하나는 함수에 Scaladoc 헤더를 추가하는 것입니다. Scaladoc 헤더는 함수 주석의 표준 포맷입니다. 아래 예시를 통해 보여드리겠습니다.

```scala
scala> /**
 | * Returns the input string without leading or trailing
 | * whitespace, or null if the input string is null.
 | * @param s the input string to trim, or null.
 | */
 | def safeTrim(s: String): String = {
 | if (s == null) return null
 | s.trim()
 | }
safeTrim: (s: String)String
```










