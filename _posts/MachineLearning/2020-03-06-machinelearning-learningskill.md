---
title : Machine Learning Learning-Related Skill
tags :
- Optimizer
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch](https://github.com/WegraLee/deep-learning-from-scratch) 를 바탕으로 작성하였습니다.*

이번 포스트에서 다룰 주제는 가중치 매개변수의 최적값을 탐색하는 최적화 방법, 가중치 매개변수 초깃값, 하이퍼파라미터 설정 방법등등 입니다.

## Update Parameter

신경망 학습의 목적은 손실 함수의 값을 가능한 낮추는 매개변수를 찾는것입니다. 이러한 문제를 푸는 것을 **최적화(Optimization)** 이라고 합니다. 지금까지 최적의 매개변수 값을 찾는 단서로 매개변수의 기울기(미분)를 이용했습니다. 매개변수의 기울기를 구해 기울어진 방향으로 매개변수 값을 갱신하다 최적의 값에 다다릅니다. 이것이 **확률적 경사 하강법(SGD)** 이란 단순한 방법입니다.

SGD 는 단순하지만, SGD 보다 좋은 방법이 있습니다. SGD 의 단점을 알아본 후 SGD 와는 다른 최적화 기법을 알아보겠습니다.

### Stochastic Gradient Descent method

SGD 는 수식으로 다음과 같이 사용할 수 있습니다.

> Expression 1

$$
W \leftarrow W - \eta { \partial L \over \partial W}
$$

여기서 $W$ 는 갱신할 가중치 매개변수고 ${ \partial L \over \partial W}$ 는 $W$ 에 대한 손실 함수의 기울기입니다. $\eta$ 는 학습률을 의미하는데, 실제로는 0.01 이나 0.001 같은 값을 미리 정해서 사용합니다.

또한, $\leftarrow$ 는 우변의 값으로 좌변의 값을 갱신한다는 의미입니다. `Expression 1` 에서 보듯이 SGD 는 기울어진 방향으로 일정 거리만 가겠다는 단순한 방법입니다. SGD 를 Python 클래스로 구현하겠습니다.

```python
class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr
    
    def update(self, params, grads):
        for key in params.keys():
            params[key] -= self.lr * grads[key]
```

`lr` 은 Learning rate 를 의미합니다. `update(params, grads)` 메소드는 SGD 과정에서 반복해서 호출이 됩니다. 인수인 `params` 와 `grads` 는 딕셔너리 변수입니다. 각각 가중치 매개변수와 기울기를 저장합니다.

SGD 클래스를 사용하여 신경망 매개변수의 진행을 다음과 같이 수행할 수 있습니다.

```python
network = TwoLayerNet()
optimizer = SGD()

for i in range(10000)
    ...
    x_batch, t_batch = get_mini_batch(...)
    grads = network.gradient(x_batch, t_batch)
    params = network.params
    optimizer.update(params, grads)
    ...
```

`optimizer` 는 *최적화를 행하는 자* 라는 뜻의 단어입니다. 이 코드에서는 SGD 가 그 역할을 합니다.

### Disadvantages of SGD

SGD 는 단순하고 구현도 쉽지만, 문제에 따라서는 비효율적일 때가 있습니다. 이번에는 SGD 의 단점을 알아보고 함수의 최솟값을 구하는 문제를 생각해보겠습니다.

> Expression 2

$$
f(x, y) = { 1 \over 20}x^2 + y^2
$$

이 함수는 `Example 1` 과 같은 모습으로 되어있습니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/76047424-f30a4300-5fa5-11ea-8637-2e562ad3662b.png)

`Expression 2` 함수의 기울기를 그려보면 `Example 2` 처럼 됩니다. 이 기울기는 $y$ 축 방향은 크고 $x$ 축 방향은 작다는것이 특징입니다. 여기서 중요한 점은 `Expression 2` 의 식은 최솟값이 되는 장소는 $(x, y) = (0,0)$ 이지만, `Example 2` 가 보여주는 기울기는 대부분 $(0,0)$ 을 가리키지 않습니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/76047463-11703e80-5fa6-11ea-834c-f7ebb11d7664.png)

`Example 1` 에 함수 SGD 를 적용해 보겠습니다. 탐색을 시작하는 장소는 $(x, y) = (-7.0, 2.0)$ 으로 하겠습니다. 결과는 `Example 3` 처럼 됩니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/76047478-1a611000-5fa6-11ea-90e7-9e69bfcb6d71.png)

SGD 의 단점은 **비등방성(Anisotropy)** 함수에서는 탐색 경로가 비효율적이라는것입니다. 이런 SGD 의 단점을 개선해주는 모멘텀, AdaGrad, Adam 이라는 방법을 알아보겠습니다.

### Momentum

**모멘텀(Momentum)** 은 *운동량* 을 뜻하는 단어로 물리와 관계가 있습니다. 수식으로는 다음과 같이 사용할 수 있습니다.

> Expression 3

$$
v \leftarrow \alpha v - \eta { \partial L \over \partial W}
$$

> Expression 4

$$
W \leftarrow W + v
$$


SGD 처럼 $W$ 는 갱신할 가중치 매개변수, ${ \partial L \over \partial W}$ 에 대한 손실함수의 기울기, $\eta$ 는 학습률입니다. $v$ 는 물리에서 말하는 속도에 해당합니다. `Exmpression 3` 은 기울기 방향으로 힘을 받아 물체가 가속된다는 물리 법칙입니다.

모멘텀은 `Example 4` 와 같이 공이 그릇의 바닥을 구르는 듯한 움직임을 보여줍니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/76047483-2351e180-5fa6-11ea-98d0-eef99b72a3e8.png)

또 `Expression 3` 의 $\alpha v$ 항은 물체가 아무런 힘을 받지 않을 때 서서히 하강시키는 역할을 합니다. 물리에서의 지면 마찰이나 공기 저항에 해당합니다. 다음은 모멘텀의 구현입니다.

```python
class Momentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None
    
    def update(self, params, grads);
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_like(val)
```

인스턴스 변수 `v` 기 물체의 속도입니다. `v` 는 초기화 때는 아무 값도 담지 않고 `update()` 가 처음 호출될 때 매개변수와 같은 구조의 데이터를 딕셔너리 변수로 저장합니다. 나머지 부분은 `Expression 3` 과 `Expression 4` 를 간단히 코드로 옮긴것입니다.

이제 Momentum 을 이요앟여 `Expression 2` 를 최적화해보겠습니다. 결과는 `Example 5` 처럼 됩니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/76047564-6f9d2180-5fa6-11ea-8940-2140fce189cf.png)

### AdaGrad

신경망 학습에서는 학습률 값이 중요합니다. 이 학습률을 정하는 효과적 기술로 **학습률 감소(Learning Rate)** 가 있습니다. 이는 학습을 진행하면서 학습률을 점차 줄여가는 방법입니다. 처음에는 크게 학습하다가 조금씩 작게 학습한다는 얘기로 실제 신경망 학습에 자주 사용됩니다.

학습률을 서서히 낮추는 가장 간단한 방법은 매개변수 전체의 학습률 값을 일괄적으로 낮추는것입니다. 이를 발전시킨것이 AdaGrad 입니다.

AdaGrad 는 개별 매개변수에 적응적으로 학습률을 조정하면서 학습을 진행합니다. AdaGrad 갱신 방법은 수식으로는 다음과 같습니다.

> Expression 5

$$
h \leftarrow h + { \partial L \over \partial W} \odot { \partial L \over \partial W}
$$

> Expression 6

$$
W \leftarrow W - \eta { 1 \over \sqrt h} { \partial L \over \partial W}
$$

마찬가지로 $W$ 는 갱신할 가중치 매개변수, ${ \partial L \over \partial W }$ 은 $W$ 에 대한 손실함수의 기울기 $\eta$ 는 학습률입니다. 여기서는 새로운 변수 $h$ 가 있습니다. 

$h$ 는 기존 기울기 값을 제곱하여 계속 더해줍니다. ($\odot$ 은 행렬의 원소별 곱셈을 의미합니다.) 그리고 매개변수를 갱신할 때 ${ 1 \over \sqrt h }$ 을 곱해 학습률을 조정합니다.

매개변수의 원소중에서 많이 움직인 원소는 학습률이 낮아진다는 뜻인데, 다시 말해 학습률 감소가 매개변수의 원소마다 다르게 적용됨을 의미합니다.

AdaGrad 를 구현해보겠습니다.

```python
class AdaGrad:
    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None
    
    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            for key, val in params.items():
                self.h[key] = np.zeros_like(val)
            
        for key in params.keys():
            self.h[key] += grads[key] * grads[key]
            params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key]) + 1e-7)
```

여기서 주의할 점은 마지막에 `1e-7` 이라는 작은 값을 더하는 부분입니다. 이 작은 값은 `self.h[key]` 에 0 이 담겨 있다해도 0 으로 나누는 사태를 막아줍니다.

AdaGrad 를 사용하여 `Expression 2` 의 문제를 풀어보겠습니다. 결과는 `Example 6` 처럼 나옵니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/76047800-429d3e80-5fa7-11ea-9b47-5b9bbaa2ce5c.png)

점점 효율적으로 탐색하는걸 볼 수 있습니다.

### Adam

AdaGrad 와 Momentum 을 융합한 기법이 Adam 이라고 보시면됩니다.

Adam 을 사용하면 `Example 7` 과 같습니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/76047827-4cbf3d00-5fa7-11ea-90d8-874278aa1bdd.png)

### Which Update Method will be Used?

아래는 지금까지 살펴본 4 개의 기법을 비교해본것입니다. 소스코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch06/optimizer_compare_naive.py) 에 있습니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/76047842-52b51e00-5fa7-11ea-803b-5eca657dfcd7.png)

### Comparing the Update Method with MNIST Datasets

각각의 학습 기법에 따른 학습 진도를 그래프로 비교해보겠습니다.

> Example 9 

![image](https://user-images.githubusercontent.com/44635266/76047854-59dc2c00-5fa7-11ea-8326-f87aa661d3f9.png)

## Weight Initial Value

### When the initial value is set to 0

오버피팅을 억제해 범용 성능을 높이는 **가중치 감소(Weight decay)** 기법을 알아보겠습니다. 이 기법은 가중치 매개변수의 값이 작아지도록 학습하는 방법입니다. 가중치 값을 작게 하여 오버피팅이 일어나지 않게 하는것입니다.

초기값을 작게 시작하는게 정공법이긴 합니다. 하지만 가중치의 초깃값을 모두 0 으로 설정하면 학습이 올바르게 이루어지지 않습니다.

왜냐하면, 오차역전파법에서 모든 가중치의 값이 똑같이 갱신되기 대문입니다. 그래서 가중치 들은 같은 초깃값에서 시작하고 갱신을 거쳐도 여전히 같은 값을 유지하기 때문에 가중치를 여러개 가지는 의미가 사라집니다.

그래서 초깃값을 무작위로 설정하는게 좋습니다.

### Distribution of Activation Value of Hidden Layer

은닉층의 활성화 값의 분포를 관찰하면 중요한 정보를 얻을 수 있습니다. 가중치의 초깃값에 따라 은닉층 활성화 값들이 어떻게 변화하는지 알아보겠습니다.

활성화 함수로 Sigmoid 함수를 사용하는 5 층 신경망에 무작위로 생성한 입력 데이터를 흘리며 각 층의 활성화값 분포를 히스토그램으로 그려보겠습니다.

전체 소스코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch06/weight_init_activation_histogram.py) 에 있습니다.

```python
import numpy as np
import matplotlib.pyplot as plt

input_data = np.random.randn(1000, 100) 
node_num = 100  
hidden_layer_size = 5
activations = {} 

x = input_data

for i in range(hidden_layer_size):
    if i != 0:
        x = activations[i-1]

    w = np.random.randn(node_num, node_num) * 1
    # w = np.random.randn(node_num, node_num) * 0.01
    # w = np.random.randn(node_num, node_num) * np.sqrt(1.0 / node_num)
    # w = np.random.randn(node_num, node_num) * np.sqrt(2.0 / node_num)
    a = np.dot(x, w)

    z = sigmoid(a)
    # z = ReLU(a)
    # z = tanh(a)

    activations[i] = z
```

위 코드를 각각 주석문을 바꿔보면서 실행을 하면 다음과 같은 히스토그램을 얻을 수 있습니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/76047860-606aa380-5fa7-11ea-872f-73c1a6b686e8.png)

각 층의 활성화 값들이 0 과 1 에 치우쳐 분포하는것을 볼 수 있습니다. 시그모이드 함수는 출력이 0 에 가까워지면 미분은 0 에 다가갑니다. 그래서 데이터가 0 과 1에 치우쳐 분포하게 되면 역전파의 기울기 값이 점점 작아지다 사라집니다.

이것이 **기울기 손실(Gradient Vanishing)** 이라고 알려진 문제입니다. 층을 깊게 하는 딥러닝에서는 기울기 소실은 심각한 문제가 될 수 있습니다.

가중치의 표준편차를 0.01 로 바꿔 같은 실험을 반복해보겠습니다. 위 코드에서 가중치 초깃값 설정 부분을 다음과 같이 바꾸면 됩니다.

```python
w = np.random.randn(node_num, node_num) * 0.01
```

표준 편차를 0.01 로 한 정규본프의 경우 각 층의 활성화 값 분포는 `Example 11` 처럼 됩니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/76047865-66f91b00-5fa7-11ea-93cb-fbf72a92feab.png)

0.5 부근에 값이 집중되어 있어 기울기 소실 문제는 일어나지 않습니다. 하지만 값들이 치우쳤다는 것은 표현력 관점에서는 문제가 있습니다. 같은 값을 출력하므로, 뉴런을 여러개 둔 의미가 없다는 뜻입니다. 그래서 활성화 값들이 치우치면 **표현력을 제한한다** 라는 문제가 발생합니다.

*Xavier Glorot* 와 *Yoshua Bengio* 논문에서 권장하는 초기값인 **Xavier 초기값** 을 사용해보겠습니다.

이 논문은 각 층의 활성화값들을 광범위하게 분포시킬 목적으로 가중치의 적절한 분포를 찾고자 했습니다. 그리고 앞 계층의 노드가 $n$ 개 라면 표준편차가 ${ 1 \over \sqrt n }$ 인 분포를 사용하면 된다는 결론을 도출했습니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/76047870-6d879280-5fa7-11ea-8b50-40408a870470.png)

Xavier 초깃값으로 사용해보겠습니다.

```python
node_num = 100
w = np.random.randn(node_num, node_num) / np.sqrt(node_num)
```

> Example 13

![image](https://user-images.githubusercontent.com/44635266/76047879-75473700-5fa7-11ea-91d0-282ae27593ac.png)

Xavier 초기값을 사용하면 층이 깊어질수록 형태가 일그러지기는 하지만, 확실히 넓게 분포되있는것을 알 수 있어 효율적인 학습이 이뤄질수 있다는것을 알 수 있습니다.

### Initial Weight Value When Using ReLU

Xavier 초기값은 호라성화 함수가 선형인 것을 전제로 이끈 결과입니다. `sigmoid` 함수와 `tanh` 함수는 좌우 대칭이라 중앙 부근이 선형인 함수로 볼 수 있습니다. 그래서 `Xavier` 초기 값이 적당합니다.

반면 ReLU 함수는 ReLU 에 특화된 초기값을 사용하라고 권장합니다. 이 특화된 초기값을 찾아낸 *Kaiming He* 의 이름을 따 **He 초깃값** 이라고 합니다.

He 초깃값은 앞 계층의 노드가 $n$ 개 일 때, 표준편차가 $\sqrt { 2 \over n}$ 인 정규분포를 사용합니다. ReLU 는 음의 영역이 0 이라서 더 넓게 분포시키기 위해 2 배의 계수가 필요하다고 해석할 수 있습니다.

ReLU 를 이용한 경우의 활성화 값 분포를 보겠습니다. `Example 14` 는 표준편차가 0.01 인 정규분포, Xavier 초깃값, He 초깃값일 때의 실험 결과를 차례대로 보여줍니다.

> Example 14 
 
![image](https://user-images.githubusercontent.com/44635266/76047886-7b3d1800-5fa7-11ea-8f0b-e446f5d2102a.png)

결과를 보면 `std = 0.01` 일 때의 각 층의 활성화 값들은 아주 작습니다. 신경망에 아주 작은 데이터가 흐른다는 것은 역전파 때의 가중치의 기울기 역시 작아진다는 의미입니다. 이는 중요한 문제이며, 실제로는 학습이 거의 이뤄지지 않을겁니다.

Xavier 초깃값 결과를 보면 층이 깊어지면서 치우침이 조금씩 커져서 학습할 때 기울기 소실 문제를 일으킵니다.

마지막 He 초깃값은 모든 층에서 균일하게 분포되어 역전파 때도 적절한 값이 나올것으로 기대할 수 있습니다.

### Comparison of Initial Values in MNIST Data Sets

실제 데이터를 가지고 가중치의 초깃값이 학습에 얼마나 영향을 미치는지 보겠습니다. 소스 코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch06/weight_init_compare.py) 에 있습니다.

> Example 15

![image](https://user-images.githubusercontent.com/44635266/76047897-8132f900-5fa7-11ea-9152-207194f7d6a6.png)

이 실험은 층별 뉴런 수가 100 개인 5층 신경망에서 활성화 함수로 ReLU 로 사용했습니다.

## Batch Normalization

각 층의 활성화값 분포를 관찰하며, 가중치의 초깃값을 적절히 설정하면 각 층의 활성화값 분포가 적당히 퍼지면서 학습이 원할하게 수행됨을 배웠습니다.

여기서 각 층이 활성화를 적당히 퍼뜨리도록 강제하면 어떻게 될까요. 이런 질문에서 출발한 아이디어가 **배치 정규화(BAtch Normalization)** 입니다.

### Batch Normalization Algorithm

배치 정규화가 주목받는 이유는 아래와 같습니다.

* 학습을 빨리 진행할 수 있다.
* 초깃값에 크게 의존하지 않는다.
* 오버피팅을 억제한다.

`Example 16` 과 같이 데이터 분포를 정규화하는 **배치 정규화 계층** 을 신경망에 삽입해보겠습니다.

> Example 16

![image](https://user-images.githubusercontent.com/44635266/76047903-8728da00-5fa7-11ea-9bb6-d24554db571a.png)

배치 정규화는 이름과 같이 학습 시 미니 배치를 단위로 정규화합니다. 구체적으로는 데이터 분포가 평균이 0, 분산이 1 이 되도록 정규화 합니다. 수식으로는 다음과 같습니다.

> Expression 7

$$
\begin{align}
\mu_B \leftarrow { 1 \over m }\sum^m_{i=1}x_i \\
\sigma^2_B \leftarrow { 1 \over m }\sum^m_{i=1}(x_i - \mu_B)^2 \\
\hat x_i \leftarrow { x_i - \mu_B \over \sqrt{\sigma^2_B + \epsilon}}
\end{align}
$$

위 식에서는 미니배치 $B = {x_1, x_2, .... x_m}$ 이라는 $m$ 개의 입력 데이터의 집합에 대해 평균 $\mu_B$ 와 분산 $\sigma^2_B$ 를 구합니다. 그리고 입력 데이터를 평균이 0, 분산이 1 이 되게 정규화합니다. 그리고 `Expression 7` 에서 $\epsilon$ 기호는 작은 값으로, 0 으로 나누는 사태를 방지합니다.

`Expression 7`은 단순히 미니배치 입력데이터를 평균 0, 분산 1인 데이터 ${\hat x_1, \hat x_2, ... \hat x_m}$ 으로 변환하는 일을 합니다. 이 처리를 활성화 함수의 앞에 삽입함으로써 데이터 분포가 덜 치우치게 할 수 있습니다.

배치 정규화 계층마다 이 정규화된 데이터에 고유한 확대와 이동 변환을 수행합니다. 수식으로는 다음과 같습니다.

> Expression 8

$$
y_i \leftarrow \gamma \hat x_i + \beta
$$

이 식에서 $\gamma$ 가 확대를, $\beta$ 가 이동을 담당합니다. 두 값은 처음에는 $\gamma=1, \beta=0$ 부터 시작하고 학습하면서 적합한 값으로 조정해갑니다.

이상이 배치 정규화의 알고리즘입니다. 이 알고리즘이 신경망에서 순전파 때 적용됩니다. 이를 계산 그래프로 나타내면 아래와같습니다.

> Example 17

![image](https://user-images.githubusercontent.com/44635266/76047910-8bed8e00-5fa7-11ea-8de2-65f2f2bb90f9.png)

### Effect of Batch Normalization

MNIST 데이터를 이용하여 배치 정규화 계층을 사용한 실험을 해보겠스빈다. 우선 사용할 때와 사용하지 않을 때의 학습 진도를 보겠습니다.

> Example 18

![image](https://user-images.githubusercontent.com/44635266/76047920-93149c00-5fa7-11ea-942a-749b6f304f44.png)

그래프를 보면 배치 정규화가 학습을 빨리 진전시키는것을 볼 수 있습니다. 계속해서 초깃값 분포를 다양하게 줘가며 학습 진행이 어떻게 달라지는지 보겠습니다. `Example 19` 는 가중치 초깃값의 표준편차를 다양하게 바꿔가며 학습 경과를 관찰한 그래프입니다.

> Example 19

![image](https://user-images.githubusercontent.com/44635266/76047934-9c056d80-5fa7-11ea-8153-c7392f278e20.png)

## For Correct Learning

기계학습에서는 오버피팅이 문제가 되는 일이 많습니다. 오버피팅이란 신경망이 훈련 데이터에만 지나치게 적응되어 그 외의 데이터에는 제대로 대응하지 못한 상태입니다.

### Overfitting

오버피팅은 주로 다음의 2 경우에 일어납니다.

* 매개변수가 많고 표현력이 높은 모델
* 훈련 데이터가 적음

MNIST 데이터를 60,000 개에서 300 개만 사용하고 7 층 네트워크를 사용하여 네트워크의 복작성을 높여서 오버피팅을 일으켜보겠습니다. 각층의 뉴런은 100 개 활성화 함수는 ReLU 를 사용하겠습니다.

전체 소스코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch06/overfit_weight_decay.py) 에 있습니다.

> Example 20

![image](https://user-images.githubusercontent.com/44635266/76047953-aa538980-5fa7-11ea-9394-c9b8057f6653.png)

훈련 데이터를 사용하여 측정한 정확도는 100 에포치를 지나는 무렵부터 거의 100% 입니다. 하지만 시험 데이터에 대해서는 큰 차이를 보입니다. 이처럼 정확도가 크게 벌어지는 것은 훈련 데이터에만 **적응(fitting)** 해버린 결과입니다.

### Weight Decay

오버피팅 억제용으로 예로부터 많이해온 방법 중 하나는 **가중치 감소(Weight Decay)** 라는 것이 있습니다. 이는 학습 과정에서 큰 가중치에 대해서는 그에 상응하는 큰 페널티를 부과하여 오버피팅을 억제하는 방법입니다.

신경망 학습의 목적은 손실 함수의 값을 줄이는 것입니다. 예를 들어 가중치의 제곱 노름을 손실 함수에 더합니다. 그러면 가중치가 커지는 것을 억제할 수 있습니다.

가중치 $W$ 라 하면 L2 노름에 따른 가중치 감소는 ${1 \over 2}\lambda W^2$ 이 되고, 이 값을 손실 함수에 더합니다. 여기서 $\lambda$ 람다는 정규화의 세기를 조절하는 하이퍼파라미터입니다. $\lambda$ 를 크게 설정할 수록 큰 가중치에대한 페널티가 커집니다.

또한, ${1 \over 2}\lambda W^2$ 의 앞쪽 ${1 \over 2}$ 은 ${1 \over 2}\lambda W^2$ 의 미분 결과인 $\lambda W$ 를 조정하는 역할의 상수입니다.

가중치 감소는 모든 가중치 각각의 손실 함수에 ${1 \over 2}\lambda W^2$ 를 더합니다. 따라서 가중치의 기울기를 구하는 계산에서 그 동안의 오차역전파법에 따른 결과에 정규화 항을 미분한 $\lambda W$ 를 더합니다.

$\lambda = 0.1$ 로 가중치 감소를 적용하고 실험을 해보겠습니다. 전체 소스코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/common/multi_layer_net.py)

> Example 21

![image](https://user-images.githubusercontent.com/44635266/76047997-cb1bdf00-5fa7-11ea-8b9d-a8702d6d2025.png)

여전히 데이터에 대한 정확도 차이가 있지만 `Example 20` 과 비교하면 차이가 줄어들은걸 확인할 수 있습니다.

### Dropout

신경망 모델이 복잡해지면 가중치 감소만으로 대응하기 어려워 집니다. 이럴때는 **드롭아웃(Dropout)** 이란 기법을 사용합니다.

드롭아웃은 뉴런을 임의로 삭제하면서 학습하는 방법입니다. 훈련 때 은닉층의 뉴런을 무작위로 골라 삭제합니다. 삭제된 뉴런은 `Example 22` 와 같이 신호를 전달하지 않게됩니다.

훈련때는 데이터를 흘릴 때마다 삭제할 뉴런을 무작위로 선택하고, 시험 때는 모든 뉴런에 신호를  전달합니다. 단, 시험 때는 각 뉴런의 출력에 훈련 때 삭제 안 한 비율을 곱하여 출력합니다.

> Example 22

![image](https://user-images.githubusercontent.com/44635266/76048007-d40cb080-5fa7-11ea-9c10-3106745b4067.png)

드롭아웃을 구현해보겠습니다. 순전파를 담당하는 `forward` 메소드는 훈련 때 `(train_flg = True)` 이지만 잘 계산해두면 시험 때는 단순히 데이터를 흘리기만 하면 됩니다.

```python
class Dropout:
    def __init__(self, dropout_ratio=0.5):
        self.dropout_ratio = droup_ratio
        self.mask = None

    def forward(self, x, train_flg=True):
        if train_flg:
            self.mask = np.random.rand(*x.shape) > self.dropout_ratio
            return x * self.mask
        else:
            return x * (1.0 - self.droup_ratio)
    
    def backward(self, dout):
        return dout * self.mask
```

여기서 핵심은 훈련 시에는 순전파 때마다 `self.mask` 에 삭제할 뉴런을 `False` 로 표시하는겁니다. `self.mask` 는 `x` 와 형상이 같은 같ㅌ은 배열을 무작위로 생성하고, 그 값이 `dropout_ratio` 보다 큰 원소만 `True` 로 설정합니다.

역전파 때의 동작은 `ReLU` 와 같습니다. 즉, 순전파 때 신호를 통과시키는 뉴런은 역전파 때도 신호를 그대로 통과시키고, 순전파 때 통과시키지 않은 뉴런은 역전파 때도 신호를 차단합니다.

그럼 드롭아웃의 효과를 MNIST 데이터셋으로 확인하겠습니다. 소스 코드는 [Github]() 에 있습닌다.

결과는 `Example 23` 에 있습니다.

> Example 23

![image](https://user-images.githubusercontent.com/44635266/76048021-e2f36300-5fa7-11ea-9a98-bae2059dc1f5.png)

## Find the Appropriate Hyperparameter Value

하이퍼파라미터는 각 층의 뉴런 수, 배치 크기, 매개변수 갱신 시의 학습률과 가중치 감소 등등 입니다.

### Validation Data

보통 훈련 데이터로 학습을 진행하고, 시험 데이터로 범용 성능을 평가했습니다.

하이퍼파라미터를 조정할 때는 하이퍼파라미터 전용 확인 데이터가 필요합니다. 하이퍼파라미터 조정용 데이터를 일반적으로 **검증 데이터(Validation Data)** 라고 부릅니다. 하이퍼파라미터의 적절성을 평가하는 데이터입니다.

> * 훈련 데이터 : 매개변수 학습
> * 검증 데이터 : 하이퍼파라미터 성능 평가
> * 시험 데이터  : 신경망의 범용 성능 평가

MNIST 데이터셋에서 검증 데이터를 얻는 가장 간단한 방법은 훈련 데이터 중 20 % 정도를 검증 데이터로 먼저 분리하는 것입니다.

코드로는 아래와 같습니다.

```python
(x_train, t_train), (x_test, t_test) = load_mnist()

x_train, t_train = shufffle_dataset(x_train, t_train)

validation_rate = 0.20
validation_num = int(x_train.shape[0] * validation_rate)

x_val = x_train[:validation_num]
t_val = t_train[:validation_num]
x_train = x_train[validation_num:]
t_train = t_train[validation_num:]
```

### Hyperparameter Optimization

하이퍼파라미터를 최적화할 때의 핵심은 하이퍼파라미터의 최적 값이 존재하는 범위를 조금씩 줄여간다는 것입니다. 범위를 줄이면서 대략적인 범위를 설정하고 그 범위내에서 무작위로 하이퍼파라미터 값을 골라낸 후, 그 값으로 정확도를 평가합니다. 정확도를 잘 살피면서 이 작업을 여러 번 반복하는게 최적 값의 범위를 좁히는것입니다.

하이퍼파라미터를 최적화할 때는 딥러닝 학습에는 오랜 시간이 걸린다는 점을 기억해야합니다.

하이퍼파라미터 값의 최적화는 아래와 같이 진행됩니다.

* 0 단계
  * 하이퍼파라미터 값의 범위를 설정
* 1 단계
  * 설정된 범위에서 하이퍼파라미터 값을 무작위로 추출
* 2 단계
  * 1 단계에서 샘플링한 하이퍼파라미터 값을 사용하여 학습하고, 검증 데이터로 정확도를 평가
* 3 단계
  * 1 단계와 2 단계를 특정 횟수 반복하며, 그 정확도의 결과를 보고 하이퍼파라미터의 범위를 좁힌다.

### Implementation of Hyperparameter Optimization

하이퍼파라미터의 검증은 그 값을 $0.001 ~ 1.000(10^{-3} \sim 10^3)$ 사이 같은 로그 스케일 범위에서 무작위로 추출해 수행합니다. 이를 Python 코드로는 `10 ** np.random.uniform(-3, 3)` 처럼 작성할 수 있습니다.

위 예에서는 가중치 감소 계수를 $10^{-8} \sim 10^{-4}$, 학습률은 $10^{-6} \sim 10^{-2}$ 범위부터 시작합니다. 하이어파라미터 무작위 추출 코드는 다음과 같이 쓸 수 있습니다.

```python
weight_decay = 10 ** np.random.uniform(-8, -4)
lr = 10 ** np.random.uniform(-6, -2)
```

결과를 보겠습니다. `Example 24` 에 실선은 검증 데이터에 대한 정확도, 점선은 훈련 데이터에 대한 정확도 입니다.

> Example 24

![image](https://user-images.githubusercontent.com/44635266/76048038-ea1a7100-5fa7-11ea-8a95-3256d87c096b.png)

