---
title: "树形 DP"
date: 2026-07-15 23:52:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

树形 DP 在 DFS 回溯时合并子树。`dp[u][0/1]` 表示 u 选或不选的最优值，父亲的状态决定儿子的转移。下面以“树的最大独立集”为例。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

vector<vector<int>> g;
vector<ll> val, dp0, dp1;

void dfs(int u, int p)
{
    dp1[u] = val[u]; // 选 u
    dp0[u] = 0;      // 不选 u

    for (int v : g[u])
    {
        if (v == p) continue;
        dfs(v, u);

        dp0[u] += max(dp0[v], dp1[v]); // 不选 u，儿子可选可不选
        dp1[u] += dp0[v];              // 选 u，儿子不能选
    }
}

void solve()
{
    int n;
    cin >> n;

    val.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> val[i];

    g.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    dp0.assign(n + 1, 0);
    dp1.assign(n + 1, 0);
    dfs(1, 0); // 以 1 为根

    cout << max(dp0[1], dp1[1]) << '\n';
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

树的最大独立集、子树大小、选课、换根 DP。每个点只访问一次，时间复杂度 O(n)，空间 O(n)。换根 DP 先算子树答案，再用父亲的信息更新儿子。
