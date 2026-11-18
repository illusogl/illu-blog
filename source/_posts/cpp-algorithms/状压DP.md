---
title: "状压 DP"
date: 2026-09-28 20:25:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

状压 DP 用一个整数的二进制位表示集合，dp[mask] 或 dp[mask][i] 存这个集合的最优值。转移时枚举没选过的元素，或者枚举子集。n 一般不超过 20。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve()
{
    int n;
    cin >> n;

    vector<vector<int>> w(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> w[i][j];

    const int INF = 0x3f3f3f3f;
    int full = (1 << n) - 1;

    // dp[mask][u]：已访问集合 mask，最后停在 u 的最小花费
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0; // 从 0 出发

    for (int mask = 1; mask <= full; mask++)
    {
        for (int u = 0; u < n; u++)
        {
            if (dp[mask][u] == INF) continue;

            for (int v = 0; v < n; v++)
            {
                if (mask >> v & 1) continue; // v 已经访问过
                int nmask = mask | (1 << v); // 把 v 加入集合
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + w[u][v]);
            }
        }
    }

    // 回到起点 0；如果只要求走遍所有点，去掉 w[i][0]
    int ans = INF;
    for (int i = 0; i < n; i++)
        ans = min(ans, dp[full][i] + w[i][0]);
    cout << ans << '\n';

    // 枚举子集：for (int sub = mask; sub; sub = (sub - 1) & mask) { ... }
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

TSP、覆盖、分组选择、子集划分。枚举元素转移是 O(2^n * n^2)，枚举子集是 O(3^n)；空间 O(2^n * n)。n 超过 20 一般就放不下了。
