---
title : Centos7 / Apache - Tomcat - JK Connector Session Clustering
tags :
- WEB
- WAS
- Session
- Clustering
- AJP
- Tomcat
- Apache
- Centos
---

환경 구성은 아래 1, 2 를 모두 해결하신 후 진행하시면 되겠습니다.

1. [[Centos7] Apache - Tomcat - JK Connector 연동하기](/web-apacheconnectortomcat)
2. [[Centos7]  Apache - Tomcat - JK Connector Load Balancing](/web-tomcatloadbalance)

## Version

사용한 버전은 아래와 같습니다.

* **Vagrant** : 2.2.6
* **Java** : openjdk-1.8.0
* **Apache Tomcat** : 9.0.34
* **Apache httpd** : 2.4.43
* **Tomcat Connectors** : 1.2.48

## Session Clustering

[Apache Tomcat 9](http://tomcat.apache.org/tomcat-9.0-doc/cluster-howto.html) 에 Session Replication How-To 문서를 바탕으로 작성했습니다.

먼저 *index.jsp* 파일을 바꿔서 세션 정보가 출력되도록 설정합니다.

```
$ vi /opt/tomcat/webapps/ROOT/index.jsp
$ vi /opt/instance1/tomcat/webapps/ROOT/index.jsp
$ vi /opt/instance2/tomcat/webapps/ROOT/index.jsp
```

Session 의 Id 값과 해당 세션을 호출한 횟수를 나타내는 HTML 코드입니다.

```jsp
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<HTML>
  <head>
  </head>
  <body>
    <h1>Session Clustering Test WAS1</h1>
  
    <%
      Integer val = (Integer)session.getAttribute("session_counter");

      if(val==null){
        val = new Integer(1);
      }
      else {
        val = new Integer(val.intValue() + 1);
      }

      session.setAttribute("session_counter", val);
    %>
    <p>Session Counter = <%= val %></p>
    <p>Current Session ID : <%= request.getRequestedSessionId() %></p>
  </body>
</html>
```

그리고 클러스터링 가능하도록 *web.xml* 에 `<distributable/>` 요소를 추가해줍니다.

```shell
$ vi /opt/tomcat/conf/web.xml
$ vi /opt/instance1/tomcat/conf/web.xml
$ vi /opt/instance2/tomcat/conf/web.xml
```

```xml
<web-app>
    <distributable/>
</web-app>
```

제가 했을 때는 위에만 수정하는게 아니라 아래 배포되는 환경에서 *webapps/ROOT/WEB-INF/web.xml* 에도 추가해야 정상적으로 Session Clustering 이 되었습니다. 마찬가지로 추가해 줘야합니다.

혹시 이유를 알고계신분은 댓글 달아주시면 감사하겠습니다.

```shell
$ vi /opt/tomcat/webapps/ROOT/WEB-INF/web.xml
$ vi /opt/instance1/tomcat/webapps/ROOT/WEB-INF/web.xml
$ vi /opt/instance2/tomcat/webapps/ROOT/WEB-INF/web.xml
```

```xml
<display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to Tomcat
  </description>
<distributable/>
```

이제 마지막으로 *server.xml* 만 수졍하면 됩니다.

```shell
server.xml

$ vi /opt/tomcat/conf/server.xml
$ vi /opt/instance1/tomcat/conf/server.xml
$ vi /opt/instance2/tomcat/conf/server.xml
```

기본적인 방법은 Setting 1 으로 해도 된다하지만 저는 Setting 2 로 설정해주었습니다.

> Setting 1
 
```xml
<Cluster className="org.apache.catalina.ha.tcp.SimpleTcpCluster"/>
``` 

> Setting 2

여기서 잘 보시면 Receiver 에 port 가 4000 번으로 잡혀있는데, 저는 각각 4000, 4001, 4002 로 잡아줬습니다. 수정하지 않아도 Tomcat 에서 해당 포트가 사용중이라면 자동으로 바꿔준다고 합니다.

```xml
<Cluster className="org.apache.catalina.ha.tcp.SimpleTcpCluster"
                 channelSendOptions="8">

          <Manager className="org.apache.catalina.ha.session.DeltaManager"
                   expireSessionsOnShutdown="false"
                   notifyListenersOnReplication="true"/>

          <Channel className="org.apache.catalina.tribes.group.GroupChannel">
            <Membership className="org.apache.catalina.tribes.membership.McastService"
                        address="228.0.0.4"
                        port="45564"
                        frequency="500"
                        dropTime="3000"/>
            <Receiver className="org.apache.catalina.tribes.transport.nio.NioReceiver"
                      address="auto"
                      port="4000"
                      autoBind="100"
                      selectorTimeout="5000"
                      maxThreads="6"/>

            <Sender className="org.apache.catalina.tribes.transport.ReplicationTransmitter">
              <Transport className="org.apache.catalina.tribes.transport.nio.PooledParallelSender"/>
            </Sender>
            <Interceptor className="org.apache.catalina.tribes.group.interceptors.TcpFailureDetector"/>
            <Interceptor className="org.apache.catalina.tribes.group.interceptors.MessageDispatchInterceptor"/>
          </Channel>

          <Valve className="org.apache.catalina.ha.tcp.ReplicationValve"
                 filter=""/>
          <Valve className="org.apache.catalina.ha.session.JvmRouteBinderValve"/>

          <Deployer className="org.apache.catalina.ha.deploy.FarmWarDeployer"
                    tempDir="/tmp/war-temp/"
                    deployDir="/tmp/war-deploy/"
                    watchDir="/tmp/war-listen/"
                    watchEnabled="false"/>

          <ClusterListener className="org.apache.catalina.ha.session.ClusterSessionListener"/>
        </Cluster>
```

위 내용을 간단히 해석하겠습니다.

1. Multicast 방식으로 동작하며 `address` 는 `228.0.0.4`, `port` 는 `45564` 를 사용하고 서버 `IP` 는 `java.net.InetAddress.getLocalHost().getHostAddress()` 로 얻어진 IP 값으로 송출됩니다.
2. 먼저 구동되는 서버부터 4000 ~ 4100 사이의 TCP port 를 통해 reqplication message 를 listening 합니다.
3. Listener는 ClusterSessionListener, interceptor 는 TcpFailureDetector 와 MessageDispatchInterceptor 가 설정됩니다.

더 자세한 설명은 [Tomcat 8 세션 클러스터링 하기
](https://jistol.github.io/java/2017/09/15/tomcat-clustering/) 포스트에서 자세히 설명되있으니 참고하시면 됩니다.

마지막으로 방화벽을 확인하시면 됩니다. 먼저 45564 tcp/udp 포트를 열고 4000 ~ 4100 번대 포트를 열어줍니다.

```shell
$ firewall-cmd --permanent --zone=public --add-port=45564/tcp
$ firewall-cmd --permanent --zone=public --add-port=45564/udp
$ firewall-cmd --permanent --zone=public --add-port=4000-4100/tcp
$ firewall-cmd --reload
```

저는 4000, 4001, 4002 포트를 열어줬습니다.

```shell
$ firwall-cmd --list-all

public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0 eth1
  sources:
  services: dhcpv6-client http ssh
  ports: 8080/tcp 18080/tcp 28080/tcp 45564/tcp 45564/udp 4000/tcp 4001/tcp 4002/tcp
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

Tomcat 인스턴스를 모두 실행 시킨뒤 *logs/catalina.out* 에서 각각의 로그를 확인해서 아래와 같이 출력이 되면 Session Clustering 이 연결됐다는 의미입니다.

> WAS1

```log
27-Apr-2020 05:21:20.581 INFO [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded Replication member added:[org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4001,{127, 0, 0, 1},4001, alive=1005, securePort=-1, UDP Port=-1, id={31 -32 -28 10 -89 -127 74 -105 -73 -39 57 56 -3 -95 -119 111 }, payload={}, command={}, domain={}]]
27-Apr-2020 05:21:37.671 INFO [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded Replication member added:[org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4002,{127, 0, 0, 1},4002, alive=1005, securePort=-1, UDP Port=-1, id={-64 85 -22 113 -108 106 66 -125 -104 -64 -67 -20 49 -70 -92 -82 }, payload={}, command={}, domain={}]]
```

> WAS2

```log
27-Apr-2020 05:21:19.760 정보 [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded 복제 멤버가 추가됨: [org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4000,{127, 0, 0, 1},4000, alive=15222, securePort=-1, UDP Port=-1, id={29 53 30 -57 -95 -30 69 81 -120 -60 80 48 81 70 -102 -125 }, payload={}, command={}, domain={}]]
27-Apr-2020 05:21:37.671 정보 [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded 복제 멤버가 추가됨: [org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4002,{127, 0, 0, 1},4002, alive=1005, securePort=-1, UDP Port=-1, id={-64 85 -22 113 -108 106 66 -125 -104 -64 -67 -20 49 -70 -92 -82 }, payload={}, command={}, domain={}]]
```

> WAS3

```log
27-Apr-2020 05:21:36.782 정보 [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded 복제 멤버가 추가됨: [org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4001,{127, 0, 0, 1},4001, alive=17204, securePort=-1, UDP Port=-1, id={31 -32 -28 10 -89 -127 74 -105 -73 -39 57 56 -3 -95 -119 111 }, payload={}, command={}, domain={}]]
27-Apr-2020 05:21:36.876 정보 [Membership-MemberAdded.] org.apache.catalina.ha.tcp.SimpleTcpCluster.memberAdded 복제 멤버가 추가됨: [org.apache.catalina.tribes.membership.MemberImpl[tcp://{127, 0, 0, 1}:4000,{127, 0, 0, 1},4000, alive=32344, securePort=-1, UDP Port=-1, id={29 53 30 -57 -95 -30 69 81 -120 -60 80 48 81 70 -102 -125 }, payload={}, command={}, domain={}]]
```

http://10.30.30.2 로 접속해서 결과를 확인해보겠습니다.

WAS1 -> tomcat1, WAS2 -> instance1, WAS3 -> instance2 로 보시면 됩니다.

> WAS 1

![image](https://user-images.githubusercontent.com/44635266/81064508-c5de0080-8f14-11ea-87b8-8c129c0e9531.png)

> WAS 2

![image](https://user-images.githubusercontent.com/44635266/81064549-d7270d00-8f14-11ea-9ed1-7059342aa855.png)

> WAS 3 

![image](https://user-images.githubusercontent.com/44635266/81064572-dee6b180-8f14-11ea-8468-2eb6964b8039.png)

