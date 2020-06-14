import os

# 获取当前文件的目录，然后加上 income_pay.txt 文件名
current_file = os.path.realpath(__file__)
dir_name = os.path.dirname(current_file)
file_name = os.path.join(dir_name, 'a.txt')


# 录入程序，格式 a1,2020-01-01,100,生活费
def input_():
    print("类别编码和类别名称的对应关系如下：")
    print("收入类：a1-生活费，a2-学习用品费，a3-日常开支")
    print("支出类：b1-学习用品，b2-电话费，b3-网费，b4-买衣服")
    print("请逐笔输入类别编码、发生日期、金额、备注(各数据用英文逗号分隔，直接输入回车表示输入结束)：")
    while True:
        s1 = input("输入进销明细: ")
        if not s1:
            break
        f = open(file_name, 'ab')
        s2 = "%s\n" % s1
        s3 = s2.encode('utf-8')
        f.write(s3)
        f.close()


# 从文件中读取，保存在a_list中
a_list = []
def load_file():
    f = open(file_name, 'rb')
    for s2 in f.readlines():
        s22 = s2.decode('utf-8')
        a_list.append(s22)
    f.close()


# 查询统计和详情
def check():
    s1 = input("请输入对收支类别数据进行汇总的月份：")
    if s1 == '' or s1 is None:
        return
    s11 = s1.split('-')
    print("%s年%s月收支类别数据的汇总" % (s11[0], s11[1]))
    ss = True
    # 找到这个日期的记录
    for s2 in a_list:
        sf = s2.find(s1)
        if sf == -1:
            continue
        else:
            ss = False
    if ss == True:
        print("没有数据")
        return

    print("收入/支出 明细类别 金额")
    # 保存收入的记录
    s22_income = dict()
    # 保存支出的记录
    s22_pay = dict()
    for s2 in a_list:
        sf = s2.find(s1)
        if sf != -1:
            s22 = s2.split(',')
            if s22[0].startswith('a'):
                if s22[0] not in s22_income:
                    s22_income[s22[0]] = float(s22[2])
                else:
                    s22_income[s22[0]] += float(s22[2])
            else:
                if s22[0] not in s22_pay:
                    s22_pay[s22[0]] = float(s22[2])
                else:
                    s22_pay[s22[0]] += float(s22[2])
    income1 = 0
    pay1 = 0
    # 输出收入的统计记录
    if s22_income:
        for s4,s5 in s22_income.items():
            m1 = s4
            if m1.startswith("a"):
                m1 = "收入"
            else:
                m1 = "支出"
            m2 = s4
            if s4 == "a1":
                m2 = "生活费"
            elif s4 == 'a2':
                m2 = "学习用品费"
            elif s4 == 'a3':
                m2 = "日常开支"
            m3 = s5
            income1 += float(s5)
            print("%s %s %s " % (m1, m2, m3))
    if s22_pay:
        # 输出支出的统计记录
        for s4,s5 in s22_pay.items():
            m1 = s4
            if m1.startswith("b"):
                m1 = "收入"
            else:
                m1 = "支出"
            m2 = s4
            if s4 == "b1":
                m2 = "学习用品"
            elif s4 == 'b2':
                m2 = "电话费"
            elif s4 == 'b3':
                m2 = "网费"
            elif s4 == 'b4':
                m2 = "买衣服"
            m3 = s5
            pay1 += float(s5)
            print("%s %s %s " % (m1, m2, m3))

    print("%s年%s月总收入为：%s，总支出为：%s" % (s11[0], s11[1], income1, pay1))
    ts = input("是否输出该月的各笔明细（y为输出，其他为不输出）：")
    if ts == 'y':
        # 输出每条记录
        print("%s年%s月收支类别数据的明细" % (s11[0], s11[1]))
        print("类别 收入/支出 发生日期 金额 备注")
        for ssss in a_list:
            ssss_s = ssss.split(',')
            sss = ssss_s[0]
            m1 = sss
            if sss == "b1":
                m1 = "学习用品"
            elif sss == 'b2':
                m1 = "电话费"
            elif sss == 'b3':
                m1 = "网费"
            elif sss == 'b4':
                m1 = "买衣服"
            elif sss == "a1":
                m1 = "生活费"
            elif sss == 'a2':
                m1 = "学习用品费"
            elif sss == 'a3':
                m1 = "日常开支"
            m2 = ssss_s[0]
            if m2.startswith('a'):
                m2 = "收入"
            else:
                m2 = "支出"
            m3 = ssss_s[1]
            m4 = ssss_s[2]
            m5 = ssss_s[3]
            print("%s %s %s %s %s" % (m1,m2,m3,m4,m5))
    ts = input("是否输出每个月的统计（y为输出，其他为不输出）：")
    if ts == 'y':
        months = dict()
        # 保存每个月的记录 {"2020-01":100,"2020-02":-100}
        for ssss in a_list:
            ssss_s = ssss.split(',')
            s1 = ssss_s[0]
            s2 = ssss_s[1].split('-')
            s2_day = "%s-%s" % (s2[0], s2[1])
            if s1.startswith('a'):
                months[s2_day] = months.get(s2_day, 0) + float(ssss_s[2])
            else:
                months[s2_day] = months.get(s2_day, 0) - float(ssss_s[2])
        for m,n in months.items():
            print("%s 统计 %s" % (m, n))


input_()
load_file()
check()






