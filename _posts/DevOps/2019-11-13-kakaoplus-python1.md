---
title : Docker와 Python Flask 를 이용한 카카오톡 플러스친구 개발 과 배포 -1-
tags:
- 챗봇
- Python
- Flask
- Docker
- 카카오톡 플러스친구
categories:
- DevOps
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

> 개발하기에 앞서 https://i.kakao.com/login 여기서 개발 제휴 신청을 하시고 진행하셔야 합니다. 


## 개발환경

```
$ Goorm IDE / Ubuntu 18.04 LTS
$ Python 3.6.0
$ Flask 1.1.0
```

## 1. Flask App 설정

Goorm IDE 에서 제공하는 서비스를 이용해서 컨테이너를 생성해줍니다.

저는 컨테이너를 만들 때 항상 Blank로 하니까 Blank로 지정해서 만들겠습니다.

> 컨테이너 설정

![image](https://user-images.githubusercontent.com/44635266/68529937-0fbfa280-0347-11ea-8861-6bf91c31a5ac.png)

> 생성된 컨테이너

![image](https://user-images.githubusercontent.com/44635266/68529938-10f0cf80-0347-11ea-9f56-02b7d7055979.png)

### 1.1 Python 및 필요한 패키지 설치

Python3.6 과 pip3 설치

```
$ sudo apt-get update

# python3.6 설치
$ sudo apt-get install python3.6

# pip 설치
$ sudo apt-get install python3-pip -y
```

Flask를 설치하겠습니다.

```
$ pip3 install Flask
```

### 1.2 application.py 설정

이제 Flask를 통해 웹 서버를 배포할 app.py 를 만들겠습니다. 이번 예제에서는 작동만 확인할거니까 간단하게 작성하겠습니다.

Flask 기본 포트가 5000번입니다. 지금은 제가 사용하고 있으니 8888포트를 이용해보겠습니다.

> app.py

```
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():
    dataSend = {
      "user" : "has3ong",
      "blog" : "github",
    }
    return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']
    
    if content == u"안녕":
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type" : "basicCard",
                            "items": [
                                {
                                    "title" : "",
                                    "description" : "안녕"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    else :
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText":{
                            "text" : "아직 공부하고있습니다."
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
```

"안녕" 이라는 메세지를 받았을 때 카카오 채널이 어떻게 대답할지는 [카카오  i 오픈빌 도움말](https://i.kakao.com/docs/skill-response-format#action) 로 가시면 됩니다. 이 URL에 전부 나와있으니까 보셔서 하시면 될겁니다.

### 1.3 Flask App 실행

```
$ python3 app.py

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8888/ (Press CTRL+C to quit)
211.214.14.153 - - [09/Nov/2019 15:10:00] "GET /keyboard HTTP/1.1" 200 -
```

### 1.4 Container 포트포워딩

다음과 같이 설정 한 뒤

![image](https://user-images.githubusercontent.com/44635266/68530729-78f6e400-034e-11ea-929d-12fc13e08534.png)

*http://13.125.220.65:56744/keyboard* 로 접속해보겠습니다.

![image](https://user-images.githubusercontent.com/44635266/68530730-7a281100-034e-11ea-9d04-aec73e10e1c0.png)

설정한것과 똑같이 표시가 되면 잘 구현이 된것입니다.

## 2. 카카오톡 오픈빌더 i 설정

![image](https://user-images.githubusercontent.com/44635266/68691190-afcf3300-05b6-11ea-882a-04bda6f62fbb.png)

개발 제휴 신청이 끝나신 분들은 **카카오톡 채널 챗봇 만들기** 버튼을 클릭하시면 됩니다.

![image](https://user-images.githubusercontent.com/44635266/68691202-b52c7d80-05b6-11ea-962c-074132adb31a.png)

저는 운영중인게 있어서 가려놓겠습니다.

![image](https://user-images.githubusercontent.com/44635266/68691208-b8276e00-05b6-11ea-884a-2db8793dd35b.png)

이름을 Docker Test로 만들었습니다. 여기서 **시나리오**에 **+ 시나리오** 버튼을 눌러줍니다.

![image](https://user-images.githubusercontent.com/44635266/68691225-bfe71280-05b6-11ea-9fed-8c7af812603b.png)

저는 간단한 발화를 할 예정이니까 사용자 발화에서 **안녕**만 사용할게요.

![image](https://user-images.githubusercontent.com/44635266/68691239-c4133000-05b6-11ea-8c6c-da8126ee775b.png)

그리고 **스킬** 메뉴로 가셔서 설명은 아무렇게 적으시고 URL을 아까 사용한 http://13.125.220.65:56744/message 로 적겠습니다.

이전에는 GET 메소드를 활용하여 접속이 되는지 확인했고, 현재 사용자들의 발화를 POST로 받아서 진행해야 하니 아까 구현한 POST 함수 message로 사용합니다.

![image](https://user-images.githubusercontent.com/44635266/68691258-cd040180-05b6-11ea-81a0-9e5145a3503c.png)

그리고 **시나리오** 탭에서 **파라미터 설정**과 **봇 응답**을 방금 설정한 스킬로 설정해줍니다.

이제 카카오톡 채널 관리자로 가볼게요.

## 3. 카카오톡 채널 설정

[카카오톡 채널 관리자](https://center-pf.kakao.com/profiles)로 가줍니다.

![image](https://user-images.githubusercontent.com/44635266/68691301-ddb47780-05b6-11ea-913a-2bf1fca8ab5b.png)

채널을 개설해 줍니다.

![image](https://user-images.githubusercontent.com/44635266/68691317-e1e09500-05b6-11ea-85fd-d2c403335d65.png)

그리고 검색이 되게하기 위해서 **관리** 메뉴에서 공개설정을 ON으로 해줍니다.

## 4. 배포

![image](https://user-images.githubusercontent.com/44635266/68691321-e4db8580-05b6-11ea-9edf-75a26ce2b961.png)

다시 오픈빌더 i 로 오셔서 설정에서 방금 설정한 카카오톡 채널과 오픈빌더를 연동시켜줍니다.

![image](https://user-images.githubusercontent.com/44635266/68691329-e9a03980-05b6-11ea-8370-e86f1d54dc1d.png)

마지막으로 배포를 눌러줍니다. 이제 모든 과정이 끝났으니까 친구 추가후 메세지를 날려볼게요.

![image](https://user-images.githubusercontent.com/44635266/68691331-eb69fd00-05b6-11ea-9327-9c81b3c0a92a.png)

정상적으로 작동하는걸 확인할 수 있습니다.
