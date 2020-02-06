---
title : Ethereum Decentralized Applications (DApps) -1-
tags :
- DApps
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

web3 **댑(DApps)** 은 storage, messaging, naming 등 어플리케이션의 다른 모든 측면을 탈중앙화하는 것에 관한것이다.

> Example 1. Web3: A decentralized web using smart contracts and P2P technologies

![image](https://user-images.githubusercontent.com/44635266/73839706-f781f580-4859-11ea-9a8d-4a33eea833b9.png)

현재 포스트에서는 경매 플랫폼인 댑 샘플 개발과 배포 프로세스를 보여줄것입니다. 먼저 댑의 특징과 장점을 살펴보겠습니다.

## What Is a DApp?

댑은 mostly / entirely 탈중앙화된 어플리케이션 입니다.

어플리케이션의 탈중앙화 가능한 측면은 다음과 같습니다.

* Backend software
* Frontend software
* Data Storage
* Message communication
* Name resolution

이를통해 중앙화된 아키텍처가 제공할 수 없는 댑이 가지는 장점이 있습니다.

**지속성(resiliency)**

비즈니스 로직은 스마트 컨트렉트로 제어되기 때문에 댑 백엔드는 블록체인 플랫폼에서 탈중앙화되고 관리됩니다.

댑은 중앙 집중식 서버에 배포된 어플리케이션과 달리 가동 중지 시간이 없으며, 플랫폼이 계속 작동하는 한 사용할 수 있다.

**투명성(transparency)**

댑의 온체인 특성으로 인해 누구나 코드를 검사하고 기능에 대해 더 확신할 수 있다. 댑과 상호작용한 모든 내용은 블록체인에 영원히 저장될 것이다.

**검열 저항(censorship resistance)**

사용자가 이더리움 노드에 접근하는 한 사용자는 중앙화된 컨트롤의 간섭 없이 댑과 항상 상호작용할 수 있다.

서비스 제공 업체 또는 심지어 스마트 컨트랙트의 소유자 또한 네트워크에 배포된 코드를 변경할 수 없다.

현재 시점에서 완전히 탈중앙화된 어플리케이션은 매우 드물지만 앞으로 댑의 모든 부분을 탈중앙화된 방식으로 운영할 수 있을 것이라 기대합니다.

### Backend (Smart Contract)

스마트 컨트랙트 아키텍처 설계의 주요 고려사항 중 하나는 스마트 컨트랙트가 배포된 후 스마트 컨트랙트의 코드를 변경할 수 없다는 것입니다. 접근 가능한 SELFDESTRUCT 연산코드가 프로그래밍된 경우 삭제할 수 있지만, 완전히 제거하는 것 외에는 코드를 변경할 수 없습니다.

두 번째 주요 고려사항은 댑 크기입니다. 스마트 컨트랙트는 배포하고 위해 많은 양의 가스를 소비할 수 있습니다. 따라서 일부 어플리케이션에서는 오프체인 계산과 외부 데이터 소스를 선택할 수 있습니다.

### Frontend (Web User Interface)

댑의 클라이언트 쪽 인터페이스는 표준 웹 기술(HTML, CSS, JS) 을 사용할 수 있습니다.

프론트엔드는 일반적으로 프론트엔드 자원과 함께 번들로 제공되며, 웹 서버에 의해 브라우저에서 제공되는 web3.js 자바스크립트 라이브러리를 통해 이더리움에 연결됩니다.

### Data Storage

높은 가스 비용과 낮은 블록 가스 한도 때문에 스마트 컨트랙트는 많은 양의 데이터를 저장하거나 처리하는 데 적합하지 않습니다. 따라서 댑은 오픈체인 데이터 스토리지 서비스를 사용하는데, 사이즈가 큰 데이터들을 이더리움 체인으로부터 데이터 스토리지 플랫폼으로 옮겨 저장합니다.

데이터 스토리지 플랫폼은 중앙화될 수 있거나 탈중앙화 될 수 있는데, 이때 IPFS 나 Swarm 같은 탈중앙화된 플랫폼에 저장합니다.

#### IPFS

IPFS(Inter-Planetary File System) 는 저장된 객체를 P2P 네트워크의 피어들에게 배포하는 중앙화된 스토리지 시스템입니다.

IPFS 는 content-addressable 한데 이 의미는 각 내용이 해싱되고 해당 파일을 식별하는데 사용된다는 의미 입니다. 그리고 해시로 요청하여 모든 IPFS 노드에서 파일을 검색할 수 있습니다.

#### Swarm

**스웜(Swarm)** 은 또다른 content-addressable 부여 가능한 P2P 스토리지 시스템으로 IPFS 와 유사합니다.

스웜은 이더리움 재단에서 **Go-Ethereum** 도구 모음의 일부로 만들어졌습니다. 스웜은 IPFS 와 유사하게 스웜 노드에 의해 전파되고 복제되는 파일을 저장할 수 있습니다. 해시를 사용하여 임의의 스웜 파일에 접근할 수 있습니다.

스웜을 사용하면 중앙 웹 서버가 아닌 탈중앙화 P2P 시스템을 통해 웹 사이트에 접근할 수 있습니다.

### Decentralized Message Communications Protocols

모든 어플레케이션의 또 다른 주요 구성 요소는 프로세스간 통신입니다. 전통적으로 프로세스 통신은 중앙화된 서버를 이용했습니다. 하지만 P2P 네트워크 위에서 메세징을 제공하는 서버 기반 프로토콜을 대체할 여러 탈중앙화 프로토콜이 있습니다.

댑의 가장 주목할 만한 P2P 메세징 프로토콜은 이더리움 재단의 **위스퍼(Whisper)** 입니다.