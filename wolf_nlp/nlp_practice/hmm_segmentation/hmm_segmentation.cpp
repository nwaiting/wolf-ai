#include <iostream>
#include <string>
#include <stdint.h>
#include <fstream>
#include <map>
#include <vector>
#include <list>
#include <stack>
#include <sstream>
#include <numeric>
#include <cmath>
#include <iomanip>
#ifdef _WIN32
#include <WinBase.h>
#endif

using namespace std;

/*
    hmm的二阶和三阶的分词比较
    参考：https://blog.csdn.net/u010189459/article/details/38337031
    处理的文本格式为utf-8格式
*/


/*
    @将字符串中所有特定的字符串替换成新的字符串
*/
std::string& replace_all(std::string& str, std::string old_str, std::string new_str)
{
    while (true) {
        int32_t pos(0);
        if ((pos = str.find(old_str)) != std::string::npos) {
            str.replace(pos, old_str.length(), new_str);
        }
        else {
            break;
        }
    }

    return str;
}

/*
    @   将训练语料和测试语料中出现的汉字进行编码，将他们的对应关系存入文件，
        格式：汉字-编码，编码从0开始
*/
void makeDB(std::string infile_1, std::string infile_2, std::string outfile)
{
    ifstream file_one(infile_1);
    ifstream file_two(infile_2);
    if (!(file_one && file_two)) {
        fprintf(stdout, "open file error, %s, %s\n", infile_1.c_str(), infile_2.c_str());
        return;
    }

    ofstream o_file(outfile);
    if (!o_file) {
        fprintf(stdout, "open file error %s\n", outfile.c_str());
        return;
    }

    std::map<std::string, int32_t> map_cchar;
    int32_t id(-1);
    std::string line("");
    std::string cchar("");

    //读入文件
    while (getline(file_one, line)) {
        line = replace_all(line, "/", "");
        if (line.size() >= 3) {
            //逐字读取
            for (auto i = 0; i < line.size() - 2; i += 3) {
                cchar = line.substr(i, 3);
                if (map_cchar.find(cchar) == map_cchar.end()) {
                    id++;
                    map_cchar[cchar] = id;
                }
            }
        }
    }

    while (getline(file_two, line)) {
        line = replace_all(line, "/", "");
        if (line.size() >= 3) {
            //逐字读取
            for (auto i = 0; i < line.size() - 2; i += 3) {
                cchar = line.substr(i, 3);
                if (map_cchar.find(cchar) == map_cchar.end()) {
                    id++;
                    map_cchar[cchar] = id;
                }
            }
        }
    }

    //输出到文件
    for (auto& it: map_cchar) {
        o_file << it.first << " " << it.second << endl;
    }

    file_one.close();
    file_two.close();
    o_file.close();
}


/*
    @ 训练语料每个汉字后面加入对应的BEMS状态
*/
void makeBMES(std::string infile, std::string outfile)
{
    ifstream f_in(infile);
    ofstream f_out(outfile);
    if (!(f_in && f_out)) {
        fprintf(stdout, "open file error %s, %s", infile.c_str(), outfile.c_str());
        return;
    }

    std::string word_in(""), word_out(""), line_in(""), line_out("");
    while (getline(f_in, line_in)) {
        if (line_in.size() >= 3) {
            line_out.clear();
            line_in = replace_all(line_in, "/", " ");
            istringstream strstm(line_in);
            while (strstm >> word_in) {
                word_out.clear();
                if (word_in.size() % 3 != 0) {
                    fprintf(stdout, "word is not right %s\n", word_in.c_str());
                    return;
                }

                int32_t num = word_in.size() / 3;
                if (num <= 0) {
                    continue;
                }

                if (num == 1) {
                    word_out = word_in;
                    word_out += "/S";
                }
                else {
                    //复制单词中的第一个字
                    word_out.insert(word_out.size(), word_in, 0, 3);
                    word_out += "\B";

                    //逐个复制单词中间的字
                    for (auto i = 1; i < num - 1; i+=3) {
                        word_out.insert(word_out.size(), word_in, i*3, 3);
                        word_out += "/M";
                    }

                    //复制单词中的最后一个字
                    word_out.insert(word_out.size(), word_in, word_in.size()-3, 3);
                    word_out += "/E";
                }

                line_out += word_out;
            }
        }
    }

    f_out << line_out << endl;
}


/*
    @ 将汉字和编码的映射文件内存，构造map
*/

//转换类，获取编号
class DB
{
private:
    std::map<std::string, int32_t> cchar_map; //汉字-编码
    std::map<int32_t, std::string> index_map; //编码-汉字

public:
    DB(){}
    DB(std::string file);
    ~DB(){}
    std::string getCchar(int32_t id); //编码获取汉字
    int32_t getObservIndex(std::string cchar); //根据汉字获取编码
    int32_t getStateIndex(char state); //根据状态获取编码
    std::vector<int32_t> makeObservs(std::string line); //将输入的句子构造为发射符号序列
};

DB::DB(std::string file)
{
    ifstream f_in(file.c_str());
    if (!f_in) {
        fprintf(stdout, "open file error %s\n", file.c_str());
        return;
    }

    std::string line(""), word(""), cchar("");
    int32_t id = 0;
    while (getline(f_in, line)) {
        istringstream strstrm(line);
        strstrm >> word;
        cchar = word;
        strstrm >> word;
        id = atoi(word.c_str());
        cchar_map[cchar] = id;
        index_map[id] = cchar;
    }
}


std::string DB::getCchar(int32_t id)
{
    auto it = index_map.find(id);
    if (it != index_map.end()) {
        return it->second;
    }
    return NULL;
}

int32_t DB::getObservIndex(std::string cchar)
{
    auto ite = cchar_map.find(cchar);
    if (ite != cchar_map.end()) {
        return ite->second;
    }
    return -1;
}

int32_t DB::getStateIndex(char state)
{
    switch (state)
    {
    case 'B':
        return 0;
    case 'M':
        return 1;
    case 'E':
        return 2;
    case 'S':
        return 3;
    default:
        return -1;
    }
}

std::vector<int32_t> DB::makeObservs(std::string line)
{
    std::vector<int32_t> observ_vecs; //输出符号集
    std::string cchar(""), word("");
    int32_t num(0), index(-1);
    line = replace_all(line, "/", " ");
    cout << line << endl;
    istringstream strstm(line);
    while (strstm >> word) {
        if (word.size() % 3 != 0) {
            fprintf(stdout, "word is not right, %s", word);
            continue;
        }

        num = word.size() / 3;
        if (num == 0) {
            continue;
        }
        else {
            for (auto i = 0; i < num; i++) {
                cchar = word.substr(i * 3, 3);
                index = getObservIndex(cchar);
                observ_vecs.push_back(index);
            }
        }
    }

    return observ_vecs;
}

/*
    用最大似然估计的方法建立HMM的模型参数
*/
const double SMO_VALUE = 1.0; //平滑算法增加的值
const int32_t N = 4; //隐藏状态的个数
const int32_t M = 4677; //汉字的个数

/*
    模型训练，将频数转为频率（加1平滑）
*/
void turingAdd(const int32_t count[], double probs[], int32_t len)
{
    double sum = 0.0;
    for (auto i = 0; i < len; i++) {
        sum += count[i];
    }
    sum += SMO_VALUE * len;

    for (auto i = 0; i < len; i++) {
        probs[i] = -log((count[i] + SMO_VALUE) / sum);
    }
}

/*
    模型训练，将发射频数转换为频率（古德-图灵平滑）
    计算步骤：
        1、计算在训练集中的词有多少个在测试集出现过c次
        2、重新估计各平滑后的值c*
            c* = (c+1)* (Nc+1/Nc)
            对于0次的：c*(.) = (0+1) * (N(0+1) / N(0)) = 0.667
        3、重新计算概率
            p'(.) = 0.667/12 
            0.667为重新估计的平滑后的c*
            12为测试集中集合大小

*/
void turingGood(const std::vector<int32_t>& count, std::vector<double>& probs)
{
    std::map<int32_t, std::list<int32_t> > freq_map; //key为词频，value为词频对于的汉字列表
    int32_t sum = 0;

    //初始化freq_map
    for (auto i = 0; i < count.size(); i++) {
        int32_t freq = count[i];
        sum += freq;
        auto ite = freq_map.find(freq);
        if (ite != freq_map.end()) {
            //如果存在将当前词加入到对应的list
            freq_map[freq].push_back(i);
        }
        else {
            std::list<int32_t> l;
            l.push_back(i);
            freq_map[freq] = l;
        }
    }

    if (sum <= 0) {
        for (auto i = 0; i < probs.size(); i++) {
            probs[i] = 0.0;
        }
        return;
    }

    //数据平滑处理
    auto mapIte = freq_map.begin();
    while (mapIte != freq_map.end()) {
        double pr = 1.0;
        int32_t freq = mapIte->first;
        int32_t freq_size = mapIte->second.size();
        if (++mapIte != freq_map.end()) {
            int32_t freq_2 = mapIte->first;
            if (freq_2 == freq + 1) {
                int32_t freq_size_2 = mapIte->second.size();
                pr = ((1.0 + freq) * freq_size_2) / (sum * freq_size);
            }
            else {
                pr = 1.0 * freq / sum;
            }
        }
        else {
            pr = 1.0 * freq / sum;
        }

        auto lt = (--mapIte)->second;
        auto ite_list = lt.begin();
        while (ite_list != lt.end()) {
            int32_t index = *ite_list;
            probs[index] = pr;
            ++ite_list;
        }

        mapIte++;
    }

    //数据归一化
    double total = std::accumulate(probs.begin(), probs.end(), 0.0);
    for (auto& it:probs) {
        it = -log((double)it / total);
    }
}

/*
    生成HMM模型的参数
    状态转移概率矩阵、初始状态概率矩阵、发送矩阵
*/
DB db("db.txt");

int generator_params(std::string outfile)
{
    ifstream f_in(outfile);
    if (!f_in) {
        fprintf(stdout, "open file %s error\n", outfile.c_str());
        return -1;
    }

    int32_t Pi[N] = { 0 };  //初始状态出现次数
    int32_t A1[N][N] = { 0 };  //二阶状态转移次数
    int32_t A2[N][N][N]= { 0 };  //三阶状态转移次数
    int32_t B1[N][M] = { 0 };  //二阶符号发送次数
    int32_t B2[N][N][M] = { 0 };  //三阶符号发送次数

    //抽取文件中的状态和观察值
    std::string line = "";
    int32_t line_num = 0;  //句子编号
    int32_t count = 0;
    while (getline(f_in, line)) {
        line_num++;
        //状态
        char state;
        //汉字
        std::string cchar = "";
        int32_t i, j, k, m;
        //当前处理位置
        std::string::size_type pos = 0;
        if ((pos = line.find("/", pos + 1)) != std::string::npos) {
            //抽取句子的第一个状态
            state = line.at(pos + 1);
            i = db.getStateIndex(state);
            Pi[i]++;

            //抽取句子的第一个观察值
            cchar = line.substr(pos - 3, 3);
            m = db.getObservIndex(cchar);
            B1[i][m]++;

            if ((pos = line.find("/", pos + 1)) != std::string::npos) {
                //抽取句子的第二个状态
                state = line.at(pos + 1);
                j = db.getStateIndex(state);
                A1[i][j]++;
                //抽取句子的第二个观测值
                cchar = line.substr(pos - 3, 3);
                m = db.getObservIndex(cchar);
                B1[i][j]++;
                B2[i][j][m]++;

                while ((pos = line.find("/", pos+1)) != std::string::npos) {
                    //抽取句子的其他状态
                    state = line.at(pos + 1);
                    k = db.getStateIndex(state);
                    A1[j][k]++;
                    A2[i][j][k]++;
                    //抽取句子的其他观察值
                    cchar = line.substr(pos - 3, 3);
                    m = db.getObservIndex(cchar);
                    B1[k][m]++;
                    B2[j][k][m]++;

                    //准备下次迭代
                    i = j;
                    j = k;
                }
            }
        }
    }
    f_in.close();

    //初始化矩阵
    ofstream f_out1("Pi.mat"); //初始化概率矩阵
    ofstream f_out2("A1.mat"); //二级状态转移矩阵
    ofstream f_out3("A2.mat"); //三阶状态转移矩阵
    ofstream f_out4("B1.mat"); //二级发送概率矩阵
    ofstream f_out5("B2.mat"); //三阶发送概率矩阵
    if (!(f_out1 && f_out2 && f_out3 && f_out4 && f_out5)) {
        fprintf(stdout, "open out file error\n");
        return -1;
    }

    //设置浮点数精度
    f_out1 << setprecision(8);
    f_out2 << setprecision(8);
    f_out3 << setprecision(8);
    f_out4 << setprecision(8);
    f_out5 << setprecision(8);

    //初始状态矩阵写入文件
    double arr_pi[N] = { 0.0 };
    turingAdd(Pi, arr_pi, N);
    for (auto i = 0; i < N; i++) {
        f_out1 << arr_pi[i] << "\t";
    }
    f_out1 << std::endl;

    //二阶状态转移矩阵写入文件
    double arr_a_1[N] = { 0.0 };
    for (auto i = 0; i < N;i++) {
        turingAdd(A1[i], arr_a_1, N);
        for (auto j = 0; j < N; j++) {
            f_out2 << arr_a_1[j] << "\t";
        }
        f_out2 << std::endl;
    }

    //三阶状态转移矩阵写入文件
    double arr_a_2[N] = { 0.0 };
    for (auto i = 0; i < N; i++) {
        for (auto j = 0; j < N; j++) {
            turingAdd(A2[i][j], arr_a_2, N);
            for (auto k = 0; k < N; k++) {
                f_out3 << arr_a_2[k] << "\t";
            }
            f_out3 << endl;
        }
    }

    //二阶发射概率矩阵写入文件
    double arr_b_1[N] = { 0.0 };
    for (auto i = 0; i < N; i++) {
        turingAdd(B1[i], arr_b_1, N);
        for (auto k = 0; k < N; k++) {
            f_out4 << arr_b_1[k] << "\t";
        }
        f_out4 << std::endl;
    }

    //三阶发送概率写入矩阵文件
    double arr_b_2[N] = { 0.0 };
    for (auto i = 0; i < N; i++) {
        for (auto j = 0; j < N; j++) {
            turingAdd(A2[i][j], arr_b_2, N);
            for (auto k = 0; k < N; k++) {
                f_out5 << arr_b_2[k] << "\t";
            }
            f_out5 << std::endl;
        }
    }

    f_out1.close();
    f_out2.close();
    f_out3.close();
    f_out4.close();
    f_out5.close();
}

//读入HMM的模型参数到内存中，构造HMM对象
class HMM
{
public:
    int32_t n;
    int32_t m;
    double Pi[N]; //初始概率
    double A1[N][N]; //二阶转移概率
    double A2[N][N][N]; //三阶转移概率
    double B1[N][M]; //二阶发送概率
    double B2[N][N][M]; //三阶发送概率

public:
    HMM(){}
    HMM(std::string f_pi, std::string f_a1, std::string f_a2, std::string f_b1, std::string f_b2){}
};


/*
    viterbi算法进行分词，二阶马尔科夫过程
*/
HMM hmm = HMM();
std::string viterbiTwo(std::string str_in)
{
    //计算输入句子中的汉字个数
    int32_t row = str_in.size() / 3;
    std::string str_out = "";

    if (row == 0) {
        return str_out;
    }

    //只有一个字
    if (row < 2) {
        str_out = str_in + "/";
        return str_out;
    }

    //分配矩阵空间
    //二级指针又名指向指针的指针。*[row]，先是数组，然后指针。也就是有row个double型指针的数组
    //第二步 delta[i]=new double[n]; i∈[0,row-1],再申请n个doulbe空间，one of m 只想这个空间
    double **delta = new double *[row];
    int32_t **path = new int32_t *[row];
    for (auto i = 0; i < row; i++) {
        delta[i] = new double[N]();
        path[i] = new int32_t[N]();
    }

    //中间变量
    std::string cchar = ""; //存汉字
    int32_t min_path = -1;
    double val = 0.0;
    double min_val = 0.0;

    //初始化矩阵，给delta和path矩阵的第一行赋初值
    cchar = str_in.substr(0, 3);
    int32_t cchar_num = db.getObservIndex(cchar);
    for (auto i = 0; i < N; i++) {
        delta[0][i] = hmm.Pi[i] + hmm.B1[i][cchar_num]; //对数
        path[0][i] = -1;
    }

    //给delta和path的后续行赋值（对数）
    for (auto t = 1; t < row; t++) {
        cchar = str_in.substr(t * 3, 3);
        cchar_num = db.getObservIndex(cchar);
        for (auto j = 0; j < N; j++) {
            min_val = 100000.0;
            min_path = -1;
            for (auto i = 0; i < N; i++) {
                val = delta[t - 1][i] + hmm.A1[i][j];
                if (val < min_val) {
                    min_path = val;
                    min_path = i;
                }
            }

            delta[t][j] = min_val + hmm.B1[j][cchar_num];
            path[t][j] = min_path;
        }
    }

    //找delta矩阵最后一行的最小值
    min_val = 100000.0;
    min_path = -1;
    for (auto i = 0; i < N; i++) {
        if (delta[row-1][i] < min_val) {
            min_val = delta[row - 1][i];
            min_path = i;
        }
    }

    //从min_path出发，回溯得到最可能的路径
    std::stack<int32_t> path_st;
    path_st.push(min_path);
    for (auto i = row - 1; i > 0; i--) {
        min_path = path[i][min_path];
        path_st.push(min_path);
    }

    //释放二维数组
    for (auto i = 0; i < N; i++) {
        delete[]delta[i];
        delete[]path[i];
    }
    delete[]delta;
    delete[]path;

    //根据标记好的状态序列分词
    int32_t pos = 0;
    int32_t index = -1;
    while (!path_st.empty()) {
        index = path_st.top();
        path_st.pop();
        str_out.insert(str_out.size(), str_in, pos, 3);
        if (index == 2 || index == 3) {
            //状态为E或S
            str_out.append("/");
        }
        pos += 3;
    }

    return NULL;
}


/*
    viterbi算法分词：三阶马尔科夫过程
*/
std::string viterbiThree(std::string str_in)
{
    //计算输入句子中的汉字个数
    int32_t row = str_in.size() / 3;
    std::string str_out("");

    //如果输入字符串为空，则直接返回空
    if (row == 0) {
        return str_out;
    }

    //如果只有一个字的话，直接输出即可
    if (row < 2) {
        str_out = str_in + "/";
        return str_out;
    }

    //分配矩阵空间
    double ***delta = new double **[row];
    int32_t ***path = new int32_t **[row];
    for (auto i = 0; i < row; i++) {
        delta[i] = new double *[N];
        path[i] = new int32_t *[N];
        for (auto j = 0; j < N; j++) {
            delta[i][j] = new double[N];
            path[i][j] = new int32_t[N];
            for (auto k = 0; k < N; k++) {
                delta[i][j][k] = 0.0;
                path[i][j][k] = 0;
            }
        }
    }

    //初始化矩阵，给delta和path矩阵的第1个面赋初值
    //初始状态需要两个面，第0个面不赋值，第1个面赋值
    std::string cchar_1 = str_in.substr(0, 3); //第一个字
    std::string cchar_2 = str_in.substr(3, 3); //第二个字
    int32_t num_1 = db.getObservIndex(cchar_1); //第一个字编号
    int32_t num_2 = db.getObservIndex(cchar_2); //第二个字编号
    for (auto i = 0; i < N; i++) {
        for (auto j = 0; j < N; j++) {
            delta[1][i][j] = hmm.Pi[i] + hmm.B1[i][num_1] + hmm.A1[i][j] + hmm.B2[i][j][num_2];
            path[1][i][j] = -1;
        }
    }

    //中间变量
    std::string cchar_3("");
    int32_t min_path = -1;
    double val = 0.0;
    double min_val = 0.0;

    //给delta和path的后续面赋值（对数）
    //第0、1面为初始面，后续面从2开始，到row-1为止
    for (auto t = 2; t < row; t++) {
        cchar_3 = str_in.substr(t * 3, 3);
        int32_t num_3 = db.getObservIndex(cchar_3);
        for (auto j = 0; j < N; j++) {
            for (auto k = 0; k < N; k++) {
                min_val = 100000.0;
                min_path = -1;
                for (auto i = 0; i < N; i++) {
                    val = delta[t - 1][i][j] + hmm.A2[i][j][k];
                    if (val < min_val) {
                        min_val = val;
                        min_path = i;
                    }
                }

                delta[t-1][j][k] = min_val + hmm.B2[j][k][num_3];
                path[t][j][k] = min_path;
            }
        }
    }

    //找delta矩阵最后一个面的最大值，最后一个面为row-1
    min_val = 100000.0;
    int32_t min_path_i = -1;
    int32_t min_path_j = -1;
    for (auto i = 0; i < N; i++) {
        for (auto j = 0; j < N; j++) {
            if (delta[row-1][i][j] < min_val) {
                min_val = delta[row - 1][i][j];
                min_path_i = i;
                min_path_j = j;
            }
        }
    }

    //从min_path_i和min_path_j出发，回溯得到最可能的路径
    //回溯从row-1开始，到2为止 
    std::stack<int32_t> path_st;
    path_st.push(min_path_j);
    path_st.push(min_path_i);
    for (auto t = row - 1; t > 0; t--) {
        int32_t min_path_k = path[t][min_path_i][min_path_j];
        path_st.push(min_path_k);
        min_path_j = min_path_i;
        min_path_i = min_path_k;
    }

    //释放三维数组
    for (auto i = 0; i < row; i++) {
        for (auto j = 0; j < row; j++) {
            delete[]delta[i][j];
            delete[]path[i][j];
        }
        delete[]delta[i];
        delete[]path[i];
    }
    delete[]delta;
    delete[]path;

    //根据标记好的状态序列分词
    int32_t pos = 0;
    int32_t index = -1;
    while (!(path_st.empty())) {
        index = path_st.top();
        path_st.pop();
        str_out.insert(str_out.size(), str_in, pos, 3);
        if (index == 2 || index == 3) {
            //状态为E或S
            str_out += "/";
        }
        pos += 3;
    }
}

//获取时间
int64_t getCurrentTime()
{
    int64_t MSTime = 0;
#ifdef _WIN32
    MSTime = GetTickCount();
#else
    timeval tv;
    gettimeofday(&tv, NULL);
    MSTime = (tv.tv_sec * 1000) + (tv.tv_usec / 1000);
#endif
    return MSTime;
}

//获取文件大小
int64_t getFileSize(const std::string& file_path)
{
    int64_t filesize = -1;
    struct stat statbuff;
    if (stat(file_path.c_str(), &statbuff) < 0) {
        return filesize;
    }
    else {
        filesize = statbuff.st_size;
    }
    return filesize;
}

/*
    计算切分标记的位置
    参数：strline_in未进行切分的汉字字符串
          strline_right切分后的字符串
    输出：vector,存放了strline_in中哪些位置放置了分词标记
          注意：vector中不包含最后标记的位置，包含位置0
*/
std::vector<int32_t> getPos(std::string strline_right, std::string strline_in)
{
    int32_t pos_1 = 0, pos_2 = -1, pos_3 = 0;
    std::string word("");
    std::vector<int32_t> vec;

    int32_t len = strline_right.length();
    while (pos_2 < len) {
        //前面的分词标记
        pos_1 = pos_2;  

        //后面的分词标记
        pos_2 = strline_right.find('/', pos_1 + 1);
        if (pos_2 > pos_1) {
            //将两个标记之间的单词取出
            word = strline_right.substr(pos_1 + 1, pos_2 - pos_1 - 1);
            //根据单词去输入中查找出现的位置
            pos_3 = strline_in.find(word, pos_3);
            //将位置存入数组
            vec.push_back(pos_3);
            pos_3 = pos_3 + word.size();
        }
        else {
            break;
        }
    }

    return vec;
}

/*
    获取标准切分和程序切分的结果
*/
std::string getString(std::string word, int32_t pos, std::vector<int32_t> vec_right)
{
    char ss[1000];
    int32_t i = 0, k = 0;
    if (vec_right.size() <= 0) {
        return word;
    }

    while (vec_right[i] < pos) {
        i++;
    }

    for (int32_t j = 0; j < word.size(); j++) {
        if (j == vec_right[i] - pos) {
            if (j != 0) {
                ss[k] = '/'; 
                k++;
            }
            i++;
        }
        ss[k] = word[j];
        k++;
    }
    ss[k] = '\0';
    return std::string(ss);
}


/*
    获取单个句子切分的结果统计
    参数：vec_right 正确的分词标记位置集合
          vec_out 函数切分得到的分词标记位置集合
    输出：vector，含有4个元素，为：
          切分正确、组合型歧义、为登录词、交集型歧义的数量
*/
std::vector<int32_t> getCount2(std::string strline, std::vector<int32_t> vec_right, std::vector<int32_t> vec_out, std::vector<std::string> &vec_err)
{
    //存放计算结果
    std::vector<int32_t> vec(4, 0);
    //建立map
    std::map<int32_t, int32_t> map_result;
    for (auto i = 0; i < vec_right.size(); i++) {
        map_result[vec_right[i]] += 1;
    }

    for (auto i = 0; i < vec_out.size(); i++) {
        map_result[vec_out[i]] += 2;
    }

    //统计map中的信息
    //若value=1，只在vec_right中
    //若value=2，只在vec_out中
    //若value=3，在vec_right和vec_out中都有 
    std::map<int32_t, int32_t>::iterator ite_pre, ite_cur;
    int32_t count_value_1 = 0;
    int32_t count_value_2 = 0;
    int32_t count_value_3 = 0;
    ite_pre = map_result.begin();
    ite_cur = map_result.begin();

    while (ite_cur != map_result.end()) {
        while (ite_cur != map_result.end() && ite_cur->second == 3) {
            ite_pre = ite_cur;
            count_value_3++; //切分正确的数目
            ite_cur++; //继续验证
        }

        while (ite_cur != map_result.end() && ite_cur->second != 3) {
            if (ite_cur->second == 1) {
                count_value_1++;
            }
            else if (ite_cur->second == 2) {
                count_value_2++;
            }
            ite_cur++;
        }

        //确定切分错误的字符串
        if (ite_cur == map_result.end() && ite_cur == ++ite_pre) {
            continue;
        }

        int32_t pos_1 = ite_pre->first;
        int32_t pos_2 = ite_cur->first;
        std::string word = strline.substr(pos_1, pos_2 - pos_1); //切分错误的单词
        std::string word_right = getString(word, pos_1, vec_right); //正确的切分方式
        std::string word_out = getString(word, pos_1, vec_out); //得到的切分方式

        std::string str_err("");
        //不同的错误类型
        if (count_value_1 > 0 && count_value_2 == 0) {
            str_err = "组合型歧义：" + word + " 正确切分：" + word_right + " 错误切分：" + word_out;
            vec_err.push_back(str_err);
            fprintf(stdout, "%s\n", str_err.c_str());
            vec[1] += count_value_1;
        }
        else if (count_value_1 == 0 && count_value_2 > 0) {
            str_err = "未登录词：" + word + " 正确切分：" + word_right + " 错误切分 " + word_out;
            vec_err.push_back(str_err);
            vec[2] += count_value_2;
        }
        else if (count_value_1 > 0 && count_value_2 > 0) {
            str_err = "交集型歧义：" + word + " 正确切分：" + word_right + " 错误切分：" + word_out;
            vec_err.push_back(str_err);
            vec[3] += count_value_3;
        }

        //计数器复位
        count_value_1 = 0;
        count_value_2 = 0;
    }

    vec[0] += count_value_3;
    return vec;
}


/*
    进行分词并统计分词
*/

//需要切分的最大句子数量
const int64_t MaxCount = 50000;

int main(int argc, char *argv[])
{
    int64_t cur_time = getCurrentTime();
    std::string strline_right; //输入语料，用作标准分词结果
    std::string strline_in; //去掉分词标记的语料（用作分词的输入）
    std::string strline_out_1; //隐马模型（二阶）分词完毕语料
    std::string strline_out_2; //隐马模型（三阶）分词完毕语料

    //输入文件
    ifstream f_in(argv[1]);
    if (!f_in) {
        fprintf(stdout, "open file error %s\n", argv[1]);
        return -1;
    }

    //输出文件
    ofstream f_out(argv[2]);
    if (!f_out) {
        fprintf(stdout, "open file erorr %s\n", argv[2]);
        return -1;
    }

    int64_t count = 0;      //句子编号
    int64_t count_1 = 0;    //隐马模型（二阶）切分完全正确句子总数
    int64_t count_2 = 0;    //隐马模型（三阶）切分完全正确句子总数
    int64_t count_right_all = 0;    //准确的切分总数

    //二阶
    int64_t count_out_1_all = 0;    //隐马模型切分总数
    int64_t count_out_1_right_all = 0;  //隐马模型切分正确总数
    int64_t count_out_1_fail_1_all = 0; //隐马模型切分(组合型歧义)
    int64_t count_out_1_fail_2_all = 0; //隐马模型（未登录词）
    int64_t count_out_1_fail_3_all = 0; //隐马模型（交集型歧义）

    //三阶
    int64_t count_out_2_all = 0;    //隐马模型切分总数
    int64_t count_out_2_right_all = 0;  //隐马模型正确切分总数
    int64_t count_out_2_fail_1_all = 0; //隐马模型（组合型歧义）
    int64_t count_out_2_fail_2_all = 0; //隐马模型（未登录词语）
    int64_t count_out_2_fail_3_all = 0; //隐马模型（交集型歧义）

    std::vector<std::string> vec_err_1; //隐马模型（二阶）切分错误的词
    std::vector<std::string> vec_err_2; //隐马模型（三阶）切分错误的词

    while (getline(f_in, strline_right, '\n') && count < MaxCount) {
        if (strline_right.length() > 1) {
            //去掉分词标记
            strline_in = strline_right;
            strline_in = replace_all(strline_in, "/", "");

            //隐马模型分词
            strline_out_1 = strline_right;
            istringstream strstm(strline_in);
            std::string sentence, result_1, result_2, line_out_1, line_out_2;
            while (strstm >> sentence) {
                //二阶切分
                result_1 = viterbiTwo(sentence);
                line_out_1 += result_1;

                //三阶切分
                result_2 = viterbiThree(sentence);
                line_out_2 += result_2;
            }

            strline_out_1 = line_out_1;
            strline_out_2 = line_out_2;
        }
    }

    //计算准确率和召回率
    double kk_1 = (double)count_out_1_right_all / count_out_1_all;  //隐马模型二阶准确率
    double kk_2 = (double)count_out_1_right_all / count_right_all;  //隐马模型二阶召回率
    double kk_3 = (double)count_out_2_right_all / count_out_2_all;  //隐马模型二阶准确率
    double kk_4 = (double)count_out_2_right_all / count_right_all;  //隐马模型三阶召回率

    return 0;
}
