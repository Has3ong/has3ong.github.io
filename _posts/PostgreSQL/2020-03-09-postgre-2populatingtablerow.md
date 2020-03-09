---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.4. Populating a Table With Rows

`INSERT` 문은 테이블을 다음 데이터를 추가하는 데 사용됩니다.

```sql
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```

모든 데이터 타입은 입력할 때 정확하게 사용한다는 점에 유의해야합니다. 단순 숫자 값이 아닌 상수는 아래 예와 같이 작은따옴표(') 로 둘러싸여 있어야 합니다. 날짜 타입은 입력할 때 상당히 유연하지만, 이 튜톨리얼에선 모호하지 않은 형식을 사용하겠습니다.

`point` 타입은 다음과 같이 좌표 쌍을 입력으로 요구한다.

```sql
INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
```

지금까지 사용된 구문에는 칼럼의 순서를 기억해야 합니다. 대체 구문을 사용하면 칼럼을 명시적으로 나열할 수 있습니다.

```sql
INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

예를 들어 강수량을 알 수 없는 경우, 아래와 같이 일부 칼럼을 누락시키거나 열을 다른 순서로 나열할 수 있습니다. 

```sql
INSERT INTO weather (date, city, temp_hi, temp_lo)
    VALUES ('1994-11-29', 'Hayward', 54, 37);
```

많은 개발자들은 암묵적으로 순서에 의존하는 것보다 명시적으로 칼럼을 나열하는 것이 더 낫다고 생각합니다.

다음 섹션에서 작업할 데이터가 있도록 위에 표시된 SQL 문을 입력해주세요.

또한, `COPY` 를 사용하여 *Flat-Text* 파일에서 대량의 데이터를 로드할 수도 있습니다. `COPY` 명령어는 `INSERT` 보다 유연성을 떨어지지만 어플리케이션에 최적화되어 있기 떄문에 더 빠르게 동작합니다.

예를 들면 다음과 같습니다.

```sql
COPY weather FROM '/home/user/weather.txt';
```

백엔드 프로세스가 파일을 직접 읽기 때문에 클라이언트가 아닌 백엔드 프로세스를 실행하는 시스템에서 소스 파일의 파일 이름을 사용할 수 있어야 합니다.

[COPY](https://www.postgresql.org/docs/12/sql-copy.html) 에서 `COPY` 명령에 대해 자세히 읽을 수 있습니다..



