---
title : PostgreSQL Chapter 4. SQL Syntax
tags :
- PostgreSQL
---

## 4.2. Value Expressions

* [4.2.1. Column References](#421-column-references)
* [4.2.2. Positional Parameters](#422-positional-parameters)
* [4.2.3. Subscripts](#423-subscripts)
* [4.2.4. Field Selection](#424-field-selection)
* [4.2.5. Operator Invocations](#425-operator-invocations)
* [4.2.6. Function Calls](#426-function-calls)
* [4.2.7. Aggregate Expressions](#427-aggregate-expressions)
* [4.2.8. Window Function Calls](#428-window-function-calls)
* [4.2.9. Type Casts](#429-type-casts)
* [4.2.10. Collation Expressions](#4210-collation-expressions)
* [4.2.11. Scalar Subqueries](#4211-scalar-subqueries)
* [4.2.12. Array Constructors](#4212-array-constructors)
* [4.2.13. Row Constructors](#4213-row-constructors)
* [4.2.14. Expression Evaluation Rules](#4214-expression-evaluation-rules)

값 표현식은 `SELECT` 명령의 대상 목록, `INSERT` 또는 `UPDATE` 의 새 열 값 또는 여러 명령의 검색 조건과 같은 다양한 컨텍스트에서 사용됩니다. 테이블 표현식 (테이블)의 결과와 구별하기 위해 값 표현식의 결과를 스칼라라고도합니다. 따라서 값 표현식은 스칼라 표현식 (또는 단순히 표현식)이라고도합니다. 표현식 구문을 사용하면 산술, 논리, 집합 및 기타 연산을 사용하여 기본 부분의 값을 계산할 수 있습니다.

값 표현식은 다음 중 하나입니다.

* A constant or literal value
* A column reference
* A positional parameter reference, in the body of a function definition or prepared statement
* A subscripted expression
* A field selection expression
* An operator invocation
* A function call
* An aggregate expression
* A window function call
* A type cast
* A collation expression
* A scalar subquery
* An array constructor
* A row constructor
* Another value expression in parentheses (used to group subexpressions and override precedence)

이 목록 외에도 표현식으로 분류 할 수 있지만 일반적인 구문 규칙을 따르지 않는 많은 구성이 있습니다. 이들은 일반적으로 함수 또는 연산자의 의미를 가지며 [Chapter 9]() 의 적절한 위치에 설명되어 있습니다. 예는 `IS NULL` 절입니다.

[Section 4.1.2]() 절에서 상수에 대해 이미 논의했습니다. 다음 섹션에서는 나머지 옵션에 대해 설명합니다.

### 4.2.1. Column References

칼럼은 다음 형식으로 참조 될 수 있습니다.

```sql
correlation.columnname
```

`correlation` 테이블 이름 (스키마 이름으로 정규화 될 수 있음) 또는 `FROM` 절을 통해 정의 된 테이블의 별명입니다. 열 이름이 현재 쿼리에서 사용중인 모든 테이블에서 고유 한 경우 상관관계 이름과 분리 점을 생략 할 수 있습니다. (또한 [Chapter 7]() 을 참조하십시오.)

### 4.2.2. Positional Parameters

위치 매개 변수 참조는 SQL 문 외부에 제공되는 값을 표시하는 데 사용됩니다. 매개 변수는 SQL 함수 정의 및 준비된 쿼리에 사용됩니다. 일부 클라이언트 라이브러리는 SQL 명령 문자열과 별도로 데이터 값 지정을 지원합니다.이 경우 매개 변수를 사용하여 *out-of-line* 데이터 값을 참조합니다. 매개 변수 참조의 형식은 다음과 같습니다.

```sql
$number
```

예를 들어 다음과 같이 `dept` 함수의 정의를 고려해보겠습니다.

```sql
CREATE FUNCTION dept(text) RETURNS dept
    AS $$ SELECT * FROM dept WHERE name = $1 $$
    LANGUAGE SQL;
```

여기서 `$1` 은 함수가 호출 될 때마다 첫 번째 함수 인수의 값을 참조합니다.

### 4.2.3. Subscripts

식이 배열 유형의 값을 생성하는 경우 다음을 작성하여 배열 값의 특정 요소를 추출 할 수 있습니다.

```sql
expression[subscript]
```

또는 여러 개의 인접한 요소 ("배열 슬라이스") 를 작성하여 추출 할 수 있습니다.

```sql
expression[lower_subscript:upper_subscript]
```

(괄호 `[]` 는 문자 그대로 나타납니다.) 각 `subscript` 자체는 표현식이며 정수 값을 가져와야합니다.

일반적으로 배열 `expression` 은 괄호로 묶어야하지만 첨자식이 칼럼 참조 또는 위치 매개 변수인 경우 괄호를 생략 할 수 있습니다. 또한, 원래 배열이 다차원 일 때는 여러 첨자를 연결할 수 있습니다. 예를 들면 다음과 같습니다.

```sql
mytable.arraycolumn[4]
mytable.two_d_column[17][34]
$1[10:42]
(arrayfunction(a,b))[42]
```

마지막 예에서 괄호가 필요합니다. 배열에 대한 자세한 내용은 [Section 8.15]() 을 참조하십시오.

### 4.2.4. Field Selection

표현식이 복합 유형(데이터 유형) 의 값을 생성하는 경우, 작성하여 데이터의 특정 필드를 추출 할 수 있습니다.

```sql
expression.fieldname
```

일반적으로 행 표현식은 괄호로 묶어야하지만 선택할 표현식이 테이블 참조 또는 위치 매개 변수 인 경우 괄호를 생략 할 수 있습니다. 예를 들면 다음과 같습니다.

```sql
mytable.mycolumn
$1.somecolumn
(rowfunction(a,b)).col3
```

(따라서 규정 된 열 참조는 실제로 필드 선택 구문의 특수한 경우입니다.) 이 특수한 경우의 중요사항은 복합 유형의 테이블 열에서 필드를 추출하는 것입니다.

```sql
(compositecol).somefield
(mytable.compositecol).somefield
```

```sql
(compositecol).*
```

여기에서 괄호는 `compositecol` 이 테이블 이름이 아닌 데이터 이름이거나 `mytable` 이 두 번째 경우 스키마 이름이 아닌 테이블 이름임을 나타 내기 위해 필요합니다.

`.*` 를 쓰면 복합 값의 모든 필드를 요청할 수 있습니다.

이 표기법은 상황에 따라 다르게 동작합니다. 자세한 내용은 [Section 8.16.5]() 을 참조하십시오.

### 4.2.5. Operator Invocations

연산자 호출에 대한 세 가지 구문이 있습니다.

`expression` `operator` `expression` (이진수 삽입 연산자)

`operator` `expression` (단일 접두사 연산자)

`expression` `operator`(단일 접미사 연산자)

여기서 `operator` 토큰은 [Section 4.1.3]() 의 구문 규칙을 따르거나 키워드 `AND`, `OR` 및 `NOT` 중 하나이거나 형식이 적합한 규정 된 연산자 이름입니다.

```sql
OPERATOR(schema.operatorname)
```

존재하는 특정 연산자와 단항인지 이진인지는 시스템이나 사용자가 정의한 연산자에 따라 다릅니다. [Chapter 9]() 에서는 내장 연산자에 대해 설명합니다.

### 4.2.6. Function Calls

함수 호출 구문은 함수 이름(스키마 이름으로 정규화 될 수 있음) 과 그 뒤에 인수 목록이 괄호로 묶여 있습니다.

```sql
function_name ([expression [, expression ... ]] )
```

예를 들어, 다음은 제곱근 2 를 계산합니다.

```sql
sqrt(2)
```

내장 기능 목록은 [Chapter 9]() 에 있습니다. 다른 기능은 사용자가 추가 할 수 있습니다.

일부 사용자가 다른 사용자를 불신하는 데이터베이스에서 쿼리를 발행 할 때는 함수 호출을 작성할 때 [Section 10.3]() 의 보안 예방 조치를 준수하십시오.

인수는 선택적으로 이름을 붙일수 있습니다. 자세한 내용은 [Section 4.3]() 을 참조하십시오.

> Note : 복합 유형의 단일 인수를 사용하는 함수는 필드 선택 구문을 사용하여 선택적으로 호출 할 수 있으며 반대로 필드 선택은 기능적 스타일로 작성할 수 있습니다. 즉, 표기법 `col(table)` 과 `table.col` 은 서로 바꿔 사용할 수 있습니다. 이 동작은 SQL 표준은 아니지만 *computed fields* 를 에뮬레이트하는 함수를 사용할 수 있으므로 PostgreSQL 에서 제공됩니다. 자세한 정보는 [Section 8.16.5]() 을 참조하십시오.

### 4.2.7. Aggregate Expressions

집계 표현식은 쿼리에 의해 선택된 데이터에서 집계 함수의 적용을 나타냅니다. 집계 함수는 여러 입력을 합 또는 평균과 같은 단일 출력 값으로 줄입니다. 집계 표현식의 구문은 다음 중 하나입니다.

```sql
aggregate_name (expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (ALL expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (DISTINCT expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( * ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( [ expression [ , ... ] ] ) WITHIN GROUP ( order_by_clause ) [ FILTER ( WHERE filter_clause ) ]
```

여기서 `aggregate_name` 은 이전에 정의 된 집계 값 (스키마 이름으로 정규화 될 수 있음) 이고 `expression` 은 집계 식이나 윈도우 함수 호출을 포함하지 않는 값 식입니다. 선택적 `order_by_clause` 및 `filter_clause` 가 아래에 설명되어 있습니다.

집계 식의 첫 번째 형식은 각 입력 데이터에 대해 집계를 한 번 호출합니다. `ALL` 이 기본값이므로 두 번째 양식은 첫 번째 양식과 동일합니다. 세 번째 형식은 입력 데이터에서 찾은 각 고유 한 식 값 (또는 여러 식의 고유 한 값 집합)에 대해 집계를 한 번 호출합니다. 네 번째 양식은 각 입력 데이터에 대해 집계를 한 번 호출합니다. 특정 입력 값이 지정되지 않았으므로 일반적으로 `count(*)` 집계 함수에만 유용합니다. 마지막 양식은 아래에 설명 된 순서대로 설정된 집계 함수와 함께 사용됩니다.

대부분의 집계 함수는 `null` 입력을 무시하므로 하나 이상의 표현식에서 `null` 을 생성하는 데이터는 삭제됩니다. 별도의 지정이없는 한 모든 내장 집계에 대해 이것이 사실이라고 가정 할 수 있습니다.

예를 들어 `count(*)`는 총 입력 데이터 수를 산출합니다. `count(f1)` 는 `f1` 이 널이 아닌 입력 데이텀의 수를 산출합니다. `count` 는 `null` 을 무시하기 때문입니다. `count(distinct f1)` 는 `f1` 의 `null` 이 아닌 고유 값의 수를 산출합니다.

일반적으로 입력 데이터는 지정되지 않은 순서로 집계 함수에 제공됩니다. 대부분의 경우 이것은 중요하지 않습니다. 예를 들어 `min` 은 입력받는 순서에 관계없이 동일한 결과를 생성합니다. 그러나 일부 집계 함수 (예 : `array_agg` 및 `string_agg`) 는 입력 데이터의 순서에 따라 결과를 생성합니다. 이러한 집계를 사용할 때 선택적으로 `order_by_clause` 를 사용하여 원하는 순서를 지정할 수 있습니다. `order_by_clause` 는 [Section 7.5]() 에 기술 된 것처럼 쿼리 레벨 `ORDER BY` 절과 동일한 구문을 갖습니다. 단, 표현식은 항상 표현식이며 출력 칼럼 이름 또는 숫자 일 수 없습니다. 예를 들면 다음과 같습니다.

```sql
SELECT array_agg(a ORDER BY b DESC) FROM table;
```

다중 인수 집계 함수를 처리 할 때 `ORDER BY` 절은 모든 집계 인수 뒤에 옵니다. 예를 들어 다음과 같이 작성하십시오.

```sql
SELECT string_agg(a, ',' ORDER BY a) FROM table;
```

아래는 올바르지 않습니다.

```sql
SELECT string_agg(a ORDER BY a, ',') FROM table;  -- incorrect
```

후자는 구문 상 유효하지만 두 개의 `ORDER BY` 키를 사용하는 단일 인수 집계 함수의 호출을 나타냅니다 (두 번째는 상수이므로 다소 쓸모가 없습니다).

`order_by_clause` 외에 `DISTINCT` 를 지정하면 모든 `ORDER BY` 표현식이 집계의 정규 인수와 일치해야합니다. 즉, `DISTINCT` 목록에 포함되지 않은 식을 정렬 할 수 없습니다.

> Note : 집계 함수에서 `DISTINCT` 와 `ORDER BY` 를 모두 지정하는것은 PostgreSQL 의 확장 기능입니다.

지금까지 설명한대로 집계의 일반 인수 목록 내에 `ORDER BY` 를 배치하는 것은 순서가 선택적인 범용 및 통계 집계에 대해 입력 데이터를 정렬 할 때 사용됩니다. `order_by_clause` 가 필요한 **순서 집합 집계(ordered-set aggregate)** 라는 집계 함수의 하위 클래스가 있습니다. 일반적으로 집계 연산은 입력 데이터의 특정 순서의 관점에서만 볼 수 있기 때문입니다. 순서 집합 집계의 일반적인 예에는 순위 및 백분위 수 계산이 포함됩니다. 순서 집합 집계의 경우 `order_by_clause` 는 위의 마지막 구문 대안에 표시된 것처럼 `WITHIN GROUP (...)` 안에 작성됩니다. `order_by_clause` 의 표현식은 일반 집계 인수와 마찬가지로 입력 행당 한 번씩 평가되며 `order_by_clause` 의 요구 사항에 따라 정렬되어 입력 인수로 집계 함수에 제공됩니다. (이것은 집계 함수에 인수로 취급되지 않는 비 `WITHIN GROUP` `order_by_clause` 의 경우와는 다릅니다.) `WITHIN GROUP` 앞의 인수 표현식이있는 경우 집계 인수와 구별하기 위해 직접 인수라고합니다. `order_by_clause` 에 나열되어 있습니다. 일반 집계 인수와 달리 직접 인수는 입력 행당 한 번이 아니라 집계 호출 당 한 번만 평가됩니다. 이는 변수가 `GROUP BY` 로 그룹화 된 경우에만 변수를 포함 할 수 있음을 의미합니다. 이 제한사항은 직접 인수가 집계 표현식 안에 전혀없는 것과 같습니다. 직접 인수는 일반적으로 백분위 수 분수와 같은 항목에 사용되며 집계 계산마다 단일 값으로 만 의미가 있습니다. 직접 인수 목록은 비어있을 수 있습니다. 이 경우 `(*)` 가 아닌 `()` 만 쓰십시오. PostgreSQL 은 실제로 철자를 허용하지만 첫 번째 방법 만 SQL 표준을 준수합니다.

순서 집합 집계 호출의 예는 다음과 같습니다.

```sql
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_cont
-----------------
           50489
```

이는 테이블 세대에서 `income` 칼럼의 50 번째 백분위 수 또는 중앙값을 얻습니다. 여기서 `0.5` 는 직접 인수입니다. 백분위 수 비율이 칼럼마다 다른 값이되는 것은 의미가 없습니다.

`FILTER` 가 지정되면 `filter_clause` 가 true 로 평가되는 입력 칼럼만 집계 함수에 제공됩니다. 다른 칼럼은 삭제됩니다. 예를 들면 다음과 같습니다.

```sql
SELECT
    count(*) AS unfiltered,
    count(*) FILTER (WHERE i < 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
         10 |        4
(1 row)
```

사전 정의 된 집계 함수는 [Section 9.20]() 에 설명되어 있습니다. 다른 집계 함수는 사용자가 추가 할 수 있습니다.

집계 표현식은 `SELECT` 명령의 결과 목록 또는 `HAVING` 절에만 나타날 수 있습니다. `WHERE` 와 같은 다른 절에서는 집계 결과가 형성되기 전에 해당 절이 논리적으로 평가되므로 금지됩니다.

하위 쿼리에 집계식이 나타나면 ([Section 4.2.11]() 및 [Section 9.22]() 참조) 집계는 일반적으로 하위 쿼리의 데이터에 대해 평가됩니다. 그러나 집계의 인수(`filter_clause` 가 있는 경우) 에 외부 레벨 변수 만 포함 된 경우 예외가 발생합니다. 그런 다음 집계는 가장 가까운 외부 레벨에 속하며 해당 쿼리의 행에 대해 평가됩니다. 전체 집계 표현식은 하위 쿼리에 대한 외부 참조이며 하위 쿼리에 대한 하나의 평가에 대해 상수 역할을 합니다. 결과 목록 또는 `HAVING` 절에만 표시되는 것에 대한 제한 사항은 집계가 속한 쿼리 레벨과 관련하여 적용됩니다.

### 4.2.8. Window Function Calls

윈도우 함수 호출은 쿼리에 의해 선택된 데이터의 일부에 대한 집계 유사 함수의 적용을 나타냅니다. 비 윈도우 집계 호출과 달리, 이것은 선택된 데이터를 단일 출력 데이터로 그룹화하는 것과 관련이 없습니다. 각 데이터는 쿼리 출력에서 분리되어 유지됩니다. 그러나 윈도우 함수는 윈도우 함수 호출의 그룹화 스펙 (`PARTITION BY` 목록) 에 따라 현재 데이터 그룹의 일부인 모든 데이터에 액세스 할 수 있습니다.

윈도우 함수 호출 구문은 다음 중 하나입니다.

```sql
function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
```

여기서 `window_definition` 에는 구문이 있습니다.

```sql
[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

`frame_clause` 는 다음 중 하나 일 수 있습니다.

```sql
{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
```

여기서 `frame_start` 및 `frame_end` 는 다음 중 하나 일 수 있습니다.

```sql
UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
```

`frame_exclusion` 은 다음 중 하나 일 수 있습니다.

```sql
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

여기서 `expression` 은 자체적으로 윈도우 함수 호출을 포함하지 않는 값 표현식을 나타냅니다.

`window_name` 은 쿼리의 `WINDOW` 절에 정의 된 명명 된 윈도우 사양에 대한 참조입니다. 또는 `WINDOW` 절에서 이름 지정된 윈도우를 정의 할 때와 동일한 구문을 사용하여 괄호 안에 전체 `window_definition` 을 제공 할 수 있습니다. 자세한 내용은 [SELECT]() 참조 페이지를 참조하시면 됩니다. `OVER wname` 이 `OVER (wname ...)` 와 정확히 일치하지는 않습니다. 후자는 윈도우 정의를 복사하고 수정하는 것을 의미하며 참조 된 윈도우 사양에 프레임 절이 포함되어 있으면 거부됩니다.

`PARTITION BY` 절은 쿼리 데이터를 파티션으로 그룹화하며, 이 데이터는 윈도우 함수에 의해 개별적으로 처리됩니다. `PARTITION BY` 는 항상 표현식이며 출력 칼럼 이름 또는 숫자 일 수 없다는 점을 제외하고 쿼리가 `GROUP BY` 절과 유사하게 작동합니다. `PARTITION BY` 가 없으면 쿼리에서 생성 된 모든 데이터가 단일 파티션으로 처리됩니다. `ORDER BY` 절은 파티션의 데이터가 윈도우 함수에 의해 처리되는 순서를 결정합니다. 쿼리는 `ORDER BY` 절과 유사하게 작동하지만 마찬가지로 출력 칼럼 이름 또는 숫자를 사용할 수 없습니다. `ORDER BY` 가 없으면 데이터는 지정되지 않은 순서로 처리됩니다.

`frame_clause` 는 전체 파티션 대신 프레임에서 작동하는 윈도우 함수에 대해 현재 파티션의 하위 세트 인 윈도우 프레임을 구성하는 데이터 세트를 지정합니다. 프레임의 데이터 세트는 현재 데이터인 데이터 행에 따라 달라질 수 있습니다. 프레임은 `RANGE`, `ROWS` 또는 `GROUPS` 모드에서 지정할 수 있습니다. 두 경우 모두 `frame_start` 에서 `frame_end` 까지 실행됩니다. `frame_end` 를 생략하면 끝은 `CURRENT ROW` 로 기본 설정됩니다.

`UNBOUNDED PRECEDING` 의 `frame_start` 는 프레임이 파티션의 첫 번째 데이터로 시작 함을 의미하며 `UNBOUNDED FOLLOWING` 의 `frame_end` 는 프레임이 파티션의 마지막 데이터로 끝남을 의미합니다.

`RANGE` 또는 `GROUPS` 모드에서 `CURRENT ROW` 의 `frame_start` 는 프레임이 현재 데이터의 첫 번째 피어 행 (윈도우의 `ORDER BY` 절이 현재 데이터와 동등한 것으로 정렬되는 행) 으로 시작하는 것을 의미하고 `CURRENT ROW` 의 `frame_end` 는 프레임이 종료됨을 의미합니다. 현재 데이터의 마지막 피어 행과 함께. `ROWS` 모드에서 `CURRENT ROW` 는 단순히 현재 행을 의미합니다.

`offset` `PRECEDING` 및 `offset` `FOLLOWING` 프레임 옵션에서 `offset` 은 변수, 집계 함수 또는 윈도우 함수를 포함하지 않는 표현식이어야합니다. `오프셋` 의 의미는 프레임 모드에 따라 다릅니다.

* `ROWS` 모드에서 `offset` 은 null 이 아닌 음이 아닌 정수를 가져와야하며 옵션은 프레임이 현재 데이터 앞 또는 뒤에 지정된 수의 데이터를 시작하거나 종료 함을 의미합니다.
* `GROUPS` 모드에서 `offset` 은 다시 null 이 아닌 음이 아닌 정수를 산출해야하며, 옵션은 프레임이 현재 데이터의 피어 그룹 전후에 지정된 피어 그룹 수를 시작하거나 종료 함을 의미합니다. 여기서 피어 그룹은 `ORDER BY` 순서와 동등한 데이터 세트. `GROUPS` 모드를 사용하려면 윈도우 정의에 `ORDER BY` 절이 있어야합니다.
* `RANGE` 모드에서 이러한 옵션을 사용하려면 `ORDER BY` 절이 정확히 하나의 칼럼을 지정해야합니다. `offset` 은 현재 데이터의 해당 칼럼 값과 프레임의 이전 또는 다음 데이터의 값 사이의 최대 차이를 지정합니다. `offset` 표현식의 데이터 유형은 순서 칼럼의 데이터 유형에 따라 다릅니다. 숫자 순서 칼럼의 경우 일반적으로 순서 칼럼과 동일한 유형이지만 날짜 시간 순서 칼럼의 경우 `interval` 입니다. 예를 들어, 주문 칼럼의 유형이 `date` 또는 `timestamp` 인 경우 `RANGE BETWEEN'1 day 'PRECEDING AND '10 days'FOLLOWING` 을 쓸 수 있습니다. 비록 *non-negative* 의 의미는 데이터 유형에 따라 다르지만 `offset` 은 여전히 null 이 아닌 음이 아닌 값이어야합니다.

어쨌든, 프레임 끝까지의 거리는 파티션 끝까지의 거리에 의해 제한되므로, 파티션 끝 근처의 데이터에 대해 프레임이 다른 곳보다 적은 데이터를 포함 할 수 있습니다.

`ROWS` 및 `GROUPS` 모드에서 0 `PRECEDING` 및 0 `FOLLOWING` 은 `CURRENT ROW` 와 같습니다. 이것은 일반적으로 *zero* 라는 적절한 데이터 유형별 의미를 위해 `RANGE` 모드에서도 유지됩니다.

`frame_exclusion` 옵션을 사용하면 현재 데이터 주위의 행을 프레임 시작 및 프레임 끝 옵션에 따라 포함하더라도 프레임에서 제외 할 수 있습니다. `EXCLUDE CURRENT ROW` 는 프레임에서 현재 데이터를 제외합니다. `EXCLUDE GROUP` 은 현재 데이터와 순서 피어를 프레임에서 제외합니다. `EXCLUDE TIES` 는 현재 데이터의 모든 피어를 프레임에서 제외하지만 현재 데이터 자체는 제외하지 않습니다. `EXCLUDE NO OTHERS` 는 단순히 현재 데이터 또는 해당 피어를 제외하지 않는 기본 동작을 명시적으로 지정합니다.

기본 프레이밍 옵션은 `RANGE UNBOUNDED PRECEDING` 이며, `UNBOUNDED PRECEDING AND CURRENT ROW` 사이의 범위와 같습니다. `ORDER BY` 를 사용하면 파티션 시작부터 현재 행의 마지막 `ORDER BY` 피어까지의 모든 행이되도록 프레임이 설정됩니다. `ORDER BY` 가 없으면 모든 행이 현재 행의 피어가되기 때문에 파티션의 모든 행이 윈도우 프레임에 포함됩니다.

제한 사항은 `frame_start` 가 `UNBOUNDED FOLLOWING` 이 될 수 없고 `frame_end` 가 `UNBOUNDED PRECEDING` 이 될 수 없으며 `frame_end` 선택이 `frame_start` 선택보다 `frame_start` 및 `frame_end` 옵션의 목록에서 더 일찍 나타날 수 없다는 것입니다. 예를 들어 현재 행과 오프셋 사이의 범위는 허용되지 않습니다. 그러나 행을 선택하지 않더라도 `ROWS BETWEEN 7 PRECEDING AND 8 PRECEDING` 은 허용됩니다.

`FILTER` 가 지정되면 `filter_clause` 가 true 로 평가되는 입력 행만 윈도우 함수에 제공됩니다. 다른 행은 삭제됩니다. 집계 된 윈도우 함수만 `FILTER` 절을 승인합니다.

내장 윈도우 기능은 [Table 9.60]() 에 설명되어 있습니다. 다른 윈도우 기능은 사용자가 추가 할 수 있습니다. 또한 *built-in*, *user-defined*, *general-purpose*, *statistical aggregate* 를 윈도우 함수로 사용할 수 있습니다. 

`*` 를 사용하는 구문은 `count (*) OVER (PARTITION BY x ORDER BY y)` 와 같이 매개 변수없는 집계 함수를 윈도우 함수로 호출하는 데 사용됩니다. 별표 (`*`) 는 일반적으로 윈도우 특정 기능에 사용되지 않습니다. 윈도우 특정 함수는 `DISTINCT` 또는 `ORDER BY` 를 함수 인수 목록 내에서 사용할 수 없습니다.

윈도우 함수 호출은 조회의 `SELECT` 목록 및 `ORDER BY` 절에서만 허용됩니다.

윈도우함수에 대한 더 많은 정보를 얻고 싶으면 [Section 3.5](), [Section 9.21](), [Section 7.2.5]() 를 확인하면 됩니다.

### 4.2.9. Type Casts

타입캐스트는 한 데이터 유형에서 다른 데이터 유형으로의 변환을 지정합니다. PostgreSQL 은 타입캐스트에 대해 두 가지 동등한 구문을 허용합니다.

```sql
CAST ( expression AS type )
expression::type
```

`CAST` 구문은 SQL 을 따릅니다. `::` 구문은 PostgreSQL 사용법입니다.

알려진 유형의 값 표현식에 타입캐스트가 적용되면 런타임 타입 변환을 나타냅니다. 적합한 타입 변환 작업이 정의된 경우에만 캐스트가 성공합니다. 이것은 [Chapter 4.1.2.7]() 에서 보여 지듯이 상수를 가진 캐스트를 사용하는 것과는 미묘한 차이가 있습니다. 비공식 문자열 리터럴에 적용된 캐스트는 리터럴 상수 값에 대한 타입의 초기 할당을 나타내므로 모든 타입에 대해 성공합니다 (문자열 리터럴의 내용이 데이터 유형에 허용되는 입력 구문 인 경우).

값 표현식이 생성해야하는 타입 (예 : 테이블 칼럼에 지정된 경우)에 대한 모호성이없는 경우 명시적 타입캐스트는 일반적으로 생략할 수 있습니다. 이 경우 시스템은 자동으로 타입 캐스트를 적용합니다. 그러나 자동 캐스트는 시스템 카탈로그에서 *OK to apply implicitly* 으로 표시된 캐스트에 대해서만 수행됩니다. 다른 캐스트는 명시적 캐스트 구문으로 호출해야합니다. 이 제한은 놀라운 전환이 자동으로 적용되지 않도록하기위한 것입니다.

함수형 구문을 사용하여 타입캐스트를 지정할 수도 있습니다.

```sql
typename ( expression )
```

그러나 이것은 이름이 함수 이름으로도 유효한 타입에 대해서만 작동합니다. 예를 들어 `double precision` 는 이런 식으로 사용할 수 없지만 `float8` 은 사용할 수 있습니다. 또한 `interval`, `time` 및 `timestamp` 라는 이름은 구문 충돌로 인해 큰 따옴표로 묶인 경우에만 이러한 방식으로 사용할 수 있습니다. 따라서 함수형 캐스트 구문을 사용하면 불일치가 발생하므로 피해야합니다.

> Note : 함수와 유사한 구문은 실제로 함수 호출입니다. 두 가지 표준 캐스트 구문 중 하나를 사용하여 런타임 변환을 수행하면 내부적으로 등록 된 함수를 호출하여 변환을 수행합니다. 관례상 이러한 변환 함수는 출력 타입과 이름이 같으므로 *function-like syntax* 은 기본 변환 함수를 직접 호출하는 것에 지나지 않습니다. 휴대용 응용프로그램이 의존해야하는 것이 아닙니다.

### 4.2.10. Collation Expressions

`COLLATE` 절은 표현식의 콜레이션을 대체합니다. 적용되는 표현식에 추가됩니다.

```sql
expr COLLATE collation
```

여기서 `collation` 은 가능한 스키마 규정 식별자입니다. `COLLATE` 절은 연산자보다 밀접하게 바인딩됩니다. 필요한 경우 괄호를 사용할 수 있습니다.

데이터 정렬을 명시적으로 지정하지 않으면 데이터베이스 시스템은 식에 포함 된 칼럼에서 데이터 정렬을 파생 시키거나 식에 칼럼이 포함되지 않은 경우 데이터베이스의 기본 데이터 정렬을 기본값으로 사용합니다.

`COLLATE` 절의 두 가지 일반적인 용도는 `ORDER BY` 절에서 정렬 순서를 대체하는 것입니다. 예를 들면 다음과 같습니다.

```sql
SELECT a, b, c FROM tbl WHERE ... ORDER BY a COLLATE "C";
```

예를 들어, *locale-sensitive* 결과를 가지는 함수나 연산자 호출의 콜레이션을 무시한다.

```sql
SELECT * FROM tbl WHERE a > 'foo' COLLATE "C";
```

후자의 경우 `COLLATE` 절은 우리가 영향을 줄 연산자의 입력 인수에 첨부됩니다. `COLLATE` 절이 첨부 된 연산자 또는 함수 호출의 인수는 중요하지 않습니다. 연산자 또는 함수에 의해 적용되는 데이터 정렬은 모든 인수를 고려하여 파생되므로 명시적 `COLLATE` 절은 다른 모든 데이터 정렬을 무시합니다. 인수. (그러나 일치하지 않는 `COLLATE` 절을 둘 이상의 인수에 첨부하는 것은 오류입니다. 자세한 내용은 [Section 23.2]() 을 참조하십시오.) 따라서 이전 예제와 동일한 결과가 나타납니다.

```sql
SELECT * FROM tbl WHERE a COLLATE "C" > 'foo';
```

하지만 아래는 에러가 발생합니다. 

```sql
SELECT * FROM tbl WHERE (a > 'foo') COLLATE "C";
```

데이터 정렬이 불가능한 데이터 유형 부울 `>` 연산자의 결과에 데이터 정렬을 적용하려고 시도하기 때문입니다.

### 4.2.11. Scalar Subqueries

스칼라 하위 쿼리는 괄호로 묶인 일반적인 `SELECT` 쿼리로 하나의 칼럼으로 정확히 하나의 행을 반환합니다. 쿼리 작성에 대한 내용은 [Chapter 7]() 을 참조하십시오. `SELECT` 쿼리가 실행되고 단일 반환 값이 주변 값 식에 사용됩니다. 스칼라 서브 쿼리로 둘 이상의 행 또는 둘 이상의 칼럼을 리턴하는 쿼리를 사용하는 것은 오류입니다. 그러나 특정 실행 중에 하위 쿼리가 행을 반환하지 않으면 오류가 없습니다. 스칼라 결과는 null 로 간주됩니다. 하위 쿼리 서브 쿼리와 관련된 다른 표현에 대해서는 [Section 9.22]() 을 참조하십시오.

예를 들어 다음은 각 주에서 가장 큰 도시 인구를 찾습니다.

```sql
SELECT name, (SELECT max(pop) FROM cities WHERE cities.state = states.name)
    FROM states;
```

### 4.2.12. Array Constructors

배열 생성자는 멤버 요소의 값을 사용하여 배열 값을 작성하는 표현식입니다. 간단한 배열 생성자는 키워드 `ARRAY`, 왼쪽 대괄호 `[`, 배열 요소 값에 대한 표현식 목록 (쉼표로 구분) 및 오른쪽 대괄호 `]` 로 구성됩니다. 예를 들면 다음과 같습니다.

```sql
SELECT ARRAY[1,2,3+4];
  array
---------
 {1,2,7}
(1 row)
```

기본적으로 배열 요소 유형은 `UNION` 또는 `CASE` 구문과 동일한 규칙을 사용하여 결정되는 멤버 표현식의 공통 유형입니다 ([Section 10.5]() 참조). 배열 생성자를 원하는 형식으로 명시적으로 캐스팅하여 재정의 할 수 있습니다. 예를 들면 다음과 같습니다.

```sql
SELECT ARRAY[1,2,22.7]::integer[];
  array
----------
 {1,2,23}
(1 row)
```

이는 각 표현식을 배열 요소 유형에 개별적으로 캐스트하는 것과 동일한 효과를 갖습니다. 캐스팅에 대한 자세한 내용은 [Section 4.2.9]() 를 참조하십시오.

배열 생성자를 중첩하여 다차원 배열 값을 작성할 수 있습니다. 내부 생성자에서 키워드 `ARRAY` 는 생략 할 수 있습니다. 예를 들어 다음과 같은 결과가 생성됩니다.

```sql
SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)

SELECT ARRAY[[1,2],[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)
```

다차원 배열은 직사각형이어야하므로 같은 수준의 내부 생성자는 같은 차원의 하위 배열을 생성해야합니다. 외부 `ARRAY` 생성자에 적용된 캐스트는 모든 내부 생성자에게 자동으로 전파됩니다.

다차원 배열 생성자 요소는 하위 `ARRAY` 구문뿐만 아니라 적절한 종류의 배열을 생성하는 모든 것이 될 수 있습니다. 예를 들면 다음과 같습니다.

```sql
CREATE TABLE arr(f1 int[], f2 int[]);

INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], ARRAY[[5,6],[7,8]]);

SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
                     array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
(1 row)
```

하위 쿼리는 단일 칼럼을 반환해야합니다. 하위 쿼리의 출력 열이 배열이 아닌 유형 인 경우 결과 1 차원 배열은 하위 쿼리 결과의 각 행에 대한 요소를 가지며 하위 요소의 출력 열과 일치하는 요소 유형을 갖습니다. 하위 쿼리의 출력 열이 배열 유형 인 경우 결과는 동일한 유형이지만 하나의 차원이 더 큰 배열이됩니다. 이 경우 모든 하위 쿼리 행은 동일한 차원의 배열을 생성해야합니다. 그렇지 않으면 결과가 직사각형이 아닙니다.

`ARRAY` 로 작성된 배열 값의 첨자는 항상 1 로 시작합니다. 배열에 대한 자세한 내용은 [Section 8.15]() 을 참조하십시오.

### 4.2.13. Row Constructors

행 생성자는 멤버 필드 값을 사용하여 행 값 (복합 값이라고도 함)을 작성하는 표현식입니다. 행 생성자는 키워드 `ROW`, 왼쪽 괄호, 행 필드 값에 대한 0 개 이상의 표현식 (쉼표로 구분) 및 마지막으로 오른쪽 괄호로 구성됩니다. 예를 들면 다음과 같습니다.

```sql
SELECT ROW(1,2.5,'this is a test');
```

키워드 `ROW` 는 목록에 둘 이상의 표현식이있는 경우 선택 사항입니다.

행 생성자는 `rowvalue.*` 구문을 포함 할 수 있습니다. 이 구문은 `.*` 구문이 `SELECT` 목록의 최상위 레벨에서 사용될 때와 같이 행 값의 요소 목록으로 확장됩니다. ([Section 8.16.5]()) 예를 들어, 테이블 `t` 에 열 `f1` 및 `f2` 가있는 경우 이들은 동일합니다.

```sql
SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

> Note : PostgreSQL 8.2 이전에는 `.*` 구문이 행 생성자에서 확장되지 않았으므로 `ROW (t. *, 42)` 를 작성하면 첫 번째 필드가 다른 행 값인 *two-field* 행이 작성되었습니다. 새로운 동작이 일반적으로 더 유용합니다. 중첩 된 행 값의 이전 동작이 필요한 경우. `*` 없이 내부 행 값을 작성하면 됩니다. (예 : `ROW (t, 42)`).

기본적으로 `ROW` 표현식으로 작성된 값은 익명 레코드 유형입니다. 필요한 경우 명명 된 복합 유형 (테이블의 행 유형 또는 `CREATE TYPE AS` 로 작성된 복합 유형)으로 캐스트 할 수 있습니다. 모호성을 피하기 위해 명시적인 캐스트가 필요할 수 있습니다. 예를 들면 다음과 같습니다.

```sql
CREATE TABLE mytable(f1 int, f2 float, f3 text);

CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- No cast needed since only one getf1() exists
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
     1
(1 row)

CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);

CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- Now we need a cast to indicate which function to call:
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR:  function getf1(record) is not unique

SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
     1
(1 row)

SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS myrowtype));
 getf1
-------
    11
(1 row)
```

행 생성자는 복합 유형 테이블 칼럼에 저장되거나 복합 매개 변수를 허용하는 함수에 전달 될 복합 값을 빌드하는 데 사용될 수 있습니다. 또한 두 개의 데이터 값을 비교하거나 `IS NULL` 또는 `IS NOT NULL` 로 행을 테스트 할 수 있습니다. 예를 들면 다음과 같습니다.

자세한 내용은 [Section 9.23]() 을 참조하십시오. [Section 9.22]() 에서 논의 된 것처럼 행 생성자는 서브 쿼리와 관련하여 사용될 수도 있습니다.

### 4.2.14. Expression Evaluation Rules

하위 표현식의 평가 순서는 정의되어 있지 않습니다. 특히, 연산자 또는 함수의 입력이 반드시 왼쪽에서 오른쪽 또는 다른 고정 된 순서로 평가 될 필요는 없습니다.

또한 표현식의 일부만 평가하여 표현식의 결과를 판별 할 수 있으면 다른 하위 표현식이 전혀 평가되지 않을 수 있습니다. 예를 들어, 다음과 같이 쓴 경우 입니다.

```sql
SELECT true OR somefunc();
```

그러면 `somefunc()` 이 전혀 호출되지 않을 것입니다. 다음과 같이 쓴 경우에도 마찬가지입니다.

```sql
SELECT somefunc() OR true;
```

이것은 일부 프로그래밍 언어에서 발견되는 부울 연산자의 왼쪽에서 오른쪽으로의 *short-circuiting* 과 동일하지 않습니다.

결과적으로 부작용이있는 함수를 복잡한 표현의 일부로 사용하는 것은 현명하지 않습니다. `WHERE` 및 `HAVING` 절에서 부작용 또는 평가 순서에 의존하는 것이 특히 위험합니다. 이러한 절은 실행 계획 개발의 일부로 광범위하게 재처리되기 때문입니다. 해당 절의 부울 표현식 (`AND` / `OR` / `NOT` 조합)은 부울 대 수법에 의해 허용되는 방식으로 재구성 할 수 있습니다.

평가 순서를 강제해야하는 경우 `CASE` 구문 ([Section 9.17]() 참조)을 사용할 수 있습니다. 예를 들어, `WHERE` 절에서 0 으로 나누지 않으려는 신뢰할 수 없는 방법입니다.

```sql
SELECT ... WHERE x > 0 AND y/x > 1.5;
```

하지만 다음은 안전합니다.

```sql
SELECT ... WHERE CASE WHEN x > 0 THEN y/x > 1.5 ELSE false END;
```

이 방식으로 사용 된 `CASE` 구문은 최적화 시도를 무효화하므로 필요할 때만 수행해야합니다. (이 특정 예에서는 `y > 1.5 * x` 를 대신 써서 문제를 회피하는 것이 좋습니다.)

그러나 `CASE` 는 이러한 문제에 대한 해결책은 아닙니다. 위에서 설명한 기술의 한 가지 제한은 상수 하위 표현식의 조기 평가를 방해하지 않는다는 것입니다. [Section 37.7]() 에 설명 된대로 `IMMUTABLE` 로 표시된 기능 및 연산자는 쿼리를 실행할 때가 아니라 쿼리를 계획 할 때 평가할 수 있습니다. 따라서 예를 들어 보겠습니다.

```sql
SELECT CASE WHEN x > 0 THEN x ELSE 1/0 END FROM tab;
```

테이블의 모든 행에 `x > 0` 이 있어도 `ELSE` 가 런타임에 입력되지 않더라도 상수 하위 표현식을 단순화하려는 플래너로 인해 *division-by-zero* 가 실패 할 수 있습니다.

이 특정 예제는 어리석은 것처럼 보일 수 있지만 함수 인수 및 로컬 변수의 값은 계획 목적을 위해 상수로 쿼리에 삽입 될 수 있으므로 함수 내에서 실행되는 쿼리에서 분명히 상수를 포함하지 않는 관련 사례가 발생할 수 있습니다. 예를 들어 PL / pgSQL 함수 내에서 `IF`-`THEN`-`ELSE` 문을 사용하여 위험한 계산을 보호하는 것은 `CASE` 표현식에 중첩시키는 것보다 훨씬 안전합니다.

동일한 유형의 또 다른 제한 사항은 `CASE` 가 `SELECT` 목록 또는 `HAVING` 절의 다른 표현식을 고려하기 전에 집계 표현식이 계산되기 때문에 `CASE` 에 포함 된 집계 표현식의 평가를 막을 수 없다는 것입니다. 예를 들어 다음 쿼리는 겉보기에 대해 보호 된 것처럼 보이지만 0 으로 나누기 오류가 발생할 수 있습니다.

```sql
SELECT CASE WHEN min(employees) > 0
            THEN avg(expenses / employees)
       END
    FROM departments;
```

`min()` 및 `avg()` 집계는 모든 입력 행에 대해 동시에 계산되므로 `employes` 행에 0 인 행이 있으면 `min()` 결과를 테스트 할 기회가 있기 전에 *division-by-zero* 오류가 발생합니다. 대신 `WHERE` 또는 `FILTER` 절을 사용하여 문제가있는 입력 행이 처음에 집계 함수에 접근하지 못하게하면 됩니다.




