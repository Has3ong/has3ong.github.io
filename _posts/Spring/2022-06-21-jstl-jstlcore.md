---
title:  "JSTL 문법 톺아보기 -1- JSTL core"
excerpt: "JSTL 문법 톺아보기 -1- JSTL core"
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

### JSTL Core Tags

태그의 핵심 그룹은 가장 일반적으로 사용되는 JSTL 태그입니다.

아래와 같이 추가하여 사용할 수 있습니다.

```xml
Standard Syntax:
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

XML Syntax:
<anyxmlelement xmlns:c="http://java.sun.com/jsp/jstl/core" />
```

출력 결과는 포스트에 담지 않았습니다. 참고해주시면 감사합니다.

### out

`<c:out>` 태그는 표현식의 결과를 출력합니다.`<%= %>`가 작동하는 방식과 거의 유사합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|Expression to be evaluated.|
|default|false|String|Default value if the resulting value is null.|
|escapeXml|false|String|Determines whether characters <,>,&,'," in the resulting string should be converted to their corresponding character entity codes. Default value is true.|

> Example

```xml
<c:out value="${jstl}"/>
```

### set

Spring Controller의 `Bean`, `Map` 등에서 받아온 값을 설정을 하거나, JSP 변수를 생성해서 값을 초기화 할 수 있습니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable to hold the value specified in the action. The type of the scoped variable is whatever type the value expression evaluates to.|
|value|false|String|Expression to be evaluated.|
|target|false|String|Target object whose property will be set. Must evaluate to a JavaBeans object with setter property property, or to a java.util.Map object.|
|property|false|String|Name of the property to be set in the target object.|
|scope|false|String|Scope for var.|

> Example 1

```java
model.addAttribute("program", "jstl");
```

```xml
<c:set var="program_var" scope="session" value="${program}"/>
<c:out value="${program_var}"/>
```

> Example 2

```java
model.addAttribute("map", new HashMap<String, String>());
```

```xml
<c:set target="${map}" property="program" value="jstl"/>
<c:out value="${map.program }"></c:out>
```

### remove

`<c:remove>` 태그는 지정된 `scope` 또는 변수가 발견된 첫 번째 `scope`(`scope가` 지정되지 않은 경우)에서 변수를 제거합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|true|String|Name of the scoped variable to be removed.|
|scope|false|String|Scope for var.|

> Example

```xml
<c:set var="program" scope="session" value="jstl"/>
<c:out value="${program}"/>
<c:remove var="program"/>
<c:out value="${program}"/>
```

### choose & when & otherwise

##### choose

`<when>` 및 `<otherwise>`로 표시되는 상호 배타적인 조건부 연산에 대한 컨텍스트를 설정하는 조건 태그입니다.

프로그래밍 언어로 비교하면 `if`, `else if`, `else` 와 유사하게 동작합니다.

##### when 

`<choose>` 에 하위 태그로 작동하며 `test` 조건이 참이면 동작합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|test|true|boolean|The test condition that determines whether or not the body content should be processed.|

##### otherwise

`<when>` 태그 다음에 오는 `<choose>` 의 하위 태그이며 `when`에서 정의된 모든 조건이 `false`일 경우에만 실행합니다.

> Example

```xml
<c:set var="program" value="jstl"/>
<c:choose>
  <c:when test="${program eq 'jstl'">
    Hello JSTL
  </c:when>
  <c:when test="${program eq 'java'">
    Hello Java!
  </c:when>
  <c:otherwise>
    Hello World!
  </c:otherwise>
</c:choose>
```

### if

`test` 조건이 `true`인 경우 동작합니다. `else` 구문은 없습니다. 

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|test|true|boolean|The test condition that determines whether or not the body content should be processed.|
|var|false|String|Name of the exported scoped variable for the resulting value of the test condition. The type of the scoped variable is Boolean.|
|scope|false|String|Scope for var.|

> Example

```xml
<c:set var="program" value="jstl"/>
<c:if test="${program eq 'jstl'}" var="program" scope="session">
  Hello JSTL
</c:if>
```

### catch

`<c:catch>` 태그는 본문에서 발생하는 모든 `throwable`을 포착하고 선택적으로 노출합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the exception thrown from a nested action. The type of the scoped variable is the type of the exception thrown.|

> Example

```xml
<c:catch var ="catchException">
  <% int x=5/0;%>
</c:catch>

<c:if test="${catchException != null}">
  <p>The exception is : ${catchException} <br />
</c:if>
```

### forEach

`<c:forEach>` 태그는 객체 컬렉션을 반복하기 때문에 일반적으로 사용되는 태그입니다. Java에서 사용하는 `for`, `while`, `do-while` 구문과 유사합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|items|false|String|Collection of items to iterate over.|
|begin|false|int|If items specified: Iteration begins at the item located at the specified index. First item of the collection has index 0. If items not specified: Iteration begins with index set at the value specified.|
|end|false|int|If items specified: Iteration ends at the item located at the specified index (inclusive). If items not specified: Iteration ends when index reaches the value specified.|
|step|false|int|Iteration will only process every step items of the collection, starting with the first one.|
|var|false|String|Name of the exported scoped variable for the current item of the iteration. This scoped variable has nested visibility. Its type depends on the object of the underlying collection.|
|varStatus|false|String|Name of the exported scoped variable for the status of the iteration. Object exported is of type javax.servlet.jsp.jstl.core.LoopTagStatus. This scoped variable has nested visibility.|

> Example 1

```xml
<c:forEach var="index" begin="1" end="5" step="2" varStatus="status" >
	<c:out value="${index}"/><p>
</c:forEach>
```

> Example 2

```java
model.addAttribute("items", new ArrayList<>(Arrays.asList("Black", "White", "Green", "Red"))
```

```xml
<c:forEach var="index" items="${items}" >
	<c:out value="${index}"/><p>
</c:forEach>
```

> varStatus 값

```xml
${status.current}   <!– 현재 값 –>
${status.index}     <!– 0부터의 순서 –>
${status.count}     <!– 1부터의 순서 –>
${status.first}     <!– 첫 번째인지 여부 –>
${status.last}      <!– 마지막인지 여부 –> 
${status.begin}     <!– 시작값 –>
${status.end}       <!– 마지막 값 –>
${status.step}      <!– 증가값 –>
```

### forTokens

`<c:forEach>` 와 유사하며 `<c:forTokens>` 태그는 문자열을 토큰으로 나누고 각 토큰을 반복하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|items|true|String|String of tokens to iterate over.|
|delims|true|String|The set of delimiters (the characters that separate the tokens in the string).|
|begin|false|int|Iteration begins at the token located at the specified index. First token has index 0.|
|end|false|int|Iteration ends at the token located at the specified index (inclusive).|
|step|false|int|Iteration will only process every step tokens of the string, starting with the first one.|
|var|false|String|Name of the exported scoped variable for the current item of the iteration. This scoped variable has nested visibility.|
|varStatus|false|String|Name of the exported scoped variable for the status of the iteration. Object exported is of type javax.servlet.jsp.jstl.core.LoopTag Status. This scoped variable has nested visibility.|

> Example

```xml
<c:forTokens items="Black,White,Green,Red" delims="," var ="color">
  <c:out value="${color}"/><p>
</c:forTokens>
```

### import

`<c:import>` 태그는 `<include>` 작업의 모든 기능을 제공하며, 절대경로 URL도 포함할 수 있습니다. 예를 들어 `import` 태그를 사용하면 다른 웹사이트나 FTP 서버의 콘텐츠를 포함할 수 있습니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|url|true|String|The URL of the resource to import.|
|var|false|String|Name of the exported scoped variable for the resource's content. The type of the scoped variable is String.|
|scope|false|String|Scope for var.|
|varReader|false|String|Name of the exported scoped variable for the resource's content. The type of the scoped variable is Reader.|
|context|false|String|Name of the context when accessing a relative URL resource that belongs to a foreign context.|
|charEncoding|false|String|Character encoding of the content at the input resource.|

> Example 1

```xml
<c:import url="/index.jsp" charEncoding="ISO-8859-1" var="data" scope="page">
  <c:param name="program" value="jstl"></c:param>
</c:import>
<c:out value="${data}" escapeXml="false"></c:out>
```

`index.jsp` 파일에서 아래와 같이 `<c:param>` 값을 받아올 수 있다.

```xml
<a href="${param.program}">jstl</a>
```

Controller 에서도 동일하게 값을 받아올 수 있다.

```java
@RequestMapping("/index") 
public String test(@RequestParam String program, Model model) throws Exception { 
}
```

### param

`<c:param>` 태그를 사용하면 적절한 URL 요청 매개변수를 URL로 지정할 수 있으며 필요한 URL 인코딩도 수행합니다.

`<c:param>` 태그 내에서 `name` 속성은 매개변수 이름을 나타내고, `value` 속성은 매개변수 값을 나타냅니다..

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|name|true|String|Name of the query string parameter.|
|value|false|String|Value of the parameter.|

> Example

```xml
<c:url value="/index.jsp" var="data">
   <c:param name="program" value="jstl"/>
   <c:param name="action" value="post"/>
</c:url>
<c:import url="${data}"/>

"/index.jsp?program=jstl;action=post;"
```

### redirect

`<c:redirect>` 태그는 `response.sendRedirect()`와 같이 `url` 지정해 특정 페이지로 리다이렉트 시켜줍니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|url|false|String|The URL of the resource to redirect to.|
|context|false|String|Name of the context when redirecting to a relative URL resource that belongs to a foreign context.|

> Example

```xml
<c:redirect url="/index.jsp" context="/example">
        <c:param name="program" value="jstl"/>
</c:redirect>
```

### url

`<c:url>` 태그는 URL을 문자열로 형식화하고 변수에 저장합니다. 이 태그는 필요할 때 자동으로 URL 재작성을 수행합니다. `var` 속성은 형식이 지정된 URL을 포함할 변수를 지정합니다. JSTL `url` 태그는 `response.encodeURL()` 메서드에 대한 호출을 작성하는 대체 메서드일 뿐입니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the processed url. The type of the scoped variable is String.|
|scope|false|String|Scope for var.|
|value|true|String|URL to be processed.|
|context|true|String|Name of the context when specifying a relative URL resource that belongs to a foreign context.|

> Example

```xml
<a href="<c:url value="/index.jsp"/>">TEST</a>
```

> 참고자료

* [JavaServer Pages Standard Tag Library 1.1 Tag Reference](https://docs.oracle.com/javaee/5/jstl/1.1/docs/tlddocs/)
* [JSP - Standard Tag Library (JSTL) Tutorial](https://www.tutorialspoint.com/jsp/jsp_standard_tag_library.htm)