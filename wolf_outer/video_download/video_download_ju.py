#coding=utf-8

import requests
import os
import time
import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

sources = """
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="615">/video/play/67/615</span><span class="video-catalog-left">(1) 第1课（上）微积分</span><span>(02:03:32)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="1316">/video/play/67/1316</span><span class="video-catalog-left">(2) 第1课（下）概率论</span><span>(02:04:46)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="617">/video/play/67/617</span><span class="video-catalog-left">(3) 第2课（上） 线性代数</span><span>(03:14:10)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="1317">/video/play/67/1317</span><span class="video-catalog-left">(4) 第2课（下） 凸优化</span><span>(01:38:30)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="620">/video/play/67/620</span><span class="video-catalog-left">(5) 第3课 回归问题与应用</span><span>(02:16:48)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="625">/video/play/67/625</span><span class="video-catalog-left">(6) 第4课 决策树、随机森林、GBDT</span><span>(01:50:09)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="659">/video/play/67/659</span><span class="video-catalog-left">(7) 第5课 SVM</span><span>(01:53:17)</span></a></li> http://v3.julyedu.com/video/67/659/3f8cb40619.m3u8  http://v3.julyedu.com/video/67/659/3f8cb40619-00001.ts
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="641">/video/play/67/641</span><span class="video-catalog-left">(8) 第6课 最大熵与EM算法（上）</span><span>(02:55:25)</span></a></li> http://v3.julyedu.com/video/67/641/ee810d8f85.m3u8
    <li class="active"><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="1358">/video/play/67/1358</span><span class="video-catalog-left">(9) 第6课 最大熵与EM算法（下）</span><span>(02:07:04)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="639">/video/play/67/639</span><span class="video-catalog-left">(10) 第7课 机器学习中的特征工程处理</span><span>(02:18:09)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="666">/video/play/67/666</span><span class="video-catalog-left">(11) 第8课 多算法组合与模型最优化</span><span>(02:08:40)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="676">/video/play/67/676</span><span class="video-catalog-left">(12) 第9课 sklearn与机器学习实战</span><span>(01:52:04)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="677">/video/play/67/677</span><span class="video-catalog-left">(13) 第10课 高级工具xgboost/lightGBM与建模实战</span><span>(02:12:19)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="682">/video/play/67/682</span><span class="video-catalog-left">(14) 第11课 用户画像与推荐系统</span><span>(01:54:57)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="685">/video/play/67/685</span><span class="video-catalog-left">(15) 第12课 聚类</span><span>(01:57:19)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="692">/video/play/67/692</span><span class="video-catalog-left">(16) 第13课 聚类与推荐系统实战</span><span>(01:42:14)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="695">/video/play/67/695</span><span class="video-catalog-left">(17) 第14课 贝叶斯网络</span><span>(01:50:42)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="696">/video/play/67/696</span><span class="video-catalog-left">(18) 第15课 隐马尔科夫模型HMM</span><span>(01:50:27)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="697">/video/play/67/697</span><span class="video-catalog-left">(19) 第16课 主题模型</span><span>(02:01:10)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="702">/video/play/67/702</span><span class="video-catalog-left">(20) 第17课 神经网络初步</span><span>(01:53:25)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="706">/video/play/67/706</span><span class="video-catalog-left">(21) 第18课 卷积神经网络与计算机视觉</span><span>(02:10:04)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="708">/video/play/67/708</span><span class="video-catalog-left">(22) 第19课 循环神经网络与自然语言处理</span><span>(01:48:31)</span></a></li>
    <li class=""><a class="videoLink" href="javascript:" ><span class="href" data-cid="67" data-lesid="714">/video/play/67/714</span><span class="video-catalog-left">(23) 第20课 深度学习实践</span><span>(01:46:37)</span></a></li>
    """

sources_urls = ["第1课（上）微积分,/67/615/585b7925ff.m3u8",
            "第1课（下）概率论,/67/1316/8fc04380c4.m3u8",
            "第2课（上） 线性代数,/67/617/689129cdec.m3u8",
            "第2课（下） 凸优化,/67/1317/65fed5fa90.m3u8",
            "第3课 回归问题与应用,/67/620/f45c5d2d88.m3u8",
            "第4课 决策树、随机森林、GBDT,/67/625/3738907e1b.m3u8",
            "第5课 SVM,/67/659/3f8cb40619.m3u8",
            "第6课 最大熵与EM算法（上）,/67/641/ee810d8f85.m3u8",
            "第6课 最大熵与EM算法（下）,/67/1358/35d55e1522.m3u8",
            "第7课 机器学习中的特征工程处理,/67/639/b708635864.m3u8",
            "第8课 多算法组合与模型最优化,/67/666/299d366254.m3u8",
            "第9课 sklearn与机器学习实战,/67/676/d524c0c2e8.m3u8",
            "第10课 高级工具xgboost/lightGBM与建模实战,/67/677/2dc0222e0b.m3u8",
            "第11课 用户画像与推荐系统,/67/682/cc4990c83f.m3u8",
            "第12课 聚类,/67/685/4096fbe221.m3u8",
            "第13课 聚类与推荐系统实战,/67/692/f9f91cd421.m3u8",
            "第14课 贝叶斯网络,/67/695/5dfe57e51f.m3u8",
            "第15课 隐马尔科夫模型HMM,/67/696/89bab3178f.m3u8",
            "第16课 主题模型,/67/697/357374ff1d.m3u8",
            "第17课 神经网络初步,/67/702/1ce717ac40.m3u8",
            "第18课 卷积神经网络与计算机视觉,/67/706/44462aa908.m3u8",
            "第19课 循环神经网络与自然语言处理,/67/708/cf9fd481fc.m3u8",
            "第20课 深度学习实践,/67/714/a90b06c249.m3u8"
            ]


def dts(url, save_file):
    chunk_size = 4096
    res = requests.get(url)
    with open(save_file, 'wb') as f:
        for chunk in res.iter_content(chunk_size):
            f.write(chunk)

def main():
    url_pre = "http://v3.julyedu.com/video"
    for line in sources_urls:
        items = line.strip().split(',')
        if len(items) == 2:
            zh_dir_path = items[0].decode('utf-8').encode('gbk')
            if not os.path.exists(zh_dir_path):
                try:
                    os.mkdir(zh_dir_path)
                except Exception as e:
                    print("error mkdir {0}".format(e))
            m3u8_url = url_pre + items[1]
            print(os.path.basename(items[1]))
            print(os.path.dirname(items[1]))
            res = requests.get(m3u8_url)

            with open(os.path.join(zh_dir_path,"m3u8.m3u8"), 'w') as f:
                f.write(res.text)

            for res_line in res.text.split('\n'):
                if res_line.startswith('#'):
                    continue
                print(res_line)
                time.sleep(1)
                res_line = res_line.strip('\r\n ')
                ts_url = url_pre + os.path.dirname(items[1]) + '/' + res_line
                file_name = os.path.join(items[0].decode('utf-8').encode('utf-8'),res_line)
                print(ts_url, file_name)
                dts(ts_url, file_name)

if __name__ == '__main__':
    main()
