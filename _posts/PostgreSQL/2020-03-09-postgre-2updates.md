---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.8. Updates

`UPDATE` 명령을 사용하여 기존 데이터를 업데이트 할 수 있습니다. 다음 구문은 11 월 28 일 이후로 모든 데이터에 대하여 최고 / 최저 기온을 각각 2 도씩 낮추는 구문입니다.

```sql
UPDATE weather
    SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```

결과 데이터를 보겠습니다.

```sql
SELECT * FROM weather;

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
 Hayward       |      35 |      52 |      | 1994-11-29
(3 rows)
```