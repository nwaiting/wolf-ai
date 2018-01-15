# -*- coding: utf-8 -*-
'''
Created on Apr 5, 2012

@author: balenocui

跨平台扩展构建模块,构建生成old key的C扩展
使用方式：
1、python setup.py build
2、python setup.py install
'''

from distutils.core import setup, Extension
import sys
macros = [] if sys.platform != "win32" else [('WIN32',None)]
ppkey_mod = Extension('pplive_example', sources = ['pplive_example.c','make_example.c'],define_macros=macros)
setup(name = 'pplive_example',
    version = '1.0',
    description = 'pplive_example extension module',
    ext_modules = [ppkey_mod])
