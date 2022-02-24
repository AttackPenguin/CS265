import select
import socket
import sys

# Get initial connection information from user and attempt connection:
connected = False
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
    sock =


# 1. Perform Handshake
# 1a. Client sends 'HELLO'
# 1b. Server sends 'HELLO'

# 2. Perform Authentication
# 2a. Client sends 'AUTH:<username>:<password>'
# 2b. Waits for two responses from server:
#   'AUTHYES' - only goes to client logging in
#   'SIGNIN:<username>' - goes to all logged in clients
# 2c. Need to handle 'AUTHNO' response, which indicates log in refusal.
# 2d. Need to handle 'UNIQNO' response, indicating user already logged in.

# 3. Present Menu
"""
    1. To send a message, enter 's'.
    2. To list online users, enter 'l'.
    3. To log off, enter 'q'.
"""

# 4. Receive messages. If at any point a message arrives, and the user is
# NOT writing a message (has not selected 1 from menu), display message:
# <sendingusername>: <message>
# If user IS writing a message, block printing received message until user
# has submitted their message, printing received messages before appending
# sent message printout.

# 5. Send messages. If user selects 's', prompt for message, and buffer
# received messages. When carriage return is entered, print buffered
# messages, then print sent message:
# <username>: <message>

# 6. List other users. If user selects 'l', get list of users from server by
# sending 'LIST', then print online users:
#   Online Users:
#       <username1>
#       <username2>
#       ...

# 7. Log off. If user selects 'q', send 'BYE' to server. Exit program with
# exit message.
