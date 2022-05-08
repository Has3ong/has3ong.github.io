---
title:  "디자인 패턴 톺아보기 - Decorator Pattern"
excerpt: "디자인 패턴 톺아보기 - Decorator Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Decorator Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 데코레이터 패턴(Decorator Pattern) 이란?

GOF 에서 말하는 데코레이터 패턴의 목적은 아래와 같습니다.

> Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

> 객체에 동적으로 새로운 책임을 추가할 수 있게 합니다. 기능을 추가하려면, 서브 클래스를 생성하는 것보다 융통성 있는 방법을 제공합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/decorator_pattern.png)

* Component
    * 동적으로 추가할 서비스를 가질 가능성이 있는 객체들에 대한 인터페이스
* ConcreteComponent
    * 추가적인 서비스가 실제로 정의되어야 할 필요가 있는 객체
* Decorator
    * Component 객체에 대한 참조자를 관리하면서 Component에 정의된 인터페이스를 만족하도록 인터페이스를 정의
* ConcreteDecorator
    * Component에 새롭게 추가할 서비스를 실제로 구현하는 클래스
    
### 1.2. 사용 방법

1. Decorator는 자신의 Component 객체 쪽으로 요청을 전달합니다. 요청 전달전 및 전달 후에 자신만의 추가 연산을 선택적으로 수행할 수도 있습니다.

### 1.3. 장/단점

* Consider the left design (problem):
    * Extending functionality at compile-time.
    * Explosion of subclasses.
* Consider the right design (solution):
    * Extending functionality at run-time.
    * Recursively nested decorators.

### 1.4. 고려사항

* Advantages (+)
    * Provides a flexible alternative to subclassing.
    * Allows an open-ended number of added functionalities.
    * Simplifies classes.
* Disadvantages (–)
    * Provides no reliability on object identity.

## 2. 데코레이터 패턴(Decorator Pattern) 사용예시

데코레이터 패턴은 다음 경우에 사용합니다.

* 다른 객체에 영향을 주지 않고 개개의 객체에 새로운 책임을 추가하기 위해 사용합니다.
* 제거될 수 있는 책임에 대해 사용합니다.
* 실제 상속으로 서브 클래스를 계속 만드는 방법이 실질적이지 못할 때 사용합니다. 너무 많은 수의 독립된 확장이 가능할 때 모든 조합을 지원하기 위해 이를 상속하고 해결하면 클래스 수가 폭발적으로 많아지게 됩니다. 아니면 클래스 정의가 숨겨지든가, 그렇지 않더라도 서브클래싱을 할 수 없게 됩니다.

### 2.1. GOF 패턴

#### 2.1.1. Component

```java
abstract class Component { 
	 public abstract String operation();    
}
```

#### 2.1.2. ConcreteComponent

```java
class Component1 extends Component {
	public String operation() {
		return "Hello World From Component1";
	}
}
```

#### 2.1.3. Decorator

```java
abstract class Decorator extends Component {
	Component component;
	public Decorator(Component component) {
		this.component = component;
	}
	
	public String operation() {
		return component.operation();
	}
}
```

#### 2.1.4. ConcreteDecorator

```java
class Decorator1 extends Decorator {
	public Decorator1(Component component) {
		super(component);
	}
	
	public String operation() {
		String result = super.operation();
		return addBehavior(result);
	}
	
	private String addBehavior(String result) {
		return "***" + result + "***";
	}
}

class Decorator2 extends Decorator {
	public Decorator2(Component component) {
		super(component);
	}
	
	public String operation() {
		String result = super.operation();
		return addBehavior(result);
	}
	
	private String addBehavior(String result) {
		return "===" + result + "===";
	}
}
```

#### 2.1.5. Main

```java
public class Main{
	public static void main(String[] args) {
		Component component = new Component1();
		System.out.println("(1) " + component.operation());
		
		component = new Decorator1(new Decorator2(component));
		System.out.println("(2) " + component.operation());
	}
}
```

결과는 아래와 같습니다.

```
(1) Hello World From Component1
(2) ***===Hello World From Component1===***
```

> 참고 자료

* [Decorator Pattern](https://en.wikipedia.org/wiki/Decorator_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
