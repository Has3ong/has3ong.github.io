---
title:  "디자인 패턴 톺아보기 - Observer Pattern"
excerpt: "디자인 패턴 톺아보기 - Observer Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Observer Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 옵저버 패턴(Observer Pattern) 이란?

GOF 에서 말하는 옵저버 패턴의 목적은 아래와 같습니다.

> Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

> 객체 사이에 일 대 다의 의존 관계를 정의해 두어, 어떤 객체의 상태가 변할 때 그 객체의 의존성을 가진 다른 객체들이 그 변화를 통지받고 자동으로 갱신될 수 있게 만듭니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/observer_pattern.png)

* Subject
  * 감시자들을 알고 있는 주체입니다. 임의 개수의 감시자 객체는 주체를 감시할 수 있습니다. 주체는 감시자 객체를 붙이거나 떼는 데 필요한 인터페이스를 제공합니다.
* Observer
  * 주체에 생긴 변화에 관심 있는 객체를 갱신하는 데 필요한 인터페이스를 정의합니다. 이로써 주체의 변경에 따라 변화되어야 하는 객체들의 일관성을 유지합니다.
* ConcreteSubject
  * ConcreteObserver 객체에게 알려주어야 하는 상태를 저장합니다. 또한 이 상태가 변경될 때 감시자에게 변경을 통보합니다.
* ConcreteObserver
  * ConcreteSubject 객체에 대한 참조자를 관리합니다. 주체의 상태와 일관성을 유지해야 하는 상태를 저장합니다. 주체의 상태와 감시자의 상태를 일관되게 유지하는 데 사용하는 갱신 인터페이스를 구현합니다.

### 1.2. 사용 방법

* ConcreteSubject는 Observer의 상태와 자신의 상태가 달라지는 변경이 발생할 때마다 감시자에게 통보합니다.
* concrete subject에서 변경이 통보된 후, ConcreteObserver는 필요한 정보를 주체에게 질의하여 얻어옵니다. ConcreteObserver는 이 정보를 이용해서 주체의 상태와 자신의 상태를 일치시킵니다.
### 1.3. 장/단점

* Advantages (+)
    * Decouples subject from observers.
    * Makes adding/withdrawing observers easy.
* Disadvantages (–)
    * Can make the update behavior complex.

### 1.4. 고려사항

* Consider the left design (problem):
    * Tight coupling between subject and dependents.
* Consider the right design (solution):
    * Loose coupling between subject and observers.

## 2. 옵저버 패턴(Adapter Pattern) 사용예시

옵저버 패턴은 다음 경우에 사용합니다.

* 어떤 추상 개념이 두 가지 양상을 갖고 하나가 다른 하나에 종속적일 때
* 한 객체에 가해진 변경으로 다른 객체를 변경해야 하고, 프로그래머들은 얼마나 많은 객체들이 변경되어야 하는지 몰라도 될 때
* 어떤 객체가 다른 객체에 자신의 변화를 통보할 수 있는데, 그 변화에 관심 있어 하는 객체들이 누구인지에 대한 가정 없이도 그러한 통보가 될 때

### 2.1. GOF 패턴

#### 2.1.1. Subject

```java
abstract class Subject { 
	private List<Observer> observers = new ArrayList<Observer>();
	
	// Registration interface.
	public void attach(Observer o) { 
		observers.add(o);
	} 
	
	// Notification interface.
	// notify() is already used by the Java Language (to wake up threads).
	public void notifyObservers() { 
		for (Observer o : observers) {
			o.update();
		}
	} 
} 
```

#### 2.1.2. Observer

```java
abstract class Observer { 
	// Synchronizing observer's state with subject's state.
	public abstract void update();
} 
```

#### 2.1.3. ConcreteSubject

```java
class Subject1 extends Subject { 
	private int state = 0;
	
	//
	public int getState() { 
		return state;
	} 
	
	void setState(int state) { 
		this.state = state;
		System.out.println("Subject1 : State changed to : " + state + "\n           Notifying observers ...");
	
		// Notifying observers that state has changed.
		notifyObservers();
	} 
} 
```

#### 2.1.4. ConcreteObserver

```java
class Observer1 extends Observer { 
	private int state;
	private Subject1 subject;
	
	public Observer1(Subject1 subject) { 
		this.subject = subject;
		// Registering this observer on subject.
		subject.attach(this); 
	} 
	
	public void update() { 
		this.state = subject.getState();
		System.out.println("Observer1: State updated to : " + this.state);
	} 
} 

class Observer2 extends Observer { 
	private int state;
	private Subject1 subject;
	
	public Observer2(Subject1 subject) { 
		this.subject = subject;
		// Registering this observer on subject.
		subject.attach(this); 
	} 
	
	public void update() { 
		this.state = subject.getState();
		System.out.println("Observer2: State updated to : " + this.state);
	} 
} 
```

#### 2.1.5. Main

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {

		Subject1 s1 = new Subject1();
		// Creating observers and registering them on subject1.
		Observer o1 = new Observer1(s1);
		Observer o2 = new Observer2(s1);
		
		System.out.println("Changing state of Subject1 ...");
		s1.setState(100);
		
	} 
}
  ```

결과는 아래와 같습니다.

```
Changing state of Subject1 ...
Subject1 : State changed to : 100
           Notifying observers ...
Observer1: State updated to : 100
Observer2: State updated to : 100
```

> 참고 자료

* [Observer Pattern](https://en.wikipedia.org/wiki/Observer_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
