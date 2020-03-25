---
title : Spark Structured API Overview
tags :
- Schema
- Dataset
- DataFrame
- Structured API
- Apache
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

**구조적 API(Structured API)** 는 비정형 로그 파일부터 반정형 CSV 파일, 정형적인 Parquet 파일까지 다양한 데이터를 처리할 수 있습니다.

구조적 API 에는 다음과 같은 3 가지 분산 컬렉션 API 가 있습니다.

* Datasets
* DataFrames
* SQLtables and views

**배치(Batch)** 와 **스티리밍(Streaming)** 처리에 구조적 API 를 사용할 수 있습니다. 구조적 API 를 활용하면 배치 작업을 스트리밍 작업으로 손쉽게 변환할 수 있습니다.

구조적 API 는 데이터 흐름을 정의하는 기본 추상화 개념입니다. 이 포스트에서 반드시 이해해야하는 3 가지 개념을 알아보겠습니다.

* the typed and untyped APIs (and their differences)
* what the core terminology is
* how Spark actually takes your Structured API data flows and executes it on the cluster

## DataFrames and Datasets

Spark 는 DataFrame 과 Dataset 이라는 두 가지 구조화된 컬렉션 개념을 가지고 있습니다. 두 타입을 먼저 정의해보겠습니다.

DataFrame 과 Dataset 은 잘 정의된 로우와 컬럼을 가지는 분산 테이블 형태의 컬렉션입니다. 각 컬럼은 다른 컬럼과 동일한 수의 로우를 가져야 합니다. 컬렉션의 모든 로우는 같은 데이터 타입 정보를 가지고 있어야합니다. DataFrame 과 Dataset 은 결과를 생성하기 위해 어떤 데이터에 연산을 적용해야 하는지 정의하는 지연 연산의 실행 계획이며, 불변성을 가집니다.

DataFrame 에 액션을 호출하면 Spark 는 트랜스포메이션을 실제로 실행하고 결과를 반환합니다.

DataFrame 과 Dataset 을 조금 더 구체적으로 정의하려면 **스키마(Schema)** 를 알아야 합니다. 스키마는 분산컬렉션에 저장할 데이터 타입을 정의하는 방법입니다.

## Schemas

스키마는 DataFrame 의 컬럼명과 데이터 타입을 정의합니다. 스키마는 데이터소스에서 얻거나 직접 정의할 수 있습니다. 스키마는 여러 데이터 타입으로 구성되므로 어떤 데이터 타입이 어느 위치에 있는지 정의하는 방법이 필요합니다.

## Overview of Structured Spark Types

Spark 는 사실상 프로그래밍 언어입니다. Spark 는 실행 계획 수립과 처리에 사용하는 자체 데이터 타입 정보를 가지고 있는 **카탈리스트(Catalyst)** 엔진을 사용합니다.

Spark 는 자체 데이터 타입을 지원하는 여러 언어 API 와 직접 매핑되며, 각 언어에 대한 매핑 테이블을 가지고 있습니다. Python 이나 R 을 이용해 Spark 의 구조적 API 를 사용하더라도 대부분의 연산은 Python 이나 R 의 데이터 타입이 아닌 Spark 의 데이터 타입을 사용합니다.

아래 예제는 Spark 의 덧셈연산입니다.

```scala
// in Scala
val df = spark.range(500).toDF("number")
df.select(df.col("number") + 10)
```

Spark 에서 덧셈 연산이 수행되는 이유는 Spark 가 지원하는 언어를 이용해 작성된 표현식을 카탈리스트 엔진에서 Spark 의 데이터 타입으로 반환해 명령을 처리하기 때문입니다.

### DataFrames Versus Datasets

본질적으로 구조적 API 에는 비타입형인 DataFrame 과 타입형인 Dataset 이 있습니다.

물론 DataFrame 에도 데이터 타입이 있지만, 스키마에 명시된 데이터타입의 일치여부를 런타임이 되어서 확인합니다. Dataset 은 컴파일 타임에 확인합니다. Dataset 은 JVM 기반 언어인 Scala 와 Java 에서만 지원합니다. Dataset 의 데이터 타입을 정의하려면 Scala 의 Case Class 나 Java Bean 을 사용해야합니다.

Spark 의 DataFrame 은 Row 타입으로 구성된 Dataset 입니다. Row 타입은 Spark 가 사용하는 연산에 최적화된 인메모리 포맷의 내부적인 표현 방식입니다. Row 타입을 사용하면 Garbage Collection 과 객체 초기화 부하가 있는 JVM 데이터 타입을 사용하는 대신 자체 데이터 포맷을 사용하기 때문에 매우 효율적인 연산이 가능합니다.

Python 이나 R 에서는 Spark 의 Dataset 을 사용할 수 없지만, 최적화된 포맷인 DataFrame 으로 처리할 수 있습니다.

### Columns

칼럼은 정수형이나 문자열 같은 단순 데이터 타입(a simple type), 배열이나 맵 같은 복합 데이터 타입(a complex type), 그리고 null 값을 표현합니다. Spark 는 데이터 타입의 모든 정보를 추적하며 다양한 칼럼 변환 방법을 제공합니다.

Spark 의 컬럼은 테이블 컬럼으로 생각할 수 있습니다.

### Rows

로우는 데이터 레코드입니다. DataFrame 의 레코드는 Row 타입으로 구성됩니다. 로우는 SQL, RDD, 데이터소스에서 얻거나 직접 만들 수 있습니다. 다음은 `range` 메소드를 사용해 DataFrame 을 생성하는 예제입니다.

```scala
// in Scala
spark.range(2).toDF().collect()
```

Row 객체로 이루어진 배열을 반환합니다.

### Spark Types

Spark 는 여러가지 내부 데이터 타입을 가지고 있습니다. `Table 1`, `Table 2`, `Table 3` 은 프로그래밍 언어의 데이터 타입이 Spark 의 어떤 데이터 타입과 매핑되는지 나타냅니다.

데이터 타입의 컬럼을 초기화하고 정의하는 방법을 알아보겠습니다.

Spark 데이터 타입을 Scala 에서 사용하려면 다음과 같은 코드를 사용합니다.

```scala
import org.apache.spark.sql.types._

val b = ByteType
```

Spark 데이터 타입을 Java 에서 사용하려면 다음 패키지의 팩토리 메소드를 사용합니다.

```java
import org.apache.spark.sql.types.DataTypes;

ByteType x = DataTypes.ByteType;
```

`Table 1` 에서는 Scala 의 데이터 타입과 관련된 제약사항을 확인할 수 있습니다. 

> Table 1 - Scala type reference

|Data Type|Value Type in Scala|API to access or create a data type|
|:--|:--|:--|
|ByteType|Byte|ByteType|
|ShortType|Short|ShortType|
|IntegerType|Int|IntegerType|
|LongType|Long|LongType|
|FloatType|Float|FloatType|
|DoubleType|Double|DoubleType|
|DecimalType|java.math.BigDecimal|DecimalType|
|StringType|String|StringType|
|BinaryType|Array[Byte]|BinaryType|
|BooleanType|Boolean|BooleanType|
|TimestampType|java.sql.Timestamp|TimestampType|
|DataType|java.sql.Date|DateType|
|ArrayType|scala.collection.Seq|`ArrayType(elementType, [containsNull])`|
|MapType|scala.collection.Map|`MapType(keyType, valueType, [valueContainsNull])`|
|StructType|org.apache.spark.sql.Row|`StructType(fields)`|
|StructField|이 필드의 데이터 타입과 대응되는 Scala 데이터 타입입니다.|`StructField(name, dataType, [nullable])`|

## Overview of Structured API Execution

구조적 API 쿼리가 사용자 코드에서 실제 실행 코드로 변환되는 과정을 보겠습니다. 진행 과정은 다음과 같습니다.

1. Write DataFrame/Dataset/SQLCode.
2. If valid code, Spark converts this to a **Logical Plan**.
3. Spark transforms this **Logical Plan** to a **Physical Plan**, checking for optimizations along the way.
4. Spark then executes this **Physical Plan** (RDD manipulations) on the cluster.

작성한 Spark 코드는 콘솔이나 `spark-submit` 쉘 스크립트로 실행합니다. **카탈리스크 옵티마이저(Catalyst Optimizer)** 는 코드를 넘겨 받고 실제 실행 계획을 생성합니다.

마지막으로 Spark 는 코드를 실행한 후 결과를 반환합니다. `Example 1` 에서 전체 과정을 확인할 수 있습니다.

> Example 1 - The Catalyst Optimizer

![image](https://user-images.githubusercontent.com/44635266/77064261-86ba2580-6a22-11ea-8ab7-1c9b6952841d.png)

### Logical Planning

첫 번째 실행 단계에서는 사용자 코드를 논리적 실행 계획으로 변환합니다.

> Example 2 - The structured API logical planning process

![image](https://user-images.githubusercontent.com/44635266/77064287-8faaf700-6a22-11ea-8ba6-5a65b3c61bef.png)

논리적 실행 계획 단계에서는 추상적 트랜스포메이션만 포함합니다. 드라이버나 익스큐터의 정보를 고려하지 않습니다. 그리고 사용자의 다양한 표현식을 최적화된 버전으로 변환합니다.

사용자 코드는 이 과정에서 **검증 전 논리적 실행 계획(Unresolved Logical Plan)** 으로 변환됩니다. 코드의 유효성과 테이블이나 컬럼의 존재 여부만을 판단하는 과정이므로 아직 실행 계획을 검증하지 않은 상태입니다.

Spark **분석기(Analyzer)** 는 컬럼과 테이블을 검증하기 위해 카탈로그, 테이블 저장소, DataFrame 정보를 활용합니다. 필요한 테이블이나 컬럼이 카탈로그에 없다면 검증 전 논리적 실행 계획이 만들어지지 않습니다.

테이블과 컬럼에 대한 검증 결과는 카탈리스트 옵티마이저로 전달됩니다. 옵티마이저는 조건절 푸시다운이나 선택절 구문을 이용해 논리적 실행 계획을 최적화하는 규칙의 모음입니다. 필요한 경우 도메인에 최적화된 규칙을 적용할 수 있는 카탈리스트 옵티마이저의 확장형 패키지를 만들 수 있습니다.

### Physical Planning

Spark 실행 계획이라고도 불리는 **물리적 실행 계획** 은 논리적 실행 계획을 클러스터 환경에서 실행하는 방법을 정의합니다. `Example 3` 처럼 다양한 물리적 실행 전략을 생성하고 비용 모델을 이용해 비교한 후 최적의 전략을 선택합니다.

> Example 3 - The physical planning process

![image](https://user-images.githubusercontent.com/44635266/77064317-9df91300-6a22-11ea-87e3-9244fba17d32.png)

물리적 실행 계획은 일련의 RDD 와 트랜스포메이션으로 변환됩니다. Spark 는 DataFrame, Dataset, SQL 로 정의된 쿼리를 RDD 트랜스포메이션으로 컴파일합니다.

### Execution

Spark 는 물리적 실행 계획을 선정한 다음 저수준 프로그래밍 인터페이슨 RDD 를 대상으로 모든 코드를 실행합니다. Spark 는 런타임에 전체 태스크나 스테이지를 제거할 수 있는 Java 바이트 코드를 생성해 추가적인 최적화를 수행하고 처리 결과를 사용자에게 반환합니다.