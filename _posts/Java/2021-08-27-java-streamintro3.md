---
title:  "Java 8 Stream API 살펴보기 -3- findAny() vs findFirst()"
excerpt: "Java 8 Stream API 살펴보기 -3- findAny() vs findFirst()"
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

find 는 Stream 에 요소를 찾는 메소드로 `findFirst()` 와 `findAny()` 가 존재합니다. 두 메소드 모두 Stream 에서 지정한 첫 번째 요소를 찾는 메소드입니다. 

* `findAny()` 는 Stream 에서 가장 먼저 탐색 되는 요소를 리턴
* `findFirst()` 는 조건에 일치하는 요소들 중에 Stream 에서 순서가 가장 앞에 있는 요소를 리턴

## 2. Stream.findFirst()

`findFirst()` 메서드는 Stream 에서 첫 번째 요소를 찾아서 `Optional` 타입으로 리턴합니다. 조건에 일치하는 요소가 없다면 `empty` 가 리턴됩니다. 따라서 Stream 의 첫 번째 요소를 구체적으로 원할 때 이 방법을 사용합니다.

```java
List<String> list = Arrays.asList("A", "A1", "A2", "B", "C", "D");
Optional<String> element = list.stream()
                                .filter(s -> s.startsWith("A"))
                                .findFirst();
System.out.println(element.get()); // A
```

`findFirst()` 메서드의 동작은 병렬 처리에서도 동일합니다.

```java
List<String> list = Arrays.asList("A", "A1", "A2", "B", "C", "D");
Optional<String> element = list.stream()
                                .parallel()
                                .filter(s -> s.startsWith("A"))
                                .findFirst();
System.out.println(element.get()); // A
```

## 3. Stream.findAny()

`findAny()` 도 마찬가지로 조건에 맞는 요소 1개를 리턴합니다.

```java
List<String> list = Arrays.asList("A", "A1", "A2", "B", "C", "D");
Optional<String> element = list.stream()
                                .filter(s -> s.startsWith("A"))
                                .findAny();
System.out.println(element.get()
```

`findFirst()` 와 `findAny()` 의 가장 큰 차이는 병렬로 처리할 때 발생합니다. 병렬 처리를 진행하면, `findAny()` 는 멀티스레드가 Stream 을 처리할 때 가장 먼저 찾은 요소를 리턴하여, 실행할 때마다 리턴값이 달라집니다.

최대 성능을 내기 위해 병렬 작업을 처리하는 경우 리턴값을 안정적으로 반환할 수 없습니다.

```java
List<String> list = Arrays.asList("A", "A1", "A2", "B", "C", "D");
Optional<String> element = list.stream()
                                .parallel()
                                .filter(s -> s.startsWith("A"))
                                .findAny();
System.out.println(element.get()); // A or A1 or A2
```

> 참고자료

* [JDK 8 Release Notes](https://www.oracle.com/java/technologies/javase/8-relnotes.html)
* [Java Streams](https://www.baeldung.com/java-streams)