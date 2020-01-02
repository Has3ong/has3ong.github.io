---
title : Ethereum Transaction -4-
tags :
- Payload
- Data
- Value
- Transaction
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Transaction Value and Data

트랜잭션의 **페이로드(payload)** 는 **값(value)** 와 **데이터(data)** 라는 2개의 필드에 포함됩니다. 트랜잭션은 value data, value, data, 모두 가지지 않는 4가지 조합이 모두 유효합니다.

값만 있는 트랜잭션은 **지급(payment)** 입니다. 데이터만 있는 트랜잭션은 **호출(invocation)** 입니다. 값과 데이터 모두를 사용한 트랜잭션은 지급과 호출이며 값과 데잍어 모두 없는 트랜잭션은 단지 가스 낭비 입니다.

이 4가지 경우를 전부 시도해보겠습니다. 먼저 출발지와 도착지를 설정합니다.

```shell
src = web3.eth.accounts[0];
dst = web3.eth.accounts[1];
```

> Example 1 - Parity wallet showing a transaction with value, but no data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: web3.toWei(0.01, "ether"), data: ""});
```

![image](https://user-images.githubusercontent.com/44635266/71664397-2957f600-2d9c-11ea-841b-9e66139751b7.png)

> Example 2 - Parity wallet showing a transaction with value and data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: web3.toWei(0.01, "ether"), data: "0x1234"});
```

![image](https://user-images.githubusercontent.com/44635266/71664399-2b21b980-2d9c-11ea-9181-321f3db20bda.png)

> Example 3 - Parity wallet showing a transaction with no value, only data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: 0, data: "0x1234"});
```

![image](https://user-images.githubusercontent.com/44635266/71664401-2c52e680-2d9c-11ea-81a4-c64c5f25c66d.png)

> Example 4 - Parity wallet showing a transaction with no value, and no data

```shell
web3.eth.sendTransaction({from: src, to: dst, value: 0, data: ""}));
```

![image](https://user-images.githubusercontent.com/44635266/71664404-2e1caa00-2d9c-11ea-9e4e-a9fb2d1e7491.png)

### Transmitting Value to EOAs and Contracts

값을 포함하는 이더리움 트랜잭션을 구성하면 지급과 동일합니다. 이러한 트랜잭션은 대상주소가 컨트랙트인지 여부에 따라 다르게 동작합니다.

EOA 주소인 경우와 블록체인의 컨트랙트로 표시되지 않는경우 이더리움은 상태 변경을 기록하여 주소 잔액에 보낸 값을 추가합니다. 이전에 주소가 표시되지 않은 경우 클라이언트 내부 상태 표현에 추가되고 잔액은 지급 금액으로 초기화됩니다.

목적지 주소가 컨트랙트면 EVM 은 컨트랙트를 실행하고 트랜잭션의 데이터 페이로드에 지정된 함수를 호출하려고 시도한다. 트랜잭션에 데이터가 없으면 EVM 은 **폴백(fallback)** 함수를 호추랗고, 해당 함수가 지급 가능하면 다음에 수행할 작업을 결정하기 위해 함수를 실행합니다.

함수가 예외 없이 성공적으로 끝나면, 컨트랙트의 상태가 이더 잔액이 증가했음을 반영하여 업데이트합니다.

### Special Transaction: Contract Creation

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

> Example 5 - Etherscan showing the contract successfully mined

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

> Example 6 - Etherscan showing the transactions for sending and receiving funds

![image](https://user-images.githubusercontent.com/44635266/71664924-45f52d80-2d9e-11ea-9613-51ad087b6207.png)