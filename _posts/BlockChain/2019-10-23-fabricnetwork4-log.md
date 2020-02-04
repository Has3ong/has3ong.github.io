---
title : Hyperledger Network 로그
---

> Orderer.example.com

```
2019-10-22 20:22:07.157 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 20:22:07.166 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
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
	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
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
	Kafka.Retry.ShortInterval = 5s
	Kafka.Retry.ShortTotal = 10m0s
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
	Kafka.Topic.ReplicationFactor = 1
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
2019-10-22 20:22:07.178 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 20:22:07.182 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 20:22:07.182 UTC [orderer.common.server] configureClusterListener -> INFO 005 Cluster listener is not configured, defaulting to use the general listener on port 7050
2019-10-22 20:22:07.182 UTC [fsblkstorage] newBlockfileMgr -> INFO 006 Getting block information from block storage
2019-10-22 20:22:07.190 UTC [orderer.consensus.etcdraft] HandleChain -> INFO 007 EvictionSuspicion not set, defaulting to 10m0s
2019-10-22 20:22:07.190 UTC [orderer.consensus.etcdraft] createOrReadWAL -> INFO 008 No WAL data found, creating new WAL at path '/var/hyperledger/production/orderer/etcdraft/wal/byfn-sys-channel' channel=byfn-sys-channel node=1
2019-10-22 20:22:07.193 UTC [orderer.commmon.multichannel] Initialize -> INFO 009 Starting system channel 'byfn-sys-channel' with genesis block hash 78fdd926e8d7ca4e6c501522b50ec1a539ed01afe88f3cfd20b7f0c169e5b6fc and orderer type etcdraft
2019-10-22 20:22:07.194 UTC [orderer.consensus.etcdraft] Start -> INFO 00a Starting Raft node channel=byfn-sys-channel node=1
2019-10-22 20:22:07.194 UTC [orderer.common.cluster] Configure -> INFO 00b Entering, channel: byfn-sys-channel, nodes: [ID: 4,
Endpoint: orderer4.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
 ID: 5,
Endpoint: orderer5.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
 ID: 2,
Endpoint: orderer2.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
 ID: 3,
Endpoint: orderer3.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
]
2019-10-22 20:22:07.195 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00c Allocating a new stub for node 4 with endpoint of orderer4.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:07.195 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00d Deactivating node 4 in channel byfn-sys-channel with endpoint of orderer4.example.com:7050 due to TLS certificate change
2019-10-22 20:22:07.195 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00e Allocating a new stub for node 5 with endpoint of orderer5.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:07.195 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00f Deactivating node 5 in channel byfn-sys-channel with endpoint of orderer5.example.com:7050 due to TLS certificate change
2019-10-22 20:22:07.196 UTC [orderer.common.cluster] updateStubInMapping -> INFO 010 Allocating a new stub for node 2 with endpoint of orderer2.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:07.196 UTC [orderer.common.cluster] updateStubInMapping -> INFO 011 Deactivating node 2 in channel byfn-sys-channel with endpoint of orderer2.example.com:7050 due to TLS certificate change
2019-10-22 20:22:07.196 UTC [orderer.common.cluster] updateStubInMapping -> INFO 012 Allocating a new stub for node 3 with endpoint of orderer3.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:07.196 UTC [orderer.common.cluster] updateStubInMapping -> INFO 013 Deactivating node 3 in channel byfn-sys-channel with endpoint of orderer3.example.com:7050 due to TLS certificate change
2019-10-22 20:22:07.197 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 014 3 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:07.197 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 015 4 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:07.197 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 016 5 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:07.197 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 017 2 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:07.197 UTC [orderer.common.cluster] Configure -> INFO 018 Exiting
2019-10-22 20:22:07.197 UTC [orderer.consensus.etcdraft] start -> INFO 019 Starting raft node as part of a new channel channel=byfn-sys-channel node=1
2019-10-22 20:22:07.197 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01a 1 became follower at term 0 channel=byfn-sys-channel node=1
2019-10-22 20:22:07.197 UTC [orderer.consensus.etcdraft] newRaft -> INFO 01b newRaft 1 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0] channel=byfn-sys-channel node=1
2019-10-22 20:22:07.198 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01c 1 became follower at term 1 channel=byfn-sys-channel node=1
2019-10-22 20:22:07.198 UTC [orderer.common.server] Start -> INFO 01d Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 20:22:07.198 UTC [orderer.common.server] Start -> INFO 01e Beginning to serve requests
2019-10-22 20:22:07.199 UTC [orderer.consensus.etcdraft] apply -> INFO 01f Applied config change to add node 1, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=1
2019-10-22 20:22:07.199 UTC [orderer.consensus.etcdraft] apply -> INFO 020 Applied config change to add node 2, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=1
2019-10-22 20:22:07.200 UTC [orderer.consensus.etcdraft] apply -> INFO 021 Applied config change to add node 3, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=1
2019-10-22 20:22:07.200 UTC [orderer.consensus.etcdraft] apply -> INFO 022 Applied config change to add node 4, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=1
2019-10-22 20:22:07.200 UTC [orderer.consensus.etcdraft] apply -> INFO 023 Applied config change to add node 5, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=1
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] Step -> INFO 024 1 [term: 1] received a MsgHeartbeat message with higher term from 5 [term: 2] channel=byfn-sys-channel node=1
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 025 1 became follower at term 2 channel=byfn-sys-channel node=1
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] run -> INFO 026 raft.node: 1 elected leader 5 at term 2 channel=byfn-sys-channel node=1
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 027 Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=1
```

> Orderer2.example.com

```
2019-10-22 20:22:06.888 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 20:22:06.904 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
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
	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
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
	Kafka.Retry.ShortInterval = 5s
	Kafka.Retry.ShortTotal = 10m0s
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
	Kafka.Topic.ReplicationFactor = 1
	Debug.BroadcastTraceDir = ""
	Debug.DeliverTraceDir = ""
	Consensus = map[SnapDir:/var/hyperledger/production/orderer/etcdraft/snapshot WALDir:/var/hyperledger/production/orderer/etcdraft/wal]
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
2019-10-22 20:22:06.944 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 20:22:06.955 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 20:22:06.955 UTC [orderer.common.server] configureClusterListener -> INFO 005 Cluster listener is not configured, defaulting to use the general listener on port 7050
2019-10-22 20:22:06.956 UTC [fsblkstorage] newBlockfileMgr -> INFO 006 Getting block information from block storage
2019-10-22 20:22:06.981 UTC [orderer.consensus.etcdraft] HandleChain -> INFO 007 EvictionSuspicion not set, defaulting to 10m0s
2019-10-22 20:22:06.982 UTC [orderer.consensus.etcdraft] createOrReadWAL -> INFO 008 No WAL data found, creating new WAL at path '/var/hyperledger/production/orderer/etcdraft/wal/byfn-sys-channel' channel=byfn-sys-channel node=2
2019-10-22 20:22:06.984 UTC [orderer.commmon.multichannel] Initialize -> INFO 009 Starting system channel 'byfn-sys-channel' with genesis block hash 78fdd926e8d7ca4e6c501522b50ec1a539ed01afe88f3cfd20b7f0c169e5b6fc and orderer type etcdraft
2019-10-22 20:22:06.984 UTC [orderer.consensus.etcdraft] Start -> INFO 00a Starting Raft node channel=byfn-sys-channel node=2
2019-10-22 20:22:06.984 UTC [orderer.common.cluster] Configure -> INFO 00b Entering, channel: byfn-sys-channel, nodes: [ID: 3,
Endpoint: orderer3.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
 ID: 4,
Endpoint: orderer4.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
 ID: 5,
Endpoint: orderer5.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
 ID: 1,
Endpoint: orderer.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
]
2019-10-22 20:22:06.984 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00c Allocating a new stub for node 3 with endpoint of orderer3.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.984 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00d Deactivating node 3 in channel byfn-sys-channel with endpoint of orderer3.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.985 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00e Allocating a new stub for node 4 with endpoint of orderer4.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.985 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00f Deactivating node 4 in channel byfn-sys-channel with endpoint of orderer4.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.986 UTC [orderer.common.cluster] updateStubInMapping -> INFO 010 Allocating a new stub for node 5 with endpoint of orderer5.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.986 UTC [orderer.common.cluster] updateStubInMapping -> INFO 011 Deactivating node 5 in channel byfn-sys-channel with endpoint of orderer5.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.987 UTC [orderer.common.cluster] updateStubInMapping -> INFO 012 Allocating a new stub for node 1 with endpoint of orderer.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.987 UTC [orderer.common.cluster] updateStubInMapping -> INFO 013 Deactivating node 1 in channel byfn-sys-channel with endpoint of orderer.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.988 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 014 3 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.988 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 015 4 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.988 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 016 5 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.988 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 017 1 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.988 UTC [orderer.common.cluster] Configure -> INFO 018 Exiting
2019-10-22 20:22:06.988 UTC [orderer.consensus.etcdraft] start -> INFO 019 Starting raft node as part of a new channel channel=byfn-sys-channel node=2
2019-10-22 20:22:06.988 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01a 2 became follower at term 0 channel=byfn-sys-channel node=2
2019-10-22 20:22:06.988 UTC [orderer.consensus.etcdraft] newRaft -> INFO 01b newRaft 2 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0] channel=byfn-sys-channel node=2
2019-10-22 20:22:06.988 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01c 2 became follower at term 1 channel=byfn-sys-channel node=2
2019-10-22 20:22:06.988 UTC [orderer.common.server] Start -> INFO 01d Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 20:22:06.988 UTC [orderer.common.server] Start -> INFO 01e Beginning to serve requests
2019-10-22 20:22:06.990 UTC [orderer.consensus.etcdraft] apply -> INFO 01f Applied config change to add node 1, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=2
2019-10-22 20:22:06.990 UTC [orderer.consensus.etcdraft] apply -> INFO 020 Applied config change to add node 2, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=2
2019-10-22 20:22:06.990 UTC [orderer.consensus.etcdraft] apply -> INFO 021 Applied config change to add node 3, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=2
2019-10-22 20:22:06.990 UTC [orderer.consensus.etcdraft] apply -> INFO 022 Applied config change to add node 4, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=2
2019-10-22 20:22:06.990 UTC [orderer.consensus.etcdraft] apply -> INFO 023 Applied config change to add node 5, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=2
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] Step -> INFO 024 2 [term: 1] received a MsgHeartbeat message with higher term from 5 [term: 2] channel=byfn-sys-channel node=2
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 025 2 became follower at term 2 channel=byfn-sys-channel node=2
2019-10-22 20:22:08.906 UTC [orderer.consensus.etcdraft] run -> INFO 026 raft.node: 2 elected leader 5 at term 2 channel=byfn-sys-channel node=2
2019-10-22 20:22:08.907 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 027 Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=2
```

> Orderer3.example.com

```
2019-10-22 20:22:06.869 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 20:22:06.883 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
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
	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
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
	Kafka.Retry.ShortInterval = 5s
	Kafka.Retry.ShortTotal = 10m0s
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
	Kafka.Topic.ReplicationFactor = 1
	Debug.BroadcastTraceDir = ""
	Debug.DeliverTraceDir = ""
	Consensus = map[SnapDir:/var/hyperledger/production/orderer/etcdraft/snapshot WALDir:/var/hyperledger/production/orderer/etcdraft/wal]
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
2019-10-22 20:22:06.895 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 20:22:06.900 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 20:22:06.901 UTC [orderer.common.server] configureClusterListener -> INFO 005 Cluster listener is not configured, defaulting to use the general listener on port 7050
2019-10-22 20:22:06.901 UTC [fsblkstorage] newBlockfileMgr -> INFO 006 Getting block information from block storage
2019-10-22 20:22:06.915 UTC [orderer.consensus.etcdraft] HandleChain -> INFO 007 EvictionSuspicion not set, defaulting to 10m0s
2019-10-22 20:22:06.916 UTC [orderer.consensus.etcdraft] createOrReadWAL -> INFO 008 No WAL data found, creating new WAL at path '/var/hyperledger/production/orderer/etcdraft/wal/byfn-sys-channel' channel=byfn-sys-channel node=3
2019-10-22 20:22:06.918 UTC [orderer.commmon.multichannel] Initialize -> INFO 009 Starting system channel 'byfn-sys-channel' with genesis block hash 78fdd926e8d7ca4e6c501522b50ec1a539ed01afe88f3cfd20b7f0c169e5b6fc and orderer type etcdraft
2019-10-22 20:22:06.919 UTC [orderer.consensus.etcdraft] Start -> INFO 00a Starting Raft node channel=byfn-sys-channel node=3
2019-10-22 20:22:06.919 UTC [orderer.common.cluster] Configure -> INFO 00b Entering, channel: byfn-sys-channel, nodes: [ID: 2,
Endpoint: orderer2.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
 ID: 4,
Endpoint: orderer4.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
 ID: 5,
Endpoint: orderer5.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
 ID: 1,
Endpoint: orderer.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
]
2019-10-22 20:22:06.919 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00c Allocating a new stub for node 2 with endpoint of orderer2.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.919 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00d Deactivating node 2 in channel byfn-sys-channel with endpoint of orderer2.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.919 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00e Allocating a new stub for node 4 with endpoint of orderer4.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.920 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00f Deactivating node 4 in channel byfn-sys-channel with endpoint of orderer4.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.921 UTC [orderer.common.cluster] updateStubInMapping -> INFO 010 Allocating a new stub for node 5 with endpoint of orderer5.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.921 UTC [orderer.common.cluster] updateStubInMapping -> INFO 011 Deactivating node 5 in channel byfn-sys-channel with endpoint of orderer5.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.922 UTC [orderer.common.cluster] updateStubInMapping -> INFO 012 Allocating a new stub for node 1 with endpoint of orderer.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.930 UTC [orderer.common.cluster] updateStubInMapping -> INFO 013 Deactivating node 1 in channel byfn-sys-channel with endpoint of orderer.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.931 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 014 5 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.932 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 015 1 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.932 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 016 2 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.932 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 017 4 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.932 UTC [orderer.common.cluster] Configure -> INFO 018 Exiting
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] start -> INFO 019 Starting raft node as part of a new channel channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01a 3 became follower at term 0 channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] newRaft -> INFO 01b newRaft 3 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0] channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01c 3 became follower at term 1 channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.common.server] Start -> INFO 01d Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 20:22:06.933 UTC [orderer.common.server] Start -> INFO 01e Beginning to serve requests
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] apply -> INFO 01f Applied config change to add node 1, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] apply -> INFO 020 Applied config change to add node 2, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=3
2019-10-22 20:22:06.933 UTC [orderer.consensus.etcdraft] apply -> INFO 021 Applied config change to add node 3, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=3
2019-10-22 20:22:06.934 UTC [orderer.consensus.etcdraft] apply -> INFO 022 Applied config change to add node 4, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=3
2019-10-22 20:22:06.934 UTC [orderer.consensus.etcdraft] apply -> INFO 023 Applied config change to add node 5, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=3
2019-10-22 20:22:07.909 UTC [orderer.consensus.etcdraft] Step -> INFO 024 3 [logterm: 1, index: 5, vote: 0] cast MsgPreVote for 5 [logterm: 1, index: 5] at term 1 channel=byfn-sys-channel node=3
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] Step -> INFO 025 3 [term: 1] received a MsgVote message with higher term from 5 [term: 2] channel=byfn-sys-channel node=3
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 026 3 became follower at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] Step -> INFO 027 3 [logterm: 1, index: 5, vote: 0] cast MsgVote for 5 [logterm: 1, index: 5] at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:22:07.913 UTC [orderer.consensus.etcdraft] run -> INFO 028 raft.node: 3 elected leader 5 at term 2 channel=byfn-sys-channel node=3
2019-10-22 20:22:07.913 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 029 Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=3
```

> Orderer4.example.com

```
2019-10-22 20:22:06.241 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 20:22:06.252 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
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
	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
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
	Kafka.Retry.ShortInterval = 5s
	Kafka.Retry.ShortTotal = 10m0s
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
	Kafka.Topic.ReplicationFactor = 1
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
2019-10-22 20:22:06.279 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 20:22:06.292 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 20:22:06.297 UTC [orderer.common.server] configureClusterListener -> INFO 005 Cluster listener is not configured, defaulting to use the general listener on port 7050
2019-10-22 20:22:06.298 UTC [fsblkstorage] newBlockfileMgr -> INFO 006 Getting block information from block storage
2019-10-22 20:22:06.317 UTC [orderer.consensus.etcdraft] HandleChain -> INFO 007 EvictionSuspicion not set, defaulting to 10m0s
2019-10-22 20:22:06.321 UTC [orderer.consensus.etcdraft] createOrReadWAL -> INFO 008 No WAL data found, creating new WAL at path '/var/hyperledger/production/orderer/etcdraft/wal/byfn-sys-channel' channel=byfn-sys-channel node=4
2019-10-22 20:22:06.329 UTC [orderer.commmon.multichannel] Initialize -> INFO 009 Starting system channel 'byfn-sys-channel' with genesis block hash 78fdd926e8d7ca4e6c501522b50ec1a539ed01afe88f3cfd20b7f0c169e5b6fc and orderer type etcdraft
2019-10-22 20:22:06.330 UTC [orderer.consensus.etcdraft] Start -> INFO 00a Starting Raft node channel=byfn-sys-channel node=4
2019-10-22 20:22:06.330 UTC [orderer.common.cluster] Configure -> INFO 00b Entering, channel: byfn-sys-channel, nodes: [ID: 1,
Endpoint: orderer.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
 ID: 2,
Endpoint: orderer2.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
 ID: 3,
Endpoint: orderer3.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
 ID: 5,
Endpoint: orderer5.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXDCCAgOgAwIBAgIRANXC+misF+P17YHZhoeSfDEwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNS5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABNyt1YhxMDWjNCjSSekkTmP9LWyVolPeVN7ZC+7dn6CM
XPS6dfzRI9qqMG0yGVRKQ2HUonTnMLBeIvnRSvj3nXSjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI1LmV4YW1wbGUuY29tgghvcmRlcmVyNTAKBggq
hkjOPQQDAgNHADBEAiA/oOEYu29nQWyy2a+zv7PTs2xFLzvql47lqdHbuAU7NAIg
R+9YkMuJiAMLMu9NuzKkBPuY4UyFTnM6IY5Wk3BBv78=
-----END CERTIFICATE-----
]
2019-10-22 20:22:06.330 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00c Allocating a new stub for node 1 with endpoint of orderer.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.330 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00d Deactivating node 1 in channel byfn-sys-channel with endpoint of orderer.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.331 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00e Allocating a new stub for node 2 with endpoint of orderer2.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.332 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00f Deactivating node 2 in channel byfn-sys-channel with endpoint of orderer2.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.332 UTC [orderer.common.cluster] updateStubInMapping -> INFO 010 Allocating a new stub for node 3 with endpoint of orderer3.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.332 UTC [orderer.common.cluster] updateStubInMapping -> INFO 011 Deactivating node 3 in channel byfn-sys-channel with endpoint of orderer3.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.335 UTC [orderer.common.cluster] updateStubInMapping -> INFO 012 Allocating a new stub for node 5 with endpoint of orderer5.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:06.335 UTC [orderer.common.cluster] updateStubInMapping -> INFO 013 Deactivating node 5 in channel byfn-sys-channel with endpoint of orderer5.example.com:7050 due to TLS certificate change
2019-10-22 20:22:06.337 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 014 1 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.337 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 015 2 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.337 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 016 3 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.337 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 017 5 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:06.337 UTC [orderer.common.cluster] Configure -> INFO 018 Exiting
2019-10-22 20:22:06.337 UTC [orderer.consensus.etcdraft] start -> INFO 019 Starting raft node as part of a new channel channel=byfn-sys-channel node=4
2019-10-22 20:22:06.337 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01a 4 became follower at term 0 channel=byfn-sys-channel node=4
2019-10-22 20:22:06.337 UTC [orderer.consensus.etcdraft] newRaft -> INFO 01b newRaft 4 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.337 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01c 4 became follower at term 1 channel=byfn-sys-channel node=4
2019-10-22 20:22:06.338 UTC [orderer.common.server] Start -> INFO 01d Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 20:22:06.338 UTC [orderer.common.server] Start -> INFO 01e Beginning to serve requests
2019-10-22 20:22:06.339 UTC [orderer.consensus.etcdraft] apply -> INFO 01f Applied config change to add node 1, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.339 UTC [orderer.consensus.etcdraft] apply -> INFO 020 Applied config change to add node 2, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.339 UTC [orderer.consensus.etcdraft] apply -> INFO 021 Applied config change to add node 3, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.339 UTC [orderer.consensus.etcdraft] apply -> INFO 022 Applied config change to add node 4, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.339 UTC [orderer.consensus.etcdraft] apply -> INFO 023 Applied config change to add node 5, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=4
2019-10-22 20:22:06.909 UTC [orderer.consensus.etcdraft] Step -> INFO 024 4 [logterm: 1, index: 5, vote: 0] cast MsgPreVote for 5 [logterm: 1, index: 5] at term 1 channel=byfn-sys-channel node=4
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] Step -> INFO 025 4 [logterm: 1, index: 5, vote: 0] cast MsgPreVote for 5 [logterm: 1, index: 5] at term 1 channel=byfn-sys-channel node=4
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] Step -> INFO 026 4 [term: 1] received a MsgVote message with higher term from 5 [term: 2] channel=byfn-sys-channel node=4
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 027 4 became follower at term 2 channel=byfn-sys-channel node=4
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] Step -> INFO 028 4 [logterm: 1, index: 5, vote: 0] cast MsgVote for 5 [logterm: 1, index: 5] at term 2 channel=byfn-sys-channel node=4
2019-10-22 20:22:07.913 UTC [orderer.consensus.etcdraft] run -> INFO 029 raft.node: 4 elected leader 5 at term 2 channel=byfn-sys-channel node=4
2019-10-22 20:22:07.913 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 02a Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=4
```

> Orderer5.example.com

```
2019-10-22 20:22:05.817 UTC [localconfig] completeInitialization -> INFO 001 Kafka.Version unset, setting to 0.10.2.0
2019-10-22 20:22:05.835 UTC [orderer.common.server] prettyPrintStruct -> INFO 002 Orderer config values:
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
	General.Cluster.ClientCertificate = "/var/hyperledger/orderer/tls/server.crt"
	General.Cluster.ClientPrivateKey = "/var/hyperledger/orderer/tls/server.key"
	General.Cluster.RootCAs = [/var/hyperledger/orderer/tls/ca.crt]
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
	Kafka.Retry.ShortInterval = 5s
	Kafka.Retry.ShortTotal = 10m0s
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
	Kafka.Topic.ReplicationFactor = 1
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
2019-10-22 20:22:05.864 UTC [orderer.common.server] extractSysChanLastConfig -> INFO 003 Bootstrapping because no existing channels
2019-10-22 20:22:05.871 UTC [orderer.common.server] initializeServerConfig -> INFO 004 Starting orderer with TLS enabled
2019-10-22 20:22:05.871 UTC [orderer.common.server] configureClusterListener -> INFO 005 Cluster listener is not configured, defaulting to use the general listener on port 7050
2019-10-22 20:22:05.871 UTC [fsblkstorage] newBlockfileMgr -> INFO 006 Getting block information from block storage
2019-10-22 20:22:05.894 UTC [orderer.consensus.etcdraft] HandleChain -> INFO 007 EvictionSuspicion not set, defaulting to 10m0s
2019-10-22 20:22:05.895 UTC [orderer.consensus.etcdraft] createOrReadWAL -> INFO 008 No WAL data found, creating new WAL at path '/var/hyperledger/production/orderer/etcdraft/wal/byfn-sys-channel' channel=byfn-sys-channel node=5
2019-10-22 20:22:05.901 UTC [orderer.commmon.multichannel] Initialize -> INFO 009 Starting system channel 'byfn-sys-channel' with genesis block hash 78fdd926e8d7ca4e6c501522b50ec1a539ed01afe88f3cfd20b7f0c169e5b6fc and orderer type etcdraft
2019-10-22 20:22:05.901 UTC [orderer.consensus.etcdraft] Start -> INFO 00a Starting Raft node channel=byfn-sys-channel node=5
2019-10-22 20:22:05.901 UTC [orderer.common.cluster] Configure -> INFO 00b Entering, channel: byfn-sys-channel, nodes: [ID: 1,
Endpoint: orderer.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICWTCCAgCgAwIBAgIRAKhupN6eLQveN4SuUuyeAlowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFgxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMRwwGgYDVQQDExNvcmRlcmVyLmV4YW1wbGUuY29tMFkwEwYHKoZIzj0C
AQYIKoZIzj0DAQcDQgAEI6sHBpEsf9hgwupeiykVXZ2Ozz/1L/sL1EYt0DWsYY19
YMHFZOJULed2X1ecwHstWQOvDpyMHGzFYV7m/TXeMqOBljCBkzAOBgNVHQ8BAf8E
BAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQC
MAAwKwYDVR0jBCQwIoAg7cO7SusG3wVllPTibPxNorFrp9aScsqLoa/mOUw24a4w
JwYDVR0RBCAwHoITb3JkZXJlci5leGFtcGxlLmNvbYIHb3JkZXJlcjAKBggqhkjO
PQQDAgNHADBEAiAfyPMzr62Ct5Ee8vQD7K+w2w5tJnBLA6PRzu07w4W5XQIgJGB8
phcY72zowReO9/hx8arUH0yO2CebXV7+/nR/cfw=
-----END CERTIFICATE-----
 ID: 2,
Endpoint: orderer2.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAMWtPo9AUl6royp6+m0CyRswCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMi5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABBB8p+M0CEWN1cDFny0Vydps+kki1A5ycFtqvvTkIbhZ
RDU1lJ1ly+YWY4+C2TFlp7otplNYsEDo55QmAZie7u6jgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIyLmV4YW1wbGUuY29tgghvcmRlcmVyMjAKBggq
hkjOPQQDAgNIADBFAiEAxkFURVcngN5RCU364QJvF/nb+wHbuGmaHMpWalf9I8oC
IHRLJGBhqVK8l/kAqiwlWSwlCs9gNlAIffrBWc4G8NKi
-----END CERTIFICATE-----
 ID: 3,
Endpoint: orderer3.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAKcgGM0fUASULJqyxKff4FcwCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyMy5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABJ3UA6Zu5kohC4y6OZmCDpZQfkUqFOeh0HGU777WX/nF
zAh9By2NIgINXqXLxBqM8qyMrf23rkYsINYj6ImFoWCjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXIzLmV4YW1wbGUuY29tgghvcmRlcmVyMzAKBggq
hkjOPQQDAgNIADBFAiEAo+a4KW6Agm15QeRrdOt31gJU1bWcxTEGgWIZ+5oT4ysC
IGLf8d8j3v2yIPSMhCQSavipR14b/pDIX5lXwKsvSfNK
-----END CERTIFICATE-----
 ID: 4,
Endpoint: orderer4.example.com:7050,
ServerTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
, ClientTLSCert:-----BEGIN CERTIFICATE-----
MIICXTCCAgOgAwIBAgIRAJy16h/9whBpBl7ssDM3PsowCgYIKoZIzj0EAwIwbDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFjAUBgNVBAcTDVNhbiBG
cmFuY2lzY28xFDASBgNVBAoTC2V4YW1wbGUuY29tMRowGAYDVQQDExF0bHNjYS5l
eGFtcGxlLmNvbTAeFw0xOTEwMjIyMDE0MDBaFw0yOTEwMTkyMDE0MDBaMFkxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1TYW4gRnJh
bmNpc2NvMR0wGwYDVQQDExRvcmRlcmVyNC5leGFtcGxlLmNvbTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABP3MSvXQkawizLGbFsF0L2k09GieFJpqQ0jYJEHn+O/z
lmC2ocXr9/56hvWUoRg4JEdl/WnvB/ZV7o4VIMklN4yjgZgwgZUwDgYDVR0PAQH/
BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8E
AjAAMCsGA1UdIwQkMCKAIO3Du0rrBt8FZZT04mz8TaKxa6fWknLKi6Gv5jlMNuGu
MCkGA1UdEQQiMCCCFG9yZGVyZXI0LmV4YW1wbGUuY29tgghvcmRlcmVyNDAKBggq
hkjOPQQDAgNIADBFAiEAw4dHB+vNLZ5GC2MKHCbHOsjR1yipB5ZTuNqmAnerRScC
IHhddVHghRPUBiWJwfxYAP/E5OUttkCwglyZclWIWDuv
-----END CERTIFICATE-----
]
2019-10-22 20:22:05.901 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00c Allocating a new stub for node 1 with endpoint of orderer.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:05.901 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00d Deactivating node 1 in channel byfn-sys-channel with endpoint of orderer.example.com:7050 due to TLS certificate change
2019-10-22 20:22:05.902 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00e Allocating a new stub for node 2 with endpoint of orderer2.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:05.902 UTC [orderer.common.cluster] updateStubInMapping -> INFO 00f Deactivating node 2 in channel byfn-sys-channel with endpoint of orderer2.example.com:7050 due to TLS certificate change
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] updateStubInMapping -> INFO 010 Allocating a new stub for node 3 with endpoint of orderer3.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] updateStubInMapping -> INFO 011 Deactivating node 3 in channel byfn-sys-channel with endpoint of orderer3.example.com:7050 due to TLS certificate change
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] updateStubInMapping -> INFO 012 Allocating a new stub for node 4 with endpoint of orderer4.example.com:7050 for channel byfn-sys-channel
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] updateStubInMapping -> INFO 013 Deactivating node 4 in channel byfn-sys-channel with endpoint of orderer4.example.com:7050 due to TLS certificate change
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 014 4 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 015 1 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 016 2 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] applyMembershipConfig -> INFO 017 3 exists in both old and new membership for channel byfn-sys-channel , skipping its deactivation
2019-10-22 20:22:05.903 UTC [orderer.common.cluster] Configure -> INFO 018 Exiting
2019-10-22 20:22:05.903 UTC [orderer.consensus.etcdraft] start -> INFO 019 Starting raft node as part of a new channel channel=byfn-sys-channel node=5
2019-10-22 20:22:05.903 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01a 5 became follower at term 0 channel=byfn-sys-channel node=5
2019-10-22 20:22:05.904 UTC [orderer.consensus.etcdraft] newRaft -> INFO 01b newRaft 5 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0] channel=byfn-sys-channel node=5
2019-10-22 20:22:05.904 UTC [orderer.consensus.etcdraft] becomeFollower -> INFO 01c 5 became follower at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:05.904 UTC [orderer.common.server] Start -> INFO 01d Starting orderer:
 Version: 1.4.3
 Commit SHA: b8c4a6a
 Go version: go1.11.5
 OS/Arch: linux/amd64
2019-10-22 20:22:05.904 UTC [orderer.common.server] Start -> INFO 01e Beginning to serve requests
2019-10-22 20:22:05.905 UTC [orderer.consensus.etcdraft] run -> INFO 01f This node is picked to start campaign channel=byfn-sys-channel node=5
2019-10-22 20:22:05.907 UTC [orderer.consensus.etcdraft] apply -> INFO 020 Applied config change to add node 1, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=5
2019-10-22 20:22:05.907 UTC [orderer.consensus.etcdraft] apply -> INFO 021 Applied config change to add node 2, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=5
2019-10-22 20:22:05.907 UTC [orderer.consensus.etcdraft] apply -> INFO 022 Applied config change to add node 3, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=5
2019-10-22 20:22:05.907 UTC [orderer.consensus.etcdraft] apply -> INFO 023 Applied config change to add node 4, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=5
2019-10-22 20:22:05.907 UTC [orderer.consensus.etcdraft] apply -> INFO 024 Applied config change to add node 5, current nodes in channel: [1 2 3 4 5] channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] Step -> INFO 025 5 is starting a new election at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] becomePreCandidate -> INFO 026 5 became pre-candidate at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] poll -> INFO 027 5 received MsgPreVoteResp from 5 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] campaign -> INFO 028 5 [logterm: 1, index: 5] sent MsgPreVote request to 1 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] campaign -> INFO 029 5 [logterm: 1, index: 5] sent MsgPreVote request to 2 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] campaign -> INFO 02a 5 [logterm: 1, index: 5] sent MsgPreVote request to 3 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.906 UTC [orderer.consensus.etcdraft] campaign -> INFO 02b 5 [logterm: 1, index: 5] sent MsgPreVote request to 4 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.907 UTC [orderer.consensus.etcdraft] logSendFailure -> ERRO 02c Failed to send StepRequest to 1, because: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.19.0.3:7050: connect: connection refused" channel=byfn-sys-channel node=5
2019-10-22 20:22:06.907 UTC [orderer.consensus.etcdraft] logSendFailure -> ERRO 02d Failed to send StepRequest to 2, because: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.19.0.10:7050: connect: connection refused" channel=byfn-sys-channel node=5
2019-10-22 20:22:06.907 UTC [orderer.consensus.etcdraft] logSendFailure -> ERRO 02e Failed to send StepRequest to 3, because: connection to 3(orderer3.example.com:7050) is in state CONNECTING channel=byfn-sys-channel node=5
2019-10-22 20:22:06.909 UTC [orderer.consensus.etcdraft] poll -> INFO 02f 5 received MsgPreVoteResp from 4 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:06.909 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 030 5 [quorum:3] has received 2 MsgPreVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=5
2019-10-22 20:22:07.906 UTC [orderer.consensus.etcdraft] Step -> INFO 031 5 is starting a new election at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.906 UTC [orderer.consensus.etcdraft] becomePreCandidate -> INFO 032 5 became pre-candidate at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.906 UTC [orderer.consensus.etcdraft] poll -> INFO 033 5 received MsgPreVoteResp from 5 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] campaign -> INFO 034 5 [logterm: 1, index: 5] sent MsgPreVote request to 4 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] campaign -> INFO 035 5 [logterm: 1, index: 5] sent MsgPreVote request to 1 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] campaign -> INFO 036 5 [logterm: 1, index: 5] sent MsgPreVote request to 2 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] campaign -> INFO 037 5 [logterm: 1, index: 5] sent MsgPreVote request to 3 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.907 UTC [orderer.consensus.etcdraft] send -> INFO 038 Successfully sent StepRequest to 3 after failed attempt(s) channel=byfn-sys-channel node=5
2019-10-22 20:22:07.908 UTC [orderer.consensus.etcdraft] poll -> INFO 039 5 received MsgPreVoteResp from 4 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.908 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 03a 5 [quorum:3] has received 2 MsgPreVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=5
2019-10-22 20:22:07.909 UTC [orderer.consensus.etcdraft] poll -> INFO 03b 5 received MsgPreVoteResp from 3 at term 1 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.909 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 03c 5 [quorum:3] has received 3 MsgPreVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] becomeCandidate -> INFO 03d 5 became candidate at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] poll -> INFO 03e 5 received MsgVoteResp from 5 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] campaign -> INFO 03f 5 [logterm: 1, index: 5] sent MsgVote request to 2 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] campaign -> INFO 040 5 [logterm: 1, index: 5] sent MsgVote request to 3 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] campaign -> INFO 041 5 [logterm: 1, index: 5] sent MsgVote request to 4 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.910 UTC [orderer.consensus.etcdraft] campaign -> INFO 042 5 [logterm: 1, index: 5] sent MsgVote request to 1 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] poll -> INFO 043 5 received MsgVoteResp from 4 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.911 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 044 5 [quorum:3] has received 2 MsgVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] poll -> INFO 045 5 received MsgVoteResp from 3 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] stepCandidate -> INFO 046 5 [quorum:3] has received 3 MsgVoteResp votes and 0 vote rejections channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] becomeLeader -> INFO 047 5 became leader at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] run -> INFO 048 raft.node: 5 elected leader 5 at term 2 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] run -> INFO 049 Leader 5 is present, quit campaign channel=byfn-sys-channel node=5
2019-10-22 20:22:07.912 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 04a Raft leader changed: 0 -> 5 channel=byfn-sys-channel node=5
2019-10-22 20:22:07.914 UTC [orderer.consensus.etcdraft] serveRequest -> INFO 04b Start accepting requests as Raft leader at block [0] channel=byfn-sys-channel node=5
2019-10-22 20:22:08.905 UTC [orderer.consensus.etcdraft] send -> INFO 04c Successfully sent StepRequest to 1 after failed attempt(s) channel=byfn-sys-channel node=5
2019-10-22 20:22:08.905 UTC [orderer.consensus.etcdraft] send -> INFO 04d Successfully sent StepRequest to 2 after failed attempt(s) channel=byfn-sys-channel node=5
```


