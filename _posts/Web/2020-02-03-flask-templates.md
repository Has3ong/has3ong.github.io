---
title : Flask Templates
tags :
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

템플릿은 응답 텍스트를 포함하고 있는 파일이며, 이 파일은 리퀘스트 내용에서 인식 가능한 동적 파트에 대한 변수들을 포함하고 있습니다. 변수들을 실제 값으로 바꾸는 프로세스와 최종 응답 문자열을 리턴하는 프로세스를 **렌더링(rendering)** 이라 합니다.

Flask 는 템플릿을 렌더링하는 테스크를 위해 **Jinja2** 라는 엔진을 사용합니다.

## The Jinja2 Template Engine

간단한 HTML 코드를 Jinja2 템플릿으로 나타내 보겠습니다.

```html
<h1> Hello World! </h1>
```

`World!` 를 `name` 이라는 변수로 바꾸고 위 코드를 Jinja2 로 구현하면 다음과 같습니다.

```html
<h1> Hello, {{ name }} ! </h1>
```

### Rendering Templates

Flask 에서는 어플리케이션 폴더 안에 위치하는 **templates** 서브폴더에서 템플릿을 검색합니다.

```python
from flask import Flask, render_template

# ...

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)
```

Flask 에서 제공하는 `render_template` 함수는 어플리케이션과 Jinja2 템플릿 엔진을 통합합니다. 이 함수는 첫 번째 인수로 템플릿의 파일 이름을 사용합니다. 추가 인수는 템플릿에서 참조한 변수들에 대한 실제 값을 표현하는 key-value 쌍이다. 이 예제에서 두 번째 템플릿은 name 변수를 받게 됩니다.

### Variables

Flask 변수는 위에서 사용되는 `{{ name }}` 부분을 뜻합니다. 

Jinja2 는 어떤 타입의 변수라도 인식합니다. List, Dictionary, Object 같은 타입도 인식합니다. 아래 예를 보여드리겠습니다.

```html
{% raw %}
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{mylist[myintvar] }}.</p>
<p> A value from an object's method: {{ myobj.somemethod() }}.</p>
{% endraw %}
```

변수는 **필터(filter)** 를 사용하여 수정할 수 있으며 파이프 기호를 분리자로 하여 변수 이름에 추가합니다. 예를 들어 다음 템플릿은 name 변수의 첫 문자를 대문자로 합니다.

```python
Hello, {{ name|capitalize }}
```

아래는 Jinja2 에서 자주 사용하는 필터를 정리한것 입니다.

|필터 이름|설명|
|:--:|:--:|
|safe|이스케이프를 적용하지 않고 값을 렌더링한다.|
|capitalize|값의 첫 번째 문자를 대문자로 만들고 나머지는 소문자로 만든다.|
|lower|값을 소문자로 만든다.|
|upper|값을 대문자로 만든다.|
|title|값의 각 단어들을 capitalize 한다.|
|trim|앞부분과 뒷부분에서 공백 문자를 삭제한다.|
|striptags|렌더링하기 전에 값에 존재하고 있는 HTML 태그를 제거한다.|

위의 safe 필터를 예로 들여보면 Jinja2 는 기본적으로 모든 변수를 보안 목적으로 **이스케이프(escape)** 합니다. 예를 들어, 변수가 `'<h1>Hello</h1>'` 라는 값으로 설정이 되어 있으면 Jinja2 는 `'&lt;h1&gt;Hello&lt;/h1&gt;'` 형태로 렌더링 합니다. 

이러한 기능은 h1 항목을 화면에는 보이되 브라우저에서는 인식하지 못하도록 합니다. 변수에 저장된 HTML 코드를 보이게 할 경우가 많으면 safe 필터를 사용하면 됩니다.
 
### Control Structure

Jinja2 는 몇가지 제어 문자를 제공합니다.

아래 예제를 통해 제어문이 템플릿에서 어떻게 사용되는지 알아보겠습니다.

```html
{% raw %}
{% if user %}
  Hello, {{ user }}!
{% else %}
  Hello, Stranger !
{% endif %}
{% endraw %}
```

템플릿의 또 다른 공통 점은 항목의 리스트를 렌더링하는 점 입니다. 다음은 for 루프를 알아보겠습니다.

```html
{% raw %}
<ul>
  {% for comment in comments %}
    <li>{{ comment }}</li>
  {% endfor %}
</ul>
{% endraw %}
```

Jinja2 에서는 **매크로** 기능도 제공합니다.

```html
{% raw %}
{% macro render_comment(comment) %}
  <li>{{ comment }}</li>
{% endmacro %}

<ul>
  {% for comment in comments %}
    {{ render_comment(comment) }}
  {% endfor %}
</ul>
{% endraw %}
```

매크로를 재사용하기 위해서는 독립적인 파일에 저장해 두고 필요할 때 템플릿에 **임포트** 하면 됩니다.

```html
{% raw %}
{% import 'macros.html' as macros %}
<ul>
  {% for comment in comments %}
    {{ macros.render_comment(comment) }}
  {% endfor %}
</ul>
{% endraw %}
```

여러 위치에 반복되어야 하는 템플릿 코드 부분은 별도의 파일에 저장하고 필요한 템플릿을 **인클루드(include)** 하여 불필요한 반복을 피한다.

```html
{% raw %}
{% include 'common.html' %}
{% endraw %}
```

재사용의 또 다른 강력한 기능으로 템플릿의 상속이 있습니다. 이 개념은 파이썬에서의 클래스 상속과 비슷합니다. 먼저 베이스 템플릿 `base.html` 을 생성해보겠습니다.

```html
{% raw %}
<html>
<head>
  {% block head %}
  <title>{% block title %}{% endblock %} - MyApplication</title>
  {% endblock %}
</head>
<body>
  {% block body %}
  {% endblock %}
</body>
</html>
{% endraw %}
```

여기서 block 태그는 파생된 템플릿이 변경할 수 있는 항목을 정의합니다. 이 예제에서는 head, title, body 라 하는 블록이 있습니다. title 은 head 에 포함되어 있습니다. 다음 예제는 베이스 템플릿에서 파생된 템플릿입니다.

```html
{% raw %}
{% extends "base.html %}
{% block title %}Index{% endblock %}
{% block head %}
  {{ super() }}
  <style>
  </style>
{% endblock %}
{% block body %}
<h1>Hello, World!</h1>
{% endblock %}
{% endraw %}
```

extends 디렉티브는 이 템플릿이 `base.html` 로부터 파생되었다는것을 선언합니다. head 블록을 새롭게 정의하는 경우에는 베이스 템플릿에 기존의 내용이 존재하기 때문에 원래의 내용을 유지하기 위해 `super()` 를 사용합니다.

## Twitter Bootstrap Integration with Flask-Bootstrap

Bootstrap 은 트위터에서 제공하는 오픈 소스 프레임 워크이며 현대의 모든 웹 브라우저와 호환되는 웹 페이지를 생성할 수 있도록 하는 사용자 인터페이스 컴포넌트를 제공합니다.

Flask 에서는 `Flask-Bootstrap` 이라는 확자응ㄹ 사용할 수 있습니다.

```shell
pip install flask-bootstrap
```

Flask-Bootstrap 초기화는 다음과 같이 합니다.

```python
from flask.ext.bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)
```

관련 소스는 [Github](https://github.com/miguelgrinberg/flasky/tree/master/app/templates) 링크에 있습니다. 간단한 예제만 보여드리고 마무리하겠습니다.

> templates/user.html

```html
{% raw %}
{% extends "base.html" %}
{% import "_macros.html" as macros %}

{% block title %}Flasky - {{ user.username }}{% endblock %}

{% block page_content %}
<div class="page-header">
    <img class="img-rounded profile-thumbnail" src="{{ user.gravatar(size=256) }}">
    <div class="profile-header">
        <h1>{{ user.username }}</h1>
        {% if user.name or user.location %}
        <p>
            {% if user.name %}{{ user.name }}<br>{% endif %}
            {% if user.location %}
                from <a href="http://maps.google.com/?q={{ user.location }}">{{ user.location }}</a><br>
            {% endif %}
        </p>
        {% endif %}
        {% if current_user.is_administrator() %}
        <p><a href="mailto:{{ user.email }}">{{ user.email }}</a></p>
        {% endif %}
        {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
        <p>Member since {{ moment(user.member_since).format('L') }}. Last seen {{ moment(user.last_seen).fromNow() }}.</p>
        <p>{{ user.posts.count() }} blog posts. {{ user.comments.count() }} comments.</p>
        <p>
            {% if current_user.can(Permission.FOLLOW) and user != current_user %}
                {% if not current_user.is_following(user) %}
                <a href="{{ url_for('.follow', username=user.username) }}" class="btn btn-primary">Follow</a>
                {% else %}
                <a href="{{ url_for('.unfollow', username=user.username) }}" class="btn btn-default">Unfollow</a>
                {% endif %}
            {% endif %}
            <a href="{{ url_for('.followers', username=user.username) }}">Followers: <span class="badge">{{ user.followers.count() - 1 }}</span></a>
            <a href="{{ url_for('.followed_by', username=user.username) }}">Following: <span class="badge">{{ user.followed.count() - 1 }}</span></a>
            {% if current_user.is_authenticated and user != current_user and user.is_following(current_user) %}
            | <span class="label label-default">Follows you</span>
            {% endif %}
        </p>
        <p>
            {% if user == current_user %}
            <a class="btn btn-default" href="{{ url_for('.edit_profile') }}">Edit Profile</a>
            {% endif %}
            {% if current_user.is_administrator() %}
            <a class="btn btn-danger" href="{{ url_for('.edit_profile_admin', id=user.id) }}">Edit Profile [Admin]</a>
            {% endif %}
        </p>
    </div>
</div>
<h3>Posts by {{ user.username }}</h3>
{% include '_posts.html' %}
{% if pagination %}
<div class="pagination">
    {{ macros.pagination_widget(pagination, '.user', username=user.username) }}
</div>
{% endif %}
{% endblock %}
{% endraw %}
```

위 파일은 Flask-Bootstrap 에서 `bootstrap/base.html` 파일을 참조하여 템플릿 상속을 구현합니다.

베이스 템플릿은 파생된 템플릿에 의해 오버라이드될 수 있는 블록을 정의합니다. block 과 endblock 디렉티브는 베이스 템플릿에 추가된 내용의 블록을 정의합니다.

`user.html` 파일은 title, navbar, content 라는 3개의 블록을 정의합니다.

결과는 아래와 같습니다.

> Example

![image](https://user-images.githubusercontent.com/44635266/73659076-d776f880-46d8-11ea-8eba-37ecb1048104.png)

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
