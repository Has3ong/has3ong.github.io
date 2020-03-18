---
title : Vue.js Lecture 2
tags :
---

## 1. Vuejs TODO App

> Result

![image](https://user-images.githubusercontent.com/44635266/76718179-42f0c300-6779-11ea-9618-4e12d051144f.png)

> App.vue

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <TodoInput v-on:addItem="addOneItem"></TodoInput>
    <TodoList v-bind:propsdata="todoItems" v-on:removeItem="removeOneItem" v-on:toggleItem="toggleOneItem"></TodoList>
    <TodoFooter v-on:clearAll="clearAllItems"></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from './components/TodoHeader.vue'
import TodoInput from './components/TodoInput.vue'
import TodoList from './components/TodoList.vue'
import TodoFooter from './components/TodoFooter.vue'

export default {
  data: function() {
    return {
      todoItems: []
    }
  },
  methods: {
    addOneItem: function(todoItem) {
      var obj = {completed: false, item: todoItem};
      localStorage.setItem(todoItem, JSON.stringify(obj));
      this.todoItems.push(obj);
    },
    removeOneItem: function(todoItem, index) {
      this.todoItems.splice(index, 1);
      localStorage.removeItem(todoItem.item);
    },
    toggleOneItem: function(todoItem, index) {
      todoItem.completed = !todoItem.completed;
      localStorage.removeItem(todoItem.item);
      localStorage.setItem(todoItem.item, JSON.stringify(todoItem));
    },
    clearAllItems: function() {
      this.todoItems = [];
      localStorage.clear();
    }
  },
  created: function() {
    if (localStorage.length > 0) {
      for (var i = 0; i < localStorage.length; i++) {
        if (localStorage.key(i) !== 'loglevel:webpack-dev-server') {
          this.todoItems.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
        }
      }
    }
  },
  components: {
    TodoHeader: TodoHeader,
    TodoInput: TodoInput,
    TodoList: TodoList,
    TodoFooter: TodoFooter
  }  
}
</script>
```

> TodoFooter.vue

```vue
<template>
  <div class="clearAllContainer">
    <span class="clearAllBtn" v-on:click="clearTodo">Clear All</span>
  </div>
</template>

<script>
export default {
  methods: {
    clearTodo: function() {
      this.$emit('clearAll');
    }
  }
}
</script>
```

> TodoHeader.vue

```vue
<template>
  <header>
    <h1>TODO it!</h1>
  </header>
</template>
```

> TodoInput.vue

```vue
<template>
  <div class="inputBox shadow">
    <input type="text" v-model="newTodoItem">
    <span class="addContainer" v-on:click="addTodo">
      <i class="addBtn fas fa-plus" aria-hidden="true"></i>
    </span>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      newTodoItem: ''
    }
  },
  methods: {
    addTodo: function() {
      if (this.newTodoItem !== '') {
        this.$emit('addItem', this.newTodoItem);
        this.clearInput();
      }
    },
    clearInput: function() {
      this.newTodoItem = '';
    }
  }
}
</script>
```

> TodoList.vue

```vue
{% raw %}
<template>
  <section>
    <ul>
      <li v-for="(todoItem, index) in propsdata" class="shadow" v-bind:key="todoItem.item">
        <i class="checkBtn fas fa-check" v-bind:class="{checkBtnCompleted: todoItem.completed}" v-on:click="toggleComplete(todoItem, index)"></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <span class="removeBtn" v-on:click="removeTodo(todoItem, index)">
          <i class="removeBtn fas fa-trash-alt"></i>
        </span>
      </li>
    </ul>
  </section>
</template>

<script>
export default {
  props: ['propsdata'],
  methods: {
    removeTodo: function(todoItem, index) {
      this.$emit('removeItem', todoItem, index);
    },
    toggleComplete: function(todoItem, index) {
      this.$emit('toggleItem', todoItem, index); 
    }
  }
}
</script>
{% endraw %}
```

## 2. ES6 / Babel

### ES6 란

* ECMAScript 2015 와 동일한 용어
* 최신 Front-End Framework 인 React, Angular, Vue 에서 권고하는 언어 형식

### Babel

* 구 버전 브라우저는 ES6 기능을 지원하지 않으므로 Transpiling 을 해줌
* ES6 의 각 문법을 각 브라우저의 호환가능한 ES5 로 변환하는 컴파일러

> Babel Loader

```js
module : {
    loaders : [{
        test: /\.js$/,
        loader: 'babel-loader',
        query : {
          presets : ['es2015']
        }
    }]
}
```

> Example - [Babel](https://babeljs.io/)

![image](https://user-images.githubusercontent.com/44635266/76718209-5308a280-6779-11ea-8c5d-ccdf4e8f2220.png)

### const / let

* 블록 단위의 `{}` 로 변수의 범위가 제한되었음.
* `const` : 한번 선언한 값에 대하여 변경할 수 없음 (상수)
* `let` : 한번 선언한 값에 대해서 다시 선언할 수 없음 (변수)

> let 사용 예

```js
// 똑같은 변수를 재선언할 때 오류
let a = 10;
let a = 20; // Uncaught SyntaxError: Identifier 'a' has already been declared
```

> const 사용 예

```js
// 값을 다시 할당했을 때 오류
const a = 10;
a = 20; // Uncaught TypeError: Assignment to constant variable.
```

하지만 const 는 `[]`, `{}` 로 선언하면 객체의 property 와 element 를 변경할 수 있습니다.

```js
const b = {
    num: 10,
    text: 'hi'
};
console.log(b.num); // 10

b.num = 20;
console.log(b.num); // 20

const c = [];
console.log(c); // []

c.push(10);
console.log(c); // [10]
```

#### var 의 유효 범위

var 의 유효 범위는 함수의 블록 단위로 제한된다. 함수 스코프(function scope) 라고 표현한다.

```vue
var a = 100;
function print() {
    var a = 10;
    console.log(a);
}
print(); // 10
```

#### for 반복문에서 var / let 유효 범위 차이

> var

```js
var a = 10;
for (var a = 0; a < 5; a++) {
    console.log(a); // 0 1 2 3 4 5
}
console.log(a); // 6
```

> let

```js
var a = 10;
for (let a = 0; a < 5; a++) {
    console.log(a); // 0 1 2 3 4 5
}
console.log(a); // 10
```

### 화살표 함수 (Arrow Function)

> 기존의 함수 정의 방식

```js
var a = function() {
    // ...
};
```

> 화살표 함수를 이용한 정의 방식  

```js
var a = () => {
    // ...
};
```

> Parameter 값이 있는 경우

```js
const a = (num) => { return num * 10 };
const b = num => num * 10;
a(10); // 100
b(10); // 100
```

### 향상된 객체 리터럴 (Enhanced Object Literals)

> 기존 방식

```js
var josh = {
  // 속성: 값
  language: 'javascript',
  coding: function() {
    console.log('Hello World');
  }
};
```

> 향상된 객체 리터럴을 이용한 정의 방식

```js
var language = 'javascript'

var josh = {
  language,
  coding() {
    console.log('Hello World');
  }
}
```

### 모듈 (Modules)

#### import & export

> export

```js
export 변수, 함수
// math.js
export var pi = 3.14;
```

> import

```js
import { 불러올 변수 또는 함수 이름 } from '파일 경로';

// app.js
import { pi } from './math.js';

console.log(pi); // 3.14
```

### 템플릿 리터럴 (Template Literal)

#### 여러 줄에 걸쳐서 문자열 선언하기

> 기존 방식

```js
var str = 'Template literals are string literals allowing embedded expressions. \n' + 
'You can use multi-line strings and string interpolation features with them. \n' + 
'They were called "template strings" in prior editions of the ES2015 specification.';
```

> 변화된 방식

```js
const str = `Template literals are string literals allowing embedded expressions.
You can use multi-line strings and string interpolation features with them.
They were called "template strings" in prior editions of the ES2015 specification.`;
```

#### 문자열 중간에 변수 대입하기

> 기존 방식

```js
var language = 'Javascript';
var expression = 'I love ' + language + '!';
console.log(expression); // I love Javascript!
```

> 변화된 방식

```js
var language = 'Javascript';
var expression = `I love ${language}!`;
console.log(expression); // I love Javascript!
```

### 스프레드 오퍼레이터(Spread Operator)

스프레드 오퍼레이터는 특정 객체 또는 배열의 값을 다른 객체, 배열로 복제하거나 옮길 때 사용합니다. 연산자의 모양은 `...` 이렇게 생겼습니다.

> 기존 선언방식

```js
import { mapGetters } from 'vuex';

export default {
  computed: {
    getStrings() {
      // ..
    },
    getNumbers() {
      // ..
    },
    getUsers() {
      // ..
    },
    anotherCounter() {
      // ..
    }
  }
}
```

> 변화된 방식

```js
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['getStrings', 'getNumbers', 'getUsers']),
    anotherCounter() {
      // ..
    }
  }
}
```

## 3. Vuex 

* 컴포넌트 데이터를 관리하기 위한 상태 관리 패턴 / 라이브러리
* React 에 Flux 패턴에 기인함

### Flux vs MVC

#### MVC

> MVC 패턴

![image](https://user-images.githubusercontent.com/44635266/76723234-e944c480-6789-11ea-9b93-1162588299f8.png)

> MVC 패턴에서 발생할 수 있는 문제점

![image](https://user-images.githubusercontent.com/44635266/76723249-f2ce2c80-6789-11ea-9722-5ccf35651b0d.png)

* 기능 추가 및 변경에 따른 생기는 문제점을 예측할 수 없음
* 앱이 복잡해지면서 생기는 업데이트 루프

#### Flux

* MVC 패턴의 복잡한 데이터 흐름 문제를 해결하는 개발 패턴
* 데이터가 무조건 한 방향으로만 흐른다.

> Flux 패턴

![image](https://user-images.githubusercontent.com/44635266/76723211-dc27d580-6789-11ea-9881-703aef1e029a.png)

* action : 화면에서 발생하는 이벤트 또는 사용자의 입력
* dispatcher : 데이터를 변경하는 방법, 메소드
* model : 화면에 표시할 데이터
* view : 사용자에게 비춰지는 화면

> Flux 패턴의 데이터 흐름

![image](https://user-images.githubusercontent.com/44635266/76723378-63754900-678a-11ea-9d95-5421f815724d.png)

* 데이터 흐름이 여러 갈래로 나눠지지 않고 단방향으로만 처리

### Vuex 컨셉

> Vuex

![image](https://user-images.githubusercontent.com/44635266/76723483-bcdd7800-678a-11ea-8bcb-8862f06de42d.png)

* State : 컴포넌트 간에 공유하는 데이터 `data()`
* View : 데이터를 표시하는 화면 `template`
* Action : 사용자의 입력에 따라 데이터를 변경하는 `methods`

> Vuex 구조

![image](https://user-images.githubusercontent.com/44635266/76723569-25c4f000-678b-11ea-84f3-7d278e0d845a.png)

컴포넌트 -> 비동기 로직(Actions) -> 동기 로직(Mutations) -> 상태

* 시작점은 Vue Components이다.
* 컴포넌트에서 비동기 로직(Method를 선언해서 API 콜 하는 부분 등)인 Actions를 콜하고,
* Actions는 비동기 로직만 처리할 뿐 State(Data)를 직접 변경하진 않는다.
* Actions가 동기 로직인 Mutations를 호출해서 State(Data)를 변경한다.
* Mutations에서만 State(Data)를 변경할 수 있다.

### Vuex 기술 요소

* state : 여러 컴포넌트의 공유되는 `data`
* getters : 연산된 state 값을 접근하는 속성 `computed`
* mutations : state 값을 변경하는 이벤트 로직 $\cdot$ 메소드 `methods`
* actions : 비동기 처리 로직을 선언하는 메소드 `async methods`

#### state

여러 컴포넌트간데 공유할 데이터 - 상태

```js
// Vue
data : {
  message : 'Hello Vue.js'
}

// Vuex
state : {
  message : 'Hello Vue.js'
}
```

```html
{% raw %}
<!-- Vue -->
<p>{{ message }}</p>
<!-- Vuex -->
<p>{{ this.$store.state.message }}</p>
{% endraw %}
```

#### getters

state 값을 접근하는 속성이자 `computed()` 처럼 미리 연산된 값을 접근하는 속성

```js
// store.js
state : {
  num : 10
},
getters : {
  getNumber(state) {
    return state.num;
  },
  getDoubleNumber(state) {
    return state.num * 2
  }
}
```

```html
{% raw %}
<p>{{ this.$store.getter.getNumber }}</p>
<p>{{ this.$store.getter.getDoubleNumber }}</p>
{% endraw %}
```

#### mutations 

* state 값을 변경할 수 있는 유일한 방법이자 메소드
* mutations 은 `commit()` 으로 동작한다.
* state 는 여러 컴포넌트에서 공유하기 때문에 mutations 으로 변경하지 않으면, 추적하기 어렵다.

```js
// store.js
state : { num : 10 },
mutations : {
  printNumber(state) {
    return state.num
  },
  sumNumber(state, anotherNum) {
    return state.num + anotherNum
  }
}
```

```js
// App.vue
this.$store.commit('printNumber');
this.$store.commit('sumNumver', 20);
```

mutations 을 동작시킬 때 인자(payload) 를 보낼 수 있음

```js
// store.js
state : { storeNum : 10 },
mutations : {
  modifyState(state, payload) {
    console.log(payload.str)
    return state.storeNum += payload.num
  }
}

// App.vue
this.$store.commit('modifyState', {
  str : 'passed from payload',
  num : 20
})
```

#### actions

* 비동기 처리 로직을 선언하는 메소드, 비동기 로직을 담당하는 mutations

```js
// store.js
state : {
  num : 10
},

mutations : {
  doubleNumber(state) {
    state.num * 2
  }
},
actions : {
  delayDoubleNumber(context) { 
    context.commit('doubleNumber');
  }
}

// App.vue
this.$store.dispatch('delayDoubleNumber');
```

* 언제 어느 컴포넌트에서 해당 state를 호출하고, 변경했는지 확인하기가 어려움
* 여러개의 컴포넌트에서 mutations로 시간차를 두고 state를 변경하는 경우
  * state값의 변화를 추적하기 어렵기 때문에 mutations 속성에는 처리 시점을 예측할 수 있는 동기 처리 로직만 넣어야 한다.

### Vuex Helper

Store 에 있는 아래 4 가지 속성을 간편하게 코딩하는 방법

* state -> mapState
* getters -> mapGetters
* mutations -> mapMutations
* actions -> mapActions

```js
// App.vue
import { mapState } from vuex;
import { mapGetters } from vuex;
import { mapMutations } from vuex;
import { mapActions } from vuex;

export default {
  computed() { ...mapState(['num']), ...mapGetters(['countedNum']) },
  methods: { ...mapMutations(['clickBtn']), ...mapActions(['asyncClickBtn']) }
}
```

## 4. Vuex 사용해보기

> store.js

```js
import Vue from 'vue';
import Vuex from 'vuex'

// 플러그인 사용
Vue.use(vuex)

export const store = new Vuex.Store({
  //
});
```

> main.js

```js
import Vue from 'vue'
import App from './App.vue'
import { store } from './store.js'

new Vue({
  el: '#app',
  store,
  render: h => h(App)
})
```

### Vuex 를 이용한 TODO Application 코드 리팩토링

> store.js

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const storage = {
    fetch() {
        const arr = [];
        if (localStorage.length > 0) {
            for (let i = 0; i < localStorage.length; i++) {
                if (localStorage.key(i) !== 'loglevel:webpack-dev-server') {
                    arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
                }
            }
        }
        return arr;
    }
}

export const store = new Vuex.Store({
    state: {
        todoItems: storage.fetch()
    },
    getters: {
        getTodoItems(state) {
            return state.todoItems;
        }
    },
    mutations: {
        addOneItem(state, todoItem) {
            const obj = {completed: false, item: todoItem};
            localStorage.setItem(todoItem, JSON.stringify(obj));
            state.todoItems.push(obj);
        },
        removeOneItem(state, payload) {
            state.todoItems.splice(payload.index, 1);
            localStorage.removeItem(payload.todoItem.item);
        },
        toggleOneItem(state, payload) {
            state.todoItems[payload.index].completed = !state.todoItems[payload.index].completed;
            localStorage.removeItem(payload.todoItem.item);
            localStorage.setItem(payload.todoItem.item, JSON.stringify(payload.todoItem));
        },
        clearAllItems(state) {
            state.todoItems = [];
            localStorage.clear();
        }
    }
});
```

> App.vue

```vue
<template>
  <div id="app">
    <TodoHeader></TodoHeader>
    <TodoInput></TodoInput>
    <TodoList></TodoList>
    <TodoFooter></TodoFooter>
  </div>
</template>

<script>
import TodoHeader from './components/TodoHeader.vue'
import TodoInput from './components/TodoInput.vue'
import TodoList from './components/TodoList.vue'
import TodoFooter from './components/TodoFooter.vue'
export default {
  components: {
    TodoHeader,
    TodoInput,
    TodoList,
    TodoFooter
  }
}
</script>
```

> TodoFooter.vue

```vue
<template>
  <div class="clearAllContainer">
    <span class="clearAllBtn" v-on:click="clearTodo">Clear All</span>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  methods: {
    ...mapMutations({
      clearTodo: 'clearAllItems'
    })
  }
}
</script>
```

> TodoInput.vue

```vue
<template>
  <div class="inputBox shadow">
    <input type="text" v-model="newTodoItem" @keyup.enter="addTodo">
    <span class="addContainer" v-on:click="addTodo">
      <i class="addBtn fas fa-plus" aria-hidden="true"></i>
    </span>

    <Modal v-if="showModal" @close="showModal = false">
      <h3 slot="header">
        경고
        <i class="closeModalBtn fa fa-times"
          aria-hidden="true"
          @click="showModal = false">
        </i>
      </h3>
      <p slot="body">할 일을 입력하세요.</p>
    </Modal>
  </div>
</template>

<script>
import Modal from './common/Modal.vue'
export default {
  data() {
    return {
      newTodoItem: '',
      showModal: false
    }
  },
  methods: {
    addTodo() {
      if (this.newTodoItem !== '') {
        const item = this.newTodoItem.trim();
        this.$store.commit('addOneItem', item);
        this.clearInput();
      } else {
        this.showModal = !this.showModal;
      }
    },
    clearInput() {
      this.newTodoItem = '';
    }
  },
  components: {
    Modal
  }
}
</script>
```

> TodoList.vue

```vue
{% raw %}
<template>
  <section>
    <transition-group name="list" tag="ul">
      <li v-for="(todoItem, index) in this.storedTodoItems" class="shadow" v-bind:key="todoItem.item">
        <i class="checkBtn fas fa-check" v-bind:class="{checkBtnCompleted: todoItem.completed}" v-on:click="toggleComplete({todoItem, index})"></i>
        <span v-bind:class="{textCompleted: todoItem.completed}">{{ todoItem.item }}</span>
        <span class="removeBtn" v-on:click="removeTodo({todoItem, index})">
          <i class="removeBtn fas fa-trash-alt"></i>
        </span>
      </li>
    </transition-group>
  </section>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  methods: {
    ...mapMutations({
      removeTodo: 'removeOneItem',
      toggleComplete: 'toggleOneItem'
    })
  },
  computed: {
    ...mapGetters({
      storedTodoItems: 'getTodoItems'
    })
  }
}
</script>
{% endraw %}
```

## 5. Store 모듈화

### 첫 번째 방법

> store.js

```js
import Vue from 'vue'
import Vuex from 'vuex'
import * as getters from './getters.js'
import * as mutations from './mutations.js'

Vue.use(Vuex);

const storage = {
    fetch() {
        const arr = [];
        if (localStorage.length > 0) {
            for (let i = 0; i < localStorage.length; i++) {
                if (localStorage.key(i) !== 'loglevel:webpack-dev-server') {
                    arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
                }
            }
        }
        return arr;
    }
}

export const store = new Vuex.Store({
    state: {
        todoItems: storage.fetch()
    },
    getters: getters,
    mutations: mutations
});
```

> getter.js

```js
export const getTodoItems = function(state) {
    return state.todoItems;
}
```

> mutations.js

```js
const addOneItem = function(state, todoItem) {
    const obj = {completed: false, item: todoItem};
    localStorage.setItem(todoItem, JSON.stringify(obj));
    state.todoItems.push(obj);
};

const removeOneItem = function(state, payload) {
    state.todoItems.splice(payload.index, 1);
    localStorage.removeItem(payload.todoItem.item);
};

const toggleOneItem = function(state, payload) {
    state.todoItems[payload.index].completed = !state.todoItems[payload.index].completed;
    localStorage.removeItem(payload.todoItem.item);
    localStorage.setItem(payload.todoItem.item, JSON.stringify(payload.todoItem));
};

const clearAllItems = function(state) {
    state.todoItems = [];
    localStorage.clear();
};

export { addOneItem, removeOneItem, toggleOneItem, clearAllItems };
```

### 두 번째 방법

> store.js

```js
import Vue from 'vue'
import Vuex from 'vuex'
import todo from './modules/todo.js'

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules : {
        todo
    }
});
```

> modules/todo.js

```js
const storage = {
    fetch() {
        const arr = [];
        if (localStorage.length > 0) {
            for (let i = 0; i < localStorage.length; i++) {
                if (localStorage.key(i) !== 'loglevel:webpack-dev-server') {
                    arr.push(JSON.parse(localStorage.getItem(localStorage.key(i))));
                }
            }
        }
        return arr;
    }
}

const state = {
    todoItems: storage.fetch()
};

const getters = {
    getTodoItems(state) {
        return state.todoItems;
    }
};

const mutations = {
    addOneItem(state, todoItem) {
        const obj = {completed: false, item: todoItem};
        localStorage.setItem(todoItem, JSON.stringify(obj));
        state.todoItems.push(obj);
    },
    removeOneItem(state, payload) {
        state.todoItems.splice(payload.index, 1);
        localStorage.removeItem(payload.todoItem.item);
    },
    toggleOneItem(state, payload) {
        state.todoItems[payload.index].completed = !state.todoItems[payload.index].completed;
        localStorage.removeItem(payload.todoItem.item);
        localStorage.setItem(payload.todoItem.item, JSON.stringify(payload.todoItem));
    },
    clearAllItems(state) {
        state.todoItems = [];
        localStorage.clear();
    }
};

export default {
    state,
    getters,
    mutations
};
```
