---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.7. Aggregate Functions

다른 관계형 데이터베이스와 마찬가지로 PostgreSQL 은 집계함수(aggregate function) 를 제공합니다. 집계 함수는 여러 데이터에 관해서 단일 결과를 계산하여 보여줍니다. 예를 들어, `count`, `sum`, `avg(average)`, `max(maxinum)`, `min(minimum)` 과 같은 함수가 있습니다.

최저기온을 기록한 데이터에서 가장 높은 값을 예시로 찾아보겠습니다.

```sql
SELECT max(temp_lo) FROM weather;
```

```sql
 max
-----
  46
(1 row)
```

위 데이터에 해당하는 도시 데이터를 조회하고 싶어서, 아래와 같이 시도했을수도 있습니다.

```sql
SELECT city FROM weather WHERE temp_lo = max(temp_lo);     WRONG
```

하지만, 집계함수 `max` 는 `WHERE` 절에서 사용할 수 없어서 작동하지 않습니다.(`max` 함수 자체가 데이터를 조회하지 않으면 나올 수 없는 값이기 때문에 `WHERE` 절에서 작동하지 않습니다.) 위 같은 문제는 `서브쿼리(subquery)` 를 사용해서 해결할 수 있습니다.

```sql
SELECT city FROM weather
    WHERE temp_lo = (SELECT max(temp_lo) FROM weather);
```

```sql
     city
---------------
 San Francisco
(1 row)
```

서브쿼리는 외부 쿼리에서 발생하는것과는 다르게 별도로 계산하기 때문에 사용해도 괜찮습니다. 집계 함수는 `GROUP BY` 절과 함께 사용하면 매우 유용합니다.

예를 들어, 각 도시에서 관찰되는 최저 기온의 최대값을 아래와 같이 조회할 수 있습니다.

```sql
SELECT city, max(temp_lo)
    FROM weather
    GROUP BY city;
```

```sql
     city      | max
---------------+-----
 Hayward       |  37
 San Francisco |  46
(2 rows)
```

또한, 집계된 데이터에 대해서 조건을 주어야할 때는 `HAVING` 구문을 사용하여 필터링할 수 있습니다.

```sql
SELECT city, max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

```sql
  city   | max
---------+-----
 Hayward |  37
(1 row)
```

아래 쿼리는 모든 `temp_lo` 값이 40 미만인 도시 데이터만 출력하는 구문입니다. 마지막으로 도시 이름이 "s" 로 시작되는 데이터만 찾습니다.

```sql
SELECT city, max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'            -- (1)
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

(1) `LIKE` 에 대한 패턴 매칭과 설명은 [Section 9.7]() 에 있습니다.

집계 함수를 사용 할 때는 `WHERE` 절과 `HAVING` 절의 관계를 반드시 숙지하고 있어야합니다. `WHERE` 절은 조회할 집계되지 않은 자료에 대한 조건이고, `HAVING` 은 집계된 자료에 대한 조건입니다. 그래서, `WHERE` 절의 조건으로 `HAVING` 절이 사용될 수 없고, `HAVING` 절 다음에는 집계 함수가 사용됩니다. 물론 더 깊게 이야기하면, `HAVING` 절에서 집계 함수를 사용안해도 되지만 효율적이지 않습니다. 같은 조건을 `WHERE` 절에서 사용하는게 더 효과적입니다.

앞 예제에서, 집계 작업을 하지 않고 `WHERE` 을 이용하여 조건을 주어 특정 데이터를 선별했습니다. 이것은 `HAVING` 예약어를 사용하는 방식보다 성능이 좋습니다. 왜냐하면, `WHERE` 절을 이용하면 집계 작업 대상 자체에서 제외하기 때문입니다.