---
title : Ethereum Tokens -4-
tags :
- ERC721
- ERC777
- ERC223
- Token
- Ethereum
- BlockChain
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Issues with ERC20 Tokens

ERC20 토큰 표준의 채택으로 인해 수천 개의 토큰이 출시되었습니다. 하지만 그에따른 몇가지 문제도 발생했습니다.

ERC20 토큰의 문제중 하나는 토큰과 이더 자체 사이의 미묘한 차이가 관련있습니다. 이더는 수신자의 주소를 목적지로 가지고 있는 트랜잭션에 의해 전송이 일어나는 반면, 토큰 전송은 **특정한 토큰 컨트랙트 상태(specific token contract state)** 안에서 일어나고 수신자의 주소가 아닌 토큰 컨트랙트를 목적지로 합니다.

토큰 컨트랙트는 밸런스를 관리하고 이벤트를 발생시킵니다. 토큰 전송에서 트랜잭션이 토큰 수신자에게 실제로 보내는 것이 아니라 받는 사람의 주소가 토큰 컨트랙트 자체의 맵에 추가됩니다.

이더를 주소로 보내는 트랜잭션은 주소의 상태를 변경합니다. 하지만, 토큰을 주소로 전송하는 트랜잭션은 토큰 컨트랙트의 상태를 변경하지 않습니다. ERC20 토큰을 지원하는 지갑조차 사용자가 토큰 컨트랙트를 명시적으로 추가하지 않는 한 토큰 잔액을 인식하지 못합니다.

또한, 토큰은 이더와 같은 방식으로 동작하지 않습니다. 이더는 `send` 함수에 의해 보내지며, 컨트랙트에 있는 `payable` 함수 또는 외부 소유 주소에 의해 수신됩니다. 토큰은 `transfer` 또는 `approve`, `transferFrom` 을 사용하여 전송되며 수령인 컨트랙트에서 `payable` 함수를 트리거하지 않습니다.

마지막으로 이더를 보내거나 이더리움 컨트랙트를 사용하려면 가스를 지급하기 위해 이더가 필요한데, 토큰을 보내도 이더가 필요합니다. 트랜잭션의 가스를 토큰으로 지급할 수 없으며, 토큰 컨트랙트는 가스를 지급할 수 없습니다.

이러한 문제는 ERC20 토큰에만 해당이 됩니다. 그래서 다양한 표준 제안을 알아보겠습니다.

## ERC223: A Proposed Token Contract Interface Standard

ERC223 제안은 목적지 주소가 컨트랙트인지 아닌지 여부를 감지함으로써 실수로 토큰을 컨트랙트로 전송하는 문제를 해결하려고 합니다. ERC223 에서는 토큰을 받도록 설계된 컨트랙트에 `tokenFallback` 이라는 함수를 구현해야 합니다.

전송 목적지가 컨트랙트인데, 그 컨트랙트에 토큰에 대한 자원이 없는 경우 전송이 실패합니다.

대상 주소가 컨트랙트인지 여부를 감지하기 위해 ERC223 표준 구현은 특별한 방법으로 인라인 바이트 코드의 작은 세그먼트를 사용합니다.

```java
function isContract(address _addr) private view returns (bool is_contract) {
  uint length;
    assembly {
       // retrieve the size of the code on target address; this needs assembly
       length := extcodesize(_addr)
    }
    return (length>0);
}
```

ERC223 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC223Token {
  uint public totalSupply;
  function balanceOf(address who) public view returns (uint);

  function name() public view returns (string _name);
  function symbol() public view returns (string _symbol);
  function decimals() public view returns (uint8 _decimals);
  function totalSupply() public view returns (uint256 _supply);

  function transfer(address to, uint value) public returns (bool ok);
  function transfer(address to, uint value, bytes data) public returns (bool ok);
  function transfer(address to, uint value, bytes data, string custom_fallback)
      public returns (bool ok);

  event Transfer(address indexed from, address indexed to, uint value,
                 bytes indexed data);
}
```

## ERC777: A Proposed Token Contract Interface Standard

ERC777 토큰에 대한 제안은 [ERC777](https://eips.ethereum.org/EIPS/eip-777)에 있습니다. 이 제안은 다음과 같은 목표가 있습니다.

* ERC20 호환 인터페이스 제공
* `send` 함수를 사용하여 토큰을 전송
* 토큰 컨트랙트 등록을 위해 ERC820 과 호환 가능
* 컨트랙트 주소가 토큰을 전송하기 전에 어느 토큰을 전송할 수 있는가를 `takesToSend` 함수를 통해 컨트롤
* 수신자의 `tokensReceived` 함수를 호출하여 컨트랙트 및 주소에 토큰의 수신 사실을 통지할 수 있게 하고 컨트랙트에 `tokensReceived` 함수를 제공하도록 요구함으로써 컨트랙트가 잠길 확률을 줄임
* 기존 컨트랙트가 `tokensToSend` 및 `tokensReceived` 함수에 대해 프록시 컨트랙트를 사용하도록 허용
* 컨트랙트로 보내거나 EOA 로 보내거나와 같은 방식으로 작동
* 토큰 발행 및 소각을 위한 특정 이벤트 제
* 토큰 보유자 대신 토큰을 이동시키는 운영자 허용
* `userData` 및 `operatorData` 필드에서 토큰 전송 트랜잭션에 대한 메타데이터 제공

ERC777 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC777Token {
    function name() public constant returns (string);
    function symbol() public constant returns (string);
    function totalSupply() public constant returns (uint256);
    function granularity() public constant returns (uint256);
    function balanceOf(address owner) public constant returns (uint256);

    function send(address to, uint256 amount, bytes userData) public;

    function authorizeOperator(address operator) public;
    function revokeOperator(address operator) public;
    function isOperatorFor(address operator, address tokenHolder)
        public constant returns (bool);
    function operatorSend(address from, address to, uint256 amount,
                          bytes userData,bytes operatorData) public;

    event Sent(address indexed operator, address indexed from,
               address indexed to, uint256 amount, bytes userData,
               bytes operatorData);
    event Minted(address indexed operator, address indexed to,
                 uint256 amount, bytes operatorData);
    event Burned(address indexed operator, address indexed from,
                 uint256 amount, bytes userData, bytes operatorData);
    event AuthorizedOperator(address indexed operator,
                             address indexed tokenHolder);
    event RevokedOperator(address indexed operator, address indexed tokenHolder);
}
```

### ERC777 hooks

ERC777 토큰 발신자 후크 사양은 다음과 같습니다.

```java
interface ERC777TokensSender {
    function tokensToSend(address operator, address from, address to,
                          uint value, bytes userData, bytes operatorData) public;
}
```

이 인터페이스의 구현은 토큰 지불 통지, 처리 또는 예방을 워하는 모든 주소에 필요합니다. 이 인터페이스를 구현하는 컨트랙트의 주소는 컨트랙트 자체 또는 다른 주소용 인터페이스를 구현하는것과 관계없이 ERC820 을 등록해야 합니다.

ERC777 토큰 수신자 후크 사양은 다음과 같습니다.

```java
interface ERC777TokensRecipient {
  function tokensReceived(
     address operator, address from, address to,
    uint amount, bytes userData, bytes operatorData
  ) public;
}
```

위 인터페이스의 구현은 토큰의 수신을 통지, 처리 거부하려는 모든 주소에 필요합니다. 토큰 발신자 인터페이스와 마찬가지로 동일한 논리 및 요구사항이 토큰 수신자 인터페이스에도 적용되어야 합니다. 즉, 수신자 컨트랙트가 토큰 잠김을 막기 위해 사용합니다. 수신자 컨트랙트가 인터페이스를 구현하는 주소를 등록하지 않으면, 토큰 전송이 실패합니다.

## ERC721: Non-fungible Token (Deed) Standard

지금까지 살펴본 토큰 표준은 **대체 가능한(fungible)** 입니다.

[ERC721 제안](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md) 은 **증서(deed)** 로 알려진 **대체할 수 없는(non-fungible)** 토큰에 표준을 위한것입니다.

대체할 수 없는 토큰은 게임 아이템이 디지털 수집물 같은 아이템일 수도 있습니다. 또한, 자동차 같은 소유권을 추적하기 위한 실물일 수도 있습니다.

ERC721 표준은 증서에의해 그 소유권이 고유하게 추적될 수 있는 한, 그 대상의 종류에 대해 어떤 제한이나 규정을 두지 않으며, 이러한 추적은 256 bit 식별자에 의해 이루어 집니다.

ERC721 의 내부 데이터 구조를 살펴보겠습니다.

```java
// Mapping from deed ID to owner
mapping (uint256 => address) private deedOwner;
```

ERC20 은 각 소유자에 속한 잔액을 추적하고 소유자는 매핑의 기본 키인 반면, ERC721 은 각 증서 ID 와 소유권자를 추적하며 증서 ID 는 매핑의 기본 키가 됩니다.

ERC721 컨트랙트 인터페이스 사양은 다음과 같습니다.

```java
interface ERC721 /* is ERC165 */ {
    event Transfer(address indexed _from, address indexed _to, uint256 _deedId);
    event Approval(address indexed _owner, address indexed _approved,
                   uint256 _deedId);
    event ApprovalForAll(address indexed _owner, address indexed _operator,
                         bool _approved);

    function balanceOf(address _owner) external view returns (uint256 _balance);
    function ownerOf(uint256 _deedId) external view returns (address _owner);
    function transfer(address _to, uint256 _deedId) external payable;
    function transferFrom(address _from, address _to, uint256 _deedId)
        external payable;
    function approve(address _approved, uint256 _deedId) external payable;
    function setApprovalForAll(address _operateor, boolean _approved) payable;
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

ERC721 은 또한 메타데이터와 증서 및 소유자의 열거를 위해 2개의 **선택적(optional)** 인터페이스를 지원합니다.

메타데이터에 대한 ERC721 선택적 인터페이스는 다음과 같습니다.

```java
interface ERC721Metadata /* is ERC721 */ {
    function name() external pure returns (string _name);
    function symbol() external pure returns (string _symbol);
    function deedUri(uint256 _deedId) external view returns (string _deedUri);
}
```

열거를 위한 ERC721 선택적 인터페이스는 다음과 같습니다.

```java
interface ERC721Enumerable /* is ERC721 */ {
    function totalSupply() external view returns (uint256 _count);
    function deedByIndex(uint256 _index) external view returns (uint256 _deedId);
    function countOfOwners() external view returns (uint256 _count);
    function ownerByIndex(uint256 _index) external view returns (address _owner);
    function deedOfOwnerByIndex(address _owner, uint256 _index) external view
        returns (uint256 _deedId);
}
```

