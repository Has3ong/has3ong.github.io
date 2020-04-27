---
title : Prometheus Node Exporter
tags :
- Collector
- Node Exporter
- Prometheus
---

*이 포스트는 [Prometheus: Up & Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/prometheus_upandrunning.pdf)를 바탕으로 작성하였습니다.*

**노드 익스포터(Node Exporter)** 는 첫 번째로 사용할 가능성이 높은 익스포터 중 하나입니다. 노드 익스포터는 CPU, 메모레, 디스크 공간, 디스크 I/O, 네트워크 대역 등 운영 시스템 커널에서 오는 머신 수준의 메트릭을 게시합니다.

노드 익스포터는 머신 자체를 모니터링하기 위한것이지 개별 프로세스나 서비스를 모니터링 위한것이 아닙니다. 그 밖의 모니터링 시스템에는 머신의 모든 사항을 모니터링하는 단일 프로세스인 **우버에이전트(Uberagent)** 가 있습니다. Prometheus 아키텍처에서 각 서비스는 익스포터를 사용해 자체 메트릭을 **게시(expose)** 합니다.

필요한 경우, Prometheus 가 직접 데이터를 수집합니다. 이를 우버에이전트가 운영상이나 성능 면에서 병목현상이 되는 것을 방지할 수 있으며, 사용자는 머신보다 동적 서비스 관점에서 생각할 수 있습니다.

리눅스의 경우 수천개의 메트릭이 제공되비다. CPU 사용량 같은 메트릭은 문서화가 잘되있습니다. 또한 메모리 사용량 같은 메트릭은 커널 버전마다 구현이 달라지기 때문에 종류가 다양합니다. 그 밖에 문서화가 전혀 되어 있지 않아 커널 소스코드르 읽고 어떤 기능을 하는지 직접 파악해야 하는 메트릭도 있습니다.

노드 익스포터는 일반 사용자가 실행할 수 있게 설계되었으며, `sshd` 나 `cron` 같은 시스템 데몬을 실행하는 것과 동일한 방법으로 머신에서 직접 실행해야 합니다.

## CPU Collector

CPU 수집기의 주요 메트릭인 `node_cpu_seconds_total` 는 각 모드에서 CPU 마다 얼마나 많은 시간을 소비했는지 나타내는 카운터로서, 레이블은 `cpu` 와 `mode` 입니다.

```
# HELP node_cpu_seconds_total Seconds the cpus spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 48649.88
node_cpu_seconds_total{cpu="0",mode="iowait"} 169.99
node_cpu_seconds_total{cpu="0",mode="irq"} 0
node_cpu_seconds_total{cpu="0",mode="nice"} 57.5
node_cpu_seconds_total{cpu="0",mode="softirq"} 8.05
node_cpu_seconds_total{cpu="0",mode="steal"} 0
node_cpu_seconds_total{cpu="0",mode="system"} 1058.32
node_cpu_seconds_total{cpu="0",mode="user"} 4234.94
node_cpu_seconds_total{cpu="1",mode="idle"} 9413.55
node_cpu_seconds_total{cpu="1",mode="iowait"} 57.41
node_cpu_seconds_total{cpu="1",mode="irq"} 0
node_cpu_seconds_total{cpu="1",mode="nice"} 46.55
node_cpu_seconds_total{cpu="1",mode="softirq"} 7.58
node_cpu_seconds_total{cpu="1",mode="steal"} 0
node_cpu_seconds_total{cpu="1",mode="system"} 1034.82
node_cpu_seconds_total{cpu="1",mode="user"} 4285.06
```

이 코드에 나오는 `idle`, `iowait`, `irq`, `nice` 같은 모드는 각 CPU 에 대해 집계를 1 초당 1 초씩 증가합니다. 이를 통해 PromQL 표현식을 사용해 모든 CPU 에서의 유효 시간 비율을 계산할 수 있습니다.

`avg without(cpu, mode)(rate(node_cpu_seconds_total{mod="idle"}[1m]))`

이 표현식은 CPU 마다 초당 유휴 시간을 계산한 다음 머신에서 모든 CPU 의 평균을 계산합니다. 하나의 머신에 대해 각 모드에서 사용한 시간 비율에 대한 계산을 다음 식과 같이 일반화할 수 있습니다.

`avg without(cpu)(rate(node_cpu_seconds_total[1m]))`

게스트 사용자에 의한 CPU 사용량은 이미 `user` 와 `nice` 모드에 포함되어 있습니다. `node_cpu_guest_seconds_total` 메트릭에서 별도로 게스트 사용자가 소비한 시간을 확인할 수 있습니다.

## Filesystem Collector

파일 시스템 수집기는 `df` 명령어에서 얻을 수 있는 것철머 마운트된 파일 시스템의 메트릭을 수집한다. `--collector.filesystem.ignored-mount-points` 와 `--collector.filesystem.ignored-fs-types` 플래그는 포함되는 파일 시스템을 제한할 수 있습니다. **루트(Root)** 사용자로 노드 익스포터를 실행시키지 않기 때문에, 마운트 지점에서 `statfs` 시스템 호출을 사용할 수 있는 파일의 접근 권한을 가지고 있는지 확인해야 합니다.

이 수집기의 모든 메트릭에는 `node_filesystem_` 접두어가 붙어 있으며, `device`, `fstyep`, `mountpoint` 레이블도 있습니다.

```
# HELP node_filesystem_size_bytes Filesystem size in bytes.
# TYPE node_filesystem_size_bytes gauge
node_filesystem_size_bytes{device="/dev/sda5",fstype="ext4",mountpoint="/"} 9e+10
```

파일 시스템 메트릭은 대부분 자명합니다. 단 `node_filesystem_avail_bytes` 와 `node_filesys`, `tem_free_bytes` 의 차이에 주의해야 합니다. 유닉스 파일시스템에서 일부 디스크공간은 루트 사용자를 위해 예약되어 있습니다. 따라서 루트 사용자는 다른 일반 사용자들이 가용 공간을 다 채워도 얼마든지 작업을 수행할 수 있습니다. `node_filesystem_avail_bytes` 는 일반 사용자들이 이용할 수 있는 공간이며, 사용된 디스크 공간을 계산하는 경우 다음과 같이 계산해야 합니다.

```
  node_filesystem_avail_bytes
/
  node_filesystem_size_bytes
```

`node_filesystem_files` 과 `node_filesystem_files_free` 는 전체 `inode` 개수와 이들 중 사용 가능한 `inode` 개수를 나타내며, 이를 통해 파일 시스템이 가지고 있는 대략적인 파일 개수를 알 수 있습니다. `df -i` 로도 내용을 확인할 수 있습니다.

## Diskstats Collector

`diskstats` 수집기는 `/proc/diskstats` 에서 얻은 디스크 I/O 메트릭을 게시합니다. 기본적으로 `--collector.diskstats.ignored-devices` 플래그는 파티션과 루프백 장치같이 실제 디스크가 아닌 경우는 제외합니다.

```
# HELP node_disk_io_now The number of I/Os currently in progress.
# TYPE node_disk_io_now gauge
node_disk_io_now{device="sda"} 0
```

모든 메트릭은 `device` 레이블을 가지고 있으며 대부분은 카운터로서 다음과 같스빈다.

* `node_disk_io_now`
  * 진행 중인 I/O 의 개수
* `node_disk_io_time_seconds_total`
  * I/O 가 진행 중일 때 증가됨
* `node_disk_read_bytes_total`
  * I/O 가 읽은 바이트 수
* `node_disk_read_time_seconds_total`
  * 읽기 I/O 에 걸린 시간
* `node_disk_reads_completed_total`
  * 완료 I/O 의 개수
* `node_disk_written_bytes_total`
  * I/O 에 쓴 바이트 수
* `node_disk_write_time_seconds_total`
  * 쓰기 I/O 에 걸린 시간
* `node_disk_writes_completed_total`
  * 완료 읽기 I/O 의 개수

디스크 I/O 사용률을 계산하려면 `iostat -x` 에 표시된 것처럼 `node_disk_to_time_seconds_total` 을 사용할 수 있습니다.

```
rate(node_disk_to_time_seconds_total[1m])
```

다음과 같이 읽기 I/O 평균 시간을 계산할 수 있습니다.

```
  rate(node_disk_read_time_seconds_total[1m])
/
  rate(node_disk_reads_completed_total[1m])
```

## Netdev Collector

`netdev` 수집기는 `node_network_` 접두어와 `device` 레이블을 사용해 네트워크 디바이스에 대한 메트릭을 게시합니다.

```
# HELP node_network_receive_bytes_total Network device statistic receive_bytes.
# TYPE node_network_receive_bytes_total counter
node_network_receive_bytes_total{device="lo"} 8.3213967e+07
node_network_receive_bytes_total{device="wlan0"} 7.0854462e+07
```

`node_network_receive_bytes_total` 과 `node_network_teansmit_bytes_total` 을 이용해 들어오고 나가는 네트워크 대역폭을 계산할 수 있습니다. 따라서 이 주요 메트릭에 관심을 기울어야 합니다.

```
rate(node_network_receive_bytes_total[1m])
```

`node_network_receive_packets_total` 과 `node_network_transmit_packets_total` 에도 주의를 기우렁야합니다. 이들은 각각 들어오고 나가는 패킷을 추적하는 메트릭입니다.

## Meminfo Collector

`meminfo` 수집기는 `node_memory_` 접두어를 가지는 모든 메모리 관련 표준 메트릭을 가지고 있습니다. 이 메트릭들은 모두 `/proc/meminfo` 에서 얻으며, 킬로바이트 단위의 결과를 바이트 단위로 변환합니다.

```
# HELP node_memory_MemTotal_bytes Memory information field MemTotal.
# TYPE node_memory_MemTotal_bytes gauge
node_memory_MemTotal_bytes 8.269582336e+09
```

`node_memory_MemTotal_bytes` 는 머신의 실제 메모리 총량을 뜻하며, 메트릭 이름에서 그 뜻이 분명하게 전달됩니다. 그러나 사용된 메모리에 대한 메트릭은 없다는 점에 주의해야합니다. 어떻게든 이에 대한 계산을 해야합니다. 따라서 다른 메트릭에서 사용되지 않은 메모리 양도 계산해야 합니다.

`node_memory_MemFree_bytes` 는 사용되지 않은 메모리의 총량이지만, 보유한 모든 메모리가 여유분이라는 사실이라는 의미는 아닙니다. 이론적으로 페이지 캐시(`node_memory_Cached_bytes`)는 쓰기 버퍼(`node_memory_Buffers_bytes`)처럼 다시 확보될 수 있지만, 일부 어플리케이션의 성능에 부정적인 영향을 줄 수 있습니다. 그리고 `slab` 과 페이지 테이블같이 메모리를 이용하는 다양한 커널 구조들도 있습니다.

`node_memory_MemAvailable` 는 커널에서 얼마나 많은 메모리를 실제로 사용할 수 있는지에 대한 표현식이지만, 메모리 소모를 감지하는 데 사용할 수 있습니다.

## Hwmon Collector

베어 메탈의 경우, `hwmon` 수집기는 온도, 팬 속도 등 `node_hwmon_` 접두어를 가지는 메트릭을 제공합니다. 이는 `sensors` 명령으로 얻을 수 있는 내용과 동일한 정보입니다.

```
# HELP node_hwmon_sensor_label Label for given chip and sensor
# TYPE node_hwmon_sensor_label gauge
node_hwmon_sensor_label{chip="platform_coretemp_0",
    label="core_0",sensor="temp2"} 1
node_hwmon_sensor_label{chip="platform_coretemp_0",
    label="core_1",sensor="temp3"} 1
# HELP node_hwmon_temp_celsius Hardware monitor for temperature (input)
# TYPE node_hwmon_temp_celsius gauge
node_hwmon_temp_celsius{chip="platform_coretemp_0",sensor="temp1"} 42
node_hwmon_temp_celsius{chip="platform_coretemp_0",sensor="temp2"} 42
node_hwmon_temp_celsius{chip="platform_coretemp_0",sensor="temp3"} 41
```

`node_hwmon_temp_celsius` 는 다양한 컴포넌트의 온도를 나타내며, `node_hwmon_sensor_label` 에 게시된 센서 레이블을 가질 수 있습니다.

일부 하드웨어는 어떤 센서인지 이해하려면 센서 레이블이 필요합니다. 이전 메트릭에서 `temp3` 는 CPU 코어 번호 1 을 나타냅니다.

`group_left` 를 이용해 `node_hwmon_sensor_label` 에서 `node_hwmon_temp_celsius` 까지 `label` 레이블을 연결할 수 있습니다.

```
  node_hwmon_temp_celsius
* ignoring(label) group_left(label)
  node_hwmon_sensor_label
```

## Stat Collector

`stat` 수집기는 `/proc/stat` 에서 메트릭을 제공하기 때문에 다양한 성격의 메트릭이 혼재되어있습니다.

`node_boot_time_seconds` 는 커널이 시작된 시간이며, 이 시작 시간부터 커널이 얼마나 오랫동안 가동했는지 계산할 수 있습니다.

```
time() - node_boot_time_seconds
```

`node_intr_total` 은 누적된 하드웨어 인터럽트 개수를 나타냅니다. 이것은 높은 카디널리티 때문에 기본적으로 비활성화되어 있는 인터럽트 수집기에서 사용되기 때문에 `node_interrupts_total` 이라 하지 않습니다.

그 밖의 메트릭들은 프로세스와 관련이 있습니다. `node_forks_total` 은 `fork` 시스템 콜의 개수에 대한 카운터이며, `node_context_switches_total` 은 컨텍스트 스위치의 횟수입니다. 반면 `node_procs_blocked` 와 `node_procs_running` 은 블록되거나 실행 중인 프로세스의 개수를 의미합니다.

## Uname Collector

`uname` 수집기는 단일 메트릭 `node_uname_info` 를 게시합니다.

```
# HELP node_uname_info Labeled system information as provided by the uname
    system call.
# TYPE node_uname_info gauge
node_uname_info{domainname="(none)",machine="x86_64",nodename="kozo",
    release="4.4.0-101-generic",sysname="Linux",
    version="#124-Ubuntu SMP Fri Nov 10 18:29:59 UTC 2017"} 1
```

`nodename` 레이블은 머신의 호스트 이름으로, `instance` 대상 레이블이나 DNS 처럼 가지고 있는 이름들과 다를 것입니다.

사용 가능한 커널 버전을 실행할 수 있는 머신의 개수를 계산하려면 다음 식을 사용합니다.

```
count by(release)(node_uname_info)
```

## Loadavg Collector

`loadavg` 수집기는 가각 1 분, 5 분, 15 분 부하 평균을 의미하는 `node_load1`, `node_load5`, `node_load15` 메트릭을 제공합니다.

이 메트릭의 의미는 플랫폼마다 다릅니다. 리눅스에서 실행 대기열에서 대기 중인 프로세스의 개수 뿐 아니라 I/O 를 기다리는 프로세스 같이 인터럽트 할 수 없는 프로세스도 의미합니다.

머신의 사용량이 더 많아졌다면 부하 평균은 간단한 솔루션으로 유용하지만, 이들은 **알림(Alert)** 를 위한 좋은 선택은 아닙니다.

## Textfile Collector

`textfile` 수집기는 앞서 설명한 수집기와는 성격이 다릅니다. 커널에서 메트릭을 얻어오지 않고, 사용자가 만든 파일에서 가져옵니다.

노드 익스포터는 루트 사용자로 실행되지 않습니다. 따라서 SMART 에 나온 메트릭은 `smartctl` 명령어를 실행하기 위해 루트 사용자 권한이 필요합니다.

루트 사용자 권한이 필요한 메트릭 외에, `iptables` 같은 명령어를 실행하면 일부 정보만 얻을 수 있습니다. 신뢰성을 위해 노드 익스포터는 프로세스들을 시작하지 않습니다.

`textfile` 수집기를 사용하려면 `smartctl` 이나 `iptables` 같은 명령어를 정기적으로 실행하는 **크론잡(cronjob)** 을 생성하고, 결과를 Prometheus 표현 형식으로 변환해야 합니다. 그리고 특정 디렉토리의 파일에 **원자적(Atomically)** 으로 기록해야 합니다. 데이터를 수집할 때마다 노드 익스포터는 해당 디렉토리의 파일을 읽고 그 결과에 메트릭을 포함할것입니다.

크론잡을 통해 자체 메트릭을 추가하거나, 머신에 대해 Chef 가 가지는 역할처럼 일부 `info` 메트릭을 제공하는 머신의 구성 관리 시스템이 작성한 파일에서 더 많은 정적 정보를 얻기 위해 `textfile` 수집기를 이용할 수 있습니다.

일반적으로 노드 익스포터처럼 `textfile` 수집기는 머신에 대한 메트릭을 대상으로 합니다. 예를 들어 노드 익스포터가 게시하지 않았다거나, 접근하는 데 루트 권한이 필요한 커널 메트릭이 있을 수 있습니다. 보류 중인 패키지 업데이트가 있거나 재부팅이 예정된 경우라면, 운여체제 수준의 더 많은 메트릭을 추적하고 싶을 수 있습니다. 

기술적으로는 운영체제 메트릭이라기보단 서비스지만, 머신에서 실행 중인 **카산드라(Cassandra)** 노드에 대한 백업과 같은 일괄처리 작업이 마지막으로 완료된 시점을 기록하는 것은 `textfile` 수집기의 좋은 활용 예가 될 수 있습니다. 머신에서 백업이 수행되고 나면 그에 대한 관심도 사라지기 때문입니다. 카산드라 노드와 머신은 동일한 수명주기를 가집니다.

### Using the Textfile Collector

`textfile` 수집기는 기본 설정에서 활성화되어 있지만, 노드 익스포터에서 동작시키려면 반드시 `--collector.textfile.directory` 명령행 플래그를 사용해야 하며, 혼돈을 피하려면 이 목적으로만 사용할 디렉토리를 지정해야 합니다.

아래 예제처럼 이 디렉토리를 사용하도록 구성된 노드 익스포터를 실행시킵니다. `textfile` 수집기는 *.prom* 확장자를 가지는 파일만 찾습니다.

```shell
hostname $ mkdir textfile
hostname $ echo example_metric 1 > textfile/example.prom
hostname $ ./node_exporter --collector.textfile.directory=$PWD/textfile
```

노드 익스포터의 `/metrics` 를 살펴보면 다음과 같은 메트릭을 볼 수 있습니다.

```
# HELP example_metric Metric read from /some/path/textfile/example.prom
# TYPE example_metric untyped
example_metric 1
```

일반적으로 *.prom* 파일은 크론잡과 함께 생성되고 업데이트됩니다. 데이터 수집은 언제든지 일어날 수 있기 때문에, 노드 익스포터가 부분적으로 작성된 파일을 참조하지 않도록 하는 것이 중요합니다. 이를 위해 동일한 디렉토리에 임시 파일을 먼저 작성해야 합니다. 그리고 완성된 파일을 최종 파일명으로 바꿉니다.

아래 예제는 `textfile` 수집기로 출력하는 크론잡을 보여줍니다. 아래 예제는 임시파일에 메트릭을 생성하고, 최종 파일명으로 이름을 변경합니다. 짧은 명령어를 사용하는 간단한 예제지만, 대부분의 실제 사용 예에서는 가독성을 유지하는 스크립트를 생성하길 원합니다.

```shell
TEXTFILE=/path/to/textfile/directory

# This must all be on one line
*/5 * * * * root (echo -n 'shadow_entries '; grep -c . /etc/shadow)
    > $TEXTFILE/shadow.prom.$$
    && mv $TEXTFILE/shadow.prom.$$ $TEXTFILE/shadow.prom
```

### Timestamps

**게시 형식(Exposition Format)** 은 **타임스탬프(Timestamp)** 를 지원하지만, `textfile` 수집기와 함께 사용할 수는 없습니다. 이는 의미론적으로 타당하지 않기 때문입니다. 메트릭이 데이터 수집에서 나온 다른 메트릭처럼 동일한 타임스탬프를 가지는 것으로 표시되지 않습니다.

그 대신, 파일의 `mtime` 을 `node_textfile_mtime_seconds` 에서 이용할 수 있습니다. 동작하지 않는 크론잡에 대한 알림을 보내는 데 이 기능을 사용할 수 있습니다. 이 값이 너무 오래된 경우에는 문제가 있음을 의미할 수 있습니다.

```
# HELP node_textfile_mtime_seconds Unixtime mtime of textfiles successfully read.
# TYPE node_textfile_mtime_seconds gauge
node_textfile_mtime_seconds{file="example.prom"} 1.516205651e+09
```
