
"""
命令启动unittest：
    指定测试模块
        python -m unittest discover -s tests        # 测试tests目录下的所有模块
    指定测试类
        python -m unittest tests.test_word
        python -m unittest tests/test_word.py       #两种方法相同，测试某一个python文件的测试用例

    指定测试方法
        python -m unittest test_module.TestClass.test_method    (测试好像不可用)
    指定测试文件路径（仅 Python 3）
        python -m unittest tests/test_something.py
"""
