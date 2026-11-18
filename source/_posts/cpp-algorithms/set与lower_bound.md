---
title: "set 与 lower_bound"
date: 2025-10-02 13:59:00
categories:
  - "算法"
tags:
  - "算法"
  - "杂项"
  - "C++"
---

set 是有序去重的平衡树，lower_bound/upper_bound 是它最常用的操作。set 自带的 lower_bound 是 O(log n)，不要对 set 用 std::lower_bound，那是 O(n)。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve()
{
    int n, q;
    cin >> n >> q;

    set<int> s;
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        s.insert(x);
    }

    while (q--)
    {
        int op, x;
        cin >> op >> x;

        if (op == 1)
        {
            s.insert(x); // 插入，重复元素会被忽略
        }
        else if (op == 2)
        {
            auto it = s.find(x);
            if (it != s.end()) s.erase(it); // 只删一个
        }
        else if (op == 3)
        {
            auto it = s.lower_bound(x); // 第一个 >= x 的位置
            if (it == s.end()) cout << -1 << '\n';
            else cout << *it << '\n';
        }
        else
        {
            auto it = s.upper_bound(x); // 第一个 > x 的位置
            if (it == s.begin()) cout << -1 << '\n';
            else
            {
                --it; // 前驱：最后一个 < x
                cout << *it << '\n';
            }
        }
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

维护有序集合、找前驱/后继。插入、删除、查找、lower_bound/upper_bound 都是 O(log n)，空间 O(n)。静态数据直接排序后用 vector 的 lower_bound 更快；multiset 要删一个元素用 `erase(find(x))`，`erase(x)` 会删掉所有 x。
