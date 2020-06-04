import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.gethostbyname("192.168.11.81")
print(addr)
port = 1234

soc.connect((addr, port))

full_msg = ''
while True:
    # the 1024 is a buffer
    msg = soc.recv(8)
    if len(msg) <= 0:
        break
    full_msg += msg.decode('utf-8')

print(full_msg)
