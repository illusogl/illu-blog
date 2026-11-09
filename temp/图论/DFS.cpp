//https://codeforces.com/contest/893/problem/C
//标准双向图的DFS算法（多次DFS求所有节点）
#include <bits/stdc++.h>
using namespace std;
#define ll long long
void slove()
{
    int n, m;
    cin >> n >> m;
    vector<ll> c(n + 1);
    for (int i = 1; i <= n; i++)
    {
        cin >> c[i];
    }
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
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int t = 1;
    //cin >> t;
    while (t--)
    {
        slove();
    }
    return 0;
}