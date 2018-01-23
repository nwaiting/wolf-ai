#coding=utf-8
from distutils.core import setup, Extension


example_module = Extension('_example',sources=['example.cpp'], )

setup (name = 'example',
            version = '0.1',
            author      = "SWIG Docs",
            description = """Simple swig example from docs""",
            ext_modules = [example_module],
            py_modules = ["example"], )

"""
foo_module = Extension('_foo',
                        sources=['foo.i' , 'foo.cpp'],
                        swig_opts=['-c++'],
                        library_dirs=['/usr/lib64'],
                        libraries=['ex'],
                        include_dirs = ['/usr/include'],
                        extra_compile_args = ['-DNDEBUG', '-DUNIX', '-D__UNIX',  '-m64', '-fPIC', '-O2', '-w', '-fmessage-length=0'])
'-Xlinker -export-dynamic'

"""
