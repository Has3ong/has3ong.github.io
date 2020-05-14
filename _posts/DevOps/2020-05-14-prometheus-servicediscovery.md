---
title : Prometheus Service Discovery
tags :
- Target Label
- Label
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

머신과 서비스들이 어디에 위치하고, 어떻게 배치되며 구성되는지에 대한 정보는 미리알 수 있습니다. **서비스 검색(Service Discovery, SD)** 을 이용하면 정보를 저장해둔 모든 데이터베이스로부터 Prometheus 로 해당 정보를 제공할 수 있습니다. 

Prometheus 는 별도의 설정 없이 **컨설(Consul)**, 아마존의 EC2, Kubernetes 같은 다양한 서비스 소스와의 연동을 지원합니다. 지원이 되지 않는 형태의 서비스 소스인 경우, 파일 기반 서비스 검색을 통해 관련 정보를 획득할 수 있습니다. 이는 **앤서블(Ansible)** 이나 **셰프(Chef)** 처럼 적절한 형식으로 머신과 서비스 목록을 작성해 주는 환경 구성 관리시스템을 이용하거나 데이터 소스에서 정기적으로 실행되는 스크립트를 작성하는 방법 등을 통해 가능합니다.

**레이블(Label)** 은 Prometheus 에서 가장 핵심적인 부분 중 하나로 **대상 레이블(Target Label)** 을 지정해두면 모니터링 대상을 이해하기 쉬운 체계로 그룹화하고 구성할 수 있습니다. 대상 레이블을 통해 동일한 역할을 수행하거나 동일한 환경에 있거나 같은 팀에 의해 운용되는 대상을 하나로 묶을 수 있습니다.

대상 레이블은 어플리케이션이나 익스포터 내에서 구성되는 것이 아니라 Prometheus 에서 구성되므로 각 팀의 관심에 따라 별도의 레이블 계층 구조를 가질 수 있습니다. Rack 이나 PDU, PostgreSQL 마스터 서버 등등 있습니다.

팀마다 자체적인 대상 레이블을 지정해 Prometheus 를 운용할 수 있기 때문에, 서비스 검색과 **풀 모델(Pull Model)** 방식을 활용하면 각 팀의 서로 다른 관심사항이 공존할 수 있습니다.

## Service Discovery Mechanisms

서비스 검색은 이미 확보된 머신과 서비스에 대한 데이터베이스와 통합되도록 설계도었습니다.

서비스 검색은 Prometheus 에 머신 목록을 제공하거나 이를 모니터링 하는것만이 아닙니다. 서비스 검색은 시스템 전반에 걸쳐 나타나는 의존성 찾기, 관심사항같은 것입니다. 따라서 머신과 서비스에 대한 단순한 목록뿐 아니라 이들이 어떻게 구성되어 있으며 어떤 수명주기로 운영되는지에 관한 규칙도 확보해야합니다.

정확한 서비스 검색 메커니즘은 **메타데이터(Metadata)** 를 제공합니다. 메타데이터란 서비스의 이름, 설명, 서비스를 보유한 팀, 태그등 유용하게 활용될 수 있는 모든 사항을 의미합니다. 메타데이터는 대상 레이블로 변환될 수 있으며, 메타데이터가 많을 수록 좋습니다.

서비스 검색 메커니즘은 하향식과 상향식 두 가지 방법이 있습니다. **상향식(Bottom-Up)** 은 컨설처럼 서비스 인스턴스를 등록할 때 메타데이터를 작성해 서비스 검색 메커니즘에 함께 등록하는 방식입니다.

**하향식(Top-Down)** 은 EC2 처럼 서비스 검색 메커니즘 스스로 구성 정보를 바탕으로 어떤 항목이 있어야 하는지 파악하고 접근하는 방식입니다.

### Static

정적 구성은 작고 간단해 변화가 없는 단순한 설정에 유용합니다. 홈 네트워크 로컬 푸시게이트웨이를 위한 수집 구성과 아래 예제에서 보듯이 Prometheus 자신을 모니터링 대상으로 설정하는 경우도 해당이 됩니다.

```yml
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
      - localhost:9090
```

앤서블같은 구성 관리도구를 사용한다면 아래 예제와 같은 템플릿 시스템으로 노드 익스포터가 모니터링 데이터를 수집하는 모든 머신의 목록을 생성할 수 있습니다.

```yml
scrape_configs:
 - job_name: node
   static_configs:
    - targets:
{% for host in groups["all"] %}
      - {{ host }}:9100
{% endfor %}
```

대상 리스트를 제공하는 것 외에, 정적 `labels` 필드 내에 이러한 대상을 위한 레이블을 추가로 정의할 수 있습니다.

다수의 `static_configs` 는 하나의 리스트 형태로 인식되며 아래 예제와 같이 여러 개의 정적 구성 정보를 하나의 수집 구성에 정의할 수 있습니다. 이 작업은 정적 구성만 고려하는것보다 여러 개의 서비스 소소와 연동하기 위해 다른 서비스 검색 메커니즘과 함께 사용하는 경우에는 유용합니다.

심지어 서로 다른 서비스 검색 메커니즘을 하나의 수집 구성에 혼합하여 정의하는 것도 가능합니다. 물론 이러한 경우에는 수집 구성이 이해하기 쉽게 작성된다고 보장하기 어렵습니다.

```yml
scrape_configs:
 - job_name: node
   static_configs:
    - targets:
       - host1:9100
    - targets:
       - host2:9100
```

마찬가지로 `scrape_configs` 에서 원하는 만큼 여러 개의 수집 구성을 하나의 리스트 형태로 반영할 수 있습니다. 한 가지 제약사항은 `job_name` 이 고유해야 한다는 점입니다.

### File

파일 기반 서비스 검색은 네트워크를 사용하지 않습니다. 그 대신, 로컬 파일 시스템에 저장된 파일에서 모니터링 대상 정보를 읽어옵니다. 이를 통해 Prometheus 가 지원하지 않는 서비스 검색 시스템과 통합하거나, 우리가 원하는 작업을 Prometheus 가 주어진 메타데이터로 충분히 수행하기 힘든 경우에 활용할 수 있습니다.

파일 형식은 JSON 이나 YAML 로 제공될 수 있으며, 확장자는 JSON 일 경우 *.json* YAML 일 경우에는 *.yml* 이나 *.yaml* 을 써야 합니다. 아래 예제에서 JSON 형식의 *filesd.json* 파일에서 모니터링 대상 정보의 작성 예를 확인할 수 있습니다. 하나의 JSON 파일에 원하는 만큼 대상을 정의할 수 있습니다.

```json
[
  {
    "targets": [ "host1:9100", "host2:9100" ],
    "labels": {
      "team": "infra",
      "job": "node"
    }
  },
  {
    "targets": [ "host1:9090" ],
    "labels": {
      "team": "monitoring",
      "job": "prometheus"
    }
  }
]
```

Prometheus 에서 파일 기반 서비스 검색의 구성은 `Example 5` 처럼 수집 구성 내의 `file_sd_configs` 항목을 이용해 정의합니다. 각 파일 기반 서비스 검색 구성은 이를 정의한 파일 들의 경로 리스트를 가지며, 파일 이름에 글로브 패턴을 사용할 수 있습니다. 파일 경로는 Prometheus 의 작업 디렉토리, 즉 Prometheus 가 시작되는 디렉토리를 기준으로 한 상대 경로로 표시합니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
```

일반적으로 파일 기반 서비스 탐색을 사용하는 경우 레이블을 다시 지정하기 위한 메타데이터를 정의하지 않고, 오히려 지속적으로 활용하려는 대상 레이블을 정의합니다.

브라우저에서 http://localhost:9090/service-discovery 로 이동해 Show More 항목을 클릭하면 `Example 1` 과 같이 *filesd.json* 에서 호출된 `job` 레이블과 `team` 레이블을 확인할 수 있습니다. 그림과 같이 대상이 구성되면 `host1` 과 `host2` 가 실제로 네트워크에 연결되어 있지 않은 상태라면 모니터링은 실패합니다.

> Example 1 - Service discovery status page showing three discovered targets from file SD

![image](https://user-images.githubusercontent.com/44635266/80584141-3801a180-8a4c-11ea-9db4-abd501aabcf3.png)

파일을 통한 모니터링 대상에 대한 정보 제공은 구성 관리 시스템의 템플릿에서 가져오거나 정기적으로 수행되는 데몬을 통해 작성됩니다. 또는 `wget` 을 사용하는 `cronjob` 을 통해 웹서비스에서 가져올 수 있습니다. 변경사항은 `inotify` 를 사용해 자동으로 선택되기 때문에 `rename` 을 써서 파일의 변경사항을 원자적으로 만들어두는 것이 좋습니다.

### Consul

**컨설(Consul)** 기반 서비스 검색은 대부분의 다른 서비스 검색 메커니즘 처럼 네트워크를 사용하는 서비스 검색 메커니즘입니다. 조직 내부의 서비스 검색 시스템이 구축되어 있지 않다면, 컨설은 구성과 실행의 쉬운 시스템 중 하나입니다. 컨설에는 각 머신에서 동작하는 에이전트가 있고 이들 사이에 통신이 이루어집니다. 어플리케이션은 머신의 로컬 에이전트하고만 연결됩니다. 몇몇 에이전트는 지속성과 일관성을 제공하는 서버로 동작합니다.

컨설 서비스 검색을 사용하기 위해 아래 예제처럼 컨설을 개발 모드로 설정하고 실행합니다.

```shell
hostname $ wget https://releases.hashicorp.com/consul/1.0.2/
    consul_1.0.2_linux_amd64.zip
hostname $ unzip consul_1.0.2_linux_amd64.zip
hostname $ ./consul agent -dev
```

이제 웹 브라우저로 *http://localhost:8500* 에 접속하면 컨설 UI 를 확인할 수 있습니다. 컨설은 서비스 개념으로 동작하므로, 개발 모드 설정에는 컨설 자체를 의미하는 하나의 서비스가 포함되어 있습니다. 그 다음으로 아래 예제에서 설정해둔 구성 정보로 Prometheus 를 실행해 보겠습니다.

```yaml
scrape_configs:
 - job_name: consul
   consul_sd_configs:
    - server: 'localhost:8500'
```

웹 브라우저에서 http://localhost:9090/service-discovery 로 접속하면 `Example 2` 와 같이 컨설을 통해 하나의 대상이 일부 메타데이터와 함께 검색되었음을 보여줍니다. 이 대상은 `instance` 와 `job` 레이블을 갖고 있습니다. 에이전트와 서비스가 더 많이 있다면, 이들 역시 이 웹페이지에 표시될 것입니다.

> Example 2 - Service discovery status page showing one discovered target, its metadata, and target labels from Consul

![image](https://user-images.githubusercontent.com/44635266/80584589-dc83e380-8a4c-11ea-8dc8-8cdb1d77c820.png)

컨설은 `/metrics` 페이지를 표시하지 않기 때문에 Prometheus 로부터 메트릭 수집은 불가능합니다. 그러나 컨설 에이전트가 동작하는 모든 머신을 찾기엔 충분한 정보가 제공됩니다. 따라서 수집이 가능한 노드 익스포터가 실행되어야 합니다.

### EC2

EC2 라는 이름은 **아마존 엘라스틱 컴퓨트 클라우드(Amazon Elastic Compute Cloud)** 라는 인기 있는 가상머신입니다. EC2 는 Prometheus 가 추가 설정 없이 서비스 검색에서 이용할 수 있는 다수의 클라우드 중 하나입니다.

EC2 를 서비스 검색에 사용하려면, EC2 API 를 사용하여 Prometheus 에 **자격증명(Credentials)** 을 제공해야 합니다. 자격증명을 제공하는 방법 중 하나는 AmazonEC2ReadOnlyAccess 정책에 따른 IAM 사용자로 설정하고 아래 예제와 같이 **접근 키(Access Key)** 와 **비밀 키(Secret Key)** 를 구성파일에 제공하는 것입니다.

```yaml
scrape_configs:
 - job_name: ec2
   ec2_sd_configs:
    - region: <region>
      access_key: <access key>
      secret_key: <secret key>
```

실행 중인 것이 없다면, Prometheus 구성 파일에서 작성한 **EC2 리전(EC2 Region)** 에서 최소한 하나의 EC2 인스턴스 를 시작하겠습니다. 웹 브라우저에서 http://localhost:9090/servicediscovery 로 접속하면 검색된 대상과 EC2 에서 추출한 메타데이터를 확인할 수 있습니다. (`Example 3`) 예를 들어, `__meta_ec2_tag_Name="My Display Name` 은 EC2 인스턴스의 Name 태그로, EC2 콘솔에서 확인할 수 있습니다.(`Example 3`)

그림을 보면 `instance` 레이블 값이 대상의 사설 IP 주소로 설정되어 있음을 알 수 있습니다. Prometheus 가 모니터링과 더불어 실행 중이라는 사실을 가정한다면 합리적인 기본값입니다. 모든 EC2 인스턴스가 공용 IP 를 갖는 것은 아니며 EC2 인스턴스의 공용 IP 로 통신하려면 네트워크 사용 비용이 발생합니다.

> Example 3 - Service discovery status page showing one discovered target, its metadata, and target labels from EC2

![image](https://user-images.githubusercontent.com/44635266/80587829-389d3680-8a52-11ea-9c02-4411d150eac2.png)

대부분 다른 클라우드 제공자를 사용한 서비스 검색도 유사한 방식으로 동작하지만, 필요한 구성 파일이나 반환되는 메타데이터는 차이가 있습니다.

## Relabelling

지금까지 서비스 검색 메커니즘을 보면 대상과 대상에 대한 메타데이터가 다소 원시적인 형식으로 표시되는 것을 확인할 수 있습니다. 파일 기반 서비스 검색과 통합해 원하는 대상과 레이블을 Prometheus 에 정확하게 제공할 수 있지만, 대부분의 경우에는 그럴 필요가 없습니다. 그 대신, Prometheus 에 **레이블 재지정(Relabeling)** 을 사용해 메타데이터를 대상과 매핑하는 방법을 보겠습니다.

이상적인 환경이라면, 새로운 머신과 어플리케이션이 자동으로 선택되고 모니터링되도록 서비스 검색과 레이블 재지정을 구성할 수 있습니다. 실제 환경에서는 설정이 견고해짐에 따라 정기적으로 Prometheus 구성 파일을 업데이트해야 할 정도로 복잡해질 가능성은 없지만, 사소한 인프라 문제가 발생할 수 있습니다.

### Choosing What to Scrape

가장 먼저 구성해야 하는 내용은 어떤 대상에 대한 정보를 실제로 수집할지 결정하는 것입니다. 하나의 서비스로 실행하는 팀의 경우, Promtehus 가 EC2 리전에 있는 모든 대상에서 데이터를 수집하길 원하지는 않습니다.

인프라 팀의 머신을 모니터링하려면 아래 예제와 같이 `keep` 유형의 **레이블 재지정 동작(Relabel Action)** 을 사용할 수 있습니다. `source_labels` 에 나열된 레이블 값에 `regex` 를 적용해 정규 표현식이 레이블과 일치하는 경우, 대상에 대한 모니터링을 계속합니다. 예제는 하나의 레이블 재지정 동작이 정의되어 있고 `team="infra"` 를 만족한느 모든 대상만 걸러냅니다.

하지만 레이블이 `team="monitoring` 인 대상은 정규 표현식과 일치하지 않기 때문에 삭제됩니다. 

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: infra
      action: keep
```

`relabel_configs` 는 여러개의 레이블 재지정 동작을 정의할 수 있습니다. `keep` 이나 `drop` 동작을 통해 대상이 삭제되지 않는 이상, 레이블 재지정 동작은 순서대로 처리됩니다. 아래 예제에서는 레이블이 `infra` 와 `monitoring` 두 값을 동시에 가질 수 없기 때문에 모든 대상을 삭제할것입니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: infra
      action: keep
    - source_labels: [team]
      regex: monitoring
      action: keep
```

레이블에 여러 개의 값을 사용하려면, 하나 이상의 표현하는 방법인 `|` 을 대체 연산자로 사용합니다. 아래 예제는 인프라 혹은 모니터링 팀 중 하나에 해당되는 경우, 대상을 유지하는 정확한 방법을 보여줍니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: infra|monitoring
      action: keep
```

일치하지 않는 대상을 삭제하는 `keep` 동작 외에, `drop` 동작은 일치하는 대상을 제외합니다. 그리고 `source_labels` 에는 여러 개의 레이블을 정의할 수 있습니다. 각 레이블은 세미콜론으로 연결됩니다. 모니터링 팀의 Prometheus 작업을 수집하지 않으려면 아래 예제와 같이 조합할 수 있습니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [job, team]
      regex: prometheus;monitoring
      action: drop
```

이렇게 레이블 재지정을 활용할 것인지는 사용자의 몫이며, 레이블 재지정을 사용하기 위한 몇 가지 규칙을 마련해야 합니다. EC2 인스턴스를 소유하는 팀 이름을 `team` 태그로 가지고 있거나, 컨설에서 모든 운영 서비스가 `production` 태그를 가지는 것이 대표적인 사례입니다. 이 규칙이 없다면 새로운 모니터링을 위해 별도 처리가 필요하며 이로 인해 시간을 효율적으로 활용하지 못할 수 있습니다.

서비스 검색 메커니즘이 일부 양식에 대한 상태 확인을 포함하는 경우, 비정상 인스턴스를 제외하기 위해 레이블 재지정 기능을 사용해서는 안됩니다. 인스턴스가 비정상적으로 보고된다고 해도 유용한 메트릭을 생성할 수 있습니다. 특히 시스템의 시작 시점이나 종료 시점에는 더 그렇습니다. 

### Target Labels

**대상 레이블(Target Label)** 은 수집을 통해 반환되는 모든 시계열의 레이블에 추가되는 레이블입니다. 대상 레이블은 수집 대상을 구분하며, 머신 소유자나 버전 번호처럼 시간이 지나면서 변경되어서는 안됩니다.

대상 레이블이 변경될 때마다 수집된 시계열을 구분하는 레이블도 변경됩니다. 그렇게 되면 그래프의 연속성이 깨질 것이며 규칙과 알림에도 문제가 발생할 수 있습니다.

무엇이 좋은 대상 레이블을 만드는 것일까?, 개발 단계인지 생산 단계인지, 지역 정보와 데이터 센터 정보와 어플리케이션을 어느 팀이 관리하는지 같은 광범위한 어플리케이션 관련 내용을 대상 레이블이 추가하는 방법이 일반적입니다. **샤딩(Sharding)** 이 있는지 여부를 표시하는 것같이, 어플리케이션 내부 구조에 대한 레이블 추가 역시 일반적입니다.

궁극적으로 대상 레이블은 PromQL 에서 대상을 선택해 그룹화하고, 집계할 수 있습니다. 예를 들어 어느 어플리케이션에 많은 부하가 걸리는지, 어느 팀이 CPU 를 가장 많이 사용하는지 알고 싶으면, 운영에 대한 알림과는 다르게 처리하는 개발에 대한 알림을 보내고자 할 때 대상레이블을 사용할 수 있습니다.

하지만 대상 레이블을 사용하는 데는 비용이 따릅니다. 자원 측면에서 볼 때, 레이블 하나를 추가하는 건 별다른 비용이 들지 않지만, PromQL 을 작성하는 경우에 실제 비용이 발생합니다. 작성한 각각의 PromQL 표현식에서 추가되는 모든 레이블은 한번씩 더 유의해서 살펴봐야합니다. 예를 들어 각 대상마다 고유한 `host` 레이블을 추가한다면, 이는 각 대상마다 `instance` 레이블만이 고유한 값을 가지는 레이블이어야 한다는 기대를 위반하게 되는 것입니다. 이로써 `without(instance)` 를 사용하는 모든 집합을 망칠 수도 있습니다.

대상 레이블은 각각 하나씩 추가되는 고유성을 가지는 계층고 계층화되어야 합니다. 예를 들어 인스턴스를 포함하는 작업, 작업을 포함하는 서비스 같이 계층 구조를 정의할 수 있습니다. 이는 고정 불변의 법칙이 아닙니다. 지금은 데이터센터가 하나뿐이더라도 향후 추가될 데이터센터를 고려해 미리 정의해둔 데이터센터를 부여할 수 있습니다.

버전 번호 같이 어플리케이션이 알고 있는 레이블이지만 대상 레이블로 사용하기 적합하지 않은 경우에는 `info` 메트릭을 사용해 표시할 수 있습니다.

Prometheus 의 모든 대상에 대해 `region` 같이 일부 레이블을 공유하고 싶어지면 `external_labels` 로 사용해야 합니다.

#### REPLACE

대상 레이블을 지정하기 위해 레이블을 재지정하면 어떻게 될까? 정답은 `replace` 동작입니다. `replace` 동작은 레이블을 복사하거나 정규 표현식을 사용할 수 있습니다.

아래 예제에 이어서 *monitoring team* 팀명이 *monitor team* 으로 변경되고 파일 기반 서비스 탐색의 입력값을 변경할 수 없어 레이블 재지정을 수행해야 한다고 해보겠습니다. 아래 예제는 정규 표현식 `monitoring` 과 일치하는 `team` 레이블을 찾고, 조건이 일치하는 경우 `team` 레이블은 **교체 값(Replacement Value)** 인 `monitor` 로 교체합니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: monitoring
      replacement: monitor
      target_label: team
      action: replace
```

간단해보이지만 실제로 사용할 때 교체 레이블 값을 일일이 지정하는 데는 많은 노력이 필요합니다. 이번에는 `monitoring` 에서 `ing` 가 문제고 팀 이름이 `ing` 로 끝나는 경우, 이를 모두 없애도록 레이블 재지정해보겠습니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: '(.*)ing'
      replacement: '${1}'
      target_label: team
      action: replace
```

`team="infra"` 같이 대상이 일치하는 레이블 값을 가지고 있지 않다면, `Example 4` 에서 볼 수 잇는 것처럼 교체 동작은 대상에 아무런 영향이 없습니다.

> Example 4 - The ing is removed from monitoring, while the infra targets are unaffected

![image](https://user-images.githubusercontent.com/44635266/80589541-57e99300-8a55-11ea-9e47-063c507512bf.png)

값이 없는 레이블은 레이블이 없는 것과 같습니다. 따라서 `team` 레이블을 삭제하고 싶다면 아래 예제와 같이 `relabel_configs` 를 구성하면 됩니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
      - '*.json'
   relabel_configs:
    - source_labels: []
      regex: '(.*)'
      replacement: '${1}'
      target_label: team
      action: replace
```

정규 표현식을 모든 문자에 적용한 다음 캡처하고 교체 값으로 사용하는 것은 일반적이기 때문에, 각각의 경우에 정규 표현식의 사용은 기본입니다. 따라서 관련 내용을 삭제할 수 있으며 아래 예제는 이전 예제와 동일한 효과를 보입니다.

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: []
      target_label: team
```

아래 예제는 포트 80 번에 대상을 생성했습니다. 하지만 대상의 포트를 노드 익스포터가 동작하고 있는 9100 번으로 변경하면 좀 더 유용할 것입니다. 아래 예제는 `__address__` 레이블 값으로 컨설 주소에 :9100 을 추가했습니다.

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_address]
      regex: '(.*)'
      replacement: '${1}:9100'
      target_label: __address__
```

#### JOB, INSTANCE, AND __ADDRESS__

`instance` 대상 레이블은 있지만 메타데이터에는 일치하는 `instance` 가 없는것을 볼 수 있습니다. 이 `instance` 레이블이 없다면 기본값은 `__address__` 레이블로 설정됩니다.

`instance` 레이블과 더불어 `job` 레이블은 대상이 항상 가지고 있어야 하는 레이블이며 `job` 레이블의 기본값은 `job_name` 구성 옵션을 참조합니다. `job` 레이블은 동일한 목적으로 동작되는 인스턴스의 집합을 나타내며, 일반적으로 동일한 바이너리와 구성으로 동작합니다. `instance` 레이블은 작업 내 하나의 인스턴스를 표시합니다.

`__address` 레이블은 Prometheus 가 데이터를 수집할 때, 접속하는 호스트 주소와 포트 번호를 가리킵니다. 이는 `instance` 레이블에 기본으로 제공되지만, 분리되어 있어 다른 값을 설정할 수 있습니다. 예를 들어 `instance` 레이블의 컨설 노드 이름을 사용하려면 아래 예제와 같이 IP 주소만 남겨둔 상태로 작성합니다. 이는 각 대상에 PromQL 을 복잡하게 만드는 고유한 두 번째 레이블을 추가하지 않으므로, 멋진 이름을 가진 `host`, `node`, `alias` 레이블을 추가하는 것보다 좋은 방법입니다.

```yaml
scrape_configs:
 - job_name: consul
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_address]
      regex: '(.*)'
      replacement: '${1}:9100'
      target_label: __address__
    - source_labels: [__meta_consul_node]
      regex: '(.*)'
      replacement: '${1}:9100'
      target_label: instance
```

#### LABELMAP

`labelmap` 은 `drop`, `keep`, `replace` 와는 달리 레이블 값이 아닌 이름에 적용됩니다. `labelmap` 은 사용하는 서비스 검색 메커니즘이 Key - Value 형태의 레이블을 사용하고, 이들 중 일부를 대상 레이블로 활용하려는 경우에 유용합니다. 또한, 새로운 레이블이 생성될 때마다 Prometheus 구성을 변경할 필요 없이 임의의 대상 레이블을 구성할 수 있습니다.

예를 들어 EC2 의 태그는 Key - Value 형태입니다. 서비스 이름을 `service` 태그에 넣고 서비스가 의도하는 바는 Prometheus 의 `job` 레이블과 일치시키는 기존 규칙이 있을 수 있습니다. 또한, `monitor_` 접두어가 붙은 모든 태그를 대상 레이블로 정의하는 규칙을 적용할 수 있습니다. 예를 들어 EC2 태그 `monitor_foo=bar` 는 Prometheus 의 대상 레이블 `foo="bar"` 로 변경할 수 있습니다. 아래 예제는 `job` 레이블에 `replace` 동작을 적용하고 접두어 `monitor_` 에 `labelmap` 동작을 적용하는 설정을 보여줍니다.

```yaml
scrape_configs:
 - job_name: ec2
   ec2_sd_configs:
    - region: <region>
      access_key: <access key>
      secret_key: <secret key>
   relabel_configs:
    - source_labels: [__meta_ec2_tag_service]
      target_label: job
    - regex: __meta_ec2_public_tag_monitor_(.*)
      replacement: '${1}'
      action: labelmap
```

그러나 Prometheus 시스템 전체 아키텍처 내에서 메타데이터의 유일한 컨슈머가 아닐 수 있기 때문에, 모든 레이블을 맹목적으로 복사해 사용하는것을 주의해야 합니다. 예를 들어 내부 청구를 목적으로 모든 EC2 인스턴스에 새로운 원가 중심점에 대한 태그를 추가할 수 있습니다.

이 태그가 `labelmap` 동작으로 인해 자동으로 대상 레이블이 된다면, 모든 대상 레이블이 바뀔 것이며 그래프와 알림이 망가질 수 있습니다. 따라서 널리 알려진 이름을 사용하거나 명확하게 네임스페이스가 부여된 이름을 사용하는 것이 바람직합니다.

#### LISTS

모든 서비스 검색 메커니즘이 Key - Value 형태의 레이블이나 태그를 제공하지는 않습니다. 일부 메커니즘은 태그 리스트만 제공하며, 대표적인 예로 컨설 태그가 있습니다. 컨설은 태그 리스트를 호라용할 가능성이 높지만, EC2 서브넷 ID 같이 서비스 검색 메커니즘이 리스트를 Key - Value 메타데이터로 변경해야 하는 또 다른 부분이 있습니다.

리스트에 있는 각 아이템들을 쉼표로 연결하고, 연결된 아이템들을 레이블 값으로 사용할 수 있습니다. 쉽게 정확한 정규 표현식을 작성할 수 있도록, 쉼표는 아이템의 처음이나 마지막에 붙일 수 있습니다.

예를 들어 컨설 서비스가 `dublin` 과 `prod` 태그를 지원한다고 가정하겠습니다. 태그에는 순서가 없기 때문에 `__mata_consul_tags` 레이블은 `dublin`, `prod` 나 `prod`, `dublin` 로 표현할 수 있습니다. 운영 대상만 수집하고자 하면 아래 예제와 같이 사용할 수 있습니다.

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_tags]
      regex:  '.*,prod,.*'
      action: keep
```

때로는 Key - Value 중에서 값만 태그에 포함되는 경우도 있습니다. 이 경우 레이블로 변환할 수 있지만 잠재적인 값이 무엇인지 파악해야 합니다. 아래 예제는 대상의 환경을 나타내는 태그를 `env` 레이블로 변경하는 방법입니다.

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_tags]
      regex:  '.*,(prod|staging|dev),.*'
      target_label: env
```

## How to Scrape

대상 레이블 및 연결을 위한 `__address__` 를 가진 수집 대상이 생겼습니다. `/metrics` 이외의 경로나 클라이언트 인증처럼 구성해야 하는 몇 가지 추가사항이 있습니다.

아래는 좀 더 일반적으로 사용 가능한 옵션 몇 가지를 보여줍니다.

```yaml
 - job_name: example
   consul_sd_configs:
    - server: 'localhost:8500'
   scrape_timeout: 5s
   metrics_path: /admin/metrics
   params:
     foo: [bar]
   scheme: https
   tls_config:
     insecure_skip_verify: true
   basic_auth:
     username: brian
     password: hunter2
```

`metrics_path` 는 유일하게 URL 경로 형식이며, `/metrics?foo=bar` 로 입력할 경우에 `/metrics%3Ffoo=bar` 로 이스케이프 됩니다. 그 대신 모든 URL 파라미터를 `params` 에 두어야 하지만 일반적으로 SNMP 익스포터와 블랙박스 익스포터를 포함하는 익스포터 클래스와 익스포터의 **페더레이션(Federation)** 에만 `params` 가 필요합니다. 디버깅을 더 어렵게 만들 수 있기 때문에, 임의의 헤더 추가는 불가능합니다. 제공하는 것 이상의 유연성이 필요한 경우에는 `proxy_url` 에 프록시 서버를 설정해 수집 요청을 조정할 수 있습니다.

`scheme` 은 `http` 나 `https` 로 설정하며, `https` 의 TLS 클라이언트 인증을 사용하려면 `key_file` 과 `cert_file` 같은 추가적인 옵션이 제공될 수 있습니다. `insecure_skip_verify` 를 사용하면 수집 다생의 TLS 인증서 유효성 검사를 비활성화할 수 있지만 보안 측면에서는 바람직 하지 않습니다.

TLS 클라이언트 인증을 제외한 HTTP 기본 인증과 HTTP 베어러 토큰 인증은 `basic_auth` 와 `bearer_token` 을 통해 제공됩니다. 베어러 토큰은 구성 파일보다 `bearer_token_file` 값에 설정된 파일을 통해 읽을 수 있습니다. 베어러 토큰과 기본 인증 비밀번호는 기밀 내용을 포함하고 있기 때문에 실수로 유출되지 않도록 Prometheus 의 상태 페이지에는 감춰집니다.

수집 구성에서 `scrape_timeout` 의 오버라이딩 이외에도 `scrape_interval` 을 오버라이드할 수 있지만 안정적인 Prometheus 에서는 단일 주기를 설정해야 합니다.

이러한 수집 구성 설정 중 URI Scheme, Path, URL Parameter 는 각각 레이블 이름 `__scheme__`, `__metrics_path__`, `__param_<name>` 으로 사용할 수 있으며, 레이블 재지정을 통해 오버라이드 할 수 있습니다. 동일한 이름을 가진 URL 파라미터가 있다면 첫 번째 파라미터만 유효합니다. 안정성과 보안성 등 다양한 이유로 인해 다른 설정에 대한 레이블 재지정은 허용되지 않습니다.

서비스 탐색 메타데이터는 보안에 민감한 부분으로 고려되지 않으며, Prometheus UI 에 접근이 가능한 누구나 확인할 수 있습니다.

#### DUPLICATE JOBS

`job_name` 은 유일해야 하지만, 기본 설정이므로 서로 다른 수집구성에서 동일 작업 레이블에 대한 대상을 생성할 수 있습니다.

컨설 태그에 표시된 서로 다른 기밀 내용이 필요한 몇 가지 작업이 있다면, **유지(keep)** 및 **삭제(drop)** 작업을 이용해서 기밀 내용을 분리한 다음 `replace` 를 사용해 `job` 레이블로 설정할 수 있습니다.

```yaml
- job_name: my_job
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel
    - source_labels: [__meta_consul_tag]
      regex:  '.*,specialsecret,.*'
      action: drop
   basic_auth:
     username: brian
     password: normalSecret

 - job_name: my_job_special_secret
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel
    - source_labels: [__meta_consul_tag]
      regex:  '.*,specialsecret,.*'
      action: keep
    - replacement: my_job
      target_label: job
   basic_auth:
     username: brian
     password: specialSecret
```

### metric_relabel_configs

레이블 재지정은 서비스 검색 메타데이터를 대상 레이블로 매핑하는 목적으로 사용하는것 이외에도 Prometheus 의 다른 영역에도 사용됩니다. 그 영역 중 하나가 대상으로부터 수집된 시계열에 레이블 재지정을 적용하는 메트릭의 레이블 재지정 입니다.

레이블 재지정 동작이 특정 위치에서만 사용되어야 하는 제약이 없기 때문에 `keep`, `drop`, `replace`, `labelmap` 모두 `metric_relabel_configs` 에서 사용할 수 있습니다.

메트릭의 레이블 재지정은 많은 비용이 드는 메트릭을 삭제하거나 잘못된 메트릭을 수정하는 두 가지 경우에 주로 사용됩니다. 데이터 소스에서 이러한 문제를 해결하는 것이 좋지만, 수정을 진행하면서 전략적인 옵션을 적용하는 것도 좋습니다.

메트릭 레이블 재지정은 시계열을 수집한 후 저장 공간에 쓰기 전에 접근할 수 있습니다. `keep` 동작과 `drop` 동작은 실제로 어떤 시계열을 수집할 지 선택할 수 있는 `__name__` 레이블에 적용할 수 있습니다. 예를 들어, Prometheus 의 `http_request_size_bytes` 메트릭이 과한 카디널리티를 갖고, 이로 인해 성능 문제가 발생하면 아래 예제와 같이 이 메트릭을 삭제할 수 있습니다. 메트릭은 여전히 네트워크를 통해 전송되고 파싱하지만 이러한 방법을 통해 약간의 여유를 제공할 수 있습니다.

```yaml
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
       - localhost:9090
   metric_relabel_configs:
    - source_labels: [__name__]
      regex: http_request_size_bytes
      action: drop
```

히스토그램의 특정 버킷을 삭제할 수 있고, 분위수를 계산할 수도 있습니다. 아래 예제는 Prometheus 의 `prometheus_tsdb_compaction_duration_seconds` 히스토그램을 통해 이러한 내용을 보여줍니다.

```yaml
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
       - localhost:9090
   metric_relabel_configs:
    - source_labels: [__name__, le]
      regex: 'prometheus_tsdb_compaction_duration_seconds_bucket;(4|32|256)'
      action: drop
```

메트릭이나 레이블을 재명명하는 경우, 메트릭 이름으로부터 레이블을 추출하는 경우에도 `metrics_relabel_configs` 를 사용할 수 있습니다.

#### LABELDROP AND LABELKEEP

대상 레이블 재지정에서는 필요하지 않을 수 있지만 메트릭의 레이블 재지정에서 필요할 수 있는 두 가지 레이블 재지정 동작이 더 있습니다. 간혹 익스포터는 적용되는 레이블을 지나치게 중요시할 수 있으며, 계측 레이블을 대상 레이블과 혼동해 수집 대상 레이블이 되어야 하는 내용을 반환할 수 있습니다. `replace` 동작은 미리 알고 있는 레이블 이름만 처리할 수 있지만 때때로 그렇지 않은 경우도 있습니다.

이 경우 `labeldrop` 과 `labelkeep` 동작을 사용합니다. `labelmap` 과 유사하게 이름도 레이블 값이 아닌 레이블 이름에 적용합니다. 레이블을 복사하는 대신 `labeldrop` 과 `labelkeep` 은 레이블을 삭제합니다. 아래 예제는 주어진 접두어를 만족하는 모든 레이블을 삭제하기 위해 `labeldrop` 을 사용합니다.

```yaml
scrape_configs:
 - job_name: misbehaving
   static_configs:
    - targets:
       - localhost:1234
   metric_relabel_configs:
    - regex: 'node_.*'
      action: labeldrop
```

이 동작을 수행하는 경우 `labeldrop` 이 더 좋습니다. `labelkeep` 을 사용하려면 `__name__`, `le`, `quantile` 를 비롯해 유지하려는 모든 레이블을 전부 나열해야 합니다.

### Label Clashes and honor_labels

`labeldrop` 은 익스포터가 필요한 레이블을 알고 있다는 잘못 추측한 경우에 사용할 수 있지만, 이미 필요한 레이블을 알고 있는 소규모의 익스포터 집합이 있습니다. 예를 들어 푸시게이트웨이 안에 있는 메트릭은 `instance` 레이블이 없어야 하기 때문에 푸시게이트웨이의 인스턴스 대상 레이블이 적용되지 않게 만드는 방법이 필요합니다.

먼저 수집 시의 계측 레이블과 동일한 이름을 가지는 대상 레이블이 있다면 어떤 일이 발생하는지 알아보겠습니다. 잘못된 동작을 하는 어플리케이션이 대상 레이블의 설정을 방해하지 않도록 대상 레이블이 우선시됩니다. 예를 들어 `job` 레이블에 충돌이 발생하면 계측 레이블은 `exported_job` 으로 다시 명명됩니다.

계측 레이블을 우선하고 대상 레이블을 오버라이드하길 원한다면 수집 구성에서 `honor_labels: true` 를 설정하면 됩니다. 빈 레이블은 누락된 레이블과 같은 것이 아니라는 사실은 Prometheus 가 가지는 특징 중 하나입니다. 수집된 메트릭이 명시적으로 `instance=""` 인 레이블을 갖고 있고 `honor_labels: true` 로 구성되었다면, 시계열 결과에는 인스턴스 레이블이 없을 것입니다. 이 기법은 푸시게이트웨이에서도 사용됩니다.

푸시게이트웨이 이외에도 `honor_labels` 는 하나의 어플리케이션 인스턴스에 대해 하나의 익스포터를 수행하는 것을 따르지 않고 다른 모니터링 시스템의 메트릭을 가져오라고 할 때 사용될 수 있습니다.

