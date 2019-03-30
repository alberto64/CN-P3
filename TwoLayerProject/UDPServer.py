import socket


class UDPServer:

    def __init__(self, server_address, debug):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.debug = debug
        if self.debug:
            print('DEBUG - Starting up on {} port {}'.format(*server_address))
        self.sock.bind(server_address)
        self.server_address = server_address

    def recieveMessage(self):
        if self.debug:
            print('DEBUG - waiting to receive message')
        data, self.server_address = self.sock.recvfrom(4096)
        if self.debug:
            print('DEBUG - received {} bytes from {}'.format(len(data), self.server_address))
        return data.decode()

    def sendMessage(self, data):
        sent = self.sock.sendto(str.encode(str(data)), self.server_address)
        if self.debug:
            print('DEBUG - sent {} bytes back to {}'.format(sent, self.server_address))

    def closeConnection(self):
        if self.debug:
            print('DEBUG - closing socket')
        self.sock.close()
