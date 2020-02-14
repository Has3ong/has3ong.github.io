---
title : MongoDB Creating, Updating, and Deleting Documents
tags :
- Insert
- Delete
- Update
- Create
- MongoDB
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Inserting and Saving Documents

삽입은 MongoDB 에 데이터를 추가하는 기본적인 방법입니다. 컬렉션에 문서를 삽입하려면 컬렉션의 `insert` 메서드를 사용합니다.

```shell
> db.foo.insert({"bar" : "baz"})
```

이렇게 하면 문서에 `_id` 키를 추가하고 MongoDB 에 저장합니다.

### Bulk Insert

컬렉션에 여러 문서를 삽입하는 경우 **일괄 삽입(batch insert)** 이 더 빠릅니다.

```shell
> db.foo.insert([{"_id" : 0}, {"_id" : 1}, {"_id" : 2}])
> db.foo.find()
{ "_id" : 0 }
{ "_id" : 1 }
{ "_id" : 2 }
```

일괄 삽입은 여러 문서를 단일 컬렉션에 삽입할 때만 유용합니다. 단일 요청으로 여러 컬렉션에 삽입할 때는 일괄 삽입을 사용할 수 없습니다.

포스트 기준 MongoDB 버전은 48 MB 보다 큰 메세지를 허용하지 않기 때문에 48 MB 보다 큰 삽입을 시도하면 대다수의 드라이버는 삽입된 데이터를 여러 48 MB 크기의 일괄 삽입으로 분할됩니다.

배치 삽입 중간에 배치 삽입이 실패하는 경우, 현재 문서까지는 최대한 삽입하지만 이후에 요청되는 문서는 삽입하지 않는다.

```shell
> db.foo.insert([{"_id" : 0}, {"_id" : 1}, {"_id" : 1}, {"_id" : 2}])
```

3 번째는 에러를 발생시킬것입니다.

에러를 무시하고 남은 배치 작업에 대해 일괄 삽입을 계속하길 원한다면 `continueOnError` 옵션을 사용하여 삽입 오류 뒤의 작업에 대해 계속 진행할 수 있습니다.

### Insert Validation

MongoDB 는 삽입된 데이터에 대해 최소한의 검사를 수행합니다. 즉, 문서의 기본 구조를 검사하여 만약 존재하지 않는다면 "_id" 필드를 추가합니다.

기본 구조 검사 항목 중 하나는 크기인데, 모든 문서는 16 MB 보다 작아야 합니다. 이는 상대적인 제한입니다. 이는 대개 나쁜 스키마 설계를 예방하고 일관된 성능을 보장합니다.

최소한의 검사는 유효하지 않는 데이터가 쉽게 입력될 수 있다는 것을 의미합니다. 그러므로 어플리케이션 서버와 같이 신뢰성 있는 소스를 데이터베이스에 연결할 수 있도록 해야합니다.

## Removing Documents

데이터베이스에 데이터를 지워보겠습니다.

```shell
> db.foo.remove()
```

위 명령은 `foo` 컬렉션에 있는 모든 문서를 삭제합니다. 실제로 컬렉션을 지우는것은 아니므로 기존에 생성된 컬렉션의 메타 정보는 그대로 남습니다.

`rmemove` 함수는 선택적으로 쿼리 문서를 매개변수로 사용할 수 있습니다. 이 경우 쿼리 조건에 일치하는 문서들만 삭제됩니다. 예를 들어 `mailing.list` 컬렉션에서 "opt-out" 이 true 인 모든 사람을 삭제하고 싶다고 가정하겠습니다.

```shell
> db.mailing.list.remove({"opt-out" : true})
```

일단 데이터가 지워지면 영원히 사라집니다. 삭제를 취소하거나 지워진 문서를 복구할 수 있는 방법은 없습니다.

### Remove Speed

컬렉션 전체를 완전히 제거하려면 컬렉션에 대해 `drop` 함수를 사용하는게 빠르다.

```python
for i in range(1000000):
 collection.insert({"foo": "bar", "baz": i, "z": 10 - i})
```

이제 삽입한 문서의 시간을 측정하면서 모두 지워보겠습니다.

```python
import time
from pymongo import Connection

db = Connection().foo
collection = db.bar

start = time.time()

collection.remove()
collection.find_one()

total = time.time() - start
print "%d seconds" % total
```

맥북에어에서는 *46.08 seconds* 가 출력되었습니다.

`remove` 와 `findOne` 함수를 `db.tester.drop()` 로 대체하면 제거 시간이 0.01 초로 줄어듭니다. 전체 컬렉션에 지워지면 메타데이터도 모두 삭제됩니다.

## Updating Documents

문서가 데이터베이스에 저장되면 `update` 를 사용하여 변경할 수 있습니다. `update` 는 두 매개변수를 받는데, 이는 어떤 문서를 갱신할것인지를 찾는 **query document** 와 문서를 어떻게 변경할지 설명하는 **modifier document** 입니다.

갱신은 원자적으로 이루어집니다. 동시에 두 갱신 요청이 발생하면 먼저 서버에 도착한 요청이 적용된 후 다음 요청이 적용됩니다.

### Document Replacement

갱신의 가장 간단한 유형은 일치된 문서를 새로운 것으로 완전히 치환하는 것입니다. 이는 대대적인 스키마 변경에 유용합니다. 예를 들어 사용자 문서에 아래와 같은 큰 규모의 변경을 수행한다고 가정하겠습니다.

```json
{
  "_id" : ObjectId("4b2b9f67a1f631733d917a7a"),
  "name" : "joe",
  "friends" : 32,
  "enemies" : 2
}
```

위 문서를 아래와 같이 변경시킬것입니다.

```json
{
  "_id" : ObjectId("4b2b9f67a1f631733d917a7a"),
  "username" : "joe",
  "relationships" :
  {
    "friends" : 32,
    "enemies" : 2
  }
}
```

그러면 다음과 같은 명령어를 수행하면 됩니다.

```shell
> var joe = db.users.findOne({"name" : "joe"});
> joe.relationships = {"friends" : joe.friends, "enemies" : joe.enemies};
{
  "friends" : 32,
  "enemies" : 2
}

> joe.username = joe.name;
"joe"
> delete joe.friends;
true
> delete joe.enemies;
true
> delete joe.name;
true
> db.users.update({"name" : "joe"}, joe);
```

`findOne` 함수를 실행하면 갱신된 문서의 구조를 확인할 수 있습니다.

흔한 실수 중 하나는 조건절로 하나 이상의 문서가 일체되게 한 후, 두 번째 매개변수로 중복된 `_id` 값을 가진 문서를 생성하는 것이다. 이 경우 데이터베이스는 오류를 반환하고 아무것도 변경하지 않습니다.

예를들어 동일한 `name` 값을 가진 여러 문서를 만들었다고 가정하겠습니다.

```shell
> db.people.find()
{"_id" : ObjectId("4b2b9f67a1f631733d917a7b"), "name" : "joe", "age" : 65},
{"_id" : ObjectId("4b2b9f67a1f631733d917a7c"), "name" : "joe", "age" : 20},
{"_id" : ObjectId("4b2b9f67a1f631733d917a7d"), "name" : "joe", "age" : 49},
```

이제 두 번째 `Joe` 의 생일이 되엇고 우리는 그의 `age` 값을 높이려 한다면 다음과같이 할 수 있습니다.

```js
> joe = db.people.findOne({"name" : "joe", "age" : 20});
{
 "_id" : ObjectId("4b2b9f67a1f631733d917a7c"),
 "name" : "joe",
 "age" : 20
}
> joe.age++;
> db.people.update({"name" : "joe"}, joe);
E11001 duplicate key on update
```

갱신을 요청하면 데이터베이스는 `{"name" : "age"}` 와 일치하는 문서를 찾습니다. 처음 65 세의 `Joe` 를 찾습니다. 이미 치환하려는 문서와 같은 `_id` 를 가진 문서가 컬렉션에 있어도 현재 `Joe` 의 변수 내 문서를 치환하려 시도합니다. 하지만 `_id` 의 값은 고유해야하기 때문에 갱신에 실패합니다.

그래서 다음과 같이 사용하는게 올바른 갱신 방법입니다.

```shell
> db.people.update({"_id" : ObjectId("4b2b9f67a1f631733d917a7c")}, joe)
```

### Using Modifiers

보통 문서의 특정 부분만 갱신하는 경우가 많습니다. 원자적 update modifier 를 사용하면 부분 갱신을 수행할 수 있습니다. 갱신 제한자는 키를 변경, 추가, 제거하고 배열과 내장 문서를 조작하는 복잡한 갱신 연산을 지정하는 데 사용되는 특수 키 입니다.

컬렉션에 웹사이트 분석 데이터를 저장하고 있고, 누군가 페이지를 방문하면 카운터를 증가시킨다고 가정하겠습니다. 갱신 제한자를 이용하면 카운터를 원자적으로 증가시킬 수 있습니다. 각 URL 과 페이지 뷰가 다음과 같이 저장되어 있다고 해보겠습니다.

```json
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "url" : "www.example.com",
  "pageviews" : 52
}
```

페이지를 방문할 때마다 URL 로 페이지를 찾고 `pageviews` 키의 값을 증가시키기 위해 `$inc` 제한자를 사용할 수 있습니다.

```shell
> db.analytics.update({"url" : "www.example.com"},
... {"$inc" : {"pageviews" : 1}})
```

확인해보면 `pageviews` 값이 증가한걸 확인할 수 있습니다.

```shell
> db.analytics.find()
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "url" : "www.example.com",
  "pageviews" : 53
}
```

제한자를 사용할 때는 `_id` 의 값은 변경시킬 수 없습니다.

**1. Getting started with the “$set” modifier**

`$set` 은 필드의 값을 설정합니다. 만약 필드가 존재하지 않으면 해당 필드를 생성합니다. 이 기능은 스키마를 갱신하거나 사용자 정의 키를 추가할 때 편리하게 쓸 수 있습니다.

예를 들어 간단한 사용자 정보가 아래와 같이 저장되어 있다고 가정하겠습니다.

```shell
> db.users.findOne()
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "name" : "joe",
  "age" : 30,
  "sex" : "male",
  "location" : "Wisconsin"
}
```

사용자가 프로필에 좋아하는 책을 추가하고 싶으면 `$set` 을 사용합니다.

```shell
> db.users.update({"_id" : ObjectId("4b253b067525f35f94b60a31")},
... {"$set" : {"favorite book" : "war and peace"}})
```

문서는 `favorite book` 을 가지게 됩니다.

```shell
> db.users.findOne()
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "name" : "joe",
  "age" : 30,
  "sex" : "male",
  "location" : "Wisconsin",
  "favorite book" : "war and peace"
}
```

`$set` 을 통해 값을 변경할 수 있습니다.

```shell
> db.users.update({"name" : "joe"},
... {"$set" : {"favorite book" : "green eggs and ham"}})
```

`$set` 은 데이터형도 변경할 수 잇습니다.

```shell
> db.users.update({"name" : "joe"},
... {"$set" : {"favorite book" :
... ["cat's cradle", "foundation trilogy", "ender's game"]}})
```

`$unset` 을 이용하여 Key / Value 모두 삭제할 수 있습니다.

```shell
> db.users.update({"name" : "joe"},
... {"$unset" : {"favorite book" : 1}})
```

`$set` 은 내장 문서 내부의 데이터를 변경할 때도 사용할 수 있습니다.

```shell
> db.blog.posts.findOne()
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "title" : "A Blog Post",
  "content" : "...",
  "author" : {
  "name" : "joe",
  "email" : "joe@example.com"
  }
}
> db.blog.posts.update({"author.name" : "joe"}, {"$set" : {"author.name" : "joe schmoe"}})
> db.blog.posts.findOne()
{
  "_id" : ObjectId("4b253b067525f35f94b60a31"),
  "title" : "A Blog Post",
  "content" : "...",
  "author" : {
  "name" : "joe schmoe",
  "email" : "joe@example.com"
  }
}
```

Key 를 추가, 변경 삭제할 때는 항상 $ 연산자를 사용해야 합니다. 일반적으로 범하는 오류는 다음과 같이 업데이트를 수행하여 `foo` 와 `bar` 로 바꾸는 경우입니다.

```shell
> db.coll.update(criteria, {"foo" : "bar"})
```

위 명령은 조건에 맞는 모든 문서를 `{"foo" : "bar"}` 로 완전히 대체 합니다. 개별 Key / Value 수정할때는 $ 연산자를 사용해야 합니다.

**2. Incrementing and decrementing**

`$inc` 제한자는 이미 존재하는 Key 의 값을 변경하거나 새롭게 생성하는데 사용합니다. 또한 자주 변하는 수치값을 갱신하는데 유용합니다.

아래와 같은 문서가 있다고 보겠습니다.

```shell
> db.games.insert({"game" : "pinball" , "user" : "joe"})
```

핀볼은 공이 범퍼에 부딪히면 점수가 증가합니다. 점수의 기본을 50 이라고 하고 플레이어의 점수에 50 을 더하는 데 `$inc` 를 사용해보겠습니다.

```shell
> db.games.update({"game" : "pinball" , "user" : "joe},
... {"$inc" : {"score" : 50}})
```

다음과 같이 갱신이 됩니다.

```shell
> db.games.findOne()
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "game" : "pinball",
  "name" : "joe",
  "score" : 50
}
```

`score` Key 는 존재하지 않지만 `$inc` 에 의해 생성되고 50 만큼 증가했습니다.

10,000 점을 추가하고 싶다고 해보겠습니다.

```shell
> db.games.update({"game" : "pinball", "user" : "joe"},
... {"$inc" : {"score" : 10000}})
```

결과를 확인해 보겠습니다.

```shell
> db.games.find()
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "game" : "pinball",
  "name" : "joe",
  "score" : 10050
}
```

`$inc` 는 `$set` 과 다르게 숫자를 증감하기 위해 설계되었습니다. 또한, **integer**, **long**, **double** 형에만 사용할 수 있습니다.

```shell
> db.foo.insert({"count" : "1"})
> db.foo.update({}, {$inc : {count : 1}})
Cannot apply $inc modifier to non-number
```

또한 `$inc` 의 값은 무조건 숫자여야 합니다.

**3. Array modifiers**

제한자의 확장 클래스는 배열을 다루는 데 쓰입니다. 배열은 공통적이고 강력한 데이터 구조체입니다. 제한자는 리스트에 대한 인덱스를 지정할 수 있을 뿐만 아니라 `set` 처럼 이중으로 사용할 수 있습니다.

**4. Adding elements**

`$push` 는 지정된 키가 이미 존재하면 배열의 끝에 요소를 추가하고, 그렇지 않으면 새로운 배열을 생성해서 추가합니다. 예를 들어 블로그 포스트를 저장하고 배열 형태의 `comments` 키를 삽입한다고 가정하겠습니다. 존재하지 않는 `comments` 배열을 생성하고, 댓글을 넣을 수 있습니다.

```shell
> db.blog.posts.findOne()
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "title" : "A blog post",
  "content" : "..."
}

> db.blog.posts.update({"title" : "A blog post"},
... {$push : {"comments" :
... {"name" : "joe", "email" : "joe@example.com",
... "content" : "nice post."}}})

> db.blog.posts.findOne()
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "title" : "A blog post",
  "content" : "...",
  "comments" : [
    {
      "name" : "joe",
      "email" : "joe@example.com",
      "content" : "nice post."
    }
  ]
}
```

또 다른 댓글을 추가하고 싶으면 `$push` 를 다시 사용하면 됩니다.

```shell
> db.blog.posts.update({"title" : "A blog post"},
... {$push : {"comments" :
... {"name" : "bob", "email" : "bob@example.com",
... "content" : "good post."}}})
> db.blog.posts.findOne()
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

단순한 추가의 형태지만 더 복잡한 배열 기능으로 사용할 수 있습니다. `$each` 를 사용하면 여러 개의 값을 한 번에 추가할 수 있습니다.

```shell
> db.stock.ticker.update({"_id" : "GOOG"},
... {"$push" : {"hourly" : {"$each" : [562.776, 562.790, 559.123]}}})
```

이는 배열에 3 개의 새로운 요소를 추가합니다.

배열을 특정 길이로 늘이고 싶은 경우, 특정 크기 이상으로 늘어나는 것을 막고 효과적으로 **top N** 목록을 만들기 위해 `$push` 와 결합하여 `$slice` 를 사용할 수 있습니다.

```shell
> db.movies.find({"genre" : "horror"},
... {"$push" : {"top10" : {
...   "$each" : ["Nightmare on Elm Street" , "Saw"],
...   "$slice" : -10}}})
```

위 예제에서는 배열에 추가할 수 있는 요소의 수를 10 개로 제한했습니다. 슬라이스는 항상 음수여야 합니다. 만약 요소의 개수가 10 보다 크면 마지막 10개의 요소만 유지가 됩니다.

마지막으로 배열에 하위객체를 추가하는 동안에는 정돈하기 전에 `$sort` 를 수행할 수 있습니다.

```shell
> db.movies.find({"genre" : "horror"},
... {"$push" : {"top10" : {
...   "$each" : [{"name" : "Nightmare on Elm Street", "rating" : 6.6},
...              {"name" : "Saw", "rating" : 4.3}],
...   "$slice" : -10,
...   "$sort" : {"rating" : -1}}}})
```

위 명령은 `rating` 필드로 배열의 모든 요소를 정렬한 후 첫 열 개의 요소를 유지합니다. `$each` 를 반드시 포함해야 합니다. `$slice` 나 `$sort` 를 배열상에서 `$push` 와 함께 쓰려면 반드시 `$each` 도 사용해야합니다.

**5. Using arrays as sets**

배욜에 같은 값이 존재하지 않는 경우에만 해당 값을 추가하면서 배열을 하나의 집합으로 처리하길 원할것입니다. 이는 쿼리 문서에 `$ne` 를 사용하여 수행할 수 있습니다. 예를 들어 인용목록에 저자가 존재하지 않을 때만 해당 저자를 추가해야 하는 경우 다음과 같이 합니다.

```shell
> db.papers.update({"authors cited" : {"$ne" : "Richie"}},
... {$push : {"authors cited" : "Richie}})
```

이는 `$addToSet` 을 통해서 가능합니다. `$addToSet` 은 `$ne` 가 작동하지 않는 경우나 `$addToSet` 이 무슨 일이 일어났는지 더 잘 설명하는 경우에 유용합니다.

예를 들어 사용자를 표현하는 문서가 있다고 가정하겠습니다. 이 경우 사용자가 입력한 이메일 주소 집합이 있을것입니다.

```shell
> db.users.findOne({"_id" : ObjectId("4b2d75476cc613d5ee930164")})
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "username" : "joe",
  "emails" : [
    "joe@example.com",
    "joe@gmail.com",
    "joe@yahoo.com"
  ]
}
```

다른 주소를 추가할 때, 중복을 막기 위해 `$addToSet` 을 사용할 수 있습니다.

```shell
> db.users.update({"_id" : ObjectId("4b2d75476cc613d5ee930164")},
... {"$addToSet" : {"emails" : "joe@gmail.com"}})
> db.users.findOne({"_id" : ObjectId("4b2d75476cc613d5ee930164")})
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "username" : "joe",
  "emails" : [
    "joe@example.com",
    "joe@gmail.com",
    "joe@yahoo.com",
  ]
}
> db.users.update({"_id" : ObjectId("4b2d75476cc613d5ee930164")},
... {"$addToSet" : {"emails" : "joe@hotmail.com"}})
> db.users.findOne({"_id" : ObjectId("4b2d75476cc613d5ee930164")})
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "username" : "joe",
  "emails" : [
    "joe@example.com",
    "joe@gmail.com",
    "joe@yahoo.com",
    "joe@hotmail.com"
  ]
}
```

여러 개의 고유한 값을 추가하기 위해 `$addToSet` 과 `$each` 를 결합하여 사용할 수 있는데 이는 $ne / $push 조합으로는 할 수 없는 작업입니다. 예를 들어 사용자가 하나 이상의 이메일 주소를 추가하고 싶을 때는 다음과 같이 제한자를 사용할 수 있습니다.

```shell
> db.users.update({"_id" : ObjectId("4b2d75476cc613d5ee930164")}, {"$addToSet" :
... {"emails" : {"$each" : ["joe@php.net", "joe@example.com", "joe@python.org"]}}})
> db.users.findOne({"_id" : ObjectId("4b2d75476cc613d5ee930164")})
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "username" : "joe",
  "emails" : [
    "joe@example.com",
    "joe@gmail.com",
    "joe@yahoo.com",
    "joe@hotmail.com"
    "joe@php.net"
    "joe@python.org"
  ]
}
```

**6. Removing elements**

배열에서 요소를 제거하는 몇 가지 방법이 있습니다. 만약 배열을 큐나 스택처럼 사용하고 싶으면 배열의 양쪽 끝에서 요소를 제거하는 `$pop` 을 사용합니다. `{"$pop" : {"key" : 1}}` 은 배열의 끝에서 부터 요소를 제거합니다. `{"$pop" : {"key" : -1}}` 은 배열의 처음부터 요소를 제거합니다.

때때로 요소가 배열의 위치가 아닌 지정된 조건에 의해 제거되어야 하는 경우가 있습니다. `$pull` 은 주어진 조건과 일치하는 배열의 요소를 제거하는 데 사용합니다. 예를 들어 특별한 순서가 없는 해야 할 일의 목록이 있다고 가정합니다.

```shell
> db.lists.insert({"todo" : ["dishes", "laundry", "dry cleaning"]})
```

세탁을 먼저 했다면 다음과 같이 목록에서 제거할 수 있습니다.

```shell
> db.lists.update({}, {"$pull" : {"todo" : "laundry"}})
```

이제 `find` 를 수행해 보면 배열에 2개 요소만 남은 것을 확인할 수 있습니다.

```shell
> db.lists.find()
{
  "_id" : ObjectId("4b2d75476cc613d5ee930164"),
  "todo" : [
    "dishes",
    "dry cleaning"
  ]
}
```

`$pull` 을 사용하면 일치하는 모든 문서를 지웁니다. 만일 `[1, 1, 2, 1]` 과 같은 배열이 있고 1을 뽑아내면 배열에는 `[2]` 하나만 남게 될 것입니다.

배열 연산자는 배열을 값으로 가진 키에만 사용할 수 있습니다. 예를 들어 정수형에 데이터를 넣거나 문자열형에서 데이터를 빼내는 작업은 할 수 없습니다. 스칼라 값을 변경하기 위해서는 `$set` 이나 `$inc` 를 사용합니다.

**7. Positional array modifications**

배열에 여러 값이 존재하고 그 중 일부를 변경하는 조작은 어렵습니다. 배열 내 여러 값을 다루기 위한 2 가지 방법은 있는데, 위치를 이용하거나 위치 연산자를 사용하는것입니다.

배열의 인덱스는 0 이 기준이며, 배열 요소는 인덱스 번호를 문서의 키처럼 사용할 수 있습니다. 예를 들어 댓글이 포함된 블로그 포스트와 같이 몇몇 내장 문서의 배열을 포함하는 문서가 있다고 가정하겠습니다.

```shell
> db.blog.posts.findOne()
{
  "_id" : ObjectId("4b329a216cc613d5ee930192"),
  "content" : "...",
  "comments" : [
    {
      "comment" : "good post",
      "author" : "John",
      "votes" : 0
    },
    {
      "comment" : "i thought it was too short",
      "author" : "Claire",
      "votes" : 3
    },
    {
      "comment" : "free watches",
      "author" : "Alice",
      "votes" : -1
    }
  ]
} 
```

첫번째 댓글의 투표수를 증가하고 싶을 때는 다음과 같이 쓸 수 있습니다.

```shell
> db.blog.update({"post" : post_id},
... {"$inc" : {"comments.0.votes" : 1}})
```

하지만 데이터가 많아지면 어느 배열 요소를 변경해야 할지 모릅니다. MongoDB 에서는 이문제를 해결하기 위해 쿼리 문서와 일치하는 배열 요소와 해당 요소의 위치를 알아내서 갱신하는 위치연산자 $ 를 제공합니다. 예를 들어 Jim 이라고 이름을 갱신해야 하는 John 이라는 사용자가 있을 때, 위치 연산자를 사용해서 댓글 내 해당 항목을 갱신할 수 있습니다.

```shell
db.blog.update({"comments.author" : "John"},
... {"$set" : {"comments.$.author" : "Jim"}})
```

위치 연산자는 오직 첫 번째로 일치하는 요소만 갱신합니다. 그러므로 John 이 하나 이상의 댓글을 남겼다면, 처음 남긴 댓글의 이름만 변경됩니다.

**8. Modifier speed**

몇몇 제한자는 다른것보다 빠릅니다. `$inc` 는 제자리에서 문서를 수정합니다. 이 경우 문서의 크기를 변경할 필요가 없기 때문에 매우 효율적입니다. 반면에, 배열 제한자는 문서의 크기를 변경하기 때문에 매우 느릴 수 있습니다.

MongoDB 몽고디비에 데이터를 삽입하면 각각의 데이터는 디스크 상의 기존에 존재하던 곳 바로 옆에 놓입니다. 그러므로 만약 문서가 커지면, 처음에 써졌을 때의 공간에는 더 이상 맞지 않꼬 결국에는 컬렉션의 또 다른 공간으로 옮겨지게 됩니다.

몇몇 문서와 함께 새로운 컬렉션을 생성한 후 서로 다른 큰 두 개의 문서 사이에 새로운 문서를 생성함으로써 이를 확인해 볼 수 있습니다. 이는 결국 문서의 끝에서 충돌을 일으키게 됩니다.

```shell
> db.coll.insert({"x" : "a"})
> db.coll.insert({"x" : "b"})
> db.coll.insert({"x" : "c"})
> db.coll.find()
{"_id" : ObjectId("507c3581d87d6a342e1c81d3"), "x" : "a" }
{"_id" : ObjectId("507c3581d87d6a342e1c81d4"), "x" : "b" }
{"_id" : ObjectId("507c3581d87d6a342e1c81d5"), "x" : "c" }
> db.coll.update({"x" : "b"}, {$set : {"x" : "bbb"}})
{"_id" : ObjectId("507c3581d87d6a342e1c81d3"), "x" : "a" }
{"_id" : ObjectId("507c3581d87d6a342e1c81d5"), "x" : "c" }
{"_id" : ObjectId("507c3581d87d6a342e1c81d4"), "x" : "bbb" }
```

MongoDB 가 문서를 이동시킬 때 MongoDB 가 새로운 문서에 대해 크기를 변경할 수 있도록 남겨둔 여분의 공간인 컬렉션의 패딩 요소에서 충돌이 일어납니다. 패딩 요소는 `db.coll.stats()` 를 실행하여 확인할 수 있습니다.

위와 같이 갱신하기 전에 `paddingFactor` 필드는 1이 될것이며,  `Example 1` 에 나타난 것처럼 새 문서에 대한 크기를 할당합니다. 만약 문서들 중 하나를 크게 만들고 다시 실행해보면 `Example 2` 처럼 1.5 배 정도 커진것을 알 수 있습니다. 각각 새 문서는 기존 크기의 절반에 해당하는 확장 여유 공간을 받을것입니다. 이후의 갱신이 더 많은 이동을 일으킬 경우 패딩 요소는 계속 증가하며, 더 이상 이동이 없다면 `Example 3` 처럼 점차 줄어들것입니다.

> Example 1

```
| "x" : "a" | "x" : "b" | "x" : "c" |
```

> Example 2

```
| "x" : "a" |         | "x" : "c" | "x" : "bbb" |
```

> Example 3

```
| "x" : "a" |         | "x" : "c" | "x" : "bbb" | "x" : "d" |     | "x" : "e" |  | "x" : "f" | |
```

문서의 이동은 느립니다. MongoDB 는 문서가 있던 공간을 빈 상태로 만들고 다른 곳에서 문서에 대한 쓰기 작업을 해야 합니다. 따라서 가능한 한 패딩 요소를 1에 가깝게 유지해야 합니다. 컬렉션을 조각 모음하지 않는 한 수동적으로 패딩 요소를 설정할 수 없지만 임의의 큰 증가에 의존하지 않는 스키마를 설계할 수는 있습니다.

다음 Python 코드로 이동하지 않고 제자리 갱신하는것과 이동하는 갱신사이의 속도차이를 알아보겠습니다.

```python
from pymongo import Connection
import time

db = Connection().performance_test
db.drop_collection("updates")
collection = db.updates

collection.insert({"x": 1})

# make sure the insert is complete before we start timing
collection.find_one()

start = time.time()

for i in range(100000):
  collection.update({}, {"$inc" : {"x" : 1}})
  
# make sure the updates are complete before we stop timing
collection.find_one()

print time.time() - start
```

맥북에어에서 위 코드는 7.33 초가 걸렸습니다.

```python
for i in range(100000):
  collection.update({}, {'$push' : {'x' : 1}})
```

위 코드는 67.58 초가 걸렸습니다.

`$push` 와 다른 배열 제한자의 사용은 권장하며 자주 필요하지만, 이런 갱신에 따른 상충이 따라옵니다. 만약 `$push` 가 병목상태가 되면 내장된 배열을 별도의 컬렉션으로 꺼내거나 수동적인 패딩을 사용해야 합니다.

MongoDB 는 빈 공간을 다시 사용하는데 용이하지 않습니다. 따라서 많은 문서를 이동시키면 빈 데이터 파일에 큰 빈공간이 야기됩니다. 만약 큰 빈 공간이 생기면 로그에서 다음과 같은 메세지가 표시됩니다.

```shell
Wed Feb 12 22:16:05 [conn17427] info DFM::findAll(): extend a:7f18dc00 was empty, skipping, ahead
```

이는 쿼리가 수행되는 동안 MongoDB 어떤 문서도 발견하지 못해 전체 익스텐트를 탐색했다는것을 의미합니다. 즉, 단편화가 존재하고 조각 모음을 수행하기를 원한다는 것입니다.

만약 스키마의 많은 디오을 요구하거나 삽입 및 삭제를 통해 많은 뒤섞임이 발생했다면 `usePowerOf2Sizes` 옵션을 사용하여 디스크 재사용을 향상시킬 수 있습니다.

```shell
> db.runCommand({"collMod" : collectioName, "usePowerOf2Sizes" : true})
```

### Upserts

**갱신 입력(Upsert)** 는 갱신의 특수한 형태입니다. 만약 갱신 조건과 일치하는 어떤 문서도 존재하지 않으면 쿼리 문서와 갱신 문서를 합쳐서 새로운 문서를 생성합니다. 만약 일치하는 문서가 발견되면 일반적인 갱신을 수행합니다. 갱신 입력은 컬렉션 내에 동일한 문서를 생성하고 갱신하므로 결과적으로 시드 문서가 필요 없어 편리합니다.

웹사이트의 경우 각 페이지 뷰를 기록하는 예제로 돌아가 보겠습니다. 갱신 입력을 하지 않는다면 URL 을 찾아 페이지 뷰 값을 증가시키거나, 해당 URL 이 없으면 새로운 문서를 하나 만들어야 할것입니다. 자바스크립트 코드로 보면 아래와 같습니다.

```js
// check if we have an entry for this page
blog = db.analytics.findOne({url : "/blog"})
// if we do, add one to the number of views and save
if (blog) {
  blog.pageviews++;
  db.analytics.save(blog);
}
// otherwise, create a new document for this page
else {
  db.analytics.save({url : "/blog", pageviews : 1})
}
```

이는 매번 누군가 페이지를 방문할 때마다 페이지를 확인하기 위해 데이터베이스를 와복하고 갱신이나 삽입을 또 보내야 한다는 의미입니다. 만약 이를 다중 프로세스 상에서 실행하면 주어진 URL 에 하나 이상의 문서가 동시에 삽입할 수 있는 경쟁 상태를 만들 수 있습니다.

갱신입력을 사용하여 코드를 줄이고 경쟁 상태를 제거할 수 있습니다.

```js
db.analytics.update({"url" : "/blog"}, {"$inc" : {"visits" : 1}}, true)
```

위 한 줄로 이전 코드 구문과 동일하게 처리를 할 수 있습니다.

예를 들어 갱신 입력에서 처리하는 키와 일치하는 문서를 찾아서 키 값을 증가한다면, 값의 증가는 일치하는 문서에 적용될 것입니다.

```shell
> db.users.update({"rep" : 25}, {"$inc" : {"rep" : 3}}, true)
> db.users.findOne()
{
  "_id" : ObjectId("4b3295f26cc613d5ee93018f"),
  "rep" : 28
```

갱신 입력은 `rep` 가 25 인 새로운 문서를 만들어 3을 증가시킨후 28인 문서를 반환합니다. 만약 갱신 입력 옵션이 명시되어 있지 않다면 {"rep" : 25} 는 어떤 문서와도 일치하지 않을것이며, 어떤 일도 발생하지 않습니다.

만약 갱신 입력을 다시 수행하면 새로운 문서를 생성할 것입니다. 이는 기준이 컬렉션의 전용 문서와 일치하지 않기 때문입니다.

때때로 필드에 문서가 생성될 때 시드값이 설정되야 하지만 이후의 갱신에서는 변경되지 않습니다. `$setOnInsert` 는 이를 위한 것입니다. 문서가 삽입될 때 오로지 필드의 값을 설정하는 제한자 입니다. 다음과 같이 사용할 수 있습니다.

```shell
> db.users.update({}, {"$setOnInsert" : {"createdAt" : new Date()}}, true)
> db.users.findOne()
{
  "_id" : ObjectId("512b8aefae74c6779e404ca"),
  "createdAt" : ISODate("2020-02-12T22:40:36.742Z")
}
```

이 문서를 다시 갱신한다면 기존 문서와 일치하는 것을 찾을 것이고 어떤 것도 입력되지 않을 것이며 `createAt` 필드는 변경되지 않을 것입니다.

```shell
> db.users.update({}, {"$setOnInsert" : {"createdAt" : new Date()}}, true)
> db.users.findOne()
{
  "_id" : ObjectId("512b8aefae74c6779e404ca"),
  "createdAt" : ISODate("2020-02-12T22:40:36.742Z")
}
```

ObjectId 가 문서가 작성될 때 타임스탬프를 포함하고 있기 때문에 일반적으로 `createAt` 필드를 유지할 필요가 없습니다. 하지만 `$setOnInsert` 는 패딩을 생성하고, 계수기를 초기화하고, ObjectId 를 사용하지 않는 컬렉션에 유용합니다. 

**1. The save shell helper**

`save` 는 문서가 존재하지 않을 경우 문서를 삽입하거나, 존재할 경우 문서를 갱신할 수 있게하는 쉘 함수 입니다. 이 함수는 문서를 넘겨받는 하나의 매개변수를 가집니다. 만약 문서가 `_id` 키를 포함하면 `save` 는 갱신 입력을 실행합니다. 그렇지 않으면 삽입을 실행합니다. `save` 는 프로그래머가 쉘에서 빠르게 문서를 수정할 수 있게 하는 함수입니다.

```shell
> var x = db.foo.findOne()
> x.num = 42
42
> db.foo.save(x)
```

`save` 가 없다면 마지막 줄은 더 복잡한 `db.foo.update({"_id" : x._id, x)` 가 되어야 합니다.

### Updating Multiple Documents

기본적으로 `update` 는 조건과 일치하는 첫 번째 문서만 갱신합니다. 조건과 일치하는 모든 문서를 갱신하기 위해서는 `update` 의 4 번째 매개변수를 true 로 설정합니다.

**다중갱신(Multiple Update)** 은 스키마를 이전하거나 특정 사용자에게 새로운 기능을 제공할 때 쓰기 좋은 방법입니다. 예를 들어 특정 날짜에 생일을 맞이하는 모든 사용자에게 선물을 준다고 가정하겠습니다. 그들 계정에 `gift` 를 추가하기 위해 다중 갱신을 사용할 수 있습니다.

```shell
> db.users.update({"birthday" : "10/13/1978"},
... {"%set" : {"gift" : "Happy Birthday!"}}, false, true}
```

위 명령은 생일이 10/13/1978 인 모든 사용자의 문서에 `gift` 필드를 추가합니다.

다중갱신을 통해 갱신한 문서의 수를 보려면 `getLastError` 의 데이터베이스 명령어를 사용합니다. `n` 키는 갱신한 문서의 수를 포함합니다.

```shell
> db.count.update({x : 1}, {$inc : {x : 1}}, false, true)
> db.runCommand({getLastError : 1})
{
  "err" : null,
  "updatedExisting" : true,
  "n" : 5,
  "ok" : true
}
```

### Returning Updated Documents

`getLastError` 를 호출해서 무엇을 갱신했는지에 대해 다소 제한된 정보를 얻을 수 있지만 실제로 갱신한 문서를 반환하지 않습니다. 이를 위해 `findAndModify` 명령어가 필요합니다. 큐를 다루거나 읽은 후 쓰기 형태의 원자적 연산이 필요한 경우에 편리합니다.

특정 순서로 실행하는 프로세스의 컬렉션이 있다고 가정하겠습니다.

```json
{
  "_id" : ObjectId(),
  "status" : state,
  "priority" : N
}
```
 
`status` 문자열로 `READY`, `RUNNING` 또는 `DONE` 이 될 수 있습니다. 우선순위가 가장 높은 `READY` 상태의 작업을 찾아 프로세스를 실행하고 마지막으로 `status` 를 `DONE` 으로 갱신해야 합니다. 우선순위 기준으로 `READY` 프로세스를 찾아 가장 높은 우선순위의 프로세스 상태를 `RUNNING` 으로 갱신합니다. 프로세스가 끝나면 `status` 를 `DONE` 으로 갱신합니다. 이 과정은 아래와 같습니다.

```js
var cursor = db.processes.find({"status" : "READY"});
ps = db.processes.find({"status" : "READY").sort({"priority" : -1}).limit(1).next()
db.processes.update({"_id" : ps._id}, {"$set" : {"status" : "RUNNING"}})
do_something(ps);
db.processes.update({"_id" : ps._id}, {"$set" : {"status" : "DONE"}})
```

위 알고리즘은 **경쟁 상태(race condition)** 를 만들기 때문에 좋지 않습니다. 경쟁 상태는 갱신 쿼리의 일부로 상태를 확인하여 피할 수 있지만 복잡합니다.

```js
var cursor = db.processes.find({"status" : "READY"}).sort({"priority" : -1}).limit(1);
while ((ps = cursor.next()) != null) {
  ps.update(
    {"_id" : ps._id, "status" : "READY"},
    {"$set" : {"status" : "RUNNING"}}
  );
  
  var lastOp = db.runCommand({getlasterror : 1});
  if (lastOp.n == 1) {
    do_something(ps);
    db.processes.update({"_id" : ps._id}, {"$set" : {"status" : "DONE"}})
    break;
  }
  cursor = db.processes.find({"status" : "READY"}).sort({"priority" : -1}).limit(1);
}
```

또한 타이밍에 따라 한 스레드가 모든 일을 하고 다른 스레드는 쓸데없이 다른 스레드의 꽁무니만 쫓고 있을 수도 있습니다. 스레드 A 가 프로세스를 항상 먼저 얻고, B 가 동일한 프로세스를 얻으려 했다가 실패하고, A 가 모든 일을 처리하도록 놔두게 됩니다.

이런 상황에는 `findAndModify` 가 가장 적합합니다. `findAndModify` 는 한 번의 연산으로 항목을 반환하고 갱신할 수 있습니다.

```shell
> ps = db.runCommand({"findAndModify" : "processes",
... "query" : {"status" : "READY"},
... "sort" : {"priority" : -1},
... "update" : {"$set" : {"status" : "RUNNING"}})
{
  "ok" : 1,
  "value" : {
    "_id" : ObjectId("4b3e7a18005cab32be6291f7"),
    "priority" : 1,
    "status" : "READY"
  }
}
```

이전 수정 상태에서 문서를 반환하는 `findAndModify` 의 기본값으로 반환된 문서의 상태는 여전히 `READY` 입니다. 만약 컬렉션에서 `find` 해보면 문서의 `status` 가 `RUNNING` 으로 변경된 것을 알 수 있습니다.

```shell
> db.processes.findOne({"_id" : ps.value._id})
{
  "_id" : ObjectId("4b3e7a18005cab32be6291f7"),
  "priority" : 1,
  "status" : "RUNNING"
}
```

프로그램은 다음과 같이 됩니다.

```js
> ps = db.runCommand({"findAndModify" : "processes",
... "query" : {"status" : "READY"},
... "sort" : {"priority" : -1},
... "update" : {"$set" : {"status" : "RUNNING"}}).value
> do_something(ps)
> db.process.update({"_id" : ps._id}, {"$set" : {"status" : "DONE"}})
```

`findAndModify` 는 `update` 또는 `remove` 키를 가질 수 있습니다. `remove` 키는 일치하는 문서가 컬렉션에서 삭제되어야 한다는 것을 가리킵니다. 예를 들어 상태를 갱신하는 대신에 작업을 삭제하고 싶으면 다음과 같이합니다.

```js
> ps = db.runCommand({"findAndModify" : "processes",
... "query" : {"status" : "READY"},
... "sort" : {"priority" : -1},
... "remove" : true).value
> do_something(ps)
```

`findAndModify` 명령어는 다음과 같은 필드를 가집니다.

* findAndModify
  * 컬렉션 이름 문자열
* query
  * 문서를 찾는 조건을 설정하는 쿼리 문서
* sort
  * 결과를 정렬하기 위한 조건
* update
  * 찾은 문서를 갱신하는 제한자 문서
* remove
  * 찾은 문서의 삭제 여부를 결정하는 불리언 값
* new
  * 반환하는 문서가 갱신한 문서인지 갱신하기 전의 문서인지 지정하는 불리언 값
* fields
  * 반환하기 위한 문서의 필드
* upsert
  * 부분 갱신되어야 하는지 말아야 하는지 명시한 불리언 값

`update` 나 `remove` 중 하나는 반드시 포함해야 하지만 둘 다 포함하면 안됩니다.

## Setting a Write Concern

**쓰기 결과 확인 정책(Write Concern)** 은 프로그램을 계속하기 전에 쓰기가 얼마나 안전하게 저장되었는지 설명하는 데 사용되는 클라이언트 설정입니다. 기본적으로 삽입, 삭제, 갱신은 해당 작업을 계속 진행하기 전에 쓰기가 성공했는지 아닌지 여부에 대해 데이터베이스의 응답을 기다립니다. 기본적인 2 가지 쓰기 결과 확인 정책은 확인과 미확인입니다.

미확인 쓰기를 사용하여 유효하지 않은 데이터를 삽입할 때 발생하는 오류는 놓치기 쉽습니다. 예를 들어 2 개의 문서를 같은 `_id` 로 삽입하려 하면 쉘은 예외를 던집니다.

```shell
> db.foo.insert({"_id" : 123, "x" : 1})
> db.foo.insert({"_id" : 123, "x" : 2})
E11000 duplicate key error index: test.foo.$_id_ dup key: { : 123.0 }
```

2 번째 쓰기의 쓰기 결과 확인 정책이 **미확인** 으로 보내졌다면, 2 번째 삽입은 예외를 던지지 않을 것입니다.

쉘에서는 클라이언트 라이브러리가 수행하는 것과 같은 방식의 쓰기 결과 확인 정책을 지원하지 않습니다. 미확인 쓰기를 수행하고 프롬프트를 회수하기 전에 마지막 연산이 성공했는지 확인합니다. 그래서 컬렉션 상에 일련의 유효하지 않는 연산을 수행하고 유효한 연산으로 끝마치면 쉘은 어떤 불평도 하지 않을것입니다.

```shell
> db.foo.insert({"_id" : 1}); db.foo.insert({"_id" : 1}); db.foo.count()
1
```

`getLastError` 를 호출하여 마지막 연산에 대한 오류 검사를 수행할 수 있습니다.

```shell
> db.foo.insert({"_id" : 1});
> db.foo.insert({"_id" : 1});
> print(db.getLastError());
E11000 duplicate key error index: test.foo.$_id_ dup key: { :1.0 }
> db.foo.count()
```