---
title : Load Balancing 
tags :
- Network
- Load Balancing
- Computer Science
---

## Load Balancing 개념

![image](https://user-images.githubusercontent.com/44635266/81061560-852fb880-8f0f-11ea-96c7-77710cad818f.png)

부하분산 또는 로드 밸런싱(load balancing) 은 컴퓨터 네트워크 기술의 일종으로 둘 혹은 셋이상의 중앙처리장치 혹은 저장장치와 같은 컴퓨터 자원들에게 작업을 나누는 것을 의미한다. 이로써 가용성 및 응답시간을 최적화 시킬 수 있습니다.

이 기술은 보통 내부 네트워크를 이용한 병렬처리(특히, 고가용성의 병렬처리)에 사용된다.

부하분산을 위한 대부분의 응용 프로그램은 다수의 서버(다른 말로, 서버 팜)를 가지고 한 가지 종류의 인터넷 서비스를 지원하는 방식이다. 보통 부하 분산은 트래픽이 많은 웹 사이트, IRC 네트워크, FTP 사이트, NNTP 서버 그리고 DNS서버에 적용이 되고 있다.

인터넷 서비스를 위해서는 소프트웨어를 이용한 부하분산이 적용되며, 이 소프트웨어는 중간에 위치에 실제 서비스하는 서버와 클라이언트를 포트를 이용해 중개하고 있다. 그러나 사용자는 이를 알아차리지 못한다. 이를 투명성이라한다.

서버의 사양을 높여서 처리량을 높이는것보다 Load Balancing 을 하는 이유를 알아보겠습니다. 먼저 Scale Up 과 Scale Out 의 개념을 알아보겠습니다.

## Scale Up vs Scale Out

![image](https://user-images.githubusercontent.com/44635266/81062908-d345bb80-8f11-11ea-9196-b20d2d3aa649.png)

### Scale Up

Scale Up 은 서버에 CPU나 RAM 등을 추가하거나 고성능의 부품, 서버로 교환하는 방법을 의미합니다. 

CPU 나 RAM 을 추가하기로 했다면 현재 서버에 추가 부품을 장착할 수 있는 여유 슬롯이 있어야 하며, 그렇지 않은 경우 서버 자체를 고성능으로 교체하는 것이 필요합니다. 

스케일 업의 경우, 서버 한 대에 모든 부하가 집중되므로 장애 시 영향을 크게 받을 수 있는 위험성이 있습니다. 한 대의 서버에서 모든 데이터를 처리하므로 데이터 갱신이 빈번하게 일어나는 Database 에 적합한 방식입니다.

결국 Scale Up 은 기술이나 물리적인 한계가 생기게 됩니다. 

### Scale Out

Scale Out 이란 서버를 여러 대 추가하여 시스템을 확장하는 방법입니다.

서버가 여러 대가 되기 때문에 각 서버에 걸리는 부하를 균등하게 해주는 Load Balancing 이 필수적으로 동반되어야 합니다. 스케일 아웃의 경우, 서버 한 대가 장애로 다운되더라도 다른 서버로 서비스 제공이 가능하다는 장점이 있습니다.

반면 모든 서버가 동일한 데이터를 가지고 있어야 하므로, 데이터 변화가 적은 Web Server 에 적합한 방식입니다.

## Load Balancing Algorithm

**라운드로빈 방식(Round Robin Method)**

서버에 들어온 요청을 순서대로 돌아가며 배정하는 방식입니다. 클라이언트의 요청을 순서대로 분배하기 때문에 여러 대의 서버가 동일한 스펙을 갖고 있고, 서버와의 연결(세션)이 오래 지속되지 않는 경우에 활용하기 적합합니다.

**가중 라운드로빈 방식(Weighted Round Robin Method)**

각각의 서버마다 가중치를 매기고 가중치가 높은 서버에 클라이언트 요청을 우선적으로 배분합니다. 주로 서버의 트래픽 처리 능력이 상이한 경우 사용되는 부하 분산 방식입니다. 예를 들어 A라는 서버가 5라는 가중치를 갖고 B라는 서버가 2라는 가중치를 갖는다면, 로드밸런서는 라운드로빈 방식으로 A 서버에 5개 B 서버에 2개의 요청을 전달합니다.

**IP 해시 방식(IP Hash Method)**

클라이언트의 IP 주소를 특정 서버로 매핑하여 요청을 처리하는 방식입니다. 사용자의 IP를 해싱해(Hashing, 임의의 길이를 지닌 데이터를 고정된 길이의 데이터로 매핑하는 것, 또는 그러한 함수) 로드를 분배하기 때문에 사용자가 항상 동일한 서버로 연결되는 것을 보장합니다. 

**최소 연결 방식(Least Connection Method)**

요청이 들어온 시점에 가장 적은 연결상태를 보이는 서버에 우선적으로 트래픽을 배분합니다. 자주 세션이 길어지거나, 서버에 분배된 트래픽들이 일정하지 않은 경우에 적합한 방식입니다.

**최소 리스폰타임(Least Response Time Method)**

서버의 현재 연결 상태와 응답시간(Response Time, 서버에 요청을 보내고 최초 응답을 받을 때까지 소요되는 시간)을 모두 고려하여 트래픽을 배분합니다. 가장 적은 연결 상태와 가장 짧은 응답시간을 보이는 서버에 우선적으로 로드를 배분하는 방식입니다.

## L4 Load Balancing vs L7 Load Balancing

Load Balancing 은 L4 로드밸런서와 L7 로드밸런서가 가장 많이 활용됩니다. 그 이유는 L4 로드밸런서부터 포트(Port)정보를 바탕으로 로드를 분산하는 것이 가능하기 때문입니다.

### L4 / L7 ?

![image](https://user-images.githubusercontent.com/44635266/81061839-025b2d80-8f10-11ea-8bef-81ba50b5d32c.png)

네트워크 통신 시스템은 크게 일곱 가지의 계층(OSI 7 layers, 개방형 통신을 위한 국제 표준 모델)으로 나뉩니다. 

각각의 계층(Layer)이 L1/L2/L3‥‥L7에 해당합니다. 상위 계층에서 사용되는 장비는 하위 계층의 장비가 갖고 있는 기능을 모두 가지고 있으며, 상위 계층으로 갈수록 더욱 정교한 로드밸런싱이 가능합니다.

### Layer 4 Load Balancing

![image](https://user-images.githubusercontent.com/44635266/81062459-f754cd00-8f10-11ea-82d5-87cc9b95fabd.png)

* Transport Layer 에서 Load Balancing 을 한다.
* TCP, UDP
* 장점
  * 데이터를 확인하지 않고 패킷 레벨에서 Load Balancing 하기 때문에 빠르다.
  * 데이터의 내용을 복호화할 필요가 없어 안전하다.
* 단점
  * 패킷의 내용을 확인할 수 없어서 섬세한 라우팅이 불가능하다.
  * 사용자의 IP 가 수시로 바뀌는 경우 연속적인 서비스 제공이 어려움

### Layer 7 Load Balancing

![image](https://user-images.githubusercontent.com/44635266/81062476-fe7bdb00-8f10-11ea-830d-ac96307cbe85.png)

* Application Layer 에서 Load Balancing 을 한다.
* HTTP, HTTPS, FTP
* 장점  
  * 상위 계층에서 Load Balancing 하기 때문에 섬세한 라우팅이 가능하다.
  * 캐싱 기능을 제공한다.
  * 비정상적인 트래픽을 사전에 필터링할 수 있어 서비스 안정성이 높다.
* 단점
  * 패킷의 내용을 복호화해야해서 더 높은 비용을 지불한다.
  * 클라이언트가 Load Balancer 와 인증서를 공유해야 하기 때문에 보안 상의 위험성이 존재한다.

## High Available Infrastructure

장애가 났을 경우 Load Balancing 이 어떻게 HA 를 하는지 보고 마무리하겠습니다.

![image](https://assets.digitalocean.com/articles/high_availability/ha-diagram-animated.gif)

## References

* https://ko.wikipedia.org/wiki/%EB%B6%80%ED%95%98%EB%B6%84%EC%82%B0
* https://velog.io/@devzunky/TIL-no.89-Network-The-7-Layers-of-the-OSI-Model
* https://www.digitalocean.com/community/tutorials/what-is-load-balancing#how-does-the-load-balancer-choose-the-backend-server
* https://microsegment.io/post/2019-09-15-scale-up-vs-scale-out/