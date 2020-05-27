---
title : Spark Advanced RDDs
tags :
- Partition
- Serialization
- Join
- Aggregation
- CoGroup
- RDD
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

[Spark RDD](/spark-resilientdistributeddatasets) 에서 사용한 데이터셋으로 이용하겠습니다.

```scala
// in Scala
val myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"
  .split(" ")
val words = spark.sparkContext.parallelize(myCollection, 2)
```

## Key-Value Basics (Key-Value RDDs)

RDD 에는 데이터를 Key - Value 형태로 다룰 수 있는 다양한 메소드가 있습니다. 이러한 메소드는 `<some-operation>ByKey` 형태의 이름을 가집니다. 메소드 이름에 `ByKey` 가 있다면 `PairRDD` 타입만 사용할 수 있습니다. 

`PairRDD` 타입을 만드는 가장 쉬운 방법은 RDD 에 맵 연산을 수행하여 Key - Value 구조로 만드는 겁니다. 즉, RDD 레코드에 두 개의 값이 존재합니다.

```scala
// in Scala
words.map(word => (word.toLowerCase, 1))
```

### keyBy

현재 값으로부터 Key 를 생성하는 `KeyBy` 함수를 사용해 동일한 결과를 얻을 수 있습니다. 다음은 단어의 첫 번째 문자를 키로 만들어 RDD 를 생성합니다. 이때 Spark 는 원본 단어를 생성된 RDD 값으로 유지합니다.

```scala
// in Scala
val keyword = words.keyBy(word => word.toLowerCase.toSeq(0).toString)
```

### Mapping over Values

생성된 Key - Value 셋을 사용해 데이터를 다뤄보겠습니다.

만약 튜플 형태의 데이터를 사용한다면 Spark 는 튜플의 첫 번째 요소를 Key, 두 번째 요소를 Value 로 추정합니다. 튜플 형태의 데이터에서 Key 를 제외하고 Value 만 추출할 수 있습니다.

아래와 같이 `mapValues` 메소드를 사용하면 값 수정 시 발생할 수 있는 오류를 미리 ㅂ아지할 수 있습니다.

```scala
// in Scala
keyword.mapValues(word => word.toUpperCase).collect()
```

결과는 아래와 같습니다.

```scala
[('s', 'SPARK'),
 ('t', 'THE'),
 ('d', 'DEFINITIVE'),
 ('g', 'GUIDE'),
 (':', ':'),
 ('b', 'BIG'),
 ('d', 'DATA'),
 ('p', 'PROCESSING'),
 ('m', 'MADE'),
 ('s', 'SIMPLE')]
```

`flatMap` 함수를 사용해 반환되는 결과의 각 로우가 문자를 나타내도록 확장할 수 있습니다. 아래는 출력 결과가 생략되어 있지만, 단어의 첫 글자를 Key, 단어의 각 문자를 Value 로 하는 배열이 생헝됩니다.

```scala
// in Scala
keyword.flatMapValues(word => word.toUpperCase).collect()
```

### Extracting Keys and Values

Key - Value 형태의 데이터를 가지고 있다면 다음 메소드를 사용해 Key 나 Value 전체를 추출할 수 있습니다.

```scala
// in Scala
keyword.keys.collect()
keyword.values.collect()
```

### lookup

RDD 를 사용해서 할 수 있는 흥미로운 작업 중 하나는 특정 Key 에 관한 결과를 찾는 겁니다. 그러나 각 입력에 대해 오직 하나의 Key 만 찾을 수 있도록 강제하는 메커니즘은 없습니다. 예를 들어 `lookup` 함수의 인수로 `s` 를 입력하면 Key 가 `s` 인 `Spark`, `Simple` 을 반환합니다.

```scala
keyword.lookup("s")
```

### sampleByKey

근사치나 정확도를 이용해 Key 를 기반으로 RDD 샘플을 생성할 수 있습니다. 두 작업 모두 특정 Key 를 부분 샘플링할 수 있으며 선택에 따라 비복원 추출을 사용할 수 있습니다.

아래 예제의 `sampleByKey` 메소드는 RDD 를 한 번만 처리하면서 간단한 무작위 샘플링을 사용하기 때문에 모든 Key 값에 대한 `math.ceil(numItems * samplingRate)` 값의 총합과 거의 동일한 크기의 샘플을 생성합니다.

```scala
// in Scala
val distinctChars = words.flatMap(word => word.toLowerCase.toSeq).distinct
  .collect()
import scala.util.Random
val sampleMap = distinctChars.map(c => (c, new Random().nextDouble())).toMap
words.map(word => (word.toLowerCase.toSeq(0), word))
  .sampleByKey(true, sampleMap, 6L)
  .collect()
```

아래 예제의 `sampleByKeyExact` 메소드는 99.99 % 신뢰도를 가진 모든 KeyValue 에 대해 RDD 를 추가로 처리합니다. 그리고 `math.ceil(numItems * samplingRate)` 의 합과 완전히 동일한 크기의 샘플 데이터를 생성하므로 `sampleByKey` 함수와는 다릅니다.

비복원 추출을 사용한다면 샘플 크기를 보장하기 위해 RDD 를 한 번 더 통과해야 하며, 복원 추출을 사용한다면 RDD 를 두 번 더 통과해야 합니다.

```scala
// in Scala
words.map(word => (word.toLowerCase.toSeq(0), word))
  .sampleByKeyExact(true, sampleMap, 6L).collect()
```

## Aggregations

사용하는 메소드에 따라 일반 RDD 나 PairRDD 를 사용해 집계를 수행할 수 있습니다. `words` 데이터셋을 이용해 알아보겠습니다.

```scala
// in Scala
val chars = words.flatMap(word => word.toLowerCase.toSeq)
val KVcharacters = chars.map(letter => (letter, 1))
def maxFunc(left:Int, right:Int) = math.max(left, right)
def addFunc(left:Int, right:Int) = left + right
val nums = sc.parallelize(1 to 30, 5)
```

위 코드 예제를 수행한 다음 Key 별 아이템 수를 구하기 위해 `countByKey` 메소드를 사용합니다.

### countByKey

`countByKey` 메소드는 각 Key 의 아이템 수를 구하고 로컬 맵으로 결과를 수집합니다. Scala 나 Java 를 사용한다면 `countByKey` 메소드에 제한 시간과 신뢰도를 인수로 지정해 근사치를 구할 수 있습니다.

```scala
// in Scala
val timeout = 1000L //milliseconds
val confidence = 0.95
KVcharacters.countByKey()
KVcharacters.countByKeyApprox(timeout, confidence)
```

### Understanding Aggregation Implementations

Key - Value 형태의 PairRDD 를 생성하는 몇 가지 방법이 있습니다. 이때 구현 방식은 잡의 안정성을 위해 매우 중요합니다.

이를 설명하기 위해 `groupBy` 와 `reduce` 함수를 비교해보겠습니다. 두 함수 모두 동일한 기본 원칙이 적용되므로 Key 를 기준으로 비교합니다.

#### groupByKey

각 Key 의 총 레코드 수를 구하는 경우 `groupByKey` 의 결과로 만들어진 그룹에 `map` 연산을 수행하는 방식이 좋습니다.

```scala
// in Scala
KVcharacters.groupByKey().map(row => (row._1, row._2.reduce(addFunc))).collect()
```

여기서 가장 큰 문제는 모든 익스큐터에서 함수를 적용하기 전에 해당 Key 와 관련된 모든 값을 메모리로 읽어들여야 하는겁니다.

이 이유로 심각하게 치우쳐진 Key 가 있다면 일부 파티션이 엄청난 양의 값을 가질 수 있으므로 OutOfMemoryError 가 발생합니다. 대규모 분산 환경에서는 심각한 문제로 이어질 수 있습니다.

그러므로 각 Key 에 대한 값의 크기가 일정하고 익스큐터에 할당된 메모리에서 처리 가능할 정도의 크기라면 `groupByKey` 메소드를 사용합니다. 또한 `groupByKey` 메소드를 사용할 때 어떤 일이 발생하는지 정확하게 알아야합니다.

#### reduceByKey

지금은 단순하게 개수를 구하므로 `flatMap` 을 동일하게 수행한 다음 `map` 연산을 통해 각 문자의 인스턴스를 1 로 매핑합니다. 그 다음 결괏값을 배열에 모을 수 있도록 합계 함수와 함께 `reduceByKey` 메소드를 수행합니다.

이러한 구현 방식은 각 파티션에서 리듀스 작업을 수행하기 때문에 훨씬 안정적이며 모든 값을 메모리에 유지하지 않아도 됩니다. 또한 최종 리듀스 과정을 제외한 모든 작업은 개별 워커에서 처리하기 때문에 연산 중에 셔플이 발생하지 않습니다.

그러므로 이러한 방식을 사용하면 안정성뿐만 아니라 연산 수행 속도가 크게 향상됩니다.

```scala
KVcharacters.reduceByKey(addFunc).collect()
```

연산 결과는 다음과 같습니다.

```scala
Array((d,4), (p,3), (t,3), (b,1), (h,1), (n,2),
...
(a,4), (i,7), (k,1), (u,1), (o,1), (g,3), (m,2), (c,1))
```

`reduceByKey` 메소드는 Key 별 그룹 RDD 를 반환합니다. 그러나 RDD 의 개별 요소는 정렬되어 있지 않습니다. 따라서 이 메소드는 작업 부하를 줄이려는 경우에 적합합니다. 반면 결과의 순서가 중요한 경우에는 적합하지 않습니다.

### Other Aggregation Methods

다양한 고급 집계 함수가 존재하며 사용자 워크로드에 따라 세부 구현 방법에서 차이가날 수 있습니다.

이 고급 집계 함수를 사용해 클러스터 노드에서 수행하는 집계를 아주 구체적이고 세밀하게 제어할 수 있습니다.

#### aggregate

이 함수는 null 값이나 집계의 시작값이 필요하며 두 가지 함수를 파라미터로 사용합니다. 첫 번째 함수는 파티션 내에서 수행되고 두 번째 함수는 모든 파티션에 걸쳐 수행합니다. 두 함수 모두 시작값을 사용합니다.

```scala
// in Scala
nums.aggregate(0)(maxFunc, addFunc)
```

`aggregate` 함수는 드라이버에서 최종 집계를 수행하기 때문에 약간의 영향이 있습니다. 예를 들어 익스큐터의 결과가 너무 크면 OutOfMemoryError 가 발생해 드라이버가 비정상적으로 종료됩니다. `aggregate` 함수와 동일한 작업을 수행하지만 다른 처리 과정을 거치는 `treeAggregate` 함수도 있습니다.

이 함수는 기본적으로 드라이버에서 최종 집계를 수행하기 전에 익스큐터끼리 트리를 형성해 집계 처리의 일부 하위 과정을 푸시다운 방식으로 먼저 수행합니다. 집계 처리를 여러 단계로 구성하는 것은 드라이버의 메모리를 모두 소비하는 현상을 막는 데 도움이 됩니다. 이러한 트리 기반의 구현 방식은 작업의 안정성을 높이기 이해 사용하기도 합니다.

```scala
// in Scala
val depth = 3
nums.treeAggregate(0)(maxFunc, addFunc, depth)
```

#### aggregateByKey

`aggregate` 함수와 동일하지만 파티션 대신 Key 를 기준으로 연산을 수행합니다.

```scala
// in Scala
KVcharacters.aggregateByKey(0)(addFunc, maxFunc).collect()
```

#### combineByKey

집계 함수 대신 **컴파이너(Combiner)** 를 사용합니다. 이 컴바이너는 Key 를 기준으로 연산을 수행하며 파라미터로 사용된 하뭇에 따라 값을 병합합니다. 그 다음 여러 컴바이너의 결괏값을 병합해 결과를 반환합니다. 사용자 정의 파티셔너를 사용해 출력 파티션 수를 지정할 수 있습니다.

```scala
// in Scala
val valToCombiner = (value:Int) => List(value)
val mergeValuesFunc = (vals:List[Int], valToAppend:Int) => valToAppend :: vals
val mergeCombinerFunc = (vals1:List[Int], vals2:List[Int]) => vals1 ::: vals2
// now we define these as function variables
val outputPartitions = 6
KVcharacters
  .combineByKey(
    valToCombiner,
    mergeValuesFunc,
    mergeCombinerFunc,
    outputPartitions)
  .collect()
```

#### foldByKey

이 함수는 결합 함수와 항등원인 제로값을 이용해 각 Key 값을 병합합니다. 제로값은 결과에 여러 번 사용될 수 있으나 결과를 변경할 수는 없습니다.

```scala
// in Scala
KVcharacters.foldByKey(0)(addFunc).collect()
```

## CoGroups

`cogrup` 함수는 Scala 를 사용하는 경우 최대 3 개, Python 을 사용하는 경우 최대 2 개의 Key - Value 형태의 RDD 를 그룹화할 수 있으며 각 Key 를 기준으로 값을 결합합니다.

즉, RDD 에 대한 그룹 기반의 조인을 수행합니다. `cogroup` 함수는 출력 파티션 수나 클러스터에 데이터 분산 방식을 정확하게 제어하기 위해 사용자 정의 파티션 함수를 파라미터로 사용할 수 있습니다.

```scala
// in Scala
import scala.util.Random
val distinctChars = words.flatMap(word => word.toLowerCase.toSeq).distinct
val charRDD = distinctChars.map(c => (c, new Random().nextDouble()))
val charRDD2 = distinctChars.map(c => (c, new Random().nextDouble()))
val charRDD3 = distinctChars.map(c => (c, new Random().nextDouble()))
charRDD.cogroup(charRDD2, charRDD3).take(5)
```

그룹화된 Key 를 `Key` 로, Key 와 관련된 모든 값을 `Value` 로 하는 Key - Value 형태의 배열을 결과로 반환합니다.

## Joins

RDD 는 구조적 API 에서 알아본 것과 거의 동일한 조인 방식을 가지고 있지만, RDD 를 사용하면 사용자가 많은 부분에 관여해야 합니다. RDD 나 구조적 API 의 조인 방식 모두 동일한 기본 형식을 사용합니다. 조인하려는 두 개의 RDD 가 기본적으로 필요합니다. 

때에 따라 출력 파티션 수나 사용자 정의 파티션 함수를 파라미터로 사용합니다.

### Inner Join

내부조인의 결과로 출력 파티션 수를 어떻게 설정하는지 살펴봐야합니다.

```scala
// in Scala
val keyedChars = distinctChars.map(c => (c, new Random().nextDouble()))
val outputPartitions = 10
KVcharacters.join(keyedChars).count()
KVcharacters.join(keyedChars, outputPartitions).count()
```

다른 조인 함수의 예제는 제공하지 않지만 모두 동일한 기본 형식을 따릅니다.

* `fullOuterJoin`
  * 외부 조인
* `leftOuterJoin`
  * 왼쪽 외부 조인
* `rightOuterJoin`
  * 오른쪽 외부 조인
* `cartesian`
  * 교차 조인

### zips

`zip` 함수를 이용해 동일한 길이의 RDD 를 **지퍼(Zipper)** 를 잠그듯이 연결할 수 있으며 PairRDD 를 생성합니다. 두 개의 RDD 는 동일한 수의 요소와 동일한 수의 파티션을 가져야 합니다.

```scala
// in Scala
val numRange = sc.parallelize(0 to 9, 2)
words.zip(numRange).collect()
```

`zip` 함수의 결과는 아래와 같습니다.

```
[('Spark', 0),
 ('The', 1),
 ('Definitive', 2),
 ('Guide', 3),
 (':', 4),
 ('Big', 5),
 ('Data', 6),
 ('Processing', 7),
 ('Made', 8),
 ('Simple', 9)]
```

## Controlling Partitions

RDD 를 사용하면 데이터가 클러스터 전체에 물리적으로 정확히 분산되는 방식을 정의할 수 있습니다.

이 기능을 가진 메소드 중 일부는 구조적 API 에서 사용했던 메소드와 기본적으로 동일합니다.

구조적 API 와 가장 큰 차이점은 파티션 함수를 파라미터로 사용할 수 있다는 사실입니다. 파티션 함수는 보통 사용자 지정 Partitioner 를 의미합니다.

### coalesce

`coalesce` 는 파티션을 재분배할 때 발생하는 데이터 셔플을 방지하기 위해 동일한 워커에 존재하는 파티션을 합치는 메소드입니다. 예를 들어 예제의 `words` RDD 는 현재 두 개의 파티션으로 구성되어 있습니다. `coalesce` 메소드를 사용해 데이터 셔플링 없이 하나의 파티션으로 합칠 수 있습니다.

```scala
// in Scala
words.coalesce(1).getNumPartitions // 1
```

### repartition

`repartition` 메소드를 사용해 파티션 수를 늘리거나 줄일 수 있지만, 처리 시 노드 간의 셔플이 발생할 수 있습니다. 파티션 수를 늘리면 맵 타입이나 필터 타입의 연산을 수행할 때 병렬 처리 수준을 높일 수 있습니다.

```scala
words.repartition(10) // gives us 10 partitions
```

### repartitionAndSortWithinPartitions

이 메소드는 파티션을 재분배할 수 있고, 재분배된 결과 파티션의 정렬 방식을 지정할 수 있습니다. 파티셔닝과 Key 비교 모두 사용자가 지정할 수 있습니다.

### Custom Partitioning

사용자 정의 파티셔닝은 RDD 를 사용하는 가장 큰 이유 중 하나입니다. 논리적인 대응책을 가지고 있찌 않으므로 구조적 API 에서는 사용자 정의 파티셔너를 파라미터로 사용할 수 없습니다. 사용자 정의 파티셔너는 저수준 API 의 세부적인 구현 방식입니다. 그리고 잡이 성공적으로 동작되는지 여부에 상당한 영향을 미칩니다.

사용자 정의 파티셔닝의 대표적인 예제는 **페이지랭크(PageRank)** 입니다. 페이지랭크는 사용자 정의 파티셔닝을 이용해 클러스터의 데이터 배치 구조를 제어하고 셔플을 회피합니다. 예제에서는 쇼핑 데이터셋을 고객 ID 별로 파티셔닝합니다.

사용자 정의 파티셔닝의 유일한 목표는 데이터 **치우침(Skew)** 같은 문제를 피하고자 클러스터 전체에 걸쳐 데이터를 균등하게 분배합니다.

사용자 정의 파티셔너를 사용하려면 구조적 API 로 RDD 를 얻고 사용자 정의 파티셔너를 적용한 다음 다시 DataFrame 이나 Dataset 으로 변환해야 합니다. 이는 필요시에만 사용자 정의 파티셔닝을 사용할 수 있으므로 구조적 API 와 RDD 의 장점을 모두 활용할 수 있습니다.

사용자 정의 파티셔닝을 사용하려면 Partitioner 를 확장한 클래스를 구현해야 합니다. 문제에 대한 업무 지식을 충분히 가지고 있는 경우에만 사용해야 합니다. 단일 값이나 다수 값을 파티셔닝해야 한다면 DataFrame API 를 사용하는 것이 좋습니다.

```scala
// in Scala
val df = spark.read.option("header", "true").option("inferSchema", "true")
  .csv("/data/retail-data/all/")
val rdd = df.coalesce(10).rdd
```

HashPartitioner 와 RangePartitioner 는 RDD API 에서 사용할 수 있는 내장형 파티셔너입니다. 각각 이산형과 연속형 값을 다룰 때 사용합니다.

두 파티셔너는 구조적 API 와 RDD 모두 사용할 수 있습니다.

```scala
// in Scala
import org.apache.spark.HashPartitioner

rdd.map(r => r(6)).take(5).foreach(println)
val keyedRDD = rdd.keyBy(row => row(6).asInstanceOf[Int].toDouble)

keyedRDD.partitionBy(new HashPartitioner(10)).take(10)
```

HashPartitioner 와 RangePartitioner 는 유용하지만 매우 기초적인 기능을 제공합니다. 매우 큰 데이터나 심각하게 치우친 Key 를 다뤄야 한다면 고급 파티셔닝 기능을 사용해야 합니다.

이 현상을 Key 치우침이라 합니다. 이는 어떤 Key 가 다른 Key 에 비해 아주 많은 데이터를 가지는 현상을 의미합니다. 병렬성을 개선하고 실행 과정에서 OutOfMemoryError 를 방지할 수 있도록 Key 를 최대한 분할해야 합니다.

Key 가 특정 형태를 띠는 경우에는 Key 를 분할해야 합니다. 예를 들어 데이터셋에 항상 분석 작업을 어렵게 만드는 두 명의 고객 정보가 있다면 다른 고객의 정보와 두 고객의 정보를 분리해야 합니다. 물론 다른 고객의 정보를 하나의 그룹으로 묶어서 처리할 수 있습니다.

하지만 두 고객의 정보와 관련된 데이터가 너무 많이 치우침이 심하게 발생한다면 나누어 처리해야 합니다.

```scala
// in Scala
import org.apache.spark.Partitioner
class DomainPartitioner extends Partitioner {
 def numPartitions = 3
 def getPartition(key: Any): Int = {
   val customerId = key.asInstanceOf[Double].toInt
   if (customerId == 17850.0 || customerId == 12583.0) {
     return 0
   } else {
     return new java.util.Random().nextInt(2) + 1
   }
 }
}

keyedRDD
  .partitionBy(new DomainPartitioner).map(_._1).glom().map(_.toSet.toSeq.length)
  .take(5)
```

위 예제를 실행하면 각 파티션 수를 확인할 수 있습니다. 데이터를 임의로 분산하여 두 숫자가 다를수도 있습니다.

사용자 정의 키 분배 로직은 RDD 수준에서만 사용할 수 있습니다. 이 로직은 임의의 로직을 사용해 물리적인 방식으로 클러스터에 데이터를 분배하는 강력한 방법입니다.

## Custom Serialization

마지막은 Kryo 직렬화 관련 내용입니다. 병렬화 대상인 모든 객체나 함수는 직렬화할 수 있어야 합니다.

```scala
// in Scala
class SomeClass extends Serializable {
  var someValue = 0
  def setSomeValue(i:Int) = {
    someValue = i
    this
  }
}

sc.parallelize(1 to 10).map(num => new SomeClass().setSomeValue(num))
```

기본 직렬화 기능은 매우 느릴 수 있습니다. Spark 는 Kryo 라이브러리를 사용해 더 빠르게 객체를 직렬화할 수 있습니다. Kryo 는 Java 직렬화보다 10 배 이상 성능이 더 좋으며 간결합니다. 하지만 모든 직렬화 유형을 지원하지는 않습니다. 그리고 최상의 성능을 얻기 위해 프로그램에서 사용할 클래스를 사전에 등록해야 합니다.

SparkConf 를 사용해 잡을 초기화하는 시점에서 `spark.serializer` 속성값을 *org.apache.spark.serializer.KryoSerializer* 로 설정해 Kry 를 사용할 수 있습니다. 

`spark.serializer` 설정으로 워커 노드 간 데이터 셔플링과 RDD 를 직렬화해 디스크에 저장하는 용도로 시리얼라이저를 지정할 수 있습니다. Kryo 가 기본 값이 아닌 유일한 이유는 사용자가 직접 클래스를 등록해야 하기 때문입니다. 그리고 네트워크에 민감한 어플리케이션에서 사용하는게 좋습니다.

Spark 2.0.0 버전부터 단순 데이터 타입, 단순 데이터 타입의 배열, 문자열 데이터 타입의 RDD 를 셔플링하면 내부적으로 Kryo 시리얼라이저에 등록합니다.

Kryo 에 사용자 정의 클래스를 등록하려면 registerKryoClasses 메소드를 사용합니다.

```scala
// in Scala
val conf = new SparkConf().setMaster(...).setAppName(...)
conf.registerKryoClasses(Array(classOf[MyClass1], classOf[MyClass2]))
val sc = new SparkContext(conf)
```

