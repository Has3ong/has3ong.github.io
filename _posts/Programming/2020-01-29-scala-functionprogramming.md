---
title : Scala 다양한 함수
tags :
- 익명함수
- anonymous function
- 순수함수
- pure function
- 고차함수
- higher-order function
- Scala
---

## 순수 함수와 고차 함수

컴퓨터 과학 관점에서 함수는 1차 함수, 고차 함수, 순수 함수와 같이 다양한 형태를 가질 수 있습니다.

이것은 수학의 관점에서도 마찬가지입니다. 고차 함수를 사용하여 다음 중 하나를 수행할 수 있습니다.

* 하나 이상의 함수를 파라미터로 사용해 일부 연산을 수행
* 함수에서 함수를 결과로 리턴

고차함수를 제외한 다른 모든 함수는 1차 함수입니다. 그러나 수학 관점에서 고차 함수는 연산자 또는 함수라 불립니다. 반면에 입력에 의해서만 결정되고 부수 효과가 없으며 관찰 가능한 함수를 순수 함수라고 합니다.

### 순수 함수

순수 함수를 가장 잘 사용한 예는 프로그램 / 어플리케이션의 코어를 순수함수로 만들고 네트워크 오버헤드와 예외 같은 모든 I/O 기능이나 부수 효과를 외부 효과에 노출하는 것 입니다.

순수함수의 예를 들어보겠습니다.

```scala
def pureFunction(Name : String) = s"My Name is $Name"
def notpureFunction(Name : String) = println(s"My Name is $Name")
```

위 두 예제를 봐서 `pureFuction` 순수 함수를 테스트 하려면 다음처럼 assert 에 순수 함수의 리턴 값과 입력을 기반으로 예상하는 값을 지정합니다.

```scala
assert(pureFunction("Alice") == "My Name is Alice")
```

순수 함수가 아닌경우 테스트하려면 표준 출력을 리디렉션한 후 assert 를 적용해야 합니다. 이처럼 순수 함수를 사용하면 코드 복제를 최소화해 코드를 쉽게 재사용할 수 있습니다.

다른 예도 알아보겠습니다.

```scala
scala> def pureSum(x: Int, y: Int) = x + y
pureSum: (x: Int, y: Int)Int

scala> def notpureSum(x: Int, y: Int) = println(x + y)
notpureSum: (x: Int, y: Int)Unit

scala>
```

순수 함수를 사용하면 테스트 코드를 추론하는데 도움이 됩니다.

```scala
def pureIncrease(x: Int) = x + 1
```

만약 순수함수로 작성하지 않으면 아래와 같이 작성해야 합니다.

```scala
def notpureIncrease() = {
  inc += 1
  inc
}
```

또한 순수함수는 다음과 같이 사용할 수 있습니다.

```scala
scala> def pureSum(x: Int, y: Int) = x + y
pureSum: (x: Int, y: Int)Int

scala> Seq.range(1, 10).reduce(pureSum)
res1: Int = 45
```

### 익명함수

보통 코드에서 함수를 정의하고 싶지 않을때 사용합니다.

예를통해 알아보겠습니다.

```scala
scala> def Fee(x: Double, rate: Double => Double): Double = {
  x + rate(x)
}
Fee: (x: Double, rate: Double => Double)Double

scala> Fee(100, (percent : Double) => percent * 0.05)
res3: Double = 105.0
```

이 예에서는 별도의 콜백 함수를 선언하는 대신 익명 함수를 직접 전달했고 `rate` 함수와 같이 동일한 작업을 수행했습니다.

익명함수에서는 타입을 생략할 수 있습니다.

```scala
scala> Fee(100, percent => percent * 0.05)
res5: Double = 105.0
```

### 고차함수

Scala 의 함수형 프로그래밍에서는 함수를 파라미터로 전달할 수 있고, 함수의 결과로 함수를 리턴할 수도 있습니다. 이를 고차함수라 정의합니다.

예를통해 알아보겠습니다.

```scala
Object Test {
  def main(args: Array[String]) {
    println(testHOF(paramFunction, 10))
  }
  
  def testHOF(func: Int => String, value : Int) = func(value)
  def paramFunction[A](x: A) = "[" + x.toString() + "]"
}
```

고차함수는 파라미터로 다른 함수를 받아들이고 결과로 리턴하는 함수로 정의할 수 있습니다.

간단한 함수 2개를 정의해보겠습니다.

```scala
def division(value : Int) : Double = value.toDouble / 2
def addTwo(value : Int) : Int = value + 2
```

위와같이 두 함수의 공통점은 두 함수 모두 Int 를 받고 AnyVal 을 호출할 수 있는 처리된 다른 값을 리턴합니다. 이제 파라미터 중에서 다른 함수를 받는 고차함수를 정의해보겠습니다.

```scala
def printRange(start: Int, end: Int, func: Int => AnyVal): Unit = {
  for(i <- start to end)
    println(func(i))
}
```

위 함수를 이용해 출력해보겠습니다.

```
scala> def printRange(start: Int, end: Int, func: Int => AnyVal): Unit = {
     |     for(i <- start to end)
     |         println(func(i))
     | }
printRange: (start: Int, end: Int, func: Int => AnyVal)Unit

scala> def addTwo(value : Int) : Int = value + 2
addTwo: (value: Int)Int

scala> def division(value : Int) : Double = value.toDouble / 2
division: (value: Int)Double

scala> printRange(1, 10, addTwo)
3
4
5
6
7
8
9
10
11
12

scala> printRange(1, 10, division)
0.5
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
5.0

scala>
```

고차함수를 이용해서 익명함수 Fee 다시 정의해보겠습니다.

```scala
def Fee(x: Double, rate: Double => Double): Double = {
  x + rate(x)
}
def rate(x: Double) = x * 0.05

Fee(100, rate)
105.0
```

### 함수를 리턴 값으로 사용

고차함수를 이용하여 다음과 같이 사용할 수 있습니다.ㅌ

```scala
def Fee(x: Double) = {
  if (x > 1000)
    (x: Double) => "X is greater than 1000 value is : " + x * 0.05
  else
    (x: Double) => "X is not greather than 1000 value is : " + x * 0.05
}
val returned = Fee(2000)
returned(2000)
res8: String = X is greater than 1000 value is : 100.0
```

### 고차 함수 사용

고차함수를 사용한 curry, uncurry 함수를 사용해 보겠습니다.

아래 예제를 통해 보시면 됩니다.

```scala
trait Curry {
    def curry[A, B, C](f: (A, B) => C): A => B => C
    def uncurry[A, B, C](f: A => B => C): (A, B) => C
}

object CurryImplement extends Curry {
    def curry[A, B, C](f: (A, B) => C): A => B => C = {
        (x: A) => {
            (y: B) => f(x, y)
        }
    }
    def uncurry[A, B, C](f: A => B => C): (A, B) => C = {
        (x: A, y: B) => f(x)(y)
    }
}


object Scala{
    def main(args: Array[String]) : Unit = {
        def add(x: Int, y: Long) : Double = x.toDouble + y

        val PlusCount = CurryImplement.curry(add)
        println(PlusCount(3)(4L))

        val increment = PlusCount(2)
        println(increment(1L))

        val unadd = CurryImplement.uncurry(PlusCount)
        println(unadd(1, 6L))
    }
}
```

**currying** : 다중의 파라미터를 갖는 함수를 단일 파라미터를 갖는 함수로 바꾸는 것을 말합니다.

**uncurrying** : 커링에 대한 역함수화의 한 형태입니다. 함수 f 를 취하면 함수 g 를 리턴 받고 함수 f 와 g 모두에 파라미터를 받는 새로운 함수 h 를 만듭니다. 그리고 결과로 해당 파라미터에 대해 f 어플리케이션과 차례로 g 어플리케이션을 리턴합니다.