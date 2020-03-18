---
title : React Functional Programming with JavaScript
tags :
- Function Programming
- ES6
- JavaScript
- React
---

*이 포스트는 [Learning React](https://www.imel.ba/edukacija/learningreact1.pdf) 를 바탕으로 작성하였습니다.*

## What It Means to Be Functional 

JavaScript 에서는 함수가 어플리케이션의 데이터를 표현할 수 있습니다. 문자열이나 수 또는 다른 모든 값과 마찬가지로 `var` 키워드를 사용해 함수를 정의할 수 있습니다.

```js
var log = function(message) {
    console.log(message)
};

log("In JavaScript functions are variables")

// In JavaScript, functions are variables
```

ES6 에서는 화살표 함수를 사용해 같은 함수를 정의할 수 있습니다. 함수형 프로그래머들은 작은 함수를 아주 많이 작성하기 때문에 화살표 함수 구문을 사용할 수 있으며 코딩이 훨씬 더 간편해집니다.

```js
const log = message => console.log(message)
```

위의 두 예제는 같은 동작을 합니다.

함수를 변수에 넣을 수 있는것과 마찬가지로 객체에 넣을 수도 있습니다.

```js
const obj = {
    message: "They can be added to objects like variables",
    log(message) {
        console.log(message)
    }
}

obj.log(obj.message)
// They can be added to objects like variables
```

함수를 배열에 넣을 수도 있습니다.

```js
const messages = [
    "They can be inserted into arrays",
    message => console.log(message),
    "like variables",
    message => console.log(message)
]

messages[1](messages[0]) // They can be inserted i
messages[3](messages[2]) // like variables
```

다른 값과 마찬가지로 함수를 다른 함수에 인자로 넘길 수도 있습니다.

```js
const insideFn = logger =>
    logger("They can be sent to other functions as arguments");

insideFn(message => console.log(message))

// They can be sent to other functions as arguments
```

함수가 함수를 반환할 수 있습니다. 이 또한 일반적인 값과 마찬가지입니다.

```js
var createScream = function(logger) {
    return function(message) {
        logger(message.toUpperCase() + "!!!")
    }
}

const scream = createScream(message => console.log(message))
scream('functions can be returned from other functions')
scream('createScream returns a function')
scream('scream invokes that returned function')

// FUNCTIONS CAN BE RETURNED FROM OTHER FUNCTIONS!!!
// CREATESCREAM RETURNS A FUNCTION!!!
// SCREAM INVOKES THAT RETURNED FUNCTION!!!
```

함수를 인자로 받거나 함수를 반환하는 함수를 고차 함수라고 부릅니다. ES6 문법을 사용하면 `createScream` 고차 함수를 화살표 함수르 표현할 수 있습니다.

```js
const createScream = logger => message =>
    ogger(message.toUpperCase() + "!!!")
```

## Imperative Versus Declarative 

함수형 프로그래밍은 **선언적 프로그래밍(Declarative Programming)** 이라는 더 넓은 프로그래밍 패러다임의 한 가지입니다.

선언적 프로그래밍은 필요한 것을 달성하는 과정을 하나하나 기술하는 것보다 필요한 것이 어떤 것인지 기술하는 데 방점을 두고 어플리케이션의 구조를 세워나가는 프로그래밍 스타일입니다.

**명령형 프로그래밍(Imperative Programming)** 은 코드로 원하는 결과를 달성해 나가는 과정에만 관심을 두는 프로그래밍 스타일입니다.

공백 문자( ) 를 하이픈(-) 으로 바꾸는 예제를 명령형 프로그래밍으로 알아보겠습니다.

```js
var string = "This is the midday show with Cheryl Waters";
var urlFriendly = "";

for (var i=0; i<string.length; i++) {
    if (string[i] === " ") {
        urlFriendly += "-";
    } else {
        urlFriendly += string[i];
    }
}
console.log(urlFriendly);
```

모든 문자를 루프를 돌면서 공백을 만날 때마다 그 공백을 `-` 로 바꿉니다.

위 문제를 선언적 프로그래밍으로 풀어보겠습니다.

```js
const string = "This is the mid day show with Cheryl Waters"
const urlFriendly = string.replace(/ /g, "-")

console.log(urlFriendly)
```

여기서는 정규식을 사용해 모든 공백을 하이픈으로 변경합니다. `replace` 함수를 사용하여 모든 공백이 하이픈으로 변경이 됩니다.

선언적 프로그래밍의 코드 구문은 어떤 일이 발생하는지 기술하고, 실제로 그 작업을 처리하는 방법은 추상화로 아랫단에 감춰집니다.

선언적 프로그램은 코드 자체가 어떤 일이 벌어질지 설명하기 때문에 좀 더 추론하기 쉽습니다. 다음 코드는 API 에서 멤버를 가져온 다음 어떤 일을 수행 하는지 기술합니다.

```js
const loadAndMapMembers = compose(
    combineWith(sessionStorage, "members"),
    save(sessionStorage, "members"),
    scopeMembers(window),
    logMemberInfoToConsole,
    logFieldsToConsole("name.first"),
    countMembersBy("location.state"),
    prepStatesForMapping,
    save(sessionStorage, "map"),
    renderUSMap
);
getFakeMembers(100).then(loadAndMapMembers);
```

선언적 프로그래밍은 추론하기 쉬운 어플리케이션을 만들어내며, 규모를 확장하는것도 더 쉬워집니다.

이제 **문서 객체 모델(Document Object Model, DOM)** 을 만드는 과정을 살펴보겠습니다. 명령형 접근 방식은 다음과 같이 DOM 을 구축하는 절차와 관련 있습니다.

```js
var target = document.getElementById('target');
var wrapper = document.createElement('div');
var headline = document.createElement('h1');

wrapper.id = "welcome";
headline.innerText = "Hello World";

wrapper.appendChild(headline);
target.appendChild(wrapper);
```

위 방법으로 구현된 DOM 에 새로운 기능을 추가하거나 규모를 확장하는 것은 아주 어려운 일입니다.

이제 React 컴포넌트를 사용해 DOM 을 선언적으로 구현해보겠습니다.

```js
const { render } = ReactDOM

const Welcome = () => (
    <div id="welcome">
        <h1>Hello World</h1>
    </div>
)

render(
    <Welcome />,
    document.getElementById('target')
)
```

React 는 선언적이며, 여기서 `Welcome` 컴포넌트는 렌더링할 DOM 을 기술합니다. `render` 함수는 컴포넌트에 있는 지시에 따라 DOM 을 만듭니다.

## Functional Concepts 

함수형 프로그래밍의 햑심 개념은 Immutability, Pure Functions, Data Transformations, Higher-Order Functions, Recursion, Composition 입니다.

### Immutability 

함수형 프로그래밍은 데이터가 변할 수 없습니다. **불변성(Immutability)** 데이터는 결코 바뀌지 않습니다.

불변성이 어떻게 작동하는지 이해하기 위해 간단한 예제를 살펴보겠습니다. 잔디 색을 표현하는 객체를 생각해보겠습니다.

```js
let color_lawn = {
    title: "lawn",
    color: "#00FF00",
    rating: 0
}
```

아래와 같이 색에 평점을 매기는 함수를 만들겠습니다. 이 함수는 넘겨받은 `color` 객체의 `rating` 을 변경합니다.

```js
function rateColor(color, rating) {
    color.rating = rating
    return color
}

console.log(rateColor(color_lawn, 5).rating) // 5
console.log(color_lawn.rating) // 5
```

JavaScript 에서 함수의 인자는 실제 데이터에 대한 참조입니다. `rateColor` 함수 안에서 `color` 의 `rating` 을 변경하면 원본 `color_lawn` 객체의 `rating` 도 바뀝니다.

`rateColor` 를 아래와 같이 수정하면, 원본에는 아무런 해가 없이 색깔에 평점을 부여할 수 있습니다.

```js
var rateColor = function(color, rating) {
    return Object.assign({}, color, {rating:rating})
}

console.log(rateColor(color_lawn, 5).rating) // 5
console.log(color_lawn.rating) // 0
```

`Object.assign` 은 빈 객체를 받고, `color` 객체를 그 빈 객체에 복사하고, 복사본에 있는 `rating` 프로퍼티의 값을 `rating` 파라미터의 값으로 변경합니다. 이제 원본은 그대로 남겨둔 채 `rating` 만 변경된 복사본을 얻게 됩니다.

ES6 의 화살표 함수와 ES7 의 객체 스프레드 연산자를 활용해 같은 함수를 작성할 수 있습니다. 이렇게 만든 `rateColor` 함수는 스프레드 연산자를 사용해 원본 `color` 를 새로운 객체 안에 복사한 다음 `rating` 프로퍼티를 덮어씁니다.

```js
const rateColor = (color, rating) => ({
    ...color,
    rating
})
```

새로운 버전의 `rateColor` 함수도 똑같이 작동합니다.

색의 이름으로 이루어진 배열을 생각해보겠습니다.

```js
let list = [
    { title: "Rad Red"},
    { title: "Lawn"},
    { title: "Party Pink"}
]
```

이 배열에 `Array.push` 를 사용해 색을 추가하는 함수를 작성할 수 있습니다.

```js
var addColor = function(title, colors) {
    colors.push({ title: title })
    return colors;
}
console.log(addColor("Glam Green", list).length) // 4
console.log(list.length) // 4
```

하지만 `Array.push` 함수는 불변성 함수가 아닙니다. 이 `addColor` 함수는 원본 배열에 새로운 원소를 추가합니다. 원래의 `colorArray` 배열을 변화시키지 않고 유지하기 위해서는 `Array.concat` 을 사용하면 됩니다.

```js
const addColor = (title, array) => array.concat({title})

console.log(addColor("Glam Green", list).length) // 4
console.log(list.length) // 3 
```

`Array.concat` 은 두 배열을 붙여줍니다. 위 예에서는 새로운 객체를 반환합니다. 그 객체에는 새로운 이름인 `title` 프로퍼티로 들어있습니다. `Array.concat` 은 객체를 원래 배열을 복사한 새로운 배열 뒤에 추가합니다.

ES6 의 스프레드 연산자를 사용해 배열을 복사할 수 있습니다.

```js
const addColor = (title, list) => [...list, {title}]
```

이 함수는 원본 리스트의 원소를 새로운 배열에 복사하고, `title` 파라미터로 받은 값을 `title` 프로퍼티로 하는 객체를 새 배열 뒤에 추가합니다. 이 함수는 인자로 받은 `list` 를 변경하지 않기 때문에 `list` 의 원본인 `colorArray` 의 불변성을 지켜줍니다.

### Pure Functions 

**순수 함수(Pure Function)** 은 파라미터에 의해서만 반환값이 결정되는 함수를 뜻합니다. 순수 함수는 최소 하나 이상의 인자를 받고 인자가 같으면 항상 같은 값이나 함수를 반환합니다. 순수 함수는 인자를 변경 불가능한 데이터로 취급합니다.

순수 함수를 이해하기 위해 먼저 일반 함수를 보겠습니다.

```js
var frederick = {
    name: "Frederick Douglass",
    canRead: false,
    canWrite: false
}

function selfEducate() {
    frederick.canRead = true
    frederick.canWrite = true
    return frederick
}

selfEducate()
console.log( frederick )

// {name: "Frederick Douglass", canRead: true, canWrite: true}
```

`selfEducate` 함수는 순수하지 않습니다. 이 함수는 인자를 취하지 않으며, 값을 반환하거나 함수를 반환하지 않습니다. 또한, 자신의 영역 밖에 있는 `frederick` 이라는 변수를 바꿉니다. `selfEducate` 함수가 호출되면 뭔가를 변화시킵니다. 즉, 부수 효과가 발생합니다.

이제 `selfEducate` 가 파라미터를 받게 만들겠습니다.

```js
const frederick = {
    name: "Frederick Douglass",
    canRead: false,
    canWrite: false
}

const selfEducate = (person) => {
    person.canRead = true
    person.canWrite = true
    return person
}

console.log( selfEducate(frederick) )
console.log( frederick )

// {name: "Frederick Douglass", canRead: true, canWrite: true}
// {name: "Frederick Douglass", canRead: true, canWrite: true}
```

파라미터를 받긴 하지만 아직 부수 효과가 있습니다. 함수에 전달된 객체를 불변 데이터로 취급한다면 순수 함수를 얻을 수 있을 것입니다.

```js
const frederick = {
    name: "Frederick Douglass",
    canRead: false,
    canWrite: false
}

const selfEducate = person => ({
    ...person,
    canRead: true,
    canWrite: true
})

console.log( selfEducate(frederick) )
console.log( frederick )

// {name: "Frederick Douglass", canRead: true, canWrite: true}
// {name: "Frederick Douglass", canRead: false, canWrite: false}
```

마침내 순수함수가 되었습니다. 이 함수는 전달받은 인자 `person` 으로부터 새로운 값을 계산합니다. 새 값을 계산할 때 전달받은 인자를 변경하지 않고 새로 만든 객체를 반환합니다. 따라서 부수효과가 없습니다.

이제 DOM 을 변경하는 순수하지 않은 함수를 살펴보겠습니다.

```js
function Header(text) {
    let h1 = document.createElement('h1');
    h1.innerText = text;
    document.body.appendChild(h1);
}

Header("Header() caused side effects");
```

이 함수는 함수나 값을 반환하지 않으며 DOM 을 변경하는 부수 효과를 발생시킵니다.

React 에선 UI 를 순수 함수로 표현합니다. 이 함수는 DOM 을 변경하는 부수 효과를 발생시키지 않고 엘리먼트를 반환합니다. 이 함수는 엘리먼트를 만드는 일만 책임지며, DOM 을 변경하는 책임은 어플리케이션의 다른 부분이 담당해야 합니다.

```js
const Header = (props) => <h1>{props.title}</h1>
```

순수 함수는 함수형 프로그래밍의 또 다른 핵심 개념이빈다. 순수 함수를 사용하면 어플리케이션의 상태에 영향을 미치지 않기 때문에 코딩이 편해집니다.

함수를 만들 때 다음 3 가지 규칙을 따르면 순수 함수를 만들 수 있습니다.

1. The function should take in at least one argument.
2. The function should return a value or another function.
3. The function should not change or mutate any of its arguments.

### Data Transformations 

함수형 JavaScript 에서 데이터 변환을 하는 핵심 함수가 2 개 있습니다. `Array.map` 과 `Array.reduce` 입니다.

학교 명단이 있는 배열을 보겠습니다.

```js
const schools = [
    "Yorktown",
    "Washington & Lee",
    "Wakefield"
]
```

`Array.join` 함수를 사용함녀 콤마(,) 로 각 학교를 구분한 문자열을 얻을 수 있습니다.

```js
console.log( schools.join(", ") )

// "Yorktown, Washington & Lee, Wakefield"
```

`join` 은 JavaScript 내장 배열 메소드입니다. `join` 은 배열의 모든 원소를 인자로 받아 구분자로 연결한 문자열을 반환합니다. 

`W` 로 시작하는 학교만 들어 있는 새로운 배열을 만들고 싶다면, `Array.filter` 메소드를 사용하면 됩니다.

```js
const wSchools = schools.filter(school => school[0] === "W")

console.log( wSchools )
// ["Washington & Lee", "Wakefield"]
```

`Array.filter` 는 원본 배열로부터 새로운 배열을 만들어내는 JavaScript 배열 내장 함수입니다. 이 함수는 **술어(Predicate)** 를 유일한 인자로 받습니다. 술어는 `true` 나 `false` 를 반환하는 함수입니다.

`Array.filter` 는 배열에 있는 모든 원소에 이 술어를 한 번씩 호출합니다. `filter` 는 술어에 배열의 원소를 인자로 전달하며, 술어가 반환한느 값이 `true` 면 해당 원소를 새 배열에 넣습니다.

배열에 원소를 제거해야 한다면 `Array.pop` 이나 `Array.splice` 보다 `Array.filter` 를 사용하면됩니다. `Array.filter` 는 순수 함수입니다.

```js
const cutSchool = (cut, list) =>
    list.filter(school => school !== cut)

console.log(cutSchool("Washington & Lee", schools).join(" * "))

// "Yorktown * Wakefield"

console.log(schools.join("\n"))

// Yorktown
// Washington & Lee
// Wakefield
```

`cutSchool` 함수는 *Washington & Lee* 가 들어 있지 않은 새로운 배열을 반환합니다. `join` 함수를 사용해 새 배열에 들어 있는 두 학교의 이름을 `*` 로 구분한 문자열을 만듭니다. `cutSchool` 은 순수 함수입니다.

함수형 프로그래밍에 꼭 필요한 다른 함수는 `Array.map` 이 있습니다. `Array.map` 은 술어가 아니라 변환 함수를 인자로 받습니다. `Array.map` 은 함수를 배열의 모든 원소에 적용해서 반환받은 값으로 이루어진 새 배열을 반환합니다.

```js
const highSchools = schools.map(school => `${school} High School`)

console.log(highSchools.join("\n"))

// Yorktown High School
// Washington & Lee High School
// Wakefield High School

console.log(schools.join("\n"))

// Yorktown
// Washington & Lee
// Wakefield
```

위 `map` 함수는 각 학교 이름 뒤에 *High School* 을 추가합니다. 이때 원본 `school` 배열은 변화가 없습니다.

`map` 함수는 객체, 값, 배열, 함수 등 모든 JavaScript 타입의 값으로 이루어진 배열을 만들 수 있습니다. 다음 예제는 학교가 담겨 있는 객체의 배열을 반환하는 `map` 함수를 보여줍니다.

```js
const highSchools = schools.map(school => ({ name: school }))

console.log( highSchools )

// [
// { name: "Yorktown" },
// { name: "Washington & Lee" },
// { name: "Wakefield" }
// ]
```

위 예제는 문자열을 포함하는 배열로부터 객체를 포함하는 배열을 만듭니다.

다음은 `schools` 배열을 변경하지 않으면서 *Stratford* 라는 학교 이름을 *HB Woodlawn* 으로 바꿉니다.

```js
let schools = [
    { name: "Yorktown"},
    { name: "Stratford" },
    { name: "Washington & Lee"},
    { name: "Wakefield"}
]

let updatedSchools = editName("Stratford", "HB Woodlawn", schools)

console.log( updatedSchools[1] ) // { name: "HB Woodlawn" }
console.log( schools[1] ) // { name: "Stratford" },
```

`schools` 배열은 객체의 배열입니다. `updatedSchools` 변수는 `editName` 함수에 대상 학교 이름, 그 학교의 새 이름, 그리고 `schools` 배열을 넘겨받은 결과를 저장합니다. `editName` 함수는 원본 배열은 그대로 둔 채 학교 이름이 바뀐 새 배열을 반환합니다.

```js
const editName = (oldName, name, arr) =>
    arr.map(item => {
        if (item.name === oldName) {
            return {
                ...item,
                name
            }
        } else {
    return item
    }
})
```

`editName` 은 `map` 함수를 사용해 원본 배열로부터 새로운 객체로 이루어진 배열을 만듭니다. `editName` 이 `Array.map` 에 전달하는 화살표 함수는 배열의 원소를 `item` 파라미터로 받으며, 파라미터의 이름과 `oldName` 이 같은지 비교한 후 이름이 같은 경우 새 이름을 넣고 반환합니다.

`editName` 함수를 한 줄로 쓸 수 있습니다. 다음은 `if/else` 문 대신 3 항 연산자를 사용한 코드입니다.

```js
const editName = (oldName, name, arr) =>
    arr.map(item => (item.name === oldName) ?
        ({...item,name}) :
    item
)
```

위 예제는 `Array.map` 에 전달한 변환 함수가 파라미터 1 개 입니다. 하지만 `Array.map` 은 각 원소의 인덱스를 변환 함수의 2 번째 인자로 넘겨줍니다. 다음 예를 보겠습니다.

```js
const editName = (n, name, arr) =>
    arr.map( (item, i) => (i === n) ?
        ({...item, name}) :
        item
    )

let updateSchools2 = editNth(2, "Mansfield", schools)

consle.log( updateSchools2[2] ) // { name: "Mansfield" }
console.log( schools[2] )   // { name: "Washington & Lee" }
```

`editNth` 에서는 원소와 인덱스를 넘겨주는 `Array.map` 기능을 사용했습니다. 변환 함수에서 인덱스 `i` 가 변경 대상 `n` 과 같은 인덱스라면 `item` 에 새 이름을 넣은 객체를 만들어서 인덱스가 같지 않으면 원래의 `item` 을 그대로 반환합니다.

객체를 배열로 변환하고 싶을 때는 `Array.map` 과 `Object.keys` 를 함께 사용하면 됩니다. `Object.keys` 는 어떤 객체의 키로 이루어진 배여릉ㄹ 반환하는 메소드입니다.

`schools` 객체를 학교의 배열로 바꾼다고 해보겠습니다.

```js
const schools = {
    "Yorktown": 10,
    "Washington & Lee": 2,
    "Wakefield": 5
}

const schoolArray = Object.keys(schools).map(key => ({
    name: key,
    wins: schools[key]
    })
)

console.log(schoolArray)
// [ { name: "Yorktown", wins: 10 },
// { name: "Washington & Lee", wins: 2 },
// { name: "Wakefield", wins: 5 } ]
```

`reduce` 와 `reduceRight` 함수를 사용하면 객체를 수, 문자열, 불린 값, 객체, 심지어 함수로 변환할 수 있습니다.

수로 이루어진 배열에서 최댓값을 찾오야 한다고 하겠습니다. 배열을 하나의 수로 변환해야 하므로 `reduce` 를 사용할 수 있습니다.

```js
const ages = [21,18,42,40,64,63,34];

const maxAge = ages.reduce((max, age) => {
    console.log(`${age} > ${max} = ${age > max}`);
    if (age > max) {
        return age
    } else {
        return max
    }
}, 0)

console.log('maxAge', maxAge);
// 21 > 0 = true
// 18 > 21 = false
// 42 > 21 = true
// 40 > 42 = false
// 64 > 42 = true
// 63 > 64 = false
// 34 > 64 = false
// maxAge 64
```

`ages` 배열을 하나의 값으로 축약했습니다. `reduce` 함수는 변환 함수와 초깃값을 인자로 받습니다. 여기서 초깃갑은 0 이고 처음에 그 값으로 최댓값 `max` 를 설정합니다. 변환 함수는 객체의 모든 원소에 한 번씩 호출됩니다.

아래와 같이 코드를 변경할 수 있습니다.

```js
const max = ages.reduce(
    (max, value) => (value > max) ? value : max,
    0
)
```

배열을 객체로 변환해야할 때가 있습니다. 다음 예제는 `reduce` 를 사용해 값이 들어있는 배열을 해시로 변환합니다.

```js
const colors = [
    {
        id: '-xekare',
        title: "rad red",
        rating: 3
    },
    {
        id: '-jbwsof',
        title: "big blue",
        rating: 2
    },
    {
        id: '-prigbj',
        title: "grizzly grey",
        rating: 5
    },
    {
        id: '-ryhbhsl',
        title: "banana",
    rating: 1
    }
]

const hashColors = colors.reduce(
    (hash, {id, title, rating}) => {
        hash[id] = {title, rating}
        return hash
    },
    {}
)

console.log(hashColors);

//{ '-xekare': {title: "rad red", rating: 3},
//  '-jbwsof': {title: "big blue", rating: 2},
//  '-prigbj': {title: "grizzly grey", rating: 5},
//  '-ryhbhsl': {title: "banana", rating: 1} }
```

위 예제에서 `reduce` 함수에 전달한 두 번째 인자는 빈 객체입니다. 이 빈 객체가 바로 해시에 대한 초깃값입니다.

이터레이션마다 변환 함수는 대괄호 [] 연산을 사용해 해시에 새로운 키를 추가합니다. 이때 배열의 각 원소에 있는 `id` 필드의 값을 키 값으로 사용합니다.

`reduce` 를 사용해 전혀 다른 배열로 만들 수 있습니다. 다음과 같이 값이 여럿 들어 있는 배열을 서로 다른 값이 한 번씩만 들어 있는 배열로 바꿀 수 있습니다.

```js
const colors = ["red", "red", "green", "blue", "green"];

const distinctColors = colors.reduce(
    (distinct, color) =>
        (distinct.indexOf(color) !== -1) ? distinct : [...distinct, color],
    []
)

console.log(distinctColors)
// ["red", "green", "blue"]
```

### Higher-Order Functions 

고차 함수는 다른 함수를 조작할 수 있는 함수입니다.

고차함수를 구현하는 예제를 보겠습니다.

```js
const invokeIf = (condition, fnTrue, fnFalse) =>
    (condition) ? fnTrue() : fnFalse()

const showWelcome = () =>
    console.log("Welcome!!!")

const showUnauthorized = () =>
    console.log("Unauthorized!!!")

invokeIf(true, showWelcome, showUnauthorized) // "Welcome"
invokeIf(false, showWelcome, showUnauthorized) // "Unauthorized"
```

`invokeIf` 는 조건이 참이면 `showWelcome` 이 호출되고 거짓이면 `showUnauthorized` 가 호출됩니다.

다른 함수를 반환하는 고차 함수는 JavaScript 에서 비동기적인 실행 맥락을 처리할 때 유용합니다. 함수를 반환하는 고차 함수를 이용하면 필요할 때 재활용할 수 있는 함수를 만들 수 있습니다.

**커링(Currying)** 은 고차 함수 사용법과 관련한 함수형 프로그래밍 기법입니다. 커링은 어떤 연산을 수행할 때 필요한 값 중 일부를 저장하고 나중에 나머지 값을 전달받는 기법입니다.

아래는 커링 예제입니다. `userLogs` 는 일부 정보를 받아서 함수를 반환합니다.

```js
const userLogs = userName => message =>
    console.log(`${userName} -> ${message}`)

const log = userLogs("grandpa23")

log("attempted to load 20 fake members")
getFakeMembers(20).then(
    members => log(`successfully loaded ${members.length} members`),
    error => log("encountered an error loading members")
)

// grandpa23 -> attempted to load 20 fake members
// grandpa23 -> successfully loaded 20 members

// grandpa23 -> attempted to load 20 fake members
// grandpa23 -> encountered an error loading members
```

`userLogs` 를 호추랳서 만들어지는 `log` 함수를 호출할 때마다 메세지 앞에 *grandpa23* 이 출력됩니다.

### Recursion 

**재귀(Recursion)** 는 자기 자신을 호출하는 함수를 만드는 기법입니다. 간단한 예제를 살펴보겠습니다.

```js
const countdown = (value, fn) => {
    fn(value)
    return (value > 0) ? countdown(value-1, fn) : value
}

countdown(10, value => console.log(value));

// 10
// 9
// 8
// 7
// 6
// 5
// 4
// 3
// 2
// 1
// 0
```

데이터 구조를 검색할 때도 재귀가 유용합니다. HTML DOM 에서 자식이 없는 엘리먼트를 찾고 싶을 때도 재귀를 사용할 수 있습니다. 다음 예제는 재귀로 객체에 내포된 값을 찾아냅니다.

```js
var dan = {
    type: "person",
    data: {
        gender: "male",
        info: {
            id: 22,
            fullname: {
                first: "Dan",
                last: "Deacon"
            }
        }
    }
}

deepPick("type", dan); // "person"
deepPick("data.info.fullname.first", dan); // "Dan"
```

`deepPick` 을 사용해 최상위 객체에 저장된 `Dan` 타입의 접근할 수 있고, 내포된 객체를 타고 내려가서 `Dan` 의 이름을 알아낼 수 있습니다. 점으로 구분한 문자열을 사용해 내포된 객체의 계층 구조를 어떻게 타고 내려가서 값을 가져올지 지정할 수 있습니다.

```js
const deepPick = (fields, object={}) => {
    const [first, ...remaining] = fields.split(".")
    return (remaining.length) ?
        deepPick(remaining.join("."), object[first]) :
        object[first]
}
```

이 함수는 `fields` 에 더 이상 점이 남아 있지 않을 때까지 재귀 호출을 반복합니다. `fields` 에 점이 없다는 말은 더 이상 아래 계층으로 내려갈 내포된 객체가 없다는 뜻입니다. 다음 예제를 보면 `deepPick` 에 있는 `first`, `remaining`, `object[first]` 가 어떻게 변하는지 알 수 있습니다.

```js
deepPick("data.info.fullname.first", dan); // "Deacon"

// First Iteration
// first = "data"
// remaining.join(".") = "info.fullname.first"
// object[first] = { gender: "male", {info} }

// Second Iteration
// first = "info"
// remaining.join(".") = "fullname.first"
// object[first] = {id: 22, {fullname}}

// Third Iteration
// first = "fullname"
// remaining.join("." = "first"
// object[first] = {first: "Dan", last: "Deacon" }

// Finally...
// first = "first"
// remaining.length = 0
// object[first] = "Deacon"
```

### Composition 

문자열에는 `replace` 메소드가 있습니다. `replace` 메소드는 문자열을 반환하며 그 문자열에는 역시 `replace` 메소드가 있습니다. 따라서 점 표기법을 사용해 문자열을 계속 변환할 수 있습니다.

```js
const template = "hh:mm:ss tt"
const clockTime = template.replace("hh", "03")
    .replace("mm", "33")
    .replace("ss", "33")
    .replace("tt", "PM")

console.log(clockTime)
// "03:33:33 PM"
```

위 예제는 문자열을 템플릿으로 사용합니다. 템플릿 문자열 끝에 `replace` 메서드를 연쇄 호출하여 시, 분, 초, 오전 / 오후 정보를 차례로 새로운 값으로 변환합니다.

체이닝은 합성 기법 중 하나이며, 다른 합성 기법도 있습니다. 합성의 목표는 *함수를 조합해 고차 함수를 만들어내는것* 입니다.

```js
const both = date => appendAMPM(civilianHours(date))
```

`both` 는 서로 다른 두 함수에 값을 흘려 넣는 함수입니다. `civilianHours` 의 출력은 `appendAMPM` 의 입력이 됩니다.

`compose` 를 이용해 함수를 조합할 수 있습니다.

```js
const both = compose(
    civilianHours,
    appendAMPM
)
both(new Date())
```

`compose` 는 고차 함수입니다. 이 함수는 함수를 인자로 받아서 값을 하나 반환합니다.

```js
const compose = (...fns) =>
    (arg) =>
        fns.reduce(
            (composed, f) => f(composed),
            arg
        ) 
```

`compose` 는 여러 함수를 인자로 받아서 한 함수를 결과로 반환합니다. 이 구현은 스프레드 연산자를 사용해 인자로 받은 함수들을 `fns` 라는 배열로 만듭니다. 그 후 `arg` 라는 인자를 받는 함수를 반환합니다.

이렇게 반환된 화살표 함수에 인자를 전ㄷ라해 호출하면 `fns` 배열에 `reduce` 가 호출되면서 `arg` 로 받은 값이 전달됩니다. `arg` 는 `reduce` 의 초깃값이 되고 각 이터레이션마다 배열의 각 원소와 이전 값을 변환 함수를 사용해 축약한 값을 전달합니다.

이때 `reduce` 의 변환 함수는 이전 이터레이션의 결과값인 `composed` 와 `f` 를 인자로 받아서 `f` 에 `composed` 를 적용해 반환합니다. 결국 마지막 함수가 호출되며 최종 결과를 반환합니다.

### Putting It All Together

함수형 프로그래밍은 다음 3 가지 규칙을 따르면 쉽게 달성할 수 있습니다.

1. Keep data immutable.
2. Keep functions pure—accept at least one argument, return data or another function.
3. Use recursion over looping (wherever possible).