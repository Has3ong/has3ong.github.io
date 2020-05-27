---
title : Jenkins Pipeline Execution Flow
tags :
- Pipeline
- Jenkins
- DevOps
---

*이 포스트는 [Jenkins 2: Up and Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/jenkins2_upandrunning.pdf)를 바탕으로 작성하였습니다.*

## Triggering Jobs

파이프라인 코드에서 잡을 트리거하는 이벤트를 지정하기 위한 세 가지 방법이 있습니다.

* 파이프라인 잡을 Jenkins 앱에서 작성한다면, 전통적인 방식인 웹 하면의 General 설정 영역에서 지정할 수 있습니다.
* 스크립트 방식 파이프라인을 작성한다면, 속성 블록을 이용해 정의할 수 있습니다.
* 서술적 파이프라인을 작성한다면 `trigger` 명령어를 통해 따른 파이프라인을 트리거할 수 있습니다.

전통적 인터페이스와 스크립트 방식, 서술적 방식에서 트리거 옵션을 알아보겠습니다.

### Build After Other Projects Are Built

이 옵션을 선택하면 하나 이상의 프로젝트를 빌드한 후 다른 프로젝트를 시작할 수 있습니다. 여기서 빌드 실행 결과를 선택 가능합니다.(`stable`, `unstable`, or `failed`)

스크립트 방식의 파이프라인의 경우 `Job1` 이라는 잡이 성공한 이후 파이프라인을 실행하는 문법은 다음과 같습니다.

```groovy
properties([
  pipelineTriggers([
    upstream(
      threshold: hudson.model.Result.SUCCESS,
      upstreamProjects: 'Job1'
    )
  ])
])
```

여러 잡을 나열해야 하는 경우에는 쉼표를 이용합니다. 잡의 브랜치를 명시해야 하는 경우에는 잡 명칭 다음에 슬래시를 추가하고 브랜치 명을 붙입니다.

### Build Periodically

이 방식은 **크론(Cron)** 형태의 기능을 제공해 특정한 시간 간격으로 잡을 실행시킬 수 있게 도와줍니다. 이는 빌드의 한 가지 옵션이기는 하지만 빌드가 소스 코드의 변경 사항에 기반하는 지속적인 통합에는 적합하지 않습니다. 하지만 자원이 충돌하지 않도록 특정 시간 간격으로 잡을 실행하는 상황에는 유용하게 사용할 수 있습니다.

스크립트 방식의 파이프 라인의 문법을 살펴보겠습니다. 이 경우 월요일부터 금요일, 매 오전 9 시에 잡이 실행됩니다.

```groovy
properties([pipelineTriggers([cron('0 9 * * 1-5')])])
```

다음은 서술적 파이프라인의 예시입니다.

```groovy
triggers { cron(0 9 * * 1-5) 
```

위 예시 모두 Jenkins 크론 문법을 활용합니다.

#### Cron Syntax

Jenkins 에 사용되는 크론 문법은 스페이스로 구분된 다섯 가지 속성에 따라 언제 작업을 실행할지 결정하는 방식입니다. 각각의 속성은 다른 단위의 시간을 나타냅니다.

* MINUTES
  * 한 시간 내의 분을 의미한다.(0 - 59)
* HOURS
  * 하루 내의 시간을 의미한다.(0 - 23)
* DAYMONTH
  * 한달 내의 일을 의미한다.(1 - 31)
* MONTH
  * 일 년 내의 월을 의미한다.(1 - 12)
* DAYWEEK
  * 일주일 내의 요일을 의미한다.(0-7), 0 과 7 은 일요일을 의미한다.

또한 `*/<value>` 문법을 사용해 매 `<value>` 를 나타낼 수 있습니다.

추가로 H 기호를 모든 속성에 사용 가능합니다. H 기호는 Jenkins 가 특정 범위 안에서 프로젝트 이름을 해시 값으로 사용해 특정한 값을 뽑아내게 합니다. 이후 이 값을 범위의 가장 낮은 값에 더해 실제로 어떤 시점에 잡이 실행되는지 결정합니다.

H 기호를 사용하는 이유는 같은 크론 값을 가지는 프로젝트가 같은 시간에 시작되지 않게 하기 위해서입니다. 해시 값에서 추출된 차이가 같은 크론 설정을 가진 프로젝트들이 동시에 실행하는것을 막아줍니다.

H 기호를 사용해 동시에 프로젝트가 실행되는 것을 막는 방법을 권장합니다. 여기서 해당 값은 프로젝트 명의 해시 값으로, 프로젝트별로는 값이 다르지만 같은 프로젝트 내에서는 쭉 같은 값으로 유지됩니다.

H 기호에는 범위가 추가돼 값이 해당 범위 안에서 결정되게 설정도 가능합니다.

아래 예시를 확인해보겠습니다.

```
// Start a pipeline execution at 15 minutes past the hour
triggers { cron(15 * * * *) }

// Scan for SCM changes at 20-minute intervals
triggers { pollSCM(*/20 * * * *) }

// Start a pipeline session at some point between
// 0 and 30 minutes after the hour
triggers { cron(H(0,30) * * * *) }

// Start a pipeline execution at 9 a.m. Monday through Friday
triggers { cron(0 9 * * 1-5) }
```

### GitHub Hook Trigger for GitSCM Polling

깃허브를 사용하게 설정된 Jenkins 프로젝트는 **푸시(Push)**, **훅(Hook)** 을 설정하여 Jenkins 프로젝트 빌드를 트리거할 수 있습니다. 이를 설정하면 저장소에 새롭게 푸시된 내용이 생기면 Jenkins 빌드가 시작돼 Jenkins 의 SCM 변경 사항 내려받기 기능을 시작합니다. 따라서 SCM 내려받기 설정이 이 기능을 위해 설정되어야 합니다.

이를 위한 대부분의 초기 작업은 훅을 위한 설정과 Jenkins 프로젝트의 소스 코드 관련 설정입니다. 스크립트 방식의 파이프라인에서 설정하는 문법은 다음과 같습니다.

```groovy
properties([pipelineTriggers([githubPush()])])
```

현재 서술적 파이프라인을 위한 문법은 존재하지 않습니다.

### Poll SCM

SCM 내려받기 기능은 소스 코드 관리 저장소에 변경 사항이 있는지 주기적으로 체크하는 기능입니다. 변경 사항이 발견되면 잡이 변경사항에 관련된 작업을 수행합니다. SCM 의 종류와 내용의 양, 빈도에 따라 많은 시스템 자원을 소모할 수 있습니다.

이를 위해 크론 문법에서 사용된 것과 같은 방법을 사용합니다.

스크립트 방식의 파이프라인 예시는 다음과 같습니다.(매 30 분 변경사항 업데이트)

```groovy
properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
```

서술적 파이프라인으로 작성하겠습니다.

```groovy
triggers { pollSCM(*/30 * * * *) }
```

### Quiet Period

이 값을 이용해 빌드가 트리거되는 시기와 실제 Jenkins 가 이를 실행하는 시기 사이의 **대기 시간(Quiet Period)** 을 정할 수 있습니다. 이는 같은 시간에 시작되는 잡을 지연시키는 상황에서 유용합니다. 값이 입력되지 않으면 전역 설정 값이 사용됩니다.

파이프라인의 빌드 스텝에 `quietPeriod` 설정이 있지만, 이를 수행하는 직접적인 파이프라인 스텝은 존재하지 않습니다. 해당 기능이 필요하다면 Throttle Concurrent Builds 플러그인의 `throttle()` 스텝을 이용해 유사한 기능을 만들 수 있습니다.

### Trigger Builds Remotely

이는 Jenkins 시스템에 있는 잡의 특정 URL 에 접근하여 빌드를 트리거하는 기능입니다. 훅이나 스크립트를 이용해 빌드를 트리거할 때 유용하게 사용할 수 있습니다. 여기서 인증된 토큰이 필요합니다.

Pipelines-as-code 관점에서 멀티브랜치 파이프라인이 Jenkinsfile 의 변경에 의해 실행될 수 있습니다.

빌드가 트리거되면 파이프라인의 특정 스테이지에서 인증이나 로직을 결정하는데 입력값이 필요할 수 있습니다. 파이프라인에서 해당 입력값을 수집하는 방법을 알아보겠습니다.

## User Input

Jenkins 잡의 주요한 기능 중 하나는 사용자 입력값에 따라 동작을 다르게 하는것입니다. Jenkins 에서는 다양한 종류의 값을 수집하기 위해 다양한 변수를 제공합니다. 또한 젠킨스 파이프라인도 이를 지원합니다.

DSL 스텝이 `input` 이 사용자 입력값을 파이프라인으로 전달하는 방식입니다. 이 스텝은 스크립트 방식의 파이프라인에서 일반적인 Jenkins 잡에서 사용하는 것과 같은 종류의 매개 변수를 사용합니다. 서술적 파이프라인에서는 `parameter` 명령어가 있어 같은 내용을 지원합니다.

파이프라인에서 사용하는 스텝과 매개 변수를 살펴보겠습니다.

### input

`input` 스텝을 통해 사용자의 입력을 기다릴 수 있습니다.

```groovy
input 'Continue to next stage?'
```

`input` 스텝은 추가 정보를 위해 필수적이지 않은 매개 변수를 입력받을 수 있습니다. Jenkins 어플리케이션에서 기본 폼은 사용자에게 Proceed 혹은 Abort 선택권을 주는 메세지를 출력합니다. GUI 스테이지 화면에는 `Example 1` 과 같이 생긴 팝업이 나타납니다. 콘솔 결과에서는 실행과 중단을 위한 링크가 나타납니다. `Example 2`

> Example 1 - GUI prompt for input

> Example 2 - Console prompt for input

Proceed 를 선택하면 파이프라인은 계속 실행합니다. Abort 를 선택하면 해당 시점에 파이프라인을 중단하고 상태는 `aborted` 가 됩니다.

여기서 시스템이 `input` 스텝을 실행하면 해당 노드에서 중단되는 것이 매우 중요합니다. 이는 다음 주의에서 설명되는 것처럼 시스템 자원의 독점으로 이어질 수 있습니다.

`input` 스텝은 다음과 같은 매개변수를 사용할 수 있습니다.

* message
  * 사용자에게 표시할 내용입니다. `input ''` 를 통해 빈 값을 나타낼 수 있습니다.
* id
  * `input` 스텝을 자동화하거나 외부의 프로세스에서 찾는 ID 입니다. REST API 콜에 반응할 때와 같은 상황에 사용가능합니다. 지정하지 않으면 유일한 값이 생성됩니다.

예를 들어 `ctns-promt` 와 같이 ID 를 만들 수 있습니다. `input` 스텝은 다음과 같습니다.

```groovy
input id: 'ctns-prompt', message: 'Continue to the next stage?'
```

이제 잡을 실행할 때 이 URL 에 POST 콜을 사용할 수 있습니다. Jenkins 에 이를 입력값 업이 실행하게 하는 URL 은 다음과 같습니다.

```
http://[jenkins-base-url]/job/[job_name]/[build_id]/input/Ctns-prompt/proceedEmpty
```

다음은 멈추는 URL 입니다.

```
http://[jenkins-base-url]/job/[job_name]/[build_id]/input/Ctns-prompt/abort
```

#### URLs And Crumbs

Jenkins 가 보안 설정을 통해 **사이트 간 요청 위조(Cross-Site Request Forgery, CSRF)** 를 막도록 설정됐다면, POST 에 사용되는 URL 에는 CSRF 토큰이 필요합니다.

이를 위한 한 가지 방법은 토큰을 얻기 위한 환경 변수를 지정하는 겁니다.

```
CSRF_TOKEN=
 $(curl -s 'http://<username>:<password
 or token>@<jenkins base
 url>/crumbIssuer/api/xml?xpath=
concat(//crumbRequestField,":",//crumb)')
```

환경 변수를 설정한 후 살펴보면 다음과 같은 것을 확인할 수 있습니다.

```
$ echo $CSRF_TOKEN
Jenkins-Crumb:0cd0babef95a70d0836c3f3e5bc4eea8
```

이후 해당 토큰을 POST 콜에 포함할 수 있습니다. 다음은 `curl` 의 예시입니다.

```
$ curl --user <userid>:<password or token> 
 -H "$CSRF_TOKEN" -X POST 
 -s <jenkins base url>/job/<job name>/<build number>/input/
 <input parameter with 1st letter capped>/proceedEmpty
```

토큰을 포함하지 않으면 403 에러가 나타납니다.

* OK Buttom caption (ok)
  * Proceed 대신 사용할 수 있는 레이블입니다.

```groovy
input message: '<message text>', ok: 'Yes'
```

* Allowed submitter (submitter)
  * 쉼표로 구분된 사용자 아이디 혹은 그룹 이름 목록으로, 인증된 제출자를 정할 때 사용합니다.

```groovy
input message: '<message text>', submitter: 'user1,user2'
```

* Parameter to store the approving submitter (submitterParameter)
  * 해당 스텝을 승인한 제출자 정보를 저장하기 위해 사용되는 변수입니다. 이를 사용하기 위해서는 `input` 스텝의 `response` 를 저장하기 위한 변수를 지정해야 합니다. 다른 매개 변수가 지정되지 않으면 `submitterParameter` 변수에 지정된 이름은 의미를 잃습니다.

`response` 변수에 접근하는 것으로 바로 내용에 접근할 수 있습니다.

```groovy
def resp = input id: 'ctns-prompt', message: 
   'Continue to the next stage?', submitterParameter: 'approver'
   echo "Answered by ${resp}"
```

다른 매개 변수도 있다면 `submitterParameter` 의 이름을 지정해야 접근 가능합니다.

```groovy
 def resp = input id: 'ctns-prompt', message: 
  'Continue to the next stage?', 
  parameters: [string(defaultValue: '', description: '',
  name: 'para1')], submitterParameter: 'approver'
  echo "Answered by " + resp['approver']
```

### Parameters

`input` 문장에서 일반적인 Jenkins 매개 변수를 사용자가 원하는 만큼 추가할 수 있습니다.

매개 변수의 종류에 따라 다른 하위 매개변수도 설명하겠습니다. 하위 매개 변수의 목적이 이름에서 명확히 유추된다면 이는 추가 설명 없이 명칭만 나열할 것입니다.

#### Boolean

true / false 를 위한 기본 매개 변수입니다. 하위 매개 변수는 이름(Name), 기본값(Default Value), 설명(Description) 입니다.

예시는 다음과 같습니다.

```groovy
def answer = input message: '<message>', 
 parameters: [booleanParam(defaultValue: true, 
 description: 'Prerelease setting', name: 'prerelease')]
```

이 결과는 *java.lang.boolean* 을 반환합니다. 

`Example 3` 은 스테이지 화면에서 표현되는 예시입니다.

> Example 3 - Boolean parameter console input

![image](https://user-images.githubusercontent.com/44635266/81054908-a1792880-8f02-11ea-9cff-e8de581bf8cc.png)

콘솔 결과에서는 간단하게 Input 요청 링크가 나타나고 이를 클릭하면 `Example 4` 로 이어집니다.

> Example 4 - Redirect screen for parameter input from console

![image](https://user-images.githubusercontent.com/44635266/81054927-aa69fa00-8f02-11ea-90f8-b7eb3ddfbfdd.png)

#### Choice

이 매개 변수는 사용자가 목록에서 선택하게 합니다. 하위 매개 변수는 이름, 선택지(Choice), 설명입니다. 여기서 Choices 란 사용자에게 보여줄 선택지의 목록입니다. 목록의 첫 번째가 기본값이 됩니다.

이에 대한 예시는 아래와 같습니다.

```groovy
def choice = input message: '<message>', 
 parameters: [choice(choices: "choice1\nchoice2\nchoice3\nchoice4\n",
 description: 'Choose an option', name: 'Options')]
```

여기서 각각의 선택지 `\n` 로 나뉜것을 봐야합니다. 같은 목적을 위한 다른 방법도 있지만, 이 방법이 제일 간단합니다.

파이프라인을 실행하고 프롬프트를 보는 것은 Boolean 예시와 비슷합니다.

#### Credentials 

이 매개변수는 사용할 인증 종류를 선택할 수 있게 합니다. 하위 매개 변수는 이름과 인증 종류(Credential Type), 필수 여부(Required), 기본값, 설명이 있습니다.

인증 종류에는 Any(인증 없음), Username with password(사용자명과 암호), Docker Host Certificate Authentication(도커 호스트 인증서를 이용한 인증), SSH Username with private key(SSH 사용자명과 개인키), Secret File(암호 파일), Secret text(암호 문자열), Certificate(인증서) 가 있습니다.

필수 여부가 명시되면 사용자가 인증 영역을 꼭 작성해야 합니다. 이것이 빌드에서 해당 인증을 이용할 수 있다거나 인증이 통과될 것이라는 의미는 아닙니다. 단지 인증 종류의 선택이 필수라는 뜻입니다.

기본값은 인증 종류에서 기본으로 쓸 값으로 Jenkins 에서 정의된 목록에서 고를 수 있습니다.

SSH 키 인증의 예시는 다음과 같습니다.

```groovy
def creds = input message: '<message>', 
 parameters: [[$class: 'CredentialsParameterDefinition', credentialType: 
 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
 defaultValue: 'jenkins2-ssh', description: 'SSH key for access',
 name: 'SSH', required: true]]
 echo creds
```

이 결과 선택된 인증의 ID 가 출력될 것입니다.

username and password 의 예시는 다음과 같습니다.

```groovy
def creds = input message: '',  parameters: [[$class:
   'CredentialsParameterDefinition', credentialType:
   'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
   defaultValue: '', description: 'Enter username and password',
   name: 'User And Pass', required: true]]
```

여기서 사용자 이름과 비밀번호를 입력하는 창이 나타나지 않는다에 주목해야 합니다. 대신 기존의 인증이나 새로운 인증 선택 화면이 나타납니다. 스테이지 뷰에서 `Example 5` 와 같이 나타납니다.

> Example 5 - Credentials input prompt in Stage View

![image](https://user-images.githubusercontent.com/44635266/81054971-bb1a7000-8f02-11ea-9fde-63bcab59f0d0.png)

Please redirect to approve 링크를 클릭하면 인증을 선택하는 프롬프트로 이동합니다.(`Example 6`) 콘솔에서 나타나는 프롬프트는 이전과 같습니다.

> Example 6 - Credentials prompt

![image](https://user-images.githubusercontent.com/44635266/81054997-c66d9b80-8f02-11ea-89a5-2a537b9a004a.png)

#### File 

`file` 매개변수는 파이프라인에서 사용할 파일을 선택합니다. 하위 매개 변수는 파일 위치와 설명이 있습니다. 문법은 아래와 같습니다.

```groovy
def selectedFile = input message: '<message>', 
 parameters: [file(description: 'Choose file to upload', name: 'local')]
```

이 결과 반환되는 아이템은 `hudson.FilePath` 객체입니다. FilePath 와 관련된 함수들 중 일부는 기본적으로 Jenkins 스크립트를 통해 사용할 수 없거나 관리자를 통해 승인하는 과정을 거쳐야 합니다.

인터페이스는 이전에 설명한 것과 거의 동일하고, 파일을 찾을 수 있는 검색 버튼이 존재하는것만 다릅니다.

#### List Subversion tags

이 매개변수는 빌드를 수행할 때 사용할 서브버전 태그를 명시하는데 사용됩니다. 하위 매개 변수는 이름, 저장소 URL(Repository URL), 인증, 태그 필터(Tag Filter), 보여줄 태그의 최대 개수, 최신 혹은 알파벳 정렬이 있습니다.

저장소 URL 은 보여주기를 원하는 태그가 있는 서브버전 저장소의 URL 입니다. 태그가 없고 하위 폴더가 있다면 이에 접근할 수 있는 화면이 나타납니다.

Jenkins 는 저장소에 접근할 수 있는지 확인 후 필요시 인증 프롬프트를 띄우게 됩니다.

인증 하위 매개 변수는 필요시 저장소에 접근할 수 있는 인증 정보를 포함합니다.

태그 필터는 보여줄 태그를 선택하는 정규 표현식입니다.

기본값은 SVN 변경 사항을 자동으로 내려받는 기능을 사용할 때만 사용합니다.

아래는 예시입니다.

```groovy
def tag = input message: '<message>', 
 parameters: [[$class: 'ListSubversionTagsParameterDefinition',
 credentialsId: 'jenkins2-ssh', defaultValue: '', maxTags: '',
 name: 'LocalSVN', reverseByDate: false, reverseByName: false,
 tagsDir: 'file:///svnrepos/gradle-demo', tagsFilter: 'rel_*']]
```

이 인터페이스는 `file` 이나 Credentials 매개 변수와 유사하게 동작하지만, 파일 선택 화면이 나타나는 이 두 개와 달리 태그의 목록을 선택하는 드롭다운이 나타납니다.

#### Multiline String

이 매개변수는 사용자가 여러 라인의 문자를 입력하게 해줍니다. 하위 매개 변수는 이름과 기본값, 설명이 있습니다.

아래는 예시입니다.

```groovy
def lines = input message: '<message>', 
 parameters: [text(defaultValue: '''line 1
 line 2
 line 3''', description: '', name: 'Input Lines')]
```

여기서 각 명령어가 새 라인에서 시작하는것에 주목해야합니다. 새로운 라인을 포함한 문자가 기본값에 입력됐기 때문입니다. 이 메세지 앞 뒤로 있는 세 개의 따옴표도 중요합니다. 이는 그루비에서 다중 라인의 문자를 입력하기 위해 사용하는 표준입니다.

#### Password

사용자가 비밀번호를 입력할 수 있게 해줍니다. 사용자가 비밀번호를 입력하는 동안 입력한 값은 알아볼 수 없게 표시합니다. 사용 가능한 하위 매개 변수는 이름과 기본값, 설명이 있습니다.

아래는 예시입니다.

```groovy
def pw = input message: '<message>', 
 parameters: [password(defaultValue: '', 
 description: 'Enter your password.', name: 'passwd')] 
```

이를 실행하면 사용자는 입력하는 동안 표시되는 암호 입력창을 보게 됩니다.

#### Run

사용자가 잡에서 특정 런을 선택할 수 있게 해줍니다. 이는 테스트 환경에서 사용할 수 있습니다. 사용 가능한 하위 매개 변수는 이름과 프로젝트, 설명, 필터가 있습니다.

프로젝트 하위 매개 변수는 특정 런을 선택하기 위한 프로젝트입니다. 기본값은 가장 최신에 실행된 런입니다.

필터 하위 매개 변수는 빌드의 상태에 따라 원하지 않는 런을 제외할 수 있게 해줍니다. 선택하는 것은 다음과 같습니다.

* All Builds (including “in-progress” ones)
* Completed Builds
* Successful Builds (this includes stable and unstable ones)
* Stable Builds Only

아래는 예시입니다.

```groovy
def selection = input message: '<message>', 
 parameters: [run(description: 'Choose a run of the project',
 filter: 'ALL', name: 'RUN', projectName: 'pipe1')]
 echo "selection is ${selection}"
```

결과는 다음과 같이 나타납니다.

```groovy
selection is <project name> #<run number>
```

#### String

사용자가 문자를 입력할 수 있게 합니다. 하위 매개 변수는 이름과 기본값, 설명이 있습니다.

다음은 예시입니다.

```groovy
def resp = input message: '<message>', parameters: [string(defaultValue: '',
   description: 'Enter response', name: 'Response')]
```

이를 실행하면 사용자는 문서를 입력할 수 있는 화면을 보게됩니다.

### Return Values from Multiple Input Parameters

위에서 본 예시는 전부 하나의 매개변수만 사용했습니다. 이 문법은 사용자가 입력한 것의 직접적인 반환 값을 돌려줍니다. Proceed 나 Abort 옵션만 가지는 것처럼 매개 변수가 하나도 없다면 반환 값은 null 이 됩니다. 다중 매개 변수를 입력하면 각 매개 변수의 반환 값을 매개 변수의 이름으로 추출할 수 있는 **맵(Map)** 이 반환됩니다.

파이프라인에 전통적인 로그인을 추가한다고 해보겠습니다. 로그인 이름과 비밀번호 두 개의 매개변수를 사용할 것이며, `input` 문장 두 개를 활용해 이를 구현한 후 반환된 맵에서 반환 값을 꺼낼 수 있습니다.

```groovy
 def loginInfo = input message: 'Login',
      parameters: [string(defaultValue: '', description: 
        'Enter Userid:', name: 'userid'),
         password(defaultValue: '',
         description: 'Enter Password:', name: 'passwd')]
       echo "Username = " + loginInfo['userid']
       echo "Password = ${loginInfo['passwd']}"
       echo loginInfo.userid + " " + loginInfo.passwd
```

### Parameters and Declarative Pipelines

`input` 문장에서 로컬 변수를 만들어 반환 값을 담는 것은 서술적 모델에 적용되지 않기 때문에, 서술적 파이프라인에서 어떻게 `input` 문장을 사용하는지 궁금할 것입니다. 여기에 몇 가지 방법이 있는데, 그 중 하나는 서술적 구조를 사용하고, 또 다른 방법은 임시방편입니다.

#### Using the Parameters Section

서술적 파이프라인 구조에서 매개 변수를 선언하는 섹션과 명령어가 있습니다. 이는 메인 파이프라인 클로저의 에이전트 블록에 있습니다. `Example 7` 은 이에 대한 예시입니다.

```groovy
pipeline {
    agent any
    parameters {
        string(name: 'USERID', defaultValue: '', 
         description: 'Enter your userid')
    }
    stages {
        stage('Login') {
            steps {
                echo "Active user is now ${params.USERID}"
            }
        }
    }
}
```

> Example 7 - Declarative Pipeline structure

![image](https://user-images.githubusercontent.com/44635266/81056595-c15e1b80-8f05-11ea-9f49-b96847b6fa4a.png)

Jenkins 어플리케이션 자체에서 작업하고 있다면, 이와 같은 매개 변수를 생성하는 것은 해당 잡의 This build is parameterized 영역을 활성화시킵니다.

이는 서술적 파이프라인에 권장되는 방식입니다.

#### Using The Jenkins Applications To Prameterized the Build

Jenkins 어플리케이션에서 잡을 생성하면, 매개 변수를 추가하는 다른 방법은 간단하게 매개 변수를 필요로 하는 잡을 생성하는 것입니다. 이는 일반 설정 영역에서 This Project is parameterized 체크박스를 선택하고 매개 변수를 일반적인 웹 인터페이스에서 입력하는 방식으로 가능합니다.(`Example 8`)

> Example 8 - Corresponding generation of parameters in Jenkins job

![image](https://user-images.githubusercontent.com/44635266/81056618-c9b65680-8f05-11ea-8163-eacef6d67fc7.png)

그 이후 다음과 같이 코드를 작성하지 않고 간단히 `params.<name of parameter>` 를 통해 이를 참조할 수 있습니다.

```groovy
pipeline {
    agent any
    stages {
        stage('Login') {
            steps {
                echo "Active user is now ${params.USERID}"
            }
        }
    }
}
```

약간 변형한 방식은 파이프라인 블록 전에 매개 변수를 프로퍼티로 정의하는 것입니다. 이는 스크립트 방식과 서술적 방식의 파이프라인에서 모두 사용 가능합니다.

```groovy
properties ([
    parameters ([
        string(defaultValue: '', description: '', name : 'USERID')
    ])
])
pipeline {
    agent any
    stages {
        stage('Login') {
            steps {
                echo "Active user is now ${params.USERID}"
            }
        }
    }
}
```

이는 Jenkins 어플리케이션의 영역 안에 있는 특정한 잡에서만 동작하기 때문에 상용환경에서 사용하는 방법으로 권장되지 않습니다. 또한, 이는 Jenkins 에서 해당 잡에 정의한 기존 설정 값을 덮어 쓰게됩니다.

따라서 특정한 경우에만 사용하는 방식입니다.

#### Using a Script Block

서술적 파이프라인은 계속 기능이 확장되고 있어서, 특정한 경우에 원하는 기능이 지원되지 않거나 구현하기 힘들 수 있습니다. 이 경우를 위해 스크립트 블록을 제공합니다.

Script 블록은 사용자가 서술적이지 않은 방식의 문법을 사용할 수 있게 해줍니다. 서술적 방식에서 할 수 없는 변수 정의와 같은게 여기에 포함됩니다. 이는 스크립트 블록에서 정의된 변수는 스크립트 블록 안에서만 참조 가능하다는 의미입니다. 이를 참조하려 시도할 경우 Jenkins 는 no such property 에러를 표시합니다.

아래는 이를 고려한 예시입니다.

```groovy
stage ('Input') {
           steps {  
              script {
                 def resp = input message: '<message>', 
                  parameters: [string(defaultValue: '',
                  description: 'Enter response 1',
                  name: 'RESPONSE1'), string(defaultValue: '',
                  description: 'Enter response 2', name: 'RESPONSE2')]
                 echo "${resp.RESPONSE1}"
              }
              echo "${resp.RESPONSE2}"
           }
}
```

서술적 파이프라인의 `input` 스텝의 일부로 서언된 두 개의 매개변수가 있습니다. 첫 번째 `echo` 는 변수 `resp` 가 정의된 `script` 블록 안에 있기 때문에 변수에 입력된 값을 출력합니다.

두 번째 `echo` 는 `resp` 가 정의된 밖에 있기 때문에 에러를 표시합니다.

이때문에 `script` 블록을 사용해야 한다면 해당 코드에 대한 접근을 최소화하는 방식이 권장됩니다. `script` 블록 밖에서 변수에 접근해야할 경우 환경 변수에 반환 값을 할당하고 이에 접근해야 합니다.

방식을 적용한 코드는 아래와 같습니다.

```groovy
stage ('Input') {
       steps {  
              script {
                 env.RESP1 = input message: '<message>', parameters: [
                    string(defaultValue: '', description: 'Enter response 1',
                    name: 'RESPONSE1')]
                 env.RESP2 = input message: '<message>', parameters: [
                    string(defaultValue: '', description: 'Enter response 2',
                    name: 'RESPONSE2')]
                 echo "${env.RESP1}"
              }
              echo "${env.RESP2}"
           }
        }
```

여기서 `input` 스텝의 결과를 환경 변수 네임스페이스에 저장했습니다. 이는 전체 환경에 대한 변수이기 때문에 파이프라인 어디서든 접근 가능합니다.

여기서 하나의 `input` 문장을 두 개로 나눈것에 주목해야 합니다. 결과적으로 환경 변수 `RESP1` 과 `RESP2` 가 해당하는 `input` 문장의 결과를 포함합니다. 다중 행 매개 변수를 사용해 이를 환경 변수에 저장할 수 있습니다. 이러한 환경ㄱ 변수의 모양은 다음과 같습니다.

```groovy
<parameter_name>=<input_value>, <parameter_name>=<input_value>, ...
```

이후 원하는 값을 위해 파싱하는 코드를 작성하면 됩니다.

#### Using External Code

또 하나의 방법은 원하는 스크립트를 외부 공유 라이브러리나 그루비 파일에 작성한 후 이를 불러와 실행하는 것입니다. 예를 들어, 다음과 같이 *vars/getuser.groovy* 공유 라이브러리에 입력값을 처리하는 코드를 넣을 수 있습니다.

```groovy
#!/usr/bin/env groovy

def call(String prompt1 = 'Please enter your data', String prompt2 = 'Please enter your data') {
   def resp = input message: '<message>', parameters: [string(defaultValue: '', description: prompt1, name: 'RESPONSE1'), string(defaultValue: '', description: prompt2, name: 'RESPONSE2')]
   echo "${resp.RESPONSE1}"
   echo "${resp.RESPONSE2}"
   // do something with the input
}
```

라이브러리의 이름을 `Utilities` 로 정했다면 다음과 같이 임포트해 호출할 수 있습니다.

```groovy
@Library('Utilities')_
pipeline {
    agent any
    stages {
        stage ('Input') {
           steps {
              getUser 'Enter response 1','Enter response 2'
           }
        }
    }
}
```

`input` 문장을 사용할 때 주의해야 할 점은 예상된 시간 내에 입력되지 않는 상황입니다. 값을 기다리는 동안 노드는 멈추고 반응을 기다립니다. 이러한 상황이 길어지는 것을 방지하려면 `input` 호출을 `timeout` 문장과 같은 명령어로 감싸야 합니다.

## Flow Control Options

Jenkins 에서 pipeline-as-code 를 작성하는 것의 장점 중 하나는 전통적 웹 폼을 사용하는 데 비해 파이프라인에서 흐름을 제어하기 용이하다는 점입니다. 파이프라인이 멈추가너 실패하는 경우도 포함됩니다. 대기 및 재시도 등도 포함됩니다. 여기에는 대기 및 재시도를 다루는 것이 있습니다.

### timeout

`timeout` 스텝은 사용자가 스크립트가 대기할 시간을 지정합니다. 문법은 아래와 같습니다.

```groovy
timeout(time:60, unit: 'SECONDS') { 
  // processing to be timed out inside this block
}
```

시간의 기본 단위는 분입니다. 시간 값만 명시한다면 분으로 간주됩니다. 타임아웃에 도달하면 해당 스텝은 예외를 전달합니다. 여기서 예외가 다른 방식으로 처리되지 않는다면 전체 잡은 멈추게 됩니다.

이를 사용하는 가장 적절한 방식은 파이프라인의 멈춤을 유발할 수 있는 모든 스텝을 `timeout` 으로 감싸는겁니다. 이를 통해 무엇이 잘못되거나 입력이 시간 제한 안에 수행되지 않을 때 파이프라인이 멈추게됩니다. 아래는 예시입니다.

```groovy
node {
    def response
    stage('input') {
       timeout(time:10, unit:'SECONDS') {
          response = input message: 'User', 
           parameters: [string(defaultValue: 'user1', 
           description: 'Enter Userid:', name: 'userid')]
       }
       echo "Username = " + response
    }
}
```

위 예시의 경우 Jenkins 는 10 초 동안 사용자의 입력을 기다립니다. 이 시간이 지나가면 Jenkins 는 예외를 발생시켜 파이프라인을 멈춥니다. `Example 9` 에서 이 결과를 볼 수 있습니다.

> Example 9 - Console output from a timeout

![image](https://user-images.githubusercontent.com/44635266/82109633-75676e00-9772-11ea-9111-850118fce9c7.png)

콘솔 결과에서 보듯이 타임아웃은 `input` 을 기다리던 프로세스를 멈춥니다. 하지만 이 과정에서 예외를 발생시켜 파이프라인을 실패시킵니다. 파이프라인이 실패하지 않게 하려면 다음 코드처럼 `timeout` 을 전통적인 `try-catch` 블록으로 감싸면 됩니다.

여기서 예외 처리 시 `response` 를 원하는 기본값으로 설정했습니다.

```groovy
node {
    def response
    stage('input') {
       try {
         timeout(time:10, unit:'SECONDS') {
            response = input message: 'User', 
             parameters: [string(defaultValue: 'user1',
             description: 'Enter Userid:', name: 'userid')]
         }
       }
       catch (err) {
          response = 'user1'
       }
    }
}
```

### retry

`retry` 클로저는 스텝의 코드를 감싸 해당 코드를 실행할 때 예외를 발생하는 경우 이를 `n` 번 재시도합니다. 여기서 `n` 은 `retry` 스텝에 넘겨주는 값이 됩니다. 문법은 다음과 같이 간단합니다.

```groovy
retry(<n>) { // processing }
```

재시도 제한 횟수에 도달하고 예외가 발생되면 프로세스는 멈춥니다.

### sleep

이 코드는 기본적으로 스텝을 지연시킵니다. 값을 전달받아 해당 프로세스를 수행하기 전 그 시간만큼 지연시킵니다. 기본 시간 단위는 초이고, `sleep time : 5` 는 프로세스를 실행하기 전 5 초를 기다리게 됩니다. 다른 시간 단위를 원한다면 다음과 같이 단위를 매개 변수로 작성하면 됩니다.

```groovy
sleep time: 5, unit: 'MINUTES'
```

### waitUntil

이름에서 추측하듯이 프로세스가 원하는 것이 일어날 때까지 멈추게 합니다. 여기서 원하는 것은 `true` 를 반환하는 클로저입니다.

여기서 해당 블록의 프로세스가 false 를 반환하면 스텝은 좀 더 대기한 후 다시 시도합니다. 프로세스에서 발생한 예외는 스텝을 즉시 중지시키고 에러를 발생시킵니다.

문법은 아래와 같이 간단합니다.

```groovy
waitUntil { // processing that returns true or false }
```

> Example 10 - Example retry run

![image](https://user-images.githubusercontent.com/44635266/82109640-8e701f00-9772-11ea-9e3b-b60e3ee77433.png)

프로세스가 true 를 반환하지 않으면 이 스텝이 무한정 반복될 수 있기 때문에, 해당 스텝을 `timeout` 스텝으로 감싸 처리하는 것을 권장합니다.

다음은 `waitUntil` 블록이 marker 파일이 존재할 때까지 기다리는 예시입니다. 여기서 `timeout` 으로 `waitUntil` 을 감싸 무한정 기다리는 것을 방지했습니다. 또한 쉘 호출의 `returnStatus` 변수를 true 로 설정해 성공과 실패를 결정하게 했습니다.

```groovy
 timeout(time:15, unit:'SECONDS') {
    waitUntil {
       def ret = sh returnStatus: true, 
         script: 'test -e /home/jenkins2/marker.txt'
       return (ret == 0)
    }

 }
```

또 다른 예시로, Docker 컨테이너가 시작돼 파이프라인 테스트의 일환으로 REST API 호출을 통해 데이터를 얻는 과정을 가정해보겠습니다. 이 경우 URL 이 사용가능하지 않다면 예외가 발생할 것입니다.

예외가 발생했을 때 바로 그만두지 않기 위해 `try-catch` 구조를 사용해 예외를 처리해 fasle 를 반환할 수 있습니다. 이를 또한 `timeout` 으로 감싸 파이프라인을 계속 지연시키지 않게 처리 가능합니다.

```groovy
       timeout(time: 120, unit: 'SECONDS') {
          waitUntil {
             try {
                sh "docker exec ${webContainer.id} curl
                   --silent http://127.0.0.1:8080/roar/api/v1/registry 
                   1>test/output/entries.txt"
                return true
             }
             catch (exception) {
                return false
             }
          }
       }
```

같은 기능을 서술적 파이프라인에서 실행하려면 `script` 블록이나 공유 라이브러리를 이용해 구현해야 합니다.

파이프라인에서 각각의 흐름을 제어하는 방법을 알아봤으니, 다음은 여러 파이프라인을 동시에 실행하도록 처리하는 방법을 알아보겠습니다.

## Dealing with Concurrency

대부분 파이프라인 빌드가 **동시성(Concurrency)** 을 갖는 것은 좋은 일입니다. 일반적으로 동시성은 병렬성을 의미하며 비슷한 형태의 잡을 다른 노드에서 동시에 실행할 수 있다는 의미입니다. 자원에 중복 접근하는 것을 적절히 제어한다면 테스트를 수행할 때 유용합니다.

Jenkins 에 동시성을 사용하는 다른 방식은 하나의 잡이나 자원에 여러 빌드가 동시에 수행하는 경우입니다. 이렇게 저장소나 브랜치, 혹은 풀 리퀘스트를 동시에 요청하는 일은 꽤 흔한 일입니다.

하지만 이런 동시 요청이 적합하지 않은 상황도 있습니다. Jenkins 가 이 상황을 다루는 두 가지 방법에 대해 알아보겠습니다.

### Locking Resources with the lock Step

Lockable Resources 플러그인을 설치했다면 다양한 빌드가 같은 자원을 동시에 사용하는 것을 제한하는 `lock` 스텝 DSL 이 존재합니다.

여기서 자원은 느슨한 정의입니다. 노드, 에이전트, 잠금을 위한 이름일 수 있습니다. 지정된 자원이 전역 설정에 정의되어 있지 않다면 자동으로 추가됩니다.

DSL `lock` 스텝은 블로킹 스텝입니다. 즉 이 스텝 안의 클로저가 완료될 때까지 자원을 잠급니다. 간단히 자원의 이름을 기본 매개 변수로 전달할 수 있습니다. 다음은 예시입니다.

```groovy
lock('worker_node1') {
  // steps to do on worker_node1
}
```

다른 방법으로 레이블 명을 적어 해당 레이블을 사용하는 여러 자원을 선택할 수 있고, 수량을 적어 이에 대응하는 레이블 중 특정 개수만 잠글 수 있습니다.

```groovy
lock(label: 'docker-node', quantity: 3) {
    // steps
}
```

*얼마나 많은 자원이 이 작업에 필요할까* 라는 질문으로 생각하면 됩니다. 수량 없이 레이블만 작성하면 해당 레이블을 가진 모든 자원이 잠깁니다.

마지막으로, `inversePrecedence` 라는 옵션이 있습니다. 이를 true 로 설정하면 가장 최신의 빌드가 사용 가능해질 때 자원을 할당받습니다.

간략하게 몇 개의 인스턴스의 파이프라인을 수행하는지에 상관없이 특정 에이전트가 빌드를 실행하게 하는 서술적 파이프라인을 생각해보겠습니다. 코드는 다음과 같이 `lock` 스텝이 포함됩니다.

```groovy
stage('Build') {
   // Run the gradle build
   steps {
      lock('worker_node1') {
         sh 'gradle clean build -x test'
      }
   }
}
```

같은 프로젝트의 실행을 여러 번 수행하거나 자원에 대해 같은 잠금 코드를 가진 프로젝트가 여러 개라면 하나의 빌드만 자원을 갖게 되고 나머지는 기다리게 됩니다.

자원을 할당받은 첫 빌드의 콘솔 로그는 다음과 같습니다.

```shell
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] lock
00:00:02.858 Trying to acquire lock on [worker_node1]
00:00:02.864 Resource [worker_node1] did not exist. Created.
00:00:02.864 Lock acquired on [worker_node1]
[Pipeline] {
[Pipeline] tool
[Pipeline] sh
00:00:02.925 [gradle-demo-simple-pipe] Running shell script
00:00:03.213 + /usr/share/gradle/bin/gradle clean build -x test
00:00:06.671 Starting a Gradle Daemon 
...
00:00:16.887
00:00:16.887 BUILD SUCCESSFUL
00:00:16.887
00:00:16.887 Total time: 13.16 secs
[Pipeline] }
00:00:17.187 Lock released on resource [worker_node1]
[Pipeline] // lock
```

같은 잠금을 가지는 다른 잡의 콘솔 결과는 다음과 같을 것입니다.

```shell
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] lock
00:00:03.262 Trying to acquire lock on [worker_node1]
00:00:03.262 Found 0 available resource(s). Waiting for correct
 amount: 1.
00:00:03.262 [worker_node1] is locked, waiting...
```

잠금을 통해 자원에 대한 접근을 제어할 수 있습니다. 동시성을 다루는 방법은 빌드가 특정 한 단계에 도달하면 이 이상 진행되지 못하게합니다. 이 단계는 마일스톤을 이용해 구성합니다.

### Controlling Concurrent Builds with Milestones

Jenkins 의 특정 시점에 다뤄야 하는것 중 하나는 같은 파이프라인에 대한 빌드가 동시에 진행돼 자원에 대해 경쟁이 생기는 상황입니다. 이 빌드는 순차적으로 실행되며 순서가 꼬이거나 하나의 빌드가 자원을 수정해 이를 적합하지 않은 상태로 만들어 다른 하나가 이를 이용해 수행할 수 있습니다.

간단히 말해 하나의 빌드가 자원을 수정하고 나면 다른 빌드가 이 자원이 아직 진행 중일 때 여기에 접근하지 않는다는 보장이 없습니다.

이렇게 빌드가 순서에 맞지 않게 실행되거나 꼬이는 것을 방지하기 위해 Jenkins 파이프라인은 마일스톤 스텝을 사용할 수 있습니다. `milestone` 스텝을 파이프라인에 작성하면 이는 먼저 시작된 빌드가 여기에 도달하면 후에 시작된 빌드가 이를 넘어서 진행되지 못하게 합니다.

다음은 그레이들 빌드 이후 `milestone` 스텝을 사용한 예시입니다.

```groovy
    sh "'${gradleLoc}/bin/gradle' clean build"
}
milestone label: 'After build', ordinal: 1
stage("NotifyOnFailure") {
```

`Example 11` 처럼 이 빌드에 대해 두 개의 런이 동시에 진행되고 있다고 보겠습니다.

> Example 11 - Two ordered builds of the same job running concurrently

![image](https://user-images.githubusercontent.com/44635266/82109667-c70ff880-9772-11ea-8f0b-cfc1c0e5e4e8.png)

빌드 #11 이 마일스톤에 먼저 도착한다면, 빌드 #10 이 마일스톤에 도달할 시 작업이 취소됩니다. 이를 통해 빌드 #10 이, 빌드 #11 이 사용하거나 수정한 자원을 덮어스는 사태를 방지합니다. `Example 12` 는 빌드 #10 의 콘솔 로그입니다.

> Example 12 - Console log for build #10

![image](https://user-images.githubusercontent.com/44635266/82109670-cc6d4300-9772-11ea-963b-91e4bc2a5970.png)

마일스톤에 대한 규칙을 요약하면 아래와 같습니다.

1. 빌드는 빌드 넘버 순서로 마일스톤을 진행한다.
2. 새 빌드가 마일스톤에 먼저 도달하면 오래된 빌드는 취소된다.
3. 빌드가 마일스톤을 지났을 때 Jenkins 는 이전 마일스톤은 지났으나 현재 마일스톤을 지니지 않은 오래된 빌드를 취소한다.
4. 오래된 빌드가 마일스톤을 지나면 아직 해당 마일스톤을 지나지 않은 새 빌드는 취소되지 않는다.

명확히 하면, 동시에 진행되는 빌드가 시작된 순서대로 마일스톤에 도달하면 모두 마일스톤을 통과할 수 있습니다.

`milestone` 스텝은 여러 개의 매개 변수를 사용할 수 있습니다. 첫 번째는 레이블로, 마일스톤을 구분하기 위해 사용되고 빌드 로그에 나타납니다. 두 번재는 서수로 특별히 지정하지 않으면 자동으로 생성됩니다.

서수를 지정하는 것은 빌드에서 마일스톤을 추가하거나 삭제하는 경우에만 필요합니다.

### Restricting Concurrency in Multibranch Pipelines

파이프라인 DSL 에서 멀티브랜치 파이프라인이 한 시점에 하나의 브랜치만 빌드하게 제약할 수 있습니다. 이는 스크립트 방식이나 서술적 방식 모두에서 가능하며, 속성을 통해 달성됩니다.

이를 설정하면 현재 빌드를 진행 중인 브랜치를 제외한 브랜치의 빌드는 큐에 들어가게 됩니다.

스크립트 방식의 문법에서 속성은 다음과 같이 정의됩니다.

```groovy
properties([disableConcurrentBuilds()])
```

서술적 방식은 다음과 같습니다.

```groovy
options {
    disableConcurrentBuilds()
}
```

### Running Tasks in Parallel

파이프라인 로직의 흐름을 제어하는 다른 명령어 외에도 스텝은 병렬로 실행될 수 있습니다.

실제 파이프라인 DSL 은 이를 위한 특별한 명령어를 가집니다. 전통적인 문법은 스크립트 방식과 서술적 방식 모두 동작하며, 새로운 문법은 서술적 방식에서만 동작합니다. 주요 내용을 설명하기 위해 전통적인 문법 먼저 설명하고 새로운 서술적 문법을 설명합니다.

#### Traditional Parallel Syntax

전통적인 `parallel` 파이프라인 스텝은 맵을 인자로 받습니다. 이 명령어를 위한 맵은 보통 `pipeline` 스텝 자체를 포함하는 클로저입니다. 다른 노드에 대한 스텝을 포함하는 것이 최고의 병렬 실행을 보장합니다. 노드가 명시되지 않으면 Jenkins 는 사용되지 않은 노드에 `parallel` 스텝을 실행합니다.

다음은 병렬 실행을 위한 간단한 스크립트입니다. 이 예시에서 `stepsToRun = [:]` 은 맵을 선언하는 그루비 문법입니다. 이후 루프가 반복되어 `Step<loop counter>` 에 키를 할당하고 각각의 키에 `echo start`, `sleeps`, `echo done` 을 실행하는 노드 블록을 할당합니다. 마지막으로 `parallel` 스텝은 맵을 인자로 받아 실행됩니다.

```groovy
node ('worker_node1') {
   stage("Parallel Demo") {
   // Run steps in parallel

      // The map we'll store the steps in
      def stepsToRun = [:]

      for (int i = 1; i < 5; i++) {
         stepsToRun["Step${i}"] = { node {
            echo "start"
            sleep 5
            echo "done"
         }}
      }
      // Actually run the steps in parallel
      //  parallel takes a map as an argument,
      parallel stepsToRun
   }
}
```

`Example 13` 은 이 영역의 코드가 실행되는 콘솔 결과입니다. 특정 노드를 지정하지 않앗기 대문에, 각 스텝은 가용한 노드 어디에서든 실행됩니다. 결과를 자세히 보면 병렬 실행을 통해 스텝의 순서가 섞이는 것을 확인할 수 있습니다.

> Example 13 - Parallel execution of dynamic steps

![image](https://user-images.githubusercontent.com/44635266/82109681-e870e480-9772-11ea-92eb-e0ee1b69d66d.png)

`parallel` 스텝을 호출할 때 맵을 정의하는 것도 가능합니다. 다음은 맵을 클로저와 노드 형태로 전달하는 방식에 주목합니다. 

이러한 구현 방식에 `master` 와 `worker2` 는 맵의 키가됩니다. 클론 이후 영역은 맵의 값이 됩니다. 맵의 값 부분에서 클로저는 해당 노드에서 실행할 코드입니다. 이 경우 클로저 블록은 그레이들을 호출해 단일 테스트를 수행하는 쉘 스텝이고 각 노드별로 다릅니다.

```groovy
stage ('Test') {
// execute required unit tests in parallel

   parallel (
      master: { node ('master'){
         sh '/opt/gradle-2.7/bin/gradle -D test.single=TestExample1 test'
      }},
      worker2: { node ('worker_node2'){
         sh '/opt/gradle-2.7/bin/gradle -D test.single=TestExample2 test'
      }},
   )
}
```

이 코드를 실행하려 하면 `Example 14` 와 같은 에러가 발생합니다.

> Example 14 - Error trying to run parallel jobs without a workspace

![image](https://user-images.githubusercontent.com/44635266/82109683-edce2f00-9772-11ea-9de5-b0706ee56360.png)

여기에 문제는 원래 빌드가 다른 노드의 워크스페이스에서 진행될 때 새로운 노드가 이 워크스페이스에 접근 권한이 없기 때문에 발생합니다.

이는 아티팩트를 압축하거나 복사하는 방법으로 해결할 수 있습니다. 하지만 Jenkins 는 이를 위한 특별한 스텝을 지원합니다.

#### Stash and Unstash

Jenkins DSL 에서 `stash` 와 `unstash` 는 각각 파이프라인의 노드 및 스테이지 간 파일을 저장하고 불러오는 역할을 합니다. 문법은 다음과 같습니다.

```groovy
stash name: "<name>" [includes: "<pattern>" excludes: "<pattern>"]

unstash "<name>"
```

이 문법은 이름과 패턴으로 포함되거나 제외딜 파일을 명시하는 기본 개념에서 나왔습니다. 여기서 추후 호출을 위해 이름이 주어집니다.

이후 파일을 가져올 필요가 생겼을 때 이름을 전달해 `unstash` 명령어를 호출할 수 있습니다. 다른 스테이지나 노드에서 이를 실행 가능합니다.

`stash` 와 `unstash` 기능은 대용량 파일을 다루는 공식적인 방법으로 설계되지는 않았습니다. 이 경우에 바이너리 저장소를 다루는 아티팩트 저장소인 아티팩토리나 넥서스를 사용하는 것이 낫습니다.

다음은 `stash` 와 `unstash` 를 노드 사이에서 사용하는 예시입니다. 이 경우 소스 코드를 내려받은 후 *build.gradle* 파일과 전체 `src/test` 목록을 `stash` 합니다. 여기에 이름은 `test-sources` 가 됩니다.

이후 다른 노드에 실행되는 `parallel` 영역에, `unstash` 명령어를 통해 이 파일을 해당 노드에 복사합니다. 그 다음 해당 노드에 테스트 파일을 만들어 병렬 실행을 지원합니다.

```groovy
stages {
   
   stage('Source') {
      git branch: 'test', url: 'git@diyv:repos/gradle-greetings'
      stash name: 'test-source', includes: 'build.gradle,src/test/'
   }
  ...
   stage ('Test') {
   // execute required unit tests in parallel

      parallel (
         master: { node ('master') {
            unstash 'test-sources'
            sh '/opt/gradle-2.7/bin/gradle -D test.single=TestExample1 test'
         }},
         worker2: { node ('worker_node2') {
            unstash 'test-sources'
            sh '/opt/gradle-2.7/bin/gradle -D test.single=TestExample2 test'
         }},
      )
   }
}
```

`Example 15` 는 이를 수행한 로그입니다. 여기서 다시 한번 각 노드 간 실행에서 순서가 꼬이는 것을 볼 수 있습니다.

> Example 15 - Parallel run with stash and unstash used to share files across nodes

![image](https://user-images.githubusercontent.com/44635266/82109688-f1fa4c80-9772-11ea-8106-572bd49e2cdf.png)

플러그인을 사용하려면 다음 환경 설정이 필요합니다.

* JUnit 호환 XML 파일
* 테스트를 제외한 목록을 포함한 파일을 다룰 수 있는 도구 사용

#### Alternative Parallel Syntax for Declartive Pipelines

2017 년 9 월 새로운 뭄법이 도입됐습니다. 이 문법은 서술적 파이프라인의 구조적인 형태와 밀접하게 연관됩니다. 또한 맵이나 노드의 설정 없이 바로 병렬 작업을 지원합니다.

새로운 문법은 `parallel` 스텝을 스테이지의 명령어로 격상시켰습니다. 하위에 병렬로 실행될 스테이지 각각을 포함할 수 있습니다. 이 각 블록에서 다른 서술적 파이프라인과 같이 실행할 에이전트와 스텝을 정의할 수 있습니다.

이 문법을 이용한 서술적 파이프라인 스테이지의 예시는 다음과 같습니다.

```groovy
 stage('Unit Test') {
           parallel{
               stage ('Util unit tests') {
                  agent { label 'worker_node2' }
                  steps {
                     cleanWs()
                     unstash 'ws-src'
                     gbuild4 ':util:test'
                  }
                   
               }
               stage ('API unit tests set 1') {
                  agent { label 'worker_node3'}
                  steps {
                     // always run with a new workspace
                     cleanWs()
                     unstash 'ws-src'
                     gbuild4 '-D test.single=TestExample1* :api:test'
                  }
               }
               stage ('API unit tests set 2') {
                   agent { label 'worker_node2' }
                   steps {
                      // always run with a new workspace
                      cleanWs()
                      unstash 'ws-src'
                      gbuild4 '-D test.single=TestExample2* :api:test'
                   }
               }
           }
       }
```

위에서 보듯이 문법은 맵을 사용하는 것보다 더 깨끗하고, 서술적 문법과 유사합니다. 이를 수행하면 각각의 스테이지 정의에 의해 `Example 16` 처럼 하위 스테이지의 결과를 출력합니다. 이는 하나의 세트 결과를 나타내는 전통정ㄱ인 병렬 문법의 결과와 다릅니다. `Example 17`

> Example 16 - Stage output for new parallel syntax

![image](https://user-images.githubusercontent.com/44635266/82109716-2cfc8000-9773-11ea-880d-b6eec896ae7e.png)

> Example 17 - Stage output for traditional parallel syntax

![image](https://user-images.githubusercontent.com/44635266/82109718-34238e00-9773-11ea-8c72-bafd89ae549b.png)

#### Parallel and Failfast

```groovy
pipeline {
    agent any
    stages {
       stage ('Parallel') {
          steps {
             parallel (
                'group1': {
                    timestamps {
                       catchError {
                          sleep 10
                          echo 'Completed group1 processing'
                       }
                    }
                 },
                 'group2': {
                     sleep 5
                     error 'Error in group2 processing'
                 },
                 failFast: true
              )
          }
       }
    }
}
```

이 파이프라인을 실행하면 `Example 18` 과 같은 결과가 나옵니다.

> Example 18 - Running with the failFast option enabled

![image](https://user-images.githubusercontent.com/44635266/82109720-3ab20580-9773-11ea-802a-19eef5d46ce6.png)

결과를 살펴보면 `group1` 에서 5 초가 지난 후 종료된 것을 볼 수 있습니다. 이는 5 초의 슬립 이후 `group2` 가 에러를 발생시켰기 때문입니다. 그 후 `failFast` 옵션이 `group1` 을 종료시켰습니다.

같은 예시에 `failFast` 를 빼거나 false 로 설정하면 `group2` 가 에러와 함께 종료되지만, `group1` 은 10 초의 슬립 이후 완료되는 것을 `Example 19` 에서 볼 수 있습니다.

> Example 19 - Running without the failFast option

![image](https://user-images.githubusercontent.com/44635266/82109724-4271aa00-9773-11ea-8d5d-6ef608721000.png)

병렬로 수행하는 방법을 알아봤으니, 조건에 따라 작업을 수행하는 방법을 알아보겠습니다.

## Conditional Execution

Conditional BuildStep 플러그인으로 사용자가 Jenkins 프리스타일 잡에서 조건부 실행을 할 수 있습니다. 이 플러그인은 특정 조건을 검사하고 이릉 이용해 하나 혹은 여러 개의 빌드 스텝을 수행할 수 있게 합니다.

Jenkins 파이프라인은 비슷한 기능을 제공합니다. 스크립트 방식 파이프라인에서는 Java 나 그루비 언어에 조건문을 사용하는 것과 같이 간단합니다. 다음은 항상 참을 반환하는 `if` 문장을 여러 개 사용한 예시입니다.

```groovy
node ('worker_node1') {
    def responses = null
    stage('selection') {
        responses = input message: 'Enter branch and select build type',
         parameters:[string(defaultValue: '', description: '', 
         name: 'BRANCH_NAME'),choice(choices: 'DEBUG\nRELEASE\nTEST',
          description: '', name: 'BUILD_TYPE')]
    }
    stage('process') {
        if ((responses.BRANCH_NAME == 'master') && 
            (responses.BUILD_TYPE == 'RELEASE')) {
            echo "Kicking off production build\n"
        }
    }
}
```

이 종류의 그루비나 Java 문법은 서술적 방식에 맞지 않아 Jenkins 의 서술적 파이프라인에서는 조건에 따라 코드를 실행할 수 있는 고유의 방식을 제공합니다. 일반적으로 여러 `expression` 블록의 조건을 확인하는 `when` 형태를 사용합니다. 조건이 참이면 스테이지의 나머지 코드가 실행됩니다. 조건이 참이 아니라면 코드는 실행되지 않습니다.

아래는 스크립트 방식에 대응하는 서술적 파이프라인의 예시입니다.

```groovy
pipeline {
   agent any
      parameters {
         string(defaultValue: '',
               description: '',
               name : 'BRANCH_NAME')
        choice (
            choices: 'DEBUG\nRELEASE\nTEST',
            description: '',
            name : 'BUILD_TYPE')
      }
   stages {
      stage('process') {
         when {
            allOf {
               expression {params.BRANCH_NAME == "master"}
               expression {params.BUILD_TYPE == 'RELEASE'}
            }
         }
         steps {
            echo "Kicking off production build\n"
         }
      }
   }
}
```

여기서 `parameter` 영역을 사용해 서술적 파이프라인에 사용하는 매개 변수를 명확하게 정의했습니다. 또한 `when` 과 `allOf` 블록을 조합하여 스크립트 방식 파이프라인의 `if` 와 `&&` 문법을 대체했습니다.

## Post-Processing

웹 기반 Jenkins 잡은 빌드 후처리 동작 영역에서 사용자가 빌드의 상태에 상관없이 빌드 종료 후 동작을 정의할 수 있습니다.

이 기능은 스크립트 방식과 서술적 방식 파이프라인에 모두 사용가능합니다.

### Scripted Pipelines Post-Processing

스크립트 방식의 파이프라인에는 빌드 후 처리를 위한 내장 명령어가 존재하지 않습니다. 따라서 그루비 문법을 통해 이를 구성합니다. 이 경우 `try-catch-finally` 를 이용합니다.

Jenkins 에선 `catchError` 명령어가 있습니다.

#### try-catch-finally

어떤 예외도 `try-catch` 를 통해 잡아내 `finally` 영역에서 빌드의 결과에 따라 원하는 작업을 진행하므로 구현 가능합니다.

일반적으로, `finally` 블록에서 하는 작업은 메일을 보내거나 빌드의 상태를 알림으로 보냅니다. 다음은 `try-catch-finally` 구조 예시입니다.

```groovy
def err = null
try {
   // pipeline code
   node ('node-name') {
      stage ('first stage') {
         ...
      } // end of last stage
   }
} 
catch (err) { 
   currentBuild.result = "FAILURE"
} 
finally {
   (currentBuild.result != "ABORTED"){
       // Send email notifications for builds that failed 
       //  or are unstable
   }
}
```

여기서 에러가 발생한 경우 `currentBuild.result` 에 값을 할당해 빌드의 결과를 Jenkins 와 일치시킵니다. 빌드가 취소되면 메일을 보내지 않습니다.

`try-catch` 블록은 원한다면 노드 블록에서도 사용 가능합니다. 하지만 이는 노드를 할당할 때 발생하는 에러를 잡을 수 없기 때문에 알림을 보내지 못할 수 있습니다. 마지막으로 에러를 상위로 전달하고 싶으면 `finally` 블록에서 에러를 발생시키면 됩니다.

#### catchError

Jenkins 파이프라인 문법은 예외를 처리하는 방식을 제공합니다. `catchError` 블록은 예외를 탐지하고 전체 빌드의 상태를 바꾸면서 프로세스는 계속 진행시킵니다.

`catchError` 문법을 사용해 특정 블록의 코드에서 예외가 발생하면 빌드의 결과를 실패로 만들 수 있습니다. 하지만 `catchError` 블록 이후 파이프라인의 코드는 계속 실행합니다.

이 방식의 장점은 작업이 실패하더라도 알림을 보내는 작업이 가능합니다. 이 방식으로 Jenkins 빌드 후처리를 구현하고, `try-catch` 를 더 짧게 구현할 수 있습니다.

아래는 예시입니다.

```groovy
node ('node-name') {
   catchError {
      stage ('first stage') {
         ...
      } // end of last stage
   }
   // step to send email notifications 
}
```

위와 동일한 코드는 아래와 같습니다.

```groovy
node ('node-name') {
    try {
       stage ('first stage') {
         ...
       } // end of last stage
    } catch (err) {
       echo "Caught: ${err}"
       currentBuild.result = 'FAILURE'
    }
    // step to send email notifications 
}
```

### Declarative Pipelines and Post-Processing

서술적 파이프라인은 빌드 후처리를 위한 기능을 가집니다. 이 섹션의 이름은 `post` 입니다.

이를 활용하는 가장 일반적인 방식은 알림과 같은 빌드 후처리를 구현하는 것입니다. 서술적 문법은 몇 가지 미리 정의된 빌드 조건을 제공하고, 이를 이용해 이후 작업을 결정할 수 있습니다. 빌드 조건의 이름과 설명은 아래 표예 있습니다.

|Condition|Description|
|`always`|해당 블록의 스텝을 항상 실행|
|`changed`|해당 블록의 스텝을 혀재 빌드의 결과가 이전 결과와 다를 때만 실행|
|`success`|해당 블록의 스텝을 현재 빌드가 성공했을 경우에만 실행|
|`failure`|해당 블록의 스텝을 현재 빌드가 실패했을 경우에만 실행|
|`unstable`|해당 블록의 스텝을 현재 빌드의 상태가 `unstable` 때만 실행|

예를 들어, `failure` 조건이 참일 때 실패 메일을 보내도록 정의할 수 있습니다.

아래는 빌드의 마지막 부분이 간단한 `post` 구조입니다.

```groovy
      }
    } // end stages
    post {
       always {
          echo "Build stage complete"
       }
       failure {
          echo "Build failed"
          mail body: 'build failed', subject: 'Build failed!',
             to: 'devops@company.com'
        }
        success {
          echo "Build succeeded"
          mail body: 'build succeeded', subject: 'Build Succeeded',
             to: 'devops@company.com'
        }
    }
} // end pipeline
```

