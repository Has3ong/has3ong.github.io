---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.6. Joins Between Tables

지금까지 사용한 쿼리는 한 번에 한 테이블에만 액세스 했습니다. 쿼리는 한 번에 여러 테이블에 액세스하거나 테이블의 여러 데이터가 동시에 처리되는 방식으로 동일한 테이블에 액세스 할 수 있습니다. 동일하거나 다른 테이블의 여러 데이터를 동시에 액세스하는 쿼리를 `Join Query` 라고 합니다. 예를 들어, 모든 날씨 기록과 관련된 도시의 위치와 함께 나열하기를 원한다고 하겠습니다. 그러려면 `weather` 테이블의 각 데이터의 `city` 칼럼과 `cities` 테이블의 `name` 칼럼의 데이터를 비교하고, 값이 일치하는 데이터의 쌍을 선택해야 합니다.

> Note : 위 예제는 개념적인 모델링입니다. 조인은 일반적으로 가능한 데이터 쌍을 모두 비교하는것보다 더 효율적인 방식으로 수행하지만, 이는 사용자에게 보여지지 않습니다.

아래 쿼리를 통해 수행하면 됩니다.

```sql
SELECT *
    FROM weather, cities
    WHERE city = name;
```

```sql
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(2 rows)
```

조인 쿼리를 사용하여 결과를 출력할 때 아래 2 가지 사항을 주의해서 봐야합니다.

* Hayward 에 대한 도시 데이터 결과는 없습니다. 이것은 Hayward 에 대한 `cities` 테이블에 일치하는 항목이 없기 때문에, 조인에서는 `weather` 테이블에 있는 비교할 수 없는 데이터는 무시합니다. 이 문제는 다른 방법을 통해 보완해보겠습니다.
* 다른 하나는 도시 이름이 두개가 보이는 것입니다. 잘못된 결과가 아니라, 출력 칼럼을 지정하는 곳에서 `*` 문자를 사용해서 모든 칼럼을 보겠다고 했으니, `weather` 테이블과 `cities` 테이블에 있는 각각의 도시 이름이 모두 보이게 된 것입니다. 이 문제는 다음과 같이 보고 싶은 럼만 지정함으로 해결 할 수 있습니다:

```sql
SELECT city, temp_lo, temp_hi, prcp, date, location
    FROM weather, cities
    WHERE city = name;
```

칼럼마다 이름이 전부 다른 경우에는 파서가 어느 테이블에 속하는지 자동으로 찾아주었습니다. 하지만, 두 테이블에서 중복된 칼럼이 있는 경우 다음과 같이 명시적으로 표현해줘야 합니다.

```sql
SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.location
    FROM weather, cities
    WHERE cities.name = weather.city;
```

조인 쿼리에서는 출력되는 모든 칼럼에 대해서 명시적으로 표현하는게 권장되는 쿼리문입니다. 그래야 이 쿼리가 수정되어 또 다른 테이블과 함께 사용되는 경우에도 쿼리 오류가 나지 않습니다.

지금까지 본 조인 쿼리도 다음과 같은 형식으로 작성할 수 있습니다.

```sql
SELECT *
    FROM weather INNER JOIN cities ON (weather.city = cities.name);
```

이 구문은 자주 사용되지는 않지만 아래 나오는 주제에 대한 이해를 돕기 때문에 소개했습니다.

Hayward 데이터를 다시 가져와 보겠습니다. 우리가 원하는건 `weather` 테이블에을 탐색한 뒤 `cities` 테이블과 일치하는 데이터를 찾아내는 쿼리입니다. 일치하는 값이 없으면 `cites` 테이블의 해당하는 칼럼 값은 빈 값으로 출력됩니다.

```sql
SELECT *
    FROM weather LEFT OUTER JOIN cities ON (weather.city = cities.name);

     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 Hayward       |      37 |      54 |      | 1994-11-29 |               |
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(3 rows)
```

조인 연산자의 왼쪽에 언급된 테이블에는 적어도 한 번씩 모두 데이터가 출력이 되는데 오른쪽 테이블에는 일치하는 데이터만 출력이 되고 일치하는 데이터가 없으면 (Null) 값이 출력됩니다. 이 쿼리를 `left outer join` 이라고 합니다. 

테이블 스스로 조인도 할 수 있습니다. 이것을 `self join` 이라고 합니다. 예를 들어, 날씨 온도 범위에있는 다른 모든 날씨 기록을 찾는다고 가정하겠습니다. 각 `weather` 테이블의 `temp_lo` 및 `temp_hi` 칼럼을 다른 모든 `weather` 데이터 `temp_lo` 와 `temp_hi` 값을 비교합니다. 아래 쿼리를 사용하면 됩니다.

```sql
SELECT W1.city, W1.temp_lo AS low, W1.temp_hi AS high,
    W2.city, W2.temp_lo AS low, W2.temp_hi AS high
    FROM weather W1, weather W2
    WHERE W1.temp_lo < W2.temp_lo
    AND W1.temp_hi > W2.temp_hi;

     city      | low | high |     city      | low | high
---------------+-----+------+---------------+-----+------
 San Francisco |  43 |   57 | San Francisco |  46 |   50
 Hayward       |  37 |   54 | San Francisco |  46 |   50
(2 rows)
```

위 쿼리에서는 조인의 왼쪽과 오른쪽을 구분하기 위해 `weather` 테이블을 각각 `W1` 과 `W2` 로 별칭을 사용하여 변경했습니다. 다른 조인 쿼리에서도 이러한 별칭을 사용할 수 있습니다.

```sql
SELECT *
    FROM weather w, cities c
    WHERE w.city = c.name;
```

이러한 스타일의 약어는 자주 볼 수 있을것입니다.