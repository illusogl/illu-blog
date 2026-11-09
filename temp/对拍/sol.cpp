#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define mod (ll)(998244353)
using PII = pair<int, int>;
using PLL = pair<ll, ll>;
int dx[8] = {0,1,0,-1,-1,-1,1,1};
int dy[8] = {1,0,-1,0,-1,1,-1,1};
const ll mask = (1LL << 31) - 1; 
static int lowbit(int x) { return x & (-x); }
int yinzi[100001]={0};
ll max(ll a,ll b){
    if(a>b) return a;
    else return b;
}
int gcd(int a,int b){
    while(b!=0){
        int t=b;
        b=a%b;
        a=t;
    }
    return a;
}
ll cou(ll g, ll m){
    if(g == 0){
        return m-1;
    }
    return yinzi[g];
}
void solve(){
    for(int i=2;i<=100000;i++){
        for(int j=2;j*j<=i;j++){
            if(i%j==0){
                if(j*j!=i) yinzi[i]+=2;
                else yinzi[i]+=1;
            }
        }
        yinzi[i]++;
    }
}
void f(){
    int n,m;
    int a[10000];
    scanf("%d %d",&n,&m);
    for(int i=1;i<=n;i++){
        scanf("%d",&a[i]);
    }
    ll res=0;
    for(int i=1;i<n;i++){
        int l=i,r=i+1;
        ll g=abs(a[l]-a[r]);
        res+=cou(g,m);
        while(l-1>=1&&r+1<=n){
            l--,r++;
            ll d=abs(a[l]-a[r]);
            g=gcd(g,d);
            res+=cou(g,m);
        }
    }
    for(int i=1;i<=n;i++){
        int l=i,r=i;
        ll g=0;
        while(l-1>=1&&r+1<=n){
            l--,r++;
            ll d=abs(a[l]-a[r]);
            g=gcd(g,d);
            res+=cou(g,m);
        }
    }
    cout << res << "\n";
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    int t = 1;
    //cin >> t;
    while (t--) solve();
    return 0;
}