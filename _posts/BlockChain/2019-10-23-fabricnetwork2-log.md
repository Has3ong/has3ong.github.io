---
title : Hyperledger Network 로그
---

> docker-compose -f docker-compose-cli.yaml up

```
peer1.org2.example.com    | 2019-10-22 15:06:14.780 UTC [nodeCmd] serve -> INFO 001 Starting peer:
peer1.org2.example.com    |  Version: 1.4.3
peer1.org2.example.com    |  Commit SHA: b8c4a6a
peer1.org2.example.com    |  Go version: go1.11.5
peer1.org2.example.com    |  OS/Arch: linux/amd64
peer1.org2.example.com    |  Chaincode:
peer1.org2.example.com    |   Base Image Version: 0.4.15
peer1.org2.example.com    |   Base Docker Namespace: hyperledger
peer1.org2.example.com    |   Base Docker Label: org.hyperledger.fabric
peer1.org2.example.com    |   Docker Namespace: hyperledger
peer1.org2.example.com    | 2019-10-22 15:06:14.782 UTC [ledgermgmt] initialize -> INFO 002 Initializing ledger mgmt
peer1.org2.example.com    | 2019-10-22 15:06:14.782 UTC [kvledger] NewProvider -> INFO 003 Initializing ledger provider
peer1.org2.example.com    | 2019-10-22 15:06:14.791 UTC [kvledger] NewProvider -> INFO 004 ledger provider Initialized
peer1.org2.example.com    | 2019-10-22 15:06:14.799 UTC [ledgermgmt] initialize -> INFO 005 ledger mgmt initialized
peer1.org2.example.com    | 2019-10-22 15:06:14.799 UTC [peer] func1 -> INFO 006 Auto-detected peer address: 172.19.0.2:10051
peer1.org2.example.com    | 2019-10-22 15:06:14.799 UTC [peer] func1 -> INFO 007 Returning peer1.org2.example.com:10051
peer1.org2.example.com    | 2019-10-22 15:06:14.799 UTC [peer] func1 -> INFO 008 Auto-detected peer address: 172.19.0.2:10051
peer1.org2.example.com    | 2019-10-22 15:06:14.799 UTC [peer] func1 -> INFO 009 Returning peer1.org2.example.com:10051
peer1.org2.example.com    | 2019-10-22 15:06:14.806 UTC [nodeCmd] serve -> INFO 00a Starting peer with TLS enabled
peer1.org2.example.com    | 2019-10-22 15:06:14.807 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00b Entering computeChaincodeEndpoint with peerHostname: peer1.org2.example.com
peer1.org2.example.com    | 2019-10-22 15:06:14.807 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00c Exit with ccEndpoint: peer1.org2.example.com:10052
peer1.org2.example.com    | 2019-10-22 15:06:14.808 UTC [sccapi] registerSysCC -> INFO 00d system chaincode lscc(github.com/hyperledger/fabric/core/scc/lscc) registered
peer1.org2.example.com    | 2019-10-22 15:06:14.808 UTC [sccapi] registerSysCC -> INFO 00e system chaincode cscc(github.com/hyperledger/fabric/core/scc/cscc) registered
peer1.org2.example.com    | 2019-10-22 15:06:14.808 UTC [sccapi] registerSysCC -> INFO 00f system chaincode qscc(github.com/hyperledger/fabric/core/scc/qscc) registered
peer1.org2.example.com    | 2019-10-22 15:06:14.808 UTC [sccapi] registerSysCC -> INFO 010 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle,true) disabled
peer1.org2.example.com    | 2019-10-22 15:06:14.810 UTC [gossip.service] func1 -> INFO 011 Initialize gossip with endpoint peer1.org2.example.com:10051 and bootstrap set [peer0.org2.example.com:9051]
peer1.org2.example.com    | 2019-10-22 15:06:14.831 UTC [gossip.gossip] NewGossipService -> INFO 012 Creating gossip service with self membership of Endpoint: peer1.org2.example.com:10051, InternalEndpoint: peer1.org2.example.com:10051, PKI-ID: bac0dd3f0d7f2ba0e44f9e9f6170fdfb658b160e8dfab97983ed01a8846b02e1, Metadata:
peer1.org2.example.com    | 2019-10-22 15:06:14.831 UTC [gossip.gossip] start -> INFO 013 Gossip instance peer1.org2.example.com:10051 started
peer1.org2.example.com    | 2019-10-22 15:06:14.836 UTC [sccapi] deploySysCC -> INFO 014 system chaincode lscc/(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer1.org2.example.com    | 2019-10-22 15:06:14.836 UTC [cscc] Init -> INFO 015 Init CSCC
peer1.org2.example.com    | 2019-10-22 15:06:14.837 UTC [sccapi] deploySysCC -> INFO 016 system chaincode cscc/(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer1.org2.example.com    | 2019-10-22 15:06:14.837 UTC [qscc] Init -> INFO 017 Init QSCC
peer1.org2.example.com    | 2019-10-22 15:06:14.837 UTC [sccapi] deploySysCC -> INFO 018 system chaincode qscc/(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer1.org2.example.com    | 2019-10-22 15:06:14.837 UTC [sccapi] deploySysCC -> INFO 019 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer1.org2.example.com    | 2019-10-22 15:06:14.837 UTC [nodeCmd] serve -> INFO 01a Deployed system chaincodes
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [discovery] NewService -> INFO 01b Created with config TLS: true, authCacheMaxSize: 1000, authCachePurgeRatio: 0.750000
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [nodeCmd] registerDiscoveryService -> INFO 01c Discovery service activated
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [nodeCmd] serve -> INFO 01d Starting peer with ID=[name:"peer1.org2.example.com" ], network ID=[dev], address=[peer1.org2.example.com:10051]
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [nodeCmd] serve -> INFO 01e Started peer with ID=[name:"peer1.org2.example.com" ], network ID=[dev], address=[peer1.org2.example.com:10051]
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [kvledger] LoadPreResetHeight -> INFO 01f Loading prereset height from path [/var/hyperledger/production/ledgersData/chains]
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [fsblkstorage] LoadPreResetHeight -> INFO 020 Loading Pre-reset heights
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [fsblkstorage] preRestHtFiles -> INFO 021 Dir [/var/hyperledger/production/ledgersData/chains/chains] missing... exiting
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [fsblkstorage] LoadPreResetHeight -> INFO 022 Pre-reset heights loaded
peer1.org2.example.com    | 2019-10-22 15:06:14.838 UTC [nodeCmd] func7 -> INFO 023 Starting profiling server with listenAddress = 0.0.0.0:6060
peer1.org2.example.com    | 2019-10-22 15:06:15.798 UTC [comm.grpc.server] 1 -> INFO 024 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:17.798Z grpc.peer_address=172.19.0.3:56844 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=40.511µs
peer1.org2.example.com    | 2019-10-22 15:06:15.803 UTC [comm.grpc.server] 1 -> INFO 025 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:06:25.802Z grpc.peer_address=172.19.0.3:56844 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=1.338597ms
peer0.org1.example.com    | 2019-10-22 15:06:15.608 UTC [nodeCmd] serve -> INFO 001 Starting peer:
peer0.org1.example.com    |  Version: 1.4.3
peer0.org1.example.com    |  Commit SHA: b8c4a6a
peer0.org1.example.com    |  Go version: go1.11.5
peer0.org1.example.com    |  OS/Arch: linux/amd64
peer0.org1.example.com    |  Chaincode:
peer0.org1.example.com    |   Base Image Version: 0.4.15
peer0.org1.example.com    |   Base Docker Namespace: hyperledger
peer0.org1.example.com    |   Base Docker Label: org.hyperledger.fabric
peer0.org1.example.com    |   Docker Namespace: hyperledger
peer0.org1.example.com    | 2019-10-22 15:06:15.609 UTC [ledgermgmt] initialize -> INFO 002 Initializing ledger mgmt
peer0.org1.example.com    | 2019-10-22 15:06:15.609 UTC [kvledger] NewProvider -> INFO 003 Initializing ledger provider
peer0.org1.example.com    | 2019-10-22 15:06:15.657 UTC [kvledger] NewProvider -> INFO 004 ledger provider Initialized
peer0.org1.example.com    | 2019-10-22 15:06:15.697 UTC [ledgermgmt] initialize -> INFO 005 ledger mgmt initialized
peer0.org1.example.com    | 2019-10-22 15:06:15.697 UTC [peer] func1 -> INFO 006 Auto-detected peer address: 172.19.0.4:7051
peer0.org1.example.com    | 2019-10-22 15:06:15.697 UTC [peer] func1 -> INFO 007 Returning peer0.org1.example.com:7051
peer0.org1.example.com    | 2019-10-22 15:06:15.697 UTC [peer] func1 -> INFO 008 Auto-detected peer address: 172.19.0.4:7051
peer0.org1.example.com    | 2019-10-22 15:06:15.697 UTC [peer] func1 -> INFO 009 Returning peer0.org1.example.com:7051
peer0.org1.example.com    | 2019-10-22 15:06:15.698 UTC [nodeCmd] serve -> INFO 00a Starting peer with TLS enabled
peer0.org1.example.com    | 2019-10-22 15:06:15.699 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00b Entering computeChaincodeEndpoint with peerHostname: peer0.org1.example.com
peer0.org1.example.com    | 2019-10-22 15:06:15.705 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00c Exit with ccEndpoint: peer0.org1.example.com:7052
peer0.org1.example.com    | 2019-10-22 15:06:15.706 UTC [sccapi] registerSysCC -> INFO 00d system chaincode lscc(github.com/hyperledger/fabric/core/scc/lscc) registered
peer0.org1.example.com    | 2019-10-22 15:06:15.706 UTC [sccapi] registerSysCC -> INFO 00e system chaincode cscc(github.com/hyperledger/fabric/core/scc/cscc) registered
peer0.org1.example.com    | 2019-10-22 15:06:15.707 UTC [sccapi] registerSysCC -> INFO 00f system chaincode qscc(github.com/hyperledger/fabric/core/scc/qscc) registered
peer0.org1.example.com    | 2019-10-22 15:06:15.707 UTC [sccapi] registerSysCC -> INFO 010 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle,true) disabled
peer0.org1.example.com    | 2019-10-22 15:06:15.709 UTC [gossip.service] func1 -> INFO 011 Initialize gossip with endpoint peer0.org1.example.com:7051 and bootstrap set [peer1.org1.example.com:8051]
peer0.org1.example.com    | 2019-10-22 15:06:15.714 UTC [gossip.gossip] NewGossipService -> INFO 012 Creating gossip service with self membership of Endpoint: peer0.org1.example.com:7051, InternalEndpoint: peer0.org1.example.com:7051, PKI-ID: 8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c, Metadata:
peer0.org1.example.com    | 2019-10-22 15:06:15.722 UTC [gossip.gossip] start -> INFO 013 Gossip instance peer0.org1.example.com:7051 started
peer0.org1.example.com    | 2019-10-22 15:06:15.732 UTC [sccapi] deploySysCC -> INFO 014 system chaincode lscc/(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer0.org1.example.com    | 2019-10-22 15:06:15.736 UTC [cscc] Init -> INFO 015 Init CSCC
peer0.org1.example.com    | 2019-10-22 15:06:15.737 UTC [sccapi] deploySysCC -> INFO 016 system chaincode cscc/(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer0.org1.example.com    | 2019-10-22 15:06:15.738 UTC [qscc] Init -> INFO 017 Init QSCC
peer0.org1.example.com    | 2019-10-22 15:06:15.739 UTC [sccapi] deploySysCC -> INFO 018 system chaincode qscc/(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer0.org1.example.com    | 2019-10-22 15:06:15.739 UTC [sccapi] deploySysCC -> INFO 019 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer0.org1.example.com    | 2019-10-22 15:06:15.740 UTC [nodeCmd] serve -> INFO 01a Deployed system chaincodes
peer0.org1.example.com    | 2019-10-22 15:06:15.742 UTC [discovery] NewService -> INFO 01b Created with config TLS: true, authCacheMaxSize: 1000, authCachePurgeRatio: 0.750000
peer0.org1.example.com    | 2019-10-22 15:06:15.744 UTC [nodeCmd] registerDiscoveryService -> INFO 01c Discovery service activated
peer0.org1.example.com    | 2019-10-22 15:06:15.745 UTC [nodeCmd] serve -> INFO 01d Starting peer with ID=[name:"peer0.org1.example.com" ], network ID=[dev], address=[peer0.org1.example.com:7051]
peer0.org1.example.com    | 2019-10-22 15:06:15.748 UTC [nodeCmd] serve -> INFO 01e Started peer with ID=[name:"peer0.org1.example.com" ], network ID=[dev], address=[peer0.org1.example.com:7051]
peer0.org1.example.com    | 2019-10-22 15:06:15.748 UTC [kvledger] LoadPreResetHeight -> INFO 01f Loading prereset height from path [/var/hyperledger/production/ledgersData/chains]
peer0.org1.example.com    | 2019-10-22 15:06:15.748 UTC [fsblkstorage] LoadPreResetHeight -> INFO 020 Loading Pre-reset heights
peer0.org2.example.com    | 2019-10-22 15:06:15.656 UTC [nodeCmd] serve -> INFO 001 Starting peer:
peer0.org2.example.com    |  Version: 1.4.3
peer0.org2.example.com    |  Commit SHA: b8c4a6a
peer0.org2.example.com    |  Go version: go1.11.5
peer0.org2.example.com    |  OS/Arch: linux/amd64
peer0.org2.example.com    |  Chaincode:
peer0.org2.example.com    |   Base Image Version: 0.4.15
peer0.org2.example.com    |   Base Docker Namespace: hyperledger
peer0.org2.example.com    |   Base Docker Label: org.hyperledger.fabric
peer0.org2.example.com    |   Docker Namespace: hyperledger
peer0.org2.example.com    | 2019-10-22 15:06:15.664 UTC [ledgermgmt] initialize -> INFO 002 Initializing ledger mgmt
peer0.org2.example.com    | 2019-10-22 15:06:15.665 UTC [kvledger] NewProvider -> INFO 003 Initializing ledger provider
peer0.org2.example.com    | 2019-10-22 15:06:15.696 UTC [kvledger] NewProvider -> INFO 004 ledger provider Initialized
peer0.org2.example.com    | 2019-10-22 15:06:15.740 UTC [ledgermgmt] initialize -> INFO 005 ledger mgmt initialized
peer0.org2.example.com    | 2019-10-22 15:06:15.740 UTC [peer] func1 -> INFO 006 Auto-detected peer address: 172.19.0.3:9051
peer0.org2.example.com    | 2019-10-22 15:06:15.740 UTC [peer] func1 -> INFO 007 Returning peer0.org2.example.com:9051
peer0.org2.example.com    | 2019-10-22 15:06:15.742 UTC [peer] func1 -> INFO 008 Auto-detected peer address: 172.19.0.3:9051
peer0.org2.example.com    | 2019-10-22 15:06:15.743 UTC [peer] func1 -> INFO 009 Returning peer0.org2.example.com:9051
peer0.org2.example.com    | 2019-10-22 15:06:15.744 UTC [nodeCmd] serve -> INFO 00a Starting peer with TLS enabled
peer0.org1.example.com    | 2019-10-22 15:06:15.748 UTC [fsblkstorage] preRestHtFiles -> INFO 021 Dir [/var/hyperledger/production/ledgersData/chains/chains] missing... exiting
peer0.org2.example.com    | 2019-10-22 15:06:15.750 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00b Entering computeChaincodeEndpoint with peerHostname: peer0.org2.example.com
peer0.org1.example.com    | 2019-10-22 15:06:15.749 UTC [fsblkstorage] LoadPreResetHeight -> INFO 022 Pre-reset heights loaded
peer0.org2.example.com    | 2019-10-22 15:06:15.750 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00c Exit with ccEndpoint: peer0.org2.example.com:9052
peer0.org1.example.com    | 2019-10-22 15:06:15.749 UTC [nodeCmd] func7 -> INFO 023 Starting profiling server with listenAddress = 0.0.0.0:6060
peer0.org2.example.com    | 2019-10-22 15:06:15.752 UTC [sccapi] registerSysCC -> INFO 00d system chaincode lscc(github.com/hyperledger/fabric/core/scc/lscc) registered
peer0.org2.example.com    | 2019-10-22 15:06:15.752 UTC [sccapi] registerSysCC -> INFO 00e system chaincode cscc(github.com/hyperledger/fabric/core/scc/cscc) registered
peer0.org1.example.com    | 2019-10-22 15:06:15.820 UTC [comm.grpc.server] 1 -> INFO 024 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:17.82Z grpc.peer_address=172.19.0.5:50492 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=44.833µs
peer0.org2.example.com    | 2019-10-22 15:06:15.752 UTC [sccapi] registerSysCC -> INFO 00f system chaincode qscc(github.com/hyperledger/fabric/core/scc/qscc) registered
peer0.org1.example.com    | 2019-10-22 15:06:15.824 UTC [comm.grpc.server] 1 -> INFO 025 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:06:25.821Z grpc.peer_address=172.19.0.5:50492 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=2.900207ms
peer0.org1.example.com    | 2019-10-22 15:06:15.826 UTC [comm.grpc.server] 1 -> INFO 026 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:17.826Z grpc.peer_address=172.19.0.5:50494 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=48.076µs
peer0.org2.example.com    | 2019-10-22 15:06:15.753 UTC [sccapi] registerSysCC -> INFO 010 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle,true) disabled
peer0.org2.example.com    | 2019-10-22 15:06:15.762 UTC [gossip.service] func1 -> INFO 011 Initialize gossip with endpoint peer0.org2.example.com:9051 and bootstrap set [peer1.org2.example.com:10051]
peer0.org2.example.com    | 2019-10-22 15:06:15.775 UTC [gossip.gossip] NewGossipService -> INFO 012 Creating gossip service with self membership of Endpoint: peer0.org2.example.com:9051, InternalEndpoint: peer0.org2.example.com:9051, PKI-ID: ddbb1278b2fcbb0e1dce2e516b8d069eb12c49e2ab5925247488e04a8511e7c8, Metadata:
peer0.org2.example.com    | 2019-10-22 15:06:15.779 UTC [gossip.gossip] start -> INFO 013 Gossip instance peer0.org2.example.com:9051 started
peer0.org2.example.com    | 2019-10-22 15:06:15.784 UTC [sccapi] deploySysCC -> INFO 014 system chaincode lscc/(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer0.org2.example.com    | 2019-10-22 15:06:15.785 UTC [cscc] Init -> INFO 015 Init CSCC
peer0.org2.example.com    | 2019-10-22 15:06:15.786 UTC [sccapi] deploySysCC -> INFO 016 system chaincode cscc/(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer0.org2.example.com    | 2019-10-22 15:06:15.787 UTC [qscc] Init -> INFO 017 Init QSCC
peer0.org2.example.com    | 2019-10-22 15:06:15.787 UTC [sccapi] deploySysCC -> INFO 018 system chaincode qscc/(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer0.org2.example.com    | 2019-10-22 15:06:15.787 UTC [sccapi] deploySysCC -> INFO 019 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer0.org2.example.com    | 2019-10-22 15:06:15.787 UTC [nodeCmd] serve -> INFO 01a Deployed system chaincodes
peer0.org2.example.com    | 2019-10-22 15:06:15.788 UTC [discovery] NewService -> INFO 01b Created with config TLS: true, authCacheMaxSize: 1000, authCachePurgeRatio: 0.750000
peer0.org2.example.com    | 2019-10-22 15:06:15.789 UTC [nodeCmd] registerDiscoveryService -> INFO 01c Discovery service activated
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [nodeCmd] serve -> INFO 01d Starting peer with ID=[name:"peer0.org2.example.com" ], network ID=[dev], address=[peer0.org2.example.com:9051]
peer1.org1.example.com    | 2019-10-22 15:06:15.719 UTC [nodeCmd] serve -> INFO 001 Starting peer:
peer1.org1.example.com    |  Version: 1.4.3
peer1.org1.example.com    |  Commit SHA: b8c4a6a
peer1.org1.example.com    |  Go version: go1.11.5
peer1.org1.example.com    |  OS/Arch: linux/amd64
peer1.org1.example.com    |  Chaincode:
peer1.org1.example.com    |   Base Image Version: 0.4.15
peer1.org1.example.com    |   Base Docker Namespace: hyperledger
peer1.org1.example.com    |   Base Docker Label: org.hyperledger.fabric
peer1.org1.example.com    |   Docker Namespace: hyperledger
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [nodeCmd] serve -> INFO 01e Started peer with ID=[name:"peer0.org2.example.com" ], network ID=[dev], address=[peer0.org2.example.com:9051]
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [kvledger] LoadPreResetHeight -> INFO 01f Loading prereset height from path [/var/hyperledger/production/ledgersData/chains]
peer1.org1.example.com    | 2019-10-22 15:06:15.719 UTC [ledgermgmt] initialize -> INFO 002 Initializing ledger mgmt
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [fsblkstorage] LoadPreResetHeight -> INFO 020 Loading Pre-reset heights
peer1.org1.example.com    | 2019-10-22 15:06:15.720 UTC [kvledger] NewProvider -> INFO 003 Initializing ledger provider
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [fsblkstorage] preRestHtFiles -> INFO 021 Dir [/var/hyperledger/production/ledgersData/chains/chains] missing... exiting
peer0.org2.example.com    | 2019-10-22 15:06:15.790 UTC [fsblkstorage] LoadPreResetHeight -> INFO 022 Pre-reset heights loaded
peer1.org1.example.com    | 2019-10-22 15:06:15.752 UTC [kvledger] NewProvider -> INFO 004 ledger provider Initialized
peer1.org1.example.com    | 2019-10-22 15:06:15.780 UTC [ledgermgmt] initialize -> INFO 005 ledger mgmt initialized
peer0.org2.example.com    | 2019-10-22 15:06:15.793 UTC [nodeCmd] func7 -> INFO 023 Starting profiling server with listenAddress = 0.0.0.0:6060
peer0.org2.example.com    | 2019-10-22 15:06:15.793 UTC [comm.grpc.server] 1 -> INFO 024 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:17.793Z grpc.peer_address=172.19.0.2:52978 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=42.556µs
peer1.org1.example.com    | 2019-10-22 15:06:15.780 UTC [peer] func1 -> INFO 006 Auto-detected peer address: 172.19.0.5:8051
peer0.org2.example.com    | 2019-10-22 15:06:15.807 UTC [comm.grpc.server] 1 -> INFO 025 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:17.807Z grpc.peer_address=172.19.0.2:52984 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=42.557µs
peer1.org1.example.com    | 2019-10-22 15:06:15.780 UTC [peer] func1 -> INFO 007 Returning peer1.org1.example.com:8051
peer0.org2.example.com    | 2019-10-22 15:06:15.807 UTC [comm.grpc.server] 1 -> INFO 026 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:06:25.798Z grpc.peer_address=172.19.0.2:52978 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=8.352098ms
peer1.org1.example.com    | 2019-10-22 15:06:15.782 UTC [peer] func1 -> INFO 008 Auto-detected peer address: 172.19.0.5:8051
peer1.org1.example.com    | 2019-10-22 15:06:15.782 UTC [peer] func1 -> INFO 009 Returning peer1.org1.example.com:8051
peer1.org1.example.com    | 2019-10-22 15:06:15.783 UTC [nodeCmd] serve -> INFO 00a Starting peer with TLS enabled
peer1.org1.example.com    | 2019-10-22 15:06:15.786 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00b Entering computeChaincodeEndpoint with peerHostname: peer1.org1.example.com
peer1.org1.example.com    | 2019-10-22 15:06:15.788 UTC [nodeCmd] computeChaincodeEndpoint -> INFO 00c Exit with ccEndpoint: peer1.org1.example.com:8052
peer1.org1.example.com    | 2019-10-22 15:06:15.789 UTC [sccapi] registerSysCC -> INFO 00d system chaincode lscc(github.com/hyperledger/fabric/core/scc/lscc) registered
peer1.org1.example.com    | 2019-10-22 15:06:15.792 UTC [sccapi] registerSysCC -> INFO 00e system chaincode cscc(github.com/hyperledger/fabric/core/scc/cscc) registered
peer1.org1.example.com    | 2019-10-22 15:06:15.792 UTC [sccapi] registerSysCC -> INFO 00f system chaincode qscc(github.com/hyperledger/fabric/core/scc/qscc) registered
peer1.org1.example.com    | 2019-10-22 15:06:15.792 UTC [sccapi] registerSysCC -> INFO 010 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle,true) disabled
peer1.org1.example.com    | 2019-10-22 15:06:15.804 UTC [gossip.service] func1 -> INFO 011 Initialize gossip with endpoint peer1.org1.example.com:8051 and bootstrap set [peer0.org1.example.com:7051]
peer1.org1.example.com    | 2019-10-22 15:06:15.810 UTC [gossip.gossip] NewGossipService -> INFO 012 Creating gossip service with self membership of Endpoint: peer1.org1.example.com:8051, InternalEndpoint: peer1.org1.example.com:8051, PKI-ID: 6416af3fc1a5e20aa872b9210b5d74c1d9b34009b289e072713cf775d26e4bb4, Metadata:
peer1.org1.example.com    | 2019-10-22 15:06:15.814 UTC [gossip.gossip] start -> INFO 013 Gossip instance peer1.org1.example.com:8051 started
peer1.org1.example.com    | 2019-10-22 15:06:15.816 UTC [sccapi] deploySysCC -> INFO 014 system chaincode lscc/(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer1.org1.example.com    | 2019-10-22 15:06:15.816 UTC [cscc] Init -> INFO 015 Init CSCC
peer1.org1.example.com    | 2019-10-22 15:06:15.816 UTC [sccapi] deploySysCC -> INFO 016 system chaincode cscc/(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer1.org1.example.com    | 2019-10-22 15:06:15.817 UTC [qscc] Init -> INFO 017 Init QSCC
peer1.org1.example.com    | 2019-10-22 15:06:15.817 UTC [sccapi] deploySysCC -> INFO 018 system chaincode qscc/(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer1.org1.example.com    | 2019-10-22 15:06:15.817 UTC [sccapi] deploySysCC -> INFO 019 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer1.org1.example.com    | 2019-10-22 15:06:15.817 UTC [nodeCmd] serve -> INFO 01a Deployed system chaincodes
peer1.org1.example.com    | 2019-10-22 15:06:15.817 UTC [discovery] NewService -> INFO 01b Created with config TLS: true, authCacheMaxSize: 1000, authCachePurgeRatio: 0.750000
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [nodeCmd] registerDiscoveryService -> INFO 01c Discovery service activated
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [nodeCmd] serve -> INFO 01d Starting peer with ID=[name:"peer1.org1.example.com" ], network ID=[dev], address=[peer1.org1.example.com:8051]
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [nodeCmd] serve -> INFO 01e Started peer with ID=[name:"peer1.org1.example.com" ], network ID=[dev], address=[peer1.org1.example.com:8051]
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [kvledger] LoadPreResetHeight -> INFO 01f Loading prereset height from path [/var/hyperledger/production/ledgersData/chains]
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [fsblkstorage] LoadPreResetHeight -> INFO 020 Loading Pre-reset heights
orderer.example.com       | 2019-10-22 15:06:16.284 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [fsblkstorage] preRestHtFiles -> INFO 021 Dir [/var/hyperledger/production/ledgersData/chains/chains] missing... exiting
orderer.example.com       | 2019-10-22 15:06:16.299 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
orderer.example.com       | 	General.LedgerType = "file"
orderer.example.com       | 	General.ListenAddress = "0.0.0.0"
orderer.example.com       | 	General.ListenPort = 7050
orderer.example.com       | 	General.TLS.Enabled = true
orderer.example.com       | 	General.TLS.PrivateKey = "/var/hyperledger/orderer/tls/server.key"
orderer.example.com       | 	General.TLS.Certificate = "/var/hyperledger/orderer/tls/server.crt"
orderer.example.com       | 	General.TLS.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
orderer.example.com       | 	General.TLS.ClientAuthRequired = false
orderer.example.com       | 	General.TLS.ClientRootCAs = []
orderer.example.com       | 	General.Cluster.ListenAddress = ""
orderer.example.com       | 	General.Cluster.ListenPort = 0
orderer.example.com       | 	General.Cluster.ServerCertificate = ""
orderer.example.com       | 	General.Cluster.ServerPrivateKey = ""
orderer.example.com       | 	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
orderer.example.com       | 	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
orderer.example.com       | 	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
orderer.example.com       | 	General.Cluster.DialTimeout = 5s
orderer.example.com       | 	General.Cluster.RPCTimeout = 7s
orderer.example.com       | 	General.Cluster.ReplicationBufferSize = 20971520
orderer.example.com       | 	General.Cluster.ReplicationPullTimeout = 5s
orderer.example.com       | 	General.Cluster.ReplicationRetryTimeout = 5s
orderer.example.com       | 	General.Cluster.ReplicationBackgroundRefreshInterval = 5m0s
orderer.example.com       | 	General.Cluster.ReplicationMaxRetries = 12
orderer.example.com       | 	General.Cluster.SendBufferSize = 10
orderer.example.com       | 	General.Cluster.CertExpirationWarningThreshold = 168h0m0s
orderer.example.com       | 	General.Cluster.TLSHandshakeTimeShift = 0s
orderer.example.com       | 	General.Keepalive.ServerMinInterval = 1m0s
orderer.example.com       | 	General.Keepalive.ServerInterval = 2h0m0s
orderer.example.com       | 	General.Keepalive.ServerTimeout = 20s
orderer.example.com       | 	General.ConnectionTimeout = 0s
orderer.example.com       | 	General.GenesisMethod = "file"
orderer.example.com       | 	General.GenesisProfile = "SampleInsecureSolo"
orderer.example.com       | 	General.SystemChannel = "test-system-channel-name"
orderer.example.com       | 	General.GenesisFile = "/var/hyperledger/orderer/orderer.genesis.block"
orderer.example.com       | 	General.Profile.Enabled = false
orderer.example.com       | 	General.Profile.Address = "0.0.0.0:6060"
orderer.example.com       | 	General.LocalMSPDir = "/var/hyperledger/orderer/msp"
orderer.example.com       | 	General.LocalMSPID = "OrdererMSP"
orderer.example.com       | 	General.BCCSP.ProviderName = "SW"
orderer.example.com       | 	General.BCCSP.SwOpts.SecLevel = 256
orderer.example.com       | 	General.BCCSP.SwOpts.HashFamily = "SHA2"
orderer.example.com       | 	General.BCCSP.SwOpts.Ephemeral = false
orderer.example.com       | 	General.BCCSP.SwOpts.FileKeystore.KeyStorePath = "/var/hyperledger/orderer/msp/keystore"
orderer.example.com       | 	General.BCCSP.SwOpts.DummyKeystore =
orderer.example.com       | 	General.BCCSP.SwOpts.InmemKeystore =
orderer.example.com       | 	General.BCCSP.PluginOpts =
orderer.example.com       | 	General.Authentication.TimeWindow = 15m0s
orderer.example.com       | 	General.Authentication.NoExpirationChecks = false
orderer.example.com       | 	FileLedger.Location = "/var/hyperledger/production/orderer"
orderer.example.com       | 	FileLedger.Prefix = "hyperledger-fabric-ordererledger"
orderer.example.com       | 	RAMLedger.HistorySize = 1000
orderer.example.com       | 	Kafka.Retry.ShortInterval = 5s
orderer.example.com       | 	Kafka.Retry.ShortTotal = 10m0s
orderer.example.com       | 	Kafka.Retry.LongInterval = 5m0s
orderer.example.com       | 	Kafka.Retry.LongTotal = 12h0m0s
orderer.example.com       | 	Kafka.Retry.NetworkTimeouts.DialTimeout = 10s
orderer.example.com       | 	Kafka.Retry.NetworkTimeouts.ReadTimeout = 10s
orderer.example.com       | 	Kafka.Retry.NetworkTimeouts.WriteTimeout = 10s
orderer.example.com       | 	Kafka.Retry.Metadata.RetryMax = 3
orderer.example.com       | 	Kafka.Retry.Metadata.RetryBackoff = 250ms
orderer.example.com       | 	Kafka.Retry.Producer.RetryMax = 3
orderer.example.com       | 	Kafka.Retry.Producer.RetryBackoff = 100ms
orderer.example.com       | 	Kafka.Retry.Consumer.RetryBackoff = 2s
orderer.example.com       | 	Kafka.Verbose = true
orderer.example.com       | 	Kafka.Version = 0.10.2.0
orderer.example.com       | 	Kafka.TLS.Enabled = false
orderer.example.com       | 	Kafka.TLS.PrivateKey = ""
orderer.example.com       | 	Kafka.TLS.Certificate = ""
orderer.example.com       | 	Kafka.TLS.RootCAs = []
orderer.example.com       | 	Kafka.TLS.ClientAuthRequired = false
orderer.example.com       | 	Kafka.TLS.ClientRootCAs = []
orderer.example.com       | 	Kafka.SASLPlain.Enabled = false
orderer.example.com       | 	Kafka.SASLPlain.User = ""
orderer.example.com       | 	Kafka.SASLPlain.Password = ""
orderer.example.com       | 	Kafka.Topic.ReplicationFactor = 1
orderer.example.com       | 	Debug.BroadcastTraceDir = ""
orderer.example.com       | 	Debug.DeliverTraceDir = ""
orderer.example.com       | 	Consensus = map[WALDir:/var/hyperledger/production/orderer/etcdraft/wal SnapDir:/var/hyperledger/production/orderer/etcdraft/snapshot]
orderer.example.com       | 	Operations.ListenAddress = "127.0.0.1:8443"
orderer.example.com       | 	Operations.TLS.Enabled = false
orderer.example.com       | 	Operations.TLS.PrivateKey = ""
orderer.example.com       | 	Operations.TLS.Certificate = ""
orderer.example.com       | 	Operations.TLS.RootCAs = []
orderer.example.com       | 	Operations.TLS.ClientAuthRequired = false
orderer.example.com       | 	Operations.TLS.ClientRootCAs = []
orderer.example.com       | 	Metrics.Provider = "disabled"
orderer.example.com       | 	Metrics.Statsd.Network = "udp"
orderer.example.com       | 	Metrics.Statsd.Address = "127.0.0.1:8125"
orderer.example.com       | 	Metrics.Statsd.WriteInterval = 30s
orderer.example.com       | 	Metrics.Statsd.Prefix = ""
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [fsblkstorage] LoadPreResetHeight -> INFO 022 Pre-reset heights loaded
peer1.org1.example.com    | 2019-10-22 15:06:15.818 UTC [nodeCmd] func7 -> INFO 023 Starting profiling server with listenAddress = 0.0.0.0:6060
orderer.example.com       | 2019-10-22 15:06:16.317 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
orderer.example.com       | 2019-10-22 15:06:16.320 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
orderer.example.com       | 2019-10-22 15:06:16.324 UTC [fsblkstorage] newBlockfileMgr -> INFO 005 Getting block information from block storage
orderer.example.com       | 2019-10-22 15:06:16.362 UTC [orderer.commmon.multichannel] Initialize -> INFO 006 Starting system channel 'byfn-sys-channel' with genesis block hash 6da0742ad1ab70247704d4088558b7d0fbec6496e10bf9cf2a3a3a4a9b05b924 and orderer type solo
orderer.example.com       | 2019-10-22 15:06:16.362 UTC [orderer.common.server] Start -> INFO 007 Starting orderer:
orderer.example.com       |  Version: 1.4.3
orderer.example.com       |  Commit SHA: b8c4a6a
orderer.example.com       |  Go version: go1.11.5
orderer.example.com       |  OS/Arch: linux/amd64
orderer.example.com       | 2019-10-22 15:06:16.362 UTC [orderer.common.server] Start -> INFO 008 Beginning to serve requests
peer0.org1.example.com    | 2019-10-22 15:06:16.731 UTC [comm.grpc.server] 1 -> INFO 027 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.5:50494 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=905.11427ms
peer1.org1.example.com    | 2019-10-22 15:06:16.730 UTC [comm.grpc.server] 1 -> INFO 024 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:18.73Z grpc.peer_address=172.19.0.4:58034 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=54.1µs
peer1.org1.example.com    | 2019-10-22 15:06:16.733 UTC [comm.grpc.server] 1 -> INFO 025 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:06:26.731Z grpc.peer_address=172.19.0.4:58034 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=2.340327ms
peer1.org1.example.com    | 2019-10-22 15:06:16.736 UTC [comm.grpc.server] 1 -> INFO 026 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:06:18.736Z grpc.peer_address=172.19.0.4:58036 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=51.974µs
```

> Channel Create

```
orderer.example.com       | 2019-10-22 15:16:52.902 UTC [fsblkstorage] newBlockfileMgr -> INFO 013 Getting block information from block storage
orderer.example.com       | 2019-10-22 15:16:52.905 UTC [comm.grpc.server] 1 -> INFO 014 streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Broadcast grpc.peer_address=172.19.0.7:49468 grpc.code=OK grpc.call_duration=18.775081ms
orderer.example.com       | 2019-10-22 15:16:52.907 UTC [orderer.commmon.multichannel] newChain -> INFO 015 Created and starting new chain mychannel
orderer.example.com       | 2019-10-22 15:16:52.913 UTC [common.deliver] Handle -> WARN 016 Error reading from 172.19.0.7:49466: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:16:52.913 UTC [comm.grpc.server] 1 -> INFO 017 streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Deliver grpc.peer_address=172.19.0.7:49466 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=29.663568ms
```

> Peer Join Channel

```
peer0.org1.example.com    | 2019-10-22 15:19:26.534 UTC [endorser] callChaincode -> INFO 02b [][8ec4ce68] Entry chaincode: name:"cscc"
peer0.org1.example.com    | 2019-10-22 15:19:26.537 UTC [ledgermgmt] CreateLedger -> INFO 02c Creating ledger [mychannel] with genesis block
peer0.org1.example.com    | 2019-10-22 15:19:26.539 UTC [fsblkstorage] newBlockfileMgr -> INFO 02d Getting block information from block storage
peer0.org1.example.com    | 2019-10-22 15:19:26.545 UTC [kvledger] CommitWithPvtData -> INFO 02e [mychannel] Committed block [0] with 1 transaction(s) in 2ms (state_validation=0ms block_and_pvtdata_commit=1ms state_commit=0ms) commitHash=[]
peer0.org1.example.com    | 2019-10-22 15:19:26.546 UTC [ledgermgmt] CreateLedger -> INFO 02f Created ledger [mychannel] with genesis block
peer0.org1.example.com    | 2019-10-22 15:19:26.549 UTC [gossip.gossip] JoinChan -> INFO 030 Joining gossip network of channel mychannel with 2 organizations
peer0.org1.example.com    | 2019-10-22 15:19:26.549 UTC [gossip.gossip] learnAnchorPeers -> INFO 031 No configured anchor peers of Org1MSP for channel mychannel to learn about
peer0.org1.example.com    | 2019-10-22 15:19:26.550 UTC [gossip.gossip] learnAnchorPeers -> INFO 032 No configured anchor peers of Org2MSP for channel mychannel to learn about
peer0.org1.example.com    | 2019-10-22 15:19:26.556 UTC [gossip.state] NewGossipStateProvider -> INFO 033 Updating metadata information, current ledger sequence is at = 0, next expected block is = 1
peer0.org1.example.com    | 2019-10-22 15:19:26.558 UTC [sccapi] deploySysCC -> INFO 034 system chaincode lscc/mychannel(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer0.org1.example.com    | 2019-10-22 15:19:26.559 UTC [cscc] Init -> INFO 035 Init CSCC
peer0.org1.example.com    | 2019-10-22 15:19:26.559 UTC [sccapi] deploySysCC -> INFO 036 system chaincode cscc/mychannel(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer0.org1.example.com    | 2019-10-22 15:19:26.560 UTC [qscc] Init -> INFO 037 Init QSCC
peer0.org1.example.com    | 2019-10-22 15:19:26.561 UTC [sccapi] deploySysCC -> INFO 038 system chaincode qscc/mychannel(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer0.org1.example.com    | 2019-10-22 15:19:26.561 UTC [sccapi] deploySysCC -> INFO 039 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer0.org1.example.com    | 2019-10-22 15:19:26.562 UTC [endorser] callChaincode -> INFO 03a [][8ec4ce68] Exit chaincode: name:"cscc"  (27ms)
peer0.org1.example.com    | 2019-10-22 15:19:26.562 UTC [comm.grpc.server] 1 -> INFO 03b unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:50436 grpc.code=OK grpc.call_duration=28.852549ms
peer0.org1.example.com    | 2019-10-22 15:19:32.559 UTC [gossip.election] beLeader -> INFO 03c 8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c : Becoming a leader
peer0.org1.example.com    | 2019-10-22 15:19:32.560 UTC [gossip.service] func1 -> INFO 03d Elected as a leader, starting delivery service for channel mychannel
peer1.org1.example.com    | 2019-10-22 15:20:30.655 UTC [endorser] callChaincode -> INFO 027 [][4c7b36f7] Entry chaincode: name:"cscc"
peer1.org1.example.com    | 2019-10-22 15:20:30.657 UTC [ledgermgmt] CreateLedger -> INFO 028 Creating ledger [mychannel] with genesis block
peer1.org1.example.com    | 2019-10-22 15:20:30.659 UTC [fsblkstorage] newBlockfileMgr -> INFO 029 Getting block information from block storage
peer1.org1.example.com    | 2019-10-22 15:20:30.664 UTC [kvledger] CommitWithPvtData -> INFO 02a [mychannel] Committed block [0] with 1 transaction(s) in 2ms (state_validation=0ms block_and_pvtdata_commit=1ms state_commit=0ms) commitHash=[]
peer1.org1.example.com    | 2019-10-22 15:20:30.665 UTC [ledgermgmt] CreateLedger -> INFO 02b Created ledger [mychannel] with genesis block
peer1.org1.example.com    | 2019-10-22 15:20:30.668 UTC [gossip.gossip] JoinChan -> INFO 02c Joining gossip network of channel mychannel with 2 organizations
peer1.org1.example.com    | 2019-10-22 15:20:30.670 UTC [gossip.gossip] learnAnchorPeers -> INFO 02d No configured anchor peers of Org2MSP for channel mychannel to learn about
peer1.org1.example.com    | 2019-10-22 15:20:30.670 UTC [gossip.gossip] learnAnchorPeers -> INFO 02e No configured anchor peers of Org1MSP for channel mychannel to learn about
peer1.org1.example.com    | 2019-10-22 15:20:30.677 UTC [gossip.state] NewGossipStateProvider -> INFO 02f Updating metadata information, current ledger sequence is at = 0, next expected block is = 1
peer1.org1.example.com    | 2019-10-22 15:20:30.679 UTC [sccapi] deploySysCC -> INFO 030 system chaincode lscc/mychannel(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer1.org1.example.com    | 2019-10-22 15:20:30.680 UTC [cscc] Init -> INFO 031 Init CSCC
peer1.org1.example.com    | 2019-10-22 15:20:30.681 UTC [sccapi] deploySysCC -> INFO 032 system chaincode cscc/mychannel(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer1.org1.example.com    | 2019-10-22 15:20:30.681 UTC [qscc] Init -> INFO 033 Init QSCC
peer1.org1.example.com    | 2019-10-22 15:20:30.682 UTC [sccapi] deploySysCC -> INFO 034 system chaincode qscc/mychannel(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer1.org1.example.com    | 2019-10-22 15:20:30.683 UTC [sccapi] deploySysCC -> INFO 035 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer1.org1.example.com    | 2019-10-22 15:20:30.683 UTC [endorser] callChaincode -> INFO 036 [][4c7b36f7] Exit chaincode: name:"cscc"  (28ms)
peer1.org1.example.com    | 2019-10-22 15:20:30.685 UTC [comm.grpc.server] 1 -> INFO 037 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:41978 grpc.code=OK grpc.call_duration=30.424378ms
peer1.org1.example.com    | 2019-10-22 15:20:35.669 UTC [gossip.channel] reportMembershipChanges -> INFO 038 Membership view has changed. peers went online:  [[peer0.org1.example.com:7051]] , current view:  [[peer0.org1.example.com:7051]]
peer0.org1.example.com    | 2019-10-22 15:20:36.550 UTC [gossip.channel] reportMembershipChanges -> INFO 03e Membership view has changed. peers went online:  [[peer1.org1.example.com:8051]] , current view:  [[peer1.org1.example.com:8051]]
peer1.org1.example.com    | 2019-10-22 15:20:36.680 UTC [gossip.election] beLeader -> INFO 039 6416af3fc1a5e20aa872b9210b5d74c1d9b34009b289e072713cf775d26e4bb4 : Becoming a leader
peer1.org1.example.com    | 2019-10-22 15:20:36.681 UTC [gossip.service] func1 -> INFO 03a Elected as a leader, starting delivery service for channel mychannel
peer0.org1.example.com    | 2019-10-22 15:20:36.691 UTC [gossip.election] stopBeingLeader -> INFO 03f 8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c Stopped being a leader
peer0.org1.example.com    | 2019-10-22 15:20:36.691 UTC [gossip.service] func1 -> INFO 040 Renounced leadership, stopping delivery service for channel mychannel
peer0.org1.example.com    | 2019-10-22 15:20:36.692 UTC [deliveryClient] try -> WARN 041 Got error: rpc error: code = Unavailable desc = transport is closing , at 1 attempt. Retrying in 1s
peer0.org1.example.com    | 2019-10-22 15:20:36.692 UTC [blocksProvider] DeliverBlocks -> WARN 042 [mychannel] Receive error: client is closing
orderer.example.com       | 2019-10-22 15:20:36.693 UTC [comm.grpc.server] 1 -> INFO 018 streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Deliver grpc.peer_address=172.19.0.4:34650 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" error="context finished before block retrieved: context canceled" grpc.code=Unknown grpc.call_duration=1m4.119626529s
peer0.org2.example.com    | 2019-10-22 15:20:44.604 UTC [endorser] callChaincode -> INFO 027 [][bee704fd] Entry chaincode: name:"cscc"
peer0.org2.example.com    | 2019-10-22 15:20:44.606 UTC [ledgermgmt] CreateLedger -> INFO 028 Creating ledger [mychannel] with genesis block
peer0.org2.example.com    | 2019-10-22 15:20:44.607 UTC [fsblkstorage] newBlockfileMgr -> INFO 029 Getting block information from block storage
peer0.org2.example.com    | 2019-10-22 15:20:44.613 UTC [kvledger] CommitWithPvtData -> INFO 02a [mychannel] Committed block [0] with 1 transaction(s) in 3ms (state_validation=0ms block_and_pvtdata_commit=1ms state_commit=0ms) commitHash=[]
peer0.org2.example.com    | 2019-10-22 15:20:44.614 UTC [ledgermgmt] CreateLedger -> INFO 02b Created ledger [mychannel] with genesis block
peer0.org2.example.com    | 2019-10-22 15:20:44.618 UTC [gossip.gossip] JoinChan -> INFO 02c Joining gossip network of channel mychannel with 2 organizations
peer0.org2.example.com    | 2019-10-22 15:20:44.619 UTC [gossip.gossip] learnAnchorPeers -> INFO 02d No configured anchor peers of Org2MSP for channel mychannel to learn about
peer0.org2.example.com    | 2019-10-22 15:20:44.619 UTC [gossip.gossip] learnAnchorPeers -> INFO 02e No configured anchor peers of Org1MSP for channel mychannel to learn about
peer0.org2.example.com    | 2019-10-22 15:20:44.626 UTC [gossip.state] NewGossipStateProvider -> INFO 02f Updating metadata information, current ledger sequence is at = 0, next expected block is = 1
peer0.org2.example.com    | 2019-10-22 15:20:44.628 UTC [sccapi] deploySysCC -> INFO 030 system chaincode lscc/mychannel(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer0.org2.example.com    | 2019-10-22 15:20:44.629 UTC [cscc] Init -> INFO 031 Init CSCC
peer0.org2.example.com    | 2019-10-22 15:20:44.630 UTC [sccapi] deploySysCC -> INFO 032 system chaincode cscc/mychannel(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer0.org2.example.com    | 2019-10-22 15:20:44.630 UTC [qscc] Init -> INFO 033 Init QSCC
peer0.org2.example.com    | 2019-10-22 15:20:44.631 UTC [sccapi] deploySysCC -> INFO 034 system chaincode qscc/mychannel(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer0.org2.example.com    | 2019-10-22 15:20:44.632 UTC [sccapi] deploySysCC -> INFO 035 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer0.org2.example.com    | 2019-10-22 15:20:44.632 UTC [endorser] callChaincode -> INFO 036 [][bee704fd] Exit chaincode: name:"cscc"  (28ms)
peer0.org2.example.com    | 2019-10-22 15:20:44.633 UTC [comm.grpc.server] 1 -> INFO 037 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:40328 grpc.code=OK grpc.call_duration=29.802773ms
peer0.org2.example.com    | 2019-10-22 15:20:50.629 UTC [gossip.election] beLeader -> INFO 038 ddbb1278b2fcbb0e1dce2e516b8d069eb12c49e2ab5925247488e04a8511e7c8 : Becoming a leader
peer0.org2.example.com    | 2019-10-22 15:20:50.629 UTC [gossip.service] func1 -> INFO 039 Elected as a leader, starting delivery service for channel mychannel
peer1.org2.example.com    | 2019-10-22 15:20:51.196 UTC [endorser] callChaincode -> INFO 026 [][f804b666] Entry chaincode: name:"cscc"
peer1.org2.example.com    | 2019-10-22 15:20:51.198 UTC [ledgermgmt] CreateLedger -> INFO 027 Creating ledger [mychannel] with genesis block
peer1.org2.example.com    | 2019-10-22 15:20:51.199 UTC [fsblkstorage] newBlockfileMgr -> INFO 028 Getting block information from block storage
peer1.org2.example.com    | 2019-10-22 15:20:51.205 UTC [kvledger] CommitWithPvtData -> INFO 029 [mychannel] Committed block [0] with 1 transaction(s) in 3ms (state_validation=0ms block_and_pvtdata_commit=1ms state_commit=0ms) commitHash=[]
peer1.org2.example.com    | 2019-10-22 15:20:51.207 UTC [ledgermgmt] CreateLedger -> INFO 02a Created ledger [mychannel] with genesis block
peer1.org2.example.com    | 2019-10-22 15:20:51.209 UTC [gossip.gossip] JoinChan -> INFO 02b Joining gossip network of channel mychannel with 2 organizations
peer1.org2.example.com    | 2019-10-22 15:20:51.210 UTC [gossip.gossip] learnAnchorPeers -> INFO 02c No configured anchor peers of Org2MSP for channel mychannel to learn about
peer1.org2.example.com    | 2019-10-22 15:20:51.210 UTC [gossip.gossip] learnAnchorPeers -> INFO 02d No configured anchor peers of Org1MSP for channel mychannel to learn about
peer1.org2.example.com    | 2019-10-22 15:20:51.219 UTC [gossip.state] NewGossipStateProvider -> INFO 02e Updating metadata information, current ledger sequence is at = 0, next expected block is = 1
peer1.org2.example.com    | 2019-10-22 15:20:51.220 UTC [sccapi] deploySysCC -> INFO 02f system chaincode lscc/mychannel(github.com/hyperledger/fabric/core/scc/lscc) deployed
peer1.org2.example.com    | 2019-10-22 15:20:51.221 UTC [cscc] Init -> INFO 030 Init CSCC
peer1.org2.example.com    | 2019-10-22 15:20:51.221 UTC [sccapi] deploySysCC -> INFO 031 system chaincode cscc/mychannel(github.com/hyperledger/fabric/core/scc/cscc) deployed
peer1.org2.example.com    | 2019-10-22 15:20:51.222 UTC [qscc] Init -> INFO 032 Init QSCC
peer1.org2.example.com    | 2019-10-22 15:20:51.223 UTC [sccapi] deploySysCC -> INFO 033 system chaincode qscc/mychannel(github.com/hyperledger/fabric/core/scc/qscc) deployed
peer1.org2.example.com    | 2019-10-22 15:20:51.223 UTC [sccapi] deploySysCC -> INFO 034 system chaincode (+lifecycle,github.com/hyperledger/fabric/core/chaincode/lifecycle) disabled
peer1.org2.example.com    | 2019-10-22 15:20:51.224 UTC [endorser] callChaincode -> INFO 035 [][f804b666] Exit chaincode: name:"cscc"  (27ms)
peer1.org2.example.com    | 2019-10-22 15:20:51.224 UTC [comm.grpc.server] 1 -> INFO 036 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:42332 grpc.code=OK grpc.call_duration=31.027954ms
peer0.org2.example.com    | 2019-10-22 15:20:54.618 UTC [gossip.channel] reportMembershipChanges -> INFO 03a Membership view has changed. peers went online:  [[peer1.org2.example.com:10051]] , current view:  [[peer1.org2.example.com:10051]]
peer1.org2.example.com    | 2019-10-22 15:20:55.636 UTC [gossip.election] leaderElection -> INFO 037 bac0dd3f0d7f2ba0e44f9e9f6170fdfb658b160e8dfab97983ed01a8846b02e1 : Some peer is already a leader
peer1.org2.example.com    | 2019-10-22 15:20:56.210 UTC [gossip.channel] reportMembershipChanges -> INFO 038 Membership view has changed. peers went online:  [[peer0.org2.example.com:9051]] , current view:  [[peer0.org2.example.com:9051]]
```

> Anchor Peer Update

```
orderer.example.com       | 2019-10-22 15:22:16.909 UTC [common.deliver] Handle -> WARN 019 Error reading from 172.19.0.7:49486: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:22:16.910 UTC [comm.grpc.server] 1 -> INFO 01a streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Deliver grpc.peer_address=172.19.0.7:49486 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=19.148775ms
orderer.example.com       | 2019-10-22 15:22:16.911 UTC [orderer.common.broadcast] Handle -> WARN 01b Error reading from 172.19.0.7:49488: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:22:16.911 UTC [comm.grpc.server] 1 -> INFO 01c streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Broadcast grpc.peer_address=172.19.0.7:49488 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=18.457719ms
peer0.org2.example.com    | 2019-10-22 15:22:16.916 UTC [gossip.privdata] StoreBlock -> INFO 03b [mychannel] Received block [1] from buffer
peer1.org1.example.com    | 2019-10-22 15:22:16.921 UTC [gossip.privdata] StoreBlock -> INFO 03b [mychannel] Received block [1] from buffer
peer1.org1.example.com    | 2019-10-22 15:22:16.926 UTC [gossip.gossip] JoinChan -> INFO 03c Joining gossip network of channel mychannel with 2 organizations
peer0.org2.example.com    | 2019-10-22 15:22:16.928 UTC [gossip.gossip] JoinChan -> INFO 03c Joining gossip network of channel mychannel with 2 organizations
peer0.org2.example.com    | 2019-10-22 15:22:16.929 UTC [gossip.gossip] learnAnchorPeers -> INFO 03d No configured anchor peers of Org2MSP for channel mychannel to learn about
peer0.org2.example.com    | 2019-10-22 15:22:16.929 UTC [gossip.gossip] learnAnchorPeers -> INFO 03e Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org1.example.com    | 2019-10-22 15:22:16.931 UTC [gossip.gossip] learnAnchorPeers -> INFO 03d Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org1.example.com    | 2019-10-22 15:22:16.932 UTC [gossip.gossip] learnAnchorPeers -> INFO 03e No configured anchor peers of Org2MSP for channel mychannel to learn about
peer1.org2.example.com    | 2019-10-22 15:22:16.934 UTC [gossip.privdata] StoreBlock -> INFO 039 [mychannel] Received block [1] from buffer
peer0.org2.example.com    | 2019-10-22 15:22:16.939 UTC [committer.txvalidator] Validate -> INFO 03f [mychannel] Validated block [1] in 21ms
peer0.org1.example.com    | 2019-10-22 15:22:16.943 UTC [gossip.privdata] StoreBlock -> INFO 046 [mychannel] Received block [1] from buffer
peer0.org1.example.com    | 2019-10-22 15:22:16.948 UTC [gossip.gossip] JoinChan -> INFO 047 Joining gossip network of channel mychannel with 2 organizations
peer1.org1.example.com    | 2019-10-22 15:22:16.949 UTC [committer.txvalidator] Validate -> INFO 03f [mychannel] Validated block [1] in 28ms
peer1.org2.example.com    | 2019-10-22 15:22:16.952 UTC [gossip.gossip] JoinChan -> INFO 03a Joining gossip network of channel mychannel with 2 organizations
peer1.org2.example.com    | 2019-10-22 15:22:16.954 UTC [gossip.gossip] learnAnchorPeers -> INFO 03b Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org2.example.com    | 2019-10-22 15:22:16.955 UTC [gossip.gossip] learnAnchorPeers -> INFO 03c No configured anchor peers of Org2MSP for channel mychannel to learn about
peer1.org2.example.com    | 2019-10-22 15:22:16.956 UTC [gossip.service] updateEndpoints -> WARN 03d Failed to update ordering service endpoints, due to Channel with mychannel id was not found
peer0.org2.example.com    | 2019-10-22 15:22:16.957 UTC [kvledger] CommitWithPvtData -> INFO 040 [mychannel] Committed block [1] with 1 transaction(s) in 16ms (state_validation=0ms block_and_pvtdata_commit=14ms state_commit=0ms) commitHash=[47dc540c94ceb704a23875c11273e16bb0b8a87aed84de911f2133568115f254]
peer1.org2.example.com    | 2019-10-22 15:22:16.958 UTC [committer.txvalidator] Validate -> INFO 03e [mychannel] Validated block [1] in 23ms
peer1.org1.example.com    | 2019-10-22 15:22:16.960 UTC [kvledger] CommitWithPvtData -> INFO 040 [mychannel] Committed block [1] with 1 transaction(s) in 7ms (state_validation=0ms block_and_pvtdata_commit=3ms state_commit=1ms) commitHash=[47dc540c94ceb704a23875c11273e16bb0b8a87aed84de911f2133568115f254]
peer0.org1.example.com    | 2019-10-22 15:22:16.965 UTC [comm.grpc.server] 1 -> INFO 049 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:18.965Z grpc.peer_address=172.19.0.3:50394 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=61.931µs
peer0.org1.example.com    | 2019-10-22 15:22:16.959 UTC [gossip.gossip] learnAnchorPeers -> INFO 048 No configured anchor peers of Org2MSP for channel mychannel to learn about
peer0.org1.example.com    | 2019-10-22 15:22:16.966 UTC [gossip.gossip] learnAnchorPeers -> INFO 04a Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer0.org1.example.com    | 2019-10-22 15:22:16.967 UTC [gossip.gossip] learnAnchorPeers -> INFO 04b Anchor peer with same endpoint, skipping connecting to myself
peer0.org1.example.com    | 2019-10-22 15:22:16.967 UTC [gossip.service] updateEndpoints -> WARN 04c Failed to update ordering service endpoints, due to Channel with mychannel id was not found
peer0.org1.example.com    | 2019-10-22 15:22:16.969 UTC [committer.txvalidator] Validate -> INFO 04d [mychannel] Validated block [1] in 25ms
peer1.org2.example.com    | 2019-10-22 15:22:16.973 UTC [kvledger] CommitWithPvtData -> INFO 03f [mychannel] Committed block [1] with 1 transaction(s) in 13ms (state_validation=0ms block_and_pvtdata_commit=11ms state_commit=1ms) commitHash=[47dc540c94ceb704a23875c11273e16bb0b8a87aed84de911f2133568115f254]
peer0.org1.example.com    | 2019-10-22 15:22:16.973 UTC [comm.grpc.server] 1 -> INFO 04e unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:18.972Z grpc.peer_address=172.19.0.5:50538 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=982.941µs
peer0.org1.example.com    | 2019-10-22 15:22:16.981 UTC [comm.grpc.server] 1 -> INFO 04f streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:22:26.976Z grpc.peer_address=172.19.0.3:50394 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=5.777982ms
peer1.org1.example.com    | 2019-10-22 15:22:16.984 UTC [comm.grpc.server] 1 -> INFO 041 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.4:58036 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=16m0.246103275s
peer0.org1.example.com    | 2019-10-22 15:22:16.986 UTC [comm.grpc.server] 1 -> INFO 050 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:18.986Z grpc.peer_address=172.19.0.2:47902 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=48.508µs
peer0.org1.example.com    | 2019-10-22 15:22:16.986 UTC [comm.grpc.server] 1 -> INFO 051 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:22:26.981Z grpc.peer_address=172.19.0.5:50538 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=5.515157ms
peer0.org1.example.com    | 2019-10-22 15:22:16.987 UTC [comm.grpc.server] 1 -> INFO 052 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:18.987Z grpc.peer_address=172.19.0.3:50398 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=39.403µs
peer0.org1.example.com    | 2019-10-22 15:22:16.996 UTC [kvledger] CommitWithPvtData -> INFO 053 [mychannel] Committed block [1] with 1 transaction(s) in 26ms (state_validation=0ms block_and_pvtdata_commit=18ms state_commit=2ms) commitHash=[47dc540c94ceb704a23875c11273e16bb0b8a87aed84de911f2133568115f254]
peer0.org1.example.com    | 2019-10-22 15:22:16.997 UTC [comm.grpc.server] 1 -> INFO 054 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:22:26.991Z grpc.peer_address=172.19.0.2:47902 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=6.478337ms
peer0.org1.example.com    | 2019-10-22 15:22:17.001 UTC [comm.grpc.server] 1 -> INFO 055 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:19.001Z grpc.peer_address=172.19.0.2:47906 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=52.251µs
peer1.org1.example.com    | 2019-10-22 15:22:18.555 UTC [comm.grpc.server] 1 -> INFO 042 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:20.555Z grpc.peer_address=172.19.0.4:58086 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=55.679µs
peer0.org2.example.com    | 2019-10-22 15:22:19.618 UTC [gossip.channel] reportMembershipChanges -> INFO 041 Membership view has changed. peers went online:  [[peer0.org1.example.com:7051 ]] , current view:  [[peer1.org2.example.com:10051] [peer0.org1.example.com:7051 ]]
peer1.org1.example.com    | 2019-10-22 15:22:20.939 UTC [comm.grpc.server] 1 -> INFO 043 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:22.939Z grpc.peer_address=172.19.0.3:45128 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=85.898µs
peer1.org1.example.com    | 2019-10-22 15:22:20.949 UTC [comm.grpc.server] 1 -> INFO 044 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:22:22.949Z grpc.peer_address=172.19.0.2:34654 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=52.989µs
peer1.org2.example.com    | 2019-10-22 15:22:21.210 UTC [gossip.channel] reportMembershipChanges -> INFO 040 Membership view has changed. peers went online:  [[peer0.org1.example.com:7051 ]] , current view:  [[peer0.org2.example.com:9051] [peer0.org1.example.com:7051 ]]
peer0.org1.example.com    | 2019-10-22 15:22:21.550 UTC [gossip.channel] reportMembershipChanges -> INFO 056 Membership view has changed. peers went online:  [[peer0.org2.example.com:9051 ] [peer1.org2.example.com:10051 ]] , current view:  [[peer1.org1.example.com:8051] [peer0.org2.example.com:9051 ] [peer1.org2.example.com:10051 ]]
peer1.org2.example.com    | 2019-10-22 15:22:26.210 UTC [gossip.channel] reportMembershipChanges -> INFO 041 Membership view has changed. peers went online:  [[peer1.org1.example.com:8051 ]] , current view:  [[peer0.org2.example.com:9051] [peer0.org1.example.com:7051 ] [peer1.org1.example.com:8051 ]]
peer0.org2.example.com    | 2019-10-22 15:22:29.618 UTC [gossip.channel] reportMembershipChanges -> INFO 042 Membership view has changed. peers went online:  [[peer1.org1.example.com:8051 ]] , current view:  [[peer0.org1.example.com:7051 ] [peer1.org1.example.com:8051 ] [peer1.org2.example.com:10051]]
peer1.org1.example.com    | 2019-10-22 15:22:30.669 UTC [gossip.channel] reportMembershipChanges -> INFO 045 Membership view has changed. peers went online:  [[peer0.org2.example.com:9051 ] [peer1.org2.example.com:10051 ]] , current view:  [[peer0.org2.example.com:9051 ] [peer0.org1.example.com:7051] [peer1.org2.example.com:10051 ]]



orderer.example.com       | 2019-10-22 15:23:02.829 UTC [common.deliver] Handle -> WARN 01d Error reading from 172.19.0.7:49506: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:23:02.830 UTC [comm.grpc.server] 1 -> INFO 01e streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Deliver grpc.peer_address=172.19.0.7:49506 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=19.547391ms
orderer.example.com       | 2019-10-22 15:23:02.831 UTC [orderer.common.broadcast] Handle -> WARN 01f Error reading from 172.19.0.7:49508: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:23:02.831 UTC [comm.grpc.server] 1 -> INFO 020 streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Broadcast grpc.peer_address=172.19.0.7:49508 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=18.490393ms
peer1.org1.example.com    | 2019-10-22 15:23:02.836 UTC [gossip.privdata] StoreBlock -> INFO 046 [mychannel] Received block [2] from buffer
peer0.org2.example.com    | 2019-10-22 15:23:02.841 UTC [gossip.privdata] StoreBlock -> INFO 043 [mychannel] Received block [2] from buffer
peer1.org1.example.com    | 2019-10-22 15:23:02.847 UTC [gossip.gossip] JoinChan -> INFO 047 Joining gossip network of channel mychannel with 2 organizations
peer0.org2.example.com    | 2019-10-22 15:23:02.849 UTC [gossip.gossip] JoinChan -> INFO 044 Joining gossip network of channel mychannel with 2 organizations
peer1.org2.example.com    | 2019-10-22 15:23:02.851 UTC [gossip.privdata] StoreBlock -> INFO 042 [mychannel] Received block [2] from buffer
peer1.org1.example.com    | 2019-10-22 15:23:02.855 UTC [gossip.gossip] learnAnchorPeers -> INFO 048 Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org1.example.com    | 2019-10-22 15:23:02.856 UTC [gossip.gossip] learnAnchorPeers -> INFO 049 Learning about the configured anchor peers of Org2MSP for channel mychannel : [{peer0.org2.example.com 9051}]
peer0.org2.example.com    | 2019-10-22 15:23:02.850 UTC [gossip.gossip] learnAnchorPeers -> INFO 045 Learning about the configured anchor peers of Org2MSP for channel mychannel : [{peer0.org2.example.com 9051}]
peer1.org1.example.com    | 2019-10-22 15:23:02.858 UTC [committer.txvalidator] Validate -> INFO 04a [mychannel] Validated block [2] in 20ms
peer0.org2.example.com    | 2019-10-22 15:23:02.859 UTC [gossip.gossip] learnAnchorPeers -> INFO 046 Anchor peer with same endpoint, skipping connecting to myself
peer0.org2.example.com    | 2019-10-22 15:23:02.860 UTC [gossip.gossip] learnAnchorPeers -> INFO 047 Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer0.org2.example.com    | 2019-10-22 15:23:02.862 UTC [committer.txvalidator] Validate -> INFO 048 [mychannel] Validated block [2] in 20ms
peer1.org2.example.com    | 2019-10-22 15:23:02.866 UTC [gossip.gossip] JoinChan -> INFO 043 Joining gossip network of channel mychannel with 2 organizations
peer1.org2.example.com    | 2019-10-22 15:23:02.866 UTC [gossip.gossip] learnAnchorPeers -> INFO 044 Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org2.example.com    | 2019-10-22 15:23:02.869 UTC [gossip.gossip] learnAnchorPeers -> INFO 045 Learning about the configured anchor peers of Org2MSP for channel mychannel : [{peer0.org2.example.com 9051}]
peer1.org2.example.com    | 2019-10-22 15:23:02.869 UTC [gossip.service] updateEndpoints -> WARN 046 Failed to update ordering service endpoints, due to Channel with mychannel id was not found
peer0.org1.example.com    | 2019-10-22 15:23:02.879 UTC [comm.grpc.server] 1 -> INFO 057 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.879Z grpc.peer_address=172.19.0.3:50412 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=71.888µs
peer0.org1.example.com    | 2019-10-22 15:23:02.881 UTC [comm.grpc.server] 1 -> INFO 058 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.3:50398 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=45.883216998s
peer0.org1.example.com    | 2019-10-22 15:23:02.882 UTC [comm.grpc.server] 1 -> INFO 059 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.88Z grpc.peer_address=172.19.0.3:50412 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=1.725784ms
peer0.org1.example.com    | 2019-10-22 15:23:02.884 UTC [gossip.privdata] StoreBlock -> INFO 05a [mychannel] Received block [2] from buffer
peer0.org2.example.com    | 2019-10-22 15:23:02.891 UTC [gossip.comm] func1 -> WARN 049 peer0.org1.example.com:7051, PKIid:8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c isn't responsive: EOF
peer1.org2.example.com    | 2019-10-22 15:23:02.894 UTC [committer.txvalidator] Validate -> INFO 047 [mychannel] Validated block [2] in 42ms
peer0.org2.example.com    | 2019-10-22 15:23:02.895 UTC [gossip.discovery] expireDeadMembers -> WARN 04a Entering [8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c]
peer0.org2.example.com    | 2019-10-22 15:23:02.896 UTC [gossip.discovery] expireDeadMembers -> WARN 04b Closing connection to Endpoint: peer0.org1.example.com:7051, InternalEndpoint: , PKI-ID: 8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c, Metadata:
peer0.org2.example.com    | 2019-10-22 15:23:02.897 UTC [gossip.discovery] expireDeadMembers -> WARN 04c Exiting
peer1.org1.example.com    | 2019-10-22 15:23:02.899 UTC [kvledger] CommitWithPvtData -> INFO 04b [mychannel] Committed block [2] with 1 transaction(s) in 40ms (state_validation=29ms block_and_pvtdata_commit=6ms state_commit=1ms) commitHash=[5f88b61407b149a48413433f4670c46531e5c4a8febdc339a9536ff8716a559e]
peer0.org2.example.com    | 2019-10-22 15:23:02.905 UTC [comm.grpc.server] 1 -> INFO 04d unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.905Z grpc.peer_address=172.19.0.5:53134 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=63.726µs
peer0.org1.example.com    | 2019-10-22 15:23:02.909 UTC [gossip.gossip] JoinChan -> INFO 05b Joining gossip network of channel mychannel with 2 organizations
peer0.org2.example.com    | 2019-10-22 15:23:02.912 UTC [comm.grpc.server] 1 -> INFO 04e unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.91Z grpc.peer_address=172.19.0.2:53058 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=72.053µs
peer0.org1.example.com    | 2019-10-22 15:23:02.915 UTC [gossip.gossip] learnAnchorPeers -> INFO 05c Learning about the configured anchor peers of Org2MSP for channel mychannel : [{peer0.org2.example.com 9051}]
peer0.org1.example.com    | 2019-10-22 15:23:02.917 UTC [gossip.gossip] learnAnchorPeers -> INFO 05d Learning about the configured anchor peers of Org1MSP for channel mychannel : [{peer0.org1.example.com 7051}]
peer1.org2.example.com    | 2019-10-22 15:23:02.918 UTC [kvledger] CommitWithPvtData -> INFO 048 [mychannel] Committed block [2] with 1 transaction(s) in 23ms (state_validation=1ms block_and_pvtdata_commit=11ms state_commit=7ms) commitHash=[5f88b61407b149a48413433f4670c46531e5c4a8febdc339a9536ff8716a559e]
peer0.org1.example.com    | 2019-10-22 15:23:02.919 UTC [gossip.gossip] learnAnchorPeers -> INFO 05e Anchor peer with same endpoint, skipping connecting to myself
peer0.org1.example.com    | 2019-10-22 15:23:02.919 UTC [gossip.service] updateEndpoints -> WARN 05f Failed to update ordering service endpoints, due to Channel with mychannel id was not found
peer1.org1.example.com    | 2019-10-22 15:23:02.926 UTC [comm.grpc.server] 1 -> INFO 04c streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.3:45128 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=41.986098918s
peer0.org1.example.com    | 2019-10-22 15:23:02.928 UTC [committer.txvalidator] Validate -> INFO 061 [mychannel] Validated block [2] in 43ms
peer0.org2.example.com    | 2019-10-22 15:23:02.929 UTC [comm.grpc.server] 1 -> INFO 04f streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.916Z grpc.peer_address=172.19.0.5:53134 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=12.907768ms
peer0.org2.example.com    | 2019-10-22 15:23:02.932 UTC [comm.grpc.server] 1 -> INFO 050 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.2:52984 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=16m47.124634509s
peer0.org1.example.com    | 2019-10-22 15:23:02.923 UTC [comm.grpc.server] 1 -> INFO 060 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.923Z grpc.peer_address=172.19.0.5:50560 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=54.411µs
peer0.org1.example.com    | 2019-10-22 15:23:02.934 UTC [comm.grpc.server] 1 -> INFO 062 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.934Z grpc.peer_address=172.19.0.2:47926 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=51.997µs
peer0.org2.example.com    | 2019-10-22 15:23:02.933 UTC [comm.grpc.server] 1 -> INFO 051 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.93Z grpc.peer_address=172.19.0.2:53058 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=3.397971ms
peer0.org2.example.com    | 2019-10-22 15:23:02.937 UTC [kvledger] CommitWithPvtData -> INFO 052 [mychannel] Committed block [2] with 1 transaction(s) in 72ms (state_validation=0ms block_and_pvtdata_commit=49ms state_commit=10ms) commitHash=[5f88b61407b149a48413433f4670c46531e5c4a8febdc339a9536ff8716a559e]
peer1.org1.example.com    | 2019-10-22 15:23:02.938 UTC [comm.grpc.server] 1 -> INFO 04d streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.4:58086 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=44.381341959s
peer0.org2.example.com    | 2019-10-22 15:23:02.941 UTC [comm.grpc.server] 1 -> INFO 053 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.941Z grpc.peer_address=172.19.0.4:41418 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=50.052µs
peer0.org1.example.com    | 2019-10-22 15:23:02.941 UTC [comm.grpc.server] 1 -> INFO 063 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.936Z grpc.peer_address=172.19.0.5:50560 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=4.65831ms
peer0.org2.example.com    | 2019-10-22 15:23:02.947 UTC [comm.grpc.server] 1 -> INFO 054 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.942Z grpc.peer_address=172.19.0.4:41418 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=4.785757ms
peer0.org2.example.com    | 2019-10-22 15:23:02.952 UTC [comm.grpc.server] 1 -> INFO 055 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:04.952Z grpc.peer_address=172.19.0.4:41420 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=52.136µs
peer0.org1.example.com    | 2019-10-22 15:23:02.955 UTC [comm.grpc.server] 1 -> INFO 064 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.peer_address=172.19.0.2:47906 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=45.952162868s
peer0.org1.example.com    | 2019-10-22 15:23:02.956 UTC [comm.grpc.server] 1 -> INFO 065 streaming call completed grpc.service=gossip.Gossip grpc.method=GossipStream grpc.request_deadline=2019-10-22T15:23:12.95Z grpc.peer_address=172.19.0.2:47926 grpc.peer_subject="CN=peer1.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=5.577433ms
peer0.org1.example.com    | 2019-10-22 15:23:02.961 UTC [kvledger] CommitWithPvtData -> INFO 066 [mychannel] Committed block [2] with 1 transaction(s) in 29ms (state_validation=0ms block_and_pvtdata_commit=28ms state_commit=0ms) commitHash=[5f88b61407b149a48413433f4670c46531e5c4a8febdc339a9536ff8716a559e]
peer1.org2.example.com    | 2019-10-22 15:23:02.972 UTC [gossip.comm] func1 -> WARN 049 peer0.org2.example.com:9051, PKIid:ddbb1278b2fcbb0e1dce2e516b8d069eb12c49e2ab5925247488e04a8511e7c8 isn't responsive: EOF
peer1.org2.example.com    | 2019-10-22 15:23:02.972 UTC [gossip.comm] func1 -> WARN 04a peer0.org1.example.com:7051, PKIid:8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c isn't responsive: EOF
peer1.org2.example.com    | 2019-10-22 15:23:02.973 UTC [gossip.discovery] expireDeadMembers -> WARN 04b Entering [ddbb1278b2fcbb0e1dce2e516b8d069eb12c49e2ab5925247488e04a8511e7c8]
peer1.org2.example.com    | 2019-10-22 15:23:02.974 UTC [gossip.discovery] expireDeadMembers -> WARN 04c Closing connection to Endpoint: peer0.org2.example.com:9051, InternalEndpoint: peer0.org2.example.com:9051, PKI-ID: ddbb1278b2fcbb0e1dce2e516b8d069eb12c49e2ab5925247488e04a8511e7c8, Metadata:
peer1.org2.example.com    | 2019-10-22 15:23:02.974 UTC [gossip.discovery] expireDeadMembers -> WARN 04d Exiting
peer1.org2.example.com    | 2019-10-22 15:23:02.975 UTC [gossip.discovery] expireDeadMembers -> WARN 04e Entering [8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c]
peer1.org2.example.com    | 2019-10-22 15:23:02.975 UTC [gossip.discovery] expireDeadMembers -> WARN 04f Closing connection to Endpoint: peer0.org1.example.com:7051, InternalEndpoint: , PKI-ID: 8c7536ced6e0c5761b692d697614fb9856bde11d39e081e508a1c8e691808c4c, Metadata:
peer1.org2.example.com    | 2019-10-22 15:23:02.976 UTC [gossip.discovery] expireDeadMembers -> WARN 050 Exiting
peer0.org2.example.com    | 2019-10-22 15:23:03.237 UTC [comm.grpc.server] 1 -> INFO 056 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:05.236Z grpc.peer_address=172.19.0.5:53146 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=58.886µs
peer0.org1.example.com    | 2019-10-22 15:23:03.238 UTC [comm.grpc.server] 1 -> INFO 067 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:05.238Z grpc.peer_address=172.19.0.5:50572 grpc.peer_subject="CN=peer1.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=51.856µs
peer1.org2.example.com    | 2019-10-22 15:23:03.256 UTC [comm.grpc.server] 1 -> INFO 051 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:05.255Z grpc.peer_address=172.19.0.4:36334 grpc.peer_subject="CN=peer0.org1.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=61.848µs
peer1.org2.example.com    | 2019-10-22 15:23:03.260 UTC [comm.grpc.server] 1 -> INFO 052 unary call completed grpc.service=gossip.Gossip grpc.method=Ping grpc.request_deadline=2019-10-22T15:23:05.259Z grpc.peer_address=172.19.0.3:56934 grpc.peer_subject="CN=peer0.org2.example.com,L=San Francisco,ST=California,C=US" grpc.code=OK grpc.call_duration=55.567µs
```

> Install ChainCode

```
peer0.org1.example.com    | 2019-10-22 15:37:12.997 UTC [endorser] callChaincode -> INFO 05e [][f8ce9931] Entry chaincode: name:"lscc"
peer0.org1.example.com    | 2019-10-22 15:37:12.998 UTC [lscc] executeInstall -> INFO 05f Installed Chaincode [mycc] Version [1.0] to peer
peer0.org1.example.com    | 2019-10-22 15:37:12.998 UTC [endorser] callChaincode -> INFO 060 [][f8ce9931] Exit chaincode: name:"lscc"  (1ms)
peer0.org1.example.com    | 2019-10-22 15:37:12.999 UTC [comm.grpc.server] 1 -> INFO 061 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:49590 grpc.code=OK grpc.call_duration=2.628743ms

peer1.org1.example.com    | 2019-10-22 15:37:21.954 UTC [endorser] callChaincode -> INFO 055 [][f41ac8c0] Entry chaincode: name:"lscc"
peer1.org1.example.com    | 2019-10-22 15:37:21.957 UTC [lscc] executeInstall -> INFO 056 Installed Chaincode [mycc] Version [1.0] to peer
peer1.org1.example.com    | 2019-10-22 15:37:21.958 UTC [endorser] callChaincode -> INFO 057 [][f41ac8c0] Exit chaincode: name:"lscc"  (3ms)
peer1.org1.example.com    | 2019-10-22 15:37:21.959 UTC [comm.grpc.server] 1 -> INFO 058 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:41360 grpc.code=OK grpc.call_duration=4.85328ms


peer0.org2.example.com    | 2019-10-22 15:37:30.613 UTC [endorser] callChaincode -> INFO 053 [][5a369f40] Entry chaincode: name:"lscc"
peer0.org2.example.com    | 2019-10-22 15:37:30.615 UTC [lscc] executeInstall -> INFO 054 Installed Chaincode [mycc] Version [1.0] to peer
peer0.org2.example.com    | 2019-10-22 15:37:30.616 UTC [endorser] callChaincode -> INFO 055 [][5a369f40] Exit chaincode: name:"lscc"  (2ms)
peer0.org2.example.com    | 2019-10-22 15:37:30.616 UTC [comm.grpc.server] 1 -> INFO 056 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:40486 grpc.code=OK grpc.call_duration=3.771975ms


peer1.org2.example.com    | 2019-10-22 15:37:37.073 UTC [endorser] callChaincode -> INFO 059 [][b01da6de] Entry chaincode: name:"lscc"
peer1.org2.example.com    | 2019-10-22 15:37:37.075 UTC [lscc] executeInstall -> INFO 05a Installed Chaincode [mycc] Version [1.0] to peer
peer1.org2.example.com    | 2019-10-22 15:37:37.077 UTC [endorser] callChaincode -> INFO 05b [][b01da6de] Exit chaincode: name:"lscc"  (3ms)
peer1.org2.example.com    | 2019-10-22 15:37:37.078 UTC [comm.grpc.server] 1 -> INFO 05c unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:42490 grpc.code=OK grpc.call_duration=5.219023ms
```

> Instantiate ChainCode

```
peer0.org1.example.com    | 2019-10-22 15:40:33.017 UTC [endorser] callChaincode -> INFO 065 [mychannel][3d47f052] Entry chaincode: name:"lscc"
peer0.org1.example.com    | 2019-10-22 15:40:33.029 UTC [chaincode.platform.golang] GenerateDockerBuild -> INFO 066 building chaincode with ldflagsOpt: '-ldflags "-linkmode external -extldflags '-static'"'
peer0.org1.example.com    | 2019-10-22 15:41:25.515 UTC [endorser] callChaincode -> INFO 067 [mychannel][3d47f052] Exit chaincode: name:"lscc"  (52497ms)
peer0.org1.example.com    | 2019-10-22 15:41:25.516 UTC [comm.grpc.server] 1 -> INFO 068 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:49610 grpc.code=OK grpc.call_duration=52.49951475s
orderer.example.com       | 2019-10-22 15:41:25.521 UTC [orderer.common.broadcast] Handle -> WARN 016 Error reading from 172.19.0.7:38356: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:41:25.522 UTC [comm.grpc.server] 1 -> INFO 017 streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Broadcast grpc.peer_address=172.19.0.7:38356 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=52.508006482s
peer0.org1.example.com    | 2019-10-22 15:41:27.522 UTC [gossip.privdata] StoreBlock -> INFO 069 [mychannel] Received block [3] from buffer
peer0.org2.example.com    | 2019-10-22 15:41:27.523 UTC [gossip.privdata] StoreBlock -> INFO 057 [mychannel] Received block [3] from buffer
peer0.org2.example.com    | 2019-10-22 15:41:27.526 UTC [committer.txvalidator] Validate -> INFO 058 [mychannel] Validated block [3] in 1ms
peer0.org1.example.com    | 2019-10-22 15:41:27.528 UTC [committer.txvalidator] Validate -> INFO 06a [mychannel] Validated block [3] in 4ms
peer0.org1.example.com    | 2019-10-22 15:41:27.529 UTC [cceventmgmt] HandleStateUpdates -> INFO 06b Channel [mychannel]: Handling deploy or update of chaincode [mycc]
peer1.org2.example.com    | 2019-10-22 15:41:27.532 UTC [gossip.privdata] StoreBlock -> INFO 05d [mychannel] Received block [3] from buffer
peer1.org1.example.com    | 2019-10-22 15:41:27.534 UTC [gossip.privdata] StoreBlock -> INFO 059 [mychannel] Received block [3] from buffer
peer1.org1.example.com    | 2019-10-22 15:41:27.536 UTC [committer.txvalidator] Validate -> INFO 05a [mychannel] Validated block [3] in 1ms
peer1.org1.example.com    | 2019-10-22 15:41:27.537 UTC [cceventmgmt] HandleStateUpdates -> INFO 05b Channel [mychannel]: Handling deploy or update of chaincode [mycc]
peer0.org2.example.com    | 2019-10-22 15:41:27.539 UTC [cceventmgmt] HandleStateUpdates -> INFO 059 Channel [mychannel]: Handling deploy or update of chaincode [mycc]
peer0.org1.example.com    | 2019-10-22 15:41:27.544 UTC [kvledger] CommitWithPvtData -> INFO 06c [mychannel] Committed block [3] with 1 transaction(s) in 14ms (state_validation=0ms block_and_pvtdata_commit=11ms state_commit=1ms) commitHash=[08d6d47dd12a66a250d98f24f564ac665fc26f40126afa808611d4d334c4704f]
peer1.org1.example.com    | 2019-10-22 15:41:27.545 UTC [kvledger] CommitWithPvtData -> INFO 05c [mychannel] Committed block [3] with 1 transaction(s) in 8ms (state_validation=0ms block_and_pvtdata_commit=4ms state_commit=0ms) commitHash=[08d6d47dd12a66a250d98f24f564ac665fc26f40126afa808611d4d334c4704f]
peer1.org2.example.com    | 2019-10-22 15:41:27.548 UTC [committer.txvalidator] Validate -> INFO 05e [mychannel] Validated block [3] in 8ms
peer0.org2.example.com    | 2019-10-22 15:41:27.549 UTC [kvledger] CommitWithPvtData -> INFO 05a [mychannel] Committed block [3] with 1 transaction(s) in 10ms (state_validation=0ms block_and_pvtdata_commit=3ms state_commit=2ms) commitHash=[08d6d47dd12a66a250d98f24f564ac665fc26f40126afa808611d4d334c4704f]
peer1.org2.example.com    | 2019-10-22 15:41:27.550 UTC [cceventmgmt] HandleStateUpdates -> INFO 05f Channel [mychannel]: Handling deploy or update of chaincode [mycc]
peer1.org2.example.com    | 2019-10-22 15:41:27.556 UTC [kvledger] CommitWithPvtData -> INFO 060 [mychannel] Committed block [3] with 1 transaction(s) in 6ms (state_validation=0ms block_and_pvtdata_commit=4ms state_commit=0ms) commitHash=[08d6d47dd12a66a250d98f24f564ac665fc26f40126afa808611d4d334c4704f]
```

> Query ChainCode

```
peer0.org1.example.com    | 2019-10-22 15:45:22.707 UTC [endorser] callChaincode -> INFO 088 [mychannel][dc492428] Entry chaincode: name:"mycc"
peer0.org1.example.com    | 2019-10-22 15:45:22.708 UTC [endorser] callChaincode -> INFO 089 [mychannel][dc492428] Exit chaincode: name:"mycc"  (1ms)
peer0.org1.example.com    | 2019-10-22 15:45:22.709 UTC [comm.grpc.server] 1 -> INFO 08a unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:49660 grpc.code=OK grpc.call_duration=2.432694ms
peer0.org1.example.com    | 2019-10-22 15:45:29.319 UTC [endorser] callChaincode -> INFO 08b [mychannel][a923f48c] Entry chaincode: name:"mycc"
peer0.org1.example.com    | 2019-10-22 15:45:29.322 UTC [endorser] callChaincode -> INFO 08c [mychannel][a923f48c] Exit chaincode: name:"mycc"  (2ms)
peer0.org1.example.com    | 2019-10-22 15:45:29.324 UTC [comm.grpc.server] 1 -> INFO 08d unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:49664 grpc.code=OK grpc.call_duration=4.867596ms
```

> Invoke ChainCode

```
peer0.org1.example.com    | 2019-10-22 15:44:57.927 UTC [endorser] callChaincode -> INFO 07f [mychannel][dfa2ce3d] Entry chaincode: name:"mycc"
peer0.org1.example.com    | 2019-10-22 15:44:57.929 UTC [endorser] callChaincode -> INFO 080 [mychannel][dfa2ce3d] Exit chaincode: name:"mycc"  (1ms)
peer0.org1.example.com    | 2019-10-22 15:44:57.929 UTC [comm.grpc.server] 1 -> INFO 081 unary call completed grpc.service=protos.Endorser grpc.method=ProcessProposal grpc.peer_address=172.19.0.7:49650 grpc.code=OK grpc.call_duration=3.223803ms
orderer.example.com       | 2019-10-22 15:44:57.934 UTC [orderer.common.broadcast] Handle -> WARN 01a Error reading from 172.19.0.7:38396: rpc error: code = Canceled desc = context canceled
orderer.example.com       | 2019-10-22 15:44:57.935 UTC [comm.grpc.server] 1 -> INFO 01b streaming call completed grpc.service=orderer.AtomicBroadcast grpc.method=Broadcast grpc.peer_address=172.19.0.7:38396 error="rpc error: code = Canceled desc = context canceled" grpc.code=Canceled grpc.call_duration=3.087267ms
peer0.org2.example.com    | 2019-10-22 15:44:59.935 UTC [gossip.privdata] StoreBlock -> INFO 05e [mychannel] Received block [5] from buffer
peer0.org2.example.com    | 2019-10-22 15:44:59.936 UTC [committer.txvalidator] Validate -> INFO 05f [mychannel] Validated block [5] in 0ms
peer0.org1.example.com    | 2019-10-22 15:44:59.938 UTC [gossip.privdata] StoreBlock -> INFO 082 [mychannel] Received block [5] from buffer
peer0.org1.example.com    | 2019-10-22 15:44:59.946 UTC [committer.txvalidator] Validate -> INFO 083 [mychannel] Validated block [5] in 3ms
peer1.org1.example.com    | 2019-10-22 15:44:59.948 UTC [gossip.privdata] StoreBlock -> INFO 060 [mychannel] Received block [5] from buffer
peer1.org1.example.com    | 2019-10-22 15:44:59.950 UTC [committer.txvalidator] Validate -> INFO 061 [mychannel] Validated block [5] in 0ms
peer1.org2.example.com    | 2019-10-22 15:44:59.953 UTC [gossip.privdata] StoreBlock -> INFO 064 [mychannel] Received block [5] from buffer
peer1.org2.example.com    | 2019-10-22 15:44:59.954 UTC [committer.txvalidator] Validate -> INFO 065 [mychannel] Validated block [5] in 0ms
peer1.org1.example.com    | 2019-10-22 15:44:59.956 UTC [kvledger] CommitWithPvtData -> INFO 062 [mychannel] Committed block [5] with 1 transaction(s) in 5ms (state_validation=0ms block_and_pvtdata_commit=1ms state_commit=2ms) commitHash=[d017e82a3361d77db00e2c933d0c4c59dd5f12d2ccd61e2c4dc8d14057a8a47f]
peer1.org2.example.com    | 2019-10-22 15:44:59.959 UTC [kvledger] CommitWithPvtData -> INFO 066 [mychannel] Committed block [5] with 1 transaction(s) in 4ms (state_validation=0ms block_and_pvtdata_commit=3ms state_commit=0ms) commitHash=[d017e82a3361d77db00e2c933d0c4c59dd5f12d2ccd61e2c4dc8d14057a8a47f]
peer0.org2.example.com    | 2019-10-22 15:44:59.964 UTC [kvledger] CommitWithPvtData -> INFO 060 [mychannel] Committed block [5] with 1 transaction(s) in 21ms (state_validation=14ms block_and_pvtdata_commit=4ms state_commit=0ms) commitHash=[d017e82a3361d77db00e2c933d0c4c59dd5f12d2ccd61e2c4dc8d14057a8a47f]
peer0.org1.example.com    | 2019-10-22 15:44:59.965 UTC [kvledger] CommitWithPvtData -> INFO 084 [mychannel] Committed block [5] with 1 transaction(s) in 12ms (state_validation=8ms block_and_pvtdata_commit=2ms state_commit=0ms) commitHash=[d017e82a3361d77db00e2c933d0c4c59dd5f12d2ccd61e2c4dc8d14057a8a47f]

```
