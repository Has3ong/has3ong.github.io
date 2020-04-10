---
title : Prometheus Instrumentation
tags :
- Histogram
- Summary
- Gague
- Counter
- Instrumentation
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

Prometheus 에서 얻을 수 있는 가장 큰 혜택은 **직접 계측(Direct Instrumentation)** 과 **클라이언트 라이브러리(Client Library)** 를 사용해 어플리케이션을 계측하는 것입니다. 클라이언트 라이브러리는 Go, Python, Java, Ruby 같은 언어를 사용할 수 있습니다.

현 포스트에서는 Python 3 버전으로 진행하겠습니다.

또한 Python 클라이언트 라이브러리도 설치해야합니다.

```shell
$ pip install prometheus_client
```

## A Simple Program

http://localhost:8001 에 접속하면 Hello World 응답을 반환하는 간단한 HTTP 서버를 작성하겠습니다.

```python
import http.server
from prometheus_client import start_http_server

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()
```

`start_http_server(8000)` 함수는 HTTP 서버를 8000 번 포트에서 시작해 Prometheus 에 메트릭을 제공합니다. `Example 1` 처럼 http://localhost:8000 에서 메트릭을 확인할 수 있습니다.

어느 메트릭이 즉시 반환되는지는 플랫폼에 따라 다르며, 리눅스 플랫폼이 가장 많은 메트릭을 반환하는 경향이 있습니다.

> Example 1 - The /metrics page when the simple program runs on Linux with CPython

![image](https://user-images.githubusercontent.com/44635266/78024274-0d5ff280-7393-11ea-8124-5bf0f55ff341.png)

주로 `/metrics` 페이지를 살펴보겠지만 여기서 하려는 것은 Prometheus 에 메트릭을 추가하는 것입니다. 아래 *prometheus.yml* 구성으로 프로메테우스를 설정하고 실행해보겠습니다.

```yml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: example
   static_configs:
    - targets:
      - localhost:8000
```

http://localhost:9090 주소로 접속하면 수식 브라우저에 PromQL 표현식을 `python_info` 를 입력하면 `Example 2` 와 같은 페이지를 보게 될 것입니다.

> Example 2 - Evaluating the expression python_info produces one result

![image](https://user-images.githubusercontent.com/44635266/78024708-ccb4a900-7393-11ea-90fd-77c14c7e7f10.png)

이 포스트에서는 Prometheus 를 실행하고 예제 어플리케이션에서 데이터를 수집한다고 가정하겠습니다. 그리고 생성한 메트릭으로 작업할 때는 수식 브라우저를 사용합니다.

## The Counter 

**카운터(Counter)** 는 계측시 가장 자주 사용하는 메트릭 유형입니다. 카운터는 이벤트 개수나 크기를 추적하며, 특정 경로의 코드가 얼마나 자주 실행되는지 추적합니다.

아래 예제처럼 위 예제 코드를 확장하여 Hello World 가 요청된 횟수를 추적하기 위한 새로운 메트릭을 추가해보겠습니다.

```python
from prometheus_client import Counter

REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
```

코드는 **임포트(import)**, **매트릭 정의(metric definition)**, **계측(instrumentation)** 의 세 부분으로 구성됩니다.

* Import
  * Python 에서 함수와 클래스를 사용하려면 다른 모듈에서 함수와 클래스를 임포트 해야합니다. 따라서 제일 상단에 `prometheus_client` 라이브러리에 `Counter` 클래스를 임포트하는 코드가 있어야 합니다.
* Definition
  * Prometheus 메트릭은 사용하기전에 정의되어야 합니다. 코드에는 `hello_worlds_total` 이라는 카운터로 정의했습니다. 이 카운터는 `Hello World requested.` 라는 도움말을 가지며, 이 도움말은 메트릭의 의미를 이해할 수 있도록 `/metric` 페이지에 표시됩니다.
  * 메트릭은 기본 레지스트리 내의 클라이언트 라이브러리와 함께 자동으로 등록되므로, 메트릭을 `start_http_server` 호출로 다시 끌어올 필요가 없습니다. 실제로 코드의 계측 방법은 결과를 게시하는 부분과 완전히 분리됩니다. Prometheus 의 계측을 포함하는 일시적인 의존성이 있다면, `/metrics` 에 의존성이 자동으로 표시됩니다.
  * 메트릭은 고유한 이름을 가지며, 두 번 등록하려고하면 오류를 보고합니다. 이를 방지하려면 메트릭을 클래스나 함수 혹은 메소드 수준이 아닌 파일 수준에서 정의해야합니다.
* Instrumentation
  * 메트릭 객체를 정의하여 메트릭 객체를 사용할 수 있습니다. `inc` 메소드는 카운터 값을 1 씩 증가합니다. 프로메테우스 클라이언트 라이브러리는 **부기(bookkeeping)** 와 **스레드 안정성(Thread-Safety)** 같은 세부사항을 다뤄주어 필요사항을 모두 처리해줍니다.

프로그램을 실행하면 `/metrics` 페이지에 새로운 메트릭이 표시됩니다. 메트릭은 0 에서 시작해 어플리케이션 URL 에 접속할 때마다 1 씩 증가합니다.

이 내용을 수식 브라우저에서 볼 수 있으며 `Example 3` 처럼 초당 얼마나 ㅁ낳은 요청이 발생했는지 확인하기 위해 PromQL 표현식 `rate(hello_worlds_total[1m])` 을 사용할 수 있습니다.

> Example 3 - A graph of Hello Worlds per second

![image](https://user-images.githubusercontent.com/44635266/78139163-0accce00-7463-11ea-8235-29e2dbb245c1.png)

### Counting Exceptions 

클라이언트 라이브러리는 핵심 기능을 제공할 뿐 아니라 일반적인 사용 예를 위한 유틸리티와 메소드도 제공합니다.

Python 클라이언트 라이브러리 중 하나는 카운터 예외처리 기능을 제공합니다. `try...except` 를 사용해 계측 기능을 작성할 필요가 없습니다. 대신 `Example 4` 처럼 `count_exception` **컨텍스트 매니저(Context Manager)** 와 **데코레이터(Decorator)** 를 이용할 수 있습니다.

```python
import random
from prometheus_client import Counter

REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.')
EXCEPTIONS = Counter('hello_world_exceptions_total',
        'Exceptions serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.inc()
        with EXCEPTIONS.count_exceptions():
          if random.random() < 0.2:
            raise Exception
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
```

`count_exception` 는 문제가 있는 경우 예외를 발생시켜 예외를 전달합니다. 따라서 어플리케이션의 로직을 방해하지 않습니다.

`rate(hello_world_exceptions_total[1m])` 을 통해 예외 비율을 확인할 수 있습니다. 얼마나 많은 요청이 처리되었는지 알지 못하면, 예외 개수는 유용하지 않습니다. 수식 브라우저에서 다음 식을 사용해 더 유용한 예외 비율을 계산할 수 있습니다.

```python
  rate(hello_world_exceptions_total[1m])
/
  rate(hello_worlds_total[1m])
```

`count_exceptions` 를 함수 데코레이터로도 사용할 수 있습니다.

```python
EXCEPTIONS = Counter('hello_world_exceptions_total',
        'Exceptions serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()
    def do_GET(self):
      ...
```

### Counting Size 

Prometheus 는 값을 표현하기 위해 64 bit 부동소수점 방식의 숫자를 사용합니다. 따라서 카운터를 1 씩 증가시키는것에 제한받지 않습니다. 실제 음수가 아닌 임의의 숫자로 카운터를 증가시킬 수 있습니다.

아래 예제처럼 처리된 레코드 개수, 제공된 바이트, 유로화로 표시된 판매량을 추적할 수 있습니다.

```python
import random
from prometheus_client import Counter

REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.')
SALES = Counter('hello_world_sales_euro_total',
        'Euros made serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.inc()
        euros = random.random()
        SALES.inc(euros)
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Hello World for {} euros.".format(euros).encode())
```

수식 브라우저에서 표현식 `rate(hello_world_sales_euro_total[1m])` 을 사용해 정수 카운터와 동일하게 초당 유료화의 판매 비율을 볼 수 있습니다.

## The Gauge 

**게이지(Gauge)** 는 현재 상태에 대한 스냅샷입니다. 카운터가 *얼마나 빨리 증가하는가* 라면, 게이지는 실젯값에 관심을 둡니다.

게이지의 예는 다음과 같습니다.

* the number of items in a queue
* memory usage of a cache
* number of active threads
* the last time a record was processed
* average requests per second in the last minute

### Using Gauges 

게이지에서 사용 가능한 3 가지 주요 메소드는 `inc`, `dec`, `set` 이 있습니다. 카운터 메소드와 마찬가지로, `inc` 와 `dec` 는 게이지의 값을 기본적으로 1 씩 변경합니다. 원하는 경우 변경하고자 하는 다른 값을 가지는 인자를 전달할 수 있습니다.

아래 예제는 진행 중인 호출 개수를 추적하고, 마지막 호출이 언제 완료되는지를 결정하기 위해 게이지를 사용하는 방법입니다.

```python
import time
from prometheus_client import Gauge

INPROGRESS = Gauge('hello_worlds_inprogress',
        'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds',
        'The last time a Hello World was served.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        INPROGRESS.inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
        LAST.set(time.time())
        INPROGRESS.dec()
```

이러한 메트릭들은 추가적인 기능 없이 수식 브라우저에서 바로 사용할 수 있습니다. 예를 들어 마지막 Hello World 가 언제 서비스되었는지 파악하기 위해, `hello_world_last_time_seconds` 가 사용될 수 있습니다.

이와 같은 메트릭의 주된 사용 예는 요청이 처리된 후 시간이 얼마나 오래되었는지 감지하는 것입니다. PromQL 표현식 `time() - hello_world_last_time_seconds` 는 마지막 요청 후 얼마나 오랜 시간이 지났는지 알려줍니다.

이 두 경우눈 모두 매우 일반적인 사용 예로 아래 예제에서 볼 수 있듯이 유틸리티 함수도 제공됩니다. `track_inprogress` 는 예외를 짧고 올바르게 처리할 수 있습니다.

`time.time()` 이 초 단위로 유닉스 시간을 반환하기 때문에, `set_to_current_time` 은 Python 에서 그리 유용하지 않습니다. 하지만 다른 언어의 클라이언트 라이브러리에서는 `set_to_current_time` 을 사용하는 것이 더 간단하고 명확합니다.

```python
from prometheus_client import Gauge

INPROGRESS = Gauge('hello_worlds_inprogress',
        'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds',
        'The last time a Hello World was served.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @INPROGRESS.track_inprogress()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
        LAST.set_to_current_time()
```

> Prometheus 의 규약으로 게이지는 **접미어(suffix)** 가 없는 반면 예제의 카운터 메트릭은 모두 `_total` 로 끝납니다. 이 외에도 `_count`, `_sum`, `_bucket` 접미어도 있습니다.

### Callbacks 

**캐시(Cache)** 내부 항목들의 크기나 번호를 추적하려면, 일반적으로 각 함수에 항목이 캐시에 추가되거나 제거되는 부분에 `inc` 와 `dec` 호출을 추가해야 합니다.

필요한 **익스포터(Exporter)** 를 작성하는 인터페이스를 사용할 필요 없이 클라이언트 라이브러리가 추적을 구현할 수 있는 손쉬운 방법을 제공합니다.

Python 에서 게이지는 게시 시점에 호출되야 하는 함수를 지정할 수 있는 `set_function` 메소드를 갖고 있습니다. 함소구 호출되는 경우 메트릭에 대한 부동소수점 값을 반드시 반환해야합니다. 하지만 직접 게측의 범위를 약간 벗어납니다. 

따라서 스레드 안정성을 고려해야 하며, **뮤텍스(mutex)** 를 사용해야 할 수도 있습니다.

```python
import time
from prometheus_client import Gauge

TIME = Gauge('time_seconds',
        'The current time.')
TIME.set_function(lambda: time.time())
```

## The Summary 

시스템의 성능을 이해하려고 할 때 어플리케이션이 요청에 응답하는 데 걸리는 시간이나 백엔드의 대기 시간은 중요한 메트릭입니다. 다른 계측 시스템에서는 **타이머(Timer)** 메트릭 같은 형태를 제공하지만, Prometheus 는 좀 더 일반적인 관점을 가집니다. 

카운터가 1 이 아닌 다른 값으로 증가될 수 있는 것처럼, 대기시간 이외에 이벤트 사항을 추적하고자 할 수도 있습니다. 예를 들어 백엔드 대기시간 이외에 돌려받은 응답의 크기를 추적하기 원할 수 있습니다.

**서머리(Summary)** 의 주요 메소드는 `observe` 로 이벤트의 크기를 넘겨줍니다. 이벤트의 크기는 반드시 음수가 아닌 값이어야 합니다. `time.time()` 을 사용해 아래 예제처럼 대기시간을 추적할 수 있습니다.

```python
import time
from prometheus_client import Summary

LATENCY = Summary('hello_world_latency_seconds',
        'Time for a request Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        start = time.time()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
        LATENCY.observe(time.time() - start)
```

`/metrics` 를 살펴보면, `hello_world_latency_seconds` 메트릭은 2 개의 시계열인 `hello_world_latency_seconds_count` 와 `hello_world_latency_seconds_sum` 을 참조하는 사실을 확인할 수 있습니다.

`hello_world_latency_seconds_count` 는 수행된 `observe` 호출의 개수로, 수식 브라우저에서 `rate(hello_world_latency_count[1m])` 은 Hello World 요청의 초당 비율을 반환합니다.

`hello_world_latency_seconds_sum` 은 `observe` 로 전달된 값의 합입니다. 따라서 `rate(hello_world_latency_count[1m])` 는 1 초당 요청에 대한 응답에 소요된 시간의 양입니다.

이 두 표현식으로 나누기를 수행하면 마지막 1 분에 대한 평균 대기시간을 얻습니다. 평균 대기시간의 전체 표현식은 다음과 같습니다.

```python
  rate(hello_world_latency_seconds_sum[1m])
/
  rate(hello_world_latency_seconds_count[1m])
```

일반적으로 서머리는 대기시간을 추적하는데 사용되며, 아래 예제에서 볼 수 잇듯이 추적 작업을 더 간단하게 만드는 데는 `time` 컨텍스트 매니저와 함수 데코레이터가 쓰입니다. 이들은 예외와 시간을 역순으로 처리합니다.

```python
from prometheus_client import Summary

LATENCY = Summary('hello_world_latency_seconds',
        'Time for a request Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @LATENCY.time()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
```

Python 클라이언트는 현재 클라이언트 측면의 **분위수(Quantile)** 를 지원하지 않지만, 서머리 메트릭은 분위수를 포함할 수 있습니다.

일반적으로 클라이언트 측면의 분위수는 상위 분위수에 대한 평균을 계산할 수 없고, 서비스 인스턴스로부터 클라이언트 측면의 분위수를 집계하지 못하므로 피해야 합니다.

또한, 클라이언트 측면 분위수는 CPU 사용량 관점에서 다른 계측 항목에 비교하면 비용이 많이 듭니다. 계측으로 얻는 이득은 계측에 드는 자원 비용보다 훨씬 더 중요하지만, 분위수의 경우는 꼭 그렇지 않습니다.

## The Histogram 

분위수는 실제 사용자 경험에 대해 추론할 때 유용합니다. 사용자의 브라우저가 어플리케이션에 20 개 요청을 동시에 보낸다면, 이중 가장 느린 요청이 사용자가 확인할 수 있는 대기시간을 결정합니다. 이 경우 95 번재 **백분위수(Percentile)** 가 대기시간을 의미합니다.

히스토그램을 위한 계측은 서머리와 동일합니다. `observe` 메소드를 통해 수동 관찰을 할 수 있으며, 아래 예제처럼 `time` 컨텍스트 매니저와 함수 데코레이터는 시간을 더 쉽게 지정할 수 있습니다.

```python
from prometheus_client import Histogram

LATENCY = Histogram('hello_world_latency_seconds',
        'Time for a request Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @LATENCY.time()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
```

이 코드는 카운터의 집합인 `hello_world_latency_seconds_bucket` 이라는 시계열 세트를 생성합니다.

히스토그램에는 1ms, 10ms, 25ms 같은 **버킷(bucket)** 의 집합이 있으며, 각 버킷에 속하는 이벤트 수를 추적합니다. `histogram_quantile` PromQL 함수는 버킷들로부터 분위수를 계산할 수 있습니다. 예를 들어 0.95 분위수는 다음과 같습니다.

```python
histogram_quantile(0.95, rate(hello_world_latency_seconds_bucket[1m]))
```

이 `rate` 함수는 버킷의 시계열이기 때문에 카운터가 필요합니다.

### Buckets 

기본 **버킷(Bucket)** 은 1 ms 에서 10 초의 범위를 다룹니다. 이것은 웹 어플리케이션의 일반적인 대기시간의 범위를 처리하기 위한 것입니다.

하지만 메트릭을 정의할 때, 이들을 오버라이딩해서 자체적인 버켓을 제공할 수 있습니다. 이것은 기본 버킷이 사용에 적합하지 않거나 **SLA(Service-level Agreement)** 에 대기시간 분위수에 대한 명시적인 버킷 추가를 언급하는 경우가 될 수 있습니다. 제공된 버킷은 오타를 감지할 수 있도록 반드시 정렬되어 있어야합니다.

```python
LATENCY = Histogram('hello_world_latency_seconds',
        'Time for a request Hello World.',
        buckets=[0.0001, 0.0002, 0.0005, 0.001, 0.01, 0.1])
```

신형 버킷이나 지수형 버킷을 원하는 경우, 다음과 같이 Python 의 **리스트 컴프리헨션(List Comprehension)** 기능을 이용할 수 있습니다. 리스트 컴프리헤션에 해당하는 기능이 없는 언어의 클라이언트 라이브러리는 이를 대신하는 다양한 유틸리티 함수를 갖고 있을 수 있습니다.

```python
buckets=[0.1 * x for x in range(1, 10)]    # Linear
buckets=[0.1 * 2**x for x in range(1, 10)] # Exponential
```

충분한 정확도를 확보하려면 10 개 정도의 버킷을 유지하길 권장합니다. 기본적으로 Prometheus 같은 메트릭 기반 시스템은 100 % 정확한 분위수를 제공하지 않습니다. 정확한 분위수를 갖기 위해서는 로그 기반 시스템에서 분위수를 계산해야 합니다. 하지만, Prometheus 가 제공하는 값은 대부분의 실질적인 알림과 디버깅 목적에 충분합니다.

분위수를 한번 계산하면, 이들에 대한 분위수 계산을 더 이상 할 수 없는 제한이 있습니다. 분위수에 대한 산술연산과 평균을 구하는 것은 통계적으로 정확하지 않습니다. 이는 PromQL 에 시도하는 것뿐만 아니라 디버깅하는 동안 시스템에 생각하는 방법에도 영향을 미칩니다. 프론트는 0.95 분위수에서 대기시간이 증가했다고 보고할 수 있지만, 백엔드는 그러한 증가를 보여주지 못합니다.

대기시간 문제는 분위수보다는 평균으로 디버깅하길 권장합니다. 평균은 생각한 대로 동작합니다. 그리고 평균을 이용해 대기시간을 증가시키는 원인이 되는 서브시스템을 찾아내면, 적절한 경우 분위수로 되돌릴 수 있습니다. 이를 위해 히스토그램은 `_sum` 과 `_count` 시계열을 포함시킵니다.

서머리와 마찬가지로, 평균 대기시간은 다음 표현식으로 계산 가능합니다.

```python
  rate(hello_world_latency_seconds_sum[1m])
/
  rate(hello_world_latency_seconds_count[1m])
```
        
## Unit Testing Instrumentation 

**단위 테스트(Unit Test)** 는 시간이 지나면서 코드가 변경됨에 따라 실수로 코드가 망가지는 것을 방지하는 좋은 방법입니다. 로그를 통해 단위 테스트에 접근하는 것과 같은 방법으로 단위 테스팅 계측에 접근해야 합니다. 디버그 수준의 로그 문장을 테스트하지 않는 것과 마찬가지로, 코드 베이스 전반에 포함되어 있는 대부분의 메트릭을 테스트해서는 안됩니다.

대부분은 트랜잭션 로그의 로그 문장만 단위 테스트하고, 요청 로그만 테스트합니다. 마찬가지로 어플리케이션이나 라이브러리의 핵심 부분인 경우에는 단위 테스트 메트릭에 대해서도 적합합니다. 예를 들어 RPFC 라이브러리를 작성하는 경우에는 핵심 요청, 대기사항, 오류 메트릭의 동작을 확인하기 위해 최소한의 기본 테스트를 수행하는 것이 좋습니다.

Python 클라이언트는 효과적으로 레지스트리를 수집하고 시계열을 살펴볼 수 있는 `get_sample_value` 함수를 제공합니다. 아래 예제처럼, 카운터 계측 테스트에는 `get_sample_value` 를 사용할 수 있습니다.

우리가 관심을 갖는건 카운터의 증가분입니다. 따라서 카운터의 절대값보단 이전 값과 이후 값을 비교해야합니다. 카운터 전후 값의 비교는 단위테스트가 카운터가 증가시키는 원인이 되는 경우에도 동작할 것입니다.

```python
import unittest
from prometheus_client import Counter, REGISTRY

FOOS = Counter('foos_total', 'The number of foo calls.')

def foo():
    FOOS.inc()

class TestFoo(unittest.TestCase):
    def test_counter_inc(self):
        before = REGISTRY.get_sample_value('foos_total')
        foo()
        after = REGISTRY.get_sample_value('foos_total')
        self.assertEqual(1, after - before)
```

## Approaching Instrumentation 

### What Should I Instrument? 

일반적으로 계측을 하는 경우에, 계측 서비스나 계측을 위한 라이브러리가 필요합니다.

#### SERVICE INSTRUMENTATION

자체적인 핵심 메트릭을 가지는 서비스 타입에는 온-오프라인 시스템, 일괄처리 작업의 3 가지가 있습니다.

**온라인 서비스 시스템(Online-Serving System)** 은 사람이나 다른 서비스가 응답을 기다리는 시스템입니다. 여기에는 웹 서버와 데이터베이스도 포함됩니다.

주요 메트릭은 **요청 비율(request rate)**, **대기시간(latency)**, **오류 비율(error rate)** 입니다. 이러한 요청 비율은 각각 Rate, Error, Duration 으로 RED 메소드라고 부릅니다.

**오프라인 서비스 시스템(Offline-Serving System)** 에는 응답을 기다리는 대기자가 없습니다. 대체로 오프라인 서비스 시스템은 작업을 일괄 처리하며, 여러 단계를 가지는 파이프라인을 갖습니다.

파이프라인의 단계들 사이에는 대기열이 존재합니다. **로그 처리 시스템(Log Processing System)** 은 오프라인 서비스 시스템의 일종입니다. 각 단계별로, 대기 중인 작업의 총량, 진행 중인 작업량, 항목의 처리 속도, 발생 오류에 대한 메트릭이 있어야 합니다.

이러한 메트릭들은 **활용도(Ultimation)**, **포화도(Saturation)**, **오류(Error)** 로 USE 메소드라고 읽습니다.

활용도는 서비스가 얼마나 충분한지를 의미하며, 포화도는 대기중인 작업의 양을 뜻합니다. 일괄처리를 하는 경우에는 일괄처리와 개별 항목 모두에 대한 메트릭을 갖는 것이 좋습니다.

**일괄 처리 작업(Batch Job)** 은 서비스의 세 번째 타입으로, 오프라인 서비스 시스템과 유사합니다. 하지만 일괄처리 작업은 정기적으로 실행되는 반면, 오프라인 서비스 시스템은 지속적으로 수행됩니다.

일괄처리 작업이 항상 살행되지는 않기 때문에, 이에 대한 데이터 수집은 잘 동작하지 않습니다. 따라서 **푸시게이트웨이(Pushgateway)** 같은 기법들이 사용됩니다.

#### LIBRARY INSTRUMENTATION

서비스는 고수준에서 관심을 갖습니다. 각 서비스에는 작은 서비스로 간주할 수 있는 라이브러리들이 있습니다. 대부분의 서비스는 **동기 함수 호출(Synchronous Function Call)** 이라 불리는 온라인 서비스 서브시스템에 의존합니다.

그리고 요청과 대기시간, 오류 같은 동일한 메트릭으로부터 이득을 얻습니다. 캐시의 경우, 캐시 전체와 캐시 미스 모두에 대해 이러한 메트릭을 원하면 결과를 계산하거나 백엔드로 요청해야 합니다. 발생하는 모든 오류와 로깅 가능한 모든 부분에 메트릭을 추가하는 것이 좋습니다.

**스레드(Thread)** 나 **워커 풀(Worker Pool)** 은 오프라인 서비스 시스템과 유사하게 계측됩니다. 여러분은 대기열 크기, 활성 스레드, 스레드 개수에 대한 모든 제한과 발생한 오류에 대한 메트릭을 갖기 우너할 수 있습니다.

한 시간 동안 여러 번 수행되는 백그라운드 유지보수 **태스크(Task)** 는 효과적인 일괄처리 작업입니다. 따라서 이러한 태스크에 대해 유사한 메트릭이 있어야 합니다.

### How Much Should I Instrument? 

Prometheus 는 처리할 수 있는 메트릭의 개수에는 제한이 있습니다. 어떤 경우에는 운영과 자원에 대한 비용이 특정 계측 전략이 갖는 이점보다 더 클 수 있습니다.

Prometheus 는 일반적으로 가장 큰 10 개 메트릭이 자원 사용량의 절반을 차지합니다. Prometheus 의 자원 사용량을 관리하려는 경우, 가장 큰 10 개의 메트릭에 초점을 맞춰 더 나은 결과를 얻을 수 있습니다.

### What Should I Name My Metrics?

메트릭 이름을 구성하기 위한 일반적인 가이드 라인도 있습니다.

일반적으로 메트릭 이름의 전체적인 구조는 `library_name_unit_suffix` 입니다.

#### CHARACTERS

Prometheus 메트릭 이름은 문자로 시작해야하며, 그 뒤에는 문자, 숫자, 밑줄 등 아무형태나 붙여 사용할 수 있습니다.

`[a-zA-Z_:][a-zA-Z0-9_:]*` 은 Prometheus 의 유효한 메트릭에 대한 정규표현식입니다.

콜론(`:`) 은 **기록 규칙(Recording Rule)** 에서 사용자가 쓰도록 예약되어 있기 때문에 계측명에 사용해서는 안됩니다. 메트릭 이름의 시작부분에 있는 밑줄(`_`) 은 Prometheus 내부 사용을 위해 예약된 문자입니다.

#### SNAKE_CASE

Prometheus 명명 규약에 따르면 메트릭 이름은 **스네이크 표기법(Snake Case)** 를 사용합니다. 이름의 각 부분은 소문자여야 하며 밑줄(`_`) 로 분리되어야 합니다.

#### METRIC SUFFIXES

카운터, 서머리, 히스토그램 메트릭에 `_total`, `_count`, `_sum`, `_bucket` 접미어가 사용됩니다. 카운터에 항상 `_total` 접미어가 붙는 것을 제외하고는, 혼란을 방지하려면 메트릭 이름의 마지막에 이러한 접미어를 붙이는 것은 피해야합니다.

#### UNITS

초, 바이트, 비율처럼 접두어가 없는 기본 단위의 사용을 선호해야 합니다. Prometheus 가 `time` 같은 함수에서 초 단위를 사용하고 kilomicrosecond 같은 단위를 사용하지 않기 때문입니다.

하나의 단위만 사용하면 특정 메트릭이 초 단위인지 밀리초 단위인지에 대한 혼동을 피할 수 있습니다. 혼동을 피하려면 항상 이름에 메트릭의 단위를 붙여야합니다. 예를 들어 `mymeric_seconds_total` 는 초 단위를 갖는 카운터입니다.

#### NAME

메트릭 이름은 메트릭의 기반이 된 서브시스템에 대해 잘 알지 못하는 사람에게 그 의미를 파악할 수 있게 하는 단초를 제공합니다. `request` 보다 `http_requests` 는 의미가 선명히 전달되며, `http_requests_authenticated` 는 훨씬 더 좋은 표현입니다.

`items` 와 `items_limits` 와 같이 일반적으로 이름은 왼쪽에서 오른쪽으로 갈수록 점차 더 구체적이어야 합니다.

#### LIBRARY

메트릭 이름은 효과적인 전역 **네임스페이스(namespace)** 이기 때문에 라이브러리 사이의 충돌을 피하고 메트릭이 어디에서 온 것인지를 표시하는 것이 중요합니다.

동일한 어플리케이션 안에 여러 개의 라이브러리가 있을수도 있을테니 `robustperception_db_pool` 이나 `rp_db_pool` 이 더 좋은 표현입니다.

예를 들어 `go_memstats_heap_inuse_bytes` 는 이름에서 Go 가 사용 중인 힙 메모리의 양이라는 사실을 간파할 수 있습니다.