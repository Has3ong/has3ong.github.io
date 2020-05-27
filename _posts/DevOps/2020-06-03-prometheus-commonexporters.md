---
title : Prometheus Common Exporters
tags :
- Exporter
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

익스포터를 간단히 정리하면 익스포터는 아무런 구성 없이 작업만합니다. 일반적으로 어떤 어플리케이션 인스턴스의 데이터를 수집할지 알려주기 위한 최소한의 설정이 익스포터에는 필요합니다. 반대의 경우, 작업 중인 데이터가 매우 일반적이기 때문에 광범위한 구성이 필요한 익스포터도 있습니다.

일반적으로 Prometheus 의 사용법은 모든 어플리케이션이 직접 계측한 다음, Prometheus 가 이를 검색하고 직접 수집하는 것입니다. 이것이 불가능한 경우 익스포터가 사용되며, 가능한 기존 아키텍처를 유지하려고 할 것입니다.

어플리케이션 인스턴스와 함게 익스포터가 수행되면 규모 확장시 관리가 쉬워지고 수집에 실패한 도메인을 정의해 관리할 수 있습니다.

## Consul

아래 예제를 통해 컨설 익스포터를 다운로드하고 실행할 수 있습니다. 컨설은 8500 포트에서 동작합니다.

```shell
hostname $ wget https://github.com/prometheus/consul_exporter/releases/
    download/v0.3.0/consul_exporter-0.3.0.linux-amd64.tar.gz
hostname $ tar -xzf consul_exporter-0.3.0.linux-amd64.tar.gz
hostname $ cd consul_exporter-0.3.0.linux-amd64/
hostname $ ./consul_exporter
INFO[0000] Starting consul_exporter (version=0.3.0, branch=master,
    revision=5f439584f4c4369186fec234d18eb071ec76fdde)
    source="consul_exporter.go:319"
INFO[0000] Build context (go=go1.7.5, user=root@4100b077eec6,
    date=20170302-02:05:48)  source="consul_exporter.go:320"
INFO[0000] Listening on :9107                   source="consul_exporter.go:339"
```

http://localhost:9107/metrics 에 접속하면 관련 메트릭을 확인할 수 있습니다.

주목해야하는 메트릭은 `consul_up` 입니다. 일부 익스포터는 데이터를 가져오는데 실패하면 Prometheus 에 HTTP 오류를 반환하며, 이로 인해 Prometheus 의 `up` 메트릭은 0 이 됩니다. 하지만 이러한 시나리오에서도 많은 익스포터들은 여전히 수집에 성공하며 `consul_up` 같은 메트릭을 사용해 문제가 있는지 여부를 확인합니다.

따라서 **컨설 중지 알람(Consul Being Down)** 을 받은 경우, `up` 과 `consul_up` 을 동시에 확인해야 합니다. 컨설을 중지하고 `/metrics` 를 살펴보면 값이 0 으로 변경되는 것을 확인할 수 있고 컨설을 다시 시작하면 1 로 변경되는 것을 확인할 수 있습니다.

`consul_catalog_service_node_healthy` 는 컨설 노드에서 실행되는 다양한 서비스의 상태를 알려주며 Kubernetes 클러스터 전체에 걸쳐 노드와 컨테이너의 상태에 대해 알려주는 `kube-state-metrics` 의 동작과 유사합니다.

`consul_self_lan_member` 는 클러스터 내의 컨설 에이전트의 개수를 의미합니다. 이는 컨설 클러스터의 리더로부터 파악될 수 있는지 의문을 가질 수 있지만, 네트워크 파티션 같은 문제가 있는 경우 각 에이전트가 클러스터 내의 멤버 개수를 다른 관점으로 파악할 수 있는 사실을 알아야 합니다.

일반적으로 클러스터의 모든 멤버로부터 나온 이와 같은 메트릭을 게시하고, PromQL 에서 집계를 사용해 원하는 값으로 통합해야 합니다.

컨설 익스포터와 관련된 메트릭도 있습니다. `consul_exporter_build_info` 는 빌드 정보를 나타내며, 다양한 `process_` 와 `go_` 메트릭들은 프로세스와 Go 런타임에 관련 정보를 나타냅니다. 이런 메트릭은 컨설 익스포터 자체 문제를 디버깅 하는데 유용합니다.

아래 예제에서 컨설 익스포터가 수집하도록 Prometheus 를 구성하는 방법을 확인할 수 있습니다. 익스포터를 통해 수집해도, 실제로는 컨설이 제공하는 정보를 수집하기 때문에 `job` 레이블은 `consul` 로 사용했습니다.

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: consul
   static_configs:
    - targets:
      - localhost:9107
```

## HAProxy

HAProxy 익스포터는 전형적인 익스포터입니다. 먼저 아래 예제와 같이 *haproxy.cfg* 라는 이름의 구성 파일을 생성해 확인합니다.

```
defaults
  mode http
  timeout server 5s
  timeout connect 5s
  timeout client 5s

frontend frontend
  bind *:1234
  use_backend backend

backend backend
  server node_exporter 127.0.0.1:9100

frontend monitoring
  bind *:1235
  no log
  stats uri /
  stats enable
```

이제 아래 명령으로 HAProxy 를 실행하겠습니다.

```shell
$ docker run -v $PWD:/usr/local/etc/haproxy:ro haproxy:1.7
```

이 구성은 http://localhost:1234 를 노드 익스포터로 프록시 처리합니다. 이 구성의 중요 부분은 아래와 같습니다.

```
frontend monitoring
  bind *:1235
  no log
  stats uri /
  stats enable
```

이를 통해 통계 보고 기능이 있는 HAProxy 프론트엔드가 http://localhost:1235 에 수행되면 HAProxy 익스포터가 사용할 CSV 결과가 http://localhost:1235/;csv 에 표시됩니다.

```shell
hostname $ wget https://github.com/prometheus/haproxy_exporter/releases/download/
    v0.9.0/haproxy_exporter-0.9.0.linux-amd64.tar.gz
hostname $ tar -xzf haproxy_exporter-0.9.0.linux-amd64.tar.gz
hostname $ cd haproxy_exporter-0.9.0.linux-amd64/
hostname $ ./haproxy_exporter --haproxy.scrape-uri 'http://localhost:1235/;csv'
INFO[0000] Starting haproxy_exporter (version=0.9.0, branch=HEAD,
    revision=865ad4922f9ab35372b8a6d02ab6ef96805560fe)
    source=haproxy_exporter.go:495
INFO[0000] Build context (go=go1.9.2, user=root@4b9b5f43f4a2,
    date=20180123-18:27:27)  source=haproxy_exporter.go:496
INFO[0000] Listening on :9101                     source=haproxy_exporter.go:521
```

http://localhost:9101/metrics 로 이동하면, 생성된 메트릭을 확인할 수 잇습니다. 컨설 익스포터의 `consul_up` 과 유사하게 HAProxy 가 정상 동작하는지 확인할 수 있는 `haproxy_up` 매트릭이 있습니다.

HAProxy 는 프론트엔드와 백엔드 그리고 서버로 구성되며, 각각 접두어 `haproxy_frontend_`, `haproxy_backend_`, `haproxy_server_` 를 가지는 메트릭을 제공합니다. 예를 들어 `haproxy_server_bytes_out_total` 은 각 서버가 반환한 바이트 수를 나타내는 카운터입니다.

백엔드에는 많은 서버가 있기 때문에, `haproxy_server_` 메트릭의 카디널리티는 문제를 일으킬 수 있습니다. `--haproxy.server-metric-fields` 명령행 플래그는 반환되는 메트릭을 제한할 수 있습니다.

이는 메트릭이 높은 카디널리티를 가질 수 있는 예로, 익스포터는 카디널리티를 선택적으로 조절할 수 있는 방법을 제공합니다. MySQLd 익스포터 같은 익스포터에스는 기본적으로 대부분의 메트릭을 비활성화하는 상반된 접근 방법을 사용합니다.

HAProxy 익스포터는 일부 익스포터에서도 구현한 주목할 만한 기능이 잇습니다. 유닉스에서는 init 시스템을 프로세스 제어에 사용하기 위해 데몬이 자신의 프로세스 ID 를 저장하는 pid 파일을 가집니다.

이 파일을 `--haproxy.pid-file` 명령행 플래그로 전달하면 HAProxy 익스포터는 HAProxy 자체 수집하는 데 실패하더라도 HAProxy 프로세스에 관련된 `haproxy_process` 메트릭을 추가합니다. 이 메트릭은 HAProxy 익스포터가 아닌 HAProxy 를 참조하는 점을 제외하면 `process_` 메트릭과 동일합니다.

아래 예제와 같이 다른 익스포터와 마찬가지로 Prometheus 가 아닌 HAProxy 익스포터를 수집하도록 구성할 수 잇습니다.

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: haproxy
   static_configs:
    - targets:
      - localhost:9101
```

## Grok Exporter

모든 어플리케이션이 익스포터를 사용해 무언가 변환하여 Prometheus 가 이해할 수 있는 형태의 메트릭을 생성하는 것은 아닙니다. 하지만 이 어플리케이션은 로그를 생성할 것이고, **그록 익스포터(Grok Exporter)** 는 로그를 메트릭으로 변환할 때 사용할 수 잇습니다.

그록은 일반적으로 **로그스태시(LogStash)** 에서 사용하는 비정형적인 로그를 파싱하는 방법입니다. 그록 익스포터는 기존 패턴을 재사용하기 위해 동일한 패턴 언어를 재사용합니다.

*example.log* 로 불리는 파일에 다음과 같이 간단한 로그가 있다고 생각해보겠습니다.

```
GET /foo 1.23
GET /bar 3.2
POST /foo 4.6
```

그록 익스포터를 사용해 이러한 로그를 메트릭으로 변경할 수 있습니다. 먼저 리눅스 amd64 용 그록 익스포터를 내려받고 압축을 해제합니다. 다음 *grok.yml* 파일을 생성하고 아래 예제와 같이 작성합니다.

```yml
global:
  config_version: 2
input:
  type: file
  path: example.log
  readall: true  # Use false in production
grok:
  additional_patterns:
   - 'METHOD [A-Z]+'
   - 'PATH [^ ]+'
   - 'NUMBER [0-9.]+'
metrics:
 - type: counter
   name: log_http_requests_total
   help: HTTP requests
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   labels:
     path: '{{.path}}'
 - type: histogram
   name: log_http_request_latency_seconds_total
   help: HTTP request latency
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   value: '{{.latency}}'
server:
   port: 9144
```

마지막으로 그록 익스포터를 실행합니다.

```shell
./grok_exporter -config grok.yml
```

자세히 살펴보면, 첫 번째 부분에는 항상 표시되어야 하는 구문이 있습니다.

```yml
global:
  config_version: 2
```

아래 부분에서 읽어야 하는 파일을 정의합니다. `readall: true` 로 설정하면, 예제와 같은 결과를 확인할 수 있습니다. 운영 환경에서 기본값인 `false` 로 두면 파일 끝부분만 처리합니다.

```yml
input:
  type: file
  path: example.log
  readall: true  # Use false in production
```

그록은 정규 표현식 기반의 패턴을 동작합니다. 어떤 동작이 이루어지는지 이해하기 위해 모든 패턴을 수동으로 작성되었습니다. 이미 사용하고 있는 정규표현식을 재사용할 수 있습니다.

```yml
grok:
  additional_patterns:
   - 'METHOD [A-Z]+'
   - 'PATH [^ ]+'
   - 'NUMBER [0-9.]+'
```

이제 두 개의 메트릭을 갖게 됐습니다. 첫 메트릭은 주어진 레이블 `path` 를 갖는 카운터 형식의 `log_http_requests_total` 입니다.

```yml
metrics:
 - type: counter
   name: log_http_requests_total
   help: HTTP requests
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   labels:
     path: '{{.path}}'
```

두 번째 메트릭은 지연 시간을 측정하고 레이블을 갖지 않는 히스토그램 형식의 `log_http_request_latency_seconds` 입니다.

```yml
 - type: histogram
   name: log_http_request_latency_seconds_total
   help: HTTP request latency
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   value: '{{.latency}}'
```

마지막으로 익스포터가 메트릭을 게시하는 포트를 정의합니다.

```yml
server:
    port: 9144
```

http://localhost:9144 을 방문하면, 결과에 다음 메트릭을 확인할 수 잇습니다.

```shell
# HELP log_http_request_latency_seconds_total HTTP request latency
# TYPE log_http_request_latency_seconds_total histogram
log_http_request_latency_seconds_total_bucket{le="0.005"} 0
log_http_request_latency_seconds_total_bucket{le="0.01"} 0
log_http_request_latency_seconds_total_bucket{le="0.025"} 0
log_http_request_latency_seconds_total_bucket{le="0.05"} 0
log_http_request_latency_seconds_total_bucket{le="0.1"} 1
log_http_request_latency_seconds_total_bucket{le="0.25"} 2
log_http_request_latency_seconds_total_bucket{le="0.5"} 3
log_http_request_latency_seconds_total_bucket{le="1"} 3
log_http_request_latency_seconds_total_bucket{le="2.5"} 3
log_http_request_latency_seconds_total_bucket{le="5"} 3
log_http_request_latency_seconds_total_bucket{le="10"} 3
log_http_request_latency_seconds_total_bucket{le="+Inf"} 3
log_http_request_latency_seconds_total_sum 0.57
log_http_request_latency_seconds_total_count 3
# HELP log_http_requests_total HTTP requests
# TYPE log_http_requests_total counter
log_http_requests_total{path="/bar"} 1
log_http_requests_total{path="/foo"} 2
```

그록 익스포터는 일반적인 익스포터보다 더 밀접하게 구성과 얽혀 있습니다. 그록 익스포터는 게시하려는 메트릭을 각각 정의해야 하기 때문에 직접 계측에 가깝습니다.

일반적으로 모니터링하려는 어플리케이션 인스턴스당 하나의 그록 익스포터가 동작하며, Prometheus 는 아래 예제와 같은 일반적인 방법으로 메트릭을 수집합니다.

```yml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: grok
   static_configs:
    - targets:
       - localhost:9144
```

## Blackbox

각 어플리케이션 인스턴스마다 하나의 익스포터가 실행하도록 배치하는 것을 권장하지만, 기술적인 이유로 불가능한 경우도 있습니다. 일반적인 블랙박스 모니터링을 적용할 수 있는 경우입니다.

블랙박스 모니터링은 시스템 내부에 대한 특별한 정보 없이 시스템 외부에서 모니터링하는 방법입니다. 블랙박스 모니터링의 목적은 명백하게 잘못된 일이 발생한 경우 신속하게 알려주는 것이기 때문에 단위 테스트를 실행하는 경우에 수행하는 스모크테스트와 유사하게 생각할 수 있습니다.

웹 서비스가 사용자 입장에서 동작하는지를 모니터링하는 경우, 일반적으로 사용자가 사용하는 것과 같은 로드 밸런서 및 가상 IP 를 통해 모니터링하려 할 것입니다. 가상 IP 는 말 그대로 가상 IP 이기 때문에, 익스포터를 정확하게 실행할 수 없습니다. 따라서 별도의 아키텍처가 필요합니다.

Prometheus 에는 어플리케이션 인스턴스 옆에서 익스포터를 수행할 수 없는 두 가지 주요 사례에 대해 참조할 수 있는 **블랙박스 스타일(Blackbox-Style)** 이나 **SNMP 스타일(SNMP Style)** 의 익스포터 클래스가 있습니다. 일반적으로 블랙박스 익스포터는 네트워크상 실행 중인 어플리케이션 인스턴스가 없는 곳에서 실행될 필요가 있습니다.

네트워크 디바이스상 직접 작성된 코드를 실행하는 경우는 매우 드물기 때문에 SNMP 익스포터가 활용됩니다. 직접 작성된 코드를 실행할 수 있는 환경이라면, SNMP 익스포터 대신 노드 익스포터의 사용이 권장됩니다.

블랙박스 스타일 익스포터는 SNMP 와 달리 대상에 대한 구성 정보를 가져오는 것이 아니라 대상을 URL 파라미터 형식으로 사용하는 점에 차이가 있습니다.

그 밖의 다른 구성들은 일반적인 경우와 같이 익스포터가 사용자에 제공합니다. 이를 통해 서비스 검색 및 수집 스케줄링에 대한 Prometheus 의 역할과 메트릭을 Prometheus 가 이해할 수 있는 형식으로 변환하는 익스포터의 역할을 유지할 수 있습니다.

블랙박스 익스포터는 ICMP, TCP, HTTP 및 DNS 탐색을 지원합니다. 각각에 대해 순서대로 살펴볼 것이지만, 아래 예제와 같이 먼저 블랙박스 익스포터를 실행해야 합니다.

```shell
hostname $ wget https://github.com/prometheus/blackbox_exporter/releases/download/
    v0.12.0/blackbox_exporter-0.12.0.linux-amd64.tar.gz
hostname $ tar -xzf blackbox_exporter-0.12.0.linux-amd64.tar.gz
hostname $ cd blackbox_exporter-0.12.0.linux-amd64/
hostname $ sudo ./blackbox_exporter
level=info ... msg="Starting blackbox_exporter" version="(version=0.12.0,
    branch=HEAD, revision=4a22506cf0cf139d9b2f9cde099f0012d9fcabde)"
level=info ... msg="Loaded config file"
level=info ... msg="Listening on address" address=:9115
```

웹 브라우저에 http://localhost:9115/ 에 접근하면 `Example 1` 과 같은 상태 페이지를 확인할 수 있습니다.

> Example 1 - The Blackbox exporter’s status page

![image](https://user-images.githubusercontent.com/44635266/82142300-43d7cb00-9876-11ea-9937-4a670a5c4762.png)

### ICMP

**ICMP(Internetl Control Message Protocol)** 은 **IP(Internet Protocol)** 의 일부입니다. 블랙박스 익스포터의 컨텍스트에는 관심을 갖고 생각해야 하는 **에코 응답(Echo Reply)** 과 **에코 요청(Echo Request)** 메세지가 있으며 일반적으로 **핑(Ping)** 으로 알려져 있습니다.

웹 브라우저로 http://localhost:9115/probe?module=icmp&target=localhost 에 접속해서 블랙박스 익스포터가 로컬 호스트로 핑을 전송하도록 요청하면 다음과 같은 출력 결과를 확인할 수 있습니다.

```shell
# HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup
    in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.000164439
# HELP probe_duration_seconds Returns how long the probe took to complete
    in seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.000670403
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 4
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 1
```

가장 중요한 메트릭은 탐색이 성공한 경우 1 을, 그렇지 않을 경우 0 을 반환하는 `probe_success` 입니다. 이 메트릭은 `consul_up` 과 유사하며 알림이 발생한 경우 `up` 이나 `probe_success` 가 0 은 아닌지 확인해야 합니다.

모든 유형의 탐색에 대해 생성되는 유용한 또 다른 메트릭도 있습니다. `probe_ip_protocol` 은 사용되는 IP 프로토콜을 표시하며, 앞의 예제에는 IPv4 가 사용됩니다. `probe_duration_seconds` 는 DNS 해석을 포함한 전체 탐색에 걸린 시간을 표시합니다.

*blackbox.yml* 내부를 살펴보면, icmp 모듈을 찾을 수 있습니다.

```yml
icmp:
  prober: icmp
```

이는 icmp 로 불리는 모듈이 있다는 의미이며, URL 에서 `?module=icmp` 로 요청할 수 있습니다. 이 모듈은 icmp 탐색을 사용하며 추가적인 옵션이 지정되지는 않았습니다. ICMP 는 꽤 간단하므로, 필요에 따라 `dont_fragment` 나 `payload_size` 를 설정하면 됩니다.

다른 대상을 탐색할 수 있습니다. 예를 들어 웹 브라우저에서 http://localhost:9115/probe?module=icmp&target=www.google.com 에 접속하면 google.com 을 탐색할 수 있습니다. icmp 탐색에서 `target URL` 파라미터는 IP 주소나 호스트 이름입니다.

이번 탐색에서는 아래와 같은 출력과 함계 실패함을 확인할 수 있습니다.

```shell
# HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup
    in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.001169908
# HELP probe_duration_seconds Returns how long the probe took to complete
    in seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.001397181
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 6
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 0
```

이 예제에는 `probe_success` 가 0 이며, 이는 탐색이 실패했음을 의미합니다. 또한 `proble_ip_protocol` 이 6 이며 IPv6 를 의미합니다. 이 예제에서 사용된 머신은 IPv6 를 사용합니다.

블랙박스 익스포터를 확인할 때, 대상이 IPv6 를 가지고 있는 경우, IPv6 를 선호하며 이를 반환합니다. 그렇지 않은 경우만 IPv4 주소를 반환합니다. google.com 은 둘 다 가지고 있으므로 IPv6 가 선택되엇으며 예제의 머신에서 탐색은 실패했습니다.

`&debuog=True` 를 URL 끝에 추가해서 http://localhost:9115/probe?module=icmp&target=www.google.com&debug=true 로 접속하면 자세한 내용을 확인할 수 있으며 다음과 같은 내용이 출력됩니다.

```shell
Logs for the probe:
... module=icmp target=www.google.com level=info
        msg="Beginning probe" probe=icmp timeout_seconds=9.5
... module=icmp target=www.google.com level=info
        msg="Resolving target address" preferred_ip_protocol=ip6
... module=icmp target=www.google.com level=info
        msg="Resolved target address" ip=2a00:1450:400b:c03::63
... module=icmp target=www.google.com level=info
        msg="Creating socket"
... module=icmp target=www.google.com level=info
        msg="Creating ICMP packet" seq=10 id=3483
... module=icmp target=www.google.com level=info
        msg="Writing out packet"
... module=icmp target=www.google.com level=warn
        msg="Error writing to socket" err="write ip6 ::->2a00:1450:400b:c03::63:
        sendto: cannot assign requested address"
... module=icmp target=www.google.com level=error
        msg="Probe failed" duration_seconds=0.008982345

Metrics that would have been returned:
# HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup
    in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.008717006
# HELP probe_duration_seconds Returns how long the probe took to complete in
    seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.008982345
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 6
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 0

Module configuration:
prober: icmp
```

디버그 출력은 광범위하기 때문에, 이를 유의해서 읽으면 탐색이 실제로 하는 일을 정확하게 이해할 수 있습니다. 이 예제에서 발생한 오류는 sendto 시스템 콜이 IPv6 주소를 할당하지 못해 발생했습니다. IPv4 주소를 선호한다면 *blackbox.yml* 에 `preferred_ip_protocol: ipv4` 옵션을 설정한 새로운 모듈을 추가할 수 잇습니다.

```yml
  icmp_ipv4:
    prober: icmp
    icmp:
      preferred_ip_protocol: ip4
```

블랙박스 익스포터를 재시작한 후 http://localhost:9115/probe?module=icmp_ipv4&target=www.google.com 을 통해 icmp_ipv4 모듈을 사용하면 IPv4 로 동작할 것입니다.

### TCP

TCP / IP 의 TCP 는 **전송 제어 프로토콜(Transmission Control Protocol)** 입니다. 웹 사이트의 HTTP, 이메일의 SMTP, 원격 접속을 위한 Telnet, SSH 등 많은 표준이 TCP 를 사용합니다.

블랙박스 익스포터의 `tcp` 탐색은 TCP 서비스를 확인하고 명령행 기반의 텍스트 프로토콜을 사용해 간단한 통신이 가능하도록 지원합니다.

http://localhost:9115/probe?module=tcp_connect&target=localhost:22 로 접속하면 로컬 SSH 서버가 22 번 포트로 서비스 중이란 사실을 확인할 수 있습니다.

```shell
# HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup
    in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.000202381
# HELP probe_duration_seconds Returns how long the probe took to complete in
    seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.000881654
# HELP probe_failed_due_to_regex Indicates if probe failed due to regex
# TYPE probe_failed_due_to_regex gauge
probe_failed_due_to_regex 0
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 4
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 1
```

이는 ICMP 탐색에 의해 메트릭이 생성되는 것과 유사하며, 탐색이 성공하면 `probe_success` 가 1 로 설정하는 것을 확인할 수 있습니다. *blackbox.yml* 에 `tcp_connect` 모듈의 정의는 다음과 같습니다.

```yml
  tcp_connect:
    prober: tcp
```

이 모듈은 대상에 접속을 시도할 것이고, 연결이 성공됨을 확인하는 즉시 연결을 종료할것입니다. `ssh_banner` 모듈은 조금 더 나아가 원격 서버의 특정 응답까지 확인합니다.

```yml
  ssh_banner:
    prober: tcp
    tcp:
      query_response:
      - expect: "^SSH-2.0-"
```

SSH 세션의 최초 부분은 일반 텍스트이므로, 이 부분에 관한 내용은 tcp 탐색으로 확인할 수 있습니다. TCP 포트가 활성화되어 있는지 여부만이 아니라 서버가 SSH 배너로 응답하는지도 확인할 수 있기 때문에 `tcp_connect` 보다 더 낫습니다.

서버가 무언가 다른 내용을 반환한다면, expect 정규 표현식이 일치하지 않으 `probe_success` 는 0 이 될것입니다. 그리고 `probe_failed_due_to_regex` 는 1 이 될 것입니다. Prometheus 는 메트릭 기반 시스템이기 때문에, 전체 디버그 출력은 이벤트 로깅처럼 저장되지 않을 것입니다. 그러나 블랙박스 익스포터는 실제 발생한 내용에 무엇이 잘못되었는지 확인하는 데 필요한 메트릭을 일부 제공합니다.

`tcp` 탐색은 TLS 를 통해 연결할 수 있습니다. *blackbox.yml* 에 `tcp_connect_tls` 옵션을 다음과 같이 추가합니다.

```yml
  tcp_connect_tls:
    prober: tcp
    tcp:
      tls: true
```

블랙박스 익스포터를 재시작한 후 http://localhost:9115/probe?module=tcp_connect_tls&target=www.robustperception.io:443 으로 접속하면 www.robustperception.io 웹 사이트가 HTTPS 로 접속 가능한지 여부를 확인할 수 있습니다.

`tcp` 탐색에 `target` URL 파라미터는 IP 주소나 호스트 이름이며 콜론 다음에 포트 번호가 표시됩니다.

메트릭 출력에는 다음과 같은 내용을 확인할 수 있습니다.

```shell
# HELP probe_ssl_earliest_cert_expiry Returns earliest SSL cert expiry date
# TYPE probe_ssl_earliest_cert_expiry gauge
probe_ssl_earliest_cert_expiry 1.522039491e+09
```

`probe_ssl_ealiest_cert_expiry` 는 탐색시 추가적으로 생성되며 TLS / SSL 인증이 만료될 예정인 경우에 발생합니다. 이는 인증이 실제로 만료되기 전에 확인하는 데 사용할 수 있습니다.

HTTP 는 `tcp` 탐색을 사용할 수 있는 명령행 기반 텍스트 프로토콜이지만 `http` 탐색에 사용하는 것이 목적에 더 적합합니다.

### HTTP

**하이퍼 텍스트 전송 프로토콜(HyperText Transfer Protocol)** 은 모든 현대 웹의 기반이며 제공되는 대부분의 서비스에 사용되고 있습니다. 웹 어플리케이션에 대한 대부분의 모니터링은 HTTP 를 통해 메트릭을 수집하는 Prometheus 에 수행되는 것이 가장 좋지만, 때로 HTTP 서비스의 블랙박스 모니터링을 수행할 수 있습니다.

`http` 탐색은 `target` URL 파라미터에 URL 정보를 가집니다. http://localhost:9115/probe?module=http_2xx&target=https://www.robustperception.io 를 방문하면, `http_2xx` 모듈을 사용해 HTTPS 로 내 회사의 홈페이지를 확인할 수 있으며, 다음과 유사한 결과를 생성합니다.

```shell
# HELP probe_dns_lookup_time_seconds Returns the time taken for probe dns lookup
    in seconds
# TYPE probe_dns_lookup_time_seconds gauge
probe_dns_lookup_time_seconds 0.00169128
# HELP probe_duration_seconds Returns how long the probe took to complete in
    seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds 0.191706498
# HELP probe_failed_due_to_regex Indicates if probe failed due to regex
# TYPE probe_failed_due_to_regex gauge
probe_failed_due_to_regex 0
# HELP probe_http_content_length Length of http content response
# TYPE probe_http_content_length gauge
probe_http_content_length -1
# HELP probe_http_duration_seconds Duration of http request by phase, summed over
    all redirects
# TYPE probe_http_duration_seconds gauge
probe_http_duration_seconds{phase="connect"} 0.018464759
probe_http_duration_seconds{phase="processing"} 0.132312499
probe_http_duration_seconds{phase="resolve"} 0.00169128
probe_http_duration_seconds{phase="tls"} 0.057145526
probe_http_duration_seconds{phase="transfer"} 6.0805e-05
# HELP probe_http_redirects The number of redirects
# TYPE probe_http_redirects gauge
probe_http_redirects 0
# HELP probe_http_ssl Indicates if SSL was used for the final redirect
# TYPE probe_http_ssl gauge
probe_http_ssl 1
# HELP probe_http_status_code Response HTTP status code
# TYPE probe_http_status_code gauge
probe_http_status_code 200
# HELP probe_http_version Returns the version of HTTP of the probe response
# TYPE probe_http_version gauge
probe_http_version 1.1
# HELP probe_ip_protocol Specifies whether probe ip protocol is IP4 or IP6
# TYPE probe_ip_protocol gauge
probe_ip_protocol 4
# HELP probe_ssl_earliest_cert_expiry Returns earliest SSL cert expiry in
    unixtime
# TYPE probe_ssl_earliest_cert_expiry gauge
probe_ssl_earliest_cert_expiry 1.522039491e+09
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 1
```

`probe_success` 이외에 상태 코드, HTTP 버전 및 HTTP 요청의 여러 단계에 대한 타이밍 등 디버깅에 유용한 다수의 메트릭을 볼 수 있습니다.

`http` 탐색은 요청이 만들어지는 방법과 어떤 응답이 성공으로 간주되는지에 영향을 미치는 많은 옵션을 갖고 있습니다. HTTP 인증 헤더와 POST 본문을 지정한 다음, 응답 메세지에서 상태 코드와 HTTP 버전, **본문(body)** 이 수용 가능한지 확인합니다.

예를 들어 사용자가 http://www.robustperception.io 로 접속하면 HTTPS 웹 사이트로 상태 코드 200 과 함께 리다이렉트되고, 본문에 Prometheus 가 있는지 테스트할 수 있습니다. 다음과 같은 모듈을 생성해 확인할 수 있습니다.

```yml
  http_200_ssl_prometheus:
    prober: http
    http:
      valid_status_codes: [200]
      fail_if_not_ssl: true
      fail_if_not_matches_regexp:
        - Prometheus
```

웹 브라우저에 http://localhost:9115/probe?module=http_200_ssl_prometheus&target=http://www.robustperception.io 에 접속하면 `probe_success` 가 1 이고 이 모듈이 동작하는 것을 확인할 수 있습니다. 동일한 요청을 http://prometheus.io 에 전송하고 싶으면 웹 브라우저에서 http://localhost:9115/probe?module=http_200_ssl_prometheus&target=​http://prometheus.io 에 접속하면 됩니다.

블랙박스 익스포터의 각 모듈은 http://www.robustperception.io 와 http://prometheus.io 에 대해 확인한 것처럼, `target` URL 파라미터를 변경해가며 다양한 대상에 수행할 수 있는 상세한 테스트입니다. 예를 들어, 웹 사이트에서 제공하는 각 프론트엔드 어플리케이션 인스턴스가 올바른 결과를 반환하는지 확인할 수 있습니다. 다양한 서비스에 각기 다른 테스트가 필요하다면, 각 서비스에 대한 모듈을 생성할 수 있습니다. URL 파라미터로 모듈을 오버라이드할 수 없다면, 블랙박스 익스포터는 개방형 프록시가 될 수 있으며, Prometheus 익스포터 사이의 역할 분할에도 혼란을 줄 수 있습니다.

`http` 탐색은 블랙박스 익스포터의 탐색 방법 중 구성 가능한 내용이 가장 많습니다. `http` 탐색은 유연하지만 상대적으로 간단한 HTTP 탐색이기 때문에, 블랙박스 익스포터가 모든 사용 예를 다룰 수는 없습니다. 좀 더 정교한 무언가가 필요하다면, 직접 익스포터를 작성하거나 웹 브라우저에서 URL 접속을 시뮬레이션할 수 있는 웹드라이버 익스포터 같은 기존 익스포터의 장점을 확인할 수 있습니다.

### DNS

`dns` 탐색은 주로 DNS 서버를 테스트하기 위해 사용합니다. 예를 들어 DNS 복제가 결과를 반환하는지 확인할 수 있습니다.

DNS 서버가 TCP 상에서 응답을 하는지 테스트하려면, *blackbox.yml* 에 다음과 같은 모듈을 생성할 수 있습니다.

```yml
  dns_tcp:
    prober: dns
    dns:
      transport_protocol: "tcp"
      query_name: "www.prometheus.io"
```

블랙박스 익스포터를 재시작한 다음, 구글 퍼블릭 DNS 서비스가 TCP 로 동작하는지 확인하기 위해 http://localhost:9115/probe?module=dns_tcp&target=8.8.8.8 로 접속해 볼 수 있습니다. `target` URL 파라미터는 DNS 서버로 설정하고 `query_name` 은 DNS 서버로 전송할 DNS 요청을 의미합니다. 이 요청은 명령행에서 `dig -tcp @8.8.8.8 www.prometheus.io` 를 수행하는 것과 같습니다.

`dns` 탐색에 `target` URL 파라미터는 IP 주소나 호스트 이름이고 콜론 다음에 포트번호가 표시됩니다. 포트번호 없이 IP 주소나 호스트 이름만 표시할 수 있는데, 이 경우 DNS 포트인 53 번 포트가 사용됩니다.

DNS 서버의 테스트 외에도, dns 탐색을 이용해 DNS 해석을 통해 특정 결과가 반환되는지 확인할 수 있습니다. 하지만 일반적으로 HTTP 나 TCP, ICMP 를 통한 서비스와 통신하기 원하며, HTTP 나 TCP, ICMP 탐색의 결과를 통해 추가 비용 없이 DNS 를 확인하는 것이 더 상식적입니다.

특정 결과를 확인하기 위해 `dns` 탐색을 사용하는 예는 MX 기록이 나타나지 않음을 확인하는 것입니다.

이를 위해 *blackbox.yml* 에 다음과 같이 새로운 모듈을 생성할 수 있습니다.

```yml
  dns_mx_present_rp_io:
    prober: dns
    dns:
      query_name: "robustperception.io"
      query_type: "MX"
      validate_answer_rrs:
        fail_if_not_matches_regexp:
          - ".+"
```

블랙박스 익스포터를 재시작한 다음, http://localhost:9115/probe?module=dns_mx_present_rp_io&target=8.8.8.8 에 접속하면 robustperception.io 에 MX 기록이 나타나는걸 확인할 수 있습니다. `query_name` 은 모듈별로 명시되어야 하는 것을 고려하면, 확인하려는 모든 도메인에 대해 모듈을 만들어야 합니다. 이 예제에는 구글 퍼블릭 DNS 8.8.8.8 을 퍼블릭 DNS 해석기로 사용했으나 로컬 해석기를 사용할 수 있습니다.

`dns` 탐색에는 권한 및 추가 레코드 같은 DSN 응답 측면에서 확인하는 데 도움이 되는 기능이 많이 있습니다.

### Prometheus Configuration

블랙박스 익스포터는 `/probe` 엔드포인트에서 `module` 과 `target` URL 파라미터를 사용합니다. `params` 와 `metrics_path` 를 사용해 이 사항들을 제공할 수 있지만, 대상마다 수집 구성을 해야 하므로 Prometheus 의 서비스 검색 기능이라는 장점을 누리지 못하는 점에서 번거로운 일이 생길 수 있습니다.

레이블 재지정을 통해 `__param_<name>` 레이블을 URL 파라미터로 제공할 수 있으므로 서비스 검색의 장점을 활용할 수 있다는 점은 좋은 점입니다.

뿐만아니라, `instance` 와 `__address__` 구별되는 값이기 때문에 Prometheus 가 실제 대상의 `instance` 레이블을 가지는 동안은 블랙박스 익스포터와 통신할 수 있습니다. 아래 예제는 이 내용에 대한 예입니다.

```yml
scrape_configs:
 - job_name: blackbox
   metrics_path: /probe
   params:
     module: [http_2xx]
   static_configs:
    - targets:
       - http://www.prometheus.io
       - http://www.robustperception.io
       - http://demo.robustperception.io
   relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: 127.0.0.1:9115
```

코드를 나눠서 살펴보겠습니다.

```yml
 - job_name: 'blackbox'
   metrics_path: /probe
   params:
     module: [http_2xx]
```

기본 `job` 레이블과 사용자 정의 경로, 그리고 하나의 URL 파라미터가 지정되었습니다.

```yml
   static_configs:
    - targets:
      - http://www.prometheus.io
      - http://www.robustperception.io
      - http://demo.robustperception.io
```

탐색 대상이 될 3 개의 웹사이트입니다.

```yml
   relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: 127.0.0.1:9115
```

`relabel_configs` 를 설정하는 부분이 바로 엄청난 일이 일어나는 곳입니다. 먼저, `__address__` 레이블은 `target` URL 파라미터가 되고, 두 번째로 `instance` 레이블이 됩니다.

이 시점에서 `instance` 레이블과, `target` URL 파라미터는 적합한 값을 가지지만, `__address__` 는 여전히 블랙박스 익스포터가 아닌 하나의 URL 입니다.

마지막으로 레이블 재지정 동작을 통해 블랙박스 익스포터의 호스트 주소와 포트 번호를 `__address__` 에 설정합니다.

이러한 구성으로 Prometheus 를 수행하면 `Example 2` 같은 대상 상태 페이지를 볼 수 있습니다. 엔드포인트에는 필요한 URL 파라미터가 있고 인스턴스 레이블은 URL 입니다.

> Example 2 - The Blackbox exporter’s status page

![image](https://user-images.githubusercontent.com/44635266/82895425-2cdc5b80-9f8f-11ea-896e-9875b9b99592.png)

이 방법은 `static_configs` 에 국한된 것은 아닙니다. 임의의 다른 서비스 검색 메커니즘에도 사용 가능합니다. 예를 들어 아래 예제에서 컨설에 등록된 모든 노드에 대해 SSH 가 응답하는지 확인합니다.

```yml
scrape_configs:
 - job_name: node
   metrics_path: /probe
   params:
     module: [ssh_banner]
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_address]
      regex: '(.*)'
      replacement: '${1}:22'
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: 127.0.0.1:9115
```

이 방법의 강점은 `/metrics` 를 수집하는 것뿐만 아니라 어플리케이션의 블랙박스 모니터링까지 할 수 있도록 서비스 검색을 재사용할 수 있는 점입니다.