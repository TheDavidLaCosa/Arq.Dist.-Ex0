import socket


class ClientToken:
    def __init__(self, id_c):
        self.id_c = id_c
        self.port = 60000 + id_c

        # Token
        self.has_token = False

        # Socket to server
        self.sk_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk_s.connect(("localhost", 60000))

    def start(self):
        print(f"Client {self.id_c}")