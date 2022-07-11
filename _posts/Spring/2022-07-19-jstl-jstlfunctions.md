---
title:  "JSTL 문법 톺아보기 -5- JSTL functions"
excerpt: "JSTL 문법 톺아보기 -5- JSTL functions"
categories:
  - Spring
tags:
  - Spring
  - Java
  - JSTL
  - JSP
  - JavaEE
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

### JSTL Functions

JSTL에는 많은 표준 함수가 포함되어 있으며 대부분이 일반적인 문자열 조작 함수입니다. 다음은 JSP에 JSTL 함수 라이브러리를 포함하는 구문입니다.

아래와 같이 사용할 수 있습니다.

```xml
Standard Syntax:
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

XML Syntax:
<anyxmlelement xmlns:fn="http://java.sun.com/jsp/jstl/functions" />
```

### boolean contains(String, String)

`fn:contains()` 함수는 입력 문자열에 지정된 하위 문자열이 포함되어 있는지 여부를 결정합니다.

> Example

```xml
<c:set var="theString" value="I am a test String"/>
<c:if test="${fn:contains(theString, 'test')}">
    <p>Found test string<p>
</c:if>

<c:if test="${fn:contains(theString, 'TEST')}">
    <p>Found TEST string<p>
</c:if>
```

### boolean containsIgnoreCase(String, String)

`fn:containsIgnoreCase()` 함수는 입력 문자열에 지정된 하위 문자열이 포함되어 있는지 여부를 결정합니다. 검색하는 동안 대소문자를 무시합니다.

> Example

```xml
<c:set var="theString" value="I am a test String"/>

<c:if test="${fn:containsIgnoreCase(theString, 'test')}">
    <p>Found test string<p>
</c:if>

<c:if test="${fn:containsIgnoreCase(theString, 'TEST')}">
    <p>Found TEST string<p>
</c:if>
```

### boolean endsWith(String, String)

`fn:endsWith()` 함수는 입력 문자열이 지정된 접미사로 끝나는지 여부를 결정합니다.

> Example

```xml
<c:set var="theString" value="I am a test String 123"/>

<c:if test="${fn:endsWith(theString, '123')}">
    <p>String ends with 123<p>
</c:if>

<c:if test="${fn:endsWith(theString, 'TEST')}">
    <p>String ends with TEST<p>
</c:if>
```

### String escapeXml(String)

`fn:escapeXml()` 함수는 XML 마크업으로 해석될 수 있는 문자를 이스케이프합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="This <abc>is second String.</abc>"/>

<p>With escapeXml() Function:</p>
<p>string (1) : ${fn:escapeXml(string1)}</p>
<p>string (2) : ${fn:escapeXml(string2)}</p>

<p>Without escapeXml() Function:</p>
<p>string (1) : ${string1}</p>
<p>string (2) : ${string2}</p>
```

### int indexOf(String, String)

`fn:indexOf()` 함수는 지정된 하위 문자열의 문자열 내에서 인덱스를 반환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="This <abc>is second String.</abc>"/>
<p>Index (1) : ${fn:indexOf(string1, "first")}</p>
<p>Index (2) : ${fn:indexOf(string2, "second")}</p>
```

### String join(String[], String)

`fn:join()` 함수는 배열의 모든 요소를 지정된 구분 기호가 있는 문자열로 연결합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:split(string1, ' ')}" />
<c:set var="string3" value="${fn:join(string2, '-')}" />
<p>Final String : ${string3}</p>
```

### int length(Object)

`fn:length()` 함수는 문자열 길이 또는 컬렉션의 항목 수를 반환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="This is second String." />
<p>Length of String (1) : ${fn:length(string1)}</p>
<p>Length of String (2) : ${fn:length(string2)}</p>
```

### String replace(String, String, String)

`fn:replace()` 함수는 문자열의 모든 항목을 다른 문자열로 바꿉니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:replace(string1, 'first', 'second')}" />
<p>Final String : ${string2}</p>
```

### String[] split(String, String)

`fn:split()` 함수는 구분 기호 문자열을 기반으로 문자열을 하위 문자열 배열로 분할합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:split(string1, ' ')}" />
<c:set var="string3" value="${fn:join(string2, '-')}" />

<p>String (3) : ${string3}</p>

<c:set var="string4" value="${fn:split(string3, '-')}" />
<c:set var="string5" value="${fn:join(string4, ' ')}" />

<p>String (5) : ${string5}</p>
```

### boolean startsWith(String, String)

`fn:startsWith()` 함수는 입력 문자열이 지정된 하위 문자열로 시작하는지 여부를 결정합니다.

> Example

```xml
<c:set var="string" value="Second: This is first String."/>
      
<c:if test="${fn:startsWith(string, 'First')}">
    <p>String starts with First</p>
</c:if>

<br />
<c:if test="${fn:startsWith(string, 'Second')}">
    <p>String starts with Second</p>
</c:if>
```

### String substring(String, int, int)

`fn:substring()` 함수는 시작 및 끝 인덱스로 지정된 문자열의 하위 집합을 반환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:substring(string1, 5, 15)}" />

<p>Final sub string : ${string2}</p>
```

### String substringAfter(String, String)

`fn:substringAfter()` 함수는 지정된 하위 문자열 뒤의 문자열 부분을 반환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:substringAfter(string1, 'is')}" />

<p>Final sub string : ${string2}</p>
```

### String substringBefore(String, String)

`fn:substringBefore()` 함수는 지정된 부분 문자열 앞의 문자열 부분을 반환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:substringBefore(string1, 'first')}" />
<p>Final sub string : ${string2}</p>
```

### String toLowerCase(String)

`fn:toLowerCase()` 함수는 문자열의 모든 문자를 소문자로 변환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:toLowerCase(string1)}" />

<p>Final string : ${string2}</p>
```

### String toUpperCase(String)

`fn:toUpperCase()` 함수는 문자열의 모든 문자를 대문자로 변환합니다.

> Example

```xml
<c:set var="string1" value="This is first String."/>
<c:set var="string2" value="${fn:toUpperCase(string1)}" />

<p>Final string : ${string2}</p>
```

### String trim(String)	

`fn:trim()` 함수는 문자열의 양쪽 끝에서 공백을 제거합니다.

> Example

```xml
<c:set var="string1" value="This is first String"/>
<p>String (1) Length : ${fn:length(string1)}</p>

<c:set var="string2" value="${fn:trim(string1)}" />
<p>String (2) Length : ${fn:length(string2)}</p>
<p>Final string : ${string2}</p>
```

> 참고자료

* [JavaServer Pages Standard Tag Library 1.1 Tag Reference](https://docs.oracle.com/javaee/5/jstl/1.1/docs/tlddocs/)
* [JSP - Standard Tag Library (JSTL) Tutorial](https://www.tutorialspoint.com/jsp/jsp_standard_tag_library.htm)