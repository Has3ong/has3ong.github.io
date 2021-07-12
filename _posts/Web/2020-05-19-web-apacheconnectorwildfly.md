---
title : Centos7 / Apache - Wildfly - JK Connector 연동하기
tags :
- WEB
- WAS
- AJP
- Wildfly
- Apache
- Centos
categories:
- WEB / WAS
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

Wildfly Standalone 방식으로 설정하겠습니다.

WEB 과 WAS 의 차이와 개념을 정확하게 모르신다면 [WEB / WAS 의 차이](/webwas) 포스트를 보시면 됩니다.

AJP 프로토콜의 개념은 [AJP Protocol](/ajpprotocol) 포스트를 보시면 됩니다.

## Version

사용한 버전은 아래와 같습니다.

* **Vagrant** : 2.2.6
* **Java** : openjdk-1.8.0
* **Apache Wildfly** : 19.0.2
* **Apache httpd** : 2.4.43
* **tomcat-connectors** : 1.2.48

## Vagrant

저는 VM 을 자동으로 관리하기 위해 Vagrant 를 사용했습니다. Vagrantfile 은 아래와 같습니다.

```vagrantfile
Vagrant.configure("2") do |config|
  vm_num = 1
  node_cpu = 2 # 1Core
  node_memory = "2048" # 2G Memory
  node_network = "10.30.30"
  node_prefix = "centos7"

  config.vm.box = "centos/7"
  config.vm.box_version = "1905.1"
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

Vagrantfile 이 있는 경로에서 `vagrant up` 명령어를 치면 VM 이 생성됩니다.

```shell
$ vagrant up

=> vagrant: A new version of Vagrant is available: 2.2.7 (installed version: 2.2.6)!
==> vagrant: To upgrade visit: https://www.vagrantup.com/downloads.html

Bringing machine 'centos7-1' up with 'virtualbox' provider...
==> centos7-1: Clearing any previously set forwarded ports...
==> centos7-1: Clearing any previously set network interfaces...
==> centos7-1: Preparing network interfaces based on configuration...
    centos7-1: Adapter 1: nat
    centos7-1: Adapter 2: hostonly
==> centos7-1: Forwarding ports...
    centos7-1: 22 (guest) => 2222 (host) (adapter 1)
==> centos7-1: Running 'pre-boot' VM customizations...
==> centos7-1: Booting VM...
==> centos7-1: Waiting for machine to boot. This may take a few minutes...
    centos7-1: SSH address: 127.0.0.1:2222
    centos7-1: SSH username: vagrant
    centos7-1: SSH auth method: private key
==> centos7-1: Machine booted and ready!
==> centos7-1: Checking for guest additions in VM...
    centos7-1: No guest additions were detected on the base box for this VM! Guest
    centos7-1: additions are required for forwarded ports, shared folders, host only
    centos7-1: networking, and more. If SSH fails on this machine, please install
    centos7-1: the guest additions and repackage the box to continue.
    centos7-1:
    centos7-1: This is not an error message; everything may continue to work properly,
    centos7-1: in which case you may ignore this message.
==> centos7-1: Setting hostname...
==> centos7-1: Configuring and enabling network interfaces...
==> centos7-1: Rsyncing folder: /Users/has3ong/Desktop/solaris10/ => /vagrant
==> centos7-1: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> centos7-1: flag to force provisioning. Provisioners marked to run always will still run.
```

`vagrant ssh centos7-1` 을 입력하면 VM 에 접속할 수 있습니다.

```shell
$ vagrant ssh centos7-1

Last login: Mon Apr 27 05:08:17 2020 from 10.0.2.2
[vagrant@centos7-1 ~]$
```

VM 을 종료시키려면 `vagrant halt` 를 입력합니다.

```shell
$ vagrant halt

==> centos7-1: Attempting graceful shutdown of VM...
```

VM 을 제거하려면 `vagrant destroy` 를 입력하면 됩니다.

```shell
$ vagrant destroy

    centos7-1: Are you sure you want to destroy the 'centos7-1' VM? [y/N]
```

```
$ yum install -y wget
```

## Install JDK

설치 가능한 Java 버전을 살펴보겠습니다.

```shell
$ yum list java*jdk-devel

Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.kakao.com
 * extras: mirror.kakao.com
 * updates: mirror.kakao.com
Available Packages
java-1.6.0-openjdk-devel.x86_64            1:1.6.0.41-1.13.13.1.el7_3             base
java-1.7.0-openjdk-devel.x86_64            1:1.7.0.251-2.6.21.0.el7_7             updates
java-1.8.0-openjdk-devel.i686              1:1.8.0.242.b08-0.el7_7                updates
java-1.8.0-openjdk-devel.x86_64            1:1.8.0.242.b08-0.el7_7                updates
java-11-openjdk-devel.i686                 1:11.0.6.10-1.el7_7                    updates
java-11-openjdk-devel.x86_64               1:11.0.6.10-1.el7_7                    updates
```

여기서 OpenJDK 1.8.0 버전을 설치하겠습니다.

```shell
$ yum install java-1.8.0-openjdk-devel.x86_64
```

OpenJDK 설치를하고 아래 명령어를 쳤을때 정확하게 출력이되면 정상적으로 설치가 된것입니다.

```shell
$ java -version

openjdk version "1.8.0_242"
OpenJDK Runtime Environment (build 1.8.0_242-b08)
OpenJDK 64-Bit Server VM (build 25.242-b08, mixed mode)
```

그리고 Java 경로를 알아보겠습니다. `which` 를 사용하면 아래와 같이 찍히지만 보통 JAVA_HOME 은 */usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-0.el7_7.x86_64* 이런식으로 잡힙니다.

```shell
$ which javac
/usr/bin/javac
$ which java
/usr/bin/java
```

```shell
$JAVA_HOME

/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-0.el7_7.x86_64
```

## Install Wildfly

제일 먼저 Apache 홈페이지에서 필요한 파일을 설치하기 위한 `wget` 패키지를 설치합니다.

```shell
$ yum install -y wget
```

Wildfly 최신 버전을 다운로드 한 뒤 압축을 풀고난 후 `/opt` 경로에다가 옮겨두겠습니다.

```shell
$ wget https://download.jboss.org/wildfly/19.0.0.Final/wildfly-19.0.0.Final.tar.gz
$ tar xvzpf wildfly-19.0.0.Final.tar.gz
$ mv wildfly-19.0.0.Final /opt/
$ mv wildfly-19.0.0.Final/ wildfly
```

옮기고 난 후 Mangement 계정을 만들겠습니다. 이는 Wildfly 관리 페이지에 접근할 때 사용됩니다.

```shell
$ /opt/wildfly/bin/add-user.sh

What type of user do you wish to add?
 a) Management User (mgmt-users.properties)
 b) Application User (application-users.properties)
(a): a

Enter the details of the new user to add.
Using realm 'ApplicationRealm' as discovered from the existing property files.
Username : root
Password recommendations are listed below. To modify these restrictions edit the add-user.properties configuration file.
 - The password should be different from the username
 - The password should not be one of the following restricted values {root, admin, administrator}
 - The password should contain at least 8 characters, 1 alphabetic character(s), 1 digit(s), 1 non-alphanumeric symbol(s)
Password :
WFLYDM0098: The password should be different from the username
Are you sure you want to use the password entered yes/no? yes
Re-enter Password :
What groups do you want this user to belong to? (Please enter a comma separated list, or leave blank for none)[  ]:
About to add user 'root' for realm 'ApplicationRealm'
Is this correct yes/no? yes
Added user 'root' to file '/opt/wildfly/standalone/configuration/application-users.properties'
Added user 'root' to file '/opt/wildfly/domain/configuration/application-users.properties'
Added user 'root' with groups  to file '/opt/wildfly/standalone/configuration/application-roles.properties'
Added user 'root' with groups  to file '/opt/wildfly/domain/configuration/application-roles.properties'
Is this new user going to be used for one AS process to connect to another AS process?
e.g. for a root host controller connecting to the master or for a Remoting connection for server to server EJB calls.
yes/no? yes
To represent the user add the following to the server-identities definition <secret value="c2xhdmU=" />
```

id 와 password 모두 root 로 했습니다.

다음으로 *standalone.xml* 를 수정하겠습니다. 현재 자기 자신의 접속만 허용이 되어 있는데 이를 모든 IP 에서 허용할 수 있게 만들어 주겠습니다.

```shell
$ vi /opt/wildfly/standalone/configuration/standalone.xml
```

```xml
<interfaces>
        <interface name="management">
                <any-address/>
<!--            <inet-address value="${jboss.bind.address.management:127.0.0.1}"/>-->
        </interface>
        <interface name="public">
                <any-address/>
<!--            <inet-address value="${jboss.bind.address:127.0.0.1}"/>-->
        </interface>
    </interfaces>
```

그리고 `systemd` 가 wildfly 데몬을 제어하도록 등록시키겠습니다.

```shell
$ vi /etc/systemd/system/wildfly.service
```

```shell
[Unit]
Description=WildFly Server
After=httpd.service
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/opt/wildfly/bin/standalone.sh
```

정확하게 작동하는지 wildfly 를 시작해보겠습니다.

```shell
$ systemctl daemon-reload
$ systemctl start wildfly
```

wildfly 의 디폴트 포트는 8080, 9090 이므로 netstat 으로 8080, 9990 포트가 작동하는지 확인해보겠습니다.

```shell
$ ss -nlp | grep tcp
tcp    LISTEN     0      128       *:111                   *:*
tcp    LISTEN     0      128       *:22                    *:*
tcp    LISTEN     0      100    127.0.0.1:25                    *:*
tcp    LISTEN     0      1        [::ffff:127.0.0.1]:8005               [::]:*
tcp    LISTEN     0      128    [::]:111                [::]:*
tcp    LISTEN     0      100    [::]:8080               [::]:*
tcp    LISTEN     0      100    [::]:9990               [::]:*
tcp    LISTEN     0      128    [::]:22                 [::]:*
tcp    LISTEN     0      100       [::1]:25                 [::]:*
```

http://10.30.30.2:8080/ 접속시 wildfly 화면이 나타나면 정상적으로 설치가 된것입니다.

![image](https://user-images.githubusercontent.com/44635266/81049328-f57f0f80-8ef8-11ea-8490-77d766cc120a.png)

http://10.30.30.2:9990/ 도 접속해 보겠습니다. 사용자 계정과 비밀번호를 요구할 수 있는데 이전에 생성했던 root / root 를 입력하면 접속할 수 있습니다. wildfly 9990 포트는 WAS 관리를 위한 URL 입니다.

![image](https://user-images.githubusercontent.com/44635266/81049346-ff087780-8ef8-11ea-9c9f-483e7dd4fe4a.png)

아래 명령어를 사용하면 다시 종료시킬 수 있습니다.

```shell
$ systemctl stop wildfly
```

만약 접속이 안된다면 방화벽을 확인하면 됩니다. `firewalld` 를 설치하겠습니다.

```shell
$ yum install firewalld
$ systemctl start firewalld
$ systemctl enable firewalld

$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0 eth1
  sources:
  services: dhcpv6-client ssh
  ports:
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

방화벽을 확인해보면 아무 포트도 열려있지 않은것을 확인할 수 있습니다. 8080, 9990 포트를 열어보겠습니다.

```shell
$ firewall-cmd --permanent --zone=public --add-port=8080/tcp
success
$ firewall-cmd --permanent --zone=public --add-port=9990/tcp
success
$ firewall-cmd --reload
success

$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0 eth1
  sources:
  services: dhcpv6-client ssh
  ports: 8080/tcp 9990/tcp
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

8080, 9990 포트가 열린것을 볼 수 있습니다. WEB Server 도 설치해야 하니 http 도 열어주겠습니다.

```shell
$ sudo firewall-cmd --permanent --zone=public --add-service=http
success
$ sudo firewall-cmd --reload
success
$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0 eth1
  sources:
  services: dhcpv6-client http ssh
  ports: 8080/tcp 9990/tcp
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

## Install Apache Web Server

아래와 같이 간단하게 설치할 수 있지만 `httpd` 파일을 다운로드 받아 컴파일하는 방식으로 설치해보겠습니다.

```shell
$ yum install httpd
$ systemctl start httpd
```

컴파일을 해야하기 때문에 사전에 필요한 패키지들을 설치하겠습니다.

```shell
$ yum -y install gcc make gcc-c++ pcre-devel expat-devel
```

`httpd`, `apr`, `apr-util` 을 `wget` 을 이용하여 다운로드 받고 압축을 해제한 다음 `/usr/local/src` 폴더로 이동시킵니다.

**APR**(아파치 포터블 런타임)는 아파치 HTTP 서버 2.x.의 핵심이며 휴대용 라이브러리입니다. 이런 APR은 고급 IO 기능(예:sendfile, epoll and OpenSSL 등)에 대한 접근을 포함하여 OS 수준의 기능 (난수 생성, 시스템 상태), 그리고 기본 프로세스 처리(공유 메모리, NT 파이프와 유닉스 소켓) 등 많은 용도로 사용되고 있습니다.

```shell
$ wget http://mirror.navercorp.com/apache/httpd/httpd-2.4.43.tar.gz
$ tar xvzpf httpd-2.4.43.tar.gz
$ wget http://mirror.apache-kr.org/apr/apr-1.6.5.tar.gz
$ tar xvzpf apr-1.6.5.tar.gz
$ wget http://mirror.apache-kr.org/apr/apr-util-1.6.1.tar.gz
$ tar xvzpf apr-util-1.6.1.tar.gz

$ mv httpd-2.4.43 /usr/local/src
$ mv apr-1.6.5 /usr/local/src
$ mv apr-util-1.6.1 /usr/local/src
```

먼저 `apr` 부터 컴파일합니다.

```shell
$ cd /usr/local/src/apr-1.6.5

$ ./configure --prefix=/usr/local/src/apr-1.6.5

$ make
$ make install
```

그 다음 `apr-util` 을 컴파일합니다.

```shell
$ cd /usr/local/src/apr-util-1.6.1

$ ./configure --prefix=/usr/local/src/apr-util-1.6.1 --with-apr=/usr/local/src/apr-1.6.5

$ make 
$ make install
```

마지막으로 `httpd` 를 컴파일합니다. 명령어가 너무 길어서 보기편하게 나눠놨으니 사용하실 때는 한번에 입력하시면 됩니다.

```shell
$ cd /usr/local/src/httpd-2.4.43

#./configure --prefix=/usr/local/apache24 --enable-modules=most --enable-mods-shared=all --enable-so --with-apr=/usr/local/src/apr-1.6.5 --with-apr-util=/usr/local/src/apr-util-1.6.1

./configure 
--prefix=/usr/local/apache24 
--enable-modules=most 
--enable-mods-shared=all 
--enable-so
--with-apr=/usr/local/src/apr-1.6.
--with-apr-util=/usr/local/src/apr-util-1.6.1

$ make 
$ make install
```

`--prefix=/usr/local/apache24` 이 경로에 WEB Server 가 설치됩니다. 컴파일이 끝나면 *httpd.conf* 파일로 들어가 ServerName 의 주석을 해제해줍니다.

```shell
$ vi /usr/local/apache24/conf/httpd.conf
```

```xml
<!-- ServerName 127.0.0.1:80 -->
```

```shell
$ /usr/local/apache24/bin/httpd -k start
```

`netstat` 명령어를 보면 80 포트가 열린것을 확인할 수 있습니다.

```shell
$ ss -nlp | grep tcp
tcp    LISTEN     0      128       *:111                   *:*
tcp    LISTEN     0      128       *:22                    *:*
tcp    LISTEN     0      100    127.0.0.1:25                    *:*
tcp    LISTEN     0      1        [::ffff:127.0.0.1]:8005               [::]:*
tcp    LISTEN     0      128    [::]:111                [::]:*
tcp    LISTEN     0      128    [::]:80                 [::]:*
tcp    LISTEN     0      100    [::]:8080               [::]:*
tcp    LISTEN     0      100    [::]:9990               [::]:*
tcp    LISTEN     0      128    [::]:22                 [::]:*
tcp    LISTEN     0      100       [::1]:25                 [::]:*
```

정상적으로 설치가 완료되면 http://10.30.30.2/ 접속시 `It Works !` 라는 문구가 출력됩니다.

![image](https://user-images.githubusercontent.com/44635266/80599488-f7af1d00-8a65-11ea-8f3d-5988707ef18f.png)

마찬가지로 `systemd` 에서 사용할 수 있게 등록 시켜주겠습니다.

```shell
$ vi /etc/systemd/system/httpd.service
```

*httpd.service* 파일에 아래 내용을 등록해줍니다.

```shell
[Unit]
Description=The Apache HTTP Server
 
[Service]
Type=forking
PIDFile=/usr/local/apache24/logs/httpd.pid
ExecStart=/usr/local/apache24/bin/apachectl start
ExecReload=/usr/local/apache24/bin/apachectl graceful
ExecStop=/usr/local/apache24/bin/apachectl stop
KillSignal=SIGCONT
PrivateTmp=true
 
[Install]
WantedBy=multi-user.target
```

## Install Tomcat Connector

마지막으로 WEB Server 와 WAS 를 연동시켜줄 JK Connector 를 설치하겠습니다. 여러가지 커넥터가 있는데 `mod_jk` 를 사용하겠습니다.

마찬가지로 `apxs` 를 미리 설치해주고 경로를 확인해보겠습니다.

apxs 는 Apache 하이퍼텍스트 전송 프로토콜 (HTTP) 서버의 확장모듈을 컴파일하고 설치하는 도구입니다. 이 도구는 여러 소스와 오브젝트파일을 가지고, `mod_so` 의 `LoadModule` 지시어로 실행중에 아파치 서버로 읽어들일 수 있는 동적공유객체(DSO)를 만들어줍니다.

```shell
$ yum install -y httpd-devel
$ which apxs
/usr/bin/apxs
```

`wget` 으로 tomcat-coonect 를 다운로드 받고 압축을 해제시킨다음 컴파일 하겠습니다.

```shell
$ wget http://mirror.navercorp.com/apache/tomcat/tomcat-connectors/jk/tomcat-connectors-1.2.48-src.tar.gz
$ tar xvzpf tomcat-connectors-1.2.48-src.tar.gz
$ cd tomcat-connectors-1.2.48-src/native/
$ which apxs
/bin/apxs
$ ./configure --with-apxs=/usr/bin/apxs
$ make
$ make install
```

정상적으로 컴파일이 되었다면 `mod_jk.so` 파일이 위에서 설치한 WEB Server 경로의 *modules* 에 생깁니다. 하지만 제대로 설치가 되지 않은 경우에는 아래 명령어를 사용하여 직접 옮겨주면 됩니다.

```shell
$ cp apache-2.0/mod_jk.so /usr/local/apache24/modules/
```

## Apache - mod_jk - Wildfly 연동하기

WEB Server 에 설정파일을 수정하겠습니다.

```shell
$ vi /usr/local/apache24/conf/httpd.conf
```

*httpd.conf* 에 아래 내용을 추가해줍니다.

```shell
LoadModule jk_module modules/mod_jk.so
JkWorkersFile conf/workers.properties
JkLogFile logs/mod_jk.log
JkShmFile logs/mod_jk.shm
JkMount /* worker1
```

그리고 *workers.properties* 파일을 만들어줍니다.

```shell
$ vi /usr/local/apache24/conf/workers.properties
```

*workers.properties* 에는 아래 내용을 등록합니다.

이는 localhost:8009 주소로 AJP1.3 프로토콜을 이용하여 WEB Server 와 WAS 를 연동하겠다는 의미입니다.

즉, http 80 포트로 접속을 하면 AJP 프로토콜을 이용해서 8009, WAS 8080 포트로 접속됩니다.

```shell
worker.list=worker1

worker.worker1.type=ajp13
worker.worker1.host=127.0.0.1
worker.worker1.port=8009
```

마지막으로 Wildfly 의 *standalone.xml* 파일에 AJP 프로토콜을 수신할 수 있도록 아래 내용을 추가해줍니다.

```
$ vi /opt/wildfly/standalone/configuration/standalone.xml
```

```xml
                <server name="default-server">
                        <ajp-listener name="ajp" socket-binding="ajp"/> <!-- 추가 -->
                        <http-listener name="default" socket-binding="http" redirect-socket="https" enable-http2="true"/>
                        <https-listener name="https" socket-binding="https" security-realm="ApplicationRealm" enable-http2="true"/>
                        <host name="default-host" alias="localhost">
                                <location name="/" handler="welcome-content"/>
                                <http-invoker security-realm="ApplicationRealm"/>
                        </host>
                </server>
                <servlet-container name="default">
                        <jsp-config/>
                        <websockets/>
                </servlet-container>
                <handlers>
                        <file name="welcome-content" path="${jboss.home.dir}/welcome-content"/>
                </handlers>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:webservices:2.0" statistics-enabled="${wildfly.webservices.statistics-enabled:${wildfly.statistics-enabled:false}}">
            <wsdl-host>${jboss.bind.address:127.0.0.1}</wsdl-host>
            <endpoint-config name="Standard-Endpoint-Config"/>
            <endpoint-config name="Recording-Endpoint-Config">
                <pre-handler-chain name="recording-handlers" protocol-bindings="##SOAP11_HTTP ##SOAP11_HTTP_MTOM ##SOAP12_HTTP ##SOAP12_HTTP_MTOM">
                    <handler name="RecordingHandler" class="org.jboss.ws.common.invocation.RecordingServerHandler"/>
                </pre-handler-chain>
            </endpoint-config>
            <client-config name="Standard-Client-Config"/>
        </subsystem>
        <subsystem xmlns="urn:jboss:domain:weld:4.0"/>
    </profile>
    <interfaces>
        <interface name="management">
            <any-address/>
        </interface>
        <interface name="public">
            <any-address/>
        </interface>
    </interfaces>
    <socket-binding-group name="standard-sockets" default-interface="public" port-offset="${jboss.socket.binding.port-offset:0}">
        <socket-binding name="ajp" port="${jboss.ajp.port:8009}"/> <!-- 추가 -->
        <socket-binding name="http" port="${jboss.http.port:8080}"/>
        <socket-binding name="https" port="${jboss.https.port:8443}"/>
        <socket-binding name="management-http" interface="management" port="${jboss.management.http.port:9990}"/>
        <socket-binding name="management-https" interface="management" port="${jboss.management.https.port:9993}"/>
        <socket-binding name="txn-recovery-environment" port="4712"/>
        <socket-binding name="txn-status-manager" port="4713"/>
        <outbound-socket-binding name="mail-smtp">
            <remote-destination host="localhost" port="25"/>
        </outbound-socket-binding>
    </socket-binding-group>
</server>
```

설정하면 http://10.30.30.2/ 를 접속해 바로 Wildfly 화면이 뜨면 정상적으로 작동하고 있습니다.

![image](https://user-images.githubusercontent.com/44635266/81050034-4c391900-8efa-11ea-8219-3519f78d5fcb.png)


