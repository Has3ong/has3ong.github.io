---
title : Scala Method / Class / Object
tags :
- Class
- Object
- Method
- Scala
---

## Scala Method

```
def min(x : Int, y: Int) : Int = {
    if (x < y) x else y
}
```

이 메소드는 2개의 파라메터를 비교해서 작은 값을 리턴한다.

Scala의 모든 메소드는 `def` 키워드로 시작해야 하고, 그 다음에 메소드의 이름이 온다. 선택적으로 메소드에 파라미터를 전달하지 않거나 아무것도 리턴하지 않을 수 있다.

또한, Scala에서는 중괄호를 사용하지 않고 메소드를 정의할 수 있다.

```
def min(x : Int, y: Int) : Int= if (x < y) x else y
```

메소드에 코드 양이 적다면 위 메소드처럼 선언할 수 있다.

또한 필요한 파라미터를 메소드에 전달하지 않고 메소드 안에서 선언할 수 있다.

```
def getPiValue(): Double = 3.14159
```

괄호가 있거나 없는 메소드는 부수효과의 유무를 의미한다. 위 메소드처럼 아래와 같이 중괄호를 사용하지 않을 수 있다.

```
def getPiValue: Double = 3.14159
```

또한, 파라미터 타입을 명시적으로 언급해 값을 리턴하는 메소드도 있다.

```
def Hello(word: String) = "Hello" + word + "!"
```

이 코드는 아래와 같이 사용할 수 있다.

```
scala> def Hello(word: String) = "Hello" + word + "!"
Hello: (word: String)String

scala> Hello("Scala Test")
res1: String = HelloScala Test!

scala>
```

### Scala Return

Scala 메소드 구조

```
def 함수이름 ([파라미터 목록]) : [return 타입] = {
  함수내용
  return 값
}
```

위에 min 함수를 이용해서 예시를 보여드리겠습니다. Scala 에서 return 키워드는 선택적이기 때문에 return 키워드가 없으면 마지막 할당 값을 리턴하게 설계됐다.

```
scala> def min(x : Int, y: Int) : Int = {
     |     if (x < y) x else y
     | }
min: (x: Int, y: Int)Int

scala> min(3, 5)
res2: Int = 3

scala>
```

## Scala Class

Scala의 클래스는 설계도로 간주되며, 실제로 메모리에 표현될 무언가를 생성하기 위해 해당 클래스를 인스턴스화한다. 클래스에 전체적으로 멤버라 불리는 메소드, 값, 변수, 타입, 오브젝트, 트레이트, 클래스를 포함할 수 있다.

다음 클래스의 예를 보여드리겠습니다.

```scala
class Person {
    var Name : String = null
    var Age : Int = 26

    def setPersonName(value: String){
        this.Name = value
    }

    def setPersonAge(value: Int){
        this.Age = value
    }

    def getPersonName() : String = {
        Name
    }

    def getPersonAge() : Int = {
        Age
    }
}
```

위 클래스 코드는 Setter 와 Getter 라는 두 변수 Name, Age를 가지고있습니다. 이 클래스를 이용해서 몇가지 조작을 해보겠습니다.

```scala
object Person{
    def main(args: Array[String]) : Unit = {
        val Jack : Person = new Person
        

        Jack.setPersonName("Jack")
        println(Jack.getPersonName())
        println(Jack.getPersonAge())
    }
}
```

Result

```
$ scala HelloWorld.scala
Jack
26
```

## Scala Object

Scala의 객체는 기존 OOP 와 약간 다른 의미를 가지고있다. OOP에서 객체는 클래스의 인스턴스지만 scala에서 객체로 선언된 모든것은 인스턴스화할 수 없다.

Scala의 객체는 `object`가 키워드다. Scala에서 객체를 선언하는 기본 구문은 다음과 같다.

```
object <식별자> [extends <식별자>] [{필드, 메소드, 클래스}]
```

이 구문을 이해하기 위해 Hello World 프로그램을 다시 살펴보겠습니다.

```scala
object HelloWorld{
    def main(args:Array[String]){
        println("Hello World!")
    }
}
```

이 HelloWorld에서 Java와의 가장 큰 차이점은 main 메소드가 클래스 내부가 아니라 오브젝트 내부에 있다는 점이다.

Scala에서 키워드 object는 다음과 같은 두 가지를 의미한다.

1. OOP처럼 오브젝트는 클래스의 인스턴스처럼 나타낼 수 있다.
2. Singleton 이라는 매우 다른 타입의 인스턴스 객체를 나타내는 키워드다.

Singleton 은 추후 다른 포스트에서 설명 드리겠습니다.