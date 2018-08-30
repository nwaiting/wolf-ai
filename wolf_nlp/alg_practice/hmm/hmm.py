#coding=utf8

import numpy as np

"""
    隐马模型是关于时序的概率模型，描述一个隐藏的马尔科夫链随机生成不可观测的状态随机序列，在生成一个观测序列的过程
    隐藏的马尔科夫随机生成的状态序列
"""

class HMM(object):
    def __init__(self,N,M):
        #状态转移
        self.A_=np.zeros((N,N))
        #发射概率
        self.B_=np.zeros((N,M))
        #初始状态概率矩阵
        self.pi_=np.array([1.0/N]*N)
        #状态集
        self.States_=N
        #观测集
        self.obs_=M
    def cal_prob(self, obs):
        res = self.forward(obs=obs)
        return sum(res[len(obs)-1])

    def forward(self, obs):
        self.alpha = np.zeros((len(obs), self.States_))

        #公式 10.15
        for i in range(self.N):
            #初始概率*发射概率
            self.alpha[0][i] = self.pi_[i] * self.B_[i][self.obs_[0]]

        # 公式 10.16
        for t in range(1,len(obs)):
            for i in range(self.N):
                sum_pro = 0.0
                for j in range(self.N):
                    sum_pro += self.alpha[t-1][j] * self.A_[j][i]
                self.alpha[t][i] = sum_pro * self.B_[i][obs[t]]

    def backward(self, obs):
        obs_len = len(obs)
        self.beta = np.zeros((obs_len, self.States_))

        #公式10.19
        for i in range(self.N):
            self.beta[obs_len-1][i] = 1

        #公式10.20
        for t in range(obs_len-2,-1,-1):
            for i in range(self.N):
                for j in range(self.N):
                    self.beta[t][i] += self.A_[i][j] * self.B_[j][obs[t+1]] * self.beta[t+1][j]

    def cal_gamma(self, t, i):
        #公式10.24 得到单个状态的概率计算公式，计算在时刻t处于状态q的概率
        numberator = self.alpha[t][i] * self.beta[t][j]
        denominator = 0.0
        for j in range(self.States_):
            denominator += self.alpha[t][i] * self.beta[t][j]
        return numberator/denominator

    def cal_ksi(self,t,i,j):
        #公式10.26  得到两个状态概率的计算公式，计算时刻t处于状态qi且时刻t+1处于状态qj的概率
        numberator = self.alpha[t][i] * self.A_[i][j] * self.B_[j][self.obs_[t+1]] * self.beta[t+1][j]
        denominator = 0.0
        for i in range(self.States_):
            for j in range(self.States_):
                denominator += self.alpha[t][i] * self.A_[i][j] * self.B_[j][self.States_[t+1]] * self.beta[t+1][j]
        return numberator/denominator


    def init(self):
        """
            随机生成A,B,pi
            保证每行相加等于1
        """
        import random
        for i in range(self.States_):
            randomlist = [random.randint(1,100) for _ in range(self.States_)]
            sum_tot = sum(randomlist)
            for j in range(self.States_):
                self.A_[i][j] = randomlist[j]/sum_tot

        for i in range(self.States_):
            randomlist=[random.randint(1,100) for _ in range(self.States_)]
            sum_tot = sum(randomlist)
            for j in range(self.obs_):
                self.B_[i][j] = randomlist[j]/sum_tot

    def train(self, obs, max_step=100):
        """
            鲍姆韦尔奇
        """
        obs_len = len(obs)
        self.init()
        step = 0
        while step < max_step:
            step += 1
            tmp_A = np.zeros((self.States_, self.States_))
            tmp_B = np.zeros((self.States_, self.obs_))
            tmp_pi = np.array([0.0] * self.States_)

            self.forward()
            self.backward()

            # a_{ij}
            for i in self.States_:
                for j in self.States_:
                    numberator = 0
                    denominator = 0
                    for t in range(obs_len):
                        numberator += self.cal_ksi(t,i,j)
                        denominator += self.cal_gamma(t, i)
                    tmp_A[i][j] = numberator/denominator

            # b{jk}
            for j in self.States_:
                for k in self.obs_:
                    numberator = 0
                    denominator = 0
                    for t in range(obs_len):
                        if k == obs[t]:
                            numberator += self.cal_gamma(t,j)
                        denominator += self.cal_gamma(t,k)
                    tmp_B = numberator/denominator

            #pi_i
            for i in range(self.States_):
                tmp_pi = self.cal_gamma(0,i)

            self.A_ = tmp_A
            self.B_ = tmp_B
            self.pi_ = tmp_pi

    def viterbi(self, obs):
        # 求出现obs最可能的隐状态序列（如词性标注）
        V = [{}]
        #初始化V
        for i in self.States_:
            V[0][i] = {'prob':self.pi_[i] * self.B_[i][obs[0]],'prev':None}

        max_prob = 0
        max_prob_state_pre = 0
        max_prob_state = 0
        for t in range(1,len(obs)):
            for i in range(self.States_):
                for j in range(self.States_):
                    p = V[t-1][j] * self.A_[j][i] * self.B_[i][obs[t-1]]
                    if max_prob > p:
                        max_prob = p
                        max_prob_state_pre = j
                        max_prob_state = i
                V[t][i] = {'prob':max_prob, "prev":max_prob_state_pre}

        obs_res = [max_prob_state]
        for t in range(len(V)-1, -1, -1):
            obs_res.append(0, V[t][max_prob_state_pre]["prev"])
            max_prob_state_pre = V[t][max_prob_state_pre]["prev"]


# 求最大的隐状态序列
def Viterbi(obs,states,start_prob,emit_prob,trans_prob):
    #先初始化变量
    max_states_value = max(states)
    max_states_value += 1
    # V[obs][states] = 概率  每一列存储第一列不同隐状态下的概率
    V = [0 for _ in range(max_states_value)] * len(obs)
    # path[states][obs] 当前状态是哪个隐状态 每一行存储V对应的路径
    path = [0 for _ in range(len(obs))] * max_states_value

    #初始化状态
    for i in states:
        V[0][i] = start_prob[i] + emit_prob[i][obs[0]]
        path[i][0] = i

    for t in range(1, len(obs)):
        new_path = [0 for _ in range(len(obs))] * max_states_value
        for y in states:
            prob = 0.0
            max_prob_state = 0
            for y0 in states:
                nprob = V[t-1][y0] + trans_prob[y0][y] + emit_prob[y][obs[t]]
                if nprob > prob:
                    prob = nprob
                    max_prob_state = y0
                    V[t][y] = prob
                    new_path[y][t] = y
        path = new_path

    prob = 0.0
    max_prob_state = 0
    for i in states:
        if V[len(obs)-1][y] < prob:
            prob = V[len(obs)-1][y]
            max_prob_state = y
    return path[max_prob_state]

def Viterbi2(obs, states, start_prob, trans_prob, emit_prob):
    V= [{}]
    # 先初始化V
    for i in states:
        V[0][i] = {"prob":start_prob[i] * emit_prob[i][obs[0]], "prev":None}

    #run Viterbi when t > 0
    for t in range(1, len(obs)):
        for y in states:
            max_prob = 0.0
            pre_state = 0
            for y0 in states:
                prob = V[t-1][y0]["prob"]*trans_prob[y0][y]*emit_prob[y][obs[t]]
                if prob > max_prob:
                    max_prob = prob
                    pre_state = y0
            V[t][y] = {"prob":max_prob, "prev":pre_state}
    opt = []
    pre = None
    max_prob = 0.0
    for state,data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            opt = [state]
            pre = state

    for t in range(len(V)-1, -1, -1):
        opt.insert(0, V[t][pre]["prev"])
        pre = V[t][pre]["prev"]

    print("max prob {0} path {1}".format(max_prob, " ".join(opt)))

def viterbi(obs, states, start_prob, trans_prob, emit_prob):
    V = [{}]
    #先初始化
    for i in states:
        V[0][i] = {'prob':start_prob[i] * emit_prob[i][obs[0]], 'prev':None}
    #开始进行viterbi计算
    for t in range(1, len(obs)):
        for y in states:
            max_prob = 0.0
            pre_state = None
            for y0 in states:
                #前一时刻不同状态的概率 * 不同状态转移到当前状态概率 * 当前状态的发射概率
                prob = V[t-1][y0]['prob'] * trans_prob[y0][y] * emit_prob[y][obs[t]]
                if prob > max_prob:
                    max_prob = prob
                    pre_state = y0
            V[t][y] = {'prob':max_prob, 'prev':pre_state}
    opt = []
    max_prob = 0.0
    pre_state = None
    #先找出最后一个最大概率的
    for p,s in V[-1].item():
        if p > max_prob:
            max_prob = p
            opt = [s]
            pre_state = s
    #从最后一个逆向遍历
    for t in range(len(V[-1])-1,-1,-1):
        opt.insert(0, V[-1][pre_state]['prev'])
        pre_state = V[-1][pre_state]['prev']

if __name__ == "__main__":
    Viterbi()
