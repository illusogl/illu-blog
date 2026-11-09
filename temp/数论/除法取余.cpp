#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define mod (ll)998244353
ll mypow(ll x, ll n, ll ans)
{
    if (n == 0)
    {
        return ans;
    }
    else if (n > 0)
    {
        if (n % 2 == 1)
        {
            ans = (ans * x) % mod;
            return mypow((x * x)% mod, (n - 1) / 2, ans);
        }
        else
        {
            return mypow((x * x)% mod, n / 2, ans);
        }
    }
}
//对于除法取余 (a / b) % mod 一般可以看成 a * pow(b,mod - 2) % mod;
//在这个函数中
void slove()
{
    int a,b;
    int temp = 1;
    int ans = a * (mypow(b,mod - 2,temp)) % mod;
}