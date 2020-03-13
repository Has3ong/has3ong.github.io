---
title : PostgreSQL Chapter 3. Advanced Features
tags :
- PostgreSQL
---

## 3.6 Inheritance

상속은 객체 지향 데이터베이스의 개념입니다. 데이터베이스 디자인의 새로운 가능성을 보여줍니다.

2 개의 테이블 `cites` 와 `capitals` 을 만들어보겠습니다. 수도도 도시입니다. 여기서 테이블 상속 개념이 나옵니다. 예전이면 다음과 같이 테이블을 만들었을겁니다.

```sql
CREATE TABLE capitals (
  name       text,
  population real,
  altitude   int,    -- (in ft)
  state      char(2)
);

CREATE TABLE non_capitals (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE VIEW cities AS
  SELECT name, population, altitude FROM capitals
    UNION
  SELECT name, population, altitude FROM non_capitals;
```

쿼리는 정상적으로 작동하지만, 여러 행을 업데이트해야할 경우에는 난감합니다.

더 좋은 해결방법은 다음과 같습니다.

```sql
CREATE TABLE cities (
  name       text,
  population real,
  altitude   int     -- (in ft)
);

CREATE TABLE capitals (
  state      char(2)
) INHERITS (cities);
```

위 경우 `capitals` 테이블은 부모 테이블은 `cities` 로부터 (`name`, `population`, `altitude`) 속성을 모두 상속받습니다. `name` 칼럼의 `text` 자료형은 PostgreSQL 에서 사용하는 고유한 가변길이 문자열 자료형입니다. PostgreSQL 에서 테이블은 하나도 상속받지 않거나 여러개의 다른 테이블에서 상속받을 수 있습니다.

예를 들어 아래의 쿼리는 `capitals` 를 포함한 500 피트 이상의 고도에 있는 모든 `cities` 의 이름을 찾습니다.

```sql
SELECT name, altitude
  FROM cities
  WHERE altitude > 500;
```

출력 결과는 다음과 같습니다.

```sql
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
 Madison   |      845
(3 rows)
```

다음 쿼리는 `capitals` 가 아니고 500 피트 이상의 고도에있는 모든 도시를 찾습니다.

```sql
SELECT name, altitude
    FROM ONLY cities
    WHERE altitude > 500;
```

```sql
   name    | altitude
-----------+----------
 Las Vegas |     2174
 Mariposa  |     1953
(2 rows)
```

이 `ONLY` 예약어는 앞에서 이야기한 모든 자료 조작 명령 — `SELECT`, `UPDATE`, `DELETE` — 에서 그대로 적용됩니다. 물론 제외하면, 그 테이블의 하위 테이블 모두 적용됩니다.

> Note : 테이블 상속 기능은 이렇게 유용함에도 불구하고, 유니크 제약조건, 외래키 같은 부분에서 그리 깔끔한 해결책을 제시하고 있지는 못합니다. 보다 자세한 사항은 [Section 5.10]() 절 에서 다루고 있습니다.