import os

income_and_pay = []
sales_dict = dict()
sales_dict["a1"] = "生活费"
sales_dict["a2"] = "学习用品费"
sales_dict["a3"] = "日常开支"
sales_dict["b1"] = "学习用品"
sales_dict["b2"] = "电话费"
sales_dict["b3"] = "网费"
sales_dict["b4"] = "买衣服"

# 获取当前文件的目录，然后加上 income_pay.txt 文件名
current_file = os.path.realpath(__file__)
dir_name = os.path.dirname(current_file)
file_income_pay = os.path.join(dir_name, 'income_pay.txt')

"""
    记录的是每个日期下面有多少的明细
    比如：
        "2020-01":{
            "收入":{
                "生活费"：1000,
                "学习用品费": 100
            },
            "支出":{
                "电话费":100,
                "网费":10
            }
        }
"""
details = dict()


# 启动的时候，从文件中读取数据
# 将收入和支出都加载到details字典中
def read_file():
    f = open(file_income_pay, 'rb')
    for line in f.readlines():
        new_line = line.decode('utf-8')
        lines = new_line.split(',')
        dates = lines[1].split('-')
        key = "%s-%s" % (dates[0], dates[1])
        if key not in details:
            tmp = {"收入":{}, "支出":{}}
            details[key] = tmp

        detail_name = sales_dict.get(lines[0])
        # 以a开头的是收入
        if lines[0].startswith("a"):
            new_income = 0
            if detail_name in details[key]["收入"]:
                new_income = details[key]["收入"][detail_name] + float(lines[2])
            else:
                new_income = float(lines[2])
            details[key]["收入"][detail_name] = new_income
        # 以b开头的是支出
        elif lines[0].startswith('b'):
            new_pay = 0
            if detail_name in details[key]["支出"]:
                new_pay = details[key]["支出"][detail_name] + float(lines[2])
            else:
                new_pay = float(lines[2])
            details[key]["支出"][detail_name] = new_pay
        income_and_pay.append(new_line)
    f.close()


# 查询统计和详情
def search():
    while True:
        string = input("请输入对收支类别数据进行汇总的月份：")
        if string == '' or string is None:
            break
        string_split = string.split('-')
        print("%s年%s月收支类别数据的汇总" % (string_split[0], string_split[1]))
        if string not in details:
            print("没有记录")
            continue
        print("收入/支出 明细类别 金额")
        detail = details[string]
        for detail1,detail2 in detail.items():
            for detail21, detail22 in detail2.items():
                print("%s %s %s" % (detail1, detail21, detail22))
        input_pay = dict()
        input_pay['收入'] = 0
        input_pay['支出'] = 0
        for detail1,detail2 in detail.items():
            for detail21, detail22 in detail2.items():
                input_pay[detail1] += int(detail22)
        year_income = input_pay['收入']
        year_pay = input_pay['支出']
        print("%s年%s月总收入为：%s，总支出为：%s" % (string_split[0], string_split[1], year_income, year_pay))
        is_detail = input("是否输出该月的各笔明细（y为输出，其他为不输出）：")
        if is_detail == 'y':
            print("%s年%s月收支类别数据的明细" % (string_split[0], string_split[1]))
            print("类别 收入/支出 发生日期 金额 备注")
            for line in income_and_pay:
                line_split = line.split(',')
                line1 = line_split[0]
                line1 = sales_dict[line1]
                line2 = line_split[0]
                if line2.startswith('a'):
                    line2 = "收入"
                else:
                    line2 = "支出"
                line3 = line_split[1]
                line4 = line_split[2]
                line5 = line_split[3]
                print("%s %s %s %s %s" % (line1,line2,line3,line4,line5))
        string = input("是否输出每天的统计（y为输出，其他为不输出）：")
        days_dict = dict()
        if string == "y":
            for line in income_and_pay:
                line_split = line.split(',')
                s1 = line_split[0]
                day_key = line_split[1]
                if day_key in days_dict:
                    if s1.startswith('a'):
                        days_dict[day_key] += float(line_split[2])
                    else:
                        days_dict[day_key] -= float(line_split[2])
                else:
                    if s1.startswith('a'):
                        days_dict[day_key] = float(line_split[2])
                    else:
                        days_dict[day_key] = -float(line_split[2])
            for i,j in days_dict.items():
                print("%s 收支情况 %s" % (i,j))
# 先加载数据
read_file()
search()






