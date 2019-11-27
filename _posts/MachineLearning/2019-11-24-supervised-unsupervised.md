---
title : Supervised Learning / Unsupervised Learning
tags :
- Supervised Learning
- Unsupervised Learning
---

## 머신러닝

머신 러닝(Machine Learning)이란 “데이터를 이용해서 컴퓨터를 학습시키는 방법론”이다. 이때, 머신 러닝 알고리즘은 크게 세가지 분류로 나눌 수 있다. 바로, 지도 학습(Supervised Learning), 비지도 학습(Unsupervised Learning), 강화 학습(Reinforcement Learning)이다.

![image](https://user-images.githubusercontent.com/44635266/69494162-8b028600-0efb-11ea-89e2-f909273a0163.png)


## 지도 학습(Supervised Learning)

![image](https://user-images.githubusercontent.com/44635266/69494124-1fb8b400-0efb-11ea-9ffa-3dfe6f84b876.png)

지도 학습 (Supervised Learning)은 훈련 데이터(Training Data)로부터 하나의 함수를 유추해내기 위한 기계 학습(Machine Learning)의 한 방법이다. 훈련 데이터는 일반적으로 입력 객체에 대한 속성을 벡터 형태로 포함하고 있으며 각각의 벡터에 대해 원하는 결과가 무엇인지 표시되어 있다. 

이때, 예측하는 결과값이 discrete value(이산값)면 classification(분류) 문제-이 이미지에 해당하는 숫자는 1인가 2인가?-,

예측하는 결과값이 continuous value(연속값)면 regression(회귀) 문제-3개월뒤 이 아파트 가격은 2억1천만원 일 것인가? 2억2천만원 일 것인가?-라고 한다.

즉, 지도 학습(Supervised Learning)은 데이터에 대한 레이블(Label)-명시적인 정답-이 주어진 상태에서 컴퓨터를 학습시키는 방법이다.

### 회귀 분석(Regression analysis)

관찰된 연속형 변수들에 대해 두 변수 사이의 모형을 구한뒤 적합도를 측정해 내는 분석 방법이다.

회귀분석은 시간에 따라 변화하는 데이터나 어떤 영향, 가설적 실험, 인과 관계의 모델링등의 통계적 예측에 이용될 수 있다. 그러나 많은 경우 가정이 맞는지 아닌지 적절하게 밝혀지지 않은 채로 이용되어 그 결과가 오용되는 경우도 있다. 특히 통계 소프트웨어의 발달로 분석이 용이해져서 결과를 쉽게 얻을 수 있지만 적절한 분석 방법의 선택이였는지 또한 정확한 정보 분석인지 판단하는 것은 연구자에 달려 있다.

### 분류 분석(Classification analysis)

데이터 분석의 가장 기본적인 방법중 하나로 데이터 클래스를 설명하는 모형을 제공한다. 데이터에 대한 클래스 라벨이 없는 상태에서 이들을 자동으로 분류하는것을 말하며, 분류가 범주형 클래스를 예측한다면 연속형 속성에 대한 모형을 세워 미래 데이터 경향을 예측할 수 있다.

분류와 예측은 데이터 클래스를 서술하는 모델을 추출하여 항후 데이터의 추세를 예측할 수 있게 해 준다는 공통점을 가진다. 단지 분류는 범주형 레이블을 대상으로 하는 반면 예측은 연속형 값에 대한 함수형태의 모델설정을 한다는 점에 차이가 있을 뿐이다. 즉, 분류는 이산치나 명목형 값을 예측하는 반면 예측모델은 연속적이거나 정렬된 데이터 값을 예측하는데 사용한다. 분류모델에서는 은행이 대출심사를 하면서 대출해도 안전한지를 구분하는 것이라면, 예측모델에서는 특정 고객에 대해 주택소비가 앞으로 어떻게 변화할 것인지를 예측하는 식이다.

### 대표적인 알고리즘

* Support Vector Machines
* linear regression
* logistic regression
* linear discriminant analysis
* Neural Networks (Multilayer perceptron)
* Similarity learning 

## 비지도 학습(Unsupervised Learning)

![image](https://user-images.githubusercontent.com/44635266/69494129-20e9e100-0efb-11ea-9124-4807084adf24.png)

비지도 학습(Unsupervised Learning)은 통계학의 밀도 추정과 깊은 연관이있고, 머신러닝 및 데이터 마이닝 분야에서는 클러스터링(Clustering)에 많이 이용되며, 데이터가 어떻게 구성이 되어있는지를 알아내는 방법이다. 이 방법은 지도 학습 (Supervised Learning) 혹은 강화 학습(Reinforcement Learning)과는 달리 입력값에 대한 목표치가 주어지지 않는다. 그래서 특정 입력에(Input)에 대하여 정답이 없는 데이터 집합이 주어지는경우의 학습이다.

즉, 비지도 학습(Unsupervised Learning)은 데이터에 대한 레이블(Label)-명시적인 정답-이 주어지지 상태에서 컴퓨터를 학습시키는 방법론이다.

### 대표적인 알고리즘

* Clustering
* k-means
* Neural Networks
* Autoencoders
* Deep Belief Nets
* Hebbian Learning