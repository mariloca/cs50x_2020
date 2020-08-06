#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    long number, checknumber;
    long pair;
    int p_digit, a_digit, pairsum, checksum = 0;
    do
    {
        number = get_long("Enter credit card number:");
        //Copy of number to check which credit card issuer
        printf("Number: %li\n", number);
        checknumber = number;
    }
    //When the number is less than 13-digit or bigger than 16-digit, go back to 'do-loop' to enter again.
    //When 'while (expr)' is true, go back to 'do' again; otherwise, break.
    while (!number);
    if (number < pow(10, 13) || number >= pow(10, 16))
    {
        printf("INVALID\n");
        //Exit code stays zero as the program terminates normally
        return 0;
    }
    while (number)
    {
        pair = number % 100;
        p_digit = pair / 10;
        a_digit = pair % 10;
        p_digit *= 2;
        if (p_digit / 10 > 0)
        {
            pairsum = p_digit / 10 + p_digit % 10;
            checksum = checksum + pairsum + a_digit;
        }
        else
        {
            pairsum = p_digit;
            checksum = checksum + pairsum + a_digit;
        }
        number /= 100;
    }
    if (checksum % 10 == 0)
    {
        if ((checknumber / (long)pow(10, 13) == 34) || (checknumber / (long)pow(10, 13) == 37))
        {
            printf("AMEX\n");
        }
        else if (51 <= (checknumber / (long)pow(10, 14)) && (checknumber / (long)pow(10, 14)) <= 55)
        {
            printf("MASTERCARD\n");
        }
        else if ((checknumber / (long)pow(10, 12)) == 4 || (checknumber / (long)pow(10, 15) == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }

    }
    else
    {
        printf("INVALID\n");
    }
    return 0;