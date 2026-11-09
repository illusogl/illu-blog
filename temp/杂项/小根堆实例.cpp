//https://codeforces.com/gym/105911/problem/D
#include <bits/stdc++.h>
using namespace std;
#define ll long long
void slove()
{
    int n, a, b, c;
    cin >> n >> a >> b >> c;
    vector<pair<int, int>> x(n), y(n), z(n);
    for (int i = 0; i < n; i++)
    {
        int x1, x2, y1, y2, z1, z2;
        cin >> x1 >> y1 >> z1 >> x2 >> y2 >> z2;
        x[i] = { min(x1,x2),max(x1,x2) };
        y[i] = { min(y1,y2),max(y1,y2) };
        z[i] = { min(z1,z2),max(z1,z2) };
    }
    sort(x.begin(), x.end(),
        [](const pair<int, int>& m, const pair<int, int>& n)
        {
            return m.first < n.first;
        }
    );
    sort(y.begin(), y.end(),
        [](const pair<int, int>& m, const pair<int, int>& n)
        {
            return m.first < n.first;
        }
    );
    sort(z.begin(), z.end(),
        [](const pair<int, int>& m, const pair<int, int>& n)
        {
            return m.first < n.first;
        }
    );
    //小根堆，堆中元素根部一定是最小的
    //priority_queue<PLL,vector<PLL>,greater<PLL>> q_min;
    //大根堆，堆中元素根部一定是最大的
    //priority_queue<PLL,vector<PLL>> q_max;
    priority_queue<int, vector<int>, greater<int>> xs;
    int xmax = 0;
    for (int i = 0; i < n; i++)
    {
        int index = 0;
        while (!xs.empty() && xs.top() < x[i].first)
        {
            xs.pop();
        }
        xs.push(x[i].second);
        if ((int)xs.size() > xmax)
        {
            xmax = xs.size();
        }
    }
    priority_queue<int, vector<int>, greater<int>> ys;
    int ymax = 0;
    for (int i = 0; i < n; i++)
    {
        int index = 0;
        while (!ys.empty() && ys.top() < y[i].first)
        {
            ys.pop();
        }
        ys.push(y[i].second);
        if ((int)ys.size() > ymax)
        {
            ymax = ys.size();
        }
    }
    priority_queue<int, vector<int>, greater<int>> zs;
    int zmax = 0;
    for (int i = 0; i < n; i++)
    {
        int index = 0;
        while (!zs.empty() && zs.top() < z[i].first)
        {
            zs.pop();
        }
        zs.push(z[i].second);
        if ((int)zs.size() > zmax)
        {
            zmax = zs.size();
        }
    }
    cout << max(xmax, max(ymax, zmax));
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t = 1;
    //cin >> t;
    while (t--)
    {
        slove();
    }
    return 0;
}