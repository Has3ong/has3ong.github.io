---
title : Virtual Memory
tags:
- Virtual Memory
- Paging
---


## 가상 메모리

다중 프로그래밍을 실현하기 위해서는 많은 프로세스들을 동시에 메모리에 올려두어야 한다. 가상메모리는 프로세스 전체가 메모리 내에 올라오지 않더라도 실행이 가능하도록 하는 기법이며, 프로그램이 물리 메모리보다 커도 된다는 주요 장점이 있다.

### 가상 메모리 개발 배경

실행되는 코드의 전부를 물리 메모리에 존재시켜야 했고, 메모리 용량보다 큰 프로그램은 실행시킬 수 없었다. 또한, 여러 프로그램을 동시에 메모리에 올리기에는 용량의 한계와, 페이지 교체등의 성능 이슈가 발생하게 된다.
또한, 가끔만 사용되는 코드가 차지하는 메모리들을 확인할 수 있다는 점에서, 불필요하게 전체의 프로그램 전체가 메모리에 올라와 있어야 하는게 아니라는 것을 알 수 있다.

#### 프로그램의 일부분만 메모리에 올릴 수 있다면...

* 물리 메모리 크기에 제약받지 않게 된다.
* 더 많은 프로그램을 동시에 실행할 수 있게 된다. 이에 따라 `응답시간`은 유지되고, `CPU 이용률`과 `처리율`은 높아진다.
* swap에 필요한 입출력이 줄어들기 때문에 프로그램들이 빠르게 실행된다.

### 가상 메모리가 하는 일

가상 메모리는 실제의 물리 메모리 개념과 사용자의 논리 메모리 개념을 분리한 것으로 정리할 수 있다. 이로써 작은 메모리를 가지고도 얼마든지 큰 `가상 주소 공간`을 프로그래머에게 제공할 수 있다.

#### 가상 주소 공간

* 한 프로세스가 메모리에 저장되는 논리적인 모습을 가상메모리에 구현한 공간이다.
  프로세스가 요구하는 메모리 공간을 가상메모리에서 제공함으로서 현재 직접적으로 필요치 않은 메모리 공간은 실제 물리 메모리에 올리지 않는 것으로 물리 메모리를 절약할 수 있다.
* 예를 들어, 한 프로그램이 실행되며 논리 메모리로 100KB 가 요구되었다고 하자.
  하지만 실행까지에 필요한 메모리 공간`(Heap영역, Stack 영역, 코드, 데이터)`의 합이 40KB 라면, 실제 물리 메모리에는 40KB 만 올라가 있고, 나머지 60KB 만큼은 필요시에 물리메모리에 요구한다고 이해할 수 있겠다.

| `Stack` | &nbsp;&nbsp;&nbsp; free (60KB) &nbsp;&nbsp;&nbsp;&nbsp; | `Heap` | `Data` | `Code` |
| ------- | ------------------------------------------------------- | :----: | ------ | ------ |


#### 프로세스간의 페이지 공유

가상 메모리는...

* `시스템 라이브러리`가 여러 프로세스들 사이에 공유될 수 있도록 한다.
  각 프로세스들은 `공유 라이브러리`를 자신의 가상 주소 공간에 두고 사용하는 것처럼 인식하지만, 라이브러리가 올라가있는 `물리 메모리 페이지`들은 모든 프로세스에 공유되고 있다.
* 프로세스들이 메모리를 공유하는 것을 가능하게 하고, 프로세스들은 공유 메모리를 통해 통신할 수 있다.
  이 또한, 각 프로세스들은 각자 자신의 주소 공간처럼 인식하지만, 실제 물리 메모리는 공유되고 있다.
* `fork()`를 통한 프로세스 생성 과정에서 페이지들이 공유되는 것을 가능하게 한다.

### Demand Paging(요구 페이징)

프로그램 실행 시작 시에 프로그램 전체를 디스크에서 물리 메모리에 적재하는 대신, 초기에 필요한 것들만 적재하는 전략을 `요구 페이징`이라 하며, 가상 메모리 시스템에서 많이 사용된다. 그리고 가상 메모리는 대개 [페이지](#paging페이징)로 관리된다.
요구 페이징을 사용하는 가상 메모리에서는 실행과정에서 필요해질 때 페이지들이 적재된다. **한 번도 접근되지 않은 페이지는 물리 메모리에 적재되지 않는다.**

프로세스 내의 개별 페이지들은 `페이저(pager)`에 의해 관리된다. 페이저는 프로세스 실행에 실제 필요한 페이지들만 메모리로 읽어 옮으로서, **사용되지 않을 페이지를 가져오는 시간낭비와 메모리 낭비를 줄일 수 있다.**

#### Page fault trap(페이지 부재 트랩)

### 페이지 교체

`요구 페이징` 에서 언급된대로 프로그램 실행시에 모든 항목이 물리 메모리에 올라오지 않기 때문에, 프로세스의 동작에 필요한 페이지를 요청하는 과정에서 `page fault(페이지 부재)`가 발생하게 되면, 원하는 페이지를 보조저장장치에서 가져오게 된다. 하지만, 만약 물리 메모리가 모두 사용중인 상황이라면, 페이지 교체가 이뤄져야 한다.(또는, 운영체제가 프로세스를 강제 종료하는 방법이 있다.)

#### 기본적인 방법

물리 메모리가 모두 사용중인 상황에서의 메모리 교체 흐름이다.

1.  디스크에서 필요한 페이지의 위치를 찾는다
1.  빈 페이지 프레임을 찾는다.
    1.  `페이지 교체 알고리즘`을 통해 희생될(victim) 페이지를 고른다.
    1.  희생될 페이지를 디스크에 기록하고, 관련 페이지 테이블을 수정한다.
1.  새롭게 비워진 페이지 테이블 내 프레임에 새 페이지를 읽어오고, 프레임 테이블을 수정한다.
1.  사용자 프로세스 재시작

#### 페이지 교체 알고리즘

##### FIFO 페이지 교체

가장 간단한 페이지 교체 알고리즘으로 FIFO(first-in first-out)의 흐름을 가진다. 즉, 먼저 물리 메모리에 들어온 페이지 순서대로 페이지 교체 시점에 먼저 나가게 된다는 것이다.

* 장점

  * 이해하기도 쉽고, 프로그램하기도 쉽다.

* 단점
  * 오래된 페이지가 항상 불필요하지 않은 정보를 포함하지 않을 수 있다(초기 변수 등)
  * 처음부터 활발하게 사용되는 페이지를 교체해서 페이지 부재율을 높이는 부작용을 초래할 수 있다.
  * `Belady의 모순`: 페이지를 저장할 수 있는 페이지 프레임의 갯수를 늘려도 되려 페이지 부재가 더 많이 발생하는 모순이 존재한다.

##### 최적 페이지 교체(Optimal Page Replacement)

`Belady의 모순`을 확인한 이후 최적 교체 알고리즘에 대한 탐구가 진행되었고, 모든 알고리즘보다 낮은 페이지 부재율을 보이며 `Belady의 모순`이 발생하지 않는다. 이 알고리즘의 핵심은 `앞으로 가장 오랫동안 사용되지 않을 페이지를 찾아 교체`하는 것이다.
주로 비교 연구 목적을 위해 사용한다.

* 장점

  * 알고리즘 중 가장 낮은 페이지 부재율을 보장한다.

* 단점
  * 구현의 어려움이 있다. 모든 프로세스의 메모리 참조의 계획을 미리 파악할 방법이 없기 때문이다.

##### LRU 페이지 교체(LRU Page Replacement)

`LRU: Least-Recently-Used`  
최적 알고리즘의 근사 알고리즘으로, 가장 오랫동안 사용되지 않은 페이지를 선택하여 교체한다.

* 특징
  * 대체적으로 `FIFO 알고리즘`보다 우수하고, `OPT알고리즘`보다는 그렇지 못한 모습을 보인다.

##### LFU 페이지 교체(LFU Page Replacement)

`LFU: Least Frequently Used`  
참조 횟수가 가장 적은 페이지를 교체하는 방법이다. 활발하게 사용되는 페이지는 참조 횟수가 많아질 거라는 가정에서 만들어진 알고리즘이다.

* 특징
  * 어떤 프로세스가 특정 페이지를 집중적으로 사용하다, 다른 기능을 사용하게되면 더 이상 사용하지 않아도 계속 메모리에 머물게 되어 초기 가정에 어긋나는 시점이 발생할 수 있다
  * 최적(OPT) 페이지 교체를 제대로 근사하지 못하기 때문에, 잘 쓰이지 않는다.

##### MFU 페이지 교체(MFU Page Replacement)

`MFU: Most Frequently Used`  
참조 회수가 가장 작은 페이지가 최근에 메모리에 올라왔고, 앞으로 계속 사용될 것이라는 가정에 기반한다.

* 특징
  * 최적(OPT) 페이지 교체를 제대로 근사하지 못하기 때문에, 잘 쓰이지 않는다.