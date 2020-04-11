---
title : Spark Joins
tags :
- Join
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

## Join Expressions

Spark 는 *left* 와 *right* 데이터셋이 있는 하나 이상의 *keys* 을 비교하고 왼쪽 데이터셋과 오른쪽 데이터셋의 결합 여부를 결정하는 **조인 표현식(Join Expression)** 의 평과 결과애 따라 두 개의 데이터셋을 조인합니다.

가장 많이 사용하는 조인 표현식은 키가 동일한지 비교하는 동등 조인(equi-join) 입니다. Spark 에선 동등 조인뿐만 아니러 복잡한 조인 정책도 지원하며, 복합 데이터 타입을 조인하여 사용할 수 있습니다.

## Join Types

조인 표현식은 두 로우의 조인 여부를 결정하는 반면 조인 타입은 결과 데이터셋에 어떤 데이터가 있어야 하는지 결정합니다. Spark 에 사용할 수 있는 조인 타입은 다음과 같습니다.

Spark 에서 사용할 수 있는 조인 타입은 다음과 같습니다.

* Inner Join
* Outer Join
* Left Outer Join
* Right Outer Join
* Left Semi Join
* Left Anti Join
* natural Join
* Cross Join

이제 각 조인 타입에 대한 예제를 살펴보겠습니다.

```scala
// in Scala
val person = Seq(
    (0, "Bill Chambers", 0, Seq(100)),
    (1, "Matei Zaharia", 1, Seq(500, 250, 100)),
    (2, "Michael Armbrust", 1, Seq(250, 100)))
  .toDF("id", "name", "graduate_program", "spark_status")

val graduateProgram = Seq(
    (0, "Masters", "School of Information", "UC Berkeley"),
    (2, "Masters", "EECS", "UC Berkeley"),
    (1, "Ph.D.", "EECS", "UC Berkeley"))
  .toDF("id", "degree", "department", "school")

val sparkStatus = Seq(
    (500, "Vice President"),
    (250, "PMC Member"),
    (100, "Contributor"))
  .toDF("id", "status")
```

생성한 데이터셋을 전체 예제에 사용하기 위해 테이블로 등록하겠습니다.

```scala
person.createOrReplaceTempView("person")
graduateProgram.createOrReplaceTempView("graduateProgram")
sparkStatus.createOrReplaceTempView("sparkStatus")
```

## Inner Joins

내부 조인은 DataFrame 이나 테이블에 존재하는 키를 평가합니다. 그리고 참으로 평가되는 로우만 결합합니다. 다음은 `graduateProgram` DataFrame 과 `person` DataFrame 을 조인해 새로운 DataFrame 을 만드는 예제입니다.

```scala
// in Scala
val joinExpression = person.col("graduate_program") === graduateProgram.col("id")
```

두 DataFrame 모두 키가 존재하지 않으면 결과 DataFrame 에서 볼 수 없습니다.

```scala
// in Scala
val wrongJoinExpression = person.col("name") === graduateProgram.col("school")
```

내부 조인은 기본 조인 방식이므로 `JOIN` 표현식에 왼쪽 DataFrame 과 오른쪽 DataFrame 을 지정하기만 하면 됩니다.

```scala
person.join(graduateProgram, joinExpression).show()
```

```sql
-- in SQL
SELECT * FROM person JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
```

실행결과는 아래와 같습니다.

```
+---+----------------+----------------+---------------+---+-------+----------+---
| id|            name|graduate_program|   spark_status| id| degree|department|...
+---+----------------+----------------+---------------+---+-------+----------+---
|  0|   Bill Chambers|               0|          [100]|  0|Masters| School...|...
|  1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|      EECS|...
|  2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|      EECS|...
+---+----------------+----------------+---------------+---+-------+----------+---
```

`join` 메소드의 세 번째 파라미터로 조인 타입을 명확하게 지정할 수 있습니다.

```scala
// in Scala
var joinType = "inner"

person.join(graduateProgram, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM person INNER JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
```

실행결과는 아래와 같습니다.

```
+---+----------------+----------------+---------------+---+-------+--------------
| id|            name|graduate_program|   spark_status| id| degree| department...
+---+----------------+----------------+---------------+---+-------+--------------
|  0|   Bill Chambers|               0|          [100]|  0|Masters|     School...
|  1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|       EECS...
|  2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|       EECS...
+---+----------------+----------------+---------------+---+-------+--------------
```

## Outer Joins

외부 조인은 DataFrame 이나 테이블에 존재하는 키를 평가하여 true 나 false 로 평가한 로우를 포함합니다. 왼쪽이나 오른쪽 DataFrame 에 일치하는 로우가 없다면 Spark 는 해당 위치에 null 을 삽입합니다.

```scala
joinType = "outer"

person.join(graduateProgram, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM person FULL OUTER JOIN graduateProgram
  ON graduate_program = graduateProgram.id
```

실행결과는 아래와 같습니다.

```
+----+----------------+----------------+---------------+---+-------+-------------
|  id|            name|graduate_program|   spark_status| id| degree| departmen...
+----+----------------+----------------+---------------+---+-------+-------------
|   1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|       EEC...
|   2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|       EEC...
|null|            null|            null|           null|  2|Masters|       EEC...
|   0|   Bill Chambers|               0|          [100]|  0|Masters|    School...
+----+----------------+----------------+---------------+---+-------+-------------
```

## Left Outer Joins

왼쪽 외부 조인은 DataFrame 이나 테이블에 존재하는 키를 평가합니다. 그리고 왼쪽 DataFrame 의 모든 로우와 왼쪽 DataFrame 과 일치하는 오른쪽 DataFrame 의 로우를 함께 포함합니다.

오른쪽 DataFrame 에 일치하는 로우가 없다면 Spark 는 해당 위치에 null 을 삽입합니다.

```scala
joinType = "left_outer"

graduateProgram.join(person, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM graduateProgram LEFT OUTER JOIN person
  ON person.graduate_program = graduateProgram.id
```

실행결과는 아래와 같습니다.

```
+---+-------+----------+-----------+----+----------------+----------------+---
| id| degree|department|     school|  id|            name|graduate_program|...
+---+-------+----------+-----------+----+----------------+----------------+---
|  0|Masters| School...|UC Berkeley|   0|   Bill Chambers|               0|...
|  2|Masters|      EECS|UC Berkeley|null|            null|            null|...
|  1|  Ph.D.|      EECS|UC Berkeley|   2|Michael Armbrust|               1|...
|  1|  Ph.D.|      EECS|UC Berkeley|   1|   Matei Zaharia|               1|...
+---+-------+----------+-----------+----+----------------+----------------+---
```

## Right Outer Joins

오른쪽 외부 조인은 DataFrame 이나 테이블에 존재하는 키를 평가합니다. 오른쪽 DataFrame 의 모든 로우와 오른쪽 DataFrame 과 일치하는 왼쪽 DataFrame 의 로우를 함께 포함합니다.

왼쪽 DataFrame 에 일치하는 로우가 없다면 Spark 는 해당 위치에 null 을 삽입합니다.

```scala
joinType = "right_outer"

person.join(graduateProgram, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM person RIGHT OUTER JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
```

실행결과는 아래와 같습니다.

```
+----+----------------+----------------+---------------+---+-------+------------+
|  id|            name|graduate_program|   spark_status| id| degree|  department|
+----+----------------+----------------+---------------+---+-------+------------+
|   0|   Bill Chambers|               0|          [100]|  0|Masters|School of...|
|null|            null|            null|           null|  2|Masters|        EECS|
|   2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|        EECS|
|   1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|        EECS|
+----+----------------+----------------+---------------+---+-------+------------+
```

## Left Semi Joins

세미 조인은 오른쪽 DataFrame 의 어떤 값도 포함하지 않기 때문에 다른 조인 타입과는 다릅니다.

단지 두 번째 DataFrame 은 값이 존재하는지 확인하기 위해 값만 비교하는 용도로 사용합니다. 만약 값이 존재한다면 왼쪽 DataFrame 에 중복 키가 존재하더라도 해당 로우는 결과에 포함됩니다.

왼쪽 세미 조인은 기존 조인 기능과는 달리 DataFrame 의 필터 정도로 볼 수 있습니다.

```scala
joinType = "left_semi"
graduateProgram.join(person, joinExpression, joinType).show()
```

실행결과는 아래와 같습니다.

```
+---+-------+--------------------+-----------+
| id| degree|          department|     school|
+---+-------+--------------------+-----------+
|  0|Masters|School of Informa...|UC Berkeley|
|  1|  Ph.D.|                EECS|UC Berkeley|
+---+-------+--------------------+-----------+
```

```scala
// in Scala
val gradProgram2 = graduateProgram.union(Seq(
    (0, "Masters", "Duplicated Row", "Duplicated School")).toDF())

gradProgram2.createOrReplaceTempView("gradProgram2")
gradProgram2.join(person, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM gradProgram2 LEFT SEMI JOIN person
  ON gradProgram2.id = person.graduate_program
```

실행결과는 아래와 같습니다.

```
+---+-------+--------------------+-----------------+
| id| degree|          department|           school|
+---+-------+--------------------+-----------------+
|  0|Masters|School of Informa...|      UC Berkeley|
|  1|  Ph.D.|                EECS|      UC Berkeley|
|  0|Masters|      Duplicated Row|Duplicated School|
+---+-------+--------------------+-----------------+
```

## Left Anti Joins

안티 조인은 세미 조인의 반대 개념입니다.

두 번째 DataFrame 은 값이 존재하는지 확인하기 위해 값만 비교하는 용도로 사용합니다. 하지만 두 번째 DataFrame 에 존재하는 값을 유지하는 대신 두 번째 DataFrame 에서 관련된 키를 찾을 수 업슨ㄴ 로우만 결과에 포함합니다.

안티 조인은 SQL 의 `NOT IN` 과 같은 스타일의 필터로 볼 수 있습니다.

```scala
joinType = "left_anti"
graduateProgram.join(person, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM graduateProgram LEFT ANTI JOIN person
  ON graduateProgram.id = person.graduate_program
```

실행결과는 아래와 같습니다.

```
+---+-------+----------+-----------+
| id| degree|department|     school|
+---+-------+----------+-----------+
|  2|Masters|      EECS|UC Berkeley|
+---+-------+----------+-----------+
```

## Natural Joins

자연 조인은 조인하려는 칼럼을 암시적으로 추정합니다. 즉, 일치하는 칼럼을 찾고 그 결과를 반환합니다.

## Cross (Cartesian) Joins

마지막으로 알아볼 조인은 교차조인입니다. 교차 조인은 조건절을 기술하지 않은 내부 조인입니다. 교차 조인은 왼쪽 DataFrame 의 모든 로우를 오른쪽 DataFrame 의 모든 로우와 결합합니다.

1,000 개의 로우가 존재하는 두 개의 DataFrame 에 교차 조인을 수행하면 1,000,000 (1,000 * 1,000) 의 결과 로우가 생성됩니다.

반드시 키워드를 이용해 교차 조인을 수행한다는 것을 명시적으로 선언해야 합니다.

```scala
joinType = "cross"
graduateProgram.join(person, joinExpression, joinType).show()
```

```sql
-- in SQL
SELECT * FROM graduateProgram CROSS JOIN person
  ON graduateProgram.id = person.graduate_program
```

실행결과는 아래와 같습니다.

```
+---+-------+----------+-----------+---+----------------+----------------+-------
| id| degree|department|     school| id|            name|graduate_program|spar...
+---+-------+----------+-----------+---+----------------+----------------+-------
|  0|Masters| School...|UC Berkeley|  0|   Bill Chambers|               0|    ...
|  1|  Ph.D.|      EECS|UC Berkeley|  2|Michael Armbrust|               1|  [2...
|  1|  Ph.D.|      EECS|UC Berkeley|  1|   Matei Zaharia|               1|[500...
+---+-------+----------+-----------+---+----------------+----------------+-------
```

교차 조인이 필요한 경우 다음과 같이 명시적으로 메소드를 호출할 수 있습니다.

```scala
person.crossJoin(graduateProgram).show()
```

```sql
-- in SQL
SELECT * FROM graduateProgram CROSS JOIN person
```

실행결과는 아래와 같습니다.

```
+---+----------------+----------------+---------------+---+-------+-------------+
| id|            name|graduate_program|   spark_status| id| degree|   departm...|
+---+----------------+----------------+---------------+---+-------+-------------+
|  0|   Bill Chambers|               0|          [100]|  0|Masters|    School...|
...
|  1|   Matei Zaharia|               1|[500, 250, 100]|  0|Masters|    School...|
...
|  2|Michael Armbrust|               1|     [250, 100]|  0|Masters|    School...|
...
+---+----------------+----------------+---------------+---+-------+-------------+
```

## Challenges When Using Joins

조인의 수행 방식과 최적화와 관련된 사항을 알아보겠습니다.

### Joins on Complex Types

불리언을 반환하는 모든 표현식은 조인 표현식으로 간주할 수 있습니다.

```scala
import org.apache.spark.sql.functions.expr

person.withColumnRenamed("id", "personId")
  .join(sparkStatus, expr("array_contains(spark_status, id)")).show()
```

```sql
-- in SQL
SELECT * FROM
  (select id as personId, name, graduate_program, spark_status FROM person)
  INNER JOIN sparkStatus ON array_contains(spark_status, id)
```

실행결과는 아래와 같습니다.

```
+--------+----------------+----------------+---------------+---+--------------+
|personId|            name|graduate_program|   spark_status| id|        status|
+--------+----------------+----------------+---------------+---+--------------+
|       0|   Bill Chambers|               0|          [100]|100|   Contributor|
|       1|   Matei Zaharia|               1|[500, 250, 100]|500|Vice President|
|       1|   Matei Zaharia|               1|[500, 250, 100]|250|    PMC Member|
|       1|   Matei Zaharia|               1|[500, 250, 100]|100|   Contributor|
|       2|Michael Armbrust|               1|     [250, 100]|250|    PMC Member|
|       2|Michael Armbrust|               1|     [250, 100]|100|   Contributor|
+--------+----------------+----------------+---------------+---+--------------+
```

### Handling Duplicate Column Names

조인을 할 때 중복된 칼럼명을 처리하는 방법은 까다롭습니다. DataFrame 의 각 칼럼은 Spark SQL 엔진인 카탈리스트 내에 고유 ID 가 있습니다.

고유 ID 는 카탈리스트 내부에서만 사용할 수 있으며 직접 참조할 수 없습니다. 그러므로 중복된 칼럼이 존재하는 DataFrame 을 사용할 때는 특정 칼럼을 참조하기 매우 어렵습니다.

이런 문제를 일으키는 두 가지 상황이 있습니다.

* The join expression that you specify does not remove one key from one of the input DataFrames and the keys have the same column name
* Two columns on which you are not performing the join have the same name

예시를 들기위해 잘못된 데이터 셋을 만들어보겠습니다.

```scala
val gradProgramDupe = graduateProgram.withColumnRenamed("id", "graduate_program")

val joinExpr = gradProgramDupe.col("graduate_program") === person.col(
  "graduate_program")
```

`graduate_program` 칼럼을 키로 해서 조인을 수행하여도 두 개의 `graduate_program` 칼럼이 존재합니다.

```scala
person.join(gradProgramDupe, joinExpr).show()
```

칼럼 중 하나를 참조할 때 문제가 발생합니다.

```scala
person.join(gradProgramDupe, joinExpr).select("graduate_program").show()
```

위 예제를 실행하면 Spark 에선 다음과 같은 오류 메세지를 출력합니다.

```scala
org.apache.spark.sql.AnalysisException: Reference 'graduate_program' is
ambiguous, could be: graduate_program#40, graduate_program#1079.;
```

#### APPROACH 1: DIFFERENT JOIN EXPRESSION

동일한 이름을 가진 두 개의 Key 를 사용한다면 가장 쉬운 조치 방법 중 하나는 불리언 형태의 조인 표현식을 문자열이나 시퀀스 형태로 바꾸는 겁니다. 이렇게 하면 조인을 할 때 두 칼럼 중 하나가 자동으로 제거됩니다.

```scala
person.join(gradProgramDupe,"graduate_program").select("graduate_program").show()
```

#### APPROACH 2: DROPPING THE COLUMN AFTER THE JOIN

조인 후 문제가 되는 칼럼을 제거하는 방법도 있습니다. 이 경우 원본 DataFrame 을 사용해 칼럼을 참조해야 합니다. 조인 시 동일한 Key 이름을 사용하거나 우너본 DataFrame 에 동일한 칼럼명이 존재하는 경우 사용할 수 있습니다.

```scala
person.join(gradProgramDupe, joinExpr).drop(person.col("graduate_program"))
  .select("graduate_program").show()

val joinExpr = person.col("graduate_program") === graduateProgram.col("id")
person.join(graduateProgram, joinExpr).drop(graduateProgram.col("id")).show()
```

이 방법은 Spark 의 SQL 분석 프로세스의 특성을 활용합니다. Spark 는 명시적으로 참조된 칼럼을 검증할 필요가 없으므로 Spark 코드 분석 단계를 통과합니다. 위 예제에서 `column` 함수 대신 `col` 메소드를 사용한 부분을 주목할 필요가 있습니다.

`col` 메소드를 사용하여 칼럼 고유의 ID 로 해당 칼럼을 암시적으로 지정할 수 있습니다.

#### APPROACH 3: RENAMING A COLUMN BEFORE THE JOIN

조인 전에 칼럼명을 변경하면 이런 문제를 완전히 회피할 수 있습니다.

```scala
val gradProgram3 = graduateProgram.withColumnRenamed("id", "grad_id")
val joinExpr = person.col("graduate_program") === gradProgram3.col("grad_id")
person.join(gradProgram3, joinExpr).show()
```

## How Spark Performs Joins

Spark 가 조인을 수행하는 방식을 이해하기 위해서는 실행에 필요한 두 가지 핵심 전략을 이해해야합니다.

* 노드간 네트워크 통신 전략
* 노드별 연산 전략

### Communication Strategies

Spark 는 조인 시 두 가지 클러스터 통신 방식을 활용합니다. 전체 노드간 통신을 유발하는 **셔플 조인(Shuffle Join)** 과 그렇지 않은 **브로드캐스트 조인(Broadcast Join)** 입니다.

내부 최적화 기술은 시간이 흘러 **비용 기반 옵티마이저(Cost-Based Optimizer)** 가 개선되고 더 나은 통신 전략이 도입되는 경우 바뀔 수 있습니다. 일반적인 상황에서 정확히 어떤 일이 일어나는지 이해할 수 있도록 고수준 예제를 알아보겠습니다. 그러면 워크로드의 성능을 빠르고 쉽게 최적화하는 방법을 알 수 있습니다.

#### BIG TABLE–TO–BIG TABLE

큰 테이블에서 다른 큰 테이블을 조인하면 `Example 1` 과 같이 셔플 조인이 발생합니다.

> Example 1 - Joining two big tables

![image](https://user-images.githubusercontent.com/44635266/78557184-4690da80-784b-11ea-810a-4b250092471f.png)

셔플 조인은 전체 노드 간 통신이 발생합니다. 그리고 조인에 사용한 특정 Key 나 Key 집합을 어떤 노드가 가졌는지에 따라 해당 노드와 데이터를 공유합니다. 이런 통신 방식때문에 네트워큰는 복잡해지고 많은 자원을 사용합니다. 특히 데이터가 잘 나뉘어 있지 않다면 더 심해집니다.

`Example 1` 의 DataFrame 1 과 2 는 모두 큰 DataFrame 입니다. 즉, 전체 조인 프로세스가 진행되는 동안 모든 워커노드에서 통신이 발생합니다.

#### BIG TABLE–TO–SMALL TABLE

테이블이 단일 워커 노드의 메모리 크기에 적합할 정도로 충분히 작은 경우 조인 연산을 최적화할 수 있습니다. 큰 테이블 사이의 조인에 사용한 방법도 유용하지만 브로드캐스트 조인이 훨씬 효율적입니다.

이 방법은 작은 DataFrame 을 클러스터의 전체 워커 노드에 복제하는 것을 의미합니다. 자원을 많이 사용할 것처럼 보이지만 조인 프로세스 내내 전체 노드가 통신하는 현상을 방지할 수 있습니다. `Example 2` 에서 보듯이 시작 시 단 한번만 복제가 수행되며 그 이후로는 개별 워커가 다른 워커 노드를 기다리거나 통신할 필요 없이 작업을 수행합니다.

> Example 2 - A broadcast join

![image](https://user-images.githubusercontent.com/44635266/78557363-9b345580-784b-11ea-871a-cb3d833d9c65.png)

브로드캐스트 조인은 이전 조인과 마찬가지로 대규모 노드간 통신이 발생합니다. 하지만, 그 이후로 노드 사이에 추가적인 통신이 발생하지 않습니다. 따라서 모든 단일 노드에서 개별적으로 조인이 수행되므로 CPU 가 가장 큰 병목 구간이 됩니다.

아래 예제와 같이 실행 계획을 살펴보면 Spark 가 자동으로 데이터셋을 브로드캐스트 조인으로 설정한것을 확인할 수 있습니다.

```scala
val joinExpr = person.col("graduate_program") === graduateProgram.col("id")

person.join(graduateProgram, joinExpr).explain()

== Physical Plan ==
*BroadcastHashJoin [graduate_program#40], [id#5....
:- LocalTableScan [id#38, name#39, graduate_progr...
+- BroadcastExchange HashedRelationBroadcastMode(....
   +- LocalTableScan [id#56, degree#57, departmen....
```

DataFrame API 를 사용하면 옵티마이저에 브로드캐스트 조인을 사용할 수 있도록 힌트를 줄 수 있습니다. 힌트를 주는 방법은 `broadcast` 함수에 작은 크기의 DataFrame 을 인수로 전달하는 겁니다.

```scala
import org.apache.spark.sql.functions.broadcast

val joinExpr = person.col("graduate_program") === graduateProgram.col("id")
person.join(broadcast(graduateProgram), joinExpr).explain()
```

SQL 역시 조인 수행에 필요한 힌트를 줄 수 있습니다. 하지만 강제성이 없으므로 옵티마이저가 이를 무시할 수 있습니다.

특수 주석 구문을 사용해 `MAPJOIN`, `BROADCAST`m `BROADCASTJOIN` 등의 힌트를 설정할 수 있습니다. 이들 모두 동일한 작업을 수행하며 모두 힌트로 사용할 수 있습니다.

```sql
-- in SQL
SELECT /*+ MAPJOIN(graduateProgram) */ * FROM person JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
```

큰 데이터를 브로드캐스트하면 고비용의 수집 연산이 발생하므로 드라이버 노드가 비정상적으로 종료될 수 있습니다. 이 현상은 향후 개선되어야 하는 영역입니다.

#### LITTLE TABLE–TO–LITTLE TABLE

아주 작은 테이블 사이의 조인은 Spark 가 조인 방식을 결정하도록 내버려두는 것이 좋습니다. 필요한 경우 브로드캐스트 조인을 강제로 지정할 수 있습니다.