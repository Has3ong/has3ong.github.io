---
title : Python
tags:
- Python
- String
- Memory
categories:
- Programming
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## [Python] 문자열의 메모리 할당 방식

Python의 경우 문자열 객체 생성 시 매번 새로운 객체를 만드는 대신 기존에 선언되어 있던 immutable 객체를 사용합니다.

이는 CPython의 최적화 기법인 string interning에 의한 동작입니다. 따라서 둘 이상의 변수가 메모리의 동일한 문자열 객체를 가리킬 수 있고, 메모리를 절약하게 됩니다.

> Example

```
a = 'Hello'
b = 'Hello'

print(id(a), id(b))
> 4376187184 4376187184
```

string interning 최적화에는 몇가지 규칙이 있습니다.

* 길이가 0 또는 1인 문자열은 intern
* 컴파일 타임에만 intern : 동적으로 문자열을 만들어내는 경우(포맷팅 등) intern되지 않음
* ASCII 문자, 숫자 또는 언더스코어가 아닌 문자가 속해 있는 경우(!, ? 등) intern되지 않음

> Example

```
a = "Hello World!"
b = "Hello World!"

print(id(a), id(b))
> 4374237616 4376187568
```
