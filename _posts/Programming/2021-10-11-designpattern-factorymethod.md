---
title:  "디자인 패턴 톺아보기 - Factory Method Pattern"
excerpt: "디자인 패턴 톺아보기 - Factory Method Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Factory Method Pattern
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 펙토리 메소드 패턴(Factory Method Pattern) 이란?

GOF 에서 말하는 추상 팩토리 패턴의 목적은 아래와 같습니다.

> Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to sub­classes.

> 객체를 생성하기 위해 인터페이스를 정의하지만, 어떤 클래스의 인스턴스를 생성할 지에 대한 결정은 서브클래스가 내리도록 합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/factory_method_pattern.png)

* Product
    * 팩토리 메소드가 생성하는 객체의 인터페이스를 정의합니다.
* ConcreteProduct
    * Product 클래스에 정의된 인터페이스를 실제로 구현합니다.
* Creator
    * Product 타입의 객체를 반환하는 팩토리 메소드를 선언합니다. Creator 클래스는 팩토리 메소드를 기본적으로 구현하는데, 이 구현에서는 ConcreteProduct 객체를 반환합니다. 또한 Product 객체의 생성을 위해 팩토리 메소드를 호출합니다.
* ConcreateCreator
    * 팩토리 메소드를 재정의하여 ConcreteProduct의 인스턴스를 반환합니다.
    
### 1.2. 사용 방법

1. Creator는 자신의 서브클래스를 통해 실제 필요한 메소드를 정의합니다.
2. 적절한 ConcreteProduct의 인스턴스를 반환한다.

### 1.3. 장/단점

* Advantages (+)
    * Avoids implementation dependencies.
* Disadvantages (–)
    * May require adding many subclasses.

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired object creation.
    * Unknown object creation.
* Consider the right design (solution):
    * Encapsulated object creation.
    * Deferred object creation.
  
## 2. 펙토리 메소드 패턴(Factory Method Pattern) 사용예시

### 2.1. GOF 패턴

#### 2.1.1. Product

```java
interface Product {
	String getName();
}
```

#### 2.1.2. ConcreteProduct

```java
class ConcreteProduct1 implements Product{
	public String getName() { 
		return "Product1";        
	}
}

class ConcreteProduct2 implements Product{
	public String getName() { 
		return "Product2";        
	}
}
```

#### 2.1.3. Creator

```java
abstract class Creator {
	private Product product;

	public abstract Product factoryMethod(String type);

	public String operation(String type) {
		product = factoryMethod(type);
		return "Creator run method is started [" + product.getName() + "] is created" ;
	}
}
```

#### 2.1.4. ConcreteCreator

```java
class ConcreteCreator extends Creator {
	public Product factoryMethod(String type) {
		
		if (type == "ONE") {
			return new ConcreteProduct1() ;
		} else {
			return new ConcreteProduct2() ;
		}
	}
}
```

#### 2.1.5 Main

```java
public class Main{
	public static void main(String[] args) {
		Creator creator = new ConcreteCreator(); 
		System.out.println(creator.operation("ONE"));
		System.out.println(creator.operation("TWO"));
	}
}
```

결과는 아래와 같습니다.

```
Creator run method is started [Product1] is created
Creator run method is started [Product2] is created
```

> 참고 자료

* [Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)


