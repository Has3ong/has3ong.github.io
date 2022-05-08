---
title:  "Java 8 Stream API 살펴보기 -4- Collector 살펴보기"
excerpt: "Java 8 Stream API 살펴보기 -4- Collector 살펴보기"
categories:
  - Programming
tags:
  - Java
  - JDK8
  - Stream
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

* [Java 8 Stream API 살펴보기 -1- Stream 생성하기](/programming/java-streamintro1)
* [Java 8 Stream API 살펴보기 -2- Stream 가공하기 / 결과 만들기](/programming/java-streamintro2)
* [Java 8 Stream API 살펴보기 -3- findAny() vs findFirst()](/programming/java-streamintro3)
* [Java 8 Stream API 살펴보기 -4- Collector 살펴보기](/programming/java-streamintro4)

## 1. Intro

본 포스트에서는 `Collector` 에서 제공하는 메소드들에 대해서 상세하게 다뤄보겠습니다.

## 2. Collectors

`Stream.collect()`는 Java 8의 Stream API 의 터미널 메서드 중 하나입니다. `collect` 메소드는 Stream 처리에서 사용되는 또 다른 종료 작업입니다. `Collector` 타입의 인자를 받아서 처리하며, 자주 사용하는 작업은 `Collectors` 객체에서 제공하고 있습니다.

미리 정의한 모든 구현은 `Collectors` 클래스에서 찾을 수 있습니다. 가독성을 높이기 위해 다음과 같이 정적 `import`를 사용하는 것이 일반적입니다.

```java
import static java.util.stream.Collectors.*;
```

또는 아래와 같이 개별로 선언하기도 합니다.

```java
import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toMap;
import static java.util.stream.Collectors.toSet;
```

본 포스트에서는 `Person` 이라는 클래스를 이용하며 아래 리스를 이용하여 예제를 다루겠습니다.

```java
class Person {
	  String name ;
	  Integer age ;
	  
	  public Person(String name, Integer age) {
		  this.name = name ;
		  this.age = age ;
	  }

	  public void setName(String name) {
	    this.name = name ;
	  }

	  public String getName() {
	    return this.name ;
	  }

	  public void setAge(Integer age) {
	    this.age = age ;
	  }

	  public Integer getAge() {
	    return this.age ;
	  }
}
```

```java
List<Person> sampleList = Arrays.asList(
				new Person("John", 23)
				, new Person("Mark", 13)
				, new Person("Gosling", 66)
				, new Person("Guido", 33));
```

### 2.1. Collectors.toList()

`toList` 메소드는 모든 Stream 요소를 List 인스턴스로 수집하는 데 사용할 수 있습니다. 중요한 점은 이 메서드로 특정 List 를 구현하는 것이 아니며, 더 잘 제어하기 위해서는 `toCollection()` 을 사용할 수 있습니다.

아래 예제를 통해 Stream 인스턴스를 만든 다음 List 인스턴스로 수집해 보겠습니다.

```java
List<Person> result = 
				sampleList.stream().collect(toList());
```

### 2.2. Collectors.toSet()

`toSet()` 메소드를 사용하여 모든 스트림 요소를 Set 인스턴스로 수정할 수 있습니다. 위와 마찬가지로 이 방법으로는 특정 Set 구현하는것이 아니며, 더 잘 제어하기 위해서는 `toCollection()` 로 사용하면 됩니다.

요소의 시퀀스를 나타내는 스트림 인스턴스를 만든 다음 집합 인스턴스로 수집합니다.

```java
List<Person> result = 
				sampleList.stream().collect(toSet());
```

Set 에는 중복 요소가 없습니다. 컬렉션에 서로 동일한 요소가 포함되면 해당 요소는 결과 집합에 한 번만 표시됩니다.

```java
List<String> listWithDuplicates = Arrays.asList("a", "bb", "c", "d", "bb");
// [bb, a, c, d]
Set<String> result = listWithDuplicates.stream().collect(toSet());
assertThat(result).hasSize(4);
```

### 2.3. Collectors.toCollection()

앞서 살펴봤듯이, `toList()`, `toSet()` 메소드는 특정한 List, Set 을 구현할 수 없습니다. 특정 Collection 을 구현하려면 `toCollection()` 을 사용해야 합니다.

```java
List<String> result = givenList.stream()
        .collect(toCollection(LinkedList::new))
```

변경 불가능한 컬렉션에서는 잘 작동하지 않습니다. 이 경우 사용자가 컬렉터를 구현하거나 `collectAndThen()` 을 사용해야 합니다.

### 2.4. Collectors.toMap()

`toMap()` 메소드는 Stream 요소를 Map 인스턴스로 수집하는 데 사용하며, 이를 위해서 두 가지 기능을 제공합니다.

* keyMapper
* valueMapper

keyMapper 를 사용하여 Stream 요소에서 keyMapper 를 추출하고 Map 키를 추출하고 valueMapper 를 사용하여 지정된 키와 연결된 값을 추출합니다.

이런 요소를 키로 저장하고 길이를 값으로 저장하는 맵으로 수집합니다.

```java
// {John=functionalTest.Person@682a0b20, Guido=functionalTest.Person@3d075dc0, Mark=functionalTest.Person@214c265e, Gosling=functionalTest.Person@448139f0}
Map<String, Person> result = sampleList.stream()
				.collect(toMap(Person::getName, Function.identity()));
```

`Function.identity()` 는 동일한 값을 허용하고 반환하는 함수를 정의하는 방법입니다.

컬렉션에 중복 요소가 포함되어 있으면 Set 과는 달리 `toMap()` 은 중복을 자동으로 필터링하지 않는데, 이 키에 대해 어떤 값을 선택해야 하는지 어떻게 알 수 있을까요?

```java
List<String> listWithDuplicates = Arrays.asList("a", "bb", "c", "d", "bb");
assertThatThrownBy(() -> {
        listWithDuplicates.stream().collect(toMap(Function.identity(), String::length));
}).isInstanceOf(IllegalStateException.class);
```

위 코드처럼 `toMap()` 값이 동일한지 확인하지 않고, 중복 키가 보이면 바로 `IllegalStateException` 을 발생시킵니다.

키 충돌이 있을 있으면 반드시 다른 서명을 사용해서 매핑해야 합니다.

```java
List<String> givenList = Arrays.asList("a", "bb", "c", "d", "bb");
// {bb=2, a=1, c=1, d=1}
Map<String, Integer> result = givenList.stream()
        .collect(toMap(Function.identity(), String::length, (item, identicalItem) -> item));
```

`toMap()` 의 3번째 인자값은 충돌을 처리하는 방법을 지정하는 이진 연산자입니다. 위 경우 동일한 문자열의 길이도 항상 같으므로 충돌 값 중 아무 값이나 선택합니다.

### 2.5. Collectors.collectingAndThen()

`collectiongAntThen` 은 특별한 메소드입니다. 스트림에서 요소들의 수집이 끝난 직후 반환된 결과에 대하여 다른 작업을 수행할 수 있습니다.

아래는 Stream 요소를 List 인스턴스로 수집한 다음 ImmutableList 인스턴스로 변환하는 예제입니다.

```java
List<String> result = sampleList.stream()
				  .collect(collectingAndThen(toList(), ImmutableList::copyOf));
```

### 2.6. Collectors.joining()

`joining()` 메소드는 Stream 의 String 요소들을 합쳐주며, 아래와 같이 사용할 수 있습니다.

```java
// JohnMarkGoslingGuido
String result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.joining());
```

그리고 특정 문자를 사용하여 `separators`, `prefixes`, `postfixes` 를 넣을 수 있습니다.

```java
// John Mark Gosling Guido
String result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.joining(" "));
```

```java
// <John Mark Gosling Guido>
String result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.joining(" ", "<", ">"));
```

### 2.7. Collectors.counting()

`counting` 은 Stream 요소들의 개수를 반환합니다.

```java
Long result = sampleList.stream()
        .collect(counting());
```

### 2.8. Collectors.summarizingDouble/Long/Int()

`summarizingDouble/Long/Int()` 는 Stream 에서 숫자 데이터에 대한 통계 정보를 포함하는 특수 클래스를 리턴하는 메소드입니다. 아래와 같이 사용할 수 있습니다.

```java
// DoubleSummaryStatistics{count=4, sum=135.000000, min=13.000000, average=33.750000, max=66.000000}
DoubleSummaryStatistics result = sampleList.stream()
				.collect(Collectors.summarizingDouble(Person::getAge));
```

### 2.9. Collectors.averagingDouble/Long/Int()

`averagingDouble/Long/Int()` 는 평균을 반환합니다.

```java
// 33.75
Double result = sampleList.stream()
				.collect(Collectors.averagingDouble(Person::getAge));
```

### 2.10. Collectors.summingDouble/Long/Int()

`summingDouble/Long/Int()` 는 합계를 번환합니다.

```java
// 135.0
Double result = givenList.stream()
  .collect(summingDouble(String::length));
```

### 2.11. Collectors.maxBy()/minBy()

`maxBy()/minBy()` 는 Stream 내의 가장 큰 요소와 가장 작은 요소를 반환합니다.

```java
Optional<String> result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.maxBy(Comparator.naturalOrder()));
```

```java
Optional<String> result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.minBy(Comparator.naturalOrder()));
```

### 2.12. Collectors.groupingBy()

`groupingBy()` 메소드는 Stream 내부 요소들을 그룹화하고 그 결과를 Map 인스턴스로 반환합니다.

아래 예제는 문자열의 길이를 그룹화하여 Set 인스턴스에 저장하는 예제입니다.

```java
// {4=[John, Mark], 5=[Guido], 7=[Gosling]}
Map<Integer, Set<String>> result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.groupingBy(String::length, toSet()));
```

### 2.13. Collectors.partitioningBy()

`partitioningBy()` 는 `Predicate` 인스턴스를 허용하고 Stream 요소를 `Boolean` 값을 키, 컬렉션을 값으로 저장하는 Map 인스턴스로 수집합니다.

`true` 키 아래에는 주어진 조건과 일치하는 컬렉션을 찾을 수 있으며, `false` 키 아래에는 조건에 맞지 않는 컬렉션을 찾을 수 있습니다.

```java
// {false=[John, Mark, Guido], true=[Gosling]}
Map<Boolean, List<String>> result = sampleList.stream()
				.map(Person::getName)
				.collect(Collectors.partitioningBy(element -> element.length() > 5));
```

> 참고자료

* [JDK 8 Release Notes](https://www.oracle.com/java/technologies/javase/8-relnotes.html)
* [Java Streams](https://www.baeldung.com/java-streams)