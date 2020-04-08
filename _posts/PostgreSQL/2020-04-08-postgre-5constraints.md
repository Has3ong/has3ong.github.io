---
title : PostgreSQL Chapter 5. Data Definition
tags :
- PostgreSQL
---

* [5.4.1. Check Constraints](#541-check-constraint)
* [5.4.2. Not-Null Constraints](#542-not-null-constraints)
* [5.4.3. Unique Constraints](#543-unique-constraints)
* [5.4.4. Primary Keys](#544-primary-keys)
* [5.4.5. Foreign Keys](#545-foreign-keys)
* [5.4.6. Exclusion Constraints](#546-exclusion-constraints)

## 5.4. Constraints

데이터 형식은 테이블에 저장할 수있는 데이터 종류를 제한하는 방법입니다. 그러나 많은 응용 프로그램에서 제공하는 제약 조건이 너무 거칩니다. 예를 들어 제품 가격이 포함된 열은 양수 값만 허용해야합니다. 그러나 양수만 허용하는 표준 데이터 유형은 없습니다. 또 한, 다른 열 또는 행과 관련하여 열 데이터를 제한할 수 있다는 것입니다. 예를 들어 제품 정보가 포함된 테이블에는 각 제품 번호에 대해 하나의 행만 있어야합니다.

이를 위해 SQL을 사용하면 열과 테이블에 대한 제약 조건을 정의 할 수 있습니다. 제약 조건을 사용하면 원하는만큼 테이블의 데이터를 제어할 수 있습니다. 사용자가 제약 조건을 위반하는 열에 데이터를 저장하려고하면 오류가 발생합니다. 디폴트 값을 정의한 경우에도 적용됩니다.

### 5.4.1. Check Constraint

*Check Constraint* 이 가장 일반적인 제약 조건 유형입니다. 특정 칼럼의 값이 부울표현식을 만족해야 함을 지정할 수 있습니다. 예를 들어, 제품 가격을 항상 양수만 요구하려면 다음을 사용할 수 있습니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

보시다시피 제약 조건 정의는 기본값 정의와 마찬가지로 데이터 유형 뒤에옵니다. 기본값 및 제약 조건은 임의의 순서로 나열될 수 있습니다. *Check Constraint* 은 키워드 `CHECK` 와 괄호 안의 표현식으로 구성됩니다. *Check Constraint* 표현식은 이와 같이 제한되는 칼럼을 포함해야합니다. 그렇지 않으면 제약 조건이 너무 의미가 없습니다.

제약 조건에 별도의 이름을 지정할 수도 있습니다. 오류 메시지를 명확하게하고 변경해야할 때 제약 조건을 참조할 수 있습니다. 구문은 다음과 같습니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CONSTRAINT positive_price CHECK (price > 0)
)
```

따라서 명명된 제약 조건을 지정하려면 키워드 `CONSTRAINT` 와 식별자, 제약 조건 정의를 차례로 사용하면됩니다. (이러한 방식으로 제약 조건 이름을 지정하지 않으면 시스템이 이름을 선택합니다.)

*Check Constraint* 은 여러 칼럼을 참조할 수도 있습니다. 일반 가격과 할인 가격을 저장하고 할인된 가격이 일반 가격보다 낮은지 확인하려는 경우는 아래와같이 사용합니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

아래는 같은 표현입니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
);
```

취향 차이입니다.

칼럼 제약 조건과 같은 방식으로 테이블 제약 조건에 이름을 할당할 수 있습니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),
    CONSTRAINT valid_discount CHECK (price > discounted_price)
);
```

점검 표현식이 `true` 또는 `null` 값으로 평가되면 *Check Constraint* 이 충족됨에 유의해야합니다. 피연산자가 `null` 이면 대부분의 표현식이 `null` 값으로 평가되므로 제한 컬럼의 `null` 값을 막지 않습니다. 칼럼에 `null` 값이 포함되지 않도록하기 위해 다음 섹션에서 설명하는 *not-null constraints* 을 사용할 수 있습니다.

> Note : PostgreSQL 은 검사 중인 새 행 또는 업데이트된 행 이외의 테이블 데이터를 참조하는 *Check Constraint* 을 지원하지 않습니다. 이 규칙을 위반하는 *Check Constraint* 이 단순한 테스트에서 작동하는 것처럼 보일 수 있지만, (관련된 다른 행의 후속 변경으로 인해) 데이터베이스가 제약조건이 거짓인 상태에 도달하지 않는다고 보장할 수는 없습니다. 이로 인해 데이터베이스 덤프 및 재로드가 실패할 수 있습니다. 완전한 데이터베이스 상태가 제약조건과 일치하더라도, 제약조건을 만족시키는 순서로 데이터를 로드되지 않기 때문에 재로드가 실패할 수 있습니다. 가능한 경우, `UNIQUE`, `EXCLUDE` 또는 `FOREIGN KEY` 제약 조건을 사용하여 교차 및 교차 테이블 제한을 표현하면됩니다. 연속적으로 유지되는 일관성 보장이 아니라 데이터 삽입 시 다른 행에 대한 일회성 점검이 필요한 경우 이를 구현하기 위해 사용자 정의 트리거를 사용할 수 있습니다.(이 방법은 데이터를 다시 로드한 후 `pg_dump` 가 트리거를 다시 설치하지 않기 때문에 데이터 재장착 시 검사가 시행되지 않도록 하기 때문에 덤프/재로드 문제를 방지할 수 있습니다. 덤프/리로드)

> Note : PostgreSQL 은 *Check Constraint* 의 조건이 불변하다고 가정하며, 즉 그들은 항상 동일한 입력 행에 동일한 결과를 줍니다. 이 가정은 행을 삽입하거나 업데이트할 때만 *Check Constraint* 을 검사하는 것을 정당화하고 다른 때는 검사하지 않습니다. (다른 테이블 데이터를 참조하지 않는 것에 대한 위의 경고는 정말로 이 제한의 특별한 경우다.) 이 가정을 깨는 일반적인 방법의 예는 Check 표현식에서 사용자 정의 함수를 참조한 다음 해당 함수의 동작을 변경하는 것입니다. PostgreSQL 은 이를 허용하지 않지만, 표에 현재 *Check Constraint* 을 위반하는 행이 있는지 여부를 알 수 없다. 그렇게 되면 후속 데이터베이스 덤프 및 재로드가 실패하게 됩니다. 이러한 변경을 처리하는 권장 방법은 제약 조건을 삭제하고(`ALTER TABLE` 사용), 기능 정의를 조정하고 제약 조건을 다시 추가하여 모든 테이블 데이터에 대해 다시 점검하는 것이다.

### 5.4.2. Not-Null Constraints

*not-null constraint* 은 칼럼이 `null` 값을 가정해서는 안됨을 지정합니다.

```sql
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric
);
```

*not-null constraint* 은 항상 열 제약 조건으로 작성됩니다. *not-null constraint* 은 기능적으로 *Check Constraint* `CHECK (column_name IS NOT NULL)` 를 만드는 것과 동일하지만 PostgreSQL 에서는 명시적인 **not-null constraint** 을 만드는 것이 더 효율적입니다. 단점은 이런 식으로 생성 된 null이 아닌 제약 조건에 명시적인 이름을 지정할 수 없다는 것입니다.

물론 칼럼에는 둘 이상의 제약 조건이있을 수 있습니다. 제약 조건을 하나씩 작성하면됩니다.

```sql
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price > 0)
);
```

순서는 중요하지 않습니다. 제약 조건이 점검되는 순서를 반드시 결정하지는 않습니다.

`NOT NULL` 제약 조건은 `NULL` 제약 조건과 반대입니다. 그렇다고해서 칼럼이 `null` 이어야 한다는 의미는 아닙니다. 간단하게 칼럼이 `null` 일 수있는 기본 동작을 선택합니다. `NULL` 제약 조건은 SQL 표준에 없으며 범용 응용 프로그램에서 사용해서는 안됩니다. (일부 다른 데이터베이스 시스템과 호환되도록 PostgreSQL 에만 추가되었습니다.) 그러나 일부 사용자는 스크립트 파일에서 제약 조건을 쉽게 전환할 수 있기 때문에 좋아합니다. 예를 들어 다음과 같이 시작할 수 있습니다.

```sql
CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);
```

그런 다음 원하는 곳에 `NOT` 키워드를 추가하면 됩니다.

> Tip : 대부분의 데이터베이스 디자인에서 대부분의 칼럼은 `null` 이 아닌 것으로 표시해야합니다.

### 5.4.3. Unique Constraints

*Unique Constraint* 은 칼럼 또는 칼럼 그룹에 포함  데이터가 테이블의 모든 행에서 고유한지 확인합니다. 구문은 다음과 같습니다.

```sql
CREATE TABLE products (
    product_no integer UNIQUE,
    name text,
    price numeric
);
```

칼럼 제약조건으로 쓸때 다음과 같이 사용합니다.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    UNIQUE (product_no)
);
```

테이블 제약 조건으로 쓸 때.

칼럼 그룹에 대한 *unique constraint* 을 정의하려면 칼럼 이름을 쉼표로 구분하여 테이블 제약 조건으로 작성하면됩니다.

```sql
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    UNIQUE (a, c)
);
```

칼럼 중 하나가 고유하지 않아도되지만 표시된 칼럼의 값 조합이 전체 테이블에서 고유하도록 지정합니다.

일반적인 방식으로 *unique constraint* 에 고유한 이름을 지정할 수 있습니다.

```sql
CREATE TABLE products (
    product_no integer CONSTRAINT must_be_different UNIQUE,
    name text,
    price numeric
);
```

*unique constraint* 을 추가하면 제약 조건에 나열된 열 또는 열 그룹에 고유 B- 트리 인덱스가 자동으로 생성됩니다. 일부 행만 포함하는 고유성 제한은 *unique constraint* 으로 작성할 수 없지만 고유 [Partial Index]() 를 작성하여 이러한 제한을 적용할 수 있습니다.

일반적으로, 테이블에 제약 조건에 포함된 모든 칼럼의 값이 동일한 행이 둘 이상 있으면 *unique constraint* 이 위반됩니다. 그러나이 비교에서 두 개의 `null` 값은 동일한 것으로 간주되지 않습니다. 이는 *unique constraint* 이 존재하는 경우에도 제한된 칼럼 중 하나 이상에 `null` 값을 포함하는 중복 행을 저장할 수 있음을 의미합니다. 이 동작은 SQL 표준을 준수하지만 다른 SQL 데이터베이스는 이 규칙을 따르지 않을 수 있습니다. 따라서 이식성이 뛰어난 응용 프로그램을 개발할때는 주의해야합니다.

### 5.4.4. Primary Keys

*primary keys contraint* 은 칼럼 또는 칼럼 그룹이 테이블의 데이터에 대한 고유 식별자로 사용될 수 있음을 나타냅니다. 이를 위해서는 값이 고유하고 `null` 이 아니어야합니다. 따라서 다음 두 테이블 정의는 동일한 데이터를 허용합니다.

```sql
CREATE TABLE products (
    product_no integer UNIQUE NOT NULL,
    name text,
    price numeric
);
```

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

기본 키는 둘 이상의 칼럼에 걸쳐있을 수 있습니다. 구문은 *unique constraint* 과 유사합니다.

```sql
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    PRIMARY KEY (a, c)
);
```

기본 키를 추가하면 기본 키에 나열된 칼럼 또는 칼럼 그룹에 고유 한 B- 트리 인덱스가 자동으로 생성되고 칼럼이 `NOT NULL` 로 표시됩니다.

테이블에는 최대 하나의 기본 키 가있을 수 있습니다. (기능적으로 거의 동일한 고유하지만 *not-null constraint* 이 많을 수 있지만 기본 키로 하나만 식별 될 수 있습니다.) 관계형 데이터베이스 이론에 따르면 모든 테이블에 기본 키가 있어야합니다. 이 규칙은 PostgreSQL 에서 시행하지 않지만 일반적으로 따르는 것이 가장 좋습니다.

기본 키는 설명서 및 클라이언트 응용 프로그램 모두에 유용합니다. 예를 들어 데이터 값을 수정할 수있는 GUI 응용 프로그램은 행을 고유하게 식별할 수 있도록 테이블의 기본 키를 알아야합니다. 데이터베이스 시스템이 기본 키가 선언된 경우 기본 키를 사용하는 다양한 방법도 있습니다. 예를 들어 기본 키는 해당 테이블을 참조하는 외래 키의 기본 대상 칼럼을 정의합니다.

### 5.4.5. Foreign Keys

*foreign key contraint* 은 칼럼의 값이 다른 테이블의 일부 행에 나타나는 값과 일치해야 함을 지정합니다. 우리는 이것을 두 개의 관련 테이블 사이의 참조 무결성을 유지한다고 말합니다.

이미 여러 번 사용한 `products` 테이블이 있다고 가정 해보겠습니다.

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

해당 제품의 주문을 저장하는 테이블이 있다고 가정 하겠습니다. 주문 테이블에는 실제로 존재하는 제품 주문만 포함된다 해보겠습니다. 따라서 `products` 테이블을 참조하는 `orders` 테이블에 *foreign key contraint* 을 정의합니다.

```sql
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

이제 `products` 테이블에 나타나지 않는 NULL이 아닌 `product_no` 항목으로 주문을 작성할 수 없습니다.

이 상황에서 `orders` 테이블은 참조 테이블(referencing table) 이고 `products` 테이블은 참조된 테이블(referenced table) 이라고합니다. 마찬가지로 *referencing and referenced* 칼럼이 있습니다.

위 명령을 단축하여 다음을 수행 할 수도 있습니다

```sql
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products,
    quantity integer
);
```

칼럼 목록이 없으면 참조된 테이블의 기본 키가 참조된 칼럼으로 사용되기 때문입니다.

외래 키는 칼럼 그룹을 제한하고 참조할 수도 있습니다. 평소와 같이 테이블 제약 조건 형식으로 작성해야합니다. 다음은 고안된 구문 예입니다.

```sql
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,
  FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

물론 제약된 칼럼의 수와 유형은 참조 된열의 칼럼과 유형과 일치해야합니다.

일반적인 방식으로 *foreign key constraint* 에 고유한 이름을 지정할 수 있습니다.

테이블에는 둘 이상의 *foreign key constraint* 이 있을 수 있습니다. 테이블간 다대다 관계를 구현하는데 사용됩니다. `products` 및 `orders` 에 대한 테이블이 있지만 이제는 하나의 주문에 많은 제품이 포함될 수 있습니다 (위의 구조에서는 허용되지 않음). 이 테이블 구조를 사용할 수 있습니다.

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

기본 키는 마지막 테이블의 외래 키와 겹칩니다.

외래 키로 인해 `products` 와 관련이 없는 `orders` 을 만들 수 없습니다. 그러나 `products` 를 참조하는 `orders` 이 작성된 후 `products` 을 제거하면 어떻게됩니까? SQL 을 사용하면 이를 처리할 수 있습니다. 직관적으로 몇가지 옵션이 있습니다.

* Disallow deleting a referenced product
* Delete the orders as well
* Something else?

이를 설명하기 위해 위의 다대다 관계 예에 대해 다음 정책을 구현해 보겠습니다. 누군가 `order` (`item_items` 를 통해) 여전히 `orders` 가 참조하는 `products` 을 제거하려는 경우 이를 허용하지 않습니다. 누군가 `orders` 을 제거하면 `orders` 항목도 제거됩니다.

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products ON DELETE RESTRICT,
    order_id integer REFERENCES orders ON DELETE CASCADE,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

*Restricting* 및 *Cascading deletes* 가장 일반적인 두 가지 옵션입니다. `RESTRICT` 는 참조된 행의 삭제를 방지합니다. `NO ACTION` 은 제약 조건을 점검할 때 참조 행이 여전히 존재하면 오류가 발생합니다. `NO ACTION` 은 디폴트 값입니다. (이 두 가지 선택의 근본적인 차이점은 `NO ACTION` 은 트랜잭션 후반까지 검사가 연기될 수 있지만 `RESTRICT` 는 그렇지 않습니다.) `CASCADE` 는 참조된 행이 삭제될 때 이를 참조하는 행이 자동으로 삭제되도록 지정합니다. 게다가, `SET NULL` 및 `SET DEFAULT` 의 두 가지 다른 옵션이 있습니다. 이로 인해 참조 행이 삭제될 때 참조 행의 참조 칼럼이 각각 `null` 또는 기본값으로 설정됩니다. 이것들이 당신이 어떤 제약 조건들을 살펴보는것을 상관하지 않습니다. 예를 들어, `SET DEFAULT` 를 지정했지만 기본값이 외래 키 제약 조건을 만족하지 않으면 동작에 실패합니다.

`ON DELETE` 와 유사하게 참조 칼럼이 변경 (업데이트) 될 때 호출되는 `ON UPDATE` 도 있습니다. 가능한 조치는 동일합니다. 이 경우 `CASCADE` 는 참조된 칼럼의 업데이트된 값이 참조 행에 복사된다는 의미입니다.

일반적으로 참조 칼럼이 `null` 인 경우 참조 행은 *foreign key contraint* 을 충족할 필요가 없습니다. `MATCH FULL` 이 외래 키 선언에 추가되면 모든 참조 칼럼이 `null` 인 경우에만 참조 행이 제약 조건을 만족시키는 이스케이프됩니다 (따라서 `null` 값과 `null` 이 아닌 값의 혼합은 `MATCH FULL` 제약 조건이 실패함을 보장합니다). 참조 행이 *foreign key contraint* 을 충족시키지 못하도록하려면 참조 칼럼을 `NOT NULL` 로 선언하면됩니다.

외래 키는 기본 키이거나 *unique constraint* 인 칼럼을 참조해야합니다. 이는 참조된 칼럼에 항상 색인 (기본 키 또는 *unique constraint* 의 기본 색인)이 있음을 의미합니다. 따라서 참조 행이 일치하는지 확인하십시오. 참조된 테이블에서 행을 삭제하거나 참조된 칼럼을 업데이트하려면 이전 값과 일치하는 행에 대해 참조 테이블을 스캔해야하므로 참조 칼럼도 색인화하는 것이 좋습니다. 이것이 항상 필요한 것은 아니며, 색인화 방법에 대한 많은 선택 사항이 있기 때문에 *foreign key contraint* 의 선언이 참조 칼럼에 색인을 자동으로 작성하지는 않습니다.

데이터 업데이트 및 삭제에 대한 자세한 내용은 [Chapter 6]() 에 있습니다. [CREATE TABLE]()에서 *foreign key contraint* 구문에 대한 설명도 참고하면됩니다.

### 5.4.6. Exclusion Constraints

*exclusion constraint* 는 지정된 연산자를 사용하여 지정된 칼럼이나 식에서 두 행을 비교하는 경우 이러한 연산자 비교 중 하나 이상이 `false` 또는 `null` 을 반환합니다. 구문은 다음과 같습니다.

```sql
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

자세한 내용은 [CREATE TABLE]() ... [CONSTRAINT]() ... [EXCLUDE]() 를 참고하면됩니다.

*exclusion constraint* 을 추가하면 제약 조건 선언에 지정된 유형의 인덱스가 자동으로 생성됩니다.