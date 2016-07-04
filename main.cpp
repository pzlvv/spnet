#include <stdio.h>
#include <iostream>
#include <math.h>
using namespace std;

const int N=10000;
const int M=10000;

int A[N+4][M+4];
int a[N+4];

int solve(int n)
{
    int sum = 0;
    for (int i=1; i<=n; ++i)
    {
	sum += a[i];
    }
    int m = sum/2;

    for (int i=1; i<=n; ++i)
    {
	A[i][0] = 0;
    }
    for (int i=1; i<=m; ++i)
    {
	A[0][i] = 0;
    }

    for (int i=1; i<=n; ++i)
    {
	for (int j=1; j<=m; ++j)
	{
	    A[i][j] = A[i-1][j];
	    if (j-a[i] >= 0)
	    {
		A[i][j] = max(A[i-1][j], A[i-1][j-a[i]]+a[i]);
	    }
	}
    }
    return abs(sum-2*A[n][m]);
}

int main(int argc, char *argv[])
{
    int cases;
    scanf("%d", &cases);
    for (int c=0; c<cases; ++c)
    {
	int n;
	scanf("%d", &n);
	for (int i=1; i<=n; ++i)
	{
	    scanf("%d", &a[i]);
	}
	printf("%d\n", solve(n));
    }
    return 0;
}
