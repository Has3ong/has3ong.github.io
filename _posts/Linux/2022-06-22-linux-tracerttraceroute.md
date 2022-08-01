---
title : IP 경로 추적 명령어 tracert / traceroute 톺아보기
categories:
 - Linux
tags:
 - Linux
 - tracert
 - traceroute
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

### `traceroute` Overview

`tracert` 및 `traceroute`는 지정된 호스트에 도달할 때까지 통과하는 경로의 정보와 각 경로에서의 지연 시간을 추적하는 명령어입니다. 보통 네트워크 라우팅의 문제점을 찾아내는 목적으로 많이 사용됩니다.

그렇다면 두 명령어의 차이는 무엇일까? 단순하게 생각하면 OS차이라고 볼 수 있습니다. 하지만 Linux에서도 `tracert`를 사용하기 때문에 근본적인 차이가 있습니다. 바로 ICMP를 사용하느냐 UDP를 사용하느냐의 차이라고 할 수 있습니다.

`traceroute`는 UDP 패킷을 보내고 `tracert`는 ICMP 패킷을 보냅니다.

그리고 IPv6를 이용하는 `traceroute6`와 `tracert6` 도 존재합니다.

이번 포스트에서는 `traceroute`에 대해서 알아보겠습니다. 먼저 명령어가 동작하는 방식을 확인해보겠습니다.

```bash
$ traceroute www.naver.com
traceroute: Warning: www.naver.com has multiple addresses; using 223.130.195.95
traceroute to www.naver.com.nheos.com (223.130.195.95), 64 hops max, 72 byte packets
 1  172.20.20.1 (172.20.20.1)  4.402 ms  3.501 ms  4.890 ms
 2  203.251.144.209 (203.251.144.209)  47.535 ms  7.664 ms  6.639 ms
 3  10.10.10.1 (10.10.10.1)  8.069 ms  8.906 ms  8.168 ms
 4  * * *
 5  * * *
 6  * * *
 7  112.174.75.114 (112.174.75.114)  5.723 ms  7.719 ms  5.861 ms
 8  * * *
 9  * * *
```

`traceroute`는 우연히 도달하는 것을 방지하기 위해 정확히 3개의 UDP 패킷을 전송합니다.

또한, `* * *` 로 표시되는 부분은 침입차단시스템 등의 접근통제리스트에 의해 `traceroute`의 UDP 패킷이 차단되었음을 확인할 수 있습니다.

### `traceroute` Documentaiton

`traceroute` 명령어의 각 옵션 간단히 정리하겠습니다.

> SYNOPSIS

```
traceroute [-46dFITUnreAV] [-f first_ttl] [-g gate,...]
        [-i device] [-m max_ttl] [-p port] [-s src_addr]
        [-q nqueries] [-N squeries] [-t tos]
        [-l flow_label] [-w waittimes] [-z sendwait] [-UL] [-D]
        [-P proto] [--sport=port] [-M method] [-O mod_options]
        [--mtu] [--back]
        host [packet_len]
traceroute6  [options]
```

> OPTIONS

* `--help`
  * 도움말 정보를 인쇄하고 종료합니다.
* `-4`, `-6`
  * 명시적으로 IPv4 또는 IPv6 추적 라우팅을 강제 실행합니다. 기본적으로 프로그램은 지정된 이름을 확인하고 적절한 프로토콜을 자동으로 선택합니다. 호스트 이름 확인이 IPv4 및 IPv6 주소를 모두 반환하는 경우 traceroute는 IPv4를 사용합니다.
* `-I`, `--icmp`
  * ICMP ECHO 사용
* `-T`, `--tcp`
  * TCP SYN 사용
* `-d`, `--debug`
  * 소켓 수준 디버깅 활성화(Linux 커널이 지원하는 경우)
* `-F`, `--dont-fragment`
  * 프로브 패킷을 조각화하지 마십시오. (IPv4의 경우 중간 라우터에 원격으로 조각화하지 않도록 지시하는 DF 비트도 설정합니다.
  * `packet_len` 명령줄 매개 변수에 따라 프로브 패킷 크기를 변경하면 개별 네트워크 홉의 MTU에 대한 정보를 수동으로 얻을 수 있습니다. `--mtu` 옵션(아래 참조)은 이 작업을 자동으로 시도합니다.
  * Linux 커널 2.6.22에서만 조각화되지 않은 기능(`-F` 또는 `--mtu`와 같은)이 제대로 작동합니다. 이 버전 이전에는 IPv6가 항상 단편화되어 있었지만 IPv4는 루트 캐시에서 발견된 최종 MTU만 사용할 수 있었으며 이는 장치의 실제 MTU보다 작을 수 있습니다.
* `-f first_ttl`, `--first=first_ttl`
  * 시작할 TTL을 지정합니다. 기본값은 1입니다.
* `-g gateway`, `--gateway=gateway`
  * 지정된 게이트웨이를 통해 패킷을 라우트하도록 네트워크에 지시하는 IP 소스 라우팅 옵션을 송신 패킷에 추가하도록 추적 라우트에 지시합니다(대부분의 라우터가 보안상의 이유로 소스 라우팅을 사용하지 않도록 설정됨). 일반적으로 여러 개의 게이트웨이가 허용됩니다(쉼표로 구분). IPv6의 경우 num, addr, addr의 형식... 여기서 num은 경로 헤더 유형(기본값은 유형 2)입니다. 이제 유형 0 루트 헤더는 더 이상 사용되지 않습니다(rfc5095).
* `-i interface`, `--interface=interface`
  * `traceroute`가 패킷을 전송해야 하는 인터페이스를 지정합니다. 기본적으로 인터페이스는 라우팅 테이블에 따라 선택됩니다.
* `-m max_ttl`, `--max-hops=max_ttl`
  * `traceroute`가 탐색할 최대 홉 수(최대 생존 시간 값)를 지정합니다. 기본값은 30입니다.
* `-N suqeris`, `--sim-queries=squeries`
  * 동시에 전송되는 시도 패킷 수를 지정합니다. 여러 개의 프로브를 동시에 전송하면 `traceroute`의 속도가 상당히 빨라질 수 있습니다. 기본값은 16입니다. 일부 라우터 및 호스트는 ICMP 속도 조절을 사용할 수 있습니다. 이러한 경우 너무 큰 숫자를 지정하면 일부 응답이 손실될 수 있습니다.
* `-n`
  * IP 주소를 표시할 때 IP 주소를 호스트 이름에 매핑하지 마십시오.
* `-p port`, `--port=port`
  * UDP 추적의 경우 사용할 대상 포트 베이스 `traceroute`를 지정합니다(대상 포트 번호는 각 시도별로 증가합니다).
  * ICMP 추적의 경우 초기 ICMP 시퀀스 값(각 시도마다 증가)을 지정합니다.
  * TCP 등의 경우 연결할 대상 포트만 지정합니다.
* `-t tos`, `--tos=tos`
  * IPv4의 경우 TOS(Type of Service) 및 우선 순위 값을 설정합니다. 유용한 값은 16(낮은 지연) 및 8(높은 처리량)입니다. 일부 TOS 우선 순위 값을 사용하려면 슈퍼 사용자여야 합니다.
  * IPv6의 경우 트래픽 제어 값을 설정합니다.
* `-l flow_label`, `--flowlabel=flow_label`
  * IPv6 패킷에 대해 지정된 `flow_label`을 사용합니다.
* `-w max[,here, near]`, `--wait=max[,here,near]`
  * 시도에 대한 응답을 기다리는 시간을 결정합니다.
  * 세 개의 부동 소수점 값이 쉼표(또는 슬래시)로 구분되어 있습니다. `Max`는 어떤 경우에도 대기할 최대 시간(초 단위, 기본 5.0)을 지정합니다.
  * 기존의 추적 경로 구현은 항상 모든 탐침을 `max`초간 기다렸다. 그러나 이미 같은 홉에서 또는 심지어 다음 홉에서 일부 응답이 있는 경우, 해당 응답의 왕복 시간을 힌트로 사용하여 실제 적절한 대기 시간을 결정할 수 있습니다.
  * 옵션인 `here`(기본값 3.0)는 동일한 홉에서 이미 수신한 응답의 왕복 시간을 곱하는 요인을 지정합니다. 결과 값은 (그러나 그 이하) `max` 대신 프로브의 타임아웃으로 사용됩니다. 옵션인 `near`(기본값 10.0)는 일부 넥스트 홉의 응답과 유사한 요인을 지정합니다. (두 경우 모두 처음 발견된 결과의 시간이 사용됩니다.)
  * 먼저, 동일한 홉(지금부터 먼저 인쇄될 프로브)을 찾습니다. 아무것도 발견되지 않으면 다음 홉을 찾습니다. 아무것도 발견되지 않으면 `max`를 사용합니다. `here` 및/또는 `near` 값이 0이면 해당 계산을 건너뜁니다. `here`와 `near`는 (이전 버전과의 호환성을 위해) `max`만 지정한 경우 항상 0으로 설정됩니다.
* `-q nqueries`, `--queries=nqueries`
  * 홉당 프로브 패킷 수를 설정합니다. 기본값은 3입니다.
* `-r`
  * 일반 라우팅 테이블을 무시하고 연결된 네트워크의 호스트로 직접 전송합니다. 호스트가 직접 연결된 네트워크에 있지 않으면 오류가 반환됩니다. 이 옵션은 라우트가 없는 인터페이스를 통해 로컬 호스트를 `ping`하는 데 사용할 수 있습니다.
* `-s source_addr`, `--source=source_addr`
  * 대체 원본 주소를 선택합니다. 인터페이스 중 하나의 주소를 선택해야 합니다. 기본적으로 송신 인터페이스의 주소가 사용됩니다.
* `-z sendwait`, `--sendwait=sendwait`
  * 시도 사이의 최소 시간 간격(기본값 0)입니다. 값이 10보다 크면 밀리초 단위의 숫자를 지정하고, 그렇지 않으면 초 단위입니다(부동점 값도 허용됨). 일부 라우터가 ICMP 메시지에 속도 제한을 사용할 때 유용합니다.
* `-e`, `--extensions`
  * ICMP 확장자를 표시합니다(rfc4884). 일반적인 형식은 `CLASS/TYPE`이며 그 다음이 16진수 덤프입니다. MPLS(rfc4950)는 다음과 같은 형식으로 구문 분석되어 표시됩니다. `L=label`,`E=exp_use`,`S=stack_bottom`,`T=TTL`( /로 구분된 더 많은 개체).
* `-A`, `--as-path-lookups`
  * 라우팅 레지스트리에서 AS 경로 검색을 수행하고 해당 주소 뒤에 직접 결과를 인쇄합니다.
* `-V`, `--version`
  * 버전을 인쇄하고 종료합니다.

아래는 고급 사용을 위한 추가 옵션(예: 대체 추적 방법 등)이 있습니다.

* `--sport=port`
  * 사용할 소스 포트를 선택합니다. `-N 1 -w 5`를 의미합니다. 일반적으로 소스 포트(해당되는 경우)는 시스템에서 선택합니다.
* `--fwmark=mark`
  * 송신 패킷에 대한 방화벽 표시를 설정합니다(리눅스 커널 2.6.25 이후).
* `-M method`, `--module=name`
  * 추적 경로 작업에 지정된 방법을 사용합니다. 기본 기존 udp 메서드의 이름은 `default`이고, icmp(`-I`)와 tcp(`-T`)는 각각 `icmp`와 `tcp`입니다.
  * 메서드별 옵션은 `-O`로 전달할 수 있습니다. 대부분의 메서드에는 간단한 바로 가기(`-I`는 `-M icmp` 등)가 있습니다.
* `-O option`, `--options=options`
  * 일부 메서드별 옵션을 지정합니다. 여러 옵션은 쉼표로 구분됩니다(또는 cmdline에서 여러 `-O`를 사용합니다). 각 방법에는 고유한 옵션이 있을 수 있으며, 그렇지 않은 경우도 많습니다.
  * 사용 가능한 옵션에 대한 정보를 인쇄하려면 `-O` 도움말을 사용하십시오.
* `-U`, `--udp`
  * 추적 라우팅에 대해 특정 대상 포트에 UDP를 사용합니다(각 시도당 포트를 늘리는 대신). 기본 포트는 53(dns)입니다.
* `-UL`
  * 추적 라우팅에 UDPLITE를 사용합니다(기본 포트는 53).
* `-D`, `--dccp`
  * 프로브에 DCCP 요청을 사용합니다.
* `-P protocol`, `--protocol=protocol`
  * 추적 라우팅에 지정된 프로토콜의 원시 패킷을 사용합니다. 기본 프로토콜은 253(rfc3692)입니다.
* `--mtu`
  * 추적 중인 경로를 따라 MTU를 검색합니다. `-F -N 1`을 의미합니다. 새로운 `mtu`는 그러한 `mtu`에 도달하기 위해 필요한 홉의 첫 번째 프로브에서 `F=NUM`의 형태로 한 번 인쇄됩니다. (실제로 해당 "필요한" icmp 메시지는 일반적으로 이전 홉에서 전송됩니다.)
  * 일부 라우터는 단편화에 대한 정보를 확인한 후 캐시할 수 있습니다. 따라서 더 가까운 홉에서 최종 mtu를 수신할 수 있습니다. 특이한 `tos`를 `-t`로 지정해 보십시오. 이렇게 하면 한 번의 시도에 도움이 될 수 있습니다(이렇게 하면 그곳에서도 캐시할 수 있습니다). 자세한 내용은 `-F` 옵션을 참조하십시오.
* `--back`
  * 전진 방향과 다르게 보일 때 후진 홉의 수를 인쇄합니다. 이 숫자는 원격 홉이 `initial ttl`이 64 또는 128 또는 255로 설정된 응답 패킷을 보낸다고 가정할 때 추측됩니다. 이 값은 `-NUM` 형식으로 음수 값으로 출력됩니다.

> 참고자료

* [Wikipedia - traceroute](https://en.wikipedia.org/wiki/Traceroute)
* [traceroute(8) — Linux manual page](https://man7.org/linux/man-pages/man8/traceroute.8.html)
* [traceroute6(8) - Linux man page](https://linux.die.net/man/8/traceroute6)