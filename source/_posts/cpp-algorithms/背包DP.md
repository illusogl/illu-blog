---
title: "背包 DP"
date: 2026-07-06 10:26:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

背包 DP 用容量作为状态。01 背包倒序枚举容量，保证每个物品只用一次；完全背包正序；多重背包二进制拆分后转 01。恰好装满时 `dp[0]=0`，其余设成负无穷。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 01 背包：dp[j] = 容量 j 的最大价值
vector<int> knapsack01(const vector<int>& w, const vector<int>& v, int W)
{
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); i++)
        for (int j = W; j >= w[i]; j--) // 倒序：每个物品只用一次
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp;
}

// 完全背包：每种物品可以用无限次
vector<int> knapsackComplete(const vector<int>& w, const vector<int>& v, int W)
{
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); i++)
        for (int j = w[i]; j <= W; j++) // 正序：可以重复选
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp;
}

// 多重背包：第 i 种物品有 c[i] 个，二进制拆分后转 01
vector<int> knapsackMultiple(const vector<int>& w, const vector<int>& v, const vector<int>& c, int W)
{
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); i++)
    {
        int cnt = c[i];
        for (int k = 1; k <= cnt; k *= 2)
        {
            int nw = w[i] * k;
            int nv = v[i] * k;
            for (int j = W; j >= nw; j--)
                dp[j] = max(dp[j], dp[j - nw] + nv);
            cnt -= k;
        }
        if (cnt > 0)
        {
            int nw = w[i] * cnt;
            int nv = v[i] * cnt;
            for (int j = W; j >= nw; j--)
                dp[j] = max(dp[j], dp[j - nw] + nv);
        }
    }
    return dp;
}

void solve()
{
    int n, W;
    cin >> n >> W;

    vector<int> w(n), v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];

    vector<int> dp = knapsack01(w, v, W);
    cout << dp[W] << '\n';
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

01/完全/多重/分组背包。01 和完全都是 O(nW)，多重是 O(W * Σ log c)，空间 O(W)。分组背包把每组当成一次 01，组内倒序、组间正序。
