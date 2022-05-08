---
title:  "디자인 패턴 톺아보기 - Facade Pattern"
excerpt: "디자인 패턴 톺아보기 - Facade Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Facade Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 퍼사드 패턴(Facade Pattern) 이란?

GOF 에서 말하는 퍼사드 패턴의 목적은 아래와 같습니다.

> Provide an unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

> 한 서브시스템 내의 인터페이스 집합에 대한 획일화된 하나의 인터페이스를 제공하는 패턴으로, 서브시스템을 사용하기 쉽도록 상위 수준의 인터페이스를 정의합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/facade_pattern.png)

* Facade
    * 단순하고 일관된 통합 인터페이스를 제공하며, 서브시스템을 구성하는 어떤 클래스가 어떤 요청을 처리해야 하는지 알고 있으며, 사용자의 요청을 해당 서브시스템 객체에 전달합니다.
* 서브시스템 클래스들(Scanner, Parser, ProgramNode 등)
    * 서브시스템의 기능을 구현하고, Facade 객체로 할당된 작업을 실제로 처리하지만 Facade에 대한 아무런 정보가 없습니다. 즉, 이들에 대한 어떤 참조자도 가지고 있지 않습니다.

### 1.2. 사용 방법

1. 사용자는 Facade에 정의된 인터페이스를 이용해서 서브시스템과 상호작용합니다.
2. 또 Facade는 해당 요청을 서브시스템을 구성하는 적당한 객체에서 전달합니다. 서브시스템을 구성하는 객체가 실제의 요청 처리를 담당하지만 퍼사드는 서브시스템에게 메세지를 전달하기 위해 자신의 인터페이스에 동일한 작업을 정의해야 합니다.
3. 퍼사드를 사용하는 사용자는 서브시스템을 구성하는 객체로 직접 접근하지 않아도 됩니다.

### 1.3. 장/단점

* Advantages (+)
    * Decouples clients from a subsystem.
    * Decouples subsystems.

### 1.4. 고려사항

* Consider the left design (problem):
    * No facade / direct access. Tight coupling between client and subsystem.
* Consider the right design (solution):
    * Working through a facade. Loose coupling between client and subsystem.

## 2. 퍼사드 패턴(Facade Pattern) 사용예시

파서드 패턴은 다음 경우에 사용합니다.

* 복잡한 서브 시스템에 대한 단순한 인터페이스 제공이 필요할 때
* 추상 개념에 대한 구현 클래스와 사용자 사이에 너무 많은 종속성이 존재할 때
* 서브시스템을 계층화시킬 때

### 2.1. GOF 패턴

#### 2.1.1. Facade

```java
abstract class Facade {
	public abstract String operation();	
}

class Facade1 extends Facade {
	private Class1 class1;
	private Class2 class2;
	private Class3 class3;

	public Facade1(Class1 class1, Class2 class2, Class3 class3) { 
		this.class1 = class1;
		this.class2 = class2;
		this.class3 = class3;
	}
	
	public String operation() { 
		return class1.operation() + class2.operation() + class3.operation();
	}
}

class Class1 { 
	public String operation() { 
		return "Class1 ";
	} 
}

class Class2 { 
	public String operation() { 
		return "Class2 ";
	} 
}

class Class3 { 
	public String operation() { 
		return "Class3 ";
	} 
}
```

#### 2.1.2 Main

```java
public class Main{
	public static void main(String[] args) {
		Facade facade = new Facade1 (new Class1(), new Class2(), new Class3());
		System.out.println(facade.operation());
	}
}
```

결과는 아래와 같습니다.

```
Class1 Class2 Class3 
```

> 참고 자료

* [Facade Pattern](https://en.wikipedia.org/wiki/Facade_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
