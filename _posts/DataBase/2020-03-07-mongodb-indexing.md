---
title : MongoDB Indexing
tags :
- Indexing
- MongoDB
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Introduction to Indexing

데이터베이스의 인덱스는 책의 인데긋와 유사합니다. 책의 인덱스가 책 전체를 살펴봐야 한다면, 데이터베이스의 인덱스는 지름길을 택해서 내용을 가리키는 정렬된 목록을 확인합니다. 이는 많은 양의 명령을 더 빠르게 쿼리할 수 있도록 해줍니다.

인덱스를 사용하지 않는 쿼리를 **테이블 스캔** 이라 하며, 이는 서버가 쿼리를 찾기 위해 데이터베이스 전체를 살펴봐야한다는 의미입니다. 서버에서 테이블 스캔을 하면 큰 컬렉션의 경우 매우 느리기 때문에 피하는 것이 좋습니다.

예를 들어 1,000,000 건의 문서를 갖는 컬렉션을 생성해보겠습니다.

```js
> for (i=0; i<1000000; i++) {
...     db.users.insertOne(
...         {
...              "i" : i, 
...              "username" : "user"+i,
...              "age" : Math.floor(Math.random()*120),  
...              "created" : new Date()
...         }
...     );
... }
```

이 컬렉션을 쿼리한다면 해당 쿼리가 실행될 때 MongoDB 가 무엇을 하는지 확인하기 위해 `explain()` 함수를 이용할 수 있습니다. 예제를 확인하기 위해 무작위 사용자 명으로 쿼리를 시도해 보겠습니다.

```js
> db.users.find({username: "user101"}).explain()
{
    "cursor" : "BasicCursor",
    "nscanned" : 1000000,
    "nscannedObjects" : 1000000,
    "n" : 1,
    "millis" : 721,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "isMultiKey" : false,
    "indexOnly" : false,
    "indexBounds" : {
        
    }
}
```

`nscanned` 는 MongoDB 가 쿼리를 실행하면서 살펴본 문서의 수며, 컬렉션 안에 들어있는 모든 문서의 수와 같습니다. 즉, MongoDB 는 모든 문서 안에 있는 모든 필드를 살펴봐야 합니다. 이 작업은 완료까지 1초가 걸렸습니다. `millis` 필드는 쿼리를 수행하는 데 걸린 시간을 밀리세컨드 단위로 보여줍니다.

`n` 필드는 반환받은 결과의 개수를 보여줍니다. 이 값은 1 인데 사용자 명이 `user101` 이 단 한명의 사용자만 있기 때문입니다. MongoDB 는 사용자명이 유일하다는 것을 알지 못했기 때문에 일치하는 항목을 찾기 위해 컬렉션 안의 모든 문서를 살펴봐야 합니다. 이 쿼리를 최적화 하려면 MongoDB 가 `user101` 을 발견한 다음에 탐색을 중지하도록 쿼리의 결과를 한개로 제한합니다.

```js
> db.users.find({username: "user101"}).limit(1).explain()
{
    "cursor" : "BasicCursor",
    "nscanned" : 102,
    "nscannedObjects" : 102,
    "n" : 1,
    "millis" : 2,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "isMultiKey" : false,
    "indexOnly" : false,
    "indexBounds" : {
        
    }
}
```

스캔 수가 줄어들었고 쿼리는 거의 즉각적입니다. 하지만 대체로 이는 실용적이지 못한 해결방법입니다. 만약 `user999999` 를 찾는다면 어떻게 할까요.

인덱스는 이와 같은 쿼리를 바로잡기에 좋은 방법입니다. MongoDB 가 데이터를 빨리 찾을 수 있도록 하기 위해 인덱스는 주어진 필드로 데이트를 구성하기 때문입니다. 사용자명 필드에 인덱스를 생성해보겠습니다.

```js
> db.users.ensureIndex({"username" : 1})
```

인덱스 생성은 장비와 컬렉션의 크기에 따라 몇 분 정도 걸릴 수 있습니다. `ensureIndex` 호출이 몇 초 후에도 응답하지 않는다면 `db.currentOp()` 를 실행하거나 `mongod` 의 로그를 확인하여 인덱스 구축 진행 상황을 확인합니다.

인덱스 구축이 완료되면 최초의 쿼리를 다시 시도해 보겠습니다.

```js
> db.users.find({username: "user101"}).explain()
{
    "cursor" : "BtreeCursor username_1",
    "nscanned" : 1,
    "nscannedObjects" : 1,
    "n" : 1,
    "millis" : 3,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "isMultiKey" : false,
    "indexOnly" : false,
    "indexBounds" : {
        "username" : [
            [
                "user101",
                "user101"
            ]
        ]
    }
}
```

위 `explain()` 결과는 더 복잡하지만 지금은 `n`, `nscanned`, `millis` 를 제외한 다른 필드는 무시하겠습니다. 보다시피 쿼리는 이제 거의 즉각적이고 어떤 사용자명으로 쿼리하더라도 비슷하거나 심지어 더 나은 실행 시간을 가집니다.

```js
> db.users.find({username: "user999999"}).explain().millis
1
```

인덱스는 쿼리 수행 시간에서 많은 차이를 만들어 냅니다. 하지만 인덱스는 나름 비용을 가지는데, 모든 쓰기는 추가한 모든 인덱스 때문에 더 오래 걸립니다. 이는 데이터가 변경될 때마다 문서 자체뿐만 아니라 MongoDB 가 모든 인덱스를 갱싱해야 하기 때문입니다.

따라서 MongoDB 는 컬렉션당 최대 64 개까지의 인덱스를 갖도록 제한되어 있습니다. 일반적으로 주어진 컬렉션에 두세 개 이상의 인덱스를 갖지 않는게 좋습니다.

### Introduction to Compound Indexes

인덱스는 모든 값을 정렬된 순서로 보관하기 때문에 인덱스 키로 문서를 정렬하는 작업에 훨씬 빠른 성능을 제공합니다. 하지만 인덱스가 정렬의 앞부분에 놓일 경우에만 정렬에 도움이 됩니다. 예를 들어 `username` 인덱스는 아래 정렬에 많은 도움이 되지는 않습니다.

```js
> db.users.find().sort({"age" : 1, "username" : 1})
```

위 명령은 `age` 로 정렬하고 그 뒤에 `username` 으로 정렬하는데, `username` 에 의해 완전 정렬은 별로 도움이 되지 않습니다. 이 정렬을 최적화 하려면 `age` 와 `username` 에 인덱스를 만들면 됩니다.

```js
> db.users.ensureIndex({"age" : 1, "username" : 1})
```

이는 복합 인덱스라 불리며 쿼리가 여러 정렬 방향이나 검색 조건에 여러 키를 가질 때 유용합니다. 복합 인덱스는 하나 이상의 필드로 구성된 인덱스입니다.

정렬 없는 쿼리를 실행했을 때 아래처럼 보이는 `user` 컬렉션이 있다고 가정하겠습니다.

```js
> db.users.find({}, {"_id" : 0, "i" : 0, "created" : 0})
{ "username" : "user0", "age" : 69 }
{ "username" : "user1", "age" : 50 }
{ "username" : "user2", "age" : 88 }
{ "username" : "user3", "age" : 52 }
{ "username" : "user4", "age" : 74 }
{ "username" : "user5", "age" : 104 }
{ "username" : "user6", "age" : 59 }
{ "username" : "user7", "age" : 102 }
{ "username" : "user8", "age" : 94 }
{ "username" : "user9", "age" : 7 }
{ "username" : "user10", "age" : 80 }
...
```

위 컬렉션에 `{"age" : 1, "username" : 1}` 로 인덱스를 만들면 인덱스는 대략 다음처럼 보일것입니다.

```js
[0, "user100309"] -> 0x0c965148
[0, "user100334"] -> 0xf51f818e
[0, "user100479"] -> 0x00fd7934
...
[0, "user99985" ] -> 0xd246648f
[1, "user100156"] -> 0xf78d5bdd
[1, "user100187"] -> 0x68ab28bd
[1, "user100192"] -> 0x5c7fb621
...
[1, "user999920"] -> 0x67ded4b7
[2, "user100141"] -> 0x3996dd46
[2, "user100149"] -> 0xfce68412
[2, "user100223"] -> 0x91106e23
...
```

각 인덱스 항목은 나이와 사용자 명을 포함하며 디스크에 있는 문서의 위치를 가라킵니다. `age` 필드는 완전히 오름차순으로 정렬되며, 각 나이 안에서 `username` 역시 오름차순으로 정렬됩니다. 각 나이별로 연관된 약 8,000 개의 사용자 명이 있기 때문에 일반적인 개념을 전달하는 데 필요한 몇몇 사용자명만 나타냈습니다.

MongoDB 가 이 인덱스를 사용하는 방법은 실행하고 있는 쿼리의 종류에 따라 다릅니다. 가장 많이 사용하는 3 가지 방법을 알아보겠습니다.

**db.users.find({"age" : 21}).sort({"username" : -1})**

이는 단일 값을 찾기 위한 포인트 쿼리입니다. 인덱스의 두 번째 필드에 인해 결과는 이미 적절한 순서로 정렬되는데, MongoDB 는 `{"age" : 21}` 과 일치하는 마지막 항목에서 시작하여 순서대로 인덱스를 탐색합니다.

```js
[21, "user999977"] -> 0x9b3160cf
[21, "user999954"] -> 0xfe039231 
[21, "user999902"] -> 0x719996aa
...
```

이런 쿼리는 매우 효율적입니다. MongoDB 는 곧바로 정확한 나이로 건너뛸 수 있고 인덱스 탐색은 올바른 순서로 데이터를 반환하기 때문에 결과를 정렬할 필요가 없습니다.

MongoDB 는 어느 방향으로도 인덱스를 쉽게 탐색하기 때문에 정렬 방향은 문제가 되지 않습니다.

**db.users.find({"age" : {"$gte" : 21, "$lte" : 30}})**

이는 다중값 쿼리이며 여러 값과 일치한느 문서를 찾아냅니다. MongoDB 는 일치하는 문서를 반환받기 위해 인덱스에 있는 첫 번째 키인 `age` 를 이처럼 사용합니다.

```js
[21, "user100000"] -> 0x37555a81
[21, "user100069"] -> 0x6951d16f 
[21, "user1001"]   -> 0x9a1f5e0c 
[21, "user100253"] -> 0xd54bd959
[21, "user100409"] -> 0x824fef6c
[21, "user100469"] -> 0x5fba778b
...
[30, "user999775"] -> 0x45182d8c
[30, "user999850"] -> 0x1df279e9
[30, "user999936"] -> 0x525caa57
...
```

일반적으로 MongoDB 가 쿼리에 대한 인덱스를 사용하면 인덱스 순서에 따라 문서 결과를 반환합니다.

**db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).sort({"username" : 1})**

이는 이전과 같은 다중값 쿼리지만 정렬을 포함하빈다. 이전처럼 MongoDB 는 검색 조건에 맞는 인덱스를 사용합니다.

```js
[21, "user100000"] -> 0x37555a81
[21, "user100069"] -> 0x6951d16f
[21, "user1001"]   -> 0x9a1f5e0c
[21, "user100253"] -> 0xd54bd959
...
[22, "user100004"] -> 0x81e862c5
[22, "user100328"] -> 0x83376384
[22, "user100335"] -> 0x55932943
[22, "user100405"] -> 0x20e7e664
...
```

하지만 인덱스는 사용자명을 정렬된 순서로 반환하지 않으며 쿼리는 사용자명에 의해 정렬된 결과를 요청하기 때문에 MongoDB 는 결과를 반환하기전에 메모리에서 정렬해야 합니다. 따라서 이 쿼리는 일반적으로 위의 쿼리보다 비효율적입니다.

결과가 단지 두 세 문서라면 MongoDB 는 정렬하는 데 많은 일을 하지 않습니다. 더 많은 결과가 있다면 느려지거나 전혀 작동하지 않을 것입니다. 결과가 32 MB 이상이면 MongoDB 는 데이터가 너무 많아 정렬을 거부한다는 오류를 발생시킵니다.

```js
Mon Oct 29 16:25:26 uncaught exception: error: {
    "$err" : "too much data for sort() with no index.  add an index or 
        specify a smaller limit",
    "code" : 10128
}
```

마지막 예제에서 사용할 수 있는 또 다른 인덱스는 같은 키를 역순으로 한 `{"username" : 1, "age" : 1}` 입니다. 이때 MongoDB 는 모든 인덱스 항목을 탐색하지만 원하는 순서로 되돌립니다. 인덱스의 `age` 부분을 이용해 일치하는 문서를 가져오겠습니다.

```js
["user0", 69]
["user1", 50]
["user10", 80]
["user100", 48]
["user1000", 111]
["user10000", 98]
["user100000", 21] -> 0x73f0b48d
["user100001", 60]
["user100002", 82]
["user100003", 27] -> 0x0078f55f
["user100004", 22] -> 0x5f0d3088
["user100005", 95]
...
```

이는 거대한 **인-메모리(In-Memory)** 정렬이 필요하지 않다는 점에서 좋습니다. 하지만 일치하는 모든 값을 찾으려면 전체 인덱스를 훑어야 합니다. 따라서 두세 개의 일치하는 항목을 찾은 후에 MongoDB 가 인덱스 스캔을 중지하도록 만들기 위해 검색 개수를 제한할 때 정렬 키를 첫 번째에 놓는 것은 좋은 방법입니다.

`explain()` 을 이용해 MongoDB 가 기본으로 `db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).sort({"username" : 1})` 를 어떻게 수행하는지 진단할 수 있습니다.

```js
> db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).
... sort({"username" : 1}).
... explain()
{
    "cursor" : "BtreeCursor age_1_username_1",
    "isMultiKey" : false,
    "n" : 83484,
    "nscannedObjects" : 83484,
    "nscanned" : 83484,
    "nscannedObjectsAllPlans" : 83484,
    "nscannedAllplans" : 83484,
    "scanAndOrder" : true,
    "indexOnly" : false,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "millis" : 2766,
    "indexBounds" : {
        "age" : [
            [
                21,
                30
            ]
        ],
        "username" : [
            [
                {
                    "$minElement" : 1
                },
                {
                    "$maxElement" : 1
                }
            ]
        ]
    }
    "server" : "spock:27017"
}
```

`cursor` 필드가 나타내는 바는 이 쿼리가 `{"age" : 1, "username" : 1}` 인덱스를 사용한다는 것입니다. `scanAndOrder` 필드는 MongoDB 가 메모리에서 데이터를 정렬한다는 의미를 나타냅니다.

MongoDB 가 특정한 인덱스를 사용하도록 강제하기 위해 `hint` 를 사용할 수 있으므로 `{"username" : 1, "age" : 1}` 인덱스를 대신 사용해서 같은 쿼리를 다시 실행해보겠습니다. 이 쿼리는 더 많은 문서를 살펴보지만 인-메모리 정렬이 필요없습니다.

```js
> db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).
... sort({"username" : 1}).
... hint({"username" : 1, "age" : 1}).
... explain()
{
    "cursor" : "BtreeCursor username_1_age_1",
    "isMultiKey" : false,
    "n" : 83484,
    "nscannedObjects" : 83484,
    "nscanned" : 984434,
    "nscannedObjectsAllPlans" : 83484,
    "nsacannedAllplans" : 984434
    "scanAndOrder" : true,
    "indexOnly" : false,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "millis" : 14820,
    "indexBounds" : {
        "username" : [
            [
                {
                    "$minElement" : 1
                },
                {
                    "$maxElement" : 1
                }
            ]
        ],
        "age" : [
            [
                21,
                30
            ]
        ]
    }
    "server" : "spock:27017"
}
```

첫 번재 인덱스를 확실한 승자로 만들어서 실행하는 데 15 초 정도 걸렸습니다. 하지만 각 쿼리 결과의 개수를 제한하면 새로운 승자가 나타납니다.

```js
> db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).
... sort({"username" : 1}).
... limit(1000).
... hint({"age" : 1, "username" : 1}).
... explain()['millis']
2031
> db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).
... sort({"username" : 1}).
... limit(1000).
... hint({"username" : 1, "age" : 1}).
... explain()['millis']
181
```

대부분의 어플리케이션은 쿼리에 대해 가능한 모든 결과가 아닌 처음 몇 개를 원하기 때문에 `{"sortKey" : 1, "queryCriteria" : 1}` 과 같은 인덱스 형태는 어플리케이션에서 대체로 잘 작동합니다. 내부적으로 인덱스가 구성되는 방법 때문에 확장도 잘됩니다.

인덱스는 기본적으로 왼쪽 최말단 리프에는 가장 작은 값이, 오른쪽 최말단 리프에 가장 큰 값이 있는 트리 구조입니다. `sort key` 가 날짜라면, 트리의 왼쪽부터 오른쪽으로 탐색하기 때문에, 기본적으로 시간에 따라 탐색할 것입니다. 따라서 오래된 데이터보다 최신의 데이터를 사용하는 경향이 있는 어플리케이션을 위해 MongoDB 는 전체가 아닌 트리의 오른쪽 최말단 브랜치들만 메모리에 보관해야 합니다. 이와같은 인덱스를 **우편향(right-balanced)** 이라고 하며, 가능하다면 인덱스를 우편향으로 만들어야 합니다. `_id` 인덱스가 우편향 인덱스의 한 예입니다.

### Using Compound Indexes

복합 인덱스에 대해 좀 더 자세히 다뤄보겠습니다.

**1. Choosing key directions**

지금까지 인덱스 항목은 오름차순 또는 작은 것에서 큰 것으로 정렬되었습니다. 하지만, 두 개의 검색 조건으로 정렬할 필요가 있다면 다른 방향으로 향하는 인덱스 키가 있어야 합니다. 

예를 들어, 위 컬렉션을 최연소부터 최연장으로 정렬된 상태에서 사용자명을 Z 부터 A 까지 정렬한다고 가정하겠습니다. 이전의 인덱스는 이 문제에 대해 매우 비효율적입니다. 각 나이 집단의 사용자들은 Z-A 순서가 아닌 A-Z 순서의 `username` 으로 정렬되기 때문입니다. 위 복합 인덱스는 오른차순의 `age` 와 내림차순의 `username` 을 얻기 위한 어떠한 유용한 순서 정보도 갖고 있지 않습니다. 복합된 정렬을 다른 방향으로 최적화하려면 방향이 맞는 인덱스를 사용합니다. 이 예제에서는 `{"age" : 1, "username" : -1}` 을 사용하여 데이터를 다음과 같이 구성할 수 있습니다.

```js
[21, "user999977"] -> 0xe57bf737 
[21, "user999954"] -> 0x8bffa512
[21, "user999902"] -> 0x9e1447d1
[21, "user999900"] -> 0x3a6a8426
[21, "user999874"] -> 0xc353ee06
...
[30, "user999936"] -> 0x7f39a81a
[30, "user999850"] -> 0xa979e136
[30, "user999775"] -> 0x5de6b77a
...
[30, "user100324"] -> 0xe14f8e4d
[30, "user100140"] -> 0x0f34d446
[30, "user100050"] -> 0x223c35b1
```

나이는 최연소부터 최연장으로 배열되고 각 나이 안에서 사용자명은 Z - A 로 정렬됩니다.

**2. Using covered indexes**

쿼리가 단지 인덱스에 포함된 필드를 찾고 있다면 문서를 가져올 필요가 없습니다. 인덱스가 사용자에 의해 요구되는 모든 값을 포함하고 있다면 쿼리가 **커버링(Covering)** 된다고 할 수 있습니다. 실무에서는 언제나 문서로 되돌아가기 보다는 **커버드 인덱스(Covered Index)** 를 사용합니다. 이러한 방법으로 작업 셋을 훨씬 작게 만들 수 있으며, 특히 이를 우편향 인덱스와 묶으면 좋습니다.

쿼리가 확실히 인덱스만 사용하도록 만들기 위해 `_id` 필드를 반환받지 않도록 하려면 반환받을 키에 대한 지정을 해야 합니다. 쿼리하지 않는 필드에 인덱스를 만들어야 할 수 있기 때문에 더 빠른 쿼리에 대한 필요와 쓰기로 인해 늘어날 부하를 잘 조율해야 합니다.

커버드 쿼리에 대해 `explain` 을 실행하면 `indexOnly` 필드는 `true` 가 됩니다.

배열을 포함한 필드에 인덱스를 만들면 그 인덱스는 쿼리를 커버할 수 없습니다. 반환 받는 필드에서 배열 필드를 제외하더라도 그런 인덱스를 사용해서 쿼리를 커버할 수 없습니다.

**3. Implicit indexes**

복합 인덱스는 이중 임무를 수행할 수 있고 다른 쿼리에 대해 다른 인덱스처럼 행동할 수 있습니다. `{"age" : 1, "username" : 1}` 인덱스를 가지면 `age` 필드는 단지 `{"age" : 1}` 로 인덱스를 가지는 것과 동일한 방법으로 정렬됩니다. 따라서 복합 인덱스는 자체적으로 `{"age" : 1}` 인덱스를 가지고 수행하는 것처럼 사용될 수 있습니다.

이는 필요한 만큼 많은 키에 적용 시킬 수 있습니다. 인덱스가 N 키를 가지면 그 키들의 앞 뿌분은 공짜 인덱스가 됩니다. 예를 들어 `{"a" : 1, "b" : 1, "c" : 1, ..... "z" : 1}` 과 같은 인덱스가 있다면 사실상 `{"a": 1}, {"a": 1, "b" : 1}, {"a": 1, "b": 1, "c": 1}` 등으로 인덱스를 가집니다.

이는 키의 어떠한 하위셋도 보유하지 않습니다. 단지 인덱스의 앞 부분을 이용하는 쿼리만 그 인덱스를 활용할 수 있기 때문에 `{"b": 1}, {"a" : 1, "c" : 1}` 인덱스를 사용하는 쿼리는 최적화 되지 않습니다.

### How $-Operators Use Indexes

어떤 쿼리는 다른 것보다 인덱스를 더 효율적으로 사용할 수 있고, 다른 쿼리는 사용할 수 없습니다. 이번 절은 MongoDB 가 다양한 쿼리 연산자를 처리하는 방법을 알아보겠습니다.

**1. Inefficient operators**

인덱스를 전혀 사용할 수 없는 쿼리가 몇 가지 있습니다. `$where` 쿼리와 `{"key" : {"$exists" : true}}` 처럼 Key 가 존재하는지 확인하는 쿼리 등 입니다.

`x` 에 평범한 인덱스가 있다면 `x` 가 존재하지 않는 문서에 대한 쿼리는 `{"x" : {"$exists" : false}}` 인덱스를 사용할 수 있습니다. 하지만 존재하지 않는 필드는 null 필드와 동일한 방식으로 인덱스에 저장되기 때문에 쿼리는 실제로 값이 null 인지 혹은 존재하지 않는지 확인하기 위해 각 문서를 방문해야 합니다. 희소 인덱스를 사용한다면 `{"$exists" : true}` 나 `{"$exists" : false}` 에 는 사용할 수 없습니다.

일반적으로 Negation 조건에 비효율적입니다. `$ne` 쿼리는 인덱스를 사용하지만 지정된 항목을 제외한 모든 인덱스 항목을 살펴봐야 하기 때문에 기본적으로 전체 인덱스를 살펴봐야 합니다.

예를 들어 그런 쿼리를 위해 탐색된 인덱스 범위는 다음과 같습니다.

```js
> db.example.find({"i" : {"$ne" : 3}}).explain()
{
    "cursor" : "BtreeCursor i_1 multi",
    ...,
    "indexBounds" : {
        "i" : [
            [
                {
                    "$minElement" : 1
                },
                3
            ],
            [
                3,
                {
                    "$maxElement" : 1
                }
            ]
        ]
    },
    ...
}
```

이 쿼리는 3 보다 작은 모든 인덱스 항목과 3보다 큰 모든 인덱스 항목을 조사합니다. 이는 컬렉션의 광범위한 부분이 3 인 경우에는 효율적일 수 있지만 그렇지 않다면 모두를 확인해야 합니다.

`$not` 은 때때로 인덱스를 사용하지만 어떻게 사용하는지는 모릅니다. 이는 `{"key" : {"$lt" : 7}}` 로 만드는 것과 같이 기초적인 범위와 정규표현식을 반대로 뒤집을 수 있습니다. 하지만 `$not` 을 사용하는 대부분의 다른 쿼리는 테이블 스캔을 수행합니다. `$nin` 은 항상 테이블 스캔을 사용합니다.

예를 들어 `birthday` 필터를 갖고 있지 않은 모든 사용자를 찾고 있다 가정하겠습니다. 어플리케이션이 생일 필드를 3월 20일 부터 추가하기 시작했음을 알았다면 그 전에 생성된 사용자로 쿼리를 제한할 수 있습니다.

```js
> db.users.find({"birthday" : {"$exists" : false}, "_id" : {"$lt" : march20Id}})
```

쿼리에서 필드 순서는 상관없으며, MongoDB 는 순서에 관계없이 인덱스를 사용할 수 있는 필드를 찾아냅니다.

**2. Ranges**

복합 인덱스는 MongoDB 가 다중 절 쿼리를 더 효율적으로 실행하도록 돕습니다. 다중 필드로 인덱스를 설계할 때 완전 일치가 사용될 필드를 첫 번째에 놓고 범위가 사용될 필드를 마지막에 놓습니다.

이는 쿼리가 첫 번째 인덱스 키에 대해 정확한 값을 찾고 그 다음에 두 번째 인덱스 범위 안에서 검색하도록 해줍니다. 예를 들어 특정한 나이와 사용자명의 범위에 대해서 `{"age" : 1, "username" : 1}` 인덱스를 사용하여 쿼리한다고 가정하겠습니다.

```js
> db.users.find({"age" : 47, 
... "username" : {"$gt" : "user5", "$lt" : "user8"}}).explain()
{
    "cursor" : "BtreeCursor age_1_username_1",
    "n" : 2788,
    "nscanned" : 2788,
    ...,
    "indexBounds" : {
        "age" : [
            [
                47,
                47
            ]
        ],
        "username" : [
            [
                "user5",
                "user8"
            ]
        ]
    },
    ...
}
```

쿼리는 곧장 `{"age" : 47}` 로 건너뛰고 곧이어 `user5` 와 `user8` 사이의 사용자명 범위 내에서 검색합니다. 반대로 `{"username" : 1, "age" : 1}` 로 인덱스를 사용한다고 가정하겠습니다. 이는 쿼리가 `user5` 와 `user8` 사이의 모든 사용자를 살펴보고 `"age" : 47` 인 사용자를 뽑아내야 하기 때문에 쿼리 수행 계획을 변경합니다.

```js
> db.users.find({"age" : 47, 
... "username" : {"$gt" : "user5", "$lt" : "user8"}}).explain()
{
    "cursor" : "BtreeCursor username_1_age_1",
    "n" : 2788,
    "nscanned" : 319499,
    ...,
    "indexBounds" : {
        "username" : [
            [
                "user5",
                "user8"
            ]
        ],
        "age" : [
            [
                47,
                47
            ]
        ]
    },
    "server" : "spock:27017"
}
```

**3. OR queries**

MongoDB 는 쿼리당 오직 하나의 인덱스를 사용할 수 있습니다. 예를 들어 `{"x" : 1}` 로 한 인덱스를 생성하고 `{"y" : 1}` 로 또 다른 인덱스를 생성한 다음에 `{"x" : 123, "y" : 456}` 으로 쿼리를 실행한다면 MongoDB 는 생성한 인덱스 2 개를 모두 사용하는 것이 아니라 그 중 하나만 사용합니다.

이 규칙의 유일한 예외는 `$or` 입니다. `$or` 은 2 개의 쿼리를 수행하고 결과를 합치기 때문에 `$or` 은 `$or` 절마다 하나의 인덱스를 사용할 수 있습니다.

```js
> db.foo.find({"$or" : [{"x" : 123}, {"y" : 456}]}).explain()
{
    "clauses" : [
        {
            "cursor" : "BtreeCursor x_1",
            "isMultiKey" : false,
            "n" : 1,
            "nscannedObjects" : 1,
            "nscanned" : 1,
            "nscannedObjectsAllPlans" : 1,
            "nscannedAllPlans" : 1,
            "scanAndOrder" : false,
            "indexOnly" : false,
            "nYields" : 0,
            "nChunkSkips" : 0,
            "millis" : 0,
            "indexBounds" : {
                "x" : [
                    [
                        123,
                        123
                    ]
                ]
            }
        },
        {
            "cursor" : "BtreeCursor y_1",
            "isMultiKey" : false,
            "n" : 1,
            "nscannedObjects" : 1,
            "nscanned" : 1,
            "nscannedObjectsAllPlans" : 1,
            "nscannedAllPlans" : 1,
            "scanAndOrder" : false,
            "indexOnly" : false,
            "nYields" : 0,
            "nChunkSkips" : 0,
            "millis" : 0,
            "indexBounds" : {
                "y" : [
                    [
                        456,
                        456
                    ]
                ]
            }
        }
    ],
    "n" : 2,
    "nscannedObjects" : 2,
    "nscanned" : 2,
    "nscannedObjectsAllPlans" : 2,
    "nscannedAllPlans" : 2,
    "millis" : 0,
    "server" : "spock:27017"
}
```

로그를 보면 2 개의 분리된 쿼리의 집합입니다. 일반적으로 2 개의 쿼리를 수행하고 결과를 병합하는 것은 하나의 쿼리를 수행하는 것보다 비효율적이기 때문에 가능하면 `$or` 보다 `$in` 을 사용하는게 좋습니다.

`$or` 을 사용해야 한다면 양쪽 쿼리의 결과를 조사해서 중복을 제거해야합니다.

### Indexing Objects and Arrays

MongoDB 는 문서 내부에 도달하여 내장 필드와 배열에 인덱스를 생성하는 것을 어용합니다. 내장 객체와 배열 필드는 복합 인덱스에서 최상위 필드와 결합될 수 있습니다.

**1. Indexing embedded docs**

인덱스는 일반적인 키에 생성되는 것과 동일한 방식으로 내장된 문서 안의 키에 생성될 수 있습니다. 각 문서가 한 사용자를 나타내는 컬렉션을 가지고 있다면 각 사용자의 위치가 명시된 내장 문서를 가지게 될 것입니다.

```js
{
    "username" : "sid",
    "loc" : {
        "ip" : "1.2.3.4",
        "city" : "Springfield",
        "state" : "NY"
    }
}
```

`loc`의 하위필드 중 하나에 해당 필드를 이용하여 쿼리할 때 속도를 높이기 위해 인덱스를 만들 수 있습니다.

```js
> db.users.ensureIndex({"loc.city" : 1})
```

내장 문서 자체`("loc")` 를 인덱싱 하는것은 내장 문서의 필드 `("loc.city")` 를 인덱싱하는 것과는 매우 다르게 동작합니다. 전체 하위문서를 인덱싱하는 것은 쿼리가 전체 하위문서에 대한 도울것입니다.

**2. Indexing arrays**

배열데오 인덱스를 생성할 수 있습니다.

각 문서가 하나의 게시물인 블로그 게시물 컬렉션이 있다고 가정하겠습니다. 각 게시물은 `comments` 필드를 가지는데 이는 의견 하위문서들로 구성된 배열입니다. 가장 최근에 의견이 달린 게시물을 찾을 수 있도록 블로그 게시물 컬렉션에 내장된 `comments` 문서의 배열에 들어있는 `date` 키에 인덱스를 생성할 수 있습니다.

```js
> db.blog.ensureIndex({"comments.date" : 1})
```

부수적으로 배열의 특정 항목에 대해 인덱스를 생성할 수 있습니다.

```js
> db.blog.ensureIndex({"comments.10.votes" : 1})
```

하지만 이 인덱스는 정확히 11 번째 배열 요소에 대한 쿼리에만 유용합니다.

인덱스 항목에 들어 있는 단 하나의 필드만 배열이 될 수 있습니다. 이는 야러 다중키 인덱스에 의해 생기는 인덱스 항목 수가 폭발적으로 늘어나는 것을 피하기 위함입니다. 모든 가능한 요소 쌍들이 인덱싱되기 때문에 문서마다 n*m 개의 인덱스 항목이 생깁니다.

예를 들어 `{"x" : 1, "y" : 1}` 로 인덱스가 만들어졌다고 가정하겠습니다.

```js
> // x is an array - legal
> db.multi.insert({"x" : [1, 2, 3], "y" : 1})
>
> // y is an array - still legal
> db.multi.insert({"x" : 1, "y" : [4, 5, 6]})
>
> // x and y are arrays - illegal!
> db.multi.insert({"x" : [1, 2, 3], "y" : [4, 5, 6]})
cannot index parallel arrays [y] [x]
```

마지막 예제에서 MongoDB 인덱싱을 했는데, `{"x" : 1, "y" : 4}, {"x" : 1, "y" : 5}, {"x" : 1, "y" : 6}, {"x" : 2, "y" : 4}, {"x" : 2, "y" : 5}, {"x" : 2, "y" : 6}, {"x" : 3, "y" : 4}, {"x" : 3, "y" : 5}, and {"x" : 3, "y" : 6}` 에 대한 인덱스 항목을 생성해야만 했습니다.

**3. Multikey index implications**

어떤 문서가 인덱스 키로 배열 필드를 가진다면 인덱스는 즉시 다중키 인덱스로 표시됩니다. `explain()` 의 출력에 다중키 인덱스 여부를 확인할 수 있으며, 다중키 인덱스가 사용되었다면 `isMultiKey` 필드는 `true` 가 됩니다. 일단 인덱스가 다중키로 표시되면 필드 안에 배열을 포함하는 모든 문서가 제거되더라도 비-다중키가 될 수 없습니다. 비-다중키를 위한 유일한 방법은 삭제하고 다시 생성하는 것입니다.

다중키 인덱스는 다중키가 아닌 인덱스보다 약간 느릴 수 있습니다. 다수의 인덱스 항목은 하나의 문서를 가리킬 수 있으므로 MongoDB 는 결과를 반환하기 전에 중복을 제거해야합니다.

### Index Cardinality

**Cardinality** 는 컬렉션의 한 필드에 고윳값이 얼마나 많은가를 나타냅니다. `"gender"` 나 `"newsletter opt-out"` 과 같은 일부 필드는 오직 2 가지의 가능한 값을 가지는데 이는 매우 낮은 카디널리티로 간주됩니다. `"username"` 이나 `"email"` 같은 것들을 컬렉션의 모든 문서마다 유일한 값을 가지며 이는 높은 카디널리티입니다. `"age"` 나 `"zip-code"` 와 같은 다른것들은 여전히 중간에 해당됩니다.

일반적으로 필드의 카디널리티가 높을수록 그 필드에 대한 인덱스는 도움이 됩니다. 이는 인덱스가 검색 범위를 훨씬 작은 결과 셋으로 빠르게 좁힐 수 있기 때문입니다. 

예를 들어, `gender` 에 인덱스가 있고 Susan 이라는 여성을 찾는다 가정하겠습니다. `name` 을 찾기 위해 개별 문서를 참조하기 전에 50 % 로 결과를 좁힐 수 있습니다. 반대로 `name` 에 인덱스가 있다면 결과 셋을 `Susan` 이라는 이름을 가진 사용자의 작은 부분으로 즉시 좁히고 성별을 학윈하기 위해 그 문서들을 참조할 수 있습니다.

## Using explain() and hint()

위에서 본 바와 같이 `explain()` 은 쿼리에 대한 많은 정보를 제공합니다.  쿼리의 설명을 살펴보면 어떤 인덱스가 어떻게 사용되는지 알 수 있습니다.

가장 흔히 볼 수 있는 2 가지 유형의 `explain()` 출력이 있는데, 이는 인덱스를 사용하는 쿼리와 인덱스를 사용하지 않는 쿼리입니다.

인덱스를 사용하는 쿼리에 대한 `explain()` 출력은 다양하지만, 가장 간단한 경우는 아래와 같습니다.

```js
> db.users.find({"age" : 42}).explain()
{
    "cursor" : "BtreeCursor age_1_username_1",
    "isMultiKey" : false,
    "n" : 8332,
    "nscannedObjects" : 8332,
    "nscanned" : 8332,
    "nscannedObjectsAllPlans" : 8332,
    "nscannedAllPlans" : 8332,
    "scanAndOrder" : false,
    "indexOnly" : false,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "millis" : 91,
    "indexBounds" : {
        "age" : [
            [
                42,
                42
            ]
        ],
        "username" : [
            [
                {
                    "$minElement" : 1
                },
                {
                    "$maxElement" : 1
                }
            ]
        ]
    },
    "server" : "ubuntu:27017"
}
```

이 출력은 사용된 인덱스를 첫 번째로 알려주며 그 값은 `age_1_username_1` 입니다. 아래는 각 필드에대한 설명입니다.

* `"cursor" : "BtreeCursor age_1_username_1"`
  * BtreeCursor 는 인덱스가 사용됨을 의미하며, 구체적으로는 age 와 username 에 대한 인덱스인 `{"age" : 1, "username" : 1}` 이 사용되었습니다. 다중키 인덱스를 사용한다면 `reverse` 나 `multi` 도 볼 수 있습니다.
* `"isMultiKey" : false`
  * 다중키 인덱스를 사용했는지에 대한 여부
* `"n" : 8332`
  * 쿼리에 의해 반환된 문서 수
* `"nscannedObjects" : 8332`
  * MongoDB 가 디스크에 있는 실제 문서를 가리키는 인덱스 포인터를 따라갔던 횟수.
  * 쿼리가 인덱스의 일부가 아닌 검색 조건을 포함하거나 인덱스에 포함되지 않은 필드를 반환하도록 요청한다면 MongoDB 는 각 인덱스 항목이 가리키는 문서를 살펴봐야합니다.
* `"nscanned" : 8332
  * 인덱스가 사용되었다면 살펴본 인덱스 항목 수.
  * 테이블 스캔이었다면 조사한 문서 수
* `"scanAndOrder" : false`
  * 메모리에서 결과를 정렬했는지 여부
* `"indexOnly" : false`
  * MongoDB 가 오직 인덱스 항목을 사용하여 이 쿼리를 수행할 수 있었는지에 대한 여부
* `"nYields" : 0`
  * 쓰기 요청을 처리하도록 이 쿼리가 양보한 횟수
  * 처리해야하는 대기 중인 쓰기가 있다면 쿼리는 일시적으로 락을 해제하고 쓰기가 처리되도록 합니
* `"millis" : 91`
  * 데이터베이스가 쿼리를 수행하는 데 걸린 밀리세컨드 단위의 시간
* `"indexBounds" : {...}`
  * 인덱스가 사용된 방법을 설명하며 탐색된 인덱스의 범위를 제공한다.
  * 쿼리의 첫 번째 절은 완전 일치이기 때문에 인덱스는 42 값만 찾기만 하면 됩니다. 두 번째 인덱스 키는 자유 변수입니다.
  
`{"username" : 1, "age" : 1}` 과 `{"age" : 1, "username" : 1}` 로 생성된 인덱스가 있다고 가정해보겠습니다. 결과를 알아보겠습니다.

```js
> db.users.find({"age" : 42}).explain()
{
    "cursor" : "BtreeCursor age_1_username_1",
    "isMultiKey" : false,
    "n" : 8332,
    "nscannedObjects" : 8332,
    "nscanned" : 8332,
    "nscannedObjectsAllPlans" : 8332,
    "nscannedAllPlans" : 8332,
    "scanAndOrder" : false,
    "indexOnly" : false,
    "nYields" : 0,
    "nChunkSkips" : 0,
    "millis" : 91,
    "indexBounds" : {
        "age" : [
            [
                42,
                42
            ]
        ],
        "username" : [
            [
                {
                    "$minElement" : 1
                },
                {
                    "$maxElement" : 1
                }
            ]
        ]
    },
    "server" : "ubuntu:27017"
}
```

`"username"` 에 완전 일치 쿼리와 `age` 에 범위 값 쿼리를 수행하기 때문에 데이터베이스는 쿼리를 반전하는 조건으로 `{"username" : 1, "age" : 1}` 인덱스를 사용하도록 선택합니다. 반대로 정확한 나이와 이름의 범위로 쿼리를 수행한다면 MongoDB 는 다른 인덱스를 사용할 것입니다.

```js
> db.c.find({"age" : 14, "username" : /.*/}).explain()
{
    "cursor" : "BtreeCursor age_1_username_1 multi",
    "indexBounds" : [
        [
            {
                "age" : 14,
                "username" : ""
            },
            {
                "age" : 14,
                "username" : {

                }
            }
        ],
        [
            {
                "age" : 14,
                "username" : /.*/
            },
            {
                "age" : 14,
                "username" : /.*/
            }
        ]
    ],
    "nscanned" : 2,
    "nscannedObjects" : 2,
    "n" : 2,
    "millis" : 2
}
```

쿼리를 수행하는데 사용되기 원했던 인덱스와 다른 인덱스를 MongoDB 가 사용한다는 사실을 안다면 `hint()` 를 이용하여 특정 인덱스를 사용하도록 강제할 수 있습니다.

아래와 같이 사용하면 됩니다.

```js
> db.c.find({"age" : 14, "username" : /.*/}).hint({"username" : 1, "age" : 1})
```

### The Query Optimizer

MongoDB 의 쿼리 옵티마이저는 다른 데이터베이스의 옵티마이저와는 다르게 작동합니다. 인덱스가 정확하게 쿼리와 일치한다면, 쿼리 옵티마이저는 그 인덱스를 사용할것입니다.

그렇지 않으면 쿼리에 대해 잘 작동할 수 있는 몇 가지 인덱스가 있을것입니다. MongoDB 는 적당한 인덱스의 부분집합을 선택하여 각 계획을 가지고 쿼리를 병렬로 한 번 실행합니다. 100 개의 결과를 반환하는 첫 번째 계획이 승자고 다른 계획들은 중지됩니다.

`explain()` 결과의 `"allPlans"` 필드는 쿼리가 수행하려고 했던 각 계획을 보여줍니다.

## When Not to Index

인덱스는 데이터의 작은 일부분을 조회하는 경우에 가장 효율적입니다. 어떤 종류의 쿼리는 인덱스가 없는 게 더 빠릅니다. 컬렉션의 더 많은 부분을 가져와야할 때 인덱스는 더 비효율적인데, 하나의 인덱스를 사용하는 것은 2 번의 검색을 요구하기 때문입니다.

인덱스가 도임되거나 방해가 될 때에 엄밀한 공식은 없습니다. 인덱스가 실제 데이터 크기, 인덱스 크기, 문서 크기, 결과 셋의 평균 크기 등에 따라 달라지기 떄문입니다.

|Indexes often work well for|Table scans often worl well for|
|:--|:--|
|Large collections|Small collections|
|Large documents|Small documents|
|Selective queries|Non-selective queries|

컬렉션 통계를 분석하는 시스템이 있다고 가정해보겠습니다. 어플리케이션은 시작하기 한 시간 전부터 모든 데이터의 그래프를 생성하기 위해 시스템에 주어진 계정의 모든 문서에 대해 쿼리합니다.

```js
> db.entries.find({"created_at" : {"$lt" : hourAgo}})
```

이 쿼리의 속도를 향상시키기 위해 `created_at` 인덱스를 생성합니다. 처음에는 효율적이지만 데이터가 쌓일 수록 쿼리의 속도가 느려질겁니다. 

리포팅 시스템을 위해 데이터를 내보내거나 일괄작업을 위해 사용하는 것처럼 대부분의 데이터나 모든 데이터를 필요로 하는 것이 적합한 경우가 있습니다. 이런 경우엔 가능한 한 빨리 데이터 셋의 많은 부분을 반환하고자 할것입니다.

`{"$natural" : 1}` 힌트로 테이블 스캔을 하도록 강제할 수 있습니다. `$natural` 을 정렬에 사용하면 디스크에 기록되어 있는 순서를 지정합니다.

```js
> db.entries.find({"created_at" : {"$lt" : hourAgo}}).hint({"$natural" : 1})
```

`"$natural"` 에 의한 정렬의 부작용은 디스크에 기록되어 있는 순서대로 결과가 제공되는것입니다. 일반적으로 분주하게 움직이는 컬렉션에는 의미가 없지만 입력전용 작업에서는 최신 문서를 제공하는 데 유용합니다.

## Types of Indexes

인덱스를 구축할 때 동작 방식을 바꾸도록 지정할 수 있는 몇 가지의 인덱스 옵션이 있습니다.

### Unique Indexes

**고유 인덱스(Unique Index)** 는 각 값이 인덱스에 많아야 한번 나토록 보장합니다. 예를 들어 두 문서에서 `"username"` 키에 동일한 값을 가질 수 없게 하려면 고유 인덱스를 만들면 됩니다.

```js
> db.users.ensureIndex({"username" : 1}, {"unique" : true})
```

위 컬렉션에 다음의 문서들을 삽입한다 가정하겠습니다.

```js
> db.users.insert({username: "bob"})
> db.users.insert({username: "bob"})
E11000 duplicate key error index: test.users.$username_1  dup key: { : "bob" }
```

컬렉션을 확인해보면 첫 번째 `"bob"` 만 저장되었음을 알 수 있습니다. 

이미 익숙한 고유 인덱스가 `"_id"` 인데 이는 언제든지 컬렉션을 생성하면 자동으로 생성됩니다. 이는 일반적인 고유 인덱스입니다.

**1. Compound unique indexes**

**복합 고유 인덱스(Compound Unique Index)** 는 개별 키는 같은 값을 가질 수 있지만, 인덱스 항목이 모든 키에 걸친 값의 조합은 인덱스에 많아야 한 번 나타납니다.

예를 들어 `{"username" : 1, "age" : 1}` 로 고유 인덱스를 가졌다면 다음의 입력은 적합합니다.

```js
> db.users.insert({"username" : "bob"})
> db.users.insert({"username" : "bob", "age" : 23})
> db.users.insert({"username" : "fred", "age" : 23})
```

하지만 이 문서들 중 어떤 문서의 추가 복사본을 입력한다면 중복 키 오류가 발생합니다.

MongoDB 에 큰 파일을 저장하기 위한 표준 방식인 GridFS 는 복합 고유 인덱스를 사용합니다. 파일 내용을 가지고 있는 컬렉션은 `{"files_id" : 1, "n" : 1}` 로 고유 인덱스를 가지는데, 이는 문서를 다음처럼 보이게합니다.

```js
{"files_id" : ObjectId("4b23c3ca7525f35f94b60a2d"), "n" : 1}
{"files_id" : ObjectId("4b23c3ca7525f35f94b60a2d"), "n" : 2}
{"files_id" : ObjectId("4b23c3ca7525f35f94b60a2d"), "n" : 3}
{"files_id" : ObjectId("4b23c3ca7525f35f94b60a2d"), "n" : 4}
```

**2. Dropping duplicates**

기존 컬렉션에 고유 인덱스를 구축하려 할 때 중복된 값이 있다면 실패합니다.

```js
> db.users.ensureIndex({"age" : 1}, {"unique" : true})
E11000 duplicate key error index: test.users.$age_1  dup key: { : 12 }
```

`"dropDups"` 옵션 발견한 첫 번째 문서를 남겨 두고 중복된 값을 가지는 모든 문서를 삭제합니다.

```js
> db.people.ensureIndex({"username" : 1}, {"unique" : true, "dropDups" : true})
```

`"dropDups"` 는 고유 인덱스 구축을 강제하지만 매우 극단적인 옵션입니다. 어느 문서가 삭제되고 어느 문서가 남겨지는지에 대해 제어할 수 없습니다.

### Sparse Indexes

고유 인덱스는 `null` 을 하나의 값으로 취급하기 때문에 키가 없는 문서가 여러 개 있는 고유 인덱스를 가질 수 없습니다. 하지만 오직 키가 존재할 때에만 고유 인덱스가 적용 되도록 하는 경우가 많습니다.

**희소 인덱스(Sparse Index)** 를 만들려면 `sparse` 옵션을 포함시ㅣㅂ니다. 예를 들어 이메일 주소는 선택 항목이지만 입력된 경우에 고유해야 한다면 다음과 같이 실행합니다.

```js
> db.users.ensureIndex({"email" : 1}, {"unique" : true, "sparse" : true})
```

희소 인덱스는 반드시 고유할 필요는 없습니다. 고유하지 않은 희소 인덱스를 만들려면 `unique` 옵션만 제외시키면 됩니다.

동일한 쿼리가 희소 인덱스의 사용 여부에 따라 다른 결과를 반환할 수 있다는 것입니다. 예를 들어 대부분의 문서가 `"x"` 필드를 갖고 있지만 한 개 문서는 `"x"` 를 갖고 있지 않은 컬렉션이 있다 가정하겠습니다.

```js
> db.foo.find()
{ "_id" : 0 }
{ "_id" : 1, "x" : 1 }
{ "_id" : 2, "x" : 2 }
{ "_id" : 3, "x" : 3 }
```

`"x"` 에 쿼리를 실행하면 모든 일치하는 문서를 반환할 것입니다.

```js
> db.foo.find({"x" : {"$ne" : 2}})
{ "_id" : 0 }
{ "_id" : 1, "x" : 1 }
{ "_id" : 3, "x" : 3 }
```

`"x"` 에 희소 인덱스를 생성하면 `"_id" : 0` 문서는 인덱스에 포함되지 않습니다. 그러므로 이제 `"x"` 에 대해 쿼리하면 MongoDB 는 인덱스를 사용할 것이고 `{"_id" : 0}` 문서를 반환하지 않습니다.

```js
> db.foo.find({"x" : {"$ne" : 2}})
{ "_id" : 1, "x" : 1 }
{ "_id" : 3, "x" : 3 }
```

필드가 없는 문서가 필요한 경우 테이블 스캔을 하도록 강제하려면 `hint()` 를 사용합니다.

## Index Administration

데이터베이스의 인덱스에 대한 모든 정보는 `system.indexes` 컬렉션에 저장됩니다. 이는 예약된 컬렉션이기 때문에 그 안에 있는 문서를 수정하거나 제거할 수 있습니다. `ensureIndex` 와 `dropIndexes` 데이터베이스 명령을 통해서만 조작이 가능합니다.

인덱스를 생성할 때 `system.indexes` 에서 메타 정보를 확인할 수 있습니다. 주어진 컬렉션에 대한 모든 인덱스 정보를 확인하려면 `db.collectionName.getIndexes()` 를 하면됩니다.

```js
> db.foo.getIndexes()
[
    {
        "v" : 1,
        "key" : {
            "_id" : 1
        },
        "ns" : "test.foo",
        "name" : "_id_"
    },
    {
        "v" : 1,
        "key" : {
            "y" : 1
        },
        "ns" : "test.foo",
        "name" : "y_1"
    },
    {
        "v" : 1,
        "key" : {
            "x" : 1,
            "y" : 1
        },
        "ns" : "test.foo",
        "name" : "x_1_y_1"
    }
]
```

중요한 필드는 `"key"` 와 `"name"` 입니다. 키는 힌트, 최대, 최소, 그리고 인덱스가 명시되어야만 하는 다른 부분에 사용될 수 있습니다.

필드 순서가 중요한데 `{"x" : 1, "y" : 1}` 인 인덱스는 `{"y" : 1, "x" : 1}` 인 인덱스와 다릅니다. 인덱스명은 `dropIndex` 와 같은 다수의 관리적인 인덱스 작업에 대한 구분자로 사용됩니다.

### Identifying Indexes

컬렉션의 각 인덱스는 고유하게 인덱스를 식별하는 이름을 가지고 있으며, 서버가 인덱스를 삭제하거나 조작하는 데 사용됩니다. *key* 가 인덱스의 키고 *dirX* 는 인덱스의 방향입니다.

기본적으로 인덱스 이름은 *keyname1_dir1_keyname2_dir2_..._keynameN_dirN, where keynameX* 입니다.

`ensureIndex` 옵션 중 하나로 자신만의 이름을 지정할 수 있습니다.

```js
> db.foo.ensureIndex({"a" : 1, "b" : 1, "c" : 1, ..., "z" : 1}, 
... {"name" : "alphabet"})
```

`getLastError` 호출은 인덱스 생성 성공 여부를 보여줍니다.

### Changing Indexes

어플리케이션이 커지면서 데이터와 쿼리가 바뀌고 잘 작동하던 인덱스가 더 이상 작동하지 않는 경우 `dropIndex` 를 통해 불필요한 인덱스를 제거할 수 있습니다.

```js
> db.people.dropIndex("x_1_y_1")
{ "nIndexesWas" : 3, "ok" : 1 }
```