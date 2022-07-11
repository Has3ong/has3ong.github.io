---
title:  "JSTL 문법 톺아보기 -4- JSTL XML"
excerpt: "JSTL 문법 톺아보기 -4- JSTL XML"
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

### JSTL XML Tags

JSTL XML 태그는 XML 문서를 만들고 조작하는 JSP 중심 방식을 제공합니다. 다음은 JSP에 JSTL XML 라이브러리를 포함하는 구문입니다.

JSTL XML 태그 라이브러리에는 XML 데이터와 상호 작용하기 위한 사용자 정의 태그가 있습니다. 여기에는 XML 구문 분석, XML 데이터 변환 및 XPath 식을 기반으로 하는 흐름 제어가 포함됩니다.

아래와 같이 사용할 수 있습니다.

```xml
Standard Syntax:
<%@ taglib prefix="x" uri="http://java.sun.com/jsp/jstl/xml" %>

XML Syntax:
<anyxmlelement xmlns:x="http://java.sun.com/jsp/jstl/xml" />
```

### out

`<x:out>` 태그는 XPath 표현식의 결과를 표시합니다. `<%= %>` JSP 구문과 동일하게 작동합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|select|true|String|XPath expression to be evaluated.|
|escapeXml|false|String|Determines whether characters <,>,&,'," in the resulting string should be converted to their corresponding character entity codes. Default value is true.|

> Example

```xml
<c:set var="xmltext">
    <books>
      <book>
          <name>Padam History</name>
          <author>ZARA</author>
          <price>100</price>
      </book>
      
      <book>
          <name>Great Mistry</name>
          <author>NUHA</author>
          <price>2000</price>
      </book>
    </books>
</c:set>

<x:parse xml="${xmltext}" var="output"/>
<b>The title of the first book is</b>: 
<x:out select="$output/books/book[1]/name" />
<br>

<b>The price of the second book</b>: 
<x:out select="$output/books/book[2]/price" />
```

### parse

`<x:parse>` 태그는 속성을 통해 또는 태그 본문에 지정된 XML 데이터를 구문 분석하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the parsed XML document. The type of the scoped variable is implementation dependent.|
|varDom|false|String|Name of the exported scoped variable for the parsed XML document. The type of the scoped variable is org.w3c.dom.Document.|
|scope|false|String|Scope for var.|
|scopeDom|false|String|Scope for varDom.|
|xml|false|String|Deprecated. Use attribute 'doc' instead.|
|doc|false|String|Source XML document to be parsed.|
|systemId|false|String|The system identifier (URI) for parsing the XML document.|
|filter|false|String|Filter to be applied to the source document.|

> Example

```xml
<!-- books.xml -->
<books>
   <book>
      <name>Padam History</name>
      <author>ZARA</author>
      <price>100</price>
   </book>
   
   <book>
      <name>Great Mistry</name>
      <author>NUHA</author>
      <price>2000</price>
   </book>
</books>
```

```xml
<h3>Books Info:</h3>
<c:import var="bookInfo" url="http://localhost:8080/books.xml"/>

<x:parse xml="${bookInfo}" var="output"/>
<b>The title of the first book is</b>: 
<x:out select="$output/books/book[1]/name" />
<br>

<b>The price of the second book</b>: 
<x:out select="$output/books/book[2]/price" />
```

### set

`<x:set>` 태그는 변수를 XPath 표현식의 값으로 설정합니다. XPath 표현식의 결과가 부울이면 `<x:set>` 태그는 `java.lang.Boolean` 객체를 설정합니다. 문자열의 경우 `java.lang.String`이며, 숫자의 경우 `java.lang.Number`로 설정합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable to hold the value specified in the action. The type of the scoped variable is whatever type the select expression evaluates to.|
|select|false|String|XPath expression to be evaluated.|
|scope|false|String|Scope for var.|

> Example

```xml
<c:set var="xmltext">
  <books>
    <book>
        <name>Padam History</name>
        <author>ZARA</author>
        <price>100</price>
    </book>
    
    <book>
        <name>Great Mistry</name>
        <author>NUHA</author>
        <price>2000</price>
    </book>
  </books>
</c:set>

<x:parse xml="${xmltext}" var="output"/>
<x:set var="fragment" select="$output//book"/>
  <b>The price of the second book</b>: 
<c:out value="${fragment}" />
```

### if

`<x:if>` 태그는 테스트 XPath 표현식을 평가하고 `true`이면 본문을 처리합니다. 테스트 조건이 거짓이면 본문은 무시됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|select|true|String|The test condition that tells whether or not the body content should be processed.|
|var|false|String|Name of the exported scoped variable for the resulting value of the test condition. The type of the scoped variable is Boolean.|
|scope|false|String|Scope for var.|

> Example

```xml
<c:set var="xmltext">
  <books>
    <book>
        <name>Padam History</name>
        <author>ZARA</author>
        <price>100</price>
    </book>
        
    <book>
        <name>Great Mistry</name>
        <author>NUHA</author>
        <price>2000</price>
    </book>
  </books>
</c:set>

<x:parse xml="${xmltext}" var="output"/>
  <x:if select="$output//book">
    Document has at least one <book> element.
  </x:if>
<br />

<x:if select="$output/books[1]/book/price > 100">
  Book prices are very high
</x:if>
```

### forEach

`<x:forEach>` 태그는 XML 문서의 노드를 반복하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the current item of the iteration. This scoped variable has nested visibility. Its type depends on the result of the XPath expression in the select attribute.|
|select|true|String|XPath expression to be evaluated.|
|begin|false|int|Iteration begins at the item located at the specified index. First item of the collection has index 0.|
|end|false|int|Iteration ends at the item located at the specified index (inclusive).|
|step|false|int|Iteration will only process every step items of the collection, starting with the first one.|
|varStatus|false|String|Name of the exported scoped variable for the status of the iteration. Object exported is of type javax.servlet.jsp.jstl.core.LoopTagStatus. This scoped variable has nested visibility.|

> Example

```xml
<c:set var="xmltext">
  <books>
    <book>
        <name>Padam History</name>
        <author>ZARA</author>
        <price>100</price>
    </book>
    
    <book>
        <name>Great Mistry</name>
        <author>NUHA</author>
        <price>2000</price>
    </book>
  </books>
</c:set>

<x:parse xml="${xmltext}" var="output"/>

<ul class="list">
  <x:forEach select="$output/books/book/name" var="item">
    <li>Book Name: <x:out select="$item" /></li>
  </x:forEach>
</ul>
```

### choose

`<x:choose>` 태그는 Java 스위치 문처럼 작동합니다. 이를 통해 여러 대안 중에서 선택할 수 있습니다. switch 문에 case 문이 있는 경우 `<x:choose>` 태그에는 `<x:when>` 태그가 있습니다. 비슷한 방식으로 switch 문에는 기본 동작을 지정하는 기본 절이 있고 `<x:choose>` 태그에는 `<x:otherwise>` 태그가 기본 절로 있습니다.

> `<x:when>` Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|select|true|String|The test condition that tells whether or not the body content should be processed|

> Example

```xml
<c:set var="xmltext">
  <books>
    <book>
        <name>Padam History</name>
        <author>ZARA</author>
        <price>100</price>
    </book>
    
    <book>
        <name>Great Mistry</name>
        <author>NUHA</author>
        <price>2000</price>
    </book>
  </books>
</c:set>

<x:parse xml="${xmltext}" var="output"/>
<x:choose>
  <x:when select="$output//book/author='ZARA'">
    Book is written by ZARA
  </x:when>
  
  <x:when select="$output//book/author='NUHA'">
    Book is written by NUHA
  </x:when>
  
  <x:otherwise>
    Unknown author.
  </x:otherwise>
</x:choose>
```

### transform

`<x:transform>` 태그는 XML 문서에 XSL 변환을 적용합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the transformed XML document. The type of the scoped variable is org.w3c.dom.Document.|
|scope|false|String|Scope for var.|
|result|false|String|Result Object that captures or processes the transformation result.|
|xml|false|String|Deprecated. Use attribute 'doc' instead.|
|doc|false|String|Source XML document to be transformed. (If exported by <x:set>, it must correspond to a well-formed XML document, not a partial document.)|
|xmlSystemId|false|String|Deprecated. Use attribute 'docSystemId' instead.|
|docSystemId|false|String|The system identifier (URI) for parsing the XML document.|
|xslt|false|String|javax.xml.transform.Source Transformation stylesheet as a String, Reader, or Source object.|
|xsltSystemId|false|String|The system identifier (URI) for parsing the XSLT stylesheet.|

> Example

```xml
<!-- style.xsl -->
<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
   version="1.0">

<xsl:output method="html" indent="yes"/>
   <xsl:template match="/">
      <html>
         <body>
            <xsl:apply-templates/>
         </body>
      </html>
   </xsl:template>

   <xsl:template match="books">
      <table border="1" width="100%">
         <xsl:for-each select="book">
            <tr>
               <td>
                  <i><xsl:value-of select="name"/></i>
               </td>
               
               <td>
                  <xsl:value-of select="author"/>
               </td>
               
               <td>
                  <xsl:value-of select="price"/>
               </td>
            </tr>
         </xsl:for-each>
      </table>
   </xsl:template>

</xsl:stylesheet>
```

```xml
<c:set var="xmltext">
  <books>
    <book>
      <name>Padam History</name>
      <author>ZARA</author>
      <price>100</price>
    </book>
  
    <book>
      <name>Great Mistry</name>
      <author>NUHA</author>
      <price>2000</price>
    </book>
  </books>
</c:set>

<c:import url="http://localhost:8080/style.xsl" var="xslt"/>
<x:transform xml="${xmltext}" xslt="${xslt}"/>
```

### param

`<x:param>` 태그는 XSLT 스타일시트에서 매개변수를 설정하기 위해 transform 태그와 함께 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|name|true|String|Name of the transformation parameter.|
|value|false|String|Value of the parameter.|

> Example

```xml
<!-- style.xsl -->
<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="html" indent="yes"/>
<xsl:param name="bgColor"/>

   <xsl:template match="/">
      <html>
         <body>
            <xsl:apply-templates/>
         </body>
      </html>
   </xsl:template>

   <xsl:template match="books">
      <table border="1" width="50%" bgColor="{$bgColor}">
         <xsl:for-each select="book">
            <tr>
               <td><i><xsl:value-of select="name"/></i></td>
               <td><xsl:value-of select="author"/></td>
               <td><xsl:value-of select="price"/></td>
            </tr>
         </xsl:for-each>
      </table>
   </xsl:template>
   
</xsl:stylesheet>
```

```xml
<c:set var="xmltext">
  <books>
    <book>
        <name>Padam History</name>
        <author>ZARA</author>
        <price>100</price>
    </book>
    
    <book>
        <name>Great Mistry</name>
        <author>NUHA</author>
        <price>2000</price>
    </book>
  </books>
</c:set>

<c:import url="http://localhost:8080/style.xsl" var="xslt"/>
<x:transform xml="${xmltext}" xslt="${xslt}">
  <x:param name="bgColor" value="grey"/>
</x:transform>
```

> 참고자료

* [JavaServer Pages Standard Tag Library 1.1 Tag Reference](https://docs.oracle.com/javaee/5/jstl/1.1/docs/tlddocs/)
* [JSP - Standard Tag Library (JSTL) Tutorial](https://www.tutorialspoint.com/jsp/jsp_standard_tag_library.htm)