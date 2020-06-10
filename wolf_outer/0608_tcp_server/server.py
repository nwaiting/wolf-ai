import socket
import sys
import threading
import os
import pickle


connections = []
stock_infos = {
    "600116": {'buy01':6.6,'buy02':6.7,'buy03':6.8,'buy04':6.9,'buy05':6.6,
               'sell01':8.8,'sell02':8.8,'sell03':8.8,'sell04':8.8,'sell05':8.8},
    "000958": {'buy01':9.9,'buy02':9.9,'buy03':9.9,'buy04':9.9,'buy05':9.9,
               'sell01':11.3,'sell02':11.3,'sell03':11.3,'sell04':11.3,'sell05':11.3},
}
buy_infos = {}
sell_infos = {}
has_stock_info = {}


def confirm_stock_price(stock_id):
    buy_total = 0
    buy_price = 0
    if buy_infos.get(stock_id):
        buy_total = int(buy_infos.get(stock_id)[-1][1])
        buy_price = buy_infos.get(stock_id)[-1][2]

    sell_total = 0
    sell_price = 0
    if sell_infos.get(stock_id):
        sell_total = int(sell_infos.get(stock_id)[-1][1])
        sell_price = sell_infos.get(stock_id)[-1][2]
    if buy_total == 0 and sell_total == 0:
        return 0
    if buy_total != 0 and sell_total == 0:
        return float(buy_price)
    if buy_total == 0 and sell_total != 0:
        return float(sell_price)
    return ((buy_total * float(buy_price)) + (sell_total * float(sell_price)))/(buy_total+sell_total)


class MyServer(object):
    def __init__(self, port=58888):
        self._host = '0.0.0.0'
        self._port = port
        self._s = None
        self._total_connections = 0
        self.init()

    def init(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._s.bind((self._host, self._port))
        except Exception as msg:
            print('Bind failed. Error {}'.format(msg))
            sys.exit()

        self._s.listen(10)

    def run(self):
        print("start listen {}:{}".format(self._host, self._port))
        while 1:
            sock, address = self._s.accept()
            connections.append(Client(sock, address, self._total_connections, "Name", True))
            connections[len(connections) - 1].start()
            print("New connection at ID {}".format(connections[len(connections) - 1]))
            self._total_connections += 1
        self._s.close()


class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self._socket = socket
        self._address = address
        self._id = id
        self._user_id = None
        self._name = name
        self._signal = signal
        self.user_datas = {}
        self.file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "accounts.data")
        self.load_user_data()
        self.buy_data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "buy.data")
        self.load_buy_data()
        self.sell_data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sell.data")
        self.load_sell_data()
        self.has_stock_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "has.data")
        self.load_has_stock_data()

    def __str__(self):
        return str(self._id) + " " + str(self._address)

    def load_sell_data(self):
        global sell_infos
        if not sell_infos:
            try:
                with open(self.sell_data_file, 'rb') as usr_file:
                    sell_infos = pickle.load(usr_file)
            except FileNotFoundError:
                sell_infos = {}

    def save_sell_data(self):
        with open(self.sell_data_file, 'wb') as usr_file:
            pickle.dump(sell_infos, usr_file)

    def load_buy_data(self):
        global buy_infos
        if not buy_infos:
            try:
                with open(self.buy_data_file, 'rb') as usr_file:
                    buy_infos = pickle.load(usr_file)
            except FileNotFoundError:
                buy_infos = {}

    def save_has_stock_data(self):
        with open(self.has_stock_file, 'wb') as usr_file:
            pickle.dump(has_stock_info, usr_file)

    def load_has_stock_data(self):
        global has_stock_info
        if not has_stock_info:
            try:
                with open(self.has_stock_file, 'rb') as usr_file:
                    has_stock_info = pickle.load(usr_file)
            except FileNotFoundError:
                has_stock_info = {}

    def save_buy_data(self):
        with open(self.buy_data_file, 'wb') as usr_file:
            pickle.dump(buy_infos, usr_file)

    def load_user_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'rb') as f:
                for line in f.readlines():
                    line = line.decode('utf-8').strip('\r\n ').split()
                    self.user_datas[line[0]] = line[1]

    def save_user_data(self, name, pwd):
        with open(self.file_name, 'a') as f:
            f.write("{} {}\n".format(name, pwd))
            self.user_datas[name] = pwd

    def send(self, msg):
        return self._socket.send(msg.encode('utf-8'))

    def run(self):
        while self._signal:
            try:
                data = self._socket.recv(4096)
            except:
                print("Client " + str(self._address) + " has disconnected")
                self._signal = False
                connections.remove(self)
                break
            if data:
                data = data.decode("utf-8")
                data_items = data.split('-')
                if data_items[0] == '1':
                    # 注册
                    # 保存账号信息
                    self.save_user_data(data_items[1], data_items[2])
                    self.send('register success')
                elif data_items[0] == '2':
                    # 登录
                    # 发送stock信息
                    if self.user_datas.get(data_items[1]) != data_items[2]:
                        self.send('err ')
                    else:
                        self._user_id = data_items[1]
                        send_str = ''
                        for k,v in stock_infos.items():
                            tmp_k = "{},".format(k) + ','.join(["{},{}".format(itemk,itemv) for itemk,itemv in v.items()])
                            send_str += "{}-".format(tmp_k)
                        send_size = self.send(send_str)
                        print("send size = {}".format(send_size))
                        send_str2 = ''
                        for tk,tv in has_stock_info.get(self._user_id, {}).items():
                            send_str2 += "{},{}-".format(tk,tv)
                        if not send_str2:
                            send_str2 = 'has no stock info'
                        send_size = self.send(send_str2)
                        print("send size2 = {}".format(send_size))
                elif data_items[0] == '3':
                    # 买入stock
                    # 3-600016-1000-9.6
                    if data_items[1] not in buy_infos:
                        buy_infos[data_items[1]] = []
                    buy_infos[data_items[1]].append([self._id, data_items[2], data_items[3]])
                    last_price = confirm_stock_price(data_items[1])
                    self.save_buy_data()
                    if self._user_id not in has_stock_info:
                        has_stock_info[self._user_id] = {}
                    if data_items[1] not in has_stock_info[self._user_id]:
                        has_stock_info[self._user_id] = {data_items[1]: 0}
                    has_stock_info[self._user_id][data_items[1]] += int(data_items[2])
                    self.save_has_stock_data()
                    self.send("success buy-{}".format(last_price))
                elif data_items[0] == '4':
                    # 卖出stock
                    # 4-600016-1000-9.6
                    has_count = has_stock_info[self._user_id].get(data_items[1], 0)
                    if has_count < int(data_items[2]):
                        self.send("err not enough stock-{}".format(has_count))
                        return
                    has_stock_info[self._user_id][data_items[1]] -= int(data_items[2])
                    self.save_has_stock_data()
                    if data_items[1] not in sell_infos:
                        sell_infos[data_items[1]] = []
                    sell_infos[data_items[1]].append([self._id, data_items[2], data_items[3]])
                    last_price = confirm_stock_price(data_items[1])
                    self.save_sell_data()
                    self.send("success sell-{}".format(last_price))
                else:
                    self.send("err type")
            else:
                self._socket.close()


def main():
    server = MyServer()
    server.run()


if __name__ == "__main__":
    main()







