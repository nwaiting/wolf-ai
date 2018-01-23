#coding=utf-8

__author__ = 'Administrator'

from stompy.simple import Client
from stompy.stomp import *

def simple():
    # 通过simple方式连接JMS服务器
    # 指定hostname和port（tips:ActiveMQ支持多种协议连接stomp协议的默认端口为61613，这里不要写为61616）
    stomp = Client('192.168.1.166', 61613)
    #stomp = Client()#如果是ActiveMQ和ActiveMQ客户端（本程序）在同一台机器可使用默认值：hostname="localhost",port=61613

    # 连接服务器
    stomp.connect()
    # 发送消息到指定的queue
    stomp.put("The quick brown fox...", destination="/queue/hello")
    # 从指定的queue订阅消息。ack参数指定为"client",不然可能出现一个问题（具体忘了，以后补充）,ack默认值为"auto"
    stomp.subscribe("/queue/hello",ack="client")
    # 等待接收ActiveMQ推送的消息
    message = stomp.get()
    # 打印消息的主体
    print message.body
    message.body
    'quick brown fox...'
    stomp.ack(message)
    # 退订
    stomp.unsubscribe("/queue/hello")
    # 关闭连接
    stomp.disconnect()

def simple_receive():
    stomp = Client('192.168.1.166', 61613)
    stomp.connect()
    stomp.subscribe("/queue/hello",ack="client")

    while True:
        message = stomp.get()
        print message.body
        stomp.ack(message)

    stomp.unsubscribe("/queue/hello")
    stomp.disconnect()

def stomp():
    stomp = Stomp('192.168.1.166', 61613)
    stomp.connect()
    stomp.send({'destination': '/queue/hello', 'body': 'Testing', 'persistent': 'true'})
    stomp.subscribe({'destination':'/queue/hello', 'ack':'client'})
    frame = stomp.receive_frame()
    print(frame.headers['message-id'])
    print frame.body
    stomp.ack(frame)
    stomp.unsubscribe({'destination': '/queue/hello'})
    stomp.disconnect()

def stomp_receive():
    stomp = Stomp('192.168.1.166', 61613)
    stomp.connect()
    stomp.subscribe({'destination':'/queue/hello', 'ack':'client'})
    while True:
        frame = stomp.receive_frame()
        print(frame.headers['message-id'])
        print frame.body
        stomp.ack(frame)
    stomp.unsubscribe({'destination': '/queue/hello'})
    stomp.disconnect()

simple()
#simple_receive()
#stomp()
#stomp_receive()
