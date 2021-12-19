---
title:  "디자인 패턴 톺아보기 - Interpreter Pattern"
excerpt: "디자인 패턴 톺아보기 - Interpreter Pattern"
categories:
  - Design Pattern
tags:
  - Design Pattern
  - Interpreter Pattern"
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

## 1. 인터프리터 패턴(Interpreter Pattern) 이란?

GOF 에서 말하는 인터프리터 패턴의 목적은 아래와 같습니다.

> Given a language, define a representation for its grammar along with an inter­preter that uses the representation to interpret sentences in the language.

> 어떤 언어에 대해, 그 언어의 문법에 대한 표현을 정의하면서 그것(표현)을 사용하여 해당 언어로 기술된 문장을 해석하는 해석자를 함께 정의합니다.

### 1.1. 구조

> Sample / Sequence Diagram

![image](/assets/images/design_pattern/interpreter_pattern.png)

* AbstractExpression
  * 추상 구문 트리에 속한 모든 노드에 해당하는 클래스들이 공통으로 가져야 할 interpret() 연산을 추상 연산으로 정의합니다.
* TerminalExpression
  * 문법에 정의한 터미널 기호와 관련된 해석 방법을 구현합니다. 문장을 구성하는 모든 터미널 기호에 대해서 해당 클래스를 만들어야 합니다.
* NonterminalExpression
  * 문법의 오른편에 나타나는 모든 기호에 대해서 클래스를 정의해야 합니다.
* Context
  * 번역기에 대한 포괄적인 정보를 포함합니다.
* Client
  * 언어로 정의한 특정 문장을 나타내는 추상 구문 트리입니다. 이 추상 구문 트리는 NonterminalExpression과 TerminalExpression 클래스의 인스턴스로 구성됩니다. 이 인스턴스의 Interpret() 연산을 호출합니다.

### 1.2. 사용 방법

* 사용자는 NonterminalExpression과 TerminalExpression 인스턴스들로 해당 문장에 대한 추상 구문 트리를 만듭니다. 그리고 사용자는 Interpret() 연산을 호출하는데, 이때 해석이 필요한 문맥 정보를 초기화합니다.
* 각 NonterminalExpression 노드는 또 다른 서브 표현식에 대한 Interpret()를 이용하여 자신의 Interpret() 연산을 정의합니다. 이 연산은 재귀적으로 Interpret() 연산을 이용하여 기본적 처리를 담당합니다.
* 각 노드에 정의한 Interpret() 연산은 해석자의 상태를 저장하거나 그것을 알기 위해서 문맥 정보를 이용합니다.

### 1.3. 장/단점

* Advantages (+)
    * Makes changing the grammar easy.
    * Makes adding new kinds of interpret operations easier.
* Disadvantages (–)
    * Makes representing complex grammars hard.

### 1.4. 고려사항

* Consider the left design (problem):
    * Hard-wired expression.
* Consider the right design (solution):
    * Separated expression.

## 2. 인터프리터 패턴(Interpreter Pattern) 사용예시

인터프리터 패턴은 다음 경우에 사용합니다.

* 해석이 필요한 언어가 존재하거나 추상 구문 트리로서 그 언어의 문장을 표현하고자 한다면 해석자 패턴을 사용할 때이다.

### 2.1. GOF 패턴

#### 2.1.1. Target

결과는 아래와 같습니다.

```
```

> 참고 자료

* [Interpreter Pattern](https://en.wikipedia.org/wiki/Interpreter_pattern)
* [The GoF Design Patterns Reference.](http://w3sdesign.com/index0100.php)
