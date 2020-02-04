---
title : Ethereum Smart Contracts and Solidity -2-
tags :
- Solidity
- Smart Contract
- Ethereum
---

## Building a Smart Contract with Solidity

솔리디티는 명시적으로 스마트 컨트랙트 작성을 위해 만들어진 언어인데, 이더리움 월드 컴퓨터의 탈중앙화된 환경에서의 실행을 직접적으로 지원합니다. 그 결과, 언어의 속성이 매우 일반적이어서 다른 여러 블로겣인 플랫폼에서 스마트 컨트랙트를 코딩하는데 사용됩니다. 현재 솔리디티는 [깃허브](https://github.com/ethereum/solidity) 에서 개발되고 유지되고있습니다.

솔리디티 프로젝트의 주된 제품은 솔리디티 언어로 작성된 프로그램을 EVM 바이트코드로 변환하는 솔리디티 컴파일러 `solc` 이다. 이 프로젝트는 또한 이더리움 스마트 컨트랙트를 위한 중요한 어플리케이션 바이너리 인터페이스(Application Binary Interface, ABI) 표준을 관리합니다.

### Selecting a Version of Solidity

솔리디티는 **시맨틱 버저닝(semantic versionig)** 이라 하는 버전관리 모델을 따르며, 버전 번호는 점으로 구분된 3개의 숫자로 구성됩니다`(MAJOR.MINOR.PATCH)`. 현재 문서에 사용한 버전은 솔리디티 `0.4.24` 이다. 

### Download and Install

`apt` 패키지 관리자 사용하여 `Ubuntu/Debian` OS 에 솔리디티의 최신 바이너리 릴리스를 설치할 수 있습니다.

```shell
$ sudo add-apt-repository ppa:ethereum/ethereum
$ sudo apt update
$ sudo apt install solc
```

solc 설치한 후에는 실행하여 버전을 확인할 수 있습니다.

```shell
$ solc --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
```

### Writing a Simple Solidity Program

이제 `Faucet` 컨트랙트를 솔리디티로 구현해보겠습니다. 이 예제는 현 파트에서 계속 사용할 예정입니다.

```java
// Our first contract is a faucet!
contract Faucet {

    // Give out ether to anyone who asks
    function withdraw(uint withdraw_amount) public {

        // Limit withdrawal amount
        require(withdraw_amount <= 100000000000000000);

        // Send the amount to the address that requested it
        msg.sender.transfer(withdraw_amount);
    }

    // Accept any incoming amount
    function () public payable {}

}
```

### Compiling with the Solidity Compiler (solc)

`solc` 의 인수 `--bin`, `--optimize` 를 이용하여 컨트랙트의 최적화된 바이너리를 생성합니다.

```java
$ solc --optimize --bin Faucet.sol
======= Faucet.sol:Faucet =======
Binary:
6060604052341561000f57600080fd5b60cf8061001d6000396000f300606060405260043610603e5
763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416
632e1a7d4d81146040575b005b3415604a57600080fd5b603e60043567016345785d8a00008111156
06357600080fd5b73ffffffffffffffffffffffffffffffffffffffff331681156108fc0282604051
600060405180830381858888f19350505050151560a057600080fd5b505600a165627a7a723058203
556d79355f2da19e773a9551e95f1ca7457f2b5fbbf4eacf7748ab59d2532130029
```

`solc` 가 생성한 결과는 이더리움 블록체인에서 실행될 수 있는 시리얼라이즈된 16진수 바이너리입니다.

## The Ethereum Contract ABI

`어플리케이션 바이너리 인터페이스(Application Binary Interface, ABI)` 는 두 프로그램 모듈 간 또는 운영체제와 사용자 프로그램 간의 인터페이스 입니다. ABI 는 데이터 구조와 함수가 어떻게 **기계 코드(machine code)** 에서 사용되는지 그 방법을 정의합니다. ABI 는 API 와 다릅니다. API 는 사람이 읽을 수 있는 형식인 고수준의 **소스 코드(source code)** 로  정의합니다. 따라서 ABI 는 기계 코드와 데이터를 교환하기 위해 인코딩 및 디코딩하는 기본 방법입니다.

이더리움에서 ABI 는 EVM 에서 컨트랙트 호출을 인코딩하고 트랜잭션에서 데이터를 읽는데 사용됩니다. ABI 의 목적은 컨트랙트에서 호출할 수 있는 함수를 정의하고 각 함수가 있는 인수를 받아들이고 결과를 반환하는 방법을 설명하는 것이다.

컨트랙트의 ABI 는 함수 설명 및 이벤트의 JSON 배열로 지정됩니다. 함수는 `type`, `name`, `inputs`, `outputs`, `constant`, `payable` 필드가 있는 JSON 객체이며, 이벤트 객체에는 `type`, `name`, `inputs`, `anonymous` 필드가 있습니다.

`solc` 커맨드를 이용하여 위의 예제 컨트랙트의 ABI 를 생성해보겠습니다.

```java
$ solc --abi Faucet.sol
======= Faucet.sol:Faucet =======
Contract JSON ABI
[{"constant":false,"inputs":[{"name":"withdraw_amount","type":"uint256"}], \
"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable", \
"type":"function"},{"payable":true,"stateMutability":"payable", \
"type":"fallback"}]
```

위와같이 JSON 배열을 생성하여 이 JSON 은 Faucet 컨트랙트에 접근하려는 모든 어플리케이션에 사용할 수 있습니다. ABI 를 사용하면 지갑이나 댑 브라우저 같은 어플리케이션은 올바른 인수와 인수 유형을 사용하여 Faucet 의 함수를 호출하는 트랜잭션을 생성할 수 있습니다.

### Selecting a Solidity Compiler and Language Version

솔리디티에는 프로그램이 특정 컴파일러 버전이 필요하다는 것을 컴파일러에 지시하는 **버전 pragma** 라고 하는 **컴파일러 지시문(compiler directive)** 을 제공합니다.

```java
pragma solidity ^0.4.19;
```

솔리디티는 컴파일러 버전 pragma 를 읽고 컴파일러 버전이 pragma 와 호환되지 않으면 오류가 발생합니다. 위 소스는 이 프로그램이 최소 `0.4.19` 인 컴파일러에서 컴파일 될 수 있다고 말합니다. 그러나 `^` 기호는 `0.4.19` 의 **마이너 수정(minor revision)** 으로 컴파일을 허용한다는 것을 나타냅니다.

예를 들어 `0.4.20` 은 되지만 `0.5.0` 은 안됩니다. pragma 지시문은 EVM 바이트코드로 컴파일 되지 않으며 지시문은 호환성을 검사하기 위해 컴파일러에서만 사용합니다.

prgama 지시문은 아래와 같이 추가합니다.

```java
// Version of Solidity compiler this program was written for
pragma solidity ^0.4.19;

// Our first contract is a faucet!
contract Faucet {

    // Give out ether to anyone who asks
    function withdraw(uint withdraw_amount) public {

        // Limit withdrawal amount
        require(withdraw_amount <= 100000000000000000);

        // Send the amount to the address that requested it
        msg.sender.transfer(withdraw_amount);
    }

    // Accept any incoming amount
    function () public payable {}

}
```