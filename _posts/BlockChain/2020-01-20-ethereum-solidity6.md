---
title : Ethereum Smart Contracts and Solidity -6-
tags :
- Solidity
- Smart Contract
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Calling Other Contracts (send, call, callcode, delegatecall)

컨트랙트 내에서 다른 컨트랙트를 호출하는 것은 매우 유용하지만 위험을 내포한 작업입니다. 스마트 컨트랙트를 작성할 때 대부분 EOA 만을 다루게 될 것으로 예상하지만, 예상치 못하게 복잡하거나 악의적인 컨트랙트가 코드를 호출하거나 악의적인 컨트랙트를 코드가 호출할 수 있음을 염두해야합니다.

### Creating a new instance

다른 컨트랙트를 호출하기 위한 가장 안전한 방법은 직접 다른 컨트랙트를 만드는것입니다.  그렇게 하면 인터페이스와 동작이 확실할 수 있습니다. 이렇게 하기 위해 `new` 키워드를 사용하여 간단히 인스턴스화 할 수 있습니다.

다음 예제는 `Token` 이라는 컨트랙트 내에서 `Faucet` 컨트랙트를 만들고 호출한다고 가정해보겠습니다.

```java
contract Token is mortal {
	Faucet _faucet;

	constructor() {
		_faucet = new Faucet();
	}
}
```

`Faucet` 컨트랙트는 `Token` 영역 안에서 정의되거나 `import` 구문을 사용하여 `Token` 영역 안에서 정의되어야 합니다.

```java
import "Faucet.sol";

contract Token is mortal {
	Faucet _faucet;

	constructor() {
		_faucet = new Faucet();
	}
}
```

또한, 인스턴스 생성 시 선택적으로 이더 전송 값을 지정할 수 있고 새 컨트랙트 생성자에게 인수로 전달할 수 있습니다.

```java
import "Faucet.sol";

contract Token is mortal {
	Faucet _faucet;

	constructor() {
		_faucet = (new Faucet).value(0.5 ether)();
	}
}
```

`Token` 의 `destroy` 함수 내에서 `Faucet` 의 `destroy` 함수를 호출할 수 있습니다.

```java
import "Faucet.sol";

contract Token is mortal {
	Faucet _faucet;

	constructor() {
		_faucet = (new Faucet).value(0.5 ether)();
	}

	function destroy() ownerOnly {
		_faucet.destroy();
	}
}
```

`Token` 컨트랙트의 소유자인 경우 `Token` 컨트랙트 자체가 새로운 `Faucet` 컨트랙트를 소유하므로 `Token` 컨트랙트는 `Faucet` 을 파기할 수 있습니다.

### Addressing an existing instance

다른 컨트랙트를 호출할 수 있는 또 다른 방법은 이미 존재하는 해당 컨트랙트의 인스턴스 주소를 캐스팅하는 방법입니다.

```java
import "Faucet.sol";

contract Token is mortal {

	Faucet _faucet;

	constructor(address _f) {
		_faucet = Faucet(_f);
		_faucet.withdraw(0.1 ether)
	}
}
```

위 코드에선 생성자 `_f` 에 대한 인수로 제공된 주소를 가져와서 `Faucet` 객체로 형변환을 합니다. 이 방법은 실제 주소가 `Faucet` 객체인지 여부를 확실히 알 수 없기 때문에 이전 메커니즘보다 위험합니다.

### Raw call, delegatecall

솔리디티는 다른 컨트랙트를 호출하기 위한 저수준 함수를 제공합니다. 이는 동일한 이름의 EVM 연산코드에 직접적으로 대응하고 컨트랙트 간의 호출을 수동으로 구성할 수 있게 해줍니다.

아래는 `call` 메소드를 사용한 예제입니다.

```java
contract Token is mortal {
	constructor(address _faucet) {
		_faucet.call("withdraw", 0.1 ether);
	}
}
```

`call` 형태는 함수 안에 **숨은(blind)** 호출이며, 원시 트랜잭션을 생성하는 것과 매우 비슷합니다. 이는 컨트랙트의 컨텍스트에서 발생하고 컨트랙트를 여러 보안 위험에 노출 시킬 수 있는데, 가장 중요한 문제는 **재진입성(reentrancy)** 입니다. `call` 함수는 어떤 문제가 있을 경우 `false` 를 반환하기 때문에 에러 처리를 하기 위해선 반환값을 조사해야 합니다.

```java
contract Token is mortal {
	constructor(address _faucet) {
		if !(_faucet.call("withdraw", 0.1 ether)) {
			revert("Withdrawal from faucet failed");
		}
	}
}
```

호출의 또 다른 변형은 `delegatecall` 입니다. `callcode` 의 위험한 방식을 대체하기 위해 나왔습니다. `delegatecall` 은 `msg` 컨텍스트가 변경되지 않는다는 점에서 `call` 과 다릅니다. `call` 은 `msg.sender` 의 값을 호출하는 컨트랙트로 변경하지만, `delegatecall` 은 호출하는 컨트랙트와 동일한 `msg.sender` 를 유지합니다. 본질적으로 `delegatecall` 은 현재 컨트랙트의 컨텍스트 내에서 다른 컨트랙트의 코드를 실행합니다. 주로 라이브러리의 코드를 생성(invoke) 할 때 사용합니다.

아래 코드는 [[Github]](https://github.com/ethereumbook/ethereumbook/blob/develop/code/truffle/CallExamples/contracts/CallExamples.sol) 에 있습니다.

```java
pragma solidity ^0.4.22;

contract calledContract {
	event callEvent(address sender, address origin, address from);
	function calledFunction() public {
		emit callEvent(msg.sender, tx.origin, this);
	}
}

library calledLibrary {
	event callEvent(address sender, address origin,  address from);
	function calledFunction() public {
		emit callEvent(msg.sender, tx.origin, this);
	}
}

contract caller {

	function make_calls(calledContract _calledContract) public {

		// Calling calledContract and calledLibrary directly
		_calledContract.calledFunction();
		calledLibrary.calledFunction();

		// Low-level calls using the address object for calledContract
		require(address(_calledContract).
		        call(bytes4(keccak256("calledFunction()"))));
		require(address(_calledContract).
		        delegatecall(bytes4(keccak256("calledFunction()"))));



	}
}
```

위의 예제와 같이 주 컨트랙트는 `caller` 이며 `caller` 는 `calledContract` 컨트랙트와 `calledLibrary` 라이브러리를 호출합니다. 호출된 컨트랙트와 라이브러리는 `calledEvent` 이벤트를 발생시키기 위한 동일한 `calledFunction` 함수를 갖습니다. `calledFunction` 는 `msg.sender`, `tx.origin`, `this` 이렇게 3가지 데이터를 로깅합니다. `calledFunction` 을 호출할 때마다 직접 호출했는지 아니면 `delegatecall` 을 통해 호출했는지에 따라 실행컨텍스트를 가질 수 있습니다.

`caller` 에서 컨트랙트와 라이브러리를 직접 호출하는 데 이때 각각 `calledFunction` 을 실행합니다. 다음 저수준 함수인 `call` 과 `delegatecall` 을 명시적으로 사용해서 `calledContract.calledFunction` 을 호출합니다. 이렇게 함으로 다양한 호출 메커니즘이 어떻게 작동하는지 확인할 수 있습니다.

아래 코드는 트러플 개발환경에서 실행해본것입니다.

```shell
truffle(develop)> migrate
Using network 'develop'.
[...]
Saving artifacts...
truffle(develop)> web3.eth.accounts[0]
'0x627306090abab3a6e1400e9345bc60c78a8bef57'
truffle(develop)> caller.address
'0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f'
truffle(develop)> calledContract.address
'0x345ca3e014aaf5dca488057592ee47305d9b3e10'
truffle(develop)> calledLibrary.address
'0xf25186b5081ff5ce73482ad761db0eb0d25abfbf'
truffle(develop)> caller.deployed().then( i => { callerDeployed = i })

truffle(develop)> callerDeployed.make_calls(calledContract.address).then(res => \
                  { res.logs.forEach( log => { console.log(log.args) })})
{ sender: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
  origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  from: '0x345ca3e014aaf5dca488057592ee47305d9b3e10' }
{ sender: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  from: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f' }
{ sender: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
  origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  from: '0x345ca3e014aaf5dca488057592ee47305d9b3e10' }
{ sender: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
  from: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f' }
```

위 코드에서는 `make_calls` 함수를 호출하고 `calledContract` 의 주소를 전달한 다음, 각각의 다른 호출에 의해 생성된 4개의 이벤트를 포착했습니다. 각 단계별로 살펴보겠습니다.

첫 번째 호출은 아래와 같습니다.

```shell
_calledContract.calledFunction();
```

여기서는 `calledFunction` 에 고수준 ABI 를 사용하여 `calledContract.calledFunction` 직접 호출하고 있습니다. 발생되는 이벤트는 아래와 같습니다.

```shell
sender: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
from: '0x345ca3e014aaf5dca488057592ee47305d9b3e10'
```

`msg.sender` 는 `caller` 컨트랙트의 주소입니다. `tx.origin` 은 `caller` 에게 트랜잭션을 보낸 계정 `web3.eth.accounts[0]` 의 주소입니다. 이벤트는 마지막 인수에서 보는것처럼 `calledContract` 에 의해 생성되었습니다.

`make_calls` 에서 다음 호출은 라이브러리입니다.

```shell
calledLibrary.calledFunction();
```

이것은 우리가 컨트랙트를 호출한 방법과 똑같아 보이지만 매우 다르게 동작합니다. 발생된 이벤트를 보겠습니다.

```shell
sender: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
origin: '0x627306090abab3a6e1400e9345bc60c78a8bef57',
from: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f'
```

이번에는 `msg.sender` 가 `caller` 주소가 아닙니다. 대신, 이것은 우리 게정의 주소이며 이 컨트랙트의 origin 과 동일합니다. 라이브러리를 호출할 때 호출은 항상 `delegatecall` 이고 호출자의 컨텍스트 내에서 실행되기 때문입니다.

따라서 `calledLibrary` 코드가 실행 중일 때 `caller` 의 코드가 `caller` 내에서 실행 중인 것처럼 `caller` 의 실행 컨텍스트를 상속합니다. this 는 `calledLibrary` 내부에서 액세스되었음에도 `caller` 의 주소를 갖게 되었습니다.

저수준의 `call` 과 `delegatecall` 을 사용하는 다음 2 번의 호출은 우리가 방금 본 내용을 반영하는 이벤트를 발생시켜 예상한것이 맞음을 확인할 수 있습니다.