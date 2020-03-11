---
title : PostgreSQL Chapter 3. Advanced Features
tags :
- PostgreSQL
---

## 3.2. Views

[Section 2.6](/postgre-2joinsbetweentables) 쿼리를 참조하겠습니다. 날씨 기록과 도시 위치의 결합된 데이터는 어플리케이션에서 중요하다 생각할 수 있습니다. 하지만, 매번 필요할때마다 쿼리를 입력할 수는 없습니다. 쿼리에 대해서 `View` 를 만들면 테이블 처럼 참조할 수 있게 만들 수 있는 쿼리를 만들 수 있습니다.

```sql
CREATE VIEW myview AS
    SELECT city, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;

SELECT * FROM myview;
```

`View` 률 자유롭게 사용하는건 SQL 데이터베이스 디자인의 핵심 요소입니다. `View` 를 사용하면 애플리케이션이 발전하고, 변경 되더라도 만들어진 `View` 에 영향을 미치지 않는 범위에서는 얼마든지 확장되고 수정될 수 있습니다.

쿼리에서 실제 테이블을 지정하는 자리 어느 곳이든 그 자리에 `View` 를 사용할 수 있습니다. 또한 `View` 를 가지고 또 다른 `View` 를 만드는 것도 흔한 방법입니다.