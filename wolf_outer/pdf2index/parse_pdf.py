#coding=utf-8

import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter, PDFConverter
from pdfminer.layout import *

def parse_pdf(filename):
    parsepdf = PDFParser(open(filename, 'rb'))
    doc = PDFDocument()
    parsepdf.set_document(doc=doc)
    doc.set_parser(parsepdf)
    doc.initialize()
    if not doc.is_extractable:
        print('PDFTextExtractionNotAllowed')
        return
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

        """
        outfp=open(os.path.join(os.path.dirname(filename), 'figure1.pdf'),'wb')
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        """

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            num_page += 1  # 页面增一
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                # 图片
                if isinstance(x,LTImage):
                    num_image += 1
                # 曲线
                if isinstance(x,LTCurve):
                    num_curve += 1
                # figure对象
                if isinstance(x,LTFigure):
                    num_figure += 1

                if num_page == 3 and isinstance(x,LTFigure):
                    print("{}".format(x))
                    print("{}".format(x._objs))
                    print('{}'.format(dir(x)))
                    print('{}'.format(x.bbox))

                    with open(os.path.join(os.path.dirname(filename), 'figure1.pdf'), 'wb') as fd:
                        fd.write(('{}'.format(x.bbox)).encode())

                # 获取文本内容
                if isinstance(x, LTTextBoxHorizontal):
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                    """
                    with open(r'test.txt', 'a') as f:
                        results = x.get_text()
                        f.write(results + '\n')
                    """
        print('object num:\n page: {0} picture: {1} curve: {2} text: {3}, figure: {4}'.format(num_page, num_image, num_curve, num_TextBoxHorizontal, num_figure))

if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(os.path.relpath(__file__)), '1.pdf')
    parse_pdf(file_name)
