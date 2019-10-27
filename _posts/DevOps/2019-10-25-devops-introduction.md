---
title : DevOps Introduction
tags:
- DevOps
---  

## 기존 개발 시스템

일반적인 개발 운영 체계는 다음과 같다. 개발팀에 의해서 개발이 끝나면, 시스템은 테스트를 거쳐서 운영팀에 이관되고, 운영팀은 해당 시스템을 배포 및 관리 운영한다.

일단 이관된 시스템은, 개발팀이 일체 관여하지 않고, 운영팀에 의해서 현상 유지 된다. 이때 여러가지 문제가 발생하는데 대표로 아래와 같습니다.

1. 문제가 발생시 서로 책임을 미루게되어 문제 해결이 지연된다.
2. 개발은 운영으로 이관 후에, 서비스에 대해서 더 이상 관심을 갖지 않는다. 그리고, 고객과의 접점도 거의 없어지므로, 새로운 VoC에 의한 개선 요청 요구 사항은 개발팀 입장에서는 추가적인 일이 되고, 개발팀은 이러한 신규 요구 사항에 대해서 저항하거나 또는 거절하게 된다.
3. 새로운 요구사항이 나왔을때 빠른 배포가 불가능하다.

## 이 좋은 시스템이 이제야 등장하게된 배경

간단하게 개발과 운영을 합쳐 버리면 될텐데, 이걸 왜 이제서야 할까? 결론부터 이야기 하면, 예전에는 어려웠다. 개발과 운영은 영역 자체가 매우 상이하고, 요구 되는 기술 능력도 많이 차이가 나기 때문에, 일반적인 엔지니어가 양쪽을 모두 커버하기가 어려웠다.

### 인터넷의 발전

인터넷은 더욱더 발전해서, 내가 필요한 자료는 인터넷에서 찾을 수 있을뿐만 아니라, 오픈소스 커뮤니티에서 남들이 만든 코드를 보고 배울 수 도 있고, YouTube에서 강의를 들을 수 도 있으며, Slideshare에서 요약된 PPT를 볼 수 도 있다. 지식을 습득할 수 있는 채널이 다양해지고, 쉬워졌다.

### 오픈소스의 발전

IBM과 같은 대형 벤더 주도의 기술이 아니라 페이스북이나 구글과 같은 거대 B2C 서비스가 IT의 흐름을 이끌기 시작했고, 이러한 업체들이 오픈소스를 적극적으로 후원 및 장려하기 시작했다. 오픈 소스를 통해서 전세계의 개발자들과 함께 이야기를 할 수 도, 일을 할 수 도 있고,  또 오픈 소스를 잘하면 이런 구글이나 페이스북과 같은 좋은 회사에도 취직할 수 있다.

문제가 있는 오픈소스는 내가 직접 고치거나, 오픈 소스 개발자들에게 부탁해서 수정을 할 수 있다. 솔루션에 대한 선택 기회가 넓어지고,  

### 좋은 협업 및 배포 툴 등장

오픈소스의 발전으로 이루어진 혜택중의 하나가, 좋은 툴이 많아 졌다는 것이다. 개발에 관련된 툴 뿐만 아니라, 빌드,배포에 대한 툴과, 모니터링에 대한 툴도 많아졌기 때문에, 운영 업무에 해당 하는 이런 부분을 상당 부분 자동화를 할 수 가 있다.

### 클라우드의 등장

클라우드 컴퓨팅의 가장 큰 특징 중의 하나는 사용자가 인프라 (서버 설치, 네트워크 케이블 구성) 구성할 필요가 없이, 간단하게 책상 앞에 앉아서 웹사이트를 몇번 클릭 하는 것만으로 지구 반대편의 데이터 센터에 서버, 스토리지 구성, 네트워크 구성이 가능하게 되었다는 것이다.

즉, 인프라에 대한 전문 지식이 없이도, 인터넷과 오픈 소스 그리고 클라우드의 도움을 받아서, “운영” 을 겸업 할 수 있는 환경이 마련 되었다는 것이다.

## Development + Operation

![image](https://user-images.githubusercontent.com/44635266/67547614-8c913080-f73a-11e9-8038-519267ebeada.png)

개발 담당자와 운영 담당자가 연계하여 협력하는 개발 방법론

## DevOps

데브옵스 `DevOps는 개발(development)과 운영(operation)`을 결합해 탄생한 개발 방법론 입니다. 시스템 개발자와 운영을 담당하는 정보기술 전문가 사이의 소통, 협업, 통합 및 자동화를 강조하는 소프트웨어 개발 방법론인데요. 

엔지니어가, 프로그래밍하고, 빌드하고, 직접 시스템에 배포 및 서비스를 RUN한다. 그리고, 사용자와 끊임 없이 Interaction하면서 서비스를 개선해 나가는 일련의 과정이자 문화입니다.

이러한 데브옵스의 개념은 애자일 소프트웨어(Agile software) 개발과 지속적인 통합(Continuous integration) 등의 개념과도 관련이 있습니다.

기존의 소프트웨어 개발 및 인프라 관리 프로세스를 사용하는 조직보다 제품을 더 빠르게 혁신하고 개선할 수 있습니다. 이러한 빠른 속도를 통해 조직은 고객을 더 잘 지원하고 시장에서 좀 더 효과적으로 경쟁할 수 있습니다.

### DevOps의 이점

![image](https://user-images.githubusercontent.com/44635266/67548916-1098e780-f73e-11e9-8533-4c8ac38ecc29.png)

### 속도

작업 속도가 빨라지므로, 고객을 위해 더 빠르게 혁신하고, 시장 변화에 더 잘 적응하고, 좀 더 효율적으로 비즈니스 성과를 창출할 수 있습니다. 데브옵스 모델을 사용하면 개발자와 운영 팀이 이러한 성과를 실현할 수 있습니다. 예를 들어 마이크로 서비스와 지속적 전달을 사용하면 팀에서 서비스를 주도적으로 운영하여 업데이트를 좀 더 빠르게 릴리스할 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/67548919-1262ab00-f73e-11e9-880d-8e4defa581f3.png)

### 신속한 제공

릴리스의 빈도와 속도를 개선하여 제품을 더 빠르게 혁신하고 향상할 수 있습니다. 새로운 기능의 릴리스와 버그 수정 속도가 빨라질수록 고객의 요구에 더 빠르게 대응하여 경쟁 우위를 강화할 수 있습니다. 지속적 통합과 지속적 전달은 빌드에서 배포까지 소프트웨어 릴리스 프로세스를 자동화하는 방식입니다.

![image](https://user-images.githubusercontent.com/44635266/67548921-12fb4180-f73e-11e9-8069-99d25bb3d6c4.png)

### 안정성

최종 사용자에게 지속적으로 긍정적인 경험을 제공하는 한편 더욱 빠르게 안정적으로 제공할 수 있도록, 애플리케이션 업데이트와 인프라 변경의 품질을 보장합니다. 지속적 통합 및 지속적 전달과 같은 방식을 사용하여 각 변경 사항이 제대로 작동하며 안전한지 테스트합니다. 모니터링과 로깅 방식을 통해 실시간으로 성능에 대한 정보를 얻을 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/67548923-142c6e80-f73e-11e9-9bb3-b3b436f292b9.png)

### 확장 가능

규모에 따라 인프라와 개발 프로세스를 운영 및 관리합니다. 자동화와 일관성이 지원되므로 위험을 줄이면서 복잡한 시스템 또는 변화하는 시스템을 효율적으로 관리할 수 있습니다. 예를 들어 코드형 인프라를 사용하면 개발, 테스트 및 프로덕션 환경을 반복 가능하고 좀 더 효율적인 방식으로 관리할 수 있습니다.

![image](https://user-images.githubusercontent.com/44635266/67548930-155d9b80-f73e-11e9-99a7-2685ad721b3e.png)

### 협업 강화

주인 의식과 책임 같은 가치를 강조하는 데브옵스 문화 모델에서 좀 더 효과적인 팀을 구축합니다. 개발자와 운영 팀은 긴밀하게 협력하고, 많은 책임을 공유하며, 워크플로를 결합합니다. 이를 통해 비효율성을 줄이고 시간을 절약합니다(예: 개발자와 운영 팀 간에 인도 기간 단축, 실행되는 환경을 고려한 코드 작성 등).

![image](https://user-images.githubusercontent.com/44635266/67548937-168ec880-f73e-11e9-82c9-2636ddb131af.png)

### 보안

제어를 유지하고 규정을 준수하면서 신속하게 진행할 수 있습니다. 자동화된 규정 준수 정책, 세분화된 제어 및 구성 관리 기술을 사용함으로써, 보안을 그대로 유지하면서 데브옵스 모델을 도입할 수 있습니다. 예를 들어 코드형 인프라와 코드형 정책을 사용하면 규모에 따라 규정 준수를 정의하고 추적할 수 있습니다.

### DevOps 개발 싸이클

1. 사용자의 needs 분석. VoC 수집
2. 사용자 스토리 작성 (요구 사항 작성)
3. 사용자 스토리에 대한 scope 정의 및 우선순위 지정
4. Stakeholder에 대한 리포팅 및 관리 (내부 영업, 보고 등)
5. 다른 프로젝트와 연관성(dependency) 관리
6. 필요의 경우 솔루션 (오픈소스 또는 상용) 평가 및 도입
7. 개발 (디자인, 빌드,테스트, 데모.-iterative way)
8. 테스팅. 실 사용자 대상 테스팅 포함
9. 서버에 배포
10. Security 관리, Compliance 관리 (개인 정보 보호, 국가별 법적 사항 확인등)
11. 서비스 운영, 모니터링.
12. 대 고객 지원 (Customer Support) – 추가 하였음

프로세스를 한마디로 정리 해보면 결국 Devops 기반의 개발팀의 특징은, 한 팀내에서 모든 개발,테스트,배포 운영이 이루어진다는 것이고, 가장 중요한 것은, 운영을 통해서 사용자의 피드백을 접수하고, 이것이 새로운 요구 사항으로 연결되는데, 이 싸이클이 매우 빠르며 연속적이고 서로 연결 되어 있다 라는 것이다.