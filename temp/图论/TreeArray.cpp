#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define mod (ll)(1000000007)
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
int dx[8] = {0,1,0,-1,-1,-1,1,1};
int dy[8] = {1,0,-1,0,-1,1,-1,1};
const ll mask = (1LL << 31) - 1;
 
static int lowbit(int x) { return x & (-x); }
// ============================================================
// 树状数组（Fenwick Tree）
// 支持：
//   1. 单点加：a[i] += v
//   2. 前缀和：a[1] + ... + a[i]
//   3. 区间和：a[l] + ... + a[r]
// 下标一律从 1 开始。
// 时间复杂度：add / sum 都是 O(log n)，build 是 O(n)。
// ============================================================
struct Fenwick
{
    int n;
    vector<ll> bit;

    Fenwick(int n = 0)
    {
        init(n);
    }

    void init(int n_)
    {
        n = n_;
        bit.assign(n + 1, 0);
    }

    // a[i] += v
    void add(int i, ll v)
    {
        for (; i <= n; i += i & -i)
        {
            bit[i] += v;
        }
    }

    // a[1] + a[2] + ... + a[i]
    ll sum(int i) const
    {
        ll res = 0;
        for (; i > 0; i -= i & -i)
        {
            res += bit[i];
        }
        return res;
    }

    // a[l] + ... + a[r]
    ll rangeSum(int l, int r) const
    {
        if (l > r) return 0;
        return sum(r) - sum(l - 1);
    }

    // O(n) 建树，a 的下标从 1 开始
    void build(const vector<ll>& a)
    {
        init((int)a.size() - 1);
        for (int i = 1; i <= n; i++)
        {
            bit[i] += a[i];
            int j = i + (i & -i);
            if (j <= n)
            {
                bit[j] += bit[i];
            }
        }
    }
};

// ============================================================
// 使用示例：单点加 + 区间和
// 输入格式：
//   n q
//   a1 a2 ... an
//   然后 q 行操作：
//     1 i x   -> a[i] += x
//     2 l r   -> 输出 a[l] + ... + a[r]
// ============================================================
void solve()
{
    int n, q;
    cin >> n >> q;

    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++)
    {
        cin >> a[i];
    }

    Fenwick fw;
    fw.build(a);

    while (q--)
    {
        int op;
        cin >> op;

        if (op == 1)
        {
            int i;
            ll x;
            cin >> i >> x;
            fw.add(i, x);
        }
        else
        {
            int l, r;
            cin >> l >> r;
            cout << fw.rangeSum(l, r) << "\n";
        }
    }
}

// ============================================================
// 如果把某个位置“改成” v，而不是加 v：
//   需要额外保存原数组 a
//   fw.add(i, v - a[i]);
//   a[i] = v;
//
// 求排列 P[1..n] 的逆序数：
//   Fenwick fw(n);
//   ll inv = 0;
//   for (int i = n; i >= 1; i--)
//   {
//       inv += fw.sum(P[i] - 1);   // 右边比 P[i] 小的个数
//       fw.add(P[i], 1);
//   }
//   只要奇偶：parity ^= (fw.sum(P[i] - 1) & 1);
// ============================================================

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);

    int t = 1;
    // cin >> t;   // 多组测试数据时取消注释
    while (t--) solve();

    return 0;
}
