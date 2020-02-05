---
title : Array / Linked List
tags:
- Array
- Linked List
- Data Structure
---  

## 배열(Array)

배열은 동일한 자료형(Data Type)의 데이터를 연속된 공간에 저장하기 위한 자료구조이다. 즉, 연관된 데이터를 그룹화하여 묶어준다고 생각하면 된다. 

연관된 데이터를 저장하기 위한 변수의 선언을 줄여주며, 반복문 등을 이용하여 계산과 같은 과정을 쉽게 처리할 수 있다.

배열을 구성하는 각각의 값을 배열 `요소(element)`라고 하며, 배열에서의 위치를 가리키는 숫자는 `인덱스(index)`라고 합니다.

C언어에서 인덱스는 언제나 0부터 시작하며, 0을 포함한 양의 정수만을 가질 수 있습니다.


언어마다 다르지만 Java에서 배열 선언 및 사용은 아래와 같이 합니다.

> Example

```
// {'', '', '', '', '', '', ''};
String[] weeks = new String[7]; 
String[] weeks = {"월", "화", "수", "목", "금", "토", "일"};
```

다음과 같이 다 차원 배열도 선언할 수 있습니다.

```
int[][] data = new int[3][4];
```

![](https://user-images.githubusercontent.com/44635266/66618883-e8759880-ec15-11e9-9a57-a4603a2d28c4.png)

## 연결리스트(Linked List)

연결리스트는 각 노드가 데이터와 포인터를 가지고 한 줄로 연결되어 있는 방식의 자료구조입니다. 데이터를 담고 있는 노드들이 연결되어 있고, 노드의 포인터가 이전, 다음 노드와의 연결을 담당합니다.

연결리스트는 3가지 종류가 있습니다.

* 단방향 연결 리스트
* 양방향 연결 리스트
* 원형 연결리스트

![](https://user-images.githubusercontent.com/44635266/66550393-45bf0a80-eb80-11e9-9176-7a97e6270f3e.png)

이중 단방향 연결리스트를 코드화 시키면 아래와 같습니다.

> Example 

```
public class LinkedList {
    private Node head;
    private int size = 0;
    
    private class Node{
        private Object data;
        private Node next;
        public Node(Object input) {
            this.data = input;
            this.next = null;
        }
    }
}
```

양방향 연결리스트 구조는 아래와 같이 prev 를 추가시켜줍니다.

> Example

```
public class LinkedList {
    private Node head;
    private int size = 0;
    
    private class Node{
        private Object data;
        private Node next;
        private Node prev;
        public Node(Object input) {
            this.data = input;
            this.next = null;
            this.prev = null;
        }
    }
}
```

### 연결리스트의 시간복잡도

|       |Search     |Insertion  |Deletion   |Access     |
|-------|-----------|-----------|-----------|-----------|
|Worst  |O(n)       |O(n)       |O(n)       |O(n)       |
|Average|O(n)       |O(n)       |O(n)       |O(n)       |




