---
title : PostgreSQL Chapter 5. Data Definition
tags :
- PostgreSQL
---

## 5.2. Default Values

칼럼에 기본값을 할당할 수 있습니다. 새로운 데이터가 작성되고 일부 칼럼에 값이 지정되지 않으면 해당 칼럼은 각각의 기본값으로 채워집니다. 또한, 데이터 조작 명령은 값이 무엇인지 알 필요없이 칼럼을 기본값으로 설정하도록 명시적으로 요청할 수 있습니다. (데이터 조작 명령에 대한 자세한 내용은 [Chapter 6]() 에 있습니다.)

기본값이 명시적으로 선언되지 않은 경우 기본값은 널값입니다. 널값이 알 수없는 데이터를 나타내는 것으로 간주될 수 있기 때문에 이는 일반적으로 의미가 있습니다.

테이블 정의에서 기본값은 칼럼 데이터 유형 뒤에 나열됩니다. 예를 들면 다음과 같습니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric DEFAULT 9.99
);
```

기본값은 표현식이 될 수 있으며, 테이블이 작성 될 때가 아니라 기본값이 삽입될 때마다 평가됩니다. 일반적인 예는 `timestamp` 칼럼의 기본값이 `CURRENT_TIMESTAMP` 이며 데이터 삽입 시간으로 설정됩니다. 또 다른 일반적인 예는 각 데이터에 대해 *serial number* 를 생성하는 것입니다. PostgreSQL 에서는 일반적으로 다음과 같은 방법으로 수행됩니다.

```sql
CREATE TABLE products (
    product_no integer DEFAULT nextval('products_product_no_seq'),
    ...
);
```

`nextval()` 함수는 시퀀스 객체로부터 연속적인 값을 제공합니다 ([Section 9.16] 참조). 이 배열은 특별한 속기법이 있습니다.

```sql
CREATE TABLE products (
    product_no SERIAL,
    ...
);
```

`SERIAL` 속기법에 대해서는 [Chapter 8.1.4]() 절에서 자세히 설명합니다.