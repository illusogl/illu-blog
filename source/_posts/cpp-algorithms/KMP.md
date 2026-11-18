---
title: "KMP"
date: 2026-05-14 21:18:00
categories:
  - "算法"
tags:
  - "算法"
  - "杂项"
  - "C++"
---

KMP 先对模式串 p 求前缀函数 nxt：nxt[i] 是 p[0..i] 的最长相等真前缀和真后缀的长度。匹配时文本指针只往前走，失配了就让模式串指针退回 nxt[index-1]，不用回到开头。匹配成功后同样回退，可以继续找下一次出现。

<!-- more -->

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 前缀函数：nxt[i] = p[0..i] 的最长相等前后缀长度
vector<int> prefixFunction(const vector<int>& p)
{
    int m = (int)p.size();
    vector<int> nxt(m, 0);
    for (int i = 1, j = 0; i < m; i++)
    {
        // 失配：沿前缀链回退
        while (j > 0 && p[i] != p[j]) j = nxt[j - 1];
        if (p[i] == p[j]) j++; // 接上了，匹配长度 +1
        nxt[i] = j; // nxt[i] = p[0..i] 的最长相等前后缀长度
    }
    return nxt;
}

// 返回第一次出现的起始下标，找不到返回 -1
int kmpFirst(const vector<int>& s, const vector<int>& p)
{
    if (p.empty()) return -1;
    vector<int> nxt = prefixFunction(p);
    int m = (int)p.size();
    for (int i = 0, j = 0; i < (int)s.size(); i++)
    {
        while (j > 0 && s[i] != p[j]) j = nxt[j - 1];
        if (s[i] == p[j]) j++;
        if (j == m) return i - m + 1; // 第一次匹配成功
    }
    return -1;
}

// 统计出现次数，允许重叠
int kmpCount(const vector<int>& s, const vector<int>& p)
{
    if (p.empty()) return 0;
    vector<int> nxt = prefixFunction(p);
    int m = (int)p.size(), cnt = 0;
    for (int i = 0, j = 0; i < (int)s.size(); i++)
    {
        while (j > 0 && s[i] != p[j]) j = nxt[j - 1];
        if (s[i] == p[j]) j++;
        if (j == m)
        {
            cnt++;
            // 继续找下一次出现，允许重叠
            j = nxt[j - 1];
        }
    }
    return cnt;
}

void solve()
{
    int n, m;
    cin >> n >> m;

    vector<int> s(n), p(m);
    for (int& x : s) cin >> x;
    for (int& x : p) cin >> x;

    cout << kmpFirst(s, p) << '\n';
    cout << kmpCount(s, p) << '\n';
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

在文本里找子串、统计出现次数、求最小循环节。预处理 O(m)，匹配 O(n)，总时间复杂度 O(n+m)，空间 O(m)。
