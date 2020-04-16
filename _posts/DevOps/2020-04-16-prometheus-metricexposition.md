---
title : Prometheus Metric Exposition
tags :
- Parser
- Bridge
- Metric
- Pushgateway
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

Prometheus 가 메트릭을 이용할 수 있게 만드는 과정을 메트릭 **게시(Exposition)** 이라 합니다.

Prometheus 에 메트릭 게시는 HTTP 를 통해 수행됩니다. 일반적으로 메트릭은 `/metrics` 경로에 표시되며, 이러한 요청은 클라이언트 라이브러리에 의해 처리됩니다. Prometheus 는 가독성 높은 텍스트 형식을 사용하기 때문에 메트릭이 표시되는 형식도 수동으로 지정할 수 있습니다.

메트릭 게시는 주로 메인 함수나 최상위 수준의 함수에서 구현되며 어플리케이션당 한 번만 구성하면 됩니다.

메트릭은 해당 메트릭이 정의되는 시점에 기본 레지스트리와 함께 등록됩니다. 참조 라이브러리 중 하나가 Prometheus 계측을 지원하는 경우, 메트릭은 자동으로 기본 레지스트리에 포함되고 추가적인 계측 정보도 얻을 수 있습니다.

일부 사용자는 메인 함수에서 레지스트리를 명시적으로 전달하는 것을 선호하기 때문에 사용자는 어플리케이션의 메인 함수와 계측을 감지하는 Prometheus 계측 사이의 모든 라이브러리에 의존해야 합니다. 이는 의존성 체인 내의 모든 라이브러리가 계측에 관련되고 계측 라이브러리를 선택하는 데 합의했음을 가정합니다. 이와 같은 설계로 메트릭 게시와는 별개로 Prometheus 메트릭을 계측할 수 있습니다.

널리 사용되는 몇 가지 클라이언트 라이브러리에서 메트릭 게시를 구현한 방법을 살펴보겠습니다.

## Python

아래 함수는 Prometheus 메트릭을 제공하는 HTTP 서버를 백그라운드 스레드로 동작시킵니다.

```python
from prometheus_client import start_http_server

if __name__ == '__main__':
    start_http_server(8000)
    # Your code goes here.
```

`start_http_server` 는 구동과 실행이 매우 빠르고 쉽습니다. 하지만 어플리케이션에는 메트릭을 제공하기 위한 HTTP 서버가 이미 있을 수 있습니다.

Python 에서는 어떤 프레임워크를 사용하느냐에 따라 다양한 방법으로 메트릭을 표시합니다.

### WSGI

WSGI(Web Server Gateway Interface, 웹 서버 게이트웨이 인터페이스) 는 웹 어플리케이션에 대한 Python 표준입니다. Python 클라이언트는 WSGI 코드를 사용할 수 있는 WSGI 어플리케이션을 제공합니다.

아래 예제를 보면 `/metrics` 경로에 대한 요청이 들어올 때 `my_app` 은 `metrics_app` 에 그 역할을 위임합니다. 그렇지 않은 경우 `my_app` 의 일반적인 로직을 수행합니다.

```python
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello World']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    httpd.serve_forever()
```

### Twisted

**트위스티드(Twisted)** 는 Python 의 이벤트 기반 네트워크 엔진으로 WSGI 를 지원하기 때문에 아래 예제처럼 `make_wsgi_app` 과 연결할 수 있습니다.

```python
from prometheus_client import make_wsgi_app
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.web.resource import Resource
from twisted.internet import reactor

metrics_resource = WSGIResource(
        reactor, reactor.getThreadPool(), make_wsgi_app())

class HelloWorld(Resource):
      isLeaf = False
      def render_GET(self, request):
          return b"Hello World"

root = HelloWorld()
root.putChild(b'metrics', metrics_resource)

reactor.listenTCP(8000, Site(root))
reactor.run()
```

### Multiprocess with Gunicorn

Prometheus 는 모니터링 대상 어플리케이션이 장시간 동작하는 멀티스레드라고 가정합니다. 하지만, CPython 은 **전역 인터프리터 락(Global Interpreter Lock)** 을 사용해 하나의 프로세서 코어로만 효율적으로 동작하도록 제한합니다. 이러한 문제를 해결하고자 **구니콘(Gunicorn)** 같은 도구를 사용해 여러 개의 프로세스를 수행해 작업 부하를 분산시키는 방법을 쓰기도 합니다.

일반적인 Python 클라이언트 라이브러리를 사용하면, 각 **워커(Worker)** 는 자체적으로 메트릭을 추적합니다. Prometheus 는 어플리케이션에서 데이터를 수집할 때 마다 다수의 워커 중 하나에서만 임의로 메트릭을 가져오게 될 수도 있습니다. 이렇게 되면 알고자 하는 정보의 파편만을 가져올 수 있고, 역행하는 카운터 같은 문제점을 발생시키며, 워커의 수명이 상대적으로 짧을 수 있습니다.

Python 클라이언트가 유발하는 이 해결책은 각 워커가 자신의 메트릭을 추적하는겁니다. 그리고 메트릭 게시 시점에 모든 워커의 모든 메트릭을 결합해 멀티스레드 어플리케이션에서 알기 원하는 유의미한 정보를 도출하면 됩니다.

이 방법에는 몇 가지 제약이 있습니다. `process_` 계열 메트릭이나 사용자 정의 수집기는 표시되지 않으며, **푸쉬게이트웨이(PushGateway)** 에는 사용할 수 없습니다.

구니콘을 사용하는 경우, 아래 예제와 같은 구성 파일을 작성해 클라이언트 라이브러리가 각 워커의 종료 시점을 알 수 있게 해야합니다.

```python
from prometheus_client import multiprocess

def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)
```

멀티프로세스 메트릭을 제공하는 어플리케이션도 필요할 수 있는데, 구니콘은 WSGI 를 사용하기 때문에 `make_wsgi_app` 를 사용해 어플리케이션을 생성할 수 있습니다. 멀티 프로세스 메트릭과 기본 레지스트리에 정의된 로컬 메트릭을 구분하기 위해서는 반드시 메트릭 게시를 위한 MultiProcessCollector 만 포함하는 **사용자 지정 레지스트리(Custom Registry)** 를 만들어야합니다.

```python
from prometheus_client import multiprocess, make_wsgi_app, CollectorRegistry
from prometheus_client import Counter, Gauge

REQUESTS = Counter("http_requests_total", "HTTP requests")
IN_PROGRESS = Gauge("http_requests_inprogress", "Inprogress HTTP requests",
        multiprocess_mode='livesum')

@IN_PROGRESS.track_inprogress()
def app(environ, start_fn):
    REQUESTS.inc()
    if environ['PATH_INFO'] == '/metrics':
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        metrics_app = make_wsgi_app(registry)
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello World']
```

위 예제를 보면 서머리와 히스토그램철머 카운터들은 정상적으로 동작합니다. 게이지는 사용 의도에 따라 다음과 같이 추가적인 `multiprocess_mode` 옵션을 지정합니다.

* all
  * 프로세스가 현재 실행 중인지 종료되었는지 여부와 상관없이 기본값으로 각 프로세스에 대한 시계열을 반환
  * PromQL 표현식을 작성하는 경우, 해당 시계열을 원하는대로 집계할 수 있으며, 각각 `pid` 레이블로 구분된다.
* liveall
  * 현재 실행 중인 프로세스에 대한 시계열을 반환
* livesum
  * 현재 실행 중인 각 프로세스로부터 수집되는 특정 값을 합해, 하나의 시계열로 반환
  * 모든 프로세스에 대해 처리 중인 총 요청 수나 자원 사용량 등이 이에 해당
  * 0 이 아닌 값을 가진 프로세스는 중단되었을 수 있기 때문에, 종료된 프로세스는 제외한다.
* max
  * 현재 실행 여부와 상관없이 모든 프로세스가 수집하는 특정 값에 대한 최댓값을 반환
* min
  * 현재 실행 여부와 상관없이 모든 프로세스가 수집하는 특정 값에 대한 최솟값을 반환

아래 예제에서는 구니콘을 수행하기 전에 설정해야 하는 내용을 일부 살펴볼 수 있습니다.

클라이언트 라이브러리가 메트릭을 추적하는 경우에 사용하기 위해 생성한 빈 디렉토리를 가리키는 환경 변수인 `prometheus_multiproc_dir` 를 설정해야 합니다. 어플리케이션을 시작하기 앞서, 계측 코드의 변경 등을 처리하려면 매번 이 디렉토리를 비워줘야 합니다.

```shell
hostname $ export prometheus_multiproc_dir=$PWD/multiproc
hostname $ rm -rf $prometheus_multiproc_dir
hostname $ mkdir -p $prometheus_multiproc_dir
hostname $ gunicorn -w 2 -c config.py app:app
[2018-01-07 19:05:30 +0000] [9634] [INFO] Starting gunicorn 19.7.1
[2018-01-07 19:05:30 +0000] [9634] [INFO] Listening at: http://127.0.0.1:8000 (9634)
[2018-01-07 19:05:30 +0000] [9634] [INFO] Using worker: sync
[2018-01-07 19:05:30 +0000] [9639] [INFO] Booting worker with pid: 9639
[2018-01-07 19:05:30 +0000] [9640] [INFO] Booting worker with pid: 9640
```

2 개의 정의된 메트릭을 `/metrics` 경로에 확인할 수 있지만 `python_info` 나 `process_` 메트릭은 보이지 않습니다.

## Go

**고(Go)** 는 HTTP 요청을 처리하기 위한 `http.Handler` 표준 인터페이스와 고 클라이언트 라이브러리와 인터페이스를 지원하는 `promhttp.Handler` 를 제공합니다. 아래 예제의 내용을 *example.go* 파일에 적용해보겠ㅅ브니다.

```go
package main

import (
  "log"
  "net/http"

  "github.com/prometheus/client_golang/prometheus"
  "github.com/prometheus/client_golang/prometheus/promauto"
  "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
  requests = promauto.NewCounter(
    prometheus.CounterOpts{
      Name: "hello_worlds_total",
      Help: "Hello Worlds requested.",
    })
)

func handler(w http.ResponseWriter, r *http.Request) {
  requests.Inc()
  w.Write([]byte("Hello World"))
}

func main() {
  http.HandleFunc("/", handler)
  http.Handle("/metrics", promhttp.Handler())
  log.Fatal(http.ListenAndServe(":8000", nil))
}
```

아래와 같이 일반적인 방식으로 의존성을 가져온 뒤 이 코드를 수행하면 됩니다.

```shell
hostname $ go get -d -u github.com/prometheus/client_golang/prometheus
hostname $ go run example.go
```

위 예제는 메트릭을 기본 레지스트리에 자동으로 추가하는 `promauto` 라이브러리를 사용합니다. 자동으로 레지스트리에 추가되는 것을 원하지 않는다면, `prometheus.NewCounter` 를 사용할 수 있습니다. 그 다음 `init` 함수에서 `MustRegister` 를 사용하면 됩니다.

```go
func init() {
  prometheus.MustRegister(requests)
}
```

메트릭을 만들고 사용하기에는 간단한 방법이지만 `MustRegister` 호출을 잊어버릴 수 있기 때문에 취약한 방법입니다.

## Java

Java 클라이언트 라이브러리는 **심플클라이언트(SimpleClient)** 라고도 불립니다. JVM 에서 동작하는 언어를 사용해 계측 코드를 개발하려면 자바 클라이언트를 써야합니다.

### HTTPServer

Python 에서 `start_http_server` 를 사용하는 것처럼 Java 클라이언트의 `HTTPServer` 클래스를 사용해 HTTP 서버를 구동하고 수행합니다.

```java
import io.prometheus.client.Counter;
import io.prometheus.client.hotspot.DefaultExports;
import io.prometheus.client.exporter.HTTPServer;

public class Example {
  private static final Counter myCounter = Counter.build()
      .name("my_counter_total")
      .help("An example counter.").register();

  public static void main(String[] args) throws Exception {
    DefaultExports.initialize();
    HTTPServer server = new HTTPServer(8000);
    while (true) {
      myCounter.inc();
      Thread.sleep(1000);
    }
  }
}
```

일반적으로 Java 메트릭은 클래스의 정적 필드로 정의되기 때문에 한 번만 등록됩니다.

다수의 `process`와 `jvm` 메트릭이 동작하기 위해서는 `DefaultExports.initialize` 함수를 호출해야합니다. 이 함수는 여러 번 호출해도 결과가 달라지지 않고 스레드에 안전하기 때문에, 여러 번 호출해도 문제 없습니다.

아래 예제의 코드를 수행시키려면, 심플클라이언트에 대한 의존성이 필요합니다. 아래 예제의 **메이븐(Maven)** 을 사용하는 경우 *pom.xml* 에 작성해야하는 `dependencies` 를 보여줍니다.

```xml
 <dependencies>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient</artifactId>
      <version>0.3.0</version>
    </dependency>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient_hotspot</artifactId>
      <version>0.3.0</version>
    </dependency>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient_httpserver</artifactId>
      <version>0.3.0</version>
    </dependency>
  </dependencies>
```

### Servlet

많은 Java 및 JVM 프레임워크는 HTTP 서버느 미들웨어에 `HttpServlet` 과 서브클래스를 지원합니다. **제티(Jetty)** 가 그러한 서버 사례중 하나로 예제에서는 Java 클라이언트의 `MetricsServlet` 의 사용 방법을 확인할 수 있습니다.

```java
import io.prometheus.client.Counter;
import io.prometheus.client.exporter.MetricsServlet;
import io.prometheus.client.hotspot.DefaultExports;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import java.io.IOException;


public class Example {
  static class ExampleServlet extends HttpServlet {
    private static final Counter requests = Counter.build()
        .name("hello_worlds_total")
        .help("Hello Worlds requested.").register();

    @Override
    protected void doGet(final HttpServletRequest req,
        final HttpServletResponse resp)
        throws ServletException, IOException {
      requests.inc();
      resp.getWriter().println("Hello World");
    }
  }

  public static void main(String[] args) throws Exception {
      DefaultExports.initialize();

      Server server = new Server(8000);
      ServletContextHandler context = new ServletContextHandler();
      context.setContextPath("/");
      server.setHandler(context);
      context.addServlet(new ServletHolder(new ExampleServlet()), "/");
      context.addServlet(new ServletHolder(new MetricsServlet()), "/metrics");

      server.start();
      server.join();
  }
}
```

Java 클라이언트에 대한 의존성도 명시해야 합니다. 아래 *pom.xml* 을 참고하면 됩니다.

```xml
 <dependencies>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient</artifactId>
      <version>0.3.0</version>
    </dependency>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient_hotspot</artifactId>
      <version>0.3.0</version>
    </dependency>
    <dependency>
      <groupId>io.prometheus</groupId>
      <artifactId>simpleclient_servlet</artifactId>
      <version>0.3.0</version>
    </dependency>
    <dependency>
      <groupId>org.eclipse.jetty</groupId>
      <artifactId>jetty-servlet</artifactId>
      <version>8.2.0.v20160908</version>
    </dependency>
  </dependencies>
```

## Pushgateway

**일괄처리 작업(Batch Job)** 은 시간 단위나 일 단위 등의 방식으로 정기적인 일정에 따라 수행됩니다. 이와 같은 일괄처리 작업은 시작되고 무언가 작업을 수행한 뒤 종료합니다. 지속적으로 동작하지 않기 때문에 Prometheus 는 이 작업에 대한 정보를 정확하게 수집할 수 없기 때문에 푸쉬게이트웨이가 필요합니다.

**푸쉬게이트웨이(Pushgateway)** 는 서비스 레벨의 일괄처리 작업에 대한 **메트릭 캐시(Metrics Cache)** 입니다. `Example 1` 은 푸쉬게이트웨이의 아키텍처를 보여줍니다. 

푸쉬게이트웨이는 각 일괄처리 작업이 푸쉬한 마지막 데이터만 캐싱합니다. 일괄처리 작업은 종료되기 직전 처리하고 있던 메트릭을 푸쉬게이트웨이로 푸쉬합니다. Prometheus 는 푸쉬게이트웨이에 저장된 메트릭을 수집하고, 이에 대한 알림을 보내거나 그래프를 그릴 수 있ㅅ브니다. 일반적으로 푸쉬게이트웨이는 Prometheus 와 함께 실행됩니다.

> Example 1 - The Pushgateway architecture

![image](https://user-images.githubusercontent.com/44635266/78896324-468f1580-7aab-11ea-8e7e-3833414ece6c.png)

**서비스 레벨 일괄처리 작업(Service-Level Batch Job)** 은 실제로 적용하는 `instance` 레이블이 없습니다. 즉 일괄처리 작업은 하나의 머신이나 프로세스 인스턴스에 묶이는게 아니라 모든 서비스에 적용됩니다.

만약 일괄처리 작업이 어디서 실행되고 있는지 신경쓸 필요가 없고 실행 자체에 관심이 있다면 그것이 바로 서비스 레벨 일괄처리 작업입니다.

일례로 고장난 머신을 찾기 위한 데이터 센터의 일괄처리 작업이나 모든 서비스에 대한 가비지컬렉션을 수행하는 일괄처리 작업 등도 서비스 레벨 일괄처리 작업이라 할 수 있습니다.

푸쉬게이트웨이는 기본 포트 9091 에서 동작하는 일종의 익스포터이며, Prometheus 가 관련 데이터를 수집하도록 설정해야 합니다. 이를 위해 아래 예제처럼 `honor_labels:true` 를 **수집 구성(Scrape Config)** 에 추가합니다.

왜냐면 푸쉬게이트웨이로 푸쉬되는 메트릭은 `instance` 레이블을 포함하지 않기 때문이며, Prometheus 가 메트릭을 수집할 때 푸쉬게이트웨이 자신에 대한 `instance` 대상 레이블을 포함해서 안되기 때문입니다.

```yaml
scrape_configs:
 - job_name: pushgateway
   honor_labels: true
   static_configs:
    - targets:
      - localhost:9091
```

푸쉬게이트웨이에 메트릭을 푸시하려면 클라이언트 라이브러리를 사용할 수 있습니다. 아래 예제는 Python 일괄처리 작업에 의해 생성된 메트릭을 푸쉬게이트웨이에 반영하는 코드 구조를 보여줍니다.

선택된 메트릭만 푸쉬하기 위한 **사용자 정의 레지스트리(Custom Registry)** 가 생성됩니다. 일괄처리 작업의 지속 시간은 항상 푸쉬게이트웨이에 반영되며, 일괄처리 작업이 성공한 시간은 푸쉬게이트웨이로 메트릭의 푸쉬가 종료된 시간입니다.

푸쉬게이트웨이에 메트릭을 사용하는 방법은 3 가지가 있습니다. Python 에는 `push_to_gateway`, `pushadd_to_gateway`, `delete_from_gateway` 함수를 사용합니다.

* `push`
  * 이미 생성된 일괄처리 작업에 대한 메트릭을 삭제하고 푸쉬게이트웨이에 푸쉬된 메트릭을 추가한다.
  * PUT HTTP 메소드를 사용한다.
* `pushadd`
  * 푸쉬게이트웨이에 푸쉬된 메트릭과 동일한 이름의 메트릭이 잇다면 새로운 값으로 갱신한다. 생성된 다른 이름을 가진 메트릭들은 변경없이 유지된다.
  * POST HTTP 메소드를 사용한다.
* `delete`
  * 일괄처리 작업과 연관된 메트릭을 모두 삭제한다.
  * DELETE HTTP 메소드를 사용한다.

아래 예제와 같이 `push_add_gateway` 를 사용하면 `my_job_duration_seconds` 값은 매번 갱신됩니다. 하지만 `my_job_last_success_seconds` 는 예외가 발생하지 않은 경우에만 갱신됩니다. 이 메트릭은 레지스트리에 추가되고 난 이후 푸쉬됩니다.

```python
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway

registry = CollectorRegistry()
duration = Gauge('my_job_duration_seconds',
        'Duration of my batch job in seconds', registry=registry)
try:
    with duration.time():
        # Your code here.
        pass

    # This only runs if there wasn't an exception.
    g = Gauge('my_job_last_success_seconds',
            'Last time my batch job successfully finished', registry=registry)
    g.set_to_current_time()
finally:
    pushadd_to_gateway('localhost:9091', job='batch', registry=registry)
```

`Example 2` 와 같이 웹 페이지를 통해 푸쉬된 데이터의 상태를 확인할 수 있습니다. 푸쉬게이트웨이는 `push_time_seconds` 메트릭을 추가로 생성하는데 이는 Prometheus 가 이 메트릭을 푸쉬게이트웨이 메트릭의 타임스탬프로 사용하기 때문입니다. `push_time_seconds` 는 데이터가 푸시된 최근의 실제 시간을 알려줍니다.

> Example 2 - The Pushgateway status page showing metrics from a push

![image](https://user-images.githubusercontent.com/44635266/78896358-54449b00-7aab-11ea-8057-d0b2fa3cbee8.png)

푸쉬는 하나의 그룹으로 참조되기도 합니다. 푸쉬할 때 `job` 레이블 외에 다른 레이블을 추가할 수 있는데, 이와 같은 레이블을 **그룹화 키(Grouping Key)** 라고 부릅니다. Python 에는 `grouping_key` 키워드 파라미터를 통해 제공합니다.

그룹화 키는 일괄처리 작업이 어떤 형태든 분산된 경우에 사용할 수 있습니다. 예를 들어 데이터베이스가 30 개로 파편화 되어 분산되어 있으며 각각 일괄처리 작업을 가지고 있다면, `shard` 레이블을 통해 일괄처리 작업을 구분할 수 있습니다.

## Bridges

Prometheus 클라이언트 라이브러리는 메트릭을 Prometheus 가 지정한 형식으로만 출력하도록 제한하지 않습니다. 계측과 표시는 서로 관심사항이 다르기 때문에, 사용자가 원하는 방식으로 메트릭을 처리할 수 있습니다.

예를 들어, Go, Python, Java 클라이언트에는 **그라파이트 브릿지(Graphite Bridge)** 가 있습니다. 브릿지는 클라이언트 라이브러리 레지스트리로부터 메트릭을 전달 받아 Prometheus 가 아닌 다른 형태로 메트릭을 출력합니다.

따라서 그라파이트 브릿지는 아래 예제같이 메트릭을 그라파이트에서 처리할 수 있는 형태로 변환해 전달합니다.

```python
import time
from prometheus_client.bridge.graphite import GraphiteBridge

gb = GraphiteBridge(['graphite.your.org', 2003])
gb.start(10)
while True:
    time.sleep(1)
```

이 코드는 레지스트리가 현재의 모든 메트릭의 스냅샷을 가져올 수 있는 메소드를 제공하기 때문에 동작합니다. Python 의 `CollectorRegistry.collect` Java 의 `CollectiorRegistry.metricFamilySamples`, Go 의 `Registry.Gather` 가 이런 메소드입니다.

이 메소드들은 HTTP 를 통해 표시할 때 이용하지만, 사용자 누구나 쓸 수 있습니다. 예를 들어 이 메소드를 사용해 Prometheus 말고도 다른 계측 라이브러리에 메트릭 데이터를 전달할 수 있습니다.

## Parsers

메트릭 결과에 접근할 수 있는 클라이언트 라이브러리 레지스트리 외에도 Go, Python 클라이언트는 Prometheus 표시 형식을 파싱할 수 있는 **파서(Parser)** 기능을 제공합니다. 아래 예제는 샘플만 출력하지만 Prometheus 는 메트릭을 그 밖의 모니터링 시스템이나 로컬 도구에 전달할 수 있습니다.

```python
from prometheus_client.parser import text_string_to_metric_families

for family in text_string_to_metric_families(u"counter_total 1.0\n"):
  for sample in family.samples:
    print("Name: {0} Labels: {1} Value: {2}".format(*sample))
```

DataDog, InfluxDB, Sensu, Metricbeat 같은 모니터링 시스템은 텍스트 형식으로 파싱할 수 있는 컴포넌트를 지원합니다. 이 모니터링 시스템을 사용한다면, Prometheus 서버를 동작시키지 않더라도 Prometheus 생태계가 가진 장점을 활용할 수 있습니다.

## Exposition Format

Prometheus 의 텍스트 형태의 메트릭 게시 형식은 생성과 **파싱(Parsing)** 이 쉽습니다. 대부분의 메트릭을 처리하는 경우 클라이언트 라이브러리에 의존하지만, 노드 익스포터의 텍스트 파일 수집기처럼 메트릭 게시 형식을 직접 만들어야 하는 경우도 있습니다.

다음과 같은 컨텐트 형식 헤더를 가지는 0.0.4 버전의 텍스트 형식을 보겠습니다.

```
Content-Type: text/plain; version=0.0.4; charset=utf-8
```

텍스트 형식을 간단하게 정리하면, 메트릭의 이름이 나오고, 뒤이어 64 bit 부동소수점 값을 표시합니다. 각 행의 마지막에는 `\n` 를 붙여서 마무리합니다.

```
my_count total 14
a_small_gauge 8.3e-96
```

### Metric Types

완전한 형태의 메트릭 출력은 다음 예제처럼 메트릭의 `HELP` 와 `TYPE` 을 포함합니다. 일반적은 `HELP` 는 메트릭에 대한 설명으로 수집할때마다 변경되어서는 안 되는 값입니다. `TYPE` 은 `counter`, `gaguge`, `summary`, `histogram`, `untyped` 중 하나의 값을 가집니다.

`untyped` 는 메트릭의 형식이 무엇인지 모르는 경우 사용하며 형식이 지정되지 않은 경우 기본값으로 사용됩니다. `HELP` 와 `TYPE` 은 현재 Prometheus 에는 무시되지만, 나중에 쿼리를 작성하기 위한 목적으로 Grafana 같은 도구에서 사용될 수 있습니다. 중복되는 메트릭을 가질 수 없기 때문에, 메트릭에 포함된 모든 시계열이 그룹핑 되어 있는지 확인해야합니다.

```
# HELP example_gauge An example gauge
# TYPE example_gauge gauge
example_gauge -0.7
# HELP my_counter_total An example counter
# TYPE my_counter_total counter
my_counter_total 14
# HELP my_summary An example summary
# TYPE my_summary summary
my_summary_sum 0.6
my_summary_count 19
# HELP my_histogram An example histogram
# TYPE my_histogram histogram
latency_seconds_bucket{le="0.1"} 7
latency_seconds_bucket{le="0.2"} 18
latency_seconds_bucket{le="0.4"} 24
latency_seconds_bucket{le="0.8"} 28
latency_seconds_bucket{le="+Inf"} 29
latency_seconds_sum 0.6
latency_seconds_count 29
```

히스토그램에서는 `_count` 는 +Inf 버킷과 일치해야 하고, +Inf 버킷은 항상 표시되어 있어야 합니다. 버킷이 변경되면 `histogram_quantile` 함수 동작에 문제를 일으킬 수 있기 때문에 데이터 수집시마다 변경되서는 안됩니다. `le` 레이블은 부동소수점 값이 할당되며 정렬되어있어야합니다. `le` 는 *Less than or Equal to* 를 의미하기 때문에 히스토그램 버킷이 어떤 방식으로 누적되는지 확인해야 합니다.

### Labels

레이블이 여러 개라면 쉼표(`,`) 로 구분되며, 닫는 괄호 안에 쉼표를 붙여도 괜찮습니다. 레이블은 순서에 상관없이 쓸 수 있지만 데이터를 수집할 때마다 레이블 순서에 일관성을 유지하는 것이 좋습니다. 일관성을 잘 지키면, 단위 테스트를 작성하기 쉬워지고 Prometheus 도 최상의 데이터 처리 성능을 발휘할 수 있습니다.

```
# HELP my_summary An example summary
# TYPE my_summary summary
my_summary_sum{foo="bar",baz="quu"} 1.8
my_summary_count{foo="bar",baz="quu"} 453
my_summary_sum{foo="blaa",baz=""} 0
my_summary_count{foo="blaa",baz="quu"} 0
```

**차일드(Child)** 가 초기화되지 않은 경우에는 시계열이 없는 메트릭을 정의할 수 있습니다.

```
# HELP a_counter_total An example counter
# TYPE a_counter_total counter
```

### Escaping

이스케이프 문자 형식은 UTF-8 로 인코딩되며 `HELP` 나 레이블 값에는 모든 UTF-8 문자가 허용됩니다. 이스케이프 문자에 역슬래시 사용이 문제가 될 경우 한 번 더 사용합니다.

`HELP` 에서는 라인피드(`\n`) 와 역슬래시(`\`) 가 레이블 값에는 라인피드, 역슬래시, 쌍따옴표가 이에 해당합니다. 이스케이프 문자 형식은 여분의 공백을 무시합니다.

```
# HELP escaping A newline \\n and backslash \\ escaped
# TYPE escaping gauge
escaping{foo="newline \\n backslash \\ double quote \" "} 1
```

### Timestamps

시계열은 **타임스탬프(Timestamp)** 를 명시할 수 있습니다. 타임스탬프는 **유닉스 에포크(UNIX Epoch)** 시간부터 경과된 시간을 밀리초 단위의 정수로 표시한 값입니다.

타임스탬프는 메트릭 값 다음에 위치합니다. 표시 형식에서의 타임스탬프는 **페더레이션(Federation)** 같은 특별한 사용 예에만 적용되며, 일반적으로 사용에 제한이 있기 때문에 잘 쓰이지 않습니다. 데이터 수집에 대한 타임스탬프는 Prometheus 에 의해 대부분 자동 반영됩니다.

하지만 이름과 레이블이 동일한 경우, 타임스탬프가 다른 여러 항목을 지정하면 어떤 일이 발생하는지에 대해서는 정의하지 않습니다.

```
# HELP foo I'm trapped in a client library
# TYPE foo gauge
foo 1 15100992000000
```

### check metrics

Prometheus 2.0 에서는 효율성을 위해 사용자 정의 파서가 도입되었습니다. 따라서 메트릭이 `/metrics` 경로로 수집된다 해서 형식을 준수한다고 볼 수 없습니다.

**프롬툴(Promtool)** 은 Prometheus 에 포함된 유틸리티로, 메트릭 결과가 유효한지 확인하는 **린트(Linx)** rjatkfmf tngodgkqslek.

```shell
curl http://localhost:8000/metrics | promtool check-metrics
```

각 행의 마지막에 라인피드(`\n`) 를 표시하지 않거나, **캐리지 리턴(Carriage Return)** 라인피드(`\r\n`) 를 사용하거나, 유효하지 않은 메트릭이나 레이블 이름을 쓰는 등의 실수가 발생할 수 있습니다.

즉, 메트릭과 레이블 이름에는 하이픈(`-`) 을 써서는 안되며, 숫자로 시작할 수 없습니다.
