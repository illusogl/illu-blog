#include<bits/stdc++.h>
#define ll long long
//标准欧几里得辗转相除法
ll gcd(ll a, ll b)
{
	if (a < b)
	{
		ll temp = a;
		a = b;
		b = temp;
	}
	return b == 0 ? a : gcd(b, a % b);
}
//扩展欧几里得算法 求ax + by = gcd（a，b）中的x，y，用于求逆元
//返回值第一个为gcd，第二个为x，第三个为y
//常用解决求余数逆元
std::tuple<ll,ll,ll> gcdE(ll a, ll b)
{
	if (a < b)
	{
		ll temp = a;
		a = b;
		b = temp;
	}//判断大小，如果大小不对则倒转

	if (b == 0)
	{
		return std::make_tuple(a,1,0);
	}//得到答案时返回 ，并从下往上计算x，y

    // 将结构化绑定替换为 std::tie 以兼容旧版 C++（如 VS 默认 C++14/17 支持有限）
    ll gcdNum, x, y;
    std::tie(gcdNum, x, y) = gcdE(b, a % b);
	ll x1 = y;
	ll y1 = x - y * (a / b);
	return std::make_tuple(gcdNum, x1, y1);
	//使用方式
	//ll a, b;
	//cin >> a >> b;
	//ll gcdNum, x, y;
	//tie(gcdNum, x, y) = gcdE(a, b);
}
//类似普通逆元x满足 a * x = 1
//余数逆元x满足 a * x = 1 (mod m) => 即 a * x + m * y = 1
//x = gcdE(a,m)中得出来的第二个数x
