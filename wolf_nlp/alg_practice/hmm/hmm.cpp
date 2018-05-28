#include <iostream>
#include <stdint.h>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

/*
    参考：https://en.wikipedia.org/wiki/Viterbi_algorithm#Example
*/
    
class HMM
{
public:
    HMM();
    ~HMM();

public:
    void Init()
    {
        //初始化
    }

    //通过观测序列得到最可能的隐状态序列
    vector<int32_t> Viterbi(vector<int32_t> obs)
    {
        int32_t max_state_value = 0;
        for (auto &it : states_){
            max_state_value = max(max_state_value, it);
        }

        max_state_value++;
        //[时刻][隐状态]=概率
        vector<float> maxv_vec(max_state_value);
        vector<vector<float>> v;
        for (auto &it:obs) {
            v.push_back(maxv_vec);
        }

        //中间变量 每一行存储v对于路径
        vector<int32_t> vec_obs(obs.size());
        vector<vector<int32_t>> path;
        for (auto i = 0; i < max_state_value;i++) {
            path.push_back(vec_obs);
        }

        for (auto &it:states_) {
            v[0][it] = start_prob_[it] + emit_prob_[it][obs[0]];
            path[it][0] = it;
        }

        for (auto &t:obs) {
            //遍历当前的各种状态
            for (auto &curr : states_){
                //计算从上一刻转移到现在 最大概率，计算最大概率
                for (auto &last : states_){
                    //概率 = 上一时刻是last概率 * last转移到curr概率 * curr转移到观测的概率
                    float nprob = v[t - 1][last] + trans_prob_[last][curr] + emit_prob_[curr][obs[t]];
                }
            }
        }
    }

    struct ViterbiInfo
    {
        int32_t t_;
        int32_t s_;
        float p_;
        int32_t pre_s_;
        ViterbiInfo() :t_(0), s_(0), p_(0.0), pre_s_(0){}
    };

    float Viterbi(vector<int32_t> obs, vector<int32_t> &des_path)
    {
        vector<map<int32_t, ViterbiInfo>> V;
        V.resize(obs.size());
        //初始化
        for (auto &it : states_){
            ViterbiInfo info;
            info.t_ = 0;
            info.s_ = it;
            info.p_ = start_prob_[it] * emit_prob_[it][obs[0]];
            info.pre_s_ = -1;
            V[0].insert(make_pair(it, info));
        }

        //开始遍历计算
        for (auto t = 1; t < obs.size(); t++) {
            for (auto &y : states_) {
                float max_prob = 0.0;
                int32_t max_prob_state_pre = 0;
                for (auto &y0 : states_) {
                    float p = V[t - 1][y0].p_ * trans_prob_[y0][y] * emit_prob_[y][obs[t]];
                    if (p > max_prob) {
                        max_prob_state_pre = y0;
                        max_prob = p;
                    }
                }

                ViterbiInfo info;
                info.t_ = t;
                info.s_ = y;
                info.p_ = max_prob;
                info.pre_s_ = max_prob_state_pre;
                V[t].insert(make_pair(y, info));
            }
        }

        //定位到最大概率的状态
        float max_prob = 0.0;
        int32_t max_prob_state_pre = 0;
        for (auto &it : V[V.size() - 1]) {
            if (it.second.p_ > max_prob){
                max_prob = it.second.p_;
                max_prob_state_pre = it.second.pre_s_;
            }
        }

        //遍历V找到最大概率对于的路径
    }

private:
    //状态集
    vector<int32_t> states_;
    //初始化概率
    vector<float> start_prob_;
    //转移概率A
    vector<vector<float>> trans_prob_;
    //发射概率B
    vector<vector<float>> emit_prob_;
};

int main()
{
    HMM hmm = HMM();
    hmm.Init();

    vector<int32_t> obsdata;
    obsdata.push_back(1);
    obsdata.push_back(2);
    obsdata.push_back(3);
    vector<int32_t> res = hmm.Viterbi(obsdata);
    for (auto it:res) {
        cout << it << " ";
    }
    cout << endl;

    cin.get();
    return 0;
}
