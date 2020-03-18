---
title : React Emerging JavaScript
tags :
- ES6
- JavaScript
- React
---

*이 포스트는 [Learning React](https://www.imel.ba/edukacija/learningreact1.pdf) 를 바탕으로 작성하였습니다.*

JavaScript 의 변화를 주도하는 기관이 바로 ECMA(European Computer Manufacturers Association) 입니다.

JavaScript 의 명세는 2015 년 6 월에 개정되었으며 ECMAScript 6, ES6, ES2015 등 다양한 이름으로 불립니다. 이 ES6 문법에 대해 알아보겠습니다.

## Declaring Variables in ES6

ES6 이전에는 `var` 키워드가 변수를 선언하는 유일한 방법이였습니다. 하지만 몇 가지 기능이 더 추가되었습니다.

### const

**상수(Constant)** 는 값을 변경할 수 없는 변수입니다.

상수가 없던 시절에는 모든 값을 변수에 넣어 사용했습니다. 하지만 변수는 값을 변경할 수 있습니다.

```js
var pizza = true
pizza = false
console.log(pizza) // false
```

상수에 값을 재 설정하는 것은 불가능합니다. 따라서 값을 변경하려면 콘솔 오류가 발생합니다.

```js
const pizza = true
pizza = false
```

```js
Uncaught TypeError: Assignment to constant variable.
    at <anonymous>:1:7
```

### let

JavaScript 에서도 이제 **구문적인 변수 영역 규칙(Lexical Variable Scoping)** 을 지원합니다. JavaScript 에서는 중괄호 `{}` 를 사용해 코드 블록을 만듭니다. 함수의 경우 이런 코드 블록의 변수 영역을 이룹니다. 하지만 `if/else` 문 경우는 다릅니다.

`if/else` 블록 안에서 변수를 새로 만드면 그 변수의 영역이 블록 안으로만 한정되지 않습니다.

```js
var topic = "JavaScript"
console.log(topic) // JavaScript

if (topic) {
    var topic = "React"
    console.log('block', topic) // block React
}

console.log('global', topic) // global React
```

`if` 블록 안의 `topic` 변수의 값을 변경하면 블록 밖의 `topic` 변수 값도 변경됩니다.

`let` 키워드를 사용하면 변수 영역을 코드 블록 안으로 한정시킬 수 있습니다. 그러므로 글로벌 변수의 값을 보호할 수 있습니다.

```js
var topic = "JavaScript"

if (topic) {
    let topic = "React"
    console.log('block', topic) // React
}

console.log('global', topic) // JavaScript
```

`if` 블록 안의 `topic` 을 변경해도 블록 밖의 `topic` 에는 아무런 영향이 없습니다.

```js
var div, container = document.getElementById('container')

for (var i=0; i<5; i++) {
    div = document.createElement('div')
    div.onclick = function() {
        alert('This is box #' + i)
        }
    container.appendChild(div)
}
```

이 루프에서는 컨테이너 안에 5 개의 `div` 만듭니다. 각 `div` 에는 경고창을 표시해주는 `onclick` 핸들러가 할당됩니다. `for` 루프 안에 `i` 를 선언해도 글로벌 영역에 `i` 가 생성되므로 5 개의 박스 중 어느것을 클릭하건 `i` 값은 5 이기 때문에 표시되는 인덱스는 모두 같습니다.

> Example 1 - i is equal to 5 for each box

![image](https://user-images.githubusercontent.com/44635266/76811007-6aa46180-6833-11ea-9b56-6ed7d1334f5e.png)

`var` 대신 `let` 을 사용해 선언하면 `i` 의 영역이 블록으로 제한됩니다. 각 박스를 클릭하면 정상적으로 표시가 됩니다.

```js
var div, container = document.getElementById('container')

for (let i=0; i<5; i++) {
    div = document.createElement('div')
    div.onclick = function() {
        alert('This is box #: ' + i)
    }
    container.appendChild(div)
}
```

> Example 2 - The scope of i is protected with let

![image](https://user-images.githubusercontent.com/44635266/76811022-73953300-6833-11ea-932c-06c5b68b47e0.png)

### Template Strings 

**템플릿 문자열(Template String)** 을 문자열 연결 대신 사용할 수 있습니다. 그러면 문자열 중간에 변수를 삽입할 수 있습니다.

기존 방식은 `+` 기호로 문자열과 변수를 이어붙이는 방식입니다.

```js
console.log(lastName + ", " + firstName + " " + middleName)
```

템플릿 문자열에선 `${}` 를 사용해 문자열안에 변수를 집어넣을 수 있기 떄문에 문자열을 하나만 사용해도 됩니다.

```js
console.log(`${lastName}, ${firstName} ${middleName}`)
```

템플릿 문자열은 공백을 유지합니다. 따라서 코드가 깨질 염려 없이 여러 줄로 된 문자열을 만들 수 있습니다.

```js
`
Hello ${firstName},
Thanks for ordering ${qty} tickets to ${event}.

Order Details:
    ${firstName} ${middleName} ${lastName}
    ${qty} x $${price} = $${qty*price} to ${event}

You can pick your tickets up at will call 30 minutes before the show.

Thanks,

${ticketAgent}
`
```

이렇게 정렬된 HTML 을 코드에 넣을 수 있습니다.

```js
document.body.innerHTML = `
<section>
    <header>
        <h1>The HTML5 Blog</h1>
    </header>
    <article>
        <h2>${article.title}</h2>
        ${article.body}
    </article>
    <footer>
        <p>copyright ${new Date().getYear()} | The HTML5 Blog</p>
    </footer>
</section>`
```

여기서도 페이지 제목과 본문에 변수를 포함시킬 수 있는걸 확인하면 됩니다.

### Default Parameters 

C++ 나 Python 같은 언어에서는 함수의 인자로 디폴트 값을 선언할 수 있습니다. ES6 명세에도 **디폴트 파라미터(Default Parameter)** 가 추가되었습니다. 함수를 호출하면서 값을 지정하지 않으면 디폴트 값이 사용됩니다.

다음과 같이 사용할 수 있습니다.

```js
function logActivity(name="Shane McConkey", activity="skiing") {
    console.log( `${name} loves ${activity}` )
}
```

logActivity 함수를 호출하면서 인자를 지정하지 않아도 디폴트 값을 사용해 함수가 정상적으로 실행이 됩니다. 다른 타입의 값도 사용할 수 있습니다.

```js
var defaultPerson = {
    name: {
    first: "Shane",
        last: "McConkey"
    },
    favActivity: "skiing"
}
function logActivity(p=defaultPerson) {
    console.log(`${p.name.first} loves ${p.favActivity}`)
}
```

## Arrow Functions 

**화살표 함수(Arrow Function)** 은 ES6 에 새로 추가된 유용한 기능입니다. 이를 사용하면 `function` 없이도 함수를 만들 수 있으며, `return` 을 사용하지 않아도 식을 계산한 값이 자동으로 반환됩니다.

아래는 기존의 함수 선언 구문입니다.

```js
var lordify = function(firstname) {
    return `${firstname} of Canterbury`
}

console.log( lordify("Dale") ) // Dale of Canterbury
console.log( lordify("Daryle") ) // Daryle of Canterbury
```

화살표 함수를 사용하면 간단하게 만들 수 있습니다.

```js
var lordify = firstname => `${firstname} of Canterbury`
```

파라미터가 2 개 이상이라면 괄호가 필요합니다.

```js
// Old
var lordify = function(firstName, land) {
    return `${firstName} of ${land}`
}

// New
var lordify = (firstName, land) => `${firstName} of ${land}`
console.log( lordify("Dale", "Maryland") ) // Dale of Maryland
console.log( lordify("Daryle", "Culpeper") ) // Daryle of Culpeper
```

반환한 결과를 ㄴ나타내는 식 하나만으로 충분했기 떄문에 화살표 함수 정의를 한 줄로 끝냈습니다.

하지만 결과를 계산하기 위해 여러 줄을 사용해야 한다면 함수 본문 전체를 중괄호로 둘러싸야 합니다.

```js
// Old
var lordify = function(firstName, land) {

    if (!firstName) {
        throw new Error('A firstName is required to lordify')
    }

    if (!land) {
        throw new Error('A lord must have a land')
    }

    return `${firstName} of ${land}`
}

// New
var lordify = (firstName, land) => {

    if (!firstName) {
        throw new Error('A firstName is required to lordify')
    }

    if (!land) {
        throw new Error('A lord must have a land')
    }

    return `${firstName} of ${land}`
}

console.log( lordify("Kelly", "Sonoma") ) // Kelly of Sonoma
console.log( lordify("Dave") ) // ! JAVASCRIPT ERROR
```

화살표 함수는 `this` 를 새로 바인딩하지 않습니다. 예를 들어 아래 코드에 `this` 는 `tahoe` 객체가 아닙니다.

```js
var tahoe = {
    resorts: ["Kirkwood","Squaw","Alpine","Heavenly","Northstar"],
    print: function(delay=1000) {
        setTimeout(function() {
            console.log(this.resorts.join(", "))
        }, delay)
    }
}

tahoe.print() // Cannot read property 'join' of undefined
```

위 경우 `this` 가 `window` 객체이기 때문에 `resorts` 가 `undefined` 입니다. 이 방법 대신 화살표 함수를 사용하면 `this` 영역이 제대로 유지가 됩니다.

```js
var tahoe = {
    resorts: ["Kirkwood","Squaw","Alpine","Heavenly","Northstar"],
    print: function(delay=1000) {
        setTimeout(() => {
            console.log(this.resorts.join(", "))
        }, delay)
    }
}

tahoe.print() // Kirkwood, Squaw, Alpine, Heavenly, Northstar
```

화살표 함수는 새로운 영역을 만들어내지 않습니다.

```js
var tahoe = {
    resorts: ["Kirkwood","Squaw","Alpine","Heavenly","Northstar"],
    print: (delay=1000) => {
        setTimeout(() => {
            console.log(this.resorts.join(","))
        }, delay)
    }
}

tahoe.print() // Cannot read property resorts of undefined
```

`print` 프로퍼티를 화살표 함수로 바꾼다는 것은 `this` 가 `window` 객체가 된다는 뜻입니다.

이를 검증하기 위해 `this` 가 `window` 인지 여부를 콘솔에 추가할 수 있습니다.

```js
var tahoe = {
    resorts: ["Kirkwood","Squaw","Alpine","Heavenly","Northstar"],
    print: (delay=1000)=> {
        setTimeout(() => {
            console.log(this === window)
        }, delay)
    }
}

tahoe.print() // true
```

결과는 `true` 입니다. 이 문제를 해결하려면 화살표가 아니라 `function` 을 사용해 정의한 함수를 사용해야 합니다.

```js
var tahoe = {
    resorts: ["Kirkwood","Squaw","Alpine","Heavenly","Northstar"],
    print: function(delay=1000) {
        setTimeout(() => {
            console.log(this === window)
        }, delay)
    }
}

tahoe.print() // false
```

## Transpiling ES6 

모든 웹 브라우저가 ES6 를 지원하지는 않습니다. 그렇기 때문에 브라우저에서 ES6 코드를 실행하기 전에 ES5 로 컴파일하면 ES6 가 작동하도록 보장할 수 있습니다. 이런 변환을 **트랜스파일링(Transpiling)** 이라 하며 가장 유명한 도구로는 **바벨(Babel)** 입니다.

아래 예제는 화살표 함수 입니다.

```js
const add = (x=5, y=10) => console.log(x + y)
```

이 코드를 트랜스파일러로 변환하면 다음과 같은 출력이 생깁니다.

```js
"use strict";

var add = function add() {
    var x = arguments.length <= 0 || arguments[0] === undefined ? 5 : arguments[0];
    var y = arguments.length <= 1 || arguments[1] === undefined ? 10 : arguments[1];
    return console.log(x + y);
};
```

트랜스파일러는 `use strict` 선언을 추가해 코드가 엄격한 모드에서 실행되도록 만듭니다. `x` 와 `y` 파라미터의 디폴트 값은 `arguments` 배열로 처리됩니다.

인라인 바벨 트랜스파일러를 사용하면 브라우저에서 JavaScript 를 직접 트랜스파일 할 수도 있습니다. 단지 `browser.js` 파일을 포함시키고, 변환하고 싶은 코드의 `script` 태그에 `type="text/babel"` 을 지정하면 됩니다.

```js
<script
    src="https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.23/browser.js">
</script>
<script src="script.js" type="text/babel">
</script>
```

## ES6 Objects and Arrays 

ES6 는 객체와 배열을 다루는 방법과 객체와 배열 안에서 변수의 영역을 제한하는 방법을 다양하게 제공합니다. 그러한 기능으로는 구조 분해, 객체 리터럴 개선, 스프레드 연산자 등이 있습니다.

### Destructuring Assignment 

**구조 분해(Destructing)** 를 사용하면 객체 안에 있는 필드 값을 원하는 변수에 대입할 수 있습니다.

다음은 `sandwich` 객체를 사용한 예제입니다.

```js
var sandwich = {
    bread: "dutch crunch",
    meat: "tuna",
    cheese: "swiss",
    toppings: ["lettuce", "tomato", "mustard"]
}

var {bread, meat} = sandwich

console.log(bread, meat) // dutch crunch tuna
```

이 코드는 `sandwich` 를 분해해서 `bread` 와 `meat` 필드를 같은 이름의 변수에 넣어줍니다. 두 변수의 값은 `sandwich` 에 있는 같은 이름의 필드 값으로 초기화되지만, 두 변수를 변경해도 원래의 필드 값은 바뀌지 않습니다.

```js
var {bread, meat} = sandwich

bread = "garlic"
meat = "turkey"

console.log(bread) // garlic
console.log(meat) // turkey

console.log(sandwich.bread, sandwich.meat) // dutch crunch tuna
```

객체를 분해해서 함수의 인자로 넘길 수도 있습니다. 어떤 사람의 이름을 귀족처럼 표현하는 함수를 보겠습니다.

```js
var lordify = regularPerson => {
    console.log(`${regularPerson.firstname} of Canterbury`)
}

var regularPerson = {
    firstname: "Bill",
    lastname: "Wilson"
}

lordify(regularPerson) // Bill of Canterbury
```

객체의 필드에 접근하기 위해 점(.) 과 필드 이름을 사용하는 대신 `regularPerson` 에 필요한 값을 구조 분해로 가져올 수 있습니다.

```js
var lordify = ({firstname}) => {
    console.log(`${firstname} of Canterbury`)
}

lordify(regularPerson) // Bill of Canterbury
```

구조 분해는 더 선언적입니다. 따라서 코드를 작서앟ㄴ 사람의 의도를 더 잘 설명해줍니다. 구조 분해를 `firstname` 을 가져와서 객체이 필드 중 `firstname` 만 사용한다는 사실을 선언합니다.

배열을 구조 분해해서 원소의 값을 변수에 대입할 수 있습니다. 배열의 첫 번째 원소를 변수에 대입한다고 하겠습니다.

```js
var [firstResort] = ["Kirkwood", "Squaw", "Alpine"]
console.log(firstResort) // Kirkwood
```

불필요한 값을 콤마(,) 를 사용해 생략하는 리스트 매칭을 사용할 수 있습니다. 위 배열에서 첫 두 원소를 콤마로 대치하면 다음과 같습니다.

```js
var [,,thirdResort] = ["Kirkwood", "Squaw", "Alpine"]
console.log(thirdResort) // Alpine
```

### Object Literal Enhancement

**객체 리터럴 개선(Object Literal Enhancement)** 은 구조 분해의 반대입니다. 객체 리터럴 개선은 구조를 다시 묶는 과정이라 할 수 있습니다.

객체 리터럴 개선을 사용하면 현재 영역에 있는 변수를 객체의 필드로 묶을 수 있습니다.

```js
var name = "Tallac"
var elevation = 9738

var funHike = {name,elevation}

console.log(funHike) // {name: "Tallac", elevation: 9738}
```

이제 `funHike` 객체는 `name` 과 `elevation` 필드가 들어 있습니다.

객체 리터럴 개선 또는 객체 재구축으로 객체 메서드를 만드는 것도 가능합니다.

```js
var name = "Tallac"
var elevation = 9738
var print = function() {
    console.log(`Mt. ${this.name} is ${this.elevation} feet tall`)
}

var funHike = {name,elevation,print}

funHike.print() // Mt. Tallac is 9738 feet tall
```

이때 객체의 키에 접근하기 위해 `this` 를 사용했습니다. 객체 메서드에 정의할 때는 더 이상 `function` 키워드를 사용하지 않아도 됩니다.

```js
// OLD
var skier = {
    name: name,
    sound: sound,
    powderYell: function() {
        var yell = this.sound.toUpperCase()
        console.log(`${yell} ${yell} ${yell}!!!`)
    },
    speed: function(mph) {
    this.speed = mph
    console.log('speed:', mph)
    }
}

// NEW
const skier = {
    name,
    sound,
    powderYell() {
        let yell = this.sound.toUpperCase()
        console.log(`${yell} ${yell} ${yell}!!!`)
    },
    speed(mph) {
        this.speed = mph
        console.log('speed:', mph)
    }
}
```

### The Spread Operator

**스프레드 연산자(Spread Operator)** 는 세 개의 점으로 이루어진 연산자입니다. 배열의 내용을 조합할 수 있습니다. 예를 들어, 아래와 같이 사용할 수 있습니다.

```js
var peaks = ["Tallac", "Ralston", "Rose"]
var canyons = ["Ward", "Blackwood"]
var tahoe = [...peaks, ...canyons]

console.log(tahoe.join(', ')) // Tallac, Ralston, Rose, Ward, Blackwood
```

`peeks` 배열을 `Array.reverse` 메소드를 이용해 요소를 뒤집어 보겠습니다.

```js
var peaks = ["Tallac", "Ralston", "Rose"]
var [last] = peaks.reverse()

console.log(last) // Rose
console.log(peaks.join(', ')) // Rose, Ralston, Tallac
```

여기서 문제는 원본 배열도 변경합니다. 하지만 스프레드 연산자를 사용하면 원본 배열을 변경하지 않고 복사본을 만들어 뒤집을 수 있습니다.

```js
var peaks = ["Tallac", "Ralston", "Rose"]
var [last] = [...peaks].reverse()

console.log(last) // Rose
console.log(peaks.join(', ')) // Tallac, Ralston, Rose
```

스프레드 연산자로 배열의 나머지 원소를 얻을 수 있습니다.

```js
var lakes = ["Donner", "Marlette", "Fallen Leaf", "Cascade"]
var [first, ...rest] = lakes

console.log(rest.join(", ")) // "Marlette, Fallen Leaf, Cascade"
```

스프레드 연산자를 사용해 함수의 인자를 배열로 모을 수 있습니다.

```js
function directions(...args) {
    var [start, ...remaining] = args
    var [finish, ...stops] = remaining.reverse()

    console.log(`drive through ${args.length} towns`)
    console.log(`start in ${start}`)
    console.log(`the destination is ${finish}`)
    console.log(`stopping ${stops.length} times in between`)
}

directions(
    "Truckee",
    "Tahoe City",
    "Sunnyside",
    "Homewood",
    "Tahoma"
)
```

`directions` 함수는 스프레드 연산자를 사용해 인자를 받습니다. 첫 번째 인자는 `start` 변수에 대입됩니다. 마지막 인자는 `finish` 변수에 `Array.reverse` 를 사용하여 대입됩니다. 그 후 `args` 배열의 `length` 를 사용해 얼마나 많은 도시를 지나는지 보여줍니다. `directions` 함수에 임의 개수의 경유 도시를 넘길 수 있기 때문에 이런 기능은 매우 편리합니다.

스프레드 연산자를 객체에 사용할 수 있습니다.

다음 예제는 두 배열을 세 번째 배열로 합쳤던 과정을 배열 대신 객체를 사용해 수행합니다.

```js
var morning = {
    breakfast: "oatmeal",
    lunch: "peanut butter and jelly"
}

var dinner = "mac and cheese"

var backpackingMeals = {
    ...morning,
    dinner
}

console.log(backpackingMeals) 
// { breakfast: "oatmeal", lunch: "peanut butter and jelly", dinner: "mac and cheese"}
 ```

## Promises 

**프로미스(Promise)** 는 비동기적인 동작을 잘 다루기 위한 방법입니다. 

randomuser.me API 로부터 데이터를 가져오는 비동기 프로미스를 만들겠습니다.

`getFakeMembers` 는 프라미스를 반환합니다.

```js
const getFakeMembers = count => new Promise((resolves, rejects) => {
    const api = `https://api.randomuser.me/?nat=US&results=${count}`
    const request = new XMLHttpRequest()
    request.open('GET', api)
    request.onload = () =>
        (request.status === 200) ?
        resolves(JSON.parse(request.response).results) :
        reject(Error(request.statusText))
    request.onerror = (err) => rejects(err)
    request.send()
})
```

이 함수로 프로미스를 만들 수 있지만 가져오고 싶은 멤버 수를 `getFakeMembers` 함수에 전달해 호출해야 실제 프로미스를 사용할 수 있습니다.

프로미스가 성공한 경우에 처리할 작업을 기술하기 위해 `then` 함수를 프로미스 뒤에 연쇄시킵니다. 이때 오류를 처리하기 위한 콜백도 함께 제공합니다.

```js
getFakeMembers(5).then(
    members => console.log(members),
    err => console.error(
        new Error("cannot load members from randomuser.me"))
)
```

## Classes

이전에는 클래스가 없어서 타입을 다음과 같이 함수를 정의하고 함수 객체에 있는 프로토타입을 사용해 메소드를 정의했습니다.

```js
function Vacation(destination, length) {
    this.destination = destination
    this.length = length
}

Vacation.prototype.print = function() {
    console.log(this.destination + " | " + this.length + " days")
}

var maui = new Vacation("Maui", 7)

maui.print() // Maui | 7 days
```

ES6 에서 클래스 선언이 추가되었습니다.

```js
class Vacation {
    constructor(destination, length) {
        this.destination = destination
        this.length = length
    }

    print() {
        console.log(`${this.destination} will take ${this.length} days.`)
    }
}
```

`new` 키워드를 이용하여 클래스의 새로운 인스턴스를 만들 수 있습니다. 그리고 인스턴스의 메소드를 호출할 수 있습니다.

```js
const trip = new Vacation("Santiago, Chile", 7)

trip.print() // Chile will take 7 days.
```

`Vacation` 을 휴가 타입을 정의하기 위한 추상 클래스로 사용할 수 있습니다. 예를 들어 `Expedition` 은 `Vacation` 클래스를 확장하여 장비를 표현하는 프로퍼티를 더 가집니다.

```js
class Expedition extends Vacation {
    constructor(destination, length, gear) {
        super(destination, length)
        this.gear = gear
    }

    print() {
        super.print()
        console.log(`Bring your ${this.gear.join(" and your ")}`)
    }
}
```

여기서 하위 클래스는 상위 클래스의 프로퍼티를 상속한다는 간단한 상속 관계를 살펴볼 수 있습니다. `print()` 에서는 상위 클래스에 있는 `print()` 를 호출한 다음 `Expedition` 에 있는 추가 정보를 출력했습니다.

```js
const trip = new Expedition(
    "Mt. Whitney", 3,
    ["sunglasses", "prayer flags", "camera"]
)

trip.print()
// Mt. Whitney will take 3 days.
// Bring your sunglasses and your prayer flags and your camera
```

## ES6 Modules

JavaScript **모듈(Modules)** 은 다른 JavaScript 파일에서 쉽게 불러서 활용할 수 있는 재사용 가능한 코드 조각입니다.

JavaScript 를 모듈화하는 방법은 모듈의 `import` 와 `export` 라이브러리를 활용하는거였지만, ES6 부터는 JavaScript 자체 모듈을 지원하기 시작했습니다.

아래 예제는 두 함수를 외부에 `export` 하는것입니다.

```js
export const print(message) => log(message, new Date())

export const log(message, timestamp) =>
    console.log(`${timestamp.toString()}: ${message}`)
```

`export` 를 사용해 다른 모듈에서 활용하도록 이름을 외부에 익스포트할 수 있습니다. 위 예제에서는 `print` 함수와 `log` 함수를 외부에 익스포트합니다.

모듈에서 단 하나의 이름만 외부에 익스포트하고 싶을 때는 `export default` 를 사용합니다.

```js
const freel = new Expedition("Mt, Freel", 2, ["water", "snack"])

export default freel
```

`export default` 는 하나의 이름만 노출하는 모듈에서 사용할 수 있습니다. `export` 한 모듈은 `import` 를 사용하여 다른 JavaScript 파일을 불러와 사용할 수 있습니다.

```js
import { print, log } from './text-helpers'
import freel from './mt-freel

print('printing a message')
log('logging a message')

freel.print()
```

모듈에서 가져온 대상에 다른 이름을 부여할 수 있습니다.

```js
import { print as p, log as l } from './text-helpers'

p('printing a message')
l('logging a message')
```

`import *` 를 사용하면 다른 모듈에서 가져온 모든 이름을 사요앚가 정한 로컬 이름 공간 안에 가둘 수 있습니다.

```js
import * as fns from './text-helpers
```

## CommonJS 

**커먼JS(CommonJS)** 는 모든 버전의 노드에서 지원하는 일반적인 모듈 패턴입니다. 이 모듈을 바벨이나 웹팩에서 여전히 사용할 수 있습니다. 커먼JS 를 사용하면 자바 객체를 `module.exports` 를 사용해 아래 예제처럼 익스포트할 수 있습니다.

```js
const print(message) => log(message, new Date())
const log(message, timestamp) =>

    console.log(`${timestamp.toString()}: ${message}`}

module.exports = {print, log}
```

커먼 JS 는 `import` 문을 지원하지 않습니다. 대신 `require` 함수로 모듈을 임포트 할 수 잇습니다.

```js
const { log, print } = require('./txt-helpers')
```