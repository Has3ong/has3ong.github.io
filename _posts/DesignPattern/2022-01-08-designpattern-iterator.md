---
title:  "디자인 패턴 톺아보기 - Iterator Pattern"
excerpt: "디자인 패턴 톺아보기 - Iterator Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Iterator Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 반복자 패턴(Iterator Pattern) 이란?

GOF 에서 말하는 반복자 패턴의 목적은 아래와 같습니다.

> Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

> 내부 표현부를 노출하지 않고 어떤 집합 객체에 속한 원소들을 순차적으로 접근할 수 있는 방법을 제공합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/iterator_pattern.png)

* Iterator
  * 원소를 접근하고 순회하는 데 필요한 인터페이스를 제공합니다.
* ConcreteIterator
  * Iterator에 정의된 인터페이스를 구현하는 클래스로, 순회 과정 중 집합 객체 내에서 현재 위치를 기억합니다.
* Aggregate
  * Iterator 객체를 생성하는 인터페이스를 제공합니다.
* ConcreteAggregate
  * 해당하는 ConcreteIterator의 인스턴스를 반환하는 Iterator 생성 인터페이스를 구현합니다.

### 1.2. 사용 방법

1. ConcreteIterator는 집합 객체 내 현재 객체를 계속 추적하고 다음번 방문할 객체를 결정합니다.

### 1.3. 장/단점

* Advantages (+)
    * Enables simultaneous traversals.
    * Simplifies the aggregate interface.
    * Allows changing the traversal dynamically at run-time.

### 1.4. 고려사항

* Consider the left design (problem):
    * Aggregate responsible for access and traversal.
    * One traversal.
* Consider the right design (solution):
    * Iterator responsible for access and traversal.
    * Multiple traversals.

## 2. 반복자 패턴(Iterator Pattern) 사용예시

반복자 패턴은 다음 경우에 사용합니다.

*  객체 내부 표현방식을 모르고도 집합 객체의 각 원소들에 접근하고 싶을 때
*  집합 객체를 순회하는 다양한 방법을 지원하고 싶을 때
*  서로 다른 집합 객체ㅔ 구조에 대해서도 동일한 방법으로 순회하고 싶을 때

### 2.1. GOF 패턴

#### 2.1.1. Iterator

```java
interface Iterator<E> { 
	E next();
	boolean hasNext();
} 
```

#### 2.1.2. Aggregate

```java
interface Aggregate<E> { 
	// ...
	Iterator<E> createIterator();
	boolean add(E element);
} 
```

#### 2.1.3. ConcreteAggregate / ConcreteIterator

```java
class Aggregate1<E> implements Aggregate<E> {  // E = Type parameter
	// Hiding the representation.
	private Object[] elementData; // represented as object array
	private int idx = 0;
	private int size;

	//
	public Aggregate1(int size) { 
		if (size < 0) {
			throw new IllegalArgumentException("size: " + size);
		}
		this.size = size;
		elementData = new Object[size];
	} 
	
	public boolean add(E element) { 
		if (idx < size) { 
			elementData[idx++] = element;
			return true;
		}  else {
			return false;
		}
	} 
	
	public int getSize() { 
		return size;
	} 
	
	// Factory method for instantiating Iterator1.
	public Iterator<E> createIterator() { 
		return new Iterator1<E>();
	} 
	
	//
	// Implementing Iterator1 as inner class.
	//
	private class Iterator1<E> implements Iterator<E> { 
		// Holds the current position in the traversal.
		private int cursor = 0; // index of next element to return
		//
		public boolean hasNext() { 
			return cursor < size;
		} 
	
		public E next() {  // E = Type of element returned by this method
			if (cursor >= size) {
				throw new NoSuchElementException();
			}
	
			return (E) elementData[cursor++]; // cast from Object to E
		} 
	} 
} 
```

#### 2.1.4. Main

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {
		// Setting up an aggregate.
		Aggregate<String> aggregate = new Aggregate1<String>(3);
		aggregate.add(" ElementA ");
		aggregate.add(" ElementB ");
		aggregate.add(" ElementC ");
		//
		// Creating an iterator.
		Iterator<String> iterator = aggregate.createIterator();
		//
		System.out.println("Traversing the aggregate front-to-back:");
		while (iterator.hasNext()) { 
			System.out.println(iterator.next());
		} 
	}
}
```

결과는 아래와 같습니다.

```
Traversing the aggregate front-to-back:
 ElementA 
 ElementB 
 ElementC 
```

> 참고 자료

* [Iterator Pattern](https://en.wikipedia.org/wiki/Iterator_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
