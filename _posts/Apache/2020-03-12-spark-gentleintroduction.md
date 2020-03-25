---
title : Spark A Gentle Introduction to Spark
tags :
- Apache
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

## Spark’s Basic Architecture 

컴퓨터 **클러스터** 는 여러 컴퓨터의 자원을 모아 하나의 컴퓨터처럼 사용할 수 있게 만듭니다. 하지만 클러스터를 구성하는것 외에 작업을 조율할 수 있는 프레임워크가 필요합니다. Spark 가 그런 역할을 하는 프레임워크입니다. Spark 는 클러스터 데이터 처리 작업을 관리하고 조율합니다.

Spark 가 연산에 사용할 클러스터는 Spark Standalone Cluster Manager, Hadoop YARN, Mesos 같은 클러스터 매니저에서 관리합니다. 사용자는 클러스터 매니저에 스파크 어플리케이션을 제출하고, 이를 제출받은 클러스터 매니저는 어플리케이션 실행에 필요한 자원을 할당하며 이 자원을 이용해 작업을 처리합니다.

### Spark Applications 

Spark 어플리케이션은 **드라이버(Driver)** 프로세스와 다수의 **익스큐터(Executor)** 프로세스로 구성됩니다.

드라이버 프로세스는 클러스터 노드 중 하나에서 실행되며 `main()` 함수를 실행합니다. 이는 유지 관리, 입력에 대한 응답, 전반적인 프로세스의 작업과 관련된 분석, 스케줄링 역할을 수행합니다.

**익스큐터** 는 드라이버 프로세스가 할당한 작업을 수행합니다. 즉, 드라이버가 할당한 코드를 실행하고 진행 상황을 다시 드라이버 노드에 보고하는 2 가지 역할을 수행합니다.

`Example 1` 은 클러스터 매니저가 물리적 머신을 관리하고 Spark 어플리케이션에 자원을 할당하는 방법을 나타냅니다. `Example 1` 에는 노드의 개념을 나타내지 않았습니다. 사용자는 각 노드에 할당할 익스큐터 수를 정할 수 있습니다.

> Example 1 - The architecture of a Spark Application

![image](https://user-images.githubusercontent.com/44635266/76216044-40f7a300-6253-11ea-9f12-713f10521dc2.png)

> Spark 는 클러스터 모드뿐만 아니라 **로컬 모드** 도 지원합니다. 로컬 모드로 실행하면 드라이버와 익스큐터를 단일 머신에서 스레드 형태로 실행합니다.

Spark 어플리케이션을 이해하기 위한 핵심사항은 다음과 같습니다.

* Spark 는 사용 가능한 자원을 파악하기 위해 클러스터 매니저를 사용한다.
* 드라이버 프로세스는 주어진 작업을 완료하기 위해 드라이버 프로그램의 명령을 익스큐터에서 실행할 책임이 있습니다.

익스큐터는 대부분 Spark 코드를 실행하는 역할을 합니다. 하지만 드라이버는 Spark 의 언어 API 를 통하여 다양한 언어로 실행할 수 있습니다.

## Spark’s Language APIs 

Spark 의 언어 API 를 이용하면 다양한 프로그래밍 언어로 Spark 코드를 실행할 수 있습니다. Spark 는 모든 언어에 맞는 몇몇 핵심 개념을 제공합니다. 이 핵심 개념은 클러스터 머신에서 실행되는 Spark 코드로 변환됩니다.

다음 목록은 언어별 요약 정보입니다.

* **Scala**
  * Spark 는 스칼라로 개발되어 있으므로 스칼라가 Spark 의 기본 언어입니다.
* **Java**
  * Spark 개발자들은 Java 를 이용해 Spark 코드를 작성할 수 있도록 만들었습니다.
* **Python**
  * 파이썬은 스칼라가 지원하는 거의 모든 구조를 지원합니다.
* **SQL**
  * ANSI SQL:2003 표준 중 일부를 지원합니다.
* **R**
  * Spark 에는 일반적으로 사용하는 2 개의 라이브러리가 있습니다. 하나는 Spark 코어에 포함되어 있는 `SparkR` 이고 다른 하나는 커뮤니티 기반 패키지인 `sparklyr` 입니다.
  
`Example 2` 는 `SparkSession` 과 Spark 의 언어 API 간의 관계를 나타냅니다.

> Example 2 - The relationship between the SparkSession and Spark’s Language API 

![image](https://user-images.githubusercontent.com/44635266/76216874-b31cb780-6254-11ea-830e-fe0ada622ec0.png)

사용자는 Spark 코드를 실행하기 위해 `SparkSession` 객체를 진입점으로 사용할 수 있습니다. 파이썬이나 R 로 Spark 를 사용할 때는 JVM 코드를 명시적으로 작성하지 않습니다. Spark 는 사용자를 대신해 파이썬이나 R 로 작성한 코드를 익스큐터의 JVM 에서 실행할 수 있는 코드로 변환합니다.

## Spark’s APIs 

다양한 언어로 Spark 를 사용할 수 있는 이유는 Spark 가 기본적으로 2 가지 API 를 제공하기 때문입니다. 하나는 저수준의 비구조적 API 이며, 다른 하나는 고수준의 구조적 API 입니다.

## Starting Spark 

Spark 어플리케이션을 개발하려면 사용자 명령과 데이터를 Spark 어플리케이션에 전송하는 방법을 알아야 합니다. SparkSession 을 생성하면서 알아보겠습니다.

대화형 모드로 Spark 를 시작하면 Spark 어플리케이션을 관리하는 SparkSession 이 자동으로 생성됩니다. 하지만 Standalone 어플리케이션으로 Spark 를 시작하면 사용자 어플리케이션 코드에서 SparkSession 을 직접 생성해야 합니다.

## The SparkSession 

Spark 어플리케이션은 SparkSession 이라 불리는 드라이버 프로세스로 제어합니다. SparkSession 인스턴스는 사용자가 정의한 처리 명령을 클러스터에서 실행합니다. 하나의 SparkSession 은 하나의 Spark 어플리케이션에 대응합니다.

Scala 와 Python 콘솔을 시작하면 `spark` 변수로 SparkSession 을 사용할 수 있습니다. 아래 코드를 실행해보겠습니다.

```shell
spark
```

스칼라 콘솔에서는 다음과 같은 결과를 출력합니다.

```scala
res0: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@...
```

이제 일정 범위의 숫자를 만드는 간단한 작업을 수행하겠습니다. 이 숫자들은 스프레드시트에서 컬럼명을 지정하는것과 같습니다.

```scala
val myRange = spark.range(1000).toDF("number")
```

위에서 생성한 DataFrame 은 한 개의 컬럼과 1,000 개의 로우로 구성되어있습니다. 이 숫자들은 **분산 컬렉션** 을 나타냅니다. 클러스터 모드에서 코드 예제를 실행하면 숫자 범위의 각 부분이 서로 다른 익스큐터에 할당됩니다.

## DataFrames 

DataFrame 은 가장 대표적인 구조적 API 입니다. DataFrame 은 테이블의 데이터를 로우와 컬럼으로 단순하게 표현합니다. 컬럼과 컬럼의 타입을 정의한 목록을 **스키마(Schema)** 라 합니다.

`Example 3` 은 DataFrame 과 스프레드시트 사이의 차이점을 보여줍니다. 스프레드시트는 컴퓨터에 있지만 DataFrame 은 수천 대의 컴퓨터에 분산되어 있습니다.

> Example 3 - Distributed versus single-machine analysis

![image](https://user-images.githubusercontent.com/44635266/76308004-41ed0b00-630d-11ea-9a10-000490e69c7c.png)

DataFrame 은 Spark 에서만 사용하는 개념은 아닙니다. 파이썬과 R 모두 비슷한 개념을 가지고 있습니다. Spark 는 파이썬과 R 언어를 모두 지원하므로 Pandas 라이브러리의 DataFrame, R 의 DataFrame 모두 Spark 로 쉽게 변환할 수 있습니다.

> Spark 는 DataSet, DataFrame, SQL 테이블, RDD 라는 몇가지 핵심 추상화 개념을 가지고 있습니다.

### Partitions 

Spark 는 모든 익스큐터가 병렬로 작업을 수행할 수 있도록 파티션이라 불리는 청크 단위로 데이터를 분할합니다. 파티션은 클러스터의 물리적 머신에 존재하는 로우 집합입니다.

DataFrame 의 파티션은 실행 중에 데이터가 컴퓨터 클러스터에 물리적으로 분산되는 방식을 나타냅니다. 만약 파티션이 하나라면 Spark 에 수천 개의 익스큐터가 있더라도 병렬성은 1 이 됩니다. 또한 수백 개의 파티션이 있더라도 익스큐터가 하나밖에 없다면 병렬성은 1 입니다.

DataFrame 을 사용하면 파티션을 수동 혹은 개별적으로 처리할 수 없습니다. 물리적 파티션에 데이터 변환용 함수를 지정하면 Spark 가 실제 처리 방법을 결정합니다.

## Transformations 

Spark 의 핵심 데이터 구조는 **불변성(Immutable)** 을 가집니다. 한번 생성하면 변경할 수 없습니다. DataFrame 을 변경하려면 원하는 변경 방법을 Spark 에 알려줘야 합니다. 이때 사용하는 명령을 **트랜스포메이션(Transformation)** 이라 부릅니다.

아래 예제는 DataFrame 에서 짝수를 찾는 간단한 트랜스포메이션 예제입니다.

```scala
val divisBy2 = myRange.where("number % 2 = 0")
```

결과는 출력이 되지 않습니다. 추상적인 트랜스포메이션만 지정한 상태이기 때문에 액션을 호출하지 않으면 Spark 는 실제 트랜스포메이션을 수행하지 않습니다. 트랜스포메이션은 Spark 에서 비즈니스 로직을 표현하는 핵심 개녑입니다.

트랜스포메이션에는 2 가지 유형이 있습니다. **좁은 의존성(Narrow Dependency)** 과 **넓은 의존성(Wide Dependency)** 입니다.

좁은 의존성을 가진 트랜스포메이션은 각 입력 파티션이 하나의 출력 파티션에만 영향을 미칩니다. 예제에서 `where` 구문은 좁은 의존성을 가집니다. 따라서 `Example 4` 와 같이 하나의 파티션이 하나의 출력 파티션에만 영향을 미칩니다.

> Example 4 - Narrow Dependency

![image](https://user-images.githubusercontent.com/44635266/76308689-b2485c00-630e-11ea-83ec-f82937158512.png)

넓은 의존성을 가진 트랜스포메이션은 하나의 입력 파티션이 여러 출력 파티션에 영향을 끼칩니다. Spark 가 클러스터에서 파티션을 교환하는 **셔플(Shuffle)** 이란 단어는 많이 들었을것입니다.

좁은 트랜스포메이션을 사용하면 Spark 에서 **파이프라이닝(PipeLining)** 을 자동으로 수행합니다. 즉 DataFrame 에 여러 필터를 지정하는 경우 모든 작업이 메모리에서 일어납니다. 하지만 셔플은 다른 방식으로 작동합니다. Spark 는 셔플의 결과를 디스크에 저장합니다. `Example 5` 는 넓은 트랜스포메이션입니다.

> Example 5 - Wide Dependency

![image](https://user-images.githubusercontent.com/44635266/76308703-b8d6d380-630e-11ea-8d38-8aa50fe800d3.png)

### Lazy Evaluation 

**지연 연산(Lazy Evaluation)** 은 Spark 가 연산 그래프를 처리하기 직전까지 기다리는 동작 방식을 의미합니다.

Spark 는 특정 연산 명령이 내려진 즉시 데이터를 수정하지 않고 원시 데이터에 적용할 트랜스포메이션의 **실행 계획** 을 생성합니다. Spark 는 코드를 실행하는 마지막 순간까지 대기하다 원형 DataFrame 이 트랜스포메이션을 간결한 물리적 실행 계획으로 컴파일합니다.

Spark 는 이 과정을 거치며 전체 데이터 흐름을 최적화합니다. DataFrame 의 **조건절 푸시다운(Predicate Pushdown)** 이 한 예입니다. 아주 복잡한 Spark 잡이 원시 데이터에서 하나의 로우만 가져오는 필터를 가지고 있다면 필요한 레코드 하나만 읽는 것이 가장 효율적입니다. Spark 는 이 필터를 데이터 소스로 위임하는 최적화 작업을 자동으로 수행합니다.

## Actions 

트랜스포메이션을 사용해 논리적 실행 계획을 세울 수 있습니다. 하지만 실제 연산을 수행하려면 **액션(Action)** 명령을 내려야 합니다. 액션은 일련의 트렌스 포메이션으로부터 결과를 계산하도록 지시하는 명령입니다.

가장 단순한 액션인 `count` 는 전체 레코드 수를 반환합니다.

```scala
divisBy2.count()
```

위 코드는 500 을 출력합니다. `count` 이외에 3 가지 유형의 액션이 있습니다.

* Actions to view data in the console
* Actions to collect data to native objects in the respective language
* Actions to write to output data sources

액션을 지정하면 Spark **잡(Job)** 이 시작됩니다. 잡은 필터를 수행한 후 파티션별로 레코드 수를 카운트 합니다. 그리고 각 언어에 적합한 네이티브 객체에 결과를 모읍니다. 이때 Spark 제공하는 Spark UI 로 클러스터에서 실행중인 Spark 잡을 모니터링할 수 있습니다.

## Spark UI 

Spark UI 는 Spark 잡의 진행 상황을 모니터링할 때 사용합니다. Spark UI 는 드라이버 노드의 4040 포트로 접속할 수 있습니다. 로컬 모드에서 Spark 했다면 Spark UI 의 http://localhost:4040 입니다. Spark UI 에서 Spark 잡의 상태, 환경 설정, 클러스터 상태등의 정보를 확인할 수 있습니다. Spark UI 는 Spark 잡의 튜닝하고 디버깅할 때 매우 유용합니다. `Example 6` 9 개의 테스크와 2 개의 스테이지로 이루어진 Spark 잡의 UI 예시 화면입니다.

> Example 6 - The Spark UI

![image](https://user-images.githubusercontent.com/44635266/76420321-47b61f80-63e5-11ea-9a07-dd6bdfcb6f8a.png)

## An End-to-End Example 

[미국 교통통계국의 항공운항 데이터](https://github.com/databricks/Spark-The-Definitive-Guide/tree/master/data/flight-data) 중 예제를 Spark 로 분석해보겠습니다.

각 파일은 여러 로우를 가집니다. 이 파일들은 CSV 파일이며 반정형 데이터 포맷입니다. 파일의 각 로우는 DataFrame 의 로우가 됩니다.

```shell
$ head /data/flight-data/csv/2015-summary.csv

DEST_COUNTRY_NAME,ORIGIN_COUNTRY_NAME,count
United States,Romania,15
United States,Croatia,1
United States,Ireland,344
```

Spark 는 다양한 데이터소스를 지원합니다. 데이터는 SparkSession 의 DataFrameReader 클래스를 사용해서 읽습니다. 이때 특정 파일 포맷과 몇 가지 옵션을 함께 설정합니다.

Spark DataFrame 의 스키마 정보를 알아내는 **스키마 추론(Schema Inference)** 기능을 사용합니다.

Spark 는 스키마 정보를 얻기 위해 데이터를 조금 읽습니다. 해당 로우의 데이터 타입을 Spark 데이터 타입에 맞게 분석합니다. 하지만 운영 환경에서는 데이터를 읽는 시점에 스키마를 엄격하게 지정하는 옵션을 사용해야 합니다.

```scala
val flightData2015 = spark
  .read
  .option("inferSchema", "true")
  .option("header", "true")
  .csv("/data/flight-data/csv/2015-summary.csv")
```

DataFrame 은 불특정 다수의 로우와 칼럼을 가집니다. 로우의 수를 알 수 없는 이유는 데이터를 읽는 과정이 지연 연산 형태의 트랜스포메이션이기 때문입니다. Spark 는 각 컬럼의 데이터 타입을 추론하기 위해 적은 양의 데이터를 읽습니다. `Example 7` 은 DataFrame 에서 CSV 파일을 읽어 로컬 배열이나 리스트 형태로 변환하는 과정입니다.

> Example 7 - Reading a CSV file into a DataFrame and converting it to a local array or list of rows

![image](https://user-images.githubusercontent.com/44635266/76518704-f40a0b80-64a2-11ea-9ecc-a255521ac37d.png)

DataFrame 의 `take` 액션을 호출하면 이전의 `head` 명령과 같은 결과를 확인할 수 있습니다.

```scala
flightData2015.take(3)

Array([United States,Romania,15], [United States,Croatia...
```

트랜스포메이션을 추가로 지정하겠습니다. 정수 데이터 타입인 `count` 컬럼을 기준으로 데이터를 정렬해보겠습니다. `Example 8` 은 처리 과정을 보여줍니다.

> Example 8 - Reading, sorting, and collecting a DataFrame

![image](https://user-images.githubusercontent.com/44635266/76518778-113eda00-64a3-11ea-8d61-192fad6c33fd.png)

`sort` 메소드는 트랜스포메이션이기 때문에 데이터에 아무런 변화도 일어나지 않습니다. 하지만 Spark 는 실행 계획을 만들고 검토하여 클러스터에서 처리할 방법을 알아냅니다.

특정 DataFrame 객체에 `explain` 메소드를 호출하면 DataFrame 의 Lineage 나 Spark 의 쿼리 실행 계획을 확인할 수 있습니다.

```scala
flightData2015.sort("count").explain()

== Physical Plan ==
*Sort [count#195 ASC NULLS FIRST], true, 0
+- Exchange rangepartitioning(count#195 ASC NULLS FIRST, 200)
  +- *FileScan csv [DEST_COUNTRY_NAME#193,ORIGIN_COUNTRY_NAME#194,count#195] ...
```

특정 컬럼을 다른 컬럼과 비교하는 `sort` 메소드가 넓은 트랜스포메이션으로 동작하는것을 볼 수 있습니다. 이제 트랜스포메이션 실행 계획을 시작하기 위해 액션을 호출하겠습니다.

```scala
spark.conf.set("spark.sql.shuffle.partitions", "5")

flightData2015.sort("count").take(2)

... Array([United States,Singapore,1], [Moldova,United States,1])
```

`Example 9` 는 위 예제의 데이터 처리 과정을 보여줍니다.

> Example 9 - The process of logical and physical DataFrame manipulation

![image](https://user-images.githubusercontent.com/44635266/76519010-814d6000-64a3-11ea-8df4-087927ecffb8.png)

### DataFrames and SQL

Spark SQL 을 사용하면 모든 DataFrame 을 테이블이나 뷰로 등록한 후 SQL 쿼리를 사용할 수 있습니다. Spark 는 SQL 쿼리를 DataFrame 코드와 같은 실행 계획으로 컴파일하므로 둘 차이의 성능 차이는 없습니다.

아래 예제처럼 `createOrReplaceTempView` 메소드를 호출하면 모든 DataFrame 을 테이블이나 뷰로 만들 수 있습니다.

```scala
flightData2015.createOrReplaceTempView("flight_data_2015")
```

이제 SQL 로 데이터를 조회할 수 있습니다. *spark.sql* 메소드로 SQL 쿼리를 실행합니다. `spark` 는 `SparkSession 의 변수입니다. DataFrame 에 쿼리를 수행하면 새로운 DataFrame 을 반환합니다.

로직을 작성할 때 매우 반복적인 느낌이 들지만 매우 효율적입니다. 2 가지 실행 계획을 비교해보겠습니다.

```scala
val sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
""")

val dataFrameWay = flightData2015
  .groupBy('DEST_COUNTRY_NAME)
  .count()

sqlWay.explain
dataFrameWay.explain

== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[count(1)])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#182, 5)
  +- *HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[partial_count(1)])
    +- *FileScan csv [DEST_COUNTRY_NAME#182] ...

== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[count(1)])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#182, 5)
  +- *HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[partial_count(1)])
    +- *FileScan csv [DEST_COUNTRY_NAME#182] ...
```

동일한 기본 실행 계획으로 컴파일됩니다.

다음 예제는 특정 위치를 왕래하는 최대 비행 횟수를 구해보겠습니다. `max` 함수를 이용하겠습니다.

```scala
spark.sql("SELECT max(count) from flight_data_2015").take(1)

import org.apache.spark.sql.functions.max

flightData2015.select(max("count")).take(1)
```

위 예제의 결괏값은 370,002 입니다. 다음은 상위 5 개의 도착 국가를 찾아내는 코드를 실행하겠습니다. 먼저 직관적인 SQL 집계 쿼리를 사용하겠습니다.

```scala
val maxSql = spark.sql("""
SELECT DEST_COUNTRY_NAME, sum(count) as destination_total
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
ORDER BY sum(count) DESC
LIMIT 5
""")

maxSql.show()

+-----------------+-----------------+
|DEST_COUNTRY_NAME|destination_total|
+-----------------+-----------------+
|    United States|           411352|
|           Canada|             8399|
|           Mexico|             7140|
|   United Kingdom|             2025|
|            Japan|             1548|
+-----------------+-----------------+
```

이어서 의미는 같고 구현과 정렬 방식이 다른 DataFrame 구문을 살펴보겠습니다.

```scala
import org.apache.spark.sql.functions.desc

flightData2015
  .groupBy("DEST_COUNTRY_NAME")
  .sum("count")
  .withColumnRenamed("sum(count)", "destination_total")
  .sort(desc("destination_total"))
  .limit(5)
  .show()

+-----------------+-----------------+
|DEST_COUNTRY_NAME|destination_total|
+-----------------+-----------------+
|    United States|           411352|
|           Canada|             8399|
|           Mexico|             7140|
|   United Kingdom|             2025|
|            Japan|             1548|
+-----------------+-----------------+
```

DataFrame 의 `explain` 메서드로 확인해보면 총 7 가지 단계가 있습니다. `Example 10` 에서 전체 코드 수행 단계를 볼 수 있습니다. `exaplain` 메서드가 출력하는 실제 실행 계획은 물리적인 실행 시점에서 수행하는 최적화로 인해 `Example 10` 과 다를 수 있습니다.

실행 계획은 트랜스포메이션의 **지향성 비순환 그래프(Directed Acyclic Graph, DAG)** 이며, 액션이 호출되면 결과를 만들어냅니다. 그리고 DAG 의 각 단계는 불변성을 가진 신규 DataFrame 을 생성합니다.

> Example 10 - The entire DataFrame transformation flow

![image](https://user-images.githubusercontent.com/44635266/76519991-595efc00-64a5-11ea-92b7-9255da725d9a.png)

과정을 보면 마지막 단계에서 액션을 수행합니다. 이 단계에서 DataFrame 의 결과를 모으는 프로세스를 시작합니다. 처리가 끝나면 코드를 작성한 프로그래밍 언어에 맞는 리스트나 배열을 반환합니다.

`exmplain` 메소드를 통해 실행 계획을 살펴보겠습니다.

```scala
flightData2015
  .groupBy("DEST_COUNTRY_NAME")
  .sum("count")
  .withColumnRenamed("sum(count)", "destination_total")
  .sort(desc("destination_total"))
  .limit(5)
  .explain()

== Physical Plan ==
TakeOrderedAndProject(limit=5, orderBy=[destination_total#16194L DESC], outpu...
+- *HashAggregate(keys=[DEST_COUNTRY_NAME#7323], functions=[sum(count#7325L)])
  +- Exchange hashpartitioning(DEST_COUNTRY_NAME#7323, 5)
    +- *HashAggregate(keys=[DEST_COUNTRY_NAME#7323], functions=[partial_sum...
      +- InMemoryTableScan [DEST_COUNTRY_NAME#7323, count#7325L]
        +- InMemoryRelation [DEST_COUNTRY_NAME#7323, ORIGIN_COUNTRY_NA...
          +- *Scan csv [DEST_COUNTRY_NAME#7578,ORIGIN_COUNTRY_NAME...
```

출력된 실행 계획은 **Conceptual Plan** 과 정확하게 일치하지 않지만 모든 부분을 포함하고 있습니다. 실힝 계획을 확인하면 첫 줄에서 `limit` 구문과 `orderBy` 구문을 확인할 수 있습니다.

또한, `partial_sum` 함수를 호출하는 부분에서 집계가 2 단계로 나누어지는 것을 알 수 있습니다. 단계가 나누어지는 이유는 숫자 목록의 합을 구하는 연산이 **가환성(Commutative)** 을 가지고 있어 합계 연산시 파티션별 처리가 가능하기 때문입니다.