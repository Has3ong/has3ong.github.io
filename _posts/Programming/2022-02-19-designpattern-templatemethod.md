---
title:  "디자인 패턴 톺아보기 - Template Method Pattern"
excerpt: "디자인 패턴 톺아보기 - Template Method Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Template Method Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 템플릿 메소드 패턴(Template Method Pattern) 이란?

GOF 에서 말하는 템플릿 메소드 패턴의 목적은 아래와 같습니다.

> Define the skeleton of an algorithm in an operation, deferring some steps to sub­classes. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

> 객체의 연산에는 알고리즘의 뼈대만을 정의하고 각 단계에서 수행할 구체적 처리는 서브클래스 쪽으로 미룹니다. 알고리즘의 구조 자체는 그대로 놔둔 채 알고리즘 각 단계 처리를 서브클래스에서 재정의할 수 있게 합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/templatemethod_pattern.jpeg)

* AbstractClass
  * 서브클래스들이 재정의를 통해 구현해야 하는 알고리즘 처리 단계 내의 기본 연산을 정의합니다. 그리고 알고리즘의 뼈대를 정의하는 템플릿 메소드를 구현합니다. 템플릿 메소드는 AbstractClass에 정의된 연산이나 다른 객체 연산뿐만 아니라 기본 연산도 호출합니다.
* ConcreteClass
  * 서브클래스마다 달라진 알고리즘 처리 단계를 수행하기 위한 기본 연산을 구현합니다.

### 1.2. 사용 방법

1. ConcreteClass는 AbstractClass를 통하여 알고리즘이 변하지 않는 처리 단계를 구현합니다.

### 1.3. 장/단점
* Advantages (+)
    * Code Reuse
    * Inversion of Control

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired variant parts.
    * Uncontrolled subclassing.
* Consider the right design (solution):
    * Separated variant parts.
    * Controlled subclassing.

## 2. 템플릿 메소드 패턴(Template Method Pattern) 사용예시

템플릿 메소드 패턴은 다음 경우에 사용합니다.

* 어떤 한 알고리즘을 이루는 부분 중 변하지 않는 부분을 한 번 정의해 놓고 다양해질 수 있는 부분은 서브클래스에 정의할 수 있도록 남겨두고자 할 때
* 서브클래스 사이의 공통적인 행동을 추출하여 하나의 공통 클래스에 몰아둠으로써 코드 중복을 피하고 싶을 때
* 서브클래스의 확장을 제어할 수 있습니다. 템플릿 메소드가 어떤 특정한 시점에 훅 연산을 호출하도록 정의하여, 그 특정 시점에서만 확장 되도록 합니다.

### 2.1. GOF 패턴

#### 2.1.1. AbstractClass

```java
abstract class Coffee {
	
	public void makeCoffee() {
		this.putWater();
		this.putBeans();
	}
	
	public void putBeans() {
		System.out.println("Put Beans");
	}	
	
	abstract void putWater();
} 
```

#### 2.1.2. ConcreteClass

```java
class HotAmericano extends Coffee {
	
	@Override
	public void putWater() {
		System.out.println("Boiled Water");
		System.out.println("Put Water");
	}
}

class IceAmericano extends Coffee {

	@Override
	public void putWater() {
		System.out.println("Put Water");
		System.out.println("Put Ice");
	}
}
```

#### 2.1.3. Main

```java
public class Main{

	// Running the Client class as application.
	public static void main(String[] args) {
		Coffee c1 = new IceAmericano();
		Coffee c2 = new HotAmericano();
		
		c1.makeCoffee();
		System.out.println("\n");
		c2.makeCoffee();
	} 
}
```

결과는 아래와 같습니다.

```
Put Water
Put Ice
Put Beans

Boiled Water
Put Water
Put Beans
```

> 참고 자료

* [Template Method Pattern](https://en.wikipedia.org/wiki/Template_method_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
