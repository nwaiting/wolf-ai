### 主要是Hanlp的常用功能以及相关算法介绍以及说明
    参考：http://www.hankcs.com/nlp/hanlp.html
- **标准分词**
    > 相关算法：
        词图的生成： http://www.hankcs.com/nlp/segment/the-word-graph-is-generated.html
- **NLP分词**
    >相关算法
        面向搜索引擎的分词器
- **N最短路径分词**
    >相关算法
        N最短路径分词： http://www.hankcs.com/nlp/segment/n-shortest-path-to-the-java-implementation-and-application-segmentation.html
- **CRF分词**
    >相关算法
        CRF对新词有很好的识别能力
        CRF分词：http://www.hankcs.com/nlp/segment/crf-segmentation-of-the-pure-java-implementation.html
- **极速词典分词**
    >相关算法
        自动机结合DoubleArrayTrie极速多模式匹配
        极速分词：http://www.hankcs.com/program/algorithm/aho-corasick-double-array-trie.html
- **用户自定义词典**
    >相关算法
        trie树分词：http://www.hankcs.com/program/java/tire-tree-participle.html
        自动机结合DoubleArrayTrie极速多模式匹配：http://www.hankcs.com/program/algorithm/aho-corasick-double-array-trie.html
- **中国人名识别**
    >相关算法：
        有一定的误命中率，比如误命中关键年，则可以通过在data/dictionary/person/nr.txt加入一条关键年 A1来排除关键年作为人名的可能性
        HMM-Viterbi角色标注中国人名识别：http://www.hankcs.com/nlp/chinese-name-recognition-in-actual-hmm-viterbi-role-labeling.html
- **音译人名识别、日本人名识别**
    >相关算法
        层叠隐马模型下的音译人名和日本人名识别：http://www.hankcs.com/nlp/name-transliteration-cascaded-hidden-markov-model-and-japanese-personal-names-recognition.html
- **地名识别**
    >相关算法
        HMM-Viterbi角色标注地名识别：http://www.hankcs.com/nlp/ner/place-names-to-identify-actual-hmm-viterbi-role-labeling.html
- **机构名识别**
    >相关算法
        HMM-Viterbi角色标注模型下的机构名识别：http://www.hankcs.com/nlp/ner/place-name-recognition-model-of-the-stacked-hmm-viterbi-role-labeling.html
- **关键词提取**
    >相关算法
        TextRank算法提取关键词的Java实现：http://www.hankcs.com/nlp/textrank-algorithm-to-extract-the-keywords-java-implementation.html
- **自动摘要**
    >相关算法
        TextRank算法自动摘要的Java实现：http://www.hankcs.com/nlp/textrank-algorithm-java-implementation-of-automatic-abstract.html
- **短语提取**
    >相关算法
        基于互信息和左右信息熵的短语提取识别：http://www.hankcs.com/nlp/extraction-and-identification-of-mutual-information-about-the-phrase-based-on-information-entropy.html
- **拼音转换、简繁转换**
    >相关算法
        汉字转拼音与简繁转换的Java实现：http://www.hankcs.com/nlp/java-chinese-characters-to-pinyin-and-simplified-conversion-realization.html#h2-17
- **文本推荐**
    >在搜索引擎的输入框中，用户输入一个词，搜索引擎会联想出最合适的搜索词，HanLP实现了类似的功能
- **语义距离**
    >相关算法
        为每个词分配一个语义ID，词与词的距离通过语义ID的差得到。语义ID通过《同义词词林扩展版》计算而来
    >说明：
        设想的应用场景是搜索引擎对词义的理解，词与词并不只存在“同义词”与“非同义词”的关系，就算是同义词，它们之间的意义也是有微妙的差别的
- **依存句法解析**
    >相关算法
        基于神经网络的高性能依存句法分析器：http://www.hankcs.com/nlp/parsing/neural-network-based-dependency-parser.html
        最大熵依存句法分析器的实现：http://www.hankcs.com/nlp/parsing/to-achieve-the-maximum-entropy-of-the-dependency-parser.html
            依存句法分析算法：自顶向下算法、 自底向上算法、 最大生成树算法
        基于CRF序列标注的中文依存句法分析器的Java实现：http://www.hankcs.com/nlp/parsing/crf-sequence-annotation-chinese-dependency-parser-implementation-based-on-java.html
- **相关新技术**
    >相关应用
        FastText,Word2Vec和WordRank 三种词嵌入模型
