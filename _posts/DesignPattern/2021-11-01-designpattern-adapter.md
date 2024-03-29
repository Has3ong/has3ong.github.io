---
title:  "디자인 패턴 톺아보기 - Adapter Pattern"
excerpt: "디자인 패턴 톺아보기 - Adapter Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Adapter Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 어댑터 패턴(Adapter Pattern) 이란?

GOF 에서 말하는 어댑터 패턴의 목적은 아래와 같습니다.

> Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

> 클래스의 인터페이스를 사용자가 기대하는 인터페이스 형태로 적응시킵니다. 서로 일치하지 않는 인터페이스를 갖는 클래스들을 함께 동작시킵니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/adapter_pattern.png)

* Target
    사용자가 사용할 응용 분야에 종속적인 인터페이스를 정의하는 클래스입니다.
* Client
    * Target 인터페이스를 만족하는 객체와 동작할 대상입니다.
* Adaptee
    * 인터페이스의 적응이 필요한 기존 인터페이스를 정의하는 클래스로서, 적응대상자라고 합니다. TextView가 예가 될 수 있습니다.
* Adapter
    * Target 인터페이스에 Adaptee의 인터페이스를 적응시키는 클래스입니다.

### 1.2. 사용 방법

1. 사용자는 적응자에 해당하는 클래스의 인스턴스에게 연산을 호출시킵니다.
2. 적응자는 해당 요청을 수행하기 위해 적응 대상자의 연산을 호출시킵니다.

### 1.3. 장/단점

* Advantages (+)
    * Supports reusing existing functionality.
    * Object adapter is more flexible than class adapter.
* Disadvantages (–)

### 1.4. 고려사항

* Consider the left design (problem):
    * No adapter. Clients can not reuse Adaptee.
* Consider the right design (solution):
    * Working through an adapter. Clients can reuse Adaptee.
  
## 2. 어댑터 패턴(Adapter Pattern) 사용예시

어댑터 패턴은 다음 경우에 사용합니다.

* 기존 클래스를 사용하고 싶은데 인터페이스가 맞지 않을 때
* 아직 예측하지 못한 클래스나 실제 관련되지 않는 클래스들이 기존 클래스를 재사용하고자 하지만, 이미 정의된 재사용 가능한 클래스가 지금 요청하는 인터페이스를 꼭 정의하고 있지 않을 때, 다시 말해, 이미 만든 것을 재사용하고자 하나 이 재사용 가능한 라이브러리를 수정할 수 없을 때
* 이미 존재하는 여러 개의 서브클래스를 사용해야 하는데, 이 서브클래스들의 상속을 통해서 이들의 인터페이스를 다 개조한다는 것이 현실성이 없을 때, 객체 적응자를 써서 부모 클래스의 인터페이스를 변형하는 것이 더 바람직함

### 2.1. GOF 패턴

#### 2.1.1. Target

```java
interface Target {
	String operation();
}
class ProductTarget implements Target {
	public String operation() {
		return "Target Class operation Method is Start.";
	}
}
```

#### 2.1.2. Client / Main

```java
public class Main{
	public static void main(String[] args) {
		Target target = new ProductTarget();
		System.out.println(target.operation());
		
		target = new Adapter(new Adaptee());
		System.out.println(target.operation());
	}
}
```

#### 2.1.3. Adaptee

```java
class Adaptee {
	public String specificOperation() {
		return "Adaptee Class specificOperation Method is Start.";
	}
}
```

#### 2.1.4. Adapter

```java
class Adapter implements Target {
	private Adaptee adaptee;
	
	public Adapter(Adaptee adaptee) {
		this.adaptee = adaptee;
	}
	
	public String operation() {
		return adaptee.specificOperation();
	}
}
```

결과는 아래와 같습니다.

```
Target Class operation Method is Start.
Adaptee Class specificOperation Method is Start.
```

> 참고 자료

* [Adapter Pattern](https://en.wikipedia.org/wiki/Adapter_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
