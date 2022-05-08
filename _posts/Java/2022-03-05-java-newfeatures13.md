---
title:  "Java 13 New Features"
excerpt: "Java 13 New Features"
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

새로운 LTS 버전인 JDK 13가 2019년 9월 17일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 13](https://openjdk.java.net/projects/jdk/13/)를 참고했습니다.

### JEP 350:	Dynamic CDS Archives

Java 애플리케이션 실행이 끝날 때 클래스의 동적 아카이브를 허용하도록 애플리케이션 클래스 데이터 공유를 확장합니다. 아카이브된 클래스에는 기본 기본 레이어 CDS 아카이브에 없는 로드된 모든 애플리케이션 클래스와 라이브러리 클래스가 포함됩니다.

#### Goals

* 응용 프로그램 클래스 데이터 공유(AppCDS)의 사용성을 개선합니다. 사용자가 각 응용 프로그램에 대한 클래스 목록을 만들기 위해 시험 실행을 할 필요가 없습니다.
* 클래스 목록을 사용하여 `-Xshare:dump` 옵션에 의해 활성화된 정적 보관은 계속 작동해야 합니다. 여기에는 내장 클래스 로더와 사용자 정의 클래스 로더 모두에 대한 클래스가 포함됩니다.

### JEP 351:	ZGC: Uncommit Unuse Memory

사용하지 않은 힙 메모리를 운영 체제로 반환하도록 ZGC를 향상시킵니다.

#### Description

ZGC 힙은 ZPages라고 하는 힙 영역 집합으로 구성됩니다. 각 ZPage는 다양한 양의 커밋된 힙 메모리와 연결됩니다. ZGC가 힙을 압축하면 ZPage가 해제되어 페이지 캐시인 ZPageCache에 삽입됩니다. 페이지 캐시의 ZPage는 새 힙 할당을 충족하기 위해 재사용할 준비가 되어 있으며, 이 경우 캐시에서 제거됩니다. 메모리 커밋 및 커밋 해제는 비용이 많이 드는 작업이므로 페이지 캐시는 성능에 매우 중요합니다.

페이지 캐시의 ZPage 집합은 커밋되지 않고 운영 체제로 반환될 수 있는 힙의 사용되지 않은 부분을 나타냅니다. 따라서 메모리 커밋 해제는 페이지 캐시에서 잘 선택된 ZPage 집합을 축출하고 이러한 페이지와 관련된 메모리를 커밋 해제하여 수행할 수 있습니다. 페이지 캐시는 이미 ZPage를 LRU(Least-Recently-Used) 순서로 유지하고 크기(소형, 중형, 대형)로 구분하므로 ZPage를 축출하고 메모리 커밋을 해제하는 메커니즘은 비교적 간단합니다. 문제는 캐시에서 ZPage를 제거할 시점을 결정하는 정책을 설계하는 데 있습니다.

간단한 정책은 ZPage가 제거되기 전에 페이지 캐시에 머무를 수 있는 시간을 지정하는 시간 초과 또는 지연 값을 갖는 것입니다. 이 시간 초과에는 재정의하는 명령줄 옵션과 함께 합리적인 기본값이 있습니다. Shenandoah GC는 기본값을 5분으로 지정하고 명령줄 옵션 `-XX:ShenandoahUncommitDelay=<milliseconds>를` 사용하여 기본값을 재정의하는 이와 같은 정책을 사용합니다.

위와 같은 정책은 합리적으로 잘 작동할 수 있습니다. 그러나 새로운 명령줄 옵션을 추가하지 않는 보다 정교한 정책을 구상할 수도 있습니다. 예를 들어, GC 빈도 또는 기타 데이터를 기반으로 적절한 시간 초과 값을 찾는 휴리스틱. 처음에는 `-XX:ZUncommitDelay=<seconds>` 옵션을 사용하여 간단한 시간 제한 정책을 제공하고 나중에 더 정교한 정책(찾을 경우)이 제공되도록 합니다.

커밋 해제 기능은 기본적으로 활성화됩니다. 그러나 정책이 무엇을 결정하든 ZGC는 힙이 최소 크기(`-Xms`) 아래로 내려가도록 메모리 커밋을 해제해서는 안 됩니다. 이는 JVM이 최대 힙 크기(`-Xmx`)와 동일한 최소 힙 크기(`-Xms`)로 시작되는 경우 커밋 해제 기능이 효과적으로 비활성화됨을 의미합니다. 이 기능을 명시적으로 비활성화하기 위해 `-XX:-ZUncommit` 옵션도 제공됩니다.

마지막으로 Linux/x64의 ZGC는 tmpfs 또는 hugetlbfs 파일을 사용하여 힙을 백업합니다. 이러한 파일이 사용하는 메모리 커밋을 해제하려면 `FALLOC_FL_PUNCH_HOLE` 지원이 포함된 `fallocate(2)`가 필요하며, 이는 Linux 3.5(tmpfs) 및 4.3(hugetlbfs)에서 처음 등장했습니다. ZGC는 커밋 해제 기능이 비활성화된 것을 제외하고 이전 Linux 커널에서 실행할 때 이전과 같이 계속 작동해야 합니다.

### JEP 353:	Reimplement the Legacy Socket API

`java.net.Socket` 및 `java.net.ServerSocket` API에서 사용하는 기본 구현을 유지 관리 및 디버그하기 쉬운 보다 간단하고 현대적인 구현으로 교체하십시오. 새로운 구현은 현재 Project Loom에서 탐색 중인 사용자 모드 스레드(일명 파이버) 작업에 쉽게 적응할 수 있습니다.

### JEP 354:	Switch Expressions (Preview)

명령문이나 표현식으로 사용할 수 있도록 `switch`를 확장하고 두 형식 모두 전통적인 대소문자를 사용할 수 있도록 `case ... :` 레이블(폴스루 포함) 또는 새 `case ... ->` 레이블(폴스루 없음) , `switch` 식에서 값을 산출하기 위한 새로운 명령문이 추가되었습니다. 이러한 변경은 일상적인 코딩을 단순화하고 스위치에서 패턴 일치([JEP 305](https://openjdk.java.net/jeps/305))를 사용하는 방법을 준비합니다. 이것은 JDK 13의 미리보기 언어 기능입니다. 

#### Description

##### Arrow labels

`switch` 블록의 기존 `case L :` 레이블 외에도 `case L ->` 레이블이 있는 새로운 단순화된 형식을 제안합니다. 레이블이 일치하면 화살표 오른쪽에 있는 표현식이나 명령문만 실행됩니다. 넘어짐이 없습니다. 예를 들어, 새로운 형태의 레이블을 사용하는 다음 `switch` 문이 주어진다면:

```java
static void howMany(int k) {
    switch (k) {
        case 1  -> System.out.println("one");
        case 2  -> System.out.println("two");
        default -> System.out.println("many");
    }
}
```

다음 코드:

```java
howMany(1);
howMany(2);
howMany(3);
```

결과는 다음과 같습니다.

```java
one
two
many
```

##### Switch expressions

표현식으로 사용할 수 있도록 `switch` 문을 확장합니다. 예를 들어, 이전 `howMany` 메소드는 스위치 표현식을 사용하도록 다시 작성될 수 있으므로 단일 `println`만 사용합니다.

```java
static void howMany(int k) {
    System.out.println(
        switch (k) {
            case  1 -> "one"
            case  2 -> "two"
            default -> "many"
        }
    );
}
```

일반적인 경우 스위치 표현식은 다음과 같습니다.

```java
T result = switch (arg) {
    case L1 -> e1;
    case L2 -> e2;
    default -> e3;
};
```

`switch` 표현식은 폴리 표현식입니다. 대상 유형이 알려진 경우 이 유형은 각 암으로 푸시됩니다. `switch` 표현식의 유형은 알려진 경우 대상 유형입니다. 그렇지 않은 경우 각 케이스 암의 유형을 결합하여 독립형 유형을 계산합니다.

##### Yielding a value

대부분의 `switch` 표현식에는 `case L ->` `switch` 레이블 오른쪽에 단일 표현식이 있습니다. 전체 블록이 필요한 경우, 우리는 값을 산출하기 위해 새로운 `yield` 문을 도입했으며, 이는 둘러싸는 `switch` 표현식의 값이 됩니다.

```java
int j = switch (day) {
    case MONDAY  -> 0;
    case TUESDAY -> 1;
    default      -> {
        int k = day.toString().length();
        int result = f(k);
        yield result;
    }
};
```

`switch` 문은 `switch` 문과 같이 `case L:` `switch` 레이블이 있는 전통적인 `switch` 블록을 사용할 수도 있습니다(의미를 통해 넘어짐을 의미). 이 경우 새로운 `yield` 문을 사용하여 값이 생성됩니다.

```java
int result = switch (s) {
    case "Foo": 
        yield 1;
    case "Bar":
        yield 2;
    default:
        System.out.println("Neither Foo nor Bar, hmmm...");
        yield 0;
};
```

`break`(레이블이 있거나 없는) 및 `yield`라는 두 문은 `switch` 문과 `switch` 식 사이의 명확한 명확성을 용이하게 합니다. `switch` 문은 하지만 `switch` 식은 `break` 문의 대상이 될 수 없습니다. 그리고 `switch` 문이 아닌 `switch` 표현식은 `yield` 문의 대상이 될 수 있습니다.

`switch` 표현식의 이전 미리 보기 버전인 [JEP 325](https://openjdk.java.net/jeps/325)에서 값이 있는 새로운 형태의 `break` 문을 추가하는 것을 제안했는데, 이는 `switch` 표현식에서 값을 생성하는 데 사용됩니다. 이 버전의 `switch` 표현식에서는 새로운 `yield` 문으로 대체됩니다.

##### Exhaustiveness

`switch` 식의 경우는 `exhaustive` 합니다. 가능한 모든 값에 대해 일치하는 `switch` 레이블이 있어야 합니다. (분명히 `switch` 문이 완전할 필요는 없습니다.)

실제로 이것은 일반적으로 `default` 절이 필요함을 의미합니다. 그러나 알려진 모든 상수를 포함하는 열거형 `switch` 식의 경우 컴파일러에서 기본 절을 삽입하여 열거형 정의가 컴파일 시간과 런타임 사이에 변경되었음을 나타냅니다. 이 암시적 `default` 절 삽입에 의존하면 코드가 더 강력해집니다. 이제 코드가 재컴파일될 때 컴파일러는 모든 경우가 명시적으로 처리되는지 확인합니다. 개발자가 명시적 `default` 절을 삽입했다면(오늘날의 경우와 같이) 가능한 오류가 숨겨졌을 것입니다.

또한 `switch` 식은 값으로 정상적으로 완료되거나 예외를 `throw`하여 갑자기 완료되어야 합니다. 이것은 여러 가지 결과를 낳습니다. 먼저 컴파일러는 모든 `switch` 레이블에 대해 일치하는 경우 값을 산출할 수 있는지 확인합니다.

```java
int i = switch (day) {
    case MONDAY -> {
        System.out.println("Monday"); 
        // ERROR! Block doesn't contain a yield statement
    }
    default -> 1;
};
i = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY: 
        yield 0;
    default: 
        System.out.println("Second half of the week");
        // ERROR! Group doesn't contain a yield statement
};
```

추가 결과는 제어 문, `break`, `yield`, `return` 및 `continue`가 다음과 같이 `switch` 식을 통해 이동할 수 없다는 것입니다.

```java
z: 
    for (int i = 0; i < MAX_VALUE; ++i) {
        int k = switch (e) { 
            case 0:  
                yield 1;
            case 1:
                yield 2;
            default: 
                continue z; 
                // ERROR! Illegal jump through a switch expression 
        };
    ...
    }
```

### JEP 355:	Text Blocks (Preview)

Java 언어에 `text blocks` 을 추가합니다. 텍스트 블록은 대부분의 이스케이프 시퀀스가 필요하지 않은 여러 줄 문자열 리터럴이며 예측 가능한 방식으로 문자열의 형식을 자동으로 지정하며 개발자가 원하는 경우 형식을 제어할 수 있도록 합니다. 이것은 JDK 13의 미리보기 언어 기능입니다.

#### Goals

* 일반적인 경우의 이스케이프 시퀀스를 피하면서 소스 코드의 여러 줄에 걸쳐 있는 문자열을 쉽게 표현할 수 있도록 하여 Java 프로그램 작성 작업을 단순화합니다.
* Java가 아닌 언어로 작성된 코드를 나타내는 Java 프로그램에서 문자열의 가독성을 향상시킵니다.
* 모든 새 구문이 동일한 문자열 집합을 문자열 리터럴로 표현하고 동일한 이스케이프 시퀀스를 해석하고 문자열 리터럴처럼 조작할 수 있다고 규정하여 문자열 리터럴에서 마이그레이션을 지원합니다.

#### Description

`text blocks`은 Java 언어에서 새로운 종류의 리터럴입니다. 문자열 리터럴이 나타날 수 있는 모든 위치에서 문자열을 표시하는 데 사용할 수 있지만 표현력이 뛰어나고 우연한 복잡성이 줄어듭니다.

텍스트 블록은 여는 구분 기호와 닫는 구분 기호로 묶인 0개 이상의 콘텐츠 문자로 구성됩니다.

`opening delimiter`는 3개의 큰따옴표 문자(`"""`) 다음에 0개 이상의 공백과 줄 종결자가 오는 시퀀스입니다. 내용은 여는 구분자의 줄 종결자 다음 첫 번째 문자에서 시작됩니다.

`closing delimiter`는 3개의 큰따옴표 문자 시퀀스입니다. 내용은 닫는 구분 기호의 첫 번째 큰따옴표 앞의 마지막 문자에서 끝납니다.

문자열 리터럴의 문자와 달리 내용에 큰따옴표 문자가 직접 포함될 수 있습니다. 텍스트 블록에서 `\"`의 사용은 허용되지만 필수 또는 권장되지는 않습니다. 굵은 구분 기호(`"""`)는 `"` 문자가 이스케이프 처리되지 않고 나타날 수 있고 텍스트 블록을 문자열 리터럴과 시각적으로 구별하기 위해 선택되었습니다.

내용은 문자열 리터럴의 문자와 달리 줄 종결자를 직접 포함할 수 있습니다. 텍스트 블록에서 `\n`을 사용하는 것은 허용되지만 필요하거나 권장되지는 않습니다. 예를 들어, 텍스트 블록:

```java
"""
line 1
line 2
line 3
"""
```

문자열 리터럴과 동일합니다.

```java
"line 1\nline 2\nline 3\n"
```

또는 문자열 리터럴의 연결:

```java
"line 1\n" +
"line 2\n" +
"line 3\n"
```

문자열 끝에 줄 종결자가 필요하지 않은 경우 닫는 구분 기호를 내용의 마지막 줄에 배치할 수 있습니다. 예를 들어, 텍스트 블록:

```java
"""
line 1
line 2
line 3"""
```

문자열 리터럴과 동일합니다.

```java
"line 1\nline 2\nline 3"
```

텍스트 블록은 빈 문자열을 나타낼 수 있지만 두 줄의 소스 코드가 필요하기 때문에 권장하지 않습니다.

```java
String empty = """
""";
```

다음은 잘못된 형식의 텍스트 블록의 몇 가지 예입니다.

```java
String a = """""";   // no line terminator after opening delimiter
String b = """ """;  // no line terminator after opening delimiter
String c = """
           ";        // no closing delimiter (text block continues to EOF)
String d = """
           abc \ def
           """;      // unescaped backslash (see below for escape processing)
```

##### Compile-time processing

텍스트 블록은 문자열 리터럴과 마찬가지로 `String` 유형의 상수 표현식입니다. 그러나 문자열 리터럴과 달리 텍스트 블록의 내용은 Java 컴파일러에서 다음 세 단계로 처리됩니다.

내용의 줄 종결자는 `LF(\u000A)`로 변환됩니다. 이 번역의 목적은 플랫폼 간에 Java 소스 코드를 이동할 때 최소한의 놀라움의 원칙을 따르는 것입니다.

1. Java 소스 코드의 들여쓰기와 일치하도록 도입된 콘텐츠 주변의 부수적인 공백이 제거됩니다.
2. 콘텐츠의 이스케이프 시퀀스가 해석됩니다. 마지막 단계로 해석을 수행하면 개발자가 이전 단계에서 수정하거나 삭제하지 않고도 `\n`과 같은 이스케이프 시퀀스를 작성할 수 있습니다.
3. 처리된 내용은 문자열 리터럴의 문자와 마찬가지로 상수 풀의 `CONSTANT_String_info` 항목으로 클래스 파일에 기록됩니다. 클래스 파일은 `CONSTANT_String_info` 항목이 텍스트 블록에서 파생되었는지 아니면 문자열 리터럴에서 파생되었는지 기록하지 않습니다.

런타임에 텍스트 블록은 문자열 리터럴과 마찬가지로 `String` 인스턴스로 평가됩니다. 텍스트 블록에서 파생된 `String` 인스턴스는 문자열 리터럴에서 파생된 인스턴스와 구별할 수 없습니다. 처리된 내용이 동일한 두 개의 텍스트 블록은 문자열 리터럴과 마찬가지로 인턴으로 인해 동일한 `String` 인스턴스를 참조합니다.

다음 섹션에서는 컴파일 시간 처리에 대해 더 자세히 설명합니다.

###### 1. Line terminators

내용의 줄 종결자는 Java 컴파일러에 의해 `CR(\u000D)` 및 `CRLF(\u000D\u000A)`에서 `LF(\u000A)`로 정규화됩니다. 이렇게 하면 소스 코드가 플랫폼 인코딩으로 변환된 경우에도 콘텐츠에서 파생된 문자열이 플랫폼 간에 동일하게 됩니다(`javac -encoding` 참조).

예를 들어 Unix 플랫폼(행 종결자가 LF인 경우)에서 생성된 Java 소스 코드가 Windows 플랫폼(행 종결자가 CRLF인 경우)에서 편집된 경우 정규화 없이 내용은 각각에 대해 한 문자 더 길어집니다. 라인. 줄 종결자가 되는 LF에 의존하는 모든 알고리즘은 실패할 수 있으며 `String::equals와` 문자열 동일성을 확인하는 데 필요한 모든 테스트는 실패합니다.

이스케이프 시퀀스 `\n(LF)`, `\f(FF)` 및 `\r(CR)`은 정규화 중에 해석되지 않습니다. 이스케이프 처리는 나중에 발생합니다.

###### 2. Incidental white space

동기 부여의 텍스트 블록은 연결된 문자열 리터럴 대응물보다 읽기 쉬웠지만 텍스트 블록의 내용에 대한 명백한 해석에는 여는 구분 기호와 깔끔하게 정렬되도록 포함된 문자열을 들여쓰기 위해 추가된 공백이 포함됩니다. 다음은 개발자가 들여쓰기를 위해 추가한 공간을 시각화하기 위해 점을 사용하는 HTML 예제입니다.

```java
String html = """
..............<html>
..............    <body>
..............        <p>Hello, world</p>
..............    </body>
..............</html>
..............""";
```

여는 구분 기호는 일반적으로 텍스트 블록을 사용하는 명령문이나 표현식과 같은 줄에 나타나도록 위치하므로 14개의 시각화된 공백이 각 줄을 시작한다는 사실에 실질적인 의미는 없습니다. 콘텐츠에 이러한 공백을 포함하면 텍스트 블록이 연결된 문자열 리터럴로 표시된 문자열과 다른 문자열을 나타냅니다. 이는 마이그레이션에 피해를 입히고 반복되는 놀라움의 원인이 됩니다. 개발자가 문자열에서 해당 공백을 원하지 않을 가능성이 압도적으로 많습니다. 또한 닫는 구분 기호는 일반적으로 내용과 정렬되도록 위치하므로 14개의 시각화된 공간이 중요하지 않음을 나타냅니다.

공백은 각 줄 끝에 나타날 수도 있습니다. 특히 텍스트 블록이 다른 파일(더 많은 파일에서 복사-붙여넣기로 구성되었을 수 있음)의 스니펫을 복사하여 붙여넣을 때 채워질 수 있습니다. 다음은 공백을 시각화하기 위해 다시 점을 사용하여 일부 후행 공백으로 재구성된 HTML 예제입니다.

```java
String html = """
..............<html>...
..............    <body>
..............        <p>Hello, world</p>....
..............    </body>.
..............</html>...
..............""";
```

후행 공백은 대부분 의도하지 않고 특이하며 중요하지 않습니다. 개발자가 그것에 대해 신경 쓰지 않을 가능성이 압도적으로 높습니다. 후행 공백 문자는 둘 다 소스 코드 편집 환경의 보이지 않는 아티팩트라는 점에서 줄 종결자와 유사합니다. 내용에 포함된 후행 공백 문자의 존재에 대한 시각적 안내가 없으면 문자열의 길이, 해시 코드 등에 영향을 미치기 때문에 반복적으로 놀라움을 금치 못할 것입니다.

따라서 텍스트 블록의 내용에 대한 적절한 해석은 각 줄의 시작과 끝에서 부수적인 공백을 필수 공백과 구별하는 것입니다. Java 컴파일러는 개발자가 의도한 대로 생성하기 위해 부수적인 공백을 제거하여 콘텐츠를 처리합니다. 그런 다음 원하는 경우 `String::indent`를 사용하여 들여쓰기를 관리할 수 있습니다. 사용 `|` 여백을 시각화하려면:

```java
|<html>|
|    <body>|
|        <p>Hello, world</p>|
|    </body>|
|</html>|
```

`re-indentation algorithm`은 줄 종결자가 LF로 정규화 된 텍스트 블록의 내용을 취합니다. 줄 중 하나 이상이 맨 왼쪽 위치에 공백이 아닌 문자가 있을 때까지 각 콘텐츠 줄에서 동일한 양의 공백을 제거합니다. 여는 `""` 문자의 위치는 알고리즘에 영향을 미치지 않지만 닫는 `"""` 문자의 위치는 자체 행에 배치되는 경우 영향을 미칩니다. 알고리즘은 다음과 같습니다.

1. 모든 LF에서 텍스트 블록의 내용을 분할하여 `individual lines` 목록을 생성합니다. LF에 불과했던 내용의 줄은 개별 줄 목록에서 빈 줄이 됩니다.
2. 개별 라인 목록에서 공백이 아닌 모든 라인을 `determining lines` 세트에 추가합니다. (빈 줄 - 비어 있거나 완전히 공백으로 구성된 줄 - 들여쓰기에 가시적인 영향을 미치지 않습니다. 결정하는 줄 집합에서 빈 줄을 제외하면 알고리즘의 4단계에서 벗어나는 것을 방지할 수 있습니다.)
3. 개별 행 목록의 마지막 행(즉, 닫는 구분 기호가 있는 행)이 `blank` 있으면 이를 결정 행 세트에 추가합니다. (닫는 구분 기호의 들여쓰기는 전체 내용의 들여쓰기에 영향을 미쳐야 합니다. "중요한 후행 줄" 정책입니다.)
4. 각 줄의 선행 공백 문자 수를 계산하고 최소 개수를 취하여 결정 줄 집합의 `common white space prefix`를 계산합니다.
5. 개별 줄 목록의 각 `non-blank` 줄에서 공통 공백 접두사를 제거합니다.
6. 5단계에서 수정된 개별 줄 목록의 모든 줄에서 후행 공백을 모두 제거합니다. 이 단계는 수정된 목록의 전체 공백 줄을 축소하여 비어 있지만 버리지는 않습니다.
7. LF를 줄 사이의 구분 기호로 사용하여 6단계에서 수정된 개별 줄 목록의 모든 줄을 결합하여 결과 문자열을 구성합니다. 6단계 목록의 마지막 줄이 비어 있으면 이전 줄의 결합 LF가 결과 문자열의 마지막 문자가 됩니다.

이스케이프 시퀀스 `\b`(백스페이스) 및 `\t`(탭)는 알고리즘에 의해 해석되지 않습니다. 이스케이프 처리는 나중에 발생합니다.

다시 들여쓰기 알고리즘은 Java 언어 사양에서 규범적입니다. 개발자는 새로운 인스턴스 메서드인 `String::stripIndent`를 통해 액세스할 수 있습니다.

##### Significant trailing line policy

일반적으로 텍스트 블록의 서식을 두 가지 방법으로 지정합니다. 첫째, 여는 구분 기호의 첫 번째 `"` 아래에 표시되도록 콘텐츠의 왼쪽 가장자리를 배치하고, 여는 구분 기호 아래에 정확히 나타나도록 닫는 구분 기호를 자체 줄에 배치합니다. 결과 문자열은 줄 시작 부분에 공백이 없으며 닫는 구분 기호의 후행 공백 줄을 포함하지 않습니다.

그러나 후행 공백 행은 결정 행으로 간주되기 때문에 왼쪽으로 이동하면 공통 공백 접두어를 줄이는 효과가 있으므로 모든 행의 시작 부분에서 제거되는 공백의 양이 줄어듭니다. 극단적인 경우 닫는 구분 기호가 왼쪽 끝까지 이동하면 일반적인 공백 접두사를 0으로 줄여 공백 제거를 효과적으로 선택 해제합니다.

예를 들어 닫는 구분 기호를 왼쪽 끝까지 이동하면 점으로 시각화할 부수적인 공백이 없습니다.

```java
String html = """
              <html>
                  <body>
                      <p>Hello, world</p>
                  </body>
              </html>
""";
```

230 / 5,000
번역 결과
닫는 구분 기호가 있는 후행 공백 줄을 포함하여 일반적인 공백 접두사는 0이므로 각 줄의 시작 부분에서 공백이 제거됩니다. 따라서 알고리즘은 다음을 생성합니다. (`|`을 사용하여 왼쪽 여백을 시각화) 

```java
|              <html>
|                  <body>
|                      <p>Hello, world</p>
|                  </body>
|              </html>
```

또는 닫는 구분 기호가 왼쪽 끝까지 이동하지 않고 `html`의 `t` 아래로 이동하여 변수 선언보다 8칸 더 깊다고 가정합니다.

```java
String html = """
              <html>
                  <body>
                      <p>Hello, world</p>
                  </body>
              </html>
        """;
```

점으로 시각화된 공간은 부수적인 것으로 간주됩니다.

```java
String html = """
........      <html>
........          <body>
........              <p>Hello, world</p>
........          </body>
........      </html>
........""";
```

닫는 구분 기호가 있는 후행 공백 줄을 포함하여 일반적인 공백 접두사는 8이므로 각 줄의 시작 부분에서 8개의 공백이 제거됩니다. 따라서 알고리즘은 닫는 구분 기호를 기준으로 콘텐츠의 필수 들여쓰기를 유지합니다.

```java
|      <html>
|          <body>
|              <p>Hello, world</p>
|          </body>
|      </html>
```

마지막으로 닫는 구분 기호가 콘텐츠의 `right`으로 약간 이동했다고 가정합니다.

```java
String html = """
              <html>
                  <body>
                      <p>Hello, world</p>
                  </body>
              </html>
                  """;
```

점으로 시각화된 공간은 부수적인 것으로 간주됩니다.

```java
String html = """
..............<html>
..............    <body>
..............        <p>Hello, world</p>
..............    </body>
..............</html>
..............    """;
```

일반적인 공백 접두사는 14이므로 각 줄의 시작 부분에서 14개의 공백이 제거됩니다. 후행 빈 줄은 제거되어 빈 줄을 남기고 마지막 줄은 삭제됩니다. 즉, 닫는 구분 기호를 콘텐츠 오른쪽으로 이동해도 효과가 없으며 알고리즘은 다시 콘텐츠의 필수 들여쓰기를 유지합니다.

```java
|<html>
|    <body>
|        <p>Hello, world</p>
|    </body>
|</html>
```

###### 3. Escape sequences

내용을 다시 들여쓴 후 내용의 모든 `escape sequences`가 해석됩니다. 텍스트 블록은 `\n`, `\t`, `\'`, `\"` 및 `\\`와 같은 문자열 리터럴과 동일한 이스케이프 시퀀스를 지원합니다. 전체 목록은 Java 언어 사양의 섹션 3.10.6을 참조하십시오. 개발자는 새로운 인스턴스 메서드인 `String::translateEscapes`를 통해 이스케이프 처리에 액세스합니다.

이스케이프를 마지막 단계로 해석하면 개발자는 1단계에서 줄 종결자의 변환에 영향을 주지 않고 문자열의 세로 서식 지정에 `\n`, `\f` 및 `\r`을 사용하고 가로 서식 지정에 `\b` 및 `\t`를 사용할 수 있습니다. 2단계에서 우발적인 공백 제거에 영향을 주지 않는 문자열입니다. 예를 들어 `\r` 이스케이프 시퀀스(CR)가 포함된 다음 텍스트 블록을 고려하십시오.

```java
String html = """
              <html>\r
                  <body>\r
                      <p>Hello, world</p>\r
                  </body>\r
              </html>\r
              """;
```

CR 이스케이프는 줄 종결자가 LF로 정규화될 때까지 처리되지 않습니다. 유니코드 이스케이프를 사용하여 `LF(\u000A)` 및 `CR(\u000D)`을 시각화하면 결과는 다음과 같습니다.

```java
|<html>\u000D\u000A
|    <body>\u000D\u000A
|        <p>Hello, world</p>\u000D\u000A
|    </body>\u000D\u000A
|</html>\u000D\u000A
```

여는 또는 닫는 구분 기호 옆에도 텍스트 블록 내에서 `"`를 자유롭게 사용하는 것은 합법적입니다. 예를 들면 다음과 같습니다.

```java
String story = """
    "When I use a word," Humpty Dumpty said,
    in rather a scornful tone, "it means just what I
    choose it to mean - neither more nor less."
    "The question is," said Alice, "whether you
    can make words mean so many different things."
    "The question is," said Humpty Dumpty,
    "which is to be master - that's all."
    """;
```

여는 또는 닫는 구분 기호 옆에도 텍스트 블록 내에서 `"`를 자유롭게 사용하는 것은 합법적입니다. 예를 들면 다음과 같습니다.

```java
String code = 
    """
    String text = \"""
        A text block inside a text block
    \""";
    """;
```

##### Concatenation of text blocks

텍스트 블록은 문자열 리터럴을 사용할 수 있는 모든 곳에서 사용할 수 있습니다. 예를 들어, 텍스트 블록과 문자열 리터럴은 서로 바꿔서 연결할 수 있습니다.

```java
String code = "public void print(Object o) {" +
              """
                  System.out.println(Objects.toString(o));
              }
              """;
```

그러나 텍스트 블록과 관련된 연결은 다소 복잡할 수 있습니다. 이 텍스트 블록을 시작점으로 삼으십시오.

```java
String code = """
              public void print(Object o) {
                  System.out.println(Objects.toString(o));
              }
              """;
```

`o` 유형이 변수에서 나오도록 변경해야 한다고 가정합니다. 연결을 사용하여 후행 코드가 포함된 텍스트 블록은 새 줄에서 시작해야 합니다. 불행히도, 아래와 같이 프로그램에 줄 바꿈을 직접 삽입하면 유형과 `o` 로 시작하는 텍스트 사이에 긴 공백이 생깁니다.

```java
String code = """
              public void print(""" + type + """
                                                 o) {
                  System.out.println(Objects.toString(o));
              }
              """;
```

공백은 수동으로 제거할 수 있지만 인용된 코드의 가독성을 떨어뜨립니다.

```java
String code = """
              public void print(""" + type + """
               o) {
                  System.out.println(Objects.toString(o));
              }
              """;
```

더 깔끔한 대안은 다음과 같이 `String::replace` 또는 `String::format`을 사용하는 것입니다.

```java
String code = """
              public void print($type o) {
                  System.out.println(Objects.toString(o));
              }
              """.replace("$type", type);
String code = String.format("""
              public void print(%s o) {
                  System.out.println(Objects.toString(o));
              }
              """, type);
```              

또 다른 대안은 다음과 같이 사용할 수 있는 새 인스턴스 메서드 `String::formatted`의 도입과 관련이 있습니다.

```java
String source = """
                public void print(%s object) {
                    System.out.println(Objects.toString(object));
                }
                """.formatted(type);
```


##### Additional Methods

텍스트 블록을 지원하기 위해 다음 메서드가 추가됩니다.

* `String::stripIndent():` 텍스트 블록 내용에서 부수적인 공백을 제거하는 데 사용됩니다.
* `String::translateEscapes():` 이스케이프 시퀀스를 번역하는 데 사용
* `String::formatted(Object... args):` 텍스트 블록에서 값 대체 단순화 