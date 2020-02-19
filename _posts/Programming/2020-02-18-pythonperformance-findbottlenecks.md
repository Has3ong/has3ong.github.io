---
title : Python Profiling to Find Bottlenecks
tags :
- Profile
- Python
---

*이 포스트는 [High Performance Python](https://github.com/darrenzeng2012/nohtyp/blob/master/High%20Performance%20Python%20-%20Practical%20Performant%20Programming%20for%20Humans%202014.pdf) 를 바탕으로 작성하였습니다.*

프로파일링을 해보면 병목 지점을 찾을 수 있기 때문에 최소한의 노력으로 성능을 최대한 끌어 올릴 수 있습니다. 큰 수고를 들이지 않고 속도를 크게 향상시키고 자원을 적게 사용하면서, 실용적인 측면에서 코드가 충분히 빠르고 유연한 것을 목표로 삼스빈다.

CPU 뿐만 아니라 측정 가능한 자원은 모두 프로파일링 할 수 있습니다.

## Profiling Efficiently 

프로파일링의 첫 번째 목표는 시스템의 어느 부분이 느린지, 어디서 RAM 을 많이 쓰고 있는지, 디스크나 네트워크의 I/O 를 과도하게 발생시키는 부분이 어디인지 확인하는 것입니다.

프로파일링하면 평소보다 10 ~ 100 배 까지 실행 속도가 느려지는데, 최대한 실제 상황과 유사한 조건에서 검사하고 싶으면 검사할 부분만 따로 떼어내서 검사하도록 하는편이 좋습니다.

비선형적인 특성이 있어 결과를 쉽게 예측할 수 없으며, RAM 과 CPU 자원을 많이 잡아먹는 쥘리아 집합을 이용하여 분석해보겠습니다.

## Introducing the Julia Set 

**쥘리아 집합(Julia Set)** 은 CPU 를 많이 사용하는 함수 입니다. 쥘리아 집합은 복잡한 그림을 생성하는 프랙탈을 말합니다.

복소수 c 가 -0.62772-0.42193j 일때 쥘리아 집합 그래프인 `Example 1` 과 `Example 3` 을 그리는 코드를 분석하겠습니다. 쥘리아 집합의 각 픽셀은 독립적으로 계산되는데, 각 점은 데이터를 공유하지 않으므로 완전하게 병렬로 계산할 수 있습니다.

> Example 1 - Julia set plot with a false grayscale to highlight detail

![image](https://user-images.githubusercontent.com/44635266/74344011-4d711300-4def-11ea-9cc9-feaebae6ec7a.png)

c 값을 다르게 하면 다른 그림을 얻을 수 있습니다. 우리가 선택한 지점은 빠르게 계산되는 부분과 느리게 계산되는 부분이 있어 우리가 해볼 분석에 적합합니다.

이 문제의 흥미로운 점은 각 픽셀을 계산하는 데 몇번이나 반복되는지 가늠하기 어려운 루프를 사용합니다. 매 반복마다 이 좌푯값이 무한 루프에 빠지는지 인력에 의해 끌어당겨지는지 검사합니다. 반복 횟수가 적을수록 어두운 색을 띠고 반복이 거듭될 수록 밝은 색을 띕니다. 하얀색 영역은 계산하기 더 복잡하며, 때문에 생성되는 시간이 오래 걸립니다.

이제 검사할 z 좌표의 집합을 정의하겠습니다. 이 함수는 복소수 z 의 제곱에 c 를 더한 값을 계산합니다.

$$f(z) = z^2 + C$$

z 의 절대값이 2보다 작으면 이 함수를 계속 반복합니다. 2 이상이면 루프를 빠져나가면서 이 좌표에 대해서 수행한 반복 횟수를 기록합니다. 종료 조건을 계속 충족하지 못하면 maxiter 만큼 반복한 후에 루프를 빠져나옵니다. 이 z 결과 값은 나중에 복소평면 상에 픽셀을 그리는 용도로 사용합니다.

의사코드는 아래와 같습니다.

```python
for z in coordinates:
  for iteration in range(maxiter): # limited iterations per point
    if abs(z) < 2.0: # has the escape condition been broken?
      z = z*z + c
    else:
      break
  # store the iteration count for each z and draw later
```

먼저 그리게 될 쥘리아 집합 그래프의 왼쪽 위 코너 좌표를 -1.8-1.8j 로 하겠습니다. 값을 계산하기 전에 `abs(z) < 2` 인 조건을 만족해야 합니다.

```python
z = -1.8-1.8j
print abs(z)

2.54558441227
```

왼쪽 위 좌표는 만족하지 못해서 루프는 한 번도 실행되지 않고 종료됩니다. 따라서 z 값을 갱신하지 않으며, 이 좌표값은 0 입니다.

원짐인 `z = 0 + 0j` 의 경우를 보겠습니다.

```python
c = -0.62772-0.42193j
z = 0+0j
for n in range(9):
  z = z*z + c
  print "{}: z={:33}, abs(z)={:0.2f}, c={}".format(n, z, abs(z), c)
  
0: z= (-0.62772-0.42193j), abs(z)=0.76, c=(-0.62772-0.42193j)
1: z= (-0.4117125265+0.1077777992j), abs(z)=0.43, c=(-0.62772-0.42193j)
2: z=(-0.469828849523-0.510676940018j), abs(z)=0.69, c=(-0.62772-0.42193j)
3: z=(-0.667771789222+0.057931518414j), abs(z)=0.67, c=(-0.62772-0.42193j)
4: z=(-0.185156898345-0.499300067407j), abs(z)=0.53, c=(-0.62772-0.42193j)
5: z=(-0.842737480308-0.237032296351j), abs(z)=0.88, c=(-0.62772-0.42193j)
6: z=(0.026302151203-0.0224179996428j), abs(z)=0.03, c=(-0.62772-0.42193j)
7: z= (-0.62753076355-0.423109283233j), abs(z)=0.76, c=(-0.62772-0.42193j)
8: z=(-0.412946606356+0.109098183144j), abs(z)=0.43, c=(-0.62772-0.42193j)
```

조건을 만족하여 계속 z 값을 갱신합니다. 이 좌표는 300 번을 반복해도 검사 조건을 만족하여 언제 끝날지 알 수 없어 무한 루프에 빠질 수 있습니다. 최대 반복횟수(maxiter) 를 설정해 무한 루프를 방지하겠습니다.

`Example 2` 는 위 계산을 50 번 반복한 그래프 입니다. `0+0j` 값이 매 8회마다 반복됨을 알 수 있습니다. 7회 까지는 편차를 가지고 있으므로, 무한 루프에 빠질지 아니면 반복이 끝날지 알 수 없습니다. 점선으로 표시된 cutoff 는 +2 경계를 나타냅니다.

> Example 2 - Two coordinate examples evolving for the Julia set

![image](https://user-images.githubusercontent.com/44635266/74430863-10655900-4ea1-11ea-9d1e-6c5165386f2f.png)

`-0.82+0j` 에 대한 값은 그림에서 보듯 9 번 반복후에 경계값인 +2 를 넘어서고 루프를 빠져나옵니다.

## Calculating the Full Julia Set 

이제 쥘리아 집합을 생성하는 코드를 살펴보겠습니다. 첫 번째 프로파일링을 위해 `time` 모듈을 임포트하고 몇 가지 좌표 상수를 정의하겠습니다.

```python
"""Julia set generator without optional PIL-based image drawing"""
import time

# area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193
```

그래프를 그리기 위해 입력 데이터를 담을 두 리스트 `zs(복소수 z축)` 와 `cs(복소수 초기 조건)` 을 생성합니다. `cs` 를 단일 `c` 값으로 최적화 할 수 있습니다. 두 벌의 입력 리스트를 생성하는 이유는 나중에 RAM 사용량을 프로파일링 할 때 납득할 만한 데이터를 얻기 위함입니다.

`zs` 리스트와 `cs` 리스트를 생성하기 위해 각 `z` 좌표를 알아야 합니다. 아래 예제에서 `xcoord` 와 `ycoord` 를 이용하여 이 좌표를 만들고 `x_step` 과 `y_step` 을 지정합니다. 약간 번잡해 보일 수 있는 이 과정은 numpy 나 다른 파이선 환경으로 코드를 포팅할 때 명확한 디버깅에 도움을 줍니다.

```python
def calc_pure_python(desired_width, max_iterations):
  """Create a list of complex coordinates (zs) and complex parameters (cs), build Julia set, and display"""
  x_step = (float(x2 - x1) / float(desired_width))
  y_step = (float(y1 - y2) / float(desired_width))
  x = []
  y = []
  ycoord = y2
  
  while ycoord > y1:
    y.append(ycoord)
    ycoord += y_step
  xcoord = x1
  
  while xcoord < x2:
    x.append(xcoord)
    xcoord += x_step
  # Build a list of coordinates and the initial condition for each cell.
  # Note that our initial condition is a constant and could easily be removed;
  # we use it to simulate a real-world scenario with several inputs to
  # our function.
  zs = []
  cs = []
  
  for ycoord in y:
    for xcoord in x:
      zs.append(complex(xcoord, ycoord))
      cs.append(complex(c_real, c_imag))
      
  print "Length of x:", len(x)
  print "Total elements:", len(zs)
  
  start_time = time.time()
  output = calculate_z_serial_purepython(max_iterations, zs, cs)
  end_time = time.time()
  secs = end_time - start_time
  print calculate_z_serial_purepython.__name__ + " took", secs, "seconds"
  
  # This sum is expected for a 1000^2 grid with 300 iterations.
  # It catches minor errors we might introduce when we're
  # working on a fixed set of inputs.
  assert sum(output) == 33219980
```

`zs` 와 `cs` 리스트를 만들어서 해당 리스트의 크기에 관한 정보를 담고 `output` 리스트에 `calculate_z_serial_purepython` 함수에서 계산한 값을 저장합니다. 마지막으로 `output` 리스트에 들어 있는 값들을 모두 더해 그 값이 기대한 값과 같은지 검사합니다.

코드는 **결정적(deterministic)** 이므로, 계산된 값을 모두 더해서 함수가 기대하는 대로 잘 작동하는지 확인할 수 있습니다. 예컨대 수치 코드를 바꿀 때면 알고리즘 논리를 깨지 않는지 확인하는게 중요합니다.

다음 예제에서는 앞서 논의했던 알고리즘을 구현하는 `calculate_z_serial_purepython` 함수를 정의하겠습니다.

```python
def calculate_z_serial_purepython(maxiter, zs, cs):
  """Calculate output list using Julia update rule"""
  output = [0] * len(zs)
  for i in range(len(zs)):
    n = 0
    z = zs[i]
    c = cs[i]
    while abs(z) < 2 and n < maxiter:
      z = z * z + c
      n += 1
    output[i] = n
  return output
```

이제 계산 루틴을 호출하겠습니다.

```python
if __name__ == "__main__":
  # Calculate the Julia set using a pure Python solution with
  # reasonable defaults for a laptop
  calc_pure_python(desired_width=1000, max_iterations=300)
```

위 코드를 실행하면 문제의 복잡도에 관한 결과를 얻을 수 있습니다.

```python
# running the above produces:
Length of x: 1000
Total elements: 1000000
calculate_z_serial_purepython took 12.3479790688 seconds
```

`Example 1` 에서는 반전된 회색조 그래프에서 고대비 색상은 함수의 어떤 부분이 빠르고 느리게 결정되는지 보여줍니다. `Example 3` 에선 색상을 더 단순화하여 검은 부분은 계산이 빠르고 하얀 부분은 계산이 오래 걸렸음을 나타냅니다.

동일한 데이터에 대해 2 가지 다른 표현을 통해 **linear mapping** 에서는 상세 내용이 많이 누락됨을 확인할 수 있습니다.

> Example 3 - Julia plot example using a pure grayscale

![image](https://user-images.githubusercontent.com/44635266/74433037-fc225b80-4ea2-11ea-9b4a-b78506a8a2b7.png)
 
## Simple Approaches to Timing—print and a Decorator 

위 예제에서는 코드의 곳곳에 `print` 문을 추가해서 실행 결과를 살펴봤습니다. 실행시간은 약간의 편차가 있습니다. 코드의 실행 시간을 반복 측정하여 정규분포도를 그려야 코드의 개선 정도를 정확하게 측정할 수 있습니다.

코드를 실행하는 동안 네트워크를 사용하거나 디스크와 RAM 에 접근하여 다른 작업이 돌고 있으면 실행 시간에 편차에 영향을 줄 수 있습니다.

디버깅과 프로파일링에서 `print` 문은 가장 흔한 방법입니다. 하지만, 코드가 금방 더럽혀지고, 작업이 끝난 후 정리하지 않으면 표준 출력을 모조리 잡아먹을것입니다.

조금 더 깨끗한 방법으로 데코레이터가 있습니다. 여기서는 시간을 측정하고 싶은 함수 위에 코드를 한 줄 추가하겠습니다.

아래 예제에서는 함수를 인자로 받는 `timefn` 이라는 함수를 새로 정의하겠습니다. 내부에서 새로 정의한 `measure_time` 은 가변길이 인자인 `*args` 와 키워드 인자인 `**kwargs` 를 받아, 실행하는 `fn` 함수로 넘겨줍니다. `fn` 함수를 호출하는 부분은 `time.time()` 으로 감사서 시간을 구하고 `fn.func_name` 과 함께 소요된 시간을 출력합니다.

이 데코레이터로 인한 오버헤드는 작지만 `fn` 을 많이 호출하면 느려진 성능을 체감할 수 있습니다. `@wraps(fn)` 을 사용해 데코레이터로 넘어온 함수의 이름과 **docstring** 을 호출하는 함수에서 확인할 수 있도록 했습니다.

```python
from functools import wraps

def timefn(fn):
  @wraps(fn)
  def measure_time(*args, **kwargs):
    t1 = time.time()
    result = fn(*args, **kwargs)
    t2 = time.time()
    print ("@timefn:" + fn.func_name + " took " + str(t2 - t1) + " seconds")
    return result
  return measure_time
  
@timefn
def calculate_z_serial_purepython(maxiter, zs, cs):
 ...
```

기존의 `print` 문은 그대로 둔채 이 코들=드를 실행하면 데코레이터를 사용한 측정값이 `calc_pure_python` 함수에서 측정한 값보다 살짝 짧음을 확인할 수 있습니다. 이는 함수 호출에 의한 오버헤드입니다.

```shell
Length of x: 1000
Total elements: 1000000
@timefn:calculate_z_serial_purepython took 12.2218790054 seconds
calculate_z_serial_purepython took 12.2219250043 seconds
```

위에서 작상한 함수의 실행속도를 측정하는 다른 방법으로 `timeit` 모듈을 사용할 수 있습니다.

```shell
$ python -m timeit -n 5 -r 5 -s "import julia1"
 "julia1.calc_pure_python(desired_width=1000, max_iterations=300)"
```

`-s` 를 사용해서 모듈을 임포트합니다. `-r` 은 반복 횟수를 나타내고 `-n` 는 각 검사에서의 평균을 구합니다. 결과로는 전체 반복 중 가장 빠른 값을 출력합니다.

```shell
5 loops, best of 5: 13.1 sec per loop
```

평범한 컴퓨터에서 확인할 수 있는 CPU 부하의 편차에 대해 생각해볼만합니다. `Example 4` 는 코드의 소요 시간동안 코어의 사용률을 확인할 수 있습니다.

하나의 코어는 갑자기 사용률이 치솟지만 다른 코어는 모두 일상적인 작업을 수행하는것을 확인할 수 있습니다.

> Example 4 - System Monitor on Ubuntu showing variation in background CPU usage while we time our function

![image](https://user-images.githubusercontent.com/44635266/74434126-18bf9300-4ea5-11ea-9b63-d945ef9b55f2.png)

## Simple Timing Using the Unix time Command 

유닉스 시스템에 포함된 표준 시스템 유틸리티를 사용해보겠습니다. 다음 명령은 프로그램의 실행 시간에 대해 다양한 정보를 제공하며, 코드 내부 구조에 대해서는 전혀 신경 쓰지 않는다.

```shell
$ /usr/bin/time -p python julia1_nopil.py
Length of x: 1000
Total elements: 1000000
calculate_z_serial_purepython took 12.7298331261 seconds
real 13.46
user 13.40
sys 0.04
```

*/usr/bin/time* 이라 명시해서 쉘에 포함된 단순한 버전의 `time` 을 실행하지 않고 시스템의 `time` 명령어를 사용했음에 주목합니다. `time --verbose` 를 실행해서 에러가 발생하면 시스템 명령어가 아닌 쉘에 포함된 `time` 을 실행했을 가능성이 높습니다.

`-p` 옵션을 주면 다음과 같은 3 가지 결과를 얻을 수 있습니다.

* real 항목은 경과된 시간을 기록한다.
* user 항목은 CPU 가 커널 함수 외 작업을 처리하느라 소비한 시간을 기록한다.
* sys 항목은 커널 함수를 수행하는 데 소비한 시간을 기록한다.

`user` 와 `sys` 항목을 추가하여 CPU 에서 시간을 어떻게 사용했는지를 알아볼 수 있습니다.

`time` 이 유용한 이유는 Python 을 필요하지 않기 때문입니다. `time` 명령어를 이용하면 python 실행파일이 시작되는 데 걸리는 시간도 측정할 수 있습니다. 장시간 실행되는 단일 프로세스를 사용하지 않고 초기에 많은 프로세스를 생성한다면 유의미한 시간입니다. 실행 시간이 짧은 스크립트에서는 초기 구동시간이 전체 시간에서 차지하는 비중이 높으므로 `time` 을 사용하면 좀 더 유용한 측정을 할 수 있습니다.

`--verbose` 플래그를 넘기면 더 자세한 결과를 확인할 수 있습니다.

```shell
$ /usr/bin/time --verbose python julia1_nopil.py
Length of x: 1000
Total elements: 1000000
calculate_z_serial_purepython took 12.3145110607 seconds
    Command being timed: "python julia1_nopil.py"
    User time (seconds): 13.46
    System time (seconds): 0.05
    Percent of CPU this job got: 99%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 0:13.53
    Average shared text size (kbytes): 0
    Average unshared data size (kbytes): 0
    Average stack size (kbytes): 0
    Average total size (kbytes): 0
    Maximum resident set size (kbytes): 131952
    Average resident set size (kbytes): 0
    Major (requiring I/O) page faults: 0
    Minor (reclaiming a frame) page faults: 58974
    Voluntary context switches: 3
    Involuntary context switches: 26
    Swaps: 0
    File system inputs: 0
    File system outputs: 1968
    Socket messages sent: 0
    Socket messages received: 0
    Signals delivered: 0
    Page size (bytes): 4096
    Exit status: 0
```

위 지표에서 가장 눈여겨봐야 하는 항목은 `Major (requiring I/O) page faults` 항목입니다. 이 항목은 운영체제가 RAM 에서 필요한 데이터를 찾을 수 없어 디스크에서 페이지를 불러 왔는지의 여부를 나타냅니다. 이는 속도를 느리게 하는 원인입니다.

## Using the cProfile Module 

cProfile 은 표준 라이브러리에 내장된 프로파일링 도구입니다. 이는 큰 오버헤드를 유발하지만 그만큼 더 많은 정보를 제공합니다.

cProfile 은 표준 라이브러리가 제공하는 3 가지 프로파일러 중 하나로, 다른 두 가지는 hotshot / profile 입니다.

cProfile 모듈을 사용하여 코드를 실행해보겠습니다. cProfile 의 `-s cumulative` 옵션은 각 함수에서 소비한 누적 시간순으로 정렬되어 어떤 함수가 더 느린지 쉽게 확인할 수 있습니다. cProfile 의 출력 결과는 코드의 `print` 문이 모두 출력된 뒤에 화면에 출력합니다.

```shell
$ python -m cProfile -s cumulative julia1_nopil.py

calculate_z_serial_purepython took 9.342324018478394 seconds
         36222239 function calls (36222238 primitive calls) in 10.050 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      2/1    0.000    0.000   10.050   10.050 {built-in method builtins.exec}
        1    0.030    0.030   10.050   10.050 kakao.py:1(<module>)
        1    0.540    0.540   10.019   10.019 kakao.py:9(calc_pure_python)
        1    7.324    7.324    9.342    9.342 kakao.py:51(calculate_z_serial_purepython)
 34219980    2.019    0.000    2.019    0.000 {built-in method builtins.abs}
  2002000    0.126    0.000    0.126    0.000 {method 'append' of 'list' objects}
        1    0.011    0.011    0.011    0.011 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:978(_find_and_load)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:663(_load_unlocked)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:722(exec_module)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:793(get_code)
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        3    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:74(_path_stat)
        5    0.000    0.000    0.000    0.000 {built-in method posix.stat}
...
```

누적 소비 시간으로 정렬하면 실행 시간을 주로 소비하는 곳이 어딘지 쉽게 확인할 수 있습니다.

cProfile 의 결과는 부모 함수에 따라 정렬되지 않으며 실행된 코드 블록 안의 모든 함수가 소비한 시간을 요약해 보여줍니다. 함수 안의 각 줄에 대한 정보가 아닌 함수 호출 자체에 대한 정보만 얻을 수 있으므로, cProfile 로 코드의 각 줄에서 일어난 일을 알아내기란 매우 어렵습니다.

`calculate_z_serial_purepython` 함수에는 `{abs}` 와 `{range}` 두 함수 호출에 대략 2.1 초를 소비했음을 알 수 있다. 그리고 `calculate_z_serial_purepython` 함수는 10.5 초를 소비했습니다.

프로파일링 결과의 마지막 줄은 cProfile 의 전신이라 볼 수 있는 `lsprof` 에서 출력한 것입니다.

cProfile 의 결과를 더 세밀하게 살펴보려면 통계 파일을 생성한 뒤 Python 으로 분석할 수 있습니다.

```shell
$ python -m cProfile -o profile.stats julia1.py
```

통계 파일을 불러들이면 앞서 살펴본 출력과 동일한 결과를 확인할 수 있습니다.

```shell
In [1]: import pstats
In [2]: p = pstats.Stats("profile.stats")
In [3]: p.sort_stats("cumulative")
Out[3]: <pstats.Stats instance at 0x177dcf8>
In [4]: p.print_stats()

Sun Feb 16 23:40:48 2020    profile.stats

         36222239 function calls (36222238 primitive calls) in 10.302 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      2/1    0.000    0.000   10.302   10.302 {built-in method builtins.exec}
        1    0.029    0.029   10.302   10.302 kakao.py:2(<module>)
        1    0.551    0.551   10.272   10.272 kakao.py:10(calc_pure_python)
        1    7.519    7.519    9.585    9.585 kakao.py:52(calculate_z_serial_purepython)
 34219980    2.066    0.000    2.066    0.000 {built-in method builtins.abs}
  2002000    0.128    0.000    0.128    0.000 {method 'append' of 'list' objects}
        1    0.008    0.008    0.008    0.008 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:978(_find_and_load)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:663(_load_unlocked)
```

프로파일 중인 함수를 추적하기 위해 해당함수를 **호출한 측(caller)** 의 정보를 출력해보겠습니다.

```shell
In [5]: p.print_callers()

   Ordered by: cumulative time

Function                                                                                                       was called by...
                                                                                                                   ncalls  tottime  cumtime
{built-in method builtins.exec}                                                                                <-       1    0.000    0.000  <frozen importlib._bootstrap>:211(_call_with_frames_removed)
kakao.py:2(<module>)                                                                                           <-       1    0.029   10.302  {built-in method builtins.exec}
kakao.py:10(calc_pure_python)                                                                                  <-       1    0.551   10.272  kakao.py:2(<module>)
kakao.py:52(calculate_z_serial_purepython)                                                                     <-       1    7.519    9.585  kakao.py:10(calc_pure_python)
{built-in method builtins.abs}                                                                                 <- 34219980    2.066    2.066  kakao.py:52(calculate_z_serial_purepython)
{method 'append' of 'list' objects}                                                                            <- 2002000    0.128    0.128  kakao.py:10(calc_pure_python)
{built-in method builtins.sum}                                                                                 <-       1    0.008    0.008  kakao.py:10(calc_pure_python)
<frozen importlib._bootstrap>:978(_find_and_load)                                                              <-       1    0.000    0.000  kakao.py:2(<module>)
<frozen importlib._bootstrap>:948(_find_and_load_unlocked)                                                     <-       1    0.000    0.000  <frozen importlib._bootstrap>:978(_find_and_load)
<frozen importlib._bootstrap>:663(_load_unlocked)                                                              <-       1    0.000    0.000  <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
<frozen importlib._bootstrap>:882(_find_spec)                                                                  <-       1    0.000    0.000  <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
<frozen importlib._bootstrap_external>:1272(find_spec)                                                         <-       1    0.000    0.000  <frozen importlib._bootstrap>:882(_find_spec)
<frozen importlib._bootstrap_external>:1240(_get_spec)                                                         <-       1    0.000    0.000  <frozen importlib._bootstrap_external>:1272(find_spec)
<frozen importlib._bootstrap_external>:722(exec_module)                                                        <-       1    0.000    0.000  <frozen importlib._bootstrap>:663(_load_unlocked)
<frozen importlib._bootstrap_external>:793(get_code)                                                           <-       1    0.000    0.000  <frozen importlib._bootstrap_external>:722(exec_module)
<frozen importlib._bootstrap_external>:1356(find_spec)                                                         <-       3    0.000    0.000  <frozen importlib._bootstrap_external>:1240(_get_spec)
{built-in method builtins.print}                                                                               <-       3    0.000    0.000  kakao.py:10(calc_pure_python)
```

반대로 해당 함수에서 호출하는 함수 목록도 확인할 수 있습니다.

```shell
In [6]: p.print_callees()

Ordered by: cumulative time

Function                                                                                                       called...
                                                                                                                   ncalls  tottime  cumtime
{built-in method builtins.exec}                                                                                ->       1    0.000    0.000  /usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/cProfile.py:5(<module>)
                                                                                                                        1    0.029   10.302  kakao.py:2(<module>)
kakao.py:2(<module>)                                                                                           ->       1    0.000    0.000  <frozen importlib._bootstrap>:978(_find_and_load)
                                                                                                                        1    0.551   10.272  kakao.py:10(calc_pure_python)
kakao.py:10(calc_pure_python)                                                                                  ->       1    7.519    9.585  kakao.py:52(calculate_z_serial_purepython)
                                                                                                                        2    0.000    0.000  {built-in method builtins.len}
                                                                                                                        3    0.000    0.000  {built-in method builtins.print}
                                                                                                                        1    0.008    0.008  {built-in method builtins.sum}
                                                                                                                        2    0.000    0.000  {built-in method time.time}
                                                                                                                  2002000    0.128    0.128  {method 'append' of 'list' objects}
kakao.py:52(calculate_z_serial_purepython)                                                                     -> 34219980    2.066    2.066  {built-in method builtins.abs}
                                                                                                                        2    0.000    0.000  {built-in method builtins.len}
{built-in method builtins.abs}                                                                                 ->
{method 'append' of 'list' objects}                                                                            ->
{built-in method builtins.sum}                                                                                 ->
<frozen importlib._bootstrap>:978(_find_and_load)                                                              ->       1    0.000    0.000  <frozen importlib._bootstrap>:143(__init__)
```

cProfile 의 출력내용은 약간 장황한 면이 있어서, 줄바꿈 없이 깔끔하게 보고 싶으면 창을 넓게 늘려서 사용해야 합니다.

## Using line_profiler for Line-by-Line Measurements 

`line_profiler` 가 Python 코드에서 CPU 가 병목 원인을 찾아주는 가장 강력한 도구일 것입니다. `line_profiler` 는 개별 함수를 한 줄씩 프로파일링할 수 있으므로 먼저 cProfile 을 사용해 어떤 함수를 `line_profiler` 로 자세히 살펴볼지 방향을 정하면 됩니다.

`line_profiler` 를 설치하려면 `pip install line_profiler` 를 입력하면 됩니다.

`@profile` 데코레이터는 선택한 함수를 표시하기 위해 사용합니다 *kernprof.py* 스크립트는 코드를 실행하고 선택한 함수의 각 줄에 대한 CPU 시간 등의 통계를 기록하는 데 사용합니다.

`-l` 옵션은 함수 단위가 한 줄씩 프로파일링하겠다는 옵션이며 `-v` 옵션은 출력결과를 다양하게 보여줍니다.

```shell

calculate_z_serial_purepython took 69.51615619659424 seconds
Wrote profile results to julia1_lineprofiler.py.lprof
Timer unit: 1e-06 s

$ kernprof -l -v julia1_lineprofiler.py

Total time: 39.9619 s
File: julia1_lineprofiler.py
Function: calculate_z_serial_purepython at line 53

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    53                                           @profile
    54                                           def calculate_z_serial_purepython(maxiter, zs, cs):
    55                                             """Calculate output list using Julia update rule"""
    56         1       6074.0   6074.0      0.0    output = [0] * len(zs)
    57   1000001     312475.0      0.3      0.8    for i in range(len(zs)):
    58   1000000     297751.0      0.3      0.7      n = 0
    59   1000000     350329.0      0.4      0.9      z = zs[i]
    60   1000000     328300.0      0.3      0.8      c = cs[i]
    61  34219980   15072458.0      0.4     37.7      while abs(z) < 2 and n < maxiter:
    62  33219980   12147692.0      0.4     30.4        z = z * z + c
    63  33219980   11108739.0      0.3     27.8        n += 1
    64   1000000     338078.0      0.3      0.8      output[i] = n
    65         1          1.0      1.0      0.0    return output
```

## Using memory_profiler to Diagnose Memory Usage 

CPU 사용량을 측정하는 `line_profiler` 처럼 메모리 사용량을 줄 단위로 측정하는 `memory_profiler` 가 있습니다.

`memory_profiler` 는 다음 명령어로 설치할 수 있습니다.

```shell
$ pip install memory_profiler
```

그리고 `psutil` 은 다음 명령어로 설치할 수 있습니다.

```shell
$ pip install psutil
```

아래는 `memory_profiler` 를 이용하여 메모리 사용을 측정한 예입니다. `line_profiler` 와 비교해서 시간이 더 오래 걸릴 수 있습니다.

```shell
calculate_z_serial_purepython took 3594.8900051116943 seconds
Filename: julia.py

Line #    Mem usage    Increment   Line Contents
================================================
    10   36.180 MiB   36.180 MiB   @profile
    11                             def calc_pure_python(desired_width, max_iterations):
    12                                 """Create a list of complex coordinates (zs) and complex parameters (cs), build Julia set, and display"""
    13   36.180 MiB    0.000 MiB       x_step = (float(x2 - x1) / float(desired_width))
    14   36.180 MiB    0.000 MiB       y_step = (float(y1 - y2) / float(desired_width))
    15   36.180 MiB    0.000 MiB       x = []
    16   36.180 MiB    0.000 MiB       y = []
    17   36.180 MiB    0.000 MiB       ycoord = y2
    18
    19   36.180 MiB    0.000 MiB       while ycoord > y1:
    20   36.180 MiB    0.000 MiB           y.append(ycoord)
    21   36.180 MiB    0.000 MiB           ycoord += y_step
    22   36.180 MiB    0.000 MiB       xcoord = x1
    23
    24   36.184 MiB    0.000 MiB       while xcoord < x2:
    25   36.184 MiB    0.004 MiB           x.append(xcoord)
    26   36.184 MiB    0.000 MiB           xcoord += x_step
    27                                 # Build a list of coordinates and the initial condition for each cell.
    28                                 # Note that our initial condition is a constant and could easily be removed;
    29                                 # we use it to simulate a real-world scenario with several inputs to
    30                                 # our function.
    31   36.184 MiB    0.000 MiB       zs = []
    32   36.184 MiB    0.000 MiB       cs = []
    33
    34  119.973 MiB    0.000 MiB       for ycoord in y:
    35  119.973 MiB    0.016 MiB           for xcoord in x:
    36  119.973 MiB    1.098 MiB               zs.append(complex(xcoord, ycoord))
    37  119.973 MiB    1.098 MiB               cs.append(complex(c_real, c_imag))
    38
    39  119.977 MiB    0.004 MiB       print("Length of x:", len(x))
    40  119.977 MiB    0.000 MiB       print("Total elements:", len(zs))
    41
    42  119.977 MiB    0.000 MiB       start_time = time.time()
    43   80.156 MiB   80.156 MiB       output = calculate_z_serial_purepython(max_iterations, zs, cs)
    44   80.184 MiB    0.027 MiB       end_time = time.time()
    45   80.184 MiB    0.000 MiB       secs = end_time - start_time
    46   80.281 MiB    0.098 MiB       print(calculate_z_serial_purepython.__name__ + " took", secs, "seconds")
    47
    48                                 # This sum is expected for a 1000^2 grid with 300 iterations.
    49                                 # It catches minor errors we might introduce when we're
    50                                 # working on a fixed set of inputs.
    51   81.172 MiB    0.891 MiB       assert sum(output) == 33219980


Filename: julia.py

Line #    Mem usage    Increment   Line Contents
================================================
    53  119.977 MiB  119.977 MiB   @profile
    54                             def calculate_z_serial_purepython(maxiter, zs, cs):
    55                               """Calculate output list using Julia update rule"""
    56  127.609 MiB    7.633 MiB     output = [0] * len(zs)
    57  137.910 MiB    0.000 MiB     for i in range(len(zs)):
    58  137.910 MiB    0.000 MiB       n = 0
    59  137.910 MiB    0.004 MiB       z = zs[i]
    60  137.910 MiB    0.004 MiB       c = cs[i]
    61  137.910 MiB    0.004 MiB       while abs(z) < 2 and n < maxiter:
    62  137.910 MiB    0.004 MiB         z = z * z + c
    63  137.910 MiB    0.000 MiB         n += 1
    64  137.910 MiB    0.000 MiB       output[i] = n
    65   80.105 MiB    0.000 MiB     return output
```

아래 `Example 5` 는 `mprof run julia1_memoryprofiler.py` 명령으로 생성한 것입니다. 이 명령을 실행하면 먼저 통계 파일을 생성하고 `mprof plot` 명령으로 시각화합니다.

> Example 5 - memory_profiler report using mprof

![image](https://user-images.githubusercontent.com/44635266/74648824-becf0e00-51c1-11ea-8864-1dc403042ca3.png)

함수 수준의 동작을 관찰하는 데 추가로 컨텍스트 관리자를 사용해 라벨을 추가할 수 있습니다. 아래 그림은 라벨과 `mprof` 를 함꼐 이용한 `memory_profiler` 입니다.

> Example 6 - memory_profiler report using mprof with labels

![image](https://user-images.githubusercontent.com/44635266/74648829-c0003b00-51c1-11ea-8a8a-bca6d13a69e6.png)

`create_range_of_zs` 뒤로 RAM 사용량이 급격하게 증가하는 것을 확인할 수 있습니다. `xrange` 를 사용하는 대신 `range` 를 사용해서 색인을 생성할 목적으로 1,000,000 개의 원소를 가지는 큰 리스트를 만들었는데, 큰 리스트를 다루게 되면 RAM 을 전부 써버릴지 모르니 비효율적인 방법입니다. 이 리스트를 저장하기 위한 메모리 할당 역시 시간을 잡아먹으며 해당 함수의 쓸모의 전혀 동무이 되지 않습니다.

```python
@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    with profile.timestamp("create_output_list"):
        output = [0] * len(zs)
    time.sleep(1)
    with profile.timestamp("create_range_of_zs"):
        iterations = range(len(zs))
        with profile.timestamp("calculate_output"):
            for i in iterations:
                n = 0
                z = zs[i]
                c = cs[i]
                while n < maxiter and abs(z) < 2:
                    z = z * z + c
                    n += 1
                output[i] = n
    return output
```

`calculate_output` 블록이 가장 오랫동안 실행되고 있는데 RAM 사용량이 아주 천천히 증가하는 것을 볼 수 있습니다. 이는 내부 반복문에서 사용하는 임시값 때문입니다.

마지막으로 `range` 를 `xrange` 로 바꿔보겠습니다. 아래 `Example 7` 을 확인해보면 RAM 사용량이 줄어든 것을 볼 수 있습니다.

> Example 7 - memory_profiler report showing the effect of changing range to xrange

![image](https://user-images.githubusercontent.com/44635266/74648830-c1c9fe80-51c1-11ea-8826-402c3075bd62.png)

여러 줄에 RAM 사용량을 확인하고 싶으면 IPython 의 명령어인 `%memit` 을 사용하면 됩니다.

## Inspecting Objects on the Heap with heapy 

Guppy 프로젝트는 Python 힙 메모리에 있는 객체의 수와 크기를 살펴볼 수 있도록 heapy 라는 이름의 힙 메모리 조사 도구를 제공합니다.

heapy 를 사용하려면 다음 명령어로 `guppy` 패키지를 설치하면 됩니다.

```shell
pip3 install guppy
```

아래 코드는 약간 변형한 쥘리아 집합 코드입니다. `calc_pure_python` 안에 힙 객체 hpy 를 포함시키고 3 곳에서 힙의 상태를 출력합니다.

```python
def calc_pure_python(draw_output, desired_width, max_iterations):
    from guppy import hpy
    hp = hpy()
    print("heapy after creating y and x lists of floats")
    h = hp.heap()
    print(h)


    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print("heapy after creating zs and cs using complex numbers")
    h = hp.heap()
    print(h)

    print ("Length of x:", len(x))
    print ("Total elements:", len(zs))
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print (calculate_z_serial_purepython.__name__ + " took", secs, "seconds")

    print ("heapy after calling calculate_z_serial_purepython")
    h = hp.heap()
    print (h)

    # this sum is expected for 1000^2 grid with 300 iterations
    assert sum(output) == 33219980
```

아래는 `guppy` 패키지를 이용한 프로파일링 결과입니다.

```shell
$ python julia1_guppy.py

heapy after creating y and x lists of floats
Partition of a set of 40479 objects. Total size = 4555081 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  11774  29  1026200  23   1026200  23 str
     1   9414  23   762816  17   1789016  39 tuple
     2   2460   6   355784   8   2144800  47 types.CodeType
     3   4824  12   337773   7   2482573  55 bytes
     4    437   1   333608   7   2816181  62 type
     5   2249   6   323856   7   3140037  69 function
     6    437   1   243536   5   3383573  74 dict of type
     7     98   0   164312   4   3547885  78 dict of module
     8    250   1   117232   3   3665117  80 dict (no owner)
     9     47   0   103576   2   3768693  83 set
<117 more rows. Type e.g. '_.more' to view.>

heapy after creating zs and cs using complex numbers
Partition of a set of 2040479 objects. Total size = 85949977 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0 2000000  98 64000000  74  64000000  74 complex
     1    109   0 17432664  20  81432664  95 list
     2  11774   1  1026200   1  82458864  96 str
     3   9414   0   762816   1  83221680  97 tuple
     4   2460   0   355784   0  83577464  97 types.CodeType
     5   4824   0   337773   0  83915237  98 bytes
     6    437   0   333608   0  84248845  98 type
     7   2249   0   323856   0  84572701  98 function
     8    437   0   243536   0  84816237  99 dict of type
     9     98   0   164312   0  84980549  99 dict of module
<118 more rows. Type e.g. '_.more' to view.>
Length of x: 1000
Total elements: 1000000
calculate_z_serial_purepython took 7.341063022613525 seconds

heapy after calling calculate_z_serial_purepython
Partition of a set of 2140852 objects. Total size = 96760453 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0 2000000  93 64000000  66  64000000  66 complex
     1    110   0 25432736  26  89432736  92 list
     2 101335   5  2840140   3  92272876  95 int
     3  11774   1  1026200   1  93299076  96 str
     4   9414   0   762816   1  94061892  97 tuple
     5   2460   0   355784   0  94417676  98 types.CodeType
     6   4824   0   337773   0  94755449  98 bytes
     7    437   0   333608   0  95089057  98 type
     8   2249   0   323856   0  95412913  99 function
     9    437   0   243536   0  95656449  99 dict of type
<118 more rows. Type e.g. '_.more' to view.>
```

`hpy.setrelheap()` 함수는 메모리 설정에서 체크포인트를 생성하기 위해 사용합니다. 이후 호출하는 `hpy.heap()` 함수는 체크포인트에서 변화된 내용을 출력합니다.

## Using dowser for Live Graphing of Instantiated Variables

`dowser` 는 실행중인 코드의 네임스페이스를 조작하여 CherryPy 인터페이스를 통해 웹 브라우저에서 생성하는 변수를 실시간으로 확인할 수 있습니다. 각 객체는 선 그래프로 보여주며 특정 객체 수가 늘어나는지 확인할 수 있습니다.

특정 조작에 따라 메모리 사용량이 변화하는 웹 서버나 오래 실행되는 프로세스가 있다면 `dowser` 를 통해 인터렉티브하게 확인할 수 있습니다. `Example 8` 은 `dowser` 의 사용 예입니다.

> Example 8 - Several sparklines shown through CherryPy with dowser

![image](https://user-images.githubusercontent.com/44635266/74650396-f8eddf00-51c4-11ea-8b3e-c6c8ded08cd5.png)

`dowser` 를 사용하기 전에 아래 코드를 추가해 CherryPy 서버를 시작합니다.

```python
def launch_memory_usage_server(port=8080):
    import cherrypy
    import dowser

    cherrypy.tree.mount(dowser.Root())
    cherrypy.config.update({
        'environment': 'embedded',
        'server.socket_port': port
    })

    cherrypy.engine.start()
```

복잡한 계산을 하기 전에 CherryPy 서버를 실행합니다. 계산이 끝난 뒤에는 `time.sleep` 을 추가하여 CherryPy 프로세스가 종료되지 않도록 하고 네임스페이스의 상태를 살펴봅니다.

```python
...
    for xcoord in x:
        zs.append(complex(xcoord, ycoord))
        cs.append(complex(c_real, c_imag))
launch_memory_usage_server()
...
output = calculate_z_serial_purepython(max_iterations, zs, cs)
...
print "now waiting..."
while True:
    time.sleep(1)
```

`Example 8` 의 TRACE 링크를 클릭하면 아래 `Example 9` 와 같이 리스트 객체의 내용을 확인할 수 있습니다.

> Example 9 - 1,000,000 items in a list with dowser

![image](https://user-images.githubusercontent.com/44635266/74650400-fab7a280-51c4-11ea-922f-4992a0eb3d2f.png)

## Using the dis Module to Examine CPython Bytecode 

Python 코드의 CPU 와 RAM 사용량을 측정하는 방법을 알아봤습니다. 이제 바이트코트에 대해 알아보겠습니다.

`dis` 모듈을 통해 스택 기반의 CPython 가상 머신에서 동작하는 바이트 코드를 살펴볼 수 있습니다. Python 코드가 가상 머신 안에서는 어떻게 동작하는지 이해하면 특정 코딩 습관이 다른 방법보다 빠른 코드를 만들어 내는지 알 수 있습니다.

`dis` 모듈은 기본으로 내장되어 있습니다. 여기에 코드나 모듈을 넘기면 역 어셈블 결과를 출력해줍니다. 아래는 함수의 역어셈블 결과입니다.

```python
import dis

dis.dis(calc_pure_python)

 11           0 LOAD_CONST               1 (0)
              2 BUILD_LIST               1
              4 LOAD_GLOBAL              0 (len)
              6 LOAD_FAST                1 (zs)
              8 CALL_FUNCTION            1
             10 BINARY_MULTIPLY
             12 STORE_FAST               3 (output)

 12          14 SETUP_LOOP              94 (to 110)
             16 LOAD_GLOBAL              1 (range)
             18 LOAD_GLOBAL              0 (len)
             20 LOAD_FAST                1 (zs)
             22 CALL_FUNCTION            1
             24 CALL_FUNCTION            1
             26 GET_ITER
        >>   28 FOR_ITER                78 (to 108)
             30 STORE_FAST               4 (i)

 13          32 LOAD_CONST               1 (0)
             34 STORE_FAST               5 (n)

 14          36 LOAD_FAST                1 (zs)
             38 LOAD_FAST                4 (i)
             40 BINARY_SUBSCR
             42 STORE_FAST               6 (z)
```

결과는 간결하며 직관적입니다. 첫 번째 컬럼은 원래 소스 파일의 줄 번호를 나타냅니다. 두 번째 칼럼은 >> 기호를 포함하는, 이는 코드의 다른 지점에서 점프해오는 지점입니다. 세 번째 컬럼은 연산의 주소와 그 이름이며, 네 번째 컬럼은 해당 연산에 전달하는 매개변수입니다. 마지막으로 다섯 번째 컬럼은 이해를 돕기위해 Python 코드를 같이 출력한 것입니다.

이해를 돕기위해 해당 Python 코드를 알려드리겠습니다.

```python
def calculate_z_serial_purepython(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while n < maxiter and abs(z) < 2:
            z = z * z + c
            n += 1
        output[i] = n
    return output
```

### Different Approaches, Different Complexity 

아래 두 코드를 살펴보겠습니다. 둘 다 같은 일을 하지만, 첫 번째 코드는 더 많은 Python 바이트코드를 생성하기 때문에 더 느리게 동작합니다.

```python
def fn_expressive(upper = 1000000):
  total = 0
  for n in xrange(upper):
    total += n
  return total

def fn_terse(upper = 1000000):
  return sum(xrange(upper))

print "Functions return the same result:", fn_expressive() == fn_terse()
Functions return the same result:
True
```

두 함수 정수 수열의 합을 구하는 함수입니다. 어림 잡아도 더 적은 수의 바이트코드를 생성하는 내장 함수를 사용하는 쪽이 더 많은 바이트코드를 생성하는 함수보다 빠르게 작동할 것입니다. 아래 `%timeit` 을 이용해 최적 실행 시간을 측정해봤습니다.

```python
%timeit fn_expressive()
10 loops, best of 3: 42 ms per loop

%timeit fn_terse()
100 loops, best of 3: 12.3 ms per loop
```

`dis` 모듈을 통하여 각 함수를 역어셈블해보면 아래와 같이 수행해야하는 연산횟수가 다릅니다.

```python
import dis

dis.dis(fn_expressive)

  2           0 LOAD_CONST               1 (0)
              2 STORE_FAST               1 (total)

  3           4 SETUP_LOOP              24 (to 30)
              6 LOAD_GLOBAL              0 (xrange)
              8 LOAD_FAST                0 (upper)
             10 CALL_FUNCTION            1
             12 GET_ITER
        >>   14 FOR_ITER                12 (to 28)
             16 STORE_FAST               2 (n)

  4          18 LOAD_FAST                1 (total)
             20 LOAD_FAST                2 (n)
             22 INPLACE_ADD
             24 STORE_FAST               1 (total)
             26 JUMP_ABSOLUTE           14
        >>   28 POP_BLOCK

  5     >>   30 LOAD_FAST                1 (total)
             32 RETURN_VALUE

dis.dis(fn_terse)
  8           0 LOAD_GLOBAL              0 (sum)
              2 LOAD_GLOBAL              1 (xrange)
              4 LOAD_FAST                0 (upper)
              6 CALL_FUNCTION            1
              8 CALL_FUNCTION            1
             10 RETURN_VALUE
```

바이트 코드로 살펴보면 두 코드 블록의 차이는 두드러집니다. `fn_expressive()` 는 두 개의 지역 변수를 가지며, for 문에 의해 리스트를 순회합니다. for 루프에서 매번 StopIteration 예외가 발생하는지 검사합니다. 루프가 계속될 때마다 두 번재 변수인 n 타입을 검사하는 `total.__add__` 함수를 호출합니다. 이러한 추가 검사 과정에서 성능 하락이 누적됩니다.

`fn_terse()` 는 최적화된 C 리스트 표현식 함수를 호출해 중간 Python 객체를 생성하지 않고 최종 결과를 생성합니다. 여전히 매 반복마다 더해야 할 객체의 타입을 검사하지만 훨씬 빠릅니다.

## Unit Testing During Optimization to Maintain Correctness 

단위 테스트와 더불어 *coverage.py* 도 함께 고려하는게 좋습니다. *coverage.py* 를 사용하면 코드의 어떤 부분이 검사되었고 검사되지 않은 부분이 어디인지 알 수 있습니다. 이를 통해 최적화하려는 코드가 검사되는지를 쉽게 알 수 있어서 최적화 중에 실수를 하게 되면 빠르게 알 수 있습니다.

### No-op @profile Decorator 

`line_profiler` 나 `memory_profiler` 에서 `@profile` 을 사용하면 단위테스트에서 NameError 가 발생합니다. 단위 테스트 프레임워크는 `@profile` 데코레이터를 로컬 네임스페이스에 추가하지 않았기 때문입니다. 아무것도 하지 않는 `no-op` 데코레이터를 이용하면 이 문제를 피할 수 있습니다. 검사하려는 코드 블록에 추가하고 검사가 끝나면 제거하면 됩니다.

`no-op` 데코레이터를 이용하면 검사하려는 코드를 변경하지 않고 테스트를 실행할 수 있습니다. 즉, 프로파일링을 통한 최적화 작업 중에도 테스트를 돌려볼 수 있기 때문에 잘못된 최적화에 빠지는 일을 방지할 수 있습니다.

아래 예제는 `nosetest` 를 위한 테스트가 있고 `line_profiler` 나 `memory_profiler` 로 프로파일링하는 함수가 하나 있습니다.

```python
# ex.py
import unittest

@profile
def some_fn(nbr):
  return nbr * 2

class TestCase(unittest.TestCase):
  def test(self):
  result = some_fn(2)
  self.assertEquals(result, 4)
```

`nosetests` 를 실행하면 NameError 가 발생합니다.

```shell
$ nosetests ex.py
E
======================================================================
ERROR: Failure: NameError (name 'profile' is not defined)
...
NameError: name 'profile' is not defined

Ran 1 test in 0.001s

FAILED (errors=1)
```

해결 방법은 첫 부분에 `no-op` 데코레이터를 추가하는것입니다. 아래는 `line_profiler` 의 경우입니다.

```python
# for line_profiler
if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'):
  def profile(func):
    def inner(*args, **kwargs):
      return func(*args, **kwargs)
    return inner
```

`__builtin` 테스트는 `nosetests` 유무를 위한것이며 `hasattr` 테스트는 네임스페이스에 `@profile` 이 추가되었는지 검사합니다.

```shell
$ kernprof.py -v -l ex.py
Line # Hits Time Per %%HTMLit % Time Line Contents
==============================================================
 11 @profile
 12 def some_fn(nbr):
 13 1 3 3.0 100.0 return nbr * 2

$ nosetests ex.py
.
Ran 1 test in 0.000s
```

아래 예제는 `memory_profiler` 를 위한 `no-op` 데코레이터 입니다.

```python
# for memory_profiler
if 'profile' not in dir():
  def profile(func):
    def inner(*args, **kwargs):
      return func(*args, **kwargs)
    return inner
```

출력 결과는 아래와 같습니다.

```shell
python -m memory_profiler ex.py
...
Line # Mem usage Increment Line Contents
================================================
 11 10.809 MiB 0.000 MiB @profile
 12 def some_fn(nbr):
 13 10.809 MiB 0.000 MiB return nbr * 2

$ nosetests ex.py
.
Ran 1 test in 0.000
```

## Strategies to Profile Your Code Successfully 

안정적인 벤치마킹을 위해서는 다음 사항을 기억하면됩니다.

* Disable TurboBoost in the BIOS.
* Disable the operating system’s ability to override the SpeedStep (you will find this in your BIOS if you’re allowed to control it).
* Only use mains power (never battery power).
* Disable background tools like backups and Dropbox while running experiments.
* Run the experiments many times to obtain a stable measurement.
* Possibly drop to run level 1 (Unix) so that no other tasks are running.
* Reboot and rerun the experiments to double-confirm the results.

