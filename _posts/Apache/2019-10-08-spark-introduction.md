---
title : Spark Introduction
tags :
- Apache
- Spark
---


## Spark

아파치 스파크(Apache Spark)는 오픈 소스 클러스터 컴퓨팅 프레임워크이다. Spark는 다양한 종류의 데이터 관련 문제, 예를 들어 반구조(semi-structured), 구조, 스트리밍 또는 머신 러닝/데이터 과학 관련 문제를 해결하기 위해 쉽고 빠르게 쓸 수 있는 프레임워크입니다.

Spark는 유연성과 맵리듀스에 대한 확장성을 훨씬 빠른 속도로 제공합니다. 데이터가 메모리에 저장돼 있을 때는 `Apache Hadoop`보다 100배 빠르며, 디스크에 저장돼 있을 때는 10배 빠릅니다.

또한, Spark API는 자바, 스칼라, 파이썬, R, SQL을 이용해 접근할 수 있습니다.

## Spark Architecture / Ecosystem

![스크린샷 2019-10-03 오전 5 00 57](https://user-images.githubusercontent.com/44635266/66077450-fb93c300-e59a-11e9-8a49-b86d69a19a2a.png)

### Spark SQL

* Spark Core 상단에 SchemaRDD라는 새로운 RDD 추상화가 있는 구성요소
* JDBC API를 통해 Spark DataFrame 노출 및 정형 및 반구조 데이터 지원한다.
* CSV, JSON, 시퀀스 및 Parquet 파일 형식의 데이터를 쿼리할 수 있는 DataFrame 기반 SQL과 같은 인터페이스 제공한다.

> Parquet 이란 `Hadoop` 생태계의 어느 프로젝트에서나 사용할 수 있는 효율적인 컬럼 기반 스토리지로 JSON 보다 효율적이다.

### Spark Machine Learning (MLlib)

* 분산, 확장성 및 메모리 계산을 위한 공통 기계 학습 라이브러리이다.
* `Hadoop MapReduce`의 `Apache Mahout`보다 상당히 빠른 속도를 지원한다.
* dimension reduction, clustering, classification, regression, collaborative filtering 등과 같은 공통 학습 알고리즘 지원한다.

### Spark Streaming

* 실시간에 가까운 스트리밍 데이터 처리 기능 추가할 수 있다.

### GraphX

* Spark Core 상단에 분산 그래프 처리 API 제공한다.
* Pregel 추상화 API를 통한 사용자 정의 그래프 모델링을 가능하게 한다.

> Pregel 이란 대용량 그래프 알고리즘을 처리기 위한 도구입니다.

### BlinkDB

* 대용량 데이터에 대한 대략적인 쿼리 엔진
* 대략적인 결과를 반환하는 대용량 데이터에 대해 대화형 SQL 실행할 수 있다.
* 집계된 값의 잠재적인 오류로 쿼리 실행 속도 향상
* 정확성이 필수가 아닌 데이터의 경우 유용하게 사용할 수 있다.

### Tachyon

* 메모리 내 분산 파일 시스템이다.
* 디스크 IO의 오버헤드가 없으므로 클러스터 전체에서 파일 공유 속도 향상시킬 수 있다.
* 예약 된 작업이 캐시에서 직접 공유 파일을 읽고 더 빠르게 실행할 수 있도록 메모리에서 자주 읽은 파일을 캐시합니다.
* MapReduce 및 Spark 작업을 사용한 메모리 파일 공유에 사용할 수 있다.


##  Spark Cluster Manager

Spark 는 여러 모듈로 구성되어 있지만 크게 두 부분으로 나눌 수 있다. 컴퓨터 cluster의 리소스를 관리하는 Cluster Manager와 그 위에서 동작하는 사용자 프로그램인 Spark Application으로 구분한다.

![스크린샷 2019-10-03 오전 5 21 04](https://user-images.githubusercontent.com/44635266/66078764-9db4aa80-e59d-11e9-862d-92b130d2296b.png)

Spark 애플리케이션은 주 프로그램의 `SparkContext` 객체에 의해 조정된 cluster에서 독립적인 프로세스 세트로 실행된다(`driver program`이라고도 함). SparkContext를 통해 Spark Cluster와 커뮤니케이션할 수 있기 때문입니다.

SparkContext를 통해 Application에서 요구하는 리소스를 요청하면, Spark Master는 Worker들에게 요청받은 리소스만큼의 Executor 프로세스를 실행하도록 요구합니다. 이때, cluster에서 실행하기 위해 SparkContext는 여러 유형의 클러스터 관리자(Spark의 자체 독립형 클러스터 관리자, Mesos 또는 YARN)에 연결하여 여러 애플리케이션 간에 리소스를 할당할 수 있다. 

다음으로 내부에서 사용 가능한 CPU cores 숫자도 할당받게 됩니다. 이 리소스 사이즈는 Application을 실행시킬 때 매개변수나 설정 파일로 전달할 수 있습니다. Application은 1개 이상의 Job을 실행시키고, 이 Job은 여러 개의 Task로 나누어서 Executor에게 요청하고 결과를 받으면서 Cluster 컴퓨팅 작업을 수행합니다. 연결되면 Spark는 cluster 내의 노드에서  executor를 획득하는데, 이 Executor 프로세스는 애플리케이션을 위해 계산을 실행하고 데이터를 저장하는 프로세스다.

다음으로, 당신의 어플리케이션 코드(JAR로 정의되거나 SparkContext로 전달된 Python 파일로 정의됨)를 실행자에게 보낸다. 마지막으로 SparkContext는 실행할 실행자에게 태스크를 전송한다.

> Cluster Manager Type으로는 `Standalone`, `Apache Mesos`, `Hadoop YARN`, `Kubernetes`가 있다. 써드파티 프로젝트로는  `Nomad Spark`가 있다.


###  Glossary

아래는 클러스터 개념을 나타내는데 사용되는 용어입니다.

* Application

Spark에 구축된 유저 프로그램. 클러스터의 Driver program과, executor로 구성되어 있다.

* Driver program

응용 프로그램의 main() 함수를 실행하고 SparkContext를 생성하는 프로세스
클러스터에서 리소스를 획득하기 위한 외부 서비스

* Cluster manager

Clutser에서 리소스를 획득하기 위한 외부 서비스(예: 독립 실행형 관리자, Mesos, YARN)

* Deploy mode

driver process가 실행되는 위치 구분 `cluster` 모드에서 framework는 cluster 내부에서 driver를 실행한다. `client` 모드에서 제출자는 cluster 외부에서 driver를 실행한다.

* Worker node

Cluster에서 애플리케이션 코드를 실행할 수 있는 모든 노드

* Executor

작업자 노드에서 응용 프로그램을 위해 시작된 프로세스로서, 작업을 실행하고 전체에서 데이터를 메모리 또는 Disk 저장소에 보관한다. 각 응용 프로그램에는 고유한 executor가 있다.

* Task

executor에게 보낼 작업 단위

* Job

Spark action(ex: savle, collect)에 대응하여 생성되는 여러 작업으로 구성된 병렬 계산. driver의 로그에 사용되는 이 용어를 볼 수 있다.

* Stage

각 job은 서로 의존하는 state라고 불리는 작은 일련의 task으로 나뉜다.  driver의 로그에 사용되는 이 용어를 볼 수 있다.


### References
* [Understanding Apache Spark Architecture - Back To Bazics](https://backtobazics.com/big-data/spark/understanding-apache-spark-architecture/)
