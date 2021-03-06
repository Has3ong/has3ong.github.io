---
title : Container 와 VM 의 차이.
tags :
- Container
- Virtual Machine
- DevOps
categories:
- DevOps
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## VM (Virtual Machine)

서버 가상화 기술의 두 축은 Hypervisor 기반의 가상화와 Container 기반의 가상화입니다.

Hypervisor 등장 전에는 단일 서버를 여러 사용자가 공유할 수 있도록 물리적으로 공간을 격리하는 데 그쳤다면, Hypervisor 가 출현하면서 물리 서버 자원을 추상화하고, 논리적으로 공간을 분할하여 ‘VM’이라는 독립적인 가상 환경의 서버를 이용할 수 있게 됐습니다.

Hypervisor 는 아래와 같이 정의 할 수 있습니다.

* 호스트 시스템에서 다수의 게스트 OS를 구동할 수 있게 하는 소프트웨어.
* 하드웨어를 가상화하면서 하드웨어와 각각의 VM을 모니터링하는 중간 관리자. VMM(Virtual Machine Monitor)이라고도 불림.

이러한 하이퍼바이저는 두 개의 범주로 분류할 수 있습니다. 

### Hypervisor

호스트 컴퓨터에서 다수의 운영 체제(operating system)를 동시에 실행하기 위한 논리적 플랫폼(platform)을 말한다. 가상화 머신 모니터 또는 가상화 머신 매니저(virtual machine monitor 또는 virtual machine manager, 줄여서 VMM)라고도 부른다.

Hypervisor 는 일반적으로 2가지 형태로 나뉜다.

![image](https://user-images.githubusercontent.com/44635266/71541673-0a262680-29a0-11ea-88d2-f3b71b3a9822.png)

**Type 1**

Type 1 하이퍼바이저는 호스트 하드웨어에 직접 설치하여 구동됩니다.
위의 그림을 보면 Type 1 하이퍼바이저의 경우 하드웨어 바로 위에 위치함을 알 수 있습니다.

그래서, 하드웨어를 제어하는 OS 역할과 VM 들을 관리하는 역할을 모두 하이퍼바이저가 담당합니다. 여러 하드웨어 드라이버들을 모두 설정해주어야 하므로 설치가 까다롭습니다. Windows 나 Linux 를 설치하듯이, 아무 것도 설치되어 있지 않은 컴퓨터에 하이퍼바이저를 설치해야 합니다.

**Type 2**
 
다른 Application 과 마찬가지로 호스트 OS 위에 설치되는 방식의 하이퍼바이저입니다. 즉, 기존의 컴퓨터 환경을 그대로 사용하는 방식이므로 설치 및 구성이 편리하다는 장점이 있습니다.

VirtualBox 설치해보신 분이라면 감이 잡히실 거예요. 다른 프로그램과 마찬가지로 설치 과정 거친 후 가상머신 이미지를 만들어서 띄우면 됩니다.
위의 Type 2 그림을 보면 하이퍼바이저가 하드웨어 바로 위에 위치하는 것이 아니라 Host OS 위에 위치한다는 것을 확인할 수 있습니다.

따라서, 하드웨어 기준으로 Type 1 에서는 Guest OS 가 2 번 째 수준에서 실행되는 반면, Type 2 에서는 3 번 째 수준에서 실행된다는 것을 알 수 있습니다.

한단계의 Layer 를 더 타야하므로 성능 관점에서 보면 Type 1 이 Type 2 보다 유리한 면이 있습니다. 

## Container

Container 의 개념은 간단합니다. 애플리케이션과 그 실행에 필요한 라이브러리, 바이너리, 구성 파일 등을 패키지로 묶어 배포하는 것입니다.

이렇게 하면 노트북-테스트 환경-실제 운영환경으로 바뀌어도 실행에 필요한 파일이 함께 따라다니므로 오류를 최소화할 수 있습니다. 운영체제를 제외하고 애플리케이션 실행에 필요한 모든 파일을 패키징한다는 점에서 운영체제 위에서 구현된 가상화, 즉 '운영체제 레벨 가상화'라고 부르기도 합니다.


Container 는 Virtual Machine 과 마찬가지로 애플리케이션을 관련 라이브러리 및 종속 항목과 함께 패키지로 묶어 소프트웨어 서비스 구동을 위한 격리 환경을 마련해 줍니다.

하지만, 아래 그림처럼 Virtual Machine 과는 다른 구조를 가지고 있습니다.

![image](https://user-images.githubusercontent.com/44635266/71541721-bc5dee00-29a0-11ea-9f2a-f68388dc53e3.png)

Virtual Machine 은 하드웨어 스택을 가상화합니다. Container 는 이와 달리 운영체제 수준에서 가상화를 실시하여 다수의 Container 를 OS 커널에서 직접 구동합니다. Container 는 훨씬 가볍고 운영체제 커널을 공유하며, 시작이 훨씬 빠르고 운영체제 전체 부팅보다 메모리를 훨씬 적게 차지합니다.