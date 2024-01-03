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

    server = ServerToken(num_clients)

    threading.Thread(target=server.start, daemon=True).start()

    clients = []
    for i in range(num_clients):
        client = ClientToken(i + 1)
        thread = threading.Thread(target=client.start, daemon=True)
        clients.append((client, thread))
        clients[i][1].start()

    while True: # TODO: Stop loop
        time.sleep(1)


    '''i=0

    init_server()
    # Reading file containing the servers
    n_elements=5

    # Initaiating the servers   
    while i < n_elements:
        i+=1

    # TODO: Send message to tell the server to start'''