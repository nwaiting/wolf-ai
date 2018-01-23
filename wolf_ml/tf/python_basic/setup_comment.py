#coding=utf-8

"""
setup.py其实是python工具包distutils的配置文件，setuptools就是基于distutils来做的
在setup.py中通过setup函数来配置打包信息。首先要引入setuptools的函数setup。setuptools的setup其实就是distutils的setup函数，

setup(...)
    --name 包名称，pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    --version (-V) 包版本
    --author 程序的作者
    --author_email 程序的作者的邮箱地址
    --maintainer 维护者
    --maintainer_email 维护者的邮箱地址
    --url 程序的官网地址
    --license 程序的授权信息
    --description 程序的简单描述
    --long_description 程序的详细描述
    --platforms 程序适用的软件平台列表
    --classifiers 程序的所属分类列表
    --keywords 程序的关键字列表
    --packages 需要处理的包目录（包含__init__.py的文件夹） 打包的文件
    --py_modules 需要打包的python文件列表
    --download_url 程序的下载地址
    --cmdclass
    --data_files 打包时需要打包的数据文件，如图片，配置文件等
    --scripts 安装时需要执行的脚步列表
    --package_dir 告诉setuptools哪些目录下的文件被映射到哪个源码包。一个例子：package_dir = {'': 'lib'}，表示“root package”中的模块都在lib 目录中。
    --requires 定义依赖哪些模块
        需要安装的依赖 install_requires=['redis>=2.10.5','setuptools>=16.0',],
    --provides 定义可以为哪些模块提供依赖
    --find_packages() 对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有 __init__.py的包。
        其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有aaa.txt文件和data数据文件夹。另外，也可以排除一些特定的包
        find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

        packages 这里要用到setuptools的另一个函数find_packages，顾名思义，find_packages用来将指定目录下的文件打包。

        修改find_packages函数中参数为'src'，同时增加package_dir参数：
        packages=find_packages('src'),
        package_dir = {'':'src'}
        这样告诉setuptools在src目录下找包，而不是原来默认的工程根目录

    --zip_safe 默认是False，这样在每次生成egg包时都会检查项目文件的内容，确保无误。
    --install_requires = ["requests"] 需要安装的依赖包
    --entry_points 动态发现服务和插件，下列entry_points中： console_scripts 指明了命令行工具的名称；在“redis_run = RedisRun.redis_run:main”中，等号前面指明了工具包的名称，等号后面的内容指明了程序的入口地址。
        entry_points={'console_scripts': ['redis_run = RedisRun.redis_run:main',]}
"""

"""
    egg的卸载：
        egg文件就是一个zip压缩包
        以python2.6版本为例，egg文件一般安装在/usr/local/lib/python2.6/dist-packages/目录下，该目录下还有一个easy-install.pth文件，用于存放安装的egg信息
        卸载egg文件很简单，首先将包含此egg的行从easy-install.pth中删除，然后删除egg文件夹即可
"""

"""
setuptools和distutils区别：
    distutils是Python标准模块，setuptools是第三方模块
    setuptools 是对 distutils 的增强, 尤其是引入了包依赖管理。
    setuptools可以为Python包创建 egg文件， Python 与 egg 文件的关系
"""

"""
安装第三方的模块：
    一般我们在python项目中，需要引入第三方模块，有两种方式（以yaml模块为例）：一种是使用python setup.py install或者easy_install yaml或者pip install yaml将yaml模块
    安装到python缺省的第三方库安装路径lib/site-packages目录中。一种是使用python setup.py build生成模块的构建文件，然后将build目录下生成的模块目录拷贝到项目目录中，
    这样将项目部署其他机器上时，就不用再去安装环境了
"""

from setuptools import setup, find_packages

from distutils.core import setup, Extension
import sys
macros = [] if sys.platform != "win32" else [('WIN32',None)]
ppkey_mod = Extension('pplive_example', sources = ['pplive_example.c','make_example.c'],define_macros=macros)
setup(name = 'pplive_example',
    version = '1.0',
    description = 'pplive_example extension module',
    ext_modules = [ppkey_mod])

setup()
