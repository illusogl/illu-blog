---
title: "Tarjan 强连通分量"
date: 2026-11-04 21:43:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

Tarjan 用 dfn/low 和栈求强连通分量。dfn 是访问时间，low 是能回到的最早时间；`low[u] == dfn[u]` 时，栈顶到 u 就是一个 SCC。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

vector<vector<int>> g;
vector<int> dfn, low, stk, comp;
vector<bool> inStack;
int timer = 0, sccCnt = 0;

void tarjan(int u)
{
    dfn[u] = low[u] = ++timer;
    stk.push_back(u);
    inStack[u] = true;

    for (int v : g[u])
    {
        if (!dfn[v])
        {
            tarjan(v);
            low[u] = min(low[u], low[v]); // 用儿子的 low 更新
        }
        else if (inStack[v])
        {
            low[u] = min(low[u], dfn[v]); // 回到栈里的点
        }
    }

    if (low[u] == dfn[u]) // u 是这个 SCC 的根
    {
        sccCnt++;
        while (true)
        {
            int v = stk.back();
            stk.pop_back();
            inStack[v] = false;
            comp[v] = sccCnt;
            if (v == u) break;
        }
    }
}

void solve()
{
    int n, m;
    cin >> n >> m;

    g.assign(n + 1, {});
    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
    }

    dfn.assign(n + 1, 0);
    low.assign(n + 1, 0);
    comp.assign(n + 1, 0);
    inStack.assign(n + 1, false);
    timer = sccCnt = 0;

    for (int i = 1; i <= n; i++)
        if (!dfn[i]) tarjan(i);

    cout << sccCnt << '\n';
    for (int i = 1; i <= n; i++) cout << comp[i] << " \n"[i == n];

    // 桥：无向图中若 low[v] > dfn[u]，则边 (u,v) 是桥
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

SCC 缩点、DAG 上 DP、2-SAT。时间复杂度 O(n+m)，空间 O(n+m)。割点和桥的 Tarjan 只需改 `low` 的判断，不需要弹栈。
