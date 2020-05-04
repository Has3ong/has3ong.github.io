---
title : MongoDB Connecting to a Replica Set from Your Application
tags :
- Replica Set
- MongoDB
- Database
---

*이 포스트는 [MongoDB: The Definitive Guide](https://github.com/wuzhouhui/misc/blob/master/programming/db/MongoDB.The.Definitive.Guide.pdf) 를 바탕으로 작성하였습니다.*

## Client-to-Replica-Set Connection Behavior

어플리케이션 관점에서 복제 셋은 독립 실행형 서버처럼 동작합니다. 기본적으로 클라이언트 라이브러리는 프라이머리에 연결되고 모든 트래픽을 프라이머리에 라우팅합니다. 어플리케이션은 복제 셋이 조용히 백그라운드에서 대기 상태를 유지하는 동안 마치 독립 실행형 서버와 통신하는 것처럼 읽기와 쓰기를 수행할 수 있습니다.

복제 셋에 대한 연결은 단일 서버에 대한 연결과 비슷합니다. 드라이버에서 MongoClient 에 상응하는 것을 사용하고, 연결할 드라이버를 위한 시드의 목록을 제공합니다. 시드는 복제 셋의 멤버입니다. 모든 멤버를 나열할 필요는 없습니다. 드라이버가 시드에 연결되었을 때 그 시드로부터 다른 멤버들을 발견할 것입니다. 연결 문자열은 보통 다음과 같습니다.

```shell
"mongodb://server-1:27017,server-2:27017"
```

프라이머리가 다운되었을 때 드라이버는 자동적으로 새로운 프라이머리를 발견하고 가능한 한 빨리 그 프라이머리로 요청을 라우팅합니다. 그러나 프라이머리에 도달할 수 없는 동안에는 어플리케이션이 쓰기를 수행할 수 없습니다.

짧은 시간 또는 연장된 시간동안에 이용 가능한 프라이머리는 존재하지 않습니다. 기본적으로 드라이버는 이 기간 동안 어떤 요청에 대해서도 처리하지 않습니다. 그러나 읽기 요청에 대해서는 선택적으로 세컨더리를 이용할 수 있습니다.

드라이버에대한 일반적인 바람은 사용자로부터 드라이버를 전체 선출 과정의 뒤로 숨기는 것입니다. 이는 많은 경우 가능하지 않거나 바람직하지 않기 때문에, 드라이버도 이런 방식으로 장애 복구를 처리하지 않습니다. 첫째로 드라이버는 오랫동안 프라이머리의 부재를 숨길 수 있습니다. 복제 셋은 프라이머리 없이 영원히 존재할 수 있습니다. 둘째로 드라이버는 종종 연산 실패로 프라이머리가 다운되었음을 발견하며, 이는 드라이버가 프라이머리가 다운되기 전에 해당 연산을 수행했는지 아닌지 알지 못합니다. 그러므로 드라이버는 사용자의 몫으로 남겨둡니다.

* 새로운 프라이머리가 빠르게 선출되면 그 프라이머리에서 해당 연산을 다시 수행하기를 원하는가
* 연산이 이전 프라이머리에서 이뤄진 것이라 추정하는가
* 새로운 프라이머리가 해당 연산을 가지고 확인하는가

어플리케이션에 따라 사용자 정의 솔루션을 제작할 수는 있지만, 서버에 문제가 생기기전까지 연산이 성공했는지 아닌지 확인하는 방법은 없습니다. 예를 들어 드라이버가 문서 `{"_id":1}` 을 입력하고 프라이머리가 손상되었다는 오류를 받으면, 새롭게 선출된 프라이머리에 재접속을 시도하고 `{"id":1}` 이 존재하는지 아닌지 확인합니다.

## Waiting for Replication on Writes

쓰기가 성공적으로 수행되었는지 확인하기 위해 `getLastError` 명령어를 사용했습니다. 쓰기가 세컨더리로 복제되었는지 확인하기 위해 동일한 명령어를 사용할 수 있습니다. `w` 매개변수는 `getLastError` 가 주어진 수의 멤버들이 마지막 쓰기를 할 때까지 기다립니다.

MongoDB 는 `w` 매개변수에 이를 전달할 수 있도록 해 주는 특수 키워드 `majority` 를 가지며 쉘에서는 다음처럼 보입니다.

```js
> db.runCommand({"getLastError" : 1, "w" : "majority"})
{
    "n" : 0,
    "lastOp" : Timestamp(1346790783000, 1),
    "connectionId" : 2,
    "writtenTo" : [
        { "_id" : 0 , "host" : "server-0" },
        { "_id" : 1 , "host" : "server-1" },
        { "_id" : 3 , "host" : "server-3" }
    ],
    "wtime" : 76,
    "err" : null,
    "ok" : 1
}
```

`getLastError` 의 출력 겨로가에 새로운 필드인 `writtenTo` 가 존재하는걸 알 수 있습니다. 이는 `w` 옵션을 사용할 때만 존재하며 마지막 연산이 복제된 서버의 목록을 보여줍니다.

위 명령을 실행하지만, 오직 프라이머리와 아비터만이 살아 있는 상태라고 가정합니다. 프라이머리는 쓰기를 복제 셋의 다른 어떤 멤버에도 복제할 수 없습니다. `getLastError` 는 얼마나 오랫동안 복제를 위해 대기해야 하는지 모르기 때문에 영원히 이를 기다립니다.

그러므로 항상 `wtimeout` 을 합리적인 값으로 설정해야 합니다. `wtimeout` 은 `getLastError` 의 또 다른 옵션이며, MongoDB 가 지정된 시간 안에 `w` 멤버에 복제할 수 없었다는 실패를 알리기 전에 얼마나 오랫동안 명령어가 대기해야 하는지 밀리세컨드 단위로 명시합니다.

아래 코드는 명령 수행을 포기하기 전에 1 초 동안 대기합니다.

```js
> db.runCommand({"getLastError" : 1, "w" : "majority", "wtimeout" : 1000})
```

이 명령은 여러가지 이유로 실패합니다.

다른 멤버가 다운 또는 지체되거나 네트워크 문제로 이용 불가능한 상태일 수도 있습니다. 만약 `getLastError` 가 시간을 초과하면, 어플리케이션은 다음에 무엇을 할지 결정해야 합니다. `getLastError` 가 시간을 초과했다는 것이 쓰기를 실패했다는 의미는 아닙니다. 단지 명시된 시간에 복제가 충분히 이뤄지지 못했음을 의미합니다. 쓰기는 여전히 모든 서버에 존재하며, 가능한 빨리 복제 셋의 다른 멤버에 전달합니다.

만약 어플리케이션이 합리적이고 견고하기를 원하면, `getLastError` 를 `majority` 그리고 적절한 타임아웃 값과 함께 규칙적으로 호출합니다. 이와 같은 호출이 시간을 초과하기 시작하면, 설정상의 문제가 무엇인지 살펴보겠습니다.

### What Can Go Wrong?

어플리케이션이 프라이머리로 쓰기를 보낸다고 가정하겠습니다. `getLastError` 를 호출하고 쓰기가 완료되었다는 확인을 받았지만, 모든 세컨더리가 쓰기를 복제할 수 있는 기회를 가지고 프라이머리에 문제가 생겼습니다.

어플리케이션은 해당 쓰기에 접근할 수 있다 생각하는데, 복제 셋의 멤버들은 해당 쓰기에 대한 복제본을 가지고 있지 않습니다.

어떤 시점에 세컨더리는 프라이머리로 선출되고, 새로운 쓰기를 시작합니다. 프라이머리가 다시 돌아오면, 프라이머리가 수행하지 않은 쓰기를 가지고 있음을 발견합니다. 이 문제를 해결하기 위해 현재 프라이머리의 연산 순서와 일치하지 않는 모든 쓰기를 취소합니다. 이러한 연산들은 손실되지 않지만 현재 프라이머리에 수동적으로 적용하기 위해 특수한 rollback 파일에 씁니다. 사고 이후로 발생한 다른 쓰기와의 충돌 때문에 MongoDB 는 자동적으로 이러한 쓰기를 적용하지 못합니다. 그러므로 관리자가 현재 프라이머리에 rollback 파일을 적용할 수 있는 기회를 얻기 전까지 쓰기는 기본적으로 사라집니다.

과반수에 쓰기를 하는 것이 이 상황을 예방할 수 있습니다. 어플리케이션이 처음에 `w : majority` 를 사용했고, 쓰기가 성공했다는 확인을 받으면, 새로운 프라이머리는 선출되기 위해 해당 쓰기의 복제본을 가져야 합니다. 만약 `getLastError` 가 실패하면 프라이머리가 손상되기 전에 복제 셋의 과반수에 쓰기를 전달하지 못한 것으로 가정하고 어플리케이션은 `getLastError` 를 다시 시도합니다.

### Other Options for “w”

`majority` 는 `getLastError` 를 통과하기 위한 유일한 옵션은 아니며, MongoDB 는 아래와 같이 `w` 에 숫자를 전달하여 복제하기 위한 서버의 임의의 숫자를 명시할 수 있게 합니다.

```js
> db.runCommand({"getLastError" : 1, "w" : 2, "wtimeout" : 500})
```

이는 두 멤버가 쓰기를 할 때까지 기다립니다.

`w` 값은 프라이머리를 포함하는 것을 알아둡니다. 만약 n 개의 세컨더리에 쓰기를 전달하기 원한다면 `w` 를 n+1 로 설정합니다. 프라이머리에 쓰기가 성공적으로 수행되었는지 확인하는 것은 `getLastEError` 에서 어차피 하는 일이기 때문에 `w : 1` 로 설정하는 것은 `w` 옵션을 전혀 전달하지 않는 것과 같습니다.

숫자를 사용할 떄의 단점은 복제 셋 구성을 변경하면 어플리케이션을 변경해야 하는 것입니다.

## Custom Replication Guarantees

복제셋의 과반수에 쓰기를 하는 것은 안전하다고 여겨집니다. 그러나 어떤 복제 셋은 더 복잡한 요구 사항을 가질 수 있습니다. 각 데이터 센터에 있는 적어도 하나의 서버나 숨겨지지 않은 노드의 과반수에 쓰기를 보장하기를 원할 수 있습니다. 복제 셋은 필요한 서버의 조합에 관계 없이 복제를 보장하기 위해 `getLastError` 에 넘겨줄 수 있는 사용자 정의 규칙을 만들 수 있게 해줍니다.

### Guaranteeing One Server per Data Center

데이터 센터 간의 네트워크 문제는 데이터 센터 내의 문제보다 훨씬 더 일반적이며, 여러 데이터 센터에 걸쳐 서버들을 동등하게 겉핥기 식으로 영향을 주기 보단 데이터 센터 전체를 오프라인으로 만들 가능성이 더 높습니다.

그러므로 쓰기를 위한 데이터 센터에 특화된 로직을 원할 수도 있습니다. 성공 통보를 받기 전에 모든 데이터 센터에 쓰기를 보장하는 것은 오프라인이 되어가는 데이터 센터에 의해 수행된 쓰기의 경우 모든 다른 데이터 센터가 적어도 하나의 로컬 복제본을 가짐을 의미합니다.

이를 설정하려면, 먼저 데이터 센터별로 멤버를 분류합니다. 복제 셋 구성에 `tags` 필드를 추가하여 이를 수행합니다.

```js
> var config = rs.config()
> config.members[0].tags = {"dc" : "us-east"}
> config.members[1].tags = {"dc" : "us-east"}
> config.members[2].tags = {"dc" : "us-east"}
> config.members[3].tags = {"dc" : "us-east"}
> config.members[4].tags = {"dc" : "us-west"}
> config.members[5].tags = {"dc" : "us-west"}
> config.members[6].tags = {"dc" : "us-west"}
```

`tags` 필드는 각 멤버가 여러 태그를 가질 수 있는 객체입니다. 예를 들어 `{"dc" : "us-east", "quality" : "high"}` 와 같은 태그 필드는 `us-east` 데이터 센터의 high quality 서버를 의미합니다.

두 번째 단계는 복제 셋 구성에 `getLastErrorMode` 필드를 추가하여 규칙을 추가하는 것입니다. 각 규칙의 형식은 `{name" : {"key" : number}}` 입니다. `name` 은 규칙의 이름이고 클라이언트가 `getLastError` 를 호출할 때 이 이름을 사용하기 때문에 클라이언트가 이해할 수 있는 방식으로 해당 규칙의 수행 절차를 적어둬야 합니다. 이 예제에서 `eachDC` 나 `user-level safe` 와 같이 더 축약된 규칙을 호출할 수 있습니다.

`key` 필드는 태그에서의 키 필드입니다. 그래서 이 예제에서의 Key 는 `dc` 입니다. `number` 는 이 규칙을 충족하는 데 필요한 수의 그룹입니다. 이 경우 `number` 는 2 입니다. `number` 는 항상 `number` 그룹 각각에서 적어도 하나의 서버를 의미합니다.

`getLastErrorModes` 를 복제 셋 구성에 추가하고 규칙을 생성하기 위해 재구성해 보겠습니다.

```js
> config.settings = {}
> config.settings.getLastErrorModes = [{"eachDC" : {"dc" : 2}}]
> rs.reconfig(config)
```

`getLastErrorModes` 는 복제 셋 구성의 하위 객체인 `settings` 에 존재하며, 복제 셋의 몇 가지 선택적인 설정을 포함합니다.

이제 쓰기에 이 규칙을 사용할 수 있습니다.

```js
> db.foo.insert({"x" : 1})
> db.runCommand({"getLastError" : 1, "w" : "eachDC", "wtimeout" : 1000})
```

규칙들이 어플리케이션 개발자에게는 다소 추상적입니다. 어프릴케이션 개발자들은 규칙을 사용하기 위해 eachDC 내에 어떤 서버가 있는지 알 필요가 없고, 규칙은 어플리케이션의 변화 없이 변경 가능합니다. 데이터 센터를 추가하거나 복제 셋 멤버를 바꿀 수 있지만 어플리케이션은 이를 알 필요가 없습니다.

### Guaranteeing a Majority of Nonhidden Members

숨겨진 멤버는 아류 멤버로 여겨집니다. 사용자는 이런 멤버를 위해 장애를 복구할 일이 없고, 거기서 어떤 읽기를 수행할 일도 절대 없습니다. 그러므로 사용자는 단지 쓰기를 받은 숨겨지지 않은 멤버만을 신경 쓰고, 숨겨진 멤버들은 그들 스스로 정렬할 수 있게 둬야합니다.

`host0` 부터 `host4` 까지 다섯 멤버가 있습니다. `host4` 가 숨겨진 멤버라 가정하겠습니다. 이때 쓰기를 가진 숨겨지지 않은 멤버가 과반수 이상인지, 즉 `host0`, `host1`, `host2`, `host3` 중 적어도 세 멤버가 숨겨지지 않은 멤버인지 확인하고 싶어합니다. 이를 위한 규칙을 만들기 위해 먼저 숨겨진 멤버 각각을 자신의 태그에 태깅합니다.

```js
> var config = rs.config()
> config.members[0].tags = [{"normal" : "A"}]
> config.members[1].tags = [{"normal" : "B"}]
> config.members[2].tags = [{"normal" : "C"}]
> config.members[3].tags = [{"normal" : "D"}]
```

숨겨진 멤버인 `host4` 는 태깅되지 않습니다.

이제 이 서버의 과반수에 대한 규칙을 추가하겠습니다.

```js
> config.settings.getLastErrorModes = [{"visibleMajority" : {"normal" : 3}}]
> rs.reconfig(config)
```

이제 어플리케이션에서 이 규칙을 사용할 수 있습니다.

```js
> db.foo.insert({"x" : 1})
> db.runCommand({"getLastError" : 1, "w" : "visibleMajority", "wtimeout": 1000})
```

이는 적어도 숨겨지지 않은 세 멤버가 쓰기를 가질 때까지 대기할 것입니다.

### Creating Other Guarantees

사용자가 생성할 수 있는 규칙에는 제한이 없습니다. 사용자 정의 복제 규칙을 만들기 위해서는 다음 두 단계를 거쳐야 합니다.

1. Key / Value 쌍을 할당하여 멤버들을 태깅한다. Key 는 분류를 나타냅니다. 예를 들어 `data_center` 나 `region` 또는 `server Quality` 와 같은 Key 를 가질 수 있습니다. 값은 서버가 분류체계 내에서 어떤 그룹에 속하게 되는지 결정합니다. 예를 들어 Key `data_center` 는 `us-east`, `us-west`, `aust` 등으로 태깅된 서버를 가질 수 있습니다.
2. 생성한 분류체계에 기반하여 규칙을 생성합니다. 규칙은 항상 `{"name" : {"key" : number}}` 형태고, 쓰기가 성공하기 전에 number 개의 그룹으로부터 적어도 하나의 서버는 쓰기를 가져야합니다. 예를 들어 `{"twoDCs" : {"data_center" : 2}}` 라는 규칙을 생성할 수 있고, 이는 쓰기가 성공하기 전에 태깅된 두 데이터 센터 내에서 적어도 하나의 서버가 쓰기에 대해 승인을 해야 하는 것을 의미합니다.

이제 이 규칙을 `getLastError` 에서 사용할 수 있습니다.

규칙을 이해하고 구성하는 것이 복잡하지만 복제를 구성하는 강력한 방법입니다. 복제 요구 사항에 얽혀 있지 않다면 `w : majority` 를 고수하여 안전할 수 있습니다.

## Sending Reads to Secondaries

기본적으로 드라이버는 모든 요청을 프라이머리로 라우팅합니다. 이는 이랍ㄴ적으로 사용자가 원하는 것이지만 드라이버에서 **읽기 선호도(Read Preference)** 를 설정하여 다른 옵션을 구성할 수 있습니다. 읽기 선호도는 쿼리가 보내져야 하는 서버의 타입을 명시합니다.

읽기 요청을 세컨더리에 보내는 것은 일반적으로 좋지 않은 생각입니다. 몇 가지 의미 있는 특수한 상황이 있지만, 일반적으로 모든 트래픽은 프라이머리로 전송해야 합니다. 만약 세컨더리로 읽기를 전송하는 것을 고려하고 있다면 이를 허용하기 전에 매우 신중하게 해당 사항에 대한 장단점을 꼭 생각해야 합니다.

### Consistency Considerations

엄격하게 일관된 읽기가 필요한 어플리케이션은 세컨더리로부터 읽기를 수행하면 안됩니다.

세컨더리는 보통 프라이머리의 몇 밀리세컨드 이내에 있어야 합니다. 하지만 이는 보장되지 않습니다. 때때로 세컨더리는 부하, 잘못된 구성, 네트워크 오류, 다른 문제들로 인해 분, 시간 심지어 일 단위로 뒤처질 수 있습니다. 클라이언트 라이브러리는 세컨더리가 얼마나 최신인지 모르기 때문에 클라이언트는 훨씬 뒤처진 세컨더리에 쿼리를 전송합니다.

클라이언트 읽기로 부터 세컨더리를 숨기는 것은 가능하지만 이는 수동 프로세스입니다. 그러므로 만약 어플리케이션이 예상대로 최신의 데이터를 필요로 하면 이는 세컨더리에서 읽으면 안됩니다.

만약 어플리케이션이 자기 자신의 쓰기를 읽을 필요가 있을 때, 쓰기가 이전과 같이 `w` 를 이용하여 모든 세컨더리에 대한 복제를 대기하지 않는다면 읽기 요청을 세컨더리에 보내면 안됩니다. 그렇게 하지 않으면 어플리케이션은 성공적으로 쓰기를 수행하고 그 값을 읽으려 할 것이므로 해당 값을 찾을 수 없게됩니다. 클라이언트는 복제가 연산을 복사할 수 있는 것보다 더 빠르게 요청을 발행합니다.

### Load Considerations

많은 사용자가 부하를 분산하기 위해 읽기를 세컨더리로 전송합니다. 서버가 초당 10,000 개의 쿼리만 처리할 수 있고, 개발자는 30,000 개를 처리할 수 있기를 원하면 여러 세컨더리를 구성해 새롭게 구성한 세컨더리가 부하를 처리하도록 합니다. 하지만 이는 실수로 시스템에 과부하를 초래할 수 있고 과부하가 발생하면 회복하기 어렵기 때문에 위험한 확장 방법입니다.

예를 들어 초당 30,000 개 이상의 읽기가 발생하고 있다고 가정하겠습니다. 이를 처리하기 위해 4-멤버의 복제 셋을 생성하기로 결정합니다. 각 세컨더리는 정상이고 최대 부하와 시스템 동작은 완벽합니다.

세컨더리 중 하나가 손상되기 전까지는 그렇습니다.

이제 남아 있는 각 멤버들은 처리 가능한 100 % 의 부하를 처리합니다. 손상된 멤버를 다시 재구축하여 사용할 필요가 있다면 다른 서버들 중 하나로부터 데이터를 복사해야 하는데, 이는 남아있는 서버를 난처하게 만듭니다. 서버에 과부하를 주는 것은 수행 속도를 낮추고, 복제 셋의 수용 능력을 낮추고, 다른 멤버가 더 많은 부하를 갖도록 하여 점점 느려지게 합니다.

과부하는 느린 복제를 유발하며, 세컨더리 역시 뒤처지도록 만듭니다. 갑잡스럽게 멤버를 다운시키면 멤버는 지연되기 시작하고 모든 것이 과부하에 걸릴 가능성이 있습니다.

서버에 얼마나 많은 부하를 감당하게 할지에 대한 좋은 생각이 있다면 더 나은 계획을 세울 수 있을지도 모릅니다. 4 개의 서버를 사용하는 대신 5 개의 서버를 사용하면 하나가 다운되더라도 복제 셋은 과부하를 받지 않게 됩니다. 하지만 완벽한 계획을 세울 수 있고, 예상되는 서버의 수만 잃게 되더라도, 다른 서버들의 문제를 해결해야 합니다.

### Reasons to Read from Secondaries

어플리케이션 읽기를 세컨더리로 전송하는 이유가 있습니다. 프라이머리가 다운되더라도 어플리케이션이 지속적으로 읽기 작업을 수행하는 경우와, 읽기를 세컨더리에 분산하는 것이 가장 일반적인 경우입니다. 복제 셋이 프라이머리를 잃게 되면 사용자는 임시로 읽기 전용 모드를 원할 수 있습니다. 이 읽기 선호도를 Primary preferred 라 합니다.

세컨더리로부터의 읽기와 관련된 한 가지 공통적인 논쟁은 낮은 지연율을 가지는 읽기를 하는것입니다. 드라이버에서 복제 셋 멤버까지의 평균 핑타임을 기반으로 한 가장 낮은 지연율을 가지는 멤버에 요청을 라우팅 하기위해 Nearest 를 읽기 선호도로 지정할 수 있습니다. 만약 어플리케이션이 여러 데이터 센터에 있는 낮은 지연율의 같은 문서에 접근할 필요가 있다면 Nearest 가 이를 수행하는 유일한 방법입니다.

그러나 문서가 위치기반이라면, 이는 샤딩으로 처리할 수 있습니다. 어플리케이션이 낮은 지연율의 읽기와 쓰기를 요구하면 샤딩을 권고합니다. 복제 셋은 프라이머리가 무엇이든지 간에 오직 하나의 위치에 대해서만 쓰기를 허용합니다. 

모든 쓰기에 대해 아직 복제하지 못한 멤버로부터 읽기를 수행하려면 일관성은 희생해야 합니다. 그 대신에 쓰기가 모든 멤버에 복제될 때까지 기다린다면 쓰기 속도를 희생할 수 있습니다.

어플리케이션이 임의의 오래된 데이터를 받아들일 수 있게 동작한다면 Secondary 또는 Secondary preferred 읽기 선호도를 사용할 수 있습니다. Secondary 는 항상 세컨더리에 읽기 요청을 합니다. 이용 가능한 세컨더리가 없다면 읽기 요청을 프라이머리에 보내기보다는 에러를 발생합니다. 이는 오래된 데이터에 대해 신경을 쓰지 않고 프라이머리를 오직 쓰기를 위해서만 사용하는 어플리케이션에 사용될 수 있습니다. 데이터가 오래되고 변질되는 것에 대한 우려가 있다면 이 방식은 추천하지 않습니다.

이용 가능하다면 Secondary preferred 는 세컨더리에 읽기 요청을 보낼 것입니다. 어떤 세컨더리도 이용 가능하지 않는다면 요청은 프라이머리에 보내질 것입니다.

때때로 읽기 부하는 쓰기 부하와 크게 다릅니다. 그래서 현재 쓰고 있는 데이터와 완전히 다른 데이터를 읽게 됩니다. 프라이머리에 두고 싶지 않은 오프라인 처리를 위해 꽤 많은 인덱스를 원할 수도 있습니다. 이 경우 프라이머리보다는 다른 인덱스로 세컨더리를 설정할 수 있습니다. 세컨더리를 이러한 목적으로 사용하기 원하는 경우, 복제 셋 연결 대신 드라이버에서 세컨더리로 직접적인 연결을 만들기 원할 것입니다.

어떤 옵션이 합리적인 어플리케이션을 만드는 데 도움이 되는지 고려해보겠습니다. 옵션을 조합하는 것 또한 가능합니다. 어느 정도의 읽기 요청이 프라이머리로부터 발생한다면 Primary 를 사용합니다. 만약 가장 최신의 데이터를 가지지 않은 다른 읽기도 괜찮다면 Primary preferred 를 사용합니다. 그리고 특정 요청이 일관성을 무시하고 낮은 지연율을 원하는 경우에 Nearest 를 사용합니다.