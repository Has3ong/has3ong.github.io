---
title : Hyperledger Network 구성 (EYFN)
tags :
- EYFN
- Hyperledger Fabric
---

## Network 구성

# Settings

`Setting` 부분은 [Hyperledger Fabric Network 구성 -1-](/fabricnetwork1) 부분과 동일하니 똑같이 진행하시면 됩니다.

`HandOn` 부분부터 다릅니다.

# HandsOn

## Generate Network Artifacts

먼저 BYFN 파일을 이용하여 초기 네트워크 설정을 합니다.

```shell
$ cd fabric-samples/first-network
$ ./byfn.sh generate

Generating certs and genesis block for channel 'mychannel' with CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
proceeding ...
/home/vagrant/fabric-samples/first-network/../bin/cryptogen

##########################################################
##### Generate certificates using cryptogen tool #########
##########################################################
+ cryptogen generate --config=./crypto-config.yaml
org1.example.com
org2.example.com
+ res=0
+ set +x

Generate CCP files for Org1 and Org2
/home/vagrant/fabric-samples/first-network/../bin/configtxgen
##########################################################
#########  Generating Orderer Genesis block ##############
##########################################################
CONSENSUS_TYPE=solo
+ '[' solo == solo ']'
+ configtxgen -profile TwoOrgsOrdererGenesis -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
2020-01-05 11:59:40.507 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-05 11:59:40.574 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 002 orderer type: solo
2020-01-05 11:59:40.574 UTC [common.tools.configtxgen.localconfig] Load -> INFO 003 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.638 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 004 orderer type: solo
2020-01-05 11:59:40.639 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 005 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.640 UTC [common.tools.configtxgen] doOutputBlock -> INFO 006 Generating genesis block
2020-01-05 11:59:40.641 UTC [common.tools.configtxgen] doOutputBlock -> INFO 007 Writing genesis block
+ res=0
+ set +x

#################################################################
### Generating channel configuration transaction 'channel.tx' ###
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID mychannel
2020-01-05 11:59:40.663 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-05 11:59:40.718 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.773 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2020-01-05 11:59:40.774 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.774 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 005 Generating new channel configtx
2020-01-05 11:59:40.776 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 006 Writing new channel tx
+ res=0
+ set +x

#################################################################
#######    Generating anchor peer update for Org1MSP   ##########
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID mychannel -asOrg Org1MSP
2020-01-05 11:59:40.799 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-05 11:59:40.855 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.914 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2020-01-05 11:59:40.915 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:40.916 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2020-01-05 11:59:40.916 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
+ res=0
+ set +x

#################################################################
#######    Generating anchor peer update for Org2MSP   ##########
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID mychannel -asOrg Org2MSP
2020-01-05 11:59:40.954 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-05 11:59:41.028 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:41.108 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2020-01-05 11:59:41.108 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2020-01-05 11:59:41.109 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2020-01-05 11:59:41.110 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
+ res=0
+ set +x
```

## Bring Up the Network

다음으로 네트워크를 구성하겠습니다. `./byfn.sh up` 명령어로 네트워크를 실행 시킵니다. 

```shell
$ ./byfn.sh up

Starting for channel 'mychannel' with CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
proceeding ...
LOCAL_VERSION=1.4.3
DOCKER_IMAGE_VERSION=1.4.3
Creating network "net_byfn" with the default driver
Creating volume "net_orderer.example.com" with default driver
Creating volume "net_peer0.org1.example.com" with default driver
Creating volume "net_peer1.org1.example.com" with default driver
Creating volume "net_peer0.org2.example.com" with default driver
Creating volume "net_peer1.org2.example.com" with default driver
Creating peer1.org1.example.com ... done
Creating orderer.example.com    ... done
Creating peer1.org2.example.com ... done
Creating peer0.org1.example.com ... done
Creating peer0.org2.example.com ... done
Creating cli                    ... done
CONTAINER ID        IMAGE                               COMMAND             CREATED             STATUS                  PORTS                      NAMES
8a0d121e21c0        hyperledger/fabric-tools:latest     "/bin/bash"         1 second ago        Up Less than a second                              cli
0548c53e2464        hyperledger/fabric-peer:latest      "peer node start"   3 seconds ago       Up Less than a second   0.0.0.0:9051->9051/tcp     peer0.org2.example.com
a176d7245611        hyperledger/fabric-peer:latest      "peer node start"   3 seconds ago       Up 1 second             0.0.0.0:7051->7051/tcp     peer0.org1.example.com
af300dab906d        hyperledger/fabric-peer:latest      "peer node start"   3 seconds ago       Up 1 second             0.0.0.0:10051->10051/tcp   peer1.org2.example.com
0f7fbfe0c0f0        hyperledger/fabric-orderer:latest   "orderer"           3 seconds ago       Up 1 second             0.0.0.0:7050->7050/tcp     orderer.example.com
90d452410ac7        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago       Up Less than a second   0.0.0.0:8051->8051/tcp     peer1.org1.example.com

 ____    _____      _      ____    _____
/ ___|  |_   _|    / \    |  _ \  |_   _|
\___ \    | |     / _ \   | |_) |   | |
 ___) |   | |    / ___ \  |  _ <    | |
|____/    |_|   /_/   \_\ |_| \_\   |_|

Build your first network (BYFN) end-to-end test

Channel name : mychannel
Creating channel...
+ peer channel create -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
+ res=0
+ set +x
2020-01-05 11:59:51.318 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 11:59:51.345 UTC [cli.common] readBlock -> INFO 002 Received block: 0
===================== Channel 'mychannel' created =====================

Having all peers join the channel...
+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 11:59:51.396 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 11:59:51.414 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer0.org1 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 11:59:54.470 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 11:59:54.492 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer1.org1 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 11:59:57.542 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 11:59:57.560 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer0.org2 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 12:00:00.612 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:00:00.632 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer1.org2 joined channel 'mychannel' =====================

Updating anchor peers for org1...
+ peer channel update -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/Org1MSPanchors.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
+ res=0
+ set +x
2020-01-05 12:00:03.686 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:00:03.716 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
===================== Anchor peers updated for org 'Org1MSP' on channel 'mychannel' =====================

Updating anchor peers for org2...
+ peer channel update -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/Org2MSPanchors.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
+ res=0
+ set +x
2020-01-05 12:00:06.771 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:00:06.786 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
===================== Anchor peers updated for org 'Org2MSP' on channel 'mychannel' =====================

Installing chaincode on peer0.org1...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2020-01-05 12:00:09.839 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:00:09.839 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:00:10.176 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org1 =====================

Install chaincode on peer0.org2...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2020-01-05 12:00:10.220 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:00:10.220 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:00:10.352 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org2 =====================

Instantiating chaincode on peer0.org2...
+ peer chaincode instantiate -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc -l golang -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P 'AND ('\''Org1MSP.peer'\'','\''Org2MSP.peer'\'')'
+ res=0
+ set +x
2020-01-05 12:00:10.398 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:00:10.399 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
===================== Chaincode is instantiated on peer0.org2 on channel 'mychannel' =====================

Querying chaincode on peer0.org1...
===================== Querying on peer0.org1 on channel 'mychannel'... =====================
Attempting to Query peer0.org1 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

100
===================== Query successful on peer0.org1 on channel 'mychannel' =====================
Sending invoke transaction on peer0.org1 peer0.org2...
+ peer chaincode invoke -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"Args":["invoke","a","b","10"]}'
+ res=0
+ set +x
2020-01-05 12:00:54.147 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
===================== Invoke transaction successful on peer0.org1 peer0.org2 on channel 'mychannel' =====================

Installing chaincode on peer1.org2...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2020-01-05 12:00:54.202 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:00:54.202 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:00:54.322 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer1.org2 =====================

Querying chaincode on peer1.org2...
===================== Querying on peer1.org2 on channel 'mychannel'... =====================
Attempting to Query peer1.org2 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

90
===================== Query successful on peer1.org2 on channel 'mychannel' =====================

========= All GOOD, BYFN execution completed ===========


 _____   _   _   ____
| ____| | \ | | |  _ \
|  _|   |  \| | | | | |
| |___  | |\  | | |_| |
|_____| |_| \_| |____/
```

네트워크 구성이 끝나면 `docker ps` 명령어를 쳤을때 현재 컨테이너의 상태가 아래와 같습니다.

```shell
$ docker ps
CONTAINER ID        IMAGE                                                                                                  COMMAND                  CREATED              STATUS              PORTS                      NAMES
d935b4c05e80        dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab   "chaincode -peer.add…"   29 seconds ago       Up 27 seconds                                  dev-peer1.org2.example.com-mycc-1.0
a406944b01ec        dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9   "chaincode -peer.add…"   49 seconds ago       Up 47 seconds                                  dev-peer0.org1.example.com-mycc-1.0
d12628a39c8b        dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org2.example.com-mycc-1.0
8a0d121e21c0        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              About a minute ago   Up About a minute                              cli
0548c53e2464        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:9051->9051/tcp     peer0.org2.example.com
a176d7245611        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:7051->7051/tcp     peer0.org1.example.com
af300dab906d        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:10051->10051/tcp   peer1.org2.example.com
0f7fbfe0c0f0        hyperledger/fabric-orderer:latest                                                                      "orderer"                About a minute ago   Up About a minute   0.0.0.0:7050->7050/tcp     orderer.example.com
90d452410ac7        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:8051->8051/tcp     peer1.org1.example.com
```

## Adding an Org to a Channel

`./eyfn.sh up` 명렁어를 통해서 새로운 org3 를 추가해보겠습니다.

```shell
$ ./eyfn.sh up

Generating certs and genesis block for with channel 'mychannel' and CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
proceeding ...
/home/vagrant/fabric-samples/first-network/../bin/cryptogen

###############################################################
##### Generate Org3 certificates using cryptogen tool #########
###############################################################
+ cryptogen generate --config=./org3-crypto.yaml
org3.example.com
+ res=0
+ set +x

/home/vagrant/fabric-samples/first-network/../bin/configtxgen
##########################################################
#########  Generating Org3 config material ###############
##########################################################
+ configtxgen -printOrg Org3MSP
2020-01-05 12:01:49.176 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2020-01-05 12:01:49.178 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/org3-artifacts/configtx.yaml
2020-01-05 12:01:49.179 UTC [common.tools.configtxgen.encoder] NewConsortiumOrgGroup -> WARN 003 Default policy emission is deprecated, please include policy specifications for the orderer org group Org3MSP in configtx.yaml
+ res=0
+ set +x


###############################################################
####### Generate and submit config tx to add Org3 #############
###############################################################

========= Creating config transaction to add org3 to network ===========

Installing jq
Hit:1 http://archive.ubuntu.com/ubuntu xenial InRelease
Get:2 http://security.ubuntu.com/ubuntu xenial-security InRelease [109 kB]
Get:3 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [109 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-backports InRelease [107 kB]
Get:5 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [1019 kB]
Get:6 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [1396 kB]
Get:7 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [593 kB]
Get:8 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [6280 B]
Get:9 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [996 kB]
Get:10 http://archive.ubuntu.com/ubuntu xenial-updates/multiverse amd64 Packages [19.3 kB]
Fetched 4355 kB in 8s (496 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
jq is already the newest version (1.5+dfsg-1ubuntu0.1).
0 upgraded, 0 newly installed, 0 to remove and 103 not upgraded.
Fetching the most recent configuration block for the channel
+ peer channel fetch config config_block.pb -o orderer.example.com:7050 -c mychannel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
2020-01-05 12:02:00.119 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:02:00.121 UTC [cli.common] readBlock -> INFO 002 Received block: 4
2020-01-05 12:02:00.125 UTC [cli.common] readBlock -> INFO 003 Received block: 2
2020-01-05 12:02:00.126 UTC [channelCmd] fetch -> INFO 004 Retrieving last config block: 2
+ set +x
Decoding config block to JSON and isolating config to config.json
+ jq '.data.data[0].payload.data.config'
+ configtxlator proto_decode --input config_block.pb --type common.Block
+ set +x
+ jq -s '.[0] * {"channel_group":{"groups":{"Application":{"groups": {"Org3MSP":.[1]}}}}}' config.json ./channel-artifacts/org3.json
+ set +x
+ configtxlator proto_encode --input config.json --type common.Config
+ configtxlator proto_encode --input modified_config.json --type common.Config
+ configtxlator compute_update --channel_id mychannel --original original_config.pb --updated modified_config.pb
+ configtxlator proto_decode --input config_update.pb --type common.ConfigUpdate
+ jq .
++ cat config_update.json
+ echo '{"payload":{"header":{"channel_header":{"channel_id":"mychannel", "type":2}},"data":{"config_update":{' '"channel_id":' '"mychannel",' '"isolated_data":' '{},' '"read_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org1MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"1"' '},' '"Org2MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"1"' '}' '},' '"mod_policy":' '"",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"Capabilities":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"1"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '},' '"write_set":' '{' '"groups":' '{' '"Application":' '{' '"groups":' '{' '"Org1MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"1"' '},' '"Org2MSP":' '{' '"groups":' '{},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"1"' '},' '"Org3MSP":' '{' '"groups":' '{},' '"mod_policy":' '"Admins",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"Admins",' '"policy":' '{' '"type":' 1, '"value":' '{' '"identities":' '[' '{' '"principal":' '{' '"msp_identifier":' '"Org3MSP",' '"role":' '"ADMIN"' '},' '"principal_classification":' '"ROLE"' '}' '],' '"rule":' '{' '"n_out_of":' '{' '"n":' 1, '"rules":' '[' '{' '"signed_by":' 0 '}' ']' '}' '},' '"version":' 0 '}' '},' '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"Admins",' '"policy":' '{' '"type":' 1, '"value":' '{' '"identities":' '[' '{' '"principal":' '{' '"msp_identifier":' '"Org3MSP",' '"role":' '"MEMBER"' '},' '"principal_classification":' '"ROLE"' '}' '],' '"rule":' '{' '"n_out_of":' '{' '"n":' 1, '"rules":' '[' '{' '"signed_by":' 0 '}' ']' '}' '},' '"version":' 0 '}' '},' '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"Admins",' '"policy":' '{' '"type":' 1, '"value":' '{' '"identities":' '[' '{' '"principal":' '{' '"msp_identifier":' '"Org3MSP",' '"role":' '"MEMBER"' '},' '"principal_classification":' '"ROLE"' '}' '],' '"rule":' '{' '"n_out_of":' '{' '"n":' 1, '"rules":' '[' '{' '"signed_by":' 0 '}' ']' '}' '},' '"version":' 0 '}' '},' '"version":' '"0"' '}' '},' '"values":' '{' '"MSP":' '{' '"mod_policy":' '"Admins",' '"value":' '{' '"config":' '{' '"admins":' '[],' '"crypto_config":' '{' '"identity_identifier_hash_function":' '"SHA256",' '"signature_hash_family":' '"SHA2"' '},' '"fabric_node_ous":' '{' '"admin_ou_identifier":' '{' '"certificate":' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWZpZ0F3SUJBZ0lSQUt0alh5aWhZeTZzazZad1drL3NUYWt3Q2dZSUtvWkl6ajBFQXdJd2N6RUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIREFhQmdOVkJBTVRFMk5oCkxtOXlaek11WlhoaGJYQnNaUzVqYjIwd0hoY05NakF3TVRBMU1URTFOekF3V2hjTk16QXdNVEF5TVRFMU56QXcKV2pCek1Rc3dDUVlEVlFRR0V3SlZVekVUTUJFR0ExVUVDQk1LUTJGc2FXWnZjbTVwWVRFV01CUUdBMVVFQnhNTgpVMkZ1SUVaeVlXNWphWE5qYnpFWk1CY0dBMVVFQ2hNUWIzSm5NeTVsZUdGdGNHeGxMbU52YlRFY01Cb0dBMVVFCkF4TVRZMkV1YjNKbk15NWxlR0Z0Y0d4bExtTnZiVEJaTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEEwSUEKQlBhUGVHNk5ZL3ZrY1BWbWg5dEFUQW4wem1KRjNNYS8wSE1FcFRSdFVhTHNrWlF5WFZ3QTdnTkI1SHduZDBTUQpSUTc2WG5qY2FxZmhxUXZ5eXRsNVRmbWpiVEJyTUE0R0ExVWREd0VCL3dRRUF3SUJwakFkQmdOVkhTVUVGakFVCkJnZ3JCZ0VGQlFjREFnWUlLd1lCQlFVSEF3RXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QXBCZ05WSFE0RUlnUWcKS3VCV0pydk5NT0cwa3F4NWxrWFM0WW4vcWpPU3BxYlN4eHhuUStJbUJmWXdDZ1lJS29aSXpqMEVBd0lEU0FBdwpSUUloQUlWcFR4Ulc1M3Z4WWk1ZGdCem14MXlWdzlydEZRVnFING5Ra05RTXNwQVRBaUJqdFZ1Qm5FM25TLzB5CnF4c3FFYVNRN1RQK0k0SnFnbUNrUGIzT3RvMExXUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",' '"organizational_unit_identifier":' '"admin"' '},' '"client_ou_identifier":' '{' '"certificate":' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWZpZ0F3SUJBZ0lSQUt0alh5aWhZeTZzazZad1drL3NUYWt3Q2dZSUtvWkl6ajBFQXdJd2N6RUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIREFhQmdOVkJBTVRFMk5oCkxtOXlaek11WlhoaGJYQnNaUzVqYjIwd0hoY05NakF3TVRBMU1URTFOekF3V2hjTk16QXdNVEF5TVRFMU56QXcKV2pCek1Rc3dDUVlEVlFRR0V3SlZVekVUTUJFR0ExVUVDQk1LUTJGc2FXWnZjbTVwWVRFV01CUUdBMVVFQnhNTgpVMkZ1SUVaeVlXNWphWE5qYnpFWk1CY0dBMVVFQ2hNUWIzSm5NeTVsZUdGdGNHeGxMbU52YlRFY01Cb0dBMVVFCkF4TVRZMkV1YjNKbk15NWxlR0Z0Y0d4bExtTnZiVEJaTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEEwSUEKQlBhUGVHNk5ZL3ZrY1BWbWg5dEFUQW4wem1KRjNNYS8wSE1FcFRSdFVhTHNrWlF5WFZ3QTdnTkI1SHduZDBTUQpSUTc2WG5qY2FxZmhxUXZ5eXRsNVRmbWpiVEJyTUE0R0ExVWREd0VCL3dRRUF3SUJwakFkQmdOVkhTVUVGakFVCkJnZ3JCZ0VGQlFjREFnWUlLd1lCQlFVSEF3RXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QXBCZ05WSFE0RUlnUWcKS3VCV0pydk5NT0cwa3F4NWxrWFM0WW4vcWpPU3BxYlN4eHhuUStJbUJmWXdDZ1lJS29aSXpqMEVBd0lEU0FBdwpSUUloQUlWcFR4Ulc1M3Z4WWk1ZGdCem14MXlWdzlydEZRVnFING5Ra05RTXNwQVRBaUJqdFZ1Qm5FM25TLzB5CnF4c3FFYVNRN1RQK0k0SnFnbUNrUGIzT3RvMExXUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",' '"organizational_unit_identifier":' '"client"' '},' '"enable":' true, '"orderer_ou_identifier":' '{' '"certificate":' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWZpZ0F3SUJBZ0lSQUt0alh5aWhZeTZzazZad1drL3NUYWt3Q2dZSUtvWkl6ajBFQXdJd2N6RUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIREFhQmdOVkJBTVRFMk5oCkxtOXlaek11WlhoaGJYQnNaUzVqYjIwd0hoY05NakF3TVRBMU1URTFOekF3V2hjTk16QXdNVEF5TVRFMU56QXcKV2pCek1Rc3dDUVlEVlFRR0V3SlZVekVUTUJFR0ExVUVDQk1LUTJGc2FXWnZjbTVwWVRFV01CUUdBMVVFQnhNTgpVMkZ1SUVaeVlXNWphWE5qYnpFWk1CY0dBMVVFQ2hNUWIzSm5NeTVsZUdGdGNHeGxMbU52YlRFY01Cb0dBMVVFCkF4TVRZMkV1YjNKbk15NWxlR0Z0Y0d4bExtTnZiVEJaTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEEwSUEKQlBhUGVHNk5ZL3ZrY1BWbWg5dEFUQW4wem1KRjNNYS8wSE1FcFRSdFVhTHNrWlF5WFZ3QTdnTkI1SHduZDBTUQpSUTc2WG5qY2FxZmhxUXZ5eXRsNVRmbWpiVEJyTUE0R0ExVWREd0VCL3dRRUF3SUJwakFkQmdOVkhTVUVGakFVCkJnZ3JCZ0VGQlFjREFnWUlLd1lCQlFVSEF3RXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QXBCZ05WSFE0RUlnUWcKS3VCV0pydk5NT0cwa3F4NWxrWFM0WW4vcWpPU3BxYlN4eHhuUStJbUJmWXdDZ1lJS29aSXpqMEVBd0lEU0FBdwpSUUloQUlWcFR4Ulc1M3Z4WWk1ZGdCem14MXlWdzlydEZRVnFING5Ra05RTXNwQVRBaUJqdFZ1Qm5FM25TLzB5CnF4c3FFYVNRN1RQK0k0SnFnbUNrUGIzT3RvMExXUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",' '"organizational_unit_identifier":' '"orderer"' '},' '"peer_ou_identifier":' '{' '"certificate":' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWZpZ0F3SUJBZ0lSQUt0alh5aWhZeTZzazZad1drL3NUYWt3Q2dZSUtvWkl6ajBFQXdJd2N6RUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIREFhQmdOVkJBTVRFMk5oCkxtOXlaek11WlhoaGJYQnNaUzVqYjIwd0hoY05NakF3TVRBMU1URTFOekF3V2hjTk16QXdNVEF5TVRFMU56QXcKV2pCek1Rc3dDUVlEVlFRR0V3SlZVekVUTUJFR0ExVUVDQk1LUTJGc2FXWnZjbTVwWVRFV01CUUdBMVVFQnhNTgpVMkZ1SUVaeVlXNWphWE5qYnpFWk1CY0dBMVVFQ2hNUWIzSm5NeTVsZUdGdGNHeGxMbU52YlRFY01Cb0dBMVVFCkF4TVRZMkV1YjNKbk15NWxlR0Z0Y0d4bExtTnZiVEJaTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEEwSUEKQlBhUGVHNk5ZL3ZrY1BWbWg5dEFUQW4wem1KRjNNYS8wSE1FcFRSdFVhTHNrWlF5WFZ3QTdnTkI1SHduZDBTUQpSUTc2WG5qY2FxZmhxUXZ5eXRsNVRmbWpiVEJyTUE0R0ExVWREd0VCL3dRRUF3SUJwakFkQmdOVkhTVUVGakFVCkJnZ3JCZ0VGQlFjREFnWUlLd1lCQlFVSEF3RXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QXBCZ05WSFE0RUlnUWcKS3VCV0pydk5NT0cwa3F4NWxrWFM0WW4vcWpPU3BxYlN4eHhuUStJbUJmWXdDZ1lJS29aSXpqMEVBd0lEU0FBdwpSUUloQUlWcFR4Ulc1M3Z4WWk1ZGdCem14MXlWdzlydEZRVnFING5Ra05RTXNwQVRBaUJqdFZ1Qm5FM25TLzB5CnF4c3FFYVNRN1RQK0k0SnFnbUNrUGIzT3RvMExXUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",' '"organizational_unit_identifier":' '"peer"' '}' '},' '"intermediate_certs":' '[],' '"name":' '"Org3MSP",' '"organizational_unit_identifiers":' '[],' '"revocation_list":' '[],' '"root_certs":' '[' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWZpZ0F3SUJBZ0lSQUt0alh5aWhZeTZzazZad1drL3NUYWt3Q2dZSUtvWkl6ajBFQXdJd2N6RUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIREFhQmdOVkJBTVRFMk5oCkxtOXlaek11WlhoaGJYQnNaUzVqYjIwd0hoY05NakF3TVRBMU1URTFOekF3V2hjTk16QXdNVEF5TVRFMU56QXcKV2pCek1Rc3dDUVlEVlFRR0V3SlZVekVUTUJFR0ExVUVDQk1LUTJGc2FXWnZjbTVwWVRFV01CUUdBMVVFQnhNTgpVMkZ1SUVaeVlXNWphWE5qYnpFWk1CY0dBMVVFQ2hNUWIzSm5NeTVsZUdGdGNHeGxMbU52YlRFY01Cb0dBMVVFCkF4TVRZMkV1YjNKbk15NWxlR0Z0Y0d4bExtTnZiVEJaTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEEwSUEKQlBhUGVHNk5ZL3ZrY1BWbWg5dEFUQW4wem1KRjNNYS8wSE1FcFRSdFVhTHNrWlF5WFZ3QTdnTkI1SHduZDBTUQpSUTc2WG5qY2FxZmhxUXZ5eXRsNVRmbWpiVEJyTUE0R0ExVWREd0VCL3dRRUF3SUJwakFkQmdOVkhTVUVGakFVCkJnZ3JCZ0VGQlFjREFnWUlLd1lCQlFVSEF3RXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QXBCZ05WSFE0RUlnUWcKS3VCV0pydk5NT0cwa3F4NWxrWFM0WW4vcWpPU3BxYlN4eHhuUStJbUJmWXdDZ1lJS29aSXpqMEVBd0lEU0FBdwpSUUloQUlWcFR4Ulc1M3Z4WWk1ZGdCem14MXlWdzlydEZRVnFING5Ra05RTXNwQVRBaUJqdFZ1Qm5FM25TLzB5CnF4c3FFYVNRN1RQK0k0SnFnbUNrUGIzT3RvMExXUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K"' '],' '"signing_identity":' null, '"tls_intermediate_certs":' '[],' '"tls_root_certs":' '[' '"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNWekNDQWY2Z0F3SUJBZ0lSQU0zVmZZOTJDVy9BKzdYTUVVVTMxQjh3Q2dZSUtvWkl6ajBFQXdJd2RqRUwKTUFrR0ExVUVCaE1DVlZNeEV6QVJCZ05WQkFnVENrTmhiR2xtYjNKdWFXRXhGakFVQmdOVkJBY1REVk5oYmlCRwpjbUZ1WTJselkyOHhHVEFYQmdOVkJBb1RFRzl5WnpNdVpYaGhiWEJzWlM1amIyMHhIekFkQmdOVkJBTVRGblJzCmMyTmhMbTl5WnpNdVpYaGhiWEJzWlM1amIyMHdIaGNOTWpBd01UQTFNVEUxTnpBd1doY05NekF3TVRBeU1URTEKTnpBd1dqQjJNUXN3Q1FZRFZRUUdFd0pWVXpFVE1CRUdBMVVFQ0JNS1EyRnNhV1p2Y201cFlURVdNQlFHQTFVRQpCeE1OVTJGdUlFWnlZVzVqYVhOamJ6RVpNQmNHQTFVRUNoTVFiM0puTXk1bGVHRnRjR3hsTG1OdmJURWZNQjBHCkExVUVBeE1XZEd4elkyRXViM0puTXk1bGVHRnRjR3hsTG1OdmJUQlpNQk1HQnlxR1NNNDlBZ0VHQ0NxR1NNNDkKQXdFSEEwSUFCQkUxYzdnc1JuZk5yRUhmd3JaMmhiRG9ydW9RTzlzOVBEWGZGcGgwUU85V013dWRlRTZ2bW55ZApmRDgzdjdKRWVKSFpRNjY2ZWlDM3VQQzllTUVYb3ZpamJUQnJNQTRHQTFVZER3RUIvd1FFQXdJQnBqQWRCZ05WCkhTVUVGakFVQmdnckJnRUZCUWNEQWdZSUt3WUJCUVVIQXdFd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBcEJnTlYKSFE0RUlnUWd3OVFRd2dMdzc1elA3MzNNV1hTZ21Dc2hIWDBDazJkNnNUNE1BUzRHYWpjd0NnWUlLb1pJemowRQpBd0lEUndBd1JBSWdiTUhDdnFraWI5N09Jc1RXZnR0cnQ1aThCRklhRGRXMysvNEw4SkFNSTBZQ0lCWFUxSWRHClJWZlRPRDNCQkVtTWFIRXFqb2M1K3RTMjB0MWcvRFgzcTdvVgotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="' ']' '},' '"type":' 0 '},' '"version":' '"0"' '}' '},' '"version":' '"0"' '}' '},' '"mod_policy":' '"Admins",' '"policies":' '{' '"Admins":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Readers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '},' '"Writers":' '{' '"mod_policy":' '"",' '"policy":' null, '"version":' '"0"' '}' '},' '"values":' '{' '"Capabilities":' '{' '"mod_policy":' '"",' '"value":' null, '"version":' '"0"' '}' '},' '"version":' '"2"' '}' '},' '"mod_policy":' '"",' '"policies":' '{},' '"values":' '{},' '"version":' '"0"' '}' '}}}}'
+ configtxlator proto_encode --input config_update_in_envelope.json --type common.Envelope
+ set +x

========= Config transaction to add org3 to network created =====

Signing config transaction

+ peer channel signconfigtx -f org3_update_in_envelope.pb
2020-01-05 12:02:00.480 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
+ set +x

========= Submitting transaction from a different peer (peer0.org2) which also signs it =========

+ peer channel update -f org3_update_in_envelope.pb -c mychannel -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
2020-01-05 12:02:00.522 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:02:00.538 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
+ set +x

========= Config transaction to add org3 to network submitted! ===========

root@fabric-1:/home/vagrant/fabric-samples/first-network# vi eyfn.sh
root@fabric-1:/home/vagrant/fabric-samples/first-network# ./eyfn.sh up
Starting with channel 'mychannel' and CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
proceeding ...
Creating volume "net_peer0.org3.example.com" with default driver
Creating volume "net_peer1.org3.example.com" with default driver
WARNING: Found orphan containers (cli, peer0.org2.example.com, peer0.org1.example.com, peer1.org2.example.com, orderer.example.com, peer1.org1.example.com) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Creating peer1.org3.example.com ... done
Creating peer0.org3.example.com ... done
Creating Org3cli                ... done

###############################################################
############### Have Org3 peers join network ##################
###############################################################
+ peer channel fetch 0 mychannel.block -o orderer.example.com:7050 -c mychannel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

========= Getting Org3 on to your first network =========

Fetching channel config block from orderer...
+ res=0
+ set +x
2020-01-05 12:02:24.562 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:02:24.563 UTC [cli.common] readBlock -> INFO 002 Received block: 0
+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 12:02:24.611 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:02:24.636 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer0.org3 joined channel 'mychannel' =====================
+ peer channel join -b mychannel.block
+ res=0
+ set +x
2020-01-05 12:02:24.686 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2020-01-05 12:02:24.702 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer1.org3 joined channel 'mychannel' =====================
Installing chaincode 2.0 on peer0.org3...
+ peer chaincode install -n mycc -v 2.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2020-01-05 12:02:24.750 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:02:24.750 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:02:24.863 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org3 =====================


========= Org3 is now halfway onto your first network =========


###############################################################
##### Upgrade chaincode to have Org3 peers on the network #####
###############################################################

========= Finish adding Org3 to your first network =========

+ peer chaincode install -n mycc -v 2.0 -l golang -p github.com/chaincode/chaincode_example02/go/
===================== Installing chaincode 2.0 on peer0.org1 =====================
+ res=0
+ set +x
2020-01-05 12:02:25.205 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:02:25.206 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:02:25.309 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org1 =====================

===================== Installing chaincode 2.0 on peer0.org2 =====================
+ peer chaincode install -n mycc -v 2.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2020-01-05 12:02:25.360 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:02:25.360 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:02:25.469 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org2 =====================

===================== Upgrading chaincode on peer0.org1 =====================
+ peer chaincode upgrade -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc -v 2.0 -c '{"Args":["init","a","90","b","210"]}' -P 'AND ('\''Org1MSP.peer'\'','\''Org2MSP.peer'\'','\''Org3MSP.peer'\'')'
2020-01-05 12:02:25.516 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:02:25.517 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
+ res=0
+ set +x
2020-01-05 12:02:25.360 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2020-01-05 12:02:25.360 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2020-01-05 12:02:25.469 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is upgraded on peer0.org1 on channel 'mychannel' =====================

========= Finished adding Org3 to your first network! =========


 ____    _____      _      ____    _____
/ ___|  |_   _|    / \    |  _ \  |_   _|
\___ \    | |     / _ \   | |_) |   | |
 ___) |   | |    / ___ \  |  _ <    | |
|____/    |_|   /_/   \_\ |_| \_\   |_|

Extend your first network (EYFN) test

Channel name : mychannel
Querying chaincode on peer0.org3...
===================== Querying on peer0.org3 on channel 'mychannel'... =====================
Attempting to Query peer0.org3 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

90
===================== Query successful on peer0.org3 on channel 'mychannel' =====================
Sending invoke transaction on peer0.org1 peer0.org2 peer0.org3...
+ peer chaincode invoke -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt --peerAddresses peer0.org3.example.com:11051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt -c '{"Args":["invoke","a","b","10"]}'
+ res=0
+ set +x
2020-01-05 12:03:28.757 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
===================== Invoke transaction successful on peer0.org1 peer0.org2 peer0.org3 on channel 'mychannel' =====================

Querying chaincode on peer0.org3...
===================== Querying on peer0.org3 on channel 'mychannel'... =====================
Attempting to Query peer0.org3 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

80
===================== Query successful on peer0.org3 on channel 'mychannel' =====================
Querying chaincode on peer0.org2...
===================== Querying on peer0.org2 on channel 'mychannel'... =====================
Attempting to Query peer0.org2 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

80
===================== Query successful on peer0.org2 on channel 'mychannel' =====================
Querying chaincode on peer0.org1...
===================== Querying on peer0.org1 on channel 'mychannel'... =====================
Attempting to Query peer0.org1 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

80
===================== Query successful on peer0.org1 on channel 'mychannel' =====================

========= All GOOD, EYFN test execution completed ===========


 _____   _   _   ____
| ____| | \ | | |  _ \
|  _|   |  \| | | | | |
| |___  | |\  | | |_| |
|_____| |_| \_| |____/

```

네트워크 org3 추가가 끝이나면 `docker ps` 명령어를 쳤을때 현재 컨테이너의 상태가 아래와 같습니다.

```shell
$ docker ps
CONTAINER ID        IMAGE                                                                                                  COMMAND                  CREATED              STATUS              PORTS                      NAMES
f3e724446a24        dev-peer0.org2.example.com-mycc-2.0-c7aee9ad18dddc18319f5f00199f05d866f9e61dca40c9af3e226d434ac4a63c   "chaincode -peer.add…"   40 seconds ago       Up 39 seconds                                  dev-peer0.org2.example.com-mycc-2.0
d75e219f00af        dev-peer0.org3.example.com-mycc-2.0-156223788c3ef42ff3094c6cf1d2f71284c36f2074cc4d1f09a7065cb903d192   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org3.example.com-mycc-2.0
6bad1c5342ca        dev-peer0.org1.example.com-mycc-2.0-2732cd4d96a0b88594aefca15581eaa0fb481ad15beeb86cc79931b2a90ee621   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org1.example.com-mycc-2.0
79b1749766ac        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              About a minute ago   Up About a minute                              Org3cli
a2f1f90c496d        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:11051->11051/tcp   peer0.org3.example.com
86c793a09dc1        hyperledger/fabric-peer:latest                                                                         "peer node start"        About a minute ago   Up About a minute   0.0.0.0:12051->12051/tcp   peer1.org3.example.com
d935b4c05e80        dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab   "chaincode -peer.add…"   2 minutes ago        Up 2 minutes                                   dev-peer1.org2.example.com-mycc-1.0
a406944b01ec        dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9   "chaincode -peer.add…"   3 minutes ago        Up 3 minutes                                   dev-peer0.org1.example.com-mycc-1.0
d12628a39c8b        dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b   "chaincode -peer.add…"   3 minutes ago        Up 3 minutes                                   dev-peer0.org2.example.com-mycc-1.0
8a0d121e21c0        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              4 minutes ago        Up 4 minutes                                   cli
0548c53e2464        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 minutes ago        Up 4 minutes        0.0.0.0:9051->9051/tcp     peer0.org2.example.com
a176d7245611        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 minutes ago        Up 4 minutes        0.0.0.0:7051->7051/tcp     peer0.org1.example.com
af300dab906d        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 minutes ago        Up 4 minutes        0.0.0.0:10051->10051/tcp   peer1.org2.example.com
0f7fbfe0c0f0        hyperledger/fabric-orderer:latest                                                                      "orderer"                4 minutes ago        Up 4 minutes        0.0.0.0:7050->7050/tcp     orderer.example.com
90d452410ac7        hyperledger/fabric-peer:latest                                                                         "peer node start"        4 minutes ago        Up 4 minutes        0.0.0.0:8051->8051/tcp     peer1.org1.example.com
root@fabric-1:/home/vagrant/fabric-samples/first-network#
```

다음 포스트에서는 이전과 같은 방식으로 하나하나 살펴보면서 넘어가보겠습니다.