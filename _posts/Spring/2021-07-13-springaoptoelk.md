---
title:  "Spring Boot AOP 를 이용하여 로그를 작성하고 ELK 스택 연동 -1-"
excerpt: "Spring Boot AOP 를 이용하여 로그를 작성하고 ELK 스택 연동 -1-"
categories:
  - Spring
tags:
  - Log
  - AOP
  - Spring
  - Spring Boot
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

위 포스트는 2개로 나누어서 -1- 에서는 Spring Boot 를 설정 및 로그를 출력하여 파일에 저장하기까지 과정을 작성하겠습니다. -2- 에서는 ELK 를 실제로 윈도우 환경에 설치하여 Filebeat 를 이용하여 수집하고 Elasticsearch 에 저장하여 Kibana 에 Visualization 하겠습니다.

상세하게 진행하면 포스트 길이가 길어지니 중요한 부분만 작성하겠습니다.

## AOP 란?

**AOP**는 **Aspect Oriented Programming**의 약자로 관점 지향 프로그램이라고도 불립니다. 쉽게 말해 분리를 허용하여 모듈성을 증가시키는 것이 목적인 프로그래밍 패러다임입니다. 여기서 모듈은 공통된 로직이나 기능을 하나의 단위로 묶는 것을 말합니다.

AOP 에서 각 관점을 기준으로 로직을 모듈화한다는 것은 코드들을 부분적으로 나눠 모듈화하겠다는 의미이며, 이때 소스 코드상 다른 부분에 반복해서 쓰는 코드를 볼 수 있는데 이를 **횡단 관심사(cross-cutting concern)** 라고 합니다. 이 횡단 관심사의 대표적인 예로 로깅이 있습니다. 로깅은 필연적으로 시스템 상에서 로그되는 모든 부분에 영향을 미치기 때문입니다. 그러므로 로깅은 로그가 되는 모든 클래스들과 메소드를 횡단합니다.

AOP 를 이용하여 기능의 코드 핵심부를 로깅과 같은 코드로 채우지 않고도 비즈니스 로직에 핵심적이지 않은 로직들을 프로그램에 추가할 수 있게 합니다.

Spring AOP 의 주요 개념은 아래에서 다시 설명하겠습니다.

## Spring Boot 설정하기.

먼저 [Spring initializr]() 를 이용해 간단한 프로젝트를 만듭니다.

![1](https://user-images.githubusercontent.com/80693904/123505415-f42f1a00-d699-11eb-9ee8-e68495c689ca.PNG)

만들어진 프로젝트에 압축을 풀고 환경을 설정한 후 테스트할 Controller, Service 구조를 만들어줍니다.

![6](https://user-images.githubusercontent.com/80693904/123505459-2b053000-d69a-11eb-87f3-83bb39ace65a.PNG)

저는 각각의 파일을 아래와 같이 작성했습니다.

> AOPController.java

```java
@Controller
@RequestMapping("/")
public class AOPController {
	
	@Autowired AOPService aopService;
	
	@RequestMapping("/index")
	public String index(@RequestParam HashMap<String, Object> param) {
		HashMap<String, Object> result = aopService.index(param);
		return "index.jsp";
	}
}
```

> AOPService.java

```java
public interface AOPService {
	public HashMap<String, Object> index(HashMap<String, Object> param) ;
}
```

> AOPServiceImpl.java

```java
@Service
public class AOPServiceImpl implements AOPService {
	public HashMap<String, Object> index(HashMap<String, Object> param) {
		return param;
	}
}
```

> index.jsp

```jsp
<h1>Hello World</h1>
```

그리고 톰캣에 올려 Spring Boot 를 실행시킨 후 정상적으로 출력이 되는걸 확인하면, 다음으로 Log 를 설정하겠습니다.

![7](https://user-images.githubusercontent.com/80693904/123505474-407a5a00-d69a-11eb-982d-8483f36bbd50.PNG)

## Spring Log 출력 설정하기

`src/main/resources/` 경로에 `logback-spring.xml` 파일을 추가한 후 아래와 같이 설정을 해줍니다.

`LOG_PATH` 및 `CONSOLE_LOG_PATH` 는 컴퓨터 환경에 맞춰서 작성하시면 됩니다.

한가지 살펴볼 부분은 `ELK` 부분에 메세제 패턴을 `%msg%n` 으로 작성한 부분입니다. 기존 로그는 날짜와, 로그 타입 부분을 같이 선언하지만, 현 포스트에서는 필요한 칼럼을 만들어서 JSON 형태로 만들어서 출력할 예정이라 `%msg` 하나만 선언했습니다.

> logback-spring.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/base.xml"/>
    <timestamp key="TIMESTAMP" datePattern="yyyyMMdd"/>

    <springProfile name="local">
        <property name="LOG_PATH" value="C:/Users/khsh5/Desktop/logs"/>
        <property name="CONSOLE_LOG_PATH" value="C:/Users/khsh5/Desktop/consolelogs"/>
    </springProfile>

    <appender name="DEFAULT" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <encoder>
            <pattern>[%d{yyyy-MM-dd HH:mm:ss}] [%-5level] [%logger{0}:%line] - %msg%n</pattern>
        </encoder>
        <prudent>true</prudent>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${CONSOLE_LOG_PATH}/${HOSTNAME}.console-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>500MB</maxFileSize>
        </rollingPolicy>
    </appender>
    
    <appender name="ELK" class="ch.qos.logback.core.rolling.RollingFileAppender">
  	<encoder>
  		<pattern>%msg%n</pattern>
	</encoder>
	<prudent>true</prudent>
	<rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
		<fileNamePattern>${LOG_PATH}/${HOSTNAME}.filebeat-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
		<maxFileSize>500MB</maxFileSize>
	</rollingPolicy>
  </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="DEFAULT"/>
    </root>

    <logger name="ELK_LOGGER" level="INFO" additivity="false">
    	<appender-ref ref="ELK"/>
    </logger>
</configuration>
```

다음은 출력할 로그의 구조 및 칼럼을 정의합니다. `LogELK` 라는 클래스를 만들어서 출력할 칼럼을 작성합니다. 지금 만든 `LogELK` 클래스를 `ObjectMapper` 객체를 이용하여 JSON 으로 변환하여 사용할 것입니다.

프로젝트나 환경에 따라서 칼럼은 조정해서 사용하시면 됩니다. Getter 와 Setter 함수는 코드가 너무 길어져서 삭제를 했습니다.

> LogELK.java

```java
package log;

public class LogELK {
	String timestamp;
	String hostname;
	String hostIp;
	String clientIp;
	String clientUrl;
	String callFunction;
	String type;
	String parameter;
}
```

## Spring AOP 설정하기

### AOP 주요 개념

* Aspect - 위에서 알아본 횡단 관심사를 모듈화한 것입니다.
* Target - Aspect 를 적용할 대상입니다.
* Advice - 실질적으로 부가기능을 담은 구현체입니다.
* JoinPoint - Advice 가 적용될 위치이며, Spring 에서는 메소드 조인포인트만 제공합니다. 즉, 메소드를 가리킨다고 생각해도 됩니다.
* PointCut - 부가기능이 적용될 메소드를 선정하는 방법입니다.

또한 스프링에서는 Aspect 의 실행 시점을 지정할 수 있는 어노테이션이 있습니다. 아래 참고한 이미지를 보시면 됩니다.

* **@Before**(메소드 실행 이전)
* **@After**(메소드 실행 이후)
* **@AfterReturning**(메소드 정상 반환)
* **@AfterThrowing**(예외 발생)
* **@Around**(메소드 실행 전후)

![image](https://i.loli.net/2019/06/01/5cf1f4f78070020870.jpg)

> 이미지 참고 - [Spring AOP](https://m.blog.naver.com/dkdldoafotn/221655932482)

### AOP 설정하기

이제 AOP 를 설정하여 로그를 출력하겠습니다. 먼저 `pom.xml` 파일에 `spring-boot-starter-aop` 를 추가합니다. 

> pom.xml

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
    <version>2.5.1</version>
</dependency>
```

다음으로 `AspectELK.java` 파일을 만들어서 아래와 같이 코드를 작성합니다. 상세 코드는 아래에 다시 기술하겠습니다.

`@AfterReturning(pointcut="bean(*ServiceImpl)", returning="retVal")` 이라는 구문이 눈에 들어오실겁니다. 이 구문은 해당 AOP 함수의 실행 범위를 설정하는데, 빈의 이름이 `ServiceImpl` 로 끝나는 빈의 모든 메소드를 포함합니다. 그리고 이 함수의 실행결과는 `retVal` 이라는 변수에 저장되어 전달합니다.

예외처리는 본 포스트에 작성하지 않았지만, 아래와 같이 사용하시면 됩니다.

```java
@AfterThrowing((pointcut="bean(*ServiceImpl)",throwing="exception")
public void afterThrowingTargetMethod(JoinPoint thisJoinPoint, Exception exception) throws Exception { ... }
```

> AspectELK.java

```java
@Aspect
@Component
public class AspectELK {
	private static final String TIMESTAMP_FORMAT = "yyyy-MM-dd HH:mm:ss.SSS";
	private static final Logger log = LoggerFactory.getLogger("ELK_LOGGER");
	private ObjectMapper mapper = new ObjectMapper();
	
	private String host = "";
	private String ip = "";
	private String clientIp = "";
	private String clientUrl = "";
	
	@PostConstruct
    public void init() throws UnknownHostException {
		InetAddress addr = InetAddress.getLocalHost();
    	this.host = addr.getHostName();
		this.ip = addr.getHostAddress();
    }
	
	@Around("bean(*Controller)")
	public Object controllerAroundLogging(ProceedingJoinPoint pjp) throws Throwable { ... }
	
	@Before("bean(*ServiceImpl)")
	public void serviceBeforeLogging(JoinPoint pjp) throws Throwable { ... }
	
	@AfterReturning(pointcut="bean(*ServiceImpl)", returning="retVal")
	public void serviceAfterReturningLogging(JoinPoint pjp, Object retVal) throws Throwable { ... }
}
```

#### @Around

`@Around` 는 메소드 수행 전후에 수행됩니다. `@Around` 를 구현한 메소드는 반드시 `ProceedingJoinPoint` 를 첫 번째 파라미터로 지정해야 합니다. 그렇지 않으면 오류가 발생합니다.

눈여겨봐야할 구문은 `Object result = pjp.proceed();` 구문입니다.  

`@Around` 는 특성상 클라이언트의 호출을 가로채기 때문에 비즈니스 로직을 호출해주지 않으면 실행되지 않습니다. 그렇기 위해서는 비즈니스 메소드에 대한 정보를 가지고 있어야 하는데, 이 정보가 `ProceedingJoinPoint` 객체입니다.

이 객체의 `proceed()` 함수를 호출하여 비즈니스 로직을 진행하게 합니다. 즉, `proceed()` 를 기준으로 비즈니스 메소드 수행 전과 후가 나뉘어집니다. 그래서 아래 코드에서도 `log.info()` 를 `proceed()` 함수 전후로 출력하는걸 확인할 수 있습니다.

```java
@Around("bean(*Controller)")
public Object controllerAroundLogging(ProceedingJoinPoint pjp) throws Throwable {
	String timeStamp = new SimpleDateFormat(TIMESTAMP_FORMAT).format(new Timestamp(System.currentTimeMillis()));
	HttpServletRequest request = ((ServletRequestAttributes)RequestContextHolder.currentRequestAttributes()).getRequest();
	this.clientIp = request.getRemoteAddr();
	this.clientUrl = request.getRequestURL().toString();
	String callFunction = pjp.getSignature().getDeclaringTypeName() + "." + pjp.getSignature().getName();
	
	LogELK logelk = new LogELK();
	logelk.setTimestamp(timeStamp);
	logelk.setHostname(host);
	logelk.setHostIp(ip);
	logelk.setClientIp(clientIp);
	logelk.setClientUrl(clientUrl);
	logelk.setCallFunction(callFunction);
	logelk.setType("CONTROLLER_REQ");
	logelk.setParameter(mapper.writeValueAsString(request.getParameterMap()));
	log.info("{}", mapper.writeValueAsString(logelk));
	
	Object result = pjp.proceed();
	
	timeStamp = new SimpleDateFormat(TIMESTAMP_FORMAT).format(new Timestamp(System.currentTimeMillis()));
	
	logelk.setTimestamp(timeStamp);
	logelk.setType("CONTROLLER_RES");
	logelk.setParameter(mapper.writeValueAsString(result));
	log.info("{}", mapper.writeValueAsString(logelk));

	return result;
}
```

#### @Before

`JoinPoint` 객체가 필요한 경우 파라미터를 작성하면 됩니다. 아래에서는 서비스 함수를 호출할 때 전달받은 Parameter 를 출력하기 위해 작성하였습니다.

```java
@Before("bean(*ServiceImpl)")
public void serviceBeforeLogging(JoinPoint pjp) throws Throwable {
	String timeStamp = new SimpleDateFormat(TIMESTAMP_FORMAT).format(new Timestamp(System.currentTimeMillis()));
	String callFunction = pjp.getSignature().getDeclaringTypeName() + "." + pjp.getSignature().getName();
	
	Object[] argNames = pjp.getArgs();

	LogELK logelk = new LogELK();
	logelk.setTimestamp(timeStamp);
	logelk.setHostname(host);
	logelk.setHostIp(ip);
	logelk.setClientIp(clientIp);
	logelk.setClientUrl(clientUrl);
	logelk.setCallFunction(callFunction);
	logelk.setType("SERVICE_REQ");
	logelk.setParameter(mapper.writeValueAsString(argNames));
	log.info("{}", mapper.writeValueAsString(logelk));
}
```

#### @AfterReturning

메소드가 정상적으로 실행된 경우에 작동합니다. `returning="retVal"` 은 리턴 값을 전달 받을 파라미터를 명시한것입니다. 만약 메소드가 정상적을 실행되지 않고 오류가 발생하면 `@AfterReturning` 이 아니라 `@AfterThrowing` 으로 전달됩니다.

```java
@AfterReturning(pointcut="bean(*ServiceImpl)", returning="retVal")
public void serviceAfterReturningLogging(JoinPoint pjp, Object retVal) throws Throwable {
	String timeStamp = new SimpleDateFormat(TIMESTAMP_FORMAT).format(new Timestamp(System.currentTimeMillis()));
	String callFunction = pjp.getSignature().getDeclaringTypeName() + "." + pjp.getSignature().getName();

	LogELK logelk = new LogELK();
	logelk.setTimestamp(timeStamp);
	logelk.setHostname(host);
	logelk.setHostIp(ip);
	logelk.setClientIp(clientIp);
	logelk.setClientUrl(clientUrl);
	logelk.setCallFunction(callFunction);
	logelk.setType("SERVICE_RES");
	logelk.setParameter(mapper.writeValueAsString(retVal));
	log.info("{}", mapper.writeValueAsString(logelk));
	
}
```

전체 프로젝트 파일 구조는 아래와 같습니다.

![image](https://user-images.githubusercontent.com/80693904/123506027-05c5f100-d69d-11eb-89fb-b2e0c56b06f1.png)

## 로그 확인하기

이제 SpringBoot 를 실행시키고 로그를 확인해보겠습니다.

Spring Boot 를 실행시키면 자동적으로 내가 `logback-spring.xml` 에 설정한 경로에 파일이 생깁니다.

![9](https://user-images.githubusercontent.com/80693904/123506957-e54c6580-d6a1-11eb-891d-b4cf85e83e43.PNG)

폴더로 접속항여 파일을 확인해보면 아래와 같이 로그가 출력됩니다.

> 콘솔로그

```
[2021-06-24 21:46:08] [INFO ] [ServletInitializer:55] - Starting ServletInitializer v0.0.1-SNAPSHOT on DESKTOP-R07FVQK with PID 14856 (C:\Users\khsh5\eclipse-workspace\.metadata\.plugins\org.eclipse.wst.server.core\tmp0\wtpwebapps\demo\WEB-INF\classes started by khsh5 in C:\Users\khsh5\Desktop)
[2021-06-24 21:46:08] [INFO ] [ServletInitializer:652] - The following profiles are active: local
[2021-06-24 21:46:09] [INFO ] [[/]:173] - Initializing Spring embedded WebApplicationContext
[2021-06-24 21:46:09] [INFO ] [ServletWebServerApplicationContext:285] - Root WebApplicationContext: initialization completed in 926 ms
[2021-06-24 21:46:09] [INFO ] [ThreadPoolTaskExecutor:181] - Initializing ExecutorService 'applicationTaskExecutor'
[2021-06-24 21:46:10] [INFO ] [ServletInitializer:61] - Started ServletInitializer in 2.687 seconds (JVM running for 5.389)
[2021-06-24 21:46:10] [INFO ] [Catalina:173] - Server startup in 4658 ms
[2021-06-24 21:46:34] [INFO ] [[/]:173] - Initializing Spring DispatcherServlet 'dispatcherServlet'
[2021-06-24 21:46:34] [INFO ] [DispatcherServlet:525] - Initializing Servlet 'dispatcherServlet'
[2021-06-24 21:46:34] [INFO ] [DispatcherServlet:547] - Completed initialization in 13 ms
```

> 파일비트 로그 - localhost:8080 접속 

```json
{"timestamp":"2021-06-24 21:46:34.166","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_REQ","parameter":"{}"}
{"timestamp":"2021-06-24 21:46:34.253","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_REQ","parameter":"[{}]"}
{"timestamp":"2021-06-24 21:46:34.266","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_RES","parameter":"{}"}
{"timestamp":"2021-06-24 21:46:34.267","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_RES","parameter":"\"index.jsp\""}
```

> 파일비트 로그 - localhost:8080?param1=filebeat&framework=springboot&language=java 접속 

Parameter 정보 있을 경우 아래와 같이 출력이 됩니다. 출력 방식은 프로젝트나 상황에 맞춰 변경하여 사용하면 됩니다.

```json
{"timestamp":"2021-06-24 22:06:03.138","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_REQ","parameter":"{\"param1\":[\"filebeat\"],\"framework\":[\"springboot\"],\"language\":[\"java\"]}"}
{"timestamp":"2021-06-24 22:06:03.234","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_REQ","parameter":"[{\"param1\":\"filebeat\",\"framework\":\"springboot\",\"language\":\"java\"}]"}
{"timestamp":"2021-06-24 22:06:03.246","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_RES","parameter":"{\"param1\":\"filebeat\",\"framework\":\"springboot\",\"language\":\"java\"}"}
{"timestamp":"2021-06-24 22:06:03.247","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_RES","parameter":"\"index.jsp\""}
```

다음 포스트에서 파일비트 설치 후 로그 수집 및 ELK 뷰어까지 알아보겠습니다.

* 참고자료
  * [Complete Spring AOP Tutorial](/https://jstobigdata.com/spring/complete-spring-aop-tutorial/)
  * [Spring AOP Tutorial](/https://www.tutorialspoint.com/springaop/index.htm)
  * [표준프레임워크 포털 eGovFrame](https://www.egovframe.go.kr/wiki/doku.php?id=egovframework:rte:fdl:aop:aspectj)