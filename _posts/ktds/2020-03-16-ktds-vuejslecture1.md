---
title : Vue.js Lecture 1
tags :
---

## 1. 환경 설정

* Github : https://github.com/joshua1988/learn-vue-js
* Node : 10.16.0
* Vue.js DevTools
* Chrome
* Visual Studio Code
  * vetur
  * material icon
  * night owl
  * live server
  * ESLint
  * Prettier

## 2. Vuejs 소개

Vuejs MVVM 패턴의 뷰모델(ViewModel) 레이어에 해당하는 화면(View) 단 라이브러리

![image](https://user-images.githubusercontent.com/44635266/76381762-b7062200-6399-11ea-9337-e0953b49a4c5.png)

* MVVM(Model-View-ViewModel)
* 모델과 뷰 사이에 뷰모델이 위치하는 구조
* DOM이 변경됐을 때, 뷰모델의 DOM Listeners를 거쳐서 모델로 신호가 간다.
* 모델에서 변경된 데이터를 뷰모델을 거쳐서 뷰로 보냈을 때, 화면이 reactive하게 반응이 일어난다.
* Vue.js 는 이와 같이 reactive한 프로그래밍이 가능하게 끔 뷰단에서 모든 것을 제어하는 뷰모델 라이브러리이다.

### MVVM(Model - View - ViewModel)

![image](https://user-images.githubusercontent.com/44635266/76382429-16653180-639c-11ea-864e-6ae9f52b64b5.png)

* Backend 로직과 Client 의 마크업 & 데이터 표현단을 분리하기 위한 구조로 전통적인 MVC 패턴의 방식에서 기인
* 간단하게 생각해서 화면 앞단의 회면 동작 관련 로직과 뒷단의 DB 데이터 처리 및 서버 로직을 분리, 뒷단에서 넘어온 데이터를 Model 에 담아 View 로 넘어주는 중간 지점

### DOM(Document Object Model)

HTML 내에 들어있는 요소를 구조화 객체 모델로 표현하는 양식

> HTML 예제

```html 
<html>
  <body>
    <p>Hello World</p>
    <div><img src="example.png" /></div>
  </body>
</html>  
```

> DOM 트리 구조

![image](https://user-images.githubusercontent.com/44635266/76381877-1bc17c80-639a-11ea-9091-208b8d2a7690.png)

**DOM 의 문제점**

* 일반적인 앱에서, DOM 에는 수 천개의 노드들이 존재할 수 있고 업데이트를 위해 복잡한 처리 과정이 필요
* 결과적으로 브라우저의 속도 저하

위 문제를 해결하기 위해 등장한것이 Virtual DOM

### Virtual DOM

* Virtual DOM 은 HTML DOM 의 추상화 개념
* DOM의 복사본을 메모리 내에 저장하여 사용
* DOM 트리를 모방한 가벼운 자바스크립트 객체를 통해 직접 DOM 을 핸들링 하지 않고 퍼포먼스를 향상

> HTML 예제

```html
<div id="main">
    <h1>Header</h1>
    <p>Description</p>
</div>
```

> JavaScript 를 이용한 Virtual DOM 표현

```js
Let domNode = {
  tag: 'div',
  attributes: { id: 'main' }
  children: [
      // where the h1 & the p's would go
  ]
};
```

## 3. 인스턴스

### Vue 인스턴스 만들기

모든 Vue 앱은 Vue 함수로 새 Vue 인스턴스를 만드는 것부터 시작합니다.

> 예제

```html
<body>
  <div id="app">
      {{ message }}
  </div>
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    var vm = new Vue({
      el: '#app',
      data: {
        message: 'Hello World'
      }
    });
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76387330-02283100-63aa-11ea-9833-20b66b088cf6.png)

### 인스턴스 속성 / API

```js
new Vue({
    el: '#app',
    template: '',
    data: {},
    props: [],
    methods: {},
    computed: {},
    watch: {}
});
```

* **el ( string | HTMLElement )**
  * 대상이 되는 html element 또는 css selector ( vm.$el )
* **template ( string )**
  * Vue 인스턴스의 마크업으로 사용할 문자열 템플릿
* **data ( Object | Function )**
  * 화면을 그리는데 사용하는 data 를 반환하는 함수 또는 data 객체 ( vm.$data )
  * Vue 인스턴스가 아닌 하위 컴포넌트에서 사용될 때는 반드시 함수형으로 표현해야함
* **props ( Array<string> | Object )**
  * 부모 컴포넌트로부터 전달 받은 property들의 Array 혹은 Object
* **methods ( [key: string]: Function )**
  * Vue 인스턴스에서 사용되는 메소드. this 컨텍스트를 Vue 인스턴스에 바인딩 합니다
* **computed ( [key: string]: Function | { get: Function, set: Function } )**
  * data를 미리 계산한 값들을 나타내는 함수들을 모아둔 객체입니다.
  * 계산된 속성. getter와 setter는 자동으로 this 컨텍스트를 Vue 인스턴스에 바인딩 합니다.
* **watch ( [key: string]: string | Function | Object | Array )**
  * 감시된 속성. Vue 인스턴스에 데이터가 변경되는 시점에 호출
  * watch는 data와 한쌍을 이룬다. 즉, data에 표현된 key와 watch에 표현된 key의 이름은 동일하게 선언
  * data의 value 값이 변경이 되면, watch의 key의 value에 할당된 콜백이 실행

### 인스턴스 라이프사이클

![image](https://user-images.githubusercontent.com/44635266/76387241-cbeab180-63a9-11ea-9e94-9d1d69bf0879.png)


* **beforeCreate**
  * Vue 인스턴스가 초기화 된 직후에 발생
  * 컴포넌트가 DOM에 추가되기도 전이어서 this.$el 에 접근 불가능
  * data, event, watcher 에도 접근하기 전이라 data, methods에도 접근 불가능
* **created**
  * data를 반응형으로 추적할 수 있게 되며 computed, methods, watch 등이 활성화되어 접근이 가능
  * 아직까지 DOM에는 추가되지 않은 상태
  * 컴포넌트 초기에 외부에서 받아온 값들로 data를 세팅해야 하거나 이벤트 리스너를 선언해야 한다면 이 단계에서 하는 것이 가장 적절
* **beforeMount**
  * DOM에 부착하기 직전에 호출
  * 이 단계 전에서 템플릿이 있는지 없는지 확인한 후 템플릿을 렌더링 한 상태
  * 가상 DOM이 생성되어 있으나 실제 DOM에 부착되지는 않은 상태
* **mounted**
  * 가상 DOM의 내용이 실제 DOM에 부착되고 난 이후에 실행
  * this.$el을 비롯한 data, computed, methods, watch 등 모든 요소에 접근이 가능
* **beforeUpdate**
  * 컴포넌트에서 사용되는 data의 값이 변해서, DOM에도 그 변화를 적용시켜야 할 때가 있는데, 이 때, 변화 직전에 호출
  * 값들을 추가적으로 변화시키더라도 랜더링을 추가로 호출하지는 않는다
* **updated**
  * 가상 DOM을 렌더링 하고 실제 DOM이 변경된 이후에 호출
  * 변경된 data가 DOM에도 적용된 상태
  * 변경된 값들을 DOM을 이용해 접근할 때 사용하면 적절
* **beforeDestroy**
  * 해당 인스턴스가 해체되기 직전에 호출
  * 아직 해체되기 이전이므로, 인스턴스는 완전하게 작동하기 때문에 모든 속성에 접근이 가능
  * 이벤트 리스너를 해제하는 등 인스턴스가 사라지기 전에 해야할 일들을 처리
* **destroyed**
  * 인스턴스가 해체되고 난 직후 호출
  * 해체가 끝난 이후기 때문에, 인스턴스의 속성에 접근 불가능
  * 하위 Vue 인스턴스 역시 삭제

## 4. 컴포넌트

화면의 영역을 일정한 단위로 쪼개어 재활용 가능한 형태로 관리하는 것이 컴포넌트

![image](https://user-images.githubusercontent.com/44635266/76387806-056fec80-63ab-11ea-928b-534280d29170.png)

> 예제 

```html
<body>
  <div id="app">
    <app-header></app-header>
    <app-footer></app-footer>
  </div>

  <div id="app2">
    <app-header></app-header>
    <app-footer></app-footer>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    // 전역 컴포넌트
    // Vue.component('컴포넌트 이름', 컴포넌트 내용);
    Vue.component('app-header', {
      template: '<h1>Header</h1>'
    });  

    new Vue({
      el: '#app',
      // 지역 컴포넌트 등록 방식
      components: {
        // '컴포넌트 이름': 컴포넌트 내용,
        'app-footer': {
          template: '<footer>First App footer</footer>'
        }
      },
    });

    new Vue({
      el: '#app2',
      components: {
        'app-footer': {
          template: '<footer>Second App footer</footer>'
        }
      }
    })
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76387886-2fc1aa00-63ab-11ea-8591-d82387f28275.png)

> 부모 컴포넌트와 자식 컴포넌트 호출 순서

![image](https://user-images.githubusercontent.com/44635266/76388174-cd1cde00-63ab-11ea-8363-6a2d49bfaa2f.png)

## 5. 컴포넌트 통신

* Vue의 경우 컴포넌트로 화면을 구성하므로 같은 웹 페이지라도 데이터를 공유할 수 없음
* 그 이유는 컴포넌트마다 자체적으로 고유한 유효 범위(Scope) 를 갖기 때문
* 각 컴포넌트의 유효 범위가 독립적이기 때문에 다른 컴포넌트의 값을 직접적으로 참조할 수가 없음

직접 다른 컴포넌트의 값을 참조할 수 없기 때문에, 뷰 프레임워크 자체에서 정의한 컴포넌트 데이터 전달 방법을 따라야 한다.

> 인스턴스와 컴포넌트가 통신하는 방식

![image](https://user-images.githubusercontent.com/44635266/76388383-5a603280-63ac-11ea-8a1b-041ffdf0430c.png)

### 인스턴트 -> 컴포넌트 : props

> 예제

```html
<body>
  <div id="app">
    <!-- <app-header v-bind:프롭스 속성 이름="상위 컴포넌트의 데이터 이름"></app-header> -->
    <app-header v-bind:propsdata="message" v-bind:appdata="string"></app-header>
    <app-content v-bind:propsdata="num"></app-content>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    var appHeader = {
      template: '<h1>{{ propsdata }}, {{ appdata }}</h1>',
      props: ['propsdata', 'appdata']
    }
    var appContent = {
      template: '<div>{{ propsdata }}</div>',
      props: ['propsdata']
    }

    new Vue({
      el: '#app',
      components: {
        'app-header': appHeader,
        'app-content': appContent
      },
      data: {
        message: 'hi',
        string : 'Hello App PropsData',
        num: 10
      }
    })
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76388276-1836f100-63ac-11ea-8566-7aea9c69ae57.png)

### 컴포넌트 -> 인스턴스 : event emit

> 예제

```html
<body>
  <div id="app">
    <p>{{ num }}</p>
    <!-- <app-header v-on:하위 컴포넌트에서 발생한 이벤트 이름="상위 컴포넌트의 메서드 이름"></app-header> -->
    <app-header v-on:pass="logText"></app-header>
    <app-content v-on:increase="increaseNumber"></app-content>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    var appHeader = {
      template: '<button v-on:click="passEvent">click me</button>',
      methods: {
        passEvent: function() {
          this.$emit('pass');
        }
      }
    }
    var appContent = {
      template: '<button v-on:click="addNumber">add</button>',
      methods: {
        addNumber: function() {
          this.$emit('increase');
        }
      }
    }

    var vm = new Vue({
      el: '#app',
      components: {
        'app-header': appHeader,
        'app-content': appContent
      },
      methods: {
        logText: function() {
          console.log('hi');
        },
        increaseNumber: function() {
          this.num = this.num + 1;
        }
      },
      data: {
        num: 10
      }
    });
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76388447-8976a400-63ac-11ea-8aa4-91a04237e02d.png)

## 6. 컴포넌트간 통신 - 응용

### 디렉티브

#### v-text

엘리먼트의 textContent를 업데이트 합니다. textContent의 일부를 갱신해야 하면 {{ Mustache }}를 사용해야 합니다.

```html
<span v-text="msg"></span>
<!-- 같습니다 -->
<span>{{msg}}</span>
```

#### v-html

엘리먼트의 innerHTML을 업데이트 합니다. 내용은 일반 HTML으로 삽입되므로 Vue 템플릿으로 컴파일 되지 않습니다. v-html을 사용하여 템플릿을 작성하려는 경우 컴포넌트를 사용하여 솔루션을 다시 생각해 보십시오.

```html
<div v-html="html"></div>
```

#### v-show 

토글은 표현식 값의 참에 기반을 둔 display CSS 속성입니다.

이 디렉티브는 조건이 바뀌면 트랜지션이 호출 됩니다.

```html
<h1 v-show="ok">안녕하세요!</h1>
```

#### v-if, v-else, v-else-if

표현식 값의 참 거짓을 기반으로 엘리먼트를 조건부 렌더링 합니다. 엘리먼트 및 포함된 디렉티브 / 컴포넌트는 토글하는 동안 삭제되고 다시 작성됩니다. 엘리먼트가 `<template>`엘리먼트인 경우 그 내용은 조건부 블록이 됩니다.

조건이 변경될 때 트랜지션이 호출 됩니다.

```html
<div v-if="type === 'A'">
  A
</div>
<div v-else-if="type === 'B'">
  B
</div>
<div v-else-if="type === 'C'">
  C
</div>
<div v-else>
  Not A/B/C
</div>
```

#### v-if vs v-show

v-if는 조건부 블럭 안의 이벤트 리스너와 자식 컴포넌트가 토글하는 동안 적절하게 제거되고 다시 만들어지기 때문에 “진짜” 조건부 렌더링 입니다

v-if는 또한 게으릅니다 초기 렌더링에서 조건이 거짓인 경우 아무것도 하지 않습니다. 조건 블록이 처음으로 참이 될 때 까지 렌더링 되지 않습니다.

비교해보면, v-show는 훨씬 단순합니다. CSS 기반 토글만으로 초기 조건에 관계 없이 엘리먼트가 항상 렌더링 됩니다.

일반적으로 v-if는 토글 비용이 높고 v-show는 초기 렌더링 비용이 더 높습니다. 매우 자주 바꾸기를 원한다면 v-show를, 런타임 시 조건이 바뀌지 않으면 v-if를 권장합니다.

#### v-for

원본 데이터를 기반으로 엘리먼트 또는 템플릿 블록을 여러번 렌더링합니다. 디렉티브의 값은 반복되는 현재 엘리먼트에 대한 별칭을 제공하기 위해 특수 구문인 alias in expression을 사용해야 합니다.

```html
<div v-for="item in items">
  {{ item.text }}
</div>
```

```html
<div v-for="(item, index) in items"></div>
<div v-for="(val, key) in object"></div>
<div v-for="(val, name, index) in object"></div>
```

#### v-on

엘리먼트에 이벤트 리스너를 연결합니다. 이벤트 유형은 전달인자로 표시됩니다. 표현식은 메소드 이름 또는 인라인 구문일 수 있으며, 수식어가 있으면 생략할 수 있습니다.

```html
<!-- 메소드 핸들러 -->
<button v-on:click="doThis"></button>
```

> 기타 속성들

* .stop - event.stopPropagation() 을 호출합니다.
* .prevent - event.preventDefault() 을 호출합니다.
* .capture - 캡처 모드에서 이벤트 리스너를 추가합니다.
* .self - 이벤트가 이 엘리먼트에서 전달된 경우에만 처리 됩니다
* .{keyCode | keyAlias} - 특정 키에 대해서만 처리 됩니다.
* .native - 컴포넌트의 루트 엘리먼트에서 네이티브 이벤트를 수신합니다.
* .once - 단 한번만 처리됩니다.
* .left - (2.2.0) 왼쪽 버튼 마우스 이벤트 트리거 처리기.
* .right - (2.2.0) 오른쪽 버튼 마우스 이벤트 트리거 처리기.
* .middle - (2.2.0) 가운데 버튼 마우스 이벤트 트리거 처리기.
* .passive - (2.3.0+) DOM 이벤트를 { passive: true }와 연결합니다.


#### v-bind

동적으로 하나 이상의 컴포넌트 속성 또는 표현식을 바인딩 합니다.

class또는 style 속성을 묶는 데 사용될 때, Array나 Objects와 같은 추가 값 유형을 지원합니다. 

```html
<!-- 속성을 바인딩 합니다. -->
<img v-bind:src="imageSrc">
```

> 기타 속성들

* .prop - 속성 대신 DOM 속성으로 바인딩 (무슨 차이가 있습니까?). 만약 태그가 컴포넌트라면 .props는 컴포넌트의 $el에 속성을 추가합니다.
* .camel - (2.1.0+) kebab-case 속성 이름을 camelCase로 변환합니다.
* .sync - (2.3.0+) 바인딩 된 값을 업데이트하기 위한 v-on를 확장하는 신택스 슈가입니다

#### v-model

폼 인풋 엘리먼트 또는 컴포넌트에 양방향 바인딩을 만듭니다. 

```html
<input v-model="message" placeholder="여기를 수정해보세요">
<p>메시지: {{ message }}</p>
```

> 예제

```html
<body>
  <div id="app">
    <app-header v-bind:propsdata="num"></app-header>
    <app-content v-on:pass="deliverNum"></app-content>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    var appHeader = {
      template: '<div>header</div>',
      props: ['propsdata']
    }
    var appContent = {
      template: '<div>content<button v-on:click="passNum">pass</button></div>',
      methods: {
        passNum: function() {
          this.$emit('pass', 10);
        }
      }
    }

    new Vue({
      el: '#app',
      components: {
        'app-header': appHeader,
        'app-content': appContent
      },
      data: {
        num: 0
      },
      methods: {
        deliverNum: function(value) {
          this.num = value;
        }
      }
    })
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76388774-3e10c580-63ad-11ea-9c45-cbf23be1af0f.png)

데이터 통신 과정

appContent 컴포넌트 passNum() -> Vue 인스턴스 deliverNunm() -> appHeader 컴포넌트 propsdata

## 7. 라우터

라우팅 이란 웹 페이지 간의 이동 방법을 말함. 라우팅은 현대 웹 앱 형태 중 하나인 싱글 페이지 애플리케이션(SPA)에서 주로 사용

* `<router-link to="URL">`
  * 페이지 이동 태그. 화면에서는 `<a>`로 표시되며 클릭하면 to에 지정한 URL로 이동
* `<router-view>`
  * 페이지 표시 태그. 변경되는 URL에 따라 해당 컴포넌트를 뿌려주는 영역

> 예제

```html
<body>
  <div id="app">
    <div>
      <router-link to="/login">Login</router-link>
      <router-link to="/main">Main</router-link>
    </div>
    <router-view></router-view>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
  <script>
    var LoginComponent = {
      template: '<div>login</div>'
    }
    var MainComponent = {
      template: '<div>main</div>'
    }

    var router = new VueRouter({
      // 페이지의 라우팅 정보      
      routes: [
        // 로그인 페이지 정보
        {
          // 페이지의 url
          path: '/login',
          // name: 'login',
          // 해당 url에서 표시될 컴포넌트
          component: LoginComponent
        },
        // 메인 페이지 정보
        {
          path: '/main',
          component: MainComponent
        }
      ]
    });

    new Vue({
      el: '#app',
      router: router,
    });
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76389046-c2634880-63ad-11ea-899c-0785cf6ff693.png)

## 8. axios

뷰에서 권고하는 HTTP 통신 라이브러리는 액시오스(Axios)입니다. Promise 기반의 HTTP 통신 라이브러리이며 상대적으로 다른 HTTP 통신 라이브러리들에 비해 문서화가 잘되어 있고 API가 다양합니다.

Github 주소 : https://github.com/axios/axios

![image](https://user-images.githubusercontent.com/44635266/76389368-61884000-63ae-11ea-9588-8ea6aa3e1639.png)

> 예제

```html
<body>
  <div id="app">
    <button v-on:click="getData">get user</button>
    <div>
      {{ users }}
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: {
        users: []
      },
      methods: {
        getData: function() { 
          console.log("Axios Start");
          var vm = this;
          axios.get('https://jsonplaceholder.typicode.com/users/')
            .then(function(response) {
              console.log(response.data);
              vm.users = response.data;
            })
            .catch(function(error) {
              console.log(error);
            });
          console.log("Axios End");
          
        }
      }
    })
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76389476-a44a1800-63ae-11ea-91f6-986dfda68e24.png)

> 비동기로 처리된 결과

![image](https://user-images.githubusercontent.com/44635266/76389492-ae6c1680-63ae-11ea-8ef3-4e22f88a4a55.png)

## 9. 템플릿 문법


> 데이터 바인딩 예제

```html
<body>
  <div id="app">
    <p v-bind:id="uuid" v-bind:class="name">{{ num }}</p>
    <!-- <p id="abc1234">{{ num }}</p> -->
    <p>{{ doubleNum }}</p>
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      test user has been logged in
    </div>
    <div v-show="loading">
      Loading...
    </div>
    <!-- TODO: 인풋 박스를 만들고 입력된 값을 p 태그에 출력해보세요 -->
    <input type="text" v-model="message">
    <p>{{ message }}</p>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: {
        num: 10,
        uuid: 'abc1234',
        name: 'text-blue',
        loading: true,
        message: ''
      },
      computed: {
        doubleNum: function() {
          return this.num * 2;
        }
      }
    })
  </script>
</body>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76390925-a8c40000-63b1-11ea-850a-9a3337bea461.png)

## 10. 템플릿 문법 - 응용

### Watch vs Computed

#### computed

computed 속성은 vue인스턴스 안에서 처리를 하는것이 좋다고 생각하는 처리를 담당하는 데이터 연산들을 정의하는 영역이다. 

#### watch

watch 속성은 데이터 변화를 감지하여 자동으로 특정 로직을 수행한다. computed 속성과 유사하지만 computed는 내장 api를 사용하는 간단한 연산정도에 적합하고
watch는 데이터 호출과 같이 시간이 상대적으로 더 많이 소모되는 비동기 처리에 적합하다.

#### computed vs watch

computed는 data 속성에 변화가 있을때 자동으로 다시 연산을 한다.

computed에서 사용하고 있는 data속성인 message라는 프로퍼티가 변화가 있을때만 다시 연산을하고 한번 연산한 값을 캐싱 해놓았다가 필요한 부분에 다시 재 사용한다. 같은 페이지내에서 같은 연산을 여러번 반복해야 할 경우에 성능면에서 효율적으로 사용할 수 있다.

반면 methods는 캐싱이라는 개념이 없기 때문에 매번 재 렌더링된다. 캐싱 효과가 필요하다면 computed를 사용하고 캐싱이 필요없다면 methods를 사용하도록 하자.

### 11. Vue CLI

```shell
$ npm install -g @vue/cli
$ $ vue --version
@vue/cli 4.2.2

$ vue create my-vue-app
Vue CLI v4.2.2
✨  Creating project in /Users/has3ong/Desktop/ktds/Practice/learn-vue-js-master/my-vue-app.
🗃  Initializing git repository...
⚙️  Installing CLI plugins. This might take a while...

yarn install v1.22.0
info No lockfile found.
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...



success Saved lockfile.
info To upgrade, run the following command:
$ curl --compressed -o- -L https://yarnpkg.com/install.sh | bash
✨  Done in 20.73s.
🚀  Invoking generators...
📦  Installing additional dependencies...

yarn install v1.22.0
[1/4] 🔍  Resolving packages...
[2/4] 🚚  Fetching packages...
[3/4] 🔗  Linking dependencies...
[4/4] 🔨  Building fresh packages...
info This module is OPTIONAL, you can safely ignore this error
success Saved lockfile.
✨  Done in 6.50s.
⚓  Running completion hooks...

📄  Generating README.md...

🎉  Successfully created project my-vue-app.
👉  Get started with the following commands:

 $ cd my-vue-app
 $ yarn serve

$ cd create my-vue-app

$ ls
README.md        babel.config.js  node_modules/    package.json     public/          src/             yarn.lock

$ npm run serve

> my-vue-app@0.1.0 serve /Users/has3ong/Desktop/ktds/Practice/learn-vue-js-master/my-vue-app
> vue-cli-service serve

 INFO  Starting development server...
98% after emitting CopyPlugin

 DONE  Compiled successfully in 2507ms                                                                                                                    오후 3:48:21


  App running at:
  - Local:   http://localhost:8081/
  - Network: http://172.20.10.2:8081/

  Note that the development build is not optimized.
  To create a production build, run yarn build.
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76389934-cb551980-63af-11ea-8e41-20b5477de89b.png)


### 12. User Input Form

> App.vue

```html
<template>
  <form v-on:submit.prevent="submitForm">
    <div>
      <label for="username">id: </label>
      <input id="username" type="text" v-model="username">
    </div>
    <div>
      <label for="password">pw: </label>
      <input id="password" type="password" v-model="password">
    </div>
    <button type="submit">login</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data: function() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    submitForm: function() {
      // event.preventDefault();
      console.log(this.username, this.password);
      var url = 'https://jsonplaceholder.typicode.com/users';
      var data = {
        username: this.username,
        password: this.password
      }
      axios.post(url, data)
        .then(function(response) {
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
}
</script>

<style>

</style>
```

> 결과화면

![image](https://user-images.githubusercontent.com/44635266/76389804-7addbc00-63af-11ea-8b3b-401d0cf7b64b.png)
