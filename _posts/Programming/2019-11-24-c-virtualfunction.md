---
title : C++ 가상함수 / 순수 가상함수 차이
tags :
- virtual
- pure virtual
- c++
---

## 가상함수

C++에서 가상 함수(virtual function)는 파생 클래스에서 재정의할 것으로 기대하는 멤버 함수를 의미합니다. 이러한 가상 함수는 자신을 호출하는 객체의 동적 타입에 따라 실제 호출할 함수가 결정됩니다.

C++에서 가상 함수는 virtual 키워드를 사용하여 선언합니다.

```cpp
virtual function(){
  ...
}
```
 
기초 클래스에서 virtual 키워드를 사용해 가상 함수를 선언하면, 파생 클래스에서 재정의된 멤버 함수도 자동으로 가상 함수가 됩니다.

## 순수 가상함수

순수 가상함수는 구현이 없는 가상함수를 말합니다.

```cpp
virtual void function() = 0;
```

구현 대신 가상함수에 NULL (0)값을 대입하면 해당 함수는 순수 가상함수가 됩니다.

이와 동시에 순수 가상함수를 포함하는 클래스는 **추상 클래스(Abstract Class)**로 지정됩니다.

> Example

```cpp
#include <iostream>
using namespace std;

class AHG {
    
public:
    int value = 0;
    void func0() {
        cout << "AHG func0, value is : " << value << endl;
    }
    // 가상함수
    virtual void func1() {
        cout << "AHG func1" << endl;
    }
    // 순수 가상함수
    virtual void func2() = 0;
};

class Child : public AHG {
    
public:
    void setValue(int temp) {
        value = temp;
    }
    void func0() {
        cout << "Child func0" << endl;
    }
    void func1() override {
        cout << "Child func1" << endl;
    }
    void func2() override {
        cout << "Child func2" << endl;
    }
};

int main(int argc, const char * argv[]) {
    // insert code here…
    Child child;
    AHG* ptr = &child;
    
    child.setValue(1);
    ptr->func0();   // AHG func0 \n 1
    ptr->func1();   // Child func1
    ptr->func2();
    
    return 0;
}
```

C++ 에서는 순수가상함수는 인터페이스를 자식에게 전달하여 재정의 즉 오버라이딩을 하기 위해 사용합니다. 즉, 재정의를 하지 않으면 오류가 발생하여 반드시 자식 클래스에서 재정의를 해야합니다.

가상함수는 함수내부 구현이 되어있는 인터페이스를 자식에게 전달합니다. 하지만 함수의 내부구현이 되어있어서 자식클래스에서는 함수를 다시 정의해도 되고 안해도 됩니다.

쉽게 말하자면 순수가상함수는 ‘너는 이 기능이 꼭 필요해 그리고 그 기능은 너가 알아서 선언해 만약 선언하지 않으면 오류가 날꺼야’ 이며 가상함수는 ‘이 기능을 물려줄건데 너가 선언을 안해도 기본적으로 작동이 되게 만들어줄게’ 입니다.

마지막으로 위 코드에서 AHG 클래스에 func0과 Child 클래스에 func0은 서로 다른 함수입니다. 우연히 이름이 같게된 함수입니다.