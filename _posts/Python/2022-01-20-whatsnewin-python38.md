---
title:  "Python 3.8의 새로운 기능"
excerpt: "Python 3.8의 새로운 기능"
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

Python 3.8 버전이 2019년 10월 14일에 Release 되었습니다.

추가된 기능에 대해서 알아보겠습니다.

[What’s New In Python 3.8](https://docs.python.org/3/whatsnew/3.8.html)를 참고했습니다.

## 1. Summary - Release Highlights

### 1.1. Assignment expressions

더 큰 표현식의 일부로 변수에 값을 대입하는 새로운 문법 `:=` 이 있습니다. 바다코끼리의 눈과 엄니를 닮아서 바다코끼리 연산자(the walrus operator)라고 친근하게 알려져 있습니다.

아래 예에서, 대입 표현식은 `len()`을 두 번 호출하지 않도록 합니다:

```python
if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")
```

매치 오브젝트가 두 번 필요한 정규 표현식 매칭 중에도 유사한 이점이 발생합니다.한 번은 매치가 발생했는지 여부를 테스트하고 다른 하나는 하위 그룹을 추출합니다.

```python
discount = 0.0
if (mo := re.search(r'(\d+)% discount', advertisement)):
    discount = float(mo.group(1)) / 100.0
```

이 연산자는 루프 종료를 테스트하기 위한 값을 계산한 다음 루프 본문에서 동일한 값을 다시 필요로하는 `while` 루프에도 유용합니다.

```python
# Loop over fixed length blocks
while (block := f.read(256)) != '':
    process(block)
```

필터링 조건에서 계산된 값이 표현식 바디에도 필요한 리스트 컴프리헨션에서 또 다른 사용 사례가 생깁니다:

```python
[clean_name.title() for name in names
 if (clean_name := normalize('NFC', name)) in allowed_names]
```
복잡성을 줄이고 가독성을 개선하는 명확한 사례로 바다코끼리 연산자 사용을 제한하십시오.

자세한 설명은 [PEP 572](https://www.python.org/dev/peps/pep-0587/)를 참조하십시오.

### 1.2. Positional-only parameters

일부 함수 매개 변수를 위치적으로 지정해야만 하고 키워드 인자로 사용할 수 없도록 지시하는 새로운 함수 매개 변수 문법 `/` 이 있습니다. 이것은 Larry Hastings의 Argument Clinic 도구로 어노테이트된 C 함수들에 대해 `help()`가 보여주는 것과 같은 표기법입니다.

다음 예에서, 매개 변수 `a`와 `b`는 위치 전용이며, `c`나 `d`는 위치나 키워드일 수 있으며, `e`나 `f`는 키워드 전용이어야 합니다:

```python
def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)
```

아래는 유한 호출입니다:

```python
f(10, 20, 30, d=40, e=50, f=60)
```

하지만, 아래 예시들은 잘못된 호출입니다:

```python
f(10, b=20, c=30, d=40, e=50, f=60)   # b cannot be a keyword argument
f(10, 20, 30, 40, 50, f=60)           # e must be a keyword argument
```

이 표기법의 한 가지 사용 사례는 순수 파이썬 함수가 기존 C 코드 함수의 동작을 완전히 흉내 낼 수 있다는 것입니다. 예를 들어, 내장 `divmod()` 함수는 키워드 인자를 허용하지 않습니다

```python
def divmod(a, b, /):
    "Emulate the built in divmod() function"
    return (a // b, a % b)
```

또 다른 사용 사례는 매개 변수 이름이 도움이 되지 않을 때 키워드 인자를 배제하는 것입니다. 예를 들어, 내장 `len()` 함수의 서명은 `len(obj, /)`입니다. 이는 아래와 같은 호출을 금지합니다.

```python
len(obj='hello')  # The "obj" keyword argument impairs readability
```

매개 변수를 위치 전용으로 표시하면 클라이언트 코드를 손상할 위험 없이 매개 변수 이름을 나중에 변경할 수 있다는 추가적인 이점이 있습니다. 예를 들어, `statistics` 모듈에서, 매개 변수 이름 `dist`는 나중에 변경될 수 있습니다. 이는 다음과 같은 함수 명세 때문에 가능해졌습니다:

```python
def quantiles(dist, /, *, n=4, method='exclusive')
    ...
```

`/`의 왼쪽에 있는 매개 변수는 가능한 키워드로 노출되지 않기 때문에, 매개 변수 이름은 `**kwargs`에서 계속 사용할 수 있습니다:

```python
>>> def f(a, b, /, **kwargs):
...     print(a, b, kwargs)
...
>>> f(10, 20, a=1, b=2, c=3)         # a and b are used in two ways
10 20 {'a': 1, 'b': 2, 'c': 3}
```

이는 임의의 키워드 인자를 받아들여야 하는 함수와 메서드의 구현을 크게 단순화합니다. 예를 들어, 다음은 `collections` 모듈의 코드에서 뽑아온 것입니다:

```python
class Counter(dict):

    def __init__(self, iterable=None, /, **kwds):
        # Note "iterable" is a possible keyword argument
```

자세한 설명은 [PEP 570](https://www.python.org/dev/peps/pep-0570/)을 참고하시면됩니다.

### 1.3. Parallel filesystem cache for compiled bytecode files

새 `PYTHONPYCACHEPREFIX` 설정(`-X pycache_prefix`로도 사용 가능합니다)은 각 소스 디렉터리 내의 기본 `__pycache__` 하위 디렉터리 대신 별도의 병렬 파일 시스템 트리를 사용하도록 묵시적 바이트 코드 캐시를 구성합니다.

캐시의 위치는 `sys.pycache_prefix`로 보고됩니다 (`None`은 `__pycache__` 하위 디렉터리의 기본 위치를 나타냅니다).

### 1.4. Debug build uses the same ABI as release build

파이썬은 이제 릴리스나 디버그 모드 중 어느 것으로 빌드되더라도 같은 ABI를 사용합니다. 유닉스에서, 파이썬이 디버그 모드로 빌드될 때, 이제 릴리스 모드로 빌드된 C extension과 stable ABI를 사용해서 빌드한 C extension을 로드할 수 있습니다.

릴리스 빌드와 디버그 빌드는 이제 ABI 호환됩니다: `Py_DEBUG` 매크로를 정의하는 것은 더는 `Py_TRACE_REFS` 매크로를 암시하지 않습니다, 이는 ABI 비 호환성만 도입할 뿐입니다. `sys.getobjects()` 함수와 `PYTHONDUMPREFS` 환경 변수를 추가하는 `Py_TRACE_REFS` 매크로는 새로운 `./configure --with-trace-refs` 빌드 옵션을 사용하여 설정할 수 있습니다.

유닉스에서, C extension은 안드로이드와 Cygwin을 제외하고는 더는 libpython에 링크되지 않습니다. 이제 정적으로 링크된 파이썬이 공유 라이브러리 파이썬을 사용하여 빌드된 C extension을 로드할 수 있습니다.

유닉스에서, 파이썬이 디버그 모드로 빌드될 때, 임포트는 이제 릴리스 모드로 컴파일된 C extension과 stable ABI로 컴파일된 C extension도 찾습니다. 

파이썬을 응용 프로그램에 내장하려면, 새로운 `--embed` 옵션을 `python3-config --libs --embed`에 전달하여 `-lpython3.8`을 얻어야 합니다 (응용 프로그램을 libpython에 링크합니다). 3.8 이하를 모두 지원하려면, 먼저 `python3-config --libs --embed`를 시도하고, 실패하면 `python3-config --libs`(`--embed` 없이)로 대체하십시오.

파이썬을 응용 프로그램에 내장하기 위해, `pkg-config python-3.8-embed` 모듈을 추가했습니다: `pkg-config python-3.8-embed --libs` 는 `-lpython3.8`을 포함합니다. 3.8 이하를 모두 지원하려면, `먼저 pkg-config python-X.Y-embed --libs` 를 시도하고, 실패하면 p`kg-config python-X.Y --libs`(`--embed` 없이)로 대체하십시오 (`X.Y`를 파이썬 버전으로 교체하십시오).

반면에, `pkg-config python3.8 --libs` 는 더는 `-lpython3.8`을 포함하지 않습니다. C extension은 libpython에 링크되어서는 안 됩니다 (안드로이드와 Cygwin은 예외인데, 이들은 스크립트로 처리됩니다); 이 변경은 의도적으로 이전 버전과 호환되지 않습니다.

### 1.5. f-strings support = for self-documenting expressions and debugging

f-string에 `=` 지정자를 추가했습니다. `f'{expr=}'`과 같은 f-string format specifiers의 텍스트, 등호, 평가된 표현식의 표현(repr)으로 확장됩니다. 아래는 예시입니다:

```python
>>> user = 'eric_idle'
>>> member_since = date(1975, 7, 31)
>>> f'{user=} {member_since=}'
"user='eric_idle' member_since=datetime.date(1975, 7, 31)"
```

일반적인 f-string format specifiers 를 사용하면 표현식의 결과가 표시되는 방식을 더 잘 제어할 수 있습니다:

```python
>>> delta = date.today() - member_since
>>> f'{user=!s}  {delta.days=:,d}'
'user=eric_idle  delta.days=16,075'
The = specifier will display the whole expression so that calculations can be shown:
```

`=` 연산자는 계산을 표시할 수 있도록 전체 표현식을 표시합니다:

```python
>>> print(f'{theta=}  {cos(radians(theta))=:.3f}')
theta=30  cos(radians(theta))=0.866
```

### 1.6. [PEP 578](https://www.python.org/dev/peps/pep-0578/): Python Runtime Audit Hooks

이 PEP는 Audit Hook과 확인된 Verified Open Hook을 추가합니다. 둘 다 파이썬과 네이티브 코드에서 사용 가능해서, 순수 파이썬 코드로 작성된 응용 프로그램과 프레임워크가 추가 알림을 활용할 수 있도록 함과 동시에 embedder나 시스템 관리자가 감사가 항상 활성화된 파이썬 빌드를 배치할 수 있도록 합니다.

자세한 설명은 [PEP 578](https://www.python.org/dev/peps/pep-0578/)을 참조하십시오.

### 1.7. [PEP 587](https://www.python.org/dev/peps/pep-0587/): Python Initialization Configuration

[PEP 587](https://www.python.org/dev/peps/pep-0587/)은 파이썬 초기화를 구성하는 새로운 C API를 추가하여 전체 구성에 대한 세밀한 제어와 개선된 에러 보고를 제공합니다.

New structures:

* `PyConfig`
* `PyPreConfig`
* `PyStatus`
* `PyWideStringList`
 
New functions:

* `PyConfig_Clear()`
* `PyConfig_InitIsolatedConfig()`
* `PyConfig_InitPythonConfig()`
* `PyConfig_Read()`
* `PyConfig_SetArgv()`
* `PyConfig_SetBytesArgv()`
* `PyConfig_SetBytesString()`
* `PyConfig_SetString()`
* `PyPreConfig_InitIsolatedConfig()`
* `PyPreConfig_InitPythonConfig()`
* `PyStatus_Error()`
* `PyStatus_Exception()`
* `PyStatus_Exit()`
* `PyStatus_IsError()`
* `PyStatus_IsExit()`
* `PyStatus_NoMemory()`
* `PyStatus_Ok()`
* `PyWideStringList_Append()`
* `PyWideStringList_Insert()`
* `Py_BytesMain()`
* `Py_ExitStatusException()`
* `Py_InitializeFromConfig()`
* `Py_PreInitialize()`
* `Py_PreInitializeFromArgs()`
* `Py_PreInitializeFromBytesArgs()`
* `Py_RunMain()`

이 PEP는 이러한 내부 구조체에 `_PyRuntimeState.preconfig`(`PyPreConfig` 타입)와 `PyInterpreterState.config` (`PyConfig` 타입) 필드를 추가합니다. `PyInterpreterState.config`는 전역 구성 변수와 기타 내부(`private`) 변수를 대체하는 새로운 참조 구성이 됩니다.

설명서는 파이썬 초기화 구성을 참조하십시오.

자세한 설명은 [PEP 587](https://www.python.org/dev/peps/pep-0587/)을 참조하십시오.

### 1.8. Vectorcall: a fast calling protocol for CPython

`vectorcall` 프로토콜은 Python/C API에 추가됩니다. 이미 다양한 클래스에 대해 수행된 기존 최적화를 공식화하기 위한 것입니다. 호출 가능을 구현하는 모든 확장 유형은 이 프로토콜을 사용할 수 있습니다.

이것은 현재 잠정적이며, 목표는 파이썬 3.9에서 완전히 공개하는 것입니다.

자세한 설명은 [PEP 590](https://www.python.org/dev/peps/pep-0590/)을 참조하십시오.

### 1.9. Pickle protocol 5 with out-of-band data buffers

멀티 코어나 멀티 머신 프로세싱을 활용하기 위해 `pickle`을 사용해서 파이썬 프로세스 간에 큰 데이터를 전송할 때, 메모리 복사를 줄이고 데이터 종속적 압축과 같은 사용자 정의 기술을 적용하여 전송을 최적화하는 것이 중요합니다.

`pickle` 프로토콜 5는 통신 계층의 재량에 따라 [PEP 3118](https://www.python.org/dev/peps/pep-3118/) 호환 데이터가 주 피클 스트림과 별도로 전송될 수 있는 아웃 오브 밴드 버퍼를 지원합니다.

자세한 설명은 [PEP 574](https://www.python.org/dev/peps/pep-0574/)를 참조하십시오.