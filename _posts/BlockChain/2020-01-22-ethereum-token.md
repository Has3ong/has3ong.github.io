---
title : Ethereum Tokens
tags :
- ERC20
- Token
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

토큰은 고대 영어에서 유래되었으며, 기호 또는 상징을 의미합니다. 

최근 블록체인에서 관리되는 토큰은 소유할 수 있고, 자산, 화폐 혹은 접근 권한 등 블록체인 기반의 추상화된 의미로 재정의 되고 있습니다.

## How Tokens Are Used

토큰의 가장 분명한 사용처는 디지털 개인 화폐입니다. 토큰은 다양한 기능을 제공하도록 프로그래밍 할 수 있습니다. 예를 들어 토큰은 어떤 자원에 대한 투표권, 접근 권한 및 소유권 기능을 동시에 수행할 수 있다. 화폐는 첫 번째 app 일 뿐이다.

**currency**

토큰은 사적인 트레이딩으로 가치가 결정되는 화폐의 한 형태로 작동할 수 없습니다.

**resource**

토큰은 공유 경제 또는 자원 공유 환경에서 획득되거나 생산된 자원을 나타낼 수 있습니다. 예를들어 storage, CPU 토큰은 네트워크상에서 공유될 수 있습니다.

**asset**

토큰은 내재적 또는 외적 유형 또는 무형 자산의 소유권을 나타낼 수 있습니다. 예를들어 금, 부동산, 자동차, 기름, 에너지, MMOG 항목 등입니다.

**access**

토큰은 접근 권한을 나타낼 수 있으며, 토큰 포럼, 회원전용 웹사이트, 호텔 객실 또는 렌터카 같은 디지털 또는 물리적 속성에 대한 접근 권한을 부여할 수 있습니다.

**equity**

토큰은 디지털 조직 또는 법인의 주주 지분을 나타낼 수 있습니다.

**voting**

토큰은 디지털 또는 법률 시스템에서 투표권을 나타낼 수 있습니다.

**collectible**

토큰은 디지털 수집물 또는 물리적인 수집물을 나타낼 수 있습니다.

**identify**

토큰은 디지털 신원 또는 법적 신원을 나타낼 수 있습니다.

**attestation**

토큰은 일부 기관이나 탈중앙화된 평판 시스템에 의한 사실 증명서 또는 인증서를 나타낼 수 있습니다.

**utility**

토큰은 서비스에 접근하거나 사용료를 지불하는 데 사용할 수 있습니다.

토큰이 위와같이 여러 기능을 포함할 수 있습니다.

### Using Tokens: Utility or Equity

현재 이더리움에 있는 거의 모든 프로젝트가 토큰을 바탕으로 시작합니다. 하지만 토큰이 실제로 필요한지는 확실하지 않습니다. 원칙적으로 토큰의 사용은 궁극적인 관리 도구나 조직 도구로 볼 수 있습니다. 현실적으로 이더리움을 포함한 블록체인 플랫폼을 사회의 기존 구조에 통합한다는 것은 지금까지 적용 가능성에 많은 한계가 있습니다.

새 프로젝트에서는 토큰의 역할을 명확히 하고 시작합니다. 대다수 프로젝트는 **utility token** 또는 **equity token** 같은 2 가지 방법 중 하나로 토큰을 사용합니다. 종종 이러한 2 가지 역할은 하나로 융합됩니다.

유틸리티 토큰은 서비스, 어플리케이션 또는 자원에 접근이 요구되는 곳에 사용됩니다. 유틸리티 토큰의 예는 공유 스토리지 같은 자원을 나타내는 토큰 혹은 소셜 미디어 네트워크 같은 서비스에 접근하는 토큰을 포함합니다.

지분 토큰은 스타트업 같은 곳의 소유권에 대한 지분을 나타냅니다. 지분 토큰은 배당금 및 이익 분배를 위한 무의결권 주식으로 제한되거나, 탈중앙화된 자율 조직의 투표 지분으로 확장될 수도 있는데, 여기서 플랫폼의 관리는 토큰 보유자들의 투표에 기반을 둔 상당히 복잡한 거버넌스 시스템을 통해 이루어집니다.

## Tokens on Ethereum

첫 번째 블록체인 화폐인 비트코인은 그 자체가 토큰입니다. 이더리움 이전에 많은 토큰 플랫폼이 비트코인 및 기타 암호화폐에서 개발되었습니다. 하지만 이더리움에서 첫 번째 토큰 표준이 소개되고 나서 토큰이 폭발적으로 증가했습니다.

비탈릭 부테린은 이더리움 같은 범용적이고 프로그래밍 가능한 블록체인의 가장 명확하고 유용한 어플리케이션의 하나로 토큰을 제안했습니다.

토큰은 이더와 다릅니다. 왜냐하면 이더리움 프로토콜은 토큰에 대해 아무것도 모르기 때문입니다. 이더 전송은 이더리움 플롯팸의 본질적인 동작이지만, 토큰을 보내거나 소유하는 것은 아닙니다. 이더리움 계정의 이더 잔액은 프로토콜 수준에서 처리되는 반면, 이더리움 계정의 토큰 잔액은 스마트 컨트랙트 수준에서 처리됩니다.

이더리움에서 새로운 토큰을 만드려면 새로운 스마트 컨트랙트를 만들어야 합니다. 배포된 스마트 컨트랙트는 소유권, 이전 및 접근 권한을 포함한 모든 것을 처리합니다. 워하는 방법대로 모든 필요한 작업을 수행하도록 스마트 컨트랙트를 작성할 수 있지만, 기존 표준을 따르는 것이 가장 바람직합니다.

이번 포스트에서는 토큰의 표준을 알아보고 장단점을 알아보겠습니다.

### The ERC20 Token Standard

첫 번째 표준은 ERC(Ethereum Request for Comments) 로 발표한 표준입니다. Github 이슈번호 20이 자동으로 할당되어 **ERC20 토큰** 이라는 이름이 되었습니다. 대다수의 토큰은 현재 ERC20 표준을 기반으로 합니다. 의견 수렴을 통하여 ERC20 요청은 결국 **Ethereum Improvement Proposal 20 (EIP-20)** 이 되었지만 여전히 ERC20 으로 언급됩니다.

ERC20 은 **대체 가능한 토큰(fungible token)** 의 표준으로, ERC20 토큰의 다른 단위가 상호 교환이 가능하고 고유한 특성이 없음을 의미합니다.

### ERC20 required functions and events

**totalSupply**

현재 존재하는 토큰의 전체 개수를 리턴합니다. ERC20 토큰에는 고정 또는 가변적인 공급량이 있을 수 있습니다.

**balanceOf**

주소가 주어지면 해당 주소의 토큰 잔액을 반환 합니다.

**transfer**

주소와 금액이 주어지면 해당 주소로 토큰의 양을 전송합니다. 전송을 실행하는 주소의 잔액에서 전송을 실행합니다.

**transferFrom**

보낸 사람, 받는 사람 및 금액이 주어지면 한 계정에서 다른 계정으로 토큰을 전송합니다. approve 와 함게 조합하여 사용합니다.

**approve**

수취인 주소와 금액이 주어지면 그 주소가 승인을 한 계정에서 최대 금액까지 여러 번 송금할 수 있도록 승인합니다.

**allowance**

소유자 주소와 지출자 주소가 주어지면, 지출자가 출금할 수 있도록 소유자가 승인한 잔액을 리턴합니다.

**Transfer**

전송이 성공하면 이벤트가 트리거 됩니다.

**Approval**

approve 를 성공적으로 호출하면 이벤트가 기록됩니다.

### ERC20 optional functions

**name**

사람이 읽을 수 있는 토큰의 이름을 반환

**symbol**

사람이 읽을 수 있는 기호를 반환

**decimals**

토큰 양을 나눌 수 있는 소수 자릿수를 반환합니다. 예를 들어, decimals 가 2이면 토큰 양을 100으로 나눠 표현합니다.

### The ERC20 interface defined in Solidity

아래는 솔리디티에서 ERC20 인터페이스 사양 입니다.

```java
contract ERC20 {
   function totalSupply() constant returns (uint theTotalSupply);
   function balanceOf(address _owner) constant returns (uint balance);
   function transfer(address _to, uint _value) returns (bool success);
   function transferFrom(address _from, address _to, uint _value) returns
      (bool success);
   function approve(address _spender, uint _value) returns (bool success);
   function allowance(address _owner, address _spender) constant returns
      (uint remaining);
   event Transfer(address indexed _from, address indexed _to, uint _value);
   event Approval(address indexed _owner, address indexed _spender, uint _value);
}
```

### ERC20 data structures

ERC20 구현을 살펴보면 2개의 데이터 구조를 포함하고 있음을 알게 됩니다.

하나는 잔고를 추적하고, 나머지 하나는 허용량을 추적합니다. 솔리디티에서는 **데이터 매핑(data mapping)** 으로 구현됩니다.

첫 번째 데이터 매핑은 소유자 별 토큰 잔액을 내부 테이블로 구현합니다. 이렇게 하면 토큰 컨트랙트에서 토큰을 소유한 사람을 추적할 수 있습니다. 각 이체는 하나의 잔액에서 공제되고 다른 잔고에 추가됩니다.

```java
mapping(address => uint256) balances;
```

두 번째 데이터 구조는 허용량의 데이터 매핑입니다. 다음 절에서 알겠지만, ERC20 토큰을 사용하면 토큰 소유자가 권한을 위임자에게 위임하여 소유자의 잔액에서 특정 금액을 지출할 수 있습니다. ERC20 컨트랙트는 기본 키가 토큰 소유자의 주소이며, 지출자 주소와 허용 한도에 매핑되는 2차원 매핑으로 허용량을 추적합니다.

```java
mapping (address => mapping (address => uint256)) public allowed;
```

### ERC20 workflows: "transfer" and "approve & transferFrom"

ERC20 토큰 표준에는 2 가지 transfer 함수가 있습니다.

첫 번째는 transfer 함수를 사용하는 단일 트랜잭션 워크플로우 입니다. 이 워크플로우는 지갑에서 다른 지갑으로 토큰을 보내는데 사용하는 워크플로우 입니다.

두 번째 워크플로우는 approve 후 transFrom 을 사용하는 두 단계 트랜잭션 워크플로우 입니다. 이 워크플로우는 토큰 소유자가 제어를 다른 주소에 위임할 수 있게 해줍니다. 이것은 제어를 토큰 배포 컨트랙트에 위임하는데 가장 많이 사용되지만 거래소에서도 사용할 수 있습니다.

예를들어 회사가 ICO를 위해 토큰을 판매하는 경우, 특정 양의 토큰을 배포하기 위헤 crowdsale 컨트랙트 주소를 approve 할 수 있습니다. 크라우드 세일 컨트랙트는 아래 `Example 1` 에 나와있는것처럼 토큰을 구매한 각 구매자에게 토큰 컨트랙트의 소유자 밸런스에게 송금합니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/73136480-707e9180-4091-11ea-8839-438c3e580d5a.png)

approve & transferFrom 워크 플로우를 위해 2개의 트랜잭션이 필요합니다.

Alice 가 Bob 같은 구매자에게 AliceCoin 토큰의 50% 를 판매하도록 AliceICO 컨트랙트를 허용한다고 가정하겠습니다.

먼저 Alice 는 AliceCoin ERC20 컨트랙트를 런칭하여 모든 AliceCoin 을 자신의 주소로 발급합니다. 다음, 앨리스는 이더용 토큰을 판매 할 수 있는 AliceICO 컨트랙트를 시작합니다.

그 후 Alice 는 워크플로우에서 approve 와 transferFrom 을 시작합니다. 그녀는 인수를 AliceICO 의 컨트랙트 주소와 totalSupply 의 50% 해서 approve 를 호출하는 트랜잭션을 AliceCoin 컨트랙트로 보냅니다. 이것은 Approval 이벤트를 트리거합니다. 이제 AliceCoin 컨트랙트는 AliceCoin 을 판매할 수 있습니다.

AliceICO 컨트랙트가 Bob 으로부터 이더를 받으면, Bob 에게 AliceCoin 을 보내야 합니다. AliceICO 컨트랙트에는 AliceCoin 과 이더 간에 환율이 있습니다. AliceICO 컨트랙트를 만들 때 앨리스가 설정한 환율은 밥이 AliceICO 컨트랙트로 보낸 이더 양에 대해 얼마나 많은 토큰을 받을지 결정합니다.

AliceICO 컨트랙트에서 AliceCoin transferFrom 함수를 호출하면 보낸 사람으로 Alice 의 주소를 설정하고, 받는 사람으로 BOB 의 주소를 설정합니다. 그리고 환율을 사용하여 value 필드에서 얼마나 많은 AliceCoin 을 Bob 에게 전송할지 결정합니다.

AliceCoin 컨트랙트는 Alice 주소에서 Bob 의 주소로 잔액을 전송하고 Transfer 이벤트를 트리거 합니다. AliceICO 컨트랙트는 Alice 가 설정한 승인 한도를 초과하지 않는 무제한으로 transferFrom 을 호출할 수 있습니다. AliceICO 컨트랙트는 allowance 함수를 호출하여 판매할 수 있는 AliceCoin 토큰의 수를 관리할 수 있습니다.

### Launching Our Own ERC20 Token

트러플 프레임워크를 이용하여 자체 토큰을 만들고 실행해보겠습니다.

*Mastering Ethereum Token* 토큰을 *MET* 라고 부르겠습니다.

> 예제는 [Github](https://github.com/ethereumbook/ethereumbook/tree/develop/code/truffle/METoken) 저장소에서 확인할 수 있습니다.

우선, 트러플 프로젝트 디렉토리를 생성하고 초기화합니다. 4개의 명령을 실행하고 모든 질문에 대해 기본 설정되어 있는 답을 합니다.

```shell
$ mkdir METoken
$ cd METoken
METoken $ truffle init
METoken $ npm init
```

하게되면 아래와같은 디렉토리 구조를 가지게됩니다.

```shell
METoken/
+---- contracts
|   `---- Migrations.sol
+---- migrations
|   `---- 1_initial_migration.js
+---- package.json
+---- test
+---- truffle-config.js
`---- truffle.js
```

`truffle.js` 와 `truffle-config.js` 설정파일을 편집하여 트러플 환경을 설정하거나, 환경설정 파일을 [Github](https://github.com/ethereumbook/ethereumbook/blob/develop/code/truffle/METoken/truffle-config.js) 에서 복사하면됩니다.

그 후에 디렉토리는 다음과 같을것입니다.

```shell
METoken/
+---- contracts
|   `---- Migrations.sol
+---- migrations
|   `---- 1_initial_migration.js
+---- package.json
+---- test
+---- truffle-config.js
+---- truffle.js
`---- .env *new file*
```

위 예제에서 몇 가지 중요한 보안 검사를 구현하고 확장하기 쉬운 오픈제플린 라이브러리를 가져옵니다.

```shell
$ npm install openzeppelin-solidity@1.12.0

+ openzeppelin-solidity@1.12.0
added 1 package from 1 contributor and audited 2381 packages in 4.074s
```

`openzeppelin-solidity` 패키지는 `node_modules` 아래 약 250 개의 파일을 추가할것이고, 오픈제플린 라이브러리에는 ERC20 토큰 이상이 포함되어 있으나, 일부만 사용할것입니다.

다음으로 토큰 컨트랙트를 작성합니다. 새파일 `METoken.sol` 을 작성하고 [Github]() 에 예제 코드를 복사합니다.

> Example - METoken.sol: A Solidity contract implementing an ERC20 token

```java
pragma solidity ^0.4.21;

import 'openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol';

contract METoken is StandardToken {
    string public constant name = 'Mastering Ethereum Token';
    string public constant symbol = 'MET';
    uint8 public constant decimals = 2;
    uint constant _initial_supply = 2100000000;

    function METoken() public {
        totalSupply_ = _initial_supply;
        balances[msg.sender] = _initial_supply;
        emit Transfer(address(0), msg.sender, _initial_supply);
    }
}
```

여기서는 상수 변수인 `name`, `symbol`, `decimals` 를 정의합니다. 2100 만 개의 토큰으로 설정된 `_initial_supply` 변수도 정의합니다. 세분화된 2 개의 십진수는 총 21 억 개의 단위를 제공합니다. 컨트랙트의 초기화 함수에서 `totalSupply` 를 `_initial_supply` 와 같게 설정하고 모두 할당합니다. `_initial_supply` 를 `METoken` 컨트랙트를 생성하는 계정의 잔액에 추가합니다.

이제 **truffle** 을 사용하여 METoken 코드를 컴파일합니다.

```shell
$ truffle compile
Compiling ./contracts/METoken.sol...
Compiling ./contracts/Migrations.sol...
Compiling openzeppelin-solidity/contracts/math/SafeMath.sol...
Compiling openzeppelin-solidity/contracts/token/ERC20/BasicToken.sol...
Compiling openzeppelin-solidity/contracts/token/ERC20/ERC20.sol...
Compiling openzeppelin-solidity/contracts/token/ERC20/ERC20Basic.sol...
Compiling openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol...
```

**truffle** 은 보다시피 오픈제플린 라이브러리에서 필요한 **dependencies** 를 포함하고 해당 컨트랙트를 컴파일합니다.

`METoken` 컨트랙트를 배포하기 위해 **migrate** 스크립트를 설정하겠습니다. `METoken/migrations` 폴더에 `2_deploy_contracts.js` 라는 새 파일을 만들고 [Github]() 에 있는 예제의 내용을 복사합니다.

```java
var METoken = artifacts.require("METoken");

module.exports = function(deployer) {
  // Deploy the METoken contract as our only task
  deployer.deploy(METoken);
};
```

이더리움 테스트 네트워크 중 하나에 배포하기 전에 로컬 블록체인을 시작하여 모든것을 테스트 합니다. `ganache-cli` 커맨드 라인 또는 GUI 에서 ganache 블록체인을 시작합니다.

ganache 가 시작되면 METoken 컨트랙트를 배포하고 모든 것이 예상대로 작동하는지 확인할 수 있습니다.

```shell
$ truffle migrate --network ganache
Using network 'ganache'.

Running migration: 1_initial_migration.js
  Deploying Migrations...
  ... 0xb2e90a056dc6ad8e654683921fc613c796a03b89df6760ec1db1084ea4a084eb
  Migrations: 0x8cdaf0cd259887258bc13a92c0a6da92698644c0
Saving successful migration to network...
  ... 0xd7bc86d31bee32fa3988f1c1eabce403a1b5d570340a3a9cdba53a472ee8c956
Saving artifacts...
Running migration: 2_deploy_contracts.js
  Deploying METoken...
  ... 0xbe9290d59678b412e60ed6aefedb17364f4ad2977cfb2076b9b8ad415c5dc9f0
  METoken: 0x345ca3e014aaf5dca488057592ee47305d9b3e10
Saving successful migration to network...
  ... 0xf36163615f41ef7ed8f4a8f192149a0bf633fe1a2398ce001bf44c43dc7bdda0
Saving artifacts...
```

ganache 콘솔에서 `Example 2` 과 같이 배포를 통해 4 가지 새로운 트랜잭션이 생성된 걸 확인할 수 있습니다.

> Example 2 - METoken deployment on ganache

![image](https://user-images.githubusercontent.com/44635266/73257609-6e3e4380-4207-11ea-81f5-0eb41832da6d.png)

### Interacting with METoken using the Truffle console

트러플 콘솔을 사용하여 ganache 블록체인상에 있는 우리의 컨트랙트와 상호작용을 할 수 있습니다. 이 콘솔은 트러플 환경과 web3 를 통해 블록체인에 접근할 수 있는 양방향 자바스크립트 환경입니다. 여기서는 트러플 콘솔을 ganache 블록체인에 연결합니다.

```shell
$ truffle console --network ganache
truffle(ganache)>
```

`truffle(ganache)>` 프롬프트는 우리가 ganache 블록체인에 연결되어 있으며 명령을 입력할 준비가 되어있음을 보여줍니다. 트러플 콘솔은 모든 truffle 명령을 지원하므로 콘솔에서 compile 과 migrate 를 할 수 있습니다. `METoken` 컨트랙트는 트러플 환경에서 자바스크립트 객체로 존재합니다. 프롬프트에서 `METoken` 을 입력하면 전체 컨트랙트 정의가 덤프될것입니다.

```shell
truffle(ganache)> METoken
{ [Function: TruffleContract]
  _static_methods:

[...]

currentProvider:
 HttpProvider {
   host: 'http://localhost:7545',
   timeout: 0,
   user: undefined,
   password: undefined,
   headers: undefined,
   send: [Function],
   sendAsync: [Function],
   _alreadyWrapped: true },
network_id: '5777' }
```

또한, `METoken` 의 객체는 컨트랙트 주소와 같은 여러 속성을 표시합니다.

```shell
truffle(ganache)> METoken.address
'0x345ca3e014aaf5dca488057592ee47305d9b3e10'
```

배포된 컨트랙트와 상호작용하려는 경우 자바스크립트 promise 형식으로 비동기 호출을 해야합니다. `deployed` 함수를 사용하여 컨트랙트 인스턴스를 가져온 후에 `totalSupply` 함수를 호출합니다.

```shell
truffle(ganache)> METoken.deployed().then(instance => instance.totalSupply())
BigNumber { s: 1, e: 9, c: [ 2100000000 ] }
```

다음으로 ganache 가 만든 계정을 사용하여 `METoken` 잔액을 확인하고 `METoken` 을 다른 주소로 보냅니다. 먼저 계정 주소를 알아보겠습니다.

```shell
truffle(ganache)> let accounts
undefined
truffle(ganache)> web3.eth.getAccounts((err,res) => { accounts = res })
undefined
truffle(ganache)> accounts[0]
'0x627306090abab3a6e1400e9345bc60c78a8bef57'
```

accounts 리스트에는 이제 ganache 가 만든 모든 계정이 포함되며, `account[0]` 은 `METoken` 컨트랙트를 배포한 계정입니다. `METoken` 생성자는 생성된 주소에 전체 토큰을 제공하기 때문에 `METoken` 잔액을 가져야 합니다. 확인해보겠습니다.

```shell
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(accounts[0]).then(console.log) })
undefined
truffle(ganache)> BigNumber { s: 1, e: 9, c: [ 2100000000 ] }
```

마지막으로, 컨트랙트의 `transfer` 함수를 호출하여 `account[0]` 에서 `account[1]` 로 1000.00 `METoken` 을 전송해보겠습니다.

```shell
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.transfer(accounts[1], 100000) })
undefined
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(accounts[0]).then(console.log) })
undefined
truffle(ganache)> BigNumber { s: 1, e: 9, c: [ 2099900000 ] }
undefined
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(accounts[1]).then(console.log) })
undefined
truffle(ganache)> BigNumber { s: 1, e: 5, c: [ 100000 ] }
```

확인하면 계정의 잔액이 바뀐걸 볼 수 있습니다.

> Example 3 - METoken transfer on ganache

![image](https://user-images.githubusercontent.com/44635266/73258408-f709af00-4208-11ea-9a5a-fa216ae8a311.png)

### Sending ERC20 tokens to contract addresses

지금까지 ERC20 토큰을 설정하고 하나의 계정에서 다른 계정으로 토큰을 전송했습니다. 데모에 사용한 모든 계정은 EOA 으로 컨트랙트가 아닌 개인키로 제어가 됩니다. MET 를 컨트랙트 주소로 보내면 어떻게 되는지 알아보겠습니다.

먼저 테스트 환경에 또 다른 컨트랙트를 배포해 보겠습니다.

아래 디렉토리와 같이 `METoken` 프로젝트에 추가해서 만들면됩니다.

```shell
METoken/
+---- contracts
|   +---- Faucet.sol
|   +---- METoken.sol
|   `---- Migrations.sol
```

`METoken` 과는 별도로 `Faucet` 을 배포하기 위해 migration 을 추가 하겠습니다.

```shell
var Faucet = artifacts.require("Faucet");

module.exports = function(deployer) {
  // Deploy the Faucet contract as our only task
  deployer.deploy(Faucet);
};
```

트러플 콘솔에서 컨트랙트를 컴파일하고 migration 하겠습니다.

```shell
$ truffle console --network ganache
truffle(ganache)> compile
Compiling ./contracts/Faucet.sol...
Writing artifacts to ./build/contracts

truffle(ganache)> migrate
Using network 'ganache'.

Running migration: 1_initial_migration.js
  Deploying Migrations...
  ... 0x89f6a7bd2a596829c60a483ec99665c7af71e68c77a417fab503c394fcd7a0c9
  Migrations: 0xa1ccce36fb823810e729dce293b75f40fb6ea9c9
Saving artifacts...
Running migration: 2_deploy_contracts.js
  Replacing METoken...
  ... 0x28d0da26f48765f67e133e99dd275fac6a25fdfec6594060fd1a0e09a99b44ba
  METoken: 0x7d6bf9d5914d37bcba9d46df7107e71c59f3791f
Saving artifacts...
Running migration: 3_deploy_faucet.js
  Deploying Faucet...
  ... 0x6fbf283bcc97d7c52d92fd91f6ac02d565f5fded483a6a0f824f66edc6fa90c3
  Faucet: 0xb18a42e9468f7f1342fa3c329ec339f254bc7524
Saving artifacts...
```

이제 `Faucet` 컨트랙트 일부 MET 를 보내보겠습니다.

```shell
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.transfer(Faucet.address, 100000) })
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(Faucet.address).then(console.log)})
truffle(ganache)> BigNumber { s: 1, e: 5, c: [ 100000 ] }
```

`Faucet` 컨트랙트에 1,000 MET 를 송금했습니다. 이제 어떻게 출금하는지 보겠습니다.

`Faucet.sol` 은 단순한 컨트랙트 입니다. **이더** 를 출금하기 위한 `withdraw` 함수 하나만 있으면 됩니다. MET 또는 ERC20 토큰을 출근할 수 있는 함수는 없습니다. `withdraw` 를 사용하면 이더를 보내려고 시도하지만, Faucet 이 아직 이더 잔액이 없으므로 실패합니다.

`METoken` 컨트랙트는 `Faucet` 잔액이 있음을 알지만, 컨트랙트 잔액을 이체할 수 있는 유일한 방법은 컨트랙트 주소에서 `transfer` 함수가 호출되는 경우입니다. 어떻게든 `Faucet` 컨트랙트가 `METoken` 의 `transfer` 함수를 호출하도록 해야 합니다.

ERC20 토큰 사용자가 실수로 교환에서 토큰을 잃어버리는 경우 중 하나는 거래소나 다른 서비스로 전송하려고 할 때입니다. 거래소의 웹사이트에서 이더리움 주소를 복사하여 단순히 토큰을 보낼 수 있다고 생각하지만, 많은 거래소는 실제 수신 주소가 컨트랙트인 주소를 게시합니다. 이 컨트랙트는 ERC20 토큰이 아닌 이더를 받기 위한 용도로 사용되며, 대부분 **cold storage** 이거나 다른 중앙 집중식 지갑으로 송금된 모든 자금으로 옮깁니다. 이러한 경우로 많은 토큰이 분실됩니다.

### Demonstrating the “approve & transferFrom” workflow

`Faucet` 컨트랙트는 ERC20 토큰을 처리할 수 없습니다. `transfer` 함수를 사용하여 토큰을 보내면 토큰의 손실됩니다. 이제 컨트랙트를 다시 작성하고 ERC20 토큰을 처리하도록 해보겠습니다.

이 예제는 truffle 과 npm 을 초기화하고 프로젝트 디렉터리의 사본을 만들며, 오픈제플린 디펜던시들을 설치한 다음, `METoken.sol` 컨트랙트를 복사하겠습니다.

새로운 `Faucet` 컨트랙트인 `METoken.sol` 은 아래와 같습니다.

> Example - METFaucet.sol: A faucet for METoken

```java
// Version of Solidity compiler this program was written for
pragma solidity ^0.4.19;

import 'openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol';


// A faucet for ERC20 token MET
contract METFaucet {

	StandardToken public METoken;
	address public METOwner;

	// METFaucet constructor, provide the address of METoken contract and
	// the owner address we will be approved to transferFrom
	function METFaucet(address _METoken, address _METOwner) public {

		// Initialize the METoken from the address provided
		METoken = StandardToken(_METoken);
		METOwner = _METOwner;
	}

	function withdraw(uint withdraw_amount) public {

    	// Limit withdrawal amount to 10 MET
    	require(withdraw_amount <= 1000);

		// Use the transferFrom function of METoken
		METoken.transferFrom(METOwner, msg.sender, withdraw_amount);
    }

	// REJECT any incoming ether
	function () external payable { revert(); }

}
```

`transferFrom` 함수를 사용하기 위해 2개의 추가 변수가 필요합니다. 하나는 배포된 `METoken` 컨트래긑의 주소를 보유하며, 다른 하나는 `Faucet` 출금을 승인할 MET 소유자의 주소를 보유합니다. `METFaucet` 컨트랙트는 `METoken.transferFrom` 을 호출하고 MET 를 소유자로부터 `Faucet` 출금 요청이 발생한 주소로 이동하도록 지시합니다.

다음 두 변수를 선언합니다.

```java
StandardToken public METoken;
address public METOwner;
```

`Facuet` 이 `METoken` 과 `METOwner` 에대해 올바른 주소로 초기화해야 하기 때문에 사용자 정의 생성자를 선언해야 합니다.

```java
// METFaucet constructor - provide the address of the METoken contract and
// the owner address we will be approved to transferFrom
function METFaucet(address _METoken, address _METOwner) public {

	// Initialize the METoken from the address provided
	METoken = StandardToken(_METoken);
	METOwner = _METOwner;
}
```

다음은 `withdraw` 함수입니다. `transfer` 를 호출하는 대신, `METFaucet` 은 `METoken` 에서 `transferFrom` 함수를 사용하고   `METoken` 에게 MET 를 `Faucet` 수신자에게 전송하도록 요청합니다.

```java
// Use the transferFrom function of METoken
METoken.transferFrom(METOwner, msg.sender, withdraw_amount);
```

마지막으로 `Faucet` 이 더 이상 이더를 보내지 않으므로 어느 누구도 `METFaucet` 에 이더를 보내지 못하게 해야합니다. 왜냐하면 이더가 잠기게 되는것을 원치 않기 때문입니다.

```java
// REJECT any incoming ether
function () external payable { revert(); }
```

`METFaucet.sol` 코드가 준비되면 migration script 를 수정하여 배포합니다. `METFaucet` 은 `METoken` 의 주소에 따라 다르므로 migration script 는 좀 더 복잡해집니다. javascript promise 를 사용하여 두 컨트랙트를 순차적으로 배포합니다. 다음과 같이 `2_deploy_contract.js` 를 만듭니다.

```java
var METoken = artifacts.require("METoken");
var METFaucet = artifacts.require("METFaucet");
var owner = web3.eth.accounts[0];

module.exports = function(deployer) {

	// Deploy the METoken contract first
	deployer.deploy(METoken, {from: owner}).then(function() {
		// Then deploy METFaucet and pass the address of METoken and the
		// address of the owner of all the MET who will approve METFaucet
		return deployer.deploy(METFaucet, METoken.address, owner);
  	});
}
```

이제 트러플에서 모두 테스트할 수 있습니다. migrate 를 사용하여 컨트랙트를 배포합니다. 배포가 되면 처음으로 모든 MET 를 `web3,eth.accounts[0]` 에 할당합니다.

다음으로 `METoken` 의 `approve` 함수를 호출하여 `web3.eth.accounts[0]` 을 대신하여 최대 1,000 MET 까지 전송하도록 `METFaucet` 을 승인합니다.

마지막으로 `Faucet` 을 테스트하기 위해 `web3.eth.accounts[1]` 에서 `METFaucet.withdraw` 를 호출하고 10 MET 를 출금합니다.

```shell
$ truffle console --network ganache
truffle(ganache)> migrate
Using network 'ganache'.

Running migration: 1_initial_migration.js
  Deploying Migrations...
  ... 0x79352b43e18cc46b023a779e9a0d16b30f127bfa40266c02f9871d63c26542c7
  Migrations: 0xaa588d3737b611bafd7bd713445b314bd453a5c8
Saving artifacts...
Running migration: 2_deploy_contracts.js
  Replacing METoken...
  ... 0xc42a57f22cddf95f6f8c19d794c8af3b2491f568b38b96fef15b13b6e8bfff21
  METoken: 0xf204a4ef082f5c04bb89f7d5e6568b796096735a
  Replacing METFaucet...
  ... 0xd9615cae2fa4f1e8a377de87f86162832cf4d31098779e6e00df1ae7f1b7f864
  METFaucet: 0x75c35c980c0d37ef46df04d31a140b65503c0eed
Saving artifacts...
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.approve(METFaucet.address, 100000) })
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(web3.eth.accounts[1]).then(console.log) })
truffle(ganache)> BigNumber { s: 1, e: 0, c: [ 0 ] }
truffle(ganache)> METFaucet.deployed().then(instance =>
                  { instance.withdraw(1000, {from:web3.eth.accounts[1]}) } )
truffle(ganache)> METoken.deployed().then(instance =>
                  { instance.balanceOf(web3.eth.accounts[1]).then(console.log) })
truffle(ganache)> BigNumber { s: 1, e: 3, c: [ 1000 ] }
```

결과를 보면 워크플로우에서 `approve` 및 `transferFrom` 을 사용하여 한 컨트랙트에서 다른 토큰에 정의된 토콘을 전송할 수 있도록 승인할 수 있습니다. 제대로 사용하면 ERC20 토큰을 EOA 및 기타 컨트랙트에서 사용할 수 있습니다.

그러나 ERC20 토큰을 올바르게 관리하는 데 드는 부담은 사용자 인터페이스로 넘겨집니다. 만약 사용자가 ERC20 토큰을 컨트랙트 주소로 전송하려고 시도하는데, 이 컨트랙트가 ERC20 토큰을 받을 준비가 되어 있지 않으면 토큰이 손실됩니다.

### Issues with ERC20 Tokens

ERC20 토큰 표준의 채택으로 인해 수천 개의 토큰이 출시되었습니다. 하지만 그에따른 몇가지 문제도 발생했습니다.

ERC20 토큰의 문제중 하나는 토큰과 이더 자체 사이의 미묘한 차이가 관련있습니다. 이더는 수신자의 주소를 목적지로 가지고 있는 트랜잭션에 의해 전송이 일어나는 반면, 토큰 전송은 **특정한 토큰 컨트랙트 상태(specific token contract state)** 안에서 일어나고 수신자의 주소가 아닌 토큰 컨트랙트를 목적지로 합니다.

토큰 컨트랙트는 밸런스를 관리하고 이벤트를 발생시킵니다. 토큰 전송에서 트랜잭션이 토큰 수신자에게 실제로 보내는 것이 아니라 받는 사람의 주소가 토큰 컨트랙트 자체의 맵에 추가됩니다.

이더를 주소로 보내는 트랜잭션은 주소의 상태를 변경합니다. 하지만, 토큰을 주소로 전송하는 트랜잭션은 토큰 컨트랙트의 상태를 변경하지 않습니다. ERC20 토큰을 지원하는 지갑조차 사용자가 토큰 컨트랙트를 명시적으로 추가하지 않는 한 토큰 잔액을 인식하지 못합니다.

또한, 토큰은 이더와 같은 방식으로 동작하지 않습니다. 이더는 `send` 함수에 의해 보내지며, 컨트랙트에 있는 `payable` 함수 또는 외부 소유 주소에 의해 수신됩니다. 토큰은 `transfer` 또는 `approve`, `transferFrom` 을 사용하여 전송되며 수령인 컨트랙트에서 `payable` 함수를 트리거하지 않습니다.

마지막으로 이더를 보내거나 이더리움 컨트랙트를 사용하려면 가스를 지급하기 위해 이더가 필요한데, 토큰을 보내도 이더가 필요합니다. 트랜잭션의 가스를 토큰으로 지급할 수 없으며, 토큰 컨트랙트는 가스를 지급할 수 없습니다.

이러한 문제는 ERC20 토큰에만 해당이 됩니다. 그래서 다양한 표준 제안을 알아보겠습니다.

### ERC223: A Proposed Token Contract Interface Standard

ERC223 제안은 목적지 주소가 컨트랙트인지 아닌지 여부를 감지함으로써 실수로 토큰을 컨트랙트로 전송하는 문제를 해결하려고 합니다. ERC223 에서는 토큰을 받도록 설계된 컨트랙트에 `tokenFallback` 이라는 함수를 구현해야 합니다.

전송 목적지가 컨트랙트인데, 그 컨트랙트에 토큰에 대한 자원이 없는 경우 전송이 실패합니다.

대상 주소가 컨트랙트인지 여부를 감지하기 위해 ERC223 표준 구현은 특별한 방법으로 인라인 바이트 코드의 작은 세그먼트를 사용합니다.

```java
function isContract(address _addr) private view returns (bool is_contract) {
  uint length;
    assembly {
       // retrieve the size of the code on target address; this needs assembly
       length := extcodesize(_addr)
    }
    return (length>0);
}
```

ERC223 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC223Token {
  uint public totalSupply;
  function balanceOf(address who) public view returns (uint);

  function name() public view returns (string _name);
  function symbol() public view returns (string _symbol);
  function decimals() public view returns (uint8 _decimals);
  function totalSupply() public view returns (uint256 _supply);

  function transfer(address to, uint value) public returns (bool ok);
  function transfer(address to, uint value, bytes data) public returns (bool ok);
  function transfer(address to, uint value, bytes data, string custom_fallback)
      public returns (bool ok);

  event Transfer(address indexed from, address indexed to, uint value,
                 bytes indexed data);
}
```

### ERC777: A Proposed Token Contract Interface Standard

ERC777 토큰에 대한 제안은 [ERC777](https://eips.ethereum.org/EIPS/eip-777)에 있습니다. 이 제안은 다음과 같은 목표가 있습니다.

* ERC20 호환 인터페이스 제공
* `send` 함수를 사용하여 토큰을 전송
* 토큰 컨트랙트 등록을 위해 ERC820 과 호환 가능
* 컨트랙트 주소가 토큰을 전송하기 전에 어느 토큰을 전송할 수 있는가를 `takesToSend` 함수를 통해 컨트롤
* 수신자의 `tokensReceived` 함수를 호출하여 컨트랙트 및 주소에 토큰의 수신 사실을 통지할 수 있게 하고 컨트랙트에 `tokensReceived` 함수를 제공하도록 요구함으로써 컨트랙트가 잠길 확률을 줄임
* 기존 컨트랙트가 `tokensToSend` 및 `tokensReceived` 함수에 대해 프록시 컨트랙트를 사용하도록 허용
* 컨트랙트로 보내거나 EOA 로 보내거나와 같은 방식으로 작동
* 토큰 발행 및 소각을 위한 특정 이벤트 제
* 토큰 보유자 대신 토큰을 이동시키는 운영자 허용
* `userData` 및 `operatorData` 필드에서 토큰 전송 트랜잭션에 대한 메타데이터 제공

ERC777 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC777Token {
    function name() public constant returns (string);
    function symbol() public constant returns (string);
    function totalSupply() public constant returns (uint256);
    function granularity() public constant returns (uint256);
    function balanceOf(address owner) public constant returns (uint256);

    function send(address to, uint256 amount, bytes userData) public;

    function authorizeOperator(address operator) public;
    function revokeOperator(address operator) public;
    function isOperatorFor(address operator, address tokenHolder)
        public constant returns (bool);
    function operatorSend(address from, address to, uint256 amount,
                          bytes userData,bytes operatorData) public;

    event Sent(address indexed operator, address indexed from,
               address indexed to, uint256 amount, bytes userData,
               bytes operatorData);
    event Minted(address indexed operator, address indexed to,
                 uint256 amount, bytes operatorData);
    event Burned(address indexed operator, address indexed from,
                 uint256 amount, bytes userData, bytes operatorData);
    event AuthorizedOperator(address indexed operator,
                             address indexed tokenHolder);
    event RevokedOperator(address indexed operator, address indexed tokenHolder);
}
```

### ERC777 hooks

ERC777 토큰 발신자 후크 사양은 다음과 같습니다.

```java
interface ERC777TokensSender {
    function tokensToSend(address operator, address from, address to,
                          uint value, bytes userData, bytes operatorData) public;
}
```

이 인터페이스의 구현은 토큰 지불 통지, 처리 또는 예방을 워하는 모든 주소에 필요합니다. 이 인터페이스를 구현하는 컨트랙트의 주소는 컨트랙트 자체 또는 다른 주소용 인터페이스를 구현하는것과 관계없이 ERC820 을 등록해야 합니다.

ERC777 토큰 수신자 후크 사양은 다음과 같습니다.

```java
interface ERC777TokensRecipient {
  function tokensReceived(
     address operator, address from, address to,
    uint amount, bytes userData, bytes operatorData
  ) public;
}
```

위 인터페이스의 구현은 토큰의 수신을 통지, 처리 거부하려는 모든 주소에 필요합니다. 토큰 발신자 인터페이스와 마찬가지로 동일한 논리 및 요구사항이 토큰 수신자 인터페이스에도 적용되어야 합니다. 즉, 수신자 컨트랙트가 토큰 잠김을 막기 위해 사용합니다. 수신자 컨트랙트가 인터페이스를 구현하는 주소를 등록하지 않으면, 토큰 전송이 실패합니다.

### ERC721: Non-fungible Token (Deed) Standard

지금까지 살펴본 토큰 표준은 **대체 가능한(fungible)** 입니다.

[ERC721 제안](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md) 은 **증서(deed)** 로 알려진 **대체할 수 없는(non-fungible)** 토큰에 표준을 위한것입니다.

대체할 수 없는 토큰은 게임 아이템이 디지털 수집물 같은 아이템일 수도 있습니다. 또한, 자동차 같은 소유권을 추적하기 위한 실물일 수도 있습니다.

ERC721 표준은 증서에의해 그 소유권이 고유하게 추적될 수 있는 한, 그 대상의 종류에 대해 어떤 제한이나 규정을 두지 않으며, 이러한 추적은 256 bit 식별자에 의해 이루어 집니다.

ERC721 의 내부 데이터 구조를 살펴보겠습니다.

```java
// Mapping from deed ID to owner
mapping (uint256 => address) private deedOwner;
```

ERC20 은 각 소유자에 속한 잔액을 추적하고 소유자는 매핑의 기본 키인 반면, ERC721 은 각 증서 ID 와 소유권자를 추적하며 증서 ID 는 매핑의 기본 키가 됩니다.

ERC721 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC721 /* is ERC165 */ {
    event Transfer(address indexed _from, address indexed _to, uint256 _deedId);
    event Approval(address indexed _owner, address indexed _approved,
                   uint256 _deedId);
    event ApprovalForAll(address indexed _owner, address indexed _operator,
                         bool _approved);

    function balanceOf(address _owner) external view returns (uint256 _balance);
    function ownerOf(uint256 _deedId) external view returns (address _owner);
    function transfer(address _to, uint256 _deedId) external payable;
    function transferFrom(address _from, address _to, uint256 _deedId)
        external payable;
    function approve(address _approved, uint256 _deedId) external payable;
    function setApprovalForAll(address _operateor, boolean _approved) payable;
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

ERC721 은 또한 메타데이터와 증서 및 소유자의 열거를 위해 2개의 **선택적(optional)** 인터페이스를 지원합니다.

메타데이터에 대한 ERC721 선택적 인터페이스는 다음과 같습니다.

```java
interface ERC721Metadata /* is ERC721 */ {
    function name() external pure returns (string _name);
    function symbol() external pure returns (string _symbol);
    function deedUri(uint256 _deedId) external view returns (string _deedUri);
}
```

열거를 위한 ERC721 선택적 인터페이스는 다음과 같습니다.

```java
interface ERC721Enumerable /* is ERC721 */ {
    function totalSupply() external view returns (uint256 _count);
    function deedByIndex(uint256 _index) external view returns (uint256 _deedId);
    function countOfOwners() external view returns (uint256 _count);
    function ownerByIndex(uint256 _index) external view returns (address _owner);
    function deedOfOwnerByIndex(address _owner, uint256 _index) external view
        returns (uint256 _deedId);
}
```

## Using Token Standards

### What Are Token Standards? What Is Their Purpose?

토큰 표준은 구현을 위한 **최소(minimum)** 사양입니다. 즉, ERC20 을 준수하려면 최소한 ERC20 표준에 명시된 함수와 동작을 구현해야합니다.

이러한 표준의 주요 목적은 컨트랙트 간의 **상호운용성(interoperability)** 를 장려하는 것입니다. 따라서 모든 지갑, 거래서 사용자 인터페이스는 사양을 따르는 컨트랙트와 예측 가능한 방식으로 **인터페이스(interface)** 할 수 있습니다. 다시 말해, ERC 20 표준을 따르는 컨트랙트를 배포하면 기존 지갑 사용자는 지갑을 업그레이드 하거나 노력하지 않아도 토큰을 원활하게 트랜잭션할 수 있습니다.