---
title : 해시함수의 속성 및 특징
categories:
- Computer Science
tags : 
- Computer Science
- Hash
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

현 포스트에서는 해시 함수에대해 간략하게만 살펴보겠습니다.

## 1. 해시함수란

![image](/assets/images/cs/hashfunction1.svg)

해시 함수는 임의 크기의 데이터를 고정 크기 값으로 매핑하는 데 사용할 수 있는 모든 함수입니다. 해시 함수에서 반환된 값을 ***hash value***, ***hash code***, ***digest*** 또는 ***simply hash*** 라고  합니다. 값은 일반적으로 해시 테이블이라는 고정 크기 테이블을 인덱싱하는 데 사용됩니다. 해시 테이블을 인덱싱하기 위해 해시 함수를 사용하는 것을 ***hashing*** 또는 ***scatter storage addressing*** 이라고 합니다.

해시 함수 및 관련 해시 테이블은 데이터 저장 및 검색 응용 프로그램에서 검색당 거의 일정한 시간에 데이터에 액세스하는 데 사용됩니다. 데이터 또는 레코드 자체에 필요한 총 공간보다 극히 일부만 더 많은 양의 저장 공간이 필요합니다. 해싱은 정렬된 목록과 정렬되지 않은 목록 및 구조화된 트리의 일정하지 않은 액세스 시간과 크거나 가변 길이 키의 상태 공간에 대한 직접 액세스의 기하급수적인 저장소 요구 사항을 피하는 계산 및 저장 공간 효율적인 데이터 액세스 형식입니다.

## 2. 해시 함수의 특징

일방향 해시함수의 특징은 아래와 같습니다.

1. 임의 길이의 메세지로부터 고정 길이의 해시 값을 계산한다.
2. 일방향성을 갖는다. 해시값으로부터 메세지를 역으로 계산할 수 없다.
3. 메세지가 다르면 해시값도 다르다.
4. 해시값을 고속으로 계산할 수 있다.

그래서 다음과 같은 효과가 있습니다.

* 압축 효과
  * 해시 함수가 반환하는 작은 해시값만으로도 거대한 크기의 데이터 무결성을 보장
* 눈사태 효과
  * 아주 작은 변화로도 결과값이 전혀 다르게 도출됨
* 정보의 무결성 확인
  * 자신이 받은 암호화의 결과에 공개된 해시값과 검사합(Checksum)을 비교하면 무결성 검증 가능
* 암호 저장
  * 암호 저장 시 그대로 저장하지 않고 해시함수로 암호화하여 저장하여 DB가 노출되어도 암호가 노출되지 않음
* 해시테이블에서의 활용
  * 데이터 목록에서 특정 데이터를 조회할 때, 키 값으로 탐색 범위 및 시간을 줄일 수 있음

## 3. 해시 함수의 요구사항

### 1. 프리 이미지 저항성 (역상 저항성)

주어진 임의의 출력값 $y$에 대해, $y = h(x)$를 만족하는 입력값 $x$를 찾는 것이 계산적으로 불가능

### 2. 제 2프리 이미지 저항성 (두 번째 역상 저항성, 약한 충돌 내성)

주어진 입력값 $x$에 대해, $h(x) = h(x^\prime) , x \neq x^\prime$을 만족하는 다른 입력값 $x^\prime$를 찾는 것이 계산적으로 불가능

### 3. 충돌 저항성 (충돌 회피성, 강한 충돌 내성)

$h(x) = h(x^\prime)$을 만족하는 임의의 두 입력값 $x, x^\prime$을 찾는 것이 계산적으로 불가능

> 참고자료

* [Hash function - Wikipedia](https://en.wikipedia.org/wiki/Hash_function)