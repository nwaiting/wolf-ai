#coding=utf8

import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def sendMessage(message, fromUser, password, toUser, smtp_server):
    '''发送邮件'''
    msg = MIMEText(message, 'plain', 'utf-8')
    # 下面三项不标明可能被当作垃圾邮件，导致接收方收不到邮件
    msg['From'] = _format_addr(u'Mac管理员-%s' % fromUser) # 邮件中标明发件人
    msg['To'] = _format_addr(u'家长-%s' % toUser) # 邮件中标明收件人
    msg['Subject'] = Header(u'屏幕监测报告', 'utf-8').encode() # 邮件标题
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.login(fromUser, password)
    server.sendmail(fromUser, toUser, msg.as_string())
    server.quit()

def _format_addr(s):
    '''调整邮件信息格式'''
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

if __name__ == '__main__':
    msg = None
    # `cat  ${SourcePath}freewenxiao_offlist`
    with open('', 'rb') as f:
        contents = f.read()
        msg = '<html><font size="2"> ' + contents + ' </font></html> '
    header_contents = 'Vod oss disabled report({0})'.format(time.strftime('%Y/%m/%d', time.localtime()))
    to_users = 'idc_wh@pptv.com,ops_isp@pptv.com,freewenxiao@pptv.com'
    from_user = 'system@p2psystem.cn'
    from_user_passwd = 'UP30sEm9'
    smtp_server_addr = 'mail.p2psystem.cn'
    sendMessage(msg, from_user, from_user_passwd, to_users, smtp_server_addr)
