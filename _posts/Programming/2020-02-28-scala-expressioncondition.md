---
title : Scala Expressions and Conditionals
tags :
- Condition
- Expression
- Scala
---

*이 포스트는 [Learning Scala](http://188.166.46.4/get/PDF/Jason%20Swartz-Learning%20Scala_125.pdf) 를 바탕으로 작성하였습니다.*

## Expressions

**표현식(expression)** 을 값을 반환하는 코드의 단위입니다. 간단한 Scala 표현식을 알아보겠습ㄴ디ㅏ.


```scala
scala> "hello"
res0: String = hello
```

다음과 같은 표현식을 좀 더 복잡하게 만들 수 있습니다.

```scala
scala> "hel" + 'l' + "o"
res1: String = hello
```

서로 다른 방식으로 구현되어 있지만 동일한 결과를 생성합니다.

### Defining Values and Variables with Expressions

표현식으로 값과 변수를 정의하는 구문을 다시 정의해보겠습니다.

**Syntax: Defining Values and Variables, Using Expressions**

```scala
val <identifier>[: <type>] = <expression>
var <identifier>[: <type>] = <expression>
```

리터럴 값 또한 표현식의 일종이기 때문에 이 정의가 더 포괄적이며 정확합니다. 표현식은 또한 대부분의 Scala 구문을 정의하는 데 좋은 기반이 될 수 있습니다.

### Expression Blocks

여러 표현식을 중괄호를 사용하여 하나로 묶어 단일 **표현식 블록(Expression Block)** 을 만들 수 잇습니다. 표현식은 자신만의 범위를 가지며, 해당 표현식 블록에 국한된 값과 변수를 포함합니다. 그 블록의 마지막 표현식이 전체 블록의 반환값이 됩니다.

예를 들어, 블록으로 더 잘 동작할 2 개의 표현식을 한 줄로 작성해보겠습니다.

```scala
scala> val x = 5 * 20; val amount = x + 10
x: Int = 100
amount: Int = 110
```

위 표현식을 블록의 반환값으로 사용해보겠습니다.

```scala
scala> val amount = { val x = 5 * 20; x + 10 }
amount: Int = 110
```

블록의 마지막 표현식인 `x + 10` 은 블록의 반환값을 결정합니다.

표현식 블록은 필요한 만큼 여러 줄로 확장할 수 있습니다.

```scala
scala> val amount = { val x = 5 * 20; x + 10 }
amount: Int = 110
```

표현식 블록 역시 중첩이 가능하며, 표현식 블록의 각 레벨은 자신만의 고유 범위의 값과 변수를 가집니다.

간단한 예제로 삼중으로 중첩된 표현식 블록을 작성하면 아래와 같습니다.

```scala
scala> { val a = 1; { val b = a * 2; { val c = b + 4; c } } }
res5: Int = 6
```

### Statements

**문장(statement)** 은 값을 반환하지 않는 표현식입니다. 문장의 반환 타입은 값이 없음을 나타내는 Unit 입니다. Scala 프로그래밍에서 보편적으로 사용되는 문장들에는 `println()` 호출과 값/변수 정의가 포함됩니다.

예를 들어, 다음의 값 정의는 어떤 것도 반환하지 않기 때문에 문장에 해당합니다.

```scala
scala> val x = 1
x: Int = 1
```

REPL 은 `x` 의 정의를 그대로 되풀이하지만, 새로운 값을 생성하는 데 사용할 수 있는 실제 값을 반환하지 않습니다.

문장 블록은 표현식 블록과 다르게 값을 반환하지 않습니다. 문장 블록은 결과값이 없습니다. 따라서 기존 데이터를 수정하거나 그 어플리케이션 범위 밖을 변경하는 데 사용합니다.

## If..Else Expression Blocks

`If .. Else` 조건식은 표현식이 참인지 거짓인지를 따져서 실행할 코드를 선택하는 고전적인 프로그래밍 구조입니다. 많은 언어에서 `if .. else if .. else` 블록 형태를 취합니다.

하지만, 공식적인 구문으로 보자면 Scala 는 하나의 `if` 와 선택적인 `else` 블록만을 지원하며, `else if` 블록을 단일 구성체로 인식하지 않습니다.

Scala 에서는 `if .. else` 블록이 표현식 블록에 기반하고 있고, 표현식 블록은 쉽게 중첩될 수 있습니다. 따라서 `if .. else if .. else` 표현식은 중첩된 `if .. else { if .. else }` 표현식과 동일하기 때문에, 논리적으로 `if .. else if .. else` 블록와 정확히 일치하며, Scala 구문으로 두 번째 `if else` 를 외부 `if .. else` 블록에 중첩된 표현식으로 인식합니다.

간단한 `if` 블록 구문을 보면서 실제 `if` 와 `if .. else` 블록에 대해 알아보겠습니다.

### If Expressions 

**Syntax: Using an If Expression**

```scala
if (<Boolean expression>) <expression>
```

여기서 용어 부울식은 `true` 나 `false` 를 반환하는 표현식을 말합니다.

다음은 부울식이 참일 때 안내문을 출력하는 간단한 형태의 `if` 블록입니다.

```scala
scala> if ( 47 % 3 > 0 ) println("Not a multiple of 3")
Not a multiple of 3
```

47 은 3 의 배수가 아니므로 부울식은 참이며, `println` 이 실행됩니다.

`if` 블록이 표현식으로 동작할 수 있지만, 이처럼 문장이 더 잘어울립니다. `if` 블록을 표현식으로 사용하면 조건부로 값을 반환하는 경우 문제가 됩니다. 만일 부울식이 거짓을 반환하면, `if` 블록은 무엇을 반환하게 되는지 알아보겠습니다.

```scala
scala> val result = if ( false ) "what does this return?"
result: Any = ()
```

여기서 `result` 값은 타입이 지정되지 않았으므로 컴파일러는 타입 추론으로 가장 적합한 타입을 결정합니다. String 이나 Unit 타입으로 반환될 수 있으므로 컴파일러는 루트 클래스 Any 를 선택합니다. Any 가 String 과 Unit 을 아우르는 공통 클래스이기 때문입니다.

독자적인 `if` 블록과 달리 `if .. else` 블록은 표현식과 동작하는 것이 잘 어울립니다.

### If-Else Expressions

**Syntax: If .. Else Expressions**

```scala
if (<Boolean expression>) <expression>
else <expression>
```

예제를 보겠습니다.

```scala
scala> val x = 10; val y = 20
x: Int = 10
y: Int = 20

scala> val max = if (x > y) x else y
max: Int = 20
```

여기서 `x`, `y` 값이 `if` 와 `else` 표현식 전체를 이루는 것을 볼 수 있습니다. 결과값은 `max` 에 할당되며, Scala 컴파일러에서 알 수 있듯이 Int 타입인데, 두 표현식 모두 Int 타입의 값을 반환하기 때문입니다.

`if..else` 블록은 조건부 로직을 작성하는 간단하고 보편적인 방식입니다. 하지만 Scala 에는 조건부 로직을 작성하는 좀 더 우아한 방법으로 **매치 표현식(Match Expression)** 을 사용할 수 있습니다.

## Match Expressions

매치 표현식은 단일 입력항목을 평가하여 처음으로 *일치하는(Match)* 패턴이 실행되고 그 값이 반환되는, C 와 Java 의 `switch` 문과 유사합니다. Scala 의 매치표현식은 다른 언어의 `switch` 문처럼 기본으로 또는 와일드카드로 모두 잡아내는 패턴을 지원합니다.

Scala 의 매치 표현식은 타입, 정규표현식, 숫자 범위, 데이터 구조 내용같은 다양한 항목을 매칭할 수 있는 유연한 방법입니다.

**Syntax: Using a Match Expression**

```scala
<expression> match {
 case <pattern match> => <expression>
 [case...]
}
```

이전 절의 `if .. else` 를 매치 표현식으로 전환해보겠습니다. 현 버전에서는 부울식을 먼저 처리하고, 그 결과를 `true` 나 `false` 로 매치하겠습니다.

```scala
scala> val x = 10; val y = 20
x: Int = 10
y: Int = 20
scala> val max = x > y match {
 | case true => x
 | case false => y
 | }
max: Int = 20
```

매치 표현식의 또 다른 예로, 정수 상태 코드를 취해서 그에 가장 접합한 메세지를 반환해보도록 하겠습니다.

```scala
scala> val status = 500
status: Int = 500

scala> val message = status match {
 | case 200 =>
 | "ok"
 | case 400 => {
 | println("ERROR - we called the service incorrectly")
 | "error"
 | }
 | case 500 => {
 | println("ERROR - the service encountered an error")
 | "error"
 | }
 | }
ERROR - the service encountered an error
message: String = error
```

여러 패턴을 하나로 결합하여 그 패턴 중 하나라도 일치하면 `case` 블록이 실행되는 **패턴 대안이(Pattern Alternative)** 로 만들 수 있습니다.

**Syntax: A Pattern Alternative**

```scala
case <pattern 1> | <pattern 2> .. => <one or more expressions>
```

패턴 대안은 여러 패턴에 대해 동일한 case 블록을 재사용함으로써 코드 중복을 방지합니다.

```scala
scala> val day = "MON"
day: String = MON

scala> val kind = day match {
 | case "MON" | "TUE" | "WED" | "THU" | "FRI" =>
 | "weekday"
 | case "SAT" | "SUN" =>
 | "weekend"
 | }
kind: String = weekday
```

입력 표현식에 일치하는 패턴을 제공하지 못하는 매치 표현식의 예제도 알아보겠습니다.

```scala
scala> "match me" match { case "nope" => "sorry" }
scala.MatchError: match me (of class java.lang.String)
 ... 32 elided
 ```

`match me` 입력 패턴은 유일하게 주어진 패턴인 `nope` 일치하지 않으므로 Scala 컴파일러는 런타임 에러로 처리합니다. 오류 타입인 `scala.MatchError` 는 매치 표현식이 입렵값을 처리하는 데 실패했음을 가리킵니다.

매치 표현식을 방해하는 에러를 예방하려면 **와일드카드 모두-일치(wildcard match-all)** 패턴을 사용하거나, 모든 가능한 입력 패턴을 포괄할 수 있을 만큼 충분한 패턴을 추가해야합니다. 매치표현식에서 와일드카드 패턴은 가능한 모든 입력 패턴을 매치시킴으로써 `scala.MatchError` 가 발생하는 것을 방지합니다.

### Matching with Wildcard Patterns

매치 표현식에서 사용할 수 있는 와일드카드 패턴에는 **값 바인딩(value binding)** 과 와일드카드 연산자가 있습니다.

**값 바인딩(Variable Binding)** 을 이용하면 매치 표현식의 입력 패턴은 로컬 값에 바인딩되어 `case` 블록의 본문에서 사용할 수 있습니다. 이 패턴은 바인딩되어 있는 값의 이름을 포함하고 있기 때문에 매칭할 실제 패턴이 없으며, 값 바인딩은 어떤 입력값에도 일치하므로 와일드카드 패턴이 됩니다.

**Syntax: A Value Binding Pattern**

```scala
case <identifier> => <one or more expressions>
```

특정 리터럴과 매칭하고 그 외의 경우는 값 바인딩을 이용하여 가능한 다른 모든 값이 매치되도록 해보겠습니다.

```scala
scala> val message = "Ok"
message: String = Ok

scala> val status = message match {
 | case "Ok" => 200
 | case other => {
 | println(s"Couldn't parse $other")
 | -1
 | }
 |}
status: Int = 200
```

값 `other` 는 `case` 블록이 유지되는 동안 정의되며, 매치 표현식의 입력값인 `message` 의 값이 할당됩니다.

와일드카드 패턴의 다른 형태로는 와일드카드 연산자가 있습니다. 이 연산자는 밑줄(_) 기호로 표시되며, 실행시간에 표현식의 최종값이 들어갈 자리의 이름을 대신하여 자리표시자 역할을 합니다. 값 바인딩과 마찬가지로, 밑줄 연산자는 매칭할 패턴을 제공하지 않기 때문에 어떤 입력값이라도 매칭되는 와일드카드 패턴이 됩니다.

**Syntax: A Wildcard Operator Pattern**

```scala
case _ => <one or more expressions>
```

값 바인딩과는 다르게, 와일드카드는 화살표 오른쪽에서 접근할 수 없습니다. `case` 블록에서 와일드카드의 값에 접근해야 한다면 값 바인딩을 쓰거나 매치 표현식의 입력값에 접근하는 것을 고려해야합니다.

와일드카드 연산자만으로 작성해보겠습니다.

```scala
scala> val message = "Unauthorized"
message: String = Unauthorized

scala> val status = message match {
 | case "Ok" => 200
 | case _ => {
 | println(s"Couldn't parse $message")
 | -1
 | }
 |}
Couldn't parse Unauthorized
status: Int = -1
```

위 경우 밑줄 연산자는 매치 표현식의 실행시간 입력값을 매칭합니다. 하지만 `case` 블록 내에서는 바인딩된 값처럼 접근할 수 없으므로, `println` 문장을 생성할 때는 매치 표현식의 입력값을 사용합니다.

### Matching with Pattern Guards 

**패턴 가드(Pattern Guard)** 는 값 바인딩 패턴에 `if` 표현식을 추가하여 `match` 표현식에 조건부 로직을 섞어 쓸 수 있게 합니다. 패턴 가드를 사용하면 그 패턴은 `if` 표현식이 `true` 를 반환할 때에만 매칭됩니다.

**Syntax: A Pattern Guard**

```scala
case <pattern> if <Boolean expression> => <one or more expressions>
```

일반적인 `if` 표현식과 달리, 여기에서의 `if` 표현식은 부울식을 둘러싸는 괄호가 필요없습니다. 일반적인 `if` 표현식은 전체 명령문을 파싱하고 조건식의 부울식을 기술하는 작업을 단순화하기 위해 괄호가 필요합니다. 이 경우 화살표(=>)가 이를 대신하고 파싱을 단순화합니다.

응답이 널이 아닌것과 널인 것을 구별하는 패턴 가드를 사용하여 올바른 메세지를 출력해보겠습니다.

```scala
scala> val response: String = null
response: String = null
scala> response match {
 | case s if s != null => println(s"Received '$s'")
 | case s => println("Error! Received a null response")
 | }
Error! Received a null response
```

### Matching Types with Pattern Variables

매치 표현식에서 패턴 매칭을 하는 다른 방법으로는 입력 표현식의 타입을 매칭하는 것입니다. 매칭된다면 **패턴 변수** 는 입력값을 다른 타입의 값으로 전환할 수 있습니다. 새로운 값과 타입은 `case` 블록에서 사용할 수 있습니다.

**Syntax: Specifying a Pattern Variable**

```scala
case <identifier>: <type> => <one or more expressions>
```

이미 살펴보았던 값과 변수의 명명 규칙 외에 패턴 변수를 명명하는 데 있어 유일한 제약사항은 반드시 소문자로 시작해야합니다.

모든 값은 타입이 있고 타입은 전형적으로 상당히 서술적이라는 점을 고려하면, 매치 표현식을 사용하여 값의 타입을 결정하는 방법에 대해 생각해 볼 수 있습니다. Scala 가 **다형적(Polymorphic)** 인 타입을 지원한다는 사실이 매치 표현식 사용법의 단서가 될 수 있습니다.

Int 타입의 값이 Any 타입의 다른 값에 할당되거나, 또는 Java 나 Scala 라이브러리 호출로부터 Any 로 반환될 수 있습니다.

```scala
scala> val x: Int = 12180
x: Int = 12180

scala> val y: Any = x
y: Any = 12180

scala> y match {
 | case x: String => s"'x'"
 | case x: Double => f"$x%.2f"
 | case x: Float => f"$x%.2f"
 | case x: Long => s"${x}l"
 | case x: Int => s"${x}i"
 | }
res9: String = 12180i
```

매치 표현식에 주어진 값이 Any 타입을 가지더라도 그 값이 가지고 있는 데이터가 Int 로 생성되었습니다. 매치 표현식은 그 값에 주어진 타입뿐 아니라 그 값의 실제 타입을 기반으로 매칭할 수 있습니다.

## Loops

**루프(Loop)** 는 하나의 작업을 반복적으로 수행하는 것을 나타내는 용어입니다. 일정 범위의 데이터를 반복하거나 부울식이 `false` 를 반환할 때까지 반복하는 것이 여기에 해당합니다.

Scala 에서 가장 중요한 루프 구조는 for 루프로 **For-Comprehension** 이라고도 합니다. 일정 범위의 데이터를 반복하며, 반복할 때마다 표현식을 실행합니다.

먼저 일련의 숫자를 반복하는 `Range` 라 불리는 데이터 구조를 알아보겠습니다. `Range` 는 시작과 끝을 나타내는 정수와 함께 `to` 또는 `until` 연산자를 이용하여 생성할 수 있는데, `to` 는 끝을 나타내는 정수를 모두 포함하는 리스트를 만드는 반면, `until` 은 끝을 나타내는 정수를 포함하지 않는 리스트를 만듭니다.

**Syntax: Defining a Numeric Range**

```scala
<starting integer> [to|until] <ending integer> [by increment]
```

다음은 for 루프의 기본정의를 나타냅니다.

**Syntax: Iterating with a Basic For-Loop**

```scala
for (<identifier> <- <iterator>) [yield] [<expression>]
```

키워드 `yield` 는 선택사항입니다. 표현식과 함께 `yield` 가 쓰여지면 호출된 모든 표현식의 반환값은 컬렉션으로 반환됩니다. 만약 `yield` 가 없이 표현식이 기술되어 있다면 그 표현식이 호출되기는 하지만, 반환값에는 접근할 수 없습니다.

또한, `for` 루프는 괄호나 중괄호를 사용하여 정의할 수 있습니다.

1 부터 7 까지 요일을 반복하고 각 요일의 헤더를 출력하는 주간계획표를 출력해보겠습니다.

```scala
scala> for (x <- 1 to 7) { println(s"Day $x:") }
Day 1:
Day 2:
Day 3:
Day 4:
Day 5:
Day 6:
Day 7:
```

루프 표현식에 중괄호는 그 안에 단일 명령문만 있으므로 생략해도 무방하지만 C 와 Java 루프와 유사해보이도록 추가했습니다.

하지만, 출력을 "Day X:" 메세지의 컬렉션으로 출력하고 싶으면 어떻게 하면 될까요. 키워드 `yield` 를 사용하여 해결할 수 있습니다.

각 메세지를 반환하는 표현식으로 전환하고 `yield` 키워드를 추가하여 전체 루프를 결과 컬렉션을 반환하는 표현식으로 전환할 수 있습니다.

```scala
scala> for (x <- 1 to 7) yield { s"Day $x:" }
res10: scala.collection.immutable.IndexedSeq[String] = Vector(Day 1:,
Day 2:, Day 3:, Day 4:, Day 5:, Day 6:, Day 7:)
```

현재 반환된 값은 `IndexedSeq[String]` 타입이며, `IndexedSeq` 의 구현 중 하나인 `Vector` 에 할당되었음을 알려줍니다. `Scala` 는 객체지향 다형성을 지원하기 때문에 `IndexedSeq` 의 서브타입은 `Vector` 는 `IndexedSeq` 타입을 가지는 값에 할당할 수 있습니다.

다른 면에서 `for` 루프를 **맵(map)** 으로 생각할 수 있는데 `for` 루프가 요일을 `String` 으로 변환하는 표현식을 취하고, 이 표현식을 입력 범위의 모든 멤버에 적용하기 때문입니다. 앞선 예제에서 숫자 범위를 같은 크기를 가지는 메세지의 컬렉셔넹 매핑하였습니다. 다른 시퀀스와 마찬가지로 이 컬렉션은 이제 다른 `for` 루프에서 반복자로 사용 가능합니다.

각 메세지를 생성하고 출력하는 시퀀스를 반복하는 `for` 루프를 생성해서 테스트해보겠습니다. 이번에는 각 메세지를 별도의 줄로 출력하는 대신 한 줄에 모두 출력하곘습니다.

```scala
scala> for (day <- res0) print(day + ", ")
Day 1:, Day 2:, Day 3:, Day 4:, Day 5:, Day 6:, Day 7:,
```

### Iterator Guards

매치표현식에서 패턴 가드와 마찬가지로 **반복자 가드(Iterator Guard)** 또는 **필터(Filter)** 는 반복자에 `if` 표현식을 추가합니다. 반복자 가드를 사용하면 `if` 표현식이 `true` 를 반환할 때만 반복을 수행합니다.

**Syntax: An Iterator Guard**

```scala
for (<identifier> <- <iterator> if <Boolean expression>) ...
```

3 의 배수로 이루어진 컬렉션을 만드는 예제를 알아보겠습니다.

```scala
scala> val threes = for (i <- 1 to 20 if i % 3 == 0) yield i
threes: scala.collection.immutable.IndexedSeq[Int] = Vector(3, 6, 9, 12, 15, 18)
```

반복자 가드는 반복자와 구분하여 벌도의 줄로 등장할 수 있습니다. 반복자와 반복자 가드를 구분하여 `for` 루프를 사용한 예는 다음과 같습니다.

```scala
scala> val quote = "Faith,Hope,,Charity"
quote: String = Faith,Hope,,Charity
scala> for {
 | t <- quote.split(",")
 | if t != null
 | if t.size > 0
 | }
 | { println(t) }
Faith
Hope
Charity
```

### Nested Iterators 

**중첩된 반복자(Nested Iterator)** 는 `for` 루프에 추가된 부가적인 반복자로, 전체 반복 횟수를 자신의 반복 횟수만큼 반복합니다. 기존의 루프에 부가적인 반복자를 추가하는 것은 별도의 중첩된 루프로 작성한 것과 동일한 결과를 가져오기 때문에 중첩된 반복자라고 부릅니다.

전체 반복 횟수는 모든 반복자 횟수의 곱셈입니다. 중첩된 루프가 반복하지 않으면 전체 방복을 취소합니다.

```scala
scala> for { x <- 1 to 2
 | y <- 1 to 3 }
 | { print(s"($x,$y) ") }
(1,1) (1,2) (1,3) (2,1) (2,2) (2,3)
scala>
```

### Value Binding 

`for` 루프에 일반적인 전략은 현행 반복을 기반으로 하는 표현식 블록 내에 임시 값 또는 변수를 지정하는 것입니다. Scala 에서 이에 대응하는 방법으로는 `for` 루프 정의에서 **값 바인딩(Value Binding)** 을 하는것입니다. 이는 동일한 작업을 하지만, 표현식 블록의 크기와 복잡도를 최소화할 수 있습니다.

**Syntax: Value Binding in For-Loops**

```scala
for (<identifier> <- <iterator>; <identifier> = <expression>) ...
```

다음은 0 부터 8 까지 2 의 거듭제곱 값을 계산하기 위해 Int 에 `<<` 이항 연산자를 사용했습니다. 각 연산의 결과는 현행 반복에서 값 `pow` 에 바인딩되어 있습니다.

```scala
scala> val powersOf2 = for (i <- 0 to 8; pow = 1 << i) yield pow
powersOf2: scala.collection.immutable.IndexedSeq[Int]
        = Vector(1, 2, 4, 8,16, 32, 64, 128, 256)
```

값 `pow` 는 루프에서 반복할 때마다 정의되고 할당됩니다. 그 값은 `for` 루프에 의해 생성되므로 각 반복마다 산출된 `pow` 값의 컬렉션입니다.

`for` 루프 정의에서 값 바인딩은 그 정의 내의 루프 조직의 대부분을 중앙 집중화합니다. 그 결과 더 간결한 `for` 루프를 한층 더 간결한 `yield` 표현식과 함께 제공합니다.

### While and Do/While Loops 

`for` 루프와 함께 `Scala` 는 `while` 과 `do/while` 루프를 지원합니다. `for` 루프 만큼 보편적이지는 않은데 그 이유는 `yield` 를 사용할 수 없기 때문입니다.

**Syntax: A While Loop**

```scala
while (<Boolean expression>) statement
```

하나의 숫자를 그 숫자가 0 보다 크지 않을 때까지 감소시키는 `while` 구문 입니다.

```scala
scala> var x = 10; while (x > 0) x -= 1
x: Int = 0
```

`do/while` 루프는 이와 유사하지만 조건식을 알아보기 전에 문장이 먼저 실행됩니다.

```scala
scala> val x = 0
x: Int = 0

scala> do println(s"Here I am, x = $x") while (x > 0)
Here I am, x = 0
```