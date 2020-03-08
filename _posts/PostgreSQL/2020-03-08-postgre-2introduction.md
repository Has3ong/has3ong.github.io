---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.1. Introduction

이 장에서는 SQL을 사용하여 간단한 작업을 수행하는 방법에 대한 개요를 제공하겠습니다. 이 튜토리얼은 소개를 할 용도지 완전한 튜톨리얼이 아닙니다. SQL에는 [melt93](https://www.postgresql.org/docs/12/biblio.html#MELT93), [date97](https://www.postgresql.org/docs/12/biblio.html#DATE97) 등 수많은 책이 쓰여져 있습니다. 어떤 PostgreSQL 은 SQL 언어 기능은 표준 확장 기능입니다.

다음 예에서, 이전 장에서 설명한 바와 같이 `mydb` 데이터베이스를 만들었고, `psql` 을 시작한다고 가정하겠습니다.

이 설명서의 예는 PostgreSQL 에서도 찾을 수 있습니다. 디렉토리 *src/tutorial/.*  (Binary PostgreSQL 파일은 컴파일되지 않을 수 있습니다.) 이 파일을 사용하려면 먼저 해당 디렉토리로 변경하고 다음 명령어를 실행하면됩니다.

```shell
$ cd ..../src/tutorial
$ make
```

위 명령어를 실행하면 스크립트가 생성되고 사용자 정의 기능과 유형이 포함된 C 파일이 컴파일됩니다. 그런 다음, 튜톨리얼을 실행하려면 다음을 수행하면됩니다.

```shell
$ cd ..../tutorial
$ psql -s mydb

...


mydb=> \i basics.sql
```

`\i` 명령어는 지정된 파일의 명령어를 읽습니다. `psql` 의 `-s` 옵션은 각 명령문을 서버로 보내거진에 **단일 단계 모드(Single Step Mode)** 에 머물게 합니다. 이 예제에 사용된 명령은 *basic.sql* 파일에 있습니다.


