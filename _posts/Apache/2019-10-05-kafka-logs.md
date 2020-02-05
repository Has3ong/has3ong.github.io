---
title : Kafka, Zookeeper Server Start Log
---

* Zookeeper Server Start

```
[2019-10-03 00:56:31,984] INFO Reading configuration from: /usr/local/Cellar/kafka/2.3.0/libexec/config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
[2019-10-03 00:56:31,986] INFO autopurge.snapRetainCount set to 3 (org.apache.zookeeper.server.DatadirCleanupManager)
[2019-10-03 00:56:31,987] INFO autopurge.purgeInterval set to 0 (org.apache.zookeeper.server.DatadirCleanupManager)
[2019-10-03 00:56:31,987] INFO Purge task is not scheduled. (org.apache.zookeeper.server.DatadirCleanupManager)
[2019-10-03 00:56:31,987] WARN Either no config or no quorum defined in config, running  in standalone mode (org.apache.zookeeper.server.quorum.QuorumPeerMain)
[2019-10-03 00:56:31,998] INFO Reading configuration from: /usr/local/Cellar/kafka/2.3.0/libexec/config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
[2019-10-03 00:56:31,998] INFO Starting server (org.apache.zookeeper.server.ZooKeeperServerMain)
[2019-10-03 00:56:32,004] INFO Server environment:zookeeper.version=3.4.14-4c25d480e66aadd371de8bd2fd8da255ac140bcf, built on 03/06/2019 16:18 GMT (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,004] INFO Server environment:host.name=218.38.137.27 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,004] INFO Server environment:java.version=1.8.0_222 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,004] INFO Server environment:java.vendor=AdoptOpenJDK (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,004] INFO Server environment:java.home=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,004] INFO Server environment:java.class.path=/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/activation-1.1.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/aopalliance-repackaged-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/argparse4j-0.7.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/audience-annotations-0.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/commons-lang3-3.8.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-api-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-basic-auth-extension-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-file-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-json-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-runtime-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-transforms-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/guava-20.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-api-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-locator-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-utils-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-annotations-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-core-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-databind-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-dataformat-csv-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-datatype-jdk8-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-jaxrs-base-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-jaxrs-json-provider-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-jaxb-annotations-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-paranamer-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-scala_2.12-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.annotation-api-1.3.4.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.inject-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.ws.rs-api-2.1.5.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javassist-3.22.0-CR2.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javax.servlet-api-3.1.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javax.ws.rs-api-2.1.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jaxb-api-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-client-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-common-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-container-servlet-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-container-servlet-core-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-hk2-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-media-jaxb-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-server-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-client-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-continuation-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-http-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-io-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-security-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-server-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-servlet-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-servlets-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-util-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jopt-simple-5.0.4.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jsr305-3.0.2.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-clients-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-log4j-appender-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-examples-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-scala_2.12-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-test-utils-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-tools-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka_2.12-2.3.0-sources.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka_2.12-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/log4j-1.2.17.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/lz4-java-1.6.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/maven-artifact-3.6.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/metrics-core-2.2.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/osgi-resource-locator-1.0.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/paranamer-2.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/plexus-utils-3.2.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/reflections-0.9.11.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/rocksdbjni-5.18.3.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-library-2.12.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-logging_2.12-3.9.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-reflect-2.12.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/slf4j-api-1.7.26.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/slf4j-log4j12-1.7.26.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/snappy-java-1.1.7.3.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/spotbugs-annotations-3.1.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/validation-api-2.0.1.Final.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zkclient-0.11.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zookeeper-3.4.14.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zstd-jni-1.4.0-1.jar (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:java.library.path=/Users/has3ong/Library/Java/Extensions:/Library/Java/Extensions:/Network/Library/Java/Extensions:/System/Library/Java/Extensions:/usr/lib/java:. (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:java.io.tmpdir=/var/folders/yq/4wxz887d6sb1xh2zqf9l4_100000gn/T/ (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:java.compiler=<NA> (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:os.name=Mac OS X (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:os.arch=x86_64 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:os.version=10.14.6 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:user.name=has3ong (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:user.home=/Users/has3ong (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,005] INFO Server environment:user.dir=/Users/has3ong (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,010] INFO tickTime set to 3000 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,010] INFO minSessionTimeout set to -1 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,010] INFO maxSessionTimeout set to -1 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:56:32,019] INFO Using org.apache.zookeeper.server.NIOServerCnxnFactory as server connection factory (org.apache.zookeeper.server.ServerCnxnFactory)
[2019-10-03 00:56:32,029] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)
```

* Kafka Server Start

```
[2019-10-03 00:58:52,318] INFO Registered kafka:type=kafka.Log4jController MBean (kafka.utils.Log4jControllerRegistration$)
[2019-10-03 00:58:52,725] INFO Registered signal handlers for TERM, INT, HUP (org.apache.kafka.common.utils.LoggingSignalHandler)
[2019-10-03 00:58:52,725] INFO starting (kafka.server.KafkaServer)
[2019-10-03 00:58:52,726] INFO Connecting to zookeeper on localhost:2181 (kafka.server.KafkaServer)
[2019-10-03 00:58:52,741] INFO [ZooKeeperClient Kafka server] Initializing a new session to localhost:2181. (kafka.zookeeper.ZooKeeperClient)
[2019-10-03 00:58:52,745] INFO Client environment:zookeeper.version=3.4.14-4c25d480e66aadd371de8bd2fd8da255ac140bcf, built on 03/06/2019 16:18 GMT (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,745] INFO Client environment:host.name=218.38.137.27 (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,745] INFO Client environment:java.version=1.8.0_222 (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,745] INFO Client environment:java.vendor=AdoptOpenJDK (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,745] INFO Client environment:java.home=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,745] INFO Client environment:java.class.path=/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/activation-1.1.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/aopalliance-repackaged-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/argparse4j-0.7.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/audience-annotations-0.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/commons-lang3-3.8.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-api-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-basic-auth-extension-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-file-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-json-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-runtime-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/connect-transforms-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/guava-20.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-api-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-locator-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/hk2-utils-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-annotations-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-core-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-databind-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-dataformat-csv-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-datatype-jdk8-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-jaxrs-base-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-jaxrs-json-provider-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-jaxb-annotations-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-paranamer-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jackson-module-scala_2.12-2.9.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.annotation-api-1.3.4.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.inject-2.5.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jakarta.ws.rs-api-2.1.5.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javassist-3.22.0-CR2.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javax.servlet-api-3.1.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/javax.ws.rs-api-2.1.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jaxb-api-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-client-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-common-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-container-servlet-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-container-servlet-core-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-hk2-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-media-jaxb-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jersey-server-2.28.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-client-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-continuation-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-http-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-io-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-security-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-server-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-servlet-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-servlets-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jetty-util-9.4.18.v20190429.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jopt-simple-5.0.4.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/jsr305-3.0.2.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-clients-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-log4j-appender-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-examples-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-scala_2.12-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-streams-test-utils-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka-tools-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka_2.12-2.3.0-sources.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/kafka_2.12-2.3.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/log4j-1.2.17.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/lz4-java-1.6.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/maven-artifact-3.6.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/metrics-core-2.2.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/osgi-resource-locator-1.0.1.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/paranamer-2.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/plexus-utils-3.2.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/reflections-0.9.11.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/rocksdbjni-5.18.3.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-library-2.12.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-logging_2.12-3.9.0.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/scala-reflect-2.12.8.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/slf4j-api-1.7.26.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/slf4j-log4j12-1.7.26.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/snappy-java-1.1.7.3.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/spotbugs-annotations-3.1.9.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/validation-api-2.0.1.Final.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zkclient-0.11.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zookeeper-3.4.14.jar:/usr/local/Cellar/kafka/2.3.0/libexec/bin/../libs/zstd-jni-1.4.0-1.jar (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:java.library.path=/Users/has3ong/Library/Java/Extensions:/Library/Java/Extensions:/Network/Library/Java/Extensions:/System/Library/Java/Extensions:/usr/lib/java:. (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:java.io.tmpdir=/var/folders/yq/4wxz887d6sb1xh2zqf9l4_100000gn/T/ (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:java.compiler=<NA> (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:os.name=Mac OS X (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:os.arch=x86_64 (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:os.version=10.14.6 (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:user.name=has3ong (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:user.home=/Users/has3ong (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,746] INFO Client environment:user.dir=/Users/has3ong (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,747] INFO Initiating client connection, connectString=localhost:2181 sessionTimeout=6000 watcher=kafka.zookeeper.ZooKeeperClient$ZooKeeperClientWatcher$@6a400542 (org.apache.zookeeper.ZooKeeper)
[2019-10-03 00:58:52,759] INFO [ZooKeeperClient Kafka server] Waiting until connected. (kafka.zookeeper.ZooKeeperClient)
[2019-10-03 00:58:52,760] INFO Opening socket connection to server localhost/0:0:0:0:0:0:0:1:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2019-10-03 00:58:52,777] INFO Socket connection established to localhost/0:0:0:0:0:0:0:1:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2019-10-03 00:58:52,783] INFO Session establishment complete on server localhost/0:0:0:0:0:0:0:1:2181, sessionid = 0x1000ca950fd0002, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2019-10-03 00:58:52,785] INFO [ZooKeeperClient Kafka server] Connected. (kafka.zookeeper.ZooKeeperClient)
[2019-10-03 00:58:52,958] INFO Cluster ID = FLY7J5tCTau1ZW_-024NMQ (kafka.server.KafkaServer)
[2019-10-03 00:58:53,017] INFO KafkaConfig values:
	advertised.host.name = localhost
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	alter.log.dirs.replication.quota.window.num = 11
	alter.log.dirs.replication.quota.window.size.seconds = 1
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 0
	broker.id.generation.enable = true
	broker.rack = null
	client.quota.callback.class = null
	compression.type = producer
	connection.failed.authentication.delay.ms = 100
	connections.max.idle.ms = 600000
	connections.max.reauth.ms = 0
	control.plane.listener.name = null
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 1
	delegation.token.expiry.check.interval.ms = 3600000
	delegation.token.expiry.time.ms = 86400000
	delegation.token.master.key = null
	delegation.token.max.lifetime.ms = 604800000
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 1800000
	group.max.size = 2147483647
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 2.3-IV1
	kafka.metrics.polling.interval.secs = 10
	kafka.metrics.reporters = []
	leader.imbalance.check.interval.seconds = 300
	leader.imbalance.per.broker.percentage = 10
	listener.security.protocol.map = PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
	listeners = null
	log.cleaner.backoff.ms = 15000
	log.cleaner.dedupe.buffer.size = 134217728
	log.cleaner.delete.retention.ms = 86400000
	log.cleaner.enable = true
	log.cleaner.io.buffer.load.factor = 0.9
	log.cleaner.io.buffer.size = 524288
	log.cleaner.io.max.bytes.per.second = 1.7976931348623157E308
	log.cleaner.max.compaction.lag.ms = 9223372036854775807
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /usr/local/var/lib/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.downconversion.enable = true
	log.message.format.version = 2.3-IV1
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = null
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections = 2147483647
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	max.incremental.fetch.session.cache.slots = 1000
	message.max.bytes = 1000012
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 1
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.alter.log.dirs.threads = null
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 10080
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
	password.encoder.cipher.algorithm = AES/CBC/PKCS5Padding
	password.encoder.iterations = 4096
	password.encoder.key.length = 128
	password.encoder.keyfactory.algorithm = null
	password.encoder.old.secret = null
	password.encoder.secret = null
	port = 9092
	principal.builder.class = null
	producer.purgatory.purge.interval.requests = 1000
	queued.max.request.bytes = -1
	queued.max.requests = 500
	quota.consumer.default = 9223372036854775807
	quota.producer.default = 9223372036854775807
	quota.window.num = 11
	quota.window.size.seconds = 1
	replica.fetch.backoff.ms = 1000
	replica.fetch.max.bytes = 1048576
	replica.fetch.min.bytes = 1
	replica.fetch.response.max.bytes = 10485760
	replica.fetch.wait.max.ms = 500
	replica.high.watermark.checkpoint.interval.ms = 5000
	replica.lag.time.max.ms = 10000
	replica.socket.receive.buffer.bytes = 65536
	replica.socket.timeout.ms = 30000
	replication.quota.window.num = 11
	replication.quota.window.size.seconds = 1
	request.timeout.ms = 30000
	reserved.broker.max.id = 1000
	sasl.client.callback.handler.class = null
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.jaas.config = null
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.login.callback.handler.class = null
	sasl.login.class = null
	sasl.login.refresh.buffer.seconds = 300
	sasl.login.refresh.min.period.seconds = 60
	sasl.login.refresh.window.factor = 0.8
	sasl.login.refresh.window.jitter = 0.05
	sasl.mechanism.inter.broker.protocol = GSSAPI
	sasl.server.callback.handler.class = null
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = []
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = https
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
	ssl.principal.mapping.rules = [DEFAULT]
	ssl.protocol = TLS
	ssl.provider = null
	ssl.secure.random.implementation = null
	ssl.trustmanager.algorithm = PKIX
	ssl.truststore.location = null
	ssl.truststore.password = null
	ssl.truststore.type = JKS
	transaction.abort.timed.out.transaction.cleanup.interval.ms = 60000
	transaction.max.timeout.ms = 900000
	transaction.remove.expired.transaction.cleanup.interval.ms = 3600000
	transaction.state.log.load.buffer.size = 5242880
	transaction.state.log.min.isr = 1
	transaction.state.log.num.partitions = 50
	transaction.state.log.replication.factor = 1
	transaction.state.log.segment.bytes = 104857600
	transactional.id.expiration.ms = 604800000
	unclean.leader.election.enable = false
	zookeeper.connect = localhost:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.max.in.flight.requests = 10
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-03 00:58:53,025] INFO KafkaConfig values:
	advertised.host.name = localhost
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	alter.log.dirs.replication.quota.window.num = 11
	alter.log.dirs.replication.quota.window.size.seconds = 1
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 0
	broker.id.generation.enable = true
	broker.rack = null
	client.quota.callback.class = null
	compression.type = producer
	connection.failed.authentication.delay.ms = 100
	connections.max.idle.ms = 600000
	connections.max.reauth.ms = 0
	control.plane.listener.name = null
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 1
	delegation.token.expiry.check.interval.ms = 3600000
	delegation.token.expiry.time.ms = 86400000
	delegation.token.master.key = null
	delegation.token.max.lifetime.ms = 604800000
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 1800000
	group.max.size = 2147483647
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 2.3-IV1
	kafka.metrics.polling.interval.secs = 10
	kafka.metrics.reporters = []
	leader.imbalance.check.interval.seconds = 300
	leader.imbalance.per.broker.percentage = 10
	listener.security.protocol.map = PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
	listeners = null
	log.cleaner.backoff.ms = 15000
	log.cleaner.dedupe.buffer.size = 134217728
	log.cleaner.delete.retention.ms = 86400000
	log.cleaner.enable = true
	log.cleaner.io.buffer.load.factor = 0.9
	log.cleaner.io.buffer.size = 524288
	log.cleaner.io.max.bytes.per.second = 1.7976931348623157E308
	log.cleaner.max.compaction.lag.ms = 9223372036854775807
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /usr/local/var/lib/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.downconversion.enable = true
	log.message.format.version = 2.3-IV1
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = null
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections = 2147483647
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	max.incremental.fetch.session.cache.slots = 1000
	message.max.bytes = 1000012
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 1
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.alter.log.dirs.threads = null
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 10080
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
	password.encoder.cipher.algorithm = AES/CBC/PKCS5Padding
	password.encoder.iterations = 4096
	password.encoder.key.length = 128
	password.encoder.keyfactory.algorithm = null
	password.encoder.old.secret = null
	password.encoder.secret = null
	port = 9092
	principal.builder.class = null
	producer.purgatory.purge.interval.requests = 1000
	queued.max.request.bytes = -1
	queued.max.requests = 500
	quota.consumer.default = 9223372036854775807
	quota.producer.default = 9223372036854775807
	quota.window.num = 11
	quota.window.size.seconds = 1
	replica.fetch.backoff.ms = 1000
	replica.fetch.max.bytes = 1048576
	replica.fetch.min.bytes = 1
	replica.fetch.response.max.bytes = 10485760
	replica.fetch.wait.max.ms = 500
	replica.high.watermark.checkpoint.interval.ms = 5000
	replica.lag.time.max.ms = 10000
	replica.socket.receive.buffer.bytes = 65536
	replica.socket.timeout.ms = 30000
	replication.quota.window.num = 11
	replication.quota.window.size.seconds = 1
	request.timeout.ms = 30000
	reserved.broker.max.id = 1000
	sasl.client.callback.handler.class = null
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.jaas.config = null
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.login.callback.handler.class = null
	sasl.login.class = null
	sasl.login.refresh.buffer.seconds = 300
	sasl.login.refresh.min.period.seconds = 60
	sasl.login.refresh.window.factor = 0.8
	sasl.login.refresh.window.jitter = 0.05
	sasl.mechanism.inter.broker.protocol = GSSAPI
	sasl.server.callback.handler.class = null
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = []
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = https
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
	ssl.principal.mapping.rules = [DEFAULT]
	ssl.protocol = TLS
	ssl.provider = null
	ssl.secure.random.implementation = null
	ssl.trustmanager.algorithm = PKIX
	ssl.truststore.location = null
	ssl.truststore.password = null
	ssl.truststore.type = JKS
	transaction.abort.timed.out.transaction.cleanup.interval.ms = 60000
	transaction.max.timeout.ms = 900000
	transaction.remove.expired.transaction.cleanup.interval.ms = 3600000
	transaction.state.log.load.buffer.size = 5242880
	transaction.state.log.min.isr = 1
	transaction.state.log.num.partitions = 50
	transaction.state.log.replication.factor = 1
	transaction.state.log.segment.bytes = 104857600
	transactional.id.expiration.ms = 604800000
	unclean.leader.election.enable = false
	zookeeper.connect = localhost:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.max.in.flight.requests = 10
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-03 00:58:53,045] INFO [ThrottledChannelReaper-Produce]: Starting (kafka.server.ClientQuotaManager$ThrottledChannelReaper)
[2019-10-03 00:58:53,046] INFO [ThrottledChannelReaper-Fetch]: Starting (kafka.server.ClientQuotaManager$ThrottledChannelReaper)
[2019-10-03 00:58:53,046] INFO [ThrottledChannelReaper-Request]: Starting (kafka.server.ClientQuotaManager$ThrottledChannelReaper)
[2019-10-03 00:58:53,079] INFO Loading logs. (kafka.log.LogManager)
[2019-10-03 00:58:53,147] INFO [Log partition=__consumer_offsets-9, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 3 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,157] INFO [ProducerStateManager partition=__consumer_offsets-9] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/__consumer_offsets-9/00000000000000000003.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,168] INFO [Log partition=__consumer_offsets-9, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 3 in 65 ms (kafka.log.Log)
[2019-10-03 00:58:53,179] INFO [Log partition=__consumer_offsets-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,181] INFO [Log partition=__consumer_offsets-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 6 ms (kafka.log.Log)
[2019-10-03 00:58:53,186] INFO [Log partition=__consumer_offsets-7, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,187] INFO [Log partition=__consumer_offsets-7, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,193] INFO [Log partition=__consumer_offsets-31, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,193] INFO [Log partition=__consumer_offsets-31, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,198] INFO [Log partition=__consumer_offsets-36, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,198] INFO [Log partition=__consumer_offsets-36, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,203] INFO [Log partition=__consumer_offsets-38, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,203] INFO [Log partition=__consumer_offsets-38, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,209] INFO [Log partition=__consumer_offsets-6, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,209] INFO [Log partition=__consumer_offsets-6, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,214] INFO [Log partition=__consumer_offsets-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,215] INFO [Log partition=__consumer_offsets-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,219] INFO [Log partition=__consumer_offsets-8, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,219] INFO [Log partition=__consumer_offsets-8, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,226] INFO [Log partition=__consumer_offsets-39, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,226] INFO [Log partition=__consumer_offsets-39, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,231] INFO [Log partition=__consumer_offsets-37, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,231] INFO [Log partition=__consumer_offsets-37, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,235] INFO [Log partition=__consumer_offsets-30, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,236] INFO [Log partition=__consumer_offsets-30, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,243] INFO [Log partition=wordcount-application-Counts-changelog-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 23 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,243] INFO [ProducerStateManager partition=wordcount-application-Counts-changelog-1] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/wordcount-application-Counts-changelog-1/00000000000000000023.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,244] INFO [Log partition=wordcount-application-Counts-changelog-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 23 in 6 ms (kafka.log.Log)
[2019-10-03 00:58:53,249] INFO [Log partition=wordcount-application-Counts-changelog-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 15 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,249] INFO [ProducerStateManager partition=wordcount-application-Counts-changelog-0] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/wordcount-application-Counts-changelog-0/00000000000000000015.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,249] INFO [Log partition=wordcount-application-Counts-changelog-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 15 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,255] INFO [Log partition=test-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 2 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,255] INFO [ProducerStateManager partition=test-1] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/test-1/00000000000000000002.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,256] INFO [Log partition=test-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 2 in 5 ms (kafka.log.Log)
[2019-10-03 00:58:53,261] INFO [Log partition=test-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 3 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,262] INFO [ProducerStateManager partition=test-0] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/test-0/00000000000000000003.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,262] INFO [Log partition=test-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 3 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,266] INFO [Log partition=__consumer_offsets-12, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,267] INFO [Log partition=__consumer_offsets-12, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,270] INFO [Log partition=__consumer_offsets-15, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,270] INFO [Log partition=__consumer_offsets-15, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,276] INFO [Log partition=__consumer_offsets-23, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,277] INFO [Log partition=__consumer_offsets-23, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,282] INFO [Log partition=__consumer_offsets-24, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 11 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,283] INFO [ProducerStateManager partition=__consumer_offsets-24] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/__consumer_offsets-24/00000000000000000011.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,283] INFO [Log partition=__consumer_offsets-24, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 2 segments, log start offset 0 and log end offset 11 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,287] INFO [Log partition=__consumer_offsets-48, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,287] INFO [Log partition=__consumer_offsets-48, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,293] INFO [Log partition=__consumer_offsets-41, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,293] INFO [Log partition=__consumer_offsets-41, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,297] INFO [Log partition=__consumer_offsets-46, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,297] INFO [Log partition=__consumer_offsets-46, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,301] INFO [Log partition=__consumer_offsets-25, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,301] INFO [Log partition=__consumer_offsets-25, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,307] INFO [Log partition=__consumer_offsets-22, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,307] INFO [Log partition=__consumer_offsets-22, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,312] INFO [Log partition=__consumer_offsets-14, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,312] INFO [Log partition=__consumer_offsets-14, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,316] INFO [Log partition=__consumer_offsets-13, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,316] INFO [Log partition=__consumer_offsets-13, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,320] INFO [Log partition=__consumer_offsets-47, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,320] INFO [Log partition=__consumer_offsets-47, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,325] INFO [Log partition=__consumer_offsets-40, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,326] INFO [Log partition=__consumer_offsets-40, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,329] INFO [Log partition=__consumer_offsets-49, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,330] INFO [Log partition=__consumer_offsets-49, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,333] INFO [Log partition=__consumer_offsets-35, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,333] INFO [Log partition=__consumer_offsets-35, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,337] INFO [Log partition=__consumer_offsets-32, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,337] INFO [Log partition=__consumer_offsets-32, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,342] INFO [Log partition=word-count-input-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 4 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,343] INFO [ProducerStateManager partition=word-count-input-0] Writing producer snapshot at offset 4 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,344] INFO [Log partition=word-count-input-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 4 and log end offset 4 in 5 ms (kafka.log.Log)
[2019-10-03 00:58:53,348] INFO [Log partition=__consumer_offsets-4, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,348] INFO [Log partition=__consumer_offsets-4, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,351] INFO [Log partition=__consumer_offsets-3, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,351] INFO [Log partition=__consumer_offsets-3, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,356] INFO [Log partition=__consumer_offsets-33, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,356] INFO [Log partition=__consumer_offsets-33, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,360] INFO [Log partition=__consumer_offsets-34, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,360] INFO [Log partition=__consumer_offsets-34, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,364] INFO [Log partition=__consumer_offsets-2, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,364] INFO [Log partition=__consumer_offsets-2, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,367] INFO [Log partition=__consumer_offsets-5, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,367] INFO [Log partition=__consumer_offsets-5, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,370] INFO [Log partition=word-count-input-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 4 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,371] INFO [ProducerStateManager partition=word-count-input-1] Writing producer snapshot at offset 4 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,371] INFO [Log partition=word-count-input-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 4 and log end offset 4 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,375] INFO [Log partition=wordcount-application-Counts-repartition-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 61 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,376] INFO [ProducerStateManager partition=wordcount-application-Counts-repartition-1] Writing producer snapshot at offset 61 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,376] INFO [Log partition=wordcount-application-Counts-repartition-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 61 and log end offset 61 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,379] INFO [Log partition=wordcount-application-Counts-repartition-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 34 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,401] INFO [ProducerStateManager partition=wordcount-application-Counts-repartition-0] Writing producer snapshot at offset 34 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,402] INFO [Log partition=wordcount-application-Counts-repartition-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 34 and log end offset 34 in 25 ms (kafka.log.Log)
[2019-10-03 00:58:53,407] INFO [Log partition=test-2, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 2 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,408] INFO [ProducerStateManager partition=test-2] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/test-2/00000000000000000002.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,408] INFO [Log partition=test-2, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 2 in 5 ms (kafka.log.Log)
[2019-10-03 00:58:53,412] INFO [Log partition=word-count-output-1, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 23 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,413] INFO [ProducerStateManager partition=word-count-output-1] Writing producer snapshot at offset 23 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,413] INFO [Log partition=word-count-output-1, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 23 and log end offset 23 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,416] INFO [Log partition=word-count-output-0, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 15 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,416] INFO [ProducerStateManager partition=word-count-output-0] Writing producer snapshot at offset 15 (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,417] INFO [Log partition=word-count-output-0, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 15 and log end offset 15 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,421] INFO [Log partition=test-3, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 3 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,421] INFO [ProducerStateManager partition=test-3] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/test-3/00000000000000000003.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,422] INFO [Log partition=test-3, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 3 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,425] INFO [Log partition=__consumer_offsets-45, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,426] INFO [Log partition=__consumer_offsets-45, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,429] INFO [Log partition=__consumer_offsets-42, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,429] INFO [Log partition=__consumer_offsets-42, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,432] INFO [Log partition=__consumer_offsets-29, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,433] INFO [Log partition=__consumer_offsets-29, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,436] INFO [Log partition=__consumer_offsets-16, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,436] INFO [Log partition=__consumer_offsets-16, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,440] INFO [Log partition=__consumer_offsets-11, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,440] INFO [Log partition=__consumer_offsets-11, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,443] INFO [Log partition=__consumer_offsets-18, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,444] INFO [Log partition=__consumer_offsets-18, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,447] INFO [Log partition=__consumer_offsets-27, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,447] INFO [Log partition=__consumer_offsets-27, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,450] INFO [Log partition=__consumer_offsets-20, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,450] INFO [Log partition=__consumer_offsets-20, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,454] INFO [Log partition=__consumer_offsets-43, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,454] INFO [Log partition=__consumer_offsets-43, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,458] INFO [Log partition=__consumer_offsets-44, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 2 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,459] INFO [ProducerStateManager partition=__consumer_offsets-44] Loading producer state from snapshot file '/usr/local/var/lib/kafka-logs/__consumer_offsets-44/00000000000000000002.snapshot' (kafka.log.ProducerStateManager)
[2019-10-03 00:58:53,459] INFO [Log partition=__consumer_offsets-44, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 2 in 4 ms (kafka.log.Log)
[2019-10-03 00:58:53,462] INFO [Log partition=__consumer_offsets-21, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,463] INFO [Log partition=__consumer_offsets-21, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,466] INFO [Log partition=__consumer_offsets-19, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,466] INFO [Log partition=__consumer_offsets-19, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,469] INFO [Log partition=__consumer_offsets-26, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,469] INFO [Log partition=__consumer_offsets-26, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,473] INFO [Log partition=__consumer_offsets-10, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,473] INFO [Log partition=__consumer_offsets-10, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 3 ms (kafka.log.Log)
[2019-10-03 00:58:53,477] INFO [Log partition=__consumer_offsets-28, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,477] INFO [Log partition=__consumer_offsets-28, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,480] INFO [Log partition=__consumer_offsets-17, dir=/usr/local/var/lib/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2019-10-03 00:58:53,480] INFO [Log partition=__consumer_offsets-17, dir=/usr/local/var/lib/kafka-logs] Completed load of log with 1 segments, log start offset 0 and log end offset 0 in 2 ms (kafka.log.Log)
[2019-10-03 00:58:53,482] INFO Logs loading complete in 403 ms. (kafka.log.LogManager)
[2019-10-03 00:58:53,493] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2019-10-03 00:58:53,494] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2019-10-03 00:58:53,716] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2019-10-03 00:58:53,736] INFO [SocketServer brokerId=0] Created data-plane acceptor and processors for endpoint : EndPoint(null,9092,ListenerName(PLAINTEXT),PLAINTEXT) (kafka.network.SocketServer)
[2019-10-03 00:58:53,738] INFO [SocketServer brokerId=0] Started 1 acceptor threads for data-plane (kafka.network.SocketServer)
[2019-10-03 00:58:53,759] INFO [ExpirationReaper-0-Produce]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,759] INFO [ExpirationReaper-0-Fetch]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,760] INFO [ExpirationReaper-0-DeleteRecords]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,760] INFO [ExpirationReaper-0-ElectPreferredLeader]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,770] INFO [LogDirFailureHandler]: Starting (kafka.server.ReplicaManager$LogDirFailureHandler)
[2019-10-03 00:58:53,815] INFO Creating /brokers/ids/0 (is it secure? false) (kafka.zk.KafkaZkClient)
[2019-10-03 00:58:53,825] INFO Stat of the created znode at /brokers/ids/0 is: 1304,1304,1570031933822,1570031933822,1,0,0,72071515385692162,188,0,1304
 (kafka.zk.KafkaZkClient)
[2019-10-03 00:58:53,826] INFO Registered broker 0 at path /brokers/ids/0 with addresses: ArrayBuffer(EndPoint(localhost,9092,ListenerName(PLAINTEXT),PLAINTEXT)), czxid (broker epoch): 1304 (kafka.zk.KafkaZkClient)
[2019-10-03 00:58:53,869] INFO [ExpirationReaper-0-topic]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,871] INFO [ExpirationReaper-0-Heartbeat]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,871] INFO [ExpirationReaper-0-Rebalance]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-03 00:58:53,895] INFO [GroupCoordinator 0]: Starting up. (kafka.coordinator.group.GroupCoordinator)
[2019-10-03 00:58:53,896] INFO [GroupCoordinator 0]: Startup complete. (kafka.coordinator.group.GroupCoordinator)
[2019-10-03 00:58:53,899] INFO [GroupMetadataManager brokerId=0] Removed 0 expired offsets in 4 milliseconds. (kafka.coordinator.group.GroupMetadataManager)
[2019-10-03 00:58:53,907] INFO [ProducerId Manager 0]: Acquired new producerId block (brokerId:0,blockStartProducerId:7000,blockEndProducerId:7999) by writing to Zk with path version 8 (kafka.coordinator.transaction.ProducerIdManager)
[2019-10-03 00:58:53,935] INFO [TransactionCoordinator id=0] Starting up. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-03 00:58:53,936] INFO [Transaction Marker Channel Manager 0]: Starting (kafka.coordinator.transaction.TransactionMarkerChannelManager)
[2019-10-03 00:58:53,936] INFO [TransactionCoordinator id=0] Startup complete. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-03 00:58:53,978] INFO [/config/changes-event-process-thread]: Starting (kafka.common.ZkNodeChangeNotificationListener$ChangeEventProcessThread)
[2019-10-03 00:58:54,000] INFO [SocketServer brokerId=0] Started data-plane processors for 1 acceptors (kafka.network.SocketServer)
[2019-10-03 00:58:54,005] INFO Kafka version: 2.3.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-03 00:58:54,005] INFO Kafka commitId: fc1aaa116b661c8a (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-03 00:58:54,005] INFO Kafka startTimeMs: 1570031934001 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-03 00:58:54,007] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
```

* After Kafka Server Start, Zookeeper Log

```
[2019-10-03 00:57:24,074] INFO Accepted socket connection from /0:0:0:0:0:0:0:1:61685 (org.apache.zookeeper.server.NIOServerCnxnFactory)
[2019-10-03 00:57:24,083] INFO Client attempting to establish new session at /0:0:0:0:0:0:0:1:61685 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:57:24,084] INFO Creating new log file: log.4e4 (org.apache.zookeeper.server.persistence.FileTxnLog)
[2019-10-03 00:57:24,090] INFO Established session 0x1000ca950fd0000 with negotiated timeout 6000 for client /0:0:0:0:0:0:0:1:61685 (org.apache.zookeeper.server.ZooKeeperServer)
[2019-10-03 00:57:24,137] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x1 zxid:0x4e5 txntype:-1 reqpath:n/a Error Path:/consumers Error:KeeperErrorCode = NodeExists for /consumers (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,146] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x2 zxid:0x4e6 txntype:-1 reqpath:n/a Error Path:/brokers/ids Error:KeeperErrorCode = NodeExists for /brokers/ids (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,147] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x3 zxid:0x4e7 txntype:-1 reqpath:n/a Error Path:/brokers/topics Error:KeeperErrorCode = NodeExists for /brokers/topics (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,148] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x4 zxid:0x4e8 txntype:-1 reqpath:n/a Error Path:/config/changes Error:KeeperErrorCode = NodeExists for /config/changes (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,149] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x5 zxid:0x4e9 txntype:-1 reqpath:n/a Error Path:/admin/delete_topics Error:KeeperErrorCode = NodeExists for /admin/delete_topics (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,150] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x6 zxid:0x4ea txntype:-1 reqpath:n/a Error Path:/brokers/seqid Error:KeeperErrorCode = NodeExists for /brokers/seqid (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,151] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x7 zxid:0x4eb txntype:-1 reqpath:n/a Error Path:/isr_change_notification Error:KeeperErrorCode = NodeExists for /isr_change_notification (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,152] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x8 zxid:0x4ec txntype:-1 reqpath:n/a Error Path:/latest_producer_id_block Error:KeeperErrorCode = NodeExists for /latest_producer_id_block (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,153] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0x9 zxid:0x4ed txntype:-1 reqpath:n/a Error Path:/log_dir_event_notification Error:KeeperErrorCode = NodeExists for /log_dir_event_notification (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,154] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0xa zxid:0x4ee txntype:-1 reqpath:n/a Error Path:/config/topics Error:KeeperErrorCode = NodeExists for /config/topics (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,155] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0xb zxid:0x4ef txntype:-1 reqpath:n/a Error Path:/config/clients Error:KeeperErrorCode = NodeExists for /config/clients (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,156] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0xc zxid:0x4f0 txntype:-1 reqpath:n/a Error Path:/config/users Error:KeeperErrorCode = NodeExists for /config/users (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:24,157] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:create cxid:0xd zxid:0x4f1 txntype:-1 reqpath:n/a Error Path:/config/brokers Error:KeeperErrorCode = NodeExists for /config/brokers (org.apache.zookeeper.server.PrepRequestProcessor)
[2019-10-03 00:57:25,454] INFO Got user-level KeeperException when processing sessionid:0x1000ca950fd0000 type:multi cxid:0x7e zxid:0x4f5 txntype:-1 reqpath:n/a aborting remaining multi ops. Error Path:/admin/preferred_replica_election Error:KeeperErrorCode = NoNode for /admin/preferred_replica_election (org.apache.zookeeper.server.PrepRequestProcessor)
```
