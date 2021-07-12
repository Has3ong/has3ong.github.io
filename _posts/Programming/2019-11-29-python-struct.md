---
title : Python 구조체 구현
tags :
- Struct
- namedtuple
- collections
- Python
categories:
- Programming
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

Python은 C언어에서 사용하는 struct를 사용할 수 없습니다.

그래서 Python 에서는 몇가지 모듈을 이용하여 C 언어에있는 struct를 구현할 수 있는데요. `struct`와 `collection` 모듈을 이용해보겠습니다.

## Struct

https://docs.python.org/2/library/struct.html 사이트에 나와있는 글을 보겠습니다.

이 모듈은 Python 값과 Python 문자열로 표시되는 C 구조체 사이의 변환을 수행합니다. 파일이나 네트워크 연결에서 저장된 이진 데이터를 처리하는 데 사용할 수 있습니다. C 구조체의 레이아웃과 파이썬 값과의 변환에 대한 간단한 설명으로 형식 문자열을 사용합니다.

### Byte Order, Size, and Alignment

|Chracter|Byte order|Size|Alignment|
|:------:|:--------:|:--:|:-------:|
|@|native|native|native|
|=|native|standard|none|
|<|little-endian|standard|none|
|>|big-endian|standard|none|
|!|network(=big -endian)|standard|none|

### Character Format

|Format|C Type|Python Type|Standard Size|Notes|
|:----:|:----:|:---------:|:-----------:|:---:|
|x|pad byte|no value|/|/|
|c|char|string of length 1|1|/|
|b|signed char|interger|1|(3)|
|B|unsigned char|integer|1|(3)|
|?|_Bool|bool|1|(1)|
|h|short|integer|2|(3)|
|H|iunsigned short|integer|2|(3)|
|i|int|integer|4|(3)|
|I|unsigned int|integer|4|(3)|
|l|long|integer|4|(3)|
|L|unsigned long|integer|4|(3)|
|q|long long|integer|8|(2), (3)|
|f|float|float|4|(4)|
|d|double|float|8|(4)|
|s|char[]|string|/|/|
|p|char[]|string|/|/|

Notes 에 대한 정확한 설명은 찾지 못했습니다. 추후 알게되면 업데이트 하겠습니다.

> Examples

**Pack, Little Endian, Big Endian**

```python
import struct

var = struct.pack('iii', 1, 2, 3)
littleVar = struct.pack('<iii', 1, 2, 3)
BigVar = struct.pack('>iii', 1, 2, 3)

print(var)
print(littleVar)
print(BigVar)
```

**Result**

생각한 결과대로 나온것을 확인할 수 있습니다. 그리고 default 값으로는 리틀엔디언이네요.

```
b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03'
```

`\x01\x00\x00\x00` -> 1

`\x02\x00\x00\x00` -> 2

`\x03\x00\x00\x00` -> 3

**UnPack**

```python
import struct
 
var = struct.pack('iii', 1, 2, 3)
unpackvar = struct.unpack('iii', var)
print(unpackvar)
print(type(unpackvar))
 
print(struct.calcsize('iii'))
```

**Result**

```
(1, 2, 3)
<class 'tuple'>
12
```

## Collection

앞전에 `struct` 모듈을 이용했습니다. 요번에는 `collection` 모듈에 있는 `namedtuple` 이용해볼게요

https://docs.python.org/3/library/collections.html#collections.namedtuple 사이트에 나와있는 글을 보겠습니다.

240/5000
`namedtuples`는 `tuple`의 각 위치에 의미를 부여하고 읽기 쉬운 자체 문서화 코드를 허용합니다. 정규 `tuple`이 사용되는 모든 곳에서 사용할 수 있으며 위치 색인 대신 이름으로 필드에 액세스하는 기능을 추가했다고 합니다.

간단한 예제로 사용해볼게요.

> Examples

```python
import collections
 
Person = collections.namedtuple('Person', 'name age job')
print(type(Person))
 
p1 = Person(name='Chul-Soo', age=29, job='Doctor')
print(p1)
 
p2 = Person('Young-Hee', 18 , 'Student')
print(p2.name)
 
for i in [p1, p2]:
    print('Name is : %s, Age is : %d, Job is : %s' % i)
```

**Result**

```
<class 'type'>
Person(name='Chul-Soo', age=29, job='Doctor')
Young-Hee
Name is : Chul-Soo, Age is : 29, Job is : Doctor
Name is : Young-Hee, Age is : 18, Job is : Student
```

`namedtuple` docs에서 지원하는 예제를 가지고 사용해보겠습니다. 오역, 의역이 있을 수 있으니 참고해주시기 바랍니다.....

**`classmethod somenamedtuple._make(iterable)`**

`sequence` 또는 `iterable`한 객체를 이용하여 새로운 인스턴스를 만들어 줍니다.

```
>>> t = [11, 22]
>>> Point._make(t)
Point(x=11, y=22)
```

**`somenamedtuple._asdict()`**

필드의 이름과 값을 이용하여 `dict` 형태로 반환해 줍니다.

```
>>> p = Point(x=11, y=22)
>>> p._asdict()
{'x': 11, 'y': 22}
```

**`somenamedtuple._replace(**kwargs)`**

`namedtuple` 에 특정한 필드와 값에 새로운 값을 대입하여 새로운 인스턴스를 만들어 줍니다.

```
>>> p = Point(x=11, y=22)
>>> p._replace(x=33)
Point(x=33, y=22)

>>> for partnum, record in inventory.items():
...     inventory[partnum] = record._replace(price=newprices[partnum], timestamp=time.now())
```

**`somenamedtuple._fields`**

기존에 존재하는 `namedtuple`에 필드들을 이용하여 새로운 `namedtuple` 을 만들어 줍니다.

```
>>> p._fields            # view the field names
('x', 'y')

>>> Color = namedtuple('Color', 'red green blue')
>>> Pixel = namedtuple('Pixel', Point._fields + Color._fields)
>>> Pixel(11, 22, 128, 255, 0)
Pixel(x=11, y=22, red=128, green=255, blue=0)
```