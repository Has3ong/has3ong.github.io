---
title:  "디자인 패턴 톺아보기 - Abstract Factory Pattern"
excerpt: "디자인 패턴 톺아보기 - Abstract Factory Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Abstract Factory Pattern
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 추상 팩토리 패턴(Abstract Factory Pattern) 이란?

GOF 에서 말하는 추상 팩토리 패턴의 목적은 아래와 같습니다.

> *Provide an interface for creating families of related or dependent objects without specifying their concrete classes.*

> 상세화된 서브클래스를 정의하지 않고도 서로 관련성이 있거나 독립적인 여러 객체의 군을 생성하기 위한 인터페이스를 제공합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/abstract_pattern.png)

* AbstractFactory
    * 개념적 제품에 대한 겍체를 생성하는 연산으로 인터페이스를 정의합니다.
* ConcreteFactory
    * 구체적인 제품에 대한 객체를 생성하는 연산을 구현합니다.
* AbstractProduct
    * 개념적 제품 객체에 대한 인터페이스를 정의합니다.
* ConcreteProduct
    * 구체적으로 팩토리가 생성할 객체를 정의하고, AbstractProduct가 정의한 인터페이스를 구현합니다.
* Client
    * AbstractFactory와 AbstractProduct 클래스에 선언된 인터페이스를 사용합니다.

### 1.2. 사용 방법

1. 일반적으로 ConcreteFactory 클래스의 인스턴스 한 개가 런타임에 만들어집니다. 이 구체 팩토리(Concrete Factory)는 어떤 특정 구현을 갖는 제품 객체를 생성합니다. 서로 다른 제품 객체를 생성하려면 사용자는 서로 다른 구체 팩토리를 사용해야 합니다.
2. AbstractFactory는 필요한 제품 객체를 생성하는 책임을 ConctreteFactory 서브 클래스에 위임합니다.

### 1.3. 장/단점

* Advantages (+)
    * Avoids compile-time implementation dependencies.
    * Ensures creating consistent object families.
    * Makes exchanging whole object families easy.
* Disadvantages (–)
    * Requires extending the Factory interface to extend an object family.
    * Introduces an additional level of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired object creation.
    * Distributed object creation.
* Consider the right design (solution):
    * Encapsulated object creation.
    * Centralized object creation.
  
## 2. 추상 팩토리 패턴(Abstract Factory Pattern) 사용예시

### 2.1. GOF 패턴

공장에서 제품을 만드는 간단한 예제를 통해 알아보겠습니다.

#### 2.1.1. AbstractFactory

```java
abstract class AbstractFactory {
	  public abstract Phone createPhone();
	  public abstract Notebook createNotebook();
}
```

#### 2.1.2. ConcreteFactory

```java
class AppleFactory extends AbstractFactory {
	  public Phone createPhone() { return new ApplePhone(); }
	  public Notebook createNotebook() { return new AppleNotebook(); }
}

class SamsungFactory extends AbstractFactory {
	  public Phone createPhone() { return new SamsungPhone(); }
	  public Notebook createNotebook() { return new SamsungNotebook(); }
}
```

#### 2.1.3. AbstractProduct

```java
abstract class Notebook{
	public abstract String getName();
}

abstract class Phone{
	public abstract String getName();
}
```

#### 2.1.4. ConcreteProduct

```java
class ApplePhone extends Phone { public String getName() { return "IPhone"; } }
class SamsungPhone extends Phone { public String getName() { return "GalaxyNote"; } }

class AppleNotebook extends Notebook { public String getName() { return "MacBook"; } }
class SamsungNotebook extends Notebook { public String getName() { return "Flex"; } }
```

#### 2.1.5. Client

```java
class Client { 
	private Phone phone;
	private Notebook notebook;
	private AbstractFactory factory;
	
	public Client(AbstractFactory factory) {
		this.factory = factory;
	}
	
	public String operation() {
		System.out.println("Client  : Delegating creating objects to a factory object.");
		phone = factory.createPhone();
		notebook = factory.createNotebook();
		return "Factory Create [Phone: " + phone.getName() + "], [Notebook: " + notebook.getName() + "]" ; 
	} 
}
```

#### 2.1.6. Main

```java
public class Main{
	public static void main(String[] args) {
		Client client1 = new Client(new AppleFactory()); 
		System.out.println(client1.operation()); 
		
		Client client2 = new Client(new SamsungFactory()); 
		System.out.println(client2.operation()); 
	}
}
```

결과는 아래와 같습니다.

```
Client  : Delegating creating objects to a factory object.
Factory Create [Phone: IPhone], [Notebook: MacBook]
Client  : Delegating creating objects to a factory object.
Factory Create [Phone: GalaxyNote], [Notebook: Flex]
```

> 참고 자료

* [Abstract Factory Pattern](https://en.wikipedia.org/wiki/Abstract_factory_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)


