#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc == 2)
    {
        //Check key length is 26
        if (strlen(key) == 26)
        {
            for (int i = 0; i < strlen(key); i++)
            {
                //Check all key chars are alpha chars
                if (isalpha(key[i]))
                {
                    //Check key chars are non-repeated
                    //Compare key[i] with key[i+1], using one loop
                    for (int j = i + 1; j < strlen(key); j++)
                    {
                        if (key[i] == key[j])
                        {
                            printf("Key must not contain repeated characters.\n");
                            return 1;
                        }
                    }
                }
                else
                {
                    printf("Key must only contain alphabetic characters.\n");
                    return 1;
                }
            }
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

        //Encifer
        string plain = get_string("plaintext: ");
        int index = 0;
        for (int j = 0; j < strlen(plain); j++)
        {
            if (isalpha(plain[j]))
            {
                if (isupper(plain[j]))
                {
                    //find index of each char in plaintext in the original ASCII chart
                    index = plain[j] % 'A';
                    plain[j] = toupper(key[index]);
                }
                else
                {
                    index = plain[j] % 'a';
                    plain[j] = tolower(key[index]);
                }
            }
        }
        printf("ciphertext: %s\n", plain);
    }
    else
    {
        //Empty input or more than 2 arguments
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    return 0;
}