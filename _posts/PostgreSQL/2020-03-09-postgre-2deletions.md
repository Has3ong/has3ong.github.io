---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.9. Deletions

`DELETE` 명령어를 이용해서 테이블 내의 데이터를 삭제할 수 있습니다. 더 이상 Hayward 날씨의 관심이 없다고 가정한 뒤, 테이블에서 해당 데이터를 삭제해보겠습니다.

```sql
DELETE FROM weather WHERE city = 'Hayward';
```

Hayward 에 관련된 모든 데이터는 삭제됩니다.

```sql
SELECT * FROM weather;
```

```sql
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
(2 rows)
```

다음과 같은 구문을 실행 할 때는 항상 조심 해야합니다.

```sql
DELETE FROM tablename;
```

권한 문제가 없다면 위 명령어는 테이블의 있는 모든 데이터를 삭제합니다. 또한, 시스템에서 확인 요청을 보내지 않습니다.