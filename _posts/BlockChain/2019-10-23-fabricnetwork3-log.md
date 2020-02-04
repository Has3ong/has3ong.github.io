---
title : Hyperledger Network 로그
---

> docker-compose -f docker-compose-kafka.yaml up

> Orderer

```
2019-10-22 17:11:34.859 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 17:11:34.928 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
	General.LedgerType = "file"
	General.ListenAddress = "0.0.0.0"
	General.ListenPort = 7050
	General.TLS.Enabled = true
	General.TLS.PrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.TLS.Certificate = "/var/hyperledger/orderer/tls/server.crt"
	General.TLS.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
	General.TLS.ClientAuthRequired = false
	General.TLS.ClientRootCAs = []
	General.Cluster.ListenAddress = ""
	General.Cluster.ListenPort = 0
	General.Cluster.ServerCertificate = ""
	General.Cluster.ServerPrivateKey = ""
	General.Cluster.ClientCertificate = ""
	General.Cluster.ClientPrivateKey = ""
	General.Cluster.RootCAs = []
	General.Cluster.DialTimeout = 5s
	General.Cluster.RPCTimeout = 7s
	General.Cluster.ReplicationBufferSize = 20971520
	General.Cluster.ReplicationPullTimeout = 5s
	General.Cluster.ReplicationRetryTimeout = 5s
	General.Cluster.ReplicationBackgroundRefreshInterval = 5m0s
	General.Cluster.ReplicationMaxRetries = 12
	General.Cluster.SendBufferSize = 10
	General.Cluster.CertExpirationWarningThreshold = 168h0m0s
	General.Cluster.TLSHandshakeTimeShift = 0s
	General.Keepalive.ServerMinInterval = 1m0s
	General.Keepalive.ServerInterval = 2h0m0s
	General.Keepalive.ServerTimeout = 20s
	General.ConnectionTimeout = 0s
	General.GenesisMethod = "file"
	General.GenesisProfile = "SampleInsecureSolo"
	General.SystemChannel = "test-system-channel-name"
	General.GenesisFile = "/var/hyperledger/orderer/orderer.genesis.block"
	General.Profile.Enabled = false
	General.Profile.Address = "0.0.0.0:6060"
	General.LocalMSPDir = "/var/hyperledger/orderer/msp"
	General.LocalMSPID = "OrdererMSP"
	General.BCCSP.ProviderName = "SW"
	General.BCCSP.SwOpts.SecLevel = 256
	General.BCCSP.SwOpts.HashFamily = "SHA2"
	General.BCCSP.SwOpts.Ephemeral = false
	General.BCCSP.SwOpts.FileKeystore.KeyStorePath = "/var/hyperledger/orderer/msp/keystore"
	General.BCCSP.SwOpts.DummyKeystore =
	General.BCCSP.SwOpts.InmemKeystore =
	General.BCCSP.PluginOpts =
	General.Authentication.TimeWindow = 15m0s
	General.Authentication.NoExpirationChecks = false
	FileLedger.Location = "/var/hyperledger/production/orderer"
	FileLedger.Prefix = "hyperledger-fabric-ordererledger"
	RAMLedger.HistorySize = 1000
	Kafka.Retry.ShortInterval = 1s
	Kafka.Retry.ShortTotal = 30s
	Kafka.Retry.LongInterval = 5m0s
	Kafka.Retry.LongTotal = 12h0m0s
	Kafka.Retry.NetworkTimeouts.DialTimeout = 10s
	Kafka.Retry.NetworkTimeouts.ReadTimeout = 10s
	Kafka.Retry.NetworkTimeouts.WriteTimeout = 10s
	Kafka.Retry.Metadata.RetryMax = 3
	Kafka.Retry.Metadata.RetryBackoff = 250ms
	Kafka.Retry.Producer.RetryMax = 3
	Kafka.Retry.Producer.RetryBackoff = 100ms
	Kafka.Retry.Consumer.RetryBackoff = 2s
	Kafka.Verbose = true
	Kafka.Version = 0.10.2.0
	Kafka.TLS.Enabled = false
	Kafka.TLS.PrivateKey = ""
	Kafka.TLS.Certificate = ""
	Kafka.TLS.RootCAs = []
	Kafka.TLS.ClientAuthRequired = false
	Kafka.TLS.ClientRootCAs = []
	Kafka.SASLPlain.Enabled = false
	Kafka.SASLPlain.User = ""
	Kafka.SASLPlain.Password = ""
	Kafka.Topic.ReplicationFactor = 3
	Debug.BroadcastTraceDir = ""
	Debug.DeliverTraceDir = ""
	Consensus = map[WALDir:/var/hyperledger/production/orderer/etcdraft/wal SnapDir:/var/hyperledger/production/orderer/etcdraft/snapshot]
	Operations.ListenAddress = "127.0.0.1:8443"
	Operations.TLS.Enabled = false
	Operations.TLS.PrivateKey = ""
	Operations.TLS.Certificate = ""
	Operations.TLS.RootCAs = []
	Operations.TLS.ClientAuthRequired = false
	Operations.TLS.ClientRootCAs = []
	Metrics.Provider = "disabled"
	Metrics.Statsd.Network = "udp"
	Metrics.Statsd.Address = "127.0.0.1:8125"
	Metrics.Statsd.WriteInterval = 30s
	Metrics.Statsd.Prefix = ""
2019-10-22 17:11:34.968 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 17:11:34.997 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 17:11:34.998 UTC [fsblkstorage] newBlockfileMgr -> INFO 005 Getting block information from block storage
2019-10-22 17:11:35.049 UTC [orderer.consensus.kafka] newChain -> INFO 006 [channel: byfn-sys-channel] Starting chain with last persisted offset -3 and last recorded block [0]
2019-10-22 17:11:35.051 UTC [orderer.commmon.multichannel] Initialize -> INFO 007 Starting system channel 'byfn-sys-channel' with genesis block hash c321ff1c6c2f91debd02ea90af3c5fd5d8aed3dbb1fa74a9a20a14c73c68f7ea and orderer type kafka
2019-10-22 17:11:35.052 UTC [orderer.common.server] Start -> INFO 008 Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 17:11:35.052 UTC [orderer.common.server] Start -> INFO 009 Beginning to serve requests
2019-10-22 17:11:35.052 UTC [orderer.consensus.kafka] setupTopicForChannel -> INFO 00a [channel: byfn-sys-channel] Setting up the topic for this channel...
2019-10-22 17:11:45.746 UTC [orderer.consensus.kafka] setupProducerForChannel -> INFO 00b [channel: byfn-sys-channel] Setting up the producer for this channel...
2019-10-22 17:11:45.757 UTC [orderer.consensus.kafka] startThread -> INFO 00c [channel: byfn-sys-channel] Producer set up successfully
2019-10-22 17:11:45.757 UTC [orderer.consensus.kafka] sendConnectMessage -> INFO 00d [channel: byfn-sys-channel] About to post the CONNECT message...
2019-10-22 17:11:47.865 UTC [orderer.consensus.kafka] startThread -> INFO 00e [channel: byfn-sys-channel] CONNECT message posted successfully
2019-10-22 17:11:47.865 UTC [orderer.consensus.kafka] setupParentConsumerForChannel -> INFO 00f [channel: byfn-sys-channel] Setting up the parent consumer for this channel...
2019-10-22 17:11:47.889 UTC [orderer.consensus.kafka] startThread -> INFO 010 [channel: byfn-sys-channel] Parent consumer set up successfully
2019-10-22 17:11:47.889 UTC [orderer.consensus.kafka] setupChannelConsumerForChannel -> INFO 011 [channel: byfn-sys-channel] Setting up the channel consumer for this channel (start offset: -2)...
2019-10-22 17:11:47.898 UTC [orderer.consensus.kafka] startThread -> INFO 012 [channel: byfn-sys-channel] Channel consumer set up successfully
2019-10-22 17:11:47.922 UTC [orderer.consensus.kafka] startThread -> INFO 013 [channel: byfn-sys-channel] Start phase completed successfully
```

> Zookeeper 0

```
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
2019-10-22 16:35:32,539 [myid:] - INFO  [main:QuorumPeerConfig@124] - Reading configuration from: /conf/zoo.cfg
2019-10-22 16:35:32,760 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:32,769 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:32,779 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper0.example.com to address: zookeeper0.example.com/172.19.0.2
2019-10-22 16:35:32,784 [myid:] - INFO  [main:QuorumPeerConfig@352] - Defaulting to majority quorums
2019-10-22 16:35:32,809 [myid:1] - INFO  [main:DatadirCleanupManager@78] - autopurge.snapRetainCount set to 3
2019-10-22 16:35:32,809 [myid:1] - INFO  [main:DatadirCleanupManager@79] - autopurge.purgeInterval set to 1
2019-10-22 16:35:32,842 [myid:1] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@138] - Purge task started.
2019-10-22 16:35:32,979 [myid:1] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@144] - Purge task completed.
2019-10-22 16:35:33,060 [myid:1] - INFO  [main:QuorumPeerMain@127] - Starting quorum peer
2019-10-22 16:35:33,179 [myid:1] - INFO  [main:NIOServerCnxnFactory@89] - binding to port 0.0.0.0/0.0.0.0:2181
2019-10-22 16:35:33,199 [myid:1] - INFO  [main:QuorumPeer@1019] - tickTime set to 2000
2019-10-22 16:35:33,209 [myid:1] - INFO  [main:QuorumPeer@1039] - minSessionTimeout set to -1
2019-10-22 16:35:33,209 [myid:1] - INFO  [main:QuorumPeer@1050] - maxSessionTimeout set to -1
2019-10-22 16:35:33,211 [myid:1] - INFO  [main:QuorumPeer@1065] - initLimit set to 5
2019-10-22 16:35:33,328 [myid:1] - INFO  [main:QuorumPeer@533] - currentEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:33,357 [myid:1] - INFO  [main:QuorumPeer@548] - acceptedEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:33,405 [myid:1] - INFO  [ListenerThread:QuorumCnxManager$Listener@534] - My election bind port: zookeeper0.example.com/172.19.0.2:3888
2019-10-22 16:35:33,515 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer@774] - LOOKING
2019-10-22 16:35:33,517 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:FastLeaderElection@818] - New election. My id =  1, proposed zxid=0x0
2019-10-22 16:35:33,530 [myid:1] - INFO  [WorkerReceiver[myid=1]:FastLeaderElection@600] - Notification: 1 (message format version), 1 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 1 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:33,556 [myid:1] - WARN  [WorkerSender[myid=1]:QuorumCnxManager@400] - Cannot open channel to 2 at election address zookeeper1.example.com/172.19.0.4:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.toSend(QuorumCnxManager.java:354)
	at org.apache.zookeeper.server.quorum.FastLeaderElection$Messenger$WorkerSender.process(FastLeaderElection.java:452)
	at org.apache.zookeeper.server.quorum.FastLeaderElection$Messenger$WorkerSender.run(FastLeaderElection.java:433)
	at java.lang.Thread.run(Thread.java:748)
2019-10-22 16:35:33,575 [myid:1] - INFO  [WorkerSender[myid=1]:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:33,584 [myid:1] - WARN  [WorkerSender[myid=1]:QuorumCnxManager@400] - Cannot open channel to 3 at election address zookeeper2.example.com/172.19.0.7:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.toSend(QuorumCnxManager.java:354)
	at org.apache.zookeeper.server.quorum.FastLeaderElection$Messenger$WorkerSender.process(FastLeaderElection.java:452)
	at org.apache.zookeeper.server.quorum.FastLeaderElection$Messenger$WorkerSender.run(FastLeaderElection.java:433)
	at java.lang.Thread.run(Thread.java:748)
2019-10-22 16:35:33,597 [myid:1] - INFO  [WorkerSender[myid=1]:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:33,774 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 2 at election address zookeeper1.example.com/172.19.0.4:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:33,775 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:33,776 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 3 at election address zookeeper2.example.com/172.19.0.7:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:33,790 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:33,791 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:FastLeaderElection@852] - Notification time out: 400
2019-10-22 16:35:34,196 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 2 at election address zookeeper1.example.com/172.19.0.4:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:34,196 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:34,196 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 3 at election address zookeeper2.example.com/172.19.0.7:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:34,196 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:34,197 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:FastLeaderElection@852] - Notification time out: 800
2019-10-22 16:35:35,001 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 2 at election address zookeeper1.example.com/172.19.0.4:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:35,002 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:35,003 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumCnxManager@400] - Cannot open channel to 3 at election address zookeeper2.example.com/172.19.0.7:3888
java.net.ConnectException: Connection refused (Connection refused)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectOne(QuorumCnxManager.java:381)
	at org.apache.zookeeper.server.quorum.QuorumCnxManager.connectAll(QuorumCnxManager.java:426)
	at org.apache.zookeeper.server.quorum.FastLeaderElection.lookForLeader(FastLeaderElection.java:843)
	at org.apache.zookeeper.server.quorum.QuorumPeer.run(QuorumPeer.java:822)
2019-10-22 16:35:35,004 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:35,005 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:FastLeaderElection@852] - Notification time out: 1600
2019-10-22 16:35:35,720 [myid:1] - INFO  [zookeeper0.example.com/172.19.0.2:3888:QuorumCnxManager$Listener@541] - Received connection request /172.19.0.7:50688
2019-10-22 16:35:35,769 [myid:1] - INFO  [WorkerReceiver[myid=1]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 3 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,770 [myid:1] - INFO  [WorkerSender[myid=1]:QuorumCnxManager@199] - Have smaller server identifier, so dropping the connection: (2, 1)
2019-10-22 16:35:35,770 [myid:1] - INFO  [WorkerReceiver[myid=1]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 1 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,820 [myid:1] - INFO  [zookeeper0.example.com/172.19.0.2:3888:QuorumCnxManager$Listener@541] - Received connection request /172.19.0.4:57446
2019-10-22 16:35:35,856 [myid:1] - INFO  [WorkerReceiver[myid=1]:FastLeaderElection@600] - Notification: 1 (message format version), 2 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,865 [myid:1] - INFO  [WorkerReceiver[myid=1]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:36,066 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer@844] - FOLLOWING
2019-10-22 16:35:36,086 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Learner@86] - TCP NoDelay set to: true
2019-10-22 16:35:36,120 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:zookeeper.version=3.4.9-1757313, built on 08/23/2016 06:50 GMT
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:host.name=42c54c6407d5
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.version=1.8.0_191
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.vendor=Oracle Corporation
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.class.path=/zookeeper-3.4.9/bin/../build/classes:/zookeeper-3.4.9/bin/../build/lib/*.jar:/zookeeper-3.4.9/bin/../lib/slf4j-log4j12-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/slf4j-api-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/netty-3.10.5.Final.jar:/zookeeper-3.4.9/bin/../lib/log4j-1.2.16.jar:/zookeeper-3.4.9/bin/../lib/jline-0.9.94.jar:/zookeeper-3.4.9/bin/../zookeeper-3.4.9.jar:/zookeeper-3.4.9/bin/../src/java/lib/*.jar:/conf:
2019-10-22 16:35:36,151 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
2019-10-22 16:35:36,181 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.io.tmpdir=/tmp
2019-10-22 16:35:36,186 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:java.compiler=<NA>
2019-10-22 16:35:36,186 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:os.name=Linux
2019-10-22 16:35:36,186 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:os.arch=amd64
2019-10-22 16:35:36,186 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:os.version=4.4.0-159-generic
2019-10-22 16:35:36,202 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:user.name=zookeeper
2019-10-22 16:35:36,208 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:user.home=/home/zookeeper
2019-10-22 16:35:36,214 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Environment@100] - Server environment:user.dir=/zookeeper-3.4.9
2019-10-22 16:35:36,291 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:ZooKeeperServer@173] - Created server with tickTime 2000 minSessionTimeout 4000 maxSessionTimeout 40000 datadir /datalog/version-2 snapdir /data/version-2
2019-10-22 16:35:36,306 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Follower@61] - FOLLOWING - LEADER ELECTION TOOK - 2789
2019-10-22 16:35:36,413 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:36,587 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:Learner@326] - Getting a diff from the leader 0x0
2019-10-22 16:35:36,598 [myid:1] - INFO  [QuorumPeer[myid=1]/0.0.0.0:2181:FileTxnSnapLog@240] - Snapshotting: 0x0 to /data/version-2/snapshot.0
2019-10-22 16:35:42,091 [myid:1] - WARN  [QuorumPeer[myid=1]/0.0.0.0:2181:Follower@116] - Got zxid 0x100000001 expected 0x1
2019-10-22 16:35:42,092 [myid:1] - INFO  [SyncThread:1:FileTxnLog@203] - Creating new log file: log.100000001
2019-10-22 16:35:42,461 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /172.19.0.12:47396
2019-10-22 16:35:42,493 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:ZooKeeperServer@928] - Client attempting to establish new session at /172.19.0.12:47396
2019-10-22 16:35:42,527 [myid:1] - INFO  [CommitProcessor:1:ZooKeeperServer@673] - Established session 0x16df452e6140000 with negotiated timeout 6000 for client /172.19.0.12:47396
```

> Zookeeper 1

```
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
2019-10-22 16:35:34,948 [myid:] - INFO  [main:QuorumPeerConfig@124] - Reading configuration from: /conf/zoo.cfg
2019-10-22 16:35:35,167 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:35,177 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:35,183 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper0.example.com to address: zookeeper0.example.com/172.19.0.2
2019-10-22 16:35:35,186 [myid:] - INFO  [main:QuorumPeerConfig@352] - Defaulting to majority quorums
2019-10-22 16:35:35,219 [myid:2] - INFO  [main:DatadirCleanupManager@78] - autopurge.snapRetainCount set to 3
2019-10-22 16:35:35,222 [myid:2] - INFO  [main:DatadirCleanupManager@79] - autopurge.purgeInterval set to 1
2019-10-22 16:35:35,235 [myid:2] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@138] - Purge task started.
2019-10-22 16:35:35,361 [myid:2] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@144] - Purge task completed.
2019-10-22 16:35:35,392 [myid:2] - INFO  [main:QuorumPeerMain@127] - Starting quorum peer
2019-10-22 16:35:35,491 [myid:2] - INFO  [main:NIOServerCnxnFactory@89] - binding to port 0.0.0.0/0.0.0.0:2181
2019-10-22 16:35:35,509 [myid:2] - INFO  [main:QuorumPeer@1019] - tickTime set to 2000
2019-10-22 16:35:35,527 [myid:2] - INFO  [main:QuorumPeer@1039] - minSessionTimeout set to -1
2019-10-22 16:35:35,528 [myid:2] - INFO  [main:QuorumPeer@1050] - maxSessionTimeout set to -1
2019-10-22 16:35:35,528 [myid:2] - INFO  [main:QuorumPeer@1065] - initLimit set to 5
2019-10-22 16:35:35,621 [myid:2] - INFO  [main:QuorumPeer@533] - currentEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:35,653 [myid:2] - INFO  [main:QuorumPeer@548] - acceptedEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:35,701 [myid:2] - INFO  [ListenerThread:QuorumCnxManager$Listener@534] - My election bind port: zookeeper1.example.com/172.19.0.4:3888
2019-10-22 16:35:35,766 [myid:2] - INFO  [zookeeper1.example.com/172.19.0.4:3888:QuorumCnxManager$Listener@541] - Received connection request /172.19.0.7:35356
2019-10-22 16:35:35,816 [myid:2] - INFO  [zookeeper1.example.com/172.19.0.4:3888:QuorumCnxManager$Listener@541] - Received connection request /172.19.0.2:46282
2019-10-22 16:35:35,827 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:QuorumPeer@774] - LOOKING
2019-10-22 16:35:35,830 [myid:2] - INFO  [WorkerReceiver[myid=2]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 3 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,833 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:FastLeaderElection@818] - New election. My id =  2, proposed zxid=0x0
2019-10-22 16:35:35,849 [myid:2] - INFO  [WorkerReceiver[myid=2]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 1 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,856 [myid:2] - INFO  [WorkerReceiver[myid=2]:FastLeaderElection@600] - Notification: 1 (message format version), 2 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,866 [myid:2] - INFO  [WorkerReceiver[myid=2]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:36,071 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:QuorumPeer@844] - FOLLOWING
2019-10-22 16:35:36,075 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Learner@86] - TCP NoDelay set to: true
2019-10-22 16:35:36,134 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:zookeeper.version=3.4.9-1757313, built on 08/23/2016 06:50 GMT
2019-10-22 16:35:36,147 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:host.name=878b55ad2ff1
2019-10-22 16:35:36,150 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.version=1.8.0_191
2019-10-22 16:35:36,150 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.vendor=Oracle Corporation
2019-10-22 16:35:36,150 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre
2019-10-22 16:35:36,170 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.class.path=/zookeeper-3.4.9/bin/../build/classes:/zookeeper-3.4.9/bin/../build/lib/*.jar:/zookeeper-3.4.9/bin/../lib/slf4j-log4j12-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/slf4j-api-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/netty-3.10.5.Final.jar:/zookeeper-3.4.9/bin/../lib/log4j-1.2.16.jar:/zookeeper-3.4.9/bin/../lib/jline-0.9.94.jar:/zookeeper-3.4.9/bin/../zookeeper-3.4.9.jar:/zookeeper-3.4.9/bin/../src/java/lib/*.jar:/conf:
2019-10-22 16:35:36,176 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
2019-10-22 16:35:36,176 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.io.tmpdir=/tmp
2019-10-22 16:35:36,176 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:java.compiler=<NA>
2019-10-22 16:35:36,204 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:os.name=Linux
2019-10-22 16:35:36,211 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:os.arch=amd64
2019-10-22 16:35:36,218 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:os.version=4.4.0-159-generic
2019-10-22 16:35:36,223 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:user.name=zookeeper
2019-10-22 16:35:36,241 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:user.home=/home/zookeeper
2019-10-22 16:35:36,246 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Environment@100] - Server environment:user.dir=/zookeeper-3.4.9
2019-10-22 16:35:36,309 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:ZooKeeperServer@173] - Created server with tickTime 2000 minSessionTimeout 4000 maxSessionTimeout 40000 datadir /datalog/version-2 snapdir /data/version-2
2019-10-22 16:35:36,330 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Follower@61] - FOLLOWING - LEADER ELECTION TOOK - 497
2019-10-22 16:35:36,407 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:36,552 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:Learner@326] - Getting a diff from the leader 0x0
2019-10-22 16:35:36,650 [myid:2] - INFO  [QuorumPeer[myid=2]/0.0.0.0:2181:FileTxnSnapLog@240] - Snapshotting: 0x0 to /data/version-2/snapshot.0
2019-10-22 16:35:42,034 [myid:2] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /172.19.0.9:55406
2019-10-22 16:35:42,086 [myid:2] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:ZooKeeperServer@928] - Client attempting to establish new session at /172.19.0.9:55406
2019-10-22 16:35:42,101 [myid:2] - WARN  [QuorumPeer[myid=2]/0.0.0.0:2181:Follower@116] - Got zxid 0x100000001 expected 0x1
2019-10-22 16:35:42,108 [myid:2] - INFO  [SyncThread:2:FileTxnLog@203] - Creating new log file: log.100000001
2019-10-22 16:35:42,156 [myid:2] - INFO  [CommitProcessor:2:ZooKeeperServer@673] - Established session 0x26df452e64a0000 with negotiated timeout 6000 for client /172.19.0.9:55406
2019-10-22 16:35:42,416 [myid:2] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /172.19.0.11:51398
2019-10-22 16:35:42,437 [myid:2] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:ZooKeeperServer@928] - Client attempting to establish new session at /172.19.0.11:51398
2019-10-22 16:35:42,443 [myid:2] - INFO  [CommitProcessor:2:ZooKeeperServer@673] - Established session 0x26df452e64a0001 with negotiated timeout 6000 for client /172.19.0.11:51398
```

> Zookeeper 2

```
ZooKeeper JMX enabled by default
Using config: /conf/zoo.cfg
2019-10-22 16:35:34,720 [myid:] - INFO  [main:QuorumPeerConfig@124] - Reading configuration from: /conf/zoo.cfg
2019-10-22 16:35:35,018 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper2.example.com to address: zookeeper2.example.com/172.19.0.7
2019-10-22 16:35:35,029 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper1.example.com to address: zookeeper1.example.com/172.19.0.4
2019-10-22 16:35:35,038 [myid:] - INFO  [main:QuorumPeer$QuorumServer@149] - Resolved hostname: zookeeper0.example.com to address: zookeeper0.example.com/172.19.0.2
2019-10-22 16:35:35,046 [myid:] - INFO  [main:QuorumPeerConfig@352] - Defaulting to majority quorums
2019-10-22 16:35:35,065 [myid:3] - INFO  [main:DatadirCleanupManager@78] - autopurge.snapRetainCount set to 3
2019-10-22 16:35:35,078 [myid:3] - INFO  [main:DatadirCleanupManager@79] - autopurge.purgeInterval set to 1
2019-10-22 16:35:35,083 [myid:3] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@138] - Purge task started.
2019-10-22 16:35:35,215 [myid:3] - INFO  [PurgeTask:DatadirCleanupManager$PurgeTask@144] - Purge task completed.
2019-10-22 16:35:35,267 [myid:3] - INFO  [main:QuorumPeerMain@127] - Starting quorum peer
2019-10-22 16:35:35,381 [myid:3] - INFO  [main:NIOServerCnxnFactory@89] - binding to port 0.0.0.0/0.0.0.0:2181
2019-10-22 16:35:35,404 [myid:3] - INFO  [main:QuorumPeer@1019] - tickTime set to 2000
2019-10-22 16:35:35,419 [myid:3] - INFO  [main:QuorumPeer@1039] - minSessionTimeout set to -1
2019-10-22 16:35:35,424 [myid:3] - INFO  [main:QuorumPeer@1050] - maxSessionTimeout set to -1
2019-10-22 16:35:35,425 [myid:3] - INFO  [main:QuorumPeer@1065] - initLimit set to 5
2019-10-22 16:35:35,507 [myid:3] - INFO  [main:QuorumPeer@533] - currentEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:35,543 [myid:3] - INFO  [main:QuorumPeer@548] - acceptedEpoch not found! Creating with a reasonable default of 0. This should only happen when you are upgrading your installation
2019-10-22 16:35:35,595 [myid:3] - INFO  [ListenerThread:QuorumCnxManager$Listener@534] - My election bind port: zookeeper2.example.com/172.19.0.7:3888
2019-10-22 16:35:35,692 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:QuorumPeer@774] - LOOKING
2019-10-22 16:35:35,702 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:FastLeaderElection@818] - New election. My id =  3, proposed zxid=0x0
2019-10-22 16:35:35,786 [myid:3] - INFO  [WorkerReceiver[myid=3]:FastLeaderElection@600] - Notification: 1 (message format version), 1 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 1 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,787 [myid:3] - INFO  [WorkerReceiver[myid=3]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 1 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,799 [myid:3] - INFO  [WorkerReceiver[myid=3]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 3 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,857 [myid:3] - INFO  [WorkerReceiver[myid=3]:FastLeaderElection@600] - Notification: 1 (message format version), 2 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:35,868 [myid:3] - INFO  [WorkerReceiver[myid=3]:FastLeaderElection@600] - Notification: 1 (message format version), 3 (n.leader), 0x0 (n.zxid), 0x1 (n.round), LOOKING (n.state), 2 (n.sid), 0x0 (n.peerEpoch) LOOKING (my state)
2019-10-22 16:35:36,072 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:QuorumPeer@856] - LEADING
2019-10-22 16:35:36,077 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Leader@59] - TCP NoDelay set to: true
2019-10-22 16:35:36,140 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:zookeeper.version=3.4.9-1757313, built on 08/23/2016 06:50 GMT
2019-10-22 16:35:36,140 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:host.name=dde0266a73ae
2019-10-22 16:35:36,146 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.version=1.8.0_191
2019-10-22 16:35:36,146 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.vendor=Oracle Corporation
2019-10-22 16:35:36,146 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre
2019-10-22 16:35:36,158 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.class.path=/zookeeper-3.4.9/bin/../build/classes:/zookeeper-3.4.9/bin/../build/lib/*.jar:/zookeeper-3.4.9/bin/../lib/slf4j-log4j12-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/slf4j-api-1.6.1.jar:/zookeeper-3.4.9/bin/../lib/netty-3.10.5.Final.jar:/zookeeper-3.4.9/bin/../lib/log4j-1.2.16.jar:/zookeeper-3.4.9/bin/../lib/jline-0.9.94.jar:/zookeeper-3.4.9/bin/../zookeeper-3.4.9.jar:/zookeeper-3.4.9/bin/../src/java/lib/*.jar:/conf:
2019-10-22 16:35:36,159 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
2019-10-22 16:35:36,159 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.io.tmpdir=/tmp
2019-10-22 16:35:36,159 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:java.compiler=<NA>
2019-10-22 16:35:36,175 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:os.name=Linux
2019-10-22 16:35:36,193 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:os.arch=amd64
2019-10-22 16:35:36,193 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:os.version=4.4.0-159-generic
2019-10-22 16:35:36,193 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:user.name=zookeeper
2019-10-22 16:35:36,193 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:user.home=/home/zookeeper
2019-10-22 16:35:36,213 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Environment@100] - Server environment:user.dir=/zookeeper-3.4.9
2019-10-22 16:35:36,292 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:ZooKeeperServer@173] - Created server with tickTime 2000 minSessionTimeout 4000 maxSessionTimeout 40000 datadir /datalog/version-2 snapdir /data/version-2
2019-10-22 16:35:36,325 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Leader@361] - LEADING - LEADER ELECTION TOOK - 623
2019-10-22 16:35:36,530 [myid:3] - INFO  [LearnerHandler-/172.19.0.4:43820:LearnerHandler@329] - Follower sid: 2 : info : org.apache.zookeeper.server.quorum.QuorumPeer$QuorumServer@32e2d8dd
2019-10-22 16:35:36,531 [myid:3] - INFO  [LearnerHandler-/172.19.0.2:52562:LearnerHandler@329] - Follower sid: 1 : info : org.apache.zookeeper.server.quorum.QuorumPeer$QuorumServer@691cdfcf
2019-10-22 16:35:36,551 [myid:3] - INFO  [LearnerHandler-/172.19.0.4:43820:LearnerHandler@384] - Synchronizing with Follower sid: 2 maxCommittedLog=0x0 minCommittedLog=0x0 peerLastZxid=0x0
2019-10-22 16:35:36,551 [myid:3] - INFO  [LearnerHandler-/172.19.0.4:43820:LearnerHandler@393] - leader and follower are in sync, zxid=0x0
2019-10-22 16:35:36,551 [myid:3] - INFO  [LearnerHandler-/172.19.0.4:43820:LearnerHandler@458] - Sending DIFF
2019-10-22 16:35:36,586 [myid:3] - INFO  [LearnerHandler-/172.19.0.2:52562:LearnerHandler@384] - Synchronizing with Follower sid: 1 maxCommittedLog=0x0 minCommittedLog=0x0 peerLastZxid=0x0
2019-10-22 16:35:36,586 [myid:3] - INFO  [LearnerHandler-/172.19.0.2:52562:LearnerHandler@393] - leader and follower are in sync, zxid=0x0
2019-10-22 16:35:36,586 [myid:3] - INFO  [LearnerHandler-/172.19.0.2:52562:LearnerHandler@458] - Sending DIFF
2019-10-22 16:35:36,640 [myid:3] - INFO  [LearnerHandler-/172.19.0.2:52562:LearnerHandler@518] - Received NEWLEADER-ACK message from 1
2019-10-22 16:35:36,640 [myid:3] - INFO  [QuorumPeer[myid=3]/0.0.0.0:2181:Leader@952] - Have quorum of supporters, sids: [ 1,3 ]; starting up and setting last processed zxid: 0x100000000
2019-10-22 16:35:36,706 [myid:3] - INFO  [LearnerHandler-/172.19.0.4:43820:LearnerHandler@518] - Received NEWLEADER-ACK message from 2
2019-10-22 16:35:42,094 [myid:3] - INFO  [SyncThread:3:FileTxnLog@203] - Creating new log file: log.100000001
2019-10-22 16:35:42,394 [myid:3] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /172.19.0.10:60660
2019-10-22 16:35:42,411 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x5 zxid:0x100000003 txntype:-1 reqpath:n/a Error Path:/brokers Error:KeeperErrorCode = NoNode for /brokers
2019-10-22 16:35:42,435 [myid:3] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:ZooKeeperServer@928] - Client attempting to establish new session at /172.19.0.10:60660
2019-10-22 16:35:42,510 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0xb zxid:0x100000009 txntype:-1 reqpath:n/a Error Path:/config Error:KeeperErrorCode = NoNode for /config
2019-10-22 16:35:42,511 [myid:3] - INFO  [CommitProcessor:3:ZooKeeperServer@673] - Established session 0x36df452e6420000 with negotiated timeout 6000 for client /172.19.0.10:60660
2019-10-22 16:35:42,579 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x13 zxid:0x10000000f txntype:-1 reqpath:n/a Error Path:/admin Error:KeeperErrorCode = NoNode for /admin
2019-10-22 16:35:42,679 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0001 type:create cxid:0xa zxid:0x100000016 txntype:-1 reqpath:n/a Error Path:/brokers/seqid Error:KeeperErrorCode = NodeExists for /brokers/seqid
2019-10-22 16:35:43,275 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x1f zxid:0x100000017 txntype:-1 reqpath:n/a Error Path:/cluster Error:KeeperErrorCode = NoNode for /cluster
2019-10-22 16:35:43,371 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0001 type:create cxid:0xf zxid:0x10000001a txntype:-1 reqpath:n/a Error Path:/cluster/id Error:KeeperErrorCode = NodeExists for /cluster/id
2019-10-22 16:35:43,398 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x16df452e6140000 type:create cxid:0xe zxid:0x10000001b txntype:-1 reqpath:n/a Error Path:/cluster/id Error:KeeperErrorCode = NodeExists for /cluster/id
2019-10-22 16:35:43,427 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x36df452e6420000 type:create cxid:0xe zxid:0x10000001c txntype:-1 reqpath:n/a Error Path:/cluster/id Error:KeeperErrorCode = NodeExists for /cluster/id
2019-10-22 16:35:47,144 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:setData cxid:0x29 zxid:0x10000001e txntype:-1 reqpath:n/a Error Path:/controller_epoch Error:KeeperErrorCode = NoNode for /controller_epoch
2019-10-22 16:35:47,548 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:setData cxid:0x3d zxid:0x100000021 txntype:-1 reqpath:n/a Error Path:/latest_producer_id_block Error:KeeperErrorCode = BadVersion for /latest_producer_id_block
2019-10-22 16:35:47,629 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:setData cxid:0x40 zxid:0x100000023 txntype:-1 reqpath:n/a Error Path:/latest_producer_id_block Error:KeeperErrorCode = BadVersion for /latest_producer_id_block
2019-10-22 16:35:47,693 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0001 type:setData cxid:0x16 zxid:0x100000025 txntype:-1 reqpath:n/a Error Path:/latest_producer_id_block Error:KeeperErrorCode = BadVersion for /latest_producer_id_block
2019-10-22 16:35:47,979 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x36df452e6420000 type:create cxid:0x20 zxid:0x100000027 txntype:-1 reqpath:n/a Error Path:/brokers Error:KeeperErrorCode = NodeExists for /brokers
2019-10-22 16:35:47,996 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x36df452e6420000 type:create cxid:0x21 zxid:0x100000028 txntype:-1 reqpath:n/a Error Path:/brokers/ids Error:KeeperErrorCode = NodeExists for /brokers/ids
2019-10-22 16:35:48,129 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:delete cxid:0x49 zxid:0x10000002a txntype:-1 reqpath:n/a Error Path:/admin/preferred_replica_election Error:KeeperErrorCode = NoNode for /admin/preferred_replica_election
2019-10-22 16:35:48,156 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0001 type:create cxid:0x24 zxid:0x10000002b txntype:-1 reqpath:n/a Error Path:/brokers Error:KeeperErrorCode = NodeExists for /brokers
2019-10-22 16:35:48,168 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0001 type:create cxid:0x25 zxid:0x10000002c txntype:-1 reqpath:n/a Error Path:/brokers/ids Error:KeeperErrorCode = NodeExists for /brokers/ids
2019-10-22 16:35:48,237 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x16df452e6140000 type:create cxid:0x22 zxid:0x10000002e txntype:-1 reqpath:n/a Error Path:/brokers Error:KeeperErrorCode = NodeExists for /brokers
2019-10-22 16:35:48,249 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x16df452e6140000 type:create cxid:0x23 zxid:0x10000002f txntype:-1 reqpath:n/a Error Path:/brokers/ids Error:KeeperErrorCode = NodeExists for /brokers/ids
2019-10-22 16:35:48,427 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x5a zxid:0x100000031 txntype:-1 reqpath:n/a Error Path:/brokers Error:KeeperErrorCode = NodeExists for /brokers
2019-10-22 16:35:48,432 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x5b zxid:0x100000032 txntype:-1 reqpath:n/a Error Path:/brokers/ids Error:KeeperErrorCode = NodeExists for /brokers/ids
2019-10-22 16:35:48,850 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:setData cxid:0x74 zxid:0x100000034 txntype:-1 reqpath:n/a Error Path:/config/topics/byfn-sys-channel Error:KeeperErrorCode = NoNode for /config/topics/byfn-sys-channel
2019-10-22 16:35:48,854 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x75 zxid:0x100000035 txntype:-1 reqpath:n/a Error Path:/config/topics Error:KeeperErrorCode = NodeExists for /config/topics
2019-10-22 16:35:48,969 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x7f zxid:0x100000038 txntype:-1 reqpath:n/a Error Path:/brokers/topics/byfn-sys-channel/partitions/0 Error:KeeperErrorCode = NoNode for /brokers/topics/byfn-sys-channel/partitions/0
2019-10-22 16:35:48,973 [myid:3] - INFO  [ProcessThread(sid:3 cport:-1)::PrepRequestProcessor@649] - Got user-level KeeperException when processing sessionid:0x26df452e64a0000 type:create cxid:0x80 zxid:0x100000039 txntype:-1 reqpath:n/a Error Path:/brokers/topics/byfn-sys-channel/partitions Error:KeeperErrorCode = NoNode for /brokers/topics/byfn-sys-channel/partitions
```

> Kafka 0

```
[2019-10-22 16:35:41,786] INFO KafkaConfig values:
	advertised.host.name = null
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 0
	broker.id.generation.enable = true
	broker.rack = null
	compression.type = producer
	connections.max.idle.ms = 600000
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 3
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 300000
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 1.0-IV0
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
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /tmp/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.format.version = 1.0-IV0
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = -1
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	message.max.bytes = 103809024
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 2
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 1440
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
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
	replica.fetch.max.bytes = 103809024
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
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.mechanism.inter.broker.protocol = GSSAPI
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = null
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = null
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
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
	zookeeper.connect = zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-22 16:35:42,166] INFO starting (kafka.server.KafkaServer)
[2019-10-22 16:35:42,187] INFO Connecting to zookeeper on zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 (kafka.server.KafkaServer)
[2019-10-22 16:35:42,279] INFO Starting ZkClient event thread. (org.I0Itec.zkclient.ZkEventThread)
[2019-10-22 16:35:42,319] INFO Client environment:zookeeper.version=3.4.10-39d3a4f269333c922ed3db283be479f9deacaa0f, built on 03/23/2017 10:13 GMT (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,320] INFO Client environment:host.name=b11af475160f (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,322] INFO Client environment:java.version=1.8.0_191 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,333] INFO Client environment:java.vendor=Oracle Corporation (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,334] INFO Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,334] INFO Client environment:java.class.path=:/opt/kafka/bin/../libs/aopalliance-repackaged-2.5.0-b32.jar:/opt/kafka/bin/../libs/argparse4j-0.7.0.jar:/opt/kafka/bin/../libs/commons-lang3-3.5.jar:/opt/kafka/bin/../libs/connect-api-1.0.0.jar:/opt/kafka/bin/../libs/connect-file-1.0.0.jar:/opt/kafka/bin/../libs/connect-json-1.0.0.jar:/opt/kafka/bin/../libs/connect-runtime-1.0.0.jar:/opt/kafka/bin/../libs/connect-transforms-1.0.0.jar:/opt/kafka/bin/../libs/guava-20.0.jar:/opt/kafka/bin/../libs/hk2-api-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-locator-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-utils-2.5.0-b32.jar:/opt/kafka/bin/../libs/jackson-annotations-2.9.1.jar:/opt/kafka/bin/../libs/jackson-core-2.9.1.jar:/opt/kafka/bin/../libs/jackson-databind-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-base-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-json-provider-2.9.1.jar:/opt/kafka/bin/../libs/jackson-module-jaxb-annotations-2.9.1.jar:/opt/kafka/bin/../libs/javassist-3.20.0-GA.jar:/opt/kafka/bin/../libs/javassist-3.21.0-GA.jar:/opt/kafka/bin/../libs/javax.annotation-api-1.2.jar:/opt/kafka/bin/../libs/javax.inject-1.jar:/opt/kafka/bin/../libs/javax.inject-2.5.0-b32.jar:/opt/kafka/bin/../libs/javax.servlet-api-3.1.0.jar:/opt/kafka/bin/../libs/javax.ws.rs-api-2.0.1.jar:/opt/kafka/bin/../libs/jersey-client-2.25.1.jar:/opt/kafka/bin/../libs/jersey-common-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-core-2.25.1.jar:/opt/kafka/bin/../libs/jersey-guava-2.25.1.jar:/opt/kafka/bin/../libs/jersey-media-jaxb-2.25.1.jar:/opt/kafka/bin/../libs/jersey-server-2.25.1.jar:/opt/kafka/bin/../libs/jetty-continuation-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-http-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-io-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-security-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-server-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlet-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlets-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-util-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jopt-simple-5.0.4.jar:/opt/kafka/bin/../libs/kafka-clients-1.0.0.jar:/opt/kafka/bin/../libs/kafka-log4j-appender-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-examples-1.0.0.jar:/opt/kafka/bin/../libs/kafka-tools-1.0.0.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-test-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0.jar:/opt/kafka/bin/../libs/log4j-1.2.17.jar:/opt/kafka/bin/../libs/lz4-java-1.4.jar:/opt/kafka/bin/../libs/maven-artifact-3.5.0.jar:/opt/kafka/bin/../libs/metrics-core-2.2.0.jar:/opt/kafka/bin/../libs/osgi-resource-locator-1.0.1.jar:/opt/kafka/bin/../libs/plexus-utils-3.0.24.jar:/opt/kafka/bin/../libs/reflections-0.9.11.jar:/opt/kafka/bin/../libs/rocksdbjni-5.7.3.jar:/opt/kafka/bin/../libs/scala-library-2.11.11.jar:/opt/kafka/bin/../libs/slf4j-api-1.7.25.jar:/opt/kafka/bin/../libs/slf4j-log4j12-1.7.25.jar:/opt/kafka/bin/../libs/snappy-java-1.1.4.jar:/opt/kafka/bin/../libs/validation-api-1.1.0.Final.jar:/opt/kafka/bin/../libs/zkclient-0.10.jar:/opt/kafka/bin/../libs/zookeeper-3.4.10.jar (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,336] INFO Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,339] INFO Client environment:java.io.tmpdir=/tmp (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,342] INFO Client environment:java.compiler=<NA> (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,343] INFO Client environment:os.name=Linux (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,344] INFO Client environment:os.arch=amd64 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,344] INFO Client environment:os.version=4.4.0-159-generic (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,345] INFO Client environment:user.name=root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,346] INFO Client environment:user.home=/root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,347] INFO Client environment:user.dir=/ (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,349] INFO Initiating client connection, connectString=zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 sessionTimeout=6000 watcher=org.I0Itec.zkclient.ZkClient@4466af20 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,431] INFO Waiting for keeper state SyncConnected (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:42,434] INFO Opening socket connection to server zookeeper0.example.com.fabric_byfn/172.19.0.2:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,473] INFO Socket connection established to zookeeper0.example.com.fabric_byfn/172.19.0.2:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,523] INFO Session establishment complete on server zookeeper0.example.com.fabric_byfn/172.19.0.2:2181, sessionid = 0x16df452e6140000, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,526] INFO zookeeper state changed (SyncConnected) (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:43,535] INFO Cluster ID = AwGmZUosRGmzhXBR9qt35A (kafka.server.KafkaServer)
[2019-10-22 16:35:43,558] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:43,832] INFO [ThrottledRequestReaper-Fetch]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,840] INFO [ThrottledRequestReaper-Produce]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,842] INFO [ThrottledRequestReaper-Request]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:44,058] INFO Log directory '/tmp/kafka-logs' not found, creating it. (kafka.log.LogManager)
[2019-10-22 16:35:44,122] INFO Loading logs. (kafka.log.LogManager)
[2019-10-22 16:35:44,191] INFO Logs loading complete in 43 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,764] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,767] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2019-10-22 16:35:46,736] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2019-10-22 16:35:46,837] INFO [SocketServer brokerId=0] Started 1 acceptor threads (kafka.network.SocketServer)
[2019-10-22 16:35:46,972] INFO [ExpirationReaper-0-Produce]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,981] INFO [ExpirationReaper-0-Fetch]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,000] INFO [ExpirationReaper-0-DeleteRecords]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,087] INFO [LogDirFailureHandler]: Starting (kafka.server.ReplicaManager$LogDirFailureHandler)
[2019-10-22 16:35:47,419] INFO [ExpirationReaper-0-topic]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,489] INFO [ExpirationReaper-0-Heartbeat]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,490] INFO [ExpirationReaper-0-Rebalance]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,555] INFO [GroupCoordinator 0]: Starting up. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,568] INFO [GroupCoordinator 0]: Startup complete. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,588] INFO [GroupMetadataManager brokerId=0] Removed 0 expired offsets in 14 milliseconds. (kafka.coordinator.group.GroupMetadataManager)
[2019-10-22 16:35:47,638] INFO [ProducerId Manager 0]: Acquired new producerId block (brokerId:0,blockStartProducerId:1000,blockEndProducerId:1999) by writing to Zk with path version 2 (kafka.coordinator.transaction.ProducerIdManager)
[2019-10-22 16:35:47,744] INFO [TransactionCoordinator id=0] Starting up. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,777] INFO [TransactionCoordinator id=0] Startup complete. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,821] INFO [Transaction Marker Channel Manager 0]: Starting (kafka.coordinator.transaction.TransactionMarkerChannelManager)
[2019-10-22 16:35:48,214] INFO Creating /brokers/ids/0 (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,264] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,268] INFO Registered broker 0 at path /brokers/ids/0 with addresses: EndPoint(b11af475160f,9092,ListenerName(PLAINTEXT),PLAINTEXT) (kafka.utils.ZkUtils)
[2019-10-22 16:35:48,276] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:48,335] INFO Kafka version : 1.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,341] INFO Kafka commitId : aaa7af6d4a11b29d (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,355] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
[2019-10-22 16:35:49,068] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,224] INFO Loading producer state from offset 0 for partition byfn-sys-channel-0 with message format version 2 (kafka.log.Log)
[2019-10-22 16:35:49,264] INFO Completed load of log byfn-sys-channel-0 with 1 log segments, log start offset 0 and log end offset 0 in 109 ms (kafka.log.Log)
[2019-10-22 16:35:49,285] INFO Created log for partition [byfn-sys-channel,0] in /tmp/kafka-logs with properties {compression.type -> producer, message.format.version -> 1.0-IV0, file.delete.delay.ms -> 60000, max.message.bytes -> 103809024, min.compaction.lag.ms -> 0, message.timestamp.type -> CreateTime, min.insync.replicas -> 2, segment.jitter.ms -> 0, preallocate -> false, min.cleanable.dirty.ratio -> 0.5, index.interval.bytes -> 4096, unclean.leader.election.enable -> false, retention.bytes -> -1, delete.retention.ms -> 86400000, cleanup.policy -> [delete], flush.ms -> 9223372036854775807, segment.ms -> 604800000, segment.bytes -> 1073741824, retention.ms -> -1, message.timestamp.difference.max.ms -> 9223372036854775807, segment.index.bytes -> 10485760, flush.messages -> 9223372036854775807}. (kafka.log.LogManager)
[2019-10-22 16:35:49,296] INFO [Partition byfn-sys-channel-0 broker=0] No checkpointed highwatermark is found for partition byfn-sys-channel-0 (kafka.cluster.Partition)
[2019-10-22 16:35:49,299] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,303] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,324] INFO [ReplicaFetcherManager on broker 0] Removed fetcher for partitions byfn-sys-channel-0 (kafka.server.ReplicaFetcherManager)
[2019-10-22 16:35:49,497] INFO [ReplicaFetcher replicaId=0, leaderId=2, fetcherId=0] Starting (kafka.server.ReplicaFetcherThread)
[2019-10-22 16:35:49,528] INFO [ReplicaFetcherManager on broker 0] Added fetcher for partitions List([byfn-sys-channel-0, initOffset 0 to broker BrokerEndPoint(2,cdc5d93847ab,9092)] ) (kafka.server.ReplicaFetcherManager)
[2019-10-22 16:35:50,584] WARN [ReplicaFetcher replicaId=0, leaderId=2, fetcherId=0] Based on follower's leader epoch, leader replied with an unknown offset in byfn-sys-channel-0. High watermark 0 will be used for truncation. (kafka.server.ReplicaFetcherThread)
[2019-10-22 16:35:50,588] INFO Truncating byfn-sys-channel-0 to 0 has no effect as the largest offset in the log is -1. (kafka.log.Log)
[2019-10-22 16:35:50,612] INFO Updated PartitionLeaderEpoch. New: {epoch:0, offset:0}, Current: {epoch:-1, offset-1} for Partition: byfn-sys-channel-0. Cache now contains 0 entries. (kafka.server.epoch.LeaderEpochFileCache)
```

> Kafka 1

```
[2019-10-22 16:35:41,672] INFO KafkaConfig values:
	advertised.host.name = null
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 1
	broker.id.generation.enable = true
	broker.rack = null
	compression.type = producer
	connections.max.idle.ms = 600000
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 3
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 300000
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 1.0-IV0
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
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /tmp/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.format.version = 1.0-IV0
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = -1
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	message.max.bytes = 103809024
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 2
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 1440
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
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
	replica.fetch.max.bytes = 103809024
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
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.mechanism.inter.broker.protocol = GSSAPI
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = null
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = null
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
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
	zookeeper.connect = zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-22 16:35:42,067] INFO starting (kafka.server.KafkaServer)
[2019-10-22 16:35:42,085] INFO Connecting to zookeeper on zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 (kafka.server.KafkaServer)
[2019-10-22 16:35:42,200] INFO Starting ZkClient event thread. (org.I0Itec.zkclient.ZkEventThread)
[2019-10-22 16:35:42,227] INFO Client environment:zookeeper.version=3.4.10-39d3a4f269333c922ed3db283be479f9deacaa0f, built on 03/23/2017 10:13 GMT (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,234] INFO Client environment:host.name=b111540fac69 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,235] INFO Client environment:java.version=1.8.0_191 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,236] INFO Client environment:java.vendor=Oracle Corporation (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,237] INFO Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,237] INFO Client environment:java.class.path=:/opt/kafka/bin/../libs/aopalliance-repackaged-2.5.0-b32.jar:/opt/kafka/bin/../libs/argparse4j-0.7.0.jar:/opt/kafka/bin/../libs/commons-lang3-3.5.jar:/opt/kafka/bin/../libs/connect-api-1.0.0.jar:/opt/kafka/bin/../libs/connect-file-1.0.0.jar:/opt/kafka/bin/../libs/connect-json-1.0.0.jar:/opt/kafka/bin/../libs/connect-runtime-1.0.0.jar:/opt/kafka/bin/../libs/connect-transforms-1.0.0.jar:/opt/kafka/bin/../libs/guava-20.0.jar:/opt/kafka/bin/../libs/hk2-api-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-locator-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-utils-2.5.0-b32.jar:/opt/kafka/bin/../libs/jackson-annotations-2.9.1.jar:/opt/kafka/bin/../libs/jackson-core-2.9.1.jar:/opt/kafka/bin/../libs/jackson-databind-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-base-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-json-provider-2.9.1.jar:/opt/kafka/bin/../libs/jackson-module-jaxb-annotations-2.9.1.jar:/opt/kafka/bin/../libs/javassist-3.20.0-GA.jar:/opt/kafka/bin/../libs/javassist-3.21.0-GA.jar:/opt/kafka/bin/../libs/javax.annotation-api-1.2.jar:/opt/kafka/bin/../libs/javax.inject-1.jar:/opt/kafka/bin/../libs/javax.inject-2.5.0-b32.jar:/opt/kafka/bin/../libs/javax.servlet-api-3.1.0.jar:/opt/kafka/bin/../libs/javax.ws.rs-api-2.0.1.jar:/opt/kafka/bin/../libs/jersey-client-2.25.1.jar:/opt/kafka/bin/../libs/jersey-common-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-core-2.25.1.jar:/opt/kafka/bin/../libs/jersey-guava-2.25.1.jar:/opt/kafka/bin/../libs/jersey-media-jaxb-2.25.1.jar:/opt/kafka/bin/../libs/jersey-server-2.25.1.jar:/opt/kafka/bin/../libs/jetty-continuation-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-http-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-io-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-security-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-server-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlet-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlets-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-util-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jopt-simple-5.0.4.jar:/opt/kafka/bin/../libs/kafka-clients-1.0.0.jar:/opt/kafka/bin/../libs/kafka-log4j-appender-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-examples-1.0.0.jar:/opt/kafka/bin/../libs/kafka-tools-1.0.0.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-test-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0.jar:/opt/kafka/bin/../libs/log4j-1.2.17.jar:/opt/kafka/bin/../libs/lz4-java-1.4.jar:/opt/kafka/bin/../libs/maven-artifact-3.5.0.jar:/opt/kafka/bin/../libs/metrics-core-2.2.0.jar:/opt/kafka/bin/../libs/osgi-resource-locator-1.0.1.jar:/opt/kafka/bin/../libs/plexus-utils-3.0.24.jar:/opt/kafka/bin/../libs/reflections-0.9.11.jar:/opt/kafka/bin/../libs/rocksdbjni-5.7.3.jar:/opt/kafka/bin/../libs/scala-library-2.11.11.jar:/opt/kafka/bin/../libs/slf4j-api-1.7.25.jar:/opt/kafka/bin/../libs/slf4j-log4j12-1.7.25.jar:/opt/kafka/bin/../libs/snappy-java-1.1.4.jar:/opt/kafka/bin/../libs/validation-api-1.1.0.Final.jar:/opt/kafka/bin/../libs/zkclient-0.10.jar:/opt/kafka/bin/../libs/zookeeper-3.4.10.jar (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,238] INFO Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,238] INFO Client environment:java.io.tmpdir=/tmp (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,239] INFO Client environment:java.compiler=<NA> (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,244] INFO Client environment:os.name=Linux (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,246] INFO Client environment:os.arch=amd64 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,246] INFO Client environment:os.version=4.4.0-159-generic (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,247] INFO Client environment:user.name=root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,247] INFO Client environment:user.home=/root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,248] INFO Client environment:user.dir=/ (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,249] INFO Initiating client connection, connectString=zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 sessionTimeout=6000 watcher=org.I0Itec.zkclient.ZkClient@4466af20 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,350] INFO Waiting for keeper state SyncConnected (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:42,354] INFO Opening socket connection to server zookeeper2.example.com.fabric_byfn/172.19.0.7:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,391] INFO Socket connection established to zookeeper2.example.com.fabric_byfn/172.19.0.7:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,501] INFO Session establishment complete on server zookeeper2.example.com.fabric_byfn/172.19.0.7:2181, sessionid = 0x36df452e6420000, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,504] INFO zookeeper state changed (SyncConnected) (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:43,538] INFO Cluster ID = AwGmZUosRGmzhXBR9qt35A (kafka.server.KafkaServer)
[2019-10-22 16:35:43,563] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:43,809] INFO [ThrottledRequestReaper-Fetch]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,812] INFO [ThrottledRequestReaper-Produce]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,852] INFO [ThrottledRequestReaper-Request]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:44,011] INFO Log directory '/tmp/kafka-logs' not found, creating it. (kafka.log.LogManager)
[2019-10-22 16:35:44,055] INFO Loading logs. (kafka.log.LogManager)
[2019-10-22 16:35:44,144] INFO Logs loading complete in 45 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,701] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,729] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2019-10-22 16:35:46,722] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2019-10-22 16:35:46,768] INFO [SocketServer brokerId=1] Started 1 acceptor threads (kafka.network.SocketServer)
[2019-10-22 16:35:46,968] INFO [ExpirationReaper-1-Produce]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,979] INFO [ExpirationReaper-1-Fetch]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,988] INFO [ExpirationReaper-1-DeleteRecords]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,075] INFO [LogDirFailureHandler]: Starting (kafka.server.ReplicaManager$LogDirFailureHandler)
[2019-10-22 16:35:47,322] INFO [ExpirationReaper-1-topic]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,402] INFO [ExpirationReaper-1-Heartbeat]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,417] INFO [ExpirationReaper-1-Rebalance]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,458] INFO [GroupCoordinator 1]: Starting up. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,475] INFO [GroupCoordinator 1]: Startup complete. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,491] INFO [GroupMetadataManager brokerId=1] Removed 0 expired offsets in 9 milliseconds. (kafka.coordinator.group.GroupMetadataManager)
[2019-10-22 16:35:47,535] INFO [ProducerId Manager 1]: Acquired new producerId block (brokerId:1,blockStartProducerId:0,blockEndProducerId:999) by writing to Zk with path version 1 (kafka.coordinator.transaction.ProducerIdManager)
[2019-10-22 16:35:47,650] INFO [TransactionCoordinator id=1] Starting up. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,652] INFO [TransactionCoordinator id=1] Startup complete. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,660] INFO [Transaction Marker Channel Manager 1]: Starting (kafka.coordinator.transaction.TransactionMarkerChannelManager)
[2019-10-22 16:35:47,960] INFO Creating /brokers/ids/1 (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,019] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,030] INFO Registered broker 1 at path /brokers/ids/1 with addresses: EndPoint(b111540fac69,9092,ListenerName(PLAINTEXT),PLAINTEXT) (kafka.utils.ZkUtils)
[2019-10-22 16:35:48,039] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:48,085] INFO Kafka version : 1.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,089] INFO Kafka commitId : aaa7af6d4a11b29d (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,123] INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
[2019-10-22 16:35:49,080] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,083] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,251] INFO Loading producer state from offset 0 for partition byfn-sys-channel-0 with message format version 2 (kafka.log.Log)
[2019-10-22 16:35:49,288] INFO Completed load of log byfn-sys-channel-0 with 1 log segments, log start offset 0 and log end offset 0 in 111 ms (kafka.log.Log)
[2019-10-22 16:35:49,314] INFO Created log for partition [byfn-sys-channel,0] in /tmp/kafka-logs with properties {compression.type -> producer, message.format.version -> 1.0-IV0, file.delete.delay.ms -> 60000, max.message.bytes -> 103809024, min.compaction.lag.ms -> 0, message.timestamp.type -> CreateTime, min.insync.replicas -> 2, segment.jitter.ms -> 0, preallocate -> false, min.cleanable.dirty.ratio -> 0.5, index.interval.bytes -> 4096, unclean.leader.election.enable -> false, retention.bytes -> -1, delete.retention.ms -> 86400000, cleanup.policy -> [delete], flush.ms -> 9223372036854775807, segment.ms -> 604800000, segment.bytes -> 1073741824, retention.ms -> -1, message.timestamp.difference.max.ms -> 9223372036854775807, segment.index.bytes -> 10485760, flush.messages -> 9223372036854775807}. (kafka.log.LogManager)
[2019-10-22 16:35:49,320] INFO [Partition byfn-sys-channel-0 broker=1] No checkpointed highwatermark is found for partition byfn-sys-channel-0 (kafka.cluster.Partition)
[2019-10-22 16:35:49,323] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,345] INFO [ReplicaFetcherManager on broker 1] Removed fetcher for partitions byfn-sys-channel-0 (kafka.server.ReplicaFetcherManager)
[2019-10-22 16:35:49,488] INFO [ReplicaFetcher replicaId=1, leaderId=2, fetcherId=0] Starting (kafka.server.ReplicaFetcherThread)
[2019-10-22 16:35:49,539] INFO [ReplicaFetcherManager on broker 1] Added fetcher for partitions List([byfn-sys-channel-0, initOffset 0 to broker BrokerEndPoint(2,cdc5d93847ab,9092)] ) (kafka.server.ReplicaFetcherManager)
[2019-10-22 16:35:49,686] WARN [ReplicaFetcher replicaId=1, leaderId=2, fetcherId=0] Based on follower's leader epoch, leader replied with an unknown offset in byfn-sys-channel-0. High watermark 0 will be used for truncation. (kafka.server.ReplicaFetcherThread)
[2019-10-22 16:35:49,700] INFO Truncating byfn-sys-channel-0 to 0 has no effect as the largest offset in the log is -1. (kafka.log.Log)
[2019-10-22 16:35:49,761] INFO Updated PartitionLeaderEpoch. New: {epoch:0, offset:0}, Current: {epoch:-1, offset-1} for Partition: byfn-sys-channel-0. Cache now contains 0 entries. (kafka.server.epoch.LeaderEpochFileCache)
```

> Kafka 2

```
[2019-10-22 16:35:41,726] INFO KafkaConfig values:
	advertised.host.name = null
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 2
	broker.id.generation.enable = true
	broker.rack = null
	compression.type = producer
	connections.max.idle.ms = 600000
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 3
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 300000
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 1.0-IV0
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
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /tmp/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.format.version = 1.0-IV0
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = -1
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	message.max.bytes = 103809024
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 2
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 1440
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
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
	replica.fetch.max.bytes = 103809024
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
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.mechanism.inter.broker.protocol = GSSAPI
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = null
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = null
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
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
	zookeeper.connect = zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-22 16:35:42,118] INFO starting (kafka.server.KafkaServer)
[2019-10-22 16:35:42,134] INFO Connecting to zookeeper on zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 (kafka.server.KafkaServer)
[2019-10-22 16:35:42,228] INFO Starting ZkClient event thread. (org.I0Itec.zkclient.ZkEventThread)
[2019-10-22 16:35:42,265] INFO Client environment:zookeeper.version=3.4.10-39d3a4f269333c922ed3db283be479f9deacaa0f, built on 03/23/2017 10:13 GMT (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,274] INFO Client environment:host.name=cdc5d93847ab (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,275] INFO Client environment:java.version=1.8.0_191 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,276] INFO Client environment:java.vendor=Oracle Corporation (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,277] INFO Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,278] INFO Client environment:java.class.path=:/opt/kafka/bin/../libs/aopalliance-repackaged-2.5.0-b32.jar:/opt/kafka/bin/../libs/argparse4j-0.7.0.jar:/opt/kafka/bin/../libs/commons-lang3-3.5.jar:/opt/kafka/bin/../libs/connect-api-1.0.0.jar:/opt/kafka/bin/../libs/connect-file-1.0.0.jar:/opt/kafka/bin/../libs/connect-json-1.0.0.jar:/opt/kafka/bin/../libs/connect-runtime-1.0.0.jar:/opt/kafka/bin/../libs/connect-transforms-1.0.0.jar:/opt/kafka/bin/../libs/guava-20.0.jar:/opt/kafka/bin/../libs/hk2-api-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-locator-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-utils-2.5.0-b32.jar:/opt/kafka/bin/../libs/jackson-annotations-2.9.1.jar:/opt/kafka/bin/../libs/jackson-core-2.9.1.jar:/opt/kafka/bin/../libs/jackson-databind-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-base-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-json-provider-2.9.1.jar:/opt/kafka/bin/../libs/jackson-module-jaxb-annotations-2.9.1.jar:/opt/kafka/bin/../libs/javassist-3.20.0-GA.jar:/opt/kafka/bin/../libs/javassist-3.21.0-GA.jar:/opt/kafka/bin/../libs/javax.annotation-api-1.2.jar:/opt/kafka/bin/../libs/javax.inject-1.jar:/opt/kafka/bin/../libs/javax.inject-2.5.0-b32.jar:/opt/kafka/bin/../libs/javax.servlet-api-3.1.0.jar:/opt/kafka/bin/../libs/javax.ws.rs-api-2.0.1.jar:/opt/kafka/bin/../libs/jersey-client-2.25.1.jar:/opt/kafka/bin/../libs/jersey-common-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-core-2.25.1.jar:/opt/kafka/bin/../libs/jersey-guava-2.25.1.jar:/opt/kafka/bin/../libs/jersey-media-jaxb-2.25.1.jar:/opt/kafka/bin/../libs/jersey-server-2.25.1.jar:/opt/kafka/bin/../libs/jetty-continuation-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-http-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-io-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-security-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-server-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlet-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlets-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-util-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jopt-simple-5.0.4.jar:/opt/kafka/bin/../libs/kafka-clients-1.0.0.jar:/opt/kafka/bin/../libs/kafka-log4j-appender-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-examples-1.0.0.jar:/opt/kafka/bin/../libs/kafka-tools-1.0.0.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-test-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0.jar:/opt/kafka/bin/../libs/log4j-1.2.17.jar:/opt/kafka/bin/../libs/lz4-java-1.4.jar:/opt/kafka/bin/../libs/maven-artifact-3.5.0.jar:/opt/kafka/bin/../libs/metrics-core-2.2.0.jar:/opt/kafka/bin/../libs/osgi-resource-locator-1.0.1.jar:/opt/kafka/bin/../libs/plexus-utils-3.0.24.jar:/opt/kafka/bin/../libs/reflections-0.9.11.jar:/opt/kafka/bin/../libs/rocksdbjni-5.7.3.jar:/opt/kafka/bin/../libs/scala-library-2.11.11.jar:/opt/kafka/bin/../libs/slf4j-api-1.7.25.jar:/opt/kafka/bin/../libs/slf4j-log4j12-1.7.25.jar:/opt/kafka/bin/../libs/snappy-java-1.1.4.jar:/opt/kafka/bin/../libs/validation-api-1.1.0.Final.jar:/opt/kafka/bin/../libs/zkclient-0.10.jar:/opt/kafka/bin/../libs/zookeeper-3.4.10.jar (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,280] INFO Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,283] INFO Client environment:java.io.tmpdir=/tmp (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,284] INFO Client environment:java.compiler=<NA> (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,287] INFO Client environment:os.name=Linux (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,288] INFO Client environment:os.arch=amd64 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,288] INFO Client environment:os.version=4.4.0-159-generic (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,289] INFO Client environment:user.name=root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,289] INFO Client environment:user.home=/root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,291] INFO Client environment:user.dir=/ (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,293] INFO Initiating client connection, connectString=zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 sessionTimeout=6000 watcher=org.I0Itec.zkclient.ZkClient@4466af20 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,388] INFO Waiting for keeper state SyncConnected (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:42,398] INFO Opening socket connection to server zookeeper1.example.com.fabric_byfn/172.19.0.4:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,418] INFO Socket connection established to zookeeper1.example.com.fabric_byfn/172.19.0.4:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,448] INFO Session establishment complete on server zookeeper1.example.com.fabric_byfn/172.19.0.4:2181, sessionid = 0x26df452e64a0001, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,456] INFO zookeeper state changed (SyncConnected) (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:43,536] INFO Cluster ID = AwGmZUosRGmzhXBR9qt35A (kafka.server.KafkaServer)
[2019-10-22 16:35:43,564] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:43,819] INFO [ThrottledRequestReaper-Produce]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,820] INFO [ThrottledRequestReaper-Fetch]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,821] INFO [ThrottledRequestReaper-Request]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:44,011] INFO Log directory '/tmp/kafka-logs' not found, creating it. (kafka.log.LogManager)
[2019-10-22 16:35:44,068] INFO Loading logs. (kafka.log.LogManager)
[2019-10-22 16:35:44,116] INFO Logs loading complete in 41 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,682] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,706] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2019-10-22 16:35:46,792] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2019-10-22 16:35:46,835] INFO [SocketServer brokerId=2] Started 1 acceptor threads (kafka.network.SocketServer)
[2019-10-22 16:35:47,046] INFO [ExpirationReaper-2-Produce]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,069] INFO [ExpirationReaper-2-Fetch]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,070] INFO [ExpirationReaper-2-DeleteRecords]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,216] INFO [LogDirFailureHandler]: Starting (kafka.server.ReplicaManager$LogDirFailureHandler)
[2019-10-22 16:35:47,429] INFO [ExpirationReaper-2-topic]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,529] INFO [ExpirationReaper-2-Heartbeat]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,532] INFO [ExpirationReaper-2-Rebalance]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,585] INFO [GroupCoordinator 2]: Starting up. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,611] INFO [GroupCoordinator 2]: Startup complete. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,635] INFO [GroupMetadataManager brokerId=2] Removed 0 expired offsets in 1 milliseconds. (kafka.coordinator.group.GroupMetadataManager)
[2019-10-22 16:35:47,723] INFO [ProducerId Manager 2]: Acquired new producerId block (brokerId:2,blockStartProducerId:3000,blockEndProducerId:3999) by writing to Zk with path version 4 (kafka.coordinator.transaction.ProducerIdManager)
[2019-10-22 16:35:47,806] INFO [TransactionCoordinator id=2] Starting up. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,813] INFO [TransactionCoordinator id=2] Startup complete. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,836] INFO [Transaction Marker Channel Manager 2]: Starting (kafka.coordinator.transaction.TransactionMarkerChannelManager)
[2019-10-22 16:35:48,150] INFO Creating /brokers/ids/2 (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,184] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,188] INFO Registered broker 2 at path /brokers/ids/2 with addresses: EndPoint(cdc5d93847ab,9092,ListenerName(PLAINTEXT),PLAINTEXT) (kafka.utils.ZkUtils)
[2019-10-22 16:35:48,202] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:48,227] INFO Kafka version : 1.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,228] INFO Kafka commitId : aaa7af6d4a11b29d (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,265] INFO [KafkaServer id=2] started (kafka.server.KafkaServer)
[2019-10-22 16:35:49,047] INFO [ReplicaFetcherManager on broker 2] Removed fetcher for partitions byfn-sys-channel-0 (kafka.server.ReplicaFetcherManager)
[2019-10-22 16:35:49,219] INFO Loading producer state from offset 0 for partition byfn-sys-channel-0 with message format version 2 (kafka.log.Log)
[2019-10-22 16:35:49,301] INFO Completed load of log byfn-sys-channel-0 with 1 log segments, log start offset 0 and log end offset 0 in 155 ms (kafka.log.Log)
[2019-10-22 16:35:49,336] INFO Created log for partition [byfn-sys-channel,0] in /tmp/kafka-logs with properties {compression.type -> producer, message.format.version -> 1.0-IV0, file.delete.delay.ms -> 60000, max.message.bytes -> 103809024, min.compaction.lag.ms -> 0, message.timestamp.type -> CreateTime, min.insync.replicas -> 2, segment.jitter.ms -> 0, preallocate -> false, min.cleanable.dirty.ratio -> 0.5, index.interval.bytes -> 4096, unclean.leader.election.enable -> false, retention.bytes -> -1, delete.retention.ms -> 86400000, cleanup.policy -> [delete], flush.ms -> 9223372036854775807, segment.ms -> 604800000, segment.bytes -> 1073741824, retention.ms -> -1, message.timestamp.difference.max.ms -> 9223372036854775807, segment.index.bytes -> 10485760, flush.messages -> 9223372036854775807}. (kafka.log.LogManager)
[2019-10-22 16:35:49,342] INFO [Partition byfn-sys-channel-0 broker=2] No checkpointed highwatermark is found for partition byfn-sys-channel-0 (kafka.cluster.Partition)
[2019-10-22 16:35:49,357] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,363] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,369] INFO Replica loaded for partition byfn-sys-channel-0 with initial high watermark 0 (kafka.cluster.Replica)
[2019-10-22 16:35:49,388] INFO [Partition byfn-sys-channel-0 broker=2] byfn-sys-channel-0 starts at Leader Epoch 0 from offset 0. Previous Leader Epoch was: -1 (kafka.cluster.Partition)
[2019-10-22 16:35:49,647] INFO Updated PartitionLeaderEpoch. New: {epoch:0, offset:0}, Current: {epoch:-1, offset-1} for Partition: byfn-sys-channel-0. Cache now contains 0 entries. (kafka.server.epoch.LeaderEpochFileCache)
```

> Kafka 3

```
[2019-10-22 16:35:41,349] INFO KafkaConfig values:
	advertised.host.name = null
	advertised.listeners = null
	advertised.port = null
	alter.config.policy.class.name = null
	authorizer.class.name =
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	background.threads = 10
	broker.id = 3
	broker.id.generation.enable = true
	broker.rack = null
	compression.type = producer
	connections.max.idle.ms = 600000
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	create.topic.policy.class.name = null
	default.replication.factor = 3
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	fetch.purgatory.purge.interval.requests = 1000
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 300000
	group.min.session.timeout.ms = 6000
	host.name =
	inter.broker.listener.name = null
	inter.broker.protocol.version = 1.0-IV0
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
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	log.dir = /tmp/kafka-logs
	log.dirs = /tmp/kafka-logs
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	log.index.interval.bytes = 4096
	log.index.size.max.bytes = 10485760
	log.message.format.version = 1.0-IV0
	log.message.timestamp.difference.max.ms = 9223372036854775807
	log.message.timestamp.type = CreateTime
	log.preallocate = false
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = -1
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides =
	message.max.bytes = 103809024
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	min.insync.replicas = 2
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 1
	num.recovery.threads.per.data.dir = 1
	num.replica.fetchers = 1
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 1440
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
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
	replica.fetch.max.bytes = 103809024
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
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.mechanism.inter.broker.protocol = GSSAPI
	security.inter.broker.protocol = PLAINTEXT
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	ssl.cipher.suites = null
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = null
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
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
	zookeeper.connect = zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
 (kafka.server.KafkaConfig)
[2019-10-22 16:35:41,807] INFO starting (kafka.server.KafkaServer)
[2019-10-22 16:35:41,846] INFO Connecting to zookeeper on zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 (kafka.server.KafkaServer)
[2019-10-22 16:35:41,911] INFO Starting ZkClient event thread. (org.I0Itec.zkclient.ZkEventThread)
[2019-10-22 16:35:41,915] INFO Client environment:zookeeper.version=3.4.10-39d3a4f269333c922ed3db283be479f9deacaa0f, built on 03/23/2017 10:13 GMT (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,926] INFO Client environment:host.name=8a22ee0028b2 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,927] INFO Client environment:java.version=1.8.0_191 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,930] INFO Client environment:java.vendor=Oracle Corporation (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,931] INFO Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,935] INFO Client environment:java.class.path=:/opt/kafka/bin/../libs/aopalliance-repackaged-2.5.0-b32.jar:/opt/kafka/bin/../libs/argparse4j-0.7.0.jar:/opt/kafka/bin/../libs/commons-lang3-3.5.jar:/opt/kafka/bin/../libs/connect-api-1.0.0.jar:/opt/kafka/bin/../libs/connect-file-1.0.0.jar:/opt/kafka/bin/../libs/connect-json-1.0.0.jar:/opt/kafka/bin/../libs/connect-runtime-1.0.0.jar:/opt/kafka/bin/../libs/connect-transforms-1.0.0.jar:/opt/kafka/bin/../libs/guava-20.0.jar:/opt/kafka/bin/../libs/hk2-api-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-locator-2.5.0-b32.jar:/opt/kafka/bin/../libs/hk2-utils-2.5.0-b32.jar:/opt/kafka/bin/../libs/jackson-annotations-2.9.1.jar:/opt/kafka/bin/../libs/jackson-core-2.9.1.jar:/opt/kafka/bin/../libs/jackson-databind-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-base-2.9.1.jar:/opt/kafka/bin/../libs/jackson-jaxrs-json-provider-2.9.1.jar:/opt/kafka/bin/../libs/jackson-module-jaxb-annotations-2.9.1.jar:/opt/kafka/bin/../libs/javassist-3.20.0-GA.jar:/opt/kafka/bin/../libs/javassist-3.21.0-GA.jar:/opt/kafka/bin/../libs/javax.annotation-api-1.2.jar:/opt/kafka/bin/../libs/javax.inject-1.jar:/opt/kafka/bin/../libs/javax.inject-2.5.0-b32.jar:/opt/kafka/bin/../libs/javax.servlet-api-3.1.0.jar:/opt/kafka/bin/../libs/javax.ws.rs-api-2.0.1.jar:/opt/kafka/bin/../libs/jersey-client-2.25.1.jar:/opt/kafka/bin/../libs/jersey-common-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-2.25.1.jar:/opt/kafka/bin/../libs/jersey-container-servlet-core-2.25.1.jar:/opt/kafka/bin/../libs/jersey-guava-2.25.1.jar:/opt/kafka/bin/../libs/jersey-media-jaxb-2.25.1.jar:/opt/kafka/bin/../libs/jersey-server-2.25.1.jar:/opt/kafka/bin/../libs/jetty-continuation-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-http-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-io-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-security-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-server-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlet-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-servlets-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jetty-util-9.2.22.v20170606.jar:/opt/kafka/bin/../libs/jopt-simple-5.0.4.jar:/opt/kafka/bin/../libs/kafka-clients-1.0.0.jar:/opt/kafka/bin/../libs/kafka-log4j-appender-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-1.0.0.jar:/opt/kafka/bin/../libs/kafka-streams-examples-1.0.0.jar:/opt/kafka/bin/../libs/kafka-tools-1.0.0.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0-test-sources.jar:/opt/kafka/bin/../libs/kafka_2.11-1.0.0.jar:/opt/kafka/bin/../libs/log4j-1.2.17.jar:/opt/kafka/bin/../libs/lz4-java-1.4.jar:/opt/kafka/bin/../libs/maven-artifact-3.5.0.jar:/opt/kafka/bin/../libs/metrics-core-2.2.0.jar:/opt/kafka/bin/../libs/osgi-resource-locator-1.0.1.jar:/opt/kafka/bin/../libs/plexus-utils-3.0.24.jar:/opt/kafka/bin/../libs/reflections-0.9.11.jar:/opt/kafka/bin/../libs/rocksdbjni-5.7.3.jar:/opt/kafka/bin/../libs/scala-library-2.11.11.jar:/opt/kafka/bin/../libs/slf4j-api-1.7.25.jar:/opt/kafka/bin/../libs/slf4j-log4j12-1.7.25.jar:/opt/kafka/bin/../libs/snappy-java-1.1.4.jar:/opt/kafka/bin/../libs/validation-api-1.1.0.Final.jar:/opt/kafka/bin/../libs/zkclient-0.10.jar:/opt/kafka/bin/../libs/zookeeper-3.4.10.jar (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,936] INFO Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,936] INFO Client environment:java.io.tmpdir=/tmp (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,938] INFO Client environment:java.compiler=<NA> (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,939] INFO Client environment:os.name=Linux (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,943] INFO Client environment:os.arch=amd64 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,944] INFO Client environment:os.version=4.4.0-159-generic (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,944] INFO Client environment:user.name=root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,945] INFO Client environment:user.home=/root (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,945] INFO Client environment:user.dir=/ (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:41,947] INFO Initiating client connection, connectString=zookeeper0.example.com:2181,zookeeper1.example.com:2181,zookeeper2.example.com:2181 sessionTimeout=6000 watcher=org.I0Itec.zkclient.ZkClient@4466af20 (org.apache.zookeeper.ZooKeeper)
[2019-10-22 16:35:42,001] INFO Waiting for keeper state SyncConnected (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:42,012] INFO Opening socket connection to server zookeeper1.example.com.fabric_byfn/172.19.0.4:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,042] INFO Socket connection established to zookeeper1.example.com.fabric_byfn/172.19.0.4:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,140] INFO Session establishment complete on server zookeeper1.example.com.fabric_byfn/172.19.0.4:2181, sessionid = 0x26df452e64a0000, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2019-10-22 16:35:42,142] INFO zookeeper state changed (SyncConnected) (org.I0Itec.zkclient.ZkClient)
[2019-10-22 16:35:43,296] INFO Cluster ID = AwGmZUosRGmzhXBR9qt35A (kafka.server.KafkaServer)
[2019-10-22 16:35:43,338] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:43,486] INFO [ThrottledRequestReaper-Fetch]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,511] INFO [ThrottledRequestReaper-Produce]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,514] INFO [ThrottledRequestReaper-Request]: Starting (kafka.server.ClientQuotaManager$ThrottledRequestReaper)
[2019-10-22 16:35:43,694] INFO Log directory '/tmp/kafka-logs' not found, creating it. (kafka.log.LogManager)
[2019-10-22 16:35:43,724] INFO Loading logs. (kafka.log.LogManager)
[2019-10-22 16:35:43,757] INFO Logs loading complete in 17 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,086] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2019-10-22 16:35:44,097] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2019-10-22 16:35:46,184] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2019-10-22 16:35:46,258] INFO [SocketServer brokerId=3] Started 1 acceptor threads (kafka.network.SocketServer)
[2019-10-22 16:35:46,513] INFO [ExpirationReaper-3-Produce]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,533] INFO [ExpirationReaper-3-DeleteRecords]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,520] INFO [ExpirationReaper-3-Fetch]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:46,740] INFO [LogDirFailureHandler]: Starting (kafka.server.ReplicaManager$LogDirFailureHandler)
[2019-10-22 16:35:46,950] INFO [ExpirationReaper-3-topic]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,008] INFO [ExpirationReaper-3-Heartbeat]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,021] INFO Creating /controller (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:47,034] INFO [ExpirationReaper-3-Rebalance]: Starting (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2019-10-22 16:35:47,089] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:47,356] INFO [GroupCoordinator 3]: Starting up. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,382] INFO [GroupCoordinator 3]: Startup complete. (kafka.coordinator.group.GroupCoordinator)
[2019-10-22 16:35:47,447] INFO [GroupMetadataManager brokerId=3] Removed 0 expired offsets in 59 milliseconds. (kafka.coordinator.group.GroupMetadataManager)
[2019-10-22 16:35:47,672] INFO [ProducerId Manager 3]: Acquired new producerId block (brokerId:3,blockStartProducerId:2000,blockEndProducerId:2999) by writing to Zk with path version 3 (kafka.coordinator.transaction.ProducerIdManager)
[2019-10-22 16:35:47,909] INFO [TransactionCoordinator id=3] Starting up. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:47,973] INFO [TransactionCoordinator id=3] Startup complete. (kafka.coordinator.transaction.TransactionCoordinator)
[2019-10-22 16:35:48,032] INFO [Transaction Marker Channel Manager 3]: Starting (kafka.coordinator.transaction.TransactionMarkerChannelManager)
[2019-10-22 16:35:48,388] INFO Creating /brokers/ids/3 (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,455] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2019-10-22 16:35:48,456] INFO Registered broker 3 at path /brokers/ids/3 with addresses: EndPoint(8a22ee0028b2,9092,ListenerName(PLAINTEXT),PLAINTEXT) (kafka.utils.ZkUtils)
[2019-10-22 16:35:48,499] WARN No meta.properties file under dir /tmp/kafka-logs/meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2019-10-22 16:35:48,629] INFO Kafka version : 1.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,658] INFO Kafka commitId : aaa7af6d4a11b29d (org.apache.kafka.common.utils.AppInfoParser)
[2019-10-22 16:35:48,694] INFO [KafkaServer id=3] started (kafka.server.KafkaServer)
[2019-10-22 16:35:48,883] INFO Topic creation {"version":1,"partitions":{"0":[2,0,1]}} (kafka.admin.AdminUtils$)
[2019-10-22 16:35:48,924] INFO [KafkaApi-3] Auto creation of topic byfn-sys-channel with 1 partitions and replication factor 3 is successful (kafka.server.KafkaApis)
```
