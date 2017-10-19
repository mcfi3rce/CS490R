#include <stdio.h>

int main(int argc, char **argv)
{
    int a[1000];

    #pragma omp parallel for
    for (int i = 0; i < 1000; i++) {
        a[i] = 2 * i;
	printf(" %d", a[i]);
    }

    return 0;
}
