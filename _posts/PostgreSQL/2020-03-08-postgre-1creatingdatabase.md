---
title : PostgreSQL Chapter 1. Getting Started
tags :
- PostgreSQL
---

## 1.3. Creating a Database

첫번째 테스트는 데이터베이스 서버에 접속을해서 데이터베이스를 만들 수 있는지 시도해보겠습니다. PostgreSQL 서버는 많은 데이터베이스를 관리할 수 있습니다. 일반적으로 각각의 프로젝트나 사용자들은 데이터베이스를 따로 사용합니다.

아마, 관리자가 이미 사용을 위한 데이터를 만들어놨을수도 있습니다. 이 경우 이 단계를 생략하고 다음 섹션으로가면 됩니다.

위 예제에서는 `mydb` 라는 이름의 새로운 데이터베이스를 만들어 보겠습니다. 아래 명령어를 입력하면 됩니다.

```shell
$ createdb mydb
```

응답이 없을 경우 성공했다는 의미이므로 아래 단계들을 건너 뛰어도 됩니다.

만약 아래와 같은 메세지가 표시될 경우

```shell
createdb : command not found
```

PostgreSQL 이 설치가 안된겁니다. PostgreSQL 이 전혀 설치가 안되있거나 경로가 설정되지 않았거나 둘 중 하나입니다. 그러니 아래 절대 경로를 출력하는 명령어를 호출해보시면 됩니다.

```shell
$ /usr/local/pgsql/bin/createdb mydb
```

환경에 따라 경로가 달라질 수 있습니다. 그러니 관리자에게 문의하거나 설치 지침서를 확인하시면 됩니다.

또 다른 응답은 아래가 있습니다.

```shell
createdb: could not connect to database postgres: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
```

서버가 아직 시작이 안됐거나, `createdb` 가 예상된 곳에서 시작되지 않았다는 뜻입니다. 설치 지침서나 관리자에게 다시 확인해야 합니다.

또 다른 응답은 아래가 있습니다.

```shell
createdb: could not connect to database postgres: FATAL:  role "joe" does not exist
```

사용자 로그인 이름이 응답에 나타난 경우, 관리자가 당신을 위한 PostgreSQL 계정을 생성하지 않았을 때 발생합니다.(Postgre SQL 은 사용자 계정와 운영 체제 사용자 계정과 구분됩니다.) 당신이 만약 관리자라면 계정 생성에 대한 도움말은 **Chapter 21** 을 확인하면 됩니다. 첫 번째 사용자 계정을 생성하기 위해서는 당신이 PostgreSQL 이 설치된 운영체제의 사용자(일반적으로 `postgres`) 가 되어야합니다. 아니면 PostgreSQL 사용자 이름과 운영ㅊ제 사용자 이름과 다르게 할당 받았을 수도 있습니다. 이 경우에는 `-U` 태그를 이용해서 `PGUSER` 환경 변수를 당신의 PostgreSQL 이름으르 솔저앟면 됩니다.

사용자 계정이 있지만 데이터베이스를 추가할 권한이 없는 경우에는 다음 메세지를 보게될것입니다.

```shell
createdb: database creation failed: ERROR:  permission denied to create database
```

모든 사용자가 데이테비스를 만드는 권한이 있는것은 아닙니다. 만약 PostgreSQL 이 새로운 데이터베이스를 만드는것을 거부한다면, 당신의 관리자로부터 데이터베이스 생성 권한을 부여받아야합니다. 이 경어 관리자에게 문의를 해야합니다. 만약 PostgreSQL 튜톨리얼을 위해 직접 설치한 경우 사용자 계정으로 시작하면됩니다.

데이터베이스를 생성할 때 다른 이름으로 작성할 수 있습니다. PostgreSQL 을 사용하면 특정 사이트에 원하는 수의 데이터베이스를 만들 수 있습니다. 데이터베이스 이름은 무조건 알파벳으로 시작해야 하며 길이는 63 byte 로 제한됩니다. 가장 편리한 방법은 사용자 이름과 동일하게 작성하는것입니다. 많은 툴에서 데이터베이스 이름을 기본값으로 사용하면 입력하는것을 절약할 수 있습니다. 데이터베이스를 생성하려면 아래와 같이 명령어를 입력하면 됩니다.

```shell
$ createdb
```

더 이상 데이터베이스를 사용하지 않는다면 삭제할 수 있습니다. 예를 들어 `mydb` 를 생성한 경우 아래와 같은 명령어로 제거할 수 있습니다.

```shell
$ dropdb mydb
```

(위 명령어의 경우 데이터베이스 이름이 사용자 계정 이름으로 기본값으로 지정되어있지 않습니다. 그러므로 항상 명시해야 합니다.) 이 동작은 물리적으로 데이터베이스와 관련된 모든 파일을 제거하며, 실행 취소가 불가능합니다. 그렇기 때문에 충분히 심사숙고하고 실행해야합니다.

`createdb` 와 `dropdb` 에 대한 자세한 내용은 [createdb] 와 [dropdb] 에서 확인할 수 있습니다.


