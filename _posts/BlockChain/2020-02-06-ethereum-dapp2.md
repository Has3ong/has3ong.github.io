---
title : Ethereum Decentralized Applications (DApps) -2-
tags :
- DApps
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## A Basic DApp Example: Auction DApp

경매 댑은 사용자가 주택, 자동차 같은 고유한 자산을 나타내는 **증서(deed)** 토큰을 등록할 수 있게 합니다. 토큰이 등록되면 토큰 소유권이 경매 댑으로 이전되며 판매를 위해 리스팅할 수 있게 합니다. 경매 중에 사용자는 경매를 위해 만들어진 대화방에 참여하고, 경매가 완료되면 증서 토큰 소유권이 경매 낙찰자에게 이전됩니다.

> Example 1

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

> Example 2 - Auction DApp user interface

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

> Example 3 - Swarm gateway on localhost

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