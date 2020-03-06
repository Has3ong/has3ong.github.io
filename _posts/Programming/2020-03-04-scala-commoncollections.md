---
title : Scala Common Collections
tags :
- Map
- Set
- List
- Collection
- Scala
---

*이 포스트는 [Learning Scala]() 를 바탕으로 작성하였습니다.*

Scala 는 JVM 언어이므로 Scala 코드에서 Java 컬렉션 라이브러리 전체에 접근하고 사용할 수 있습니다.

또한, Scala 도 Java 와 마찬가지로 *high-performance, object-oriented, type-parameterized* 의 컬렉션 프레임워크를 가지고 있습니다. 하지만 Scala 의 컬렉션은 `map`, `filter`, `reduce` 와 같이 짧고 표현력 있는 표현식으로 데이터를 관리하고 처리하는 고차 연산도 가지고 있습니다. 또한, 가변적 컬렉션 타입 계층구조와 불변의 컬렉션 타입 계층구조를 별개로 가지고 있어서 불변의 데이터와 가변적인 데이터 사이의 전환을 쉽게 만들어줍니다.

## Lists, Sets, and Maps 

불변의 단방향 연결 리스트인 List 를 알아보겟습니다. 리스트는 함수를 호출하여 생성할 수 있습니다. 호출 시 그 리스트에 포함될 내용을 쉼표로 구분된 매개변수 형태로 전달합니다.

```scala
scala> val numbers = List(32, 95, 24, 21, 17)
numbers: List[Int] = List(32, 95, 24, 21, 17)

scala> val colors = List("red", "green", "blue")
colors: List[String] = List(red, green, blue)

scala> println(s"I have ${colors.size} colors: $colors")
I have 3 colors: List(red, green, blue)
```

모든 컬렉션과 String 인스턴스에서 사용할 수 있는, `size` 메소드는 컬렉션에 포함된 항목들의 개수를 반환합니다. 컬렉션 또한 타입 - 매개변수화 되어 초기화할 때 사용했던 타입을 기억하고 고수합니다. REPL 은 타입 - 매개변수화된 컬렉션을 `List[Int]` 와 `List[String]` 으로 표시됩니다.

List 스타일의 `head()` 와 `tail()` 메소드를 사용하여 리스트의 첫 번째 요소와 뒤쪽 요소에 각각 접근해보겟습니다.

```scala
scala> val colors = List("red", "green", "blue")
colors: List[String] = List(red, green, blue)

scala> colors.head
res0: String = red

scala> colors.tail
res1: List[String] = List(green, blue)

scala> colors(1)
res2: String = green

scala> colors(2)
res3: String = blue
```

`for` 루프로 리스트를 반복해서 접근할 수 있습니다.

```scala
scala> val numbers = List(32, 95, 24, 21, 17)
numbers: List[Int] = List(32, 95, 24, 21, 17)

scala> var total = 0; for (i <- numbers) { total += i }
total: Int = 189

scala> val colors = List("red", "green", "blue")
colors: List[String] = List(red, green, blue)

scala> for (c <- colors) { println(c) }
red
green
blue
```

List 와 컬렉션에서 사용할 수 있는 고차 함수인 `foreach(), map(), reduce()` 를 사용해보겠습니다. 이 함수 리터럴에는 괄호로 묶인 입력 매개변수의 함수 반복문이 포함되어있습니다.

```scala
scala> val colors = List("red", "green", "blue")
colors: List[String] = List(red, green, blue)

scala> colors.foreach( (c: String) => println(c) )
red
green
blue

scala> val sizes = colors.map( (c: String) => c.size )
sizes: List[Int] = List(3, 5, 4)

scala> val numbers = List(32, 95, 24, 21, 17)
numbers: List[Int] = List(32, 95, 24, 21, 17)

scala> val total = numbers.reduce( (a: Int, b: Int) => a + b )
total: Int = 189
```

Set 은 유일한 요소들로 이루어진 순서가 없는 불변의 컬렉션이지만, List 와 유사하게 동작합니다. 다음은 중복된 항목들로 Set 을 생성하는 예제입니다. Iterable 의 또 다른 서브타입으로 Set 인스턴스는 List 와 마찬가지로 동일한 연산을 지원합니다.

```scala
scala> val unique = Set(10, 20, 30, 20, 20, 10)
unique: scala.collection.immutable.Set[Int] = Set(10, 20, 30)

scala> val sum = unique.reduce( (a: Int, b: Int) => a + b )
sum: Int = 60
```

Map 은 불변의 Key-Value 의 저장소로, 다른 언어에서는 HaspMap, Dictionary, Associatve Array 로 알려져 있습니다. Map 에 주어진 유일한 키로 저장된 값은 그 키를 이용하여 추출할 수 있습니다. Key 와 Value 는 타입 매개변수화되어 문자열을 정수에 매핑할 수 있습니다.

Map 은 `->` 관계 연산자를 사용하여 기술할 수 있습니다. Map 을 활용한 예제를 보겠습니다.

```scala
scala> val colorMap = Map("red" -> 0xFF0000, "green" -> 0xFF00,
 "blue" -> 0xFF)
colorMap: scala.collection.immutable.Map[String,Int] =
 Map(red -> 16711680, green -> 65280, blue -> 255)

scala> val redRGB = colorMap("red")
redRGB: Int = 16711680

scala> val cyanRGB = colorMap("green") | colorMap("blue")
cyanRGB: Int = 65535

scala> val hasWhite = colorMap.contains("white")
hasWhite: Boolean = false

scala> for (pairs <- colorMap) { println(pairs) }
(red,16711680)
(green,65280)
(blue,255)
```

## What’s in a List? 

List 나 다른 타입의 컬렉셔능ㄹ 생성하는 표준 방식은 그 타입을 원하는 내용과 함께 호출하는것입니다.

```scala
scala> val colors = List("red", "green", "blue")
colors: List[String] = List(red, green, blue)
```

컬렉션에는 지금까지 사용했던 문자열과 숫자 대신 어떤 타입의 값도 저장할 수 있습니다. 예를 들어 컬렉션의 컬렉션을 만들 수 있습니다.

```scala
scala> val oddsAndEvents = List(List(1, 3, 5), List(2, 4, 6))
oddsAndEvents: List[List[Int]] = List(List(1, 3, 5), List(2, 4, 6))
```

또는 2 개의 항목으로 이루어진 튜플의 컬렉션을 가질 수 있어서 Map 과 유사하게 생긴 List 를 생성할 수 있습니다.

```scala
scala> val keyValues = List(('A', 65), ('B',66), ('C',67))
keyValues: List[(Char, Int)] = List((A,65), (B,66), (C,67))
```

Scala 의 단일 구성 요소에는 그 요소를 가리키는 인덱스 번호와 함께 List 를 함수로 호출하여 접근할 수 있습니다.

```scala
scala> val primes = List(2, 3, 5, 7, 11, 13)
primes: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> val first = primes(0)
first: Int = 2

scala> val fourth = primes(3)
fourth: Int = 7
```

List 를 List 의 첫 번째 항목 **헤드(Head)** 와 나머지 항목들인 **테일(Tail)** 로 분해할 수 있습니다.

```scala
scala> val first = primes.head
first: Int = 2

scala> val remaining = primes.tail
remaining: List[Int] = List(3, 5, 7, 11, 13)
```

List 는 불변의 재귀적인 데이터 구조이므로 List 의 각 요소는 자신만의 헤드와 점진적으로 더 짧아지는 테일을 가지고 있습니다. 이를 사용하여 헤드로 시작하여 테일들이 지나가는 길을 만들면서 List Iterator 를 만들 수 있습니다.

반복자를 만들 때 어려운 부분은 List 의 마지막에 언제 도착하는지 알아내는것입니다. List 에는 순회하지 않아도 되는 `isEmpty` 메소드가 있습니다.

`isEmpty` 를 이용한 `while` 루프를 구현해보겠습니다.

```scala
scala> val primes = List(2, 3, 5, 7, 11, 13)
primes: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> var i = primes
i: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> while(! i.isEmpty) { print(i.head + ", "); i = i.tail }
2, 3, 5, 7, 11, 13,
```

또는 다음과 같이 가변적인 변수를 사용하지 않고 재귀적 형태로 List 를 순회하는 함수를 만들 수 있습니다.

```scala
scala> val primes = List(2, 3, 5, 7, 11, 13)
primes: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> def visit(i: List[Int]) { if (i.size > 0) { print(i.head + ", ");
 visit(i.tail) } }
visit: (i: List[Int])Unit

scala> visit(primes)
2, 3, 5, 7, 11, 13,
```

이 재귀적 함수는 List 에 얼마나 많은 메소드들이 구현되어 있는지를 대표적으로 보여줍니다.

List 의 마지막인지를 검사하기위해 `isEmpty` 를 호출하는것도 효율적이지만, 다른 방법도 있습니다. 모든 List 는 종점으로 `Nil` 의 인스턴스로 끝나기 때문에 반복자는 현재의 항목과 `Nil` 을 비교하여 List 의 끝을 확인할 수 있습니다.

```scala
scala> val primes = List(2, 3, 5, 7, 11, 13)
primes: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> var i = primes
i: List[Int] = List(2, 3, 5, 7, 11, 13)

scala> while(i != Nil) { print(i.head + ", "); i = i.tail }
2, 3, 5, 7, 11, 13,
```    

`Nil` 은 근본적으로 `List[Nothing]` 의 싱글턴 인스턴스입니다. 타입 `Nothing` 은 다른 모든 Scala 타입의 서브타입으로 인스턴스화할 수 없습니다. 따라서 `Nothing` 타입의 List 는 모든 타입의 리스트와 호환되어, 종점으로 사용할 수 있습니다.

새로운 빈 List 를 생성하면 실제로는 새로 생긴 인스턴스 대신 `Nil` 을 반환합니다. 단일 항목을 가지는 새로운 리스트를 생성하는 것은 자신의 테일로 `Nil` 을 가리키는 단일 리스트 항목을 생성합니다.

몇 가지 예제를 통해 알아보겠습니다.

```scala
scala> val l: List[Int] = List()
l: List[Int] = List()

scala> l == Nil
res0: Boolean = true

scala> val m: List[String] = List("a")
m: List[String] = List(a)

scala> m.head
res1: String = a

scala> m.tail == Nil
res2: Boolean = true
```

데이터 타입과 상관없이 List 가 언제나 `Nil` 로 끝나는것을 확인할 수 있습니다. 

### The Cons Operator 

List 를 생성하는 다른 방법은 `Nil` 관계를 이용하는것입니다. List 를 인정하는 또 다른 의미로, Scala 는 List 를 만들기 위해 **생성(Cons,Construct)** 연산자 사용을 지원합니다. `Nil` 기반으로 항목들을 결합하기 위해 *오른쪽-결합형(Right-Associative)* 생성 연산자 `::` 를 사용하여 리스트를 만들 수 있습니다.

```scala
scala> val numbers = 1 :: 2 :: 3 :: Nil
numbers: List[Int] = List(1, 2, 3)
```

`::` 는 단순히 List 에서 제공하는 메소드라는 점을 기억하면됩니다. 이 메소드는 새로운 List 의 헤드가 될 단일 값을 취하며, 그 테일은 `::` 가 호출된 List 를 가리킵니다. 생성 연산자에 전형적인 점 표기법도 이용할 수 있습니다.

```scala
scala> val first = Nil.::(1)
first: List[Int] = List(1)

scala> first.tail == Nil
res3: Boolean = true
```

기존 리스트의 앞에 값을 추가하여 새로운 리스트를 만들기 위해 연산자를 사용해보겠습니다.

```scala
scala> val second = 2 :: first
second: List[Int] = List(2, 1)

scala> second.tail == first
res4: Boolean = true
```

`second` List 가 `first` List 를 포함하지만 이 둘 모두 독자적으로 사용할 수 있는 유효한 List 입니다. 하나의 값을 다른 값에 추가하여 하나의 List 를 만드는 이 예제는 Scala 의 불변의 List 가 가지는 재귀적이며 재사용 가능한 특성을 보여줍니다.

## List Arithmetic 

List 의 기본 산술 연산에 초점을 맞춰보겠습니다. 아래 표는 List 에서 사용하는 산술 연산자입니다. 전체 메소드 목록을 보려면 [Scala 공식 문서](https://www.scala-lang.org/api/current/scala/collection/immutable/List.html) 를 참조하시면 됩니다.

|Name|Example|Description|
|:--|:--|:--|
|`::`|`1 :: 2 :: Nil`|List 에 개별 요소를 덧붙임, 오른쪽-결합형 연산자|
|`:::`|`List(1, 2) ||| List(2, 3)`|이 List 앞에 다른 리스트를 추가함, 오른쪽 - 결합형 연산자|
|`++`|`List(1, 2) ++ Set(3, 4, 3)`|이 List 에 다른 컬렉션을 덧붙임|
|`==`|`List(1, 2) == List(1, 2)`|두 컬렉션의 타입과 내용을 비교|
|`distinct`|`List(3, 5, 4, 3, 4).distinct`|중복 요소가 없는 List 버전을 반환함|
|`drop`|`List(1, 2, 3, 4) drop 2`|List 의 첫 번째 n 개 요소를 뺌|
|`filter`|`List(23, 8, 14, 21) filter ( _ > 18)`|참 / 거짓 함수를 통과한 List 의 요소를 반환|
|`flatten`|`List(List(1, 2), List(3, 4)).flatten`|List 의 List 구조를 그 요소들을 모두 포함하는 단일 리스트로 전환함|
|`partition`|`List(1, 2, 3, 4, 5) partition (_ < 3)`|List 의 요스들을 참 / 거짓 함수의 결과에 따라 분류하여 2 개의 List 를 포함하는 Tuple 로 만듬|
|`reverse`|`List(1, 2, 3).reverse`|List 요소들의 순서를 거꾸로 함|
|`slice`|`List(2, 3, 5, 7) slice (1, 3)`|첫 번째 인덱스부터 두 번재 인덱스 -1 까지 해당하는 부분을 반환|
|`sortBy`|`List("apple", "to") sortBy (_.size)`|주어진 함수로부터 반환된 값으로 List 순서를 정렬|
|`sorted`|`List("apple", "to").sorted`|핵심 Scala 타입의 List 를 자연값 기준으로 정렬|
|`splitAt`|`List(2, 3, 5, 7) splitAt 2`|List 요소들을 주어진 인덱스의 앞에 위치하는지 뒤에 위치하는지에 따라 두 List 의 Tuple 로 반환|
|`take`|`List(2, 3, 5, 7, 11, 13) take 3`|List 첫 번째 n 개의 요소들을 추출|
|`zip`|`List(1, 2) zip List("a", "b")|두 List 를 각 인덱스에 해당하는 요소들기리 구성된 Tuple 의 List 로 결합|

위에서 알아본 함수 중 고차 연산 3 가지 예제를 살펴보겠습니다.

```scala
scala> val f = List(23, 8, 14, 21) filter (_ > 18)
f: List[Int] = List(23, 21)

scala> val p = List(1, 2, 3, 4, 5) partition (_ < 3)
p: (List[Int], List[Int]) = (List(1, 2),List(3, 4, 5))

scala> val s = List("apple", "to") sortBy (_.size)
s: List[String] = List(to, apple)
```

## Mapping Lists

Map 메소드는 함수를 취하여 각 함수를 리스트의 모든 요소들에 적용하고, 그 결과를 새로운 리스트에 수집합니다. 한 리스트의 각 항목을 다른 List 에 매핑하며, 다른 List 는 첫 번째 List 와 같은 크기에 다른 데이터 또는 요소 타입을 가집니다. 아래 표는 Scala Lis 에서 사용할 수 있는 map 메소드 중 일부입니다.

|Name|Example|Description|
|:--|:--|:--|
|`collect`|`List(0, 1, 0) collect {case 1 => "ok"}`|각 요소를 부분 함수를 사용하여 변환하고, 해당 함수를 적용할 수 있는 요소를 유지함|
|`flatMap`|`List("milk, tea") flatMap (_.splut(','))`|주어진 함수를 이용하여 각 요소를 변환하고, 그 결과 List 를 이 List 에 평면화한다.|
|`map`|`List("milk", "tea") map (_.toUpperCase)`|주어진 함수를 이용하여 각 요소를 변환함|

List-Mapping 연산자가 REPL 에서 어떻게 작동하는지 알아보겠습니다.

```scala
scala> List(0, 1, 0) collect {case 1 => "ok"}
res0: List[String] = List(ok)

scala> List("milk,tea") flatMap (_.split(','))
res1: List[String] = List(milk, tea)

scala> List("milk","tea") map (_.toUpperCase)
res2: List[String] = List(MILK, TEA)
```

## Reducing Lists 

List **축소(Reducing)** 는 컬렉션으로 작업하는 데 있어 보편적인 연산입니다. 등급 List 를 합산하거나 단일 값으로 축소를 합니다.

내장된 수학적 축소 연산을 살펴보겠습니다.

|Name|Example|Description|
|:--|:--|:--|
|`max`|`List(41, 59, 26).max`|List 의 최댓값 구하기|
|`min`|`List(10.9, 32.5, 4.23, 5.67).min`|List 의 최솟값 구하기|
|`product`|`List(5, 6, 7).product`|List 의 숫자들을 곱하기|
|`sum`|`List(11.3, 23.5, 7.2).sum`|List 의 숫자들을 합산하기|

다음은 단일 부울값으로 축소하는 연산을 보겠습니다.

|Name|Example|Description|
|:--|:--|:--|
|`contains`|`List(34, 29, 18) contains 29`|List 가 이 요소를 포함하고 있는지를 검사|
|`endsWith`|`List(0, 4, 3) endsWith List(4, 3)`|List 가 주어진 List 로 끝나는지 검사|
|`exists`|`List(24, 17, 32) exists (_ < 18)`|List 에서 최소 하나의 요소에 대해 조건자가 성립하는지 검사|
|`forall`|`List(24, 17, 32) forall (_ < 18)`|List 의 모든 요소에 대해 조건자가 성립하는지 검사|
|`startsWith`|`List(0, 4, 3) startsWith List(0)`|List 가 주어진 List 로 시작하는지를 테스트|


부울 축소 연산에 대한 예제를 살펴보겠습니다.

```scala
scala> val validations = List(true, true, false, true, true, true)
validations: List[Boolean] = List(true, true, false, true, true, true)

scala> val valid1 = !(validations contains false)
valid1: Boolean = false

scala> val valid2 = validations forall (_ == true)
valid2: Boolean = false

scala> val valid3 = validations.exists(_ == false) == false
valid3: Boolean = false
```

이 축소 연산들이 어떻게 구현되는지 보기위해 직접 축소 연산을 만들어 보겠습니다. 먼저 누곗값을 가지는 **누산기(Accumulator)** 변수와 현재 요소를 기반으로 누산기를 업데이트하는 로직을 가지고 컬렉션을 반복해야합니다.

```scala
scala> def contains(x: Int, l: List[Int]): Boolean = {
 | var a: Boolean = false
 | for (i <- l) { if (!a) a = (i == x) }
 | a
 | }
contains: (x: Int, l: List[Int])Boolean

scala> val included = contains(19, List(46, 19, 92))
included: Boolean = true
```

정확히 작동하지만 `contains` 로직을 함수 매개변수로 옮겨서 `boolReduce` 라는 함수를 구현했습니다.

```scala
scala> def boolReduce(l: List[Int], start: Boolean)(f: (Boolean, Int) =>
 | Boolean): Boolean = {
 |
 | var a = start
 | for (i <- l) a = f(a, i)
 | a
 | }
boolReduce: (l: List[Int], start: Boolean)(f: (Boolean, Int) => Boolean)Boolean

scala> val included = boolReduce(List(46, 19, 92), false) { (a, i) =>
 | if (a) a else (i == 19)
 | }
included: Boolean = true
```

다음은 `reduceOp` 로 `boolReduce` 연산을 다시 작성한것입니다. 이 연산은 Int 와 Boolean 타입을 각각 타입 매개변수 A 와 B 로 치환했습니다. 아래는 `sum` 예제를 추가한것입니다.

```scala
scala> def reduceOp[A,B](l: List[A], start: B)(f: (B, A) => B): B = {
 | var a = start
 | for (i <- l) a = f(a, i)
 | a
 | }
reduceOp: [A, B](l: List[A], start: B)(f: (B, A) => B)B

scala> val included = reduceOp(List(46, 19, 92), false) { (a, i) =>
 | if (a) a else (i == 19)
 | }
included: Boolean = true

scala> val answer = reduceOp(List(11.3, 23.5, 7.2), 0.0)(_ + _)
answer: Double = 42.0
```

Scala 컬렉션에서는 `reduceOp` 와 유사한 내장 연산을 제공합니다. 이 내장 연산은 왼쪽-오른쪽, 오른쪽-왼쪽 방향 그리고 순서와 무관한 버전을 모두 제공하며, 누산기와 누곗값으로 작업하는 다른 방법들을 제공하기도 합니다.

이렇게 List 를 입력 함수 기반으로 축소하는 고차 함수를 속칭 **리스트-접기(List-Folding)** 연산이라 하는데, List 를 축소하는 함수는 **접기(Fold)** 로 더 잘 알려져 있기 때문입니다.

아래는 Scala 컬렉션에서 List-Fold 함수 중 일부입니다.

|Name|Example|Description|
|:--|:--|:--|
|`fold`|`List(4, 5, 6).fold(0)(_ + _)`|주어진 시작값과 축소 함수로 List 를 축소|
|`foldLeft`|`List(4, 5, 6).foldLeft(0)(_ + _)`|주어진 시작값과 축소 함수로 List 를 왼쪽에서 오른쪽으로 축소함|
|`foldRight`|`Left(4, 5, 6).foldRight(0)(_ + _)|주어진 시작값과 축소 함수로 List 를 오른쪽에서 왼쪽으로 축소함|
|`reduce`|`List(4, 5, 6).reduce(_ + _)`|List 의 첫 번째 요소를 시작으로, 주어진 축소 함수로 List 를 축소함|
|`reduceLeft`|`List(4, 5, 6).reduceLeft(_ + _)`|List 의 첫 번째 요소를 시작으로, 주어진 축소 함수로 List 를 왼쪽부터 오른쪽으로 축소함|
|`reduceRight`|`List(4, 5, 6).reduceRight(_ + _)`|List 의 마지막 시작으로, 주어진 축소 함수로 List 를 오른쪽부터 왼쪽으로 축소함|
|`scan`|`List(4, 5, 6).scan(0)(_ + _)`|시작값과 축소 함수를 취하여 각각의 누곗값의 List 를 반환함|
|`scanLeft`|`List(4, 5, 6).scanLeft(0)(_ + _)`|시작값과 축소 함수를 취하고, 왼쪽부터 오른쪽으로 각각의 누곗값의 List 를 반환함|
|`scanRight`|`List(4, 5, 6).scanRight(0)(_ + _)`|시작값과 축소 함수를 취하고 오른쪽부터 왼쪽으로 각각의 누곗값의 List 를 반환|

## Converting Collections

아래 표에는 컬렉션 전환 메소드들을 정리하였습니다.

|Name|Example|Description|
|:--|:--|:--|
|`mkString`|`List(24, 99, 104).mkString(", ")`|주어진 구분자를 사용하여 컬렉션을 String 으로 만듬|
|`toBuffer`|`List('f', 't').toBuffer`|불변의 컬렉션을 가변적인 컬렉션으로 전환|
|`toList`|`Map("a" -> 1, "b" -> 2).toList`|컬렉션을 List 로 전환|
|`toMap`|`Set(1 -> true, 3 -> true).tmMap`|두 요소로 구성된 튜플의 컬렉션을 Map 으로 전환|
|`toSet`|`List(2, 5, 5, 3, 2).toSet`|컬렉션을 Set 으로 전환|
|`toString`|`List(2, 5, 5, 3, 2).toString`|컬렉션을 String 으로 컬렉션의 타입을 포함하여 만듬|

### Java and Scala Collection Compatibility

컬렉션 전환하는 것과관련하여 하나 더 알아두어야 할 중요한 관점이 있습니다. Scala 는 JVM 으로 컴파일하고 그 위에서 동작하므로 JDK 와 상호작용뿐 아니라 어떤 Java 라이브러리도 추가할 수 있어야 하는것이 요구사항입니다.

Java 와 Scala 상호작용의 일부는 Java 컬렉션과 Scala 컬렉션간 전환하는 것인데 이 두 컬렉션 타입은 기본적으로 호환되지 않습니다.

Java 와 Scala 컬렉션 사이를 직접 전환할 수 있도록 다음 명령어를 추가할 수 있습니다.

```scala
scala> import collection.JavaConverters._
import collection.JavaConverters._
```

이 `import` 명령어는 `JavaConverters` 와 그 메소드를 현재의 네임스페이스에 추가합니다. 현재의 네임스페이스가 REPL 에서는 현재 세션을 의미하지만, 소스 파일에서는 `import` 명령어가 추가된 파일 도는 로컬 범위의 나머지를 의미합니다.

아래 표는 `JavaConverters` 가 임포트되면 Java 와 Scala 컬렉션에 추가되는 연산입니다.

|Name|Example|Description|
|:--|:--|:--|
|`asJava`|`List(12, 29).asJava`|Scala 컬렉션을 그에 대응하는 Java 컬렉션으로 전환|
|`asScala`|`new java.util.ArrayList(5).asScala`|이 Java 컬렉션을 그에 대응하는 Scala 컬렉션으로 전환|

## Pattern Matching with Collections 

아래는 컬렉션을 이용한 매치표현식 사용입니다.

```scala
scala> val statuses = List(500, 404)
statuses: List[Int] = List(500, 404)

scala> val msg = statuses.head match {
 | case x if x < 500 => "okay"
 | case _ => "whoah, an error"
 | }
msg: String = whoah, an error
```

컬렉션은 등호 연산자를 지원하므로 컬렉션이 패턴 매칭을 지원합니다. 전체 컬렉션을 매칭하기 위해 패턴으로 새로운 컬렉션을 사용

```scala
scala> val msg = statuses match {
 | case x if x contains(500) => "has error"
 | case _ => "okay"
 | }
msg: String = has error
```

값 바인딩으로 모든 요소에 값을 바인딩 할 수 있습니다.

```scala
scala> val msg = statuses match {
 | case List(500, x) => s"Error followed by $x"
 | case List(e, x) => s"$e was followed by $x"
 | }
msg: String = Error followed by 404
```

List 는 헤드 요소와 테일로 분해할 수 있습니다. 패턴으로서 List 헤드와 테일요소에 매칭될 수 있습니다.

```scala
scala> val head = List('r','g','b') match {
 | case x :: xs => x
 | case Nil => ' '
 | }
head: Char = r
```

공식적으로 컬렉션은 아니지만 튜플도 패턴 매칭과 값 바인딩을 지원합니다. 단일 튜플은 다른 타입의 값을 지원하기 때문에 튜플의 패턴 매칭이 때로는 컬렉션의 패턴 매칭보다 더 유용합니다.

```scala
scala> val code = ('h', 204, true) match {
 | case (_, _, false) => 501
 | case ('c', _, true) => 302
 | case ('h', x, true) => x
 | case (c, x, true) => {
 | println(s"Did not expect code $c")
 | x
 | }
 | }
code: Int = 204
```


