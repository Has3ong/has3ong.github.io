---
title : Scala 변수
tags :
- Variable
- Data Type
- Scala
---

## Scala Variable

`Scala`에서 변수를 선언하려면 `var` 또는 `val` 키워드를 사용해야한다. `Scala`에서 변수를 선언하는 정식 구문은 다음과 같다.

```
val / var 변수이름 : 데이터타입 = 초기값
```

일반적으로 가변 변수를 선언하려면 `var` 키워드를 이용한다. 하지만 불변 변수 즉, 상수를 선언하려면 `val` 키워드를 사용한다.

`val`로 선언한 변수에 값을 변경하려 하면 `reassignment to val`이라는 에러를 표시한다.

> Example

```scala
var Var : Int = 10
val Val : String = "Hello World!"
```

데이터 타입을 지정하지 않고 변수만 선언할 수 있다.

```scala
var Var = 10
val Val = "Hello World!"
```

## Scala Variable Scope

`Scala` 변수는 선언한 위치에 따라 세 가지 범위(scope)를 가진다.

### Field

`Scala` 코드의 클래스 인스턴스에 속한 변수다. 필드는 객체의 모든 메소드 내부에서 접근할 수 있다. 그러나 접근 한정자에 따라 필드는 다른 클래스의 인스턴스에서 필드에 접근될 수 있다.

### Method Arguments

메소드 파라미터는 변수에 포함되며, 메소드가 호출될 때 메소드 내부에 값을 전달하기 위해 사용될 수 있다. 메소드 파라미터는 메소드 내부에서만 접근할 수 있다. 그러나 전달되는 객체는 외부에서 접근할 수 있다.

### Local Variable

지역 변수는 메소드 내부에서 선언되며, 메소드 내부에서 접근할 수 있다. 그러나 호출하는 코드는 리턴된 값을 통해 접근할 수 있다.

## Scala Data Type

`Scala`는 `JVM`언어이기 때문에 `Java`와 공통점을 공유한다. 즉, `Scala` 와 `Java` 동일한 데이터 타입을 공유한다. 즉 메모리 구조와 정밀도가 동일하다.

|Number|Data Type Description|
|:------:|:---------|
|1|Byte: 8bit -128 to 127|
|2|Short: 16bit -32768 to 32767|
|3|Int: 32bit -2147483648 to 2147483647|
|4|Long: 64bit -9223372036854775808 to 9223372036854775807|
|5|Float: 32bit IEEE 754 단정밀도 부동소수점|
|6|Double: 64bit IEEE 754 배정밀도 부동소수점|
|7|Char: 16bit 유니코드 글자 U+0000 to U+FFFF|
|8|String: Char의 Sequence|
|9|Boolean: Literal true or false|
|10|Unit: 값이 없음|
|11|Null: NUll or 비어있음|
|12|Nothing: 모든 타입의 하위 타입이고 값이 없음을 포함한다.|
|13|Any: 모든 타입의 상위 타입이고 모든 타입은 Any 타입이다.|
|14|AnyRef: 모든 참조 타입의 상위 타입이다.|

## Type Ascription

타입 어스크립션은 유효한 모든 타입에서 표현식에 예상되는 타입을 컴파일러에 알리기 위해 사용되며, is-a 관계에 적용되는 타입 중 하나이거나 범위에 적용되는 변환입니다.

> Example

```scala
scala> val s = "Hello World"
s: String = Hello World

scala> val p = s:Object
p: Object = Hello World

scala>
```

## 느긋한 val

바인딩된 표현식이 즉시 계산되지 않고 처음 접근할 때 한 번에 계산된다. 처음 접근할 떄 표현식이 계산되고 표현식의 결과는 식별자인 lazy val에 바인딩된다. 다음에 접근할 때는 추가로 계산되지 않고 대신 저장된 결과가 즉시 리턴된다.

> Example

```scala
scala> lazy val num = 1 / 0
num: Int = <lazy>
```

0으로 나누더라도 에러를 던지지 않고 코드가 실행이 되는걸 볼 수 있다.

```scala
scala> val x = {println("x"); 20}
x
x: Int = 20

scala> x
res0: Int = 20

scala>
```

추후 필요할 때 변수 x의 값에 접근할 수 있다.