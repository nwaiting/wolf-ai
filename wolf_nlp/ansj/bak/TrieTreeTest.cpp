#include <TrieTree.hpp> 
#include <stdio.h>

int main()
{
        TireTree *tree = new TireTree();
        tree->Insert("abc1");
        tree->Insert("abc1");
        tree->Insert("abc1");
        tree->Insert("abc2");
        tree->Insert("abc2");
        tree->Insert("abc3");
        tree->Insert("abc4");
        printf("abc1 %d\n", tree->SearchFre("abc1"));
        printf("abc0 %d\n", tree->SearchFre("abc0"));
        printf("abc2 %d\n", tree->SearchFre("abc2"));
        printf("abc3 %d\n", tree->SearchFre("abc3"));
    return 0;
}

