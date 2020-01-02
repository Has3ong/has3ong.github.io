---
title : Ethereum Transaction -2-
tags :
- Nonce
- Transaction
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

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

