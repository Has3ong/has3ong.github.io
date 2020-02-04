---
title : Scala Constructor
tags :
- Constructor
- Scala
---

## Scala Constructor

Scala 에서 생성자의 개념과 사용법은 Java 와 다르다. 

Scala 에는 두 가지타입의 생성자 즉, 기본 생성자와 보조 생성자가 있습니다. 기본 생성자는 클래스의 몸체이며, 클래스 이름 바로 뒤에 파라미터 목록이 나타납니다.

기본 생성자의 예시를 보여드리겠습니다.

```scala
class Animal (animalName:String, animalAge:int){
  def getAnimalName () : String = {
    animalName
  }
  
  def getAnimalAge () : Int = {
    animalAge
  }
}

object Example extends App {
  val animalobject = new Animal("Cat" , 3)
  println(animalobject.getAnimalName)
  println(animalobject.getAnimalAge
}
```

생성자를 표현하기 위한 클래스 정의 시간에 파라미터가 주어집니다. 생성자를 선언할 때 생성자에 지정된 파라미터의 기본 값을 제공하지 않고서는 클래스를 생성할 수 없습니다. Scala 는 생성자에 필요한 파라미터를 제공하지 않은채 객체를 인스턴스로 생성할 수 있습니다.

보조 생성자를 사용할 때 제약이 있지만 원하는 만큼 보조 생성자를 추가할 수 있습니다. 보조 생성자는 몸체의 첫번째 라인에서 이전에 선언된 다른 **보조 생성자** 또는 **기본 생성자** 를 호출해야 합니다. 이 규칙을 따르기 위해 각 보조 생성자는 직접 또는 간접적으로 기본 생성자를 호출해야 합니다.

보조 생성자의 예시를 보여드리겠습니다.

```scala
class Animal (animalName:String, animalAge:int){
  // 보조 생성자
  def this(animalName:String) = this(animalName, "")
  def sayName() = println(animalName + animalAge)
}

object Constructors {
  def main(args: Array[String]): Unit = {
    val animal = new Animal("Hello Dog", 3)
    animal.sayName()
  }
}
```

기본 생성자에 보조 생성자가 2 Line 에서 메세지가 포함됐습니다. 기본 생성자는 새로운 Animal 객체를 인스턴스화하며, sayName() 메소드는 연결된 메세지를 출력합니다.

> 보조생성자

Scala 에서는 Scala 클래스에서 하나 이상의 보조 생성자를 정의하면 클래스 소비자는 여러 방법으로 객체 인스턴스를 생성할 수 있다. this라는 클래스 메소드로 보조 생성자를 정의할 수 있다. 여러 보조 생성자를 정의할 수 있지만, 다른 시그니처가 있어야한다. 또한 각 생성자는 이전에 정의된 생성자 중 하나를 호출해야 한다.