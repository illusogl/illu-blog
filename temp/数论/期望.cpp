//https://codeforces.com/problemset/problem/453/A
//期望值的标准求法：
//Σ可能值*概率
#include <bits/stdc++.h>
using namespace std;
#define ll long long
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
void solve()
{
    ll n,m;
    //m面骰子，骰n次
    cin >> m >> n;
    double ans = 0;
    vector<double> index(m + 1);
    for(ll i = 1; i <= m; i++)
    {
        index[i] = pow(i*1.0/m,n);
        ans += i * (index[i] - index[i - 1]);
    }
    cout << fixed << setprecision(9) << ans << "\n";
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int t = 1;
    //cin >> t;
    while (t--)
        solve();
    return 0;
}