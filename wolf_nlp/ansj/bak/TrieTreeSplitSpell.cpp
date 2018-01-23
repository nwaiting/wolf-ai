#include <TrieTree.hpp>
#include <string>
#include <string.h>
#include <stdio.h>
using namespace std;

int main(int argc, char* argv[])
{
  if(argc != 2) {
    perror("arg not right");
    return -1;
  }

  FILE *pf = fopen(argv[1], "rb");
  if(!pf) {
    perror("read file error");
    return -1;
  }

  TireTree *tree = new TireTree();
  char buf[256];
  memset(buf, 0, sizeof(buf));
  while (fgets(buf, sizeof(buf), pf) != NULL) {
    tree->Insert(buf);
    memset(buf, 0, sizeof(buf));
  }
  fclose(pf);

  string split_spell("qinshimingyuehanshiguan"), result_spell;
  Node *root = tree->GetRootNode();
  for (int i = 0; i < split_spell.size(); i++) {
    std::map<char, Node*>::iterator mapIte = root->GetChildrens().find(split_spell[i]);
    if(mapIte != root->GetChildrens().end()) {
      root = mapIte->second;
      result_spell += split_spell[i];
    }
    else {
      i--;
      result_spell += " ";
      root = tree->GetRootNode();
    }
  }
  printf("%s\n", result_spell.c_str());
  return 0;
}
