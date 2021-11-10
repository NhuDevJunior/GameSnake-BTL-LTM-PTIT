class SnakeClient:
    def __init__(self,HOST=IP_LAN, PORT=65432):

        self.HOST = HOST  
        self.PORT = PORT        

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        self.s.connect((self.HOST, self.PORT))

    def Send(self, snake):
        data = pickle.dumps(snake)
        self.s.sendall(data)

    def Receive(self):
        data = self.s.recv(1024)
        enemy_snake = pickle.loads(data)
        return enemy_snake