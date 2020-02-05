---
title : Hyperledger Network 구성 (BYFN)
tags :
- BYFN
- Hyperledger Fabric
- BlockChain
---

## Network 구성

크게 2가지로 나눠서 해보겠습니다.

첫 번째로는 Hyperledger 에서 제공하는 `byfn.sh` 파일을 이용하여 간단하고 빠르게 네트워크를 구성하는 방법을 이용할것입니다.

두 번째로는 hyperledger 에서 제공하는 `binary` 파일들을 이용하여 천천히 하나하나 명령어를 설명하면서 진행하겠습니다.

현 포스트는 두 번째 방법을 이용하여 네트워크를 구성해보겠습니다.

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

`bin`, `base`, `chaincode`, `configtx.yaml`, `crypto-config.yaml`, `docker-compose-cli.yaml` 입니다.

```
$ sudo cp -r ../fabric-samples/bin .
$ sudo cp -r ../fabric-samples/first-network/base .
$ sudo cp -r ../fabric-samples/first-network/configtx.yaml .
$ sudo cp -r ../fabric-samples/first-network/crypto-config.yaml .
$ sudo cp -r ../fabric-samples/first-network/docker-compose-cli.yaml .
$ sudo cp -r ../fabric-samples/chaincode .
$ mkdir channel-artifacts
```

파일을 다 옮기고 나면 현재와 같은 상태가 만들어집니다.
```
$ ls

base  bin  channel-artifacts  configtx.yaml  crypto-config.yaml  docker-compose-cli.yaml
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

그다음 우리가 사용할 Fabric 네트워크에 `profile` 즉, orderer type(?) 을 설정합니다. `fabric-samples` 에서 제공하는 종류로는 `Solo`, `RAFT`, `Kafka` 3가지가 있는데 지금은 `Solo`로 사용하겠습니다.

`RAFT`, `Kafka`는 추후에 포스트로 올려드리겠습니다.

Solo

```
$ ./bin/configtxgen -profile TwoOrgsOrdererGenesis -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block

2019-10-22 14:55:14.818 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 14:55:14.886 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 002 orderer type: solo
2019-10-22 14:55:14.886 UTC [common.tools.configtxgen.localconfig] Load -> INFO 003 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:55:14.947 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 004 orderer type: solo
2019-10-22 14:55:14.947 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 005 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:55:14.949 UTC [common.tools.configtxgen] doOutputBlock -> INFO 006 Generating genesis block
2019-10-22 14:55:14.949 UTC [common.tools.configtxgen] doOutputBlock -> INFO 007 Writing genesis block
```

RAFT

```
$ ./bin/configtxgen -profile SampleMultiNodeEtcdRaft -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
```

Kafka

```
$ ../bin/configtxgen -profile SampleDevModeKafka -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
```

### Create a Channel Configuration Transaction

`channel.tx`파일을 만들어 주어야 합니다. `channel.tx`에는 현재 우리가 구현할 채널의 정책이나 조직의 정보가 담겨져 있다고 생각하면 됩니다.

그리고, 각각의 Org에 올라갈 `AnchorPeer`를 설정합니다. 이 모두에 대한 정보는 `configtx.yaml`에서 확인할 수 있습니다.

```
$ export CHANNEL_NAME=mychannel  && ../bin/configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME


$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP

2019-10-22 14:56:00.846 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 14:56:00.913 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:56:00.981 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-22 14:56:00.981 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:56:00.981 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 14:56:00.982 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update


$ ./bin/configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org2MSP

2019-10-22 14:56:14.326 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-22 14:56:14.399 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:56:14.467 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-22 14:56:14.467 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/has3ong/configtx.yaml
2019-10-22 14:56:14.467 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-22 14:56:14.468 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
```

여기 까지의 과정이 `byfn.sh`에서의 `generate`입니다.

### Start the network

이제 초기 설정은 끝났으니 네트워크를 시작해보겠습니다. `docker-compose-cli.yaml` 파일을 이용하여 도커 위에 올려줍니다.

마지막 -d 파라메터를 넣어주면 컨테이너의 로그가 안뜨고 백그라운드로 진행이 됩니다. 저는 `orderer`, `peer`들의 로그도 같이 보면서 진행할 예정이니 빼서 진행하겠습니다.

```
$ export IMAGE_TAG="latest"
$ export SYS_CHANNEL="byfn-sys-channel"
$ export COMPOSE_PROJECT_NAME=fabric

docker-compose -f docker-compose-cli.yaml up -d
```

했을시 엄청나게 많은 로그가 나오는데요 이건 [여기](/blog/fabricnetwork2-log)서 확인할 수 있습니다. 엄청 길어서 따로 포스트 했습니다.

현재 docker 컨테이너의 목록입니다.

```
$ docker ps

CONTAINER ID        IMAGE                               COMMAND             CREATED             STATUS              PORTS                      NAMES
d20b921e8191        hyperledger/fabric-tools:latest     "/bin/bash"         3 minutes ago       Up 3 minutes                                   cli
bda1f2020634        hyperledger/fabric-peer:latest      "peer node start"   3 minutes ago       Up 3 minutes        0.0.0.0:8051->8051/tcp     peer1.org1.example.com
ac07375045df        hyperledger/fabric-peer:latest      "peer node start"   3 minutes ago       Up 3 minutes        0.0.0.0:9051->9051/tcp     peer0.org2.example.com
8afba007e165        hyperledger/fabric-orderer:latest   "orderer"           3 minutes ago       Up 3 minutes        0.0.0.0:7050->7050/tcp     orderer.example.com
8a2d65f884c2        hyperledger/fabric-peer:latest      "peer node start"   3 minutes ago       Up 3 minutes        0.0.0.0:7051->7051/tcp     peer0.org1.example.com
f8e2fcb418da        hyperledger/fabric-peer:latest      "peer node start"   3 minutes ago       Up 3 minutes        0.0.0.0:10051->10051/tcp   peer1.org2.example.com
```

그리고 `cli` 컨테이너에 들어가서 피어들에게 명령을 주겠습니다.

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

$ export CHANNEL_NAME=mychannel
$ export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

$ peer channel create -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/channel.tx --tls --cafile $ORDERER_CA

2019-10-22 15:16:52.883 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:16:52.910 UTC [cli.common] readBlock -> INFO 002 Received block: 0

$ peer channel join -b mychannel.block
2019-10-22 15:19:26.532 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:19:26.563 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer1.org1.example.com:8051 \
peer channel join -b mychannel.block

2019-10-22 15:20:30.652 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:20:30.686 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 15:20:44.601 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:20:44.634 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer channel join -b mychannel.block

2019-10-22 15:20:51.191 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:20:51.226 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
```

### Update Anchor Peer

```
$ peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org1MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 15:22:16.890 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:22:16.907 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update

$ CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_ADDRESS=peer0.org2.example.com:9051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/Org2MSPanchors.tx --tls --cafile $ORDERER_CA

2019-10-22 15:23:02.809 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-22 15:23:02.827 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
```

### Install Chaincode

```
$ peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 15:37:12.709 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 15:37:12.710 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 15:37:13.000 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

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

2019-10-22 15:37:30.491 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 15:37:30.491 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 15:37:30.618 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >

$ CORE_PEER_ADDRESS=peer1.org2.example.com:10051 \
CORE_PEER_LOCALMSPID="Org2MSP" \
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp \
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer1.org2.example.com/tls/ca.crt \
peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

2019-10-22 15:37:36.945 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 15:37:36.946 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-22 15:37:37.079 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
```

check chaindoe

```
$ peer chaincode list --installed

Name: mycc, Version: 1.0, Path: github.com/chaincode/chaincode_example02/go/, Id: 476fca1a949274001971f1ec2836cb09321f0b71268b3762d68931c93f218134
```

### ChacinCode Instantiate

```
$ peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.peer','Org2MSP.peer')"

2019-10-22 15:40:33.013 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-22 15:40:33.014 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
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

2019-10-22 15:42:00.760 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
```

### ChainCode Query

```
$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'
90

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","b"]}'
210
```

체인코드까지 정상적으로 작동했습니다. 이 포스트는 여기로 마무리하고 다음엔 kafka를 이용한 하이퍼렛져 페브릭 네트워크 구성으로 찾아뵙겠습니다.

읽어주셔서 감사합니다.

> 끝난 모습

![](https://user-images.githubusercontent.com/44635266/67305066-c215fe00-f52f-11e9-8a7f-3b93cdc4f478.png)

