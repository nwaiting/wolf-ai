#coding=utf-8

"""
    for (var t = "",
    a = 0; a < e.length; a++) {
        var i = e.charCodeAt(a).toString(16);
        2 == i.length ? t += "n" + i: t += i
    }
    return t

好吃吗
597d54035417
啊
554a
"""

import binascii
t = ''
for i in u'啊':
    j = binascii.b2a_hex(i.encode('utf-8'))
    print j
    if len(j) == 2:
        t += "n" + j
    else:
        t += j
print t
print binascii.b2a_hex(u'啊'.encode('utf-8'))

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)
print toHex(u'啊')
print ' 771f76844e0d597d ======='
print toHex(u'真的不好')

#print(binascii.b2a_hex('好吃吗'.encode('utf_8')))
