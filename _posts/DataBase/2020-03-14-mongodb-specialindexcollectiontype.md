---
title : MongoDB Special Index and Collection Types
tags :
- Collection
- Index
- MongoDB
- Database
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Capped Collections

MongoDB 의 일반적인 컬렉션은 동적으로 생성되고 추가적인 데이터에 맞춰 크기가 자동으로 늘어납니다. MongoDB 는 **제한 컬렉션(Capped Collection)** 으로 불리는 컬렉션을 지원하는데 이는 미리 생성되어 크기가 고정됩니다.(`Example 1`) 이미 가득찬 제한 컬렉션에 입력하려 한다면 컬렉션이 **환형 큐(Circular Queue)** 처럼 작동합니다.

빈 공간이 없다면 가장 오래된 문서가 지워지고 새로운 문서가 그 자리를 차지합니다.(`Example 2`) 

> Example 1 - New documents are inserted at the end of the queue

![image](https://user-images.githubusercontent.com/44635266/76207406-13a1f980-6241-11ea-8bff-019aa0a5450f.png)

> Example 2 - When the queue is full, the oldest element will be replaced by the newest

![image](https://user-images.githubusercontent.com/44635266/76207420-1a307100-6241-11ea-9746-e6279058fb9a.png)

제한 컬렉션은 문서의 입력 순서대로 저장되고, 삭제된 문서들로 인해 생긴 가용한 저장 공간 목록을 유지할 필요가 없음을 보장합니다.

제한 컬렉션은 대부분 MongoDB 컬렉션과 접근 방식이 다른데 데이터가 디스크의 고정된 영역에 순서대로 기록합니다. 이는 회전식 디스크에서 쓰기를 빠르게 수행하도록 만들어 주며, 특히 전용 디스크가 주어질 때 그런 경향이 있습니다.

제한 컬렉션은 유연성이 부족하지만 로깅을 위해서는 유용합니다.

### Creating Capped Collections

일반 컬렉션과 달리 제한 컬렉션은 명시적으로 생성되어야 합니다. 제한 컬렉션을 생성하려면 `create` 명령어를 사용합니다. 쉘에서는 `createCollection` 을 사용하여 생성할 수 있습니다.

```js
> db.createCollection("my_collection", {"capped" : true, "size" : 100000});
{ "ok" : true }
```

위 명령으로 100,000 Byte 고정 크기로 제한 컬렉션 `my_collection` 을 만듭니다. 또한 문서 수 제한과 더불어 크기도 지정할 수 있습니다.

```js
> db.createCollection("my_collection2", 
... {"capped" : true, "size" : 100000, "max" : 100});
{ "ok" : true }
```

일단 제한 컬렉션이 생성되면 변경할 수 없기 때문에 생성하기 전에 크기에 대해 신중히 검토해야 합니다.

제한 컬렉션을 생성하는 또 다른 방법은 일반 컬렉션을 변환하는것입니다. `convertToCapped` 명령어를 사용해 실행할 수 있습니다. 다음 예제는 `test` 컬렉션을 10,000 Byte 크기의 제한 컬렉션으로 변환합니다.

```js
> db.runCommand({"convertToCapped" : "test", "size" : 10000});
{ "ok" : true }
```

제한 컬렉션을 일반 컬렉션으로 전환하는 방법은 없습니다.

### Sorting Au Naturel

제한 컬렉션에서 사용할 수 있는 **순차 정렬(Natural Sort)** 라는 정렬 형태가 있습니다. 순차 정렬은 문서를 디스크에 나타나는 순서로 반환합니다.(`Example 3`)

> Example 3 - Sort by `{"$natural” : 1}`

![image](https://user-images.githubusercontent.com/44635266/76207450-2ae0e700-6241-11ea-966a-e715207b7d15.png)

이는 문서의 위치가 자주 바뀌기 때문에 대부분의 컬렉션에선 유용하지 않습니다. 하지만, 제한 컬렉션 내 문서는 항상 입력 순서로 보관되므로 순차는 입력순서와 동일합니다.

따라서 순차 정렬은 문서를 오래된 것부터 새로운 것 순으로 제공합니다. 물론 역순으로도 가능합니다.(`Example 4`)

```js
> db.my_collection.find().sort({"$natural" : -1})
```

> Example 4 - Sort by `{"$natural” : -1}`

![image](https://user-images.githubusercontent.com/44635266/76207478-346a4f00-6241-11ea-9530-4e1f19af2973.png)

### Tailable Cursors

**꼬리를 무는 커서(Tailable Cursor)** 결과를 모두 꺼내도 종료되지 않는 커서입니다. 이 커서는 결과를 다 반환하여도 종료되지 않기 때문에 컬렉션에 데이터가 추가되면 바로 새로운 결과를 반환할 수 있습니다. 이 커서는 제한컬렉션에서만 사용가능한데 일반 컬렉션에서는 입력 순서가 추적되지 않기 때문입니다.

이 커서는 문서가 제한 컬렉션에 입력되었을 때 문서를 처리하는 데 사용합니다. `mongo` 쉘에서는 사용할 수 없지만 PHP 에선 다음과 같이 사용할 수 있습니다.

```php
$cursor = $collection->find()->tailable();

while (true) {
    if (!$cursor->hasNext()) {
        if ($cursor->dead()) {
            break;
        }
        sleep(1);
    }
    else {
        while ($cursor->hasNext()) {
            do_stuff($cursor->getNext());

        }
    }
}
```

### No-_id Collections

`createCollection` 을 호출할 때 `autoIndexId` 옵션을 `false` 로 설정하여 `_id` 가 없는 컬렉션을 생성할 수 있습니다. 권장되는 방법은 아니지만 입력 전용 컬렉션의 속도를 약간 향상시킬 수 있습니다.

## Time-To-Live Indexes

제한 컬렉션 보다 더 유연한 나이 순 삭제 시스템이 필요하다면 **TTL(Time-To-Live)** 인덱스를 이용하여 각 문서에 유효 시간을 설정할 수 있습니다. 문서가 미리 설정된 시간에 도달하면 지워집니다. 이런 형태의 인덱스는 세션 스토리지와 같은 문제를 캐싱하는데 유용합니다.

`ensureIndex` 의 두 번째 인수에 `expireAfterSeconds` 옵션을 명시하여 TTL 인덱스를 생성할 수 있습니다.

```js
> // 24-hour timeout
> db.foo.ensureIndex({"lastUpdated" : 1}, {"expireAfterSeconds" : 60*60*24})
```

위 명령은 `lastUpdated` 필드에 TTL 인덱스를 생성합니다. 서버 시간이 문서 시간의 `expreAfterSeconds` 를 지나면 그 문서는 삭제됩니다.

MongoDB 는 TTL 인덱스를 매 분마다 청소하기 때문에 초 단위에 의존할 필요가 없습니다. `collMod` 명령어를 이용하여 `expireAfterSeconds` 를 변경할 수 있습니다.

```js
> db.runCommand( {
    "collMod" : "someapp.cache" ,
    "index" : { 
        "keyPattern" : {
            "lastUpdated" : 1
            }, 
        "expireAfterSeconds" : 3600
    }
} ); 
```

주어진 컬렉션에 다중 TTL 인덱스도 가질 수 있습니다.

## Full-Text Indexes

MongoDB 의 **전문 인덱스(Full-Text Index)** 는 문장을 빠르게 검색하는 기능 뿐만 아니라 다국어 형태소 분석 및 정지단어를 위한 내장된 기능을 제공합니다.

모든 인덱스 생성비용이 비싸지만 전문 인덱스는 특히 비쌉니다. 전문 인덱스는 `--setParameter textSearchEnabled=true` 옵션으 ㄹ주고 MongoDB 를 시작하거나 임시 `setParameter` 명령어를 통해 설정합니다.

```js
> db.adminCommand({"setParameter" : 1, "textSearchEnabled" : true})
```

문장 검색을 실행하려면 우선 `text` 인덱스를 생성합니다.

```js
> db.hn.ensureIndex({"title" : "text"})
```

이제 인덱스를 사용하기 위해 `text` 명령어를 사용하겠습니다.

```js
test> db.runCommand({"text" : "hn", "search" : "ask hn"})
{
    "queryDebugString" : "ask|hn||||||",
    "language" : "english",
    "results" : [
        {
            "score" : 2.25,
            "obj" : {
                "_id" : ObjectId("50dcab296803fa7e4f000011"),
                "title" : "Ask HN: Most valuable skills you have?",
                "url" : "/comments/4974230",
                "id" : 4974230,
                "commentCount" : 37,
                "points" : 31,
                "postedAgo" : "2 hours ago",
                "postedBy" : "bavidar"
            }
        },
        {
            "score" : 0.5625,
            "obj" : {
                "_id" : ObjectId("50dcab296803fa7e4f000001"),
                 "title" : "Show HN: How I turned an old book...",
                 "url" : "http://www.howacarworks.com/about",
                 "id" : 4974055,
                 "commentCount" : 44,
                 "points" : 95,
                 "postedAgo" : "2 hours ago",
                 "postedBy" : "AlexMuir"
            }
        },
        {
            "score" : 0.5555555555555556,
            "obj" : {
                 "_id" : ObjectId("50dcab296803fa7e4f000010"),
                 "title" : "Show HN: ShotBlocker - iOS Screenshot detector...",
                 "url" : "https://github.com/clayallsopp/ShotBlocker",
                 "id" : 4973909,
                 "commentCount" : 10,
                 "points" : 17,
                 "postedAgo" : "3 hours ago",
                 "postedBy" : "10char"
            }
        }
    ],
    "stats" : {
        "nscanned" : 4,
        "nscannedObjects" : 0,
        "n" : 3,
        "timeMicros" : 89
    },
    "ok" : 1
}
```

일치하는 문서는 관령성이 떨어지는 순서로 반환합니다. 첫 번째는 Ask HN 이며, 두 번재는 Show Hn 인데 이 둘은 일부분이 일치합니다. 각 결과 항목 앞부분의 `score` 필드는 결과가 쿼리에 일치하는 정도를 나타냅니다.

전문인덱스는 단지 인덱스 문자열 데이터입니다. 다른 데이터 종류는 무시되며 인덱스에 포함되지 않습니다. 컬렉션당 전문 인덱스는 오직 하나만 허용되지만 이는 여러 필드를 포함할 수 있습니다.

```js
> db.blobs.ensureIndex({"title" : "text", "desc" : "text", "author" : "text"})
```

키에 순서가 있는 다중키 인덱스와는 다르며 각 필드는 동등하게 간주됩니다. 가중치를 명시해서 MongoDB 가 각 필데으 부여하는 상대적인 중요도를 제어할 수 있습니다.

```js
> db.hn.ensureIndex({"title" : "text", "desc" : "text", "author" : "text"}, 
... {"weights" : {"title" : 3, "author" : 2}})
```

기본 가중치는 1 이며, 1 부터 10 억 까지 가중치를 사용할 수 있습니다. 가중치는 `title` 필드가 최고며, 뒤 따르는 `author` 와 그 다음으로 `desc` 순으로 부여됩니다.

일부 컬렉션의 경우 문서가 포함한 필드를 알지 못할수도 있습니다. `$**` 로 인덱스를 생성하여 문서 내의 모든 문자열 필드에 전문 인덱스를 생성할 수 있습니다. 이는 모든 최상위 문자열 필드에 대한 인덱스뿐만 아니라 문다열 필드에 내장된 문서와 배열에 대한 검색도 포함합니다.

```js
> db.blobs.ensureIndex({"$**" : "text"})
```

또한 `$**` 에 가중치를 부여할 수 있습니다.

```js
> db.hn.ensureIndex({"whatever" : "text"}, 
... {"weights" : {"title" : 3, "author" : 1, "$**" : 2}})
```

`whatever` 는 아직 사용되지 않았기 때문에 무엇이든지 될 수 있습니다. 가중치는 모든 필드를 인덱싱 할 것임을 명시하기 때문에 MongoDB 에 필드 목록을 제공할 필요가 없습니다.

### Search Syntax

기본적으로 MongoDB 는 `ask Or hn` 과 같이 모든 단어를 OR 로 쿼리합니다. 이는 전문 쿼리를 수행하는 데 가장 효율적인 방법이지만 정확한 문구 검색과 NOT 도 수행할 수 있습니다. `ask hn` 으로 정확한 문구를 검색하려면 쿼리를 따옴표로 감싸 쿼리합니다.

```js
> db.runCommand({text: "hn", search: "\"ask hn\""})
{
    "queryDebugString" : "ask|hn||||ask hn||",
    "language" : "english",
    "results" : [
        {
            "score" : 2.25,
            "obj" : {
                "_id" : ObjectId("50dcab296803fa7e4f000011"),
                "title" : "Ask HN: Most valuable skills you have?",
                "url" : "/comments/4974230",
                "id" : 4974230,
                "commentCount" : 37,
                "points" : 31,
                "postedAgo" : "2 hours ago",
                "postedBy" : "bavidar"
            }
        }
    ],
    "stats" : {
        "nscanned" : 4,
        "nscannedObjects" : 0,
        "n" : 1,
        "nfound" : 1,
        "timeMicros" : 20392
    },
    "ok" : 1
}
```

이는 MongoDB 가 우선 OR 일치를 수행한 다음에 문서가 AND 일치를 보장하도록 후처리하기 때문에 OR 형 일치보다 느립니다.

문자열을 쿼리에 포함시킬 수 있고 제외시킬 수도 있습니다.

```js
> db.runCommand({text: "hn", search: "\"ask hn\" ipod"})
```

이는 `ask hn` 을 검색하고 `ipod` 를 선택적으로 검사합니다.

`-` 를 이용해서 특정 문자열을 포함하지 않은 검색을 할 수 있습니다.

```js
> db.runCommand({text: "hn", search: "-startup vc"})
```

이는 `vc` 에 일치하고 `startup` 단어를 포함하지 않는 결과를 반환합니다.

### Full-Text Search Optimization

전문 검색을 최적화하기 위한 방법은 두 가지입니다. 우선 다른 기준을 첫 번째로 두고 전문 필드를 그 다음으로 두어 복합 인덱스를 생성합니다.

```js
> db.blog.ensureIndex({"date" : 1, "post" : "text"})
```

`date` 에 따라 몇 개의 작은 트리 구조로 쪼개기 때문에 이는 전문 인덱스 분할로 불립니다. 이는 특정 날짜에 대해 전문 검색을 훨씬 빠르게 만듭니다.

인덱스로 쿼리를 커버하기 위해 다른 기준을 뒤쪽에 두어 사용할 수 있습니다. `author` 와 `post` 필드만 반환한다면 두 필드에 대해 복합 인덱스를 생성할 수 있습니다.

```js
> db.blog.ensureIndex({"post" : "text", "author" : 1})
```

앞쪽에 두는 것과 뒤쪽에 두는 형태는 합쳐질 수 있습니다.

```js
> db.blog.ensureIndex({"date" : 1, "post" : "text", "author" : 1})
```

앞쪽이나 뒤쪽 인덱스 필드에 다중키 필드를 사용할 수 없습니다.

전문 인덱스 생성은 컬렉션에 `usePowerOf2Sizes` 옵션을 자동으로 활성화하는데, 이 공간 할당 방법을 제어합니다. 이는 쓰기 속도를 향상시키므로 비활성화하면 안됩니다.

### Searching in Other Languages

문서가 입력되었을 때 MongoDB 는 인덱스 필드를 살펴보고 기본 구성 단위로 줄여가며 각 단어의 형태소를 분석합니다. 하지만, 다른 언어는 다른 방식으로 단어의 형태소를 분석하기 때문에 인덱스나 문서의 언어가 무엇인지 명시해야 합니다.

따라서 문장 유형의 인덱스에는 `default_language` 옵션이 지정될 수 있고 기본값은 `english` 지만 다양한 언어를 설정할 수 있습니다.

프랑스어 인덱스는 다음과 같이 실행할 수 있습니다.

```js
> db.users.ensureIndex({"profil" : "text", "intérêts" : "text"}, 
... {"default_language" : "french"})
```

## Geospatial Indexing

MongoDB 는 공간 정보 인덱스를 가지고 있습니다. 가장 흔히 사용되는 것은 지구 표면 형태의 지도를 위한 `2dsphere` 와 지도를 위한 `2d` 이빈다.

`2dsphere` 는 점, 선, 다각형을 GeoJSON 형식으로 명시하도록 허용합니다. 점은 `[longitude, latitude]` 를 나타내는 배열입니다.

```json
{
    "name" : "New York City",
    "loc" : {
        "type" : "Point",
        "coordinates" : [50, 2]
    }
}
```

선은 점의 배열로 주어집니다.

```json
{
    "name" : "Hudson River",
    "loc" : {
        "type" : "Line",
        "coordinates" : [[0,1], [0,2], [1,2]]
    }
}
```

다각형은 선과 동일한 방식으로 명시되지만 다른 `type` 을 가집니다.

```json
{
    "name" : "New England",
    "loc" : {
        "type" : "Polygon",
        "coordinates" : [[0,1], [0,2], [1,2]]
    }
}
```

`loc` 필드명은 변경해도 상관없지만 하위객체의 필드명들은 GeoJSON 에 명시되어 있어서 변경할 수 없습니다.

`ensureIndex` 로 `2dsphere` 유형을 사용하는 공간 정보 인덱스를 생성할 수 있습니다.

```js
> db.world.ensureIndex({"loc" : "2dsphere"})
```

### Types of Geospatial Queries

교차, 포함, 근접과 같은 몇 가지 수행 가능한 공간 정보 쿼리가 있습니다. 쿼리하려면 찾고자 하는 것을 `{"$gemoetry" : geoJsonDesc}` 처럼 GeoJSON 객체로 지정합니다.

예를 들어 `$geoIntersects` 연산자를 이용해 쿼리의 위치와 교차하는 문서를 찾을 수 있습니다.

```js
> var eastVillage = {
... "type" : "Polygon",
... "coordinates" : [
...     [-73.9917900, 40.7264100], 
...     [-73.9917900, 40.7321400], 
...     [-73.9829300, 40.7321400], 
...     [-73.9829300, 40.7264100]
... ]}
> db.open.street.map.find(
... {"loc" : {"$geoIntersects" : {"$geometry" : eastVillage}}})
```

위 예제는 East Village 내에 한 점을 가지는 모든 점 / 선 / 다각형이 포함된 문서를 찾습니다.

완전히 한 지역에 포함되는 것에 대한 쿼리를 하려면 `$within` 을 사용합니다.

```js
> db.open.street.map.find({"loc" : {"$within" : {"$geometry" : eastVillage}}})
```

마지막으로 `$near` 를 이용해 근처 위치에 대해 쿼리할 수 있습니다.


```js
>>> db.open.street.map.find({"loc" : {"$near" : {"$gemotry" : eastVillage}}})
```

`$near` 는 유일하게 정렬을 포함하는 공간 정보 연산이며, `$near` 에 나온 결과는 항상 거리가 가까운 곳부터 먼 곳 순으로 반환됩니다.

공간 정보 쿼리에 대한 흥미로운 점은 `$geoIntersects` 나 `$within` 을 사용하는데 공간 정보 인덱스가 필요하지 않다는 것입니다. 하지만 공간 정보 필드에 인덱스를 가지면 확실히 쿼리 속도가 높아지므로 대개 권장됩니다.

### Compound Geospatial Indexes

더 복잡한 쿼리를 최적화하기 위해 공간 정보 인덱스를 다린 필드와 묶을 수 있습니다.

`restaurants` 나 `pizza` 식으로 좁힐 수 있습니다.

```js
> db.open.street.map.ensureIndex({"tags" : 1, "location" : "2dsphere"})
```

그러면 East Village 내에서 피자 레스토랑을 빠르게 찾을 수 있습니다.

```js
> db.open.street.map.find({"loc" : {"$within" : {"$geometry" : eastVillage}}, 
... "tags" : "pizza"})
```

첫 번째 인덱스 조건으로 더 많은 결과를 필터링하는 쪽으로 선택합니다.

### 2D Indexes

비-구체의 지도를 위해 `2dsphere` 대신 `2d` 인덱스를 사용할 수 있습니다.

```js
> db.hyrule.ensureIndex({"tile" : "2d"})
```

`2d` 인덱스는 구체 대신 완전히 평평한 표면이라고 생각하면 됩니다. 문서는 2d 인덱스 필드에 대해 2 개의 요소로 구성된 배열을 사용합니다. 샘플 문서는 아래와 같습니다.

```json
{
    "name" : "Water Temple",
    "tile" : [ 32, 22 ]
}
```

`2d` 인덱스는 단지 인덱스 점들입니다. 점들의 배열을 저장할 수 있지만 정확하게는 선이 아닌 점들의 배열을 저장합니다. 이는 특히 `$within` 쿼리에 대해 중요한 차이가 있습니다.

길거리를 점의 배열로 저장했다면 주어진 도형 안에 점들 중 하나가 있을 때 문서는 `$within` 과 일치합니다. 하지만 그 점들로 생성된 선은 도형 안에 완전히 포함되지 않습니다.

기본적으로 공간 정보 인덱싱은 값이 -180 ~ 180 까지 범위 내에 있다 가정합니다. 더 크거나 작은 범위를 사용하려면 `ensureIndex` 옵션으로 지정하면 됩니다.

```js
> db.star.trek.ensureIndex({"light-years" : "2d"}, {"min" : -1000, "max" : 1000})
```

이는 $2,000 \times 2,000$ 평방에 대한 보정된 공간 정보 인덱스를 생성합니다.

`2d` 는 `2dsphere` 보다 이전에 나와서 쿼리가 더 단순합니다. 오직 `$near` 나 `$within` 을 사용할 수 있고, `$geometry` 하위객체는 갖지 않습니다. 단지 좌표만 지정하면 됩니다.

```js
> db.hyrule.find({"tile" : {"$near" : [20, 21]}})
```

위 쿼리는 모든 문서를 점 (20, 21) 로부터의 거리 순으로 찾습니다. 문서 수 제한을 명시하지 않으면 기본 제한인 100 개 문서로 적용됩니다. 예를 들어 다음 코드는 (20, 21) 에 가까운 10 개 문서를 반환합니다.

```js
> db.hyrule.find({"tile" : {"$near" : [20, 21]}}).limit(10)
```

`$within` 은 직사각형, 원, 다각형 안에 모든 점을 쿼리할 수 있습니다. 직사각형은 `$box` 옵션을 이용합니다.

```js
> db.hyrule.find({"tile" : {"$within" : {"$box" : [[10, 20], [15, 30]]}}})
```

`$box` 는 첫 번재 요소는 좌측 하단 좌표, 두 번째 요소는 우측 상단 좌표를 명시합니다.

비슷하게 중점과 반경을 배열로 가지는 `$center` 로 원 안의 모든 점을 찾을 수 있습니다.

```js
> db.hyrule.find({"tile" : {"$within" : {"$center" : [[12, 25], 5]}}})
```

마지막으로 점의 배열로 다각형을 명시할 수 있습니다.

```js
> db.hyrule.find(
... {"tile" : {"$within" : {"$polygon" : [[0, 20], [10, 0], [-10, 0]]}}})
```

위 예제는 주어진 삼각형 안에 점을 포함하는 모든 문서의 위치를 파악합니다. 다각형의 형태를 만들기 위해 목록의 마지막 점은 첫 번째 점과 연결됩니다.

## Storing Files with GridFS

GridFS 는 MongoDB 에 대용량 이진파일을 저장하기 위한 메커니즘입니다. 파일 저장에 GridFS 를 고려하는 이유는 다음과 같습니다.

* GridFS 를 사용하면 아키텍처 스택을 단순화할 수 있다.
* GridFS 는 MongoDB 를 위해 설정한 기존의 복제나 자동 샤딩을 이용할 수 있어, 파일 저장소를 위한 장애복구와 분산 확장이 더욱 쉽다.
* GridFS 는 사용자가 올린 파일을 저장할 때 특정 파일시스템이 가지는 문제를 피할 수 있다.
* MongoDB 는 2 GB 청크에 데이터 파일을 할당하기 때문에 GridFS 를 이용하면 광대한 디스크 지역성을 얻을 수 있습니다.

하지만 몇 가지 단점도 존재합니다.

* 느린 성능
* 문서를 수정하려면 전체를 삭제하고 다시 저장하는 방법 밖에 없다.

GridFS 는 일반적으로 큰 변화가 없고 순차적인 방식으로 접근하려는 대용량 파일을 가지고 있을 때 최선입니다.

### Getting Started with GridFS: mongofiles

`mongofiles` 유틸리티로 GridFS 를 설치하고 운영할 수 있습니다.

`mognofiles` 를 사용해보겠습니다.

```shell
$ echo "Hello, world" > foo.txt
$ ./mongofiles put foo.txt
connected to: 127.0.0.1
added file: { _id: ObjectId('4c0d2a6c3052c25545139b88'),
              filename: "foo.txt", length: 13, chunkSize: 262144,
              uploadDate: new Date(1275931244818),
              md5: "a7966bf58e23583c9a5a4059383ff850" }
done!
$ ./mongofiles list
connected to: 127.0.0.1
foo.txt 13
$ rm foo.txt
$ ./mongofiles get foo.txt
connected to: 127.0.0.1
done write to: foo.txt
$ cat foo.txt
Hello, world
```

위 예제는 `put`, `list`, `get` 기본적인 연산을 수행했습니다. `put` 은 파일시스템으로부터 파일을 받아 GridFS 에 추가합니다. `list` 는 GridFS 의 파일 목록을 출력합니다. `get` 은 `put` 과 반대로 GridFS 로 부터 파일을 받아 파일시스템에 저장합니다.

### Working with GridFS from the MongoDB Drivers

모든 클라이언트 라이브러리는 GridFS API 를 가지고 있습니다. 예를 들어 `pyMongo` 를 사용하여 `mongofiles` 로 했을 때 똑같은 일련의 작업을 수행할 수 있습니다.

```python
>>> from pymongo import Connection
>>> import gridfs
>>> db = Connection().test
>>> fs = gridfs.GridFS(db)
>>> file_id = fs.put("Hello, world", filename="foo.txt")
>>> fs.list()
[u'foo.txt']
>>> fs.get(file_id).read()
'Hello, world'
```

### Under the Hood

GridFS 는 파일 저장을 위한 간단한 명세이며 일반 MongoDB 문서를 기반으로 만들어졌습니다. MongoDB 서버는 GridFS 요청을 처리하면서 실제로는 특별한 작업을 하지 않고 클라이언트 쪽의 드라이버 도구가 처리합니다.

GridFS 의 기본 개념은 대용량 파일을 청크로 나눈 뒤 청크를 문서로 저장할 수 있다는 것입니다. MongoDB 는 문서에 이진 데이터를 저장할 수 있기 때문에 청크에 대한 저장 부하를 최소화할 수 있습니다. 파일의 청크를 저장하는 것 외에 여러 청크를 묶고 파일의 메타데이터를 포함하는 문서를 하나 만듭니다.

GridFS 의 청크는 자체 콜렉션에 저장됩니다. 청크는 기본적으로 *fs.chunks* 컬렉션에 저장되지만 바꿀 수 있습니다. 청크 컬렉션 내 각 문서의 구조는 매우 간단합니다.

```json
{
    "_id" : ObjectId("..."),
    "n" : 0,
    "data" : BinData("..."),
    "files_id" : ObjectId("...")
}
```

다른 MongoDB 문서처럼 청크도 고유 `_id` 를 가지고 있습니다. 그리고 몇 개의 키를 더 가지고 있습니다.

* **files_id**
  * 청크에 대한 메타데이터를 포함하는 파일 문서의 `_id`
* **n**
  * 다른 청크를 기준으로 한 파일 내 청크의 위치
* **data**
  * 파일 내 청크의 크기

각 파일의 메타데이터는 기본적으로 별도의 컬렉션인 *fs.files* 에 저장됩니다. files 컬렉션 내 각 문서는 GridFS 에서 하나의 파일을 나타내고 해당 파일과 관련된 어떠한 메타데이터라도 포함할 수 있습니다. 사용자 정의 키 외에도 GridFS 명세에서 강제하는 몇 개의 키가 더 있습니다.

* **_id**
  * 파일의 고유 id 로 청크의 `file_id` 키의 값으로 저장
* **length**
  * 파일 내용의 총 바이트 수
* **chunkSize**
  * 파일을 구성하는 각 청크의 크기이며 바이트 단위, 디폴트 값은 256K
* **uploadDate**
  * GridFS 에 파일이 저장된 시간
* **md5**
  * 서버에서 생성된 파일 내용의 md5 체크썸