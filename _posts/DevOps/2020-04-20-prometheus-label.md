---
title : Prometheus Labels
tags :
- Label
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

## What Are Labels?

레이블은 시계열과 연간된 **키-값(Key-Value)** 쌍으로, 메트릭 이름뿐만 아니라 시계열을 고유하게 식별합니다.

경로별로 분류된 HTTP 요청에 관한 메트릭이 있는 경우, **그라파이트(Graphite)** 에서 흔히 볼 수 있는 것처럼 메트릭 이름에 경로를 넣으려고 할 것입니다.

```
http_requests_login_total
http_requests_logout_total
http_requests_adduser_total
http_requests_comment_total
http_requests_view_total
```

이는 PromQL 에서 작업하기 어려울 수 있습니다. 전체 요청을 계산하기 위해 가능한 한 모든 HTTP 경로를 알고 있거나 잠재적으로 많은 자원을 사용하는 일부 유형을 모든 메트릭 이름에 대해 매칭시켜야 하기 때문에 회피해야 하는 **안티패턴(Antipattern)** 입니다.

대신 이와 같은 일반적인 사용 예를 처리하기 위해 Prometheus 는 레이블을 사용합니다. 앞의 예제의 경우에서는 다음과 같이 `path` 레이블을 이용할 수 있습니다.

```
http_requests_total{path="/login"}
http_requests_total{path="/logout"}
http_requests_total{path="/adduser"}
http_requests_total{path="/comment"}
http_requests_total{path="/view"}
```

`path` 레이블을 포함하는 하나의 `http_requests_total` 메트릭을 사용해 작업할 수 있습니다. PromQL 을 이용해, 전체적으로 집계된 요청 비율, 경로 중 단 한 경로의 비율, 전체 요청 대비 각 요청의 비율 등을 얻을 수 있습니다.

메트릭은 레이블을 하나 이상 가질 수 있습니다. 레이블에는 순서가 없기 때문에, 주어진 레이블을 이용해 다른 레이블을 무시하면서 집계하거나 한 번에 여러 개의 레이블을 갖고 집계할 수 있습니다.

## Instrumentation and Target Labels

레이블은 **계측 레이블(Instrumentation Label)** 과 **대상 레이블(Target Label)**, 이 두가지에서 유래합니다. PromQL 로 작업하는 경우, 이 두 레이블 사이의 차이는 없습니다. 하지만 레이블을 통해 효율을 얻기위해선 이들을 구별해야합니다.

계측 레이블은 어플리케이션이나 라이브러리 내부에서 알 수 있는 내용을 담고 있습니다. 어플리케이션이나 라이브러리가 수신하는 HTTP 요청 타입이나 통신 대상 데이터베이스 등을 비롯한 그 외의 내부상에 관련된 내용을 알 수 있습니다.

대상 레이블은 Prometheus 가 데이터를 수집하는 특정 모니터링 대상을 식별합니다. 아키텍처와 관련이 깊어서, 어플리케이션 유형, 데이터 센터 유형, 개발 환경이나, 운영 환경 여부, 같은 내용이 포함됩니다. Prometheus 는 대상 레이블을 데이터 수집 과정의 일부로 추가할 수 있습니다.

## Instrumentation

아래 예제의 정의 부분에는 `label names=['path']` 레이블을 볼 수 있는데, 이는 메트릭이 `path` 라 불리는 단일 레이블을 가지고 있다는 뜻입니다. 계측에서 메트릭을 사용하는 경우, 레이블 값에 대한 인자와 더불아 반드시 `labels` 메소드에 대한 호출을 추가해야 합니다.

```python
import http.server
from prometheus_client import start_http_server, Counter

REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.',
        labelnames=['path'])

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.labels(self.path).inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()
```

http://localhost:8001/ 와 http://localhost:8001/foo 에 접속하면 http://localhost:8000/metrics 의 `/metrics` 페이지에서 각 경로에 대한 시계열을 볼 수 있습니다.

```
# HELP hello_worlds_total Hello Worlds requested.
# TYPE hello_worlds_total counter
hello_worlds_total{path="/favicon.ico"} 6.0
hello_worlds_total{path="/"} 4.0
hello_worlds_total{path="/foo"} 1.0
```

대체로 메트릭 이름과 달리 레이블 이름은 네임스페이스에 속하지 않습니다. 하지만, 계측 레이블을 정의하는 경우 `env`, `cluster`, `service`, `team`, `zone`, `region` 같이 대상 레이블로 쓰일 것 같은 으림 이름은 피해야 합니다. 또한, 레이블 이름으로 `type` 은 너무 일반적이기 때문에 사용하지 않기 바랍니다. 레이블 이름은 스네이크 표기법을 따릅니다.

모든 UTF-8 문자는 레이블 값으로 쓰일 수 있습니다. 빈 레이블 값도 쓸 수 있지만, 언뜻 보면 해당 레이블이 없는 것처럼 보이기 때문에 Prometheus 서버에 약간의 혼동을 가져올 수 있습니다.

> 레이블의 첫 글자로 `_` 시작은 가능하지만 지양해야 합니다. Prometheus 에 예약된 레이블 이름은 밑줄 `_` 로 시작하기 때문입니다. 
> 메트릭 이름은 Prometheus 내부적으로 `__name__` 이라 불리는 또 다른 레이블을 가집니다. 표현식 `up` 은 `{__name__="up}` 의 간단한 표현입니다.

### Metric

**메트릭(Metric)** 이라는 단어는 메트릭 패밀리, 차일드, 시계열을 의미할 수 있습니다.

```
# HELP latency_seconds Latency in seconds.
# TYPE latency_seconds summary
latency_seconds_sum{path="/foo"} 1.0
latency_seconds_count{path="/foo"} 2.0
latency_seconds_sum{path="/bar"} 3.0
latency_seconds_count{path="/bar"} 4.0
```

`latency_seconds_sum{path="/bar"}` 는 차일드이며 Python 클라이언트에서 `labels()` 의 반환값을 나타냅니다. **서머리(summary)** 경우에 차일드는 이 레이블과 함께 `_sum` 과 `_count` 시계열을 모두 포함합니다.

`latency_seconds` 는 메트릭 패밀리로, 메트릭 이름이나 그와 관련된 타입이며 클라이언트 라이브러리를 사용하는 경우의 메트릭 정의입니다. 레이블이 없는 게이지 메트릭의 경우, 메트릭 패밀리와 메트릭 차일드, 시계열은 동일합니다.

### Multiple Labels

메트릭을 정의하는 경우, 레이블 개수를 지정하고 레이블 호출 시 같은 순서로 값을 지정할 수 있습니다.

```python
REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.',
        labelnames=['path', 'method'])

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.labels(self.path, self.command).inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")
```

Python 과 Go 에서 레이블 이름은 메트릭 정의에 있는 이름과 반드시 일치해야 하지만, 레이블 이름과 값 모두를 **맵(Map)** 으로 제공할 수 있습니다. 이로 인해 인자의 순서를 섞는 것이 어려워질 수도 있지만, 이것이 진짜 문제가 된다면 레이블이 너무 많은 것일 수 있습니다.

메트릭에 대해 변화하는 레이블 이름의 사용은 불가능하며, 클라이언트 라이브러리는 이를 허용하지 않습니다. 중요한 메트릭을 가지고 작업하면 관련 레이블이 무엇인지 알 수 있어야 합니다.

따라서 직접 계층을 수행하는 경우에도 반드시 사전에 레이블 이름을 알고 있어야 합니다. 레이블을 모르면 특정 사용 예를 위한 로그 기반 모니터링 도구가 필요할 수 있습니다.

### Child

Python 에서 `labels` 메소드의 반환 값을 **차일드(Child)** 라 합니다. 차일드는 나중에 사용하기 위해 저장할 수 있습니다. 그러면 각 계측 이벤트에서 차일드를 조회하지 않아도 되고 성능이 중요한 초당 수십만 번 호출되는 코드에서는 시간을 절약할 수 있습니다.

객체가 메트릭에 대해 하나의 차일드만 참조하는 경우 아래 예제와 같이 `labels` 를 한 번 호출한 다음 해당 객체에 저장하는 것이 일반적인 패턴입니다.

```python
from prometheus_client import Counter

FETCHES = Counter('cache_fetches_total',
        'Fetches from the cache.',
        labelnames=['cache'])

class MyCache(object):
    def __init__(self, name):
        self._fetches = FETCHES.labels(name)
        self._cache = {}

    def fetch(self, item):
        self._fetches.inc()
        return self._cache.get(item)

    def store(self, item, value):
        self._cache[item] = value
```

차일드를 보게 되는 또 다른 부분은 이들을 초기화하는 부분입니다. 차일드는 `labels` 를 호출한 후 `/metrics` 에만 표시합니다. 나타났다 사라지는 시계열을 가지고 작업하기란 매우 어렵기 때문에 PromQL 에서 문제가 될 수 있습니다. 따라서 가능하다면 아래 예제와 같이 시작 시점에 차일드를 초기화 해야합니다.

위 예제의 패턴을 따르더라도 시작 시점의 차일드 초기화는 아무런 자원도 사용하지 않습니다.

```python
from prometheus_client import Counter

REQUESTS = Counter('http_requests_total',
        'HTTP requests.',
        labelnames=['path'])
REQUESTS.labels('/foo')
REQUESTS.labels('/bar')
```

Python **데코레이터(Decorator)** 를 사용하는 경우 아래 예제와 같이 반환 값에 대한 메소드를 바로 호출하지 않고도 레이블을 사용할 수 있습니다.

```python
from prometheus_client import Summary

LATENCY = Summary('http_requests_latency_seconds',
        'HTTP request latency.',
        labelnames=['path'])

foo = LATENCY.labels('/foo')
@foo.time()
def foo_handler(params):
    pass
```

## Aggregating

PromQL 에서 레이블을 사용해보겠습니다. 아래 리스트는 이전에 살펴본 `rate(hello_worlds_total[5m])` 의 출력 결과입니다. 각기 다른 HTTP 경로와 메소드를 가지는 두 개의 어플리케이션 인스턴스에 대한 결과를 보여줍니다.

```
{job="myjob”,instance="localhost:1234”,path="/foo”,method="GET"} 1
{job="myjob”,instance="localhost:1234”,path="/foo”,method="POST"} 2
{job="myjob”,instance="localhost:1234”,path="/bar”,method="GET"} 4
{job="myjob”,instance="localhost:5678”,path="/foo”,method="GET"} 8
{job="myjob”,instance="localhost:5678”,path="/foo”,method="POST"} 16
{job="myjob”,instance="localhost:5678”,path="/bar”,method="GET"} 32
```

이 간단한 예제보다 더 많은 시계열이 있는 경우라면 처리가 더 어려울 수 있습니다. 먼저 `path` 레이블로 집계를 시작하겠습니다. 함께 추가하고자 하는 샘플에 대해 `sum` 집계를 사용해 수행합니다. `without` 절은 제거하기 원하는 레이블을 나타냅니다. 이렇게 하면 아래 리스트에 출력 결과를 생성하는 `sum without(path)(rate(hello_worlds_total[5m]))`

```
{job="myjob”,instance="localhost:1234”,method="GET"} 5
{job="myjob”,instance="localhost:1234”,method="POST"} 2
{job="myjob”,instance="localhost:5678”,method="GET"} 40
{job="myjob”,instance="localhost:5678”,method="POST"} 16
```

수백 개의 인스턴스가 있는 경우는 드문일이 아니며, 대시보드에서 개별 인스턴스를 살펴보면 어딘가 3 ~ 5 개로 나뉩니다. `without` 절을 확장하여 `instance` 레이블을 포함할 수 있으며 그 결과 아래 리스트에 보이는 출력 결과를 얻습니다. `GET` 의 경우 초당 $1 + 4 + 8 + 32 = 45$ 개의 요청이 있고 POST 에 대해서는 초당 $2 + 16 = 18$ 개의 요청이 있습니다.

```
{job="myjob”,method="GET"} 45
{job="myjob”,method="POST"} 18
```

레이블은 어떤 방식으로도 정렬되지 않습니다. 따라서 `path` 를 제거할 수 있는 것처럼 `method` 도 제거할 수 있습니다.

```
{job="myjob”,path="/foo"} 27
{job="myjob”,path="/bar"} 36
```

## Label Patterns

Prometheus 는 시계열 값으로 문자열 같은 타입은 지원하지 않고 64 bit 부동소수점 숫자만 지원합니다. 레이블 값은 문자열이며, 로그 기반 모니터링을 너무 많이 사용하지 않고도 레이블을 사용할 수 있는 몇가지 제한된 사용 예가 있습니다.

### Enum

문자열에 대해 일반적인 첫 번째 경우는 **열거형(Enum)** 입니다. 예를 들어 정확하게 `STARTING`, `RUNNING`, `STOPPING`, `TERMINATED` 상태 중 하나를 가지는 자원이 있을 수 있습니다.

이 경우 각각 0, 1, 2, 3 인 게이지로 표시할 수 있습니다. 하지만 PromQL 에서 작업하기는 까다롭습니다. 숫자 0 ~ 3 은 불분명하며, 자원이 `STARTING` 에 사용한 시간의 비율을 알려주는 데 쓸 수 있는 표현식은 하나도 없습니다.

이에 대한 해결책은 차일드가 되는 각각의 잠재적인 상태와 더불어 게이지 상태에 대한 테이블을 추가하는것입니다. Prometheus 에서 불리언 값을 표시할 때 참인 경우 1 을 거짓인 경우 0 을 사용합니다. 따라서 차일드 중 하나는 1 의 값을 가지고 다른 모든 차일드들은 0 의 값을 가질것입니다. 

이에따라 아래 예제와 같은 메트릭을 생성할 것입니다.

```
# HELP gauge The current state of resources.
# TYPE gauge resource_state
resource_state{resource_state="STARTING",resource="blaa"} 0
resource_state{resource_state="RUNNING",resource="blaa"} 1
resource_state{resource_state="STOPPING",resource="blaa"} 0
resource_state{resource_state="TERMINATED",resource="blaa"} 0
```

0 은 항상 존재하기 때문에 PromQL 표현식 `avg_over_time(resource_state[1h])` 은 각 상태에서 사용한 시간의 비율을 제공합니다. 각 상태에서 얼마나 많은 자원을 사용했는지 확인하기 위해, `sum without(resource)(resource_state)` 을 사용해 `resource_state` 에 따라 집계할 수 있습니다.

이 메트릭을 생성하는 데 게이지에 `set` 을 사용할 수 있지만, 이는 경쟁 조건을 발생시킬 수도 있습니다. 정확하게 언제 발생했는지에 따라 데이터 수집 상태는 0 이나 2, 또는 1 인것을 볼 수 있습니다. 업데이트 중간에 게이지가 표시되지 않도록 약간의 상태 격리가 필요합니다.

이에 대한 해결책은 **사용자 정의 수집기(Custom Collectors)** 를 사용하는것입니다.

아래 예제에서 기본적인 구현사항을 확인하고 해결책에 대한 아이디어를 찾아보겠습니다. 일반적으로는 독립 실행형 클래스보단 기존 클래스에 다음과 같은 코드를 추가할 수 있습니다.

```python
from threading import Lock
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class StateMetric(object):
    def __init__(self):
        self._resource_states = {}
        self._STATES = ["STARTING", "RUNNING", "STOPPING", "TERMINATED",]
        self._mutex = Lock()

    def set_state(self, resource, state):
        with self._mutex:
            self._resource_states[resource] = state

    def collect(self):
        family = GaugeMetricFamily("resource_state",
                "The current state of resources.",
                labels=["resource_state", "resource"])
        with self._mutex:
            for resource, state in self._resource_states.items():
                for s in self._STATES:
                    family.add_metric([s, resource], 1 if s == state else 0)
        yield family

sm = StateMetric()
REGISTRY.register(sm)

# Use the StateMetric.
sm.set_state("blaa", "RUNNING")
```

**열거형 게이지(Enum Gauge)** 는 모든 일반적인 게이지의 의미를 따르는 일반적인 게이지이기 때문에, 특별한 메트릭 접미어가 필요하지 않습니다. 

다른 레이블의 개수와 결합 상태의 개수가 너무 많으면 샘플과 시계열의 양 때문에 성능 문제가 발생할 수 있습니다. 유사한 상태들을 함께 결합하려 할 수 있지만, 최악의 경우 열거형을 나타내고 PromQL 에서의 복잡성을 처리하기 위해 0 ~ 3 같은 값을 가지는 게이지를 사용하는 것으로 되돌아가야 할 수 있습니다.

### Info

문자열에 대한 일반적인 두 번재 경우는 `info` 메트릭으로, 역사적인 이유로 **머신 역할 접근방식(Machine Roles Approach)** 이라고도 불립니다. `info` 메트릭은 쿼리하는 데 활용할 수 있는 버전 번호를 비롯한 빌드 정보 등의 어노테이션에 유용합니다. 

하지만 `info` 메트릭을 대상의 모든 메트릭에 적용되는 대상 테이블로 사용하는 것은 타당하지 않으며, 이 사항은 대상의 모든 레이블에 적용됩니다.

이에 따라 나타난 규칙은 1 의 값을 가지는 게이지와 대상에 레이블로 어노테이션하고 싶은 모든 문자열을 사용하는 것입니다. 게이지는 접미어로 `_info` 를 사용해야 합니다. 아래 예제에서 확인하면 됩니다.

```
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="5",patchlevel="2",
        version="3.5.2"} 1.0
```

Python 에서 `info` 메트릭을 생성하려면, 직접 계측이나 사용자 정의 수집기를 사용해야 합니다. 아래 예제는 직접 계측하는 방법을 수행하며, Python 클라이언트에서 키워드 인수로 레이블을 전달하는 기능을 활용합니다.

```python
from prometheus_client import Gauge

version_info = {
    "implementation": "CPython",
    "major": "3",
    "minor": "5",
    "patchlevel": "2",
    "version": "3.5.2",
}

INFO = Gauge("my_python_info", "Python platform information",
        labelnames=version_info.keys())
INFO.labels(**version_info).set(1)
```

`info` 메트릭은 곱셈 연산자와 `group_left` 변경자를 이용해 다른 모든 메트릭과 **조인(join)** 할 수 있습니다. 메트릭을 조인하는 데는 어떤 연산자든 사용할 수 있지만, 정보 메트릭의 값이 1 이기 때문에 곱셈은 다른 메트릭의 값을 바꾸지 않습니다.

모든 `up` 메트릭에 `python_info` 로부터 온 `version` 레이블을 추가하려면 PromQL 표현식을 사용할 수 있습니다.

```
  up
* on (instance, job) group_left(version)
  python_info
```

`group_left(version)` 은 **다대일(Many-to-One)** 일치이며, 따라서 `version` 레이블이 `python_info` 에 동일한 `job` 레이블과 `instance` 레이블을 가지는 모든 `up` 메트릭으로 복사되어야함을 의미합니다.

이 표현식의 출력 결과는 `version` 레이블이 추가된 `up` 메트릭의 레이블을 가지게 될 것이라 말할 수 있습니다. `python_info` 로부터 모든 레이블을 추가하는 것은 불가능하기 때문에, 잠재적으로 표현식의 양쪽에 알려지지 않은 레이블들을 포함할 수 있으며, 의미론적으로 이 표현식은 동작하지 않습니다. 어떤 레이블이 사용 중인지를 알아야 합니다.

또한 `info` 메트릭은 1 의 값을 가집니다. 따라서 `sum` 을 이용해 각 라벨 값을 가지는 시계열의 수를 계산하는 것은 쉽습니다. Python 의 각 버전을 실행하는 어플리케이션 인스턴스의 개수는 `sum by (version)(python_info)` 가 될 수 있습니다. 0 이 아닌 값인 경우, 집계 계층 구조에 필요할 수 있는 `sum` 과 `count` 의 혼합은 더 복잡하며 오류를 발생하기 쉽습니다.

## When to Use Labels

메트릭이 유용해지려면 어떤 방법이든 집계할 수 있습니다. 메트릭의 합계나 평균을 구하는 것이 의미 있는 결과를 만드는 것이 기본 규칙입니다. 경로나 메소드에 따라 HTTP 요청을 나누는 경우, 합은 전체 요청 개수입니다. 큐의 경우 큐 안에 있는 항목들과 큐의 크기를 하나의 메트릭으로 합하는 것은 적절하지 않으며, 합계나 평균 모두 유용한 결과를 만들지 못합니다.

계측 레이블이 유용하지 않다는 한 가지 힌트는 PromQL 에서 메트릭을 사용할 때마다 해당 레이블을 지정해야 하는 경우입니다. 이 경우 레이블을 계속 사용하는 대신 메트릭 이름으로 이동시켜야 합니다.

피해야 하는 다른 경우는 다음과 같이 나머지 메트릭의 전체 합인 시계열을 만드는 것입니다.

```
some_metric{label="foo"} 7
some_metric{label="bar"} 13
some_metric{label="total"} 20
```

또는

```
some_metric{label="foo"} 7
some_metric{label="bar"} 13
some_metric{} 20
```

두 경우 모두 두 번 계산하기 때문에 PromQL 에서 `sum` 을 통한 집계가 엉망이 됩니다. PromQL 에서는 이와 같은 집계를 계산하는 기능을 이미 제공하고 있습니다.

