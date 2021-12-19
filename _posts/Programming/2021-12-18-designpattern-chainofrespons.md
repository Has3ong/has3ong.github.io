---
title:  "디자인 패턴 톺아보기 - Chain of Responsibility Pattern"
excerpt: "디자인 패턴 톺아보기 - Chain of Responsibility Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Chain of Responsibility Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 책임 연쇄 패턴(Chain of Responsibility Pattern) 이란?

GOF 에서 말하는 책임 연쇄 패턴의 목적은 아래와 같습니다.

> Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

> 메세지를 보내는 객체와 이를 받아 처리하는 객체들 간의 결합도를 없애기 위한 패턴입니다. 하나의 요청에 대한 처리가 반드시 한 객체에서만 되지 않고, 여러 객체에게 그 처리 기회를 주려는 것이다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/chainofrespons_pattern.png)

* Handler
  * 요청을 처리하는 인터페이스를 정의하고, 후속 처리자와 연결을 구현합니다. 즉, 연결 고리에 연결된 다음 객체에게 다시 메세지를 보냅니다.
* ConcreteHandler
  * 책임져야 할 행동이 있다면 스스로 요청을 처리하여 후속 처리자에 접근할 수 있습니다. 즉, 자신이 처리할 행동이 있으면 처리하고, 그렇지 않으면 후속 처리자에 다시 처리를 요청합니다.
* Client
  * 객체에게 필요한 요청을 보냅니다.

### 1.2. 사용 방법

1. 사용자는 처리 요청하고, 이 처리 요청은 실제로 그 요청을 받을 책임이 있는 ConcreteHandler 객체를 만날 때까지 정의된 연결 고리를 따라서 계속 전달됩니다.
### 1.3. 장/단점

* Advantages (+)
    * Decouples sender from receiver
    * Makes changing the chain of handlers easy.
* Disadvantages (–)
    * Successor chain can be complex.

### 1.4. 고려사항

* Consider the left design (problem):
    * One receiver.
* Consider the right design (solution):
    * Encapsulated request.

## 2. 책임 연쇄 패턴(Chain of Responsibility Pattern) 사용예시

책임 연쇄 패턴은 다음 경우에 사용합니다.

* 하나 이상의 객체가 요청을 처리해야 하고, 그 요청 처리자 중 어떤 것이 선행자인지 모를 때, 처리자가 자동으로 확정되어야 합니다.
* 메세지를 받을 객체를 명시하지 않은 채 여러 객체 중 하나에게 처리를 요청하고 싶을 때
* 요청을 처리할 수 있는 객체 집합이 동적으로 정의되어야 할 때

### 2.1. GOF 패턴

#### 2.1.1. Handler

```java
abstract class Handler {
	private Handler handler;
	public Handler() {}
	
	public Handler(Handler handler) {
		this.handler = handler;
	}
	
	public void handlerRequest() {
		if (this.handler != null) {
			handler.handlerRequest();
		}
	}
	
	public boolean canHandlerRequest() {
		return false;
	}
}
```

#### 2.1.2. ConcreteHandler

```java
class Receiver1 extends Handler {
	public Receiver1(Handler handler) {
		super(handler);
	}
	
	@Override
	public void handlerRequest() {
		if (canHandlerRequest()) { 
			System.out.println("Receiver1: Handling the request ...");
		}  else { 
			System.out.println("Receiver1: Passing the request along the chain ...");
			super.handlerRequest();
		} 
	}
}

class Receiver2 extends Handler {
	public Receiver2(Handler handler) {
		super(handler);
	}
	
	@Override
	public void handlerRequest() {
		if (canHandlerRequest()) { 
			System.out.println("Receiver2: Handling the request ...");
		}  else { 
			System.out.println("Receiver2: Passing the request along the chain ...");
			super.handlerRequest();
		} 
	}
}

class Receiver3 extends Handler {
	@Override
	public void handlerRequest() {
		System.out.println("Receiver3: Handling the request.");
	}
}
```
#### 2.1.3. Client

```java
public class Main{
	public static void main(String[] args) {
		Handler handler = new Receiver1(new Receiver2(new Receiver3()));
		System.out.println("Issuing a request to a handler object ... "); 
		handler.handlerRequest();
	}
}
```

결과는 아래와 같습니다.

```
Issuing a request to a handler object ... 
Receiver1: Passing the request along the chain ...
Receiver2: Passing the request along the chain ...
Receiver3: Handling the request.
```

### 2.2. 예제 

GOF 패턴은 이해하기 어려우니 예제를 통해 다시 알아보겠습니다.

잔돈을 거슬러주는 코드를 만들어보겠습니다. 제가 작성한 코드보다 더 좋은 코드가 있을 수 있으니 참고하시기 바랍니다.

```java
abstract class Exchange {
	private Exchange exchange;
	private Integer money;
	
	public Exchange() {};
	public Exchange(Exchange exchange) {
		exchange.setMoney(this.money);
		this.exchange = exchange;
		
	}
	
	public void setMoney(Integer money) {
		this.money = money;
	}
	
	public Integer getMoney() {
		return this.money;
	}
	
	public void getExchange() {
		this.getExchange(1000);
	}

	public void getExchange(Integer pay) {
		int num = this.getMoney() / pay;
		int remain = money - (pay * num);
		System.out.println("[Recive Money: " + this.getMoney() + ", Exchange :" + pay + "W * " + num + ", Remain Money: " + remain + "]");
		
		if (exchange != null) {
			this.exchange.setMoney(remain);
			this.exchange.getExchange(pay);
		}
	}
}

class Exchange1000 extends Exchange {
	public Exchange1000(Exchange exchange) {
		super(exchange);
	}
	
	@Override
	public void getExchange(Integer pay) {
		super.getExchange(1000);
	}
}

class Exchange500 extends Exchange {
	public Exchange500(Exchange exchange) {
		super(exchange);
	}
	
	@Override
	public void getExchange(Integer pay) {
		super.getExchange(500);
	}
}

class Exchange100 extends Exchange {
	@Override
	public void getExchange(Integer pay) {
		super.getExchange(100);
	}
}

public class Main{
	public static void main(String[] args) {
		Exchange exchange = new Exchange1000(new Exchange500(new Exchange100()));
		exchange.setMoney(2800);
		exchange.getExchange();
	}
}
```

결과는 아래와 같습니다.

```
[Recive Money: 2800, Exchange :1000W * 2, Remain Money: 800]
[Recive Money: 800, Exchange :500W * 1, Remain Money: 300]
[Recive Money: 300, Exchange :100W * 3, Remain Money: 0]
````

> 참고 자료

* [Chain of Responsibility Pattern](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
