import socket


class ServerToken:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 60000

        # Token
        self.has_token = True

        # Server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))

    def start(self):

        print(f"Server starting")
        while True:
            self.socket.listen()
            comm_sock, address = self.socket.accept()

            # Checking if the socket has been created
            if comm_sock is None:
                print(f"[ERROR]: Communication failed!")
                continue

            print(f"Processes successfully connected!")

