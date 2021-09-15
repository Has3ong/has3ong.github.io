---
title:  "Spring Boot AOP 를 이용하여 로그를 작성하고 ELK 스택 연동 -2-"
excerpt: "Spring Boot AOP 를 이용하여 로그를 작성하고 ELK 스택 연동 -2-"
categories:
  - Spring
tags:
  - ELK
  - Filebeat
  - Elastic Search
  - Kibana
  - Log
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

위 포스트는 2개로 나누어서 -1- 에서는 Spring Boot 를 설정 및 로그를 출력하여 파일에 저장하기까지 과정을 작성하겠습니다. -2- 에서는 ELK 를 실제로 윈도우 환경에 설치하여 Filebeat 를 이용하여 수집하고 Elasticsearch 에 저장하여 Kibana 에 Visualization 하겠습니다.

ELK 에는 shard, replica 와 같이 다양한 속성이 있지만, 현 포스트에서는 다루지 않겠습니다.

## ELK 란?

![elkstac](https://user-images.githubusercontent.com/80693904/123505606-16756780-d69b-11eb-87bc-762379c3312e.jpg)

ELK 란 Elasticsearch, Logstash, Kibana 이 오픈 소스 프로젝트의 3개의 머리글자입니다.

Elasticsearch 는 검색 및 분석 엔진입니다. Logstash는 여러 소스에서 동시에 데이터를 수집하여 변환한 후 Elasticsearch 같은 “stash”로 전송하는 서버 사이드 데이터 처리 파이프라인입니다. Kibana는 사용자가 Elasticsearch에서 차트와 그래프를 이용해 데이터를 시각화할 수 있게 해줍니다.

현재 ELK 솔루션에서 Beats 가 추가되며 ELK Stack 이라고 불립니다. Beats 는 서버의 에이전트로 설치하여 다양한 유형의 데이터를 Elasticsearch 나 Logstash 로 전송하는 오픈 소스 데이터 발송자입니다.

Filebeat 와 LogStash 의 차이를 간단하게 설명하자면 Logstash 가 Filebeat 보다 더 많은 기능을 지원합니다.

### ELK 설치하기

> ElasticSearch, Filebeat, Kibana 모두 Linux 환경에서 구성하실 때 반드시 `chown -R` 명령어를 통해 root 권한을 바꿔주고 진행하셔야 합니다.

Elastic 홈페이지에 접속하여 환경에 맞는 파일을 다운받습니다. 

![1](https://user-images.githubusercontent.com/80693904/123509814-aa9ef900-d6b2-11eb-859f-44e02e299211.PNG)

다운을 받고 압축을 풀면 아래와 같습니다.

![image](https://user-images.githubusercontent.com/80693904/123509837-c2767d00-d6b2-11eb-80cd-d78a5c03f528.png)

다른 설정은 건들 필요없고 `filebeat.yml` 파일을 열어 설정을 바꿔줍니다. 그리고 YAML 파일 설정을 아래처럼 바꿔주면 됩니다.

```yml
filebeat.config:
  modules:
    path: ${path.config}/modules.d/*.yml
    reload.enabled: false

filebeat.inputs:
  - type: log
    paths:
      - "C:\Users\khsh5\Desktop\logs/*.filebeat-*.log"
    ignore_older: 24h

processors:
  - decode_json_fields:
      fields: ["message"]
      max_depth: 1
      target: "filebeat"

setup.ilm.enabled: false
setup.template.overwrite: true
output.elasticsearch:
  hosts: ["localhost:9200"]
  output.elasticsearch.index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

`filebeat.inputs.paths` 는 수집할 로그 파일의 위치의 파일 형태를 작성하시면 됩니다.


```json
{"timestamp":"2021-06-24 22:06:03.138","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_REQ","parameter":"{\"param1\":[\"filebeat\"],\"framework\":[\"springboot\"],\"language\":[\"java\"]}"}
{"timestamp":"2021-06-24 22:06:03.234","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_REQ","parameter":"[{\"param1\":\"filebeat\",\"framework\":\"springboot\",\"language\":\"java\"}]"}
{"timestamp":"2021-06-24 22:06:03.246","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.service.AOPServiceImpl.index","type":"SERVICE_RES","parameter":"{\"param1\":\"filebeat\",\"framework\":\"springboot\",\"language\":\"java\"}"}
{"timestamp":"2021-06-24 22:06:03.247","hostname":"DESKTOP-R07FVQK","hostIp":"192.168.35.6","clientIp":"0:0:0:0:0:0:0:1","clientUrl":"http://localhost:8080/index","callFunction":"com.example.demo.controller.AOPController.index","type":"CONTROLLER_RES","parameter":"\"index.jsp\""}
```

`processors` 항목은 위와 같이 문자열 형태로 들어오는 로그 메세지를 JSON 형식으로 변환해줍니다.

마지막으로 `output.elasticsearch` 속성은 수집한 로그를 어디로 보낼지 정하는 속성입니다. elasticsearch, kafka, logstash 등등 다양하게 보낼 수 있습니다.

### Filebeat 실행하기

터미널을 켜서 아래 명령어를 입력해 Filebeat 를 실행시킵니다.

```
$ .\filebeat.exe -c .\filebeat.yml -e
```

`-c` 는 Filebeat 를 실행할 때 설정파일을 지정하며 `-e` 는 로그를 출력합니다.

```
2021-06-26T19:41:30.609+0900    INFO    instance/beat.go:665    Home path: [C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64] Config path: [C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64] Data path: [C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64\data] Logs path: [C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64\logs]
2021-06-26T19:41:30.610+0900    INFO    instance/beat.go:673    Beat ID: 57a1349d-2e5e-4658-8072-432d515c4065
2021-06-26T19:41:30.610+0900    INFO    [beat]  instance/beat.go:1014   Beat info       {"system_info": {"beat": {"path": {"config": "C:\\Users\\khsh5\\Desktop\\새 폴더\\filebeat-7.13.2-windows-x86_64", "data": "C:\\Users\\khsh5\\Desktop\\새 폴더\\filebeat-7.13.2-windows-x86_64\\data", "home": "C:\\Users\\khsh5\\Desktop\\새 폴더\\filebeat-7.13.2-windows-x86_64", "logs": "C:\\Users\\khsh5\\Desktop\\새 폴더\\filebeat-7.13.2-windows-x86_64\\logs"}, "type": "filebeat", "uuid": "57a1349d-2e5e-4658-8072-432d515c4065"}}}
2021-06-26T19:41:30.610+0900    INFO    [beat]  instance/beat.go:1023   Build info      {"system_info": {"build": {"commit": "686ba416a74193f2e69dcfa2eb142f4364a79307", "libbeat": "7.13.2", "time": "2021-06-10T21:04:13.000Z", "version": "7.13.2"}}}
2021-06-26T19:41:30.610+0900    INFO    [beat]  instance/beat.go:1026   Go runtime info {"system_info": {"go": {"os":"windows","arch":"amd64","max_procs":12,"version":"go1.15.13"}}}
2021-06-26T19:41:30.664+0900    INFO    [beat]  instance/beat.go:1030   Host info       {"system_info": {"host": {"architecture":"x86_64","boot_time":"2021-06-14T19:53:20.09+09:00","name":"DESKTOP-R07FVQK","ip":["fe80::48e5:d68c:2138:3c4a/64","192.168.35.6/24","fe80::29a0:c101:5216:151e/64","169.254.21.30/16","fe80::3485:d527:3435:78e8/64","169.254.120.232/16","fe80::201e:38f6:4356:8669/64","169.254.134.105/16","fe80::e5e4:8f16:c95c:14d6/64","169.254.20.214/16","::1/128","127.0.0.1/8"],"kernel_version":"10.0.19041.1052 (WinBuild.160101.0800)","mac":["00:e0:4c:68:15:7e","14:f6:d8:ee:9c:60","14:f6:d8:ee:9c:61","16:f6:d8:ee:9c:60","14:f6:d8:ee:9c:64"],"os":{"type":"windows","family":"windows","platform":"windows","name":"Windows 10 Home","version":"10.0","major":10,"minor":0,"patch":0,"build":"19042.1052"},"timezone":"KST","timezone_offset_sec":32400,"id":"f1e0a85c-bc1c-439c-bd8d-a7e1f561ccbd"}}}
2021-06-26T19:41:30.665+0900    INFO    [beat]  instance/beat.go:1059   Process info    {"system_info": {"process": {"cwd": "C:\\Users\\khsh5\\Desktop\\새 폴더\\filebeat-7.13.2-windows-x86_64", "exe": "C:\\Users\\khsh5\\Desktop\\\ufffd\ufffd \ufffd\ufffd\ufffd\ufffd\\filebeat-7.13.2-windows-x86_64\\filebeat.exe", "name": "filebeat.exe", "pid": 10760, "ppid": 11284, "start_time": "2021-06-26T19:41:30.408+0900"}}}
2021-06-26T19:41:30.665+0900    INFO    instance/beat.go:309    Setup Beat: filebeat; Version: 7.13.2
2021-06-26T19:41:30.665+0900    INFO    eslegclient/connection.go:99    elasticsearch url: http://localhost:9200
2021-06-26T19:41:30.666+0900    INFO    [publisher]     pipeline/module.go:113  Beat name: DESKTOP-R07FVQK
2021-06-26T19:41:30.671+0900    INFO    instance/beat.go:473    filebeat start running.
2021-06-26T19:41:30.671+0900    INFO    [monitoring]    log/log.go:117  Starting metrics logging every 30s
2021-06-26T19:41:30.673+0900    INFO    memlog/store.go:119     Loading data file of 'C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64\data\registry\filebeat' succeeded. Active transaction id=0
2021-06-26T19:41:30.673+0900    INFO    memlog/store.go:124     Finished loading transaction log file for 'C:\Users\khsh5\Desktop\새 폴더\filebeat-7.13.2-windows-x86_64\data\registry\filebeat'. Active transaction id=0
2021-06-26T19:41:30.673+0900    INFO    [registrar]     registrar/registrar.go:109      States Loaded from registrar: 0
2021-06-26T19:41:30.673+0900    INFO    [crawler]       beater/crawler.go:71    Loading Inputs: 1
2021-06-26T19:41:30.680+0900    INFO    log/input.go:157        Configured paths: [C:\Users\khsh5\Desktop\logs\*.filebeat-*.log]
2021-06-26T19:41:30.681+0900    INFO    [crawler]       beater/crawler.go:141   Starting input (ID: 6921238670259708846)
2021-06-26T19:41:30.681+0900    INFO    [crawler]       beater/crawler.go:108   Loading and starting Inputs completed. Enabled inputs: 1
2021-06-26T19:41:30.682+0900    INFO    cfgfile/reload.go:164   Config reloader started
2021-06-26T19:41:30.682+0900    INFO    cfgfile/reload.go:224   Loading of config files completed.
2021-06-26T19:41:30.684+0900    INFO    log/harvester.go:302    Harvester started for file: C:\Users\khsh5\Desktop\logs\DESKTOP-R07FVQK.filebeat-2021-06-26.0.log
2021-06-26T19:42:00.673+0900    INFO    [monitoring]    log/log.go:144  Non-zero metrics in the last 30s        {"monitoring": {"metrics": {"beat":{"cpu":{"system":{"ticks":125,"time":{"ms":125}},"total":{"ticks":203,"time":{"ms":203},"value":203},"user":{"ticks":78,"time":{"ms":78}}},"handles":{"open":229},"info":{"ephemeral_id":"3086b266-75db-4017-97d3-31f5c7b98805","uptime":{"ms":30132}},"memstats":{"gc_next":18039552,"memory_alloc":9409264,"memory_sys":33594536,"memory_total":43314464,"rss":53612544},"runtime":{"goroutines":31}},"filebeat":{"events":{"added":2,"done":2},"harvester":{"open_files":1,"running":1,"started":1}},"libbeat":{"config":{"module":{"running":0},"reloads":1,"scans":1},"output":{"events":{"active":0},"type":"elasticsearch"},"pipeline":{"clients":1,"events":{"active":0,"filtered":2,"total":2},"queue":{"max_events":4096}}},"registrar":{"states":{"current":2,"update":2},"writes":{"success":2,"total":2}},"system":{"cpu":{"cores":12}}}}}
2021-06-26T19:42:30.672+0900    INFO    [monitoring]    log/log.go:144  Non-zero metrics in the last 30s        {"monitoring": {"metrics": {"beat":{"cpu":{"system":{"ticks":125},"total":{"ticks":203,"value":203},"user":{"ticks":78}},"handles":{"open":231},"info":{"ephemeral_id":"3086b266-75db-4017-97d3-31f5c7b98805","uptime":{"ms":60132}},"memstats":{"gc_next":18039552,"memory_alloc":9520248,"memory_total":43425448,"rss":53649408},"runtime":{"goroutines":31}},"filebeat":{"harvester":{"open_files":1,"running":1}},"libbeat":{"config":{"module":{"running":0}},"output":{"events":{"active":0}},"pipeline":{"clients":1,"events":{"active":0}}},"registrar":{"states":{"current":2}}}}}
2021-06-26T19:42:46.736+0900    INFO    [publisher_pipeline_output]     pipeline/output.go:143  Connecting to backoff(elasticsearch(http://localhost:9200))
2021-06-26T19:42:46.736+0900    INFO    [publisher]     pipeline/retry.go:219   retryer: send unwait signal to consumer
2021-06-26T19:42:46.737+0900    INFO    [publisher]     pipeline/retry.go:223     done
2021-06-26T19:42:46.762+0900    INFO    [esclientleg]   eslegclient/connection.go:314   Attempting to connect to Elasticsearch version 7.13.2
2021-06-26T19:42:46.775+0900    INFO    [esclientleg]   eslegclient/connection.go:314   Attempting to connect to Elasticsearch version 7.13.2
2021-06-26T19:42:46.779+0900    INFO    template/load.go:228    Existing template will be overwritten, as overwrite is enabled.
2021-06-26T19:42:47.695+0900    INFO    template/load.go:131    Try loading template filebeat-7.13.2 to Elasticsearch
2021-06-26T19:42:47.946+0900    INFO    template/load.go:123    template with name 'filebeat-7.13.2' loaded.
2021-06-26T19:42:47.946+0900    INFO    [index-management]      idxmgmt/std.go:297      Loaded index template.
2021-06-26T19:42:47.948+0900    INFO    [publisher_pipeline_output]     pipeline/output.go:151  Connection to backoff(elasticsearch(http://localhost:9200)) established
```

### ElasticSearch 실행하기

ElasticSearch 는 `./bin/elasticsearch.bat` 파일을 실행시키면 됩니다.

```
$ ./bin/elasticsearch.bat
```

```
[2021-06-26T19:24:24,661][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] version[7.13.2], pid[8028], build[default/zip/4d960a0733be83dd2543ca018aa4ddc42e956800/2021-06-10T21:01:55.251515791Z], OS[Windows 10/10.0/amd64], JVM[AdoptOpenJDK/OpenJDK 64-Bit Server VM/16/16+36]
[2021-06-26T19:24:24,666][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] JVM home [C:\Users\khsh5\Desktop\???대뜑\elasticsearch-7.13.2\jdk], using bundled JDK [true]
]
[2021-06-26T19:24:24,667][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] JVM arguments [-Des.networkaddress.cache.ttl=60, -Des.networkaddress.cache.negative.ttl=10, -XX:+AlwaysPreTouch, -Xss1m, -Djava.awt.headless=true, -Dfile.encoding=UTF-8, -Djna.nosys=true, -XX:-OmitStackTraceInFastThrow, -XX:+ShowCodeDetailsInExceptionMessages, -Dio.netty.noUnsafe=true, -Dio.netty.noKeySetOptimization=true, -Dio.netty.recycler.maxCapacityPerThread=0, -Dio.netty.allocator.numDirectArenas=0, -Dlog4j.shutdownHookEnabled=false, -Dlog4j2.disable.jmx=true, -Djava.locale.providers=SPI,COMPAT, --add-opens=java.base/java.io=ALL-UNNAMED, -XX:+UseG1GC, -Djava.io.tmpdir=C:\Users\khsh5\AppData\Local\Temp\elasticsearch, -XX:+HeapDumpOnOutOfMemoryError, -XX:HeapDumpPath=data, -XX:ErrorFile=logs/hs_err_pid%p.log, -Xlog:gc*,gc+age=trace,safepoint:file=logs/gc.log:utctime,pid,tags:filecount=32,filesize=64m, -Xms8051m, -Xmx8051m, -XX:MaxDirectMemorySize=4221566976, -XX:G1HeapRegionSize=4m, -XX:InitiatingHeapOccupancyPercent=30, -XX:G1ReservePercent=15, -Delasticsearch, -Des.path.home=C:\Users\khsh5\Desktop\???대뜑\elasticsearch-7.13.2, -Des.path.conf=C:\Users\khsh5\Desktop\???대뜑\elasticsearch-7.13.2\config, -Des.distribution.flavor=default, -Des.distribution.type=zip, -Des.bundled_jdk=true]
rue]
[2021-06-26T19:24:32,880][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [aggs-matrix-stats]
[2021-06-26T19:24:32,880][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [analysis-common]
[2021-06-26T19:24:32,881][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [constant-keyword]
[2021-06-26T19:24:32,881][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [frozen-indices]
[2021-06-26T19:24:32,881][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [ingest-common]
[2021-06-26T19:24:32,882][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [ingest-geoip]
[2021-06-26T19:24:32,882][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [ingest-user-agent]
[2021-06-26T19:24:32,882][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [kibana]
[2021-06-26T19:24:32,882][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [lang-expression]
[2021-06-26T19:24:32,883][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [lang-mustache]
[2021-06-26T19:24:32,883][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [lang-painless]
[2021-06-26T19:24:32,883][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [mapper-extras]
[2021-06-26T19:24:32,883][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [mapper-version]
[2021-06-26T19:24:32,884][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [parent-join]
[2021-06-26T19:24:32,884][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [percolator]
[2021-06-26T19:24:32,884][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [rank-eval]
[2021-06-26T19:24:32,885][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [reindex]
[2021-06-26T19:24:32,885][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [repositories-metering-api]
[2021-06-26T19:24:32,885][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [repository-encrypted]
[2021-06-26T19:24:32,885][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [repository-url]
[2021-06-26T19:24:32,886][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [runtime-fields-common]
[2021-06-26T19:24:32,886][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [search-business-rules]
[2021-06-26T19:24:32,886][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [searchable-snapshots]
[2021-06-26T19:24:32,886][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [snapshot-repo-test-kit]
[2021-06-26T19:24:32,887][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [spatial]
[2021-06-26T19:24:32,887][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [transform]
[2021-06-26T19:24:32,887][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [transport-netty4]
[2021-06-26T19:24:32,887][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [unsigned-long]
[2021-06-26T19:24:32,888][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [vectors]
[2021-06-26T19:24:32,888][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [wildcard]
[2021-06-26T19:24:32,888][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-aggregate-metric]
[2021-06-26T19:24:32,888][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-analytics]
[2021-06-26T19:24:32,889][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-async]
[2021-06-26T19:24:32,889][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-async-search]
[2021-06-26T19:24:32,889][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-autoscaling]
[2021-06-26T19:24:32,889][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-ccr]
[2021-06-26T19:24:32,890][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-core]
[2021-06-26T19:24:32,890][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-data-streams]
[2021-06-26T19:24:32,890][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-deprecation]
[2021-06-26T19:24:32,890][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-enrich]
[2021-06-26T19:24:32,891][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-eql]
[2021-06-26T19:24:32,891][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-fleet]
[2021-06-26T19:24:32,891][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-graph]
[2021-06-26T19:24:32,891][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-identity-provider]
[2021-06-26T19:24:32,892][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-ilm]
[2021-06-26T19:24:32,892][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-logstash]
[2021-06-26T19:24:32,892][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-ml]
[2021-06-26T19:24:32,892][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-monitoring]
[2021-06-26T19:24:32,893][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-ql]
[2021-06-26T19:24:32,893][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-rollup]
[2021-06-26T19:24:32,893][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-security]
[2021-06-26T19:24:32,893][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-shutdown]
[2021-06-26T19:24:32,894][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-sql]
[2021-06-26T19:24:32,894][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-stack]
[2021-06-26T19:24:32,894][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-text-structure]
[2021-06-26T19:24:32,894][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-voting-only-node]
[2021-06-26T19:24:32,895][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] loaded module [x-pack-watcher]
[2021-06-26T19:24:32,895][INFO ][o.e.p.PluginsService     ] [DESKTOP-R07FVQK] no plugins loaded
[2021-06-26T19:24:33,459][INFO ][o.e.e.NodeEnvironment    ] [DESKTOP-R07FVQK] using [1] data paths, mounts [[(C:)]], net usable_space [32.4gb], net total_space [498.3gb], types [NTFS]
[2021-06-26T19:24:33,459][INFO ][o.e.e.NodeEnvironment    ] [DESKTOP-R07FVQK] heap size [7.8gb], compressed ordinary object pointers [true]
[2021-06-26T19:24:33,604][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] node name [DESKTOP-R07FVQK], node ID [3ORVXNfgSmWRE6yRjN2yXQ], cluster name [elasticsearch], roles [transform, data_frozen, master, remote_cluster_client, data, ml, data_content, data_hot, data_warm, data_cold, ingest]
[2021-06-26T19:24:37,552][INFO ][o.e.x.m.p.l.CppLogMessageHandler] [DESKTOP-R07FVQK] [controller/12508] [Main.cc@117] controller (64 bit): Version 7.13.2 (Build 4d6c6f14d75f39) Copyright (c) 2021 Elasticsearch BV
[2021-06-26T19:24:38,281][INFO ][o.e.x.s.a.s.FileRolesStore] [DESKTOP-R07FVQK] parsed [0] roles from file [C:\Users\khsh5\Desktop\???대뜑\elasticsearch-7.13.2\config\roles.yml]
]
[2021-06-26T19:24:38,843][INFO ][o.e.i.g.LocalDatabases   ] [DESKTOP-R07FVQK] initialized default databases [[GeoLite2-Country.mmdb, GeoLite2-City.mmdb, GeoLite2-ASN.mmdb]], config databases [[]] and watching [C:\Users\khsh5\Desktop\???대뜑\elasticsearch-7.13.2\config\ingest-geoip] for changes
s
[2021-06-26T19:24:38,846][INFO ][o.e.i.g.DatabaseRegistry ] [DESKTOP-R07FVQK] initialized database registry, using geoip-databases directory [C:\Users\khsh5\AppData\Local\Temp\elasticsearch\geoip-databases\3ORVXNfgSmWRE6yRjN2yXQ]
[2021-06-26T19:24:39,471][INFO ][o.e.t.NettyAllocator     ] [DESKTOP-R07FVQK] creating NettyAllocator with the following configs: [name=elasticsearch_configured, chunk_size=1mb, suggested_max_allocation_size=1mb, factors={es.unsafe.use_netty_default_chunk_and_page_size=false, g1gc_enabled=true, g1gc_region_size=4mb}]
[2021-06-26T19:24:39,531][INFO ][o.e.d.DiscoveryModule    ] [DESKTOP-R07FVQK] using discovery type [zen] and seed hosts providers [settings]
[2021-06-26T19:24:39,924][INFO ][o.e.g.DanglingIndicesState] [DESKTOP-R07FVQK] gateway.auto_import_dangling_indices is disabled, dangling indices will not be automatically detected or imported and must be managed manually
[2021-06-26T19:24:40,294][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] initialized
[2021-06-26T19:24:40,295][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] starting ...
[2021-06-26T19:24:40,305][INFO ][o.e.x.s.c.f.PersistentCache] [DESKTOP-R07FVQK] persistent cache index loaded
[2021-06-26T19:24:40,559][INFO ][o.e.t.TransportService   ] [DESKTOP-R07FVQK] publish_address {127.0.0.1:9300}, bound_addresses {127.0.0.1:9300}, {[::1]:9300}
[2021-06-26T19:24:40,708][WARN ][o.e.b.BootstrapChecks    ] [DESKTOP-R07FVQK] the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
[2021-06-26T19:24:40,721][INFO ][o.e.c.c.ClusterBootstrapService] [DESKTOP-R07FVQK] no discovery configuration found, will perform best-effort cluster bootstrapping after [3s] unless existing master is discovered
[2021-06-26T19:24:43,730][INFO ][o.e.c.c.Coordinator      ] [DESKTOP-R07FVQK] setting initial configuration to VotingConfiguration{3ORVXNfgSmWRE6yRjN2yXQ}
[2021-06-26T19:24:43,878][INFO ][o.e.c.s.MasterService    ] [DESKTOP-R07FVQK] elected-as-master ([1] nodes joined)[{DESKTOP-R07FVQK}{3ORVXNfgSmWRE6yRjN2yXQ}{WnNwmwrfQHG9dpFLrfnv3w}{127.0.0.1}{127.0.0.1:9300}{cdfhilmrstw} elect leader, _BECOME_MASTER_TASK_, _FINISH_ELECTION_], term: 1, version: 1, delta: master node changed {previous [], current [{DESKTOP-R07FVQK}{3ORVXNfgSmWRE6yRjN2yXQ}{WnNwmwrfQHG9dpFLrfnv3w}{127.0.0.1}{127.0.0.1:9300}{cdfhilmrstw}]}
[2021-06-26T19:24:43,950][INFO ][o.e.c.c.CoordinationState] [DESKTOP-R07FVQK] cluster UUID set to [QkhgEGFPRKqO-mCJXzPIQQ]
[2021-06-26T19:24:44,025][INFO ][o.e.c.s.ClusterApplierService] [DESKTOP-R07FVQK] master node changed {previous [], current [{DESKTOP-R07FVQK}{3ORVXNfgSmWRE6yRjN2yXQ}{WnNwmwrfQHG9dpFLrfnv3w}{127.0.0.1}{127.0.0.1:9300}{cdfhilmrstw}]}, term: 1, version: 1, reason: Publication{term=1, version=1}
[2021-06-26T19:24:44,072][WARN ][o.e.c.r.a.DiskThresholdMonitor] [DESKTOP-R07FVQK] high disk watermark [90%] exceeded on [3ORVXNfgSmWRE6yRjN2yXQ][DESKTOP-R07FVQK][C:\Users\khsh5\Desktop\???
대뜑\elasticsearch-7.13.2\data\nodes\0] free: 32.4gb[6.5%], shards will be relocated away from this node; currently relocating away shards totalling [0] bytes; the node is expected to continue to exceed the high disk watermark when these relocations are complete
e
[2021-06-26T19:24:44,082][INFO ][o.e.x.c.t.IndexTemplateRegistry] [DESKTOP-R07FVQK] adding legacy template [.ml-anomalies-] for [ml], because it doesn't exist
[2021-06-26T19:24:44,083][INFO ][o.e.x.c.t.IndexTemplateRegistry] [DESKTOP-R07FVQK] adding legacy template [.ml-state] for [ml], because it doesn't exist
[2021-06-26T19:24:44,083][INFO ][o.e.x.c.t.IndexTemplateRegistry] [DESKTOP-R07FVQK] adding legacy template [.ml-notifications-000001] for [ml], because it doesn't exist
[2021-06-26T19:24:44,084][INFO ][o.e.x.c.t.IndexTemplateRegistry] [DESKTOP-R07FVQK] adding legacy template [.ml-stats] for [ml], because it doesn't exist
[2021-06-26T19:24:44,134][INFO ][o.e.h.AbstractHttpServerTransport] [DESKTOP-R07FVQK] publish_address {127.0.0.1:9200}, bound_addresses {127.0.0.1:9200}, {[::1]:9200}
[2021-06-26T19:24:44,135][INFO ][o.e.n.Node               ] [DESKTOP-R07FVQK] started
[2021-06-26T19:24:44,153][INFO ][o.e.g.GatewayService     ] [DESKTOP-R07FVQK] recovered [0] indices into cluster_state
[2021-06-26T19:24:44,314][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.ml-anomalies-] for index patterns [.ml-anomalies-*]
[2021-06-26T19:24:44,408][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.ml-notifications-000001] for index patterns [.ml-notifications-000001]
[2021-06-26T19:24:44,539][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.ml-stats] for index patterns [.ml-stats-*]
[2021-06-26T19:24:44,628][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.ml-state] for index patterns [.ml-state*]
[2021-06-26T19:24:44,705][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [metrics-settings]
[2021-06-26T19:24:44,798][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [metrics-mappings]
[2021-06-26T19:24:44,883][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [synthetics-settings]
[2021-06-26T19:24:44,972][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [synthetics-mappings]
[2021-06-26T19:24:45,053][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [logs-mappings]
[2021-06-26T19:24:45,135][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding component template [logs-settings]
[2021-06-26T19:24:45,232][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [ilm-history] for index patterns [ilm-history-5*]
[2021-06-26T19:24:45,330][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [.watch-history-13] for index patterns [.watcher-history-13*]
[2021-06-26T19:24:45,417][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [.slm-history] for index patterns [.slm-history-5*]
[2021-06-26T19:24:45,496][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.monitoring-alerts-7] for index patterns [.monitoring-alerts-7]
[2021-06-26T19:24:45,590][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.monitoring-es] for index patterns [.monitoring-es-7-*]
[2021-06-26T19:24:45,676][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.monitoring-kibana] for index patterns [.monitoring-kibana-7-*]
[2021-06-26T19:24:45,762][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.monitoring-logstash] for index patterns [.monitoring-logstash-7-*]
[2021-06-26T19:24:45,846][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding template [.monitoring-beats] for index patterns [.monitoring-beats-7-*]
[2021-06-26T19:24:45,934][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [metrics] for index patterns [metrics-*-*]
[2021-06-26T19:24:46,029][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [synthetics] for index patterns [synthetics-*-*]
[2021-06-26T19:24:46,108][INFO ][o.e.c.m.MetadataIndexTemplateService] [DESKTOP-R07FVQK] adding index template [logs] for index patterns [logs-*-*]
[2021-06-26T19:24:46,184][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [ml-size-based-ilm-policy]
[2021-06-26T19:24:46,273][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [logs]
[2021-06-26T19:24:46,357][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [metrics]
[2021-06-26T19:24:46,433][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [synthetics]
[2021-06-26T19:24:46,507][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [watch-history-ilm-policy]
[2021-06-26T19:24:46,586][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [ilm-history-ilm-policy]
[2021-06-26T19:24:46,663][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [slm-history-ilm-policy]
[2021-06-26T19:24:46,736][INFO ][o.e.x.i.a.TransportPutLifecycleAction] [DESKTOP-R07FVQK] adding index lifecycle policy [.fleet-actions-results-ilm-policy]
[2021-06-26T19:24:46,910][INFO ][o.e.l.LicenseService     ] [DESKTOP-R07FVQK] license [dd25b4c7-5e93-4673-ba6d-529d4019fabb] mode [basic] - valid
[2021-06-26T19:24:46,911][INFO ][o.e.x.s.s.SecurityStatusChangeListener] [DESKTOP-R07FVQK] Active license is now [BASIC]; Security is disabled
[2021-06-26T19:24:46,912][WARN ][o.e.x.s.s.SecurityStatusChangeListener] [DESKTOP-R07FVQK] Elasticsearch built-in security features are not enabled. Without authentication, your cluster could be accessible to anyone. See https://www.elastic.co/guide/en/elasticsearch/reference/7.13/security-minimal-setup.html to enable security.
```

정상적으로 올라왔으면 `localhost:9200` 에 접속하시면 확인할 수 있습니다.

![image](https://user-images.githubusercontent.com/80693904/123510050-4d0bac00-d6b4-11eb-87d8-1a6623c06294.png)

참고로 Chrome 확장 프로그램 elasticsearch-head 를 이용하면 간단한 UI 를 이용할 수 있습니다.

![image](https://user-images.githubusercontent.com/80693904/123510279-75e07100-d6b5-11eb-960c-fc8f02710dc5.png)


### Kibana 실행하기

Kibana 도 마찬가지로 `./bin/kibana.bat` 파일을 실행시키면 됩니다.

```
$ ./bin/kibana.bat
```

```
  log   [19:27:39.366] [info][plugins-service] Plugin "timelines" is disabled.
  log   [19:27:39.432] [warning][config][deprecation] plugins.scanDirs is deprecated and is no longer used
  log   [19:27:39.432] [warning][config][deprecation] Config key [monitoring.cluster_alerts.email_notifications.email_address] will be required for email notifications to work in 8.0."
  log   [19:27:39.674] [info][plugins-system] Setting up [106] plugins: [taskManager,licensing,globalSearch,globalSearchProviders,banners,code,usageCollection,xpackLegacy,telemetryCollectionManager,telemetry,telemetryCollectionXpack,kibanaUsageCollection,securityOss,share,newsfeed,mapsEms,mapsLegacy,kibanaLegacy,translations,licenseApiGuard,legacyExport,embeddable,uiActionsEnhanced,esUiShared,expressions,charts,bfetch,data,home,apmOss,console,consoleExtensions,searchprofiler,painlessLab,grokdebugger,management,advancedSettings,savedObjects,visualizations,visTypeVislib,visTypeVega,visTypeTimelion,features,licenseManagement,watcher,visTypeTagcloud,visTypeMarkdown,visTypeTable,visTypeMetric,visTypeXy,tileMap,regionMap,presentationUtil,canvas,graph,timelion,dashboard,dashboardEnhanced,visualize,visTypeTimeseries,inputControlVis,indexPatternManagement,discover,discoverEnhanced,savedObjectsManagement,spaces,security,savedObjectsTagging,lens,reporting,lists,encryptedSavedObjects,dataEnhanced,dashboardMode,cloud,upgradeAssistant,snapshotRestore,fleet,indexManagement,rollup,remoteClusters,crossClusterReplication,indexLifecycleManagement,enterpriseSearch,beatsManagement,transform,ingestPipelines,fileUpload,maps,fileDataVisualizer,eventLog,actions,alerting,triggersActionsUi,stackAlerts,ruleRegistry,observability,osquery,ml,securitySolution,cases,infra,monitoring,logstash,apm,uptime]
  log   [19:27:39.676] [info][plugins][taskManager] TaskManager is identified by the Kibana UUID: 9543a33f-55d2-46b6-813f-7b34662fd3c2
  log   [19:27:40.415] [warning][config][plugins][security] Generating a random key for xpack.security.encryptionKey. To prevent sessions from being invalidated on restart, please set xpack.security.encryptionKey in the kibana.yml or use the bin/kibana-encryption-keys command.
  log   [19:27:40.416] [warning][config][plugins][security] Session cookies will be transmitted over insecure connections. This is not recommended.
  log   [19:27:40.450] [warning][config][plugins][reporting] Generating a random key for xpack.reporting.encryptionKey. To prevent sessions from being invalidated on restart, please set xpack.reporting.encryptionKey in the kibana.yml or use the bin/kibana-encryption-keys command.
  log   [19:27:40.455] [info][config][plugins][reporting] Chromium sandbox provides an additional layer of protection, and is supported for Win32 OS. Automatically enabling Chromium sandbox.
  log   [19:27:40.456] [warning][encryptedSavedObjects][plugins] Saved objects encryption key is not set. This will severely limit Kibana functionality. Please set xpack.encryptedSavedObjects.encryptionKey in the kibana.yml or use the bin/kibana-encryption-keys command.
  log   [19:27:40.543] [warning][actions][actions][plugins] APIs are disabled because the Encrypted Saved Objects plugin is missing encryption key. Please set xpack.encryptedSavedObjects.encryptionKey in the kibana.yml or use the bin/kibana-encryption-keys command.
  log   [19:27:40.553] [warning][alerting][alerting][plugins][plugins] APIs are disabled because the Encrypted Saved Objects plugin is missing encryption key. Please set xpack.encryptedSavedObjects.encryptionKey in the kibana.yml or use the bin/kibana-encryption-keys command.
  log   [19:27:40.613] [info][monitoring][monitoring][plugins] config sourced from: production cluster
  log   [19:27:40.785] [info][savedobjects-service] Waiting until all Elasticsearch nodes are compatible with Kibana before starting saved objects migrations...
  log   [19:27:40.846] [info][savedobjects-service] Starting saved objects migrations
  log   [19:27:40.883] [info][savedobjects-service] [.kibana] INIT -> CREATE_NEW_TARGET. took: 17ms.
  log   [19:27:40.890] [info][savedobjects-service] [.kibana_task_manager] INIT -> CREATE_NEW_TARGET. took: 22ms.
  log   [19:27:41.316] [info][savedobjects-service] [.kibana_task_manager] CREATE_NEW_TARGET -> MARK_VERSION_INDEX_READY. took: 426ms.
  log   [19:27:41.396] [info][savedobjects-service] [.kibana] CREATE_NEW_TARGET -> MARK_VERSION_INDEX_READY. took: 513ms.
  log   [19:27:41.473] [info][savedobjects-service] [.kibana_task_manager] MARK_VERSION_INDEX_READY -> DONE. took: 157ms.
  log   [19:27:41.474] [info][savedobjects-service] [.kibana_task_manager] Migration completed after 606ms
  log   [19:27:41.549] [info][savedobjects-service] [.kibana] MARK_VERSION_INDEX_READY -> DONE. took: 153ms.
  log   [19:27:41.549] [info][savedobjects-service] [.kibana] Migration completed after 683ms
  log   [19:27:41.574] [info][plugins-system] Starting [106] plugins: [taskManager,licensing,globalSearch,globalSearchProviders,banners,code,usageCollection,xpackLegacy,telemetryCollectionManager,telemetry,telemetryCollectionXpack,kibanaUsageCollection,securityOss,share,newsfeed,mapsEms,mapsLegacy,kibanaLegacy,translations,licenseApiGuard,legacyExport,embeddable,uiActionsEnhanced,esUiShared,expressions,charts,bfetch,data,home,apmOss,console,consoleExtensions,searchprofiler,painlessLab,grokdebugger,management,advancedSettings,savedObjects,visualizations,visTypeVislib,visTypeVega,visTypeTimelion,features,licenseManagement,watcher,visTypeTagcloud,visTypeMarkdown,visTypeTable,visTypeMetric,visTypeXy,tileMap,regionMap,presentationUtil,canvas,graph,timelion,dashboard,dashboardEnhanced,visualize,visTypeTimeseries,inputControlVis,indexPatternManagement,discover,discoverEnhanced,savedObjectsManagement,spaces,security,savedObjectsTagging,lens,reporting,lists,encryptedSavedObjects,dataEnhanced,dashboardMode,cloud,upgradeAssistant,snapshotRestore,fleet,indexManagement,rollup,remoteClusters,crossClusterReplication,indexLifecycleManagement,enterpriseSearch,beatsManagement,transform,ingestPipelines,fileUpload,maps,fileDataVisualizer,eventLog,actions,alerting,triggersActionsUi,stackAlerts,ruleRegistry,observability,osquery,ml,securitySolution,cases,infra,monitoring,logstash,apm,uptime]
  log   [19:27:46.193] [info][server][Kibana][http] http server running at http://localhost:5601
  log   [19:27:46.534] [info][plugins][reporting] Browser executable: C:\Users\khsh5\Desktop\새 폴더\kibana-7.13.2-windows-x86_64\x-pack\plugins\reporting\chromium\chrome-win\chrome.exe
  log   [19:27:46.593] [info][kibana-monitoring][monitoring][monitoring][plugins] Starting monitoring stats collection
  log   [19:27:48.590] [info][plugins][securitySolution] Dependent plugin setup complete - Starting ManifestTask
```

마찬가지로 `localhost:5601` 에서 확인할 수 있습니다.

![image](https://user-images.githubusercontent.com/80693904/123510175-0ec2bc80-d6b5-11eb-9a9c-04f2cd440bd2.png)

### 로그 확인 및 Kibana 에서 출력

이제 `localhost:8080` 에 접속하여 로그가 Filebeat 로 수집이 되는지 확인하는 일만 남았습니다.

로그 수집이 정상저거으로 작동하면 아래와 같이 새로운 인덱스 `filebeat-7.13.2-2021.06.26` 가 생성됩니다.

![image](https://user-images.githubusercontent.com/80693904/123510516-079cae00-d6b7-11eb-9c0c-951c45ba8a4c.png)

이제 수집한 로그를 시각화하기 위해 `localhost:5601` 키바나 서버로 접속한 후 Dashboard 메뉴로 들어갑니다.

![image](https://user-images.githubusercontent.com/80693904/123510579-55191b00-d6b7-11eb-99b6-4c6a34970e7c.png)

Create new Dashboard 버튼을 누릅니다.

![image](https://user-images.githubusercontent.com/80693904/123510589-64986400-d6b7-11eb-94c4-69bf3330e460.png)

Create Index 버튼을 누릅니다.

![image](https://user-images.githubusercontent.com/80693904/123510602-75e17080-d6b7-11eb-85d5-f41077d20dca.png)

인덱스 패턴을 입력하고 

![image](https://user-images.githubusercontent.com/80693904/123510602-75e17080-d6b7-11eb-85d5-f41077d20dca.png)

Timefield 를 `@timestamp` 로 설정한 후 인덱스 패턴을 생성하면 됩니다.

![image](https://user-images.githubusercontent.com/80693904/123510620-8f82b800-d6b7-11eb-80ef-a44bb3acef20.png)

생성이 완료되면 Dashboard 로 돌아와서 Create Visualization 버튼을 클릭합니다.

![image](https://user-images.githubusercontent.com/80693904/123510634-a5907880-d6b7-11eb-93df-36b503de792d.png)

이제 원하는대로 데이터를 시각화해서 보여주면 됩니다.

![image](https://user-images.githubusercontent.com/80693904/123510720-0ddf5a00-d6b8-11eb-9c4b-56d96ce61b54.png)

[사이트](/https://www.elastic.co/kr/demos) 를 클릭하여 접속하시면 다양한 Kibana 대쉬보드 예제를 살펴볼 수 있습니다.


### 추가사항

filebeat 로 수집한 로그 중에 Parameter 값이 `{\"param\":\"1\"}` 이와 같이 들어가서 파싱이 안되는 경우가 있습니다.

위 같은 경우 Filebeat -> Logstash -> Elasticsearch 방식으로 중간에 Logstash 를 이용하여 필터링하시면 됩니다.

* 참고자료
  * [Elastic Stack and Product Documentation](/https://www.elastic.co/guide/index.html)