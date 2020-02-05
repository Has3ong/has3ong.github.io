---
title : Ethereum Tokens -2-
tags :
- ERC20
- Token
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

이번 포스트에서는 토큰의 표준을 알아보고 장단점을 알아보겠습니다.

## The ERC20 Token Standard

첫 번째 표준은 ERC(Ethereum Request for Comments) 로 발표한 표준입니다. Github 이슈번호 20이 자동으로 할당되어 **ERC20 토큰** 이라는 이름이 되었습니다. 대다수의 토큰은 현재 ERC20 표준을 기반으로 합니다. 의견 수렴을 통하여 ERC20 요청은 결국 **Ethereum Improvement Proposal 20 (EIP-20)** 이 되었지만 여전히 ERC20 으로 언급됩니다.

ERC20 은 **대체 가능한 토큰(fungible token)** 의 표준으로, ERC20 토큰의 다른 단위가 상호 교환이 가능하고 고유한 특성이 없음을 의미합니다.

### ERC20 required functions and events

**totalSupply**

현재 존재하는 토큰의 전체 개수를 리턴합니다. ERC20 토큰에는 고정 또는 가변적인 공급량이 있을 수 있습니다.

**balanceOf**

주소가 주어지면 해당 주소의 토큰 잔액을 반환 합니다.

**transfer**

주소와 금액이 주어지면 해당 주소로 토큰의 양을 전송합니다. 전송을 실행하는 주소의 잔액에서 전송을 실행합니다.

**transferFrom**

보낸 사람, 받는 사람 및 금액이 주어지면 한 계정에서 다른 계정으로 토큰을 전송합니다. approve 와 함게 조합하여 사용합니다.

**approve**

수취인 주소와 금액이 주어지면 그 주소가 승인을 한 계정에서 최대 금액까지 여러 번 송금할 수 있도록 승인합니다.

**allowance**

소유자 주소와 지출자 주소가 주어지면, 지출자가 출금할 수 있도록 소유자가 승인한 잔액을 리턴합니다.

**Transfer**

전송이 성공하면 이벤트가 트리거 됩니다.

**Approval**

approve 를 성공적으로 호출하면 이벤트가 기록됩니다.

### ERC20 optional functions

**name**

사람이 읽을 수 있는 토큰의 이름을 반환

**symbol**

사람이 읽을 수 있는 기호를 반환

**decimals**

토큰 양을 나눌 수 있는 소수 자릿수를 반환합니다. 예를 들어, decimals 가 2이면 토큰 양을 100으로 나눠 표현합니다.

### The ERC20 interface defined in Solidity

아래는 솔리디티에서 ERC20 인터페이스 사양 입니다.

```java
contract ERC20 {
   function totalSupply() constant returns (uint theTotalSupply);
   function balanceOf(address _owner) constant returns (uint balance);
   function transfer(address _to, uint _value) returns (bool success);
   function transferFrom(address _from, address _to, uint _value) returns
      (bool success);
   function approve(address _spender, uint _value) returns (bool success);
   function allowance(address _owner, address _spender) constant returns
      (uint remaining);
   event Transfer(address indexed _from, address indexed _to, uint _value);
   event Approval(address indexed _owner, address indexed _spender, uint _value);
}
```

### ERC20 data structures

ERC20 구현을 살펴보면 2개의 데이터 구조를 포함하고 있음을 알게 됩니다.

하나는 잔고를 추적하고, 나머지 하나는 허용량을 추적합니다. 솔리디티에서는 **데이터 매핑(data mapping)** 으로 구현됩니다.

첫 번째 데이터 매핑은 소유자 별 토큰 잔액을 내부 테이블로 구현합니다. 이렇게 하면 토큰 컨트랙트에서 토큰을 소유한 사람을 추적할 수 있습니다. 각 이체는 하나의 잔액에서 공제되고 다른 잔고에 추가됩니다.

```java
mapping(address => uint256) balances;
```

두 번째 데이터 구조는 허용량의 데이터 매핑입니다. 다음 절에서 알겠지만, ERC20 토큰을 사용하면 토큰 소유자가 권한을 위임자에게 위임하여 소유자의 잔액에서 특정 금액을 지출할 수 있습니다. ERC20 컨트랙트는 기본 키가 토큰 소유자의 주소이며, 지출자 주소와 허용 한도에 매핑되는 2차원 매핑으로 허용량을 추적합니다.

```java
mapping (address => mapping (address => uint256)) public allowed;
```

### ERC20 workflows: "transfer" and "approve & transferFrom"

ERC20 토큰 표준에는 2 가지 transfer 함수가 있습니다.

첫 번째는 transfer 함수를 사용하는 단일 트랜잭션 워크플로우 입니다. 이 워크플로우는 지갑에서 다른 지갑으로 토큰을 보내는데 사용하는 워크플로우 입니다.

두 번째 워크플로우는 approve 후 transFrom 을 사용하는 두 단계 트랜잭션 워크플로우 입니다. 이 워크플로우는 토큰 소유자가 제어를 다른 주소에 위임할 수 있게 해줍니다. 이것은 제어를 토큰 배포 컨트랙트에 위임하는데 가장 많이 사용되지만 거래소에서도 사용할 수 있습니다.

예를들어 회사가 ICO를 위해 토큰을 판매하는 경우, 특정 양의 토큰을 배포하기 위헤 crowdsale 컨트랙트 주소를 approve 할 수 있습니다. 크라우드 세일 컨트랙트는 아래 `Example 1` 에 나와있는것처럼 토큰을 구매한 각 구매자에게 토큰 컨트랙트의 소유자 밸런스에게 송금합니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/73136480-707e9180-4091-11ea-8839-438c3e580d5a.png)

approve & transferFrom 워크 플로우를 위해 2개의 트랜잭션이 필요합니다.

Alice 가 Bob 같은 구매자에게 AliceCoin 토큰의 50% 를 판매하도록 AliceICO 컨트랙트를 허용한다고 가정하겠습니다.

먼저 Alice 는 AliceCoin ERC20 컨트랙트를 런칭하여 모든 AliceCoin 을 자신의 주소로 발급합니다. 다음, 앨리스는 이더용 토큰을 판매 할 수 있는 AliceICO 컨트랙트를 시작합니다.

그 후 Alice 는 워크플로우에서 approve 와 transferFrom 을 시작합니다. 그녀는 인수를 AliceICO 의 컨트랙트 주소와 totalSupply 의 50% 해서 approve 를 호출하는 트랜잭션을 AliceCoin 컨트랙트로 보냅니다. 이것은 Approval 이벤트를 트리거합니다. 이제 AliceCoin 컨트랙트는 AliceCoin 을 판매할 수 있습니다.

AliceICO 컨트랙트가 Bob 으로부터 이더를 받으면, Bob 에게 AliceCoin 을 보내야 합니다. AliceICO 컨트랙트에는 AliceCoin 과 이더 간에 환율이 있습니다. AliceICO 컨트랙트를 만들 때 앨리스가 설정한 환율은 밥이 AliceICO 컨트랙트로 보낸 이더 양에 대해 얼마나 많은 토큰을 받을지 결정합니다.

AliceICO 컨트랙트에서 AliceCoin transferFrom 함수를 호출하면 보낸 사람으로 Alice 의 주소를 설정하고, 받는 사람으로 BOB 의 주소를 설정합니다. 그리고 환율을 사용하여 value 필드에서 얼마나 많은 AliceCoin 을 Bob 에게 전송할지 결정합니다.

AliceCoin 컨트랙트는 Alice 주소에서 Bob 의 주소로 잔액을 전송하고 Transfer 이벤트를 트리거 합니다. AliceICO 컨트랙트는 Alice 가 설정한 승인 한도를 초과하지 않는 무제한으로 transferFrom 을 호출할 수 있습니다. AliceICO 컨트랙트는 allowance 함수를 호출하여 판매할 수 있는 AliceCoin 토큰의 수를 관리할 수 있습니다.