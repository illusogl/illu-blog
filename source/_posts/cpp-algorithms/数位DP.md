---
title: "数位 DP"
date: 2026-10-14 10:35:00
categories:
  - "算法"
tags:
  - "算法"
  - "DP"
  - "C++"
---

数位 DP 按十进制位从高到低枚举。`tight` 表示是否贴着上界，`started` 处理前导零；把题目条件写进枚举下一位的判断里。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

ll memo[20][2][2];
int a[20];

// 统计 [0, x] 中不含数字 4 的数的个数
ll dfs(int pos, bool tight, bool started)
{
    if (pos == -1) return 1;

    ll &res = memo[pos][tight][started];
    if (res != -1) return res;

    res = 0;
    int up = tight ? a[pos] : 9;
    for (int d = 0; d <= up; d++)
    {
        if (d == 4) continue; // 题目条件：不能出现 4
        res += dfs(pos - 1, tight && d == up, started || d != 0);
    }
    return res;
}

ll count(ll x)
{
    if (x < 0) return 0;

    int len = 0;
    while (x > 0)
    {
        a[len++] = x % 10;
        x /= 10;
    }

    memset(memo, -1, sizeof(memo));
    return dfs(len - 1, true, false);
}

void solve()
{
    ll L, R;
    cin >> L >> R;
    cout << count(R) - count(L - 1) << '\n';
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

区间计数、数位和、windy 数、不含某数字。复杂度 O(位数 * 状态数 * 10)，空间 O(位数 * 状态数)。注意前导零和上界，`count(0)` 是否算 0 要看题目。
