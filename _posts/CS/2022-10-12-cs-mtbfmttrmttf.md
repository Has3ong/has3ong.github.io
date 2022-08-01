---
title : MTBF, MTTR, MTTF, 가용성 개념
tags :
- MTTR
- MTTF
- MTBF
- Computer Science
categories:
- Computer Science
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

MTBF, MTTR, MTTF 설비 보전의 신뢰성 지표로 사용합니다. 이는 하드웨어 제품 또는 구성 요소의 성능, 장비 설계, 신뢰성 및 안전에 대한 중요한 유지관리 조치입니다.

![image](/assets/images/cs/mtbf2.png)

* **평균고장간격(MTBF, Mean Time Between Failures)**
  * 고장들 사이 간격시간들의 평균
  * 고장 복구부터 다음 고장 시점까지 평균연속 가동시간(무고장 동작시간,평균 작동시간)
* **평균고장수명(MTTF, Mean Time To Failure)**
  * 고장나기까지의 시간들의 평균
* **평균수리시간(MTTR, Mean Time To Repair)**
  * 보전성의 척도
  * 시스템을 정상 운용상태로 돌려 놓기위해(수리복구등) 시스템의 자동 복구 또는 유지보수 요원이 소비하게 되는 평균시간
* **가용성(Availability)**
  * = (실질 가동 시간) / (총 운용 시간)
  * = MTBF / ( MTBF + MTTR ) 
  * = 평균고장간격 / (평균고장간격 + 평균수리시간)

그 밖의 다른 지표들도 있으니 참고로 보셔도 됩니다.

![image](/assets/images/cs/mtbf1.svg)

* **MTTD(Mean Time To Detect)**: 문제가 시작된 후 조직에서 이를 감지한 시간 사이의 평균 시간입니다. MTTD는 IT가 문제 티켓을 받기 전과 MTTR 시계를 시작할 때까지의 시간 범위를 나타냅니다.
* **MTTI(Mean Time To Investigate)**: IT 사고를 감지한 후 조직이 원인 및 솔루션을 조사하기 시작하는 사이의 평균 시간입니다. 이것은 MTTD와 MTTR의 시작 사이의 시간을 나타냅니다.
* **MTRS(Mean Time to Restore Service)**: 인시던트 감지부터 영향을 받는 시스템 또는 구성 요소를 사용자가 다시 사용할 수 있을 때까지 경과된 평균 시간입니다. MTRS는 MTTR이 항목을 수리하는 데 걸리는 시간을 나타내는 반면 MTRS는 해당 항목이 수리된 후 서비스를 복원하는 데 걸리는 시간을 나타낸다는 점에서 MTTR과 다릅니다.
* **MTBSI(Mean Time Between System Incidents)**: 두 개의 연속적인 사고 감지 사이의 평균 경과 시간. MTBSI는 MTBF와 MTRS를 더하여 계산할 수 있습니다(MTBSI = MTBF + MTRS).
* **Failure rate**: 구성 요소 또는 시스템이 실패하는 빈도를 측정하는 또 다른 신뢰성 메트릭입니다. 단위 시간 동안의 실패 횟수로 표현됩니다.

> 참고자료

* [MTTR vs MTBF vs MTTF? – A Simple Guide To Failure Metrics](https://saigoncantho.com.vn/mttr-la-gi/)
* [What Is Mean Time to Repair (MTTR)?](https://www.splunk.com/en_us/data-insider/what-is-mean-time-to-repair.html)
