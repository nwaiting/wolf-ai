#coding=utf-8

"""
参考：http://www.jianshu.com/p/218c1e4f0891
计算从A到B的最短路径
将同一列定位一个点
"""
def viterbi():
    for i in xrange(1,len(data)):
        k = x
        for j in xrange(i):
            if data[j][i] < x and dist[j] + data[j][i] < k:
                k = dist[j] + data[j][i]
        dist[i] = k

def showpath():
    j = len(data) - 1
    st = [j,]
    while j > 0:
        for i in xrange(j):
            if data[i][j] > 0:
                if dist[j] - data[i][j] == dist[i]:
                    st.append(i)
                    print i,st
        j = st[len(st)-1]
    print st



"""
states = ('Rainy', 'Sunny')
observations = ('walk', 'shop', 'clean')
start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
transition_probability = {
    'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
    }

emission_probability = {
    'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}

# 打印所有路径概率表
def print_dptable(V):
    print '',
    for t in range(len(V)):
        print "%7d" % t,
    print('')
    print '=============='
    for y in V[0].keys():
        print "%.5s:" % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print ''

def viterbi_internet(stas, obs, start_p, trans_p, emit_p):
    '''
    :param stas:隐状态
    :param obs:观测序列
    :param start_p:初始概率（隐状态）
    :param trans_p:转移概率（隐状态）
    :param emit_p:发射概率（隐状态表现为显状态的概率）
    :return:
    思路：
    定义V[时间][今天天气] = 概率，注意今天天气指的是，前几天的天气都确定下来了（概率最大）今天天气是X的概率，这里的概率就是一个累乘的概率了
    因为第一天我的朋友去散步了，所以第一天下雨的概率V[第一天][下雨] = 初始概率[下雨] * 发射概率[下雨][散步] = 0.6 * 0.1 = 0.06，同理可得V[第一天][天晴] = 0.24。从直觉上来看，因为第一天朋友出门了，她一般喜欢在天晴的时候散步，所以第一天天晴的概率比较大，数字与直觉统一了。
    从第二天开始，对于每种天气Y，都有前一天天气是X的概率 * X转移到Y的概率 * Y天气下朋友进行这天这种活动的概率。因为前一天天气X有两种可能，所以Y的概率有两个，选取其中较大一个作为V[第二天][天气Y]的概率，同时将今天的天气加入到结果序列中
    比较V[最后一天][下雨]和[最后一天][天晴]的概率，找出较大的哪一个对应的序列，就是最终结果
    '''

    V = [{}]   # 路径概率表 V[时间][隐状态] = 概率
    path = {}  # 一个中间变量，代表当前状态是哪个隐状态

    # 初始化初始状态 (对t == 0)
    for y in stas:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y] # 记录初始路径，前面的key对应y状态

    # 跑一遍维特比算法 (对 t > 0)
    for t in range(1, len(obs)):
        V.append({})

        new_path = {}
        for y in stas:
            '''隐状态概率 = 前状态是y0的概率 * y0转移到y的概率 * y表现为当前状态的概率'''
            # y的最大概率及对应的前状态sta
            (prob, sta) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in stas])
            # 记录最大隐状态概率
            V[t][y] = prob
            # 记录路径
            new_path[y] = path[sta] + [y] # 记录当前路径，前面的key对应y状态

        # 不需要保留旧路径
        path = new_path

    print_dptable(V)

    # 找出概率最大的最后状态
    (prob, sta) = max([(V[len(obs) - 1][y], y) for y in stas])
    return prob, path[sta]
"""




def ViterbiCompute(obs, states, start_p, trans_p, emit_p):
    """
    obs:观测序列
    states:隐状态
    start_p:初始概率(隐状态)
    trans_p:转移概率(隐状态)
    emit_p:发射状态(隐状态表现为显状态的概率)
    return:返回最可能的概率
    """
    v = [[0 for i in xrange(len(states))] for j in xrange(len(obs))]
    path = [[0 for i in xrange(len(obs))] for j in xrange(len(states))]
    for i in states:
        v[0][i] = start_p[i] * emit_p[i][obs[0]]
        path[i][0] = i
    for i in xrange(1, len(obs)):
        newpath = [[0 for j in xrange(len(obs))] for jj in xrange(len(states))]
        for s in states:
            prob = -1
            state = None
            for ss in states:
                tmpprob = v[i-1][ss] * trans_p[ss][s] * emit_p[s][obs[i]]
                if tmpprob > prob:
                    prob = tmpprob
                    state = ss
                    v[i][s] = prob
                    for m in xrange(i):
                        newpath[s][m] = path[state][m]
                    newpath[s][i] = s
        path = newpath
    prob = -1
    state = 0
    for y in states:
        if v[len(obs)-1][y] > prob:
            prob = v[len(obs)-1][y]
            state = y
    return path[state]

def ViterbiComputePy(obs, states, start_p, trans_p, emit_p):
    """
    obs:观测序列
    states:隐状态
    start_p:初始概率(隐状态)
    trans_p:转移概率(隐状态)
    emit_p:发射状态(隐状态表现为显状态的概率)
    return:返回最可能的概率

    思路：
        定义V[时间][今天天气] = 概率，注意今天天气指的是，前几天的天气都确定下来了（概率最大）今天天气是X的概率，这里的概率就是一个累乘的概率了
        因为第一天我的朋友去散步了，所以第一天下雨的概率V[第一天][下雨] = 初始概率[下雨] * 发射概率[下雨][散步] = 0.6 * 0.1 = 0.06，同理可得V[第一天][天晴] = 0.24。
            从直觉上来看，因为第一天朋友出门了，她一般喜欢在天晴的时候散步，所以第一天天晴的概率比较大，数字与直觉统一了。
        从第二天开始，对于每种天气Y，都有前一天天气是X的概率 * X转移到Y的概率 * Y天气下朋友进行这天这种活动的概率。因为前一天天气X有两种可能，
            所以Y的概率有两个，选取其中较大一个作为V[第二天][天气Y]的概率，同时将今天的天气加入到结果序列中
        比较V[最后一天][下雨]和[最后一天][天晴]的概率，找出较大的哪一个对应的序列，就是最终结果
    """
    v=[{}] #[时间][隐状态]=概率
    path={} #中间变量代表当前状态是哪个隐状态
    #初始状态 t=0
    for i in states:
        v[0][i] = start_p[i] * emit_p[i][obs[0]]
        path[i] = [i]
    #t>0执行一遍viterbi
    for t in range(1, len(obs)):
        v.append({})
        newpath = {}
        for k in states:
            #概率 隐状态 = 昨天的概率 * 转移概率 * 发射概率
            prob,state = max((v[t-1][m]*trans_p[m][k]*emit_p[k][obs[t]],m) for m in states)
            v[t][k] = prob
            #上一时刻最优状态和当前状态
            newpath[k] = path[state] + [k]
        path = newpath
    prob,state = max((v[len(obs)-1][m],m) for m in states)
    return prob,path[state]

if __name__ == '__main__':
    """
    s = [0,1] #状态 比如：天晴或者下雨
    o = [0,1,2] #观测序列 比如：散步、购物等
    s_p = [0.6,0.4] #开始概率 比如：开始是天晴或者是下雨的概率
    t_p = [[0.7,0.3],[0.6,0.4]] #转移概率 比如：今天是晴天转成明天是晴天的概率
    e_p = [[0.1,0.4,0.5],[0.6,0.3,0.1]] #隐状态表现为显状态的概率 比如：天晴出去散步、购物等的概率

    print ViterbiCompute(o, s, s_p, t_p, e_p)
    print ViterbiComputePy(o, s, s_p, t_p, e_p)

    import sys
    sys.exit(0)
    """
    x = 99999999
    data = [[x,4,2,3,x,x,x,x,x,x],
            [x,x,x,x,10,9,x,x,x,x],
            [x,x,x,x,6,7,10,x,x,x],
            [x,x,x,x,x,3,8,x,x,x],
            [x,x,x,x,x,x,x,4,8,x],
            [x,x,x,x,x,x,x,9,6,x],
            [x,x,x,x,x,x,x,5,4,x],
            [x,x,x,x,x,x,x,x,x,8],
            [x,x,x,x,x,x,x,x,x,4],
            [x,x,x,x,x,x,x,x,x,x]]
    dist = [0 for i in xrange(len(data))]
    viterbi()
    print dist
    showpath()
