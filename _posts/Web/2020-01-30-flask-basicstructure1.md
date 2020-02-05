---
title : Basic Application Structure -1-
tags :
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

### Server Startup

어플리케이션 인스턴스는 run 메소드를 가지고 있는데 이 메소드는 Flask 의 통합 개발 웹 서버를 실행합니다.

```python
if __name__ == '__main__':
  app.run(debug=True)
```

`__name__ = '__main__'` 이라는 파이썬 코드는 스크립트가 직접 실행될 때만 개발 웹 서버가 실행되는것을 알려줍니다. 스크립트가 다른 스크립트에 의해 임포트 되면 부모 스크립트는 다른 서버를 실행할 수 있으며 따라서 `app.run()` 호출은 건너 뜁니다.

`app.run()` 에 주어진 여러가지 옵션 인수를 사용하여 웹 서버의 오퍼레이션 모드를 설정할 수 있습니다. 개발 과정에서 이러한 기능은 디버그 모드를 사용할 수 있도록 하기 때문에 **디버거(debugger)** 와 **리로더(reloader)** 를 활성화 할 수도 있습니다.

### A Complication Application

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


