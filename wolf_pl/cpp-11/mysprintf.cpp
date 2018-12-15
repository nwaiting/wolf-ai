#include <iostream>

/*
    比较常用格式化函数的区别：
        #define _TRUNCATE -1
        #define vsnprintf_s(destStr,destSize, maxsize,format,ap)  vsnprintf(destStr,maxsize,format,ap)
        #define sprintf_s(destStr, destSize, format, ...)	sprintf(destStr, format, __VA_ARGS__)
        #define _vsnwprintf_s(wcs, wcsSize, maxlen, format, args)	vswprintf(wcs, maxlen, format, args)
        #define swprintf_s(destStr, destSize, format, ...)	swprintf(destStr, destSize, format, __VA_ARGS__)
        #define _snprintf_s snprintf
        #define vsprintf_s(destStr,destSize,format, ap)			vsprintf(destStr,format, ap)
        #define strcpy_s(destStr, maxsize, srcStr) strncpy(destStr, srcStr, maxsize)
        #define strcat_s(destStr, maxsize, srcStr)	strncat(destStr, srcStr, maxsize)
        #define localtime_s(ptm, timeep)	localtime_r(timeep, ptm)

*/

void  func1() {

}

int main()
{
    func1();

    std::cin.get();
    return 0;
}
