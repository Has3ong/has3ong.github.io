---
title : Jenkins The Foundations
tags :
- Jenkins
- DevOps
---

*이 포스트는 [Jenkins 2: Up and Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/jenkins2_upandrunning.pdf)를 바탕으로 작성하였습니다.*

## Syntax: Scripted Pipelines Versus Declarative Pipelines

스크립트 방식의 문법은 Jenkins 에서 pipelines-as-code 가 수행되는 초기 방식입니다. 이는 명령적은 스타일의 로직에 기반하고 파이프라인 스크립트의 흐름을 따릅니다. 또한 그루비 언어와 명령어에 밀접하게 연관돼 있고, 특히 에러 확인과 예외 처리 부분에 의존성이 강합니다.

서술적 문법은 Jenkins 의 새로운 선택지입니다. 서술적 스타일로 작성된 파이프라인은 주요 영역에서 필요한 상태와 결과를 나타내는 구역이 잘 나뉘어져 있고 로직 자체에 대한 집중은 적습니다.

다음 예시는 스크립트 방식의 문법으로 작성된 파이프라인과 서술적 방식으로 작성된 파이프라인의 예시입니다.

```groovy
// Scripted Pipeline
node('worker_node1') {
    stage('Source') { // Get code
        // get code from our Git repository
        git 'git@diyvb2:/home/git/repositories/workshop.git'
    }
    stage('Compile') { // Compile and do unit testing
       // run Gradle to execute compile and unit testing
       sh "gradle clean compileJava test"
    }
}

// Declarative Pipeline
pipeline {
    agent {label 'worker_node1'}
    stages {
        stage('Source') { // Get code
            steps {
                // get code from our Git repository
                git 'git@diyvb2:/home/git/repositories/workshop.git'
            }
        }
        stage('Compile') { // Compile and do unit testing
            steps {
                // run Gradle to execute compile and unit testing
                sh "gradle clean compileJava test"
            }
        }
    }
}
```

스크립트 방식의 파이프라인은 프로그램의 흐름과 로직을 실행하기 위해 일반적인 명령형 언어로 작성된 프로그램이나 스크립트고, 서술적 파이프라인은 전통적인 Jenkins 웹 폼에서 주요 정보를 특정 목적과 행동을 하는 미리 정의된 섹션에 입력하는 것으로 생각하면 됩니다.

전통적인 웹 폼처럼 서술적 파이프라인을 실행시키면 각 섹션의 타입이 어떤 데이터를 가지고 어던 일을 실행할지 결정하게 됩니다.

### Choosing Between Scripted and Declarative Syntax

스크립트 방식 파이프라인의 장점은 다음과 같습니다.

* 대체로 더 적은 섹션과 설명이 필요하다.
* 더 많은 절차형 코드를 사용 가능하다.
* 프로그램을 작성하는 것과 유사하다.
* 전통적인 pipeline-as-acode 모델로서 더 익숙하고 하위 호환성이 좋다.
* 필요시 맞춤화된 동작을 수행하기 쉽다.
* 더 복잡한 파이프라인을 설계할 수 있다.

스크립트 방식 파이프 라인의 단점은 다음과 같습니다.

* 더 많은 프로그래밍이 필요하다.
* 문법 검사가 그루비 환경에 국한된다.
* 전통적인 Jenkins 모델과 연관이 적다.
* 서술적 파이프라인에 같은 내용이 구현이 가능하다 가정하면 상대적으로 더 복잡하다.

다음으로 서술적 파이프 라인의 장점은 다음과 같습니다.

* 더 구조하돼 전통적 Jenkins 웹 폼과 유사하다.
* 필요한 것을 선언하는 것이 유연해 대체로 가독성이 좋다.
* 블루 오션 화면의 인터페이스를 이용해 생성 가능하다.
* 알림과 같이 기존 Jenkins 개념에 대응할 수 있는 섹션이 존재한다.
* 문법 확인 및 에러 확인이 쉽다.
* 파이프라인 사이의 일관성이 높다.

서술적 파이프라인의 단점은 다음과 같습니다.

* 반복되는 로직에 대한 지원이 적다.
* 아직 발전중이다.
* 유연성이 적은 구조다.
* 현재 복잡한 파이프라인이나 워크플로우에 잘 적용되지 않는다.

서술적 방식은 새로운 파이프라인 사용자가 배우고 유지하기에 더 쉽고, 기존 Jenkins 처럼 바로 사용 가능한 기능을 원하는 경우에 유용합니다. 반대급부로 제공되는 구조에서 벗어나는 일을 할 수 있는 유연성이 적습니다.

스크립트 방식은 더 유연해 숙련된 사용자가 이 구조를 이용해 많은 일을 할 수 있습니다. 하지만 결국 두 방식 모두 대부분의 경우를 처리할 수 있습니다.

Jenkins 가 파이프라인을 수행할 수 있는 시스템에 대해 알아보겠습니다.

## Systems: Masters, Nodes, Agents, and Executors

스크립트 방식 혹은 서술적 파이프라인을 사용하는 것과는 상관없이 모든 Jenkins 파이프라인은 코드를 실행하기 위해 하나 이상의 시스템이 필요합니다. 여기서 시스템이란 용어는 우리가 다루는 다양한 용어에 대한 총칭입니다. 하지만 시스템이나 머신에 설치된 Jenkins 에 여러 인스턴스가 존재할 수 있습니다.

전통적 Jenkins 에서는 마스터와 슬레이브 두 종류의 구분만 있었습니다.

### Master

Jenkins 마스터는 Jenkins 인스턴스 제어에 중심이 됩니다. 마스터에는 Jenkins 의 모든 설정과 옵션, 잡에 대한 권한이 있습니다. 다른 시스템에 정의되지 않았다면 잡을 실행하는 기본 장소가 됩니다.

하지만 마스터는 무거운 작업을 수행하는 데는 적합하지 않습니다. 이 작업이 필요한 잡은 마스터가 아닌 다른 시스템에서 수행해야 합니다.

그 이유는 마스터에 수행되는 잡은 모든 데이터, 환경 설정과 같은 접근 권한이 있어 보안에 심각한 위협이 될 수 있기 때문입니다. 또 다른 이유는 마스터가 끊김 없이 작업을 관리해야 하므로 과부하로 인해 중돤되는 일이 발생하면 안되기 때문입니다.

### Node

노드는 Jenkins 에 사용되는 일반적인 용어로, Jenkins 잡을 실행할 수 있는 시스템을 의미합니다. 여기에는 마스터 혹은 에이전트가 포함되며, 때로는 이 둘을 지칭하는 용어로 사용되기도 합니다. 도커와 같은 컨테이너를 의미할 때도 있습니다.

마스터 노드는 Jenkins 를 설치하면 무조건 생기지만, 위 기술한 이유로 잡을 실행하는 것은 적합하지 않습니다.

### Agent

에이전트는 이전 Jenkins 의 슬레이브와 같습니다. Jenkins 에서 이는 마스터가 아닌 시스템을 의미합니다. 에이전트는 마스터에 의해 관리되고 필요에 의해 할당되어 각 잡의 수행을 담당합니다. 에이전트를 OS 에 따라 다르게 빌드를 수행할 수 있게 할당하거나, 테스트를 위해 여러 개의 에이전트를 병렬로 실행시킬 수 있습니다.

시스템 부하와 보안 위험을 줄이기 위해 접근 권한이 제한된 경량화된 Jenkins 클라이언트를 설치해 잡을 처리합니다.

에이전트는 노드에서 실행합니다. 스크립트 방식의 파이프라인에서 노드는 에이전트가 있는 시스템을 지칭합니다. 서술적 파이프라인에서는 특정 에이전트를 명시해 노드를 할당합니다.

#### Directives Versus Steps

노드는 스크립트 방식의 파이프라인과 연관이 있습니다. 기술적으로 이는 **스텝(Step)** 이 되는데 파이프 라인에서 수행돼야 할 행동을 유발시키는 역할을 합니다. 이는 엑시큐터를 노드에 할당하고 정의된 영역 안에 있는 코드를 실행합니다. 다음은 노드 단계에 짧은 예시 입니다.

```groovy
// Scripted Pipeline
node('worker') {
    stage('Source') { // Get code
        // Get code from our Git repository
```

반면 에이전트는 서술적 파이프라인의 명령어입니다. `none` 에이전트를 사용하는 특별한 경우를 제외하고 노드를 할당하는 역할을 합니다. 다음은 에이전트의 간단한 선언 예시입니다.

```groovy
// Declarative Pipeline
pipeline {
    agent {label:'worker'}
    stages {
        stage('Source') { // Get code
```

### Executor

위 다룬 모든 것과 연관된 것은 **엑시큐터(Executor)** 입니다.

엑시큐터는 노드나 에이전트에서 잡을 실행시키는 장소입니다. 노드는 엑시큐터를 여러개 가지고 있을 수 있고, 하나도 가지고있지 않을 수 있습니다. 엑시큐터의 개수에 따라 해당 노드에서 동시에 실행될 수 있는 잡의 개수가 정의됩니다. 마스터가 잡을 특정 노드에 할당했을 때 해당 잡이 즉시 수행되려면 사용 가능한 엑시큐터가 있어야 합니다. 그렇지 않으면 엑시큐터가 사용 가능해질 때까지 기다리게 됩니다.

`Example 1` 은 지금까지 다른 시스템의 역할을 비교합니다.

> Example 1 - Types of systems involved in doing work in Jenkins

![image](https://user-images.githubusercontent.com/44635266/79679281-91452600-823f-11ea-92d8-c2a63ce1ba99.png)

### Creating Nodes

전통적 Jenkins 에 잡은 마스터 혹은 슬레이브에서 실행됩니다. 앞에서 다룬 것처럼 Jenkins 에서는 마스터와 슬레이브를 모두 노드로 지칭합니다. 이는 Jenkins 에서 슬레이브를 설정하는 것처럼 노드를 설정할 수 있습니다.

Jenkins 에 로그인 후 관리 페이지로 이동해 노드 관리를 클릭하겠습니다.

> Example 2 - The Manage Nodes option on the Manage Jenkins page

![image](https://user-images.githubusercontent.com/44635266/79679288-9c985180-823f-11ea-8008-891fa39488a1.png)

노드 관리 화면에서 새로운 노드를 선택하고 엑시큐터의 숫자를 포함해 폼에 내용을 작성할 수 있습니다.(`Example 3`, `Example 4`)

> Example 3 - Node basics: choosing the node’s name and type

![image](https://user-images.githubusercontent.com/44635266/79679289-a326c900-823f-11ea-8536-806eae32326c.png)

> Example 4 - Entering parameters to define how the node should be used      

![image](https://user-images.githubusercontent.com/44635266/79679291-a91caa00-823f-11ea-9cfc-e627f9e11a1a.png)

레이블 영역에서는 여러 개의 레이블을 설정할 수 있습니다. 따옴표로 묶어서 스페이스를 레이블에 포함시킬 수 있습니다.

#### A Quick Note About Node Labels

레이블 시스템과 사용자 모두를 위해 사용될 수 있습니다. 예를 들어, 레이블은 다음과 같은 목적으로 사용됩니다.

* 고유 레이블을 통한 노드의 구분
* 같은 레이블을 지정해 노드를 그룹화하는 용도
* 작업에 필요한 노드의 특징을 알려주는 용도로 사용

마지막 방식의 예시가 권장되는 레이블 사용법입니다. 레이블은 파이프라인에서 코드를 실행하는 장소를 지정할 때 참조됩니다.

## Structure: Working with the Jenkins DSL

DSL 은 Domain-Specific Language 의 약자로 특정한 상황을 위한 프로그래밍 언어입니다. 여기서 상황이란 Jenkins 파이프라인 생성을 의미합니다.

Jenkins DSL 은 그루비 언어를 이용해 작성됐습니다. 그루비 가 선택된 이유는 기능이 다른 언어보다 DSL 을 생성하기 쉽게 만들기 때문입니다. 반대로 문법에 심하게 의존하는 결과가 나오기도 합니다.

다음은 Jenkins DSL 로 표현된 간단한 파이프라인입니다.

```groovy
node ('worker1') {

     stage('Source') { // for display purposes

      // Get some code from our Git repository

      git 'https://github.com/brentlaster/gradle-greetings.git'

      }
}
```

### node

먼저 노드 키워드가 있습니다. 노드는 마스터나 에이전트를 위한 새로운 용어입니다. 노드는 Manage Jenkins > Manages Nodes 인터페이스를 통해 마치 슬레이브처럼 설정됩니다. 각 노드에는 Jenkins 에이전트가 설치돼 잡을 실행합니다.

이 코드 라인은 Jenkins 에게 어떤 노드에서 해당 파이프라인을 실행해야 하는지 알려줍니다. 이는 코드를 노드에서 실행되는 특정 Jenkins 에이전트 프로그램에 묶는 역할을 합니다. 여기서 특정한 노드를 찾는 방법은 레이블에 해당하는 명칭을 변수로 넘겨 지정합니다.

이는 이미 정의된 노드나 시스템이어야 하고 Jenkins 가 이를 알고 있어야 합니다. 레이블을 생략할 수 있는데 이렇게 되면 이 코드는 다음과 같이 처리됩니다.

* master 가 실행을 위한 기본 노드로 설정됐을 경우 이 잡을 master 에서 수행합니다.
* 그 외의 경우 비어 있는 레이블은 Jenkins 가 여러 노드 중 가용한 첫 번째 엑시큐터를 이용해 잡을 수행합니다.

#### Leveraging Multiple Labels on a Node

노드를 설정할 때 레이블 사이에 스페이스를 사용하면 여러 개의 레이블을 설정할 수 있습니다. or 를 위해서는 `||`, and 를 위해서는 `&&` 를 사용하면 됩니다.

```groovy
node("linux && east"){}
```

`{}` 기호는 그루비 **클로저(Closure)** 로 파이프라인의 현재 노드에 연관되어 있는 코드 블록의 시작과 끝을 나타냅니다. 클로저는 프로그램 간 전달할 수 있는 엔티티 역할도 하며 마지막 문장이 리턴값이 됩니다. 파이프라인에서 이 부분이 실행되면, 노드에 연결되어 워크스페이스를 생성하고 엑시큐터가 사용가능할 때 코드를 수행할 수 있게 스케줄을 정의합니다.

다음 예시처럼 노드는 매핑과 연동되어 코드 블록을 어디에서 실행할 지 결정할 수 있습니다.

```groovy
parallel (
            win: { node ('win64'){
             ...
             }},
            linux: { node ('ubuntu') {
             ...
             }},
          )
```

### stage

노드의 정의 부분 안에 존재하는 `stage` 클로저는 각각의 설정, DSL 명령어, 로직을 그룹으로 묶을 수 있게 해줍니다. 스테이지는 이름이 꼭 필요하며, 이를 통해 스테이지가 수행하는 일을 요약하게 됩니다. 현재 파이프 라인을 실행할 때 스테이지의 이름이 실제로 실행하는 동작은 없지만 로그에 이름이 출력되어 어떤 스테이지를 실행하는지 알 수 있습니다.

하나의 스테이지에 파이프라인 로직을 얼마나 포함하게 할지는 개발자에게 달려있습니다. 하지만 권장되는 방식은 각각의 스테이지를 전통적인 파이프라인 하나가 담당하는 크기로 나누는것입니다. 예를 들어 컴파일 하는것, 통합 테스트를 실행하는것이 될 수 있습니다.

### steps

스테이지 안에는 실제 Jenkins DSL 명령어가 들어갑니다. Jenkins 에서는 이를 스탭이라 지칭합니다. 스텝은 DSL 에 가장 최소 기능 단위입니다. 그루비 명령어는 아니지만 사용할 수 있습니다. 아래 예시에서는 소스 코드를 내려받기 위해 아래와 같은 스텝을 사용합니다.

```groovy
git 'https://github.com/brentlaster/gradle-greetings.git'
```

깃 명령어를 소스 코드를 가져올 장소의 매개변수와 함께 호출합니다.

스크립트에서 DSL 을 사용하다 보면 축약된 문법과 전체 문법을 모두 볼 수 있습니다.

#### UNDERSTANDING STEP SYNTAX

Jenkins DSL 에서 스탭은 맵 형태의 매개변수를 사용합니다.

```groovy
git branch: 'test', 
    url: 'https://github.com/brentlaster/gradle-greetings.git'
```

`branch`, `url` 매개변수가 두 개가 있는것을 볼 수 있습니다. 위는 실제 그루비에 사용되는 매핑 문법의 축약된 버전입니다. `[named parameter: value, named parameter: value]` 형태가 `[key: value, key: value]` 문법에 대응되는 표현입니다. 여기서 매개 변수의 이름이 맵의 키 역할을 합니다.

그루비에서는 매개 변수를 사용할 때 괄호를 생략하는 것을 허용합니다. 따라서 이러한 생략을 제외하고 더 긴 버전은 다음과 같습니다.

```groovy
git([branch: 'test', 
   url: 'http://github.com/brentlaster/gradle-greetings.git'])
```

또 다른 트릭은 단 하나의 매개변수만 존재할 때 키를 생략할 수 있습니다. 이를 통해 축약된 버전의 스텝이 됩니다.

```groovy
git 'https://github.com/brentlaster/gradle-greetings.git'
```

여기서 `url` 이 제공돼야 하는 유일한 매개변수입니다. 매개 변수가 필수가 아니라면 기본 매개 변수는 `script` 객체입니다. 위 예시에서 사용하는 `bat` 스텝은 윈도우에서 **배치(Batch)** 나 **쉘(Shell)** 작업을 위해 사용합니다. 전체 문법은 다음과 같습니다.

```groovy
bat([script: 'echo hi'])
```

축약하면 다음과 같습니다.

```groovy
bat 'echo hi'
```

`Example 5` 는 노드와 스테이지, 스텝의 관계를 그림으료 표현한 것입니다.

> Example 5 - Relationship between nodes, stages, and steps

![image](https://user-images.githubusercontent.com/44635266/79679297-b043b800-823f-11ea-8a13-da950a59aea2.png)

## Supporting Environment: Developing a Pipeline Script

Jenkins 의 버전에서 사용자는 특정 타입의 아이템을 생성함으로써 프로젝트를 만들게 됩니다. Jenkins 에서는 통합된 프로젝트 타입인 파이프라인 타입을 지원합니다. 파이프라인 타입의 프로젝트는 파이프라인을 정의하기 위한 코드 개발환경을 만듭니다. 이 타입의 프로젝트를 만들 때 어떻게 설정하고 환경을 사용해 파이프라인을 생성하고 수정, 실행, 모니터링하는지 알아두면 도움이 됩니다.

Jenkins 의 파이프라인 스크립트는 파이프라인 잡 타입이나. Jenkinsfile 을 통해 생성됩니다.

Jenkinsfile 을 통해 생성된 경우 소스 코드와 함께 저장됩니다. 후에 DSL 스크립트 생성 방법을 알아볼 때 파이프라인 잡에 스크립트를 작성하는 방식을 사용합니다. Jenkinsfile 은 에디터에서 작성하거나 기존 파이프라인 잡에서 복사하는 방식으로 생성할 수 있습니다.

### Starting a Pipeline Project

생성할 프로젝트의 타입으로 파이프라인을 선택하면 익숙한 웹 기반 폼이 나타납니다. 각각의 주요 영역은 탭으로 구분되어 있습니다. 먼저 General 탭에서 시작하겠습니다.

> Example 6 - The General tab of a new Pipeline project

![image](https://user-images.githubusercontent.com/44635266/79679466-34e30600-8241-11ea-9b00-c7c1c0f67a17.png)

파이프라인 프로젝트에서 주목할 부분은 Pipeline 탭입니다. 여기서 파이프라인 스크립트를 입력할 수 있는 화면이 나타납니다. `Example 7` 은 간단한 파이프라인 스크립트를 작성한 예시입니다.

> Example 7 - Pipeline tab with a simple script example

![image](https://user-images.githubusercontent.com/44635266/79679472-3e6c6e00-8241-11ea-9dbd-119de0a4946d.png)

이 파이프라인 코드는 Jenkins 내장 편집기를 이용해 작성했습니다.

### The Editor

편집기를 사용핼 따 알아두면 좋은 기능이 있습니다.

#### Syntax checking

문법 편집기는 그루비 문법 검사 및 참조 검사를 수행합니다. `Example 8` 처럼 문자게 있는 라인에 붉은 X 표시를 나타냅니다.

> Example 8 - Error indications in the pipeline script window

![image](https://user-images.githubusercontent.com/44635266/80592867-1e1b8b00-8a5b-11ea-84f3-1dc4cfebb859.png)

하지만 이렇게 표시된 모든 에러가 실제 에러가 아닐 수 있습니다. 의존성이나 방금 생성된 임포트가 아직 해결되지 않았을 수도 있습니다.

#### Extended error information

X 표시는 문제가 있는 라인을 알려주고 마우스를 이 표시 위에 올려 놓으면 더 자세한 정보를 볼 수 있습니다. 에러 내용의 전체가 팝업으로 나타납니다.

> Example 9 - Hovering displays the full text of the error message

![image](https://user-images.githubusercontent.com/44635266/80592883-24aa0280-8a5b-11ea-8185-412100742041.png)

#### Autocomplete

편집기는 괄호 등에 자동 완성을 지원합니다. 즉 사용자가 괄호의 시작을 `{` 을 작성하면 편집기가 자동으로 공백과 함께 괄호의 끝 `}` 을 입력해줍니다. 사용자가 괄호의 끝을 입력하는 습관이 있는 경우 괄호의 끝이 두 개가 되어 컴파일 에러가 발생하기도 합니다.

> Example 10 - Autocompletion of brackets

![image](https://user-images.githubusercontent.com/44635266/80592903-2bd11080-8a5b-11ea-9207-53e8dbbbe814.png)

편집기 외에도 문법을 확인을 도와주는 도구가 있습니다. 이는 **스니펫 생성기(Sinpper Generator)** 라 불립니다.

### Working with the Snippet Generator

기존 폼 기반의 웹 인터페이스에서 잡과 파이프라인을 설정하는 방식에서 DSL 스크립트를 사용하는 방식으로 변경하는 것에는 많은 장점이 있습니다. 하지만 원하는 작업을 하기 위해 적합한 스텝과 문법을 아는 과정은 이에 속하지 않습니다. 위에서 다른 `git` 스텝 같은 경우는 문법과 매개 변수가 직관적이지만 그 외의 경우는 그렇지 않습니다. 스텝을 위한 올바른 문법을 위해 Jenkins 2 는 스니펫 생성기라 불리는 파이프라인 문법 지원 도구를 포함합니다.

스닛 생성기는 사용 가능한 DSL 스텝을 살펴보며 원하는 문법과 내용을 고를 수 있게 합니다. 또한 내용에 대한 온라인 도움말도 제공합니다. 하지만 가장 유용한 기능은 값을 입력할 수 있는 웹 폼을 제공하는 것입니다. 웹 폼을 이용해 버튼을 눌러 원하는 스텝을 호출하는 그루비 DSL 코드를 생성할 수 있습니다. DSL 생성한 후에는 그냥 복사해서 사용하면 됩니다. 이런 기능은 특정 스텝을 사용하는 데 드는 수고를 크게 줄여줍니다.

스니펫 생성기가 어떻게 도착하는지 예시를 통해 알아보겠습니다. 깃 코드를 가져오는 스텝이 필요한 상황을 가정해보겠습니다. `Example 11` 은 시작점을 보여줍니다.

> Example 11 - Code block for source pull

![image](https://user-images.githubusercontent.com/44635266/80593395-1d372900-8a5c-11ea-87d2-38484bd4a98b.png)

깃을 사용할 것을 알지만 어떤 문법이 필요한지는 모릅니다. 그래서 `Example 12` 에서와 같이 Pipeline 탭 하단의 Pipeline Syntax 링크를 클릭합니다. 그러면 스니펫 생성기 화면으로 이동합니다.

> Example 12 - The Snippet Generator

![image](https://user-images.githubusercontent.com/44635266/80593410-245e3700-8a5c-11ea-830b-05de85d22d05.png)

여기서 `Example 13` 처럼 Steps 드롭다운 옵션에서 `git` 을 선택할 수 있습니다. 이제 스텝에 넘겨 줄 수 있는 매개변수가 나타납니다. 여기서 기본값을 선택하거나 원하는 값을 입력합니다. 마지막으로 Generate Pipeline Script 버튼을 클릭해 파이프라인 스크립트를 생성합니다. 그림에서 보이는 것처럼 간단한 `git` 스텝이 나타납니다.

> Example 13 - Generating pipeline code for the git step with defaults

![image](https://user-images.githubusercontent.com/44635266/80593425-2d4f0880-8a5c-11ea-87ae-0c17e3e1b6a6.png)

이를 스테이지 클로저에 복사하면 다음과 같은 결과가 됩니다.

```groovy
stage('Source') {
// Get some code from our Git repository
    git 'https://github.com/brentlaster/gradle-greetings.git'
}
```

기본값을 덮어쓰기로 선택하면 입력한 값이 스탭에 반영됩니다. 체크 박스 해제도 잊지 말아야 합니다.

> Example 14 - Overriding default values for the git step

![image](https://user-images.githubusercontent.com/44635266/80593433-33dd8000-8a5c-11ea-9121-a1891fad1938.png)

여러 매개변수가 사용될 경우 매개 변수의 이름이 필요합니다. 이전 예시처럼 이 코드는 스크립트에 바로 복사해 사용할 수 있습니다.

### Running a Pipeline

코드를 입력했으니 파이프라인 실행 준비가 끝났습니다. 파이프라인은 컴파일, 통합 테스트, 분석 등 여러 단계로 구성되어 있습니다. 과거 버전의 Jenkins 에서 각 분야를 프리스타일 잡으로 분리한 후 선후 관계를 지정하여 가장 먼저 수행되는 잡을 실행하는 것이 일반적인 방법입니다.

시간이 흐르면서 스테이지를 나타내는 잡의 흐름을 시각화하는 플러그인이 생겨났습니다. 이 중에서 가장 일반적인 것은 Build Pipeline 플러그인입니다. 이 플러그인을 통해 파이프라인에 있는 잡을 연결된 박스로 표현하는 화면을 생성할 수 있습니다. 각 박스는 현재 상태에 따라 다른 색상으로 표현되는데 파란색은 실행되지 않은 잡, 노란색은 진행 중인 잡, 초록색은 끝난 잡, 붉은색은 실패한 잡입니다. `Example 15` 는 이 예시입니다.

> Example 15 - The original Build Pipeline plug-in

![image](https://user-images.githubusercontent.com/44635266/80593791-be25e400-8a5c-11ea-9296-4d8cce59a773.png)

Jenkins 2 에는 전체 파이프라인을 작성하는 프로젝트 타입이 있습니다. 이제 파이프라인을 이전 깃 예시에서 처럼 `stage{}` 블록을 통해 표현할 수 있습니다. 파이프라인에 새로운 스테이지를 추가해보겠습니다. 너무 복잡하지 않게 빌드 스텝을 위한 영역만 추가하겠습니다.

```groovy
node ('worker1') {
     stage('Source') {
      // Get some code from our Git repository
         git 'https://github.com/brentlaster/gradle-greetings.git'
     }
     stage('Build') {
      // TO-DO: Execute the gradle build associated with this project
         sh 'echo gradle build will go here'
     }
}
```

`Example 16` 은 파이프라인 탭에 나타난 스크립트입니다.

> Example 16 - Script in the Pipeline tab

![image](https://user-images.githubusercontent.com/44635266/80593808-c54cf200-8a5c-11ea-9bb8-9bb6d8d939a1.png)

이 파이프라인을 저장하면 *No data available. This Pipeline has not yet run* 이라고 아직 이 파이프라인을 실행하지 않았다는 UI 가 표시됩니다.(`Example 17`) 여기서 헤딩이 Stage View 에 주목하면 됩니다. Jenkins 2 에는 이것이 파이프라인 기본 결과 화면입니다.

> Example 17 - Before the first run

![image](https://user-images.githubusercontent.com/44635266/80593821-cbdb6980-8a5c-11ea-9eb3-24c57e328f23.png)

왼쪽 메뉴에서 Build Now 를 클릭하면 Jenkins 는 파이프라인을 빌드합니다. 이 예시의 경우 모든 것이 성공적으로 끝날 것입니다. `Example 18` 에 스테이지 뷰 결과 화면에 잡 실행이 타일 형태로 뜨는것을 보면됩니다. 초록색은 성공을 의미합니다. 각 타일을 해석하는 방법을 좀 더 알아보겠습니다.

> Example 18 - Successful first run

![image](https://user-images.githubusercontent.com/44635266/80593832-d3027780-8a5c-11ea-84b3-15d3269ab15d.png)

각 파이프라인 빌드 스테이지마다 젠킨스는 새로운 타일을 생성합니다. 각각의 행은 프로젝트의 빌드를, 열은 파이프라인의 스테이지를 의미합니다. 즉 하나의 타일은 특정 스테이지의 실행을 의미합니다. 여기서 텍스트는 `stage` 스텝의 `name` 매개 변수가 화면에 나타나는 것입니다. 스테이지 실행에 걸린 시간은 타일 안에 표시됩니다.

타일의 색상도 매우 중요합니다. 일반적인 의미는 아래 표에 정의했습니다.

|Color|Meaning|
|:--|:--|
|Blue Stripes|Processing in progress|
|White|Stage has not been run yet|
|Rose Stripes|Stage Failed|
|Green|Stage Succeeded|
|Rose|Stage succeeded but some ohter stage failed downsteram|

> 타일이 초록색이더라도 하위 스테이지가 실패하면 장미색으로 바뀔 수 있습니다.

#### Viewing Logs

전통적인 Jenkins 와 동일하게 로그를 확인하려면 Console Output 링크를 누르거나 빌드 결과화면에서 공 모양을 누르면 됩니다.

스테이지 뷰에서는 특정 빌드의 특정 스테이지에 해당하는 로그를 볼 수 있는 기능이 제공됩니다. 간단히 원하는 빌드와 스테이지 위에 마우스를 올려 놓은 후 나타나는 박스의 버튼을 누르면 로그로 갈 수 있는 팝업이 나타납니다. `Example 19` 와 `Example 20` 을 참고하면 됩니다.

> Example 19 - Hover over a tile to get the pop-up with the Logs button

![image](https://user-images.githubusercontent.com/44635266/80593847-d8f85880-8a5c-11ea-979f-f636c9a8f5bf.png)

> Example 20 - Click on the Logs button to get the pop-up with the actual logs for the stage

![image](https://user-images.githubusercontent.com/44635266/80593859-e1e92a00-8a5c-11ea-8993-3860a934d4de.png)

#### Stage View With Errors

에러가 발생한 스테이지 뷰를 보겠습니다. 코드가 실행되는 환경이 리눅스라 가정하겠습니다. 파이프라인에는 아주 작은 차이만 생깁니다. 아래는 리눅스 명령어입니다.

```groovy
sh 'echo gradle build will go here'
```

윈도우는 다음과 같이 바뀝니다.

```groovy
bat  'echo gradle build will go here' 
```

`bat` 명령어를 리눅스 시스템에 복사했다고 가정하고, 빌드를 시작하면 `Example 21` 과 유사한 스테이지 뷰가 나타납니다.

> Example 21 - Stage View with errors

![image](https://user-images.githubusercontent.com/44635266/80593878-eca3bf00-8a5c-11ea-9af3-72b478da7d44.png)

두 번재 실행이 매트릭스의 새로운 행을 추가한 것을 볼 수 있습니다. 위에 위치하는 행이 최신 실행 결과입니다. 상단의 Build 타일의 줄므늬 색상이 스테이지가 실패했다는 것을 알려줍니다. Source 스테이지의 밝은 장미색은 해당 스테이지는 성공했지만 그 하위 스테이지가 실패했다는 의미입니다.

에러를 확인하려면 위에서 기술한 단계를 따라가면 됩니다. 실패한 타일 위에 마우스를 올려 놓으면 로그로 향하는 링크가 팝업으로 나타납니다. 여기서 스테이지가 실패한 이유를 알 수 있습니다. 팝업 상단에 *Failed with the following error(s) Windows Batch Script Batch scripts can only be run on Windows nodes* 라는 내용이 나타납니다. `Example 22` 가 이를 보여줍니다.

> Example 22 - Viewing the failures in one stage

![image](https://user-images.githubusercontent.com/44635266/80593922-004f2580-8a5d-11ea-9348-e946e5f843ad.png)

Jenkins 는 팝업에 실패한 이유를 나타냅니다. Logs 버튼을 클릭해 로그를 확인할 수 있지만, 이 경우 더 많은 정보를 얻을 수 없습니다. 첫 번째 실행 문장이 에러를 발생했기 때문에 추가 로그가 없습니다.

파이프라인 코드를 변경하지 않고 여러 시도를 할 수 있게 해주는 기능이 있습니다.

### Replay

파이프라인을 작성하는 것은 웹 폼을 작성하는 것보다는 Jenkins 와 더 밀접하게 연관되어 있습니다. 무언가 작업이 실패해 사용자가 코드를 변경하지 않고 간단한 변경을 적용해 다시 실행해보겠습니다. 혹은 프로토타입을 만들어 커밋하기 전에 시험해보고 싶을 수 잇습니다. Jenkins 는 이러한 경우를 위해 **리플레이(Replay)** 기능을 제공합니다. 리플레이는 실행 이후 코드를 수정할 수 있게 하여 변경사항을 적용시켜 다시 실행할 수 있게 합니다. 새로운 빌드 결과는 보존되지만, 원래 코드는 변경되지 않고 유지됩니다.

이전 실패한 예시에서 이를 알아보겠습니다. `sh` 이 올바른 스텝인것을 깨달았지만 코드를 변경하지 않고 시험해보고 싶다고 가정하겠습니다. `Example 23` 과 같이 Console Output 으로 이동해 왼쪽 메뉴에서 Replay 를 선택합니다.

> Example 23 - Location of the Replay menu item

![image](https://user-images.githubusercontent.com/44635266/80593933-07763380-8a5d-11ea-974f-f355ea0b3d81.png)

Jenkins 가 파이프라인 탭의 파이프라인 프로젝트와 유사한 편집 창을 띄워줄것입니다.(`Example 24`) 이 창에서 프로그램을 원하는 대로 변경 후 Run 을 선택해 해당 내용을 시험할 수 있습니다.

> Example 24 - Instituting a replay for a failed run

![image](https://user-images.githubusercontent.com/44635266/80593951-0f35d800-8a5d-11ea-95f5-a77dec01c520.png)

Jenkins 는 리플레이 창에서 수정된 코드를 이용해 빌드를 실행합니다. 이경우 성공한 #3 실행결과가 생성될 것입니다. `Example 25`

> Example 25 - A successful replay

![image](https://user-images.githubusercontent.com/44635266/80593962-1361f580-8a5d-11ea-8f5e-6b8dcd886274.png)

하지만 왼쪽 메뉴에서 Configure 를 눌러 Pipeline 탭의 코드를 보면 여전히 `bat` 을 사용하는 것을 확인할 수 있습니다.(`Example 26`) 리플레이 기능은 변경 시도를 허용하지만, 이 변경을 저장하려면 코드로 돌아가 수정 사항을 적용해야 합니다.

> Example 26 - The original code is unchanged

![image](https://user-images.githubusercontent.com/44635266/80593972-18bf4000-8a5d-11ea-8bc6-6cabcedffc3b.png)

