#include <iostream>
#include <algorithm>
#include <list>
#include <vector>
#include <string>
#include <stdint.h>
using namespace std;

/*
*   Viterbi算法
*       viterbi算法是最优路径算法的一种。
*       常用的最优路径算法：
*           穷举法
*           A*算法（运用贪心策略的启发式算法）
*           beam search（每一步只走最好走的N条路，这里的N为Beam Width，N越大，找到最优解的概率越大，响应的复杂度越大。因此设置一个合适的Beam Width是一个工程需要trade off的事情）
*           Viterbi算法
*       viterbi算法就是多步骤每步多选择模型的最优选择问题，其在每一步的所有选择都保存了前续多有步骤到当前步骤选择最小总代价（概率最大）。
*       
*       从HMM开始，HMM的5元组中，状态集合、观测结合、初始概率、转移概率、发射概率
*       
*       
*/

/*
*   obs观测序列，以时间t为索引
*   states状态集合
*   start_p状态对应的概率
*   trans_p状态转移到状态的概率
*   emit_p状态到观测集合的概率
*
*/
double viterbi(const std::vector<int32_t> &obs, const std::vector<int32_t> &states, const std::vector<double> &start_p, const std::vector<std::vector<double>> &trans_p, const std::vector<std::vector<double>> &emit_p)
{
    //初始化
    std::vector<std::vector<double>> results;
    std::vector<double> tmp(states.size() + 1, 0.0);
    for (auto i = 0; i <= obs.size(); i++) {
        results.push_back(tmp);
    }

    std::vector<std::vector<int32_t>> paths(states.size());
    for (auto &it:states) {
        results[0][it] = start_p[it] * emit_p[it][obs[0]];
        paths[it] = std::vector<int32_t>();
    }

    //开始计算
    //根据观测集合，遍历每一种观测值对应的概率，每一种观测值都是从上一个状态转移到当前状态，然后发送生成
    for (auto t = 1; t < obs.size(); t++) {
        std::vector<int32_t> new_path;
        for (auto it:states) {
            double max_p = 0.0;
            int32_t max_p_state = 0;
            for (auto it0:states) {
                double tmp_p = results[t - 1][it0] * trans_p[it0][it] * emit_p[it][obs[t]];
                if (tmp_p > max_p) {
                    max_p = tmp_p;
                    max_p_state = it0;
                }
            }
            results[t][it] = max_p;
            paths[it].push_back(max_p_state);
        }
    }

    double max_p = 0.0;
    int32_t max_p_state = 0;
    for (auto &it:states) {
        if (results[obs.size() - 1][it] > max_p) {
            max_p = results[obs.size() - 1][it];
            max_p_state = it;
        }
    }

    for (auto it = 0; it < paths.size(); it++) {
        std::cout << it << " ";
        for (auto jt = 0; jt < paths[it].size(); jt++) {
            std::cout << jt << " ";
        }
        std::cout << std::endl;
    }

    for (auto i = 0; i < paths[max_p_state].size(); i++) {
        std::cout << paths[max_p_state][i] << " ";
    }
    std::cout << max_p_state << " ";
    std::cout << std::endl;

    return max_p;
}


int main()
{
    std::vector<int32_t> states({ 0, 1 });
    std::vector<int32_t> obs({ 0, 1, 2 });
    std::vector<double> start_p({ 0.6, 0.4 });
    std::vector<std::vector<double>> trans_p;
    trans_p.push_back({ 0.7, 0.3 });
    trans_p.push_back({ 0.4, 0.6 });
    std::vector<std::vector<double>> emit_p;
    emit_p.push_back({ 0.5, 0.4, 0.1 });
    emit_p.push_back({ 0.1, 0.3, 0.6 });

    std::cout << viterbi(obs, states, start_p, trans_p, emit_p) << std::endl;
    std::cin.get();
    return 0;
}
