---
title:  "Python 3.7의 새로운 기능"
excerpt: "Python 3.7의 새로운 기능"
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

Python 3.7 버전이 2018년 6월 27일에 Release 되었습니다.

추가된 기능에 대해서 알아보겠습니다.

[What’s New In Python 3.7](https://docs.python.org/3/whatsnew/3.7.html)를 참고했습니다.

## 1. New Features

### 1.1. PEP 563: Postponed Evaluation of Annotations

파이썬에서 type hint의 출현은 [PEP 3107](https://www.python.org/dev/peps/pep-3107/)에서 추가되고 [PEP 526](https://www.python.org/dev/peps/pep-0526/)에서 더욱 다듬어진 어노테이션의 두 가지 사용성 문제를 드러냈습니다:

* 어노테이션은 현재 스코프에서 이미 사용 가능한 이름 만 사용할 수 있습니다. 즉, 어떤 종류의 전방 참조도 지원하지 않았습니다;
* 소스 코드에 어노테이션을 붙이는 것은 파이썬 프로그램의 시작 시간에 악영향을 미쳤습니다.

이 두 가지 문제는 어노테이션 평가를 지연시키는 것으로 해결됩니다. 정의 시간에 어노테이션의 표현식을 실행하는 코드를 컴파일하는 대신, 컴파일러는 해당 표현식의 AST와 동등한 문자열 형식으로 어노테이션을 저장합니다. 필요하다면, 실행시간에 `typing.get_type_hints()` 를 사용하여 어노테이션을 해석 할 수 있습니다. 이것이 필수적이지 않은 일반적인 경우에는, 어노테이션을 싸게 저장할 수 있고 (짧은 문자열은 인터프리터에 의해 한 번만 만들어지기 때문입니다), 시작 시간을 더 빠르게 할 수 있습니다.

사용성 측면에서, 이제 어노테이션이 전방 참조를 지원하므로 다음 문법이 유효합니다:

```python
class C:
    @classmethod
    def from_string(cls, source: str) -> C:
        ...

    def validate_b(self, obj: B) -> bool:
        ...

class B:
    ...
```

이 변경으로 인해 호환성이 깨지기 때문에, 파이썬 3.7에서 새 동작은 `__future__` 임포트를 사용하여 모듈별로 새로운 동작을 활성화해야 합니다:

```python
from __future__ import annotations
```

### 1.2. PEP 538: Legacy C Locale Coercion

파이썬 3시리즈에서 진행 중인 과제는, 윈도우 이외의 플랫폼에서 기본 C 또는 POSIX 로케일 사용으로 인해 묵시적으로 가정되는 《7-bit ASCII》 텍스트 인코딩을 처리하기 위한 적절한 기본 전략을 결정하는 것입니다.

새 `PYTHONCOERCECLOCALE` 환경 변수의 설명서에 설명되어있듯이, [PEP 538](https://www.python.org/dev/peps/pep-0538s/) 은 기본 인터프리터 명령행 인터페이스를 갱신하여, 사용 가능한 UTF-8 기반 로케일로 자동으로 강제 변경합니다. 이런 식으로 `LC_CTYPE` 을 자동 설정하는 것은, 핵심 인터프리터와 로케일을 인식하는 C 확장 (가령 `readline`) 모두 기본 텍스트 인코딩으로 ASCII 대신 UTF-8을 가정하게 된다는 뜻입니다.

[PEP 11](https://www.python.org/dev/peps/pep-0011/) 의 플랫폼 지원 정의 역시 전체 텍스트 처리 지원을 적절히 구성된 비 ASCII 기반 로케일로 제한하도록 갱신되었습니다.

이 변경의 일부로, 이제 정의된 강제 변경 대상 로케일(현재 `C.UTF-8,` `C.utf8`, `UTF-8`)을 사용할 때, `stdin` 과 `stdout` 의 기본 에러 처리기는 (`strict` 대신) `surrogateescape` 입니다. `stderr` 의 기본 에러 처리기는 로케일에 관계없이 계속 `backslashreplace` 입니다.

로케일 강제 변경은 기본적으로 조용히 일어나지만, 로케일 관련 통합 문제를 디버깅하는 데 도움을 주기 위해 `PYTHONCOERCECLOCALE=warn` 를 설정해서 (`stderr` 로 직접 출력되는) 명시적 경고를 요청할 수 있습니다. 또한, 이 설정은 핵심 인터프리터가 초기화될 때 레거시 C 로케일이 활성 상태로 남아 있으면 파이썬 런타임이 경고를 하도록 만듭니다.

[PEP 538](https://www.python.org/dev/peps/pep-0538/) 의 로케일 강제 변환이 (비 파이썬 응용 프로그램과 이전 버전의 파이썬을 실행하는 경우를 포함하는) 자식 프로세스뿐만 아니라 (GNU `readline` 같은) 확장 모듈에도 영향을 주는 장점이 있지만, 실행 중인 시스템에 적절한 대상 로케일이 있어야 한다는 단점이 있습니다. 적절한 대상 로케일을 사용할 수 없는 경우(예를 들어, RHEL/CentOS 7에서 발생하듯이)를 더 잘 처리하기 위해, **파이썬 3.7은 PEP 540: 강제 UTF-8 실행시간 모드** 또한 구현합니다.

### 1.3. PEP 540: Forced UTF-8 Runtime Mode

새로운 `-X utf8` 명령행 옵션과 `PYTHONUTF8` 환경 변수를 사용하여 CPython UTF-8 모드 를 활성화할 수 있습니다.

UTF-8 모드에서, CPython은 로케일 설정을 무시하고 기본적으로 UTF-8 인코딩을 사용합니다. `sys.stdin` 과 `sys.stdout` 스트림의 에러 처리기는 `surrogateescape` 로 설정됩니다.

강제 UTF-8 모드는 임베디드 응용 프로그램의 로케일 설정을 변경하지 않고 임베디드 파이썬 인터프리터의 텍스트 처리 동작을 변경하는 데 사용할 수 있습니다.

[PEP 540](https://www.python.org/dev/peps/pep-0540/) 의 UTF-8 모드는 실행 중인 시스템에서 사용할 수 있는 로케일에 관계없이 작동하는 이점이 있지만, (GNU readline 과 같은) 확장 모듈, 비 파이썬 응용 프로그램을 실행하는 자식 프로세스, 이전 버전의 파이썬을 실행하는 자식 프로세스에 영향을 주지 못하는 단점이 있습니다. 이러한 구성 요소와 통신 할 때 텍스트 데이터가 손상될 위험을 줄이기 위해 파이썬 3.7은 **PEP 540: 강제 UTF-8 실행시간 모드** 또한 구현합니다.

UTF-8 모드는 로케일이 `C` 또는 `POSIX` 이고, [PEP 538](https://www.python.org/dev/peps/pep-0538/) 로케일 강제 변환이 UTF-8 기반 대안으로의 변경에 실패할 때 (그 실패가 P`YTHONCOERCECLOCALE=0` 설정 때문이든, `LC_ALL` 설정 때문이든, 적절한 대상 로케일이 없기 때문이든 무관하게) 기본적으로 활성화됩니다.

### 1.4. PEP 553: Built-in breakpoint()

파이썬 3.7에는 파이썬 디버거에 진입하는 쉽고 일관된 방식을 제공하는 새로운 내장 `breakpoint()` 함수가 포함되어 있습니다.

내장 `breakpoint()` 는 `sys.breakpointhook()` 을 호출합니다. 기본적으로, 후자는 `pdb`를 임포트 한 다음 `pdb.set_trace()` 를 호출합니다. 하지만, `sys.breakpointhook()` 을 여러분이 선택한 함수에 연결하면, `breakpoint()` 는 임의의 디버거에 진입할 수 있습니다. 또한, 환경 변수 `PYTHONBREAKPOINT` 를 여러분이 선택한 디버거의 콜러블로 설정할 수 있습니다. 내장 `breakpoint()` 를 완전히 비활성화하려면 `PYTHONBREAKPOINT=0` 를 설정하십시오.

### 1.5. PEP 539: New C API for Thread-Local Storage

파이썬은 스레드 로컬 저장소 지원을 위한 C API를 제공하지만; **기존 스레드 로컬 저장소 (TLS) API** 는 모든 플랫폼에서 TLS 키로 int를 사용합니다. 이것은 공식적으로 지원되는 플랫폼에서는 일반적으로 문제가 되지 않지만, POSIX를 준수하지도 실용적인 의미에서 이식성이 있지도 않습니다.

[PEP 539](https://www.python.org/dev/peps/pep-0539/) 는 CPython에 **새로운 스레드 특정 저장소 (TSS) API** 를 제공해서 이를 변경하는데, CPython 인터프리터 내에서 기존 TLS API의 사용을 대체하는 동시에 기존 API를 폐지합니다. TSS API는 TSS 키를 나타내는데 int 대신 `Py_tss_t`라는 새로운 형을 사용합니다. 이 형은 하부 TLS 구현에 따라 달라질 수 있는 불투명 한 형입니다. 그래서 네이티브 TLS 키가 int로 안전하게 캐스팅될 수 없는 방식으로 정의된 플랫폼에서 CPython을 빌드 할 수 있게 합니다.

네이티브 TLS 키가 int로 안전하게 캐스팅될 수 없는 방식으로 정의된 플랫폼에서는, 기존 TLS API의 모든 함수는 작동하지 않고 즉시 실패를 반환합니다. 이는 이전 API가 신뢰성 있게 사용될 수 없는 플랫폼에서 지원되지 않으며, 이러한 지원을 추가하기 위한 노력이 없을 것을 분명하게 나타냅니다.

`Py_tss_t` 는 현재 다음과 같이 정의되어 있습니다.

```c
typedef struct {
    int _is_initialized;
    NATIVE_TSS_KEY_T _key;
} Py_tss_t;
```

### 1.6. PEP 562: Customization of Access to Module Attributes

파이썬 3.7은 모듈에, 발견되지 않는 어트리뷰트마다 호출되는 `__getattr__()` 을 정의할 수 있도록 합니다. 이제 모듈에 `__dir__()` 도 정의할 수 있게 되었습니다.

이것이 유용한 전형적인 예는 모듈 어트리뷰트 폐지와 지연 로딩입니다

### 1.7. PEP 564: New Time Functions With Nanosecond Resolution

현대 시스템의 시계 해상도는 `time.time()` 함수와 그 변형이 반환하는 부동 소수점 숫자의 제한된 정밀도를 초과 할 수 있습니다. [PEP 564](https://www.python.org/dev/peps/pep-0564/) 는 기존 타이머 함수의 새로운 《나노 초》 변형을 `time` 모듈에 추가합니다:

* `time.clock_gettime_ns()`
* `time.clock_settime_ns()`
* `time.monotonic_ns()`
* `time.perf_counter_ns()`
* `time.process_time_ns()`
* `time.time_ns()`

새로운 함수는 나노초의 수를 정숫값으로 반환합니다.

<https://www.python.org/dev/peps/pep-0564/#annex-clocks-resolution-in-python> 의 측정에 의하면 리눅스와 윈도우에서 `time.time_ns()` 의 해상도는 `time.time()` 보다 약 3배 정밀합니다.

### 1.8. PEP 565: Show DeprecationWarning in __main__

`DeprecationWarning`의 기본 처리 방식이 변경되어, 이러한 경고가 다시 한번 기본적으로 표시됩니다. 하지만, 이를 발생시킨 코드가 `__main__` 모듈에서 직접 실행될 때만 표시됩니다. 결과적으로, 단일 파일 스크립트 개발자와 파이썬을 대화식으로 사용하는 개발자는 사용하는 API에 대한 폐지 경고를 다시 보게 되지만, 임포트되는 응용 프로그램, 라이브러리, 프레임워크 모듈에서 발생하는 Deprecation Warnings 는 기본적으로 계속 숨겨집니다.

이 변경으로 인해, 이제 표준 라이브러리는 개발자가 세 가지 다른 Deprecation Warnings 동작 중 하나를 선택할 수 있도록 합니다:

* `FutureWarning`: 기본적으로 항상 표시됩니다. 응용 프로그램 최종 사용자를 대상으로 하는 경고로 권장됩니다 (예, 폐지된 응용 프로그램 구성 설정).
* `DeprecationWarning`: 기본적으로 `__main__` 과 테스트 실행 시에 표시됩니다. 버전 업그레이드가 동작 변경이나 에러를 일으킬 수 있어서, 다른 파이썬 개발자를 대상으로 하는 경고로 권장됩니다.
* `PendingDeprecationWarning`: 기본적으로 테스트 실행 시에만 표시됩니다. 향후 버전 업그레이드가 경고 범주를 `DeprecationWarning` 이나 `FutureWarning`으로 변경하게 될 경우를 위한 것입니다.

이전에는 `DeprecationWarning` 과 `PendingDeprecationWarning` 둘 다 테스트를 실행할 때만 볼 수 있었습니다. 주로 단일 파일 스크립트를 작성하거나 대화식으로 파이썬을 사용하는 개발자는 사용된 API가 호환되지 않는 방식으로 변경된 것을 보고 놀랄 수 있었습니다.

### 1.9. PEP 560: Core Support for typing module and Generic Types

처음에는 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 가 핵심 CPython 인터프리터의 어떤 변경도 도입하지 않도록 설계되었습니다. 이제 type hint와 `typing` 모듈이 커뮤니티에서 광범위하게 사용되므로, 이 제한이 제거됩니다. PEP는 두 개의 특수 메서드 `__class_getitem__()` 과 `__mro_entries__` 를 소개합니다. 이 메서드는 이제 `typing` 에 있는 대부분 클래스와 특수 구조체에서 사용됩니다. 그 결과로, 타입과 관련된 여러 연산의 속도가 최대 7배까지 증가했고, 제네릭 형은 메타 클래스 충돌 없이 사용할 수 있으며, `typing` 모듈의 몇 가지 오랜 버그가 해결되었습니다.

### 1.10. PEP 552: Hash-based .pyc Files

파이썬은 전통적으로 바이트 코드 캐시 파일(즉, `.pyc` 파일)의 최신성을 검사하기 위해, 소스 메타 데이터(최종 수정 타임스탬프와 크기)를 캐시 파일이 만들어질 때 헤더에 저장된 소스 메타 데이터와 비교했습니다. 효과적이지만, 이 무효화 방법에는 단점이 있습니다. 파일 시스템 타임스탬프가 너무 조잡한 경우, 파이썬은 소스 변경을 놓칠 수 있어 사용자 혼란을 낳을 수 있습니다. 또한, 캐시 파일에 타임스탬프를 갖는 것은 빌드 재현성 과 콘텐츠 기반 빌드 시스템에서 문제가 됩니다.

[PEP 552](https://www.python.org/dev/peps/pep-0552/) 는 소스 타임스탬프 대신 소스 파일의 해시가 소스 타임스탬프 대신 무효화에 사용될 수 있도록 pyc 형식을 확장합니다. 이러한 `.pyc` 파일을 《해시 기반》이라고 합니다. 기본적으로, 파이썬은 여전히 타임스탬프 기반 무효화를 사용하며 실행 시간에 해시 기반 `.pyc` 파일을 생성하지 않습니다. 해시 기반 `.pyc` 파일은 `py_compile` 또는 `compileall`로 만들 수 있습니다.

해시 기반 `.pyc` 파일에는 두 가지 변형이 있습니다: 검사형(checked)과 비검사형(unchecked). 파이썬은 검사형 해시 기반 `.pyc` 파일을 실행시간에 해당 소스 파일에 대해 유효성을 검사하지만, 비검사형 해시 기반 pyc에 대해서는 확인하지 않습니다. 비검사형 해시 기반 `.pyc` 파일은 파이썬 외부의 시스템(가령 빌드 시스템)이 `.pyc` 파일을 최신 상태로 유지하는 책임을 지는 환경에서 유용한 성능 최적화입니다.

### 1.11. PEP 545: Python Documentation Translations

[PEP 545](https://www.python.org/dev/peps/pep-0545/)는 파이썬 설명서 번역을 만들고 유지하는 과정을 설명합니다.

세 가지 새로운 번역이 추가되었습니다:

* 일본어: https://docs.python.org/ja/
* 프랑스어: https://docs.python.org/fr/
* 한국어: https://docs.python.org/ko/

### 1.12. Development Runtime Mode: -X dev

새 `-X dev` 명령행 옵션이나 새 `PYTHONDEVMODE` 환경 변수를 사용하여 CPython의 개발 모드를 활성화할 수 있습니다. 개발 모드에 있을 때, CPython은 기본적으로 활성화되기에는 너무 비싸고 추가적인 실행 시간 검사를 수행합니다. 이 모드의 효과에 대한 자세한 설명은 `-X dev` 설명서를 보십시오.

## 2. Summary – Release Highlights

#### New syntax features:

* [PEP 563](https://www.python.org/dev/peps/pep-0563/), postponed evaluation of type annotations.

#### Backwards incompatible syntax changes:

* `async` and `await` are now reserved keywords.

#### New library modules:

* contextvars: [PEP 567](https://www.python.org/dev/peps/pep-0567/) – Context Variables
* dataclasses: [PEP 557](https://www.python.org/dev/peps/pep-0557/) – Data Classes
* importlib.resources

#### New built-in features:

* [PEP 553](https://www.python.org/dev/peps/pep-0563/), the new `breakpoint()` function.

#### Python data model improvements:

* [PEP 562](https://www.python.org/dev/peps/pep-0562/), customization of access to module attributes.
* [PEP 560](https://www.python.org/dev/peps/pep-0560/), core support for typing module and generic types.
* the insertion-order preservation nature of dict objects has been declared to be an official part of the Python language spec.

#### Significant improvements in the standard library:

* The `asyncio` module has received new features, significant usability and performance improvements.
* The `time` module gained support for functions with nanosecond resolution.

#### CPython implementation improvements:

* Avoiding the use of ASCII as a default text encoding:
  * [PEP 538](https://www.python.org/dev/peps/pep-0538/), legacy C locale coercion
  * [PEP 540](https://www.python.org/dev/peps/pep-0540/), forced UTF-8 runtime mode
* [PEP 552](https://www.python.org/dev/peps/pep-0552/), deterministic .pycs
* the new development runtime mode
* [PEP 565](https://www.python.org/dev/peps/pep-0565/), improved DeprecationWarning handling

#### C API improvements:

* [PEP 539](https://www.python.org/dev/peps/pep-0539/), new C API for thread-local storage

#### Documentation improvements:

* [PEP 545](https://www.python.org/dev/peps/pep-0545/), Python documentation translations
* New documentation translations: Japanese, French, and Korean.