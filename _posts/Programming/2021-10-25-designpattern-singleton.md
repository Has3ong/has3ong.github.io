---
title:  "디자인 패턴 톺아보기 - Singleton Pattern"
excerpt: "디자인 패턴 톺아보기 - Singleton Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Singleton Pattern
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 싱글톤 패턴(Singleton Pattern) 이란?

GOF 에서 말하는 싱글톤 패턴의 목적은 아래와 같습니다.

> Ensure a class only has one instance, and provide a global point of access to it.

> 오직 한 개의 클래스 인스턴스만을 갖도록 보장하고, 이에 대한 전역적인 접근점을 제공합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/singleton_pattern.png)

* Singleton
    * `Instance()` 연산을 정의하여, 유일한 인스턴스로 접근할 수 있도록 합니다.
    * `Instance()` 연산은 클래스 연산이며, 유일한 인스턴스를 생성하는 책임을 맡습니다.

### 1.2. 사용 방법

1. 사용자는 Singleton 클래스에 정의된 `Instance()` 연산을 통해서 유일하게 생성되는 단이렟 인스턴스에 접근할 수 있습니다.

### 1.3. 장/단점

* Advantages (+)
    * Can control object creation.
* Disadvantages (–)
    * Makes clients dependent on the concrete singleton class.
    * Can cause problems in a multi-threaded environment.

### 1.4. 고려사항

* Consider the left design (problem):
    * Multiple instances possible.
* Consider the right design (solution):
    * Only one instance possible.
    
## 2. 싱글톤 패턴(Singleton Pattern) 사용예시

### 2.1. GOF 패턴

#### 2.1.1. Singleton

```java
class Singleton {
	private static final Singleton INSTANCE = new Singleton();
	
	private Singleton() {}
	
	public static Singleton getInstance() {
		return INSTANCE;
	}
}
```

#### 2.1.2. Main

```java
public class Main{
	public static void main(String[] args) { 
		Singleton ref1 = null;
		Singleton ref2 = null;
		
		ref1 = Singleton.getInstance();
		ref2 = Singleton.getInstance();
		
		if (ref1 == ref2) {
			System.out.println("ref1 == ref2");
		}
		
		if (ref1.equals(ref2)) {
			System.out.println("ref1.equals(ref2)");
		}
	}
}
```

결과는 아래와 같습니다.

```
ref1 == ref2
ref1.equals(ref2)
```

> 참고 자료

* [Singleton Pattern](https://en.wikipedia.org/wiki/Singleton_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)


