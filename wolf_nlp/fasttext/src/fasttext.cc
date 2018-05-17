/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

#include "fasttext.h"

#include <iostream>
#include <sstream>
#include <iomanip>
#include <thread>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <numeric>


namespace fasttext {

//constexpr int32_t FASTTEXT_VERSION = 12; /* Version 1b */
    const int32_t FASTTEXT_VERSION = 12; /* Version 1b */
//constexpr int32_t FASTTEXT_FILEFORMAT_MAGIC_INT32 = 793712314;
    const int32_t FASTTEXT_FILEFORMAT_MAGIC_INT32 = 793712314;

FastText::FastText() : quant_(false) {}

void FastText::addInputVector(Vector& vec, int32_t ind) const {
  if (quant_) {
    vec.addRow(*qinput_, ind);
  } else {
    vec.addRow(*input_, ind);
  }
}

std::shared_ptr<const Dictionary> FastText::getDictionary() const {
  return dict_;
}

const Args FastText::getArgs() const {
  return *args_.get();
}

std::shared_ptr<const Matrix> FastText::getInputMatrix() const {
  return input_;
}

std::shared_ptr<const Matrix> FastText::getOutputMatrix() const {
  return output_;
}

int32_t FastText::getWordId(const std::string& word) const {
  return dict_->getId(word);
}

int32_t FastText::getSubwordId(const std::string& word) const {
  int32_t h = dict_->hash(word) % args_->bucket;
  return dict_->nwords() + h;
}

void FastText::getWordVector(Vector& vec, const std::string& word) const {
  const std::vector<int32_t>& ngrams = dict_->getSubwords(word);
  vec.zero();
  for (int i = 0; i < ngrams.size(); i ++) {
    //ngram的累加
    addInputVector(vec, ngrams[i]);
  }
  if (ngrams.size() > 0) {
    //词向量均值
    vec.mul(1.0 / ngrams.size());
  }
}

void FastText::getVector(Vector& vec, const std::string& word) const {
  getWordVector(vec, word);
}

void FastText::getSubwordVector(Vector& vec, const std::string& subword)
    const {
  vec.zero();
  int32_t h = dict_->hash(subword) % args_->bucket;
  h = h + dict_->nwords();
  addInputVector(vec, h);
}

void FastText::saveVectors() {
  std::ofstream ofs(args_->output + ".vec");
  if (!ofs.is_open()) {
    throw std::invalid_argument(
        args_->output + ".vec" + " cannot be opened for saving vectors!");
  }
  ofs << dict_->nwords() << " " << args_->dim << std::endl;
  Vector vec(args_->dim);
  for (int32_t i = 0; i < dict_->nwords(); i++) {
    std::string word = dict_->getWord(i);
    getWordVector(vec, word);
    ofs << word << " " << vec << std::endl;
  }
  ofs.close();
}

void FastText::saveOutput() {
  std::ofstream ofs(args_->output + ".output");
  if (!ofs.is_open()) {
    throw std::invalid_argument(
        args_->output + ".output" + " cannot be opened for saving vectors!");
  }
  if (quant_) {
    throw std::invalid_argument(
        "Option -saveOutput is not supported for quantized models.");
  }
  int32_t n = (args_->model == model_name::sup) ? dict_->nlabels()
                                                : dict_->nwords();
  ofs << n << " " << args_->dim << std::endl;
  Vector vec(args_->dim);
  for (int32_t i = 0; i < n; i++) {
    std::string word = (args_->model == model_name::sup) ? dict_->getLabel(i)
                                                         : dict_->getWord(i);
    vec.zero();
    vec.addRow(*output_, i);
    ofs << word << " " << vec << std::endl;
  }
  ofs.close();
}

bool FastText::checkModel(std::istream& in) {
  int32_t magic;
  in.read((char*)&(magic), sizeof(int32_t));
  if (magic != FASTTEXT_FILEFORMAT_MAGIC_INT32) {
    return false;
  }
  in.read((char*)&(version), sizeof(int32_t));
  if (version > FASTTEXT_VERSION) {
    return false;
  }
  return true;
}

void FastText::signModel(std::ostream& out) {
  const int32_t magic = FASTTEXT_FILEFORMAT_MAGIC_INT32;
  const int32_t version = FASTTEXT_VERSION;
  out.write((char*)&(magic), sizeof(int32_t));
  out.write((char*)&(version), sizeof(int32_t));
}

void FastText::saveModel() {
  std::string fn(args_->output);
  if (quant_) {
    fn += ".ftz";
  } else {
    fn += ".bin";
  }
  saveModel(fn);
}

void FastText::saveModel(const std::string path) {
  std::ofstream ofs(path, std::ofstream::binary);
  if (!ofs.is_open()) {
    throw std::invalid_argument(path + " cannot be opened for saving!");
  }
  signModel(ofs);
  args_->save(ofs);
  dict_->save(ofs);

  ofs.write((char*)&(quant_), sizeof(bool));
  if (quant_) {
    qinput_->save(ofs);
  } else {
    input_->save(ofs);
  }

  ofs.write((char*)&(args_->qout), sizeof(bool));
  if (quant_ && args_->qout) {
    qoutput_->save(ofs);
  } else {
    output_->save(ofs);
  }

  ofs.close();
}

void FastText::loadModel(const std::string& filename) {
  std::ifstream ifs(filename, std::ifstream::binary);
  if (!ifs.is_open()) {
    throw std::invalid_argument(filename + " cannot be opened for loading!");
  }
  if (!checkModel(ifs)) {
    throw std::invalid_argument(filename + " has wrong file format!");
  }
  loadModel(ifs);
  ifs.close();
}

void FastText::loadModel(std::istream& in) {
  args_ = std::make_shared<Args>();
  input_ = std::make_shared<Matrix>();
  output_ = std::make_shared<Matrix>();
  qinput_ = std::make_shared<QMatrix>();
  qoutput_ = std::make_shared<QMatrix>();
  args_->load(in);
  if (version == 11 && args_->model == model_name::sup) {
    // backward compatibility: old supervised models do not use char ngrams.
    args_->maxn = 0;
  }
  dict_ = std::make_shared<Dictionary>(args_, in);

  bool quant_input;
  in.read((char*) &quant_input, sizeof(bool));
  if (quant_input) {
    quant_ = true;
    qinput_->load(in);
  } else {
    input_->load(in);
  }

  if (!quant_input && dict_->isPruned()) {
    throw std::invalid_argument(
        "Invalid model file.\n"
        "Please download the updated model from www.fasttext.cc.\n"
        "See issue #332 on Github for more information.\n");
  }

  in.read((char*) &args_->qout, sizeof(bool));
  if (quant_ && args_->qout) {
    qoutput_->load(in);
  } else {
    output_->load(in);
  }

  model_ = std::make_shared<Model>(input_, output_, args_, 0);
  model_->quant_ = quant_;
  model_->setQuantizePointer(qinput_, qoutput_, args_->qout);

  if (args_->model == model_name::sup) {
    model_->setTargetCounts(dict_->getCounts(entry_type::label));
  } else {
    model_->setTargetCounts(dict_->getCounts(entry_type::word));
  }
}

void FastText::printInfo(real progress, real loss, std::ostream& log_stream) {
  // clock_t might also only be 32bits wide on some systems
  double t = double(clock() - start_) / double(CLOCKS_PER_SEC);
  double lr = args_->lr * (1.0 - progress);
  double wst = 0;
  int64_t eta = 720 * 3600; // Default to one month
  if (progress > 0 && t >= 0) {
    eta = int(t / progress * (1 - progress) / args_->thread);
    wst = double(tokenCount_) / t;
  }
  int32_t etah = eta / 3600;
  int32_t etam = (eta % 3600) / 60;
  progress = progress * 100;
  log_stream << std::fixed;
  log_stream << "Progress: ";
  log_stream << std::setprecision(1) << std::setw(5) << progress << "%";
  log_stream << " words/sec/thread: " << std::setw(7) << int64_t(wst);
  log_stream << " lr: " << std::setw(9) << std::setprecision(6) << lr;
  log_stream << " loss: " << std::setw(9) << std::setprecision(6) << loss;
  log_stream << " ETA: " << std::setw(3) << etah;
  log_stream << "h" << std::setw(2) << etam << "m";
  log_stream << std::flush;
}

std::vector<int32_t> FastText::selectEmbeddings(int32_t cutoff) const {
  Vector norms(input_->size(0));
  input_->l2NormRow(norms);
  std::vector<int32_t> idx(input_->size(0), 0);
  std::iota(idx.begin(), idx.end(), 0);
  auto eosid = dict_->getId(Dictionary::EOS);
  std::sort(idx.begin(), idx.end(),
      [&norms, eosid] (size_t i1, size_t i2) {
      return eosid ==i1 || (eosid != i2 && norms[i1] > norms[i2]);
      });
  idx.erase(idx.begin() + cutoff, idx.end());
  return idx;
}

void FastText::quantize(const Args qargs) {
  if (args_->model != model_name::sup) {
    throw std::invalid_argument(
        "For now we only support quantization of supervised models");
  }
  args_->input = qargs.input;
  args_->qout = qargs.qout;
  args_->output = qargs.output;

  if (qargs.cutoff > 0 && qargs.cutoff < input_->size(0)) {
    auto idx = selectEmbeddings(qargs.cutoff);
    dict_->prune(idx);
    std::shared_ptr<Matrix> ninput =
        std::make_shared<Matrix>(idx.size(), args_->dim);
    for (auto i = 0; i < idx.size(); i++) {
      for (auto j = 0; j < args_->dim; j++) {
        ninput->at(i, j) = input_->at(idx[i], j);
      }
    }
    input_ = ninput;
    if (qargs.retrain) {
      args_->epoch = qargs.epoch;
      args_->lr = qargs.lr;
      args_->thread = qargs.thread;
      args_->verbose = qargs.verbose;
      startThreads();
    }
  }

  qinput_ = std::make_shared<QMatrix>(*input_, qargs.dsub, qargs.qnorm);

  if (args_->qout) {
    qoutput_ = std::make_shared<QMatrix>(*output_, 2, qargs.qnorm);
  }

  quant_ = true;
  model_ = std::make_shared<Model>(input_, output_, args_, 0);
  model_->quant_ = quant_;
  model_->setQuantizePointer(qinput_, qoutput_, args_->qout);
  if (args_->model == model_name::sup) {
    model_->setTargetCounts(dict_->getCounts(entry_type::label));
  } else {
    model_->setTargetCounts(dict_->getCounts(entry_type::word));
  }
}


/*
    这样文本训练的任务就完成了。大家可能会好奇，ngram加在哪里了，实际上全在dictionary类中处理了。
    dictionary类直接返回line，line中包括了单词以及ngram的id
*/
void FastText::supervised(
    Model& model,
    real lr,
    const std::vector<int32_t>& line,
    const std::vector<int32_t>& labels) {
  if (labels.size() == 0 || line.size() == 0) return;
  // 因为一个句子可以打上多个 label，但是 fastText 的架构实际上只有支持一个 label，所以这里随机选择一个 label 来更新模型，这样做会让其它 label 被忽略
  // 所以 fastText 不太适合做多标签的分类
  std::uniform_int_distribution<> uniform(0, labels.size() - 1);
  int32_t i = uniform(model.rng);
  //更新，对line中的所有向量取平均，去预测label，更新词向量也是调用这个函数
  model.update(line, labels[i], lr);
}

void FastText::cbow(Model& model, real lr,
                    const std::vector<int32_t>& line) {
  std::vector<int32_t> bow;
  std::uniform_int_distribution<> uniform(1, args_->ws);

  // 在一个句子中，每个词可以进行一次 update
  for (int32_t w = 0; w < line.size(); w++) {
    // 一个词的上下文长度是随机产生的
    int32_t boundary = uniform(model.rng);
    bow.clear();
    // 以当前词为中心，将左右 boundary 个词加入 input
    for (int32_t c = -boundary; c <= boundary; c++) {
      if (c != 0 && w + c >= 0 && w + c < line.size()) {
        // 实际被加入 input 的不止是词本身，还有词的 word n-gram
        //将上下文的子字符串加入到包中
        const std::vector<int32_t>& ngrams = dict_->getSubwords(line[w + c]);
        bow.insert(bow.end(), ngrams.cbegin(), ngrams.cend());
      }
    }
    //用所有词的子串预测中心词，更新参数
    model.update(bow, line[w], lr);
  }
}

//这里是和文本分类的关键区别，循环。第一层是对一行的每个单词，第二层循环是对每个单词找到其周围的上下文，
// 一个单词用vector去存是因为一个单词由多个subword组成
void FastText::skipgram(Model& model, real lr,
                        const std::vector<int32_t>& line) {
  std::uniform_int_distribution<> uniform(1, args_->ws);
  for (int32_t w = 0; w < line.size(); w++) {
    // 一个词的上下文长度是随机产生的    
    int32_t boundary = uniform(model.rng);
    // 采用词+word n-gram 来预测这个词的上下文的所有的词
    const std::vector<int32_t>& ngrams = dict_->getSubwords(line[w]);
    // 在 skipgram 中，对上下文的每一个词分别更新一次模型
    for (int32_t c = -boundary; c <= boundary; c++) {
      if (c != 0 && w + c >= 0 && w + c < line.size()) {
        //ngram作为上下文
        // 通过 ngrams 计算 line[w] 的表示，通过逻辑回归优化 ngrams 的嵌入表示
        model.update(ngrams, line[w + c], lr);
      }
    }
  }
}

std::tuple<int64_t, double, double> FastText::test(
    std::istream& in,
    int32_t k,
    real threshold) {
  int32_t nexamples = 0, nlabels = 0, npredictions = 0;
  double precision = 0.0;
  std::vector<int32_t> line, labels;

  while (in.peek() != EOF) {
    dict_->getLine(in, line, labels);
    if (labels.size() > 0 && line.size() > 0) {
      std::vector<std::pair<real, int32_t>> modelPredictions;
      model_->predict(line, k, threshold, modelPredictions);
      for (auto it = modelPredictions.cbegin(); it != modelPredictions.cend(); it++) {
        if (std::find(labels.begin(), labels.end(), it->second) != labels.end()) {
          precision += 1.0;
        }
      }
      nexamples++;
      nlabels += labels.size();
      npredictions += modelPredictions.size();
    }
  }
  return std::tuple<int64_t, double, double>(
      nexamples, precision / npredictions, precision / nlabels);
}

void FastText::predict(
  std::istream& in,
  int32_t k,
  std::vector<std::pair<real,std::string>>& predictions,
  real threshold
) const {
  std::vector<int32_t> words, labels;
  predictions.clear();
  dict_->getLine(in, words, labels);
  predictions.clear();
  if (words.empty()) return;
  Vector hidden(args_->dim);
  Vector output(dict_->nlabels());
  std::vector<std::pair<real,int32_t>> modelPredictions;
  // 调用 model 模块的预测接口，获取 k 个最可能的分类
  model_->predict(words, k, threshold, modelPredictions, hidden, output);

  // 输出结果
  for (auto it = modelPredictions.cbegin(); it != modelPredictions.cend(); it++) {
    predictions.push_back(std::make_pair(it->first, dict_->getLabel(it->second)));
  }
}

void FastText::predict(
  std::istream& in,
  int32_t k,
  bool print_prob,
  real threshold
) {
  std::vector<std::pair<real,std::string>> predictions;
  while (in.peek() != EOF) {
    predictions.clear();
    predict(in, k, predictions, threshold);
    if (predictions.empty()) {
      std::cout << std::endl;
      continue;
    }
    for (auto it = predictions.cbegin(); it != predictions.cend(); it++) {
      if (it != predictions.cbegin()) {
        std::cout << " ";
      }
      std::cout << it->second;
      if (print_prob) {
        std::cout << " " << std::exp(it->first);
      }
    }
    std::cout << std::endl;
  }
}

void FastText::getSentenceVector(
    std::istream& in,
    fasttext::Vector& svec) {
  svec.zero();
  if (args_->model == model_name::sup) {
    std::vector<int32_t> line, labels;
    dict_->getLine(in, line, labels);
    //句子的词以及ngram的索引
    for (int32_t i = 0; i < line.size(); i++) {
      //将词的向量求出和
      addInputVector(svec, line[i]);
    }

    //求均值
    if (!line.empty()) {
      svec.mul(1.0 / line.size());
    }
  } else {
    Vector vec(args_->dim);
    std::string sentence;
    std::getline(in, sentence);
    std::istringstream iss(sentence);
    std::string word;
    int32_t count = 0;
    while (iss >> word) {
      getWordVector(vec, word);
      real norm = vec.norm();
      if (norm > 0) {
        vec.mul(1.0 / norm);
        svec.addVector(vec);
        count++;
      }
    }
    if (count > 0) {
      svec.mul(1.0 / count);
    }
  }
}

void FastText::ngramVectors(std::string word) {
  std::vector<int32_t> ngrams;
  std::vector<std::string> substrings;
  Vector vec(args_->dim);
  dict_->getSubwords(word, ngrams, substrings);
  for (int32_t i = 0; i < ngrams.size(); i++) {
    vec.zero();
    if (ngrams[i] >= 0) {
      if (quant_) {
        vec.addRow(*qinput_, ngrams[i]);
      } else {
        vec.addRow(*input_, ngrams[i]);
      }
    }
    std::cout << substrings[i] << " " << vec << std::endl;
  }
}

void FastText::precomputeWordVectors(Matrix& wordVectors) {
  Vector vec(args_->dim);
  wordVectors.zero();
  for (int32_t i = 0; i < dict_->nwords(); i++) {
    std::string word = dict_->getWord(i);
    getWordVector(vec, word);
    real norm = vec.norm();
    if (norm > 0) {
      wordVectors.addRow(vec, i, 1.0 / norm);
    }
  }
}

void FastText::findNN(
    const Matrix& wordVectors,
    const Vector& queryVec,
    int32_t k,
    const std::set<std::string>& banSet,
    std::vector<std::pair<real, std::string>>& results) {
  results.clear();
  std::priority_queue<std::pair<real, std::string>> heap;
  real queryNorm = queryVec.norm();
  if (std::abs(queryNorm) < 1e-8) {
    queryNorm = 1;
  }
  Vector vec(args_->dim);
  for (int32_t i = 0; i < dict_->nwords(); i++) {
    std::string word = dict_->getWord(i);
    real dp = wordVectors.dotRow(queryVec, i);
    heap.push(std::make_pair(dp / queryNorm, word));
  }
  int32_t i = 0;
  while (i < k && heap.size() > 0) {
    auto it = banSet.find(heap.top().second);
    if (it == banSet.end()) {
      results.push_back(std::pair<real, std::string>(heap.top().first, heap.top().second));
      i++;
    }
    heap.pop();
  }
}

void FastText::analogies(int32_t k) {
  std::string word;
  Vector buffer(args_->dim), query(args_->dim);
  Matrix wordVectors(dict_->nwords(), args_->dim);
  precomputeWordVectors(wordVectors);
  std::set<std::string> banSet;
  std::cout << "Query triplet (A - B + C)? ";
  std::vector<std::pair<real, std::string>> results;
  while (true) {
    banSet.clear();
    query.zero();
    std::cin >> word;
    banSet.insert(word);
    getWordVector(buffer, word);
    query.addVector(buffer, 1.0);
    std::cin >> word;
    banSet.insert(word);
    getWordVector(buffer, word);
    query.addVector(buffer, -1.0);
    std::cin >> word;
    banSet.insert(word);
    getWordVector(buffer, word);
    query.addVector(buffer, 1.0);

    findNN(wordVectors, query, k, banSet, results);
    for (auto& pair : results) {
      std::cout << pair.second << " " << pair.first << std::endl;
    }
    std::cout << "Query triplet (A - B + C)? ";
  }
}

//该函数的主要工作是 实现了标准的随机梯度下降，并随着训练的进行逐步降低学习率
//一哄而上的并行训练：每个训练线程在更新参数时并没有加锁，这会给参数更新带来一些噪音，但是不会影响最终的结果
void FastText::trainThread(int32_t threadId) {
  std::ifstream ifs(args_->input);
  //根据每个线程定位到不同位置，每个线程一直执行下午，到文档最后在从第一行开始
  // 根据线程数，将训练文件按照总字节数（utils::size）均分成多个部分
  // 这么做的一个后果是，每一部分的第一个词有可能从中间被切断，这样的"小噪音"对于整体的训练结果无影响
  utils::seek(ifs, threadId * utils::size(ifs) / args_->thread);

  //模型主要就包括的是输入输出向量
  Model model(input_, output_, args_, threadId);
  if (args_->model == model_name::sup) {
    model.setTargetCounts(dict_->getCounts(entry_type::label));
  } else {
    model.setTargetCounts(dict_->getCounts(entry_type::word));
  }

  // 训练文件中的 token 总数
  const int64_t ntokens = dict_->ntokens();
  // 当前线程处理完毕的 token 总数
  int64_t localTokenCount = 0;
  std::vector<int32_t> line, labels;

  //一共要处理 epoch乘以ntokens个tokens，tokenCount记录一共处理了多少个tokens
  // tokenCount 为所有线程处理完毕的 token 总数，当处理了 args_->epoch 遍所有 token 后，训练结束 
  while (tokenCount_ < args_->epoch * ntokens) {

    //更新alpha的逻辑和word2vec一样， progress = 0 ~ 1，代表当前训练进程，随着训练的进行逐渐增大
    real progress = real(tokenCount_) / (args_->epoch * ntokens);
    // 学习率根据 progress 线性下降
    real lr = args_->lr * (1.0 - progress);
    if (args_->model == model_name::sup) {
      //词典类中的getline得到一行文本line，以及对应的label，line是单词的id数组（向量）
      localTokenCount += dict_->getLine(ifs, line, labels);
      supervised(model, lr, line, labels);
    } else if (args_->model == model_name::cbow) {
      localTokenCount += dict_->getLine(ifs, line, model.rng);
      cbow(model, lr, line);
    } else if (args_->model == model_name::sg) {
      localTokenCount += dict_->getLine(ifs, line, model.rng);
      skipgram(model, lr, line);
    }

    //大于一定的阈值打印
    // args_->lrUpdateRate 是每个线程学习率的变化率，默认为 100，
    // 它的作用是，每处理一定的行数，再更新全局的 tokenCount 变量，从而影响学习率
    if (localTokenCount > args_->lrUpdateRate) {
      tokenCount_ += localTokenCount;
      // 每次更新 tokenCount 后，重置计数
      localTokenCount = 0;
      // 0 号线程负责将训练进度输出到屏幕
      if (threadId == 0 && args_->verbose > 1)
        loss_ = model.getLoss();
    }
  }
  if (threadId == 0)
    loss_ = model.getLoss();
  ifs.close();
}

void FastText::loadVectors(std::string filename) {
  std::ifstream in(filename);
  std::vector<std::string> words;
  std::shared_ptr<Matrix> mat; // temp. matrix for pretrained vectors
  int64_t n, dim;
  if (!in.is_open()) {
    throw std::invalid_argument(filename + " cannot be opened for loading!");
  }
  in >> n >> dim;
  if (dim != args_->dim) {
    throw std::invalid_argument(
        "Dimension of pretrained vectors (" + std::to_string(dim) +
        ") does not match dimension (" + std::to_string(args_->dim) + ")!");
  }
  mat = std::make_shared<Matrix>(n, dim);
  for (size_t i = 0; i < n; i++) {
    std::string word;
    in >> word;
    words.push_back(word);
    dict_->add(word);
    for (size_t j = 0; j < dim; j++) {
      in >> mat->at(i, j);
    }
  }
  in.close();

  dict_->threshold(1, 0);
  dict_->init();
  input_ = std::make_shared<Matrix>(dict_->nwords()+args_->bucket, args_->dim);
  input_->uniform(1.0 / args_->dim);

  for (size_t i = 0; i < n; i++) {
    int32_t idx = dict_->getId(words[i]);
    if (idx < 0 || idx >= dict_->nwords()) continue;
    for (size_t j = 0; j < dim; j++) {
      input_->at(idx, j) = mat->at(i, j);
    }
  }
}

/*
  skipgram：
    之前已经介绍过这个函数，首先建立词典，然后初始化所有参数，然后多线程训练然后保存参数。目前大多都和文本分类一样。
    一点关键的区别是output向量的维度不一样了。在文本分类中维度是标签个数乘以词向量维度，这里是上下文单词个数乘以词向量维度。
    因为文本分类是预测标签，而词向量是预测单词

    区别就是调用了skipgram函数。其他流程一样：首先根据参数初始化模型，然后循环，读入一行，训练，隔一段时间更新一次learning rate

    这里是和文本分类的关键区别，循环。第一层是对一行的每个单词，第二层循环是对每个单词找到其周围的上下文，一个单词用vector去存是因为一个单词由多个subword组成
*/
void FastText::train(const Args args) {
  args_ = std::make_shared<Args>(args);

  //基本所有自然语言处理的第一步都是构建一个词典
  dict_ = std::make_shared<Dictionary>(args_);

  if (args_->input == "-") {
    // manage expectations
    throw std::invalid_argument("Cannot use stdin for training!");
  }
  std::ifstream ifs(args_->input);
  if (!ifs.is_open()) {
    throw std::invalid_argument(
        args_->input + " cannot be opened for training!");
  }

  //通过语料构建词典
  dict_->readFromFile(ifs);
  ifs.close();

  //和word2vec一样，参数由两部分组成，一部分是词向量，一部分是上下文向量/label向量，即input向量和output向量
  if (args_->pretrainedVectors.size() != 0) {
    loadVectors(args_->pretrainedVectors);
  } else {
    //初始化输入层
    //对于普通 word2vec，输入层就是一个词向量的查找表，所以它的大小为 nwords 行，dim 列（dim 为词向量的长度），
    //但是 fastText 用了word n-gram 作为输入，所以输入矩阵的大小为 (nwords + ngram 种类) * dim
    //代码中，所有 word n-gram 都被 hash 到固定数目的 bucket 中，所以输入矩阵的大小为(nwords + bucket 个数) * dim
    //词向量的个数=单词的数量+桶的个数，多个ngram或是字符ngram会在一个桶中共享一个向量
    input_ = std::make_shared<Matrix>(dict_->nwords()+args_->bucket, args_->dim);
    //初始化词向量，均匀随机分布初始化，在(-1/dim,1/dim)之间
    input_->uniform(1.0 / args_->dim);
  }

  //初始化输出层
  // 输出层无论是用负采样，层次 softmax，还是普通 softmax，对于每种可能的输出，都有一个 dim 维的参数向量与之对应
  // 当 args_->model == model_name::sup 时，训练分类器，所以输出的种类是标签总数 dict_->nlabels()
  if (args_->model == model_name::sup) {
    //分类：label数量 * 词向量维度
    output_ = std::make_shared<Matrix>(dict_->nlabels(), args_->dim);
  } else {
    //词向量：词数量 * 词向量维度
    output_ = std::make_shared<Matrix>(dict_->nwords(), args_->dim);
  }
  output_->zero();

  //开启多线程训练
  startThreads();
  //最后训练的结果就是词向量和上下文向量，即输入向量和输出向量
  model_ = std::make_shared<Model>(input_, output_, args_, 0);
  if (args_->model == model_name::sup) {
    model_->setTargetCounts(dict_->getCounts(entry_type::label));
  } else {
    model_->setTargetCounts(dict_->getCounts(entry_type::word));
  }
}

void FastText::startThreads() {
  start_ = clock();
  tokenCount_ = 0;
  loss_ = -1;
  std::vector<std::thread> threads;
  for (int32_t i = 0; i < args_->thread; i++) {
    threads.push_back(std::thread([=]() { trainThread(i); }));
  }
  const int64_t ntokens = dict_->ntokens();
  // Same condition as trainThread
  while (tokenCount_ < args_->epoch * ntokens) {
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    if (loss_ >= 0 && args_->verbose > 1) {
      real progress = real(tokenCount_) / (args_->epoch * ntokens);
      std::cerr << "\r";
      printInfo(progress, loss_, std::cerr);
    }
  }
  for (int32_t i = 0; i < args_->thread; i++) {
    threads[i].join();
  }
  if (args_->verbose > 0) {
      std::cerr << "\r";
      printInfo(1.0, loss_, std::cerr);
      std::cerr << std::endl;
  }
}

int FastText::getDimension() const {
    return args_->dim;
}

bool FastText::isQuant() const {
  return quant_;
}

}
