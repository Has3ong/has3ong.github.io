---
title : Spark Working with Different Types of Data
tags :
- Type
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

Spark 에서는 아래와 같이 다양한 데이터 타입이 있습니다.

* Booleans
* Numbers
* Strings
* Dates and timestamps
* Handling null
* Complex types
* User-defined functions

## Where to Look for APIs

Spark 의 데이터 변환용 함수를 찾기 위해 핵심적으로 보아야 할 부분은 다음과 같습니다.

* DataFrame(Dataset) Method
* Column Method

모든 함수는 데이터 로우의 특정 포맷이나 구조를 다른 형태로 변환하기 위해 존재합니다. 함수를 사용해 더 많은 로우를 만들거나 줄일 수 있습니다.

다음은 분석에 사용할 DataFrame 을 생성하는 예제입니다.

```scala
// in Scala
val df = spark.read.format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/data/retail-data/by-day/2010-12-01.csv")
df.printSchema()
df.createOrReplaceTempView("dfTable")
```

스키마와 데이터 슴팰은 다음과 같습니다.

```scala
root
|-- InvoiceNo: string (nullable = true)
|-- StockCode: string (nullable = true)
|-- Description: string (nullable = true)
|-- Quantity: integer (nullable = true)
|-- InvoiceDate: timestamp (nullable = true)
|-- UnitPrice: double (nullable = true)
|-- CustomerID: double (nullable = true)
|-- Country: string (nullable = true)

+---------+---------+--------------------+--------+-------------------+----...
|InvoiceNo|StockCode|Description         |Quantity|InvoiceDate        |Unit...
+---------+---------+--------------------+--------+-------------------+----...
|   536365|   85123A|WHITE HANGING HEA...|       6|2010-12-01 08:26:00|    ...
|   536365|    71053| WHITE METAL LANTERN|       6|2010-12-01 08:26:00|    ...
...
|   536367|    21755|LOVE BUILDING BLO...|       3|2010-12-01 08:34:00|    ...
|   536367|    21777|RECIPE BOX WITH M...|       4|2010-12-01 08:34:00|    ...
+---------+---------+--------------------+--------+-------------------+----...
```

## Converting to Spark Types

Scala 데이터 타입을 Spark 데이터 타이븡로 변환해보겠습니다. 데이터 타입 변환은 `list` 함수를 사용합니다.`list` 함수는 다른 언어의 데이터 타입을 Spark 데이터 타입에 맞게 변환합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.lit

df.select(lit(5), lit("five"), lit(5.0))
```

SQL 에서는 Spark 데이터 타입으로 변환할 필요가 없으므로 직접 입력해 사용합니다.

```sql
-- in SQL
SELECT 5, "five", 5.0
```

## Working with Booleans

불리언은 모든 필터링 작업의 기반이므로 데이터 분석에 필수입니다. 불리언 구문은 `and`, `or`, `true`, `false` 로 구성됩니다.

소매 데이터셋을 사용해 불리언을 다루어보겠습니다. 불리언 식에는 일치 조건뿐만 아니라 비교 연산 조건을 사용할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.col

df.where(col("InvoiceNo").equalTo(536365))
  .select("InvoiceNo", "Description")
  .show(5, false)
```

> Scala 에서 `==` 와 `===` 은 특별한 의미가 있습니다. Spark 에서 동등 여부를 판별해 필터링하려면 일치를 나타내는 `===` 나 불일치를 나타내는 `=!=` 를 사용해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.col
df.where(col("InvoiceNo") === 536365)
  .select("InvoiceNo", "Description")
  .show(5, false)
```

실행 결과는 다음과 같습니다.

```scala
+---------+-----------------------------+
|InvoiceNo|Description                  |
+---------+-----------------------------+
|  536366 |HAND WARMER UNION JACK       |
...
|  536367 |POPPY'S PLAYHOUSE KITCHEN    |
+---------+-----------------------------+
```

가장 명확한 방법은 문자열 표현식에 조건절을 명시하는 겁니다. Scala 에서 사용할 수 있으며, 다음과 같이 일치하지 않음을 표현할 수 있습니다.

```scala
df.where("InvoiceNo = 536365")
  .show(5, false)

df.where("InvoiceNo <> 536365")
  .show(5, false)
```

`and` 메소드나 `or` 메소드를 사용해 불리언 표현식을 여러 부분에 지정할 수 있습니다. 불리언 표현식을 사용하는 경우 항상 모든 표현식을 `and` 로 묵어서 차례대로 필터를 적용해야 합니다.

불리언 문을 차례대로 표현하더라도 Spark 는 내부적으로 `and` 구문을 필터 사이에 추가해 모든 필터를 하나의 문장으로 변환합니다. 그 다음 동시에 모든 필터를 처리합니다. 원하면 `and` 구문으로 조건문을 만들 수 있습니다. 하지만 차례로 조건을 나열하면 이해하기 쉽고 읽기도 편해집니다.

반면 `or` 구문을 사용할 때는 반드시 동일한 구문에 조건을 정의해야합니다.

```scala
// in Scala
val priceFilter = col("UnitPrice") > 600
val descripFilter = col("Description").contains("POSTAGE")
df.where(col("StockCode").isin("DOT")).where(priceFilter.or(descripFilter))
  .show()
```

```sql
-- in SQL
SELECT * FROM dfTable WHERE StockCode in ("DOT") AND(UnitPrice > 600 OR
instr(Description, "POSTAGE") >= 1)
```

결과는 아래와 같습니다.

```scala
+---------+---------+--------------+--------+-------------------+---------+...
|InvoiceNo|StockCode|   Description|Quantity|        InvoiceDate|UnitPrice|...
+---------+---------+--------------+--------+-------------------+---------+...
|   536544|      DOT|DOTCOM POSTAGE|       1|2010-12-01 14:32:00|   569.77|...
|   536592|      DOT|DOTCOM POSTAGE|       1|2010-12-01 17:06:00|   607.49|...
+---------+---------+--------------+--------+-------------------+---------+...
```

불리언 표현식을 필터링 조건에만 사용하는 것이 아니라 칼럼을 사용해 DataFrame 을 필터링할 수 있습니다.

```scala
// in Scala
val DOTCodeFilter = col("StockCode") === "DOT"
val priceFilter = col("UnitPrice") > 600
val descripFilter = col("Description").contains("POSTAGE")
df.withColumn("isExpensive", DOTCodeFilter.and(priceFilter.or(descripFilter)))
  .where("isExpensive")
  .select("unitPrice", "isExpensive").show(5)
```

```sql
-- in SQL
SELECT UnitPrice, (StockCode = 'DOT' AND
  (UnitPrice > 600 OR instr(Description, "POSTAGE") >= 1)) as isExpensive
FROM dfTable
WHERE (StockCode = 'DOT' AND
  (UnitPrice > 600 OR instr(Description, "POSTAGE") >= 1))
```

모든 구문은 SQL `where` 절로 표현할 수 있습니다. 필터를 표현해야 한다면 DataFrame 인터페이스 방식보다 SQL 이 더 쉽습니다. Spark SQL 을 사용한다 해서 성능 저하가 발생하지 않습니다.

예를 들어 다음 두 문장은 동일하게 처리합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{expr, not, col}

df.withColumn("isExpensive", not(col("UnitPrice").leq(250)))
  .filter("isExpensive")
  .select("Description", "UnitPrice").show(5)
df.withColumn("isExpensive", expr("NOT UnitPrice <= 250"))
  .filter("isExpensive")
  .select("Description", "UnitPrice").show(5)
```

## Working with Numbers

**카운트(count)** 는 빅데이터 처리에서 필터링 다음으로 많이 수행되는 작업입니다. 대부분 수치형 데이터 타입을 사용해 연산 방식을 정의하기만 하면 됩니다.

대표적인 예로는 제곱을 계산할 수 있는 `pow` 함수가 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{expr, pow}

val fabricatedQuantity = pow(col("Quantity") * col("UnitPrice"), 2) + 5
df.select(expr("CustomerId"), fabricatedQuantity.alias("realQuantity")).show(2)
```

```scala
+----------+------------------+
|CustomerId|      realQuantity|
+----------+------------------+
|   17850.0|239.08999999999997|
|   17850.0|          418.7156|
+----------+------------------+
```

두 칼럼 모두 수치형이므로 곱셈 연산이 가능합니다. 그리고 덧셈이나 뺄셈도 가능합니다. SQL 을 사용하게 동일하기 처리할 수 있습니다.

```scala
// in Scala
df.selectExpr(
  "CustomerId",
  "(POWER((Quantity * UnitPrice), 2.0) + 5) as realQuantity").show(2)
```

```sql
-- in SQL
SELECT customerId, (POWER((Quantity * UnitPrice), 2.0) + 5) as realQuantity
FROM dfTable
```

반올림도 자주 사용하는 수치형 작업 중 하나입니다. 때로는 소수점 자리를 없애기 위해 Integer 데이터 타입으로 형변환하기도 합니다. Spark 는 정확한 계산이 가능한 함수를 제공합니다. 그리고 정밀도를 사용해 더 세밀한 작업을 수행할 수 있습니다. 다음은 소수점 첫째 자리에서 반올림하는 예제입니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{round, bround}

df.select(round(col("UnitPrice"), 1).alias("rounded"), col("UnitPrice")).show(5)
```

기본적으로 `round` 함수는 소수점 값이 정확히 중간값 이상이라면 반올림합니다. 내림은 `bround` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.lit

df.select(round(lit("2.5")), bround(lit("2.5"))).show(2)
```

```sql
-- in SQL
SELECT round(2.5), bround(2.5)
```

실행결과는 아래와 같습니다.

```scala
+-------------+--------------+
|round(2.5, 0)|bround(2.5, 0)|
+-------------+--------------+
|          3.0|           2.0|
|          3.0|           2.0|
+-------------+--------------+
```

두 칼럼 사이의 상관관계를 계산하는 것도 수치형 연산 작업 중 하나입니다. 예를 들어 고객이 비싼 물건보다 저렴한 물건을 더 많이 구매하는지 알기 위해 두 칼럼에 대한 피어슨 상관계수를 계산할 필요가 있습니다. 다음 예제와 같이 DataFrame 의 통계용 함수나 메소드를 사용해 피어슨 상관 계수를 계산할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{corr}

df.stat.corr("Quantity", "UnitPrice")
df.select(corr("Quantity", "UnitPrice")).show()
```

```sql
-- in SQL
SELECT corr(Quantity, UnitPrice) FROM dfTabl
```

실행결과는 아래와 같습니다.

```scala
+-------------------------+
|corr(Quantity, UnitPrice)|
+-------------------------+
|     -0.04112314436835551|
+-------------------------+
```

요약 통계는 `describe` 메소드를 사용해 얻을 수 있습니다. `describe` 메소드는 관련 칼럼에 대한 집계(count), 평균(mean), 표준편차(stddev), 최소 값(min), 최댓값(max) 을 계산합니다.

```scala
// in Scala
df.describe().show()
```

실행결과는 아래와 같습니다.

```scala
+-------+------------------+------------------+------------------+
|summary|          Quantity|         UnitPrice|        CustomerID|
+-------+------------------+------------------+------------------+
|  count|              3108|              3108|              1968|
|   mean| 8.627413127413128| 4.151946589446603|15661.388719512195|
| stddev|26.371821677029203|15.638659854603892|1854.4496996893627|
|    min|               -24|               0.0|           12431.0|
|    max|               600|            607.49|           18229.0|
+-------+------------------+------------------+------------------+
```

정확한 수치가 필요하다면 함수를 임포트하고 해당 칼럼에 적용하는 방식으로 직접 집계를 수행할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{count, mean, stddev_pop, min, max}
```

StatFunctions 패키지는 다양한 통계 함수를 제공합니다. `stat` 속성을 사용해 접근할 수 있으며 다양한 통곗값을 계산할 때 사용하는 DataFrame 메소드입니다. 예를 들어 `approxQuantile` 메소드를 사용해 데이터의 백분위수를 정확하게 계산하거나 근사치를 계산할 수 있습니다.

```scala
// in Scala

val colName = "UnitPrice"
val quantileProbs = Array(0.5)
val relError = 0.05

df.stat.approxQuantile("UnitPrice", quantileProbs, relError) // 2.51
```

StatFunctions 패키지는 교차표나 자주 사용하는 항목 쌍을 확인하는 용도의 메소드도 제공합니다.

```scala
// in Scala
df.stat.crosstab("StockCode", "Quantity").show()

// in Scala
df.stat.freqItems(Seq("StockCode", "Quantity")).show()
```

마지막으로 `monotonically_increasing_id` 함수는 모든 로우에 고유 ID 값을 추가합니다. 이 함수는 모든 로우에 0 부터 시작하는 고윳값을 생성합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.monotonically_increasing_id

df.select(monotonically_increasing_id()).show(2)
```

## Working with Strings

문자열을 다루는 작업은 모든 데이터 처리 과정에서 발생합니다. 그러므로 문자열을 다루는 방법을 알아야 합니다. 로그 파일에 정규 표현식을 사용해 데이터 추출, 데이터 치환, 문자열 존재 여부, 대 / 소문자 변화나 처리 등의 작업을 할 수 있습니다.

대 / 소문자 변호나 작업부터 시작하겠습니다. `initcap` 함수는 주어진 문자열에서 공백으로 나뉘는 모든 단어의 첫 글자를 대문자로 변경합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{initcap}

df.select(initcap(col("Description"))).show(2, false)
```

```sql
-- in SQL
SELECT initcap(Description) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+----------------------------------+
|initcap(Description)              |
+----------------------------------+
|White Hanging Heart T-light Holder|
|White Metal Lantern               |
+----------------------------------+
```

`lower`, `upper` 함수를 사용해 문자열 전체를 소문자로 변경하거나 대문자로 변경할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{lower, upper}

df.select(col("Description"),
  lower(col("Description")),
  upper(lower(col("Description")))).show(2)
```

```sql
-- in SQL
SELECT Description, lower(Description), Upper(lower(Description)) FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+--------------------+--------------------+-------------------------+
|         Description|  lower(Description)|upper(lower(Description))|
+--------------------+--------------------+-------------------------+
|WHITE HANGING HEA...|white hanging hea...|     WHITE HANGING HEA...|
| WHITE METAL LANTERN| white metal lantern|      WHITE METAL LANTERN|
+--------------------+--------------------+-------------------------+
```

문자열 주변의 공백을 제거하거나 추가하는 작업도 가능합니다. 이 작업은 `lpad`, `ltrim`, `rpad`, `rtrim`, `trim` 함수를 사용합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{lit, ltrim, rtrim, rpad, lpad, trim}

df.select(
  ltrim(lit(" HELLO ")).as("ltrim"),
  rtrim(lit(" HELLO ")).as("rtrim"),
  trim(lit(" HELLO ")).as("trim"),
  lpad(lit("HELLO"), 3, " ").as("lp"),
  rpad(lit("HELLO"), 10, " ").as("rp")).show(2)
```

```sql
-- in SQL
SELECT
  ltrim(' HELLLOOOO '),
  rtrim(' HELLLOOOO '),
  trim(' HELLLOOOO '),
  lpad('HELLOOOO ', 3, ' '),
  rpad('HELLOOOO ', 10, ' ')
FROM dfTable
```

실행결과는 아래와 같습니다.

```scala
+---------+---------+-----+---+----------+
|    ltrim|    rtrim| trim| lp|        rp|
+---------+---------+-----+---+----------+
|   HELLO |    HELLO|HELLO| HE|    HELLO |
|   HELLO |    HELLO|HELLO| HE|    HELLO |
+---------+---------+-----+---+----------+
```

`lpad` 함수나 `rpad` 함수에 문자열의 길이보다 작은 숫자를 넘기면 문자열의 오른쪽부터 제거됩니다.

### Regular Expressions

문자열의 존재 여부를 확인하거나 모든 문자열을 치환할 때는 보통 **정규 표현식(Regular Expression)** 을 사용합니다. 정규 표현식을 사용해 문자열에서 값을 추출하거나 다른 값으로 치환하는 데 필요한 규칙 모음을 정의할 수 있습니다.

Spark 는 Java 정규 표현식이 가진 강력한 능력을 활용합니다. Spark 는 정규 표현식을 위해 `regexp_extract` 함수와 `regexp_replace` 함수를 제공합니다. 이 함수들은 값을 추출하고 치환하는 역할을 합니다.

`regexp_replace` 함수를 사용해 `decription` 칼럼의 값을 `COLOR` 로 치환해보겠습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.regexp_replace

val simpleColors = Seq("black", "white", "red", "green", "blue")
val regexString = simpleColors.map(_.toUpperCase).mkString("|")
// the | signifies `OR` in regular expression syntax
df.select(
  regexp_replace(col("Description"), regexString, "COLOR").alias("color_clean"),
  col("Description")).show(2)
```

```sql
-- in SQL
SELECT
  regexp_replace(Description, 'BLACK|WHITE|RED|GREEN|BLUE', 'COLOR') as
  color_clean, Description
FROM dfTable
```

실행 결과는 아래와 같습니다.

```scala
+--------------------+--------------------+
|         color_clean|         Description|
+--------------------+--------------------+
|COLOR HANGING HEA...|WHITE HANGING HEA...|
| COLOR METAL LANTERN| WHITE METAL LANTERN|
+--------------------+--------------------+
```

주어진 문자를 다른 문자로 치환해야할 때 있습니다. `translate` 를 이용해 치환해보겠습니다. 이 연산은 문자 단위로 이루어집니다. 교체 문자열에서 색인된 문자에 해당하는 모든 문자를 치환합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.translate

df.select(translate(col("Description"), "LEET", "1337"), col("Description"))
  .show(2)
```

```sql
-- in SQL
SELECT translate(Description, 'LEET', '1337'), Description FROM dfTable
```

실행 결과는 아래와 같습니다.

```scala
+----------------------------------+--------------------+
|translate(Description, LEET, 1337)|         Description|
+----------------------------------+--------------------+
|              WHI73 HANGING H3A...|WHITE HANGING HEA...|
|               WHI73 M37A1 1AN73RN| WHITE METAL LANTERN|
+----------------------------------+--------------------+
```

처음 나타난 색상 이름을 추출하는 것과 같은 작업을 수행할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.regexp_extract

val regexString = simpleColors.map(_.toUpperCase).mkString("(", "|", ")")
// the | signifies OR in regular expression syntax
df.select(
  regexp_extract(col("Description"), regexString, 1).alias("color_clean"),
  col("Description")).show(2)
```

```sql
-- in SQL
SELECT regexp_extract(Description, '(BLACK|WHITE|RED|GREEN|BLUE)', 1),
  Description
FROM dfTable
```

실행 결과는 아래와 같습니다.

```scala
+-------------+--------------------+
|  color_clean|         Description|
+-------------+--------------------+
|        WHITE|WHITE HANGING HEA...|
|        WHITE| WHITE METAL LANTERN|
+-------------+--------------------+
```

때로는 값 추출 없이 단순히 값의 존재 여부를 확인하고 싶을 때가 있습니다. 이때 `contains` 메소드를 사용합니다. 이 메소드는 인수로 입력된 값이 칼럼의 문자열에 존재하는지 불리언 타입으로 반환합니다.

```scala
// in Scala
val containsBlack = col("Description").contains("BLACK")
val containsWhite = col("DESCRIPTION").contains("WHITE")

df.withColumn("hasSimpleColor", containsBlack.or(containsWhite))
  .where("hasSimpleColor")
  .select("Description").show(3, false)
```

```sql
-- in SQL
SELECT Description FROM dfTable
WHERE instr(Description, 'BLACK') >= 1 OR instr(Description, 'WHITE') >= 1
```

실행 결과는 아래와 같습니다.

```scala
+----------------------------------+
|Description                       |
+----------------------------------+
|WHITE HANGING HEART T-LIGHT HOLDER|
|WHITE METAL LANTERN               |
|RED WOOLLY HOTTIE WHITE HEART.    |
+----------------------------------+
```

위 예제는 값을 두 개만 사용하므로 간단해보이지만, 값의 개수가 늘어나면 복잡해집니다.

동적으로 인수의 개수가 변하는 상황을 Spark 가 어떻게 처리하는지 알아보겠습니다. 값 목록을 인수로 변환해 함수에 전달할 때는 `varargs` 라 불리는 Scala 고유 기능을 활용합니다.

이 기능을 사용해 임의 길이의 배열을 효율적으로 다룰 수 있습니다. 예를 들어 `select` 메소드와 `varargs` 를 함께 사용해 원하는 만큼 동적으로 칼럼을 생성할 수 있습니다.

```scala
// in Scala
val simpleColors = Seq("black", "white", "red", "green", "blue")
val selectedColumns = simpleColors.map(color => {

  col("Description").contains(color.toUpperCase).alias(s"is_$color")
}):+expr("*") // could also append this value

df.select(selectedColumns:_*).where(col("is_white").or(col("is_red")))
  .select("Description").show(3, false)
```

실행 결과는 아래와 같습니다.

```scala
+----------------------------------+
|Description                       |
+----------------------------------+
|WHITE HANGING HEART T-LIGHT HOLDER|
|WHITE METAL LANTERN               |
|RED WOOLLY HOTTIE WHITE HEART.    |
+----------------------------------+
```

`locate` 함수는 쉽게 확장할 수 있습니다. 따라서 칼럼이나 불리언 필터를 프로그래밍 방식으로 생성할 수 있습니다. 예를 들어 `locate` 함수를 확장해 입력값의 최소공배수를 구하거나 소수 여부를 판별할 수 있습니다.

## Working with Dates and Timestamps

Spark 는 두 가지 종류의 시간 관련 정보만 관리합니다. 하나는 달력 형태의 날짜(date) 이고, 다른 하나는 날짜와 시간 정보를 모두 가지는 타임스탬프(timestamp) 입니다. 

Spark 는 `inferSchema` 옵션이 활성화된 경우 날짜와 타임 스탬프를 포함해 칼럼의 데이터 타입을 최대한 정확하게 식별하려 시도합니다. Spark 는 특정 날짜 포맷을 명시하지 않아도 자체적으로 식별해 데이터를 읽을 수 있습니다. 따라서 예제의 데이터셋이 잘 동작하는 것을 확인할 수 있습니다.

Spark 는 특정 시점에 데이터 포맷이 약간 특이하게 변할 수 있습니다. 이 문제를 피하려면 파싱이나 변환 작업을 해야 합니다. Spark 는 Java 의 날짜와 타임스탬프를 사용해서 표준 체계를 따릅니다. 다음은 오늘 날짜와 현재 타임스탬프값을 구하는 예제입니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{current_date, current_timestamp}

val dateDF = spark.range(10)
  .withColumn("today", current_date())
  .withColumn("now", current_timestamp())
dateDF.createOrReplaceTempView("dateTable")
```

실행 결과는 아래와 같습니다.

```scala
root
  |-- id: long (nullable = false)
  |-- today: date (nullable = false)
  |-- now: timestamp (nullable = false)
```

위 예제로 만들어진 DataFrame 을 사용해 오늘을 기준으로 5 일 전후의 날짜를 구현해보겠습니다. `date_sum` 함수와 `date_add` 함수는 칼럼과 더하거나 뺄 날자 수를 인수로 전달해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{date_add, date_sub}

dateDF.select(date_sub(col("today"), 5), date_add(col("today"), 5)).show(1)
```

```sql
-- in SQL
SELECT date_sub(today, 5), date_add(today, 5) FROM dateTable
```

실행 결과는 아래와 같습니다.

```scala
+------------------+------------------+
|date_sub(today, 5)|date_add(today, 5)|
+------------------+------------------+
|        2017-06-12|        2017-06-22|
+------------------+------------------+
```

두 날자짜의 차이를 구하는 작업도 자주 발생합니다. 두 날짜 사이의 일 수를 반환하는 `datediff` 함수를 사용해 이 작업을 수행할 수 있습니다. 월별로 일수가 다르므로 날짜만 신경쓰는 경우가 많지만, 두 날짜 사이의 개월 수를 반환하는 `months_between` 함수도 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{datediff, months_between, to_date}

dateDF.withColumn("week_ago", date_sub(col("today"), 7))
  .select(datediff(col("week_ago"), col("today"))).show(1)

dateDF.select(
    to_date(lit("2016-01-01")).alias("start"),
    to_date(lit("2017-05-22")).alias("end"))
  .select(months_between(col("start"), col("end"))).show(1)
```

```sql
-- in SQL
SELECT to_date('2016-01-01'), months_between('2016-01-01', '2017-01-01'),
datediff('2016-01-01', '2017-01-01')
FROM dateTable
```

실행 결과는 아래와 같습니다.

```scala
+-------------------------+
|datediff(week_ago, today)|
+-------------------------+
|                       -7|
+-------------------------+

+--------------------------+
|months_between(start, end)|
+--------------------------+
|              -16.67741935|
+--------------------------+
```

`to_date` 함수는 문자열을 날짜로 변환할 수 있으며, 필요에 따라 날짜 포맷도 함께 지정할 수 있습니다. 함수의 날짜 포맷은 반드시 Java 의 `SimpleDateFormat` 클래스가 지원하는 포맷을 사용해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{to_date, lit}

spark.range(5).withColumn("date", lit("2017-01-01"))
  .select(to_date(col("date"))).show(1)
```

Spark 는 날짜를 파싱할 수 없다면 에러 대신 null 값을 반환합니다. 그래서 다단계 처리 파이프라인에서 까다로울 수 있습니다. 데이터 포맷이 지정된 데이터에서 또 다른 포맷의 데이터가 나올 수 있기 때문입니다. 

년-월-일 형태가 아닌 년-일-월 형태의 날짜 포맷을 사용해보겠습니다. Spark 는 날짜를 파싱할 수 없으므로 null 값을 반환합니다.

```scala
dateDF.select(to_date(lit("2016-20-12")),to_date(lit("2017-12-11"))).show(1)

+-------------------+-------------------+
|to_date(2016-20-12)|to_date(2017-12-11)|
+-------------------+-------------------+
|               null|         2017-12-11|
+-------------------+-------------------+
```

날짜(2017-12-11) 가 의도한 날짜인 11-12 대신 12-11 로 표시되었습니다. Spark 는 날짜가 뒤섞여 있거나 데이터가 잘못되었는지 판단할 수 없으므로 오류를 발생시키지 않습니다.

문제를 해결하기 위해 `to_date` 와 `to_timestamp` 함수를 사용합니다. `to_timestamp` 함수는 반드시 날짜 포맷을 지정해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.to_date

val dateFormat = "yyyy-dd-MM"
val cleanDateDF = spark.range(1).select(
  to_date(lit("2017-12-11"), dateFormat).alias("date"),
  to_date(lit("2017-20-12"), dateFormat).alias("date2"))
cleanDateDF.createOrReplaceTempView("dateTable2")
```

```sql
-- in SQL
SELECT to_date(date, 'yyyy-dd-MM'), to_date(date2, 'yyyy-dd-MM'), to_date(date)
FROM dateTable2
```

실행 결과는 아래와 같습니다.

```scala
+----------+----------+
|      date|     date2|
+----------+----------+
|2017-11-12|2017-12-20|
+----------+----------+
```

항상 날짜 포맷을 지장해야 하는 `to_timestamp` 함수의 예제를 살펴보겠습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.to_timestamp

cleanDateDF.select(to_timestamp(col("date"), dateFormat)).show()
```

```sql
-- in SQL
SELECT to_timestamp(date, 'yyyy-dd-MM'), to_timestamp(date2, 'yyyy-dd-MM')
FROM dateTable2
```

실행 결과는 아래와 같습니다.

```scala
+----------------------------------+
|to_timestamp(`date`, 'yyyy-dd-MM')|
+----------------------------------+
|               2017-11-12 00:00:00|
+----------------------------------+
```

모든 언어에서 날짜와 타임스탬프 간의 변환은 간단합니다. SQL 에서는 다음과 같은 방식을 사용합니다.

```sql
-- in SQL
SELECT cast(to_date("2017-01-01", "yyyy-dd-MM") as timestamp)
```

올바른 포맷과 타입의 날짜나 타임스탬프를 사용한다면 매우 쉽게 비교할 수 있습니다. 날짜를 비교할 때는 날짜나 타임스탬프 타입을 사용하거나 **yyyy-mm-dd** 포맷에 맞는 문자열을 지정합니다.

```scala
cleanDateDF.filter(col("date2") > lit("2017-12-12")).show()
```

Spark 가 리터럴로 인식하는 문자열을 지정해 날짜를 비교할 수도 있습니다.

```scala
cleanDateDF.filter(col("date2") > "'2017-12-12'").show()
```

## Working with Nulls in Data

DataFrame 에서 빠져 있거나 비어 있는 데이터를 표현할 때는 항상 null 값을 사용하는 것이 좋습니다. Spark 에서 빈 문자열이나 대체 값 대신 null 값을 사용해야 최적화를 수행할 수 있습니다.

null 값을 다루는 두 가지 방법이 있습니다. 명시적으로 null 값을 제거하거나, 전역 또는 칼럼 단위로 null 값을 특정 값으로 채워 넣는 겁니다. 두 가지 방법을 알아보겠습니다.

### Coalesce

Spark 의 `coalesce` 함수는 이수로 지정한 여러 칼럼중 null 이 아닌 첫 번째 값을 반환합니다. 모든 칼럼이 null 이 아닌 값을 가지는 첫 번째 칼럼의 값을 반환합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.coalesce

df.select(coalesce(col("Description"), col("CustomerId"))).show()
```

### ifnull, nullIf, nvl, and nvl2

`coalesce` 함수와 유사한 결과를 얻을 수 있는 SQL 함수가 있습니다. `ifnull` 함수는 첫 번째 값이 null 이면 두 번째 값을 반환합니다. 첫 번째 값이 null 이 아니면 첫 번째 값을 반환합니다.

반면 `nullif` 함수는 두 값이 같으면 null 을 반환합니다. 두 값이 다르면 첫 번째 값을 반환합니다. 

`nvl` 함수는 첫 번째 값이 null 이면 두 번째 값을 반환합니다. 첫 번째 값이 null 이 아니면 첫 번째 값을 반환합니다.

`nvl2` 함수는 첫 번째 값이 null 이 아니면 두 번째 값을 반환합니다. 그리고 첫 번째 값이 null 이면 세 번째 인수로 지정된 값을 반환합니다.

```sql
-- in SQL
SELECT
  ifnull(null, 'return_value'),
  nullif('value', 'value'),
  nvl(null, 'return_value'),
  nvl2('not_null', 'return_value', "else_value")
FROM dfTable LIMIT 1

+------------+----+------------+------------+
|           a|   b|           c|           d|
+------------+----+------------+------------+
|return_value|null|return_value|return_value|
+------------+----+------------+------------+
```

이 함수들은 DataFrame 의 `select` 표현식으로 사용할 수 있습니다.

### drop

`drop` 메소드는 null 값을 가진 로우를 제거하는 가장 간단한 함수입니다. 기본적으로 null 값을 가지는 모든 로우를 제거합니다.

```scala
df.na.drop()
df.na.drop("any")
```

SQL 을 사용한다면 칼럼별로 수행해야 합니다.

```sql
-- in SQL
SELECT * FROM dfTable WHERE Description IS NOT NULL
```

`drop` 메소드의 인수로 `any` 를 지정한 경우 로우의 칼럼값 중 하나라도 null 값을 가진다면 해당 로우를 제거합니다. `all` 을 지정한 경우 모든 칼럼의 값이 null 이거나 NaN 인 경우에만 해당 로우를 제거합니다.

```scala
df.na.drop("all")
```

`drop` 메소드에 배열 형태의 칼럼을 인수로 전달해 적용할 수도 있습니다.

```scala
// in Scala
df.na.drop("all", Seq("StockCode", "InvoiceNo"))
```

### fill

`fill` 함수를 사용해 하나 이상의 칼럼을 특정 값으로 채울 수 있습니다. 채워 넣을 값과 카럶 집합으로 구성된 맵을 인수로 사용합니다.

예를 들어 String 데이터 타입의 칼럼에 존재하는 null 값을 다른 값으로 채워 넣는 방법은 다음과 같습니다.

```scala
df.na.fill("All Null values become this string")
```

`df.na.fill(5:Integer)` 같은 방식을 사용해 Integer 데이터 타입의 칼럼에 존재하는 null 값을 다른 값으로 채워 넣을 수 있습니다. Double 데이터 타입의 칼럼에는 `df.na.fill(5:Double)` 같은 방식으로 사용할 수 있습니다. 다수의 칼럼에 적용하고 싶다면 적용하고자 하는 칼럼명을 배여롤 만들어 인수로 사용합니다.

```scala
// in Scala
df.na.fill(5, Seq("StockCode", "InvoiceNo"))
```

Scala `Map` 사용해 다수의 칼럼에 `fill` 메소드를 적용할 수 있습니다. 여기서 Key 는 칼럼명이고, Value 은 null 값을 채우는데 사용할 값입니다.

```scala
// in Scala
val fillColValues = Map("StockCode" -> 5, "Description" -> "No Value")
df.na.fill(fillColValues)
```

### replace

`drop` 메소드와 `fill` 메소드 외에도 null 값을 유연하게 대처할 방법이 있습니다. 조건에 따라 다른 값으로 대체하는 겁니다. `replace` 를 사용하려면 변경하고자 하는 값과 원래 값의 데이터 타입이 같아야 합니다.

```scala
// in Scala
df.na.replace("Description", Map("" -> "UNKNOWN"))
```

## Ordering

`asc_nulls_first`, `desc_nulls_first`, `asc_nulls_last`, `desc_nulls_last` 함수를 사용해 DataFrame 을 정렬할 때 null 값이 표시되는 기준을 지정할 수 있습니다.

## Working with Complex Types

복합 데이터 타입에는 구조체, 배열, 맵이 있습니다.

### Structs

구조체는 DataFrame 내부의 DataFrame 으로 생각할 수 있습니다. 쿼리문에서 다수의 칼럼을 괄호로 묶어 구조체를 만들 수 있습니다.

```scala
df.selectExpr("(Description, InvoiceNo) as complex", "*")

df.selectExpr("struct(Description, InvoiceNo) as complex", "*")

// in Scala
import org.apache.spark.sql.functions.struct

val complexDF = df.select(struct("Description", "InvoiceNo").alias("complex"))
complexDF.createOrReplaceTempView("complexDF")
```

복합 데이터 타입을 가진 DataFrame 으로 다른 DataFrame 을 조회하는 것과 동일하게 사용할 수 있습니다. 유일한 차이점은 문법에 점(`.`) 을 사용하거나 `getField` 메소드를 사용하는 겁니다.

```scala
complexDF.select("complex.Description")
complexDF.select(col("complex").getField("Description"))
```

`*` 문자를 사용해 모든 값을 조회할 수 있으며, 모든 칼럼을 DataFrame 의 최상위 수준으로 끌어올릴 수 ㅣㅇㅆ습니다.

```scala
complexDF.select("complex.*")

-- in SQL
SELECT complex.* FROM complexDF
```

### Arrays

데이터에서 `Description` 칼럼의 모든 단어를 하나의 로우로 변환할 겁니다. `Description` 칼럼을 복합 데이터 타입인 배열로 변환하겠습니다.

#### split

배열로 변환하려면 `split` 함수를 사용합니다. `split` 함수에 구분자를 인수로 전달해 배열로 변환합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.split

df.select(split(col("Description"), " ")).show(2)
```

```sql
-- in SQL
SELECT split(Description, ' ') FROM dfTable
```

결과는 아래와 같습니다.

```scala
+---------------------+
|split(Description,  )|
+---------------------+
| [WHITE, HANGING, ...|
| [WHITE, METAL, LA...|
+---------------------+
```

`split` 함수는 Spark 에서 복합 데이터 타입을 마치 또 다른 칼럼처럼 다룰 수 있는 매우 강력한 기능입니다. Python 과 유사한 문법을 사용해 배열값을 조회할 수 있습니다.

```scala
// in Scala
df.select(split(col("Description"), " ").alias("array_col"))
  .selectExpr("array_col[0]").show(2)
```

```sql
-- in SQL
SELECT split(Description, ' ')[0] FROM dfTable
```

결과는 아래와 같습니다.

```scala
+------------+
|array_col[0]|
+------------+
|       WHITE|
|       WHITE|
+------------+
```

#### Array Length

배열의 크기를 조회해 배열의 길이를 알 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.size

df.select(size(split(col("Description"), " "))).show(2) // shows 5 and 3
```

#### array_contains

`array_contains` 함수를 사용해 배열에 특정 값이 존재하는지 확인할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.array_contains

df.select(array_contains(split(col("Description"), " "), "WHITE")).show(2)
```

```sql
-- in SQL
SELECT array_contains(split(Description, ' '), 'WHITE') FROM dfTable
```

실행 결과는 아래와 같습니다.

```scala
+--------------------------------------------+
|array_contains(split(Description, ), WHITE)|
+--------------------------------------------+
|                                        true|
|                                        true|
+--------------------------------------------+
```

복합 데이터 타입의 배열에 존재하는 모든 값을 로우로 변환하려면 `explode` 함수를 사용합니다.

#### explode

`explode` 함수는 배열 타입의 칼럼을 입력받습니다. 그리고 입력된 칼럼의 배열값에 포함된 모든 값을 로우로 변환합니다. 나머지 칼럼값은 중복되어 표시합니다. `Example 1` 은 처리 과정을 보여줍니다.

> Example 1 - Exploding a column of text

![image](https://user-images.githubusercontent.com/44635266/77643101-1a9b6c80-6fa2-11ea-8256-7a7e73238464.png)

```scala
// in Scala
import org.apache.spark.sql.functions.{split, explode}

df.withColumn("splitted", split(col("Description"), " "))
  .withColumn("exploded", explode(col("splitted")))
  .select("Description", "InvoiceNo", "exploded").show(2)
```

```sql
-- in SQL
SELECT Description, InvoiceNo, exploded
FROM (SELECT *, split(Description, " ") as splitted FROM dfTable)
LATERAL VIEW explode(splitted) as exploded
```

실행 결과는 아래와 같습니다.

```scala
+--------------------+---------+--------+
|         Description|InvoiceNo|exploded|
+--------------------+---------+--------+
|WHITE HANGING HEA...|   536365|   WHITE|
|WHITE HANGING HEA...|   536365| HANGING|
+--------------------+---------+--------+
```

### Maps

맵은 `map` 함수와 칼럼의 Key - Value 쌍을 이용해 생성합니다. 그리고 배열과 동일한 방법으로 값을 선택할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.map

df.select(map(col("Description"), col("InvoiceNo")).alias("complex_map")).show(2)
```

```sql
-- in SQL
SELECT map(Description, InvoiceNo) as complex_map FROM dfTable
WHERE Description IS NOT NULL
```

실행 결과는 아래와 같습니다.

```scala
+--------------------+
|         complex_map|
+--------------------+
|Map(WHITE HANGING...|
|Map(WHITE METAL L...|
+--------------------+
```

적합한 키를 사용해 데이터를 조회할 수 있으며 해당 키가 없다면 null 값을 반환합니다.

```scala
// in Scala
df.select(map(col("Description"), col("InvoiceNo")).alias("complex_map"))
  .selectExpr("complex_map['WHITE METAL LANTERN']").show(2)
```

실행 결과는 아래와 같습니다.

```scala
+--------------------------------+
|complex_map[WHITE METAL LANTERN]|
+--------------------------------+
|                            null|
|                          536365|
+--------------------------------+
```

`map` 타입은 분해하여 칼럼으로 변환할 수 있습니다.

```scala
// in Scala
df.select(map(col("Description"), col("InvoiceNo")).alias("complex_map"))
  .selectExpr("explode(complex_map)").show(2)
```

실행 결과는 아래와 같습니다.

```scala
+--------------------+------+
|                 key| value|
+--------------------+------+
|WHITE HANGING HEA...|536365|
| WHITE METAL LANTERN|536365|
+--------------------+------+
```

## Working with JSON

Spark 는 JSON 데이터를 다루기 위한 몇 가지 고유 기능을 지원합니다. Spark 에서 문자열 형태의 JSON 을 직접 조작할 수 있으며, JSON 을 파싱하거나 JSON 객체로 만들 수 있습니다.

다음은 JSON 칼럼을 생성하는 예제입니다.

```scala
// in Scala
val jsonDF = spark.range(1).selectExpr("""
  '{"myJSONKey" : {"myJSONValue" : [1, 2, 3]}}' as jsonString""")
```

`get_json_object` 함수는 JSON 객체를 인라인 쿼리로 조회할 수 있습니다. 중첩이 없는 단일 수준의 JSON 객체라면 `json_tuple` 을 사용할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{get_json_object, json_tuple}

jsonDF.select(
  get_json_object(col("jsonString"), "$.myJSONKey.myJSONValue[1]") as "column",
  json_tuple(col("jsonString"), "myJSONKey")).show(2)
```


SQL 을 사용한 처리는 다음과 같습니다.

```sql
jsonDF.selectExpr(
  "json_tuple(jsonString, '$.myJSONKey.myJSONValue[1]') as column").show(2)
```

실행 결과는 아래와 같습니다.

```scala
+------+--------------------+
|column| c0                 |
+------+--------------------+
|     2|{"myJSONValue":[1...|
+------+--------------------+
```

`to_json` 함수를 사용해 `StructType` 을 JSON 문자열로 변경할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.to_json

df.selectExpr("(InvoiceNo, Description) as myStruct")
  .select(to_json(col("myStruct")))
```

`to_json` 함수에 JSON 데이터소스와 동일한 형태의 딕셔너리를 파라미터로 사용할 수 있습니다. `from_json` 함수를 사용해 JSON 문자열을 다시 객체로 변환할 수 있습니다.

`from_json` 함수는 파라미터로 반드시 스키마를 지정해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.from_json
import org.apache.spark.sql.types._

val parseSchema = new StructType(Array(
  new StructField("InvoiceNo",StringType,true),
  new StructField("Description",StringType,true)))

df.selectExpr("(InvoiceNo, Description) as myStruct")
  .select(to_json(col("myStruct")).alias("newJSON"))
  .select(from_json(col("newJSON"), parseSchema), col("newJSON")).show(2)
```

실행 결과는 아래와 같습니다.

```scala
+----------------------+--------------------+
|jsontostructs(newJSON)|             newJSON|
+----------------------+--------------------+
| [536365,WHITE HAN...|{"InvoiceNo":"536..."|
| [536365,WHITE MET...|{"InvoiceNo":"536..."|
+----------------------+--------------------+
```

## User-Defined Functions

Spark 의 가장 강력한 기능 중 하나는 **사용자 정의 함수(User Defined Function, UDF)** 를 사용할 수 있다는 겁니다. UDF 는 Python 이나 Scala 그리고 외부 라이브러리를 사용해 사용자가 원하는 형태로 트랜스포메이션을 만들 수 있게 합니다.

UDF 는 레코드별로 데이터를 처리하는 함수이기 때문에 독특한 포맷이나 도메인에 특화된 언어를 사용하지 않습니다. 이러한 UDF 는 기본적으로 SparkSession 이나 Context 에서 사용할 수 있도록 임시 함수 형태로 등록됩니다.

숫자를 입력받아 세제곱 연산을 하는 `power3` UDF 함수를 만들어보겠습니다.

```scala
// in Scala
val udfExampleDF = spark.range(5).toDF("num")
def power3(number:Double):Double = number * number * number
power3(2.0)
```

Python 으로 함수를 작성했다면 매우 다르게 동작합니다. Spark 는 워커 노드에 Python 프로세스를 실행하고 Python 이 이해할 수 있는 포맷으로 모든 데이터를 직렬화합니다. 그리고 Python 프로세스에 있는 데이터의 로우마다 함수를 실행하고 마지막으로 JVM 과 Spark 에 처리결과를 반환합니다. `Example 2` 에 처리 과정을 나타냈습니다.

> Example 2 - Figure caption

![image](https://user-images.githubusercontent.com/44635266/77644202-03f61500-6fa4-11ea-9051-575c572da5fb.png)

UDF 를 실행해보겠습니다. 먼저 DataFrame 에 사용할 수 있도록 함수를 등록합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.udf

val power3udf = udf(power3(_:Double):Double)
```

이제 `power3` 함수를 DataFrame 의 다른 함수와 동일한 방법으로 사용할 수 있습니다.

```scala
// in Scala
udfExampleDF.select(power3udf(col("num"))).show()
```

위 예제는 Python 에도 동일하게 적용됩니다. 먼저 사용자 정의 함수를 등록합니다.

```python
# in Python
from pyspark.sql.functions import udf

power3udf = udf(power3)
```

사용자 정의 함수 등록이 완료되면 DataFrame 에서 사용할 수 있습니다.

```python
# in Python
from pyspark.sql.functions import col

udfExampleDF.select(power3udf(col("num"))).show(2)

+-----------+
|power3(num)|
+-----------+
|          0|
|          1|
+-----------+
```

아직까지는 DataFrame 에서만 사용할 수 있고, 문자열 표현식에서는 사용할 수 없습니다. 사용자 정의 함수를 SparkSQL 에 등록하면 모든 프로그래밍 언어와 SQL 에서 사용자 정의 함수를 사용할 수 있습니다.

Scala 를 사용해 사용자 정의 함수를 등록해보겠습니다.

```scala
// in Scala
spark.udf.register("power3", power3(_:Double):Double)
udfExampleDF.selectExpr("power3(num)").show(2)
```

사용자 정의 함수를 SparkSQL 함수로 등록하여 Scala 로 개발된 사용자 정의 함수를 Python 에서 우회적으로 사용할 수 있습니다. 하지만 사용자 정의 함수를 DataFrame 함수 대신 SQL 표현식으로 사용해야 합니다.

```python
# in Python
udfExampleDF.selectExpr("power3(num)").show(2)
```

Python 함수를 SQL 함수로 등록할 수 있습니다.

함수가 올바르게 동작할 수 있도록 반환될 실제 데이터 타입과 일치하는 데이터 타입을 지정해야합니다. 그렇지 않으면 Spark 는 오류가 아닌 null 값을 반환합니다. 아래 예제는 반환 데이터 타입을 DoubleType 으로 변경하면 이러한 현상을 확인할 수 있습니다.

```python
# in Python
from pyspark.sql.types import IntegerType, DoubleType

spark.udf.register("power3py", power3, DoubleType())

# in Python
udfExampleDF.selectExpr("power3py(num)").show(2)
# registered via Python
```

null 값을 반환하는 이유는 `range` 메소드가 Integer 데이터 타입의 데이터를 만들기 때문입니다. 이 타입을 Float 데이터 타이븡로 변환할 수 없으므로 null 을 반환합니다.

SQL 에서도 등록된 사용자 정의 함수를 사용할 수 있습니다.

```sql
-- in SQL
SELECT power3(12), power3py(12) -- doesn't work because of return type
```

사용자 정의 함수에서 값을 선택적으로 반환하려면 Python 은 None 을 Scala 는 Option 타입을 반환해야 합니다.

## Hive UDFs

Hive 문법을 사용해서 만든 UDF/UDAF 도 사용할 수 있습니다. SparkSession 을 생성할 때 `SparkSession.builder().enableHiveSupport()` 를 명시해 반드시 Hive 지원 기능을 활성화 해야합니다.

```sql
-- in SQL
CREATE TEMPORARY FUNCTION myFunc AS 'com.organization.hive.udf.FunctionName'
```

`TEMPORARY` 키워드를 제거하면 Hive 메타스토어에 영구 함수로 등록됩니다.