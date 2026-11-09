#include <bits/stdc++.h>
using namespace std;
//基环数定义：n个顶点n条边，不存在重复路径和自环
//可以得出，图中一定有且只有一个环
void solve()
{
    int n;
    cin >> n;
    vector<vector<int>> g(n + 1);
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < n; i++)
    {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
        deg[u]++;
        deg[v]++;
    }
    
    // 拓扑排序剥叶子
    vector<bool> on_cycle(n + 1, true);  // 先假定所有节点都在环上
    queue<int> q;
    for (int i = 1; i <= n; i++)
    {
        if (deg[i] == 1)
            q.push(i);
    }
    
    while (!q.empty())
    {
        int u = q.front();
        q.pop();
        on_cycle[u] = false;  // 不在环上
        for (int v : g[u])
        {
            if(on_cycle[v])
            {
                deg[v]--;        // 邻居度数减1（相当于删掉了u）
                if (deg[v] == 1) // 如果邻居变成叶子了
                    q.push(v);
            }
        }
    }
    
    // 输出环上的节点
    cout << "环上的节点:";
    for (int i = 1; i <= n; i++)
    {
        if (on_cycle[i])
            cout << " " << i;
    }
    cout << "\n";
}