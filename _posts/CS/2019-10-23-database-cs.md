---
title : DataBase
tags:
- SQL
- DDL
- DML
- DCL
categories:
- Computer Science
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

## SQL(Structed Query Language)

SQL은 구조적인 질의 언어라고 하며, 이 SQL이라는 질의 언어를 통해서 데이터베이스를 제어 관리한다.

SQL은 다음 언어로 나눌 수 있다.

DDL, DML DCL

### DDL (Data Definition Language)

데이터 베이스 스키마를 정의하거나 조작하기위해 사용한다.

```
CREATE, ALTER, DROP, TRUCATE
```

### DML (Data Manipulation Language)

데이터를 조작하기 위해 사용한다. 사용자가 응용 프로그램과 데이터 베이스 사이에 실질적인 데이터 처리를 위해서 사용한다.

```
SELECT, INSERT, DELETE, UPDATE
```

### DCL (Data Control Language)

데이터를 제어하는 언어이다. 데이터의 보안, 무결성, 회복, 병행 수행제어 등을 정의하는데 사용한다.

```
COMMIT, ROLLBACK, GRANT, REVOKE
```

### TCL (Transaction Control Language)

일부에서는 DCL 에서 트랜잭션을 제어하는 명령인 `COMMIT` 과 `ROLLBACK` 만을 따로 분리해서 TCL (Transaction Control Language) 라고 표현하기도 한다.


## Mysql vs MariaDB

MySQL이 오라클로 넘어간 뒤, 불확실한 라이선스 문제를 해결하려고 나온 오픈 소스 DBMS. 2009년에 MySQL AB 출신 개발자들이 따로 나와 MariaDB 재단을 세워서 개발하고 있다. 

MariaDB 5.5 버전은 MySQL 5.5 버전을 기반으로 포크했기 때문에 MySQL 5.5 버전과 거의 모든 기능이 호환된다. 

그 이후 나온 10.0 버전은 MySQL 5.6에서 업데이트된 기능을 반영한 버전이다. 10.1 버전은 MySQL 5.7에서 추가 및 변경된 기능을 반영하여 출시되었다. MySQL과의 호환성을 최대한 유지하면서 좀더 나은 성능을 구현하는 것이 주된 개발 방향인 듯하다. 10.2부터는 MySQL의 개발 속도를 앞서나가서 오히려 이쪽 기능이 MySQL로 역수출되고 있는 실정이다.

* MariaDB는 서브 쿼리와 조인 쿼리 최적화를 지원한다.
* MariaDB는 멀티 스레드 리플리케이션을 지원한다.
* MariaDB는 롤(ROLE) 기반의 권한 관리를 지원한다.
* MariaDB는 가상 칼럼과 동적 칼럼을 지원한다.

### 가상칼럼

* 다른 컬럼에 의해서 자동으로 설정되는 기능을 의미함.

### 동적칼럼

* NoSQL 형태의 데이터 저장 및 접근을 위해서 동적 칼럼 기능을 제공함.
* 하나의 대용량 컬럼 정의하고, 그 칼럼을 여러 개의 임의 칼럼으로 정의하여 사용가능

