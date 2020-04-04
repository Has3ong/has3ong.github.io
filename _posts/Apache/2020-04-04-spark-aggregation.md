---
title : Spark Aggregations
tags :
- Window Function
- Grouping
- Aggregation
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

**집계(aggregation)** 는 빅데이터 분석의 초석입니다. 집계를 수행하려면 **Key** 나 **Group** 을 지정하고 하나 이상의 칼럼을 변환하는 방법을 지정하는 집계 함수를 사용합니다.

Spark 는 모든 데이터 타입을 다루는것 외에도 다음과 같은 그룹화 데이터 타입을 생성할 수 있습니다.

* The simplest grouping is to just summarize a complete DataFrame by performing an aggregation in a `select` statement.
* A `group by` allows you to specify one or more keys as well as one or more aggregation functions to transform the value columns.
* A `window` gives you the ability to specify one or more keys as well as one or more aggregation functions to transform the value columns. However, the rows input to the function are somehow related to the current row.
* A `grouping set`, which you can use to aggregate at multiple different levels. Grouping sets are available as a primitive in SQLand via rollups and cubes in DataFrames.
* A `rollup` makes it possible for you to specify one or more keys as well as one or more aggregation functions to transform the value columns, which will be summarized hierarchically.
* A `cube` allows you to specify one or more keys as well as one or more aggregation functions to transform the value columns, which will be summarized across all combinations of columns.

지정된 집계 함수에 따라 그룹화된 결과는 `RelationalGroupedDataset` 을 반환합니다.

구매 이력 데이터를 사용해 파티션을 훨씬 적은 수로 분한할 수 있도록 리파티셔닝하고 빠르게 접근할 수 있도록 캐싱하겠습니다. 파티션 수를 줄이는 이유는 적은 양의 데이터를 가진 수많은 파일이 존재하기 때문입니다.

```scala
// in Scala
val df = spark.read.format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/data/retail-data/all/*.csv")
  .coalesce(5)

df.cache()
df.createOrReplaceTempView("dfTable")
```

다음은 함수의 결과를 비교할 수 있도록 샘플 데이터를 출력한 겁니다.

```scala
+---------+---------+--------------------+--------+--------------+---------+-----
|InvoiceNo|StockCode|         Description|Quantity|   InvoiceDate|UnitPrice|Cu...
+---------+---------+--------------------+--------+--------------+---------+-----
|   536365|   85123A|   WHITE HANGING... |       6|12/1/2010 8:26|     2.55| ...
|   536365|    71053|     WHITE METAL... |       6|12/1/2010 8:26|     3.39| ...
...
|   536367|    21755|LOVE BUILDING BLO...|       3|12/1/2010 8:34|     5.95| ...
|   536367|    21777|RECIPE BOX WITH M...|       4|12/1/2010 8:34|     7.95| ...
+---------+---------+--------------------+--------+--------------+---------+-----
```

DataFrame 을 사용해 기본 집계를 수행해보겠습니다. 다음은 `count` 메소드를 사용한 간단한 예제입니다.

```scala
df.count() == 541909
```

`count` 메소드는 트랜스포메이션이 아닌 액션이므로 결과를 즉시 반환합니다.

지금은 `count` 함수가 메소드 형태로 존재하고 트랜스포메이션처럼 지연 연산 방식이 아닌 즉시 연산을 수행하기 때문입니다. 지연 연산 방식으로 `count` 메소드를 사용하는 방법을 알아보겠습니다.

## Aggregation Functions

집계 함수는 `org.apache.spark.sql.functions` 패키지에서 찾아볼 수 있습니다.

### count

`count` 함수는 두 가지 방식으로 사용할 수 있습니다. 하나는 `count` 함수에 특정 칼럼을 지정하는 방식이고 다른 하나는 `count(*)` 나 `count(1)` 을 사용하는 방식입니다.

```scala
// in Scala
import org.apache.spark.sql.functions.count

df.select(count("StockCode")).show() // 541909
```

```sql
-- in SQL
SELECT COUNT(*) FROM dfTable
```

### countDistinct

전체 레코드 수가 아닌 고유 레코드 수를 구해야 한다면 `countDistinct` 함수를 사용합니다. 이 함수는 개별 칼럼을 처리하는 데 더 적합합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.countDistinct

df.select(countDistinct("StockCode")).show() // 4070
```

```sql
-- in SQL
SELECT COUNT(DISTINCT *) FROM DFTABLE
```

### approx_count_distinct

대규모 데이터셋을 다루다 보면 정확한 고유 개수가 무의미할 때도 있습니다. 어느 정도 수준의 정확도를 가지는 근사치만으로도 유의미하다면 `approx_count_distinct` 함수를 사용해 근사치를 계산할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.approx_count_distinct

df.select(approx_count_distinct("StockCode", 0.1)).show() // 3364
```

```sql
-- in SQL
SELECT approx_count_distinct(StockCode, 0.1) FROM DFTABLE
```

`approx_count_distinct` 함수는 **최대 추정 오류율(maximum estimation error)** 라는 한 가지 파라미터를 더 사용합니다. 예제는 큰 오류율 설정했기 때문으 기대치에서 크게 벗어나는 결과를 얻지만, `countDistinct` 함수보다 더 빠르게 결과를 반환합니다. 

이 함수의 성능은 대규모 데이터셋을 사용할 때 훨씬 더 좋아집니다.

### first and last

`first` 와 `last` 는 DataFrame 의 첫 번째 값과 마지막 값을 얻을 때 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{first, last}

df.select(first("StockCode"), last("StockCode")).show()
```

```sql
-- in SQL
SELECT first(StockCode), last(StockCode) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+-----------------------+----------------------+
|first(StockCode, false)|last(StockCode, false)|
+-----------------------+----------------------+
|                 85123A|                 22138|
+-----------------------+----------------------+
```

### min and max

DataFrame 에 최솟값과 최댓값을 추출하려면 `min` 과 `max` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{min, max}

df.select(min("Quantity"), max("Quantity")).show()
```

```sql
-- in SQL
SELECT min(Quantity), max(Quantity) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+-------------+-------------+
|min(Quantity)|max(Quantity)|
+-------------+-------------+
|       -80995|        80995|
+-------------+-------------+
```

### sum

DataFrame 에 특정 칼럼의 모든 값을 합산하려면 `sum` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.sum

df.select(sum("Quantity")).show() // 5176450
```

```sql
-- in SQL
SELECT sum(Quantity) FROM dfTable
```

### sumDistinct

특정 칼럼의 모든 값을 합산하는 방법 외에도 `sumDistinct` 함수를 사용해 고윳값을 합산할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.sumDistinct

df.select(sumDistinct("Quantity")).show() // 29310
```

```sql
-- in SQL
SELECT SUM(Quantity) FROM dfTable -- 29310
```

### avg

`sum` 함수의 결과를 `count` 함수의 결과로 나누어 평균값을 구할 수 있지만, Spark 의 `avg` 나 `mean` 함수를 사용해 더 쉽게 구할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{sum, count, avg, expr}

df.select(
    count("Quantity").alias("total_transactions"),
    sum("Quantity").alias("total_purchases"),
    avg("Quantity").alias("avg_purchases"),
    expr("mean(Quantity)").alias("mean_purchases"))
  .selectExpr(
    "total_purchases/total_transactions",
    "avg_purchases",
    "mean_purchases").show()
```

실행결과는 아래와 같습니다.

```scala
+--------------------------------------+----------------+----------------+
|(total_purchases / total_transactions)|   avg_purchases|  mean_purchases|
+--------------------------------------+----------------+----------------+
|                      9.55224954743324|9.55224954743324|9.55224954743324|
+--------------------------------------+----------------+----------------+
```

### Variance and Standard Deviation

분산은 평균과의 차이를 제곱한 결과의 평균이며 표준편차는 분산의 제곱근입니다. Spark 에서는 함수를 사용해 분산과 표준 편차를 구할 수 있습니다.

`variance` 함수나 `stddev` 함수를 사용한다면 기본적으로 **표본표준분산(Sample Standard Variance)** 과 표본표준편차 공식을 이용합니다.

**모표준분산(Population Standard Variance)** 이나 모표준편차 방식을 사용하려면 다음 예제와 같이 `var_pop` 함수나 `stddev_pop` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{var_pop, stddev_pop}
import org.apache.spark.sql.functions.{var_samp, stddev_samp}

df.select(var_pop("Quantity"), var_samp("Quantity"),
  stddev_pop("Quantity"), stddev_samp("Quantity")).show()
```

```sql
-- in SQL
SELECT var_pop(Quantity), var_samp(Quantity),
  stddev_pop(Quantity), stddev_samp(Quantity)
FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+------------------+------------------+--------------------+-------------------+
| var_pop(Quantity)|var_samp(Quantity)|stddev_pop(Quantity)|stddev_samp(Quan...|
+------------------+------------------+--------------------+-------------------+
|47559.303646609056|47559.391409298754|  218.08095663447796|   218.081157850...|
+------------------+------------------+--------------------+-------------------+
```

### skewness and kurtosis

**비대칭도(Skewness)** 와 **첨도(Kurtosis)** 모두 데이터의 **변곡점(Extreme Point)** 을 측정하는 방법입니다. 비대칭도는 데이터 평균의 비대칭 정도를 측정하고, 첨도는 데이터 끝 부분을 측정합니다.

비대칭도와 첨도는 **확률변수(Random Variable)** 의 **확률분포(Probability Distribution)** 로 데이터를 모델링할 때 중요합니다.

```scala
import org.apache.spark.sql.functions.{skewness, kurtosis}

df.select(skewness("Quantity"), kurtosis("Quantity")).show()
```

```sql
-- in SQL
SELECT skewness(Quantity), kurtosis(Quantity) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+-------------------+------------------+
| skewness(Quantity)|kurtosis(Quantity)|
+-------------------+------------------+
|-0.2640755761052562|119768.05495536952|
+-------------------+------------------+
```

### Covariance and Correlation

두 칼럼값 사이의 영향도를 비교하는 함수를 알아보겠습니다. `cov` 와 `corr` 함수를 사용해 **공분산(Covariance)** 과 **상관관계(Correlation)** 를 계산할 수 있습니다.

공분산은 데이터 입력값에 따라 다른 범위를 가집니다. 상관관계는 **피어슨 상관계수(Pearson Correlation Coefficient)** 를 측정하며 -1 과 1 사이의 값을 가집니다.

`var` 함수처럼 **표본공분산(Sample Covariance)** 방식이나 **모공분산(Population Covariance)** 방식으로 공분산을 계산할 수 있습니다. 상관관계는 모집단이나 표본에 대한 계산 개념이 없습니다. 공분산과 상관관계를 수행하는 방법은 다음과 같습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{corr, covar_pop, covar_samp}

df.select(
  corr("InvoiceNo", "Quantity"),
  covar_samp("InvoiceNo", "Quantity"),
  covar_pop("InvoiceNo", "Quantity")).show()
```

```sql
-- in SQL
SELECT corr(InvoiceNo, Quantity), covar_samp(InvoiceNo, Quantity),
  covar_pop(InvoiceNo, Quantity)
FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+-------------------------+-------------------------------+---------------------+
|corr(InvoiceNo, Quantity)|covar_samp(InvoiceNo, Quantity)|covar_pop(InvoiceN...|
+-------------------------+-------------------------------+---------------------+
|     4.912186085635685E-4|             1052.7280543902734|            1052.7...|
+-------------------------+-------------------------------+---------------------+
```

### Aggregating to Complex Types

Spark 는 수식을 이용한 집계뿐만 아니라 복합 데이터 타입을 사용해 집계를 수행할 수 있습니다. 예를 들어 특정 칼럼의 값을 리스트로 수집하거나 셋 데이터 타입으로 고윳값만 수집할 수 있습니다.

수집된 데이터는 처리 파이프라인에서 다양한 프로그래밍 방식으로 다루거나 사용자 정의 함수를 사용해 전체 데이터에 접근할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{collect_set, collect_list}

df.agg(collect_set("Country"), collect_list("Country")).show()
```

```sql
-- in SQL
SELECT collect_set(Country), collect_set(Country) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+--------------------+---------------------+
|collect_set(Country)|collect_list(Country)|
+--------------------+---------------------+
|[Portugal, Italy,...| [United Kingdom, ...|
+--------------------+---------------------+
```

## Grouping

데이터 **그룹** 기반의 집계를 수행하는 경우가 더 많습니다. 데이터 그룹 기반의 집계는 단일 칼럼의 데이터를 그룹화하고 해당 그룹의 다른 여러 칼럼을 사용해서 계산하기 위해 카테고리형 데이터를 사용합니다.

데이터 그룹 기반의 집계를 설명하는 데 가장 좋은 방법은 그룹화입니다. 그룹화 작업은 하나 이상의 칼럼을 그룹화하고 집계 연산을 수행하는 두 단계로 이뤄집니다.

첫 번째 단계에서는 RelationalGroupedDataset 이 반환되고, 두 번째 단계에서는 DataFrame 이 반환됩니다. 그룹의 기준이 되는 칼럼을 여러 개 지정할 수 있습니다.

```scala
df.groupBy("InvoiceNo", "CustomerId").count().show()
```

```sql
-- in SQL
SELECT count(*) FROM dfTable GROUP BY InvoiceNo, CustomerId
```

실행결과는 아래와 같습니다.

```scala
+---------+----------+-----+
|InvoiceNo|CustomerId|count|
+---------+----------+-----+
|   536846|     14573|   76|
...
|  C544318|     12989|    1|
+---------+----------+-----+
```

### Grouping with Expressions

카운팅은 메소드로 사용할 수 있으므로 조금 특별합니다. 하지만 메소드 대신 `count` 함수를 사용할 것을 추천합니다. `count` 함수를 `select` 구문에 표현식으로 지정하는 것보다 `agg` 메소드를 사용하는 것이 좋습니다.

`agg` 메소드는 한 번에 지정할 수 있으며, 집계에 표현식을 사용할 수 있습니다. 또한 트랜스포메이선이 완료된 `alias` 메소드를 사용할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.count

df.groupBy("InvoiceNo").agg(
  count("Quantity").alias("quan"),
  expr("count(Quantity)")).show()
```

실행결과는 아래와 같습니다.

```scala
+---------+----+---------------+
|InvoiceNo|quan|count(Quantity)|
+---------+----+---------------+
|   536596|   6|              6|
...
|  C542604|   8|              8|
+---------+----+---------------+
```

### Grouping with Maps

칼럼을 Key 로, 수행할 집계 함수의 문자열을 Value 로 하는 Map 타입을 사용해 트랜스포메이션을 정의할 수 있습니다. 수행할 집계 함수를 한 줄로 작성하면 여러 칼럼명을 재사용할 수 있습니다.


```scala
// in Scala
df.groupBy("InvoiceNo").agg("Quantity"->"avg", "Quantity"->"stddev_pop").show()
```

```sql
-- in SQL
SELECT avg(Quantity), stddev_pop(Quantity), InvoiceNo FROM dfTable
GROUP BY InvoiceNo
```

실행결과는 아래와 같습니다.

```scala
+---------+------------------+--------------------+
|InvoiceNo|     avg(Quantity)|stddev_pop(Quantity)|
+---------+------------------+--------------------+
|   536596|               1.5|  1.1180339887498947|
...
|  C542604|              -8.0|  15.173990905493518|
+---------+------------------+--------------------+
```

## Window Functions

**윈도우 함수(Window Function)** 를 집계에 사용할 수 있습니다. 윈도우 함수는 데이터의 특정 윈도우를 대상으로 고유의 집계 연산을 수행합니다. 데이터의 윈도우는 현재 데이터에 대한 참조를 정의해 사용합니다.

**윈도우 명세(Window Specification)** 는 함수에 전달될 로우를 결정합니다. 표준 `group-by` 함수와 유사해보일 수 있으니 차이를 알아보겠습니다.

`group-by` 함수는 모든 로우 레코드가 단일 그룹으로만 이동합니다. 윈도우 함수는 프레임에 입력되는 모든 로우에 대해 결괏값을 계산합니다. 프레임은 로우 기반의 테이블을 의미합니다. 각 로우는 하나 이상의 프레임에 할당 될 수 있습니다.

가장 흔하게 사용되는 방법 중 하난는 하루를 나타내는 값의 **롤링 평균(Rolling Average)** 를 구하는 겁니다. 이 자겅ㅂ을 수행하려면 개별 로우가 7 개의 다른 프레임으로 구성되어야 합니다. 프레임을 정의하는 방법은 잠시 후 알아보겠습니다.

Spark 는 3 가지 종류의 윈도우 함수를 지원합니다.

* Ranking Function
* Analytic Function
* Aggregate Function

`Example 1` 은 로우가 어떻게 여러 프레임에 할당될 수 있는지를 나타냅니다.

> Example 1 - Visualizing window functions

![image](https://user-images.githubusercontent.com/44635266/78028819-929ad580-739a-11ea-8d74-d7dc06f18bf4.png)

예제를 위해 주문 일자 (`InvoiceDate`) 컬럼을 변환해 `date` 컬럼을 만듭니다. 이 칼럼은 시간 정보를 제외한 날짜 정보만 가집니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{col, to_date}
val dfWithDate = df.withColumn("date", to_date(col("InvoiceDate"),
  "MM/d/yyyy H:mm"))
dfWithDate.createOrReplaceTempView("dfWithDate")
```

윈도우 함수를 정의하기 위해 첫 번재 단계로 윈도우 명세를 만듭니다. 아래에서 사용하는 `partitionBy` 메소드는 지금까지 사용한 파티셔닝 스키마의 개념과는 관련이 없으며 그룹을 어떻게 나눌지 결정하는것과 유사한 개념입니다. 

`orderBy` 메소드는 파티션의 정렬 방식을 정의합니다. 프레임 명세는 입력된 로우의 참조를 기반으로 프레임에 로우가 포함될 수 잇는지 결정합니다. 아래 예제에서 첫 로우부터 현재 로우까지 확인합니다.

```scala
// in Scala
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.col

val windowSpec = Window
  .partitionBy("CustomerId", "date")
  .orderBy(col("Quantity").desc)
  .rowsBetween(Window.unboundedPreceding, Window.currentRow)
```

집계 함수를 사용하여 시간대별 최대 구매 개수를 구해보겠습니다. 그리고 이 함수를 적용할 데이터 프레임이 정의된 윈도우 명세도 함께 사용합니다.

```scala
import org.apache.spark.sql.functions.max

val maxPurchaseQuantity = max(col("Quantity")).over(windowSpec)
```

앞 예제는 칼럼이나 표현식을 반환하므로 DataFrame 의 `select` 구문에서 사용할 수 있습니다. 먼저 구매량 순위를 만들겠습니다. `dense_rank` 함수를 사용해 모든 고객에 대해 최대 구매 수량을 가진 날짜가 언제인지 알아보겠습니다.

동일한 값이 나오거나 중복 로우가 발생해 순위가 비어 있을 수 있으므로 `rank` 함수 대신 `dense_rank` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{dense_rank, rank}

val purchaseDenseRank = dense_rank().over(windowSpec)
val purchaseRank = rank().over(windowSpec)
```

이 예제 또한, `select` 구문에서 사용할 수 있는 칼럼을 반환합니다. 이제 `select` 메소드를 사용해 계산된 윈도우 값을 확인해보겠습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.col

dfWithDate.where("CustomerId IS NOT NULL").orderBy("CustomerId")
  .select(
    col("CustomerId"),
    col("date"),
    col("Quantity"),
    purchaseRank.alias("quantityRank"),
    purchaseDenseRank.alias("quantityDenseRank"),
    maxPurchaseQuantity.alias("maxPurchaseQuantity")).show()
```

```sql
-- in SQL
SELECT CustomerId, date, Quantity,
  rank(Quantity) OVER (PARTITION BY CustomerId, date
                       ORDER BY Quantity DESC NULLS LAST
                       ROWS BETWEEN
                         UNBOUNDED PRECEDING AND
                         CURRENT ROW) as rank,

  dense_rank(Quantity) OVER (PARTITION BY CustomerId, date
                             ORDER BY Quantity DESC NULLS LAST
                             ROWS BETWEEN
                               UNBOUNDED PRECEDING AND
                               CURRENT ROW) as dRank,

  max(Quantity) OVER (PARTITION BY CustomerId, date
                      ORDER BY Quantity DESC NULLS LAST
                      ROWS BETWEEN
                        UNBOUNDED PRECEDING AND
                        CURRENT ROW) as maxPurchase
FROM dfWithDate WHERE CustomerId IS NOT NULL ORDER BY CustomerId
```

실행결과는 아래와 같습니다.

```scala
+----------+----------+--------+------------+-----------------+---------------+
|CustomerId|      date|Quantity|quantityRank|quantityDenseRank|maxP...Quantity|
+----------+----------+--------+------------+-----------------+---------------+
|     12346|2011-01-18|   74215|           1|                1|          74215|
|     12346|2011-01-18|  -74215|           2|                2|          74215|
|     12347|2010-12-07|      36|           1|                1|             36|
|     12347|2010-12-07|      30|           2|                2|             36|
...
|     12347|2010-12-07|      12|           4|                4|             36|
|     12347|2010-12-07|       6|          17|                5|             36|
|     12347|2010-12-07|       6|          17|                5|             36|
+----------+----------+--------+------------+-----------------+---------------+
```

## Grouping Sets

칼럼의 값을 이용해 여러 칼럼을 집계하는 데 `group-by` 표현식을 사용했습니다. 때로는 여러 그룹에 걸쳐 집계할 수 있는 무언가가 필요합니다. **그룹화 셋(Grouping Set)** 이 바로 그 주인공입니다.

그룹화 셋은 여러 집계를 결합하는 저수준 기능입니다. 그룹화 셋을 이용하면 `group-by` 구문에서 원하는 형태로 집계를 생성할 수 있습니다.

다음 `stockCode` 와 `CustomerId` 별 총 수량을 출력해보겠습니다.

```scala
// in Scala
val dfNoNull = dfWithDate.drop()
dfNoNull.createOrReplaceTempView("dfNoNull")
```

```sql
-- in SQL
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode
ORDER BY CustomerId DESC, stockCode DESC
```

실행결과는 아래와 같습니다.

```scala
+----------+---------+-------------+
|CustomerId|stockCode|sum(Quantity)|
+----------+---------+-------------+
|     18287|    85173|           48|
|     18287|   85040A|           48|
|     18287|   85039B|          120|
...
|     18287|    23269|           36|
+----------+---------+-------------+
```

그룹화 셋을 사용해 동일한 작업을 수행할 수 있습니다.

```sql
-- in SQL
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode))
ORDER BY CustomerId DESC, stockCode DESC
```

```scala
+----------+---------+-------------+
|CustomerId|stockCode|sum(Quantity)|
+----------+---------+-------------+
|     18287|    85173|           48|
|     18287|   85040A|           48|
|     18287|   85039B|          120|
...
|     18287|    23269|           36|
+----------+---------+-------------+
```

고객이나 재고 코드에 상관없이 총 수량의 합산 결과를 추가하려하면 이야기는 달라집니다. `group-by` 구문을 사용해 처리하는 것은 불가능합니다. 

하지만 그룹화 셋을 사용하면 가능합니다. 단지 `GROUPING SETS` 구문에 집계 방식을 지정하면 됩니다. 이 과정은 여러 개의 그룹을 하나로 묶는 것과 같습니다.

```sql
-- in SQL
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode),())
ORDER BY CustomerId DESC, stockCode DESC
```

실행결과는 아래와 같습니다.

```scala
+----------+---------+-------------+
|customerId|stockCode|sum(Quantity)|
+----------+---------+-------------+
|     18287|    85173|           48|
|     18287|   85040A|           48|
|     18287|   85039B|          120|
...
|     18287|    23269|           36|
+----------+---------+-------------+
```

`GROUPING SETS` 구문은 SQL 에서만 사용할 수 있습니다. DataFrame 에서 동일한 연산을 수행하려면 `rollup` 메소드와 `cube` apthemfmf tkdydgkqslek.

### Rollups

아래는 시간(`Date`) 과 공간(`Country`) 을 축으로 하는 롤업을 생성합니다. 롤업의 결과로 생성된 DataFrame 은 모든 날짜의 총합, 날짜별 총합, 날짜별 국가별 총합을 포함합니다.

```scala
val rolledUpDF = dfNoNull.rollup("Date", "Country").agg(sum("Quantity"))
  .selectExpr("Date", "Country", "`sum(Quantity)` as total_quantity")
  .orderBy("Date")
rolledUpDF.show()
```

실행결과는 아래와 같습니다.

```scala
+----------+--------------+--------------+
|      Date|       Country|total_quantity|
+----------+--------------+--------------+
|      null|          null|       5176450|
|2010-12-01|United Kingdom|         23949|
|2010-12-01|       Germany|           117|
|2010-12-01|        France|           449|
...
|2010-12-03|        France|           239|
|2010-12-03|         Italy|           164|
|2010-12-03|       Belgium|           528|
+----------+--------------+--------------+
```

null 값을 가진 로우에서 전체 날짜의 합계를 확인할 수 있습니다. 롤업된 두 개의 칼럼값이 모두 null 인 로우는 두 칼럼에 속한 레코드의 전체 합계를 나타냅니다.

```scala
rolledUpDF.where("Country IS NULL").show()

rolledUpDF.where("Date IS NULL").show()
```

실행결과는 아래와 같습니다.

```scala
+----+-------+--------------+
|Date|Country|total_quantity|
+----+-------+--------------+
|null|   null|       5176450|
+----+-------+--------------+
```

### Cube

**큐브(Cube)** 는 롤업을 고차원적으로 사용할 수 있게 해줍니다. 큐브는 요소들을 계층적으로 다루는 대신 모든 차원에 대해 동일한 작업을 수행합니다. 즉, 전체 기간에 대해 날짜와 국가별 결과를 얻을 수 있습니다.

* The total across all dates and countries
* The total for each date across all countries
* The total for each country on each date
* The total for each country across all dates

메소드 호출 방식은 롤업과 매우 유사합니다.

```scala
// in Scala
dfNoNull.cube("Date", "Country").agg(sum(col("Quantity")))
  .select("Date", "Country", "sum(Quantity)").orderBy("Date").show()
```

실행결과는 아래와 같습니다.

```scala
+----+--------------------+-------------+
|Date|             Country|sum(Quantity)|
+----+--------------------+-------------+
|null|               Japan|        25218|
|null|            Portugal|        16180|
|null|         Unspecified|         3300|
|null|                null|      5176450|
|null|           Australia|        83653|
...
|null|              Norway|        19247|
|null|           Hong Kong|         4769|
|null|               Spain|        26824|
|null|      Czech Republic|          592|
+----+--------------------+-------------+
```

큐브를 사용해 테이블에 있는 모든 정보를 빠르고 쉽게 조회할 수 있는 요약 정보 테이블을 만들 수 있습니다.

### Grouping Metadata

큐브와 롤업을 사용하다 보면 집계 수준에 따라 쉽게 필터링하기 위해 집계 수준을 조회하는 경우가 발생합니다. 이때 `grouping_id` 를 사용합니다. `grouping_id` 는 결과 데이터셋의 집계 수준을 명시하는 칼럼을 제공합니다.

예제의 쿼리는 다음과 같은 네 개의 개별 그룹화 ID 값을 반환합니다.

|Grouping ID|Description|
|:--|:--|
|3|가장 높은 계층의 집계 결과에서 나타납니다. `customerId` 나 `stockCode` 에 관계 없이 총 수량을 제공|
|2|개별 재고 코드의 모든 집계 결과에서 나타납니다. `customerId` 에 관계없이 재고 코드별 총 수량을 제공|
|1|구매한 물품에 관계없이 `customerId` 를 기반으로 총 수량으로 제공|
|0|`customerId` 와 `stockCode` 별 조합에 따라 총 수량을 제공|

아래 예제를 보겠습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{grouping_id, sum, expr}

dfNoNull.cube("customerId", "stockCode").agg(grouping_id(), sum("Quantity"))
.orderBy(expr("grouping_id()").desc)
.show()
```

실행결과는 아래와 같습니다.

```
+----------+---------+-------------+-------------+
|customerId|stockCode|grouping_id()|sum(Quantity)|
+----------+---------+-------------+-------------+
|      null|     null|            3|      5176450|
|      null|    23217|            2|         1309|
|      null|   90059E|            2|           19|
...
+----------+---------+-------------+-------------+
```

### Pivot

**피벗(Pivot)** 을 사용해 로우를 칼럼으로 변환할 수 있습니다. 현재 데이터셋에는 `Country` 칼럼이 있습니다. 피벗을 사용해 국가별로 집계 함수를 적용할 수 있으며 쿼리를 사용해 쉽게 결과를 확인할 수 있습니다.

```scala
// in Scala
val pivoted = dfWithDate.groupBy("date").pivot("Country").sum()
```

DataFrame 은 국가명, 수치형 변수, 날짜를 나타내는 칼럼을 조합한 칼럼을 가집니다.

또한 집계를 수행하여 수치형 칼럼으로 나타납니다. 아래는 결과입니다.

```scala
pivoted.where("date > '2011-12-05'").select("date" ,"`USA_sum(Quantity)`").show()
```

```
+----------+-----------------+
|      date|USA_sum(Quantity)|
+----------+-----------------+
|2011-12-06|             null|
|2011-12-09|             null|
|2011-12-08|             -196|
|2011-12-07|             null|
+----------+-----------------+
```

이제 칼럼의 모든 값을 단일 그룹화하여 계산할 수 있습니다. 하지만 데이터를 탐색하는 방식에 따라 피벗을 수행한 결괏값이 감소할 수 있습니다.

특정 칼럼의 카디널리티가 낮다면 스키마와 쿼리 대상을 확인할 수 있도록 피벗을 사용해 다수의 칼럼으로 변환하는것이 좋습니다.

## User-Defined Aggregation Functions

**사용자 정의 집계 함수(User-Defined Aggregation Functions UDAF)** 는 직접 제작한 함수느 비즈니스 규칙에 기반을 둔 자체 집계 함수를 정의하는 방법입니다.

UDAF 를 사용해 입력 데이터 그룹에 직접 개발한 연산을 수행할 수 있습니다. Spark 는 입력 데이터의 모든 그룹의 중간 결과를 단일 AggregationBuffer 에 저장하여 관리합니다.

UDAF 를 생성하려면 기본 클래스인 UserDefinedAggregateFunction 을 상속받습니다. 그리고 다음과 같은 메소드를 정의합니다.

* inputSchema
  * UDAF 입력 파라미터의 스키마를 StructType 으로 정의
* bufferSchema
  * UDAF 중간 결과의 스키마를 StructType 으로 정의
* dataType
  * 변환될 값의 DataType 을 정의
* deterministic
  * UDAF 가 동일한 입력값에 대해 항상 동일한 결과를 반환하는지 불리언값으로 정의
* initialize
  * 집계용 버퍼의 값을 초기화하는 로직을 정의
* update
  * 입력받은 로우를 기반으로 내부 버퍼를 업데이트하는 로직을 정의
* merge
  두 개의 집계용 버퍼를 병합하는 로직을 정의
* evaluate
  * 집계의 최종 결과를 생성하는 로직을 정의

아래 예제는 입력된 모든 로우의 칼럼이 true 인지 판단하는 `BoolAnd` 클래스입니다. 하나의 칼럼이라도 true 가 아니면 false 를 반환합니다.

```scala
// in Scala
import org.apache.spark.sql.expressions.MutableAggregationBuffer
import org.apache.spark.sql.expressions.UserDefinedAggregateFunction
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
class BoolAnd extends UserDefinedAggregateFunction {
  def inputSchema: org.apache.spark.sql.types.StructType =
    StructType(StructField("value", BooleanType) :: Nil)
  def bufferSchema: StructType = StructType(
    StructField("result", BooleanType) :: Nil
  )
  def dataType: DataType = BooleanType
  def deterministic: Boolean = true
  def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = true
  }
  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    buffer(0) = buffer.getAs[Boolean](0) && input.getAs[Boolean](0)
  }
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getAs[Boolean](0) && buffer2.getAs[Boolean](0)
  }
  def evaluate(buffer: Row): Any = {
    buffer(0)
  }
}
```

클래스를 초기화하고 함수로 등록합니다.

```scala
// in Scala
val ba = new BoolAnd
spark.udf.register("booland", ba)

import org.apache.spark.sql.functions._

spark.range(1)
  .selectExpr("explode(array(TRUE, TRUE, TRUE)) as t")
  .selectExpr("explode(array(TRUE, FALSE, TRUE)) as f", "t")
  .select(ba(col("t")), expr("booland(f)"))
  .show()
```

실행결과는 아래와 같습니다.

```
+----------+----------+
|booland(t)|booland(f)|
+----------+----------+
|      true|     false|
+----------+----------+
```

UDAF 는 Scala 와 Java 로만 사용할 수 있습니다.