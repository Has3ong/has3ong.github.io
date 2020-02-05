---
title : Ethereum Transaction -6-
use_math: true
tags :
- Transaction
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Transaction Signing in Practice

유효한 트랜잭션을 생성하기 위해선 ECDSA 를 사용하여 메세지에 디지털 서명을 해야합니다. 트랜잭션에 서명하는 말을 곧 RLP 시리얼라이즈된 트랜잭션 데이터의 Keccak-256 해시에 서명하라는 뜻이다. 서명은 트랜잭션 자체가 아니라 트랜잭션 데이터의 해시에 적용됩니다.

발신자는 이더리움에서 트랜잭션을 발생하기 위해 반드시 다음 과정을 거쳐야 합니다.

1. **nonce**, **gasPrice**, **gasLimit**, **to**, **value**, **data**, **chainID**, **0**, **0** 의 9개 필드를 포함하는 트랜잭션 데이터 구조를 만든다.
2. RLP 로 인코딩된 트랜잭션 데이터 구조의 시리얼라이즈된 메세지를 생성한다.
3. 시리얼라이즈된 메세지의 Keccak-256 의 해시를 계산한다.
4. EOA 의 개인키로 해시에 서명하여 ECDSA 서명을 계산한다.
5. ECDSA 서명의 계산된 **v**, **r**, **s** 값을 트랜잭션에 추가한다.

특수 서명 변수 v 는 2 가지를 나타내는데, ECDSArecover 함수가 서명을 확인하는 데 도움이 되는 복구 식별자와 체인 ID 이다. v 는 27 또는 28 중 하나로 계산되거나, 체인 ID 의 2배 에 35, 36 이 더해져 계산됩니다.

## Raw Transaction Creation and Signing

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