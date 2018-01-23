#codind=utf-8

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#文档较多
from pdfminer

#文档较少
import PyPDF2

def main():
    with open('outer/parse_pdf/1.pdf', 'rb') as fpdf:
        pr = PyPDF2.PdfFileReader(fpdf)
        print(pr.getNumPages())
        page_obj = pr.getPage(3)
        print(page_obj)
        print('contents ', page_obj.extractText())
        doc_info = pr.getDocumentInfo()
        print(doc_info.author)
        print(doc_info.creator)
        print(doc_info.producer)
        print(doc_info.title)
        print(doc_info.subject)
        print(doc_info.subject_raw)
        print('text ', doc_info.getText('/Subject'))
        print('fields ', pr.getFields())
        print('xmpMetadata ', pr.getXmpMetadata())

if __name__ == '__main__':
    main()
