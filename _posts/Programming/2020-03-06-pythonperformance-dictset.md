---
title : Python Dictionarys and Sets
tags :
- HashTable
- Set
- Dictionary
- Python
---

*이 포스트는 [High Performance Python](https://github.com/darrenzeng2012/nohtyp/blob/master/High%20Performance%20Python%20-%20Practical%20Performant%20Programming%20for%20Humans%202014.pdf) 를 바탕으로 작성하였습니다.*

셋과 사전은 정해진 내재적 순서가 있지는 않지만, 특정 데이터를 고유하게 참조할 수 있는 별도 객체가 있는 이상적인 자료구조입니다.

참조하는 객체는 일반적으로 문자열이지만 해시가 가능한 타입이라면 어떤것도 상관없습니다. 이때 참조 객체를 **Key**, 데이터를 **Value** 라 합니다.

사전과 셋은 거의 동일하지만 셋은 같은 값을 가지지 않는다는 점만 다릅니다. 쉽게 말해 셋은 유일한 키를 저장하는 자료구조입니다. 이름에서 알 수 있듯이 셋은 집합 연산을 수행할 때 매우 유용합니다.

사전과 셋은 일반적으로 메모리를 많이 사용합니다. 또한 삽입 / 탐색 시간 복잡도가 O(1) 이긴 하지만, 실제 속도는 사용하는 해시 함수에 전적으로 의존합니다. 만일 해시 함수가 느리다면 사전이나 셋의 모든 연산도 마찬가지로 느릴것입니다.

예제로 알아보겠습니다. 전화번호부에 있는 모든 사람의 연락처 정보를 저장하려고 합니다. 리스트를 이용하면 아래와 같이 전화번호와 이름을 연속으로 저장하여 필요한 전화번호를 찾으려면 전체 시스템을 탐색해야합니다.

```python
def find_phonenumber(phonebook, name):
  for n, p in phonebook:
    if n == name:
      return p
  return None

phonebook = [
  ("John Doe", "555-555-5555"),
  ("Albert Einstein", "212-555-5555"),
]
print ("John Doe's phone number is", find_phonenumber(phonebook, "John Doe"))
```

하지만 아래 예제처럼 사전을 이용하면 색인에서 이름을 찾아 전화번호를 바로 얻을 수 있습니다. 전체 데이터를 살펴보는 대신 직접 참조를 통해 필요한 값을 간단하게 가져오는 것입니다.


```python
phonebook = {
  "John Doe": "555-555-5555",
  "Albert Einstein" : "212-555-5555",
}
print ("John Doe's phone number is", phonebook["John Doe"])
```

전화번호부는 두껍기 때문에 O(1) 시간과 리스트가 제공하는 선형 탐색의 O(n) 시간의 차이는 많습니다.

반면 전화번호부에서 이름이 중복되지 않는 사람은 몇 명인지를 알려면 셋을 이용하면 됩니다. 셋은 단순히 유일한 키의 모음입니다. 아래 예제에서 볼 수 잇듯이 리스트를 이용한 방법은 자료구조에서 이름 속성을 분리하기 위해 모든 이름을 비교해야 합니다.

```python
def list_unique_names(phonebook):
  unique_names = []
  for name, phonenumber in phonebook: #
    first_name, last_name = name.split(" ", 1)
    for unique in unique_names: #
      if unique == first_name:
        break
      else:
        unique_names.append(first_name)
  return len(unique_names)

def set_unique_names(phonebook):
  unique_names = set()
  for name, phonenumber in phonebook: #
    first_name, last_name = name.split(" ", 1)
    unique_names.add(first_name) #
  return len(unique_names)

phonebook = [
  ("John Doe", "555-555-5555"),
  ("Albert Einstein", "212-555-5555"),
  ("John Murphey", "202-555-5555"),
  ("Albert Rutherford", "647-555-5555"),
  ("Elaine Bodian", "301-555-5555"),
]

print ("Number of unique names from set method:", set_unique_names(phonebook))
print ("Number of unique names from list method:", list_unique_names(phonebook))
```

셋을 이용한 알고리즘은 내부 루프가 없고 `set.add` 연산은 전화번호부의 크기에 상관없이 O(1) 의 시간 복잡도로 수행합니다. 상수 시간에 수행되지 않는 연산은 전화번호부를 순회하는 루프뿐이므로 최종 알고리즘은 O(n) 의 시간 복잡도를 가집니다.

10,000 개의 항목 중 유일한 이름이 7,422 개인 전화번호부를 각각의 알고리즘을 사용해 돌려보면 O(n) 과 O(n log n) 의 차이가 얼마나 큰지 알 수 있습니다.

```python
>>> %timeit list_unique_names(large_phonebook)
1 loops, best of 3: 2.56 s per loop
>>> %timeit set_unique_names(large_phonebook)
100 loops, best of 3: 9.57 ms per loop
```

셋을 이용한 알고리즘이 270 배 정도 빠릅니다. `phonebook` 의 크기가 커질수록 이 차이는 더 벌어집니다.

## How Do Dictionaries and Sets Work? 

사전과 셋 모두 해시 테이블을 사용해서 O(1) 의 시간 복잡도를 가집니다.

### Inserting and Retrieving 

해시 테이블을 처음 생성하면 배열을 사용할 때처럼 메모리를 먼저 할당합니다. 배열에서는 데이터를 추가하려면 사용하지 않은 메모리 블록을 찾아서 데이터를 추가하고 필요한 경우 크기를 조정했습니다. 해시 테이블에서는 먼저 이 연속적인 메모리에서 데이터를 넣을 위치를 정할 방법을 생각해봐야 합니다.

새로운 데이터의 위치는 그 데이터의 2 가지 속성에 의해 결정됩니다. 하나는 Key 의 해시값이고, 다른 하나는 그 데이터의 Value 를 다른 객체와 비교하는 방법입니다. 데이터를 삽입하면 먼저 Key 를 해시한 후 마스크 처리하여 배열의 색인으로 쓸 수 있는 형태로 만듭니다. 마스크는 해시값이 할당된 메모리 블록의 수보다 작아지도록 조정합니다. 만약 8 개 메모리 블록을 할당했고 해시 값이 28,975 라면, `28975 & 0b111 = 7` 을 블록 색인으로 사용할 수 있습니다. 하지만 사전이 512 개의 메모리 블록을 차지할 정도로 커지면 마스크는 `0b111111111` 이 되어야 하고, 블록 색인은 `28975 & 0b111111111` 이 됩니다.

이제 해당 블록이 사용 중인지 검사하여 블록이 비어있으면 Key 와 Value 를 그 블록에 삽입합니다. 이때 Key 도 함께 저장하여 탐색시 올바른 값을 찾았는지 확인할 수 있습니다. 반대로 해당 블록이 사용중이고 저장된 값이 삽입하려는 값과 같다면 데이터를 저장할 다른 곳을 찾습니다.

이때 새로운 색인을 단순한 선형 검색 함수를 이용해 계산하는데 이를 **프로빙(Probing)** 이라 합니다. Python 의 프로빙 메커니즘은 원래 해시값에서 더 상위의 비트를 활용합니다. 이때 사용한 마스크는 `mask = 0b111 = bin(8-1)` 입니다. 충돌을 피할 수 있도록 이 상위 비트를 사용해 다음 위치를 찾습니다.

새로운 색인을 생성하는 알고리즘은 다양한 선택지가 있습니다. 데이터가 해시 테이블에 균일하게 분포되도록 가능한 모든 색인값을 고루 출력하는 알고리즘이어야 합니다. 해시 테이블에서 데이터가 얼마나 균등하게 분포되어 있는지를 **로드 팩터(load factor)** 라 하며, 해시 함수의 엔트로피와 관련 있습니다. 아래 예제는 CPython 2.7 에서 사용하는 해시 색인의 계산과정을 의사 코드로 표현했습니다.

```python
def index_sequence(key, mask=0b111, PERTURB_SHIFT=5):
  perturb = hash(key) #
  i = perturb & mask
  yield i
  while True:
    i = ((i << 2) + i + perturb + 1)
    perturb >>= PERTURB_SHIFT
    yield i & mask
```

이상의 프로빙 과정은 선형 프로빙의 변형입니다. 선형 프로빙에서는 `i = (5 * i + 1) & mask` 값을 반환하는데, 여기서 i 의 초기값은 Key 의 해시값입니다. 여기서 중요한 점은 해시의 마지막 몇 비트만 사용하고 나머지는 무시한다는 점입니다. 하위 3비트가 같은 항목들을 해싱하면 색인이 같아져 충돌이 일어나는데 Python 은 그 항목의 해시값에서 추가 비트를 더 사용해 이 문제를 회피합니다.

특정 Key 로 Value 를 검색하는 과정도 이와 유사합니다. Key 를 색인으로 변환하고 그 색인의 Value 를 검증합니다. 만약 Key 가 해당 색인에 저장한 기존 Key 와 같으면 해당 값을 반환합니다. 그렇지 않으면 같은 방식으로 새로운 색인을 만들어 일치하는 Key 를 찾거나 빈 블록을 찾을 때까지 이 과정을 반복합니다. 생성한 색인이 빈 블록을 참조한다면 해당 데이터가 해시 테이블에 존재하지 않는다는 점입니다.

아래 `Example 1` 은 해시 테이블에 데이터를 추가하는 과정입니다. 여기선 간단하게 입력의 첫 글자를 사용하는 해시 함수를 만들었습니다. 이 함수는 Python 의 `ord` 함수를 입력해 입력의 첫 글자를 정수로 변환합니다.

> Example 1 - The resulting hash table from inserting with collisions

![image](https://user-images.githubusercontent.com/44635266/74833168-494b7500-535c-11ea-8cd2-7551de4a97a8.png)

키가 `Barcelona` 인 데이터를 삽입하면 충돌이 발생하고 위의 예제의 방식에 따라 새로운 색인을 생성합니다. 이 사전은 아래의 코드를 이용해 생성할 수 있습니다.

```python
class City(str):
  def __hash__(self):
    return ord(self[0])

# We create a dictionary where we assign arbitrary values to cities
data = {
  City("Rome"): 4,
  City("San Francisco"): 3,
  City("New York"): 5,
   City("Barcelona"): 2,
}
```

여기서는 `Barcelona` 와 `Rome` 의 해시가 충돌합니다.

항목이 4개인 사전에서 `mask` 로 `0b111` 을 사용했는데 `Barcelona` 는 `ord("B") & 0b111 = 66 & 0b111 = 0b10000010 & 0b111 = 0b010 = 2` 과정을 거쳐 색인이 2 가 되고 `Rome` 은 `ord("R") & 0b111 = 82 & 0b111 = 0 b1010010 & 0b111 = 0b010 = 2` 의 과정을 거쳐 역시 같은 2를 색인으로 가지기 때문입니다.

### Deletion  

해시 테이블에서 값을 삭제할 때 단순히 해당 메모리 블록을 NULL 로 만드는 방법은 사용할 수 없습니다. 프로빙 시 해시가 충돌했는지를 확인한 값으로 NULL 을 사용하기 때문입니다.

따라서 해당 블록이 비어있음을 나타내는 특수 값을 기록하고 나중에 해시 충돌을 해결하는 과정에서 새로운 값을 저장할 수 있습니다. 해시테이블에 비어있는 슬롯은 나중에 새로운 값이 쓰이거나 해시 테이블의 크기가 변경될 때 삭제됩니다.

### Resizing 

해시 테이블에 항목이 추가됨에 따라 해시 테이블의 크기도 변경되야 합니다. 해시 테이블의 2/3 이하만 채워진다면 충돌 횟수와 공간 활용 측면 모두 적절하다 볼 수 있습니다.

크기를 변경할 때는 충분히 큰 해시 테이블을 할당하고 그 크기에 맞게 마스크를 조정합니다. 그리고 모든 항목을 새로운 해시 테이블로 옮깁니다. 이 과정에서 바뀐 마스크 때문에 색인을 다시 계산하기 때문에 해시 테이블의 크기 변경은 비싼 작업이라고 볼 수 있습니다.

기본적으로 사전, 셋의 최소 크기는 8 입니다. 이 크기는 50,000 까지는 4 배씩 증가하고 그 뒤로는 2 배씩 증가합니다. 즉, 다음과 같은 순서로 크기가 변경됩니다.
$$
8, \; 32, \; 128, \; 512, \; 2048, \; 8192, \; 31768, \; 131072, \; 262144 ...
$$

기억해야 할 점은 해시 테이블에서 데이터가 많이 삭제되면 크기가 줄어듭니다. 하지만 크기 변경은 삽입 연산 중에만 발생합니다.

### Hash Functions and Entropy 

Python 객체는 이미 `__hash__` 와 `__cmp__` 함수를 구현하여 해시가 가능합니다. `int` 나 `float` 같은 산술 타입은 간단하게 그 수의 비트를 기반으로 해시값을 구합니다. 튜플과 문자열은 그 내용을 기반으로 해시값을 구합니다. 반면 리스트는 그 값이 변경될 수 있으므로 해시를 지원하지 않습니다. 리스트의 값은 변경될 수 있기 때문입니다.

사용자 정의 클래스도 기본적으로 해시 함수와 비교 함수가 있습니다. `__hash__` 함수는 내장 함수인 `id` 함수를 이용해 객체의 메모리 위치를 반환합니다. `__cmp__` 연산자는 그 객체의 메모리 위치를 산술 비교합니다.

일반적으로 어떤 클래스의 두 인스턴스는 서로 다르고 해시 테이블 내에 충돌이 발생하지 않으므로 위 내용은 납득이 가능합니다. 하지만 경우에 따라서 셋이나 사전 객체가 원소간의 `id` 차이를 인식하지 않았으면 하는 경우가 있습니다. 다음 클래스 정의를 보겠습니다.

```python
class Point(object):
  def __init__(self, x, y):
    self.x, self.y = x, y
```

만일 `x, y` 값이 동일한 `Point` 객체를 여러 개 생성하면 메모리 주소는 전부 독립적이므로 모두 다른 해시값을 가지게 됩니다. 이 객체들을 모두 하나의 셋에 추가하면, 각각의 항목이 모두 추가됩니다.

```python
>>> p1 = Point(1,1)
>>> p2 = Point(1,1)
>>> set([p1, p2])
set([<__main__.Point at 0x109b95910>])
>>> Point(1,1) in set([p1, p2])
True
```

이 문제는 객체 메모리 주소가 아니라 실제 내용을 기반으로 하는 사용자 정의 해시 함수를 작성하여 해결할 수 있습니다. 해시 함수는 같은 내용의 객체에 대해서는 항상 같은 결과를 반환합니다.

`Point` 클래스를 다음과 같이 변경하여 원하는 결과를 얻을 수 있습니다.

```python
class Point(object):
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __hash__(self):
    return hash((self.x, self.y))

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
```

이를 이용하면 인스턴스화한 객체의 메모리 주소가 아니라 `Point` 객체의 속성으로 사전이나 셋에 필요한 색인을 만들 수 있습니다.

```python
>>> p1 = Point(1,1)
>>> p2 = Point(1,1)
>>> set([p1, p2])
set([<__main__.Point at 0x109b95910>])
>>> Point(1,1) in set([p1, p2])
True
```

사용자 정의 해시 함수는 충돌을 피하기 위해 해시값이 균일하게 분포되도록 신경써야 합니다. 충돌이 잦으면 해시 테이블의 성능에 악영향을 미치게됩니다.

사전에 저장할 값이 5,000 개이고 그 키에 적용할 해시 함수를 작성한다 가정하겠습니다. 사전을 보관할 해시 테이블의 크기는 32,786 이 되므로 해시값 중 하위 15 bit 만 색인 생성에 사용됩니다. 이 크기의 해시 테이블의 마스크는 `bin(32768 - 1) = 0b111111111111111` 입니다.

해시 함수가 해시 값을 얼마나 균일한 분포로 만들어내는지를 해시 함수의 Entropy 라 하며, 다음과 같이 정의합니다.

$$
S = -\sum_ip(i)\cdot \log(p(i))
$$

여기서 $p(i)$ 는 해시 함수가 $i$ 를 출력할 확률입니다. 모든 해시값의 확률이 동일할 때 엔트로피가 최대가 됩니다. 엔트로피 최대가 되는 해시 함수는 최소 충돌을 보장하며 완전 해시 함수라고 합니다.

유한한 모든 사전에서 사용할 수 있는 완벽한 해시 함수는 없습니다. 하지만 저장할 값의 범위와 사전의 크기가 어느 정도인지 미리 알 수 있다면 좋은 선택을 하는데 도움이 됩니다.

예를들어 사전의 키로 두 소문자의 모든 조합('aa', 'ab')을 사용한다면 아래 해시 함수가 괜찮은 선택이 될 것입니다.

```python
def twoletter_hash(key):
  offset = ord('a')
  k1, k2 = key
  return (ord(k2) - offset) + 26 * (ord(k1) - offset)
```

아래 예제는 나쁜 해시 함수와 좋은 해시 함수를 사용한 탐색속도 비교입니다. 엄청나게 많은 차이가 나는걸 볼 수 있습니다.

```python
import string
import timeit

class BadHash(str):
  def __hash__(self):
    return 42

class GoodHash(str):
  def __hash__(self):
    """
    This is a slightly optimized version of twoletter_hash
    """
    return ord(self[1]) + 26 * ord(self[0]) - 2619

baddict = set()
gooddict = set()
for i in string.ascii_lowercase:
  for j in string.ascii_lowercase:
    key = i + j
    baddict.add(BadHash(key))
    gooddict.add(GoodHash(key))

badtime = timeit.repeat(
  "key in baddict",
  setup = "from __main__ import baddict, BadHash; key = BadHash('zz')",
  repeat = 3,
  number = 1000000,
)
goodtime = timeit.repeat(
  "key in gooddict",
  setup = "from __main__ import gooddict, GoodHash; key = GoodHash('zz')",
  repeat = 3,
  number = 1000000,
)

print "Min lookup time for baddict: ", min(badtime)
print "Min lookup time for gooddict: ", min(goodtime)

# Results:
# Min lookup time for baddict: 16.3375990391
# Min lookup time for gooddict: 0.748275995255
```

## Dictionaries and Namespaces 

사전에서 값을 찾는 작업은 빠릅니다. 하지만 불필요한 탐색은 다른 쓸데없는 코드만큼이나 실행속도를 떨어트립니다. 과도한 사전 탐색으로 인해 이런 문제가 불거지는 곳이 Python 의 네임스페이스 관리입니다.

Python 에서 객체를 어디서 찾을지 결정하는 계층이 있습니다. 가장 먼저 모든 지역 변수를 담고 있는 `locals()` 에서 찾습니다. 그 다음 `globals()` 사전에서 찾습니다. 마지막으로 `__builtin__` 객체에서 찾습니다.

여기서 중요한건 `locals()` 와 `globals()` 는 명백한 사전이지만 `__builtin__` 은 기술적으로는 모듈 객체입니다.

다른 범위에 정의된 함수를 호출하는 간단한 예제를 보겠습니다. 

```python
import math
from math import sin

def test1(x):
  """
  >>> %timeit test1(123456)
  1000000 loops, best of 3: 381 ns per loop
  """
  return math.sin(x)

def test2(x):
  """
  >>> %timeit test2(123456)
  1000000 loops, best of 3: 311 ns per loop
  """
  return sin(x)
def test3(x, sin=math.sin):
  """
  >>> %timeit test3(123456)
  1000000 loops, best of 3: 306 ns per loop
  """
  return sin(x)
```

다음은 `dis` 모듈을 사용해 함수를 역어셈블하고 네임스페이스 탐색이 어떻게 이루어지는지 보겠습니다.

```python
>>> dis.dis(test1)
  9           0 LOAD_GLOBAL              0 (math) # Dictionary lookup
              2 LOAD_METHOD              1 (sin) # Dictionary lookup
              4 LOAD_FAST                0 (x) # Local lookup
              6 CALL_METHOD              1
              8 RETURN_VALUE
>>> dis.dis(test2)
 16           0 LOAD_GLOBAL              0 (sin) # Dictionary lookup
              2 LOAD_FAST                0 (x) # Local lookup
              4 CALL_FUNCTION            1
              6 RETURN_VALUE
>>> dis.dis(test3)
 22           0 LOAD_FAST                1 (sin) # Local lookup
              2 LOAD_FAST                0 (x) # Local lookup
              4 CALL_FUNCTION            1
              6 RETURN_VALUE
```

`test1` 은 `math` 라이브러리에서 명시적으로 `sin` 을 호출했습니다. 먼저 `math` 모듈을 로드하고 이 모듈에서 `sin` 함수를 찾았습니다. 2 번의 사전 탐색이 발생했는데, 하나는 `math` 모듈, 다른 하나는 모듈 안에서 `sin` 함수를 찾는 과정입니다.

`test2` 는 `math` 모듈에서 명시적으로 `sin` 함수를 임포트 했는데, 이 `sin` 함수는 전역 네임스페이스에서 직접 접근할 수 있습니다. 즉, `math` 모듈을 탐색하는 과정을 피해주는겁니다.

`test3` 은 `sin` 함수를 키워드 인자로 받고 기본값을 `math` 모듈의 `sin` 함수로 지정했습니다. 여전히 `math` 모듈 안에서 이 함수를 찾아야 하지만, 이는 `test3` 함수를 처음 정의할 때만 필요합니다. 함수가 정의되고나면 `sin` 함수에 대한 참조는 함수 정의부에 기본 키워드인자의 형태로 지역 변수에 저장됩니다.

따라서 사전 탐색이 필요치 않으므로 조금이나마 더 빠르게 동작합니다.

비록 사전 탐색에 걸리는 시간은 아주 짧은 순간이지만, 위 코드가 수백만 번 실행되는 경우 그 차이는 엄청나게되어 성능 저하를 초래할 수 있습니다. 아래 예제는 `sin` 함수에 대한 참조를 지역변수로 선언하여 9.4 % 성능 향상을 보였습니다.

```python
from math import sin

def tight_loop_slow(iterations):
  """
  >>> %timeit tight_loop_slow(10000000)
  1 loops, best of 3: 2.21 s per loop
  """
  result = 0
  for i in xrange(iterations):
    # this call to sin requires a global lookup
    result += sin(i)

def tight_loop_fast(iterations):
  """
  >>> %timeit tight_loop_fast(10000000)
  1 loops, best of 3: 2.02 s per loop
  """
  result = 0
  local_sin = sin
  for i in xrange(iterations):
    # this call to local_sin requires a local lookup
    result += local_sin(i)
```

