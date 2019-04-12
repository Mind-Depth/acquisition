def print_message(message, socket=None):
    print("MESSAGE: " + message)
    if (socket):
        socket.send(message.encode())

def print_error(message, socket=None):
    print("ERROR: " + message)
    if (socket):
        socket.send(message.encode())