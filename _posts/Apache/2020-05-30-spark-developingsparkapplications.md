---
title : Spark Developing Spark Applications
tags :
- Cluster
- Spark
---

*이 포스트는 [Spark The Definitive Guide](https://github.com/manparvesh/bigdata-books/blob/master/Spark%20-%20The%20Definitive%20Guide%20-%20Big%20data%20processing%20made%20simple.pdf) 를 바탕으로 작성하였습니다.*

Spark 가 클러스터 환경에서 어떻게 Spark 코드를 실행하는지 알아보겠습니다.

## Writing Spark Applications

Spark 어플리케이션은 Spark 클러스터와 사용자 코드 두 가지 조합으로 구성됩니다. 이번 예제에서는 클러스터 모드를 로컬 모드로 설정하고 사전에 정의된 어플리케이션을 사용자 코드로 사용합니다. Spark 가 지원하는 언어로 Spark 어플리케이션을 보겠습니다.

### A Simple Scala-Based App

Scala 는 Spark 의 기본 언어이기 때문에 어플리케이션을 개발하는 가장 적합한 방법으로 볼 수 있습니다. 이는 일반 Scala 어플리케이션을 개발하는 방법과 크게 다르지 않습니다.

Spark 어플리케이션은 두 가지 JVM 의 빌드 도구인 sbt 나 Apache Maven 을 이용해 빌드할 수 있습니다. 이 빌드 도구는 각각 장단점을 가지지만 sbt 를 사용하는 것이 더 쉽슷ㅂ니다.

Scala 어플리케이션에 sbt 빌드 환경을 구성하려면 패키지 정보를 관리하기 위해 *build.sbt* 파일에 포함되어야 할 핵심 항목은 다음과 같습니다.

* 프로젝트 메타데이터
* 라이브러리 의존성을 관리하는 장소
* 라이브러리에 포함된 의존성 정보

다음은 Scala 용 *build.sbt* 파일 내용 중 일부입니다.

```scala
name := "example"
organization := "com.databricks"
version := "0.1-SNAPSHOT"
scalaVersion := "2.11.8"

// Spark Information
val sparkVersion = "2.2.0"

// allows us to include spark packages
resolvers += "bintray-spark-packages" at
  "https://dl.bintray.com/spark-packages/maven/"

resolvers += "Typesafe Simple Repository" at
  "http://repo.typesafe.com/typesafe/simple/maven-releases/"

resolvers += "MavenRepository" at
  "https://mvnrepository.com/"

libraryDependencies ++= Seq(
  // spark core
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
// the rest of the file is omitted for brevity
)
```

*build.sbt* 파일을 정의했으므로 프로젝트에 실제 코드를 작성해보겠습니다. sbt 는 표준 Scala 프로젝트 구조를 사용합니다.

```
src/
  main/
    resources/
       <files to include in main jar here>
    scala/
       <main Scala sources>
    java/
       <main Java sources>
  test/
    resources
       <files to include in test jar here>
    scala/
       <test Scala sources>
    java/
       <test Java sources>
```

다음은 SparkSession 을 초기화하고 어플리케이션을 실행한 다음 종료하는 예제입니다.

```scala
object DataFrameExample extends Serializable {
  def main(args: Array[String]) = {

    val pathToDataFolder = args(0)

    // start up the SparkSession
    // along with explicitly setting a given config
    val spark = SparkSession.builder().appName("Spark Example")
      .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
      .getOrCreate()

    // udf registration
    spark.udf.register("myUDF", someUDF(_:String):String)
    val df = spark.read.json(pathToDataFolder + "data.json")
    val manipulated = df.groupBy(expr("myUDF(group)")).sum().collect()
     .foreach(x => println(x))

  }
}
```

`spark-submit` 명령을 사용해 위 코드를 클러스터에 제출하겠습니다. 실행 명령 중 `main` 클래스를 확인해봐야 합니다.

프로젝트를 설정하고 코드를 작성했으니 빌드해야 합니다. 하나의 JAR 파일 안에 관련된 라이브러리를 모두 포함하는 uber-jar 나 fat-jar 로 빌드하기 위해 `sbt assemble` 명령을 사용할 수 있습니다.

이 명령은 배포 작업에서는 간단할 수 있지만 때로는 복잡한 상황이 발생할 수 있습니다.

가장 쉬운 빌드 방법은 `sbt package` 명령을 실행하는 겁니다. 이 명령을 사용해 관련 라이브러리 모두를 *target* 폴더로 모울 수 있지만 관련 라이브러리ㅡㄹㄹ 모두 가지는 하나의 거대한 JAR 파일을 만들지는 않습니다.

#### Running the Apllications

*target* 폴더에는 `spark-submit` 에 인수로 사용할 jar 파일이 있습니다. Scala 패키지를 빌드하면 다음 예제와 같이 `spark-submit` 명령을 사용해 로컬 머신에 실행할 수 있습니다.

다음 예제는 `$SPARK_HOME` 변수를 사용했습니다. `$SPARK_HOME` 은 Spark 를 설치한 디렉토리의 경로로 변경할 수 있습니다.

```shell
$SPARK_HOME/bin/spark-submit \
   --class com.databricks.example.DataFrameExample \
   --master local \
   target/scala-2.11/example_2.11-0.1-SNAPSHOT.jar "hello"
```

### Writing Python Applications

PySpark 어플리케이션을 작성하는 방법은 일반 Python 어플리케이션이나 패키지를 작성하는 방법은 거의 비슷합니다. 특히 명령행을 사용해 어플리케이션을 작성하는 방식과 매우 유사합니다. Spark 엔 빌드 개념이 없으며 PySpark 어플리케이션은 Python 스크립트에 지나지 않습니다. 그러므로 어플리케이션을 실행하려면 클러스터에 스크립트를 실행하면 됩니다.

보통 코드 재사용을 위해 여러 Python 파일을 하나의 egg 나 ZIP 파일 형태로 압축합니다. `spark-submit` 의 `--py-files` 인수로 *.py*, *.zip*, *.eggg* 파일을 지정하면 어플리케이션과 함께 배포할 수 있습니다.

코드를 실행하면 Scala 나 Java 의 메인 클래스 역할을 하는 Python 파일을 작성해야 합니다. 즉, SparkSession 을 생성하는 실행 가능한 스크립트 파일을 만들어야 합니다. 다음은 `spark-submit` 의 `main` 인수로 지정할 클래스의 코드 예제입니다.

```python
# in Python
from __future__ import print_function
if __name__ == '__main__':
    from pyspark.sql import SparkSession
    spark = SparkSession.builder \
        .master("local") \
        .appName("Word Count") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    print(spark.range(5000).where("id > 500").selectExpr("sum(id)").collect())
```

위 코드가 실행되면 어플리케이션에서 활용할 수 있는 SparkSession 객체가 생성됩니다. 모든 Python 클래스에 SparkSession 객체를 생성하는 것보다 런타임 환경에서 변수를 생성해 Python 클래스에 전달하는 방식이 좋습니다.

Python 으로 Spark 어플리케이션을 개발할 때는 PySpark 를 라이브러리 의존성으로 정의하기 위해 `pip` 를 사용할 수 있습니다.

PySpark 는 `pip install pyspark` 명령으로 설치하며, 설치 후에는 다른 Python 패키지와 같은 방식응로 의존성을 정의합니다. 이 방법을 사용하면 여러 에디터가 제공하는 코드 자동완성 기능을 사용할 수 있습니다.

#### Running the Applications

실행을 위해 코드를 클러스터에 전달해야 합니다. 아래와 같이 `spark-submit` 명령을 호출합니다.

```shell
$SPARK_HOME/bin/spark-submit --master local pyspark_template/main.py
```

### Writing Java Applications

Java 와 Scala 를 이용해 Spark 어플리케이션을 작성하는 방법은 거의 유사합니다. 가장 큰 차이점은 라이브러리 의존성을 지정하는 방법입니다.

다음 Java 어플리케이션 예제는 사용자가 메이븐을 사용해 라이브러리 의존성을 지정합니다. 메이븐은 다음과 같은 형식을 사용합니다. 메이븐을 사용하려면 Spark 패키지 저장소를 반드시 추가해야 합니다. 그래야 해당 저장소에서 Spark 와 관련된 라이브러리를 얻을 수 있습니다.

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-core_2.11</artifactId>
        <version>2.1.0</version>
    </dependency>
    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-sql_2.11</artifactId>
        <version>2.1.0</version>
    </dependency>
    <dependency>
        <groupId>graphframes</groupId>
        <artifactId>graphframes</artifactId>
        <version>0.4.0-spark2.1-s_2.11</version>
    </dependency>
</dependencies>
<repositories>
    <!-- list of other repositories -->
    <repository>
        <id>SparkPackagesRepo</id>
        <url>http://dl.bintray.com/spark-packages/maven</url>
    </repository>
</repositories>
```

디렉토리 구조는 Scala 프로젝트와 같습니다. 이제 Java 코드를 빌드하고 실행하겠습니다. Java 코드를 실행하려면 `main` 클래스가 필요합니다. 다음은 `main` 클래스 코드입니다.

```java
import org.apache.spark.sql.SparkSession;
public class SimpleExample {
    public static void main(String[] args) {
        SparkSession spark = SparkSession
                .builder()
                .getOrCreate();
        spark.range(1, 2000).count();
    }
}
```

이제 `mvn package` 명령으로 패키지를 만들 수 있습니다.

#### Running the Applications

Java 어플리케이션은 Scala 어플리케이션과 같은 방법으로 실행합니다.

```shell
$SPARK_HOME/bin/spark-submit \
   --class com.databricks.example.SimpleExample \
   --master local \
   target/spark-example-0.1-SNAPSHOT.jar "hello"
```

## Testing Spark Applications

Spark 어플리케이션을 테스트하려면 어플리케이션을 작성할 때 몇 가지 핵심 원칙과 구성 전략을 고려해야 합니다.

### Strategic Principles

데이터 파이프라인과 어플리케이션에 대한 테스트 코드 개발은 실제 어플리케이션 개발만큼이나 중요합니다.

테스트 코드는 미래에 발생할 수 있는 데이터, 로직 그리고 결과 변화에 유연하게 대처할 수 있습니다. 일반적인 Spark 어플리케이션에서 테스트해야 할 내용과 테스트 편리성을 높여주는 코드 구성을 알아보겠습니다.

#### Input Data Resilience

데이터 파이프라인은 다양한 유형의 입력 데이터에 유연하게 대처할 수 있어야 합니다. 비즈니스 요구사항이 변하면 데이터도 변합니다. 따라서 Spark 어플리케이션과 파이프라인은 입력 데이터 중 일부가 변하더라도 유연하게 대처할 수 있습니다. 아니면 오류 상황을 적절하고 유연하게 제어할 수 있습니다.

따라서 입력 데이터로 인해 발생할 수 있는 다양한 예외 상황을 테스트하는 코드를 작성해야 합니다. 그러면 심각한 문제가 발생했을 때만 저녁잠을 깨우는 견고한 어플리케이션을 만들 수 있습니다.

#### Business Logic Resilience and Evolution

입력 데이터뿐만 아니라 파이프라인 내부의 비즈니소 로직이 바뀔 수도 있습니다. 예상했던 원형 데이터의 형태가 실제 원형 데이터와 같은지 확인하고 싶을겁니다. 이는 원하는 결과를 얻을 수 있도록 실제 유사한 데이터를 사용해 비즈니스 로직을 꼼꼼하게 테스트해야합니다.

이 유형의 데스트에선 Spark 가 가진 기능을 테스트하는 Spark 단위 테스트를 작성하지 않도록 조심해야 합니다. 대신 비즈니스 로직을 테스트해 복잡한 비즈니스 파이프라인이 의도한 대로 동작하는지 반드시 확인해야 합니다.

#### Resilience in Output and Atomicity

입력 데이터 및 비즈니스 로직의 테스트가 완료된다면 결과를 의도한 대로 반환하는지 확인해야 합니다. 즉, 결과 데이터가 스키마에 맞는 적절한 형태로 반환될 수 있도록 제어해야 합니다.

단순히 데이터를 특정 경로에 저장해 놓고 전혀 사용하지 않는 경우는 없습니다. 즉, 대부분의 Spark 파이프라인에 데이터의 상태, 즉 데이터가 얼마나 자주 갱신되는지 데이터가 완벽한지, 마지막 순간에 데이터가 변경되지는 않았는지 등을 이해할 수 있도록 만듭니다.

앞서 언급한 주제는 데이터 파이프라인을 구성할 때 고려해야 하는 원칙입니다. 

### Tactical Takeaways

전략적 사고도 중요하지만 어플리케이션 테스트를 쉽게 만들어주는 테스트 구성 전략에 대해 자세히 알아보겠습니다. 적절한 단위 테스트를 작성해 입력 데이터나 구조가 변경되어도 비즈니스 로직이 정상적으로 동작하는지 확인해야 합니다.

단위 테스트를 하면 스키마가 변경되는 상황에 쉽게 대응할 수 있습니다. 단위 테스트의 구성 방법은 비즈니스 도메인과 도메인 경험에 따라 다양할 수 있으므로 개발자 역량에 달려있습니다.

#### Managing SparkSession

Spark 로컬 모드 덕분에 JUnit 이나 ScalaTest 같은 단위 테스트용 프레임워크로 비교적 쉽게 Spark 코드를 테스트할 수 있습니다. 단위 테스트 하네스의 일부로 로컬 모드의 SparkSession 을 만들어 사용하면 됩니다.

이 텟트 방식이 잘 동작하려면 Spark 코드에 의존성 주입 방식으로 SparkSession 을 관리하도록 만들어야 합니다. 즉, SparkSesion 을 한 번만 초기화하고 런타임 환경에서 함수와 클래스에 전달하는 방식을 사용하면 테스트 중에 SparkSession 을 쉽게 교체할 수 있습니다.

이 방법을 사용하면 단위 테스트를 수행할 때 테스트용 SparkSession 으로 개별 함수를 쉽게 테스트할 수 있습니다.

#### Which Spark API to Use

Spark 는 SQL, DataFrame, Dataset 등 다양한 API 를 제공합니다. 각 API 는 사용자 어플리케이션의 유지 보수성과 테스트 용이성 측면에 서로 다른 영향을 미칠 수 있습니다. 적합한 API 는 사용자가 속한 팀과 팀에서 무엇을 필요로 하는지에 따라 달라질 수 있습니다.

어떤 팀이나 프로젝트에선 개발 속도를 올리기 위해 덜 엄격한 SQL 과 DataFrame API 를 사용할 수 있고 다른 팀에서는 타입 안정성을 얻기 위해 Dataset 과 RDD API 를 사용할 수 있습니다.

API 유형에 상관없이 각 함수의 입력과 출력 타입을 문서로 만들고 테스트해야 합니다. 타입 안정성 API 를 사용하면 함수가 가지는 최소한의 규약을 지켜야 하므로 다른 코드에서 재사용하기 쉽습니다. 모든 동적 데이터 타입 언어가 그렇듯 DataFrame 이나 SQL 을 사용할 때는 혼란을 없애기 위해 각 함수의 입력 타입과 출력 타입을 문서로 만들고 테스트하는 노력이 필요합니다.

저수준 RDD API 는 정적 데이터 타입을 사용하지만 Dataset API 에는 없는 파티셔닝 같은 저수준 API 의 기능이 필요한 경우에만 사용합니다. Dataset API 를 사용하면 성능을 최적화할 수 있으며 앞으로 더 많은 성능 최적화 방식을 제공할 가능성이 높습니다.

어플리케이션에 사용할 언어를 선택할 때도 비슷한 고려사항이 적용됩니다. 

### Connecting to Unit Testing Frameworks

코드를 단위 테스트하려면 각 언어의 표준 프레임워크를 사용하고 테스트 하네스에는 테스트마다 SparkSession 을 생성하고 제거하도록 설정하는 것이 좋습니다. 각 프레임 워크는 SparkSession 생성과 제거를 수행할 수 있는 메커니즘을 제공합니다. 

### Connecting to Data Sources

가능하면 테스트 코드에서 운영 환경의 데이터소스에 접속하지 말아야 합니다. 그래야 데이터소스가 변경되더라도 고립된 환경에서 개발자가 쉽게 테스트 코드를 실행할 수 있습니다. 이 환경을 구성하는 방법의 하나로 비즈니스 로직을 가진 함수가 데이터소스에 직접 접근하지 않고 DataFrame 이나 Dataset 을 넘겨받을 수 있습니다.

이렇게 생성된 함수를 재사용하는 코드는 데이터소스의 종류에 상관없이 같은 방식으로 동작합니다. Spark 의 구조적 API 를 사용하는 경우 이름이 지정된 테이블을 이용해 문제를 해결할 수 있습니다. 간단히 몇 개의 더미 데이터셋에 이름을 붙여 테이블로 등록하고 사용할 수 있습니다.

## The Development Process

Spark 어플리케이션 개발 프로세스는 기존 개발 프로세스와 유사합니다.

로컬 머신에서 실행한다면 `spark-shell` 과 Spark 가 지원하는 다른 언어용 쉘을 사용해 어플리케이션 개발에 활용하는 것이 가장 적합한 방식입니다. 대부분의 쉘은 대화형 어플리케이션을 개발할 때 사용하지만 `spark-submit` 명령은 Spark 클러스터에 운영용 어플리케이션을 실행할 때 사용합니다.

이 모드로 실행할 수 있는 쉘에는 PySpark, Spark SQL, SparkR 이 있습니다.

어플리케이션을 개발하고 실행할 패키지나 스크립트를 만들고 나면 `spark-submit` 명령으로 클러스터에 제출할 수 있습니다.

## Launching Applications

대부분의 Spark 어플리케이션은 `spark-submit` 명령으로 실행합니다. `spark-submit` 은 옵션, 어플리케이션 JAR 파일이나 스크립트와 관련된 인수를 지정해 사용합니다.

```shell
./bin/spark-submit \
  --class <main-class> \
  --master <master-url> \
  --deploy-mode <deploy-mode> \
  --conf <key>=<value> \
  ... # other options
  <application-jar-or-script> \
  [application-arguments]
```

`spark-submit` 명령으로 Spark 잡을 제출할 때는 클라이언트 모드와 클러스터 모드 중 하나를 선택해야 합니다. 하지만 드라이버와 익스큐터 간의 지연 시간을 줄이기 위해 클러스터 모드로 실행할 것을 추천합니다.

Python 어플리케이션을 제출하라면 *.jar* 파일의 위치에 *.py* 파일을 지정하고 *.zip*, *.egg*, *.py* 파일을 `--py-files` 에 추가합니다.

아래 표는 특정 클러스터 매니저에서 사용할 수 있는 옵션을 포함해 `spark-submit` 명령에서 사용할 수 있는 모든 옵션 정보를 제공합니다. `spark-submit --help` 명령을 실행하면 전체 옵션을 직접 확인할 수 있습니다.

|Parameter|Description|
|:--|:--|
|`--master MASTER_URL`|spark://host:port, mesos://host:port, yarn 또는 local 을 지정합니다.|
|`--deploy-mode DEPLOY_MODE`|드라이버 프로그램을 로컬에서 실행할 지 워커 머신 중 하나에서 실행할지 지정합니다. 기본값은 client dlqslek.|
|`--class CLASS_NAME`|사용자 어플리케이션의 메인 클래스를 지정합니다.|
|`--name NAME`|어플리케이션의 이름을 지정합니다.|
|`--jars JARS`|드라이버와 익스큐터이 클래스패스에 포함될 로컬 JAR 파일을 콤마로 구분된 목록으로 지정합니다.|
|`--packages`|드라이버와 익스큐터의 클래스패스에 포함될 메이븐 의존성 정보를 콤마로 구분된 목록으로 지정합니다. 로컬 저장소를 먼저 검색하고 해당 의존성 라이브러리가 없는 경우 메이븐 중앙 저장소나 `--repositories` 에 명시된 원격 저장소를 검사합니다. groupId:artifactId:version 포맷으로 표기합니다.|
|`--exclude-packages`|`--packages` 에 명시된 의존성 라이브러리 중에서 충돌 방지를 위해 제외해야 하는 목록을 콤마로 구분된 목록으로 지정합니다.|
|`--repositories`|`--packages` 에 지정된 의존성 라이브러리를 검색할 때 사용할 원격 메이븐 저장소를 콤마로 구분된 목록으로 지정합니다.|
|`--py-files PY_FILES`|Python 어플리케이션 실행 시 PYTONPATH 에 추가할 *.zip*, *.egg*, *.py* 파일을 지정합니다.|
|`--files FILES`|각 익스큐터의 작업 디렉토리에 위치할 파일을 콤마로 구분된 목록으로 지정합니다.|
|`--conf PROP=VALUE`|임의의 Spark 환경 설정 속성값을 지정합니다.|
|`--properties-file FILE`|부가적인 속성 정보를 읽어 들일 파일의 경로를 지정합니다. 지정하지 않으면 *conf/spark-defaults.conf* 파일을 참조합니다.|
|`--driver-memory MEM`|드라이버에서 사용할 메모리를 지정합니다. 기본값은 1024 MB 입니다.|
|`--driver-java-options`|드라이버에서 지정할 부가적인 Java 옵션 정보를 지정합니다.|
|`--driver-library-path`|드라이버에 지정할 부가적인 라이브러리 경로를 지정합니다.|
|`--driver-class-path`|드라이버에 지정할 부가적인 클래스패스를 지정합니다. `--jars` 에 지정한 JAR 파일은 자동으로 클래스패스에 추가됩니다.|
|`--executor-memory MEM`|각 익스큐터에서 사용할 메모리를 지정합니다. 기본값은 1 GB 입니다.|
|`--proxy-user NAME`|어플리케이션을 제출할 때 위장용으로 사용할 사용자 이름을 지정합니다. 이 인수는 `--principal` / `--keytab` 인수와 함께 사용할 수 없습니다.|
|`--help`, `-h`|도움말을 출력합니다.|
|`--verbose`, `-v`|추가적인 디버그 메세지를 함께 출력합니다.|
|`--version`|사용중인 Spark 버전을 출력합니다.|

특정 배포 환경에서 사용할 수 있는 설정은 아래 표에있습니다.

|Cluster Managers|Modes|Conf|Description|
|:--|:--|:--|:--|
|Standalone|Cluster|`--driver-cores NUM`|드라이버에서 사용할 코어 수를 지정합니다. 기본값은 1 입니다.|
|Standalone/Mesos|Clstuer|`--supervise`|이 옵션을 지정하면 드라이버 실패 시 재시작합니다.|
|Standalone/Mesos|Cluster|`kill SUBMISSION_ID`|지정한 드라이버를 강제 종료합니다.|
|Standalone/Mesos|Cluster|`--status SUBMISSION_ID`|지정한 드라이버의 상태를 조회합니다.|
|Standalone/Mesos|Either|`--total-executor-cores NUM`|전체 익스큐터가 사용할 총 코어 수를 지정합니다.|
|Standalone/YARN|Either|`--executor-cores NUM1`|익스큐터별로 사용할 코어 수를 지정합니다. YARN 모드에서 기본 값은 1 입니다. 스탠드 얼론 모드에서는 사용 가능한 전체 워커의 코어 수를 기본값으로 사용합니다.|
|YARN|Either|`--driver-cores NUM`|드라이버에서 사용할 코어 수를 지정합니다. 클러스터 모드에서만 사용 가능하며 기본값은 1 입니다.|
|YARN|Either|`queue QUEUE_NAME`|잡을 제출할 YARN 의 큐 이름을 지정합니다. 기본값은 default 입니다.|
|YARN|Either|`--num-executors NUM`|실행할 익스큐터 수를 지정합니다. 기본값은 2 입니다. 동적 할당 옵션이 활성화 되어 있으면 초기 익스큐터 수는 NUM 에 지정된 수 이상으로 생성됩니다.|
|YARN|Either|`--archives ARCHIVES`|각 익스큐터의 작업 디렉토리에 압축을 해제할 아카이브의 목록을 콤마로 구분하여 지정합니다.|
|YARN|Either|`--principal PRINCIPAL`|보안이 활성화된 HDFS 를 사용하는 경우 KDC 에 로그인할 때 사용할 보안 주체를 지정합니다.|
|YARN|Either|`--keytab KEYTAB`|보안 주체에 대한 keytab 파일이 저장된 전체 경로를 지정합니다. keytab 파일은 주기적으로 로그인 티켓과 위임 토큰을 갱신해 보안통신 분산 캐시를 통해 어플리케이션 마스터를 실행하는 노드로 복사합니다.|

### Application Launch Examples

특정 파라미터를 어떻게 사용해야 할지 막막하다면 다음과 같이 로컬 머신에서 SparkPi 클래스를 메인 클래스로 사용해 테스트할 수 있습니다.

```shell
./bin/spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master spark://207.184.161.138:7077 \
  --executor-memory 20G \
  --total-executor-cores 100 \
  replace/with/path/to/examples.jar \
  1000
```

Python 에는 다음 코드를 이용해 위와 같은 작업을 수행합니다. Spark 디렉토리에서 명령을 실행하면 스탠드얼론 클러스터 매니저로 Python 어플리케이션을 제출합니다. 또한 위 예제와 동일한 수의 익스큐터를 사용하도록 제한할 수 있습니다.

```shell
./bin/spark-submit \
  --master spark://207.184.161.138:7077 \
  examples/src/main/python/pi.py \
  1000
```

`master` 옵션의 값을 `local` 이나 `local[*]` 로 변경하면 어플리케이션을 로컬 모드로 실행할 수 있습니다. 그리고 *replace/with/path/to/examples.jar* 파일을 로컬에서 사용 중인 Scala 와 Spark 버전에 맞게 컴파일한 파일로 바꿔야 할 수도 있습니다.

## Configuring Applications

Spark 는 다양한 환경 설정을 제공합니다. 대부분의 설정은 다음과 같이 분류할 수 있습니다.

* Application properties
* Runtime environment
* Shuffle behavior
* Spark UI
* Compression and serialization
* Memory management
* Execution behavior
* Networking
* Scheduling
* Dynamic allocation
* Security
* Encryption
* Spark SQL
* Spark streaming
* SparkR

Spark 에서는 다음과 같은 방식으로 시스템을 설정할 수 있습니다.

* Spark 는 대부분의 어플리케이션 파라미터를 제어하며 SparkConf 객체를 사용해 Spark 속성을 설정할 수 있습니다.
* Java 시스템 속성
* 하드코딩된 환경 설정 파일

Spark 의 */conf* 디렉토리에 사용 가능한 여러 종류의 템플릿 파일을 찾아볼 수 있습니다. 어플리케이션을 개발할 때 템플릿의 설정값을 하드코딩할 수 있으며 템플릿에 속성 값을 지정해 런타임에 사용할 수도 있습니다.

### The SparkConf

SparkConf 는 어플리케이션의 모든 설정을 관리합니다. 아래 예제처럼 `import` 구문을 지정하고 객체를 생성할 수 있습니다. Spark 어플리케이션에 생성된 SparkConf 객체는 불변성입니다.

```scala
// in Scala
import org.apache.spark.SparkConf

val conf = new SparkConf().setMaster("local[2]").setAppName("DefinitiveGuide")
  .set("some.conf", "to.some.value")
```

SparkConf 객체는 개별 Spark 어플리케이션에 대한 Spark 속성값을 구성하는 용도로 사용합니다. Spark 속성값은 Spark 어플리케이션의 동작 방식과 클러스터 구성 방식을 제어합니다. 위 예제에서는 로컬 클러스터에 2 개의 스레드를 생성하도록 설정하고 Spark UI 에 표시할 어플리케이션 이름을 지정합니다.

이런 설정 값은 명령행 인수를 통해 런타임에 구성할 수 있습니다. 자동으로 기본 Spark 어플리케이션을 포함하는 Spark 쉘을 시작할 때 도움이 됩니다. 예를 들면 아래와 같습니다.

```shell
./bin/spark-submit --name "DefinitiveGuide" --master local[4] ...
```

시간 주기 형태의 속성값을 정의할 때는 다음 포맷을 사용합니다.

* 25ms (milliseconds)
* 5s (seconds)
* 10m or 10min (minutes)
* 3h (hours)
* 5d (days)
* 1y (years)

### Application Properties

어플리케이션 속성은 `spark-submit` 명령이나 Spark 어플리케이션을 개발할 때 설정할 수 있습니다. 어플리케이션의 속성은 기본 어플리케이션 메타데이터와 일부 실행 특성을 정의합니다. 아래 표에 현재 지원하는 어플리케이션 속성 목록을 나타냈습니다.

|Property name|Default|Meaning|
|:--|:--|:--|
|`spark.app.name`|(none)|사용자 어플리케이션의 이름을 지정합니다. 이 이름은 Spark UI 와 로그데이터에서 확인할 수 있습니다.|
|`spark.driver.cores`|1|드라이버 프로세스에서 사용할 코어 수를 지정합니다. 단 클러스터 모드에서만 사용 가능합니다.|
|`spark.driver.maxResultSize`|1g|Spark 액션에 대한 직렬화된 결과의 최대 크기, 최솟값은 1 M 이며 0 으로 설정하는 경우 무제한입니다. 총 결과 크기가 이 제한을 넘어가는 경우에는 잡을 종료합니다. 너무 큰 값으로 지정하면 드라이버에서 OutOfMemoryError 가 발생할 수 있습니다.|
|`spark.driver.memory`|1g|SparkContext 가 초기화되는 드라이버 프로세스에서 사용할 총 메모리의 크기를 지정합니다. client 모드에서 이 설정을 적용하려면 해당 시점에 이미 드라이버 JVM 이 실행되고 있기 때문에 어플리케이션 구현 시 SparkConf 에 직접 설정해야 합니다. 또한 명령행의 `--driver-memory` 옵션이나 기본 속성 파일에 지정할 수 있습니다.|
|`spark.executor.memory`|1g|각 익스큐터 프로세스에 사용할 메모리의 크기를 지정합니다.|
|`spark.extraListeners`|(none)|SparkListener 를 상속받아 구현한 클래스를 콤마로 구분된 목록으로 지정합니다. SparkContext 초기화 시점에 이 클래스의 인스턴스가 생성되어 Spark 의 Listener Bus 에 등록됩니다.|
|`spark.logConf`|FALSE|SparkContext 가 시작될 때 SparkConf 에 포함된 정보를 INFO 로그로 출력합니다.|
|`spark.master`|(none)|연결할 클러스터 매니저를 지정합니다. `--master` 속성으로 사용 가능한 `master URL` 을 확인할 수 있습니다.|
|`spark.submit.deployMode`|(none)|Spark 드라이버 프로그램의 배포 모드를 지정합니다. `client`, `cluster` 를 사용할 수 있습니다.|
|`spark.log.callerContext`|(none)|YARN/HDFS 환경에 실행할 때 YARN RM 로그나 HDFS 감사 로그에 기록할 어플리케이션 정보를 지정합니다. 이 설정값의 길이는 Hadoop 설정인 `hadoop.caller.context.max.size` 의 설정값에 따라 달라집니다.|
|`spark.driver.supervise`|FALSE|값이 true 인 경우 종료 상태가 0 이 아니면 자동으로 드라이버를 재시작합니다. Spark 스탠드얼론 모드나 메소스 클러스터 모드에서만 사용할 수 있습니다.|

드라이버가 실행된 호스트의 4040 포트로 접속하면 Spark UI 에서 확인할 수 있습니다.

### Runtime Properties

어플리케이션의 런타임 환경을 설정해야 할 수도 있습니다. 드라이버와 익스큐터를 위한 추가 클래스패스와 로그 관련 속성을 정의할 수 있습니다. [Documentation](http://spark.apache.org/docs/latest/configuration.html#runtime-environment) 에서 확인할 수 있습니다.

### Execution Properties

실행 속성과 관련된 설정값은 실제 처리를 더욱 세밀하게 제어할 수 있습니다. 대표적인 속성으로는 `spark.executor.cores` 랑 `spark.files.maxPartitionBytes` 가 있습니다. [Documentation](http://spark.apache.org/docs/latest/configuration.html#execution-behavior) 에서 다른 속성을 확인할 수 있습니다.

### Configuring Memory Management

사용자 어플리케이션을 최적화할 때 메모리 옵션을 수동으로 관리할 때 사용합니다. [Documentation](http://spark.apache.org/docs/latest/configuration.html#memory-management) 에서 다른 속성을 확인할 수 있습니다.

### Configuring Shuffle Behavior

과도한 네트워크 부하 때문에 Spark 잡에서 셔플이 큰 병목 구간이 될 수 있습니다. 이 셔플 동작 방식을 제어하기 위한 고급 설정이 존재합니다. [Documentation](http://spark.apache.org/docs/latest/configuration.html#shuffle-behavior) 을 참고하시면됩니다.

### Environmental Variables

Spark 가 설치된 디렉토리의 *conf/spark-env.sh* 파일에 읽은 환경변수로 특정 Spark 설정을 구성할 수 있습니다. 스탠드얼론과 메소스 모드에서는 이 파일로 머신에 특화된 정보를 제공할 수 있습니다. 또한 이 파일은 로컬 어플리케이션이나 제출용 스크립트를 실행할 때 함께 적용됩니다.

Spark 를 설치한다고 해서 *conf/spark-env.sh* 파일이 기본적으로 존재하는 것은 아닙니다. 하지만 *conf/spark-env.sh.template* 파일을 복사해 생성할 수 있습니다.

*spark-env.sh* 스크립트에 다음과 같은 변수를 설정할 수 있습니다.

* `JAVA_HOME`
  * Java 가 설치된 경로를 지정합니다.
* `PYSPARK_PYTHON`
  * PySpark 의 드라이버와 워커 모두에 사용할 Python 바이너리 파일을 지정합니다.
  * *spark.pyspark.python* 속성은 PYSPARK_PYTHON 보다 우선권을 가집니다.
* `PYSPARK_DRIVER_PYTHON`
  * 드라이버에서 PySpark 를 사용하기 위해 실행 가능한 Python 바이너리를 지정합니다. 기본값은 PYSPARK_PYTHON 입니다. *spark.pyspark.driver.python* 속성은 PYSPARK_DRIVER_PYTHON 보다 우선권을 가집니다.
* `SPARKR_DRIVER_R`
  * SparkR 쉘에서 사용할 R 바이너리 실행 명령을 지정합니다. 기본값은 R 입니다. *spark.r.shell.command* 속성은 SPARKR_DRIVER_R 보다 우선권을 가집니다.
* `SPARK_LOCAL_IP`
  * 머신의 IP 주소를 지정합니다.
* `SPARK_PUBLIC_DNS`
  * Spark 프로그램이 다른 머신에 알려줄 호스트명입니다.

나열된 목록 외에도 각 머신이 사용할 코어 수나 최대 메모리 크기 같은 Spark 스탠드얼론 클러스터 설정과 관련된 옵션도 있습니다. *spark-env.sh* 파일은 쉘 스크립트이므로 프로그래밍 방식으로 일부 값을 설정할 수 있습니다. 예를 들어 특정 네트워크 인터페이스의 IP 를 찾아 `SPARK_LOCAL_IP` 변수의 값을 설정할 수 있습니다.

### Job Scheduling Within an Application

Spark 어플리케이션에서 별도의 스레드를 이용해 여러 잡을 동시에 실행할 수 있습니다. 이 절에서 잡은 해당 액션을 수행하기 위해 실행되어야 할 모든 태스크와 Spark 액션을 의미합니다. Spark 스케줄러는 스레드 안정성을 충분히 보장합니다. 그리고 여러 요청을 동시에 처리할 수 있는 어플리케이션을 만들 수 있습니다.

기본적으로 Spark 의 스케줄러는 FIFO 방식으로 동작합니다. 큐의 전단에 있는 잡이 클러스터의 전체 자원을 사용하지 않으면 이후 잡을 바로 실행할 수 있습니다. 하지만 큐의 전단에 있는 잡이 너무 크면 이후 잡은 늦게 실행될 겁니다.

여러 Spark 잡이 자원을 공평하게 나눠 쓰도록 구성할 수 있습니다. Spark 는 모든 잡이 클러스터 자원을 거의 동일하게 사용할 수 있도록 **라운드-로빈(Round-Robin)** 방식으로 여러 Spark 잡의 태스크를 할당합니다. 즉, 장시간 수행되는 Spark 잡이 처리되는 중에 짧게 끝난 Spark 잡이 제출된 경우 즉시 장시간 수행하는 Spark 잡의 자원을 할당받아 처리합니다. 따라서 장시간 수행되는 Spark 잡의 종료를 기다리지 않고 빠르게 응답할 수 있습니다. 이 모드는 사용자가 많은 환경에 가장 적합합니다.

**페어 스케줄러(Fair Scheduler)** 를 사용하려면 SparkContext 를 설정할 때 *spark.scheduler.mode* 속성을 FAIR 로 지정해야 합니다.

페어 스케줄러는 여러 개의 잡을 풀로 그룹화하는 방식도 지원합니다. 그리고 개별 풀에 다른 스케줄링 옵션이나 가중치를 설정할 수 있습니다. 페어 스케줄러를 사용하면 더 중요한 Spark 잡을 할당할 수 있도록 우선순위가 높은 풀을 만들 수 있습니다. 또한 각 잡에 같은 양의 자원을 할당하는 대신 각 잡에 같은 양의 자원을 할당하는 대신 각 사용자의 Spark 잡을 그룹화할 수도 있습니다. 동시에 실행하는 잡수를 고려하지 않고 모든 사용자가 같은 양의 자원을 사용하도록 설정하면 됩니다. Spark 의 페어 스케줄러는 Hadoop 의 페어 스케줄러 모델을 본떠서 만들었습니다.

사용자가 명시적으로 풀을 지정하지 않으면 Spark 는 새로운 잡을 default 풀에 할당합니다. 잡을 제출하는 스레드에서 SparkContext 의 로컬 속성인 *spark.scheduler.pool* 속성을 설정해 풀을 지정할 수 있습니다. sc 가 SparkContext 에 변수라 가정하면 다음과 같이 지정합니다.

```scala
sc.setLocalProperty("spark.scheduler.pool", "pool1")
```

이 로컬 속성을 지정하면 이 스레드에서 제출하는 모든 잡은 이 풀을 사용합니다. 이 설정은 사용자를 대신해 스레드가 여러 잡을 쉽게 실행할 수 있도록 스레드별로 지정할 수 있습니다. 스레드에 연결된 풀을 초기화하고 싶다면 *spark.scheduler.pool* 속성의 값을 null 로 지정합니다.


