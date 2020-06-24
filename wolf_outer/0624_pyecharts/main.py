"""
    我大致给你说下思路  就是利用pandas将网页中的json数据获取然后进行重排版变成excel导出，
    然后利用百度的pyecharts这个包将这个excel里的数据进行可视化
"""

from lxml import etree
import json
import matplotlib.pyplot as plt
from pylab import mpl

# 图中显示乱码
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']

datas = []
file_list = ["疫情地图升级版/疫情地图.html", "疫情地图原版本/疫情地图.html"]
for file_item in file_list:
    with open(file_item, 'rb') as f:
        content = f.read()
        content = content.decode('utf-8')
        html = etree.HTML(content)
        item = html.xpath('//body/script/text()')
        item_str = item[0].strip('\r\n ')
        new_item_str = item_str[item_str.find('"series":')+len('"series":'):item_str.find('"legend"')].strip('\r\n ')
        rfind_index = new_item_str.rfind(',')
        new_item_str = new_item_str[:rfind_index]
        json_str = json.loads(new_item_str)
        datas.append(json_str)


for data in datas:
    for data_item in data:
        all_show_datas = []
        for item in data_item['data']:
            all_show_datas.append((item['name'], item['value']))
        sd = sorted(all_show_datas, key=lambda x: x[1], reverse=True)
        plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb', tick_label=[i[0] for i in sd])
        plt.title(data_item['name'])
        plt.savefig('{}.png'.format(data_item['name']))
        plt.show()




