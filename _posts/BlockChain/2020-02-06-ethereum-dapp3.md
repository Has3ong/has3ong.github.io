---
title : Ethereum Decentralized Applications (DApps) -3-
tags :
- ENS
- DApps
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## The Ethereum Name Service (ENS)

전통적인 인터넷에서 DNS 는 브라우저에서 사람이 읽을 수 있는 이름을 사용할 수 있게 해줍니다. DNS 는 브라우저에서 사용하는 이름을 IP 주소 해당 페이지 내에 다른 식별자로 해석한다. 이더리움 블록체인에서는 ENS(Ethereum Naming System) 가 이와 같은 문제를 탈중앙화된 방식으로 풀어줍니다.

예를 들어, 이더리움 재단의 기부 주소 **0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359** 는 ENS 를 지원하는 지갑에서는 간단하게 `ethereum.eth` 가 됩니다.

ENS 는 스마트 컨트랙트 이상의 기능이 있습니다. ENS 는 기본적으로 댑이고 탈중앙화 네임 서비스를 제공합니다. 또한 등록, 관리 그리고 등록된 이름의 경매를 위한 여러 댑이 ENS 기능을 지원합니다. ENS 는 댑이 다른 댑을 지원하기 위해 만들어지고, 댑의 생태계에 의해서 유지되고, 다른 댑에 포함되어 동작하는 등 댑들이 어떻게 협력하는지 보여줍니다.

### History of Ethereum Name Services

네임 등록은 **네임 코인(Namcoin)** 개척한 블록체인 최초 비화폐 어플리케이션이었습니다.

게스와 C++ 이더리움 클라이언트의 초기 릴리스에는 namereg 컨트랙트 내장되어 있으며, 네임 서비스를 위한 많은 제안과 ERC 가 만들어졌습니다. 그러나 2016년 부터 **레지스타(registrar)** 에 대한 작업이 시작되었습니다.

### The ENS Specification

ENS 는 주로 3 가지 이더리움 개선 제안에 명시되어 있습니다.

* **EIP-137** : 기본 기능을 지정
* **EIP-162** : .eth 루트에 대한 경매 시스템
* **EIP-181** : 주소의 역 등록을 지정

ENS 는 샌드위치 디자인 철학을 따릅니다. 맨 아래에는 매우 단순한 층이 있고, 그 다음에는 더 복잡하지만 대체 가능한 코드가 포함되어 있으며, 매우 간단한 최상위 계층은 모든 자금을 별도의 계정에 보관합니다.

## Bottom Layer: Name Owners and Resolvers

ENS 는 사람이 읽을 수 있는 이름 대신 **노드(node)** 로 작동합니다. 사람이 읽을 수 있는 이름은 **네임해시(Namehash)** 알고리즘을 사용하여 노드로 변환합니다.

ENS 의 기본 계층은 노드의 소유자만 자신의 이름에 대한 정보를 설정하고 하위 노드를 만들 수 있도록 하는 ERC137 에서 정의한 단순 스마트 컨트랙트 입니다.

기본 계층의 유일한 기능은 노드 소유자가 자신의 노드에 대한 정보(resolver) 를 설정하고 새 하위 노드의 소유자를 만들 수 있게 하는 기능입니다.

### The Namehash algorithm

네임해시는 어떤 이름이라도 그 이름을 식별하는 해쉬로 변환할 수 있는 재귀 알고리즘입니다.

네임해시는 재귀적으로 이름의 구성요소를 해시하여 유효한 입력 도메인에 대한 고유한 고정 길이 문자열을 생성합니다. 예를 들어, `subdomain.example.eth` 의 네임해시 노드는 `keccak('<example.eth> node) + keccak('<subbdomain>)` 입니다. 우리가 해결해야할 하위 문제는 `keccak('<.eth>' node) + keccak('<example>')` 인 `example.eth` 노드를 계산하는 거싱ㅂ니다. 먼저 `keccak(<root node>) + keccak('<eth>')` 인 eth 에 대한 노드를 계산해야합니다.

루트 노드는 재귀의 **기본 케이스(base case)** 라 부르는 것이며, 이것은 당연히 재귀적으로 정의할 수 없는데, 그렇지 않으면 알고리즘은 영원히 종료되지 않을 것입니다. 루트노드는 `0x0000000000000000000000000000000000000000000000000000000000000000` 로 정의합니다.
 
이 모든 것을 합치면, `subdomain.example.eth` 의 노드가 `keccak(keccak(keccak(0x0...0 + keccak('eth')) + keccak('example')) + keccak('subdomain'))` 으로 됩니다.

일반화하자면 네임해시 함수를 다음과 같이 정의할 수 있습니다.

```shell
namehash([]) = 0x0000000000000000000000000000000000000000000000000000000000000000
namehash([label, ...]) = keccak256(namehash(...) + keccak256(label))
```

파이썬에서는 다음과 같습니다.

```python
def namehash(name):
  if name == '':
    return '\0' * 32
  else:
    label, _, remainder = name.partition('.')
    return sha3(namehash(remainder) + sha3(label))
```

따라서 mastering-ethereum.eth 에서는 다음과 같이 처리됩니다.

```shell
namehash('mastering-ethereum.eth')
⇒ sha3(namehash('eth') + sha3('mastering-ethereum'))
⇒ sha3(sha3(namehash('') + sha3('eth')) + sha3('mastering-ethereum'))
⇒ sha3(sha3(('\0' * 32) + sha3('eth')) + sha3('mastering-ethereum'))
```

하위 도메인은 그 자체가 하위 도메인을 가질 수 있습니다. `subdomain.example.eth` 다음에 `sub.subdomain.example.eth`, 그 다음은 `sub.sub.subdomain.example.eth` 등이 될 수 있습니다.

값비싼 재계산을 피하기 위해 네임해시는 이름 자체에만 의존하기 때문에 주어진 이름의 노드를 미리 계산한 후 컨트랙트에 삽입하여 문자열 조작의 필요성을 제거하고 원시 이름의 구성요소 수에 관계없이 ENS 레코드를 즉시 검색할 수 있습니다.

### How to choose a valid name

라벨과 도메인을 길이에 관계없이 사용할 수 있지만, 레거시 DNS 와의 호환성을 위해 다음 규칙을 권장합니다.

* 라벨은 각각 64 자를 넘지 않아야 한다.
* 완전한 ENS 이름은 255 자를 넘지 않아야 한다.
* 라벨은 하이픈으로 시작하거나 끝나서는 안되며, 숫자로 시작해서도 안 된다.

### Root node ownership

계층적 시스템의 결과 중 하나는 이것이 최상위 도메인(Top-Level Domain, TLD) 을 만들 수 있는 루트 노드의 소유자에 의존한다는 것이다.

궁금적인 목표는 새로운 TLD 들을 위한 탈중앙화된 의사결정 프로세스를 만드는 것이지만, 루트 노드는 4 of 7 멀티시그에 의해 컨트롤되고 있는데, 여러 국가에 그 키홀더들이 나누어져 있다. 그 결과, 변경을 위해서는 최소한 7명 중 4명의 키홀더가 동의해야만 합니다.

현재 이 키홀더의 목적과 목표는 커뮤니티와 합의하에 다음과 같은 작업을 하는 것입니다.

* 시스템이 일단 한번 검증되면 `.eth TLD` 의 임시 소유권을 보다 영구적인 컨트랙트로 마이그레이션하고 업그레이드한다.
* 커뮤니티는 TLD 가 필요하다고 동의하면 새로운 TLD 들의 추가를 허용한다.
* 그러한 시스템이 합의되고, 테스트되고, 구현될 때 루트 다중 서명의 소유권을 더 탈중앙화된 컨트랙트로 마이그레이션한다.
* 최상위 저장소의 모든 버그 또는 취약점을 처리하는 최후의 수단으로 사용한다.

### Resolvers

기본 ENS 컨트랙트는 이름에 메타데이터를 추가할 수 없다. 이것은 소위 **리졸버(resolver) 컨트랙트** 가 담당한다. 리졸버 컨트랙트는 앱과 관련된 스웜 주소, 앱에 지불할 주소 혹은 앱의 해시와 같은 이름에 대한 질문에 답변할 수 있는 사용자 생성 컨트랙트입니다.

## Middle Layer: The .eth Nodes

글을 쓰는 시점에서 스마트 컨트랙트에서 유일하게 등록할 수 있는 유일한 최상위 도메인은 .eth 입니다.

.eth 도메인은 경매 시스템을 통해 배포됩니다. 예약 목록이나 우선순위가 없으며, 이름을 얻는 유일한 방법은 시스템을 사용하는것입니다. 경매 시스템 코드는 상당히 복잡합니다. ENS 의 초기 개발 노력 대부분이 시스템의 이 부분에 포함되었습니다. 그러나 보관된 자금에 대한 리스크 없이 나중에 교체 및 업그레이드 할 수 있습니다.

### Vickrey auctions

이름은 수정된 비크레이 경매를 통해 배포된다. 전통적인 비크레이 경매에서는 모든 입찰자가 봉인된 입찰을 제출하고 모두가 동시에 공개합니다. 이때 가장 높은 입찰자가 경매에서 이기지만 두 번째로 높은 입찰가만 지불합니다. 그러므로 입찰자는 경매에 붙여진 이름의 실제 가치보다 더 적은 금액의 입찰을 하지 않게 됩니다. 실제 가치에 입찰하는것이 이길 확률을 높여주지만, 결국 지불하게 될 가격에는 영향을 미치지 않습니다.

블록체인에서는 일부 변경이 필요합니다.

## Top Layer: The Deeds

ENS 의 최상위 계층은 단일 목적을 지닌 또 다른 매우 단순한 컨트랙트다.

유저가 이름을 얻었을 때 그 돈은 실제로 아무데도 보내지는 않지만, 유저가 이름을 갖고 싶어 하는 기간 동안 잠겨있습니다. 이것은 보증된 바이백과 같이 동작합니다. 소유자가 더 이상 이름을 원하지 않으면 시스템으로 다시 판매하고 이더를 복구 할 수 있습니다.

단일 컨트랙트가 수백만 달러의 이더를 보유하는 것이 매우 위험하다는 것이 입증되었습니다. 그래서 ENS 는 각각의 이름에 대해 증서 컨트랙트를 생성합니다. 증서 컨트랙트는 간단합니다. 그리고 지금은 단일 계정에게만 전송되고 단일 엔티티에 의해서만 호출됩니다. 이 접근법은 버그로 인해 자금이 위험에 처할 수 있는 공격 영역을 크게 줄였습니다.

## Registering a Name

Vickrey Auction 에서 봤듯이, ENS 에 이름을 등록하는 과정은 4단계로 진행됩니다. 아래 `Example 1` 은 등록 일정을 보여주는 도표입니다.

> Example 1 - ENS timeline for registration

![image](https://user-images.githubusercontent.com/44635266/73934382-a0dfee80-4921-11ea-80c9-e6b1e60271a4.png)

사용 가능한 이름을 검색하고, `ethereumbook.eth` 라는 이름에 입찰하고, 입찰가를 공개하고, 이름을 보호하기 위해 몇 가지 사용자 친화적인 인터페이스 중 하나를 사용할 것이다.

ENS 탈중앙화 어플리케이션과 상호작용할 수 있는 ENS 웹 기반 인터페이스가 많이 있습니다. 이 예제에서는 메타마스크와 함께 마이크립토(MyCrypto) 인터페이스를 지갑으로 사용합니다.

먼저 우리가 원하는 이름을 사용할 수 있는지 확인해야 합니다. 이 책을 쓰는 동안 우리는 정말로 `mastering.eth` 라는 이름을 동록하려고 했지만, `Example 2` 같이 이미 사용된 것으로 나왔다. ENS 등록은 1년밖에 되지 않기 때문에 향후 해당 이름을 보유할 수 있습니다. 그동안 `ethereumbook.eth` 를 검색해 보겠습니다.

> Example 2 - Searching for ENS names on MyCrypto.com

![image](https://user-images.githubusercontent.com/44635266/73935829-ce7a6700-4924-11ea-89dc-9eb903ff5c8d.png)

이제 이름을 사용할 수 있기 때문에 `Example 3` 을 진행하겠습니다. 메타마스크의 잠금을 해제하고 `ethereumbook.eth` 에 대한 경매를 시작하겠습니다.

> Example 3 - Starting an auction for an ENS name

![image](https://user-images.githubusercontent.com/44635266/73935832-d0442a80-4924-11ea-845f-5004509542a0.png)

`Example 4` 에서는 입찰을 해보겠습니다.

> Example 4 - Placing a bid for an ENS name

![image](https://user-images.githubusercontent.com/44635266/73935834-d1755780-4924-11ea-95a6-6d332e418729.png)

마지막으로 SUBMIT 버튼을 클릭하여 트랜잭션을 확인하겠습니다.

> Example 5 - MetaMask transaction containing your bid

![image](https://user-images.githubusercontent.com/44635266/73936041-447ece00-4925-11ea-8438-da0174caa22b.png)

이 방법으로 트랜잭션을 제출한 후 48 시간안에 입찰가를 공개하면, 우리가 요청한 입력은 우리의 이더리움 주소로 등록될 것입니다.

## Managing Your ENS Name

ENS 이름을 등록하면 ENS 관리자 같은 사용자 친화적인 인터페이스를 사용하여 ENS 이름을 관리할 수 있습니다.

검색 상자에 관리하려는 이름을 입력하고, ENS 관리자 댑이 사용자를 대신하여 이름을 관리할 수 있도록 이더리움 지갑을 잠금 해제해야 합니다.

> Example 6 - The ENS Manager web interface

![image](https://user-images.githubusercontent.com/44635266/73936039-434da100-4925-11ea-8b03-8429f9005683.png)

이 인터페이스에서 하위 도메인을 만들고, 리졸버 컨트랙트를 설정하고 각 이름을 댑 프론트엔드의 스웜 주소 같은 적절한 자원에 연결할 수 있습니다.

### Creating an ENS subdomain

먼저 경매 댑 하위 도메인을 만듭니다. 그리고 하위 도메인을 auction 이라는 이름을 붙입니다. 그래서 완전한 이름은 `auction.ethereumbook.eth` 가 될것입니다. 아래 `Example 7` 을 참고하면 됩니다.

> Example 7 - Adding the subdomain auction.ethereumbook.eth

![image](https://user-images.githubusercontent.com/44635266/73936043-46489180-4925-11ea-8750-119b3673dfc0.png)

하위 도메인을 만들고 나면 이전에 도메인 `etereumbook.eth` 를 관리했던 것처럼 검색 상자에 다른 곳의 주소록을 입력하고 관리할 수 있습니다.

### ENS Resolver

ENS 에서 이름을 확인하는 과정은 두 단계로 이루어집니다.

1. ENS 레지스트리는 해시 후 해석할 이름과 함께 호출된다. 레코드가 존재하면 레지스트리는 리졸버의 주소를 리턴한다.
2. 리졸버는 요청된 자원에 적절한 메소드를 사용하여 호출한다. 리졸버는 원하는 결과를 반환한다.

이 프로세스를 거치면 리졸버의 기능을 네이밍 시스템 자체와 분리하여 더 많은 유연성을 얻을 수 있습니다.

이름 소유자는 사용자 정의 리졸버를 사용하여 어떠한 타입이나 자원을 해석할 수 있으며, ENS 의 기능을 확장할 수도 있습니다.

경매 댑을 스웜 해시에 연결하고자 하면 아래 그림 `Example 8` 과 같이 컨텐츠 해석을 지원하는 공개 리졸버를 사용할 수 있습니다. 우리는 사용자 정의 리졸버를 코딩하거나 배포할 필요가 없습니다.

> Example 8 - Setting the default public resolver for auction.ethereumbook.eth
 
### Resolving a Name to a Swarm Hash (Content)

`auction.ethereumbook.eth` 의 리졸버가 공개 리졸버로 설정되면, 스웜 해시를 이름의 컨텐츠로 반환하도록 설정할 수 있습니다.

> Example 9 - Setting the 'content' to return for auction.ethereumbook.eth

아래 그림은 경매 댑의 전체 아키텍처입니다.

> Example 10 - Auction DApp architecture