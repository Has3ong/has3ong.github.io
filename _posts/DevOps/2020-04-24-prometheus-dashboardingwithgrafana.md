---
title : Prometheus Dashboarding with Grafana
tags :
- Template Variable
- Table Panel
- Graph Panel
- Singlestat Panel
- Dashboard 
- Data Source
- Grafana
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

알림이 발생했을 때나 시스템의 현재 성능을 확인하려고 할대 가장 먼저 접하는 화면이 **대시보드(Dashboard)** 입니다.

대시보드란 그래프나 테이블, 시스템을 시각화할 수 있는 집합입니다. 어떤 서비스에 얼마나 많은 트래픽이 집중되고, 이 때문에 대기시간이 어느 정도인지 등을 표시하는 전체 시스템 트래픽에 관한 대시보드를 쓰는 이들도 있을 것입니다.

각 서비스마다 대기시간, 오류, 응답률, 인스턴스 개수, CPU 사용량 메트릭등을 표시하는 개별 대시보드를 쓰고 있을 수 있습니다. 자세하게 이야기하면 특정 서브시스템이나 서비스의 대시보드, Java 어플리케이션에 사용하는 가비지 컬렉션 대시보드도 있을 수 있습니다.

널리 사용되는 Grafa 는 Graphite, InfluxDB 를 비롯해 다양한 모니터링 시스템과 비모니터링 시스템 대시보드를 제작할 수 있는 도구입니다. Grafana 는 Prometheus 를 사용하는 경우, 대시보드 제작에 가장 권장되는 도구로 Prometheus 를 꾸준히 지원하고 있습니다.

## Installation

Grafana 는 http:s//grafana.com/grafana/download 에서 설치할 수 있습니다. 웹사이트에서 설치하는 방법을 설명하지만, **도커(Docker)**를 사용하는 경우에도 다음 명령을 실행하면 됩니다.

```shell
docker run -d --name=grafana --net=host grafana/grafana:5.0.0
```

도커는 볼륨 마운트를 사용하지 않으므로 모든 상태를 컨테이너 내부에 저장하는 사실을 염두해야합니다.

Grfana 를 실행하고 브라우저에서 http://localhost:3000 으로 접속하면 `Example 1` 과 같은 로그인 화면을 볼 수 있습니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/79745783-dfdbe880-8343-11ea-8b67-eb26168c5fae.png)

이름 `admin` 과 비밀번호 `admin` 을 입력해 로그인하면 `Example 2` 처럼 **홈 대시보드(Home Dashboard)** 를 확인할 수 있습니다. 스크린샷의 내용을 좀 더 쉽게 파악하기 위해 밝은 테마로 변경했습니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/79745807-e9655080-8343-11ea-84d0-2b73dd140f06.png)

## Data Source

Grafana 는 그래프를 그릴 때 필요한 정보를 추출하기 위해 **데이터 소스(Data Source)** 를 사용합니다. Prometheus 는 물론, OpenTSDB, PostgreSQL 과 같이 추가적은 설정 없이 사용할 수 있는 다양한 유형의 데이터 소스가 있습니다.

동일 유형의 데이터 소스를 여러 개 사용할 수 있지만, 일반적으로 실행 중인 Prometheus 마다 1 개의 데이터 소스를 사용합니다. Grafana 대시보드는 다양한 데이터 소스로부터 그래프를 작성할 수 있으며, 그래프 패널에서 이런 데이터 소스를 혼합할 수 있습니다.

최신 버전의 Grafana 는 첫 데이터 소스를 쉽게 등록할 수 있습니다. App data source 를 클릭하여, Name 과 Type 모두 Prometheus, URL 은 Prometheus 가 실행중인 http://localhost:9090 인 데이터 소스를 추가하겠습니다. 입력 양식은 `Example 3` 과 같습니다.

나머지 설정값은 그대로 두고 마지막으로 Save & Test 를 클릭하여 제대로 동작하면 데이터 소스가 동작중이라는 메세지를 보게될것입니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/79745837-f41fe580-8343-11ea-8089-e571f1884f6f.png)

## Dashboards and Panels

http://localhost:3000 에 접속하여 New Dashboard 를 클릭하면 Example 4 와 같은 웹 페이지를 확인할 수 있습니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/79745856-fc782080-8343-11ea-9b7d-974d422af368.png)

이 웁페이지에서 대시보드에 어떤 패널을 추가할 지 선택할 수 있습니다. **패널(Panel)** 은 그래프나 테이블, 시각화된 다른 정보를 포함하는 사각의 공간입니다. 맨 위에 있는 + 로 표시된 Add Panel 버튼을 눌러 새로운 패널을 추가할 수 있습니다.

웹 페이지 상단의 톱니바퀴 모양 아이콘을 클릭하면 대시보드 이름 등을 설정할 수 있는 대시보드 설정 메뉴에 접근할 수 있습니다. 대시보드를 여러 개 만들어보려면 설정 메뉴에서 Save As 메뉴로 쉽게 복제할 수 있습니다.

### Avoiding the Wall of Graphs

실행 중인 서비스마다 여러 개의 대시보드를 별도로 작성하는 경우는 흔하지 않습니다. 대시 보드를 너무 많이 넣으면 실제 시스템에서 어떤 일이 일어나는지 해석하기가 어려워 집니다. 그래서 각 팀과 목적에 맞는 대시보드를 개별적으로 제공해야 합니다.

## Graph Panel

**그래프 패널(Graph Panel)** 은 앞으로 많이 쓰게 될 주요한 패널입니다. 명칭에서 뜻하는 바 그대로, 그래프를 보여주는 패널입니다. 아래 Example 4 에서 Graph 버튼을 눌러 그래프 패널을 추가해보겠습니다. 비어 있는 그래프가 하나 생기고 `Example 5` 처럼 Panel Title 을 클릭한 다음 Edit 을 누르고 그래프를 구성합니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/79745872-0568f200-8344-11ea-9926-69368cbe63e2.png)

이제 그래프 편집기의 **메트릭(Metrics)** 탭으로 활성화 되어 열립니다. `Example 6` 과 같이 A 옆에 있는 텍스트 박스에 쿼리 표현식 `process_resident_memory_bytes` 를 입력하고 텍스트 박스 바깥쪽을 클릭합니다. 수식 브라우저에서 동일한 표현식을 작성해 메모리 사용량 그래프를 확인할 수 있습니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/79745893-10bc1d80-8344-11ea-8520-c5c1524f7418.png)

Grafana 는 수식 브라우저보다 더 많은 기능을 제공합니다. 전체 시계열의 이름 이외의 사항을 표시하는 **범례(Legend)** 를 구성할 수 있습니다. Legend Format 텍스트 박스에 `{{job}}` 을 입력하고, Axes 탭에서 Left Y Unit 을 data/bytes 로 변경하고, General 탭의 Title 을 Memory Usage 로 변경합니다.

이제 `Example 7` 처럼 표현이 됩니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/79745927-1dd90c80-8344-11ea-9ade-d8c592987f0e.png)

이 내용은 모든 그래프를 그릴 때 구성하는 설정 사항이지만 Grafana 에서는 작은 부분에 지나지 않습니다. 색상, 스타일, 채우깅 등을 설정할 수 있으며, 다수의 데이터 소스에서 제공받는 메트릭도 넣을 수 있습니다. 

### Time Controls

대시보드 화면의 우측 상단에서 **시간 제어(Time Controls)** 와 관련된 내용을 발견했을지도 모릅니다. 기본 값으로는 최근 6 시간으로 표시됩니다. 시간 제어 메뉴를 클릭하면 `Example 8` 에서 볼 수 있듯이 시간 범위를 선택하고 얼마나 자주 갱신할 것인지 등을 설정할 수 있는 화면이 표시됩니다. 시간 제어는 전체 대시보드에 한꺼번에 적용되지만 재정의를 통해 패널 단위로 다시 설정할 수 있습니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/79745950-27627480-8344-11ea-900d-ebec42983aee.png)

## Singlestat Panel

**단일 상태 패널(Singlestat Panel)** 은 하나의 시계열 값만 표시합니다. 최신 버전의 Grafana 는 Prometheus 의 레이블 값도 보여줄 수 있습니다.

하나의 시계열 값을 추가해 예제를 시작해보겠습니다. 그래프 패널에서 대시보드 화면으로 돌아가기 위해 **되돌아가기(Back)** 버튼을 클릭하겠습니다. Add panel 을 누른 후, Singlestat panel 을 추가합니다. 그래프 패널을 추가할 때와 마찬가지로 Panel Title 을 클릭하고 Edit 을 클릭합니다.

Metrics 탭의 쿼리 표현식은 Prometheus 가 수집하는 시계열의 수를 나타내는 `prometheus_tsdb_head_series` 으로 작성합니다. 기본적으로, 단일 상태 패널은 대시보드의 시간 범위 동안의 시계열 평균값을 계산합니다. 가끔 이 평균값은 우리가 원하는 값이 아닐수도 있으므로 Options 탭에서 Stat 를 Current 로 변경합니다.

기본값으로 출력되는 텍스트는 다소 작을 수 있으므로 Font size 를 200 % 로 바꾸길 권장합니다. General 탭에서 Title 을 Prometheus Time Series 로 변경하고, 되돌아가기 버튼을 눌러 처음으로 가면 `Example 9` 같은 화면을 볼 수 있습니다.

> Example 9 

![image](https://user-images.githubusercontent.com/44635266/79745977-31847300-8344-11ea-93de-409aa477b67c.png)

그래프에 레이블 값을 보여줌으로써 소프트웨어 버전을 알려주면 유용합니다. 새로운 단일 상태 패널을 추가해보겠습니다. `uname -a` 명령어와 동일한 정보를 포함하는 쿼리 표현식은 `node_uname_info` 을 사용할 것입니다. Format 을 Table 로 설정하고, Options 탭에서 Column 항목을 release 로 설정합니다.

General 탭에서 Title 은 Kernel Version 으로 작성합니다. 대시보드로 가면 `Example 10` 과 같은 화면을 볼 수 있습니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/79745998-3ba67180-8344-11ea-8576-210d1e922c79.png)

단일 상태 패널에는 시계열 값에 따라 각기 다른 색상으로 표시하거나 값 뒤쪽에 **스파크라인(Sparkline)** 을 표시하는 것과 같은 추가 기능이 제공됩니다.

## Table Panel

단일 상태 패널이 한 번에 하나의 시계열만 표시할 수 있다면, **테이블 패널(Table Panel)** 은 여러 개의 시계열을 표시할 수 있습니다. 테이블 패널은 다른 형태의 패널보다 많은 구성 정보가 필요한 편이며, 관련된 모든 텍스트가 대시보드상에 어수선하게 보일 수 있습니다.

테이블 패널을 새로운 패널로 추가해보겠습니다. Panel Title 을 클릭한 다음 Edit 를 클릭합니다. Metrics 탭에서 쿼리 표현식 `rate(node_network_receive_bytes_total[1m])` 을 작성한 다음, Instance 체크 박스를 체크합니다. 테이블 패널에는 필요한 열이 더 있습니다. Column styles 탭에서 기존의 Time rune 을 Type of Hidden 으로 변경합니다. +Add 를 클릭하여 열의 형식은 Type of Hidden, 이름은 job 으로 설정하 다음 Apply 를 클릭해 새로운 규칙을 추가합니다.

instance 를 숨기기위한 또 다른 규칙을 추가합니다. 단위를 설정하기 위해, +Add 를 클릭해 Value 열에 대한 규칙을 추가하고 데이터 속도의 Unit 를 Bytes/sec 로 설정합니다. 마지막으로 General 탭에서 제목을 Network Traffic Received 설정하면 `Example 11` 과 같은 대시보드를 확인할 수 있습니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/79746027-46f99d00-8344-11ea-89b0-69ffbdbd75c9.png)

## Template Variables

네트워크 장치 기반 템플릿을 사용할 최소 2 대 이상의 장치를 모니터링 하겠습니다. `Example 12` 처럼 대시보드 이름을 클릭하고 화면 하단의 +New dashboard 를 클릭하여 새로운 대시보드를 추가합니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/79746052-511b9b80-8344-11ea-95bf-737a9de01799.png)

화면 상단의 기어 아이콘을 클릭한 다음 Variabls 를 클릭합니다. +Add Variable 를 클릭해 템플릿 변수를 추가합니다. Name 은 Device, Data source 는 Prometheus, Refresh 는 On Time Range Change 로 설정합니다.

사용하게 될 Query 는 `node_network_receive_bytes_total` 로 설정하고 device 레이블의 값을 추출하기 위해 Regex 을 `.*device="(.*?)".*` 로 설정합니다. 설정을 마치면 아래 처럼 보입니다.

> Example 13

![image](https://user-images.githubusercontent.com/44635266/79746078-5b3d9a00-8344-11ea-9fe5-6196f3c7ecb9.png)

Add 를 클릭하여 템플릿 변수를 추가한 다음 대시보드를 확인하면 `Example 14` 처럼 추가한 템플릿 변수에 대한 드롭다운 메뉴가 추가되고 활성화된 화면을 확인할 수 있습니다.

> Example 14

![image](https://user-images.githubusercontent.com/44635266/79746101-642e6b80-8344-11ea-9946-cd9491ce7a66.png)

Template 섹션을 닫고 ... 을 클릭한 다음 새로운 그래프 패널을 추가합니다. 위 예제처럼 Panel Title 을 클릭한 뒤 Edit 을 선택해 수정을 마칩니다. 쿼리 표현식을 `rate(node_network_receive_bytes_total{device="$Device"}[1m])` 으로 구성하면 $Device 가 저장된 템플릿 변수에 포함된 값으로 변경됩니다. 범례 형식인 Legend Format 은 `{{device}}` 로 Title 은 Bytes Received, 데이터 속도의 단위인 Unit 은 bytes/sec 로 설정합니다.

대시보드로 이동하여 패널 제목을 클릭합니다. 이번에는 더 보기 메뉴인 More 를 클릭한 다음 Duplicate 를 클릭하여 복제합니다. 이렇게 하면 기존 패널을 복사해 새로운 패널을 생성합니다. 복제된 패널 설정에서 표현식은 `rate(node_network_transmit_bytes_total{device=~"$Device"})[1m]` 으로, Title 은 Bytes Transmitted 로 변경합니다. 이제 대시보드에 `Example 15` 처럼 양방향으로 주고받는 데이터의 속도를 표시하는 패널이 생깁니다. 드롭다운 메뉴로 네트워크 장치를 선택해 각 네트워크 장치에 대한 패널을 확인할 수 있습니다.

> Example 15

![image](https://user-images.githubusercontent.com/44635266/79746121-6db7d380-8344-11ea-95b9-36257091846c.png)

실제 환경에서는 instance 레이블을 기반으로 템플릿을 만들며, 하나의 머신에 관련된 모든 네트워크 메트릭들을 동시에 보여줄것입니다. 하나의 대시보드에 여러 개의 템플릿 변수가 있을 수도 있습니다. 자바 가비지 컬렉션을 위한 대시보드도 이와같이 동작합니다.

시간 제어를 사용할 때와 비슷하게 템플릿 값을 변경하면, URL 의 파라미터도 변경됩니다. 이를 통해 대시보드 링크를 공유하거나 정확한 값을 사용해 대시보드에 알림 링크를 설정할 수 있습니다.

웹 페이지 상단에는 현재 대시보드의 URL 을 생성하고 대시보드에 표시된 데이터 스냅샷을 확인할 수 있는 **대시보드 공유(Share Dashboard)** 아이콘이 있습니다. 스냅샷은 사후 검토나 정전으로 인한 보고서를 작성하는 경우처럼, 대시보드의 현재 상태를 보존하려는 경우에 매우 적합합니다.