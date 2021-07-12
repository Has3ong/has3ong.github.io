---
title:  "Spring Boot Tiles 설정하기"
excerpt: "Spring Boot Tiles 설정하기"
categories:
  - Spring
tags:
  - Spring
  - Spring Boot
  - Tiles
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## Tiles 란

Tiles 는 뷰 패턴을 구현한 것이다. Tiles 는 자신만의 사용자가 만든 패턴을 웹 하면을 구성하기 쉽게해주는 프레임워크입니다. 

Tiles 에는 `Template`, `Attribute`, `Definition` 이라는 개념 가지고 있습니다.

### Template

tiles 에서 Template 이란 하나의 페이지 레이아웃입니다. 예를 들어 전통적인 페이지 구조는 아래와 같습니다.

![image](https://user-images.githubusercontent.com/80693904/123540537-7989fb80-d77a-11eb-8fd8-dbb413d0b91d.png)

위 구조를 JSP 페이지로 표현하면 아래와 같이 표현할 수 있습니다.

```jsp
<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>
<table>
  <tr>
    <td colspan="2">
      <tiles:insertAttribute name="header" />
    </td>
  </tr>
  <tr>
    <td>
      <tiles:insertAttribute name="menu" />
    </td>
    <td>
      <tiles:insertAttribute name="body" />
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <tiles:insertAttribute name="footer" />
    </td>
  </tr>
</table>
```

### Attribute

Attribute 는 Template 의 빈 공간을 채우기 위해 사용하는 정보이며 총 3가지 타입이 있습니다.

* **string** : 페이지로 표시되는 문자열.
* **template** : Template 안의 표시되는 템플릿(레이아웃)
* **definition** : Attribute 의 파일들이 실제 내용으로 채워진 페이지

### Definition

Definition 은 사용자에게 제공되는 페이지며, Template 과 Attribute 를 연결할 수 있습니다.

예를 들어 위에서 알아본 클래식 레이아웃 구조를 만든다면 아래와 같이 작성할 수 있습니다.

```xml
<definition name="myapp.homepage" template="/layouts/classic.jsp">
  <put-attribute name="header" value="/tiles/banner.jsp" />
  <put-attribute name="menu" value="/tiles/common_menu.jsp" />
  <put-attribute name="body" value="/tiles/home_body.jsp" />
  <put-attribute name="footer" value="/tiles/credits.jsp" />
</definition>
```

## Spring Boot 설정하기

이제 Spring Boot 환경에서 설정을 진행하겠습니다.

![1](https://user-images.githubusercontent.com/80693904/123541758-21a2c300-d781-11eb-9653-0ca2413e8a87.PNG)

Spring Initializr 를 이용해서 Spring Boot 프로젝트를 만들어줍니다.

다음으로 `pom.xml` 에 아래 코드를 추가시킵니다.

```xml
<!-- https://mvnrepository.com/artifact/org.apache.tiles/tiles-jsp -->
<dependency>
    <groupId>org.apache.tiles</groupId>
    <artifactId>tiles-jsp</artifactId>
    <version>3.0.7</version>
</dependency>

<!-- https://mvnrepository.com/artifact/javax.servlet/jstl -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>jstl</artifactId>
    <version>1.2</version>
</dependency>
```

먼저 `application.properties` 파일을 수정합니다.

```properties
spring.mvc.view.prefix=/WEB-INF/
spring.mvc.view.suffix=.jsp
```

`TilesConfig` 클래스를 추가하고 아래 설정을 추가합니다. 

> TilesConfig.java

```java
@Configuration
public class TilesConfig {
	
	@Bean
    public UrlBasedViewResolver viewResolver() {
    	UrlBasedViewResolver tilesViewResolver = new UrlBasedViewResolver();
    	tilesViewResolver.setViewClass(TilesView.class);
    	tilesViewResolver.setOrder(0);
    	return tilesViewResolver;
    }

    @Bean
    public TilesConfigurer tilesConfigurer() {
        final TilesConfigurer configurer = new TilesConfigurer();

        configurer.setDefinitions(new String[]{"/WEB-INF/tiles/tiles.xml"});
        configurer.setCheckRefresh(true);
        return configurer;
    }
}
```

`/WEB-INF/tiles/tiles.xml` 경로에 xml 파일을 추가합니다.

> tiles.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tiles-definitions PUBLIC "-//Apache Software Foundation//DTD Tiles Configuration 3.0//EN" "http://tiles.apache.org/dtds/tiles-config_3_0.dtd">
<tiles-definitions>
        <definition name="index" template="/WEB-INF/layout/indexLayout.jsp">
                <put-attribute name="header" value="/WEB-INF/layout/indexHeader.jsp" />
                <put-attribute name="footer" value="/WEB-INF/layout/indexFooter.jsp" />
        </definition>

        <definition name="index/*" extends="index">
                <put-attribute name="contents" value="/WEB-INF/index/{1}.jsp" />
        </definition>
        
        <definition name="index/*/*" extends="base">
                <put-attribute name="contents" value="/WEB-INF/index/{1}/{2}.jsp" />
        </definition>
 
        <definition name="index/*/*/*" extends="base">
                <put-attribute name="contents" value="/WEB-INF/index/{1}/{2}/{3}.jsp" />
        </definition>
        
        <definition name="base" template="/WEB-INF/layout/baseLayout.jsp">
                <put-attribute name="header" value="/WEB-INF/layout/baseHeader.jsp" />
                <put-attribute name="footer" value="/WEB-INF/layout/baseFooter.jsp" />
        </definition>
        
         <definition name="base/*" extends="base">
                <put-attribute name="contents" value="/WEB-INF/base/{1}.jsp" />
        </definition>
        
        <definition name="base/*/*" extends="base">
                <put-attribute name="contents" value="/WEB-INF/base/{1}/{2}.jsp" />
        </definition>
 
        <definition name="base/*/*/*" extends="base">
                <put-attribute name="contents" value="/WEB-INF/base/{1}/{2}/{3}.jsp" />
        </definition>
        
</tiles-definitions>
```

`tiles.xml` 에 설정한 대로 디렉토리 구조를 만들어 줍니다.

![image](https://user-images.githubusercontent.com/80693904/123547669-9c2d0c00-d79c-11eb-9305-230c2bbf3346.png)

그리고 `indexLayout.jsp`, `baseLayout.jsp` 파일의 코드를 아래처럼 작성합니다.

간략하게 코드를 설명하면 xml 파일에서 `<put-attribute name="header" value="/webapp/layout/indexHeader.jsp" />` 로 설정했듯이, `indexHeader.jsp` 파일이 `<tiles:insertAttribute name="header"/>` 부분으로 출력이 됩니다.

> indexLayout.jsp, baseLayout.jsp

```jsp
<%@ page pageEncoding="UTF-8" contentType="text/html; charset=utf-8" %>
<%@ taglib uri="http://www.springframework.org/tags" prefix="spring" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>

<!doctype html>
<html lang="ko">
<head>
</head>

<body>
	<header>
		<tiles:insertAttribute name="header"/>
	</header>

	<tiles:insertAttribute name="contents"/>
	
	<footer>
		<tiles:insertAttribute name="footer"/>
	</footer>
</body>
</html>
```

Header 와 Footer 파일은 `<h1>` 태그를 이용하여 간략하게 작성하겠습니다.

> Header.jsp

```jsp
<%@ page pageEncoding="UTF-8" contentType="text/html; charset=utf-8" %>
<%@ taglib uri="http://www.springframework.org/tags" prefix="spring" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>

<h1>baseHeader.jsp</h1>
```

> Footer.jsp

```jsp
<%@ page pageEncoding="UTF-8" contentType="text/html; charset=utf-8" %>
<%@ taglib uri="http://www.springframework.org/tags" prefix="spring" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>

<h1>baseFooter.jsp</h1>
```

컨트롤러도 base 와 index 구분하여 간단하게 작성했습니다.

> indexController.java

```java
@Controller
@RequestMapping("/index")
public class indexController {

	@RequestMapping("/index")
	public String index() {
		return "index/index";
	}
}
```

> baseController.java

```java
@Controller
@RequestMapping("/base")
public class baseController {

	@RequestMapping("/base")
	public String base() {
		return "base/base";
	}
}
```

Spring Boot 를 실행시키고 난 후 `localhost:8080/index/index` 랑 `localhost:8080/base/base` 를 접속해서 정확히 동작하는지 확인합니다.

![image](https://user-images.githubusercontent.com/80693904/123547779-0cd42880-d79d-11eb-8c04-e85cb9a9bdd1.png)

![image](https://user-images.githubusercontent.com/80693904/123547799-21182580-d79d-11eb-9e1d-709215a9f039.png)


* 참고자료
  * [Apache Tiles Documentation 2.2](/https://tiles.apache.org/2.2/framework/index.html)