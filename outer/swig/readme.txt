Python调用c++两种方法：

1、使用swig工具
	a、编写xxx.i接口文件，使用swig -python -c++ example.i 会生成example.py和example_wrap.cxx两个文件，两个封装文件
	b、使用setup.py进行编译和安装 build和install

2、自定义
	a、自定义Python的接口封装接口进行封装和初始化
	b、使用setup.py进行编译和安装

c/c++写Python扩展：
	https://www.ibm.com/developerworks/cn/linux/l-pythc/	用C语言扩展Python的功能
	https://docs.microsoft.com/zh-cn/visualstudio/python/cpp-and-python		创建适用于 Python 的 C++ 扩展
	http://zqpythonic.qiniucdn.com/data/20060106095504/index.html 	Python 与 C++ 的交互编程
	http://blog.csdn.net/yueguanghaidao/article/details/11538433	Python之美[从菜鸟到高手]--一步一步动手给Python写扩展(爱之初体验)
	http://usyiyi.cn/translate/python_352/extending/extending.html	Extending Python with C or C++
	http://blog.guoyb.com/2016/07/03/python-coroutine/	Python协程：从yield/send到async/await
	http://swig.org/papers/PyTutorial98/PyTutorial98.pdf	Interfacing C/C++ and Python with SWIG
