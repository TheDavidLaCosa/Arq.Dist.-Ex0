import socket


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

    def start(self):
        self.print_m(f"Waking up...")

        # Listening loop
        while True:
            msg = self.sk_s.recv(1024).decode("utf-8")
            msg = msg.split("-")

            self.decode_messge(msg)

    # Function that decodes de message received
    def decode_messge(self, msg):
        # Handling token message
        if msg[0] == "T":
            self.print_m(f"I have the token!")
            self.sk_s.send(f"BACK FROM {self.id_c}".encode("utf-8"))
        # Handling update
        elif msg[0] == "U":
            self.value = int(msg[1])
        # Handling unknown message
        else:
            self.print_m("UNKNOWN MESSAGE")

    def print_m(self, msg):
        print(f"[{self.id_c}]: {msg}")