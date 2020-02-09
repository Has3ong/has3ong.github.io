---
title : MongoDB Getting Started
tags :
- Getting Started
- MongoDB
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

* MongoDB 데이터의 기본 단위는 문서인데 관계형 데이터베이스의 행과 유사하다.
* 같은 맥락에서 컬렉션은 스키아 없는 테이블로 생각할 수 있다.
* MongoDB 의 단일 인스턴스는 여러 독립적인 데이터베이스를 호스팅할 수 있고, 데이터베이스는 자체적인 컬렉션들의 권한을 가진다.
* 모든 문서는 문서 컬렉션 내에서 고유한 특수키인 "_id" 를 가지고 있다.
* MongoDB 는 인스턴스 관리와 데이터 조작에 유용한 JavaScript 쉘을 지원한다.

## Documents

MongoDB 의 핵심은 정렬된 key 와 연결된 value 의 집합으로 이루어진 문서 입니다.

자바스크립트에서 문서는 아래와 같이 객체로 표현할 수 있습니다.

```js
{"greeting" : "Hello, World!"}
```

위 예제는 `greeting` 이라는 key 에 연결된 `Hello, World!` 라는 값을 가집니다. 대부분의 문서는 이보다 더 복잡한 다중 key / value 쌍을 가집니다.

```js
{"greeting" : "Hello, World!", "foo" : 3}
```

문서의 값은 blob 형이 아닙니다. `greeting` 의 값은 문자열이고, `foo` 의 값은 정수입니다. 문서의 Key 는 문자열입니다.

MongoDB 는 데이터형과 대소문자를 구별합니다. 예를 들어 다음 예제는 서로 다릅니다.

```js
{"foo" : 3}
{"foo" : "3"}
```

다음 예제도 마찬가지 입니다.

```js
{"foo" : 3}
{"Foo" : 3}
```

MongoDB 의 문서에서 가장 중요한 점은 Key 가 중복될 수 없습니다. 예를 들어 다음 예제는 잘못된 문서입니다.

```js
{"greeting" : "Hello, World!", "greeting" : "Hello, MongoDB!"}
```

문서의 Key / Value 쌍은 정렬되어 있습니다. 그러므로 `{"x" : 1, "y" : 2}` 와 `{"y" : 2, "x" : 1}` 은 서로 다릅니다. 

## Collections

컬렉션은 문서의 모음입니다. 만약 MongoDB 의 문서가 관계형 데이터베이스의 행이라면 컬렉션은 테이블이라 볼 수 있습니다.

### Dynamic Schemas

컬렉션은 동적 스키마를 가집니다. 이는 하나의 컬렉션 내 문서들이 모두 다른 구조를 가질 수 있다는 의미입니다. 예를 들어 다음 문서들을 하나의 컬렉션 내에 같이 저장할 수 있습니다.

```js
{"greeting" : "Hello, World!"}
{"foo" : 5}
```

위 문서들은 value 의 데이터형 이 다를 뿐 아니라 key 마저도 완전히 다릅니다. 하지만, 스키마의 구조가 다른데 같은 컬렉션을 사용하는것은 비효율적입니다. 아래 예를통해 알려드리겠습니다.

* 컬렉션 별로 데이터를 뽑는것이 한 컬렉션 내 특정 데이터형을 뽑는것보다 효율적이다.
* 같은 종류의 데이터를 하나의 컬렉션에 모아두는게 데이터 지역성 측면에서 좋다.
* 하나의 컬렉션에 단일한 데이터형의 문서를 넣으면 더 효율적으로 인덱스를 생성할 수 있다.

위와 같이 스키마를 생성하고 같은 종류의 문서를 모아두는 데에는 이유가 있지만 MongoDB 에서 이를 강제하지는 않습니다.

### Naming

컬렉션은 그 이름으로 식별됩니다. 컬렉션명은 몇가지 제약조건을 제외한 UTF-8 문자열도 사용할 수 있습니다.

* 빈 문자열("") 은 유효한 컬렉션 명이 아니다.
* 컬렉션명에는 \0(null 문자) 을 쓸 수 없다. 이는 컬렉션명의 끝을 나타내는 문자이기 떄문입니다.
* *system* 으로 시작하는 컬렉션명은 예약어 이므로 사용할 수 없다.
  * *system.users* 컬렉션은 데이터베이스 사용자 정보를 가지고 있다.
  * *system.namespaces* 컬렉션은 데이터베이스 내 모든 컬렉션 정보를 가지고 있다.
* $ 예약어를 사용할 수 없다.

**1. Subcollections**

컬렉션을 체계화하는 기존의 방법 중 하나는 서브컬렉션의 네임스페이스에 `.` 문자를 쓰는것입니다.

예를들어 블로그 기능을 가지는 어플리케이션은 `blog.posts` 와 `blog.authors` 라는 컬렉션을 가질 수 있습니다. 이렇게 쓰는 이유는 체계화를 위한 방법 중 하나입니다.

## Databases

MongoDB 는 컬렉션에 문서를 그룹핑할 뿐만 아니라 데이터베이스에 컬렉션을 그룹지어 놓습니다. MongoDB 의 단일 인스턴스는 여러 데이터베익스를 호스팅 할 수 있으며, 각 데이터베이스를 완전히 독립적으로 취급할 수 있습니다.

하나의 데이터베이스는 자체 권한을 가지며, 따로 분리된 파일로 디스크에 저장됩니다. 한 어플리케이션의 데이터를 동일한 데이터베이스에 저장하는건 좋은 원칙입니다.

컬렉션과 마찬가지로 데이터베이스는 이름으로 식별됩니다.

직접 접근할 수 있지만 특별한 의미를 가지는 예약된 데이터베이스 이름도 있습니다.

* admin
  * 인증의 관점에서 root 데이터베이스다.
  * admin 데이터 베이스에 사용자를 추가하면, 해당 사용자는 자동으로 모든 데이터베이스에 대한 사용권한을 상속받는다.
  * 모든 데이터베이스 목록을 조회하거나 서비스를 중지하는 명령어는 admin 데이터베이스에서만 실행 가능하다.
* local
  * 절대로 복제되지 않기 때문에 특정 서버에만 저장하는 컬렉션에 사용
* config
  * MongoDB 를 샤딩 설정
  
컬렉션을 저장하는 데이터베이스의 이름을 컬렉션명 앞에 붙여서 올바른 컬렉션명인 네임스페이스를 얻을 수 있습니다.

예를 들어 cms 데이터베이스의 `blog.posts` 컬렉션을 사용한다면 컬렉션의 네임 스페이스는 `cms.blog.posts` 가 됩니다. 네임스페이스의 최대 길이는 121 bytes 지만, 실제로는 100 bytes 보다 짧아야합니다.
 
## Getting and Starting MongoDB

MongoDB 서버를 실행하기 위해선 먼저 `mongod` 를 실행합니다.

```shell
$ mongod 

mongod --help for help and startup options
2020-02-08T02:35:09.858+0000 [initandlisten] MongoDB starting : pid=3360 port=27017 dbpath=/data/db 64-bit host=fabric-1
2020-02-08T02:35:09.858+0000 [initandlisten] db version v2.6.10
2020-02-08T02:35:09.859+0000 [initandlisten] git version: nogitversion
2020-02-08T02:35:09.859+0000 [initandlisten] OpenSSL version: OpenSSL 1.0.2g  1 Mar 2016
2020-02-08T02:35:09.859+0000 [initandlisten] build info: Linux lgw01-12 3.19.0-25-generic #26~14.04.1-Ubuntu SMP Fri Jul 24 21:16:20 UTC 2015 x86_64 BOOST_LIB_VERSION=1_58
2020-02-08T02:35:09.860+0000 [initandlisten] allocator: tcmalloc
2020-02-08T02:35:09.860+0000 [initandlisten] options: {}
2020-02-08T02:35:09.861+0000 [initandlisten] journal dir=/data/db/journal
2020-02-08T02:35:09.861+0000 [initandlisten] recover : no journal files present, no recovery needed
2020-02-08T02:35:09.881+0000 [initandlisten] waiting for connections on port 27017
```

`mongod` 로 시작하면 기본 데이터 디렉토리로 */data/db* 를 사용한다. 데이터 디렉토리가 없거나 읽기 쓰기 권한이 없을때는 서버가 시작되지 않습니다.

그럴경우 데이터 디렉토리를 생성하고 `mkdir -p /data/db` 디렉토리에 읽기, 쓰기 권한이 있는지 확인해야합니다.

MongoDB 의 기본 포트는 27017 이며, 웹 브라우저는 28017 포트입니다.

## Introduction to the MongoDB Shell

MongoDB 는 명령행에서 MongoDB 인스턴스와 상호 작용하는 자바스크립트 Shell 을 제공합니다. Shell 은 관리 기능을 수행하거나, 실행중인 인스턴스를 점검하거나, 간단한 기능을 시험할 때 매우 유용합니다.

### Running the Shell

Shell 을 시작하기 위해 `mongo` 를 실행합니다.

```shell
$ mongo
MongoDB shell version: 2.6.10
connecting to: test
```

Shell 은 시작 시 자동으로 MongoDB 서버에 접속을 시도하기 때문에 Shell 을 시작하기 전에 `mongod` 를 시작했는지 확인해야합니다.

Shell 은 온전한 자바스크립트 Interpreter 로 임의의 자바스크립트 프로그램을 실행할 수 있습니다. 몇 가지 기본 연산도 수행 가능합니다.

```shell
> x = 200
200
> x / 5;
40
```

표준 자바스크립트 라이브러리의 모든 기능을 활용할 수 있습니다.

```shell
> Math.sin(Math.PI / 2);
1
> new Date("2010/1/1");
"Fri Jan 01 2010 00:00:00 GMT-0500 (EST)"
> "Hello, World!".replace("World", "MongoDB");
Hello, MongoDB!
```

자바스크립트 함수를 정의하고 호출할 수 있습니다.

```shell
> function factorial (n) {
... if (n <= 1) return 1;
... return n * factorial(n - 1);
... }
> factorial(5);
120
```

여러 줄의 명령도 작성할 수 있습니다.
 
### A MongoDB Client

임의의 자바스크립트를 실행하는 기능이 멋지긴해도, Shell 은 독자적을 쓸 수 있는 MongoDB 클라이언트에 있습니다.

Shell 은 시작할 때 MongoDB 서버의 `test` 데이터베이스에 연결을 하고 이 데이터베이스에 연결을 전역변수 db에 할당합니다. Shell 에서는 이 변수를 통해 MongoDB 에 접근합니다.

현재 db 에 할당된 데이터베이스를 확인하려면 `db` 를 입력합니다.

```shell
> db
test
```

Shell 은 자바스크립트 구문으로는 유효하지 않지만, SQL Shell 사용자들에게 친숙한 추가 기능을 포함하고 있습니다. 추가 기능은 다른 확장 기능을 제공하진 않지만, 편리한 문법을 제공합니다. 예를 들어 가장 중요한 작업 중 하나인 데이터베이스 선택을 살펴보겠습니다.

```shell
> use foobar
switched to db foobar
```

db 변수를 확인하면 foobar 데이터 베이스를 가리키고 있을 것입니다.

```shell
> db
foobar
```

자바스크립트 Shell 이기 때문에 변수를 입력하면 변수가 문자열로 변환되고 출력됩니다.

컬렉션은 db 변수를 통해 접근할 수 있습니다. 예를 들어 `db.baz` 는 현재 데이터베이스의 baz 컬렉션을 반환합니다.

### Basic Operations with the Shell

Shell 에서 데이터를 조작하고 보기 위해 *Create*, *Read*, *Update*, *Delete* 의 4 가지 기본적인 작업을 사용할 수 있습니다.

**1. Create**

insert 함수는 컬렉션에 문자를 추가합니다.

예를 들어 블로그 게시물을 저장한다고 가정하겠습니다. 우선 문서를 나타내는 자바스크립트 객체인 post 라는 지역 변수를 생성합니다. post 변수는 **"title", "content", "date"** 와 같은 Key 를 가집니다.

```shell
> post = {"title" : "My Blog Post",
... "content" : "Here's my blog post.",
... "date" : new Date()}
{
	"title" : "My Blog Post'",
	"content" : "Here's my blog post.",
	"date" : ISODate("2020-02-08T05:35:15.113Z")
}
```

이 객체는 유효한 MongoDB 문서며 `insert` 함수를 이용해서 *blog* 컬렉션에 저장할 수 있습니다.

```shell
> db.blog.insert(post)
WriteResult({ "nInserted" : 1 })
```

저장이되면 컬렉션에 `find` 를 통해 호출해서 확인할 수 있습니다.

```shell
> db.blog.find()
{
  "_id" : ObjectId("5e3e48a7a85c8a51548510ea"),
  "title" : "My Blog Post'",
  "content" : "Here's my blog post.",
  "date" : ISODate("2020-02-08T05:35:15.113Z")
}
```

**_id** 키가 자동으로 추가되었고 다른 key / value 쌍들은 입력한 대로 저장된 것을 확인할 수 있습니다.

**Read**

`find` 와 `findOne` 은 컬렉션을 쿼리하는데 사용합니다. 단일 문서 보기를 원한다면 `findOne` 을 사용합니다.

```shell
> db.blog.findOne()
{
	"_id" : ObjectId("5e3e48a7a85c8a51548510ea"),
	"title" : "My Blog Post'",
	"content" : "Here's my blog post.",
	"date" : ISODate("2020-02-08T05:35:15.113Z")
}
```

**Update**

게시물을 수정하고 싶다면 `update` 를 사용합니다. `update` 는 최소 두 개의 메개변수를 가집니다. 1 번째는 수정할 문서를 찾기 위한 기준이며, 2 번째는 새로운 문서입니다.

앞서 만든 게시물에 댓글을 사용할 수 있도록 한다고 가정해보겠습니다. 그러기 위해선 문서에 새 key 값으로 댓글 배열을 추가하겠습니다.

```
> post.comments = []
[ ]
```

다음으로 새 버전의 문서로 교체하는 `update` 를 수행합니다.

```shell
> db.blog.update({title : "My Blog Post"}, post)
WriteResult({ "nMatched" : 0, "nUpserted" : 0, "nModified" : 0 })
```

이제 문서는 **comments** Key 를 가지게 됩니다.

```shell
> db.blog.findOne()
{
	"_id" : ObjectId("5e3e48a7a85c8a51548510ea"),
	"title" : "My Blog Post'",
	"content" : "Here's my blog post.",
	"date" : ISODate("2020-02-08T05:35:15.113Z"),
	"comments" : [ ]
}
```

**Delete**

`remove` 문서를 데이터베이스에서 영구적으로 삭제합니다. 매개변수 없이 호출하면 컬렉션 내의 모든 문서가 삭제됩니다.

```shell
db.blog.remove({title : "My Blog Post")}
```

## Data Types

MongoDB 는 문서의 값으로 다양한 데이터형을 지원합니다. 모든 데이터형의 개요를 알아보겠습니다.

### Basic Data Types

MongoDB 문서는 자바스크립트와 개념적으로 닮았다는 점에서 JSON 과 닮았다고 생각할 수 있습니다.

MongoDB 는 JSON 의 필수 key / value 쌍의 성질을 유지하면서 추가적인 데이터형을 지원합니다. 아래는 흔한 데이터형 입니다.

**null**

null 값과 존재하지 않는 필드를 표현

```json
{"x" : null}
```

**boolean**

참과 거짓에 사용

```json
{"x" : true}
```

**integer**

Shell 은 64 bit 부동 소수점 숫자를 기본으로 사용합니다.

```json
{"x" : 3.14}
```

```json
{"x" : 3}
```

4 byte 혹은 8 byte 의 부호 정수는 각각 `NumberInt` 혹은 `NumberLong` 클래스를 사용합니다.

```json
{"x" : NumberInt("3")}
{"x" : NumberLong("3")}
```

**string**

모든 UTF-8 문자열도 표현할 수 있습니다.

```json
{"x" : "foobar"}
```

**date**

날짜는 1970 년 1월 1일 부터의 시간을 1 / 1.0000 초 단위로 저장합니다. 표준 시간대는 저장하지 않습니다.

```json
{"x" : new Date()}
```

**regular expression**

쿼리는 자바스크립트의 정규표현식 문법을 사용할 수 있습니다.

```json
{"x" : /foobar/i}
```

**array**

값의 Set 이나 List 를 배열로 표현할 수 있습니다.

```json
{"x" : ["a", "b", "c"]}
```

**embedded document**

문서는 부모 문서의 값으로 내장된 전체 문서를 포함할 수 있습니다.

```json
{"x" : {"foo" : "bar"}}
```

**object id**

객체 ID 는 문서용 12 byte ID 입니다.

```json
{"x" : ObjectId()}
```

또한 필요할 수도 있는 몇가지 일반적인 종류도 있습니다.

**binary data**

임의의 byte 문자열이며 Shell 에서 조작 불가능 합니다. 이진 데이터는 데이터베이스에 UTF-8 이 아닌 문자열을 저장하기 위한 유일한 방법입니다.

**code**
  
쿼리와 문서는 임의의 자바스크립트 코드를 포함할 수 있습니다.

```json
{"x" : function() { /* ... */)}
```
  
### Dates

자바스크립트에서 `Date` 클래스는 MongoDB 날짜형을 위해 사용됩니다. 새로운 `Date` 객체를 생성할 때는 항상 `Date(...)` 가 아닌 `new Date(...)` 를 호출합니다.

`Date` 는 Shell 에서 현지 시간대 설정을 이요해 표시합니다. 하지만 데이터베이스의 날짜는 1970 년 1월 1일 부터의 시간을 1/1,000 초 단위로 저장하고 표준 시간대 정보는 없습니다.

### Arrays

배열은 정렬 연산(List, Stack, Queue) 과 비정렬 연산(Set) 에 호환성 있게 사용할 수 있는 값입니다.

다음 예제에서 `things` Key 는 배열 값을 가집니다.

```json
{"things" : ["pie", 3.14]}
```

### Embedded Documents

문서는 Key 에 대한 값으로 사용될 수 있으며, 이것을 내장 문서라고 합니다. 내장 문서는 데이터를 Key / Value 쌍의 평면적인 구조보다 좀 더 자연스러운 방법으로 구성하기 위해 사용합니다.

예를 들어 아래 예제와 같이 한 사람에 대한 정보를 나타내는 문서를 가지고 있으며 그의 주소를 저장하기 원한다면, `address` 내장 문서로 중첩할 수 있습니다.

```json
{
  "name" : "John Doe",
  "address" : {
    "street" : "123 Park Street",
    "city" : "Anytown",
    "state" : "NY"
  }
}
```

위 예제에서 `address` Key 에 대한 값은 `street`, `city`, `state` 의 Key / Value 쌍을 가지는 내장 문서입니다.

### _id and ObjectIds

MongoDB 에 저장된 모든 문서는 `_id` Key 를 가져야 합니다. `_id` Key 값은 어떤 데이터 형이어도 상관없지만 `ObjectId` 가 기본입니다. 하나의 컬렉션에서 모든 문서는 고유한 `_id` 값을 가져야 하며, 이 값은 컬렉션 내의 고유하게 구분되도록 보장합니다.

**1. ObjectIds**

`ObjectId` 는 `_id` 의 기본 데이터형입니다.

`ObjectId` 는 12 byte 의 저장소를 사용하고 24 자리 16 진수 문자열 표현이 가능합니다. 각 byte 마다 2 자리를 사용합니다.

`ObjectId` 가 16 진수 문자열로 표현된다 하더라도 문자열은 저장된 데이터보다 실제로 2 배만큼 더 길어지게됩니다.

`ObjectId` 를 연속적으로 생성하면, 매번 마지막 숫자만 바뀝니다. 이것은 `ObjectId` 가 생성되는 방식 때문입니다. ObjectId 의 12 byte 는 다음과 같이 생성됩니다.

```
0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 
  타임스탬프  |    장비   |  PID  |    증가량
```

`ObjectId` 의 처음 4 byte 는 1970년 1월 1일 부터의 시간을 1/10,000 단위로 저장되는 타임 스탬프 입니다.

* 타임스탬프는 그 다음 5 byte 와 묶였을 때 초 단위의 고유성을 제공한다.
* 타임스탬프가 첫 번째로 온다는 것은 `ObjectId` 들이 입력 순서로 정렬됨을 의미합니다.

`ObjectId` 의 다음 3 byte 는 `ObjectId` 의 생성된 장비의 유일한 식별자 입니다. 주로 장비 호스트명의 해시값입니다. 이 byte 를 포함하면 다른 장비에서 `ObjectId` 의 충돌이 일어나지 않음을 보장합니다.

단일 장비에서 동시에 생성하는 다른 프로세스 간에 유일성을 제공하기 위해 다음 2 byte 에는 `ObjectId` 를 생성하는 **PID(Process Identifier)** 를 가져옵니다.

`ObjectId` 의 앞에서 9 byte 는 1초 동안 장비와 프로세스에 걸쳐서 유일성을 보장합니다. 

마지막 3 byte 는 1초 내에서 단일 프로세스의 유일성을 보장해 주는 단순히 증가하는 숫자입니다. 이것은 1초에 프로세스당 $256^3$ (16,777,216) 개의 고유한 `ObjectId` 를 생성할 수 있도록 해 줍니다.

**2. Autogeneration of _id**

앞서 말한대로 문서가 입력될 때 `_id` Key 를 명시하지 않으면 입력된 문서에 자동으로 추가됩니다. 이것은 MongoDB 서버에서 관리될 수 있지만 일반적으로 클라이언트 쪽에서 드라이버에 의해 관리됩니다. 클라이언트에서 `_id` 를 생성하는것은 MongoDB 의 철학을 반영합니다.

작업은 서버 밖에서 언제든지 드라이버가 가능할 때 밀어 넣어져야 합니다. 이 철학은 MongoDB 와 같은 확장형 데이터베이스들이 데이터베이스 계층에서보다는 어플리케이션 계층에서 규모 확장이 더 용이하다는 사실을 반영합니다.

## Using the MongoDB Shell

이전에선 로컬 `mongod` 인스턴스에 연결했지만, 가끔 유저의 장비가 도달할 수 있는 MongoDB 의 인스턴스에 Shell 을 연결할 수 있습니다. 다른 장비 또는 포트에 `mongod` 를 연결하려면 Shell 을 시작할 때 호스트명, 포트, 그리고 데이터베이스를 명시해야 합니다.

```shell
$ mongo some-host:30000/myDB
MongoDB shell version: 2.6.10
connecting to: some-host:30000/myDB
```

`mongod` 를 연결하지 않고 Shell 을 시작할 수도 있습니다.

```shell
$ mongo --nodb
MongoDB shell version: 2.6.10
```

`new Mongo (host)` 를 실행함으로 편한 시간에 `mongod` 에 연결할 수 있습니다.

```shell
> conn = new Mongo("some-host:30000)
connection to some-host:30000
> db = conn.getDB("myDB")
myDB
```

### Tips for Using the Shell

Shell 에서 `help` 를 입력해 내장된 도움말을 확인할 수 있습니다.

```shell
> help

	db.help()                    help on db methods
	db.mycoll.help()             help on collection methods
	sh.help()                    sharding helpers
	rs.help()                    replica set helpers
	help admin                   administrative help
	help connect                 connecting to a db help
	help keys                    key shortcuts
	help misc                    misc things to know
	help mr                      mapreduce

	show dbs                     show database names
	show collections             show collections in current database
	show users                   show users in current database
	show profile                 show most recent system.profile entries with time >= 1ms
	show logs                    show the accessible logger names
	show log [name]              prints out the last segment of log in memory, 'global' is default
	use <db_name>                set current database
	db.foo.find()                list objects in collection foo
	db.foo.find( { a : 1 } )     list objects in foo where a == 1
	it                           result of the last line evaluated; use to further iterate
	DBQuery.shellBatchSize = x   set default number of items to display on shell
	exit                         quit the mongo shell
```

컬렉션의 수준은 `db.foo.help()` 로 확인할 수 있습니다.

```shell
> db.foo.help()

DBCollection help
	db.foo.find().help() - show DBCursor help
	db.foo.count()
	db.foo.copyTo(newColl) - duplicates collection by copying all documents to newColl; no indexes are copied.
	db.foo.convertToCapped(maxBytes) - calls {convertToCapped:'foo', size:maxBytes}} command
	db.foo.dataSize()
	db.foo.distinct( key ) - e.g. db.foo.distinct( 'x' )
	db.foo.drop() drop the collection
	db.foo.dropIndex(index) - e.g. db.foo.dropIndex( "indexName" ) or db.foo.dropIndex( { "indexKey" : 1 } )
	db.foo.dropIndexes()
	db.foo.ensureIndex(keypattern[,options]) - options is an object with these possible fields: name, unique, dropDups
	db.foo.reIndex()
	db.foo.find([query],[fields]) - query is an optional query filter. fields is optional set of fields to return.
	                                              e.g. db.foo.find( {x:77} , {name:1, x:1} )
	db.foo.find(...).count()
	db.foo.find(...).limit(n)
	db.foo.find(...).skip(n)
	db.foo.find(...).sort(...)
	db.foo.findOne([query])
	db.foo.findAndModify( { update : ... , remove : bool [, query: {}, sort: {}, 'new': false] } )
	db.foo.getDB() get DB object associated with collection
	db.foo.getPlanCache() get query plan cache associated with collection
	db.foo.getIndexes()
	db.foo.group( { key : ..., initial: ..., reduce : ...[, cond: ...] } )
	db.foo.insert(obj)
	db.foo.mapReduce( mapFunction , reduceFunction , <optional params> )
	db.foo.aggregate( [pipeline], <optional params> ) - performs an aggregation on a collection; returns a cursor
	db.foo.remove(query)
	db.foo.renameCollection( newName , <dropTarget> ) renames the collection.
	db.foo.runCommand( name , <options> ) runs a db command with the given name where the first param is the collection name
	db.foo.save(obj)
	db.foo.stats()
	db.foo.storageSize() - includes free space allocated to this collection
	db.foo.totalIndexSize() - size in bytes of all the indexes
	db.foo.totalSize() - storage allocated for all data and indexes
	db.foo.update(query, object[, upsert_bool, multi_bool]) - instead of two flags, you can pass an object with fields: upsert, multi
	db.foo.validate( <full> ) - SLOW
	db.foo.getShardVersion() - only for use with sharding
	db.foo.getShardDistribution() - prints statistics about data distribution in the cluster
	db.foo.getSplitKeysForChunks( <maxChunkSize> ) - calculates split points over all chunks and returns splitter function
	db.foo.getWriteConcern() - returns the write concern used for any operations on this collection, inherited from server/db if set
	db.foo.setWriteConcern( <write concern doc> ) - sets the write concern for writes to the collection
	db.foo.unsetWriteConcern( <write concern doc> ) - unsets the write concern for writes to the collection
```

함수가 어떤 기능을 수행하는지 알기 위해서는 괄호 없이 입력하면 됩니다.

```shell
> db.foo.update

function ( query , obj , upsert , multi ){
    assert( query , "need a query" );
    assert( obj , "need an object" );

    var wc = undefined;
    // can pass options via object for improved readability
    if ( typeof(upsert) === 'object' ) {
        assert( multi === undefined,
                "Fourth argument must be empty when specifying upsert and multi with an object." );

        var opts = upsert;
        multi = opts.multi;
        wc = opts.writeConcern;
        upsert = opts.upsert;
    }
```

### Running Scripts with the Shell

아래와 같이 자바스크립트 파일을 Shell 로 전달하여 실행할 수 있습니다. 단순히 명령행에 스크립트만 남습니다.

```shell
$ mongo script1.js script2.js script3.js
MongoDB shell version: 2.6.10
connecting to: test
I am script1.js
I am script2.js
I am script3.js
```

`load()` 함수를 사용하여 대화용 Shell 에서 스크립트를 실행할 수 있습니다.

```shell
> load("script1.js")
I am script1.js
>
```

### Creating a .mongorc.js

만약 자주 로드되는 스크립트가 있다면 `mongorc.js` 파일에 넣고 싶을것입니다.

로그인할 때 사용자를 맞이할 Shell 을 가정할 때, 홈 디렉토리에 `mongorc.js` 파일을 만들고 다음을 추가합니다.

```js
// mongorc.js

var compliment = ["attractive", "intelligent", "like Batman"];
var index = Math.floor(Math.random() * 3);

print("Hello, you're looking particularly "+compliment[index]+" today!");
```

그러면 Shell 을 시작할 때 다음 문구를 보게 됩니다.

```shell
$ mongo
MongoDB shell version: 2.6.10
connecting to: test
Hello, you're looking particularly like Batman today!
>
```

### Customizing Your Prompt

기본 Shell 프롬프트는 문자열이나 함수에 `prompt` 변수를 설정하여 재정의할 수 있습니다. 예를 들어 완료되는 데 몇 분이 걸리는 쿼리를 실행하는 경우, 마지막 작업이 완료된 시각을 알 수 있도록 현재 시각을 출력하는 프롬프트를 만들 수 있습니다.

```js
prompt = function() {
  return (new Date())+"> ";
};
```

현재 사용하는 데이터베이스를 보여주는 프롬프트를 만들 수 있습니다.

```js
prompt = function() {
  if (typeof db == 'undefined'){
    return '(nodb)>';
  }
  
  try {
    db.runCommand({getLastError:1]});
  }
  catch (e) {
    print(e);
  }
  
  return db+"> ";
};
```

일반적으로 프롬프트는 `getLastError` 호출을 포함해야 합니다. 그렇게 해 두면 Shell 의 연결이 끊겼을 때 쓰기에서 오류를 감지해 다시 연결해 줍니다.

### Editing Complex Variables

Shell 에 다중행 지원은 다소 제한적입니다. 따라서 코드나 객체의 큰 블록에 대해 작업할 때는 편집기에서 편집합니다. 그렇게 하면 Shell 에서 `EDITOR` 변수를 설정해야 합니다.

```shell
> EDITOR="/user/bin/emacs"
```

이제 'edit 변수명' 형식으로 변수를 편집할 수 있습니다.

``shell
> var wap = db.books.findOne({title: "War and Peace"})
> edit wap
```

`EDITOR="EDITOR 경로` 를 `mongorc.js` 파일에 추가하면 다시는 설정에 대해 걱정할 필요 없습니다.