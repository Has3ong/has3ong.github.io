---
title : Spark Dataset
tags :
- Dataset
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

Dataset 은 구조적 API 의 기본 데이터 타입입니다. DataFrame 은 Row 타입의 Dataset 입니다. Spark 가 지원하는 다양한 언어에서 사용할 수 있습니다. Dataset 은 JVM 을 사용하는 언어인 Scala 와 Java 에서만 사용할 수 있습니다. Dataset 을 사용해 데이터셋의 각 로우를 구성하는 객체를 정의합니다. Scala 에서는 스키마가 정의된 케이스 클래스 객체를 사용하여 Dataset 을 정의합니다. Java 에서는 Java 빈 객체를 사용해 Dataset 을 정의합니다.

Spark 는 StringType, BigIntType, StructType 과 같은 다양한 데이터 타입을 제공합니다. 또한, Spark 가 지원하는 다양한 언어의 String, Integer, Double 같은 데이터 타입을 Spark 의 특정 데이터 타입으로 매핑할 수 있습니다. DataFrame API 를 사용할 때 String 이나 Integer 데이터 타입의 객체를 생성하지는 않지만 Spark 는 Row 객체를 변환해 처리합니다. Scala 나 Java 를 사용할 때 모든 DataFrame 은 Row 타입의 Dataset 을 의미합니다. 도메인별 특정 객체를 효과적으로 지원하기 위해 **인코더(Encoder)** 라 부르는 특수 개념이 필요합니다. 인코더는 도메인별 특정 객체를 Spark 의 내부 데이터 타입으로 매핑하는 시스템입니다.

예를 들어, `name(string)` 과 `age(int)` 를 가지는 `Person` 클래스가 있다고 가정하겠습니다. 인코더는 런타임 환경에서 Person 객체를 바이너리 구조로 직렬화하는 코드를 생성하도록 Spark 에 지시합니다. DataFrame 이나 구조적 API 를 사용한다면 Row 타입을 직렬화된 바이너리 구조로 변환합니다. 도메인에 특화된 객체를 만들어 사용하려면 Scala 의 케이스 클래스나 Java 의 자바빈 형태로 사용자 정의 데이터 타입을 정의해야 합니다. Spark 에서는 Row 타입 대신 사용자가 정의한 데이터 타입을 분산 방식으로 다룰 수 있습니다.

Dataset API 를 사용한다면 Spark 는 데이터셋에 접근할 때마다 Row 포맷이 아닌 사용자 정의 데이터타입으로 변환합니다. 이 변환 작업은 느리긴 하지만 사용자에게 더 많은 유연성을 제공합니다. 사용자 정의 데이터 타입을 사용하면 성능이 나빠지게됩니다. Python 으로 만든 사용자 정의 함수와 비슷한 상황으로 볼 수 있으니 자릿수가 다를 정도로 사용자 정의 함수가 훨씬 더 느립니다. 그 이유는 프로그래밍 언어를 전환하는 것이 사용자 정의 데이터 타입을 사용하는 것보다 훨씬 느리기 때문입니다.

## When to Use Datasets

아래는 Dataset 을 사용해야하는 이유입니다.

* DataFrame 기능만으로 수행할 연산을 표현할 수 없는 경우
* 성능 저하를 감수하더라도 타입 안정성을 가진 데이터 타입을 사용하고 싶은 경우

Dataset 을 사용해야 하는 이유를 알아보겠습니다. 구조적 API 를 사용해 표현할 수 없는 몇 가지 작업이 있습니다. 복잡한 비즈니스 로직을 SQL 이나 DataFrame 대신 단일 함수로 인코딩해야 하는 경우가 있습니다. 이 경우 Dataset 을 사용하는 것이 적합합니다. 또한 Dataset API 는 타입 안정성이 있습니다. 

두 문자열을 사용해 뺄셈 연산을 하는 것처럼 데이터 타입이 유효하지 않은 작업은 런타임이 아닌 컴파일 타임에 오류가 발생합니다. 만약 정확도와 방어적 코드를 중요시한다면 성능을 조금 희생하더라도 Dataset 을 사용하는것이 좋습니다. Dataset API 를 사용하면 잘못된 데이터로부터 어플리케이션을 보호할 수 없지만 보다 우아하게 데이터를 제어하고 구조화할 수 있습니다.

단일 노드의 워크로드와 Spark 워크로드에서 전체 로우에 대한 다양한 트랜스 포메이션을 재사용하려면 Dataset 을 사용하는 것이 적합합니다. Scala 를 사용한 경험이 있다면 Spark 의 API 는 Scala Sequence 타입의 API 가 일부 반영되어 있지만 분산 방식으로 동작하는 것을 알 수 있습니다. 결국 Dataset 을 사용하는 장점은 로컬과 분산 환경의 워크로드에서 재사용할 수 있다는 겁니다. 케이스 클래스로 구현된 데이터 타입을 사용해 모든 데이터와 트랜스포메이션을 정의하면 재사용할 수 있습니다. 또한 올바른 클래스와 데이터 타입이 지정된 DataFrame 을 로컬 디스크에 저장하면 다음 처리과정에서 사용할 수 있어 더 쉽게 데이터를 다룰 수 있습니다.

더 적합한 워크로드를 만들기 위해 DataFrame 과 Dataset 을 동시에 사용할 때가 있습니다. 하지만 성능과 타입 안정성 중 하나는 희생해야 합니다. 이러한 방식은 대량의 DataFrame 기반의 ETL 트랜스포메이션의 마지막 단계에서 사용할 수 있습니다. 예를 들어 드라이버로 데이터를 수집해 단일 노드의 라이브러리로 수집된 데이터를 처리하는 경우입니다. 반대로 트랜스포메이션의 첫 번째 단계에서 사용할 수 있습니다. 예를 들어 Spark SQL 에서 필터링 전에 로우 단위로 데이터를 파싱하는 경우입니다.

## Creating Datasets

Dataset 을 생성하는 것은 수동 작업이므로 정의할 스키마를 미리 알고 있어야 합니다.

### In Java: Encoders

Java 인코더는 매우 간단합니다. 데이터 타입 클래스를 정의한 다음 DataFrame 에 지정해 인코딩할 수 있습니다.

```scala
import org.apache.spark.sql.Encoders;

public class Flight implements Serializable{
  String DEST_COUNTRY_NAME;
  String ORIGIN_COUNTRY_NAME;
  Long DEST_COUNTRY_NAME;
}

Dataset<Flight> flights = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
  .as(Encoders.bean(Flight.class));
```

### In Scala: Case Classes

Scala 에서 Dataset 을 생성하려면 Scala case class 구문을 사용해 데이터 타입을 정의해야 합니다. 케이스 클래스는 다음과 같은 특징을 가진 정규 클래스 입니다.

* 불변성
* 패턴 매칭으로 분해 가능
* 참조값 대신 클래스 구조를 기반으로 비교
* 사용하기 쉽고 다루기 편함

이러한 특징으로 케이스 클래스를 판별할 수 있으므로 데이터 분석시 매우 유용합니다. 케이스 클래스는 불변성을 가지며 값 대신 구조로 비교할 수 있습니다.

Scala 문서는 케이스 클래스를 다음과같이 설명합니다.

* 불변성이므로 객체들이 언제 어디서 변경되었는지 추적할 필요가 없다.
* 값으로 비교하면 인스턴스를 마치 원시 데이터 타입의 값처럼 비교합니다. 그러므로 클래스 인스턴스가 값으로 비교되는지, 참조로 비교되는지 불확실해하지 않아도 됩니다.
* 패턴 매칭은 로직 분기를 단순화해 버그를 줄이고 가독성을 좋게 만든다.

Spark 에서 케이스 클래스를 사용할 때도 이러한 장점은 유지됩니다.

Dataset 을 생성하기 위해 예제 데이터셋 중 하나를 case class 로 정의합니다.

```scala
case class Flight(DEST_COUNTRY_NAME: String,
                  ORIGIN_COUNTRY_NAME: String, count: BigInt)
```

앞서 데이터셋의 레코드를 표현할 case class 를 정의했습니다. 즉, `Flight` 데이터 타입의 DataFrame 을 생성했습니다. `Flight` 데이터 타입은 스키마만 정의되어 있을 뿐 아무런 메소드도 정의되어 있지 않습니다. 데이터를 읽으면 DataFrame 이 반환됩니다. 그리고 `as` 메소드를 사용해 `Flight` 데이터 타입으로 변환합니다.

```scala
val flightsDF = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
val flights = flightsDF.as[Flight]
```

## Actions

지금까지 Dataset 의 특징을 봤습니다. 하지만 Dataset 과 DataFrame 에 `collect`, `take` 그리고 `count` 같은 액션을 적용할 수 있다는 사실이 더 중요합니다.

```scala
flights.show(2)
```

```
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|    1|
|    United States|            Ireland|  264|
+-----------------+-------------------+-----+
```

또한 케이스 클래스에 실제로 접근할 때 어떠한 데이터 타입도 필요하지 않다는 사실을 알아야 합니다. case class 의 속성명을 지정하면 속성에 맞는 값과 데이터 타입 모두를 반환합니다.

```scala
flights.first.DEST_COUNTRY_NAME // United States
```

## Transformations

Dataset 의 트랜스포메이션은 DataFrame 과 동일합니다. DataFrame 의 모든 트랜스포메이션은 Dataset 에서 사용할 수 있습니다.

Dataset 을 사용하면 원형의 JVM 데이터 타입을 다루기 때문에 DataFrame 만 사용해서 트랜스포메이션을 수행하는 것보다 좀 더 복잡하고 강력한 데이터 타입으로 트랜스포메이션을 사용할 수 있습니다. 이전에 사용한 Dataset 에 필터를 적용해보겠습니다.

### Filtering

`Flight` 클래스를 파라미터로 사용해 불리언 값을 반환하는 함수를 만들어 보겠습니다. 불리언 값은 출발지와 도착지가 동일한지 나타냅니다. 이 함수는 사용자 정의 함수가 아닌 일반 함수입니다.

```scala
def originIsDestination(flight_row: Flight): Boolean = {
  return flight_row.ORIGIN_COUNTRY_NAME == flight_row.DEST_COUNTRY_NAME
}
```

위에서 정의한 함수를 `filter` 메소드에 적용해 각 행이 true 를 반환하는 지 평가하고 데이터셋을 필터링할 수 있습니다.

```scala
flights.filter(flight_row => originIsDestination(flight_row)).first()
```

결과는 아래와 같습니다.

```scala
Flight = Flight(United States,United States,348113)
```

이 함수는 Spark 코드에서 호출하지 않아도 됩니다. Spark 코드에서 사용하기 전에 사용자 정의 함수처럼 로컬 머신의 데이터를 대상으로 테스트할 수 있습니다.

예를 들어 아래의 데이터셋은 드라이버에 모을 수 있을 만큼 아주 작기 때문에 동일한 필터 연산을 수행할 수 있습니다.

```scala
flights.collect().filter(flight_row => originIsDestination(flight_row))
```

결과는 아래와 같습니다.

```scala
Array[Flight] = Array(Flight(United States,United States,348113))
```

함수를 사용했을 때와 동일한 결과가 반환됩니다.

### Mapping

필터링은 단순한 트랜스포메이션입니다. 때로는 특정 값을 다른 값으로 **매핑(Mapping)** 해야 합니다. 이전 예제에서 함수를 정의하면서 이미 매핑 작업을 수행했습니다. 정의한 함수는 `Flight` 데이터 타입을 입력으로 사용해 불리언 값을 반환합니다. 하지만 실무에서는 값을 추출하거나 값을 비교하는 것과 같은 정교한 처리가 필요합니다.

Dataset 을 다루는 가장 간단한 예제는 로우의 특정 칼럼을 추출하는 겁니다. DataFrame 에 매핑 작업을 수행하는 것은 Dataset 의 `select` 메소드를 사용하는 것과 같습니다. 다음은 목적지 칼럼을 추출하는 예제입니다.

```scala
val destinations = flights.map(f => f.DEST_COUNTRY_NAME)
```

최종적으로 String 데이터 타입의 Dataset 을 반환합니다. Spark 는 결과로 반환할 JVM 데이터 타입을 알고 있기 때문에 컴파일 타임에 데이터 타입의 유효성을 검사할 수 있습니다.

드라이버는 결괏값을 모아 문자열 타입의 배열로 반환합니다.

```scala
val localDestinations = destinations.take(5)
```

매핑 작업을 사용하면 DataFrame 을 사용하는 것보다 훨씬 정교하게 로우 단위로 처리가 가능합니다.

## Joins

조인은 DataFrame 과 마찬가지로 Dataset 에도 동일하게 적용됩니다. 하지만 Dataset 은 `joinWith` 처럼 정교한 메소드를 제공합니다. `joinWith` 메소드는 `co-group` 과 유사하며 Dataset 안쪽에 다른 두 개의 중첩된 Dataset 으로 구성됩니다. 각 칼럼은 단일 Dataset 이므로 Dataset 객체를 칼럼처럼 다룰 수 있습니다. 그러므로 조인 수행 시 더 많은 정보를 유지할 수 있으며 고급 맵이나 필터처럼 정교하게 데이터를 다룰 수 있습니다.

`joinWith` 메소드를 설명하기 위해 가짜 항공운항 메타데이터 Dataset 을 생성합니다.

```scala
case class FlightMetadata(count: BigInt, randomData: BigInt)

val flightsMeta = spark.range(500).map(x => (x, scala.util.Random.nextLong))
  .withColumnRenamed("_1", "count").withColumnRenamed("_2", "randomData")
  .as[FlightMetadata]

val flights2 = flights
  .joinWith(flightsMeta, flights.col("count") === flightsMeta.col("count"))
```

최종적으로 오누는 `Flight` 와 `FlightMetadata` 로 이루어진 일종의 Key-Value 형태의 Dataset 을 반환합니다. Dataset 이나 복합 데이터 타입의 DataFrame 으로 조회할 수 있습니다.

```scala
flights2.selectExpr("_1.DEST_COUNTRY_NAME")
```

이전 예제처럼 드라이버로 데이터를 모은 다음 결과를 반환합니다.

```scala
flights2.take(2)

Array[(Flight, FlightMetadata)] = Array((Flight(United States,Romania,1),...
```

일반 조인 역시 아주 잘 동작합니다. 하지만 DataFrame 을 반환하므로 JVM 데이터 타입 정보를 모두 잃게 됩니다.

```scala
val flights2 = flights.join(flightsMeta, Seq("count"))
```

이 정보를 다시 얻으려면 다른 Dataset 을 정의해야 합니다. DataFrame 과 Dataset 을 조인하는 것은 문제가 되지 않으며 최종적으로 동일한 결과를 반환합니다.

```scala
val flights2 = flights.join(flightsMeta.toDF(), Seq("count"))
```

## Grouping and Aggregations

그룹화와 집계는 기본 표준을 따르므로 `groupBy`, `rollup`, `cube` 메소드를 사용할 수 있습니다. 하지만 Dataset 대신 DataFrame 을 반환하기 때문에 데이터 타입 정보를 잃게 됩니다.

```scala
flights.groupBy("DEST_COUNTRY_NAME").count()
```

데이터 타입 정보를 잃는 것은 큰 문제는 아니지만, 이를 유지할 수 있는 그룹화와 집계 방법이 있습니다. 한 가지 예로 `groupByKey` 메소드는 Dataset 의 특정 키를 기준으로 그룹화하고 형식화된 Dataset 을 반환합니다. 하지만 이 함수는 칼럼명 대신 함수를 파라미터러 사용해야 합니다. 따라서 다음 예제와 같이 훨씬 더 정교한 그룹화 함수를 사용할 수 있습니다.

```scala
flights.groupByKey(x => x.DEST_COUNTRY_NAME).count()
```

`groupByKey` 메소드의 파라미터 함수를 사용하여 유연성을 얻을 수 있습니다. 하지만 Spark 는 함수와 JVM 데이터 타입을 최적화할 수 없으므로 트레이드오프가 발생합니다. 이로 인해 성능 차이가 발생할 수 있으며 실행 계획으로 그 이유를 확인할 수 있습니다.

아래 예제는 `groupByKey` 메소드를 사용해 DataFrame 에 새로운 칼럼을 추가한 다음 그룹화를 수행합니다.

```scala
flights.groupByKey(x => x.DEST_COUNTRY_NAME).count().explain

== Physical Plan ==
*HashAggregate(keys=[value#1396], functions=[count(1)])
+- Exchange hashpartitioning(value#1396, 200)
   +- *HashAggregate(keys=[value#1396], functions=[partial_count(1)])
      +- *Project [value#1396]
         +- AppendColumns <function1>, newInstance(class ...
         [staticinvoke(class org.apache.spark.unsafe.types.UTF8String, ...
            +- *FileScan parquet [D...
```

Dataset 의 Key 를 이용하여 그룹화를 수행한 다음 결과를 Key-Value 형태로 함수에 전달해 원시 객체 형태로 그룹화된 데이터를 다룰 수 있습니다.

```scala
def grpSum(countryName:String, values: Iterator[Flight]) = {
  values.dropWhile(_.count < 5).map(x => (countryName, x))
}
flights.groupByKey(x => x.DEST_COUNTRY_NAME).flatMapGroups(grpSum).show(5)
+--------+--------------------+
|      _1|                  _2|
+--------+--------------------+
|Anguilla|[Anguilla,United ...|
|Paraguay|[Paraguay,United ...|
|  Russia|[Russia,United St...|
| Senegal|[Senegal,United S...|
|  Sweden|[Sweden,United St...|
+--------+--------------------+
def grpSum2(f:Flight):Integer = {
  1
}
flights.groupByKey(x => x.DEST_COUNTRY_NAME).mapValues(grpSum2).count().take(5)
```

아래 예제처럼 새로운 처리 방법을 생성해 그룹을 **축소(Reduce)** 하는 방법을 정의할 수 있습니다.

```scala
def sum2(left:Flight, right:Flight) = {
  Flight(left.DEST_COUNTRY_NAME, null, left.count + right.count)
}
flights.groupByKey(x => x.DEST_COUNTRY_NAME).reduceGroups((l, r) => sum2(l, r))
  .take(5)
```

`groupByKey` 메소드는 동일한 결과를 반환하지만 데이터 스캔 직후에 집계를 수행하는 `groupBy` 메소드에 비해 더 비싼 처리라는 것을 실행 계획으로 알 수 있습니다.

```scala
flights.groupBy("DEST_COUNTRY_NAME").count().explain

== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#1308], functions=[count(1)])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#1308, 200)
   +- *HashAggregate(keys=[DEST_COUNTRY_NAME#1308], functions=[partial_count(1)])
      +- *FileScan parquet [DEST_COUNTRY_NAME#1308] Batched: tru...
```

사용자가 정의한 인코딩으로 세밀한 처리가 필요하거나 필요한 경우에만 Dataset 의 `groupByKey` 메소드를 사용해야 합니다. Dataset 은 빅데이터 처리 파이프라인의 처음과 끝 작업에서 주로 사용합니다.

