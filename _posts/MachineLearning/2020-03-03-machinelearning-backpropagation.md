---
title : Machine Learning Backpropagation
tags :
- Sigmoid
- ReLu
- Softmax
- Affine
- Backpropagation
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch](https://github.com/WegraLee/deep-learning-from-scratch) 를 바탕으로 작성하였습니다.*

기존에는 가중치 매개변수의 기울기는 수치 미분을 사용했습니다. 하지만, 수치 미분은 단순하고 구현하기 쉽지만 계산 시간이 오래걸린다는 단점이 있습니다. **오차역전파법(Backpropagation)** 을 이용하면 가중치 매개변수의 기울기를 효율적으로 계산할 수 있습니다.

## Computational Graph

**계산 그래프(Computational Graph)** 는 계산 과정을 그래프로 나타낸 것입니다. 여기서 그래프는 복수의 **노드(Node)** 와 **엣지(Edge)** 로 표현됩니다.

### Work Out a Computation Graph

> 문제 1 : 슈퍼에서 1 개에 100 원인 사과 2 개를 구매했습니다. 이때 지불 금액을 구하세요. 단, 소비세가 10% 부과됩니다.

계산 그래프는 과정을 노드와 화살표로 표현합니다. 노드는 원(ㅇ) 으로 표기하고 안에 연산 내용을 적습니다. 계산 결과를 화살표 위에 적어 각 노드의 계산 결과가 왼쪽에서 오른쪽으로 전해지게 합니다. 문제 1 을 계산 그래프로 풀면 `Example 1` 이 됩니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/75774920-53299b00-5d94-11ea-8136-f0f758930932.png)

위 그림을 `Example 2` 처럼 원 밖에 표기할 수 있습니다.

> Example 2 

![image](https://user-images.githubusercontent.com/44635266/75774949-5c1a6c80-5d94-11ea-8417-f4992624f832.png)

다음 문제를 보겠습니다.

> 문제 2 : 슈퍼에서 사과를 2 개, 귤을 3 개 샀습니다. 사과는 1 개에 100 원, 귤은 1 개 150 원입니다. 소비세가 10% 일 때 지불 금액을 구하세요.

정답을 알아보겠습니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/75774969-663c6b00-5d94-11ea-8737-21dd34db0a8b.png)

계산 그래프를 이용한 문제풀이는 다음 흐름으로 진행합니다.

1. 계산 그래프를 구성한다.
2. 그래프에서 계산을 왼쪽에서 오른쪽으로 진행한다.

여기서 2 번째 *계산을 왼쪽에서 오른족으로 진행* 하는 단계를 **순전파(Foreward Propagation)** 이라고 합니다. 그리고 순전파의 반대를 **역전파(Backward Propogation)** 라고 합니다. 역전파는 이후 미분을 계산할 때 중요한 역할을 합니다.

### Local Computation

계산 그래프의 특징은 **국소적 계산** 을 전파함으로 최종 결과를 얻는다는 점에 있습니다.

> 국소적 계산 : 현재 계산이 이전 계산이나 다음 계산의 영향을 받지 않는다.

국소적 계산을 예를 들어보겠습니다. 슈퍼에서 사과 2 개를 포함한 여러 식품을 구입하는 경우를 알아보겠습니다. `Example 4` 처럼 계산 그래프로 나타낼 수 있습니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/75774990-6fc5d300-5d94-11ea-9146-0d0e58acd1ce.png)

각 노드는 자신과 관련된 계산 외에는 아무것도 신경 쓸 게 없습니다. 이처럼 계산 그래프는 국소적 계산에 집중합니다.

### Advantages of Computation Graphs

계산그래프의 가장 큰 이점은 전체가 아무리 복잡해도 각 노드에서는 단순한 계산에 집중하여 문제를 단순화 시킬 수 있습니다. 실제 계산 그래프를 사용하는 가장 큰 이유는 역전파를 통해 미분을 효율적으로 계산할 수 있는 점에 있습니다.

계산 그래프의 역전파를 설명하기 위해 `문제 1` 을 다시 살펴보겠습니다. `문제 1` 은 사과를 2개 사서 소비세를 포함한 최종 금액을 구하는것이였습니다.

여기서 가령 사과 가격이 오르면 최종 금액에 어떤 영향을 끼치는지 알고싶다고 합시다. 이는 *사과 가격에 대한 지불 금액의 미분* 을 구하는 문제입니다.

기호로 나타내면 사과 값을 $x$ 지불 금액을 $L$ 이라 했을 때 ${ \partial L \over \partial x }$ 을 구하는 것입니다. 이 미분 값은 사과 값이 올랐을 때 지불 금액이 얼마나 증가하느냐를 표시한 것입니다.

`Example 5` 처럼 계싼 그래프 상의 역전파에 의해서 미분을 구할 수 있습니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/75775011-78b6a480-5d94-11ea-88ca-c94b02eb2f8d.png)

역전파는 오른쪽에서 왼쪽으로 *1 -> 1.1 -> 2.2* 순으로 미분 값을 전달합니다. 이 결과로부터 *사과 가겨에 대한 지불 금액의 미분 값* 은 **2.2** 라 할 수 있습니다. 사과가 1원 오르면 최종 금액은 2.2 원 오른다는 뜻입니다.

## Chain Rule

위에서 살펴본 국소적 미분을 전달하는 원리가 **연쇄법칙(Chain Rule)** 에 따른 것입니다.

### Backward Propagation of Computation Graph

계산그래프를 사용한 역전파의 예를 하나 살펴보겠습니다. $y = f(x)$ 라는 계산의 역전파는 `Example 6` 과 같습니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/75775029-810edf80-5d94-11ea-8652-0022602a9474.png)

`Example 6`  과 같이 역전파의 계산 절차는 신호 $E$ 에 노드의 국소적 미분 $({ \partial y \over \partial x})$ 을 곱훈하 다음 노드로 전달하는 것입니다. 여기서 말하는 국소적 미분은 순전파 때의 $y = f(x)$ 계산의 미분을 구하는 것이며, 이는 $x$ 에 대한 $y$ 의 미분 $({ \partial y \over \partial x})$ 을 구한다는 의미 입니다.

가령 $y = f(x) = x^2$ 이라면 ${ \partial y \over \partial x} = 2x$ 가 됩니다. 이 국소적인 미분을 상류에서 전달된 값에 곱해 앞쪽 노드로 전달하는 것입니다.

이것이 역전파의 계산 순서인데, 이러한 방식을 따르면 목표로 하는 미분 값을 효율적으로 구할 수 있다는 것이 이 전파의 핵심입니다. 왜 이런 일이 가능한지 연쇄법칙의 원리로 설명하겠습니다.

### What is a Chain Rule ?

연쇄법칙을 설명하기 위해선 합성 함수부터 시작해야 합니다. **합성 함수** 란 여러 함수로 구성된 함수입니다. 예를 들어 $z = (x + y)^2$ 이라는 식은 `Expression 1` 처럼 두 개의 식으로 구성됩니다.

> Expression 1

$$
z = t^2 \\
t = x + y
$$

연쇄법칙은 합성 함수의 미분에 대한 성질이며, 다음과 같이 정의됩니다.

> 합성 함수의 미분은 합성 함수를 구성하는 각 함수의 미분의 곱으로 나타낼 수 있습니다.

이것이 연쇄법칙의 원리입니다. `Expression 1` 을 예로 설명하면 ${ \partial z \over \partial x}$ ($x$ 에 대한 $z$의 미분) 은 ${ \partial z \over \partial t}$ ($t$ 에 대한 $z$ 의 미분) 과 ${ \partial t \over \partial x}$ ($x$ 에 대한 $t$ 의 미분) 의 곱으로 나타낼 수 있습니다. 수식으로는 `Expression 2` 처럼 쓸 수 있습니다.

> Expression 2

$$
{ \partial z \over \partial x} = { \partial z \over \partial t} { \partial t \over \partial x}
$$

이 식은 아래와 같이 $\partial t$ 를 지울 수 있습니다. 

$$
{ \partial z \over \partial x} = { \partial z \over \partial x}
$$

연쇄 법칙을 써서 `Expression 2` 의 미분 ${ \partial z \over \partial x}$ 를 구해보겠습니다. 먼저 `Expression 1` 의 편미분을 구합니다.

> Expression 3

$$
{ \partial z \over \partial t } = 2t \\
{ \partial t \over \partial x } = 1
$$

`Expression 3` 과 같이 ${ \partial t \over \partial x}$ 는 1 입니다. 이는 미분 공식에서 해석적으로 구한 결과입니다. 그리고 최종적으로 구하고 싶은 ${ \partial z \over \partial x }$ 는 `Expression 3` 에서 구한 두 미분을 곱해 계산합니다.

> Expression 4

$$
{ \partial z \over \partial x } = { \partial z \over \partial t}
{ \partial t \over \partial x } = 2 t \cdot 1 = 2(x+y)
$$

### Chain Rule and Computation Graphs

`Expression 4` 의 연쇄법칙 계산을 계산 그래프로 나타내보겠습니다. 2 제곱 계산을 **2 노드로 나타내면 `Example 7` 처럼 그릴 수 있습니다.

> Example 7

![image](https://user-images.githubusercontent.com/44635266/75775052-8bc97480-5d94-11ea-96f6-fac36d480444.png)

`Example 7` 과 같이 계산 그래프의 역전파는 오른쪽에서 왼쪽으로 신호를 전파합니다. 역전파의 계산 절차에서는 노드로 들어온 입력 신호에 그 노드의 국소적 미분을 곱한 후 다음 노드로 전달합니다.

예를 들어 **2 노드에서의 역전파를 보겠습니다. 입력은 ${ \partial z \over \partial z}$ 이며, 이에 국소적 미분인 ${ \partial z \over \partial t}$ 를 곱하고 다음 노드로 넘깁니다. 한 가지 `Example 7` 에서 역전파의 첫 신호인 ${ \partial z \over \partial z }$ 의 값은 결국 1 이라서 앞의 수식에서 언급하지 않았습니다.

`Example 7` 에서 주목할 것은 왼쪽 역전파입니다. 이 계산은 연쇄 법칙에 따르면 ${ \partial z \over \partial z } { \partial z \over \partial t} { \partial t \over \partial x} = { \partial z \over \partial t} { \partial t \over \partial x} = { \partial z \over \partial x}$ 가 성립되어 *$x$ 에 대한 $z$ 의 미분* 이 됩니다.

`Example 7` 에 `Expression 3` 의 결과를 대입하면 `Example 8` 이 되며, ${ \partial z \over \partial x }$ 는 $2(x+y)$ 임을 구할 수 있습니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/75775079-93891900-5d94-11ea-9c9d-180c351e226d.png)

## Backward Propagation

$+$ 와 X 등의 연산을 예로 들어 역전파의 구조를 설명하겠습니다.

### Backward Propagation of Addition Node

$z = x + y$ 라는 식을 대상으로 역전파를 살펴보겠습니다. 우선 $z = x + y$ 의 미분은 다음과 같이 해석적으로 계산할 수 있습니다.

> Expression 5

$$
{ \partial z \over \partial x } = 1 \\
{ \partial z \over \partial y } = 1 
$$

`Expression 5` 와 같이 모두 1 이 됩니다. 이를 계산 그래프로 나타내면 `Exapmle 9` 처럼 됩니다.

> Example 9

![image](https://user-images.githubusercontent.com/44635266/75775093-9a179080-5d94-11ea-8a92-3f327c3530f6.png)

`Example 9` 와 같이 역전파 때는 상류에서 전해진 미분에 1을 곱하여 하류로 흘립니다. 즉, 덧셈 노드의 역전파는 1 을 곱하기만 할 뿐 입력된 값을 그대로 다음 노드로 보냅니다.

상류에서 전해진 미분 값을 ${ \partial L \over \partial z }$ 라 했는데, 이는 `Example 10` 과 같이 최종적으로 $L$ 이라는 값을 출력하는 큰 계산 그래프를 가정하기 때문입니다. $z = x+y$ 계산은 그 큰 계산 그래프의 중간 어딘가에 존재하고, 상류로부터 ${ \partial L \over \partial z }$ 값이 전해진 것입니다. 그리고 다시 하류로 ${ \partial L \over \partial x }$ 와 ${ \partial L \over \partial y }$ 값을 전달합니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/75775115-a4398f00-5d94-11ea-8170-a2ecd3e9090b.png)

가령 *10 + 5 = 15* 라는 계산이 있고 상류에서 1.3 이라는 값이 흘러옵니다. 이를 계산 그래프로 나타내면 `Example 11` 처럼 됩니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/75775140-ad2a6080-5d94-11ea-8885-baa0de90eba4.png)

덧셈 노드의 역전파는 입력신호를 다른 노드로 출력할 뿐만 아니라 `Example 11` 처럼 1.3 을 그대로 다음 노드에 전달합니다.

### Backward Propagation of Multiple Node

곱셈 노드의 역전파를 설명하겠습니다. $z=xy$ 식을 생각해보겠습니다. 이 식의 미분은 다음과 같습니다.

> Expression 6

$$
{ \partial z \over \partial x } = y \\
{ \partial z \over \partial y } = x
$$

`Expression 6` 계산 그래프는 다음과 같이 그릴 수 있습니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/75775162-b74c5f00-5d94-11ea-9dee-28db2b4cc487.png)

곱셈 노드 역전파는 상류의 값의 순전파 때의 입력 신호들을 서로 바꾼 값을 곱해서 하류로 보냅니다. 서로 바꾼 값이란 `Example 12` 처럼 순전파 때 $x$ 였다면 역전파에서는 $y$, 순전파 때 $y$ 였다면 역전파에서는 $x$ 로 바꾼다는 의미입니다.

구체적인 예를 들어보겠습니다. 가령 $10 \times 5 = 50$ 이라는 계산이 있고 역전파 때 상류에서 1.3 값이 흘러온닥 하겠습니다. 이를 계산 그래프로 그리면 `Example 13` 처럼 됩니다.

> Example 13

![image](https://user-images.githubusercontent.com/44635266/75775176-bf0c0380-5d94-11ea-8f66-3b895557e84d.png)

곱셈의 역전파는 순방향 입력 신호의 값이 필요합니다. 그래서 곱셈 노드를 구현할 때는 순전파의 입력 신호를 변수에 저장해 둡니다.

## Implementing a Simple Layer

위에서 살펴본 사과 예를 Python 으로 구현해보겠습니다. 곱셈 노드를 `MulLayer` 덧셈 노드를 `AddLayer` 라는 이름으로 구현하겠습니다.

### Multiplication Layer

모든 계층은 `forward()` 와 `backward()` 라는 공통의 메소드를 갖도록 구현할것입니다. `forward()` 는 순전파, `backward()` 는 역전파를 처리합니다.

먼저 곱셈 계층을 구현해보겠습니다.

```python
class MulLayer :
    def __init__(self):
        self.x = None
        self.y = None
    
    def forward(self, x, y):
        self.x = x
        self.y = y
        out = x * y

        return out
    
    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x

        return dx, dy
```

`__init__()` 에서는 인스턴스 변수 $x$ 와 $y$ 를 초기화합니다. 이 두 변수는 순전파 시의 입력 값을 유지하기 위해 사용합니다. `forward()` 에서는 $x$ 와 $y$ 를 인수로 받고 두 값을 곱해서 반환합니다. 반면 `backward()` 에서는 상류에서 넘어온 미분`(dout)`  에 순전파 때의 값을 서로바꿔 곱한 후 하류로 흘려보냅니다.

MulLayer 를 사용해서 앞에서 본 사과 쇼핑을 계산 그래프로 구현해보겠습니다.

> Example 14

![image](https://user-images.githubusercontent.com/44635266/75775380-3a6db500-5d95-11ea-87d1-0910564c433d.png)

MulLayer 를 사용하여 `Example 14` 의 순전파를 다음과 같이 구현할 수 있습니다.

```python
apple = 100
apple_num = 2
tax = 1.1

# Layer
mul_apple_layer = MulLayer()
mul_tax_layer = MulLayer()

# Forward
apple_price = mul_apple_layer.forward(apple, apple_num)
price = mul_tax_layer.forward(apple_price, tax)

print(price)
```

각 변수에 대한 미분은 `backward()` 에서 구할 수 있습니다.

```python
dprice=1
dapple_price, dtax = mul_tax_layer.backward(dprice)
dapple, dapple_num = mul_apple_layer.backward(dapple_price)

print(dapple, dapple_num, dtax)
```

`backward()` 호출 순서는 `forward()` 때와는 반대입니다. 또, `backward()` 가 받는 인수는 *순전파의 출력에 대한 미분* 입니다. 가령 `mul_apple_layer` 라는 곱셈 계층은 순전파때는 `apple_price` 를 출력합니다만, 역전파 때는 `apple_price` 의 미분 값인 `dapple_price` 를 인수로 받습니다. 이 코드를 실행한 결과는 `Example 14` 의 결과와 일치합니다.

### Addition Layer

덧셈 노드의 계층은 다음과 같이 구현할 수 있습니다.

```python
class AddLayer:
    def __init__(self):
        pass
    
    def forward(self, x, y):
        out = x + y
        return out

    def backward(self, dout):
        dx = dout * 1
        dy = dout * 1
        return dx, dy
```

덧셈 계층의 `forward()` 에서는 입력받은 두 인수 `x`, `y` 를 더해서 반환합니다. `backward()` 에서는 상류에서 내려온 미분을 그대로 하류로 흘립니다.

덧셈 계층과 곱셈 계층을 사용하여 사과 2 개와 귤 3 개를 사는 `Example 15` 의 상황을 구현해보겠습니다.

> Example 15

![image](https://user-images.githubusercontent.com/44635266/75775406-43f71d00-5d95-11ea-8a1c-b6f75cc19188.png)

`Example 15` 의 계산 그래프를 Python 으로 구현하면 다음과 같습니다. 코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch05/buy_apple_orange.py) 에서 참조했습니다.

```python
apple = 100
apple_num = 2
orange = 150
orange_num = 3
tax = 1.1

# layer
mul_apple_layer = MulLayer()
mul_orange_layer = MulLayer()
add_apple_orange_layer = AddLayer()
mul_tax_layer = MulLayer()

# forward
apple_price = mul_apple_layer.forward(apple, apple_num)  # (1)
orange_price = mul_orange_layer.forward(orange, orange_num)  # (2)
all_price = add_apple_orange_layer.forward(apple_price, orange_price)  # (3)
price = mul_tax_layer.forward(all_price, tax)  # (4)

# backward
dprice = 1
dall_price, dtax = mul_tax_layer.backward(dprice)  # (4)
dapple_price, dorange_price = add_apple_orange_layer.backward(dall_price)  # (3)
dorange, dorange_num = mul_orange_layer.backward(dorange_price)  # (2)
dapple, dapple_num = mul_apple_layer.backward(dapple_price)  # (1)

print("price:", int(price))
print("dApple:", dapple)
print("dApple_num:", int(dapple_num))
print("dOrange:", dorange)
print("dOrange_num:", int(dorange_num))
print("dTax:", dtax)
```

## Implement Activation Function Layer

활성화 함수인 ReLU / Sigmoid Layer 를 구현해보겠습니다.

### ReLU Layer

ReLU 함수에 사용되는 규칙은 다음과 같습니다.

> Expression 7

$$
y = \begin{cases}
x \; (x>0) \\
0 \; (x \leq 0 )
    
\end{cases}
$$

`Expression 7` 에서 $x$ 대한 $y$ 의 미분은 `Example 16` 처럼 구합니다.

> Expression 8

$$
{ \partial y \over \partial x} = \begin{cases}
1 \; (x>0) \\
0 \; (x \leq 0)
\end{cases}
$$

`Expression 8` 에서와 같이 순전파 때의 입력이 $x$ 가 0 보다 크면 역전파는 상류의 값을 그대로 하류로 흘려보냅니다. 하지만 순전파 때 $x$ 가 0 이면 역전파 대는 하류로 신호를 보내지 않습니다.

계산 그래프로는 `Example 16` 처럼 그릴 수 있습니다.

> Example 16

![image](https://user-images.githubusercontent.com/44635266/75775431-51aca280-5d95-11ea-92dd-ce8e1269f04c.png)

ReLU 를 Python 으로 구현해보겠습니다.

```python
class ReLU:
    def __init__(self):
        self.mask = None
    
    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0

        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx
```

ReLU 클래스는 `mask` 라는 인스턴스 변수를 가집니다. `mask` 는 `True/False` 로 구성된 Numpy 배열로 순전파의 입력인 `x` 의 원소 값이 0 이하인 경우 True, 그 외는 False 로 유지합니다.

```python
>>> x = np.array( [[1.0, -0.5], [-2.0, 3.0]])
>>> print(x)
[[ 1. -0.5]
 [-2.  3. ]]
>>> mask = (x <= 0)
>>> print(mask)
[[False  True]
 [True  False]]
```

### Sigmoid Layer

아래 `Expression 9` 은 Sigmoid 함수를 의미하는 함수입니다.

> Expression 9

$$
y = { 1 \over 1 + \exp(-x)}
$$

`Expression 9` 를 계산 그래프로 그리면 `Example 17` 처럼 됩니다.

> Example 17

![image](https://user-images.githubusercontent.com/44635266/75775466-64bf7280-5d95-11ea-8db7-b000b409642d.png)

`Example 17` 에서  $\times$ 와 $+$ 노드 말고도 $exp$ 와 $/$ 노드가 등장했습니다. $exp$ 노드는 $y = exp(x)$ 계산을 수행하고 $/$ 노드는 $y = { 1 \over x}$ 계산을 수행합니다.

`Example 17` 와 같이 `Example 9` 의 계산은 국소적 계산의 전파로 이루어집니다. 이제 `Example 17` 의 역전파를 알아보겠습니다. 여기서 역전파의 흐름을 오른쪽에서 왼쪽으로 1 단계씩 알아보겠습니다.

#### 1 Step

$/$ 노드, $y = { 1 \over x}$ 를 미분하면 다음 식이 됩니다.

> Expression 10

$$
\begin{align}
{ \partial y \over \partial x } = - { 1 \over x^2 } \\
= -y^2
\end{align}
$$

`Expression 10` 에 따르면 역전파 때는 상류에서 흘러온 값에 $-y^2$ 을 곱해서 하류로 전달합니다. 계산 그래프에서는 다음과 같습니다.

> Example 17-1

![image](https://user-images.githubusercontent.com/44635266/75775503-743ebb80-5d95-11ea-8941-977d82cc3a05.png)

#### 2 Step

$+$ 노드는 상류의 값을 여과없이 하류로 내보내는 게 다입니다. 계산 그래프에서는 다음과 같습니다.

> Example 17-2

![image](https://user-images.githubusercontent.com/44635266/75775539-86b8f500-5d95-11ea-95c9-3f02e62099ac.png)

#### 3 Step

$exp$ 노드는 $y=exp(x)$ 연산을 수행하며, 그 마분은 다음과 같습니다.

> Expression 11

$$
{ \partial y \over \partial x} = \exp(x)
$$

계산 그래프에서는 상류의 값에 순전파 때의 출력을 곱해 하류로 전파합니다.

> Example 17-3

![image](https://user-images.githubusercontent.com/44635266/75775563-95071100-5d95-11ea-9153-9a1d594c3fc9.png)

#### 4 Step

$\times$ 노드는 순전파 때의 값을 서로 바꿔서 곱합니다. 이 예에서는 $-1$ 을 곱합니다.

> Example 18

![image](https://user-images.githubusercontent.com/44635266/75775585-9fc1a600-5d95-11ea-8e29-d6c7d022aa78.png)

`Example 18` 에서 알 수 있듯이 역전파의 최종 출력인 ${ \partial L \over \partial y}y^2 \exp(-x)$ 의 값이 하류 노드로 전파됩니다. 저 값은 순전파의 입력 $x$ 와 $y$ 만으로 계산할 수 있습니다.

`Example 18` 의 계산 그래프의 중간 과정을 묶어 `Example 19` 처럼 간단하게 단순한 `sigmmoid` 노드 하나로 대체할 수 있습니다.

> Example 19

![image](https://user-images.githubusercontent.com/44635266/75775649-be27a180-5d95-11ea-8875-6851eae651d4.png)

${ \partial L \over \partial y}y^2 \exp(-x)$ 는 다음처럼 정리해서 사용할 수 있습니다.

> Expression 12

$$
\begin{align}
= { \partial L \over \partial y} { 1 \over (1 + \exp(-x))^2} \exp(-x) \\
= { \partial L \over \partial y} { 1 \over 1 + \exp(-x)} { \exp(-x) \over 1 + \exp(-x)} \\
= { \partial L \over \partial y} y (1-y) 
\end{align}
$$

이처럼 Sigmoid 계층의 역전파는 순전파의 출력 $(y)$ 만으로 계산할 수 있습니다.

> Example 20

![image](https://user-images.githubusercontent.com/44635266/75775660-c5e74600-5d95-11ea-9a98-cd0291b9edb7.png)

Sigmoid 계층을 Python 으로 구현해보겠습니다.

```python
class Sigmoid:
    def __init__(self):
        self.out = None
    
    def forward(self, x):
        out = 1 / (1 + np.exp(-x))
        self.out = out

        return out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out
        
        return dx
```

## Implementing the Affine / Softmax Layer

### Affine Layer

행렬의 곱계산은 `Example 21` 처럼 차원의 원소 수를 일치시키는게 핵심입니다.

> Example 21

![image](https://user-images.githubusercontent.com/44635266/75775673-cf70ae00-5d95-11ea-9912-ddbab7987062.png)

신경망의 순전파 때 수행하는 행렬의 곱은 기하학에서는 **어파인 변환(Affine Transformation)** 이라고 합니다. 그래서 이 책에서는 어파인 변환을 수행하는 처리를 Affine 계층이라는 이름으로 구현합니다.

`Example 21` 수행한 연산을 계산 그래프로 그려보겠습니다. 곱을 계산하는 노드를 `dot` 이라 하면, `np.dot(X, W) + B` 계산은 `Example 22` 처럼 그립니다. 각 변수의 이름 위에 그 변수의 형상도 표기합니다. `Example 22` 에서는 $X$ 의 형상은 $(2, )$ $X \cdot W$ 의 형상은 $(3, )$ 임을 표기했습니다.

> Example 22

![image](https://user-images.githubusercontent.com/44635266/75775687-d7305280-5d95-11ea-9a3f-dd4e474d5ee1.png)

`Example 22` 의 역전파에 대해 생각해보겠습니다. 행렬을 사용한 역전파도 행렬의 원소마다 전개해보면 스칼라값을 사용한 지금까지의 계산 그래프와 순서로 생각할 수 있습니다. 그 결과 다음 식이 도출됩니다.

> Expression 13

$$
{ \partial L \over \partial X } = { \partial L \over \partial Y } \cdot W^T \\
{ \partial L \over \partial W } = X^T \cdot { \partial L \over \partial Y }
$$

`Expression 13` 에서 $W^T$ 의 $T$ 전치 행렬을 뜻합니다. 전치행렬은 $W$ 의 $(i, j)$ 위치의 원소를 $(j, i)$ 위치로 바꾼겁니다. 수식으로는 아래와 같이 사용할 수 있습니다.

> Expression 14

$$
W = \begin{pmatrix}
w_{11} \; w_{12} \; w_{13} \\ 
w_{21} \; w_{22} \; w_{23}
\end{pmatrix} \\

W^T = \begin{bmatrix}
w_{11} \; w_{12} \\
w_{12} \; w_{22} \\
w_{13} \; w_{23}
\end{bmatrix}
$$

`Expression 14` 와 같이 $W$ 의 형상이 $(2, 3)$ 이였다면 전치행렬 $W^T$ 의 형상은 $(3, 2)$ 가 됩니다. `Expression 13` 을 바탕으로 계산 그래프의 역전파를 그려보겠습니다.

> Example 23

![image](https://user-images.githubusercontent.com/44635266/75775704-de576080-5d95-11ea-972f-0f2779a55ee8.png)

`Example 23` 의 계산 그래프에서는 각 변수의 형상에 주의해서 살펴봅시다. 특히 $X$ 와 ${ \partial L \over \partial X }$ 은 같은 형상이고 $W$ 와 ${ \partial L \over \partial W }$ 도 같은 형상입니다. 이유는 아래 식을보면 됩니다.

> Expression 15

$$
X = (x_0, x_1, \cdot \cdot \cdot, x_n) \\
{ \partial L \over \partial X } = ({ \partial L \over \partial x_0 },
{ \partial L \over \partial x_1 }, \cdot \cdot \cdot,
{ \partial L \over \partial x_n })
$$

행렬끼리 곱셈을 할 때에는 아래 그림과 같이 항상 형상의 주의해야합니다.

> Example 24

![image](https://user-images.githubusercontent.com/44635266/75775740-f202c700-5d95-11ea-805e-81f25ee1e40a.png)

### Affine Layer for Batch

위에서 살펴본 Affine 계층은 입력 데이터 $X$ 하나만 가지고 고려했습니다. 이번에는 데이터 N 개를 모아 순전파하는, 배치용 Affine 계층을 생각해보겠습니다.

배치용 Affine 계층을 계산 그래프로 그려보겠습니다.

> Example 25

![image](https://user-images.githubusercontent.com/44635266/75775757-fb8c2f00-5d95-11ea-8745-01c52eb73fc6.png)

기존과 다른건 X 의 형상이 $(N, 2)$ 가 된것입니다.

편향을 더할 때도 주의해야 합니다. 순전파 때의 편향 덧셈은 $X \cdot W$ 에 대한 편향이 각 데이터에 더해집니다. 예를 들어 $N = 2$ 인 경우, 편향은 그 두 데이터 각각에 더해집니다. 구체적인 예를 보겠습니다.

```python
>>> X_dot_W = np.array([[0, 0, 0], [10, 10, 10,]])
>>> B = np.array([1, 2, 3])
>>>
>>> X_dot_W
array([[ 0,  0,  0],
       [10, 10, 10]])
>>> X_dot_W + B
array([[ 1,  2,  3],
       [11, 12, 13]])
```

역전파 때는 각 데이터의 역전파 값이 편향의 원소에 모여야 합니다. 코드로는 다음과 같습니다.

```python
>>> dY = np.array([[1, 2, 3], [4, 5, 6]])
>>> dY
array([[1, 2, 3],
       [4, 5, 6]])
>>>
>>> dB = np.sum(dY, axis=0)
>>> dB
array([5, 7, 9])
```

Affine 을 코드로 구현하면 아래와 같습니다.

```python

class Affine:
    def __init__(self, W, b):
        self.W = W
        self.b = b        
        self.x = None
        self.dW = None
        self.db = None

    def forward(self, x):
        self.x = x
        out = np.dot(self.x, self.W) + self.b

        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)

        return dx
```

### Softmax-with-Loss Layer

소프트맥스 함수는 입력 값을 정규화하여 출력합니다. 예를 들어 MNIST 데이터 인식 Softmax 계층의 출력은 `Example 26` 처럼 됩니다.

> Example 26

![image](https://user-images.githubusercontent.com/44635266/75775783-0c3ca500-5d96-11ea-9824-75aa62859852.png)

Softmax 계층은 입력 값을 정규화하여 출력합니다. MNIST 데이터가 10 개 이므로 Softmax 계층의 입력은 10개가 됩니다.

Softmax 계층은 손실함수인 교차 엔트로피 오차도 포함하여 *Softmax-with-Loss Layer* 이라고도 합니다.

> Example 27

![image](https://user-images.githubusercontent.com/44635266/75775795-16f73a00-5d96-11ea-8b53-e86d6a32169d.png)

Softmax-with-Loss 계층은 복잡해서 간단한 계산그래프로 나타내면 `Example 28` 처럼 나타낼 수 있습니다.

> Example 28

![image](https://user-images.githubusercontent.com/44635266/75775815-21193880-5d96-11ea-9fb8-8c1eeb71740e.png)

`Example 28` 에서 주목할만한 것은 역전파의 결과입니다. Softmax 계층의 역전파는 $(y_1 - t_1, y_2 - t_2, y_3 - t_3)$ 라는 깔끔한 결과를 출력합니다. $(y_1, y_2, y_3)$ 는 Softmax 계층의 출력이고 $(t_1, t_2, t_3)$ 는 정답 레이블이므로 $(y_1 - t_1, y_2 - t_2, y_3 - t_3)$ 는 Softmax 계층의 출력과 정답 레이블의 차분입니다. 신경망의 역전파에서는 이 차이인 오차가 앞 계층에 전해지는 것입니다. 이는 신경망 학습의 중요한 성질입니다.

Softmax-with-Loss 계층의 코드를 보겠습니다.

```python
class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None
        self.t = None
    
    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size
        return dx
```

## Implementation of Backpropagation

### Implementing a Neural Network Using Backpropagation

2 층 신경망을 `TwoLayerNet` 클래스로 구현해보겠습니다. 먼저 이 클래스의 인스턴스 변수와 메서드를 정리한 표를 확인하면 됩니다.

|Instance Variable|Description|
|:--|:--|
|params|딕셔너리 변수로, 신경망의 매개변수를 보관|
|layers|순서가 있는 딕셔너리 변수로, 신경망의 계층을 보관|
|lastLayer|신경망의 마지막 계층, SoftmaxWithLoss 계층|

|Method|Description|
|:--|:--|
|__init__(self, input_size, hidden_size, output_size, weight_init_std)|초기화를 수행한다. 인수는 맨 앞에서부터 입력층 뉴런의 수, 은닉층 뉴런 수, 출력층 뉴런 수, 가중치 초기화 시 정규분포의 스케일|
|predict(self, x)|예측을 수행, x 는 이미지 데이터|
|loss(self, x, t)|손실 함수의 값을 구한다. x 는 이미지 데이터, t 는 정답 레이블|
|accuracy(self, x, t)|정확도를 구한다.|
|numerical_gradient(self, x, t)|가중치 매개변수의 기울기를 수치 미분 방식으로 구한다.|
|gradient(self, x, t)|가중치 매개변수의 기울기를 오차역전파법으로 구한다.|

코드로 알아보겠습니다. 전체 코드는[Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch05/two_layer_net.py) 에 있습니다.

```python
class TwoLayerNet:

    def __init__(self, input_size, hidden_size, output_size, weight_init_std = 0.01):

        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size) 
        self.params['b2'] = np.zeros(output_size)

        self.layers = OrderedDict()
        self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1'])
        self.layers['Relu1'] = Relu()
        self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])

        self.lastLayer = SoftmaxWithLoss()
```

### Verification of Gradient with Backpropagation

코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch05/gradient_check.py) 에서 확인하면됩니다.

```python
import sys, os
sys.path.append(os.pardir)
import numpy as np
from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

x_batch = x_train[:3]
t_batch = t_train[:3]

grad_numerical = network.numerical_gradient(x_batch, t_batch)
grad_backprop = network.gradient(x_batch, t_batch)

for key in grad_numerical.keys():
    diff = np.average( np.abs(grad_backprop[key] - grad_numerical[key]) )
    print(key + ":" + str(diff)
```

MNIST 데이터 셋을 읽어서 훈련 데이터 일부를 수치 미분으로 구한 기울기와 오차역전파법으로 구한 기울기의 오차를 확인해보겠습니다.

```python
b1:9.70418809871e-13
W2:8.41139039497e-13
b2:1.1945999745e-10
W1:2.2232446644e-13
```

결과를 살펴보면 수치 미분과 오차역전파법으로 구한 기울기의 차이가 매우 적다는것을 알 수 있습니다.

### To Implement Learning Using Backpropagation

마지막으로 오차역전파법을 사용한 신경망을 구현하겠습니다. 소스 코드는 [Github](https://github.com/WegraLee/deep-learning-from-scratch/blob/master/ch05/train_neuralnet.py) 에 있습니다.

```python
import sys, os
sys.path.append(os.pardir)

import numpy as np
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
        print(train_acc, test_acc)
```