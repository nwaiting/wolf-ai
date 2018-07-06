#include <iostream>
#include <string>
#include <stdint.h>
#include <fstream>
#include <map>
#include <vector>
#include <sstream>
using namespace std;

/*
    hmm的二阶和三阶的分词比较
    参考：https://blog.csdn.net/u010189459/article/details/38337031
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
    std::vector<ifstream> file_vec;
    file_vec.push_back(file_one);
    file_vec.push_back(file_two);
    for (auto& it:file_vec) {
        while (getline(it, line)) {
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
const double SMO_VALUE = 1.0;
/*
    模型训练，将频数转为频率（加1平滑）
*/
void turingAdd()
{

}

int main()
{
    return 0;
}
