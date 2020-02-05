---
title : Hyperledger Network 구성 (BYFN)
tags :
- Kafka
- Zookeeper
- BYFN
- Hyperledger Fabric
- BlockChain
---

기존 포스트 까지는 orderer의 타입을 `solo`로 놓고 진행했습니다. 이번 포스트에서는 kafka를 이용해서 만들어 보겠습니다.

`fabric-samples`에서 제공하는 kafka 모드는 `zookeeper` 1개 `kafka` 1개로 이루어져 있습니다. 이 예제로 사용해도 되지만 그러면 zookeeper들간의 `Leader Election` 같은 중요한 부분을 놓칠 수 있으니 `zookeeper` 3개 `kafka` 4개로 만들어서 진행해보겠습니다.

아 그리고 이 방법은 VM 3개로 만드셔도 무방합니다. 해당 환경 셋팅은 아래처럼 하면 됩니다.

* VM1 kafka1 zookeeper1 orderer1 
* VM2 kafka1 zookeeper1 orderer1
* VM3 kafka2 zookeeper1 orderer1
* VM4 peer2
* VM5 peer2

제일먼저 `fabric-samples/first-nework` 폴더 안에 있는 `docker-compose-kafka.yaml` 파일을 확인하고 수정해 보겠습니다.

# Settings

`Setting` 부분은 [Hyperledger Fabric Network 구성 -1-](/blog/fabricnetwork1) 부분과 동일하니 똑같이 진행하시면 됩니다.

`HandOn` 부분부터 다릅니다.

# HandsOn

먼저 필요한 파일을 가져옵니다. 이전 예제와는 다르게 `bin`, `chaincode`만 가져오면 됩니다. 나머지는 제가 만들어논 깃 레포를 불러오면 됩니다.

```
$ git clone https://github.com/Has3ong/hyperledger-kafka.git
$ cd hyperledger-kafka

$ ls
base  configtx.yaml  crypto-config.yaml  docker-compose-kafka.yaml  README.md

$ sudo cp -r ../fabric-samples/bin .
$ sudo cp -r ../fabric-samples/chaincode .

$ mkdir channel-artifacts
```

`Kafka` 모드에서는 환경에 맞춰서 만든 깃헙 레포지토리를 이용해보겠습니다. 그리고 처음부터 끝까지 명령어를 치면서 진행하겠습니다.

먼저 제가 만들어논 레포를 가져오고 `fabric-samples`에서 필요한 파일을 가져오겠습니다.

`Kafka`와 `Zookeeper`에 대한 설명은 따로하지 않겠습니다.

### Manually generate the artifacts

첫 번째로 `cryptogen` 파일을 이용하여 인증서 파일을 만들어 줍니다. 인증서 파일들은 `crypto-config.yaml`을 확인해보시면 이해가 되실겁니다. 

전부 하나하나 뜯어보기에는 포스트의 양이 많아지기 때문에 추후에 정리해드리겠습니다.

```
$ ./bin/cryptogen generate --config=./crypto-config.yaml

org1.example.com
org2.example.com
```

다음 FABRIC_CFG_PATH를 현재 디렉토리로 설정합니다.

```
$ export FABRIC_CFG_PATH=$PWD
```

그 다음 우리가 사용할 Fabric 네트워크에 profile 즉, orderer type(?) 을 설정합니다. fabric-samples 에서 제공하는 종류로는 Solo, RAFT, Kafka 3가지가 있는데 지금은 Kafka로 사용하겠습니다.

```
$ ./bin/configtxgen -profile SampleDevModeKafka -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block

2019-10-22 16:20:04.785 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 16:20:04.854 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 002 orderer type: kafka
2019-10-22 16:20:04.854 UTC [common.tools.configtxgen.localconfig] Load -> INFO 003 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:20:04.920 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 004 orderer type: kafka
2019-10-22 16:20:04.920 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 005 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:20:04.922 UTC [common.tools.configtxgen] doOutputBlock -> INFO 006 Generating genesis block
2019-10-22 16:20:04.922 UTC [common.tools.configtxgen] doOutputBlock -> INFO 007 Writing genesis block
```

### Create a Channel Configuration Transaction

`channel.tx`파일을 만들어 주어야 합니다. `channel.tx`에는 현재 우리가 구현할 채널의 정책이나 조직의 정보가 담겨져 있다고 생각하면 됩니다.

그리고, 각각의 Org에 올라갈 `AnchorPeer`를 설정합니다. 이 모두에 대한 정보는 `configtx.yaml`에서 확인할 수 있습니다.


```
$ export CHANNEL_NAME=mychannel  && ./bin/configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME

2019-10-22 16:21:38.626 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 16:21:38.694 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:21:38.760 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: kafka
2019-10-22 16:21:38.760 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:21:38.761 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 005 Generating new channel configtx
2019-10-22 16:21:38.763 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 006 Writing new channel tx
```


```
$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP

2019-10-22 16:22:03.078 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 16:22:03.143 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:22:03.206 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: kafka
2019-10-22 16:22:03.207 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:22:03.207 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 16:22:03.208 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update

$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org2MSP

2019-10-22 16:22:15.177 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 16:22:15.245 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:22:15.311 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: kafka
2019-10-22 16:22:15.312 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/hyperledger-kafka/configtx.yaml
2019-10-22 16:22:15.312 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 16:22:15.313 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
```

여기 까지의 과정이 `byfn.sh`에서의 `generate`입니다.

### Start the network

이제 초기 설정은 끝났으니 네트워크를 시작해보겠습니다. `docker-compose-cli.yaml`과 `docker-compose-etcdraft2` 파일을 이용하여 도커 위에 올려줍니다.

마지막 -d 파라메터를 넣어주면 컨테이너의 로그가 안뜨고 백그라운드로 진행이 됩니다. 저는 `orderer`, `peer`들의 로그도 같이 보면서 진행할 예정이니 빼서 진행하겠습니다.

```
$ export IMAGE_TAG="latest"
$ export SYS_CHANNEL="byfn-sys-channel"
$ export COMPOSE_PROJECT_NAME=fabric

$ docker-compose -f docker-compose-kafka.yaml up
```

했을시 엄청나게 많은 로그가 나오는데요 이건 [여기](/blog/fabricnetwork3-log)서 확인할 수 있습니다. 엄청 길어서 따로 포스트 했습니다. 

위 포스트에서는 시작시 나오는 로그만 적었고 그외에 피어 채널을 만들던가 조인하는 과정에서 발생하는 로그는 `solo`와 다르니까 이 포스트에서 다루겠습니다.

현재 docker 컨테이너의 목록입니다.

```
$ docker ps

CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS                                                                       NAMES
ded764ed15a7        hyperledger/fabric-tools:latest     "/bin/bash"              31 seconds ago      Up 29 seconds                                                                                   cli
6ee2bede7a1b        hyperledger/fabric-orderer:latest   "orderer"                33 seconds ago      Up 31 seconds       0.0.0.0:7050->7050/tcp                                                      orderer.example.com
8a22ee0028b2        hyperledger/fabric-kafka            "/docker-entrypoint.…"   37 seconds ago      Up 34 seconds       0.0.0.0:12092->9092/tcp, 0.0.0.0:12093->9093/tcp                            kafka3.example.com
b111540fac69        hyperledger/fabric-kafka            "/docker-entrypoint.…"   37 seconds ago      Up 33 seconds       0.0.0.0:10092->9092/tcp, 0.0.0.0:10093->9093/tcp                            kafka1.example.com
b11af475160f        hyperledger/fabric-kafka            "/docker-entrypoint.…"   37 seconds ago      Up 33 seconds       0.0.0.0:9092-9093->9092-9093/tcp                                            kafka0.example.com
cdc5d93847ab        hyperledger/fabric-kafka            "/docker-entrypoint.…"   37 seconds ago      Up 33 seconds       0.0.0.0:11092->9092/tcp, 0.0.0.0:11093->9093/tcp                            kafka2.example.com
b02247bb20be        hyperledger/fabric-peer:latest      "peer node start"        41 seconds ago      Up 37 seconds       0.0.0.0:9051->7051/tcp, 0.0.0.0:9053->7053/tcp                              peer0.org2.example.com
dde0266a73ae        hyperledger/fabric-zookeeper        "/docker-entrypoint.…"   41 seconds ago      Up 37 seconds       0.0.0.0:22181->2181/tcp, 0.0.0.0:22888->2888/tcp, 0.0.0.0:23888->3888/tcp   zookeeper2.example.com
d35cc0974733        hyperledger/fabric-peer:latest      "peer node start"        41 seconds ago      Up 37 seconds       0.0.0.0:8051->7051/tcp, 0.0.0.0:8053->7053/tcp                              peer1.org1.example.com
efd6d970ecea        hyperledger/fabric-peer:latest      "peer node start"        41 seconds ago      Up 37 seconds       0.0.0.0:10051->7051/tcp, 0.0.0.0:10053->7053/tcp                            peer1.org2.example.com
878b55ad2ff1        hyperledger/fabric-zookeeper        "/docker-entrypoint.…"   41 seconds ago      Up 37 seconds       0.0.0.0:12181->2181/tcp, 0.0.0.0:12888->2888/tcp, 0.0.0.0:13888->3888/tcp   zookeeper1.example.com
f15a30013765        hyperledger/fabric-peer:latest      "peer node start"        41 seconds ago      Up 39 seconds       0.0.0.0:7051->7051/tcp, 0.0.0.0:7053->7053/tcp                              peer0.org1.example.com
42c54c6407d5        hyperledger/fabric-zookeeper        "/docker-entrypoint.…"   41 seconds ago      Up 38 seconds       0.0.0.0:2181->2181/tcp, 0.0.0.0:2888->2888/tcp, 0.0.0.0:3888->3888/tcp      zookeeper0.example.com
```

네트워크 구성을 하기전에 몇 가지 알아보고 가겠습니다. 

## Zookeeper Leader Election

주키퍼에서 리더 선출하는 과정을 한번 확인해보겠습니다. 일단 제일먼저 리더를 찾아봐야합니다. 제가 확인해봤을때 현재 1번 주키퍼가 리더인 상태입니다. `LEADING`이라는걸 보고 확인할 수 있습니다.

![스크린샷 2019-10-23 오전 4 27 27](https://user-images.githubusercontent.com/44635266/67323708-d0731280-f54d-11e9-9af4-fe8c03d53095.png)

```
2019-10-22 16:35:36,072 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:QuorumPeer@856] - LEADING
2019-10-22 16:35:36,077 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Leader@59] - TCP NoDelay set to: true
```

그럼 여기서 1번 주키퍼를 죽여보겠습니다.

```
$ docker stop zookeeper1.example.com
```

![스크린샷 2019-10-23 오전 4 27 59](https://user-images.githubusercontent.com/44635266/67323709-d0731280-f54d-11e9-8351-72a010ddc378.png)

그렇게 되면 리더가 없다는 에러를 발생시키고 다시 리더를 선출하게됩니다. 2번 주키퍼가 리더가 되었네요.

```
2019-10-22 16:47:39,235 [myid:3] - WARN  [QuorumPeer[myid=3]/0.0.0.0:2181:Follower@87] - Exception when following the leader
```

만약 리더를 한 번더 죽이면 어떻게 될까요. 그러면 3개의 주키퍼중 과반수 이상이 죽었기 때문에 리더 선출을 하지 못하고 정상적인 시스템 작동이 불가능하게 됩니다.

```
$ docker stop zookeeper2.example.com
```

![스크린샷 2019-10-23 오전 4 28 17](https://user-images.githubusercontent.com/44635266/67324104-40819880-f54e-11e9-83e1-5a4da041be24.png)

## Kafka Leader Election

이전에는 주키퍼에서 리더 선출하는 과정을 한번 확인해보았는데. 이번에는 카프카로 확인해 보겠습니다. 현재 카프카의 리더는 1번 카프카입니다.

제가 설정을 잘못했는지 `kafka3.example.com`이 붙지를 않네요. 그점 감안하셔서 보면 될거같습니다.

![스크린샷 2019-10-23 오전 4 53 08](https://user-images.githubusercontent.com/44635266/67326361-665c6c80-f551-11e9-8eb2-6e82abade140.png)

하나씩 죽이면서 어떻게 변화되는지 알아보겠습니다.

```
$ docker stop kafka1.example.com
```

![스크린샷 2019-10-23 오전 4 54 03](https://user-images.githubusercontent.com/44635266/67326363-665c6c80-f551-11e9-9d73-5337a3d92c2a.png)

```
$ docker stop kafka2.example.com
```

![스크린샷 2019-10-23 오전 4 55 13](https://user-images.githubusercontent.com/44635266/67326364-66f50300-f551-11e9-9b0e-d3a68ea62cd4.png)

카프카는 주키퍼와 다르게 3개중에 과반수 이상이 고장이나서 정지가 되어도 시스템이 유지가 됩니다.

그럼 다시 `kafk1`과 `kafka2`를 살려보겠습니다.

```
$ docker start kafka1.example.com
$ docker start kafka2.example.com
```

![스크린샷 2019-10-23 오전 4 55 44](https://user-images.githubusercontent.com/44635266/67326366-66f50300-f551-11e9-899e-579a263b832b.png)


그러면 아래와 같은 로그가 적힙니다.

```
[2019-10-22 19:55:24,960] INFO [Partition byfn-sys-channel-0 broker=0] Expanding ISR from 0 to 0,1 (kafka.cluster.Partition)
[2019-10-22 19:55:30,000] INFO [Partition byfn-sys-channel-0 broker=0] Expanding ISR from 0,1 to 0,1,2 (kafka.cluster.Partition)
```

카프카에 복제인 `ISR`이 만들어지면서 다시 정상적으로 작동하는것을 확인할 수 있습니다. `ISR`은 `replication group`이라고 이해하시면 쉬울것입니다.

이 리더 선출을 포스트에 담기 위해서 주키퍼와 카프카를 각각 3개 4개씩 생성했습니다.

다음으로는 네트워크를 돌려볼게요.


`cli` 컨테이너에 들어가서 피어들에게 명령을 주겠습니다.

```
docker exec -it cli bash

root@0d78bb69300d:/opt/gopath/src/github.com/hyperledger/fabric/peer#
```

### Create & Join Channel

```
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
CORE_PEER_ADDRESS=peer0.org1.example.com:7051
CORE_PEER_LOCALMSPID="Org1MSP"
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt

export CHANNEL_NAME=mychannel
export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

$ peer channel create -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/channel.tx --tls --cafile $ORDERER_CA

2019-10-22 17:17:59.288 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 17:17:59.298 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 17:17:59.322 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 17:17:59.373 UTC [cli.common] readBlock -> INFO 004 Got status: &{NOT_FOUND}
2019-10-22 17:17:59.395 UTC [channelCmd] InitCmdFactory -> INFO 005 Endorser and orderer connections initialized
2019-10-22 17:17:59.600 UTC [cli.common] readBlock -> INFO 006 Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 17:17:59.603 UTC [channelCmd] InitCmdFactory -> INFO 007 Endorser and orderer connections initialized
2019-10-22 17:17:59.807 UTC [cli.common] readBlock -> INFO 008 Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 17:17:59.810 UTC [channelCmd] InitCmdFactory -> INFO 009 Endorser and orderer connections initialized
2019-10-22 17:18:00.016 UTC [cli.common] readBlock -> INFO 00a Received block: 0
```

카프카와 오더러의 로그를 보겠습니다. 가장 오른쪽이 오더러이며 왼쪽으로 한칸씩 가면서 leader 카프카, follower 카프카 입니다.


![스크린샷 2019-10-23 오전 5 07 59](https://user-images.githubusercontent.com/44635266/67327580-1e3e4980-f553-11e9-9c8c-b28089e74e1f.png)


![스크린샷 2019-10-23 오전 5 07 03](https://user-images.githubusercontent.com/44635266/67327488-fa7b0380-f552-11e9-94ed-04f07be3f882.png)


가장 큰 특징으로는 리더 카프카에서는 `Topic`을 만들었고 다른 `follower`들은 리더에 데이터를 복제했습니다. 마지막으로 오더러에서는 `producer`와, `consumer`를 Setting했다고 나오네요.

```
$ peer channel join -b mychannel.block

2019-10-22 18:27:58.955 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:27:58.960 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:27:58.969 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:27:58.998 UTC [channelCmd] executeJoin -> INFO 004 Successfully submitted proposal to join channel


$ CORE_PEER_ADDRESS=peer1.org1.example.com:8051 \
peer channel join -b mychannel.block

2019-10-22 18:28:04.276 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:04.280 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:04.284 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:28:04.307 UTC [channelCmd] executeJoin -> INFO 004 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 18:28:09.625 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:09.631 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:09.636 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:28:09.661 UTC [channelCmd] executeJoin -> INFO 004 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 18:28:15.381 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:15.386 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:15.389 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:28:15.419 UTC [channelCmd] executeJoin -> INFO 004 Successfully submitted proposal to join channel
```

### Update Anchor Peer

```
$ peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org1MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 18:28:54.867 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:54.871 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:28:54.874 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:28:54.898 UTC [channelCmd] update -> INFO 004 Successfully submitted channel update


$ CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org2MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 18:29:07.687 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:29:07.691 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:29:07.695 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 18:29:07.721 UTC [channelCmd] update -> INFO 004 Successfully submitted channel update
```

### Install Chaincode

```
$ peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 18:35:31.465 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:31.473 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:31.479 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 003 Using default escc
2019-10-22 18:35:31.479 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 004 Using default vscc
2019-10-22 18:35:31.801 UTC [chaincodeCmd] install -> INFO 005 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer1.org1.example.com:8051 \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 15:37:21.836 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 15:37:21.837 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 15:37:21.961 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 18:35:53.716 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:53.722 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:53.731 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 003 Using default escc
2019-10-22 18:35:53.731 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 004 Using default vscc
2019-10-22 18:35:53.888 UTC [chaincodeCmd] install -> INFO 005 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 18:35:57.818 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:57.823 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:35:57.831 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 003 Using default escc
2019-10-22 18:35:57.831 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 004 Using default vscc
2019-10-22 18:35:58.011 UTC [chaincodeCmd] install -> INFO 005 Installed remotely response:<status:200 payload:"OK" >
```

### ChacinCode Instantiate

```
$ peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.peer','Org2MSP.peer')"

2019-10-22 18:36:30.531 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:36:30.537 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:36:30.552 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 003 Using default escc
2019-10-22 18:36:30.552 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 004 Using default vscc
```

### ChainCode Query

```
$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'
100

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","b"]}'
200
```

### ChainCode Invoke
```
$ peer chaincode invoke -o orderer.example.com:7050  --tls --cafile $ORDERER_CA  -C $CHANNEL_NAME -n mycc -c '{"Args":["invoke","a","b","10"]}'

2019-10-22 18:37:10.074 UTC [main] InitCmd -> WARN 001 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:37:10.079 UTC [main] SetOrdererEnv -> WARN 002 CORE_LOGGING_LEVEL is no longer supported, please use the FABRIC_LOGGING_SPEC environment variable
2019-10-22 18:37:10.105 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 003 Chaincode invoke successful. result: status:200
```

### ChainCode Query

```
$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'
90

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","b"]}'
210
```

체인코드까지 정상적으로 작동했습니다. 이 포스트는 여기로 마무리하고 다음엔 Raft를 이용한 하이퍼렛져 페브릭 네트워크 구성으로 찾아뵙겠습니다.

읽어주셔서 감사합니다.



