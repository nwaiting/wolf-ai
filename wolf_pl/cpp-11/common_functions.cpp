#include <iostream>

/*
sprintf_s、_snprintf和_snprintf_s区别：
    int sprintf_s(char *buffer,size_t sizeOfBuffer,const char *format [,argument] ... );
    int _snprintf(char *buffer,size_t count,const char *format [,argument] ... );
    int _snprintf_s(char *buffer,size_t sizeOfBuffer,size_t count,const char *format [,argument] ... );

    sprintf_s：在缓冲区不够大时会失败，失败时缓冲区中是一个空字符串。
    _snprintf：不会失败，但是必须注意,如果缓冲区不够大，缓冲区的内容将不是null-teminate的，必须自己注意字符串的结束。
    _snprintf_s：结合了2者的优点，只要count参数设置合理(如果希望缓冲区被尽量利用，可以把count参数置为_TRUNCATE，这样的情况下，实际上效果相当于是将count设置为sizeOfBuffer-1)，函数就不会因缓冲区不够而失败。
    所以，在C++中使用这类函数，还是应该尽可能的使用_snprintf_s才好。
*/
void func1()
{

}

int main()
{
    func1();

    std::cin.get();
    return 0;
}
