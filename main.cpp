#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;

const int N = 10000007;
unsigned long a[20];

void mat_mul(unsigned long A[15][15], unsigned long B[15][15], unsigned long out[15][15], int n)
{
    for (int i=0; i<n; ++i)
    {
        for (int j=0; j<n; ++j)
        {
            unsigned long long sum = 0;
            for (int k=0; k<n; ++k)
            {
                sum = (sum + (A[i][k]*B[k][j] % N)) % N;
            }
            out[i][j] = sum;
        }
    }
}

void mat_exp(unsigned long x[15][15], int n, int y, unsigned long out[15][15])
{
    if (y == 1)
    {
        memcpy(out, x, sizeof(unsigned long)*15*15);
        return;
    }
    unsigned long t[15][15];
    if (y % 2 == 0)
    {
        mat_mul(x, x, t, n);
        mat_exp(t, n, y/2, out);
    }
    else
    {
        mat_exp(x, n, y-1, t);
        mat_mul(x, t, out, n);
    }
}

unsigned long M[15][15];
unsigned long X[15][15];
int main()
{
    int m, n;
    while(~scanf("%d%d", &m, &n))
    {
        a[0] = 911;
        a[m+1] = 1;
        for (int i=1; i<=m; ++i)
        {
            scanf("%d", &a[i]);
        }

        memset(M, 0, sizeof(M));
        M[0][0] = 10;
        M[0][m+1] = 1;
        M[m+1][m+1] = 1;
        for (int i=1; i<=m; ++i)
        {
            for (int j=0; j<=i; ++j)
            {
                M[i][j] = 1;
            }
        }
        mat_exp(M, m+2, n, X);
        unsigned long ans = 0;
        for (int i=0; i<=m+1; ++i)
        {
            ans = (ans + (a[i]*X[m][i] % N)) % N;
        }
        cout << ans << endl;
    }
}
