---
title : First steps with Docker and Kubernetes
tags :
- Docker
- Kubernetes
---

*이 포스트는 [Kubernetes In Action](https://github.com/KeKe-Li/book/blob/master/kubernetes/Kubernetes%20in%20Action.pdf)를 바탕으로 작성하였습니다.*

Kubernetes 를 알아보기 전에 간단한 어플리케이션을 만들어 컨테이너 이미지로 패키징하고 관리형 Kubernetes 클러스터나 로컬의 단일 노드 클러스터에서 실행하는 방법을 살펴보겠습니다.

## CREATING, RUNNING, AND SHARING A CONTAINER IMAGE

Kubernetes 에서 구동되는 어플리케이션은 컨테이너 이미지로 패키징해야 한다는 것을 배웠습니다. Docker 의 기본적인 방법은 아래와 같습니다.

1. Install Docker and run your first “Hello world” container
2. Create a trivial Node.js app that you’ll later deploy in Kubernetes
3. Package the app into a container image so you can then run it as an isolated container
4. Run a container based on the image
5. Push the image to Docker Hub so that anyone anywhere can run it

### Installing Docker and running a Hello World container

먼저 리눅스 머신에 Docker 를 설치합니다. 리눅스를 사용하지 않는다면 가상머신을 시작하고 가상머신에 Docker 를 싱행합니다. Mac 이나 Window 를 사용하는 환경은 설명에 따라 Docker 를 설치하면 가상머신이 생성되고, 가상 머신 안에 Docker 데몬이 구동됩니다. 호스트 OS 에서 Docker 클라이언트 실행파일을 사용하면 가상머신에 구동된 Docker 데몬과 통신합니다.

Docker 를 설치하려면 http://docs.docker.com/engine/installation/ 를 참고해 운영체제에 맞게 설치를 진행합니다. 설치가 완료되면 Docker 클라이언트 실행파일로 다양한 Docker 명령을 실행할 수 있습니다.

예를 들어 Docker Hub 에있는 이미지를 **풀(pull)** 하거나 실행할 수 있습니다. Docker Hub 는 소프트웨어 패키지를위한 즉시 실행 가능한 이미지를 가지고 있습니다. 그 가운데 하나가 `busybox` 이미지이며, 간단하게 `echo "Hello World"` 명령어를 실행하는 데 사용합니다.

#### Running a Hello World container

`busybox` 는 `echo`, `ls`, `gzip` 같은 UNIX 명령을 합쳐놓은 단일 실행파일입니다.

`busybox` 이미지를 실행하기 위해 어떤 것도 다운로드하거나 설치할 필요가 없습니다. 단지 `docker run` 명령어를 사용해 어떤 이미지를 다운로드하고 실행할지, 필요하다면 실행할 다른 명령어를 추가적으로 기술하면됩니다.

```shell
$ docker run busybox echo "Hello world"
Unable to find image 'busybox:latest' locally
latest: Pulling from docker.io/busybox
9a163e0b8d13: Pull complete
fef924a0204a: Pull complete
Digest: sha256:97473e34e311e6c1b3f61f2a721d038d1e5eef17d98d1353a513007cf46ca6bd
Status: Downloaded newer image for docker.io/busybox:latest
Hello world
```

아무런 설치나 추가 작업 없이 전체 어플리케이션이 다운로드되고 실행됩니다. `busybox` 는 단일 실행파일이지만 다양한 종속성을 가진 복잡한 어플리케이션이 될 수도 있습니다.

#### Understanding what happens behind the scenes

`Example 1` 은 `docker run` 명령을 수행했을 때 일어나는 일을 보여줍니다. 먼저 Docker 는 `busybox:latest` 이미지가 로컬 컴퓨터에 존재하는지 체크합니다. 존재하지 않는다면 Docker 는 docker.io 의 Hub 레지스트리에서 이미지를 다운로드합니다.

컴퓨터에 이미지의 다운로드가 완료되면 Docker 는 이미지로부터 컨테이너를 생성하고 컨테이너 내부에서 명령어를 실행합니다. `echo` 명령어는 텍스트를 표준출력으로 출력한 후 프로세스를 중단하고 컨테이너도 중지합니다.

> Example 1 - Running echo “Hello world” in a container based on the busybox container image

![image](https://user-images.githubusercontent.com/44635266/79064666-c1437500-7ce5-11ea-8df5-e24f082768af.png)

#### Running other images

다른 이미지를 실행하는 것도 `busybox` 를 실행하는것과 동일합니다.

Docker Hub 에 공개된 이미지를 검색하거나 탐색한 후 다음과 같이 Docker 이미지를 실행하도록 전달할 수 있습니다.

```shell
$ docker run <image>
```

#### Versioning container images

Docker 는 동일한 이미지와 이름에 여러 개의 버전을 가질 수 있습니다. 각 버전은 고유한 태그를 가집니다. 이미지를 참조할 때 명시적으로 태그를 지정하지 않으면, Docker 는 `latest` 태그를 참조한 것으로 간주합니다. 다른 버전의 이미지를 실행하려면 다음과 같이 이미지 이름에 태그를 같이 지정해야 합니다.

```shell
$ docker run <image>:<tag>
```

### Creating a trivial Node.js app

Docker 설정이 완료되면 어플리케이션을 생성해보겠습니다. 간단한 Node.js 웹 어플리케이션을 만들고 이미지로 패키징합니다. 어플리케이션은 HTTP 요청을 받아 어플리케이션이 실행 중인 머신의 호스트 이름을 응답으로 반환합니다.

이렇게 하면 여느 프로세스와 마찬가지로 호스트 머신에서 실행되고 있음에도 호스트 머신의 호스트 이름을 바라보는 것이 아니라 어플리케이션이 실행 중인 컨테이너 내부의 호스트 이름을 바라보는 것을 알 수 있습니다.

Kubernetes 위에 어플리케이션을 배포하고 스케일 아웃을 할 때 유용하게 사용됩니다. HTTP 요청이 어플맄이션의 다른 인스턴스를 호출하는 것을 볼 수 있습니다.

어플리케이션은 *app.js* 라 부르는 단일 파일로 이뤄지고 다음 예제와 같은 내용으로 구성돼 있습니다.

```js
const http = require('http');
const os = require('os');

console.log("Kubia server starting...");

var handler = function(request, response) {
  console.log("Received request from " + request.connection.remoteAddress);
  response.writeHead(200);
  response.end("You've hit " + os.hostname() + "\n");
};

var www = http.createServer(handler);
www.listen(8080);
```

이 코드가 하는 일은 명확합니다. 포트 8080 으로 HTTP 서버를 시작하고, 서버는 모든 요청에 대해 상태 코드 200 OK 와 *You've hit <hostname>* 의 텍스트를 HTTP 응답으로 합니다. 요청 핸들러는 자웅에 필요한 경우를 위해 클라이언트 IP 주소를 표준 출력에 로깅합니다.

Docker 를 통해 어플리케이션은 컨테이너 이미지로 패키징하면 다운로드를 하거나 설치하지 않고도 어디서든 실행할 수 있습니다.

### Creating a Dockerfile for the image

어플리케이션을 이미지로 패키징하기 위해 먼저 Dockerfile 이라 부르는 파일을 생성해야 합니다. Dockerfile 에는 Docker 가 이미지를 생성하기 위해 수행해야 할 지시 사항이 담겨있습니다. Dockerfile 은 app.js 파일과 동일한 디렉터리에 있어야 하며 다음 예제와 같은 내용을 가지고 잇어야 합니다.

```dockerfile
FROM node:7
ADD app.js /app.js
ENTRYPOINT ["node", "app.js"]
```

`FROM` 줄은 시작점으로 사용할 컨테이너 이미지를 정의합니다. 이 경우에는 `node` 컨테이너 이미지의 태그  7 을 사용합니다. 두 번째 줄은 로컬 디렉터리의 *app.js* 파일을 이미지의 루트 디렉터리에 동일한 이름으로 추가합니다. 마지막으로 세 번째 줄에는 이미지를 실행했을 때 수행돼야 할 명령어를 정의합니다. 이 경우는 `node app.js` 입니다.

### Building the container image

Dockerfile 과 *app.js* 파일을 생성했으므로 이미지를 빌드하기 위한 모든 것이 준비됐습니다. 이미지를 빌드하려면 다음 Docker 명령어를 실행합니다.

```shell
$ docker build -t kubia.
```

`Example 2` 는 빌드 과정에서 일어나는 일을 보여줍니다. Docker 에 현재 디렉터리의 컨텐츠를 기반으로 `kubia` 라 부르는 이미지를 빌드하라고 요청했습니다. Docker 는 디렉토리 내 Dockerfile 을 살펴보고 파일에 명시된 지시 사항에 근거해 이미지를 빌드합니다.

> Example 2 - Building a new container image from a Dockerfile

![image](https://user-images.githubusercontent.com/44635266/79064982-36b04500-7ce8-11ea-95f8-d6b9c79b61a2.png)

#### Understanding how an image is built

빌드 프로세스는 Docker 클라이언트가 수행하지 않습니다. 그 대신 디렉토리의 전체 컨텐츠가 Docker 데몬에 업로드되고 그곳에서 이미지가 빌드됩니다. Docker 클라이언트 데몬은 같은 머신에 있을 필요는 없습니다.

Linux 가 아닌 OS 에서 Docker 를 사용하는 경우 Docker 클라이언트는 호스트 OS 에 위치하고, 데몬은 가상머신 내부에서 실행됩니다. 빌드 디렉토리의 모든 파일이 데몬에 업로드돼야 하기 때문에 데몬이 로컬로 실행중이지 않은 상황에서 큰 파일이 다수 포함되면ㅁ 업로드 시간이 오래 걸릴 수 있습니다.

빌드 프로세스 동안 이미지가 사용자 컴퓨터에 저장돼 있지 않다면 Docker 는 기본 이미지(`node:7`) 를 퍼블릭 이미지 레포지토리에서 가져옵니다.

#### Understanding image layers

`busybox` 를 보면 이미지라는 것이 하나의 큰 바이너리 덩어리가 아니라 여러개의 레이어로 구성된다는것을 알 수 있습니다. 서로 다른 이미지가 여러개의 레이어를 공유할 수 있기 때문에 이미지의 저장과 전송에 효과적입니다. 예를 들어 동일한 기본 이미지(`node:7`) 를 바탕으로 다수의 이미지를 생성하더라도 기본 이미지를 구성하는 모든 레이어는 단 한 번만 저장됩니다.

또한 이미지를 가져올 때도 Docker 는 각 레이어를 개별적으로 다운로드합니다. 컴퓨터에 여러개의 레이어가 저장돼 있다면 Docker 는 저장되지 않은 레이어만 다운로드합니다.

각 Dockerfile 이 새로운 레이어를 하나만 생성한다고 생각할 수 있지만 그렇지 않습니다. 이미지를 빌드하는 동안 기본 이미지의 모든 레이어를 가져온 다음, Docker 는 그 위에 새로운 레이어를 생성하고 *app.js* 파일을 그 위에 추가합니다. 그 다음 이미지가 실행할 때 수행돼야 할 명령을 지정하는 또 하나의 레이어를 추가합니다. 이 마지막 레이어는 `kubia:latest` 라고 태그를 지정합니다.

`Example 3` 을 보면 어떻게 `other:latest` 라는 별도의 이미지가 `kubia:latest` 에 사용하는 것과 동일한 *Node.js* 이미지의 레이어를 사용할 수 있는지 보여줍니다.

> Example 3 - Container images are composed of layers that can be shared among different images.

![image](https://user-images.githubusercontent.com/44635266/79681972-767fab00-8259-11ea-9fe6-af7c42d3948d.png)

이비지 빌드 프로세스가 완료되면 새로운 이미지가 로컬에 저장됩니다. 아래 예제와 같이 로컬에 저장된 이미지 리스트를 Docker 에 요청할 수 있습니다.

```shell
$ docker images
REPOSITORY   TAG      IMAGE ID           CREATED             VIRTUAL SIZE
kubia        latest   d30ecc7419e7       1 minute ago        637.1 MB
...
```

#### Comparing building images with a Dockerfile vs. manually

Dockerfile 은 Docker 컨테이너 이미지를 생성하는 일반적인 방법이지만, 기존 이미지에서 컨테이너를 실행하고 컨테이너 내부에서 명령어를 수행한 후 빠져나와 최종 상태를 새로운 이미지로 **커밋(commit)** 하는 방법으로 이미지를 수동으로 생성할 수 있습니다.

이는 Dockerfile 로부터 빌드를 하는 것과 정확히 동일한 방법이지만, Dockerfile 을 이용하는 것이 훨씬 반복 가능하고 이미지 빌드를 자동화할 수 있는 방법입니다. 이는 모든 명령어를 다시 수동으로 입력할 필요 없이 Dockerfile 만 변경하면 언제든지 다시 빌드할 수 있기 때문입니다.

### Running the container image

다음 명령어를 이용해 이미지를 실행할 수 있습니다.

```shell
$ docker run --name kubia-conatainer -p 8080:8080 -d kubia
```

이 명령어는 Docker 가 `kubia` 이미지에서 `kubia-container` 라는 이름의 새로운 컨테이너를 실행하도록 합니다. 컨테이너는 `-d` 플래그로 백그라운드에서 실행됨을 의미하며 `-p 8080:8080` 은 로컬 머신의 8080 포트가 컨테이너 내부의 8080 포트오 매핑되어 http://localhost:8080 으로 어플리케이션에 접근할 수 있습니다.

로컬 머신에서 Docker 데몬이 실행 중이 아니라면 localhost 대신 데몬이 실행 중인 가상머신의 호스트 이름이나 IP 를 사용해야 합니다. 이 정보는 `DOCKER_HOST` 환경변수로 확인 가능합니다.

#### Accessing your app

이제 http://localhost:8080 의 어플리케이션에 접근해보겠습니다.

```shell
$ curl localhost:8080
You've hit 44d76963e8e1
```

이것이 어플리케이션의 응답입니다. 작은 어플리케이션은 격리된 컨테이너 내부에서 실행중입니다. 호스트 이름을 44d76963e8e1 을 응답하지만 호스트 머신의 호스트 이름과 다르다는 것을 알 수 있습니다. 이 16 진수는 Docker 컨테이너의 ID 입니다.

#### Listing all running containers

다음 예제와 같이 실행 중인 모든 컨테이너를 조회해서 리스트를 확인할 수 있습니다.

```shell
$ docker ps
CONTAINER ID  IMAGE         COMMAND               CREATED        ...
44d76963e8e1  kubia:latest  "/bin/sh -c 'node ap  6 minutes ago  ...

...  STATUS              PORTS                    NAMES
...  Up 6 minutes        0.0.0.0:8080->8080/tcp   kubia-container
```

컨테이너 하나가 실행 중입니다. Docker 는 각 컨테이너의 ID, 이름, 컨테이너를 실행하는 데 사용된 이미지, 내부에 수행된 명령어를 출력합니다.

#### Getting additional information about a container

`docker ps` 명령어는 컨테이너의 기본 정보만 표시합니다. 자세한 정보를 보려면 `docker inspect` 를 사용합니다.

```shell
$ docker inspect kubia-container
```

Docker 는 컨테이너 상세 정보를 JSON 형식으로 출력할 것입니다.

### Exploring the inside of a running container

컨테이너 내부의 환경을 보고싶다면  추가 프로세스를 실행해서 컨테이너 내부를 살펴볼 수 있습니다.

#### Running a shell inside an existing container

실행 중인 컨테이너의 기본 이미지인 *Node.js* 는 `bash` 셸을 포함하고 있으므로 다음과 같이 내부에서 셸을 실행할 수 있습니다.

```shell
$ docker exec -it kubia-container bash
```

이 명령어는 현재 실행 중인 `kubia-container` 컨테이너 내부에 `bash` 를 실행합니다. `bash` 프로세스는 컨테이너의 메인 프로세스와 동일한 리눅스 네임스페이스를 가집니다. 따라서 컨테이너 내부를 탐색할 수 있고, 컨테이너 내부에서 실행될 때 *Node.js* 와 어플리케이션이 시스템을 보는 방법을 알 수 있습니다. `-it` 옵션은 두 옵션을 축약한 것입니다.

* `-i` : 표준입력을 오픈 상태로 유지합니다. 쉘에 명령어를 입력하기 위해 필요하다.
* `-t` : **의사(pseudo)** 터미널을 할당한다.

일반적인 쉘을 사용하는것과 동일하게 쉘을 사용하고 싶다면 두 옵션이 필요합니다.

#### Exploring the container from within

다음 예제를 통해 쉘을 사용해 컨테이너 내부에 실행 중인 프로세스를 조회하는 방법을 살펴볼 수 있습니다.

```shell
root@44d76963e8e1:/# ps aux
USER  PID %CPU %MEM    VSZ   RSS TTY STAT START TIME COMMAND
root    1  0.0  0.1 676380 16504 ?   Sl   12:31 0:00 node app.js
root   10  0.0  0.0  20216  1924 ?   Ss   12:31 0:00 bash
root   19  0.0  0.0  17492  1136 ?   R+   12:38 0:00 ps aux
```

3 개의 프로세스만 볼 수 있고 호스트 운영체제의 다른 프로세스는 볼 수 없습니다.

#### Understanding that processes in a container run in the host operating system

다른 터미널을 열고 호스트 운영체제의 프로세스를 조회하면 모든 프로세스를 조회할 수 있는데 아래 예제와 같이 컨테이너에서 실행 중인 프로세스도 볼 수 있습니다.

```shell
$ ps aux | grep app.js
USER  PID %CPU %MEM    VSZ   RSS TTY STAT START TIME COMMAND
root  382  0.0  0.1 676380 16504 ?   Sl   12:31 0:00 node app.js
```

이는 컨테이너에 실행 중인 프로세스가 호스트 운영체제에서 실행 중이라는 것을 증명합니다. 자세히 살펴보면 호스트 운영체제와 컨테이너 내부에서 조회한 프로세스의 ID 가 다르다는 것을 알 수 있습니다. 컨테이너는 자체 리눅스 PID 네임 스페이스를 사용하며 고유의 시퀀스 번호를 가지고 완전히 분리된 프로세스 트리를 가지고 있습니다.

#### The container’s filesystem is also isolated

격리된 프로세스를 가진 것과 마찬가지로 각 컨테이너는 격리된 파일 시스템을 가지고 있습니다.

컨테이너 내부에서 루트 디렉토리의 내용을 조회해보면 컨테이너 안의 파일을 보여줍니다. 아래 예제를 보면 이 파일들은 이미지에 있는 모든 파일과 컨테이너가 실행되는 동안 생성한 파일을 포함합니다.

```shell
root@44d76963e8e1:/# ls /
app.js  boot  etc   lib    media  opt   root  sbin  sys  usr
bin     dev   home  lib64  mnt    proc  run   srv   tmp  var
```

*app.js* 파일과 사용한 `node:7` 기본 이미지의 일부인 시스템 디렉토리를 포함하고 있습니다.

### Stopping and removing a container

어플리케이션을 종료하기 위해 Docker 에게 `kubia-container` 를 중지하도록 명령하겠습니다.

```shell
$ docker stop kubia-container
```

이는 컨테이너에 실행 중인 메인 프로세스를 중지시키며 컨테이너 내부에 실행 중인 다른 프로세스가 없으므로 결과적으로 컨테이너가 중지됩니다. `docker ps -a` 로 보면 컨테이너 자체는 존재함을 확인할 수 있습니다. `-a` 실행 중인 컨테이너와 중지된 모든 컨테이너를 출력합니다.

컨테이너를 완전히 삭제하려면 `docker rm` 명령을 수행해야 합니다.

```shell
$ docker rm kubia-container
```

이렇게 하면 컨테이너가 삭제됩니다.

### Pushing the image to an image registry

지금까지 빌드한 이미지는 로컬에서만 사용이 가능했습니다. 다른 컴퓨터에서도 실행 가능하려면 외부 이미지 저장소에 이미지를 푸시해야 합니다. 공개적으로 사용할 수 있는 레지스트리 중 하나인 Docker Hub 에 이미지를 푸시하겠습니다.

이미지를 푸시하기 전에 Docker Hub 규칙에 따라 이미지 태그를 다시 지정해야 합니다. 이미지의 리포지토리 이름이 Docker Hub ID 로 시작해야만 이미지를 푸시할 수 있습니다. http://hub.docker.com 에 등록해 Docker Hub ID 를 생성합니다.

#### Tagging an image under an additional tag

ID 가 준비되었으면 `kubia` 로 태그된 이미지를 `luksa/kubia` 로 바꿔줍니다.

```shell
$ docker tag kubia luksa/kubia
```

이 명령은 태그를 변경하지 않습니다. 같은 이미지에 추가적인 태그를 생성합니다. 예제와 같이 `docker image` 명령으로 시스템에 저장된 이미지를 조회해 추가된 태그를 확인할 수 있습니다.

```shell
$ docker images | head
REPOSITORY        TAG      IMAGE ID        CREATED             VIRTUAL SIZE
luksa/kubia       latest   d30ecc7419e7    About an hour ago   654.5 MB
kubia             latest   d30ecc7419e7    About an hour ago   654.5 MB
docker.io/node    7.0      04c0ca2a8dad    2 days ago          654.5 MB
...
```

예제에서 보는것처럼 `kubia` 와 `luksa/kubia` 가 동일한 이미지 ID 를 가리키고 있으므로 사실 같은 이미지에 두 개의 태그를 갖는것입니다.

#### Pushing the image to Docker Hub

Docker Hub 에 이미지를 푸시하기 전에 `docker login` 명령을 이용해 로그인해야 합니다. 로그인을 하면 아래와 같이 `yourid/kubia` 로 이미지를 푸시할 수 있습니다.

```shell
$ docker push luksa/kubia
```

#### Running the image on a different machine

Docker Hub 에 이미지 푸시가 완료되면 모든 사람이 이미지를 사용할 수 있습니다. 이제 다음 명령어를 실행하면 Docker 를 실행하는 모든 머신에 이미지를 실행할 수 있습니다.

```shell
$ docker run -p 8080:8080 -d luksa/kubia
```

## SETTING UP A KUBERNETES CLUSTER

Docker 에서 직접 실행하는 대신 Kubernetes 클러스터에 배포할 수 있습니다. 

### Running a local single-node Kubernetes cluster with Minikube

정상적으로 동작하는 Kuberentes 를 가장 빠르고 간단하게 접근하는 방법은 Minikube 를 사용하는 것입니다. Minikube 는 로컬에서 Kuberentes 를 테스트하고 어플리케이션을 개발하는 목적으로 단일 노드 클러스터를 설치하는 도구입니다.

여러 노드에서 어플리케이션을 관리하는 것과 관련된 Kuberentes 기능을 볼 수는 없지만 단일 노드 클러스터만으로도 이 책에서 다루는 대부분의 주제를 살펴보기엔 충분합니다.

#### Installing Minikube

Minikube 는 단일 이진 파일로 다운로드한 후 실행 가능한 특정 경로에 저장합니다. OSX, Linux, Window 에서 사용가능합니다.

예를 들어 OSX 나 리눅스는 Minkube 를 명령어 하나로 다운로드하고 설치할 수 있습니다. OSX 는 다음과 같습니다.

```shell
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/
 v0.23.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube
 /usr/local/bin/
```

Linux 에서는 다른 릴리스를 다운로드합니다. 윈도우 환경에서는 파일을 수동으로 다운로드하고 *minikube.exe* 로 이름을 바꿔 실행 가능한 경로로 이동합니다. Minikube 는 VirtualBox 나 KVM 을 통해 실행된 가상머신 내부에 Kuberentes 를 실행하므로 Minikube 클러스터를 시작하기전에 이 가운데 하나를 설치해야 합니다.

#### Starting a Kubernetes cluster with Minikube

Minikube 가 설치되면 아래 명령어를 사용해 Kuberentes 클러스터를 바로 시작할 수 있습니다.

```shell
$ minikube start
Starting local Kubernetes cluster...
Starting VM...
SSH-ing files into VM...
...
Kubectl is now configured to use the cluster.
```

#### Installing the Kubernetes client (kubectl)

Kuberentes 를 다루려면 `kubectl` CLI 클라이언트가 필요합니다.필요한 것은 바이너리를 다운로드하고 실행 가능한 경로에 두는 것입니다. 예를 들어 OSX 는 다음 명령어를 사용해 다운로드하고 설치할 수 있습니다.

```shell
$ curl -LO https://storage.googleapis.com/kubernetes-release/release
 /$(curl -s https://storage.googleapis.com/kubernetes-release/release
 /stable.txt)/bin/darwin/amd64/kubectl
 && chmod +x kubectl
 && sudo mv kubectl /usr/local/bin/
```

Linux 에서 `kubectl` 을 다운로드하기 위해서 URL 의 `darwin` 을 `linux` 로 변경합니다. 윈도우에서는 `windows` 로 변경하고 맨 뒤에 *.exe* 를 추가합니다.

#### Checking to see the cluster is up and kubectl can talk to it

아래와 같이 `kubectl cluster-info` 명령어를 사용해 클러스터가 정상 작동하는지 확인합니다.

```shell
$ kubectl cluster-info
Kubernetes master is running at https://192.168.99.100:8443
KubeDNS is running at https://192.168.99.100:8443/api/v1/proxy/...
kubernetes-dashboard is running at https://192.168.99.100:8443/api/v1/...
```

이는 클러스터가 동작중임을 나타냅니다.

### Using a hosted Kubernetes cluster with Google Kubernetes Engine

완전한 다중 노드 Kuberentes 를 살펴보려면 GKE 클러스터를 사용할 수 있습니다. 이 방법을 사용하면 모든 클러스터 노드와 네트워킹을 수동으로 설정할 필요가 없으며 Kuberentes 를 처음 접하는 사람들의 부담을 줄여줍니다.

#### Setting up a Google Cloud project and downloading the necessary client binaries

새로운 Kuberentes 클러스터를 생성하기 전에 GKE 환경을 먼저 설정해야 합니다. 전체 절차는 대략적으로 다음과 같습니다.

1. 구글에 가입한다.
2. GCP 콘솔에 프로젝트를 만든다.
3. 빌링을 활성화한다.
4. Kuberentes 엔진 API 를 활성화한다.
5. 구글 클라우드 SDK 를 다운로드하고 설치한다.
6. `gcloud components install kubectl` 명령으로 `kubectl` 명령행 도구를 설치한다.

#### Creating a Kubernetes cluster with three nodes

설치가 완료되면 아래에 표시된 명령어를 사용해 워커 노드 3 개를 가진 Kuberentes 클러스터를 생성할 수 있습니다.

```shell
$ gcloud container clusters create kubia --num-nodes 3
 --machine-type f1-micro
Creating cluster kubia...done.
Created [https://container.googleapis.com/v1/projects/kubia1-
     1227/zones/europe-west1-d/clusters/kubia].
kubeconfig entry generated for kubia.
NAME   ZONE   MST_VER MASTER_IP     TYPE     NODE_VER NUM_NODES STATUS
kubia  eu-w1d 1.5.3   104.155.92.30 f1-micro 1.5.3    3         RUNNING
```

`Example 4` 와 같이 워커 노드 3 개를 가진 Kuberentes 클러스터를 생성했습니다. 노드 3 개를 사용하면 다중 노드를 활용하는 기능을 제대로 시연할 수 있습니다.

> Example 4 - How you’re interacting with your three-node Kubernetes cluster

![image](https://user-images.githubusercontent.com/44635266/79681977-84cdc700-8259-11ea-9715-50cc0adaa904.png)

#### Getting an overview of your cluster

클러스터의 기본 아이디어와 상호작용 방법은 `Example 4` 를 참고하면 됩니다. 각 노드는 Docker, Kubelet, kube-proxy 를 실행합니다. `kubectl` 클라이언트 명령어는 마스터 노드에서 실행 중인 Kubernetes API 서버로 REST 요청을 보내 클러스터와 상호작용합니다.

#### Checking if the cluster is up by listing cluster nodes

아래 예제와 같이 `kubectl` 명령으로 클러스터의 모든 노드를 조회합니다.

```shell
$ kubectl get nodes
NAME                      STATUS  AGE  VERSION
gke-kubia-85f6-node-0rrx  Ready   1m    v1.5.3
gke-kubia-85f6-node-heo1  Ready   1m    v1.5.3
gke-kubia-85f6-node-vs9f  Ready   1m    v1.5.3
```

`kubectl` 명령어로 모든 종류의 Kubernetes 오브젝트를 조회할 수 있습니다.

#### Retrieving additional details of an object

오브젝트에 대한 상세 정보를 보려면 `kubectl describe` 명령을 사용할 수 있습니다.

```shell
$ kubectl describe node gke-kubia-85f6-node-0rrx
```

여기서 `describe` 명령의 출력 결과는 상당히 길고 완전히 읽기 어려우므로 생략합니다. 출력 결과는 CPU 와 메모리, 시스템 정보, 노드에 실행 중인 컨테이너 등을 포함한 노드 상태를 보여줍니다.

`Kubectl describe` 예제에서 특정 노드의 이름을 명시했지만 노드의 이름을 입력하지 않고 `kubectl describe node` 라 수행하면 모든 노드의 상세 정보가 출력됩니다.

Kubernetes 에 첫 번째 어플리케이션을 실행하기 전에, 키 입력을 줄이기 위한 방법과 같은 `kubectl` 을 훤씬 쉽게 사용하기 위한 추가적인 방법을 살펴보겠습니다.

### Setting up an alias and command-line completion for kubectl

`kubectl` 을 자주 사용하면 이 명령어를 매번 입력하는게 힘들 수 있습니다. 이를 위해 `kubectl` 의 **별칭(Alias)** 를 설정해보겠습니다.

#### Creating an alias

`kubectl` 을 `k` 로 바꿔서 설정하겠습니다. *~/.bashrc* 파일에 다음 행을 추가합니다.

```shell
alias k=kubectl
```

#### Configuring tab completion for kubectl

`kubectl` 명령어는 `bash` 와 `zsh` 쉘에서 완성 기능을 사용할 수 있습니다. 명령어 이름분만 아니라 오브젝트 이름에 관해서 탭 완성을 사용할 수 있습니다. 이전에 살펴봤던 명령어의 전체 이름을 입력했다면 다음과 같이 입력할 수 있습니다.

```shell
$ kubectl desc<TAB> no<TAB> gke-ku<TAB>
```

`bash` 탭 완성을 활성화하려면 먼저 `bash-competion` 패캐지를 설치하고 다음 명령어를 실행해야 합니다.

```shell
$ source <(kubectl completion bash)
```

여기서 주의사항이 있습니다. 위 명령을 실행하면 탭 완성은 전체 `kubectl` 이름을 사용할 때만 동작합니다. 이 문제를 해결하려면 `kubectl` 와선 명령의 출력을 일부 변경해야 합니다.

```shell
$ source <(kubectl completion bash | sed s/kubectl/k/g)
```

이제 명령어에 많은 입력 없이도 클러스터와 상호작용할 수 있습니다. 

## RUNNING YOUR FIRST APP ON KUBERNETES

Kubernetes 위에 어플리케이션을 실행할 수 있는 간단한 방법을 사용하겠습니다. 보통 배포하고자 하는 구성 요소를 기수한 JSON, YAML 매니페스트를 준비해야지만 간단한 명령어 한 줄로 어플리케이션을 실행하겠습니다.

### Deploying your Node.js app

어플리케이션을 배포하기 위한 가장 간단한 방법은 `kubectl run` 명령어를 사용해 JSON 이나 YAML 을 사용하지 않고 필요한 구성 요소를 생성하는 방법입니다. 이렇게 하면 오브젝트의 구조를 깊이 살펴볼 필요가 없습니다.

이전에 생성해 Docker Hub 에 푸시한 이미지를 실행해보겠습니다. Kubernetes 에 실행하는 방법은 다음과 같습니다.

```shell
$ kubectl run kubia --image=luksa/kubia --port=8080 --generator=run/v1
replicationcontroller "kubia" created
```

`--image=luksa/kubia` 부분은 실행하고자 하는 컨테이너 이미지를 명시하는 것이고 `-port=8080` 옵션은 Kubernetes 에 어플리케이션이 8080 포트를 수신 대기해야 하는 사실을 알려줍니다. `--generator` 는 Kubernetes 에서 디플로이먼트 대신 레플리케이션컨트롤러를 생성하기 때문에 사용했습니다.

#### Introducing Pods

Kubernetes 는 개별 컨테이너를 직접 다루지 않습니다. 대신 함께 배치된 다수의 컨테이너라는 개념을 사용합니다. 이 컨테이너의 그룹을 **파드(Pods)** 라 합니다.

파드는 하나 이상의 밀접하게 연관된 컨테이너 그룹으로 같은 워커 노드에서 같은 리눅스 네임스페이스로 함께 실행됩니다. 파드는 자체 IP, 호스트 이름, 프로세스 등이 있는 논리적으로 분리된 머신입니다. 어플리케이션은 단일 컨테이너로 실행되는 단일 프로세스일 수도 있고, 개별 컨테이너에서 실행되는 주 어플리케이션 프로세스와 부가적으로 도와주는 프로세스로 이뤄질 수 있습니다.

파드에서 실행 중인 모든 컨테이너는 동일한 논리적인 머신에서 실행하는 것처럼 보이는 반면, 다른 파드에 실행 중인 컨테이너는 같은 워커 노드에서 실행 중이라 할지라도 다른 머신에서 실행 중인 것으로 나타납니다.

컨테이너와 파드, 노드 간의 관계를 더 잘 이해하려면 `Example 5` 를 보면 됩니다. 각 파드는 고유한 IP 와 어플리케이션 프로세스를 실행하는 하나 이상의 컨테이너를 가집니다. 파드는 다른 워커 노드에 퍼져있습니다.

> Example 5 - The relationship between containers, pods, and physical worker nodes

![image](https://user-images.githubusercontent.com/44635266/79681980-8c8d6b80-8259-11ea-8391-1452f3734688.png)

#### Introducing Pods

컨테이너는 독립적인 Kubernetes 오브젝트가 아니기 때문에 개별 컨테이너를 조회할 수 없습니다. 대신 파드를 조회해야 합니다. 아래 예제를 통해 `kubectl` 로 파드를 조회해보겠습니다.

```shell
$ kubectl get pods
NAME          READY     STATUS    RESTARTS   AGE
kubia-4jfyf   0/1       Pending   0          1m
```

파드가 보입니다. 파드의 상태가 **보류(Pending)** 상태로 파드의 단일 컨테이너가 아직 준비가 되지 않았습니다. 파드가 아직 실행되지 않은 이유는 할당된 워커 노드가 컨테이너를 실행하기 전에 컨테이너 이미지를 다운로드 하는 중이기 때문입니다.

다운로드가 완료되면 파드의 컨테이너가 생성되고 파드의 상태가 다음과 같이 `Running` 상태로 전환됩니다.

```shell
$ kubectl get pods
NAME          READY     STATUS    RESTARTS   AGE
kubia-4jfyf   1/1       Running   0          5m
```

`kubectl describe pod` 명령어로 파드의 세부 정보를 볼 수 있습니다. 파드가 Pending 상태면 Kubernetes 가 레지스트리로부터 이미지를 가져오지 못했기 때문일 수 있습니다. 자체 이미지를 사용한다면 Docker Hub 에 **퍼블릭(Public)** 으로 표시돼 있는지 확인해야합니다.

이미지를 가져올 수 있는지 확인하기 위해 다른 머신에서 `docker pull` 명령으로 이미지 **풀링(Pulling)** 을 시도할 수 있습니다.

#### Understanding what happened behind the scenes

어떤 프로세스가 진행되는지 보기위해 `Example 6` 으로 시각화 했습니다.

Kubernetes 내부에서 이미지를 가져오기 위해 수행하는 모든 단계를 보여줍니다.

1. 이미지를 빌드해 Docker Hub 에 푸시
2. `kubectl` 명령어를 실행해 Kubernetes API 서버로 REST HTTP 요청을 전달하고 클러스터에 새로운 레플리케이션 컨트롤러 오브젝트 생성
3. 레플리케이션 컨트롤러는 새 파드를 생성하고 **스케줄러(Scheduler)** 가 워커 노드 중 하나에 스케줄링
4. 해당 워커 노드의 `Kubelet` 는 파드가 스케줄링 된걸 확인
5. 이미지가 로컬에 없기 때문에 Docker 에게 레지스트리에서 특정 이미지를 풀 하도록 지시
6. 이미지 다운 후 Docker 는 컨테이너를 생성하고 실행

> Example 6 - Running the luksa/kubia container image in Kubernetes

![image](https://user-images.githubusercontent.com/44635266/80271208-19707300-86f9-11ea-8298-5844e43a8b62.png)

### Accessing your web application

각 파드는 자체 IP 를 가지고 있지만, 이 주소는 클러스터 내부에 있으며 외부에서 접근이 불가능합니다. 

#### Creating a Service object

```shell
$ kubectl expose rc kubia --type=LoadBalancer --name kubia-http
service "kubia-http" exposed
```

#### Listing services

`expose` 명령어의 출력 결과를 보면 `kubia-http` 라는 서비스가 표시됩니다. 서비스는 파드나 노드 같은 오브젝트로 아제 예제와 같이 `kubectl get services` 명령으로 새로 생성된 서비스 오베즉트를 볼 수 있습니다.

```shell
$ kubectl get services
NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
kubernetes   10.3.240.1     <none>        443/TCP         34m
kubia-http   10.3.246.185   <pending>     8080:31348/TCP  4s
```

이 예제는 두 가지 서비스를 보여줍니다. 여기서 `kubernetes` 서비스에 관한 설명은 생략하고 생성한 `kubia-http` 서비스를 살펴보겠습니다. Kubernetes 가 실행 중인 클라우드 인프라 스트럭처에서 로드 밸런서를 생성하는 데 시간이 걸리기 때문에 아직 외부 IP 주소는 없습니다.

로드 밸런서의 기동이 완료되면 서비스의 외부 IP 주소가 표시됩니다. 아래 예제와 같이 서비스를 다시 조회해보겠습니다.

```shell
$ kubectl get svc
NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
kubernetes   10.3.240.1     <none>        443/TCP         35m
kubia-http   10.3.246.185   104.155.74.57 8080:31348/TCP  1m
```

외부 IP 가 확인이 됩니다. 어플리케이션이 외부의 어디에서나 http://104.155.74.57:8080 으로 접근이 가능합니다.

#### Accessing your service through its external IP

이제 서비스의 외부 IP 와 포트를 통해 파드에 요청할 수 있습니다.

```shell
$ curl 104.155.74.57:8080
you've hit kubia-4jfyf
```

이 어플리케이션 노드 3 개의 Kubernetes 클러스터 중 어디선가 실행되고 있습니다. 전체 클러스터를 생성하기 위한 절차를 제외하면 두 개의 명령어로 어플리케이션을 실행하고 외부 사용자들이 접근 가능하게 만들었습니다.

어플리케이션에서 파드 이름을 호스트 이름으로 사용한다는 것을 알 수 있습니다. 아서 언급했듯이 각 파드는 자체 IP 주소와 호스트 이름을 가진 별도의 독립 머신처럼 동작합니다. 어플리케이션이 워커 노드 운영체제에서 실행 중이라 할지라도 어플리케이션은 다른 프로세스와 함께 실행중인 상태가 아니며 어플리케이션 전용으로 분리된 머신에서 실행중인 것으로 나타납니다.

### The logical parts of your system

시스템의 물리적인 관점 외에도 논리적으로 분리된 관점도 있습니다. 파드, 레플리케이션 컨트롤러, 서비스에 관해 언급했습니다. 이어지는 몇몇 장에서 모두 설명하겠지만 어떻게 어울려 돌아가는지, 각각 어떤 역할을 하는지 살펴보면 될거같습니다.

##### Understanding how the ReplicationController, the Pod, and the Ser- rvice fit together

사용자가 컨테이너를 직접 생성하거나 동작시키지는 않습니다. 대신 Kubernetes 의 기본 빌딩 블록인 파드를 이용합니다. 파드도 직접 생성하지 않습니다. `kubectl run` 명령을 수행하면 레플리케이션컨트롤러를 생성하고 레플리케이션컨트롤러가 실제 파드를 새엇ㅇ합니다. 클러스터 외부에 파드에 접근하게 하기 위해 Kubernetes 에게 레플리케이션컨트롤러에 의해 관리되는 모든 파드를 단일 서비스로 노출하도록 명령하겠습니다. 아래 `Example 7` 에 세 가지 구성 요소를 간략하게 표현했습니다.

> Example 7 - Your system consists of a ReplicationController, a Pod, and a Service.

![image](https://user-images.githubusercontent.com/44635266/80271213-21c8ae00-86f9-11ea-881c-546c577c1da3.png)

#### Understanding the pod and its container

시스템의 가장 중요한 구성 요소는 파드입니다. 여기서 파드가 하나의 컨테이너를 가지고 있지만 보통 파드는 원하는 만큼의 컨테이너를 포함시킬 수 있습니다. 컨테이너 내부에는 Node.js 프로세스가 있고 포트 8080 에 바인딩되어 HTTP 요청을 기다리고 있습니다. 파드는 자체의 고유한 사설 IP 주소와 호스트 이름을 가집니다.

#### Understanding the role of the ReplicationController

다음 구성 요소는 `kubia` 레플리케이션컨트롤러입니다. 항상 하나의 파드 인스턴스를 실행하도록 지정합니다. 보통 레플리케이션 컨트롤러는 파드를 복제하고 항상 실행 상태로 만듭니다. 여기서 파드의 레플리카를 지정하지 않았기 때문에 레플리케이션 컨트롤러는 파드를 하나만 생성했습니다. 파드가 사라진다면 레플리케이션컨트롤러는 사라진 파드를 대체하기 위해 새로운 파드를 생성할것입니다.

#### Understanding why you need a service

시스템의 세 번째 구성 요소는 `kubia-http` 서비스입니다. 서비스가 필요한 이유를 이해하기 위해 파드의 주요 특성을 알아야 합니다. 파드는 **일시적(Ephemeral)** 입니다.

파드는 언제든 사라질 수 있습니다. 그래서 사라진 파드는 레플리케이션컨트롤러에 의해 생성된 파드로 대체됩니다. 새로운 파드는 다른 IP 주소를 할당받습니다. 이것이 서비스가 필요한 이유입니다. 항상 변경되는 파드의 IP 주소문제와 여러 개의 파드를 단일 IP 와 포트의 쌍으로 노출시키는 문제를 해결합니다.

서비스가 생성되면 정적 IP 를 할당받고 서비스가 존속하는 동안 변경되지 않습니다. 파드에 직접 연결하는 대신 클라이언트는 서비스의 IP 주소를 통해 연결해야 합니다. 서비스는 어떤 파드가 어디에 존재하는지에 관계없이 파드 중 하나로 연결해 요청을 처리하도록 합니다.

서비스는 동일한 서비스를 제공하는 하나 이상의 파드 그룹의 정적 위치를 나타냅니다. 서비스의 IP 와 포트로 유입된 요청은 그 순간 서비스에 속해 있는 파드 중 하나에 전달됩니다.

### Horizontally scaling the application

실행 중인 어플리케이션은 레플리케이션컨트롤러에 의해 모니터링되고 실행되며 서비스를 통해 외부에 노출됩니다.

Kubernetes 를 사용하는 이점 중 하나는 간단하게 배포를 확장할 수 있다는 점입니다. 파드는 레플리케이션 컨트롤러에 의해 관리됩니다.`kubectl get` 명령으로 살펴보겠습니다.

```shell
$ kubectl get replicationcontrollers
NAME        DESIRED    CURRENT   AGE
kubia       1          1         17m
```

조회 결과 `kubia` 라는 단일 레플리케이션컨트롤러가 표시됩니다. `DESIRED` 열은 레플리케이션컨트롤러가 유지해야 할 파드의 레플리카 수를 보여주는 반면, `CURRENT` 열은 현재 실행 중인 파드의 실제 수를 나타냅니다. 여기서 파드의 레플리카를 하나만 실행하도록 지정했고, 정확히 하나의 레플리카가 실행 중입니다.

#### Increasing the desired replica count

파드의 레플리카 수를 늘리려면 레플리카 컨트롤러에 의해 의도하는 레플리카 수를 변경해야 합니다.

```shell
$ kubectl scale rc kubia --replicas=3
replicationcontroller "kubia" scaled
```

Kubernetes 에 파드 인스턴스 세 개를 항상 유지하도록 알려줬습니다. Kubernetes 에 어떤 액션이 필요한지 지시는 하지 않았습니다. 두 개의 파드를 추가하도록 지시하는 것이 아니라 원하는 인스턴스 수를 설정해 Kubernetes 가 요청된 상태를 달성하기 위해 어떤 액션을 취해야 하는지 판단하도록 했습니다.

이것이 가장 기본적인 Kubernetes 의 원칙 중 하나입니다. Kubernetes 가 어떤 액션을 수행해야 하는지 정확하게 알려주는 대신 시스템에 **의도하는 상태(Desired State)** 를 선언적으로 변경하고 Kubernetes 가 **실제 현재 상태(Current State)** 를 검사해 의도한 상태로 **조정(Reconcile)** 합니다. Kubernetes 전체 기능은 이와 동일한 방식으로 돌아갑니다.

#### Seeing the results of the scale-out

레플리카 수를 증가한 것으로 돌아가 레플리카 수가 업데이트됐는지 레플리케이션 컨트롤러를 다시 조회해보겠습니다.

```shell
$ kubectl get rc
NAME        DESIRED    CURRENT   READY   AGE
kubia       3          3         2       17m
```

파드의 개수가 이미 세 개도 한 개가 아닌 세 개로 표시됩니다.

```shell
$ kubectl get pods
NAME          READY     STATUS    RESTARTS   AGE
kubia-hczji   1/1       Running   0          7s
kubia-iq9y6   0/1       Pending   0          7s
kubia-4jfyf   1/1       Running   0          18m
```

파드가 하나가 아니고 세 개가 존재합니다. 두 개는 실행 중이고, 하나는 보류 중이지만 컨테이너 이미지를 다운로드하고 컨테이너가 시작하는 즉시 수분 내에 준비 상태가 될것입니다.

어플리케이션 스케일링은 이와 같이 매우 간단합니다. 일단 어플리케이션을 프로덕션 환경에서 실행 중이라면 언제든 확장이 필요할 때 새로운 복제본을 수동으로 설치하고 실행하지 않더라도 명령어 하나로 인스턴스를 추가할 수 있습니다.

어플리케이션 자체에서 수평 확장을 지원하도록 만들어야 하는것을 유념해야 합니다. Kubernetes 가 마법처럼 어플리케이션을 확장 가능하게 만들어 주지 않으며, 어플리케이션의 스케일업이나 스케일 다운을 간단하게 만들어줍니다.

#### Seeing requests hit all three pods when hitting the service

실행 중인 어플리케이션이 다수의 인스턴스를 가지기 때문에 서비스 URL 을 호출했을 때 어떤 일이 일어나는지 확인해보겟습니다.

```shell
$ curl 104.155.74.57:8080
Youve hit kubia-hczji
$ curl 104.155.74.57:8080
Youve hit kubia-iq9y6
$ curl 104.155.74.57:8080
Youve hit kubia-iq9y6
$ curl 104.155.74.57:8080
Youve hit kubia-4jfyf
```

요청이 무작위로 다른 파드를 호출합니다. 하나 이상의 파드가 서비스 뒤에 존재할 때 Kubernetes 서비스는 이렇게 행동합니다. 서비스는 다수의 파드 앞에서 로드밸런서 역할을 합니다. 파드가 하나만 있으면 서비스는 이 파드 하나에 정적 주소를 제공합니다. 서비스를 지원하는 파드가 하나든지 파드 그룹이든지 관계없이 해당 파드가 클러스터 내에서 이동하면서 생성되고 삭제되며 IP 가 변경되지만, 서비스는 항상 동일한 주소를 가집니다.

이런식으로 많은 파드가 존재하고 위치가 변경되는지 관계없이 클라이언트가 파드에 쉽게 연결할 수 있습니다.

#### Visualizing the new state of your system

이전과 무엇이 달라졌는지 시스템을 시각화해보겠습니다. `Example 8` 은 시스템의 새로운 상태를 보여줍니다. 하나의 서비스와 하나의 레플리케이션컨트롤러가 있지만, 이제 모든 다른 파드 인스턴스 세 개가 모두 레플리케이션 컨트롤러에 의해 관리됩니다. 서비스는 모든 요청을 하나의 파드로 보내지 않고 위 예제처럼 파드 모두에게 전송합니다.

> Example 8 - Three instances of a pod managed by the same ReplicationController and exposed through a single service IP and port.

![image](https://user-images.githubusercontent.com/44635266/80271588-7ae61100-86fc-11ea-8960-fa7867c64341.png)

### Examining what nodes your app is running on

어떤 노드에 파드가 스케줄링됐는지 궁금할 수 있습니다. Kubernetes 에는 파드가 적절히 실행하는 데 필요한 CPU 와 메모리를 제공하는 노드에 스케줄링됐다면, 어떤 노드에 파드가 실행중인지는 중요하지 않습니다.

파드가 스케줄링된 노드와 상관없이 컨테이너 내부에 실행 중인 모든 어플리케이션은 동일한 유형의 운영체제 환경을 가집니다. 각 파드는 자체 IP 를 가지고 다른 파드가 같은 노드에 있는지 다른 노드에서 실행 중인지에 상관없이 통신할 수 있습니다. 각 파드는 다른 요청된 만큼의 컴퓨팅 리소스를 제공받습니다. 리소스가 하나의 노드에 제공되는지 다른 노드에서 제공되는지는 중요하지 않습니다.

#### Displaying the pod IP and the pod’s node when listing pods

`kubectl get pods` 명령에 파드가 스케줄링된 노드에 대한 정보가 보이지 않는것을 알 수 있습니다. 중요한 정보가 아니기 때문입니다.

하지만 `-o wide` 옵션을 사용하면 추가 열을 요청할 수 있습니다. 파드를 조회할 때 이 옵션은 파드 IP 와 파드가 실행 중인 노드를 표시합니다.

```shell
$ kubectl get pods -o wide
NAME          READY   STATUS    RESTARTS   AGE   IP         NODE
kubia-hczji   1/1     Running   0          7s    10.1.0.2   gke-kubia-85...
```

#### Inspecting other details of a pod with kubectl describe

아래 예제와 같이 `kubectl describe` 명령을 사용하여 파드의 상세 정보를 보여주므로 노드를 확인할 수 있습니다.

```shell
$ kubectl describe pod kubia-hczji
Name:        kubia-hczji
Namespace:   default
Node:        gke-kubia-85f6-node-vs9f/10.132.0.3        1
Start Time:  Fri, 29 Apr 2016 14:12:33 +0200
Labels:      run=kubia
Status:      Running
IP:          10.1.0.2
Controllers: ReplicationController/kubia
Containers:  ...
Conditions:
  Type       Status
  Ready      True
Volumes: ...
Events: ...
```

파드가 스케줄링된 노드 정보를 포함해 실행된 시간, 실행 중인 이미지와 같은 유용한 정보를 나타냅니다.

### Introducing the Kubernetes dashboard

대시보드에서 파드, 레플리케이션컨트롤러, 서비스 같은 많은 오베즉트를 생성, 수정, 삭제, 조회할 수 있습니다. `Example 9` 에서 확인할 수 있습니다.

> Example 9 - Screenshot of the Kubernetes web-based dashboard

![image](https://user-images.githubusercontent.com/44635266/80271591-846f7900-86fc-11ea-8b8a-ccc142c119a3.png)

#### Accessing the dashboard when running Kubernetes in GKE

GKE 를 사용하는 경우 `kubectl cluster-info` 로 대시보드 URL 을 찾을 수 있습니다.

```shell
$ kubectl cluster-info | grep dashboard
kubernetes-dashboard is running at https://104.155.108.191/api/v1/proxy/
 namespaces/kube-system/services/kubernetes-dashboard
```

이 URL 을 보면 이름과 패스워드를 묻습니다. 다음 명령으로 알아낼 수 있습니다.

```shell
$ gcloud container clusters describe kubia | grep -E "(username|password):"
  password: 32nENgreEJ632A12                                               1
  username: admin                                                          1
```

#### Accessing the dashboard when using Minikube

Minikube 를 사용하면 다음 명령어로 대시보드를 열 수 있습니다.

```shell
$ miminkube dashboard
```
