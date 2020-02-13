---
title : Database
tags :
- Database
- Python
- Flask
---

*이 포스트는 [Flask Web Development](https://github.com/gary136/ebook/blob/master/Flask%20Web%20Development.pdf)를 바탕으로 작성하였습니다.*

데이터베이스는 구조적인 방법으로 어플리케이션 데이터를 저장합니다. 데이터 베이스는 크게 **RDB(Relational DataBase)** 와 **NoSQL** 데이터베이스가 있습니다.

## SQL Databases 

관계형 데이터베이스는 **테이블(table)** 에 데이터를 저장하며 어플리케이션 도메인에 따라 다른 **엔티티(Entity)** 를 모델링합니다.

테이블은 고정된 수의 **열(column)** 과 변경 가능한 **행(row)** 로 구성됩니다. 열은 테이블에서 표현된 엔티티의 데이터 속성을 정의합니다. 예를 들어 **customers** 테이블은 **name, address, phone** 과 같은 열을 가집니다. 테이블의 각 행은 모든 열의 값으로 구성된 실제 데이터 항목을 정의합니다.

테이블은 **기본 키(primary key)** 라는 각 행을 위한 유일한 인식자를 가집니다. 또한 **외래 키(foreign key)** 라는 열도 있는데, 다른 테이블에서 다른 열의 기본키를 참조합니다. 열 사이의 링크는 **관계(relationship)** 라 하는데 이는 관계형 데이터베이스 모델의 기본이 됩니다.

아래 `Example 1` 은 2 개의 테이블로 이루어진 간단한 데이터베이스의 다이어그램을 보여줍니다. 2 개의 테이블을 연결한 라인은 테이블 사이의 관계를 표현합니다.

> Example 1 - Relational database example

![image](https://user-images.githubusercontent.com/44635266/74330057-556f8980-4dd4-11ea-967b-3895e5305d59.png)

`roles` 테이블의 `id` 키는 기본키이며 `users` 의 `role_id` 는 `roles` 테이블의 `id` 를 참조하는 외래키입니다.

2 개의 테이블을 같이 읽어 표한하기위해서는 **조인(join)** 을 해야합니다. 관계 데이터베이스 엔진은 필요할 때 테이블들 사이에 조인 오퍼레이션을 수행하도록 지원합니다.

## NoSQL Databases

앞에서 설명한 관계형 모델을 따르지 않는 데이터베이스를 NoSQL 이라 합니다. NoSQL 은 테이블을 대신하여 **컬렉션(collection)** 과 레코드 대신 **도큐먼트(document)** 를 사용합니다. NoSQL 에서는 조인을 전혀 사용하지 않습니다. 그리고 이 도큐먼트들은 **Key - Value** 의 **JSON** 구조를 가지고 있습니다.

NoSQL 데이터베이스 예제는 아래 `Example 2` 에 있습니다. 이것은 **역정규화(denormalization)** 라고 하는 오퍼레이션을 적용한 결과이며 이 결과 데이터 중복으로 인해 발생하는 테이블의 수를 감소시킵니다.

> Example 2 - NoSQL database example

![image](https://user-images.githubusercontent.com/44635266/74330055-53a5c600-4dd4-11ea-97c6-094d0887bf5d.png)

NoSQL 은 데이터가 중복되면 더 빠르게 쿼리를 실행할 수 있습니다. 사용자와 사용자 규칙은 조인이 필요 없기 때문에 직관적입니다.

## SQL or NoSQL? 

SQL 은 효율적이고 컴팩트한 형태에서 구조화된 데이터를 저장할 때 성능을 발휘하며 일관성을 유지하는 데 효과적입니다. 반면에 NoSQL 은 일관성 유지 측면에서 다소 약한편이어서 결국 성능 한계에 부딪히기도 합니다.

하지만 최근 빅데이터와 관련해서 NoSQL 이 각광을 받고 있습니다.

중소 규모의 어플리케이션에서는 SQL / NoSQL 모두 효율적입니다.

## Python Database Frameworks

파이썬은 오픈 소스와 상용 데이터베이스에 대한 대부분의 데이터베이스 엔진을 위한 패키지를 가지고 있습니다. *MySQL, Postgre, SQLite, Redis, MongoDB, CouchDB* 를 사용할 수 있습니다.

데이터베이스 프레임워크를 사용할 때 평가할 요소는 다음과 같습니다.

**Ease of use**

직관적인 데이터베이스 엔진과 데이터베이스 추상화 레이어를 비교할 때 후자가 더 우월합니다.

**Performance**

ORM 과 ODM 이 오브젝트 도메인을 데이터베이스 도메인으로 변환할 때 오버헤드가 생겨 성능저하가 생길 수 있습니다. 네이티브 데이터베이스 명령어로 직접 구현하여 최적화할 필요가 있는 특정한 오퍼레이션의 경우에 내부 데이터베이스에 대한 옵션 액세스를 제공하는 데이터베이스 추상화 레이어를 선택하는게 타당합니다.

**Portability**

데이터베이스를 선택할 때 유저의 개발과 제품 플랫폼에 사용 가능한지를 고려해야합니다.

**Flask Integration**

Flask 를 사용하여 통합할 프레임워크를 선택하는 것은 필수적이지는 않지만, 유저가 직접 통합 코드를 작성해냐 하는 부담을 줄일 수 있습니다.

현 포스트에서는 SQLAlchemy 를 이용해 보겠습니다.

## Database Management with Flask-SQLAlchemy

Flask-SQLAlchemy 는 Flask 어플리케이션 안에 있는 SQLAlchemy 의 사용을 간단하게 하는 Flask 확장 입니다.

`pip` 를 이용하여 설치하면 됩니다.

```shell
$ pip install flask-alchemy
```

Flask-SQLAlchemy 에서 데이터베이스는 URL 을 사용하여 설정합니다. 아래 표는 인기 있는 3 개의 데이터베이스 엔진을 위한 데이터베이스 URL 포맷 리스트입니다.

|데이터베이스 엔진|URL|
|:--|:--|
|MySQL|mysql://username:password@hostname/database|
|Postgre|postgresql://username:password@hostname/database|
|SQLite(Linux)|sqlite:////absolute/path/to/database|
|SQLite(Window)|sqlite:///c:/absolute/path/to/database|

이 URL 에서 `hostname` 은 MySQL 서비스를 호스트하는 서버를 참조하는데 **localhost** 나 리모트 서버가 될 수 있습니다. 데이터베이스 서버는 여러 데이터베이스를 호스트하므로 **database** 는 사용할 데이터베이스 이름을 가리킵니다. 인증을 위해 데이터베이스에 **username** 과 **password** 를 데이터베이스 사용자 자격으로 사용합니다.

어플리케이션 데이터베이스의 URL 은 Flask 설정 오브젝트에서 `SQLALCHEMY_DATABASE_URI` 키로 설정되어야 합니다. 다른 사용자 옵션은 설정키인 `SQLALCHEMY_COMMIT_ON_TEARDOWN` 인데 이 키는 True 로 설정하면 각 리퀘스트의 끝에 데이터베이스 변경의 자동 커밋을 가능하도록 해줍니다.

아래 예제는 간단한 SQLite 데이터베이스를 초기화하고 설정하는 방법을 보여줍니다.

```python
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
```

클래스 SQLAlchemy 에서 인스턴스화된 `db` 오브젝트는 데이터베이스를 표현하며 Flask-SQLAlchemy 에 대한 모든 기능을 액세스 할 수 잇도록 제공합니다.

## Model Definition 

**모델** 이라는 용어는 어플리케이션에서 아용되는 영구적인 엔티티를 참조할 때 사용합니다. ORM 의 컨텍스트에서 모델은 일반적으로 대응되는 데이터베이스 테이블의 열과 매칭되는 속성을 가지는 파이썬 클래스를 의미합니다.

Flask-SQLAlchemy 에서 데이터베이스 인스턴스는 모델을 위해 헬퍼 클래스의 집합과 이러한 구조를 정의하기 위해 사용하는 함수로 구성된 베이스 클래스를 제공합니다.

위 그림 `Example 1` 의 roles 와 users 테이블은 아래와같이 정의될 수 있습니다.

```python
class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  
  def __repr__(self):
    return '<Role %r>' % self.name
    
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
 
  def __repr__(self):
    return '<User %r>' % self.username
```

`__tablename__` 클래스 변수는 데이터베이스에 있는 테이블 이름을 정의합니다. 만약 이 변수가 생략이 되면 디폴트 값으로 들어가게 된다. 남아 있는 클래스 변수들은 모델의 속성이며 `db.Column` 클래스의 인스턴스로 정의됩니다.

아래는 일반적으로 사용하는 SQLAlchemy 열 타입 입니다.

|Type Name|Python Type|Description|
|:--|:--|:--|
|Integer|int|32 bit 일반적인 정수형|
|SmallInteger|int|16 bit 정수형|
|BigInteger|int / long|제한 없는 정확도의 정수형|
|Float|float|부동소수점 숫자|
|Numeric|decimal.Decimal|고정자릿수 숫자|
|String|str|가변 문자열|
|Text|str|가변 문자열 / 무제한 길이에 최적화|
|Unicode|unicode|가변 유니코드 문자열|
|UnicodeText|unicode|가변 유니코드 문자열 / 무제한 길이에 최적화|
|Boolean|bool|불린 값|
|Date|datetime.date|날짜 값|
|Time|datetime.time|시간 값|
|DateTime|datetime.datetime|날짜와 시간 값|
|Interval|datetime.timedelta|시간 간격|
|Enum|str|문자열 값의 리스트|
|PickleType|임의의 파이썬 오브젝트|자동 피클 직렬화|
|LargeBinary|str|바이너리 블롭(blob)|

`db.Column` 남은 인수들은 각 속성의 설정 옵션을 설정합니다. 아래는 사용 가능한 옵션 리스트 입니다.

|Option Name|Description|
|:--|:--|
|primary_key|True 설정 시, 열은 테이블의 기본키가 된다.|
|unique|True 설정 시, 중복 값을 허용하지 않는다.|
|index|True 설정시, 인덱스를 생성하므로 쿼리가 효율적이된다.|
|nullable|True 설정시, 빈 값을 허용한다.|
|default|열에 디폴트 값을 설정한다.|

## Relationships 

관계형 데이터베이스는 관계를 통해 서로 다른 테이블의 행들을 연결합니다. 그림 `Example 1` 은 **일대다(one-to-many)** 관계를 보여줍니다. 하나의 규칙은 많은 사용자에게 속해있고 사용자는 오직 하나의 규칙만을 가지는 의미입니다.

아래 예제는 일대다 관계가 어떻게 모델 클래스를 표현하는지 보여줍니다.

```python
class Role(db.Model):
  # ...
  users = db.relationship('User', backref='role')
  
class User(db.Model):
  # ...
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

외래키를 통해 2 개의 행을 연결합니다. `User` 의 모델에 추가된 `role_id` 열은 외래키로 정의되는데 이것은 관계를 만듭니다. `db.ForeignKey()` 에 전달한 `roles.id` 인수는 열이 `roles` 테이블에 있는 행에서 `id` 값을 가지는 것으로 해석되어야 합니다.

`db.relationship()` 에 대한 `backref` 인수는 `User` 모델에 `role` 속성을 추가하여 관계의 반대 방향을 정의합니다. 이 속성은 `Role` 모델이 외래키 대신 오브젝트에 접근하도록 `role_id` 대신 사용합니다.

아래 표는 `db.relationship()` 에서 사용할 수 있는 옵션 중 몇 가지를 나열한 것입니다.

|Option Name|Description|
|:--|:--|
|backref|관계에서 다른 모델에 있는 back reference 를 추가한다.|
|primaryjoin|모델 사이의 join 조건을 명확히한다.|
|lazy|관계된 아이템이 어떻게 로드되는지를 설정한다. select, immediate, joined, subquery, noload, dynamic 이 있습니다.|
|uselist|False 설정시 리스트 대신 스칼라를 사용한다.|
|order_by|관계에서 아이템을 위해 사용되는 순서로 설정한다.|
|secondary|다대다 관계에서 사용하기 위해 관계 테이블의 이름을 설정한다.|
|secondaryjoin|SQLAlchemy 가 결정하지 못할 때 다대다 관계를 위한 2 번째 조인 조건을 설정한다.|

관계에는 일대다 외에 다른 타입이 있습니다. **일대일** 관계는 표현 가능하지만 `userlist` 옵션을 사용하여 `db.relationship()` 정의에서 False 로 설정시 "다(Many)" 측이 "일(one)" 이됩니다. **다대다** 의 경우 **관련 테이블(association table)** 이라 하는 추가 테이블이 필요합니다.

## Database Operations

`Example 1` 의 데이터베이스 다이어그램에 따라 모델을 모두 설정하여 이제 사용할 준비가 됬습니다. 이 모델의 사용법을 배우는 가장 좋은 방법은 파이썬 쉘입니다. 다음은 공통적인 데이터베이스 오퍼레이션에 대해 알아보겠습니다.

### Creating the Tables 

가장 먼저 해야 할 작업은 Flask-SQLAlchemy 명령어를 사용해 모델 클래스에 기반한 데이터베이스를 생성하는 일입니다. `db.create_all()` 함수가 이 작업을 수행합니다.

```python
(venv) $ python hello.py shell
>>> from hello import db
>>> db.create_all()
```

어플리케이션 디렉토리를 체크하면 *data.sqlite* 라는 파일을 보게됩니다. 이름은 설정에 있는 SQLite 데이터베이스에 주어진 이름입니다. `db.create_all()` 함수는 데이터베이스 안에 존재할 경우 데이터베이스 테이블을 새로 생성하거나 업데이트 하지 않습니다. 이로인해 모델이 수정되거나 기존 데이터베이스에 적용되기 위해 불편할 수 있지만 주먹구구식 해결 방법은 테이블을 먼저 제거하는것입니다.

```python
>>> db.drop_all()
>>> db.create_all()
```

이 함수를 사용하면 모든 데이터를 파괴하기 때문에 사용하기 전에 주의해야합니다.

### Inserting Rows 

다음 예제는 몇 개의 `roles` 와 `users` 를 생성합니다.

```python
>>> from hello import Role, User
>>> admin_role = Role(name='Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name='User')
>>> user_john = User(username='john', role=admin_role)
>>> user_susan = User(username='susan', role=user_role)
>>> user_david = User(username='david', role=user_role)
```

모델을 위한 생성자는 키워드 인수로 모델 속성을 위한 초기값을 받아들입니다. 이 새로운 오브젝트의 id 속성은 명시적으로 설정하지 않습니다. 주요 키는 Flask-SQLAlchemy 에 의해 관리됩니다. 오브젝트는 아직 파이썬에만 존재하며 아직 데이터베이스에는 작성되지 않았습니다. id 값이 아직 설정되지 않았기 떄문입니다.

```python
>>> print(admin_role.id)
None
>>> print(mod_role.id)
None
>>> print(user_role.id)
None
```

데이터베이스에 대한 변경사항은 데이터베이스 **세션(session)** 을 통해 관리되는데 Flask-SQLAlchemy 는 `db.session` 으로 제공합니다. 데이터베이스 작성을 위해 오브젝트를 준비하기 위해서는 오브젝트가 세션에 추가되어야 합니다.

```python
>>> db.session.add(admin_role)
>>> db.session.add(mod_role)
>>> db.session.add(user_role)
>>> db.session.add(user_john)
>>> db.session.add(user_susan)
>>> db.session.add(user_david)
```

자세하게 작성하면 아래와 같습니다.

```python
>>> db.session.add_all([admin_role, mod_role, user_role,
... user_john, user_susan, user_david])
```

데이터베이스에 오브젝트를 작성하기 위해서는 세션이 `commit()` 메소드를 호출하여 **커밋(commit)** 해야합니다.

```python
>>> db.session.commit()
```

id 속성을 다시 체크하면 속성이 설정됩니다.

```python
>>> print(admin_role.id)
1
>>> print(mod_role.id)
2
>>> print(user_role.id)
3
```

데이터베이스 세션은 데이터베이스의 일관성을 유지하는 매우 유용한 방법입니다. 커밋 오퍼레이션은 자동으로 세션에 추가되는 모든 오브젝트를 작성합니다. 세션이 작성되는 동안 에러가 발생하면 전체 세션은 무시됩니다. 세션에 관련된 변경 사항을 함께 커밋하면 부분적인 업데이트로 인한 데이터베이스의 불일치성 회피가 보장됩니다.

> 데이터베이스 세션은 또한 **롤백(roll back)** 됩니다. `db.session.rollback()` 이 호출되면 데이터베이스 세션에 추가된 오브젝트는 이전 상태로 되돌아갑니다.

### Modifying Rows

데이터베이스 세션 `add()` 메소드는 모델을 업데이트하는 데도 사용됩니다. 같은 쉘 세션에서 다음 예제는 `Admin` role 을 `Administrator` 로 재명명합니다.

```python
>>> admin_role.name = 'Administrator'
>>> db.session.add(admin_role)
>>> db.session.commit()
```

### Deleting Rows

데이터베이스 세션은 `delete()` 메소드도 가지고 있습니다. 다음 예제는 데이터베이스에서 `Moderator` role 을 삭제합니다.

```python
>>> db.session.delete(mod_role)
>>> db.session.commit()

삽입 업데이트와 마찬가지로 삭제는 데이터베이스 세션이 커밋될 때만 실행합니다.
```

### Querying Rows

Flask-SQLAlchemy 는 각 모델 클래스에서 사용 가능한 query 오브젝트를 생성합니다. 모델을 위한 가장 기본적 쿼리는 그에 대응하는 테이블의 전체 내용을 리턴하는 것입니다.

```python
>>> Role.query.all()
[<Role u'Administrator'>, <Role u'User'>]
>>> User.query.all()
[<User u'john'>, <User u'susan'>, <User u'david'>]
```

쿼리 오브젝트는 `filters` 사용을 통해 더 정확한 데이터베이스 검색을 실행하도록 설정됩니다. 다음 예제는 User 규칙에 할당된 모든 사용자를 검색합니다.

```python
>>> User.query.filter_by(role=user_role).all()
[<User u'susan'>, <User u'david'>]
```

쿼리 오브젝트를 문자열로 변경하여 SQLAlchemy 는 주어진 쿼리를 위해 네이티브 SQL 쿼리를 조사할 수 있습니다.

```python
>>> str(User.query.filter_by(role=user_role))
'SELECT users.id AS users_id, users.username AS users_username,
users.role_id AS users_role_id FROM users WHERE :param_1 = users.role_id'
```

쉘 세션을 종료하면 이전 예제에서 생성된 오브젝트는 파이썬 오브젝트로서의 존재를 멈추고 데이터베이스 테이블에 있는 행으로 존재하게 됩니다. 새로운 쉘 세션을 시작한다면 데이터베이스 행에서 파이썬 오브젝트를 재생성해야 합니다. 다음 예제는 User 라는 이름의 사용자 규칙을 로드하는 쿼리를 호출합니다.

```python
>>> user_role = Role.query.filter_by(name='User').first()
```

`filter_by()` 와 같은 필터는 쿼리 오브젝트에서 호출되며 새로 정의된 쿼리를 리턴합니다. 다중 필터는 쿼리가 필요한대로 설정될 때까지 순차적으로 호출됩니다.

아래 표는 쿼리에서 사용하는 일반적인 필터의 일부입니다.

|Option|Description|
|:--|:--|
|filter()|원래 쿼리에 추가 필터를 더한 새로운 쿼리를 리턴|
|filter_by()|원래 쿼리에 추가된 동일한 필터를 더한 새로운 쿼리를 리턴|
|limit()|원래 쿼리의 결과 수를 주어진 수만큼 제한하는 새로운 쿼리를 리턴|
|offset()|원래 쿼리의 결과의 리스트에 옵셋을 적용하는 새로운 쿼리를 리턴|
|order_by()|주어진 영역에 따라 원래의 쿼리의 결과를 **정렬** 하는 새로운 쿼리를 리턴|
|group_by()|주어진 영역에 따라 원래의 쿼리의 결과를 **그룹** 하는 새로운 쿼리를 리턴|

원하는 필터를 쿼리에 적용한 후 `all()` 의 호출은 쿼리를 실행시키고 리스트와 같은 결과를 리턴합니다. 그러나 `all()` 외에 쿼리의 실행을 시작하는 다른 방법들도 있습니다.

|Option|Description|
|:--|:--|
|all()|쿼리의 결과를 모두 리스트로 리턴|
|first()|쿼리의 첫 번째 결과를 리턴|
|first_or_404()|쿼리의 첫 번째 결과를 리턴하거나 404 에러를 전송|
|get()|주어진 주요키에 매칭하는 행을 리턴|
|get_or_404()|주어진 주요키에 매칭하는 행을 리턴하거나 404 에러를 전송|
|count()|쿼리의 결과 카운트 리턴|
|paginate()|결과의 특정 영역을 포함하는 Pagination 오브젝트를 리턴|

관계는 쿼리에 비슷하게 동작합니다. 아래는 규칙과 사용자 사이의 일대다 관계에 대한 쿼리입니다.

```python
>>> users = user_role.users
>>> users
[<User u'susan'>, <User u'david'>]
>>> users[0].role
<Role u'User'>
```

`user_role.users` 쿼리는 작은 문제가 있습니다. 사용자의 리스트를 리턴하기위해 내부적으로 `all()` 의 호출을 실행할 때 묵시적으로 쿼리가 실행됩니다. 쿼리 오브젝트가 숨겨져 있기 때문에 추가적인 쿼리 필터를 이용하여 개선하는 것이 불가능합니다. 이 예제에서는 사용자 리스트가 알파벳 순서로 리턴되는 리퀘스트에 유용합니다.

아래 예제에서 관계 설정은 쿼리가 자동으로 실행되지 않도록 리퀘스트하기 위해 `lazy='dynamic'` 인수로 수정됩니다.

```python
class Role(db.Model):
  # ...
  users = db.relationship('User', backref='role', lazy='dynamic')
  # ...
```

이 방법으로 설정된 관계에서 `user_role.users` 는 아직 실행하지 않은 쿼리를 리턴합니다. 따라서 필터가 추가될 수 있습니다.

```python
>>> user_role.users.order_by(User.username).all()
[<User u'david'>, <User u'susan'>]
>>> user_role.users.count()
2
```

## Database Use in View Functions 

아래 예제는 데이터베이스에 사용자가 입력한 이름을 저장하는 홈페이지 라우트의 새로운 버전입니다.

```python
@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username = form.name.data)
      db.session.add(user)
      session['known'] = False
    else:
      session['known'] = True
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('index'))
  return render_template('index.html',
    form = form, name = session.get('name'),
    known = session.get('known', False))
```

어플리케이션 이름은 어플리케이션에 서브밋할 때마다 `filter_by()` 쿼리 필터를 사용하여 데이터베이스에 대해 확인합니다. `known` 변수는 사용자 세션에 작성되고, 리다이렉트 후에 정보는 템플릿으로 전송되어 인사말을 커스터마이징 하는 데 사용됩니다.

관계 템플릿의 새로운 버전은 아래 예제에 나타나있습니다. 이 템플릿은 인사말에 2 번째 라인을 추가하기 위해 `known` 인수를 사용합니다. 인사말은 `known` 과 새로운 사용자마다 다릅니다.

```html
{% raw %}
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Flasky{% endblock %}
{% block page_content %}
<div class="page-header">
  <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
  {% if not known %}
  <p>Pleased to meet you!</p>
  {% else %}
  <p>Happy to see you again!</p>
  {% endif %}
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
{% endraw %}
```

## Integration with the Python Shell 

쉘 세션이 시작할 때마다 데이터베이스 인스턴스와 모델을 임포트하는것은 귀찮습니다. 항상 이러한 반복을 피하기 위해 Flask-Script 의 쉘 커맨드는 특정 오브젝트를 자동으로 임포트 하기 위해 설정됩니다.

아래 예제는 임포트 리스트에 오브젝트를 추가하기 위해 `make_context` 콜백 함수를 등록하는 예제 입니다.

```python
from flask.ext.script import Shell
  
  def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
```

`make_shell_context()` 함수는 어플리케이션과 데이터베이스 인스턴스 모델을 등록합니다. 이것들은 자동으로 쉘에 임포트됩니다.

```shell
$ python hello.py shell
>>> app
<Flask 'app'>
>>> db
<SQLAlchemy engine='sqlite:////home/flask/flasky/data.sqlite'>
>>> User
<class 'app.User'>
```

## Database Migrations with Flask-Migrate 

어플리케이션 개발 과정에서 데이터베이스 모델을 변경하거나 데이터베이스를 업데이트해야 하는 경우가 있을 것입니다.

이 경우 **데이터베이스 마이그레이션** 프레임워크를 사용하면 테이블을 삭제하지 않고도 변경이 가능합니다. 이는 데이터베이스 **스키마(Schema)** 의 변경을 추적하여 추가된 변경 사항을 데이터베이스에 적용합니다.
 
### Creating a Migration Repository 

시작하기 전에 Flask-Migrate 가 설치되어 있어야합니다.

```shell
$ pip install flask-migrate
```

아래 예제는 확장을 초기화하는 코드입니다.

```python
from flask.ext.migrate import Migrate, MigrateCommand

# ...

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
```

데이터베이스 마이그레이션 커맨드를 보여 주기 위해 Flask-Migrate 는 Flask-Script 의 manager 오브젝트에 연결되어 있는 MigrateCommand 클래스를 보여줍니다.

데이터베이스 마이그레이션이 유지되기 전에 `init` 커맨드를 사용하여 마이그레이션 저장소를 생성해야 합니다.

```shell
(venv) $ python hello.py db init
 Creating directory /home/flask/flasky/migrations...done
 Creating directory /home/flask/flasky/migrations/versions...done
 Generating /home/flask/flasky/migrations/alembic.ini...done
 Generating /home/flask/flasky/migrations/env.py...done
 Generating /home/flask/flasky/migrations/env.pyc...done
 Generating /home/flask/flasky/migrations/README...done
 Generating /home/flask/flasky/migrations/script.py.mako...done
 Please edit configuration/connection/logging settings in
 '/home/flask/flasky/migrations/alembic.ini' before proceeding.
```

이 커맨드는 *migrations* 폴더를 생성하는데 이 폴더에는 모든 마이그레이션 스크립트가 저장될 것입니다.

### Creating a Migration Script 

Alembic 에서 데이터베이스 마이그레이션은 **마이그레이션 스크립트(migration script)** 로 표현됩니다. 이 스크립트는 `upgrade()` 와 `downgrade()` 라는 2 개의 함수를 갖고 있습니다. `upgrade()` 함수는 마이그레이션의 부분으로 데이터베이스 변경을 적용하고 `downgrade()` 함수는 그것들을 삭제합니다. 변경사항을 추가하고 삭제하는 기능을 갖고 있는 Alembic 은 변경 히스토리의 포인트에서 데이터베이스를 재설정합니다.

Alembic 마이그레이션은 revision / migrate 커맨드를 사용하여 각각 수동 / 자동으로 생성됩니다. 수동 마이그레이션은 비어 있는 `upgrade()` 와 `downgrade()` 함수를 가지는 마이그레이션 스켈레톤 스크립트를 생성하는데 이 함수들은 Alembic 의 Operations 오브젝트에 의해 제공되는 디렉티브를 사용하여 개발자가 구현해야 합니다.

자동 마이그레이션은 모델 정의와 데이터베이스의 현 상태 사이의 차이점을 찾아서 `upgrade()` 와 `downgrade()` 코드를 생성합니다.

`migrate` 커맨드는 자동 마이그레이션 스크립트를 생성합니다.

```shell
(venv) $ python hello.py db migrate -m "initial migration"
INFO [alembic.migration] Context impl SQLiteImpl.
INFO [alembic.migration] Will assume non-transactional DDL.
INFO [alembic.autogenerate] Detected added table 'roles'
INFO [alembic.autogenerate] Detected added table 'users'
INFO [alembic.autogenerate.compare] Detected added index
'ix_users_username' on '['username']'
 Generating /home/flask/flasky/migrations/versions/1bc
 594146bb5_initial_migration.py...done
```

### Upgrading the Database 

마이그레이션 스크립트를 검토하고 받아들이면, 스크립트는 `db upgrade` 커맨드를 사용하여 데이터베이스에 적용됩니다.

```shell
(venv) $ python hello.py db upgrade
INFO [alembic.migration] Context impl SQLiteImpl.
INFO [alembic.migration] Will assume non-transactional DDL.
INFO [alembic.migration] Running upgrade None -> 1bc594146bb5, initial migration
```

첫 마이그레이션을 위해서는 `db.create_all()` 을 호출하지만 이후의 마이그레이션에서는 `upgrade` 커맨드를 사용하여 컨텐츠에 영향을 주지 않고 테이블의 업데이트를 적용할 수 있습니다.

