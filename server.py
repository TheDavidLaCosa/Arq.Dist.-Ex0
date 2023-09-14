import socket

def read():
    print("Read")

def update(value):
    print("Update")


if __name__ == "__main__":
    # Server creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 1500))
    s.listen(5)

    print(" ----------------------------\n"
          "|           SERVER           |\n"
          " ----------------------------\n\n")
    while True:
        client, address = s.accept()
        print(f'Connection {address} de {client}')

        #Sending information to the client
        client.send(bytes("Pipooo", "utf-8"))
