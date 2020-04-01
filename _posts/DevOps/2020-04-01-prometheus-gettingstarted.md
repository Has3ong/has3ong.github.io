---
title : Prometheus Getting Started with Prometheus
tags :
- Alert
- Node Exporter
- Expression Browser
- Getting Started
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

## Running Prometheus 

Prometheus 는 https://prometheus.io/download/ 에 접속해서 리눅스 운영체제를 지원하는 Prometheus 를 내려받을 수 있습니다.

> Example 1 - Part of the Prometheus download page. The Linux/amd64 version is in the middle.

![image](https://user-images.githubusercontent.com/44635266/77849550-6d299280-7207-11ea-954e-e2bd8f552d8f.png)

현재 Prometheus 2.2.1 버전을 사용하고 파일 이름은 *prometheus-2.2.1.linux-amd64.tar.gz* 입니다.

해당 파일을 내려받은 **타르볼(Tarball)** 파일의 압축을 해제하고, 해당 디렉토리를 보겠습니다.

```shell
hostname $ tar -xzf prometheus-*.linux-amd64.tar.gz
hostname $ cd prometheus-*.linux-amd64/
```

이제 아래 내용이 포함이 되도록 *prometheus.yml* 파일을 변경해 보겠습니다.

```yaml
global:
    scrape_interval: 10s
scrape_configs:
    - job_name: prometheus
    static_configs:
        - targets:
        - localhost:9090
```

기본적으로 Prometheus 는 TCP 포트 9090 에서 작동하며, 10 초에 1 번씩 정보를 수집하도록 구성되어 있습니다. 이제 `./Prometheus` 명령을 수행하여 Prometheus 를 실행해 보겠습니다.

```shell
hostname $ ./prometheus
level=info ... msg="Starting Prometheus" version="(version=2.2.1, branch=HEAD,
    revision=bc6058c81272a8d938c05e75607371284236aadc)"
level=info ... build_context="(go=go1.10, user=root@149e5b3f0829,
    date=20180314-14:15:45)"
level=info ... host_details="(Linux 4.4.0-98-generic #121-Ubuntu..."
level=info ... fd_limits="(soft=1024, hard=1048576)"
level=info ... msg="Start listening for connections" address=0.0.0.0:9090
level=info ... msg="Starting TSDB ..."
level=info ... msg="TSDB started"
level=info ... msg="Loading configuration file" filename=prometheus.yml
level=info ... msg="Server is ready to receive web requests."
```

Prometheus 가 실행되면 버전, 머신의 상세 정보등 여러가지 정보가 출력이 됩니다. 이제 웹 브라우저에서 http://localhost:9090 으로 접속하면 `Example 2` 와 같이 Prometheus UI 에 접속할 수 있습니다.

> Example 2 - The Prometheus expression browser

![image](https://user-images.githubusercontent.com/44635266/77849716-9f87bf80-7208-11ea-88ca-d76d9ad87811.png)

`Example 2` 는 PromQL 쿼리를 수행할 수 있는 수식 브라우저를 보여줍니다. 그 외에도 Status 탭 하위에 있는 Targets 페이지(`Example 3`) 처럼 Prometheus 가 수행하는 작업을 파악할 수 있는 여러 웹 페이지들이 제공됩니다.

> Example 3 - The target status page

![image](https://user-images.githubusercontent.com/44635266/77849718-a8789100-7208-11ea-951b-4d558edcc5fd.png)

`Example 3` 의 페이지에선 최근의 데이터 수집이 성공했음을 의미하는 가동 상태인 하나의 Prometheus 서버만이 표시되어 있습니다. 만약 데이터를 수집하는 데 문제가 발생하면, 오류 항목에 어떤 메세지가 떴을 것입니다.

살펴볼 또 다른 웹 페이지는 Prometheus `/metrics` 페이지입니다. Prometheus 자체가 Prometheus 메트릭으로 계측되는 것은 놀라울 일이 아닙니다. 이러한 메트릭들은 http://localhost:9090/metrics 로 접근하면 볼 수 있으며 `Example 4` 처럼 가독성이 좋습니다.

> Example 4 - The first part of Prometheus’s /metrics

![image](https://user-images.githubusercontent.com/44635266/77849721-b201f900-7208-11ea-9fcc-95892207ebc1.png)

`metrics` 페이지에는 Prometheus 코드에 대한 메트릭뿐 아니라 Go 런타임과 프로세스에 관한 내용도 포함되어 있습니다.

## Using the Expression Browser 

수식 브라우저는 **애드혹 쿼리(ad hoc query)** 를 수행하고, PromQL 표현식을 작성하며, Prometheus 내부의 PromQL 쿼리 및 데이터를 디버깅하는 데 유용합니다.

수식 브라우저를 시작하려면 먼저 `Console` 뷰로 이동해서 표현식 `up` 을 입력한 다음 `Execute` 버튼을 클릭합니다.

`Example 5` 를 보면 `up{instance="localhost:9090", job="prometheus"}` 라는 항목에 1 의 값을 가지는 결과가 하나 있습니다. `up` 은 데이터를 수집할 때 Prometheus 가 추가하는 특별한 형태의 메트릭이며, 수집이 성공했을 때 1 로 표시됩니다. 

`instance` 는 수집한 대상을 나타내는 레이블입니다. 이 경우 Prometheus 자체를 나타냅니다. `Example 5` 는 Prometheus 가 자신에 대한 데이터를 수집했고 성공했음을 의미합니다.

> Example 5 - The result of up in the expression browser

![image](https://user-images.githubusercontent.com/44635266/77914461-eb9e3700-72d0-11ea-9b66-c438edd75b43.png)

여기에 표시된 `job` 레이블은 *prometheus.yml* 의 `job_name` 항목에서 따왔습니다. Prometheus 가 마법처럼 Prometheus 에 대한 데이터를 수집했음을 알아채서 자동으로 `job` 레이블을 `prometheus` 라는 값으로 설정할 수 있는것은 아닙니다.

오히려 사용자가 설정을 생성해야 하는 것이 규칙입니다. `job` 레이블은 어플리케이션의 형식을 나타냅니다.

아래 `Example 6` 처럼 `process_resident_memory_bytes` 항목을 확인해보겠습니다.

> Example 6 - The result of process_resident_memory_bytes in the expression browser

![image](https://user-images.githubusercontent.com/44635266/77914506-007aca80-72d1-11ea-88ed-b50cf7d3c55c.png)

이 예제의 Prometheus 는 약 44 MB 메모리를 사용합니다. 이 메트릭은 Byte 로 표시돼어있습니다.

서로 다른 환경에서는 동일한 이진값조차 서로 다른 **차수(magnitude)** 로 해석되어 값이 달라질 수 있습니다. 내부 RPC 는 몇 마이크로초가 걸릴 수 있고, 장기 프로세스는 며칠이 걸릴 수 있습니다. 따라서 Prometheus 의 규칙은 Byte 나 초 같은 기본 단위를 사용합니다.

현재의 메모리 사용량을 파악하는 것도 중요하지만 시간에 따라 메모리 사용량이 어떻게 변화하는지 살펴보는것도 중요합니다. 시간에 따른 메모리 사용량의 변화를 확인하기 위해 `Example 7` 처럼 `Graph` 를 클릭해 그래프 뷰로 이동해보겠습니다.

> Example 7 - A graph of process_resident_memory_bytes in the expression browser

![image](https://user-images.githubusercontent.com/44635266/77914529-083a6f00-72d1-11ea-85d2-ea9c8816fd7e.png)

`process_resident_memory_bytes` 같은 메트릭을 **게이지(Gauge)** 라고 부릅니다. 게이지에서는 특정 시점의 절댓값이 중요한 의미를 가집니다. 메트릭의 두 번째 주요 타입은 **카운터(Counter)** 입니다. 카운터는 얼마나 많은 이벤트가 발생했는지와 이벤트의 전체 크기는 얼마나 되는지를 추적합니다.

Prometheus 가 모은 샘플의 수를 나타내는 `prometheus_tsdb_head_samples_appended_total` 의 그래프를 작성해 카운터를 확인해보겠습니다.

> Example 8 - A graph of prometheus_tsdb_head_samples_appended_total in the expression browser

![image](https://user-images.githubusercontent.com/44635266/77914815-6b2c0600-72d1-11ea-8332-4cd72abdf4a2.png)

카운터는 항상 증가합니다. 여기서 중점적으로 보는 정보는 카운터 값이 얼마나 빨리 증가하는지이며, 이럴 때 `rate` 함수가 필요합니다. `rate` 함수는 초당 카운터 값이 얼마나 빨리 증가하는지 계산합니다.

이전 표현식을 `rate(prometheus_tsdb_head_samples_appended_total[1m])` 로 바구면 1 분 동안 평균적으로 초당 몇 개의 샘픙르 저장하는지 계산하고, 그 결과를 `Example 9` 처럼 보여줍니다.

> Example 9 - A graph of rate(prometheus_tsdb_head_samples_appended_total[1m]) in the expression browser

![image](https://user-images.githubusercontent.com/44635266/77915031-c2ca7180-72d1-11ea-9b64-8a85d66b9e4a.png)

`Example 9` 에서는 Prometheus 가 초당 68 개 정도의 샘플을 저장하는 것을 확인할 수 있습니다.

## Running the Node Exporter 

**노드 익스포터(Node Exporter)** 는 리눅스와 같은 유닉스 계열 시스템에서 커널이나 머신 레벨의 메트릭을 표시합니다. 노트 익스포터는 CPU, 메모리, 디스크 공간, 네트워크 대역폭 같은 표준 메트릭을 제공합니다.

노드 익스포터를 실행해보겠습니다.

```shell
hostname $ tar -xzf node_exporter-*.linux-amd64.tar.gz
hostname $ cd node_exporter-*.linux-amd64/
hostname $ ./node_exporter
INFO[0000] Starting node_exporter (version=0.16.0, branch=HEAD,
 revision=d42bd70f4363dced6b77d8fc311ea57b63387e4f)
 source="node_exporter.go:82"
INFO[0000] Build context (go=go1.9.6, user=root@a67a9bc13a69,
 date=20180515-15:52:42)
 source="node_exporter.go:83"
INFO[0000] Enabled collectors: source="node_exporter.go:90"
INFO[0000] - arp source="node_exporter.go:97"
INFO[0000] - bacahe source="node_exporter.go:97"
...
various other collectors
...
INFO[0000] Listening on :9100 source="node_exporter.go:111"
```

이제 웹 브라우저 http://localhost:9100/ 에 접근하면 노트 익스포터에 접속할 수 있고 `/metrics` 페이지로 이동할 수 있습니다.

Prometheus 가 노드 익스포터를 모니터링하려면 *prometheus.yml* 파일에 `scrape_configs` 항목을 추가해야 합니다.

```yml
global:
    scrape_interval: 10s
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
          - localhost:9090
  - job_name: node
    static_configs:
      - targets:
        - localhost:9100
```

Prometheus 를 종료하고 디사 시작하여 새로운 설정이 적용됩니다. `Targets` 페이지를 보면 `Example 10` 과 같이 `UP` 상태인 대상 2 개를 확인할 수 있습니다.

> Example 10 - The target status page with Node exporter

![image](https://user-images.githubusercontent.com/44635266/78021595-75f8a080-738e-11ea-8c62-a0eb773e67e9.png)

수식 브라우저의 콘솔 뷰를 통해 `up` 명령을 수행해보면 `Example 11` 과 같이 두 개의 항목이 표시됩니다.

> Example 11 - There are now two results for up

![image](https://user-images.githubusercontent.com/44635266/78021618-7e50db80-738e-11ea-9378-65995ff3ddad.png)

더 많은 작업과 `scrape_configs` 를 추가하더라도, 동일한 시간에 서로 다른 작업으로부터의 동일한 메트릭을 참조하고자 하는일은 거의 없습니다. 예를 들어 Prometheus 와 노드 익스포터의 메모리 사용량은 상관 관계가 없는데, 이와 같이 서로 무관한 데이터로 인해 디버깅이 어려워집니다.

이런 이유로, 노드 익스포터의 메모리 사용량에 대해서만 `process_resident_memory_bytes{job="node"}` 표현식을 사용해 그래프를 그릴 수 있습니다. `job="node"` 로 구분된 부분을 **레이블 매처(Label Matcher)** 라 하며 `Example 12` 에서 보듯이 반환되는 메트릭을 레이블이 제한합니다.

> Example 12 - A graph of the resident memory of just the Node exporter

![image](https://user-images.githubusercontent.com/44635266/78022371-c9b7b980-738f-11ea-97b7-77fee10e5a64.png)

`process_resident_memory_bytes` 는 노드 익스포터가 설치된 머신 전체의 메모리가 아니라 노드 익스포터 프로세스가 사용하고 있는 메모리 크기입니다.

마지막 예제에서 `Graph` 뷰에서 `rate(node_network_receive_bytes_total[1m])` 를 계산하고 `Example 13` 과 같은 그래프를 만듭니다.

> Example 13 - A graph of the network traffic received on several interfaces

![image](https://user-images.githubusercontent.com/44635266/78022414-d805d580-738f-11ea-91ff-070a63549634.png)

`node_network_receive_bytes_total` 은 네트워크 인터페이스에 수신된 데이터를 Byte 단위로 표시하는 카운터 값입니다. 노드 익스포터는 자동으로 모든 네트워크 인터페이스를 선택하며, 선택된 인터페이스들은 PromQL 에서 하나의 그룹으로 처리될 수 있습니다.

이것은 알림을 표시할 때 유용한데, 알림을 받기 원하는 모든 메트릭에 대한 레이블을 일일이 나열할 필요는 없습니다.

## Alerting 

**알림(Alert)** 두 부분으로 나뉩니다.

첫 부분은 Prometheus 에 알림 규칙을 추가하고 알림을 구성하는 로직을 정의합니다. 두 번째 부분은 발생된(Firing) 알림들을 **알림매니저(AlertManager)** 가 이메일이나 무선 호출, 채팅메세지로 변경합니다.

알림을 받는 조건을 만들어보겠습니다. 노드 익스포터를 중지시킨뒤 다음 수집이 진행되고 나면, `Targets` 페이지에서는 노드 익스포터와 연결된 TCP 포트로 아무것도 수신되지 않고, 이로 인해 HTTP 요청이 전달되지 않기 때문에 **연결 거부(Connection Refused)** 오류와 함께 `DOWN` 상태로 표시됩니다.

> Example 14 - The target status page showing the Node exporter as down

![image](https://user-images.githubusercontent.com/44635266/78022440-e2c06a80-738f-11ea-9029-16c651db0571.png)

`down` 상태의 인스턴스에 대해 `Targets` 페이지를 수동으로 확인하는 것은 시간 낭비입니다. 다행스럽게도 `up` 메트릭은 든든한 지원군이 됩니다. 수식 브라우저의 `Console` 뷰에서 `up` 을 수행하면 `Example 15` 처럼 노드 익스포터 값이 0 이 되는 것을 볼 수 있습니다.

> Example 15 - up is now 0 for the Node exporter

![image](https://user-images.githubusercontent.com/44635266/78022454-ec49d280-738f-11ea-84b6-d1593868e49a.png)

알림 규칙을 작성하려면 받기 원하는 알림 결과를 반환하는 PromQL 표현식이 필요합니다. 이때는 `==` 연산자를 사용하면 편리합니다. `==` 연산자는 값이 일치하는 모든 시계열을 걸러냅니다.

만약 수식 브라우저에 `up == 0` 을 입력한다면 `Example 16` 처럼 `down` 상태의 인스턴스들만 반환합니다.

> Example 16

![image](https://user-images.githubusercontent.com/44635266/78022629-3f238a00-7390-11ea-8703-45cd4defa019.png)

다음은 이 표현식을 Prometheus 의 알림 규칙에 추가합니다. Prometheus 에게 어떤 알림매니저와 통신할것인지를 알려주어야 합니다. 이를 위해 *prometheus.yml* 에 관련 내용을 추가해야합니다.

```yml
global:
    scrape_interval: 10s
    evaluation_interval: 10s
rule_files:
    - rules.yml
alerting:
    alertmanagers:
      - static_configs:
          - targets:
              - localhost:9093
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
          - localhost:9090
  - job_name: node
    static_configs:
      - targets:
          - localhost:9100
```

새로운 *rules.yml* 파일을 작성하고 Prometheus 를 재시작해보겠습니다.

```yml
groups:
  - name: example
    rules:
      - alert: InstanceDown
        expr: up == 0
        for: 1m
```

`InstanceDown` 알림은 `evaluation_interval` 에 설정된 대로 10 초마다 1 번씩 확인됩니다. 만약 이 계열 값이 적어도 1 분정도 지속적으로 반환되면, 알림이 발생합니다.

필요한 시간(`for`) 이 될때까지 알림은 **보류(Pending)** 상태에 있을 것입니다. `Alert` 페이지에서 `Example 17` 과 같이 각 알림을 클릭해 알림의 레이블과 더 상세한 정보를 확인할 수 있습니다.

> Example 17 - A firing alert on the Alerts page

![image](https://user-images.githubusercontent.com/44635266/78023057-f28c7e80-7390-11ea-9b7b-14cd37c75581.png)

알림매니저를 다운받아 압축을 풀고 해당 디렉토리로 이동해보겠습니다.

```shell
hostname $ tar -xzf alertmanager-*.linux-amd64.tar.gz
hostname $ cd alertmanager-*.linux-amd64/
```

알림매니저의 통보 방식은 다양하지만, 별도 설정 없이 동작하는 대부분의 방식은 상용 서비스 제공자를 사용하는 것입니다. 이 방식은 시간이 자나면서 설정 절차가 변경되는 경향이 있습니다.

따라서 공개된 SMTP 스마트 호스트가 가능하다고 가정하겠습니다. *alertmanager.yml* 을 기반으로 `smtp_smarthost`, `smtp_from`, `to` 를 적용된 설정과 사용하는 이메일 주소에 맞게 수정해야 합니다.

```yml
global:
    smtp_smarthost: 'localhost:25'
    smtp_from: 'youraddress@example.org'
route:
    receiver: example-email
receivers:
  - name: example-email
    email_configs:
      - to: 'youraddress@example.org'    
```

`./alertmanager` 명령으로 알림매니저를 시작할 수 있습니다.

```shell
hostname $ ./alertmanager
level=info ... caller=main.go:174 msg="Starting Alertmanager"
 version="(version=0.15.0, branch=HEAD,
 revision=462c969d85cf1a473587754d55e4a3c4a2abc63c)"
level=info ... caller=main.go:175 build_context="(go=go1.10.3,
 user=root@bec9939eb862, date=20180622-11:58:41)"
level=info ... caller=cluster.go:155 component=cluster msg="setting advertise
 address explicitly" addr=192.168.1.13 port=9094
level=info ... caller=cluster.go:561 component=cluster msg="Waiting for
 gossip to settle..." interval=2s
level=info ... caller=main.go:311 msg="Loading configuration file"
 file=alertmanager.yml
level=info ... caller=main.go:387 msg=Listening address=:9093
level=info ... caller=cluster.go:586 component=cluster msg="gossip not settled"
 polls=0 before=0 now=1 elapsed=2.00011639s
level=info ... caller=cluster.go:578 component=cluster msg="gossip settled;
 proceeding" elapsed=10.000782554s
```

http://localhost:9093 로 접속해 알림매니저를 접속해보면 알림매니저에서 발생한 알림은 `Example 18` 과 비슷할 것입니다.

> Example 18 - A InstanceDown alert in the Alertmanager

![image](https://user-images.githubusercontent.com/44635266/78023476-ae4dae00-7391-11ea-840c-643929b28200.png)

만약 모든 설정이 다 되있고 정상적으로 동작한다면 1, 2 분 후 알림매니저로부터 `Example 19` 와 같은 형태로 이메일 통보가 수신되어야 합니다.

> Example 19 - An email notification for an InstanceDown alert

![image](https://user-images.githubusercontent.com/44635266/78023528-c1f91480-7391-11ea-9956-0b3f0c1a9d97.png)

*prometheus.yml* 에 더 많은 대상을 추가하면, 알림 역시 추가된 대상에 대해 자동으로 동작하게 됩니다.
