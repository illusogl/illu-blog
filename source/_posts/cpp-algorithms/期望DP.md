---
title: "期望 DP"
date: 2026-10-04 16:05:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

期望 DP 把“还要多少步/多少代价”作为状态，通常倒推：`E[i] = 1 + Σ p * E[next]`。有环时不能直接递推，需要解方程或高斯消元。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve()
{
    int n, m;
    cin >> n >> m; // 掷 m 面骰子，求达到 >= n 的期望次数

    vector<double> E(n + 1, 0);
    E[n] = 0; // 已经达到目标

    for (int i = n - 1; i >= 0; i--)
    {
        E[i] = 1; // 先算这一步
        for (int x = 1; x <= m; x++)
        {
            int nxt = min(n, i + x); // 超过 n 也视为到达
            E[i] += E[nxt] / m;
        }
    }

    cout << fixed << setprecision(9) << E[0] << '\n';
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

期望 DP、概率 DP、收集问题、步数期望。线性递推 O(nm)，空间 O(n)。概率/期望取模时把除法换成逆元；状态转移有环时用高斯消元或迭代。
