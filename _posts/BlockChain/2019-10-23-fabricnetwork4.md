---
title : Hyperledger Network 구성 (BYFN)
tags :
- RAFT
- BYFN
- Hyperledger Fabric
---

기존 포스트 까지는 orderer의 타입을 `solo`로와 `kafka` 놓고 진행했습니다. 이번 포스트에서는 `raft`를 이용해서 만들어 보겠습니다.

`fabric-samples`에서 제공하는 RAFT 모드는 `orderer` 5개로 이루어져 있습니다.

그래서 서로 

# Settings

`Setting` 부분은 [Hyperledger Fabric Network 구성 -1-](/blog/fabricnetwork1) 부분과 동일하니 똑같이 진행하시면 됩니다.

`HandOn` 부분부터 다릅니다.

# HandsOn

여기서 부터는 `byfn.sh` 내부를 들어가서 하나하나 명령어를 치면서 따라가셔도 되고 [Glossary](https://hyperledger-fabric.readthedocs.io/en/release-1.4/build_network.html) 문서를 따라가셔도 똑같습니다.

먼저 빈 파일을 만들어보겠습니다.

```
$ mkdir has3ong
$ cd has3ong
$ ls
```

그리고 이 파일에 필요한 파일들을 복사하겠습니다.

`bin`, `base`, `chaincode`, `configtx.yaml`, `crypto-config.yaml`, `docker-compose-cli.yaml`, `docker-compose-etcdraft2.yaml` 입니다.

```
$ sudo cp -r ../fabric-samples/bin .
$ sudo cp -r ../fabric-samples/first-network/base .
$ sudo cp -r ../fabric-samples/first-network/configtx.yaml .
$ sudo cp -r ../fabric-samples/first-network/crypto-config.yaml .
$ sudo cp -r ../fabric-samples/first-network/docker-compose-cli.yaml .
$ sudo cp -r ../fabric-samples/first-network/docker-compose-etcdraft2.yaml .
$ sudo cp -r ../fabric-samples/chaincode .
$ mkdir channel-artifacts
```

파일을 다 옮기고 나면 현재와 같은 상태가 만들어집니다.

```
$ ls
base  bin  chaincode  channel-artifacts  configtx.yaml  crypto-config.yaml  docker-compose-cli.yaml  docker-compose-etcdraft2.yaml
```

### Manually generate the artifacts

첫 번째로 `cryptogen` 파일을 이용하여 인증서 파일을 만들어 줍니다. 인증서 파일들은 `crypto-config.yaml`을 확인해보시면 이해가 되실겁니다. 

전부 하나하나 뜯어보기에는 포스트의 양이 많아지기 때문에 추후에 정리해드리겠습니다.

```
$ ./bin/cryptogen generate --config=./crypto-config.yaml

org1.example.com
org2.example.com
```

다음 `FABRIC_CFG_PATH`를 현재 디렉토리로 설정합니다.

```
$ export FABRIC_CFG_PATH=$PWD
```

그다음 우리가 사용할 Fabric 네트워크에 `profile` 즉, orderer type(?) 을 설정합니다. `fabric-samples` 에서 제공하는 종류로는 `Solo`, `RAFT`, `Kafka` 3가지가 있는데 지금은 `RAFT`로 사용하겠습니다.

RAFT

```
$ ./bin/configtxgen -profile SampleMultiNodeEtcdRaft -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block

2019-10-22 20:19:45.363 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 20:19:45.421 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 002 orderer type: etcdraft
2019-10-22 20:19:45.421 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 Orderer.EtcdRaft.Options unset, setting to tick_interval:"500ms" election_tick:10 heartbeat_tick:1 max_inflight_blocks:5 snapshot_interval_size:20971520
2019-10-22 20:19:45.421 UTC [common.tools.configtxgen.localconfig] Load -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:19:45.473 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 005 orderer type: solo
2019-10-22 20:19:45.473 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 006 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:19:45.475 UTC [common.tools.configtxgen] doOutputBlock -> INFO 007 Generating genesis block
2019-10-22 20:19:45.475 UTC [common.tools.configtxgen] doOutputBlock -> INFO 008 Writing genesis block
```

### Create a Channel Configuration Transaction

`channel.tx`파일을 만들어 주어야 합니다. `channel.tx`에는 현재 우리가 구현할 채널의 정책이나 조직의 정보가 담겨져 있다고 생각하면 됩니다.

그리고, 각각의 Org에 올라갈 `AnchorPeer`를 설정합니다. 이 모두에 대한 정보는 `configtx.yaml`에서 확인할 수 있습니다.

```
$ export CHANNEL_NAME=mychannel  && ./bin/configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME

2019-10-22 20:20:03.636 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 20:20:03.697 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:03.747 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-22 20:20:03.747 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:03.747 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 005 Generating new channel configtx
2019-10-22 20:20:03.749 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 006 Writing new channel tx

$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP

2019-10-22 20:20:16.260 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 20:20:16.326 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:16.392 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-22 20:20:16.392 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:16.393 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 20:20:16.393 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update


$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org2MSP

2019-10-22 20:20:28.067 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 20:20:28.125 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:28.180 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-22 20:20:28.181 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 20:20:28.181 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 20:20:28.181 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
```

여기 까지의 과정이 `byfn.sh`에서의 `generate`입니다.

### Start the network

이제 초기 설정은 끝났으니 네트워크를 시작해보겠습니다. `docker-compose-cli.yaml`과 `docker-compose-etcdraft2` 파일을 이용하여 도커 위에 올려줍니다.

마지막 -d 파라메터를 넣어주면 컨테이너의 로그가 안뜨고 백그라운드로 진행이 됩니다. 저는 `orderer`, `peer`들의 로그도 같이 보면서 진행할 예정이니 빼서 진행하겠습니다.

```
$ export IMAGE_TAG="latest"
$ export SYS_CHANNEL="byfn-sys-channel"
$ export COMPOSE_PROJECT_NAME=fabric

docker-compose -f docker-compose-cli.yaml up -d

Creating network "fabric_byfn" with the default driver
Creating volume "fabric_orderer.example.com" with default driver
Creating volume "fabric_peer0.org1.example.com" with default driver
Creating volume "fabric_peer1.org1.example.com" with default driver
Creating volume "fabric_peer0.org2.example.com" with default driver
Creating volume "fabric_peer1.org2.example.com" with default driver
Creating volume "fabric_orderer2.example.com" with default driver
Creating volume "fabric_orderer3.example.com" with default driver
Creating volume "fabric_orderer4.example.com" with default driver
Creating volume "fabric_orderer5.example.com" with default driver
Creating orderer.example.com    ... done
Creating orderer5.example.com   ... done
Creating peer0.org1.example.com ... done
Creating orderer3.example.com   ... done
Creating orderer4.example.com   ... done
Creating peer1.org1.example.com ... done
Creating peer0.org2.example.com ... done
Creating orderer2.example.com   ... done
Creating peer1.org2.example.com ... done
Creating cli                    ... done
```

했을시 엄청나게 많은 로그가 나오는데요 이건 [여기](/blog/fabricnetwork4-log)서 확인할 수 있습니다. 엄청 길어서 따로 포스트 했습니다.

현재 docker 컨테이너의 목록입니다. `orderer`가 5개가 올라가있으면 정확하게 된것입니다.

```
$ docker ps

CONTAINER ID        IMAGE                               COMMAND             CREATED             STATUS              PORTS                      NAMES
b7ec0f79b52c        hyperledger/fabric-tools:latest     "/bin/bash"         15 seconds ago      Up 14 seconds                                  cli
d7e50c6331b3        hyperledger/fabric-orderer:latest   "orderer"           19 seconds ago      Up 17 seconds       0.0.0.0:8050->7050/tcp     orderer2.example.com
69f4e90a56ff        hyperledger/fabric-peer:latest      "peer node start"   20 seconds ago      Up 16 seconds       0.0.0.0:10051->10051/tcp   peer1.org2.example.com
14d53d5f174c        hyperledger/fabric-peer:latest      "peer node start"   20 seconds ago      Up 15 seconds       0.0.0.0:9051->9051/tcp     peer0.org2.example.com
8b8940e514a0        hyperledger/fabric-peer:latest      "peer node start"   20 seconds ago      Up 17 seconds       0.0.0.0:7051->7051/tcp     peer0.org1.example.com
a085431154c1        hyperledger/fabric-peer:latest      "peer node start"   20 seconds ago      Up 17 seconds       0.0.0.0:8051->8051/tcp     peer1.org1.example.com
73bb5a1ae4bb        hyperledger/fabric-orderer:latest   "orderer"           20 seconds ago      Up 17 seconds       0.0.0.0:10050->7050/tcp    orderer4.example.com
3648ca9b41ec        hyperledger/fabric-orderer:latest   "orderer"           20 seconds ago      Up 17 seconds       0.0.0.0:9050->7050/tcp     orderer3.example.com
1354f1e8c27b        hyperledger/fabric-orderer:latest   "orderer"           20 seconds ago      Up 18 seconds       0.0.0.0:11050->7050/tcp    orderer5.example.com
0df26153906b        hyperledger/fabric-orderer:latest   "orderer"           20 seconds ago      Up 16 seconds       0.0.0.0:7050->7050/tcp     orderer.example.com
```


peer 들에게 명령을 내리기전에 `RAFT`의 중요한 특징을 적고 넘어가겠습니다.

바로 5개의 `orderer`들간의 리더선출을 하게됩니다. 그리고 리더가 고장이 났을시서로 통신을 하는데 이때 `HeartBeat`라는 메세지를 보내 체크합니다. 그 후 살아있는 `orderer`들간에 리더선출을 하게 됩니다.

![스크린샷 2019-10-23 오전 5 29 04](https://user-images.githubusercontent.com/44635266/67331709-11bcef80-f559-11e9-929b-080278f343e2.png)

위 사진을 보면 아래 로그 메세지를 통해 현재 리더가 `orderer5.example.com`이란걸 알 수 있습니다.

```
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 027 Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=1
```

한 번 리더를 정지시켜보겠습니다.

리더가 5 -> 0, 0 -> 3 최종적으로 `orderer3.example.com`이 리더가 됐다고 하네요. 사진을 못찍어서 로그를 올려드리겠습니다.

```
2019-10-22 20:44:45.613 UTC [orderer.consensus.etcdraft] Step -> INFO 02c 1 [logterm: 2, index: 6, vote: 5] cast MsgPreVote for 3 [logterm: 2, index: 6] at term 2 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.624 UTC [orderer.consensus.etcdraft] Step -> INFO 02d 1 [term: 2] received a MsgVote message with higher term from 3 [term: 3] channel=byfn-sys-channel node=1
2019-10-22 20:44:45.624 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 02e 1 became follower at term 3 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.624 UTC [orderer.consensus.etcdraft] Step -> INFO 02f 1 [logterm: 2, index: 6, vote: 0] cast MsgVote for 3 [logterm: 2, index: 6] at term 3 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.625 UTC [orderer.consensus.etcdraft] run -> INFO 030 raft.node: 1 lost leader 5 at term 3 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.626 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 031 Raft leader changed: 5 -> 0 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.635 UTC [orderer.consensus.etcdraft] run -> INFO 032 raft.node: 1 elected leader 3 at term 3 channel=byfn-sys-channel node=1
2019-10-22 20:44:45.636 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 033 Raft leader changed: 0 -> 3 channel=byfn-sys-channel node=1
```

그럼 `orderer3.example.com`에서는 무슨일이 벌어졌는지 확인해보겠습니다.

```
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] Step -> INFO 02c 3 is starting a new election at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] becomePreCandidate -> INFO 02d 3 became pre-candidate at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] poll -> INFO 02e 3 received MsgPreVoteResp from 3 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] campaign -> INFO 02f 3 [logterm: 2, index: 6] sent MsgPreVote request to 2 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] campaign -> INFO 030 3 [logterm: 2, index: 6] sent MsgPreVote request to 4 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] campaign -> INFO 031 3 [logterm: 2, index: 6] sent MsgPreVote request to 5 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] campaign -> INFO 032 3 [logterm: 2, index: 6] sent MsgPreVote request to 1 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.605 UTC [orderer.consensus.etcdraft] run -> INFO 033 raft.node: 3 lost leader 5 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.606 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 034 Raft leader changed: 5 -> 0 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.616 UTC [orderer.consensus.etcdraft] poll -> INFO 035 3 received MsgPreVoteResp from 2 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.616 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 036 3 [quorum:3] has received 2 MsgPreVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=3
2019-10-22 20:44:45.619 UTC [orderer.consensus.etcdraft] poll -> INFO 037 3 received MsgPreVoteResp from 1 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.619 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 038 3 [quorum:3] has received 3 MsgPreVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=3
2019-10-22 20:44:45.619 UTC [orderer.consensus.etcdraft] becomeCandidate -> INFO 039 3 became candidate at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.619 UTC [orderer.consensus.etcdraft] poll -> INFO 03a 3 received MsgVoteResp from 3 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.619 UTC [orderer.consensus.etcdraft] campaign -> INFO 03b 3 [logterm: 2, index: 6] sent MsgVote request to 2 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.621 UTC [orderer.consensus.etcdraft] campaign -> INFO 03c 3 [logterm: 2, index: 6] sent MsgVote request to 4 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.621 UTC [orderer.consensus.etcdraft] campaign -> INFO 03d 3 [logterm: 2, index: 6] sent MsgVote request to 5 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.622 UTC [orderer.consensus.etcdraft] campaign -> INFO 03e 3 [logterm: 2, index: 6] sent MsgVote request to 1 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.623 UTC [orderer.consensus.etcdraft] logSendFailure -> ERRO 03f Failed to send StepRequest to 5, because: aborted channel=byfn-sys-channel node=3
2019-10-22 20:44:45.630 UTC [orderer.consensus.etcdraft] poll -> INFO 040 3 received MsgVoteResp from 2 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.631 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 041 3 [quorum:3] has received 2 MsgVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=3
2019-10-22 20:44:45.632 UTC [orderer.consensus.etcdraft] poll -> INFO 042 3 received MsgVoteResp from 1 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.632 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 043 3 [quorum:3] has received 3 MsgVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=3
2019-10-22 20:44:45.632 UTC [orderer.consensus.etcdraft] becomeLeader -> INFO 044 3 became leader at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.632 UTC [orderer.consensus.etcdraft] run -> INFO 045 raft.node: 3 elected leader 3 at term 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.634 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 046 Raft leader changed: 0 -> 3 channel=byfn-sys-channel node=3
2019-10-22 20:44:45.638 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 047 Start accepting requests as Raft leader at block [0] channel=byfn-sys-channel node=3
```

`orderer3.example.com`에서 리더를 선출하는거 같습니다. 제가 여러번 시도해 봤는데 항상 달라졌습니다.

로그를 확인해보면 0번 즉, 어떤 `orderer`도 리더가 아닌 상태로 셋팅합니다. 그 후 각각의 `orderer`로 부터 `MsgPreVoteResp`라는 투표 메세지를 받고 3번 `orderer`로 바뀌는거같습니다. 계속해서 리더를 정지시켜볼게요.

![스크린샷 2019-10-23 오전 5 48 04](https://user-images.githubusercontent.com/44635266/67331710-11bcef80-f559-11e9-8b0b-7c088648f56d.png)

이번엔 `orderer.example.com`이 리더로 선출되었습니다. 계속해서 리더를 정지시켜볼게요.

![스크린샷 2019-10-23 오전 5 49 11](https://user-images.githubusercontent.com/44635266/67331712-11bcef80-f559-11e9-890e-0794a32969cf.png)

3번째 `orderer`를 정지시킨 순간부터 리더 선출을 하지 못하게 되었습니다. `RAFT`도 과반수 이하가 에러가 발생하면 리더 선출이 안됩니다.

그래서 `orderer`하나를 살려봤는데 리더를 정상적으로 선출했습니다.

![스크린샷 2019-10-23 오전 5 49 41](https://user-images.githubusercontent.com/44635266/67331713-11bcef80-f559-11e9-96e8-6407272093e3.png)



`raft`에 대한 특징은 여기까지 하고 `cli` 컨테이너에 들어가서 피어들에게 명령을 주겠습니다.

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

2019-10-22 20:57:30.512 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:57:30.583 UTC [cli.common] readBlock -> INFO 002 Got status: &{NOT_FOUND}
2019-10-22 20:57:30.610 UTC [channelCmd] InitCmdFactory -> INFO 003 Endorser and orderer connections initialized
2019-10-22 20:57:30.812 UTC [cli.common] readBlock -> INFO 004 Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 20:57:30.816 UTC [channelCmd] InitCmdFactory -> INFO 005 Endorser and orderer connections initialized
2019-10-22 20:57:31.018 UTC [cli.common] readBlock -> INFO 006 Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 20:57:31.022 UTC [channelCmd] InitCmdFactory -> INFO 007 Endorser and orderer connections initialized
2019-10-22 20:57:31.223 UTC [cli.common] readBlock -> INFO 008 Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 20:57:31.227 UTC [channelCmd] InitCmdFactory -> INFO 009 Endorser and orderer connections initialized
2019-10-22 20:57:31.430 UTC [cli.common] readBlock -> INFO 00a Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 20:57:31.433 UTC [channelCmd] InitCmdFactory -> INFO 00b Endorser and orderer connections initialized
2019-10-22 20:57:31.634 UTC [cli.common] readBlock -> INFO 00c Got status: &{SERVICE_UNAVAILABLE}
2019-10-22 20:57:31.658 UTC [channelCmd] InitCmdFactory -> INFO 00d Endorser and orderer connections initialized
2019-10-22 20:57:31.860 UTC [cli.common] readBlock -> INFO 00e Received block: 0

$ peer channel join -b mychannel.block

2019-10-22 20:58:29.845 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:58:29.870 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer1.org1.example.com:8051 \
peer channel join -b mychannel.block

2019-10-22 20:58:36.796 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:58:36.822 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 20:58:41.443 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:58:41.464 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 20:58:45.319 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:58:45.347 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
```

### Update Anchor Peer

```
$ peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org1MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 20:58:49.024 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:58:49.035 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update

$ CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org2MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 20:59:16.262 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 20:59:16.273 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
```

> Orderer Log

![스크린샷 2019-10-23 오전 6 00 36](https://user-images.githubusercontent.com/44635266/67332970-be4ba100-f55a-11e9-8559-86c4719c82de.png)

### Install Chaincode

```
$ peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 21:00:43.398 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 21:00:43.398 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 21:00:43.817 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer1.org1.example.com:8051 \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 21:00:55.756 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 21:00:55.756 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 21:00:55.905 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 21:01:06.699 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 21:01:06.699 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 21:01:06.845 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 21:01:15.649 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 21:01:15.649 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 21:01:15.803 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
```

check chaindoe

```
$ peer chaincode list --installed

Name: mycc, Version: 1.0, Path: github.com/chaincode/chaincode_example02/go/, Id: 476fca1a949274001971f1ec2836cb09321f0b71268b3762d68931c93f218134
```

### ChacinCode Instantiate

```
$ peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.peer','Org2MSP.peer')"

2019-10-22 21:01:28.842 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 21:01:28.842 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
```

> Orderer Log

![스크린샷 2019-10-23 오전 6 02 10](https://user-images.githubusercontent.com/44635266/67332960-bb50b080-f55a-11e9-8c5d-4c66e73d8bd8.png)

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

2019-10-22 15:42:00.760 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
```

> Orderer Log

![스크린샷 2019-10-23 오전 6 02 21](https://user-images.githubusercontent.com/44635266/67332972-be4ba100-f55a-11e9-8418-c42cc205b735.png)

### ChainCode Query

```
$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'
90

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","b"]}'
210
```

체인코드까지 정상적으로 작동했습니다. 이 포스트는 여기로 마무리하겠습니다.

읽어주셔서 감사합니다.
