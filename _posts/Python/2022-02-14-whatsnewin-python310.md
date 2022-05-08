---
title:  "Python 3.10의 새로운 기능"
excerpt: "Python 3.10의 새로운 기능"
categories:
  - Programming
tags:
  - Programming
  - Python
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

Python 3.10 버전이 2022년 1월 11일에 Release 되었습니다.

추가된 기능에 대해서 알아보겠습니다.

[What’s New In Python 3.10](https://docs.python.org/3/whatsnew/3.10.html)를 참고했습니다.

## 1. New Features

### 1.1. Parenthesized context managers

이제 컨텍스트 관리자에서 여러 줄에 걸쳐서 둘러싸는 괄호를 사용할 수 있습니다. 이를 통해 이전에 `import` 문으로 가능했던 것과 유사한 방식으로 여러 줄로 된 컨텍스트 관리자의 긴 컬렉션을 형식화할 수 있습니다. 예를 들어 아래 유형 모두가 가능합니다.

```python
with (CtxManager() as example):
    ...

with (
    CtxManager1(),
    CtxManager2()
):
    ...

with (CtxManager1() as example,
      CtxManager2()):
    ...

with (CtxManager1(),
      CtxManager2() as example):
    ...

with (
    CtxManager1() as example1,
    CtxManager2() as example2
):
    ...
```

끝에 쉼표도 사용할 수 있습니다.

```python
with (
    CtxManager1() as example1,
    CtxManager2() as example2,
    CtxManager3() as example3,
):
    ...
```

이 새 구문은 새로운 파서의 비 LL(1) 용량을 사용합니다. 자세한 내용은 PEP 617을 확인하십시오.

### 1.2. Better error messages

**SyntaxErrors**

닫히지 않은 괄호 또는 대괄호가 포함된 코드를 구문 분석할 때 *SyntaxError: unexpected EOF while parsing*를 표시하는 대신 닫히지 않은 괄호 위치를 인터프리터에 포함합니다. 예를 들어, 다음 코드를 생각해 보십시오(닫히지 않은 '{'에 주목하십시오).

```python
expected = {9: 1, 18: 2, 19: 2, 27: 3, 28: 3, 29: 3, 36: 4, 37: 4,
            38: 4, 39: 4, 45: 5, 46: 5, 47: 5, 48: 5, 49: 5, 54: 6,
some_other_code = foo()
```

이전 버전의 인터프리터는 구문 오류의 위치로 혼동되는 위치를 보고했습니다.

```python
File "example.py", line 3
    some_other_code = foo()
                    ^
SyntaxError: invalid syntax
```

그러나 Python 3.10에서는 더 많은 오류 정보를 제공합니다.

```python
File "example.py", line 1
    expected = {9: 1, 18: 2, 19: 2, 27: 3, 28: 3, 29: 3, 36: 4, 37: 4,
               ^
SyntaxError: '{' was never closed
```

마찬가지로, 닫히지 않은 문자열 리터럴(단일 및 삼중 따옴표)과 관련된 오류는 이제 EOF/EOL을 보고하는 대신 문자열의 시작을 가리킵니다.

이러한 개선 사항은 PyPy 인터프리터의 이전 작업에서 영감을 받았습니다.

인터프리터가 제기한 `SyntaxError` 예외는 이제 문제가 감지된 위치 대신 구문 오류 자체를 구성하는 식의 전체 오류 범위를 강조 표시합니다. (before Python 3.10):

```python
>>> foo(x, z for z in range(10), t, w)
  File "<stdin>", line 1
    foo(x, z for z in range(10), t, w)
           ^
SyntaxError: Generator expression must be parenthesized
```

이제 Python 3.10은 다음과 같이 예외를 표시합니다.

```python
>>> foo(x, z for z in range(10), t, w)
  File "<stdin>", line 1
    foo(x, z for z in range(10), t, w)
           ^^^^^^^^^^^^^^^^^^^^
SyntaxError: Generator expression must be parenthesized
```

상당량의 `SyntaxError` 예외에 대한 새로운 메시지가 통합되었습니다. 주목할 만한 사항들을 알아보겠습니다.

* Missing `:` before blocks:

```python
>>> if rocket.position > event_horizon
  File "<stdin>", line 1
    if rocket.position > event_horizon
                                      ^
SyntaxError: expected ':'
```

* Unparenthesised tuples in comprehensions targets:

```python
>>> {x,y for x,y in zip('abcd', '1234')}
  File "<stdin>", line 1
    {x,y for x,y in zip('abcd', '1234')}
     ^
SyntaxError: did you forget parentheses around the comprehension target?
```

* Missing commas in collection literals and between expressions:

```python
>>> items = {
... x: 1,
... y: 2
... z: 3,
  File "<stdin>", line 3
    y: 2
       ^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

* Multiple Exception types without parentheses:

```python
>>> try:
...     build_dyson_sphere()
... except NotEnoughScienceError, NotEnoughResourcesError:
  File "<stdin>", line 3
    except NotEnoughScienceError, NotEnoughResourcesError:
           ^
SyntaxError: multiple exception types must be parenthesized
```

* Missing `:` and values in dictionary literals:

```python
>>> values = {
... x: 1,
... y: 2,
... z:
... }
  File "<stdin>", line 4
    z:
     ^
SyntaxError: expression expected after dictionary key and ':'

>>> values = {x:1, y:2, z w:3}
  File "<stdin>", line 1
    values = {x:1, y:2, z w:3}
                        ^
SyntaxError: ':' expected after dictionary key
```

* `try` blocks without `except` or `finally` blocks:

```python
>>> try:
...     x = 2
... something = 3
  File "<stdin>", line 3
    something  = 3
    ^^^^^^^^^
SyntaxError: expected 'except' or 'finally' block
```

* Usage of `=` instead of `==` in comparisons:

```python
>>> if rocket.position = event_horizon:
  File "<stdin>", line 1
    if rocket.position = event_horizon:
                       ^
SyntaxError: cannot assign to attribute here. Maybe you meant '==' instead of '='?
```

* Usage of `*` in f-strings:

```python
>>> f"Black holes {*all_black_holes} and revelations"
  File "<stdin>", line 1
    (*all_black_holes)
     ^
SyntaxError: f-string: cannot use starred expression here
```

**IndentationErrors**

많은 `IndInditionError` 예외는 이제 구문의 위치를 포함하여 들여쓰기가 예상되는 블록 종류에 대한 더 많은 컨텍스트를 가지고 있습니다.

```python
>>> def foo():
...    if lel:
...    x = 2
  File "<stdin>", line 3
    x = 2
    ^
IndentationError: expected an indented block after 'if' statement in line 2
```

**AttributeErrors**

`AttributeError`를 출력할 때 `PyErr_Display()`는 예외가 발생한 객체와 비슷한 이름을 제안합니다.

```python
>>> collections.namedtoplo
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'collections' has no attribute 'namedtoplo'. Did you mean: namedtuple?
```

**NameErrors**

인터프리터가 발생시킨 `NameError`를 출력할 때 `PyErr_Display()`는 예외가 발생한 함수에서 유사한 변수 이름을 제안합니다

```python
>>> schwarzschild_black_hole = None
>>> schwarschild_black_hole
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'schwarschild_black_hole' is not defined. Did you mean: schwarzschild_black_hole?
```

### 1.3. PEP 626: Precise line numbers for debugging and other tools

PEP 626은 디버깅, 프로파일링 및 커버리지 도구를 위한 보다 정확하고 신뢰할 수 있는 라인 번호를 제공합니다. 올바른 라인 번호를 가진 추적 이벤트는 실행된 모든 코드 라인과 실행된 코드 라인에 대해서만 생성됩니다.

프레임 객체의 `f_lineno` 특성은 항상 예상되는 라인 번호를 포함합니다.

코드 객체의 `co_lnotab` 특성은 더 이상 사용되지 않으며 3.12에서 제거됩니다. 오프셋에서 라인 번호로 변환해야 하는 코드는 대신 새 `co_lines()` 방법을 사용해야 합니다.

### 1.4. PEP 634: Structural Pattern Matching

구조 패턴 매칭은 연관된 동작과 *match statement* 및 *case statement* 형태로 추가되었습니다. 패턴은 시퀀스, 매핑, 원시 데이터 타입 및 클래스 인스턴스로 구성됩니다. 패턴 매칭을 통해 프로그램은 복잡한 데이터 유형에서 정보를 추출하고, 데이터 구조를 분기하며, 다양한 데이터 형식을 기반으로 특정 작업을 적용할 수 있습니다.

**Syntax and operations**

패턴 매칭의 일반적인 문법은 다음과 같다.

```python
match subject:
    case <pattern_1>:
        <action_1>
    case <pattern_2>:
        <action_2>
    case <pattern_3>:
        <action_3>
    case _:
        <action_wildcard>
```

*match statement*는 식을 가져와서 그 값을 하나 이상의 대/소문자 블록으로 주어진 연속적인 패턴과 비교합니다. 특히 패턴 매칭은 다음을 통해 동작한다.

1. using data with type and shape (the `subject`)
2. evaluating the `subject` in the `match` statement
3. comparing the subject with each pattern in a case statement from top to bottom until a match is confirmed.
4. executing the action associated with the pattern of the confirmed match
5. If an exact match is not confirmed, the last case, a wildcard `_`, if provided, will be used as the matching case. If an exact match is not confirmed and a wildcard case does not exist, the entire match block is a no-op.

**Declarative approach**

독자들은 C, 자바, 자바스크립트(및 많은 다른 언어)에서 볼 수 있는 스위치 문과 제목(데이터 객체)을 리터럴(패턴)에 맞추는 간단한 예를 통해 패턴 매칭을 인지할 수 있다. 종종 객체/표현식과 리터럴을 포함하는 대/소문자문을 비교하는 데 스위치 문이 사용됩니다.

패턴 매칭의 더 강력한 예는 Scalar, Elixir 같은 언어에서 찾을 수 있다. 구조적 패턴 일치를 통해 접근 방식은 "선언적"이며 데이터가 일치할 수 있는 조건(패턴)을 명시적으로 명시한다.

중첩된 "만약" 문을 사용하여 구조 패턴 매칭과 유사한 것을 수행하는데 사용될 수 있다면, 이것은 "선언적" 접근법보다 명확하지 않다. 대신, "선언적" 접근법은 조건에 맞추기 위해 조건을 명시하고 그것의 명시적인 패턴을 통해 더 읽기 쉽다. 구조적 패턴 매칭은 변수를 사례문의 리터럴과 비교하는 가장 간단한 형태로 사용될 수 있지만 파이썬의 진정한 가치는 대상의 유형과 모양을 처리하는 데 있다.

**Simple pattern: match to a literal**

이 예제를 가장 간단한 형태의 패턴 매칭으로 보자: 값, 주제, 여러 리터럴, 패턴과 매칭된다. 아래의 예에서 `status`는 일치문의 제목입니다. 패턴은 리터럴이 요청 상태 코드를 나타내는 각각의 case statements 입니다. 조건과 관련된 작업은 일치 후 실행됩니다.

```python
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```

위의 함수가 418의 `status`를 전달하면 "I'm a teapot"가 반환된다. 위의 함수가 `status`로 500을 전달하면 `_`와 대/소문자 구분이 와일드카드로 일치하고 "Something is about the Internet"이 반환된다. 마지막 블록에 유의하십시오. 변수 이름 `_`는 와일드카드 역할을 하며 제목이 항상 일치하도록 합니다. `_`의 사용은 선택 사항입니다.

```python
case 401 | 403 | 404:
    return "Not allowed"
```

`|`("or")를 사용하여 여러 리터럴을 단일 패턴으로 결합할 수 있습니다.

**Behavior without the wildcard**

위의 예제를 마지막 블록을 제거하여 수정하면 다음과 같이 됩니다.

```python
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
```

대소문자 문에서 `_`를 사용하지 않으면 일치가 존재하지 않을 수 있습니다. 일치하는 항목이 없으면 동작하지 않습니다.. 예를 들어, 500의 `status`가 전달되면 no-op이 발생합니다.

**Patterns with a literal and variable**

패턴은 unpacked 하는것처럼 보일 수 있으며 패턴을 사용하여 변수를 바인딩할 수 있습니다. 이 예제에서 데이터 점은 x 좌표와 y 좌표로 unpacked 할 수 있습니다.

```python
# point is an (x, y) tuple
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
```

첫 번째 패턴은 `(0, 0)`이라는 두 개의 리터럴을 가지고 있으며, 위에 보이는 리터럴 패턴의 확장으로 생각할 수 있다. 다음 두 패턴은 리터럴과 변수를 결합하고 변수는 주제(`point`)의 값을 바인딩합니다. 네 번째 패턴은 두 값을 참조하며, 이는 개념적으로 압축 풀기 할당 `(x, y) = point`와 유사합니다.

**Patterns and classes**

클래스를 사용하여 데이터를 구조화하는 경우 패턴으로 클래스 이름 다음에 생성자를 닮은 인수 목록을 사용할 수 있습니다. 이 패턴은 클래스 속성을 다음과 같은 변수로 캡처할 수 있습니다.

```python
class Point:
    x: int
    y: int

def location(point):
    match point:
        case Point(x=0, y=0):
            print("Origin is the point's location.")
        case Point(x=0, y=y):
            print(f"Y={y} and the point is on the y-axis.")
        case Point(x=x, y=0):
            print(f"X={x} and the point is on the x-axis.")
        case Point():
            print("The point is located somewhere else on the plane.")
        case _:
            print("Not a point")
```

**Patterns with positional parameters**

속성에 대한 순서를 제공하는 일부 내장 클래스와 함께 위치 매개변수를 사용할 수 있다(예: dataclasses)를 사용하였다. 또한 클래스에서 `__match_args__` 특수 속성을 설정하여 패턴의 속성에 대한 특정 위치를 정의할 수 있습니다.("x", "y")로 설정되면 다음 패턴은 모두 동일합니다 (그리고 모두 `y` 속성을 `var` 변수에 바인딩 함).

```python
Point(1, var)
Point(1, y=var)
Point(x=1, y=var)
Point(y=var, x=1)
```

**Nested patterns**

패턴을 임의로 중첩할 수 있습니다.예를 들어, 데이터가 짧은 포인트 목록인 경우 다음과 같이 일치할 수 있습니다.

```python
match points:
    case []:
        print("No points in the list.")
    case [Point(0, 0)]:
        print("The origin is the only point in the list.")
    case [Point(x, y)]:
        print(f"A single point {x}, {y} is in the list.")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two points on the Y axis at {y1}, {y2} are in the list.")
    case _:
        print("Something else is found in the list.")
```

**Complex patterns and the wildcard**

이 점에서 예제는 마지막 case 문에서 `_`만 사용했습니다. 와일드카드는 `('error', code, _)`와 같이 더 복잡한 패턴으로 사용될 수 있다. 예를 들면 다음과 같다.

```python
match test_variable:
    case ('warning', code, 40):
        print("A warning has been received.")
    case ('error', code, _):
        print(f"An error {code} occurred.")
```

위의 경우 `test_variable`은 `('error', code, 100)` 및 `('error', code, 800)`와 일치합니다.

**Guard**

패턴에 `if` 절을 추가할 수 있습니다. 가드가 false이면 `match`는 다음 케이스 블록을 시도하기 위해 계속됩니다. 가드가 평가되기 전에 값 캡처가 발생합니다.

```python
match point:
    case Point(x, y) if x == y:
        print(f"The point is located on the diagonal Y=X at {x}.")
    case Point(x, y):
        print(f"Point is not on the diagonal.")
```

**Other Key Features**

몇 가지 다른 주요 기능

* unpacking assignments와 마찬가지로 tuple과 list 패턴은 정확히 같은 의미를 가지며 실제로 임의의 시퀀스와 일치합니다. 엄밀히 말하면 피사체는 시퀀스여야 합니다. 따라서 중요한 예외는 패턴이 반복자와 일치하지 않는다는 것입니다. 또한 일반적인 실수를 방지하기 위해 시퀀스 패턴이 문자열과 일치하지 않습니다.
* 시퀀스 패턴은 와일드 카드를 지원합니다 : `[x, y, * rest]` 및 `(x, y, * rest)`는 풀기 과제에서 와일드 카드와 유사하게 작동합니다. `*` 뒤의 이름은 `_`일 수도 있으므로 `(x, y, *_)`는 나머지 항목을 바인딩하지 않고 적어도 두 항목의 시퀀스를 일치시킵니다.
* 매핑 패턴 : `{"bandwidth": b, "latency": l}` 은 칙령에서 `"bandwidth"` 및 `"latency"` 값을 캡처합니다.시퀀스 패턴과 달리 여분의 키는 무시된다. 와일드카드 `**rest`도 지원된다.(그러나 `**_`는 중복되므로 허용되지 않습니다.)
* 서브 패턴은 `as` 키워드를 사용하여 캡처할 수 있습니다.

```python
case (Point(x1, y1), Point(x2, y2) as p2): ...
```

이것은 x1, y1, x2, y2를 `as` 절없이 예상하는 것처럼 바인딩하고 p2는 피사체의 두 번째 항목 전체에 바인딩합니다.

* 대부분의 리터럴은 평등에 의해 비교됩니다.그러나 싱글 톤 `True`, `False` 및 `None`은 동일성에 의해 비교됩니다.
* 명명 된 상수는 패턴에 사용될 수 있습니다.이러한 명명된 상수는 상수가 캡처 변수로 해석되지 않도록 점선 이름이어야 합니다.

```python
from enum import Enum
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
```

### 1.5. Optional `EncodingWarning` and `encoding="locale"` option

`TextIOWrapper`와 `open()`의 기본 인코딩은 플랫폼과 로캘에 따라 다릅니다. UTF-8은 대부분의 유닉스 플랫폼에서 사용되기 때문에 UTF-8 파일을 열 때 `encoding` 옵션을 생략한다(예:).JSON, YAML, TOML, Markdown)은 매우 흔한 버그이다. 예를 들면 다음과 같다.

```python
# BUG: "rb" mode or encoding="utf-8" should be used.
with open("data.json") as f:
    data = json.load(f)
```

이러한 유형의 버그를 찾으려면 옵션인 `EncodingWarning`이 추가됩니다. [`sys.flags.warn_default_encoding`](https://docs.python.org/3.10/library/sys.html#sys.flags)이 true이고 `locale-specific default encoding`이 사용될 때 방출됩니다.

`-X warning_default_encoding` 옵션과 `PYTHONWARNDEFAULTENCODING`이 추가되어 경고가 가능하다.

자세한 내용은 [Text Encoding](https://docs.python.org/3.10/library/io.html#io-text-encoding)을 참조하십시오.

## 2. New Features Related to Type Hints

### 2.1. PEP 604: New Type Union Operator

구문 `X | Y`를 가능하게하는 새로운 유형의 조합 연산자가 도입되었습니다. 이를 [`typing.Union`](https://docs.python.org/3.10/library/typing.html#typing.Union)이라 하며, 특히 type 힌트를 사용하는 대신 *type X 또는 type Y*를 표현하는보다 좋은 방법을 제공합니다.

이전 버전의 Python에서는 여러 유형의 인수를 허용하는 함수에 유형 힌트를 적용하기 위해 [`typing.Union`](https://docs.python.org/3.10/library/typing.html#typing.Union)이 사용되었습니다.

```python
def square(number: Union[int, float]) -> Union[int, float]:
    return number ** 2
```

유형 힌트는 이제보다 간결한 방식으로 작성할 수 있습니다.

```python
def square(number: int | float) -> int | float:
    return number ** 2
```

이 새로운 구문은 `isinstance()` 및 `issubclass()`에 대한 두 번째 인수로도 받아 들여집니다.

```python
>>>
>>> isinstance(1, int | str)
True
```

자세한 내용은 [Union Type](https://docs.python.org/3.10/library/stdtypes.html#types-union) 및 [PEP 604](https://www.python.org/dev/peps/pep-0604/)를 참조하십시오.

### 2.2. PEP 612: Parameter Specification Variables

[PEP 484](https://www.python.org/dev/peps/pep-0484/)'s `Callable`용 정적 타입 체커에 제공되는 정보를 개선하기 위한 두 가지 새로운 옵션이 [`typing`](https://docs.python.org/3.10/library/typing.html#module-typing) 모듈에 추가되었습니다.

첫 번째는 매개 변수 지정 변수입니다.이들은 호출 가능한 하나의 매개 변수 유형을 다른 호출 가능한 고차 함수 및 데코레이터에서 일반적으로 발견되는 패턴으로 전달하는 데 사용됩니다. 사용 예제는 [`typing.ParamSpec`](https://docs.python.org/3.10/library/typing.html#typing.ParamSpec)에서 찾을 수 있습니다. 이전에는 매개 변수 유형의 주석 종속성을 정확한 방식으로 입력하는 쉬운 방법이 없었습니다.

두 번째 옵션은 새로운 `Concatenate` 연산자입니다. 다른 호출 가능한 매개 변수를 추가하거나 제거하는 상위 호출 가능한 주석을 입력하기 위해 매개 변수 지정 변수와 함께 사용됩니다. 사용 예제는 [`typing.concatenate`](https://docs.python.org/3.10/library/typing.html#typing.Concatenate)에서 찾을 수 있습니다.

자세한 내용은 [`typing.Callable`](https://docs.python.org/3.10/library/typing.html#typing.Callable), [`typing.ParamSpec`](https://docs.python.org/3.10/library/typing.html#typing.ParamSpec), [`typing.Concatenate`](https://docs.python.org/3.10/library/typing.html#typing.Concatenate), [`typing.ParamSpecArgs`](https://docs.python.org/3.10/library/typing.html#typing.ParamSpecArgs), [`typing.ParamSpecKwargs`](https://docs.python.org/3.10/library/typing.html#typing.ParamSpecKwargs) 및 [PEP 612](https://www.python.org/dev/peps/pep-0612/)를 참조하십시오.

### 2.3. PEP 613: TypeAlias

[PEP 484](https://www.python.org/dev/peps/pep-0484/)는 유형 별칭의 개념을 도입했으며 최상위 수준의 주석이 없는 할당만 요구했습니다. 이러한 단순성으로 인해 유형 검사기는 유형 별칭과 일반 할당을 구별하기가 어려웠습니다. 특히 순방향 참조 또는 유효하지 않은 유형이 관련되어있는 경우 특히 그렇습니다. 비교하십시오 :

```python
StrCache = 'Cache[str]'  # a type alias
LOG_PREFIX = 'LOG[DEBUG]'  # a module constant
```

이제 [`typing`](https://docs.python.org/3.10/library/typing.html#module-typing) 모듈에는 유형 별칭을보다 명확하게 선언할 수 있는 특수 값 `TypeAlias`가 있습니다.

```python
StrCache: TypeAlias = 'Cache[str]'  # a type alias
LOG_PREFIX = 'LOG[DEBUG]'  # a module constant
```

자세한 내용은 [PEP 613](https://www.python.org/dev/peps/pep-0613/)을 참조하십시오.

### 2.4. PEP 647: User-Defined Type Guards

[`typing`](https://docs.python.org/3.10/library/typing.html#module-typing) 모듈에 `TypeGuard`가 추가되어 타이프 가드 기능에 주석을 달고, 타이프 협소화 시 정적 타입 체커에게 제공되는 정보를 개선하였다.자세한 내용은 `TypeGuard` 문서 및 [PEP 647](https://www.python.org/dev/peps/pep-0647/)을 참조하십시오.

## 3. Summary - Release Highlights

#### New syntax features:

* [PEP 634](https://www.python.org/dev/peps/pep-0634/), Structural Pattern Matching: Specification
* [PEP 635](https://www.python.org/dev/peps/pep-0635/), Structural Pattern Matching: Motivation and Rationale
* [PEP 636](https://www.python.org/dev/peps/pep-0636/), Structural Pattern Matching: Tutorial
* [bpo-12782](https://bugs.python.org/issue12782/), Parenthesized context managers are now officially allowed.

#### New features in the standard library:

* [PEP 618](https://www.python.org/dev/peps/pep-0618/), Add Optional Length-Checking To zip.

#### Interpreter improvements:

* [PEP 626](https://www.python.org/dev/peps/pep-0626/), Precise line numbers for debugging and other tools.

#### New typing features:

* [PEP 604](https://www.python.org/dev/peps/pep-0604/), Allow writing union types as X | Y
* [PEP 613](https://www.python.org/dev/peps/pep-0613/), Explicit Type Aliases
* [PEP 612](https://www.python.org/dev/peps/pep-0612/), Parameter Specification Variables
  
#### Important deprecations, removals or restrictions:

* [PEP 644](https://www.python.org/dev/peps/pep-0644/), Require OpenSSL 1.1.1 or newer
* [PEP 632](https://www.python.org/dev/peps/pep-0632/), Deprecate distutils module.
* [PEP 623](https://www.python.org/dev/peps/pep-0623/), Deprecate and prepare for the removal of the wstr member in PyUnicodeObject.
* [PEP 624](https://www.python.org/dev/peps/pep-0624/), Remove Py_UNICODE encoder APIs
* [PEP 597](https://www.python.org/dev/peps/pep-0597/), Add optional EncodingWarning

> 참고자료

* [What’s New In Python 3.10](https://docs.python.org/3/whatsnew/3.10.html)