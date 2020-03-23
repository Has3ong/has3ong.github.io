---
title : React Pure React
tags :
- Factory
- Component
- JavaScript
- React
---

*이 포스트는 [Learning React](https://www.imel.ba/edukacija/learningreact1.pdf) 를 바탕으로 작성하였습니다.*

## Page Setup 

React 를 브라우저에서 다룰려면 React 와 ReactDOM 라이브러리를 불러와야 합니다. React 는 뷰를 만들기 위한 라이브러리고 ReactDOM 은 UI 를 실제로 렌더링할 때 사용하는 라이브러리 입니다.

스크립트와 HTML 에릴먼트를 추가하는 방법을 아래 예제에서 확인할 수 있습니다.

```js
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pure React Samples</title>
</head>
<body>
    <!-- Target container -->
    <div id="react-container"></div>

    <!-- React library & ReactDOM-->
    <script src="https://unpkg.com/react@15.4.2/dist/react.js"></script>
    <script src="https://unpkg.com/react-dom@15.4.2/dist/react-dom.js"></script>
    <script>
    // Pure React and JavaScript code
    </script>
</body>
</html>
```

위 설정이 브라우저에서 React 를 사용하기 위한 최소 요구사항입니다.

## The Virtual DOM 

HTML 은 브라우저가 DOM 을 구성하기 위해 따라야 하는 절차라 간단히 말할 수 있습니다.

HTML 문서를 이루는 엘리먼트는 브라우저가 HTML 문서를 읽어 들이면 DOM 엘리먼트가 되고, 이 DOM 이 화면에 사용자 인터페이스를 표시합니다. 아래 간단한 조리법 예제를 보겠습니다.

```js
<section id="baked-salmon">
    <h1>Baked Salmon</h1>
    <ul class="ingredients">
        <li>1 lb Salmon</li>
        <li>1 cup Pine Nuts</li>
        <li>2 cups Butter Lettuce</li>
        <li>1 Yellow Squash</li>
        <li>1/2 cup Olive Oil</li>
        <li>3 cloves of Garlic</li>
    </ul>
  <section class="instructions">
      <h2>Cooking Instructions</h2>
      <p>Preheat the oven to 350 degrees.</p>
      <p>Spread the olive oil around a glass baking dish.</p>
      <p>Add the salmon, garlic, and pine nuts to the dish.</p>
      <p>Bake for 15 minutes.</p>
      <p>Add the yellow squash and put back in the oven for 30 mins.</p>
      <p>Remove from oven and let cool for 15 minutes. Add the lettuce and serve.</p>
    </section>
</section>
```

React 는 브라우저 DOM 을 갱신하기 위해 만들어진 라이브러리입니다. React 가 모든 처리를 대신 해주기 때문에 더이상 SPA(Singple-Page, Application) 를 더 효유렂긍로 만들기 위해 여러 복잡한 내용을 신경 쓸 필요 없습니다.

DOM API 를 직접 조작하지 않습니다. 대신 **가상 DOM** 을 다루거나 React 가 UI 를 생성하고 브라우저와 상호작용하기 위해 사용하는 몇 가지 명령을 다룹니다.

가상 DOM 은 React 엘리먼트로 이루어져있습니다. React 에릴먼트는 개념상 HTML 엘리먼트와 비슷하지만 실제로 JavaScript 객체입니다. DOM API 를 직접 다루는 것보다 JavaScript 객체인 가상 DOM 을 직접 다루는 편이 훨씬 빠릅니다. 우리가 가상 DOM 을 변경하면 React 는 DOM API 를 사용해 변경사항을 가장 효율적으로 렌더링해줍니다.

## React Elements 

브라우저 DOM 은 DOM 엘리먼트로 이루어집니다. 마찬가지로 React DOM 은 React 엘리먼트로 이루어집니다.

React.createElement 를 사용해 `h1` 을 표현하는 React 앨리먼트를 만들어 보겠습니다.

```js
React.createElement("h1", null, "Baked Salmon")
```

첫 번째 인자는 만드려는 엘리먼트의 타입을 정의합니다. 두 번째 인자는 엘리먼트의 프로퍼티를 표현합니다. 여기서 `h1` 에는 프로퍼티가 없습니다. 세 번째 인자는 태그사이에 들어가야 할 엘리먼트의 자식 노드를 표현합니다.

렌더링 과정에서 리액트는 다음 엘리먼트를 실제 DOM 엘리먼트로 변환합니다.

```js
<h1>Baked Salmon</h1>
```

DOM 엘리먼트에 있는 속성을 React 앨리먼트의 프로퍼티로 표현할 수 있습니다. 다음은 `id` 와 `data-type` 속성이 있는 HTML `h1` 태그르 보여줍니다.

```js
React.createElement("h1",
    {id: "recipe-0", 'data-type': "title"},
    "Baked Salmon"
)

<h1 data-reactroot id="recipe-0" data-type="title">Baked Salmon</h1>
```

각 프로퍼티는 태그에 어트리뷰트로 추가되며 자식 텍스트는 엘리먼트 내부의 텍스트로 추가됩니다. 또한 `data-reactroot` 라는 어트리뷰트를 볼 수 있습니다. 이는 React 컴포넌트의 루트 엘리먼트를 식별해주는 어트리뷰트입니다.(`Example 1`)

> Example 1 - Relationship between createElement and the DOM element

![image](https://user-images.githubusercontent.com/44635266/76917466-d86d8d80-6906-11ea-8d26-592eddab408c.png)

React 엘리먼트는 React 가 DOM 엘리먼트를 구성하는 방법을 알ㄹ려주는 JavaScript 리터럴입니다. 아래 예제는 `createElement` 가 실제로 만든 엘리먼트입니다.

```js
{
    $$typeof: Symbol(React.element),
    "type": "h1",
    "key": null,
    "ref": null,
    "props": {"children": "Baked Salmon"},
    "_owner": null,
    "_store": {}
}
```

React 엘리먼트는 위와같이 생겼습니다. 그 안에는 React 가 사용하는 `_owner`, `_store`, `$$typeof` 같은 필드가 있습니다. React 엘리먼트에서는 `key` 와 `ref` 필드가 중요합니다.

React 엘리먼트의 `type` 프로퍼티는 만들려는 HTML 이나 SVG 엘리먼트의 타입을 지정합니다. `props` 프로퍼티는 DOM 엘리먼트를 만들기 위해 필요한 데이터나 자식 엘리먼트를 표현합니다. `children` 프로퍼티는 텍스트 형태로 표시할 다른 내부 엘리먼트입니다.

## ReactDOM 

ReactDOM 에는 React 엘리먼트를 브라우저에 렌더링하는 데 필요한 모든 도구가 들어 있습니다. ReactDOM 에는 `render` 메소드가 들어 있고 서버에서 사용하기 위해 `renderToString` 과 `renderToStaticMarkup` 메소드도 들어있습니다. 가상 DOM 에서 HTML 을 생성하는 데 필요한 모든 도구가 이 라이브러리 안에 있습니다.

React 엘리먼트와 그 모든 자식 엘리먼트를 함께 렌더링하기 위해 `ReactDOM.render` 를 사용합니다. 첫 번째 인자는 렝더링할 React 에릴먼트며, 두 번째 인자는 렌더링이 일어날 대상 DOM 노드 입니다.

```js
var dish = React.createElement("h1", null, "Baked Salmon")
ReactDOM.render(dish, document.getElementById('react-container'))
```

제목 엘리먼트를 DOM 으로 렌더링하면 HTML 에 정의해둔 `react-container` 라는 `id` 를 가지는 `div` 의 자식으로 `h1` 엘리먼트가 추가됩니다. 아래 예제를 보면 `body` 의 자식인 `div` 에 `h1` 이 생긴 것을 볼 수 있습니다.

```js
<body>
 <div id="react-container">
    <h1>Baked Salmon</h1>
 </div>
</body>
```

## Children 

ReactDOM 에는 항상 한 엘리먼트만 DOM 으로 렌더링할 수 있습니다. React 는 렌더링할 엘리먼트에 `data-reactroot` 라는 꼬리표를 답니다. 모든 다른 React 엘리먼트는 이 루트 엘리먼트 아래에 포함됩니다.

React 는 `props.children` 을 사용해 자식 엘리먼트를 렌더링합니다. 앞 절에서는 텍스트 엘리먼트 `h1` 엘리먼트의 유일한 자식으로 렌더링했기 때문에 `props.children` 이 `Baked Salmon` 으로 설정되었습니다.

텍스트가 아닌 다른 React 엘리먼트를 자식으로 렌더링할 수 있고, 엘리먼트의 트리가 생깁니다. 컴포넌트 트리라는 말을 사용합니다. 트리에는 루트 컴포넌트가 하나 존재하고, 루트 아래로 많은 가지가 자랍니다.

아래 예제와 같이 재료가 들어있는 번호가 붙지 않은 리스트를 생각해보겠습니다.

```js
<ul>
 <li>1 lb Salmon</li>
 <li>1 cup Pine Nuts</li>
 <li>2 cups Butter Lettuce</li>
 <li>1 Yellow Squash</li>
 <li>1/2 cup Olive Oil</li>
 <li>3 cloves of Garlic</li>
</ul>
```

위 예제에서는 번호가 붙지 않은 리스트가 루트 엘리먼트이며 그 엘리먼트에는 6 개의 자식 엘리먼트가 있습니다. 이 `ul` 과 자식을 `React.createElement` 로 나타낼 수 있습니다.

```js
React.createElement(
 "ul",
 null,
 React.createElement("li", null, "1 lb Salmon"),
 React.createElement("li", null, "1 cup Pine Nuts"),
 React.createElement("li", null, "2 cups Butter Lettuce"),
 React.createElement("li", null, "1 Yellow Squash"),
 React.createElement("li", null, "1/2 cup Olive Oil"),
 React.createElement("li", null, "3 cloves of Garlic")
)
```

위 호출의 결과로 생기는 React 엘리먼트를 보면 React 엘리먼트로 표현한 각 원소가 `props.children` 배열 안에 들어 있는 모습을 볼 수 있습니다. 실제로 결과 엘리먼트를 알아보겠습니다.

```json
{
    "type": "ul",
    "props": {
        "children": [
            { "type": "li", "props": { "children": "1 lb Salmon" } … },
            { "type": "li", "props": { "children": "1 cup Pine Nuts"} … },
            { "type": "li", "props": { "children": "2 cups Butter Lettuce" } … },
            { "type": "li", "props": { "children": "1 Yellow Squash"} … },
            { "type": "li", "props": { "children": "1/2 cup Olive Oil"} … },
            { "type": "li", "props": { "children": "3 cloves of Garlic"} … }
        ]
    ...
    }
}
```

이제 리스트의 각 원소가 자식으로 들어간 모습을 볼 수 있습니다. [The Virtual DOM](#the-virtual-dom) 에서 본 예제를 React 를 사용해 만들려면 다음과 같이 호출해야 합니다.

```js
React.createElement("section", {id: "baked-salmon"},
    React.createElement("h1", null, "Baked Salmon"),
    React.createElement("ul", {"className": "ingredients"},
        React.createElement("li", null, "1 lb Salmon"),
        React.createElement("li", null, "1 cup Pine Nuts"),
        React.createElement("li", null, "2 cups Butter Lettuce"),
        React.createElement("li", null, "1 Yellow Squash"),
        React.createElement("li", null, "1/2 cup Olive Oil"),
        React.createElement("li", null, "3 cloves of Garlic")
    ),
    React.createElement("section", {"className": "instructions"},
        React.createElement("h2", null, "Cooking Instructions"),
        React.createElement("p", null, "Preheat the oven to 350 degrees."),
        React.createElement("p", null,
        "Spread the olive oil around a glass baking dish."),
        React.createElement("p", null, "Add the salmon, garlic, and pine..."),
        React.createElement("p", null, "Bake for 15 minutes."),
        React.createElement("p", null, "Add the yellow squash and put..."),
        React.createElement("p", null, "Remove from oven and let cool for 15 ....")
    )
)
```

순수 리액트는 결국 브라우저에서 생성됩니다. 가상 DOM 은 단일 루트로부터 뻗어 나온 React 엘리먼트의 트리입니다. React 엘리먼트는 React 가 브라우저에서 UI 를 어떻게 구성할 지 지시하는 명령입니다.

## Constructing Elements with Data 

React 사용의 장점은 UI 엘리먼트와 데이터를 분리할 수 있다는 것입니다. React 는 단순한 JavaScript 이기 때문에 React 컴포넌트 트리를 더 편하게 구성하기 위해 JavaScript 로직을 얼마든지 추가할 수 있습니다.

예를 들어 배열에 재료를 저장하고 그 배열을 React 엘리먼트로 `map` 할 수 있습니다.

```js
React.createElement("ul", {"className": "ingredients"},
    React.createElement("li", null, "1 lb Salmon"),
    React.createElement("li", null, "1 cup Pine Nuts"),
    React.createElement("li", null, "2 cups Butter Lettuce"),
    React.createElement("li", null, "1 Yellow Squash"),
    React.createElement("li", null, "1/2 cup Olive Oil"),
    React.createElement("li", null, "3 cloves of Garlic")
);
```

이 데이터를 JavaScript 배열로 간단하게 표현할 수 있습니다.

```js
var items = [
    "1 lb Salmon",
    "1 cup Pine Nuts",
    "2 cups Butter Lettuce",
    "1 Yellow Squash",
    "1/2 cup Olive Oil",
    "3 cloves of Garlic"
]
```

이제 `Array.map` 함수를 사용해 간편하게 가상 DOM 을 구현할 수 있습니다.

```js
React.createElement(
    "ul",
    { className: "ingredients" },
    items.map(ingredient =>
        React.createElement("li", null, ingredient)
    )
)
```

이 코드를 실행하면 콘솔에서 `Example 2` 와 같은 경고를 볼 수 있습니다.

> Example 2 - Console warning

![image](https://user-images.githubusercontent.com/44635266/77137677-3b4f5800-6ab2-11ea-8f80-15195944bf2b.png)

배열을 이터레이션해서 자식 엘리먼트의 리스트를 만드는 경우 React 에서는 각 자식 엘리먼트에 `key` 프로퍼티를 넣을 것을 권장합니다. React 는 `key` 를 사용해 DOM 을 효율적으로 갱신할 수 있습니다.

각 `li` 엘리먼트에 고유 키를 부여해보겠습니다.

```js
React.createElement("ul", {className: "ingredients"},
 items.map((ingredient, i) =>
 React.createElement("li", { key: i }, ingredient)
)
```

## React Components 

모든 사용자 인터페이스는 여러 부분으로 이루어집니다. 아래 에서 보여주는 조리법 예제도 각 부분을 이루는 몇 가지 조리법이 있습니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/77138083-cd0b9500-6ab3-11ea-994b-fe0e508478f6.png)

React 에서 이 부분을 각 컴포넌트라고 부릅니다. 컴포넌트를 사용하면 서로 다른 데이터 집합에 같은 DOM 구조를 재사용할 수 있습니다.

React 로 만들고 싶은 인터페이스를 생각할 떄는 엘리먼트를 재사용 가능한 조각으로 나눌 수 있는지 고려해야합니다. 예를 들어 `Example 4` 조리법에는 각각 제목, 재료 리스트, 조리 절차가 들어 있습니다. 그림에서 사각형으로 표시한 각 부분에 해당하는 컴포넌트를 만들 수 있습니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/77138092-d5fc6680-6ab3-11ea-8e97-4b8dab127a67.png)

### createClass 

`React.createClass` 를 사용해React 컴포넌트를 만들 수 있습니다.

```js
const IngredientsList = React.createClass({
    displayName: "IngredientsList",
    render() {
        return React.createElement("ul", {"className": "ingredients"},
            React.createElement("li", null, "1 lb Salmon"),
            React.createElement("li", null, "1 cup Pine Nuts"),
            React.createElement("li", null, "2 cups Butter Lettuce"),
            React.createElement("li", null, "1 Yellow Squash"),
            React.createElement("li", null, "1/2 cup Olive Oil"),
            React.createElement("li", null, "3 cloves of Garlic")
        )
    }
})

const list = React.createElement(IngredientsList, null, null)

ReactDOM.render(
    list,
    document.getElementById('react-container')
)
```

컴포넌트를 사용하면 데이터로부터 재사용 가능한 UI 를 만들 수 잇습니다. `render` 함수에서 `this` 키워드를 사용해 컴포넌트 인스턴스를 가리킬 수 있고 그 인스턴스의 프로퍼티를 `this.props` 로 접근할 수 있습니다.

아래 예제에서는 컴포넌트를 만들고 이름을 `IngredientsList` 로 정했습니다.

```js
<IngredientsList>
    <ul className="ingredients">
        <li>1 lb Salmon</li>
        <li>1 cup Pine Nuts</li>
        <li>2 cups Butter Lettuce</li>
        <li>1 Yellow Squash</li>
        <li>1/2 cup Olive Oil</li>
        <li>3 cloves of Garlic</li>
    </ul>
</IngredientsList>
```

React 컴포넌트에 데이터를 넘길 때는 프로퍼티로 넘깁니다. 재사용 가능한 재료 리스트를 만들기 위해 재료들이 들어 있는 배열을 이 컴포넌트에 넘길 수 있습니다.

```js
const IngredientsList = React.createClass({
    displayName: "IngredientsList",
    render() {
        return React.createElement("ul", {className: "ingredients"},
            this.props.items.map((ingredient, i) =>
                React.createElement("li", { key: i }, ingredient)
            )
        )
    }
})

const items = [
    "1 lb Salmon",
    "1 cup Pine Nuts",
    "2 cups Butter Lettuce",
    "1 Yellow Squash",
    "1/2 cup Olive Oil",
    "3 cloves of Garlic"
]

ReactDOM.render(
    React.createElement(IngredientsList, {items}, null),
    document.getElementById('react-container')
)
```

이제 ReactDOM 을 살펴보겠습니다. `items` 라는 데이터 프로퍼티는 6 가지 재료가 들어 있는 배열입니다. `map` 을 사용해 `li` 태그를 만들면서 배열 인덱스를 `li` 태그의 고유 키로 지정햇습니다.

```js
<IngredientsList items=[...]>
    <ul className="ingredients">
        <li key="0">1 lb Salmon</li>
        <li key="1">1 cup Pine Nuts</li>
        <li key="2">2 cups Butter Lettuce</li>
        <li key="3">1 Yellow Squash</li>
        <li key="4">1/2 cup Olive Oil</li>
        <li key="5">3 cloves of Garlic</li>
    </ul>
</IngredientsList>
```

컴포넌트는 객체입니다. 따라서 일반 JavaScript 클래스와 마찬가지로 내부에 코드를 캡슐화할 수 있습니다. 따라서 리스트 원소를 하나 생성하는 메소드를 만들어서 리스트를 만들 떄 사용할 수 있습니다.


```js
const IngredientsList = React.createClass({
    displayName: "IngredientsList",
    renderListItem(ingredient, i) {
        return React.createElement("li", { key: i }, ingredient)
    },
    render() {
    return React.createElement("ul", {className: "ingredients"},
        this.props.items.map(this.renderListItem)
        )
    }
})
```

위 구현은 MVC 프레임워크의 핵심 아이디어이기도 합니다. `IngredientsList` 에서 UI 와 관계있는 부분은 모두 한 컴포넌트 안에 캡슐화됩니다.

이렇게 컴포넌트를 사용해 React 엘리먼트를 만들 수 있고, 그 컴포넌트에 재료 리스트를 프로퍼티로 전달할 수 있습니다. 컴포넌트를 사용해 만들어진 엘리먼트를 쓸 떄는 문자열이 아닌 컴포넌트 클래스를 직접 쓴다는 점에 유의해야합니다.

`IngredientsList` 컴포넌트에 데이터를 전달해 렌더링하면 다음과 같은 DOM 이 생깁니다.

```js
<ul data-react-root class="ingredients">
    <li>1 lb Salmon</li>
    <li>1 cup Pine Nuts</li>
    <li>2 cups Butter Lettuce</li>
    <li>1 Yellow Squash</li>
    <li>1/2 cup Olive Oil</li>
    <li>3 cloves of Garlic</li>
</ul>
```

### Component

ES6 의 명세의 핵심 특징 중 하나는 클래스 선언입니다. React 컴포넌트를 새로 만들 때는 `React.Component` 를 추상 클래스로 사용할 수 있습니다. ES6 구문으로 이 추상 클래스를 상속하면 커스텀 컴포넌트를 만들 수 있습니다. `IngredientsList` 도 마찬가지 방법으로 만들 수 있습니다.

```js
class IngredientsList extends React.Component {
 
    renderListItem(ingredient, i) {
        return React.createElement("li", { key: i }, ingredient)
    }
    
    render() {
        return React.createElement("ul", {className: "ingredients"},
            this.props.items.map(this.renderListItem)
        )
    }
}
```

### Stateless Functional Components 

상태가 없는 함수형 컴포넌트는 객체가 아니라 함수입니다. 따라서 컴포넌트 영역에는 `this` 가 없습니다.

상태가 없는 함수형 컴포넌트는 프로퍼티를 인자로 받아 DOM 엘리먼트를 반환하는 함수입니다. 각각의 상태가 없는 함수형 컴포넌트를 순수 함수로 만들어야합니다. 이들은 프로퍼티를 인자로 받아서 부수 효과 없이 결과 DOM 엘리먼트를 만들어냅니다. 그러므로 코드가 단순해지고 훨씬 더 테스트하기 쉽습니다.

아래 예제는 `renderListItem` 과 `render` 의 기능을 한 함수로 엮습니다.

```js
const IngredientsList = props =>
    React.createElement("ul", {className: "ingredients"},
        props.items.map((ingredient, i) =>
            React.createElement("li", { key: i }, ingredient)
        )
    )
```

이 컴포넌트를 `createClass` 나 ES6 클래스 구문으로 만든 컴포넌트를 렌더링할 떄와 마찬가지로 `ReactDOM.render` 로 렌더링할 수 있습니다. 이 컴포넌트는 단지 함수에 불과합니다. 이 함수는 `props` 를 인자로 받아서 `props` 안에 있는 데이터가 원소인 원소인 번호가 붙어있지 않은 리스트를 만들어 반환합니다.

이 함수형 컴포넌트를 개선하는 방법은 `props` 를 구조 분해하는 것입니다. ES6 를 사용하면 프로퍼티의 리스트를 바로 함수에서 사용할 수 있어서 점(`.`) 구문을 사용해 프로퍼티에 접근할 필요가 없어집니다.

이 `IngredientsList` 도 일반 컴포넌트 클래스를 렌더링하는 것과 같은 방식으로 렌더링할 수 있습니다.

```js
const IngredientsList = ({items}) =>
    React.createElement("ul", {className: "ingredients"},
        items.map((ingredient, i) =>
            React.createElement("li", { key: i }, ingredient)
        )
    )
```

## DOM Rendering 

어플리케이션에 있는 모든 데이터를 한 JavaScript 객체에 저장했을 때, 이 객체를 변경할 때마다 그 객체를 컴포넌트에 프로퍼티로 전달하고 UI 를 렌더링해야 합니다. 이는 `ReactDOM.render` 가 대부분의 무거운 작업을 처리해야 하는 뜻입니다.

React 수긍할만한 시간 안에 작동하게 만들기 위해 `ReactDOM.render` 는 더 영리하게 작동합니다. 전체 DOM 을 없애고 재구축하는 대신 `ReactDOM.render` 는 현재의 DOM 을 남겨둔 채 가능한 한 DOM 을 작게 변경하면서 새로운 UI 를 만듭니다.

다섯 팀원의 기분을 표시하는 앱이 잇다고 하겠습니다. 이 기분을 배열로 표현할 수 있습니다.

```js
["smile", "smile", "frown", "smile", "frown"];
```

![image](https://user-images.githubusercontent.com/44635266/77140805-1b259600-6abe-11ea-96d2-eb6a43ea194a.png)

이 배열을 사용해 다음과 같은 UI 를 만들 수 있습니다.

```js
["frown", "frown", "frown", "frown", "frown"];
```

![image](https://user-images.githubusercontent.com/44635266/77140868-4b6d3480-6abe-11ea-95cf-7bb9692dd711.png)

주말에도 팀원들이 일을 해야 한다면 팀원들의 기분을 반영할 수 있습니다.

첫 번째 배열을 두 번째 배열처럼 변경하려면 총 3 번 데이터를 변경해야합니다.

```js
["smile", "smile", "frown", "smile", "frown"];

["frown", "frown", "frown", "frown", "frown"];
```

이제 이런 변경을 반영하기 위해 DOM 을 어떻게 갱신하는지 살펴보겠습니다. UI 를 바꾸는 한가지 비효율적인 방법은 아래 예제처럼 전체 DOM 을 지우고 재구성하는 것입니다.

```js
<ul>
  <li class="smile">smile</li>
  <li class="smile">smile</li>
  <li class="frown">frown</li>
  <li class="smile">smile</li>
  <li class="frown">frown</li>
</ul>
```

1. 모든 데이터를 지운다.

```js
<ul>
</ul>
```

2. 데이터를 이터레이션하고, 첫 번째 리스트 원소를 만든다.

```js
<ul>
   <li class="frown">frown</li>
</ul>
```

3. 두 번째 리스트 원소를 만들어 추가한다.

```js
<ul>
    <li class="frown">frown</li>
    <li class="frown">frown</li>
</ul>
```

4. 마지막 원소까지 만들어 추가한다.

```js
<ul>
   <li class="frown">frown</li>
   <li class="frown">frown</li>
   <li class="frown">frown</li>
   <li class="frown">frown</li>
   <li class="frown">frown</li>
</ul>
```

DOM 을 지우고 다시 만든다면 5 개의 DOM 엘리먼트를 만들어 삽입해야 합니다. 엘리먼트를 DOM 에 삽입하는 것은 DOM API 연산 중 가장 비싼 연산입니다. 즉, DOM 엘리먼트 삽입은 느립니다. 하지만, 제 위치에 있는 DOM 엘리먼트를 갱신하면 새로운 엘리먼트를 삽입하는 것보다 빠릅니다.

`ReactDOM.render` 는 현재 DOM 을 그대로 두고 갱신이 필요한 DOM 엘리먼트만 변경합니다. 예제에서는 3 부분이 변경됩니다. 따라서 `ReactDOM.render 는 세 DOM 엘리먼트만 변경하면 됩니다.

> Example 5 - Three DOM elements are updated

![image](https://user-images.githubusercontent.com/44635266/77141067-f8e04800-6abe-11ea-93f2-ed5ed974e71c.png)

## Factories 

지금까지는 `React.createElement` 만 사용했습니다. 하지만 **팩토리(Factory)** 를 사용해 React 엘리먼트를 만들 수 있습니다. `factory` 는 객체를 인스턴스화하는 자세한 과정을 감추고 객체 생성 과정을 추상화해주는 특별한 객체입니다.

React 에서는 엘리먼트 인스턴스를 만들 때 팩토리를 사용합니다.

React 는 흔히 쓰이는 HTML 과 SVG DOM 엘리먼트를 만들어주는 팩토리를 기본으로 제공합니다. `React.createFactory` 함수를 사용하면 컴포넌트를 만들어주는 팩토리를 사용자가 만들 수 있습니다.

앞에서 본 `h1` 엘리먼트를 보겠습니다.

```js
<h1>Baked Salmon</h1>
```

`createElement` 대신 내장 팩토리를 사용해 React 엘리먼트를 만들 수 있습니다.

```js
ReactDOMFactories.h1(null, "Baked Salmon")
```

첫 번째 인자는 프로퍼티고 두 번째 인자는 자식 노드입니다. DOM 팩토리를 아래 예제처럼 사용하면 번호가 붙지 않은 리스트를 만들 수 있습니다.

```js
React.DOM.ul({"className": "ingredients"},
    React.DOM.li(null, "1 lb Salmon"),
    React.DOM.li(null, "1 cup Pine Nuts"),
    React.DOM.li(null, "2 cups Butter Lettuce"),
    React.DOM.li(null, "1 Yellow Squash"),
    React.DOM.li(null, "1/2 cup Olive Oil"),
    React.DOM.li(null, "3 cloves of Garlic")
)
```

`ul` 의 첫 번째 인자는 프로퍼티며 이 경우 `className` 을 정의합니다. 두 번째부터 추가된 인자는 `ul` 의 `children` 배열에 들어갈 자식 엘리먼트들입니다. 방금 본 팩토리를 사용한 리스트 정의를 개선해 재료 데이터를 분리할 수 있습니다.

```js
var items = [
   "1 lb Salmon",
   "1 cup Pine Nuts",
   "2 cups Butter Lettuce",
   "1 Yellow Squash",
   "1/2 cup Olive Oil",
   "3 cloves of Garlic"
]

var list = React.DOM.ul(
    { className: "ingredients" },
    items.map((ingredient, key) =>
        React.DOM.li({key}, ingredient)
    )
)

ReactDOM.render(
   list,
   document.getElementById('react-container')
)
```

### Using Factories with Components

컴포넌트를 함수로 마늗ㄹ어 코드를 단순화하고 싶다면 팩토리를 마늗ㄹ어야 합니다.

```js
const { render } = ReactDOM;

const IngredientsList = ({ list }) =>
    React.createElement('ul', null,
        list.map((ingredient, i) =>
            React.createElement('li', {key: i}, ingredient)
    )
)

const Ingredients = React.createFactory(IngredientsList)

const list = [
    "1 lb Salmon",
    "1 cup Pine Nuts",
    "2 cups Butter Lettuce",
    "1 Yellow Squash",
    "1/2 cup Olive Oil",
    "3 cloves of Garlic"
]

render(
    Ingredients({list}),
    document.getElementById('react-container')
)
```

`Ingredients` 팩토리를 사용해 React 엘리먼트를 빠르게 렌더링할 수 있습니다. `Ingredients` 는 다른 DOM 팩토리와 마찬가지로 프로퍼티와 자식 노드를 인자로 받습니다.

JSX 를 다루지 않는다면 `React.createElement` 를 반복 호출하는 것보다 팩토리를 사용하는게 더 좋습니다.