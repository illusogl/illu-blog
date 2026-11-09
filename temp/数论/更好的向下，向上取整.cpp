#define ll long long
//适应负数的向下向上取整
//向下取整
ll floor_div(ll a, ll b) {
    return a / b - (a % b && (a ^ b) < 0);
}

//向上取整
ll ceil_div(ll a, ll b) {
    return a / b + (a % b != 0 && (a ^ b) >= 0);
}