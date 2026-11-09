#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long

/*
 * 题目：隐藏树直径（交互题）
 *
 * 核心推导：
 *   1. 经典结论：任选点 r，离 r 最远的点 x 必是直径的一个端点；
 *      离 x 最远的点 y 是另一端，dist(x,y) 即直径长度。
 *   2. 「找离 s 最远的点」用阈值查询 dist(s,v) >= D+1 线性扫描：
 *      - 维护当前最远点 cur 和其精确距离 D。
 *      - 对每个 v：查询 dist(s,v) >= D+1。
 *          若 0：不更新；
 *          若 1：v 更远，cur=v，并把 D 递增到 dist(s,v) 的精确值
 *               （while(dist(s,v) >= D+1) D++）。
 *      查询次数 = (n-1) 次比较 + D 的总增量。
 *   3. 关键优化（把总查询压到 3n）：
 *      第二次找离 x 最远的点时，初始 D 直接设为 dist(x, 1) = 第一次算出的 D1，
 *      而不是 0。这样第二次的 D 增量只有 (直径 - D1)。
 *
 *      总查询 = (n-1) + D1 + (n-1) + (直径 - D1)
 *             = 2(n-1) + 直径  <=  2(n-1) + (n-1) = 3n - 3 < 3n
 */

int n;

int ask(int u, int v, int d)
{
    cout << "? " << u << " " << v << " " << d << "\n";
    cout.flush();
    int r;
    cin >> r;
    return r;
}

// 找离 s 最远的点；初始候选 init，其精确距离 initDist = dist(s, init) 已知
pair<int, int> farthest(int s, int init, int initDist)
{
    int cur = init;
    int D = initDist;
    for (int v = 1; v <= n; v++)
    {
        if (v == init) continue;
        if (ask(s, v, D + 1))
        {
            cur = v;
            D++;
            while (ask(s, v, D + 1)) D++;
        }
    }
    return {cur, D};
}

void solve()
{
    cin >> n;
    auto [x, D1] = farthest(1, 1, 0);      // x 是直径一端
    auto [y, D2] = farthest(x, 1, D1);     // y 是另一端，D2 = 直径
    cout << "! " << x << " " << y << "\n";
    cout.flush(); // 输出直径两端点（若只输出长度则改为 D2）
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    int t = 1;
    cin >> t;
    while (t--) solve();
    return 0;
}
