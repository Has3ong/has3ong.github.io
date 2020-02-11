---
title : Web Forms
tags :
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

Flask-WTF 확장은 웹 폼을 사용할 수 있게 해줍니다.

```python
$ pip install flask-wtf
```

## Cross-Site RequestForgercy (CSRF) Protection

기본적으로 Flask-WTF 는 CSRF 공겨으로부터 폼을 보호합니다. CSRF 공격은 악의적 웹사이트에서 희생자가 로그인한 다른 웹 사이트로 리퀘스트를 전송할 때 일어납니다.

CSRF 보호를 구현하기 위해 Flask-WTF 는 암호화 키를 설정하기 위한 어플리케이션이 필요합니다. Flask-WTF 는 이 키를 사용하여 암호화된 토큰을 생성하고 토큰은 폼 데이터와 함께 리퀘스트 인증을 검증하는 데 사용합니다.

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```

`app.config` 딕셔너리는 어플리케이션 자체에서 사용하는 설정 변수들을 저장하기 위해 사용되는 공간입니다.

**SECRET_KEY** 설정 변수는 Flask 와 서드파티 확장에서 일반적인 암호화 키로 사용됩니다.

## Form Classes

Flask-WTF 를 사용할 때 각 웹 폼은 Form 클래스로부터 상속한 클래스에 의해 표현됩니다. 클래스는 폼에 있는 필드의 리스트를 정의하는데 이 필드는 각각 오브젝트로 표현됩니다. 각 필드 오브젝트는 하나 이상의 **검증자(validator)** 가 붙어 있습니다.

아래는 텍스트 필드와 서브밋 버튼을 갖는 웹 폼 입니다.

```python
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
  name = StringField('What is your name?', validators=[Required()])
  submit = SubmitField('Submit')
```

폼에 필드는 클래스 변수로 정의되며 각 클래스 변수는 필드 타입과 관계된 오브젝트로 할당됩니다.

`StringField` 클래스는 <input> 항목을 type="text" 속성으로 표현합니다. `SubmitField` 클래스는 <input> 항목을 type="submit" 속성으로 표현합니다.

`StringField` 생성자에 포함되어있는 validator 인수는 옵션이며, 사용자가 서브밋한 데이터를 받기 전에 적용하게 되는 체커들의 리스트를 정의합니다. `Required()` 검증자는 필드가 빈 공란으로 서브밋되지 않는 것을 보장한다.

> WTForms standard HTML fields

|Field Type|Description|
|:--|:--|
|StringField|Text field|
|TextAreaField|Multiple-line text field|
|PasswordField|Password text field|
|HiddenField|Hidden text field|
|DateField|Text field that accepts a `datetime.date` value in a given format|
|DateTimeField|Text field that accepts a `datetime.datetime` value in a given format|
|IntegerField|Text field that accepts an integer value|
|DecimalField|Text field that accepts a `decimal.Decimal` value|
|FloatField|Text field that accepts a floating-point value|
|RadioField|List of radio buttons|
|SelectField|Drop-down list of choices|
|SelectMultipleField|Drop-down list of choices with multiple selection|
|FileField|File upload field|
|SubmitField|Form submission button|
|FormField|Embed a form as a field in a container form|
|FieldList|List of fields of a given type|

> WTForms Validator

|Validator|Description|
|:--|:--|
|Email|Validates an email address|
|EqualTo|Compares the values of two fields; useful when requesting a password to be entered twice for confirmation|
|IPAddress|Validate an IPv4 network address|
|Length|Validates the length of the string entered|
|NumberRange|Validates that the value entered is within a numeric range|
|Optional|Allows empty input on the field, skipping additional validators|
|Required|Validates that the field contains data|
|Regexp|Validates the input against a regular expression|
|URL|Validates a URL|
|AnyOf|Validates that the input is one of a list of possible values|
|NoneOf|Validates that the input is none of a list of possible values|

## HTML Rendering of Forms 

폼 필드는 호출이 가능합니다. 이 폼 필드가 호출되면 테믈릿은 HTML 로 렌더링 됩니다.

뷰 함수는 NameForm 인스턴스를 form 이라는 이름을 갖는 인수로서 템플릿에 전달하여 간단한 HTML 폼을 생성합니다.

```html
{% raw %}
<form method="POST">
  {{ form.name.label}} {{ form.name() }}
  {{ form.submit() }}
</form>
{% endraw %}
```

id 필드나 class 속성을 주게 되면 CSS 스타일을 정의합니다.

```html
{% raw %}
<form method="POST">
  {{ form.name.label }} {{ form.name(id='my-text-field') }}
  {{ form.submit() }}
</form>
{% endraw %}
```
Flask-Bootstrap 은 전체 Flask-WTF 폼을 렌더링하기 위해 부트스트랩의 미리 정의된 폼 스타일을 사용하도록 하는 상위 레벨의 헬퍼 함수를 제공하는데, 이 모든 것이 한 번의 호출로 이루어집니다. Flask-Bootstrap 을 사용하면 이전 폼은 다음과 같이 렌더링됩니다.

```html
{% raw %}
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
{% endraw %}
```

`import` 는 일반적인 파이썬 스크립트가 하는 작업과 동일하며 템플릿 엘리먼트가 임포트되고 다른 템플릿에서 사용되도록 해줍니다. 임포트된 *bootstrap/wtf.html* 파일은 부트스트랩을 사용하여 Flask-WTF 폼을 렌더링하도록 하는 헬퍼 함수를 정의합니다.

`Wtf.quick_form()` 함수는 Flask-WTF 폼 오브젝트를 받아서 디폴트 부트스트랩 스타일을 사용하여 렌더링합니다. hello.py 의 전체 템플릿은 아래와 같습니다.

```html
{% raw %}
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky{% endblock %}

{% block page_content %}
<div class="page-header">
  <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
{% endraw %}
```

템플릿의 컨텐츠 영역은 2 개의 섹션으로 나누어져 있습니다. 첫 번재 섹션은 페이지 헤더이며 인사말을 보여줍니다. 여기서 템플릿은 조건문을 사용합니다.

Jinja2 의 조건문은 `{% if variable %} ... {% else %} ... {% endif %}` 와 같은 포맷을 가집니다.

`name` 템플릿 인수가 정의되지 않으면 예제 템플릿은 문자열 *Hello, Stranger!* 를 렌더링합니다. 컨텐츠의 두 번째 섹션은 `wtf.quick_form()` 함수를 사용하여 NameForm 오브젝트를 렌더링 합니다.

## Form Handling in View Functions

폼을 렌더링하고 폼의 데이터를 받는 `index()` 뷰 함수를 보여주겠습니다.

```python
@app.route('/', methods=['GET', 'POST'])
def index():
  name = None
  form = NameForm()
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
  return render_template('index.html', form=form, name=name
```

`app.route` 데코레이터에 추가된 `methods` 인수는 Flask 에서 URL 맵의 GET 과 POST 리퀘스트를 위한 핸들러로 뷰 함수를 등록하도록 합니다. `methods` 가 주어지지 않으면 뷰 함수는 GET 리퀘스트만 처리하도록 등록 됩니다.

로컬 `name` 변수는 가능한 경우에 폼으로부터 받은 이름을 저장하는 데 사용됩니다. 이름을 알지 못하면 그 변수는 None 으로 초기화 됩니다. 뷰 함수는 폼을 표현하기 위해 이젠어 봤던 NameForm 클래스의 인스턴스를 생성합니다. 폼의 `validate_on_submit()` 메소드는 폼이 서브밋될 때 True 를 리턴하고 데이터는 모든 필즈 검증자에 의해 받아들여집니다. 다른 경우에는 `validate_on_submit()` 이 False 를 리턴합니다.

사용자가 폼을 제출할 때 데이터와 함께 서버는 POST 리퀘스트를 받습니다. `validate_on_submit()` 을 호출하면 `name` 필드에 붙어 있는 `Required()` 검증자가 호출됩니다. `name` 이 비어 있으면, 검증자가 값을 받게되고 `validate_on_submit()` 은 True 를 반환합니다.

아래 `Example 1` 은 폼이 브라우저에서 어떻게 작동하는지 보이는 예시들 입니다.

`Example 2` 은 새로운 이름을 제출한 상태이며, `Example 3` 은 검증에 실패한 상태입니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/74240822-0ff08500-4d1e-11ea-9226-adc2f97f6ebb.png)

> Example 2 

![image](https://user-images.githubusercontent.com/44635266/74240825-10891b80-4d1e-11ea-9650-c9eae0516b50.png)

> Example 3

![image](https://user-images.githubusercontent.com/44635266/74240827-1252df00-4d1e-11ea-9021-d9b9ecd44c74.png)

## Redirects and User Sessions

위에서 사용한 예제 경우 폼을 제출하고 새로고침을 하면 제출이 또 일어나서 폼 서브미션이 두 번 하게 되는 문제가 발생합니다.

이는 브라우저에서 마지막 리퀘스트를 반복하여 POST 리퀘스트가 다시 전송되서 생기는 분제입니다.

이를 위해 정상적인 응답 대신 **리다이렉트(redirect)** 와 함께 POST 리퀘스트에 대해 응답하는것입니다. 리다이렉트는 특별한 형태의 응답이며 HTML 코드로 되어 있는 문자열 대신 URL 을 가지고 있습니다.

브라우저가 이 응답을 받게되면 리다이렉트 URL 에 대한 GET 리퀘스트를 발생시키는데 이것이 보여지는 페이지 입니다. 하지만 사용자 입장에서는 리아티렉트를 사용했다고 알 수 는 없지만 마지막 리퀘스트가 GET 가 되어 새로고침 커맨드는 예상대로 동작합니다.

이러한 기법이 **Post/Redirect/Get pattern** 입니다.

이 방법은 2 번재 문제를 가지고 있습니다. 어플리케이션인 POST 리퀘스트를 처리할 때 사용자가 `form.name.data` 에 입력한 이름을 접근하게 됩니다. 그러나 리퀘스트가 끝나는 순간 폼 데이터는 사라집니다. POST 리퀘스트가 리다이렉트로 처리되므로 어플리케이션은 이름을 저장해두어야 하고, 따라서 리다이렉트 리퀘스트는 이름 데이터를 액세스하여 실제 응답을 만드는 데 사용합니다.

어플리케이션은 **사용자세션(user session)** 에 데이터를 저장하여 이후에 받게 되는 다른 리퀘스트에서 그 데이터를 기억합니다. 각각의 클라이언트에 대해 프라이빗 스토리지를 사용할 수 있습니다.

아래 예제는 리다이렉트와 사용자 세션을 구현한 새로운 버전의 `index()` 뷰 함수 입니다.

```python
from flask import Flask, render_template, session, redirect, url_for

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    session['name'] = form.name.data
    return redirect(url_for('index'))
 return render_template('index.html', form=form, name=session.get('name'))
```

이전의 예제에서는 로컬 `name` 변수는 폼에서 사용자가 입력한 이름을 저장하는 용도로 사용되었지만, 그 변수는 `session['name']` 으로 변경하여 리퀘스트 이후에도 사용할 수 있습니다.

올바른 폼 데이터와 함께 전송된 리퀘스트는 `redirect()` 를 호출하여 끝맺습니다. 이 `redirect()` 함수는 헬퍼 함수이며 인수로 리다이렉트할 URL 을 받습니다. 이 경우 사용되는 리다이렉트 URL 은 루트 URL 이기 때문에 응답은 `redirect('/)` 로 작성이 됩니다.

하지만 Flask 에서는 URL 생성함수인 `url_for()` 대신에 사용된것입니다. URL 을 생성할 때는 `url_for()` 함수가 더 좋은데 이 함수가 URL 맵을 이용하여 URL 을 생성하기 때문입니다. 따라서 이 함수를 사용하면 URL 이 정의된 라우터와 호환되는것을 보장받을 수 있습니다.

`url_for()` 에서 필요한 인수는 **Endpoint** 의 이름으로 각 라우트가 가지고 있는 내부 이름을 의미합니다. 기본적으로 라우트의 Endpoint 는 연결되어 있는 뷰 함수의 이름입니다. 이 예제에서 루트 URL 을 처리하는 뷰 함수가 `index()` 이므로 `url_for()` 에 주어진 이름은 `index` 입니다.

마지막 변경 사항은 `render_template()` 함수로, 이 함수는 `session.get('name')` 을 사용하여 세션으로부터 직접 `name` 인수를 얻어 옵니다. 일반적인 딕셔너리를 사용하여, 딕셔너리 키를 요구하는 `get()` 을 사용하면 찾을 수 없는 키로 인한 예외 상황을 피할 수 있습니다. 그것은 `get()` 이 키가 없을 때는 기본값으로 None 을 리턴하기 때문입니다.

## Message Flashing

유저가 웹 사이트에 로그인할 때 잘못된 아이디와 패스워드를 제출하면 올바르지 않은 메세지를 로그인 폼에 다시 렌더링하도록 응답하는걸 볼 수 있습니다.

Flask 에서는 이러한 기능을 포함하고 있습니다. 아래 예제는 `flash()` 함수의 목적으로 어떻게 사용되는지 보여줍니다.

```python
from flask import Flask, render_template, session, redirect, url_for, flash

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('index'))
 return render_template('index.html',
    form = form, name = session.get('name'))
```

이 예제에서는 저장된 이름과 비교해야 하는 이름이 제출될때마다 이전의 동일한 폼의 서브미션에 그 값을 유지합니다. 두 개의 이름이 다르면, `flash()` 함수는 클라이언트로 되돌려 보낸 다음 응답에 메세지를 보이도록 호출합니다.

`flash()` 호출 이외에도 메세지를 출력하기 충분하지 않습니다. 어플리케이션에서 사용되는 템플릿은 이러한 메세지를 렌더링 해야합니다. 플래시되는 메세지를 렌더링하는 데 가장 적합한 위치는 베이스 템플릿 입니다. 메세지가 모든 페이지에서 가능해야하기 때문입니다. Flask 에서는 `get_flashed_messages()` 함수가 템플릿에서 메세지를 추출하고 렌더링하도록 해줍니다.

```html
{% raw %}
{% block content %}
<div class="container">
  {% for message in get_flashed_messages() %}
  <div class="alert alert-warning">
    <button type="button" class="close" data-dismiss="alert">&times;</button>
    {{ message }}
  </div>
  {% endfor %}
  {% block page_content %}{% endblock %}
</div>
{% endblock %}
{% endraw %}
```

> Example 4

루프는 디스플레이될 여러 메세지가 있는 경우에 사용되고 `flash()` 는 이전 리퀘스트 사이클에서 호출됩니다. `get_flashed_messages()` 에서 추출된 메세지는 이 함수가 호출된 다음 번에는 리턴되지 않습니다. 따라서 플래시된 메세지는 오로지 한 번만 나오게됩니다.

