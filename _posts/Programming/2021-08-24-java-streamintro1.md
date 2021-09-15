---
title:  "Java 8 Stream API 살펴보기 -1- Stream 생성하기"
excerpt: "Java 8 Stream API 살펴보기 -1- Stream 생성하기"
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

## 1. Intro, Why Java 8?

이번 포스트에서 다룰 Java 8 은 2014년에 발표된 자바 버전입니다. 2014년 이후 지금까지 꾸준히 Java 의 버전은 올라갔으며, 현재 2021년 3월 16일 기준으로 JDK 16이 릴리즈 됐습니다. 

![image](/assets/images/java/java8_01/java8_01_01.png)

> 출처 : https://openjdk.java.net/projects/jdk/16/

7년 동안 많은 Java 버전이 나왔는데 최신버전이 아닌, 7년이나 지난 Java 8 을 왜 다룰까요? 그리고 많은 곳에서 Java 8 의 추가기능을 따로 배우고 중요시할까요?

본론에 앞서 Stackoverflow 에서 조사한 프로그래밍 언어별 연봉을 알아보겠습니다.

![image](/assets/images/java/java8_01/java8_01_02.png)

> 출처 : https://insights.stackoverflow.com/survey/2021

Java 는 하위권에 있으며, Java 보다 낮은 언어는 Delphi, Matlab, PHP, Dart 가 있습니다. 반면 상위권에 있는 Clojure, F#, Elixir, Erlang, Scala 같은 언어들을 분석해보면 한 가지 공통점이 있는데 바로 **함수형 프로그래밍 언어(Functional Programming Language)** 입니다.

그래서 기존 객체지향 프로그래밍 언어인 Java 에서 `함수형 프로그래밍 패러다임의 지원` 이 가능한 Java 8 을 따로 배우고 중요하게 여겨집니다. Java 8 에서의 주요 변경사항은 다음과 같습니다.

1. 람다 표현식(lambda expression)
2. 스트림 API(stream API)
3. java.time 패키지
4. 나즈혼(Nashorn)

하나하나씩 간단하게만 서술해보겠습니다.

1. 람다 표현식이란 익명 클래스의 한 개의 메소드를 식으로 표현한 것입니다. 여기서 익명 클래스란 말 그대로 이름이 없는 클래스로써, 단 한 개의 객체만을 생성할 수 있는 일회용 클래스입니다.
2. 스트림 API 는 컬렉션을 다루는 새로운 방법을 제공하는 API 이며, 컬렉션, 배열등 저장한 데이터에 대하여 filtering, macthing, mapping 과 같은 복잡한 데이터 처리 작업을 수행하는 데 사용합니다.
3. Java 8 에서는 `java.time` 패키지에 `LocalDateTime` 과 타임존 개념까지 포함할 수 있는 `ZonedDateTime` 이 추가되었다.
4. 지금까지 자바스크립트의 기본 엔진으로는 모질라의 라이노(Rhino) 가 사용되었으며, Java 8 버전부터는 자바스크립트의 새로운 엔진으로 오라클의 나즈혼 (Nashorn)을 도입

본 포스트에서는 Java 8 에 주된 변경사항 중 **2. 스트림 API** 에 대해서 다룰 예정입니다. 포스트는 총 3개의 포스트로 나눌 예정이며, 스트림 API 를 이용하여 Java 에서 함수형 프로그래밍을 사용하는 방법을 알아볼 것입니다.

이번 포스트에서는 Stream 에 대한 기본 사항과 생성하는 방법을 알아보겠습니다.

## 2. Stream

자바에서는 많은 양의 데이터를 저장하기 위해서 Array 나 Collection 을 사용합니다. 또한, 이렇게 저장된 데이터에 접근하기 위해서는 반복문이나 반복자(iterator)를 사용하여 매번 코드를 작성해야 했습니다.

하지만 이렇게 작성된 코드는 길이가 너무 길고 가독성도 떨어지며, 코드의 재사용이 거의 불가능합니다. 그리고 데이터베이스의 쿼리와 같이 정형화된 처리 패턴을 가지지 못했기에 데이터마다 다른 방법으로 접근해야만 했습니다.

이러한 문제점을 극복하기 위해서 Java 8에서 도입된 방법이 바로 Stream API입니다. 기존 for 문이나 반복자로 처리했던 많은 일을 간결한 코드로 작성할 수 있게 해줍니다.

## 3. Stream API 의 특징

Stream API 의 특징은 크게 3가지가 있습니다.

1. 외부 반복을 통해 작업하는 컬렉션과는 달리 내부 반복(internal iteration)을 통해 작업을 수행한다.
2. 원본 데이터를 변경하지 않는다.
3. 재사용이 가능한 컬렉션과는 달리 단 한 번만 사용할 수 있다.

각각의 특징에 대해 간략하게 알아보겠습니다. 먼저 아래와 같이 간단한 String 배열을 선언하고 Stream 으로 만들어줍니다.

```java
String[] arr = {"Java", "C++", "Python", "Scala", "Go"} ;
Stream<String> stream = Arrays.stream(arr) ;
```

### 3.1. 외부 반복을 통해 작업하는 컬렉션과는 달리 내부 반복(internal iteration)을 통해 작업을 수행한다.

Stream 을 이용하면 코드가 간결해지는 이유 중 하나는 '내부 반복' 때문입니다. 기존에는 반복문을 사용하기 위해서 `for`, `while`, `do-while` 등과 같은 루프를 사용해야 했지만, Stream 에서는 그러한 반복 문법을 메소드 내부에 숨기고 있으며, 간결한 코드의 작성이 가능하다. 

```java
stream.forEach(System.out::println);
```

> 출력 결과 

```java
Java
C++
Python
Scala
Go
```

### 3.2. 원본 데이터를 변경하지 않는다.

Stream 은 데이터를 조회하여 원본의 데이터가 아닌 별도의 데이터들로 Stream 을 생성합니다. 그래서 원본 데이터는 조회만 할 뿐이며, Filter 나 Sort 와 같은 작업은 별도의 Stream 요소들에서 처리가 됩니다.

```java
// [C++, Go, Java, Python, Scala]
List<String> list = stream.sorted().collect(Collectors.toList());
```

### 3.3. 재사용이 가능한 컬렉션과는 달리 단 한 번만 사용할 수 있다.

Stream API는 일회용이기 때문에 한번 사용이 끝나면 재사용이 불가능하다. Stream 이 또 필요한 경우에는 Stream 을 다시 생성해주어야 한다. 만약 닫힌 Stream 을 다시 사용한다면 `IllegalStateException` 에러가 발생하게 된다.

```java
stream.forEach(System.out::println);
List<String> list = stream.sorted().collect(Collectors.toList());
```

출력 결과

```java
Java
C++
Python
Scala
Go
Exception in thread "main" java.lang.IllegalStateException: stream has already been operated upon or closed
	at java.util.stream.AbstractPipeline.<init>(AbstractPipeline.java:203)
	at java.util.stream.ReferencePipeline.<init>(ReferencePipeline.java:94)
	at java.util.stream.ReferencePipeline$StatefulOp.<init>(ReferencePipeline.java:647)
	at java.util.stream.SortedOps$OfRef.<init>(SortedOps.java:111)
	at java.util.stream.SortedOps.makeRef(SortedOps.java:51)
	at java.util.stream.ReferencePipeline.sorted(ReferencePipeline.java:389)
	at functionalTest.lambdaTest.main(lambdaTest.java:19)
```

간단한 특징을 알아봤으니 Stream API 의 생성하는 방법을 알아보겠습니다.

## 4. Stream 생성하기

보통 Array 와 Collection 을 이용해서 Stream 을 만들지만, 이 외에도 다양한 방법으로 Stream 을 만들 수 있습니다. 하나씩 살펴보겠습니다.

### 4.1. Stream of Array

아래와 같이 배열을 선언하지 않고 Stream 을 바로 만들어줄 수 있습니다.

```java
Stream<String> stream = Stream.of("Java", "C++", "Python", "Scala", "Go");
```

또한, 선언한 배열을 `Arrays.stream` 을 이용하여 Stream 을 만들 수 있습니다.

```java
String[] arr = {"Java", "C++", "Python", "Scala", "Go"};
Stream<String> streamOfArrayFull = Arrays.stream(arr);
Stream<String> streamOfArrayPart = Arrays.stream(arr, "Scala", "Ruby");
```

### 4.2. Stream of ArrayList

마찬가지로 myBatis 에서 자주 사용하는 ArrayList 도 동일하게 만들어 줄 수 있습니다.

```java
ArrayList<String> arr = new ArrayList<String>(Arrays.asList("Java", "C++", "Python", "Scala", "Go"));
Stream<String> StreamOfArrayList = arr.stream();
```

### 4.3. Stream of Collection

컬렉션 타입(Collection, List, Set)의 경우 인터페이스에 추가된 디폴트 메소드 `stream` 을 이용해서 스트림을 만들 수 있습니다.

```java
Collection<String> collection = Arrays.asList("Java", "C++", "Python", "Scala", "Go");
Stream<String> streamOfCollection = collection.stream();
```

### 4.4. Empty Stream

비어있는 Stream 을 생성하는 경우 `empty()` 메서드를 사용해야 합니다.

```java
Stream<String> empty = Stream.empty();
```

비어있는 Stream 에 대해 `null` 반환을 피하기 위해서는 Stream 을 생성할 때 `empty()` 메서드를 활용하면 됩니다.

```java
public Stream<String> streamOf(List<String> list) {
    return list == null || list.isEmpty() ? Stream.empty() : list.stream();
}
```

### 4.5. Stream.builder()

빌더(Builder)를 사용하면 스트림에 직접적으로 원하는 값을 넣을 수 있습니다. 그리고 빌더를 사용할 때는 원하는 유형의 문을 오른쪽에 반드시 지정해야 합니다. 그렇지 않으면 `build()` 메소드가 `Stream<Object>` 형태의 인스턴스를 생성하게 됩니다.


```java
Stream<String> builder = Stream.<String>builder().add("Java").add("Python").add("C++").build();
```

### 4.6. Stream.generate()

`generate()` 메소드는 Stream 생성을 위해 `Supplier<T>` 를 허용합니다. 결과로 나오는 Stream 의 크기가 정해져 있지 않고 무한하므로 개발자가 특정 크기를 명시하여 크기를 제한해야 합니다.

```java
Stream<String> generate = Stream.generate(() -> "element").limit(10);
```

무한 스트림을 만드는 또 다른 방법은 `iterate()` 가 있습니다.

### 4.7. Stream.iterate()

`iterate()` 메소드를 이용하면 초깃값과 해당 값을 다루는 람다를 이용하여 Stream 에 들어갈 요소를 반환합니다. 아래는 초깃값이 40 이고, 2씩 증가하는 요소들이 Stream 으로 들어가게 됩니다. `generate()` 와 마찬가지로 Stream 의 크가 무한하므로 크기를 명시해서 제한해줘야 합니다.

```java
Stream<Integer> iterate = Stream.iterate(40, n -> n + 2).limit(20);
```

### 4.8. Stream of Primitives

Java 8 에서는 `int`, `long`, `double` 의 3 가지 기본 유형에서 Stream 을 생성할 수 있습니다. `Stream<T>` 는 제네릭 인터페이스이고, 제네릭과 같이 형식 매개변수로 프리미티브를 사용할 수 없으므로 `IntStream`, `LongStream`, `DoubleStream` 의 3 가지 인터페이스가 생성되었습니다. 이 인터페이스를 사용하면 생산성을 높일 수 있습니다.

```java
IntStream intstream = IntStream.range(1, 3);            //[1, 2]
LongStream longstream = LongStream.rangeClosed(1, 3);   //[1, 2, 3]
```

Java 8 부터 `Random` 클래스는 Stream 을 생성하기 위한 광범위한 메서드를 제공합니다. 예를 들어 아래 코드는 세 개의 난수가 있는 `DoubleStream` 을 만듭니다.

```java
Random random = new Random();
DoubleStream doubleStream = random.doubles(3);
```

### 4.9. Stream of String

String 을 이용하여 Stream 을 생성할 수 있습니다. 아래는 문자열의 각 문자를 `IntStream` 으로 변환하는 예제입니다.

```java
IntStream streamOfChars = "ABC".chars(); // [65, 66, 67]
```

정규표현식을 이용하여 문자열을 자르고 Stream 을 만들 수도 있습니다.

```java
Stream<String> stringstream = Pattern.compile(", ").splitAsStream("A, B, C"); // [A, B, C]
```

### 4.10. Stream of File

Java NIO 의 `File` 클래스를 사용하면 `lines()` 메소드를 통하여 텍스트 파일의 `Stream<String>` 을 생성할 수 있습니다. 텍스트의 모든 라인은 Stream 의 데이터가 됩니다.

또한 `Charset` 은 `lines()` 메소드의 인수로 지정할 수 있습니다.

```java
Path filepath = Paths.get("C:\\file.txt");
Stream<String> streamOfStrings = Files.lines(filepath);
Stream<String> streamWithCharset = Files.lines(filepath, Charset.forName("UTF-8"));
```

### 4.11. Connect to Stream

`Stream.concat()` 을 이용하여 Steram 을 연결해 새로운 Stream 을 만들 수 있습니다.

```java
Stream<String> stream1 = Stream.of("A", "B", "C");
Stream<String> stream2 = Stream.of("D", "E", "F");
Stream<String> concat = Stream.concat(stream1, stream2);
// [A, B, C, D, E, F]
```

### 4.12. Parallel Stream

Stream 생성 시 사용하는 `stream` 대신 `parallelStream` 메소드를 사용해 병렬 Stream 을 생성할 수 있습니다.

```java
Stream<Product> parallel = productList.parallelStream();
```

또한, 기존 Stream 을 `parallel()` 을 이용하여 병렬 처리할 수 있습니다.

```java
String[] arr = {"Java", "C++", "Python", "Scala", "Go"} ;
Stream<String> stream = Arrays.stream(arr) ;
stream.parallel().forEach(System.out::println);
```

> 출력결과

```
Python
Scala
Java
C++
Go
```

지금까지 Stream 의 특징과 Stream 을 생성하는 방법을 간단하게 알아봤습니다. 다음 포스트에서는 Stream 을 가공하고 결과를 만드는 방법을 알아보겠습니다.


> 참고자료

* [JDK 8 Release Notes](https://www.oracle.com/java/technologies/javase/8-relnotes.html)
* [Java Streams](https://www.baeldung.com/java-streams)