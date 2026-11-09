#include<bits/stdc++.h>
using namespace std;

using ll = long long;
using i128 = __int128_t;
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
#define fir first
#define sec second
#define fori(begin, end) for (int i = begin; i < end; ++i) 
const int dx[] = {0, -1, 0, 1, 1, -1, -1, 1};
const int dy[] = {1, 0, -1, 0, 1, 1, -1, -1};
const char fk = '\n';



void solve()
{
    int n, M;
    cin >> n >> M;
    vector<ll> a(n);
    fori(0, n) cin >> a[i];

    ll ans = 0;
    vector<int> s(n);
    vector<int> d1(n), d2(n);
    for (int m = 2; m <= M; ++m) {
        fori(0, n) s[i] = a[i] % m;

        for (int i = 0; i < n; ++i) {
            d1[i] = 0;
            while (0 <= i - d1[i] - 1 && n > i + d1[i] + 1 && s[i - d1[i] - 1] == s[i + d1[i] + 1])
                d1[i]++;

            d2[i] = 0;
            while (0 <= i - d2[i] - 1 && n > i + d2[i] && s[i - d2[i] - 1] == s[i + d2[i]])
                d2[i]++;
            ans += d1[i] + d2[i];
        }
    }

    cout << ans << fk;
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int t__ = 1;
    // cin >> t__;
    while(t__--)
        solve();
    return 0;
}
