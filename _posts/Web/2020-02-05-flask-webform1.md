---
title : Web Forms -1-
tags :
- Web Forms
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

`StringField` 클래스는 input 항목을 type="text" 속성으로 표현합니다. `SubmitField` 클래스는 input 항목을 type="submit" 속성으로 표현합니다.

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


