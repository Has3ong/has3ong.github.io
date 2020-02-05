---
title : Ethereum Cryptography -3-
tags :
- Ethereum Address
- Hash Function
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Cryptographic Hash Functions

암호화 **해시 함수(hash function)** 는 이더리움 전반에 걸쳐 사용됩니다. 이더리움 공개키를 주소로 변환하는 작업에서 해시 함수가 사용이 됩니다. 또한, 데이터 확인에 도움이 되는 **디지털 지문(Digital Fingerprints)** 을 만드는데 사용할 수 있다.

해시 함수의 정의는 *임의 크기의 데이터를 고정된 크기의 데이터로 매핑하는 데 사용할 수 있는 모든 함수* 라 한다. 해시 함수에 대한 입력을 **사전 이미지(pre-image), 메세지(message)** 또는 단순히 **입력 데이터(input data)** 라고 합니다. 그 결과를 **해시(hash)** 라고 한다. **암호화 해시 함수(cryptographic hash function)** 는 이더리움 같은 플랫폼을 보호하는 데 유용한 특정 속성은 갖는 하위 범주다.

암호 해시 함수는 임의 크기의 비트열로 매핑하는 **단방향(one-way)** 해시 함수입니다. 단방향 특성은 결과값 해시만 알고 있을 때 입력 데이터를 다시 작성하는 것이 계산적으로 불가능함을 의미합니다. 가능한 입력을 결정하는 유일한 방법은 각 후보에 일치하는 결과가 이쓴ㄴ지 확인하며 무차별 대입 검색을 수행하는 것입니다.

해시함수는 다대일 함수 입니다. 동일환 결과에 해시 처리한 두 입력 데이터 집합을 찾는 것을 **해시 충돌(hash collision)** 찾기라고 합니다. 간단히 말해서, 해시 함수가 좋을수록 해시 충돌이 덜 발생하게 됩니다.

아래 암호화 해시 함수의 주요 속성을 알아보겠습니다.

* **Determinism**
  * 주어진 입력 메세지는 항상 동일한 해시 결과를 생성한다.
* **Verifiability**
  * 메세지의 해시 계산은 효율적이다. 
* **Noncorrelation**
  * 메세지에 대한 작은 변화는 해시 출력을 광범위하게 변경해야 해서 원본 메세지의 해시의 상관 관계가 없다.
* **Irreversibility**
  * 해시로부터 메세지를 계산하는 것은 불가능하다.
  * 모든 가능한 메세지에 대한 무차별 검색과 같다.
* **Collision protection**
  * 같은 해시 결과를 생성하는 2개의 서로 다른 메세지를 계산하는것은 불가능하다.
  
해시 충돌에 대한 저항은 특히 이더리움에서 디지털 서명 위조를 피하기 위해 중요합니다.

암호화 해시 기능이 다음과 같은 다양한 보안 어플리케이션에 유용합니다.

* Data fingerprinting
* Message integrity (error detection)
* Proof of work
* Authentication (password hashing and key stretching)
* Pseudorandom number generators
* Message commitment (commit–reveal mechanisms)
* Unique identifiers

## Ethereum’s Cryptographic Hash Function: Keccak-256

이더리움은 많은 곳에서 Keccak-256 암호화 해시 함수를 사용합니다. Keccak-256 은 SHA-3 암호화 해시 함수 경쟁대회의 후보로 설계되어 우승한 알고리즘 입니다.

### Which Hash Function Am I Using?

두 소프트웨어 모두 SHA-3 이라면 사용중인 소프트웨어 라이브러리가 SHA-3 또는 Keccak-256 인지 어떻게 알 수 있을까요.

방법은 주어진 입력에 대해 예상되는 결과인 **테스트 벡터(text vector)** 를 사용하는 것이다. 해시 함수에 가장 일반적으로 사용되는 테스트는 **빈 입력(empty input)** 입니다. 빈 문자열을 입력으로 해시 함수를 실행하면 다음과 같은 결과가 나옵니다.

```
Keccak256("") =
  c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470

SHA3("") =
  a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
```

이 간단한 테스트를 실행하여 어떤 라이브러리를 사용하는지 확인할 수 있습니다.

## Ethereum Addresses

이더리움 주소는 Keccak-256 단방향 해시 함수를 사용하는 공개키 또는 컨트랙트에서 파생한 **고유 식별자(unique identifier)** 입니다.

**개인키 k**

```
k = f8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315
```

**공개키 K** (x 및 y 좌표가 연결되고 16진수로 표시)

```
K = 6e145ccef1033dea239875dd00dfb4fee6e3348b84985c92f103444683bae07b83b5c38e5e...
```

**Keccak-256 을 이용하여 공개키의 해시를 계산**

```
Keccak256(K) = 2a5bc342ed616b5ba5732269001d3f1ef827552ae1114027bd3ecf1f086ba0f9
```

이더리움 주소인 마지막 20byte 만 유지한다.

```
001d3f1ef827552ae1114027bd3ecf1f086ba0f9
```

종종 이더리움 주소가 접두어 0x 로 표시되어 다음과 같이 16 진수로 인코딩된 것을 볼 수 있다.

```
0x001d3f1ef827552ae1114027bd3ecf1f086ba0f9
```

## Ethereum Address Formats

이더리움 주소는 16진수이며, 공개키 Keccak-256 해시의 마지막 20 byte 에서 파생한 식별자 입니다.

모든 클라이언트의 사용자 인터페이스에 내장된 체크섬을 포함하여 잘못 입력된 주소를 보호하도록 인코딩된 비트코인 주소와 달리 이더리움 주소는 체크섬이 없는 원시 16진수로 표시한다.

### Inter Exchange Client Address Protocol

**클라이언트 주소 상호교환 프로토콜** 은 국제 은행 계좌번호 인코딩과 부분적으로 호환되는 이더리움 주소 인코딩으로 이더리움 주소에 대한 다목적의 체크섬이 가능하고 상호운용 가능한 인코딩을 제공한다. ICAP 주소는 이더리움 이름 레지스트리에 등록한 이더리움 주소 또는 일반 이름을 인코딩할 수 있다.

IBAN 은 은행 계좌 번호를 식별하기 위한 국제 표준으로 중앙 집중적이고 엄격하게 규제되는 서비스다. ICAP 는 탈중앙화형이지만 이더리움 주소에 대해 호환 가능하다.

IBAN 은 국가 코드, 체크섬 및 은행 계좌 식별자를 포함하는 최대 34개의 영수자로 구성된 문자열로 구성한다.

ICAP 는 '이더리움' 을 나타내는 비표준 국가 코드 'XE' 를 도입한 후에 두 문자 체크섬과 계정 식별자의 세 가지 가능한 변형을 도입하여 동일한 구조를 사용한다.

* **Direct**
  * 이더리움 주소의 최하위 비트 155개를 나타내는 최대 30자의 영숫자로 구성된 빅엔디안 base36 정수
  * 이더리움 주소에서만 동작
  * 필드 길이와 체크섬 측면에서 IBAN 과 호환이가능
  * ex) XE60HAMICDXSV5QXVJA7TJW47Q9CHWKJD (33 characters long).
* **Basic**
  * Direct 와 동일하지만 길이는 31자다.
  * 이더리움 주소를 인코딩 할 수 있지만 IBAN 필드 유효성 검사와 호환되지 않는다.
  * ex) XE18CHDJBPLTBCJ03FE9O2NS0BPOJVQCU2P (35 characters long).
* **InDirect**
  * 레지스트리 공급자를 통해 이더리움 주소로 확인하는 식별자를 인코딩
  * **자산 식별자(asset identifier, ex: ETH)**, 이름 서비스 및 사람이 읽을 수 있는 9자 이름 으로 구성된 16개의 영수자를 사용
  * ex) XE##ETHXREGKITTYCATS (20 characters long) 
  * '##' 은 2개의 계산된 체크섬 문자로 대체된다.

helpeth 커맨드 라인 도구를 사용하여 ICAP 주소를 만들 수 있습니다.

```shell
$ helpeth keyDetails \
  -p 0xf8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315

Address: 0x001d3f1ef827552ae1114027bd3ecf1f086ba0f9
ICAP: XE60 HAMI CDXS V5QX VJA7 TJW4 7Q9C HWKJ D
Public key: 0x6e145ccef1033dea239875dd00dfb4fee6e3348b84985c92f103444683bae07b...
```

예제 키의 ICAP 주소는 다음과 같다.

```
XE60HAMICDXSV5QXVJA7TJW47Q9CHWKJD
```

이더리움 주소는 0 byte 로 시작하기 때문에 IBAN 형식으로 유효한 Direct ICAP 인코딩 방법을 사용하여 인코딩 할 수 있다.

주소가 0 으로 시작하지 않으면 Basic 인코딩으로 인코딩한다. 길이는 35자이며 IBAN 은 유효하지 않다.

### Hex Encoding with Checksum in Capitalization (EIP-55)

ICAP 네임 서비스의 느린 배포 때문에 **이더리움 개선 제안(Ethereum Improvement Proposal 55, EIP-55)** 에서 표준을 제안 햇다. EIP-55 는 16진수 주소의 대소문자를 수정하여 이더리움 주소에 대한 이전 버전과 호환되는 체크섬을 제공합니다.

주소의 알파벳 대소문자를 수정함으로써 입력의 무결성을 보호하기 위해 사용할 수 있는 체크섬을 전달 할 수 있다. EIP-55 체크섬을 지원하지 않는 지갑은 주소에 대문자가 혼용된다는 사실을 무시하지만, 이를 지원하는 사용자는 주소를 확인하고 99.986% 의 정확도로 오류를 감지할 수 있다.

혼합 대문자 인코딩은 미묘하기 때문에 처음에는 인식하지 못할 수도 있다. 예제 주소는 다음과 같습니다.

```
0x001d3f1ef827552ae1114027bd3ecf1f086ba0f9
```

EIP-55 혼합 대문자 체크섬을 사용하면 다음과 같이 됩니다.

```
0x001d3F1ef827552Ae1114027BD3ECF1f086bA0F9
```

16 진수 인코딩 알파벳의 일부 알파벳 문자는 대문자인 반면, 그 밖의 문자는 소문자다.

EIP-55 는 구현하기 쉽습니다. 소문자 16 진수 주소의 Keccak-256 해시를 사용합니다.

1. 0x 접두어 없이 소문자 주소를 해시 처리한다.

```
Keccak256("001d3f1ef827552ae1114027bd3ecf1f086ba0f9") =
23a69c1653e4ebbb619b0b2cb8a9bad49892a8b9695d9a19d8f673ca991deae1
```

2. 해시의 해당 16 진수가 0x8 이상인 경우 각 알파벳 문자를 대문자로 만들어라. 

```
Address: 001d3f1ef827552ae1114027bd3ecf1f086ba0f9
Hash   : 23a69c1653e4ebbb619b0b2cb8a9bad49892a8b9...
```

위 주소에는 4번째 위치의 알파벳 문자 d 가 들어있다. 해시의 4번째 문자는 6보다 작아서 소문자로 남겨둡니다. 주소의 다음 알파벳 문자는 6번째 위치에 있는 문자는 f 다. 16 진수 해시의 6번째 문자는 c보다 크고 8이다. 따라서 주소에서 F를 대문자로 반환하는 식이다.

해시의 처음 20 byte 는 체크섬으로 사용한다. 주소에 20 byte 가 적절하게 대문자로 되어 있기 때문이다.

결과로 나온 혼합 대문자를 확인하고 대문자로 된 문자와 주소 해시에 해당하는 문자를 알 수 이는지 확인한다.

```
Address: 001d3F1ef827552Ae1114027BD3ECF1f086bA0F9
Hash   : 23a69c1653e4ebbb619b0b2cb8a9bad49892a8b9...
```

### Detecting an error in an EIP-55 encoded address

주소 마지막 알파벳 F 를 E 로 잘못 읽었다고 가정하자.
```
original : 0x001d3F1ef827552Ae1114027BD3ECF1f086bA0F9
error : 0x001d3F1ef827552Ae1114027BD3ECF1f086bA0E9
```

주소의 유효성을 검사하고 소문자로 변환하여 체크섬 해시를 계산합니다.

```
Keccak256("001d3f1ef827552ae1114027bd3ecf1f086ba0e9") =
5429b5d9460122fb4b11af9cb88b7bb76d8928862e0a57d46dd18dd8e08a6927
```

글자 하나만 변경되어도 해시값은 급격하게 변경이 된다. 이제 대문자를 확인해보면 모두 잘못되었다는것을 확인할 수 있습니다.

```
001d3F1ef827552Ae1114027BD3ECF1f086bA0E9
5429b5d9460122fb4b11af9cb88b7bb76d892886...
```