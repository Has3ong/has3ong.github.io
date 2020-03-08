---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.3. Creating a New Table

모든 열 이름 및 유형과 함께 테이블 이름을 지정하여 새 테이블을 만들 수 있습니다.

```shell
CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
```


`psql` 에서 줄 바꿈을 입력할 수 있습니다. `psql` 은 `;` 세미콜론이 표시될 때 까지 명령이 종료되지 않았음을 인식할것입니다.

White Space(공백, 탭, 새로운 라인) 는 SQL 명령에서 자유롭게 사용할 수 있습니다. 위와 다르게 정렬된 명령어를 입력하거나 한 줄에 모두 입력할 수 있다는 의미입니다. 두 개의 대시(`--`) 는 주석(Comment) 입니다. 뒤에 나오는 문장은 모두 무시됩니다. SQL 은 주요 단어와 식별자에 대해 대소문자를 구분하지 않습니다. 하지만, 식별자가 사례 보존을 위해 이중 인용된 경우는 예외입니다.

`varchar(80)` 은 임의 문자열을 최대 80 자까지 저장할 수 있는 데이터 유형입니다. `int` 는 일반 정수형 타입입니다. `real` 은 단일 정밀 부동 소수점 숫자를 저장하는 유형입니다. `date` 는 자체 설명해야합니다.(속성의 이름과 데이터 형식의 이름 모두 똑같아서 혼란이 올 수 있습니다.)

PostgreSQL 은 `int`, `smallint`, `real`, `double precision`, `char(N)`, `varchar(N)`, `date`, `time`, `timestamp`, `interval` 말고도 일반 유틸리티와 풍부한 기하학적 유형도 지원합니다. PostgreSQL 은 사용자 정의 데이터 유형을 정의하여 사용할 수 있습니다. 따라서, SQL 표준에서는 특별한 경우를 지원하기 위해 필요한 경우를 제외하고는 구문에서 유형 이르미 키워드가 아닙니다.

두 번째 에제로는 도시와 관련 지리적 위치를 저장하는 테이블을 만들어 보겠습니다.

```shell
CREATE TABLE cities (
    name            varchar(80),
    location        point
);
```

`point` 타입은 PostgreSQL 의 특수한 데이터 타입입니다.

마지막으로 더 이상 테이블을 사용하지 않을때는 다음 명령어를 통해 삭제할 수 있습니다.

```shell
DROP TABLE tablename;
```