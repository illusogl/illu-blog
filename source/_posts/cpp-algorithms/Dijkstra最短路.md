---
title: "Dijkstra 最短路"
date: 2026-06-11 19:22:00
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

using ll = long long;

const ll INF = 0x3f3f3f3f3f3f3f3fLL; // 足够大的无穷大

void solve()
{
    int n, m, s;
    cin >> n >> m >> s;

    vector<vector<pair<int, ll>>> g(n + 1);
    for (int i = 0; i < m; i++)
    {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        // 无向图再加一条：g[v].push_back({u, w});
    }

    vector<ll> dist(n + 1, INF);
    vector<bool> done(n + 1, false);
    // 小根堆：pair 先按距离排序，距离小的先出队
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;

    dist[s] = 0;
    pq.push({0, s});

    while (!pq.empty())
    {
        auto [d, u] = pq.top();
        pq.pop();

        if (done[u]) continue; // 堆里的旧记录，跳过
        done[u] = true; // 此时 dist[u] 已经是最短路

        for (auto [v, w] : g[u])
        {
            // 松弛：经过 u 到 v 更短就更新
            if (dist[v] > dist[u] + w)
            {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v}); // 新距离入堆
            }
        }
    }

    for (int i = 1; i <= n; i++)
    {
        if (dist[i] == INF) cout << "INF ";
        else cout << dist[i] << ' ';
    }
    cout << '\n';
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T = 1;
    // cin >> T;
    while (T--) solve();
    return 0;
}
```

求单源最短路，适合边权非负的有向图或无向图。无向图存边时加一条反向边即可。用邻接表和小根堆，时间复杂度 O((n+m) log n)，空间复杂度 O(n+m)。
