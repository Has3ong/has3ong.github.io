---
title : Python OpenAPI 데이터 활용하기
tags :
- Python
- OpenAPI
---

[공공데이터 포털](https://www.data.go.kr/)을 이용했습니다.

회원 가입 후 원하는 공공 데이터를 찾습니다.

보통 데이터를 XML과 JSON타입으로 주는데 저는 XML로 사용했습니다.

사용하실 서비스를 신청한 뒤에 참고 문서와 인증키를 확인하시고,

URL 과 Parameter를 맞춰줍니다. API_Key 변수에다가 공공 API에서 받은 키(일반인증키, UTF-8)를 입력하시면 됩니다.

저는 현재 포스트에서 **대기오염정보 조회 서비스** 를 사용해보겠습니다.

> Example

```python
# -- coding: utf-8 --
import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote

class oDust:
    session = requests.Session
    def __init__(self):
        self.pm10 = ""
        self.pm25 = ""

    def Update(self):
        API_Key = unquote('')
        url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
        queryParams = '?' + urlencode(
            {
                quote_plus('sidoName'): '경기',
                quote_plus('pageNo'): '1', quote_plus('numOfRows') : '7', quote_plus('serviceKey') : API_Key,
                quote_plus('ver') : '1.3'
             }
        )

        request = Request(url+queryParams)
        request.get_method = lambda : 'GET'
        response_body = urlopen(request).read().decode('utf-8')

        print(response_body)
```

Result

```
<?xml version="1.0" encoding="UTF-8"?>

<response>
	<header>
		<resultCode>00</resultCode>
		<resultMsg>NORMAL SERVICE.</resultMsg>
	</header>
	<body>
		<items>

				<item>
					<stationName>신풍동</stationName>

                        <mangName>도시대기</mangName>

					<dataTime>2019-11-28 18:00</dataTime>
					<so2Value>0.003</so2Value>
					<coValue>0.4</coValue>
					<o3Value>0.010</o3Value>
					<no2Value>0.034</no2Value>
					<pm10Value>35</pm10Value>

                        <pm10Value24>40</pm10Value24>


				        <pm25Value>14</pm25Value>


                        <pm25Value24>24</pm25Value24>

					<khaiValue>72</khaiValue>
					<khaiGrade>2</khaiGrade>
					<so2Grade>1</so2Grade>
					<coGrade>1</coGrade>
					<o3Grade>1</o3Grade>
					<no2Grade>2</no2Grade>
					<pm10Grade>2</pm10Grade>

				        <pm25Grade>2</pm25Grade>


                        <pm10Grade1h>2</pm10Grade1h>
                        <pm25Grade1h>1</pm25Grade1h>

				</item>

				<item>
					<stationName>인계동</stationName>

                        <mangName>도시대기</mangName>

					<dataTime>2019-11-28 18:00</dataTime>
					<so2Value>0.003</so2Value>
					<coValue>0.6</coValue>
					<o3Value>0.004</o3Value>
					<no2Value>0.043</no2Value>
					<pm10Value>28</pm10Value>

                        <pm10Value24>40</pm10Value24>


				        <pm25Value>25</pm25Value>


                        <pm25Value24>27</pm25Value24>

					<khaiValue>79</khaiValue>
					<khaiGrade>2</khaiGrade>
					<so2Grade>1</so2Grade>
					<coGrade>1</coGrade>
					<o3Grade>1</o3Grade>
					<no2Grade>2</no2Grade>
					<pm10Grade>2</pm10Grade>

				        <pm25Grade>2</pm25Grade>


                        <pm10Grade1h>1</pm10Grade1h>
                        <pm25Grade1h>2</pm25Grade1h>

				</item>
		</items>
			<numOfRows>7</numOfRows>
			<pageNo>1</pageNo>
			<totalCount>97</totalCount>
	</body>
</response>
```