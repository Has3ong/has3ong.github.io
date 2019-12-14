---
title : Keras Classification Analysis
tags :
- Keras
- Classfication
- Fashion MNIST Data
---

## Classification Analysis

데이터 분석의 가장 기본적인 방법중 하나로 데이터 클래스를 설명하는 모형을 제공한다. 데이터에 대한 클래스 라벨이 없는 상태에서 이들을 자동으로 분류하는것을 말하며, 분류가 범주형 클래스를 예측한다면 연속형 속성에 대한 모형을 세워 미래 데이터 경향을 예측할 수 있다.


분류와 예측은 데이터 클래스를 서술하는 모델을 추출하여 항후 데이터의 추세를 예측할 수 있게 해 준다는 공통점을 가진다. 단지 분류는 범주형 레이블을 대상으로 하는 반면 예측은 연속형 값에 대한 함수형태의 모델설정을 한다는 점에 차이가 있을 뿐이다. 즉, 분류는 이산치나 명목형 값을 예측하는 반면 예측모델은 연속적이거나 정렬된 데이터 값을 예측하는데 사용한다. 분류모델에서는 은행이 대출심사를 하면서 대출해도 안전한지를 구분하는 것이라면, 예측모델에서는 특정 고객에 대해 주택소비가 앞으로 어떻게 변화할 것인지를 예측하는 식이다.

## Fashion MNIST DataSet Classification

10개의 범주(category)와 70,000개의 흑백 이미지로 구성된 패션 MNIST 데이터셋을 사용하겠습니다. 이미지는 해상도(28x28 픽셀)가 낮고 다음처럼 개별 옷 품목을 나타냅니다

![image](https://user-images.githubusercontent.com/44635266/69493671-ce0d2b00-0ef4-11ea-9da4-690ba49d2de9.png)

패션 MNIST는 컴퓨터 비전 분야의 "Hello, World" 프로그램격인 고전 MNIST 데이터셋을 대신해서 자주 사용됩니다. MNIST 데이터셋은 손글씨 숫자(0, 1, 2 등)의 이미지로 이루어져 있습니다. 여기서 사용하려는 옷 이미지와 동일한 포맷입니다.

패션 MNIST는 일반적인 MNIST 보다 조금 더 어려운 문제이고 다양한 예제를 만들기 위해 선택했습니다. 두 데이터셋은 비교적 작기 때문에 알고리즘의 작동 여부를 확인하기 위해 사용되곤 합니다. 코드를 테스트하고 디버깅하는 용도로 좋습니다.

네트워크를 훈련하는데 60,000개의 이미지를 사용합니다. 그다음 네트워크가 얼마나 정확하게 이미지를 분류하는지 10,000개의 이미지로 평가하겠습니다. 패션 MNIST 데이터셋은 텐서플로에서 바로 임포트하여 적재할 수 있습니다

```python
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import *
from keras.models import Sequential
import keras

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

train_images = train_images / 255.0
test_images = test_images / 255.0

model = Sequential()
model.add(Flatten(input_shape=(28, 28)))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=3)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print(test_loss, test_acc)

predictions = model.predict(test_images)

def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)
plt.show()
```

> Check Data Format / Label

![image](https://user-images.githubusercontent.com/44635266/69493672-cf3e5800-0ef4-11ea-8d04-39f0937e774b.png)

> epochs = 5, Prediction

![image](https://user-images.githubusercontent.com/44635266/69493702-4aa00980-0ef5-11ea-8c80-84cc0e49f512.png)

> epochs = 25, Prediction

![image](https://user-images.githubusercontent.com/44635266/69493718-8935c400-0ef5-11ea-8999-372f30e3f916.png)

## References

(https://www.tensorflow.org/tutorials/keras/classification?hl=ko)

