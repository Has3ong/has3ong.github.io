---
title : Scala Working with Data Literals, Values, Variables, and Types
tags :
- Tuple
- Literal
- Type
- Variable
- Scala
---

*이 포스트는 [Learning Scala](http://188.166.46.4/get/PDF/Jason%20Swartz-Learning%20Scala_125.pdf) 를 바탕으로 작성하였습니다.*

* **리터럴(Literal)** 은 숫자 5, 문자 A, 텍스트 'Hello World' 처럼 소스코드에 바로 등장하는 데이터 입니다.
* 값은 불변의 타입을 가지는 저장 단위입니다. 값을 정의될 때 데이터가 할당될 수 있지만, 절대 재할당 될 수는 없습니다.
* 변수는 가변의 타입을 갖는 저장 단위입니다. 변수는 정의시 데이터를 할당할 수 있으며, 재할당이 가능합니다.
* 타입은 작업한느 데이터의 종류로 데이터의 또는 분류를 의미합니다. Scala 의 모든 데이터는 특정 타입에 대응하며, 모든 Scala 타입은 그 데이터를 처리하는 메소드를 갖는 클래스로 정의합니다.

Scala 에서 값과 변수에 저장된 데이터를 더 이상 사용하지 않으면 JVM 의 GC 가 자동으로 할당을 취소합니다.

Scala **REPL(Read-Evaluate-Print-Loop)** 에서 데이터로 작업하면서 이 용어들을 사용해보겠습니다. 스칼라의 값은 구문 `val <name>: <type> = <literal>` 로 정의합니다.

```scala
scala> val x: Int = 5
x: Int = 5
```

REPL 은 값 정의를 읽어 들이고, 이를 평가하고 확인차 재출력합니다. 이제 이름 x 의 새로운 값이 정이되고 사용할 수 있습니다. 이 값을 사용해보겠습니다.

```scala
scala> x
res0: Int = 5

scala> x * 2
res1: Int = 10

scala> x / 5
res2: Int = 1
```

각 3 개의 입력줄은 유효한 Scala 구문으로 정숫값을 반환합니다. 각 경우마다 값을 반환하므로 REPL 은 그 값과 타입을 반복하고 `res0` 을 시작으로 순차적으로 번호가 매겨진 유일한 이름의 값을 할당합니다.

```scala
scala> res0 * res1
res3: Int = 50
```

여기에 `res0` 과 `res` 을 곱하면 값 50 이 반환되고 새로운 값 `res3` 에 저장됩니다. 값과 달리 변수는 변경할 수 있습니다. 구문 `var <name>: <type> = <literal>` 로 정의합니다.

```scala
scala> var a: Double = 2.72
a: Double = 2.72

scala> a = 355.0 / 113.0
a: Double = 3.1415929203539825

scala> a = 5
a: Double = 5.0
```

이 구문에서 **배정밀도 부동 소수점 숫자(double-precision floating-point number)** 인 Double 타입을 가지고 변수 `a` 를 정의하였습니다. 그리고 `a` 는 변수이므로 여기에 다른 값을 재할당해보았습니다.

## Values

**값(value)** 는 불변의 타입을 가지는 스토리지 단위며, 관례적으로 데이터를 저장하는 기본적인 방법입니다. `val` 키워드를 사용하여 새로운 값을 정의할 수 있습니다.

**Syntax: Defining a Value**

```scala
val <identifier>[: <type>] = <data>
```

값은 이름과 할당된 데이터 모두 필요하지만, 명시적인 타입이 있어야 하는것은 아닙니다. 타입이 지정되지 않았다면, Scala 컴파일러는 할당된 데이터를 기반으로 타입을 추론합니다.

```scala
scala> val x: Int = 20
x: Int = 20

scala> val greeting: String = "Hello, World"
greeting: String = Hello, World

scala> val atSymbol: Char = '@'
atSymbol: Char = @
```

Scala 에서는 값 정의에서 타입을 지정하는것이 선택사항입니다. 값 할당을 기반으로 그 타입을 추론하는것이 가능하면 제외하고 선언을 해도 됩니다. Scala 컴파일러는 할당된 값을 보고 그 값의 타입을 알아차립니다. 이를 **타입 추론(Type Inference)** 라고 합니다. 값을 타입 없이 정의하더라더 타입이 없는것이 아니며, 마치 타입을 지정하여 정의한것처럼 적절한 타입을 할당합니다.

타입을 지정하지 않은 예를 보겠습니다.

```scala
scala> val x = 20
x: Int = 20

scala> val greeting = "Hello, World"
greeting: String = Hello, World

scala> val atSymbol = '@'
atSymbol: Char = @
```

Scala 컴파일러는REPL 을 통해 각각 Int, String, Char 에 대응함을 알 수 있습니다.

타입 추론을 사용하면 면시적으로 값의 타입을 작성할 필요가 없기 때문에 코드를 작성할 때 유용합니다. 하지만, 코드의 가독성을 떨어뜨리지 않는 범위에서 사용해야 합니다.

타입추론이 데이터를 저장하는 데 사용할 올바른 타입을 추론하겠지만, 개발자가 설정한 명시적인 타입을 대체하지는 않습니다. 초깃값과 호환되지 않는 타입으로 정의하면 컴파일 에러가 발생합니다.

```scala
scala> val x: Int = "Hello"
<console>:7: error: type mismatch;
    found : String("Hello")
    required: Int
        val x: Int = "Hello"
```

위 에러 메세지는 Int 타입에 String 을 저장할 수 없음을 알려줍니다.

## Variables

컴퓨터 과학에서 **변수(Variable)** 은 값을 저장하고 그 값을 가져올 수 있도록 할당하거나 예약된 메모리 공간에 대응하는 유일한 식별자를 의미합니다. 메모리 공간이 예약되어 있는 동안에는 새로운 값을 계속 할당할 수 있습니다. 따라서 메모리 공간의 내용은 동적이며 가변적입니다.

Scala 에서는 관례상 변수보다 값을 선호합니다. 이는 값을 사용하면 소스 코드가 안정적이며 예측할 수 있기 때문입니다. 값이 유지되므로 코드를 읽고 디버깅하는 일이 더 쉬우며, 가변데이터보다 더 안정적이며 에러가 발생할 가능성이 적기 때문입니다.

Scala 에서는 주어진 이름, 타입, 할당으로 변수를 정의할 때는 `var` 키워드를 사용합니다.

**Syntax: Defining a Variable**

```scala
var <identifier>[: <type>] = <data>
```

변수를 정의하고 재할당하는 예로 그 변수와 다른 숫자를 곱해보겠습니다.

```scala
scala> var x = 5
x: Int = 5

scala> x = x * 4
x: Int = 20
```

변수에 재할당이 가능하지만, 지정된 타입을 바꿀 수는 없으므로 그 변수의 타입과 호환되지 않는 타입의 데이터를 재할당할 수 없습니다. 예를 들어, 타입 Int 의 변수를 정의하고 여기에 String 값을 할당하면 컴파일 에러가 발생합니다.

```scala
scala> var x = 5
x: Int = 5

scala> x = "what's up?"
<console>:8: error: type mismatch;
    found : String("what\'s up?")
    required: Int
        x = "what's up?"
            ^
```

하지만 Double 타입 변수를 정의하고 여기에 Int 값을 할당하면, Int 숫자는 자동으로 Double 숫자로 전환될 수 있어 정상적으로 동작합니다.

```scala
scala> var y = 1.5
y: Double = 1.5

scala> y = 42
y: Double = 42.0
```

## Naming

Scala 이름에는 문자, 숫자, 그리고 다양한 특수 **연산자(operator)** 기호를 사용할 수 있습니다. 따라서 좀 더 표현력 있는 코드를 작성할 수 있도록 더 긴 이름 대신 표준 수학 연산자와 상수를 사용할 수 있습니다. **스칼라 언어 설명서(The Scala Language Specification)** 는 이 연산자 기호를 `\u0020 - \u007F` 사이의 문자와 유니코드 `Sm[Symbol/Math]` 카테고리에서 대괄호와 마침표를 제외한 모든 문자로 정의합니다. 대괄호는 타입 매개변수화에 사용하도록 예약되어 있으며, 마침표는 객체의 필드와 메소드에 접근하기 위해 예약되어있습니다.

Scala 에 유효한 식별자를 만들기 위해 문자, 숫자, 기호를 조합하는 규칙은 다음과 같습니다.

1. A letter followed by zero or more letters and digits.
2. A letter followed by zero or more letters and digits, then an underscore (_), and then one or more of either letters and digits or operator characters.
3. One or more operator characters.
4. One or more of any character except a backquote, all enclosed in a pair of backquotes.

REPL 에서 이 명명 규칙을 시험해보겠습니다.

```scala
scala> val π = 3.14159 // 1
π: Double = 3.14159

scala> val $ = "USD currency symbol"
$: String = USD currency symbol

scala> val o_O = "Hmm"
o_O: String = Hmm

scala> val 50cent = "$0.50" // 2
<console>:1: error: Invalid literal number
 val 50cent = "$0.50"
 ^

scala> val a.b = 25 // 3
<console>:7: error: not found: value a
 val a.b = 25

scala> val `a.b` = 4 // 4
a.b: Int = 4
```

1. 특수 문자 $\pi$ 는 유효한 Scala 식별자다.
2. 변수명 `50cent` 는 숫자로 시작하기 때문에 사용 불가능하다.
3. 변수명 `a.b` 는 마침표가 연산자 기호가 아니기 때문에 사용 불가능하다.
4. 미적으로 좋지는 않지만 역인용 부호와 함께 사용하면 문제가 해결됩니다.

값과 변수명은 관례상 소문자로 시작하고 추가적인 단어는 대문자로 시작합니다. 이는 일반적으로 **낙타대문자(Camel Case)** 라 하며, Scala 개발자에게 권장되는 방식입니다.

## Types

Scala 에는 값과 변수를 정의할 때 사용하는 숫자 타입과 숫자가 아닌 타입이 있습니다. 이 핵심 타입은 컬렉션을 포함하여 다른 모든 타입의 기본 요소가 되며, 그 자체도 자신의 데이터에 동작하는 메소드와 연산자를 갖는 객체가 됩니다.

Java, C 와 달리 Scala 에는 원시 데이터 타입의 개념이 없습니다. JVM 은 원시 정수 타입인 int 와 정수 클래스 Integer 를 지원하는 반면, Scala 는 정수 클래스인 Int 만 지원합니다.

### Numeric Data Types

아래 표는 Scala 의 숫자형 데이터 타입을 나타냅니다.

|Name|Description|Size|Min|Max|
|:--|:--|:--|:--|:--|
|Byte|Signed Integer|1 byte|-127|128|
|Short|Signed Integer|2 bytes|-32768|32767|
|Int|Signed Integer|4 bytes|$-2^{31}$|$2^{31}-1$|
|Long|Signed Integer|8 bytes|$-2^{63}$|$2^{63}-1$|
|Float|Signed Floating Point|4 bytes|n/a|n/a|
|Double|Signed Floating Point|8 bytes|n/a|n/a|

Scala 는 타입 순위에 기반하여 한 타입의 숫자를 자동으로 다른 타입으로 전환해줍니다. 위 표의 숫자 타입은 이 자동 전환 순위대로 정렬한 것으로, Byte 타입이 최하위에 있어 다른 모든 타입으로 전환될 수 있습니다.

이제 서로 다른 타입의 값을 생성하고 자동으로 그보다 높은 순위의 타입으로 전환해보겠습니다.

```scala
scala> val b: Byte = 10
b: Byte = 10

scala> val s: Short = b
s: Short = 10

scala> val d: Double = s
d: Double = 10.0
```

여기에서 `b` 와 `s` 의 값은 더 높은 순위를 갖는 새로운 값에 할당되며, 자동으로 더 높은 순위로 전환됩니다.

Scala 는 높은 순위의 데이터 타입이 더 낮은 순위의 타입으로 자동 전환되는 것을 허용하지 않습니다. 이는 더 적은 저장 공간을 가지는 타입으로 전환하면 데이터 손실이 일어나게 된다는 사실로도 충분히 이해할 수 있습니다. 

이번에는 높은 순위의 타입에서 낮은 순위의 타입으로 자동 전환하는걸 해보겠습니다.

```scala
scala> val l: Long = 20
l: Long = 20

scala> val i: Int = l
<console>:8: error: type mismatch;
 found : Long
 required: Int
    val i: Int = l
```

에러가 발생합니다. 하지만 모든 숫자 타입에 적용할 수 있는 `to<Type>` 메소드를 이용하여 수동으로 타입 전환을 할 수 있습니다. 이때 더 하위 순위의 타입으로 전환함으로써 데이터를 잃을 수도 있지만, 해당 데이터가 더 낮은 순위의 타입과 호환이 가능하다는 점을 알고 있을 때는 유용합니다.

아래 예에서 `Long` 값은 `toInt` 메소드를 이용하여 안전하게 `Int` 타입으로 전환될 수 있는데, 그 데이터가 `Int` 의 저장 공간 범위 내에 있기 때문입니다.

```scala
scala> val l: Long = 20
l: Long = 20

scala> val i: Int = l.toInt
i: Int = 20
```

명시적 타입의 대안으로 리터럴 타입을 위한 Scala 표기 법을 사용하여 리터럴 데이터의 타입을 직접 지정할 수 있습니다. 리터럴 타입을 지정하는 전체 표기법을 아래 표에 정리했습니다.

|Literal|Type|Description|
|:--|:--|:--|
|5|Int|접두사 / 접미사 없는 리터럴은 기본적으로 Int 다.|
|0x0f|Int|접두사 `0x` 는 16 진수 표기법을 의미한다.|
|5l|Long|접미사 `l` 은 Long 타입을 의미한다.|
|5.0|Double|접두사 / 접미사 없는 소수 리터럴은 기본 DOuble 형이다.|
|5f|Float|`f` 접미사는 Float 타입을 나타낸다.|
|5d|Double|`d` 접미사는 Double 타입을 나타낸다.|

리터럴을 시험해보기 위해 타입을 기술하지 않고 새로운 값을 할당해보겠습니다. Scala REPL 은 각 값의 적절한 타입을 추정하기 위해 타입 추론을 사용할 것입니다.

```scala
scala> val anInt = 5
anInt: Int = 5

scala> val yellowRgb = 0xffff00
yellowRgb: Int = 16776960

scala> val id = 100l
id: Long = 100

scala> val pi = 3.1416
pi: Double = 3.1416
```

### Strings

String 타입은 모든 프로그래밍 언어에서 가장 일반적인 핵심 타입 중 하나로, 텍스트의 문자열을 나타냅니다. Scala 의 String 은 Java 의 String 을 기반으로 하며, 여러 줄 리터럴과 문자열 보간 같은 고유의 특징을 추가했습니다.

큰따옴표 및 역슬래시와 함께 이스케이프 문자를 사용하여 String 리터럴을 작성하겠습니다.

```scala
scala> val hello = "Hello There"
hello: String = Hello There

scala> val signature = "With Regards, \nYour friend"
signature: String =
With Regards,
Your friend
```

숫자 타입과 마찬가지로 String 타입은 수학 연산자 사용을 지원합니다. 예를 들어, 2 개의 String 값을 비교하기 위해 등호 연산자(==) 를 사용합니다. Java 와 달리 등호 연산자(==) 는 객체 참조가 같은지를 검사하는 것이 아니라 실제 두 값이 같은지를 검사합니다.

```scala
scala> val greeting = "Hello, " + "World"
greeting: String = Hello, World

scala> val matched = (greeting == "Hello, World")
matched: Boolean = true

scala> val theme = "Na " * 16 + "Batman!" // what do you expect this to print?
```

여러 줄의 String 은 큰 따옴표 3 개를 이용하여 생성합니다. 여러 줄의 문자열은 리터럴이며, 따라서 특수 문자의 시작을 나타내는 역슬래시를 인지하지 못합니다.

```scala
scala> val greeting = """She suggested reformatting the file
 | by replacing tabs (\t) with newlines (\n);
 | "Why do that?", he asked. """
greeting: String =
She suggested reformatting the file
by replacing tabs (\t) with newlines (\n);
"Why do that?", he asked.
```

**String Interpolation**

문자열 추가를 이용하여 다른 값을 기반으로 String 을 만드는 것은 상당히 쉽습니다. 아래에서는 Float 값의 앞 뒤로 텍스트를 추가하여 만드는 String 을 보여줍니다.

```scala
scala> val approx = 355/113f
approx: Float = 3.141593

scala> println("Pi, using 355/113, is about " + approx + "." )
Pi, using 355/113, is about 3.141593.
```

값 또는 변수를 String 내에 결합시키는 보다 직접적인 방식은 외부 값과 변수명을 인식하고 해석하는 특수 모드인 **문자열 보간(String Interpolation)** 을 사용합니다. Scala 에서 문자열 보간은 문자열의 첫 큰따옴표 전에 접두사 `s` 를 추가하여 표기합니다. 다음, 달러 기호($) 로 외부 데이터에 대한 참조임을 표시합니다.

앞의 예제를 다시 문자열 보간법을 이용해 작성해보면 다음과 같습니다.

```scala
scala> println(s"Pi, using 355/113, is about $approx." )
Pi, using 355/113, is about 3.141593.
```

참조하는 내용에 단어가 아닌 문자가 있다거나 참조 내용이 그것을 둘러싼 텍스트와 구분되지 않으면, 선택적으로 중괄호를 사용할 수 있습니다.

```scala
scala> val item = "apple"
item: String = apple

scala> s"How do you like them ${item}s?"
res0: String = How do you like them apples?

scala> s"Fish n chips n vinegar, ${"pepper "*3}salt"
res1: String = Fish n chips n vinegar, pepper pepper pepper salt
```

문자열 보간의 또 다른 포맷은 `printf` 표기법을 사용하는 것으로 문자 개수를 세거나 소수점 표시와 같은 데이터 서식을 제어하고자 할 때 매우 유용합니다. `printf` 표기법에서는 접두사를 `f` 로 바꾸고, 참조 바로 뒤에 `printf` 표기법을 써줍니다.

```scala
scala> val item = "apple"
item: String = apple

scala> f"I wrote a new $item%.3s today"
res2: String = I wrote a new app today

scala> f"Enjoying this $item ${355/113.0}%.5f times today"
res3: String = Enjoying this apple 3.14159 times today
```

이 `printf` 표기 법은 이전 예제에 비해 참조 읽기를 다소 어렵게 하지만, 출력을 근본적으로 제어할 수 있는 장점이 있습니다.

**Regular Expression**

정규표현식은 검색 패턴을 나타내는 문자와 구두점으로 이루어진 문자열입니다.

String 타입은 정규 표현식을 지원하는 다양한 내장 연산을 제공합니다. 아래 표는 연산 중 일부를 엄선하여 정리하였습니다.

|Name|Example|Description|
|:--|:--|:--|
|matches|"Froggy went a' courting" matches ".* courting"|정규 표현식이 전체 문자열과 맞으면 참을 반환|
|replaceAll|"milk, tea, muck" replaceAll ("m[^ ]+k", "coffee")|일치하는 문자열을 모두 치환 텍스트로 치환함|
|replaceFirst|"milk, tea, muck" replaceFirst ("m[^ ]+k", "coffee")|첫 번째로 일치하는 문자열을 치환 텍스트로 치환함|

정규 표현식의 고급 처리 기법을 위해서는 `r` 연산자를 호출하여 정규 표현식 타입으로 전환하면 됩니다. 이는 캡처 그룹을 지원하는 것과 함께 추가적인 검색 / 치환 연산을 처리할 수 있는 `Regex` 인스턴스를 반환합니다. **캡처 그룹(capture group)** 은 정규 표현식 패턴을 기반으로 주어진 문자열에서 항목을 선택하고 이를 로컬 값으로 전환할 수 있게 해줍니다.

패턴은 최소 하나의 괄호로 정의된 캡처 그룹을 포함해야만 하며, 입력값은 값을 반환할 최소 하나의 캡처된 패턴을 포함해야합니다.

**Syntax: Capturing Values with Regular Expressions**

```scala
val <Regex value>(<identifier>) = <input string>
```

정규 표현식 패턴을 지정하기 위해 여러 줄 문자열을 사용했습니다. 이는 리터럴로 역슬래시를 인식하기 위해 두 번째 역슬래시가 없어도 되게 해줍니다.

```scala
scala> val input = "Enjoying this apple 3.14159 times today"
input: String = Enjoying this apple 3.14159 times today

scala> val pattern = """.* apple ([\d.]+) times .*""".r // 1
pattern: scala.util.matching.Regex = .* apple ([\d.]+) times .* // 2

scala> val pattern(amountText) = input // 3
amountText: String = 3.14159

scala> val amount = amountText.toDouble // 4
amount: Double = 3.14159
```

1. 캡처 그룹은 단어 `apple` 과 `times` 사이에 있는 일련의 숫자와 점으로 이루어진 문자열이다. 여기서는 정규 표현식을 얻기 위해 `StringOps` 의 `r` 메소드를 사용한다.
2. 전체 정규 표현식 타입은 `scala.util.matching.Regex` 또는 `util.matching.Regex` 이다.
3. 포맷은 확실히 특이하다. 캡처 그룹 매치를 포함하는 새로운 값의 이름인 `amountText` 는 `val` 식별자 뒤에 바로 따라나오지 않는다.
4. 텍스트 형태의 숫자를 `Double` 로 전환하여 숫자 값을 얻는다.

정규 표현식은 매칭, 치환, 캡처와 같은 연산을 이용하여 간결하고 효과적으로 텍스트를 처리하는 방법이다.

### An Overview of Scala Types

숫자, 문자열 외 Scala 핵심 타입에 대해 더 살펴보겠습니다. 모든 Scala 타입은 숫자에서 문자열 그리고 컬렉션에 이르기까지 타입 계층 구조의 일부로 존재합니다. 아래 `Example 1` 을 확인하면 Scala 의 핵심 타입과 계층 구조를 알 수 있습니다.

> Example 1 - The Scala type hierarchy

![image](https://user-images.githubusercontent.com/44635266/75152476-72994600-574c-11ea-8ea0-ccd557739410.png)

화살표는 슈퍼타입을 가리킵니다. 위 다이어그램에서 언급한 타입들을 설명과 함께 아래 표에 정리해보겠습니다.

|Name|Description|Instantiable|
|:--|:--|:--|
|Any|Scala 에서 모든 타입의 루트|X|
|AnyVal|모든 값 타입의 루트|X|
|AntRef|모든 참조 타입의 루트|X|
|Nothing|모든 타입의 하위 클래스|X|
|Null|Null 값을 의미하는 모든 AnyRef 타입의 하위 클래스|X|
|Char|유니코드 문자|O|
|Boolean|True 또는 False|O|
|String|문자열열|O|
|Unit|값이 없음을 나타냄|X|

Any, AnyVal, AnyRef 타입은 Scala 타입 계층 구조의 루트입니다. Any 는 절대루트입니다. AnyVal 을 확장한 타입은 데이터를 표현하는 데 사용하는 핵심 값들이기 때문에 **값 타입(value type)** 이라 합니다. 여기에는 우리가 다루었던 숫자 타입과 함께 Char, Boolean, Unit 이 포함됩니다. AnyVal 타입은 다른 타입들과 마찬가지로 접근되지만, 객체로 힙 메모리에 할당되거나 JVM 기본값으로 스택에 지역적으로 할당됩니다. 값 타입 이외의 모든 타입들 AnyRef 가 루트이며, 오직 객체로 힙 메모리에만 할당됩니다. AnyRef 의 Ref 라는 용어는 메모리 참조를 통해 접근되는 참조 타입임을 의미합니다.

Char 리터럴은 작은따옴표로 작성되어 큰따옴표로 작성되는 String 리터럴과 구분됩니다.

```scala
scala> val c = 'A'
c: Char = A

scala> val i: Int = c
i: Int = 65

scala> val t: Char = 116
t: Char = t
```

Boolean 타입은 true 와 false 값만을 가집니다. 그 외에도 비교와 부울 논리 연산자로부터 Boolean 값을 얻을 수 있습니다.

```scala
scala> val isTrue = !true
isTrue: Boolean = false

scala> val isFalse = !true
isFalse: Boolean = false

scala> val unequal = (5 != 6)
unequal: Boolean = true

scala> val isLess = (5 < 6)
isLess: Boolean = true

scala> val unequalAndLess = unequal & isLess
unequalAndLess: Boolean = true

scala> val definitelyFalse = false && unequal
definitelyFalse: Boolean = false
```

다른 동적 언어들과는 달리 Scala 는 다른 타입을 부울 타입으로 자동 전환해주지 않습니다. 숫자 0 은 false 와 다릅니다. 값의 상태를 부울타입으로 평가하려면 명시적으로 비교해야 합니다.

```scala
scala> val zero = 0
zero: Int = 0

scala> val isValid = zero > 0
isValid: Boolean = false
```

Unit 타입은 데이터 타입을 나타내는 대신 데이터가 없음을 나타냅니다. 다른 언어에서 사용하는 키워드 void 와 유사합니다. Scala 에서는 어떤 것도 반환하지 앟는 함수나 표현식의 반환 타입으로 쓰입니다.

Unit 리터럴은 빈 괄호 () 로 값이 없음을 나타냅니다. 원한다면 Unit 타입으로 값이나 변수를 정의할 수 있지만, 가장 보편적인 용도는 함수와 표현식을 정의하는데 있습니다.

```scala
scala> val nada = ()
nada: Unit = ()
```

**Type operations**

아래 표는 Scala 의 모든 타입에서 사용 가능한 연산을 보여줍니다. 모든 JVM 인스턴스에서는 `toString` 과 `hashCode` 메소드가 필요합니다.

|Name|Example|Description|
|:--|:--|:--|
|asInstanceOf[<Type>]|5.asInstanceOf[Long]|해당 값을 원하는 타입으 ㅣ값으로 전환, 그 값이 새로운 타입과 호환되지 않으면 에러 발생|
|getClass|(7.0 / 5).getClass|해당 값의 타입 반환|
|isInstanceOf|(5.0).isInstanceOf[Float]|해당 값이 주어진 타입을 가지면 true 반환|
|hashCode|"A".hashCode|해당 값의 해시코드를 반환, 해시 기반 컬렉션에 유용함|
|to<Type>|20.toByte; 47.toFloat|하나의 값을 호환되는 값으로 바꿔주는 전환 함수|
|toString|(3.0 / 4.0).toString|해당 값을 String 으로 전환|

지금가지 본 모든 타입은 단일 요소를 나타내는 **스칼라(scalar)** 값 입니다. 이 스칼라 값의 보완책으로 둘 이상의 값을 새로운, 순서가 있는 단일 요소로 수집하는 Tuple 타입을 살펴보겠습니다.

### Tuples

**튜플(Tuple)** 은 둘 이상의 값을 가지는 순서가 있는 컨테이너로, 여기에 포함된 각각의 값은 서로 다른 타입을 가질 수 있습니다. 테이블의 단일 행을 튜플로 간주하는 관계형 데이터베이스로 작업해본 경험이 있다면 이 용어가 익숙할 것입니다.

튜플은 리스트와 배열과는 달리 튜플의 요소들을 반복할 수 없습니다. 튜플은 단지 하나 이상의 값을 담기 위한 컨테이너입니다.

튜플을 만들려면 괄호 안에 각 값을 쉼표로 분리하여 나열하면 됩니다.

```scala
( <value 1>, <value 2>[, <value 3>...] )
```

예를 들어, Int, String, Boolean 값을 가지는 튜플을 만들어보면 다음과 같습니다.

```scala
scala> val info = (5, "Korben", true)
info: (Int, String, Boolean) = (5,Korben,true)
```

튜플의 각 항목은 1 부터 시작하는 인덱스를 이용하여 접근할 수 있습니다.

```scala
scala> val name = info._2
name: String = Korben
```

2 개의 항목을 가지는 튜플을 생성하는 다른 형식으로는 화살표 연산자(->) 를 사용하는 방식이 있습니다. 이 방식은 튜플에서 Key - Value 쌍을 표현하는 가장 보편적인 방법입니다.

```scala
scala> val red = "red" -> "0xff0000"
red: (String, String) = (red,0xff0000)

scala> val reversed = red._2 -> red._1
reversed: (String, String) = (0xff0000,red)
```


