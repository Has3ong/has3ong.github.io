---
title : Flask Email
tags :
- Email
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

파이썬 표준 라이브러리에서 제공하는 **smtplib** 패키지는 Flask 어플리케이션에서 이메일을 전송하는 데 사용되며, Flash-Mail 확장자는 smptlib 를 래퍼하고 Flask 에서 쉽게 사용할 수 있도록 통합되어 있습니다.

## Email Support with Flask-Mail 

Flask-mail 을 먼저 설치합니다.

```shell
(venv) $ pip install flask-mail
```

확장은 간단한 **메일 전송 프로토콜(Simple Mail Transfer Protocol, SMTP)** 서버와 연결하여 전송을 목적으로 이메일을 서버에 전달합니다. 설정이 주어져 있지 않으면 Flask-Mail 은 25 포트를 통해 localhost 와 연결하여 인증 없이 이메일을 전송합니다. 아래 표는 SMTP 서버를 설정하는 데 사용하는 설정키의 리스트를 보여줍니다.

|Key|Default|Description|
|:--|:--|:--|
|MAIL_HOSTNAME|localhost|호스트 이름 / 이메일 서버의 IP 주소|
|MAIL_PORT|25|이메일 서버의 포트|
|MIAL_USE_TLS|False|전송레이어보안의 보안을 활성화|
|MAIL_USE_SSL|False|보안 소켓 레이어의 보안을 활성화|
|MAIL_USERNAME|None|메일 계정의 사용자 이름|
|MAIL_PASSWORD|None|메일 계정의 패스워|

개발 중 외부 SMTP 서버를 연결하는 것이 더 편리할 수 있습니다. 아래 예제는 구글 지메일 계정을 통해 이메일을 전송하기 위한 어플리케이션 설정법입니다.

```python
import os
# ...
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```

Flask-Mail 은 아래와같이 초기화합니다.

```python
from flask.ext.mail import Mail
mail = Mail(app)
```

이메일 서버 사용자 이름과 패스워드를 보관하는 두 개의 환경 변수를 정의해야합니다.

```python
(venv) $ export MAIL_USERNAME=<Gmail username>
(venv) $ export MAIL_PASSWORD=<Gmail password>
```

### Sending Email from the Python Shell 

설정을 테스트하기 위해 쉘 세션을 시작하고 이메일을 테스트해보겠습니다.

```python
(venv) $ python hello.py shell
>>> from flask.ext.mail import Message
>>> from hello import mail
>>> msg = Message('test subject', sender='you@example.com',
... recipients=['you@example.com'])
>>> msg.body = 'text body'
>>> msg.html = '<b>HTML</b> body'
>>> with app.app_context():
... mail.send(msg)
...
```

Flask-Mail 의 `send()` 함수는 current_app 을 사용합니다. 따라서 활성화된 어플리케이션 컨텍스트에서 실행되어야 합니다.

### Integrating Emails with the Application 

매번 수작업으로 이메일 메세지를 생성하는 번거로움을 피하기 위해 어플리케이션의 이메일 전송 기능을 함수로 추상화하는것이 좋은 아이디어 입니다. 이 함수는 높은 호환성에 기반하여 Jinja2 템플릿으로부터 이메일 본문을 렌더링합니다. 아래 예제를 참고하면 됩니다.

```python
from flask.ext.mail import Message

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg)
```

함수는 두 개의 어플리케이션에 따른 설정키에 의존적입니다. 하나는 주제를 위한 문자열을 정의하는 것이며, 다른 하나는 전송자로 사용될 주소를 정의하는것입니다. 

`send_email` 함수는 목적지 주소, 제목 라인, 이메일 본문을 위한 템플릿, 키워드 인수의 리스트를 가져옵니다. 템플릿 이름이 확장 없이 주어져야 하므로 2 개의 템플릿 버전은 플레인-텍스트 본문과 리치-텍스트 본문으로 사용됩니다.

호출자에 의해 넘겨진 키워드 인수는 `render_template()` 호출에 전달되어 이메일 본문을 생성하는 템플릿에 의해 사용됩니다.

`index()` 뷰 함수는 새로운 이름이 폼과 함께 수신될 때마다 관리자에게 이메일을 전송하도록 쉽게 확장할 수 있습니다. 아래 예제는 이러한 변경사항을 보여줍니다.

```python
# ...
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
# ...
@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
      if user is None:
        user = User(username=form.name.data)
        db.session.add(user)
        session['known'] = False
        if app.config['FLASKY_ADMIN']:
          send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
      else:
        session['known'] = True
      session['name'] = form.name.data
      form.name.data = ''
      return redirect(url_for('index'))
    return render_template(
      'index.html',
      form=form,
      name=session.get('name'),
      known=session.get('known', False)
    )
```

이메일 수신자는 시작하는 동안 같은 이름의 설정 변수로 로드된 `FLASK_ADMIN` 환경 변수에서 얻게 됩니다. 두 개의 템플릿 파일이 이메일의 텍스트와 HTML 버전을 생성하는 데 필요합니다. 이 파일들은 **templates** 폴더 안의 **mail** 서브 폴더에 저장되어 일반적인 템플릿과 구별되어 보관됩니다.

사용자들은 이메일 템플릿이 템플릿 인수로 주어질 것을 기대하므로 `send_email()` 은 키워드 인수로 그것을 포함합니다.

앞에서 설명한 `MAIL_USERNAME` 과 `MAIL_PASSWORD` 환경 변수에 추가하여, 어플리케이션의 이 버전은 FLASK_ADMIN 환경 변수가 필요합니다.

```python
(venv) $ export FLASKY_ADMIN=<your-email-address>
```

이 환경 변수들이 설정되면 어플리케이션을 테스트하여 폼 안에 새로운 이름을 입력할 때마다 이메일을 수신할 수 있습니다.

### Sending Asynchronous Email 

이메일을 테스트해 보면 `mail.send()` 함수가 이메일이 전송되는 몇 초 동안 블록되는것을 확인할 수 있습니다. 이것은 그 시간동안 브라우저에서 아무 반응도 하지 않기 때문입니다.

리퀘스트 핸들링을 하는 동안 불필요한 지연을 피하기 위해, 이메일 전송 함수는 백그라운드 스레드로 처리되어야 합니다. 아래 예제는 그러한 변경사항을 보여줍니다.

```python
from threading import Thread

def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)
    
def send_email(to, subject, template, **kwargs):
  msg = Message(
    app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'],
    recipients=[to]
  )
  
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  thr = Thread(target=send_async_email, args=[app, msg])
  thr.start()
  return thr
```

많은 Flask 확장은 활성화된 어플리케이션과 리퀘스트 컨텍스트가 있다는 가정하에 동작합니다. Flask-Mail 의 `send()` 함수는 `current_app` 을 사용하여 어플리케이션 컨텍스트가 활성화될 것을 요구합니다. 그러나 `mail.send()` 함수가 다른 스레드에서 실행될 때는 어플리케이션 컨텍스트가 인위적으로 `app.app_context()` 를 생성해야합니다.

이메일 전송 작업을 하나의 작업으로 만들어 놓는 것이 이메일을 사용할 대마다 새로운 스레드를 시작하는 것보다 더 적합합니다.