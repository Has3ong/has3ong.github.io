---
title : Java Overriding / OverLoading
tags :
- Overloading
- Overriding
- Java
---

## OverLoading

오버로딩(Overloading)은 메소드 오버로딩과 생성자 오버로딩이 있다. 하지만 둘다 같은 개념이다.

같은 이름의 함수를 여러 개 정의하고, 매개변수의 유형과 개수를 다르게 하여 다양한 유형의 호출에 응답하게 한다.

> Example

```
class Calculator{
    public void sum(int a, int b){
        System.out.println("public void sum(int a, int b) is called value is : " + (a + b));
    }

    public void sum(int a, int b, int c){
        System.out.println("public void sum(int a, int b, int c) is called value is : " + (a + b + c));
    }

    public void sum(double a, double b){
        System.out.println("public void sum(double a, double b) is called value is : " + (a + b));
    }

}

public class Test {

    public static void main (String[] args){
        Calculator calculator = new Calculator();
        calculator.sum(1, 2);
        calculator.sum(1, 2, 3);
        calculator.sum(1.53, 2.51);
    }
}
```

## Overriding

상위 클래스가 가지고 있는 멤버변수가 하위 클래스로 상속되는 것처럼 상위 클래스가 가지고 있는 메소드도 하위 클래스로 상속되어 하위 클래스에서 사용할 수 있다. 하지만, 하위 클래스에서 메소드를 재정의해서 사용할 수 있다.

상속 관계에 있는 클래스 간에 같은 이름의 메소드를 **재정의**하는 기술을 오버라이딩(Overriding) 이라고 한다.

하지만 오버로딩과 다르게 **매개변수**, **함수 명**, **반환 타입** 모든게 똑같아야 한다.

```
class Calculator{
    public void sum(int a, int b){
        System.out.println("Calculator Class is called value is : " + (a + b));
    }
}

class otherCalculator extends Calculator{

    @Override
    public void sum(int a, int b){
        System.out.println("otherCalculator Class is called value is : " + (a + b));
    }
}

public class Test {

    public static void main (String[] args){
        Calculator calculator = new Calculator();
        otherCalculator other = new otherCalculator();

        calculator.sum(1, 2);
        other.sum(1, 2);

    }
}
```