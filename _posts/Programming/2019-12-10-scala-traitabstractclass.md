---
title : Scala Trait / Abstract Class
tags :
- Case Class
- Abstract Class
- Trait
- Scala
---

## Scala Trait

Scala의 Trait는 Java의 인터페이스 개념과 비슷합니다. 단, 실체 메소드를 포함할 수 있습니다. Java8의 인터페이스에서는 구체적인 메소드를 지원합니다.

Trait는 Scala의 새로운 개념입니다. 생성자가 없다는 점을 제외하면 추상클래스처럼 보입니다. 

Trait 사용예시를 보여드리겠습니다.

```scala
trait Animal {
  val age : Int
  val gender : String
  val origin : String
}
```

트레이트나 클래스를 확장하려면 extend 키워드를 사용하면 됩니다. 트레이트는 구현하지 않은 메소드를 포함하기 때문에 인스턴스화 할 수없으므로 트레이트에 추상 멤버를 구현해야 합니다.

```scala
trait Dog extends Animal {}
```

Scala 의 추상 클래스와 트레이트의 차이점은 추상 클래스는 생성자 파라미터, 타입 파라미터등 여러 파라미터를 가질 수 있지만, Scala의 트레이트에는 타입 파라미터만 가질 수 있습니다.

또한, 추상 클래스는 트레이트를 확장 시킬 수 있습니다.

```scla
abstract class Cat exnteds Animal {}
```

## Scala Abstract Class

Scala의 추상 클래스는 타입 파라미터뿐만 아니라 생성자 파라미터를 가질 수 있다. Scala의 추상 클래스는 Java와 상호운용되어 중간에 wrapper를 두지 않고 Java 코드를 호출 할 수 있습니다.

Scala의 추상클래스 사용예시를 보여드리겠습니다.

```scala
abstract class Animal(animalName : String = "Undefined") {
  // 1. 메소드 정의 / 리턴 타입 X
  def getAnimalAge
  
  // 2. 메소드 정의 X
  def getAnimalGender : String
  
  // 3. 메소드 구현이 없음을 명시적으로 알리는 방법
  def getAnimalOrigin() : String {}
  
  // 4. 하위 클래스에서 구현할 필요가 없지만 오버라이드할 수 있다.
  def getAnimalName : String = {
    animalName
  }
}
```

이 클래스를 다른 클래스로 확장시키리면 `getAnimalAge`, `getAnimalGender`, `getAnimalOrigin` 메소드를 구현해야한다. `getAnumalName`의 구현은 이미 있기 때문에 재정의할 수 있다.

### Override

슈퍼클래스에서 실체 메소드를 재정의하려면 override 한정자를 추가해야한다. 그러나 추상 메소드를 구현하는 경우 override 한정자가 필요는 없다. Scala 는 override 키워드를 사용해 부모 클래스의 메소드를 재정의합니다.

예를 통해 알아보겠습니다.

> Example

```scala
abstract class Test {
    var message : String = "null"
    def setMessage(message : String): Unit
    def printMessage() : Unit
}
```

실제 구현 클래스를 추가해보겠습니다.

```scala
class TestImplements extends Test {
    def setMessage(contents: String): Unit = {
        this.message = contents
    }
    def printMessage(): Unit = {
        println(message)
    }
}
```

다음으로 이 실체 클래스의 동작을 수정할 수 있는 트레이트를 생성합니다.

```scala
trait TestTrait extends Test {
    abstract override def setMessage(contents: String) = printMessage()
}
```

이제 클래스를 사용해보겠습니다.

```scala
val printer : TestImplements = new TestImplements()
printer.setMessage("Hello World")
printer.printMessage()
```

Result

```
Hello World
```

## Scala Case Class

케이스 클래스는 자동으로 생성되는 메소드를 퐘한 인스턴스를 생성할 수 있는 클래스 입니다. 또한 케이스 클래스는 자동으로 생성되는 캠패니언 오브젝트도 포함합니다.

스칼라에서 케이스 클래스의 기본 구문은 다음과 같습니다.

```
case class <식별자> ([var] <식별자> : <타입:> [, ...])[extends <식별자>(<입력 파라미터>)] [{필드와 메소드}]
```

일반 클래스와 마찬가지로 케이스 클래스는 생성자 파라미터에 대해 자동으로 게터 메소드를 정의합니다. 다음 코드 예제를 보겠습니다.

> Example

```scala
object CaseClass{
    def main(args: Array[String]) : Unit = {
        case class Character(name : String, isHacker: Boolean)

        val nail = Character("Nail", true)
        val joyce = nail.copy(name = "Joyce")
        
        println(nail == joyce)
        println(nail.equals(joyce))
        println(nail.equals(nail))
        println(nail.hashCode())
        println(nail)

    }
}
```

Result

```
false
false
true
512894591
Character(Nail,true)
```