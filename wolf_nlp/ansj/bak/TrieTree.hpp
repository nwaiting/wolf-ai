#include <map>
#include <string>

class Node
{
public:
  Node(const std::string& str=std::string()) {
    contents_ = str;
    fre_ = -1;
    root_ = false;
    end_ = false;
  }
  ~Node();
public:
  std::string GetContent() const {
    return contents_;
  }
  void SetContent(const std::string& str) {
    contents_ = str;
  }
  int GetFre() const {
    return fre_;
  }
  void SetFre(int f) {
    fre_ = f;
  }
  bool IsEnd() const {
    return end_;
  }
  void SetIsEnd(bool flag) {
    end_ = flag;
  }
  bool IsRoot() {
    return root_;
  }
  void SetRoot(bool flag) {
    root_ = flag;
  }
  std::map<char, Node*>& GetChildrens() {
    return childrens_;
  }
  void SetChildrens(const std::map<char, Node*>& childs) {
    childrens_ = childs;
  }
private:
  char c_;
  std::string contents_;
  int fre_;
  bool end_;
  bool root_;
  std::map<char, Node*> childrens_;
};

class TrieTree
{
public:
  TrieTree(){
    root_p_ = new Node("root");
    root_p_->SetRoot(true);
    root_p_->SetFre(0);
    root_p_->SetIsEnd(false);
  }
  ~TrieTree();

public:
  void Insert(const std::string& str){
    Node *proot = root_p_;
    for(int index = 0; index < str.size(); index++) {
      std::map<char, Node*>::iterator mapIte = proot->GetChildrens().find(str[index]);
      if (mapIte != proot->GetChildrens().end()) {
        if(index == str.size() - 1) {
          Node *node = mapIte->second;
          node->SetFre(node->GetFre() + 1);
          node->SetIsEnd(true);
        }
      }
      else {
        Node *node = new Node();
        count_++;
        if (index == str.size()-1) {
          node->SetFre(1);
          node->SetIsEnd(true);
        }
        else {
          node->SetFre(0);
        }
        proot->GetChildrens().insert(std::pair<char,Node*>(str[index], node));
      }

      proot = proot->GetChildrens().find(str[index])->second;
    }
  }

  int SearchFre(const std::string& str) {
    int fre = -1;
    Node *node = root_p_;
    for (int index = 0; index < str.size(); index++) {
      std::map<char, Node*>::iterator mapIte = node->GetChildrens().find(str[index]);
      if(mapIte != node->GetChildrens().end()) {
        node = mapIte->second;
        fre = node->GetFre();
      }
      else {
        fre = -1;
        break;
      }
    }
    return fre;
  }

  Node* GetRootNode() const {
    return root_p_;
  }

  int GetSize() const {
    return count_;
  }

private:
  Node *root_p_;
  int count_;
};
