---
title: "区间 DP"
date: 2026-08-22 15:44:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

区间 DP 以区间长度为阶段，`dp[l][r]` 表示区间 `[l,r]` 的最优值，枚举断点 `k` 合并左右两段。先算短区间，再算长区间。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = 0x3f3f3f3f3f3f3f3fLL;

void solve()
{
    int n;
    cin >> n;

    vector<ll> a(n + 1), pre(n + 1, 0);
    for (int i = 1; i <= n; i++)
    {
        cin >> a[i];
        pre[i] = pre[i - 1] + a[i];
    }

    // dp[l][r]：把 a[l..r] 合并成一堆的最小代价
    vector<vector<ll>> dp(n + 1, vector<ll>(n + 1, 0));
    for (int len = 2; len <= n; len++) // 区间长度从小到大
    {
        for (int l = 1; l + len - 1 <= n; l++)
        {
            int r = l + len - 1;
            dp[l][r] = INF;

            for (int k = l; k < r; k++) // 断点：左边 [l,k]，右边 [k+1,r]
            {
                ll cost = dp[l][k] + dp[k + 1][r] + pre[r] - pre[l - 1];
                dp[l][r] = min(dp[l][r], cost);
            }
        }
    }

    cout << dp[1][n] << '\n';
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

石子合并、括号匹配、回文分割。时间复杂度 O(n^3)，空间 O(n^2)。环形区间把数组复制一份接在后面，长度开到 2n。
