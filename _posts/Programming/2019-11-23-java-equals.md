---
title : Java equals()와 == 의 차이점
tags :
- Java
- equals()
- ==
---

`equals()` 메소드는 비교자하는 대상의 내용 자체를 비교하지만, `==` 연산자는 비교하고자 하는 대상의 주소값을 비교합니다.

예를들어, String 클래스를 이용한 문자열을 만들어 볼게요.

```
String aString = "Hello World";
String bString = aString;
String cString = new String("Hello World");
```

`aString`, `bString`, `cString`, 을 각각 비교해 보겠습니다.

> Example

```
public class Test {
    public static void main (String[] args){

        String aString = "Hello World";
        String bString = aString;
        String cString = new String("Hello World");

        System.out.println("aString.equals(bString) : " + aString.equals(bString));
        System.out.println("aString.equals(cString) : " + aString.equals(cString));
        System.out.println("bString.equals(cString) : " + bString.equals(cString));
        System.out.println("aString == bString : " + (aString == bString));
        System.out.println("aString == cString : " + (aString == cString));
        System.out.println("bString == cString : " + (bString == cString));
    }
}
```

Result

```
aString.equals(bString) : true
aString.equals(cString) : true
bString.equals(cString) : true
aString == bString : true
aString == cString : false
bString == cString : false
```

주소값을 비교하는 == 연산자에서 `aString`과 `bString`은 서로 같지만 `cString`과는 다르다고 출력이 되었습니다.

왜냐하면 `cString` 은 new 연산자를 통해서 만들어 졌기 때문입니다. 이를 간단한 그림으로 표현하자면 아래와 같습니다.

![image](https://user-images.githubusercontent.com/44635266/69470591-f6086b80-0dda-11ea-9ce4-fba85b9504f1.png)

위와같은 결과가 나온 이유는 Java의 JVM 때문입니다. JVM의 메모리는 여러 구역으로 나뉘어져있습니다. 그 중 Constant Pool, Heap 영역이 존재합니다.

`aString`처럼 리터럴로 선언할 경우, “Hello World”라는 값은 Constant Pool에 저장됩니다. 이후에 또 `bString`과 같이 리터럴로 선언하면, 일단 자바는 Constant Pool에서 `bString`의 값인 “Hello World”를 찾습니다.

만약 존재하면 `bString`를 따로 저장하는게 아니라, 기존에 저장된 “Hello World”객체를 참조합니다. 즉, `aString`과 `bString`는 완전 똑같은 객체입니다. 그래서 `aString` == `bString` 조차도 주소값이 같으므로 **true**가 나옵니다.

`cString`처럼 new를 이용해 선언하면 이 String객체는 Heap영역에 저장됩니다. 즉, Constant Pool에 저장된 `aString`, `bString`와는 주소값이 다릅니다. 그래서 `aString` != `cString` 이 됩니다.