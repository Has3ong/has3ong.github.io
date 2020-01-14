---
title : Hyperledger Network 구성 (EYFN)
tags :
- EYFN
- Hyperledger Fabric
---

# Settings

`Setting` 부분은 [Hyperledger Fabric Network 구성 -1-](/fabricnetwork1) 부분과 동일하니 똑같이 진행하시면 됩니다.

`HandOn` 부분부터 다릅니다.

# HandsOn

## Bring Org3 into the Channel Manually

일단 제일 먼저 기본 네트워크를 구성해줍니다. EYFN 즉 새로운 `org` 를 추가하기 위해서는 기존 네트워크가 만들어진 상태에서 진행해야 하기 때문입니다.

```shell
$ ./byfn.sh generate
$ ./byfn.sh up
```

끝나고 나서 `docker ps` 명령어를 치면 아래와같이 설정이 되어있어야 합니다.

```shell
$ docker ps
CONTAINER ID        IMAGE                                                                                                  COMMAND                  CREATED              STATUS              PORTS                      NAMES
39969b0b38d7        dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab   "chaincode -peer.add…"   50 seconds ago       Up 48 seconds                                  dev-peer1.org2.example.com-mycc-1.0
95358327fe95        dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org1.example.com-mycc-1.0
a3b4300dd49b        dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org2.example.com-mycc-1.0
c20200aa1fbb        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              2 minutes ago        Up 2 minutes                                   cli
ea27dd462838        hyperledger/fabric-peer:latest                                                                         "peer node start"        2 minutes ago        Up 2 minutes        0.0.0.0:8051->8051/tcp     peer1.org1.example.com
a9eb0c75a4ed        hyperledger/fabric-peer:latest                                                                         "peer node start"        2 minutes ago        Up 2 minutes        0.0.0.0:7051->7051/tcp     peer0.org1.example.com
20f02bdc7981        hyperledger/fabric-peer:latest                                                                         "peer node start"        2 minutes ago        Up 2 minutes        0.0.0.0:9051->9051/tcp     peer0.org2.example.com
6e4c68bcfdab        hyperledger/fabric-peer:latest                                                                         "peer node start"        2 minutes ago        Up 2 minutes        0.0.0.0:10051->10051/tcp   peer1.org2.example.com
a67a88110615        hyperledger/fabric-orderer:latest                                                                      "orderer"                2 minutes ago        Up 2 minutes        0.0.0.0:7050->7050/tcp     orderer.example.com
```

## Generate the Org3 Crypto Material

`org3-artifacts` 라는 서브 디렉토리로 들어가줍니다.

```shell
$ cd org3-artifacts
```

디렉토리로 들어가보면 `org3-crypto.yaml` 과 `configtx.yaml` 라는 2개의 yaml 파일이 있습니다. 이 파일을 이용하여 인증서 파일을 만들어줍니다.

```shell
$ ../../bin/cryptogen generate --config=./org3-crypto.yaml
org3.example.com
```

그럼 아래와 같이 `crypto-config` 라는 폴더가 생겨납니다.

```shell
$ ls
configtx.yaml  crypto-config  org3-crypto.yaml
```

이제 `configtxgen` 유틸리티를 사용하여 `Org3` 특정 구성 자료를 JSON으로 출력합니다. 다음 명령을 입력하여 현재 디렉토리에서 수집해야하는 `configtx.yaml` 파일을 찾도록 지시합니다.

```shell
$ export FABRIC_CFG_PATH=$PWD && ../../bin/configtxgen -printOrg Org3MSP > ../channel-artifacts/org3.json
2020-01-06 11:12:53.747 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-06 11:12:53.748 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/org3-artifacts/configtx.yaml
2020-01-06 11:12:53.750 UTC [common.tools.configtxgen.encoder] NewConsortiumOrgGroup -> WARN 003 Default policy emission is deprecated, please include policy specifications for the orderer org group Org3MSP in configtx.yaml
```

위의 명령은 JSON 파일 (`org3.json`)을 작성하여 첫 번째 네트워크의 루트에있는 채널 아티팩트 서브 디렉토리에 출력합니다. 이 파일에는 Org3에 대한 정책 정의와 기본 64 형식으로 제공되는 세 가지 중요한 인증서, 즉 `admin user certificate` (나중에 `Org3` 의 관리자로 작동하는 데 필요함), `CA root cert` 및 ` TLS root cert` 가 포함되어 있습니다. 다음 단계에서는이 JSON 파일을 채널 구성에 추가합니다.

마지막 정리 작업은 `Orderer Org` 의 `MSP` 자료를 `Org3` `crypto-config` 디렉토리로 이식하는 것입니다. 특히, 우리는 `Org3` 엔티티와 네트워크의 `orderering node` 사이의 안전한 통신을 허용하는 Orderer의 TLS 루트 인증서에 관심가져야 합니다.

```shell
$ cd ../ && cp -r crypto-config/ordererOrganizations org3-artifacts/crypto-config/
```

이제 준비단계는 끝났습니다.

## Prepare the CLI Environment 

`cli` 컨테이너로 접속을 합니다.

```shell
$ docker exec -it cli bash
root@c20200aa1fbb:/opt/gopath/src/github.com/hyperledger/fabric/peer#
```

`ORDERER_CA` 와 `CHANNEL_NAME` 변수를 설정합니다.

```shell
$ export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem  && export CHANNEL_NAME=mychannel
```

변수가 정확하게 설정이 되었는지 확인합니다.

```shell
$ echo $ORDERER_CA && echo $CHANNEL_NAME

/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
mychannel
```

## Fetch the Configuration

아래 명령은 바이너리 `protobuf` 채널 구성 블록을 `config_block.pb` 에 저장합니다. 이름과 파일 확장자의 선택은 임의적입니다. 그러나 표시되는 객체 유형과 인코딩 (protobuf 또는 JSON)을 모두 식별하는 규칙을 따르는 것이 좋습니다.

```shell
$ peer channel fetch config config_block.pb -o orderer.example.com:7050 -c $CHANNEL_NAME --tls --cafile $ORDERER_CA

2020-01-06 11:20:09.140 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-06 11:20:09.142 UTC [cli.common] readBlock -> INFO 002 Received block: 4
2020-01-06 11:20:09.144 UTC [cli.common] readBlock -> INFO 003 Received block: 2
2020-01-06 11:20:09.144 UTC [channelCmd] fetch -> INFO 004 Retrieving last config block: 2
```

이것은 `mychannel` 에 대한 가장 최신 구성 블록이 실제로 블록 2가 아니라 생성 블록이라는 것을 알려줍니다. 기본적으로 `peer channel fetch config` 명령은 대상 채널에 대한 최신 구성 블록 (이 경우 세 번째 블록)을 반환합니다. BYFN 스크립트가 두 조직 (`Org1` 및 `Org2`)의 앵커 피어를 두 개의 개별 채널 업데이트 트랜잭션에 정의했기 때문입니다.

결과적으로 다음과 같은 구성 순서가 있습니다.

* block 0: genesis block
* block 1: Org1 anchor peer update
* block 2: Org2 anchor peer update

## Convert the Configuration to JSON and Trim It Down

이제 `configtxlator` 도구를 사용하여이 채널 구성 블록을 JSON 형식 (인간이 읽고 수정할 수 있음)으로 디코딩합니다. 또한 변경하려는 내용과 관련이없는 모든 헤더, 메타 데이터, 제작자 서명 등을 제거해야합니다. `jq` 도구를 사용하여이를 수행합니다.

```shell
$ configtxlator proto_decode --input config_block.pb --type common.Block | jq .data.data[0].payload.data.config > config.json
```

이로 인해 첫 번째 네트워크 내의 `fabric-samples` 폴더에있는 정리 된 JSON 객체 인 `config.json` 이 구성 업데이트의 기준으로 사용됩니다.

## Add the Org3 Crypto Material

`jq` 도구를 한 번 더 사용하여 Org3 구성 정의 (org3.json)를 채널의 애플리케이션 그룹 필드에 추가하고 출력 이름을 `modified_config.json` 으로 지정합니다.

```shell
$ jq -s '.[0] * {"channel_group":{"groups":{"Application":{"groups": {"Org3MSP":.[1]}}}}}' config.json ./channel-artifacts/org3.json > modified_config.json
```

이제 `CLI` 컨테이너 내에 `config.json` 과 `modified_config.json` 이라는 두 개의 JSON 파일이 있습니다. 초기 파일에는 `Org1` 및 `Org2` 만 포함되어 있으며 수정 된 파일에는 3 개의 조직이 모두 포함되어 있습니다. 이 시점에서 두 JSON 파일을 다시 인코딩하고 델타를 계산하면됩니다.

먼저 `config.json` 을 `config.pb` 라는 프로토 타입으로 다시 변환하십시오.

```shell
$ configtxlator proto_encode --input config.json --type common.Config --output config.pb
```

그런 다음 `modified_config.json` 을 `modified_config.pb` 로 인코딩하십시오.

```shell
$ configtxlator proto_encode --input modified_config.json --type common.Config --output modified_config.pb
```

이제 `configtxlator` 를 사용하여이 두 구성 프로토 타입 간의 델타를 계산하십시오. 이 명령은 `org3_update.pb` 라는 새 프로토 타입 바이너리를 출력합니다.

```shell
$ configtxlator compute_update --channel_id $CHANNEL_NAME --original config.pb --updated modified_config.pb --output org3_update.pb
```

이 새로운 프로토 타입 인 `org3_update.pb` 에는 Org3 정의와 Org1 및 Org2 에 대한 고급 포인터가 포함되어 있습니다. Org1 및 Org2에 대한 광범위한 MSP 자료 및 수정 정책 정보는 채널의 생성 블록 내에 이미 존재하므로이를 무시할 수 있습니다. 따라서 두 구성 사이의 델타 만 필요합니다.

채널 업데이트를 제출하기 전에 몇 가지 최종 단계를 수행해야합니다. 먼저이 객체를 편집 가능한 JSON 형식으로 디코딩하여 `org3_update.json` 이라고합니다.

```shell
$ configtxlator proto_decode --input org3_update.pb --type common.ConfigUpdate | jq . > org3_update.json
```

이제 봉투 메시지로 감싸 야하는 디코딩 된 업데이트 파일 `(org3_update.json)` 이 있습니다. 이 단계는 이전에 제거했던 헤더 필드를 다시 제공합니다. 이 파일 이름을 `org3_update_in_envelope.json` 으로 지정합니다.

```shell
$ echo '{"payload":{"header":{"channel_header":{"channel_id":"'$CHANNEL_NAME'", "type":2}},"data":{"config_update":'$(cat org3_update.json)'}}}' | jq . > org3_update_in_envelope.json
```

올바르게 구성된 `JSON (org3_update_in_envelope.json)` 을 사용하여 마지막으로 `configtxlator` 도구를 활용하여 `Fabric` 에 필요한 본격적인 프로토 타입 형식으로 변환합니다. 최종 업데이트 개체 이름을 `org3_update_in_envelope.pb` 로 지정합니다.

```shell
$ configtxlator proto_encode --input org3_update_in_envelope.json --type common.Envelope --output org3_update_in_envelope.pb
```

처음 파일 디렉토리는 아래처럼 변경이 됩니다.

```shell
$ ls
channel-artifacts  config_block.pb  crypto  log.txt  mychannel.block scripts

$ ls
channel-artifacts  config.pb        crypto   modified_config.json  mychannel.block   org3_update.pb               org3_update_in_envelope.pb
config.json        config_block.pb  log.txt  modified_config.pb    org3_update.json  org3_update_in_envelope.json  scripts
```

## Sign and Submit the Config Update



```shell
$ peer channel signconfigtx -f org3_update_in_envelope.pb

2020-01-06 11:22:13.217 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
```

마지막으로 `peer channel update` 명령을 실행합니다. `Org2 Admin` 서명이 호출에 첨부되므로 두 번째로 프로토 타입에 수동으로 서명 할 필요가 없습니다.

```shell
$ peer channel update -f org3_update_in_envelope.pb -c $CHANNEL_NAME -o orderer.example.com:7050 --tls --cafile $ORDERER_CA

2020-01-06 11:22:52.420 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-06 11:22:52.440 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
```

## Join Org3 to the Channel

이 시점에서 새로운 조직인 `Org3` 을 포함하도록 채널 구성이 업데이트되었습니다. 즉, 조직에 연결된 피어가 이제 내 채널에 참여할 수 있습니다.

먼저 `Org3` 피어 및 `Org3` 관련 CLI에 대한 컨테이너를 시작하겠습니다.

```shell
$ docker-compose -f docker-compose-org3.yaml up -d

Creating volume "net_peer0.org3.example.com" with default driver
Creating volume "net_peer1.org3.example.com" with default driver
WARNING: Found orphan containers (cli, peer1.org1.example.com, peer0.org1.example.com, peer0.org2.example.com, peer1.org2.example.com, orderer.example.com) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Creating peer0.org3.example.com ... done
Creating peer1.org3.example.com ... done
Creating Org3cli                ... done
```

`docker ps` 명령어를 치면 아래와같이 설정이 되어있어야 합니다.

```shell
$ docker ps
CONTAINER ID        IMAGE                                                                                                  COMMAND                  CREATED             STATUS              PORTS                      NAMES
08a94fe84b9c        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              3 seconds ago       Up 2 seconds                                   Org3cli
939f8ec6075f        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 seconds ago       Up 2 seconds        0.0.0.0:12051->12051/tcp   peer1.org3.example.com
22ad29d58ae6        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 seconds ago       Up 2 seconds        0.0.0.0:11051->11051/tcp   peer0.org3.example.com
39969b0b38d7        dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab   "chaincode -peer.add…"   17 minutes ago      Up 17 minutes                                  dev-peer1.org2.example.com-mycc-1.0
95358327fe95        dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9   "chaincode -peer.add…"   18 minutes ago      Up 18 minutes                                  dev-peer0.org1.example.com-mycc-1.0
a3b4300dd49b        dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b   "chaincode -peer.add…"   18 minutes ago      Up 18 minutes                                  dev-peer0.org2.example.com-mycc-1.0
c20200aa1fbb        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              19 minutes ago      Up 19 minutes                                  cli
ea27dd462838        hyperledger/fabric-peer:latest                                                                         "peer node start"        19 minutes ago      Up 19 minutes       0.0.0.0:8051->8051/tcp     peer1.org1.example.com
a9eb0c75a4ed        hyperledger/fabric-peer:latest                                                                         "peer node start"        19 minutes ago      Up 19 minutes       0.0.0.0:7051->7051/tcp     peer0.org1.example.com
20f02bdc7981        hyperledger/fabric-peer:latest                                                                         "peer node start"        19 minutes ago      Up 19 minutes       0.0.0.0:9051->9051/tcp     peer0.org2.example.com
6e4c68bcfdab        hyperledger/fabric-peer:latest                                                                         "peer node start"        19 minutes ago      Up 19 minutes       0.0.0.0:10051->10051/tcp   peer1.org2.example.com
a67a88110615        hyperledger/fabric-orderer:latest                                                                      "orderer"                19 minutes ago      Up 19 minutes       0.0.0.0:7050->7050/tcp     orderer.example.com
```

## Setting Environments Variables

먼저 `Org3cli` 컨테이너로 접속을 합니다. 아래 명령어는 2번 더 사용할 예정입니다.

```shell
$ docker exec -it Org3cli /bin/bash
```

다음으로 먼저 환경변수 설정을 하겠습니다.

```shell
CHANNEL_NAME=mychannel
CLI_DELAY=3
LANGUAGE=golang
CLI_TIMEOUT=10
VERBOSE=false
ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
CC_SRC_PATH="github.com/chaincode/chaincode_example02/go/"
VERSION=2.0
```

## Fetch & Join Channel

```shell
$ peer channel fetch 0 $CHANNEL_NAME.block -o orderer.example.com:7050 -c $CHANNEL_NAME --tls --cafile $ORDERER_CA

2020-01-07 13:34:36.159 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-07 13:34:36.162 UTC [cli.common] readBlock -> INFO 002 Received block: 0
```

**peer0.org3**

```shell
PEER0_ORG3_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org3MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG3_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp
CORE_PEER_ADDRESS=peer0.org3.example.com:11051

$ peer channel join -b $CHANNEL_NAME.block

2020-01-07 13:36:36.686 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-07 13:36:36.706 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
```

**peer1.org3**

```shell
export CORE_PEER_ADDRESS=peer1.org3.example.com:12051

$ peer channel join -b $CHANNEL_NAME.block

2020-01-07 13:37:31.067 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-07 13:37:31.088 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
```

## Install Chaincode

**peer0.org3**

```shell
CORE_PEER_ADDRESS=peer0.org3.example.com:11051 

$ peer chaincode install -n mycc -v ${VERSION} -l ${LANGUAGE} -p ${CC_SRC_PATH}

2020-01-07 13:40:35.753 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-07 13:40:35.754 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-07 13:40:35.877 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
```

여기서 `Org3cli` 컨테이너를 나간 뒤 `cli` 컨테이너로 접속합니다.

```shell
$ docker exec -it cli /bin/bash
```

다음 **Setting Environments Variables** 설정한 환경변수를 다시 설정해줍니다.

**peer0.org1**

```shell
PEER0_ORG1_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org1MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG1_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
CORE_PEER_ADDRESS=peer0.org1.example.com:7051

$ peer chaincode install -n mycc -v ${VERSION} -l ${LANGUAGE} -p ${CC_SRC_PATH}

2020-01-07 13:55:38.492 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-07 13:55:38.493 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-07 13:55:38.609 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
```

**peer0.org2**

```shell
PEER0_ORG2_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org2MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG2_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
CORE_PEER_ADDRESS=peer0.org2.example.com:9051

$ peer chaincode install -n mycc -v ${VERSION} -l ${LANGUAGE} -p ${CC_SRC_PATH}

2020-01-07 13:57:06.527 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-07 13:57:06.528 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-07 13:57:06.649 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
```

## Upgrade Chaincode

**peer0.org1**

```shell
PEER0_ORG1_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org1MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG1_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
CORE_PEER_ADDRESS=peer0.org1.example.com:7051

$ peer chaincode upgrade -o orderer.example.com:7050 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc -v 2.0 -c '{"Args":["init","a","90","b","210"]}' -P "AND ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

2020-01-07 14:00:30.299 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-07 14:00:30.300 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
```

여기서 `cli` 컨테이너를 나간 뒤 `Org3cli` 컨테이너로 접속합니다.

```shell
$ docker exec -it Org3cli /bin/bash
```

마찬가지로 **Setting Environments Variables** 설정한 환경변수를 다시 설정해줍니다.

## Invoke, Query

**peer0.org3 Query**

```shell
PEER0_ORG3_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org3MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG3_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp
CORE_PEER_ADDRESS=peer0.org3.example.com:11051

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'

90
```

**Invoke**

```shell
peer chaincode invoke -o orderer.example.com:7050 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc $PEER_CONN_PARMS -c '{"Args":["invoke","a","b","10"]}'

2020-01-07 14:09:08.245 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
```

**peer0.org3 Query**

```shell
PEER0_ORG3_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org3MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG3_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp
CORE_PEER_ADDRESS=peer0.org3.example.com:11051

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'

80
```

**peer0.org2 Query**

```shell
PEER0_ORG2_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org2MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG2_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
CORE_PEER_ADDRESS=peer0.org2.example.com:9051

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'

80
```

**peer0.org1 Query**

```shell
PEER0_ORG1_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
CORE_PEER_LOCALMSPID="Org1MSP"
CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG1_CA
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
CORE_PEER_ADDRESS=peer0.org1.example.com:7051

$ peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'

80
```

이렇게 까지 확인하면 끝났습니다.

이 포스트는 `./eyfn.sh generate` 와 `./eyfn.sh up` 까지의 과정입니다. `peer` 를 추가하고 `chaincode` 를 업데이트 하는 부분은 다른 포스트에서도 확인하고 많이 해봤기 때문에 설명은 적게하고 `generate` 부분을 많이 추가하도록 노력했습니다.

감사합니다.