---
title:  "Java Junit5 Assert 함수 정리"
excerpt: "Java Junit5 Assert 함수 정리"
categories:
  - Programming
tags:
  - Programming
  - Java
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

TDD 공부하는 김에 정리하겠습니다.

`assert` 함수는 [JUnit5 Documentation](https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html) 참고했습니다.

### assertTrue & assertFalse​

Assertion 조건이 `true` 인지 `false` 인지 확인합니다.

```java
assertTrue("5 is greater then 4", 5 > 4);
assertFalse("5 is not greater then 6", 5 > 6);
```

### assertAll

JUnit5에서 새로 도입된 Assertion 구문입니다.

이 Assertion를 사용하면 실행되고 실패가 함께 보고되는 그룹화된 Assertion을 만들 수 있습니다.

```java
Object obj = null;
assertAll(
  "heading",
  () -> assertEquals(100, 10 * 10),
  () -> assertEquals("java", "JAVA".toLowerCase()),
  () -> assertNull(obj, "obj is null")
);
```

그룹화된 Assertion는 실행 파일 중 하나가 블랙리스트 예외(예: `OutOfMemoryError`)를 `throw`하는 경우에만 중단됩니다.

### assertArrayEquals

두 Array 를 비교할 때 사용하는 Assertion입니다.

```java
char[] expected = {'J', 'A', 'V', 'A'};
char[] actual = "JAVA".toCharArray();

assertArrayEquals(expected, actual);
```

만약 두 배열이 모두 `null`이면 두 배열이 같다고 간주합니다.

```java
int[] expected = null;
int[] actual = null;

assertArrayEquals(expected, actual);
```

### assertEquals​ & assertNotEquals

두 값을 비교하여 일치 여부 판단합니다.

```java
String expected = "has3ong";
String actual = "has3ong";

assertEquals(expected, actual);
```
`assertEquals` 를 보완하는 `assertNotEquals` 는 기대값과 실제 값이 일치하지 않는 경우를 판단합니다.

```java
Integer value = 5; // result of an algorithm
    
assertNotEquals(0, value, "The result cannot be 0");
```

Assertion 실패시 오류 메세지도 정의할 수 있습니다.

```java
assertEquals("failure - strings are not equal", expected, actual);
```

### assertIterableEquals​

`assertItableEquals`는 `Iterable`이 동일한 유형일 필요는 없지만, 동일한 순서로 동일한 값을 반환해야합니다.

```java
Iterable<String> expectedList = new ArrayList<>(asList("Java", "Junit", "Test"));
Iterable<String> actualList = new LinkedList<>(asList("Java", "Junit", "Test"));

assertIterableEquals(expectedList, actualList);
```

### assertLinesMatch​

`assertLinesMatch`는 예상되는 문자열 목록이 실제 목록과 일치하는지 확인합니다.

이 방법은 `assertEquals` 및 `assertItableEquals`와 다르며, 이는 예상되는 라인과 실제 라인에 대해 아래와 같은 알고리즘을 수행하기 때문입니다.

1. 예상 라인이 실제 라인과 동일한지 확인. `true` 인 경우 다음 라인으로 이동.
2. 예상되는 라인을 정규식으로 처리하고 `String.matches()` 메서드를 사용하여 검사를 수행 `true`인 경우 다음 라인으로 이동
3. 예상되는 라인이 fast-forward marker인지 확인. `true`인 경우 빨리 감기(fast-forward)를 적용하고 1단계부터 알고리즘을 반복.

이 어설션을 사용하여 문자열의 두 목록에 일치하는 줄이 있다고 판별할 수 있는 방법을 알아보겠습니다.

```java
List<String> expected = asList("Java", "\\d+", "JUnit");
List<String> actual = asList("Java", "11", "JUnit");

assertLinesMatch(expected, actual);
```

### assertNull​ & assertNotNull

객체가 `null` 인지 판별합니다.

```java
Object java = null;

assertNull(java, () -> "The java should not be null");

Object python = new Object();

assertNotNull(python, () -> "The python should not be null");
```

### assertSame & assertNotSame

두 변수가 동일한 객체를 참조하는지 판별합니다.

```java
String language = "Java";
Optional<String> optional = Optional.of(language);

assertSame(language, optional.get());

Object java = new Object();
Object python = new Object();

assertNotSame(java, python);
```

### assertThrows

특정 예외가 발생하였는지 확인합니다.

```java
Throwable exception = assertThrows(
  IllegalArgumentException.class, () -> {
    throw new IllegalArgumentException("Exception message");
  }
);
assertEquals("Exception message", exception.getMessage());
```

### assertDoesNotThrow​

에러가 발생하지 않으면 `true`를 반환합니다.

```java
String message = assertDoesNotThrow(() -> { return "Hello World!"; } );
```

### assertThrowsExactly​

특정 예외를 발생하였는지 확인합니다. `assertThrows`는 예외가 자식 유형인 경우에 `true`를 반환하기 때문에 더 정확합니다.

```java
Throwable exception = assertThrowsExactly(
  IllegalArgumentException.class, () -> {
    throw new IllegalArgumentException("Exception message");
  }
);
assertEquals("Exception message", exception.getMessage());
```

### assertTimeout​ & assertTimeoutPreemptively​

테스트가 지정한 시간 안에 끝나는지 판별할 때 사용합니다.

* 지정한 시간보다 오래 걸려도 끝날 때까지 대기 : `assertTimeout`
* 지정한 시간을 초과하면 바로 종료 : `assertTimeoutPreemptively`

```java
assertTimeout(
  ofSeconds(2), () -> {
    // code that requires less than 2 minutes to execute
    Thread.sleep(1000);
  }
);
```

### fail

`fail` Assertion이 `AssertionFailedError`를 발생시키는 테스트에 실패합니다. 실제 예외가 발생했는지, 또는 테스트 개발 중에 실패하기를 원할 때 이를 검증하는 데 사용할 수 있다.

```java
try {
  methodThatShouldThrowException();
  fail("Exception not thrown");
} catch (UnsupportedOperationException e) {
  assertEquals("Operation Not Supported", e.getMessage());
}
```

> 참고자료

* [JUnit5 Documentation](https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html)
* [Assertions in JUnit 4 and JUnit 5](https://www.baeldung.com/junit-assertions)