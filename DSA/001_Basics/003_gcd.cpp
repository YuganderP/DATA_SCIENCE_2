#include <bits/stdc++.h>
using namespace std;
int main()
{
    int a = 40;
    int b = 80;

    int c = min(a, b);

    for (int i = c; i >= 1; i--)
    {
        if (a % i == 0 && b % i == 0)
        {
            cout << i;
            break;
        }
    }
}