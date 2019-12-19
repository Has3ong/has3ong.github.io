---
title : Ethereum Wallet -2-
tags :
- Deterministic Wallets (BIP-32/BIP-44)
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Hierarchical Deterministic Wallets (BIP-32/BIP-44)

결정적 지갑은 단일 시드로부터 많은 키를 쉽게 추출하기 위해 개발되었다. 현재 가장 개선된 결정적 지갑은 비트코인의 **BIP-32** 로 정의된 **HD(hierarchical deterministic)** 지갑 입니다. HD 지갑은 트리 구조로 파생된 키드릉ㄹ 가지고 있다. 이러한 구조는 부모 키가 자식 키의 시퀀스를 파생할 수 있고, 각각의 자식은 다시 또 손자 키의 시퀀스를 파생할 수 있다.

이 트리 구조는 아래 `Example 1` 에 있다.

> Example 1 - HD wallet: a tree of keys generated from a single seed

![image](https://user-images.githubusercontent.com/44635266/71069295-c5d6a180-21bb-11ea-805b-ebce5856fd09.png)

HD 지갑은 결정적 지갑에 비해 몇 가지 장점을 가지고 있다. 트리 구조는 하위 키의 특정 분기는 입금을 받는 데 사용하고 다른 분기는 송금 후 잔액을 받는데 사용할 수 있으며, 부서, 기능 범주로 다른 분기를 할당하여 기업환경 설정과 같은 구조적인 의미를 표현하는 데도 사용할 수 있다.

HD 지갑의 두 번째 장점은 개인키에 접속하지 않고 사용자가 공개키 시퀀스를 만들 수 있다. HD 지갑은 보안상 안전하지 않은 서버 보기 전용, 수신 전용의 용도로 사용할 수 있는데, 이때 이 지갑에는 자금을 움직이는 개인키가 들어 있지 않게 만들 수 있다.

### Seeds and Mnemonic Codes (BIP-39)

안전한 백업 및 검색을 위해 개인키를 인코딩하는 데는 다양한 방법이 이다. 현재 많이 사용하는 방법은 단어 시퀀스를 사용하는 것인데, 이는 올바른 순서로 단어 시퀀스가 입력이 되면 고유한 개인키를 다시 만들수 있다. 이 방법을 **니모닉(mnemonic)** 이라 하며, BIP-39 표준으로 되어있다.

많은 이더리움 지갑은 이 표준을 사용하여 백업 및 복구를 위해 호환이 가능한 니모닉으로 시드 가져오기 내보내기할 수 있다. 다음 예를 알아보겠습니다.

결정적 지갑 16진수 시드

```
FCCF1AB3329FD5DA3DA9577511F8F137
```

12 니모닉에서 나온 결정적 지갑 시드

```
wolf juice proud gown wool unfair
wall cliff insect more detail hub
```

실용적인 측면에서, 16진수 시퀀스를 기록할 때는 오류가 발생할 학률이 매우 높다. 반대로 알려진 단어 목록은 단어들을 사용할 때 중복성이 커서 다루기가 매우 쉽다. 만약 `inzect` 라고 우연히 기록된 게 있다면, 지갑을 복구해야 할 때 `inzect` 는 유효한 영어 단어가 아니므로 `insect` 를 사용해야 한다고 빠르게 결정할 수 있다.

이는 HD 지갑을 관리할 때 시드를 어떻게 보관해야 하는가와 연결된 문제입니다. 데이터 손실이 나서 지갑을 복구하려면 시드가 필요하므로 백업은 매우 중요합니다. 그래서 시드는 디지털 백업보다 종이에 써서 보관할 것을 추천합니다.

## Wallet Best Practices

암호화폐 지갑 기술이 성숙해짐에 따라 광범위하게 상호운용할 수 있고, 사용하기 쉽고, 안전하고, 유연한 지갑을 만들기 위한 일반적인 산업 표준이 등장했다. 또한, 이러한 표준을 통해 지갑은 단일 니모닉에서 여러 개의 서로 다른 암호화폐에 대한 키를 파생시킬 수 있다. 이러한 일반적인 표준은 아래와 같습니다.

* Mnemonic code words, based on BIP-39
* HD wallets, based on BIP-32
* Multipurpose HD wallet structure, based on BIP-43
* Multicurrency and multiaccount wallets, based on BIP-44

현재 대부분의 블록체인 플랫폼과 암호화폐를 서로 연결해 주는 사실상의 기술적 지갑 표준으로 사용되고 있다.

이 지갑 표준은 소프트웨어 및 하드웨어 지갑에 광범위하게 채택되어 모든 지갑의 상호운용이 가능하게 되었다. 사용자는 이러한 지갑 중 하나에서 생성된 니모닉을 내보내고 다른 지갑으로 가져와 모든 키와 주소를 복구할 수 있습니다.

이 표준을 지원하는 대표적인 SW 지갑의 예로 MetaMask 가 있다.