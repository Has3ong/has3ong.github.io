---
title : Ethereum Decentralized Applications (DApps)
tags :
- DApps
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

web3 **댑(DApps)** 은 storage, messaging, naming 등 어플리케이션의 다른 모든 측면을 탈중앙화하는 것에 관한것이다.

> Example 1 - Web3: A decentralized web using smart contracts and P2P technologies

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


## A Basic DApp Example: Auction DApp

경매 댑은 사용자가 주택, 자동차 같은 고유한 자산을 나타내는 **증서(deed)** 토큰을 등록할 수 있게 합니다. 토큰이 등록되면 토큰 소유권이 경매 댑으로 이전되며 판매를 위해 리스팅할 수 있게 합니다. 경매 중에 사용자는 경매를 위해 만들어진 대화방에 참여하고, 경매가 완료되면 증서 토큰 소유권이 경매 낙찰자에게 이전됩니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/73842165-644bbe80-485f-11ea-9c83-b78a473518f2.png)

경매 댑의 주요 구성 요소는 다음과 같습니다.

* ERC721 대체 불가능한 증서 토큰을 구현하는 스마트 컨트랙트
* 증서를 팔기 위해 경매를 구현하는 스마트 컨트랙트
* Vue/Vuetify 자바 스크립트 프레임 워크를 사용하는 웹 프론트엔드
* 이더리움 체인에 연결하는 web3.js 라이브러리
* 이미지 같은 자원을 저장하는 스웜 클라이언트
* 모든 참여자를 위해 경매별 대화방을 개설하기 위한 위스퍼 클라이언트

경매댑 소스 코드는 [Github](https://github.com/ethereumbook/ethereumbook/tree/develop/code/auction_dapp) 로 가면 됩니다.

### Auction DApp: Backend Smart Contracts

아래 예제는 `DeedRepository` 를 살펴보겠습니다. 이 컨트랙트는 ERC721 대체 불가능한 토큰입니다.

> Example - DeedRepository.sol: An ERC721 deed token for use in an auction

```java
pragma solidity ^0.4.17;
import "./ERC721/ERC721Token.sol";

/**
 * @title Repository of ERC721 Deeds
 * This contract contains the list of deeds registered by users.
 * This is a demo to show how tokens (deeds) can be minted and added 
 * to the repository.
 */
contract DeedRepository is ERC721Token {


    /**
    * @dev Created a DeedRepository with a name and symbol
    * @param _name string represents the name of the repository
    * @param _symbol string represents the symbol of the repository
    */
    function DeedRepository(string _name, string _symbol) 
        public ERC721Token(_name, _symbol) {}
    
    /**
    * @dev Public function to register a new deed
    * @dev Call the ERC721Token minter
    * @param _tokenId uint256 represents a specific deed
    * @param _uri string containing metadata/uri
    */
    function registerDeed(uint256 _tokenId, string _uri) public {
        _mint(msg.sender, _tokenId);
        addDeedMetadata(_tokenId, _uri);
        emit DeedRegistered(msg.sender, _tokenId);
    }

    /**
    * @dev Public function to add metadata to a deed
    * @param _tokenId represents a specific deed
    * @param _uri text which describes the characteristics of a given deed
    * @return whether the deed metadata was added to the repository
    */
    function addDeedMetadata(uint256 _tokenId, string _uri) public returns(bool){
        _setTokenURI(_tokenId, _uri);
        return true;
    }

    /**
    * @dev Event is triggered if deed/token is registered
    * @param _by address of the registrar
    * @param _tokenId uint256 represents a specific deed
    */
    event DeedRegistered(address _by, uint256 _tokenId);
}
```

보다시피 ERC721 호환 토큰을 간단하게 구현한 것입니다.

이 컨트랙트를 사용하여 각 경매에 대한 토큰을 발행하고 추적합니다. 경매 자체는 `AuctionRepository` 컨트랙트에 의해 조율됩니다.

위 코드는 너무 길어서 중요한 부분만 적겠습니다. 전체 코드는 [Github](https://github.com/ethereumbook/ethereumbook/blob/develop/code/auction_dapp/backend/contracts/AuctionRepository.sol) 경로에 있습니다.

> Example - AuctionRepository.sol: The main Auction DApp smart contract

```java
contract AuctionRepository {
    
    // Array with all auctions
    Auction[] public auctions;

    // Mapping from auction index to user bids
    mapping(uint256 => Bid[]) public auctionBids;

    // Mapping from owner to a list of owned auctions
    mapping(address => uint[]) public auctionOwner;

    // Bid struct to hold bidder and amount
    struct Bid {
        address from;
        uint256 amount;
    }

    // Auction struct which holds all the required info
    struct Auction {
        string name;
        uint256 blockDeadline;
        uint256 startPrice;
        string metadata;
        uint256 deedId;
        address deedRepositoryAddress;
        address owner;
        bool active;
        bool finalized;
    }
```

`AuctionRepository` 컨트랙트는 다음 기능을 사용하여 모든 경매를 관리합니다.

```java
getCount()
getBidsCount(uint _auctionId)
getAuctionsOf(address _owner)
getCurrentBid(uint _auctionId)
getAuctionsCountOfOwner(address _owner)
getAuctionById(uint _auctionId)
createAuction(address _deedRepositoryAddress, uint256 _deedId,
              string _auctionTitle, string _metadata, uint256 _startPrice,
              uint _blockDeadline)
approveAndTransfer(address _from, address _to, address _deedRepositoryAddress,
                   uint256 _deedId)
cancelAuction(uint _auctionId)
finalizeAuction(uint _auctionId)
bidOnAuction(uint _auctionId)
```

책의 저장소에 있는 truffle 을 사용하여 이더리움 블록체인에 컨트랙트를 배포할 수 있습니다.

```shell
$ cd code/auction_dapp/backend
$ truffle init
$ truffle compile
$ truffle migrate --network ropsten
```

### DApp governance

경매 댑의 스마트 컨트랙트를 살펴보면 특별 권한을 가진 계정이나 역할이 없습니다. 경매에는 특별한 권한이 있는 소유자가 있지만 경매 댑 자체에는 특권을 가진 사용자가 없습니다.

이는 댑 거버넌스를 탈중앙화하고 배포되면 모든 통제권을 포기하게 만들기 위한 선택입니다. 이에 비해 일부 댑은 컨트랙트를 무시하거나 설정을 변경하거나 특정 작업을 'veto' 할 수 있는 능력을 가진 계정을 보유하고 있습니다. 일반적으로 이러한 기능은 버그로 인해 알려지지 않은 문제를 피하기 위해 댑에 적용됩니다.

댑은 특권 계정을 위한 특수 접근 권한을 허용하지 말아야합니다. 왜냐하면 그것은 탈중앙화가 아니기 때문입니다.

### Auction DApp: Frontend User Interface

경매 댑이 배포되면 web3.js 나 web3 라이브러리를 사용하여 댑의 컨트랙트와 상호작용 할 수 있지만 대부분의 사용자는 쉬운 인터페이스가 필요하기 때문에 Vue/Vuetify 자바스크립트 프레임워크를 사용하여 작성하였습니다.

위 경로에는 [Github](https://github.com/ethereumbook/ethereumbook/tree/develop/code/auction_dapp/frontend) 사용자 인터페이스 코드를 찾을 수 있습니다. 디렉토리 구조는 아래와 같습니다.

```shell
frontend/
|-- build
|   |-- build.js
|   |-- check-versions.js
|   |-- logo.png
|   |-- utils.js
|   |-- vue-loader.conf.js
|   |-- webpack.base.conf.js
|   |-- webpack.dev.conf.js
|   `-- webpack.prod.conf.js
|-- config
|   |-- dev.env.js
|   |-- index.js
|   `-- prod.env.js
|-- index.html
|-- package.json
|-- package-lock.json
|-- README.md
|-- src
|   |-- App.vue
|   |-- components
|   |   |-- Auction.vue
|   |   `-- Home.vue
|   |-- config.js
|   |-- contracts
|   |   |-- AuctionRepository.json
|   |   `-- DeedRepository.json
|   |-- main.js
|   |-- models
|   |   |-- AuctionRepository.js
|   |   |-- ChatRoom.js
|   |   `-- DeedRepository.js
|   `-- router
|       `-- index.js
```

컨트랙트 배포 후 *frontend/src/config.js* 에서 프론트엔드 설정을 편집하고 `DeedRepository` 및 `AuctionRepository` 컨트랙트 주소를 배포된 대로 입력하세요. 프론트 어플리케이션도 JSON-RPC / WebSockets 인터페이스를 제공하는 이더리움 노드에 대한 접근이 필요합니다. 그 후 프론트앤드를 실행하면 됩니다.

```shell
$ npm install
$ npm run dev
```

실행이 되면 웹 브라우저에서 **http://localhost:8080** 을 통해 접근할 수 있습니다.

정상적으로 실행되면 아래와 같은 화면이 표시됩니다.

> Example 3 - Auction DApp user interface

![image](https://user-images.githubusercontent.com/44635266/73845255-96601f00-4865-11ea-945f-d3e56cde059b.png)

## Further Decentralizing the Auction DApp

댑을 탈중앙화하고 복원력을 좋게 만들 수 있는 2 가지 방법이 있습니다.

* 모든 어플리케이션 코드를 스웜 또는 IPFS 에 저장한다.
* 이더리움 네임 서비스를 사용하여 네임을 참조하여 댑에 접근한다.

## Storing the Auction DApp on Swarm

댑 자체의 프론트엔드 전체를 스웜에 저장하고 웹 서버를 실행하는대신 스웜 노드에서 직접 실행해 보겠습니다.

### Preparing Swarm

먼저 스웜을 설치하고 스웜 노드를 초기합니다.

스웜을 설치하고나면 스웜을 실행하여 version 명령어로 올바르게 설치된지 확인합니다.

```shell
$ swarm version
Version: 0.3
Git Commit: 37685930d953bcbe023f9bc65b135a8d8b8f1488
Go Version: go1.10.1
OS: linux
```

스웜을 실행하려면 JSON_RPC API 에 접근하기 위해 게스 인스턴스에 연결해야 합니다.

스웜을 시작하면 다음 내용이 표시됩니다.

```shell
Maximum peer count                       ETH=25 LES=0 total=25
Starting peer-to-peer node               instance=swarm/v0.3.1-225171a4/linux...
connecting to ENS API                    url=http://127.0.0.1:8545
swarm[5955]: [189B blob data]
Starting P2P networking
UDP listener up                          self=enode://f50c8e19ff841bcd5ce7d2d...
Updated bzz local addr                   oaddr=9c40be8b83e648d50f40ad3... uaddr=e
Starting Swarm service
9c40be8b hive starting
detected an existing store. trying to load peers
hive 9c40be8b: peers loaded
Swarm network started on bzz address: 9c40be8b83e648d50f40ad3d35f...
Pss started
Streamer started
IPC endpoint opened                      url=/home/ubuntu/.ethereum/bzzd.ipc
RLPx listener up                         self=enode://f50c8e19ff841bcd5ce7d2d...
```

로컬 스웜 게이트웨이 웹 인터페이스 **http://localhost:8500** 에 연결하여 스웜 노드가 올바르게 실행되고 있는지 확인할 수 있습니다.

> Example 4 - Swarm gateway on localhost

![image](https://user-images.githubusercontent.com/44635266/73930718-59a22f80-491a-11ea-9fee-dad4c1c4a021.png)

### Uploading Files to Swarm

로컬 스웜 노드와 게이트웨이가 실행되면 스웜에 업로드 할 수 있으며, 파일 해시를 참조하여 스웜 노드에서 파일에 접근할 수 있습니다.

파일을 업로드하여 테스트해보겠습니다.

```shell
$ swarm up code/auction_dapp/README.md
ec13042c83ffc2fb5cb0aa8c53f770d36c9b3b35d0468a0c0a77c97016bb8d7c
```

경매 댑에는 모든 자원을 패키징하는 스크립트가 있습니다.

파일 하나를 업로드 하는 것은 비교적 간단하지만, 댑 프런트 엔드 전체를 업로드 하는 것은 좀 더 복잡합니다. 일반적으로 웹 서버는 URL 을 로컬 파일로 변환하고 올바른 자원을 제공합니다. 우리는 댑을 패키징하여 스웜에 대해서도 동일한 결과를 얻을 수 있습니다.

경매 댑에는 모든 자원을 패키징하는 스크립트가 있습니다.

```shell
$ cd code/auction_dapp/frontend
$ npm run build

> frontend@1.0.0 build /home/aantonop/Dev/ethereumbook/code/auction_dapp/frontend
> node build/build.js

Hash: 9ee134d8db3c44dd574d
Version: webpack 3.10.0
Time: 25665ms
Asset     Size
static/js/vendor.77913f316aaf102cec11.js  1.25 MB
static/js/app.5396ead17892922422d4.js   502 kB
static/js/manifest.87447dd4f5e60a5f9652.js  1.54 kB
static/css/app.0e50d6a1d2b1ed4daa03d306ced779cc.css  1.13 kB
static/css/app.0e50d6a1d2b1ed4daa03d306ced779cc.css.map  2.54 kB
static/js/vendor.77913f316aaf102cec11.js.map  4.74 MB
static/js/app.5396ead17892922422d4.js.map   893 kB
static/js/manifest.87447dd4f5e60a5f9652.js.map  7.86 kB
index.html  1.15 kB

Build complete.
```

이 명령의 결과는 새로운 디렉터리 `code/auction_dapp/frontend/dist` 에 있스빈다. 경매 댑 프론트엔드 전체를 포함하여 함께 패키징됩니다.

```shell
dist/
|-- index.html
`-- static
    |-- css
    |   |-- app.0e50d6a1d2b1ed4daa03d306ced779cc.css
    |   `-- app.0e50d6a1d2b1ed4daa03d306ced779cc.css.map
    `-- js
        |-- app.5396ead17892922422d4.js
        |-- app.5396ead17892922422d4.js.map
        |-- manifest.87447dd4f5e60a5f9652.js
        |-- manifest.87447dd4f5e60a5f9652.js.map
        |-- vendor.77913f316aaf102cec11.js
        `-- vendor.77913f316aaf102cec11.js.map
```

이제 up 명령과 --recursive 옵션을 사용하여 댑 전체를 스웜에 업로드할 수 있습니다. 여기서 `index.html` 이 댑을 로드하기 위한 defaultpath 라는 사실을 스웜에게 알려줍니다.

```shell
$ swarm --bzzapi http://localhost:8500 --recursive \
  --defaultpath dist/index.html up dist/

ab164cf37dc10647e43a233486cdeffa8334b026e32a480dd9cbd020c12d4581
```

## The Ethereum Name Service (ENS)

전통적인 인터넷에서 DNS 는 브라우저에서 사람이 읽을 수 있는 이름을 사용할 수 있게 해줍니다. DNS 는 브라우저에서 사용하는 이름을 IP 주소 해당 페이지 내에 다른 식별자로 해석한다. 이더리움 블록체인에서는 ENS(Ethereum Naming System) 가 이와 같은 문제를 탈중앙화된 방식으로 풀어줍니다.

예를 들어, 이더리움 재단의 기부 주소 **0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359** 는 ENS 를 지원하는 지갑에서는 간단하게 `ethereum.eth` 가 됩니다.

ENS 는 스마트 컨트랙트 이상의 기능이 있습니다. ENS 는 기본적으로 댑이고 탈중앙화 네임 서비스를 제공합니다. 또한 등록, 관리 그리고 등록된 이름의 경매를 위한 여러 댑이 ENS 기능을 지원합니다. ENS 는 댑이 다른 댑을 지원하기 위해 만들어지고, 댑의 생태계에 의해서 유지되고, 다른 댑에 포함되어 동작하는 등 댑들이 어떻게 협력하는지 보여줍니다.

### History of Ethereum Name Services

네임 등록은 **네임 코인(Namcoin)** 개척한 블록체인 최초 비화폐 어플리케이션이었습니다.

게스와 C++ 이더리움 클라이언트의 초기 릴리스에는 namereg 컨트랙트 내장되어 있으며, 네임 서비스를 위한 많은 제안과 ERC 가 만들어졌습니다. 그러나 2016년 부터 **레지스타(registrar)** 에 대한 작업이 시작되었습니다.

### The ENS Specification

ENS 는 주로 3 가지 이더리움 개선 제안에 명시되어 있습니다.

* **EIP-137** : 기본 기능을 지정
* **EIP-162** : .eth 루트에 대한 경매 시스템
* **EIP-181** : 주소의 역 등록을 지정

ENS 는 샌드위치 디자인 철학을 따릅니다. 맨 아래에는 매우 단순한 층이 있고, 그 다음에는 더 복잡하지만 대체 가능한 코드가 포함되어 있으며, 매우 간단한 최상위 계층은 모든 자금을 별도의 계정에 보관합니다.

## Bottom Layer: Name Owners and Resolvers

ENS 는 사람이 읽을 수 있는 이름 대신 **노드(node)** 로 작동합니다. 사람이 읽을 수 있는 이름은 **네임해시(Namehash)** 알고리즘을 사용하여 노드로 변환합니다.

ENS 의 기본 계층은 노드의 소유자만 자신의 이름에 대한 정보를 설정하고 하위 노드를 만들 수 있도록 하는 ERC137 에서 정의한 단순 스마트 컨트랙트 입니다.

기본 계층의 유일한 기능은 노드 소유자가 자신의 노드에 대한 정보(resolver) 를 설정하고 새 하위 노드의 소유자를 만들 수 있게 하는 기능입니다.

### The Namehash algorithm

네임해시는 어떤 이름이라도 그 이름을 식별하는 해쉬로 변환할 수 있는 재귀 알고리즘입니다.

네임해시는 재귀적으로 이름의 구성요소를 해시하여 유효한 입력 도메인에 대한 고유한 고정 길이 문자열을 생성합니다. 예를 들어, `subdomain.example.eth` 의 네임해시 노드는 `keccak('<example.eth> node) + keccak('<subbdomain>)` 입니다. 우리가 해결해야할 하위 문제는 `keccak('<.eth>' node) + keccak('<example>')` 인 `example.eth` 노드를 계산하는 거싱ㅂ니다. 먼저 `keccak(<root node>) + keccak('<eth>')` 인 eth 에 대한 노드를 계산해야합니다.

루트 노드는 재귀의 **기본 케이스(base case)** 라 부르는 것이며, 이것은 당연히 재귀적으로 정의할 수 없는데, 그렇지 않으면 알고리즘은 영원히 종료되지 않을 것입니다. 루트노드는 `0x0000000000000000000000000000000000000000000000000000000000000000` 로 정의합니다.
 
이 모든 것을 합치면, `subdomain.example.eth` 의 노드가 `keccak(keccak(keccak(0x0...0 + keccak('eth')) + keccak('example')) + keccak('subdomain'))` 으로 됩니다.

일반화하자면 네임해시 함수를 다음과 같이 정의할 수 있습니다.

```shell
namehash([]) = 0x0000000000000000000000000000000000000000000000000000000000000000
namehash([label, ...]) = keccak256(namehash(...) + keccak256(label))
```

파이썬에서는 다음과 같습니다.

```python
def namehash(name):
  if name == '':
    return '\0' * 32
  else:
    label, _, remainder = name.partition('.')
    return sha3(namehash(remainder) + sha3(label))
```

따라서 mastering-ethereum.eth 에서는 다음과 같이 처리됩니다.

```shell
namehash('mastering-ethereum.eth')
⇒ sha3(namehash('eth') + sha3('mastering-ethereum'))
⇒ sha3(sha3(namehash('') + sha3('eth')) + sha3('mastering-ethereum'))
⇒ sha3(sha3(('\0' * 32) + sha3('eth')) + sha3('mastering-ethereum'))
```

하위 도메인은 그 자체가 하위 도메인을 가질 수 있습니다. `subdomain.example.eth` 다음에 `sub.subdomain.example.eth`, 그 다음은 `sub.sub.subdomain.example.eth` 등이 될 수 있습니다.

값비싼 재계산을 피하기 위해 네임해시는 이름 자체에만 의존하기 때문에 주어진 이름의 노드를 미리 계산한 후 컨트랙트에 삽입하여 문자열 조작의 필요성을 제거하고 원시 이름의 구성요소 수에 관계없이 ENS 레코드를 즉시 검색할 수 있습니다.

### How to choose a valid name

라벨과 도메인을 길이에 관계없이 사용할 수 있지만, 레거시 DNS 와의 호환성을 위해 다음 규칙을 권장합니다.

* 라벨은 각각 64 자를 넘지 않아야 한다.
* 완전한 ENS 이름은 255 자를 넘지 않아야 한다.
* 라벨은 하이픈으로 시작하거나 끝나서는 안되며, 숫자로 시작해서도 안 된다.

### Root node ownership

계층적 시스템의 결과 중 하나는 이것이 최상위 도메인(Top-Level Domain, TLD) 을 만들 수 있는 루트 노드의 소유자에 의존한다는 것이다.

궁금적인 목표는 새로운 TLD 들을 위한 탈중앙화된 의사결정 프로세스를 만드는 것이지만, 루트 노드는 4 of 7 멀티시그에 의해 컨트롤되고 있는데, 여러 국가에 그 키홀더들이 나누어져 있다. 그 결과, 변경을 위해서는 최소한 7명 중 4명의 키홀더가 동의해야만 합니다.

현재 이 키홀더의 목적과 목표는 커뮤니티와 합의하에 다음과 같은 작업을 하는 것입니다.

* 시스템이 일단 한번 검증되면 `.eth TLD` 의 임시 소유권을 보다 영구적인 컨트랙트로 마이그레이션하고 업그레이드한다.
* 커뮤니티는 TLD 가 필요하다고 동의하면 새로운 TLD 들의 추가를 허용한다.
* 그러한 시스템이 합의되고, 테스트되고, 구현될 때 루트 다중 서명의 소유권을 더 탈중앙화된 컨트랙트로 마이그레이션한다.
* 최상위 저장소의 모든 버그 또는 취약점을 처리하는 최후의 수단으로 사용한다.

### Resolvers

기본 ENS 컨트랙트는 이름에 메타데이터를 추가할 수 없다. 이것은 소위 **리졸버(resolver) 컨트랙트** 가 담당한다. 리졸버 컨트랙트는 앱과 관련된 스웜 주소, 앱에 지불할 주소 혹은 앱의 해시와 같은 이름에 대한 질문에 답변할 수 있는 사용자 생성 컨트랙트입니다.

## Middle Layer: The .eth Nodes

글을 쓰는 시점에서 스마트 컨트랙트에서 유일하게 등록할 수 있는 유일한 최상위 도메인은 .eth 입니다.

.eth 도메인은 경매 시스템을 통해 배포됩니다. 예약 목록이나 우선순위가 없으며, 이름을 얻는 유일한 방법은 시스템을 사용하는것입니다. 경매 시스템 코드는 상당히 복잡합니다. ENS 의 초기 개발 노력 대부분이 시스템의 이 부분에 포함되었습니다. 그러나 보관된 자금에 대한 리스크 없이 나중에 교체 및 업그레이드 할 수 있습니다.

### Vickrey auctions

이름은 수정된 비크레이 경매를 통해 배포된다. 전통적인 비크레이 경매에서는 모든 입찰자가 봉인된 입찰을 제출하고 모두가 동시에 공개합니다. 이때 가장 높은 입찰자가 경매에서 이기지만 두 번째로 높은 입찰가만 지불합니다. 그러므로 입찰자는 경매에 붙여진 이름의 실제 가치보다 더 적은 금액의 입찰을 하지 않게 됩니다. 실제 가치에 입찰하는것이 이길 확률을 높여주지만, 결국 지불하게 될 가격에는 영향을 미치지 않습니다.

블록체인에서는 일부 변경이 필요합니다.

## Top Layer: The Deeds

ENS 의 최상위 계층은 단일 목적을 지닌 또 다른 매우 단순한 컨트랙트다.

유저가 이름을 얻었을 때 그 돈은 실제로 아무데도 보내지는 않지만, 유저가 이름을 갖고 싶어 하는 기간 동안 잠겨있습니다. 이것은 보증된 바이백과 같이 동작합니다. 소유자가 더 이상 이름을 원하지 않으면 시스템으로 다시 판매하고 이더를 복구 할 수 있습니다.

단일 컨트랙트가 수백만 달러의 이더를 보유하는 것이 매우 위험하다는 것이 입증되었습니다. 그래서 ENS 는 각각의 이름에 대해 증서 컨트랙트를 생성합니다. 증서 컨트랙트는 간단합니다. 그리고 지금은 단일 계정에게만 전송되고 단일 엔티티에 의해서만 호출됩니다. 이 접근법은 버그로 인해 자금이 위험에 처할 수 있는 공격 영역을 크게 줄였습니다.

## Registering a Name

Vickrey Auction 에서 봤듯이, ENS 에 이름을 등록하는 과정은 4단계로 진행됩니다. 아래 `Example 5` 은 등록 일정을 보여주는 도표입니다.

> Example 5 - ENS timeline for registration

![image](https://user-images.githubusercontent.com/44635266/73941973-8f9ede00-4931-11ea-997d-47a7f8eec52e.png)

사용 가능한 이름을 검색하고, `ethereumbook.eth` 라는 이름에 입찰하고, 입찰가를 공개하고, 이름을 보호하기 위해 몇 가지 사용자 친화적인 인터페이스 중 하나를 사용할 것이다.

ENS 탈중앙화 어플리케이션과 상호작용할 수 있는 ENS 웹 기반 인터페이스가 많이 있습니다. 이 예제에서는 메타마스크와 함께 마이크립토(MyCrypto) 인터페이스를 지갑으로 사용합니다.

먼저 우리가 원하는 이름을 사용할 수 있는지 확인해야 합니다. 이 책을 쓰는 동안 우리는 정말로 `mastering.eth` 라는 이름을 동록하려고 했지만, `Example 6` 같이 이미 사용된 것으로 나왔다. ENS 등록은 1년밖에 되지 않기 때문에 향후 해당 이름을 보유할 수 있습니다. 그동안 `ethereumbook.eth` 를 검색해 보겠습니다.

> Example 6 - Searching for ENS names on MyCrypto.com

![image](https://user-images.githubusercontent.com/44635266/73935829-ce7a6700-4924-11ea-89dc-9eb903ff5c8d.png)

이제 이름을 사용할 수 있기 때문에 `Example 7` 을 진행하겠습니다. 메타마스크의 잠금을 해제하고 `ethereumbook.eth` 에 대한 경매를 시작하겠습니다.

> Example 7 - Starting an auction for an ENS name

![image](https://user-images.githubusercontent.com/44635266/73935832-d0442a80-4924-11ea-845f-5004509542a0.png)

`Example 8` 에서는 입찰을 해보겠습니다.

> Example 8 - Placing a bid for an ENS name

![image](https://user-images.githubusercontent.com/44635266/73935834-d1755780-4924-11ea-95a6-6d332e418729.png)

마지막으로 SUBMIT 버튼을 클릭하여 트랜잭션을 확인하겠습니다.

> Example 9 - MetaMask transaction containing your bid

![image](https://user-images.githubusercontent.com/44635266/73936041-447ece00-4925-11ea-8438-da0174caa22b.png)

이 방법으로 트랜잭션을 제출한 후 48 시간안에 입찰가를 공개하면, 우리가 요청한 입력은 우리의 이더리움 주소로 등록될 것입니다.

## Managing Your ENS Name

ENS 이름을 등록하면 ENS 관리자 같은 사용자 친화적인 인터페이스를 사용하여 ENS 이름을 관리할 수 있습니다.

검색 상자에 관리하려는 이름을 입력하고, ENS 관리자 댑이 사용자를 대신하여 이름을 관리할 수 있도록 이더리움 지갑을 잠금 해제해야 합니다.

> Example 10 - The ENS Manager web interface

![image](https://user-images.githubusercontent.com/44635266/73936039-434da100-4925-11ea-8b03-8429f9005683.png)

이 인터페이스에서 하위 도메인을 만들고, 리졸버 컨트랙트를 설정하고 각 이름을 댑 프론트엔드의 스웜 주소 같은 적절한 자원에 연결할 수 있습니다.

### Creating an ENS subdomain

먼저 경매 댑 하위 도메인을 만듭니다. 그리고 하위 도메인을 auction 이라는 이름을 붙입니다. 그래서 완전한 이름은 `auction.ethereumbook.eth` 가 될것입니다. 아래 `Example 11` 을 참고하면 됩니다.

> Example 11 - Adding the subdomain auction.ethereumbook.eth

![image](https://user-images.githubusercontent.com/44635266/73936043-46489180-4925-11ea-8750-119b3673dfc0.png)

하위 도메인을 만들고 나면 이전에 도메인 `etereumbook.eth` 를 관리했던 것처럼 검색 상자에 다른 곳의 주소록을 입력하고 관리할 수 있습니다.

### ENS Resolver

ENS 에서 이름을 확인하는 과정은 두 단계로 이루어집니다.

1. ENS 레지스트리는 해시 후 해석할 이름과 함께 호출된다. 레코드가 존재하면 레지스트리는 리졸버의 주소를 리턴한다.
2. 리졸버는 요청된 자원에 적절한 메소드를 사용하여 호출한다. 리졸버는 원하는 결과를 반환한다.

이 프로세스를 거치면 리졸버의 기능을 네이밍 시스템 자체와 분리하여 더 많은 유연성을 얻을 수 있습니다.

이름 소유자는 사용자 정의 리졸버를 사용하여 어떠한 타입이나 자원을 해석할 수 있으며, ENS 의 기능을 확장할 수도 있습니다.

경매 댑을 스웜 해시에 연결하고자 하면 아래 그림 `Example 12` 과 같이 컨텐츠 해석을 지원하는 공개 리졸버를 사용할 수 있습니다. 우리는 사용자 정의 리졸버를 코딩하거나 배포할 필요가 없습니다.

> Example 12 - Setting the default public resolver for auction.ethereumbook.eth

![image](https://user-images.githubusercontent.com/44635266/74652660-dad6ad80-51c9-11ea-8602-d823c5bde6aa.png)
 
### Resolving a Name to a Swarm Hash (Content)

`auction.ethereumbook.eth` 의 리졸버가 공개 리졸버로 설정되면, 스웜 해시를 이름의 컨텐츠로 반환하도록 설정할 수 있습니다.

> Example 13 - Setting the 'content' to return for auction.ethereumbook.eth

![image](https://user-images.githubusercontent.com/44635266/74652662-dca07100-51c9-11ea-9f43-2625c28bd05c.png)

아래 그림은 경매 댑의 전체 아키텍처입니다.

> Example 14 - Auction DApp architecture

![image](https://user-images.githubusercontent.com/44635266/74652659-d90cea00-51c9-11ea-81b9-dba0c6182f48.png)