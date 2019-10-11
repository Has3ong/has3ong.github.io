---
title : Stack / Queue
---  

## 스택 (Stack)

![](https://user-images.githubusercontent.com/44635266/66646539-6a3ee380-ec61-11e9-8cfd-63cc6096da35.png)

선형 자료구조의 일종으로 `Last In First Out (LIFO)`. `push()`와 `pop()` 으로 원소를 넣고 뺄 수 있다.

즉, 나중에 들어간 원소가 먼저 나온다. 이것은 Stack 의 가장 큰 특징이다. 차곡차곡 쌓이는 구조로 먼저 Stack 에 들어가게 된 원소는 맨 바닥에 깔리게 된다.

그렇기 때문에 늦게 들어간 녀석들은 그 위에 쌓이게 되고 호출 시 가장 위에 있는 녀석이 호출되는 구조이다.


## 큐 (Queue)

![](https://user-images.githubusercontent.com/44635266/66646540-6a3ee380-ec61-11e9-9a00-b8b020ac70f9.png)

선형 자료구조의 일종으로 `First In First Out (FIFO)`. 즉, 먼저 들어간 놈이 먼저 나온다. `enqueue()`와 `dequeue()`로 원소를 넣고 뺄 수 있다.

Stack 과는 반대로 먼저 들어간 놈이 맨 앞에서 대기하고 있다가 먼저 나오게 되는 구조이다.

참고로 Java Collection 에서 Queue 는 인터페이스이다. 이를 구현하고 있는 Priority queue등을 사용할 수 있다.


### 관련 문제

* Stack 을 사용하여 미로찾기 구현하기
* Queue 를 사용하여 Heap 자료구조 구현하기
* Stack 두 개로 Queue 자료구조 구현하기
* Stack 으로 괄호 유효성 체크 코드 구현하기

