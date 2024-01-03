import socket
import threading
import time


class ClientToken:
    def __init__(self, id_c, port):

        self.value = 0
        self.has_token = False

        # Socket to server
        self.id_c = id_c
        self.port = port + id_c
        self.sk_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk_s.bind(("localhost", self.port))
        self.sk_s.connect(("localhost", port))

        # Debug options
        self.debug = True

        # UI
        self.color = "\033[3" + str(self.id_c) + "m"

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
                pass

        elif msg[0] == "R":
            try:
                self.value = int(msg[1])

            except ValueError:
                pass

        # Handling unknown message
        else:
            self.print_m(f"UNKNOWN MESSAGE - {msg}")


    # Function that performs the actions
    def actions(self):
        if not self.has_token:
            pass

        print("-----------------------------------------------")
        for i in range(3):
            self.update()
            self.value += 1
            self.read()
            time.sleep(1)
        print("-----------------------------------------------")

    # Function that returns the token
    def return_token(self):
        if self.has_token:
            self.sk_s.send(f"T-{self.id_c}".encode("utf-8"))

    def print_m(self, msg):
        print(f"[{self.color}{self.id_c}\033[0m]: {msg}")

    def update(self):
        time.sleep(0.1)
        self.sk_s.send(f"U-{self.id_c}-{self.value + 1}".encode("utf-8"))

    def read(self):
        time.sleep(0.1)
        self.sk_s.send(f"R-{self.id_c}".encode("utf-8"))
        # TODO: wait for value
