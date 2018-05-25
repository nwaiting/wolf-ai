#coding=utf8


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

if __name__ == "__main__":
    Viterbi()
