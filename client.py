import socket
import threading
import sys
import time

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"
shutdown = False
shared_value=0
sock = None



# Function that generates the structure of the message
def format_action(mode, value):

    if value:
        text = f'{value}'
    else:
        text = f'{str(mode):<{1}}'
    return text + "&"


def read(s):
    txt = format_action("r", "")
    s.send(txt.encode(FORMAT))


def update(s, value):
    txt=format_action("u", value)
    s.send(txt.encode(FORMAT))

# Function that controls the user input
def recieve_messages(sock):

    while True:
        length = sock.recv(HEADER_SIZE)
        mesg=sock.recv(int(length))

        shared_value = bytes(mesg)
        print(f'Received: {shared_value}')

    '''try:
        while True:
            # Reading the header of the message to know the length
            msg = sock.recv(HEADER_SIZE)

            # Checking if the message is not none (sometimes the client sends none during the first connection)
            if length:
                length = int(length.decode(FORMAT))

                # Reading the message
                msg = client.recv(length).decode(FORMAT)

                # Checking if the connection has been terminated
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f'Client {address[1]} has disconnected')
                    delete_user((client, address[1]))
                else:
                    # Decoding the message received
                    deformat_message(msg, client)

                    print(f'The client with ID = {address[1]} said \'{msg}\'')

    # Handling unexpected disconnect
    except ConnectionResetError:
        print(f'Client {address[1]} has disconnected unexpectedly')
        delete_user((client, address[1]))

    # Deleting the thread
    client.close()'''

    '''is_new_msg = False
    full_msg = ""
    length = 0

    # Asking for the value
    message = format_action(1, "")
    send(sock, message)

    # Waiting for the response
    while True:

        # Receiving the message in small sizes
        msg = sock.recv(HEADER_SIZE)

        # Reading the length of the message
        if is_new_msg:
            # Reading the header to know where the length of the message
            length = int(msg[:HEADER_SIZE])  # The :HEADER_SIZE deletes the spaces after the message

            # After reading the message we stop reading the header
            is_new_msg = False

        # Adding the part of the message received and adding it to the full message
        full_msg += msg.decode(FORMAT)

        # Showing the full message
        if len(full_msg) - HEADER_SIZE == length:
            print(full_msg[HEADER_SIZE:])  # The HEADER_SIZE: deletes the size of the message that is being shown

            value = full_msg[HEADER_SIZE:]

            try:
                shared_value = int(value)
                print(f'{value}')
                continue
            except ValueError:
                print(f'[ERROR]: The received value is not a number (received: {value})')'''


if __name__ == "__main__":

    # Connection to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", u.PORT))

    # Watch for client input
    thread = threading.Thread(target=recieve_messages, args=(sock,))
    thread.start()

    try:

        while True:
            valor = read(sock)

            print("read")

            update(sock, 500)
            print("update")

            time.sleep(1)


    except ConnectionResetError:
        print("[ERROR]: The server has disconnected unexpectedly")
        shutdown = True  # TODO: Gestionar que l'usuari escrigui input després de que el servidor s'hagi desconnectat (peta)
        # Closing connection
        sock.close()
        # TODO: Matar els threads al apagar

        sys.exit()





