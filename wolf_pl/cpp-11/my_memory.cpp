#include <iostream.h>

int func1() {
    /*
    * memset()和fill()的区别：
        memset():是将s所指向的某一块内存的每个字节的内容全部设置为ch指定的ASCII值
        fill():是把那一块单元赋成指定的值，可以是任何值
    区别：
        int array[5] = {1,4,3,5,2}; //默认打印结果 1 4 3 5 2
        memset(array,1,5*sizeof(int)); //输出结果 16843009 16843009 16843009 16843009 16843009
        因为是将每个字节赋值
        因为memset是以字节为单位就是对array指向的内存的5个字节进行赋值，每个都用ASCII为1的字符去填充，转为二进制后，1就是00000001,占一个字节。一个INT元素是4字节，合一起就是00000001000000010000000100000001，就等于16843009，就完成了对一个INT元素的赋值了。　　
        所以用memset对非字符型数组赋初值是不可取的！
    */
}

int main(int argc, char const *argv[]) {
    /* code */
    return 0;
}
