---
title:  "Python 3.6의 새로운 기능"
excerpt: "Python 3.6의 새로운 기능"
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

Python 3.6 버전이 2016년 12월 23일에 Release 되었습니다.

추가된 기능에 대해서 알아보겠습니다.

[What’s New In Python 3.6](https://docs.python.org/3/whatsnew/3.6.html)를 참고했습니다.

## 1. New Features

### 1.1. PEP 498: Formatted string literals

[PEP 498](https://www.python.org/dev/peps/pep-0498/)은 새로운 종류의 문자열 리터럴 f-문자열(f-strings), 또는 **포맷 문자열 리터럴** 을 도입합니다.

포맷 문자열 리터럴은 `f`를 접두어로 사용하고 `str.format()`에서 허용하는 포맷 문자열과 유사합니다. 중괄호로 둘러싸인 치환 필드가 포함됩니다. 치환 필드는 실행 시간에 평가된 다음 `format()` 프로토콜을 사용하여 포맷되는 표현식입니다:

```python
>>> name = "Fred"
>>> f"He said his name is {name}."
'He said his name is Fred.'
>>> width = 10
>>> precision = 4
>>> value = decimal.Decimal("12.34567")
>>> f"result: {value:{width}.{precision}}"  # nested fields
'result:      12.35'
```

### 1.2. PEP 526: Syntax for variable annotations

[PEP 484](https://www.python.org/dev/peps/pep-0484/)는 함수 매개 변수의 형 어노테이션, 일명 형 힌트에 대한 표준을 도입했습니다. 이 PEP는 클래스 변수와 인스턴스 변수를 포함한 변수 형에 어노테이트하기 위해 파이썬에 구문을 추가합니다:

```python
primes: List[int] = []

captain: str  # Note: no initial value!

class Starship:
    stats: Dict[str, int] = {}
```

함수 어노테이션과 마찬가지로, 파이썬 인터프리터는 변수 어노테이션에 특별한 의미를 부여하지 않고 클래스나 모듈의 `__annotations__` 어트리뷰트에 저장하기만 합니다.

정적으로 타이핑된 언어의 변수 선언과 달리, 어노테이션 문법의 목표는 추상 구문 트리와 `__annotations__` 어트리뷰트를 통해 제삼자 도구와 라이브러리를 위해 구조화된 형 메타 데이터를 쉽게 지정할 방법을 제공하는 것입니다.

### 1.3. PEP 515: Underscores in Numeric Literals

[PEP 515](https://www.python.org/dev/peps/pep-0515/)는 가독성을 높이기 위해 숫자 리터럴에 밑줄을 사용하는 기능을 추가합니다. 예를 들면:

```python
>>> 1_000_000_000_000_000
1000000000000000
>>> 0x_FF_FF_FF_FF
4294967295
```

숫자 사이와 진수 지정자(base specifier) 뒤에 단일 밑줄이 허용됩니다. 선행, 후행 또는 여러 밑줄이 연속해서 나오는 것은 허용되지 않습니다.

문자열 포매팅 언어는 이제 부동 소수점 표시형과 정수 표시형 `d`에 대해 천 단위 구분자에 밑줄 사용을 알리는 `_` 옵션을 지원합니다. 정수 표시형 `b`, `o`, `x` 및 `X`의 경우, 밑줄이 4자리마다 삽입됩니다:

```python
>>> '{:_}'.format(1000000)
'1_000_000'
>>> '{:_x}'.format(0xFFFFFFFF)
'ffff_ffff'
```

### 1.4. PEP 525: Asynchronous Generators

[PEP 492](https://www.python.org/dev/peps/pep-0492/)는 파이썬 3.5에 네이티브 코루틴과 `async` / `await` 구문에 대한 지원을 도입했습니다. 파이썬 3.5 구현의 주목할만한 제한은 같은 함수 본문에서 `await`와 `yield`를 사용할 수 없다는 것입니다. 파이썬 3.6에서는 이 제한이 해제되어 *비동기 제너레이터(asynchronous generators)*를 정의할 수 있습니다:

```python
async def ticker(delay, to):
    """Yield numbers from 0 to *to* every *delay* seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)
```

새로운 문법은 더 빠르고 간결한 코드를 허용합니다.

### 1.5. PEP 530: Asynchronous Comprehensions

[PEP 530](https://www.python.org/dev/peps/pep-0530/) 은 리스트, 집합, 딕셔너리 컴프리헨션과 제너레이터 표현식에서 `async for` 사용에 대한 지원을 추가합니다:

```python
result = [i async for i in aiter() if i % 2]
```

또한, `await` 표현식은 모든 종류의 컴프리헨션에서 지원됩니다:

```python
result = [await fun() for fun in funcs if await condition()]
```

### 1.6. PEP 487: Simpler customization of class creation

이제 메타 클래스를 사용하지 않고도 서브클래스 생성을 사용자 정의할 수 있습니다. 새로운 서브클래스가 만들어질 때마다 새로운 `__init_subclass__` 클래스 메서드가 베이스 클래스에서 호출됩니다:

```python
class PluginBase:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

class Plugin1(PluginBase):
    pass

class Plugin2(PluginBase):
    pass
```

인자가 없는 `super()` 호출이 `__init_subclass__()` 구현에서 올바르게 작동하도록 하기 위해, 사용자 정의 메타 클래스에서 새 `__classcell__` 이름 공간 항목이 `type.__new__`로 전파되도록 해야 합니다.

### 1.7. PEP 487: Descriptor Protocol Enhancements

[PEP 487](https://www.python.org/dev/peps/pep-0487/)은 새로운 선택적 `__set_name__()` 메서드를 포함하도록 디스크립터 프로토콜을 확장합니다. 새 클래스가 정의될 때마다, 정의에 포함된 모든 디스크립터에 대해 새 메서드가 호출되어, 정의되는 클래스에 대한 참조와 클래스 이름 공간 내에서 디스크립터에 지정된 이름을 제공합니다. 즉, 디스크립터의 인스턴스는 이제 소유자 클래스에 있는 디스크립터의 어트리뷰트 이름을 알 수 있습니다:

```python
class IntField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f'expecting integer in {self.name}')
        instance.__dict__[self.name] = value

    # this is the new initializer:
    def __set_name__(self, owner, name):
        self.name = name

class Model:
    int_field = IntField()
```

### 1.8. PEP 519: Adding a file system path protocol

파일 시스템 경로는 역사적으로 `str`이나 `bytes` 객체로 표현되었습니다. 이로 인해 파일 시스템 경로에서 작동하는 코드를 작성하는 사람들은 이러한 객체가 두 형 중 하나일 뿐이라고 가정합니다 (파일 기술자를 나타내는 `int`는 파일 경로가 아니기 때문에 고려하지 않습니다). 불행히도 이러한 가정은 `pathlib`와 같은 파일 시스템 경로의 대체 객체 표현이 파이썬의 표준 라이브러리를 포함하여 기존 코드와 함께 작동하지 못하게 합니다.

이 상황을 해결하기 위해, `os.PathLike`으로 표현되는 새 인터페이스가 정의되었습니다. `__fspath__()` 메서드를 구현하면, 객체가 경로를 나타낸다는 신호를 보내는 것입니다. 그런 다음 객체는 파일 시스템 경로의 저수준 표현을 `str`이나 `bytes` 객체로 제공할 수 있습니다. 이것은 `os.PathLike`을 구현하거나 파일 시스템 경로를 나타내는 `str`나 `bytes` 객체면 객체를 경로류로 간주함을 뜻합니다. 코드는 `os.fspath()`, `os.fsdecode()` 또는 `os.fsencode()`를 사용하여 경로류 객체의 `str` 및/또는 `bytes` 표현을 명시적으로 얻을 수 있습니다.

내장 `open()` 함수는 `os`와 `os.path` 모듈의 모든 관련 함수와 표준 라이브러리의 대부분의 다른 함수와 클래스와 마찬가지로, os.PathLike 객체를 받아들이도록 갱신되었습니다. `os.DirEntry` 클래스와 `pathlib`의 관련 클래스도 `os.PathLike`을 구현하도록 갱신되었습니다.

기대하는 것은 파일 시스템 경로에서 작동하는 기반 함수들을 갱신하면 코드 변경 없이, 혹은 최소한의 변경만으로도 (예를 들어 경로류 객체에 대한 연산 전에 코드 시작 부분에서 `os.fspath()`를 호출하기), 제삼자 코드가 모든 경로류 객체를 묵시적으로 지원하게 되는 것입니다.

다음은 새 인터페이스를 사용하여 `pathlib.Path`를 기존 코드로보다 쉽고 투명하게 사용할 수 있는 방법에 대한 몇 가지 예입니다:

```python
>>> import pathlib
>>> with open(pathlib.Path("README")) as f:
...     contents = f.read()
...
>>> import os.path
>>> os.path.splitext(pathlib.Path("some_file.txt"))
('some_file', '.txt')
>>> os.path.join("/a/b", pathlib.Path("c"))
'/a/b/c'
>>> import os
>>> os.fspath(pathlib.Path("some_file.txt"))
'some_file.txt'
```

### 1.9. PEP 495: Local Time Disambiguation

대부분의 세계 위치에서, 현지 시계가 뒤로 이동하는 시간이 있었고 앞으로도 있을 것입니다. 이 시간에는, 현지 시계가 같은 날에 같은 시간을 두 번 표시하는 간격이 도입되었습니다. 이러한 상황에서, 현지 시계에 표시되는 (또는 파이썬 `datetime` 인스턴스에 저장된) 정보는 특정 시점을 식별하기에 충분하지 않습니다.

[PEP 495](https://www.python.org/dev/peps/pep-0495/)는 `datetime.datetime`과 `datetime.time` 클래스의 인스턴스에 새로운 `fold` 어트리뷰트를 추가하여 현지 시간이 같은 두 순간을 구별합니다:

```python
>>> u0 = datetime(2016, 11, 6, 4, tzinfo=timezone.utc)
>>> for i in range(4):
...     u = u0 + i*HOUR
...     t = u.astimezone(Eastern)
...     print(u.time(), 'UTC =', t.time(), t.tzname(), t.fold)
...
04:00:00 UTC = 00:00:00 EDT 0
05:00:00 UTC = 01:00:00 EDT 0
06:00:00 UTC = 01:00:00 EST 1
07:00:00 UTC = 02:00:00 EST 0
```

`fold` 어트리뷰트의 값은 모호한 경우의 두 번째 (시간순으로) 순간을 나타내는 인스턴스를 제외한 모든 인스턴스에 대해 0 값을 갖습니다.

### 1.10. PEP 529: Change Windows filesystem encoding to UTF-8

파일 시스템 경로를 나타내는 것은 `bytes`가 아닌 `str`(유니코드)로 수행하는 것이 가장 좋습니다. 그러나, `bytes` 사용이 충분하고 올바른 경우가 있습니다.

파이썬 3.6 이전에는, 윈도우에서 `bytes` 경로를 사용할 때 데이터 손실이 발생할 수 있습니다. 이 변경으로 인해, 이제 윈도우에서 `bytes`를 사용하여 경로를 나타내는 것이 지원됩니다. 단, 해당 `bytes`는 `sys.getfilesystemencoding()`에서 반환한 인코딩으로 인코딩되며, 현재 기본값은 `'utf-8'`입니다.

경로를 나타내기 위해 `str`을 사용하지 않는 응용 프로그램은 `os.fsencode()`와 `os.fsdecode()`를 사용하여 해당 `bytes`가 올바르게 인코딩되도록 해야 합니다. 이전 동작으로 되돌리려면, `PYTHONLEGACYWINDOWSFSENCODING`을 설정하거나 `sys._enablelegacywindowsfsencoding()`을 호출하십시오.

필요한 코드 수정에 대한 자세한 정보와 논의는 [PEP 529](https://www.python.org/dev/peps/pep-0529/)를 참조하십시오.

### 1.11. PEP 528: Change Windows console encoding to UTF-8

윈도우의 기본 콘솔은 이제 모든 유니코드 문자를 허용하고 파이썬 코드에 올바르게 읽힌 `str` 객체를 제공합니다. `sys.stdin`, `sys.stdout` 및 `sys.stderr`은 이제 `utf-8` 인코딩으로 기본 설정됩니다.

이 변경은 대화 형 콘솔을 사용할 때만 적용되며, 파일이나 파이프를 리디렉션 할 때는 적용되지 않습니다. 대화식 콘솔 사용 시에 이전 동작으로 되돌리려면, `PYTHONLEGACYWINDOWSSTDIO`를 설정하십시오.

### 1.12. PEP 520: Preserving Class Attribute Definition Order

클래스 정의 본문의 어트리뷰트는 자연스러운 순서를 갖습니다: 이름이 소스에 나타나는 것과 같은 순서. 이 순서는 이제 새 클래스의 `__dict__` 어트리뷰트에 유지됩니다.

또한, 유효한 기본 클래스 실행 이름 공간(`type.__prepare__()`에서 반환되는 것)은 이제 삽입 순서 보존 매핑입니다.

### 1.13. PEP 468: Preserving Keyword Argument Order

함수 서명의 `**kwargs`는 이제 삽입 순서 보존 매핑임이 보장됩니다.

### 1.14. New dict implementation

`dict` 형은 이제 PyPy에서 처음 구현된 Raymond Hettinger의 제안에 기반한 《compact》 표현을 사용합니다. 새로운 `dict()`의 메모리 사용량은 파이썬 3.5에 비해 20%에서 25% 더 적습니다.

### 1.15. PEP 523: Adding a frame evaluation API to CPython

파이썬은 코드 실행 방법을 사용자 정의하기 위한 광범위한 지원을 제공하지만, 빠진 한 가지는 프레임 객체를 평가하는 것입니다. 파이썬에서 프레임 평가를 가로채는 방법을 원한다면 정의된 함수에 대한 함수 포인터를 직접 조작하지 않고는 방법이 없었습니다.

[PEP 523](https://www.python.org/dev/peps/pep-0523/)은 프레임 평가를 C 수준에서 끼워 넣을 수 있도록 하는 API를 제공하여 이를 바꿉니다. 이를 통해 디버거와 JIT과 같은 도구가 파이썬 코드 실행이 시작되기 전에 프레임 평가를 가로챌 수 있습니다. 이를 통해 파이썬 코드의 대체 평가 구현, 추적 프레임 평가 등이 가능해집니다.

이 API는 제한된 C API의 일부가 아니며 이 API의 사용이 제한적일 것으로 기대하고, 매우 선별된 저수준 사용 사례에만 적용 가능함을 알리기 위해 비공개로 표시됩니다. API의 의미는 필요에 따라 파이썬과 함께 변경됩니다.

### 1.16. PYTHONMALLOC environment variable

새로운 `PYTHONMALLOC` 환경 변수를 사용하면 파이썬 메모리 할당자를 설정하고 디버그 훅을 설치할 수 있습니다.

이제 `PYTHONMALLOC=debug`를 사용하여 릴리스 모드로 컴파일된 파이썬의 파이썬 메모리 할당자에 디버그 훅을 설치할 수 있습니다. 디버그 훅의 효과:

* 새로 할당된 메모리는 `0xCB` 바이트로 채워집니다
* 해제된 메모리는 `0xDB` 바이트로 채워집니다
* 파이썬 메모리 할당자 API 위반을 감지합니다. 예를 들어, `PyMem_Malloc()`에 의해 할당된 메모리 블록에 대해 호출된 `PyObject_Free()`.
* 버퍼 시작 앞에 쓰기를 감지합니다 (버퍼 언더플로)
* 버퍼 끝 뒤에 쓰기를 감지합니다 (버퍼 오버플로)
* `PYMEM_DOMAIN_OBJ`(예: `PyObject_Malloc()`)와 `PYMEM_DOMAIN_MEM`(예: `PyMem_Malloc()`) 도메인의 할당자 함수가 호출될 때 GIL을 잡았는지 확인합니다.
 
GIL을 잡았는지 확인하는 것도 파이썬 3.6의 새로운 기능입니다.

파이썬 메모리 할당자에 대한 디버그 훅은 `PyMem_SetupDebugHooks()` 함수를 참조하십시오.

이제 `PYTHONMALLOC=malloc`을 사용해서 모든 파이썬 메모리 할당에 대해 C 라이브러리의 `malloc()` 할당자를 강제로 사용하게 할 수도 있습니다. 이것은 릴리스 모드로 컴파일된 파이썬에 Valgrind와 같은 외부 메모리 디버거를 사용할 때 유용합니다.

에러 시, 파이썬 메모리 할당자의 디버그 훅은 이제 `tracemalloc` 모듈을 사용하여 메모리 블록이 할당된 트레이스백을 가져옵니다.

`python3.6 -X tracemalloc=5`(트레이스에 5개 프레임을 저장합니다)를 사용하는 버퍼 오버플로로 인한 치명적인 에러의 예:

```python
Debug memory block at address p=0x7fbcd41666f8: API 'o'
    4 bytes originally requested
    The 7 pad bytes at p-7 are FORBIDDENBYTE, as expected.
    The 8 pad bytes at tail=0x7fbcd41666fc are not all FORBIDDENBYTE (0xfb):
        at tail+0: 0x02 *** OUCH
        at tail+1: 0xfb
        at tail+2: 0xfb
        at tail+3: 0xfb
        at tail+4: 0xfb
        at tail+5: 0xfb
        at tail+6: 0xfb
        at tail+7: 0xfb
    The block was made by call #1233329 to debug malloc/realloc.
    Data at p: 1a 2b 30 00

Memory block allocated at (most recent call first):
  File "test/test_bytes.py", line 323
  File "unittest/case.py", line 600
  File "unittest/case.py", line 648
  File "unittest/suite.py", line 122
  File "unittest/suite.py", line 84

Fatal Python error: bad trailing pad byte

Current thread 0x00007fbcdbd32700 (most recent call first):
  File "test/test_bytes.py", line 323 in test_hex
  File "unittest/case.py", line 600 in run
  File "unittest/case.py", line 648 in __call__
  File "unittest/suite.py", line 122 in run
  File "unittest/suite.py", line 84 in __call__
  File "unittest/suite.py", line 122 in run
  File "unittest/suite.py", line 84 in __call__
  ...
```

### 1.17. DTrace and SystemTap probing support

이제 파이썬은 인터프리터에서 다음 이벤트에 대한 정적 마커를 활성화하는 `--with-dtrace`로 빌드 할 수 있습니다:

* function call/return
* garbage collection started/finished
* line of code executed.

이것은 특정 디버그 build를 다시 컴파일하거나 응용 프로그램 별 프로파일링 / 디버깅 코드를 제공할 필요없이 프로덕션에서 실행중인 인터프리터를 계측하는 데 사용할 수 있습니다.

## 2. Summary – Release highlights

#### New syntax features:

* [PEP 498](https://www.python.org/dev/peps/pep-0498/), formatted string literals.
* [PEP 515](https://www.python.org/dev/peps/pep-0515/), underscores in numeric literals.
* [PEP 526](https://www.python.org/dev/peps/pep-0526/), syntax for variable annotations.
* [PEP 525](https://www.python.org/dev/peps/pep-0525/), asynchronous generators.
* [PEP 530](https://www.python.org/dev/peps/pep-0530/): asynchronous comprehensions.

#### New library modules:

* secrets: [PEP 506](https://www.python.org/dev/peps/pep-0506/) – Adding A Secrets Module To The Standard Library.

#### CPython implementation improvements:

* The dict type has been reimplemented to use a more compact representation based on a proposal by Raymond Hettinger and similar to the PyPy dict implementation. This resulted in dictionaries using 20% to 25% less memory when compared to Python 3.5.
* Customization of class creation has been simplified with the new protocol.
* The class attribute definition order is now preserved.The order of elements in `**kwargs` now corresponds to the order in which keyword arguments were passed to the function.
* DTrace and SystemTap probing support has been added.
* The new PYTHONMALLOC environment variable can now be used to debug the interpreter memory allocation and access errors.

#### Significant improvements in the standard library:

* The `asyncio` module has received new features, significant usability and performance improvements, and a fair amount of bug fixes. Starting with Python 3.6 the asyncio module is no longer provisional and its API is considered stable.
* A new file system path protocol has been implemented to support path-like objects. All standard library functions operating on paths have been updated to work with the new protocol.
* The `datetime` module has gained support for Local Time Disambiguation.
* The `typing` module received a number of improvements.
* The `tracemalloc` module has been significantly reworked and is now used to provide better output for `ResourceWarning` as well as provide better diagnostics for memory allocation errors. See the PYTHONMALLOC section for more information.

#### Security improvements:

* The new `secrets` module has been added to simplify the generation of cryptographically strong pseudo-random numbers suitable for managing secrets such as account authentication, tokens, and similar.
* On Linux, `os.urandom()` now blocks until the system urandom entropy pool is initialized to increase the security. See the PEP 524 for the rationale.
* The `hashlib` `and` ssl modules now support OpenSSL 1.1.0.
* The default settings and feature set of the `ssl` module have been improved.
* The `hashlib` module received support for the BLAKE2, SHA-3 and SHAKE hash algorithms and the `scrypt()` key derivation function.

#### Windows improvements:

* [PEP 528](https://www.python.org/dev/peps/pep-0528/) and [PEP 529](https://www.python.org/dev/peps/pep-0529/), Windows filesystem and console encoding changed to UTF-8.
* The py.exe launcher, when used interactively, no longer prefers Python 2 over Python 3 when the user doesn’t specify a version (via command line arguments or a config file). Handling of shebang lines remains unchanged - “python” refers to Python 2 in that case.
* python.exe and pythonw.exe have been marked as long-path aware, which means that the 260 character path limit may no longer apply. See removing the MAX_PATH limitation for details.
* A ._pth file can be added to force isolated mode and fully specify all search paths to avoid registry and environment lookup. See the documentation for more information.
* A python36.zip file now works as a landmark to infer PYTHONHOME. See the documentation for more information.

