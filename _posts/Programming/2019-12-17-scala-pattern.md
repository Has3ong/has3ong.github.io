---
title : Scala Pattern Macthing
tags :
- Pattern Matching
- Scala
---

## Pattern Matching

Scala 패턴 매칭에는 일련의 대안이 있고, 각각은 case 키워드로 시작됩니다. 각 대안은 패턴이 일치하고 평가되는 패턴과 표현식을 갖습니다.

또한 화살표 심볼 => 은 표현식에서 패턴을 분리합니다. 예를 통해 알아보겠습니다.

> Example

```scala
object PatternMatching1{
    def main(args: Array[String]) : Unit = {
        println(matchInteger(3))
    }

    def matchInteger(x: Int): String = x match {
        case 1 => "one"
        case 2 => "two"
        case _ => "Greater than two"
    }
}
```

Result

```
Greater than two
```

case 문은 정수를 문자열에 매핑하는 함수로 사용됩니다. 다음은 여러 타입에 일치하는지 확인하는 예 입니다.

> Example 

```scala
object PatternMatching2{
    def main(args: Array[String]) : Unit = {
        println(comparison("Hello"))
        println(comparison("World"))
        println(comparison(1))
        println(comparison(1.3))
    }

    def comparison(x: Any): Any = x match {
        case 1 => "one"
        case 1.3 => "one dot three"
        case 2 => "two"
        case "Hello" => "Hello World"
        case _ => "nothing"
    }
}
```

Result

```
Hello World
nothing
one
one dot three
```