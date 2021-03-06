import fcntl
import os
import selectors
import socket
import sys

sel = selectors.DefaultSelector()


def print_options():
    print("\nChoose an option:\n"
          "1. List online users\n"
          "2. Send someone a message\n"
          "3. Sign off\n")


# Get initial connection information from user and attempt connection:
connected = False
sock = None
while not connected:
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
        sys.exit(0)
    sock.sendall(f"AUTH:{user_name}:{password}\n".encode())
    response = sock.recv(1024).decode()
    if response != 'AUTHYES\n':
        print("Incorrect username and/or password.")
    else:
        response = sock.recv(1024)
        print("You are now authenticated.")
        print_options()
        connected = True


def process_response(response: str):
    if response.startswith('SIGNIN'):
        print(f"\n{response[8:-1]} Signed In\n")
    elif response.startswith('SIGNOFF'):
        print(f"\n{response[9:-1]} Signed Out\n")
    elif response.startswith('From'):
        subs = response.split(':')
        print(f"\nMessage from {subs[1]}: {subs[2][0:-1]}\n")
    else:
        print(f"\nUnhandled response from server:\n"
              f"{response}\n")


def get_server_message(sock):
    response = sock.recv(1024).decode()
    process_response(response)


continue_listening = True


def get_user_input(user_input):
    user_input = user_input.read()
    print(user_input)
    if user_input == '1\n':
        # Get and print list of online users
        sock.sendall("LIST\n".encode())
        while True:
            response = sock.recv(1024).decode()
            print(response)
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
        print_options()
    if user_input == '2\n':
        sel.unregister(sock)
        sel.unregister(sys.stdin)
        print("Enter user you would like to message:")
        user = input()
        print('Message:')
        message = input()
        sock.sendall(
            f"To:{user}:{message}"
        )
        print("Message sent.\n")
        print_options()
        sel.register(sock, selectors.EVENT_READ, get_server_message)
        sel.register(sock, selectors.EVENT_READ, get_server_message)
    if user_input == '3\n':
        print('Signing off...')
        sock.send('BYE'.encode())
        sel.unregister(sock)
        sel.unregister(sys.stdin)
        sock.close()
        sys.exit(0)
    else:
        print("Input not recognized.\n")
        print_options()


sel.register(sock, selectors.EVENT_READ, get_server_message)
sel.register(sys.stdin, selectors.EVENT_READ, get_user_input)

# I cannot figure out how to do this with os.set_blocking, and I'm tired,
# so I'm just accessing the nix functionality via fcntl. Not great for
# portability, I know.
fcntl.fcntl(
    sys.stdin, fcntl.F_SETFL,
    fcntl.fcntl(sys.stdin, fcntl.F_GETFL) | os.O_NONBLOCK
)

while continue_listening:
    for key, mask in sel.select():
        callback = key.data
        callback(key.fileobj)
