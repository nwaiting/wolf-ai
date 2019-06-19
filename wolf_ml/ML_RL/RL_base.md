## RL base
- **概述：**
>       RL与其他学习方法最大的区别在于它使用的训练信息是对actions的评价，而其他方法是给出正常的actions
>       RL思想：
>           RL是想让一个智能体(agent)在不同的环境状态(state)下，学会选择那个使得奖赏(reward)最大的动作(action)。
>           就是一个agent与environment的交互过程，交互的过程是有一定的目的，就是为了获得尽可能多的reward
>           agent的目标：选择一系列的动作去最大化总的未来奖励。（动作序列可能会很长才能到达目标）
>
>       RL最重要的3个特性在于：
>           （1）通常是一种闭环的形式
>           （2）不会直接指示选择哪种行动（actions）
>           （3）一系列的 actions 和奖励信号（reward signals）都会影响之后较长的时间
>
>
>       在RL问题中，有四个非常重要的概念：
>           （1）规则（policy）
>               在RL中目标就是要学习出了policy，用这个policy来选择动作可以使得我们最终获得的reward最大
>                   可以把policy看成一个关于状态s的函数f。这个函数的输入是状态s（需要把状态描述成可以输入的形式），输出则是一个动作
>
>               Policy定义了agents在特定的时间特定的环境下的行为方式，可以视为是从环境状态到行为的映射，常用π来表示
>               policy可以分为两类：
>                   确定性的policy（Deterministic policy）: a=π(s)
>                   随机性的policy（Stochastic policy）: π(a∣s)=P[At=a∣St=t]
>                       其中，t是时间点，t=0,1,2,3,……
>                           S是环境状态的集合，St代表时刻t的状态，s代表其中某个特定的状态
>                           A(St)是在状态St下的actions的集合，At代表时刻t的行为，a代表其中某个特定的行为
>
>           （2）奖励信号（a reward signal）
>               Reward就是一个标量值，是每个time step中环境根据agent的行为返回给agent的信号，reward定义了在该情景下执行该行为的好坏，
>                   agent可以根据reward来调整自己的policy
>               reward定义了强化学习问题的目的。它告诉agent你这个动作是好还是坏
>               agent的目标：选择一系列的动作去最大化总的未来奖励。（动作序列可能会很长才能到达目标）
>
>               状态state：
>                   整个过程就是一系列的observation，reward，action
>                   环境有两种：
>                       1、S^e：
>                           环境的隐藏表示，事实上，它客观存在，但是agent观测到的不一定是全面的。所以是为了区分agent观测到的状态。
>                           而且agent执行一个动作之后，环境的状态就会有所变化，然后根据环境的状态产生reward反馈给agent。
>                       2、S^a
>                           如果agent能够完全观测到环境的状态，S^a==S^e，这说明是一个马尔科夫决策过程
>
>           （3）值函数（value function）
>               Reward定义的是立即的收益，而value function定义的是长期的收益，它可以看作是累计的reward，常用v来表示
>               reward表示了agent选择一个动作的好坏，而value function则是表示从长期来看的好坏。
>                   即一个状态s的value是指在状态s下的平均reward。从状态s出发，有很多个动作可以选择，然后到达下一个状态，又有很多动作可以选择，这就像一棵树一样，不断展开。
>               不同的动作会得到不同的reward
>               value function就是想表示一个状态s的平均reward
>
>           （4）环境模型（a model of the environment）
>               model based：
>                   即如果知道环境的一切，我们就说这个环境是已知的
>                   在这种情况下，agent知道选择一个动作后，它的状态转移概率是怎样的，获得奖赏是怎样的
>                   这些都知道的话，我们就可以使用动态规划的方法（DP）来解决问题
>               model free：
>                   但是在现实生活中，我们是很难知道状态之间的转移概率的
>                   所以我们无法直接使用动态规划的方法来解决问题
>
>       RL中，agents是具有明确的目标的，所有的agents都能感知自己的环境，并根据目标来指导自己的行为，
>           因此RL的另一个特点是它将agents和与其交互的不确定的环境视为是一个完整的问题。
>
>
>
>       RL中的两个非常重要的概念：
>           1、探索（exploration）
>               exploration是指选择之前未执行过的actions，从而探索更多的可能性；
>           2、开发（exploitation）
>               exploitation是指选择已执行过的actions，从而对已知的actions的模型进行完善
>       “exploration”与“exploitation”在RL中同样重要，如何在“exploration”与“exploitation”之间权衡是RL中的一个重要的问题和挑战。
>           探索也不能一直去探索，因为可能你只有有限的时间，不能把时间一直放在探索上面。所以看起来这是一对矛盾体。如何平衡它们是一个很重要的事情
>           在强化学习中，目标就是为了累积奖赏最大化。那么在每次选择动作时，agent会选择在过去经历中它认为奖赏最大的动作去执行，但是这容易陷入到局部最优，
>               所以，agent需要去探索。探索那些奖赏比较小的动作，也许它后面的奖赏会很大。
>
>

- **RL与ML的区别：**
>       时序是很重要的。也就是动作是一步一步来的。agent的动作会影响后续的子序列。机器学习中的数据可以看成是独立同分布的，
>           但是在RL中，是一个动态的系统，每一步的动作会影响到后续的动作或者reward
>
>
>
>
>
>
>

- **待续：**
>       参考：
>
>
>
>
>
>
>
>
>
>
>
