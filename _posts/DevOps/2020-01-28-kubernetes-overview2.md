---
title : An Overview of Kubernetes -2-
tags :
- Secret
- ConfigMap
- Volume
- Storage
- Service
- Replica Set
- Pod
- Kubernetes
---

*이 포스트는 [Managing Kubernetes](https://go.heptio.com/rs/383-ENX-437/images/Managing_Kubernetes.pdf)를 바탕으로 작성하였습니다.*

## The Kubernetes API

Kubernetes API 는 HTTP 및 JSON 기반의 RESTful API 이며 API 서버가 제공됩니다. Kubernetes 의 구성 요소는 API 를 이용해 통신합니다.

### Basic Objects: Pods, ReplicaSets, and Services

**Pod**

> Pod

![image](https://user-images.githubusercontent.com/44635266/73261949-78187480-4210-11ea-843e-8bcdb5133777.png)

> Simple Pod Templates

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
   - name: nginx
     image: nginx:1.7.9
     ports:
      - containerPort: 8090
```

* apiVersion은 이 스크립트를 실행하기 위한 쿠버네티스 API 버전이다 보통 v1을 사용합니다.
* kind 에는 리소스의 종류를 정의하는데, Pod를 정의하려고 하기 때문에, Pod라고 넣는다.
* metadata에는 이 리소스의 각종 메타 데이타를 넣는데, 라벨이나 리소스의 이름등 각종 메타데이타를 넣는다
* spec 부분에 리소스에 대한 상세한 스펙을 정의한다.
  * Pod는 컨테이너를 가지고 있기 때문에, container 를 정의한다. 이름은 nginx로 하고 도커 이미지 nginx:1.7.9 를 사용하고, 컨테이너 포트 8090을 오픈한다.

파드는 Kubernetes 클러스터 스케줄링에서 가장 작은 원자 단위입니다. 파드는 하나 이상의 실행 중인 컨테이너로 구성됩낟. 또한, Kubernetes 객체 모델 중 만들고 배포할 수 있는 가장 작은 단위입니다.

파드를 원자라고 하는것은 모든 컨테이너가 클러스터에서 동일한 시스템을 차지하도록 보장한다는 의미입니다. 또한 파드는 컨테이너 사이에서 많은 자원을 공유합니다.

예를 들어 모두 동일한 네트워크 네임스페이스를 공유합니다. 즉 파드에 있는 각 컨테이너는 localhost 의 파드에 있는 다른 컨테이너를 볼 수 있습니다. 또한 파드는 프로세스와 프로세스 간 통신 네임 스페이스를 공유하고 있어서, 공유 메모리나 시그널링 같은 툴을 사용하여 다른 컨테이너에서 파드의 여러 프로세스를 제어할 수 있게 해줍니다.

즉, 파드는 다음과 같이 2가지 큰 특징이 있습니다.

1. Pod 내의 컨테이너는 IP 와 Port 를 공유한다.
2. Pod 내에 배포된 컨테이너간에는 디스크 볼륨을 공유할 수 있다.

파드는 어플리케이션이 계속해서 실행 상태에 있도록 도와줍니다. 컨테이너의 프로세스가 충돌하면 Kubernetes 는 자동으로 프로세스를 다시 시작합니다. 파드 또한 어플리케이션 수준의 상태 검사를 정의하여 파드를 자동으로 다시 시작해야 하는지 결정할 수 있는 다양한 어플리케이션별 방법을 제공할 수 있습니다.

**ReplicaSets**

> ReplicaSets

![image](https://user-images.githubusercontent.com/44635266/73261957-7b136500-4210-11ea-9fe6-f4b940880a57.png)

> Simple ReplicaSets Templates

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  # modify replicas according to your case
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
```

개별 컨테이너가 고장 나거나 시스템의 부하를 처리할 수 없는 경우에 실행중인 컨테이너에 어플리케이션을 복제해 놓으면 특정 순간에 서비스가 완전히 중단되거나 실패할 가능성이 크게 줄어듭니다.

또한, 수평적 확장으로 부하에 대응하여 어플리케이션을 확장시킬 수 있습니다. Kubernetes API 에서 이러한 종류의 stateless 복제는 레플리카셋 오브젝트로 처리합니다. 레플리카셋은 주어진 파드 정의에서 여러개의 레플리카가 존재함을 보장합니다.

**Service**

> Service

![image](https://user-images.githubusercontent.com/44635266/73261950-78b10b00-4210-11ea-873f-cd80bbdec9b7.png)

> Simple Service Templates

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

ReplicaSet 을 사용하여 어플리케이션을 복제할 수 있게 되면 다음 단계는 여러 레플리카에 트래픽을 분산시키는 로드밸런서 장치를 만드는 것입니다.

이를 위해 Kubernets 는 **Service** 라는 오브젝트를 가지고 있습니다. Service 는 TCP / UDP 로드밸런싱 서비스를 나타냅니다. 모든 서비스는 TCP / UDP 와 상관없이 다음 3 가지를 가지고 있습니다.

* Its own IP address
* A DNS entry in the Kubernetes cluster DNS
* Load-balancing rules that proxy traffic to the Pods that implement the Service

Service 가 생성되면 고정 IP 주소가 할당됩니다. 이 주소는 가상 주소여서 네트워크에 있는 인터페이스와 일치하지 않습니다. 대신 할당된 IP 주소는 로드밸런싱될 IP 주소로 네트워크 패브릭에 프로그래밍 됩니다. 패킷이 해당 IP 로 전송되면 Service 를 구현하는 Pod 집합으로 로드밸런스 됩니다. 로드밸런싱은 라운드 로빈이나 소스 및 대상 IP 주소 튜플에 기반해 결정하는 방식으로 수행합니다.

고정 IP 주소가 주어지면 DNS 이름이 Kubernets 클러스터의 DNS 서버에 프로그래밍 됩니다. 이 DNS 주소는 Kubernets Service 오브젝트의 이름과 동일한 의미의 이름을 제공하며, 클러스터의 다른 컨테이너가 Service 로드 밸런서의 IP 주소를 검색할 수 있게 해줍니다.

마지막으로 Service 의 로드밸런싱은 Kubernets 클러스터의 네트워크 패브릭에 프로그래밍이 되어 Service IP 주소와 통시나혈고 시도하는 컨테이너가 해당 Pod 에 올바르게 로드밸런싱 되는 방식으로 이루어 집니다. 이 네트워크 패브릭 프로그래밍은 동적이므로 ReplicaSet 의 장애나 확장으로 Pod 들이 오갈 때 로드밸런서는 클러스터의 현재 상태와 일치하도록 끊임없이 다시 프로그래밍 됩니다.

즉, 클라이언트는 Service 를 구현하는 Pod 에 대한 Service IP 주소 연결을 신뢰할 수 있음을 의미합니다.

### Storage: Persistent Volumes, ConfigMaps, and Secrets

Kubernets 에서 처음 소개된 스토리지 개념은 Volume 입니다. 실제로 파드 API 의 일부입니다. 개발자는 파드 내에서 Volume 집합을 정의할 수 있습니다.

> Volume Simple Templates

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-volumes 
spec:
  containers:
  - name: redis
    image: redis
    volumeMounts:
    - name: shared-storage
      mountPath: /data/shared
  - name: nginx
    image: nginx
    volumeMounts:
    - name: shared-storage
      mountPath: /data/shared
  volumes:
  - name : shared-storage
    emptyDir: {}
```
  
Pod 에 Volume 을 추가할 때 실행 중인 각 컨테이너의 임의의 위치에 Volumes 을 **mount** 하도록 선택할 수 있습니다. 이렇게 하면 실행 중인 컨테이너가 볼륨 내의 스토리지에 접근할 수 있습니다. 다른 컨테이너들은 이 Volume 을 다른 위치로 연결하거나 Volume 을 완전히 무시할 수 있습니다.

기본 파일 외에도 Pod 에 Volume 으로 연결할 수 있는 여러 유형의 Kubernetes 오브젝트가 있습니다. 첫 번째는 **ConfigMap** 입니다. ConfigMap 은 구성 파일의 모음을 나타냅니다.

> Simple ConfigMap Templates

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-cm
data:
  language: java
```

Kubernetes 를 사용하다보면 동일한 컨테이너 이미지에 다른 구성을 사용하고 싶어질 수 있습니다. Pod 에 ConfigMap 기반의 Volume 을 추가하면 ConfigMap 의 파일이 실행중인 컨테이너의 지정된 디렉토리에 나타납니다.

Kubernetes 는 데이터베이스 암호 및 인증서와 같은 보안 데이터에 **Secret** 구성 유형을 사용합니다. Volume 컨텍스트 안에서 Secret 은 ConfigMap 과 동일하게 동작합니다. Sercet 은 Volume 으로 Pod 에 부착할 수 있으며 사용 중인 컨테이너에 연결할 수 있습니다.

> Base64 Encoding

```shell
echo -n 'admin' | base64
YWRtaW4=
echo -n '1f2d1e2e67df' | base64
MWYyZDFlMmU2N2Rm
```

> Create Simple Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

Kubernetes 를 사용하면서 Pod 와 Volume 결합에 문제가 발생하는 경우가 있습니다. 예를 들어 ReplicaSet 으로 복제된 컨테이너를 만들 때 모든 레플리카에서 똑같은 Volume 을 사용해야 하는데 때에 따라서 다른 볼륨을 사용하는 경우가 있습니다.

또한, 정확한 Volume 유형을 지정하면 Pod 정의를 특정 환경에 결합하지만 구체적 제공자리를 지정하지 않고 일반적인 스토리지를 요청하는 경우에는 Pod 정의가 필요한 경우가 많습니다.

이를 위해 Kubernetes 에는 **PersistentVolumes** 와 **PersistentVolumesClaims** 가 있습니다. Pod 에 직접 Volume 을 결합하는 대신 PersistentVolume 이 별도의 오브젝트로 생성됩니다. PersistentVolumesClaims 이 오브젝트를 특정 Pod 에 할당하고 이 요청으로 Pod 에 최종적으로 연결됩니다.

Volume 과 Pod 의 추상화는 이전의 2 가지 유스케이스에서 요구되는 이식성과 자동 Volume 생성을 모두 가능하게 합니다.

> Simple Persistent Volume Templates

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```