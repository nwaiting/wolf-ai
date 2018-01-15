#coding=utf-8

"""
    Python命令行解析
    1、sys.argv
        sys.argv[1:]
    2、getopt
        options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['output=', 'verbose', 'version=',])
    3、argparse
        import argparse
        parser = argparse.ArgumentParser(description="some information here")
        args = parser.parse_args()
    4、docopt
        docopt就比较强大了，它是根据你自己写的help messages（文档描述），自动为你生成parser
    5、clize
        clize也比较强大，利用装饰器将函数转换成命令行解析器。github地址：https://github.com/epsy/clize
    6、Fire
        Google开源的库，Google出手，必是精品，强烈推荐
"""
