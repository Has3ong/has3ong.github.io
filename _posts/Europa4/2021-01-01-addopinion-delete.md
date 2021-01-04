---
title : Europa Universalis 4 - Delete add opinion command
tags :
- Europa Universalis 4
---

Europa Universalis 4 에서 add_opinion Tag 는 다음과 같습니다.

```
add_opinion [<Country Tag>] 지정한 국가와 관계를 100만큼 상승시킨다. 총 두번 사용 가능.
```

설정했을 때 `same_religion` 즉 같은 종교로 해서 아래와 같이 +100 관계도가 상승이 됩니다.

![asd](https://user-images.githubusercontent.com/44635266/103434160-bbf5d400-4c40-11eb-9f7b-729b02247973.png)

이 효과는 영구 지속되어 게임 상으로는 다시 해제할 수 없습니다.

하지만 이 효과를 없애는 방법이 하나 있는데, 바로 세이브 파일로 들어가 직접 수정해서 없애는 방법입니다.

![ssd](https://user-images.githubusercontent.com/44635266/103434180-070fe700-4c41-11eb-9ace-5d2310750cf1.JPG)

유로파 세이브 경로로 들어가서 내가 진행하던 게임 파일을 메모장으로 열어줍니다.(시간이 상당히 걸립니다.!)

그리고 `current_opinion=200.00` 혹은 `current_opinion=100.00` 으로 검색을 해줍니다.

그러면 아래처럼 딱봐도 수상한(?) 놈이 보입니다. 같은 종교인데 현재 의견 200 이라내요.

![3](https://user-images.githubusercontent.com/44635266/103434265-36732380-4c42-11eb-9341-1e6d56d59007.JPG)

```
opinion={
  modifier="same_religion"
  date=1467.8.1
  current_opinion=200.000
  expiry_date=yes
}
```

삭제해주고 저장합니다.

그리고 게임을 다시 실행시키고 관계도를 확인해보겠습니다.

![4](https://user-images.githubusercontent.com/44635266/103434288-936ed980-4c42-11eb-8c7a-2da8e1e7256b.png)

같은 종교 관계도 증진이 사라진것을 확인할 수 있습니다.

### 주의사항 !

종속국인 경우 관계도를 200 까지 올릴 수 있으니 `modifier` 의 값을 잘 살펴보고 진행하면 됩니다.

```
opinion={
  modifier="improved_relation"
  date=1462.8.18
  current_opinion=200.000
  expiry_date=yes
  delayed_decay=yes
}
```

그럼 즐거운 유로파 하시고

새해복 많이 받으세요. !
