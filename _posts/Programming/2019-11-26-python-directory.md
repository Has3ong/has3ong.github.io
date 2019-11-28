---
title : Python 현재 디렉토리 위치 구하기
tags :
- Python
---

사용할 디렉토리 예시

![image](https://user-images.githubusercontent.com/44635266/69623016-7225dc00-1085-11ea-9705-0909aad53769.png)

## 파일 이름, 파일 경로

`test.py`를 생성하고 아래 코드를 실행하면 파일 이름과 경로가 출력됩니다. `realpath()`는 심볼릭 링크 등의 실제 경로를 찾아주며, `abspath`는 파일의 절대경로를 리턴합니다.

```
import os
print(__file__)
print(os.path.realpath(__file__))
print(os.path.abspath(__file__))
```

Result

```
/Users/has3ong/Desktop/vrlab python/Test.py
/Users/has3ong/Desktop/vrlab python/Test.py
/Users/has3ong/Desktop/vrlab python/Test.py
```

## 현재 파일의 디렉토리(폴더) 경로

아래 코드들은 파일이 있는 폴더의 경로를 구하는 2가지 방법입니다. os.getcwd()는 폴더 경로를 리턴합니다. os.path.dirname()는 파일의 폴더 경로를 리턴합니다.

```
import os
print(os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)) )
```

Result

```
/Users/has3ong/Desktop
/Users/has3ong/Desktop/vrlab python
```

## 현재 디렉토리에 있는 파일 리스트

listdir()는 인자로 넘겨준 경로의 파일 리스트를 리턴합니다.

```
import os
print(os.listdir(os.path.dirname(os.path.realpath(__file__))))
```

Result

```
['Box', 'Cone', 'Sphere', 'Test.py', 'Cylinder']
```

> Example

```
import os

dirPath = os.path.dirname(os.path.realpath(__file__)) 
folderList = os.listdir(dirPath)

for i in folderList:
    if ".py" in i:
        folderList.remove(i)
        
for i in folderList:
    searchPath = dirPath + "/" + i
    FileList = os.listdir(searchPath)
    print("Label is : {}, File List is : {}".format(i, FileList))
```

Result

```
Label is : Box, File List is : ['3.txt', '2.txt', '1.txt']
Label is : Cone, File List is : ['5.txt', '4.txt', '6.txt']
Label is : Sphere, File List is : ['12.txt', '10.txt', '11.txt']
Label is : Cylinder, File List is : ['9.txt', '8.txt', '7.txt']
```