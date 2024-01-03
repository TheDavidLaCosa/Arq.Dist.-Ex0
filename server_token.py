import random
import socket


class ServerToken:
    def __init__(self, num_clients):

        # Clients
        self.clients = []
        self.num_clients = num_clients

        # Token
        self.has_token = True

        # Server
        self.HOST = "localhost"
        self.PORT = 60000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))


    def start(self):

        print(f"Server starting")

        # Connecting to all the clients
        for i in range(self.num_clients):
            self.socket.listen()
            client_sk, address = self.socket.accept()

            # Checking if the socket has been created
            if client_sk is None:
                print(f"[ERROR]: Communication failed!")
                continue

            self.clients.append(client_sk)
            print(f"Process nº{i + 1} successfully connected!")

        # Sending token to a client
        self.send_token(0)

        i = 0
        while True:

            print("AHHHH")
            # Listening to the sockets of the other processes
            temp = self.clients[0].recv(1024).decode("utf-8")
            i += 1

            print(f"aaaaa{temp}")





    # Function that sends a message to all the clients
    def send_all(self):
        for i in range(len(self.clients)):
            self.clients[i].send("Hola".encode("utf-8"))


    # Function that sends the token to a client
    def send_token(self, id_c):
        # TODO: Fer que es segueixi algun criteri d'enviament (prioritat?)
        self.clients[id_c].send("T".encode("utf-8"))

    # Function that sends the token to a random client
    def send_token_random(self):
        self.send_token(random.randint(0, self.num_clients - 1))