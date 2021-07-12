---
title : Struct 
tags:
- Computer Science
categories:
- Computer Science
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

구조체 크기를 구하기전 구조체와 자료형 크기에 대해서 정리를 하고 시작하겠습니다.

## Struct

C/C++ 프로그래밍 언어에서 구조화 된 데이터를 처리할 때 struct를 사용하는데 이를 구조체라고 한다. 구조화되었다는 말은 의미가 연결되어 한 덩어리로 처리하는 방식을 말한다. 관련된 컴퓨터 용어로 보면 record 그리고 Object와 비슷한 개념이다. 그리고 자료처리와 연관하여 데이터 구조와 연관이 되어 있다.

> Example

```
struct Man {
  char name[50];
  int  age;
  char gender;
  char tel[50];
};
```

## 자료형 크기

그리고 아래는 32bit를 기준으로 한 자료형의 크기입니다.
* char 1byte
* wchar_t 2byte
* bool 1byte
* short 2byte
* int 4byte
* long 4byte
* float 4byte
* double 8byte

## 구조체 크기 구하기

대부분의 자료가 10년 이상된 자료라 요즘 컴파일러로 적용하면 자동으로 1배수 정렬을 사용하여 사이즈를 계산해 주기 때문에 아래와 같이 명시적으로 4배수 정렬을 사용한다고 해줘야합니다.

```
//
//  main.c
//  abc
//
//  Created by AHG223 on 2019/10/07.
//  Copyright © 2019 None. All rights reserved.
//
#include <stdio.h>


struct PacketHeader {
    __attribute__((aligned(4))) char a;
    __attribute__((aligned(4))) char b;
    __attribute__((aligned(4))) double c;
};

int main()
{
    struct PacketHeader header;
    printf("%d\n", sizeof(header)); // 6
    return 0;
}
```

### 데이터 정렬

현대의 컴퓨터는 메모리에 데이터를 쓰거나 읽을 때 워드(WORD)라는 단위로 수행한다. 그리고 32Bit 컴퓨터에서 1WORD는 4바이트(Bytes)의 크기를 가진다. 그러면 데이터 정렬은 무엇을 의미하게 되는지 알려드리겠습니다.
예를들어, 데이터는 6byte지만 데이터가 메모리 3, 4, 5, 6, 7, 8 이렇게 위치한다고 보겠습니다. 그림으로 그려보면 아래와 같습니다.(죄송합니다.)

```
|-|-|-|o| |o|o|o|o| |o|-|-|-|
```

컴퓨터는 이 데이터를 읽기 위해선 총 12바이트의 데이터를 읽어야 하게 됩니다. 이는 상당히 비효율적이므로 데이터 정렬을 이용하여 아래와 같이 만들면 8byte만 읽어도 전체 데이터를 읽을 수 있게 할 수 있습니다.

```
|-|-|-|-| |o|o|o|o| |o|o|-|-|
```

### 데이터 패딩

컴파일러가 데이터 패딩을 할 때 암묵적인 규칙이 있습니다. 그래서 미리 몇 배수 정렬을 사용할것인가를 명시적으로 사용하지 않으면 아래의 규칙을 따르게 됩니다.

```
1. 구조체의 크기는 구조체를 이루는 자료형 중 가장 크기가 큰 자료형의 배수가 된다.

2. 구조체를 이루는 자료형 중 가장 크기가 큰 자료형으로 데이터를 정렬한다.

3. 데이터는 자기 배수의 위치에 정렬한다.
```

사용 예시는 아래 블로그에 좋은 자료가 있어서 사진으로 대체 하겠습니다.

> Case 1

```
struct A{
  char a;
  char b;
  int c;
};
```

![스크린샷 2019-10-08 오후 4 50 20](https://user-images.githubusercontent.com/44635266/66377081-d0223580-e9eb-11e9-9002-80a4bf288a5f.png)


> Case2

```
struct A{
  char a;
  int c;
  char b;
};
```

![스크린샷 2019-10-08 오후 4 50 24](https://user-images.githubusercontent.com/44635266/66377085-d0bacc00-e9eb-11e9-896e-9f31bcd76096.png)


> Case3


```
struct A{
  char a;
  double b;
};
```

![스크린샷 2019-10-08 오후 4 50 30](https://user-images.githubusercontent.com/44635266/66377086-d0bacc00-e9eb-11e9-9d92-5ed406ac58de.png)

> Case4

```
struct A{
  char a;
  int c;
  double b;
};
```

![스크린샷 2019-10-08 오후 4 50 34](https://user-images.githubusercontent.com/44635266/66377087-d0bacc00-e9eb-11e9-8ce6-805482ac98b5.png)

만약 Case3에서 4배수 정렬을 사용하겠다고 하면 데이터의 크기는 어떻게 될까요. 정답은 12byte입니다.
char a가 가장 큰 double 8byte를 가지는게 아니라 4byte로 가지게 되어 12byte가 됩니다.
### Reference

[C언어 구조체의 메모리 사이즈(크기 계산)](https://blog.naver.com/sharonichoya/220495444611)
