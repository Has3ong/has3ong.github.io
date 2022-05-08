---
title:  "Python 3.9의 새로운 기능"
excerpt: "Python 3.9의 새로운 기능"
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

Python 3.9 버전이 2019년 1월 4일에 Release 되었습니다.

추가된 기능에 대해서 알아보겠습니다.

[What’s New In Python 3.9](https://docs.python.org/3/whatsnew/3.9.html)를 참고했습니다.

## 1. New Features

### 1.1. Dictionary Merge & Update Operators

dictionary 타입에서 기존에 사용하던 `dict.uupdate`와 `{**d1, **d2}`를 개선했습니다. `|`와 `|=` 연산자를 통해 merge와 update를 수행할 수 있습니다.

```python
>>> x = {"key1": "value1 from x", "key2": "value2 from x"}
>>> y = {"key2": "value2 from y", "key3": "value3 from y"}
>>> x | y
{'key1': 'value1 from x', 'key2': 'value2 from y', 'key3': 'value3 from y'}
>>> y | x
{'key2': 'value2 from x', 'key3': 'value3 from y', 'key1': 'value1 from x'}
```

자세한 내용은 [PEP 584](https://www.python.org/dev/peps/pep-0584/)에서 전부 확인할 수 있습니다. 

### 1.2. New String Methods to Remove Prefixes and Suffixes

`str.removeprefix(suffix)`와 `str.removesuffix(suffix)` 함수가 추가됐습니다. 이제 문자열에 접두사와 접미사를 쉽게 제거할 수 있습니다.

함수 원형은 다음과 같습니다.

```python
def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

def removesuffix(self: str, suffix: str, /) -> str:
    # suffix='' should not call self[:-0].
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]
```

다음과 같이 사용합니다.

```python
string = "has3ong.github.io"
print(string.removeprefix("has3ong"))
print(string.removeprefix("github"))
print(string.removesuffix("io"))
print(string.removesuffix("github"))
```

결과는 아래와 같습니다.

```
.github.io
has3ong.github.io
has3ong.github.
has3ong.github.io
```

자세한 내용은 [PEP 616](https://www.python.org/dev/peps/pep-0616/)에서 전부 확인할 수 있습니다. 

### 1.3. Type Hinting Generics in Standard Collections

타입 어노테이션에서 `typing`에 해당하는 대문자 형을 사용하는 대신 `list`와 `dict` 같은 내장 컬렉션 타입을 제네릭 타입으로 사용할 수 있습니다. 표준 라이브러리에 있는 일부 다른 타입도 이제 제네릭으로 사용할 수 있습니다. 대표적으로 `queue.Queue`가 있습니다.

> 예시

```python
def greet_all(names: list[str]) -> None:
    for name in names:
        print("Hello", name)
```

자세한 내용은 [PEP 585](https://www.python.org/dev/peps/pep-0585/)에서 전부 확인할 수 있습니다. 

### 1.4. New Parser

Python 3.9에서는 [LL(1)](https://en.wikipedia.org/wiki/LL_parser) 대신 [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar)를 기반으로 하는 새로운 파서를 사용합니다. 새로운 파서는 기존 파서와 성능이 비슷하지만, PEG 형식은 새로운 언어 기능을 설계할 때 보다 더 유연합니다.

자세한 내용은 [PEP 617](https://www.python.org/dev/peps/pep-0617/)에서 전부 확인할 수 있습니다. 

## 2. Summary – Release highlights

#### New syntax features:

* [PEP 584](https://www.python.org/dev/peps/pep-0584/), union operators added to dict;
* [PEP 585](https://www.python.org/dev/peps/pep-0585/), type hinting generics in standard collections;
* [PEP 614](https://www.python.org/dev/peps/pep-0614/), relaxed grammar restrictions on decorators.

#### New built-in features:

* [PEP 616](https://www.python.org/dev/peps/pep-0616/), string methods to remove prefixes and suffixes.

#### New features in the standard library:

* [PEP 593](https://www.python.org/dev/peps/pep-0593/), flexible function and variable annotations;
* `os.pidfd_open()` added that allows process management without races and signals.

#### Interpreter improvements:

* [PEP 573](https://www.python.org/dev/peps/pep-0573/), fast access to module state from methods of C extension types;
* [PEP 617](https://www.python.org/dev/peps/pep-0617/), CPython now uses a new parser based on PEG;
* a number of Python builtins (range, tuple, set, frozenset, list, dict) are now sped up using PEP 590 vectorcall;
* garbage collection does not block on resurrected objects;
* a number of Python modules (`_abc`, `audioop`, `_bz2`, `_codecs`, `_contextvars`, `_crypt`, `_functools`, `_json`, `_locale`, `math`, `operator`, `resource`, `time`, `_weakref`) now use multiphase initialization as defined by PEP 489;
* a number of standard library modules (`audioop`, `ast`, `grp`, `_hashlib`, `pwd`, `_posixsubprocess`, `random`, `select`, `struct`, `termios`, `zlib`) are now using the stable ABI defined by PEP 384.

#### New library modules:

* [PEP 615](https://www.python.org/dev/peps/pep-0615/), the IANA Time Zone Database is now present in the standard library in the zoneinfo module;
* an implementation of a topological sort of a graph is now provided in the new graphlib module.

#### Release process changes:

* [PEP 602](https://www.python.org/dev/peps/pep-0602/), CPython adopts an annual release cycle.

> 참고자료

* [What’s New In Python 3.9](https://docs.python.org/3/whatsnew/3.9.html)