import socket
import time

HEADER_SIZE = 5

def read():
    print("Read")

def update(value):
    print("Update")

# Function that adds the header to the message
def format_message(text):

    text = f'[Server message]: ' + text
    text = f'{len(text):<{HEADER_SIZE}}' + text

    return text


if __name__ == "__main__":
    # Server creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 1500))
    s.listen(5)

    # Initial message
    print(" ----------------------------\n"
          "|           SERVER           |\n"
          " ----------------------------\n\n")

    # Listening loop
    while True:

        # Receive connection
        client, address = s.accept()
        print(f'Connection {address} de {client}')

        message = format_message("Hola!")


        #Sending information to the client

        client.send(bytes(message, "utf-8"))
        time.sleep(5)
