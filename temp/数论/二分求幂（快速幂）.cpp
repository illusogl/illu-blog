#define ll long long
double pow(double x, ll n, double ans)
{
    if (n == 0)
    {
        return ans;
    }
    else if (n > 0)
    {
        if (n % 2 == 1)
        {
            ans *= x;
            return pow(x * x, (n - 1) / 2, ans);
        }
        else
        {
            return pow(x * x, n / 2, ans);
        }
    }
    else
    {
        x = 1 / x;
        return pow(x, -n, ans);
    }
}