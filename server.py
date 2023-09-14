import socket
import threading
import time

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"

# Function that adds the header to the message
def format_message(text):

    text = f'[Server message]: ' + text
    text = f'{len(text):<{HEADER_SIZE}}' + text

    return text

# Funtion that handles multiple clients
def handle_client(client, address):

    connected = True

    while connected:
        # Reading the header of the message to know the length
        length = client.recv(HEADER_SIZE)

        # Checking if the message is not none (sometimes the client sends none during the first connection)
        if length:
            length = int(length.decode(FORMAT))

            # Reading the message
            msg = client.recv(length).decode(FORMAT)

            # Checking if the connection is terminated
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f'Client {address[1]} has disconnected')

    client.close()



if __name__ == "__main__":

    # Server creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", u.PORT))
    s.listen(5)

    # Initial message
    print(" ----------------------------\n"
          "|           SERVER           |\n"
          " ----------------------------\n\n")

    # Listening loop
    while True:

        # Accept connection
        client, address = s.accept()

        # Keep the client conncted
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

        print(f'Connection nº{threading.active_count() - 1}: {address[1]}')

        message = format_message("Hola!")


        #Sending information to the client
        client.send(bytes(message, FORMAT))
        time.sleep(5)



def read():
    print("Read")

def update(value):
    print("Update")
