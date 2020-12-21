---
title : PyOpenGL - OpenGL.error.NullFunctionError 에러 해결
tags :
- PyOpenGL
- OpenGL
- Error
---

Window 환경에서 PyOpenGL 을 설치화하고 기본 예제를 돌리려할 때 glutInit 초기화 에러가 발생할 수 있습니다.

대표적인 에러 로그는 아래와 같습니다.

```
OpenGL.error.NullFunctionError: Attempt to call an undefined function glutInit, check for bool(glutInit) before calling
```

대표적으로 원인은 2 가지가 있습니다.

1. Python 과 PyOpenGL 버전 문제(자주 발생하지 않음)
2. freeglut 관련 문제

첫 번째는 자주 발생하지 않지만 저 같은 경우 한번 문제가 생겨서 현재

* Python 3.8.0
* PyOpenGL 3.1.0

버전으로 사용하고 있습니다.

두 번째 에러의 같은 경우 [https://www.transmissionzero.co.uk/software/freeglut-devel/](https://www.transmissionzero.co.uk/software/freeglut-devel/) 사이트로 접속을합니다.

freeglut 파일을 다운 받고 압축 해제 후 Binary 폴더에 있는 freeglut.dll 파일을 아래 폴더에 넣어주시면 됩니다.

* C:\Windows\SysWOW64
* C:\Windows\System32

