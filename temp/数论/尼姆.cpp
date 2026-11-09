//https://codeforces.com/problemset/problem/15/C
//尼姆游戏
//基本规则，有n个方格，每个方格有a[i]个物品，两名玩家轮流最少拿一个，最多全拿完
//通解：对0 ~n的a[i]求异或，结果为0一方必胜，不为0另一方赢，结果视情况而定
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define PII pair<int, int>
#define PLL pair<ll, ll>
bool isPrime(int n)
{
    for (int i = 2; i * i <= n; i++)
    {
        if (n % i == 0)
        {
            return false;
        }
    }
    return true;
}
ll F1n(ll n)
{
    //对1~n求异或的解很特殊，通过观察可得
    switch (n % 4)
    {
    case 0:
        return n;
    case 1:
        return 1;
    case 2:
        return n + 1;
    case 3:
        return 0;
    }
}
void solve()
{
    int n;
    cin >> n;
    vector<PLL> arr(n);
    for (int i = 0; i < n; i++)
    {
        ll x, m;
        cin >> x >> m;
        arr[i] = { m,x };
    }
    ll ans = 0;
    for (int i = 0; i < n; i++)
    {
        ans ^= F1n(arr[i].second + arr[i].first - 1) ^ F1n(arr[i].second - 1);
    }
    if (ans)
    {
        cout << "tolik" << "\n";
    }
    else
    {
        cout << "bolik" << "\n";
    }
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
