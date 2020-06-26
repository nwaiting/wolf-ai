"""
    我大致给你说下思路  就是利用pandas将网页中的json数据获取然后进行重排版变成excel导出，
    然后利用百度的pyecharts这个包将这个excel里的数据进行可视化

    pip install pyecharts==0.1.9.4
"""

from lxml import etree
import json
import matplotlib.pyplot as plt
from pylab import mpl
from pyecharts import Map

# 图中显示乱码
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 柱形图表中最多显示多少个数据
show_lines = 100


datas = []
new_datas = []


def main():
    with open("疫情地图原版本/疫情地图.html", 'rb') as f:
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

    with open("疫情地图升级版/疫情地图.html", 'rb') as f:
        content = f.read()
        content = content.decode('utf-8')
        html = etree.HTML(content)
        item = html.xpath('//body/script/text()')
        item_str = item[0].strip('\r\n ')
        new_item_str = item_str[item_str.find('"series":')+len('"series":'):item_str.find('"legend"')].strip('\r\n ')
        rfind_index = new_item_str.rfind(',')
        new_item_str = new_item_str[:rfind_index]
        json_str = json.loads(new_item_str)
        new_datas.append(json_str)

    for data in datas:
        for data_item in data:
            all_show_datas = []
            for item in data_item['data']:
                all_show_datas.append((item['name'], item['value']))
            old_sd = sorted(all_show_datas, key=lambda x: x[1], reverse=True)
            sd = old_sd[:show_lines]
            plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb', tick_label=[i[0] for i in sd])
            plt.title(data_item['name'])
            plt.savefig('{}.png'.format(data_item['name']))
            plt.show()

            d1 = [i[0] for i in sd]
            d2 = [i[1] for i in sd]
            char_map = Map('{}'.format(data_item['name']),'data from network', width=1500, height=800, title_pos='center')
            char_map.add("", d1, d2, maptype='china', is_visualmap=True, visual_text_color='#000', is_label_show=True)
            char_map.render('{}.html'.format(data_item['name']))

    for data in new_datas:
        for data_item in data:
            all_show_datas = []
            for item in data_item['data']:
                all_show_datas.append((item['name'], item['value']))
            old_sd = sorted(all_show_datas, key=lambda x: x[1], reverse=True)
            sd = old_sd[:show_lines]
            plt.bar(range(len(sd)), [i[1] for i in sd], color='rgb', tick_label=[i[0] for i in sd])
            plt.title(data_item['name'])
            plt.savefig('{}.png'.format(data_item['name']))
            plt.show()

            d1 = [i[0] for i in sd]
            d2 = [i[1] for i in sd]
            char_map = Map('{}'.format(data_item['name']),'data from network', width=1500, height=800, title_pos='center')
            char_map.add("", d1, d2, maptype='china', is_visualmap=True, visual_text_color='#000', is_label_show=True)
            char_map.render('{}.html'.format(data_item['name']))


main()



