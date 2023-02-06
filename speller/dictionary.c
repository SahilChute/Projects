// Implements a dictionary's functionality
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <math.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
// TODO: Choose number of buckets in hash table
unsigned int count;

const unsigned int N = 26;//(maximum case (z+z+z)/3)

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)//correct
{
    node *cursor;
    int h_val = hash(word);
    cursor = table[h_val];
    while(cursor != NULL)
    {
        if( strcasecmp( cursor->word, word ) == 0 )
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int h_val = 0;
    if (strlen(word)>2)
    {
        h_val = round(((toupper(word[0]) + toupper(word[1]) + toupper(word[2])) - (30))/3);
        return h_val;
    }
    else if( strlen(word) ==2)
    {
        h_val = round(((toupper(word[0])) + toupper(word[1])- (20))/2);
        return h_val;
    }
    else if( strlen(word) == 1 )
    {
        h_val = toupper(word[0])- 10;
        return h_val; //returns hash value I didnt check online if anyone has used this hash function yet.
    }
    return false;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)// is correct
{
    FILE *f = fopen( dictionary, "r" );
    char word[LENGTH + 1];
    if(f==NULL)
    {
        printf("file cannot be opened");
        return false;
    }
    while(fscanf( f, "%s" , word )!= EOF)
    {
        node *n = malloc(sizeof(node));
        if(n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        int h_val = hash(word);
        n->next =  table[h_val];
        table[h_val] = n;
        count++;
    }
    fclose(f);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)//no problems here
{
    return count;//we declared count as a global variable.
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)//seems correct
{
    node *cursor;
    node *tmp;
    for (int i = 0; i < N ; i++)
    {
        cursor = table[i];//points to the header
        while ( cursor != NULL)
        {
            tmp = cursor;//points to the node we are about to free
            cursor = cursor->next;//goes to the next node to avoid losing memory
            free(tmp);//free
        }
        if(cursor == NULL)
        {
           return true;//marks end of linked list
        }
    }
    return false;
}
