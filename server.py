import queue
import socket
import threading
import time

import utils as u

HEADER_SIZE = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISC"

shared_variable = 50

broadcast_users = []

actions=[]
action_cliens=[]


def read(client):
    print("Read")
    txt = format_message(str(shared_variable))
    send(client, txt)


def update(value):
    print("Update")

    shared_variable = value

    print(f"{type(value)} {value}")

    try:
        value = int(value) + 2

    except ValueError:
        print("ERROR int")
    # Sending message to all the clients
    for u in broadcast_users:
        print(u[0])
        send(u[0], f'{str(value)}')


# Function that adds the header to the message
def format_message(text):

    text = f'{len(text):<{HEADER_SIZE}}' + text
    return text


# Function that decodes the received message

# Function that adds a user to the user list
def add_user(user):
    broadcast_users.append(user)


# Function that deletes a user from the user list
def delete_user(user):
    broadcast_users.remove(user)


def send(client, message):
    client.send(message.encode(FORMAT))


# Funtion that handles multiple clients
def process_mesg(mesg, client):

    actions.extend(str(mesg).rstrip("&").split("&"))

    for i in str(mesg).rstrip("&").split("&"):
        action_cliens.append(client)

    action_cliens.append(client)
def broadcast():
    pass


def handle_action():

    global shared_variable

    while True:
        if len(actions) > 0:

            action = actions.pop(0)
            #print(f"ACTION: {action}")

            print(f'{4-len(actions)}:{action}')

            if action == "r": # READ

                read(action_cliens.pop(0))

                #act_c.send(str(shared_variable).encode(FORMAT))
            else: # UPDATE

                try:
                    shared_variable = int(action)
                    action_cliens.pop(0)
                    broadcast()
                except ValueError:
                    print("[ERROR]: Unable to update value")

            print(len(action_cliens))

            # TODO: registrar usuaris en llista

            # Deleting the first user who requested an action


def handle_client(client, address):

    while True:
        mesg = (client.recv(100)).decode(FORMAT)
        print("\""+mesg+"\"")
        process_mesg(mesg, client)


if __name__ == "__main__":

    # Server creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", u.PORT))
    s.listen(5)

    # Initial message
    print(" ----------------------------\n"
          "|           SERVER           |\n"
          " ----------------------------\n\n")

    action_thread = threading.Thread(target=handle_action, args=())
    action_thread.start()

    # Listening loop
    while True:
        # Accept connection
        client, address = s.accept()

        # Keep the client conncted
        handle_thread = threading.Thread(target=handle_client, args=(client, address))
        handle_thread.start()

        print(f'Connection nº{threading.active_count() - 1}: {address[1]}')  # TODO: Fer que s'incrementi i es decrementi quan entra i s'envà o solament incrementar?

        add_user((client, address[1]))

        #message = format_message("Hola!")

        # Sending information to the client
        #send(client, message)

        # TODO: Gestionar enviament a clients no existens (al fer broadcast)
        #print(broadcast_users)
