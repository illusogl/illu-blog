---
title: "BFS"
date: 2025-11-18 23:11:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

BFS 从起点开始按层扩展。队列里放待访问的点，每次取出队首，把还没访问过的邻居加进队列，并把它们的距离记成当前点的距离加一。每个点只入队一次，所以第一次访问到它时，经过的边数就是最短距离。下面的 bfs(s, g) 返回从 s 到每个点的距离，不可达为 -1。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 返回从 s 到每个点的最短距离，-1 表示不可达
vector<int> bfs(int s, const vector<vector<int>>& g)
{
    int n = (int)g.size() - 1;
    vector<int> dist(n + 1, -1); // -1 表示还没访问
    queue<int> q;

    dist[s] = 0; // 起点距离为 0
    q.push(s);
    while (!q.empty())
    {
        int u = q.front();
        q.pop();
        for (int v : g[u])
        {
            if (dist[v] != -1) continue; // 第一次访问到就是最短路
            dist[v] = dist[u] + 1;       // 层数加一
            q.push(v);
        }
    }
    return dist;
}

void solve()
{
    int n, m, s;
    cin >> n >> m >> s;

    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> dist = bfs(s, g); // 不可达的点仍是 -1
    for (int i = 1; i <= n; i++)
        cout << dist[i] << " \n"[i == n];
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

适合边权为 1 的图求最短路，也常用来按层遍历和统计连通块。每个点和每条边只处理一次，时间复杂度 O(n+m)，空间 O(n+m)。
