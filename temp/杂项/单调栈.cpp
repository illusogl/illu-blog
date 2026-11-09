#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define mod 998244353
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
void solve()
{
    int n;
    cin >> n;
    vector<int> arr(n + 1);
    for(int i = 1; i < n + 1; i++)
    {
        cin >> arr[i];
    }
    //所有字段最大值减去最小值的和 = 最大值之和 - 最小值之和
    ll ansMax = 0,ansMin = 0;
    //定义leftMax[i]为在arr[i]左边且比arr[i]大的元素下标位置，如不存在则返回0；
    //ansMax += arr[i] * (i - leftMax[i]) * (rightMax[i] - i) 
    vector<ll> leftMin(n + 1),rightMin(n + 1) ,leftMax(n + 1), rightMax(n + 1);
    stack<ll> slma,slmi,srma,srmi;
    //对于leftMax[i]计算用单调递减栈维护，如果栈顶小于arr[i]，弹栈直到遇到比他大的元素，插入并返回那个值，如果没有则返回0
    for(int i = 1; i < n + 1; i++)
    {
        while(slma.size() > 0)
        {
            if(arr[slma.top()] <= arr[i])
            {
                slma.pop();
            }
            else
            {
                leftMax[i] = slma.top();
                slma.push(i);
                break;
            }
        }
        if(slma.size() == 0)
        {
            slma.push(i);
            leftMax[i] = 0;
        }
    }
    for(int i = n; i > 0; i--)
    {
        while(srma.size() > 0)
        {
            if(arr[srma.top()] < arr[i])
            {
                srma.pop();
            }
            else
            {
                rightMax[i] = srma.top();
                srma.push(i);
                break;
            }
        }
        if(srma.size() == 0)
        {
            srma.push(i);
            rightMax[i] = n + 1;
        }
    }
    for(int i = 1; i < n + 1; i++)
    {
        while(slmi.size() > 0)
        {
            if(arr[slmi.top()] >= arr[i])
            {
                slmi.pop();
            }
            else
            {
                leftMin[i] = slmi.top();
                slmi.push(i);
                break;
            }
        }
        if(slmi.size() == 0)
        {
            slmi.push(i);
            leftMin[i] = 0;
        }
    }
    for(int i = n; i > 0; i--)
    {
        while(srmi.size() > 0)
        {
            if(arr[srmi.top()] > arr[i])
            {
                srmi.pop();
            }
            else
            {
                rightMin[i] = srmi.top();
                srmi.push(i);
                break;
            }
        }
        if(srmi.size() == 0)
        {
            srmi.push(i);
            rightMin[i] = n + 1;
        }
    }
    for(int i = 1; i < n + 1; i++)
    {
        ansMax += (ll)arr[i] * (i - leftMax[i]) * (rightMax[i] - i);
        ansMin += (ll)arr[i] * (i - leftMin[i]) * (rightMin[i] - i);
    }
    cout << ansMax - ansMin << "\n";
}