---
title : PostgreSQL Chapter 3. Advanced Features
tags :
- PostgreSQL
---

## 3.4. Transactions

**트랜잭션(Transaction)** 이란 데이터베이스 시스템에서 기본적인 하나의 개념입니다. 트랜잭션의 핵심은 여러 작업을 하나의 작업으로 묶는 것입니다. 각각의 트랜잭션은 모두 독립적으로 작동하며, 동시에 발생한 트랜잭션에 대해서는 그 트랜잭션 안에서의 데이터만 적용이 됩니다. 만약 트랜잭션안에서 작업 도중 오류가 발생한다면, 이전에 적용되었던 모든 작업은 취소됩니다.

예를 들어, 다양한 고객 계정에 대한 잔액과 은행 지점에 대한 총 예금 잔액이 포함 된 은행 데이터베이스가 있다고 생각해보겠습니다. Alice 계정에서 Bob 계정으로 100 $ 를 지불하겠습니다. 이것을 간단하게 구현하면 다음과 같이 사용할 수 있습니다.

```sql
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
UPDATE branches SET balance = balance - 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Alice');
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
UPDATE branches SET balance = balance + 100.00
    WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Bob');
```

위 SQL 의 세부사항은 중요하지 않습니다. 하지만, 중요한 사항은 이체를 처리하기 위해서 4 개의 독립된 `UPDATE` 구문을 사용한다는 것입니다. 위 작업을 수행하는데, 만약 부분적으로 작업을 성공하고, 나머지는 실패한다면, 각 계좌에 남아있는 금액은 이상해지므로, 모든 작업이 수행되거나 전부 취소되어야합니다. 이 문제를 트랜잭션을 그룹화하여 문제를 해결할 수 있습니다. 이를 트랜잭션의 **원자성(Atomic)** 이라고 합니다. 다른 트랜잭션 관점에서보면 모두 처리되거나 아예 실행되지 않습니다.

또한, 데이터베이스 시스템에서 트랜잭션을 완료된 후에 데이터가 업데이트 되어 이후에 충돌이 발생하더라도 데이터 손실을 보장해야합니다. 예를 들어, Bob 이 현금 인출을 진행하는 사이에도, Bob 에게 현금을 줄 때까지 어떠한 오류도 발생하면 안됩니다. 트랜잭션 기능을 제공하는 데이터베이스에서는 트랜잭션이 정상적으로 종료되었다고 알려주기 전에 이미 하나의 트랜잭션에서 발생하는 모든 작업들은 영구저장장치(예, 하드디스크)에 기록을 해둡니다. 이를 **영속성(durability)** 이라고 합니다.

트랜잭션의 또 다른 속성 중 하나는 원자성과 관련이 있습니다. 여러 트랜잭션이 동시에 실행이 되는 경우, 각 트랜잭션이 다른 트랜잭션을 간섭할 수 없어야 합니다. 즉, 다른 트랜잭션에 의해 변경되고 있는 자료를에 대해서 참조할 수 없어야합니다. 이것을 **고립성(Isolation)** 이라 합니다. 예를 들어서, 모든 계좌의 현잔액 합계를 구하는 트랜잭션이 작업 중인데, Alice 나 Bob 의 현 잔액을 바꾸는 다른 트랜잭션에 의해서 그 계좌의 현 잔액이 바뀌게 된다면, 그 시점의 정확한  현 잔액 합계를 구할 수가 없게됩니다. 그래서, 트랜잭션은 각각의 명령이 수행 될 때 마다 그 변경 사항이 데이터베이스의 원래 자료에 영향을 주는 것이 아니라, 트랜잭션 영역안에 있는 모든 작업이 끝났을 때, 한꺼번에 그 변경 사항이 데이터베이스에 적용됩니다. 이때부터 다른 트랜잭션이 그 변경된 데이터를 참조 할 수 있게 됩니다. 이를 **정합성(Consistency)** 이라 합니다.

PostgreSQL 에서 트랜잭션 작업을 하려면, 작업을 `BEGIN` 명령과 `COMMIT` 명령안에 작성하면됩니다. 다음과 같은 형태가 트랙잭션을 사용하는 예입니다.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
-- etc etc
COMMIT;
```

트랜잭션을 도중에 커밋하지 않기로 결정한 경우 (아마도 Alice의 잔액이 마이너스) `COMMIT` 대신 `ROLLBACK` 명령을 실행할 수 있으며 지금까지의 모든 업데이트가 취소됩니다.

PostgreSQL은 실제로 모든 SQL 문을 트랜잭션 내에서 실행되는 것으로 취급합니다. `BEGIN` 명령을 명시적으로 작성하지 않앗다고 해도 실행하고자 하는 SQL 문 앞 뒤에 `BEGIN` 과 `COMMIT` 구문이 감싸집니다. `BEGIN` 과 `COMMIT` 으로 둘러싸인 SQL 문을 트랜잭션 블록이라고도합니다.

> Note : 몇몇 클라이언트 라이브러리는 자동으로 `BEGIN`, `COMMIT` 명령을 포함해서 실행되기 때문에, 사용자가 트랜잭션 지정하면 오류를 내는 경우도 있습니다. 자세한 것은 해당 라이브러리 문서를 참조하십시오.

**savepoints** 를 사용하여 트랜잭션의 명령문을보다 세분화 된 방식으로 제어 할 수 있습니다. savepoint 를 사용하면 나머지 부분을 커밋하면서 트랜잭션 작업의 일부를 보장할 수 있습니다. `SAVEPOINT` 로 정의한 후 필요한 경우 `ROLLBACK TO` 를 사용하여 savepoint 로 롤백 할 수 있습니다. savepoint 와 롤백 사이의 모든 트랜잭션 데이터베이스 변경 사항은 버려지지만 savepoint 이전의 변경 사항은 유지됩니다.

savepoint 로 롤백이 된 후에는 savepoint 가 계속 정의되어 있으므로, 여러번 롤백할 수 있습니다. 반대로, 특정 savepoint 로 다시 롤백할 필요가 없을 시, 이를 해제하여 할당된 시스템 자원을 회수할 수 있습니다. 주의 할 사항은 특정 savepoint 로 돌아갈 경우 그 지점 이후에 지정해 두었던 다른 savepoint 들도 모두 취소 되어 사라져버린다는 점입니다.

이 모든 것이 트랜잭션 블록 내에서 일어나므로 다른 데이터베이스 세션에서는 확인할 수 없습니다. 트랜잭션이 커밋된다면 커밋된 작업은 다른 세션에대해 표시가 되지만, 롤백 된 작업은 표시가되지 않아서 확인할 수 없습니다.

다음 예제는 윗 은행 거래 예제를 다시 savepoint 사용과 함께 구현해 본 것입니다.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
-- oops ... forget that and use Wally's account
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Wally';
COMMIT;
```

이 예제는 처음처럼 Alice 계좌에서 출금을 하고, Bob 계좌로 잘못 입금해서 `ROLLBACK TO` 명령으로 입금 전 상태로 되돌리고, 다시 바른 입금 처리를 하고, 트랜잭션을 커밋하는 것을 보여주는 것입니다. 

위 예제는 단순하지만, savepoint 를 이용하여 트랜잭션 블록에서 많은 제어가 가능합니다. 또한,  오류로 인해 시스템이 중단 상태에 놓였던 트랜잭션 블록에 제어권을 얻기위해선 `ROLLBACK TO` 하는 방법밖에 없습니다.