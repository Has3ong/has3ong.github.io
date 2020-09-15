---
title : Machine Learning Convolutional Neural Network, CNN
tags :
- Pooling Layer
- Convolution Layer
- CNN
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch](https://github.com/WegraLee/deep-learning-from-scratch) 를 바탕으로 작성하였습니다.*

CNN 은 이미지 인식과 음성 인식 등 다양한 곳에서 사용됩니다.

## Overall Structure

CNN 에서는 새로은 계층이 등장합니다. **합성곱 계층(Convolutional Layer)** 와 **풀링 계층(Pooling Layer)** 이 새롭게 등장합니다.

지금까지 본 신경망은 인접하는 계층의 모든 뉴런과 결합되어 있습니다. 이를 **완전 연결(Fully-Connected)** 이라고 하며, 완전히 연결된 계층을 **Affine Layer** 이라는 이름으로 구현했습니다. 이 Affine Layer 를 사용하면 층이 5 개인 신경망은 `Example 1` 과 같이 구현할 수 있습니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/76160413-8772d200-616d-11ea-8488-4c9e3016f927.png)

`Example 1` 은 Affine Layer 뒤에 활성화 함수를 가지는 ReLU, Sigmoid 계층이 이어집니다.

CNN 의 구조는 `Example 2` 와 같습니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/76160418-8e99e000-616d-11ea-995b-bbd26fcfc85b.png)

CNN 에서는 새로운 *Conv* 과 *Pooling* 이 추가됩니다.

## Convolutional Layer

CNN 에서는 **패딩(padding)**, **스트라이드(stride)** 등 CNN 고유의 언어가 등장합니다. 또, 각 계층 사이에는 3 차원 데이터같이 입체적인 데이터가 흐른다는 점에서 완전연결 신경망과 다릅니다.

### Problems with the Fully Connected Layer

완전연결 계층의 문제점은 데이터의 형상이 무시된다는 사실입니다. 입력 데이터가 이미지인 경우 width, height, channel(color) 로 구성된 3차원 데이터입니다. 하지만 완전연결 계층에 입력할 때는 3 차원 데이터를 평평한 1 차원 데이터로 만들어줘야합니다.

이미지는 3 차원 형상이며, 이 형상에는 소중한 공간 데이터도 같이 담겨있습니다. 예를 들어, 공간적으로 가까운 픽셀은 값이 비슷하거나, RGB 의 각 채널은 서로 밀접하게 있거나 등, 의미를 가지는 패턴이 있습니다. 하지만 완전연결 계층은 형상을 무시하고 모든 입력 데이터를 동등한 뉴런으로 취급하여 형상에 담긴 정보를 살릴 수 없습니다.

하지만, 합성곱 계층은 형상을 유지합니다. 이미지도 3 차원 데이터로 입력받으며 3 차원 데이터로 출력합니다.

CNN 에서는 합성곱 계층의 입출력 데이터를 **특징 맵(Feature Map)** 이라고도 합니다. 합성곱 계층의 입력 데이터를 **입력 특징 맵(Input Feature Map)**, 출력 데이터를 **출력 특징 맵(Output Feature Map)** 이라고 합니다.

### Computation of Convolution

합성곱 계층에서의 **합성곱 연산** 을 처리합니다. 합성곱 연산은 이미지 처리에서 말하는 **필터 연산** 에 해당합니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/76160422-95285780-616d-11ea-95f1-822de6ba837c.png)

`Example 3` 과 같이 합성곱 연산은 입력 데이터에 필터를 적용합니다. 이 예에서 입력 데이터는 세로 - 가로 방향의 형상을 가졌고, 필터 역시 세로 - 가로 방향의 차원을 가집니다.

데이터와 필터의 형상을 (height, width) 로 표기하며, 이 예에서는 입력은 $(4, 4)$, 필터는 $(3, 3)$, 출력은 $(2, 2)$ 가 됩니다. 필터를 **커널** 이라고도 칭합니다.

`Example 4` 는 `Example 3` 에서 어떤 연산이 이뤄지는지 계산 순서를 나타낸 것입니다.

합성곱 연산은 **윈도우(window)** 를 일정 간격으로 이동해가며 입력 데이터에 적용합니다. 여기서 말하는 윈도우는 `Example 4` 의 회색 $3 \times 3$ 부분을 가리킵니다.

그림에서 보듯이 입력과 필터에서 대응하는 원소끼리 곱한 후 그 총합을 구합니다. 이 계산을 **단일 곱셈-누산(Fused Multiply-Add, FMA)** 라 합니다. 결과를 출력하여 해당 장소에 저장합니다. 이 과정을 모든 장소에 수행하면 합성곱 연산의 출력이 완성됩니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/76160429-9bb6cf00-616d-11ea-9f8a-a2826f9ae80f.png)

완전 연결 신경망에는 가중치 매개변수와 편향이 존재하는 데, CNN 에서는 필터의 매개변수가 그 동안의 가중치에 해당합니다. 그리고 CNN 에도 편향이 존재합니다. `Example 3` 은 필터를 적용하는 단계까지만 보여줬고, 편향까지 포함하면 `Example 5` 와 같은 흐름이 됩니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/76160434-a7a29100-616d-11ea-8ea4-293bd8d39b26.png)

`Example 5` 와 같이 편향은 필터를 적용한 후의 데이터에 더해집니다. 그리고 편향은 항상 하나만 존재합니다. 그 하나의 값은 필터를 적용한 모든 원소에 더해줍니다.

### Padding

합성곱 연산을 수행하기 전에 입력 데이터 주변을 특정 값으로 채우기도 합니다. 이를 **패딩(padding)** 이라 합니다. 합성곱 연산에서 주로 이용하는 기법입니다. `Example 6` 은 $(4, 4)$ 크기의 입력 데이터에 폭이 1 인 패딩을 적용한 모습입니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/76160439-affacc00-616d-11ea-8e24-9c511327e442.png)

`Example 6` 과 같이 처음에 크기가 $(4, 4)$ 인 입력 데이터에 패딩이 추가되어 $(6, 6)$ 이 됩니다. 이 입력에 $(3, 3)$ 크기의 필터를 걸면 $(4, 4)$ 크기의 출력 데이터가 생성됩니다.

> 패딩은 주로 출력 크기를 조정할 목적으로 사용합니다.

### Stride

필터를 적용하는 위치의 간격을 **스트라이드(Stride)** 라 합니다. `Example 7` 을 통해 스트라이드의 예를 알아보겠습니다. 스트라이드는 필터를 적용하는 간격을 지정합니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/76160442-b5581680-616d-11ea-84b6-ee10e442c737.png)

패딩, 스트라이드, 출력 크기를 수식화하여 표현해보겠습니다.

입력 크기를 $(H, W)$, 필터 크기를 $(FH, FW)$, 출력 크기를 $(OH, OW)$, 패딩을 $P$, 스트라이드를 $S$ 라 하면 출력 크기는 다음 식으로 계산됩니다.

> Expression 1

$$
OH = { H + 2P - FH \over S } + 1 \\
OW = { W + 2P - FW \over S } + 1
$$

이 식을 사용하여 `Example 6`, `Example 7` 의 예를 들어보겠습니다.

> Example 6 입력 : (4, 4), 패딩 : 1, 스트라이드 : 1, 필터 : (3, 3)

$$
OH = { 4 + 2 \cdot 1 - 3 \over 1 } + 1 = 4 \\
OW = { 4 + 2 \cdot 1 - 3 \over 1 } + 1 = 4
$$

> Example 7 입력 : (7, 7), 패딩 : 0, 스트라이드 : 2, 필터 : (3, 3)

$$
OH = { 7 + 2 \cdot 0 - 3 \over 2 } + 1 = 3 \\
OW = { 7 + 2 \cdot 0 - 3 \over 2 } + 1 = 3
$$

위 처럼 단순히 값을 대입하기만 하면 출력 크기를 구할 수 있습니다. 하지만, 식이 정수로 나눠떨어지는 값이어야 하는 점을 주의해야합니다.

### Convolution Arithmetic of Three-Dimensional Data

`Example 8` 은 3 차원 데이터의 합성곱 연산의 예입니다. 그리고 `Example 9` 는 계산 순서입니다. 2 차원일 때와 비교하면 길이 방향으로 측징 맵이 늘어났습니다.

채널 쪽으로 특징 맵이 여러 개 있다면 입력 데이터와 필터의 합성곱 연산을 채널마다 수행하고, 그 결과를 더해 하나의 출력을 얻습니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/76160457-c7d25000-616d-11ea-95a2-f42c93004a61.png)

> Example 9

![image](https://user-images.githubusercontent.com/44635266/76160461-cdc83100-616d-11ea-8004-f46faa753a51.png)

3 차원의 합성곱 연산에서 주의할 점은 입력 데이터의 채널 수와 필터의 채널 수가 같아야 한다는 것입니다.

### Think of Block

3 차원의 합성곱 연산은 데이터와 필터를 직육면체 블록이라 생각하면 쉽습니다. 블록은 `Example 10` 과 같이 3 차원 직육면체 입니다. 3 차원 데이터를 다차원 배열로 나타낼 때는 (Channel, Height, Width) 순서로 표현합니다.

데이터의 형상은 (C, H, W) 로 씁니다. 필터도 (C, FH, FW) 로 씁니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/76160463-d3257b80-616d-11ea-9794-e66884375926.png)

위 예에서 출력 데이터는 한 장의 특징 맵입니다. 한 장의 특징 맵을 다른 말로 하면 채널이 1 개인 특징 맵입니다. 합성곱 연산의 출력으로 다수의 채널을 내보내려면 필터를 다수 사용하는것입니다. `Example 11` 을 통해 알아보겠습니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/76160466-d9b3f300-616d-11ea-8d2a-f7d99f18b2cf.png)

필터를 FN 개 적용하면 출력 맵도 FN 개가 생성이 됩니다. 그리고 FN 개의 맵을 모으면 형상이 (FN, OH, OW) 인 블록이 완성됩니다. 이 블록을 다음 계층으로 넘기는게 CNN 의 처리 흐름입니다.

합섭ㅇ곱 연산에서는 필터의 수도 고려해야합니다. 그래서 필터의 가중치 데이터는 4 차원 데이터이며, (출력 채널 수, 입력 채널 수, 높이, 너비) 순으로 씁니다.

합성곱 연산에서도 편향이 사용합니다. `Example 12` 는 `Example 11` 에서 편향을 더한 모습입니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/76160469-de78a700-616d-11ea-82f4-294394493dce.png)

편향은 채널 하나에 값 하나씩으로 구성됩니다. 

### Batch Processing

신경망 처리에서는 입력 데이터를 한 덩어리로 묶어 배치로 처리했습니다.

합성곱 연산도 마찬가지로 배치 처리를 지원합니다. 그래서 각 계층을 흐르는 데이터의 차원을 하나 늘려 4 차원 데이터로 저장합니다. 데이터가 N 개일 때 `Example 12` 를 배치 처리하면 `Example 13` 처럼 됩니다.

> Example 13

![image](https://user-images.githubusercontent.com/44635266/76160476-e5071e80-616d-11ea-8001-214fd9186599.png)

배치 처리시 데이터 흐름을 보면 각 데이터의 선두에 배치용 차원을 추가합니다. 데이터는 4 차원 형상을 가진 채 각 계층을 타고 흐릅니다.

여기서 주의할 점은 신경망에 4 차원 데이터가 하나 흐를 때마다 데이터 N 개에 대한 합성곱 연산이 이뤄진다는 것입니다. 즉, N 회 분의 처리를 한 번에 수행합니다.

## Pooling Layer

풀링은 세로 $\cdot$ 가로 방향의 공간을 줄이는 연산입니다. 예를 들어 `Example 14` 와 같이 $2 \times 2$ 영역을 원소 하나로 집약하여 공간 크기를 줄입니다.

> Example 14

![image](https://user-images.githubusercontent.com/44635266/76160480-e9cbd280-616d-11ea-8fe7-c74ed42bb692.png)

위 그림은 $2 \times 2$ **최대 풀링(Max Pooling)** 을 스트라이드 2 로 처리하는 순서입니다. 최대 풀링은 최댓값을 구하는 연산입니다.

### Feature of Pooling Layer

풀링의 특징은 아래와 같습니다.

* 학습해야 할 매개변수가 없다
  * 풀링은 대상 영역에서 최댓값이나 평균을 취하는 명확한 처리이므로 학습할 것이 없다.
* 채널 수가 변하지 않는다.
  * 풀링 연산은 입력 데이터의 채널 수 그대로 출력 데이터로 보낸다. `Example 15` 처럼 채널마다 독립적으로 계산하기 때문입니다.

> Example 15

![image](https://user-images.githubusercontent.com/44635266/76160488-f05a4a00-616d-11ea-8f54-3a6edccf3924.png)

* 입력의 변화에 영향을 적게 받는다.
  * 입력 데이터가 조금 변해도 풀링의 값은 잘 변하지 않습니다. `Example 16` 을 참고하시면 됩니다.

> Example 16

![image](https://user-images.githubusercontent.com/44635266/76160495-f6502b00-616d-11ea-963b-ba1af592849a.png)

## To Implement of Convolution / Pooling Layer

### Four-Dimensional Array

CNN 에서 계층 사이를 흐르는 데이터는 4 차원입니다. 예를 들어 데이터 형상이 (10, 1, 28, 28) 를 구현하면 다음과 같습니다.

```python
>>> x = np.random.rand(10, 1, 28, 28)
>>> x.shape
(10, 1, 28, 28)
```

여기서 첫 번째 데이터에 접근하려면 `x[0]` 이라고 사용하면 됩니다.

```python
>>> x[0].shape
(1, 28, 28)
>>> x[1].shape
(1, 28, 28)
```

### Data deployment to im2col

합성곱 연산을 곧이곧대로 구현하려면 `for` 문을 겹겹히 써야합니다. 하지만 이 방법을 사용하면 성능이 떨어지는 단점이 있습니다. 그래서 `im2col` 을 이용하면 입력 데이터를 필터링하기 좋게 전개하는 함수입니다.

`Example 17` 은 3 차원 입력 데이터에 `im2col` 을 적용하여 2 차원 행렬로 바꾸는 예시입니다.

> Example 17

![image](https://user-images.githubusercontent.com/44635266/76160497-fcdea280-616d-11ea-8a50-64e6d0ed3500.png)

`im2col` 은 필터링하기 좋게 입력 데이터를 전개합니다. 구체적으로 `Example 18` 과 같이 입력 데이터에서 필터를 적용하는 영역을 한줄로 늘어놓습니다.

이 전개를 필터를 적용하는 모든 영역에서 수행하는게 `im2col` 입니다.

> Example 18

![image](https://user-images.githubusercontent.com/44635266/76160498-023bed00-616e-11ea-8a39-80b609387022.png)

`im2col` 로 입력 데이터를 전개한 다음에 합성곱 계층의 필터를 1 열로 전개하고, 두 행렬의 곱을 계산하면 됩니다. 이는 완전연결 계층의 Affine 과 비슷합니다.

> Example 19

![image](https://user-images.githubusercontent.com/44635266/76160501-0831ce00-616e-11ea-8624-9466ec05e51c.png)

`Example 19` 처럼 `im2col` 방식으로 출력한 결과는 2 차원 행렬입니다. CNN 은 데이터를 4 차원 배열로 저장하므로 2 차원인 출력 데이터를 4 차원으로 변형합니다.

### Implementing a Convolution layer

`im2col` 함수의 인터페이스는 아래와 같습니다.

```python
im2col(input_data, filter_h, filter_w, stride=1, pad=0)
```

* **input_data** - (데이터 수, 채널 수, 높이, 너비) 의 4 차원 배열로 이뤄진 입력 데이터
* **filter_h** - 필터의 높이
* **filtwr_w** - 필터의 너비
* **stride** - 스트라이드
* **pad** - 패딩

`im2col` 을 사용한 예를 보겠습니다.

```python
import sys, os
sys.path.append(os.pardir)
from common.util import im2col

x1 = np.random.rand(1, 3, 5, 7)
col1 = im2col(x1, 5, 5, 1, 0)

x2 = np.random.rand(10, 3, 7, 7)
col2 = im2col(x2, 5, 5, 1, 0)
```

이 `im2col` 을 이용해 합성곱 계층을 구현해보겠습니다. 전체 소스는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/common/layers.py) 에 있습니다.

```python
class Convolution:
    def __init__(self, W, b, stride=1, pad=0)
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad
    
    def forward(self, x):
        FN, C, FH, FW = self.W.shape
        N, C, H, W = x.shape
        out_h = int(1 + (H + 2*self.pad - FH) / self.stride)
        out_w = int(1 + (W + 2*self.pad - FW) / self.stride)

        col = im2col(x, FH, FW, self.stride, self.pad)
        col_W = self.W.reshape(FN, -1).T
        out = np.dot(col, col_W) + self.b

        out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)

        return out
```

합성곱 계층은 필터, 편향, 스트라이드, 패딩을 인수로 받아 초기화합니다.

필터를 전개하는 부분은 `Example 19` 와 같이 필터 블록을 1 줄로 펼칩니다. 즉 (10, 3, 5, 5) 형상을 한 다차원 배열에 `reshape(10, -1)` 을 호출하면 형상이 (10, 75) 인 배열로 만들어줍니다.

`forward` 구현의 마지막에서는 출력 데이터를 적절한 형상으로 바꿔줍니다. 이때 Numpy 의 `transpose` 함수를 사용하는데, 이는 다차원 배열의 축 순서를 바꿔줍니다. `Example 20` 과 같이 축의 순서를 변경해줍니다.

> Example 20

![image](https://user-images.githubusercontent.com/44635266/76160503-0c5deb80-616e-11ea-8728-ecd51381ac3e.png)

### Implementing a Pooling layer

풀링의 경우엔 채널 쪽이 독립적이라 합성곱 계층 때와 다릅니다. `Example 21` 과 같이 풀링 적용 영역을 채널마다 독립적으로 전개합니다.

> Example 21

![image](https://user-images.githubusercontent.com/44635266/76160507-1384f980-616e-11ea-86c4-44a9a35fed9d.png)

위와 같이 전개한 후, 행렬에서 행별 최댓값을 구하고 적절한 형상으로 바꿔줍니다.

> Example 22

![image](https://user-images.githubusercontent.com/44635266/76160511-1aac0780-616e-11ea-96c2-872ec90b2d73.png)

이상이 풀링 계층의 흐름입니다. 소스를 통해 보겠습니다. 소스는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/common/layers.py) 에 있습니다.

```python
class Pooling:
    def __init__(self, pool_h, pool_w, stride=1, pad=0):
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad
        
        self.x = None
        self.arg_max = None

    def forward(self, x):
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_h) / self.stride)
        out_w = int(1 + (W - self.pool_w) / self.stride)

        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
        col = col.reshape(-1, self.pool_h*self.pool_w)

        arg_max = np.argmax(col, axis=1)
        out = np.max(col, axis=1)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        self.x = x
        self.arg_max = arg_max

        return out
```

풀링은 아래 3 단계로 진행합니다.

1. 입력 데이터 전개
2. 행별 최댓값 구하기
3. 적절한 모양으로 성형

## Implementing a CNN

손글씨 숫자를 인식하는 CNN 을 구현해보겠습니다. `Example 23` 과 같이 CNN 을 구현하겠습니다.

> Example 23

![image](https://user-images.githubusercontent.com/44635266/76160514-24356f80-616e-11ea-8059-034f00c3fde5.png)

네트워크는 *Convolution - ReLU - Pooling - Affine - ReLu - Affine - Softmax* 순으로 흐릅니다.

전체 소스는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch07/simple_convnet.py) 에 있습니다.

```python
class SimpleConvNet:

    # conv - relu - pool - affine - relu - affine - softmax

    def __init__(self, input_dim=(1, 28, 28), 
                 conv_param={'filter_num':30, 'filter_size':5, 'pad':0, 'stride':1},
                 hidden_size=100, output_size=10, weight_init_std=0.01):
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1]
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))

        self.params = {}
        self.params['W1'] = weight_init_std * \
                            np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params['b1'] = np.zeros(filter_num)
        self.params['W2'] = weight_init_std * \
                            np.random.randn(pool_output_size, hidden_size)
        self.params['b2'] = np.zeros(hidden_size)
        self.params['W3'] = weight_init_std * \
                            np.random.randn(hidden_size, output_size)
        self.params['b3'] = np.zeros(output_size)

        self.layers = OrderedDict()
        self.layers['Conv1'] = Convolution(self.params['W1'], self.params['b1'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu1'] = Relu()
        self.layers['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Affine1'] = Affine(self.params['W2'], self.params['b2'])
        self.layers['Relu2'] = Relu()
        self.layers['Affine2'] = Affine(self.params['W3'], self.params['b3'])

        self.last_layer = SoftmaxWithLoss()
```

위 모델을 바탕으로 학습을 해보면 99 % 의 정확도가 출력되는걸 알 수 있습니다. 작은 네트워크로도 높은 정확도를 구현할 수 있습니다. 학습을 위한 코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch07/train_convnet.py) 에 있습니다.