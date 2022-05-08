---
title:  "디자인 패턴 톺아보기 - Composite Pattern"
excerpt: "디자인 패턴 톺아보기 - Composite Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Composite Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 컴포지트 패턴(Composite Pattern) 이란?

GOF 에서 말하는 컴포지트 패턴의 목적은 아래와 같습니다.

> Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

> 부분과 전체의 계층을 표현하기 위해 객체들을 모아 트리 구조로 구성합니다. 사용자로 하여금 개별 객체와 복합 객체를 모두 동일하게 다룰 수 있도록 하는 패턴입니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/composite_pattern.png)

* Component
    * 집합 관계에 정의될 모든 객체에 대한 인터페이스를 정의합니다. 
    * 모든 클래스에 해당하는 인터페이스에 대해서는 공통의 행동을 구현합니다. 
    * 전체 클래스에 속한 요소들을 관리하는 데 필요한 인터페이스를 정의합니다.
    * 순환 구조에서 요소들을 포함하는 전체 클래스로 접근하는 데 필요한 인터페이스를 정의하며, 적절하다면 그 인터페이스를 구현합니다.
* Leaf
    * 가장 말단의 객체, 즉 자식이 없는 객체를 나타냅니다. 객체 합성에 가장 기본이 되는 객체의 행동을 정의합니다.
* Composite
    * 자식이 있는 구성요소에 대한 행동을 정의합니다. 자신이 복합하는 요소들을 저장하면서, Component 인터페이스에 정의된 자식 관련 연산을 구현합니다.
* Client
    * Component 인터페이스를 통해 복합 구조 내의 객체들을 조작합니다. 

### 1.2. 사용 방법

1. 사용자는 복합 구조 내 객체 간의 상호작용을 위해 Component 클래스 인터페이스를 사용합니다.
2. 요청받은 대상이 Leaf 인스턴스이면 자신이 정의한 행동을 직접 수행하고, 대상이 Composite이면 자식 객체들에게 요청을 위임합니다.
3. 위임하기 전후에 다른 처리를 수행할 수도 있습니다.

### 1.3. 장/단점

* Advantages (+)
    * Provides a flexible alternative to subclassing.
* Disadvantages (–)
    * Introduces an additional level of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
    * Implementation is coupled to the abstraction.
* Consider the right design (solution):
    * Implementation is decoupled from the abstraction.

## 2. 컴포지트 패턴(Composite Pattern) 사용예시

컴포지트 패턴은 다음 경우에 사용합니다.

* 부분 전체의 객체 계통을 표현하고 싶을 때
* 사용자가 객체의 합성으로 생긴 복합 객체와 개개의 객체 사이의 차이를 알지 않고도 자기 일을 할 수 있도록 만들고 싶을 때 사용자는 컴포지트의 모든 객체를 똑같이 취급하게 됩니다. 

### 2.1. GOF 패턴

#### 2.1.1. Component

```java
abstract class Component {
	private String name;
	
	public Component(String name) { 
		 this.name = name;
	} 
	
	public abstract String operation();
	
	public String getName() { 
		return name;
	} 
	
	public boolean add(Component child) { 
		return false;
	}
	
	public void remove(Component child) {
		
	}
	
	public Iterator<Component> iterator() {  // null iterator
		return Collections.<Component>emptyIterator();
	} 
}
```

#### 2.1.2. Leaf

```java
class Leaf extends Component { 
	 public Leaf(String name) { 
		 super(name);
	 } 
	 public String operation() { 
	 	return getName();
	 }
} 
```

#### 2.1.3. Composite

```java
class Composite extends Component { 
	private List<Component> children = new ArrayList<Component>();
	
	public Composite(String name) { 
		super(name);
	} 
	
	public String operation() { 
		Iterator<Component> it = children.iterator();
		String str = getName();
		Component child;
		while (it.hasNext()) { 
			child = it.next();
			str += child.operation();
		} 
		return str;
	} 
	
	// Overriding the default implementation.
	@Override
	public boolean add(Component child) { 
		return children.add(child);
	} 
	
	@Override
	public void remove(Component child) { 
		children.remove(children.indexOf(child));
		
	} 
	
	@Override
	public Iterator<Component> iterator() { 
		return children.iterator();
	} 
} 
```

#### 2.1.4. Client

```java
public class Main{
	public static void main(String[] args) {
		Component composite1 = new Composite("Composite1 ");
		Component composite2 = new Composite("Composite2 ");
		
		Leaf leaf1 = new Leaf("Leaf1 ");
		Leaf leaf2 = new Leaf("Leaf2 ");
		Leaf leaf3 = new Leaf("Leaf3 ");
		Leaf leaf4 = new Leaf("Leaf4 ");
		Leaf leaf5 = new Leaf("Leaf5 ");
		
		composite1.add(leaf1);
		composite1.add(leaf2);
		
		composite2.add(leaf3);
		composite2.add(leaf4);
		composite2.add(leaf5);
		
		composite1.add(composite2);
		composite1.remove(leaf2);
		
		System.out.println("(1) " + composite1.operation()); 
		System.out.println("(2) " + composite2.operation()); 
	}
}
```

결과는 아래와 같습니다.

```
(1) Composite1 Leaf1 Composite2 Leaf3 Leaf4 Leaf5 
(2) Composite2 Leaf3 Leaf4 Leaf5 
```

> 참고 자료

* [Composite Pattern](https://en.wikipedia.org/wiki/Composite_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
