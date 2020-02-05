---
title : Ethereum Cryptography -1-
tags :
- Cryptography
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Cryptography

이더리움의 기반 기술중 하나는 **암호학(Cryptography)** 입니다. 암호학은 데이터 지식을 증명하거나 진위성을 증명하는데 사용할 수 있습니다.

암호화 증명은 이더리움 플랫폼의 작동을 위한 중요한 수학도구이며, 이더리움 어플리케이션에 광범위하게 사용이 됩니다.

### Keys and Addresses

이더리움은 **외부 소유 계정(Externally Owned Account, EOA)** 와 **컨트랙트(contract)** 라는 두가지 계정을 가지고 있습니다. 디지털 **개인키(private key)**, **이더리움 주소(Ethereum address)**, **디지털 서명(Digital Signature)** 을 통해 외부 소유 계정의 이더 소유권을 확립합니다. 개인 키는 모든 사용자와 이더리움 간 상호작용의 핵심입니다. 계정 주소는 개인키에서 직접 파생이되며, 개인키는 계정이라고 불리는 단일 이더리움 주소를 고유하게 정해줍니다.

이더리움 시스템은 개인키를 이더리움에 전송하거나 저장하는 방식으로 직접 사용하지 않습니다. 개인키는 항상 비공개로 유지되어야 하며 이더리움 체인에 저장되어서도 안됩니다. 계정 주소와 디지털 서명만 시스템에 전송되고 저장됩니다.

개인키를 사용하여 생성된 디지털 서명을 통해 자금의 접근과 통제가 이루어집니다. 이더리움 트랜잭션은 유효한 디지털 서명이 블록체인에 있어야 합니다. 왜냐하면 개인키의 사본을 누군가 가지게되면 해당 계정과 이더를 제어할 수 있기 때문입니다. 사용자가 자신의 개인키를 안전하게 유지한다면, 이더리움 트랜잭션의 디지털 서명은 개인키의 소유권을 증명하기에 자금의 실제 소유자임도 증명하게 됩니다.

이더리움에서 똑같이 사용하는 암호화 시스템에서는 개인키와 공개키로 구성된 쌍으로 제공을 합니다. 개인키 자체는 이더리움 사용자에게 보여주지 않으며, 대부분 암호화된 형태로 파일로 저장하고 이더리움 지갑 SW 관리한다.

### Public Key Cryptography and Cryptocurrency

공개키 암호화는 정보보안의 핵심입니다. 공개키 암호화는 고유한 키를 사용하여 정보를 보호합니다. 이 키는 **inverse(수학의 역)** 를 계산하기 어렵다는 수학 함수를 바탕으로 합니다. 이 함수를 바탕으로 디지털 비밀과 위조 불가능한 디지털 서명을 만들 수 있게 합니다.

예를 들어, 2개의 큰 소수를 곱하는 것은 간단합니다. 하지만 8,0818,009 라는 숫자를 제시하고 이것이 두 소수의 곱의 결과라 가정해보면 어떤 소수의 곱인지 찾는것이 소수를 곱하는 것보다 어렵습니다.

이런 수학 함수 중 일부는 비밀 정보를 알고 있을때 쉽게 계산할 수 있습니다. 앞의 예에서 소수 하나가 2,003 이라고 하면 나머지 소수를 쉽게 찾을 수 있습니다. 이런 함수는 역산하기 위한 단축키로 사용할 수 있는 비밀정보가 없으면 거꾸로 계산하기 어렵기 때문에 **트랩 도어 함수** 라고도 합니다. 아래 그림은 트랩도어 함수를 간단한 그림으로 그린 자료입니다.

> Example 1

![1018px-Trapdoor_permutation svg](https://user-images.githubusercontent.com/44635266/70844468-d10c9300-1e84-11ea-8642-d3b1c10606f2.png)

암호학에 유용한 수학 함수의 좀 더 발전된 범주는 타원 곡선의 산술 연산을 바탕으로 합니다. 타원 곡선 산술에서 소수로 나눈 나머지를 곲하는 것은 간단하지만, 나눗셈은 사실상 불가능 합니다. 이것을 **이산 로그 문제(discrete logarithm problem)** 이라고 하며, 현재 알려진 트랩 도어는 없습니다. **타원 곡선 암호화(elliptic curve cryptography)** 는 최신 컴퓨터 시스템에서 광범위하게 활용되며, 이더리움에서 개인키와 디지털 서명을 사용하는 기초가 됩니다.

> 암호학 위키피디아 자료

* [Cryptography](https://en.wikipedia.org/wiki/Cryptography)
* [Trapdoor function](https://en.wikipedia.org/wiki/Trapdoor_function)
* [Prime factorization](https://en.wikipedia.org/wiki/Integer_factorization)
* [Discrete logarithm](https://en.wikipedia.org/wiki/Discrete_logarithm)
* [Elliptic curve cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)

이더리움에서 개인키는 계정에서 자금을 지출하기 위해 트랜잭션에 서명해야 하는 **디지털 서명(Digital Signature)**  을 만드는데 필요한 고유한 정보의 접근을 제어한다. 디지털 서명은 소유자 또는 컨트랙트 사용자를 인증하는데도 사용한다.


