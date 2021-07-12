---
title : Hyperledger Network 구성 (BYFN)
categories:
- BlockChain
tags :
- BYFN
- Hyperledger Fabric
- BlockChain
---

## Network 구성

크게 2가지로 나눠서 해보겠습니다.

첫 번째로는 Hyperledger 에서 제공하는 `byfn.sh` 파일을 이용하여 간단하고 빠르게 네트워크를 구성하는 방법을 이용할것입니다.

두 번째로는 hyperledger 에서 제공하는 `binary` 파일들을 이용하여 천천히 하나하나 명령어를 설명하면서 진행하겠습니다.

현 포스트는 첫 번째 방법을 이용하여 네트워크를 구성해보겠습니다.

### Version

```
Vagrant 2.2.5
Ubuntu 16.04.6 LTS
Hyperledger Fabric 1.4.x
```

> Vagrantfile

```shell
Vagrant.configure("2") do |config|
  vm_num = 1
  node_cpu = 1 # 1Core
  node_memory = "2048" # 2G Memory
  node_network = "10.30.30"
  node_prefix = "fabric"

  config.vm.box = "ubuntu/xenial64"
  config.vm.box_check_update = false
  #config.disksize.size = "10GB" # > 10GB

  (1..vm_num).each do |i|
    config.vm.define "#{node_prefix}-#{i}" do |node|
      hostname = "#{node_prefix}-#{i}"
      hostip = "#{node_network}.#{i + 1}"

      node.vm.hostname = hostname
      node.vm.network "private_network", ip: hostip

      node.vm.provider "virtualbox" do |vb|
        vb.name = "#{node_prefix}-#{i}"
        vb.gui = false
        vb.cpus = node_cpu
        vb.memory = node_memory
      end
    end
  end
end
```

### 1. VM 생성 / 재시작

```shell
$ vagrant up

Bringing machine 'fabric-1' up with 'virtualbox' provider...
==> fabric-1: Importing base box 'ubuntu/xenial64'...
==> fabric-1: Matching MAC address for NAT networking...
==> fabric-1: Setting the name of the VM: fabric-1
==> fabric-1: Fixed port collision for 22 => 2222. Now on port 2200.
==> fabric-1: Clearing any previously set network interfaces...
==> fabric-1: Preparing network interfaces based on configuration...
    fabric-1: Adapter 1: nat
    fabric-1: Adapter 2: hostonly
==> fabric-1: Forwarding ports...
    fabric-1: 22 (guest) => 2200 (host) (adapter 1)
==> fabric-1: Running 'pre-boot' VM customizations...
==> fabric-1: Booting VM...
==> fabric-1: Waiting for machine to boot. This may take a few minutes...
    fabric-1: SSH address: 127.0.0.1:2200
    fabric-1: SSH username: vagrant
    fabric-1: SSH auth method: private key
    fabric-1:
    fabric-1: Vagrant insecure key detected. Vagrant will automatically replace
    fabric-1: this with a newly generated keypair for better security.
    fabric-1:
    fabric-1: Inserting generated public key within guest...
    fabric-1: Removing insecure key from the guest if it's present...
    fabric-1: Key inserted! Disconnecting and reconnecting using new SSH key...
==> fabric-1: Machine booted and ready!
==> fabric-1: Checking for guest additions in VM...
    fabric-1: The guest additions on this VM do not match the installed version of
    fabric-1: VirtualBox! In most cases this is fine, but in rare cases it can
    fabric-1: prevent things such as shared folders from working properly. If you see
    fabric-1: shared folder errors, please make sure the guest additions within the
    fabric-1: virtual machine match the version of VirtualBox you have installed on
    fabric-1: your host and reload your VM.
    fabric-1:
    fabric-1: Guest Additions Version: 5.1.38
    fabric-1: VirtualBox Version: 6.0
==> fabric-1: Setting hostname...
==> fabric-1: Configuring and enabling network interfaces...
==> fabric-1: Mounting shared folders...
    fabric-1: /vagrant => /Users/has3ong/Desktop/fabric-2
```

### 2. VM 접속

```shell
$ vagrant ssh fabric-1
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-159-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

New release '18.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

vagrant@fabric-1:~$
```

### 3. VM 중지

```shell
$ vagrant halt fabric-1
==> fabric-1: Attempting graceful shutdown of VM...
```

### 4. VM 삭제

```shell
$ vagrant destroy fabric-1
    fabric-1: Are you sure you want to destroy the 'fabric-1' VM? [y/N] y
==> fabric-1: Destroying VM and associated drives...
```

# VM Setting

## 1. VM 접속 실습파일 다운로드 및 적용

### 1.1 VM 접속

```shell
$ vagrant status
Current machine states:

fabric-1                    poweroff (virtualbox)

The VM is powered off. To restart the VM, simply run `vagrant up`

$ vagrant up fabric-1

$ vagrant ssh fabric-1

vagrant@fabric-1:~$
```

## 2. Install Go

```shell
$ wget https://dl.google.com/go/go1.12.9.linux-amd64.tar.gz
$ tar zxf go1.12.9.linux-amd64.tar.gz
$ sudo mv go /usr/local
$ rm go1.12.9.linux-amd64.tar.gz
$ sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common

operties-common
Reading package lists... Done
Building dependency tree
Reading state information... Done
apt-transport-https is already the newest version (1.2.32).
ca-certificates is already the newest version (20170717~16.04.2).
curl is already the newest version (7.47.0-1ubuntu2.13).
software-properties-common is already the newest version (0.96.20.9).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

## 3. Install Docker

```shell
$ sudo apt-get remove docker docker-engine docker.i

$ sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

$ sudo add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) \
 stable"
 
$ sudo apt-get update
$ sudo apt-get install docker-ce
$ sudo usermod -a -G docker vagrant

$ docker version

Client: Docker Engine - Community
 Version:           19.03.4
 API version:       1.40
 Go version:        go1.12.10
 Git commit:        9013bf583a
 Built:             Fri Oct 18 15:53:51 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.4
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.10
  Git commit:       9013bf583a
  Built:            Fri Oct 18 15:52:23 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

## 4. Install Docker Compose

```shell
$ sudo curl -L https://github.com/docker/compose/releases/download/1.23.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose

$ docker-compose --version
docker-compose version 1.23.2, build 1110ad01
```

## 5. Install Hyperledger Fabric Samples

네트워크 구성에 필요한 바이너리 파일 및 docker images를 다운받습니다. 밑에 로그를 확인해보면 peer, ordererd와 같은 이미지를 다운받는걸 알 수 있습니다.

```shell
$ curl -sSL http://bit.ly/2ysbOFE | bash -s -- 1.4.3 1.4.3 0.4.15

Installing Hyperledger Fabric docker images

===> Pulling fabric Images
==> FABRIC IMAGE: peer

1.4.3: Pulling from hyperledger/fabric-peer

Digest: sha256:fc11964a5201fc559bcee573e601753bf6218e35ded2f5259d86bc73cdc38976
Status: Downloaded newer image for hyperledger/fabric-peer:1.4.3
docker.io/hyperledger/fabric-peer:1.4.3
==> FABRIC IMAGE: orderer

1.4.3: Pulling from hyperledger/fabric-orderer

Digest: sha256:efbcd38e7a09066621a16e6da0e35329c02c3491046538cfd1107a96f0c750cf
Status: Downloaded newer image for hyperledger/fabric-orderer:1.4.3
docker.io/hyperledger/fabric-orderer:1.4.3
==> FABRIC IMAGE: ccenv

1.4.3: Pulling from hyperledger/fabric-ccenv

Digest: sha256:33068b526a06eea57e131a86472f1117d8d525245ff7b66d436b18a5a53dbb4e
Status: Downloaded newer image for hyperledger/fabric-ccenv:1.4.3
docker.io/hyperledger/fabric-ccenv:1.4.3
==> FABRIC IMAGE: tools

1.4.3: Pulling from hyperledger/fabric-tools

Digest: sha256:eda7bc6d79d55bcbae248333f3275c46f57ccab610251b55f8e6845ebe8fcf52
Status: Downloaded newer image for hyperledger/fabric-tools:1.4.3
docker.io/hyperledger/fabric-tools:1.4.3
==> FABRIC IMAGE: baseos

Error response from daemon: manifest for hyperledger/fabric-baseos:1.4.3 not found: manifest unknown: manifest unknown
Error response from daemon: No such image: hyperledger/fabric-baseos:1.4.3
==> FABRIC IMAGE: nodeenv

Error response from daemon: manifest for hyperledger/fabric-nodeenv:1.4.3 not found: manifest unknown: manifest unknown
Error response from daemon: No such image: hyperledger/fabric-nodeenv:1.4.3
==> FABRIC IMAGE: javaenv

Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: TLS handshake timeout
Error response from daemon: No such image: hyperledger/fabric-javaenv:1.4.3
===> Pulling fabric ca Image
==> FABRIC CA IMAGE

1.4.3: Pulling from hyperledger/fabric-ca

Digest: sha256:82a7f653ed0de520bf3ee565a07a76aac8b91ed80869b33dddfec39652c9d183
Status: Downloaded newer image for hyperledger/fabric-ca:1.4.3
docker.io/hyperledger/fabric-ca:1.4.3
===> Pulling thirdparty docker images
==> THIRDPARTY DOCKER IMAGE: couchdb

0.4.15: Pulling from hyperledger/fabric-couchdb

Digest: sha256:f6c724592abf9c2b35d2f4cd6a7afcde9c1052cfed61560b20ef9e2e927d1790
Status: Downloaded newer image for hyperledger/fabric-couchdb:0.4.15
docker.io/hyperledger/fabric-couchdb:0.4.15
==> THIRDPARTY DOCKER IMAGE: kafka

0.4.15: Pulling from hyperledger/fabric-kafka

Digest: sha256:62418a885c291830510379d9eb09fbdd3d397052d916ed877a468b0e2026b9e3
Status: Downloaded newer image for hyperledger/fabric-kafka:0.4.15
docker.io/hyperledger/fabric-kafka:0.4.15
==> THIRDPARTY DOCKER IMAGE: zookeeper

0.4.15: Pulling from hyperledger/fabric-zookeeper


===> List out hyperledger docker images
hyperledger/fabric-tools       1.4.3               18ed4db0cd57        7 weeks ago         1.55GB
hyperledger/fabric-tools       latest              18ed4db0cd57        7 weeks ago         1.55GB
hyperledger/fabric-ca          1.4.3               c18a0d3cc958        7 weeks ago         253MB
hyperledger/fabric-ca          latest              c18a0d3cc958        7 weeks ago         253MB
hyperledger/fabric-ccenv       1.4.3               3d31661a812a        7 weeks ago         1.45GB
hyperledger/fabric-ccenv       latest              3d31661a812a        7 weeks ago         1.45GB
hyperledger/fabric-orderer     1.4.3               b666a6ebbe09        7 weeks ago         173MB
hyperledger/fabric-orderer     latest              b666a6ebbe09        7 weeks ago         173MB
hyperledger/fabric-peer        1.4.3               fa87ccaed0ef        7 weeks ago         179MB
hyperledger/fabric-peer        latest              fa87ccaed0ef        7 weeks ago         179MB
hyperledger/fabric-zookeeper   0.4.15              20c6045930c8        7 months ago        1.43GB
hyperledger/fabric-zookeeper   latest              20c6045930c8        7 months ago        1.43GB
hyperledger/fabric-kafka       0.4.15              b4ab82bbaf2f        7 months ago        1.44GB
hyperledger/fabric-kafka       latest              b4ab82bbaf2f        7 months ago        1.44GB
hyperledger/fabric-couchdb     0.4.15              8de128a55539        7 months ago        1.5GB
hyperledger/fabric-couchdb     latest              8de128a55539        7 months ago        1.5GB

vagrant@fabric-1:~$ ls
fabric-samples

$ chown -R vagrant:vagrant fabric-samples
```

# HandsOn

## Generate Network Artifacts

fabric-samples에 first-network로 이동해줍니다. 해당 디렉토리에는 아래와 같은 파일들이 있습니다. 저희들은 여기서 byfn.sh 파일을 사용하겠습니다.

```shell
$ cd fabric-samples/first-network/
vagrant@fabric-1:~/fabric-samples/first-network$ ls
base               configtx.yaml            docker-compose-couch-org3.yaml    eyfn.sh
byfn.sh            connection-org3.json     docker-compose-couch.yaml         org3-artifacts
ccp-generate.sh    connection-org3.yaml     docker-compose-e2e-template.yaml  README.md
ccp-template.json  crypto-config.yaml       docker-compose-etcdraft2.yaml     scripts
ccp-template.yaml  docker-compose-ca.yaml   docker-compose-kafka.yaml
channel-artifacts  docker-compose-cli.yaml  docker-compose-org3.yaml
```

`./byfn.sh generate`를 입력해줍니다. 로그는 아래에서 확인해보면 됩니다.

```shell
$ ./byfn.sh generate
Generating certs and genesis block for channel 'mychannel' with CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
```

`byfn.sh` 을 `generate` 하게 되면 제일 먼저 org1과 org2의 crypto-config가 만들어집니다. 이 디렉토리는 각각의 `peer` 과 `orderer가` 서로 통신할 때 사용하는 키와 인증서가 만들어집니다. 실제로 진행을 시키고 나면 `crypto-config` 파일이 만들어져있습니다.

```shell
$ ls
base                  connection-org2.yaml              docker-compose-e2e.yaml
byfn.sh               connection-org3.json              docker-compose-etcdraft2.yaml
ccp-generate.sh       connection-org3.yaml              docker-compose-kafka.yaml
ccp-template.json     crypto-config                     docker-compose-org3.yaml
ccp-template.yaml     crypto-config.yaml                eyfn.sh
channel-artifacts     docker-compose-ca.yaml            org3-artifacts
configtx.yaml         docker-compose-cli.yaml           README.md
connection-org1.json  docker-compose-couch-org3.yaml    scripts
connection-org1.yaml  docker-compose-couch.yaml
connection-org2.json  docker-compose-e2e-template.yaml
```

crypto-config 디렉토리를 간략하게 보면 다음과 같습니다. 궁금하실 수도 있어서 참고로 올려놓겠습니다.

![스크린샷 2019-10-21 오후 11 07 56](https://user-images.githubusercontent.com/44635266/67212726-bce58000-f457-11e9-9574-5c94350a9137.png)

![스크린샷 2019-10-21 오후 11 08 03](https://user-images.githubusercontent.com/44635266/67212727-bce58000-f457-11e9-8cce-6a62544d74b7.png)


```shell
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
```

그리고 `channel-artifacts` 디렉토리 안에 `genesis.block`, `channel.tx`, `Org1MSPanchors.tx`, `Org2MSPanchors.tx` 4가지 파일이 만들어집니다.

`제네시스 블록(genesis block)`은 블록체인에서 생성된 첫 번째 블록을 말한다. 첫 번째 블록이 생성된 이후에 다음 블록이 지속적으로 생성되어 마치 체인처럼 이전 블록에 연결되기 때문에, 제네시스 블록이 생성되었다는 것은 해당 블록체인 네트워크가 시작되었다고 생각하면 됩니다.

`channel.tx`, `Org1MSPanchors.tx`, `Org2MSPanchors.tx`는 각각 채널의 대한 정보와 1번째 조직과 2번째 조직에 `AnchorPeer`의 정보를 담는 트랜잭션입니다.

```shell
Generate CCP files for Org1 and Org2
/home/vagrant/fabric-samples/first-network/../bin/configtxgen
##########################################################
#########  Generating Orderer Genesis block ##############
##########################################################
CONSENSUS_TYPE=solo
+ '[' solo == solo ']'
+ configtxgen -profile TwoOrgsOrdererGenesis -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
2019-10-21 14:04:28.604 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-21 14:04:28.678 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 002 orderer type: solo
2019-10-21 14:04:28.679 UTC [common.tools.configtxgen.localconfig] Load -> INFO 003 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:28.752 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 004 orderer type: solo
2019-10-21 14:04:28.752 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 005 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:28.754 UTC [common.tools.configtxgen] doOutputBlock -> INFO 006 Generating genesis block
2019-10-21 14:04:28.755 UTC [common.tools.configtxgen] doOutputBlock -> INFO 007 Writing genesis block
+ res=0
+ set +x

#################################################################
### Generating channel configuration transaction 'channel.tx' ###
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID mychannel
2019-10-21 14:04:28.792 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-21 14:04:28.888 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:28.971 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-21 14:04:28.971 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:28.972 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 005 Generating new channel configtx
2019-10-21 14:04:28.974 UTC [common.tools.configtxgen] doOutputChannelCreateTx -> INFO 006 Writing new channel tx
+ res=0
+ set +x

#################################################################
#######    Generating anchor peer update for Org1MSP   ##########
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID mychannel -asOrg Org1MSP
2019-10-21 14:04:29.008 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-21 14:04:29.093 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:29.170 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-21 14:04:29.171 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:29.171 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-21 14:04:29.171 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
+ res=0
+ set +x

#################################################################
#######    Generating anchor peer update for Org2MSP   ##########
#################################################################
+ configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID mychannel -asOrg Org2MSP
2019-10-21 14:04:29.203 UTC [common.tools.configtxgen] main -> INFO 001 Loading configuration
2019-10-21 14:04:29.273 UTC [common.tools.configtxgen.localconfig] Load -> INFO 002 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:29.342 UTC [common.tools.configtxgen.localconfig] completeInitialization -> INFO 003 orderer type: solo
2019-10-21 14:04:29.343 UTC [common.tools.configtxgen.localconfig] LoadTopLevel -> INFO 004 Loaded configuration: /home/vagrant/fabric-samples/first-network/configtx.yaml
2019-10-21 14:04:29.343 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 005 Generating anchor peer update
2019-10-21 14:04:29.343 UTC [common.tools.configtxgen] doOutputAnchorPeersUpdate -> INFO 006 Writing anchor peer update
+ res=0
+ set +x
```

## Bring Up the Network

그 다음으로는 `./byfn.sh up` 명령어로 네트워크를 실행 시킵니다. byfn을 실행시키면 엄청 많은 과정이 진행되니까 하나하나 뜯어서 살펴보겠습니다.

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
Creating orderer.example.com    ... done
Creating peer1.org2.example.com ... done
Creating peer0.org2.example.com ... done
Creating peer1.org1.example.com ... done
Creating peer0.org1.example.com ... done
Creating cli                    ... done
CONTAINER ID        IMAGE                               COMMAND             CREATED                  STATUS                  PORTS                      NAMES
a6bc396e9eb4        hyperledger/fabric-tools:latest     "/bin/bash"         Less than a second ago   Up Less than a second                              cli
964870f62a62        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago            Up 1 second             0.0.0.0:8051->8051/tcp     peer1.org1.example.com
01cd5cc6dc85        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago            Up 1 second             0.0.0.0:7051->7051/tcp     peer0.org1.example.com
cc1323d17f4a        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago            Up 1 second             0.0.0.0:9051->9051/tcp     peer0.org2.example.com
9897b1ed790c        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago            Up Less than a second   0.0.0.0:10051->10051/tcp   peer1.org2.example.com
85ce288db191        hyperledger/fabric-orderer:latest   "orderer"           4 seconds ago            Up 2 seconds            0.0.0.0:7050->7050/tcp     orderer.example.com

 ____    _____      _      ____    _____
/ ___|  |_   _|    / \    |  _ \  |_   _|
\___ \    | |     / _ \   | |_) |   | |
 ___) |   | |    / ___ \  |  _ <    | |
|____/    |_|   /_/   \_\ |_| \_\   |_|

Build your first network (BYFN) end-to-end test
```

`docker-compose-cli.yaml` 파일에 설정되어 있는 서비스를 실행시킵니다. `docker-compose-cli.yaml` 파일을 가져와서 이해를 쉽게 하도록 돕겠습니다. `service`에 `orderer.example.com`, `peer0.example.com` 등등 정상적으로 컨테이너에 올라가는 모습을 확인할 수 있습니다.

```yaml
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

version: '2'

volumes:
  orderer.example.com:
  peer0.org1.example.com:
  peer1.org1.example.com:
  peer0.org2.example.com:
  peer1.org2.example.com:

networks:
  byfn:

services:

  orderer.example.com:
    extends:
      file:   base/docker-compose-base.yaml
      service: orderer.example.com
    container_name: orderer.example.com
    networks:
      - byfn

  peer0.org1.example.com:
    container_name: peer0.org1.example.com
    extends:
      file:  base/docker-compose-base.yaml
      service: peer0.org1.example.com
    networks:
      - byfn

  peer1.org1.example.com:
    container_name: peer1.org1.example.com
    extends:
      file:  base/docker-compose-base.yaml
      service: peer1.org1.example.com
    networks:
      - byfn

  peer0.org2.example.com:
    container_name: peer0.org2.example.com
    extends:
      file:  base/docker-compose-base.yaml
      service: peer0.org2.example.com
    networks:
      - byfn

  peer1.org2.example.com:
    container_name: peer1.org2.example.com
    extends:
      file:  base/docker-compose-base.yaml
      service: peer1.org2.example.com
    networks:
      - byfn

  cli:
    container_name: cli
    image: hyperledger/fabric-tools:$IMAGE_TAG
    tty: true
    stdin_open: true
    environment:
      - SYS_CHANNEL=$SYS_CHANNEL
      - GOPATH=/opt/gopath
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      #- FABRIC_LOGGING_SPEC=DEBUG
      - FABRIC_LOGGING_SPEC=INFO
      - CORE_PEER_ID=cli
      - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
      - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
    command: /bin/bash
    volumes:
        - /var/run/:/host/var/run/
        - ./../chaincode/:/opt/gopath/src/github.com/chaincode
        - ./crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/
        - ./scripts:/opt/gopath/src/github.com/hyperledger/fabric/peer/scripts/
        - ./channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts
    depends_on:
      - orderer.example.com
      - peer0.org1.example.com
      - peer1.org1.example.com
      - peer0.org2.example.com
      - peer1.org2.example.com
    networks:
      - byfn
```

다음은 모든 `peer`들이 들어갈 수 있는 채널을 만들어줍니다. `peer`들은 하나의 `node`라고 보셔도 무방합니다.

```shell
+ peer channel create -o orderer.example.com:7050 -c mychannel -f

./channel-artifacts/channel.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
Channel name : mychannel
Creating channel...
+ res=0
+ set +x
2019-10-21 14:23:54.000 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:23:54.028 UTC [cli.common] readBlock -> INFO 002 Received block: 0
===================== Channel 'mychannel' created =====================
```

각각의 `peer`들을 `mychannel`에 조인시켜줍니다. 만들어진 `peer`는 총 4개로 `peer0.org1.example.com`, `peer1.org1.example.com`, `peer0.org2.example.com`, `peer1.org2.example.com` 이란 이름을 가지고 있습니다.

```shell
Having all peers join the channel...
+ peer channel join -b mychannel.block
+ res=0
+ set +x
2019-10-21 14:23:54.084 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:23:54.110 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer0.org1 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2019-10-21 14:23:57.167 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:23:57.193 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer1.org1 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2019-10-21 14:24:00.255 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:24:00.283 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer0.org2 joined channel 'mychannel' =====================

+ peer channel join -b mychannel.block
+ res=0
+ set +x
2019-10-21 14:24:03.340 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:24:03.362 UTC [channelCmd] executeJoin -> INFO 002 Successfully submitted proposal to join channel
===================== peer1.org2 joined channel 'mychannel' =====================
```

다음 각각의 Organization에서 첫 번째 `peer`를 `Anchor Peer`로 업데이트합니다.

```shell
Updating anchor peers for org1...
+ peer channel update -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/Org1MSPanchors.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
+ res=0
+ set +x
2019-10-21 14:24:06.418 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:24:06.432 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
===================== Anchor peers updated for org 'Org1MSP' on channel 'mychannel' =====================

Updating anchor peers for org2...
+ peer channel update -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/Org2MSPanchors.tx --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
+ res=0
+ set +x
2019-10-21 14:24:09.490 UTC [channelCmd] InitCmdFactory -> INFO 001 Endorser and orderer connections initialized
2019-10-21 14:24:09.506 UTC [channelCmd] update -> INFO 002 Successfully submitted channel update
===================== Anchor peers updated for org 'Org2MSP' on channel 'mychannel' =====================
```

다음 `peer`들에게 원장에 내용을 기록하게 만들 수 있는 `chaincode`를 설치합니다. 후에 이 `chaincode`돌려서 가상의 거래를 실행해볼것입니다.

```shell
Installing chaincode on peer0.org1...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2019-10-21 14:24:12.567 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-21 14:24:12.567 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-21 14:24:12.965 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org1 =====================

Install chaincode on peer0.org2...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2019-10-21 14:24:13.009 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-21 14:24:13.009 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-21 14:24:13.110 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer0.org2 =====================

Instantiating chaincode on peer0.org2...
+ peer chaincode instantiate -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc -l golang -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P 'AND ('\''Org1MSP.peer'\'','\''Org2MSP.peer'\'')'
+ res=0
+ set +x
2019-10-21 14:24:13.155 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-21 14:24:13.155 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
===================== Chaincode is instantiated on peer0.org2 on channel 'mychannel' =====================
```

그리고 `peer0.org1.example.com`에서 `Query`를 돌려 자신의 자산을 확인합니다. `first-network` 에서는 A = 100, B = 200 을 초기화 시켜놓고 다음 과정에 나올 `Invoke`를 할 때마다 A에서 B로 10원씩 이동합니다. 즉 거래가 이루어진다고 보시면 됩니다.

맨 마지막에 체인코드를 첨부하여 확인하실 수 있게 하겠습니다.

```shell
Querying chaincode on peer0.org1...
===================== Querying on peer0.org1 on channel 'mychannel'... =====================
Attempting to Query peer0.org1 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

100 // A
===================== Query successful on peer0.org1 on channel 'mychannel' =====================
```

위에서 같은 `peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'` `Query`를 날렸을때 100을 반환했던것과는 달리 아래에서는 90을 반환하는걸 볼 수 있습니다.

이 과정을 통해서 fabric에서 제공하는 한 사이클을 돌리는걸 마무리했습니다.

```shell
Sending invoke transaction on peer0.org1 peer0.org2...
+ peer chaincode invoke -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"Args":["invoke","a","b","10"]}'
+ res=0
+ set +x
2019-10-21 14:25:11.764 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
===================== Invoke transaction successful on peer0.org1 peer0.org2 on channel 'mychannel' =====================

Installing chaincode on peer1.org2...
+ peer chaincode install -n mycc -v 1.0 -l golang -p github.com/chaincode/chaincode_example02/go/
+ res=0
+ set +x
2019-10-21 14:25:11.823 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 001 Using default escc
2019-10-21 14:25:11.823 UTC [chaincodeCmd] checkChaincodeCmdParams -> INFO 002 Using default vscc
2019-10-21 14:25:11.969 UTC [chaincodeCmd] install -> INFO 003 Installed remotely response:<status:200 payload:"OK" >
===================== Chaincode is installed on peer1.org2 =====================

Querying chaincode on peer1.org2...
===================== Querying on peer1.org2 on channel 'mychannel'... =====================
Attempting to Query peer1.org2 ...3 secs
+ peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
+ res=0
+ set +x

90 // A
===================== Query successful on peer1.org2 on channel 'mychannel' =====================

========= All GOOD, BYFN execution completed ===========
```

네트워크 종료가 되고 현재 올라와있는 도커의 상태를 확인할 수 있습니다.

```shell
 _____   _   _   ____
| ____| | \ | | |  _ \
|  _|   |  \| | | | | |
| |___  | |\  | | |_| |
|_____| |_| \_| |____/

root@fabric-1:/home/vagrant/fabric-samples/first-network# docker ps
CONTAINER ID        IMAGE                                                                                                  COMMAND                  CREATED              STATUS              PORTS                      NAMES
eea95535a7cc        dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab   "chaincode -peer.add…"   36 seconds ago       Up 35 seconds                                  dev-peer1.org2.example.com-mycc-1.0
287502b12881        dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org1.example.com-mycc-1.0
10b325e0dc6f        dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b   "chaincode -peer.add…"   About a minute ago   Up About a minute                              dev-peer0.org2.example.com-mycc-1.0
a6bc396e9eb4        hyperledger/fabric-tools:latest                                                                        "/bin/bash"              2 minutes ago        Up 2 minutes                                   cli
964870f62a62        hyperledger/fabric-peer:latest                                                                         "peer node start"        2 minutes ago        Up 2 minutes        0.0.0.0:8051->8051/tcp     peer1.org1.example.com
01cd5cc6dc85        hyperledger/fabric-peer:latest
```

이전과는 달리 체인코드가 3개가 추가되있는것을 보실수 있습니다.

`Invoke`를 한번 더 날려보고 `Query`를 돌려서 결과값을 보겠습니다. 한 번더 돌리게되면 a는 80 b는 220이 되야합니다.

먼저 `cli`로 접속합니다.

```shell
$ docker exec -it cli /bin/bash
```

그리고 `Invoke`와 `Query`를 날려볼게요.

```shell
root@a6bc396e9eb4:/opt/gopath/src/github.com/hyperledger/fabric/peer# peer chaincode invoke -o orderer.example.com:7050 --tls true --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n mycc --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses peer0.org2.example.com:9051 --tlsRootCertFiles /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"Args":["invoke","a","b","10"]}'

2019-10-21 14:47:59.734 UTC [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200

root@a6bc396e9eb4:/opt/gopath/src/github.com/hyperledger/fabric/peer# peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
80

root@a6bc396e9eb4:/opt/gopath/src/github.com/hyperledger/fabric/peer# peer chaincode query -C mychannel -n mycc -c '{"Args":["query","b"]}'
220

root@a6bc396e9eb4:/opt/gopath/src/github.com/hyperledger/fabric/peer#
```

위와같이 되면 네트워크가 잘 구현이된것입니다.

## Bring Down the Network

```shell
$ ./byfn.sh down

Stopping for channel 'mychannel' with CLI timeout of '10' seconds and CLI delay of '3' seconds
Continue? [Y/n] y
proceeding ...
WARNING: The BYFN_CA1_PRIVATE_KEY variable is not set. Defaulting to a blank string.
WARNING: The BYFN_CA2_PRIVATE_KEY variable is not set. Defaulting to a blank string.
Stopping cli                    ... done
Stopping peer1.org1.example.com ... done
Stopping peer0.org1.example.com ... done
Stopping peer0.org2.example.com ... done
Stopping peer1.org2.example.com ... done
Stopping orderer.example.com    ... done
Removing cli                    ... done
Removing peer1.org1.example.com ... done
Removing peer0.org1.example.com ... done
Removing peer0.org2.example.com ... done
Removing peer1.org2.example.com ... done
Removing orderer.example.com    ... done
Removing network net_byfn
Removing volume net_orderer.example.com
Removing volume net_peer0.org1.example.com
Removing volume net_peer1.org1.example.com
Removing volume net_peer0.org2.example.com
Removing volume net_peer1.org2.example.com
Removing volume net_orderer2.example.com
WARNING: Volume net_orderer2.example.com not found.
Removing volume net_orderer3.example.com
WARNING: Volume net_orderer3.example.com not found.
Removing volume net_orderer4.example.com
WARNING: Volume net_orderer4.example.com not found.
Removing volume net_orderer5.example.com
WARNING: Volume net_orderer5.example.com not found.
Removing volume net_peer0.org3.example.com
WARNING: Volume net_peer0.org3.example.com not found.
Removing volume net_peer1.org3.example.com
WARNING: Volume net_peer1.org3.example.com not found.
eea95535a7cc
287502b12881
10b325e0dc6f
Untagged: dev-peer1.org2.example.com-mycc-1.0-26c2ef32838554aac4f7ad6f100aca865e87959c9a126e86d764c8d01f8346ab:latest
Deleted: sha256:e963251a570a754197239d14fd1d0c4340a4212d87568d47c00fed16292ca812
Deleted: sha256:f16de60844b3cf46ec680c26341ac3b3e210fc65206576534f216d8c9f457823
Deleted: sha256:6f63b8afbc4454e769950c74b4cd3a955d8794b93aff745bd5016819326045ae
Deleted: sha256:1626842065e58a30bbbab5355877ae397f7d686041a456879af9af5f5307736e
Untagged: dev-peer0.org1.example.com-mycc-1.0-384f11f484b9302df90b453200cfb25174305fce8f53f4e94d45ee3b6cab0ce9:latest
Deleted: sha256:73204622e3468ca14d4803839f73622af869661f9b5c473981f261615921699c
Deleted: sha256:125e975089bb462e317c8ebc4c2d518ac3b9af1299315ce2eb1551c21f4036c7
Deleted: sha256:0cf54547c5f086e1a94949bbd74e4f40ab55f38cacaf879508bf156745bf4307
Deleted: sha256:261656bc1ef289d10e2c02f5b869eb692c9c6df48a32645ced6fd6c9e9bd9d4a
Untagged: dev-peer0.org2.example.com-mycc-1.0-15b571b3ce849066b7ec74497da3b27e54e0df1345daff3951b94245ce09c42b:latest
Deleted: sha256:209594d56247631cf2ca3ccbd583addd1d5c12fd9c9b547e33d729e89b68d853
Deleted: sha256:ab043f74e02ccf42704f707e7f2df8e6af2994b0300e894c0f49581a20523270
Deleted: sha256:37c67e3515100c4dba5c4c694089c3a471a1f731757b61cbcfd71804a558c7dc
Deleted: sha256:35672f428af63c9f9b768412a9edec8fa3c0a27f19a43b63e584a33111ac187b
```

## Invoke

```go
// Transaction makes payment of X units from A to B
func (t *SimpleChaincode) invoke(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var A, B string    // Entities
	var Aval, Bval int // Asset holdings
	var X int          // Transaction value
	var err error

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	A = args[0]
	B = args[1]

	// Get the state from the ledger
	// TODO: will be nice to have a GetAllState call to ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Avalbytes == nil {
		return shim.Error("Entity not found")
	}
	Aval, _ = strconv.Atoi(string(Avalbytes))

	Bvalbytes, err := stub.GetState(B)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Bvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Bval, _ = strconv.Atoi(string(Bvalbytes))

	// Perform the execution
	X, err = strconv.Atoi(args[2])
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Aval = Aval - X
	Bval = Bval + X
	fmt.Printf("Aval = %d, Bval = %d\n", Aval, Bval)

	// Write the state back to the ledger
	err = stub.PutState(A, []byte(strconv.Itoa(Aval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.Itoa(Bval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}
```

## Query

```go
// query callback representing the query of a chaincode
func (t *SimpleChaincode) query(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var A string // Entities
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to query")
	}

	A = args[0]

	// Get the state from the ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	if Avalbytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := "{\"Name\":\"" + A + "\",\"Amount\":\"" + string(Avalbytes) + "\"}"
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Avalbytes)
}
```
