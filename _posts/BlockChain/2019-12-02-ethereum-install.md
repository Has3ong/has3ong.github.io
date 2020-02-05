---
title : Ethereum 환경 설치하기 및 거래 송금하기
tags :
- Go
- Geth
- Ethereum
- BlockChain
---

### RunTime Environment

* macOS Catalina version 10.15.1

## 1. Install Go

```
$ brew install go
```

```
$ go version
go version go1.13.4 darwin/amd64
```

## 2. Install Geth

Homebrew를 이용하여 간단하게 Geth를 설치할 수 있습니다. Homebrew가 설치되어 있지 않다면 설치 해야합니다.

```
$ brew tap ethereum/ethereum
$ brew install ethereum
```

geth를 입력했을 떄 다음과같은 로그가 나오면 설치를 완료한것입니다.

```
$ geth
INFO [12-02|04:09:10.076] Bumping default cache on mainnet         provided=1024 updated=4096
INFO [12-02|04:09:10.077] Maximum peer count                       ETH=50 LES=0 total=50
INFO [12-02|04:09:10.094] Starting peer-to-peer node               instance=Geth/v1.9.8-stable/darwin-amd64/go1.13.4
INFO [12-02|04:09:10.094] Allocated trie memory caches             clean=1024.00MiB dirty=1024.00MiB
INFO [12-02|04:09:10.094] Allocated cache and file handles         database=/Users/has3ong/Library/Ethereum/geth/chaindata cache=2.00GiB handles=5120
INFO [12-02|04:09:10.181] Opened ancient database                  database=/Users/has3ong/Library/Ethereum/geth/chaindata/ancient
INFO [12-02|04:09:10.182] Writing default main-net genesis block
INFO [12-02|04:09:10.429] Persisted trie from memory database      nodes=12356 size=1.79MiB time=47.878259ms gcnodes=0 gcsize=0.00B gctime=0s livenodes=1 livesize=0.00B
INFO [12-02|04:09:10.429] Initialised chain configuration          config="{ChainID: 1 Homestead: 1150000 DAO: 1920000 DAOSupport: true EIP150: 2463000 EIP155: 2675000 EIP158: 2675000 Byzantium: 4370000 Constantinople: 7280000 Petersburg: 7280000 Istanbul: 9069000 Engine: ethash}"
INFO [12-02|04:09:10.429] Disk storage enabled for ethash caches   dir=/Users/has3ong/Library/Ethereum/geth/ethash count=3
INFO [12-02|04:09:10.429] Disk storage enabled for ethash DAGs     dir=/Users/has3ong/Library/Ethash count=2
INFO [12-02|04:09:10.429] Initialising Ethereum protocol           versions="[64 63]" network=1 dbversion=<nil>
WARN [12-02|04:09:10.429] Upgrade blockchain database version      from=<nil> to=7
INFO [12-02|04:09:10.430] Loaded most recent local header          number=0 hash=d4e567…cb8fa3 td=17179869184 age=50y7mo3w
INFO [12-02|04:09:10.430] Loaded most recent local full block      number=0 hash=d4e567…cb8fa3 td=17179869184 age=50y7mo3w
INFO [12-02|04:09:10.430] Loaded most recent local fast block      number=0 hash=d4e567…cb8fa3 td=17179869184 age=50y7mo3w
INFO [12-02|04:09:10.430] Regenerated local transaction journal    transactions=0 accounts=0
INFO [12-02|04:09:10.457] Allocated fast sync bloom                size=2.00GiB
INFO [12-02|04:09:10.491] New local node record                    seq=1 id=dbeb9d8785f5d8e3 ip=127.0.0.1 udp=30303 tcp=30303
INFO [12-02|04:09:10.492] Started P2P networking                   self=enode://45b350e5871bc9273bfdedabf3f1958979bd2be86a0982f7b03213433911f8dcbbd49e49421615c0108d1a96edeb08e29848993a808b729459e79974b96cc5fd@127.0.0.1:30303
INFO [12-02|04:09:10.493] IPC endpoint opened                      url=/Users/has3ong/Library/Ethereum/geth.ipc
INFO [12-02|04:09:10.536] Initialized fast sync bloom              items=12356 errorrate=0.000 elapsed=78.754ms
INFO [12-02|04:09:12.638] Mapped network port                      proto=udp extport=30303 intport=30303 interface="UPNP IGDv2-IP1"
INFO [12-02|04:09:12.646] New local node record                    seq=2 id=dbeb9d8785f5d8e3 ip=211.214.14.153 udp=30303 tcp=30303
INFO [12-02|04:09:12.650] Mapped network port                      proto=tcp extport=30303 intport=30303 interface="UPNP IGDv2-IP1"
INFO [12-02|04:09:20.497] Block synchronisation started
WARN [12-02|04:09:34.669] Dropping unsynced node during fast sync  id=78d91b32df671fb4 conn=dyndial addr=178.170.102.139:30303 type=Geth/v4.2.0-c999068/linux/go1.9.2
```

### Geth 데이터 디렉토리 구조

```
~/Library/Ethereum

.
├── geth
│   ├── LOCK
│   ├── chaindata
│   │   ├── 000001.log
│   │   ├── CURRENT
│   │   ├── LOCK
│   │   ├── LOG
│   │   ├── MANIFEST-000000
│   │   └── ancient
│   │       ├── FLOCK
│   │       ├── bodies.0000.cdat
│   │       ├── bodies.cidx
│   │       ├── diffs.0000.rdat
│   │       ├── diffs.ridx
│   │       ├── hashes.0000.rdat
│   │       ├── hashes.ridx
│   │       ├── headers.0000.cdat
│   │       ├── headers.cidx
│   │       ├── receipts.0000.cdat
│   │       └── receipts.cidx
│   ├── nodekey
│   ├── nodes
│   │   ├── 000001.log
│   │   ├── CURRENT
│   │   ├── LOCK
│   │   ├── LOG
│   │   └── MANIFEST-000000
│   └── transactions.rlp
└── keystore
```

**chaindata** : 블록체인 데이터가 저장된다.
**keystore** : 어카운트의 개인 키를 저장한다.

## Geth Simple HandsOn

Geth 로컬 테스트 네트워크로 접속해서 계좌를 등록하고 채굴을 진행한 뒤 이더 송금까지의 과정을 진행해보겠습니다.

로컬 테스트넷에서 Geth 를 가동하기 위해선 두가지를 준비해야합니다.

1. 데이터 디렉터리 ( chaindata )
2. genesis.json 파일

> genesis.json

```
{
  "coinbase"   : "0x0000000000000000000000000000000000000001",
  "difficulty" : "0x20000",
  "extraData"  : "",
  "gasLimit"   : "0x8000000",
  "nonce"      : "0x0000000000000042",
  "mixhash"    : "0x0000000000000000000000000000000000000000000000000000000000000000",
  "parentHash" : "0x0000000000000000000000000000000000000000000000000000000000000000",
  "timestamp"  : "0x00",
  "alloc": {},
  "config": {
        "chainId": 15,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0
    }
}
```

Geth로 초기화를 진행합니다.

```
$ geth --datadir=./chaindata/ init ./genesis.json

INFO [12-02|04:41:47.755] Maximum peer count                       ETH=50 LES=0 total=50
INFO [12-02|04:41:47.770] Allocated cache and file handles         database=/Users/has3ong/Desktop/ethereum/chaindata/geth/chaindata cache=16.00MiB handles=16
INFO [12-02|04:41:47.798] Writing custom genesis block
INFO [12-02|04:41:47.798] Persisted trie from memory database      nodes=0 size=0.00B time=9.994µs gcnodes=0 gcsize=0.00B gctime=0s livenodes=1 livesize=0.00B
INFO [12-02|04:41:47.798] Successfully wrote genesis state         database=chaindata hash=9b8d4a…9021ba
INFO [12-02|04:41:47.798] Allocated cache and file handles         database=/Users/has3ong/Desktop/ethereum/chaindata/geth/lightchaindata cache=16.00MiB handles=16
INFO [12-02|04:41:47.829] Writing custom genesis block
INFO [12-02|04:41:47.829] Persisted trie from memory database      nodes=0 size=0.00B time=4.05µs  gcnodes=0 gcsize=0.00B gctime=0s livenodes=1 livesize=0.00B
INFO [12-02|04:41:47.830] Successfully wrote genesis state         database=lightchaindata hash=9b8d4a…9021ba
```

네트워크로 접속합니다.

```
$ geth --networkid 4649 --nodiscover --maxpeers 0 --datadir chaindata console 2>> chaindata/geth.log

Welcome to the Geth JavaScript console!

instance: Geth/v1.9.8-stable/darwin-amd64/go1.13.4
at block: 0 (Thu, 01 Jan 1970 09:00:00 KST)
 datadir: /Users/has3ong/Desktop/ethereum/chaindata
 modules: admin:1.0 debug:1.0 eth:1.0 ethash:1.0 miner:1.0 net:1.0 personal:1.0 rpc:1.0 txpool:1.0 web3:1.0
```

* -- networkdid / 네트워크 식별자로 쓰인다. 0~3까지는 예약어이다.
* -- nodiscover / 생성자의 노드를 다른 노드에서 검색할 수 없게 하는 옵션이다. 노드 추가는 수동으로 해야함,
* -- maxpeers 0 / 생성자의 노드에 연결할 수 있는 노드의 수를 지정함, 0은 다른 노드와 연결안함
* -- datadir / 데이터 디렉토리 저정
* console / 콘솔로 진입한다.
* 2>> / 데이터 디렉토리/geth.log 로그 파일 만들때 사용하는 옵션 리눅스 셀 명령어


그리고 현재 접속한 네트워크의 어카운트와 블록 넘버를 확인한다. 현재 어카운트는 없으며, 블록넘버는 0이다.

```
> eth.accounts
[]
> eth.blockNumber
0
>
```

가상으로 거래를 만들 송신자 `Sender`와 수신자 `Receiver`의 계좌를 만들어준다.

```
> personal.newAccount("Sender")
"0xb156e708ff91b41dd29dd15603075a8f4d87c576"
> personal.newAccount("Receiver")
"0x02fef921ce74db5c6ab469fad5e9a652cc2859f2"
> eth.accounts
["0xb156e708ff91b41dd29dd15603075a8f4d87c576", "0x02fef921ce74db5c6ab469fad5e9a652cc2859f2"]

> eth.getBalance(eth.accounts[0]) // Sender의 계좌 잔액
0
> eth.getBalance(eth.accounts[1]) // Receiver의 계좌 잔액
0
>
```

그리고 `Sender`를 채굴에 성공하면 이더랄 저장할 기본 어카운트인 코인베이스로 지정합니다.

```
> miner.setEtherbase(eth.accounts[0])
true
```

채굴해서 잔고를 채운후 잠시 후에 채굴을 종료합니다.

```
> miner.start(4) // null or true
null
> miner.hashrate // 1086190 or 0
0
> miner.mining
true
> eth.blockNumber
16
> eth.getBalance(eth.coinbase)
140000000000000000000
> eth.getBalance(eth.coinbase)
145000000000000000000
> miner.stop()
null
> eth.blockNumber
32
```

그리고 계좌 잔액을 조회해보겠습니다.

```
> eth.getBalance(eth.coinbase)
160000000000000000000
> eth.getBalance(eth.accounts[0])
160000000000000000000
> eth.getBalance(eth.accounts[1])
0
```

현재 단위가 높아서 이더 양이 많아보이지만 최소단위인 wei로 표현되서 그렇습니다. 이더로 표현을 다시 해보겠습니다.

```
web3.fromWei(eth.getBalance(eth.accounts[0]),"ether")
160
```

이제 송금을 진행해보겠습니다.

```
> sender = eth.accounts[0]
"0xb156e708ff91b41dd29dd15603075a8f4d87c576"
> receiver = eth.accounts[1]
"0x02fef921ce74db5c6ab469fad5e9a652cc2859f2"
> eth.sendTransaction({from : sender, to : receiver, value: web3.toWei(1, "ether"), gasLimit: 30400, gasPrice: 10000000000000})
Error: authentication needed: password or unlock
    at web3.js:3143:20
    at web3.js:6347:15
    at web3.js:5081:36
    at <anonymous>:1:1
```

위 트랜잭션을 실행하면 `Sender`의 계정이 Lock이 되어있어서 Unlock 될대까지 예외사항이 발생합니다. 그렇기 때문에 계정의 Lock을 해제시켜줍니다.

```
> personal.unlockAccount(sender)
Unlock account 0xb156e708ff91b41dd29dd15603075a8f4d87c576
Password: // "Sender" 라고 계정의 이름을 입력한다.
true
>
```

다시 송금을 진행해보겠습니다.

```
> eth.sendTransaction({from : sender, to : receiver, value: web3.toWei(1, "ether"), gasLimit: 30400, gasPrice: 10000000000000})
"0x09cb1acd5b05b64ffce8c40b854584b0d41c19c13e3f54478e8b076c66ccb1fe"
> eth.getBalance(eth.accounts[1])
0
```

`Receiver`의 잔액을 조회하면 여전히 0원이다. 이는 트랜잭션이 바로 수행되지 않고 대기 상태에 빠져있기 떄문입니다.

대기 상태의 트랜잭션 실행을 위해서는 마이닝 작업을 진행해야합니다. 마이닝 작업을 통해 신규 블록이 생성되며 해당 블록에 포함되어 있는 트랜잭션 수행이 완료가 됩니다.

```
> eth.pendingTransactions
[{
    blockHash: null,
    blockNumber: null,
    from: "0xb156e708ff91b41dd29dd15603075a8f4d87c576",
    gas: 21000,
    gasPrice: 10000000000000,
    hash: "0x09cb1acd5b05b64ffce8c40b854584b0d41c19c13e3f54478e8b076c66ccb1fe",
    input: "0x",
    nonce: 0,
    r: "0x5c4745a5c690bd934cbf5bc14e9ce7fffbb4e334acf1c519886479aa90a65408",
    s: "0x24bc048b2932601bba6d3f2562a5e4ccb34d8bc91e4f36034cafd13ee890b529",
    to: "0x02fef921ce74db5c6ab469fad5e9a652cc2859f2",
    transactionIndex: null,
    v: "0x41",
    value: 1000000000000000000
}]
> miner.start(1)
null
> miner.stop()
null
> eth.pendingTransactions
[]
> eth.getBalance(eth.accounts[1])
1000000000000000000
>
```

확인결과 정상적으로 트랜잭션이 처리된것을 알 수 있습니다.

해당 로그 참고로 확인하시면 될거같습니다.

```
INFO [12-02|05:19:23.387] Submitted transaction                    fullhash=0x09cb1acd5b05b64ffce8c40b854584b0d41c19c13e3f54478e8b076c66ccb1fe recipient=0x02FeF921ce74db5c6Ab469FAD5e9a652cC2859F2
INFO [12-02|05:20:05.169] Updated mining threads                   threads=1
INFO [12-02|05:20:05.169] Transaction pool price threshold updated price=1000000000
INFO [12-02|05:20:05.169] Commit new mining work                   number=33 sealhash=845dd1…6f4fbf uncles=0 txs=0 gas=0 fees=0 elapsed=101.379µs
INFO [12-02|05:20:05.170] Commit new mining work                   number=33 sealhash=dc6747…236859 uncles=0 txs=1 gas=21000 fees=0.21 elapsed=399.623µs
INFO [12-02|05:20:08.601] Successfully sealed new block            number=33 sealhash=dc6747…236859 hash=eab9f0…89bf82 elapsed=3.431s
INFO [12-02|05:20:08.601] 🔗 block reached canonical chain          number=26 hash=1f36a4…735733
INFO [12-02|05:20:08.601] 🔨 mined potential block                  number=33 hash=eab9f0…89bf82
INFO [12-02|05:20:08.602] Commit new mining work                   number=34 sealhash=c07d32…ecf7d6 uncles=0 txs=0 gas=0     fees=0    elapsed=149.528µs
```