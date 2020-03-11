---
title : PostgreSQL Chapter 3. Advanced Features
tags :
- PostgreSQL
---

## 3.3. Foreign Keys

[Chapter 2](/postgre-2tutorialsql) 의 `weather` 와 `cities` 의 테이블을 다시 생각해보겠습니다.

다음 문제를 고려해야합니다. `cities` 테이블에 일치하는 항목이 없는 데이터를 `weather` 테이블에 추가할 수 없도록 만들어야합니다. 이를 데이터베이스에 **참조 무결성(Referential Integrity)** 라고 합니다. 단순한 데이터베이스 시스템에서는 우선 `cities` 테이블을보고 일치하는 데이터가 있는지 확인한 다음 새로운 데이터를 `weather` 테이블에 추가합니다. 이러한 방식은 매우 불편하고 문제가 발생할 수 있습니다. 이 문제를 PostgreSQL 에서 해결할 수 있습니다.

새로운 테이블을 선언해보겠습니다.

```sql
CREATE TABLE cities (
        city     varchar(80) primary key,
        location point
);

CREATE TABLE weather (
        city      varchar(80) references cities(city),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
```

새로운 데이터를 추가해보겠습니다.

```sql
INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');
```

```sql
ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".
```

외래키는 어플리케이션에 맞춰서 조정할 수 있습니다. 이 섹션에서는 간단한 튜톨리얼만 진행할 예정이니 자세한 내용은 [Chapter 5]() 내용을 참고하시면 됩니다. 외래 키를 정확하게 사용하면 어플리케이션에 성능을 향상시킬 수 있습니다.

