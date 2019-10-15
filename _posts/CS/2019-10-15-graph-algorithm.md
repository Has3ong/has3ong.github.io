---
title : Graph Algorithm
tags:
- DFS
- BFS
- Dijkstra
- Kruskal
- Prim
---

## DFS / BFS

![](http://blog.hackerearth.com/wp-content/uploads/2015/05/dfsbfs_animation_final.gif)

그래프는 정점의 구성 뿐만 아니라 간선의 연결에도 규칙이 존재하지 않기 때문에 탐색이 복잡하다. 따라서 그래프의 모든 정점을 탐색하기 위한 방법은 다음의 두 가지 알고리즘을 기반으로 한다.

### 깊이 우선 탐색(Depth First Search: DFS)

그래프 상에 존재하는 임의의 한 정점으로부터 연결되어 있는 한 정점으로만 나아간다라는 방법을 우선으로 탐색한다. 일단 연결된 정점으로 탐색하는 것이다.

연결할 수 있는 정점이 있을 때까지 계속 연결하다가 더이상 연결되지 않은 정점이 없으면 바로 그 전 단계의 정점으로 돌아가서 연결할 수 있는 정점이 있는지 살펴봐야 할 것이다. 갔던 길을 되돌아 오는 상황이 존재하는 미로찾기처럼 구성하면 되는 것이다.

어떤 자료구조를 사용해야할까? 바로 Stack 이다. `Time Complexity : O(V+E) … vertex 개수 + edge 개수`

### 너비 우선 탐색(Breadth First Search: BFS)

그래프 상에 존재하는 임의의 한 정점으로부터 연결되어 있는 모든 정점으로 나아간다. Tree 에서의 Level Order Traversal 형식으로 진행되는 것이다.

BFS 에서는 자료구조로 Queue 를 사용한다. 연락을 취할 정점의 순서를 기록하기 위한 것이다. 우선, 탐색을 시작하는 정점을 Queue 에 넣는다.(enqueue) 그리고 dequeue 를 하면서 dequeue 하는 정점과 간선으로 연결되어 있는 정점들을 enqueue 한다. 즉 vertex 들을 방문한 순서대로 queue 에 저장하는 방법을 사용하는 것이다.

`Time Complexity : O(V+E) … vertex 개수 + edge 개수 ! BFS 로 구한 경로는 최단 경로이다.`

## Dijkstra algorithm


![DijkstraDemo](https://user-images.githubusercontent.com/44635266/66711762-f0c40400-edcc-11e9-8fa7-d59f1c9d71db.gif)


다익스트라 알고리즘은 도로 교통망 같은 곳에서 나타날 수 있는 그래프에서 꼭짓점 간의 최단 경로를 찾는 알고리즘이다. 이 알고리즘은 컴퓨터 과학자 에츠허르 다익스트라가 1956년에 고안했으며 삼 년 뒤에 발표했다.



다익스트라의 슈도코드는 아래와 같다

> pseudo code

```
function Dijkstra(Graph, source):

  create vertex set Q
  
  for each vertex v in Graph:   // 초기화
    if dist[v] then
      dist[v] ← distance
    else
      dist[v] ← INFINITY    // 소스에서 v까지의 아직 모르는 길이
    add v to Q    // 모든 노드는 초기에 Q에 속해있다 (미방문 집합)
    
  dist[source] ← 0    // 소스에서 소스까지의 길이
  
  while Q is not empty:
    u ← vertex in Q with min dist[u]    // 최소 거리를 갖는 꼭짓점
    
    remove u from Q
    
    for each neighbor v of u:   // v는 여전히 Q에 있다.
      alt ← dist[u] + length(u, v)
      if alt < dist[v]:   // v 까지의 더 짧은 경로를 찾았을 때
        dist[v] ← alt
        
  return dist[]
```

### 시간복잡도

하나의 노드에 대해 다익스트라 알고리즘을 수행하는 경우를 따져보겠습니다. 미방문노드 가운데 거리가 가장 작은 노드에 BFS를 적용합니다. 거리를 가장 작은 미방문노드를 가려내려면 최악의 경우 노드 전체를 모두 따져봐야 하므로 `O(|V|)`입니다. 선택된 노드의 모든 이웃노드들에 대해 최단경로 정보를 업데이트합니다. 한 노드당 엣지의 기대값은 `|E|/|V`입니다.

다익스트라 알고리즘은 이러한 연산을 전체 노드 수만큼 반복하므로 전체적인 계산복잡성은 `O(|V|2+|E|)`가 됩니다. 보통의 dense graph는 엣지의 수가 노드 수의 제곱만큼 있으므로 간략하게 계산복잡성을 적으면 `O(|V|2)`이 됩니다.


## MST (최소 신장 트리, Minimum Spanning Tree)

먼저 spanning tree는 모든 정점을 포함하고 , 정점간 서로 연결되면서 사이클이 존재하지 않는 그래프입니다.

spanning tree 중 edge weight 의 합이 최소인 spanning tree를 말한다. 여기서 말하는 spanning tree란 그래프 G 의 모든 vertex 가 cycle 이 없이 연결된 형태를 말한다.

### Kruskal Algorithm

![KruskalDemo](https://user-images.githubusercontent.com/44635266/66712118-cf661680-edd2-11e9-952c-b043e2bcdb8a.gif)

> Pseudo Code

초기화 작업으로 edge 없이 vertex 들만으로 그래프를 구성한다. 그리고 weight 가 제일 작은 edge 부터 검토한다. 그러기 위해선 Edge Set 을 non-decreasing 으로 sorting 해야 한다. 그리고 가장 작은 weight 에 해당하는 edge 를 추가하는데 추가할 때 그래프에 cycle 이 생기지 않는 경우에만 추가한다. spanning tree 가 완성되면 모든 vertex 들이 연결된 상태로 종료가 되고 완성될 수 없는 그래프에 대해서는 모든 edge 에 대해 판단이 이루어지면 종료된다.

#### 어떻게 cycle 생성 여부를 판단하는가?

`Union-Find` 아록리즘을 사용하거나 Graph 의 각 vertex 에 `set-id`라는 것을 추가적으로 부여한다. 그리고 초기화 과정에서 모두 1~n 까지의 값으로 각각의 vertex 들을 초기화 한다. 여기서 0 은 어떠한 edge 와도 연결되지 않았음을 의미하게 된다. 그리고 연결할 때마다 `set-id`를 하나로 통일시키는데, 값이 동일한 `set-id` 개수가 많은 `set-id` 값으로 통일시킨다.

#### Time Complexity

Edge 의 weight 를 기준으로 sorting - `O(E log E)`
cycle 생성 여부를 검사하고 set-id 를 통일 - `O(E + V log V)` => 전체 시간 복잡도 : `O(E log E)`

### Prim Algoirthm

![PrimAlgDemo](https://user-images.githubusercontent.com/44635266/66712119-cffead00-edd2-11e9-8b44-df14a85bf7da.gif)

초기화 과정에서 한 개의 vertex 로 이루어진 초기 그래프 A 를 구성한다. 그리고나서 그래프 A 내부에 있는 vertex 로부터 외부에 있는 vertex 사이의 edge 를 연결하는데 그 중 가장 작은 weight 의 edge 를 통해 연결되는 vertex 를 추가한다. 어떤 vertex 건 간에 상관없이 edge 의 weight 를 기준으로 연결하는 것이다. 이렇게 연결된 vertex 는 그래프 A 에 포함된다. 위 과정을 반복하고 모든 vertex 들이 연결되면 종료한다.

#### Time Complexity
전체 시간 복잡도 : `O(E log V)`
