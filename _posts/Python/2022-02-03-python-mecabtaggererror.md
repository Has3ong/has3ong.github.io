---
title:  "Python3 Install Mecab NameError: name 'Tagger' is not defined` Solution"
excerpt: "Python3 Install Mecab NameError: name 'Tagger' is not defined` Solution"
categories:
  - Programming
tags:
  - Programming
  - Mecab
  - Konlpy
  - Python
toc: true
#toc_min: 1
#toc_max: 3
toc_sticky: true
toc_label: "On This Page"
author_profile: false
---

### 설치 환경

* Python 3.8.3
* macOs Monterey 12.2
* konlpy 0.6.0
* JPype1 1.3.0

### Konlpy Mecab 설치하기

Konlpy 홈페이지에 가서 설치문서를 보면 Mac 환경에서 아래와 같이 알려줍니다.

1. Install KoNLPy

```
$ python3 -m pip install --upgrade pip
$ python3 -m pip install konlpy        # Python 3.x
```

2. Install MeCab (optional)

```
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

하지만 홈페이지에서 알려주는것과 다르게 설치하는게 더 효과적입니다. 수동으로 Mecab 관련 파일을 3가지 설치해주면 됩니다.

* mecab-ko
* mecab-dic
* mecab-python

https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/ 에 자세히 나와있는데 정리해서 작성해드리겠습니다.

1. mecab-ko 설치

```bash
$ cd /tmp
$ sudo wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
$ sudo tar xvf mecab-0.996-ko-0.9.2.tar.gz

$ cd /tmp/mecab-0.996-ko-0.9.2
$ sudo ./configure
$ sudo make check
$ sudo make install
```

2. mecab-dic 설치

```bash
$ cd /tmp
$ wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
$ tar zxvf mecab-ko-dic-2.1.1-20180720.tar.gz

$ cd /tmp/mecab-ko-dic-2.1.1-20180720
$ sudo ./autogen.sh
$ sudo ./configure
$ sudo make
$ sudo make install
```

3. mecab-python 설치

```bash
$ cd /tmp
$ git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
$ cd mecab-python-0.996
$ python3 setup.py build
$ python3 setup.py install
```

위와같이 설치를 마무리 한 후 아래를 입력했을 때 다음과 같은 에러가 발생한 경우에는 `pip`를 이용해서 `mecab-python3`를 설치합니다.

```python
>>> from konlpy.tag import Mecab
>>> mecab = Mecab()

Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/konlpy/tag/_mecab.py", line 107, in __init__
    self.tagger = Tagger('-d %s' % dicpath)
NameError: name 'Tagger' is not defined
```

```bash
$ pip3 install mecab-python3
```

설치 후 실행결과.

```python
Python 3.8.3 (v3.8.3:6f8c8320e9, May 13 2020, 16:29:34)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from konlpy.tag import Mecab
>>> a = Mecab()
>>> a.pos("안녕하세요")
[('안녕', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF')]
```

편안

> 참고자료

* https://github.com/konlpy/konlpy/issues/187
* https://konlpy.org/en/latest/install/
* https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/