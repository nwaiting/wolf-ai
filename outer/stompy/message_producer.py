#coding=utf-8

import time
import datetime
import sys
from stompy.simple import Client
from stompy.stomp import Stomp, ConnectionError, ConnectionTimeoutError

def main():
    cstomp = Client(host='10.200.10.194',port=61613)
    cstomp.connect()
    cstomp.subscribe("test1")
    cstomp.put("The quick brown fox...", destination="/queue/test1")
    try:
        message = cstomp.get_nowait()
    except Exception as e:
        print('error {0}'.format(e))
    print('message ', message.body)
    cstomp.ack(message.body)
    cstomp.unsubscribe("/queue/test1")
    cstomp.disconnect()

def func2():
    class MyListener(object):
        def on_error(self, headers, message):
            print('received an error %s' % message)
        def on_message(self, headers, message):
            print('received a message %s' % message)

    #官方示例的连接代码
    conn = stomp.Connection([('10.200.10.194',61627)])
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect()

    conn.subscribe(destination='test1', id=1, ack='auto')
    #注意，官方示例这样发送消息的  $ python simple.py hello world
    #conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')
    conn.send(body='hello,garfield!', destination='test1')

    time.sleep(1)
    conn.disconnect()

def func3():
    connection = Stomp('10.200.10.194', 61627)
    connection.connect()
    while True:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        send_msg = 'hello,garfield! {0}'.format(time_str)
        connection.send({'body':send_msg, 'destination':'/queue/test1', 'persistent':'true'})
        #connection.send({'body':send_msg, 'destination':'/queue/test1'})
        #connection.subscribe({'destination': '/queue/test1', 'ack': 'client'})
        print(send_msg)
        time.sleep(0.5)
    """
    frame = connection.receive_frame()
    print(frame.headers['message-id'])
    print('body : ', frame.body)
    connection.ack(frame=frame)
    """
    connection.unsubscribe({'destination':'/queue/test1'})
    time.sleep(0.1)
    connection.disconnect()



if __name__ == '__main__':
    #main()
    #func2()
    func3()
