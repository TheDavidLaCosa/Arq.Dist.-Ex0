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

    try:
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
                else:
                    print(f'The client with ID = {address[1]} said \'{msg}\'')

    # Handling unexpected disconnect
    except ConnectionResetError:
        print(f'Client {address[1]} has disconnected unexpectedly')

    # Deleting the thread
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

        print(f'Connection nº{threading.active_count() - 1}: {address[1]}')  # TODO: Fer que s'incrementi i es decrementi quan entra i s'envà o solament incrementar?

        message = format_message("Hola!")


        #Sending information to the client
        client.send(message.encode(FORMAT))
        time.sleep(5)

        client.send(message.encode(FORMAT))



def read():
    print("Read")

def update(value):
    print("Update")
