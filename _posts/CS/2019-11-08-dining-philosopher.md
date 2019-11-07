---
title : Dining Philosophers Problem
tags:
- 식사하는 철학자
- DeadLock
---  

세마포어와 뮤텍스, DeadLock과 같은 개념을 모르신다면 [프로세스와 스레드](/process-thread)와 [임계영역](/critical-section)포스트를 보고오시면 됩니다.

## 식사하는 철학자 문제

![image](https://user-images.githubusercontent.com/44635266/68369600-09ca9580-017e-11ea-8f58-7c83fe50e3a6.png)

철학자들은 생각하거나, 밥을먹거나, 배가고프거나 3가지 상태를 가질 수 있다. 철학자들은 밥을 먹을때 왼쪽 포크와 오른쪽 포크를 각 손에 하나씩 들어야 식사를 할 수 있다. 하지만 사람이 5명인데 포크는 5개밖에 없다. 그래서 최대 2명만 동시에 밥을 먹을 수 있다.

프로세스가 어떤 공유자원(여기선 포크)을 가지고 아무한테도 주지 않으면서 다른 프로세스의 공유자원을 달라고 요구하게 되면 데드락이 발생 할 수 있다. 이것을 해결하기 위해서 세마포어를 사용해야 한다.

mutex라는 이진 세마포어를 활용해서 포크를 손에 쥐는 행위를 하는것을 한 시점에 한 사람만 가능하게끔 해주고 각 프로세스 별로 세마포어를 또 따로 두어서 최대 2명까지 식사를 하게끔 해주어야 한다.

### 해결방법

철학자들이 동시에 오른쪽 포크를 집어든 후 DeadLock이 발생하는 조건은 아래와 같습니다.

1. 철학자들은 포크를 공유할 수 없고(상호 배제)
2. 자신의 왼쪽에 앉은 철학자가 포크를 놓을 때까지 기다린다.(점유 대기)
3. 철학자들은 왼쪽 철학자의 포크를 빼앗을 방법도 없으며,(선점 불가) 
4. 각 철학자들은 자신의 왼쪽 철학자의 포크를 대기한다.(순환대기)

그래서 나온 완벽한 해결책은 2번과 4번을 제거한것이다. 

한번에 포크를 하나만 들 수 있게 하는게 아니라 동시에 왼쪽 오른쪽 포크를 들게 한다. 

그리고 나서 각 프로세스마다 세마포어를 하나씩 두게 한다. 동시에 2개의 포크를 들게 한다는것은 점유대기를 없앤다는것이다.

이렇게 하면 오른쪽 포크를 든 상태에서 왼쪽 프로세스의 포크를 얻을때 까지 기다리는 점유대기가 사라진다.

동시에 2개의 포크를 들면 또 다른 포크를 얻기 위해서 기다리는 일이 없어진다. 따라서 점유대기가 사라진다.(2번제거) 또한 각 프로세스는 자기가 포크를 들었으면 또 포크를 달라고 요구하지 않으므로 덩달아 순환대기도 제거 된다. (데드락은 포크를 2개 동시에 드는 행위로 제거 되었다.)

만약에 각 프로세스별로 세마포어가 없고 이진 세마포어로 포크를 들고 내려놓는 행위가 한번에 한 프로세스만 가능하게끔 해놨다고 가정해보자.

그렇게 될 경우 1번 프로세스가 포크를 들었을때 0번과 2번 프로세스가 take_forks를 호출하게 되면 아무일도 없이 함수 호출이 끝나게 된다.

그렇게 되면 eating()을 할꺼고 put_forks()를 차례로 호출하게 될텐데, 사실 1번 프로세스가 먹고있는 와중에 0번과 2번은 포크를 집을 수 없게 되서 1번이 식사를 마칠때까지 블락되어야 한다. 

그래서 각 프로세스별로 세마포어를 따로 두어서 1번이 식사중일때 양옆은 1번이 식사를 끝낼때 까지 기다리게끔 한 것이다.


> Source Code (references / https://www.geeksforgeeks.org/)

```
#include <pthread.h> 
#include <semaphore.h> 
#include <stdio.h> 
  
#define N 5 
#define THINKING 2 
#define HUNGRY 1 
#define EATING 0 
#define LEFT (phnum + 4) % N 
#define RIGHT (phnum + 1) % N 
  
int state[N]; 
int phil[N] = { 0, 1, 2, 3, 4 }; 
  
sem_t mutex; 
sem_t S[N]; 
  
void test(int phnum) 
{ 
    if (state[phnum] == HUNGRY 
        && state[LEFT] != EATING 
        && state[RIGHT] != EATING) { 
        // state that eating 
        state[phnum] = EATING; 
  
        sleep(2); 
  
        printf("Philosopher %d takes fork %d and %d\n", 
                      phnum + 1, LEFT + 1, phnum + 1); 
  
        printf("Philosopher %d is Eating\n", phnum + 1); 
  
        // sem_post(&S[phnum]) has no effect 
        // during takefork 
        // used to wake up hungry philosophers 
        // during putfork 
        sem_post(&S[phnum]); 
    } 
} 
  
// take up chopsticks 
void take_fork(int phnum) 
{ 
  
    sem_wait(&mutex); 
  
    // state that hungry 
    state[phnum] = HUNGRY; 
  
    printf("Philosopher %d is Hungry\n", phnum + 1); 
  
    // eat if neighbours are not eating 
    test(phnum); 
  
    sem_post(&mutex); 
  
    // if unable to eat wait to be signalled 
    sem_wait(&S[phnum]); 
  
    sleep(1); 
} 
  
// put down chopsticks 
void put_fork(int phnum) 
{ 
  
    sem_wait(&mutex); 
  
    // state that thinking 
    state[phnum] = THINKING; 
  
    printf("Philosopher %d putting fork %d and %d down\n", 
           phnum + 1, LEFT + 1, phnum + 1); 
    printf("Philosopher %d is thinking\n", phnum + 1); 
  
    test(LEFT); 
    test(RIGHT); 
  
    sem_post(&mutex); 
} 
  
void* philospher(void* num) 
{ 
  
    while (1) { 
  
        int* i = num; 
  
        sleep(1); 
  
        take_fork(*i); 
  
        sleep(0); 
  
        put_fork(*i); 
    } 
} 
  
int main() 
{ 
  
    int i; 
    pthread_t thread_id[N]; 
  
    // initialize the semaphores 
    sem_init(&mutex, 0, 1); 
  
    for (i = 0; i < N; i++) 
  
        sem_init(&S[i], 0, 0); 
  
    for (i = 0; i < N; i++) { 
  
        // create philosopher processes 
        pthread_create(&thread_id[i], NULL, 
                       philospher, &phil[i]); 
  
        printf("Philosopher %d is thinking\n", i + 1); 
    } 
  
    for (i = 0; i < N; i++) 
  
        pthread_join(thread_id[i], NULL); 
} 
```

