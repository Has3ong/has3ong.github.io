---
title : Machine Learning Perceptron
tags :
- Perceptron
- Machine Learning
- Python
---

*이 포스트는 [Deep Learning from Scratch]() 를 바탕으로 작성하였습니다.*

## What is Perceptron?

**퍼셉트론(Perceptron)** 은 다수의 신호를 받아 하나의 신호를 출력합니다. 여기서 말하는 신호란 전류나 강물처럼 흐름이 있는 것을 상상하면 좋습니다. 전류가 전선을 타고 흐르는 전자를 내보내듯, 퍼셉트론 신호도 흐름을 만들고 정보를 앞으로 전달합니다. 다만, 퍼셉트론의 신호는 1 / 0 두 가지 값을 가질 수 있습니다. 여기선 1 을 *신호가 흐른다*, 0 을 *신호가 흐르지 않는다* 의미로 사용하겠습니다.

> Example 1

![image](https://user-images.githubusercontent.com/44635266/75086452-aec77d80-5577-11ea-8b78-27b7f47a4001.png)

`Example 1` 은 입력으로 2개의 신호를 받는 퍼셉트론의 예입니다. $x_1$ 과 $x_2$ 는 입력신호 $y$ 는 출력 신호, $w_1$ 과 $w_2$ 는 가중치를 뜻합니다.

그림의 원을 **뉴런** 혹은 **노드** 라고 부릅니다. 입력 신호가 뉴런에 보내질 때는 각각 고유한 가중치가 곱해집니다. 뉴런에서 보내온 신호의 총합이 정해진 한계를 넘어설 때만 1 을 출력합니다.

퍼셉트론을 수식으로 나타내면 아래처럼 됩니다.

$$y = 
\begin{cases}
0\;(w_1x_1 + w_2x_2 \le \theta) \\
1\;(w_1x_1 + w_2x_2 > \theta)
\end{cases}
$$

퍼셉트론은 복수의 입력 신호 각각에 고유한 가중치를 부여합니다. 가중치는 각 신호가 결과에 주는 영향력을 조절하는 요소로 작용합니다. 즉, 가중치가 클수록 해당 신호가 그만큼 더 중요함을 뜻합니다.

## Simple Logic Gate

### AND GATE

퍼셉트론을 활용한 간단한 문제를 살펴보겠습니다. 논리 회로를 알아보는 첫걸음으로 AND 게이트를 알아보겠습니다. AND 게이트는 입력이 둘이고 출력은 하나입니다. 아래 `Example 2` 와 같은 입력 신호화 출력 신호의 대응 표를 진리표라고 합니다. 이 그림은 AND 게이트의 진리표로 두 입력이 모두 1 일 때만 1을 출력하고, 그 외에는 0 을 출력합니다.

> Example 2

![image](https://user-images.githubusercontent.com/44635266/75086456-b0914100-5577-11ea-8ce6-bdceea19a112.png)

### NAND GATE / OR GATE

이어서 NAND 게이트를 알아보겠습니다. NAND 는 Not AND 를 의미하며 그 동작은 AND 게이트의 출력을 뒤집은 것입니다. 진리표로 나타내면 `Example 3 ` 과 같이 $x_1$ 과 $x_2$ 가 모두 1 일 때만 0 을 출력하고 나머지는 1을 출력합니다.

> Example 3

![image](https://user-images.githubusercontent.com/44635266/75086457-b25b0480-5577-11ea-92de-094f7310c351.png)


`Example 4` 는 OR 게이트입니다. OR 게이트는 입력값 중 하나 이상이 1 이면 출력이 1 이 되는 논리 회로 입니다.

> Example 4

![image](https://user-images.githubusercontent.com/44635266/75086459-b424c800-5577-11ea-9f2b-fa500a0cf5a8.png)

## Implementing Perceptron

### From simple implementation

논리 회로를 Python 으로 구현해보겠습니다. 다음은 x1 과 x2 를 인수로 받는 AND 라는 함수입니다.

```python
def AND(x1, x2):
    w1, w2, theta = 0.5, 0.5, 0.7
    tmp = x1 * w1 + x2 * w2
    if tmp <= theta:
        return 0
    elif tmp > theta:
        return 1
```

매개변수 `w1`, `w2`, `theta` 는 함수 안에서 초기화하고, 가중치를 곱한 입력의 총합이 임계값을 넘으면 1 을 반환하고 그 외에는 0 을 반환합니다. 이 함수의 출력이 `Example 2` 와 확인해보면 됩니다.

```python
AND(0, 0) # 0
AND(1, 0) # 0
AND(0, 1) # 0
AND(1, 1) # 1
```

### Introduction of weights and bias

앞에서 구현한 AND 게이트는 직관적이고 알기 쉽지만 앞으로 생각해서 다른 방식으로 수정하겠습니다. 위의 수식의 $\theta$ 를 $-b$ 로 치환하면 퍼셉튼론의 동작이 아래처럼 됩니다.

$$y = 
\begin{cases}
0\;(b + w_1x_1 + w_2x_2 \le \theta) \\
1\;(b + w_1x_1 + w_2x_2 > \theta)
\end{cases}
$$

기호 표기에 변화만 줬으며, 그 의미는 같습니다. 여기에서 `b` 를 **편향(Bias)** 라 하며, $w_1$ 과 $w_2$ 는 그대로 가중치 입니다. 위 식의 관점에서 해석해보면 퍼세브론은 입력신호에 가중치를 곱한 값과 편향을 합하여 그 값이 0 을 넘으면 1 을 출력하고 그렇지 않으면 0 을 출력합니다.

그럼 Numpy 를 이용하여 위의 식을 구현해보겠습니다.

```python
>>> import numpy as np
>>> x = np.array([0, 1])
>>> w = np.array([0.5, 0.5])
>>> b = -0.7
>>> w * x
array([0. , 0.5])
>>> np,sum(w*x)
0.5
>>> np.sum(w*x) + b
-0.1999999999999996
```

Numpy 배열끼리의 곱셈은 두 배열의 원소수가 같다면 각 원소끼리 곱합니다. 또 `np.sum()` 메소드는 입력한 배열에 담긴 모든 원소의 총합을 계산합니다.

### To Implement weights and deflections

```python
def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1
```

여기서 $-\theta$ 가 편향 $b$ 로 치환되었습니다. 그리고 편향은 가중치 $w_1, w_2$ 와 기능이 다른 사실도 주의해야 합니다.

편향은 뉴런이 어라만 쉽게 활성화 하느냐를 조정하는 매개변수입니다. 예를들어 $b$ 가 -0.1 이면 각 입력 신호에 가중치를 곱한 값들이 합이 0.1 을 초과할 때만 뉴런이 활성화합니다. 반면 b 가 -20 인 경우 각 입렵신호에 가중치를 곱한 값들의 합이 20.0 을 넘지 않으면 뉴런은 활성화하지 않습니다.

한편 $w_1$ 과 $w_2$ 는 가중치로 $b$ 는 편향으로 서로 구별하기도 하지만 셋다 가중치라 할 때도 있습니다.

이어서 NAND 게이트와 OR 게이트를 구현해보겠씁니다.
    
```python
def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1
```

## Perceptron's Limit

### XOR Gate

XOR 게이트는 배타적 논리합이라는 논리 회로입니다. $x_1$ 과 $x_2$ 중 한쪽에서 1일 때만 1을 출력합니다.

아래 `Example 5` 가 XOR 진리표입니다.

> Example 5

![image](https://user-images.githubusercontent.com/44635266/75086736-de2bb980-557a-11ea-8e70-3693e7e15a70.png)

사실 지금까지 알아본 퍼셉트론으로는 이 XOR 게이트를 구현할 수 없습니다. 시각적으로 알아보겠습니다.

먼저 OR 게이트의 수식을 알아보겠습니다.

위 식은 OR 게이트이며 이 식의 퍼셉트론은 직선으로 나뉜 두 영역으로 만듭니다. 직선으로 나뉜 한쪽 영역은 1 로 출력하고 다른 한쪽은 0 을 출력합니다. 이를 그림으로 그려보면 `Example 6` 처럼 됩니다.

> Example 6

![image](https://user-images.githubusercontent.com/44635266/75086739-e4ba3100-557a-11ea-914f-1f614f95b269.png)

OR 게이트는 $(x_1, x_2) = (0, 0)$ 일 때 0 을 출력하고 나머지는 1 을 출력합니다. 그림에서는 0 을 원 1 을 삼각형으로 표시햇습니다.

그럼 XOR 게이트의 경우를 알아보겠습니다. 아래 `Example 7` 을 보고 직선 하나로 나누는 방법을 생각해보겠습니다. 

> Example 7

![image](https://user-images.githubusercontent.com/44635266/75086740-eab01200-557a-11ea-9761-1c4084d6bc1e.png)

### Linear and Nonlinear

직선 하나로는 위 `Example 7` 을 나눌 수 없습니다. 하지만 `Example 8` 처럼 나눌 수 있습니다.

> Example 8

![image](https://user-images.githubusercontent.com/44635266/75086744-f0a5f300-557a-11ea-84a1-3222c2d4f63f.png)

퍼셉트론은 직선 하나로 나눈 영역만 표현할 수 있는 한계가 있습니다. 위 `Example 8` 같은 곡선은 표현할 수 없습니다. 위 그림과 같은 곡선의 영역을 비선형 영역이라 하며, 직선의 영역은 선형 영역이라고 합니다.

## If a multi - layered Perceptron goes in,

퍼셉트론으로는 XOR 게이트를 표현할 수 없습니다.

하지만 **다층 퍼셉트론(Multi-Layer Perceptron)** 을 만들 수 있습니다. 층을 하나 더 쌓아서 XOR 을 표현해보겠습니다.

### To combine existing Logic Gates

XOR 게이트를 만드는 방법은 다양하지만, 그중 하나는 AND, NAND, OR 게이트를 조합하는 방법입니다. 여기서는 각각의 게이트를 `Example 9` 과 같은 기호로 표기하겠습니다.

> Example 9

![image](https://user-images.githubusercontent.com/44635266/75086792-5f834c00-557b-11ea-9376-d999ccb4042c.png)

아래 와 같이 세 가지 게이트를 하나씩 조합하면 XOR 게이트를 완성할 수 있습니다.

> Example 10

![image](https://user-images.githubusercontent.com/44635266/75086794-6611c380-557b-11ea-92f1-1b6d90e11cc0.png)

진리표를 이용하여 정말 XOR을 구현하는지 알아보겠습니다. NAND 의 출력을 $s_1$ OR 의 출력을 $s_2$ 해서 진리표를 만들면 아래 `Example 11` 처럼 됩니다.

> Example 11

![image](https://user-images.githubusercontent.com/44635266/75086797-6ca03b00-557b-11ea-9cd7-f3ee41620559.png)

### Implementing an XOR logical circuit

이어서 XOR 게이트를 Python 으로 구현해보겠습니다. 아래와 같이 구현하면 됩니다.

```python
def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y
```

이 XOR 함수는 기대한 결과로 출력합니다.

```python
XOR(0, 0) # 0
XOR(1, 0) # 1
XOR(0, 1) # 1
XOR(1, 1) # 0
```

지금 구현한 XOR 을 뉴런을 이용한 퍼셉트론으로 표현하면 아래 `Example 12 ` 처럼 됩니다.

> Example 12

![image](https://user-images.githubusercontent.com/44635266/75086814-b4bf5d80-557b-11ea-8b90-461cb19fa519.png)

XOR 은 위 `Example 12` 처럼 다층 구조의 네트워크 입니다. 기존의 AND, OR 는 단층 퍼셉트론인 데 반해, XOR는 2층 퍼셉트론입니다. 이처럼 여러 개인 퍼셉트론을 다층 퍼셉트론이라 합니다.

2 층 퍼셉트론의 동작을 공장의 조립라인에 비유할 수 있습니다. 1 단 작업자는 부품을 다듬어 일이 완료되면 2 단 작업제가에게 건네줍니다. 2 단 작업자는 부품을 다듬어 완성품을 출하합니다. 이처럼 XOR 게이트 퍼셉트론에서는 작업자들 사이에 부품을 전달하는 일이 이뤄집니다.

다시 말해 **단층 퍼셉트론으로 표현하지 못한 것을 층을 하나 늘려 구현** 할 수 있습니다.

