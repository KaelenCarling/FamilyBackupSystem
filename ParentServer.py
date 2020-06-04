import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = '192.168.11.121'
port = 1234

soc.bind((addr, port))
soc.listen(5)

while True:
    clientsocket, address = soc.accept()
    print(f'Connection from {address} has been established!')
    clientsocket.send(bytes(
        "˙ɐnbᴉlɐ ɐuƃɐɯ ǝɹolop ʇǝ ǝɹoqɐl ʇn ʇunpᴉpᴉɔuᴉ ɹodɯǝʇ poɯsnᴉǝ op pǝs 'ʇᴉlǝ ƃuᴉɔsᴉdᴉpɐ ɹnʇǝʇɔǝsuoɔ 'ʇǝɯɐ ʇᴉs ɹolop ɯnsdᴉ ɯǝɹo˥00˙Ɩ$-̭̗̮",
        "utf-8"))
    clientsocket.close()
