---
title : IP 경로 추적 명령어 netstat 톺아보기
categories:
 - Linux
tags:
 - Linux
 - netstat
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

### `netstat` Overview

`netstat`(network statistics)는 전송 제어 프로토콜, 라우팅 테이블, 수많은 네트워크 인터페이스(네트워크 인터페이스 컨트롤러 또는 소프트웨어 정의 네트워크 인터페이스), 네트워크 프로토콜 통계를 위한 네트워크 연결을 보여주는 명령어입니다. 

간단한 사용 예시를 살펴보겠습니다.

```bash
$ netstat -antl
Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address                                 Foreign Address                               (state)
tcp4       0      0  172.20.20.87.60473                            103.102.166.240.443                           ESTABLISHED
tcp4       0      0  172.20.20.87.60472                            103.102.166.224.443                           ESTABLISHED
tcp4       0      0  172.20.20.87.60419                            213.239.192.222.443                           ESTABLISHED
tcp4       0      0  172.20.20.87.60414                            213.239.192.222.443                           ESTABLISHED

...

tcp6       0      0  *.7000                                        *.*                                           LISTEN
tcp4       0      0  *.7000                                        *.*                                           LISTEN
tcp4       0      0  172.20.20.87.60490                            52.78.231.108.443                             TIME_WAIT
tcp4       0      0  172.20.20.87.60492                            52.78.231.108.443                             TIME_WAIT
```

### `netstat` Documentaiton

`netstat` 명령어의 각 옵션 간단히 정리하겠습니다.

> SYNOPSIS

```bash
netstat [address_family_options] [--tcp|-t] [--udp|-u]
[--udplite|-U] [--sctp|-S] [--raw|-w] [--l2cap|-2] [--rfcomm|-f]
[--listening|-l] [--all|-a] [--numeric|-n] [--numeric-hosts]
[--numeric-ports] [--numeric-users] [--symbolic|-N]
[--extend|-e[--extend|-e]] [--timers|-o] [--program|-p]
[--verbose|-v] [--continuous|-c] [--wide|-W]

netstat {--route|-r} [address_family_options]
[--extend|-e[--extend|-e]] [--verbose|-v] [--numeric|-n]
[--numeric-hosts] [--numeric-ports] [--numeric-users]
[--continuous|-c]

netstat {--interfaces|-i} [--all|-a] [--extend|-e[--extend|-e]]
[--verbose|-v] [--program|-p] [--numeric|-n] [--numeric-hosts]
[--numeric-ports] [--numeric-users] [--continuous|-c]

netstat {--groups|-g} [--numeric|-n] [--numeric-hosts]
[--numeric-ports] [--numeric-users] [--continuous|-c]

netstat {--masquerade|-M} [--extend|-e] [--numeric|-n]
[--numeric-hosts] [--numeric-ports] [--numeric-users]
[--continuous|-c]

netstat {--statistics|-s} [--tcp|-t] [--udp|-u] [--udplite|-U]
[--sctp|-S] [--raw|-w]

netstat {--version|-V}

netstat {--help|-h}

address_family_options:

[-4|--inet] [-6|--inet6]
[--protocol={inet,inet6,unix,ipx,ax25,netrom,ddp,bluetooth, ... }
] [--unix|-x] [--inet|--ip|--tcpip] [--ax25] [--x25] [--rose]
[--ash] [--bluetooth] [--ipx] [--netrom] [--ddp|--appletalk]
[--econet|--ec]
```

> OPTIONS

* `--verbose`, `-v`
  * 사용자에게 자세한 내용을 설명합니다. 특히 구성되지 않은 주소 패밀리에 대한 유용한 정보를 인쇄합니다.
* `--wide`, `-W`
  * 필요한 만큼 넓은 출력을 사용하여 IP 주소를 자르지 마십시오.
  * 현재 이 옵션은 기존 스크립트를 중단하지 않는 옵션입니다.
* `--numeric`, `-n`
  * 기호 호스트, 포트 또는 사용자 이름을 확인하는 대신 숫자 주소를 표시합니다.
* `--numeric-hosts`
  * 숫자 호스트 주소를 표시하지만 포트 또는 사용자 이름 확인에는 영향을 주지 않습니다.
* `--numeric-ports`
  * 숫자 포트 번호를 표시하지만 호스트 또는 사용자 이름 확인에는 영향을 주지 않습니다.
* `--numeric-users`
  * 숫자 사용자 ID를 표시하지만 호스트 또는 포트 이름 확인에는 영향을 주지 않습니다.
* `--protocol=family`, `-A`
  * 연결을 표시할 주소 패밀리(낮은 수준 프로토콜로 더 잘 설명됨)를 지정합니다. `family`는 **inet**, **inet6**, **unix**, **ipx**, **ax25**, **netrom**, **econet**, **ddp**, **bluetooth** 와 같은 주소 패밀리 키워드의 쉼표(',')로 구분된 목록이다.
  * 이는 `--inet|-4`, `--inet6|-6`, `--unix|-x`, `--ipx`, `--ax25`, `--netrom`, `--ddp` 및 `--bluetooth` 옵션을 사용하는 것과 동일한 효과를 가집니다.
  * 주소 패밀리 인넷(Iv4)은 raw, udp, udplite, tcp 프로토콜 소켓을 포함한다.
  * 주소 패밀리 블루투스(Iv4)는 l2cap 및 rfcomm 프로토콜 소켓을 포함한다.
* `-c`, `--continuous`
  * 이렇게 하면 `netstat`가 매초마다 선택한 정보를 연속적으로 인쇄합니다.
* `-e`, `--extend`
  * 추가 정보를 표시합니다. 최대 세부 정보를 보려면 이 옵션을 두 번 사용하십시오.
* `-o`, `--timers`
  * 네트워킹 타이머와 관련된 정보를 포함합니다.
* `-p`, `--program`
  * 각 소켓이 속한 프로그램의 PID와 이름을 표시합니다. 소켓이 커널에 속하거나(예: 커널 서비스가 종료되었지만 소켓이 아직 닫히지 않은 경우) 하이픈이 표시됩니다.
* `-l`, `--listening`
  * 수신 소켓만 표시합니다. (기본적으로 생략됩니다.)
* `-a`, `--all`
  * 수신 소켓과 수신 소켓을 모두 표시합니다. `--interfaces` 옵션을 사용하여 업 상태가 아닌 인터페이스를 표시합니다.
* `-F`
  * FIB에서 라우팅 정보를 인쇄합니다(기본값).
* `-C`
  * 경로 캐시에서 라우팅 정보를 인쇄합니다.

> OUTPUT

#### Active Internet connections

* Proto
  * 소켓에서 사용하는 프로토콜(tcp, udp, udpl, raw)입니다.
* Recv-Q
  * Established: 이 소켓에 연결된 사용자 프로그램에서 복사하지 않은 바이트 수입니다. 듣기: 커널 2.6.18 이후 이 열에는 현재 synbacklog가 포함되어 있습니다.
* Send-Q
  * Established: 원격 호스트에서 승인되지 않은 바이트 수입니다. 듣기: 커널 2.6.18 이후 이 열에는 synbacklog의 최대 크기가 포함됩니다.
* Local Address
  * 소켓의 로컬 끝 주소 및 포트 번호. `--numeric(-n)` 옵션이 지정되지 않은 경우 소켓 주소는 표준 호스트 이름(FQDN)으로 확인되고 포트 번호는 해당 서비스 이름으로 변환됩니다
* Foreign Address
  * Address and port number of the remote end of the socket. Analogous to "Local Address".
* State
  * 소켓의 상태입니다. 원시 모드 상태도 없고 일반적으로 UDP 및 UDPLite에서 사용되는 상태도 없기 때문에 이 열은 비워둘 수 있습니다. 일반적으로 이 값은 여러 값 중 하나일 수 있습니다.
  * *ESTABLISHED*
    * 소켓에 연결이 설정되어 있습니다.
  * *SYN_SENT*
    * 소켓이 연결을 설정하려고 시도 중입니다.
  * *SYN_RECV* 
    * 네트워크로부터 연결 요청이 수신되었습니다.
  * *FIN_WAIT1*
    * 소켓이 닫혔고 연결이 종료되고 있습니다.
  * *FIN_WAIT2*
    * 연결이 닫혔고 소켓이 원격 엔드에서 종료 대기 중입니다.
  * *TIME_WAIT*
    * 소켓은 아직 네트워크에 있는 패킷을 처리하기 위해 닫은 후 대기 중입니다.
  * *CLOSE*
    * 소켓을 사용하지 않습니다.
  * *CLOSE_WAIT*
    * 원격 엔드가 종료되어 소켓이 닫히기를 기다립니다.
  * *LAST_ACK*
    * 원격 엔드가 종료되었고 소켓이 닫혔습니다. 확인을 기다리는 중입니다.
  * *LISTEN*
    * 소켓이 들어오는 연결을 수신 중입니다. `--listening(-l)` 또는 `--all(-a)` 옵션을 지정하지 않는 한 이러한 소켓은 출력에 포함되지 않습니다.
  * *CLOSING*
    * 두 소켓 모두 종료되었지만 아직 모든 데이터를 전송하지 못했습니다.
  * *UNKNOWN*
    * 소켓의 상태를 알 수 없습니다.
* User
  * 소켓 소유자의 사용자 이름 또는 UID(사용자 ID)입니다.
* PID/Program name
  * 소켓을 소유하는 프로세스의 프로세스 이름(PID)과 프로세스 이름의 슬래시로 구분된 쌍입니다. `--program`은 이 열을 포함합니다. 소유하지 않은 소켓에서 이 정보를 보려면 `superuser` 권한도 필요합니다. IPX 소켓에는 아직 이 식별 정보를 사용할 수 없습니다.
* Timer
  * 이 소켓과 연결된 TCP 타이머입니다. 형식은 `timer(a/b/c)`입니다. 타이머는 다음 값 중 하나입니다.
  * *off*
    * 이 소켓에는 타이머가 설정되어 있지 않습니다.
  * *on*
    * 소켓에 대해 재전송 타이머가 활성화됩니다.
  * *keepalive*
    * 킵얼라이브 타이머가 소켓에 대해 활성화됩니다.
  * *timewait*
    * 연결이 닫히고 소켓에 대한 대기 시간 타이머가 활성화됩니다.
  * *a*
    * 타이머 값
  * *b*
    * 보낸 재전송 횟수입니다.
  * *c*
    * 전송된 킵얼라이브 수입니다.

#### Active UNIX domain Sockets

* Proto
  * 소켓에서 사용하는 프로토콜(일반적으로 유닉스)입니다.
* RefCnt
  * 기준 카운트(즉, 이 소켓을 통해 연결된 프로세스).
* Flags
  * 표시되는 플래그는 `SO_ACCEPTON`(**ACC** 로 표시), `SO_WAITDATA`(**W**) 또는 `SO_NOSPACE`(**N**)입니다. `SO_ACCECPTON`은 해당 프로세스가 연결 요청을 기다리는 경우 연결되지 않은 소켓에서 사용됩니다. 다른 깃발들은 보통 관심사가 아니다.
* Type
  * 소켓 액세스에는 몇 가지 유형이 있습니다.
  * *SOCK_DGRAM*
    * 소켓은 데이터그램(무연결) 모드에서 사용됩니다.
  * *SOCK_STREAM*
    * 이것은 스트림(연결) 소켓입니다.
  * *SOCK_RAW*
    * 소켓은 원시 소켓으로 사용됩니다.
  * *SOCK_RDM*
    * 이것은 신뢰할 수 있는 전달된 메시지를 제공합니다.
  * *SOCK_SEQPACKET*
    * 이것은 순차적 패킷 소켓입니다.
  * *SOCK_PACKET*
    * 원시 인터페이스 액세스 소켓.
  * *UNKNOWN*
    * Who ever knows what the future will bring us - just fill in here :-)
* State
  * 이 필드에는 다음 키워드 중 하나가 포함됩니다.
  * *FREE*
    * 소켓이 할당되지 않았습니다.
  * *LISTENING*
    * 소켓이 연결 요청을 수신하고 있습니다. 이러한 소켓은 `--listening(-l)` 또는 `--all(-a)` 옵션을 지정한 경우에만 출력에 포함됩니다.
  * *CONNECTING*
    * 소켓이 연결을 설정하려고 합니다.
  * *CONNECTED*
    * 소켓이 연결되어 있습니다.
  * *DISCONNECTING*
    * 소켓이 분리되고 있습니다.
  * *(empty)*
    * 소켓이 다른 소켓에 연결되어 있지 않습니다.
  * *UNKNOWN*
    * 이 상태는 절대 일어나서는 안 된다.
* PID/Program name
  * 소켓이 열려 있는 프로세스의 프로세스 ID(PID) 및 프로세스 이름입니다. 자세한 내용은 위에 쓰여진 활성 인터넷 연결 섹션에서 확인할 수 있습니다.
* Path
  * 해당 프로세스가 소켓에 연결된 경로 이름입니다.
* Active IPX sockets
  * (이 작업은 아는 사람이 수행해야 합니다.)
* Active NET/ROM sockets
  * (이 작업은 아는 사람이 수행해야 합니다.)
* Active AX.25 sockets
  * (이 작업은 아는 사람이 수행해야 합니다.)

> 참고자료

* [Wikipedia - netstat](https://en.wikipedia.org/wiki/Netstat)
* [netstat(8) — Linux manual page](https://man7.org/linux/man-pages/man8/netstat.8.html)