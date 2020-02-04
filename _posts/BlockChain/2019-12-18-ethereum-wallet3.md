---
title : Ethereum Wallet -3-
tags :
- mnemonic
- Mnemonic Code Words (BIP-39)
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Mnemonic Code Words (BIP-39)

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

아래 `Example 1` 을 통해 알아보갰습니다.

> Example 1 - Generating entropy and encoding as mnemonic words

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

아래 `Example 2` 는 니모닉이 어떻게 시드를 생성하는지를 보여줍니다.

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
