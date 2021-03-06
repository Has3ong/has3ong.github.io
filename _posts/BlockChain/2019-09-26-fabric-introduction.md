---
title : Hyperledger Fabric Introduction
categories:
 - BlockChain
tags:
 - Hyperledger Fabric
 - BlockChain
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## Hyperledger

스마트 계약을 구현할 수 있는 오픈소스 기반의 프라이빗 블록체인 프로젝트이다. 리눅스재단(Linux Foundation)이 주관하고 있다. 금융, 사물인터넷(IoT), 물류, 제조, 기술 등 여러 산업에 걸쳐 응용 가능한 블록체인 기술을 만드는 것을 목표로 하고 있다.
 
프라이빗 블록체인 기술의 표준으로 자리잡고 있다. 이 외에도 리플, 이더리움등 다른 블록체인도 있다. 하지만 하이퍼레저가 특별한 이유는 아래와 같다.
* 하이퍼레저는 프라이빗 블록체인 플랫폼으로 기업 비즈니스를 구현하기에 적합한 환경이다.
* 하이퍼레저는 특정 비즈니스 모델에 특화된 타 플랫폼과 달리 여러 산업에 범용적으로 도입 가능한 기술 표준을 제시한다.
 
하이퍼레저는 위와 같은 차별화 전략을 구현하기 위해 다양한 기업용 블록체인 기술을 양산하고자 한다. 
* 분산원장 프레임워크
* 스마트 계약 엔진
* 클라이언트 라이브러리
* 그래픽 인터페이스
* 기타 유틸리티
* 샘플 어플리케이션


## Hyperledger Fabric

![스크린샷 2019-09-27 오전 3 05 32](https://user-images.githubusercontent.com/44635266/65715929-0e108700-e0d9-11e9-9070-500ad61ec485.png)

하이퍼레저 패브릭(Hyperledger Fabric)은 모듈형 구조로 응용 프로그램 및 솔루션 개발의 중심 역할을 수행한다. 의견 상의 일치 또는 회원 서비스와 같은 구성 요소를 플러그 인드 플레이(plug and play) 방식으로 지원한다. 사실상 ‘하이퍼레저’라고 명명할 때에는 하이퍼레저 패브릭을 의미하는 경우가 많을 정도로, 하이퍼레저 프로젝트 전체의 핵심이 되는 부분이다.


## Hyperledger Architecture

![스크린샷 2019-09-27 오전 3 05 38](https://user-images.githubusercontent.com/44635266/65715927-0e108700-e0d9-11e9-85ea-effd18b349f8.png)

> Hyperledger APIs, SDKs, CLI

## Hyperledger Fabric Model

### Peer

Peer는 Ledger와 Chaincode를 관리하는 네트워크 노드입니다. 블록체인 네트워크는 Peer들의 집합으로 이루어져 있습니다. Peer들은 Ledgers와 Chaincode에 대해 호스팅하기에 블록체인 네트워크의 기본적인 요소입니다. Ledger는 Chaincode로 인해 발생하는 모든 거래를 불변하게 기록하게 됩니다. Chaincode와 Ledger는 각각 공유 프로세스와 정보를 네트워크에 캡슐화하는데 사용됩니다.

* Endorsing Peer: 스마트 컨트랙트에 수행될 트랜잭션을 시뮬레이션해보고 그 결과를 클라이언트 어플리케이션에 리턴해주는 피어입니다. 트랜잭션을 검증하는 역할을 하는 거죠.
* Committing Peer: 오더링까지 되어서 전달된 트랜잭션 블럭을 검증하고, 검증이 완료되면 자기가 갖고 있는 원장에 해당 블럭을 추가하고 관리합니다. 모든 피어는 기본적으로 committing peer입니다.
* Anchor Peer: 채널 내의 대표 피어입니다. 채널에 다른 조직이 가입하면 가장 먼저 발견하는 피어입니다.
* Leading Peer: 여러 피어를 가지고 있는 조직의 경우, 모든 피어를 대표하여 네트워크와 커뮤니케이션 하는 피어입니다.

### Assets

블록체인은 거래를 전제로 하는 네트워크다. 그 거래가 이루어질려면 부동산과 같은 유형에서 계약, 지적 재산과 같은 품목을 Assets이라고 한다. Assets은 패브릭에서 키 값 쌍으로 표시되며 상태 변경은 채널 원장에서 트랜잭션으로 기록된다.
 
거래의 과정에 따라 *State*가 생기며 이 State가 변하는 것을 기록한것이 *Ledger*이다.
 
### Chaincode

Chaincode는 자산 또는 자산을 정의하는 소프트웨어 및 수정하기 위한 거래 지시 사항이다. Chaincode키 값 쌍 또는 다른 상태 데이터베이스 정보를 읽거나 변경하기 위한 규칙을 시행한다. Chaincode기능은 원장의 상태 데이터베이스에 대해 실행되며 거래 제안을 통해 시작된다. 체인코드 실행은 네트워크에 제출되어 모든 피어의 원장에 키 값이 적용된다
 
네트워크 권한에 따라 접근할 수 있는 Chaincode가 달라진다. 여러 트랜잭션이 동시에 발생한다면 그 발생한 순서에 따라 제대로 ordering 될대만 실제 ledger에 반영이 된다.
 
### Ledger

Ledger는 패브릭의 모든 상태에 대한 변경 방지 기록이다. 생태 전이는 참여 당사자가 제출 한 Chaincode호출의 결과이다. 자산 키-값의 생성으로 각 트랜잭션 결과를 원장에 기여하고 있다. 원장은 불변의 레코드를 블록으로 저장하는 블록체인과 현재 패브릭 상태를 유지하는 스테이트 데이터베이스로 구성된다. 채널당 1개의 원장이 있으며 각 피어는 각 채널에 대해 원장 사본을 보관한다.
 
### Consensus

Consensus는 블록체인 네트워크 내의 peer들이 항상 동기화 된 State과 Ledger를 가지게 하는 기술이다.
공유 원장 기술에서 합의는 단일 기능 내에서 특정 알고리즘과 동의어로 사용된다. 그러나 합의는 단순히 거래 순서에 동의하는 것 이상의 의미를 지니며, 이러한 차별화는 제안 및 보증, 오더링, 검증에 이르기까지 전체 거래 흐름에서 기본적인 역할을 한다. 합의는 블록을 구성하는 일련의 트랜잭션의 정확성에 대한 완전한 단일 검증으로 정의된다. 컨센서스는 블록 트랜잭션의 순서와 결과가 명시적인 기준 검사를 충족하면 달성된다. 이러한 확인 및 잔액은 거래의 주기 동안 발생하며 특정 거래 클래스를 보증해야하는 특정 회원 및 시스템 Chaincode를 보증하는 보증정책의 사용을 포함하여 이러한 정책이 시행되고 유지되도록 한다.

트랜잭션이 포함 된 블록이 원장에 추가되기 전에 원장의 현재 상태에 대한 확인이 수행된다. 수많은 승인, 유효성 및 버전 검사가 수행되는 것 외에도 트랜잭션 흐름의 모든 방향에서 신원 확인이 진행된다. 액세스 제어 목록은 네트워크의 계층 구조에서 구현되며 트랜잭션 제안이 다른 아키텍처 구성 요소를 통과 할 때 페이로드는 반복적으로 서명, 확인 및 인증된다. 결론적으로, 합의는 일련의 거래의 합의 된 오더링에만 국한되는 것이 아니라 오히려 거래 제안이 의결에서 수락되기까지 진행되는 검증의 부산물로서 달성되는 중요한 특성이다.
 
### Privacy

하이퍼레저 패브릭은 채널별로 원장을 사용하고 자산의 현재 상태를 수정할 수 있는 Chaincode를 사용한다. 모든 참가자가 하나의 공통 채널에서 운영되고 있다고 가정하면 전체 네트워크에서 공유 할 수 있다. 또는 특정 참여자 집합만 포함하도록 사유화 할 수 있다.
후자의 시나리오에서, 이 참여자는 별도의 *Channel*을 작성하여 거래 및 원장을 분리한다. Channel은 페브릭 네트워크 서브넷 개념으로 생각하면 된다. 채널 안에서 피어들은 프라이빗하게 정보를 주고 받을 수 있다. 전체 투명성과 프라이버시 사이의 차이를 좁히고 Chaincode는 자산 상태에 액세스하여 읽기 및 쓰기를 수행해야하는 피어에만 설치가능하다. 데이터에 대한 보안성을 높이기 위해 Chaincode내의 값은 장부에 추가하기 전에 AES와 같은 공통 암호화 알고리즘을 사용하여 부분적으로 또는 전체적으로 암호화 한다.
 
### Security & Membership Service

하이퍼레저 페브릭은 신원이 확인되고 가입에 대해 사전 승인을 받은 피어만이 네트워크에 가입할 수 있다.
하이퍼레저 패브릭은 모든 참가자가 신원을 알고 있는 트랜잭션 네트워크를 지원한다. 공개 키 인프라는 조직, 네트워크 구성 요소 및 최종 사용자 또는 클라이언트 응용 프로그램에 연결된 암호화 인증서를 생성하는 데 사용된다. 결과적으로 데이터 액세스 제어는 광범위한 네트워크 및 채널 수준에서 조작되고 제어된다. 하이퍼레저 패브릭의 허가의 개념은 채널의 존재 및 기능과 함께 개인 정보 및 기밀성이 중요한 관심사인 시나리오를 해결하는 데 도움이 된다.

## Hyperledger Fabric Transaction Flow

![스크린샷 2019-09-27 오전 3 06 43](https://user-images.githubusercontent.com/44635266/65715926-0e108700-e0d9-11e9-8146-b90528c0f063.png)

### Step 1: Client 가 트랜잭션 요청(transaction proposal)

Client A가 블록체인 네트워크에 트랜잭션을 요청합니다. 그 트랜잭션에 대해서 승인해야 하는 피어가 endorsement policy로 정의되어 있는데, 이 단계에서 그 피어들에게 해당 요청을 전송합니다. 이 피어들에게 *transaction proposal이라는 형태로 전송*되는데, 클라이언트의 SDK는 이를 gRPC 프로토콜로 전송할 수 있는 프로토콜 버퍼 형태로 변형합니다. 또한 사용자의 신원 정보를 서명 형태로 proposal에 삽입합니다.

### Step 2: Endorsing peers 가 서명을 확인하고 트랜잭션 실행

Endorsing peer는 일단 트랜잭션을 전달 받으면, 1) 트랜잭션의 형식에 맞게 내용이 잘 채워져있는지 2) 이전에 제출된 적 있었던 트랜잭션은 아닌지 3) 서명이 유효한지(MSP를 통함) 4) 트랜잭션을 제출한 클라이언트가 그럴 권한이 있는지 확인합니다. 이게 확인이 되면, Endorsing peer는 Transaction proposal을 인자로 받아서 체인코드를 실행합니다. State DB의 값에 체인코드가 실제로 실행되며 결과값, read/write set을 반환합니다. *이 시점에는 원장 업데이트는 하지 않고, 반환된 결과값을 proposal response로 클라이언트 SDK로 전송합니다.*

### Step 3: Proposal responses 검토

그후 클라이언트 SDK가 Endorsing peer의 서명을 확인한 뒤 각 피어로부터의 proposal response를 비교하는 작업을 거칩니다. 단순한 쿼리 같이 Ordering service가 필요 없는 경우에는 쿼리 결과값을 얻고 프로세스가 종료됩니다. 원장 업데이트와 같은 경우, 클라이언트 차원에서 Endorsement policy에 준하는 proposal response가 왔는지(A, B가 모두 결과를 보냈는지) 검토합니다.
단, 이 단계에서 클라이언트가 endorsement policy를 검토하지 않는다고 해도, committing 단계에서 각 피어가 별도로 검토를 합니다.

### Step 4: 클라이언트가 Transaction 전달

검토가 완료되고 나면 클라이언트가 Transaction message에 proposal과 proposal response를 담아서 Ordering service에 보냅니다. 트랜잭션에는 read/write set이 들어가 있을 것이고, Endorsing peer의 서명과 채널 ID가 포함됩니다. Orderer는 트랜잭션 내용에 관계 없이, 모든 채널에서 발생하는 트랜잭션을 받아서 시간 순서대로 정렬하여 블럭을 생성합니다.

### Step 5: Committing Peer에서 트랜잭션을 검증하고 커밋

트랜잭션 블럭이 해당 채널의 모든 Committing Peer에게 전달됩니다. 각각의 committing peer는 블럭 내의 모든 트랜잭션이 각각의 Endorsement policy를 준수하는지, world state 값의 read-set 버전이 맞는지(read-set 버전은 트랜잭션 이후에만 변경됨) 확인합니다. 검사 과정이 끝나면 해당 블럭 내의 트랜잭션에는 valid/invalid 값이 태그됩니다.

### Step 6: Ledger updated

각 피어는 최종 검증을 마친 블럭을 채널 내 체인에 붙입니다. 그리고 유효한 트랜잭션의 경우 write-set이 state DB에 입력됩니다. 일련의 과정이 마무리되면 이벤트를 발생시켜 클라이언트에게 작업 결과에 대해 알립니다.


