---
title:  "디자인 패턴 톺아보기 - Builder Pattern"
excerpt: "디자인 패턴 톺아보기 - Builder Pattern"
categories:
  - Programming
tags:
  - Design Pattern
  - Builder Pattern
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 빌더 패턴(Builder Pattern) 이란?

GOF 에서 말하는 빌더 패턴의
 목적은 아래와 같습니다.

> Separate the construction of a complex object from its representation so that the same construction process can create different representations.

> 복잡한 객체를 생성하는 방법을 정의하는 클래스와 표현하는 방법을 정의하는 클래스를 별도로 분리하여, 서로 다른 표현이라도 이를 생성할 수 있는 동일한 프로세스를 제공하는패턴입니다.  

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/builder_pattern.jpg)

* Builder
  * Product 객체의 일부 요소들을 생성하기 위한 추상 인터페이스를 정의합니다.
* ConcreteBuilder
  * Builder 클래스에 정의된 인터페이스를 구현하며, 제품의 부품들을 모아 빌더를 복합합니다. 생성한 요소의 표현을 정의하고 관리합니다. 또한 제품을 검색하는 데 필요한 인터페이스를 제공합니다.
* Director
  * Builder 인터페이스를 사용하는 객체를 합성합니다. 
* Product
  * 생성할 복합 객체를 표현합니다. ConcreteBuilder는 제품의 내부 표현을 구축하고 복합 객체가 어떻게 구성되는지에 관한 절차를 정의합니다.
  
### 1.2. 사용 방법

1. 사용자는 Director 객체를 생성하고 생성한 객체를 자신이 원하는 Builder 객체로 합성한다.
2. 제품의 일부가 build 될 때마다 Director는 Builder에 통보한다.
3. Builder는 Director의 요청을 처리하여 제품에 부품을 추가한다.
4. 사용자는 Builder에서 제품을 검색한다.

### 1.3. 장/단점

* Advantages (+)
    * Avoids compile-time implementation dependencies.
    * Simplifies clients.
* Disadvantages (-)
    * Introduces an additional level of indirection.

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired object creation.
    * Complicated classes.
* Consider the right design (solution):
    * Encapsulated object creation.
    * Simplified classes.
  
## 2. 빌더 패턴(Builder Pattern) 사용예시

빌더 패턴은 다음 경우에 사용합니다.

* 복합 객체의 생성 알고리즘이 이를 합성하는 요소 객체들이 무엇인지 이들의 조립 방법에 독립적일 때
* 합성할 객체들의 표현이 서로 다르더라도 생성 절차에서 이를 지원해야 할 때

### 2.1. GOF 패턴

회원을 생성하는 간단한 예제를 통해 알아보겠습니다.

#### 2.1.1. Builder

```java
/** Builder */
abstract class MemberBuilder {
	protected Member member;

	public Member getMember() {
		return this.member;
	}

	public void createNewMemberProduct() {
		member = new Member();
	}

	public abstract void buildName();

	public abstract void buildAge();
	
	public abstract void buildType();
}
```

#### 2.1.2. ConcreteBuilder

```java
/** ConcreteBuilder */
class StaffMemberBuilder extends MemberBuilder {
	public void buildName() {
		member.setName("Alice");
	}

	public void buildAge() {
		member.setAge(23);
	}

	public void buildType() {
		member.setType("STAFF");
	}
}

/** ConcreteBuilder */
class ManagerMemberBuilder extends MemberBuilder {
	public void buildName() {
		member.setName("Bob");
	}

	public void buildAge() {
		member.setAge(31);
	}

	public void buildType() {
		member.setType("MANGER");
	}
}
```

#### 2.1.3. Product

```java
/** Product */
class Member {
	private String name ;
	private int age ;
	private String type;

	public void setName(String name) {
		this.name = name;
	}

	public void setAge(int age) {
		this.age = age;
	}
	
	public void setType(String type) {
		this.type = type;
	}
	
	@Override
	public String toString() {
		return "회원정보 [성명: " + this.name + "],  [나이: " + this.age + "], [등급: " + this.type + "]" ;
	}
}
```

#### 2.1.4. Director

```java
/** Director */
class Director {
	private MemberBuilder memberBuilder;

	public void setMemberBuilder(MemberBuilder memberBuilder) {
		this.memberBuilder = memberBuilder;
	}

	public Member getMember() {
		return memberBuilder.getMember();
	}

	public void constructMember() {
		memberBuilder.createNewMemberProduct();
		memberBuilder.buildAge();
		memberBuilder.buildName();
		memberBuilder.buildType();
	}
}
```

#### 2.1.5. Main

* Main 클래스에서 간단한 예시를 통해 사용해보겠습니다.

```java
public class Main{

	public static void main(String[] args) {
		Director director = new Director();
		MemberBuilder staffBuilder = new StaffMemberBuilder();
		MemberBuilder managerBuilder = new ManagerMemberBuilder();

		director.setMemberBuilder(staffBuilder);
		director.constructMember();
		System.out.println(hire.getMember());
		
		director.setMemberBuilder(managerBuilder);
		director.constructMember();
		System.out.println(hire.getMember());
	}
}
```

결과는 아래와 같습니다.

```java
회원정보 [성명: Alice],  [나이: 23], [등급: STAFF]
회원정보 [성명: Bob],  [나이: 31], [등급: MANGER]
```

### 2.2. Effective Builder 패턴

```java
Company c1 = new Company("Github", "1", "01012345678", "0312223333", "서울시", "13322");
```

위와같이 클래스의 매개변수가 많아질 수록 생성자 함수를 사용할 때 각각의 인자가 무엇을 의미하는지 알기 어렵습니다.

이러한 문제를 해결하기 위해서 JavaBeans Pattern 이 나왔는데 바로 Getter/Setter 를 이용한 패턴입니다.

```java
class Member {
  private String name;
  private int age;
  
  public String getName() {
    return this.name;
  }
  public void setName(String name){
    this.name = name;
  }
  public int getAge() {
    return this.age;
  }
  public void setAge(int age){
    this.age = age;
  }
}

public class Main {
	public static void main(String[] args) {
	  Member m = new Member();
	  m.setName("사용자");
	  m.setAge(12);
	}
}
```

위 방법을 사용하면 각각 메소드의 인자가 어떤 인자이지 파악하기 쉽습니다. 하지만 immutable 한 객체를 만들 수 없고 객체를 여러번 호출해야 하는 단점이 있습니다. 

마지막으로는 Effective Java 에서 소개하는 Builder Pattern 입니다.

```java
class Company {
	
	private final String cmpynm;
	private final String cmpyno;
	private final String telno;
	private final String faxno;
	private final String address;
	private final String zipcode;
	private final List<Person> personlist;
	
	public static class Builder {
		private final String cmpynm ;
		private final String cmpyno ;
		
		private String telno ;
		private String faxno ;
		private String address ;
		private String zipcode ;
		private List<Person> personlist = new ArrayList<Person>();
		
		public Builder(String cmpynm, String cmpyno) {
			this.cmpynm = cmpynm;
			this.cmpyno = cmpyno;
		}
		public Builder telno(String telno) {
			this.telno = telno;
			return this;
		}
		public Builder faxno(String faxno) {
			this.faxno = faxno;
			return this;
		}
		public Builder address(String address) {
			this.address = address;
			return this;
		}
		public Builder zipcode(String zipcode) {
			this.zipcode = zipcode;
			return this;
		}
		public Builder personlist(Person personlist) {
			this.personlist.add(personlist);
			return this;
		}
		public Company build() {
			return new Company(this);
		}
	}
	
	private Company(Builder builder) {
		this.cmpynm = builder.cmpynm;
		this.cmpyno = builder.cmpyno;
		this.telno = builder.telno;
		this.faxno = builder.faxno;
		this.address = builder.address;
		this.zipcode = builder.zipcode;
		this.personlist = builder.personlist;
	}
	
}

class Person {
	private String name;
	private String code;
	private Integer salary;
	
	public Person(String name, String code, Integer salary) {
		this.name = name;
		this.code = code;
		this.salary = salary;
	}
}
```

아래와 같이 객체를 생성할 수 있습니다.

```java
Company.Builder builder = new Company.Builder("Java", "J0000001");
builder.telno("01012345678");
builder.faxno("0212345678");
builder.address("서울시");
builder.zipcode("06789");
builder.personlist(new Person("Alice", "0000001", 1000000));
builder.personlist(new Person("Bob", "0000002", 2000000));
builder.personlist(new Person("Charlie", "0000003", 3000000));
Company company = builder.build();
```

```java
Company comapny2 = new Company
        .Builder("Java", "J000001")
        .telno("01012345678")
        .faxno("0212345678")
        .address("서울시")
        .zipcode("06789")
        .personlist(new Person("Alice", "0000001", 1000000))
        .personlist(new Person("Bob", "0000002", 2000000))
        .personlist(new Person("Charlie", "0000003", 3000000))
        .build();
```

> 참고 자료

* [Builder Pattern](https://en.wikipedia.org/wiki/Builder_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
* [Effective Java 3th Edition](http://www.yes24.com/Product/Goods/65551284)


