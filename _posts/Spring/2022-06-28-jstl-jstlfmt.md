---
title:  "JSTL 문법 톺아보기 -2- JSTL fmt"
excerpt: "JSTL 문법 톺아보기 -2- JSTL fmt"
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

### JSTL Formatting Tags

JSTL Formatting Tags는 국제화된 웹 사이트의 텍스트, 날짜, 시간 및 숫자 형식을 지정하고 표시하는 데 사용됩니다. 

아래와 같이 추가하여 사용할 수 있습니다.

```xml
Standard Syntax:
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

XML Syntax:
<anyxmlelement xmlns:fmt="http://java.sun.com/jsp/jstl/fmt" />
```

출력 결과는 포스트에 담지 않았습니다. 참고해주시면 감사합니다.

### requestEncoding

`<fmt:requestEncoding>` 태그는 웹 애플리케이션에 데이터를 출력할 때 사용하는 인코딩 유형을 지정하는 데 사용합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|Name of character encoding to be applied when decoding request parameters.|

> Example

```xml
<fmt:requestEncoding value="UTF-8" />
```

### setLocale

`<fmt:setLocale>` 태그는 주어진 로케일을 변수에 저장하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|A String value is interpreted as the printable representation of a locale, which must contain a two-letter (lower-case) language code (as defined by ISO-639), and may contain a two-letter (upper-case) country code (as defined by ISO-3166). Language and country codes must be separated by hyphen (-) or underscore (_).|
|variant|false|String|Vendor- or browser-specific variant. See the java.util.Locale javadocs for more information on variants.|
|scope|false|String|Scope of the locale configuration variable.|

> Example

```xml
<fmt:setLocale value="ko_kr"/>
<fmt:formatNumber value="10000" type="currency"/>

<fmt:setLocale value="ja_jp"/>
<fmt:formatNumber value="10000" type="currency"/>

<fmt:setLocale value="en_us"/>
<fmt:formatNumber value="10000" type="currency"/>
```

### timeZone

`<fmt:timeZone>` 태그는 본문 내의 모든 태그가 사용할 시간대를 지정하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|The time zone. A String value is interpreted as a time zone ID. This may be one of the time zone IDs supported by the Java platform (such as "America/Los_Angeles") or a custom time zone ID (such as "GMT-8"). See java.util.TimeZone for more information on supported time zone formats.|

> Example

```xml
<c:set var="now" value="<%=new java.util.Date()%>"></c:set>
<fmt:formatDate value="${now}" type="both" />
<fmt:timeZone value="GMT">
	<c:set var="now" value="<%=new java.util.Date()%>"></c:set>
	<fmt:formatDate value="${now}" type="both" />
</fmt:timeZone>
```

### setTimeZone

`<fmt:setTimeZone>` 태그는 시간대 객체를 지정된 범위 변수에 복사하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|The time zone. A String value is interpreted as a time zone ID. This may be one of the time zone IDs supported by the Java platform (such as "America/Los_Angeles") or a custom time zone ID (such as "GMT-8"). See java.util.TimeZone for more information on supported time zone formats.|
|var|false|String|Name of the exported scoped variable which stores the time zone of type java.util.TimeZone.|
|scope|false|String|Scope of var or the time zone configuration variable.|

> Example

```xml
<c:set var="now" value="<%=new java.util.Date()%>" />
<fmt:formatDate value="${now}" type="both" timeStyle="long" dateStyle="long" />
      
<fmt:setTimeZone value="GMT-8" />
<fmt:formatDate value="${now}" type="both" timeStyle="long" dateStyle="long" />
```

### bundle

`<fmt:bundle>` 태그는 `<fmt:bundle>` 과 `</fmt:bundle>` 태그 사이에 모든 `<fmt:message>` 태그에서 지정된 번들을 사용할 수 있도록 합니다. 이렇게 하면 각 `<fmt:message>` 태그에 대한 리소스 번들을 지정할 필요가 없습니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|basename|true|String|Resource bundle base name. This is the bundle's fully-qualified resource name, which has the same form as a fully-qualified class name, that is, it uses "." as the package component separator and does not have any file type (such as ".class" or ".properties") suffix.|
|prefix|false|String|Prefix to be prepended to the value of the message key of any nested <fmt:message> action.|

> Example

```java
public class Example_En extends ListResourceBundle {
  static final Object[][] contents={
    {"count.one", "One"},
    {"count.two", "Two"},
    {"count.three", "Three"},
  };
}
```

```xml
<fmt:bundle basename="com.tutorialspoint.Example" prefix="count.">
  <fmt:message key="one"/><br/>
  <fmt:message key="two"/><br/>
  <fmt:message key="three"/><br/>
</fmt:bundle>
```

### setBundle

`<fmt:setBundle>` 태그는 리소스 번들을 로드하고 범위 변수 또는 번들 구성 변수에 저장하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|basename|true|String|Resource bundle base name. This is the bundle's fully-qualified resource name, which has the same form as a fully-qualified class name, that is, it uses "." as the package component separator and does not have any file type (such as ".class" or ".properties") suffix.|
|var|false|String|Name of the exported scoped variable which stores the i18n localization context of type javax.servlet.jsp.jstl.fmt.LocalizationC ontext.|
|scope|false|String|Scope of var or the localization context configuration variable.|

> Example

```java
public class Example_En extends ListResourceBundle {
  static final Object[][] contents={
    {"count.one", "One"},
    {"count.two", "Two"},
    {"count.three", "Three"},
  };
}
```

```xml
<fmt:setBundle basename="com.tutorialspoint.Example" var="lang"/>
  <fmt:message key="count.one" bundle="${lang}"/><br/>
  <fmt:message key="count.two" bundle="${lang}"/><br/>
  <fmt:message key="count.three" bundle="${lang}"/><br/>
</fmt:setBundle>
```

### message

`<fmt:message>` 태그는 키를 메시지에 매핑하고 매개변수 교체를 수행합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|key|false|String|Message key to be looked up.|
|bundle|false|String|Localization context in whose resource bundle the message key is looked up.|
|var|false|String|Name of the exported scoped variable which stores the localized message.|
|scope|false|String|Scope of var.|

> Example

```java
public class Example_En extends ListResourceBundle {
  static final Object[][] contents={
    {"count.one", "One"},
    {"count.two", "Two"},
    {"count.three", "Three"},
  };
}
```

```xml
<fmt:setBundle basename="com.tutorialspoint.Example" var="lang"/>

<fmt:message key="count.one" bundle="${lang}"/><br/>
<fmt:message key="count.two" bundle="${lang}"/><br/>
<fmt:message key="count.three" bundle="${lang}"/><br/>
```

### param

`<fmt:param>` 작업은 매개변수화된 메시지에 대한 매개변수 값을 제공하기 위해 `<fmt:message>` 가 중첩된 작업으로 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|Argument used for parametric replacement.|

> Example

```xml
<fmt:message key="result">
  <fmt:param value="${result.total}" />
  <fmt:param value="${result.percentage}" />
</fmt:message>
```

### formatNumber

`<fmt:formatNumber>` 태그는 숫자, 백분율 및 통화의 형식을 지정하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|Numeric value to be formatted.|
|type|false|String|Specifies whether the value is to be formatted as number, currency, or percentage.|
|pattern|false|String|Custom formatting pattern.|
|currencyCode|false|String|ISO 4217 currency code. Applied only when formatting currencies (i.e. if type is equal to "currency"); ignored otherwise.|
|currencySymbol|false|String|Currency symbol. Applied only when formatting currencies (i.e. if type is equal to "currency"); ignored otherwise.|
|groupingUsed|false|String|Specifies whether the formatted output will contain any grouping separators.|
|maxIntegerDigits|false|String|Maximum number of digits in the integer portion of the formatted output.|
|minIntegerDigits|false|String|Minimum number of digits in the integer portion of the formatted output.|
|maxFractionDigits|false|String|Maximum number of digits in the fractional portion of the formatted output.|
|minFractionDigits|false|String|Minimum number of digits in the fractional portion of the formatted output.|
|var|false|String|Name of the exported scoped variable which stores the formatted result as a String.|
|scope|false|String|Scope of var.|

> Symbol & Description

|S.No.|Symbol & Description|
|:--|:--|
|1|<strong>0</strong><br>Represents a digit.|
|2|<strong>E</strong><br>Represents in exponential form.|
|3|<strong>E</strong><br>Represents a digit; displays 0 as absent.|
|4|<strong>.</strong><br>Serves as a placeholder for a decimal separator.|
|5|<strong>,</strong><br>Serves as a placeholder for a grouping separator.|
|6|<strong>;</strong><br>Separates formats.|
|7|<strong>-</strong><br>Used as the default negative prefix.|
|8|<strong>%</strong><br>Multiplies by 100 and displays as a percentage.|
|9|<strong>?</strong><br>Multiplies by 1000 and displays as per mille.|
|10|<strong>¤</strong><br>Represents the currency sign; replaced by actional currency symbol.|
|11|<strong>X</strong><br>Indicates that any other characters can be used in the prefix or suffix.
|12|<strong>'</strong><br>Used to quote special characters in a prefix or suffix.|

> Example

```xml
<c:set var="var" value="123456.7890" />

<fmt:formatNumber value="${var}" type="currency"/><br/> <!-- ￦123,457 -->
<fmt:formatNumber type="number" maxIntegerDigits="2" value="${var}" /><br/> <!-- 56.789 -->
<fmt:formatNumber type="number" maxFractionDigits="3" value="${var}" /><br/> <!-- 123,456.789 -->
<fmt:formatNumber type="number" groupingUsed="false" value="${var}" /><br/> <!-- 123456.789 -->
<fmt:formatNumber type="percent" maxIntegerDigits="3" value="${var}" /><br/> <!-- 679% -->
<fmt:formatNumber type="percent" minFractionDigits="10" value="${var}" /><br/> <!-- 12,345,678.9000000000% -->
<fmt:formatNumber type="percent" maxIntegerDigits="3" value="${var}" /><br/> <!-- 679% -->
<fmt:formatNumber type="number" pattern="###.###E0" value="${var}" /><br/> <!-- 123.457E3 -->
<fmt:formatNumber type="currency" value="${var}" /><br/> <!-- ￦123,457 -->
<fmt:formatNumber type="currency" value="${var}" currencySymbol="USD"/><br/> <!-- USD123,457 -->
```

### parseNumber

`<fmt:parseNumber>` 태그는 숫자, 백분율 및 통화를 구문 분석하는 데 사용됩니다. `<fmt:formatNumber>` 과 유사하므로 예제는 간단하게 작성했습니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|String to be parsed.|
|type|false|String|Specifies whether the string in the value attribute should be parsed as a number, currency, or percentage.|
|pattern|false|String|Custom formatting pattern that determines how the string in the value attribute is to be parsed.|
|parseLocale|false|String|Locale whose default formatting pattern (for numbers, currencies, or percentages, respectively) is to be used during the parse operation, or to which the pattern specified via the pattern attribute (if present) is applied.|
|integerOnly|false|String|Specifies whether just the integer portion of the given value should be parsed.|
|var|false|String|Name of the exported scoped variable which stores the parsed result (of type java.lang.Number).|
|scope|false|String|Scope of var.|

> Example

```xml
<c:set var="var" value="12345.6789" />
<fmt:parseNumber var="i" type="number" pattern="###.###" value="${var}" /><br/>
<c:out value="${i}" />
<fmt:parseNumber var="i" integerOnly="true" type="number" value="${var}" /><br/>
<c:out value="${i}" />
```

### formatDate

`<fmt:formatDate>` 태그는 다양한 방식으로 날짜 형식을 지정하는 데 사용됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|Date and/or time to be formatted.|
|type|false|String|Specifies whether the time, the date, or both the time and date components of the given date are to be formatted.|
|dateStyle|false|String|Predefined formatting style for dates. Follows the semantics defined in class java.text.DateFormat. Applied only when formatting a date or both a date and time (i.e. if type is missing or is equal to "date" or "both"); ignored otherwise.|
|timeStyle|false|String|Predefined formatting style for times. Follows the semantics defined in class java.text.DateFormat. Applied only when formatting a time or both a date and time (i.e. if type is equal to "time" or "both"); ignored otherwise.|
|pattern|false|String|Custom formatting style for dates and times.|
|timeZone|false|String|Time zone in which to represent the formatted time.|
|var|false|String|Name of the exported scoped variable which stores the formatted result as a String.|
|scope|false|String|Scope of var.|

> The pattern attribute is used to specify even more precise handling of the date −

|Code|Purpose|Sample|
|:--:|:--|:--:|
|G|The era designator|AD|
|y|The year|2002|
|M|The month|April & 04|
|d|The day of the month|20|
|h|The hour(12-hour time)|12|
|H|The hour(24-hour time)|0|
|m|The minute|45|
|s|The second|52|
|S|The millisecond|970|
|E|The day of the week|Tuesday|
|D|The day of the year|180|
|F|The day of the week in the month|2 (2nd Wed in month)|
|w|The week in the year|27|
|W|The week in the month|2|
|a|The a.m./p.m. indicator|PM|
|k|The hour(12-hour time)|24|
|K|The hour(24-hour time)|0|
|z|The time zone|Central Standard Time|
|'||The escape for text|
|''||The single quote|

> Example

```xml
<c:set var="now" value="<%= new java.util.Date()%>" />
<fmt:formatDate type="time" value="${now}" /><br/> <!-- 오후 2:09:00 -->
<fmt:formatDate type="date" value="${now}" /><br/> <!-- 2022. 6. 23 -->
<fmt:formatDate type="both" value="${now}" /><br/> <!-- 2022. 6. 23 오후 2:09:00 -->
<fmt:formatDate type="both" dateStyle="short" timeStyle="short" value="${now}" /><br/> <!-- 22. 6. 23 오후 2:09 -->
<fmt:formatDate type="both" dateStyle="medium" timeStyle="medium" value="${now}" /><br/> <!-- 2022. 6. 23 오후 2:09:00 -->
<fmt:formatDate type="both" dateStyle="long" timeStyle="long" value="${now}" /><br/> <!-- 2022년 6월 23일 (목) 오후 2시 09분 00초 -->
<fmt:formatDate pattern="yyyy-MM-dd" value="${now}" /><br/> <!-- 2022-06-23 -->
```

### parseDate

`<fmt:parseDate>` 태그는 날짜를 구문 분석하는 데 사용됩니다. `<fmt:formatDate>` 과 유사하므로 예제는 간단하게 작성했습니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|Date string to be parsed.|
|type|false|String|Specifies whether the date string in the value attribute is supposed to contain a time, a date, or both.|
|dateStyle|false|String|Predefined formatting style for days which determines how the date component of the date string is to be parsed. Applied only when formatting a date or both a date and time (i.e. if type is missing or is equal to "date" or "both"); ignored otherwise.|
|timeStyle|false|String|Predefined formatting styles for times which determines how the time component in the date string is to be parsed. Applied only when formatting a time or both a date and time (i.e. if type is equal to "time" or "both"); ignored otherwise.|
|pattern|false|String|Custom formatting pattern which determines how the date string is to be parsed.|
|timeZone|false|String|Time zone in which to interpret any time information in the date string.|
|parseLocale|false|String|Locale whose predefined formatting styles for dates and times are to be used during the parse operation, or to which the pattern specified via the pattern attribute (if present) is applied.|
|var|false|String|Name of the exported scoped variable in which the parsing result (of type java.util.Date) is stored.|
|scope|false|String|Scope of var.|

> Example

```xml
<c:set var="now" value="20-10-2010" />
<fmt:parseDate value="${now}" var="parsedEmpDate" pattern="dd-MM-yyyy" />
<c:out value="${parsedEmpDate}" />
```

> 참고자료

* [JavaServer Pages Standard Tag Library 1.1 Tag Reference](https://docs.oracle.com/javaee/5/jstl/1.1/docs/tlddocs/)
* [JSP - Standard Tag Library (JSTL) Tutorial](https://www.tutorialspoint.com/jsp/jsp_standard_tag_library.htm)