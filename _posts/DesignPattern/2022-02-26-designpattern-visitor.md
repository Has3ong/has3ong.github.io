---
title:  "디자인 패턴 톺아보기 - Visitor Pattern"
excerpt: "디자인 패턴 톺아보기 - Visitor Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Visitor Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 방문자 패턴(Visitor Pattern) 이란?

GOF 에서 말하는 방문자 패턴의 목적은 아래와 같습니다.

> Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

> 객체 구조를 이루는 원소에 대해 수행할 연산을 표현합니다. 연산을 적용할 원소의 클래스를 변경하지 않고도 새로운 연산을 정의할 수 있게 합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/visitor_pattern.png)

* Visitor
  * 객체 구조 내에 있는 각 ConcreteElement 클래스를 위한 Visit() 연산을 선언합니다. 연산의 이름과 인터페이스 형태는 Visit() 요청을 방문자에게 보내는 클래스를 식별합니다. 이로써 방문자는 방문된 원소의 구체 클래스를 결정할 수 있습니다. 그러고 나서 방문자는 그 원소가 제공하는 인터페이스를 통해 원소에 직접 접근할 수 있습니다.
* ConcreteVisitor
  * Visitor 클래스에 선언된 연산을 구현합니다. 각 연산은 구조 내에 있는 객체의 대응 클래스에 정의된 일부 알고리즘을 구현합니다. ConcreteVisitor 클래스는 알고리즘이 운영될 수 있는 상황 정보를 제공하며 자체 상태를 저장합니다. 이 상태는 객체 구조를 순회하는 도중 순회 결과를 누적할 때가 많습니다.
* Element
  * 방문자를 인자로 받아들이는 Accept() 연산을 정의합니다.
* ConcreteElement
  * 인자로 방문자 객체를 받아들이는 Accept() 연산을 구현합니다.
* ObjectStructure
  * 객체 구조 내의 원소들을 나열할 수 있습니다. 방문자가 이 원소에 접근하게 하는 상위 수준 인터페이스를 제공합니다. Object-Structure는 Composite 패턴으로 만든 복합체일 수도 있고, 리스트나 집합 등 컬렉션일 수도 있습니다.

### 1.2. 사용 방법

1. 방문자 패턴을 사용하는 사용자는 ConcreteVisitor 클래스의 객체를 생성하고 객체 구조를 따라서 각 원소를 방문하여 순회해야 합니다.
2. 구성 원소들을 방문할 때, 구성 원소는 해당 클래스의 Visitor 연산을 호출합니다. 이 원소들은 자신을 Visitor 연산에 필요한 인자로 제공하여 방문자 자신의 상태에 접근할 수 있도록 합니다.

### 1.3. 장/단점

* Advantages (+)
    * Makes adding new operations easy.
    * Enables visiting elements of different types across inheritance hierarchies.
    * Makes accumulating state easy.
* Disadvantages (–)
    * Requires extending the visitor interface to support new element classes.
    * May require extending the element interfaces.
    * Introduces additional levels of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
    * New operations are distributed across the Element classes.
* Consider the right design (solution):
    * New operations are encapsulated in a separate Visitor class.

## 2. 방문자 패턴(Visitor Pattern) 사용예시

방문자 패턴은 다음 경우에 사용합니다.

* 다른 인터페이스를 가진 클래스가 객체 구조에 포함되어 있으며, 구체 클래스에 따라 달라진 연산을 이들 클래스의 객체에 대해 수행하고자 할 때
* 각각 특징이 있고, 관련되지 않은 많은 연산이 한 객체 구조에 속해있는 객체들에 대해 수행할 필요가 있으며, 연산으로 클래스들을 더럽히고 싶지 않을 때
* 객체 구조를 정의한 클래스는 거의 변하지 않지만, 전체 구조에 걸쳐 새로운 연산을 추가하고 싶을 때

### 2.1. GOF 패턴

#### 2.1.1. Visitor

```java
abstract class Visitor { 
	public abstract void visitElementA(ElementA e);
	public abstract void visitElementB(ElementB e);
}
```

#### 2.1.2. ConcreteVisitor

```java
class Visitor1 extends Visitor {
	public void visitElementA(ElementA element) { 
		System.out.println("Visitor1: Visiting (doing something on) ElementA.\n" + element.operationA());
	} 
	
	public void visitElementB(ElementB element) { 
		System.out.println("Visitor1: Visiting (doing something on) ElementB.\n" + element.operationB());
	}
}
```

#### 2.1.3. Element

```java
abstract class Element {
	public abstract void accept(Visitor visitor);
}
```

#### 2.1.4. ConcreteElement

```java
class ElementA extends Element {
	public void accept(Visitor visitor) { 
		visitor.visitElementA(this);
	} 
	
	public String operationA() { 
		return "Hello World from ElementA!";
	} 
}

class ElementB extends Element {
	public void accept(Visitor visitor) { 
		visitor.visitElementB(this);
	} 
	
	public String operationB() { 
		return "Hello World from ElementN!";
	} 
}
```

#### 2.1.5. Main

```java
public class Main{
	public static void main(String[] args) {
		// Setting up an object structure.
		List<Element> elements = new ArrayList<Element>();
		elements.add(new ElementA());
		elements.add(new ElementB());
		
		// Creating a Visitor1 object.
		Visitor visitor = new Visitor1();
		
		// Traversing the object structure and
		// calling accept(visitor) on each element.
		for (Element element : elements) { 
			element.accept(visitor);
		}
	}
}
```

결과는 아래와 같습니다.

```
Visitor1: Visiting (doing something on) ElementA.
Hello World from ElementA!
Visitor1: Visiting (doing something on) ElementB.
Hello World from ElementN!
```

> 참고 자료

* [Visitor Pattern](https://en.wikipedia.org/wiki/Visitor_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
