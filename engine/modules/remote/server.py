import socket
import random

class Server:
    def __init__(self, host = '0.0.0.0', port = None):
        if port is None:
            port = random.randrange(0, 65536)
        self.host = host
        self.port = port
        self.server_socket = None

    def create_socket(self):
        # 创建一个TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        # 绑定地址和端口
        self.server_socket.bind((self.host, self.port))

    def listen(self, max_connections=5):
        # 监听连接
        self.server_socket.listen(max_connections)

    def accept(self):
        # 等待客户端连接
        client_socket, client_address = self.server_socket.accept()
        return client_socket, client_address

    def close(self):
        # 关闭服务器socket
        self.server_socket.close()

    def on_receive(self):
        while True:
            ...