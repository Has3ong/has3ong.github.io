---
title : Ethereum Transaction
tags :
- Transaction
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

트랜잭션은 EOA 에 의해 서명된 메세지인데, 이더리움 네트워크에 전송되고 이더리움 블록체인에 기록됩니다.

트랜잭션은 EVM 에서 상태 변경을 유발하거나 컨트랙트를 실행할 수 잇는 유일한 방법이다.

## The Structure of a Transaction

**직렬화된(serialized)** 트랜재션을 수신하는 각 클라이언트와 어플리케이션은 자체 내부 데이터 구조를 사용하여 트랜잭션을 메모리에 저장하며, 네트워크에서 직렬화된 트랜잭션 자체에는 존재하지 않는 메타데이터가 포함되어 있습니다.

네트워크 serialization 은 트랜잭션의 유일한 표준 형식 입니다.

아래 `Example 1` 은 이해를 돕기위한 트랜잭션 구조를 간단하게 그린겁니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/71636270-f82ed700-2c70-11ea-9a87-e322d00023a0.png)

트랜잭션은 다음 데이터를 포함하는 *serialized binary message* 입니다.

* **Nonce**
  * 발신 EOA 에 의해 발행되어 메세지 재사용을 방지하는 데 사용하는 일련번호
* **Gas Price**
  * 발신자가 지급 하는 가스의 가격(wei)
* **Gas Limit**
  * 트랜잭션을 위해 구입할 가스의 최대량
* **Recipient**
  * 목적지 이더리움 주소
* **Value**
  * 목적지에 보낼 이더의 양
* **Data**
  * 가변 길이 바이너리 데이터 페이로드
* **v, r, s**
  * EOA 의 ECDSA 디지털 서명의 3 가지 구성요소

트랜잭션 메세지의 구조는 이더리움에서 *byte-perfect data serialization* 를 위해 만들어진 **RLP(Recursive Length Prefix** 인코딩 체계를 사용하여 직렬화됩니다. 이더리움의 모든 숫자는 8bit 배수 길이의 빅엔디안 정수로 인코딩 됩니다.

트랜잭션 내부 정보를 보여주거나 사용자 인터페이스를 시각화하기 위해서는 트랜잭션 구조 이외에도 트랜잭션이나 블록체인에서 파생된 추가정보를 사용합니다.

예를 들어 발신자 EOA 를 식별하는 주소에 **발신자(from)** 데이터가 없는데, 이것은 EOA 의 공개키를 ECDSA 서명의 **v, r, s** 구성요소로부터 알아낼수 있으며, 이는 공개키를 통해 주소를 알아낼 수 있음을 의미합니다.

즉, 주소는 공개키에서 파생될 수 있습니다. 발신자 필드가 표시된 트랜잭션이라면, 시각화하는 데 사용된 소프트웨어에 의해 추가된 것이다. 클라이언트 소프트웨어에 의해 트랜잭션에 자주 추가되는 다른 메타데이터는 블록 번호와 트랜잭션 ID 를 포함합니다. 다시 말하면, 이 데이터는 트랜잭션에서 파생되며 트랜잭션 메세지 자체의 일부가 아닙니다.

## The Transaction Nonce

**Nonce** 는 트랜잭션에서 가장 중요합니다. *Mastering Ethereum* 에서는 nonce 를 아래와같이 정의합니다.

> nonce: A scalar value equal to the number of transactions sent from this address or, in the case of accounts with associated code, the number of contract-creations made by this account.

nonce 는 발신 주소의 속성이며 발신 주소의 컨텍스트 안에서만 의미를 가집니다. 하지만 논스는 명시적으로 블록체인 계정 상태에 저장되지 않고, 해당 주소에서 발생한 트랜잭션 건수를 세어서 동적으로 계산되는 값 입니다.

먼저 nonce 의 특징을 알아보고 설명하겠습니다.

* **nonce는 계정에서 보내는 트랜잭션에 할당 된 번호입니다.**
  * 거래(transaction)를 전송시 nonce는 1씩 증가합니다.
  * nonce는 계정에서 유일합니다. 동일한 nonce 가 존재 하지 않습니다.
* **트랜잭션은 순서대로 이루어져야 합니다.**
  * 현재 계정의 nonce가 1이라면, nonce가 0인 트랜잭션을 전송할 수 없습니다. (오류발생 : 순서를 역행할 수 없습니다.)
* **순번을 건너 뛰지 않습니다.**
  * nonce 는 순차적으로 증가하고 처리되기 때문에 nonce 가 3인 트랜잭션을 전송하려면, nonce의 값 0~2까지 전송한 내역이 있어야 합니다.

```shell
예)최초 계정 생성시 nonce는 0 (계정 기준으로 전송된 트랜잭션이 하나도 없을때 )

전송한 Transaction1 : 1(nonce)
전송한 Transaction2 : 2(nonce)
전송한 Transaction3 : 3(nonce)
.
…
……
전송한 Transaction10 : 10(nonce)
```

nonce는 중복되지 않고 순차적이기 때문에, 같은 nonce 에 여러 트랜잭션 전송이 발생하였다면 해당 nonce 중 제일 높은 가스비를 지불한 트랜잭션이 처리됩니다. 이더리움에서는 이러한 방법으로 이중 지불 문제를 방지합니다.

### Keeping Track of Nonces

nonce 값을 알기 위해선 web3 인터페이스를 통해 블록체인을 조회하면 됩니다. 또한, 사용자의 지갑은 그 지갑에서 관리하는 각 주소에 대한 nonce 를 추적합니다. 하나의 지갑에서만 트랜잭션을 만드는 경우에는 nonce 추적이 간단합니다.

하나의 지갑에서 트랜잭션을 만들 때마다 시퀀스상 다음 차례 nonce 값을 부여합니다. 하지만 이것이 컨펌될 때 까지는 `getTransactonCount` 에 포함되지 않습니다.

예시를 통해 알려드리겠습니다.

```shell
> web3.eth.getTransactionCount("0x9e713963a92c02317a681b9bb3065a8249de124f", "pending")
40

> web3.eth.sendTransaction({from: web3.eth.accounts[0], to: "0xB0920c523d582040f2BCB1bD7FB1c7C1ECEbdB34", value: web3.toWei(0.01, "ether")});

> web3.eth.getTransactionCount("0x9e713963a92c02317a681b9bb3065a8249de124f", "pending")
41

> web3.eth.sendTransaction({from: web3.eth.accounts[0], to: "0xB0920c523d582040f2BCB1bD7FB1c7C1ECEbdB34", value: web3.toWei(0.01, "ether")});

> web3.eth.getTransactionCount("0x9e713963a92c02317a681b9bb3065a8249de124f", "pending")
41

> web3.eth.sendTransaction({from: web3.eth.accounts[0], to: "0xB0920c523d582040f2BCB1bD7FB1c7C1ECEbdB34", value: web3.toWei(0.01, "ether")});

> web3.eth.getTransactionCount("0x9e713963a92c02317a681b9bb3065a8249de124f", "pending")
41
```

유저가 보낸 트랜잭션은 트랜잭션 nonce 를 41로 늘렸고 현재 상태는 보류 중 입니다. 하지만 우리가 연속적으로 3 번 더 트랜잭션을 보냈을때 `getTransactonCount` 은 트랜잭션을 세지 않았습니다.

유저는 mempool 에 보류 중인 트랜잭션 3개가 있을 것이라고 생각하지만, 하나의 트랜잭션만 대기중입니다. 네트워크 통신이 완료될 때까지 몇 초를 기다린 후에 `getTransactonCount` 를 호출하면 예쌍했던 숫자를 반환해 줄것입니다.

### Gaps in Nonces, Duplicate Nonces, and Confirmation

이더리움 네트워크는 nonce 에 따라 트랜잭션을 순차적으로 처리한다. 즉, nonce 가 0인 트랜잭션을 전송한 다음 nonce 가 2인 트랜잭션을 전송하면, 2 번째 트랜잭션은 어떤 블록에도 포함되지 않습니다. 이더리움 네트워크가 누락된 nonce 가 나타날 때까지 기다리는 동안 2 번째 트랜잭션은 mempool 에 저장됩니다.

다음 nonce 가 1인 누락된 트랜잭션을 전송하면, 두 트랜잭션이 처리되고 블록에 포함됩니다. gap 을 메우면 네트워크 mempool 에서 보유한 순서가 잘못된 트랜잭션을 처리할 수 있습니다.

또한, nonce 가 같지만 수신자나 값이 다른 2개의 트랜잭션이 전송하여 nonce 의 중복이 일어나면, 그 중 하나가 확정되고 하나는 거부됩니다. 어떤 트랜잭션이 확정되는지는 트랜잭션이 첫 유효 노드에 달성하는 순서에 따라 결정됩니다. 즉, 무작위입니다.

## Transaction Gas

Gas 는 이더리움의 연료입니다. 가스는 이더가 아니라 이더에 대한 자체 환율을 가진 별도의 가상화폐라고 보시면 됩니다. 이더리움 은 가스를 사용하여 트랜잭션이 사용할 수 있는 자원의 양을 제어합니다.

가스는 이더 가치의 급격한 변화와 함께 발생할 수 있는 변동성으로부터 시스템을 보호하고, 가스가 지급하는 다양한 자원의 비용사이의 중요하고 민감한 비율을 관리하기 위해 가스를 이더와 분리합니다.

트랜잭션의 `gasPrice` 필드는 트랜잭션 생성자가 가스와 교환하여 지급할 가격을 설정할 수 있게합니다. 가격은 가스 단위당 wei 단위로 측정됩니다.

지갑은 신속한 트랜잭션 컨펌을 위해 `gasPrice` 를 조정할 수 있습니다. `gasPrice` 가 높을수록 트랜잭션이 더 빨리 컨펌될것이며, 우선순위가 낮은 트랜잭션은 낮은 가격을 설정하여 컨펌이 느려지게 할 수 있습니다. `gasPrice` 가 설정할 수 있는 최솟값은 0이고, 이것은 수수료 없는 트랜잭션을 의미합니다. 블록 공간에 대한 수요가 낮은 기간에는 수수료가 0인 트랜잭션도 블록에 포함될 수 있습니다.

> gasPrice 가 0인경우 지갑이 완전히 무료 트랜잭션을 생성할 수 있음을 의미한다.

web3 인터페이스를 이용하여 여러 블록에 걸친 중간 가격을 계산하여 `gasPrice` 를 제안하는 기능을 제공한다.

```shell
> web3.eth.getGasPrice(console.log)
> null BigNumber { s: 1, e: 10, c: [ 10000000000 ] }
```

가스와 관련된 2 번째 중요한 필드는 `gasLimit` 입니다. 간단히 말하면 트랜잭션을 완료하기위해 트랜잭션을 시도하는 사람이 기꺼이 구매할 수 있는 최대 가스 단위 수를 제공합니다.

하나의 EOA 에서 다른 EOA 로 이더를 전송하는 트랜잭션을 의미하며, 필요한 가스 양은 21,000 개의 가스 단위로 고정됩니다. 얼마나 많은 양의 이더가 소비되는지 알고싶으면 지급하고자 하는 `gasPrice`에 21,000 을 곱하면 됩니다.


```shell
> web3.eth.getGasPrice(function(err, res) {console.log(res*21000)} )
> 210000000000000
```

## Transaction Recipient

to 필드에 트랜잭션 수신자가 지정이 된다. 이것은 20 byte 이더리움 주소를 포함합니다. 주소는 EOA 또는 컨트랙트에 주소일 수 있습니다.

이더리움은 이 필드를 검증하지 않습니다. 모든 20 byte 값은 유효한 것으로 간주합니다. 20 byte 값이 개인키가 없거나 상응하는 컨트랙트가 없는 주소의 경우에도 트랜잭션은 여전히 유효합니다. 이더리움은 주소가 공개키에서 올바르게 파생되었는지 여부를 알 수 있는 방법이 없습니다.

> 이더리움 프로토콜은 트랜잭션의 수신자 주소를 검증하지 않습니다. 해당하는 개인키 또는 컨트랙트가 없는 주소로 보내질 수 있습니다. 그러면 이더가 burning 되어 영구적으로 사용할 수 없게됩니다. 유효성 검사는 사용자 인터페이스 수준에서 수행되어야 합니다.

이더를 연소시키는 데는 여러가지 정당한 이유가 있을 수 있습니다. 예를 들면, 지급 채널 및 기타 스마트 컨트랙트에서의 부정행위를 저지하는 것이나, 이더의 양이 유한하므로 이더를 연소시키면 모든 이더 보유자에게 연소된 값을 효과적으로 분배한 것으로 이해할 수 있습니다.

## Transaction Value and Data

트랜잭션의 **페이로드(payload)** 는 **값(value)** 와 **데이터(data)** 라는 2개의 필드에 포함됩니다. 트랜잭션은 value data, value, data, 모두 가지지 않는 4가지 조합이 모두 유효합니다.

값만 있는 트랜잭션은 **지급(payment)** 입니다. 데이터만 있는 트랜잭션은 **호출(invocation)** 입니다. 값과 데이터 모두를 사용한 트랜잭션은 지급과 호출이며 값과 데잍어 모두 없는 트랜잭션은 단지 가스 낭비 입니다.

이 4가지 경우를 전부 시도해보겠습니다. 먼저 출발지와 도착지를 설정합니다.

```shell
src = web3.eth.accounts[0];
dst = web3.eth.accounts[1];
```

> Example 2 - Parity wallet showing a transaction with value, but no data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: web3.toWei(0.01, "ether"), data: ""});
```

![image](https://user-images.githubusercontent.com/44635266/71664397-2957f600-2d9c-11ea-841b-9e66139751b7.png)

> Example 3 - Parity wallet showing a transaction with value and data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: web3.toWei(0.01, "ether"), data: "0x1234"});
```

![image](https://user-images.githubusercontent.com/44635266/71664399-2b21b980-2d9c-11ea-9181-321f3db20bda.png)

> Example 4 - Parity wallet showing a transaction with no value, only data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: 0, data: "0x1234"});
```

![image](https://user-images.githubusercontent.com/44635266/71664401-2c52e680-2d9c-11ea-81a4-c64c5f25c66d.png)

> Example 5 - Parity wallet showing a transaction with no value, and no data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: 0, data: ""}));
```

![image](https://user-images.githubusercontent.com/44635266/71664404-2e1caa00-2d9c-11ea-9e4e-a9fb2d1e7491.png)

### Transmitting Value to EOAs and Contracts

값을 포함하는 이더리움 트랜잭션을 구성하면 지급과 동일합니다. 이러한 트랜잭션은 대상주소가 컨트랙트인지 여부에 따라 다르게 동작합니다.

EOA 주소인 경우와 블록체인의 컨트랙트로 표시되지 않는경우 이더리움은 상태 변경을 기록하여 주소 잔액에 보낸 값을 추가합니다. 이전에 주소가 표시되지 않은 경우 클라이언트 내부 상태 표현에 추가되고 잔액은 지급 금액으로 초기화됩니다.

목적지 주소가 컨트랙트면 EVM 은 컨트랙트를 실행하고 트랜잭션의 데이터 페이로드에 지정된 함수를 호출하려고 시도한다. 트랜잭션에 데이터가 없으면 EVM 은 **폴백(fallback)** 함수를 호추랗고, 해당 함수가 지급 가능하면 다음에 수행할 작업을 결정하기 위해 함수를 실행합니다.

함수가 예외 없이 성공적으로 끝나면, 컨트랙트의 상태가 이더 잔액이 증가했음을 반영하여 업데이트합니다.

## Special Transaction: Contract Creation

특별한 트랜잭션 경우중 하나는 **새로운 컨트랙트** 를 만들어 향후 사용을 위해 배포하는 트랜잭션입니다. 컨트랙트 생성 트랜잭션은 **제로 어드레스** 라고 하는 특수 대상 주소로 전송됩니다. 컨트랙트 등록 트랜잭션의 to 필드는 0x0 주소를 포함합니다. 이 주소는 EOA 나 컨트랙트를 나타내지 않습니다. 이 필드는 목적지로만 사용되며 컨트랙트 작성을 위해 사용됩니다.

제로 어드레스는 컨트랙트 생성에만 사용하려는 의도로 만들었지만 이더 손실이나 이더 연소에도 사용할 수 있습니다. 하지만 이더 연소를 사용할 때는 네트워크에 의도를 분명이 하고 지정된 주소를 사용해야 합니다.

> 연소 주소로 보내진 이더는 영원히 사라집니다.

데이터 페이로드에서 컨트랙트를 사용하여 트랜잭션을 수동으로 생성하여 컨트랙트를 생성할 수 있습니다. 컨트랙트는 바이트코드 표현으로 컴파일 해야하며, 이것은 솔리디티로 컴파일 할 수 있습니다.

```shell
$ solc --bin Faucet.sol

Binary:
6060604052341561000f57600080fd5b60e58061001d6000396000f30060606040526004361060...
```

아래와 같이 똑같은 정보를 얻을 수 있습니다.

```shell
> src = web3.eth.accounts[0];
> faucet_code = \
  "0x6060604052341561000f57600080fd5b60e58061001d6000396000f300606...f0029";
> web3.eth.sendTransaction({from: src, to: 0, data: faucet_code, \
  gas: 113558, gasPrice: 200000000000});

"0x7bcc327ae5d369f75b98c0d59037eec41d44dfae75447fd753d9f2db9439124b"
```

실수로 0x0 에 이더를 보내고 그것을 영원히 잃는 데 드는 비용이 많기 때문에, 제로 어드레스 컨트랙트 생성 시에는 to 파라미터를 지정하는 것이 좋습니다.

> Example 6 - Etherscan showing the contract successfully mined

![image](https://user-images.githubusercontent.com/44635266/71664923-442b6a00-2d9e-11ea-805b-e8a1799521d1.png)

컨트랙트에 대한 정보가 담겨져 있는 트랜잭션 영수증을 확인할 수 있습니다.

```shell
> eth.getTransactionReceipt("0x7bcc327ae5d369f75b98c0d59037eec41d44dfae75447fd753d9f2db9439124b");

{
  blockHash: "0x6fa7d8bf982490de6246875deb2c21e5f3665b4422089c060138fc3907a95bb2",
  blockNumber: 3105256,
  contractAddress: "0xb226270965b43373e98ffc6e2c7693c17e2cf40b",
  cumulativeGasUsed: 113558,
  from: "0x2a966a87db5913c1b22a59b0d8a11cc51c167a89",
  gasUsed: 113558,
  logs: [],
  logsBloom: "0x00000000000000000000000000000000000000000000000000...00000",
  status: "0x1",
  to: null,
  transactionHash: "0x7bcc327ae5d369f75b98c0d59037eec41d44dfae75447fd753d9f2db9439124b",
  transactionIndex: 0
}
```

컨트랙트 주소가 포함되어 있습니다.

```shell
> contract_address = "0xb226270965b43373e98ffc6e2c7693c17e2cf40b"
> web3.eth.sendTransaction({from: src, to: contract_address, value: web3.toWei(0.1, "ether"), data: ""});

"0x6ebf2e1fe95cc9c1fe2e1a0dc45678ccd127d374fdf145c5c8e6cd4ea2e6ca9f"

> web3.eth.sendTransaction({from: src, to: contract_address, value: 0, data: "0x2e1a7d4d000000000000000000000000000000000000000000000000002386f26fc10000"});

"0x59836029e7ce43e92daf84313816ca31420a76a9a571b69e31ec4bf4b37cd16e"
```

> Example 7 - Etherscan showing the transactions for sending and receiving funds

![image](https://user-images.githubusercontent.com/44635266/71664924-45f52d80-2d9e-11ea-9613-51ad087b6207.png)

## Digital Signatures

디지털 서명은 네트워크에서 송신자의 신원을 증명하는 방법으로, 송신자가 자신의 비밀키로 암호화한 메시지를 수신자가 송신자의 공용 키로 해독하는 과정이다.

### The Elliptic Curve Digital Signature Algorithm

이더리움에서 사용하는 디지털 서명 알고리즘은 ECDSA 입니다. 타원 곡선의 **개인키 - 공개키** 쌍을 기반으로 합니다.

디지털 서명은 이더리움에서 3 가지 용도로 사용이됩니다.

1. 이더리움 계정과 개인키의 소유자가 이더 지출 또는 컨트랙트 이행을 **승인**했음을 증명
2. **부인방지(non-repudiation)** 보장
3. 트랜잭션 데이터를 **수정할 수 없음**을 증명

### How Digital Signatures Work

디지털 서명은 2 단계로 구성된 수학적 체계입니다. 1 번째 부분은 메세지에서 개인키를 사용하여 서명을 만드는 알고리즘입니다. 2 번째 부분은 누구나 메세지와 공개키만 사용하여 서명을 검증할 수 있게 하는 알고리즘 입니다.

### Creating a digital signature

이더리움의 ECDSA 구현에서 서명된 메세지는 트랜잭션 입니다. 트랜잭션의 RLP 로 인코딩된 데이터의 Keccak-256 의 해시입니다. 서명 키는 EOA 의 개인키입니다.

$$Sig = F_{sig}(F_{keccak256}(m),k)$$

* **k** : 서명 개인키
* **m** : RLP 인코딩된 트랜잭션
* $F_{keccak256}$ : Keccak-256 해시 함수
* $F_{sig}$ : 서명 알고리즘
* **Sig** : 결과 서명

함수 $F_{sig}$ 는 일반적으로 r 및 s 라고 하는 두 값으로 구성된 서명 Sig 를 생성합니다.

$$Sig = (r,s)$$

### Verifying the Signature

서명을 확인하려면 서명(r, s) 과 시리얼라이즈된 트랜잭션 그리고 서명을 만드는데 사용된 개인키에 상응하는 공개키가 있어야 한다. 서명 확인은 공개키를 생성한 개인키의 소유자만이 트랜잭션에서 서명을 생성할 수 있다.

서명 알고리즘은 메세지, 서명자의 공개키 및 서명을 가져와서 서명이 메세지와 공개키에 유효하면 true 를 반환합니다.

### ECDSA Math

서명은 2개의 r과 s로 구성된 서명을 생성하는 수학 함수 F_{sig} 에 의해 생성됩니다.

서명 알고리즘은 처음에는 일시적인 개인키를 암호학적인 안전한 방법으로 생성합니다. 이 임시 키는 이더리움 네트워크에서 서명된 트랜잭션을 보는 공격자가 발신자의 실제 개인키를 계산할 수 없도록 r 및 s 값을 계산하는데 사용합니다.

이 방법은 다음과 같은 이점이 있습니다.

* 임시 개인키로 사용되는 암호학적으로 안전한 난수 q
* q 로부터 생성된 상응하는 임시 공개키 Q와 타원곡선 생성자 점 G

디지털 서명의 r 값은 일시적인 공개키 Q 의 x 좌표 입니다.

여기서 알고리즘은 다음과 같이 서명의 s 값을 계산합니다.

$$s \equiv q^{-1}(Keccak256(m) + r*k) \quad(mod\,p)$$

* **q** : 일시적인 개인키
* **r** : 일시적인 공개키 x 의 좌표
* **k** : 서명 개인키
* **m** : 트랜잭션 데이터
* **p** : 타원 곡선의 소수 차수

검증은 r 및 s 값과 보낸 사람의 공개키를 사용하여 타원 곡선의 한 지점인 값 Q 를 계산하는, 서명 생성 함수의 반대 프로세스입니다. 단계는 다음과 같습니다.

1. 모든 입력이 올바르게 구성되어있는지 확인한다.
2. $w=s^{-1}mod\,p$ 를 계산
3. $u_1 = Keccak256(m) *w \,mod\, p$ 를 계산
4. $u_2 = r*w\, mod\,p를 계산
5. 타원 곡선을 계산한다.$

$$Q \equiv u_1* G + u_2 * K\;(mod\,p)$$

* **r, s** : 서명 값
* **K** : 서명자의 공개키
* **m** : 서명된 트랜잭션 데이터
* **G** : 타원 곡선 생성자 점
* **p** : 타원 곡선의 소수 차수

계산된 포인트 Q의 x 좌표가 r 과 같으면, 검증자는 서명이 유효하다고 결론을 내릴 수 있습니다.

### Transaction Signing in Practice

유효한 트랜잭션을 생성하기 위해선 ECDSA 를 사용하여 메세지에 디지털 서명을 해야합니다. 트랜잭션에 서명하는 말을 곧 RLP 시리얼라이즈된 트랜잭션 데이터의 Keccak-256 해시에 서명하라는 뜻이다. 서명은 트랜잭션 자체가 아니라 트랜잭션 데이터의 해시에 적용됩니다.

발신자는 이더리움에서 트랜잭션을 발생하기 위해 반드시 다음 과정을 거쳐야 합니다.

1. **nonce**, **gasPrice**, **gasLimit**, **to**, **value**, **data**, **chainID**, **0**, **0** 의 9개 필드를 포함하는 트랜잭션 데이터 구조를 만든다.
2. RLP 로 인코딩된 트랜잭션 데이터 구조의 시리얼라이즈된 메세지를 생성한다.
3. 시리얼라이즈된 메세지의 Keccak-256 의 해시를 계산한다.
4. EOA 의 개인키로 해시에 서명하여 ECDSA 서명을 계산한다.
5. ECDSA 서명의 계산된 **v**, **r**, **s** 값을 트랜잭션에 추가한다.

특수 서명 변수 v 는 2 가지를 나타내는데, ECDSArecover 함수가 서명을 확인하는 데 도움이 되는 복구 식별자와 체인 ID 이다. v 는 27 또는 28 중 하나로 계산되거나, 체인 ID 의 2배 에 35, 36 이 더해져 계산됩니다.

### Raw Transaction Creation and Signing

아래 코드는 원시 트랜잭션을 생성하고 `ethereu,js-tx` 라이브러리를 사용하여 서명합니다. 일반적으로 사용자를 대신해서 트랜잭션에 서명을 하는 지갑 또는 어플리케이션의 함수가 어떻게 작동하는지를 보여줍니다.

```shell
// Load requirements first:
//
// npm init
// npm install ethereumjs-tx
//
// Run with: $ node raw_tx_demo.js
const ethTx = require('ethereumjs-tx');

const txData = {
  nonce: '0x0',
  gasPrice: '0x09184e72a000',
  gasLimit: '0x30000',
  to: '0xb0920c523d582040f2bcb1bd7fb1c7c1ecebdb34',
  value: '0x00',
  data: '',
  v: "0x1c", // Ethereum mainnet chainID
  r: 0,
  s: 0 
};

tx = new ethTx(txData);
console.log('RLP-Encoded Tx: 0x' + tx.serialize().toString('hex'))

txHash = tx.hash(); // This step encodes into RLP and calculates the hash
console.log('Tx Hash: 0x' + txHash.toString('hex'))

// Sign transaction
const privKey = Buffer.from(
    '91c8360c4cb4b5fac45513a7213f31d4e4a7bfcb4630e9fbf074f42a203ac0b9', 'hex');
tx.sign(privKey);

serializedTx = tx.serialize();
rawTx = 'Signed Raw Transact
```

예제 코드를 실행하면 다음과 같은 결과가 생성됩니다.

```shell
$ node raw_tx_demo.js
RLP-Encoded Tx: 0xe6808609184e72a0008303000094b0920c523d582040f2bcb1bd7fb1c7c1...
Tx Hash: 0xaa7f03f9f4e52fcf69f836a6d2bbc7706580adce0a068ff6525ba337218e6992
Signed Raw Transaction: 0xf866808609184e72a0008303000094b0920c523d582040f2bcb1...
```

### Raw Transaction Creation with EIP-155

*EIP-155 Simple Replay Attack Protection* 표준은 서명하기 전에 트랜잭션 데이터 내부에 **체인 식별자(chain identifier)** 를 포함하여 재생공격 방지가 가능한 트랜잭션 인코딩을 지정한다. 이렇게 하면 하나의 블록체인에 대해 생성된 트랜잭션이 다른 블록체인에서 유효하지 않습니다. 따라서 표준의 이름 그대로 한 네트워크에서 전파된 트랜잭션은 다른 네트워크에서 재생될 수 없습니다.

EIP-155 는 트랜잭션 데이터 구조의 주요 6개 필드에 **체인식별자, 0, 0** 의 3개 필드를 추가합니다. 이 3필드는 인코딩되고 해싱되기 전에 트랜잭션 데이터에 추가됩니다.  따라서 트랜잭션의 해시가 변경되어 나중에 서명이 적용됩니다. 체인 식별자가 서명한 데이터에 포함됨으로써, 트랜잭션 서명은 체인 식별자가 수정되면 서명이 무효화되어 데이터 변경을 식별할 수 있다. 따라서 EIP-155 는 서명의 유효성이 체인 식별자에 의존하기 때문에 다른 체인에서 트랜잭션을 재생할 수 없습니다.

> Chain identifiers

|Chain|Chain ID|
|:--:|:--:|
|Ethereum mainnet|1|
|Morden (obsolete), Expanse|2|
|Ropsten|3|
|Rinkeby|4|
|Rootstock mainnet|30|
|Rootstock testnet|31|
|Kovan|42|
|Ethereum Classic mainnet|61|
|Ethereum Classic testnet|62|
|Geth private testnets|1337|

결과로 생성되는 트랜잭션 구조는 RLP 로 인코딩되고 해싱되고 서명됩니다. 서명 알고리즘은 v 접두어에 체인 식별자를 인코딩하기 위해 약간 수정됩니다.

### The Signature Prefix Value (v) and Public Key Recovery

서명자의 공개키를 복구하는 프로세스를 **공개키 복구(public key recovery)** 라고 합니다.

먼저 서명에 있는 x 좌표인 r 값에서 2개의 타원 곡선 점 $R$ 과 $R^`$ 를 계산 합니다. 타원 곡선은 x 축에 대칭이므로, 어떤 값 x 에 대해서도 곡선에 2개의 가능한 값이 있기 때문에 2개의 점이 있습니다.

r 에서 우리는 r 의 곱셈 역함수인 $r^{-1}$ 를 계산합니다.

마지막으로 메세지 해시의 m 최하위 비트인 z 를 계산합니다. 여기서 n 은 타원 곡선의 차수입니다. 그결과 가능한 공개키는 다음과 같습니다.

$$K_1 = r^{-1}(sR-zG)\\
K_2 = r^{-1}(sR-zG)$$

* $K_1$ 과 $K_2$ 는 서명자의 2 가지 가능한 공개키
* $r^{-1}$ 은 서명 $r$ 곱셈 역함수 
* s 는 서명의 $s$ 값
* $R$ 과 $R^`$ 는 ㄷ2가지 가능한 일시적인 공개키 $Q$
* z 는 메세지 해시의 n 최하위 비트
* G 는 타원 곡선 생성자 점

좀 더 효율적으로 접근하기 위해, 트랜잭션 서명에는 2개의 가능한 R 값 중 임시 공개키가 무엇인지 알려주는 접두어 값 v 가 포함됩니다. v 가 짝수이면 $R$ 이 올바른 값이고, v 가 홀수이면 $R^`$ 입니다. 이런식으로 각각 하나의 값만 계산해야 합니다.


### Separating Signing and Transmission

트랜잭션이 서명되면 트랜잭션은 이더리움 네트워크로 전송할 준비가 됩니다. 트랜잭션 생성, 서명, 브로드캐스트의 3 단계는 일반적으로 단일 작업에 의해 처리됩니다. 하지만, 2 단계로 나누어 트랜잭션을 생성하고 서명합니다.

서명된 트랜잭션이 있으면 `web3.eth.sendSignedTransaction` 을 사용하여 트랜잭션을 16 진수로 인코딩하고 서명해서 이더리움 네트워크에서 전송할 수 있습니다.

트랜잭션의 서명과 전송을 분리하는 보편적인 이유는 보안입니다. 트랜잭션에 서명하는 컴퓨터에는 잠금 해제된 개이니가 메모리에 로드되어 있어야 합니다. 전송을 수행하는 컴퓨터는 인터넷에 연결되어 있어야 하며, 이더리움 클라이언트를 실행해야 합니다. 이 2 기능이 하나의 컴퓨터에 있으면 온라인 시스템에 개인키가 있게 되며, 이는 위험한 상황입니다.

따라서 서명 및 전송 기능을 분리하여 각기 다른 시스템(offline, online) 에서 수행하는 것을 **오프라인 서명(offline signing)** 이라 하며, 이는 일반적인 보안 방법 입니다.

아래 `Example 8` 은 이더리움 트랜잭션의 오프라인 서명 프로세스를 보여줍니다.

> Example 8 - Offline signing of Ethereum transactions

![image](https://user-images.githubusercontent.com/44635266/71893186-3c006f80-318e-11ea-9b28-7a2264a8ae04.png)

1. 현재의 nonce 및 사용 가능한 자금을 검색할 수 있는 계정에서 서명되지 않은 트랜잭션을 온라인 컴퓨터에 만듭니다.
2. 서명되지 않은 트랜잭션을 QR 코드 또는 USB 를 통해 트랜잭션 서명을 위한 air-gapped 오프라인 장치로 전송한다.
3. 이더리움 블록체인에 브로드캐스트하기 위해, 서명된 트랜잭션을 QR 코드 또는 USB 를 통해 온라인 장치로 전송한다.

필요한 보안 수준에 따라 격리되고 방화벽이 있는 서브넷 에서 에어 갭 시스템으로 알려진 오프라인 시스템에 이르기까지 온라인 컴퓨터와 분리 정도를 다르게 할 수 있습니다.

에어 갭 시스템에서는 네트워크 연결이 없습니다. 트랜잭션에 서명하려면 데이터 저장 매체 또는 웹캠과 QR 코드를 사용하여 에어 갭 컴퓨터와 주고받는 트랜잭션을 생성합니다. 물론 이것은 서명하고자 하는 모든 트랜잭션을 수동으로 전송해야 하며 스케일링할 수 없습니다.

에어 갭 시스템을 많이 사용할 수 없지만 약간의 격리로도 많은 보안 이점을 얻을 수 있습니다. 예를들어 메세지 대기열 프로토콜만 허용하는 방화벽이 있는 격리된 서브넷은 온라인 시스템에 서명하는 것보다 공격할 부분을 줄어들게 하고 훨씬 높은 보안을 제공할 수 있습니다.

### Transaction Propagation

이더리움 네트워크는 **플러드 라우팅(flood routing)** 프로토콜을 사용합니다. 이더리움 클라이언트는 **메시(mesh)** 네트워크를 형성하는 **피어투피어(P2P)** 네트워크에서 **노드(node)** 역할을 합니다. 어떠한 네트워크 노드도 특별하지 않습니다. 노드란 네트워크에 연결되어 참여하는 모든 이더리움 클라이언트 입니다.

트랜잭션 전파는 서명된 트랜잭션을 생성한 이더리움 노드에서 시작합니다. 트랜잭션은 검증된 후에 트랜잭션을 생성한 직접 연결한 다른 모든 이더리움 노드로 전송됩니다.

평균적으로 각 이더리움 노드는 **이웃(neighbor)** 이라고 불리는 13개의 다른 노드에 대한 연결을 유지합니다. 각 이웃 노드는 트랜잭션을 수신하자마자 즉시 유효성을 검사합니다. 그리고 노드가 검증에 동의하면 사본을 저장하고 모든 이웃에게 전파합니다. 결과적으로 트랜잭션은 네트워크의 모든 노드가 트랜잭션 사본을 가질 때까지 원래 노드에서 *물결치며 퍼진다(flooding)* 노드는 전달하는 메세지를 필터링 할 수 있지만, 기본 규칙은 전달 받은 모든 유효한 트랜잭션 메세지를 전파하는 것입니다.

각 노드의 관점에서 보면 트랜잭션의 출처를 식별할 수 없습니다. 노드로 전송한 이웃 노드는 트랜잭션의 생성자이거나 인접 노드 중 하나로부터 트랜잭션을 수신했을 수 있습니다. 트랜잭션의 출처를 추적하거나 전파를 방해하기 위해 공격자는 모든 노드 중 상당 부분을 제어해야 합니다. 이것은 P2P 네트워크의 보안 및 개인정보 보호 설계의 일부이며, 특히 블록체인 네트워크에 적용됩니다.

### Recording on the Blockchain

이더리움의 모든 노드는 동등한 피어지만, 일부는 채굴을 하며 GPU 가 장착된 컴퓨터인 **채굴 팜(mining farm)** 에 트랜잭션 및 블록을 제공합니다. 채굴 컴퓨터는 트랜잭션을 후보 블록에 추가하고 후보 블록을 유효하게 만드는 **작업증명(PoW)** 를 찾으려고 시도합니다.

유효한 트랜잭션이 결국 트랜잭션 블록에 포함되어 이더리움 블록체인에 기록됩니다. 트랜잭션이 블록으로 채워지면 계정의 잔액을 수정하거나 내부 상태를 변경하는 컨트랙트를 호출하여 트랜잭션은 이더리움 싱글톤 상태를 수정합니다. 이러한 변경사항은 트랜잭션 **영수증(receipt)** 형식으로 트랜잭션과 기록됩니다.

생성에서 EOA 에 의한 서명, 전파, 그리고 채굴까지 완료된 트랜잭션은 싱글톤의 상태를 변경하고 블록체인에서 지울 수 없는 기록을 남깁니다.

### Multiple-Signature (Multisig) Transactions

여러명의 유저 당사자가 트랜잭션에 서명할 때만 자금을 사용할 수 있는 **비트코인 다중 서명(multiple signature, multisig)** 계정을 만들 수 있다. 이더리움의 기본 EOA 값 트랜잭션에는 다중 서명 조항이 없습니다. 그러나 이더와 토큰을 전송하는 어떤 조건들도 처리할 수 있는 스마트 컨트랙트를 사용하여 임의의 서명 룰을 적용할 수 있습니다.

스마트 컨트랙트로 다중 서명 트랜잭션을 구현하는 기능은 이더리움의 유연성을 입증합니다. 그러나 이러한 유연성으로 인해 다중 서명 체계의 보안을 약화시키는 버그가 발생할 수 있으므로 양날의 검입니다. 실제로 간단한 *M - of - N* 다중 서명 구성을 스마트 컨트랙트를 이용하지 않고 EVM 에서 직접 다중 서명 명령을 처리하게 하자는 제안이 많습니다. 이는 핵심 합의 규칙의 일부이며, 강력하고 안전한 것으로 입증된 비트코인의 다중 서명 시스템과 동일합니다.