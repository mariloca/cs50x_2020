
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height:");
    }
    while (n < 1 || n > 8);
    //Row loop
    for (int i = 1; i < n + 1; i++)
    {
        //First Space loop
        for (int j = 0; j < n - i; j++)
        {
            printf(" ");
        }
        //First Hash loop
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        //print two space before next hash
        printf("  ");
        //Second Hash loop
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}