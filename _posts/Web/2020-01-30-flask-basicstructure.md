---
title : Basic Application Structure
tags :
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

## Initialization

모든 Flask 어플리케이션은 **어플리케이션 인스턴스(application instance)** 를 생성해야 합니다. 웹 서버는 클라이언트로부터 수신한 모든 request 를 오브젝트에서 처리하는데 이때 **웹 서버 게이트웨이 인터페이스(Web Server Gateway Interface)** 라는 프로토콜을 사용합니다.

어플리케이션 인스턴스는 Flask 클래스의 오브젝트이며 다음과 같이 생성됩니다.

```python
from flask import Flask
app = Flask(__name__)
```

Flask 클래스 생성자에 필요한 인자는 메인 모듈의 이름이나 어플리케이션 패키지 이름 입니다. 대부분의 어플리케이션에서는 파이썬의 `__name__` 변수가 적절한 값 입니다.

## Routes and View Functions

웹 브라우저와 같은 클라이언트는 웹 서버에 **리퀘스트(request)** 를 전송하며 플라스크 어플리케이션 인스턴스에 교대로 전송합니다. 어플리케이션 인스턴스는 각 URL 리퀘스트 실행을 위해 어떤 코드가 필요한지 알아야 하며, 따라서 URL 을 파이썬에 매핑하는 기능이 필요합니다. 이 URL 을 처리하는 함수의 관련성을 **라우트(route)** 라고한다.

파이썬에서는 `app.route` 데코레이터를 사용하는 것입니다. 데코레이터는 아래와 같이 작성합니다.

```python
@app.route
def index():
  return '<h1>Hello World!</h1>
```

클라이언트가 웹 서버에 리퀘스트를 보내면 서버에서는 리턴값으로 **응답(response)** 을 보냅니다. 이 응답은 클라이언트가 수신하는 값이며, 사용자가 보게 되는 인터넷 문서 입니다.

많은 웹 서비스의 URL 은 `http://example.com/<name>` 와 같이 되어있습니다. Flask 에서는 이러한 여러가지 타입의 URL 을 route 데코레이터에 있는 특별한 문법을 사용하여 지원합니다. 다음 예제는 동적 이름 컴포넌트를 가지는 라우트 입니다.

```python
@app.route('/user/<name>')
def user(name):
  return '<h1>Hello, %s!</h1>' % name
```

`<name>` 부분이 동적 부분이며 정적 부분과 매칭되는 URL 이 라우트에 매핑 됩니다. 이 `user()` 같은 함수를 **뷰 함수(view function)** 이라 하며, 뷰 함수가 실행되면 플라스크는 동적 컴포넌트를 인수로 전송합니다.

라우트에 있는 동적 컴포넌트는 기본적으로 문자열이지만 타입에 의해 정의될 수도 있습니다. 라우트 `/user/<int:id>` 는 id 동적 세그먼트에서 정숫값을 갖는 URL 에만 매칭됩니다. Flask 는 라우트에 대해 `int`, `float`, `path` 를 지원합니다.

## Server Startup

어플리케이션 인스턴스는 run 메소드를 가지고 있는데 이 메소드는 Flask 의 통합 개발 웹 서버를 실행합니다.

```python
if __name__ == '__main__':
  app.run(debug=True)
```

`__name__ = '__main__'` 이라는 파이썬 코드는 스크립트가 직접 실행될 때만 개발 웹 서버가 실행되는것을 알려줍니다. 스크립트가 다른 스크립트에 의해 임포트 되면 부모 스크립트는 다른 서버를 실행할 수 있으며 따라서 `app.run()` 호출은 건너 뜁니다.

`app.run()` 에 주어진 여러가지 옵션 인수를 사용하여 웹 서버의 오퍼레이션 모드를 설정할 수 있습니다. 개발 과정에서 이러한 기능은 디버그 모드를 사용할 수 있도록 하기 때문에 **디버거(debugger)** 와 **리로더(reloader)** 를 활성화 할 수도 있습니다.

## A Complication Application

위에서 사용한 예제를 사용하여 간단한 어플리케이션을 만들어 보겠습니다.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Hello World !</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1> Hello %s !</h1>' % name

if __name__=='__main__':
    app.run(debug=True)
```

실행을 시키면 아래와 같이 로그가 나오게 됩니다. 여기서 `http://127.0.0.1:5000/` 로 접속해보겠습니다.

```python
 * Serving Flask app "kakao" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 269-076-111
```

> `http://127.0.0.1:5000/`

![image](https://user-images.githubusercontent.com/44635266/73446680-8a291d00-43a0-11ea-8ecc-0bbd4818d97a.png)

동적 라우팅 테스트도 해보겠습니다.

> `http://127.0.0.1:5000/user/has3ong`

![image](https://user-images.githubusercontent.com/44635266/73446753-b0e75380-43a0-11ea-83f6-36c1357a5ac0.png)

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


## Custom Error Page

브라우저 주소 바에 정확하지 않은 경로를 입력하면 404 코드 에러 페이지를 만나게됩니다.

Flask 에서는 어플리케이션에서 일반적인 라우터와 마찬가지로 커스텀 에러페이지를 정의할 수 있도록 해줍니다.

가장 일반적인 두 가지 에러코드는 404 이며 클라이언트가 알지 못하는 경로를 요청했을 때 발생합니다. 또한, 500 코드는 처리하지 못하는 예외에 대해 발생합니다.

```python
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500
```

에러 핸들러는 뷰 함수와 마찬가지로 상태코드랑 같이 응답을 리턴합니다.

관련 에러코드 소스는 [Github](https://github.com/miguelgrinberg/flasky/tree/master/app/templates) 경로에서 `templates/user.html`, `templates/404.html`, `templates/500.html` 과 같이 사용하면 됩니다. `404.html` 을 예시로 보여드리겠습니다.

> templates/404.html

```html
{% raw %}
{% extends "base.html" %}

{% block title %}Flasky - Page Not Found{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Not Found</h1>
</div>
{% endblock %}
{% endraw %}
```

위 페이지는 아래와 같이 보입니다.

![image](https://user-images.githubusercontent.com/44635266/73659071-d645cb80-46d8-11ea-83cc-ea0c2d6dd367.png)

## Links

하나 이상의 라우터가 필요한 어플리케이션은 내비게이션 바와 같이 서로 다른 페이지들을 연결하는 링크를 포함시켜야 합니다.

간단한 사용법은 함수는 하나의 인수로 뷰 함수 이름을 가지고 URL 을 리턴합니다. 예를 들어 `hello.py` 에서 `url_for('index')` 호출은 / 를 리턴합니다. `url_for('index, _external=True)` 호출은 절대 경로의 URL 을 리턴하지 않습니다. 

위 예에서는 **http://localhost:5000/** 을 리턴합니다.

동적 URL 은 동적 파트를 키워드 인수로 `url_for()` 에 넘겨서 생성할 수 있습니다. 예를 들어, `url_for('user', name='john', _external=True)` 은 **http://localhost:5000/user/john** 을 리턴합니다.

`url_for()` 에 전송된 키워드 인수는 동적 라우트에 사용된 인수들의 제한을 받지 않습니다. 함수에서는 쿼리 문자열에 다음과 같이 추가 인수를 더할 수도 있습니다. ` url_for('index', page=2)` 는 **/?page=2** 를 리턴합니다.

## Static Files

정적 파일은 HTML 코드에 참조되는 이미지, JavaScript 파일, CSS 파일입니다.

정적 파일을 사용할 때 URL 맵에 정적 엔트리가 존재하여 정적 파일에 대한 참조가 `/static/filename` 과 같이 경로로 정의되어 처리됩니다. 예를들어 `url_for('static', filename='css/styles.css', _external=True)` 에 대한 호출은 **http://localhost:5000/static/css/styles.css** 을 리턴합니다.

기본 설정에서 Flask 는 어플리케이션의 루트 폴더에 있는 static 이라는 서브디렉토리에서 정적 파일을 찾습니다. 서버가 URL 을 받으면 `static/css/style.css` 에 있는 파일 시스템의 파일 내용을 포함하는 응답을 생성합니다.

다음은 `favicon.ico` 아이콘을 어떻게 포함하는지 나타냅니다.

```html
{% raw %}
{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
{% endblock %}
{% endraw %}
```

아이콘 선언은 head 블록 끝부분에 추가합니다. `super()` 가 베이스 템플릿에 정의된 블록의 원래 컨텐츠를 보존하기 위해 어떻게 사용하는지 보겠습니다.

## Localization of Dates and Times with Flask-Moment

웹 어플리케이션에서 날짜와 시간을 처리하는 것은 사용자가 전 세계에서 서로 다른 시간대를 사용하기 때문에 간단하지 않습니다.

서버는 각 사용자의 위치와 무관한 시간 단위가 필요하며 따라서 **협정세계시(Coordinated Universal Time, UTC) 를 사용합니다.** 하지만 사용자는 일반적으로 자신이 거주하는 위치에 맞게 시간이 표현되기 원합니다.

이를 위해 자바스크립트로 작성된 라이브러리를 사용하면 좋습니다. 이 라이브러리는 `moment.js` 라 하며 브라우저에서 시간과 날짜를 렌더링 해줍니다.

Flask-Moment 는 pip 를 사용하여 설치합니다.

```shell
pip install flask-moment
```

다음과 같이 초기화 합니다.

```python
from flask.ext.moment import Moment
moment = Moment(app)
```

Flask-moment 는 `moment.js` 이외에도 `jquery.js` 가 필요합니다.

두 파일은 CDN 에서 참조하면 됩니다. 이 라이브러리가 베이스 템플릿의 scripts 에서는 다음과 같이 로드됩니다.

```html
{% raw %}
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
{% endraw %}
```

Flask-Moment 는 다음과 같이 사용하면 됩니다.

```python
from datetime import datetime

@app.route('/')
def index():
  return render_template('index.html', current_time=datetime.utcnow())
```

```html
{% raw %}
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
{% endraw %}
```

`Format('LLL)` 은 컴퓨터에 설정되어 있는 시간대와 위치에 따라 날짜와 시간을 렌더링 합니다. 인수는 렌더링 스타일을 정합니다.

`fromNow()` 렌더링 스타일은 상대 타임스탬프를 렌더링 하고 넘겨진 시간에 따라 자동으로 **refresh** 합니다.