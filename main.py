import socket
import threading
import time

from client_token import ClientToken
from server_token import ServerToken


def init_server():
    # Server creation
    print("a")

if __name__ == "__main__":

    #Todo: Preguntar per nº clients
    num_clients = 5
    port = 6000

    server = ServerToken(num_clients, port)

    threading.Thread(target=server.start, daemon=True).start()

    clients = []
    for i in range(num_clients):
        client = ClientToken(i + 1, port)
        thread = threading.Thread(target=client.start_client, daemon=True)
        clients.append((client, thread))
        clients[i][1].start()

    while True:
        time.sleep(1)
