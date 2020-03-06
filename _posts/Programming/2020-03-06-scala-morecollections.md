---
title : Scala More Collections
tags :
- Future
- Try
- Option
- String
- Stream
- Buffer
- Collection
- Scala
---

*이 포스트는 [Learning Scala]() 를 바탕으로 작성하였습니다.*

### Mutable Collections

List, Set, Map 은 생성된 후 변경할 수 없습니다. 하지만 새로운 컬렉션으로 변형될 수 있습니다. 예를 들어 불변의 맵을 생성하고 난 뒤 이 중 하나의 매핑을 제거하고 다른 매핑을 추가하여 변형할 수 있습니다.

```scala
scala> val m = Map("AAPL" -> 597, "MSFT" -> 40)
m: scala.collection.immutable.Map[String,Int] =
 Map(AAPL -> 597, MSFT -> 40)

scala> val n = m - "AAPL" + ("GOOG" -> 521)
n: scala.collection.immutable.Map[String,Int] =
 Map(MSFT -> 40, GOOG -> 521)

scala> println(m)
Map(AAPL -> 597, MSFT -> 40)
```

### Creating New Mutable Collections

가장 간단하게 컬렉션을 변경하는 방법은 가변의 컬렉션 타입을 이용하는것입니다. 아래 표에는 표준 불변 타입인 List, Map, Set 에 대응하는 가변 데이터 타입을 보여줍니다.

|Immutable type|Mutable counterpart|
|:--|:--|
|`collection.immutable.List`|`collection.mutable.Buffer`|
|`collection.immutable.Set`|`collection.mutable.Set`|
|`collection.immutable.Map`|`collection.mutable.Map`|

`collection.immutable` 패키지는 Scala 에서 현재 네임스페이스에 자동으로 추가되는 반면, `collection.mutable` 패키지는 아닙니다. 가변의 컬렉션을 생성할 때 그 타입의 전체 패키지 이름을 포함하였는지 반드시 확인해야 합니다.

`collection.mutable.Buffer` 타입은 범용적인 가변의 시퀀스이며, 그 시작과 중간, 끝에 요소들을 추가할 수 있습니다.

다음은 이 타입을 이용하여 하나의 요소로 시작해서 정수 리스트를 만드는 것을 보여줍니다.

```scala
scala> val nums = collection.mutable.Buffer(1)
nums: scala.collection.mutable.Buffer[Int] = ArrayBuffer(1)

scala> for (i <- 2 to 10) nums += i

scala> println(nums)
Buffer(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

맵과 집합도 유사한 과정으로 만들 수 있습니다. 새로운 집합의 타입 매개변수나 새로운 맵의 키와 값의 타입 매개변수를 지정하는 것은 빈 컬렉션을 생성할 때에만 필요합니다.

가변적인 버퍼는 `toList` 메소드를 이용하여 어느 때라도 다시 불변의 List 로 전환할 수 있습니다.

```scala
scala> println(nums)
Buffer(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

scala> val l = nums.toList
l: List[Int] = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

### Creating Mutable Collections from Immutable Ones

가변적인 컬렉션을 직접 생성하는 다른 방법으로는 불변의 컬렉션으로부터 전환하는 것입니다. 이 방법은 이미 시작한 불변의 컬렉션이 있어 이를 변경하여 사용하고 싶거나 `collection.mutable.Buffer()` 대신 `List()` 를 타이핑하고 싶을 때 유용합니다.

불변의 컬렉션인 List, Map, Set 모두 `toBuffer` 메소드를 이용하여 가변적인 타입 `collection.mutable.Buffer()` 으로 전환할 수 있습니다.

List 에서는 이 방법이 간단한데, 버퍼와 List 타입 모드 시퀀스이기 때문입니다. `Iterable` 의 서브타입인 맵 또한 시퀀스로 간주될 수 있으며, Key-Value 튜플의 시퀀스로서 버퍼로 전환됩니다.

다음은 불변하는 맵을 가변적인 버퍼로 전환한 다음, 다시 불변의 맵으로 전환하는 예제입니다.

```scala
scala> val m = Map("AAPL" -> 597, "MSFT" -> 40)
m: scala.collection.immutable.Map[String,Int] =
 Map(AAPL -> 597, MSFT -> 40)

scala> val b = m.toBuffer
b: scala.collection.mutable.Buffer[(String, Int)] =
 ArrayBuffer((AAPL,597), (MSFT,40))

scala> b trimStart 1

scala> b += ("GOOG" -> 521)
res1: b.type = ArrayBuffer((MSFT,40), (GOOG,521))

scala> val n = b.toMap
n: scala.collection.immutable.Map[String,Int] =
 Map(MSFT -> 40, GOOG -> 521)
```

버퍼를 불변의 컬렉션으로 전환할 때 `toMap` 과 함께 버퍼 메소드 `toList`, `toSet` 을 사용할 수 있습니다.

Set 의 모든 항목은 유일해야 한다는 제약 조건을 검증하기 위해, 우선 이 버퍼에 중복 요소를 추가해보겠습니다.

```scala
scala> b += ("GOOG" -> 521)
res2: b.type = ArrayBuffer((MSFT,40), (GOOG,521), (GOOG,521))

scala> val l = b.toList
l: List[(String, Int)] = List((MSFT,40), (GOOG,521), (GOOG,521))

scala> val s = b.toSet
s: scala.collection.immutable.Set[(String, Int)] = Set((MSFT,40), (GOOG,521))
```

List 는 중복된 항목을 포함하지만 Set 은 유일한 항목만 포함되는것을 확인할 수 있습니다.

Buffer 타입은 범용적으로 사용되는 좋은 가변적인 컬렉션으로 List 와 유사하지만, 그 내용을 추가, 삭제, 교체가 가능합니다. `Buffer` 타입이 지원하는 전환 메소드는 자신에 대응하는 불변의 타입에 적용하는 `toBuffer` 메소드와 함께 가변적인 데이터로 작업하기에 유용한 메커니즘을 만듭니다.

Buffer 의 유일한 단점은 너무 광범위하게 적용될 수 있다는 것입니다. 예를 들어 루프 내에서 컬렉션을 반복적으로 추가하는 작업이라면 Buffer 대신 빌더(Builder) 를 사용하는 것이 더 나을것입니다.

### Using Collection Builders

Builder 는 Buffer 를 단순화한 형태로 할당된 컬렉션 타입을 생성하고, 추가 연산만을 지원하도록 제한되어있습니다.

특정 컬렉션 타입의 빌더를 생성하려면 해당 타입의 `newBuilder` 메소드를 호출하고, 해당 타입의 컬렉션 구성 요소를 포함하면 됩니다. 빌더의 `result` 메소드를 호출하면 이를 최종적으로 Set 로 전환해줍니다.

```scala
scala> val b = Set.newBuilder[Char]
b: scala.collection.mutable.Builder[Char,scala.collection.immutable.
 Set[Char]] = scala.collection.mutable.SetBuilder@726dcf2c

scala> b += 'h'
res3: b.type = scala.collection.mutable.SetBuilder@d13d812

scala> b ++= List('e', 'l', 'l', 'o')
res4: b.type = scala.collection.mutable.SetBuilder@d13d812

scala> val helloSet = b.result
helloSet: scala.collection.immutable.Set[Char] = Set(h, e, l, o)
```

## Arrays

Array 는 고정된 크기를 가지며, 내용을 변경할 수 있으며, 인덱스를 가지고 있는 컬렉션 입니다. 이것은 `scala.collections` 패키지에 있지 않고 루트 Iterable 타입으로부터 확장된 타입이 아니므로 공식적으로 컬렉션은 아닙니다.

Array 타입은 실제로 Java 의 배열 타입을 **묵시적 클래스(Implicit class)** 라 부르는 고급 특징으로 감싼 wrapper 입니다.

묵시적 클래스는 배열을 시퀀스로 사용할 수 있도록 해줍니다. Scala 는 JVM 라이브러리 및 Java 코드와의 호환성을 위해 Array 타입을 제공합니다.

다음은 배열로 작업하는 예시입니다.

```scala
scala> val colors = Array("red", "green", "blue")
colors: Array[String] = Array(red, green, blue)

scala> colors(0) = "purple"

scala> colors
res0: Array[String] = Array(purple, green, blue)

scala> println("very purple: " + colors)
very purple: [Ljava.lang.String;@70cf32e3

scala> val files = new java.io.File(".").listFiles
files: Array[java.io.File] = Array(./Build.scala, ./Dependencies.scala,
 ./build.properties, ./JunitXmlSupport.scala, ./Repositories.scala,
 ./plugins.sbt, ./project, ./SBTInitialization.scala, ./target)

scala> val scala = files map (_.getName) filter(_ endsWith "scala")
scala: Array[String] = Array(Build.scala, Dependencies.scala,
 JunitXmlSupport.scala, Repositories.scala, SBTInitialization.scala)
```

Java 배열은 모든 Java 와 Scala 객체가 상속하는 `toString()` 메소드를 재정의하지 않기 때문에 타입 매개변수와 참조를 출력하는 기본 구현을 사용합니다.

따라서 Array 에서 `toString()` 을 호출하면 마지막 예제처럼 읽을 수 없는 결과를 보여줍니다. 하지만 Scala 컬렉션은 그렇지 않은데 Scala 컬렉션은 `toString()` 을 재정의해서 사용가능합니다.

## Seq and Sequences

`Seq` 는 모든 시퀀스의 루트 타입으로, List 와 같은 연결 리스트와 Vector 같은 색인 List 를 포함합니다. 루트 타입으로서 `Seq` 는 인스턴스화될 수 없지만, List 를 생성하는 빠른 방법으로 `Seq` 를 호출할 수 있습니다.

```scala
scala> val inks = Seq('C','M','Y','K')
inks: Seq[Char] = List(C, M, Y, K)
```

> Example 1 - The sequence collections hierarchy

![image](https://user-images.githubusercontent.com/44635266/76055116-0d4c1d00-5fb6-11ea-8bc3-1eff0dd99916.png)

아래 표는 각 타입에 대한 설명입니다.

|Name|Description|
|:--|:--|
|Seq|모든 시퀀스의 루트, `List()` 의 간단한 방법|
|IndexedSeq|색인 시퀀스의 루트, `Vector()` 의 가장 손쉬운 방법|
|Range|정수의 범위, 데이터를 즉시 생성함|
|LinearSeq|선형 시퀀스의 루트|
|List|구성 요소들의 단방향 연결 리스트|
|Queue|FIFO 리스트|
|Stack|LIFO 리스트|
|Stream|지연 리스트, 항목들은 그 항목에 접근할 때 추가됨|
|String|문자의 컬렉션|

Vector 타입은 저장을 위해 Array 로 구현됩니다. 색인 시퀀스로 Vector 에 인덱스로 항목에 접근할 수 있습니다. 반면에, List 의 n 번째 항목에 접근하려면 리스트의 헤드로부터 n-1 단계가 필요합니다.

시퀀스에 String 타입도 포함이 됩니다. Scala 에서는 다른 타입들과 마찬가지로 유효한 컬렉션입니다. String 도 문자들의 연속이므로 Char 구성요소를 가지는 시퀀스가 됩니다. String 타입은 불변하는 컬렉션이며, Iterable 에서 확장된 타입으로 Iterable 연산뿐 아니라 `split`, `trim` 같은 `java.lang.String` 연산도 지원합니다.

```scala
scala> val hi = "Hello, " ++ "worldly" take 12 replaceAll ("w","W")
hi: String = Hello, World
```

## Streams

Stream 타입은 하나 또는 그 이상의 시작 요소들과 재귀 함수로 생성되는 **지연(lazy)** 컬렉션입니다. 다른 불변의 컬렉션들은 그 내용의 100 % 를 초기화 시점에 받지만, Stream 의 구성 요소들은 최초로 접근될 때 컬렉션에 추가됩니다.

Stream 이 생성한 구성 요소들은 캐시에 저장되어 각 요소가 한 번만 생성되는것을 보장합니다. Stream 은 무한히 커질 수 있으며, 이론적으로 구성 요소들이 접근 시에만 현실화되는 무한 컬렉션입니다. Stream 은 `List.Nil` 에 대응하는 항목인 `Stream.Empty` 로 종료될 수 있습니다.

Stream 은 List 와 마찬가지로 Head 와 Tail 로 구성된 재귀적 데이터 구조입니다. 다음은 새로운 Stream 을 구성하고 재귀적으로 생성하는 함수입니다.

```scala
scala> def inc(i: Int): Stream[Int] = Stream.cons(i, inc(i+1))
inc: (i: Int)Stream[Int]

scala> val s = inc(1)
s: Stream[Int] = Stream(1, ?)
```

Stream 은 시작값과 다음 데이터에 약속값(?) 만 포함하고 있스빈다. 이들을 가져와서 내용을 List 에 검색하여 시작값 다음으로 4 개의 값을 추가해보겠습니다.

```scala
scala> val l = s.take(5).toList
l: List[Int] = List(1, 2, 3, 4, 5)

scala> s
res1: Stream[Int] = Stream(1, 2, 3, 4, 5, ?)
```

Stream 은 재귀 함수 호출을 포함하고 있어서 이를 이용하여 끝없이 새로운 요소들을 생성할 수 있습니다.

`Streams.cons` 연산자 대신 `#::` 연산자가 있는데 간단히 Stream 을 위한 생성 연산자라고 합니다. 이 연산자는 `Streams.cons` 와 동일한 기능을 수행하지만 오른쪽-결합형 표기법이라는 점에서 다르며 List 의 생성 연산자 `::` 를 보완합니다.

```scala
scala> def inc(head: Int): Stream[Int] = head #:: inc(head+1)
inc: (head: Int)Stream[Int]

scala> inc(10).take(10).toList
res0: List[Int] = List(10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
```

**한정된 스트림(Bounded Stream)** 을 만들어보겠습니다. 재귀 함수는 두 인수를 받는데, 하나는 새로운 헤드요소이며, 다른 하나는 추가될 마지막 요소입니다.

```scala
scala> def to(head: Char, end: Char): Stream[Char] = (head > end) match {
 | case true => Stream.empty
 | case false => head #:: to((head+1).toChar, end)
 | }
to: (head: Char, end: Char)Stream[Char]

scala> val hexChars = to('A', 'F').take(20).toList
hexChars: List[Char] = List(A, B, C, D, E, F)
```

위와 같이 새로운 함수 `to` 를 이용하여 16 진수를 쓸 때 사용되는, 문자로 구성된 한정된 Stream 을 생성할 수 있습니다.

재귀 함수는 새로운 Stream 을 생성하고 매번 새로운 헤드 요소를 유도하는 데 사용합니다.

## Monadic Collections

**모나딕 컬렉션(Monadic Collection)** 은 Iterable 연산 같은 변형 연산을 지원하지만, 하나 이상의 요소는 포함할 수 없습니다.

### Option Collections

크기가 1 이 넘지 않는 컬렉션으로 Option 타입은 단일 값의 존재 또는 부재를 나타냅니다.

Option 을 Null 의 안전한 대체재로 보는데, 사용자에게 값이 누락될 수 있음을 알리고 `NullPointerException` 을 일으킬 가능성을 줄여주기 때문입니다.

Option 타입은 하나의 요소로 구성된 타입-매개변수화된 컬렉션인 Some 과 빈 컬렉션인 None, 이 두 서브타입에 기반하여 구현할 수 있습니다. None 타입은 타입 매개변수가 없는데 그 안에 어떤 것도 포함되어 있지 않기 때문입니다.

이 두 타입을 직접 사용하거나 `Option()` 을 호출하여 Null 값을 감지하고 적절한 서브타입을 선택할 수 있습니다.

Option 을 생성해보겠습니다.

```scala
scala> var x: String = "Indeed"
x: String = Indeed

scala> var a = Option(x)
a: Option[String] = Some(Indeed)

scala> x = null
x: String = null

scala> var b = Option(x)
b: Option[String] = None
```

`isDefined` 와 `isEmpty` 를 사용하여 주어진 `Option` 이 각각 `Some` 인지 `None` 인지 확인할 수 있습니다.

```scala
scala> println(s"a is defined? ${a.isDefined}")
a is defined? true

scala> println(s"b is not defined? ${b.isEmpty}")
b is not defined? true
```

`Option` 값을 반환하는 함수를 정의해보겠습니다. 

```scala
scala> def divide(amt: Double, divisor: Double): Option[Double] = {
 | if (divisor == 0) None
 | else Option(amt / divisor)
 | }
divide: (amt: Double, divisor: Double)Option[Double]

scala> val legit = divide(5, 2)
legit: Option[Double] = Some(2.5)

scala> val illegit = divide(3, 0)
illegit: Option[Double] = None
```

값을 Option 컬렉션에 감싸서 반환하는 함수는 그 함수가 입력값에 적용되지 않을수도 있으며, 그에 따라 유효한 결과를 반환하지 못할 수도 있음을 의미합니다. 이는 호출자에게 그 함숫값이 단지 가능성일 뿐이라는 것을 명확하게 알려주고 그 결과는 신중하게 처리되어야 함을 확인시켜줍니다. 이렇게 하여 Option 은 함수 결과를 처리하는 타입에 안전한 방식을 제공하며 누락된 값을 의미하는 Null 값을 반환하는 Java 보다 더 안전합니다.

Scala 컬렉션은 Option 타입을 사용하여 빈 컬렉션이 발생하는 상황을 처리하는 안전한 연산을 제공합니다. Head 연산이 비어 있지 않은 List 에 동작하지만 빈 List 에 대해서는 에러를 발생시킵니다. 빈 List 에도 동작할 수 있도록 Option 에 헤드 옵션을 깜사서 반환하는 `headOption` 을 사용합니다.

빈 컬렉션을 안전하게 처리하는 `headOption` 호출을 보겠습니다.

```scala
scala> val odds = List(1, 3, 5)
odds: List[Int] = List(1, 3, 5)

scala> val firstOdd = odds.headOption
firstOdd: Option[Int] = Some(1)

scala> val evens = odds filter (_ % 2 == 0)
evens: List[Int] = List()

scala> val firstEven = evens.headOption
firstEven: Option[Int] = None
```

컬렉션 옵션의 다른 용도는 `find` 연산으로, 조건자 함수에 맞는 첫 번째 요소를 반환하는 `filter` 와 `headOption` 의 조합입니다. 다음은 `find` 를 이용한 검색 예제를 보겠습니다.

```scala
scala> val words = List("risible", "scavenger", "gist")
words: List[String] = List(risible, scavenger, gist)

scala> val uppercase = words find (w => w == w.toUpperCase)
uppercase: Option[String] = None

scala> val lowercase = words find (w => w == w.toLowerCase)
lowercase: Option[String] = Some(risible)
```

List 축소 연산을 사용하여 컬렉션을 단일 Option 으로 축소하였습니다. 하지만, Option 자체가 컬렉션이기 때문에 계속해서 이를 변환할 수 있습니다.

`fliter` 와 `map` 을 사용하여 값을 유지하는 방식으로 값을 잃어버리는 방식으로도 변환할 수 있습니다. 각 연산은 타입에 안전하며 `NullPointerException` 에러를 일으키지 않습니다.

```scala
scala> val filtered = lowercase filter (_ endsWith "ible") map (_.toUpperCase)
filtered: Option[String] = Some(RISIBLE)

scala> val exactSize = filtered filter (_.size > 15) map (_.size)
exactSize: Option[Int] = None
```

`filter` 는 `RISIBLE` 에 적용될 수 없으므로 `None` 을 반환합니다. `None` 에 뒤따라 나오는 `map` 연산은 어떤 영향도 줄 수 없으며 다시 `None` 을 반환합니다.

이는 모나딕 컬렉션으로서 Option 의 훌룡한 예제입니다. 연산에서 안전하게 실행될 수 있는 하나의 단위를 제공합니다.

연산은 현재 값(Some) 에 적용되고 누락 된 값(None) 에는 적용 되지 않지만, 결과 타입은 마지막 연산의 타입과 일치하게됩니다.

**Extracting values from Options**

추출 연산 중 `get()` 연산은 안전하지 않습니다. Some 인스턴스에는 값을 성공적으로 받지만, None 인스턴스에 `get()` 을 호출하면 `no such element` 에러가 발생합니다.

아래 예제는 매번 유효한 Option 값과 누락된 Option 값 중 하나를 임의로 반환하는 `nextOption` 함수를 호출하겠습니다. 이 예제를 통해 Some 과 None 이 연산의 결과를 바꾸는지 보겠습니다.

```scala
scala> def nextOption = if (util.Random.nextInt > 0) Some(1) else None
nextOption: Option[Int]

scala> val a = nextOption
a: Option[Int] = Some(1)

scala> val b = nextOption
b: Option[Int] = None
```

아래 표는 연산 중 일부를 정리했습니다. 

|Name|Example|Description|
|:--|:--|:--|
|`fold`|`nextOption.fold(-1)(x => x)`|Some 인 경우 주어진 함수로 부터 추출한 값, None 인 경우 시작 값을 반환함|
|`getOrElse`|`nextOption getOrElse 5` 또는 `nextOption getOrElse { println("error!"); -1 }`|Some 의 값을 반환하거나 아니면 이름 매개변수의 결과를 반환|
|`orElse`|`nextOption orElse nextOption`|실제 값을 호출하지 않지만, None 인 경우 값을 채우려함. Option 이 비어 있지 않으면 Option 을 반한화고, 그렇지 않은 경우 주어진 이름 매개변수로부터 Option 을 반환|
|Match expressions|`nextOption match { case Some(x) => x; case None => -1 }`|`Some(x)` 의 표현식은 데이터를 추출하여 매치 표현식의 결괏값으로 사용되거나 또 다른 변환에 재사용할 수 있는 지정된 값 `x` 에 넣음|

### Try Collections 

`util.Try` 컬렉션은 에러 처리를 컬렉션 관리로 바꿔 놓습니다. 주어진 함수 매개변수에서 발생한 에러를 잡아내는 메커니즘을 제공합니다.

Scala 는 **예외(Exception)** 을 발생시켜 에러를 일으킬 수 있습니다. 예외가 제대로 처리되지 않으면 퍼를리케이션은 종료하게 됩니다.

예외는 코드, 라이브러리, JVM 에서 발생할 수 있습니다. 만약 `None.get` 또는 `Nil.head` 를 호출한다면 JVM 은 `java.util.NoSuchElementException` 을 일으키며, Null 값인 필드나 메소드에 접근한다면 `java.lang.NullPointerException` 을 발생시킵니다.

예외를 발생시키기 위해 새로운 `Exception` 키워드나 `throw` 를 사용하면 됩니다.

```scala
scala> throw new Exception("No DB connection, exiting...")
java.lang.Exception: No DB connection, exiting...
 ... 32 elided
```

예외를 발생시켜 보겠습니다.

```scala
scala> def loopAndFail(end: Int, failAt: Int): Int = {
 | for (i <- 1 to end) {
 | println(s"$i) ")
 | if (i == failAt) throw new Exception("Too many iterations")
 | }
 | end
 | }
loopAndFail: (end: Int, failAt: Int)Int
```

검사 기준보다 더 많이 반복하여 `loopAndFail` 로부터 예외가 발생하는지 확인해 보겠습니다. 다음은 예외가 어떻게 `for` 루프와 함수를 방해하는지 알아보겠습니다.

```scala
scala> loopAndFail(10, 3)
1)
2)
3)
java.lang.Exception: Too many iterations
 at $anonfun$loopAndFail$1.apply$mcVI$sp(<console>:10)
 at $anonfun$loopAndFail$1.apply(<console>:8)
 at $anonfun$loopAndFail$1.apply(<console>:8)
 at scala.collection.immutable.Range.foreach(Range.scala:160)
 at .loopAndFail(<console>:8)
 ... 32 elided
```

Option 처럼 `util.Try` 타입은 구현되어 있지 않지만, 2 개의 구현된 서브타입인 `Success` 와 `Failure` 를 가지고 있습니다. 각각 무슨 의미를 하는지 예제를 통해 알아보겠습니다.

```scala
scala> val t1 = util.Try( loopAndFail(2, 3) )
1)
2)
t1: scala.util.Try[Int] = Success(2)

scala> val t2 = util.Try{ loopAndFail(4, 2) }
1)
2)
t2: scala.util.Try[Int] = Failure(
 java.lang.Exception: Too many iterations) 
```

아래 표는 에러를 처리하는 전략입니다.

|Name|Example|Description|
|:--|:--|:--|
|`flatMap`|`nextError flatMap { _ => nextError }`|Success 인 경우 `util.Try` 를 반환하는 함수를 호출함으로써 현재의 반환값을 새로운 내장된 반환값에 매핑함. 예제 함수는 입력값을 취하지 않기 때문에 Success 로부터 사용하지 않는 입력값을 나타내는 언더스코어 사용|
|`foreach`|`nextError foreach(x => println("success!" + x))`|Success 인 경우 주어진 함수를 한 번 실행하고, Failure 일 때는 실행하지 않음|
|`getOrElse`|`nextError getOrElse 0`|Success 에 내장된 값을 반환하거나, Failure 인 경우 이름에 의한 매개변수 반환|
|`orElse`|`nextError orElse nextError`|`flatMap` 의 반대되는 메소드로 Failure 인 경우 `util.Try` 를 반환하는 함수 호출함. `orElse` 로 Failure 를 Success 로 전환할 수 있음|
|`toOption`|`nextError.toOption`|Success 는 Some 으로 Failure 는 None 이 됨.|
|`map`|`nextError map (_ * 2)`|Success 인 경우 새로운 값에 내장된 값을 매핑하는 함수를 호출|
|`Match expressions`|`nextError match { case util.Success(x) => x; case util.Failure(error) => -1 }`|Success 를 반환값으로 또는 Failure 를 예외로 처리하기 위해 매치표현식을 사용함|
|`Do nothing`|`nextError`|가장 쉬운 에러처리 방식|

많은 개발자들이 처리해야할 보편적인 예외는 문자열에 저장된 숫자를 검증하는 것입니다. 아래 예제는 `orElse` 연산자를 이용하여 문자열에서 숫자를 파싱하고, 성공 시 그 결과를 출력하는 `ofreach` 연산 사용 예제입니다.

```scala
scala> val input = " 123 "
input: String = " 123 "

scala> val result = util.Try(input.toInt) orElse util.Try(input.trim.toInt)
result: scala.util.Try[Int] = Success(123)

scala> result foreach { r => println(s"Parsed '$input' to $r!") }
Parsed ' 123 ' to 123!

scala> val x = result match {
 | case util.Success(x) => Some(x)
 | case util.Failure(ex) => {
 | println(s"Couldn't parse input '$input'")
 | None
 | }
 | }
x: Option[Int] = Some(123)
```

### Future Collections 

Future 는 백그라운드 작업을 개시합니다.

기본적으로 Scala 는 JVM 의 main 스레드에서 동작하지만, 병행 스레드에서 백그라운드 작업을 실행할 수 있도록 지원할 수 있습니다. Future 를 함수로 호출하면 현행 스레드가 계속 작업하는 동안 별도의 스레드에서 그 함수를 실행합니다. 따라서 Future 는 그 스레드의 최종 반환값의 모나딕 컨테이너일 뿐 아니라 백그라운드 Java 스레드의 감시자이기도 합니다.

메세지를 출력하는 함수로 Future 를 생성해보겠습니다.


```scala
scala> import concurrent.ExecutionContext.Implicits.global
import concurrent.ExecutionContext.Implicits.global

scala> val f = concurrent.Future { println("hi") }
hi
f: scala.concurrent.Future[Unit] =
 scala.concurrent.impl.Promise$DefaultPromise@29852487
```

백그라운드 작업은 Future 가 값을 반환하기도 전에 *hi* 를 출력했습니다. 다른 예로 백그라운드 작업이 여전히 실행하는 동안 퓨처를 받을 수 있게 Java 의 `Thread.sleep` 을 이용해보겠습니다.

```scala
scala> val f = concurrent.Future { Thread.sleep(5000); println("hi") }
f: scala.concurrent.Future[Unit] =
 scala.concurrent.impl.Promise$DefaultPromise@4aa3d36

scala> println("waiting")
waiting

scala> hi
```

백그라운드 작업은 5 초 동안 잠든 후 *hi* 메세지를 출력했고 그 사이에 main 스레드에서의 코드는 백그라운드 작업이 완료되기 전에 *waiting* 메세지를 출력했습니다.

Future 의 작업이 완료될 때 실행할 콜백 함수 또는 추가적인 퓨처도 설정할 수 있습니다. Future 는 비동기 / 동기식 모두 관리 될 수 있습니다.

**Handling Futures Asynchronously**

Future 가 완료된 다음 실행될 함수나 Future 에 결괏값을 전달하여 연결할 수 있습니다. 이 방식으로 처리된 Future 는 결국 그 함수의 반환값 또는 예외를 포함한 `util.Try` 를 반환합니다. 반환값을 받아 성공하면 연결된 함수 도는 Future 는 반환값에 전달되고, 성꽁 또는 실패를 반환하는 Future 로 전환됩니다.

Future 의 최종 결과를 받기 위해 콜백 함수를 지정할 수 있습니다. 콜백 함수는 최종 성공적인 값 또는 예외를 받아 그 Future 를 생성했던 원래 코드를 해제하여 다른 작업으로 넘어갈 수 있게 해줍니다.

아래 표는 Future 를 연결하고 콜백 함수를 설정하는 연산입니다. 이전 테이블에서와 같이 무작위로 실제 테스트 케이스를 제공하는 함수를 만들어 보겠습니다.

```scala
scala> import concurrent.ExecutionContext.Implicits.global
import concurrent.ExecutionContext.Implicits.global

scala> import concurrent.Future
import concurrent.Future

scala> def nextFtr(i: Int = 0) = Future {
 | def rand(x: Int) = util.Random.nextInt(x)
 |
 | Thread.sleep(rand(5000))
 | if (rand(3) > 0) (i + 1) else throw new Exception
 | }
nextFtr: (i: Int)scala.concurrent.Future[Int]
```

|Name|Example|Description|
|:--|:--|:--|
|`fallbackTo`|`nextFtr(1) fallbackTo nextFtr(2)`|2 번째 Future 를 1 번째 Future 에 연결하고 새로운 종합적인 Future 를 반환|
|`flatMap`|`nextFtr(1) flatMap nextFtr()`|2 번째 Future 를 1 번째 Future 에 연결하고 새로운 종합적인 Future 를 반환, 1 번째가 성공적이면 그 반환값이 2 번째를 호출하는 데 사용|
|`map`|`nextFtr(1) map (_ * 2)`|주어진 함수를 Future 에 연결하고 새로운 종합적인 Future 를 반환|
|`onComplete`|`nextFtr() onComplete { _ getOrElse 0 }`|Future 의 작업이 완료된 후 주어진 함수가 값 또는 예외를 포함한 `util.Try` 를 이용하여 호출|
|`onFailure`|`nextFtr() onFailure { case _ => "Error!" }`|Future 의 작업이 예외를 발생시키면 주어진 함수는 그 반환값을 가지고 호출|
|`onSuccess`|`nextFtr() onSuccess { case x => s"Got $x" }`|Future 의 작업이 성공적으로 완료되면 주어진 함수는 그 반환값을 가지고 호출|
|`Future.sequence`|`concurrent.Future sequence List(nextFtr(1), nextFtr(5))`|주어진 시퀀스에서 Future 를 병행으로 실행하여 새로운 Future 를 반환|

**Handling Futures Synchronously**

백그라운드 스레드가 완료되기를 기다리는 동안 스레드를 차단하는 것은 자원이 많이 소요되는 작업입니다. 트래픽 양이 많거나 높은 성능을 요구하는 어플리케이션이라면 이 방식을 피하고 `onComplete` 나 `onSuccess` 같은 콜백 함수를 사용하는것이 좋습니다.

현행 스레드를 차단하고 다른 스레드가 완료되기를 기다리기 위해서 백그라운드 스레드와 기다릴 수 있는 최대 시간을 취하는 `conCurrent.Await.result()` 를 사용합니다.

만약 Future 가 더 빨리 종료된다면 `Future` 의 결과가 반환되지만 Future 가 시간내에 완료되지 않으면 `java.util.concurrent.TimeoutException` 을 일으킵니다.

아래는 `concurret.Await.result` 사용법을 알기 위해 위에서 사용한 비동기식 함수를 사용하여 예를 들어보겠습니다.


```scala
scala> import concurrent.duration._
import concurrent.duration._

scala> val maxTime = Duration(10, SECONDS)
maxTime: scala.concurrent.duration.FiniteDuration = 10 seconds

scala> val amount = concurrent.Await.result(nextFtr(5), maxTime)
amount: Int = 6

scala> val amount = concurrent.Await.result(nextFtr(5), maxTime)
java.lang.Exception
 at $anonfun$nextFtr$1.apply$mcI$sp(<console>:18)
 at $anonfun$nextFtr$1.apply(<console>:15)
 at $anonfun$nextFtr$1.apply(<console>:15)
 ...
```


