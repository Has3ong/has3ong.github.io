---
title : Ethereum Smart Contracts and Solidity
tags :
- Solidity
- Smart Contract
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## What Is a Smart Contract?

**스마트 컨트랙트(smart contract)** 라는 용어는 다양한 것들을 설명하기 위해 수년동안 사용되어왔습니다.

암호학자 *Nick Szabo* 는 이 용어를 **당사자들이 다른 약속에 따라 수행하는 프로토콜을 포함하여 디지털 형식으로 지정된 일련의 약속** 이라고 정의했다.

스마트 컨트랙트의 개념은 비트코인의 발명으로 탈중앙화 블록체인 플랫폼이 도입된 후에 진화했다. 스마트 컨트랙트 이더리움 네트워크 프로토콜의 일부인 이더리움 가상 머신의 컨텍스트상에서 결정론적으로(deterministically) 작동한다.

이제 스마트 컨트랙트의 정의를 살펴보겠습니다.

* **computer programs**
  * 스마트 컨트랙트는 단순히 컴퓨터 프로그램이다. 컨트랙트라는 단어는 이런 맥락에서 법적인 의미는 없다.
* **immutable**
  * 스마트 컨트랙트 코드는 일단 배포되면, 변경할 수 없다. 기존 소프트웨어와 달리 컨트랙트를 수정하는 유일한 방법은 새로운 인스턴스를 배포하는 것이다.
* **deterministic**
  * 스마트 컨트랙트를 실행한 결과물은 그것을 실행한 모든 이에게 동일한데, 실행을 시작한 트랜잭션의 컨텍스트와 실행 시점에 이더리움 블록체인의 상태가 동일한다는 전제가 있기 때문이다.
* **EVM context**
  * 스마트 컨트랙트는 매우 제한적인 실행 컨텍스트에서 작동된다. 이들은 자신의 상태, 호출한 트랜잭션의 컨텍스트 및 가장 최근 블로그이 일부 정보에 접근할 수 있다.
* **decentralized world computer**
  * EVM 은 모든 이더리움 노드에서 로컬 인스턴스로 실행되지만, EVM 의 모든 인스턴스는 동일한 초기 상태에서 작동하고 동일한 최종 상태를 생성하기 때문에 시스템 전체가 단일 '월드 컴퓨터'로 작동한다. 
  
## Life Cycle of a Smart Contract

스마트 컨트랙트는 일반적으로 솔리디티 같은 고급 언어로 작성됩니다. 컨트랙트를 실행하려면 EVM 에서 실행되는 저수준의 바이트 코드로 컴파일 되어야 합니다. 일단 컴파일되면 고유한 **컨트랙트 생성(contract creation)** 트랜잭션을 사용하여 이더리움 플랫폼에 배포되며, 이 트랜잭션은 고유한 컨트랙트 생성 주소, 0x0 으로 전송됩니다.

각 컨트랙트는 이더리움 주소로 식별되며, 이 주소는 원래 계정 및 논스의 함수로 컨트랙트 생성 트랜잭션에서 파생됩니다. 컨트랙트의 이더리움 주소는 트잭잭션에서 수신자로 사용되거나 컨트랙트에 자금을 보내거나 컨트랙트 함수를 호출하는 데 사용할 수 있습니다.

컨트랙트는 **트랜잭션에 의해 호출된 경우에만 실행됩니다.** 이더리움의 모든 스마트 컨트랙트는 EOA 에서 시작된 트랜잭션으로 인해 실행됩니다. 컨트랙트는 다른 컨트랙트를 호출할 수 있고 그 컨트랙트는 또 다른 컨트랙트를 호출할 수 있지만, 체안에서 첫번째 컨트랙트 실행은 항상 EOA 로부터 트랜잭션에 의해 호출됩니다. 스마트 컨트랙트는 체인의 일부분으로 트랜잭션에 의해 직접 혹은 간접적으로 호출되기 전까지는 대기 상태에 놓여 있습니다.

트랜잭션은 호출하는 컨트랙트 수 또는 호출 시 해당 컨트랙트가 수행하는 작업과 상관없이 **원자성(atmoic)** 의 특징을 지닙니다. 트랜잭션은 모든 실행이 성공적으로 종료된 경우에만 글로벌 상태의 모든 변경사항이 기록되고 전체가 실행됩니다. 성공적인 종료는 모든 프로그램이 오류 없이 실행되었음을 의미합니다. 오류로 인한 실행이 실패하면 모든 영향은 트랜잭션이 실행되지 않은 것처럼 **롤백(rolled back)** 됩니다. 실패한 트랜잭션은 여전히 시도된것으로 기도되며, 실행을 위해 가스로 소비된 어디는 원 계정에서 차감되지만, 컨트랙트 또는 계좌 상태에는 영향을 미치지 않습니다.

컨트랙트를 삭제하려면 SELFDESTRUCT 라는 EVM 연산 코드를 실행해야 합니다. 이 작업은 **음의 가스(negative gas)** 즉, 가스 환불이 일어나기 때문에 저장된 상태의 삭제로 인한 네트워크 클라이언트의 자원을 반환하도록 하는 동기부여를 만듭니다. 이 방법으로 컨트랙트를 삭제해도 컨트랙트의 트랜잭션 내역이 제거되지는 않습니다.

## Introduction to Ethereum High-Level Languages

일반적으로 프로그래밍 언어는 **선언형(declaretive)** 프로그래밍과 **명령형(imperative)** 프로그래밍이라는 2가지 프로그래밍으로 분류할 수 있습니다. **함수형(functional)** 프로그래밍과 **절차적(procedural)** 프로그래밍이라고도 합니다. 

선언형 프로그래밍에서는 프로그래밍은 프로그램이 **logic** 을 표현하지만, 그 **flow** 는 표현하지 않는 함수를 작성합니다. 선언형 프로그래밍은 **부작용(side effect)** 가 없는 프로그램을 만드는데 사용됩니다.

선언형 프로그램의 예로는 SQL 이 있습니다. 반대로 명령형 프로그래밍 언어에는 C++ 및 Java 가 있습니다.

스마트 컨트랙트에서 널리 사용되는 언어는 명령형 언어입니다.

스마트 컨트랙트에 대해 현재 지원되는 고급 프로그래밍 언어는 아래와 같습니다.

* LLL(Low-level Lisp-like Language)
* Serpent
* Solidity
* Vyper
* Bamboo

## Building a Smart Contract with Solidity

솔리디티는 명시적으로 스마트 컨트랙트 작성을 위해 만들어진 언어인데, 이더리움 월드 컴퓨터의 탈중앙화된 환경에서의 실행을 직접적으로 지원합니다. 그 결과, 언어의 속성이 매우 일반적이어서 다른 여러 블로겣인 플랫폼에서 스마트 컨트랙트를 코딩하는데 사용됩니다. 현재 솔리디티는 [깃허브](https://github.com/ethereum/solidity) 에서 개발되고 유지되고있습니다.

솔리디티 프로젝트의 주된 제품은 솔리디티 언어로 작성된 프로그램을 EVM 바이트코드로 변환하는 솔리디티 컴파일러 `solc` 이다. 이 프로젝트는 또한 이더리움 스마트 컨트랙트를 위한 중요한 어플리케이션 바이너리 인터페이스(Application Binary Interface, ABI) 표준을 관리합니다.

### Selecting a Version of Solidity

솔리디티는 **시맨틱 버저닝(semantic versionig)** 이라 하는 버전관리 모델을 따르며, 버전 번호는 점으로 구분된 3개의 숫자로 구성됩니다`(MAJOR.MINOR.PATCH)`. 현재 문서에 사용한 버전은 솔리디티 `0.4.24` 이다. 

### Download and Install

`apt` 패키지 관리자 사용하여 `Ubuntu/Debian` OS 에 솔리디티의 최신 바이너리 릴리스를 설치할 수 있습니다.

```shell
$ sudo add-apt-repository ppa:ethereum/ethereum
$ sudo apt update
$ sudo apt install solc
```

solc 설치한 후에는 실행하여 버전을 확인할 수 있습니다.

```shell
$ solc --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
```

### Writing a Simple Solidity Program

이제 `Faucet` 컨트랙트를 솔리디티로 구현해보겠습니다. 이 예제는 현 파트에서 계속 사용할 예정입니다.

```java
// Our first contract is a faucet!
contract Faucet {

    // Give out ether to anyone who asks
    function withdraw(uint withdraw_amount) public {

        // Limit withdrawal amount
        require(withdraw_amount <= 100000000000000000);

        // Send the amount to the address that requested it
        msg.sender.transfer(withdraw_amount);
    }

    // Accept any incoming amount
    function () public payable {}

}
```

### Compiling with the Solidity Compiler (solc)

`solc` 의 인수 `--bin`, `--optimize` 를 이용하여 컨트랙트의 최적화된 바이너리를 생성합니다.

```java
$ solc --optimize --bin Faucet.sol
======= Faucet.sol:Faucet =======
Binary:
6060604052341561000f57600080fd5b60cf8061001d6000396000f300606060405260043610603e5
763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416
632e1a7d4d81146040575b005b3415604a57600080fd5b603e60043567016345785d8a00008111156
06357600080fd5b73ffffffffffffffffffffffffffffffffffffffff331681156108fc0282604051
600060405180830381858888f19350505050151560a057600080fd5b505600a165627a7a723058203
556d79355f2da19e773a9551e95f1ca7457f2b5fbbf4eacf7748ab59d2532130029
```

`solc` 가 생성한 결과는 이더리움 블록체인에서 실행될 수 있는 시리얼라이즈된 16진수 바이너리입니다.

## The Ethereum Contract ABI

`어플리케이션 바이너리 인터페이스(Application Binary Interface, ABI)` 는 두 프로그램 모듈 간 또는 운영체제와 사용자 프로그램 간의 인터페이스 입니다. ABI 는 데이터 구조와 함수가 어떻게 **기계 코드(machine code)** 에서 사용되는지 그 방법을 정의합니다. ABI 는 API 와 다릅니다. API 는 사람이 읽을 수 있는 형식인 고수준의 **소스 코드(source code)** 로  정의합니다. 따라서 ABI 는 기계 코드와 데이터를 교환하기 위해 인코딩 및 디코딩하는 기본 방법입니다.

이더리움에서 ABI 는 EVM 에서 컨트랙트 호출을 인코딩하고 트랜잭션에서 데이터를 읽는데 사용됩니다. ABI 의 목적은 컨트랙트에서 호출할 수 있는 함수를 정의하고 각 함수가 있는 인수를 받아들이고 결과를 반환하는 방법을 설명하는 것이다.

컨트랙트의 ABI 는 함수 설명 및 이벤트의 JSON 배열로 지정됩니다. 함수는 `type`, `name`, `inputs`, `outputs`, `constant`, `payable` 필드가 있는 JSON 객체이며, 이벤트 객체에는 `type`, `name`, `inputs`, `anonymous` 필드가 있습니다.

`solc` 커맨드를 이용하여 위의 예제 컨트랙트의 ABI 를 생성해보겠습니다.

```java
$ solc --abi Faucet.sol
======= Faucet.sol:Faucet =======
Contract JSON ABI
[{"constant":false,"inputs":[{"name":"withdraw_amount","type":"uint256"}], \
"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable", \
"type":"function"},{"payable":true,"stateMutability":"payable", \
"type":"fallback"}]
```

위와같이 JSON 배열을 생성하여 이 JSON 은 Faucet 컨트랙트에 접근하려는 모든 어플리케이션에 사용할 수 있습니다. ABI 를 사용하면 지갑이나 댑 브라우저 같은 어플리케이션은 올바른 인수와 인수 유형을 사용하여 Faucet 의 함수를 호출하는 트랜잭션을 생성할 수 있습니다.

### Selecting a Solidity Compiler and Language Version

솔리디티에는 프로그램이 특정 컴파일러 버전이 필요하다는 것을 컴파일러에 지시하는 **버전 pragma** 라고 하는 **컴파일러 지시문(compiler directive)** 을 제공합니다.

```java
pragma solidity ^0.4.19;
```

솔리디티는 컴파일러 버전 pragma 를 읽고 컴파일러 버전이 pragma 와 호환되지 않으면 오류가 발생합니다. 위 소스는 이 프로그램이 최소 `0.4.19` 인 컴파일러에서 컴파일 될 수 있다고 말합니다. 그러나 `^` 기호는 `0.4.19` 의 **마이너 수정(minor revision)** 으로 컴파일을 허용한다는 것을 나타냅니다.

예를 들어 `0.4.20` 은 되지만 `0.5.0` 은 안됩니다. pragma 지시문은 EVM 바이트코드로 컴파일 되지 않으며 지시문은 호환성을 검사하기 위해 컴파일러에서만 사용합니다.

prgama 지시문은 아래와 같이 추가합니다.

```java
// Version of Solidity compiler this program was written for
pragma solidity ^0.4.19;

// Our first contract is a faucet!
contract Faucet {

    // Give out ether to anyone who asks
    function withdraw(uint withdraw_amount) public {

        // Limit withdrawal amount
        require(withdraw_amount <= 100000000000000000);

        // Send the amount to the address that requested it
        msg.sender.transfer(withdraw_amount);
    }

    // Accept any incoming amount
    function () public payable {}

}
```

## Programming with Solidity

### Data Types

**부울(bool)**

논리연산자(!, &&, ||, ==, !=) 가 있는 부울 값 true 또는 false

**정수(int, uint)**

int8 에서 uint256 까지 8 bit 씩 증가하여 선언된 부호 있는 정수 및 부호 없는 (uint) 정수. 크기 접미어가 없으면 EVM 의 단어 크기를 맞추기 위해 256 bit 가 사용된다.

**고정소수점(fixed, ufixed)**

(u)fixed MxN 으로 선언된 고정 소수점 숫자. 여기서 M 은 비트 단위의 크기(8 ~ 256) 이고, N 은 소수점 이하 자릿수(최대 18) 이다.

**Address**

20 byte 이더리움 주소. address 객체에는 유용한 멤버 함수가 많이 있으며, 주요 함수는 balance(계정 잔액 반환) 와 transfer(이더 전송) 이 있다.

**Byte array (fixed)**

고정 크기의 바이트 배열로, bytes1 에서 bytes32 까지 선언된다.

**Byte array (dynamic)**

bytes 도는 string 으로 선언된 가변 크기의 바이트 배열

**Enum**

이산 값을 열거하기 위한 사용자 정의 유형

ex) `enum NAME {LABEL 1, LABEL 2 , ...`

**Arrays**

모든 유형의 고정 또는 동적 배열, 예를 들어 `uint32[][5]` 는 부호 없는 정수의 동적 배열 5개로 이루어진 고정 크기 배열이다.

**Struct**

변수 그룹화를 위한 사용자 정의 데이터 컨테이너

ex) `struct NAME {TYPE1 VARIABLE1; TYPE2 VARIABLE2; ...}`

**Mapping**

key -> value 쌍에 대한 해시 조회 테이블

ex) `mapping(KEY_TYPE => VALUE_TYPE) NAME`

이러한 데이터 타입 외에도 솔리디티는 단위를 계산하는 데 사용할 수 있는 다양한 값 리터럴을 제공합니다.

**Time units**

단위 seconds, minutes, hours, days 를 기본 단위인 seconds 의 배수로 변환하야 접미어로 사용할 수 있습니다.

**Ether units**

단위 wei, finney, szabo, ether 를 기본 단위인 wei 의 배수로 변환하야 접미어로 사용할 수 있습니다.

유닛 멀티플라이어(unit multiplier) 중 하나를 사용하여 컨트랙트의 가독성을 향상할 수 있습니다.

```java
require(withdraw_amount <= 100000000000000000);
```

이러한 형식은 읽기가 까다로운데 유닛 멀티플라이어 ether 를 사용하여 코드를 개선하여 웨이 대신 이더로 값을 표현할 수 있습니다.

```java
require(withdraw_amount <= 0.1 ether);
```

### Predefined Global Variables and Functions

컨트랙트가 EVM 에서 실행되면 몇 개의 글로벌 객체에 접근할 수 있다. 여기에는 `block`, `msg`, `tx` 객체가 포함됩니다. 

### Transaction/message call context

`msg` 객체는 이 컨트랙트 실행을 시작한 트랜잭션 호출 또는 메세지 호출(컨트랙트 발신) 입니다. 여기에는 많은 유용한 속성이 포함되어 있습니다.

**msg.sender**

발신자는 이 컨트랙트 호출을 시작한 주소를 나타냅니다. 만약 EOA 트랜잭션이 컨트랙트를 직접 호출했다면 이것튼 트랜잭션에 서명한 주소이지만, 그렇지 않으면 트랜잭션 주소가 될 것입니다.

**msg.value**

이 호출과 함께 전송된 이더의 값(웨이)입니다.

**msg.gas**

이 실행 환경의 가스 공급에 남은 가스의 양입니다. 이것은 솔리디티 `v0.4.21` 에서는 사용되지 않고 `gasleft` 함수로 대체되었습니다.

**msg.data**

이 호출의 데이터 페이로드가 컨트랙트에 포함됩니다.

**msg.sig**

함수 선택자인 데이터 페이로드의 처음 4 byte 입니다.

### Transaction context

`tx` 객체는 트랜잭션 관련 정보에 접근하는 방법을 제공합니다.

**tx.gasprice**

트랜잭션을 호출하는데 필요한 가스 가격입니다.

**tx.origin**

트랜잭션에 대한 원래 EOA 의 주소 입니다.

### Block context

`block` 객체에는 현재 블록에 대한 정보가 포함되어 있습니다.

**block.blockhash(blockNumber)**

지정된 블록 번호의 블록해시입니다. 솔리디티 `v0.4.22` 의 `blockhash` 함수로 대체되었습니다.

**block.coinbase**

현재 블록 수수료 및 보상의 수취인 주소

**block.difficulty**

현재 블록의 난이도 (PoW)

**block.gaslimit**

현재 블록에 포함된 모든 트랜잭션에 소요될 수 있는 최대 가스양

**block.number**

현재 블록 번호

**block.timestamp**

채굴자가 현재 블록에 넣은 타임스탬프

### address object

입력으로 전달되거나 컨트랙트 객체에서 형변환 되는 모든 주소에는 다음과 같은 많은 속성과 메소드가 있습니다.

**address.balance**

웨이로 표현된 주소의 잔액

**address.transfer(__amount__)**

이 주소로 금액을 전송시키는데, 오류가 발생한 경우 예외를 발생시킵니다.

**address.send(__amount__)**

`transfer` 과 마찬가지로 예외를 발생시키는 대신, 오류가 발생하면 false 를 반환

**address.call(__payload__)**

저수준 **CALL** 함수

**address.callcode(__payload__)**

`address.call` 과 같지만 컨트랙트의 코드가 주소으 ㅣ코드로 대체된 저수준 **CALLCODE** 함수입니다.

**address.delegatecall()**

`callcode` 와 같지만 현재 컨트랙트에서 볼 수 있는 전체 msg 컨텍스트가 있는 저수준 **DELEGATECALL** 함수다.

### Built-in functions

**addmod, mulmod**

모듈로 더하기 및 곱하기, 예를들어, `addmod(x, y, k)` 는 `(x + y) % k` 를 계산합니다.

**keccak256, sha256, sha3, ripemd160**

다양한 표준 해시 알고리즘을 사용하여 해시를 계산하는 함수입니다.

**ecrecover**

서명에서 메세지 서명에 사용된 주소를 복구한다.

**selfdestruct(__recipient_address__)**

현재 컨트랙트를 삭제하고 계정의 나머지 이더를 받는 사람 주소로 보냅니다.

**this**

현재 실행중인 컨트랙트의 계정 주소 입니다.

### Contract Definition

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

### Calling Other Contracts (send, call, callcode, delegatecall)

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