---
title : PostgreSQL Chapter 4. SQL Syntax
tags :
- PostgreSQL
---

## 4.3. Calling Functions

* [4.3.1. Using Positional Notation](#431-using-positional-notation)
* [4.3.2. Using Named Notation](#432-using-named-notation)
* [4.3.3. Using Mixed Notation](#433-using-mixed-notation)

PostgreSQL 에서는 이름이 지정된 매개변수가있는 함수를 `positional` 또는 `named` 표기법을 사용하여 호출 할 수 있습니다. 명명된 표기법은 매개변수와 실제 인수 사이의 연관성을보다 명확하고 안정적으로 만들기 때문에 많은 매개 변수가있는 함수에 특히 유용합니다. 위치 표기법에서 함수 호출은 함수 선언에 정의 된 순서대로 인수 값으로 작성됩니다. 명명된 표기법에서 인수는 이름별로 함수 매개 변수와 일치하며 순서에 관계없이 작성할 수 있습니다. 각 표기법에 대해 [Section 10.3]() 에 설명된 함수 인수 유형의 영향도 고려하십시오.

두 표기법에서 함수 선언에 제공된 기본값을 가진 매개 변수는 호출에 전혀 쓸 필요가 없습니다. 그러나 이는 매개 변수 조합을 생략 할 수 있으므로 명명 된 표기법에 특히 유용합니다. 위치 표기법에서 매개 변수는 오른쪽에서 왼쪽으로 만 생략 할 수 있습니다.

PostgreSQL은 위치 표기법과 이름 표기법을 결합한 혼합 표기법도 지원합니다. 이 경우 위치 매개 변수가 먼저 기록되고 이름 지정된 매개 변수가 그 뒤에 나타납니다.

다음 예제는 다음 함수 정의를 사용하여 세 가지 표기법의 사용법을 보여줍니다.

```sql
CREATE FUNCTION concat_lower_or_upper(a text, b text, uppercase boolean DEFAULT false)
RETURNS text
AS
$$
 SELECT CASE
        WHEN $3 THEN UPPER($1 || ' ' || $2)
        ELSE LOWER($1 || ' ' || $2)
        END;
$$
LANGUAGE SQL IMMUTABLE STRICT;
```

`concat_lower_or_upper` 함수에는 두 개의 필수 매개변수 `a` 와 `b` 가 있습니다. 또한 기본적으로 `false` 로 설정되는 선택적 매개변수 `uppercase` 가 있습니다. `a` 및 `b` 입력은 연결되고 대문자 매개 변수에 따라 대문자 또는 소문자로 강제 설정됩니다. 이 함수 정의의 나머지 세부 사항은 여기서 중요하지 않습니다 (자세한 내용은 [Chapter 37]() 참조).

### 4.3.1. Using Positional Notation

위치 표기법은 PostgreSQL 의 함수에 인수를 전달하는 일반적인 메커니즘입니다. 예를 들면 다음과 같습니다.

```sql
SELECT concat_lower_or_upper('Hello', 'World', true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

모든 인수는 순서대로 지정됩니다. `uppercase` 가 `true` 로 지정되므로 결과는 대문자입니다. 다른 예는 다음과 같습니다.

```sql
SELECT concat_lower_or_upper('Hello', 'World');
 concat_lower_or_upper 
-----------------------
 hello world
(1 row)
```

여기서 `uppercase` 매개변수는 생략되므로 기본값 `false` 를 수신하여 소문자 출력이 발생합니다. 위치 표기법에서 인수는 기본값이있는 한 오른쪽에서 왼쪽으로 생략할 수 있습니다.

### 4.3.2. Using Named Notation

명명 된 표기법에서 각 인수의 이름은 `=>` 를 사용하여 인수 표현식과 구분하여 지정됩니다. 예를 들면 다음과 같습니다.

```sql
SELECT concat_lower_or_upper(a => 'Hello', b => 'World');
 concat_lower_or_upper 
-----------------------
 hello world
(1 row)
```

대문자 `uppercase` 는 생략되었으므로 암시적으로 `false` 로 설정됩니다. 명명된 표기법을 사용하면 다음과 같은 순서로 인수를 지정할 수 있다는 이점이 있습니다.

```sql
SELECT concat_lower_or_upper(a => 'Hello', b => 'World', uppercase => true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)

SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b => 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

`:=` 에 기반한 구문은 이전 버전과의 호환성을 위해 지원됩니다.

```sql
SELECT concat_lower_or_upper(a := 'Hello', uppercase := true, b := 'World');
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

### 4.3.3. Using Mixed Notation

혼합 표기법은 위치 표기법과 명명된 표기법을 결합합니다. 그러나 이미 언급했듯이 명명된 인수는 위치 인수 앞에 올 수 없습니다. 예를 들면 다음과 같습니다.

```sql
SELECT concat_lower_or_upper('Hello', 'World', uppercase => true);
 concat_lower_or_upper 
-----------------------
 HELLO WORLD
(1 row)
```

위의 쿼리에서 인수 `a` 와 `b` 는 위치 적으로 지정되고 `uppercase` 는 이름으로 지정됩니다. 이 예제에서는 문서를 제외하고 거의 추가하지 않습니다. 명명된 또는 혼합 표기법은 기본값을 갖는 수많은 매개 변수를 갖는보다 복잡한 함수를 사용하면 많은 양의 쓰기를 저장하고 오류 가능성을 줄일 수 있습니다.

> Note : 집계 함수를 호출 할 때는 현재 이름이 지정된 혼합 호출 표기법을 사용할 수 없습니다 (단, 집계 함수가 창 함수로 사용될 때는 작동합니다).