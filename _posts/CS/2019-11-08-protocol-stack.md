---
title : Protocol Stack
tags:
- Protocol Stack
---  

## Protocol Stack 이란

컴퓨터들이 네트워크를 통해 데이터를 주고 받기 위해서는 프로토콜이 필요하다고 말씀 드렸습니다. 사용되고 있는 프로토콜의 종류는 여러 가지들이 있는데요. 이들이 어떤 구조로 이뤄져 있는지를 알아야 합니다. 이것이 바로 컴퓨터 네트워크를 이해하기 위한 초석입니다.

프로토콜 스택(protocol stack)은 계층화된 구조(layered architecture)로 모여 있는 프로토콜들의 집합을 말합니다. 계층을 나누는 목적은 매우 복잡한 네트워크에서 프로토콜들의 역할을 분담하기 위해서입니다. 한 계층에 속하는 하나의 프로토콜이 인접한 계층의 다른 프로토콜과 통신을 합니다. 이러한 방식으로 꼭대기 계층에서부터 가장 아래에 있는 계층까지 또는 그 반대 방향으로 프로토콜 스택 내에서 통신이 이루어집니다. 컴퓨터 간의 물리적인 데이터 송수신은 가장 아래 계층에서 이루어집니다.

**즉, 프로토콜 스택이란 간단히 프로토콜의 집합이라고 생각하시면 됩니다. **

## Protocol Stack Architecture

![image](https://user-images.githubusercontent.com/44635266/68398142-a1000f00-01b7-11ea-9594-d46ba678a6ae.png)

**OSI 7 Layer**와 **TCP/IP 4 Layer**와 비교해보겠습니다.

![image](https://user-images.githubusercontent.com/44635266/68398144-a198a580-01b7-11ea-8ad5-ca71735fad7a.png)

TCP/IP 와 같이 Application Layer는 합쳐져있지만 Physical Layer 와 DataLink Layer가 분리되있는것에 대해 차이점이 있습니다.

## Protocol Stack Data Type

데이터 타입과 프로토콜은 [OSI 7 Layer](/osi-layer) 포스트와 각각의 레이어 별 포스트를 확인하면 자세히 알 수 있으니 간략하게 적겠습니다.

### Application Layer

**데이터 종류** : Message
	
어플리케이션 계층이 보낼 데이터입니다. 파일 전송을 목적으로 하는 FTP의 경우 파일의 일부가 메시지에 포함됩니다.

### Transport Layer

**데이터 종류** : Segment

메시지에 세그먼트 헤더를 결합하여 세그먼트가 생성됩니다. 세그먼트 헤더는 이 계층들 사이의 통신에 필요한 부가적인 데이터들을 담습니다.

### Network Layer

**데이터 종류** : Datagram

세그먼트에 데이터그램 헤더를 결합하여 데이터그램이 생성됩니다. 데이터그램 헤더도 이 계층들의 통신에 필요한 부가적인 데이터들을 담습니다. IP 프로토콜의 경우 IP 주소가 데이터그램의 헤더에 포함됩니다.

### DataLink Layer

**데이터 종류** : Frame

데이터그램에 프레임 헤더를 결합하여 프레임이 생성됩니다. 프레임 헤더 역시 링크 계층들의 통신에 필요한 데이터들을 갖습니다.

### Physical Layer

**데이터 종류** : Bit
	
프레임을 구성하는 비트들입니다. 이들이 유선/무선으로 전송하기 위해 신호로 바뀝니다. 수신측에서는 이들을 다시 비트로 원복합니다.

