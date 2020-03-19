---
title : Spark A Tour of Spark’s Toolset
tags :
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

Spark 에코 시스템은 방대한 기능과 라이브러리를 가지고 있습니다.(`Example 1`) Spark 는 기본 요소인 저수준 API 와 구조적 API 그리고 추가 기능을 제공하는 일련의 표준 라이브러리로 구성되어 있습니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/76521448-33872680-64a8-11ea-9eff-01e136a04df1.png)

Spark 의 라이브러리는 그래프 분석, 머신러닝, 스트리밍 등 다양한 작업을 지원하며, 컴퓨팅 및 스토리지 시스템과의 통합을 돕는 역할을 합니다.

이번 포스팅에서는 다음과 같은 내용을 설명하겠습니다.

* Running production applications with spark-submit
* Datasets: type-safe APIs for structured data
* Structured Streaming
* Machine learning and advanced analytics
* Resilient Distributed Datasets (RDD): Spark’s low level APIs
* SparkR
* The third-party package ecosystem

## Running Production Applications 

Spark 를 사용하면 빅데이터 프로그램을 쉽게 개발할 수 있습니다. `spark-submit` 명령을 사용하여 개발한 프로그램을 운영용 어플레킹션으로 쉽게 전환할 수 있습니다.

`spark-submit` 명령은 어플리케이션 코드를 클러스터에 전송해 실행시키는 역할을 합니다. Spark 어플리케이션은 Standalone, Mesos, YARN 클러스터 매니저를 이용해 실행됩니다.

사용자는 Spark 가 지원하는 프로그래밍 언어로 어플리케이션을 개발한 다음 실행할 수 있습니다. 가장 간단한 방법은 로컬 머신에서 어플리케이션을 실행하는 겁니다. Spark 어플리케이션 예제를 실행해보겠습니다.

```scala
./bin/spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master local \
  ./examples/jars/spark-examples_2.11-2.2.0.jar 10
```
  
위 스칼라 어플리케이션 예제는 $\pi$ 값을 계산합니다.

## Datasets: Type-Safe Structured APIs 

첫 번째로 설명할 API 는 Dataset 입니다. Dataset 은 자바와 스칼라의 정적 데이터 타입에 맞는 코드, 즉 **정적 타입 코드(Statically Typed Code)** 를 지원하기 위해 고안된 Spark 의 구조적 API 입니다. Dataset 은 타입 안정성을 지원하며 동적 타입 언어인 Python 과 R 에서는 사용할 수 없습니다.

DataFrame 은 다양한 데이터 타입의 테이블형 데이터를 보관할 수 있는 Row 타입의 객체로 구성된 분산 컬렉션입니다. Dataset API 는 DataFrame 의 레코드를 사용자가 Java 나 스칼라로 정의한 클래스에 할당하고 자바의 ArrayList 또는 스칼라의 Seq 객체 등의 고정 타입형 컬렉션으로 다룰 수 있는 기능을 제공합니다.

Dataset API 는 **타입 안정성** 을 지원하므로 초기화에 사용한 클래스 대신 다른 클래스를 사용해 접근할 수 없습니다. 따라서 Dataset API 는 다수의 소프트웨어 엔지니어가 잘 정의된 인터페이스로 상호작용하는 대규모 어플리케이션을 개발하는 데 특히 유용합니다.

Dataset 클래스는 내부 객체의 데이터 타입을 매개변수로 사용합니다. 예를 들어 `Dataset[Person]` 은 `Person` 클래스의 객체만 가질 수 있습니다. Spark 2.0 에서 자바의 JavaBean 패턴과 스칼르의 케이스 클래스 유형으로 정의된 클래스를 지원합니다. 

Dataset 은 필요한 경우 선택적으로 사용할 수 있습니다. 예를 들어 아래 예제와 같이 데이터 타입을 정의하고 `map`, `filter` 함수를 사용할 수 있습니다. Spark 는 처리를 마치고 결과를 DataFrame 으로 자동 변환해 반환합니다. 또한 Spark 가 제공하는 여러 함수를 이용해 추가 작업을 할 수 있습니다.

아래 예제는 타입 안정성 함수와 DataFrame 을 사용해 비즈니스 로직을 신속하게 작성하는 방법을 보여주는 간단한 예제입니다.

```scala
// in Scala
case class Flight(DEST_COUNTRY_NAME: String,
                  ORIGIN_COUNTRY_NAME: String,
                  count: BigInt)
val flightsDF = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
val flights = flightsDF.as[Flight]
```

마지막으로 알아볼 Dataset 의 장점은 `collect` 메소드나 `take` 메소드를 호출하면 DataFrame 을 구성하는 Row 타입의 객체가 아닌 Dataset 에 매개변수로 지정한 타입의 객체를 반환하는 겁니다.

따라서 코드 변경 없이 타입 안정성을 보장할 수 있으며 로컬이나 분산 클러스터 환경에서 데이터를 안전하게 다룰 수 있습니다.

```scala
// in Scala
flights
  .filter(flight_row => flight_row.ORIGIN_COUNTRY_NAME != "Canada")
  .map(flight_row => flight_row)
  .take(5)

flights
  .take(5)
  .filter(flight_row => flight_row.ORIGIN_COUNTRY_NAME != "Canada")
  .map(fr => Flight(fr.DEST_COUNTRY_NAME, fr.ORIGIN_COUNTRY_NAME, fr.count + 5))
```

## Structured Streaming 

구조적 스티리밍은 Spark 2.2 버전에서 안정화된 스트림 처리용 고수준 API 입니다. 구조적 스트리밍을 사용하면 구조적 API 로 개발된 배치 모드의 연사을 스트리밍 방식으로 실행하여, 지연 시간을 줄이고 증분 처리할 수 있습니다.

샘플 데이터를 확인하면 데이터 구조를 확인할 수 있습니다.

```scala
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,2010-12-01 08:26:00,2.55,17...
536365,71053,WHITE METAL LANTERN,6,2010-12-01 08:26:00,3.39,17850.0,United Kin...
536365,84406B,CREAM CUPID HEARTS COAT HANGER,8,2010-12-01 08:26:00,2.75,17850...
```

정적 데이터셋의 데이터를 분석해 DataFrame 을 생성합니다. 정적 데이터셋의 스키마도 함께 생성합니다.

```scala
// in Scala
val staticDataFrame = spark.read.format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/data/retail-data/by-day/*.csv")

staticDataFrame.createOrReplaceTempView("retail_data")
val staticSchema = staticDataFrame.schema
```

특정 고객이 대량으로 구매하는 영업 시간을 살펴보겠습니다. 총 구매비용 컬럼을 추가하고 고객이 가장 많이 소비한 날을 찾아보겠습니다.

윈도우 함수는 집계 시에 시계열 컬럼을 기준으로 각 날짜에 대한 전체 데이터를 가지는 윈도우를 구성합니다. 윈도우는 간격을 통해 처리 요건을 명시할 수 있기 때문에 날짜와 타임스탬프 처리에 유용합니다. Spark 는 관련 날짜의 데이터를 그룹화합니다.

```scala
// in Scala
import org.apache.spark.sql.functions.{window, column, desc, col}

staticDataFrame
  .selectExpr(
    "CustomerId",
    "(UnitPrice * Quantity) as total_cost",
    "InvoiceDate")
  .groupBy(
    col("CustomerId"), window(col("InvoiceDate"), "1 day"))
  .sum("total_cost")
  .show(5)
```

SQL 코드를 사용해 동일한 작업을 할 수 있습니다. 결과는 아래와 같습니다.

```scala
+----------+--------------------+------------------+
|CustomerId|              window|   sum(total_cost)|
+----------+--------------------+------------------+
|   17450.0|[2011-09-20 00:00...|          71601.44|
...
|      null|[2011-12-08 00:00...|31975.590000000007|
+----------+--------------------+------------------+
```

null 값을 가진 결과는 트랜잭션에 `customerId` 값이 없음을 의미합니다.

로컬 모드로 이 코드를 실행하려면 로컬 모드에 적합한 셔플 파티션 수를 설정하는 것이 좋습니다. 셔플 파티션 수는 셔플 이후에 생성될 파티션 수를 의미합니다. 디폴트 값은 200 입니다.

```scala
spark.conf.set("spark.sql.shuffle.partitions", "5")
```

`maxFilesPerTrigeer` 옵션을 지정하면, 한 번에 읽을 파일 수를 설정할 수 있습니다. 

```scala
val streamingDataFrame = spark.readStream
  .schema(staticSchema)
  .option("maxFilesPerTrigger", 1)
  .format("csv")
  .option("header", "true")
  .load("/data/retail-data/by-day/*.csv")
```

이제 DataFrame 이 스트리밍 유형인지 확인할 수 있습니다.

```scala
streamingDataFrame.isStreaming // returns true
```

기존 DataFrame 처리와 동일한 비즈니스 로직을 적용해보겠습니다. 다음 코드는 총 판매 금액을 계산합니다.

```scala
// in Scala
val purchaseByCustomerPerHour = streamingDataFrame
  .selectExpr(
    "CustomerId",
    "(UnitPrice * Quantity) as total_cost",
    "InvoiceDate")
  .groupBy(
    $"CustomerId", window($"InvoiceDate", "1 day"))
  .sum("total_cost")
```

이 작업 역시 **지연 연산(Lazy Operation)** 이므로 데이터 플로를 실행하기 위해 스트리밍 액션을 호출해야 합니다.

스티리밍 액션은 어딘가에 데이터를 채워 넣어야 하므로 `count` 메소드와 같은 일반적인 액션과는 다른 특성을 가집니다. 스트리밍 액션은 **트리거(Trigger)** 가 실행된 다음 데이터를 갱신하게 될 인메모리 테이블에 데이터를 저장합니다.

아래 예제에서는 파일마다 트리거를 실행합니다. Spark 는 집계값보다 더 큰 값이 발생한 경우에만 인메모리 테이블을 갱신하여 언제나 가장 큰 값을 얻을 수 있습니다.

```scala
// in Scala
purchaseByCustomerPerHour.writeStream
  .format("memory") // memory = store in-memory table
  .queryName("customer_purchases") // the name of the in-memory table
  .outputMode("complete") // complete = all the counts should be in the table
  .start()
```

스트림이 시작되면 쿼리 실행 결과가 어떠한 형태로 인메모리 테이블에 기록되는지 확인할 수 있습니다.

```scala
// in Scala
spark.sql("""
  SELECT *
  FROM customer_purchases
  ORDER BY `sum(total_cost)` DESC
  """)
  .show(5)
```

더 많은 테이블을 읽을수록 테이블 구성이 바뀌는것을 알 수 있습니다. 또한, 상황에 따라 처리 결과를 콘솔에 출력할 수 있습니다.

```scala
purchaseByCustomerPerHour.writeStream
  .format("console")
  .queryName("customer_purchases_2")
  .outputMode("complete")
  .start()
```

## Machine Learning and Advanced Analytics 

Spark 에선 머신러닝 알고리즘 라이브러리인 MLlib 를 사용해 대규모 머신러닝을 수행할 수 있습니다.

MLlib 을 사용하면 대용량 데이터를 대상으로 **전처리(Preprocessing)**, **멍잉(Munging)**, **모델 학습(Model Training)**, **예측(Prediction)** 을 할 수 있습니다. 구조적 스트리밍에서 예측할 때도 MLlib 에서 학습시킨 예측 모델을 사용할 수 있습니다.

Spark 는 **분류(Classification)**, **회귀(Regression)**, **군집화(Clustering)** 그리고 **딥 러닝(Deep Learning)** 까지 머신러닝과 관련된 API 를 제공합니다.

k-평균 이라는 표준 알고리즘을 이용해 군집화를 수행해보겠습니다.

> k-평균 : 데이터에서 k 개의 중심이 임의로 할당되는 군집화 알고리즘. 중심점에 가까운 점들을 군집에 할당하고 할당된 점들의 중심을 계산합니다. 이 중심점을 **센트로이드(Centroid)** 라 합니다. 해당 센트로이드에 가까운 점들의 군집에 레이블을 지정하고, 새로 계산한 중심으로 센트로이드를 이동시킵니다. 이 과정을 정해진 횟수나 수렴할 때까지 반복합니다.

다음 예제는 원본 데이터를 올바른 포맷으로 만드는 트랜스포메이션을 정의하고, 모델을 학습한 뒤 예측을 수행합니다.

```scala
staticDataFrame.printSchema()

root
|-- InvoiceNo: string (nullable = true)
|-- StockCode: string (nullable = true)
|-- Description: string (nullable = true)
|-- Quantity: integer (nullable = true)
|-- InvoiceDate: timestamp (nullable = true)
|-- UnitPrice: double (nullable = true)
|-- CustomerID: double (nullable = true)
|-- Country: string (nullable = true)
```

MLlib 의 머신러닝을 사용하기 위해선 수치형 데이터가 필요합니다. 예제의 데이터는 타임스탬프, 정수, 문자열 등 다양한 데이터 타입으로 이루어져 있으므로 수치형으로 변환해야 합니다. 다음은 몇 가지 DataFrame 트랜스포메이션을 사용해 날짜 데이터를 다루는 예제입니다.

```scala
// in Scala
import org.apache.spark.sql.functions.date_format

val preppedDataFrame = staticDataFrame
  .na.fill(0)
  .withColumn("day_of_week", date_format($"InvoiceDate", "EEEE"))
  .coalesce(5)
```

다음 데이터를 학습 데이터셋과 테스트 데이터셋으로 분리합니다. 예제에서는 특정 구매가 이루어진 날짜를 기준으로 직접 분리합니다.

`TrainValidationSplit` 이나 `CrossValidator` 를 사용해 테스트 데이터셋을 생성할 수 있습니다.

```scala
// in Scala
val trainDataFrame = preppedDataFrame
  .where("InvoiceDate < '2011-07-01'")
val testDataFrame = preppedDataFrame
  .where("InvoiceDate >= '2011-07-01'")
```

데이터가 준비되었으니 액션을 호출해 데이터를 분리하겠습니다. 예제의 데이터는 시계열 데이터셋으로 임의 날짜를 기준으로 데이터를 분리합니다.

위 예제의 코드는 데이터셋을 대략 절반으로 나눕니다.

```scala
trainDataFrame.count()
testDataFrame.count()
```

Spark MLlib 은 일반적인 트랜스포메이션을 자동화하는 다양한 트랜스포메이션을 제공합니다. 그 중 하나가 바로 `StringIndexer` 입니다.

```scala
// in Scala
import org.apache.spark.ml.feature.StringIndexer

val indexer = new StringIndexer()
  .setInputCol("day_of_week")
  .setOutputCol("day_of_week_index")
```

위 예제는 요일을 수칳영으로 반환합니다. 예를 들어 토요일을 6, 월요일을 1 로 반환합니다. 하지만 이런 번호 지정 체계는 수치로 표현되어 암묵적으로 토요일이 월요일보다 더 크다는 것을 의미합니다. 이 문제점을 보완하기 위해서는 `OneHotEncoder` 를 사용해 각 값을 자체 컬럼으로 인코딩해야 합니다.

이렇게 하면 특정 요일이 해당 요일인자 아닌지 Boolean 타입으로 나타낼 수 있습니다.

```scala
// in Scala
import org.apache.spark.ml.feature.OneHotEncoder

val encoder = new OneHotEncoder()
  .setInputCol("day_of_week_index")
  .setOutputCol("day_of_week_encoded")
```

위 예제의 결과는 벡터 타입을 구성한 컬럼 중 하나로 사용됩니다. Spark 의 모든 머신러닝 알고리즘은 수치형 벡터 타입을 입력으로 사용합니다.

```scala
// in Scala
import org.apache.spark.ml.feature.VectorAssembler

val vectorAssembler = new VectorAssembler()
  .setInputCols(Array("UnitPrice", "Quantity", "day_of_week_encoded"))
  .setOutputCol("features")
```

위 예제는 3 가지 핵심 특징인 `UnitPrice`, `Quantity`, `day_of_week_encoded` 를 가지고 있습니다. 다음은 입력값으로 들어올 데이터가 같은 프로세스를 거쳐 변환되도록 파이프라인을 설정하는 예제입니다.

```scala
// in Scala
import org.apache.spark.ml.Pipeline

val transformationPipeline = new Pipeline()
  .setStages(Array(indexer, encoder, vectorAssembler))
```

학습 준비 과정은 2 단계로 이루어집니다. 우선 **변환자(Transformer)** 를 데이터셋에 **적합(Fit)** 시켜야합니다. 기본적으로 `StringIndexer` 는 인덱싱할 고윳값의 수를 알아야 합니다. 고윳값의 수를 알 수 있다면 인코딩을 매우 쉽게 할 수 있지만, 만약 알수 없다면 컬럼에 있는 모든 고윳값을 조사하고 인덱싱해야 합니다.

```scala
// in Scala
val fittedPipeline = transformationPipeline.fit(trainDataFrame)
```

학습 데이터셋에 변환자를 적합시키고 나면 학습을 위한 **맞춤 파이프라인(Fitted Pipeline)** 이 준비됩니다. 그리고 이것을 사용해서 일관되고 반복적인 방식으로 모든 데이터를 변환할 수 있습니다.

```scala
// in Scala
val transformedTraining = fittedPipeline.transform(trainDataFrame)
```

동일한 트랜스포메이션을 계속 반복할 수 없으므로 모델에 일부 하이퍼 파라미터 튜닝값을 적용합니다. 캐싱을 사용하면 중간 변환된 데이터셋의 복사본을 메모리에 저장하므로 전체 파이프라인을 재실행하는 것보다 훨씬 반복적으로 데이터셋에 접근할 수 있습니다.

아래 코드를 제거하여 예제를 동작시키면 캐싱의 차이를 알 수 있습니다.

```scala
transformedTraining.cache()
```

학습 데이터셋이 완성되어 모델을 학습할 차례입니다. 머신러닝 모델을 사용하려면 관련 클래스를 임포트하고 인스턴스를 생성해야 합니다.

```scala
// in Scala
import org.apache.spark.ml.clustering.KMeans
val kmeans = new KMeans()
  .setK(20)
  .setSeed(1L)
```

Spark 에서 머신러닝 모델을 학습시키는 과정은 크게 2 단계입니다. 첫 번재 단계는 아직 학습되지 않은 모델을 초기화하고, 두 번째 단계는 해당 모델을 학습시킵니다. MLlib 의 DataFrame API 에서 제공하는 모든 알고리즘은 항상 두 가지 유형으로 구성되어 다음과 같은 명명 규칙을 따릅니다.

* 학습 전 알고리즘 명칭 : Algorithm
* 학습 후 알고리즘 명칭 : AlgorithmModel

이번 예제에서는ㄴ `KMeans` 와 `KMeansModel` 이 학습 전 / 후 알고리즘 명칭입니다.

MLlib 의 DataFrame API 에서 제공하는 **추정자(Estimator)** 는 앞서 사용한 전처리 변환자와 동일한 인터페이스를 가지고 있습니다. 이 인터페이스를 사용해 전체 파이프라인의 학습 과정을 단순화할 수 있습니다.

```scala
// in Scala
val kmModel = kmeans.fit(transformedTraining)
```

모델 학습이 완료되면 성과 평가지표에 따라 학습 데이터셋에 대한 비용을 계산할 수 있습니다. 예제에서 사용한 데이터셋의 군집 비용은 상당히 높은 편입니다. 입력 데이터에 대한 전처리와 표준화 작업이 이루어지지 않았기 때문입니다.

```scala
kmModel.computeCost(transformedTraining)

val transformedTest = fittedPipeline.transform(testDataFrame)

kmModel.computeCost(transformedTest)
```

예제 모델은 개선할 부분이 많습니다. 더 많은 전처리 과정을 추가하고, 하이퍼파라미터 값을 튜닝하면 더 좋은 모델을 만들 수 있습니다.

## Lower-Level APIs 

Spark 는 거의 모든 기능은 RDD 기반으로 만들어졌습니다. DataFrame 연산도 RDD 기반으로 만들어져서 편리하고 매우 효율적인 분산처리를 위해 저수준 명령으로 컴파일됩니다.

원시 데이터를 읽거나 다루는 용도로 RDD 를 사용할 수 있지만 구조적 API 를 사용하는 것이 좋습니다. 하지만 RDD 를 이용해 파티션과 같은 물리적 실행 특성을 결정할 수 있으므로 DataFrame 보다 더 세밀한 제어를 할 수 있습니다.

또한, 드라이버 시스템의 메모리에 저장된 원시 데이터를 병렬처리 하는 데 RDD 를 사용할 수 있습니다. 아래는 간단한 숫자를 이용해 병렬화해 RDD 를 생성하는 예제입니다. 그 다음 DataFrame 으로 변환합니다.

```scala
// in Scala
spark.sparkContext.parallelize(Seq(1, 2, 3)).toDF()

spark.sparkContext.parallelize([Row(1), Row(2), Row(3)]).toDF()
```

RDD 는 Scala 뿐만 아니라 Python 에서도 사용할 수 있습니다.

## SparkR 

SparkR 은 Spark 를 R 언어로 사용하기 위한 기능입니다. Python 대신 R 구문을 사용하는 점만 다릅니다.

```r
# in R
library(SparkR)
sparkDF <- read.df("/data/flight-data/csv/2015-summary.csv",
  source = "csv", header="true", inferSchema = "true")
take(sparkDF, 5)

# in R
collect(orderBy(sparkDF, "count"), 20)
```

R 사용자는 `magrittr` 의 `pipe` 연산자와 같은 R 라이브러리를 사용해 Spark 트랜스포메이션 과정을 R 과 유사하게 만들 수 있습니다. 이 특징을 활용하면 정교한 플로팅(Plotting) 작업을 지원하는 `ggplot` 과 같은 라이브러리를 손쉽게 사용할 수 있습니다.

```r
# in R
library(magrittr)
sparkDF %>%
  orderBy(desc(sparkDF$count)) %>%
  groupBy("ORIGIN_COUNTRY_NAME") %>%
  count() %>%
  limit(10) %>%
  collect()
```