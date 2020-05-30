import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.gethostname()
port = 1234

soc.bind((addr, port))
soc.listen(5)

while True:
    clientsocket, address = soc.accept()
    print(f'Connection from {address} has been established!')
    clientsocket.send(bytes("welcome to the server!", "utf-8"))
    clientsocket.close()
