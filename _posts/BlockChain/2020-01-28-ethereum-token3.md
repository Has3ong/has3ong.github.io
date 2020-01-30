---
title : Ethereum Tokens -3-
tags :
- ERC20
- Token
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

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

ganache 콘솔에서 `Example 1` 과 같이 배포를 통해 4 가지 새로운 트랜잭션이 생성된 걸 확인할 수 있습니다.

> Example 1 - METoken deployment on ganache

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