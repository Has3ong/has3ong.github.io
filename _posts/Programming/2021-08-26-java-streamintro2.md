---
title:  "Java 8 Stream API 살펴보기 -2- Stream 가공하기 / 결과 만들기"
excerpt: "Java 8 Stream API 살펴보기 -2- Stream 가공하기 / 결과 만들기"
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

본 포스트에서는 Stream 에서 데이터를 가공하고, 결과를 반환하는 메소드에 대해 알아보겠습니다.

함수가 다양하고 많기 때문에 간단하게 설명하면서 진행하겠습니다.

* 가공하기
  * Filtering
  * Mapping
  * Sorting
  * Iterating
* 결과 만들기
  * Calculating
  * Reduction
  * Collecting
  * Matching
  * Iterating

결과 만들기에서 `findAny()`, `findFirst()` 함수는 다음 포스트에서 다루겠습니다.

## 2. 가공하기

### 2.1. Filtering

#### 2.1.1. filter

필터(filter) 는 Stream 내 요소들을 하나씩 비교하여 걸러내는 메소드입니다. 인자로 받는 `Predicate` 는 `boolean` 을 리턴하는 함수형 인터페이스이며, 조건식을 표현하는 데 사용됩니다.

```java
Stream<T> filter(Predicate<? super T> predicate);
```

Stream 에서 "A" 와 동일한 요소를 걸러내는 예제입니다.

```java
List<String> list = Arrays.asList("A", "B", "C", "D");
Stream<String> stream = list.stream()
                            .filter(s -> s.equals("A")); // [A]
```

#### 2.1.2. limit

최대 `maxSize` 까지 Stream 을 리턴합니다. 보통 `generate()` 와 같이 사용합니다.

```java
Stream<T> limit(long maxSize);
```

```java
Stream<String> stream = Stream.generate(() -> "element").limit(2);
// [element, element]
```

#### 2.1.3. limit

Stream 의 상위 `n` 개 요소를 생략한 Stream 을 리턴합니다.

```java
Stream<T> skip(long n);
```

```java
List<Integer> list = Arrays.asList(5, 7, 3, 1, 2, 6, 1, 9, 0);
Stream<Integer> stream = list.stream()
                             .sorted(Comparator.reverseOrder())
                             .skip(4); // [3, 2, 1, 1, 0]
```

#### 2.1.4. distinct

중복제거(distinct) 는 Stream 에서 중복된 요소를 제거한 Stream 을 리턴합니다.

```java
Stream<T> distinct();
```

간단한 예제를 보겠습니다.

```java
List<String> list = Arrays.asList("A", "A", "B", "B", "C", "C");
Stream<String> stream = list.stream()
                            .distinct(); // [A, B, C]
```

### 2.2. Mapping

#### 2.2.1. map

맵(map) 은 Stream 내 요소들을 하나씩 특정 값으로 변환합니다. 이때 람다를 인자로 받습니다.

```java
<R> Stream<R> map(Function<? super T, ? extends R> mapper);
```

문자열을 소문자로 바꿔주는 예제입니다.

```java
List<String> list = Arrays.asList("A", "B", "C", "D");
Stream<String> stream = list.stream()
                            .map(String::toLowerCase); // [a, b, c, d]
```

#### 2.2.2. mapToInt, mapToLong, mapToDouble

`mapToInt()`, `mapToLong()`, `mapToDouble()` 함수들은 Stream 을 해당하는 타입으로 바꿔줍니다.

```java
IntStream mapToInt(ToIntFunction<? super T> mapper);

LongStream mapToLong(ToLongFunction<? super T> mapper);

DoubleStream mapToDouble(ToDoubleFunction<? super T> mapper);
```

`mapToInt()` 를 예시로 간단한 예제를 알아보겠습니다.

```java
List<String> list = Arrays.asList("1", "2", "3", "4");
IntStream stream = list.stream()
                        .mapToInt(s -> Integer.parseInt(s)); // [1, 2, 3, 4]
```

### 2.2.3. flatMap, flatMapToInt, flatMapToLong, flatMapToDouble

`flatMap()` 은 조금 더 복잡합니다. 인자로 `mapper` 를 받고 리턴 타입이 `Stream` 입니다. 새로운 Stream 을 생성해서 리턴하는 람다를 넘겨야 하는데, `flatMap` 은 중첩 구조를 한 단계 제거하고 단일 컬렉션으로 만들어줍니다.

```java
<R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper);
```

간단한 예제로 살펴보겠습니다.

```java
List<List<String>> list =  Arrays.asList(Arrays.asList("a"), Arrays.asList("b")); // [[a], [b]]
List<String> flatMap = list.stream()
                            .flatMap(Collection::stream)
                            .collect(Collectors.toList()); // [a, b]
```

`flatMapToInt()`, `flatMapToLong()`, `flatMapToDouble()` 는 위에서 설명한 `mapToInt()` 와 동일합니다.

### 2.3. Sorting

#### 2.3.1. sorted

정렬도 다른 정렬과 동일하게 `Comparator` 를 사용합니다.

```java
Stream<T> sorted(Comparator<? super T> comparator);
```

인자 없이 출력하면 디폴트 값은 오름차순입니다.

```java
List<Integer> list = Arrays.asList(5, 7, 3, 1, 2, 6, 1, 9, 0);
Stream<Integer> stream = list.stream()
                             .sorted(); // [0, 1, 1, 2, 3, 4, 5, 6, 7, 9]
```

```java
List<Integer> list = Arrays.asList(5, 7, 3, 1, 2, 6, 1, 9, 0);
Stream<Integer> stream = list.stream()
                             .sorted(Comparator.reverseOrder());
                             // [9, 7, 6, 5, 4, 3, 2, 1, 1, 0]
```

### 2.4. Iterating

#### 2.4.1 peak

특정 결과를 반환하지 않는 `Consumer` 를 인자로 받으며, Stream 내 특정 작업을 수행할 뿐 결과에 영향을 미치지 않습니다. 아래 예제처럼 작업을 처리하는 중간에 결과를 확인할 때 사용할 수 있습니다.

```java
Stream<T> peek(Consumer<? super T> action);
```

```java
List<Integer> list = Arrays.asList(5, 7, 3, 1, 2, 6, 1, 9, 0);
Stream<Integer> stream = list.stream()
                             .peek(System.out::println)
                             .sorted(Comparator.reverseOrder());
```

## 3. 결과 만들기

### 3.1. Reduction

Stream 은 `reduce()` 라는 메소드를 이용해 결과를 만듭니다. 이 메소드는 3 가지의 파라미터를 가지고 있습니다.

* `accumulator` : 각 요소를 처리하는 계산 로직
* `identity` : 계산을 위한 초깃값으로 Stream 이 비어서 계산할 내용이 없더라도 리턴한다
* `combiner` : 병렬 Stream 처리할 때 나눠서 계산한 결과를 하나로 합치는 로직.

```java
Optional<T> reduce(BinaryOperator<T> accumulator);

T reduce(T identity, BinaryOperator<T> accumulator);

<U> U reduce(U identity,
                 BiFunction<U, ? super T, U> accumulator,
                 BinaryOperator<U> combiner);
```

각각 인자별로 예제를 살펴보겠습니다.

```java
// 45
OptionalInt reduce = 
    IntStream.range(1, 10)
             .reduce((a, b) -> { return a + b; });
```

```java
// 55
Integer reduce = 
    IntStream.range(1, 10)
             .reduce(10, Integer::sum);
```

```java
// 36
Integer reduce = 
    Stream.of(1, 2, 3)
          .parallel()
          .reduce(10, Integer::sum, (a, b) -> { return a + b; });
```

### 3.2. Collecting

필요한 요소룰 수집하여 새로운 `Collection` 으로 반환하는 메소드입니다. 이번 포스트에서는 간단히 다루고 추후 `toList()`, `joining()` 과 같은 세부 메소드를 다루겠습니다.


```java
<R> R collect(Supplier<R> supplier,
                  BiConsumer<R, ? super T> accumulator,
                  BiConsumer<R, R> combiner);

<R, A> R collect(Collector<? super T, A, R> collector);
```

아래 예제는 문자열 Stream 에서 "b" 가 포함된 문자를 `filter` 를 통하여 거르고 `collect()` 메소드를 이용하여 다시 `List` 로 만들어주는 예제입니다.

```java
List<String> list =
    Stream.of("a", "b", "c").filter(element -> element.contains("b"))
                            .collect(Collectors.toList());
```    

`Collector` 에는 다양한 메소드가 존재하기 때문에 [Java 8 Stream API 살펴보기 -4- Colector 살펴보기](/_posts/2021-08-28-java-streamintro4.md) 위 포스에서 상세하게 다루겠습니다.

### 3.3. Calculating

기본형 Stream 의 통계가 있으며 T 타입 Stream 의 통계가 있습니다.

```java
Optional<T> min(Comparator<? super T> comparator);

Optional<T> max(Comparator<? super T> comparator);

long count();
```

기본형 Stream 통계

* `count()`
* `sum()`
* `average()`
* `min()`
* `max()`

### 3.4. Matching

#### 3.4.1. anyMatch, allMatch, noneMatch

Stream 에서 찾고자 하는 객체가 존재하는지 탐색을 하고 `boolean` 타입을 리턴합니다. 메소드는 `anyMatch()`, `allMatch()`, `noneMatch()` 가 있습니다.

* `anyMatch()` 는 하나라도 조건에 맞는 요소가 있으면 `true` 를 리턴
* `allMatch()` 는 모든 요소가 조건에 맞아야 `true` 를 리턴
* `noneMatch()` 는 조건에 맞는 객체가 없어야 `true` 를 리턴

```java
boolean anyMatch(Predicate<? super T> predicate);

boolean allMatch(Predicate<? super T> predicate);

boolean noneMatch(Predicate<? super T> predicate);
```

예제를 통해 한번에 알아보겠습니다.

```java
List<String> list = Arrays.asList("A", "B", "C", "D");

boolean anyMatch = list.stream()
                        .anyMatch(s -> s.contains("A")); // true
boolean allMatch = list.stream()
                        .allMatch(s -> s.contains("A")); // false
boolean noneMatch = list.stream()
                        .noneMatch(s -> s.contains("A")); // false
```

### 3.5. Iterating

#### 3.5.1. forEach

`forEach()` 는 요소를 돌면서 실행하는 최종 작업입니다. `peek()` 와의 차이는 중간 작업이냐, 최종 작업이냐의 차이가 있습니다.

```java
void forEach(Consumer<? super T> action);
```

```java
List<Integer> list = Arrays.asList(1, 2, 3);
list.stream().forEach(System.out::println); // 1 2 3
```

#### 3.5.2. forEachOrdered

병렬처리에서 순서를 보장할 때 사용할 수 있습니다.

```java
void forEachOrdered(Consumer<? super T> action);
```

```java
// 651728934
IntStream.range(1, 10).parallel().forEach(System.out::print);
// 123456789
IntStream.range(1, 10).parallel().forEachOrdered(System.out::print);
```

> 참고자료

* [JDK 8 Release Notes](https://www.oracle.com/java/technologies/javase/8-relnotes.html)
* [Java Streams](https://www.baeldung.com/java-streams)

