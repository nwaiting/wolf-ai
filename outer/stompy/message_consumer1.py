#coding=utf-8

import time
from stompy.stomp import Stomp, ConnectionError, ConnectionTimeoutError
from stompy.simple import Client

def main():
    stomp = Client('10.200.10.194', 61624)
    stomp.connect()
    stomp.subscribe('/queue/test1', ack='client')
    while True:
        message = stomp.get(block=True)
        print(type(message), message.body)
        stomp.ack(message)
    connection.unsubscribe({'destination':'/queue/test1'})
    time.sleep(1)
    connection.disconnect()


if __name__ == '__main__':
    main()
