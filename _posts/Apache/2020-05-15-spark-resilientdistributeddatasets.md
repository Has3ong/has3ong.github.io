---
title : Spark RDD(Resilient Distributed Datasets)
tags :
- RDD
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

대부분 상황에서 고수준 API 를 사용하는 것이 좋습니다. 하지만 기술적 문제를 고수준 API 를 사용해 모두 처리할 수 있는것이 아닙니다. 이런 경우 Spark 의 저수준 API 를 사용해야 할 수도 있습니다. Spark 의 저수준 API 는 RDD, SparkContext 그리고, **어큐뮬레이터(Accumulator)** 와 **브로드캐스트 변수(Broadcast Variable)** 같은 **분산형 공유 변수(Distributed Shared Variables)** 등을 의미합니다.

## What Are the Low-Level APIs?

Spark 에는 두 종류의 저수준 API 가 있습니다. 분산 데이터 처리를 위한 RDD 이며, 다른 하나는 브로드캐스트 변수와 어큐뮬레이터처럼 분상형 공유 변수를 배포하고 다루기 위한 API 입니다.

### When to Use the Low-Level APIs?

다음과 같은 상황에서 저수준 API 를 사용합니다.

* 고수준 API 에서 제공하지 않는 기능이 필요한 경우. 예를 들어 클러스터의 물리적 데이터의 배치를 아주 세밀하게 제어해야 하는 상황
* RDD 를 사용해 개발된 기존 코드를 유지하는 경우
* 사용자가 정의한 공유 변수를 다뤄야 하는 경우

위 같은 상황에서만 저수준 API 기능을 사용합니다. 하지만 Spark 의 모든 워크로드는 저수준 기능을 사용하는 기초적인 형태로 컴파일 되므로 이를 이해하는 것은 많은 도움이 될 수 있습니다. DataFrame 트랜스포메이션을 호출하면 다수의 RDD 트랜스포메이션으로 변환됩니다. 이 관계를 이해하면 점점 더 복잡해지는 워크로드를 디버깅하는 작업이 더 쉬워질 겁니다.

### How to Use the Low-Level APIs?

SparkContext 는 저수준 API 기능을 사용하기 위한 진입 지점입니다. Spark 클러스터에서 연산을 수행하는 데 필요한 도구인 SparkSession 을 이용하여 SparkContext 에 접근할 수 있습니다. 아래 명령으로 SparkContext 에 접근할 수 있습니다.

```
spark.sparkContext
```

## About RDDs

RDD 는 Spark 1.x 버전의 핵심 API 입니다.

RDD 는 불변성을 가지며 병렬로 처리할 수 있는 파티셔닝된 레코드의 모음입니다. DataFrame 의 각 레코드는 스키마를 알고 있는 필드로 구성된 구조화된 로우인 반면, RDD 의 레코드는 프로그래머가 선택하는 Java, Scala, Python 객체입니다.

RDD 의 모든 레코드는 Java 나 Python 의 객체이므로 완벽하게 제어할 수 있습니다. 이 객체에는 사용자가 원하는 포맷을 사용해 원하는 모든 데이터를 가질 수 있습니다. 모든 값을 다루거나, 값 사이의 상호작용 과정을 반드시 수동으로 정의해야합니다.

또한 구조적 API 와는 다르게 레코드의 내부 구조를 Spark 에서 파악할 수 없으므로 최적화를 하려면 더 많은 수작업이 필요합니다. 예를 들어 Spark 의 구조적 API 는 자동으로 데이터를 최적화하고 압축된 바이너리 포맷으로 저장합니다. 반면 저수준 API 에서 동일한 공간 효율성과 성능을 얻으려면 객체에 이런 포맷 타입을 구현해 모든 저수준 연산 과정에서 사용해야 합니다. 이와 유사하게 Spark SQL 에서 자동으로 수행되는 필터 재정렬과 집계 같은 최적화 기법도 구현해야 합니다. 그러므로 Spark 의 구조적 API 를 사용할 것을 권고합니다.

RDD 는 Dataset 과 유사하지만 RDD 는 구조화된 데이터 엔진을 사용해 데이터를 저장하거나 다루지 않습니다.

### Types of RDDs

Spark API 문서를 보면 RDD 에 수많은 하위 클래스가 존재한다는 사실을 알 수 있습니다. RDD 는 DataFrame API 에서 최적화된 물리적 실행 계획을 만드는 데 대부분 사용합니다.

사용자는 두 가지 타입의 RDD 를 가질 수 있습니다. 하나는 Generic RDD 타입이며, 다른 하나는 Key-Value RDD 입니다. 목적에 맞게 두 RDD 중 하나를 선택할 수 있습니다. 둘 다 객체의 컬렉션을 표현하지만 Key-Value RDD 는 특수 연산뿐만 아니라 키를 이용한 사용자 지정 파티셔닝 개념을 가지고 있습니다.

RDD 는 다음 5 개의 주요 속성으로 구분됩니다.

* 파티션 목록
* 각 조각을 연산하는 함수
* 다른 RDD 와의 의존성 목록
* 부가적으로 Key - Value RDD 를 위한 Partitioner
* 부가적으로 각 조각을 연산하기 위한 기본 위치 목록(ex: HDFS 파일의 블록위치)

이러한 속성은 사용자 프로그램을 스케줄링하고 실행하는 Spark 의 모든 처리 방식을 결정합니다. 각 RDD 유형은 앞서 나열한 각 속성에 대한 구현체를 가지고 있습니다. 사용자는 각 속성을 구현하여 새로운 데이터소스를 정의할 수 있습니다.

RDD 는 Spark 프로그래밍 패러다임을 그대로 따릅니다. RDD 역시 분산환경에서 데이터를 다루는 데 필요한 지연 처리 방식의 트랜스포메이션과 즉시 실행 방식의 액션을 제공합니다. 그리고 DataFrame 과 Dataset 과 동일하게 동작합니다. RDD 에는 Row 라는 개념이 없습니다. 개별 레코드는 Java, Scala, Python 객체일 뿐이며 구조적 API 에서 제공하는 여러 함수를 사용하지 못하기 때문에 수동으로 처리해야 합니다.

RDD API 는 Scala 와 Java 뿐만 아니라 Python 에서도 사용할 수 있습니다. Scala 와 Java 를 사용하는 경우 비슷한 성능이 나오지만, 원형 객체를 다룰 때는 큰 성능 손실이 발생할 수 있습니다. 반면 Python 을 사용해 RDD 를 다룰 때는 상당한 성능 저하가 발생할 수 있습니다.

Python 으로 RDD 를 실행하는 것은 Python 으로 만든 사용자 정의 함수를 사용해 로우마다 적용하는 것과 동일하다고 볼 수 있습니다. 직렬화 과정을 거친 데이터를 Python 프로세스에 전달하고, Python 처리가 끝나면 다시 직렬화하여 JVM 머신에 반환합니다. 그러므로 Python 을 사용해 RDD 를 다룰 때는 높은 오버헤드가 발생합니다.

### When to Use RDDs?

정말 필요한 경우가 아니라면 수동으로 RDD 를 생성해서는 안됩니다. RDD 는 많은 강점이 있지만 구조적 API 가 제공하는 여러 최적화 기법을 사용할 수 없습니다. DataFrame 은 RDD 보다 효율적이고 안정적이며 표현력이 좋습니다.

물리적으로 분산된 데이터에 세부적인 제어가 필요할 때 RDD 를 사용하는 것이 가장 적합합니다.

### Datasets and RDDs of Case Classes

Dataset 은 구조적 API 가 제공하는 풍부한 기능과 최적화 기법을 제공합니다. Dataset 을 사용하면 JVM 데이터 타입과 Spark 데이터 타입 중 어떤 것을 쓸지 고민하지 않아도 됩니다. 어떤 것을 사용하더라도 성능은 동일하므로 가장 쉽게 사용할 수 있고 유연하게 대응할 수 있는 데이터 타입을 선택하면 됩니다.

## Creating RDDs

RDD 사용하는 법을 알아보겠습니다.

### Interoperating Between DataFrames, Datasets, and RDDs

RDD 를 얻을 수 있는 가장 쉬운 방법은 기존에 사용하던 DataFrame 이나 Dataset 을 이용하는겁니다. 기존에 사용하던 DataFrame 이나 Dataset 의 `rdd` 메소드를 호출하면 쉽게 RDD 로 변활할 수 있습니다. `Dataset[T]` 를 RDD 로 변환하면 데이터 타입 T 를 가진 RDD 를 얻을 수 있습니다.

이 처리 방식은 Java 와 Scala 에서만 사용할 수 있습니다.

```scala
// in Scala: converts a Dataset[Long] to RDD[Long]
spark.range(500).rdd
```

Python 에는 DataFrame 만 존재하며 Dataset 을 사용할 수 없으므로 Row 타입의 RDD 를 얻습니다.

```python
spark.range(10).rdd
```

위 예제에서 만들어진 데이터를 처리하려면 아래 예제처럼 Row 객체를 올바른 데이터 타입으로 변환하거나 Row 객체에서 값을 추출해야 합니다. 처리가 끝나면 Row 타입을 가진 RDD 가 반환됩니다.

```scala
// in Scala
spark.range(10).toDF().rdd.map(rowObject => rowObject.getLong(0))
```

RDD 를 사용해 DataFrame 이나 Dataset 을 생성할 때도 동일한 방법을 사용합니다. RDD 의 `toDF` 메소드를 호출하면 됩니다.

```scala
// in Scala
spark.range(10).rdd.toDF()
```

`rdd` 메소드는 Row 타입을 가진 RDD 를 생성합니다. Row 타입은 Spark 가 구조적 API 에서 데이터를 표현하는 데 사용하는 내부 카탈리스트 포맷입니다. 이 기능을 사용하면 상황에 따라 구조적 API 와 저수준 API 사이를 오고가게 만들 수 있습니다.

RDD API 와 Dataset API 는 구조적 API 가 제공하는 여러 가지 기능과 인터페이스를 가지고 있지 않으므로 매우 유사하게 느껴질 수 있습니다.

### From a Local Collection

컬렉션 객체를 RDD 로 만들려면 SparkContext 의 `parallelize` 메소드를 호출해야 합니다. 이 메소드는 단일 노드에 있는 컬렉션을 병렬 컬렉션으로 전환합니다. 또한 파티션 수를 명시적으로 지정할 수 있습니다. 아래는 두 개의 파티션을 가진 병렬 컬렉션 객체를 만듭니다.

```scala
// in Scala
val myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"
  .split(" ")
val words = spark.sparkContext.parallelize(myCollection, 2)
```

RDD 에 이름을 지정하면 Spark UI 에 지정한 이름으로 RDD 가 표시됩니다.

```scala
// in Scala
words.setName("myWords")
words.name // myWords
```

### From Data Sources

데이터소스나 텍스트 파일을 이용해 RDD 를 생성할 수 있지만 DataSource API 를 사용하는 것이 더 바람직합니다. RDD 에는 DataFrame 이 제공하는 DataSource API 라는 개념이 없습니다. RDD 는 주로 RDD 간의 의존성 구조와 파티션 목록을 정의합니다. DataSource API 는 데이터를 읽는 가장 좋은 방법입니다. `sparkContext` 를 사용해 데이터를 RDD 로 읽을 수 있습니다. 다음은 줄 단위로 텍스트 파일을 읽는 예제입니다.

```scala
spark.sparkContext.textFile("/some/path/withTextFiles")
```

예제는 여러 텍스트 파일의 각 줄을 레코드로 가진 RDD 를 생성합니다. 또한 텍스트 파일 하나를 레코드로 읽어야 하는 경우도 있습니다. 예를 들어 JSON 객체나 문서로 구헝된 파일을 개별 레코드로 처리해야 할 수 있습니다.

```scala
spark.sparkContext.wholeTextFiles("/some/path/withTextFiles")
```

생성된 RDD 에서 파일명은 첫 번째 객체인 RDD 의 키가되며 텍스트 파일의 값은 두 번째 문자열 객체인 RDD 의 값이 됩니다.

## Manipulating RDDs

RDD 를 다루는 방식은 DataFrame 을 다루는 방식과 매우 유사합니다. RDD 는 Spark 데이터 타입 대신 Java 나 Scala 의 객체를 다룹니다. 또한 연산을 단순화하는 헬퍼 메소드나 함수도 DataFrame 에 비해 많이 부족합니다. 그러므로 필터, 맵, 집계 그리고 DataFrame 의 다양한 함수를 사용자가 직접 정의해야 합니다.

RDD 에 다양한 기능을 정의해보겠습니다.

## Transformations

대부분의 RDD 트랜스포메이션은 구조적 API 에서만 사용할 수 있는 기능을 가지고 있습니다. DataFrame 이나 Dataset 과 동일하게 RDD 에 트랜스포메이션을 지정해 새로운 RDD 를 생성할 수 있습니다. 

이때 RDD 에 포함된 데이터를 다루는 함수에 따라 다른 RDD 에 대한 의존성도 함께 정의합니다.

### distinct

RDD 의 `distinct` 메소드를 호출하면 중복된 데s이터를 제거합니다.

```scala
words.distinct().count()
```

### filter

필터링은 SQL 의 `where` 조건절을 생성하는 것과 비슷합니다. RDD 의 레코드를 모두 확인하고 조건 함수를 만족하는 레코드만 반환합니다. 조건 함수는 필터 함수로 동작하므로 불리언 타입으로 반환해야 합니다.

모든 로우는 어떠한 경우라도 입력값을 가지고 있어야 합니다. 아래 예제는 문자 `S` 로 시작하는 단어만 남도록 RDD 를 필터링 합니다. 

```scala
// in Scala
def startsWithS(individual:String) = {
  individual.startsWith("S")
}
```

조건 함수를 정의했으니 데이터를 필터링해보겠습니다. 이 함수 역시 RDD 의 레코드를 개별적으로 처리합니다.

```scala
// in Scala
words.filter(word => startsWithS(word)).collect()
```

이 코드는 Spark 의 Simple 이라는 결과를 사용한 언어의 데이터 타입으로 반환합니다. 그 이유는 데이터를 Row 타입으로 강제 변환하거나 데이터를 수집한 다음 변환할 필요가 없기 때문입니다.

### map

주어진 입력을 원하는 값으로 반환하는 함수를 명시하고 레코드별로 적용합니다. 설명을 위해 이전 예제와 유사한 처리를 수행해보겠습니다. 아래는 현재 단어를 *단어*, *단어의 시작 문자*, *첫 문자가 S 인지 아닌지* 순서로 매핑합니다.

람다 구문을 사용해 함수를 한 줄로 정의했습니다.

```scala
// in Scala
val words2 = words.map(word => (word, word(0), word.startsWith("S")))
```

새로 만든 함수의 세 번째 반환값인 불리언값으로 필터링할 수 있습니다.

```scala
// in Scala
words2.filter(record => record._3).take(5)
```

*Spark*, *S*, *true* 와 *Simple*, *S*, *ture* 가 결과로 반환됩니다.

#### FLATMAP

`flatMap` 메소드는 `map` 함수의 확장 버전입니다. 단일 로우를 여러 로우로 변환해야 하는 경우가 있습니다. 예를 들어 `flatMap` 메소드를 사용해 단어를 문자 집합으로 변환할 수 있습니다.

각 단어는 여러 문자로 구성되어 있으므로 `flatMap` 메소드를 사용해 다수의 로우로 변환할 수 있습니다. `flatMap` 은 확장 가능한 `map` 함수의 출력을 반복 처리할 수 있는 형태로 반환합니다.

```scala
// in Scala
words.flatMap(word => word.toSeq).take(5)
```

결과는 *S*, *P*, *A*, *R*, *K* 입니다.

### sort

RDD 를 정렬하려면 `sortBy` 메소드를 사용합니다. 다른 RDD 작업과 마찬가지로 함수를 지정해 RDD 의 데이터 객체에서 값을 추출한 다음 값을 기준으로 정렬합니다. 예를 들어 다음 예제는 단어 길이가 가장 긴 것부터 짧은 순으로 정렬합니다.

```scala
// in Scala
words.sortBy(word => word.length() * -1).take(2)
```

### Random Splits

`randomSplit` 메소드는 RDD 를 임의로 분할해 RDD 배열을 만들 때 사용하며, 가중치와 **난수 시드(Random Seed)** 로 구성된 배열을 파라미터로 사용합니다.

```scala
// in Scala
val fiftyFiftySplit = words.randomSplit(Array[Double](0.5, 0.5))
```

위 코드는 개별로 다룰 수 있는 RDD 배열을 결과로 반환합니다.

## Actions

DataFrame 과 Dataset 에서 했던 것처럼 지정된 트랜스포메이션 연산을 시작하려면 액션을 사용합니다. 액션은 데이터를 드라이버로 모으거나 외부 데이터 소스로 내보낼 수 있습니다.

### reduce

RDD 의 모든 값을 하나의 값으로 만들려면 `reduce` 메소드를 사용합니다. 예를 들어 정수형 집합이 주어진다면 두 개의 입력값을 하나로 줄이는 함수를 사용해 합계를 구할 수 있습니다. 함수형 프로그래밍에 익숙한 개념입니다.

```scala
// in Scala
spark.sparkContext.parallelize(1 to 20).reduce(_ + _) // 210
```

단어 집합에서 가장 긴 단어를 ㅊ자는 예제는 `reduce` 를 사용해 처리할 수 있습니다.

```scala
// in Scala
def wordLengthReducer(leftWord:String, rightWord:String): String = {
  if (leftWord.length > rightWord.length)
    return leftWord
  else
    return rightWord
}

words.reduce(wordLengthReducer)
```

`wordLengthReducer` 함수는 두 개의 입력값을 하나의 결과로 만들기 때문에 `reduce` 메소드를 설명하는 데 적합합니다. 파티션에 대한 리듀스 연산은 비결정적 특성을 가집니다. 따라서 길이가 10 인 *definitive* 나 *processing* 중 하나가 `leftWord` 변수에 할당될 수 있습니다. 즉, `reduce` 메소드를 실행할 때마다 다른 결과를 반환할 수 있습니다.

### count

`count` 함수를 사용하면 RDD 의 전체 로우 수를 알 수 있습니다.

```scala
words.count()
```

#### COUNTAPPROX

이 함수의 반환 결과는 조금 이상해 보이지만 꽤 정교합니다. 앞서 알아본 `count` 함수의 근사치를 제한 시간 내에 계산합니다. 제한 시간을 초과하면 불완전한 결과를 반환할 수 있습니다.

신뢰도(`confidence`) 는 실제로 연산한 결과와의 오차율을 의미합니다. 즉, `countApprox` 메소드의 신뢰도를 0.9 로 설정하고 반복적으로 호출하면 실제 연산 결과와 동일한 값이 90 % 이상 포함될 것으로 기대할 수 있습니다. 신뢰도는 `[0,1]` 범위의 값이어야 하며, 범위를 벗어나면 예외가 발생합니다.

```scala
val confidence = 0.95
val timeoutMilliseconds = 400
words.countApprox(timeoutMilliseconds, confidence)
```

#### COUNTAPPROXDISTINCT

`countApproxDistinct` 메소드의 첫 번재 구현체에서는 상대 정확도를 파라미터로 사용합니다. 이 값을 작게 설정하면 더 많은 메모리 공간을 사용하는 카운터가 생성됩니다. 설정 값은 반드시 0.000017 보다 커야 합니다.

```scala
words.countApproxDistinct(0.05)
```

다른 구현체를 사용하면 동작을 세부적으로 제어할 수 있습니다. 상대 정확도를 지정할 때 두 개의 파라미터를 사용합니다. 하나는 일반 데이터를 위한 파라미터이며, 다른 하나는 희소 표현을 위한 파라미터 입니다.

두 인수 `p` 와 `sp` 는 정밀도와 희소 정밀도를 의미합니다. 상대 정확도는 대략 $1.054 / sqrt(2^p)$ 입니다. 카디널리티가 작을 때 0 이 아닌 값($sp > p$) 를 설정하면 메모리 소비를 줄이면서 정확도를 증가시킬 수 있습니다. 두 파라미터 모두 정수 데이터 타입을 사용합니다.

```scala
words.countApproxDistinct(4, 10)
```

#### COUNTBYVALUE

이 메소드는 RDD 값의 개수를 구합니다. 결과 데이터셋을 드라이버의 메모리로 읽어들여 처리합니다. 이 메소드를 사용하면 익스큐터의 연산 결과가 드라이버 메모리에 모두 적재됩니다. 따라서 결과가 작은 경우에만 사용해야 합니다.

그러므로 이 메소드는 전체 로우 수나 고유 아이템 수가 작은 경우에만 사용하는 것이 좋습니다.

```scala
words.countByValue()
```

#### COUNTBYVALUEAPPROX

`count` 함수와 동일한 연산을 수행하지만 근사치를 계산합니다. 이 함수는 반드시 지정된 제한 시간 내에 처리해야 합니다. 제한 시간을 초과하면 불완전한 결과를 반환할 수 있습니다.

신뢰도는 실제로 연산한 결과와의 오차율을 의미합니다. 즉, `countByValueApprox` 메소드의 신뢰도를 0.9 로 설정하고 반복적으로 호출하면 실제 연산 결과와 동일한 값이 90 % 이상 포함됩니다. 신뢰도는 `[0,1]` 범위의 값이어야 하며 범위를 벗어나면 예외가 발생합니다.

```scala
words.countByValueApprox(1000, 0.95)
```

### first

`first` 메소드는 데이터셋의 첫 번째 값을 반환합니다.

```scala
words.first()
```

### max and min

`max` 와 `min` 메소드는 각각 최댓값과 최솟값을 반환합니다.

```scala
spark.sparkContext.parallelize(1 to 20).max()
spark.sparkContext.parallelize(1 to 20).min()
```

### take

`take` 와 파생 메소드는 RDD 에서 가져올 값의 개수를 파라미터로 사용합니다. 이 메소드는 먼저 하나의 파티션을 스캔합니다. 그 다음에 해당 파티션의 결과 수를 이용해 파라미터로 지정된 값을 만족하는 데 필요한 추가 파티션 수를 예측합니다.

또한 `takeOrdered`, `takeSample` 그리고 `top` 같은 다양한 유사 함수가 존재합니다. RDD 에서 고정 크기의 임의 표본 데이터를 얻기 위해 `takeSample` 함수를 사용할 수 있습니다. `takeSample` 함수는 `withReplacement`, 임의 표본 수, 난수 시드값을 파라미터로 사용합니다. `top` 함수는 암시적 순서에 따라 최상윗값을 선택한다는 점에서 `takeOrdered` 함수와 반대되는 개념으로 볼 수 있습니다.

```scala
words.take(5)
words.takeOrdered(5)
words.top(5)
val withReplacement = true
val numberToTake = 6
val randomSeed = 100L
words.takeSample(withReplacement, numberToTake, randomSeed)
```

## Saving Files

파일 저장은 데이터 처리 결과를 일반 텍스트 파일로 쓰는 것을 의미합니다. RDD 를 사용하면 일반적인 의미의 데이터소스에 저장할 수 없습니다. 각 파티션의 내용을 저장하려면 전체 파티션을 순회하면서 외부 데이터베이스에 저장해야 합니다. 이 방식은 고수준 API 의 내부 처리 과정을 저수준 API 로 구현하는 접근법입니다.

Spark 는 각 파티션의 데이터를 파일로 저장합니다.

### saveAsTextFile

텍스트 파일로 저장하려면 경로를 지정해야 합니다. 필요한 경우 압축코덱을 설정할 수 있습니다.

```scala
words.saveAsTextFile("file:/tmp/bookTitle")
```

압축 코덱을 설정하려면 하둡에서 사용 가능한 코덱을 임포트해야합니다. *org.zpache.hadoop.io.compress* 라이브러리에서 지원하는 코덱을 찾을 수 있습니다.

```scala
// in Scala
import org.apache.hadoop.io.compress.BZip2Codec
words.saveAsTextFile("file:/tmp/bookTitleCompressed", classOf[BZip2Codec])
```

### SequenceFiles

Spark 는 Hadoop 에코시스템을 기반으로 성장해서 다양한 하둡 기능과 잘 호환됩니다. 시퀀스 파일은 바이너리 Key - Value 쌍으로 구성된 플랫 파일이며, 맵 리듀스의 입출력 포맷으로 널리 사용됩니다.

Spark 는 `saveAsObjectFile` 메소드나 명시적인 Key - Value 쌍 데이터 저장 방식을 이용해 시퀀스 파일을 작성할 수 있습니다.

```scala
words.saveAsObjectFile("/tmp/my/sequenceFilePath")
```

### Hadoop Files

데이터를 저장하는 데 사용할 수 있는 여러가지 Hadoop 파일 포맷이 있습니다. Hadoop 파일 포맷을 사용하면 클래스, 출력 포맷, 하둡 설정, 그리고 압축 방식을 지정할 수 있습니다.

이러한 Hadoop 파일 에코시스템이나 기존의 맵리듀스 잡을 깊이 있게 다루는 경우가 아니라면 크게 관련이 없습니다.

## Caching

RDD 캐싱에도 DataFrame 이나 Dataset 의 캐싱과 동일한 원칙이 적용됩니다. RDD 를 캐시하거나 **저장(Persist)** 할 수 있습니다. 기본적으로 캐시와 저장은 메모리에 있는 데이터만을 대상으로 합니다. `setName` 함수를 사용하면 캐시된 RDD 에 이름을 지정할 수 있습니다.

```scala
words.cache()
```

저장소 수준은 싱글턴 객체인 *org.apache.spark.storate.StorageLevel* 의 속성 중 하나로 지정할 수 있습니다.

저장소 수준을 지정하고 나면 아래와 같이 저장소 수준을 조회할 수 있습니다.

```scala
// in Scala
words.getStorageLevel
```

## Checkpointing

DataFrame API 에서 사용할 수 없는 기는 중 하나는 **체크포인팅(Checkpointing)** 개념입니다. 체크포인팅은 RDD 를 디스크에 저장하는 방식입니다. 나중에 저장된 RDD 를 참조할 때는 원본 데이터소스를 다시 계산해 RDD 를 생성하지 않고 디스크에 저장된 중간 결과 파티션을 참조합니다.

이런 동작은 메모리에 저장하지 않고 디스크에 저장하는 사실만 제외한다면 캐싱과 유사합니다. 이 기능은 반복적인 연산 수행 시 매우 유용합니다.

```scala
spark.sparkContext.setCheckpointDir("/some/path/for/checkpointing")
words.checkpoint()
```

이제 words RDD 를 참조하면 데이터소스의 데이터 대신 체크포인트에 저장된 RDD 를 사용합니다.

## Pipe RDDs to System Commands

`pipe` 메소드는 Spark 의 흥미로운 메소드 중 하나입니다. `pipe` 메소드를 사용하면 파이핑 요소로 생성된 RDD 를 외부 프로세스로 전달할 수 있습니다. 이때 외부 프로세스는 파티션마다 한 번씩 처리해 결과 RDD 를 생성합니다.

각 입력 파티션의 모든 요소는 개행 문자 단위로 분할되어 여러 줄의 입력 데이터로 변경된 후 프로세스의 표준 입력에 전달됩니다. 결과 파티션은 프로세스의 표준출력으로 생성됩니다. 이때 표준 출력의 각 줄은 출력 파티션의 하나의 요소가 됩니다. 비어 있는 파티션을 처리할 때도 프로세스는 실행됩니다.

사용자가 정의한 두 함수를 인수로 전달하면 출력 방식을 원하는 대로 변경할 수 있습니다.

아래 예제는 각 파티션을 `wc` 명령에 연결할 수 있습니다. 각 로우는 신규 로우로 전달되므로 로우를 세면 각 파티션별로 로우 수를 얻을 수 있습니다.

```scala
words.pipe("wc -l").collect()
```

### mapPartitions

Spark 는 실제 코드를 실행할 때 파티션 단위로 동작합니다. 또한 `map` 함수에서 반환하는 RDD 의 진짜 형태가 `MapPartitionsRDD` 입니다.

`map` 은 `mapPartitions` 의 로우 단위 처리를 위한 별칭입니다. `mapPartitions` 는 개별 파티션에 대해 `map` 연산을 수행할 수 있습니다. 그 이유는 클러스터에서 물리적인 단위로 개별 파티션을 처리하기 때문입니다.

다음은 데이터의 모든 파티션에 '1' 값을 생성하고 표현식에 따라 파티션 수를 세어 합산합니다.

```scala
// in Scala
words.mapPartitions(part => Iterator[Int](1)).sum() // 2
```

이 메소드는 파티션 단위로 작업을 수행합니다. 따라서 전체 파티션에 대한 연산을 수행할 수 있습니다. RDD 의 전체 하위 데이터셋에 원하는 연산을 수행할 수 있으므로 아주 유용한 기능입니다. 파티션 그룹의 전체 값을 단일 파티션으로 모은 다음 임의의 함수를 적용하고 제어할 수 있습니다.

`mapPartitionsWithIndex` 같이 `mapPartitions` 와 유사한 기능을 제공하는 함수가 있습니다. `mapPartitionsWithIndex` 함수를 사용하려면 인덱스와 파티션의 모든 아이템을 순회하는 이터레이터를 가진 함수를 인수로 지정해야 합니다.

파티션 인덱스는 RDD 의 파티션 번호입니다. 그리고 이 정보를 디버깅에 활용할 수 있습니다. 이 기능을 이용해 `map` 함수가 정상적으로 동작하는지 시험해볼 수 있습니다.

```scala
// in Scala
def indexedFunc(partitionIndex:Int, withinPartIterator: Iterator[String]) = {
  withinPartIterator.toList.map(
    value => s"Partition: $partitionIndex => $value").iterator
}
words.mapPartitionsWithIndex(indexedFunc).collect()
```

### foreachPartition

`mapPartitions` 함수는 처리 결과를 반환하지만 `foreachPartition` 함수는 파티션의 모든 데이터를 순회할 뿐 결과는 반환하지 않습니다. 즉, 반환값의 존재 여부가 두 함수의 차이점입니다. `foreachPartition` 은 각 파티션의 데이터를 데이터베이스에 저장하는 것과 같이 개별 파티션에서 특정 작업을 수행하는 데 매우 적합한 함수입니다.

실제 많은 데이터소스 커넥터에서 이 함수를 사용합니다. 아래는 임의로 생성한 ID 를 이용해 임시 디렉토리에 결과를 저장하는 텍스트 파일 소스를 자체 구현한 예제입니다.

```scala
words.foreachPartition { iter =>
  import java.io._
  import scala.util.Random
  val randomFileName = new Random().nextInt()
  val pw = new PrintWriter(new File(s"/tmp/random-file-${randomFileName}.txt"))
  while (iter.hasNext) {
      pw.write(iter.next())
  }
  pw.close()
}
```

*/tmp* 디렉토리를 조회하면 두 개의 파일을 찾을 수 있습니다.

### glom

`glom` 함수는 데이터셋의 모든 파티션을 배열로 변환하는 흥미로운 함수입니다. 이 기능은 데이터를 드라이버로 모으고 데이터가 존재하는 파티션의 배열이 필요한 경우에 매우 유용합니다.

하지만 파티션이 크거나 파티션 수가 많다면 드라이버가 비정상적으로 종료될 수 있습니다.

아래는 입력된 단어를 두 개의 파티션에 개별적으로 할당하는 예제입니다.

```scala
// in Scala
spark.sparkContext.parallelize(Seq("Hello", "World"), 2).glom().collect()
// Array(Array(Hello), Array(World))
```