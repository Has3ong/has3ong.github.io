---
title : Scala Implicit
tags :
- Implicit
- Scala
---

## Implicit

Scala 에서 제공하는 암시는 다음과 같이 3가지 참조할 수 있습니다.

* 자동으로 전달될 수 있는 값
* 한 타입에서 다른 타입으로 자동 변환
* 클래스의 기능을 확장하는 데 사용

실제 자동 변환은 다음 예와 같이 implicit def 로 수행할 수 있습니다.

```scala
scala> implicit def stringToInt(s: String) = s.toInt
stringToInt: (s: String)Int
```

다음 코드도 실행이 가능합니다.

```scala
scala> def add(x:Int, y:Int) = x+y
add: (x: Int, y: Int)Int

scala> add(1, "2")
res0: Int = 3

scala>
```

add 함수에서 요구하는 파라메터는 둘 다 Int 타입이다. 하지만, add 에 전달된 파라미터중 하나가 String 타입이지만 암시적 변환을 수행하여 String 타입을 Int 타입으로 자동 변환이 된다.

암시의 첫 번째 타입은 암시적 파라미터를 자동으로 전달할 수 잇는 값이다. 파라미터는 일반적인 파라미터와 같이 메소드를 호출하는 동안 전달되지만 스칼라 컴파일러는 자동으로 파라미터를 채운다. Scala 컴파일러는 암시적 파라미터를 자동으로 채우지 못한다면 불평할 것이다.

다음은 암시의 첫 번째 타입을 보여주는 예다.

```scala
def add(implicit num : Int) = 2 + num
```

메소드를 호출할 때 암시적 파라미터인 num 을 제공하지 않으면 num 에 대한 암묵적인 값을 찾을 수 있게 컴파일러에 요청한다. 다음과 같이 컴파일러에 암시적 값을 정의한다.

```scala
implicit val adder = 2
```

그리고 함수를 다음과 같이 호출 할 수 있다.

```
add
```

메소드에 명시적 파라미터와 암시적 파라미터를 모두 포함할 수 있다. 다음 Scala REPL 예를 살펴보자.

```scala
scala> def helloworld(implicit a: Int, b:String) = println(a, b)
helloworld: (implicit a: Int, implicit b: String)Unit

scala> val i = 2
i: Int = 2

scala> implicit val b = ""
b: String = ""

scala> helloworld(2, implicitly)
(2,)

scala> helloworld(2, implicitly[String])
(2,)
```

implicitly 는 Scala 2.8 버전부터 사용할 수 있는 함수로서 타입 T 의 암시 값이 존재하는지 확인하고 해당 값을 리턴하는 데 사용한다.

그러나 Scala 컴파일러는 helloworld 메소드의 두 번째 파라미터가 사용되기 전에 먼저 암시가 선언된 변수가 없으면 에러를 발생시킨다. 다음 REPL 예제를 보겠습니다.

```scala
scala> def helloWorld(implicit a : Int, b : String) = println(a, b)
helloWorld: (implicit a: Int, implicit b: String)Unit

scala> val i = 2
i: Int = 2

scala> helloWorld(i, implicitly)
<console> :14: error: ambiguous implicit values:
both value StringCanBuildFrom in object Predef of type => scala.collection.generic.CanBuildFrom[String,Char,String] and method $conforms in object Predef of type[A]=> <:<[A,A] match expected type T
  helloWorld(i, implicitly)
```

helloWorld 함수의 매개변수로 일반 상수 값을 사용하면 잘 동작합니다.

```scala
scala> def helloWorld(implicit a : Int, b : String) = println(a, b)
helloWorld: (implicit a: Int, implicit b: String)Unit

scala> helloWorld(20, "Hello World!")
(20,Hello World!)

scala>
```