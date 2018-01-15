Python调用c++两种方法：

1、使用swig工具
	a、编写xxx.i接口文件，使用swig -python -c++ example.i 会生成example.py和example_wrap.cxx两个文件，两个封装文件
	b、使用setup.py进行编译和安装 build和install

2、自定义
	a、自定义Python的接口封装接口进行封装和初始化
	b、使用setup.py进行编译和安装