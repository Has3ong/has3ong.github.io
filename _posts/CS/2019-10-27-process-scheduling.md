---
title : Process Scheduling
tags:
- Process
- Scheduling
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

## 프로세스 스케쥴링(Process Scheduling)

CPU를 사용하려고 하는 프로세스들 사이의 우선 순위를 관리하는 일이다. 스케줄링은 처리율과 CPU 이용률을 증가시키고 오버헤드/응답시간/반환시간/대기시간 최소하 시키는 기법이다.

## 프로세스 상태(Process State)

![image](https://user-images.githubusercontent.com/44635266/68083184-75a0bb80-fe69-11e9-984d-d5c977f1f4f3.png)

* 생성 (New) : 프로세스 생성 상태
* 실행 (Running) : 프로세스가 CPU에 할당되어 실행 중인 상태
* 준비 (Ready) : 프로세스가 CPU에 할당되기를 기다리는 상태
* 대기 (Waiting) : 보류(Block)라고도 하며, 프로세스가 입출력이나 이벤트를 기다리는 상태
* 종료 (Terminated) : 프로세스 종료 상태

### 프로세스의 상태 전이

* 승인 (Admitted) : 프로세스 생성이 가능하여 승인됨.
* 스케줄러 디스패치 (Scheduler Dispatch) : 준비 상태에 있는 프로세스 중 하나를 선택하여 실행시키는 것.
* 인터럽트 (Interrupt) : 예외, 입출력, 이벤트 등이 발생하여 현재 실행 중인 프로세스를 준비 상태로 바꾸고, 해당 작업을 먼저 처리하는 것.
* 입출력 또는 이벤트 대기 (I/O or Event wait) : 실행 중인 프로세스가 입출력이나 이벤트를 처리해야 하는 경우, 입출력/이벤트가 모두 끝날 때까지 대기 상태로 만드는 것.
* 입출력 또는 이벤트 완료 (I/O or Event Completion) : 입출력/이벤트가 끝난 프로세스를 준비 상태로 전환하여 스케줄러에 의해 선택될 수 있도록 만드는 것.

## 선점 & 비선점 스케줄링

스케줄링은 적용시점에 따라 비선점형과 선점형으로 나눌 수 있다.

### 선점형 스케줄링(Preemptive Scheduling)

CPU가 어떤 프로세스에 의해 점유 중일 때, 우선 순위가 높은 프로세스가 CPU를 차지할 수 있습니다. 우선 순위가 높은 프로세스를 빠르게 처리해야할 경우 유용. 선점이 일어날 경우, 오버헤드가 발생하며 처리시간을 예측하기 힘듦.

* SRT(Short Remaining Time)
  * 짧은 시간 순서대로 프로세스를 수행한다. 남은 처리 시간이 더 짧은 프로세스가 Ready 큐에 들어오면 그 프로세스가 바로 선점됨. 아래에 소개할 SJF의 선점 버전이라고 할 수 있다.
* RR (Round-Robin)
  * 각 프로세스는 같은 크기의 CPU 시간을 할당 받고 선입선출에 의해 행된다. 할당시간이 너무 크면 선입선출과 다를 바가 없어지고, 너무 작으면 오버헤드가 너무 커진다.

### 비선점형 스케줄링(Non-Preemptive Scheduling)

선점 스케줄링의 경우에는 I/O요청, I/O응답, Interrupt발생, 작업완료 등의 상황에서 스케줄링이 일어날 수 있다. 하지만 비선점 스케줄링의 경우 프로세스가 스스로 CPU를 놓아주는 시점(작업이 완료되는 시점)에만 스케줄링이 일어난다. 

* HRN(Highest response ratio next)
  * 긴 작업과 짧은 작업간의 지나친 불평등을 어느 정도 보완한 기법. 수행시간의 길이와 대기 시간을 모두 고려해 우선순위를 정한다.
  * 우선순위 = (대기시간 + 실행시간)/실행시간
* SJF(Shortest Job First)
  * 큐 안에 있는 프로세스 중 수행시간이 짧은 것을 먼저 수행. 평균 대기 시간을 감소시킨다.
* 우선순위(priority)
  * 프로세스에게 우선순위를 정적, 혹은 동적으로 부여하여 우선순위가 높은 순서대로 처리한다. 동적으로 부여할 경우, 구현이 복잡하고 오버헤드가 많다는 단점이 있으나, 시스템의 응답속도를 증가시킨다.
* FIFO
  * 프로세스들은 Ready큐에 도착한 순서대로 CPU를 할당 받는다. 작업 완료 시간을 예측하기 매우 용이하다. 하지만 덜 중요한 작업이 중요한 작업을 기다리게 할 수도 있다.

## 정적 & 동적 스케줄링

프로세스 우선순위 변동 여부에 따라 구분할 수 있다.

### 정적 스케줄링(Static Scheduling)

프로세스에 부여된 우선순위가 바뀌지 않는다. 고정 우선순위 스케줄링이라고도 한다.

### 동적 스케줄링(Dynamic Scheduling)

스케줄링 과정에서 프로세스의 우선순위를 변동시킨다. 유동 우선순위 스케줄링이라고도 한다.

## 장기 & 중기 & 단기 스케줄링

![image](https://user-images.githubusercontent.com/44635266/68083164-12168e00-fe69-11e9-9225-38cc110ecd2a.png)

### 장기 스케줄링

메모리는 한정되어 있는데 많은 프로세스들이 한꺼번에 메모리에 올라올 경우, 대용량 메모리(일반적으로 디스크)에 임시로 저장된다. 이 pool 에 저장되어 있는 프로세스 중 어떤 프로세스에 메모리를 할당하여 ready queue 로 보낼지 결정하는 역할을 한다.

* 메모리와 디스크 사이의 스케줄링을 담당.
* 프로세스에 memory(및 각종 리소스)를 할당(admit)
degree of Multiprogramming 제어
*메모리에 여러 프로그램이 올라가는 것) 몇 개의 프로그램이 올라갈 것인지를 제어
* 프로세스의 상태 new -> ready(in memory)

cf) 메모리에 프로그램이 너무 많이 올라가도, 너무 적게 올라가도 성능이 좋지 않은 것이다. 참고로 time sharing system 에서는 장기 스케줄러가 없다. 그냥 곧바로 메모리에 올라가 ready * 상태가 된다.

### 중기 스케줄링

* 여유 공간 마련을 위해 프로세스를 통째로 메모리에서 디스크로 쫓아냄 (swapping)
* 프로세스에게서 memory 를 deallocate
* degree of Multiprogramming 제어
* 현 시스템에서 메모리에 너무 많은 프로그램이 동시에 올라가는 것을 조절하는 스케줄러.
* 프로세스의 상태 ready -> suspended

 
### 단기 스케줄링

* CPU 와 메모리 사이의 스케줄링을 담당.
* Ready Queue 에 존재하는 프로세스 중 어떤 프로세스를 running 시킬지 결정.
* 프로세스에 CPU 를 할당(scheduler dispatch)
* 프로세스의 상태
* ready -> running -> waiting -> ready

