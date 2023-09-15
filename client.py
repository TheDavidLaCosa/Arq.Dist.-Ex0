import socket
import threading
import sys

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"
shutdown = False


# Function that adds the header to the message
def format_message(text):
    text = f'{len(text):<{HEADER_SIZE}}' + text

    return text


def send(s, text):
    text = format_message(text)
    s.send(text.encode(FORMAT))

# Function that controlls the user input
def handle_input(sock):

    while True:

        if shutdown:
            sock.close()
        else:
            txt = input("Message: ")
            print(txt)
            send(sock, txt)

if __name__ == "__main__":

    # Connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", u.PORT))

    # send(s, DISCONNECT_MESSAGE)
    # exit()

    # Watch for client input
    thread = threading.Thread(target=handle_input, args=(s,))
    thread.start()

    try:

        # Listening to all the messages
        while True:
            full_msg = ""
            is_new_msg = True

            while True:

                # Receiving the message in small sizes
                msg = s.recv(HEADER_SIZE)

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

                    is_new_msg = True
                    full_msg = ""

    except ConnectionResetError:
        print("[ERROR]: The server has disconnected unexpectedly")
        shutdown = True # TODO: Gestionar que l'usuari escrigui input després de que el servidor s'hagi desconnectat
        # Closing connection
        s.close()
        # TODO: Matar els threads al apagar

        sys.exit()





