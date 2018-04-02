
#include <cstdlib>
#include <set>
#include <string>
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

#define ALPHABET_NUMBER 26

struct StateNode
{
    bool finish_{ false };
    int state_{ 0 };
    string pattern_{};
    //goto table
    vector<StateNode *> transition_table_{ vector<StateNode *>(ALPHABET_NUMBER) };
};

class ACSM
{
private:
    StateNode *start_node_;
    int state_count_;
    vector<StateNode *> corresponding_node_;
    vector<StateNode *> fail_;
public:
    ACSM() :start_node_{ new StateNode() }, state_count_{ 0 }
    {
        //state0 is start_node_
        corresponding_node_.push_back(start_node_);
    }
    //read all patterns and produce the goto table
    void load_pattern(const vector<string> &_Patterns)
    {
        int latest_state = 1;
        for (const auto &pattern : _Patterns)
        {
            auto *p = start_node_;
            for (int i = 0; i < pattern.size(); ++i)
            {
                auto *next_node = p->transition_table_[pattern[i] - 'a'];
                if (next_node == nullptr)
                {
                    next_node = new StateNode();
                }
                if (next_node->state_ == 0)
                {
                    next_node->state_ = latest_state++;
                    //update the table
                    corresponding_node_.push_back(next_node);
                }
                //the goto table
                p->transition_table_[pattern[i] - 'a'] = next_node;
                p = next_node;
            }
            p->finish_ = true;
            p->pattern_ = pattern;
        }
        for (int i = 0; i < ALPHABET_NUMBER; ++i)
        {
            if (start_node_->transition_table_[i] == nullptr)
            {
                start_node_->transition_table_[i] = start_node_;
            }
        }
        state_count_ = latest_state;
    }
    //produce fail function
    void dispose()
    {
        queue<StateNode *> q;
        fail_ = std::move(vector<StateNode *>(state_count_));
        // 给深度为1的复制为0
        for (const auto nxt : start_node_->transition_table_)
        {
            //d=1,f=0
            if (nxt->state_ != 0)
            {
                fail_[nxt->state_] = start_node_;
                q.push(nxt);
            }
        }
        //calculate all fail redirection
        while (!q.empty())
        {
            auto known = q.front();
            q.pop();
            for (int i = 0; i < ALPHABET_NUMBER; ++i)
            {
                auto nxt = known->transition_table_[i];
                if (nxt && nxt->state_ != 0)
                {
                    //上一级的fail的同条件的，
                    //比如：如果在状态8失败，那么先求fail(7)，然后在fail(7)条件下goto，条件为到从7到8的条件c，然后goto(fail(7),c)
                    auto p = fail_[known->state_];
                    //这里...？？？
                    while (!p->transition_table_[i])
                    {
                        p = fail_[p->state_];
                    }
                    fail_[nxt->state_] = p->transition_table_[i];
                    q.push(nxt);
                }
            }
        }
    }
    //search matching
    void match(const string &_Str, set<string> &_S)
    {
        auto p = start_node_;
        for (int i = 0; i < _Str.size(); ++i)
        {
            int trans = _Str[i] - 'a';
            p = p->transition_table_[trans] ? p->transition_table_[trans] : (--i, fail_[p->state_]);
            if (p->finish_)
            {
                _S.insert(p->pattern_);
            }
        }
    }
};

int main()
{
    ACSM acsm;
    vector<string> patterns{ "his","hers","she","he" };
    set<string> matched;
    acsm.load_pattern(patterns);
    acsm.dispose();
    string str{ "hishers" };
    acsm.match(str, matched);
    for (const auto str : matched)cout << str << endl;
    system("pause");
    return 0;
}
