---
title: "DFS"
date: 2025-11-07 19:15:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

DFS 沿着一条路走到底，走不通再退回上一个分叉。这里用栈代替递归，避免深图爆栈。每访问一个点就标记，外层循环保证每个连通块都会被扫到。下面的 dfs(s, g, vis) 只负责遍历一个连通块，solve 里统计连通块个数。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 遍历一个连通块，vis 记录是否访问过
void dfs(int s, const vector<vector<int>>& g, vector<bool>& vis)
{
    stack<int> st; // 用栈模拟递归，避免深图爆栈
    st.push(s);
    vis[s] = true;

    while (!st.empty())
    {
        int u = st.top();
        st.pop();
        for (int v : g[u])
        {
            if (vis[v]) continue; // 已访问的点不再入栈
            vis[v] = true;
            st.push(v);
        }
    }
}

void solve()
{
    int n, m;
    cin >> n >> m;

    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<bool> vis(n + 1, false);
    int components = 0;
    for (int i = 1; i <= n; i++)
    {
        if (vis[i]) continue;
        components++; // 发现一个新的连通块
        dfs(i, g, vis); // 把这个连通块全部标记
    }

    cout << components << '\n';
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

用来遍历图或树、求连通块、判断连通性。每个点和每条边只处理一次，时间复杂度 O(n+m)，空间 O(n+m)。
