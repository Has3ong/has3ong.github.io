---
title : Apache vs Nginx
tags :
- Apache
- Nginx
---

## Apache

Apache 서버는 요청 하나 당 프로세스(또는 쓰레드)가 처리하는 구조입니다. 즉 요청이 많을수록 CPU와 메모리 사용이 증가하기 때문에 성능 저하가 있을 수 있습니다. 또한 Apache 서버의 프로세스가 블록킹( blocking )이 되면 요청을 처리하지 못하고, 처리가 완료 될 때까지 계속 대기하는 일이 발생합니다.

![](https://user-images.githubusercontent.com/44635266/67272766-21581c00-f4f8-11e9-9e78-97af5947027d.png)

동시 접속 요청이 10,000 개라면 그 만큼 Process or Thread 생성 비용이 들 것이고 대용량 요청을 처리할 수 있는 웹서버로서의 한계를 드러내게 된다.

이와 같은 문제들은 Keep Alive를 활성화 함으로써 해결이 가능하지만, Keep Alive 때문에 대량 접속 시 효율이 급격하게 떨어지는 또 다른 문제점이 발생합니다.

### Keep Alive

![](https://user-images.githubusercontent.com/44635266/67273091-be1ab980-f4f8-11e9-8f6a-c0a51e1ac77f.png)

HTTP 프로토콜의 특성상 한 번 통신이 이루어지면 접속을 끊어 버리지만, KeepAlive On 상태에서는 KeepAliveTimeOut 시간 동안 접속을 끊지 않고 다음 접속을 기다립니다.

즉, 한 번 연결된 클라이언트와 통신을 유지하고 있기 때문에, 다음 통신 시에 Connection을 생성하고 끊는 작업이 필요 없게 됩니다.

따라서 Keep Alive을 활성화 함으로써, 성능 향상을 기대 할 수 있습니다. 하지만, 프로세스 수가 기하급수적으로 늘어나 MaxClient값을 초과하게 됩니다.

따라서 메모리를 많이 사용하게 되며 이는 곧 성능 저하의 원인이 됩니다. ( 대량 접속 시 효율이 떨어짐 )

## Nginx

Apache 서버와 비교하여 큰 특징이라면 `Event Driven` 방식을 꼽을수 있을것 같다. `Event Driven`은 한 개 또는 고정된 프로세스만 생성 하고, 그 프로세스 내부에서 비 동기 방식으로 효율적으로 작업들을 처리한다. 따라서 동시 접속 요청이 많아도 Process 또는 Thread 생성 비용이 존재하지 않는다.

![](https://user-images.githubusercontent.com/44635266/67272661-ee158d00-f4f7-11e9-999d-b08153ef31ff.png)

그러다보니 프로세스를 fork하거나 쓰레드를 사용하는 아파치와는 달리 CPU와 관계없이 모든 IO들을 전부 Event Listener로 미루기 때문에 흐름이 끊기지 않고 응답이 빠르게 진행이 되어 1개의 프로세스로 더 빠른 작업이 가능하게 될수 있다. 이때문에 메모리적인 측면에서 Nginx가 System Resource를 적게 처리한다는 장점이 있다고 한다.
