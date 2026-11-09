---
title: "DFS"
date: 2026-11-09 20:01:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

DFS 沿着一条路走到底，走不通再退回上一个分叉。这里用栈代替递归，避免深图爆栈。外层循环保证每个点都会被访问到；进入一个连通块后，不断取出栈顶点，把未访问的邻居压栈，同时更新这个连通块里的最小花费。

<!-- more -->

```cpp
void slove()
{
    vector<bool> use(n + 1, false);
    vector<vector<int>> tree(n + 1);
    for (int i = 0; i < m; i++)
    {
        int x, y;
        cin >> x >> y;
        tree[x].push_back(y);
        tree[y].push_back(x);
    }
    ll ans = 0;
    ll minNum;
    int index = 1;
    stack<int> s;
    int temp = 0;
    while (index <= n)
    {
        s.push(index);
        use[index] = true;
        minNum = c[index];
        while (!s.empty())
        {
            temp = s.top();
            s.pop();
            for (int i : tree[temp])
            {
                if (!use[i])
                {
                    use[i] = true;
                    minNum = min(minNum, c[i]);
                    s.push(i);
                }

            }
        }
        ans += minNum;
        while (index <= n && use[index])
        {
            index++;
        }
    }
    cout << ans << "\n";
}
```

用来遍历图或树、求连通块、判断连通性。每个点和每条边只处理一次，时间复杂度 O(n+m)，空间复杂度 O(n+m)。
