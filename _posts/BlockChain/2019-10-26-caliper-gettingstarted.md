---
title : Hyperledger Caliper Getting Started
tags :
- Getting Started
- Hyperledger Caliper
- Benchmark
- BlockChain
---

# Settings

Vagrant 파일 조작이랑 명령어는 [Hyperledger Fabric Network 구성 -1-](/fabricnetwork1) 부분과 동일하니 똑같이 진행하시면 됩니다.

`Caliper`에서는 아래 파일을 사용하겠습니다. 위 포스트와는 다르게 코어와 메모리를 늘렸습니다.

> Vagrantfile 

```
ENV["LC_ALL"] = "en_US.UTF-8"

Vagrant.configure("2") do |config|
  vm_num = 1
  node_cpu = 2 # 2Core
  node_memory = "4096" # 4G Memory
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

# HandsOn

정말 까다로웠습니다. 순서가 잘못되어도 오류가 날 수 있으니 똑같이 따라해주세요. 기본적인 셋팅은 비슷합니다.

## Install Docker

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ apt-get update
$ apt-get -y install docker-ce
$ usermod -aG docker vagrant
```

## Install Docker Compose

```
$ curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
$ echo "PATH=$PATH:/usr/local/go/bin" >> /etc/profile
```

## Install Nodejs 8

```
$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
$ sudo apt-get install -y nodejs
```

## Install following tool(g++, make, python2)
```
$ sudo apt install g++
$ sudo apt-get install make
$ sudo apt-get install python2.7 

$ git clone https://github.com/hyperledger/caliper.git
```

## Install @hyperledger/caliper-cli

```
$ npm install -g npx
$ npm install -g node-gyp

$ cd caliper/packages/caliper-samples

vagrant@caliper-1:~/caliper/packages/caliper-samples$ ls
benchmark network  package.json  package-lock.json  README.md  src

$ npm init -y

$ npm install --only=prod @hyperledger/caliper-cli
$ npx caliper bind --caliper-bind-sut fabric --caliper-bind-sdk 1.4.0
```

이제 여기까지 문제 없이 되셨다면 당신은 fabric 성능 측정을 할 자격이 있는겁니다.

아래 명령어를 입력해서 2org 1peer leveldb 환경에서 성능 측정을 해보겠습니다.

```
$ npx caliper benchmark run --caliper-workspace . --caliper-benchconfig benchmark/simple/config.yaml --caliper-networkconfig network/fabric-v1.4/2org1peergoleveldb/fabric-go.yaml
```

성능 측정이 끝나고나면 해당 디렉토리에 html 파일이 생깁니다. 그 파일은 아래처럼 나오게 됩니다.


![image](https://user-images.githubusercontent.com/44635266/67596778-7e77fa00-f7a4-11e9-9287-6e994b7ed172.png)


아래는 성능 측정시 나오는 로그 입니다. 참고로 확인하시면 될거같아요. 저는 오류가 좀 있내요.

포스트에는 담지 않았지만 저는 `3org2peergoleveldb`와 `2org1peergoleveldb`를 돌려봤는데요. 두 파일 모두 별다른 차이는 없었습니다.


끝나고 나니 정말 눈물이 나네요.... 순서만 틀려도 정말 너무 많은 오류가 발생해서 몇번을 날려먹었는지.. 그래도 포스트 마치고 나니 보람은 있내요

> Fabric-v1.4 2 Org 1 Peer Level DB

```
Benchmark for target Blockchain type fabric about to start
info: [caliper-flow]: ####### Caliper Test #######
info: [caliper-utils]: Executing command: cd /home/vagrant/caliper/packages/caliper-samples;docker-compose -f network/fabric-v1.4/2org1peergoleveldb/docker-compose.yaml up -d;sleep 3s
Creating network "2org1peergoleveldb_default" with the default driver
Pulling ca.org1.example.com (hyperledger/fabric-ca:1.4.0)...
1.4.0: Pulling from hyperledger/fabric-ca
Digest: sha256:c1dce534d9e9202697e0aaad7c5521d958700fda0b05127dafb9333c22e15f74
Status: Downloaded newer image for hyperledger/fabric-ca:1.4.0
Pulling orderer.example.com (hyperledger/fabric-orderer:1.4.0)...
1.4.0: Pulling from hyperledger/fabric-orderer
Digest: sha256:644265186b4887c7d9dcb91895124ccead3c0125c2c4f9eadc421dc9555d7495
Status: Downloaded newer image for hyperledger/fabric-orderer:1.4.0
Pulling peer0.org1.example.com (hyperledger/fabric-peer:1.4.0)...
1.4.0: Pulling from hyperledger/fabric-peer
Digest: sha256:9707c97f787de1d4d6dd60994d6b8ea2e5cc28b0f42e6849df3fb41c64b41372
Status: Downloaded newer image for hyperledger/fabric-peer:1.4.0
Creating ca.org2.example.com ... done
Creating ca.org1.example.com ... done
Creating orderer.example.com ... done
Creating peer0.org2.example.com ... done
Creating peer0.org1.example.com ... done
info: [adapters/fabric]: Fabric SDK version: 1.4.0; TLS: none
info: [adapters/fabric]: Org1's registrar enrolled successfully
info: [adapters/fabric]: Org2's registrar enrolled successfully
info: [adapters/fabric]: Org1's admin's materials are successfully loaded
info: [adapters/fabric]: Org2's admin's materials are successfully loaded
info: [adapters/fabric]: client0.org1.example.com's materials are successfully loaded
info: [adapters/fabric]: client0.org2.example.com's materials are successfully loaded
info: [adapters/fabric]: Channel 'mychannel' definiton being retrieved from file
info: [adapters/fabric]: Channel 'mychannel' successfully created
info: [adapters/fabric]: Sleeping 5s...
info: [adapters/fabric]: Org1's peers successfully joined mychannel: peer0.org1.example.com
info: [adapters/fabric]: Org2's peers successfully joined mychannel: peer0.org2.example.com
info: [adapters/fabric]: Sleeping 5s...
info: [adapters/fabric]: Installing chaincodes for mychannel...
info: [adapters/fabric]: marbles@v0 successfully installed on Org1's peers: peer0.org1.example.com
info: [adapters/fabric]: marbles@v0 successfully installed on Org2's peers: peer0.org2.example.com
info: [adapters/fabric]: drm@v0 successfully installed on Org1's peers: peer0.org1.example.com
info: [adapters/fabric]: drm@v0 successfully installed on Org2's peers: peer0.org2.example.com
info: [adapters/fabric]: simple@v0 successfully installed on Org1's peers: peer0.org1.example.com
info: [adapters/fabric]: simple@v0 successfully installed on Org2's peers: peer0.org2.example.com
info: [adapters/fabric]: smallbank@v0 successfully installed on Org1's peers: peer0.org1.example.com
info: [adapters/fabric]: smallbank@v0 successfully installed on Org2's peers: peer0.org2.example.com
info: [adapters/fabric]: Instantiating marbles@v0 in mychannel. This might take some time...
info: [adapters/fabric]: Successfully instantiated marbles@v0 in mychannel
info: [adapters/fabric]: Instantiating drm@v0 in mychannel. This might take some time...
info: [adapters/fabric]: Successfully instantiated drm@v0 in mychannel
info: [adapters/fabric]: Instantiating simple@v0 in mychannel. This might take some time...
info: [adapters/fabric]: Successfully instantiated simple@v0 in mychannel
info: [adapters/fabric]: Instantiating smallbank@v0 in mychannel. This might take some time...
info: [adapters/fabric]: Successfully instantiated smallbank@v0 in mychannel
info: [adapters/fabric]: Sleeping 5s...
info: [caliper-flow]: Started monitor successfully
info: [defaultTest]: ####### Testing 'open' #######
info: [defaultTest]: ------ Test round 1 ------
info: [client-util.js]: Launching client with PID  22838
info: [client-util.js]: Waiting for 1 clients to be ready...
info: [demo.js]: [Transaction Info] - Submitted: 0 Succ: 0 Fail:0 Unfinished:0
info: [client-util.js]: Client ready message recieved
info: [client-util.js]: 1 clients ready, starting test phase
info: [fabric/fabricClientWorker]: Client ready
info: [local-client.js]: txUpdateTime: 1000
info: [local-client.js]: Info: client 22838 start test runFixedNumber():opening accounts
info: [demo.js]: [Transaction Info] - Submitted: 0 Succ: 0 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 46 Succ: 40 Fail:0 Unfinished:6
info: [report-builder]: ###test result:###
info: [report-builder]:
+------+------+------+-----------+-------------+-------------+-------------+------------+
| Name | Succ | Fail | Send Rate | Max Latency | Min Latency | Avg Latency | Throughput |
|------|------|------|-----------|-------------|-------------|-------------|------------|
| open | 100  | 0    | 50.6 tps  | 0.30 s      | 0.03 s      | 0.16 s      | 49.8 tps   |
+------+------+------+-----------+-------------+-------------+-------------+------------+

info: [report-builder]: ### resource stats ###
info: [report-builder]:
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+
| TYPE    | NAME                              | Memory(max) | Memory(avg) | CPU(max) | CPU(avg) | Traffic In | Traffic Out | Disc Read | Disc Write |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Process | node local-client.js(avg)         | -           | -           | NaN%     | NaN%     | -          | -           | -         | -          |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...nk-v0 | 6.6MB       | 6.6MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...nk-v0 | 6.2MB       | 6.2MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...le-v0 | 5.9MB       | 5.9MB       | 1.13%    | 1.13%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...le-v0 | 6.3MB       | 6.3MB       | 0.90%    | 0.90%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...rm-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...rm-v0 | 6.4MB       | 6.4MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...es-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...es-v0 | 5.9MB       | 5.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org1.example.com            | 171.0MB     | 171.0MB     | 6.31%    | 6.31%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org2.example.com            | 199.4MB     | 199.4MB     | 5.03%    | 5.03%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | orderer.example.com               | 8.0MB       | 8.0MB       | 1.25%    | 1.25%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org1.example.com               | 6.9MB       | 6.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org2.example.com               | 8.0MB       | 8.0MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+

info: [defaultTest]: ------ Passed 'open' testing ------
info: [defaultTest]: Waiting 5 seconds for the next round...
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [defaultTest]: ####### Testing 'query' #######
info: [defaultTest]: ------ Test round 2 ------
info: [client-util.js]: Waiting for 0 clients to be ready...
info: [client-util.js]: 0 clients ready, starting test phase
info: [local-client.js]: txUpdateTime: 1000
info: [local-client.js]: Info: client 22838 start test runFixedNumber():querying accounts
info: [demo.js]: [Transaction Info] - Submitted: 100 Succ: 100 Fail:0 Unfinished:0
info: [report-builder]: ###test result:###
info: [report-builder]:
+-------+------+------+-----------+-------------+-------------+-------------+------------+
| Name  | Succ | Fail | Send Rate | Max Latency | Min Latency | Avg Latency | Throughput |
|-------|------|------|-----------|-------------|-------------|-------------|------------|
| query | 100  | 0    | 101.0 tps | 0.06 s      | 0.01 s      | 0.02 s      | 100.2 tps  |
+-------+------+------+-----------+-------------+-------------+-------------+------------+

info: [report-builder]: ### resource stats ###
info: [report-builder]:
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+
| TYPE    | NAME                              | Memory(max) | Memory(avg) | CPU(max) | CPU(avg) | Traffic In | Traffic Out | Disc Read | Disc Write |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Process | node local-client.js(avg)         | -           | -           | NaN%     | NaN%     | -          | -           | -         | -          |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...nk-v0 | 6.6MB       | 6.6MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...nk-v0 | 6.2MB       | 6.2MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...le-v0 | 5.9MB       | 5.9MB       | 2.36%    | 2.36%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...le-v0 | 6.4MB       | 6.4MB       | 2.19%    | 2.19%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...rm-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...rm-v0 | 6.4MB       | 6.4MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...es-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...es-v0 | 5.9MB       | 5.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org1.example.com            | 198.9MB     | 198.9MB     | 8.30%    | 8.30%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org2.example.com            | 200.5MB     | 200.5MB     | 7.54%    | 7.54%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | orderer.example.com               | 11.3MB      | 11.3MB      | 0.01%    | 0.01%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org1.example.com               | 6.9MB       | 6.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org2.example.com               | 8.0MB       | 8.0MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+

info: [defaultTest]: ------ Passed 'query' testing ------
info: [defaultTest]: Waiting 5 seconds for the next round...
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
info: [defaultTest]: ####### Testing 'transfer' #######
info: [defaultTest]: ------ Test round 3 ------
info: [client-util.js]: Waiting for 0 clients to be ready...
info: [client-util.js]: 0 clients ready, starting test phase
info: [local-client.js]: txUpdateTime: 1000
info: [local-client.js]: Info: client 22838 start test runFixedNumber():transfering money
info: [demo.js]: [Transaction Info] - Submitted: 200 Succ: 200 Fail:0 Unfinished:0
error: [adapters/fabric]: Transaction[5bab4fbf08] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[edf7b2a1b8] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[38632f2903] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[859863d540] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
2019-10-24T18:57:29.545Z - error: [Channel.js]: compareProposalResponseResults - read/writes result sets do not match index=1
error: [adapters/fabric]: Transaction[35f9f06599] life-cycle errors:
	- Read/Write set mismatch between endorsements
error: [adapters/fabric]: Transaction[cc24927389] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[106e8b42f2] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[727bef81fb] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
info: [demo.js]: [Transaction Info] - Submitted: 246 Succ: 234 Fail:7 Unfinished:5
2019-10-24T18:57:29.934Z - error: [Channel.js]: compareProposalResponseResults - read/writes result sets do not match index=1
error: [adapters/fabric]: Transaction[6595c265e2] life-cycle errors:
	- Read/Write set mismatch between endorsements
error: [adapters/fabric]: Transaction[88deb3c609] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[92466518cb] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[49b2ee5b50] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
2019-10-24T18:57:30.349Z - error: [Channel.js]: compareProposalResponseResults - read/writes result sets do not match index=1
error: [adapters/fabric]: Transaction[72e2a0fd8a] life-cycle errors:
	- Read/Write set mismatch between endorsements
error: [adapters/fabric]: Transaction[77a7a90d3a] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
error: [adapters/fabric]: Transaction[be7a170345] commit errors:
	- Commit error on peer0.org1.example.com with code MVCC_READ_CONFLICT
	- Commit error on peer0.org2.example.com with code MVCC_READ_CONFLICT
info: [demo.js]: [Transaction Info] - Submitted: 296 Succ: 278 Fail:15 Unfinished:3
info: [report-builder]: ###test result:###
info: [report-builder]:
+----------+------+------+-----------+-------------+-------------+-------------+------------+
| Name     | Succ | Fail | Send Rate | Max Latency | Min Latency | Avg Latency | Throughput |
|----------|------|------|-----------|-------------|-------------|-------------|------------|
| transfer | 85   | 15   | 50.6 tps  | 0.28 s      | 0.04 s      | 0.15 s      | 39.7 tps   |
+----------+------+------+-----------+-------------+-------------+-------------+------------+

info: [report-builder]: ### resource stats ###
info: [report-builder]:
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+
| TYPE    | NAME                              | Memory(max) | Memory(avg) | CPU(max) | CPU(avg) | Traffic In | Traffic Out | Disc Read | Disc Write |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Process | node local-client.js(avg)         | -           | -           | NaN%     | NaN%     | -          | -           | -         | -          |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...nk-v0 | 6.6MB       | 6.6MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...nk-v0 | 6.2MB       | 6.2MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...le-v0 | 5.9MB       | 5.9MB       | 6.65%    | 6.65%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...le-v0 | 6.4MB       | 6.4MB       | 6.57%    | 6.57%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...rm-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...rm-v0 | 6.4MB       | 6.4MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...es-v0 | 6.1MB       | 6.1MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...es-v0 | 5.9MB       | 5.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org1.example.com            | 201.6MB     | 201.6MB     | 21.81%   | 21.81%   | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org2.example.com            | 201.0MB     | 201.0MB     | 22.14%   | 22.14%   | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | orderer.example.com               | 12.1MB      | 12.1MB      | 7.00%    | 7.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org1.example.com               | 6.9MB       | 6.9MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|-------------|----------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org2.example.com               | 8.0MB       | 8.0MB       | 0.00%    | 0.00%    | 0B         | 0B          | 0B        | 0B         |
+---------+-----------------------------------+-------------+-------------+----------+----------+------------+-------------+-----------+------------+

info: [defaultTest]: ------ Passed 'transfer' testing ------
info: [caliper-flow]: ---------- Finished Test ----------

info: [report-builder]: ###all test results:###
info: [report-builder]:
+------+----------+------+------+-----------+-------------+-------------+-------------+------------+
| Test | Name     | Succ | Fail | Send Rate | Max Latency | Min Latency | Avg Latency | Throughput |
|------|----------|------|------|-----------|-------------|-------------|-------------|------------|
| 1    | open     | 100  | 0    | 50.6 tps  | 0.30 s      | 0.03 s      | 0.16 s      | 49.8 tps   |
|------|----------|------|------|-----------|-------------|-------------|-------------|------------|
| 2    | query    | 100  | 0    | 101.0 tps | 0.06 s      | 0.01 s      | 0.02 s      | 100.2 tps  |
|------|----------|------|------|-----------|-------------|-------------|-------------|------------|
| 3    | transfer | 85   | 15   | 50.6 tps  | 0.28 s      | 0.04 s      | 0.15 s      | 39.7 tps   |
+------+----------+------+------+-----------+-------------+-------------+-------------+------------+

info: [monitor.js]:
 ### resource stats (maximum) ###
info: [monitor.js]:
+---------+-----------------------------------+-------------+----------+------------+-------------+-----------+------------+
| TYPE    | NAME                              | Memory(max) | CPU(max) | Traffic In | Traffic Out | Disc Read | Disc Write |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Process | node local-client.js(avg)         | -           | NaN%     | -          | -           | -         | -          |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...nk-v0 | 6.6MB       | 0.00%    | 70B        | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...nk-v0 | 6.2MB       | 0.00%    | 70B        | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...le-v0 | 5.9MB       | 6.65%    | 146.6KB    | 64.3KB      | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...le-v0 | 6.4MB       | 6.57%    | 149.9KB    | 64.6KB      | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...rm-v0 | 6.1MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...rm-v0 | 6.4MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org2.example.co...es-v0 | 6.1MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | dev-peer0.org1.example.co...es-v0 | 5.9MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org1.example.com            | 201.6MB     | 21.81%   | 482.9KB    | 246.5KB     | 0B        | 532.0KB    |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | peer0.org2.example.com            | 201.0MB     | 22.14%   | 529.5KB    | 260.8KB     | 0B        | 596.0KB    |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | orderer.example.com               | 12.1MB      | 7.00%    | 363.4KB    | 740.7KB     | 232.0KB   | 424.0KB    |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org1.example.com               | 6.9MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
|---------|-----------------------------------|-------------|----------|------------|-------------|-----------|------------|
| Docker  | ca.org2.example.com               | 8.0MB       | 0.00%    | 0B         | 0B          | 0B        | 0B         |
+---------+-----------------------------------+-------------+----------+------------+-------------+-----------+------------+

info: [caliper-flow]: Generated report with path /home/vagrant/caliper/packages/caliper-samples/report-20191024T185731.html
info: [demo.js]: [Transaction Info] - Submitted: 300 Succ: 285 Fail:15 Unfinished:0
info: [caliper-flow]:

#######################################
# Test summary: 3 succeeded, 0 failed #
#######################################

info: [caliper-utils]: Executing command: cd /home/vagrant/caliper/packages/caliper-samples;docker-compose -f network/fabric-v1.4/2org1peergoleveldb/docker-compose.yaml down;(test -z \"$(docker ps -aq)\") || docker rm $(docker ps -aq);(test -z \"$(docker images dev* -q)\") || docker rmi $(docker images dev* -q);rm -rf /tmp/hfc-*
info: [client-util.js]: Client exited with code null
Stopping peer0.org1.example.com ... done
Stopping peer0.org2.example.com ... done
Stopping orderer.example.com    ... done
Stopping ca.org1.example.com    ... done
Stopping ca.org2.example.com    ... done
Removing peer0.org1.example.com ... done
Removing peer0.org2.example.com ... done
Removing orderer.example.com    ... done
Removing ca.org1.example.com    ... done
Removing ca.org2.example.com    ... done
Removing network 2org1peergoleveldb_default
/bin/sh: 1: test: "c24816493846: unexpected operator
c24816493846
240823eeeab4
dd89baedfc0f
c05c9afb6b2a
0e1ff0e94347
6bd51dac5c2b
4f267c5cdd0e
5b12d0a8148b
/bin/sh: 1: test: "04c878d2ff7e: unexpected operator
Untagged: dev-peer0.org1.example.com-smallbank-v0-b1f07dc4b6d8079c04183f3e9c828770349d6c0fd5ce55d82a7782925b2ce03a:latest
Deleted: sha256:04c878d2ff7ecbc08ed72aa1555ef05a48c634cd49ce2dd61497ede32b053325
Deleted: sha256:772a486cbaa0fe4b88bdd60d6459606ff2074265324358734e7af38d07e4e2ba
Deleted: sha256:157a52735f210436c05cb74377c080698874f599d04faf030fc384dfcc66042a
Deleted: sha256:d3b8e1d2f699a6055012a8f690d7781c5bac75aff9360893417f397b7345b4bb
Untagged: dev-peer0.org2.example.com-smallbank-v0-f8b95020f1a3b8371f7c58e1af1ff3d9fe0d4b26389373fa678955579a772c8f:latest
Deleted: sha256:b83ebba3430f24cc03e7c617176c0f4602101f88fa34f9067c36d3b8eb33a4fa
Deleted: sha256:ab092da0111c2f10c89957ef3548d4dc78095e6be0b28335226efb90c1dd41c2
Deleted: sha256:61b39269db68453e928846a81162e8620d1fa976024f395df2a46c0974d35093
Deleted: sha256:5b168e89a85808c278a02deec737b85c15a60e1d840c49e29b7255b2806928b8
Untagged: dev-peer0.org2.example.com-simple-v0-7ebccf7a7fd05d8ac0a55ea61f1f0397ca89de629cef5f537c0950ecf302d423:latest
Deleted: sha256:bdba6d10c7b2ab1316680ca7863c6aa0357f1b899f47988cc113d6e10fffc5ee
Deleted: sha256:6da2a47286c58fb051ed4564d7178f3a92d3e4fff1fe23bcaddf0d1a938be6d8
Deleted: sha256:1fafdbf4d42eb64bcbd3ed89ea40d7bfc30885aaeb94323ccc4a9a5ce573d3fa
Deleted: sha256:18541457d6159bda47d2f6452fd1841e678577dbddfdc418fe0588d0022ec679
Untagged: dev-peer0.org1.example.com-simple-v0-b845a7f88df0bd3a47a573b80bd5cfab0986278f024e8667a3c90fb0eb1f4d6d:latest
Deleted: sha256:10d68d008ecec36f6b4e0d7c563126c06730ec7d690deb50c27594025a3cabca
Deleted: sha256:10b1306225ef9cfa14f4041ef561352f23a93f4071b20848a2bc71a26914e43f
Deleted: sha256:e2cc7078ad16a148b9cb454938627fa6cbd6bd2ba8c4b2c95d78828b8c2875ca
Deleted: sha256:03e85b1f202a69c917aaeb789ca606a375458eeeb07df6331e938bc81f6b3a3c
Untagged: dev-peer0.org2.example.com-drm-v0-c25cb5f64ec9f30764df0f6b930f1f3bc7b96f88da333c49c4c6779ac65a4552:latest
Deleted: sha256:7060048b38c7cc4015ff28e7ea6a1189791fc44b7fcec34fb6a6a6b92be2253f
Deleted: sha256:e5b0cb34b243c04b7e0d9745c9032f60ef7593a8df0e79eb9b77e7bc24f04e6a
Deleted: sha256:8d57016fbf29e723173e273df1d059c8517dd8a50eacf20f9376eab10c248a35
Deleted: sha256:ff540395e7fb5b2afbf099357fe06ba41971e3e4fc09389add90793f0c47c2b3
Untagged: dev-peer0.org1.example.com-drm-v0-08a16fdaf3af53efb6b99e3c2ec4de9aa78e4d592b4582fc4aa4709c1f3b13cb:latest
Deleted: sha256:9aadffffdfb7b9a7d4703d0c0f36015765ec73a653d73a9293181204e1e24eea
Deleted: sha256:a346f594975e76bf152d1afc9af66cab918695819ef0e070851640d28f1a1e91
Deleted: sha256:600aebc82bdd1e8dbd9bb6544589279af5bf66bed996ab29a602f4cfd6ddc9fd
Deleted: sha256:06384cb4d709b667d936bf66af11ab5c4808ea07c1cc9f2afa3fff5b87dd3a49
Untagged: dev-peer0.org2.example.com-marbles-v0-82ec74ea3ac84a8926b1d7d3d256a2e2f41b74928c28cf4bcdbb5a7774a90f87:latest
Deleted: sha256:e65ab314b96329b13f964c39ddf8db03ced6e1de1640fb3d2a953b19fe95de1f
Deleted: sha256:ff851ae4d93b7021490f8703c6cf3ddcb7fe05c24661bb3969463e2ea484ac83
Deleted: sha256:6b55dc5878281f64b4ca314f3bdb3758aad3de0553f432fb279f1647129134a3
Deleted: sha256:2c62683f8dd2a15cca17aac30fa1f70cbe032afa2c2a8337975e2e2a48672ed1
Untagged: dev-peer0.org1.example.com-marbles-v0-d970bb5377683adf108a269e3670f7f9cbb849f3eff58fe19595ea3374a52ea0:latest
Deleted: sha256:1bfac54535c650395afd5080e2c01415b725d096af1f4b00d3b4505c478d0e22
Deleted: sha256:395ecb4fec1f22a5e31087b589402bdf4592dc6d094f1604e9e4fe388e5dd83c
Deleted: sha256:bbd224abe28b1b285b7f076fc9fddf58f3cb83023a817daceed00bcff39f380a
Deleted: sha256:608b3dac9caa882b6f650f493b5df17d27c893e5dcad1067ce61b76e429c0f85
Benchmark run successful

Command succeeded
```
