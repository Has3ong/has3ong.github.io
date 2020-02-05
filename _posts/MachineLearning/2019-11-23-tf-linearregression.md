---
title : Tensorflow Linear Regression Analysis
tags :
- Keras
- Linear Regression
- MachineLearning
---

통계학에서, 선형 회귀는 종속 변수 y와 한 개 이상의 독립 변수 (또는 설명 변수) X와의 선형 상관 관계를 모델링하는 회귀분석 기법이다. 한 개의 설명 변수에 기반한 경우에는 단순 선형 회귀, 둘 이상의 설명 변수에 기반한 경우에는 다중 선형 회귀라고 한다.

선형 회귀는 선형 예측 함수를 사용해 회귀식을 모델링하며, 알려지지 않은 파라미터는 데이터로부터 추정한다. 이렇게 만들어진 회귀식을 선형 모델이라고 한다.

> 독립변수 1개와 종속변수 1개를 가진 선형 회귀의 예

![image](https://user-images.githubusercontent.com/44635266/69471140-6a450e00-0ddf-11ea-9992-f3391772b330.png)

임의의 학습용 데이터 점 1000개를 가지고 해보겠습니다.

> Example

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


pointsNum = 1000
pointSet = []
for i in range(pointsNum):
         x = np.random.normal(0.0, 0.55)
         y = x * 0.1 + 0.3 + np.random.normal(0.0, 0.03)
         pointSet.append([x, y])

x_data = [v[0] for v in pointSet]
y_data = [v[1] for v in pointSet]

plt.plot(x_data, y_data, 'ro')
plt.legend()
plt.show()

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
y = W * x_data + b

loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for step in range(10):
     sess.run(train)
     print(step, sess.run(W), sess.run(b))
     print(step, sess.run(loss))

     plt.plot(x_data, y_data, 'ro')
     plt.plot(x_data, sess.run(W) * x_data + sess.run(b))
     plt.xlabel('x')
     plt.xlim(-2,2)
     plt.ylim(0.1,0.6)
     plt.ylabel('y')
     plt.legend()
     plt.show()
```

위 코드에서 볼 수 있듯이 y = 0.1 * x + 0.3 관계를 가지는 데이터를 생성했습니다. 하지만 정규분포(normal distribution)를 따라 약간의 편차를 두어 완전히 직선에 일치하지 않는 리얼리틱한 예를 만들었습니다.

결과 데이터 포인트의 그래프는 아래와 같습니다.

![image](https://user-images.githubusercontent.com/44635266/69471335-6d40fe00-0de1-11ea-8c69-ddc8d43ef6a2.png)

그리고 Linear Regression Analysis 결과를 아래에 보여드리겠습니다.

![image](https://user-images.githubusercontent.com/44635266/69471419-17208a80-0de2-11ea-95c1-031453c918fb.png)

![image](https://user-images.githubusercontent.com/44635266/69471423-28699700-0de2-11ea-9546-c76d980a1845.png)

횟수 즉, 학습량이 증가할 수록 loss 값이 줄어드는걸 알 수 있습니다.

```
출력양식은
step W B
step Loss 입니다.

0 [0.7135699] [0.3058917]
0 0.115596965

1 [0.5276394] [0.30456874]
1 0.056872442

2 [0.39774454] [0.303652]
2 0.028210754

3 [0.30699736] [0.30301154]
3 0.014221836

4 [0.24359955] [0.3025641]
4 0.0073942593

5 [0.19930854] [0.30225152]
5 0.004061921

6 [0.16836596] [0.30203313]
6 0.0024355068

7 [0.14674883] [0.30188057]
7 0.0016417017

8 [0.13164666] [0.301774]
8 0.001254269

9 [0.12109599] [0.30169952]
9 0.0010651746
```