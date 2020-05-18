---
title : Prometheus Containers and Kubernetes
tags :
- Kubernetes
- Container
- Docker
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

Docker 와 Kubernetes 같은 기술들은 컨테이너 배포를 점점 더 보편화시킵니다. 

## cAdvisor

노드 익스포터가 머신에 대한 메트릭을 제공하는 것과 같은 방법으로, cAdvisor 익스포터는 `cgroups` 에 대한 메트릭을 제공합니다. `cgroups` 는 리눅스 커널 격리 기능으로서, 일반적으로 리눅스상의 컨테이너를 구현하기 위해 사용되며, `systemd` 같은 런타임 환경에서도 쓰입니다.

다음과 같이 cAdvisor 를 Docker 로 실행가능합니다.

```shell
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:v0.28.3
```

http://localhost:8080/metrics 를 접속하면 `Example 1` 과 같이 긴 메트릭 목록을 볼 수 있습니다.

컨테이너 메트릭은 `container_` 접두어를 가지며, 이들은 모두 `id` 레이블을 가지는 것을 알 수 있습니다. `/docker/` 로 시작하는 `id` 레이블은 Docker 와 Docker 컨테이너에서 나왔으며, `/user.slice/` 와 `/system.slice/`  로 시작하는 `id` 레이블을 가지는 경우 머신에서 실행되는 `systemd` 에서 나왔습니다. `cgroups` 를 사용하는 다른 소프트웨어가 있다면, 해당 소프트웨어의 `cgroups` 리스트도 만들어집니다.

> Example 1 - The start of a /metrics page from cAdvisor

![image](https://user-images.githubusercontent.com/44635266/80860569-62996780-8ca3-11ea-87ca-e3d60577c691.png)

이러한 메트릭은 *prometheus.yml* 을 통해 수집할 수 있습니다.

```yaml
scrape_configs:
 - job_name: cadvisor
   static_configs:
    - targets:
      - localhost:8080
```

### CPU

컨테이너 CPU 에 대한 메트릭은 `container_cpu_usage_seconds_total` 과 `container_cpu_system_seconds_total`, `container_cpu_user_seconds_total` 이 있습니다.

`container_cpu_usage_seconds_total` 는 CPU 에 의해 분할되지만, 모드에 의해서는 분할되지 않습니다. `container_cpu_system_seconds_total` 과 `container_cpu_user_seconds_total` 는 각각 시스템 모드와 사용자 모드이며, 노드 익스포터의 CPU 수집기와 비슷합니다. 이들 모두 `rate` 함수를 사용할 수 있는 카운터입니다.

### Memory

`container_memory_cache` 는 컨테이너가 사용하는 페이지 캐시로 바이트 단위입니다. `container_memory_rss` 는 메모리에 상주하는 세트의 크기로 바이트단위입니다. 이것은 동일한 RSS 나 프로세스가 사용하는 물리적인 메모리가 아니므로 매핑된 파일의 크기를 제외합니다. `container_memory_usage_bytes` 는 RSS 와 페이지 캐시이며, 0 으로 제한되지 않은 경우, `container_spec_memory_limit_bytes` 에 의해 제한됩니다. `container_memory_working_set_bytes` 는 `container_memory_usage_bytes` 에서 비활성 파일 기반 메모리를 빼서 계산합니다.

실제로 `container_memory_working_set_bytes` 는 게시된 RSS 에 가장 가깝습니다. 그리고 페이지 캐시를 포함하기 때문에, `container_memory_usage_bytes` 는 계속 감시하고 싶을 수 있습니다.

일반적으로 `cgroups` 의 메트릭보다 프로세스 자체의 `process_resident_memory_bytes` 같은 메트릭에 의존하는 것을 권장합니다. 어플리케이션이 Prometheus 메트릭을 게시하지 않는다면, cAdvisor 가 좋은 임시 방편입니다. 그리고 cAdvisor 메트릭들은 디버깅과 프로파일링에 여전히 중요합니다.

### Labels

`cgroups` 은 계층 구조의 루트에 `/` `cgroup` 을 가지는 계층 구조로 구조화되어 있습니다. 각각의 `cgroup` 의 메트릭들은 하위 `cgroup` 의 사용량을 포함합니다. 따라서 메트릭 내의 합계나 평균이 의미를 가지는 일반적인 규칙에 어긋납니다.

`id` 레이블 이외에도 `cAdvisor` 는 컨테이너가 있는 경우, 컨테이너에 대한 더 많은 레이블을 추가합니다. 실행되는 특정 Docker 이미지와 컨테이너의 Docker 이름에 대해 항상 `image` 와 `name` 레이블을 가집니다.

Docker 가 컨테이너에 대해 가지는 모든 메타데이터 레이블은 `container_label_` 접두어와 함께 포함됩니다. 이러한 임의의 레이블은 데이터 수집시 모니터링을 망칠 수 있으며, 아래 예제처럼 `labeldrop` 을 사용해 제거할 수 있습니다.

```yaml
scrape_configs:
 - job_name: cadvisor
   static_configs:
    - targets:
       - localhost:9090
   metric_relabel_configs:
    - regex: 'container_label_.*'
      action: labeldrop
```

## Kubernetes

Kubernetes 는 컨테이너 오케스트레이션 플랫폼입니다. Prometheus 처럼 Kubernetes 프로젝트는 **CNCF(Cloud Native Computing Foundation)** 의 일부입니다.

### Running in Kubernetes

단일 노드 Kubernetes 클러스터의 실행에 사용하는 도구인 **미니쿠베(Minikube)** 로 사용하겠습니다.

아래 예제를 따라하면됩니다.

```shell
hostname $ wget \
    https://storage.googleapis.com/minikube/releases/v0.24.1/minikube-linux-amd64
hostname $ mv minikube-linux-amd64 minikube
hostname $ chmod +x minikube
hostname $ ./minikube start
Starting local Kubernetes v1.8.0 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
Loading cached images from config file.
```

Kubernetes 클러스터와 상호작용하는 데 사용하는 명령행 도구인 `kubectl` 도 설치해야 합니다. 아래는 `kubectl` 을 설치하는 방법과 Kubernetes 클러스터와 통신하는지 확인하는 방법입니다.

```shell
hostname $ wget \
    https://storage.googleapis.com/kubernetes-release/release/v1.9.2/bin/linux/amd64
    /kubectl
hostname $ chmod +x kubectl
hostname $ ./kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   44s
```

아래는 미니쿠베에서 실행중인 Prometheus 를 확인하는 방법입니다. *prometheus-deployment.yml* 은 권한을 포함하고 있어, 클러스터에서 Prometheus 가 파드와 노드, Prometheus 구성 파일을 유지하기 위해 생성된 configMap, Prometheus 를 실행하기 위한 배치같은 자원에 접근할 수 있습니다.

그리고 Prometheus UI 에 더 쉽게 접근할 수 있는 서비스도 제공됩니다. 마지막 명령어인 `./minikube service` 는 Prometheus UI 에 접근할 수 있는 URL 을 제공합니다.

```shell
hostname $./kubectl apply -f prometheus-deployment.yml
hostname $./minikube service prometheus --url
http://192.168.99.100:30114
```

**대상(Target)** 페이지는 `Example 2` 처럼 보이게 됩니다. 파일은 [Github](https://raw.githubusercontent.com/prometheus-up-and-running/examples/master/9/prometheus-deployment.yml) 에 있습니다.

> Example 2 - Targets of the example Prometheus running on Kubernetes

![image](https://user-images.githubusercontent.com/44635266/80861579-68467b80-8caa-11ea-9159-a0d978419e37.png)

여기까지가 Kubernetes 에 모니터링의 배경이 되는 핵심 아이디어를 보여주기 위한 기본 Kubernetes 설정입니다.

### Service Discovery

현재 Prometheus 에서 사용할 수 있는 Kubernetes 서비스 검색에는 node, endpoint, service, pod, ingress 의 5 가지 타입이 있습니다.

#### Node

**노드 서비스 검색(Node Service Discovery)** 은 Kubernetes 를 구성하는 노드가 발견하는데 쓰이며, Kubernetes 와 관련된 인프라 모니터링에서 사용합니다.

**쿠블릿(Kubelet)** 은 각 노드에서 실행하는 에이전트 이름으로, Kubernetes 클러스터의 상태 모니터링의 일부로 에이전트에서 데이터를 수집해야 합니다.

아래는 Prometheus 가 쿠블릿 데이터를 수집하는 구성을 보여줍니다.

```yaml
scrape_configs:
- job_name: 'kubelet'
  kubernetes_sd_configs:
   - role: node
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
```

```yaml
job_name: 'kubelet'
```

기본 작업 레이블이 제공되며, `relabel_configs` 가 없기 때문에 `kubelet` 이 작업 레이블이 됩니다.

```yaml
kubernetes_sd_configs:
- role: node
```

단일 Kubernetes 서비스 검색은 `node` 역할과 함께 제공됩니다. `node` 역할은 각 쿠블릿에 대해 하나의 대상을 발견합니다. Prometheus 가 클러스터 내부에서 실행되기 때문에, Kubernetes 서비스 검색의 기본값은 Kubernetes API 로 인증하도록 이미 설정되어 있습니다.

```yaml
scheme: https
tls_config:
  ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  insecure_skip_verify: true
```

쿠블릿은 HTTPS 를 통해 `/metrics` 를 제공합니다. 따라서 `scheme` 을 지정해야 합니다. 일반적으로 Kubernetes 클러스터는 자신들의 TLS 인증서 서명에 사용되는 자체 인증기관을 갖고 있으며, 데이터 수집을 위한 `ca_file` 을 제공합니다.

하지만 미니쿠베는 이 사항이 존재하지 않습니다. 그래서 보안 검사를 우회하려면 `insecure_skip_verify` 가 필요합니다.

`Example 3` 에서 보듯이 사용 가능한 메타 데이터는 노드 어노테이션과 레이블을 포함합니다. 다양한 하드웨어를 가지는 노드처럼, 관심을 가지는 노드의 하위 세트를 구별하는 레이블을 추가하는 데는 `relabel_configs` 와 함께 이 메타데이터를 사용할 수 있습니다.

> Example 3 - The Kubelet on the service discovery status page of Prometheus

![image](https://user-images.githubusercontent.com/44635266/80933276-0434cc00-8dfe-11ea-9d42-a9178d3a2bca.png)

쿠블릿의 자체 `/metrics` 는 쿠블릿에 대한 메트릭만 포함하며, 컨테이너 수준의 정보는 포함하지 않습니다. 쿠블릿은 `/metrics/cadvisor` 엔드포인트를 가지는 cAdvisor 를 내장하고 있습니다.

아래 에제에서 보듯이, 내장된 cAdvisor 에서 데이터의 수집은 쿠블릿에 사용된 데이터 수집 구성에 `metrics_path` 를 추가하면 됩니다. 내장 cAdvisor 는 Kubernetes 의 `namespace` 와 `pod_name` 에 대한 레이블을 포함합니다.

```yaml
scrape_configs:
- job_name: 'cadvisor'
  kubernetes_sd_configs:
   - role: node
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  metrics_path: /metrics/cadvisor
```

노드 서비스 검색은 Kubernetes 클러스터의 각 머신에서 실행되는 모든 모니터링 대상에서 사용할 수 있습니다. 예를 들어 노드 익스포터가 미니쿠베 노드에서 실행중이라면 포트의 레이블을 재지정해 데이터를ㄹ 수집할 수 있습니다.

#### Service

노드 서비스 검색은 Kubernetes 하위 구조를 모니터링하는 데 유용하지만, Kubernetes 서 실행되는 어플리케이션의 모니터링에는 많이 이용되지 않습니다.

Kubernetes 상 어플리케이션을 구성할 수 있는 방법은 몇 가지가 있으며, 아직 단일 표준은 나타나지 않았습니다. 하지만, Kubernetes 상의 각 어플리케이션이 서로 발견하는 방법으로 서비스를 이용할 가능성이 있습니다.

서비스 역할은 각 포트에 대해 단일 대상을 반환합니다. 서비스들은 기본적으로 로드밸런서이며, Prometheus 가 매번 다른 어플리케이션에서 인스턴스에서 데이터를 수집할 수 있기 때문에, 로드 밸런서를 통한 대상의 데이터 수집은 현명한 방법이 아닙니다.

그러나 서비스 역할은 서비스가 조금이라도 응답하는지 여부를 확인하는 블랙박스 모니터링에는 유용할 수 있습니다.

#### Endpoint

Prometheus 는 각 어플리케이션 인스턴스가 대상을 가지도록 구성되어야 하며, `endpoints` 역할은 바로 이 기능을 제공합니다. 서비스들은 파드에 의해 지원됩니다. 파드는 강하게 결홥된 컨테이너들의 그룹으로, 네트워크와 저장 장치를 공유합니다.

각 Kubernetes 서비스 포트에 대해, 엔드포인트 서비스 검색 역할은 해당 서비스를 지원하는 각 파드의 대상을 반환합니다. 추가적으로, 다른 모든 파드의 포트는 모니터링 대상으로 반환됩니다.

아래 예제는 API 서버를 발견하고 데이터를 수집하는 데이터 수집 구성을 보여줍니다.

```yaml
scrape_configs:
- job_name: 'k8apiserver'
  kubernetes_sd_configs:
   - role: endpoints
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  relabel_configs:
   - source_labels:
      - __meta_kubernetes_namespace
      - __meta_kubernetes_service_name
      - __meta_kubernetes_endpoint_port_name
     action: keep
     regex: default;kubernetes;https
```

이 데이터 수집 구성을 부분씩 나눠서 살펴보겠습니다.

```yaml
job_name: 'k8apiserver'
```

`job` 레이블은 `k8apiserver` 가 될것입니다. 따라서 레이블을 재지정하기 위해 변경해야 하는 대상은 없습니다.

```yaml
kubernetes_sd_configs:
- role: endpoints
```

`endpoints` 역할은 사용하는 단일 Kubernetes 서비스 검색이 있으며 이것은 각 서비스를 지원하는 모든 파드의 모든 포트를 대상으로 반환할것입니다.

```yaml
scheme: https
tls_config:
  ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  insecure_skip_verify: true
bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

쿠블릿과 마찬가지로, API 서버는 HTTPS 를 통해 제공됩니다. 또한, `bearer_token_file` 이 제공하는 인증이 필요합니다.

```yaml
relabel_configs:
- source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_service_name
    - __meta_kubernetes_endpoint_port_name
  action: keep
  regex: default;kubernetes;https
```

이 레이블 재지정 구성은 `default` 네임스페이스에 있는 대상만 반환하며, `https` 라는 포트를 가지는 `kubernetes` 서비스의 일부입니다.

아래 `Example 4` 에서 결과 대상을 확인할 수 있습니다. API 서버는 특별하기 때문에, 메타데이터가 많지 않습니다. 이 밖의 모든 잠재적인 대상은 제거되었습니다.

> Example 4 - The API server on the service discovery status page of Prometheus

![image](https://user-images.githubusercontent.com/44635266/81028606-23def980-8ebd-11ea-946a-c3225332b80c.png)

API 서버들의 데이터를 수집하길 원하지만, 대부분의 경우 어플리케이션에 초점을 맞춥니다. 아래 예제는 모든 서비스의 파드 데이터를 자동으로 수집하는 방법입니다.

```yaml
scrape_configs:
 - job_name: 'k8services'
   kubernetes_sd_configs:
    - role: endpoints
   relabel_configs:
    - source_labels:
       - __meta_kubernetes_namespace
       - __meta_kubernetes_service_name
      regex: default;kubernetes
      action: drop
    - source_labels:
       - __meta_kubernetes_namespace
      regex: default
      action: keep
    - source_labels: [__meta_kubernetes_service_name]
      target_label: job
```

```yaml
job_name: 'k8services'
kubernetes_sd_configs:
 - role: endpoints
```

위 예제는 작업 이름과 Kubernetes `endpoints` 역할을 제공합니다. 그러나 나중에 다시 지정하기 때문에 `job` 레이블로 끝나지 않습니다.

알고있는 대상은 모두 일반적인 HTTP 이기 때문에 HTTPS 설정은 없습니다. 인증이 필요 없기 때문에 `bearer_token_file` 도 없으며, 베어러 토큰을 모두 서비스에 보내는 것은 누군가 당신인 처 가장하는것입니다.

```yaml
relabel_configs:
- source_labels:
    - __meta_kubernetes_namespace
    - __meta_kubernetes_service_name
  regex: default;kubernetes
  action: drop
- source_labels:
    - __meta_kubernetes_namespace
  regex: default
  action: keep
```

이미 또 다른 데이터 수집 구성에서 처리하고 있기 때문에 API 서버는 제외했으며, 어플리케이션을 시작하는 `default` 네임스페이스에 대해서만 알아봤습니다.

```yaml
- source_labels: [__meta_kubernetes_service_name]
  target_label: job
```

이러한 레이블 재지정 동작은 Kubernetes 서비스 이름을 가져와 `job` 레이블로 사용합니다. 데이터 수집 구성을 위해 제공한 `job_name` 은 기본값일 뿐이며, 적용되지 않습니다.

이러한 방법으로, Prometheus 는 새로운 서비스를 자동으로 선택하고 유용한 `job` 레이블을 사용해 서비스들에 대한 데이터 수집을 시작할 수 있습니다. 이 경우 `Example 5` 처럼 `job` 레이블은 Prometheus 그 자체가 됩니다.

> Example 5 - Prometheus has automatically discovered itself using endpoint service discovery

![image](https://user-images.githubusercontent.com/44635266/81028611-2a6d7100-8ebd-11ea-8a9d-7a51851e0096.png)

아래 예제처럼 서비스나 파드 메타데이터 Kubernetes 어노테이션을 기반으로 하는 `__scheme__` 나 `__metrics_path__` 로부터 레이블을 더 추가하기 위해 레이블 재지정을 사용할 수 있습니다. 이들은 `prometheus.io/scheme`, `prometheus.io/path`, `prometheus.io/port` 서비스 어노테이션을 찾고, 존재하는 경우에는 발견된 것들을 사용합니다.

```yaml
relabel_configs:
 - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
   regex: (.+)
   target_label: __scheme__
 - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
   regex: (.+)
   target_label: __metrics_path__
 - source_labels:
    - __address__
    - __meta_kubernetes_service_annotation_prometheus_io_port
   regex: ([^:]+)(:\d+)?;(\d+)
   replacement: ${1}:${3}
   target_label: __address__
```

이 코드는 서비스당 하나의 포트만 모니터링하는 것으로 제한됩니다. `prometheus.io/port2` 어노테이션을 사용해 또 다른 데이터 수집 구성을 할 수 있으며, 모니터링이 필요한 많은 포트를 가지는 경우에도 마찬가지로 처리 가능합니다.

#### Pod

엔드포이트 검색은 서비스를 지원하는 주된 프로세스의 모니터링에 좋지만, 서비스의 일부가 아닌 파드는 발견하지 못했습니다.

`pod` 역할은 파드를 검색하며, 파드의 모든 포트에 대한 대상을 반환합니다. 이를 통해 파드를 제거하기 때문에, 파드가 속한 서비스가 어느 것인지 알 수 없으므로 레이블과 어노테이션 같은 서비스 메타데이터를 사용할 수 없습니다.

하지만 모든 파드 메타데이터에 접근해야 합니다. 파트 메타데이터를 사용하는 방법은 어떤 규칙을 사용하고 싶은지와 귀결됩니다.

모든 파드는 서비스의 이룹가 되고 나서 서비스 검색에 `endpoint` 역할을 사용해야 한다는 규약을 생성할 수 잇습니다. 모든 파드는 자신이 속한 Kubernetes 서비스를 나타내는 레이블을 갖고 서비스 검색에 `pod` 역할을 사용하는 규약을 가질 수 있습니다.

모든 포트는 이름이 있으므로, 해당 규약을 사용하지 않고 `prom-http` 접두어를 포함하는 이름을 가지는 포트들은 HTTP 를 통해 데이터를 수집하고, `prom-https` 접두어를 가지는 포트의 경우 HTTPS 를 통해 데이터를 수집합니다.

미니쿠베와 함께 제공되는 컴포넌트 중 하나인 `kube-dns` 는 DNS 서비스를 제공합니다. `kube-dns` 의 파드는 Prometheus 메트릭을 제공하는 `metrics` 라는 포트를 비롯한 여러 개의 포트를 가집니다. 아래 예제는 이 포트를 탐색하는 방법과 `Example 6` 과 같이 컨테이너 이름을 `job` 레이블로 이용하는 방법입니다.

```yaml
scrape_configs:
- job_name: 'k8pods'
  kubernetes_sd_configs:
   - role: pod
  relabel_configs:
   - source_labels: [__meta_kubernetes_pod_container_port_name]
     regex: metrics
     action: keep
   - source_labels: [__meta_kubernetes_pod_container_name]
     target_label: job
```

> Example 6 - Two targets discovered using pod service discovery

![image](https://user-images.githubusercontent.com/44635266/81028780-c8613b80-8ebd-11ea-95a0-a1dd632b38c6.png)

#### Ingress

인그레스는 Kubernetes 서비스를 클러스터 외부에 표시하는 방법입니다. 인그레스는 서비스의 최상위에 있는 계층이기 때문에, 기본적으로 `service` 역할과 비슷하게 `ingress` 역할도 로드밸런서입니다. 여러 파드가 해당 서비스와 인그레스를 지원하기 때문에 Prometheus 에서 데이터를 수집할 때 문제가 발생할 수 있습니다.

따라서 블랙박스 모니터링에만 이 역할을 사용해야 합니다.

### kube-state-metrics

Kubernetes 서비스 검색을 사용해, Prometheus 가 어플리케이션과 Kubernetes 인프라에서 데이터를 수집하게 할 수 있습니다. 하지만 여기에는 서비스, 파드, 배치, 기타 자원에 대해 Kubernetes 가 알고있는 사항에 대한 메트릭은 포함되지 않습니다.

이는 쿠블릿과 Kubernetes API 서버 같은 어플리케이션이 각자 자신의 성능에 대한 정보는 게시해야 하지만, 내부 데이터 구조는 저장하지 않아야 하기 때문입니다.

대신 다른 엔드포인트에서 이 메트릭을 얻을 수 있습니다. 또는 엔드포인트가 존재하지 않는다면, 관련 정보를 추출하는 익스포터를 가질 수 있습니다. Kubernetes 의 경우 `kube-state-metrics` 가 이에 해당하는 익스포터입니다.

`kube-state-metrics` 을 실행하기 위해서는 아래 예제의 단계를 따르고 브라우저에서 반환되는 URL 의 `/metrics` 에 접속해야 합니다. [Github](https://raw.githubusercontent.com/prometheus-up-and-running/examples/master/9/kube-state-metrics.yml) 에서 파일을 확인할 수 있습니다.

```shell
hostname $./kubectl apply -f kube-state-metrics.yml
hostname $./minikube service kube-state-metrics --url
http://192.168.99.100:31774
```

배포할 때 의도된 개수의 메트릭을 위한 `kube_deployment_spec_replicas`, 노드 문제를 위한 `kube_node_status_condition`, 그리고 파드 재시작과 관련된 `kube_pod_container_status_restart_total` 같은 메트릭이 있습니다.



