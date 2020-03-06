---
title : Machine Learning Neural Network
tags :
- Activation Function
- Neural Network
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch]() 를 바탕으로 작성하였습니다.*

신경망을 이용하면 사람이 수동으로 설정해야하는 가중치 매개변수의 적절한 값을 데이터로부터 자동으로 학습하여 설정합니다.

## From Perceptron to Nerual Network

신경망을 그림으로 나타내면 `Example 1` 처럼 됩니다. 가장 왼쪽 줄을 **입력층(Input Layer)** 맨 오른쪽 층을 **출력층(Output Layer)** 중간 줄을 **은닉층(Hidden Layer)** 라 합니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/75087691-05888380-5587-11ea-9529-6afca470e96a.png)

### Review Perceptron

먼저 퍼셉트론을 복습해보겠습니다. `Example 2` 와 같은 네트워크를 생각해보겠습니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/75087706-146f3600-5587-11ea-86ee-25617f13a337.png)

위 `Example 2` 는 두 신호를 입력받아 y 를 출력하는 퍼셉트론입니다. 이 퍼셉트론을 수식으로 나타내면 아래와 같습니다.

> Expression 1

$$y = 
\begin{cases}
0\;(b + w_1x_1 + w_2x_2 \le \theta) \\
1\;(b + w_1x_1 + w_2x_2 > \theta)
\end{cases}
$$

여기서 
$b$ 는 **편향** $w$ 는 **가중치** 를 나타내는 매개변수입니다. 하지만 `Example 2` 에서는 편향 $b$ 가 안보입니다. 여기에 편향을 명시한다면 `Example 3` 과 같습니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/75087710-1cc77100-5587-11ea-91f5-715644741935.png)

`Example 3` 에서는 가중치가 $b$ 이고 입력이 1 인 뉴런이 추가되었습니다. 이 퍼셉트론의 동작은 $x1, x2, 1$ 이라는 3 개의 신호가 뉴런에 입력되어, 각 신호에 가중치를 곱한 후 다음 뉴런에 전달됩니다.

다음 뉴런에서는 이 신호들의 갑승ㄹ 더하여 그 합이 0 을 넘으면 1 을 출력하고 그렇지 않으면 0 을 출력합니다. 참고로, 편향의 입력 신호는 항상 1 이기 때문에 그림에서는 해당 뉴런을 회색으로 채워 다른 뉴런과 구별했습니다.

위 식을 간결한 형태로 작성해 보겟습니다. 아래 두 식처럼 만들 수 있습니다.

> Expression 2

$$ y = h(b + w_1x_1 + w_2x_2) $$

> Expression 3

$$
y = 
\begin{cases}
0
(x\le 0) \\
1(x > 0)
\end{cases}
$$

`Expression 2` 은 입력 신호의 총합이 $h(x)$ 라는 함수를 거쳐 변환되어, 그 변환된 값이 y 의 출력이 됨을 보여줍니다. 그리고 `Exporesson 2` 의 $h(x)$ 함수는 입력이 0 을 넘으면 1을 돌려주고 그렇지 않으면 0 을 돌려줍니다. 결과적으로 동작하는 방식이 같습니다.

### Appearance of Activation Function

입력신호의 총합을 출력 신호로 변환하는 함수를 일반적으로 **활성화 함수(activation function)** 라 합니다.

그럼 `Expression 2` 를 다시 사용해보겠습니다. `Expression 2` 는 가중치가 곱해진 입력 신호의 총합을 계산하고, 그 합을 활성화 함수에 입력해 결과를 내는 2 단계로 처리됩니다. 그래서 이 식은 다음과 같은 2 개의 식으로 나타낼 수 있습니다.

> Expression 4

$$
a = b+ w_1x_1 + w_2x_2
$$

> Expression 5

$$
y = h(a)
$$

`Expression 4` 는 가중치가 달린 입력 신호와 편향의 총합을 계산하고, 이를 $a$ 라 합니다. 그리고 `Expression 5` 는 $a$ 를 함수 $h()$ 에 넣어 $y$ 를 출력하는 흐름입니다.

지금까지와 같이 뉴런을 큰 원으로 그려보면 `Expression 4` , `Expression 5` 는 `Example 4` 처럼 나타낼 수 있습니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/75087712-2355e880-5587-11ea-8f43-6c54e4ec0c7f.png)

위 그림과 같이 뉴런의 원을 키우고 그 안에 활성화 함수의 처리 과정을 명시적으로 그려 넣었습니다. 가중치 신호를 조합한 결과가 $a$ 라는 노드가 되고, 활성화 함수 $h()$ 를 통과하여 $y$ 라는 노드로 변환되는 과정이 나타나 있습니다.

참고로 뉴런과 노드라는 용어는 같은 의미로 사용합니다.

## Activation Function

`Exporession 3` 과 같은 활성화 함수는 임계값을 경계로 출력이 바뀌는데, 이런 함수를 **계단 함수(Step Function)** 이라 합니다. 신경망에소 사용하는 활성화 함수를 살펴보겠습니다.

### Sigmoid Function

다음은 신경망에서 자주 사용하는 활성화 함수인 **시그모이드 함수(Sigmoid Function)** 를 나타낸 식입니다.

> Expression 6

$$
h(x) = {1 \over 1 + exp(-x)}
$$

$exp(-x)$ 는 $e^{-x}$ 를 뜻하며 $e$ 는 자연상수 2.7182.. 의 값을 가지는 실수입니다.

`Expression 6` 으로 나타내는 시그모이드 함수는 복잡해 보이지만 단순한 함수입니다. 함수는 입력을 주면 출력을 돌려주는 변환기입니다. 예를 들어 시그모이드 함수에 1.0 과 2.0 을 입력하면

$h(1.0) = 0.731...$ h(2.0) = 0.880...$ 처럼 특정 값을 출력합니다.

신경망에서는 활성화 함수로 시그모이드 함수를 이용하여 신호를 변환하고 그 변환된 신호를 다음 뉴런에 전달합니다.

활성화 함수로 이용되는 시그모이드 함수를 계단 함수와 비교하며 알아보겠습니다.

### Implementing Stair Functions

계단함수는 `Expression 3` 과 같이 입력이 0 을 넘으면 1 을 출력하고, 그 외에는 0 을 출력하는 함수입니다.

아래는 계단 함수를 단순하게 구현한 예제입니다.

```python
def step_function(x):
    if x > 0:
        return 1
    else:
        return 0
```

이 구현은 단순하고 쉽지만, 인수 x 는 실수만 받아들입니다. 즉, `step_function(3.0)` 은 되지만 Numpy 배열을 인수로 넣을 수는 없습니다. Numpy 배열도 지원하기 위해 다음과 같은 구현도 생각할 수 있습니다.

```python
def step_function(x):
    y = x > 0
    return y.astype(np.int)
```

두 줄이라 엉성해보이지만 Numpy 의 편리한 트릭을 사용한 덕분입니다. Python 인터프리터를 통해 알아보겠습니다.

```python
>>> import numpy as np
>>> x = np.array([-1.0, 1.0, 2.0])
>>> x
array([-1., 1., 2.])
>>> y = x > 0
>>> y
array([False, True, True], dtype=bool)
```

Numpy 배열에 부등호 연산을 수행하면 배열의 선고 각각에 부등호 연산을 수행한 배열이 생성됩니다.

y 는 bool 배열입니다. 여기서 우리가 원하는 계단 함수는 0 이나 1 의 int 형을 출력하는 함수입니다. 그래서 배열 y 의 원소를 bool 에서 int 형으로 바꿔보겠습니다.

```python
>>> y = y.astype(np.int)
>>> y
array([0, 1, 1])
```

이처럼 Numpy 배열의 자료형을 변환할 때는 `astype()` 메소드를 이용합니다. 원하는 자료형을 인수로 지정하면 됩니다.

### Graph of Stair Function

`matplotlib` 를 이용해 계산함수를 그래프로 그려보겠습니다.

```python
import numpy as np
import matplotlib.pylab as plt


def step_function(x):
    return np.array(x > 0, dtype=np.int)

X = np.arange(-5.0, 5.0, 0.1)
Y = step_function(X)
plt.plot(X, Y)
plt.ylim(-0.1, 1.1) 
plt.show()
```

`np.arrange(-5.0, 5.0, 0.1)` 은 -5.0 에서 5.0 전까지 0.1 간격의 Numpy 배열을 생성합니다. `step_function()` 은 인수로 받은 Numpy 배열의 원소 각각을 인수로 계단 함수 실행해 그 결과를 다시 배열로 만들어 돌려줍니다. 이 x, y 배열을 그래프로 그리면 `Example 6` 처럼 됩니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/75087727-4aacb580-5587-11ea-9bf7-19964dfa66ab.png)

`Example 6` 에서 보듯이 계단 함수는 0 을 결계로 출력이 0 에서 1로 바뀝니다.

### Implement a Sigmoid Function

이제 `Expression 6` 을 이용하여 시그모이드 함수를 작성해보겠습니다.

```python
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
```

`np.exp(-x)` 는 `exp(-x)` 수식에 해당합니다.

```python
>>> x = np.array([-1.0, 1.0, 2.0])
>>> sigmoid(x)
array([0.26894142, 0.73105858, 0.88079708])
```

이 함수가 Numpy 배열도 훌룡히 처리할 수 있는 비밀은 브로드캐스트에 있습니다. 브로드캐스트 기능이란 Numpy 배열과 스칼라 값의 연산을 넘어 Numpy 배열의 원소 각각과 스칼라값의 연산으로 바꿔 수행하는 것입니다.

예를 통해 알아보겠습니다.

```python
>>> t = np.array([1.0, 2.0, 3.0])
>>> 1.0 + t
array([2., 3., 4.])
>>> 1.0 / t
array([1.        , 0.5       , 0.33333333])
```

스칼라 값 1.0 과 Numpy 배열 사이에서 수치 연산을 했습니다. 결과적으로 스칼라값과 Numpy 배열의 각 원소 사이에서 연산이 이뤄지고, 연산 결과가 Numpy 배열로 출력됩니다. 앞에서 구현한 `sigmoid` 함수도 `np.exp(-x)` 가 Numpy 배열을 반환하기 때문에 `1 / (1 + np.exp(-x))` 도 Numpy 배열의 각 원소에 연산을 수행한 결과를 내줍니다.

시그모이드 함수를 그려보겠습니다.

```python
x = np.arrange(-5.0, 5.0, 0.1)
y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()
```

이 코드를 실행하면 `Example 7` 의 그래프를 보실 수 있습니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/75087735-58fad180-5587-11ea-937e-e5fe30e6f87a.png)

### Comparison of Sigmoid Function and Stair Function

> Example 8

![image](https://user-images.githubusercontent.com/44635266/75087736-60ba7600-5587-11ea-82d8-f78efccd886b.png)

`Example 8` 을 보면 가장 먼저 느끼는 점은 기울기의 차이입니다. 시그모이드 함수는 계단함수와 달리 입력에 따라 출력이 연속적으로 변화합니다.

또한 계단 함수가 0 과 1 중 하나의 값만 돌려주는 반면 시그모이드 함수는 실수를 돌려줍니다.

### Nonlinear Function

계단 함수와 시스모이드 함수 모두 **비선형 함수** 입니다.

신경망에서는 활성화 함수로 비선형 함수를 사용해야 합니다. 왜냐하면, 선형 함수를 이용하면 신경망의 층을 깊게 하는 의미가 없어지기 때문입니다.

선형 함수의 문제는 층을 아무리 깊게 해도 은닉층이 없는 네트워크로도 똑같은 기능을 할 수 있습니다. 예를 들어 선형함수인 $h(x) = cs$ 를 활성화 삼수로 사용한 3 층 네트워크를 생각해보겠습니다. 이를 식으로 나타내면 $y(x) = h(h(h(x)))$ 가 됩니다. 이 계산은 $y(x) = c * c * c * x$ 처럼 곱셈을 3 번 수행하지만 실은 $y(x) = ax$ 와 같은 식입니다. $a = c^3$ 입니다.

즉, 은닉층이 없는 네트워크로 표현할 수 있습니다. 그래서 층을 쌓는 혜택을 얻고 싶다면 활성화 함수로는 반드시 비선형 함수를 사용해야 합니다.

### ReLU Function

최근에는 **ReLU(Rectified Linear Unit)** 함수를 주로 이용합니다.

ReLU 는 입력이 0 을 넘으면 그 입력을 그대로 출력하고 0 이하이면 0 을 출력하는 함수입니다.

> Example 9

![image](https://user-images.githubusercontent.com/44635266/75087739-67e18400-5587-11ea-830b-c33593710cc9.png)

수식으로는 다음과 같이 사용할 수 있습니다.

> Expression 7

$$
y = 
\begin{cases}
x \; ( x > 0) \\
0 \; ( x \le 0)
\end{cases}
$$

수식에서 보듯이 간단하게 구현할 수 있습니다.

```python
def relu(x):
    return np.maximum(0, x)
```

## Calculation of Multidimension Array

Numpy 의 다차원 배열을 사용한 계산법을 숙달하면 신경망을 효율적으로 구현할 수 있습니다.

### Multidimension Array

다차원 배열의 기본은 *숫자의 집합* 입니다. 숫자가 한 줄로 늘어선 것이나 직사각형으로 늘어선 것, N 차원으로 나열하는것을 다차원 배열이라고 합니다. Numpy 배열을 이용하여 다차원 배열을 만들어보겠습니다.

```python
>>> A = np.array([1, 2, 3, 4])
>>> A
array([1, 2, 3, 4])
>>> np.ndim(A)
1
>>> A.shape
(4,)
```
이와같이 배열의 차원 수는 `np.ndim()` 으로 확인할 수 있습니다. 배열의 형상은 `shape` 으로 알 수 있습니다.

2차원 배열을 작성해보겠습니다.

```python
>>> B = np.array([[1, 2], [3, 4], [5, 6]])
>>> B
array([[1, 2],
       [3, 4],
       [5, 6]])
>>> np.ndim(B)
2
>>> B.shape
(3, 2)
```

위 배열을 그림으로 표현하면 `Example 10` 과 같습니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/75087742-6f089200-5587-11ea-9d82-2de098f518a8.png)

2 차원 배열은 특히 **행렬(matrix)** 라 하며, 가로 방향을 **행(Row)** 세로 방향을 **열(Column)** 이라고 합니다.

### Multiplying Matrix

2 x 2 행렬의 곱은 아래 `Example 11` 과 같이 계산합니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/75087744-75970980-5587-11ea-9b59-3b9bb1bdd56e.png)

왼쪽 행렬의 행과 오른쪽 행렬의 열을 원소별로 곱하고 그 값들을 더해서 계산합니다. 그리고 그 계산 결과가 새로운 다차원 배열의 원소가 됩니다. 이 계산을 Python 으로 구현하면 다음과 같습니다.

```python
>>> A = np.array([[1, 2], [3, 4]])
>>> A.shape
(2, 2)
>>> B = np.array([[5, 6], [7, 8]])
>>> B.shape
(2, 2)
>>> np.dot(A, B)
array([[19, 22],
       [43, 50]])
```

이 코드에서 A 와 B 는 2 X 2 행렬이며 두 행렬의 곱은 Numpy 함수 `np.dot()` 으로 계산합니다.

아래에서는 2 X 3 행렬과 3 X 2 행렬의 곱을 Python 으로 구현해보겠습니다.

```python
>>> A = np.array([[1, 2, 3], [4, 5, 6]])
>>> A.shape
(2, 3)
>>> B = np.array([[1, 2], [3, 4], [5, 6]])
>>> B.shape
(3, 2)
>>> np.dot(A, B)
array([[22, 28],
       [49, 64]])
```

이때 행렬의 형상을 주의해야합니다. 구체적으로 말하면 행렬 A 의 1 번째 차원의 원소 수와 행렬 B 의 0 번째 차원의 원소수가 같아야 합니다. 이 값이 다르면 행렬의 곱을 계산할 수 없습니다. 예를 통해 알아보겠습니다.

```python
>>> C = np.array([[1, 2], [3, 4]])
>>> C.shape
(2, 2)
>>> A.shape
(2, 3)
>>> np.dot(A, C)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<__array_function__ internals>", line 6, in dot
ValueError: shapes (2,3) and (2,2) not aligned: 3 (dim 1) != 2 (dim 0)
```

아래 `Example 12` 를 통해 다시 정리하겠습니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/75087747-821b6200-5587-11ea-82c1-c3c394187a32.png)

A 가 2 차원 해열ㄹ이고 B 가 1 차원 배열일 때도 `Example 13` 과 같이 차원의 원소스를 일치시켜야 하는 원칙은 똑같이 적용됩니다.

> Example 13

![image](https://user-images.githubusercontent.com/44635266/75087751-8a739d00-5587-11ea-87eb-f504dba9976d.png)

```python
>>> A = np.array([[1, 2], [3, 4], [5, 6]])
>>> A.shape
(3, 2)
>>> B = np.array([7, 8])
>>> B.shape
(2,)
>>> np.dot(A, B)
array([23, 53, 83])
```

### Matrix Multiplication in Neural Network

Numpy 행렬을 써서 신경망을 구현해보겠습니다. `Example 14` 의 간단한 신경망을 가정해보겠습니다. 이 신경망은 편향과 활성화 함수를 생략하고 가중치만 가집니다.

> Example 14

![image](https://user-images.githubusercontent.com/44635266/75087756-919aab00-5587-11ea-948b-8b84b0f0c7de.png)

이 구현에서도 X, W, Y 의 형상을 주의해야합니다. 특히 X 와 W 의 대응하는 차원의 원소 수가 같아야합니다.

```python
>>> X = np.array([1, 2])
>>> X.shape
(2,)
>>> W = np.array([[1, 3, 5], [2, 4, 6]])
>>> W
array([[1, 3, 5],
       [2, 4, 6]])
>>> W.shape
(2, 3)
>>> Y = np.dot(X, W)
>>> Y
array([ 5, 11, 17])
```

다차원 배열의 스칼라곱을 구해주는 함수를 사용하면 단번에 `Y` 를 계산할 수 있습니다.

## Implementation of a 3-Layer Neural Network

아래 `Example 15` 처럼 3 층 신경망에서 사용하는 입력부러 처리를 구현하겠습니다. Numpy 를 이용하면 간결하게 구현할 수 있습니다.

> Example 15

![image](https://user-images.githubusercontent.com/44635266/75104850-21f0f280-5651-11ea-8262-1acd1b6b11e1.png)

### Notation Description

$w_{12}^{(1)}$ 과 $a_1^{(1)}$  과 같은 표기법을 알아보겠습니다. 아래 `Example 16` 을 보겠습니다.

`Example 16` 은 입력층의 뉴런 $x_2$ 에서 다음 층의 뉴런 $a_1^{(1)}$ 로 향하는 선 위에 가중치를 표시하고 있습니다.

> Example 16

![image](https://user-images.githubusercontent.com/44635266/75104853-2a492d80-5651-11ea-8ab5-9e5f19899fc4.png)

가중치와 은닉층 뉴런의 오른쪽 위에는 $^{(1)}$ 라는 표시가 붙어있습니다. 이는 1 층의 가중치, 1 층의 뉴런임을 뜻하는 번호입니다. 또 가중치의 오른쪽 아래의 두 숫자는 차례로 다음 층 뉴런과 앞 층 뉴런의 인덱스 번호입니다.

### Implementing Signal Transmission on Each Layer

> Example 17

![image](https://user-images.githubusercontent.com/44635266/75104856-39c87680-5651-11ea-8952-43c5b6d2af4d.png)

`Example17` 과 같이 편향을 뜻하는 뉴런인 1 이 추가되었습니다. 편햔은 오른쪽 아래 인덱스가 하나밖에 없다는것에 주의하면 됩니다.

지금까지 확인한것을 반영하여 $a_1^{(1)}$ 을 수식으로 나타내보겠습니다.

> Expression 8

$$
a_1^{(1)} = w_{11}^{(1)}x_1 + w_{12}^{(1)}x_2 + b_1^{(1)}
$$

여기에서 행렬의 곱을 이용하면 1 층의 가중치 부분을 다음식처럼 간소화할 수 있습니다.

> Expression 9

$$
A^{(1)} = XW^{(1)} + B^{(1)}
$$

이때 행렬은 각각 아래와 같습니다.

$$
A^{(1)} = (a_1^{(1)} \; a_2^{(1)} \; a_3^{(1)}), \; X=(x_1 \; x_2), \;
B = (b_1^{(1)} \; b_2^{(1)} \; b_3^{(1)}) \;
W = \begin{pmatrix}
w_{11}^{(1)} \; w_{21}^{(1)} \; w_{31}^{(1)} \\
w_{12}^{(1)} \; w_{22}^{(1)} \; w_{32}^{(1)}  
\end{pmatrix}
$$

그럼 Numpy 배열을 사용해 `Expression 9` 를 구현해보겠습니다.

```python
X = np.array([1.0, 0.5])
W1 = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6])
B1 = np.array([0.1, 0.2, 0.3])

print(W1.shape) # (2, 3)
print(X.shape) # (2,)
print(B1.shape) # (3,)

A1 = np.dot(X, W1) + B
```

이 계산은 앞에서 한 계산과 같습니다. W1 은 2 X 3 행렬, X 는 원소가 2 개인 1 차원 배열입니다.

이어서 1 층의 활성화 함수에서의 처리를 알아보겠습니다. 이 활성화 함수의 처리를 그림으로 나타내면 아래와 같습니다.

> Example 18

![image](https://user-images.githubusercontent.com/44635266/75104858-4351de80-5651-11ea-920c-312ed94ba803.png)

`Example 18` 처럼 은닉층에서의 가중치 합을 $a$ 로 표기하고 활성화 함수 $h()$ 로 변환된 신호를 z 로 표기합니다. 여기서는 화럿ㅇ화 함수로 시그모이드 함수를 사용하기로 합니다. 이를 Python 으록 구현하면 아래와 같습니다.

```python
Z1 = sigmoid(A1)

print(A1) # [0.3, 0.7, 1.1]
print(Z1) # [0.57444252, 0.66818777, 075026011]
```

이 `sigmoid()` 함수는 앞에서 정의한 함수입니다. 이 함수는 Numpy 배열을 받아 같은 수의 원소로 구성된 Numpy 배열을 반환합니다.

이어서 1층에서 2층으로 가는 과정 `Example 19` 를 구현해보겠습니다.

> Example 19

![image](https://user-images.githubusercontent.com/44635266/75104863-4cdb4680-5651-11ea-820a-0cd364c0c583.png)

```python
W2 = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
B2 = np.array([0.1, 0.2])

print(Z1.shape) # (3,)
print(W2.shape) # (3, 2)
print(B2.shape) # (2,)

A2 = np.dot(Z1, W2) + B2
Z2 = sigmoid(A2)
```

이 구현은 1층의 출력 Z1 이 2층의 입력이 된다는 점을 제외하면 조금 전의 구현과 똑같습니다. 이처럼 Numpy 배열을 사용하면서 층 사이의 신호 전달을 쉽게 구현할 수 있습니다.

마지막으로 2층에서 출력층으로의 신호 전달입니다. 출력층의 구현도 이전과 동일합니다. 활성화 함수만 지금까지의 은닉층과 다릅니다.

> Example 20

![image](https://user-images.githubusercontent.com/44635266/75104875-7a27f480-5651-11ea-87e8-8a9cc2e9a802.png)

```python
def identity_function(x):
    return x

W3 = np.array([[0.1, 0.3], [0.2, 0.4]])
B3 = np.array([0.1, 0.2])

A3 = np.dot(Z2, W3) + B3
Y = identity_function(A3)
```

여기에서는 항등 함수인 `identity_function()` 을 정의하고 이를 출력층의 활성화 함수로 이용했습니다. 항등 함수는 입력을 그대로 출력하는 함수입니다. 이 예에서는 `identity_function()` 을 굳이 정의할 필요는 없지만 그동안의 흐름과 통일하기 위해 구현했습니다.

`Example 20` 에서는 출력층의 활성화 함수를 $\sigma()$ 로 표시하여 은닉층의 활성화 함수 $h()$ 와는 다름을 명시했습니다.

### Implementation Cleanup

지금까지의 구현을 정리해보겠습니다.

```python
def init_network():
    network = {}
    network['W1'] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6])
    network['b1'] = np.array([0.1, 0.2, 0.3])
    network['W2'] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    network['b2'] = np.array([0.1, 0.2])
    network['W3'] = np.array([[0.1, 0.3], [0.2, 0.4]])
    network['b3'] = np.array([0.1, 0.2])

    return network

def forward(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = identity_function(a3)

    return y

network = init_network()
x = np.array([1.0, 0,5])
y = forward(network, x)
print(y) # [ 0.31682708, 0.69627909]
```

여기서는 `init_network()` 와 `forward()` 함수를 정의했습니다. `init_network()` 함수는 가중치와 편향을 초기화하고 이들을 딕셔너리 변수인 `network()` 에 저장합니다. 이 딕셔너리 변수 `network` 에는 각 층에 필요한 매개변수를 저장합니다. 그리고 `forward()` 함수는 입력 신호를 출력으로 변환하는 처리과정을 모두 구현하고 있습니다.

함수 이름을 `forward` 라 한것은 신호가 순방향으로 전달됨을 알리고 위함입니다.

## To Design an Output Layer

신경망은 분류와 회귀 모두 이용할 수 있습니다. 둘 중 어던 문제냐에 따라 출력층에서 사용하는 활성화 함수가 달라집니다. 일반적으로 회귀에는 항등 함수를, 분류에는 소프트맥스 함수를 사용합니다.

> 기계학습은 **분류(Classification) 과 회귀(Regression)** 으로 나눕니다. 분류는 데이터가 어느 클래스에 속하냐는 문제입니다. 회귀는 입력 데이터에서 연속적인 수치를 예측하는 문제입니다.

### Implementing Identity Function and a Softmax Function

**항등 함수(Identity Function)** 는 입력을 그대로 출력합니다. 입력과 출력이 항상 같다는 뜻의 항등입니다. 그래서 출력층에서 항등 함수를 사용하면 입력 신호가 그대로 출력신호가 됩니다. 항등 함수의 처리는 신경망 그림으로 `Example 21` 과 같습니다.

> Example 21

![image](https://user-images.githubusercontent.com/44635266/75104877-8318c600-5651-11ea-8260-45cb6b39a7d1.png)

분류에서 사용되는 **소프트맥스 함수(Softmax Function)** 의 식은 다음과 같습니다.

> Expression 10

$$
y_k = { exp(a_k) \over \sum_{i=1}^n exp(a_i)}
$$

$exp(x)$ 는 $e^x$ 를 뜻하는 **지수 함수(Exponential Function)** 입니다. $n$ 은 출력층의 뉴런 수, $y_k$ 는 그 중 $k$ 번째 출력입니다. `Expression 10` 과 같이 소프트맥스 함수의 분자는 입력 신호 $a_k$ 의 지수 함수, 분모는 모든 입력 신호의 지수 함수의 합으로 구성됩니다.

이 소프트맥스 함수를 그림으로 나타내면 `Example 22` 처럼 됩니다. 그림과 같이 소프트맥스의 출력은 모든 입력신호로부터 화살표를 받습니다. `Expression 10` 의 분모에서 보듯 출력층의 각 뉴런이 모든 입력 신호에 영향을 받기 때문입니다.

> Example 22

![image](https://user-images.githubusercontent.com/44635266/75104880-8b710100-5651-11ea-9a99-3ff32d2a0769.png)

그럼 소프트맥스 함수를 구현해 보겠습니다.

```python
>>> a = np.array([0.3, 2.9, 4.0])
>>> exp_a = np.exp(a)
>>> exp_a
array([ 1.34985881, 18.17414537, 54.59815003])
>>> sum_exp_a = np.sum(exp_a)
>>> sum_exp_a
74.1221542101633
>>> y = exp_a / sum_exp_a
>>> y
array([0.01821127, 0.24519181, 0.73659691])
```

위 구현은 소프트맥스 함수를 그대로 Python 으로 표현한 것입니다.

```python
def softmax(a):
    exp_a = np.exp(a)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y
```

### Caution Points for Implementing Softmax Functions

`softmax()` 함수는 컴퓨터로 계산할 때는 결함이 있습니다. 바로 오버플로우 문제입니다. 소프트맥스 함수는 지수 함수를 사용하는데, 지수 함수는 쉽게 아주 큰 값을 내뱉습니다.

가령 $e^{10}$ 은 20,000 이 넘고 $e^{100}$ 은 0 이 40개가 넘는 큰 값이 됩니다. 그리고 이 큰 값끼리 나눗셈을 하면 수치가 불안정 해집니다.

이 문제를 해결하도록 소프트맥스 함수 구현을 개선해보겠습니다. 다음은 개선한 수식입니다.

> Expression 11

$$
\begin{align}

y = {exp(a_k) \over \sum^n_{i=1} exp(a_i)}

= {C exp(a_k) \over C \sum^n_{i=1} exp(a+i)} \\ 
= {exp(a_k + \log C) \over  \sum^n_{i=1} exp(a_i + \log C)} \\
= {exp(a_k + C`) \over \sum^n_{i=1} exp(a_i + C`)} \\

\end{align}
$$

`Expression 11` 이 말하는 것은 소프트맥스의 지수 함수를 계산할 때 어떤 정수를 더해도 결과는 바뀌지 않는다는 점입니다. 여기서 $C`$ 에 어떤 값을 대입해도 상관없지만, 오버플로우를 막을 목적으로 입력 신호 중 최댓값을 이용하는 것이 일반적입니다. 구체적인 예를 알아보겠습니다.

```python
>>> a = np.array([1010, 1000, 990])
>>> np.exp(a) / np.sum(np.exp(a))
array([nan, nan, nan])
>>> c = np.max(a)
>>> a - c
array([  0, -10, -20])
>>> np.exp(a-c) / np.sum(np.exp(a-c))
array([9.99954600e-01, 4.53978686e-05, 2.06106005e-09])
```

아무런 조치 없이 계산하면 nan 이 출력됩니다. 하지만 입력 신호 중 최댓값을 빼주면 올바르게 계산할 수 있습니다. 이를 바탕으로 함수를 다시 구현해보겠습니다.

```python
def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y
```

### Features of the Softmax Function

`softmax()` 함수를 사용하면 신경망의 출력은 다음과 같이 계산할 수 있습니다.

```python
>>> a = np.array([0.3, 2.9, 4.0])
>>> y = softmax(a)
>>> y
[ 0.01821127  0.24519181  0.73659691]
>>> np.sum(y)
1.0
```

보는바와 같이 소프트맥스 함수의 출려긍ㄴ 0 에서 1.0 사이의 실수 입니다. 즉, 소프트맥스 함수의 출력의 총합은 1입니다. 이 성질 덕분에 소프트맥스 함수의 출력을 *확률* 로 해석할 수 있습니다.

위 결과를 해석해보면 74 % 확률로 2 번째 클래스, 25 % 확률로 1 번째 클래스, 0 % 확률로 0 번째 클래스라는 결론을 낼 수 있습니다.

### To Determine the Number of Neurons in the Output Layer

출력층의 뉴런 수는 풀려는 문제아 맞게 적절히 정해야 합니다. 분류에서는 분류하고 싶은 클래스 수로 설정하는 것이 일반적입니다. 예를 들어 입력 이미지를 숫자 0 부터 9 중 하나로 분류하는 문제라면 `Example 23` 처럼 출력층의 뉴런을 10 개로 설정합니다.

> Example 23

![image](https://user-images.githubusercontent.com/44635266/75104886-9a57b380-5651-11ea-8162-4047605a7178.png)

`Example 23` 에서 출력층 뉴런은 위에서 부터 숫자 0, 1 ... 9 에 대응하며, 뉴런의 회색 농도에 따라 출력 값의 크기를 의미합니다.

## Handwriting Numerical Recognition

신경망의 구조를 배웠으니 실전 예를 적용해보겠습니다.

이미 학습된 매개변수를 사용하여 학습 과정은 생략하고, 추론 괒어만 구현하겠습니다. 이 추론 과정을 신경망의 **순전파(Forward Propagation)** 라고도 합니다.

### MNIST Data Set

사용할 예제는 MNIST 손글시 숫자 이미지 집합입니다. MNIST 는 기계 학습 분야에서 아주 유명한 데이터 셋입니다.

MNIST 데이터 셋은 0 부터 9 까지 숫자 이미지로 구성 됩니다. `Example 24` 처럼 훈련 이미지가 60,000 장 테스트 이미지가 10,000 장 있습니다. 일반적으로 이 이미지를 사용하여 모델을 학습하고 학습한 모델로 테스트 이미지들이 얼마나 정확한지를 분류합니다.

> Example 24

![image](https://user-images.githubusercontent.com/44635266/75104888-a0e62b00-5651-11ea-9ed5-40b30ff3139a.png)

아래 코드를 이용하면 쉽게 MNIST 데이터를 가져올것입니다. 예제에서는 keras 를 이용하여 가져오겠습니다.

MNIST 의 이미지 데이터는 28 X 28 회색조 이미지이며, 각 픽셀은 0 에서 255까지의 값을 취합니다.

먼저 Python 파일 위에 [dataset](https://github.com/WegraLee/deep-learning-from-scratch/tree/master/dataset) 디렉토리를 저장해 둡니다.

```python
import sys, os
sys.path.append(os.pardir)
from dataset.mnist import load_mnist

(x_train, t_train), (x_test, t_test) = mnist.load_data(flatten=True, normalize = False)

print(x_train.shape) # (60000, 784)
print(t_train.shape) # (60000,)
print(x_test.shape) # (10000, 784)
print(t_test.shape) # (10000,)
```

`normalize` 는 입력 이미지의 픽셀 값을 0.0 ~ 1.0 사이의 값으로 정규화 할지를 결정합니다.

데이터 확인 겸 MNIST 이미지를 불러보도록 하겠습니다. `flatten=True` 는 28 X 28 Nunmpy 배열을 784 개의 원소로 이루어진 1 차원 배열로 저장합니다.

```python
# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 부모 디렉터리의 파일을 가져올 수 있도록 설정
import numpy as np
from dataset.mnist import load_mnist
from PIL import Image


def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()

(x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)

img = x_train[0]
label = t_train[0]
print(label)  # 5

print(img.shape)  # (784,)
img = img.reshape(28, 28)  # 형상을 원래 이미지의 크기로 변형
print(img.shape)  # (28, 28)

img_show(img)
```

> Example 25

![image](https://user-images.githubusercontent.com/44635266/75104890-a80d3900-5651-11ea-91b4-d0e0c0b2561d.png)

여기서 `flatten=True` 로 설정하면 읽어온 이미지는 1 차원 Numpy 배열로 저장되는겁니다. 이미지를 표시할 때는 28 X 28 크기로 다시 변형하기 위해 `reshape()` 함수를 사용했습니다.

### Inference Processing of Neural Networks

이제 이 신경망을 구현해보겠ㅅ습니다. 은닉층은 총 2 개로, 첫 번재 은닉층에는 50 개의 뉴런을, 2 번째 은닉층에는 100 개의 뉴런을 배치하겠습니다. 이 뉴런의 개수는 임의로 정한 값입니다.

```python
def get_data():
    (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, flatten=True, one_hot_label=False)
    return x_test, t_test


def init_network():
    with open("sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    return network


def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return y
```

추론을 수행해보고 정확도 평가를 해보겠습니다.

```python
x, t = get_data()
network = init_network()
accuracy_cnt = 0
for i in range(len(x)):
    y = predict(network, x[i])
    p= np.argmax(y)
    if p == t[i]:
        accuracy_cnt += 1

print("Accuracy:" + str(float(accuracy_cnt) / len(x)))
```

먼저 MNIST 데이터 세승ㄹ 얻고 네트워크를 생성합니다. 이어서 for 문을 돌며 이미지 데이터를 꺼내 `predict()` 함수로 분류합니다.  `predict()` 함수는 각 레이블의 확률을 Numpy 배열로 반환합니다. 예를 들어 [0.1, 0.3 .....] 와 같은 배열이 반환되며, 이 이미지가 0 일 확률 1 일 확률 식으로 해석합니다. 그런다음 `np.argmax()` 함수로 가장 큰 원소의 인덱스를 구합니다. 이것이 바로 예측 결과입니다. 마지막으로 신경망이 예측한 답변과 정답 레이블을 비교하여 맞은 카운트를 세고 전체 이미지 숫자로 나눠 정확도를 구합니다. 

위 코드를 수행하면 *Accuracy:0.9352* 라 출력합니다. 올바르게 분류한 비율이 93.52 % 라는 뜻입니다.

위 예에서는 `normalize=True` 설정했습니다. 이 의미는 0 ~ 255 범위인 픽셀의 값을 0.0 ~ 1.0 범위로 변환합니다. 이처럼 데이터를 특정 범위로 변환하는 처리를 **정규화(Normalization)** 이라 합니다. 신경망의 입력 데이터에 특정 변환을 가하는 것을 **전처리(Pre-Processing)** 이라 합니다.

### Batch Processing

앞서 구현한 신경망의 각 층의 가중치 형상을 알아보겠습니다.

```python
>>> x, _ = get_data()
>>> network = init_network()
>>> W1, W2, W3 = network['W1'], network['W2'], network['W3']
>>>
>>> x.shape
(10000, 784)
>>> x[0].shape
(784, )
>>> W1.shape
(784, 50)
>>> W2.shape
(50, 100)
>>> W3.shape
(100, 10)
```

다차원 배열의 대응하는 차원의 원소수가 일치함을 확인할 수 있습니다. 그림으로 표현하면 `Example 26` 처럼 됩니다.

> Example 26

![image](https://user-images.githubusercontent.com/44635266/75104891-af344700-5651-11ea-8496-8e95945b7ba9.png)

이미지를 여러 장을 한꺼번에 입력하는 경우를 알아보겠습니다.

> Example 27

![image](https://user-images.githubusercontent.com/44635266/75104894-b65b5500-5651-11ea-9abb-258266922fb3.png)

100 장의 이미지를 하나로 묶은 입력 데이터를 **배치(batch)** 라 합니다. 배치가 곧 묶음이란 의미입니다.