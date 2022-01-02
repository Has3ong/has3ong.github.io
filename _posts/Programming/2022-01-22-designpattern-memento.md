---
title:  "디자인 패턴 톺아보기 - Memento Pattern"
excerpt: "디자인 패턴 톺아보기 - Memento Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Memento Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 메멘토 패턴(Memento Pattern) 이란?

GOF 에서 말하는 메멘토 패턴의 목적은 아래와 같습니다.

> Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.
 
> 캡슐화를 위배하지 않은 채 어떤 객체의 내부 상태를 잡아내고 실체화시켜 둠으로서, 이후 객체가 그 상태로 되돌아올 수 있도록 합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/memento_pattern.png)

* Memento
  * 원조본 객체의 내부 상태를 저장합니다. 메멘토는 원조 본 객체의 내부 상태를 필요한 만큼 저장해 둡니다. 메멘토는 원조본 객체를 제외한 다른 객체는 자신에게 접근할 수 없도록 막습니다.
  * 그래서 Memento 클래스에는 사실상 두 종류의 인터페이스가 있습니다. 관리 책임을 갖는 Caretaker 클래스는 Memento에 대한 제한 범위 인터페이스만을 볼 수 있습니다. 즉 Caretaker는 메멘토를 다른 객체에게 넘겨줄 수만 있습니다.
  * 이와 반대로 Originator 클래스에게는 광범위 인터페이스가 보입니다. 즉, 자신의 상태를 이전 상태로 복원하기 위해 필요한 모든 자료에 접근하게 해 주는 인터페이스입니다. 이상적으로는 메멘토를 생성하는 원조본 객체만이 메멘토의 내부 상태에 접근할 수 있는 권한을 갖습니다.
* Originator
  * 원조본 객체입니다. 메멘토를 생성하여 현재 객체의 상태를 저장하고 메멘토를 사용하여 내부 상태를 복원합니다.
* Caretaker
  * 메멘토의 보관을 책임지는 보관자입니다. 메멘토의 내용을 검사하거나 그 내용을 건드리지는 않습니다.

### 1.2. 사용 방법

1. 보관자 객체는 원조본 객체에 메멘토 객체를 요청합니다. 또 요청한 시간을 저장하며, 받은 메멘토 객체를 다시 원조본 객체에게 돌려줍니다.
2. 보관자 객체는 메멘토 객체를 원조본 객체에 전달하지 않을 수도 있습니다. 원조본 객체가 이전 상태로 돌아갈 필요가 없을 때는 전달할 필요가 없기 때문입니다.
3. 메멘토 객체는 수동적입니다. 메멘토 객체를 생성한 원조본 객체만이 상태를 설정하고 읽어올 수 있습니다.

### 1.3. 장/단점

* Advantages (+)
    * Preserves encapsulation.
* Disadvantages (–)
    * May introduce run-time costs.

### 1.4. 고려사항

* Consider the left design (problem):
    * Originator's internal state can't be saved. 
* Consider the right design (solution):
    * Originator's internal state can be saved.

## 2. 메멘토 패턴(Memento Pattern) 사용예시

메멘토 패턴은 다음 경우에 사용합니다.

* 어떤 객체의 상태에 대한 스냅샷을 저장한 후 나중에 이 상태로 복구해야 할 때
* 상태를 얻는 데 필요한 직접적인 인터페이스를 두면 그 객체의 구현 세부사항이 드러날 수 밖에 없고, 이것으로 객체의 캡슐화가 깨질 때

### 2.1. GOF 패턴

#### 2.1.1. Memento / Originator

```java
class Originator { 
	// Hiding internal state.
	private String state;
	
	// ...
	// Saving internal state.
	public Memento createMemento() { 
		Memento memento = new Memento();
		memento.setState(state);
		return memento;
	} 
	
	// Restoring internal state.
	void restore(Memento memento) { 
		state = memento.getState();
	} 
	
	//
	public String getState() { 
		return state;
	} 
	
	void setState(String state) { 
		this.state = state;
	} 
	
	//
	// Implementing Memento as inner class.
	// All members are private and accessible only by originator.
	//
	public class Memento { 
		// Storing Originator's internal state.
		private String state;
	
		// ...
		private String getState() { 
			return state;
		} 
		
		private void setState(String state) { 
			this.state = state;
		} 
	} 
} 
```

#### 2.1.2. Caretaker

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {

		Originator originator = new Originator();
		Originator.Memento memento; // Memento is inner class of Originator
		
		// List of memento objects.  
		List<Originator.Memento> mementos = new ArrayList<Originator.Memento>();
		
		originator.setState("A"); 
		
		// Saving state.
		memento = originator.createMemento(); 
		mementos.add(memento); // adding to list
		System.out.println("(1) Saving current state ...... : " + originator.getState());
		
		originator.setState("B"); 
		// Saving state.
		memento = originator.createMemento(); 
		mementos.add(memento); // adding to list
		System.out.println("(2) Saving current state ...... : " + originator.getState());
		
		// Restoring to previous state.
		memento = mementos.get(0); // getting previous (first) memento from the list 
		originator.restore(memento);
		System.out.println("(3) Restoring to previous state : " + originator.getState());
		
	} 
}
```

결과는 아래와 같습니다.

```
(1) Saving current state ...... : A
(2) Saving current state ...... : B
(3) Restoring to previous state : A
```

> 참고 자료

* [Memento Pattern](https://en.wikipedia.org/wiki/Memento_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
