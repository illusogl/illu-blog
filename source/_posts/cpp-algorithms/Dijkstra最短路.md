---
title: "Dijkstra 最短路"
date: 2026-11-09 20:02:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

Dijkstra 维护一个距离数组，每次从优先队列里取出当前距离最小的点，确认它的最短路后，用它去松弛所有出边。队列里可能留下同一个点的旧记录，出队时用 vis 跳过。边权必须非负，否则已经确定的点还可能被更短的路径更新。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long INF = 0x3f3f3f3f3f3f3f3fLL;

int main() {

    // 邻接表：g[u] 存 {v, w}，表示 u -> v 有一条权为 w 的边
    vector<vector<pair<int, long long>>> g(n + 1);

    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        // 无向图再加一行：g[v].push_back({u, w});
    }

    // ---- 初始化（用 for 循环，不用 memset）----
    vector<long long> dist(n + 1);
    vector<bool> vis(n + 1, false);
    for (int i = 1; i <= n; i++) {
        dist[i] = INF;      // 初始距离全为无穷大
        vis[i] = false;     // 初始都未确定最短路
    }
    dist[s] = 0;            // 起点到自己距离为 0

    // 小根堆：pair<距离, 点>，按距离从小到大出堆
    priority_queue<pair<long long, int>,
                   vector<pair<long long, int>>,
                   greater<pair<long long, int>>> pq;
    pq.push({0, s});

    // ---- Dijkstra 主循环 ----
    while (!pq.empty()) {
        auto [d, u] = pq.top();   // 取出当前距离最小的点
        pq.pop();

        if (vis[u]) continue;     // 懒删除：该点已确定，跳过堆里的旧记录
        vis[u] = true;            // 标记 u 的最短路已确定

        // 遍历 u 的所有出边
        for (auto [v, w] : g[u]) {
            // 松弛：若经过 u 到 v 更短，则更新
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});   // 新距离入堆
            }
        }
    }

    // ---- 输出 ----
    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) cout << "INF ";
        else cout << dist[i] << ' ';
    }
    cout << '\n';

    return 0;
}
```

求单源最短路，适合边权非负的有向图或无向图。无向图存边时加一条反向边即可。用邻接表和小根堆，时间复杂度 O((n+m) log n)，空间复杂度 O(n+m)。
