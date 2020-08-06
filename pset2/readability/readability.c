#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int countletters(string text);
int countwords(string text);

int main(void)
{
    string text = get_string("Text: ");
    //Count sentences
    int sentences = 0;
    int words, letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences ++;
        }
        words = countwords(text);
        letters = countletters(text);
    }
    //float letters/words/sentences will avoid truncate quotient, because dividing int, the result will also be int, digits after decimal point will be discarded.
    float index = round(0.0588 * ((float)letters * 100 / (float)words) - 0.296 * ((float)sentences * 100 / (float)words) - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }
}


//Count letters
int countletters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //letters from A~z, use single quotation mark for single char, ex: 'A'
        if (text[i] >= 'A' && text[i] <= 'z')
        {
            letters ++;
        }
    }
    return letters;
}

//Count words
int countwords(string text)
{
    int words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }
    //Add last word
    words += 1;
    return words;
}