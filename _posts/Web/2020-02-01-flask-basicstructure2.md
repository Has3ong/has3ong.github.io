---
title : Basic Application Structure -2-
tags :
- Response
- Request
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

## The Request - Response Cycle

프레임워크에 대해 설계 측면에서 설명해 보겠습니다.

### Application and Request Contexts

Flask 가 클라이언트에서 리퀘스트를 수신하면 이 리퀘스트를 처리하기 위해 뷰 함수에서는 사용 가능한 오브젝트를 생성해야 합니다.

좋은 예는 **리퀘스트 오브젝트(request object)** 인데 이 오브젝트는 클라이언트에 의해 송신된 HTTP 리퀘스트를 캡슐화 합니다.

뷰 함수가 필요하지도 않은 너무 많은 인수를 가지는 것을 피하기 위해 Flask 는 **컨텍스트(contexts)** 를 사용하여 임시적으로 오브젝트를 글로벌하게 액세스하도록 합니다. 뷰 함수는 다음과 같이 작성할 수 있습니다.

```python
from flask import request

@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  return '<p>Your browser is %s</p>' $ user_agent
```

Flask 에서는 2 가지 컨텍스트가 있습니다. 하나는 **어플리케이션 컨택스트(application context)** 이며, 다른 하나는 **리퀘스트 컨텍스트(request context)** 입니다. 아래 표는 각각의 컨텍스트에서 사용되는 변수입니다.

|변수 이름|컨텍스트|설명|
|:--:|:--:|:--:|
|current_app|어플리케이션 컨택스트|활성화된 어플리케이션을 위한 인스턴스|
|g|어플리케이션 컨택스트|리퀘스트를 처리하는 동안 어플리케이션에서 임시 스토리지를 사용할 수 있는 오브젝트|
|request|리퀘스트 컨텍스트|클라이언트에 의해 송신된 HTTP 리퀘스트의 콘텐츠를 캡슐화 하는 리퀘스트 오브젝트|
|session|리퀘스트 컨텍스트|사용자 세션이며, 어플리케이션이 리퀘스트 사이의 "remembered" 인 값들을 저장하는데 사용하는 딕셔너리|

Flask 는 리퀘스트를 디스패치 하기 전에 어플리케이션과 리퀘스트 컨텍스트를 활성화 하며, 따라서 리퀘스트가 처리될 때 삭제합니다.

어플리케이션 컨텍스트가 푸시되면 current_app 과 g 변수는 스레드에서 사용 가능해 집니다. 리퀘스트 컨텍스트가 푸시될 때 request 와 session 역시 사용 가능해집니다.

활성화 어플리케이션이나 리퀘스트 컨텍스트 없이 변수들을 접근하려면 에러가 발생합니다.

아래는 어플리케이션 컨텍스트의 동작 방법입니다.

```shell
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```

위 예제에서는 `current_app.name` 은 어플리케이션 컨텍스트 없이 컨텍스트가 올바르다고 푸시될 때 실패합니다.

### Request Dispatching

어플리케이션의 클라이언트에서 리퀘스트를 수신하면 서비스하기 위해 실행할 뷰 함수를 검색해야 합니다. 이를 위해 Flask 어플리케이션 **URL 맵** 에서 리퀘스트에서 주어진 URL 을 검토하고 처리할 뷰 함수에 URL 의 매핑을 포함하고 있는지 확인합니다. Flask 는 이 맵을 app.route 데코레이터나 데코레이터를 사용하지 않은 버전인 app.add_url_rule() 를 사용하여 빌드합니다.

플라스크 어플리케이션의 URL 맵이 어떤 것과 비슷한지 보려면 Python 쉘에서 hello.py 생성된 맵을 보겠습니다.

```shell
(venv) $ python
>>> from hello import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
  <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
  <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

/ 와 **/user/<name>** 라우트 어플리케이션에 있는 app.route 데코레이터에 정의 되어 있습니다. **/static/<filename>** 라우트는 Flask 에 의해 추가된 특별한 라우트 파일이며 정적 파일을 접근할 수 있습니다.

URL 맵에 있는 HEAD, GET, OPTIONS 항목은 라우트에 의해 처리되는 리퀘스트 메소드 입니다.

### Request Hooks

가끔 각각의 리퀘스트를 처리하기 전후에 코드를 실행하는것이 유용합니다. 대표적으로 데이터베이스 커넥션을 생성하는 경우와 사용자를 인증하는 경우입니다. 모든 뷰 함수에서 이러한 작업을 처리하는 코드를 중복으로 생성하는 대신 Flask 에서는 옵션을 제공하여 함수로 등록하고 리퀘스트가 뷰 함수에 디스패치되는 전후에 실행되도록 합니다.

리퀘스트 후크는 데코레이터를 사용하여 구현합니다.

아래는 Flask 에서 제공하는 4 개의 후크 입니다.

* **before_first_request** : 함수를 등록하여 첫 번째 리퀘스트가 처리되기 전에 실행한다.
* **before_request** : 각 리퀘스트 전에 실행하는 함수를 등록한다.
* **after_request** : 처리되지 않는 예외가 발생하지 않으면 각 리퀘스트 이후에 실행하는 함수를 등록한다.
* **teardown_request** : 처리되지 않는 예외가 발생하더라도 각 리퀘스트 이후에 실행하는 함수를 등록한다.

리퀘스트 후크 함수와 뷰 함수 사이에 데이터를 공유하기 위한 공통패턴은 g 컨텍스트 전역 변수를 사용하는것입니다.

### Responses

Flask 뷰 함수를 호출할 때 리퀘스트에 대한 응답(response) 로 값을 리턴합니다.

HTTP 응답의 가장 중요한 부분은 **상태 코드(status code)** 입니다. Flask 에서는 기본적으로 200 으로 설정하며, 이 코드는 리퀘스트가 올바르게 처리됐다는 의미입니다.

다른 상태 코드를 가지는 응답을 필요할 때, 응답 텍스트 이후 2 번째 리턴값으로 뉴메릭 코드를 추가할 수 있습니다. 아래는 잘못된 리퀘스트 에러 코드 입니다.

```python
@app.route('/')
def index():
  return '<h1>Bad Request</h1>', 400
```

뷰 함수에 의해 리턴된 응답은 3 번째 인수를 가질 수 있는데 이 인수는 HTTP 응답에 추가된 헤더의 딕셔너리 입니다.

Flask 뷰 함수는 하나, 두 개 혹은 세 개의 값을 튜플로 리턴하는 대신 Response 오브젝트를 리턴하는 옵션을 갖습니다. `make_response()` 함수는 여러개의 인수를 가지는데 이는 뷰 함수에서 리턴되는 것과 같은 값이며 Response 오브젝트를 리턴합니다.

아래 예제는 응답 오브젝트를 생성하고 그 안에 쿠키를 설정하는 예 입니다.

```python
from flask import make_response

@app.route('/')
def index():
  response = make_response('<h1>This document carries a cookie!<h1>')
  response.set_cookie('answer', '42')
  return response
```

**리다이렉트(redirect)** 라는 응답 타입이 있습니다. 페이지 도큐먼트를 포함하지 않으며 새로운 페이지를 로드하는 새로운 URL 을 브라우저에 전달합니다.

리다이렉트는 302 응답 상태 코드와 Location 헤더에 있는 리다이렉트할 URL 을 사용하여 알려줍니다. `redirect()` 함수를 제공합니다.

```python
from flask import redirect

@app.route('/')
def index():
  return redirect('http://www.example.com')
```

다른 응답은 abort 함수가 사용되는데 에러 핸들링을 위해 사용됩니다.

```python
from flask import abort

@app.route('/user/<id>')
def get_user(id):
  if not user:
    abort(404)
  return '<h1>Hello, %s</h1>' % user.name
```

abort 는 예외를 발생시켜 웹 서버에 제어를 넘겨 줍니다.

## Flask Extensions

Flask 에서는 데이터베이스 사용자 인증과 같은 중요한 기능이 확장 가능하도록 설계되어 있습니다.

### Command-Line Options with Flask-Script

Flask-script 는 Flask 어플리케이션에 커맨드 라인 파서를 추가하는 플라스크 확장 입니다.아래 명령어로 설치할 수 있습니다.

```shell
$ pip install flask-script
```

다음과 같이 코드를 작성해 보겠습니다.

```python
from flask import Flask
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return '<h1> Hello World !</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1> Hello %s !</h1>' % name

if __name__=='__main__':
    manager.run()
```

이제 shell 커맨드에서 웹 서버를 시작하여 많은 옵션을 사용할 수 있습니다.


```shell
$ python3 kakao.py runserver --help                     

usage: kakao.py runserver [-?] [-h HOST] [-p PORT] [--threaded]
                          [--processes PROCESSES] [--passthrough-errors] [-d]
                          [-D] [-r] [-R] [--ssl-crt SSL_CRT]
                          [--ssl-key SSL_KEY]

Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
  -h HOST, --host HOST
  -p PORT, --port PORT
  --threaded
  --processes PROCESSES
  --passthrough-errors
  -d, --debug           enable the Werkzeug debugger (DO NOT use in production
                        code)
  -D, --no-debug        disable the Werkzeug debugger
  -r, --reload          monitor Python files for changes (not 100% safe for
                        production use)
  -R, --no-reload       do not monitor Python files for changes
  --ssl-crt SSL_CRT     Path to ssl certificate
  --ssl-key SSL_KEY     Path to ssl key
```

**http://0.0.0.0:5000** 으로 웹 서버를 시작해 보겠습니다.

```shell
$ python3 kakao.py runserver --host 0.0.0.0           
 * Serving Flask app "kakao" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```