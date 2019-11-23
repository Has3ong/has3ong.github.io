---
title : Java Abstract Class와 Interface의 차이점
tags :
- Java
- Abstract Class
- Interface
---

## Abstract Class

Java에서 추상클래스(Abstract Class)는 **미완성된 클래스**라고 표현을 한다.

추상 클래스의 목적은 기존의 클래스에서 공통된 부분을 추상화하여 상속하는 클래스에게 구현을 강제화하여 메서드의 동작을 구현하는 자식클래스로 책임을 위임한 후 공유의 목적 이라고 할 수 있습니다. 즉, 추가적인 확장이 가능합니다.

선언은 다음과 같이 합니다. 

```
abstract class Animal
```

클래스 상속은 `extends`를 사용하면 됩니다.

```
class Dog extends Animal
```

추상클래스에는 일반 메소드와 추상 메소드로 구분이 되는데 추상 메소드는 내용이 없는 메소드 입니다. 즉 구현이 되지 않은 메소드입니다. 다음과 같이 작성하시면 됩니다. 

```
public abstract void Bye();
```

추상 메소드를 자식클래스에서 구현할 때에는 `@Override`를 이용해야 합니다.

> Example

```
abstract class Animal{
    // Method
    public void Hello(){
        System.out.println("Hello World");
    }
    // Abstract Method
    public abstract void Bye();
}

class Dog extends Animal{
    @Override
    public void Bye(){
        System.out.println("Bye Dog");
    }

    public void Run(){
        System.out.println("Dog is Runnung");
    }
}

class Cat extends Animal{
    @Override
    public void Bye(){
        System.out.println("Bye Cat");
    }
}

public class test {

    public static void main (String[] args){
        Dog dog = new Dog();
        Cat cat = new Cat();

        dog.Bye();
        dog.Hello();
        dog.Run();

        cat.Bye();
        cat.Hello();
    }
}
```

Result

```
Bye Dog
Hello World
Dog is Runnung
Bye Cat
Hello World
```

## Interface

Java에서 인터페이스(Interface)는 **미완성된 설계도**라고 표현한다.

하나의 설계도로 여러가지 나사 제품을 만든다고 생각하면 됩니다. 즉, 구현하는 모든 클래스에 대해서 특정한 메서드를 강제할 수 있다. 이 의미는 클래스를 추가 확장할 수 없이 Interface에 구현된 메소드만 사용할 수 있다는 뜻입니다.

선언은 다음과 같이 합니다.  

```
Interface Car
```

Interface에는 몇가지 규칙이 있습니다.

- 모든 메서드는 public abstract 이어야 하며, 이를 생략할 수 있다.
- 모든 멤버변수는 public static final 이어야 하며, 이를 생략할 수 있다.
- 반드시 인터페이스에 명시되어 있는 추상메서드들을 모두 구현해야 한다.

Interface를 사용하기 위해선 `implements`를 사용합니다.

또한, Java에서 오직 인터페이스에서만 다중 상속이 가능합니다. 다음과 같이 사용할 수 있습니다. 

```
class A implements InterfaceA, InterfaceB
``` 

> Example

```
package Test;

interface Car{
    public void Run();
    public void Hello();
}

class Benz implements Car{

    @Override
    public void Run(){
        System.out.println("Benz is Run");
    }
    
    @Override
    public void Hello() {
    	System.out.println("Hello Benz");
    }

}

public class test {

    public static void main (String[] args){
        Benz car = new Benz();
        car.Run();
        car.Hello();
    }
}
```

Result

```
Benz is Run
Hello Benz
```



