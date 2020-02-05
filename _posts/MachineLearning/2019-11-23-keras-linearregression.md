---
title : Keras Linear Regression Analysis
tags :
- Keras
- Linear Regression
- MachineLearning
---

통계학에서, 선형 회귀는 종속 변수 y와 한 개 이상의 독립 변수 (또는 설명 변수) X와의 선형 상관 관계를 모델링하는 회귀분석 기법이다. 한 개의 설명 변수에 기반한 경우에는 단순 선형 회귀, 둘 이상의 설명 변수에 기반한 경우에는 다중 선형 회귀라고 한다.

선형 회귀는 선형 예측 함수를 사용해 회귀식을 모델링하며, 알려지지 않은 파라미터는 데이터로부터 추정한다. 이렇게 만들어진 회귀식을 선형 모델이라고 한다.

> 독립변수 1개와 종속변수 1개를 가진 선형 회귀의 예

![image](https://user-images.githubusercontent.com/44635266/69471140-6a450e00-0ddf-11ea-9992-f3391772b330.png)

화씨랑 섭씨 온도를 이용하여 선형 회귀 분석을 해보겠습니다.

> Example

```python
import numpy as np
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import *

Fahrenheit = np.array(
    [-140, -136, -124, -112, -105, -96, -88, -75, -63, -60, -58, -40, -20, -10, 0, 30, 35, 48, 55, 69, 81, 89, 95, 99,
     105, 110, 120, 135, 145, 158, 160], dtype=float)

Celsius = np.array(
    [-95.55, -93.33, -86.66, -80, -76.11, -71.11, -66.66, -59.44, -52.77, -51.11, -50, -40, -28.88, -23.33, -17.77,
     -1.11, 1.66, 8.88, 12, 20, 27.22, 31.66, 35, 37.22, 40.55, 43.33, 48.88, 57.22, 62.77, 70, 71.11], dtype=float)

model = Sequential()

model.add(Dense(64, activation='relu', input_shape=[1]))
model.add(Dense(64, activation='relu'))
model.add(Dense(1))

model.summary()

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy', 'mean_absolute_error', 'mean_squared_error'])

model.fit(Fahrenheit, Celsius, epochs=500)

print(model.predict([-140]))
```

> epochs = 500, Prediction

```
print(model.predict([-140])) [[-100.046234]]
```

> epochs = 5000, Prediction

```
print(model.predict([-140]))[[-95.59061]]
```

![image](https://user-images.githubusercontent.com/44635266/69471102-13d7cf80-0ddf-11ea-876d-a4d4f16af64b.png)

학습횟수를 높일수록 정답에 가까워지는 모습을 볼 수 있습니다.