---
title : Scala final vs val
tags :
- val
- final
- Scala
---

Scala 에서 사용하는 val 키워드와 final 키워드를 비교하기 위해 간단한 동물과 사람 클래스를 선언해 보겠습니다.

> val 

```
scala> class Animal {
     |     val age = 2
     | }
defined class Animal

scala> class Cat extends Animal {
     |     override val age = 3
     |     def printAge = {
     |         println(age)
     |     }
     | }
defined class Cat

scala> val cat: Cat = new Cat()
cat: Cat = Cat@317a118b

scala> cat.printAge
3
```

> final 

```
scala> class Person {
     |     final val age = 3
     | }
defined class Person

scala> class Students extends Person {
     |     override val age = 5
     | }

<console>:13: error: overriding value age in class Animal of type Int(3); value age cannot override final member
           override val age = 5
                        ^
scala>
```

age 변수를 val 로 선언했을 시 Override가 되는데 final 키워드로 사용했을 시 다음과 같은 에러가 발생한다.