---
title : Spark How Spark Runs on a Cluster
tags :
- Cluster
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

## The Architecture of a Spark Application

* Spark Driver 
  * Spark Driver 는 Spark 어플리케이션의 운전자 역할을 하는 프로세스입니다. 드라이버는 Spark 어플리케이션의 실행을 제어하고 Spark 클러스터의 모든 상태 정보를 유지합니다.
  * 또한 물리적 컴퓨팅 자원 확보와 익스큐터 실행을 위해 클러스터 매니저와 통신할 수 있어야 합니다.
  * 요약하면 Spark 드라이버는 물리적 머신의 프로세스이며, 클러스터에서 실행 중인 어플리케이션 상태를 유지합니다.
* Spark Executor
  * Spark Executor 는 Spark Driver 가 할당한 태스크를 수행하는 프로세스입니다.
  * 익스큐터는 드라이버가 할당한 태스크를 받아 실행하고 태스크의 상태와 결괄를 드라이버에 보고합니다. 모든 Spark 어플리케이션은 개별 익스큐터 프로세스를 사용합니다.
* Cluster Manager
  * Spark Driver 와 익스큐터를 허공에 띄울 수는 없으므로 Cluster Manager 가 필요합니다. Cluster Manager 는 Spark 어플리케이션을 실행할 클러스터 머신을 유지합니다.
  * Cluster Manager 는 Driver 와 Worker 라는 개념을 가지고 있으며 이 때문에 혼란스러울 수 있습니다. 큰 차이점은 프로세스가 아닌 물러직인 머신에 연결되는 개념입니다. 
  * `Example 1` 에 기본적인 클러스터 구성을 나타냈습니다. 그림 왼쪽에 있는 머신은 Cluster Manager 의 드라이버 노드입니다. 원은 개별 워커 노드를 실행하고 관리하는 데몬 프로세스입니다.
  * 그림에서 Spark 어플리케이션은 아직 실행되지 않았으며, 표시된 원들은 Cluster Manager 의 프로세스입니다.

> Example 1 - A cluster driver and worker (no Spark Application yet)

![image](https://user-images.githubusercontent.com/44635266/82111432-3d672780-9780-11ea-9254-5214bc6f82b3.png)

Spark 어플리케이션을 실제로 실행할 때가 되면 클러스터 매니저에 자원 할당을 요청합니다. 사용자 어플리케이션의 설정에 따라 Spark 드라이버를 실행할 자원을 포함해 요청하거나 Spark 어플리케이션 실행을 위한 익스큐터 자원을 요청할 수 있습니다.

Spark 어플리케이션의 실행 과정이나 클러스터 매니저는 어플리케이션이 실행되는 머신을 관리합니다.

Spark 가 지원하는 클러스터 매니저는 다음과 같습니다.

* Standalone Cluster Manager
* Apache Mesos
* Hadoop YARN

Spark 가 지원하는 클러스터 매니저가 늘어날 수 있습니다.

### Execution Modes

실행 모드는 어플리케이션을 실행할 때 요청한 자원의 물리적인 위치를 결정합니다. 선택할 수 있는 실행 모드는 다음과 같습니다.

* Cluster Mode
* Client Mode
* Local Mode

`Example 1` 을 기준으로 각 실행 모드를 알아보겠습니다. 실선으로 그려진 직사각형은 Spark 드라이버 프로세스를 나타내며 점선으로 그려진 직사각형은 기스큐터 프로세스를 나타냅니다.

#### Cluster Mode

흔하게 사용하는 Spark 어플리케이션 실행 방식은 클러스터 모드입니다. 클러스터 모드를 사용하려면 컴파일된 JAR 나 Python, R 스크립트를 클러스터 매니저에 전달해야 합니다.

클러스터 매니저는 파일을 받은 다음 워커 노드에 드라이버와 익스큐터 프로세스를 실행합니다. 즉, 클러스터 매니저는 모든 Spark 어플리케이션과 관련된 프로세스를 유지하는 역할을 합니다. `Example 2` 는 하나의 워커 노드에 Spark 드라이버를 할당하고 다른 워커 노드에 익스큐터를 할당하는 모습을 나타냅니다.

> Example 2 - Spark’s cluster mode

![image](https://user-images.githubusercontent.com/44635266/82111736-26293980-9782-11ea-911e-2ce025f3cef0.png)

#### Client Mode

클라이언트 모드는 어플리케이션을 제출한 클라이언트 머신에 Spark 드라이버가 위치했다는 것을 제외하면 클러스터 모드와 비슷합니다. 즉, 클라이언트 머신은 Spark 드라이버 프로세스를 유지하면 클러스터 매니저는 익스큐터 프로세스를 유지합니다. 

`Example 3` 을 보면 Spark 어플리케이션이 클러스터와 무관한 머신에서 동작하는 것을 알 수 있습니다.

보통 이런 머신을 **게이트웨이 머신(Gateway Machine)** 또는, **엣지 노드(Edge Node)** 라 부릅니다. `Example 3` 을 보면 드라이버는 클러스터 외부의 머신에 실행되며 나머지 워커는 클러스터에 위치하는 것을 알 수 있습니다.

> Example 3 - Spark’s client mode

![image](https://user-images.githubusercontent.com/44635266/82111746-34775580-9782-11ea-89e1-3d9f1782faff.png)

#### Local Mode

로컬 모드는 두 모드와 다릅니다. 로컬 모드로 설정된 경우 모든 Spark 어플리케이션은 단일 머신에서 실행됩니다. 로컬 모드는 어플리케이션의 병렬 처리를 위해 단일 머신의 스레드를 활용합니다.

이 모드는 Spark 를 학습하거나 어플리케이션 테스트 그리고 개발 중인 어플리케이션을 반복적으로 실험하는 용도로 주로 사용합니다. 그러므로 운영용 어플리케이션을 실행할 때는 로컬 모드 사용을 권장하지 않습니다.

## The Life Cycle of a Spark Application (Outside Spark)

Spark 어플리케이션을 다루는 데 필요한 용어를 알아보겠습니다. Spark 어플리케이션의 생애주기를 알아보겠습니다. `spark-submit` 을 사용해 어플리케이션을 실행하는 예제를 설명하겠습니다.

하나의 드라이버 노드와 세 개의 워커 노드로 구성된 총 네 대 규모의 클러스터가 이미 실행되고 있다고 가정하겠습니다. Spark 어플리케이션의 초기화부터 종료까지 생애주기를 알아보겠습니다.

### Client Request

첫 단계는 Spark 어플리케이션을 제출하는 겁니다. Spark 어플리케이션은 컴파일된 JAR 나 라이브러리 파일을 의미합니다. Spark 어플리케이션을 제출하는 시점에 로컬 머신에서 코드가 실행되어 클러스터 드라이버 노드에 요청합니다(`Example 4`).

이 과정에서 Spark 드라이버 프로세스의 자원을 함께 요청합니다. 클러스터 매니저는 이 요청을 받아들이고 클러스터 노드 중 하ㅏㄴ에 드라이버 프로세스를 실행합니다. Spark 잡을 제출한 클라이언트 프로세스는 종료되고 어플리케이션은 클러스터에서 실행합니다.

> Example 4 - Requesting resources for a driver

![image](https://user-images.githubusercontent.com/44635266/82111978-ecf1c900-9783-11ea-9743-2040d01cb27a.png)

Spark 어플리케이션을 제출하기 위해 터미널에서 다음과 같은 형태의 명령을 실행합니다.

```shell
./bin/spark-submit \
  --class <main-class> \
  --master <master-url> \
  --deploy-mode cluster \
  --conf <key>=<value> \
  ... # other options
  <application-jar> \
  [application-arguments]
```

### Launch

드라이버 플세스가 클러스터에 배치되었으므로 사용자 코드를 실행할 차례입니다(`Example 5`). 사용자 코드에는 반드시 Spark 클러스터를 초기화하는 SparkSession 이 포함되어야 합니다.

SparkSession 은 클러스터 매니저와 통신 Spark 익스큐터 프로세스의 실행을 요청합니다. 사용자는 `spark-submit` 을 실행할 때 사용하는 명령행 인수로 익스큐터 수와 설정값을 지정할 수 있습니다.

> Example 5 - Launching the Spark Application

![image](https://user-images.githubusercontent.com/44635266/82111983-f713c780-9783-11ea-8e1d-908953bca37f.png)

클러스터 매니저는 익스큐터 프로세스를 시작하고 결과를 응답받아 익스큐터의 위치와 관련 정보를 드라이버 프로세스로 전송합니다. 모든 작업이 정상적으로 완료되면 Spark 클러스터가 완성됩니다.

### Execution

Spark 클러스터가 생성되었으므로 `Example 6` 과 같이 코드를 실행합니다. 드라이버와 워커는 코드를 실행하고 데이터를 이동하는 과정에서 서로 통신합니다. 

드라이버는 각 워커에 태스크를 할당합니다. 태스크를 할당받은 워커는 태스크의 사태와 성공 / 실패 여부를 드라이버에 전송합니다.

> Example 6 - Application execution

![image](https://user-images.githubusercontent.com/44635266/82111986-ff6c0280-9783-11ea-8637-aa115571c4af.png)

### Completion

Spark 어플리케이션의 실행이 완료되면 드라이버 프로세스가 성공이나 실패 중 하나의 상태로 종료됩니다(`Example 7`). 그 다음 매니저는 드라이버가 속한 Spark 클러스터의 모든 익스큐터를 종료시킵니다.

이 시점에 Spark 어플리케이션의 성공 / 실패 여부는 클러스터 매니저에 요청해 확인할 수 잇습니다. 

> Example 7 - Shutting down the application

![image](https://user-images.githubusercontent.com/44635266/82111992-0abf2e00-9784-11ea-96ff-da1d5568b328.png)

## The Life Cycle of a Spark Application (Inside Spark)

클러스터 관점에서 Spark 어플리케이션의 생애 주기를 살펴봤습니다. 그러나 어플리케이션을 실행하면 Spark 내부에 어떤 일이 발생하는지 알아야 합니다. 여기서 Spark 어플리케이션을 정의하는 실제 사용자 코드와 관련된 이야기를 합니다.

Spark 어플리케이션은 하나 이상의 Spark 잡으로 구성됩니다. 스레드를 사용해 여러 액션을 병렬로 수행하는 경우가 아니라면 어플리케이션의 Spark 잡은 차례대로 실행합니다.

### The SparkSession

모든 Spark 어플리케이션은 가장 먼저 SparkSession 을 생성합니다. 여러 대화형 모드에서는 자동으로 생성되지만, 어플리케이션을 만드는 경우 직접 생성해야 합니다.

기존 코드에서는 new SparkContext 패턴을 사용했습니다. 그러나 SparkSession 의 빌더 메소드를 사용해 생성할 것을 추천합니다. 이 방식을 사용하면 Spark 와 Spark SQL 컨텍스트를 new SparkContext 패턴을 사용해 만드는 것보다 안전하게 생성할 수 있습니다.

그리고 Spark 어플리케이션에서 다수의 라이브러리가 세션을 생성하려는 상황에 컨텍스트 충돌을 방지할 수 있습니다.

```scala
// Creating a SparkSession in Scala
import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder().appName("Databricks Spark Example")
  .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
  .getOrCreate()
```

SparkSession 을 생성하면 Spark 코드를 실행할 수 있습니다. SparkSession 을 사용해 모든 저수준 API, 기존 컨텍스트 그리고 관련 설정 정보에 접근할 수 있습니다.

#### SparkContext

SparkSession 의 SparkContext 는 Spark 클러스터에 대한 연결을 나타냅니다. SparkContext 를 이용해 RDD 같은 Spark 의 저수준 API 를 사용할 수 있습니다.

Spark 과거 버전의 예제나 문서를 보면 SparkContext 는 일반적으로 `sc` 변수를 사용했습니다. SparkContext 로 RDD, 어큐뮬레이터 그리고 브로드캐스트 변수를 생성하고 코드를 실행할 수 있습니다.

대부분의 경우 SparkSession 으로 SparkContext 에 접근할 수 있으므로 명시적으로 SparkContext 를 초기화할 필요는 없습니다. 직접 초기화하는 가장 일반적인 방법은 `getOrCreate` 메소드를 사용하는 겁니다.

```scala
// in Scala
import org.apache.spark.SparkContext

val sc = SparkContext.getOrCreate()
```

SparkSession 이 초기화되었다면 코드를 실행할 차례입니다. 모든 Spark 코드는 RDD 명령으로 컴파일됩니다. 따라서 일부 논리적 명령을 알아보고 어떤 일이 발생하는지 단계별로 알아보겠습니다.

### Logical Instructions

Spark 는 트랜스포메이션과 액션으로 구성됩니다. 사용자 SQL, 저수준 RDD 처리, 머신러닝 알고리즘 등을 사용해 트랜스포메이션과 액션을 마음대로 구성할 수 있습니다.

그러므로 DataFrame 과 같은 선언적 명령을 사용하는 방법과 논리적 명령이 물리적 실행 계획으로 어떻게 변환하는지 이해하는 것은 중요합니다. 이를 기반으로 Spark 클러스터에 동작하는 방식을 이해할 수 있습니다.

#### Logical Instructions to Physical Execution

Spark 사용자 코드를 어떻게 받아들이고 클러스터에 어떻게 명령을 전달하는지 다시 한번 되짚어보겠습니다. 코드 예제를 한 줄씩 살펴보면서 그 안에서 일어나는 작업을 알아보겠습니다.

DataFrame 을 이용해 파티션을 재분배하는 잡, 값을 트랜스포메이션하는 잡, 집계 및 최종 결과를 얻어내는 잡 이렇게 세 단계의 잡을 수행합니다.

```python
# in Python
df1 = spark.range(2, 10000000, 2)
df2 = spark.range(2, 10000000, 4)
step1 = df1.repartition(5)
step12 = df2.repartition(6)
step2 = step1.selectExpr("id * 5 as id")
step3 = step2.join(step12, ["id"])
step4 = step3.selectExpr("sum(id)")

step4.collect() # 2500000000000
```

위 코드를 실행하면 액션으로 하나의 Spark 잡이 완료되는 것을 확인할 수 있습니다. 물리적 실행 계획에 대한 이해를 높이기 위해 실행 계획을 살펴보겠습니다.

실행 계획 정보는 쿼리를 실제로 수행한 다음 Spark UI 의 SQL 탭에서도 확인할 수 있습니다.

```scala
step4.explain()

== Physical Plan ==
*HashAggregate(keys=[], functions=[sum(id#15L)])
+- Exchange SinglePartition
   +- *HashAggregate(keys=[], functions=[partial_sum(id#15L)])
      +- *Project [id#15L]
         +- *SortMergeJoin [id#15L], [id#10L], Inner
            :- *Sort [id#15L ASC NULLS FIRST], false, 0
            :  +- Exchange hashpartitioning(id#15L, 200)
            :     +- *Project [(id#7L * 5) AS id#15L]
            :        +- Exchange RoundRobinPartitioning(5)
            :           +- *Range (2, 10000000, step=2, splits=8)
            +- *Sort [id#10L ASC NULLS FIRST], false, 0
               +- Exchange hashpartitioning(id#10L, 200)
                  +- Exchange RoundRobinPartitioning(6)
                     +- *Range (2, 10000000, step=4, splits=8)
```

`collect` 같은 액션을 호출하면 개별 스테이지와 태스크로 이루어진 Spark 잡이 실행됩니다. 로컬 머신에서 Spark 잡을 실행하면 localhost:4040 에 접속해 Spark UI 를 확인할 수 있습니다.

### A Spark Job

보통 액션 하나당 하나의 Spark 잡이 생성되며 액션은 항상 결과를 반환합니다. Spark 잡은 일련의 스테이지로 나뉘며 스테이지 수는 셔플 작업이 얼마나 많이 발생하는지에 따라 달라집니다.

이전 예제의 잡은 다음과 같이 나뉩니다.

* Stage 1 : Task 8
* Stage 2 : Task 8
* Stage 3 : Task 5
* Stage 4 : Task 6
* Stage 5 : Task 200
* Stage 6 : Task 1

### Stages

Spark 의 스테이지는 다수의 머신에 동일한 연산을 수행하는 태스크의 그룹을 나타냅니다. Spark 는 가능한 많은 태스크를 동일한 스테이지로 묶으려 노력합니다.

셔플 작업이 일어난 다음에는 반드시 새로운 스테이지를 시작합니다. 셔플은 데이터의 물리적 재분배 과정입니다. 예를 들어 DataFrame 정렬이나 키별로 적재된 파일 데이터를 그룹화하는 작업과 같습니다.

파티션을 재분배하는 과정은 데이터를 이동시키는 작업이므로 익스큐터 간의 조정이 필요합니다. Spark 는 셔플이 끝난 다음 새로운 스테이지를 시작하며 최종 결과를 계산하기 위해 스테이지 실행 순서를 추적합니다.

이 잡에서 두 스테이지는 DataFrame 생성을 위해 사용한 `range` 명령을 수행하는 단계입니다. `range` 명령을 사용해 DataFrame 을 생성하면 기본적으로 8 개의 파티션을 생성합니다. 다음은 파티션 재분배 단계입니다. 이 단계에서는 데이터 셔플링으로 파티션 수를 변경합니다. 두 개의 DataFrame 은 스테이지 3 과 4의 태스크 수에 해당하는 5 개, 6 개의 파티션으로 재분배됩니다.

스테이지 3 과 4 는 개별 DataFrame 에 수행됩니다. 마지막 두 스테이지는 조인을 수행합니다. 그 이유는 Spark SQL 섲렂ㅇ 때문입니다. *spark.sql.shuffle.partitions* 속성의 기본값은 200 입니다.

그러므로 Spark 잡이 실행되는 도중에 셔플을 수행하면 기본적으로 200 개의 셔플 파티션을 생성합니다. *spark.sql.shuffle.partitions* 속성을 원하는 값으로 변경할 수 있습니다. 그러면 셔플을 수행할 때 생성되는 파티션 수가 변경됩니다.

여러 요인에 의해 영향 받을 수 있지만, 경험적으로 보면 클러스터의 익스큐터 보다 파티션 수를 ㅣ정하는 것이 좋습니다. 로컬 머신에 코드를 실행하는 경우 병렬로 처리할 수 있는 태스크 수가 제한적이므로 이 값을 작게 설정해야 합니다.

이 설정은 더 많은 익스큐터 코어를 사용할 수 있는 클러스터 환경을 위한 기본값입니다. 최종 스테이지에서는 드라이버로 결과를 전송하기 전에 파티션마다 개별적으로 수행된 결과를 단일 파티션으로 모으는 작업을 수행합니다.

### Tasks

Spark 의 스테이지는 태스크로 구성됩니다. 각 태스크는 단일 익스큐터에 실행할 데이터 블록과 다수의 트랜스포메이션 조합으로 볼 수 있습니다. 만약 데이터 셋이 거대한 하나의 파티션일 경우 하나의 태스크만 생성됩니다.

만약 1,000 개의 작은 파티션으로 구성되어 있다면 1,000 개의 태스크를 만들어 병렬로 실행할 수 잇습니다. 즉, 태스크는 데이터 단위에 적용되는 연산 단위를 의미합니다. 파티션 수를 늘리면 더 높은 병렬성을 얻을 수 있습니다.

## Execution Details

Spark 의 스테이지와 태스크는 알아두면 좋은 특성을 가지고 있습니다. 첫째, Spark 는 `map` 연산 후 다른 `map` 연산이 이어진다면 함께 실행할 수 있도록 스테이지와 태스크를 자동으로 연결합니다.

둘 째 Spark 는 모든 셔플을 작업할 때 데이터를 안정적인 저장소에 저장하므로 여러 잡에서 재사용할 수 있습니다.

### Pipelining

Spark 를 인메모리 컴퓨팅 도구로 만들어주는 핵심 요소 중 하나는 맵리듀스와 같은 Spark 이전 기능과 달리 Spark 는 메모리나 디스크에 쓰기 전에 최대한 많은 단계를 수행하는 점입니다.

Spark 가 수행하는 주요 최적화 기법 중 하나는 RDD 나 RDD 보다 더 아래에서 발생하는 파이프라이닝 기법입니다. 파이프라이닝 기법은 노드 간의 데이터 이동 없이 각 노드가 데이터를 직접 공급할 수 있는 연산만 모아 태스크의 단일 스테이지로 만듭니다.

`map`, `filter`, `map` 순서로 수행되는 RDD 기반 프로그램을 개발했다면 개별 입력 레코드를 읽어 첫 번째 `map` 으로 전달한 다음 `filter` 하고 마지막 `map` 함수로 전달해 처리하는 과정을 태스크의 단일 스테이지로 만듭니다.

따라서 파이프라인으로 구성된 연산 작업은 단계별로 메모리나 디스크에 중간 결과를 기록하는 방식보다 훨씬 더 처리 속도가 빠릅니다. `select`, `filter` 그리고 `select` 를 수행하는 DataFrame 이나 SQL 연산에서도 동일한 파이프라이닝 유형이 적용됩니다.

Spark 런타임에서 파이프라이닝을 자동으로 수행하기 때문에 어플리케이션을 개발할 때는 눈에 보이지 않습니다. Spark UI 나 로그 파일로 어플리케이션을 확인해보면 다수의 RDD 또는 DataFrame 연산이 하나의 스테이지로 파이프라이닝되어 있음을 알 수 있습니다.

### Shuffle Persistence

두 번째 특성은 **셔플 결과 저장(Shuffle Persistence)** 입니다. Spark 가 `reduce-by-key` 연산 같이 노드 간 복제를 유발하는 연산을 실행하면 엔진에서 파이프라이닝을 수행하지 못하므로 네트워크 셔플이 발생합니다.

노드 간 복제를 유발하는 연산은 각 Key 에 대한 입력 데이터를 먼저 여러 노드로부터 복사합니다. 항상 데이터 전송이 필요한 소스 태스크를 먼저 수행하기 때문입니다. 그리고 소스 태스크의 스테이지가 실행되는 동안 셔플 파일을 로컬 디스크에 기록합니다.

그 다음 그룹화나 리듀스를 수행하는 스테이지가 시작됩니다. 이 스테이지에서는 셔플 파일에서 레코드를 읽어 들인 다음 연산을 수행합니다. 예를 들어 특정 범위의 키와 관련된 데이터를 읽고 처리합니다. 만약 잡이 실패한 경우 셔플 파일을 디스크에 저장했기 때문에 소스 스테이지가 아닌 해당 스테이지부터 처리할 수 있습니다. 따라서 소스 태스크를 재실행할 필요 없이 실패한 리듀스 태스크부터 다시 시작할 수 있습니다.

셔플 결과를 저장할 때 발생할 수 있는 부작용은 이미 셔플된 데이터를 이용해 새로운 잡을 실행하면 소스와 관련된 셔플이 다시 실행되지 않습니다. Spark 는 다음 스테이지를 실행하는 과정에 디스크에 이미 기록되어 있는 셔플 파일을 다시 사용할 수 있다고 판단하기 때문에 이전 스테이지를 처리하지 않습니다.

Spark UI 와 로그 파일에서 `skipped` 라 표시된 사전 셔플 스테이지를 확인할 수 있습니다. 이러한 자동 최적화 기능은 동일한 데이터를 사용해 여러 잡을 실행하는 워크로드의 시간을 절약할 수 있습니다.

그러면 사용자가 직접 캐싱을 수행할 수 있으며 정확히 어떤 데이터가 어딛에 저장되는지 제어할 수 있습니다. 집계된 데이터에 Spark 액션을 수행한 다음 Spark UI 를 확인하면 이 방식을 이해할 수 있습니다.