---
title: "LCA"
date: 2026-08-12 11:55:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

LCA 用倍增预处理每个点往上 2^k 步的祖先。查询时先把深的点抬到同一深度，再一起往上跳，直到父亲相同。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int LOG = 20; // 2^20 > 1e6，n 更大时调大
vector<vector<int>> g;
vector<int> dep;
vector<vector<int>> up;

void dfs(int u, int p)
{
    up[u][0] = p;
    for (int k = 1; k < LOG; k++)
        up[u][k] = up[up[u][k - 1]][k - 1]; // 2^k 级祖先

    for (int v : g[u])
    {
        if (v == p) continue;
        dep[v] = dep[u] + 1;
        dfs(v, u);
    }
}

int lca(int a, int b)
{
    if (dep[a] < dep[b]) swap(a, b);

    int diff = dep[a] - dep[b];
    for (int k = 0; k < LOG; k++)
        if (diff >> k & 1) a = up[a][k]; // 先抬到同一深度

    if (a == b) return a;

    for (int k = LOG - 1; k >= 0; k--)
    {
        if (up[a][k] != up[b][k]) // 还没到公共祖先就一起跳
        {
            a = up[a][k];
            b = up[b][k];
        }
    }
    return up[a][0];
}

void solve()
{
    int n, q;
    cin >> n >> q;

    g.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    dep.assign(n + 1, 0);
    up.assign(n + 1, vector<int>(LOG, 0));
    dfs(1, 0);

    while (q--)
    {
        int a, b;
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
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

LCA、树上两点距离 `dep[a] + dep[b] - 2 * dep[lca]`、树上差分。预处理 O(n log n)，每次查询 O(log n)，空间 O(n log n)。
