---
title : Iterators and Generators
tags :
- Generator
- Iterator
- Python
---

*이 포스트는 [High Performance Python](https://github.com/darrenzeng2012/nohtyp/blob/master/High%20Performance%20Python%20-%20Practical%20Performant%20Programming%20for%20Humans%202014.pdf) 를 바탕으로 작성하였습니다.*


다른 프로그래밍 언어에 익숙한 사람이 Python 을 처음 접하면 루프 표기법에 놀라곤 합니다. 다른 언어의 루프는 보통 다음과 같은 형태입니다.

```java
# Other languages
for (i=0; i<N; i++) {
    do_work(i);
}
```

하지만 Python 에서는 `range` 나 `xrange` 를 사용할 수 있습니다.

```python
# Python
for i in range(N):
    do_work(i)
```

`range` 와 `xrange` 함수는 통하여 **제너레이터(Genrator)** 를 사용할 수 있습니다. 제너레이터를 이해하기 위해 이들 함수의 간단한 구현을 살펴보겠습니다.

```python
def range(start, stop, step=1):
    numbers = []
    while start < stop:
        numbers.append(start)
        start += step
    return numbers

def xrange(start, stop, step=1):
    while start < stop:
        yield start #
        start += step

for i in range(1,10000):
    pass

for i in xrange(1,10000):
    pass
```

> 이 함수는 값을 반환하는 대신 `yield` 를 이용하여 여러 값을 생산합니다. 이로인해 함수가 반복적으로 다음 값을 생산하는 제너레이터로 변합니다.

`range` 함수는 주어진 범위의 모든 수를 담는 리스트를 생성합니다. 따라서 1 부터 10,000 까지 범위를 구하면 `numbers` 리스트에 값을 10,000 번 추가한 다음 그 리스트를 반환합니다.

반면 제너레이터는 값을 여러 번 반환할 수 있습니다. 코드가 `yield` 를 실행하는 순간 이 함수는 값을 방출하고, 다른 값 요청이 들어오면 이전 상태를 유지한 채로 실행을 재개하여 새로운 값을 방출합니다.

함수가 끝나면 `StopIteration` 예외를 발생시킵니다. 결국 두 함수가 같은 횟수의 연산을 수행해도 `range` 를 사용하는 루프가 10 배 이상의 메모리를 사용합니다.

위 함수를 염두에 두고 `range` 와 `xrange` 를 사용한 `for` 루프를 분석해보겠습니다. Python 의 `for` 루프에는 반복할 수 있는 객체가 필요합니다. 즉, 루프 밖에서 **이터레이터(Iterator)** 를 생성할 수 있어야 하는 의미입니다. 

대부분 객체에서 이터레이터를 생성하려면 Python 의 내장 함수인 `iter` 를 사용하면 됩니다. 이 함수는 리스트, 튜플, 사전, 셋에 사용할 수 있으며 객체의 값이나 키에 대한 이터레이터를 반환합니다. `xrange` 는 이미 이터레이터를 반환하므로 `xrange` 에 `iter` 를 호출할 필요는 없습니다.

하지만 `range` 는 리스트를 반환하므로 리스트의 모든 값을 순회하는 리스트 이터레이터 객체를 새로 만들어야 합니다. 이터레이터를 생성하고 나면 그 이터레이터에 `next()` 를 호출하는 것만으로 `StopIteration` 예외가 발생할 때까지 새로운 값을 얻어올 수 있습니다. 이를 바탕으로 아래와 같이 `for` 루프를 재구성할 수 있습니다.

```python
# The python loop
for i in object:
    do_work(i)

# Is equivalent to
object_iterator = iter(object)
while True:
    try:
        i = next(object_iterator)
    except StopIteration:
        break
    else:
        do_work(i)
```

예제의 `for` 루프 코드에서 `xrange` 대신 `range` 를 사용했을 때 추가 `iter` 를 호출하는걸 확인할 수 있습니다. `xrange` 를 사용하면 이터레이터로 변형되는 제너레이터를 생성합니다. 하지만, `range` 는 새로운 리스트를 할당하고 값을 미리 계산한 다음 이터레이터를 생성해야 합니다.

`range` 는 리스트를 미리 계산하려면 한 번에 하나의 값만 필요함에도 전체 데이터를 저장할 수 있는 공간을 할당하고 올바른 값을 넣어야 한다는 것입니다. `range` 는 사용할 수 있는 양보다 더 많은 메모리를 할당하려 시도해 루프 자체를 동작 불능에 빠트릴 가능성도 있습니다.

```python
def test_range():
    """
    >>> %timeit test_range()
    1 loops, best of 3: 446 ms per loop
    """
    for i in range(1, 10000000):
        pass

def test_xrange():
    """
    >>> %timeit test_xrange()
    1 loops, best of 3: 276 ms per loop
    """
    for i in xrange(1, 10000000):
        pass  
```

이 문제는 `range` 대신 `xrange` 를 사용하여 아주 간단하게 해결할 수 있습니다. 하지만 실제 문제는 다른곳에 숨어있습니다. 아주 많은 수를 담은 리스트 `list_of_numbers` 가 있고 그중 3의 배수가 몇 개인지 확인해보겠습니다.

```python
divisible_by_three = sum(1 for n in fibonacci_gen(100_000) if n % 3 == 0)
```

이 코드는 `range` 와 동일한 문제가 있습니다. 여기선 **리스트 내포(List Comprehension)** 문법을 사용했기 때문에 `list_of_numbers` 에 있는 모든 리스트를 미리 생성한 다음 계산을 수행합니다. 그래서 리스트의 크기가 상당히 크다면 불필요한 리스트 때문에 사실상 아무런 이유 없이 많은 메모리를 할당할 수 있고, 할당한 용량이 실제 사용할 수 있는 메모리를 초과할 수 있습니다.

리스트 내포와 **제너레이터 내포(Generator Comphrehension)** 문법의 작은 차이로 `divisible_by_three` 를 만드는 코드를 최적화할 수 있습니다. 하지만 제너레이터에는 `length` 속성이 없다는것을 기억하고 다시 구현해보겠습니다.

```python
divisible_by_three = sum(( 1 for n in list_of_numbers if n % 3 == 0))
```

여기선 3 의 배수이면 1 을 생상하는 제너레이터를 만들었습니다. 두 버전의 성능은 비슷하지만 메모리 사용량은 제너레이터를 사용한 쪽어 훨씬 작습니다.

## Iterators for Infinite Series

지나온 상태 중 일부만 저장하고 현재 값만 출력하면 되는 상황이라면, 제너레이터는 **무한 급수(Infinite Series)** 를 위한 이상적인 해법입니다. 피보나치 수열이 좋은 예입니다.

```python
def fibonacci():
    i, j = 0, 1
    while True:
        yield j
        i, j = j, i + j
```

제너레이터에서 생성하는 값은 `j` 지만 피보나치 수열의 상태를 추적하기 위해 `i` 값도 계속 유지하는것을 볼 수 있습니다.

계산에 필요한 상태의 양은 메모리에서 객체가 차지하는 실제 크기에 직결되므로 중요합니다. 따라서 다수의 상태를 계속 유지해야 하고 반환하는 결과가 많지 않다면 제너레이터보다 리스트를 미리 생성하는 이터레이터 방식이 좋습니다.

제너레이터는 코드의 흐름을 감추기 때문에 남발하지 않는게 좋습니다. 제너레이터는 실제 코드를 정돈하고 매끈한 루프를 작성하기 위한 수단입니다. 피보나치 수를 구하는 몇 가지 예제를 보겠습니다.

```python
def fibonacci_naive():
    i, j = 0, 1
    count = 0
    while j <= 5000:
        if j % 2:
            count += 1
        i, j = j, i + j
    return count

def fibonacci_transform():
    count = 0
    for f in fibonacci():
        if f > 5000:
            break
        if f % 2:
            count += 1
    return count

from itertools import takewhile
def fibonacci_succinct():
    first_5000 = takewhile(lambda x: x <= 5000,
                           fibonacci())
    return sum(1 for x in first_5000
               if x % 2)
```

## Lazy Generator Evaluation 

제너레이터를 사용한 피보나치 수열 계산에서는 항상 현재 값만 사용할 뿐 수열 앞쪽에 나온 다른 값을 참조할 수 없습니다. 이런 특징 때문에 가끔 제너레이터를 사용하기 어려운 경우가 있는데, 그럴 때 도움이 되는 모듈이나 함수가 있습니다.

그 중 표준 라이브러리인 `itertools` 가 가장 대표적입니다. 대표적인 함수는 아래와 같습니다.

* **islice**
  * 제너레이터에 대한 슬라이스 기능 제공
* **chain**
  * 여러 제너레이터를 연결
* **takewhile**
  * 제너레이터 종료 조건을 추가
* **cycle**
  * 유한한 제너레이터를 계속 반복하게 하여 무한 제너레이터로 동작

대용량 데이터 분석에 제너레이터를 사용하는 예제를 작성해보겠습니다.

데이터 파일은 `"timestamp, value"` 형태로 저장되어 있고 일 평균에서 $3\sigma$ 를 벗어난 날짜를 찾는 것이 목표입니다.

먼저 파일을 줄 단위로 읽는 코드부터 작성하겠습니다. 그리고 각 줄의 값을 Python 객체로 출력합니다. `read_fake_data()` 는 알고리즘을 테스트하는 가짜 데이터를 생산하는 제너레이터입니다. `read_data()` 와 같은 모양이 되도록 하면 아래 예제처럼 됩니다.

제너레이터의 `next()` 가 호출되어야만 실제로 파일에서 한 줄을 읽거나 가짜 데이터를 생성하는 **지연 실행(Lazy Evaluation)** 을 구현했습니다.

```python
from random import normalvariate, rand
from itertools import count

def read_data(filename):
    with open(filename) as fd:
    for line in fd:
        data = line.strip().split(',')
        yield map(int, data)

def read_fake_data(filename):
    for i in count():
        sigma = rand() * 10
        yield (i, normalvariate(0, sigma))
```

`itertools` 의 `groupby` 함수를 사용하여 같은 날의 타임 스탬프를 하나씩 묶어보겠습니다. 이 함수는 연속적인 항목과 이 항목들을 그룹 지을 키를 인자로 받고 결과로는 튜플을 생성하는 제너레이터를 반환합니다.

즉 입력이 *A A A A B B A A* 인 경우에 `groupby` 로 묶으면 *(A, [A, A, A, A]), (B, [B, B]), (A, [A, A])* 이렇게 3 그룹이 생깁니다.

```python
from datetime import date
from itertools import groupby

def day_grouper(iterable):
    key = lambda (timestamp, value) : date.fromtimestamp(timestamp)
    return groupby(iterable, key)
```

특이점을 찾는 코드를 작성해보겠습니다. 날짜별로 값을 살펴보고 평균과 최댓값을 계속 유지합니다. 최댓값은 특이점을 찾기 위해 사용합니다. 만약 최댓값이 평균보다 3 시그마 이상 벌어진다면 해당 날짜의 `date` 객체를 반환하게 만들었습니다. 

`check_anomaly` 함수는 데이터 필터 역할을 하도록 설계하여 특이점인 경우 `True` 를 반환하고, 그렇지 않으면 `False` 를 반환하게 하여 원래 데이터 중 조건에 맞는 날자만 걸러내도록 했습니다.

```python
import math
def check_anomaly((day, day_data)):
  # We find the mean, standard deviation, and maximum values for the day.
  # Using a single-pass mean/standard deviation algorithm allows us to only
  # read through the day's data once.
    n = 0
    mean = 0
    M2 = 0
    max_value = None
    for timestamp, value in day_data:
        n += 1
        delta = value - mean
        mean = mean + delta/n
        M2 += delta*(value - mean)
        max_value = max(max_value, value)
    variance = M2/(n - 1)
    standard_deviation = math.sqrt(variance)
 
    # Here is the actual check of whether that day's data is anomalous. If it
    # is, we return the value of the day; otherwise, we return false.
    if max_value > mean + 3 * standard_deviation:
        return day
    return False
```

이제 아래와 같이 제너레이터를 조합하여 특이점을 찾을 수 잇습니다.

```python
from itertools import ifilter, imap

data = read_data(data_filename)
data_day = day_grouper(data)
anomalous_dates = ifilter(None, imap(check_anomaly, data_day)) #

first_anomalous_date, first_anomalous_data = anomalous_dates.next()
print ("The first anomalous date is: ", first_anomalous_date)
```

위 예제는 어떠한 계산도 하지 않고 실제 계산을 수행하는 다른 함수를 연결하여 문제를 해결합니다. `anomalous_dates.next()` 가 호출되거나 `anomalous_dates` 제너레이터가 다음 값을 생성하지 않는 한 파일을 절대 읽지 않습니다. 사실상 `nomalous_dates` 에서 새로운 값을 받았을때만 분석을 수행합니다.

하지만 전체 데이터에 다섯 군데의 특이점이 있는데 첫 번째 지점만 보고를 받고 새로운 값을 더 이상 요청하지 않는다면, 해당 지점까지만 파일을 읽습니다. 이를 지연 실행이라 하며, 요청이 명시적으로 들어오는 경우에만 실행하여 종료 조건을 빨리 만나면 전체 실행 시간이 극적으로 단축됩니다.

이런 방식으로 분석을 시도하면 코드를 많이 고치지 않고도 쉽게 대규모 분석을 할 수 있습니다. 예를 들어 하루 단위로 계산하는 대신 한 시간 크기의 이동칭으로 계산하고 싶다면 다음의 `day_grouper` 를 이용할 수 있습니다.

```python
from datetime import datetime

def rolling_window_grouper(data, window_size=3600):
    window = tuple(islice(data, 0, window_size))
    while True:
        current_datetime = datetime.fromtimestamp(window[0][0])
        yield (current_datetime, window)
        window = window[1:] + (data.next(),)
```

`day_grouper` 대신 `rolling_window_grouper` 를 사용하여 원하는 결과를 얻을 수 있습니다. 여기선 하루 치 데이터를 다루는 대신 한 시간 데이터만 저장하므로 메모리를 아낄 수 있습니다.

또한, 이렇게 샘플링한 데이터조차 메모리에 담을 수 없는 경우에는 파일을 여러 번 열어서 정확히 원하는 위치를 가리키는 **디스크립터(Descriptor)** 를 만들어 사용할 수 있습니다.

마지막으로 `rolling_window_group` 함수에는 `window` 리스트에 대해 `pop` 와 `append` 연산을 많이 사용하는데 `collections` 모듈에 `deque` 를 사용해 최적화할 수 있습니다.