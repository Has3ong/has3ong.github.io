---
title : Flask Large Application Structure
tags :
- Structure
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

대부분의 웹 프레임워크와는 달리, Flask 는 거대한 프로젝트를 위해 특정 구조를 사용할 것을 요구하지 않습니다. 어플리케이션의 구조 자체는 전적으로 개발자의 몫입니다.

## Project Structure 

아래는 Flask 어플리케이션의 기본적인 레이아웃을 보여줍니다.

```shell
|-flasky
  |-app/
    |-templates/
    |-static/
    |-main/
      |-__init__.py
      |-errors.py
      |-forms.py
      |-views.py
    |-__init__.py
    |-email.py
    |-models.py
  |-migrations/
  |-tests/
    |-__init__.py
    |-test*.py
  |-venv/
  |-requirements.txt
  |-config.py
  |-manage.py
```

위 구조는 4 개의 최상위 - 레벨 폴더로 구성되어 있습니다.

* app
  * Flask 어플리케이션이 존재
* migrations
  *  데이터베이스 마이그레이션 스크립트를 포함
* tests
  * 유닛 테스트 작성되는 디렉토리
* venv
  * 파이썬 가상환경을 포함
  
그리고 4 4개의 파일도 있습니다.

* requirements.txt
  * 패키지 의존성 리스트
* config.py
  * 설정값을 저장 
* manage.py
  * 어플리케이션과 다른 어플리케이션의 태스크를 실행

## Configuration Options 

어플리케이션은 종종 여러 설정값이 필요한데, 개발, 테스트, 배포 과정 중에 서로 다른 데이터베이스를 사용해야 하는 경우가 대표적인 예입니다. 이 데이터베이스들은 서로 간섭해서는 안됩니다.

*hello.py* 에서 사용된 간단한 딕셔너리 형태의 구조를 가진 설정 대신에 설정 클래스의 계층 구조 형태가 사용될 수 있습니다. 아래 예제는 *config.py* 파일입니다.

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
 
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
```

`Config` 베이스 클래스는 모든 설정에 사용하는 공통값들을 퐇마하고 있습니다. 서로 다른 서브 클래스는 특정 설정에 대한 값을 정의합니다. 그 외 설정이 필요하면 추가할 수 있습니다.

좀 더 호환성 있고 안전하게 설정하려면 몇 가지 설정을 환경 변수에서 옵션으로 임포트해야 합니다. 예를 들어, 민감한 상황에서 필요한 `SECRET_KEY` 의 값은 환경에 설정되지만 환경에 정의되어 있지 않은 경우 기본값이 제공됩니다.

`SQLALCHEMY_DATABASE_URI` 변수는 3 개의 설정에 따라 각각 서로 다른 값으로 할당됩니다. 이것은 어플리케이션이 서로 다른 데이터베이스와 다른 설정에서 동작하도록 해줍니다.

`Configuration` 클래스는 `init_app()` 클래스 메소드를 정의하며 이 메소드는 어플리케이션 인스턴스를 인수로 받습니다. 여기서 설정에 따른 초기화가 수행됩니다. 베이스인 `Config` 클래스는 비어 있는 `init_app()` 메소드를 구현합니다.

설정 스크립트 아랫부분에 다른 설정 정보를 `config` 딕셔너리로 등록합니다.

## Application Package 

어플리케이션 패키지는 어플리케이션의 코드, 템플릿, 정적 파일이 위치하는 곳입니다. 보통 간단하게 **app** 이라 하지만 필요한 경우 어플리케이션의 특성에 맞는 이름으로 생성할 수 있습니다.

*teampltes* 와 *static* 폴더는 어플리케이션 패키지의 일부로 **app** 안으로 이동합니다. 데이터베이스 모델과 이메일 지원 역시 이 패키지 안으로 이동하며 자신의 모듈에서 각각 *app/models.py* 와 *app/email.py* 라는 이름으로 존재합니다.

### Using an Application Factory

어플리케이션을 하나의 파일 버전으로 생성하면 편리하지만 큰 단점이 따릅니다. 어플리케이션이 전역 영역에 생성되어 동적으로 설정 변경을 적용할 방법이 없다는 것입니다. 스크립트를 실행하는 시간에 어플리케이션 인스턴스가 생성되어 있어 설정 변경을 할 수 없기 때문입니다.

이 문제에 대한 해결책은 어플리케이션을 **팩토리 함수(Factory Function)** 안으로 이동시켜 어플리케이션의 생성을 지연시키는 방법입니다. 이 팩토리 함수는 스크립트에서 직접 호출됩니다. 이 방법은 스크립트 시간에 설정할 수 있도록 해 줄 뿐만 아니라 여러 어플리케이션 인스턴스를 생성할 수 있게 해줍니다. 때로는 이 방법이 테스트 중에 매우 유용합니다.

이 생성자는 사용할 대부분의 Flask 확장을 임포트 하지만 그 확장을 초기화해야 하는 어플리케이션 인스턴스가 없기 때문에 생성자 자체에는 아무 인수도 넘기지 않고 초기화하지 않은 상태로 생성합니다.

`create_app()` 함수는 어플리케이션 팩토리 함수이며 어플리케이션에서 사용할 설정 이름을 인수로 가집니다. *config.py* 에 정의된 클래스 중 하나에 저장되는 설정값은 Flask 의 *app.config* 설정 오브젝트에서 사용 가능한 `from_object()` 메소드를 사용하여 어플리케이션에서 직접 임포트합니다.

설정 오브젝트는 `config` 딕셔너리에서 이름으로 선택됩니다. 어플리케이션이 한 번 생성되고 설정되면 확장이 초기화됩니다. 미리 생성한 확장에서 `init_app()` 을 호출하면 초기화가 완료됩니다.

```python
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    # attach routes and custom error pages here

    return app
```

팩토리 함수는 생성된 어플리케이션 인스턴스를 리턴하지만, 현재 상태에서 팩토리 함수와 함께 생성한 어플리케이션은 아직 완전하지 않습니다. 이 어플리케이션에는 라우트와 커스텀 에러 페이지 핸들러가 빠져있습니다.

### Implementing Application Functionality in a Blueprint

어플리케이션 팩토리 변환은 복잡합니다. 하나의 스크립트로 된 어플리케이션에서 어플리케이션 인스턴스가 전역 영역에 존재하기 때문에 라우트는 `app.route` 데코레이터를 사용하여 쉽게 정의됩니다. 그러나 어플리케이션이 런타임에 생성되면 `app.route` 데코레이터는 `create_app()` 이 실행된 이후에만 존재할 수 있습니다. 따라서 이러한 방식은 너무 늦습니다.

Flask 에서는 **블루프린트(Blueprints)** 를 사용하여 해결책을 제공합니다. 블루프린트는 라우트를 정의하는 어플리케이션과 비슷합니다. 차이점은 블루프린트와 관련된 라우트는 블루프린트가 어플리케이션과 함게 등록될 때까지 휴면상태라는 점입니다.

어플리케이션과 함께 등록되는 시점에서 라우트도 어플리케이션의 한 부분이 됩니다. 전역 영역에 정의된 블루프린트를 사용하면 어플리케이션의 라우트는 하나의 스크립트로 되어 있는 어플리케이션과 거의 같은 방법으로 정의할 수 있습니다.

어플리케이션과 마찬가지로 블루프린트는 하나의 파일에 정의할 수 있고, 패키지 안의 다중 모듈과 함께 좀 더 구조화된 방법으로 생성할 수 있습니다. 호환성을 극대화하기 위해 어플리케이션 패키지 내부 서브패키지가 블루프린트를 호스트하도록 생성할 수 있습니다.

아래 예제는 패키지 생성자가 블루프린트를 생성하는것을 보여줍니다.

```python
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
```

`Blueprint` 클래스의 오브젝트를 인스턴스화 하여 생성합니다. 이 클래스의 생성자는 2 개의 인수가 필요한데, 하나는 블루프린트 이름이고 다른 하나는 블루프린트가 위치하게 될 모듈이나 패캐지입니다. 어플리케이션과 마찬가지로 Python 의 `__name__` 변수를 사용하면 대부분의 경우 두 번째 인수에 올바른 값을 사용할 수 있습니다.

어플리케이션의 라우트는 패키지 안의 *app/main/views.py* 에 저장되며, 에러 핸들러는 *app/main/erros.py* 에 저장됩니다. 이 모듈들을 임포트하여 라우트와 에러 핸들러를 블루프린트와 연결시킵니다. 원형 의존성을 피하기 위해 모듈들을 *app/__init__.py* 의 아래 부분에 임포트해야 하는 점이 중요합니다. *views.py* 와 *erros.py* 는 메인 블루프린트를 임포트 해야합니다.

아래 예제는 `create_app()` 팩토리 함수내 블루프린트를 등록시키는겁니다.

```python
def create_app(config_name):
    # ...
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
```

아래 예제는 에러 핸들러입니다.

```python
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

블루프린트 내에서 에러 핸들러를 작성할 때 차이점은 `errorhandler` 데코레이터를 사용하면 핸들러가 단지 블루프린트에서 발생한 에러에만 호출된다는 점입니다. 어플리케이션 레벨의 에러 핸들러를 설치하기 위해서는 `app_errorhandler` 를 사용해야 합니다.

아래 예제는 블루프린트에서 업데이트된 어플리케이션의 라우터를 보여줍니다.

```python
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template(
        'index.html',
        form=form, name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow()
    )
```

블루프린트 내 뷰 함수를 작성할 때는 2 가지 중요한 차이점이 있습니다. 첫째, 앞에서 본 에러 핸들러의 경우처럼 라우트 데코레이터가 블루프린트로부터 오게됩니다. 또 다른 차이점은 `url_for()` 함수의 사용입니다. 이 함수에 대한 첫 번째 인수는 라우트의 종단 이름이며 어플리케이션 기반의 라우트는 뷰 함수의 이름을 기본값으로 합니다.

예를 들어, 하나의 스크립트로 된 어플리케이션에서 `index()` 뷰 함수를 위한 URL 은 `url_for('index')` 로 얻을 수 있습니다.

블루프린트를 사용할 때의 차이점은 Flask 가 블루프린트로부터 온 모든 종단점에 네임스페이스를 적용하는 점입니다. 따라서 여러 블루프린트는 충돌 없이도 같은 종단점 이름을 가지는 뷰 함수들을 정의할 수 있습니다. 네임 스페이스는 블루프린트의 이름이며, 따라서 `index()` 뷰 함수는 종단점 이름 `main.index` 와 함께 등록되고 URL 은 `url_for('main.index')` 를 사용하여 얻습니다.

`url_for()` 함수는 블루프린트 내에서 종단점을 위해 블루프린트 이름이 생략된 더 짧은 포맷도 지원합니다. 예를 들면 `url_for('.index')` 와 같은 포맷입니다. 이와 같은 형식을 사용하면 현재 리퀘스트에 블루프린트를 사용할 수 있습니다. 이 방법은 블루프린트에 대한 리다이렉트가 네임스페이스 종단 이름을 사용해야만 하기 때문에 같은 블루프린트를 갖는 리다이렉트를 더 짧은 형태로 사용할 수 있기 때문에 효과적입니다.

어플리케이션 패키지의 변경 사항을 완성하기 위해 폼 오브젝트는 또한 *app/main/forms.py* 모듈에 있는 블루프린트 내에 저장되기도 합니다.

## Launch Script 

최상위 레벨 폴더에 있는 *manage.py* 파일은 어플리케이션을 시작할 때 사용됩니다.

```python
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

스크립트는 어플리케이션을 생성하면서 시작합니다. 사용된 설정은, 정의되어 있다면 환경 변수 `FLASK_CONFIG` 에서 가져옵니다. 정의되어있지 않으면 디폴트 설정이 사용됩니다.

좀 더 편리하게 사용할 수 있도록 몇 개의 라인이 추가되어 유닉스 기반 운영체제 스크립트인 *./manage.py* 가 `python manage.py` 형태 대신 실행될 수 있습니다.

## Requirements File 

어플리케이션은 정확한 버전 넘버를 포함하여 모든 패키지 의존성을 기록한 *requirements.txt* 파일을 포함해야합니다. 가상 환경의 경우 컴퓨터에서 재생성해야 하기 때문입니다. 이 파일은 다음 커맨드와 같이 `pip` 를 이용하여 자동으로 생성할 수 있습니다.

```shell
(venv) $ pip freeze > requirements.txt
```

패키지가 설치되거나 업그레이드될 때마다 이 파일을 새로고침하는 것이 좋습니다. *requirements.txt* 의 예제는 다음과 같습니다.

```shell
Flask==0.10.1
Flask-Bootstrap==3.0.3.1
Flask-Mail==0.9.0
Flask-Migrate==1.1.0
Flask-Moment==0.2.0
Flask-SQLAlchemy==1.0
Flask-Script==0.6.6
Flask-WTF==0.9.4
Jinja2==2.7.1
Mako==0.9.1
MarkupSafe==0.18
SQLAlchemy==0.8.4
WTForms==1.0.5
Werkzeug==0.9.4
alembic==0.6.2
blinker==1.3
itsdangerous==0.23
```

가상 환경을 완벽하게 복사할 필요가 있을 때 새로운 가상 환경을 생성하고 다음과 같은 커맨드로 실행할 수 있습니다.

```shell
(venv) $ pip install -r requirements.txt
```

## Unit Tests

이 어플리케이션은 너무 작아 많은 테스트를 할 수 없지만, 두 개의 간단한 테스트를 정의해보겠습니다.

```python
import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
 
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
 
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

이 테스트는 Python 표준 라이브러리에서 제공하는 표준 `unittest` 패키지를 사용하여 작성되었습니다. `setup()` 과 `tearDown()` 메소드는 각각의 테스트 앞과 뒤에서 실행하며 테스트하려는 메소드는 `test_` 로 시작하도록 이름을 붙이면 됩니다.

`setup()` 메소드는 실행하는 어플리케이션의 복사본을 테스트하기 위한 환경을 생성합니다. 먼저 테스트를 위해 어플리케이션을 생성하고 그 컨텍스트를 활성화합니다. 이 과정은 일반적인 리퀘스트와 마찬가지로 테스트가 `current_app` 을 액세스 하게 도와줍니다. 따라서 필요한 경우 테스트에 사용할 브랜드별 새 데이터베이스를 생성합니다. 데이터베이스와 어플리케이션 컨텍스트는 `tearDown()` 메소드에서 삭제됩니다.

첫 번째 테스트는 어플리케이션 인스턴스가 존재하는지를 확인합니다. 두 번째 테스트는 어플리케이션이 테스트 설정 내에서 실행되는지 확인합니다. 적절한 패키지에 *tests* 폴더를 만들기 위해선 *tests/__init__.py* 파일 추가가 필요합니다. `unittest` 패미지가 모든 모듈을 스캔하고 테스트를 위치시킵니다.

유닛 테스트를 실행하기 위해 커스텀 커맨드를 *manage.py* 스크립트에 추가합니다. 아래는 `test` 커맨드를 추가하는 방법입니다.

```python
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```

`manager.command` 데코레이터는 커스텀 커맨드를 구현하기 위해 간단하게 만듭니다. 데코레이트 함수의 이름은 커맨드 이름으로 사용되며 함수의 `docstring` 은 헬프메세지에 나타납니다. `test()` 함수의 구현은 `unittest` 패키지로부터 테스트 러너를 호출합니다.

유닛 테스트는 다음과 같이 실행됩니다.

```shell
(venv) $ python manage.py test
test_app_exists (test_basics.BasicsTestCase) ... ok
test_app_is_testing (test_basics.BasicsTestCase) ... ok

.----------------------------------------------------------------------
Ran 2 tests in 0.001s
OK
```

## Database Setup

데이터베이스 URL 은 첫째로 환경 변수로부터 얻어 오며 디폴트는 SQLite 데이터베이스입니다. 개발 설정에서는 URL 을 환경 변수인 `DEV_DATABASE_URL` 에서 얻어 오며, 정의되어 있지 않으면 SQLite 데이터베이스에는 *data-dev.sqlite* 이름이 사용됩니다.

데이터베이스 URL 의 소스와 상관없이 데이터베이스 테이블은 새로운 데이터베이스를 위해 생성되야 합니다. Flask-Migrate 를 사용하여 마이그레이션을 유지하도록 작업할 때 데이터베이스 테이블은 한 개의 커맨드를 사용해 최신 버전으로 생성하거나 업그레이드 합니다.

```shell
(venv) $ python manage.py db upgrade
```