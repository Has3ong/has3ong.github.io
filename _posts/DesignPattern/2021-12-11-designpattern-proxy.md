---
title:  "디자인 패턴 톺아보기 - Proxy Pattern"
excerpt: "디자인 패턴 톺아보기 - Proxy Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Proxy Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 프록시 패턴(Proxy Pattern) 이란?

GOF 에서 말하는 프록시 패턴의 목적은 아래와 같습니다.

> Provide a surrogate or placeholder for another object to control access to it.

> 다른 객체에 대한 접근을 제어하기 위한 대리자나 자리채움자 역할을 하는 객체를 둡니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/proxy_pattern.png)

* Proxy
    * 실제 참조할 대상에 대한 참조자를 관리합니다.
    * Subject와 동일한 인터페이스를 제공하여 실제 대상을 대체할 수 있어야 합니다.
    * 실제 대상에 대한 접근을 제어하고 실제 대상의 생성과 삭제를 책임집니다.
* Subject
    * RealSubject와 Proxy에 공통적인 인터페이스를 정의하여, RealSubject가 요청되는 곳에 Proxy를 사용할 수 있게 합니다.
* RealSubject
    * 프록시가 대표하는 실제 객체입니다.

### 1.2. 사용 방법

1. 프록시 클래스는 자신이 받은 요청을 RealSubejct 객체에 전달합니다.

### 1.3. 장/단점

* Advantages (+)
    * Simplifies clients.
* Disadvantages (–)
    * Proxy is coupled to real subject.

### 1.4. 고려사항

* Consider the left design (problem):
    * No proxy / direct access. Complicated clients.
* Consider the right design (solution):
    * Working through a proxy. Simplified clients.

## 2. 프록시 패턴(Proxy Pattern) 사용예시

프록시 패턴은 단순한 포인터보다 조금 더 다방면에 활용할 수 있거나 정교한 객체 참조자가 필요할 때 적용할 수 있습니다. 어떨 때인지 살펴봅시다.

* 원격지 프록시(Remote Proxy)
    * 서로 다른 주소 공간에 존재하는 객체를 가리키는 대표 객체로 로컬 환경에 위치합니다.
* 가상 프록시(Virtual Proxy)
    * 요청이 있을 때만 필요한 고비용 객체를 생성합니다.
* 보호용 프록시(Protection Proxy)
    * 원래 객체에 대한 실제 접근을 제어합니다. 이는 객체별로 접근 제어 권한이 다를 때 유용하게 사용할 수 있습니다.
* 스마트 참조자(Smart Reference)
    * 원시 포인터의 대체용 객체로, 실제 객체에 접근이 일어날 때 추가적인 행동을 수행합니다. 전형적인 사용예는 다음과 같습니다.
        * 실제 객체에 대한 참조 횟수를 저장하다 더는 참조가 없을 때 해당 객체를 자동으로 없앱니다.
        * 맨 처음 참조되는 시점에 영속적 저장소의 객체를 메모리로 옮깁니다.
        * 실제 객체에 접근하기 전에, 다른 객체가 그것을 변경하지 못하도록 실제 객체에 대해 잠금을 겁니다.   

### 2.1. GOF 패턴

#### 2.1.1. Proxy

```java
class Proxy extends Subject {
	private RealSubject realSubject;
	
	public Proxy(RealSubject realSubject, Integer index) {
		this.realSubject = realSubject;
		this.realSubject.setIndex(index);
	}
	
	public String operation() {
		return "Proxy and " + this.realSubject.operation(); 
	}
}
```

#### 2.1.2. Subject

```java
abstract class Subject {
	public abstract String operation();
}
```

#### 2.1.3. RealSubject

```java
class RealSubject extends Subject {
	private Integer index;
	
	public String operation() {
		return "RealSubject" + this.index;
	}
	
	public void setIndex(Integer index) {
		this.index = index;
	}
}
```

#### 2.1.4. Main

```java
public class Main{
	public static void main(String[] args) {
		Proxy proxy = new Proxy(new RealSubject(), 1);
		System.out.println(proxy.operation());
		
		Proxy proxy2 = new Proxy(new RealSubject(), 2);
		System.out.println(proxy2.operation());
	}
}
```

결과는 아래와 같습니다.

```
Proxy and RealSubject1
Proxy and RealSubject2
```

> 참고 자료

* [Proxy Pattern](https://en.wikipedia.org/wiki/Proxy_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
