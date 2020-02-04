---
title : Scala Generic
tags :
- Generic
- Scala
---

## Generic

제네릭 클래스는 타입을 파라미터로 사용하는 클래스다. 특히 제네릭 클래스는 컬렉션 클래스에 유용하다. 제네릭 클래스는 Stack, Queue, Linked list 등과 같은 데이터 구조 구현에 사용될 수 있습니다.

### Generic Class Definition

제네릭 클래스는 대괄호 [] 에 파라미터로 타입을 사용한다. 한 가지 규칙은 타입 파라미터 식별자로 문자 A를 사용하는 것이지만 모든 파라미터 이름이 사용될 수 있다.

> Example

```scala
class Stack[A] {
    private var elements : List[A] = Nil
    def push(x: A) { elements = x :: elements }
    def peek: A = elements.head
    def pop() : A = {
        val currentTop = peek
        elements = elements.tail
        println(currentTop)
        currentTop
    }
}
```

Stack 클래스 구현에서는 모든 타입 A 를 파라미터로 사용한다. 해당 리스트는 A 타입의 엘리먼트만 저장할 수 있다. def push 메소드는 A 타입만 받는다. Stack 클래스를 사용한 스택을 구현하는 예를 보겠습니다.

> Example

```scala
object Scala{
    def main(args: Array[String]) : Unit = {

        val stack = new Stack[Int]
        stack.push(10)
        stack.push(20)
        stack.push(30)
        stack.pop()
        stack.pop()
        stack.pop()

    }
}
```

Result

```
30
20
10
```

Linked List 클래스를 구현에 사용해보겠습니다.

> Example

```scala
class LinkedList[A] {
    private class Node[A] (elem : A) {
        var next : Node[A] = _
        override def toString = elem.toString
    }

    private var head : Node[A] = _

    def add(elem : A) {
        val value = new Node(elem)
        value.next = head
        head = value
    }

    private def printNodes(value : Node[A]) {
        if (value != null) {
            println(value)
            printNodes(value.next)
        }
    }

    def printAll() { printNodes(head) }
}
```

앞에서 만든 클래스를 이용하여 데이터를 다루어 보겠습니다.

```scala
object Scala{
    def main(args: Array[String]) : Unit = {

        val ints = new LinkedList[Int]()

        ints.add(10)
        ints.add(20)
        ints.add(30)
        ints.printAll()

        val strings = new LinkedList[String]()

        strings.add("Scala")
        strings.add("Java")
        strings.add("Python")
        strings.printAll()

        val floats = new LinkedList[Double]()

        floats.add(3.14)
        floats.add(1.72)
        floats.add(1.414)
        floats.printAll()

    }
}
```

Result

```
30
20
10
Python
Java
Scala
1.414
1.72
3.14
```