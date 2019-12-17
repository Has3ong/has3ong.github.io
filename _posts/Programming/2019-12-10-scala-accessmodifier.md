---
title : Scala Access Modifier
tags :
- Private 
- Protected
- Public
- Access Modifier
- Scala
---

## Scala Access Modifier

OOP와 Scala는 비슷하다.

|접근자|클래스|컴패니언 오브젝트|패키지|하위클래스|프로젝트|
|:-:|:-:|:-:|:-:|:-:|:-:|
|default / public|O|O|O|O|O|
|protected|O|O|O|X|X|
|private|O|O|X|X|X|

### public

private 과 protected 와 달리 키워드를 지정할 필요가 없다. public 멤버에 대한 명시적인 한정자가 없다. public 멤버는 어디서나 접근할 수 있다.

```scala
class OuterClass {
  class InnerClass {
    def printName() { println("Hello World") }
    class InnerMost {
      printName()
    }
  }
  
  (new InnerClass).printName() // 동작
}
```

### protected

protected 멤버가 정의된 클래스의 하위 클래스에서만 접근할 수 있다.

```scala
package MyPackage{
  class SuperClass {
    protected def printName(){
      println("Hello World!")
    }
  }
  
  class SubClass extends SuperClass {
    printName() // 동작
  }
  
  class otherClass {
    (new SuperClass).printName() // Error
  }
}
```

### private

멤버 정의가 포홤된 클래스 또는 객체 내부에서만 사용할 수 있다.

```scala
package MyPackage{
  class SuperClass{
    private def printName() {
      println("Hello World!");
    }
  }
  
  class SubClass extends SuperClass {
    printName() // Error
  }
  
  class otherClass {
    (new SuperClass).printName() // Error
  }
}
```

Scala는 이외에도 **수식자(qualifier)** 를 사용해 확장할 수 있다. `private[X]` / `protected[X]` 형태의 한정자는 각각 접근이 X까지 private 또는 protected 임을 의미한다. 아래 예제를 통해 살펴보겠습니다.

```scala
package Country{
  package Professional {
    class Executive {
      private[Professional] var jobTitle = "Big Data"
      private[Country] var friend = "Scala"
      protected[this] var secret = "Age"
      
      def getInfo(another : Execeutive) {
        println(another.jobTitle)
        println(another.friend)
        println(another.secret) // Error
        println(this.secret) // 동작
    }
  }
}
```

위 코드의 간단한 참고 내용 입니다.

* jobTitle 변수는 Professional 패키지 내의 모든 클래스에 접근이 가능하다.
* friend 변수는 Country 패키지 내의 모든 클래스에서 접근할 수 있다.
* secret 변수는 인스턴스 메소드(this)의 암시(implicit) 객체에만 접근할 수 있다.

위 예제에서는 package 키워드를 사용했습니다.