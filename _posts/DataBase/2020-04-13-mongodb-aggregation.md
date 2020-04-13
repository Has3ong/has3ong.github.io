---
title : MongoDB Aggregation
tags :
- MapReduce
- Pipeline
- Aggregation
- MongoDB
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## The Aggregation Framework

**집계 프레임워크(Aggregation Framework)** 를 통해 컬렉션 내 문서들을 변환하고 결합할 수 있습니다. 

기본적으로 여과, 선출, 묶음, 정렬, 제한, 건너뛰기 같은 구성 요소를 통해 문서의 흐름을 처리하는 파이프 라인을 만들 수 있습니다.

예를 들어, 잡지 기사 컬렉션에서 가장 많은 기자를 쓴 저자를 찾고자 할 수 있습니다. 각 기사가 MongoDB 의 문서로 저장되어있다고 가정하면 몇몇 단계로 이루어진 파이프 라인을 생성해서 해결할 수 있습니다.

1. 각 기사 문서의 저자들을 선출한다.
2. 이름으로 저자를 묶고 그룹 내에서 나타난 횟수를 센다.
3. 나타난 횟수를 기준으로 저자를 내림차순으로 정렬한다.
4. 처음 다섯 개로 결과를제한한다.

각 단게는 집계 프레임워크 연산자에 매핑됩니다.

1. `{"$project" : {"author" : 1}}`
   1. 각 문서의 저자 필드를 선출한다.
   2. 구문은 쿼리할 때 사용하는 필드 선택자와 비슷합니다. `fieldname : 1` 을 명시하여 필드가 선출되도록 하거나 0 을 명시하여 제외시킬 수 있습니다.
2. `{"$group" : {"_id" : "$author", "count" : {"$sum" : 1}}}`
   1. 이름으로 저자들을 묶고 저자가 나타난 각 문서에 대해 `count` 를 증가시킨다.
   2. 첫 번째는 묶고자 하는 필드인 `author` 를 명시합니다.
   3. 두 번째는 그룹 내 각 문서에 대해 `count` 필드에 1 을 더한다는 뜻입니다.
   4. 이 단계의 끝에서, 결과 내 각 문서는 `{"_id" : "authorName", "count" : articleCount}` 처럼 보입니다.
3. `{"$sort" : {"count" : -1}}`
   1. 결과 문서를 `count` 필드 기준의 내림차순으로 재정렬합니다.
4. `{"$limit" : 5}`
   1. 결과 셋을 처음 다섯 개의 결과 문서로 제한합니다.

MongoDB 에서 이를 실행하려면 `agggregate()` 함수에 각 연산을 전달합니다.

```js
> db.articles.aggregate({"$project" : {"author" : 1}},
... {"$group" : {"_id" : "$author", "count" : {"$sum" : 1}}},
... {"$sort" : {"count" : -1}},
... {"$limit" : 5})
{
    "result" : [
        {
            "_id" : "R. L. Stine",
            "count" : 430
        },
        {
            "_id" : "Edgar Wallace",
            "count" : 175
        },
        {
            "_id" : "Nora Roberts",
            "count" : 145
        },
        {
            "_id" : "Erle Stanley Gardner",
            "count" : 140
        },
        {
            "_id" : "Agatha Christie",
            "count" : 85
        }
    ],
    "ok" : 1
}
```

`aggregate()` 는 가장 많은 기사를 작성한 다섯 명의 저자를 나타내는 결과 문서들의 배열을 반환합니다.

집계 프레임워크는 컬렉션에 기록할 수 없기 때문에 모든 결과는 클라이언트로 반환되어야 합니다. 따라서 집계 결과는 16 MB 데이터로 제한됩니다.

## Pipeline Operations

각 연산은 문서의 흐름을 받아들이고 그 문서를 어떠한 형태로 변환하고, 변환 결과를 전달합니다 마지막 파이프라 연산자의 결과가 클라이언트로 반환됩니다. 그렇지 않으면 결과는 다음 연산의 입력으로 흘러 들어갑니다.

연산자는 어떤 순서로도 결합될 수 있으며 필요한 만큼 반복 가능합니다. `$match` 와 `$group` 을 수행한 후 다시 다른 조건으로 `$match` 를 수행할 수 있습니다.

### $match

`$match` 는 문서를 걸러내 주기 때문에 문서의 일부분에 집계를 실행할 수 있습니다. 예를 들어 Oregon 주에 있는 사용자 현황만 찾고자 한다면 `{$match : {"state" : "OR"}}` 과 같이 `$match` 표현식을 추가하면 됩니다. `$match` 는 모든 쿼리 연산자 `("$gt", "$lt", "$in", etc.)` 를 사용할 수 있습니다.

일반적으로 파이프라인에서 `$match` 표현식을 앞 쪽에 배치하는것이 좋습니다. 불필요한 문서를 재빨리 걸러낼 수 있으며, 선출이나 그룹으로 묶기 전에 실행하면 쿼리가 인덱스를 이용할 수 있습니다.

### $project

**선출(Projection)** 은 쿼리 언어에 있는 것보다 파이프라인에 있는 것이 훨씬 강력합니다. `$project` 를 이용하면 하위문서에서 필드를 추출하여 필드명을 바꾸고 관심 있는 연산을 수행할 수 있습니다.

`$project` 가 수행하는 가장 간단한 연산은 들어오는 문서에서 간단히 필드를 선택하는 것입니다. 필드를 포함하거나 제외시키려면 쿼리에서 사용하는 2 번째 인수와 같은 구문을 사용합니다. 다음은 원본 컬렉션에서 각 문서에 대해 `author` 필드 하나를 포함함는 결과 문서를 반환합니다.

```js
> db.articles.aggregate({"$project" : {"author" : 1, "_id" : 0}})
```

기본적으로 들어오는 문서에 `_id` 가 존재한다면 이는 항상 반환됩니다. 또한, 일반적이으로 포함 및 제외 규칙은 쿼리의 규칙과 동일한 방식으로 작동합니다. 선출된 필드명을 바꿀 수도 있습니다. 예를 들어 각 사용자의 `_id` 를 `userId` 로 반환해보겠습니다.

```js
> db.users.aggregate({"$project" : {"userId" : "$_id", "_id" : 0}})
{
    "result" : [
        {
            "userId" : ObjectId("50e4b32427b160e099ddbee7")
        },
        {
            "userId" : ObjectId("50e4b32527b160e099ddbee8")
        }
        ...
    ],
    "ok" : 1
}
```

집계 프레임워크에서 `$fieldname` 은 필드명의 값을 가리키는 데 사용됩니다. 예를 들어 `$age` 는 `age` 필드의 내용으로 대체되고, `$tags.3` 은 `tags` 배열의 네 번째 요소로 대체됩니다. 따라서 `$_id` 는 파이프라인을 통해 들어오는 각 문서의 `_id` 필드로 대체됩니다.

한 번은 `userId` 로 표시된 필드로, 또 한 번은 `_id` 로 표시된 필드로 두 번 반환하는 것을 방지하려면 `_id` 를 특별히 제외시켜야 합니다. 나중에 `$group` 에서 사용하기 위해 필드의 여러 복제본을 만드는 데 이 기법을 이용할 수 있습니다.

MongoDB 는 필드명이 바뀔 때 필드명 이력을 추적하지 않습니다. 따라서 `originalFieldname` 인덱스를 가졌다면 비록 `newFieldname` 이 `originalFieldname` 과 똑같이 보이더라도 집계는 아래 정렬에 대해 인덱스를 사용할 수 없습니다.

```js
> db.articles.aggregate({"$project" : {"newFieldname" : "$originalFieldname"}},
... {"$sort" : {"newFieldname" : 1}})
```

그렇기 때문에 필드 이름을 바꾸기 전에 인덱스를 활용하도록 합니다.

#### Pipeline expressions

가장 간단한 `$project` 표현식은 포함, 제외, 필드명을 명시하지만 더 강력한 옵션이 있씁니다. 표현식을 통해 하나의 값에 여러 문자와 변수를 결합할 수 있습니다.

복잡한 표현식을 만들기 위해 결합할 수 있고 깊이에 상관없이 중첩이 가능합니다.

**Mathematical expressions**

산술 표현식을 사용하여 숫자값을 조작할 수 있습니다. 연산하려면 일반적으로 숫자의 배열을 열거하여 표현식을 사용합니다. 예를 들어 아래 표현식은 `salary` 와 `bonus` 필드를 합계합니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...          "totalPay" : {
...              "$add" : ["$salary", "$bonus"]
...          }
...     }
... })
```

더 복잡한 표현식이 있다면 중첩할 수 있습니다. 총액에서 세금 401k 를 제외한다고 가정하겠습니다. 다음과 같이 `$subtract` 표현식을 추가할 수 있습니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...         "totalPay" : {
...              "$subtract" : [{"$add" : ["$salary", "$bonus"]}, "$401k"]
...         }
...     }
... })
```

표현식의 중첩 깊이에는 제한이 없습니다. 각 연산에 대한 구문을 살펴보겠습니다.

* `"$add" : [expr1[, expr2, ..., exprN]]`
  * 하나 혹은 여러 개의 표현식을 받아서 모두 더한다.
* `"$subtract" : [expr1, expr2]`
  * 2 개의 표현식을 받아서 첫 번째에서 두 번째를 뺍니다.
* `"$multiply" : [expr1[, expr2, ..., exprN]]`
  * 하나 혹은 여러 개의 표현식을 받아서 모두 곱한다.
* `"$divide" : [expr1, expr2]`
  * 두 개의 표현식을 받아서 첫 번째를 두 번째로 나눕니다.
* `"$mod" : [expr1, expr2]`
  * 두 개의 표현식을 받아서 첫 번째를 두 번째로 나눈 나머지 값을 반환합니다.

**Date expressions**

집계는 보다 유용한 방법으로 날짜 정보를 추출할 수 있도록 `$year`, `$month`, `$week`, `$dayOfMonth`, `$dayOfWeek`, `$dayOfYear`, `$hour`, `$minute`, `$second` 와 같은 표현식 셋을 가집니다. 숫자 형식이 아닌 날짜 형식으로 저장된 필드에만 날짜 연산을 사용할 수 있습니다.

각각의 날짜 형식은 기본적으로 동일하며, 이는 날짜 표현식을 받아들이고 숫자를 반환합니다. 다음은 각 종업원이 채용된 월을 반환합니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...         "hiredIn" : {"$month" : "$hireDate"}
...     }
... })
```

문자열 날짜를 사용할 수도 있습니다. 종업원이 회사에서 일한 연수를 계산합니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...         "tenure" : {
...             "$subtract" : [{"$year" : new Date()}, {"$year" : "$hireDate"}]
...         }
...     }
... })
```

**String expressions**

사용 가능한 몇 가지 기본적인 문자열 연산이 있습니다. 특징은 아래와 같습니다.

* `"$substr" : [expr, startOffset, numToReturn]`
  * startOffset 바이트에서 시작해 다음 numToReturn 바이트만큼 첫 번째 인수의 일부 문자열을 반환한다.
* `"$concat" : [expr1[, expr2, ..., exprN]]`
  * 주어진 각 문자열 표현식을 연결한다.
* `"$toLower" : expr`
  * 문자열을 소문자로 반환한다. 표현식은 문자열이어야 한다.
* `"$toUpper" : expr`
  * 문자열을 대문자로 반환한다. 표현식은 문자열이어야 한다.

대소문자에 영향을 미치는 연산은 알파벳 문자에 대해서만 작동합니다.

다음은 *j.doe@example.com* 형식의 이메일 주소를 생성하는 예제입니다. 첫 번째 이니셜을 추출하여 몇 가지의 상수 문자열 및 `lastName` 필드와 연결합니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...         "email" : {
...             "$concat" : [
...                 {"$substr" : ["$firstName", 0, 1]}, 
...                 ".", 
...                 "$lastName", 
...                 "@example.com"
...             ]
...         }
...     }
... })
```

**Logical expressions**

제어문을 위해 사용할 수 있는 몇 가지 연산이 있습니다.

* `"$cmp" : [expr1, expr2]`
  * 두 표현식을 비교합니다. 표현식이 같으면 0 을 반환하고 `expr1` 이 `expr2` 보다 작으면 음수를 크면 양수를 반환한다.
* `"$strcasecmp" : [string1, string2]`
  * 대소문자 구분 없이 문자열을 비교합니다. 알파벳 문자에 대해서만 작동한다.
* `"$eq"/"$ne"/"$gt"/"$gte"/"$lt"/"$lte" : [expr1, expr2]`
  * 참 또는 거짓 여부를 반환하는 표현식의 비교를 수행한다.

다음은 몇 가지 불리언 표현식 입니다.

* `"$and" : [expr1[, expr2, ..., exprN]]`
  * 모든 표현식이 참이면 참을 반환한다.
* `"$or" : [expr1[, expr2, ..., exprN]]`
  * 적어도 하나의 표현식이 참이면 참을 반환한다.
* `"$not" : expr`
  * 표현식과 반대되는 불리언 값을 반환한다.

마지막으로 두 가지 제어문이 있습니다.

* `"$cond" : [booleanExpr, trueExpr, falseExpr]`
  * 불리언 표현식이 참으로 판단되면 참이 반환되고, 그렇지 않으면 거짓 표현힉이 반환된다.
* `"$ifNull" : [expr, replacementExpr]`
  * 표현식이 null 이면 대체 표현식을 반환하고, 그렇지 않으면 표현식을 반환

파이프라인은 제대로 형태를 갖춘 입력을 받아들이는 데 민감하기 때문에 연산들은 기본값을 채우는게 중요합니다. 산술 연산자는 숫자가 아닌 값에 대해 거부하고 날짜 연산자는 날짜가 아닌 값에 대해 거부합니다. 데이터셋에 일관성이 없는 경우, 입력되지 않은 값을 감지해서 채워 넣는 데 이러한 조건문들을 사용할 수 있습니다.

#### A projection example

학생들의 성적을 출석 10%, 퀴즈 30%, 시험 60% 비중으로 매겨진다고 하겠습니다. 이때 규칙은 다음과 같이 표현할 수 있습니다.

```js
> db.students.aggregate(
... {
...     "$project" : {
...         "grade" : {
...             "$cond" : [
...                 "$teachersPet", 
...                 100, // if 
...                 {    // else
...                     "$add" : [
...                         {"$multiply" : [.1, "$attendanceAvg"]},
...                         {"$multiply" : [.3, "$quizzAvg"]}, 
...                         {"$multiply" : [.6, "$testAvg"]}
...                     ]
...                 }
...             ]
...         }
...     }
... })
```

### $group

그룹으로 묶는 것은 특정 필드로 문서를 묶고 문서의 값들을 합칠 수 있게 해줍니다.

그룹으로 묶을 하나의 필드 또는 필드들을 선택하면 그것을 `$group` 함수에 그룹의 `_id` 필드로 전달합니다. 따라서 위 예제들은 다음과 같은 표현식을 가집니다.

* `{"$group" : {"_id" : "$day"}}`
* `{"$group" : {"_id" : "$grade"}}`
* `{"$group" : {"_id" : {"state" : "$state", "city" : "$city"}}}`

현 상태에서 결과는 각 그룹에 대해 그룹으로 묶는 키 필드 하나를 갖는 단일 문서입니다. 예를 들어 성적을 매긴 결과는 `{"result" : [{"_id" : "A+"}, {"_id" : "A"}, {"_id" : "A-"}, ..., {"_id" : "F"}], "ok" : 1}` 과 같습니다.

하나의 필드에 대해 모든 고유한 값을 얻는 데는 좋지만 모든 예제가 무언가 계산하기 위해 이 그룹을 이용하는 것을 필요로 합니다. 따라서 각 그룹에 속한 문서를 기반으로 계산하기 위해 그룹을 묶는 연산자를 사용하는 필드를 추가합니다.

#### Grouping operators

묶음 연산자를 이용하여 각 그룹에 대한 결과를 계산할 수 있습니다.

**Arithmetic operators**

필드에서 숫자값을 계산할 때는 `$sum` 과 `$avg` 연산자를 사용합니다.

* `"$sum" : value`
  * 각 문서에 대해 값을 더한 다음에 결과를 반환한다.

```js
> db.sales.aggregate(
... {
...     "$group" : {
...         "_id" : "$country", 
...         "totalRevenue" : {"$sum" : "$revenue"}
...     }
... })
```

* `"$avg" : value`
  * 그룹으로 묶는 동안에 확인된 모든 입력값의 평균을 반환한다.

```js
> db.sales.aggregate(
... {
...     "$group" : {
...         "_id" : "$country", 
...         "averageRevenue" : {"$avg" : "$revenue"}, 
...         "numSales" : {"$sum" : 1}
...     }
... })
```

**Extreme operators**

데이터셋의 *edges* 를 얻기 위한 네 가지 연산자가 있습니다.

* `"$max" : expr`
  * 모든 입력값 중 가장 큰 값을 반환한다.
* `"$min" : expr`
  * 모든 입력값 중 가장 작은 값을 반환한다.
* `"$first" : expr`
  * 그룹에서 발견된 첫 번째 값을 반환한다.
* `"$last" : expr`
  * 그룹에서 발견된 마지막 값을 반환

`$max` 와 `$min` 은 각 문서를 훑어보고 극한값을 찾아냅니다. 따라서 이러한 연산들은 정렬되지 않은 데이터를 가지고 있는데 그 데이터를 정렬하는 것이 다소 낭비일 때 적합합니다.

시험 점수의 등급별로 경계가 되는 점수를 찾아보겠습니다.

```js
> db.scores.aggregate(
... {
...     "$group" : {
...         "_id" : "$grade", 
...         "lowestScore" : {"$min" : "$score"}, 
...         "highestScore" : {"$max" : "$score"}
...     }
... })
```

반면 데이터를 찾고자 하는 필드로 정렬시키면 `$first` 와 `$last` 는 유용한 결과륿 나환합니다. 예를 들어 위와 동일한 결과를 얻으려면 다음과 같이 실행합니다.

```js
> db.scores.aggregate(
... {
...     "$sort" : {"score" : 1}
... },
... {
...     "$group" : {
...         "_id" : "$grade", 
...         "lowestScore" : {"$first" : "$score"}, 
...         "highestScore" : {"$last" : "$score"}
...     }
... })
```

데이터가 정렬되었다면 후자가 전자에 비해 더 효율적입니다. 데이터가 정렬되지 않았다면 반대로 전자가 효율적입니다.

**Array operators**

배열을 조작하는데 사용할 수 있는 두 가지 연산자가 있습니다.

* `"$addToSet" : expr`
  * 지금까지 확인된 배열값을 보관하며, 배열에 표현식이 보이지 않으면 배열에 추가합니다. 각 값은 결과 배열에서 많아야 한 번 나타나며 순서는 보장되지 않는다.
* `"$push" : expr`
  * 배열에 각 값을 가리지 않고 추가합니다. 모든 값의 배열을 반환한다.

####  Grouping behavior

`$group` 은 앞서 설명했던 흐름 방식으로 처리할 수 없는 연산자 입니다.

대부분의 연산자가 지속적으로 문서를 처리할 수 있는 반면 `$group` 은 모든 문서를 모아 그룹으로 나눈 후 파이프라인의 다음 연산자로 보냅니다. 샤딩을 사용할 경우 `$group` 은 각 샤드에서 실행되고 각 개별적인 샤드의 그룹은 마지막으로 그룹을 묶기 위해 `mongos` 로 보내지며 파이프라인의 남아 있는 작업은 `mongos` 에 실행됩니다.

### $unwind

**전개(unwind)** 배열의 각 필드를 별개의 문서로 변환합니다. 예를들어 의견이 달린 블로그에서 각 의견을 독립적인 문서로 변환하는데 전개를 이용할 수 있습니다.

```js
> db.blog.findOne()
{
    "_id" : ObjectId("50eeffc4c82a5271290530be"),
    "author" : "k",
    "post" : "Hello, world!",
    "comments" : [
        {
            "author" : "mark",
            "date" : ISODate("2013-01-10T17:52:04.148Z"),
            "text" : "Nice post"
        },
        {
            "author" : "bill",
            "date" : ISODate("2013-01-10T17:52:04.148Z"),
            "text" : "I agree"
        }
    ]
}
> db.blog.aggregate({"$unwind" : "$comments"})
{
    "result" :
        {
            "_id" : ObjectId("50eeffc4c82a5271290530be"),
            "author" : "k",
            "post" : "Hello, world!",
            "comments" : {
                "author" : "mark",
                "date" : ISODate("2013-01-10T17:52:04.148Z"),
                "text" : "Nice post"
            }
        },
        {
            "_id" : ObjectId("50eeffc4c82a5271290530be"),
            "author" : "k",
            "post" : "Hello, world!",
            "comments" : {
                "author" : "bill",
                "date" : ISODate("2013-01-10T17:52:04.148Z"),
                "text" : "I agree"
            }
        }
    ],
    "ok" : 1
}
```

이는 특히 쿼리에서 특정 하위문서를 반환하고자 할 때 유용합니다. 하위문서를 `$unwind` 한 다음에 원하는 문서를 `$match` 합니다. 예를 들어 특정 사용자와 의견이 달린 게시물이 아닌 오직 사용자의 의견으로 모든 의견을 반환받는 것은 일반적인 쿼리로는 불가능합니다.

하지만 선출, 전개, 일치를 사용하면 쉽게 해결됩니다.

```js
> db.blog.aggregate({"$project" : {"comments" : "$comments"}}, 
... {"$unwind" : "$comments"}, 
... {"$match" : {"comments.author" : "Mark"}})
```

모든 의견은 여전히 `comments` 하위 문서에 있기 때문에 결과를 보다 보기 좋게 구성하려면 최종 선출을 합니다.

### $sort

존재하는 필드와 선출된 필드를 모두 정렬에 사용할 수 있습니다.

```js
> db.employees.aggregate(
... {
...     "$project" : {
...         "compensation" : {
...             "$add" : ["$salary", "$bonus"]
...         }, 
...         "name" : 1
...     }
... }, 
... {
...     "$sort" : {"compensation" : -1, "name" : 1}
... })
```

위 예제는 연봉이 높은 순에서 낮은 순으로 정렬한 다음에 이름을 A 에서 Z 로 정렬합니다. 

1 은 오름차순이고 -1 은 내림차순입니다.

`$sort` 는 앞서 보았던 `$group` 과 같은 또 다른 장애물 연산자입니다. 샤딩을 사용하는 경우, `$sort` 가 올바르게 정렬하려면 모든 문서를 수집하고 추가적인 처리를 위해 각 샤드의 정렬된 결과를 `mongos` 로 보내야 합니다.

### $limit

`$limit` 는 숫자 `n` 을 받고 처음 `n` 개의 결과 문서를 반환합니다.

### $skip

`$skip` 은 숫자 `n` 을 받고 처음 `n` 개의 문서를 결과 셋에서 제거합니다. `$skip` 은 뛰어넘고 제거해야할 모든 일치를 찾아내야 하기 때문에 일반적인 쿼리에서와 같이 대량의 뛰어넘기는 

### Using Pipelines

`$project`, `$group`, `$unwind` 연산을 수행하기 전에 파이프라인의 도입부에서 가능한 한 많은 문서를 걸러냅니다. 일단 파이프라인이 직접 콜렉션에서 데이터를 사용하지 않는다면 인덱스는 여과나 정렬에 더 이상 도움을 줄 수 없습니다.

가능하다면 인덱스 사용이 가능하도록 집계 파이프라인은 연산 재정렬을 시도합니다.

## MapReduce

맵리듀스는 데이터를 집계하는 강력하고 유용한 도구입니다. 집계 프레임워크의 쿼리 언어를 사용해서 표현하기에는 너무 복잡한 여러 문제를 해결할 수 있습니다.

맵리듀스는 다수의 서버에 걸쳐서 쉽게 병렬화할 수 있습니다. 문제를 분할하고 각 청크를 다른 서버로 보내고 각 서버가 해당 부분을 처리하도록 합니다. 모든 서버의 작업이 끝나면 작업 결과를 모아 하나의 완전한 결과를 만듭니다.

맵리듀스는 몇 단계에 걸쳐 수행됩니다. 맵 단계부터 시작하는데, 이는 컬렉션의 모든 문서에 대해 연산 매핑을 수행합니다. 그 다음에는 Key 들을 묶고 각 Key 별로 출력한 값들의 목록을 생성하는 **셔플(Shuffle)** 이라는 중간 단계가 있습니다.

**리듀스(Reduce)는** 이 목록을 받아 하나의 요소로 줄입니다. 이 요소는 각 Key 가 하나의 Value, 즉 결과를 가질 때까지 다시 셔플 단계로 전달합니다.

### Example 1: Finding All Keys in a Collection

MongoDB 는 스키마가 가변적이라 가정하기 때문에 각 문서의 키를 따지지 않습니다. 일반적으로 컬렉션 내의 모든 문서에 걸쳐 Key 를 찾는 가장 좋은 방법은 맵리듀스를 사용하는것입니다. 예제에서는 컬렉션에 각각의 Key 가 몇 번이나 나타내는지 세어보겠습니다.

매핑 단계에서 컬렉션 내 모든 문서의 Key 를 얻고자 합니다. `map` 함수는 나중에 처리할 값을 반환하기 위해 `emit` 이라는 특별한 함수를 사용합니다. `emit` 함수는 맵리듀스에 Key 와 같은 Value 를 제공합니다.

여기서는 문서에서 Key 가 몇 번이나 나오는지 출력합니다. 각 Key 에 대해 별도로 세어보려 하기 때문에 문서의 모든 Key 마다 `emit` 을 호출할 것입니다. `this` 는 현재 매핑하고 있는 문서에 대한 참조입니다.

```js
> map = function() {
... for (var key in this) {
...     emit(key, {count : 1});
... }};
```

이제 컬렉션 내 Key 와 연결된 수많은 `{count : 1}` 문서를 만들었습니다. 하나 이상의 `{count : 1}` 문서를 가진 배열들은 `reduce` 함수로 전달됩니다. `reduce` 함수에는 `emit` 함수의 첫 번째 인자인 `key` 와 해당 Key 로 출력된 하나 이상의 `{count : 1}` 문서로 구성된 배열, 두 인자가 전달됩니다.

```js
> reduce = function(key, emits) {
... total = 0;
... for (var i in emits) {
...     total += emits[i].count;
... }
... return {"count" : total};
... }
```

`reduce` 는 맵 단계나 이전 리듀스 단계의 결과를 반복적으로 호출할 수 있어야 합니다. 그러므로 `reduce` 는 `reduce` 의 두 번째 인자로 `reduce` 를 다시 보낼 수 있는 문서를 반환해야 합니다. 예를 들어 `x` Key 가 3 개의 문서 `{count : 1, id : 1}`, `{count : 1, id : 2}`, `{count : 1, id : 3}` 에 매핑되엇다고 하겠습니다.

MongoDB 는 다음과 같은 형태로 `reduce` 를 호출합니다.

```js
> r1 = reduce("x", [{count : 1, id : 1}, {count : 1, id : 2}])
{count : 2}
> r2 = reduce("x", [{count : 1, id : 3}])
{count : 1}
> reduce("x", [r1, r2])
{count : 3}
```

두 번째 인자가 항상 초기 문서 중 하나를 가지고 잇거나 특정 크기라고 가정할 수 없습니다. `reduce` 는 어떤 조합의 `emit` 문서나 `reduce` 결과값을 가지고도 작동할 수 있어야 합니다.

종합해 보면 이 맵리듀스 함수는 다음과 같습니다.

```js
> mr = db.runCommand({"mapreduce" : "foo", "map" : map, "reduce" : reduce})
{
    "result" : "tmp.mr.mapreduce_1266787811_1",
    "timeMillis" : 12,
    "counts" : {
        "input" : 6
        "emit" : 14
        "output" : 5
    },
    "ok" : true
}
```

맵리듀스 문서는 연산에 대한 메타 정보 묶음을 반환합니다.

* `"result" : "tmp.mr.mapreduce_1266787811_1"`
  * 맵리듀스 결과가 저장된 컬렉션의 이름
  * 임시 컬렉션이며 맵리듀스를 수행하는 연결이 닫히면 삭제된다
* `"timeMillis" : 12`
  * 연산이 수행된 시간
  * 1 / 1000 초 단위
* `"counts" : { ... }`
  * 이 내장 문서는 디버깅하는 데 사용되며 3 개의 Key 를 가지고 있다.
    * `"input" : 6`
      * `map` 함수로 보내진 문서 수
    * `"emit" : 14`
      * `map` 함수로 호출된 `emit` 수
    * `"output" : 5`
      * 결과 컬렉션에 생성된 문서 수

컬렉션에서 `find` 함수를 실행하면 원본 컬렉션의 모든 Key 와 사용 횟수를 볼 수 있습니다.

```js
> db[mr.result].find()
{ "_id" : "_id", "value" : { "count" : 6 } }
{ "_id" : "a", "value" : { "count" : 4 } }
{ "_id" : "b", "value" : { "count" : 2 } }
{ "_id" : "x", "value" : { "count" : 1 } }
{ "_id" : "y", "value" : { "count" : 1 } }
```

각 Key 값은 `_id` 가 되며 리듀스 단계의 최종 결과는 `value` 입니다.

### Example 2: Categorizing Web Pages

사용자들이 페이크 링크를 올려서 *politics*, *geek* 같은 특정한 주제와 연관된 태크를 달 수 있는 사이트가 있다고 가정하겠습니다. 맵리듀스를 사용하여 최신이면서 가장 많이 추천받은 조합을 이용해 어떤 주제가 인기 있는지 알아낼 수 있습니다.

태그와 문서의 인기도와 최신성에 기반한 값을 출력하는 `map` 함수가 필요합니다.

```js
map = function() {
    for (var i in this.tags) {
        var recency = 1/(new Date() - this.date);
        var score = recency * this.score;

        emit(this.tags[i], {"urls" : [this.url], "score" : score});
    }
};
```

이제 태그에 대해 출력된 모든 갑승ㄹ 해당 태그에 대한 하나의 점수로 리듀스합니다.

```js
reduce = function(key, emits) {
    var total = {urls : [], score : 0}
    for (var i in emits) {
        emits[i].urls.forEach(function(url) {
            total.urls.push(url);
        }
        total.score += emits[i].score;
    }
    return total;
};
```

최종 컬렉션은 각 태그에 대한 전체 URL 목록과 해당 태그의 유명한 정도를 보여주는 점수로 나오게 됩니다.

### MongoDB and MapReduce

위 예제에서는 `mapreduce`, `map`, `reduce` 를 사용했습니다. 이3 가지 Key 외에도 다양한 추가적인 Key 를 맵리듀스 명령어로 전달할 수 있습니다.

* `"finalize" : function`
  * `reduce` 의 결과를 전달하는 마지막 단계
* `"keeptemp" : boolean`
  * 연결을 종료한 후에도 임시 결과 컬렉션을 저장해야 할 때 사용
* `"out" : string`
  * 결과 컬렉션에 대한 이름. 이 옵션을 사용할 때는 `keeptemp : true` 로 인식
* `"query" : document`
  * `map` 함수에 보내기 전에 문서를 걸러내는 쿼리
* `"sort" : document`
  * `map` 함수로 보내기 전에 문서를 정렬하기 위해 사용
* `"limit" : integer`
  * `map` 함수로 전달하는 문서의 최대 수
* `"scope" : document`
  * 자바스크립트 코드에서 사용할 수 있는 변수
* `"verbose" : boolean`
  * 상세한 서버 로그 출력 여부

#### 1. The finalize function

이전의 `group` 명령과 마찬가지로 맵리듀스도 마지막 출력을 임시 컬렉션에 저장하기 전에 마지막 `reduce` 의 결과에 대해 실행될 `finalize` 함수를 전달할 수 있습니다.

맵리듀스는 전체 결과의 크기를 4 MB 에 맞출 필요가 없기 때문에 대량의 결과 셋을 반환할 때가 `group` 명령을 사용할 때보다 덜 치명적입니다. 하지만 네트워크를 통해 전송되기 전에 `finalize` 를 일반적으로 평균을 구하고, 배열을 줄이고, 부가 정보를 삭제하는 데 쓸 수 있습니다.

#### 2. Keeping output collections

기본적으로 MongoDB 는 맵리듀스를 처리하면서 잘 쓰이지 않을 이름으로 임시 컬렉션을 생성합니다. 이 이름은 `mr`, 맵리듀스를 하는 컬렉션의 이름, 타임스탬프, 데이터베이스의 작업 ID 를 점으로 구분한 문자열로 이루어져 있습니다. 예를 들어 `mr.stuff.18234210220.2` 와 같이 명명됩니다. MongoDB 는 맵리듀스를 수행한 연결이 종료될 때 자동으로 이 컬렉션을 삭제합니다. 연결을 종료한 후에도 컬렉션을 유지하고 싶다면 `keeptemp : true` 로 지정하면 됩니다.

맵리듀스가 생성한 결과 컬렉션은 일반 컬렉션입니다. 즉, 여기에 다시 맵리듀스를 수행하거나, 맵리듀스를 무한히 수행해도 문제가 없습니다.

#### 3. MapReduce on a subset of documents

때로는 컬렉션의 일부만 맵리듀스할 필요가 있습니다. 이때 `map` 함수로 넘기기 전에 문서를 걸래내는 쿼리를 추가할 수 있습니다.

`map` 함수로 넘겨진 모든 문서는 BSON 에서 자바스크립트 객체로 역직렬화해야 하는데 이는 무거운 작업입니다. 컬렉션 내 문서 중 일부분만 맵리듀스해야 한다면 필터를 추가해 속도를 높일 수 있습니다. `query`, `limit`, `sort` 키로 필터를 지정할 수 있습니다.

`uery` 키는 쿼리 문서를 값으로 받습니다. 그 쿼리가 정상적으로 반환하는 모든 문서는 `map` 함수로 전달됩니다. 예를 들어 웹 지표를 기록하는 어플리케이션이 지난 주 상황을 요약하고 싶다면 다음 명령으로 가장 최근 주의 문서에만 맵리듀스를 사용할 수 있습니다.`

```js
> db.runCommand({"mapreduce" : "analytics", "map" : map, "reduce" : reduce, 
                 "query" : {"date" : {"$gt" : week_ago}}})
```

`sort` 옵션은 `limit` 과 함께 사용하면 유용합니다. `limit` 은 `map` 함수로 보내는 문서 수를 제한하며, 혼자서 사용될 수 있습니다.

위 예에서 최근 10,000 페이지 뷰의 분석을 원한다면 `limit` 와 `sort` 를 사용할 수 있습니다.

```js
> db.runCommand({"mapreduce" : "analytics", "map" : map, "reduce" : reduce, 
                 "limit" : 10000, "sort" : {"date" : -1}})
```

`query`, `limit`, `sort` 함수는 어떤 조합으로도 사용될 수 있지만, `sort` 는 `limit` 가 없다면 유용하지 않습니다.

#### 4. Using a scope

맵리듀스는 `map`, `reduce`, `finalize` 함수에 대한 코드 유형을 받을 수 있고 대부분의 언어에서 코드로 유효 범위를 전달할 수 있습니다. 하지만 맵리듀스는 이 유효 범위를 무시합니다. 맵리듀스는 `scope` 라는 자체 유효 범위 키를 가지며 맵리듀스에서 클라이언트 쪽의 유혀범위를 사용하고 싶다면 이 키를 지정해야 합니다. 이 값은 `variable : value` 형태로 지정할 수 있으며, `map`, `reduce`, `finalize` 함수에서 사용할 수 있습니다. 이 함수 내에서는 유효 범위가 변하지 않습니다.

예를 들어 `1/(new Date() - this.date)` 를 이용해 페이지의 최신성을 계산했습니다. 대신 다음 코드로 오늘 날자를 유효 범위 일부분으로 전달할 수 있습니다.

```js
> db.runCommand({"mapreduce" : "webpages", "map" : map, "reduce" : reduce, 
                 "scope" : {now : new Date()}})
```

그러면 `map` 함수에서 `1/(now - this.date)` 를 쓸 수 있습니다.

#### 5. Getting more output

맵리듀스의 진행 상황을 확인하고 싶다면 `"verbose" : true` 로 지정하면 됩니다.

`print` 를 통해 `map`, `reduce`, `finalize` 함수에서 일어나는 일을 확인할 수 있습니다. `print` 는 서버 로그에 내용을 출력합니다.

## Aggregation Commands

컬렉션에 대한 기본적인 집계 작업을 하기 위한 MongoDB 의 명령어가 있습니다.

### count

`count` 가장 간단한 집계 도구며, 컬렉션 내의 문서 수를 봔한합니다.

```js
> db.foo.count()
0
> db.foo.insert({"x" : 1})
> db.foo.count()
1
```

컬렉션 내 전체 문서 수를 세는 것은 컬렉션의 크기와 상관없이 빠릅니다. 쿼리를 전달할 수도 있으며 MongoDB 는 해당 쿼리의 결과 수를 카운트합니다.

```js
> db.foo.insert({"x" : 2})
> db.foo.count()
2
> db.foo.count({"x" : 1})
1
```

### distinct

`distinct` 는 주어진 Key 에 대한 모든 고유값을 찾습니다. 아래와 같이 컬렉션과 Key 를 지정해야 합니다.

```js
> db.runCommand({"distinct" : "people", "key" : "age"})
```

예를 들어 컬렉션에 다음과 같은 문서가 있을때

```json
{"name" : "Ada", "age" : 20}
{"name" : "Fred", "age" : 35}
{"name" : "Susan", "age" : 60}
{"name" : "Andy", "age" : 35}
```

`age` 로 `distinct` 를 호출하면 아래와 같은 결과를 반환합니다.

```js
> db.runCommand({"distinct" : "people", "key" : "age"})
{"values" : [20, 35, 60], "ok" : 1}
```

### group

`group` 은 복잡한 집계 연산을 제공합니다. 그룹으로 묶을 Key 를 선택하면 MongoDB 는 선택한 Key 읙 ㅏㅂㅅ으로 컬렉션을 각 그룹으로 나눕니다. 각 그룹에 속한 문서들을 집계해서 그룹별로 결과 문서를 생성할 수 있습니다.

주가를 기록한 데이터에서 30 일 동안의 종가를 찾을 때 `group` 으로 쉽게 처리할 수 있습니다.

주가 데이터는 아래와 같은 형식입니다.

```json
{"day" : "2010/10/03", "time" : "10/3/2010 03:57:01 GMT-400", "price" : 4.23}
{"day" : "2010/10/04", "time" : "10/4/2010 11:28:39 GMT-400", "price" : 4.27}
{"day" : "2010/10/03", "time" : "10/3/2010 05:00:23 GMT-400", "price" : 4.10}
{"day" : "2010/10/06", "time" : "10/6/2010 05:27:58 GMT-400", "price" : 4.30}
{"day" : "2010/10/04", "time" : "10/4/2010 08:34:50 GMT-400", "price" : 4.01}
```

아래와 같이 하루 중 마지막 시간과 가격의 목록을 보고자 합니다.

```json
[
    {"time" : "10/3/2010 05:00:23 GMT-400", "price" : 4.10},
    {"time" : "10/4/2010 11:28:39 GMT-400", "price" : 4.27},
    {"time" : "10/6/2010 05:27:58 GMT-400", "price" : 4.30}
]
```

컬렉션 내 문서들을 `day` 로 묶은 후 날짜별로 마지막 타임스탬프의 문서를 찾아 결과셋에 추가하면 됩니다. 전체 함수는 다음과 같이 구성할 수 있습니다.

```js
> db.runCommand({"group" : {
... "ns" : "stocks",
... "key" : "day",
... "initial" : {"time" : 0},
... "$reduce" : function(doc, prev) {
...     if (doc.time > prev.time) {
...         prev.price = doc.price;
...         prev.time = doc.time;
...     }
... }}})
```

명령을 구성 Key 별로 분해하여 살펴보겠습니다.

* `"ns" : "stocks"`
  * 어떤 컬렉션에서 `group` 을 수행할 지 결정
* `"key" : "day"`
  * 컬렉션 내에서 문서를 묶을 Key 를 지정한다. 예제에서는 `day` 가 지정된다.
* `"initial" : {"time" : 0}`
  * 주어진 그룹에 대해 처음으로 `reduce` 함수가 호출되면 이를 초기화 문서로 넘긴다. 주어진 그룹의 멤버는 같은 누산기를 사용하기 때문에 적용된 변경은 계속 유지된다.
* `"$reduce" : function(doc, prev) { ... }`
  * 컬렉션 내의 각 문서에 대해 한 번씩 호출된다. 현재 문서와 해당 그룹에 대한 지금까지의 결괏값인 누산기 문서를 받는다. 예제에서는 리듀스 함수에서 현재 문서의 시간과 누산기 문서의 시간을 비교한다. 만약 현재 문서가 더 나중 시간의 것이라면 수산기 문서에 현재 문서의 시간과 주가를 설정 한다. 각 모음에 대해 별도의 누산기가 있음을 기억한다면 다른 날짜에서 같은 누산기를 사용할지 모른다는 우려할 필요 없다.

문서에서는 30 일 동안의 가격만 보기를 원했습니다. 하지만 현재의 해결법은 컬렉션 전체를 조회해야합니다. 이것이 `group` 명령어가 처리하기 위해 충족해야 하는 `condition` 을 포함할 수 있는 이유입니다.

```js
> db.runCommand({"group" : {
... "ns" : "stocks",
... "key" : "day",
... "initial" : {"time" : 0},
... "$reduce" : function(doc, prev) {
...     if (doc.time > prev.time) {
...         prev.price = doc.price;
...         prev.time = doc.time;
...     }},
... "condition" : {"day" : {"$gt" : "2010/09/30"}}
... }})
```

명령문은 30 개의 문서 배열을 반환하는데, 각각은 그룹입니다. 각 그룹은 해당 그룹이 기준으로 삼은 Key 와 마지막 `prev` 값을 가지고 있습니다. 일부 문서가 Key 를 가지고 있지 않다면 이것들을 `"day" : null` 요소로 묶습니다. `"condition"` 에 `"day" : {"$exists" : true}` 를 추가해 이 그룹을 제거할 수 있습니다. `group` 명령어는 참조에 사용한 문서의 총 수와 고유한 `key` 의 수를 반환합니다.

```js
> db.runCommand({"group" : {...}})
{
    "retval" :
        [
            {
                "day" : "2010/10/04",
                "time" : "Mon Oct 04 2010 11:28:39 GMT-0400 (EST)"
                "price" : 4.27
            },
            ...
        ],
    "count" : 734,
    "keys" : 30,
    "ok" : 1
}
```

각 그룹에 대해 `price` 는 명시적으로 지정했고, `time` 은 초기활르 통해 설정한 후 갱신한 값입니다. 그룹을 묶는 데 사용한 Key 는 각각의 `retval` 내장 문서에 기본적으로 들어가기 때문에 `day` 가 포함됩니다.

이 Key 를 반환할 필요가 없다면 종결자를 사용해 최종 누산기 문서를 특정 형태로 바꿀수도 있습니다.

#### 1. Using a finalizer

종결자는 데이터베이스에서 사용자에게 전송하는 데이터양을 최소화하는 데 사용할 수 있습니다.

이는 `group` 명령어의 결과가 단일 데이터베이스 응답에 맞아야 하기 때문에 중요합니다. 이를 확인하기 위해 태그를 가지는 블로그 게시물을 예로 들어보겠습니다.

각각의 날짜에 가장 인기가 많은 태그를 찾고 `day` 로 묶어서 태그를 셉니다.

```js
> db.posts.group({
... "key" : {"day" : true},
... "initial" : {"tags" : {}},
... "$reduce" : function(doc, prev) {
...     for (i in doc.tags) {
...         if (doc.tags[i] in prev.tags) {
...             prev.tags[doc.tags[i]]++;
...         } else {
...             prev.tags[doc.tags[i]] = 1;
...         }
...     }
... }})
```

이제 다음과 같은 결과가 반환됩니다.

```json
[
    {"day" : "2010/01/12", "tags" : {"nosql" : 4, "winter" : 10, "sledding" : 2}},
    {"day" : "2010/01/13", "tags" : {"soda" : 5, "php" : 2}},
    {"day" : "2010/01/14", "tags" : {"python" : 6, "winter" : 4, "nosql": 15}}
]
```

그 다음 클라이언트 측 `tags` 문서에서 가장 큰 값을 찾습니다.

하지만 하나의 문자열이 필요한 상황에 각 날짜별로 전체 태그의 Key / Value 쌍을 모두 클라이언트로 전송하면 부담이 크게 발생합니다. 이때문에 `group` 명령에서 `finalize` Key 를 받는 이유입니다. `finalize` 는 각 모음별로 클라이언트에 결과를 반환하기 직전에 단 한번 수행하는 함수를 포함할 수 있습니다.

`finalize` 함수를 사용해 결과에서 원치 않은 정보를 모두 제거할 수 있습니다.

```js
> db.runCommand({"group" : {
... "ns" : "posts",
... "key" : {"day" : true},
... "initial" : {"tags" : {}},
... "$reduce" : function(doc, prev) {
...     for (i in doc.tags) {
...         if (doc.tags[i] in prev.tags) {
...             prev.tags[doc.tags[i]]++;
...         } else {
...             prev.tags[doc.tags[i]] = 1;
...         }
...     },
... "finalize" : function(prev) {
...     var mostPopular = 0;
...     for (i in prev.tags) {
...         if (prev.tags[i] > mostPopular) {
...             prev.tag = i;
...             mostPopular = prev.tags[i];
...         }
...     }
...     delete prev.tags
... }}})
```

서버는 다음과 같은 결과를 반환합니다.

```js
[
    {"day" : "2010/01/12", "tag" : "winter"},
    {"day" : "2010/01/13", "tag" : "soda"},
    {"day" : "2010/01/14", "tag" : "nosql"}
]
```

`finalize` 는 전달된 인자를 변경하거나 새로운 값을 반환할 수 있습니다.

#### 2. Using a function as a key

때로 하나의 Key 가 아닌 복잡한 조건으로 묶고 싶을 때가 있습니다.

그룹 묶음 함수를 정의하려면 `$keyf` 를 사용해야합니다. `$keyf` 를 통해 임의의 복잡한 조건으로 묶을 수 있습니다.

```js
> db.posts.group({"ns" : "posts",
... "$keyf" : function(x) { return x.category.toLowerCase(); },
... "initializer" : ... })
```