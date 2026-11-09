---
title: "BFS"
date: 2026-11-09 20:00:00
categories:
  - "算法"
tags:
  - "算法"
  - "图论"
  - "C++"
---

BFS 从起点开始按层扩展。队列里放待访问的点，每次取出队首，把还没访问过的邻居加进队列，并把它们的距离记成当前点的距离加一。每个点只入队一次，所以第一次访问到它时，经过的边数就是最短距离。代码后半段按颜色统计答案，是这道题自己的处理，套模板时只留 BFS 部分即可。

<!-- more -->

```cpp
void slove()
{
	vector<vector<int>> load(m + 1);
	for (int i = 0; i < m; i++)
	{
		int u, v;
		cin >> u >> v;
		load[u].push_back(v);
		load[v].push_back(u);
	}
	vector<int> dist(n + 1, -1);
	// BFS
	queue<int> q;
	dist[1] = 0;
	q.push(1);
	while (!q.empty())
	{
		int node = q.front();
		q.pop();
		for(int n : load[node])
		{
			if(dist[n] == -1)
			{
				dist[n] = dist[node] + 1;
				q.push(n);
			}
		}
	}
	cout << "\n";
}
```

适合边权相同或边权为 1 的图求最短路，也常用来按层遍历和统计连通块。每个点和每条边只处理一次，时间复杂度 O(n+m)，空间复杂度 O(n+m)。
