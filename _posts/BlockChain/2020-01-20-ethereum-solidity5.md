---
title : Ethereum Smart Contracts and Solidity -5-
tags :
- Solidity
- Smart Contract
- Ethereum
- BlockChain
---

### Function Modifiers

솔리디티에서는 **함수 변경자(function modifier)** 라 불리는 함수를 제공합니다. 함수 선언에 `modifier` 라는 이름을 추가하여 적용합니다. 변경자는 컨트랙트 내에서 함수에 적용되어야 할 여러 조건을 생성하기위해 자주 사용됩니다. 아래는 예시입니다.

```java
modifier onlyOwner {
    require(msg.sender == owner);
    _;
}
```

컨트랙트의 owner 로 저장된 주소가 트랜잭션의 `msg.sender` 주소가 동일해야 합니다. 오직 컨트랙트 소유자만 `onlyOwner` 변경자를 가진 모든 함수를 실행할 수 있게 해줍니다.

함수 변경자는 안에 **표시자(placeholder)** 가 있고 밑줄 뒤에 세미콜린이 따라옵니다. 이 표시는 수정되는 함수의 코드로 대체됩니다. 기본적으로 변경자는 변경된 함수 주변을 둘러쌉니다. 밑줄 문자로 식별된 위치에 코드가 삽입됩니다.

변경자를 적용하려면 함수 선언에 변경자 이름을 추가합니다. 함수에 둘 이상의 변경자를 적용할 수 있습니다.

`onlyOwner` 변경자를 사용하여 `destroy` 함수를 작성해보겠습니다.

```java
function destroy() public onlyOwner {
    selfdestruct(owner);
}
```

`destroy` 함수가 `onlyOwner` 변경자에 의해 한정되는것을 알 수 있습니다. 실제 결과 코드는 `onlyOwner` 가 `destroy` 함수를 감싸고 있는 **wrapping** 코드와 같습니다.

### Contract Inheritance

상속을 사용하기 위해선 부모 컨트랙트에 `is` 키워드를 사용하면 됩니다.

```java
contract Child is Parent {
  ...
}
```

위 구조는 `Child` 컨트랙트가 `Parent` 의 모든 메소드, 변수, 기능을 상속한다는 의미입니다. 솔리디티에서는 다중 상속도 지원합니다.

```java
contract Child is Parent1, Parent2 {
  ...
}
```

컨트랙트 상속을 통해서 모듈성, 확장성, 재사용을 달성할 수 있는 방법으로 컨트랙트를 작성할 수 있습니다. 단순하고 일반적인 기능을 구현한 컨트랙트를 시작한 다음 전문화된 컨트랙트로 기능을 상속하여 확장시킬 수 있습니다.

`owner` 변수가 있는 `owned` 컨트랙트를 정의하고 컨트랙트의 생성자에서 `owner` 를 설정합니다.

```java
contract owned {
	address owner;

	// Contract constructor: set owner
	constructor() {
		owner = msg.sender;
	}

	// Access control modifier
	modifier onlyOwner {
	    require(msg.sender == owner);
	    _;
	}
}
```

`owned` 를 상속한 기본 컨트랙트인 `mortal` 을 정의합니다.

```java
contract mortal is owned {
	// Contract destructor
	function destroy() public onlyOwner {
		selfdestruct(owner);
	}
}
```

```java
contract Faucet is mortal {
    // Give out ether to anyone who asks
    function withdraw(uint withdraw_amount) public {
        // Limit withdrawal amount
        require(withdraw_amount <= 0.1 ether);
        // Send the amount to the address that requested it
        msg.sender.transfer(withdraw_amount);
    }
    // Accept any incoming amount
    function () public payable {}
}
```

`owned` 를 상속받은 `mortal` 을 상속받아서 **Faucet** 컨트랙트는 생성자와 `destroy` 함수 그리고 소유자가 정의한 것들을 가질 수 있습니다.

### Error Handling (assert, require, revert)

컨트랙트 호출은 중단되고 에러를 반환할 수 있습니다. 솔리디티에서는 에러 제어를 `assert`, `require`, `revert`, `throw` 4 가지 함수를 사용합니다.

에러로 스마트 컨트랙트가 중지될 때는 둘 이상의 컨트랙트가 호출된 경우 컨트랙트 호출 연결을 따라 모든 상태가 원래대로 되돌려집니다. 왜냐하면, 트랜잭션들이 **원자성(atomic)** 을 보장해야 하기 때문입니다.

`assert` 와 `require` 함수도 조건을 평가하고, 조건이 거짓이면 에러로 실행을 중지시키는 동일한 방식으로 동작합니다. 통상적으로 `assert` 는 결과가 참일 것으로 예상될 때 사용하는데, 이것은 내적인 조건이 만족되는지 테스트를 하는 의미입니다. 이에 비해 `require` 는 입력값이 설정한 조건의 기댓값에 맞는지 테스트할 때 사용합니다.

메세지 발신자가 컨트랙트의 소유자임을 테스트하기 위해 함수 변경자 `onlyOwner` 에서 `require` 를 사용합니다.

```java
require(msg.sender == owner);
```

`require` 함수는 요구되는 조건이 만족되지 않을 경우 에러를 발생시켜 함수의 나머지 부분이 실행되지 않도록 하는 **게이트 조건(gate condition)** 기능을 합니다. 또한, 아래와 같이 `require` 함수에 에러 메세지를 추가함으로써 코드를 개선할 수 있습니다.

```java
require(msg.sender == owner, "Only the contract owner can call this function");
```

`revert` 와 `throw` 함수는 컨트랙트의 실행을 중지하고 모든 변경상태를 되돌립니다. `throw` 함수는 제거될 예정이라 `revert` 를 사용합니다. `revert` 함수는 다른 변수 없이 에러 메세지만을 인수로 사용할 수 있는데, 이 메세지는 트랜잭션 로그에 기록됩니다.

앞선 예제에서는 출금 요청을 할 때 이더가 충분한지 여부를 명시적으로 확인하지 않습니다. 그 이유는 `transfer` 함수에서 이더가 충분하지 않으면 에러를 내고 트랜잭션을 되돌릴 것이기 때문입니다.

```java
msg.sender.transfer(withdraw_amount);
```

하지만 아래와같이 실패시 에러 메세지를 명시적으로 확인하는것이 좋습니다.

```java
require(this.balance >= withdraw_amount,
	"Insufficient balance in faucet for withdrawal request");
msg.sender.transfer(withdraw_amount);
```

### Event

트랜잭션이 완료되면 **트랜잭션 영수증(transaction receipt)** 를 발행합니다. 트랜잭션 영수증은 트랜잭션의 실행 동안 발생했던 행위에 관한 정보를 제공하는 **로그(log)** 를 가지고 있습니다. 이벤트는 이러한 로그를 만들기 위해 사용하는 솔리디티의 고수준 객체 입니다.

앞선 예제에 이벤트를 추가하지 않았으므로 **출금(withdrawal)** 과 **입금(deposit)** 을 해보겠습니다.

```java
contract Faucet is mortal {
	event Withdrawal(address indexed to, uint amount);
	event Deposit(address indexed from, uint amount);

	[...]
}
```

다음은 트랜잭션 로그에 이벤트 데이터를 넣기 위해서 `emit` 키워드를 사용합니다.

```java
// Give out ether to anyone who asks
function withdraw(uint withdraw_amount) public {
    [...]
    msg.sender.transfer(withdraw_amount);
    emit Withdrawal(msg.sender, withdraw_amount);
}
// Accept any incoming amount
function () public payable {
    emit Deposit(msg.sender, msg.value);
}
```

이벤트를 추가하여 만든 결과는 다음과 같습니다.

```java
// Version of Solidity compiler this program was written for
pragma solidity ^0.4.22;

contract owned {
	address owner;
	// Contract constructor: set owner
	constructor() {
		owner = msg.sender;
	}
	// Access control modifier
	modifier onlyOwner {
		require(msg.sender == owner,
		        "Only the contract owner can call this function");
		_;
	}
}

contract mortal is owned {
	// Contract destructor
	function destroy() public onlyOwner {
		selfdestruct(owner);
	}
}

contract Faucet is mortal {
	event Withdrawal(address indexed to, uint amount);
	event Deposit(address indexed from, uint amount);

	// Give out ether to anyone who asks
	function withdraw(uint withdraw_amount) public {
		// Limit withdrawal amount
		require(withdraw_amount <= 0.1 ether);
		require(this.balance >= withdraw_amount,
			"Insufficient balance in faucet for withdrawal request");
		// Send the amount to the address that requested it
		msg.sender.transfer(withdraw_amount);
		emit Withdrawal(msg.sender, withdraw_amount);
	}
	// Accept any incoming amount
	function () external payable {
		emit Deposit(msg.sender, msg.value);
	}
}
```

### Catching events

`truffle` 을 사용하여 Faucet 컨트랙트에 대한 테스트 트랜잭션을 실행해보겠습니다. 코드의 주소는 [[Github]](https://github.com/ethereumbook/ethereumbook/tree/develop/code/truffle/FaucetEvents) 에 있습니다.

```shell
$ truffle develop
truffle(develop)> compile
truffle(develop)> migrate
Using network 'develop'.

Running migration: 1_initial_migration.js
  Deploying Migrations...
  ... 0xb77ceae7c3f5afb7fbe3a6c5974d352aa844f53f955ee7d707ef6f3f8e6b4e61
  Migrations: 0x8cdaf0cd259887258bc13a92c0a6da92698644c0
Saving successful migration to network...
  ... 0xd7bc86d31bee32fa3988f1c1eabce403a1b5d570340a3a9cdba53a472ee8c956
Saving artifacts...
Running migration: 2_deploy_contracts.js
  Deploying Faucet...
  ... 0xfa850d754314c3fb83f43ca1fa6ee20bc9652d891c00a2f63fd43ab5bfb0d781
  Faucet: 0x345ca3e014aaf5dca488057592ee47305d9b3e10
Saving successful migration to network...
  ... 0xf36163615f41ef7ed8f4a8f192149a0bf633fe1a2398ce001bf44c43dc7bdda0
Saving artifacts...

truffle(develop)> Faucet.deployed().then(i => {FaucetDeployed = i})
truffle(develop)> FaucetDeployed.send(web3.toWei(1, "ether")).then(res => \
                  { console.log(res.logs[0].event, res.logs[0].args) })
Deposit { from: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  amount: BigNumber { s: 1, e: 18, c: [ 10000 ] } }
truffle(develop)> FaucetDeployed.withdraw(web3.toWei(0.1, "ether")).then(res => \
                  { console.log(res.logs[0].event, res.logs[0].args) })
Withdrawal { to: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  amount: BigNumber { s: 1, e: 17, c: [ 1000 ] } }
```

`deployed` 함수를 사용하여 컨트랙트를 배포한 후 트랜잭션을 실행합니다. 1 번째는 트랜잭션 로그에 `Deposit` 이벤트를 내보내는 입금입니다.

```java
Deposit { from: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  amount: BigNumber { s: 1, e: 18, c: [ 10000 ] } }
```

다음은 출금을 만들기 위해 `withdraw` 함수를 사용합니다. 이것은 `Withdrawal` 이벤트를 내보냅니다.

```java
Withdrawal { to: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  amount: BigNumber { s: 1, e: 17, c: [ 1000 ] } }
```

이벤트를 컨트랙트 내에서의 커뮤니케이션뿐만 아니라 개발 과정에서의 디버깅에도 매우 유용합니다.