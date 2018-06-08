#coding=utf-8

from login import WeiboLogin
import collectData

if __name__ == '__main__':
    uid = '18640376585'
    psw = '89364013'

    WeiboLogin(uid, psw)
    collectData.main()
