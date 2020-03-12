---
title : PostgreSQL Chapter 3. Advanced Features
tags :
- PostgreSQL
---

## 3.5. Window Functions

`window function` 은 현재 행과 관련이있는 테이블 행에서 계산을 수행합니다. 집계 함수로 수행 할 수있는 계산 유형과 비슷하다 생각하시면 됩니다. 집계 함수는 해당 되는 로우 집합에 대해서 하나의 로우로 그 결과물을 보여주지만, 윈도우 함수는 각 로우 단위로 그 처리결과를 출력한다. 결과에 대해서 별도의 ID 를 유지합니다. 윈도우 함수는 쿼리 결과의 현재 데이터 뿐만 아니라 더 많은 것을 접근할 수 있다.

다음은 각 직원의 급여를 부서의 평균 급여와 비교하는 방법을 보여주는 예입니다.

```sql
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
```

```sql
  depname  | empno | salary |          avg          
-----------+-------+--------+-----------------------
 develop   |    11 |   5200 | 5020.0000000000000000
 develop   |     7 |   4200 | 5020.0000000000000000
 develop   |     9 |   4500 | 5020.0000000000000000
 develop   |     8 |   6000 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     3 |   4800 | 4866.6666666666666667
 sales     |     1 |   5000 | 4866.6666666666666667
 sales     |     4 |   4800 | 4866.6666666666666667
(10 rows)
```

처음 3 개의 칼럼은 `empsalary` 테이블에서 가져온 데이터입니다.

네 번째 칼럼은 현재 데이터와 동일한 `depname` 값을 가진 모든 테이블 데이터에서 계산한 평균을 나타냅니다. (이것은 집계 함수의 `SUM` 같은 기능이지만, `OVER` 절은 그것을 윈도우 함수(window function) 로 취급하고 윈도우 프레임(window frame) 에서 계산합니다.)

윈도우 함수 호출은 항상 윈도우 함수의 이름과 인수 바로 다음에 `OVER` 절을 포함합니다. 집계 함수와는 비교되는 문법입니다. `OVER` 절은 윈도우 함수에 처리하기 위해 쿼리의 행이 어떻게 분할되는지 정확하게 정의합니다. `OVER` 내의 `PARTITION BY` 절은 행을 `PARTITION BY` 식과 동일한 값을 공유하는 그룹이나 파티션으로 나눕니다. 각 행에 대해 윈도우 함수는 현재 행과 동일한 파티션에 속하는 행에서 계산됩니다.

`OVER` 절 내에서 `ORDER BY` 를 사용하여 윈도우 함수에 의해 행이 처리되는 순서를 제어 할 수도 있습니다. (`ORDER BY` 윈도우는 행이 출력되는 순서와 일치하지 않아도됩니다.) 예를 들면 다음과 같습니다.

```sql
SELECT depname, empno, salary,
       rank() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
```

```sql
  depname  | empno | salary | rank 
-----------+-------+--------+------
 develop   |     8 |   6000 |    1
 develop   |    10 |   5200 |    2
 develop   |    11 |   5200 |    2
 develop   |     9 |   4500 |    4
 develop   |     7 |   4200 |    5
 personnel |     2 |   3900 |    1
 personnel |     5 |   3500 |    2
 sales     |     1 |   5000 |    1
 sales     |     4 |   4800 |    2
 sales     |     3 |   4800 |    2
(10 rows)
```

표시된 것처럼 `rank` 함수는 `ORDER BY` 절에 의해 정의 된 순서를 사용하여 현재 행의 파티션에서 각각의 고유 한 `ORDER BY` 값에 대한 숫자 순위를 생성합니다. `rank` 의 동작은 `OVER` 절에 의해 결정되므로 명시적인 매개 변수가 필요하지 않습니다.

윈도우 함수에 의해 고려되는 행은 `WHERE`, `GROUP BY` 및 `HAVING` 절이 필터링 된 경우 쿼리의 `FROM` 절에 의해 생성 된 "가상 테이블"의 행입니다. 예를 들어, `WHERE` 조건을 만족하지 않아서 행을 제거하면 윈도우 기능이 표시되지 않습니다. 쿼리에는 다른 `OVER` 절을 사용하여 다른 방식으로 데이터를 분할하는 여러 개의 윈도우 함수가 포함될 수 있지만, 가상 테이블에 의해 정의 된 동일한 행 컬렉션에서만 작동합니다.

행 순서가 중요하지 않은 경우 `ORDER BY` 를 생략 할 수 있습니다. `PARTITION BY` 를 생략 할 수도 있습니다. 이 경우 모든 행을 포함하는 단일 파티션이 됩니다.

윈도우 함수와 함께 또 다른 중요한 개념이 있습니다. 각 행마다 파티션 안에 윈도우 프레임이라는 행 세트가 있습니다. 구분 대상이 되는 로우 집함들 가운데, 현재 윈도우 함수가 처리 하는 로우 집합을 뜻한다. 많은 윈도우 함수들이 이 윈도우 프래임 단위로 계산을 합니다. 초기값으로 `ORDER BY` 절을 사용하면, 윈도우 프래임은 정렬 해서 순차적으로 계산하여 현재까지 행까지 반환합니다 . `ORDER BY` 절을 생략하면, 그 구분되는 집합들의 모든 행이 윈도우 함수의 계산 대상이 된다.

다음은 `sum` 윈도우 함수를 사용한 예제입니다.

```sql
SELECT salary, sum(salary) OVER () FROM empsalary;
```

```sql
 salary |  sum  
--------+-------
   5200 | 47100
   5000 | 47100
   3500 | 47100
   4800 | 47100
   3900 | 47100
   4200 | 47100
   4500 | 47100
   4800 | 47100
   6000 | 47100
   5200 | 47100
(10 rows)
```

여기서 합계는 현재 급여의 사본을 포함하여 현재 급여를 통해 첫 번째 (가장 낮은) 급여에서 가져옵니다 (중복 급여의 결과에 주목하십시오).

윈도우 함수는 조회의 `SELECT` 목록 및 `ORDER BY` 절에서만 허용됩니다. `GROUP BY`, `HAVING` 및 `WHERE` 절과 같은 다른 곳에서는 금지되어 있습니다. 이는 논리적으로 이 함수의 처리 대상이 되는 입력 매개 변수값이 이미 결정이 나야하기 때문입니다. 이와 같은 이유로, 윈도우 함수의 입력 매개 변수로 집계 함수의 결과를 사용 할 수는 있지만, 그 반대는 불가능 하다.

윈도우 계산을 수행 한 후 행을 필터링하거나 그룹화해야하는 경우 서브쿼리를 사용할 수 있습니다. 예를 들면 다음과 같습니다.

```sql
SELECT depname, empno, salary, enroll_date
FROM
  (SELECT depname, empno, salary, enroll_date,
          rank() OVER (PARTITION BY depname ORDER BY salary DESC, empno) AS pos
     FROM empsalary
  ) AS ss
WHERE pos < 3;
```

위의 쿼리는 내부 쿼리의 `rank` 가 3 보다 작은 행만 표시합니다.

여러 개의 윈도우 함수를 함께 쓸 때는 각각 `OVER` 절을 사용해야하는데, 이 때 지정할 원도우 프래임이 복잡하다면, 그것을 계속 중복 입력해야는 것과, 이로 인해 오류를 낼 가능성 커지게됩니다. 이 문제점을 줄이기 위해서 `WINDOW` 절을 이용합니다. 아래는 그 예시입니다.

```sql
SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

더 많은 윈도우 함수에 대해서 알고싶으면 [Section 4.2.8](), [Section 9.21](), [Section 7.2.5](), [SELECT]() 를 참고하시면 됩니다.