## Graph

### Bandwidth First Search

```python
import sys
from collections import deque

dx = [0, 0, 1, -1, 1, -1, 1, -1]
dy = [1, -1, 0, 0, 1, -1, -1, 1]

def BFS(maps, M, N, x, y):
    check = [[-1 for _ in range(N)] for _ in range(M)]
    dq = deque()
    dq.append((x, y))

    while dq:
        tx, ty = dq.popleft()
        for i in range(8):
            nx = tx + dx[i]
            ny = ty + dy[i]

            if 0 <= nx < M and 0 <= ny < N:
                if maps[nx][ny] == 1:
                    dq.append((nx, ny))
                    maps[nx][ny] = 0

def solution():
    M, N = map(int, sys.stdin.readline().split())

    maps = []
    for _ in range(M):
        maps.append(list(map(int, sys.stdin.readline().split())))

    cnt = 0
    for i in range(M):
        for j in range(N):
            if maps[i][j] == 1:
                cnt += 1
                BFS(maps, M, N, i, j)

    print(cnt)

solution()
```

### Floyd–Warshall

```python
import sys

def solution():
    _INF = 10000001
    N = int(input())
    T = int(input())
    Floyd = [[_INF] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if i == j :
                Floyd[i][j] = 0
            else:
                Floyd[i][j] = _INF

    for i in range(T):
        x, y, distance = map(int,sys.stdin.readline().split())
        Floyd[x-1][y-1] = min(Floyd[x-1][y-1], distance)

    for k in range(N):
        for i in range(N):
            for j in range(N):
                Floyd[i][j] = min(Floyd[i][j], Floyd[i][k] + Floyd[k][j])

    for i in range(N):
        ret = ''
        for j in range(N):
            if Floyd[i][j] == _INF:
                ret += '0'
                ret += ' '
            else:
                ret += str(Floyd[i][j])
                ret += ' '
        print(ret)

solution()
```

## Tree

### Segment Tree

```python
import sys, math
mod = 1000000007

def init(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
        return tree[node]

    mid = (start + end) // 2
    tree[node] = init(arr, tree, node * 2, start, mid) + \
                 init(arr, tree, node * 2 + 1, mid + 1, end)
    return tree[node]

def updateValue(tree, node, left, right, target, value):
    if (target < left or right < target): return 0
    tree[node] += value
    if left == right: return 0

    mid = (left + right) // 2
    updateValue(tree, node * 2, left, mid, target, value)
    updateValue(tree, node * 2 + 1, mid + 1, right, target, value)

def sumValue(tree, node, start, end, left, right):

    if (right < start or end < left): return 0
    elif (left <= start and end <= right): return tree[node]

    mid = (start + end) // 2
    return sumValue(tree, node * 2, start, mid, left, right) + \
           sumValue(tree, node * 2 + 1, mid + 1, end, left, right)

def solution():
    N, M, K = map(int, sys.stdin.readline().split())

    arr = []
    for i in range(N):
        arr.append(int(sys.stdin.readline()))

    height = int(math.ceil(math.log2(N)))
    treeSize = 1 << (height + 1)
    segmentTree = [0] * treeSize

    init(arr, segmentTree, 1, 0, N-1)

    for i in range(M + K):
        command = list(map(int, sys.stdin.readline().split()))

        if command[0] == 1:
            value = command[2] - arr[command[1] - 1]
            arr[command[1] - 1] = command[2]
            updateValue(segmentTree, 1, 0, N-1, command[1] - 1, value)

        else:
            print(sumValue(segmentTree, 1, 0, N-1, command[1]-1, command[2]-1))

solution()
```

### Segment tree with lazy propagation

```python
import sys, math

def init(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
        return tree[node]

    mid = (start + end) // 2
    tree[node] = init(arr, tree, node * 2, start, mid) + \
                 init(arr, tree, node * 2 + 1, mid + 1, end)
    return tree[node]

def updateLazyTree(tree, lazy, node, start, end):
    if lazy[node] != 0:
        tree[node] += lazy[node] * (end - start + 1)
        if start != end:
            lazy[node * 2] += lazy[node]
            lazy[node * 2 + 1] += lazy[node]
        lazy[node] = 0

def updateValue(tree, lazyTree, node, start, end, left, right, value):
    updateLazyTree(tree, lazyTree, node, start, end)

    if (right < start or end < left): return tree[node]
    elif (left <= start and end <= right):
        tree[node] += value * (end - start + 1)
        if start != end:
            lazyTree[node * 2] += value
            lazyTree[node * 2 + 1] += value
        return tree[node]

    mid = (start + end) // 2
    tree[node] = updateValue(tree, lazyTree, node * 2, start, mid, left, right, value) + \
                 updateValue(tree, lazyTree, node * 2 + 1, mid + 1, end, left, right, value)
    return tree[node]

def sumValue(tree, lazy, node, start, end, left, right):
    updateLazyTree(tree, lazy, node, start, end)
    if (right < start or end < left): return 0
    elif (left <= start and end <= right): return tree[node]

    mid = (start + end) // 2
    return sumValue(tree, lazy, node * 2, start, mid, left, right) + \
           sumValue(tree, lazy, node * 2 + 1, mid + 1, end, left, right)

def solution():
    N, M, K = map(int, sys.stdin.readline().split())

    arr = []
    for i in range(N):
        arr.append(int(sys.stdin.readline()))

    height = int(math.ceil(math.log2(N)))
    treeSize = 1 << (height + 1)
    segmentTree = [0] * treeSize
    lazySegmentTree = [0] * treeSize

    init(arr, segmentTree, 1, 0, N-1)

    for i in range(M + K):
        command = list(map(int, sys.stdin.readline().split()))

        if command[0] == 1:
            updateValue(segmentTree, lazySegmentTree, 1, 0, N-1, command[1]-1, command[2]-1, command[3])
        else:
            print(sumValue(segmentTree, lazySegmentTree, 1, 0, N-1, command[1]-1, command[2]-1))

solution()
```