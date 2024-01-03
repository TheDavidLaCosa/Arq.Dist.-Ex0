import socket
import threading
import time


class ClientToken:
    def __init__(self, id_c):

        self.value = 0
        # Token
        self.has_token = False

        # Socket to server
        self.id_c = id_c
        self.port = 60000 + id_c
        self.sk_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk_s.bind(("localhost", self.port))
        self.sk_s.connect(("localhost", 60000))

    def start_client(self):
        self.print_m(f"Waking up...")

        # Starting action loop
        threading.Thread(target=self.actions, daemon=True).start()

        # Listening loop
        while True:
            msg = self.sk_s.recv(1024).decode("utf-8")
            msg = msg.split("-")

            self.decode_messge(msg)

    # Function that decodes de message received
    def decode_messge(self, msg):
        # Handling token message
        if msg[0] == "T":
            # Informing of ownership of token
            self.print_m(f"I have the token!")
            # Performing actions
            self.actions()
            # # Retuning token
            self.return_token()

        # Handling update
        elif msg[0] == "U":
            self.value = int(msg[1])
        # Handling unknown message
        else:
            self.print_m("UNKNOWN MESSAGE")


    # Function that performs the actions
    def actions(self):
        while True:
            self.sk_s.send(f"U-{self.id_c}".encode("utf-8"))
            time.sleep(1)

    # Function that returns the token
    def return_token(self):
        self.sk_s.send(f"T".encode("utf-8"))

    def print_m(self, msg):
        print(f"[{self.id_c}]: {msg}")
