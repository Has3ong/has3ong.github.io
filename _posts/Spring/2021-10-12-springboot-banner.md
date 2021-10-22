---
title:  "Spring Boot Banner 문구 변경하기"
excerpt: "Spring Boot Banner 문구 변경하기"
categories:
  - Spring
tags:
  - Banner
  - Spring
  - Spring Boot
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## 1. Intro

SpringBoot를 시작할 때 아래와 같은 Spring 문구를 볼 수 있는데, 이를 SpringBoot Banner 라고 합니다.

이 부분을 수정하는 방법을 알아보겠습니다.

포스트 주제 자체가 가벼워서 간단하게 공식문서 그대로 왔습니다. 참고해주시기 바랍니다.

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.5.5)

2021-10-10 10:59:26.281  INFO 78937 --- [ost-startStop-1] com.example.demo.ServletInitializer      : Starting ServletInitializer v0.0.1-SNAPSHOT using Java 1.8.0_241 on gimhaseong-ui-MacBookPro.local with PID 78937 (/Users/has3ong/eclipse-workspace/.metadata/.plugins/org.eclipse.wst.server.core/tmp4/wtpwebapps/demo/WEB-INF/classes started by has3ong in /Applications/Eclipse Java.app/Contents/MacOS)
2021-10-10 10:59:26.287  INFO 78937 --- [ost-startStop-1] com.example.demo.ServletInitializer      : No active profile set, falling back to default profiles: default
2021-10-10 10:59:27.290  INFO 78937 --- [ost-startStop-1] o.a.c.c.C.[.[localhost].[/demo]          : Initializing Spring embedded WebApplicationContext
2021-10-10 10:59:27.290  INFO 78937 --- [ost-startStop-1] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 911 ms
2021-10-10 10:59:28.079  INFO 78937 --- [ost-startStop-1] com.example.demo.ServletInitializer      : Started ServletInitializer in 2.503 seconds (JVM running for 5.243)
2021-10-10 10:59:28.104  INFO 78937 --- [           main] org.apache.catalina.startup.Catalina     : Server startup in 4359 ms
```

## 2. Banner 수정하기

먼저 `resources` 폴더 아래에 `banner.txt` 파일을 생성하고 SpringBoot Banner Test 를 입력해주겠습니다.

```text
SpringBoot Banner Test
```

생성하고 나서 다시 실행시키면 배너가 변경되는것을 알 수 있습니다. 우리는 여기서 한 걸음 더 나아가 보겠습니다.

```
SpringBoot Banner Test
2021-10-10 11:04:21.057  INFO 79365 --- [ost-startStop-1] com.example.demo.ServletInitializer      : Starting ServletInitializer v0.0.1-SNAPSHOT using Java 1.8.0_241 on gimhaseong-ui-MacBookPro.local with PID 79365 (/Users/has3ong/eclipse-workspace/.metadata/.plugins/org.eclipse.wst.server.core/tmp4/wtpwebapps/demo/WEB-INF/classes started by has3ong in /Applications/Eclipse Java.app/Contents/MacOS)
2021-10-10 11:04:21.062  INFO 79365 --- [ost-startStop-1] com.example.demo.ServletInitializer      : No active profile set, falling back to default profiles: default
2021-10-10 11:04:22.274  INFO 79365 --- [ost-startStop-1] o.a.c.c.C.[.[localhost].[/demo]          : Initializing Spring embedded WebApplicationContext
2021-10-10 11:04:22.274  INFO 79365 --- [ost-startStop-1] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 1130 ms
2021-10-10 11:04:23.230  INFO 79365 --- [ost-startStop-1] com.example.demo.ServletInitializer      : Started ServletInitializer in 3.161 seconds (JVM running for 6.102)
2021-10-10 11:04:23.255  INFO 79365 --- [           main] org.apache.catalina.startup.Catalina     : Server startup in 5349 ms
```

아래 SpringBoot Banner Generator 사이트를 들어가서 개발자스러운 배너 텍스트를 복사해서 `banner.txt`에 작성한 후 다시 재시작합니다. 

* [Spring Boot banner.txt generator](https://devops.datenkollektiv.de/banner.txt/index.html)
* [Text to ASCII Art Generator (TAAG)](http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20)

문자가 너무 길어서 저는 두 줄로 출력하겠습니다.

![images](/assets/images/springboot-banner/springboot-banner.png)

그러면 아래와 같이 배너가 변경된 것을 확인할 수 있습니다.

![images](/assets/images/springboot-banner/springboot-banner2.png)

## 3. Banner 환경 변수

추가로 Banner.txt에 사용할 수 있는 환경 변수에 대해 알아보고 마치겠습니다.

|Variable|Description|
|:--|:--|
|${application.version}|The version number of your application, as declared in MANIFEST.MF. For example, Implementation-Version: 1.0 is printed as 1.0.|
|${application.formatted-version}|The version number of your application, as declared in MANIFEST.MF and formatted for display (surrounded with brackets and prefixed with v). For example (v1.0).|
|${spring-boot.version}|The Spring Boot version that you are using. For example 2.5.5.|
|${spring-boot.formatted-version}|The Spring Boot version that you are using, formatted for display (surrounded with brackets and prefixed with v). For example (v2.5.5).|
|${Ansi.NAME} (or ${AnsiColor.NAME}, ${AnsiBackground.NAME}, ${AnsiStyle.NAME})|Where NAME is the name of an ANSI escape code. See AnsiPropertySource for details.|
|${application.title}|The title of your application, as declared in MANIFEST.MF. For example Implementation-Title: MyApp is printed as MyApp.|

## 4. Banner 설정

마지막으로 `SpringApplication` 에서 배너 On/Off 기능을 사용할 수 있는데 아래 코드 참고하시면 됩니다.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication application = new SpringApplication(MyApplication.class);
        application.setBannerMode(Banner.Mode.OFF);
        application.run(args);
    }
}
```  

* 참고자료
    * [Spring Boot Features](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.spring-application)