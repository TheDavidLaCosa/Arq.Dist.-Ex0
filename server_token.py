import random
import socket
import threading


class ServerToken:
    def __init__(self, num_clients, port):

        # Clients
        self.clients = []
        self.num_clients = num_clients

        self.value = 0

        # Token
        self.has_token = True

        # Server
        self.HOST = "localhost"
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.port))

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

            temp = threading.Thread(target=self.listen, args=(i,), daemon=True)
            self.clients.append((client_sk, temp))
            temp.start()

            print(f"Process nº{i + 1} successfully connected!")

        # Sending token to a client
        self.send_token(0)

    def listen(self, id_c):
        color = "\033[3" + str(id_c + 1) + "m"
        while True:
            # Receive message
            temp = self.clients[id_c][0].recv(1024).decode("utf-8")
            print(f"[{color}S{id_c + 1}\033[0m] received: {temp}")
            # Decode message received
            self.decode_message(temp)

    # Function that sends a message to all the clients
    def send_all(self, msg):
        for i in range(len(self.clients)):
            self.clients[i][0].send(msg.encode("utf-8"))

    # Function that sends the token to a client
    def send_token(self, id_c):
        # TODO: Fer que es segueixi algun criteri d'enviament (prioritat?)
        self.clients[id_c][0].send("T".encode("utf-8"))

    # Function that sends the token to a random client
    def send_token_random(self):
        self.send_token(random.randint(0, self.num_clients - 1))

    def decode_message(self, msg):

        msg = msg.split("-")

        # Handling token message
        if msg[0] == "T":
            # Sending token to another client
            self.send_token_random()

        # Handling update
        elif msg[0] == "U":
            try:
                # Updating the value
                self.value = int(msg[2])
                print(f"UPDATEEE: {msg[1]} - value: {msg[2]}")
                # Sending updated value to all the clients
                #self.send_all(f"U-{self.value}")

            except ValueError:
                print(f"\033[91mERROR!\033[0m: \"{msg}\"")

        # Handling read
        elif msg[0] == "R":
            try:
                self.send_read(int(msg[1]))
            except ValueError:
                pass
        # Handling unknown message
        else:
            self.print_m("UNKNOWN MESSAGE")

    def send_update(self, id_c):
        self.clients[id_c - 1][0].send(f"U-{self.value}".encode("utf-8"))

    def send_read(self, id_c):
        print(f"READ de {id_c}")
        self.clients[id_c - 1][0].send(f"R-{self.value}".encode("utf-8"))