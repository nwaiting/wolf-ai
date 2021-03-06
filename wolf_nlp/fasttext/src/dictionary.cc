/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

#include "dictionary.h"

#include <assert.h>

#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <cmath>
#include <stdexcept>

namespace fasttext {

const std::string Dictionary::EOS = "</s>";
const std::string Dictionary::BOW = "<";
const std::string Dictionary::EOW = ">";

Dictionary::Dictionary(std::shared_ptr<Args> args) : args_(args),
  word2int_(MAX_VOCAB_SIZE, -1), size_(0), nwords_(0), nlabels_(0),
  ntokens_(0), pruneidx_size_(-1) {}

Dictionary::Dictionary(std::shared_ptr<Args> args, std::istream& in) : args_(args),
  size_(0), nwords_(0), nlabels_(0), ntokens_(0), pruneidx_size_(-1) {
  load(in);
}

int32_t Dictionary::find(const std::string& w) const {
  return find(w, hash(w));
}

int32_t Dictionary::find(const std::string& w, uint32_t h) const {
  int32_t word2intsize = word2int_.size();
  int32_t id = h % word2intsize;
  while (word2int_[id] != -1 && words_[word2int_[id]].word != w) {
    id = (id + 1) % word2intsize;
  }
  return id;
}

void Dictionary::add(const std::string& w) {
  int32_t h = find(w);
  ntokens_++;
  if (word2int_[h] == -1) {
    entry e;
    e.word = w;
    e.count = 1;
    e.type = getType(w);
    words_.push_back(e);
    word2int_[h] = size_++;
  } else {
    words_[word2int_[h]].count++;
  }
}

int32_t Dictionary::nwords() const {
  //单词的个数
  return nwords_;
}

int32_t Dictionary::nlabels() const {
  return nlabels_;
}

int64_t Dictionary::ntokens() const {
  //总的个数 = 词数 + label数
  return ntokens_;
}

const std::vector<int32_t>& Dictionary::getSubwords(int32_t i) const {
  assert(i >= 0);
  assert(i < nwords_);
  return words_[i].subwords;
}

//获取一个词的词向量，不仅仅是对已知的，还能对未知进行预测
const std::vector<int32_t> Dictionary::getSubwords(
    const std::string& word) const {
  int32_t i = getId(word);
  if (i >= 0) {
    return getSubwords(i);
  }
  std::vector<int32_t> ngrams;
  if (word != EOS) {
    computeSubwords(BOW + word + EOW, ngrams);
  }
  return ngrams;
}

/*
    getSubwords被用于训练词向量模型(skipgram和cbow)、输出词向量(print-word-vectors和print-sentence-vectors)、计算词相似性(nn和analogies)
*/
void Dictionary::getSubwords(const std::string& word,
                           std::vector<int32_t>& ngrams,
                           std::vector<std::string>& substrings) const {
  int32_t i = getId(word);
  ngrams.clear();
  substrings.clear();
  if (i >= 0) {
    ngrams.push_back(i);
    substrings.push_back(words_[i].word);
  }

  //如果该词在入库词典中没有，则计算ngram，然后就可以通过其他词的近似ngram来获取该词的ngram
  if (word != EOS) {
    computeSubwords(BOW + word + EOW, ngrams, substrings);
  }
}

bool Dictionary::discard(int32_t id, real rand) const {
  assert(id >= 0);
  assert(id < nwords_);
  if (args_->model == model_name::sup) return false; //非词向量不丢弃
  return rand > pdiscard_[id];
}

int32_t Dictionary::getId(const std::string& w, uint32_t h) const {
  int32_t id = find(w, h);
  return word2int_[id];
}

int32_t Dictionary::getId(const std::string& w) const {
  int32_t h = find(w);
  return word2int_[h];
}

entry_type Dictionary::getType(int32_t id) const {
  assert(id >= 0);
  assert(id < size_);
  return words_[id].type;
}

entry_type Dictionary::getType(const std::string& w) const {
  return (w.find(args_->label) == 0) ? entry_type::label : entry_type::word;
}

std::string Dictionary::getWord(int32_t id) const {
  assert(id >= 0);
  assert(id < size_);
  return words_[id].word;
}

uint32_t Dictionary::hash(const std::string& str) const {
  uint32_t h = 2166136261;
  for (size_t i = 0; i < str.size(); i++) {
    h = h ^ uint32_t(str[i]);
    h = h * 16777619;
  }
  return h;
}

void Dictionary::computeSubwords(const std::string& word,
                               std::vector<int32_t>& ngrams,
                               std::vector<std::string>& substrings) const {
  for (size_t i = 0; i < word.size(); i++) {
    std::string ngram;
    if ((word[i] & 0xC0) == 0x80) continue;
    //n-1个词背景
    for (size_t j = i, n = 1; j < word.size() && n <= args_->maxn; n++) { 
      ngram.push_back(word[j++]);

      //处理utf-8字符，见 https://blog.csdn.net/lainegates/article/details/77776419
      //utf-8是变长编码，utf-8分3种情况，0或者10或者110/1110等
      while (j < word.size() && (word[j] & 0xC0) == 0x80) {
        ngram.push_back(word[j++]);
      }

      if (n >= args_->minn && !(n == 1 && (i == 0 || j == word.size()))) {
        int32_t h = hash(ngram) % args_->bucket;
        ngrams.push_back(nwords_ + h);
        substrings.push_back(ngram);
      }
    }
  }
}

// 该函数仅被 Dictionary::getSubword（...）调用
// Dictionary::getSubword（...）被用于训练词向量模型(skipgram和cbow）
// 、输出词向量（print-word-vectors和print-sentence-vectors）和计算词相似性（nn和analogies）
// ！！！也就是说这个函数计算的ngram与分类不相关！！！
void Dictionary::computeSubwords(const std::string& word,
                               std::vector<int32_t>& ngrams) const {
  for (size_t i = 0; i < word.size(); i++) {
    std::string ngram;
    if ((word[i] & 0xC0) == 0x80) continue;
    for (size_t j = i, n = 1; j < word.size() && n <= args_->maxn; n++) {
      ngram.push_back(word[j++]);
      while (j < word.size() && (word[j] & 0xC0) == 0x80) {
        ngram.push_back(word[j++]);
      }
      if (n >= args_->minn && !(n == 1 && (i == 0 || j == word.size()))) {
        int32_t h = hash(ngram) % args_->bucket;
        pushHash(ngrams, h);
      }
    }
  }
}

void Dictionary::initNgrams() {
  for (size_t i = 0; i < size_; i++) {
    std::string word = BOW + words_[i].word + EOW;
    words_[i].subwords.clear();
    words_[i].subwords.push_back(i);
    if (words_[i].word != EOS) {
      computeSubwords(word, words_[i].subwords);
    }
  }
}

bool Dictionary::readWord(std::istream& in, std::string& word) const
{
  int c;
  std::streambuf& sb = *in.rdbuf();
  word.clear();
  while ((c = sb.sbumpc()) != EOF) {
    if (c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == '\v' ||
        c == '\f' || c == '\0') {
      if (word.empty()) {
        if (c == '\n') {
          word += EOS;
          return true;
        }
        continue;
      } else {
        if (c == '\n')
          sb.sungetc();
          //streambuf 类同样定义了如下几个函数来支持对于输入缓冲区的读取和管理：
            //sgetc: 从输入缓冲区中读取一个字符；
            //sbumpc : 从输入缓冲区中读取一个字符，并将 gptr() 指针向后移动一个位置；
            //sgetn : 从输入缓冲区中读取 n 个字符；
            //sungetc : 将缓冲区的 gptr() 指针向前移动一个位置；
            //sputbackc : 将一个读取到的字符重新放回到输入缓冲区中；
        return true;
      }
    }
    word.push_back(c);
  }
  // trigger eofbit
  in.get();
  return !word.empty();
}

void Dictionary::readFromFile(std::istream& in) {
  std::string word;
  int64_t minThreshold = 1;
  //每次读入一个词
  while (readWord(in, word)) { 
    //向词典添加单词
    add(word); 
    if (ntokens_ % 1000000 == 0 && args_->verbose > 1) {
      std::cerr << "\rRead " << ntokens_  / 1000000 << "M words" << std::flush;
    }

    //保证word和label的总数小于限额
    if (size_ > 0.75 * MAX_VOCAB_SIZE) {
      minThreshold++;
      //超过限额，删除一些低频词
      //reduce单词，和word2vec的reduce一样
      threshold(minThreshold, minThreshold);
    }
  }

  //语料扫描完以后再去掉低频词
  threshold(args_->minCount, args_->minCountLabel);
  
  //与 word2vec 中处理高频和低频单词一样，以一定的概率过滤掉单词
  //初始化采样概率表
  initTableDiscard();
  
  //用于得到单词的subword
  initNgrams();
  if (args_->verbose > 0) {
    std::cerr << "\rRead " << ntokens_  / 1000000 << "M words" << std::endl;
    std::cerr << "Number of words:  " << nwords_ << std::endl;
    std::cerr << "Number of labels: " << nlabels_ << std::endl;
  }
  if (size_ == 0) {
    throw std::invalid_argument(
        "Empty vocabulary. Try a smaller -minCount value.");
  }
}

void Dictionary::threshold(int64_t t, int64_t tl) {
  sort(words_.begin(), words_.end(), [](const entry& e1, const entry& e2) {
      if (e1.type != e2.type) return e1.type < e2.type;
      return e1.count > e2.count;
    });
  words_.erase(remove_if(words_.begin(), words_.end(), [&](const entry& e) {
        return (e.type == entry_type::word && e.count < t) ||
               (e.type == entry_type::label && e.count < tl);
      }), words_.end());

  //当vector中数据太大，有删除操作时，手动释放空间有两种方法：1、swap  2、shrink_to_fit
  //释放的是没有使用的空间
  //手动释放空间 c++11增加
  words_.shrink_to_fit();
  size_ = 0;
  nwords_ = 0;
  nlabels_ = 0;
  //fill和fill_n两个函数都是用value填充begin和end的值
  std::fill(word2int_.begin(), word2int_.end(), -1);
  for (auto it = words_.begin(); it != words_.end(); ++it) {
    int32_t h = find(it->word);
    word2int_[h] = size_++;
    if (it->type == entry_type::word) nwords_++;
    if (it->type == entry_type::label) nlabels_++;
  }
}

//初始化initTableDiscard表，对每个词根据词的频率获取相应的丢弃概率值，若是给定的阈值小于这个表的值那么就丢弃该词，这里是因为对于频率过高的词可能就是无用词，所以丢弃。比如"的"，"是"等；这里的实现与论文中有点差异，这里是当表中的词小于某个值表示该丢弃，这里因为这里没有对其求1-p形式，而是p+p^2。若是同理转为同方向，则论文是p，现实是p+p^2，这样的做法是使得打压更加宽松点，也就是更多词会被当作无用词丢弃 ??
//以一定的概率过滤掉单词
void Dictionary::initTableDiscard() {
  pdiscard_.resize(size_);
  for (size_t i = 0; i < size_; i++) {
    //词频 (words是删除低频单词后的结果列表,  ntokens是总共的单词数)
    real f = real(words_[i].count) / real(ntokens_);
    //是为了后面以一定的概率删除词频很高的词，公式：r=sqrt(t/f)+t/f，其中t为一阈值，f为词频，处理方式和word2vec一致
    pdiscard_[i] = std::sqrt(args_->t / f) + args_->t / f;
  }
}

std::vector<int64_t> Dictionary::getCounts(entry_type type) const {
  std::vector<int64_t> counts;
  for (auto& w : words_) {
    if (w.type == type) counts.push_back(w.count);
  }
  return counts;
}

void Dictionary::addWordNgrams(std::vector<int32_t>& line,
                               const std::vector<int32_t>& hashes,
                               int32_t n) const {
  for (int32_t i = 0; i < hashes.size(); i++) {
    uint64_t h = hashes[i];
    //n就是wordNgram
    for (int32_t j = i + 1; j < hashes.size() && j < i + n; j++) {
      /*
        fasttext使用两种ngram
        词向量的ngram是分解词,如 abc => a,ab,abc,b,bc
        分类的ngram是组合词，如 a,b,c => a,ab,abc,b,bc
      */
      h = h * 116049371 + hashes[j];
      pushHash(line, h % args_->bucket);
    }
  }
}

void Dictionary::addSubwords(std::vector<int32_t>& line,
                             const std::string& token,
                             int32_t wid) const {
  if (wid < 0) { // out of vocab
    if (token != EOS) {
      computeSubwords(BOW + token + EOW, line);
    }
  } else {
    if (args_->maxn <= 0) { // in vocab w/o subwords
      line.push_back(wid);
    } else { // in vocab w/ subwords
      const std::vector<int32_t>& ngrams = getSubwords(wid);
      //vector::cbegin表示const begin
      line.insert(line.end(), ngrams.cbegin(), ngrams.cend());
    }
  }
}

void Dictionary::reset(std::istream& in) const {
  if (in.eof()) {
    in.clear();
    in.seekg(std::streampos(0));
  }
}

int32_t Dictionary::getLine(std::istream& in,
                            std::vector<int32_t>& words,
                            std::minstd_rand& rng) const {
  std::uniform_real_distribution<> uniform(0, 1);
  std::string token;
  int32_t ntokens = 0;

  reset(in);
  words.clear();
  while (readWord(in, token)) {
    //得到单词的哈希值
    int32_t h = find(token);

    //得到单词的id
    int32_t wid = word2int_[h];
    if (wid < 0) continue;

    ntokens++;
    //确定是单词还是标签，如果是单词且没有被subsampling掉，discard 会计算概率过滤掉一些词
    if (getType(wid) == entry_type::word && !discard(wid, uniform(rng))) {
      //存入单词id
      words.push_back(wid);
    }
    if (ntokens > MAX_LINE_SIZE || token == EOS) break;
  }
  return ntokens;
}

// 输入是文件流，输出是的得到一行单词的id、得到一行的label
int32_t Dictionary::getLine(std::istream& in,
                            std::vector<int32_t>& words,
                            std::vector<int32_t>& labels) const {
  std::vector<int32_t> word_hashes;
  std::string token;
  int32_t ntokens = 0;

  reset(in);
  words.clear();
  labels.clear();
  while (readWord(in, token)) {
    uint32_t h = hash(token);
    int32_t wid = getId(token, h);
    entry_type type = wid < 0 ? getType(token) : getType(wid);

    ntokens++;
    if (type == entry_type::word) {
      addSubwords(words, token, wid);
      //存入单词哈希
      word_hashes.push_back(h);
    } else if (type == entry_type::label && wid >= 0) {
      //保存label
      labels.push_back(wid - nwords_);
    }
    //如果换行就跳出循环
    if (token == EOS) break;
  }

  //对于有监督任务还要加入ngram，words中包括了单词和ngram的id
  // 将一个词的 n-gram 加入词表，用于处理未登录词。（即便一个词不在词表里，我们也可以用它的 word n-gram 来预测一个结果）
  addWordNgrams(words, word_hashes, args_->wordNgrams);
  // 返回读取了多少的单词
  return ntokens;
}

void Dictionary::pushHash(std::vector<int32_t>& hashes, int32_t id) const {
  if (pruneidx_size_ == 0 || id < 0) return;
  if (pruneidx_size_ > 0) {
    if (pruneidx_.count(id)) {
      id = pruneidx_.at(id);
    } else {
      return;
    }
  }
  hashes.push_back(nwords_ + id);
}

std::string Dictionary::getLabel(int32_t lid) const {
  if (lid < 0 || lid >= nlabels_) {
    throw std::invalid_argument(
        "Label id is out of range [0, " + std::to_string(nlabels_) + "]");
  }
  return words_[lid + nwords_].word;
}

void Dictionary::save(std::ostream& out) const {
  out.write((char*) &size_, sizeof(int32_t));
  out.write((char*) &nwords_, sizeof(int32_t));
  out.write((char*) &nlabels_, sizeof(int32_t));
  out.write((char*) &ntokens_, sizeof(int64_t));
  out.write((char*) &pruneidx_size_, sizeof(int64_t));
  for (int32_t i = 0; i < size_; i++) {
    entry e = words_[i];
    out.write(e.word.data(), e.word.size() * sizeof(char));
    out.put(0);
    out.write((char*) &(e.count), sizeof(int64_t));
    out.write((char*) &(e.type), sizeof(entry_type));
  }
  for (const auto pair : pruneidx_) {
    out.write((char*) &(pair.first), sizeof(int32_t));
    out.write((char*) &(pair.second), sizeof(int32_t));
  }
}

void Dictionary::load(std::istream& in) {
  words_.clear();
  in.read((char*) &size_, sizeof(int32_t));
  in.read((char*) &nwords_, sizeof(int32_t));
  in.read((char*) &nlabels_, sizeof(int32_t));
  in.read((char*) &ntokens_, sizeof(int64_t));
  in.read((char*) &pruneidx_size_, sizeof(int64_t));
  for (int32_t i = 0; i < size_; i++) {
    char c;
    entry e;
    while ((c = in.get()) != 0) {
      e.word.push_back(c);
    }
    in.read((char*) &e.count, sizeof(int64_t));
    in.read((char*) &e.type, sizeof(entry_type));
    words_.push_back(e);
  }
  pruneidx_.clear();
  for (int32_t i = 0; i < pruneidx_size_; i++) {
    int32_t first;
    int32_t second;
    in.read((char*) &first, sizeof(int32_t));
    in.read((char*) &second, sizeof(int32_t));
    pruneidx_[first] = second;
  }
  initTableDiscard();
  initNgrams();

  int32_t word2intsize = std::ceil(size_ / 0.7);
  word2int_.assign(word2intsize, -1);
  for (int32_t i = 0; i < size_; i++) {
    word2int_[find(words_[i].word)] = i;
  }
}

void Dictionary::init() {
  initTableDiscard();
  initNgrams();
}

void Dictionary::prune(std::vector<int32_t>& idx) {
  std::vector<int32_t> words, ngrams;
  for (auto it = idx.cbegin(); it != idx.cend(); ++it) {
    if (*it < nwords_) {words.push_back(*it);}
    else {ngrams.push_back(*it);}
  }
  std::sort(words.begin(), words.end());
  idx = words;

  if (ngrams.size() != 0) {
    int32_t j = 0;
    for (const auto ngram : ngrams) {
      pruneidx_[ngram - nwords_] = j;
      j++;
    }
    idx.insert(idx.end(), ngrams.begin(), ngrams.end());
  }
  pruneidx_size_ = pruneidx_.size();

  std::fill(word2int_.begin(), word2int_.end(), -1);

  int32_t j = 0;
  for (int32_t i = 0; i < words_.size(); i++) {
    if (getType(i) == entry_type::label || (j < words.size() && words[j] == i)) {
      words_[j] = words_[i];
      word2int_[find(words_[j].word)] = j;
      j++;
    }
  }
  nwords_ = words.size();
  size_ = nwords_ +  nlabels_;
  words_.erase(words_.begin() + size_, words_.end());
  initNgrams();
}

void Dictionary::dump(std::ostream& out) const {
  out << words_.size() << std::endl;
  for (auto it : words_) {
    std::string entryType = "word";
    if (it.type == entry_type::label) {
      entryType = "label";
    }
    out << it.word << " " << it.count << " " << entryType << std::endl;
  }
}

}
