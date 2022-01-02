---
title:  "디자인 패턴 톺아보기 - Strategy Pattern"
excerpt: "디자인 패턴 톺아보기 - Strategy Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Strategy Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 전략 패턴(Strategy Pattern) 이란?

GOF 에서 말하는 전략 패턴의 목적은 아래와 같습니다.

> Define a family of algorithms, encapsulate each one, and make them interchange­able. Strategy lets the algorithm vary independently from clients that use it.

> 동일 계열의 알고리즘 군을 정의하고, 각 알고리즘을 캡슐화하며, 이들을 상호교환이 가능하도록 만듭니다. 알고리즘을 사용하는 클라이언트와 상관없이 독립적으로 알고리즘을 다양하게 변경할 수 있게 합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/strategy_pattern.png)

* Strategy
  * 제공하는 모든 알고리즘에 대한 공통의 연산들을 인터페이스로 정의합니다. Context 클래스는 ConcreteStrategy 클래스에 정의한 인터페이스를 통해서 실제 알고리즘을 사용합니다.
* ConcreteStrategy
  * Strategy 인터페이스를 실제 알고리즘으로 구현합니다.
* Context
  * ConcreteStrategy 객체를 통해 구성됩니다. 즉, Strategy 객체에 대한 참조자를 관리하고, 실제로는 Strategy 서브클래스의 인스턴스를 갖고 있음으로써 구체화합니다. 또한 Strategy 객체가 자료에 접근해가는 데 필요한 인터페이스를 정의합니다.

### 1.2. 사용 방법

1. Strategy 클래스와 Context 클래스는 의사교환을 통해 선택한 알고리즘을 구현합니다. 즉, Context 클래스는 알고리즘에 해당하는 연산이 호출되면, 알고리즘 처리에 필요한 모든 데이터를 Strategy 클래스로 보냅니다. 이때, Context 객체 자체를 Strategy 연산에다가 인자로 전송할 수도 있습니다.
2. Context 클래스는 사용자 쪽에소 온 요청을 각 전략 객체로 전달합니다. 이를 위해 사용자는 필요한 알고리즘에 해당하는 ConcreteStrategy 객체를 생성하여 이를 Context 클래스에 전송하는데, 이 과정을 거치면 사용자는 Context 객체와 동작할 때 전달한 ConcreteStrategy 객체와 함께 동작합니다. 사용자가 선택할 수 있는 동일 계열의 ConcreteStrategy 클래스 군이 준비될 때가 자주 있습니다.

### 1.3. 장/단점
* Advantages (+)
  * Avoids compile-time implementation dependencies.
  * Provides a flexible alternative to subclassing.
  * Avoids conditional statements for switching between algorithms.
* Disadvantages (-)
  * Can make the common Strategy interface complex.
  * Requires that clients understand how strategies differ.
  * Introduces an additional level of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
  * Hard-wired algorithms.
  * Conditional statements required.
  * Complicated classes.
* Consider the right design (solution):
  * Encapsulated algorithms.
  * No conditional statements required.
  * Simplified classes.

## 2. 전략 패턴(Strategy Pattern) 사용예시

전략 패턴은 다음 경우에 사용합니다.

* 행동들이 조금씩 다를 뿐 개념적으로 관련된 많은 클래스들이 존재할 때
* 알고리즘의 변형이 필요할 때
* 사용자가 몰라야 하는 데이터를 사용하는 알고리즘이 있을 때
* 하나의 클래스가 많은 행동을 정의하고, 이런 행동들이 그 클래스의 연산 안에서 복잡한 다중 조건문의 모습을 취할 때

### 2.1. GOF 패턴

#### 2.1.1. Strategy

```java
interface Strategy { 
	int algorithm();
}
```

#### 2.1.2. ConcreteStrategy

```java
class Strategy1 implements Strategy { 
	public int algorithm() { 
		// Implementing the algorithm.
		return 1; // return result
	} 
} 

class Strategy2 implements Strategy { 
	public int algorithm() {
		// Implementing the algorithm.
		return 2; // return result
	} 
} 
```

#### 2.1.3. Context

```java
class Context { 
	private Strategy strategy;

	public Context(Strategy strategy) { 
		this.strategy = strategy;
	} 

	public String operation() { 
		return "Context: Delegating an algorithm to a strategy: Result = " + strategy.algorithm();
	} 
	
	public void setStrategy(Strategy strategy) { 
		this.strategy = strategy;
	} 
} 
```

#### 2.1.4. Main

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {
		// Creating a Context object 
		// and configuring it with a Strategy1 object.
		Context context = new Context(new Strategy1());
		
		// Calling an operation on context.
		System.out.println("(1) " + context.operation());
		
		// Changing context's strategy.
		context.setStrategy(new Strategy2());
		System.out.println("(2) " + context.operation());
	} 
}
```

결과는 아래와 같습니다.

```
(1) Context: Delegating an algorithm to a strategy: Result = 1
(2) Context: Delegating an algorithm to a strategy: Result = 2
```

> 참고 자료

* [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
