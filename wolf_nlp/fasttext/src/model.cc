/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

#include "model.h"

#include <iostream>
#include <assert.h>
#include <algorithm>
#include <stdexcept>

namespace fasttext {

/*
constexpr int64_t SIGMOID_TABLE_SIZE = 512;
constexpr int64_t MAX_SIGMOID = 8;
constexpr int64_t LOG_TABLE_SIZE = 512;
*/
    const int64_t SIGMOID_TABLE_SIZE = 512;
    const int64_t MAX_SIGMOID = 8;
    const int64_t LOG_TABLE_SIZE = 512;

Model::Model(
    std::shared_ptr<Matrix> wi,
    std::shared_ptr<Matrix> wo,
    std::shared_ptr<Args> args,
    int32_t seed)
    : hidden_(args->dim),
      output_(wo->size(0)),
      grad_(args->dim),
      rng(seed),
      quant_(false) {
  wi_ = wi;
  wo_ = wo;
  args_ = args;
  osz_ = wo->size(0);
  hsz_ = args->dim;
  negpos = 0;
  loss_ = 0.0;
  nexamples_ = 1;
  t_sigmoid_.reserve(SIGMOID_TABLE_SIZE + 1);
  t_log_.reserve(LOG_TABLE_SIZE + 1);
  initSigmoid();
  initLog();
}

void Model::setQuantizePointer(std::shared_ptr<QMatrix> qwi,
                               std::shared_ptr<QMatrix> qwo, bool qout) {
  qwi_ = qwi;
  qwo_ = qwo;
  if (qout) {
    osz_ = qwo_->getM();
  }
}

//逻辑回归步先计算X^Tθ，然后计算ð(X^Tθ) ，然后计算误差lr * (label - score) ，接着根据 grad + alpha * Out 去更新梯度，
//然后更新 Haffman 树节点的权重向量θ；最后根据预测正例还是反例返回负指数损失
real Model::binaryLogistic(int32_t target, bool label, real lr) {
  // 将 hidden_ 和参数矩阵的第 target 行做内积，并计算 sigmoid，逻辑回归
  real score = sigmoid(wo_->dotRow(hidden_, target));
  // 计算梯度时的中间变量  
  //线性搜索误差，不过这里是不是还应该乘以sigmoid的导数:  score*(1 - score) ？
  real alpha = lr * (real(label) - score);
  // Loss 对于 hidden_ 的梯度累加到 grad_ 上
  //更新梯度
  grad_.addRow(*wo_, target, alpha);
  //Loss 对于 LR 参数的梯度累加到 wo_ 的对应行上
  //更新target对应的行参数
  wo_->addRow(hidden_, target, alpha);
  // LR 的 Loss，负指数损失，
  if (label) {
    // 1  公式：L=log(1/p(x))，p(x)是概率值
    return -log(score);
  } else {
    // 0 公式：p(x)=1-score，score为1的概率
    return -log(1.0 - score);
  }
}

real Model::negativeSampling(int32_t target, real lr) {
  real loss = 0.0;
  grad_.zero();
  for (int32_t n = 0; n <= args_->neg; n++) {
    // 对于正样本和负样本，分别更新 LR
    if (n == 0) {
      //将当前词作为正面例子对target类进行LR训练
      loss += binaryLogistic(target, true, lr);
    } else {
      //负采样args_->neg个
      loss += binaryLogistic(getNegative(target), false, lr);
    }
  }
  return loss;
}

//hierarchical softmax 的思想就是从根节点开始，逐步做逻辑回归二分类，一层一层往下，沿着预测 label 的 路径到达预测 label 所在的叶子节点 . 其中 Haffman 树的节点的参数向量为权值向量  ，边的 code 即为分类的标号
real Model::hierarchicalSoftmax(int32_t target, real lr) {
  real loss = 0.0;
  grad_.zero();
  // 先确定霍夫曼树上的路径
  //通过target索引获取路由路径
  const std::vector<bool>& binaryCode = codes[target];
  const std::vector<int32_t>& pathToRoot = paths[target];
  
  // 分别对路径上的中间节点做 LR
  //从叶子节点开始往上回溯，逐步逻辑回归
  for (int32_t i = 0; i < pathToRoot.size(); i++) {
    loss += binaryLogistic(pathToRoot[i], binaryCode[i], lr);
  }
  return loss;
}

void Model::computeOutputSoftmax(Vector& hidden, Vector& output) const {
  //输出=参数转移矩阵*输入
  if (quant_ && args_->qout) {
    output.mul(*qwo_, hidden);
  } else {
    //输出向量（多个输出向量是矩阵）和hidden向量做乘积
    output.mul(*wo_, hidden);
  }
  real max = output[0], z = 0.0;
  //softmax常规策略，减去最大值避免over/underflow，获取最大的内积值
  for (int32_t i = 0; i < osz_; i++) {
    max = std::max(output[i], max);
  }

  //求出每个内绩值相对最大值的情况
  for (int32_t i = 0; i < osz_; i++) {
    output[i] = exp(output[i] - max);
    //计算分母，用于归一化
    z += output[i];
  }
  for (int32_t i = 0; i < osz_; i++) {
    //最终的softmax结果
    output[i] /= z;
  }
}

void Model::computeOutputSoftmax() {
  computeOutputSoftmax(hidden_, output_);
}

// 普通 softmax 的参数更新
real Model::softmax(int32_t target, real lr) {
  grad_.zero();
  //计算softmax
  computeOutputSoftmax();
  //遍历所有输出向量，遍历所有词---此次操作只是针对一个词的更新
  for (int32_t i = 0; i < osz_; i++) {
    real label = (i == target) ? 1.0 : 0.0;
    //要更新的梯度
    real alpha = lr * (label - output_[i]);
    //更新累积梯度，将来更新输入向量去，更新e值
    grad_.addRow(*wo_, i, alpha);
    //更新输出向量
    wo_->addRow(hidden_, i, alpha);
  }

  //loss损失值
  return -log(output_[target]);
}

//在 CBOW 模型中，隐藏层的工作就是将当前词的上下文的词向量进行累加，生成 text representation .
void Model::computeHidden(const std::vector<int32_t>& input, Vector& hidden) const {
  assert(hidden.size() == hsz_);
  // 计算前向传播：输入层 -> 隐层
  hidden.zero();
  for (auto it = input.cbegin(); it != input.cend(); ++it) {
    if(quant_) {
      // hidden_ 向量保存输入词向量的均值，
      //addRow 的作用是将 wi_ 矩阵的第 *it 列加到 hidden_ 上
      hidden.addRow(*qwi_, *it);
    } else {
      //子词嵌入 子串加和，然后平均
      hidden.addRow(*wi_, *it);
    }
  }

  // 求和后除以输入词个数，得到均值向量，每个词是其子串嵌入表示的加和平均
  hidden.mul(1.0 / input.size());
}

bool Model::comparePairs(const std::pair<real, int32_t> &l,
                         const std::pair<real, int32_t> &r) {
  return l.first > r.first;
}

void Model::predict(const std::vector<int32_t>& input, int32_t k, real threshold,
                    std::vector<std::pair<real, int32_t>>& heap,
                    Vector& hidden, Vector& output) const {
  if (k <= 0) {
    throw std::invalid_argument("k needs to be 1 or higher!");
  }
  if (args_->model != model_name::sup) {
    throw std::invalid_argument("Model needs to be supervised for prediction!");
  }
  heap.reserve(k + 1);
  //计算 hidden_ 通过词向量平均得到hidden向量 
  computeHidden(input, hidden);
  if (args_->loss == loss_name::hs) {
    // 如果是层次 softmax，使用 dfs 遍历霍夫曼树的所有叶子节点，找到 top－k 的概率
    dfs(k, threshold, 2 * osz_ - 2, 0.0, heap, hidden);
  } else {
    // 如果是普通 softmax，在结果数组里找到 top-k
    findKBest(k, threshold, heap, hidden, output);
  }

  // 对结果进行排序后输出，因为 heap 中虽然一定是 top-k，但并没有排好序
  std::sort_heap(heap.begin(), heap.end(), comparePairs);
}

//predict 函数可以用于给输入数据打上 1 ～ K 个类标签，并输出各个类标签对应的概率值，
//对于层次 softmax，我们需要遍历霍夫曼树，找到 top－K 的结果，对于普通 softmax（包括负采样和 softmax 的输出），我们需要遍历结果数组，找到 top－K
void Model::predict(
  const std::vector<int32_t>& input,
  int32_t k,
  real threshold,
  std::vector<std::pair<real, int32_t>>& heap
) {
  //hidden_和output_是model类自带的，一会儿用于存储结果
  predict(input, k, threshold, heap, hidden_, output_);
}

//vector寻找topk---获得一个最小堆
void Model::findKBest(
  int32_t k,
  real threshold,
  std::vector<std::pair<real, int32_t>>& heap,
  Vector& hidden, Vector& output
) const {
  // 计算结果数组， softmax的运算结果 
  computeOutputSoftmax(hidden, output);
  //遍历得到的softmax值，选取k个最大的
  for (int32_t i = 0; i < osz_; i++) {
    if (output[i] < threshold) continue;
    if (heap.size() == k && std_log(output[i]) < heap.front().first) {
      continue;
    }
    //如果大于第k个值就更新堆，使用一个堆来保存 top－k 的结果，这是算 top-k 的标准做法
    heap.push_back(std::make_pair(std_log(output[i]), i));
    std::push_heap(heap.begin(), heap.end(), comparePairs);
    if (heap.size() > k) {
      std::pop_heap(heap.begin(), heap.end(), comparePairs);
      heap.pop_back();
    }
  }
}

void Model::dfs(int32_t k, real threshold, int32_t node, real score,
                std::vector<std::pair<real, int32_t>>& heap,
                Vector& hidden) const {
  if (score < std_log(threshold)) return;
  if (heap.size() == k && score < heap.front().first) {
    return;
  }

  // 只输出叶子节点的结果，表示为叶子节点
  if (tree[node].left == -1 && tree[node].right == -1) {
    //根到叶子的损失总值，叶子也就是词了
    heap.push_back(std::make_pair(score, node));
    
    //维持最小堆，以损失值
    std::push_heap(heap.begin(), heap.end(), comparePairs);
    if (heap.size() > k) {
      std::pop_heap(heap.begin(), heap.end(), comparePairs);
      heap.pop_back();
    }
    return;
  }

  // 将 score 累加后递归向下收集结果，计算出sigmod值，用于计算损失
  real f;
  if (quant_ && args_->qout) {
    f= qwo_->dotRow(hidden, node - osz_);
  } else {
    f= wo_->dotRow(hidden, node - osz_);
  }
  f = 1. / (1 + std::exp(-f));

  dfs(k, threshold, tree[node].left, score + std_log(1.0 - f), heap, hidden);
  dfs(k, threshold, tree[node].right, score + std_log(f), heap, hidden);
}


//三个参数，分别是“输入”，“类标签”，“学习率”。
//输入是一个 int32_t数组，每个元素代表一个词在 dictionary 里的 ID。对于分类问题，这个数组代表输入的短文本，对于 word2vec，这个数组代表一个词的上下文
//类标签是一个 int32_t 变量。对于 word2vec 来说，它就是带预测的词的 ID，对于分类问题，它就是类的 label 在 dictionary 里的 ID。因为 label 和词在词表里一起存放，所以有统一的 ID 体系


//三种输出层对应的更新函数：negativeSampling,hierarchicalSoftmax,softmax。
//model 模块中最有意思的部分就是将层次 softmax 和负采样统一抽象成多个二元 logistic regression 计算。
//如果使用负采样，训练时每次选择一个正样本，随机采样几个负样本，每种输出都对应一个参数向量，保存于 wo_ 的各行。对所有样本的参数更新，都是一次独立的 LR 参数更新。
//如果使用层次 softmax，对于每个目标词，都可以在构建好的霍夫曼树上确定一条从根节点到叶节点的路径，路径上的每个非叶节点都是一个 LR，参数保存在 wo_ 的各行上，训练时，这条路径上的 LR 各自独立进行参数更新。
//无论是负采样还是层次 softmax，在神经网络的计算图中，所有 LR 都会依赖于 hidden_的值，所以 hidden_ 的梯度 grad_ 是各个 LR 的反向传播的梯度的累加

void Model::update(const std::vector<int32_t>& input, int32_t target, real lr) {
  //确认标签的合法性
  assert(target >= 0);
  assert(target < osz_);
  if (input.size() == 0) return;

  //子串加和平均得到词嵌入表示，对输入的词向量做平均得到hidden向量
  computeHidden(input, hidden_);
  //接下来就是将隐藏层传入输出层计算损失函数:

  // 根据输出层的不同结构，调用不同的函数，在各个函数中，
  // 不仅通过前向传播算出了 loss_，还进行了反向传播，计算出了 grad_，后面逐一分析。
  //负采样 损失函数
  if (args_->loss == loss_name::ns) {
    //负采样的更新
    loss_ += negativeSampling(target, lr);
  } else if (args_->loss == loss_name::hs) {
    loss_ += hierarchicalSoftmax(target, lr);
  } else {
    //文本分类模式使用，做softmax，里面会对输出向量更新
    loss_ += softmax(target, lr);
  }
  //用于真正训练的样例
  nexamples_ += 1;

  if (args_->model == model_name::sup) {
      // 如果是在训练分类器，就将 grad_ 除以 input_ 的大小
      //返回的要调整的值要除以文本的长度，这样每轮对词向量的调整非常小。大家可能疑惑为什么CBOW不这么做。
      //实际上CBOW的调整策略并不严谨。但是因为上下文一般单词不多，所以对CBOW影响不大。当然CBOW也不是完全没道理，
      //可以把CBOW看做是SG的特例。认为上下文中每个单词都是上下文中所有单词的平均

      //在逻辑回归中产生了导数，在文本分类情况下导数向量需要除以子串数量

      //梯度平均分配
    grad_.mul(1.0 / input.size());
  }

  //导数直接加到子串向量中

  // 反向传播，将 hidden_ 上的梯度传播到 wi_ 上的对应行

  //分别将梯度误差贡献到每个词向量上
  for (auto it = input.cbegin(); it != input.cend(); ++it) {
    //对词（输入）向量更新，迭代加上上下文的词向量，来更新上下文的词向量
    wi_->addRow(grad_, *it, 1.0);
  }
}

void Model::setTargetCounts(const std::vector<int64_t>& counts) {
  assert(counts.size() == osz_);
  //初始化负采样表
  if (args_->loss == loss_name::ns) {
    initTableNegatives(counts);
  }
  //构建huffuman
  if (args_->loss == loss_name::hs) {
    buildTree(counts);
  }
}

//通过词频构造负采样表
void Model::initTableNegatives(const std::vector<int64_t>& counts) {
  real z = 0.0;
  for (size_t i = 0; i < counts.size(); i++) {
    z += pow(counts[i], 0.5);
  }
  for (size_t i = 0; i < counts.size(); i++) {
    real c = pow(counts[i], 0.5);

    //每个词在采样表中数量跟词频开方成正比

    //0,0,0,1,1,1,1,1,1,1,2,2类似这种有序的，0表示第一个词，占个坑，随机读取时，越多则概率越大。所有词的随机化
    //最多重复次数，若是c/z足够小，会导致重复次数很少，最小是1次
    //NEGATIVE_TABLE_SIZE含义是一个词最多重复不能够超过的值
    for (size_t j = 0; j < c * NEGATIVE_TABLE_SIZE / z; j++) {
      //该词映射到表的维度上的取值情况，也就是不等分区映射到等区分段上
      negatives_.push_back(i);
    }
  }
  //随机打乱
  std::shuffle(negatives_.begin(), negatives_.end(), rng);
}

//对于词target获取负采样的值
int32_t Model::getNegative(int32_t target) {
  int32_t negative;
  do {
    //由于表是随机化的，取值就是随机采的
    negative = negatives_[negpos];
    //下一个，不断的累加的，由于表格随机的，所以不需要pos随机了
    negpos = (negpos + 1) % negatives_.size();
  } while (target == negative); //若是遇到为正样本则跳过
  return negative;
}

//算法的性能取决于如何实现这个逻辑。网上的很多实现都是在新增节点都时遍历一次当前所有的树，这种算法的复杂度是 O(n2)，性能很差。???
//聪明一点的方法是用一个优先级队列来保存当前所有的树，每次取 top 2，合并，加回队列。这个算法的复杂度是 O(nlogn)，缺点是必需使用额外的数据结构，而且进堆出堆的操作导致常数项较大
//word2vec 以及 fastText 都采用了一种更好的方法，时间复杂度是 O(nlogn)O(nlogn)，只用了一次排序，一次遍历，简洁优美，但是要理解它需要进行一些推理

//算法首先对输入的叶子节点进行一次排序（O(nlogn)O(nlogn) ），然后确定两个下标 leaf 和 node，leaf 总是指向当前最小的叶子节点，node 总是指向当前最小的非叶子节点，
//所以，最小的两个节点可以从 leaf, leaf - 1, node, node + 1 四个位置中取得，时间复杂度 O(1)O(1)，每个非叶子节点都进行一次，所以总复杂度为 O(n)O(n)，算法整体复杂度为 O(nlogn)

//构建过程：
//上面用数组的方式来创建 Haffman 树的过程比较复杂. 首先是 counts 列表是从大到小排，依次存放在 tree 列表的前 osz 个索引位，为Haffman树的叶子节点；
//然后从第 osz + 1 开始往右就是存放非叶子节点。由于从 tree 列表从 0 到 osz - 1 是从大到小排，根据 Haffman 树的构造过程，
//不断合并 leaf 和 node 出较小的节点生成它们的父节点，并添加到 tree 的 最优边，这么递归下去，Haffman 树就构建完成了；其中最后一个节点就是根节点

void Model::buildTree(const std::vector<int64_t>& counts) {
  // 数组的方式保存huffuman树，大小为：2*num(叶子节点数) - 1
  tree.resize(2 * osz_ - 1);

  // 初始每个节点
  for (int32_t i = 0; i < 2 * osz_ - 1; i++) {
    tree[i].parent = -1;
    tree[i].left = -1;
    tree[i].right = -1;
    tree[i].count = 1e15;
    tree[i].binary = false;
  }

  //tree的前osz_保存叶子节点标签
  for (int32_t i = 0; i < osz_; i++) {
    tree[i].count = counts[i];
  }
  // leaf 指向当前未处理的叶子节点的最后一个，也就是权值最小的叶子节点
  int32_t leaf = osz_ - 1;

  // node 指向当前未处理的非叶子节点的第一个，也是权值最小的非叶子节点
  int32_t node = osz_;

  // 从叶子节点往后构建，逐个构造所有非叶子节点（i >= osz_, i < 2 * osz - 1)
  for (int32_t i = osz_; i < 2 * osz_ - 1; i++) {
    // 最小的两个节点的下标
    int32_t mini[2];
    // 首先 counts实体列表应该是按照 count 从大到小排列的顺序，从 osz 开始依次去左右两边的合成 count 较小的两个实体，然后在右边最新节点创建实体
    // 计算权值最小的两个节点，候选只可能是 leaf, leaf - 1,以及 node, node + 1
    for (int32_t j = 0; j < 2; j++) {
      // 从这四个候选里找到 top-2
      if (leaf >= 0 && tree[leaf].count < tree[node].count) {
        mini[j] = leaf--;
      } else {
        mini[j] = node++;
      }
    }
    // 更新非叶子节点的属性
    // 构建父节点
    tree[i].left = mini[0];
    tree[i].right = mini[1];
    tree[i].count = tree[mini[0]].count + tree[mini[1]].count;
    tree[mini[0]].parent = i;
    tree[mini[1]].parent = i;
    //左侧编码为 false，右侧编码为 true
    tree[mini[1]].binary = true;
  }//则 tree 的最后一个节点即为根节点

  // 计算霍夫曼编码
  //对每个叶子节点创建路由选择路径
  for (int32_t i = 0; i < osz_; i++) {
    std::vector<int32_t> path;
    std::vector<bool> code;
    int32_t j = i;
    while (tree[j].parent != -1) {
      //由 Huffman 树叶子节点的特殊性得
      path.push_back(tree[j].parent - osz_);
      code.push_back(tree[j].binary);
      j = tree[j].parent;
    }
    paths.push_back(path);
    codes.push_back(code);
  }
}

//获取均匀损失值，平均每个样本的损失
real Model::getLoss() const {
  return loss_ / nexamples_;
}

//初始化sigmod表
void Model::initSigmoid() {
  for (int i = 0; i < SIGMOID_TABLE_SIZE + 1; i++) {
    real x = real(i * 2 * MAX_SIGMOID) / SIGMOID_TABLE_SIZE - MAX_SIGMOID;
    t_sigmoid_.push_back(1.0 / (1.0 + std::exp(-x)));
  }
}

//初始化log函数的表，对于0~1之间的值
void Model::initLog() {
  for (int i = 0; i < LOG_TABLE_SIZE + 1; i++) {
    real x = (real(i) + 1e-5) / LOG_TABLE_SIZE;
    t_log_.push_back(std::log(x));
  }
}

//log的处理
real Model::log(real x) const {
  if (x > 1.0) {
    return 0.0;
  }
  int64_t i = int64_t(x * LOG_TABLE_SIZE);
  return t_log_[i];
}

real Model::std_log(real x) const {
  return std::log(x+1e-5);
}

//获取sigmod值
real Model::sigmoid(real x) const {
  if (x < -MAX_SIGMOID) {
    return 0.0;
  } else if (x > MAX_SIGMOID) {
    return 1.0;
  } else {
    int64_t i = int64_t((x + MAX_SIGMOID) * SIGMOID_TABLE_SIZE / MAX_SIGMOID / 2);
    return t_sigmoid_[i];
  }
}

}
