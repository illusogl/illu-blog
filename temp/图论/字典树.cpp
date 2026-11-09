#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define mod (ll)998244353
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
int dic[31000005];
int di[31000005][2];
int T = 30;
ll tot = 0;
void insert(ll x)
{
    ll u = 0;
    for(int i = T - 1; i >= 0; i--)
    {
        int b = (x >> i) & 1;
        if (!di[u][b]) di[u][b] = ++tot;
        u = di[u][b];
        dic[u]++;
    }
}
ll query(ll x, ll k)
{
    int u = 0;
    ll cur = 0;
    ll res = 0;
    for (int i = T - 1; i >= 0; i--)
    {
        int b = (x >> i) & 1;
        int o = di[u][b ^ 1];
        if (o)
        {
            if (cur + (1LL << i) >= k) res += dic[o];      // 整个子树都 >= k
            else { cur += 1LL << i; u = o; continue; }     // 走 b 的子树全 < k, 转进 o
        }
        u = di[u][b];
        if (!u) break;
    }
    return res;
}