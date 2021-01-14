---
title : Elastic Search Getting Started 
tags :
- Elasticsearch
- Logstash
- Kibana
---

[Getting started with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html) 이 자료 참고하여 포스트 작성하였습니다.

설치부터 실행, 시각화까지 진행하겠습니다. 개인 공부 기록용으로 만든 자료라 설명이 부실합니다. 참고해주세요.

### ELK Installation

3 시스템 모두 brew 이용하여 설치할 수 있습니다. 그리고 설치 이전에 java8 버전 이상 설치되어 있어야 합니다.

```shell
$ java -version
java version "1.8.0_241"
Java(TM) SE Runtime Environment (build 1.8.0_241-b07)
Java HotSpot(TM) 64-Bit Server VM (build 25.241-b07, mixed mode)
```

아래 명령어를 이용하여 설치할 수 있습니다.

```shell
$ brew tap elastic/tap
$ brew install elastic/tap/elasticsearch-full
$ brew install elastic/tap/kibana-full
$ brew install elastic/tap/logstash-full
```

그리고 시작해보겠습니다. logstash 현 포스트 외에 다른 포스트에서 추가로 다루겠습니다.

```
$ brew services start elastic/tap/elasticsearch-full
$ brew services start elastic/tap/kibana-full
$ brew services start elastic/tap/logstash-full

$ brew services list
Name               Status  User    Plist
elasticsearch-full started has3ong /Users/has3ong/Library/LaunchAgents/homebrew.mxcl.elasticsearch-full.plist
kibana-full        started has3ong /Users/has3ong/Library/LaunchAgents/homebrew.mxcl.kibana-full.plist
logstash-full      stopped
```

그리고 각각 `localhost:9200`, `localhost:5601` 로 접속하면 elasticsearch 와 kibana 로 접속할 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/104570656-92539880-5695-11eb-8286-95311031d197.png)

![image](https://user-images.githubusercontent.com/44635266/104570661-92ec2f00-5695-11eb-9323-0d0fe8893934.png)

이제 제공해주는 데이터를 다운받아 보겠습니다.

```shell
$ curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/shakespeare.json
$ curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/accounts.zip
$ curl -O https://download.elastic.co/demos/kibana/gettingstarted/8.x/logs.jsonl.gz
$ unzip accounts.zip gunzip logs.jsonl.gz
```

각각의 데이터 구조를 살펴볼게요.

> shakespeare

```json
{
    "line_id": INT,
    "play_name": "String",
    "speech_number": INT,
    "line_number": "String",
    "speaker": "String",
    "text_entry": "String",
}
```

> accounts

```json
{
    "account_number": INT,
    "balance": INT,
    "firstname": "String",
    "lastname": "String",
    "age": INT,
    "gender": "M or F",
    "address": "String",
    "employer": "String",
    "email": "String",
    "city": "String",
    "state": "String"
}
```

> logs

```json
{
    "memory": INT,
    "geo.coordinates": "geo_point"
    "@timestamp": "date"
}
```

그리고 이 데이터들을 elasticsearch 에다가 매핑을 해줍니다.

```shell
curl -u elastic -H 'Content-Type: application/x-ndjson' -XPOST '<host>:<port>/bank/_bulk?pretty' --data-binary @accounts.json
curl -u elastic -H 'Content-Type: application/x-ndjson' -XPOST '<host>:<port>/shakespeare/_bulk?pretty' --data-binary @shakespeare.json
curl -u elastic -H 'Content-Type: application/x-ndjson' -XPOST '<host>:<port>/_bulk?pretty' --data-binary @logs.jsonl
```

`<host>` 와 `<port>` 값만 수정해서 넣으시면 됩니다.

그리고 kibana 의 DevTools 나 http://localhost:9200 에 `GET _cat/indices?v` 값을 입력하면 아래와 같이 추가한 데이터셋 인덱스가 보입니다.

```shell
health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   bank                            gIs8AAK0QvOOWJBYwAQg0w   1   1       1000            0    379.3kb        379.3kb
yellow open   shakespeare                     0b9fkWqAQeGOI4Sg3HGS5A   1   1     111396            0     18.
yellow open   logstash-2015.05.18             Z7edFomnTmymmJuEA1hbtg   1   1       4631            0     14.7mb         14.7mb
yellow open   logstash-2015.05.19             26XoYFkeQQKFINxBAoXDTw   1   1       4624            0     14.9mb         14.9mb
yellow open   logstash-2015.05.20             oKb2dAHDTBSHApduSfurwQ   1   1       4750            0     15.9mb         15.9mb
```

위와 같이 표시가 된다면 정확하게 데이터가 적재된것입니다.

이제 이 데이터들을 가지고 시각화를 해보겠습니다.

### Create Index Pattern

먼저 Index Patterns 페이지로 가서 `ba*` 를 입력하고 Create Index Pattern 버튼을 눌러줍니다.

![image](https://user-images.githubusercontent.com/44635266/104574241-25da9880-5699-11eb-8dc4-2c5342924091.png)

그러면 이전에 매핑을 해논 bank 데이터가 표시가 됩니다. 해당 데이터를 체크하고 Next step 버튼을 눌러줍니다. 그리고 Create Index pattern 버튼을 눌러줍니다.

![image](https://user-images.githubusercontent.com/44635266/104574246-26732f00-5699-11eb-97a4-6c15cb533d1f.png)

![image](https://user-images.githubusercontent.com/44635266/104574251-27a45c00-5699-11eb-890c-b7cf53ef1f93.png)

shakespear 데이터도 마찬가지로 진행하면됩니다.

log 데이터 같은 경우 위 데이터랑은 다르게 처리합니다.

마찬가지로 `logstash-2015.05.*` 까지 입력해줍니다.

![image](https://user-images.githubusercontent.com/44635266/104574252-28d58900-5699-11eb-8e95-1906a1ccb373.png)

이전 데이터와는 다르게 해당 데이터는 시계열 데이터라 시간 필드를 선언해줘야 합니다. `timestamp`, `utc_time` 아무거나 상관없습니다.

![image](https://user-images.githubusercontent.com/44635266/104574258-296e1f80-5699-11eb-998a-7c4168b2dc8c.png)

생성하기전에 Show advanced settings 버튼을 클릭합니다. `logstash-2015.05.*` 데이터의 경우 `geo.coordinates` 변수 타입이 `geo_point` 인것을 꼭 확인해야 합니다.

![image](https://user-images.githubusercontent.com/44635266/104574263-2a9f4c80-5699-11eb-8d87-fcd15dcba70f.png)

![image](https://user-images.githubusercontent.com/44635266/104574258-296e1f80-5699-11eb-998a-7c4168b2dc8c.png)

이제 시각화 준비가 끝났으니 Dashboard 로 넘어갑니다.

### Dashboards

대시보드는 우리가 설정한 데이터의 상태를 보는 화면이라 생각하시면 됩니다. Grafana 의 Dahsboard 와 유사합니다.

![image](https://user-images.githubusercontent.com/44635266/104575472-74d4fd80-569a-11eb-9b59-bbeadf888a48.png)

우리는 만들어논 Dashboard 가 없으니 Create dashboard 버튼을 클릭합니다.

그러면 어떤 차트나 방식을 통해서 데이터를 시각화할지 선택할 수 있습니다. 저는 Metric 을 이용해보겠습니다.

![image](https://user-images.githubusercontent.com/44635266/104575631-9635e980-569a-11eb-93df-8f625182c46e.png)

bank 데이터를 이용하겠습니다.

![image](https://user-images.githubusercontent.com/44635266/104575652-9c2bca80-569a-11eb-8e1a-563dbe17b31d.png)

아래와 같이 bank 데이터의 개수를 보여주는 화면이 나옵니다. 오른쪽 탭에서 집계 함수를 선택할 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/104575664-a221ab80-569a-11eb-8f66-985fd05ddbc8.png)

현 데이터에서는 간단하게 Save 만 하여 진행하겠습니다.

![image](https://user-images.githubusercontent.com/44635266/104575690-a9e15000-569a-11eb-879b-7adaafd4021a.png)

Save 를 한뒤에 Dashboard 를 가서 Add 버튼을 누르면 이전에 저장해두었던 Metric 을 불러와서 Dashboard 에 위치시킬 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/104575715-afd73100-569a-11eb-9934-d81129ce5837.png)

![image](https://user-images.githubusercontent.com/44635266/104575732-b665a880-569a-11eb-9048-c44aefc59bf2.png)

다음은 shakespeare 데이터로 pie 차트를 만들어 보겠습니다. 아래 사진부터는 필요한 설명만 하고 그림으로만 진행하겠습니다.

![image](https://user-images.githubusercontent.com/44635266/104575738-b796d580-569a-11eb-8a61-52f520feeee6.png)

![image](https://user-images.githubusercontent.com/44635266/104575772-bfef1080-569a-11eb-8f39-c6e01aebb000.png)

![image](https://user-images.githubusercontent.com/44635266/104575785-c5e4f180-569a-11eb-920c-58bd37963573.png)

![image](https://user-images.githubusercontent.com/44635266/104575848-d6956780-569a-11eb-93b8-e3f264fb338a.png)

pie 차트도 저장을 하고 나서, 마지막으로 `log` 데이터를 Map 으로 진행하겠습니다.

![image](https://user-images.githubusercontent.com/44635266/104576396-7a7f1300-569b-11eb-95d9-32a349039399.png)

Map 버튼을 누른 후 Add Layer 버튼을 누릅니다.

![image](https://user-images.githubusercontent.com/44635266/104576424-82d74e00-569b-11eb-8be9-ad6186972e15.png)

오른쪽 탭에서 Documents 를 클릭한 후에 이전에 만들어 둔 `logstash-2015.05.8` 을 선택해줍니다.

![image](https://user-images.githubusercontent.com/44635266/104576496-98e50e80-569b-11eb-98ac-cb3e849f4dc4.png)

선택을 완료하면 Map 의 아무런 변화가 없는데 이유는 해당 데이터가 2015 년 기준이고, 현재 날짜는 2021 년이기 때문에 아무런 변화가 없습니다.

![image](https://user-images.githubusercontent.com/44635266/104576513-a00c1c80-569b-11eb-9241-c27c5f3cb47b.png)

상단에 있는 달력을 클릭한 후 날짜를 맞춰줍니다.

![image](https://user-images.githubusercontent.com/44635266/104576563-b87c3700-569b-11eb-82fd-6355f9efdf30.png)

그러면 데이터가 정상적으로 표시가 되는걸 확인할 수 있습니다.

마찬가지로 Save 버튼을 눌러서 저장을 해줍니다.

![image](https://user-images.githubusercontent.com/44635266/104576595-c0d47200-569b-11eb-8733-d15cc31b6a67.png)

Dashboard 로 가서 Add 버튼을 눌러 이전에 만들어뒀던 차트들을 추가해줍니다. 각각의 차트나 맵 크기도 변경이 가능합니다.

![image](https://user-images.githubusercontent.com/44635266/104576615-c6ca5300-569b-11eb-8244-788215556937.png)

