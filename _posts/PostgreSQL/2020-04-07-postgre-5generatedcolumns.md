---
title : PostgreSQL Chapter 5. Data Definition
tags :
- PostgreSQL
---

## 5.3. Generated Columns

*generated column* 은 항상 다른 칼럼에서 계산되는 특수 칼럼입니다. 따라서 테이블에 대한 뷰는 칼럼에 대한 것입니다. *generated column* 에는 *stored* 및 *virtual* 의 두 가지 종류가 있습니다. *stored generated column* 은 기록 (삽입 또는 업데이트) 될 때 계산되며 일반 칼럼인 것처럼 스토리지를 차지합니다. *virtual generated column* 은 스토리지를 차지하지 않으며 읽을 때 계산됩니다. 따라서 *virtual generated column* 은 뷰와 유사하고 *stored generated column* 은 구체화 된 뷰와 유사합니다 (항상 자동으로 업데이트되는 것을 제외하고). PostgreSQL 은 현재 *stored generated column* 만 구현합니다.

*generated column* 을 작성하려면 다음과 같이 `CREATE TABLE` 에서 `GENERATED ALWAYS AS` 절을 사용하십시오.

```sql
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

*stored generated column* 을 선언할려면 키워드 `STORED` 를 지정해야합니다. 자세한 내용은 [CREATE TABLE]() 을 참조하십시오.

*generated column* 은 직접 쓸 수 없습니다. `INSERT` 또는 `UPDATE` 명령에서 *generated column* 에 값을 지정할 수 없지만 키워드 `DEFAULT` 를 지정할 수 있습니다.

기본값이있는 칼럼과 *generated column* 의 차이점을 고려해야합니다 다른 값을 제공하지 않은 경우 데이터를 처음 삽입하면 열 기본값이 한 번 평가됩니다. *generated column* 은 데이터가 변경 될 때마다 업데이트되며 재정의수 없습니다. 칼럼 기본값은 테이블의 다른 칼럼을 참조하지 않을 수 있습니다. *generation expression* 은 보통 그렇게합니다. 칼럼 기본값은 휘발성 함수 (예 : `random()` 또는 현재 시간을 참조하는 함수)를 사용할 수 있습니다. *generated column* 에는 허용되지 않습니다.

*generated column* 및 *generated column* 과 관련된 테이블의 정의에는 몇 가지 제한 사항이 적용됩니다.

* *generation expression* 은 변경 불가능한 함수만 사용할 수 있으며 서브 쿼리를 사용하거나 현재 행 이외의 것을 참조할 수 없습니다.
* *generation expression* 은 다른 *generated column* 을 참조할 수 없습니다.
* *generation expression* 은 `tableoid` 를 제외하고 시스템 열을 참조할 수 없습니다.
* *generated column* 은 칼럼 기본값 또는 아이디 정의를 가질 수 없습니다.
* *generated column* 은 파티션 키의 일부가 될 수 없습니다.
* 외부 테이블은 칼럼을 생성 할 수 있습니다. 자세한 내용은 [CREATE FOREIGN TABLE]() 을 참조하십시오.

*generated column* 사용시 추가 고려 사항이 적용됩니다.

* *generated column* 은 기본 칼럼과 별도로 액세스 권한을 유지 관리합니다. 따라서 기본 역할이 아닌 *generated column* 에서 특정 역할을 읽을 수 있도록 정렬할 수 있습니다.
* *generated column* 은 개념적으로 `BEFORE` 트리거가 실행 된 후에 업데이트됩니다. 따라서 `BEFORE` 트리거에서 기본 칼럼에 대한 변경 사항은 *generated column* 에 반영됩니다. 반대로 `BEFORE` 트리거에서 *generated column* 에 액세스할 수 없습니다.