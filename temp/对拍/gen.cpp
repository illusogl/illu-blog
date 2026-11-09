// 数据生成器：seed 从命令行传入，WA 后可直接复现
// 用法: .\gen 42 > in.txt
// 第二参数可选: big = 稍大规模（n<=60, 值域 11 位），用于第二遍对拍
#include <bits/stdc++.h>
using namespace std;

int main(int argc, char* argv[]) {
    mt19937 rng(atoi(argv[1]));
    // ===== 每道题只改这里：按题意生成一组【小规模】数据 =====
    bool big = argc > 2 && string(argv[2]) == "big";
    int n = 10, m = 100;
    cout << n  << " " << m << "\n";
    for (int i = 1; i <= n; i++)
        cout << rng() % m + 1 << " \n"[i == n];
    // ===== 改到这里为止 =====
    return 0;
}
