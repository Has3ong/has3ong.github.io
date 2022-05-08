---
title : JAR / WAR 차이점 및 특징 
tags : 
- WAR
- JAR
- Computer Science
categories:
- Programming
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## JAR / WAR

일단 두 파일 모두 `jar` 툴을 사용한 압축 파일인데 사용 목적이 다릅니다.

### JAR (Java Archive)

*.jar* 파일은 Class 와 같은 Java 리소스와 속성 파일, 라이브러리 파일이 포함되어 있습니다. 쉽게 말하면 Java 어플리케이션이 동작할 수 있도록 Java 프로젝트를 압축한 파일이라 생각하면 됩니다.

JAR 파일은 원하는 구조로 구성이 가능하며 JDK 에 포함하고 있는 JRE 만 가지고도 실행이 가능합니다.

아래는 예시로 나타낸 JAR 파일 구조입니다.

```
META-INF/
    MANIFEST.MF
com/
    baeldung/
        MyApplication.class
```

### WAR (Web Application Archive)

*.war* 파일은 servlet, jsp, jar, html 등등 Servlet Context 파일이 포함되어 있습니다. 즉, JAR 파일과 달리 웹 어플리케이션을 지원하기 위한 압축 방식입니다.

JAR 파일과 달리 WAR 파일은 WEB-INF 와 META-INF 디렉토리로 정의된 구조를 사용하며, WAR 파일을 실행하기 위해선 Tomcat, Apache 와 같은 Web Server 나 WAS 가 필요합니다.

아래는 예시로 나타낸 WAR 파일 구조입니다.

```
META-INF/
    MANIFEST.MF
WEB-INF/
    web.xml
    jsp/
        helloWorld.jsp
    classes/
        static/
        templates/
        application.properties
    lib/
        // *.jar files as libs
```

### EAR (Enterprise Archive)

추가로 EAR 은 Java EE(Enterprise Edition) 에 쓰이는 파일 형식으로 한 개 이상의 모듈을 단일 아카이브로 패키징 하여 어플리케이션 서버에 동시에 일관적으로 올리기 위해 사용하는 포맷입니다.

### JAR vs WAR vs EAR

세 파일의 차이를 알아보기위 해선 아래 그림이 가장 적절하다고 생각됩니다.

![image](https://user-images.githubusercontent.com/44635266/81690703-a73cb400-9496-11ea-9588-a41277e239da.png)

## References

* https://web.archive.org/web/20120626012843/http://java.sun.com/developer/Books/javaprogramming/JAR/basics
* https://web.archive.org/web/20120626020019/http://java.sun.com/j2ee/tutorial/1_3-fcs/doc/WCC3.html
* https://www.baeldung.com/java-jar-war-packaging
* https://simuing.tistory.com/269