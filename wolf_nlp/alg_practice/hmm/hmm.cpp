#include <iostream>
#include <stdint.h>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

/*
    参考：https://en.wikipedia.org/wiki/Viterbi_algorithm#Example
        https://www.jianshu.com/nb/18954627
*/

/*
    //http://www.52nlp.cn/hmm-learn-best-practices-five-forward-algorithm-4
    hmm一个模型，俩个假设，五个基本元素，4大问题，几种算法（前向、后向、EM、BaumWelch、viterbi）
    三大假设：
        1、齐次性假设（隐状态仅与前一个有关）
        2、观测独立性假设（输出只与当前状态有关）
*/

typedef struct {
    int32_t N;  //隐状态数目
    int32_t M;  //观测状态数目
    double **A;   //转移矩阵A[N][N]
    double **B;   //发射矩阵B[N][M]
    double *pi;    //初始概率分布pi[N]
}HMMInfo;

/*
    phmm：已知的HMM模型
    T：观测序列时间长度T
    O：观测序列
    alpha：局部概率，中间状态
    pprob：最终的观测概率
*/
void Forward(HMMInfo *phmm, int32_t T, int32_t *O, double **alpha, double *pprob)
{
    int32_t i,j; //状态索引
    int32_t t;  //时间索引
    double psum; //局部概率的中间值
    /*1、初始化：计算t=1时刻所有状态的局部概率alpha*/
    for(i = 1; i <= phmm->N; i++){
        alpha[1][i] = phmm->pi[i] * phmm->B[i][O[1]];
    }

    /*2、归纳：递归计算每个时间点的局部概率*/
    for(t = 1; t < T; t++){
        for(j = 1; j <= phmm->N; j++){
            psum = 0;
            for(i = 1; i <= phmm->N; i++){
                psum += alpha[t][i] * phmm->A[i][j];
            }
            alpha[t+1][j] = psum * phmm->B[j][O[t+1]];
        }
    }
    /*3、观测序列的概率等于T时刻所有局部概率之和*/
    *pprob = 0.0;
    for(i = 1; i < phmm->N; i++){
        *pprob += alpha[T][i];
    }
}

void Backward(HMMInfo *phmm, int32_t T, int32_t *O, double **beta, double *pprob)
{
    int32_t i,j;
    int32_t t;
    double psum;
    /*1、初始化*/
    for(i = 1; i <= phmm->N; i++){
        beta[T][i] = 1.0;
    }
    /*2、归纳*/
    for(t = T - 1; t >= 1; t--){
        for(i = 1; i <= phmm->N; i++){
            psum = 0.0;
            for(j = 1; j <= phmm->N; j++){
                psum += phmm->A[i][j] * phmm->B[j][O[t+1]] * beta[t+1][j];
            }
            beta[t][i] = psum;
        }
    }

    /*3、结束*/
    *pprob = 0.0;
    for(i = 0; i < phmm->N; i++){
        *pprob += beta[1][i];
    }
}

void BaumWelch(HMMInfo *phmm, int32_t t, int32_t *O, double **alpha, double **beta, double **gamma, int32_t *pniter, double *plogprobinit, double *plogprobfinal)
{
    /*
    ForwardWithScale();
    BackwardWithScale();
    ComputeGamma();
    ComputeXi();
    */
}

void Viterbi(HMMInfo *phmm, int32_t T, int32_t *O, double **delta, int32_t **psi, int32_t *q, double *pprob)
{
    int32_t i,j;
    int32_t t;
    int32_t maxvalind;
    double maxval,val;

    //1、初始化
    for(i = 1; i <= phmm->N; i++){
        delta[1][i] = phmm->pi[i] * phmm->B[i][O[1]];
        psi[1][i] = 0;
    }

    //2、归纳
    for(t = 2; t <= T; t++) {
        for(j = 1; j <= phmm->N; j++) {
            maxval = 0.0;
            maxvalind = 1;
            for(i = 1; i < phmm->N; i++) {
                val = delta[t-1][i] * phmm->A[i][j];
                if(val > maxval){
                    maxval = val;
                    maxvalind = i;
                }
            }
            delta[t][j] = maxval * phmm->B[j][O[t]];
            psi[t][j] = maxvalind;
        }
    }

    //3、结束
    *pprob = 0.0;
    q[T] = 1;
    for(i = 1; i<= phmm->N; i++){
        if(delta[T][i] > *pprob){
            *pprob = delta[T][i];
            q[T] = i;
        }
    }

    //4、回溯path
    for(t = T - 1; t > 0; i--){
        q[t] = psi[t+1][q[t+1]];
    }
}

class HMM
{
public:
    HMM(){}
    ~HMM(){}

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

        return vec_obs;
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

//快排和归并
void quickSort(int32_t *source, int32_t l, int32_t r)
{
    if (l >= r){
        return;
    }

    int32_t key = source[l];
    int32_t begin = l;
    int32_t end = r;
    while (l < r) {
        while (l < r) {
            if (source[r] >= key) {
                r--;
            }
        }
        while (l < r){
            if (source[l] <= key){
                l++;
            }
        }

        swap(source[l], source[r]);
    }
    swap(source[begin], source[l]);
    quickSort(source, begin, l-1);
    quickSort(source, l+1, end);
}

int main()
{
    /*
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
    */
    int32_t s[10] = {10,1000,30,500,300,600,200,100,400,80};
    cout << sizeof(s) << endl;
    //quickSort(s, 0, sizeof(s)-1);
    for (auto i = 0; i < 10; i++) {
        cout << s[i] << " ";
    }
    cin.get();
    return 0;
}
