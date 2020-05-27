---
title : Spark Distributed Shared Variables
tags :
- Accumulator
- Broadcast Variable
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

Spark 저수준 API 에는 RDD 외에도 두 번째 유형인 **분산형 공유 변수(distributed shared variables)** 가 있습니다. 이는 브로드캐스트 변수와 어큐물레이터라는 두 개의 타입이 존재합니다.

클러스터를 실행할 때 특별한 속성을 가진 사용자 정의 함수에서 이 변수를 사용할 수 있습니다. 특히 **어큐뮬레이터(Accumulator)** 를 사용하면 모든 태스크의 데이터를 공유 결과에 추가할 수 있습니다.

예를 들어, 잡의 입력 레코드를 파싱하면서 얼마나 많은 오류가 발생했는지 확인하는 카운터를 구현할 수 있습니다. 반면 **브로드캐스트 변수(Brocast Variable)** 를 사용하면 모든 워커 노드에 큰 값을 저장하므로 재전송 없이 많은 Spark 액션에서 재사용할 수 있습니다.

## Broadcast Variables

브로드캐스트 변수는 변하지 않는 값을 **클로저(Closure)** 함수의 변수로 캡슐화하지 않고 클러스터에서 효율적으로 공유하는 방법을 제공합니다. 태스크에서 드라이버 노드의 변수를 사용할 때는 클로저 함수 내부에서 단순하게 참조하는 방법을 사용합니다.

하지만 이는 비효율적입니다. 룩업 테이블이나 머신러닝 모델 같은 큰 변수를 사용하는 겨우 더 비효율적입니다. 왜냐하면 크롤저 함수에서 변수를 사용할 때 워커노드에서 여러 번 역직렬화가 일어나기 때문입니다. 게다가 여러 Spark 액션과 잡에서 동일한 변수를 사용하면 잡을 실행할 때마다 워커로 큰 변수를 재전송합니다.

이 상황에선 브로드캐스트 변수를 사용합니다. 이 변수는 모든 태스크마다 직렬화하지 않고 클러스터의 모든 머신에 캐시하는 불변성 공유 변수입니다. `Example 1` 처럼 익스큐터 메모리 크기에 맞는 조회용 테이블을 전달하고 함수에 사용하는 것이 대표적인 예입니다.

> Example 1 - Broadcast variables

![image](https://user-images.githubusercontent.com/44635266/81498892-7a579800-9302-11ea-8d41-5e6203404fa5.png)

예를 들어 아래와 같이 단어나 값의 목록을 가지고 있다고 가정하겠습니다.

```scala
// in Scala
val myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"
  .split(" ")
val words = spark.sparkContext.parallelize(myCollection, 2)
```

어떤 크기를 가진 다른 정보와 함께 단어 목록을 추가해야 할 수도 있습니다. 이 처리는 SQL 의 오른쪽 조인에 해당합니다.

```scala
// in Scala
val supplementalData = Map("Spark" -> 1000, "Definitive" -> 200,
                           "Big" -> -300, "Simple" -> 100)
```

이 구조체를 Spark 에 브로드캐스트할 수 있으며 `suppBroadcast` 변수를 이용해 참조합니다. 이 값은 불변성이며 액션을 실행할 때 클러스터의 모든 노드에 지연 처리 방식으로 복제됩니다.

```scala
// in Scala
val suppBroadcast = spark.sparkContext.broadcast(supplementalData)
```

`suppBroadcast` 변수의 `value` 메소드를 사용해 위 예제에 브로드캐스트된 `supplementalData` 값을 참조할 수 있습니다. `value` 메소드는 직렬화된 함수에서 브로드캐스트된 데이터를 직렬화하지 않아도 접근할 수 있습니다.

Spark 는 브로드캐스트 기능을 이용해 데이터를 보다 효율적으로 전송하므로 직렬화와 역직렬화에 대한 부하를 크게 줄일 수 있습니다.

```scala
// in Scala
suppBroadcast.value
```

이제 브로드캐스트된 데이터를 사용해 RDD 를 변환할 수 있습니다.

아래는 맵 연산의 처리 과정에 따라 Key - Value 쌍 데이터를 생성합니다. 값이 비어 있는 경우 간단히 0 으로 치환합니다.

```scala
// in Scala
words.map(word => (word, suppBroadcast.value.getOrElse(word, 0)))
  .sortBy(wordPair => wordPair._2)
  .collect()
```

결과는 아래와 같습니다.

```
[('Big', -300),
 ('The', 0),
...
 ('Definitive', 200),
 ('Spark', 1000)]
```

브로드 캐스트 변수를 사용한 방식과 클로저에 담아 전달하는 방식의 유일한 차이점은 브로드캐스트 변수를 사용하는 것이 훨씬 더 효율적이라는 겁니다. 당연히 데이터의 총량과 익스큐터수에 따라 다룰 수 있으며 아주 작은 데이터를 작은 클러스터에서 돌린다면 크게 차이가 나지 않을 수 있습니다.

브로드캐스트 변수에 작은 클러스터에서 돌린다면 크게 차이가 나지 않을 수 있습니다. 브로드캐스트 변수에 작은 크기의 딕셔너리 타입을 사용한다면 큰 부하가 발생합니다. 하지만 훨씬 큰 크기의 데이터를 사용하는 경우라면 전체 태스크에서 데이터를 직렬화하는 데 발생하는 부하가 매우 커질 수 있습니다.

여기서 중요한 점은 RDD 영역에서 브로드캐스트 변수를 사용한다는 겁니다. 그리고 UDF 나 Dataset 에서도 사용할 수 있으며 동일한 효과를 얻을 수 있습니다.

## Accumulators

어큐뮬레이터는 Spark 의 두 번째 공유 변수 타입입니다. 이는 트랜스포메이션 내부의 다양한 값을 갱신하는데 사용합니다. 그리고 내고장성을 보장하면서 효율적인 방식으로 드라이버에 값을 전달할 수 있습니다.

> Example 2 - Accumulator variable

![image](https://user-images.githubusercontent.com/44635266/81565822-ee627080-93d4-11ea-8936-2c4d7cbbd1ea.png)

어큐뮬레이터는 Spark 클러스터에서 로우 단위로 안전하게 값을 갱신할 수 있는 변경 가능한 변수를 제공합니다. 그리고 디버깅용이나 저수준 집계 생성용으로 사용할 수 있습니다. 예를 들어 파티션별로 특정 변수의 값을 추적하는 용도로 사용할 수 있으며 시간이 흐를수록 더 유용하게 사용됩니다.

어큐뮬레이터는 결합성과 가환성을 가진 연산을 통해서만 더할 수 있는 변수이므로 병렬 처리 과정에서 효율적으로 사용할 수 있습니다. 어큐뮬레이터는 카운터나 합계를 구하는 용도로 사용할 수 있습니다. Spark 는 기본적으로 수치형 어큐뮬레이터를 지우너하며 사용자 정의 어큐뮬레이터를 만들어 사용할 수 있습니다.

어큐뮬레이터의 값은 액션을 처리하는 과정에서만 갱신됩니다. Spark 는 각 태스크에서 어큐뮬레이터를 한 번만 갱신하도록 제어합니다 따라서 재시작한 태스크는 어큐뮬레이터값을 갱신할 수 없습니다. 트랜스포메이션에서 태스크나 잡 스테이지를 재처리하는 경우 각 태스크의 갱신 작업이 두 번 이상 적용될 수 있습니다.

어큐뮬레이터는 Spark 의 지연 연산 모델에 영향을 주지 않습니다. 어큐뮬레이터가 RDD 처리 중에 갱신되면 RDD 연산이 실제로 수행된 시점, 즉 특정 RDD 나 그 RDD 의 부모 RDD 에 액션을 실행하는 시점에 한 번만 값을 갱신합니다. 따라서 `map` 같은 함수 지연 처리 형태의 트랜스포메이션에서 어큐뮬레이터 갱신 작업을 수행하는 경우 실제 실행 전까지는 어큐뮬레이터가 갱신되지 않습니다.

어큐뮬레이터의 이름은 선택적으로 지정할 수 있습니다. 이름이 지정된 어큐뮬레이터 실행 결과는 Spark UI 에 표시되며, 이름이 지정되지 않은 어큐뮬레이터의 경우 Spark UI 에 표시되지 않습니다.

### Basic Example

이전에 만들었던 항공운항 데이터셋에 사용자 정의 집계를 수행하면서 어큐뮬레이터를 사용해보겠습니다. 아래 예제는 RDD API 가 아닌 Dataset API 를 사용합니다.

```scala
// in Scala
case class Flight(DEST_COUNTRY_NAME: String,
                  ORIGIN_COUNTRY_NAME: String, count: BigInt)
val flights = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet")
  .as[Flight]
```

출발지나 도착지가 중국인 항공편의 수를 구하는 어큐뮬레이터를 생성하겠습니다.

이런 유형의 집계는 SQL 로 처리할 수 있습니다. 하지만 어큐뮬레이터를 사용해 프로그래밍 방식으로 처리해보겠습니다. 아래 예제는 이름이 지정되지 않은 어큐뮬레이터를 생성합니다.

```scala
// in Scala
import org.apache.spark.util.LongAccumulator
val accUnnamed = new LongAccumulator
val acc = spark.sparkContext.register(accUnnamed)
```

이 예제에는 이름이 지정된 어큐뮬레이터가 적합합니다. 어큐뮬레이터를 만드는 가장 간단한 방법은 SparkContext 를 사용하는 겁니다. 아니면 직접 어큐뮬레이터를 생성하고 이름을 붙여 등록할 수 있습니다.

```scala
// in Scala
val accChina = new LongAccumulator
val accChina2 = spark.sparkContext.longAccumulator("China")
spark.sparkContext.register(accChina, "China")
```

함수의 파라미터로 문자열값을 전달하거나 `register` 함수의 두 번째 파라미터를 사용해 이름을 지정할 수 있습니다. 이름이 지정된 어큐뮬레이터는 실행 결과를 Spark UI 에서 확인할 수 있으며 이름이 지정되지 않았다면 Spark UI 에서 확인할 수 없습니다.

다음은 어큐뮬레이터에 값을 더하는 방법을 정의하는 단계입니다. 아래 예제의 함수는 직관적인 형태로 구성되어 있습니다.

```scala
// in Scala
def accChinaFunc(flight_row: Flight) = {
  val destination = flight_row.DEST_COUNTRY_NAME
  val origin = flight_row.ORIGIN_COUNTRY_NAME
  if (destination == "China") {
    accChina.add(flight_row.count.toLong)
  }
  if (origin == "China") {
    accChina.add(flight_row.count.toLong)
  }
}
```

이제 `foreach` 를 이용해 항공운항 데이터셋의 전체 로우를 처리하겠습니다. 이렇게 하는 이유는 `foreach` 메소드가 액션이고 Spark 는 액션에서만 어큐뮬레이터의 실행을 보장하기 때문입니다. `foreach` 메소드는 입력 DataFrame 의 매 로우마다 함수를 한 번씩 적용해 어큐뮬레이터값을 증가시킵니다.

```scala
// in Scala
flights.foreach(flight_row => accChinaFunc(flight_row))
```

이 연산은 빠르게 종료되며 `Example 3` 과 같이 Spark UI 에서 익스큐터 단위로 어큐뮬레이터값을 확인할 수 있습니다.

> Example 3 - Executor Spark UI

![image](https://user-images.githubusercontent.com/44635266/81566553-fec71b00-93d5-11ea-8bde-09291a7414c7.png)

어큐뮬레이터값을 프로그래밍 방식으로 조회할 수 있습니다. 이 경우 `value` 속성을 사용합니다.

```scala
// in Scala
accChina.value // 953
```

### Custom Accumulators

Spark 는 몇가지 기본 어큐뮬레이터를 제공합니다. 하지만 때에 따라 사용자 정의 어큐뮬레이터가 필요할 수 있습니다. 어큐뮬레이터를 직접 정의하려면 AccumulatorV2 클래스를 상속받아야 합니다.

아래 예제와 같이 구현해야 하는 추상 메소드가 몇 가지 있습니다. 다음은 어큐뮬레이터에 짝수값만 더하는 예제입니다. 간단하지만 사용자 정의 어큐뮬레이터를 구현하는 과정이 얼마나 쉬운지 알 수 있습니다.

```scala
// in Scala
import scala.collection.mutable.ArrayBuffer
import org.apache.spark.util.AccumulatorV2

val arr = ArrayBuffer[BigInt]()

class EvenAccumulator extends AccumulatorV2[BigInt, BigInt] {
  private var num:BigInt = 0
  def reset(): Unit = {
    this.num = 0
  }
  def add(intValue: BigInt): Unit = {
    if (intValue % 2 == 0) {
        this.num += intValue
    }
  }
  def merge(other: AccumulatorV2[BigInt,BigInt]): Unit = {
    this.num += other.value
  }
  def value():BigInt = {
    this.num
  }
  def copy(): AccumulatorV2[BigInt,BigInt] = {
    new EvenAccumulator
  }
  def isZero():Boolean = {
    this.num == 0
  }
}
val acc = new EvenAccumulator
val newAcc = sc.register(acc, "evenAcc")

acc.value // 0
flights.foreach(flight_row => acc.add(flight_row.count))
acc.value // 31390
```