### Google算法 - 系统设计简介
- **Google索引系统：**
>       先由URL Server发送一系列的URL地址让网站爬虫Crawlers去采集，网页采集后交给存储服务器Store Server，存储服务器压缩网页内容后存放到信息仓库Repository。所有的新网页都被赋予一个docID。
>           索引功能由索引器Indexer和排序器Sorter来执行完成。
>       Indexer读取Repository的文件，并将其转换为一系列的关键字排序，称为命中hits。Hits记录了关键字，出现在文件的位置，字体的相对大小和字母的大小写。
>       Indexer然后将这些hits放到一系列的桶Barrels中，建立了部分排 序好了的正向索引。Indexer还分离出网页中的所有链接，将重要的信息存放在Anchors文件中。这个文件包含的信息可以确定链接的指向和链接的描述文件。
>       URL Server读取Anchors文件并将相对URL转换为绝对URL，并依次放到docID中。它再将链接的描述文件放到正向索引，并将docID与链接的描述文本相对应。同时，它也产生一个链接links和docIDs相对应的数据库。
>           这个links数据库将被用于计算所有网页的PageRanks。
>
>       然后，排序器Sorter从Barrels中取得按docID排序的网页，再将其按照wordID产生一个反向索引。Sorter还在反向索引产生一个wordIDs及其偏移的列表。
>           一个叫做DumpLexicon的程序将这个列表结合搜索引擎的词库再产生一个可以被搜索器Searcher使用的新的词库Lexicon。由网页服务器构成的搜索引擎Searcher利用这个新的词库配合反向索引和PageRanks来回答查询。
>
>       命中列表Hit Lists记录了一系列的关键字出现在一个网页中的信息，包括在网页中的位置，字体的相对大小和字母的大小写。Hit Lists占用了正向和反向索引里的绝大部分的空间。
>       命中分为两种：特别命中Fancy Hits和普通命中Plain Hits。
>       Fancy Hits包括了在URL、标题、链接文本、元标签出现的关键字，所有在其它位置出现的关键字均为Plain Hits。
>       一个Plain Hits由大小写位1bit，字体大小3bits和用来表示关键字在网页的位置所组成12位bits位置（所有位置大于4095的均表示为4096）。
>
>       正向索引由64个桶Barrel组成，每个Barrel存放了一个特定范围的wordIDs。如果一个网页包含的关键字属于某个Barrel范围，这个docID就记录到这个特定的Barrel之中。
>           docID与wordIDs以及这些关键字的命中列表Hit Lists一起记录在这个Barrel中。
>
>       反向索引与正向使用相同的Barrels，唯一的区别是反向索引由排序器Sorter处理。对每一个有效的wordID，词库Lexicon中包含了指针指向具体的Barrel。
>           它指向的由docID组成的docList列表，以及它们所对应的命中列表Hit Lists。这个docList代表了那个单词在所有文件中所出现的列表。
>


- **Google查询流程：**
>       （1）解析查询关键字。
>       （2）转换关键字为wordIDs。
>       （3）在短桶Short Barrels中寻找每个关键字在docList的起点。
>       （4）扫描这个docList直到有个网页与查询全部匹配。
>       （5）计算这个网页的查询排名Rank。
>       （6）如果在短桶Short Barrels docList列表已经查完，寻找每个关键字在长桶Long Barrels docList的起点，重复第4步。
>       （7）如果还没有查完docList，重复第4步。
>       （8）将匹配的网页根据计算出的rank排序，并返回前k个查询结果。
>
>
>
>

- **Google的排名系统：**
>       Google包含了比其它搜索引擎更多的网页信息，每一个Hit List包含了位置、字体、大小写信息。另为Google还参考了anchor text以及网页的PageRank。没有一个单一的因素会对搜索结果的排序产生太大的影响。
>       让我们来看一下单个关键字的查询：Google先查看对应于这个单词的网页的命中列表Hist List。
>       Google区分每个Hit由几种不同的类型（标题、anchor、URL、大小写字体），每一种类型都有自己的类型权重Type-Weight，这些Type-Weights组成一个类型向量。
>       Google计算每一种类型的命中计数，然后这些命中计数又转换为计数权重Count-Weights。计数权重开始以线性增加，然后很快就逐渐停止，这样太多的命中计数就会没有作用。
>       Google在将Count-Weights和Type-Weight相乘计算出网页的IR Score。最后这个IR Score与PageRank相结合得到最终的搜索排序结果。
>
>       对于多关键词的搜索，计算方法就比较复杂一些。现在多个命中列表必须要全部扫描，这样对那些出现在文章中靠近的Hits就比那些分开较远的Hits有更高的权重。
>       那些相接近的Hits被匹配到一起，然后计算出这些相匹配的Hits的相关度Proximity。相>关度是基于这些Hits出现在文章中的距离决定的，并被分为10个不同的值，分别表示为短语匹配（Phrase Match）到根本不匹配（Not Even Close）。
>       命中计数不仅计算每种类型，而且还计算每个类型和它们的相关度匹配。每个类型和相关度配对有一个type-prox-weight权重。这个计数器被转换为计数权重。
>       然后这个计数权重与类型权重type-prox-weights相乘得到文章的IR Score。当然最后是IR Score与PageRank相结合得到最终搜索排序的结果。
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

- **待续：**
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
>
>
>
>
>
>
