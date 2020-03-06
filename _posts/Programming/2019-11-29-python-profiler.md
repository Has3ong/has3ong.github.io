---
title : Python Code Profiler
tags :
- Python
- Profiler
- Memory
- CPU
---

테스트는 피보나치 수열을 이용했습니다.

보통 피보나치는 재귀형식으로 불렀을 때 효율이 엄청나게 안좋아 지는 모습을 보여주는데요. 재귀형식과 반복법을 이용하여 두 코드를 비교하도록 했습니다.

> Test.py

```python
@profile
def Fibonacci_Recursion(val):
    if (val == 1):
        return 0
    elif (val == 2):
        return 1
    else:
        return Fibonacci_Recursion(val - 1) + Fibonacci_Recursion(val - 2)
@profile
def Fibonacci_Repeat(val):
    val_1 = 0
    val_2 = 1
    val_3 = 0
    temp  = 0
 
    if (val == 0):
        return 0
    elif (val == 1):
        return 1
    else:
        for i in range (0, val):
            temp = val_2
            val_2 = val_1 + val_2
            val_1 = temp
 
        return val_2
 
@profile
def TEST():
    recursion = 0
    repeat = 0
 
    recursion = Fibonacci_Recursion(20)
    repeat = Fibonacci_Repeat(20)
 
    print(recursion, repeat)
 
if __name__ == "__main__":
    TEST()
```


## cProfile

Python 은 자체적으로 cProfile이라는 모듈을 내장하고있다. 이 프로파일러는 전체 실행시간과 각각의 함수가 동작하는 시간을 측정해주며, 함수가 몇번이나 호출되었는지의 정보를 출력해준다.

cProfile을 사용할때는 코드의 `@Profile`을 모두 제거한 상태에서 진행했습니다.

```
$ python -m cProfile Test.py                                                                                                                    
(4181, 10946)
         13536 function calls (8 primitive calls) in 0.004 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.004    0.004 Test.py:1(<module>)
        1    0.000    0.000    0.000    0.000 Test.py:11(Fibonacci_Repeat)
  13529/1    0.003    0.000    0.003    0.003 Test.py:3(Fibonacci_Recursion)
        1    0.000    0.000    0.003    0.003 Test.py:30(TEST)
        1    0.000    0.000    0.000    0.000 cProfile.py:5(<module>)
        1    0.000    0.000    0.000    0.000 cProfile.py:66(Profile)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {range}
```

## Line Profiler

함수에 대해서 라인별로 얼마나 시간이 소요되는지를 정리해주는 함수입니다.

`pip3 install line_profiler`

```
$ kernprof -l -v Test.py

4181 10946
Wrote profile results to Test.py lprof
Timer unit 2.77277e-07 s

Total time: 0.015355 s
File: Test.py
Function: Fibonacci_Recursion at line 2

Line #  Hits    Time  Per Hit   % Time  Line Contents
=====================================================
     2                                  @profile
     3                                  def Fibonacci_Recursion(val):
     4  13529 16056.0     1.2     29.0      if (val == 1):
     5   2584  2502.0     1.0      4.5          return 0
     6  10945 11366.0     1.0     20.5      elif (val == 2):
     7   4181  3944.0     0.9      7.1          return 1
     8                                      else:
     9   6764 21510.0     3.2     38.8          return Fibonacci_Recursion(val - 1) + Fibonacci_Recursion(val -2)

Total time: 3.1055e-05 s
File: Test.py
Function: Fibonacci_Repeat at line 10

Line #  Hits    Time  Per Hit   % Time  Line Contents
=====================================================
    10                                  @profile
    11                                  def Fibonacci_Repeat(val):
    12      1     1.0     1.0      0.9      val_1 = 0
    13      1     2.0     2.0      1.8      val_2 = 1
    14      1     1.0     1.0      0.9      val_3 = 0
    15      1     1.0     1.0      0.9      temp = 0
    16             
    17      1     1.0     1.0      0.9      if (val == 0)
    18                                        return 0
    19      1     1.0     1.0      0.9      elif (val ==1)
    20                                        return 1
    21                                      else:
    22     21    36.0     1.7     32.1        for i in range(0, val):
    23     20    20.0     1.0     17.9          temp = val_2
    24     20    25.0     1.2     22.3          val_2 = val_1 + val_2
    25     20    23.0     1.1     20.5          val_1 = temp
    26
    27      1     1.0     1.0      0.9        return val_2
    
Total time: 0.0378974 s
File: Test.py
Function: TEST at line 29

Line #  Hits    Time  Per Hit   % Time  Line Contents
=====================================================
    29                                  @profile
    30                                  def TEST():
    31    1      3.0      3.0      0.0      recursion = 0
    32    1      1.0      1.0      0.0      repeat = 0
    33
    34    1 135767.0 135767.0     99.3      recursion = Fibonacci_Recursion(20)
    35    1    204.0    204.0      0.1      repeat = Fibonacci_Repeat(20)
    36
    37    1    702.0    702.0      0.5      print(recursion, repeat)
```

## Memory Profiler

`Momory Profiler`는 프로세스의 메모리 소비를 모니터링하고 파이썬 프로그램의 메모리 소비를 라인 단위로 분석하는 python 모듈입니다.

`pip3 install memory_profiler`

```
$ python3 -m memory_profiler Test.py                                                                                          
4181 10946
Filename: Test.py

Line #    Mem usage    Increment   Line Contents
================================================
     1   35.836 MiB   35.797 MiB   @profile
     2                             def Fibonacci_Recursion(val):
     3   35.836 MiB    0.012 MiB       if (val == 1):
     4   35.836 MiB    0.012 MiB           return 0
     5   35.836 MiB    0.016 MiB       elif (val == 2):
     6   35.836 MiB    0.000 MiB           return 1
     7                                 else:
     8   35.836 MiB    0.000 MiB           return Fibonacci_Recursion(val - 1) + Fibonacci_Recursion(val - 2)


Filename: Test.py

Line #    Mem usage    Increment   Line Contents
================================================
     9   35.836 MiB   35.836 MiB   @profile
    10                             def Fibonacci_Repeat(val):
    11   35.836 MiB    0.000 MiB       val_1 = 0
    12   35.836 MiB    0.000 MiB       val_2 = 1
    13   35.836 MiB    0.000 MiB       val_3 = 0
    14   35.836 MiB    0.000 MiB       temp  = 0
    15
    16   35.836 MiB    0.000 MiB       if (val == 0):
    17                                     return 0
    18   35.836 MiB    0.000 MiB       elif (val == 1):
    19                                     return 1
    20                                 else:
    21   35.836 MiB    0.000 MiB           for i in range (0, val):
    22   35.836 MiB    0.000 MiB               temp = val_2
    23   35.836 MiB    0.000 MiB               val_2 = val_1 + val_2
    24   35.836 MiB    0.000 MiB               val_1 = temp
    25
    26   35.836 MiB    0.000 MiB           return val_2


Filename: Test.py

Line #    Mem usage    Increment   Line Contents
================================================
    28   35.797 MiB   35.797 MiB   @profile
    29                             def TEST():
    30   35.797 MiB    0.000 MiB       recursion = 0
    31   35.797 MiB    0.000 MiB       repeat = 0
    32
    33   35.836 MiB   35.836 MiB       recursion = Fibonacci_Recursion(20)
    34   35.836 MiB   35.836 MiB       repeat = Fibonacci_Repeat(20)
    35
    36   35.840 MiB    0.004 MiB       print(recursion, repeat)
```