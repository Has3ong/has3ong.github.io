  ---
title : Python Lists and Tuples
tags :
- Tuple
- List
- Python
---

*이 포스트는 [High Performance Python](https://github.com/darrenzeng2012/nohtyp/blob/master/High%20Performance%20Python%20-%20Practical%20Performant%20Programming%20for%20Humans%202014.pdf) 를 바탕으로 작성하였습니다.*

리스트와 튜플은 배열이라고 하는 자료구조의 한 종류입니다. 배열은 어떤 정해진 내재적 순서에 따라 데이터를 나열해둔 것입니다. 이렇게 순서를 미리 알 수 있다는 점이 중요합니다. 순서를 미리 알 수 있으면, 배열 내 특정 위치에 있는 데이터를 O(1) 시간 복잡도로 접근할 수 있습니다.

배열은 여러가지 방법으로 구현할 수 있는데, 리스트는 동적 배열이고 튜플은 정적 배열이라고 할 수 있습니다.

배열을 생성하려면 먼저 시스템의 메모리 블록을 할당해야 합니다. 리스트와 튜플도 마찬가지 입니다. 이때 블록의 각 구역에는 실제 데이터의 위치를 가리키는 포인터가 저장될 것이며, 포인터의 크기는 정수형(Integer) 의 크기입니다.

메모리 블록 할당 과정은 커널까지 내려가 N 개의 연속된 바구니를 요청합니다. `Example 1` 은 크기가 6인 배열이 시스템 메모리에 배치된 예를 보여줍니다. Python 의 리스트는 그 크기도 저장하기 때문에 할당된 여섯 블록 중 하나는 크기를 저장하고 나머지 다섯 개만 사용할 수 있습니다.

> Example 1 - Example of system memory layout for an array of size 6

![image](https://user-images.githubusercontent.com/44635266/74741267-d8df1e00-529f-11ea-9777-e8c682b92bc1.png)

리스트에서 특정 항목을 찾으려면 그 항목이 무엇이며, 그 데이터가 어떤 바구니에 저장되는지만 알면 됩니다. 모든 데이터는 같은 크기를 점유하므로 데이터의 종류는 알 필요가 없습니다.

예를 들어 배열의 첫 번째 항목을 찾으려고 한다면 배열이 시작하는 위치에 있는 첫 번째 바구니의 값(M)을 읽으면 됩니다. 다섯 번째 항목을 읽으려면 M+4 위치에 값을 읽으면 됩니다. 따라서 연속적인 메모리에 정렬되어 저장된 데이터는 배열의 크기에 상관없이 한 번에 읽을 수 있습니다. 따라서 시간 복잡도는 O(1) 입니다.

```python
>>> %%timeit l = list(range(10))
        ...: l[5]
        ...:
30.1 ns ± 0.996 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

>>> %%timeit l = list(range(10_000_000))
        ...: l[100_000]
        ...:
28.9 ns ± 0.894 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

순서가 알려지지 않은 배열에서 특정 값을 찾기 위해선 탐색해야합니다. 가장 기본적인 방법은 배열의 모든 항목을 검사해 원하는 값이 있는지 찾아내는 선형 탐색 기법입니다.

```python
def linear_search(needle, array):
    for i, item in enumerate(array):
        if item == needle:
            return i
    return -1
```

이 알고리즘은 최악의 경우 O(n) 의 시간 복잡도를 가지는데, 찾으려는 항목이 배열에 존재하지 않아 모든 항목을 다 검사해야만 하는 경우입니다. 결국 마지막에는 `return -1` 문을 실행하게 됩니다. 이 알고리즘은 `list.index()` 에서 사용하는 것과 동일합니다.

이를 개선하려면 데이터가 메모리에 어떻게 저장되는지를 알거나 데이터를 담은 리스트가 어떤 순서로 나열되어 있는지 이해해야합니다. 예를 들어, Python 에는 **사전(Dictionary)** 과 **셋(Set)** 에 쓰이는 해시 테이블은 원래 순서에 상관없이 독특한 방법으로 O(1) 만에 이 문제를 해결합니다. 만약 데이터가 크기순으로 정렬되어 있다면 시간복잡도를 O(log n) 으로 떨어트리는 방법도 존재합니다.

상수 시간 안에 검색하는 방법이 있으니 이런 방식을 채택할 이유가 없을거 같지만 경우에 따라 O(log n) 이 최선일 때도 있습니다.

## A More Efficient Search 

데이터를 먼저 정렬하면 더 나은 탐색 성능을 얻을 수 있습니다. 사용자 정의 객체를 사용하면 `__eq__` 와 `__lt__` 함수를 이용해 크기를 비교할 수 있습니다.

핵심은 정렬과 탐색 알고리즘입니다. Python 리스트는 정렬 알고리즘을 내장하고 있으며 **팀(Tim)** 정렬을 사용합니다. 팀 정렬은 최적의 경우 O(n) 최악의 경우 O(n log n) 의 시간 복잡도를 가집니다.

리스트를 정렬하고 나면 평균 O(log n) 의 복잡도를 가지는 이진 탐색을 사용하여 항목을 찾습니다.

이진 탐색은 리스트의 가운데 값과 찾고자 하는 값을 비교합니다. 가운데 값이 찾고자 하는 값보다 작다면 값은 리스트의 오른쪽에 있을 것입니다. 이런 식으로 값을 찾을 때까지 리스트를 작게 나누어 탐색합니다. 이렇게 하면 선형 탐색 알고리즘과 달리 일부만 살펴보면 됩니다.

```python
def binary_search(needle, haystack):
    imin, imax = 0, len(haystack)
    while True:
        if imin > imax:
            return -1
        midpoint = (imin + imax) // 2
        if haystack[midpoint] > needle:
            imax = midpoint
        elif haystack[midpoint] < needle:
            imin = midpoint+1
        else:
            return midpoint
```

리스트가 정렬된 상태라면 데이터를 사전으로 바꾸는 것보다 그냥 간단히 이진 탐색으로 데이터를 찾는 편이 더 효과적입니다.

또한 `bisect` 모듈을 이용하면 잘 최적화된 이진 탐색 기법으로 항목을 찾을 수 있을 뿐 아니라 새로운 항목을 추가해도 정렬된 상태를 유지할 수 있습니다. `bisect` 모듈에 있는 새로운 항목을 추가하는 함수가 이런 기능을 제공합니다. 리스트를 항상 정렬된 상태로 유지하면 원하는 항목을 쉽게 찾을 수 있습니다. 추가로 `bisect` 를 사용해 우리가 찾는 원소와 가장 가까운 값을 매우 빠르게 찾을 수 있습니다. 이런 기능은 비슷한 두 데이터셋을 비교할 때 특히 유용합니다.

```python
import bisect
import random

def find_closest(haystack, needle):
    # bisect.bisect_left will return the first value in the haystack
    # that is greater than the needle
    i = bisect.bisect_left(haystack, needle)
    if i == len(haystack):
        return i - 1
    elif haystack[i] == needle:
        return i
    elif i > 0:
        j = i - 1
        # since we know the value is larger than needle (and vice versa for the
        # value at j), we don't need to use absolute values here
        if haystack[i] - needle > needle - haystack[j]:
            return j
    return i

important_numbers = []
for i in range(10):
    new_number = random.randint(0, 1000)
    bisect.insort(important_numbers, new_number)

# important_numbers will already be in order because we inserted new elements
# with bisect.insort
print(important_numbers)
# > [14, 265, 496, 661, 683, 734, 881, 892, 973, 992]

closest_index = find_closest(important_numbers, -250)
print(f"Closest value to -250: {important_numbers[closest_index]}")
# > Closest value to -250: 14

closest_index = find_closest(important_numbers, 500)
print(f"Closest value to 500: {important_numbers[closest_index]}")
# > Closest value to 500: 496

closest_index = find_closest(important_numbers, 1100)
print(f"Closest value to 1100: {important_numbers[closest_index]}")
# > Closest value to 1100: 992
```

이처럼 올바른 자료구조를 선택하고 일관되게 사용하는것은 효율적인 코드를 작성하는 기본 법칙이기도 합니다.

## Lists Versus Tuples

리스트와 튜플의 차이점을 알아보겠습니다.

1. 리스트는 동적인 배열이다. 수정이 가능하며, 저장 용량을 늘리거나 줄일 수 있다.
2. 튜플은 정적인 배열이다. 일단 생성이 되면 배열의 크기뿐 아니라 그 안의 데이터도 변경할 수 없다.
3. 튜플은 파이썬 런타임에서 캐싱하므로 사용할때마다 커널에 메모리 요청을 안해도된다.

튜플은 변치 않는 특정 대상의 여러 속성을 표현하며 리스트는 서로 이질적인 객체들의 모음입니다.

크기와 내용을 변경할 수 있는 리스트와는 다르게 튜플은 그 불변성 덕분에 아주 가벼운 자료구조입니다. 즉, 튜플을 저장하는 데에는 메모리 오버헤드가 크지 않으며 그에 대한 연산도 꽤 명료합니다. 앞으로 배우겠지만 리스트는 변경할 수 있다는 점 때문에 메모리를 더 많이 사용하며 추가적인 연산도 필요합니다.

### Lists as Dynamic Arrays 

리스트는 생성한 후에도 필요할 때마다 내용을 변경할 수 있습니다.


```python
>>> numbers = [5, 8, 1, 3, 2, 6]
>>> numbers[2] = 2*numbers[0]  
>>> numbers
[5, 8, 10, 3, 2, 6]
```

리스트에 새로운 데이터를 추가하면 크기가 커집니다.

```python
>>> len(numbers)
6
>>> numbers.append(42)
>>> numbers
[5, 8, 10, 3, 2, 6, 42]
>>> len(numbers)
7
```

크기가 N 인 꽉찬 리스트에 새로운 항목을 추가하면 원래 담고 있던 N 개와 새로 추가한 항목까지 모두 담기에 충분한 크기의 새로운 리스트를 생성합니다. 하지만 N+1 크기를 할당하는 게 아니라 나중을 위한 여유분으로 N 보다 큰 M 만큼의 메모리를 할당합니다.

크기에 여유를 두는 이유는 리스트에 값을 한 번 추가하면 그 뒤로도 여러 번 더 추가할 확률이 높기 때문에 메모리 할당과 복사 요청 횟수를 줄이기 위함입니다. 메모리 복사는 비용이 많이 들기 때문에 리스트 크기가 계속 증가할 경우 중요한 사항입니다.

`Example 2` 는 Python 3.5 에서 추가 할당이 어떻게 일어나는지 그림으로 표현했습니다.

식으로 나타내면 아래 예제와 같습니다.

```python
M = (N >> 3) + (N < 9 ? 3 : 6)

N 0 1-4 5-8 9-16 17-25 26-35 36-46 … 991-1120
M 0 4 8 16 25 35 46 … 1120
```

> Example 2 - Graph showing how many extra elements are being allocated to a list of a particular size

![image](https://user-images.githubusercontent.com/44635266/74830068-aee83300-5355-11ea-82a4-8e066fa8ae50.png)

리스트에 데이터를 추가하면 여분의 공간을 하나 차지하며, 리스트의 유효 크기 N 이 1 증가하며, N 과 M 이 같아질 때 (N == M) 까지 값이 증가합니다. 두 값이 같아지는 시점이 되면 새로운 데이터를 추가할 여유 공간이 없기 때문에 더 큰 크기의 새로운 리스트를 생성합니다. 새로운 리스트는 위 예제의 공식에 따라 여유 있는 크기로 생성하고 이전 데이터를 새로운 리스트로 복사합니다.

아래 `Example 3` 에 이런 일련의 과정을 표현했습니다. `Example 3` 리스트 1 에 일어나는 다양한 연산을 순서대로 보여줍니다.

```python
l = [1, 2]
for i in range(3, 7):
    l.append(i)
```

> Example 3 - Example of how a list is mutated on multiple appends 

![image](https://user-images.githubusercontent.com/44635266/74830330-3a61c400-5356-11ea-8057-dd46aa44d076.png)

추가로 할당되는 여유 공간은 크지 않지만, 때에 따라 부담이 될 수 있습니다. 이 문제는 크기가 작은 리스트를 여럿 다루거나 아주 큰 리스트를 사용할 때 두드러집니다.

### Tuples As Static Arrays 

리스트와 달리, 튜플은 한 번 생성되면 내용을 바꾸거나 크기를 변경할 수 없습니다.

```python
>>> t = (1,2,3,4)
>>> t[0] = 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

크기를 변경할 순 없어도 두 튜플을 하나의 공간으로 새로운 튜플로 합칠 수는 있습니다.

```python
>>> t1 = (1,2,3,4)
>>> t2 = (5,6,7,8)
>>> t1 + t2
(1, 2, 3, 4, 5, 6, 7, 8)
```

리스트의 `append` 에선 이 과정이 O(1) 만에 이루어지지만 튜플에서는 O(n) 시간이 걸립니다. 여유 공간이 부족할 때만 할당 복사가 일어나는 리스트와 달리, 튜플에서는 새로운 항목을 추가할 때마다 할당과 복사가 일어나기 때문입니다.

튜플은 `append` 와 같이 기존 튜플이 차지하고 있는 메모리 안에 새로운 항목을 추가하는 연산은 지원하지 않는다. 두 튜플을 합치면 항상 새로운 튜플을 위한 메모리를 새로 할당합니다. 크기 변경을 위한 여유 공간을 할당하지 않으면 자원을 더 적게 사용하는 장점이 있씁니다.

튜플이 정적이기 때문에 얻을 수 있는 또 다른 장점으로, Python 이 내부적으로 수행하는 리소스 캐싱이 있습니다. Python 은 GC 를 통해 더 이상 사용하지 않는 변수에 할당된 메모리를 반환합니다. 하지만 크기가 20 이하인 튜플은 즉시 회수되지 않고 나중을 위해 저장해둡니다. 이 말은 같은 크기의 튜플이 나중에 다시 필요해지면 OS 로부터 메모리를 새로 할당받지 않고 기존에 할당해둔 메모리를 재사용한다는 뜻입니다.

위 장점이 튜플의 환상적인 특징 중 하나입니다. OS 를 통하지 않아도 되기 때문에 쉽고 빠르게 튜플을 생성할 수 있습니다. OS 를 거치면 시간이 약간 더 걸립니다. 아래 예제는 리스트 인스턴스를 만드는 것이 튜플 생성에 비해 5.1 배 더 느리다는 사실을 보여줍니다. 이렇게 작은 차이라도 빠른 루프 안에서 누적되면 쉽게 큰 차이로 벌어지게됩니다.

```python
>>> %timeit l = [0,1,2,3,4,5,6,7,8,9]
95 ns ± 1.87 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

>>> %timeit t = (0,1,2,3,4,5,6,7,8,9)
12.5 ns ± 0.199 ns per loop (mean ± std. dev. of 7 runs, 100000000 loops each)
```