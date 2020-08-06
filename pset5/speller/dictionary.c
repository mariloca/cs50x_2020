/*Hash Function reference: */
/* http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html */
// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"
#define MULTIPLIER (37)  //For hash function

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

unsigned int wordcnt = 0;

// Number of buckets in hash table
const unsigned int N = 26000; //set initial value to 1

// Hash table
node *table[N] = {0}; //make sure hash table point to NULL

/*============================================================*/

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    unsigned int index;
    node *cursor;
    int i, j = 0;
    char lowerword[LENGTH + 1];
    while (word[j] != '\0')
    {
        lowerword[j] = tolower(word[j]);
        j++;
    }
    lowerword[j] = '\0'; //quick jump out

    index = hash(lowerword) % N; //hash lower case word, since dictionary is also hasing lower case word, make sure same index
    cursor = table[index];
    while (cursor != NULL)
    {
        //i = strcmp(lowerword, cursor->word);
        i = strcasecmp(word, cursor->word);
        if (i == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }

    return false;
}

// Hashes word to a number
//unsigned int hash(const char *word)
unsigned int hash(const char *word)
{
    // TODO
    unsigned int h;
    unsigned const char *us;

    /* cast s to unsigned const char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    us = (unsigned const char *) word;

    h = 0;
    while (*us != '\0')
    {
        h = h * MULTIPLIER + *us;
        us++;
    }

    return h;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    unsigned int index;
    char word[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        fclose(file);
        return false;
    }
    else
    {
        while (fscanf(file, "%s", word) != EOF)
        {
            node *n = malloc(sizeof(node)); //allocate memory for new node
            if (n == NULL)
            {
                fclose(file);
                return false;
            }
            strcpy(n->word, word); //copy word into node.word
            n->next = NULL; //set next pointer to NULL if not know where is next node
            index = hash(word) % N; //hasing the word, find the key, hash(n->word) also works.
            //insert the new node into the first node of the this indexed linked-list
            //if table[index] existed
            if (table[index] != NULL)
            {
                n->next = table[index]; //switch pointer
                table[index] = n;
            }
            else
            {
                table[index] = n;
                n->next = NULL;
            }

            wordcnt++;
        }
        fclose(file);
        return true;
    }
    fclose(file);
    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (wordcnt)
    {
        return wordcnt;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    node *cursor, *next;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        if (cursor == NULL)
        {
            return false;
        }
        while (cursor != NULL)
        {
            next = cursor->next;
            free(cursor);
            cursor = next;
        }
    }
    return sizeof(table) == 0; //same as next 5 lines;
    //if (sizeof(table) != 0) //check if hash table is empty
    //{
    //    return false;
    //}
    //return true;
}
