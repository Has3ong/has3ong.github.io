---
title : Ethereum Smart Contracts and Solidity -4-
tags :
- Contract
- Solidity
- Smart Contract
- Ethereum
- BlockChain
---

## Contract Definition

솔리디티의 주요 데이터 타입은 contract 입니다. 앞서 살펴본 예제는 단순하게 contract 객체를 정의합니다. 컨트랙트는 OOP 의 객체와 마찬가지로 데이터와 메서드가 포함된 컨테이너 입니다.

솔리디티는 컨트랙트와 유사한 2 가지 객체 유형을 제공합니다.

**interface**

함수가 정의되어 있지 않고 선언만 되어 있다는것을 제외하면 컨트랙트와 완전히 같은 구조로 되어 있스비다.

이런 유형의 선언은 흔히 stub 이라고 불립니다. 어떤 구현도 없이 함수의 인자와 유형을 알려줍니다. 

인터페이스는 컨트랙트의 형태를 지정합니다. 상속될 때 인터페이스에 의해 선언된 각 함수는 자식에 의해 정의되어야 합니다.

**library**
라이브러리 컨트랙트는 `delegatecall` 메서드를 사용하여 한 번만 배포되고 다른 컨트랙트에서 사용되기 위한 컨트랙트 입니다.

### Functions

솔리디티에서 함수를 선언할 때 사용하는 구문은 다음과 같습니다.

```java
function FunctionName([parameters]) {public|private|internal|external}
[pure|constant|view|payable] [modifiers] [returns (return types)]
```

**FunctionName**

다른 컨트랙트 또는 동일한 컨트랙트 내에서 함수를 호출하는데 사용하는 함수의 이름입니다. 각 컨트랙트마다 한 개의 함수는 이름이 없이 정의될 수 있는데, 그것을 **fallback** 함수라 부르고 다른 함수 이름이 없을 때 호출됩니다. 폴백함수는 인수가 없으며 아무것도 반환할 수 없습니다.

**parameters**

이름 뒤에 함수 이름과 유형과 함께 전달되어야 하는 인수를 지정합니다.

다음 키워드 세트 (public, private, internal, external) 는 함수의 **visibility** 를 지정합니다.

**public**

공개 함수는 기본값입니다. 공개 함수는 다른 컨트랙트 또는 EOA 트랜잭션 또는 컨트랙트 내에서 호출할 수 있습니다.

**external**

외부 함수는 명시적으로 키워드 this 가 앞에 붙지 않는 한, 컨트랙트 내에서 호출할 수 없다는 점을 제외하면 공개 함수와 같습니다.

**internal**

내부 함수는 컨트랙트 내에서만 접근할 수 있습니다. 다른 컨트랙트 또는  EOA 트랜잭션으로는 호출할 수 있습니다. 파생된 컨트랙트 의해서는 호출할 수 있습니다.

**private**

비공개 함수는 내부 함수와 유사하지만 패상된 컨트랙트에서도 호출할 수 없습니다.

**내부(internal)** 및 **프라이빗(private)** 이라는 용어는 다소 오해의 소지가 있습니다. 컨트랙트 내의 모든 함수 또는 데이터는 공개 블록체인에서 항상 볼 수 있습니다. 즉 누구나 코드나 데이터를 볼 수 있습니다. 위에 설명한 키워드는 함수를 **호출** 할 수 있는 방법과 조건에만 영향을 줍니다.

2 번째 키워드 세트 (pure, constant, view, payable) 는 함수의 동작에 영향을 줍니다.

**constant, view**

**view** 로 표시된 함수는 상태를 변경하지 않습니다. **상수(constant)** 라는 용어는 향후 릴리스에서 사용되지 않는 뷰의 별칭 입니다.

**pure**

순수 함수는 스토리지에서 변수를 읽거나 쓰지 않는 함수입니다. 저장된 데이터를 참고하지 않고 인수에 대해서만 작동하고 데이터를 반환할 수 있습니다. 순수 함수는 부작용이나 상태가 없는 선언형 프로그래밍을 지원하기 위한 것입니다.

**payable**

payable 이 선언되어 있다면 입금을 받을 수 있는 함수이고, 그렇지 않으면 입금이 거부됩니다. EVM 에서 설계할 때 2 가지 예외가 있는데, **보상 지불** 및 **SELFDESTRUCT** 입니다. 이 2 가지 경우는 코드의 실행이 지불의 이룹는 아니기 때문에 폴백 함수가 payable 로 선언되어 있지 않은 경우에도 지불될 것입니다.

### Contract Constructor and selfdestruct

컨트랙트가 생성될 때 **생성자 함수(constructor function)** 가 있는 경우 이를 실행하여 컨트랙트의 상태를 초기화 합니다. 생성자는 컨트랙트 생성과 동일한 트랜잭션에서 실행 됩니다.

```java
contract MEContract {
	function MEContract() {
		// This is the constructor
	}
}
```

위 방식의 문제점은 컨트랙트 이름이 변경되는 경우 생성자 함수가 작동되지 않게 되는 점 입니다.

솔리디티 `v0.4.22` 에서는 생성자 함수처럼 작동하지만, 이름이 없는 `constructor` 키워드를 도입했습니다. 컨트랙트의 이름을 변경해도 생성자에는 전혀 영향을 주지 않습니다.

```java
pragma ^0.4.22
contract MEContract {
	constructor () {
		// This is the constructor
	}
}
```

컨트랙트의 생명주기는 EOA 또는 컨트랙트 계정으로부터 트랜잭션 생성을 시작합니다. 생서앚가 있는 경우라면 컨트랙트 생성의 일부분으로 실행되어 컨트랙트가 생성될 때 컨트랙트 상태를 초기화한 다음 소멸합니다.

컨트랙트의 생명주기의 끝은 **컨트랙트 소멸(contract destruction)** 입니다. 컨트랙트는 SELFDESTRUCT 라는 EVM 연산 코드에 의해 소멸됩니다. 이 함수는 컨트랙트 계정에 남아 있는 이더 잔액을 받기 위한 주소를 받습니다.

```java
selfdestruct(address recipient);
```

컨트랙트가 영원히 지속된다는 것을 보장해야 할 때는 SELFDESTRUCT 연산 코드를 포함하지 않으면 안됩니다.

### Adding a Constructor and selfdestruct to Our Faucet Example

Constructor 와  selfdestrcut 함수를 추가한 예제를 만들어보겟습니다.

```java
// Version of Solidity compiler this program was written for
pragma solidity ^0.4.22;

// Our first contract is a faucet!
contract Faucet {

	address owner;

	// Initialize Faucet contract: set owner
	constructor() {
		owner = msg.sender;
	}

[...]
```

일반적으로 생성자는 address 를 owner 라는 주소 변수에 저장합니다. 생성자는 owner 라는 변수를 설정하고 owner  변수에 `msg.sender` 의 주소를 할당합니다.

컨트랙트를 파기하는 함수를 추가할 수 있습니다. 소유자만이 이 함수를 실행할 수 있음을 표시할 필요가 있습니다. 그래서 접근 제어를 위해 `require` 구문을 사용합니다.

```java
// Contract destructor
function destroy() public {
	require(msg.sender == owner);
	selfdestruct(owner);
}
```

owner 가 아닌 다른 주소에서 destroy 함수를 호출하면 실행이 되지 않습니다. 하지만 생성자가 owner 에 저장한 동일한 주소를 호출하면 컨트랙트는 자기파괴되고 남은 잔액을 owner 주소로 되돌려 줍니다.