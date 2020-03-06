---
title : Ethereum Wallet
tags :
- Wallet
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

개발자의 시각으로는 지갑이란 단어는 사용자의 키를 보관하고 관리하기 위해 사용되는 시스템 입니다. 모든 지갑은 키 관리 구성요소를 갖추고 있습니다.

## Wallet Technology Overview

지갑을 설계할 때 가장 중요한 고려사항은 편의성과 프라이버시 사이에 균형을 맞추는 것이다. 가장 편리한 이더리움 지갑은 하나의 개인키와 주소를 가지고 이를 재사용해서 모든것을 처리하는 지갑이다.

이더리움 지갑은 이더나 토큰을 보유하는것이 아니라 키만 보유한다. 이더 혹은 다른 토큰은 이더리움 블록체인에 기록이 된다. 사용자는 지갑에 있는 키로 트랜잭션을 서명함으로써 네트워크에 있는 토큰을 제어하는것이다. 이러한 맥락에서 이더리움은 **키체인(keychain)** 입니다.

지갑은 두 가지 주요 형태가 있습니다. 지갑이 포함하는 키가 서로 관련이 있느냐와 없느냐 입니다.

첫 번째 유형은 각기 다른 무작위 수로부터 각각의 키를 무작위적으로 추출하는 **비결정적 지갑(nondeterministic wallet)** 이라고 한다. 이러한 형태의 지갑을 JBOK(Just a Bunch Of Keys) 지갑이라 한다.

두 번째 유형은 모든 키가 **시드(seed)** 라 하는 단일 마스터 키로부터 파생된 **결정적 지갑(deterministic wallet)** 입니다. 이러한 지갑 형태의 모든 키는 서로 관련이 있고 원래의 시드를 갖고 잇다면 다시 키를 파생시킬 수 있습니다.

결정적 지갑에는 여러 가지 **키 파생(key derivation)** 방식이 있는데, 가장 많이 사용하는 파생 방식은 HD 지갑(BIP-32/BIP-44) 같은 트리구조를 사용합니다.

안전한 결정적 지갑을 만들기 위해서 시드는 단어 목록으로 인코딩되어 불의의 사고에 대비할 수 있도록 적어두고 사용합니다. 이를 지갑의 **니모닉 코드 단어(mnemonic code words)** 라고 합니다. 물론, 누군가가 사용자의 니모닉 코드 단어를 손에 넣으면 지갑을 재생성하여 사용자의 이더와 스마트 컨트랙트에 접근할 수 있다.

## Nondeterministic (Random) Wallets

비결정적 지갑은 무작위로 추출된 단일 개인키를 저장했다. 이 지갑은 여러 측면에서 불편하기 때문에 대체되고 있다. 예를 들어, 이더리움을 사용하는 동안 프라이버시를 극대화한다는 차원에서 이더리움 주소의 재사용을 피하는것이 좋은 지침으로 간주가 됩니다. 즉, 자금을 받을 때마다 새로운 주소를 사용합니다.

이렇게 하려면 비결정적 지갑은 정기적으로 키 목록을 증가시켜야 하는데,이는 정기 적인 백업이 필요하다는 뜻이다. 만약 지갑을 백업하기 전에 데이터를 잃어 버리면 자금과 스마트 컨트랙트에 접근할 수 없게 됩니다.

비결정적 지갑은 'JIT(Just In Time)' 모두 새로운 주소를 위한 새로운 지갑 파일을 만들기 때문에 다루기 어렵습니다.

그럼에도 불구하고 많은 이더리움 클라이언트는 보안 강화를 위해 암호문으로 암호화된 단일 개인키가 들어있는, JSON 인코딩 파일인 **키 저장소** 파일을 사용한다. JSON 파일의 내용은 다음과 같다.

```json
{
    "address": "001d3f1ef827552ae1114027bd3ecf1f086ba0f9",
    "crypto": {
        "cipher": "aes-128-ctr",
        "ciphertext":
            "233a9f4d236ed0c13394b504b6da5df02587c8bf1ad8946f6f2b58f055507ece",
        "cipherparams": {
            "iv": "d10c6ec5bae81b6cb9144de81037fa15"
        },
        "kdf": "scrypt",
        "kdfparams": {
            "dklen": 32,
            "n": 262144,
            "p": 1,
            "r": 8,
            "salt":
                "99d37a47c7c9429c66976f643f386a61b78b97f3246adca89abe4245d2788407"
        },
        "mac": "594c8df1c8ee0ded8255a50caf07e8c12061fd859f4b7c76ab704b17c957e842"
    },
    "id": "4fcb2ba4-ccdb-424f-89d5-26cce304bf9c",
    "version": 3
}
```

키 저장소 형식은 무차별(brute-force), 사전(dictionary) 및  레인보우 테이블(rainbow table) 공격을 대비해 암호 확장 알고리즘으로 알려진 **키 파생 함수(key derivation fuction, KDF)** 를 사용합니다.

개인키는 암호문에 의해 직접적으로 암호화 되지 않습니다. 대신, 암호문은 반복적으로 해싱됨으로써 강화됩낟. 해시 함수는 262,144 라운드로 반복되며, 키 저장소 JSON에서 파라미터 crypto.kdfparams.n 으로 확인할 수 있습니다. 공격자가 암호문을 무차별적으로 생성하려면 암호화를 시도할 대마다 262,144 해시 라운드를 적용해야 할것이며, 이는 공격 속도를 늦추어 암호문에 대한 공격을 불가능하게 합니다.

### Deterministic (Seeded) Wallets

단일 마스터 키 또는 단일 시드로부터 파생된 개인키를 포함합니다. 시드는 개인키를 만들기 위해 인덱스 번호나 체인코드 같은 데이터와 결합된 무작위로 추출된 번호 입니다.

결정적 지갑에서 시드는 모든 파생된 키를 복구할 수 있습니다. 그러므로 생성 시점에 단일 백업으로 지갑에 있는 모든 자금과 컨트랙트를 안전하게 보호할 수 있습니다. 시드는 지갑을 내보내거나(export) 가져오기(import) 에 활용되며 다른 지갑 간에 모든 키를 쉽게 이관할 수 있습니다.

이러한 구조로 인해 시드만 있으면 전체 지갑에 접근이 가능하기 때문에 시드의 보안이 최 우선 과제가 됩니다. 한편, 보안 노력을 단일 데이터에 집중할 수 있다는 것은 장점으로 볼 수 있습니다.

### Hierarchical Deterministic Wallets (BIP-32/BIP-44)

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

### Mnemonic Code Words (BIP-39)

니모닉 코드 단어는 결정적 지갑을 파생하기 위해 시드로 사용되는 난수를 인코딩하는 단어 시퀀스다. 단어 시퀀스는 시드를 다시 만들어내고, 이 시드로부터 지갑과 모든 파생된 키들을 재생성할 수 있다.

니모닉 단어와 함께 결정적 지갑을 구현한 지갑 어플리케이션은 지갑을 처음 만들 때 12 ~ 24 개의 단어 시퀀스를 보여준다. 단어 시퀀스는 지갑의 백업으로, 동일하거나 호환 가능한 지갑 어플리케이션에서 모든 키를 복구하고 다시 생성하는데 사용할 수 있다. 

> 니모닉 단어를 브레인월렛(brainwallet) 과 혼동하는데 다른 개념이다. 브레인월렛은 사요앚가 고른 단어로 구성되는 반면, 니모닉 단어는 지갑이 무작위로 생성해서 사용자에게 보여준다는것이 가장 큰 차이점이다.

니모닉 코드는 BIP-39 에 정의 되어있습니다.

### Generating mnemonic words

니모닉 단어는 BIP-39 에 정의한 표준화된 절차에 따라 지갑으로 자동으로 생성이 됩니다.

1. Create a cryptographically random sequence S of 128 to 256 bits.
2. Create a checksum of S by taking the first length-of-S ÷ 32 bits of the SHA-256 hash of S.
3. Add the checksum to the end of the random sequence S.
4. Divide the sequence-and-checksum concatenation into sections of 11 bits.
5. Map each 11-bit value to a word from the predefined dictionary of 2,048 words.
6. Create the mnemonic code from the sequence of words, maintaining the order.

아래 `Example 2` 을 통해 알아보갰습니다.

> Example 2 - Generating entropy and encoding as mnemonic words

![image](https://user-images.githubusercontent.com/44635266/71072182-48ae2b00-21c1-11ea-873b-d445382f36f2.png)

아래는 엔트로피 데이터 크기와 니모닉 코드 길이 간의 관계 입니다.

|Entropy (bits)|Checksum (bits)|Entropy + checksum (bits)|Mnemonic length (words)|
|:--:|:--:|:--:|:--:|
|128|4|132|12|
|160|5|165|15|
|192|6|198|18|
|224|7|231|21|
|256|8|264|24|

### From mnemonic to seed

니모닉 단어는 128 ~ 256 비트 길이의 엔트로피를 표현한다. 엔트로피는 키 스트레칭 함수 PBKDF2 를 사용하여 더 긴 시드를 파생하는데 사용하며, 생성된 시드는 결정론적 지갑을 구축하고 키를 파생하는데 사용된다.

키 스트레칭 함수에는 니모닉과 **솔트(salt)** 라는 파라미터가 있습니다. 키 스트레칭 함수에서 솔트의 목적은 무차별 대입 공격을 가능하게 하는 조회 테이블 생성을 어렵게 하는것이다. BIP-39 표준에서 솔트는 또 다른 목적이 있습니다.

솔트는 추가적인 보안 요소 역할을 하는 암호문을 추가를 사용할 수 있게 해줍니다.

7. he first parameter to the PBKDF2 key-stretching function is the mnemonic produced in step 6.
8. The second parameter to the PBKDF2 key-stretching function is a salt. The salt is composed of the string constant "mnemonic" concatenated with an optional user-supplied passphrase.
9. PBKDF2 stretches the mnemonic and salt parameters using 2,048 rounds of hashing with the HMAC-SHA512 algorithm, producing a 512-bit value as its final output. That 512-bit value is the seed.

아래 `Example 3` 는 니모닉이 어떻게 시드를 생성하는지를 보여줍니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/71072754-79db2b00-21c2-11ea-90c3-8ca5e733a1b3.png)

아래 표는 생성한 니모닉 코드와 시드의 예시를 보여줍니다.

128-bit entropy mnemonic code, no passphrase, resulting seed

|Entropy input (128 bits)|0c1e24e5917779d297e14d45f14e1a1a|
|:-:|:-|
|Mnemonic (12 words)|army van defense carry jealous true garbage claim echo media make crunch|
|Passphrase|(none)|
|Seed (512 bits)|5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570|

128-bit entropy mnemonic code, with passphrase, resulting seed

|Entropy input (128 bits)|0c1e24e5917779d297e14d45f14e1a1a|
|:-:|:-|
|Mnemonic (12 words)|army van defense carry jealous true garbage claim echo media make crunch|
|Passphrase|SuperDuperSecret|
|Seed (512 bits)|3b5df16df2157104cfdd22830162a5e170c0161653e3afe6c88defeefb0818c793dbb28ab3ab091897d0715861dc8a18358f80b79d49acf64142ae57037d1d54|

256-bit entropy mnemonic code, no passphrase, resulting seed

|Entropy input (256 bits)|2041546864449caff939d32d574753fe684d3c947c3346713dd8423e74abcf8c|
|:-:|:-|
|Mnemonic (24 words)|cake apple borrow silk endorse fitness top denial coil riot stay wolf luggage oxygen faint major edit measure invite love trap field dilemma oblige|
|Passphrase|(none)|
|Seed (512 bits)|3269bce2674acbd188d4f120072b13b088a0ecf87c6e4cae41657a0bb78f5315b33b3a04356e53d062e5 5f1e0deaa082df8d487381379df848a6ad7e98798404|

### Optional passphrase in BIP-39

BIP-39 표준은 시드의 파생에 선택적 암호문을 사용할 수 있다. 암호문을 사용하지 않으면 니모닉은 상수 문자열 "mnemonic" 과 함께 솔트를 구성하여 연장되고, 주어진 니모닉으로부터 특정한 512 비트 시드를 생성한다. 만약 암호문을 사용한다면 스트래칭 함수는 동일한 니모닉으로부터 다른 시드를 생성하게됩니다.

선택적 암호문은 2가지 특성이 있습니다.

* 니모닉 자체만으로는 의미가 없도록 만들어서, 니모닉 백업이 도난으로부터 보호될 수 있도록 하는 2차 팩터로 기능한다.
* 공격자의 협박 때문에 암호문을 가르쳐 줘야 할 경우는 진짜 암호문 대신 그럴듯한 가자 암호문을 제공한다.

하지만 암호문의 사용은 손실의 위험도 가져온다

* 지갑의 주인이 의식을 잃거나 사망할 경우 암호문을 알고 있는 사람이 없다면 시드는 쓸모가 없어지고 지갑에 저장된 모든 자금은 영원히 잃게된다.
* 소유자가 암호문을 시드와 동일한 위치에 백업하는 것은 2차 팩터를 사용하는 목적에 어긋난다.