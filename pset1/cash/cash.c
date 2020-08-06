
#include <cs50.h>
#include <stdio.h>
#include <math.h>
//Use a list of all coins and loop thru it
int main(void)
{
    float change;
    int array[4] = {25, 10, 5, 1};
    do
    {
        change = get_float("Enter the change: ");
    }
    while (change <= 0);
    int cents;
    cents = round(change * 100);
    int i;
    int coins = 0;
    //Loop thru the coin list to calculate the quotient
    for (i = 0; i < 4; i++)
    {
        //cents/array[i] is the quotient divided by each coin
        coins = coins + cents / array[i];
        //remainder will be the next dividend to be divided by
        //next coin
        cents = cents % array[i];
    }
    printf("%i\n", coins);
}