import socket
import pickle
import random
import threading

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
IP_LAN="192.168.0.102"
PORT = 65432
def get_ip():
    try:
        h_name = socket.gethostname()
        IP = socket.gethostbyname(h_name)
        print(IP)
    except Exception:
        IP = IP_LAN
    return IP

class SnakeServer:
    def __init__(self):
        self.running = True

    def GameSession(self, Connections):
        food_pos = []
        data_snake_1 = []
        data_snake_2 = []
        no_food = True
        while self.running:

            data_snake_1 = Connections[0].recv(1024)
            data_snake_2 = Connections[1].recv(1024)
            if not data_snake_1:
                break
            if not data_snake_2:
                break

            data_snake_1 = pickle.loads(data_snake_1)
            data_snake_2 = pickle.loads(data_snake_2)
            if not food_pos:
                no_food = True
            else:
                no_food = False
            while not food_pos:
                x = random.randint(2, 28) * 20
                y = random.randint(2, 28) * 20
                if not [x, y] in data_snake_1 and not [x, y] in data_snake_2:
                    food_pos = [x, y]
                    data_snake_1.append(food_pos)
                    data_snake_2.append(food_pos)

            if data_snake_1[-2] == food_pos or data_snake_2[-2] == food_pos:
                food_pos = []
                data_snake_1.append([-20, -20])
                data_snake_2.append([-20, -20])
            if food_pos and no_food == False:
                data_snake_1.append(food_pos)
                data_snake_2.append(food_pos)

            data_snake_1 = pickle.dumps(data_snake_1)
            data_snake_2 = pickle.dumps(data_snake_2)

            Connections[0].sendall(data_snake_2)
            Connections[1].sendall(data_snake_1)

    def Start(self):
        self.running = True
        HOST = get_ip()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((HOST, PORT))
        self.s.listen(5)
        conn_list = []
        threads = []
        print("Server is Running")
        print(PORT)
        while self.running:
            for i in range(2):
                try:
                    if i:
                        print("Waiting for 2nd Player to connect")
                    conn, addr = self.s.accept()
                    print('Connected by', addr[0])
                    conn_list.append(conn)
                except:
                    self.running = False
            threads.append(threading.Thread(
                target=self.GameSession, args=(conn_list,)))
            threads[-1].start()
            conn_list = []

    def Stop(self):
        self.s.close()
        self.running = False


class ServerWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ServerWindow, self).__init__(*args, **kwargs)
        self.server_is_online = False
        self.ss = SnakeServer()
        # self.server = threading.Thread(target=self.ss.Start, args=())

        self.setWindowTitle("Server")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.server_status = QLabel("  Server Status: Offline", self)
        self.server_status.setStyleSheet("background-color: red")
        self.server_status.resize(150, 30)
        self.server_status.move(0, 0)

        ip_label = QLabel("Local IP:" + get_ip(),self)
        ip_label.move(170,0)

        #init port server
        self.port_label = QLabel("Port:",self)
        self.port_label.move(20,100)
        self.port_input = QLineEdit(self)
        self.port_input.move(50, 105)
        self.port_input.resize(50,20)
        self.port_input.setText("65432")
        start_btn = QPushButton("Start", self)
        start_btn.setToolTip("Start your Server")
        start_btn.resize(150, 100)
        start_btn.move(0, 200)
        start_btn.setStyleSheet("QPushButton"
                                "{"
                                "background-color : green;"
                                "}")
        start_btn.clicked.connect(self.On_start)

        stop_btn = QPushButton("Stop", self)
        stop_btn.setToolTip("Stop your Server")
        stop_btn.resize(150, 100)
        stop_btn.move(150, 200)
        stop_btn.setStyleSheet("QPushButton"
                               "{"
                               "background-color : red;"
                               "}")
        stop_btn.clicked.connect(self.On_stop)
    def PlayerList(self):
        pass
    def On_start(self):
        if not self.server_is_online:
            self.server_status.setStyleSheet("background-color: green")
            self.server_status.setText("  Server Status: Online")
            global PORT
            port = self.port_input.text()
            PORT = int(port)
            self.server = threading.Thread(target=self.ss.Start, args=())
            self.server.start()
            self.server_is_online = True
        else:
            print("Server is allready running")

    def On_stop(self):

        if self.server_is_online:
            self.server_status.setStyleSheet("background-color: red")
            self.server_status.setText("  Server Status: Offline")
            print("Server is stopping...")
            self.ss.Stop()
            self.server.join()
            print("Server Stopped")
            self.server_is_online = False
        else:
            print("Server is allready stopped")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    app.exec_()
