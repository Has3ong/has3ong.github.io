---
title : Sync vs Async / Blocking vs Non-Blocking
tags:
- Synchronous
- Asynchronous
- Blocking
- NonBlocking
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

## Synchronous / Asynchronous

호출되는 함수의 작업완료 여부를 누가 신경쓰냐의 문제입니다.

호출되는 함수에게 callback을 전달해서, 호출되는 함수의 작업이 완료되면 호출되는 함수가 전달받은 callback을 실행하고, 호출하는 함수는 작업 완료 여부를 신경쓰지 않으면 Asynchronous다.

호출하는 함수가 호출되는 함수의 작업 완료 후 리턴을 기다리거나, 또는 호출되는 함수로부터 바로 리턴 받더라도 작업 완료 여부를 호출하는 함수 스스로 계속 확인하며 신경쓰면 Synchronous다.

## Blocking/NonBlocking

Blocking/NonBlocking은 호출되는 함수가 바로 리턴하느냐 마느냐가 관심사다.

호출된 함수가 바로 리턴해서 호출한 함수에게 제어권을 넘겨주고, 호출한 함수가 다른 일을 할 수 있는 기회를 줄 수 있으면 NonBlocking이다.

그렇지 않고 호출된 함수가 자신의 작업을 모두 마칠 때까지 호출한 함수에게 제어권을 넘겨주지 않고 대기하게 만든다면 Blocking이다.

각각의 case에 따라 그림을 그려보면 아래와 같습니다.

![image](https://user-images.githubusercontent.com/44635266/68367180-75116900-0178-11ea-84dd-e9467b233eec.png)

Case마다 실생활 예제를 잘 해논 블로그가 있어서 글의 내용과 주소를 달아놓겠습니다.

[동기와 비동기, 그리고 블럭과 넌블럭](https://musma.github.io/2019/04/17/blocking-and-synchronous.html)

## Case Study

* Blocking & Synchronous

```
나 : 대표님, 개발자 좀 더 뽑아주세요..
대표님 : 오케이, 잠깐만 거기 계세요!
나 : …?!!
대표님 : (채용 공고 등록.. 지원자 연락.. 면접 진행.. 연봉 협상..)
나 : (과정 지켜봄.. 궁금함.. 어차피 내 일 하러는 못 가고 계속 서 있음)
```

* Blocking & Asynchronous

```
나 : 대표님, 개발자 좀 더 뽑아주세요..
대표님 : 오케이, 잠깐만 거기 계세요!
나 : …?!!
대표님 : (채용 공고 등록.. 지원자 연락.. 면접 진행.. 연봉 협상..)
나 : (안 궁금함.. 지나가는 말로 여쭈었는데 붙잡혀버림.. 딴 생각.. 못 가고 계속 서 있음)
```

*Non-blocking & Synchronous

```
나 : 대표님, 개발자 좀 더 뽑아주세요..
대표님 : 알겠습니다. 가서 볼 일 보세요.
나 : 넵!
대표님 : (채용 공고 등록.. 지원자 연락.. 면접 진행.. 연봉 협상..)
나 : 채용하셨나요?
대표님 : 아직요.
나 : 채용하셨나요?
대표님 : 아직요.
나 : 채용하셨나요?
대표님 : 아직요~!!!!!!
```

* Non-blocking & Asynchronous

```
나 : 대표님, 개발자 좀 더 뽑아주세요..
대표님 : 알겠습니다. 가서 볼 일 보세요.
나 : 넵!
대표님 : (채용 공고 등록.. 지원자 연락.. 면접 진행.. 연봉 협상..)
나 : (열일중..)
대표님 : 한 분 모시기로 했습니다~!
나 : 😍
```
