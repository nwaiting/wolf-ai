import os

current_file = os.path.realpath(__file__)
dir_name = os.path.dirname(current_file)
file_income_pay = os.path.join(dir_name, 'income_pay.txt')


def income():
    print("类别编码和类别名称的对应关系如下：")
    print("收入类：a1-生活费，a2-学习用品费，a3-日常开支")
    print("支出类：b1-学习用品，b2-电话费，b3-网费，b4-买衣服")
    print("请逐笔输入类别编码、发生日期、金额、备注(各数据用英文逗号分隔，直接输入回车表示输入结束)：")
    while True:
        details_string = input("输入进销明细: ")
        if not details_string:
            break
        f = open(file_income_pay, 'ab')
        save_str = "%s\n" % details_string
        save_str_str = save_str.encode('utf-8')
        f.write(save_str_str)
        f.close()

income()






