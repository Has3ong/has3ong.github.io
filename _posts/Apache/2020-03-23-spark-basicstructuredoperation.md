---
title : Spark Basic Structured Operations
tags :
- DataFrame Transformation
- Row
- Column
- Schema
- Apache
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

DataFrame 은 Row 타입의 **레코드(Record)** 와 각 레코드에 수행할 연산 표현식을 나타내는 여러 **칼럼(Column)** 으로 구성됩니다. **스키마(Schema)** 는 각 컬럼명과 데이터 타입을 정의합니다. DataFrame 의 **파티셔닝(Partitioning)** 은 DataFrame 이나 Dataset 이 클러스터에서 물리적으로 배치되는 형태를 정의합니다.

**파티셔닝 스키마(Partitioning Schema)** 는 파티션을 배치하는 방법을 정의합니다. 파티셔닝의 분할 기준은 특정 컬럼이나 비결정론적 값을 기반으로 설정할 수 있습니다.

우선 DataFrame 을 생성합니다.

```scala
// in Scala
val df = spark.read.format("json")
  .load("/data/flight-data/json/2015-summary.json")
```

DataFrame 은 컬럼을 가지며 스키마로 컬럼을 정의합니다. DataFrame 의 스키마를 보겠습니다.

```scala
df.printSchema()
```

스키마는 관련된 모든 것을 하나로 묶는 역할을 합니다.

## Schemas

스키마는 DataFrame 의 컬럼명과 데이터 타입을 정의합니다. 데이터소스에서 스키마를 얻거나 직접 정의할 수 있습니다.

아래 예제는 미국 교통통계국이 제공하는 [항공운항 데이터](https://github.com/databricks/Spark-The-Definitive-Guide/tree/master/data/flight-data)이며 줄로 구분된 반정형 JSON 데이터 입니다.

```scala
// in Scala
spark.read.format("json").load("/data/flight-data/json/2015-summary.json").schema
```

Scala 코드의 실행 결과는 아래와 같습니다.

```scala
org.apache.spark.sql.types.StructType = ...
StructType(StructField(DEST_COUNTRY_NAME,StringType,true),
StructField(ORIGIN_COUNTRY_NAME,StringType,true),
StructField(count,LongType,true))
```

스키마는 여러 개의 `StructField` 타입 필드로 구성된 `StructType` 객체입니다. `StructField` 는 이름, 데이터 타입, 컬럼이 값이 없거나 `null` 일 수 있는지 지정하는 불리언값을 가집니다.

필요한 경우 칼럼과 관련된 메타데이터를 지정할 수 잇습니다. 메타데이터는 해당 컬럼과 관련된 정보이며, Spark 의 머신러닝 라이브러리에서 사용합니다.

스키마는 복합 데이터 타입인 `StructType` 을 가질 수 있습니다. 다음은 DataFrame 에 스키마를 만들고 적용하는 예제입니다.

```scala
// in Scala
import org.apache.spark.sql.types.{StructField, StructType, StringType, LongType}
import org.apache.spark.sql.types.Metadata

val myManualSchema = StructType(Array(
  StructField("DEST_COUNTRY_NAME", StringType, true),
  StructField("ORIGIN_COUNTRY_NAME", StringType, true),
  StructField("count", LongType, false,
    Metadata.fromJson("{\"hello\":\"world\"}"))
))

val df = spark.read.format("json").schema(myManualSchema)
  .load("/data/flight-data/json/2015-summary.json")
```

Spark 는 자체 데이터 타입 정보를 사용하므로 프로그래밍 언어에의 데이터 타입을 Spark 의 데이터 타입으로 설정할 수 없습니다.

## Columns and Expressions

Spark 의 컬럼은 스프레드시트, R 의 DataFrame, Pandas 의 DataFrame 컬럼과 유사합니다. 사용자는 표현식으로 DataFrame 의 컬럼을 선택 조작 제거할 수 있습니다.

Spark 의 클럼은 표현식으로 레코드 단위로 계산한 값을 단순히 나타내는 논리적인 구조입니다. 컬럼의 실젯값을 얻으려면 로우가 필요하고, 로우를 얻으려면 DataFrame 이 필요합니다. DataFrame 을 통하지 않으면 외부에서 칼럼에 접근할 수 없습니다.

칼럼 내용을 수정하려면 반드시 DataFrame 의 Spark 트랜스포메이션을 사용해야 합니다.

### Columns

컬럼을 생성하고 참조할 수 있는 다양한 방법이 있지만, `col` 함수나 `column` 함수를 사용하는 것이 가장 간단합니다. 이들 함수는 컬럼명을 인수로 받습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{col, column}
col("someColumnName")
column("someColumnName")
```

컬럼이 DataFrame 에 있을지 없을지는 알 수 없습니다. 컬럼은 컬럼명을 **카탈로그** 에 저장된 정보와 비교하기 전까지 **미확인** 상태로 남습니다. **분석기** 가 동작하는 단계에서 컬럼과 테이블을 참조합니다.

#### Explicit column references

DataFrame 의 컬럼은 `col` 메소드로 참조합니다. `col` 메소드는 조인 시 유용합니다. 예를 들어, DataFrame 의 어떤 컬럼은 다른 DataFrame 의 조인 대상 컬럼에서 참조하기 위해 `col` 메소드를 사용합니다. `col` 메소드를 사용해 명시적으로 칼럼을 정의하면 Spark 는 분석기 실행 단계에서 컬럼 확인 절차를 생략합니다.

```scala
df.col("count")
```

### Expressions

DataFrame 을 정의할 때 컬럼은 표현식이라고 했습니다. **표현식** 은 DataFrame 레코드의 여러 값에 대한 트랜스포메이션 집합을 의미합니다.

여러 컬럼명을 입력으로 받아 식별하고, 단일 값을 만들기 위해 다양한 표현식을 각 레코드에 적용하는 함수라 생각할 수 있습니다. 여기서 단일 값은 Map 이나 Array 같은 복합 데이터 타입일 수 있습니다.

표현식은 `expr` 함수로 가장 간단히 사용할 수 있습니다. 이 함수를 사용해 DataFrame 의 컬럼을 참조할 수 있습니다. 예를 들어 `expr("SomeCol")` 은 `col("someCol")` 구문과 동일하게 동작합니다.

#### Columns as expressions

컬럼은 표현식의 일부 기능을 제공합니다. `col()` 함수를 호출해 컬럼에 트랜스포메이션을 수행하려면 반드시 칼럼 참조를 사용해야 합니다. `expr` 함수의 인수로 표현식을 사용하면 표현식을 분석해 트랜스포메이션과 컬럼 참조를 알아낼 수 있으며, 다음 트랜스포메이션에 컬럼 참조를 전달할 수 있습니다.

`expr("someCol - 5")`, `col("someCol") - 5`, `expr("someCol") -5` 는 모두 같은 트랜스포메이션 과정을 거칩니다. Spark 가 연산 순서를 지정하는 논리적 트리로 컴파일하기 때문입니다.

* Columns are just expressions.
* Columns and transformations of those columns compile to the same logical plan as parsed expressions

예제를 보겠습니다.

```scala
(((col("someCol") + 5) * 200) - 6) < col("otherCol")
```

`Example 1` 은 논리적 트리의 개요를 나타냅니다.

> Example 1 - A logical tree

![image](https://user-images.githubusercontent.com/44635266/77066819-2ed1ed80-6a27-11ea-9246-c6ecd40e4865.png)

`Example 1` 이 어색하지 않은 이뉴는 **지향성 비순환 그래프(Directed Acyclic Graph, DAG)** 이기 때문입니다 이 그래프는 다음 코드로 동일하게 표현할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.expr
expr("(((someCol + 5) * 200) - 6) < otherCol")
```

SQL 의 `SELECT` 구문에 이전 표현식을 사용해도 잘 동작하며 동일한 결과를 생성합니다. 그 이유는 SQL 표현식과 위 예제의 DataFrame 코드는 실행 시점에 동일한 논리 트리로 컴파일되기 때문입니다. 따라서 DataFrame 코드나 SQL 로 표현식을 작성할 수 있으며 동일한 성능을 발휘합니다.

#### Accessing a DataFrame’s columns

`printSchema` 메소드로 DataFrame 의 전체 컬럼 정보를 확인할 수 있습니다. 하지만 프로그래밍 방식으로 컬럼에 접근할 때는 DataFrame 의 `columns` 속성을 사용합니다.

```scala
spark.read.format("json").load("/data/flight-data/json/2015-summary.json")
  .columns
```

## Records and Rows

Spark 에서 DataFrame 의 각 로우는 하나의 레코드입니다. Spark 는 레코드를 Row 객체로 표현합니다. Spark 는 값을 생성하기 위해 컬럼 표현식으로 Row 객체를 다룹니다.

Row 객체는 내부에 바이트 배열을 가집니다. 이 바이트 배열 인터페이스는 오직 컬럼 표현식으로만 다룰 수 있으므로 사용자에게 노출되지 않습니다.

DataFrame 을 사용해 드라이버에 개별 로우를 반환하는 명령은 항상 하나 이상의 Row 타입을 반환합니다.

DataFrame 의 `first` 메소드로 로우를 확인해보겠습니다.

```scala
df.first()
```

### Creating Rows

각 컬럼에 해당하는 값을 사용해 Row 객체를 직접 생성할 수 있습니다. Row 객체는 스키마 정보를 가지고 있지 않습니다. DataFrame 마느 유일하게 스키마를 갖습니다. 그러므로 Row 객체를 직접 생성하려면 DataFrame 의 스키마와 같은 순서로 값을 명시해야 합니다.

```scala
// in Scala
import org.apache.spark.sql.Row
val myRow = Row("Hello", null, 1, false)
```

Row 의 데이터에 접근하는 방법은 매우 간단합니다. 원하는 위치를 지정하기만 하면 됩니다. Scala 나 Java 에서는 헬퍼 메서드를 사용하거나 명시적으로 데이터 타입을 지정해야 합니다. 반면 Python 이나 R 에서는 올바른 데이터 타입으로 자동 변환 됩니다.

```scala
// in Scala
myRow(0) // type Any
myRow(0).asInstanceOf[String] // String
myRow.getString(0) // String
myRow.getInt(2) // Int
```

Dataset API 를 사용하면 JVM 객체를 가진 데이터셋을 얻을 수 있습니다.

## DataFrame Transformations

DataFrame 을 다루는 방법은 `Example 2` 처럼 몇 가지 주요 작업으로 나눌 수 있습니다.

* We can add rows or columns
* We can remove rows or columns
* We can transform a row into a column (or vice versa)
* We can change the order of rows based on the values in columns

> Example 2 - Different kinds of transformations

![image](https://user-images.githubusercontent.com/44635266/77247237-70a2a400-6c72-11ea-9466-e17ae60f62aa.png)

이 모든 유형의 작업은 트랜스포메이션으로 변호나할 수 있습니다. 가장 일반적인 트랜스포메이션은 모든 로우의 특정 컬럼값을 변경하고 그 결과를 반환하는 겁니다.

### Creating DataFrames

원시 데이터소스에서 DataFrame 을 생성할 수 있습니다. 

```scala
// in Scala
val df = spark.read.format("json")
  .load("/data/flight-data/json/2015-summary.json")
df.createOrReplaceTempView("dfTable")
```

Row 객체를 가진 Seq 타입을 직접 변환해 DataFrame 을 생성할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.{StructField, StructType, StringType, LongType}

val myManualSchema = new StructType(Array(
  new StructField("some", StringType, true),
  new StructField("col", StringType, true),
  new StructField("names", LongType, false)))

val myRows = Seq(Row("Hello", null, 1L))
val myRDD = spark.sparkContext.parallelize(myRows)
val myDf = spark.createDataFrame(myRDD, myManualSchema)

myDf.show()
```

실행 결과는 아래와 같습니다.

```scala
+-----+----+-----+
| some| col|names|
+-----+----+-----+
|Hello|null|    1|
+-----+----+-----+
```

다음과 같이 가장 유용하게 사용할 수 있는 메소드를 알아보겠습니다.

* 칼럼이나 표현식을 사용하는 `select` 메소드
* 문자열 표현식을 사용하는 `selectExpr` 메소드
* 메소드로 사용할 수 없는 `org.apache.spark.sql.functions` 패키지에 포함된 다양한 함수

이 세 가지 유형의 메서도르 DataFrame 을 다룰 때 필요한 대부분의 트랜스포메이션 작업을 해결할 수 있습니다.

### select and selectExpr

`select` 와 `selectExpr` 메소드를 사용하면 데이터 테이블에 SQL 을 실해앟는 것처럼 DataFrame 에서도 SQL 을 사용할 수 있습니다.

```sql
-- in SQL
SELECT * FROM dataFrameTable
SELECT columnName FROM dataFrameTable
SELECT columnName * 10, otherColumn, someOtherCol as c FROM dataFrameTable
```

DataFrame 의 컬럼을 다룰 때 SQL 을 사용할 수 있습니다. DataFrame 을 사용한 몇 가지 예제를 살펴보며 컬럼을 다루는 방법을 알아보겠습니다. 그중 문자열 컬럼명을 인수로 받는 `select` 메소드를 사용하는 방법이 가장 쉽습니다.

```scala
// in Scala
df.select("DEST_COUNTRY_NAME").show(2)
```

```sql
-- in SQL
SELECT DEST_COUNTRY_NAME FROM dfTable LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+
|DEST_COUNTRY_NAME|
+-----------------+
|    United States|
|    United States|
+-----------------+
```

같은 형태의 쿼리로 여러 칼럼을 선택할 수 있습니다. 여러 칼럼을 선택하면 `select` 메소드에 원하는 칼럼명을 추가합니다.

```scala
// in Scala
df.select("DEST_COUNTRY_NAME", "ORIGIN_COUNTRY_NAME").show(2)
```

```sql
-- in SQL
SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME FROM dfTable LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+-------------------+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|
+-----------------+-------------------+
|    United States|            Romania|
|    United States|            Croatia|
+-----------------+-------------------+
```

또한, 다양한 칼럼 참조 방법이 있습니다. 칼럼을 참조하는 다양한 방법을 섞어가면서 사용할 수 있는 점을 알아두면 좋습니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{expr, col, column}
df.select(
    df.col("DEST_COUNTRY_NAME"),
    col("DEST_COUNTRY_NAME"),
    column("DEST_COUNTRY_NAME"),
    'DEST_COUNTRY_NAME,
    $"DEST_COUNTRY_NAME",
    expr("DEST_COUNTRY_NAME"))
  .show(2)
```

Column 객체와 문자열을 ㅎ마께 섞어 쓰는 실수를 많이 합니다. 아래 코드는 컴파일러 오류가 발생합니다.

```scala
df.select(col("DEST_COUNTRY_NAME"), "DEST_COUNTRY_NAME")
```

`expr` 함수는 가장 유연한 참조 방법입니다. `expr` 함수는 단순 칼럼 참조나 문자열을 이용해 칼럼을 참조할 수 있습니다. `AS` 키워드로 칼럼명을 변경한 다음 `alias` 메소드로 원래 칼럼명을 되돌려 보겠습니다.

```scala
// in Scala
df.select(expr("DEST_COUNTRY_NAME AS destination")).show(2)
```

```sql
-- in SQL
SELECT DEST_COUNTRY_NAME as destination FROM dfTable LIMIT 2
```

위 코드는 칼럼명을 `destination` 으로 변경합니다. 표현식의 결과를 다른 표현식으로 다시 처리할 수 있습니다.

```scala
// in Scala
df.select(expr("DEST_COUNTRY_NAME as destination").alias("DEST_COUNTRY_NAME"))
  .show(2)
```

위 코드는 변경한 칼럼명을 원래 이름으로 되돌려 놓습니다.

`select` 메소드에 `expr` 함수를 사용하는 패턴을 자주 사용합니다. Spark 는 이런 작업을 간단하고 효율적으로 할 수 있는 `selectExpr` 메소드를 제공합니다. `selectExpr` 메소드는 자주 사용하는 편리한 인터페이스 중 하나입니다.

```scala
// in Scala
df.selectExpr("DEST_COUNTRY_NAME as newColumnName", "DEST_COUNTRY_NAME").show(2)
```

`selectExpr` 메소드는 Spark 의 진정한 능력을 보여줍니다. 이 메소드는 새로운 DataFrame 을 생성하는 복잡한 표현식을 간단하게 만들어 줍니다. 사실 모든 유효한 **비 집계형(Non Aggregating)** SQL 구문을 지정할 수 있습니다. 단, 칼럼을 식별할 수 있어야 합니다.

다음은 DataFrame 에 출발지와 도착지가 같은지 나타내는 새로운 `withinCountry` 칼럼을 추가하는 예제입니다.

```scala
// in Scala
df.selectExpr(
    "*", // include all original columns
    "(DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry")
  .show(2)
```

```sql
-- in SQL
SELECT *, (DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry
FROM dfTable
LIMIT 2
```

결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+-------------+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|withinCountry|
+-----------------+-------------------+-----+-------------+
|    United States|            Romania|   15|        false|
|    United States|            Croatia|    1|        false|
+-----------------+-------------------+-----+-------------+
```

`select` 표현식에는 DataFrame 의 컬럼에 대한 집계 함수를 지정할 수 있습니다.

```scala
// in Scala
df.selectExpr("avg(count)", "count(distinct(DEST_COUNTRY_NAME))").show(2)
```

```sql
-- in SQL
SELECT avg(count), count(distinct(DEST_COUNTRY_NAME)) FROM dfTable LIMIT 2
```

결과는 다음과 같습니다.

```scala
+-----------+---------------------------------+
| avg(count)|count(DISTINCT DEST_COUNTRY_NAME)|
+-----------+---------------------------------+
|1770.765625|                              132|
+-----------+---------------------------------+
```

### Converting to Spark Types (Literals)

때로는 새로운 칼럼이 아닌 명시적인 값을 Spark 에 전달해야 합니다. 명시적인 값은 상숫값일 수 있고, 추후 비교에 사용할 무언가가 될 수도 있습니다. 이때 **리터럴(Literal)** 을 사용합니다.

리터럴은 프로그래밍 언어의 리터럴값을 Spark 가 이해할 수 있는 값으로 변환합니다. 리터럴은 표현식이며 예제와 같은 방식으로 작동합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.lit
df.select(expr("*"), lit(1).as("One")).show(2)
```

SQL 에서 리터럴은 상숫값을 의미합니다.

```sql
-- in SQL
SELECT *, 1 as One FROM dfTable LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+---+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|One|
+-----------------+-------------------+-----+---+
|    United States|            Romania|   15|  1|
|    United States|            Croatia|    1|  1|
+-----------------+-------------------+-----+---+
```

어떤 상수나 프로그래밍으로 생성된 변숫값이 특정 칼럼의 값보다 큰지 확인할 때 리터럴을 사용합니다.

### Adding Columns

DataFrame 에 신규 칼럼을 추가하는 공식적인 방법은 DataFrame 에 `withColumn` 메서드를 사용하는 겁니다. 숫자 1 을 값으로 가지는 칼럼을 추가하는 예제는 다음과 같습니다.

```scala
// in Scala
df.withColumn("numberOne", lit(1)).show(2)
```

```sql
-- in SQL
SELECT *, 1 as numberOne FROM dfTable LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+---------+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|numberOne|
+-----------------+-------------------+-----+---------+
|    United States|            Romania|   15|        1|
|    United States|            Croatia|    1|        1|
+-----------------+-------------------+-----+---------+
```

다음은 출발지와 도착지가 같은지 여부를 불리언 타입으로 표현하는 예제입니다.

```scala
// in Scala
df.withColumn("withinCountry", expr("ORIGIN_COUNTRY_NAME == DEST_COUNTRY_NAME"))
  .show(2)
```

`withColumn` 메서드는 2 개의 인수를 사용합니다. 하나는 칼럼명이고, 다른 하나는 값을 생성할 표현식입니다. 한 가지 재미있는 것은 `withColumn` 메소드로 칼럼명을 변경할 수 있다는 것입니다.

SQL 문법은 이전과 동일하여 생략하겠습니다.

```scala
df.withColumn("Destination", expr("DEST_COUNTRY_NAME")).columns
```

실행 결과는 다음과 같습니다.

```scala
... DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count, Destination
```

### Renaming Columns

`withColumn` 메소드를 사용하는 대신 `withColumnRenamed` 메소드로 칼럼명을 변경할 수 있습니다. `withColumnRenamed` 메소드는 첫 번째 인수로 전달된 칼럼명을 두 번째 인수의 문자열로 변경합니다.

```scala
// in Scala
df.withColumnRenamed("DEST_COUNTRY_NAME", "dest").column
```

### Reserved Characters and Keywords

공백이나 하이픈(`-`) 같은 예약 문자는 칼럼명에 사용할 수 없습니다. 예약 문자를 칼럼명에 사용하려면 백틱 문자를 이용해 이스케이핑해야 합니다. `withColumn` 메소드를 사용해 예약 문자가 포함된 칼럼을 생성해보겠습니다.

다음은 이스케이핑 문자가 필요한 경우와 필요 없는 경우의 예제입니다.

```scala
// in Scala
import org.apache.spark.sql.functions.expr

val dfWithLongColName = df.withColumn(
  "This Long Column-Name",
  expr("ORIGIN_COUNTRY_NAME"))
```

위 예제에서는 `withColumn` 메소드의 첫 번째 인수로 새로운 칼럼명을 나타내는 문자열을 지정했기 떄문에 이스케이프 문자가 필요없습니다. 하지만 다음은 표현식으로 칼럼을 참조하므로 백틱 문자를 사용합니다.

```scala
// in Scala
dfWithLongColName.selectExpr(
    "`This Long Column-Name`",
    "`This Long Column-Name` as `new col`")
  .show(2)
```

```sql
-- in SQL
SELECT `This Long Column-Name`, `This Long Column-Name` as `new col`
FROM dfTableLong LIMIT 2
```

표현색 대신 문자열을 사용해 명시적으로 칼럼을 참조하면 리터럴로 해석되기 때문에 예약 문자가 포함된 칼럼을 참조할 수 있습니다. 예약 문자나 키워드를 사용하는 표현식에만 이스케이프 처리가 필요합니다.

```scala
// in Scala
dfWithLongColName.select(col("This Long Column-Name")).columns
```

### Case Sensitivity

기본적으로 Spark 는 대소문자를 가리지 않습니다. 다음과 같이 설정하여 대소문자를 구분하게 만들 수 있습니다.

```sql
-- in SQL
set spark.sql.caseSensitive true
```

### Removing Columns

DataFrame 에 칼럼을 제거하는 방법을 알아보겠습니다. `select` 메소드로 칼럼을 제거할 수 있지만 칼럼을 제거하는 메서드인 `drop` 을 사용할 수 있습니다.

```scala
df.drop("ORIGIN_COUNTRY_NAME").columns
```

다수의 칼럼명을 `drop` 메소드의 인수로 사용해 칼럼을 한꺼번에 제거할 수 있습니다.

```scala
dfWithLongColName.drop("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME")
```

### Changing a Column’s Type (cast)

가끔 특정 데이터 타입을 다른 데이터 타입으로 형변환할 필요가 있습니다. 다수의 `StringType` 칼럼을 정수형으로 변환해야 하는 경우가 그 예입니다. `cast` 메소드로 데이터 타입을 변환할 수 있습니다. 다음은 `count` 칼럼을 `Integer` 데이터 타입에서 `String` 데이터 타입으로 형변환하는 예제입니다.

```scala
// in Scala
df.withColumn("count2", col("count").cast("string"))
```

```sql
-- in SQL
SELECT *, cast(count as string) AS count2 FROM dfTable
```

### Filtering Rows

로우를 필터링하려면 참과 거짓을 판별하는 표현식을 만들어야 합니다. 그러면 표현식의 결과가 `false` 인 로우를 걸러낼 수 있습니다. DataFrame 의 가장 일반적인 필터링 방법은 문자열 표현식이나 칼럼을 다루는 기능을 이용해 표현식을 만드는 겁니다. DataFrame 의 `where` 메소드나 `filter` 메소드로 필터링 할 수 있습니다.

두 메소드는 같은 연산을 수행하며 같은 파라미터 타입을 사용합니다.

다음 예제의 `filter` 와 `where` 메소드는 동일하게 동작합니다.

```scala
df.filter(col("count") < 2).show(2)
df.where("count < 2").show(2)
```

```sql
-- in SQL
SELECT * FROM dfTable WHERE count < 2 LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Croatia|    1|
|    United States|          Singapore|    1|
+-----------------+-------------------+-----+
```

같은 표현식에 여러 필터를 적용해야 할 때도 있습니다. 하지만 Spark 는 자동으로 필터의 순서와 상관없이 동시에 모든 필터링 작업을 수행하기 때문에 항상 유요한건 아닙니다. 그러므로 여러 개의 `AND` 필터를 지정하려면 차례대로 필터를 연결하고 판단은 Spark 에 맡겨야합니다.

```scala
// in Scala
df.where(col("count") < 2).where(col("ORIGIN_COUNTRY_NAME") =!= "Croatia")
  .show(2)
```

```sql
-- in SQL
SELECT * FROM dfTable WHERE count < 2 AND ORIGIN_COUNTRY_NAME != "Croatia"
LIMIT 2
```

실행 결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|          Singapore|    1|
|          Moldova|      United States|    1|
+-----------------+-------------------+-----+
```

### Getting Unique Rows

일반적으로 DataFrame 에 고윳값이나 중복되지 않은 값을 얻는 연산을 자주 사용합니다. 고윳값을 얻으려면 하나 이상의 칼럼을 사용해야 합니다. DataFrame 의 모든 로우에서 중복 데이터를 제거할 수 있는 `distinct` 메소드를 사용해 고윳값을 찾을 수 있습니다.

항공운항 데이터셋에서 중복되지 않은 출발지 정보를 얻는 예제를 보겠습니다. `distinct` 메소드는 중복되지 않은 로우를 가진 새로운 DataFrame 을 반환합니다.

```scala
// in Scala
df.select("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME").distinct().count()
```

```sql
-- in SQL
SELECT COUNT(DISTINCT(ORIGIN_COUNTRY_NAME, DEST_COUNTRY_NAME)) FROM dfTable
```

결과값은 256 입니다.

```scala
// in Scala
df.select("ORIGIN_COUNTRY_NAME").distinct().count()
```

```sql
-- in SQL
SELECT COUNT(DISTINCT ORIGIN_COUNTRY_NAME) FROM dfTable
```

결과값은 125 입니다.

### Random Samples

DataFrame 에 무작위 샘플 데이터를 얻으려면 DataFrame 의 `sample` 메소드를 사용합니다. DataFrame 에서 표본 데이터 추출 비율을 지정할 수 있으며 **복원 추출(Sample with Replacement)** 이나 **비복원 추출(Sample without Replacement)** 의 사용 여부를 지정할 수 있습니다.

```scala
val seed = 5
val withReplacement = false
val fraction = 0.5
df.sample(withReplacement, fraction, seed).count()
```

결과값은 126 입니다.

### Random Splits

**임의 분할(Random Split)** 은 원본 DataFrame 을 임의 크기로 분할할 때 유용하게 사용합니다. 이 기능은 머신러닝 알고리즘에서 사용할 학습셋, 검증셋 그리고 테스트셋을 만들 때 주로 사용합니다.

아래 예제는 분할 가중치를 함수의 파라미터로 설정해 원본 DataFrame 을 서로 다른 데이터를 가진 두 개의 DataFrame 으로 나눕니다. 이 메소드는 **임의성(Randomized)** 을 가지도록 설계되었으므로 시드값을 반드시 설정해야 합니다.

```scala
// in Scala
val dataFrames = df.randomSplit(Array(0.25, 0.75), seed)
dataFrames(0).count() > dataFrames(1).count() // False
```

### Concatenating and Appending Rows (Union)

DataFrame 은 불변성을 가집니다. 그러므로 DataFrame 에 레코드를 추가하는 작업은 DataFrame 을 변경하는 작업이기 때문에 불가능합니다.

DataFrame 에 레코드를 추가하려면 원본 DataFrame 을 새로운 DataFrame 과 **통합(Union)** 해야 합니다. 통합은 2 개의 DataFrame 을 단순히 결합하는 행위입니다. 통합하려는 두 개의 DataFrame 은 반드시 동일한 스키마와 칼럼 수를 가져야 합니다.

```scala
// in Scala
import org.apache.spark.sql.Row

val schema = df.schema
val newRows = Seq(
  Row("New Country", "Other Country", 5L),
  Row("New Country 2", "Other Country 3", 1L)
)

val parallelizedRows = spark.sparkContext.parallelize(newRows)
val newDF = spark.createDataFrame(parallelizedRows, schema)
df.union(newDF)
  .where("count = 1")
  .where($"ORIGIN_COUNTRY_NAME" =!= "United States")
  .show() // get all of them and we'll see our new rows at the end
```

Scala 에선 반드시 `=!=` 연산자를 사용해야 합니다. 칼럼 표현식과 문자열을 비교할 때 `=!=` 연산자를 사용하면 칼럼 표현식(`$"ORIGIN_COUNTRY_NAME"`) 이 아닌 칼럼의 실젯값을 비교 대상 문자열과 비교합니다.

실행결과는 다음과 같습니다.

```scala
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Croatia|    1|
|    United States|            Namibia|    1|
|    New Country 2|    Other Country 3|    1|
+-----------------+-------------------+-----+
```

로우가 추가된 DataFrame 을 참조하려면 새롭게 만들어진 DataFrame 객체를 사용해야 합니다. DataFrame 을 뷰로 만들거나 테이블로 등록하면 DataFrame 변경 작업과 관계없이 동적으로 참조할 수 있습니다.

### Sorting Rows

`sort` 와 `orderBy` 메소드를 사용해 DataFrame 의 최댓값 혹은 최솟값이 상단에 위치하도록 정렬할 수 있습니다. 두 메소드는 완전히 같은 방식으로 동작합니다. 두 메소드 모두 칼럼 표현식과 문자열을 사용할 수 있으며 다수의 칼럼을 지정할 수 있습니다.

디폴트는 오름차순입니다.

```scala
// in Scala
df.sort("count").show(5)
df.orderBy("count", "DEST_COUNTRY_NAME").show(5)
df.orderBy(col("count"), col("DEST_COUNTRY_NAME")).show(5)
```

정렬 기준을 명확히 지정하려면 `asc` 나 `desc` 함수를 사용합니다. 두 함수 모두 칼럼의 정렬 순서를 지정합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{desc, asc}
df.orderBy(expr("count desc")).show(2)
df.orderBy(desc("count"), asc("DEST_COUNTRY_NAME")).show(2)
```

```sql
-- in SQL
SELECT * FROM dfTable ORDER BY count DESC, DEST_COUNTRY_NAME ASC LIMIT 2
```

`asc_nulls_first`, `desc_nulls_first`, `asc_nulls_last`, `desc_nulls_last` 메소드를 사용하여 정렬된 DataFrame 에서 `null` 값이 표시되는 기준을 지정할 수 있습니다.

트랜스포메이션을 처리하기 전에 성능을 최적화하기 위해 파티션별로 정렬을 수행하기도 합니다. 파티션별로 정렬은 `sortWithinPartitions` 메소드로 할 수 있습니다.

```scala
// in Scala
spark.read.format("json").load("/data/flight-data/json/*-summary.json")
  .sortWithinPartitions("count")
```

### Limit

DataFrame 에서 추출할 로우 수를 제한해보겠습니다. `limit` 메소드를 사용해 추출할 로우 수를 제한할 수 있습니다.

```scala
// in Scala
df.limit(5).show()
```

```sql
-- in SQL
SELECT * FROM dfTable LIMIT 6
```

```scala
// in Scala
df.orderBy(expr("count desc")).limit(6).show()
```

```sql
-- in SQL
SELECT * FROM dfTable ORDER BY count desc LIMIT 6
```

### Repartition and Coalesce

또 다른 최적화 기법은 자주 필터링 하는 칼럼을 기준으로 데이터를 분할하는 겁니다. 이를 통해 파티셔닝 스키마와 파티션 수를 클러스터 전반의 물리적 데이터 구성을 제어할 수 있습니다.

`repartition` 메소드를 호출하면 무조건 전체 데이터를 셔플합니다. 향후에 사용할 파티션 수가 현재 파티션 수보다 많거나 칼럼을 기준으로 파티션을 만드는 경우에만 사용해야 합니다.

```scala
// in Scala
df.rdd.getNumPartitions // 1
```

```scala
// in Scala
df.repartition(5)
```

특정 칼럼을 기준으로 자주 필터링한다면 자주 필터링되는 칼럼을 기준으로 파티션을 재분배하는 것이 좋습니다.

```scala
// in Scala
df.repartition(col("DEST_COUNTRY_NAME"))
```

선택적으로 파티션 수를 지정할 수 있습니다.

```scala
// in Scala
df.repartition(5, col("DEST_COUNTRY_NAME"))
```

`coalesce` 메소드는 전체 데이터를 셔플하지 않고 파티션을 병합하려는 겨우에 사용합니다. 다음은 목적지를 기준으로 셔플을 수행해 5 개의 파티션을 나누고 전체 데이터를 셔플잆이 병합하는 예제입니다.

```scala
// in Scala
df.repartition(5, col("DEST_COUNTRY_NAME")).coalesce(2)
```

### Collecting Rows to the Driver

Spark 는 드라이버에서 클러스터 상태 정보를 유지합니다. 로컬 환경에서 데이터를 다루려면 드라이버로 데이터를 수집해야 합니다.

`collect` 메소드는 전체 DataFrame 의 모든 데이터를 수집하며, `take` 메소드는 상위 `N` 개의 로우를 반환합니다. `show` 메소드는 여러 로우를 보기 좋게 출력합니다.

```scala
// in Scala
val collectDF = df.limit(10)
collectDF.take(5) // take works with an Integer count
collectDF.show() // this prints it out nicely
collectDF.show(5, false)
collectDF.collect()
```

전체 데이터 셋에 대한 반복 처리를 위해 드라이버 로우를 모우는 또 다른 방법이 있습니다. `toLocalIterator` 메소드는 이터레이터로 모든 파티션의 데이터를 드라이버에 전달합니다. `toLocalIterator` 메소드를 사용해 데이터셋의 파티션을 차례로 반복처리할 수 있습니다.

```scala
collectDF.toLocalIterator()
```

> 드라이버로 모든 데이터 컬렉션을 수집하는 작업은 매우 큰 비용이 발생합니다. 대규모 데이터셋에 `collect` 와 `toLocalIterator` 명령을 수행하면 어플리케이션과 드라이버가 비정상적으로 종료될 수 있습니다. 또한, 연산을 병렬로 수행하지 않고 차례로 처리하기 떄문에 매우 큰 처리 비용이 발생합니다.

