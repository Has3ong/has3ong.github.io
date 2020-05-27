---
title : Jenkins Notifications and Reports
tags :
- Report
- Alarm
- Notification
- Jenkins
- DevOps
---

*이 포스트는 [Jenkins 2: Up and Running](http://docsresearch.com/research/Files/ReadingMaterial/Books/Technology/Misc/jenkins2_upandrunning.pdf)를 바탕으로 작성하였습니다.*

Jenkins 사용하는 가장 일반적인 목적 중 하나는 자동화입니다. 특정 이벤트에 트리거된 프로세스를 실행시키는것 외에도 프로세스가 끝났을 때 해당 작업의 상태에 대해 자도오하된 알림을 받는 것이 중요합니다. 또한 여러 플러그인과 스텝을 통해 유용한 리포트를 받을 수 있습니다.

Jenkins 가 보낼 수 있는 알림을 알아보고, 그리고 Slack 과 HipChat 을 연동해보겠습니다.

## Notifications

스크립트 방식 파이프라인에서는 `try-catch-finally` 문법을 통해 항상 실행돼야 할 후처리를 구현합니다. 서술적 파이프라인에서는 좀 더 직관적인 `post` 섹션을 사용할 수 있습니다.

이메일을 통해 알림을 받는 전통적인 방식과 달리 다양한 방식을 통해 알림을 받을 수 있습니다. 알림은 인스턴스 메세지인 경우가 많고, 사용자는 인스턴스 메세지 색상을 바꾸는 등 다양한 작업을 할 수 있습니다.

### Email

전통적 Jenkins 에 이메일은 알림의 기본 방식입니다. 따라서 메일 알림을 설정하는 것은 상당히 쉽고 다양한 방법이 지원됩니다. 옵션은 Jenkins 관리의 시스템 설정 페이지에서 설정할 수 있습니다.

#### Jenkins Location

이번 절에서 알아볼 URL 외에도 시스템 관리자의 이메일을 설정할 수 있는 장소가 있습니다. 이는 Jenkins 가 프로젝트에 관련된 사람에게 메일을 보낼 때 보낸 사람 주소에 나타날 이름입니다. `Example 1` 의 도움 화면에 나오는 것처럼, 간단한 이메일이나 Jenkins 인스턴스의 이름뿐만 아니라 이메일 주소가 모두 가능합니다.

이 부분은 필수 입력 영역입니다.

> Example 1 - Jenkins Location settings

![image](https://user-images.githubusercontent.com/44635266/82110558-405f1980-977a-11ea-8e59-e2c830a436ef.png)

실제로 대부분의 경우 사용자 이메일 주소는 이후 설정하는 주소입니다. 대부분 이메일의 헤더를 분석하지 않는 이상 관리자 주소를 볼 일은 없습니다. 이를 살펴보는 방법을 알아보겠습니다.

X-Google-Original-From 헤더의 System Admin e-mail address 필드의 값은 아래와 같습니다.

```
X-Received: by 10.55.93.197 with SMTP id r188mr35950021qkb.277.1502803051345;
 Tue, 15 Aug 2017 06:17:31 -0700 (PDT)
Received: from diyvb2 (sas08001.nat.sas.com. [149.173.8.1])
 by smtp.gmail.com with ESMTPSA id 131sm6301940qki.23.2017.08.15.06.17.30
 for <bcl@nclasters.org >
 (version=TLS1 cipher=ECDHE-RSA-AES128-SHA bits=128/128);
 Tue, 15 Aug 2017 06:17:30 -0700 (PDT)
From: jenkins-demo@gmail.com
X-Google-Original-From: jenkins-notifications@myserver.com
Date: Tue, 15 Aug 2017 09:17:30 -0400 (EDT)
Reply-To: no-reply@jenkins.foo
To: bcl@nclasters.org
Message-ID: <2007092803.5.1502803050373.JavaMail.jenkins@diyvb2>
Subject: Test email #6
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 7bit
```

이메일 알림 설정해보겠습니다.

#### Email Notification

전역 환경 설정 페이지에 E-Mail Notification 영역을 통해 기본 이메일 기능을 설정할 수 있습니다. 이 필드는 이름 자체가 내포하듯 이메일의 기본 정보를 설정하는 장소입니다. 여기서 오른쪽 Advanced 버튼을 누르면 추가 필드를 나타납니다.

> Example 2 - E-mail Notification settings

![image](https://user-images.githubusercontent.com/44635266/82110561-48b75480-977a-11ea-827d-620a71b08a0e.png)

이제 Jenkins 에서 이메일 알림을 설정하는 법을 알아보겠습니다.

주의할 점은 아래와 같습니다.

* SMTP Server 는 빈 값으로 남겨둘 시 localhost 가 된다.
* SSL 을 사용하면 포트의 기본값은 465 가 된다. 사용하지 않으면 25 가 된다.
* Reply-To-Address 필드는 필드가 아니지만 설정할 필요가 있을 때 꽤 유용하다.

> Example 3 - Traceback for failure sending test email

![image](https://user-images.githubusercontent.com/44635266/82111149-fd9f4080-977d-11ea-93e5-b40be68facb7.png)

이를 파이프라인 스크립트에서 사용해 보겠습니다.

#### Sending Email in Pipelines

```groovy
node ('worker_node1') {
  try {
      ...
    }
    currentBuild.result = 'SUCCESS'
  }
  catch (err) {
    currentBuild.result = 'FAILURE'
  }
  finally {
    mail to: 'bcl@nclasters.org',
      subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
      body: "${env.BUILD_URL} has result ${currentBuild.result}"
  }
}
```

비슷한 방식으로 다음과 같이 `mail` 스텝을 서술적 파이프라인에서 설정할 수 있습니다.

```groovy
pipeline {
  agent any
  stages {
   ...
  }
  post {
    always {
       mail to: 'bcl@nclasters.org',
          subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
          body: "${env.BUILD_URL} has result ${currentBuild.result}"
    }
  }
}
```

이 파이프라인은 빌드가 실패할 경우 다음과 같은 메일을 생성합니다.

```shell
---------------------------- Original Message ----------------------------
Subject: Status of pipeline: pipeline2 #1
From:    jenkins-demo@gmail.com
Date:    Tue, August 15, 2017 9:33 pm
To:      bcl@nclasters.org
--------------------------------------------------------------------------

http://jenkins1.demo.org/job/pipeline2/1/ has result FAILURE
```

빌드가 성공할 경우 `FAILURE` 가 `SUCCESS` 로 바뀌고 나머지 부분은 동일합니다.

#### Extended Email Notification

기본 메일 기능 외에도 email-ext 플러그인이 있습니다. 이를 통해 Jenkins 에서 이메일을 보내는 기능을 다양하게 설정할 수 있습니다. 기본 메일 플러그인과 유사한 기본 설정이 있지만 아래 세 영역에 새로운 기능이 추가됩니다.

* Content
  * 메일 알림의 제목과 내용을 동적으로 바꿀 수 있다.
* Recipients
  * 사용자 역할에 따라 수신자를 설정할 수 있다.
* Triggers
  * 메일 알림을 보내는 조건을 설정할 수 있다.

각 기능을 자세히 살펴보고 유용하게 사용할 수 있는 장소를 알아보겠습니다.

**Global configuration**

email-ext 플러그인은 파이프라인 잡에서 사용하기 전에 전역 환경 설정을 해야 합니다. 이중 대부분은 기본 이메일 기능의 설정과 유사합니다.(`Example 4`)

> Example 4 - General configuration for extended emails

![image](https://user-images.githubusercontent.com/44635266/82111150-05f77b80-977e-11ea-84d6-696a0d1cabc2.png)

여기서 몇몇 필드는 부연 설명이 필요합니다. 이를 알아보겠습니다.

* User List-ID Email Header
  * 이 옵션을 선택하면 이메일에 list-id 헤더를 추가할 수 있습니다. 도움말이 암시하듯 필터링이나 자동 답장을 피하는 데 유용합니다. 도움말에 예시 포맷이 있습니다.
* Add 'Precedence: bulk'Email Header
  * 이 옵션을 선택하면 메일에 헤더가 추가됩니다. 메일 시스템에서 사용되는 기본값에 따라 Jenkins 에 자동으로 보내지는 답장을 제거합니다.
* Reply To List
  * 새로운 옵션은 아니지만, 콤마로 구분되는 사용자 목록을 입력할 수 있습니다.
* Emergency Reroute
  * 이 필드를 작성하면 모든 Jenkins 메일은 이곳에 작성된 주소로만 보내집니다. 이를 통해 특정 이슈가 있을 때 임시적으로 Jenkins 가 원래 주소로 메일을 보내지 않게 할 수 있습니다.
* Excluded Recipients
  * 이 플러그인에서 생성된 수신 주소에 특정 주소를 제외하기 위해 사용됩니다.

아래 `email-ext` 플러그인으로 메일 내용을 작성해 보겠습니다.

**Content**

전역 환경 설정 페이지에서 Jenkins 가 이메일 알림에서 보낸 메일의 내용을 동적으로 작성하거나 수정할 수 있게 도와주는 필드가 있습니다. `Example 5` 는 이에 관련된 필드입니다.

> Example 5 - Default global content settings for extended email

![image](https://user-images.githubusercontent.com/44635266/82111157-160f5b00-977e-11ea-93d2-4355c299af8f.png)

처음 세 필드는 그 자체로 이해하기 충분합니다. 여기서 첨부 파일 사이즈는 MB 단위고, 전체 첨부 파일의 용량을 제한합니다.

기본 선처리 스크립트와 기본 후처리 스크립트는 이메일이 발송되기 전과 후에 실행할 그루비 스크립트를 위한 장소다. 이에 관심이 있다면 웹에 유용한 사용법을 찾을 수 있습니다.

기본 제목과 기본 내용 필드를 구성하기 위해 여러 토큰을 사용할 수 있습니다. 여기서 `token` 이란 해당 빌드에서 Jenkins 에 의해 채워지는 환경 변수 입니다. `$BUILD_NUMBER` 에는 빌드 번호, `$PROJECT_NAME` 이라는 프로젝트 이름이 포함돼 있습니다.

정의되어 있다면 선처리와 후처리 스크립트는 다른 잡에서 `${DEFAULT_PRESEND_SCRIPT}` 와 `${DEFAULT_POSTSEND_SCRIPT}` 를 이용해 참조할 수 있습니다.

메일의 내용에 다양한 옵션을 제공하는 것 외에도 extended email 은 메일을 받을 수신자의 종류를 선택할 수 있게 합니다.

**Recipients**

Email EXtension 플러그인을 사용하면 `examilext` 파이프라인 스텝을 통해 수신자의 종류를 선택할 수 있습니다. 이는 설정된 수신자에 추가로 더해집니다.

`Example 6` 은 해당 스텝의 드롭다운에서 선택 가능한 목록입니다.

> Example 6 - Adding extended email recipients

아래 표는 플러그인 페이지를 참조하여 작성한 해당 목록과 정의입니다.

|Name|Description|
|:--|:--|
|Culprits|마지막 성공한 빌드와 지금 빌드 사이에 변경 사항을 커밋한 사용자에게 메일 발송, 최소 지금 빌드의 변경 사항을 만든 사람이 포함되고, 직전 빌드가 실패했다면 직전 빌드의 culprit 목록도 포함|
|Developers|변경 사항을 작성한 사람에게 메일 발송|
|Requestor|빌드가 수동으로 시작됐다 가정하고 해당 빌드를 시작한 사람에게 메일 발송|
|Suspects Causing Unit Tests to Begin Failing|단위 테스트를 실패하게 만들었다고 추정되는 사용자에게 메일 발송, 해당 목록에는 단위 테스트가 실패한 빌드의 committer 와 requestor, 그리고 테스트가 실패하기 전 실패한 빌드를 포함|
|Suspects Causing the Build to Begin Failing|이 빌드를 실패하게 만들었다고 추정되는 사용자에게 메일 발송|
|Upstream Committers|이 빌드를 트리거한 상위 빌드 커밋 작성자에게 메일 발송|

`emailext` 파이프라인 스텝을 사용하려면 `$class` 를 사용해 위 범주를 참조하면 됩니다.

```groovy
emailext body: 'body goes here',
 recipientProviders: [[$class: 'CulpritsRecipientProvider'],
 [$class: 'DevelopersRecipientProvider'],
 [$class: 'RequesterRecipientProvider'], 
 [$class: 'FailingTestSuspectsRecipientProvider'],
 [$class: 'FirstFailingBuildSuspectsRecipientProvider'],
 [$class: 'UpstreamComitterRecipientProvider']],
 subject: 'subject goes here
```

**Trigger**

`email-ext` 플러그인을 위한 전역 설정에서 메일을 보낼 이벤트의 기본 트리거를 설정할 수 있습니다. 하지만 이 설정은 프리스타일 잡을 사용하고 빌드 후처리 작업에 수정 가능한 이메일 알림을 추가해야만 동작합니다. 즉 파이프라인에는 유용하지 않습니다.

파이프라인에서 두 가지 방법으로 접근할 수 있습니다. 스크립트 방식에서는 `finally` 블록에서 빌드 상태를 확인하는 방법으로 접근할 수 있고, 서술적 파이프라인에서는 `post` 블록에서 조건을 통해 이메일을 보낼 수 있습니다.

**Including logs**

`email-ext` 플러그인의 유용한 내장 기능 중 하나는 로그를 포함할 수 있다는 것입니다. 이를 pipeline 스텝에서 사용하려면 다음과 같이 옵션을 활성화합니다.

```groovy
attachLog: true, compressLog:true
```

궁극적으로 이 플러그인은 파이프라인 개발자에게 다양한 방식을 제공합니다. 좋은 점은 다양한 종류의 수신자를 추가하고 로그를 추가하는 것입니다. 반면에 `emailext` 스텝은 전역 환경 설정에 기반해 동작하도록 설정되고 프리스타일 잡에 빌드 후처리를 추가하게 설계됐습니다. 이는 파이프라인 환경에 잘 맞지 않아 빌드 후처리에 해당하는 코드를 작성하지 않으면 기본 기능이 활성화됩니다.

또 다른 점은 `emailext` 파이프라인 스텝인 pre-send 와 post-send 스크립트가 동작하지 않는다는 점입니다. 두 스크립트가 접근 권한을 가져야 할 `build` 객체 등이 접근 불가능합니다.

다음은 위 내용을 참고해 유용한 내용을 추가한 `emailext` 파이프라인 스텝의 최종 예시입니다.

```groovy
emailext attachLog: true, body:
   """<p>EXECUTED: Job <b>\'${env.JOB_NAME}:${env.BUILD_NUMBER})\'
   </b></p><p>View console output at "<a href="${env.BUILD_URL}"> 
   ${env.JOB_NAME}:${env.BUILD_NUMBER}</a>"</p> 
     <p><i>(Build log is attached.)</i></p>""", 
    compressLog: true,
    recipientProviders: [[$class: 'DevelopersRecipientProvider'], 
     [$class: 'RequesterRecipientProvider']],
    replyTo: 'do-not-reply@company.com', 
    subject: "Status: ${currentBuild.result?:'SUCCESS'} - 
    Job \'${env.JOB_NAME}:${env.BUILD_NUMBER}\'", 
    to: 'bcl@nclasters.org Brent.Laster@domain.com'
```

`emailext` 스텝에 주요 내용은 다음과 같습니다.

* 이 스텝은 페이지의 제한에 의해 줄바꿈 처리가 됐다.
* 스크립트 방식의 파이프라인을 작성할 때는 긴 값을 저장할 수 있는 변수를 선언해 스텝에서 사용하는 것이 좋습니다.
* `"""` 가 문자열을 감싸는 것을 볼 수 있는데, 다중 라인 메세지를 표현하기 위한 그루비 문법이다.
* 이메일 바디에서 HTML 태그를 사용했다. 이메일을 HTML 형태로 나타내려면 Global configuration 에 `email-ext` 플러그인의 기본 컨텐트 타입이 `text` 가 아닌 HTML 로 설정돼야 한다.
* 문자열을 감싸는 `""` 는 문자열 안에 변수가 있는 경우 사용하는 그루비 문법이다.
* `${currentBuild.result?:'SUCCESS'}` 문법은 `currentBuild.result` 이 NULL 인지 확인하고, 이 경우 SUCCESS 값을 할당한다. 이는 Jenkins 에서 NULL 이 빌드 성공을 의미하기에 필요합니다.
* `replyTo` 필드를 사용해 답신할 주소를 지정했다.
* 스페이스를 사용해 여러 사용자 주소를 나타낼 수 있다.

`Example 7` 은 위 명령어를 통해 생성된 이메일이다.

> Example 7 - Example email from sample command

![image](https://user-images.githubusercontent.com/44635266/82143320-fa8b7980-987d-11ea-9550-7379cbff960d.png)

Jenkins 사용자에게 이벤트와 정보를 알리는 방법 중 이메일이 가장 보편적이지만, 점점 더 많은 팀이 알림을 활용하기 위해 인스턴스 메세지를 사용하고 있습니다. 이 중 가장 유명한 것이 슬랙과 힙챗입니다.

### Collaboration Services

유명한 메세지 및 협업 서비스에 Jenkins 알림을 보낼 수 있는 플러그인 중 슬랙과 힙챗에 대해 알아보겠습니다.

#### Slack Notification

슬랙으로 알림을 보내기 위해선 Slack Notification 플러그인을 설치해야 합니다.

설치 및 전역 환경 설정 이후 slackSend 스텝을 통해 파이프라인에서 슬랙 채널에 알림을 보낼 수 있습니다. 하지만 슬랙을 통한 통합 설정할 수 있어야 합니다.

**Setup in Slack**

Jenkins 와 슬랙의 연동을 위해 먼저 슬랙 계정과 팀, 채널이 있다 가정하겠습니다. 예제로 explore-jenkins 팀과 #jenkins2 채널을 슬랙에 만들었습니다.

다음으로 Jenkins 통합 설정하겠습니다.

`Example 8` 은 설정의 첫 화면입니다. 여기서 explore-jenkins 팀에 로그인하여 해당 팀의 #jenkins2 채널과 Jenkins CI 와의 통합을 활성화 시킵니다.

> Example 8 - Enabling the Jenkins Slack integration on a channel

![image](https://user-images.githubusercontent.com/44635266/82143393-9ddc8e80-987e-11ea-8f03-268f5a4bc57f.png)

Add Jenkins CI integration 버튼을 클릭하면 통합을 위해 Jenkins 에서 해야 할 내용을 알려주는 화면으로 이동할 것입니다. 아래는 Jenkins 통합을 위해 사용할 설정을 다룹니다.

먼저 설정해야 할 것은 기본 URL 과 토큰입니다. 이 둘은 `Example 9` 에서 보여지듯이 Step 3 의 결과에 나타납니다. 원하는 설정을 수정한 후 Save Settings 버튼을 페이지 하단에서 클릭하겠습니다. 그러면 설정은 저장 곤간만 같은 페이지에 머물게 될 것입니다.

> Example 9 - Information from Slack integration page with info needed for Jenkins config

![image](https://user-images.githubusercontent.com/44635266/82143395-a92fba00-987e-11ea-825b-d7f5931850cb.png)

다음은 보안 관련 문제를 고려하면 좋습니다. Jenkins 전역 환경 설정 페이지에서 토큰을 볼 수 있지만, 보안 위협이 존재합니다. 여기서 Secret text 인증을 만들어 보관하는게 좋습니다. `Example 10` 은 새로운 인증을 만드는 스텝입니다.

> Example 10 - Creating a new “Secret text” credential for Slack

![image](https://user-images.githubusercontent.com/44635266/82143398-adf46e00-987e-11ea-9479-3492e483ff57.png)

다음은 전역 환경 설정에서 사용할 인증이 이미 만들어졋다고 가정하겠습니다.

**Global configuration in Jenkins**

슬랙 알림을 위한 전역 환경 설정 화면은 `Example 11` 과 같습니다.

> Example 11 - Global configuration for the Jenkins/Slack notifications

![image](https://user-images.githubusercontent.com/44635266/82143402-b64ca900-987e-11ea-9bc2-a34f7d7c2ec5.png)

가장 중요한 것은 URL 입니다. 

다음으로 중요한 것이 subdomain 입니다. 이는 슬랙에서 사용할 팀으로 토큰을 설정한 것과 같이 설정할 수 있습니다. 채널도 이와 같이 설정 가능합니다.

슬랩 통합 토큰을 새로 생성하는 것이 토큰 자체를 노출하는 것보다 좋습니다. Integration Token Credential ID 필드는 이전에 생성한 토큰을 포함한 인증을 선택할 수 있는 장소입니다. 이 옵션을 사용하면 Integration Token 은 공백으로 바꿉니다.

마지막으로, Is Bot User? 체크박스가 있습니다. 체크하면 봇 사용자로부터 알림을 보내는 것이 활성화 됩니다. 동작하게 하려면 봇 사용자를 위한 인증이 필요합니다.

이제 연결 테스트 버튼을 통해 테스트할 수 있습니다. 제대로 설정이 됐다면 성공 메세지를 볼 수 있고, 슬랙에서 알림을 확인할 수 있습니다.

> Example 12 - Notifications of Slack integration setup

![image](https://user-images.githubusercontent.com/44635266/82143411-c2d10180-987e-11ea-97f9-0476a13f75dd.png)

**Webhooks in Slack**

통합을 위한 API 토큰의 설정이 쉽지만, 이 외에도 사용할 수 있는 방법이 있는데 이는 **웹훅(Webhook)** 입니다. 웹훅은 Jenkins 와 슬랙의 연동을 위한 방법으로 슬랙이 공유할 것이 생겼을 때 Jenkins 에 정의된 public endpoint 에 페이로드를 보내는 방법입니다.

Jenkins CI 통합처럼 슬랙의 subdomain 과 팀의 웹훅 통합부터 활성화해야 합니다. 여기서 incoming 웹훅이 아니라 outgoing 웹훅을 설정해야 합니다. `Example 13` 은 outgoing 웹훅 통합을 슬랙에서 활성화하는 화면입니다.

> Example 13 - Enabling the outgoing webhook integration in Slack

![image](https://user-images.githubusercontent.com/44635266/82143414-cbc1d300-987e-11ea-983c-9d1b096bb94d.png)

Add Outgoing WebHooks Integration 버튼 클릭 후 새로운 통합에 토큰을 포함시키면 추가 정보가 있는 화면으로 이동할 것입니다.

> Example 14 - Outgoing webhook integration details—including token

![image](https://user-images.githubusercontent.com/44635266/82143428-e6944780-987e-11ea-9de3-1dc13af0413a.png)

이후 슬랙 웹훅을 위해 토큰과 엔드포인트가 포함된 전역 환경 설정을 진행할 수 있습니다(`Example 15`).

> Example 15 - Setting global configuration in Jenkins for Slack webhooks

![image](https://user-images.githubusercontent.com/44635266/82143439-f4e26380-987e-11ea-9988-941a4d685215.png)

**Sending Slack notifications in a job**

slackSend 파이프라인 스텝을 통해 슬랙으로 메세지를 보낼 수 있습니다. 여기서 필수 매개변수는 보낼 메세지입니다. 어떤 메세지를 보내도 상관 없는데 `env.JOB_NAME`, `env.BUILD_NUM` 같은 Jenkins 의 환경 변수나 전역 변수도 보내고 싶을 것입니다.

이를 사용할 경우 `""` 로 감싸진 문자열 안에서 `${}` 문법을 사용해 이를 감싸 그루비 문법을 충족시켜야 합니다. 다음은 기본 매개변수만 가진 간략한 예시입니다.

```groovy
slackSend  "Build ${env.BUILD_NUMBER} completed for ${env.JOB_NAME}."
```

그 외에 사용할 만한 매개변수로는 `color` 가 있습니다. `color` 는 메세지 첨부 파일의 왼쪽과 보더의 색상 설정을 위해 사용합니다.

색상은 이미 정의된 레이블이나 헥스 값으로 설정할 수 있습니다. good, warning, danger 가 있습니다.

색상과 링크를 추가한 샘플은 다음과 같습니다.

```groovy
slackSend color: 'good', message: "Build ${env.BUILD_NUMBER}
 completed for  ${env.JOB_NAME}.  Details: (<${env.BUILD_URL} |
 here >)"
```

여기서 변수가 같이 있는 메세지는 큰따옴표로 감싸야 실제 값이 변수에 할당합니다.

slackSend 스텝이 받을 수 있는 추가 매개 변수가 있습니다. 추가 매개 변수의 이름과 타입은 대부분 슬랙 통합을 위한 전역 환경 변수와 같습니다. 이는 필요시 기본 설정을 덮어쓸 수 있게 하려는 것입니다. 파이프라인 문법 화면으로 이동해 slackSend 스텝을 선택 후 Advanced 버튼을 클릭하면 자세히 알아볼 수 있습니다.

마지막으로, 사용 가능한 매개 변수로는 failOnError 도 있습니다. 이를 true 로 설정하면 알림 전송시 문제가 발생했을 때 해당 런이 취소됩니다.

#### HipChat Notification

슬랙 알림 플러그인과 유사하게 힙챗 알림 플러그인이 있습니다. 이는 파이프라인 DSL 에 hipchatSend 스텝을 추가합니다. 슬랙 플러그인처럼, 힙챗 플러그인도 어플리케이션에 설정부터 해야합니다.

슬랙과 달리 힙챗 버전 1 API 나 새로운 버전 2 API 중 선택할 수 있습니다. 여기선 버전 1 을 사용하겠습니다. explore-jenkins 라는 이름을 가진 룸으로 설정하겠습니다.

**Setup in HipChat for version 1 API use**

룸 메뉴에서 Integration 을 선택하면 Jenkins 타일을 찾을 수 있습니다(`Example 16`).

> Example 16 - The Jenkins integration tile in HipChat

![image](https://user-images.githubusercontent.com/44635266/82143449-ff9cf880-987e-11ea-82fc-1815d1609c8f.png)

Jenkins 타일을 선택하면 버전 1 토큰이 있는 화면으로 이동합니다(`Example 17`).

> Example 17 - v1 token screen

![image](https://user-images.githubusercontent.com/44635266/82143453-09266080-987f-11ea-81d3-4fbc22b53b13.png)

이 토큰을 Jenkins 전역 환경 설정에 사용하려면 새로운 Jenkins Secret text 인증을 생성해야 합니다.

**Setup in HipChat for version 2 API use**

힙챗 버전 2 API 를 사용할 때 토큰을 얻는 가장 쉬운 방법은 http://<your room>.hipchat.com/account/api 를 사용하는 것입니다. 이동하면 Create new token 영역에서 토큰의 레이블을 입력한 후 타입을 선택합니다.

Create 버튼을 클릭하면 사용 가능한 v2 토큰을 볼 수 있습니다(`Example 18`).

> Example 18 - Getting a HipChat v2 token

![image](https://user-images.githubusercontent.com/44635266/82143455-13485f00-987f-11ea-8988-53414c3f402f.png)

이 토큰을 젠킨스 전역 환경 설정에서 사용하려면 새로운 Jenkins 인증을 생성해야 합니다.

**Global configuration in Jenkins**

힙챗 전역 환경 설정을 하려면 힙챗 서버의 위치부터 입력해야 합니다. 이를 위한 고유한 명칭이 있지 않으면 기본값인 api.hipchat.com 으로 두어도 됩니다.

다음은 v2 API 사용 여부 체크박스입니다. v1 API 를 사용한다면 체크하지 않고 넘어갑니다.

그 밑으로 알림을 보낼 룸의 이름을 입력합니다. 대소문자를 구분하는 룸 이름이거나 힙챗 ID 숫자가 됩니다. 쉼표로 구분하여 다중 입력이 가능합니다.

다음은 v1 을 사용할 경우 알림을 보내는 다른 ID 를 설정할 수 있습니다. 기본 값은 Jenkins 입니다.

Card Provider 필드는 힙챗의 알림 카드와 연관이 있습니다. 알림 카드에 내용은 Default cards 로 둡니다.

`Example 19` 는 Jenkins 의 힙챗 전역 환경 설정의 예시입니다.

> Example 19 - HipChat global configuration

![image](https://user-images.githubusercontent.com/44635266/82143461-1d6a5d80-987f-11ea-8f7b-650947b5ef27.png)

이 정보를 채우고 난 후 Jenkins 와 힙챗의 연동을 테스트할 수 있습니다. Test configuration 버튼을 눌렀을 때 연동이 성공했다면 `Example 20` 과 같은 테스트 알림 전송 메세지가 나타납니다.

> Example 20 - Test notification from Jenkins

![image](https://user-images.githubusercontent.com/44635266/82143466-278c5c00-987f-11ea-9773-2f3ac377c81e.png)

**Default notifications**

힙챗의 또 하나의 전역 환경 설정 옵션은 기본 알림입니다. 이는 전여긍로 설정 가능한 마지막 영역입니다. 이 영역의 내용이 기본 알림을 설정할 때 추가할 수 있는 내용입니다. 기본 알림을 추가하려면 Add 버튼을 눌러 값을 입력하면 됩니다.

기본 알림 기능은 잡의 기본 알림을 위해 존재합니다. 이 알림은 해당 잡에 알림이 설정되어 있지 않고 힙챗 알림이 빌드 후처리에 추가됐을 경우에만 전송합니다. 이 조건은 프리스타일 프로젝트에서만 가능하고, 힙챗 통합을 사용하는 파이프라인 프로젝트는 고유의 알림 스텝을 갖기 때문에, 기본 알림은 파이프라인 프로젝트에 적용되지 않습니다.

**Sending HipChat notifications in a job**

힙챗 알림 플러그인은 앞에서 언급한 hipchatSend 스텝을 사요앚가 파이프라인에서 사용할 수 있게 제공해야 합니다. 유일한 필수 매개변수는 메세지입니다. 

여기에 어떤 메세지를 보내도 상관 없는데 `env.JOB_NAME`, `env.BUILD_NUM` 같은 Jenkins 의 환경 변수나 전역 변수를 보내고 싶을 수도 있습니다. 이를 사용하려면 "" 로 감싸지는 문자열 안에서 `${}` 문법을 사용해 이를 포함시켜 그루비 문법을 충족시켜야 합니다. 다음은 기본 매개 변수만 있는 간략한 예시입니다.

```groovy
 hipchatSend "Build Started: ${env.JOB_NAME} ${env.BUILD_NUMBER}" 
```

그 외 사용할 만한 매개 변수로는 인터페이스에 메세지의 배경색을 설정합니다. 슬랙의 색상 옵션과 달리 사용할 수 있는 색상으로는 GREEN, YELLOW, RED, PURPLE, GRAY 나 RANDOM 이 있고 디폴트는 GRAY 입니다.

추가 옵션을 통해 메세지의 다른 부분을 변경할 수 있습니다. `notify` 옵션은 true 나 false 로 설정할 수 있고 이를 통해 모바일 기기 등에서 소리가 나는 사용자 알림을 트리거할 지 결정하게 됩니다. `textFomrat` 옵션은 메세지가 텍스트 포맷으로 보내지는지 결정하는 데 사용합니다. 기본 값은 false 입니다.

#### Addling Links in the Message

textFormat 옵션이 true 로 설정되지 않았을 경우 기본 HTML 을 사용해 hipchatSend 메세지에 링크를 추가할 수 있습니다. 다음은 예시입니다.

```groovy
hipchatSend "Build ${env.BUILD_NUMBER} completed for
   ${env.JOB_NAME}. Details: <a href=${env.BUILD_URL}>
   here</a>"
```

룸에 `color` 옵션과 알림을 추가한 좀 더 복잡한 예시는 다음과 같습니다.

```groovy
 hipchatSend color: 'GREEN',
      notify: true,
      message: "Build ${env.BUILD_NUMBER} completed for
      ${env.JOB_NAME}.  Details: <a href=${env.BUILD_URL}>here</a>"
```

실제 힙챗 알림은 `Example 21` 과 같습니다.

> Example 21 - HipChat notification from Jenkins

![image](https://user-images.githubusercontent.com/44635266/82143468-2eb36a00-987f-11ea-9b45-68a419982426.png)

hipchatSend 스텝이 받을 수 있는 추가 매개 변수가 잇습니다. 추가 매개 변수의 이름과 타입은 힙챗 전역 환경 설정의 값과 같습니다. 원하는 경우 기본 설정을 덮어쓸 수 잇게 하기 위해 설계됐습니다. 자세한 정보는 파이프라인 문법 화면에서 hipChat 스텝을 클릭 후 Advanced 버튼을 눌러 확인 가능합니다.

이메일 기능과 달리 협업 도구의 통합흔 계속 발전하고 잇습니다. 힙챗 v1 API 에서 v2 API 로 이동했고 슬랙은 웹훅을 더 많이 지원하고 있습니다. 호환되는 다른 서비스들도 접근 방식이 달라지고 있습니다.

Jenkins 가 정보를 전달하기 위해 사용하는 다른 수단은 리포트를 생성하거나 이를 수행할 수 있는 어플리케이션과 연동하는 것입니다.

## Reports

HTML Publisher 플러그인은 사용자가 파이프라인 코드에 스텝을 추가해 HTML 리포트의 위치를 지정할 수 있게 합니다. 또한 잡의 결과 페이지에 맞춤형 링크를 만들고, 해당 리포트를 특정 기간 동안 보관하는 기능도 제공합니다.

### Publishing HTML Reports

하위 프로젝트가 여러 개 있는 그레들 빌드 방식의 프로젝트가 있다 가정하겠습니다. 하위 프로젝트의 이름 중 하나는 api, util 이라 생각하겠습니다. 파이프라인은 하위 프로젝트에 그레들 테스트 작업을 수행하고, 각각에 작성한 단위 테스트가 수행됩니다.

관례적으로 그레들은 *index.html* 이라는 이름으로 수행한 단위 테스트의 리포트를 만듭니다. 그후 이를 `<component>/build/reports/test` 폴더에 저장합니다. 파이프라인을 위해 그레들이 생성한 HTML 테스트 리포트에 대해 api 와 util 두 하위 프로젝트에 링크를 추가합니다.

`publishHTMl` 은 DSL 스텝에 넘겨야 할 기본 정보를 알려줍니다. api 리포트를 위해 스텝을 호출하는 코드는 다음과 같습니다.

```groovy
publishHTML (target: [
      allowMissing: false,
      alwaysLinkToLastBuild: false,
      keepAll: true,
      reportDir: 'api/build/reports/test',
      reportFiles: 'index.html',
      reportName: "API Unit Testing Results"
    ])
```

대부분 필드는 이름으로 의므를 추측할 수 있습니다. HTML Publisher 플러그인이 설치 됐다면 스니펫 생성기를 통해 문법을 불러낼 수 있습니다. 일반적으로 생성기를 통해 코드를 생성하기 쉽지만, 옵션을 알아보겠습니다.

먼저 `target` 블록이 매개 변수인것을 봐야합니다. `target` 은 여러 하위 매개 변수가 있습니다.

* allowMissing
  * 이 옵션은 리포트가 없을 때 빌드를 실패시킬지 결정합니다. false 로 설정하면, 리포트가 없을 때 빌드가 실패합니다.
* alwaysLinkToLastBuild
  * 이를 true 로 설정하면 Jenkins 는 항상 마지막으로 성공한 빌드의 링크를 보여줍니다. 현재 빌드가 실패하더라도 동일합니다.
* keepAll
  * 이를 true 로 설정하면 Jenkins 는 성공한 모든 빌드의 리포트를 보관합니다. false 로 설정하면 Jenkins 는 가장 최신의 성공한 빌드의 리포트만 보관합니다.
* reportDir
  * Jenkins 워크스페이스에 HTML 파일의 상대 경로입니다.
* reportFiles
  * 보여줄 HTML 파일의 이름입니다.
* reportName
  * 잡 결과 페이지에서 리포트의 링크 이름입니다.

알림과 유사하게 이 스텝은 빌드의 끝에 수행합니다. 빌드의 성공 여부와 관계 없이 수행할 경우가 많습니다.

스크립트 방식 파이프라인의 경우 알림 스테이지의 `try-catch-finally` 영역에 추가하게 되고, 서술적 파이프라인의 경우 post 스테이지에 추가할 수 있습니다.

파이프라인 스크립트의 `finally` 섹션에 이 스텝을 추가하는 예시는 다음에 나와있습니다. 여기서 다른 노드의 `parallel` 스텝에 리포트가 생성됐기 때문에 이를 `unstash` 하고 있습니다.

```groovy
  finally {
      
      unstash 'api-reports'
      
      publishHTML (target: [
         allowMissing: false,
         alwaysLinkToLastBuild: false,
         keepAll: true,
         reportDir: 'api/build/reports/test',
         reportFiles: 'index.html',
         reportName: "API Unit Testing Results"
    ])
    
      unstash 'util-reports'
      
      publishHTML (target: [
         allowMissing: false,
         alwaysLinkToLastBuild: false,
         keepAll: true,
         reportDir: 'util/build/reports/test',
         reportFiles: 'index.html',
         reportName: "Util Unit Testing Results"
    ])
   }
```

서술적 파이프라인에선 이에 대응하는 post 섹션을 사용할 수 있습니다. `Example 22` 는 잡의 결과 페이지에 맞춤화된 리포트의 이름을 가진 링크가 왼쪽에 나타난 것입니다.

> Example 22 - Job output showing the custom report links in the left menu

![image](https://user-images.githubusercontent.com/44635266/82143470-37a43b80-987f-11ea-8662-1630d8005f0e.png)


