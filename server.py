import socket

def read():
    print("Read")

def update(value):
    print("Update")


if __name__ == "__main__":
    # Server creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1000))

    while True:
        client, address = s.accept()
        print(f'Connection {address} de {client}')

        #Sending information to the client
        client.send(bytes("Pipooo", "utf-8"))
