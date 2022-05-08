---
title:  "디자인 패턴 톺아보기 - State Pattern"
excerpt: "디자인 패턴 톺아보기 - State Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - State Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 상태 패턴(State Pattern) 이란?

GOF 에서 말하는 상태 패턴의 목적은 아래와 같습니다.

> Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

> 객체의 내부 상태에 따라 스스로 행동을 변경할 수 있게 허가하는 패턴으로, 이렇게 하면 객체는 마치 자신의 클래스를 바꾸는 것처럼 보입니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/state_pattern.png)

* Context
  * 사용자가 관심 있는 인터페이스를 정의합니다. 객체의 현재 상태를 정의한 ConcreteState 서브클래스의 인스턴스를 유지/관리합니다.
* State
  * Context의 각 상태별로 필요한 행동을 캡슐화하여 인터페이스로 정의합니다.
* ConcreteState
  * 각 서브 클래스들은 Context의 상태에 따라 처리되어야 할 실제 행동을 구현합니다.

### 1.2. 사용 방법

* 상태에 따라 다른 요청을 받으면 Context 클래스는 현재의 ConcreteState 객체로 전달합니다. 이 ConcreteState 클래스의 객체는 State 클래스를 상속하는 서브클래스들 중 하나의 인스턴스일 것입니다.
* Context 클래스는 실제 연산을 처리할 State 객체에 자신을 매개변수로 전달합니다. 이로써 State 객체는 Context 클래스에 정의된 정보에 접근할 수 있게 됩니다.
* Context 클래스는 사용자가 사용할 수 있는 기본 인터페이스를 제공합니다. 사용자는 상태 객체를 Context 객체와 연결시킵니다. 즉, Context 클래스에 현재 상태를 정의합니다. 이렇게 Context 객체를 만들고 나면 사용자는 더는 State 객체를 직접 다루지 않고 Context 객체에 요청을 보내기만 하면 됩니다.
* Context 클래스 또는 ConcreteState 서브클래스들은 자기 다음의 상태가 무엇이고, 어떤 환경에서 다음 상태로 가는지 결정할 수 있습니다. 즉, 상태는 상태 전이의 규칙이 있으므로, 각각 한 상태에서 다른 상태로 전이하는 규칙을 알아야 합니다.

### 1.3. 장/단점

* Advantages (+)
    * Makes adding new states easy.
    * Avoids conditional statements for switching between states.
    * Ensures consistent states.
    * Makes state transitions explicit.
* Disadvantages (–)
    * May require extending the Context interface.
    * Introduces an additional level of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired state-specific behavior.   
    * Conditional statements required.
    * Complicated class.
* Consider the right design (solution):
    * Encapsulated state-specific behavior.
    * No conditional statements required.
    * Simplified class.

## 2. 상태 패턴(State Pattern) 사용예시

상태 패턴은 다음 경우에 사용합니다.

* 객체의 행동이 상태에 따라 달라질 수 있고, 객체의 상태에 따라 런타임에 행동이 바뀌어야 할 때
* 어떤 연산에 그 객체의 상태에 따라 달라지는 다중 분기 조건 처리가 너무 많이 들어 있을 때

### 2.1. GOF 패턴

#### 2.1.1. Context

```java
class Context { 
	private State state; // reference to the current State object

	public Context(State state) {  
			this.state = state;
	} 

	public String operation() { 
		return "Context: Delegating state-specific behavior to the current State object.\n"  + state.operation(this);
	} 

	void setState(State state) {  // package private
		this.state = state;
	} 
} 
```

#### 2.1.2. State

```java
interface State { 
	String operation(Context context);
} 
```

#### 2.1.3. ConcreteState

```java
class State1 implements State { 
	// Implemented as Singleton.
	private static final State1 INSTANCE = new State1();
	private State1() { } 

	public static State1 getInstance() { 
		return INSTANCE;
	} 
   
	public String operation(Context context) { 
		String result = "    State1 : Hello World1!" + " Changing current state of Context to State2.";
		context.setState(State2.getInstance()); // state transition 
		return result;
	} 
} 


class State2 implements State { 
	// Implemented as Singleton.
	private static final State2 INSTANCE = new State2();
	private State2() { } 
	
	public static State2 getInstance() { 
		return INSTANCE;
	} 

	public String operation(Context context) { 
		String result = "    State2 : Hello World2!" + " Changing current state of Context to State1.";
		context.setState(State1.getInstance()); // state transition
		return result;
	} 
} 
```

#### 2.1.4. Main

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {

		// Creating a Context object 
		// and configuring it with the initial State1 object.
		Context context = new Context(State1.getInstance());
		// Calling an operation on context.
		System.out.println("(1) " + context.operation());    
		// Calling the operation again.
		System.out.println("(2) " + context.operation());
		
	} 
}
```

결과는 아래와 같습니다.

```
(1) Context: Delegating state-specific behavior to the current State object.
    State1 : Hello World1! Changing current state of Context to State2.
(2) Context: Delegating state-specific behavior to the current State object.
    State2 : Hello World2! Changing current state of Context to State1.
```

> 참고 자료

* [State Pattern](https://en.wikipedia.org/wiki/State_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
