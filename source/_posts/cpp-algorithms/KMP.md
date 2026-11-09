---
title: "KMP"
date: 2026-11-09 20:18:00
categories:
  - "算法"
tags:
  - "算法"
  - "杂项"
  - "C++"
---

KMP 先对模式串求前缀函数 nxt：nxt[i] 是 s[0..i] 的最长相等真前缀和真后缀的长度。匹配时文本指针只往前走，失配了就让模式串指针退回 nxt[index-1]，不用回到开头。匹配成功后同样回退，可以继续找下一次出现。

<!-- more -->

```cpp
// GetNeed：前缀函数（next 数组）—— 背板模板，一个字都别改
//
// nxt[i] = s[0..i] 的最长“真前缀 == 真后缀”的长度
// 含义：当 s[j] 失配时，j 退到 nxt[j-1] 继续比，文本指针永不回退
//
// 例：s = [1,1,2]   -> nxt = [0,1,0]
//     s = [1,2,1,2] -> nxt = [0,0,1,2]
// 常考：最小循环节长度 = n - nxt[n-1]（n % 该长度 == 0 时整串是循环节拼的）
vector<int> GetNeed(vector<int>& s)
{
    int n = s.size();
    vector<int> nxt(n, 0);        // nxt[0] 恒为 0
    int j = 0;                    // j = 已匹配的前后缀长度，下一步比较 s[j]
    for (int i = 1; i < n; i++)   // 从 1 开始
    {
        // 失配：沿“前缀链”回退，直到能接上或退到 0
        while (s[j] != s[i] && j != 0)
            j = nxt[j - 1];       // ★ 唯一要背的一句：必须是 nxt[j-1]（写 s[j-1] 会死循环）
        if (s[j] == s[i]) j++;    // 接上了，长度 +1
        nxt[i] = j;               // 记录
    }
    return nxt;
}

// ============================================================
// KMP：比赛时只改这个函数的“匹配成功”分支
// 版本 1：返回第一次出现的【结尾下标】，没有返回 -1
// 想要【起始下标】-> return i - m + 1;
// ============================================================
int KMP_first(vector<int>& a, vector<int>& b)
{
    if (b.empty()) return -1;               // 边界：空模式串，按题目约定
    vector<int> nxt = GetNeed(b);           // 前缀表只跟模式串有关，原样调用
    int n = a.size(), m = b.size();
    int index = 0;                          // 当前已匹配的模式串长度
    for (int i = 0; i < n; i++)             // 文本指针 i 只前进不回退，O(n+m)
    {
        while (a[i] != b[index] && index > 0)
            index = nxt[index - 1];         // 失配：模式串指针按前缀表回退
        if (a[i] == b[index]) index++;      // 匹配：长度 +1
        if (index == m)                     // ★★ 匹配成功：改这里！★★
        {
            return i;                       // 要起始位置就写 return i - m + 1;
        }
    }
    return -1;                              // 没找到
}
int KMP(vector<int> &a,vector<int> &b)
{
    vector<int> next = GetNeed(b);
    int n = a.size(); int m = b.size();
    int index = 0;
    int ans = 0;
    for(int i = 0; i < n; i++)
    {
        while(a[i] != b[index] && index > 0)
        {
            index = next[index - 1];
        }
        if(a[i] == b[index])
        {
            index++;
        }
        if(index == m)
        {
            ans++;
            index = next[index - 1];
        }
    }
    return ans;
}
```

在文本里找子串、统计出现次数、求最小循环节。预处理 O(m)，匹配 O(n)，总时间复杂度 O(n+m)，空间 O(m)。
