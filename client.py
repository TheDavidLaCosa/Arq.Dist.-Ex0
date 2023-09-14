import socket
import threading

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"

if __name__ == "__main__":

    # Connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", u.PORT))

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


