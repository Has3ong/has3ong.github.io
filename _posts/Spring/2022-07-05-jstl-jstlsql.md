---
title:  "JSTL 문법 톺아보기 -3- JSTL sql"
excerpt: "JSTL 문법 톺아보기 -3- JSTL sql"
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

### JSTL SQL Tags

JSTL SQL 태그 라이브러리는 Oracle, mySQL 또는 Microsoft SQL Server와 같은 관계형 데이터베이스(RDBMS)와 상호 작용하기 위한 태그를 제공합니다.

아래와 같이 추가하여 사용할 수 있습니다.

```xml
Standard Syntax:
<%@ taglib prefix="sql" uri="http://java.sun.com/jsp/jstl/sql" %>

XML Syntax:
<anyxmlelement xmlns:sql="http://java.sun.com/jsp/jstl/sql" />
```

아래는 공통적으로 사용할 테이블입니다.

```SQL
create table Employees (
  id int not null,
  age int not null,
  first varchar (255),
  last varchar (255)
);

create table Students (
  id int not null,
  first varchar (255),
  last varchar (255),
  dob date
);
```

### setDataSource

`<sql:setDataSource>` 태그는 데이터 소스 구성 변수를 설정하거나 다른 JSTL 데이터베이스 작업에 대한 입력으로 사용할 수 있는 범위 변수에 데이터 소스 정보를 저장합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the data source specified. Type can be String or DataSource.|
|scope|false|String|If var is specified, scope of the exported variable. Otherwise, scope of the data source configuration variable.|
|dataSource|false|String|Data source. If specified as a string, it can either be a relative path to a JNDI resource, or a JDBC parameters string as defined in Section 10.1.1.|
|driver|false|String|JDBC parameter: driver class name.|
|url|false|String|JDBC parameter: URL associated with the database.|
|user|false|String|JDBC parameter: database user on whose behalf the connection to the database is being made.|
|password|false|String|JDBC parameter: user password|

> Example

```xml
<sql:setDataSource var="snapshot" driver="com.mysql.jdbc.Driver"
  url="jdbc:mysql://localhost/TEST"
  user="user_id"  password="mypassword"/>
<sql:query dataSource="${snapshot}" sql="..." var="result" />
```

### query

`<sql:query>` 태그는 SQL `SELECT` 문을 실행하고 결과를 범위 변수에 저장합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|true|String|Name of the exported scoped variable for the query result. The type of the scoped variable is javax.servlet.jsp.jstl.sql. Result (see Chapter 16 "Java APIs").|
|scope|false|String|Scope of var.|
|sql|false|String|SQL query statement.|
|dataSource|false|String|Data source associated with the database to query. A String value represents a relative path to a JNDI resource or the parameters for the DriverManager class.|
|startRow|false|String|The returned Result object includes the rows starting at the specified index. The first row of the original query result set is at index 0. If not specified, rows are included starting from the first row at index 0.|
|maxRows|false|String|The maximum number of rows to be included in the query result. If not specified, or set to -1, no limit on the maximum number of rows is enforced.|

> Example

```xml
<sql:query dataSource="${snapshot}" var="result">
  SELECT * from Employees;
</sql:query>

<table border="1" width="100%">
  <tr>
    <th>Emp ID</th>
    <th>First Name</th>
    <th>Last Name</th>
    <th>Age</th>
  </tr>
  
  <c:forEach var="row" items="${result.rows}">
    <tr>
        <td> <c:out value="${row.id}"/></td>
        <td> <c:out value="${row.first}"/></td>
        <td> <c:out value="${row.last}"/></td>
        <td> <c:out value="${row.age}"/></td>
    </tr>
  </c:forEach>
</table>
```

### update

`<sql:update>` 태그는 데이터를 반환하지 않는 SQL 문을 실행합니다. 예를 들어, SQL `INSERT`, `UPDATE` 또는 `DELETE` 문.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|var|false|String|Name of the exported scoped variable for the result of the database update. The type of the scoped variable is java.lang.Integer.|
|scope|false|String|Scope of var.|
|sql|false|String|SQL update statement.|
|dataSource|false|String|Data source associated with the database to update. A String value represents a relative path to a JNDI resource or the parameters for the JDBC DriverManager class.|

> Example

```xml
<sql:update dataSource="${snapshot}" var="count">
  INSERT INTO Employees VALUES (104, 2, 'Nuha', 'Ali');
</sql:update>
```

```xml
<sql:update dataSource="${snapshot}" var="data">
  UPDATE Employees SET first=?, last=?, age=? where id=?
  <sql:param value="${param.id}" />
  <sql:param value="${param.first}" />
  <sql:param value="${param.last}" />
  <sql:param value="${param.ages}" />
</sql:update>
```

```xml
<sql:update dataSource="${dbSource}" var="dbResult">
  DELETE FROM Employees WHERE id=${param.id};
  <sql:param value="${param.id}" />
</sql:update>
```

### param

값 자리 표시자에 대한 값을 제공하기 위해 `<sql:query>` 태그 및 `<sql:update>` 태그에 대한 중첩 작업으로 사용되는 `<sql:param>` 태그입니다. `null` 값이 제공되면 값은 자리 표시자에 대해 SQL `NULL`로 설정됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|false|String|Parameter value.|

> Example

```xml
<c:set var="empId" value="103"/>

<sql:update dataSource="${snapshot}" var="count">
  DELETE FROM Employees WHERE Id=?
  <sql:param value="${empId}" />
</sql:update>
```

### dateParam

`<sql:dateParam>` 태그는 값 자리 표시자에 대한 날짜 및 시간 값을 제공하기 위해 `<sql:query>` 및 `<sql:update>` 태그에 대한 중첩 작업으로 사용됩니다. `null` 값이 제공되면 값은 자리 표시자에 대해 SQL `NULL`로 설정됩니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|value|true|String|Parameter value for DATE, TIME, or TIMESTAMP column in a database table.|
|type|false|String|One of "date", "time" or "timestamp".|

> Example

```xml
<%
  Date DoB=new Date("2001/12/16");
  int studentId=100;
%>

<sql:update dataSource="${snapshot}" var="count">
  UPDATE Students SET dob=? WHERE Id=?
  <sql:dateParam value="<%=DoB%>" type="DATE" />
  <sql:param value="<%=studentId%>" />
</sql:update>
```

### transaction

`<sql:transaction>` 태그는 `<sql:query>` 및 `<sql:update>` 태그를 트랜잭션으로 그룹화하는 데 사용됩니다. 단일 트랜잭션을 생성하기 위해 `<sql:transaction>` 태그 내부에 명령문만큼 많은 `<sql:query>` 및 `<sql:update>` 태그를 넣을 수 있습니다.

이는 중첩된 작업에 의해 예외가 `throw`되는 경우 중첩된 작업에 의해 수행된 데이터베이스 수정 사항이 커밋되거나 롤백되도록 합니다.

> Attributes

|Name|Required|Type|Description|
|:--|:--|:--|:--|
|dataSource|false|String|DataSource associated with the database to access. A String value represents a relative path to a JNDI resource or the parameters for the JDBC DriverManager facility.|
|isolation|false|String|Transaction isolation level. If not specified, it is the isolation level the DataSource has been configured with.|

> Example

```xml
<sql:transaction dataSource="${snapshot}">
  <sql:update var="count">
    UPDATE Students SET last='Ali' WHERE Id=102
  </sql:update>
  
  <sql:update var="count">
    UPDATE Students SET last='Shah' WHERE Id=103
  </sql:update>
  
  <sql:update var="count">
    INSERT INTO Students 
    VALUES (104,'Nuha', 'Ali', '2010/05/26');
  </sql:update>
</sql:transaction>
```

> 참고자료

* [JavaServer Pages Standard Tag Library 1.1 Tag Reference](https://docs.oracle.com/javaee/5/jstl/1.1/docs/tlddocs/)
* [JSP - Standard Tag Library (JSTL) Tutorial](https://www.tutorialspoint.com/jsp/jsp_standard_tag_library.htm)