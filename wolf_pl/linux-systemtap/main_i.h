#ifndef __MAIN_I_H__
#define __MAIN_I_H__

#include <iostream>
#include <memory>
#include <string>
#include <algorithm>

using namespace std;

struct Node {
    int value_;
    Node *left_;
    Node *right_;
};

extern void pre_list(Node *root);

class Solution
{
public:
    int32_t result;
    int32_t show_value;
    int32_t maxPathSum(Node *root);
    int32_t helper(Node *root);
    void show();
    void show_this();
};

#endif
