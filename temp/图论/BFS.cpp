//不许删。标准BFS模板
#include <bits/stdc++.h>
using namespace std;
#define ll long long
void slove()
{
	int n, m, k;
	cin >> n >> m >> k;
	vector<int> arr(n + 1);
	for(int i = 1 ; i <= n; i++)
	{
		cin >> arr[i];
	}
	if(n == 1 && m == 0)
	{
		cout << 0 << "\n";
		return;
	}
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
	// 统计答案
	vector<int> ans(k + 1);
	for (int i = 1; i <= n; i++)
	{
		if (dist[i] != -1 && dist[i] < k && ans[arr[i]] < dist[i])
		{
			ans[arr[i]] = dist[i];
		}
	}
	for (int i = 1; i <= k; i++)
	{
		cout << ans[i] << " ";
	}
	cout << "\n";
}
int main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	slove();
	return 0;
}
