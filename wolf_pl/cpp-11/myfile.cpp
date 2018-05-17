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

/*
    #include <fstream>
    ofstream         //文件写操作 内存写入存储设备
    ifstream         //文件读操作，存储设备读区到内存中
    fstream          //读写操作，对打开的文件可进行读写操作

    ofstream out("...", ios::out);
    ifstream in("...", ios::in);
    fstream foi("...", ios::in|ios::out);
    fstream file1;
        file1.open("c:\\config.sys",ios::binary|ios::in,0);
        file1.open("c:\\config.sys"); <=> file1.open("c:\\config.sys",ios::in|ios::out,0);
    ios::in	    为输入(读)而打开文件，只可以对ifstream和fstream设定
    ios::out	为输出(写)而打开文件，只可以对ofstream和fstream设定
    ios::ate	初始位置：文件尾
    ios::app	所有输出附加在文件末尾
    ios::trunc	如果文件已存在则先删除该文件
    ios::binary	二进制方式
*/
void func2()
{

}

int main()
{
    func1();

    cin.get();
    return 0;
}
