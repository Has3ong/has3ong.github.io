---
title : Kubernetes Pods, running containers in Kubernetes
tags :
- Namespace
- Label
- Pods
- Kubernetes
---

*이 포스트는 [Kubernetes In Action](https://github.com/KeKe-Li/book/blob/master/kubernetes/Kubernetes%20in%20Action.pdf)를 바탕으로 작성하였습니다.*

## Introducing Pods

파드는 함께 배치된 컨테이너 그룹이며 Kubernetes 의 기본 빌딩 블록입니다. 컨테이너를 개별적으로 배포하기보다는 컨테이너를 가진 파드를 배포하고 운영합니다. 여기서 파드가 항상 두 개 이상의 컨테이너를 포함하는 것을 의미하는 것은 아닙니다. 일반적으로 파드는 하나 이상의 컨테이너만 포함딥니다.

파드의 핵심 사항은 파드가 여러 컨테이너를 가지는 경우에, 모든 컨테이너는 항상 하나의 워커 노드에서 실행되며 여러 워커 노드에 걸쳐 실행되지 않습니다. `Example 1`

> Example 1 - All containers of a pod run on the same node. A pod never spans two nodes.

![image](https://user-images.githubusercontent.com/44635266/80271719-e67cae00-86fd-11ea-923a-5a6ca2f386b9.png)

### Understanding why we need pods

#### Understanding why multiple containers are better than one contain- ner running multiple processes

**IPC(Inter-Process Communication)** 혹은 로컬 파일을 통해 통신하는 여러 프로세스로 구성돼, 같은 노드에서 실행하는 어플리케이션을 생각해보겠습니다. Kubernetes 선 프로세스를 항상 컨테이너에서 실행시키고, 각 컨테이너는 격리된 머신과 비슷하기 때문에 여러 프로세스를 단일 컨테이너 안에서 실행하는 것이 타당하다고 생각할 수 있지만 실제로는 그렇지 않습니다.

컨테이너는 단일 프로세스를 실행하는 경우 모든 프로세스를 실행하고 로그를 관리하는 것은 모두 사용자 책임입니다. 일례로 개별 프로세스가 실패하는 경우 자동으로 재시작하는 메커니즘을 포함해야 합니다. 또한 모든 프로세스는 동일한 표준 출력으로 로그를 기록하기 때문에 어떤 프로세스가 남긴 로그인지 파악하는것이 어렵습니다.

따라서 각 프로세스를 자체의 개별 컨테이너로 실행해야 합니다. 이는 Docker 와 Kubernetes 를 사용하는 방법입니다.

### Understanding pods

여러 프로세스를 단일 컨테이너로 묶지 않기 때문에, 컨테이너를 함께 묶고 하나의 단위로 관리할 수 있는 또 다른 상위구조가 필요합니다. 이 사항이 파드가 필요한 이유입니다.

컨테이너 모음을 사용해 밀접하게 연관된 프로세스를 함께 실행하고 단일 컨테이너 안에서 모두 함께 실행되는 것처럼 동일한 환경을 제공할 수 있으면서도 이들을 격리된 상태로 유지할 수 있습니다. 이런 방식으로 두 개의 장점을 모두 활용합니다. 컨테이너가 제공하는 모든 기능을 활용하는 동시에 프로세스가 함께 실행되는 것처럼 보이게 할 수 있습니다.

#### Understanding the partial isolation between containers of the same pod

컨테이너가 서로 완벽히 격리되어있지만, 개별 컨테이너가 아닌 컨테이너 그룹을 분리하려 합니다. 그룹 안에 있는 컨테이너가 특정 리소스를 공유하기 위해 각 컨테이너가 완벽하게 격리되지 않도록 합니다. Kubernetes 는 파드 안에 있는 모든 컨테이너가 자체 네임스페이스가 아닌 동일한 리눅스 네임스페이스를 공유하도록 Docker 를 설정합니다.

파드의 모든 컨테이너는 동일한 네트워크 네임스페이스와 UTS 네임스페이스 안에서 실행되기 때문에, 모든 컨테이너는 같은 호스트 이름과 네트워크 인터페이스를 공유합니다. 비슷하게 파드의 모든 컨테이너는 동일한 IPC 네임스페이스 아래에서 실행되어 IPC 를 통해 서로 통신할 수 있습니다. 최신 Kubernetes 와 Docker 에서는 동일한 PID 네임스페이스를 공유할 수 있지만, 기본적으로 활성화돼 있지는 않습니다.

파일시스템에서는 사정이 다릅니다. 대부분의 컨테이너 파일 시스템은 컨테이너 이미지에서 나오기 때문에, 파일 시스템은 다른 컨테이너와 완전히 분리됩니다. 그러나 Kubernetes 볼륨 개념을 이용해 컨테이너가 파일 디렉토리를 공유하는 것이 가능합니다.

#### Understanding how containers share the same IP and port space

파드 안의 컨테이너가 동일한 네트워크 네임스페이스에서 실행되기 때문에, 동일한 IP 주소와 포트 공간을 공유하는 것입니다. 이는 동일한 파드 안 컨테이너에서 실행 중인 프로세스가 같은 포트 번호를 사용하지 않도록 주의해야 합니다. 그렇지 않으면 포트 충돌이 발생할 수 있습니다.

위는 동일한 파드일 때만 해당합니다. 다른 파드 안에 있는 컨테이너는 서로 다른 포트 공간을 가지기 때문에 포트 충돌이 일어나지 않습니다. 파드 안에 있는 모든 컨테이너는 동일한 루프백 네트워크 인터페이스를 가지기 때문에 컨테이너들이 로컬 호스트를 통해 서로 통신할 수 있습니다.

#### Introducing the flat inter-pod network

Kuberenetes 클러스터의 모든 파드는 하나의 **플랫(Flat)** 한 공유 네트워크 주소 공간에 상주하므로(`Example 2`) 모든 파드는 다른 파드의 IP 주소를 사용해 접근하는 것이 가능합니다. 둘 사이에는 어떠한 **NAT(Network Address Translation)** 도 존재하지 않습니다. 두 파드가 서로 네트워크 패킷을 보내면, 상대방의 실제 IP 주소를 패킷 안에 있는 출발지 IP 주소에서 찾을 수 있습니다.

> Example 2 - Each pod gets a routable IP address and all other pods see the pod under that IP address.

![image](https://user-images.githubusercontent.com/44635266/80281879-35036a00-8749-11ea-8ae1-edd4d9407287.png)

결과적으로 파드 사이에 통신은 단순합니다. 두 파드가 동일한 서로 다른 워커 노드에 있는지는 중요하지 않으며, 두 경우 모두 파드 안에 있는 컨테이너는 NAT 없는 플랫 네트워크를 통해 서로 통신하는 것이 가능합니다. 이는 실제 노드 간 네트워크 토폴로지에 관계없이, 근거리 네트워크에 있는 컴퓨터 간의 통신과 비슷합니다. LAN 상에 있는 컴퓨터처럼 각 파드는 고유 IP 를 가지며 모든 다른 파드에서 이 네트워크를 통해 접속할 수 있습니다. 이는 일반적으로 물리 네트워크 위에 추가적은 소프트웨어 정의 네트워크 계층을 통해 달성합니다.

파드는 논리적인 호스트로서 컨테이너가 아닌 환경에서의 물리적 호스트나 VM 과 매우 유사하게 동작합니다. 동일한 파드에서 실행한 프로세스는 각 컨테이너 안에 캡슐화돼 있는 점을 제외하면 물리적 혹은 가상머신에서 동작하는 것과 동일합니다.

### Organizing containers across pods properly

파드를 각각 별도의 머신으로 생각할 수 있지만, 파드는 특정 어플리케이션만을 호스팅합니다. 한 호스트에 모든 유형의어플리케이션만을 호스팅합니다. 한 호스트에 모든 유형의 어플리케이션을 넣는 이전과 달리, 상대적으로 가볍기 때문에 오버헤드 없이 필요한 만큼 파드를 가질 수 있습니다.

모든 것을 파드 하나에 넣는 대신 어플리케이션을 여러 파드로 구성하고 각 파드에는 밀접하게 관련 있는 구성 요소나 프로세스만 포함해야 합니다.

#### Splitting multi-tier apps into multiple pods

프론트엔드 서버와 데이터베이스 컨테이너 두 개로 구성된 단일 파드를 실행하지 못할 것은 없지만, 적절한 방법은 아닙니다. 파드의 모든 컨테이너는 항상 같은 위치에서 실행되지만, 웹 서버와 데이터베이스가 같은 머신에서 실행되서는 안됩니다. 

프론트엔드와 백엔드가 같은 파드에 있다며, 둘은 항상 같은 노드에서 실행됩니다. 만약에 두 노드를 가진 Kubernetes 클러스터가 있고 이 파드 하나만 있다면, 워커 노드 하나만 사용하고 두 번째 노드에서 이용할 수 있는 컴퓨팅 리소스를 활용하지 않고 그냥 버립니다.

파드를 두 개로 분리하면 Kubernetes 가 프론트엔드를 한 노드로 그리고 백엔드는 다른 노드에 스케줄링해 인프라 스트럭처의 활용도를 향상시킬 수 있습니다.

#### Splitting into multiple pods to enable individual scaling

두 컨테이너를 하나의 파드에 넣지 말아야 하는 이유는 스케일링 때문입니다. 파드는 스케일링의 기본 단위입니다. Kubernetes 는 개별 컨테이너를 수평으로 확장할 수 없습니다. 대신 파드를 수평으로 확장합니다. 만약 프론트와 백엔드 컨테이너로 구성된 파드를 두 개로 늘리면, 프론트엔드 컨테이너 두 개와 백엔드 컨테이너 두 개를 가지게됩니다.

일반적으로 프론트엔드 구성 요소는 백엔드와 완전히 다른 스케일링 요구 사항을 가지고 있어 개별적으로 확장하는 경향이 있습니다. 데이터베이스와 같은 백엔드는 프론트엔드 웹 서버에 비해 확장하기가 훨씬 어렵습니다. 컨테이너를 개별적으로 스케일링하는 것이 필요하다면, 별도 파드에 배포해야 합니다.

#### Understanding when to use multiple containers in a pod

여러 컨테이너를 단일 파드에 넣는 주된 이유는 `Example 3` 과 같이 어플리케이션이 하나의 주요 프로세스와 하나 이상의 보완 프로세스로 구성된 경우입니다.

> Example 3 - Pods should contain tightly coupled containers, usually a main container and containers that support the main one.

![image](https://user-images.githubusercontent.com/44635266/80281987-d1c60780-8749-11ea-92fb-ecbc8c9e5eed.png)

예를 들어 파드 안에 주 컨테이너는 특정 디렉토리에서 파일을 제공하는 웹 서버일 수 있으며, 추가 컨테이너는 외부 소스에서 주기적으로 컨텐츠를 받아 웹 서버의 디렉토리에 저장합니다.
 
사이드카 컨테이너의 다른 에제로는 로그 데이터와 수집기, 데이터 프로세서, 통신 어댑터 등이 있습니다.

#### Deciding when to use multiple containers in a pod

컨테이너를 파드로 묶어 그룹으로 만들 때는, 두 개의 컨테이너를 단일 파드로 넣을지 두 개의 별도 파드에 넣을지 결정하기 위해 아래와 같은 질문을 해야합니다.

* 컨테이너를 함께 실행해야 하는가, 서로 다른 호스트에서 실행할 수 있는가
* 여러 컨테이너가 모여 하나의 구성 요소를 나타내는가, 개별적인 구성 요소인가
* 컨테이너가 함께, 혹은 개별적으로 스케일링돼야 하는가

기본적으로 특정한 이유 때문에 컨테이너를 단일 파드로 구성하는 것을 요구하지 않는다면, 분리된 파드에서 컨테이너를 실행하는 것이 좋습니다. `Example 4` 는 이를 기억하는 데 도움을 줍니다.

> Example 4 - container shouldn’t run multiple processes. A pod shouldn’t contain multiple containers if they don’t need to run on the same machine.

![image](https://user-images.githubusercontent.com/44635266/80281995-e4404100-8749-11ea-95ea-e3598dbb6a97.png)

파드는 여러 컨테이너를 포함할 수 있지만, 단순하게 유지하기 위해 단일 컨테이너 파드만을 다룹니다.

## Creating Pods From Yaml or Json Descriptors

파드를 포함한 Kubernetes 리소스는 일반적으로 Kubernetes RESET API 엔드포인트에 JSON 혹은 YAML 매니페스트를 전송해 생성합니다. 앞전에 살펴본 `kubectl run` 명령처럼 다른 간단한 방법으로 리소스를 만들 수 있지만, 제한된 속성 집합만 설정할 수 있습니다. 그리고 YAML 파일에 모든 Kubernetes 오브젝트를 정의하면 버전 관리 시스템에 넣는 것이 가능해져, 모든 이점을 누릴 수 있습니다

각 유형별 리소스의 모든 것을 구성하려면 Kubernetes API 오브젝트 정의를 알고 이해해야 합니다.

### Examining a YAML descriptor of an existing pod

앞서 생성한 파드 중 하나에 관한 YAML 정의가 어떤지 보겠습니다. `kubectl get` 명령과 함께 `-o yaml` 옵션을 통해 다음 예제와 같이 전체 YAML 정의를 볼 수 있습니다.

```
$ kubectl get po kubia-zxzij -o yaml
apiVersion: v1                                            1
kind: Pod                                                 2
metadata:                                                 3
  annotations:                                            3
    kubernetes.io/created-by: ...                         3
  creationTimestamp: 2016-03-18T12:37:50Z                 3
  generateName: kubia-                                    3
  labels:                                                 3
    run: kubia                                            3
  name: kubia-zxzij                                       3
  namespace: default                                      3
  resourceVersion: "294"                                  3
  selfLink: /api/v1/namespaces/default/pods/kubia-zxzij   3
  uid: 3a564dc0-ed06-11e5-ba3b-42010af00004               3
spec:                                                     4
  containers:                                             4
  - image: luksa/kubia                                    4
    imagePullPolicy: IfNotPresent                         4
    name: kubia                                           4
    ports:                                                4
    - containerPort: 8080                                 4
      protocol: TCP                                       4
    resources:                                            4
      requests:                                           4
        cpu: 100m                                         4
    terminationMessagePath: /dev/termination-log          4
    volumeMounts:                                         4
    - mountPath: /var/run/secrets/k8s.io/servacc          4
      name: default-token-kvcqa                           4
      readOnly: true                                      4
  dnsPolicy: ClusterFirst                                 4
  nodeName: gke-kubia-e8fe08b8-node-txje                  4
  restartPolicy: Always                                   4
  serviceAccount: default                                 4
  serviceAccountName: default                             4
  terminationGracePeriodSeconds: 30                       4
  volumes:                                                4
  - name: default-token-kvcqa                             4
    secret:                                               4
      secretName: default-token-kvcqa                     4
status:                                                   5
  conditions:                                             5
  - lastProbeTime: null                                   5
    lastTransitionTime: null                              5
    status: "True"                                        5
    type: Ready                                           5
  containerStatuses:                                      5
  - containerID: docker://f0276994322d247ba...            5
    image: luksa/kubia                                    5
    imageID: docker://4c325bcc6b40c110226b89fe...         5
    lastState: {}                                         5
    name: kubia                                           5
    ready: true                                           5
    restartCount: 0                                       5
    state:                                                5
      running:                                            5
        startedAt: 2016-03-18T12:46:05Z                   5
  hostIP: 10.132.0.4                                      5
  phase: Running                                          5
  podIP: 10.0.2.3                                         5
  startTime: 2016-03-18T12:44:32Z                         5                       
```

1. YAML 디스크럽터에서 사용한 Kubernetes API 버전
2. Kubernetes 오브젝트 / 리소스 유형
3. 파드 메타데이터
4. 파드 정의내용
5. 파드와 그 안의 여러 컨테이너의 상세한 상태

#### Introducing the main parts of a pod definition

파드 정의는 몇 부분으로 구성됩니다. YAML 에서 사용하는 Kubernetes API 버전과 YAML 이 설명하는 리소스 유형이 있습니다. 거의 모든 Kubernetes 리소스가 가지고 있는 세 가지 부분이 있습니다.

* Metadata
  * 이름, 네임스페이스, 레이블, 파드에 관한 기타 정보를 포함한다.
* Spec
  * 파드 컨테이너, 볼륨, 기타 데이터 등 파드 자체에 관한 실제 명세를 가진다.
* Status
  * 파드 상태, 각 컨테이너 설명과 상태, 파드 내부 IP, 기타 기본 정보 등 현재 실행 중인 파드에 관한 현재 정보를 포함한다.

위 예제는 실행 중인 파드의 상태를 포함한 자세한 설명을 보여줍니다. `status` 부분에는 특정 시간의 리소스 상태를 보여주는 읽기 전용의 런타임 데이터가 포함돼 있습니다. 새 파드를 만들 때 `status` 부분을 작성할 필요가 없습니다.

위 세가지 부분은 Kubernetes API 오브젝트의 일반적인 구조를 보여줍니다. 

### Creating a simple YAML descriptor for a pod

*kubia-manual.yaml* 파일을 만들작성해보겠습니다.

```yaml
apiVersion: v1               1
kind: Pod                    2
metadata:
  name: kubia-manual         3
spec:
  containers:
  - image: luksa/kubia       4
    name: kubia              5
    ports:
    - containerPort: 8080    6
      protocol: TCP
```

1. Kubernetes API 버전 v1 을 준수함
2. 오브젝트 종류가 파드
3. 파드 이름
4. 컨테이너를 만드는 컨테이너 이미지
5. 컨테이너 이름
6. 어플리케이션이 수신하는 포트

이 정의는 Kubernetes API v1 버전을 준수합니다. 정의하는 리소스 유형은 파드이며 이름은 kubia-manual 입니다. 파드는 `luksa/kubia` 이미지 기반 단일 컨테이너로 구성됩니다. 컨테이너에 이름을 지정하고 8080 포트에서 연결을 기다리는 것을 표시합니다.

#### Specifying container ports

포트 정의 안에서 포트를 지정해둔 것은 단지 정보에 불과합니다. 이를 생략해도 다른 클라이언트에서 포트를 통해 파드에 연결할 수 있는 여부에 영향을 미치지 않습니다. 컨테이너가 0.0.0.0 주소에 열어둔 포트를 통해 접속을 허용할 경우 파드 스펙에 포트를 명시적으로 나열하지 않아도 다른 파드에서 항상 해당 파드에 접속할 수 있습니다.

포트를 명시적으로 정의한다면, 클러스터를 사용하는 모든 사람이 파드에서 노출한 포트를 빠르게 볼 수 있습니다. 또한 포트를 명시적으로 정의하면 포트에 이름을 지정해 편리하게 사용할 수 있습니다.

`kubectl explain` 을 이용해 사용 가능한 API 오브젝트 필드를 찾을 수 있습니다.

```shell
$ kubectl explain pods

DESCRIPTION:
Pod is a collection of containers that can run on a host. This resource
             is created by clients and scheduled onto hosts.
FIELDS:
   kind      <string>
     Kind is a string value representing the REST resource this object
     represents...
   metadata  <Object>
     Standard objects metadata...
   spec      <Object>
     Specification of the desired behavior of the pod...
   status    <Object>
     Most recently observed status of the pod. This data may not be up to
     date...
```

아래와 같이 `spec` 속성도 볼 수 있습니다.

```shell
$ kubectl explain pod.spec

RESOURCE: spec <Object>

DESCRIPTION:
    Specification of the desired behavior of the pod...
    podSpec is a description of a pod.

FIELDS:
   hostPID   <boolean>
     Use the hosts pid namespace. Optional: Default to false.
   ...

   volumes   <[]Object>
     List of volumes that can be mounted by containers belonging to the
     pod.

   Containers  <[]Object> -required-
     List of containers belonging to the pod. Containers cannot currently
     Be added or removed. There must be at least one container in a pod.
     Cannot be updated. More info:
     http://releases.k8s.io/release-1.4/docs/user-guide/containers.md
```

### Using kubectl create to create the pod

YAML 파일을 이용해 파드를 만들려면 `kubectl create` 명령을 이용합니다.

```shell
$ kubectl create -f kubia-manual.yaml
pod "kubia-manual" created
```

`kubectl create -f` 명령은 YAML 이나 JSON 파일로 리소스를 만드는 데 사용합니다.

#### Retrieving the whole definition of a running pod

파드를 만든 후에는 Kubernetes 에 파드의 전체 YAML 을 요청할 수 있습니다. 요청한 결과를보면 앞에서 본 YAML 과 비슷하다는 것을 알 수 있습니다. 아래 명령을 통해 파드 전체 정의를 볼 수 있습니다.

```shell
$ kubectl get po kubia-manual -o yaml
```

JSON 으로 보기 원하면, `kubectl` 명령으로 YAML 대신 JSON 을 반환하도록 할 수 있습니다.

```shell
$ kubectl get po kubia-manual -o json
```

#### Seeing your newly created pod in the list of pods

파드의 상태를 조회해보겠습니다.

```shell
$ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
kubia-manual    1/1     Running   0          32s
kubia-zxzij     1/1     Running   0          1d
```

`kubia-manual` 파드가 실행 중이라는것을 볼 수 있습니다.  

### Viewing application logs

이 작은 *Node.js* 어플리케이션은 로그를 프로세스의 표준 출력에 기록합니다. 컨테이너화된 어플리케이션은 로그를 파일에 쓰기보다는 표준 출력과 표준 에러에 로그를 남기는 게 일반적입니다. 이를 통해 사용자는 다른 어플리케이션 로그를 간단하고 동일한 방식으로 볼 수 있습니다.

컨테이너 런타임은 이러한 스트림을 파일로 전달하고 다음 명령을 이용해 컨테이너 로그를 가져옵니다.

```shell
$ docker logs <container id>
```

ssh 로 파드가 실행 중인 노드에 접속해 `docker logs` 명령으로 로그를 가져올 수 있지만, Kubernetes 는 더 쉬운 방법을 제공합니다.

```shell
$ kubectl logs kubia-manual
Kubia server starting...
```

어떠한 요청도 *Node.js* 어플리케이션으로 보내지 않았기 때문에, 서버가 시작할 때 남긴 로그 한 줄만 표시합니다. 파드에 컨테이너 하나만 있다면 어플리케이션 로그를 가져오는 것은 매우 간단합니다.

#### Retrieving a pod’s log with kubectl logs

여러 컨테이너를 포함한 파드인 경우에는, 컨테이너 이름을 `kubectl logs` 명령에 `-c <contaier name>` 옵션과 함께 명시적으로 포함해야 합니다. `kubia-manual` 파드에서는 컨테이너 이름을 `kubia` 로 지정했습니다. 다른 컨테이너가 존재한다면 로그를 가져오기 위해 다음과 같은 명령어를 사용해야 합니다.

```shell
$ kubectl logs kubia-manual -c kubia
Kubia server starting...
```

현재 존재하는 파드의 컨테이너 로그만 가져올 수 있습니다. 파드가 삭제되면 해당 로그도 같이 삭제됩니다. 파드가 삭제된 후에도 로그를 보기 위해서는 모든 로그를 중앙 저장소에 저장하게 만들어야 합니다.

### Sending requests to the pod

파드에 테스트와 디버깅 목적으로 연결하는 방법이 있습니다. **포트 포워딩(Port Forwarding)** 입니다.

#### Forwarding a local network port to a port in the pod

서비스를 거치지않고 특정 파드와 대화하고 싶을 때 Kubernetes 는 해당 파드로 향하는 포트 포워딩을 구성해줍니다. 포트 포워딩 구성은 `kubectl port-forward` 명령으로 할 수 있습니다. 다음 명령은 머신의 로컬 포트 8888 을 `kubia-manual` 파드의 8080 포트로 향하게 합니다.

```shell
$ kubectl port-forward kubia-manual 8888:8080
... Forwarding from 127.0.0.1:8888 -> 8080
... Forwarding from [::1]:8888 -> 8080
```

포트 포워딩이 실행되 이제 로컬 포트로 파드에 연결할 수 있습니다.

#### Connecting to the pod through the port forwarder

이제 터미널에서 `curl` 을 이용해 localhost:8888 에 실행되고 있는 `kubectl port-forward` 프록시를 통해 HTTP 요청을 해당 파드에 보낼 수 있습니다.

```shell
$ curl localhost:8888
Youve hit kubia-manual
```

`Example 5` 는 요청을 보낼 때 발생하는 상황을 매우 간략하게 보여줍니다. 실제로는 몇 가지 추가적인 구성 요소가 `kubectl` 프로세스와 파드 사이에 존재합니다.

> Example 5 - A simplified view of what happens when you use curl with kubectl port-forward

![image](https://user-images.githubusercontent.com/44635266/80665544-bace3f00-8ad4-11ea-8b37-cf7c84f90d30.png)

이렇게 포트 포워딩을 사용해 개별 파드를 효과적으로 테스트할 수 있습니다.

## Organizing Pods with Labels

파드 두 개가 클러스테어 실행되고 있습니다. 실제 어플리케이션을 배포할 때 대부분의 사용자는 더 많은 파드를 실행하게 될 것입니다. 파드 수가 증가함에 따라 파드를 부분 집합으로 분류할 필요가 있습니다.

마이크로서비스 아키텍처의 경우 배포된 마이크로서비스의 수는 매우 쉽게 20 개를 초과합니다. 이러한 구성 요소는 복제돼 여러 버전이나 릴리스가 동시에 실행됩니다. 이로 인해 시스템에 수백 개 파드가 생길 수 있습니다. 파드를 정리하는 메커니즘이 없다면 `Example 6` 처럼 이해하기 어려운 난장판이 됩니다. 

> Example 6 - Uncategorized pods in a microservices architecture

![image](https://user-images.githubusercontent.com/44635266/80667067-15699a00-8ad9-11ea-9e72-76faf01f943d.png)

모든 개발자와 시스템 관리자는 어떤 파드가 어떤 것인지 쉽게 알 수 있도록 임의의 기준에 따라 작은 그룹으로 조직하는 방법이 필요합니다. 각 파드에 대해 개별적으로 작업을 수행하기보다 특정 그룹에 속한 모든 파드에 관해 한 번에 작업하기를 원할 것입니다.

**레이블(Label)** 을 통해 파드와 기타 다른 Kubernetes 오브젝트의 조직화가 이루어집니다.

### Introducing labels

레이블은 파드와 모든 다른 Kubernetes 리소스를 조직화할 수 있는 단순하면서 강력한 Kubernetes 기능입니다. 레이블은 리소스에 첨부하는 Key - Value 쌍으로, 이 쌍은 레이블 셀렉터를 사용해 리소스를 선택할 때 활용됩니다.

레이블 키가 해당 리소스 내에서 고유하다면, 하나 이상 원하는 만큼 레이블을 가질 수 있습니다. 일반적으로 리소스를 생성할 때 레이블을 붙이지만, 나중에 레이블을 추가하거나 기존 레이블 값을 수정할 수 있습니다.

`Example 6` 마이크로서비스 예제로 돌아가겠습니다. 파드에 레이블을 붙여 누구나 쉽게 이해할 수 있는 체계적인 시스템을 구성할 수 있습니다. 각 파드에는 레이블 두 개를 붙였습니다.

* **app** : 파드가 속한 어플리케이션, 구성 혹은 마이크로서비스를 지정한다.
* **rel** : 파드에서 실행 중인 어플리케이션이 **안정(Stable)**, 베타 혹은 카나리 릴리스인지 보여준다.

두 레이블을 추가하여 `Example 7` 처럼 파드를 2 차원으로 구성했습니다.

> Example 7 - Organizing pods in a microservices architecture with pod labels

![image](https://user-images.githubusercontent.com/44635266/80667498-44ccd680-8ada-11ea-92cd-5fdece70f781.png)

클러스터에 접속할 수 있는 개발자와 운영자는 이제 파드 레이블을 보고 시스템 구조와 각 파드가 적합한 위치에 있는지 볼 수 있습니다.

### Specifying labels when creating a pod

레이블 두 개를 가진 파드를 생성해 실제로 레이블이 어떻게 동작하는지 보겠습니다. 다음 예제에 있는 내용으로 *kubia-manual-with-labels.yaml* 파일을 만들겠습니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual-v2
  labels:
    creation_method: manual          1
    env: prod                        1
spec:
  containers:
  - image: luksa/kubia
    name: kubia
    ports:
    - containerPort: 8080
      protocol: TCP
```

1. 레이블 두 개를 파드에 붙였다.

레이블 `creation_manual=manual` 과 `env=prod` 를 *metadata.labels* 섹션에 포함했습닏나. 이제 이 파드를 생성하겠습니다.

```shell
$ kubectl create -f kubia-manual-with-labels.yaml
pod "kubia-manual-v2" created
```

`kubectl get pods` 명령은 레이블을 표시하지 않는 것이 기본값이라 `--show-labels` 스위치를 사용해 레이블을 볼 수 있습니다.

```shell
$ kubectl get po --show-labels
NAME            READY  STATUS   RESTARTS  AGE LABELS
kubia-manual    1/1    Running  0         16m <none>
kubia-manual-v2 1/1    Running  0         2m  creat_method=manual,env=prod
kubia-zxzij     1/1    Running  0         1d  run=kubia
```

모든 레이블을 나열하는 대신 특정 레이블에만 관심 있는 경우 해당 레이블일 `-L` 스위치로 지정해 각 레이블을 자체 열을 표시할 수 있습니다. 파드를 다시 나열하면서 `kubia-manual-v2` 파드에 부착한 레이블 두 개만 표시하겠습니다.

```shell
$ kubectl get po -L creation_method,env
NAME            READY   STATUS    RESTARTS   AGE   CREATION_METHOD   ENV
kubia-manual    1/1     Running   0          16m   <none>            <none>
kubia-manual-v2 1/1     Running   0          2m    manual            prod
kubia-zxzij     1/1     Running   0          1d    <none>            <none>
```

### Modifying labels of existing pods

기존 파드에 레이블을 추가하거나 수정할 수 있습니다. `kubia-manual` 파드를 수동으로 생성했으니, 여기에 `creation_method=manual` 레이블을 추가하겠습니다.

```shell
$ kubectl label po kubia-manual creation_method=manual
pod "kubia-manual" labeled
```

기존에 가지고 있던 레이블을 어떻게 변경하는지 보기 위해 `kubia-manual-v2` 파드의 `env=prod` 레이블을 `env=debug` 레이블로 변경하겠습니다. 기존 레이블을 변경할 때는 `--overwrite` 옵션이 필요합니다.

```shell
$ kubectl label po kubia-manual-v2 env=debug --overwrite
pod "kubia-manual-v2" labeled
```

갱신된 레이블을 보기위해 파드를 나열합니다.

```shell
$ kubectl get po -L creation_method,env
NAME            READY   STATUS    RESTARTS   AGE   CREATION_METHOD   ENV
kubia-manual    1/1     Running   0          16m   manual            <none>
kubia-manual-v2 1/1     Running   0          2m    manual            debug
kubia-zxzij     1/1     Running   0          1d    <none>            <none>
```

위에서 본 것처럼 리소스에 레이블을 붙이거나 기존 리소스에 있는 레이블을 변경하는 일은 간단합니다.

## Listing Subsets of Pods Through Label Selectors

리소스를 조회할 때 각 리소스에 부착된 레이블을 같이 표시하는 것은 흥미로운 일이 아닙니다. 중요한 것은 레이블이 레이블 셀렉터와 함께 사용되는 점입니다. 레이블 셀렉터는 특정 레이블로 태그된 파드의 부분 집합을 선택해 원하는 작업을 수행합니다. 레이블 셀렉터는 특정 값과 레이블을 가지는지 여부에 따라 리소르를 필터링하는 기준이 됩니다.

레이블 셀렉터는 리소스 중에서 다음 기준에 따라 리소스를 선택합니다.

* 특정한 키를 포함하거나 포함하지 않는 레이블
* 특정한 키와 값을 가진 레이블
* 특정한 키를 가지고 있지만, 다른 값을 가진 레이블

### Listing pods using a label selector

만들어 둔 파드에 레이블 셀렉터를 사용해보겠습니다. 수동으로 생성한 모든 파드를 보려면 (`creation_method=manual`) 붙인 다음 명령을 실행합니다.

```shell
$ kubectl get po -l creation_method=manual
NAME              READY     STATUS    RESTARTS   AGE
kubia-manual      1/1       Running   0          51m
kubia-manual-v2   1/1       Running   0          37m
```

`env` 레이블을 가지고 있지만, 값은 무엇이든 상관없는 파드를 보려면 다음 명령을 실행합니다.

```shell
$ kubectl get po -l env
NAME              READY     STATUS    RESTARTS   AGE
kubia-manual-v2   1/1       Running   0          37m
```

그리고 다음은 `env` 레이블을 가지고 있지 않은 파드입니다.

```shell
$ kubectl get po -l '!env'
NAME           READY     STATUS    RESTARTS   AGE
kubia-manual   1/1       Running   0          51m
kubia-zxzij    1/1       Running   0          10d
```

마찬가지로 레이블 셀렉터를 이용하여 일치하는 파드를 찾을 수 있습니다.

* `creation_method!=manual` : `creation_method` 레이블을 가지는 파드 중에 값이 `manual` 이 아닌 것
* `env in (prod, devel)` : `env` 레이블 값이 `prod` 또는 `devel` 로 설정돼 있는 파드
* `env notin (prod, devel)` : `env` 레이블 값이 `prod`, `devel` 이 아닌 파드

마이크로서비스 지향 아키텍처 예제로 돌아가 제품 카탈로가 마이크로서비스에 속해 있는 모든 파드는 `app=pc` 레이블 셀렉터를 이용해 선택할 수 있습니다.

> Example 8 - Selecting the product catalog microservice pods using the “app=pc” label selector

![image](https://user-images.githubusercontent.com/44635266/80711918-1aa40480-8b2c-11ea-8a35-78e84eec721b.png)

### Using multiple conditions in a label selector

셀렉터는 쉼표로 구분된 여러 기준을 포함하는것이 가능합니다. 셀렉터를 통해 선택하기 위해서는 리소스가 모든 기준을 만족해야 합니다. 예를 들어 제품 카탈로그 마이크로서비스의 베타 릴리스인 파드를 선택하기 위해선 `app=pc`, `rel=beta` 셀렉터를 사용합니다.

레이블 셀렉터는 파드 목록을 나열하는 것뿐만 아니라, 파드 부분 집합에 작업을 수행할 때도 유용합니다.

> Example 9 - Selecting pods with multiple label selectors

![image](https://user-images.githubusercontent.com/44635266/80711944-2394d600-8b2c-11ea-922b-b6bdce93f1f1.png)

## Using Labels and Selectors to Constrain Pod Scheduling

지금까지 생성한 모든 파드는 워커 노드 전체에 걸쳐 무작위로 스케줄링 됐습니다. Kubernetes 는 모든 노드를 하나의 대규모 배포 플랫폼에 노출시키기 때문에, 파드가 어느 노드에 스케줄링됐느냐는 중요하지 않습니다.

각 파드는 요청한 만큼의 정확한 컴퓨팅 리소스를 할당받습니다. 그리고 다른 파드에서 해당 파드로 접근하는 것은 파드가 스케줄링된 노드에 아무런 영향을 받지 않습니다. 그렇기 때문에 Kubernetes 에게 파드를 어디에 스케줄링할지 알려줄 필요는 없습니다.

파드를 스케줄링할 위치를 결정할 때 약간이라도 영향을 미치고 싶은 상황이 있습니다. 예를 들어 하드웨어 인프라가 동일하지 않은 경우입니다. 워커 노드 일부는 HDD 를 가지고 나머지는 SSD 를 가지는 경우, 특정 파드를 한 그룹에 나머지 파드는 다른 그룹에 스케줄링할 수 있습니다. 또 다른 예로는 GPU 가속을 제공하는 노드에만 GPU 계산이 필요한 파드를 스케줄링할 수 있습니다.

Kubernetes 의 전체 아이디어는 그 위에 실행되는 어플리케이션으로부터 실제 인프라스트럭처를 숨기는 것에 있기에 파드가 어떤 노드에 스케줄링돼야 하는지 구체적으로 지정하지 않습니다. 그로 인해 어플리케이션이 인프라스트럭처에 결합되기 때문입니다.

정확한 노드를 지정하는 대신 필요한 노드 요구사항을 기술하고 Kubernetes 가 요구사항을 만족하는 노드를 선택하도록 합니다. 이는 노드 레이블과 레이블 셀렉터를 통해 알 수 있습니다.

### Using labels for categorizing worker nodes

파드는 레이블을 부착할 수 있는 유일한 Kubernetes 리소스가 아닙니다. 노드를 포함한 모든 Kubernetes 오브젝트에 레이블을 부착할 수 있습니다. 일반적으로 운영팀은 새 노드를 클러스터에 추가할 때, 노드가 제공하는 하드웨어나 파드를 스케줄링할 때 유용하게 사용할 수 있는 기타 사항을 레이블로 지정해 노드로 분류합니다.

클러스터에 범용 GPU 컴퓨팅에 사용할 수 있는 GPU 를 가지고 있는 노드가 있다고 가정하겠습니다. 이 기능을 가지고 있음을 보여주는 레이블을 노드에 추가하려고 합니다. `gpu=true` 레이블을 노드 중 하나에 추가하겠습니다.

```shell
$ kubectl label node gke-kubia-85f6-node-0rrx gpu=true
node "gke-kubia-85f6-node-0rrx" labeled
```

이제 파드를 나열할 때처럼 노드를 나열할 때 레이블 셀렉터를 사용할 수 있습니다. 노드중에 `gpu=true` 레이블을 가진 노드를 조회합니다.

```shell
$ kubectl get nodes -l gpu=true
NAME                      STATUS AGE
gke-kubia-85f6-node-0rrx  Ready  1d
```

한 노드만 이 레이블을 가지고 있습니다. `kubectl` 을 이용해 모든 노드를 나열하고 각 노드의 `gpu` 레이블 값을 보여주는 추가 열을 표시하도록 하는 것도 가능합니다.

### Scheduling pods to specific nodes

GPU 를 필요하는 새로운 파드를 배포한다고 가정하겠습니다. 스케줄러가 GPU 를 제공하는 노드를 선택하도록 요청하려면, 파드의 YAML 파일에 노드 셀렉터를 추가합니다 다음 예제로 *kubia-gpu.yaml* 파일을 작성하고 `kubectl create -f kubia-gpu.yaml` 명령을 실행합니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubia-gpu
spec:
  nodeSelector:               1
    gpu: "true"               1
  containers:
  - image: luksa/kubia
    name: kubia
```

1. nodeSelector 는 Kubernetes 에 `gpu=true` 레이블을 포함한 노드에 이 파드를 배포하도록 지시한다.

`spec` 섹션 안에 `nodeSelector` 필드를 추가했습니다. 파드를 생성할 때, 스케줄러는 `gpu=true` 레이블을 가지고 있는 노드 중에서 선택해야 합니다.

### Scheduling to one specific node

마찬가지로 각 노드에는 키를 `kubernetes.io/hostname` 으로 하고 값에는 호스트 이름이 설정돼 있는 고유한 레이블이 있기 때문에, 파드를 특정한 노드로 스케줄링하는 것도 가능합니다. 그러나 `nodeSelector` 에 실제 호스트 이름을 지정할 경우에 해당 노드가 오프라인 상태인 경우 파드가 스케줄링 되지 않을 수 있습니다. 개별 노드로 생각해서는 안됩니다. 레이블 셀렉터를 통해 지정한 기준을 만족하는 노드의 논리적인 그룹을 생각해야 합니다.

## Annotating Pods

파드 및 다른 오브젝트는 레이블 외에 **어노테이션(Annotation)** 을 가질 수 있습니다. 어노테이션은 Key-Value 쌍으로 레이블과 비슷하지만 식별 정보를 갖지 않습니다. 레이블은 오브젝트를 묶는데 사용하지만, 어노테이션은 불가능합니다. 레이블 셀렉터를 통해 오브젝트를 선택하는 것이 가능하지만 어노테이션은 셀렉터가 없습니다.

하지만 어노테이션은 더 많은 정보를 유지할 수 있습니다. 이는 주로 도구들에서 사용됩니다. 특정 어노테이션은 Kubernetes 에 의해 자동으로 오브젝트에 추가되지만, 나머지 어노테이션은 사용자에 의해 수동으로 추가됩니다.

어노테이션은 Kubernetes 에 새로운 기능을 추가할 때 흔히 사용됩니다. 일반적으로 새로운 기능의 알파나 베타 버전은 API 오브텢ㄱ트에 새로운 필드를 바로 도입하지 않습니다. 필드 대신 어노테이션을 사용하고, 필요한 API 변경이 명확해지고 Kubernetes 개발자가 이에 동의하면 새로운 필드가 도입됩니다. 그리고 관련 어노테이션은 사용이 중단됩니다.

어노테이션이 유용하게 사용되는 경우는 파드나 다른 API 오브젝트에 설명을 추가해 두는것입니다. 이렇게 하면 클러스터를 사용하는 모든 사람이 개별 오브젝트에 관한 정보를 빠르게 찾아볼 수 있습니다. 예를 들어 오브젝트를 만든 사람 이름을 어노테이션으로 지정하면 좀 더 쉽게 협업할 수 있습니다.

### Looking up an object’s annotations

어노테이션을 보기 위해서 `kubectl describe` 명령을 이용하거나 YAML 전체 내용을 요청해야 합니다. 다음 예제 안에 있는 첫 번째 옵션을 사용하겠습니다.

```shell
$ kubectl get po kubia-zxzij -o yaml
apiVersion: v1
kind: pod
metadata:
  annotations:
    kubernetes.io/created-by: |
      {"kind":"SerializedReference", "apiVersion":"v1",
      "reference":{"kind":"ReplicationController", "namespace":"default", ...
```

`kubernetes.io/created-by` 어노테이션이 오브젝트를 사용할 때 사용한 JSON 데이터를 가지고 있는 것을 볼 수 있습니다. 이 데이터는 레이블에 넣고 싶은 데이터가 아닙니다. 레이블에는 짧은 데이터를 넣고, 어노테이션은 상대적으로 큰 데이터를 넣을 수 있습니다.(256 KB 까지)

### Adding and modifying annotations

레이블을 만들 때와 같은 방법으로 파드를 생성할 때 어노테이션을 추가할 수 있습니다. 이미 존재하는 파드에 어노테이션을 추가하거나 수정하는 것도 가능합니다. 어노테이션을 추가하는 가장 간단한 방법은 `kubectl annotate` 명령을 사용하는 것입니다. 

`kubia-manual` 파드에 어노테이션을 추가해보겠습니다.

```shell
$ kubectl annotate pod kubia-manual mycompany.com/someannotation="foo bar"
pod "kubia-manual" annotated
```

`mycompany.com/someannotation` 어노테이션을 `foo bar` 라는 값과 함께 추가했습니다. 키 충돌을 방지하기 위해 어노테이션 키로 이런 형식을 사용하는 것이 좋습니다.

앞서 사용한것처럼 고유한 접두사를 사용하지 않았을 때 다른 도구나 라이브러리가 오브젝트에 어노테이션을 추가하면서 기존에 있던 어노테이션을 덮어버릴수 있습니다.

`kubectl describe` 를 이용해 추가한 어노테이션을 볼 수 있습니다.

```shell
$ kubectl describe pod kubia-manual
...
Annotations:    mycompany.com/someannotation=foo bar
...
```

## Using Namespace to Group Resources

각 오브젝트는 여러 레이블을 가질 수 있기 때문에, 오브젝트 그룹은 서로 겹쳐질 수 있습니다. 또한 클러스터에서 작업을 수행할 때 레이블 셀렉터를 명시적으로 지정하지 않으면 항상 모든 오브젝트를 보게됩니다.

Kubernetes 는 오브젝트를 네임스페이스로 그룹화합니다. Kubernetes 네임스페이스는 오브젝트 이름의 범위를 제공합니다. 모든 리소스를 하나의 단일 네임스페이스에 두는 대신에 여러 네임스페이스로 분할할 수 있으며, 이렇게 분리된 네임스페이스는 같은 리소스 이름을 다른 네임스페이스에 걸쳐 여러 번 사용할 수 있게 해줍니다.

### Understanding the need for namespaces

여러 네임스페이스를 사용하면 많은 구성 요소를 가진 복잡한 시스템을 좀 더 작은 개별 그룹으로 분리할 수 있습니다. 또한 **멀티테넌트(Multi-Tenant)** 환경처럼 리소스를 분리하는 데 사용됩니다. 리소스를 프로덕션, 개발 QA 환경이나 원하는 다른 방법으로 나누어 사용할 수 있습니다.

리소스 이름은 네임스페이스 안에서만 고유하면 됩니다. 서로 다른 두 네임스페이스는 동일한 이름의 리소스를 가질 수 있습니다. 대부분의 리소스 유형은 네임스페이스 안에 속하지만 일부는 그렇지 않습니다. 그 가운데 하나는 노드 리소스인데, 이 리소스는 전역이며 단일 네임스페이스에 얽매이지 않습니다.

### Discovering other namespaces and their pods

먼저 클러스터에 있는 모든 네임스페이스를 나열하겠습니다.

```shell
$ kubectl get ns
NAME          LABELS    STATUS    AGE
default       <none>    Active    1h
kube-public   <none>    Active    1h
kube-system   <none>    Active    1h
```

지금까지는 `default` 네임스페이스에서만 작업했습니다. `kubectl get` 을 이용해 리소스를 나열할 때 네임스페이스를 명시적으로 지정한 적이 없기 때문에 `kubectl` 명령어는 항상 기본적으로 `default` 네임스페이스에 속해 있는 오브젝트만 표시했습니다.

그러나 목록을 보면 `kube-public` 과 `kube-system` 네임스페이스도 존재하는 것을 알 수 있습니다. `kube-system` 네임스페이스에 속해있는 파드를 보겠습니다.

```shell
$ kubectl get po --namespace kube-system
NAME                                 READY     STATUS    RESTARTS   AGE
fluentd-cloud-kubia-e8fe-node-txje   1/1       Running   0          1h
heapster-v11-fz1ge                   1/1       Running   0          1h
kube-dns-v9-p8a4t                    0/4       Pending   0          1h
kube-ui-v4-kdlai                     1/1       Running   0          1h
l7-lb-controller-v0.5.2-bue96        2/2       Running   92         1h
```

네임스페이스이름으로 유추해보면 Kubernetes 시스템 자체와 관련된 리소스입니다. 이 분리된 네임스페이스에 해당 리소스를 포함시켜 깔끔하게 정돈되도록 유지합니다.

만약 이 파드들이 `default` 네임스페이스 안에 있어 개발자가 직접 생성한 리소스와 섞여있다면, 어떤 리소스가 어디에 속해 있는지 구분하기 어렵게됩니다.

네임스페이스를 사용해 서로 관계없는 리소스를 겹치지 않는 그룹으로 분리할 수 있습니다. 여러 사용자나 그룹이 동일한 Kubernetes 클러스터를 사용하고 있고, 각자 자신들의 리소스를 관리한다면 각각 고유한 네임스페이스를 사용해야 합니다. 

이렇게 하면 다른 사용자의 리소스를 수정하거나 삭제하지 않도록 주의해야 합니다. 또한 언급한것처럼 네임스페이스가 리소스 이름에 관한 접근 범위를 제공하기 때문에 리소스 이름이 충돌하는 경우를 걱정할 필요가 없습니다.

네임스페이스는 리소스를 격리하는것 이외에도 특정 사용자가 지정된 리소스에 접근할 수 있도록 허용하고, 개별 사용자가 사용할 수 있는 컴퓨팅 리소스를 제한하는 데에도 사용됩니다.

### Creating a namespace

네임스페이스는 다른것과 마찬가지로 Kubernetes 리소스이기 때문에 YAML 파일을 Kubernetes API 서버에 요청해 생성할 수 있습니다.

```yaml
apiVersion: v1
kind: Namespace                  1
metadata:
  name: custom-namespace         2
```

1. 네임스페이스를 정의한다.
2. 네임스페이스 이름.

이제 `kubectl` 명령을 사용해 해당 파일을 Kubernetes API 서버로 전송합니다.

```shell
$ kubectl create -f custom-namespace.yaml
namespace "custom-namespace" created
```

#### Creating a namespace with kubectl create namespace

`kubectl create namespace` 명령을 사용해 네임스페이스를 생성할 수 있습니다. 이 방법은 YAML 파일을 작성하는 것보다 빠릅니다.

```shell
$ kubectl create namespace custom-namespace
namespace "custom-namespace" created
```

### Managing objects in other namespaces

생성한 네임스페이스 안에 리소스를 만들기 위해서는 `metadata` 섹션에 `namespace: custom-namespace` 항목을 넣거나 `kubectl create` 명령을 사용할 때 네임스페이스를 지정합니다.

```shell
$ kubectl create -f kubia-manual.yaml -n custom-namespace
pod "kubia-manual" created
```

이제 동일한 이름을 가진 두 파드가 있습니다. 하나는 `default` 네임스페이스에 있고 나머지는 `custom-namespace` 에 있습니다.

다른 네임스페이스 안에 있는 오브젝트를 나열하거나 어노테이션 달기, 수정 또는 삭제할 때는 `--namespace` 플래그를 `kubectl` 에 전달해야 합니다. 네임스페이스를 지정하지 않으면 `kubectl` 은 현재 `kubectl` 컨텍스트에 구성돼 있는 기본 네임스페이스에서 작업을 수행합니다.

현재 컨텍스트의 네임스페이스와 현재 컨텍스트 자체는 `kubectl config` 명령으로 변경할 수 있습니다.

### Understanding the isolation provided by namespaces

네임스페이스가 제공하지 않는 것을 설명하겠습니다. 네임 스페이스를 사용하면 오브젝트를 별도 그룹으로 분리해 특정한 네임스페이스 안에 속한 리소스를 대상으로 작업할 수 있게 해주지만, 실행 중인 오브젝트에 대한 격리는 제공하지 않습니다.

예를 들어 다른 사용자들이 서로 다른 네임스페이스에 파드를 배포할 때 해당 파드가 서로 격리돼 통신할 수 없다고 생각할 수 있지만, 반드시 그렇지 않습니다.

네임스페이스에서 네트워크 격리를 제공하는지는 Kubernetes 와 함께 배포하는 네트워킹 솔루션에 따라 다릅니다. 네트워크 솔루션이 네임스페이스 간 격리를 제공하지 않는 경우 `foo` 네임스페이스 안에 있는 파드가 `bar` 네임스페이스 안에 있는 파드의 IP 주소를 알고 잇다면, HTTP 요청과 같은 트래픽을 다른 파드로 보낼 수 있습니다.

## Stopping and Removing Pods

파드를 모두 종료시켜보겠습니다.

### Deleting a pod by name

먼저 `kubia-gpu` 파드를 이름으로 삭제합니다.

```shell
$ kubectl delete po kubia-gpu
pod "kubia-gpu" deleted
```

파드를 삭제하면 Kubernetes 안에 있는 모든 컨테이너를 종료하도록 지시합니다. Kubernetes 는 SIGTERM 신호를 프로세스에 보내고 지정된 시간동안 기다립니다.

지정된 시간내에 종료하지 않으면 SIGKILL 신호를 통해 종료합니다. 프로세스가 항상 정상적으로 종료되게 하기 위해선 SIGTERM 신호를 올바르게 처리해야 합니다.

### Deleting pods using label selectors

이름을 지정해 파드를 삭제하는 대신 레이블 셀렉터에 관한 내용을 사용해 `kubia-manual`, `kubia-manual-v2` 를 중지할 수 있습니다. 두 파드 모두 `creation_method=manual` 레이블을 가지고 있으므로 레이블 셀렉터를 이용해 삭제할 수 있습니다.

```shell
$ kubectl delete po -l creation_method=manual
pod "kubia-manual" deleted
pod "kubia-manual-v2" deleted
```

마이크로 서비스 예제처럼 수십 개 파드를 가지고 있을 때 `rel=canary` 레이블을 지정해 모든 `canary` 파드를 지울 수 있습니다.(`Example 10`)

```shell
$ kubectl delete po -l rel=canary
```

> Example 10 - Selecting and deleting all canary pods through the rel=canary label selector

![image](https://user-images.githubusercontent.com/44635266/81057652-cc19b000-8f07-11ea-8e8b-cbc5c31f823e.png)

### Deleting pods by deleting the whole namespace

실제 파드로 가보겠습니다. `custom-namespace` 안에 있는 파드는 네임스페이스 자체를 필요로 하지 않습니다. 이런 경우 다음 명령을 사용해 네임스페이스 전체를 삭제할 수 있습니다.

```shell
$ kubectl delete ns custom-namespace
namespace "custom-namespace" deleted
```

### Deleting all pods in a namespace, while keeping the namespace

`kubectl run` 으로 생성한 파드는 아직 살아 있습니다.

```shell
$ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
kubia-zxzij     1/1     Running   0          1d
```

특정 파드를 삭제하는 대신 `--all` 옵션을 이용해 Kubernetes 가 현재 네임스페이스에 있는 모든 파드를 삭제하도록 하겠습니다.

```shell
$ kubectl delete po --all
pod "kubia-zxzij" deleted
```

실행 중인 파드가 남아있는지 확인해보겠습니다.

```shell
$ kubectl get pods
NAME            READY   STATUS        RESTARTS   AGE
kubia-09as0     1/1     Running       0          1d
kubia-zxzij     1/1     Terminating   0          1d
```

`kubia-zxzij` 는 종료되고 있지만 새로운 파드 `kubia-09as0` 가 생성됐습니다. 이는 파드를 직접 만드는 대신 **레플리케이션컨트롤러(ReplicationController)** 를 만들고 그 다음 만들었습니다. 이때문에 생성된 파드를 삭제하면 즉시 새로운 파드를 생성하기 때문에 레플리케이션컨트롤러도 삭제해야 합니다.

### Deleting (almost) all resources in a namespace

하나의 명령으로 현재 네임스페이스에 있는 모든 리소스를 삭제할 수 있습니다.

```shell
$ kubectl delete all --all
pod "kubia-09as0" deleted
replicationcontroller "kubia" deleted
service "kubernetes" deleted
service "kubia-http" deleted
```

첫 번째 `all` 은 모든 유형의 리소스를 삭제하도록 지정하고 `--all` 옵션으로 리소스 이름이 아닌 모든 리소스 인스턴스를 삭제할 것을 지정합니다.