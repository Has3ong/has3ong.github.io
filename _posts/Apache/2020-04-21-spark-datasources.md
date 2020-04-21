---
title : Spark Data Sources
tags :
- Text
- JDBC
- ORC
- Parquet
- JSON
- CSV
- Data Source
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

다음은 Spark 의 핵심 데이터소스입니다.

* CSV
* JSON
* Parquet
* ORC
* JDBC / ODBC Connection
* Plain-text files

Spark 에는 커뮤니티에서 만든 수많은 데이터소스가 존재합니다. 그중 일부는 다음과 같습니다.

* Cassandra
* HBase
* MongoDB
* AWS Redshift
* XML

## The Structure of the Data Sources API

특정 포멧을 읽고 쓰는 방법을 알아보기전에 데이터소스 API 의 전체 구조를 알아보겠습니다.

### Read API Structure

데이터 읽기의 핵심 구조는 다음과 같습니다.

```scala
DataFrameReader.format(...).option("key", "value").schema(...).load()
```

모든 데이터소스를 일긍ㄹ 때 위와 같은 형식을 사용합니다. `format` 메소드느 선택적으로 사용할 수 있으며, 기본값은 Parquet 포맷입니다. `option` 메소드는 데이터를 읽는 방법에 대한 파라미터를 Key - Value 쌍으로 설정할 수 있습니다.

마지막으로 `schema` 메소드는 데이터소스에서 스키마를 제공하거나, 스키마 추론 기능을 사용하려는 경우에 선택적으로 사용할 수 있습니다.

### Basics of Reading Data

Spark 에 데이터를 읽을 때 기본적으로 DataFrameReader 를 사용합니다. DataFrameReader 는 SparkSession 의 `read` 속성으로 접근합니다.

```
spark.read
```

DataFrameReader 를 얻은 다음에는 다음과 같은 값을 지정해야 합니다.

* The format
* The schema
* The read mode
* A series of options

포맷, 스키마, 옵션은 트랜스포메이션을 추가로 정의할 수 있는 DataFrameReader 를 반환합니다. 그리고 읽기 모드를 제외한 3 가지 항목은 필요한 경우에만 선택적으로 지정할 수 있습니다. 

데이터소스마다 데이터를 읽는 방식을 결정할 수 있는 옵션을 제공합니다. 사용자는 DataFrameReader 에 반드시 데이터를 읽을 경로를 지정해야 합니다. 전반적인 코드 구성은 다음곽 같습니다.

```scala
```

옵션을 설정할 수 있는 방법은 다양합니다.

#### READ MODES

외부 데이터소스에서 데이터를 읽다 보면 자연스럽게 형식에 맞지 않는 데이터를 만나게 됩니다. 특히 반정형 데이터소스를 다룰 때 많이 발생합니다. 읽기 모드는 Spark 가 형식에 맞지 않는 데이터를 만났을 때의 동작 방식을 지정하는 옵션입니다.

아래 표에 읽기 모드의 종류를 나타냈습니다.

|Read mode|Description|
|:--|:--|
|`permissive`|오류 레코드의 모든 필드를 `null` 로 설정하고 모든 오류 레코드를 `_corrupt_record` 라는 문자열 칼럼에 기롭합니다.|
|`dropMalformed`|형시에 맞지 않는 레코드가 포함된 로우를 제거합니다.|
|`failFast`|형식에 맞지 않는 레코드를 만나면 즉시 종료합니다.|

읽기 모드의 기본값은 `permissive` 입니다.

### Write API Structure

데이터 쓰기의 핵심 구조는 다음과 같습니다.

```scala
DataFrameWriter.format(...).option(...).partitionBy(...).bucketBy(...).sortBy(...).save()
```

모든 데이터소스에 데이터를 쓸 때 위와 같은 형식을 사용합니다. `format` 메소드는 선택적으로 사용할 수 있으며 기본값은 Parquet 포맷입니다. 그리고 `option` 메소드를 사용해 데이터 쓰기 방법을 설정할 수 있습니다.

`partitionBy`, `bucketBy` 그리고 `sortBy` 메소드는 파일 기반의 데이터소스에서만 동작하며, 이 기능으로 최종 파일 배치 형태를 제어할 수 있습니다.

### Basics of Writing Data

데이터 쓰기는 데이터 읽기와 매우 유사하며, DataFrameReader 대신 DataFrameWriter 를 사용합니다. 데이터소스에 항상 데이터를 기록해야 하기 때문에 DataFrame 의 `write` 속성을 이용해 DataFrame 별로 DataFrameWriter 에 접근해야 합니다.

```scala
// in Scala
dataFrame.write
```

DataFrameWriter 를 얻은 다음에는 `format`, `option`, `save` 모드를 저장해야 하며, 데이터가 저장될 경로를 반드시 입력해야합니다.

```scala
// in Scala
dataframe.write.format("csv")
  .option("mode", "OVERWRITE")
  .option("dateFormat", "yyyy-MM-dd")
  .option("path", "path/to/file(s)")
  .save()
```

#### SAVE MODES

저장 모드는 Spark 가 지정된 위치에서 동일한 파일이 발견했을 때의 동작 방식을 지원하는 옵션입니다. 아래 표는 저장 모드의 종류입니다.

|Save Mode|Description|
|:--|:--|
|`append`|해당 경로에 이미 존재하는 파일 목록에 결과 파일을 추가.|
|`overwrite`|이미 존재하는 모든 데이터를 덮어쓴다.|
|`errorIfExists`|해당 경로에 데이터나 파일이 존재하는 경우 오류를 발생시키며 쓰기 작업이 실패.|
|`ignore`|해당 경로에 데이터나 파일이 존재하는 경우 아무런 처리도 하지 않는다.|

기본값은 `errorIfExists` 입니다. 즉, Spark 가 파일을 저장할 경로에 데이터나 파일이 이미 존재하면 쓰기 작업은 즉시 실패한합니다.

## CSV Files

**CSV(Comma-Separated Values)** 는 콤마(`,`) 로 구분된 값을 의미합니다. CSV 는 각 줄이 단일 레코드가 되며 레코드의 각 필드를 콤마루 구분하는 일반적인 텍스트 파일 포맷입니다.

CSV 파일은 구조적으로 보이지만, 까다로운 파일 포맷 중 하나입니다. 그 이유는 운영 환경에서 어떤 내용이 들어있는지, 어떤 구조로 되어 있는지 등 다양한 전제를 만들어낼 수 없기 때문입니다. 그렇기 때문에 CSV reader 는 다양한 옵션을 제공합니다.

### CSV Options

아래 표는 CSV reader 에서 사용할 수 있는 옵션입니다.

|Read/write|Key|Potential values|Default|Description|
|:--|:--|:--|:--|:--|
|Read|`sep`|Any single string character|,|각 필드와 값을 구분하는 데 사용하는 단일 문자|
|Both|`header`|true, false|false|첫 번째 줄이 칼럼명인지 나타내는 불리언값|
|Read|`escape`|Any string characte|\|Spark 가 파일에서 이스케이프 처리할 문자|
|Read|`inferSchema`|true, false|false|Spark 가 파일을 읽을때 칼럼의 데이터 타입을 추론할지 정의|
|Read|`ignoreLeadingWhiteSpace`|true, false|false|값을 읽을 때 값의 선행 공백을 무시할지 정의|
|Read|`ignoreTrailingWhiteSpace`|true, false|false|값을 읽을 때 값의 후행 공백을 무시할지 정의|
|Both|`nullValue`|Any string characte|""|파일에서 null 값을 나타내는 문자|
|Both|`nanValue`|Any string characte|NaN|CSV 파일에서 NaN 이나 값없음을 나타내는 문자를 선언|
|Both|`positiveInf`|Any string or character|Inf|양의 무한 값을 나타내는 문자를 선언|
|Both|`negativeInf`|Any string or character|-Inf|음의 무한 값을 나타내는 문자를 선언|
|Both|`compression` or `codec`|None, uncompressed, bzip2, deflate, gzip, lz4, or snappy|none|Spark 가 파일을 읽고 쓸 때 사용하는 압축 코덱을 정의|
|Both|`dateFormat`|Any string or character that conforms to java’s `SimpleDataFormat`.|yyyy-MM-dd|날짜 데이터 타입인 모든 필드에서 사용할 날짜 형식|
|Both|`timestampFormat`|Any string or character that conforms to java’s `SimpleDataFormat`.|yyyy-MM-dd’T’HH:mm​:ss.SSSZZ|타임스탬프 데이터 타입인 모든 필드에서 사용할 날짜 형식|
|Read|`maxColumns`|Any integer|20480|파일을 구성하는 최대 칼럼 수를 선언|
|Read|`maxCharsPerColumn`|Any integer|1000000|칼럼의 문자 최대 길이를 선언|
|Read|`escapeQuotes`|true, false|true|Spark 가 파일의 라인에포함된 인용부호를 이스케이프할지 선언|
|Read|`maxMalformedLogPerPartition`|Any integer|10|Spark 가 파티션별로 비정상적인 레코드를 발견했을 때 기록할 최대 수, 이 숫자를 초과하는 레코드는 무시됨|
|Write|`quoteAll`|true, false|false|인용부호 문자가 있는 값을 이스케이프 처리하지 않고, 전체 값을 인용 부호로 묶을지 여부|
|Read|`multiLine`|true, false|false|하나의 논리적 레코드가 여러 줄로 이루어진 CSV 파일 읽기를 허용할지 여부|

### Reading CSV Files

CSV 파일을 읽으려면 먼저 CSV 용 DataFrameReader 를 생성합니다.

```scala
spark.read.format("csv")
```

그 다음 스키마와 읽기 모드를 지정합니다. 이제 몇 가지 옵션을 지정해보겠습니다. 앞에서 보았던 옵션도 있지만, 아직 보지 못한 옵션도 있습니다. `header` 옵션은 CSV 파일을 읽기 위해 `true` 로 `mode` 옵션은 `FAILFAST` 로 `inferSchema` 옵션은 `true` 로 설정합니다.

```scala
// in Scala
spark.read.format("csv")
  .option("header", "true")
  .option("mode", "FAILFAST")
  .option("inferSchema", "true")
  .load("some/path/to/file.csv")
```

아래와 같이 생성한 스키마를 파일의 데이터가 예상한 형태로 이루어져있는지 검증하는 용도로 사용할 수 있습니다.

```scala
// in Scala
import org.apache.spark.sql.types.{StructField, StructType, StringType, LongType}
val myManualSchema = new StructType(Array(
  new StructField("DEST_COUNTRY_NAME", StringType, true),
  new StructField("ORIGIN_COUNTRY_NAME", StringType, true),
  new StructField("count", LongType, false)
))
spark.read.format("csv")
  .option("header", "true")
  .option("mode", "FAILFAST")
  .schema(myManualSchema)
  .load("/data/flight-data/csv/2010-summary.csv")
  .show(5)
```

데이터의 포맷이 맞지않으면 에러가 발생합니다.

현재 스키마의 모든 칼럼의 데이터타입을 `LongType` 으로 변경시켜보겠습니다. 실제 스키마와 일치하지는 않지만 Spark 는 에러를 발생시키지 않습니다. 문제는 Spark 가 실제로 데이터를 읽어들이는 시점에서 발생합니다.

데이터가 지정된 스키마에 일치하지 않으므로 Spark 잡은 시작하자마자 종료됩니다.

```scala
// in Scala
val myManualSchema = new StructType(Array(
                     new StructField("DEST_COUNTRY_NAME", LongType, true),
                     new StructField("ORIGIN_COUNTRY_NAME", LongType, true),
                     new StructField("count", LongType, false) ))

spark.read.format("csv")
  .option("header", "true")
  .option("mode", "FAILFAST")
  .schema(myManualSchema)
  .load("/data/flight-data/csv/2010-summary.csv")
  .take(5)
```

Spark 는 지연 연산 특성이 있어 DataFrame 정의 시점이 아닌 잡 실행 시점에만 오류가 발생합니다. 예를 들어 DataFrame 을 정의하는 시점에 존재하지 않는 파일을 지정해도 오류가 발생하지 않습니다.

### Writing CSV Files

데이터 읽기와 마찬가지로 CSV 파일을 쓸 때 사용할 수 있는 다양한 옵션이 있습니다. `maxColumns` 와 `inferSchema` 옵션 같이 데이터 쓰기에는 적용되지 않는 옵션을 제외하면 데이터 읽기와 동일한 옵션을 제공합니다.

```scala
// in Scala
val csvFile = spark.read.format("csv")
  .option("header", "true").option("mode", "FAILFAST").schema(myManualSchema)
  .load("/data/flight-data/csv/2010-summary.csv")
```

CSV 파일을 읽어 TSV 파일 처리도 가능합니다.

```scala
// in Scala
csvFile.write.format("csv").mode("overwrite").option("sep", "\t")
  .save("/tmp/my-tsv-file.tsv")
```

디렉토리에 가서 `ls` 명령을 실행하면 *my-tsv-file* 은 여러 파일 들어 있는 디렉토리라는 사실을 알 수 있습니다.

```shell
$ ls /tmp/my-tsv-file.tsv/

/tmp/my-tsv-file.tsv/part-00000-35cf9453-1943-4a8c-9c82-9f6ea9742b29.csv
```

이 명령은 실제로 데이터를 쓰는 시점에 DataFrame 파티션 수를 반영합니다. 만약 사전에 데이터를 분할했다면 파일 수가 달라집니다.

## JSON Files

Spark 에서 JSON 파일을 사용할 때 줄로 구분된 JSON 을 기본적으로 사용합니다. 이는 큰 JSON 객체나 배열을 하나씩 가지고 있는 파일을 다루는것과 다릅니다.

`multiline` 옵션을 사용해 줄로 구분된 방식과 여러 줄로 구성된 방식을 선택적으로 사용할 수 있습니다. 이 옵션을 true 로 설정하면 전체 파일을 하나의 JSON 객체로 읽을 수 있습니다.

Spark 는 JSON 파일을 파싱한 다음 DataFrame 을 생성합니다. 줄로 구분된 JSON 은 전체 파일을 읽은 다음 저장하는 방식이 아니므로 새로운 레코드를 추가할 수 있습니다. 다른 포맷에 비해 안정적인 포맷이므로 이 방식을 사용하는 것이 좋습니다.

JSON 은 객체기 때문에 CSV 보다 옵션 수가 적습니다.

### JSON Options

|Read/write|Key|Potential values|Default|Description|
|:--|:--|:--|:--|:--|
|Both|`compression` or `codec`|None, uncompressed, bzip2, deflate, gzip, lz4, or snappy|none|Spark 가 파일을 읽고 쓸 때 사용하는 압축 코덱을 정의|
|Both|`dateFormat`|Any string or character that conforms to Java’s `SimpleDataFormat`.|yyyy-MM-dd|날짜 데이터 타입인 모든 필드에서 사용할 날짜 형식을 정의|
|Both|`timestampFormat`|Any string or character that conforms to Java’s `SimpleDataFormat`.|yyyy-MM-dd’T’HH:​mm:ss.SSSZZ|타임스탬프 데이터 타입인 모든 필드에서 사용할 날짜 형식을 정의|
|Read|`primitiveAsString`|true, false|false|모든 프리미티브 값을 문자열로 추정할지 정의|
|Read|`allowComments`|true, false|false|JSON 레코드에서 Java 나 C++ 스타일로 된 커멘트를 무시할지 정의|
|Read|`allowUnquotedFieldNames`|true, false|false|인용부호로 감싸여 있지 않은 JSON 필드명을 허용할지 정의|
|Read|`allowSingleQuotes`|true, false|true|인용부호로 큰따옴표(") 대신 (') 를 허용할지 정의|
|Read|`allowNumericLeadingZeros`|true, false|false|숫자 앞에 0 을 허용할지 정의 (ex:00012)|
|Read|`allowBackslashEscapingAnyCharacter`|true, false|false|백슬래시 인용부호 메커니즘을 사용한 인용부호를 허용할지 정의|
|Read|`columnNameOfCorruptRecord`|Any string|Value of `spark.sql.column&NameOfCorruptRecord`|`permissive` 모드에서 생성된 비정상 문자열을 가진 새로운 필드명을 변경할 수 있습니다. 이 값을 설정하면 `spark.sql.columnNameOfCorruptRecord` 설정값 대신 적용됩니다.|
|Read|`multiLine`|true, false|false|줄로 구분되지 않은 JSON 파일의 읽기를 허용할지 정의|

줄로 구분된 JSON 파일을 읽는 방법은 데이터 파일 포맷 설정과 옵션을 지정하는 방식만 다릅니다.

```scala
spark.read.format("json")
```

### Reading JSON Files

JSON 파일을 읽는 방법과 표에서 적은 옵션을 비교해보겠습니다.

```scala
// in Scala
spark.read.format("json").option("mode", "FAILFAST").schema(myManualSchema)
  .load("/data/flight-data/json/2010-summary.json").show(5)
```

### Writing JSON Files

데이터 소스에 관계없이 JSON 파일에 저장할 수 있습니다. 그래서 이전에 만들었던 CSV DataFrame 을 JSON 파일의 소스로 재사용할 수 있습니다.

파티션당 하나의 파일을 만들며 전체 DataFrame 을 단일 폴더에 저장합니다.

```scala
// in Scala
csvFile.write.format("json").mode("overwrite").save("/tmp/my-json-file.json")
```

```shell
$ ls /tmp/my-json-file.json/

/tmp/my-json-file.json/part-00000-tid-543....json
```

## Parquet Files

Parquet 는 다양한 스토리지 최적화 기술을 제공하는 오픈소스로 만들어진 칼럼 기반의 데이터 저장 방식입니다. 특히, 분석 워크로드에 최적화되어 있습니다. 저장소 공간을 절약할 수 있고 전체 파일을 읽는 대신 개별 칼럼을 읽을 수 있으며, 칼럼 기반의 압축 기능을 제공합니다.

특히 Spark 와 호환이 잘되어 기본 파일 포맷입니다. Parquet 파일은 읽기 연산시 CSV, JSON 보다 효율적으로 동작하여 장기 저장용 데이터에 적합합니다.

Parquet 은 복합데이터 타입을 지원합니다. 칼럼이 배열, 맵, 구조체 데이터 타입이라 해도 문제없이 읽고 쓸 수 있습니다. 하지만 CSV 배열은 사용할 수 없습니다.

Parquet 은 다음과 같이 사용합니다.

```scala
spark.read.format("parquet")
```

### Reading Parquet Files

Parquet 는 옵션이 거의 없습니다. 데이터를 저장할 때 자체 스키마를 사용해 데이터를 저장하기 때문입니다. 따라서 포맷을 설정하는 것만으로도 충분합니다. DataFrame 을 표현하기 위해 정확한 스키마가 필요한 경우에만 스키마를 설정합니다. 하지만 이런 작업은 거의 필요 없습니다. 그 이유는 CSV 파일에 `inferSchema` 를 사용하는 것과 유사하게 읽는 시점에 스키마를 알 수 있기 때문입니다.

Parquet 파일은 스키마가 파일 자체에 내장되어 있으므로 추정이 필요 없습니다. 그러므로 이 방법이 더 효과적입니다.

다음은 Parquet 파일을 읽는 간단한 예제입니다.

```scala
// in Scala
spark.read.format("parquet")
  .load("/data/flight-data/parquet/2010-summary.parquet").show(5)
```

#### PARQUET OPTIONS

Parquet 에는 정확히 2 개의 옵션이 있습니다. 2 개의 옵션은 Spark 개념에 아주 잘 부합하고 알맞게 정의된 명세를 가지고 있습니다.

|Read/Write|Key|Potential Values|Default|Description|
|:--|:--|:--|:--|:--|
|Write|`compression` or `codec`|None, `uncompressed`, `bzip2`, `deflate`, `gzip`, `lz4`, or `snappy`|none|Spark 가 파일을 읽고 쓸 때 사용하는 압축 코덱을 정의합니다.|
|Read|`mergeSchema`|true, false|*spark.sql.parquet.mergeSchema* 속성의 설정값|동일한 테이블이나 폴더에 신규 추가된 파케이 파일에 칼럼을 점진적으로 추가할 수 있습니다. 이러한 기능을 활성화하거나 비활성화하기 위해 이 옵션을 사용합니다.|

### Writing Parquet Files

Parquet 파일 쓰기는 읽기 만큼 간단합니다. 파일의 경로만 명시하면 됩니다. 분할 규칙은 다른 포맷과 동일하게 적용됩니다.

```scala
// in Scala
csvFile.write.format("parquet").mode("overwrite")
  .save("/tmp/my-parquet-file.parquet")
```

## ORC Files

ORC 는 하둡 워크로드를 위해 설계된 **자기 기술적(Self-Describing)** 이며 데이터 타입을 인식할 수 있는 칼럼 기반의 파일 포맷입니다. 이 포맷은 대규모 스트리밍 읽기에 최적화되어 있을 뿐만 아니라 필요한 로우를 신속하게 찾아낼 수 있는 기능이 통합되어 있습니다.

Spark 는 ORC 파일 포맷을 효율적으로 사용할 수 있으므로 별도의 옵션 지정 없이 데이터를 읽을 수 있습니다. 두 포맷은 매우 유사하나 Parquet 은 Spark 에 최적화된 반면 ORC 는 Hive 에 최적화되어 있습니다.

### Reading Orc Files

Spark 에 ORC 파일을 읽는 방법은 다음과 같습니다.

```scala
// in Scala
spark.read.format("orc").load("/data/flight-data/orc/2010-summary.orc").show(5)
```

### Writing Orc Files

ORC 파일도 동일한 사용 패턴을 사용하여 파일을 저장합니다.

```scala
// in Scala
csvFile.write.format("orc").mode("overwrite").save("/tmp/my-json-file.orc")
```

## SQL Databases

SQL 데이터소스는 강력한 커넥터 중 하나입니다. 사용자는 SQL 을 지원하는 다양한 시스템에 SQL 데이터소스를 연결할 수 있습니다. 예를 들어, PostgreSQL, Oracle DB 에 접속할 수 있습니다.

예제에서 사용할 SQLite 에도 접속할 수 있습니다. 데이터베이스는 원시 파일 형태가 아니므로 고려해야 할 옵션이 많습니다. 예를 들어, 데이터베이스의 인증 정보나 접속과 관련된 옵션이 필요합니다. 그리고 Spark 클러스터에서 데이터 베이스 시스템에 접속 가능한지 네트워크 상태를 확인해야 합니다.

데이터베이스를 설정하는 번거로움을 없애고 이 책의 목적에 충실하기 위해 SQLite 실행을 위한 참고용 샘플을 사용하겠습니다. 데이터베이스에 데이터를 읽고 쓰기 위해서는 Spark Classpath 에 데이터베이스의 **JDBC(Java Database Connectivity)** 드라이버를 추가하고 적절한 JDBC 드라이버 jar 파일을 제공해야 합니다. 예를 들어 PostgreSQL 데이터베이스에 데이터를 읽거나 쓰려면 다음과 같이 샐행합니다.

```shell
./bin/spark-shell \
--driver-class-path postgresql-9.4.1207.jar \
--jars postgresql-9.4.1207.jar
```

다른 데이터소스와 마찬가지로 SQL 데이터베이스에서 데이터를 읽고 쓸 때 사용할 수 있는 몇가지 옵션이 있습니다.  아래 표는 JDBC 데이터베이스를 사용할 때 설정할 수 있는 모든 옵션 정보를 제공합니다.

|Property Name|Meaning|
|:--|:--|
|`url`|접속을 위한 JDBC URL|
|`dbtable`|읽을 JDBC 테이블을 설정한다. SQL 쿼리의 FROM 절에 유효한 모든 것을 사용할 수 있습니다. 전체 테이블 대신 괄호 안에 서브쿼리를 사용할 수 있습니다.|
|`driver`|지정한 URL 에 접속할 때 사용할 JDBC 드라이버 클래스 명을 지정합니다.|
|`partitionColumn`, `lowerBound`, `upperBound`|항상 같이 지정해야하며 `numPartitions` 도 반드시 지정해야 합니다. 다수의 워커에서 병렬로 테이블을 나눠 읽는 방법을 정의합니다. `partitionColumn` 은 반드시 해당 테이블의 수치형 칼럼이어야 합니다. `lowerBound` 와 `upperBound` 는 테이블의 로우를 필터링 하는 데 사용되는 것이 아니라 각 파티션의 범위를 결정하는데 사용됩니다. 따라서 테이블의 모든 로우는 분할되어 반환됩니다.|
|`numPartitions`|테이블의 데이터를 병렬로 읽거나 쓰기 작업에 사용할 수 있는 최대 파티션 수를 결정합니다. 이 속성은 최대 동시 JDBC 연결 수를 결정합니다. 쓰기에 사용되는 파티션 수가 이 값을 초과하는 경우 쓰기 연산 전에 `coalesce(numPartitions)` 를 실행해 파티션 수를 이 값에 맞게 줄이게 됩니다.|
|`fetchSize`|한 번에 얼마나 많은 로우를 가져올 지 결정하는 JDBC 의 패치 크기를 결정합니다. 이 옵션은 기본적으로 패치 크기가 작게 설정된 JDBC 드라이버의 성능을 올리는 데 도움이 됩니다.|
|`batchSize`|한 번에 얼마나 많은 로우를 저장할지 결정하는 JDBC 의 배치 크기를 설정합니다. 이 옵션은 JDBC 드라이버의 성능을 향상시킬 수 있습니다. 쓰기에만 적용되며 기본값은 1000 입니다.|
|`isolationLevel`|현재 연결에 적용되는 트랜잭션 격리 수준을 정의합니다. JDBC Connection 객체에서 정의하는 표준 트랜잭션 격리 수준에 해당하는 `NONE`, `READ_COMMITTED`, `READ_UNCOMMITTED`, `REPETABLE_READ`, `SERIALIZABLE` 중 하나가 될 수 있습니다. 기본 값은 `READ_UNCOMMITTED` 입니다.|
|`trucate`|JDBC writer 관련 옵션입니다. `SaveMode.Overwrite` 가 활성화되면 Spark 는 기존 테이블을 삭제하거나 재생성하는 대신 데이터베이스의 truncate 명령을 실행합니다. 이 동작 방식이 더 효율적일 수 있으며, 인덱스 같은 테이블 메타데이터가 제거되는 현상을 방지할 수 있습니다. 하지만 신규 데이터가 현재 스키마와 다른 경우와 같이 일부 경우에는 정상적으로 동작하지 않을 수도 있습니다. 기본 값은 false 이며 쓰기에만 적용됩니다.|
|`createTableOptions`|JDBC write 관련 옵션입니다. 테이블 생성 시 특정 테이블의 데이터베이스와 파티션 옵션을 설정할 수 있습니다. (ex : `CREATE TABLE t (name string) ENGINE=InnodB`) 이 옵션은 쓰기에만 적용됩니다.|
|`createTableColumnTypes`|테이블을 생성할 때 기본값 대신 사용할 데이터베이스 칼럼 데이터 타입을 정의합니다. 데이터 타입 정보는 반드시 `CREATE TABLE` 에서 사용하는 칼럼 정의 구문과 동일한 형식으로 지정해야 합니다. (ex: `name CHAR(64), comments VARCHAR(1024)`. 지정된 데이터 타입은 유효한 Spark SQL 데이터 타입이어야 하며, 쓰기에만 적용됩니다.|

### Reading from SQL Databases

파일 읽기와 마찬가지로 SQL 데이터베이스에서 데이터를 읽는 방법은 다른 데이터소스와 다르지 않습니다. 다른 데이터 소스처럼 포맷과 옵션을 지정한 후 데이터를 읽어 들입니다.

```scala
// in Scala
val driver =  "org.sqlite.JDBC"
val path = "/data/flight-data/jdbc/my-sqlite.db"
val url = s"jdbc:sqlite:/${path}"
val tablename = "flight_info"
```

접속 관련 속성을 정의한 다음, 정상적으로 데이터베이스에 접속되는지 테스트해 해당 연결이 유효한지 확인할 수 있습니다. 이것은 Spark 드라이버가 데이터베이스에 접속할 수 있는지 확인할 수 있는 훌룡한 문제 해결 기술입니다. SQLite 는 로컬 머신에 존재하는 파일 형태이므로 접속 테스트가 무의미할 수 있습니다.

하지만 MySQL 같은 데이터베이스를 사용하는 경우 다음과 같은 코드를 사용해 접속 테스트를 해볼 수 있습니다.

```scala
import java.sql.DriverManager
\
val connection = DriverManager.getConnection(url)
connection.isClosed()
connection.close()
```

접속에 성공하면 다음 예제를 진행할 수 있습니다. SQL 테이블을 읽어 DataFrame 을 만들어보겠습니다.

```scala
// in Scala
val dbDataFrame = spark.read.format("jdbc").option("url", url)
  .option("dbtable", tablename).option("driver",  driver).load()
```

SQLite 는 설정이 간단합니다. 사용자 인증 정보가 필요 없습니다. PostgreSQL 과 같은 데이터베이스에는 더 많은 설정이 필요합니다. 다음 예제는 PostgreSQL 을 이용해 위 예제와 동일한 데이터 읽기 작업을 수행합니다.

```scala
// in Scala
val pgDF = spark.read
  .format("jdbc")
  .option("driver", "org.postgresql.Driver")
  .option("url", "jdbc:postgresql://database_server")
  .option("dbtable", "schema.tablename")
  .option("user", "username").option("password","my-secret-password").load()
```

생성한 DataFrame 은 기존 예제에서 생성한 DataFrame 과 같습니다. 문제 없이 조회하고 변환해 조인할 수 있으며 이미 스키마가 적용되어 있습니다.

Spark 는 데이터베이스의 테이블에서 스키마 정보를 읽어 테이블에 존재하는 칼럼의 데이터 타입을 Spark 데이터 타입으로 변환하기 때문입니다. 원하는 대로 쿼리를 수행할 수 있는지 확인하기 위해 중복 데이터가 제거된 국가 목록을 조회해보겠습니다.

```scala
dbDataFrame.select("DEST_COUNTRY_NAME").distinct().show(5)
```

결과는 아래와 같습니다.

```
+-----------------+
|DEST_COUNTRY_NAME|
+-----------------+
|         Anguilla|
|           Russia|
|         Paraguay|
|          Senegal|
|           Sweden|
+-----------------+
```

### Query Pushdown

Spark 는 DataFrame 을 만들기 전에 데이터베이스 자체에서 데이터를 필터링하도록 만들 수 있습니다. 예를 들어 이전 예제에서 사용한 쿼리의 실행 계획을 들여다보면 테이블의 여러 칼럼 중 관련 있는 칼럼만 선택하는 것을 알 수 있습니다.

```scala
dbDataFrame.select("DEST_COUNTRY_NAME").distinct().explain
```

```
== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#8108], functions=[])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#8108, 200)
   +- *HashAggregate(keys=[DEST_COUNTRY_NAME#8108], functions=[])
      +- *Scan JDBCRelation(flight_info) [numPartitions=1] ...
```

Spark 는 특정 유형의 쿼리를 더 나은 방식으로 처리할 수 있습니다. 예를 들어 DataFrame 에 필터를 명시하면 Spark 는 해당 필터에 대한 처리를 데이터베이스로 위임합니다. 실행 계획의 PushedFilters 부분에서 관련 내용을 확인할 수 있습니다.

```scala
// in Scala
dbDataFrame.filter("DEST_COUNTRY_NAME in ('Anguilla', 'Sweden')").explain
```

```
== Physical Plan ==
*Scan JDBCRel... PushedFilters: [*In(DEST_COUNTRY_NAME, [Anguilla,Sweden])],
...
```

Spark 는 모든 Spark 함수를 사용하는 SQL 데이터베이스에 맞게 변환하지는 못합니다. 따라서 전체 쿼리를 데이터베이스에 전달해 결과를 DataFrame 으로 받아야 하는 경우도 있습니다. 

복잡해보이는 처리 방식이지만 간단합니다. 테이블 명 대신 SQL 쿼리를 명시하면 됩니다. 물론 이렇게 하려면 괄호로 쿼리를 묶고 이름으 ㄹ변경하는 특수한 방식을 사용해야 합니다. 다음 예제에서는 테이블 명을 별칭으로 사용했습니다.

```scala
// in Scala
val pushdownQuery = """(SELECT DISTINCT(DEST_COUNTRY_NAME) FROM flight_info)
  AS flight_info"""
val dbDataFrame = spark.read.format("jdbc")
  .option("url", url).option("dbtable", pushdownQuery).option("driver",  driver)
  .load()
```

이 테이블에 쿼리할 때 실제로는 pushdownQuery 변수에 명시한 쿼리를 사용해 수행합니다. 이 사실은 실행 계획에서 확인할 수 있습니다. Spark 는 테이블의 실제 스키마와 관련된 정보를 알지 못하며 단지 쿼리의 결과에 대한 스키마만 알 수 있습니다.

```scala
dbDataFrame.explain()
```

```
== Physical Plan ==
*Scan JDBCRelation(
(SELECT DISTINCT(DEST_COUNTRY_NAME)
  FROM flight_info) as flight_info
) [numPartitions=1] [DEST_COUNTRY_NAME#788] ReadSchema: ...
```

#### READING FROM DATABASES IN PARALLEL

Spark 는 파일 크기, 유형, 압축 방식에 따른 분할 가능성에 따라 여러 파일을 읽어 하나의 파티션으로 만들거나 여러 파티션을 하나의 파일로 만드는 기본 알고리즘을 가지고 있습니다.

파일이 가진 이런 유연성은 SQL 데이터베이스에도 존재하지만 몇 가지 수동 설정이 필요합니다. 이전 옵션 목록 중 `numPartitions` 옵션을 사용해 읽기 및 쓰기용 동시 작업 수를 제한할 수 있는 최대 파티션 수를 설정할 수 있습니다.

```scala
// in Scala
val dbDataFrame = spark.read.format("jdbc")
  .option("url", url).option("dbtable", tablename).option("driver", driver)
  .option("numPartitions", 10).load()
```

데이터가 많지 않기 때문에 한 개의 파티션만 존재합니다. 이 설정을 활용해 데이터베이스에 일어날 수 있는 과도한 쓰기나 읽기를 막을 수 있습니다.

```scala
dbDataFrame.select("DEST_COUNTRY_NAME").distinct().show()
```

API 셋에서만 사용할 수 있는 몇 가지 최적화 방법이 있습니다. 데이터베이스 연결을 통해 명시적으로 조건절을 SQL 데이터베이스에 위임할 수 있습니다. 이 최적화 방법은 조건절을 명시하여 특정 파티션에 특정 데이터의 물리적 위치를 제어할 수 있습니다.

전체 데이터 중 Anguilla, Sweden 두 국가의 데이터만 필요할 때, 두 국가에 대한 필터를 데이터베이스에 위임해 처리된 결과를 반환할 수 있지만, Spark 자체 파티션에 결과 데이터를 저장하여 더 많은 처리를 할 수 있습니다. 데이터소스 생성 시 조건절 목록을 정의해 Spark 자체 파티션에 결과 데이터를 저장할 수 있습니다.

```scala
// in Scala
val props = new java.util.Properties
props.setProperty("driver", "org.sqlite.JDBC")
val predicates = Array(
  "DEST_COUNTRY_NAME = 'Sweden' OR ORIGIN_COUNTRY_NAME = 'Sweden'",
  "DEST_COUNTRY_NAME = 'Anguilla' OR ORIGIN_COUNTRY_NAME = 'Anguilla'")
spark.read.jdbc(url, tablename, predicates, props).show()
spark.read.jdbc(url, tablename, predicates, props).rdd.getNumPartitions // 2
```

실행 결과는 다음과 같습니다.

```
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|           Sweden|      United States|   65|
|    United States|             Sweden|   73|
|         Anguilla|      United States|   21|
|    United States|           Anguilla|   20|
+-----------------+-------------------+-----+
```

연관성 없는 조건절을 정의하면 중복 로우가 많이 발생할 수 있습니다. 다음은 중복 로우를 발생시키는 조건절 예제입니다.

```scala
// in Scala
val props = new java.util.Properties
props.setProperty("driver", "org.sqlite.JDBC")
val predicates = Array(
  "DEST_COUNTRY_NAME != 'Sweden' OR ORIGIN_COUNTRY_NAME != 'Sweden'",
  "DEST_COUNTRY_NAME != 'Anguilla' OR ORIGIN_COUNTRY_NAME != 'Anguilla'")
spark.read.jdbc(url, tablename, predicates, props).count() // 510
```

#### PARTITIONING BASED ON A SLIDING WINDOW

조건절을 기반으로 분할해보겠습니다. 예제에서는 수치형 `count` 칼럼을 기준으로 분할합니다. 여기서는 처음과 마지막 파티션 사이의 최솟값과 최댓값을 사용합니다. 이 범위 밖의 모든 값은 첫 번재 또는 마지막 파티션에 속합니다. 그 다음 전체 파티션 수를 설정합니다. 이 값은 병렬 처리 수준을 의미합니다.

Spark 는 데이터베이스에 병렬로 쿼리를 요청하며 `numPartitions` 에 설정된 값만큼 파티션을 반환합니다. 그리고 파티션에 값을 할당하기 위해 상한값과 하한값을 수정합니다.

```scala
// in Scala
val colName = "count"
val lowerBound = 0L
val upperBound = 348113L // this is the max count in our database
val numPartitions = 10
```

최젓값에서 최곳값까지 동일하게 분배합니다.

```scala
// in Scala
spark.read.jdbc(url,tablename,colName,lowerBound,upperBound,numPartitions,props)
  .count() // 255
```

### Writing to SQL Databases

SQL 데이터베이스에 데이터를 쓰는 것은 읽기만큼이나 쉽습니다. URI 를 지정하고 지정한 쓰기 모드에 따라 데이터를 쓰면 됩니다. 다음 예제는 전체 테이블을 덮어쓰는 `overwrite` 쓰기 모드를 사용합니다. 처리를 위해 이전에 정의한 CSV DataFrame 을 사용합니다.

```scala
// in Scala
val newPath = "jdbc:sqlite://tmp/my-sqlite.db"
csvFile.write.mode("overwrite").jdbc(newPath, tablename, props)
```

실행 결과는 다음과 같습니다.

```scala
// in Scala
spark.read.jdbc(newPath, tablename, props).count() // 255
```

새로운 테이블에 쉽게 데이터를 추가할 수 있습니다.

```scala
// in Scala
csvFile.write.mode("append").jdbc(newPath, tablename, props)
```

레코드 수가 증가하는 것을 확인하겠습니다.

```scala
// in Scala
spark.read.jdbc(newPath, tablename, props).count() // 765
```

## Text Files

Spark 는 일반 텍스트 파일도 읽을 수 있습니다. 파일의 각 줄은 DataFrame 의 레코드가 됩니다.

### Reading Text Files

`textFile` 메소드에 텍스트 파일을 지정하기만 하면됩니다. `textFile` 메소드는 파티션 수행 결과로 만들어진 디렉토리명을 무시합니다. 파티션된 텍스트 파일을 읽거나 쓰려면 읽기 및 쓰기 시 파티션 수행 결과로 만들어진 디렉토리를 인식할 수 있도록 `text` 메소드를 사용해야 합니다.

```scala
spark.read.textFile("/data/flight-data/csv/2010-summary.csv")
  .selectExpr("split(value, ',') as rows").show()
```

실행 결과는 다음과 같습니다.

```
+--------------------+
|                rows|
+--------------------+
|[DEST_COUNTRY_NAM...|
|[United States, R...|
...
|[United States, A...|
|[Saint Vincent an...|
|[Italy, United St...|
+--------------------+
```

### Writing Text Files

텍스트 파일을 쓸 때는 문자열 칼럼 하나만 존재합니다.

```scala
csvFile.select("DEST_COUNTRY_NAME").write.text("/tmp/simple-text-file.txt")
```

텍스트 파일에 데이터를 저장할 때 파티셔닝 작업을 수행하면 더 많은 칼럼을 저장할 수 있습니다. 하지만 모든 파일에 칼럼을 추가하는 것이 아니라 텍스트 파일이 저장되는 디렉토리에 폴더별로 칼럼을 저장합니다.

```scala
// in Scala
csvFile.limit(10).select("DEST_COUNTRY_NAME", "count")
  .write.partitionBy("count").text("/tmp/five-csv-files2.csv")
```

## Advanced I/O Concepts

쓰기 작업 전에 파티션 수를 조절하여 병렬로 처리할 파일 수를 제어할 수 있습니다. 또한 **버케팅** 과 **파티셔닝** 을 조절하여 데이터의 저장 구조를 제어할 수 있습니다.

### Splittable File Types and Compression

특정 파일 포맷은 기본적으롭 분할을 지원합니다. 따라서 Spark 에서 전체 파일이 아닌 쿼리에 필요한 부분만 읽을 수 있으므로 성능 향상에 도움이 됩니다. 게다가 HDFS 같은 시스템을 사용한다면 분할된 파일을 여러 블록으로 나누어 분산 저장하기 때문에 훨씬 더 최적화할 수 있습니다. 

이와 함게 압축 방식도 관리해야 합니다. 모든 압축 방식이 분할 압축을 지원하지는 않습니다. 데이터를 저장하는 방식에 따라 Spark 잡이 원할하게 동작하는 데 막대한 영향을 끼칠 수 있습니다. 추천하는 파일 포맷과 압축 방식은 Parquet, GZIP 압축 방식입니다.

### Reading Data in Parallel

여러 익스큐터가 같은 파일을 동시에 읽을 수는 없지만 여러 파일을 동시에 읽을 수 있습니다.

다수의 파일이 존재하는 폴더를 읽을 때 폴더의 개별 파일은 DataFrame 의 파티션이 됩니다. 따라서 사용 가능한 익스큐터를 이용해 병렬로 파일을 읽습니다.

### Writing Data in Parallel

파일이나 데이터 수는 데이터를 쓰는 시점에 DataFrame 이 가진 파티션 수에 따라 달라질 수 있습니다. 기본적으로 데이터 파티션당 하나의 파일이 작성됩니다. 옵션에 지정된 파일 명은 실제로 다수의 파일을 가진 디렉토리입니다. 그리고 디렉토리 안에 파티션당 하나의 파일로 데이터를 저장합니다.

예를 들어 다음 코드는 폴더 안에 5 개의 파일을 생성합니다.

```scala
csvFile.repartition(5).write.format("csv").save("/tmp/multiple.csv")
```

`ls` 명령의 결과는 다음과 같습니다.

```shell
$ ls /tmp/multiple.csv

/tmp/multiple.csv/part-00000-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00001-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00002-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00003-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00004-767df509-ec97-4740-8e15-4e173d365a8b.csv
```

#### PARTITIONING

파티셔닝은 데이터를 어디에 저장할 것인지 제어할 수 있는 기능입니다. 파티셔닝된 디렉토리 또는 테이블에 파일을 쓸 때 디렉토리별로 칼럼 데이터를 인코딩해 저장합니다. 그러므로 데이터를 읽을 때 전체 데이터셋을 스캔하지 않고 필요한 칼럼의 데이터만 읽을 수 있습니다.

이 방식은 모든 파일 기반의 데이터소스에서 지원합니다.

```scala
// in Scala
csvFile.limit(10).write.mode("overwrite").partitionBy("DEST_COUNTRY_NAME")
  .save("/tmp/partitioned-files.parquet")
```

결과를 확인해보겠습니다.

```shell
$ ls /tmp/partitioned-files.parquet

...
DEST_COUNTRY_NAME=Costa Rica/
DEST_COUNTRY_NAME=Egypt/
DEST_COUNTRY_NAME=Equatorial Guinea/
DEST_COUNTRY_NAME=Senegal/
DEST_COUNTRY_NAME=United States/
```

각 폴더는 조건절을 폴더명으로 사용하여 조건절을 만족하는 데이터가 저장된 Parquet 파일을 가지고 있습니다.

```shell
$ ls /tmp/partitioned-files.parquet/DEST_COUNTRY_NAME=Senegal/

part-00000-tid.....parquet
```

파티셔닝은 필터링을 자주 사용하는 테이블을 가진 경우에 사용할 수 있는 가장 손쉬운 최적화 방식입니다. 예를 들어 전체 데이터를 스캔하지 않고 지난주 데이터만 보려면 날짜를 기준으로 파티션을 만들 수 있습니다. 이 기법을 사용하면 빠른 속도로 데이터를 읽어 들일 수 있습니다.

#### BUCKETING

**버케팅(Bucketing)** 은 각 파일에 저장된 데이터를 제어할 수 있는 또 다른 조직화 기법입니다. 이 기법을 사용하면 동일한 버킷 ID 를 가진 데이터가 하나의 물리적 파티션에 모두 모여 있기 때문에 데이터를 읽을 때 셔플을 피할 수 있습니다.

즉, 데이터가 이후의 사용 방식에 맞춰 사전에 파티셔닝되므로 조인이나 집계 시 발생하는 고비용의 셔플을 피할 수 있습니다.

특정 칼럼의 파티셔닝하면 수억 개의 디렉토리를 만들어 낼 수 있습니다. 이 경우 데이터를 버케팅할 수 있는 방법을 찾아야 합니다. 다음은 버켓 단위로 데이터를 모아 일정 수의 파일로 저장하는 예제입니다.

```scala
val numberBuckets = 10
val columnToBucketBy = "count"

csvFile.write.format("parquet").mode("overwrite")
  .bucketBy(numberBuckets, columnToBucketBy).saveAsTable("bucketedFiles")
```

```shell
$ ls /user/hive/warehouse/bucketedfiles/

part-00000-tid-1020575097626332666-8....parquet
part-00000-tid-1020575097626332666-8....parquet
part-00000-tid-1020575097626332666-8....parquet
...
```

버케팅은 Spark 관리 테이블에서만 사용할 수 있습니다.

### Writing Complex Types

Spark 는 다양한 자체 데이터 타입을 제공합니다. 이 데이터 타입은 Spark 에서 잘 동작하지만 모든 데이터 파일 포맷에 적합한 것은 아닙니다.

### Managing File Size

파일 크기를 관리하는 것은 데이터를 저장할 떄는 중요한 요소가 아닙니다. 하지만, 데이터를 읽을 때는 중요한 요소 중 하나입니다. 작은 파일을 많이 생성하면 메타데이터에 엄청난 관리 부하가 발생합니다. HDFS 같은 파일 시스템은 작은 파일을 잘 다루지 못합니다. Spark 에서는 특히 그렇습니다.

이런 상황을 작은 크기의 파일 문제라고도 합니다. 반대의 경우도 문제가 됩니다. 몇 개의 로우가 필요하더라도 전체 데이터 블록을 읽어야 하기 때문에 비효율적입니다.

Spark 2.2 에선 자동으로 파일 크기를 제어할 수 있는 새로운 방법이 도입되었습니다. 이전 예제에서 결과 파일 수는 파일을 쓰는 시점에서의 파티션 수에서 파생되었음을 알 수 있습니다. 이 결과 파일을 최적의 크기로 제한할 수 있는 새로운 기능을 활용해보겠습니다. 이 기능을 사용하려면 `maxRecordsPerFile` 옵션에 파일당 레코드 수를 지정해야 합니다. 

각 파일에 기록된 레코드를 조절할 수 있으므로 파일 크기를 효과적으로 제어할 수 있습니다. 만약 파일 쓰기 객체에 다음과 같은 옵션을 설정했다면 Spark 는 파일당 최대 5,000 개의 로우를 포함하도록 보장할 수 있습니다.

```scala
df.write.option("maxRecordsPerFile", 5000)
```