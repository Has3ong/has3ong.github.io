---
title : Gossip Protocol
tags :
- Gossip Protocol
- Hyperledger Fabric
- BlockChain
---

## Gossip Protocol

![image](https://user-images.githubusercontent.com/44635266/67632960-44fed600-f8ed-11e9-9bb0-cfcd76f07fba.png)

하이퍼래저 패브릭에서는 트랜잭션 실행 피어와 트랜잭션 정렬 피어사이에서 업무를 분담해서 CPU부하(고루틴을 통함)  및 네트웍 부하를 처리한다. 이런 분리된 네트워크에서 확장성,보안성등에 대한 처리를 유연하게 하기 위해 패브릭은  가쉽 데이터 전파 프로토콜  을 만들었다. 

각 가십메세지들은 서명되어서 전달되며, 그에 따라 중간에 악의적인 노드의 메세지도 쉽게 확인되며, 가쉽 프로토콜 특성상 늦게 도착하거나, 몇몇 노드들의 네트워크 분단 상황에서도 결국 싱크는 맞춰지게된다.   

패프릭 네트워크에서 가쉽 데이터 전파 프로토콜 의 주요 3가지 기능으로는 다음과 같다.

1. 피어 발견 및 채널 멤버쉽을 관리한다. (이용 가능한 피어들을 계속해서 체크함)
2. 장부에 기록할 데이터들을 모든 채널 상의 피어들에 전파.싱크가 안맞는 피어들을 확인하여 모자란 블럭 정보들을 계속해서 공급해줌. 
3. 새로운 피어가 참여하면 peer to peer 로 장부 데이터들을 업데이트 해줌. 

동일한 채널위의 피어들은 메세지를 계속해서 수신하고,주변 피어에 전파하며, 싱크를 맞추게 된다. 이웃피어의 갯수는 설정으로 정해져 있으며, Pull 메커니즘을 따른다. 따라서 메세지가 올 때 까지 기다리는게 아니라, 적극적으로 가지고 오려는 행동을 한다. 채널 상의 각 조직의 리더 피어는 오더러에게 데이터를 가져(Pull)온 후 자신의 조직에 포함된 피어들에게 전파하기 시작한다.


![image](https://user-images.githubusercontent.com/44635266/67632961-46c89980-f8ed-11e9-9c19-709a2f1c78bc.png)

하이퍼레저 패브릭의 워크플로우를 간단히 설명하면,

1. 클라이언트는 어플리케이션(SDK)를 통해서 Peer 들에게 트랜잭션을 실행 시킨다.
2. Endorsement역할을 하는 이 Peer 들은 체인코드를 실행시키고 장착된 체인코드 로직에 따라서 결과를 내어 다시 클라쪽으로 read/write 셋을 전달 한다.(이 과정에서 장부를 업데이트 하지 않음)
3. 이 결과 셋을 가지고 orderer 서비스에게 순서를 정해서 블록화 해달라고 요청한다.
4. **orerer 서비스는 블록화 한 후에 Peer 들에게 이 블록을 검증하고 저장하여라~~ 하고 보내준다.**

이 과정 중에서 Gossip 프로토콜이 이용되는것이 바로 4번 flow 에서이다. 
즉 orderer 는 모든 peer과 커뮤니케이션을 하는게 아니라, 대표 peer 하나에게 알리면 이 peer 가 gossip 을 통해 점진적으로 전체로 전달되게 되는 것이다. 각 피어는 전달받은 블록(트랜잭션 뭉치들)을 검증하고 장부(상태DB&블록체인) 에 저장한다.

![image](https://user-images.githubusercontent.com/44635266/67632962-47f9c680-f8ed-11e9-9ff7-67e8ead65350.png)

조금 더 구체적인 위의 그림에서는 5번에 해당한다.

조직마다 Leader Peer가 있으며, 이 Leader Peer가 오더러에게서 Pull 하면서 시작된다. 그림에는 구분이 안되어 있지만 추가적으로 하나의 조직이 다른 조직의 Peer 와 연계할 때에  Anchor Peer 를 이용한다. Leader Peer=Anchor Peer 로도 설정 할 수도 있다

Fabric에 Peer Leader 선출은 `config/core.yaml`에 나와있다.

> core.yaml

```
peer:
    # Gossip related configuration
    gossip:
      # Defines whenever peer will initialize dynamic algorithm for
      # "leader" selection, where leader is the peer to establish
      # connection with ordering service and use delivery protocol
      # to pull ledger blocks from ordering service. It is recommended to
      # use leader election for large networks of peers.
      useLeaderElection: true
      # Statically defines peer to be an organization "leader",
      # where this means that current peer will maintain connection
      # with ordering service and disseminate block across peers in
      # its own organization
      orgLeader: false
```
