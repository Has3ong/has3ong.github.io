---
title:  "Java 8 Optional 살펴보기"
excerpt: "Java 8 Optional 살펴보기"
categories:
  - Programming
tags:
  - Java
  - JDK8
  - Optional
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## 1. Intro

Java 를 이용하여 개발하면서 가장 많이 발생하는 예외중 하나는 NPE(NullPointerException) 입니다. NPE 예외를 피하기 위해서는 `null` 체크를 필수로 해줘야 하는데, 확인해야 하는 변수가 많아질수록 코드가 복잡해집니다.

그러므로 `null` 대신 초깃값으로 사용하기도 권장합니다.

위와 같은 이유로 `Optional` 클래스가 Java 8 에서 최초로 도입되었습니다. 간단한 예제를 통해서 알아보겠습니다. 아래와 같은 `Person` 클래스가 있다고 가정하겠습니다.

```java
class Person {
	  String name ;
	  Integer age ;
}
```

`Service` 로직에서 `Person` 정보를 아래와 같이 가져온다고 가정하겠습니다.

```java
Person person = personService.getPerson() ;
System.out.println("name : " + person.getName()) ;
System.out.println("age : " + person.getAge()) ;
```

`person` 객체가 `null` 이 아니면 정상적으로 출력이 되지만 `null` 일 경우 NPE 예외가 발생합니다. 위 예외 처리를 해결하기 위해 `if` 문을 활용하면 아래와 같이 작성해야 합니다.

```java
Person person = personService.getPerson() ;
if (person != null) {
    System.out.println("name : " + person.getName()) ;
    System.out.println("age : " + person.getAge()) ;
}
```

간단하게 해결할 수 있습니다. 하지만 여기서 아래와 같이 새로운 요구사항이 발생합니다.

* 이름과 나이의 값이 `null` 일 경우에는 노출해주지 마세요.

```java
Person person = personService.getPerson() ;
if (person != null) {
    if (person.getName() != null) {
        System.out.println("name : " + person.getName()) ;
    }
    if (person.getAge() != null) {
        System.out.println("age : " + person.getAge()) ;
    }
}
```

`if` 문으로 위 요구사항을 해결했지만 점점 코드가 복잡해지고 너저분해지는것을 알 수 있습니다. 위 사항을 `Optional` 클래스로 간단히 해결할 수 있습니다. 아래 예시를 통해 알아보겠습니다.

```java
Person person = personService.getPerson() ;
Optional<Person> personOptional = Optional.ofNullable(person);
personOptional.map(Person::getName).ifPresent(name -> System.out.println("name : " + name));
personOptional.map(Person::getAge).ifPresent(age -> System.out.println("age : " + age));
```

위처럼 `if` 분기문으로 나누지 않고 함수형으로 코드를 작성할 수 있어 가동성을 높일 수 있습니다.

하지만 `Optional` 을 사용할 때 중요한 사항이 하나 있습니다. `Optional` 은 반환할 값이 없을 때 `null` 대신 Wrapper 로 감싸는 타입입니다. 즉, `Optional` 을 반환하는 메소드를 만들 때 절대 `null` 을 반환하는 `Optional` 을 리턴하면 안됩니다.

왜냐하면, `Optional` 값을 Wrapping 하고 다시 풀고, `null` 일 경우에는 대체함수를 호출해야 하기 때문에 오버헤드가 발생하여 성능저하가 발생합니다. `Optional` 을 사용하는 가장 좋은 상황은 **메소드의 결과를 알 수 없으며, 클라이언트가 이 상황을 특별하게 처리해야 할 때** `Optional<T>` 를 반환하면 됩니다. 

간단한 예제를 알아봤으니 `Optional` 클래스에서 제공하는 메소드들을 알아보겠습니다.

## 2. Creating Optional Objects

먼저 `Optional` 객체를 생성하는 메소드들을 알아보겠습니다.

### 2.1. Optional.of

`of` 메소드는 값이 `null` 인 경우 NullPointerException 예외가 발생합니다. 반드시 값이 있어야 하는 객체인 경우 해당 메서드를 사용하면 됩니다.

```java
Optional<String> optional = Optional.of("result");
```

### 2.2. Optional.ofNullable

값이 `null` 인 경우 비어있는 `Optional` 을 반환합니다. `of` 메소드와는 다르게 값이 `null` 일수도 있는 것은 해당 메서드를 사용하면 됩니다.

```java
Optional<String> optional1 = Optional.ofNullable("result");
Optional<String> optional2 = Optional.ofNullable(null);
```

### 2.3. Optional.empty

`empty` 메소드를 이용하면 `null` 값을 전달 할 때 예외가 발생하지 않으며 비어있는 `Optional` 객체를 반환할 수 있습니다.

```java
Optional<String> optional = Optional.empty();
```

## 3. Optional Object Intermediate Processing

`Optional` 객체를 여러 메서드를 사용하여 값을 필터링하거나 다른 값으로 변환할 수 있습니다. Java 8 에서 제공하는 `Stream` 클래스처럼 `Optional` 도 메소드 체이닝을 통해 여러 개의 중간 연산을 처리하고 최종적으로 종단 처리 메서드를 통해 최종 결과를 반환할 수 있습니다.

`Optional` 객체를 중간처리할 수 있는 메소드에 대해 알아보겠습니다.

### 3.1. Optional.filter

`filter` 메서드를 활용하면 원하는 값을 갖는 `Optional` 객체만 필터링할 수 있습니다. 연도를 비교하는 간단한 예시를 통해 알아보겠습니다.

`isPresent` 메소드는 4절에서 알아보겠습니다.

```java
Integer year = 2021;
Optional<Integer> yearOptional = Optional.of(year);
// True
boolean is2021 = yearOptional.filter(y -> y == 2021).isPresent();
// False
boolean is2022 = yearOptional.filter(y -> y == 2022).isPresent();
```

다음으로 복잡한 예시를 알아보겠습니다. `Person` 객체 들의 나이가 범위 내에 있는지 확인하는 코드를 `Optional` 사용 여부에 따라 비교해보겠습니다.

먼저 `Optional` 이 없는 코드를 살펴보겠습니다.

```java
public boolean isCheck1(Person person) {
    boolean isInRange = false;
    
    if (person != null && person.getAge() != null && 
            (person.getAge() >= 10  && person.getAge() <= 30)) {
        isInRange = true;
    }
    
    return isInRange; 
}
```

`Optional` 을 사용해서 코드를 작성해보겠습니다.

```java
public boolean isCheck2(Person person) {
    return Optional.ofNullable(person)
            .map(Person::getAge)
            .filter(p -> p >= 10)
            .filter(p -> p <= 30)
            .isPresent();
}
```

### 3.2. Optional.map

`map` 메서드로 `Optional` 값을 변환할 수 있습니다.

```java
List<String> list = Arrays.asList(
        "Alice", "Bob", "Charlie", "David");
Optional<List<String>> listOptional = Optional.of(list);
// 4
int size = listOptional
        .map(List::size)
        .orElse(0);
```

위 예제는 `Optional` 객체 안에 문자열 목록을 래핑하고 `map` 메소드를 사용하여 포함된 목록에 대한 작업을 수행합니다. 위에서 수행하는 작업은 리스트 크기를 반환하는 것입니다.

`map` 과 `filter` 메소드를 함께 사용하면 더 유용한 작업을 진행할 수 있습니다. 사용자가 입력한 비밀번호의 정확성을 확인하는 예제를 통해 알아보겠습니다.

```java
String password = " password ";
Optional<String> passOpt = Optional.of(password);

// false
boolean correctPassword = passOpt
        .filter(p -> p.equals("password"))
        .isPresent();

// true
correctPassword = passOpt
        .map(String::trim)
        .filter(p-> p.equals("password"))
        .isPresent();
```

### 3.3. Optional.flatMap

`map` 메소드와 마찬가지로 값을 변환하는 대안으로 `flatMap` 메서드도 있습니다. 차이점은 `map` 은 래핑되지 않은 경우에만 값을 변환하는 반면 `flatMap` 은 래핑 된 값을 가져와 변환하기 전에 래핑 해제한다는 것입니다.

이전 예제에서는 `Optional` 인스턴스에서 래핑하기 위해 간단한 `String` 및 `Integer` 개체를 만들었습니다. 하지만 대부분 상황에서 복잡한 객체의 접근자로부터 객체를 반환받습니다. 예제를 통해 알아보겠습니다.

```java
class Person {
	  String name ;
	  Integer age ;
	  
	  public Person() {}
	  
	  public Person(String name, Integer age) {
		  this.name = name ;
		  this.age = age ;
	  }

	  public Optional<String> getName() {
		  return Optional.ofNullable(name);
	  }

	  public Optional<Integer> getAge() {
		  return Optional.ofNullable(age);
	  }
}
```

위와 같이 래핑 된 `Person` 클래스를 이용하여 아래 예제를 사용하면 됩니다.

```java
Person person = new Person("Alice", 26);
Optional<Person> personOptional = Optional.of(person);

Optional<Optional<String>> nameOptionalWrapper  
    = personOptional.map(Person::getName);
Optional<String> nameOptional 
    = nameOptionalWrapper.orElseThrow(IllegalArgumentException::new);

// Alice
String name1 = nameOptional.orElse("");
System.out.println(name1) ;

// Alice
String name = personOptional
        .flatMap(Person::getName)
        .orElse("");
System.out.println(name);
```

위 코드에서는 `Person` 개체의 이름을 검색하는 예제입니다.

세 번째 명령문에서 `map` 메소드와 `flatMap` 메소드로 동일한 작업을 수행하는 방법의 차이를 주의하셔서 확인하면 됩니다.

`map` 함수를 이용하여 반환하면 추가로 래핑 된 객체를 반환하기 위해 추가 호출을 해야 하는데 `flatMap` 을 사용하면 암시적으로 래핑을 해제시키는 것을 알 수 있습니다.

## 4. Optional Object Result Processing

마지막으로 종단 처리에 대해 알아보겠습니다. 종단 처리는 `Optional` 객체의 메소드 체이닝을 끝낸다는 의미입니다.

### 4.1. Optional.isPresent

최종적으로 연산을 끝낸 후 생성된 `Optional` 객체가 존재하는지를 확인합니다.

```java
// true
Optional.ofNullable("result")
    .isPresent();
// false
Optional.ofNullable("result")
    .filter(val -> "false".equals(val))
    .isPresent(); 
```

### 4.2. Optional.ifPresent

`ifPresent` 메소드를 사용하면 값이 `null`이 아닌 것으로 확인되면 래핑 된 값에 대해 일부 코드를 실행할 수 있습니다.

```java
Optional<String> opt = Optional.of("result");
opt.ifPresent(name -> System.out.println(name.length()));
```

### 4.3. Optional.get

`get` 메서드는 `Optional` 객체에서 값을 꺼낼 수 있는 가장 간단한 메소드입니다.

하지만 값이 `null` 인 경우에 NullPointerException 예외가 발생합니다.

```java
Optional<String> opt = Optional.of("result");
String name = opt.get();
```

### 4.4. Optional.orElse

`orElse` 메서드는 `Optional` 객체 내부에 값을 조회하는 데 사용합니다. 이 메서드는 래핑 된 값이 있으면 반환하고, 그렇지 않으면 인수를 반환합니다.

```java
String nullName = null;
String name = Optional.ofNullable(nullName).orElse("result");
```

### 4.5. Optional.orElseGet

`orElseGet` 메소드는 `orElse`와 유사합니다. 차이점은 `Optional` 값이 없으면 반환할 값을 가져오는 대신 **공급자 함수(Supplier Function)**를 사용하여 호출 값을 반환합니다.

```java
String nullName = null;
String name = Optional.ofNullable(nullName).orElseGet(() -> "result");
```

### 4.6. Optional.orElseThrow

`orElseThrow` 메소드는 `orElse` 및 `orElseGet` 의 뒤를 이으며 최종적으로 연산을 끝낸후 `Optional` 객체가 비어있으면 예외가 발생합니다.

```java
String nullName = null;
String name = Optional.ofNullable(nullName).orElseThrow(
    IllegalArgumentException::new);
```

### 4.7. Difference Between orElse and orElseGet

`Optional` 개념을 처음 접하면 `orElse` 와 `orElseGet` 의 차이점을 모르는 경우가 많습니다.

하지만 차이점을 명확히 모르면 코드의 성능에 크게 영향을 줄 수 있습니다. 이를 예시를 통해 알아보겠습니다. 먼저 인수를 사용하지 않고 기본값을 반환하는 메소드를 만들겠습니다.

```java
public String getDefaultValue() {
    System.out.println("getDefaultValue is Call");
    return "Default Value";
}
``` 

이 함수를 `orElse`, `orElseGet` 으로 접근하여 래핑 된 값을 가져와보겠습니다.

```java
String text = null;

String defaultText = Optional.ofNullable(text).orElseGet(this::getDefaultValue);
defaultText = Optional.ofNullable(text).orElse(getDefaultValue());
```

실행 결과는 아래와 같습니다. 두 메소드 모두 래핑 된 값이 없을 때는 똑같은 방식으로 작동합니다.

```java
getDefaultValue is Call
getDefaultValue is Call
```

하지만 값이 존재할 때는 어떻게 동작하는지 알아보겠습니다.

```java
String text = "text";

System.out.println("orElseGet is Call");
String defaultText 
  = Optional.ofNullable(text).orElseGet(this::getDefaultValue);

System.out.println("orElse is Call");
defaultText = Optional.ofNullable(text).orElse(getDefaultValue());
```

실행 결과는 아래와 같습니다. 가장 큰 차이점은 `orElse` 메소드는 값이 `null` 여부에 상관없이 항상 함수가 호출됩니다.

```java
orElseGet is Call
orElse is Call
getDefaultValue is Call
```

여기서 큰 문제가 발생할 수 있습니다. 앞서 정의한 `getDefaultValue()` 함수 내부에서 새로운 객체를 생성해서 초기화를 시켜주면, `Optional` 내부 값에 관계없이 호출이 되므로 값이 변경될 수 있기 때문입니다.

버그는 사소한 것에서부터 올 수 있으니 모두 조심합시다. 

> 참고자료

* [JDK 8 Release Notes](https://www.oracle.com/java/technologies/javase/8-relnotes.html)
* [Guide To Java 8 Optional](https://www.baeldung.com/java-optional)
* [Throw Exception in Optional in Java 8](https://www.baeldung.com/java-optional-throw-exception)
* [Java Optional ? orElse() vs orElseGet()](https://www.baeldung.com/java-optional-or-else-vs-or-else-get)
