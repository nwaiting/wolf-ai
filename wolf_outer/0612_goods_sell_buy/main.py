# -*- encoding: utf-8 -*-"

"""
    @File    :   main.py
    @Time    :   2020/06/12 20:30:00
    @Author  :   xxx
    @Version :   1.0
    @Contact :   xxx@gmail.com
"""

import os


goods_buy_sell_list = []
goods_buy_sell_dict = {}

type_goods_dict = {
    "01": "电视机",
    "02": "洗衣机",
    "03": "电冰箱",
    "04": "台式电脑",
    "05": "笔记本电脑",
    "06": "平板电脑",
    "07": "4G手机",
    "08": "5G手机",
    "09": "针式打印机",
    "10": "激光打印机"
}


def save_data(file_name, data):
    # 保存数据到文件中
    with open(file_name, 'ab') as f:
        f.write(("{}\n".format(data)).encode('utf-8'))


def load_data(file_name):
    # 从文件中加载数据
    if not os.path.exists(file_name):
        return
    with open(file_name, 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip('\r\n ')
            goods_buy_sell_list.append(line)

            line_items = line.split(',')
            date_items = line_items[1].split('-')
            dict_key = "{}-{}".format(date_items[0], date_items[1])
            if dict_key not in goods_buy_sell_dict:
                goods_buy_sell_dict[dict_key] = {"进货": {}, "销售": {}}
            goods_name = type_goods_dict.get(line_items[0][1:])
            if line_items[0].startswith("A"):
                goods_buy_sell_dict[dict_key]["进货"][goods_name] = goods_buy_sell_dict[dict_key]["进货"].get(goods_name,0) + int(line_items[2])
            elif line_items[0].startswith('B'):
                goods_buy_sell_dict[dict_key]["销售"][goods_name] = goods_buy_sell_dict[dict_key]["销售"].get(goods_name,0) + int(line_items[2])


def main():
    save_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buy_sell.data')
    # 启动时候 加载数据
    load_data(save_file_name)
    while True:
        print("是否录入数据，还是查询信息（输入y进入录入数据程序）：", end='')
        input_str = input()
        if input_str.lower() == 'y':
            # 录入数据
            print("进入录入数据程序，数据格式为(类别编码、发生日期、 数量、单价、 经办人信息)，输入no，录入数据结束")
            while True:
                s = input("输入进销明细: ")
                s = s.strip('\r\n ')
                if s == 'no':
                    break
                s_items = s.split(',')
                if len(s_items) != 5:
                    print("输入格式有误，请重新录入")
                    continue
                goods_buy_sell_list.append(s)
                date_items = s_items[1].split('-')
                if len(date_items) != 3:
                    print("日期格式有误，如：2020-01-01，请重新输入")
                    continue

                dict_key = "{}-{}".format(date_items[0], date_items[1])
                if dict_key not in goods_buy_sell_dict:
                    goods_buy_sell_dict[dict_key] = {"进货": {}, "销售": {}}
                goods_name = type_goods_dict.get(s_items[0][1:])
                print("goods_buy_sell_dict={}".format(goods_buy_sell_dict))
                if s_items[0].startswith("A"):
                    goods_buy_sell_dict[dict_key]["进货"][goods_name] = goods_buy_sell_dict[dict_key]["进货"].get(goods_name, 0) + int(s_items[2])
                elif s_items[0].startswith('B'):
                    goods_buy_sell_dict[dict_key]["销售"][goods_name] = goods_buy_sell_dict[dict_key]["销售"].get(goods_name, 0) + int(s_items[2])
                else:
                    print("类别编码有误，请重新录入")
                    continue
                save_data(save_file_name, s)

        else:
            # 查询信息
            print("进入数据统计程序，输入no，统计程序结束")
            while True:
                s = input("请输入年和月（格式： yyyy-mm）: ")
                s = s.strip('\r\n ')
                if s == 'no':
                    break
                s_items = s.split('-')
                if len(s_items) != 2:
                    print("输入数据有误，请重新输入")
                    continue
                if s not in goods_buy_sell_dict:
                    print("当前日期没有记录，请重新输入")
                    continue
                print("{}年{}月商品进销数据汇总".format(s_items[0], s_items[1]))
                print("进货/销售 商品名 数量")
                current_goods = goods_buy_sell_dict.get(s)
                for k,v in current_goods.items():
                    for kk,vv in v.items():
                        print("{} {} {}".format(k, kk, v))
                ss = input("是否输出该月的各笔明细（y 为输出，其他为不输出）：")
                ss = ss.strip('\r\n ')
                if ss.lower() == 'y':
                    print("{}年{}月商品进销数据的明细：".format(s_items[0], s_items[1]))
                    print("类别编码 商品名称 发生日期 数量 经办人")
                    for s_item_inner in goods_buy_sell_list:
                        s_items_inner = s_item_inner.split(',')
                        if s_items_inner[1].startswith(s):
                            print("{} {} {} {} {}".format(s_items_inner[0],type_goods_dict[s_items_inner[0][1:]],
                                                          s_items_inner[1],s_items_inner[2],s_items_inner[4]))


if __name__ == '__main__':
    main()






