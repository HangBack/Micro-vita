import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def create_socket(self):
        # 创建一个TCP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # 连接到服务器
        self.client_socket.connect((self.host, self.port))

    def send(self, data):
        # 发送数据
        self.client_socket.sendall(data.encode())

    def receive(self, buffer_size=1024):
        # 接收数据
        data = self.client_socket.recv(buffer_size)
        return data.decode()

    def close(self):
        # 关闭客户端socket
        self.client_socket.close()