---
title : Ethereum Smart Contracts and Solidity -3-
tags :
- Solidity
- Smart Contract
- Ethereum
- BlockChain
---

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

## Predefined Global Variables and Functions

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