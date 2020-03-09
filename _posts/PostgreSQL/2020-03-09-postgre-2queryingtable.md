---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.5. Querying a Table

테이블에서 데이터를 검색하려면 SQL `SELECT` 문을 사용하면 테이블에 쿼리하면 됩니다. 쿼리문은 **검색 목록(select list)** (반환할 칼럼을 나열하는 부분), **테이블 목록** (데이터를 검색할 테이블을 나열하는 부분), **옵션 자격(optional qualification)** (제약조건을 지정하는 부분) 으로 나뉜다. 예를 들어 모든 날씨 테이블의 모든 데이터(rows) 를 검색하려면 다음을 입력하시면 됩니다.

```sql
SELECT * FROM weather;
```

여기서 `*` 은 모든 칼럼의 줄임말 입니다. 그래서 같은 결과를 반환합니다.

```sql
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```

출력은 아래와 같이 될것입니다.

```sql
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
 Hayward       |      37 |      54 |      | 1994-11-29
(3 rows)
```

`SELECT` 문에서 단순 칼럼 참조가 아닌 식을 사용할 수 있습니다. 예를 들어 다음과 같은 작업을 수행할 수 있습니다.

```sql
SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;
```

출력은 아래와 같이 될것입니다.

```sql
     city      | temp_avg |    date
---------------+----------+------------
 San Francisco |       48 | 1994-11-27
 San Francisco |       50 | 1994-11-29
 Hayward       |       45 | 1994-11-29
(3 rows)
```

출력 데이에 레이블을 다시 지정하는 데 `AS` 절이 어떻게 사용되는지 주목하시면 됩니다. (`AS` 문은 선택사항입니다.)

쿼리는 원하는 칼을 지정하는 `WHERE` 절을 추가하여 "조건(qualified)" 을 얻을 수 있습니다. `WHERE` 절에는 부울식(truth value) 이 포함되어 있으며, 부울식이 참인 데이터만 반환됩니다. 일반적으로 부울 연산자(`AND`, `OR`, `NOT`) 들이 허용되어 사용할 수 있습니다.

예를 들어, 다음은 비오는 날의 **San Francisco** 의 날씨를 검색합니다.

```sql
SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```

결과

```sql
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)
```

아래 쿼리로 정렬된 결과를 반환할 수 있습니다.

```sql
SELECT * FROM weather
    ORDER BY city;
```

```sql
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 Hayward       |      37 |      54 |      | 1994-11-29
 San Francisco |      43 |      57 |    0 | 1994-11-29
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
```

위 예에서는 정렬 순서를 확실히 지정하지 않아서 **San Francisco** 행이 어떤 순서로든 나올 수 있습니다. 다음 쿼리로 항상 위에 표시하게 반환할 수 있습니다.

```sql
SELECT * FROM weather
    ORDER BY city, temp_lo;
```

아래 쿼리를 통해 중복된 값을 제거할 수 있습니다.

```sql
SELECT DISTINCT city
    FROM weather;
```

```sql
     city
---------------
 Hayward
 San Francisco
(2 rows)
```

또 다시, 결과 데이터 순서는 달라질 수 있습니다. `DISTINCT` 와 `ORDER BY` 를 함께 사용하여 일관된 결과를 보장할 수 있습니다.

```sql
SELECT DISTINCT city
    FROM weather
    ORDER BY city;
```