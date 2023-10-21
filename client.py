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
using_variable=False



# Function that generates the structure of the message
def format_action(mode, value):

    if value:
        text = f'{value}'
    else:
        text = f'{str(mode):<{1}}'
    return text + "&"


def read():

    global sock
    global shared_value
    global using_variable

    # Waiting for the variable to be free
    while True:
        if using_variable:
            print("Wait")
            continue

        print("Read")
        using_variable = True

        txt = format_action("r", "")
        sock.send(txt.encode(FORMAT))

        using_variable = False
        break

    return shared_value


def update(value):

    global sock
    global shared_value
    global using_variable

    # Waiting for the variable to be free
    while True:
        if using_variable:
            print("Wait")
            continue

        print("Update")
        using_variable = True

        shared_value = value
        txt = format_action("u", value)
        sock.send(txt.encode(FORMAT))

        print(f"Send: {txt}")

        using_variable = False
        break




# Function that controls the user input
def recieve_messages(sock):

    global shared_value

    # Read inicial per a tenir el valor actual del servidor
    read()

    while True:
        length = sock.recv(HEADER_SIZE)
        mesg=sock.recv(int(length))

        try:
            shared_value = int(mesg)
            print(f'Received: {int(mesg)} -> mes: \'{mesg}\'')
        except ValueError:
            print(f"Transmission error, message recieved: {mesg}")

            arr = str(mesg).strip("\'").split(' ')
            mida = len(arr)

            shared_value = int(arr[mida - 1])



if __name__ == "__main__":

    # Connection to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", u.PORT))

    # Watch for client input
    thread = threading.Thread(target=recieve_messages, args=(sock,))
    thread.start()

    time.sleep(3) # Temps d'espera per que el primer read es faci be i aixi evitar que es faci un update abans del que toca

    try:

        while True:

            valor = read()
            update(valor + 1)


            time.sleep(1)


    except ConnectionResetError:
        print("[ERROR]: The server has disconnected unexpectedly")
        shutdown = True  # TODO: Gestionar que l'usuari escrigui input després de que el servidor s'hagi desconnectat (peta)
        # Closing connection
        sock.close()
        # TODO: Matar els threads al apagar

        sys.exit()





