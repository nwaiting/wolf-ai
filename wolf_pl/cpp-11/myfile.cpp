#include <iostream>
#include <fstream>
#include <string>
using namespace std;

/*
    fseek定义：
        函数原型：int fseek(FILE *fp, LONG offset, int origin)
        参数含义：fp 文件指针 offset 相对于origin规定的偏移位置量 origin 指针移动的起始位置，可设置为以下三种情况： SEEK_SET 文件开始位置 SEEK_CUR 文件当前位置 SEEK_END 文件结束位置

    tellg()定义：
        tellg() 用于在输入流中获取位置
        streampos tellg();//返回一个整型数，代表读指针的位置
        example:streampos pos = tellg();//将tellg()返回的指针位置赋值给pos
    seekg()定义：
        seekg()用于设置在输入流中的位置
        istream& seekg(streampos pos);//将读指针设置到pos位置
        istream& seekg(streamoff off, ios_base::seekdir way);//将读指针设置为way+off，其中off 代表偏移值，而way代表基址

        in.seekg(0,ios::end);   //基地址为文件结束处，偏移地址为0，于是指针定位在文件结束处
        in.seekg(-sp/3,ios::end); //基地址为文件末，偏移地址为负，于是向前移动sp/3个字节
        in.seekg(0,ios::beg);   //基地址为文件头，偏移量为0，于是定位在文件头
        curpos = in.tellg();  //获取当前位置

        获取文件长度：
            ifs.seekg(std::streamoff(0), std::ios::end);
            return ifs.tellg();
*/

void func1()
{
    ifstream ifs("ReadMe.txt");
    streampos pos = ifs.tellg();
    ifs.seekg(streamoff(0), ios::end);
    cout << "file length " << ifs.tellg() << endl;

    ifs.seekg(pos);
    ifs.seekg(streampos(1000), ios::end);
    cout << "file have " << ifs.tellg() << endl;
}


int main()
{
    func1();

    cin.get();
    return 0;
}
