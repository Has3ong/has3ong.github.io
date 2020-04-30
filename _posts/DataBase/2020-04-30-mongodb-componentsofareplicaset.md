---
title : MongoDB Components of a Replica Set
tags :
- Election
- Primary
- Replica Set
- MongoDB
- Database
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Syncing

복제는 여러 서버에 걸쳐 동일한 데이터 복사본을 유지하는 것과 관련이 있습니다. MongoDB 는 프라이머리가 수행한 모든 쓰기를 포함하는 `oplog` 를 보관하여 복제를 수행합니다. 이는 프라이머리의 로컬 데이터베이스에 있는 **제한 컬렉션(Capped Collection)** 이고, 세컨더리는 이 컬렉션에 복제를 위한 연산을 쿼리합니다.

각 세컨더리는 프라이머리로부터 복제한 각 작업을 기록하고 있는 자신의 `oplog` 를 보관합니다. `Example 1` 처럼 어떤 멤버든지 다른 멤버에 대해 동기화 소스로 사용되는 것을 허용합니다. 세컨더리는 동기화하고 있는 멤버로부터 연산을 가져와 그 연산을 데이터 셋에 적용한 뒤 해당 연산을 `oplog` 에 쓰게됩니다. 만약 연산 적용에 실패한다면 세컨더리는 종료됩니다.

> Example 1 - Oplog keep an ordered list of write operations that have occurred. Each member has its own copy of the oplog, which should be identical to the primary’s (modulo some lag).

![image](https://user-images.githubusercontent.com/44635266/79978026-32e7a400-84da-11ea-81b3-94d912b9b837.png)

만약 세컨더리가 다운된다면 세컨더리가 재시작할 때 `oplog` 의 마지막 연산으로부터 동기화됩니다. 연산이 데이터에 적용되고 `oplog` 에 써지면 세컨더리는 이미 데이터에 적용된 연산을 재생할 수 있습니다. `oplog` 연산을 여러 번 재생해도 한 번 재생한 것과 같은 결과를 얻을 수 있습니다.

`oplog` 는 고정된 크기여서 특정 개수의 연산만을 담을 수 있습니다. 일반적으로 `oplog` 는 쓰기 연산이 시스템에 적용되는 것과 동일한 비율로 공간을 사용합니다. 만약 프라이머리에서 쓰기 연산이 분당 1 KB 가 발생한다면, `oplog` 는 분당 1 KB 씩 채워질것입니다.

하지만 몇 가지 예외가 있습니다. 삭제 및 다중갱신과 같이 여러 문서에 영향을 미치는 연산은 여러 개의 `oplog` 목록으로 분해됩니다. 프라이머리에서 하나의 연산은 영향을 받는 문서마다 하나의 `oplog` 연산으로 분할됩니다. 따라서 `db.col.remove()` 로 컬렉션에 존재하는 1,000,000 개의 문서를 삭제하려면 한 번에 문서 하나만 삭제하지만 `oplog` 는 1,000,000 개가 됩니다. 대량 작업을 수행하는 경우 예상보다 더 빠르게 `oplog` 가 채워집니다.

### Initial Sync

복제 셋의 멤버가 시작할 때, 그 멤버가 다른 멤버로부터 동기화를 시작하기에 유효한 상태인지 확인합니다. 유효하지 않다면 복제 셋의 다른 멤버로부터 데이터의 전체 복제본을 생성합니다. 이를 **초기 동기화(Initial Syncing)** 라 하는데 해당 프로세스를 위해 여러 단계를 진행하게 되며, `mongod` 로그에서 확인할 수 있습니다.

1. 먼저 멤버는 예비 장부정리를 합니다. 동기화를 진행할 멤버를 선택한 뒤 *local.me* 에 자기 식별자를 생성하고, 기존의 모든 데이터베이스를 삭제하여 깨끗한 상태로 시작할 수 있게 합니다.

```shell
Mon Jan 30 11:09:18 [rsSync] replSet initial sync pending
Mon Jan 30 11:09:18 [rsSync] replSet syncing to: server-1:27017
Mon Jan 30 11:09:18 [rsSync] build index local.me { _id: 1 }
Mon Jan 30 11:09:18 [rsSync] build index done 0 records 0 secs
Mon Jan 30 11:09:18 [rsSync] replSet initial sync drop all databases
Mon Jan 30 11:09:18 [rsSync] dropAllDatabasesExceptLocal 1
```

기존의 모든 데이터는 이 시점에 삭제가 됩니다. `mongod` 의 첫 번째 작업이 전체 삭제이기 대문에 데이터 디렉토리에 존재하는 데이터를 원하지 않거나 다른 곳으로 옮기는 경우에만 초기 동괴하를 수행해야 합니다.

2. 복제는 동기화 소스로부터 발생한 모든 레코드의 초기 데이터 복제본입니다. 이는 보통 프로세스 중에서 시간을 가장 많이 사용합니다.

```shell
Mon Jan 30 11:09:18 [rsSync] replSet initial sync clone all databases
Mon Jan 30 11:09:18 [rsSync] replSet initial sync cloning db: db1
Mon Jan 30 11:09:18 [FileAllocator] allocating new datafile /data/db/db1.ns, 
    filling with zeroes...
```

3. 그 다음 복제하는 동안에 발생한 모든 연산에 적용하는 첫 번째 `oplog` 적용이 발생합니다. 그러모르 **복제자(Cloner)** 에 의해 이동되거나 놓친 몇몇 문서에 대해 재복제를 수행해야 할 수도 있습니다.

```shell
Mon Jan 30 15:38:36 [rsSync] oplog sync 1 of 3
Mon Jan 30 15:38:36 [rsBackgroundSync] replSet syncing to: server-1:27017
Mon Jan 30 15:38:37 [rsSyncNotifier] replset setting oplog notifier to 
    server-1:27017
Mon Jan 30 15:38:37 [repl writer worker 2] replication update of non-mod
    failed: 
    { ts: Timestamp 1352215827000|17, h: -5618036261007523082, v: 2, op: "u", 
      ns: "db1.someColl", o2: { _id: ObjectId('50992a2a7852201e750012b7') }, 
      o: { $set: { count.0: 2, count.1: 0 } } }
Mon Jan 30 15:38:37 [repl writer worker 2] replication info 
    adding missing object
Mon Jan 30 15:38:37 [repl writer worker 2] replication missing object
    not found on source. presumably deleted later in oplog
```

위 로그는 일부 문서가 재복제될 수 밖에 없었던 경우의 모습입니다. 동기화 소스에서 발생하고 있는 트래픽 수준과 연산의 종류에 따라 개체를 누락할 수도 있고 그렇지 않을 수도 있습니다.

4. 그 다음 첫 번째 `oplog` 를 적용하는 동안에 발생한 연산에 적용하는 두 번째 `oplog` 적용이 발생합니다.

```shell
Mon Jan 30 15:39:41 [rsSync] oplog sync 2 of 3
```

두 번째 `olog` 적용은 일반적으로 요란하지 않게 전달하고 더 이상 재복제되는 것이 없어야 한다는 점에서 첫 번째 적용과는 다릅니다.

5. 이 시점에서 데이터는 세컨더리가 인덱스 구축을 시작할 수 있도록 프라이머리의 어느 시점에 존재하는 데이터 셋과 정확히 일치해야 합니다. 만약 대량의 컬렉션이나 인덱스를 가지고 있다면 이 작업은 꽤 시간이 걸립니다.

```shell
Mon Jan 30 15:39:43 [rsSync] replSet initial sync building indexes
Mon Jan 30 15:39:43 [rsSync] replSet initial sync cloning indexes for : db1
Mon Jan 30 15:39:43 [rsSync] build index db.allObjects { someColl: 1 }
Mon Jan 30 15:39:44 [rsSync] build index done.  scanned 209844 total records. 
    1.96 secs
```

6. 그 다음 마지막 `oplog` 적용이 발생하는데, 이 마지막 단계는 단지 멤버가 동기화 소스에 꽤 뒤처져 있는 동안 세컨더리가 되는 것을 방지하기 위한 것입니다. 이는 인덱스가 생성되는 동안 발생한 모든 연산에 적용됩니다.

```shell
Tue Nov  6 16:05:59 [rsSync] oplog sync 3 of 3
```

7. 이 시점에서 해당 멤버는 초기 동기화 과정을 완료하고 해당 멤버가 세컨더리가 되는 것을 허용하는 일반 동기화 단계로 전환됩니다.

```shell
Mon Jan 30 16:07:52 [rsSync] replSet initial sync done
Mon Jan 30 16:07:52 [rsSync] replSet syncing to: server-1:27017
Mon Jan 30 16:07:52 [rsSync] replSet SECONDARY
```

초기 동기화 과정을 추적하는 가장 좋은 방법은 서버 로그를 보는것입니다.

초기 동기화는 운영자 관점에서는 쉬운 일입니다. 데이터 디렉토리를 깔끔하게 유지한 상태에서 `mongod` 를 시작하면 됩니다. 때때로 백업으로부터 복원하는 방식은 `mongod` 를 통해 데이터를 복사하는 방식보다 빠릅니다.

복제는 동기화 소스의 작업 셋을 망칠 수 있습니다. 대부분의 배포는 결국 자주 접근하고 항상 메모리에 존재하는 데이터들의 집합입니다. 초기 동기화를 수행하는 것으로 해당 멤버가 자주 사용되는 데이터를 추출하여 메모리로 페이징하도록 합니다. 이는 램에 있는 데이터에 의해 처리되는 요청들이 갑자기 디스크로 향하도록 하여 멤버가 급격하게 느려집니다. 하지만 초기 동기화는 약간의 여유 공간이 있는 작은 데이터 셋과 서버에 좋은 쉬운 옵션입니다.

초기 동기화와 관련하여 일반적인 문제 중 하나는 2 단계(복제) 와 5 단계(인덱스 구축) 에서 시간이 오래 걸리는것입니다. 이 경우 새로운 멤버는 동기화 소스의 `oplog` 끝으로 밀려날 수 있는데, 동기화 소스의 `oplog` 는 새로운 멤버가 복제를 계속할 필요가 있는 데이터를 덮어쓰기 때문에 새로운 멤버는 더 이상 따라잡을 수 없을 정도로 동기화 소스보다 뒤처져 버립니다.

만약 멤버가 동기화 소스의 `oplog` 보다 뒤쳐지면 초기 동기화를 진행할 수 없습니다.

### Handling Staleness

만약 세컨더리가 동기화 소스 상에서 수행된 실제 연산들보다 훨씬 뒤떨어져 있다면 세컨더리는 곧 실효상태가 됩니다. 동기화 소스의 모든 연산이 실효 세컨더리보다 훨씬 앞서 있기 때문에 실효 세컨더리가 소스의 모든 연산을 따라 잡는것이 불가능합니다. 만약 동기화가 계속되는 경우 이 작업을 건너뜁니다. 이는 슬레이브가 다운타임이거나, 쓰기 요청이 처리량을 뛰어남거나, 읽기 작업이 매우 바쁠때 발생합니다.

세컨더리가 실효 상태가 되면 독자적으로 이행할 수 있는 긴 `oplog` 를 가진 멤버가 있는지 보기 위해 차례로 복제 셋의 각 멤버로부터 복제를 시도합니다. 만약 충분히 긴 `oplog` 를 가진 멤버를 발견하지 못하면 그 멤버에서의 복제는 중지되고 완전히 재동기화되어야 합니다.

세컨더리가 동기화되지 못하는 상황을 피하려면 프라이머리가 많은 양의 연산 이력을 보관할 수 있도록 큰 `oplog` 를 가져야 합니다. 그러면 많은 디스크 공간을 사용하게 되지만, 충분히 감수할 수 있습니다.

## Heartbeats

누가 프라이머리고, 동기화를 어디로부터 하는지, 누가 다운되었는지 같은 멤버 상태 정보를 멤버들이 알아야 합니다. 복제 셋에 대해 최신의 관점을 유지하기 위해 멤버는 **하트비트(Heartbeat)** 요청을 복제 셋의 모든 다른 멤버로 2 초마다 보냅니다. 하트비트 요청은 모두의 상태를 점검하기 위한 짧은 메세지 입니다.

하트비트의 가장 중요한 기능은 프라이머리가 복제 셋의 과반수에 도달할 수 있는지 여부를 알 수 있도록 해주는 것입니다. 만약 프라이머리가 더 이상 서버의 과반수에 도달할 수 없다면 그 프라이머리는 스스로르 강등시켜 세컨더리가 됩니다.

### Member States

멤버들은 하트비트를 통해 그들이 어떤 상태인지 통신할 수 있습니다. 두 가지 상태, 즉 프라이머리와 세컨더리에 대해 살펴봤습니다. 멤버들이 가질 수 있는 다른 일반적인 상태는 다음과 같습니다.

* STARTUP
  * 멤버를 처음 시작할 때의 상태로 MongoDB 가 멤버의 복제 셋 구성 정보를 로드할 때 이 상태가 됩니다. 구성 정보가 로드되면 상태가 STARTUP2 로 전환됩니다.
* STARTUP2
  * 이 상태는 초기 동기화 과정 전반에 걸쳐 지속되지만 일반 멤버에서는 몇 초 동안만 지속됩니다. 이는 복제와 선출을 다루기 위해 몇몇 스레드로 분리되고 다음 상태인 RECOVERING 으로 변환됩니다.
* RECOVERING
  * 멤버가 현재 올바르게 작동하고 있지만, 읽기 작업을 수행할 수 없음을 의미합니다. 이 상태는 과부화된 상태로 다양한 상황에서 나타납니다.
  * 시작 시 멤버는 읽기 요청을 받아들이기 전에 유효한 상태인지 확인할 수 있는 여러 검사를 수행해야 합니다. 그러므로 모든 멤버는 시작 시 세컨더리가 되기 전에 짧게 RECOVERING 상태를 거칩니다. 멤버는 조각 모음 같은 긴 연산이 진행되거나 `replSetMaintenance` 명령에 대한 응답으로 RECOVERING 상태가 될 수 있습니다.
  * 멤버는 다른 멤버들보다 많이 뒤처져 있을 때 이를 따라잡기 위해 RECOVERING 상태가 될 수 있습니다. 이는 일반적으로 멤버 재동기화가 요구되는 장애 상태입니다. 이 시점에서 멤버는 오류 상태가 되지 않는데 이는 해당 멤버가 스스로 유효 상태로 돌아갈 수 있도록 독자적으로 이행할 수 있는 충분히 긴 `oplog` 를 누군가가 가지고 온라인 상태가 될 것이라 기대합니다.
* ARBITER
  * 아비터는 일반적인 연산 동안에는 아비터가 가진 특별한 상태인 ARBITER 를 유지해야 합니다.

다음과 같이 시스템 상의 문제를 나타내는 몇몇 상태가 있습니다.

* DOWN
  * 멤버가 살아 있지만 도달할 수 없는 상태가 되었다고 하겠습니다. 멤버는 이미 DOWN 으로 보고했지만 사실 여전히 살아 있고 단지 네트워크 문제 때문에 도달할 수 없을 뿐입니다.
* UNKNOWN
  * 멤버가 다른 멤버에 전혀 도달한 적이 없었다면 어떤 상태에 있는지 전혀 알 수 없으므로 UNKNOWN 으로 알립니다. 이는 일반적으로 알 수 없는 멤버가 다운되거나 두 멤버 간에 네트워크 문제가 있음을 가리킵니다.
* REMOVED
  * 멤버가 복제 셋으로부터 제거된 상태입니다. 만약 제거된 멤버가 복제 셋에 다시 추가된다면 NORMAL 상태로 변합니다.
* ROLLBACk
  * 이 상태는 멤버가 데이터를 롤백할 때 스입니다. 롤백 과정의 끝에서 서버는 복구 상태로 전환되고, 세컨더리가 됩니다.
* FATAL
  * 회복할 수 없는 무엇인가 잘못된 방향으로 흐르고 이 멤버가 기능을 정상화하는 시도를 포기할 때 나타나는 상태입니다. 무슨 이유로 이 상태를 발생시켰는지 확인하려면 로그를 봐야합니다.
  * 이 상태가 되면 일반적으로 서버를 종료하고 재동기화하거나 복원을 수행해야 합니다.

## Elections

멤버가 프라이머리에 도달하지 못하면 프라이머리 선출을 모색합니다. 선출도디고자 하는 멤버는 도달할 수 있는 다른 멤버들에게 선출에 대한 알림을 보냅니다. 알림을 받은 멤버들은 알림을 보낸 멤버가 프라이머리가 될 자격이 있는지 알아봅니다. 복제에 뒤처졌을 수도 있고 선출되기를 원하는 멤버가 도달할 수 없는 프라이머리가 이미 존재할 지도 모릅니다. 이 경우에 다른 멤버들이 그 선출을 더 이상 진행하지 않습니다.

반대할 이유가 없다고 가정하면, 다른 멤버들은 선출되고자 하는 멤버에 투표를 합니다. 만약 그 멤버가 복제 셋의 과반수로부터 득표하면, 그 선출은 성공적인 것이 되고, 해당 멤버는 프라이머리 상태로 전환됩니다. 만약 과반수로부터 득표하지 못하면, 그 멤버는 세컨더리 상태로 남게되고 다시 프라이머리가 되기위한 시도를 합니다. 프라이머리는 멤버와 과반수에 도달할 수 없거나 다운되거나, 세컨더리로 강등되거나, 복제 셋이 재구성될 때까지는 그 자격을 계속 유지합니다.

네트워크 상태가 양호하고 서버의 과반수가 살아 있다면 선출은 빠르게 진행됩니다. 프라이머리가 다운되는 것을 알리기 위해 멤버를 살아 있는 사앹로 만드는 데 2 초가 소요되고, 단지 몇 밀리초가 걸리는 선출을 즉시 시작합니다. 하지만 이 상황은 종종 최선이 아닐 수도 있는데, 네트워크에 문제가 있거나 너무 느리게 응답하는 과부하 서버때문에 선출이 발생할 수 있기 때문입니다. 이 경우 하트비트는 타임아웃을 위해 20 초를 소요합니다. 만약 그 시점에 선출 결과가 무승부라면 모든 멤버는 다른 선출을 시도하기 위해 30 초를 기다려야 합니다. 그러므로 만약 모든 것이 잘못되어 간다면 선출은 몇 분이 걸릴 수도 있습니다.

## Rollbacks

앞서 설명한 선출 과정은 프라이머리가 쓰기를 수행하고 세컨더리가 이를 복제하기 전에 프라이머리가 다운되면 다음에 선출되는 프라이머리가 쓰기를 수행하지 않습니다. `Example 2` 처럼 두 개의 데이터 센터, 즉 하나는 프라이머리와 세컨더리를 가지고 다른 하나는 세 개의 세컨더리를 가진다고 가정하겠습니다.

> Example 2 - A possible two-data-center configuration

![image](https://user-images.githubusercontent.com/44635266/80304412-8fa3d100-87f0-11ea-823d-e31eaa0669a5.png)

`Example 3` 처럼 두 데이터 센터 간에 네트워크 파티션이 존재한다고 가정하겠습니다. 첫 번째 데이터센터에 있는 서버들은 연산 126 까지 있지만, 그 데이터 센터는 아직 다른 데이터 센터에 있는 서버들로 복제되지 않습니다.

> Example 3 - Replication across data centers can be slower than within a single data center

![image](https://user-images.githubusercontent.com/44635266/80304417-9f231a00-87f0-11ea-8918-b200da5e4028.png)

다른 데이터 센터의 서버들은 복제 셋의 과반수에 도달할 수 있습니다. 그중 하나가 프라이머리로 선출될 수 있습니다. 이 새로운 프라이머리는 `Example 4` 처럼 쓰기를 수행합니다.

네트워크가 복구되면 첫 번째 데이터 센터의 서버들은 다른 서버들로부터 동기화를 하고자 연산 126 을 찾지만 결국 찾지 못합니다. 이런 현상이 발생할 때 A 와 B 는 **롤백(Rollback)** 이라는 과정을 시작합니다. 롤백은 복구 전에 복제되지 않은 연산을 원래 상태로 되돌리기 위해 사용됩니다. `oplog` 에 126 이 있는 서버들은 공통 지점을 찾기 위해 다른 데이터 센터 서버들의 `oplog` 를 살핍니다. 그리고 일치하는 가장 최신 연산이 125 임을 발견하게 됩니다. `EXample 5` 는 `oplog` 의 모습을 보여줍니다.

> Example 4 - Unreplicated writes won’t match writes on the other side of a network partition

![image](https://user-images.githubusercontent.com/44635266/80304426-a77b5500-87f0-11ea-9f5e-4ba3631cb1a8.png)

> Example 5 - Two members with conflicting oplogs: A apparently crashed before replicating ops 126−128, so these operations are not present on B, which has more recent operations. A will have to rollback these three operations before resuming syncing.

![image](https://user-images.githubusercontent.com/44635266/80304430-afd39000-87f0-11ea-90b8-74548534c7a5.png)

이 시점에서 `oplog` 에 126 이 있는 서버는 자신이 가진 연산을 살펴보고 그 연산에 의해 영향을 받은 각 문서의 버전에 대해 데이터 디렉토리의 `rollback` 디렉토리에 있는 *.bson* 파일에 쓰기를 수행합니다. 그래서 연산 126 이 갱신 작업이었다면, 연산 126 에 의해 업데이트된 문서를 *컬렉션명.bson* 으로 씁니다. 그 후 현재 프라이머리에서 해당 문서의 버전을 복제합니다.

다음은 전형적인 롤백으로부터 생성된 로그 항목들입니다.

```shell
Fri Oct  7 06:30:35 [rsSync] replSet syncing to: server-1
Fri Oct  7 06:30:35 [rsSync] replSet our last op time written: Oct  7 
    06:30:05:3 
Fri Oct  7 06:30:35 [rsSync] replset sources GTE: Oct  7 06:30:31:1
Fri Oct  7 06:30:35 [rsSync] replSet rollback 0
Fri Oct  7 06:30:35 [rsSync] replSet ROLLBACK
Fri Oct  7 06:30:35 [rsSync] replSet rollback 1
Fri Oct  7 06:30:35 [rsSync] replSet rollback 2 FindCommonPoint
Fri Oct  7 06:30:35 [rsSync] replSet info rollback our last optime:   Oct  7 
    06:30:05:3
Fri Oct  7 06:30:35 [rsSync] replSet info rollback their last optime: Oct  7 
    06:30:31:2
Fri Oct  7 06:30:35 [rsSync] replSet info rollback diff in end of log times: 
    -26 seconds
Fri Oct  7 06:30:35 [rsSync] replSet rollback found matching events at Oct  7 
   06:30:03:4118
Fri Oct  7 06:30:35 [rsSync] replSet rollback findcommonpoint scanned : 6
Fri Oct  7 06:30:35 [rsSync] replSet replSet rollback 3 fixup
Fri Oct  7 06:30:35 [rsSync] replSet rollback 3.5
Fri Oct  7 06:30:35 [rsSync] replSet rollback 4 n:3
Fri Oct  7 06:30:35 [rsSync] replSet minvalid=Oct  7 06:30:31 4e8ed4c7:2
Fri Oct  7 06:30:35 [rsSync] replSet rollback 4.6
Fri Oct  7 06:30:35 [rsSync] replSet rollback 4.7
Fri Oct  7 06:30:35 [rsSync] replSet rollback 5 d:6 u:0
Fri Oct  7 06:30:35 [rsSync] replSet rollback 6
Fri Oct  7 06:30:35 [rsSync] replSet rollback 7
Fri Oct  7 06:30:35 [rsSync] replSet rollback done
Fri Oct  7 06:30:35 [rsSync] replSet RECOVERING
Fri Oct  7 06:30:36 [rsSync] replSet syncing to: server-1
Fri Oct  7 06:30:36 [rsSync] replSet SECONDARY
```

해당 서버는 다른 서버로부터 동기화를 시작하고, 동기화 소스로부터 최신의 연산을 찾을 수 없다는 것을 인지합니다. 그 시점부터 롤백 상태로 전환(`replSet ROLLBACK`) 함으로써 롤백 프로세스를 시작하게 됩니다.

두 번재 단계에서는 26 초 전인 두 `oplog` 사이의 공통 지점을 발견합니다. 그 다음 `oplog` 에서 26 초 전의 연산을 실행 취소하기 시작합니다. 롤백이 완료되면 해당 서버는 복구상태로 전환되고 동기화를 시작합니다.

현재 프라이머리로 롤백된 연산을 적용하려면 먼저 해당 연산을 임시 컬렉션으로 로드하기 위해 `mogorestore` 를 사용합니다.

```shell
$ mongorestore --db stage --collection stuff \
> /data/db/rollback/important.stuff.2012-12-19T18-27-14.0.bson
```

문서들을 검증하고 그 문서들을 발생한 컬렉션의 현재 내용과 비교해야 합니다. 예를 들어 롤백 멤버에 일반 인덱스와 현재 프라이머리에 고유 인덱스를 만들엇다면, 롤백 데이터에 어떤 중복도 없으며 있더라도 그 문제를 해결할 수 있도록 확인해야 합니다.

원하는 스테이징 컬렉션 문서들의 버전을 가지고 있다면 이를 주 컬렉션으로 로드합니다.

```shell
> staging.stuff.find().forEach(function(doc) {
...     prod.stuff.insert(doc);
... })
```

입력 전용 컬렉션이 있다면 롤백 문서를 그 컬렉션으로 직접 로드할 수 있습니다. 컬렉션에 갱신 작업을 진행하고 있다면 어떻게 롤백 데이터를 병합할지에 대해 주의해야 합니다.

자주 오용되는 멤버 구성 옵션은 각 멤버가 가진 득표수입니다. 득표수를 조작해봤자 원하는 바가 달성되기보다는 수많은 롤백이 발생합니다. 규칙적인 롤백을 처리할 준비가 되기 전까지 득표수를 바꾸지 않는것이 좋습니다.

### When Rollbacks Fail

경우에 따라서 MongoDB 는 롤백이 수행되기에 너무 큰지 아닌지에 대한 결정을 내립니다. 만약 롤백에 시간이 30 분 이상 걸리거나 300 MB 이상의 데이터를 처리해야 한다면 롤백이 실패할 수 있습니다. 이 경우에 롤백에 갇힌 노드를 재동기화해야 합니다.

이 현상이 가장 일반적으로 발생하는 원인은 세컨더리가 뒤처지고 프라이머리가 다운될때입니다. 세컨더리 중 하나가 프라이머리가 되면 이전 프라이머리로부터 많은 연산들을 놓치게 됩니다. 멤버가 롤백에 갇히지 않게 하려면 세컨더리를 가능한 한 최신 상태로 유지하는게 좋습니다.