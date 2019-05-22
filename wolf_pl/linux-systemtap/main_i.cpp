#include <string.h>
#include "main_i.h"

void pre_list(Node *root)
{
    if (!root) {
        std::cout << "is null" << std::endl;
        return;
    }

    std::cout << root->value_ << std::endl;
    pre_list(root->left_);
    pre_list(root->right_);
}

int32_t Solution::maxPathSum(Node *root)
{
    if (!root) {
        return 0;
    }
    result = root->value_;
    helper(root);
    show();
    return result;
}

int32_t Solution::helper(Node *root)
{
    if (!root) {
        return 0;
    }
    int32_t left = helper(root->left_);
    int32_t right = helper(root->right_);
    result = max(result, max(left, 0) + max(right, 0) + root->value_);
    int res = max(root->value_, max(left+root->value_, right+root->value_));
    //cout << "result=" << result << " return=" << res << endl;
    return res;
}

void Solution::show()
{
	cout << "show value is " << show_value << endl;
	show_value++;
	show_this();
}
	

void Solution::show_this()
{
    	char *p = (char*)malloc(500);
	char *q = (char*)"this is";
	memcpy(p, q, strlen(q));
	cout << "q="<<p<<endl;
	free(p);
}





