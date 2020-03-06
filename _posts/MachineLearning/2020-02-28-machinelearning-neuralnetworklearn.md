---
title : Machine Learning Neural Network Learning
tags :
- Loss Function
- Neural Network
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch]() 를 바탕으로 작성하였습니다.*

**학습** 이란 훈련 데이터로부터 가중치 매개변수의 최적값을 자동으로 획득하는 것을 뜻합니다. 신경망이 학습할 수 있도록 해주는 지표인 **손실 함수** 를 알아보겠습니다.

## Learning from Data!

신경망의 특징은 데이터를 보고 학습할 수 있습니다. 데이터에서 학습한다는 것은 가중치 매개변수의 값을 데이터를 보고 자동으로 결정한다는 것입니다.

### Data-Driven Learning

기계학습은 데이터가 생명입니다. 데이터에서 답을 찾고 패턴을 발견하는것이 바로 기계학습니다. 그래서 기계학습의 중심에는 데이터가 존재합니다.

구체적인 예를 통해 알아보겠습니다. 이미지에서 ***5*** 라는 숫자를 인식하는 프로그램을 구현해보겠습니다 `Example 1` 과 같이 자유로운 손글씨 이미지를 보고 5 인지 아닌지 알아보는 프로그램을 하는것이 목표입니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/75603270-31b87d00-5b10-11ea-9302-ad29187dcbc9.png)

사람이라면 어렵지 않게 인식하지만 그 안에 숨은 규칙성을 명확한 로직으로 풀기가 어렵습니다. 그래서 이미지에서 **특징** 을 추출하고 그 특징의 패턴을 기계학습 기술로 학습하는 방법이 있습니다.

이미지의 특지응ㄴ 보통 벡터로 기술하고, 컴퓨터 비전 분야에서는 SIFT, SURF, HOG 등의 특징을 많이 사용합니다. 이런 특징을 사용하여 이미지 데이터를 벡터로 변환하고, 변환된 벡터를 가지고 지도 학습 방식의 대표 분류 기법인 SVM, KNN 등으로 학습할 수 있습니다.

이와 같은 기계학습에서는 모아진 데이터로부터 규칙을 찾아내는 역할을 ***기계*** 가 담당합니다.

지금까지 기계학습의 2 가지 접근법을 알아봤습니다. 이 두 방식 모두 그림으로 나타내면 `Example 2` 의 중간과 같습니다. 반면 딥러닝 방식은 `Example 2` 의 아래처럼 사람이 개입하지 않는 블록 하나로 그려집니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/75603278-3da43f00-5b10-11ea-970e-4861968556dc.png)

신경망의 이점은 모든 문제를 같은 맥락에서 풀 수 있다는 점입니다. 예를들어 숫자를 인식하든 개를 인식하든 세부사항과 관계없이 신경망은 주어진 데이터를 온전히 학습하고 주어진 문제의 패턴을 발견하려 시도합니다. 즉, 신경망은 모든 문제를 주어진 데이터 그대로를 입력데이터로 활용해 **end - to - end** 로 학습합니다.

### Training Data and Test Data

기계학습 문제는 데이터를 **훈련 데이터(Training Data)** 와 **시험 데이터(Test Data)** 로 나눠 학습화 실험을 수행하는 것이 일반적입니다. 우선 훈련 데이터로만 학습하며 최적의 매개변수를 찾습니다. 그 다음 시험 데이터를 사용하여 앞서 훈련한 모델의 실력을 평가합니다.

여기서 훈련 데이터와 시험 데이터를 분류하는 이유는 우리가 원하는 것은 범용적으로 사용할 수 있는 모델이기 때문입니다. 이 **범용 능력** 을 제대로 평가하기 위해 훈련 데이터와 시험 데이터를 분리합니다. **범용 능력** 은 아직 보지 못한 데이터로도 올바르게 풀어내는 능력입니다.

하지만, 데이터 셋 하나로만 매개변수의 학습과 평가를 수행하면 평가가 될 수 없습니다. 수중의 데이터셋은 제대로 맞추더라도 다른 데이터셋에는 엉망인 일도 벌어집니다. 참고로 한 데이터셋에만 지나치게 최적화된 상태를 **오버피팅(Overfitting)** 이라 합니다. 오버피팅 피하기는 기계학습의 주요 과제중 하나입니다.

## Loss Function

신경망은 *하나의 지표* 를 기준으로 최적의 매개변수 값을 탐색합니다. 신경망의 학습에서 사용하는 지표는 **손실함수(Loss Function)** 이라 합니다. 이 손실 함수는 잉믜의 함수를 사용할 수도 있지만, 오차 제곱합과 교차 엔트로피 오차를 사용합니다.

> 손실함수는 신경망 성능의 나쁨을 나타내는 지표입니다.

### Sum of Squares for Error

가장 많이 쓰이는 손실 함수는 **오차제곱합(Sum of Squares for Error, SSE)** 입니다. 수식으로는 다음과 같습니다.

> Expression 1

$$
E = { 1 \over 2} \sum_k (y_k - t_k)^2
$$

여기서 $y_k$ 는 신경망의 출력, $t_k$ 는 정답 레이블, $k$ 는 데이터의 차원 수를 나타냅니다. 예시를 통해 알아보겠습니다.

```python
>>> y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
>>> t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
```

`t` 와 같이 가장 높은 값 한 원소만 1 로 하고 그 외는 0 으로 나타내는 표기법을 **원-핫 인코딩(One-Hot Encoding)** 이라 합니다.

오차 제곱합은 `Expression 1` 과 같이 원소의 출력과 정답레이블의 차를 제곱한 후, 그 총합을 구합니다. 이 오차제곱합을 Python 으로 구현해보겠습니다.

```python
def sum_suqares_error(y, t):
    return 0.5 * np.sum((y-t) ** 2)
```

여기서 인수 `y` 와 `t` 는 Numpy 배열입니다. 이제 실제로 사용해보겠습니다.

```python
# 정확하게 예측 했을 때
>>> t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
>>> y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
>>> sum_squares_error(np.array(y), np.array(t))
0.097500000000000031

# 다르게 예측 했을 때
>>> y = [0.1, 0.05, 0.1, 0.0, 0.05, 0.1, 0.0, 0.6, 0.0, 0.0]
>>> sum_squares_error(np.array(y), np.array(t))
0.597500000000000003
```

### Cross Entropy Error

또 다른 손실 함수로서 **교차 엔트로피 오차(Cross Entropy Error, CEE)** 도 자주 이용합니다. 수식은 다음과 같습니다.

> Expression 2

$$
E = - \sum _k t^k \log y_k
$$

여기서 $log$ 는 밑이 $e$ 인 자연로그$\log_e$입니다. $y_k$ 는 신경망의 출력, $t_k$ 는 정답 레이블입니다. 또 $t_k$ 는 정답에 해당하는 인덱스의 원소만 1 이고 나머지는 0 입니다. 그래서 `Expression 2` 는 실질적으로 정답일 때의 추정 ($t_k$ 가 1 일 때의 $y_k$) 의 자연로그를 계산하는 식이 됩니다.

예를 들어 정답 레이블은 2 가 정답이라 하고 이때의 신경망 출력이 0.6 이라면 교차 엔트로피 오차는 $-\log0.6 = 0.51$ 이 됩니다. 또한, 같은 조건에서 신경망 출력이 0.1 이라면 $-\log0.1 = 2.30$ 이 됩니다. 즉, 교차 엔트로피 오차는 정답일 때의 출력이 전체 값을 정하게 됩니다.

`Example 3` 은 자연로그의 그래프입니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/75603281-4563e380-5b10-11ea-826c-e8d7864f9911.png)

$x$ 가 1 일때 $y$ 는 0 이 되고 $x$ 가 0 에 가까워질수록 $y$ 의 값은 점점 작아집니다.

교차 엔트로피 오차를 구현해보겠습니다.

```python
def cross_entropy_error(y, t):
    delta = 1e-7
    return -np.sum(t * np.log(y + delta))
```

여기서 $y$ 와 $t$ 는 Numpy 배열입니다. 하지만 코드 마지막을 보면 `np.log` 를 계산할 때 아주 작은 값인 `delta` 를 더했습니다. 이는 `np.log()` 함수에 0 을 입력하면 마이너스 무한대를 뜻하는 `-inf` 가 되어 더이상 계산을 진행할 수 없게 됩니다.

아주 작은 값을 더해서 절대 0 이 되지 않도록, 즉 마이너스 무한대가 발생하지 않도록 하는것입니다. 그러면 이 `cross_entropy_error(y, t)` 함수를 써서 간단한 계산을 해보겠습니다.

```python
>>> t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
>>> y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
>>> cross_entropy_error(np.array(y), np.array(t))
0.51082545709933802
>>>
>>> y = [0.1, 0.05, 0.1, 0.0, 0.05, 0.1, 0.0, 0.6, 0.0, 0.0]
>>> cross_entropy_error(np.array(y), np.array(t))
2.3025840929945458
```

첫 번째 예는 정답일 때의 출력이 0.6 인 경우로 이때의 오차 값은 약 0.51 입니다. 그 다음 정답일 때의 출력이 0.1 인 경우에는 오차는 무려 2.3 입니다. 즉, 첫 번째 추정이 정답일 가능성이 높다고 판단한 것입니다.

### Mini-Batch Learning

기계학습 문제는 훈련 데이터를 사용해 학습합니다. 즉, 훈련 데이터에 대한 손실 함수의 값을 구하고 그 값을 최대한 줄여주는 매개변수를 찾아냅니다.

지금까지 데이터 하나에 대한 손실 함수만 생각해왔으니, 이제 훈련 데이터 모두에 대한 손실함수의 합을 구하는 법을 알아보겠습니다. 예를 들어 교차엔트로피 오차는 `Expresson 3` 과 같습니다.

> Expression 3

$$
E = - {1 \over N} \sum_n \sum t_{nk} \log y_{nk}
$$

이는 데이터가 N 개라면 $t_{nk}$ 는 $n$ 번째 데이터의 $k$ 번째 값을 의미합니다. 수식이 복잡해 보이지만 데이터 하나에 대한 손실 함수를 N 개의 데이터로 확장한한것입니다. 다만, 마지막에 N 으로 나누어 정규화 즉, **평균 손실 함수** 를 구하는것입니다.

MNIST 훈련 데이터 셋은 60,000 개였습니다. 하지만 모든 데이터를 대상으로 손실 함수의 합을 구하려면 시간이 많이 소요됩니다. 즉, 데이터 일부를 추려 전체의 근사치를 이용할 수 있는데 이 일부를 **미니 배치(Mini-Batch)** 라고 합니다.

미니배치 학습을 구현해보겠습니다. 먼저 MNIST 데이터 셋을 읽어오는 코드를 가져오겠습니다.

```python
import sys, os
sys.path.append(os.pardir)
import numpy as np
from dataset.mnist import load_mnist

(x_train, t_train), (x_test, t_test) = \
    load_mnist(normalize=True, one_hot_label=True)

print(x_train.shape) # (60000, 784)
print(t_train.shape) # (60000, 10)
```

`load_mnist` 함수는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/tree/master/dataset) 에 있습니다.

여기서 Numpy 의 `np.random.choice()` 함수를 이용하여 무작위 10 장만 빼내보겠습니다.

```python
train_size = x_train.shape[0]
batch_size = 10
batch_mask = np.random.choice(train_size, batch_size)
x_batch = x_train[batch_mask]
t_batch = t_train[batch_mask]
```

출력을 하면 다음과 같이 무작위 데이터가 나옵니다.

```python
>>> np.random.choice(60000, 10)
array([48481, 48267, 10042, 47689, 49392, 41305, 13759, 58075, 38188, 3048])
```

이 무작위로 선택한 인덱스를 사용해 미니배치를 사용하면됩니다.

### To Implement Cross Entropy Errors

교차 엔트로피 오차를 구하는 함수를 구현해보겠습니다.

```python
def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    
    batch_size = y.shape[0]
    return -np.sum(t * np.log(y + 1e-7)) / batch_size
```

이 코드에서 $y$ 는 신경망의 출력, $t$ 는 정답 레이블입니다.

정답 레이블이 원-핫 인코딩이 아니라 숫자 레이블로 주어진 경우 교차엔트로피 오차는 다음과 같이 구현할 수 있습니다.

```python
def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size
```

이 구현에서는 원-핫 인코딩일 때 $t$ 가 0 인 원소는 교차 엔트로피 오차도 0 이므로 그 계산은 무시해도 좋다는것이 핵심입니다. 다시 말하면 정답에 해당하는 신경망의 출력만으로 교차 엔트로피 오차를 계산할 수 있습니다. 그래서 원-핫 인코딩 시 `t * np.log(y)` 였던 부분을 레이블로 표현일 때는 `np.log(y[np.arrange(batch_size), t])` 로 구현합니다.

참고로 위 예제에서 `np.log(y[np.arrange(batch_size), t])` 코드는 `[y[0, 2], y[1, 7], y[2, 0] ... ]` 인 Numpy 배열을 생성합니다.

### Why Set the Loss Function?

신경망 학습에서의 궁극적인 목표는 높은 정확도를 끌어내는 매개변수를 찾는것입니다. 그렇다면 정확도가 아닌 손실 함수의 값 이라는 우회적인 방법을 택하는 이유가 무엇일까요

이 의문은 신경망 학습에서의 미분의 역할에 주목하면 해결됩니다. 신경망에서는 최적의 매개변수를 탐색할 때 손실 함수의 값을 가능한 한 작게 하는 매개변수 값을 찾습니다. 이때 매개변수의 미분을 계산하고, 그 미분 값을 단서로 매개변수의 값을 서서히 갱신하는 과정을 반복합니다.

가중치 매개변수의 손실 함수의 미분이란 *가중치 매개변수의 값을 변화시켰을때, 손실 함수가 어떻게 변하냐* 라는 의미입니다.

만약 미분 값이 음수인경우 가중치를 양의 방향으로 변화시키면 됩니다. 반대로 미분 값이 양수인 경우 가중치를 음의 방향으로 변화시킵니다. 그러다 미분 값이 0 이되면 어느쪽으로 움직여도 손실함수의 값이 줄어들지 않으므로 매개변수의 갱신은 멈춥니다.

> 만약 정확도로 지표를 삼는경우 매개변수의 미분이 대부분의 장소에서 0 이되므로 안된다.

계단 함수의 미분은 `Example 4` 와 같이 대부분의 장소에서 0 입니다. 그 결과 계단 함수를 이용하면 손실 함수를 지표로 삼는게 아무 의미가 없어집니다. 매개변수의 작은 변화가 주는 파장을 계단함수가 말살하여 손실 함수의 값에는 아무런 변화가 없기 때문입니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/75603286-4eed4b80-5b10-11ea-8c67-1b18c401fd56.png)

계단 함수는 한순간만 변화를 일으키지만, 시그모이드 함수의 미분은 `Example 4` 와 같이 출력이 연속적으로 변하고 곡선의 기울기도 연속적으로 변합니다. 이는 시그모이드 함수의 미분은 어느 장소라도 0 이 되지 않습니다.

이는 신경망 학습에서 가장 중요한 성질로, 기울기가 0 이 되지 않는 덕분에 신경망이 올바르게 학습할 수 있습니다.

## Numerical Differential

경사법에서는 기울기 값을 기준으로 나아갈 방향을 정합니다. 여기서 기울기란 무엇인지 미분을 보면서 알아보겠습니다.

### Differential

미분이란 한 순간의 변화량을 표시한것입니다. 수식으로 나타내면 아래와 같습니다.

> Expression 4

$$
{df(x) \over dx} = \lim_{h->0} {f(x+h) - f(x) \over h}
$$

위 식은 함수의 미분을 나타낸 것입니다. 좌변은 $f(x)$ 의 $x$ 에 대한 미분을 나타내는 기호입니다. 결국 $x$ 의 작은 변화가 함수 $f(x)$ 를 얼마나 변화시키느냐를 의미합니다.

이때 시간의 작은 변화, 즉 시간을 뜻하는 $h$ 를 한없이 0 에 가깝게 한다는 의미를 $\lim _{h->0}$ 로 나타냅니다.

`Expression 4` 를 참고하여 함수를 미분하는 계산을 Python dmfh rngusgoqhrpTtmqslek.

```python
def numerical_diff(f, x):
    h = 10e-50
    return (f( + h) - f(x)) / h
```

위 구현에서는 개선해야할 점이 2 개 있습니다.

$h$ 에 가급적 작은 값을 대입하고 싶었기에 $10e-50$ 이라는 작은 값을 이용했습니다. 하지만 이 방식은 **반올림 오차(Rounding Error)** 문제가 있습니다. 반올림 오차는 작은 값이 생략되어 최종 계산 결과에 오차가 생기게 합니다. 파이썬에서의 반올림 오차로는 다음과 같은 예가 있습니다.

```python
>>> np.float32(1e-50)
0.0
```

이와 같이 $1e-50$ 을 float32 형으로 나타내면 0.0 이 되어 올바른 표현을 할 수 없습니다.

두 번재 개선은 함수 `f` 의 차분과 관련한것입니다. 앞의 구현에서는 `x+h` 와 `x` 사이의 함수 `f` 의 차분을 계산하지만, 애당초 이 계산에는 오차가 있습니다.

`Example 5` 와 같이 진정한 미분은 $x$ 위치의 함수의 기울기에 해당하지만 이 구현에서의 미분은 $(x + h)$ 와 $x$ 사이의 기울기에 해당합니다. 그래서 진정한 미분과 이번 구현의 값은 엄밀히 말하면 일치하지 않습니다. 이 차이는 $h$ 를 무한히 0 으로 좁히는것이 불가능해 생기는 한계입니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/75603295-5876b380-5b10-11ea-891f-0bfb45f4f9d9.png)

`Example 5` 처럼 수치 미분에는 오차가 포함됩니다. 이 오차를 줄이기 위해 $(x+h)$ 와 $(x-h)$ 의 함수 $f$ 의 차분을 계산하는 방법을 쓰기도 합니다.

이 차분은 $x$ 를 중심으로 그 전후의 차분을 계산한다는 의미에서 **중심차분** 혹은 **중앙차분** 이라 합니다.

이 두 개선점을 적용해 수치 미분을 다시 구현해보겠습니다.

```python
def numerical_diff(f, x):
    h = 1e-4
    return (f(x+h) - f(x-h)) / (2*h)
```

### An Example of a Numerical Differential

앞 절의 수치 미분을 사용하여 간단한 함수를 미분하겠습니다. 우선 다음과 같은 2차 함수 입니다.

> Expression 5

$$
y = 0.01x^2 + 0.1x
$$

`Exmpression 5` 를 Python 으로 구현하면 다음과 같습니다.

```python
def function_1(x):
    return 0.01*x**2 + 0.1*x
```

이어서 함수를 그려보겠습니다.

```python
import numpy as np
import matplotlib

x = np.arange(0.0, 20.0 0.1)
y = function_1(x)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.plot(x, y)
plt.show()
```

> Example 6

![image](https://user-images.githubusercontent.com/44635266/75603301-62001b80-5b10-11ea-8ec2-a19645f4aab0.png)

`x = 5` 와 `x = 10` 일 때 계산해보겠습니다.

```python
>>> numerical_diff(function_1, 5)
0.19999999999990898
>>> numerical_diff(function_1, 10)
0.29999999999986347
```

이렇게 계산한 미분 값이 $x$ 에 대한 $f(x) 의 변화량입니다. 즉, 함수의 기울기에 해당합니다. 또한 $f(x) = 0.01x^2 + 0.1x$ 의 해석적 해는 ${df(x) \over dx} = 0.02x + 0.1$ 입니다. 진짜 미분값을 계산하면 0.2, 0.3 입니다.

오차가 매우 작은것을 알 수 있습니다.

앞에서 구한 수치 미분 값을 기울기로 하는 직선을 그려보겠습니다. `Example 7` 을 보면 함수의 접선에 해당하는것을 알 수 있습니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/75603307-6a585680-5b10-11ea-80c2-42eedc63e225.png)

### partial differential

이어서 `Expression 6` 을 보겠습니다. 인수들의 제곱 합을 계산하는 단순한 식이지만, 변수가 2 개라는 점에 주의해야합니다.

> Expression 6

$$
f(x_0, x_1) = x^2_0 + x^2_1
$$

이 식은 Python 으로 다음과 같이 구현할 수 있습니다.

```python
def function_2(x):
    return x[0]**2 + x[1]**2
```

인수 x 는 Numpy 배열이라 가정 했을때, 이 코드는 배열의 각 원소를 제곱하고 그 합을 구하는 간단한 함수입니다. 이 함수의 그래프를 그리면 다음과 같이 3차원으로 그려집니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/75603309-6fb5a100-5b10-11ea-8d0a-df49917da6bf.png)

`Expression 6` 을 미분해 보겠습니다. 여기서는 변수가 2 개라서 둘 중 어느 변수에 대한 미분이냐를 구분해야 합니다. 이와 같이 변수가 여럿인 함수에 대한 미분을 **편미분** 이라 합니다. 편미분을 수식으로는 ${\partial f \over \partial x_0}$ 처럼 사용합니다.

${\partial f \over \partial x_0}$ 편미분을 구해보겠습니다.

```python
>>> def function_tmp1(x0):
...    return x0*x0 + 4.0 ** 2.0
...
>>> numerical_diff(fuction_tmp1, 3.0)
6.00000000378
```

${\partial f \over \partial x_1}$ 편미분을 구해보겠습니다.
```python
>>> def function_tmp1(x1):
...    return 3.0 ** 2.0 + x1*x1
...
>>> numerical_diff(fuction_tmp2, 4.0)
7.99999999119
```

이처럼 편미분도 변수가 하나인 미분과 마찬가지로 특정 장소의 기울기를 구합니다. 단 여러 변수 중 목표 변수 하나에 초저믕ㄹ 맞추고 다른 변수는 값을 고정합니다.

## Gradient

만약 편미분을 동시에 계산하고 싶다면 어떻게 할까요. 이때 아래 처럼 모든 변수의 편미분을 벡터로 정리한 것을 **기울기(Gradient)** 라고 합니다. 기울기는 다음과 같이 구현이 가능합니다.

$$
({\partial f \over \partial x_0}
{\partial f \over \partial x_1})
$$

```python
def numerical_gradient(f, x):
    h = 1e-4
    grad = np.zeros_like(x)

    for idx in range(x.size):
        tmp_val = x[idx]

        #f(x+h) 계산
        x[idx] = tmp_val + h
        fxh1 = f(x)

        #f(x-h) 계산
        x[idx] = tmp_val -h
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2*h)
        x[idx] = tmp_val

    return grad
```

`numerical_gradient(f, x)` 함수의 구현은 복잡해 보이지만, 동작 방식은 변수가 하나일 때의 수치 미분과 동일합니다. `np.zeros_like(x)` 는 `x` 와 형상이 같고 그 원소가 모두 0 인 배열을 만듭니다.

이 함수를 사용하여 실제 기울기를 계산해보겠습니다.

```python
>>> numerical_gradient(function_2, np.array([3.0, 4.0]))
array([ 6., 8.])
>>> numerical_gradient(function_2, np.array([0.0, 2.0]))
array([ 0., 4.])
>>> numerical_gradient(function_2, np.array([3.0, 0.0]))
array([ 6., 0.])
```

이 처럼 $(x_0, x_1)$ 의 각 점에서 기울기를 계산할 수 있습니다. 이 기울기라는게 의미하는지 알아보겠습니다. 기울기의 결과에 마이너스를 붙인 벡터를 그려보겠습니다.

> Example 9

![image](https://user-images.githubusercontent.com/44635266/75603312-793f0900-5b10-11ea-8837-1d41226fa2ea.png)


`Example 9` 처럼 방향을 가진 벡터로 그려집니다. 이 기울기는 함수의 가장 낮은 장소(최솟값) 을 가리킵니다. 또한, 가장 낮은 곳에서 멀어질 수록 화살표의 크기가 커지는것을 볼 수 있습니다.

즉 ***기울기가 기리키는 쪽은 각 장소에서 함수의 출력 값을 가장 크게 줄이는 방향*** 이라고 볼 수 있습니다.

### Gradient (Gradient Descent Method)

기계학습 문제는 대부분 학습단계에서 최적의 매개변수를 찾습니다. 여기서 최적이란 손실 함수가 최솟값이 될 때의 매개변수 값입니다. 하지만 손실함수는 매우 복잡하고매개변수 공간이 광대하여 어디가 최솟값이 되는지 짐작할 수 없습니다.

이런 상황에서 기울기를 이용해 함수의 최솟값을 찾으려는 것이 경사법입니다.

> 함수가 극솟값, 최솟값 또 안장점(Saddle Point) 가 되는 장소에서의 기울기는 0 입니다.

경사법은 현 위치에서 기울어진 방향으로 일정 거리만큼 이동합니다. 그 다음 이동한곳에서 기울기를 구하고 기울어진 방향으로 나아가기를 반복합니다.

이렇게 함수의 값을 점차 줄이는 것이 **경사법(Gradient Method)** 입니다. 경사법은 기계학습을 최적화하는 데 흔히 쓰는 방법입니다.

수식으로 나타내면 아래와 같습니다.

> Expression 7

$$
x_0 = x_0 - \eta { \partial f \over \partial x_0} \\
x_1 = x_1 - \eta { \partial f \over \partial x_1}
$$

$\eta$ 의 기호 Eta 는 갱신하는 양을 나타냅니다. 이를 신경망 학습애서는 **학습 률(Learnging Rate)** 라고 합니다. 한 번의 학습으로 얼만큼 학습할 지, 즉 매개변수 값을 얼마나 갱신하냐를 정하는것이 학습률 입니다.

`Expression 7` 은 1 회에 해당하는 갱신이고 이 단계를 반복합니다.

또한 학습률 값은 0.01 이나 0.001 등 미리 특정한 값으로 정해두어야 합니다. 일반적으로 이 값이 너무 크거나 작으면 좋은 장소를 찾아갈 수 없습니다.

경사 하강법은 다음과 같이 간단하게 구현할 수 있습니다.

```python
def gradient_descent(f, init_x, lr=0.01, step_num=100):
    x = init_x

    for i in range(step_num):
        grad = numerical_gradient(f, x)
        x -= lr * grad
    return x
```

인수 `f` 는 최적화하려는 함수, `init_x` 는 초깃값, `lr` 은 *Learning Rate* 를 의미하는 학습률, `step_num` 은 경사법에 따른 반복 횟수를 뜻합니다. 함수의 기울기는 `numerical_gradient(f, x)` 로 구하고, 그 기울기에 따라 학습률을 곱한 값으로 갱신하는 처리를 `step_num` 번 반복합니다.

경사법으로 $f(x_0, x_1) = x_0^2 + x_1^2$ 의 최솟값을 구하겠습니다.

```python
def function_2(x):
... return x[0]**2 + x[1]**2
...
>>> init_x = np.array([-3.0, 4.0])
>>> gradient_descent(function_2, init_x=init_x, lr=0.1, step_num=100)
array([-6.11110793e-10, 8.14814391e-10])
```

초기값을 (-3.0, 4.0) 으로 설정한 후 경사법을 사용해 최솟값 탐색을 시작합니다. 최종 결과는 (-6.1e-10, 8.1e-10) 으로 거의 (0, 0) 에 가까운 결과로 정확한 결과를 얻은것입니다.

경사법을 사용하는 갱신 과정을 그림으로 나타내면 `Example 10` 처럼 됩니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/75603330-9ecc1280-5b10-11ea-93f4-f4db34d35584.png)

학습률이 너무 크거나 작은 경우에도 알아보겠습니다.

```python 
# lr = 10.0
>>> init_x = np.array([-3.0, 4.0])
>>> gradient_descent(function_2, init_x=init_x, lr=10.0, step_num=100)
array([-2.58983747e+13, -1.29524862e+12])

# lr = 1e-10
>>> init_x = np.array([-3.0, 4.0])
>>> gradient_descent(function_2, init_x=init_x, lr=1e-10, step_num=100)
array([-2.999994, 3.999992])
```

학습률이 너무 크면 발산하고 작으면 갱신되지 않은 채 끝나버립니다.

> 학습률 같은 매개변수를 **Hyper Parameter** 라 합니다. 가중치와 편향과는 다릅니다. 가중치는 자동으로 획득되는 매개변수이지만 학습률은 사람이 직접 설정해야 합니다.

### Gradient in Neural Network

신경망 학습에서도 기울기를 구해야합니다. 여기서 말하는 기울기는 가중치 매개변수에 대한 손실 함수의 기울기입니다. 예를 들어 형상아 2 X 3, 가중치가 $W$, 손실 함수가 $L$ 인 신경망을 생각해보겠습니다. 이 경우 경사는 ${ \partial L \over \partial W}$ 로 나타낼 수 있습니다. 수식은 아래와 같습니다.

$$
W = \begin{pmatrix}
w_{11} \; w_{21} \; w_{31} \\
w_{12} \; w_{22} \; w_{32}  
\end{pmatrix} \\

{ \partial L \over \partial W} = \begin{pmatrix}
{ \partial L \over \partial W_{11} } { \partial L \over \partial W_{12} } { \partial L \over \partial W_{13} } \\
{ \partial L \over \partial W_{21} } { \partial L \over \partial W_{22} } { \partial L \over \partial W_{23} }
\end{pmatrix}
$$

${ \partial L \over \partial W}$ 의 각 원소는 각각의 원소에 관한 편미분 입니다. 예를들어 각 1행 1 번째 원소를 변경했을때 손실 함수 L 이 얼마나 변화느냐를 나타냅니다. 여기서 중요한 점은 ${ \partial L \over \partial W}$ 의 형상이 $W$ 와 같다는 것입니다.

간단한 신경망을 예로 들어 실제로 기울기를 구하는 코드를 보겠습니다. 전체 코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch04/gradient_simplenet.py) 에 있습니다.

```python
import sys, os
sys.path.append(os.pardir)
import numpy as np
from common.functions import softmax, cross_entropy_error
from common.gradient import numerical_gradient

class simpleNet:
    def __init__(self):
        self.W = np.random.randn(2,3)

    def predict(self, x):
        return np.dot(x, self.W)

    def loss(self, x, t):
        z = self.predict(x)
        y = softmax(z)
        loss = cross_entropy_error(y, t)

        return loss
```

`predict(x)` 함수는 예측을 수행하는 함수이며, `loss(x, t)` 는 손실 함수의 갑승ㄹ 구하는 함수입니다. 인수 `x` 는 입력 데이터, `t` 는 정답 레이블입니다.

```python
>>> net = simpleNet()
>>> print(net.W)
[[ 0.47355232 0.9977393 0.84668094]
 [ 0.85557411 0.0356366 0.69422093]]
>>>
>>> x = np.array([0.6, 0.9])
>>> p = net.predict(x)
>>> p
[ 1.05414809 0.63071653 1.1328074]
>>> np.argmax(p)
2
>>>
>>> t = np.array([0, 0, 1])
>>> net.loss(x, t)
0.92806853663411326
```

이어서 기울기를 알아보겠습니다. `numerical_gradient(f, x)` 를 써서 구하면 됩니다.

```python
>>> def f(W):
...     return net.loss(x, t)
...
>>> dW = numerical_gradient(f, net.W)
>>> print(dW)
[[ 0.21924763 0.14356247 -0.36281009 ]
 [ 0.32887144 0.2153437  -0.54421514 ]]
```

`numerical_gradient(f, x)` 의 인수 `f` 는 함수, `x` 는 함수 `f` 의 싱ㄴ수입니다. 여기서 `net.W` 를 인수로 받아 손실함수를 계산하는 함수를 정의했습니다. 그리고 정의한 함수를 `numerical_gradient(f, x)` 에 넙깁니다.

$dW$ 는 `numericla_gradient(f, net.W)` 의 결과입니다. $dW$ 의 내용을 보면, 예를 들어 ${ \partial L \over \partial W}$ 의 ${ \partial L \over \partial W_{11}}$ 은 대략 0.2 입니다. 이는 $w_{11}$ 을 $h$ 만큼 늘리면 손실 함수의 값은 $0.2h$ 만큼 증가한다는 의미입니다.

그래서 손실 함수를 줄인다는 의미는 ${ \partial L \over \partial w_{23}}$ 은 양의 방향으로 갱신하고 $w_{11}$ 은 음의 방향으로 갱신해야 함을 알 수 있습니다.

Python 에서는 **lambda** 를 사용하면 더 쉽게 구현할 수 있습니다.

```python
>>> f = lambda w: net.loss(x, t)
>>> dW = numerical_gradient(f, net.W)
```

신경망의 기울기를 구한 다음에는 경사법에 따라 가중치 매개변수를 갱신하기만 하면 됩니다.

## Implementing Learning Algorithms

신경망 학습의 절차는 다음과 같습니다.

* 전제
  * 신경망에서는 적응 가능한 가중치와 편향이 잇고, 이 가중치와 편향을 훈련 데이터에 적응하도록 조정화는 과정을 학습이라 합니다.
  * 신경망 학습은 다음 4 단계로 수행합니다.
* 1.미니배치
  * 훈련 데이터중 일부를 무작위로 가져와서 이 선별한 데이터를 이용하여 손실 함수 값을 줄인다.
* 2.기울기 산출
  * 미니배치의 손실 함수 값을 줄이기 위해 각 가중치 매개변수의 기울기를 구한다. 기울기는 손실 함수의 값을 가장 작게 하는 뱡향을 제시
* 3.매개변수 갱신
  * 가중치 매개변수를 기울기 방향으로 조금 갱신
* 4.반복
  * 1 ~ 3 단계를 반복합니다.

이는 경사 하강법으로 매개변수를 갱신하는 방법이며, 이때 데이터를 미니배치로 무작위로 선정하기 때문에 **확률적 경사 하강법(Stochastic Gradient Descent, SGD)** 라고 합니다. 대부분 딥러닝 프레임워크는 확률적 경사 하강법의 영어 머리글자를 딴 SGD 함수로 이 기능을 구현합니다.

### Implementing a Two-Layer Neural Network Class

처음에는 2 층 신경망을 하나의 클래스로 구현하는 것부터 시작합니다. 이 전체소스는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch04/two_layer_net.py) 에 있습니다.

```python
class TwoLayerNet:

    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        # 가중치 초기화
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)
    
    def predict(self, x):
        ...

    def loss(self, x, t):
        ...

    def accuracy(self, x, t):
        ...

    def numerical_gradient(self, x, t):
        ...
        
    def gradient(self, x, t):
        ...
```

이 클래스에서 사용하는 변수와 메소드를 정리해보겠습니다.

**변수**

|Variables|Description|
|:--|:--|
|params|신경망의 매개변수를 보관하는 딕셔너리 변수|
|grads|기울기 보관하는 딕셔너리 변수|

**메소드**

|Methods|Description|
|:--|:--|
|_ _init _ _(self.input_size, hidden_size, output_size|초기화 수행, 인수는 순서대로 입력층의 뉴런 수, 은닉층의 뉴런 수, 출력층의 뉴런 수|
|predict(self, x)|예측을 수행한다. x 는 이미지 데이터|
|loss(self.x, t)|손실 함수의 값을 구한다, x 는 이미지 데이터, t 는 정답 레이블|
|accuracy(self.x, t)|정확도를 구한다|
|numerical_gradient(self.x, t)|가중치 매개변수의 기울기를 구한다.|
|gradient(self.x, t)|가중치 매개변수의 기울기를 구한다.|

### Implement Mini-Batch Learning

위에서 알아본 클래스와 MNIST 데이터 셋을 사용하여 미니 배치 학습을 수행해보겠습니다.

```python
import sys, os
sys.path.append(os.pardir) 
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

iters_num = 10000  
train_size = x_train.shape[0]
batch_size = 100   
learning_rate = 0.1

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)

for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    grad = network.gradient(x_batch, t_batch)
        
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key]
    
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

markers = {'train': 'o', 'test': 's'}
x = np.arange(len(train_acc_list))
plt.plot(x, train_acc_list, label='train acc')
plt.plot(x, test_acc_list, label='test acc', linestyle='--')
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()
```

여기서는 미니배치 크기를 100 개로 했습니다. 그리고 그 100 개의 미니배치를 대상으로 확률적 경사 하강법을 수행해 매개변수를 갱신합니다. 경사법에 의한 갱신 횟수를 10,000 번으로 설정했습니다. `Example 11` 은 손실 함수의 값이 변화하는 추이를 그래프로 나타낸것입니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/75603334-ab506b00-5b10-11ea-991e-908ff536a4fb.png)

그래프로 확인하면 학습 횟수에 따라 손실 함수의 값이 줄어드는걸 볼 수 있어서 학습하면서 신경망의 가중치 매개변수가 데이터에 적응하고 있음을 의미합니다.

### Evaluate with Test Data

`Example 11` 의 결과로 학습을 반복함으로 손실 함수의 값이 서서히 내려가는것을 확인할 수 있습니다.

하지만 훈련 데이터 외의 데이터를 올바르게 인식하는지를 확인해야 합니다. 다른 말로 **과적합(Overfitting)** 을 일으키는지 확인해야 합니다. 과적합이 된다는 것은, 훈련 데이터에 포함된 이미지만 제대로 구분하고, 다른 이미지는 식별할 수 없다는 의미입니다.

신경망 학습의 원래 목표는 범용적인 능력을 익히는 것이기 때문에 정확도를 기록해보겠습니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/75603339-b4413c80-5b10-11ea-8505-c944f49f763b.png)

`Example 12` 는 위 예제의 훈련 데이터와 시험 데이터에 대한 정확도 추이입니다.

**Train_acc** 와 **test_acc** 의 정확도에는 차이가 없는것을 알 수 있습니다. 다시 말해 과적합이 일어나지 않았습니다.