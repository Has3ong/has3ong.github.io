---
title : Python 동기 / 비동기 구현 -1-
tags :
- Asynchronous
- Synchronous
- Callback
- Python
---

## Callback

코드가 다른 작업을 시작할 수 있게 만들기 위해 프로그램의 남은 부분이 다른 작업들을 진행할 수 있도록 실행 흐름을 중단하지 않을 방법을 찾아야 한다.

비동기로 동작하기위해 가장 간단한 방법 중 하나는 callback이다. 코드로 아래 예시를 보여드리겠습니다.

> Example

```python
import threading
import time

def sync_wait_and_print(msg):
    time.sleep(1.0)
    print(msg)

def async_wait_and_print(msg):
    def callback():
        print(msg)

    timer = threading.Timer(1.0, callback)
    timer.start()

first = "First Call"
second = "Second Call"
third = "Third Call"

print("Start Sync")
sync_wait_and_print(first)
sync_wait_and_print(second)
sync_wait_and_print(third)
print("End Sync")

print("Start Async")
async_wait_and_print(first)
async_wait_and_print(second)
async_wait_and_print(third)
print("End Async")
```

**Result**

결과를 확인해보면 동기로 작성한 코드는 순서대로 진행이 되지만, 비동기적으로 작성한 코드는 `async_wait_and_print` 함수를 재출하고 바로 진행하기 때문에 "End Async" 메세지가 먼저 출력되는것을 확인할 수 있습니다.

```
Start Sync
First Call
Second Call
Third Call
End Sync

Start Async
End Async
First Call
Second Call
Third Call
```

만약 아무것도 반환할 수 없다면 요청이 반환하는 값을 어떻게 전달할 수 있을지 생각해봐야합니다. 이 경우에는 값을 반환하는 대신 on_done 콜백에 인자로 전달을 합니다.

> Example

```python
import threading
import time

def async_network_request(number, on_done):

    def timer_done():
        on_done({"Value" : number, "Resut" : number ** 2})

    timer = threading.Timer(1.0, timer_done)
    timer.start()

def on_done(result):
    print(result)

print("Start Async")
async_network_request(3, on_done)
async_network_request(4, on_done)
async_network_request(5, on_done)
print("End Async")
```

**Result**

위의 예와 비슷합니다. 제곱하려는 숫자와 결과값이 준비가되면 그 값을 받을 콜백을 넘기기만 하면 됩니다.

```
Start Async
End Async
{'Value': 4, 'Result': 16}
{'Value': 3, 'Result': 9}
{'Value': 5, 'Result': 25}
```

하나의 함수를 더 추가해서 `async_network_request` 함수를 사용하여 비동기적으로 코드를 작성해 보겠습니다.

> Example

```python
def fetch_square(number):
    def on_done(response):
        if response["Result"]:
            print("Result is : {}".format(response["Result"]))
    async_network_request(number, on_done)
```

## Future

Future 는 비동기 호출의 결과를 추적하는데 사용할 수 있는 편리한 패턴입니다. Future를 이용하면 요청한 자원을 추적하고 가용할 수 있을때까지 대기하는데 도움이 되는 추상화 입니다.

Future 는 아래와 같이 부를 수 있습니다.

```python
>>> from concurrent.futures import Future
>>> fut = Future()
<Future at 0x10b195290 state=pending>
```

현재 Future는 사용할 수 없는 값을 나타냅니다. 결과값을 사용할 수 있게 `set.result` 메소드를 사용하겠습니다.

```python
>>> fut.set_result("Hello World")
<Future at 0x10b195290 state=finished returned str>
>>> fut.result()
'Hello World'
```

이제 Future를 이용하여 코드를 작성해 보겠습니다.

> Example

```python
from concurrent.futures import Future
import threading

def async_network_request(number):
    future = Future()
    result = {"value" : number, "result" : number ** 2, "success": True}
    timer = threading.Timer(1.0, lambda: future.set_result(result))
    timer.start()
    return future

def fetch_square(number):
    fut = async_network_request(number)
    def on_done_future(future):
        response = future.result()
        if response["success"]:
            print("Value is : {}, Result is : {}".format(response["value"], response["result"]))

    fut.add_done_callback(on_done_future)

print("Start Async Future")
fetch_square(3)
fetch_square(4)
fetch_square(5)
print("End Async Future")
```

**Result**

```
Start Async Future
End Async Future
Value is : 3, Result is : 9
Value is : 4, Result is : 16
Value is : 5, Result is : 25
```

callback 과 상당히 비슷하기도 합니다. 한가지 차이점으로는 `Future.add_done_callback()` 메소드로 콜백을 연결하기 때문에 이전과 같이 `on_done` 콜백을 받을 필요가 없습니다.

## Event Loop

지금까지는 OS 스레드를 이용해 병렬처리를 구현했습니다. 하지만 이벤트 루프를 이용한 비동기를 사용하는 방법도 있습니다.

이벤트 루프의 경우 다양한 자원의 상태를 감시하여 이벤트가 일어나면 콜백 실행을 트리거 하는것입니다.

아래 코드를 통해 살펴보겠습니다.

> Example

```python
import time

class Timer:

    def __init__(self, timeout):
        self.timeout = timeout
        self.start = time.time()

    def done(self):
        return time.time() - self.start > self.timeout

    def on_timer_done(self, callback):
        self.callback = callback

timers = []

timer1 = Timer(1.0)
timer1.on_timer_done(lambda : print("First Time is Done"))

timer2 = Timer(2.0)
timer2.on_timer_done(lambda : print("Second Timer is Done"))

timers.append(timer1)
timers.append(timer2)

while True:
    for timer in timers:
        if timer.done():
            timer.callback()
            timers.remove(timer)
    if len(timers) == 0:
        break
```

print 함수를 사용하는 대신 적절한 시간에 루프가 `timer.callback` 을 호출할것입니다. 그래서 비동기 프레임 워크가 시작이 됩니다.

타이머들은 이벤트 루프 즉, `while True:` 안에서 주기적으로 타이머를 검사합니다. 그리고 필요한 경우 콜백을 처리합니다.

**Result**

```
First Time is Done
Second Timer is Done
```

계속해서 실행되는 루프가 실행 흐름을 관리하기 떄문에 이벤트 루프 안에서는 블로킹 호출을 절대 사용하면 안됩니다.

그렇기 때문에 `time.sleep`과 같은 블로킹 호출을 사용하는 대신 이벤트 루프가 자원이 준비될 때 감지해서 콜백을 실행하게하며, 실행흐름을 중단하지 않으므로 이벤트 루프가 여러 자원을 제약없이 동시적으로 감시할 수 있습니다.


