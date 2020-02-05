---
title : Hyperledger Indy Getting Started
tags :
- Indy
- Hyperledger
- Getting Started
- BlockChain
---

*이 포스트는 `Hyperledger Korea User Group`에서 만든 글을 바탕으로 만들었습니다.*

# Settings

## Hyperledger Indy - Getting Started 환경 구성하기

### Version

```
$ vagrant -v
Vagrant 2.2.5

VirtualBox 버전 6.0.10 r132072 (Qt5.6.3)
```

본 포스트에서는 Hyperledger Indy SDK 1.11.x 의 Getting Started 설치를 대상으로 설명합니다.

아래는 1Core, 2G 메모리 VM 한개를 생성하는 샘플 Vagrantfile입니다.(Hyperledger Indy SDI 1.11.x)

> Vagrantfile

```
ENV["LC_ALL"] = "en_US.UTF-8"

Vagrant.configure("2") do |config|
  vm_num = 1
  node_cpu = 1 # 1Core
  node_memory = "2048" # 2G Memory
  node_network = "10.30.30"
  node_prefix = "indy"
  
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

  config.vm.provision "shell", inline: <<-EOF
        cd /etc/apt
        mv sources.list sources.list-
        wget https://raw.githubusercontent.com/hlkug/meetup/master/000000/ubuntu/16.04/sources.list
        cp sources.list /tmp

    	apt-get update
      	apt-get upgrade

    	# Install Go
    	wget https://dl.google.com/go/go1.12.10.linux-amd64.tar.gz
        tar zxf go1.12.10.linux-amd64.tar.gz
        mv go /usr/local
        rm go1.12.10.linux-amd64.tar.gz

    	# Install Docker
        apt-get -y install apt-transport-https ca-certificates curl software-properties-common
    	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    	add-apt-repository \
    	   "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    	apt-get update
    	apt-get -y install docker-ce
        usermod -aG docker vagrant

    	# Install Docker Compose
    	curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    	chmod +x /usr/local/bin/docker-compose
        echo "PATH=$PATH:/usr/local/go/bin" >> /etc/profile

	# Install Indy
        cd /home/vagrant
        git clone -b v1.11.1 https://github.com/hyperledger/indy-sdk.git

        cd indy-sdk/ci
        cp /tmp/sources.list .
        sed -i -e 's/1.9.2~dev871/1.10.0~dev916/g' \
            -e 's/1.9.2~dev1061/1.10.0~dev1095/g' \
            -e 's/127.0.0.1/10.0.0.2/g' indy-pool.dockerfile

        sed -i '2i COPY sources.list /etc/apt' indy-pool.dockerfile
        sed -i '3i RUN ln -s /usr/lib/apt/methods/http /usr/lib/apt/methods/https' indy-pool.dockerfile
        docker build -t indy_pool -f indy-pool.dockerfile .

        cd /home/vagrant/indy-sdk/docs/getting-started
        cp /tmp/sources.list .
        sed -i '2i COPY sources.list /etc/apt' getting-started.dockerfile
        sed -i '3i RUN ln -s /usr/lib/apt/methods/http /usr/lib/apt/methods/https' getting-started.dockerfile
        docker build -t getting-started -f getting-started.dockerfile .
        chown -R vagrant:vagrant /home/vagrant/indy-sdk
  EOF
end
```

### 1. VM 생성 / 재시작

```
$ vagrant up indy-1

==> vagrant: A new version of Vagrant is available: 2.2.6 (installed version: 2.2.5)!
==> vagrant: To upgrade visit: https://www.vagrantup.com/downloads.html

Bringing machine 'indy-1' up with 'virtualbox' provider...
==> indy-1: Importing base box 'ubuntu/xenial64'...
==> indy-1: Matching MAC address for NAT networking...
==> indy-1: Setting the name of the VM: indy-1
==> indy-1: Clearing any previously set network interfaces...
==> indy-1: Preparing network interfaces based on configuration...
    indy-1: Adapter 1: nat
    indy-1: Adapter 2: hostonly
==> indy-1: Forwarding ports...
    indy-1: 22 (guest) => 2222 (host) (adapter 1)
==> indy-1: Running 'pre-boot' VM customizations...
==> indy-1: Booting VM...
==> indy-1: Waiting for machine to boot. This may take a few minutes...
    indy-1: SSH address: 127.0.0.1:2222
    indy-1: SSH username: vagrant
    indy-1: SSH auth method: private key
    indy-1:
    indy-1: Vagrant insecure key detected. Vagrant will automatically replace
    indy-1: this with a newly generated keypair for better security.
    indy-1:
    indy-1: Inserting generated public key within guest...
    indy-1: Removing insecure key from the guest if it's present...
    indy-1: Key inserted! Disconnecting and reconnecting using new SSH key...
==> indy-1: Machine booted and ready!
==> indy-1: Checking for guest additions in VM...
    indy-1: The guest additions on this VM do not match the installed version of
    indy-1: VirtualBox! In most cases this is fine, but in rare cases it can
    indy-1: prevent things such as shared folders from working properly. If you see
    indy-1: shared folder errors, please make sure the guest additions within the
    indy-1: virtual machine match the version of VirtualBox you have installed on
    indy-1: your host and reload your VM.
    indy-1:
    indy-1: Guest Additions Version: 5.1.38
    indy-1: VirtualBox Version: 6.0
==> indy-1: Setting hostname...
==> indy-1: Configuring and enabling network interfaces...
==> indy-1: Mounting shared folders...
    indy-1: /vagrant => /Users/has3ong/Desktop/indy
==> indy-1: Running provisioner: shell...
    indy-1: Running: inline script
```

### 2. VM 접속

```
$ vagrant ssh indy-1

Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-159-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

52 packages can be updated.
21 updates are security updates.

New release '18.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


vagrant@indy-1:~$
```

### 3. VM 중지

```
$ vagrant halt indy-1
==> indy-1: Attempting graceful shutdown of VM...
```

### 4. VM 삭제

```
$ vagrant destroy indy-1
    indy-1: Are you sure you want to destroy the 'indy-1' VM? [y/N] y
==> indy-1: Destroying VM and associated drives...
```

# HandsOn

## 1. VM 접속 실습파일 다운로드 및 적용

### 1.1 VM 접속

```
$ vagrant status
Current machine states:

indy-1                    poweroff (virtualbox)

The VM is powered off. To restart the VM, simply run `vagrant up`

$ vagrant up
Bringing machine 'indy-1' up with 'virtualbox' provider...
==> indy-1: Clearing any previously set forwarded ports...
==> indy-1: Clearing any previously set network interfaces...
==> indy-1: Preparing network interfaces based on configuration...
    indy-1: Adapter 1: nat
    indy-1: Adapter 2: hostonly
==> indy-1: Forwarding ports...
    indy-1: 22 (guest) => 2222 (host) (adapter 1)
==> indy-1: Running 'pre-boot' VM customizations...
==> indy-1: Booting VM...
==> indy-1: Waiting for machine to boot. This may take a few minutes...
    indy-1: SSH address: 127.0.0.1:2222
    indy-1: SSH username: vagrant
    indy-1: SSH auth method: private key
==> indy-1: Machine booted and ready!
==> indy-1: Checking for guest additions in VM...
    indy-1: The guest additions on this VM do not match the installed version of
    indy-1: VirtualBox! In most cases this is fine, but in rare cases it can
    indy-1: prevent things such as shared folders from working properly. If you see
    indy-1: shared folder errors, please make sure the guest additions within the
    indy-1: virtual machine match the version of VirtualBox you have installed on
    indy-1: your host and reload your VM.
    indy-1:
    indy-1: Guest Additions Version: 5.1.38
    indy-1: VirtualBox Version: 6.0
==> indy-1: Setting hostname...
==> indy-1: Configuring and enabling network interfaces...
==> indy-1: Mounting shared folders...
    indy-1: /vagrant => /Users/yunho.chung/Vagrant/indy
==> indy-1: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> indy-1: flag to force provisioning. Provisioners marked to run always will still run.

$ vagrant status
Current machine states:

indy-1                    running (virtualbox)

The VM is running. To stop this VM, you can run `vagrant halt` to
shut it down forcefully, or you can run `vagrant suspend` to simply
suspend the virtual machine. In either case, to restart it again,
simply run `vagrant up`.

$ vagrant ssh indy-1
```

### 1.2 실습파일 다운로드 및 적용

```
vagrant@indy-1:~$ git clone http://github.com/hlkug/meetup


Cloning into 'meetup'...
remote: Enumerating objects: 85, done.
remote: Counting objects: 100% (85/85), done.
remote: Compressing objects: 100% (54/54), done.
Receiving objects:  12% (74/588), 55.14 MiB | 8.72 MiB/s

Receiving objects: 100% (588/588), 70.48 MiB | 9.08 MiB/s, done.
Resolving deltas: 100% (178/178), done.
Checking connectivity... done.


vagrant@indy-1:~$ cd meetup/201910/vagrant/
vagrant@indy-1:~/meetup/201910/vagrant$ ls
docker-compose.yml  getting-started_by_hlkug.ipynb

# docker-compose.yml, getting-started_by_hlkug.ipynb 파일 복사
vagrant@indy-1:~/meetup/201910/vagrant$ cp * /home/vagrant/indy-sdk/docs/getting-started
```

## 2. Getting Started 예제 구동

### 2.1 IP 확인

Host에서 VM에 접속하기 위해 VM의 IP를 확인합니다.

아래 처럼 enp0s8 인터페이스에 10.30.30.2 주소가 할당된 것을 확인하면 됩니다.

```
vagrant@indy-1:~$ ip a

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:49:b7:a9:fe:dc brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::49:b7ff:fea9:fedc/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:f8:20:21 brd ff:ff:ff:ff:ff:ff
    inet 10.30.30.2/24 brd 10.30.30.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fef8:2021/64 scope link
       valid_lft forever preferred_lft forever
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:96:f2:07:99 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:96ff:fef2:799/64 scope link
       valid_lft forever preferred_lft forever
15: br-4508b0dbadaa: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:12:bb:a3:38 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.1/24 brd 10.0.0.255 scope global br-4508b0dbadaa
       valid_lft forever preferred_lft forever
    inet6 fe80::42:12ff:febb:a338/64 scope link
       valid_lft forever preferred_lft forever
39: veth5faf222@if38: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-4508b0dbadaa state UP group default
    link/ether f2:0f:30:28:6b:cd brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::f00f:30ff:fe28:6bcd/64 scope link
       valid_lft forever preferred_lft forever
41: vethe618648@if40: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-4508b0dbadaa state UP group default
    link/ether aa:76:de:d9:aa:60 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::a876:deff:fed9:aa60/64 scope link
       valid_lft forever preferred_lft forever
```

### 2.2 Docker Compose 구동

"Getting Started" 예제를 위해 두개의 컨테이너가 제공 됩니다.

* indy_pool - Hyperledger Indy Network 컨테이너, Indy Pool
* getting_started - Jupyter Notebook 컨테이너, 제공되는 Python 코드 예제 실습

```
# "Getting Started" 관련 파일은 Indy SDK 내 /docs/getting-started 폴더에 있습니다.
vagrant@indy-1:~$ cd /home/vagrant/indy-sdk/docs/getting-started
vagrant@indy-1:~/indy-sdk/docs/getting-started$ ls

# Docker Compose 구동
vagrant@indy-1:~/indy-sdk/docs/getting-started$ docker-compose up
vagrant@indy-1:~/indy-sdk/docs/getting-started$ docker-compose up

Creating indy_pool ... done
Creating getting_started ... done
Attaching to indy_pool, getting_started
indy_pool    | 2019-10-17 17:25:20,255 CRIT Set uid to user 1000
getting_started | [I 17:25:21.159 NotebookApp] Writing notebook server cookie secret to /home/indy/.local/share/jupyter/runtime/notebook_cookie_secret
getting_started | [I 17:25:21.553 NotebookApp] Serving notebooks from local directory: /home/indy
getting_started | [I 17:25:21.553 NotebookApp] The Jupyter Notebook is running at:
getting_started | [I 17:25:21.554 NotebookApp] http://bcd14c338e06:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459
getting_started | [I 17:25:21.555 NotebookApp]  or http://127.0.0.1:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459
getting_started | [I 17:25:21.555 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
getting_started | [W 17:25:21.561 NotebookApp] No web browser found: could not locate runnable browser.
getting_started | [C 17:25:21.566 NotebookApp]
getting_started |
getting_started |     To access the notebook, open this file in a browser:
getting_started |         file:///home/indy/.local/share/jupyter/runtime/nbserver-1-open.html
getting_started |     Or copy and paste one of these URLs:
getting_started |         http://bcd14c338e06:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459
getting_started |      or http://127.0.0.1:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459
```

### 2.3 Jupyter Notebook 구동

Docker Compose 구동 후 출력되는 로그에서 URL을 복사해서 127.0.0.1 부분을 VM IP로 변경한 후 Host에서 웹브라우저(크롬)으로 접속합니다. 아래 토큰 값은 컨테이너(getting_started) 구동 시 임의의 값으로 변경되는 값입니다.

http://127.0.0.1:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459

--> http://10.30.30.2:8888/?token=a6be01baa780e898649b0394a524d9f95b82d0ab16d61459

![](https://user-images.githubusercontent.com/44635266/67033612-1d6f7700-f151-11e9-8064-27ff69506845.png)


## Hyperledger Indy Getting Started

### Overview

5개의 Actor가 있다. `Government`, `Faber College`, `Acme Corp`, `Thrift Bank`, `Alice` 첫 4개는 조직이며 `Alice`는 `Getting Started` 예제에서 그들과 교류한다.

`Government`는 스키마의 표준을 정하는 책임이 있다. 이는 모든 조직이 따를 수 있는 다양한 유형의 스키마 표준을 갖는 것이 더 바람직하기 때문에 이치에 맞는다. 이 예에서는 두 개의 스키마가 생성된다. `Transcript Schema` 및 `Job-Certificate Schema`.

`Alice`는 `Acme Corp`에 입사지원서를 내고 있다. `Acme Corp`는 입사지원서의 한 가지 요건으로서 교육수준의 증명을 요구한다. `Alice`가 `Faber College`을 졸업한 후, `Alice`가 보관하고 있는 자격증인 `Faber College`의 성적표를 먼저 적용하고 있다. 

`Faber College`는 `Government`의 `Transcript Schema`를 채택한다. `Acme Corporation`에서 그 직장에 지원할 때, 그녀는 `Acme Corp`에게 이 자격증명서를준다. `Acme Corp`는 이 자격증명서를 `Faber College`로부터 받은 자신의 교육수준의 증거로 받아들인다.

위 경우 아래와 같은 역할을 가지게된다.

* Alice: prover and credential holder
* Faber College: credential issuer
* Acme Corp: credential verifier

`Alice`는 `Thrift Bank`에서 자동차 대출을 신청하고 있다. `Thrift Bank`는 그녀의 고용 상태와 신분, 즉 KYC(Know Your Customer) 과정이라는 것을 증명해야 한다. `Alice`는 이제 `Acme Corp`의 취업증명서를 적용하고 있는데, 이것은 정부의 취업인증서 제도에 따라 다시 아크미사가 발행한 자격증명서다.

현재 `Alice`는 두 가지 자격증을 가지고 있다. 하나는 신분을 가진 `Faber College` 출신이고, 하나는 고용 상태에 대한 `Acme Corportaion` 션 출신이다. 그녀는 이 자격증을 자동차 대출 신청서에 제출한다.

위 경우 아래와 같은 역할을 가지게된다.

* Alice: prover and credential holder
* Faber College and Acme Bank: credential issuers
* Thrift Bank: credential verifier

저는 `Hyperledger Korea User Group`를 정리한 문서를 바탕으로 Alice가 Acme Corporation에 취업하는 과정까지 알아보겠습니다. 

### 1. 초기화

```
Getting started -> started
Open Pool Ledger: pool1
```

Hyperledger Indy에서는 다양한 default ledger가 존재합니다. 그중에서 pool 은 네트워크를 관리하는 ledger라고 보면 됩니다.

* pool ledger: transactions related to pool/network configuration (listing all nodes, their keys and addresses)
* config ledger: transactions for pool configuration plus transactions related to pool upgrade
* domain ledger: all main domain and application specific transactions (including NYM transactions for
DID)

pool_transactions_genesis

```
{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node1","blskey":"4N8aUNHSgjQVgkpm8nhNEfDf6txHznoYREg9kirmJrkivgL4oSEimFF6nsQ6M41QvhM2Z33nves5vfSn9n1UwNFJBYtWVnHYMATn76vLuL3zU88KyeAYcHfsih3He6UHcXDxcaecHVz6jhCYz1P2UZn2bDVruL5wXpehgBfBaLKm3Ba","blskey_pop":"RahHYiCvoNCtPTrVtP7nMC5eTYrsUA8WjXbdhNc8debh1agE9bGiJxWBXYNFbnJXoXhWFMvyqhqhRoq737YQemH5ik9oL7R4NTTCz2LEZhkgLJzB3QRQqJyBNyv7acbdHrAT8nQ9UkLbaVL9NBpnWXBTw4LEMePaSHEw66RzPNdAX1","client_ip":"10.0.0.2","client_port":9702,"node_ip":"10.0.0.2","node_port":9701,"services":["VALIDATOR"]},"dest":"Gw6pDLhcBcoQesN72qfotTgFa7cbuqZpkX3Xo6pLhPhv"},"metadata":{"from":"Th7MpTaRZVRYnPiabds81Y"},"type":"0"},"txnMetadata":{"seqNo":1,"txnId":"fea82e10e894419fe2bea7d96296a6d46f50f93f9eeda954ec461b2ed2950b62"},"ver":"1"}
{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node2","blskey":"37rAPpXVoxzKhz7d9gkUe52XuXryuLXoM6P6LbWDB7LSbG62Lsb33sfG7zqS8TK1MXwuCHj1FKNzVpsnafmqLG1vXN88rt38mNFs9TENzm4QHdBzsvCuoBnPH7rpYYDo9DZNJePaDvRvqJKByCabubJz3XXKbEeshzpz4Ma5QYpJqjk","blskey_pop":"Qr658mWZ2YC8JXGXwMDQTzuZCWF7NK9EwxphGmcBvCh6ybUuLxbG65nsX4JvD4SPNtkJ2w9ug1yLTj6fgmuDg41TgECXjLCij3RMsV8CwewBVgVN67wsA45DFWvqvLtu4rjNnE9JbdFTc1Z4WCPA3Xan44K1HoHAq9EVeaRYs8zoF5","client_ip":"10.0.0.2","client_port":9704,"node_ip":"10.0.0.2","node_port":9703,"services":["VALIDATOR"]},"dest":"8ECVSk179mjsjKRLWiQtssMLgp6EPhWXtaYyStWPSGAb"},"metadata":{"from":"EbP4aYNeTHL6q385GuVpRV"},"type":"0"},"txnMetadata":{"seqNo":2,"txnId":"1ac8aece2a18ced660fef8694b61aac3af08ba875ce3026a160acbc3a3af35fc"},"ver":"1"}
{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node3","blskey":"3WFpdbg7C5cnLYZwFZevJqhubkFALBfCBBok15GdrKMUhUjGsk3jV6QKj6MZgEubF7oqCafxNdkm7eswgA4sdKTRc82tLGzZBd6vNqU8dupzup6uYUf32KTHTPQbuUM8Yk4QFXjEf2Usu2TJcNkdgpyeUSX42u5LqdDDpNSWUK5deC5","blskey_pop":"QwDeb2CkNSx6r8QC8vGQK3GRv7Yndn84TGNijX8YXHPiagXajyfTjoR87rXUu4G4QLk2cF8NNyqWiYMus1623dELWwx57rLCFqGh7N4ZRbGDRP4fnVcaKg1BcUxQ866Ven4gw8y4N56S5HzxXNBZtLYmhGHvDtk6PFkFwCvxYrNYjh","client_ip":"10.0.0.2","client_port":9706,"node_ip":"10.0.0.2","node_port":9705,"services":["VALIDATOR"]},"dest":"DKVxG2fXXTU8yT5N7hGEbXB3dfdAnYv1JczDUHpmDxya"},"metadata":{"from":"4cU41vWW82ArfxJxHkzXPG"},"type":"0"},"txnMetadata":{"seqNo":3,"txnId":"7e9f355dffa78ed24668f0e0e369fd8c224076571c51e2ea8be5f26479edebe4"},"ver":"1"}
{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node4","blskey":"2zN3bHM1m4rLz54MJHYSwvqzPchYp8jkHswveCLAEJVcX6Mm1wHQD1SkPYMzUDTZvWvhuE6VNAkK3KxVeEmsanSmvjVkReDeBEMxeDaayjcZjFGPydyey1qxBHmTvAnBKoPydvuTAqx5f7YNNRAdeLmUi99gERUU7TD8KfAa6MpQ9bw","blskey_pop":"RPLagxaR5xdimFzwmzYnz4ZhWtYQEj8iR5ZU53T2gitPCyCHQneUn2Huc4oeLd2B2HzkGnjAff4hWTJT6C7qHYB1Mv2wU5iHHGFWkhnTX9WsEAbunJCV2qcaXScKj4tTfvdDKfLiVuU2av6hbsMztirRze7LvYBkRHV3tGwyCptsrP","client_ip":"10.0.0.2","client_port":9708,"node_ip":"10.0.0.2","node_port":9707,"services":["VALIDATOR"]},"dest":"4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"},"metadata":{"from":"TWwCRQRZ2ZHMJFn9TzLp7W"},"type":"0"},"txnMetadata":{"seqNo":4,"txnId":"aa5e817d7cc626170eca175822029339a444eb0ee8f0bd20d3b0b76e566fb008"},"ver":"1"}
```

### 2. Wallet DID 생

본 예제에서 `Steward`는 다른 actor들을 시스템에 추가하고 역할을 할당시킬 수 있다. `Steward`는 전체 네트워크의 신뢰와 신뢰도를 유지하는 데 궁극적인 책임을 지는 관리 기구의 중요한 구성원이다. 즉, Getting Started에 언급된 모든 조직과 개인은 모든 활동을 수행하기 전에 `Trust Anchor` 역할을 가진 `Steward`에 의해 "창조"된다.

![](https://user-images.githubusercontent.com/44635266/67156705-42383a00-f35d-11e9-8246-43967257aa89.png)

```
"Sovrin Steward" -> Create wallet
"Sovrin Steward" -> Create and store in Wallet DID from seed

"Government" -> Create wallet
"Government" -> Create and store in Wallet "Government" new DID
{'did': 'RHKghEbdHBHX5PfSk9ksrU', 'verkey': 'EEaqgWbqSwacXRqCUkm5sZ5NSKgxJAPY4cyUVGAxtp8t'}

"Sovrin Steward" -> Send Nym to Ledger for "Government DID" with TRUST_ANCHOR Role

"Faber" -> Create wallet
"Faber" -> Create and store in Wallet "Faber" new DID
{'did': 'DhJmyHoKvzJcNnJq6cWv3J', 'verkey': '7vK6kR2SLCuLx9pHhkv1wiYfpCuf4Sswj4ctTmadx9NG'}

"Sovrin Steward" -> Send Nym to Ledger for "Faber DID" with TRUST_ANCHOR Role

"Acme" -> Create wallet
"Acme" -> Create and store in Wallet "Acme" new DID
{'did': 'HP2QPeAscfS2b6YamgRjdm', 'verkey': '9vo8z4tHNVvC5HjhM6KzgqnfhJhK3vRfigQNyK5bisgG'}

"Sovrin Steward" -> Send Nym to Ledger for "Acme DID" with TRUST_ANCHOR Role

"Thrift" -> Create wallet
"Thrift" -> Create and store in Wallet "Thrift" new DID
{'did': '4uPFd8x1tawi9N9LwyCK99', 'verkey': '38PS9xHkcsc8WNYCng4xes2SkuVxLjCcQJR8rJWed6jb'}

"Sovrin Steward" -> Send Nym to Ledger for "Thrift DID" with TRUST_ANCHOR Role
```

### 3. Credential Schema 생성 - Transcript, Job Certificate by Government

![](https://user-images.githubusercontent.com/44635266/67156706-42d0d080-f35d-11e9-9229-5cae01025aac.png)

`Government`는` Transcript Schema`와 `Job-Certificate Schema`를 발행하고 이를 ledger에 기록한다. 스키마는 누구나 쉽게 구할 수 있다.

```
"Government" -> Create "Transcript" Schema
"Government" -> Send "Transcript" Schema to Ledger

"Government" -> Create "Job-Certificate" Schema
"Government" -> Send "Job-Certificate" Schema to Ledger
```

### 4. Credential Definition 생성 - Faber / Acme

![](https://user-images.githubusercontent.com/44635266/67156707-42d0d080-f35d-11e9-8fb9-59adfd638890.png)

![](https://user-images.githubusercontent.com/44635266/67156708-42d0d080-f35d-11e9-8bb7-19955ce54fa6.png)

`Government`가 발행한 스키마에 근거하여 그들만의 credential definitions를 만든다.

credential definitions에는 사용 중인 스키마와 credential definition의 `issuer`에 대한 필요한 정보가 포함되어 있다.

그리고 두 가지 스키마 모두 ledger에 기록을한다.

```
"Faber" -> Get "Transcript" Schema from Ledger
"Faber" -> Create and store in Wallet "Faber Transcript" Credential Definition
"Faber" -> Send  "Faber Transcript" Credential Definition to Ledger

"Acme" -> Get from Ledger "Job-Certificate" Schema
"Acme" -> Create and store in Wallet "Acme Job-Certificate" Credential Definition
"Acme" -> Send "Acme Job-Certificate" Credential Definition to Ledger
```

### 5. Faber College로 부터 Transcript 발급(for Alice)

![](https://user-images.githubusercontent.com/44635266/67156709-43696700-f35d-11e9-9129-fddd417db63e.png)

1. `Faber College`와 `Alice`(온보드 프로세스) 간의 연결 구축
2. `Faber College`은 자격증 제안을 만들어 `Alice`에게 보낸다.
3. `Alice`는 원장에게서 `Faber Transcript Credential Definition`를 회수해, 자격 증명 요청을 만들어 `Faber College`에 보낸다.
4. `Faber College`는 `Alice`를 위한 자격증을 만든다. 자격 증명 내부에는 `Faber Transcript Credential Definition`(및 Transcript Schema)에 나열된 항목의 값과 더불어 `Acme`가 요청할 때 `Alice`가 나중에 사용할 수 있다는 필요한 증거가 포함되어 있다.
5. `Alice`는 이제 자격증을 받아서 지갑에 보관한다.

```
"Alice" -> Create wallet
"Alice" -> Create and store in Wallet "Alice" new DID
{'did': 'KJfDoWvzj5aX3X7Mqjwtaq', 'verkey': 'Aye8jCjYbnTWqdSegWb6HMxBeTgfPrGWJBv8LuqZDgGe'}

"Faber" -> Send Nym to Ledger for "Alice Faber" DID

"Faber" -> Create "Transcript" Credential Offer for Alice
"Faber" -> Get key for Alice did
"Faber" -> Send "Transcript" Credential Offer to Alice

"Alice" -> Create and store "Alice" Master Secret in Wallet
"Alice" -> Get "Faber Transcript" Credential Definition from Ledger
"Alice" -> Create "Transcript" Credential Request for Faber
"Alice" -> Send "Transcript" Credential Request to Faber

"Faber" -> Create "Transcript" Credential for Alice
"Faber" -> Send  "Transcript" Credential to Alice

"Alice" -> Store "Transcript" Credential from Faber
```

Transcript

```
{'nonce': '191273141286763352691368', 'cred_def_id': 'DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1', 'key_correctness_proof': {'c': '83274154335989837619870188929660682589490962338323954943447575591195925876741', 'xz_cap': '697110871479600777487590691847306898652853501957292670689681452966370805984664406735043887354071944372772546327258744371125968128939986765911538460652630316981454702202809698494441983542501510551360399057982053184372549898060890372277912604590836112287005556575402881829292990078542714720065111719078540774777788288909551525962647175085000317546433898586430179605186222477940704159108090584352278023542415262249803734958104776766725629238310868227755025891469367074321107475532090355272832106034099045848570054757685980454973403563579151336353340308743808121481475497282984171036166506324527179392962828197153665711150924800697632408543308543720351997158666904886574798692308931079974758483234', 'xr_cap': [['first_name', '1758035912926950446717666858971127454335804476389735507124245433272426579874917669713743914157464810221951068407860146785177286496398407989449696515844331277194046804275618900072028191728484629665531754470879576115493242424089960795487743226035614026922161201251398777183168357243479107354694552452510465204446398287610806927880303226513012785625599090235193799320271077627756698195704683651038149304892035102573780063239775063771030653445874258098665452724411764502143171392284436705545604238879101717365976040368691976341357733410519490452914917806458754037019476394311009129235069927375445705137098889354751183125335028746095931832135476254457355627248879493943514843049342391322585993157909'], ['master_secret', '653066121604013974250943999266663902417725910649252196832398324490025160689005917742586261972493943608939268314051208264822463727066380589495327178045530312467203622499057596272855462878979094775094269976551450487759935466488260529064913984648536136123442791471363700059360684324721685800303500819817489226883557914204661454091922164267568360680018052995473724589336883089613390378253193699864826894807415199262433317712372312873150425298333079714285339294989804402659371298157668504900269443330167178842603298551613362882127392260128359990100354832198666417333764942941521266647355129087050108396788881137936948602238985367957696470720628127770292525940993297031328543750906611864837904917454'], ['degree', '166304763119086964577350207667475805157777573857895034922074799548718219584196202460530268047720905852066626637639932446916391134045330763536585164715972949466549217037024234689425555998019358243266103486110176669033260350129102147976633074032304101833912493455814712256799602527271977218108959202429473630602210820074591797482942511560205721744787326064280904226960488704771598335088067091806577647539527221257768492572504555694377816532242707771188824815643324195967480546713084890241600834932692982367830235916244332898548007986600304866094037348595405137624696406687836331109134388505314281594398870359834338876023138868904128068831486020478115274450294794519487385163594283707959579226517'], ['ssn', '81872842944367541612844673918736997199108254900457781045627003991149091011576254987165691634697267917887474700082578804237705827217466986826666683154396295026105698337685338924531931817123017196406616274307986577904758457828362560798480154455883302931927548811028023922894687646262476661677709675375790730768505081060239117776630868636112916400277219818083187645898360561458054717989490093518022915761026699352172493525360631190016591323413810433455479942285727770274711364010107789933950724230835845963103968416546696657393313766163071196592987524091788159258069200358843013324127761836943936485614343817185137962770965260693868208736059691583363099332066490852093583989493447111957266262869'], ['year', '1677615483784117152897443223399973094449492346553679840974759935970136779557990747651995452244400817879222373674479722031938908581361140713500919459368446354753678433906419864955531244853476569348812602451017350033409241693833192673364602333839883319460881560431195660508417322942324269091819649016447583543978803712848590089049675838104103568553385163051685544638829610228780006240985208763816911261860041465259515627406715014220470156177404571447058485746067515179410041714803156519651291223048366727421533659849452273473755284110926820864032067760438303482344999706050192500413455140428890062339448584381755306903742377255137035195292074212726850831182495709172205291783999135982255736235057'], ['last_name', '972577720071556761653902899888070654505859704725506017391574667155788880027279621978276976571193040494076493376490549704185523415235497416612767368930123201620818254230204064568757957244853439588942798191703506964902784886134432710963455094483766834721977708292975054685183194974729737024432356777691459087099015075866803181731937108735603752003422602787843616959725843733418824025906960151911796255144372437605279060467449342551048179606638359741437580272667440774367436813476113946970475802400278882274933871342793474404312640614801202001520223816184078534272284949618960969324132559429527419871711493959932830272786738335420162444445989688518674230440875362039108342345595065787871450472747'], ['status', '40228856648327849579390617869008495880548969438552446566398206259234003341152555195299636652279109134525523138670545203787395783146901611021078017564527307870483114745157559352708312519796350635700806904050095140997376525079812349551346726575134299240439979598510768885597679346929618780460302611622996641598319742066508133145958729144570908831455677049797675142289769395223350229636712643431610748410981650817378141649856369971751916448497496256407130433865323092908736223469102798005984308991581188692871001654315192281309175598141854500287893356131228768973105690233253722553781522719653148197194832207644593903139749071333976601549464172325509445803933374820584798178543253491640481073491'], ['average', '1516034810778891125676950449133383277232539804805633821624395828697376889570177601002894036713694314948745593604333761079213870131966689831020337417683414385233864197077821735551149159843900706594840986780809661167511359697952330147284405567234502055911518477224987687367507854027289070659941919828491523617985729490115379359873790127320112734811595683033701490004921706456020432133367660039438000371378928805545412448899088066914933029084275240914141121319506769452581567497659478788883504737462021565165425774216030077530279382635602811174639768158985404490232455235130439165807972826620784408613485884909264716639120655775503704249207903222558338400099898629367873989314671228279573533866529']]}, 'schema_id': 'RHKghEbdHBHX5PfSk9ksrU:2:Transcript:1.2'}
```

### 6. Acme Corp 입사 지원(for Alice)

![](https://user-images.githubusercontent.com/44635266/67156710-43696700-f35d-11e9-937a-c3161380b737.png)

1. `Acme Corp`과 `Alice` 간의 연결 구축(온보드 프로세스)

2. `Acme Corp`은 필요한 항목과 조건을 나열한 Proof Request를 생성한다. 이 경우 `Acme Corp`는 `Faber College` 학위증명, 신분, ssn을 필요로 하며, 평균은 4가 넘는다.

3. `Alice`는 이 증명 요청을 받고, `Faber College`에서 얻은 자격 증명을 바탕으로 증명서를 만든다. 증명은 Acme의 증명요청 요건을 충족할 수 있는 정보를 포함하고 있다.

4. `Acme Corp`는 `Alice`로부터 증명을 받는다. 증명서 안에서, `Acme Corporation`은 필요한 정보와 상태를 보고, 그것들이 `Faber College`에서 오고 있는지 확인한다.

5. `Acme Corp`는 이 증명을 받아들인다.

```
==============================
== Apply for the job with Acme - Transcript proving ==
------------------------------
"Acme" -> Create "Job-Application" Proof Request
"Acme" -> Get key for Alice did
"Acme" -> Send "Job-Application" Proof Request to Alice

"Alice" -> Get credentials for "Job-Application" Proof Request

>> alice['job_application_proof_request'] : 
{"requested_attributes": {"attr3_referent": {"restrictions": [{"cred_def_id": "DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1"}], "name": "degree"}, "attr2_referent": {"name": "last_name"}, "attr4_referent": {"restrictions": [{"cred_def_id": "DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1"}], "name": "status"}, "attr5_referent": {"restrictions": [{"cred_def_id": "DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1"}], "name": "ssn"}, "attr6_referent": {"name": "phone_number"}, "attr1_referent": {"name": "first_name"}}, "version": "0.1", "name": "Job-Application", "nonce": "390462888633022186190843", "requested_predicates": {"predicate1_referent": {"p_type": ">=", "p_value": 4, "restrictions": [{"cred_def_id": "DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1"}], "name": "average"}}}

>> cred_for_attr1 : 
{'referent': 'e2f6d2d1-2e63-4ae6-8cf5-f8fb6e2ad871', 'cred_def_id': 'DhJmyHoKvzJcNnJq6cWv3J:3:CL:15:TAG1', 'cred_rev_id': None, 'schema_id': 'RHKghEbdHBHX5PfSk9ksrU:2:Transcript:1.2', 'rev_reg_id': None, 'attrs': {'year': '2015', 'degree': 'Bachelor of Science, Marketing', 'ssn': '123-45-6789', 'average': '5', 'status': 'graduated', 'first_name': 'Alice', 'last_name': 'Garcia'}}

"Alice" -> Get Schema from Ledger
"Alice" -> Get Credential Definition from Ledger
"Alice" -> Create "Job-Application" Proof
"Alice" -> Send "Job-Application" Proof to Acme

"Acme" -> Get Schema from Ledger
"Acme" -> Get Credential Definition from Ledger
"Acme" -> Verify "Job-Application" Proof from Alice
```

### 7. 종료

그 다음으로는 위에서 말했듯이 `Alice`가 `Thrift Bank`에게 대출을 신청하는 스토리가 있지만, 여기서 마무리하겠습니다.

마지막으로는 사용된 `pool`과 `wallet`을 지워줍니다.

```
==============================
"Sovrin Steward" -> Close and Delete wallet
"Government" -> Close and Delete wallet
"Faber" -> Close and Delete wallet
"Acme" -> Close and Delete wallet
"Thrift" -> Close and Delete wallet
"Alice" -> Close and Delete wallet
Close and Delete pool
Getting started -> done
```


