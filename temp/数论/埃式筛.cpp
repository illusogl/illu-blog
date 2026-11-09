#include <bits/stdc++.h>
using namespace std;
#define ll long long 
vector<ll> get_p()
{
	vector<bool> ans(150000, true);
	vector<ll> ansV(10001);
	ans[0] = false;
	for (ll i = 2; i < 150000; i++)
	{
		if (ans[i])
		{
			for (ll j = i * i; j < 150000; j += i)
			{
				ans[j] = false;
			}
		}
	}
	int index = 0;
	for (int i = 1; i < 150000; i++)
	{
		if (ans[i] && index < 10001)
		{
			ansV[index++] = i;
		}
	}
	return ansV;
}
