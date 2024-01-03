import socket
import threading
import time


class ClientToken:
    def __init__(self, id_c, port):

        self.value = 0
        # Token
        self.has_token = False

        # Socket to server
        self.id_c = id_c
        self.port = port + id_c
        self.sk_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk_s.bind(("localhost", self.port))
        self.sk_s.connect(("localhost", port))

    def start_client(self):
        self.print_m(f"Waking up...")
        time.sleep(0.2)
        # Starting action loop
        #threading.Thread(target=self.actions, daemon=True).start()

        # Listening loop
        while True:
            msg = self.sk_s.recv(1024).decode("utf-8")

            self.decode_messge(msg)

    # Function that decodes de message received
    def decode_messge(self, msg):

        msg = msg.split("-")
        # Handling token message
        if msg[0] == "T":
            # Taking ownership of token
            self.print_m(f"I have the token!")
            self.has_token = True
            # Performing actions
            self.actions()
            # # Retuning token
            self.return_token()

        # Handling update
        elif msg[0] == "U":
            try:
                self.value = int(msg[1])

            except ValueError:
                print(f"AAAAAAAAAAAAAAAAAAA {self.id_c} --- {msg}")

        elif msg[0] == "R":
            try:
                self.value = int(msg[1])

            except ValueError:
                print(f"AAAAAAAAAAAAAAAAAAA {self.id_c} --- {msg}")

        # Handling unknown message
        else:
            self.print_m(f"UNKNOWN MESSAGE - {msg}")


    # Function that performs the actions
    def actions(self):
        if self.has_token:
            pass
        for i in range(3):
            self.sk_s.send(f"R-{self.id_c}".encode("utf-8"))
            time.sleep(1)

    # Function that returns the token
    def return_token(self):
        if self.has_token:
            self.sk_s.send(f"T".encode("utf-8"))

    def print_m(self, msg):
        print(f"[{self.id_c}]: {msg}")
