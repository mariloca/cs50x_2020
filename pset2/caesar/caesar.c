#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


int main(int argc, string argv[])
{
    int key = 0;
    if (argc == 2)
    {
        string digitcheck = argv[1];
        int digit = 0;
        //Generate the key
        for (int i = 0; i < strlen(digitcheck); i++)
        {
            //Check argv[i] is a digit or not
            if (!isdigit(digitcheck[i]))
            {
                printf("Usage: %s key\n", argv[0]);
                return 1;
            }
            else
            {
                //digitcheck[i]-'0': ASCII - 0 makes a new int
                digit = digit * 10 + digitcheck[i] - '0';
            }
        }
        //Got key, proceed to encipher text
        string plain = get_string("plaintext: ");
        for (int j = 0; j < strlen(plain); j++)
        {
            //Formula: cipher[i] = (plain[i] + key) % 26;
            //Convert only alphabetic character
            if (isalpha(plain[j]))
            {
                if (isupper(plain[j]))
                {
                    //convert plain[i] to alphabetic index (0-26), use formula to calculate new position, then convert back to ASCII
                    //thus to formulate a loop a-z and A-Z
                    plain[j] = (plain[j] - 'A' + digit) % 26 + 'A';
                }
                else
                {
                    plain[j] = (plain[j] - 'a' + digit) % 26 + 'a';
                }
            }
        }
        printf("ciphertext: %s\n", plain);

    }
    else
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    return 0;
}