---
title : Ethereum Transaction -1-
tags :
- Transaction
- Ethereum
---

*이 포스트는 [Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)를 바탕으로 작성하였습니다.*

## Transaction

트랜잭션은 EOA 에 의해 서명된 메세지인데, 이더리움 네트워크에 전송되고 이더리움 블록체인에 기록됩니다.

트랜잭션은 EVM 에서 상태 변경을 유발하거나 컨트랙트를 실행할 수 잇는 유일한 방법이다.

## The Structure of a Transaction

**직렬화된(serialized)** 트랜재션을 수신하는 각 클라이언트와 어플리케이션은 자체 내부 데이터 구조를 사용하여 트랜잭션을 메모리에 저장하며, 네트워크에서 직렬화된 트랜잭션 자체에는 존재하지 않는 메타데이터가 포함되어 있습니다.

네트워크 serialization 은 트랜잭션의 유일한 표준 형식 입니다.

아래 `Example 1` 은 이해를 돕기위한 트랜잭션 구조를 간단하게 그린겁니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/71636270-f82ed700-2c70-11ea-9a87-e322d00023a0.png)

트랜잭션은 다음 데이터를 포함하는 *serialized binary message* 입니다.

* **Nonce**
  * 발신 EOA 에 의해 발행되어 메세지 재사용을 방지하는 데 사용하는 일련번호
* **Gas Price**
  * 발신자가 지급 하는 가스의 가격(wei)
* **Gas Limit**
  * 트랜잭션을 위해 구입할 가스의 최대량
* **Recipient**
  * 목적지 이더리움 주소
* **Value**
  * 목적지에 보낼 이더의 양
* **Data**
  * 가변 길이 바이너리 데이터 페이로드
* **v, r, s**
  * EOA 의 ECDSA 디지털 서명의 3 가지 구성요소

트랜잭션 메세지의 구조는 이더리움에서 *byte-perfect data serialization* 를 위해 만들어진 **RLP(Recursive Length Prefix** 인코딩 체계를 사용하여 직렬화됩니다. 이더리움의 모든 숫자는 8bit 배수 길이의 빅엔디안 정수로 인코딩 됩니다.

트랜잭션 내부 정보를 보여주거나 사용자 인터페이스를 시각화하기 위해서는 트랜잭션 구조 이외에도 트랜잭션이나 블록체인에서 파생된 추가정보를 사용합니다.

예를 들어 발신자 EOA 를 식별하는 주소에 **발신자(from)** 데이터가 없는데, 이것은 EOA 의 공개키를 ECDSA 서명의 **v, r, s** 구성요소로부터 알아낼수 있으며, 이는 공개키를 통해 주소를 알아낼 수 있음을 의미합니다.

즉, 주소는 공개키에서 파생될 수 있습니다. 발신자 필드가 표시된 트랜잭션이라면, 시각화하는 데 사용된 소프트웨어에 의해 추가된 것이다. 클라이언트 소프트웨어에 의해 트랜잭션에 자주 추가되는 다른 메타데이터는 블록 번호와 트랜잭션 ID 를 포함합니다. 다시 말하면, 이 데이터는 트랜잭션에서 파생되며 트랜잭션 메세지 자체의 일부가 아닙니다.