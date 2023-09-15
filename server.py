import socket
import threading
import time

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"
users = []


def read():
    print("Read")


def update(value):
    print("Update")

# Function that adds the header to the message
def format_message(text):
    text = f'[Server message]: ' + text
    text = f'{len(text):<{HEADER_SIZE}}' + text

    return text


# Function that decodes the received message
def deformat_message(text):

    # Getting the values
    mode = int(text[:1])
    value = text[2:]

    if mode == 1:
        read()
    elif mode == 2:
        update(value)
    else:
        print(f'[ERROR]: Action {mode} doesn\'t exist')


# Function that adds a user to the user list
def addUser(user):
    users.append(user)


# Function that deletes a user from the user list
def deleteUser(user):
    users.remove(user)


def send(client, message):
    client.send(message.encode(FORMAT))


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

                # Checking if the connection has been terminated
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f'Client {address[1]} has disconnected')
                    deleteUser((client, address[1]))
                else:
                    # Decoding the message received
                    deformat_message(msg)

                    print(f'The client with ID = {address[1]} said \'{msg}\'')

    # Handling unexpected disconnect
    except ConnectionResetError:
        print(f'Client {address[1]} has disconnected unexpectedly')
        deleteUser((client, address[1]))

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

        print(
            f'Connection nº{threading.active_count() - 1}: {address[1]}')  # TODO: Fer que s'incrementi i es decrementi quan entra i s'envà o solament incrementar?
        addUser((client, address[1]))

        message = format_message("Hola!")

        # Sending information to the client
        send(client, message)
        time.sleep(3)

        # TODO: Gestionar enviament a clients no existens (al fer broadcast)
        print(users)


