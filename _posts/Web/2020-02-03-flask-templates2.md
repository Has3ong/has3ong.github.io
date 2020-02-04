---
title : Templates -2-
tags :
- Flask-Moment
- Static Files
- Custom Error Pages
- Link
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

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
{% extends "base.html" %}

{% block title %}Flasky - Page Not Found{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Not Found</h1>
</div>
{% endblock %}
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
{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
{% endblock %}
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
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

Flask-Moment 는 다음과 같이 사용하면 됩니다.

```python
from datetime import datetime

@app.route('/')
def index():
  return render_template('index.html', current_time=datetime.utcnow())
```

```html
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
```

`Format('LLL)` 은 컴퓨터에 설정되어 있는 시간대와 위치에 따라 날짜와 시간을 렌더링 합니다. 인수는 렌더링 스타일을 정합니다.

`fromNow()` 렌더링 스타일은 상대 타임스탬프를 렌더링 하고 넘겨진 시간에 따라 자동으로 **refresh** 합니다.