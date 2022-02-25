import fcntl
import os
import select
import selectors
import socket
import sys


def print_options():
    print("\nChoose an option:\n"
          "1. List online users\n"
          "2. Send someone a message\n"
          "3. Sign off\n")


# Get initial connection information from user and attempt connection:
sock = None
while "The Stars Still Shine":
    hostname = input(
        "Please enter the server hostname or IPv4 address: "
    )
    port_num = input(
        "Please enter the server port number: "
    )
    user_name = input(
        "Please enter a username: "
    )
    password = input(
        "Please enter a password: "
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # I'm assuming the user will enter the correct host name and port number
    # for purposes of this exercise.
    sock.connect((hostname, int(port_num)))
    sock.sendall("HELLO\n".encode())
    response = sock.recv(1024).decode()
    if response != "HELLO\n":
        print(f"Client did not correctly respond to handshake.\n"
              f"Client response: {response}")
        sys.exit(1)
    sock.sendall(f"AUTH:{user_name}:{password}\n".encode())
    response = sock.recv(1024).decode()
    if response == "UNIQNO\n":
        print(f"This user is already logged into the server.")
        continue
    elif response == 'AUTHNO\n':
        print("Incorrect username and/or password.")
        continue
    elif response == 'AUTHYES\n':
        print("You are now authenticated.")
        print_options()
        break
    else:
        print(f"Unhandled response received: {response}")
        sys.exit(1)


def process_response(response: str):
    if response is None or response == '':
        pass
    elif response.startswith('SIGNIN'):
        if not response[7:-1] == user_name:
            print(f"\n{response[7:-1]} Signed In\n")
    elif response.startswith('SIGNOFF'):
        print(f"\n{response[8:-1]} Signed Out\n")
    elif response.startswith('From'):
        subs = response.split(':')
        print(f"\nMessage from {subs[1]}: {subs[2][0:-1]}\n")
    else:
        print(f"\nUnhandled response from server:\n"
              f"{response}\n")


def get_server_message():
    response = sock.recv(1024).decode()
    process_response(response)


continue_listening = True


def get_user_input():
    user_input = sys.stdin.readline()
    if user_input == '1\n':
        # Get and print list of online users
        sock.sendall("LIST\n".encode())
        while True:
            response = sock.recv(1024).decode()
            if (
                    response.startswith('SIGNIN') or
                    response.startswith('SIGNOFF') or
                    response.startswith('From')
            ):
                process_response(response)
            else:
                print("Users currently logged in:")
                users = response.split(', ')
                for user in users:
                    print(f'  {user}')
                break
    elif user_input == '2\n':

        print("Enter user you would like to message:")
        user = sys.stdin.readline()
        print('Message:')
        message = sys.stdin.readline()
        sock.sendall(
            f"To:{user}:{message}".encode()
        )
        print("Message sent.\n")

    elif user_input == '3\n':
        print('Signing off...')
        sock.sendall('BYE\n'.encode())
        sock.close()
        sys.exit(0)
    else:
        print("Input not recognized.\n")
    print_options()


# I cannot figure out how to do this with os.set_blocking, and I'm tired,
# so I'm just accessing the nix functionality via fcntl. Not great for
# portability, I know.
# fcntl.fcntl(
#     sys.stdin, fcntl.F_SETFL,
#     fcntl.fcntl(sys.stdin, fcntl.F_GETFL) | os.O_NONBLOCK
# )

while "The Wind Still Blows":
    readable, _, _ = select.select([sock, sys.stdin], [], [])
    if sys.stdin in readable:
        get_user_input()
    if sock in readable:
        get_server_message()
