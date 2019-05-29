## cpp-笔记 - dllimport-dllexport区别
- **概述：**
>       在windows上，对于一个方法，一个是提供者，一个是使用者，二者之间的接口是头文件。
>       提供者应该申明为__declspec(dllexport)
>       在使用应该申明为__declspec(dllimport)
>       例如：
>            #ifndef DLL_H_
>            #define DLL_H_
>               #ifdef DLLProvider
>               #define DLL_EXPORT_IMPORT __declspec(dllexport)
>               #else
>               #define DLL_EXPORT_IMPORT __declspec(dllimport)
>               #endif
>
>               DLL_EXPORT_IMPORT int add(int ,int);
>            #endif
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
