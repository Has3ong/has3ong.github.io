---
title : PostgreSQL Chapter 5. Data Definition
tags :
- PostgreSQL
---

* [5.6.1. Adding a Column](#561-adding-a-column)
* [5.6.2. Removing a Column](#562-removing-a-column)
* [5.6.3. Adding a Constraint](#563-adding-a-constraint)
* [5.6.4. Removing a Constraint](#564-removing-a-constraint)
* [5.6.5. Changing a Column's Default Value](#565-changing-a-columns-default-value)
* [5.6.6. Changing a Column's Data Type](#566-changing-a-columns-data-type)
* [5.6.7. Renaming a Column](#567-renaming-a-column)
* [5.6.8. Renaming a Table](#568-renaming-a-table)

## 5.6 Modifying Tables

테이블을 만들 때 실수를했거나 응용 프로그램의 요구 사항이 변경되었다는 것을 알게되면 테이블을 삭제하고 다시 만들 수 있습니다. 그러나 테이블이 이미 데이터로 채워져 있거나 다른 데이터베이스 개체 (예 : *foreign key constraint*)에서 테이블을 참조하는 경우 편리한 옵션이 아닙니다. 따라서 PostgreSQL 은 기존 테이블을 수정하기위한 명령을 제공합니다. 이것은 개념적으로 테이블에 포함된 데이터를 변경하는 것과 구별됩니다. 여기서 우리는 테이블의 정의 또는 구조를 변경하는데 관심이 있습니다.

아래 동작을 수행할 수 있습니다.

* Add columns
* Remove columns
* Add constraints
* Remove constraints
* Change default values
* Change column data types
* Rename columns
* Rename tables

이러한 모든 동작은 [ALTER TABLE]() 명령을 사용하여 수행됩니다.

### 5.6.1. Adding a Column

칼럼을 추가하기 위해선 아래 명령어를 입력합니다.

```sql
ALTER TABLE products ADD COLUMN description text;
```

추가된 칼럼은 처음에 지정된 기본값으로 채워집니다 (`DEFAULT` 절을 지정하지 않으면 `null` 입니다.).

일반적인 구문을 사용하여 칼럼에 대한 제약 조건을 동시에 정의할 수도 있습니다.

```sql
ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

실제로 `CREATE TABLE` 의 칼럼 설명에 적용할 수 있는 모든 옵션을  여기에서 사용할 수 있습니다. 그러나 기본값이 주어진 제한 조건을 만족해야합니다. 그렇지 않으면 `ADD` 가 실패합니다. 또는 새 칼럼을 올바르게 입력한 후 나중에 제약 조건을 추가할 수 있습니다 (아래 참조).

### 5.6.2. Removing a Column

칼럼을 삭제하려면 아래와 같이 입력하면 됩니다.

```sql
ALTER TABLE products DROP COLUMN description;
```

칼럼에 있던 데이터는 모두 사라집니다. 칼럼과 관련된 테이블 제약 조건도 삭제됩니다. 그러나 칼럼이 다른 테이블의 *foreign key constraint* 에 의해 참조되는 경우 PostgreSQL 은 해당 제약 조건을 자동으로 삭제하지 않습니다. `CASCADE` 를 추가하여 칼럼에 종속된 모든 항목을 삭제하도록 승인할 수 있습니다.

```sql
ALTER TABLE products DROP COLUMN description CASCADE;
```

이것의 일반적인 메커니즘에 대한 설명은 [Section 5.14]() 을 참조하십시오.

### 5.6.3. Adding a Constraint

제한 조건을 추가하기 위해 테이블 제한 조건 구문이 사용됩니다. 예를 들면 다음과 같습니다.

```sql
ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
```

테이블 제약 조건으로 쓸 수 없는 *not-null constraint* 을 추가하려면 다음 구문을 사용하면됩니다

```sql
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

제약 조건이 즉시 점검되므로 테이블 데이터를 추가하기전에 제약 조건을 충족시켜야합니다.

### 5.6.4. Removing a Constraint

제약 조건을 제거하려면 해당 이름을 알아야합니다. 이름을 알고있으면 쉽습니다. 그렇지 않으면 시스템이 생성된 이름을 지정했으며, 이를 찾아야합니다. `psql` 명령 `\d tablename` 을 사용하면 확인할 수 있습니다. 다른 인터페이스는 테이블 세부 사항을 검사하는 방법을 제공할 수도 있습니다. 제거하는 명령은 다음과 같습니다.

```sql
ALTER TABLE products DROP CONSTRAINT some_name;
```

(`$2` 와 같이 생성된 제약 조건 이름을 처리하는 경우 유효한 식별자로 만들려면 큰 따옴표를 사용해야합니다.)

열을 삭제하는 것과 마찬가지로 다른 항목이 의존하는 제약 조건을 삭제하려면 `CASCADE` 를 추가해야합니다. *foreign key constraint* 은 참조된 칼럼의 *unique or primary key constraint* 에 따라 달라집니다.

*not-null constraint* 을 제외한 모든 제약 조건 유형에 대해 동일하게 작동합니다. *not-null constraint* 을 삭제하려면 다음과 같이 사용하면됩니다.

```sql
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

*not-null constraint* 에는 이름이 없습니다.

### 5.6.5. Changing a Column's Default Value

칼럼에 대한 새 기본값을 설정하려면 다음 명령어를 사용하면 됩니다.

```sql
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

이는 테이블의 기존 데이터에는 영향을 미치지 않으며 향후 `INSERT` 명령의 기본값만 변경합니다.

기본값을 제거하려면 다음 명령어를 사용하면됩니다.

```sql
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

이것은 기본값을 `null` 로 설정하는것과 사실상 동일합니다. 결과적으로 기본값은 암시적으로 `null` 값이므로 기본값이 정의되지않은 기본값을 삭제하는 것은 오류가 아닙니다.

### 5.6.6. Changing a Column's Data Type

칼럼의 데이터 타입을 바꾸려면 다음 명령어를 사용하면됩니다.

```sql
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

이는 칼럼의 기존 항목이 새 유형으로 변환될 수있는 경우에만 성공합니다. 복잡한 변환이 필요한 경우 이전 값에서 새 값을 계산하는 방법을 지정하는 `USING` 절을 추가할 수 있습니다.

PostgreSQL 은 칼럼의 기본값 (있는 경우)과 새 유형으로의 변환뿐만 아니라 칼럼과 관련된 모든 제약을 시도합니다. 그러나 이러한 변환은 실패하거나 안좋은 결과를 반환할 수 있습니다. 유형을 변경하기 전에 칼럼에서 제약 조건을 삭제한 다음 적절하게 수정된 제약 조건을 나중에 다시 추가하는것이 가장 좋습니다. 

### 5.6.7. Renaming a Column

기존 칼럼의 이름을 바꿔보겠습니다.

```sql
ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

### 5.6.8. Renaming a Table

기존 테이블의 이름을 바꿔보겠습니다.

```sql
ALTER TABLE products RENAME TO items;
```