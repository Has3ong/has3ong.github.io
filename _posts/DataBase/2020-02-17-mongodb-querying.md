---
title : MongoDB Querying
tags :
- Querying
- MongoDB
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Introduction to find

MongoDB 에서 `find` 함수는 쿼리에 사용합니다. 쿼리는 컬렉션에서 문서의 부분집합을 반환합니다. `find` 의 첫 매개변수로 어떤 문서를 가져올지 결정합니다.

빈쿼리 문서는 컬렉션 내 모든것과 일치합니다. 만약 `find` 함수에 쿼리 문서가 없으면 빈 쿼리 문서로 인식합니다. 따라서 다음 명령어는 컬렉션안의 모든 문서를 반환합니다.

```js
> db.c.find()
```

쿼리 문서에 여러 Key / Value 쌍을 추가해서 검색을 제한할 수 있습니다. 이는 대부분의 데이터형에 대해 직접적으로 작동합니다. 찾고자 하는 값만 지정하면 간단한 데이터형을 쿼리할 수 있습니다.

```js
> db.users.find({"age" : 27})
```

`username` Key 값이 `joe` 인 경우와 같이 문자열형이 일치하는 문서를 찾고 싶다면 아래와 같이 Key / Value 쌍을 사용할 수 있습니다.

```js
> db.users.find({"usersname" : "joe"})
```

쿼리 문서에 여러 Key / Value 쌍을 추가할 수 있으며 AND 조건으로 해석됩니다.

```js
> db.users.find({"username" : "joe", "age" : 27})
```

### Specifying Which Keys to Return

때때로 반환받은 문서 내의 모든 Key / Value 정보가 필요하지 않을 수도 있습니다. 이런 경우에는 `find()` 의 2 번째 매개변수에 원하는 Key 를 지정하면 됩니다. 이는 네트워크상의 데이터 전송량과 클라이언트 쪽에서 문서를 해석하는 데 드는 시간과 메모리를 줄여줍니다.

예를 들어 사용자 컬렉션이 있고 `username` 과 `email` 키의 값만 원할 때는 아래와 같은 쿼리를 통해 받을 수 있습니다.

```js
> db.users.find({}, {"username" : 1, "email" : 1})
{
  "_id" : ObjectId("4ba0f0dfd22aa494fd523620"),
  "username" : "joe",
  "email" : "joe@example.com"
}
```

위 결과에서 보듯이 `_id` 키는 특별히 지정하지 않아도 항상 반환됩니다.

두 번째 매개변수를 사용해 쿼리 결과로부터 특정 Key / Value 쌍을 제외할 수 있습니다. 예를 들어 다양한 키가 존재하는 문서에서 `fatal_weakness` 키 값이 절대 쓸일이 없다면 다음과 같이 제외할 수 있습니다.

```js
> db.users.find({}, {"fatal_weakness" : 0})
```

`_id` 의 반환을 제외할 수 있습니다.

```js
> db.users.find({}, {"username" : 1, "_id" : 0})
{
 "username" : "joe",
}
```

### Limitations

쿼리에는 몇 가지 제약이 있습니다. 쿼리값은 데이터베이스 관점에서는 반드시 상수여야 합니다. 이는 문서 내 다른 Key 의 값을 참조할 수 없음을 의미합니다. 예를 들어 인벤토리를 유지하면서 `in_stock` 과 `num_sold` 라는 Key 가 있으면 이 값들은 다음과 같은 쿼리로 비교할 수 있습니다.

```js
> db.stock.find({"in_stock" : "this.num_sold"}) // doesn't work
```

이를 쿼리하는 방법은 있으나 일반적인 쿼리로 처리할 수 있도록 문서 구조를 약간 재구성하면 더 좋은 성능을 얻을 수 있습니다. `initial_stock` 과 `in_stock` Key 를 사용해보겠습니다. 누군가 상품을 구매하면 `in_stock` 의 값이 매번 감소하므로 결국 품절 상품을 확인하는 쿼리는 다음과 같습니다.

```js
> db.stock.find({"in_stock" : 0})
```

## Query Criteria

쿼리는 이전에 설명한 완전한 일치 외에도 범위, `OR` 절, `Negation` 조건 등 더욱 복잡한 조건으로 검색할 수 있습니다.

### Query Conditionals

`$lt`, `$lte`, `$gt`, `$gte` 는 모두 비교 연산자고 각각 <, <=, >, >= 에 해당합니다. 이를 조합해서 사용하면 범위 내에서 값을 쿼리할 수 있습니다. 예를 들어 18 세에서 30 세 사이의 사용자를 찾기 위해서는 다음과 같이 쿼리합니다.

```js
> db.users.find({"age" : {"$gte" : 18, "$lte" : 30}})
```

위 명령은 `age` 가 18 세 이상이고 30 세 이하인 모든 문서를 찾을것입니다.

이런 종류의 범위 쿼리는 날짜 쿼리에도 유용합니다. 다음은 2007 년 1 월 1 일 이전에 등록한 사람을 찾는 예제입니다.

```js
> start = new Date("01/01/2007")
> db.users.find({"registered" : {"$lt" : start}})
```

날짜는 1 / 1000 초 정확도로 저장하므로 정확한 일치 여부는 그리 유용하지 않습니다. 보통 하루, 한 주 , 한 달 단위로 원하는 경우가 있기 떄문에 범위 쿼리가 필요합니다.

특정 값과 일치하지 않는 값의 문서를 찾으려면 `not equal` 을 나타내는 `$ne` 를 사용합니다. 만약 사용자명이 **joe** 가 아닌 모든 사용자를 찾는다면 아래와 같이 쿼리할 수 있습니다.

```js
> db.users.find({"username" : {"$ne" : "joe"}})
```

`$ne` 는 모든 데이터형에 사용할 수 있습니다.

### OR Queries

MongoDB 의 `OR` 쿼리에는 2 가지 방법이 있습니다. `$in` 은 하나의 Key 에 대해 다양한 값과 비교하는 쿼리에 사용할 수 있습니다. `$or` 은 더 일반적이며 여러 `Key` 에 대해 주어진 값과 비교하는 쿼리에 사용할 수 있습니다.

만약 하나의 Key 에 대해 일치하는 여러 값을 찾고자 한다면 `$in` 에 조건 배열을 사용합니다. 예를 들어 추첨 당첨자를 뽑고 있고, 당첨 번호가 725, 542, 390 이라고 가정하겟습니다. 이 세 문서를 찾으려면 다음과 같이 쿼리합니다.

```js
> db.raffle.find({"ticket_no" : {"$in" : [725, 542, 390]}})
```

`$in` 은 매우 유연하여 여러 다른 값을 쓸 수 있을 뿐만 아니라 다른 데이터형도 쓸 수 있습니다. 예를 들어 점진적으로 사용자 ID 번호 대신 사용자 이름을 쓰도록 이전하고 있다면, 이 두 조건 중 하나라도 맞는 문서를 찾도록 쿼리할 수 있습니다.

```js
db.users.find("user_id" : {"$in" : [12345, "joe"]})
```

이 쿼리는 `user_id` 가 12345 이거나 joe 인 문서를 찾습니다.

만약 `$in` 의 조건 배열에 하나의 값만 주어지면 바로 일치하는 것을 `find` 하는 것과 같습니다. 예를 들어 `{ticket_no : {$in : [725]}}` 의 문서는 `{ticket_no : 725}` 의 문서와 일치합니다. `$in` 의 반대는 `$nin` 이며, 배열 내 조건과 일치하지 않는 문서를 반환합니다. 추첨에 당첨되지 않은 모든 사람을 반환받고 싶다면 다음과 같이 쿼리할 수 있습니다.

```js
> db.raffle.find({"ticket_no" : {"$nin" : [725, 542, 390]}})
```

이 쿼리는 당첨된 추첨권 번호를 가지지 않은 모든 사람을 반환합니다.

`$in` 은 하나의 키에 대해 OR 연산을 제공하는데, 만약 `ticket_no` 가 725 이거나 `winner` 가 `true` 인 문서를 찾고 싶을 땐, `$or` 연산자를 사용하여 해결 가능합니다. `$or` 은 가으한 조건들의 배열을 취합니다. 추첨권 예제에 다음과 같이 `$or` 연산자를 사용할 수 있습니다.

```js
> db.raffle.find({"$or" : [{"ticket_no" : 725}, {"winner" : true}]})
```

`$or` 은 다른 조건절도 포함할 수 있습니다. 예를 들어 `ticket_no` 가 세 번호 중 하나라도 일치하거나 `winner` 가 `true` 인 경우를 찾으면 다음과 같이 할 수 있습니다.

```js
> db.raffle.find({"$or" : [{"ticket_no" : {"$in" : [725, 542, 390]}}, {"winner" : true}]})
```

일반적인 `AND` 형 쿼리에서는 최소한의 인자로 최대한의 결과를 추려내야 합니다. 하지만 `OR` 형 쿼리는 반대입니다. 가장 첫 번째 인자가 많은 문서와 일치할수록 더 효율적입니다.

`$or` 연산자가 항상 작동하는 동안에는, 쿼리 옵티마이저가 이를 효유렂ㄱ으로 다룰 수 있도록 가능한 한 `$in` 을 사용합니다.

### $not

`$not` 은 메타 조건절이며 어떤 조건에도 적용할 수 있습니다. 예를 들어 나머지 연산자 `$mod` 를 생각 해보겠습니다. `$mod` 는 Key 의 값을 첫 번째 값으로 나눈 후 그 나머지 값의 조건을 두 번째 값으로 기술하는 연산자입니다. 다음은 `$mod` 연산자로 문서를 쿼리하는 예제입니다.

```js
> db.users.find({"id_num" : {"$mod" : [5, 1]}})
```

위 쿼리는 1, 6, 11, 16 등의 `id_num` 을 가지는 사용자를 반환합니다. 2, 3, 4, 5, 7, 8, 9, 10, 12 등의 `id_num` 을 가진 사용자를 받으려면 `$not` 을 사용합니다.

`$not` 은 특히 정규표현식과 함께 사용해서 주어진 패턴과 일치하지 않는 문서를 찾을 때 유용합니다.

### Conditional Semantics

하나의 Key 에 여러 조건을 지정할 수 있습니다. 예를 들어 20 세와 30 세 사이의 모든 사용자를 찾을 때는 `age` 키에 `$gt` 와 `$lt` 를 사용합니다.

```
> db.users.find({"age" : {"$lt" : 30, "$gt" : 20}})
```

하지만 하나의 Key 에 여러 갱신 제한자를 사용할 수 없습니다. 예를 들어 `{"$inc" : {"age" : 1}, "$set" : {age: 40}}` 과 같은 갱신 제한자는 `age` 를 2 번 수정하기 때문에 사용할 수 없습니다. 쿼리 조건절에는 이런 규칙이 적용되지 않습니다.

`$and`, `$or`, `$nor` 과 같이 외부 문서의 안으로 들어갈 수 있는 몇몇 메타 연산자가 존재합니다. 이들은 모두 다음과 같이 비슷한 형태를 가집니다.

```js
> db.users.find({"$and" : [{"x" : {"$lt" : 1}}, {"x" : 4}]})
```

위 쿼리는 `x` 필드가 1 보다 작은 경우와 4 와 같은 경우 둘다 일치하는 문서를 찾습니다. 이는 모순된 상황처럼 보이지만 `x` 필드가 배열 `{"x" : [0, 4]}` 와 일치하면 가능합니다.

쿼리 옵티마이저는 다른 연산들처럼 `$and` 에 대해 최적화를 수행하지 않습니다. 이 쿼리는 다음과 같이 구조를 잡는 것이 더 효율적입니다.

```js
> db.users.find(["x" : {"$lt" : 1, "$in" : [4]}])
```

## Type-Specific Queries

MongoDB 는 문서 내에서 다양한 데이터형을 사용할 수 있습니다. 이들 중 일부는 쿼리 시 형에 특정하게 작동합니다.

### null

`null` 은 다른 DB 와 다르게 행동합니다. `null` 은 스스로와 일치하는 것을 찾습니다. 아래와 같이 문서들의 컬렉션이 있다 가정하겠습니다.

```js
> db.c.find()
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523621"), "y" : null }
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523622"), "y" : 1 }
{ "_id" : ObjectId("4ba0f148d22aa494fd523623"), "y" : 2 }
```

`y` Key 가 `null` 인 문서를 쿼리한 예상 결과는 다음과 같습니다.

```js
> db.c.find({"y" : null})
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523621"), "y" : null }
```

하지만 `null` 은 자신과 일치하는 것 뿐만 아니라 *존재하지 않는* 것과도 일치합니다. 그러므로 Key 가 `null` 인 값을 쿼리하면 해당 Key 를 가지고 있지 않은 문서도 반환할 것입니다.

```js
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523621"), "y" : null }
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523622"), "y" : 1 }
{ "_id" : ObjectId("4ba0f148d22aa494fd523623"), "y" : 2 }
```

만약 `null` 인 Key 만 찾고 싶으면 Key 가 `null` 인 값을 쿼리하고 `$exists` 조건절을 사용해 `null` 존재 여부를 확인하면 됩니다.

```js
> db.c.find({"z" : {"$in" : [null], "$exists" : true}})
```

불행하게도 `$eq` 연산자는 없습니다. 하지만 `$in` 에 하나의 조건을 배열 요소로 넣어 사용하면 됩니다.

### Regular Expressions

정규 표현식은 유연하게 매칭되는 문자열을 찾아낼 때 유용합니다. 예를 들어 이름이 Joe 이거나 joe 인 사용자 모두를 찾아내고자 할 때 정규표현식을 이용하면 대소문자 구분 없이 찾을 수 있습니다.

```js
> db.users.find({"name" : /joe/i})
```

정규표현식의 플래그는 사용할 수 있으나 꼭 필요한 것은 아닙니다. joe 뿐만 아니라 joey 를 찾기 원한다면 다음과 같이 바꾸면 됩니다.

```js
> db.users.find({"name" : /joey?/i})
```

MongoDB 는 정교표현식ㄱ의 매칭을 위해 **Perl Compatible Regular Expression, PCRE** 라이브러리를 사용하며, PCRE 에서 사용하는 모든 문법을 사용할 수 있습니다. 실제 쿼리하기 전에 자바스크립트 쉘로 해당 정규표현식이 의도한 대로 동작하는지 확인해 보는 것이 좋습니다.

정규표현식 또한 스스로와 일치하는 문서를 찾을 수 있습니다. 데이터베이스에 정규표현식을 입력하는 사람은 매우 드물지만, 만약 삽입했다면 찾을 수 있습니다.

```js
> db.foo.insert({"bar" : /baz/})
> db.foo.find({"bar" : /baz/})
{
 "_id" : ObjectId("4b23c3ca7525f35f94b60a2d"),
 "bar" : /baz/
}
```

### Querying Arrays

배열 요소에 대한 쿼리는 전체 수량에 대한 쿼리를 수행하기 위한 방식으로 설계되어 있습니다. 예를 들어 배열이 다음과 같은 파일 목록이라 가정하겠습니다.

```js
> db.food.insert({"fruit" : ["apple" , "banana" , "peach"]})
```

`{"fruit" : "apple" , "fruit" : "banana", "fruit" : "peach"}` 와 같은 문서를 가졌다고 가정했을 때와 대체로 비슷하게 쿼리를 수행해 볼 수 있습니다.

**1. $all**

만약 배열 내 하나 이상의 요소와 일치하는 배열을 찾으려면 `$all` 을 사용합니다. 이는 배열 내 여러요소와 일치하는지 확인하도록 해줍니다. 예를 들어 다음 세 문서로 구성된 컬렉션을 만든다고 가정하겠습니다.

```js
> db.food.insert({"_id" : 1, "fruit" : ["apple", "banana", "peach"]})
> db.food.insert({"_id" : 2, "fruit" : ["apple", "kumquat", "orange"]})
> db.food.insert({"_id" : 3, "fruit" : ["cherry", "banana", "apple"]})
```

`apple` 과 `banana` 요소를 `$all` 연산자와 함께 써서 해당 문서를 찾을 수 있습니다.

```js
> db.food.find({fruit : {$all : ["apple", "banana"]}})
 {"_id" : 1, "fruit" : ["apple", "banana", "peach"]}
 {"_id" : 3, "fruit" : ["cherry", "banana", "apple"]}
```

순서는 중요하지 않습니다. 두 번째 결과에서 `banana` 가 `apple` 보다 먼저 나타난 것을 주목하면 됩니다. 요소가 하나뿐일 때는 `$all` 연산자 사용 여부와 관계 없이 결과는 같습니다. 예를 들어 `{fruit : {$all : ["apple"]}}` 은 `{fruit : "apple"}` 과 같습니다.

또한 전체 배열과 정확하게 일치하는 문서를 쿼리할 수 있습니다. 당연히 완벽히 일치하지 않으면 안됩니다. 예를 들어 아래의 쿼리는 이전에 나온 첫 번째 문서와 일치합니다.

```js
> db.food.find({"fruit" : ["apple", "banana", "peach"]})
```

그러나 아래와 같을 땐 일치하지 않습니다.

```js
> db.food.find({"fruit" : ["apple", "banana"]})
```

아래 역시 마찬가지입니다.

```js
> db.food.find({"fruit" : ["banana", "apple", "peach"]})
```

배열 내 특정 요소를 쿼리하려면 *key.index* 구문을 이용하여 순서를 지정합니다.

```js
> db.food.find({"fruit.2" : "peach"})
```

배열은 항상 0 에서 시작하므로 배열의 3 번째 요소와 `peach` 문자열이 일치하는지 확인합니다.

**2. $size**

배열을 쿼리하기 위한 유용한 조건절은 주어진 크기의 배열을 반환하는 `$size` 입니다.

```js
> db.food.find({"fruit" : {"$size" : 3}})
```

자주 쓰이는 쿼리 중 하나는 크기의 범위로 쿼리하는 것입니다. `$size` 는 다른 $ 조건절과 결합하여 사용할 수 없지만, 문서에 `$size` Key 를 추가하면 이런 쿼리를 처리할 수 있습니다. 그리고 배열에 요소를 추가할 때마다 `size` 값을 증가시키면 됩니다. 원래의 갱신 구문이 다음과 같다고 가정하겠습니다.

```js
> db.food.update(criteria, {"$push" : {"fruit" : "strawberry"}})
```

다음과 같이 간단하게 바꿀 수 있습니다.

```js
> db.food.update(criteria, {"$push" : "fruit" : "strawberry"}, "$inc" : {"size" : 1})
```

값의 증가는 매우 빠르게 이루어지므로 성능에 대해서는 크게 걱정할 필요가 없습니다. 위와 같이 문서를 저장하고 나면 다음과 같은 쿼리가 가능합니다.

```js
> db.food.find({"size" : {"$gt" : 3}})
```

불행하게도 이 기능은 `$addToSet` 연산자와는 작동하지 않습니다.

**3. The $slice operator**

특수한 `$slice` 연산자를 사용해 배열 요소의 부분집합을 반환받을 수 있습니다.

예를 들어 블로그 게시물에 먼저 달린 댓글 10 개를 반환받길 원한다고 가정하겠습니다.

```js
> db.blog.posts.findOne(criteria, {"comments" : {"$slice" : 10}})
```

나중에 달린 댓글 10 개를 원하면 -10 을 지정하면 됩니다.

```js
> db.blog.posts.findOne(criteria, {"comments" : {"$slice" : -10}})
```

`$slice` 는 또한 오프셋과 요소 개수를 사용하여 원하는 범위에 있는 결과를 반환할 수 있습니다.

```js
> db.blog.posts.findOne(criteria, {"comments" : {"$slice" : [23, 10]}})
```

이 쿼리는 24 번째 인덱스에 있는 값부터 10 개를 반환합니다. 만약 값이 34개가 되지 않는 경우 현재 있는 값 까지만 반환합니다.

특별히 명시하지 않는 한 `$slice` 연산자는 문서내 모든 Key 를 반환합니다. 이는 명시하지 않은 Key 를 반환하지 않는 다른 Key 명시자들과는 다릅니다. 아래와 같은 블로그 게시물이 있다고 하겠습니다.

```js
{
    "_id" : ObjectId("4b2d75476cc613d5ee930164"),
    "title" : "A blog post",
    "content" : "...",
    "comments" : [
        {
            "name" : "joe",
            "email" : "joe@example.com",
            "content" : "nice post."
        },
        {
            "name" : "bob",
            "email" : "bob@example.com",
            "content" : "good post."
        }
    ]
}
```

마지막 댓글을 얻기 위해 `$slice` 연산자를 추가한 결과는 다음과 같습니다.

```js
> db.blog.posts.findOne(criteria, {"comments" : {"$slice" : -1}})
{
    "_id" : ObjectId("4b2d75476cc613d5ee930164"),
    "title" : "A blog post",
    "content" : "...",
    "comments" : [
        {
            "name" : "bob",
            "email" : "bob@example.com",
            "content" : "good post."
        }
    ]
}
```

Key 명시자에 직접 지정하지 않아도 `title` 과 `content` Key 모두 반환합니다.

**4. Returning a matching array element**

구성 요소의 인덱스를 알고 있는 경우 `$slice` 연산자가 도움이 될 수 있지만, 때로는 뭐든지간에 기준과 일치하는 배열 값을 원할 수 있습니다. $ 연산자로 일치하는 값을 반환할 수 있습니다. 위에 주어진 블로그 예제에서 밥의 댓글을 얻으려면 다음과 같이 하면 됩니다.

```js
> db.blogs.posts.find({"comments.name" : "bob"}, {"comments.$" : 1})
{
    "_id" : ObjectId("4b2d75476cc613d5ee930164"),
    "comments" : [
        {
            "name" : "bob",
            "email" : "bob@example.com",
            "content" : "good post."
        }
    ]
}
```

위 쿼리는 각 문서에서 첫 번째로 일치하는 댓글만 반환함을 알려줍니다. 만약 밥이 여러 댓글을 남겼다면 `comments` 배열에 존재하는 첫 번째 댓글만 반환될 것입니다.

**5. Array and range query interactions**

문서내 스칼라는 쿼리 기준의 각 절을 일치시켜야 합니다. 예를 들어 `{"x" : {"$gt" : 10, "$lt" : 20}}` 과 같이 쿼리했다면 `x` 는 10 보다 크고 20 보다 작을것입니다. 하지만 만약 문서의 `x` 필드가 배열이라면, 기준의 각 부분에 대해 일치하지만 각 쿼리 절이 다른 배열 요소와 일치하는 `x` 값이 있는 경우에는 문서와 일치시킵니다.

이 작업을 이해하는 가장 좋은 방법은 예제를 참조하는것입니다.

```js
{"x" : 5}
{"x" : 15}
{"x" : 25}
{"x" : [5, 25]}
```

만약 `x` 의 값이 10 에서 20 사이인 모든 문서를 찾기 원한다면 순진하게 `db.test.find({"x" : {"$gt" : 10, "$lt" : 20}})` 과 같이 쿼리를 구성하고, `{"x" : 15}` 라는 단 하나의 결과 문서만 기다릴것입니다. 하지만 이를 실행하면 다음과 같은 두 결과 문서를 얻게 됩니다.

```js
> db.test.find({"x" : {"$gt" : 10, "$lt" : 20}})
{"x" : 15}
{"x" : [5, 25]}
```

MongoDB 에서 이 문제를 해결하기 위해 양쪽 절을 하나의 배열 요소와 비교하도록 하는 `$elemMatch` 연산자를 사용할 수 있습니다. 하지만 `$elemMatch` 연산자는 비 배열 요소를 일치시키지 않는 점을 조심해야 합니다.

```js
> db.test.find({"x" : {"$elemMatch" : {"$gt" : 10, "$lt" : 20}}})
```

하지만 위 결과는 `x` 필드가 배열이 아니기 때문에 아무 값도 반환하지 않습니다.

`$gt` 와 `$lt` 값 사이를 쿼리하도록 인덱스 범위를 제한하기 위해 `min()` 과 `max()` 함수를 사용해야합니다.

```js
> db.test.find({"x" : {"$gt" : 10, "$lt" : 20}})
    .min({"x" : 10})
    .max({"x" : 20})
{"x" : 15}
```

### Querying on Embedded Documents

내장 문서 쿼리는 전체 문서를 대상으로 하는 방식과 Key / Value 쌍을 대상으로 하는 방식이 있습니다.

전체 문서를 대상으로 하는 방식이 일반적인 쿼리입니다. 다음과 같은 문서가 있다고 가정하겠습니다.

```js
{
    "name" : {
        "first" : "Joe",
        "last" : "Schmoe"
    },
    "age" : 45
}
```

아래와 같이 Joe Schmoe 라는 사람을 쿼리할 수 있습니다.

```js
> db.people.find({"name" : {"first" : "Joe", "last" : "Schmoe"}})
```

하지만 전체 하위 문서에 대한 쿼리는 정확히 하위 문서와 일치해야 합니다. 만약 Joe 가 가운데 이름 필드를 추가하게 되면 전체 문서가 일치하지 않기 때문에 더 이상 작동하지 않습니다. 이러한 형태의 쿼리는 또한 순서도 따지기 때문에 `{"first" : "Joe", "last" : "Schmoe"}` 도 일치하지 않습니다.

가능하면 내장 문서를 쿼리할 때는 특정 키로 쿼리하는 방법이 좋습니다. 내장 문서의 Key 를 쿼리할 때는 점 표기법을 사용하면 됩니다.

```js
> db.people.find({"name.first" : "Joe", "name.last" : "Schmoe"})
```

내장 문서의 구조가 복잡해지면 일치하는 내장 문서를 찾기가 더 어려워집니다. 예를 들어 블로그 게시물 중 5 점 이상을 받은 Joe 의 댓글을 찾는다 가정하겠습니다. 게시물은 다음과 같이 모델링 할 수 있습니다.

```js
> db.blog.find()
{
    "content" : "...",
    "comments" : [
        {
            "author" : "joe",
            "score" : 3,
            "comment" : "nice post"
        },
        {
            "author" : "mary",
            "score" : 6,
            "comment" : "terrible post"
        }
    ]
}
```

이때 `db.blog.find({"comments" : {"author" : "joe", "score" : {"$get" : 5}}})` 로 쿼리할 수 없습니다. 내장 문서는 전체 문서가 다 일치해야 하지만 이 쿼리 문서는
`comments` 키가 없기 떄문입니다. `db.blog.find({"comments.author" : "joe", "comments.score" : {"$get" : 5}})` 도 작동하지 않습니다.

이는 댓글의 `score` 조건과 `author` 조건은 댓글 배열 내의 각기 다른 댓글 문서와 일치할 수 있기 때문입니다. 즉, 직전의 문서를 그대로 반환하게 되는데, 이는 첫 번째 댓글의 `"author" : "joe"` 와 2 번째 댓글의 `"score" : 6` 이 조건과 일치하기 때문입니다.

모든 Key 를 지정하지 않고 조건을 정확하게 묶으려면 `$elemMatch` 를 사용합니다. 이름의 조건절은 배열 내에서 하나의 내장 문서를 찾기 위한 조건을 부분적으로 지정할 수 있도록 해줍니다. 정확한 쿼리는 다음과 같습니다.

```js
> db.blog.find({"comments" : {"$elemMatch" : {"author" : "joe",
                                            "score" : {"$gte" : 5}}}})
```

`$elemMatch` 는 조건의 그룹화를 지원합니다. 따라서 내장 문서에 하나 이상의 Key 에 대한 조건과 일치 여부를 확인할 때만 필요합니다.

## $where Queries

Key / Value 만으로도 꽤 다양한 쿼리를 할 수 있습니다. 정확하게 표현할 수 없는 쿼리도 있습니다. 다른 방법으로 표현할 수 없는 쿼리는 임의의 자바스크립트를 쿼리의 일부분으로 실행할 수 있는 `$where` 절을 사용하면 됩니다. 이를 통해 어떤 쿼리라도 표현할 수 있습니다.

보안상의 이유로 `$where` 절의 사용은 크게 제한되어야 합니다. 최종 사용자가 임의의 `$where` 절을 실행하지 못하게 해야 합니다.

`$where` 절을 가장 자주 쓰는 경우로 문서 내 두 Key 의 값을 비교하는 쿼리를 들 수 있습니다. 예를 들어 다음과 같은 문서가 있다고 가정하겠습니다.

```js
> db.foo.insert({"apple" : 1, "banana" : 6, "peach" : 3})
> db.foo.insert({"apple" : 8, "spinach" : 4, "watermelon" : 4})
```

두 필드의 값이 동일한 문서를 반환받고 싶을 것입니다. 예를 들어 2 번째 문서에서 `spinach` 와 `watermelon` 이 같은 값을 가지고 있기 때문에 이 문서를 반환받고 싶은 것입니다. 하지만 MongoDB 는 이런 $ 조건절을 제공하지 않으므로 `$where` 절 내 자바스크립트로 처리해야 합니다.

```js
> db.foo.find({"$where" : function () {
... for (var current in this) {
...     for (var other in this) {
...         if (current != other && this[current] == this[other]) {
...             return true;
...         }
...     }
... }
... return false;
... }});
```

이 함수가 `true` 를 반환하면 해당 문서는 결과 셋에 포함되며, `false` 면 포함되지 않습니다.

`$where` 쿼리는 일반 쿼리보다 훨씬 느리기 때문에 반드시 필요한 경우가 아니면 사용하지 말아야 합니다. `$where` 절 실행시 각 문서는 BSON 에서 자바스크립트 객체로 변환되어야 하기 떄문입니다. 또한, `$where` 절에 쓸 수 있는 인덱스도 없습니다.

`$where` 절과 다른 쿼리 필터를 함께 사용하면 성능 저하를 줄일 수 있습니다. 가능하면 `$where` 절이 아닌 조건은 색인을 통해 거르고 `$where` 절은 결과를 세부 방식으로 조정하는 방식으로 사용합니다.

### Server-Side Scripting

서버에서 자바스크립트를 수행할 때는 보안에 매우 주의해야 합니다. 입력을 받아들이는 일정한 규칙을 준수하면 안전하게 사용할 수 있습니다. 또는 `--noscripting` 옵션으로 `mongod` 를 실행하여 사용할 수 있습니다.

자바스크립트에서 보안 문제는 모두 서버에서 제공 프로그램을 수행하는 것과 관련되어 있습니다. 이를 피하려면 사용자의 입력을 받아들이지 않고 이를 직접 `mongod` 로 넘기는지 확인합니다. 예를 들어 사용자에 의해 `name` 이 제공되어 **Hello, *name*!** 형태로 출력 되도록 원한다고 가정하겠습니다. 다음과 같이 자바스크립트 함수를 쓸 수 있습니다.

```js
> func = "function() { print('Hello, "+name+"!'); }"
```

만일 `name` 이 사용자 정의 변수라면 다음과 같이 변환할 수 있는 `'); db.dropDatabase(); print('` 형태의 문자열일 수 있습니다.

```js
> func = "function() { print('Hello, '); db.dropDatabase(); print('!'); }"
```

이제 이 코드를 실행시키면 전체 데이터베이스가 삭제됩니다. 이러한 사고를 방지하기 위해 이름을 전달하는 유효 범위(Scope) 를 사용해야 합니다. 예를 들어 Python 에선 다음과 같이 나타낼 수 있습니다.

```python
func = pymongo.code.Code("function() {
    print('Hello, '+username+'!'); }", {"username": name}
})
```

이제 데이터베이스에 아무런 해를 끼치지 않고 다음과 같이 출력합니다.

```js
Hello, '); db.dropDatabase(); print('!
```

코드가 실제로 문자열과 유효 범위를 합성할 수 있기 때문에, 대부분의 드라이버는 데이터베이스에 전송하기 위한 특별한 유형의 전송 코드를 가지고 있습니다. 유효 범위는 변수 이름을 값으로 매핑한 문서입니다.

이러한 매핑값은 자바스크립트 함수가 실행 중인 로컬 범위가 됩니다. 그러므로 위 예에서 함수는 문자열 형태의 값을 가지는 `username` 이라는 변수에 접근할 수 있습니다.

## Cursors

데이터베이스는 **커서(cursor)** 를 사용하여 `find` 의 결과를 반환합니다. 커서 구현체들은 쿼리의 최종 결과에 대해 강력한 제어권을 제공합니다. 결과의 수를 제한하고 몇개 건너뛰거나 여러 키의 조합으로 어떤 방향으로도 정렬할 수 있습니다.

쉘로 커서를 생성하기 위해서는 문서들을 컬렉션에 집어넣고, 그에 대해 쿼리를 수행하고 결과를 지역변수에 할당하면 됩니다. 여기서는 아주 간단한 컬렉션을 생성하고 쿼리를 수행한 다음에 결과를 `cursor` 변수에 저장했습니다.

```js
> for(i=0; i<100; i++) {
... db.c.insert({x : i});
... }
> var cursor = db.collection.find();
```

이렇게 하면 결과를 한 번에 하나씩 볼 수 있는 장점이 있습니다. 전역변수에 결과를 저장하거나 아예 변수가 없다면, MongoDB 쉘은 자동으로 결과를 훑으며 처음 몇 문서를 표시할 것입니다. 이 부분까지는 지금까지 우리가 봐온것이고, 컬렉션 내 무엇이 들어 있는지 보기위해 자주 쓰는 동작 방식입니다. 하지만 쉘에서 실제 프로그래밍하기에는 적합하지 않습니다.

결과를 얻기위해서 커서는 `next` 메서드를 사용합니다. 다음 결과가 있는지 확인할 때는 `hasNext` 를 사용합니다.

```js
> while (cursor.hasNext()) {
... obj = cursor.next();
... // do stuff
... }
```

또한 `cursor` 클래스는 자바스크립트의 **반복자(iterator)** 인터페이스를 구현했기 때문에 `forEach` 반복문을 사용할 수 있습니다.

```js
> var cursor = db.people.find();
> cursor.forEach(function(x) {
... print(x.name);
... });
adam
matt
zak
```

`find` 를 호출할 때 쉘이 데이터베이스를 즉시 쿼리하지 않습니다. 실제로 결과를 요청하는 쿼리를 보낼 때까지 기다리므로 쿼리를 수행하기 전에 옵션을 추가할 수 있습니다. 또한 커서 객체 상의 모든 메소드는 커서 자체를 반환하기 때문에 이 옵션들을 어떤 순서로도 이어 쓸 수 있습니다.

예를 들어 다음 쿼리는 모두 동일하게 작동합니다.

```js
> var cursor = db.foo.find().sort({"x" : 1}).limit(1).skip(10);
> var cursor = db.foo.find().limit(1).sort({"x" : 1}).skip(10);
> var cursor = db.foo.find().skip(10).limit(1).sort({"x" : 1});
```

이 시점에서 쿼리는 아직 수행되지 않습니다. 이 함수들은 단지 쿼리를 만들기만 했습니다. 다음 메소드를 호출한다고 가정하겠습니다.

```js
> cursor.hasNext()
```

이 시점에서 쿼리가 서버로 전송됩니다. 쉘은 `next` 나 `hasNext` 메소드 호출 시 서버까지의 왕복 횟수를 줄이기 위해 한 번에 처음 100 개 또는 4 MB 크기의 결과를 가져옵니다. 클라이언트가 첫 번째 결과 셋을 살펴본 후에, 쉘은 다시 데이터베이스에 접근하여 `getMore` 요청을 통해 더 많은 결과를 요구합니다. `getMore` 요청은 기본적으로 쿼리에 대한 식별자를 보유하고 DB가 다음 배치를 반환하도록 요구합니다. 이 프로세스는 모든 결과를 반환해 커서가 소진될 때까지 계속 됩니다.

### Limits, Skips, and Sorts

일반적인 쿼리 옵션은 반환받은 결과 수를 limit, skip, sort 하는 정도가 있습니다. 이런 옵션은 쿼리가 데이터베이스에 전송되기 전에 추가되어야 합니다.

결과수에 제한을 두려면 `find` 호출에 `limit` 함수를 연결합니다. 예를 들어 3 개의 결과만 받고자 하면 다음과 같이 수행합니다.

```js
> db.c.find().limit(3)
```

컬렉션에서 쿼리 조건과 맞는 결과가 3개보다 적다면 조건과 맞는 문서의 수만큼만 반환합니다.

`skip` 은 `limit` 과 유사하게 작동합니다.

```js
> db.c.find().skip(3)
```

조건과 맞는 처음 3 개의 결과를 건너뛰고 그 나머지 결과를 반환합니다. 만약 조건과 맞는 결과가 3 개 이하면 아무런 결과도 반환하지 않습니다.

`sort` 는 객체를 매개변수로 받습니다. 이 매개변수는 Key / Value 쌍의 셋이고, Key 는 Key 의 이름이고 Value 는 정렬 방향입니다. 정렬방향이 1 (오름차순) 또는 -1 (내림차순) 이 될 수 있습니다.

`username` 은 오름차순, `age` 는 내림차순으로 정렬하려면 다음과 같이 사용합니다.

```js
> db.c.find().sort({username : 1, age : -1})
```

이 3 개의 메소드는 조합하여 사용할 수 있습니다. 예를 들어 온라인 상점에 고객이 들어와 mp3 를 검색한다고 가정하겠습니다. 가격을 내림차순으로 정렬해 한 페이지당 50 개씩 결과를 보여주고 싶으면 다음과 같이 합니다.

```js
> db.stock.find({"desc" : "mp3"}).limit(50).sort({"price" : -1})
```

만약 다음 페이지를 클릭했을때 더 많은 결과를 보여 주고 싶으면 쿼리에 `skip` 을 추가하면 됩니다.

```js
> db.stock.find({"desc" : "mp3"}).limit(50).skip(50).sort({"price" : -1})
```

**1. Comparison order**

MongoDB 는 데이터형을 비교하는 위계 구조가 있습니다. 여러 데이터형이 섞여 있는 키를 정렬할 때는 미리 정의된 순서가 있습니다. 다음은 데이터형을 최솟값에서 최댓값 순으로 나타낸 것입니다.

1. Minimum value
2. null
3. Numbers (integers, longs, doubles)
4. Strings
5. Object/document
6. Array
7. Binary data
8. Object ID
9. Boolean
10. Date
11. Timestamp
12. Regular expression
13. Maximum value

### Avoiding Large Skips

문서가 적을때는 `skip` 을 사용해도 무리가 없습니다. 하지만 `skip` 은 모든 생략된 결과물을 발견하기 폐기해야 하기 때문에 결과가 많으면 느려집니다. 대부분 데이터베이스는 `skip` 을 위해 인덱스 안에 메타데이터를 저장하지만, MongoDB 는 지원하지 않습니다. 따라서 많은 수의 건너뛰기는 피해야 합니다. 종종 직전 쿼리의 결과를 기반으로 하여 다음 쿼리를 계산할 수 있습니다.

**1. Paginating results without skip**

페이지를 나누는 가장 쉬운 방법은 `limit` 을 사용하여 첫 번째 페이지를 반환하고, 다음 페이지들은 첫 페이지부터 오프셋을 주어 반환하는 것입니다.

```js
> // do not use: slow for large skips
> var page1 = db.foo.find(criteria).limit(100)
> var page2 = db.foo.find(criteria).skip(100).limit(100)
> var page3 = db.foo.find(criteria).skip(200).limit(100)
...
```

하지만 쿼리에 따라 `skip` 을 사용하지 않는 방법을 찾을 수 있습니다. 예를 들어 `date` 를 내림차순으로 정렬해서 문서를 표시한다고 가정하겠습니다. 첫 페이지는 다음과 같이 구할 수 있습니다.

```js
> var page1 = db.foo.find().sort({"date" : -1}).limit(100)
```

그리고 다음 페이지를 가져오기 위해 마지막 문서의 `date` 값을 사용할 수 있습니다.

```js
var latest = null;
// display first page
while (page1.hasNext()) {
    latest = page1.next();
    display(latest);
}
// get next page
var page2 = db.foo.find({"date" : {"$gt" : latest.date}});
page2.sort({"date" : -1}).limit(100);
```

이제 쿼리는 `skip` 을 사용할 필요 없습니다.

**2. Finding a random document**

랜덤으로 문서를 가져오는 방법 중 가장 간단하고 느린 방법은 문서의 전체 개수를 세고 `find` 를 수행한 뒤, 0 부터 컬렉션 크기 사이에서 랜덤으로 정해진 숫자만큼 건너뛰는 것입니다.

```js
> // do not use
> var total = db.foo.count()
> var random = Math.floor(Math.random()*total)
> db.foo.find().skip(random).limit(1)
```

이는 매우 비효율적입니다. 전체 컬렉션을 탐색해야하며, 큰 수의 요소를 건너뛰어야 하기 때문에 오래 걸립니다.

문서를 입력할 때 랜덤 키를 별도로 추가하면 효율적으로 랜덤으로 문서를 찾을 수 있습니다. 예를 들어 쉘을 사용하고 있다면 `Math.random()` 함수를 사용할 수 있습니다.

```js
> db.people.insert({"name" : "joe", "random" : Math.random()})
> db.people.insert({"name" : "john", "random" : Math.random()})
> db.people.insert({"name" : "jim", "random" : Math.random()})
```

이제 `skip` 대신 랜덤 수를 계산하여 사용할 수 있습니다.

```js
> var random = Math.random()
> result = db.foo.findOne({"random" : {"$gt" : random}})
```

`random` 값이 컬랙션 내 어떤 `random` 값보다 클 수 있어 빈 결과를 반환할 수 있습니다. 이런 경우에 문서를 다른 방향으로 반환함으로써 빈 결과를 반환하는 것을 간단히 방지할 수 있습니다.

```js
> if (result == null) {
... result = db.foo.findOne({"random" : {"$lt" : random}})
... }
```

컬렉션 내 아무런 문서가 존재하지 않으면 이 방법은 당연이 `null` 을 반환하고 끝날 것입니다.

이 방법은 복잡한 쿼리에 적합합니다. 다만 랜덤 Key 가 인덱스를 가지는지 명확해야 합니다. 예를 들어 랜덤으로 배관공을 찾고자 할 때, `profession` 과 `stat` 과 `random` 에 인덱스를 생성하면 됩니다.

```js
> db.people.ensureIndex({"profession" : 1, "state" : 1, "random" : 1})
```

### Advanced Query Options

쿼리 종류는 **감싼(wrapped)** 형과 **일반(plain)** 형이 있습니다. 일반적인 쿼리는 다음과 같습니다.

```js
> var cursor = db.foo.find({"foo" : "bar"})
```

쿼리를 감쌀 때 몇 가지 옵션이 존재하며, 한 예로 정렬을 수행한다 가정하겠습니다.

```js
> var cursor = db.foo.find({"foo" : "bar"}).sort({"x" : 1})
```

`{"foo" : "bar"}` 를 데이터베이스에 쿼리로 보내는 대신, 쿼리는 더 큰 문서에 감싸입니다. 쉘은 쿼리의 형태를 `{"foo" : "bar"}` 에서 `{"$query" : {"foo" : "bar"}, "$orderby" : {"x" : 1}}` 로 변환합니다.

대부분의 드라이버는 쿼리에 임의의 옵션을 추가하기 위한 보조자 기능을 제공합니다. 다른 유용한 옵션에 대해 알아보겠습니다.

**$maxScan : 정수**

쿼리에서 살펴볼 문서의 최대 수를 지정합니다.

**$min : 문서**

쿼리에 대한 시작 조건입니다.

**$max : 문서**

쿼리에 대한 끝 조건입니다.

### Getting Consistent Results

일반적으로 데이터는 MongoDB 에서 데이터를 꺼내고, 가공하고 다시 저장하는 과정을 거칩니다.

```js
cursor = db.foo.find();
while (cursor.hasNext()) {
 var doc = cursor.next();
 doc = process(doc);
 db.foo.save(doc);
}
```

결과의 수가 적을 경우에는 문제가 없지면 결과가 많을 떄는 처리에 문제가 생깁니다. 아래 `Example 1` 처럼 컬렉션을 문서의 목록으로 나타낼 수 있습니다. 문서를 눈송이로 표현하겠습니다.

> Example 1 - A collection being queried

![image](https://user-images.githubusercontent.com/44635266/74657556-d1ead980-51d3-11ea-81ee-9a3b35783149.png)

`find` 를 호출하면 커서는 컬렉션의 시작 부분부터 결과를 반환하며, 오른쪽으로 이동합니다. 프로그램은 처음 100 개의 문서를 가져와서 처리합니다. 처리한 문서를 다시 데이터베이스에 저장할 때 `Example 2` 와 같이 문서의 크기가 증가해 기존에 할당해 둔 추가 공간에 맞지 않으면 재배치됩니다. 일반적으로 `Example 3` 과 같이 컬렉션 마지막에 재배치 됩니다.

> Example 2 - An enlarged document may not fit where it did before

![image](https://user-images.githubusercontent.com/44635266/74657557-d31c0680-51d3-11ea-8e70-64f33abdfe3d.png)

> Example 3 - MongoDB relocates updated documents that don’t fit in their original position

![image](https://user-images.githubusercontent.com/44635266/74657562-d4e5ca00-51d3-11ea-8612-26d2cf36c7e5.png)

프로그램 문서들은 묶음을 계속해서 가져옵니다. 끝에 다다르면 재배치한 문서를 반환합니다.

> Example 4 - A cursor may return these relocated documents again in a later batch

![image](https://user-images.githubusercontent.com/44635266/74657565-d616f700-51d3-11ea-99f0-3d64d4c65ebf.png)

이러한 문제를 해결하려면 쿼리의 스냅샷을 찍어야 합니다. `$snapshot` 옵션을 추가하면 쿼리는 한번에 하나의 문서만 반환하는 `_id` 인덱스를 탐색하여 실행합니다. 예를 들어 `db.foo.find()` 대신 다음을 실행할 수 있습니다.

```js
> db.foo.find().snapshot()
```

스냅샷은 쿼리를 느리게 하기 때문에 필요한 순간에만 사용해야 합니다.

결과를 한 묶음으로 반환하는 모든 쿼리는 효과적으로 스냅샷을 찍을 수 있습니다. 커서가 결과의 다른 작업을 얻기 위해 대기하는 동안 컬렉션에 커서를 변경할 때만 데이터 불일치가 발생합니다.

### Immortal Cursors

커서에는 두 가지 측면이 있습니다. 클라이언트가 보는 커서와 클라이언트 커서가 나타내는 데이터베이스 커서입니다.

서버 측면에서 보면 커서는 메모리와 자원을 점유합니다. 커서가 결과를 가져오거나 클라이언트가 끝내라는 요청을 하면 데이터베이스는 사용하고 있던 자원을 해제합니다. 이렇게 자원을 해제하면 커서 역시 신속하게 해제해야 합니다.

서버 커서를 종료하는 몇 가지 조건이 있습니다.

첫 번째로 커서는 조건과 일치하는 결과를 모두 살펴본 후에 스스로 정리합니다.

두 번째로 커서가 클라이언트 측에서 유효 영역 바깥으로 나갈 경우 드라이버는 데이터베이스에 특별한 메세지를 보내 커서를 종료해도 된다고 알립니다.

마지막으로 사용자가 결과를 다 살펴보지 않았는데 커서가 10 분동안 활동이 없으면 자동으로 죽습니다.

일반적으로 Timeout 에 의한 종료는 정상적인 동작 방식입니다. 가끔 커서를 오래 남겨두고 싶어 `immortal` 이라는 함수를 사용할 경우 반드시 커서를 종료시켜줘야 합니다. 그렇지 않으면 데이터베이스에 계속 남아 자원을 점유할 것입니다.

## Database Commands

데이터베이스 명령이라 불리는 특별한 유형의 쿼리가 있습니다. 이 명령은 서버의 종료와 데이터베이스 복제와 같은 관리자 업무를 수행합니다.

이 명령은 데이터 조작, 관리, 모니터링 같은 측면에서 유용하기 때문에 본문 전체에 걸쳐 언급되어있습니다. 예를 들어 컬렉션을 삭제할 때는 `drop` 데이터베이스 명령을 통해 수행합니다.

```js
> db.runCommand({"drop" : "test"})
{
    "nIndexesWas" : 1,
    "msg" : "indexes dropped for collection",
    "ns" : "test.test",
    "ok" : 1
}
```

아래 명령이 더 익숙할지도 모릅니다.

```js
> db.test.drop()
```

쉘은 새 데이터베이스 명령에 대해 재정의된 명령어를 가지고 있지 않을 수 있지만, 여전히 `runCommand()` 를 통해 이를 실행할 수 있습니다.

```js
> db.count.update({x : 1}, {$inc : {x : 1}}, false, true)
> db.runCommand({getLastError : 1})
{
    "err" : nil,
    "updatedExisting" : true,
    "n" : 5,
    "ok" : 1
}
```

MongoDB 에선 `db.listCommands()` 명령을 통해 모든 명령을 확인할 수 있습니다.

### How Commands Work

데이터베이스 명령은 항상 `ok` 값을 포함하는 문서를 반환합니다. 만약 값이 1 이면 성공한것이며, 0 이면 실패한것입니다.

만약 `ok` 가 0 이면 `errmsg` 라는 추가 Key 가 제공됩니다. `errmsg` 의 값은 명령이 실패한 이유를 설명한 문자열입니다. 예제를 통해 알아보겠습니다.

```js
> db.runCommand({"drop" : "test"})
{"errmsg" : "ns not found" , "ok" : 0}
```

일부 명령은 **관리자(admin)** 데이터베이스에서 실행되어야 합니다. 명령이 다른 데이터베이스에서 실행되는 경우 `access denied` 오류가 반환됩니다. 다른 데이터베이스에서 작업하고 `admin` 명령을 실행해야 하는경우 `runCommand` 대신 `adminCommand` 를 사용합니다.

```js
> use temp
switched to db temp
> db.runCommand({shutdown:1})
{ "errmsg" : "access denied; use admin db", "ok" : 0}
> db.adminCommand({"shutdown" : 1})
```



