import socket
import random


class UDPClient:

    def __init__(self, server_address, debug):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_address
        self.debug = debug

    def sendMessage(self, message):
        if random.randint(0, 5) == 0:
            if self.debug:
                print('\nDEBUG - Data did not send!')
            return False
        else:
            if self.debug:
                print('\nDEBUG - Sending {!r}'.format(message))
            #if random.randint(0, 10) == 0:
            if self.debug:
                print('DEBUG - Sent data twice!')
            self.sock.sendto(str.encode(message), self.server_address)
            self.sock.sendto(str.encode(message), self.server_address)
            return True

    def recieveMessage(self):
        if self.debug:
            print('DEBUG - waiting to receive')
        data, server = self.sock.recvfrom(4096)
        if self.debug:
            print('DEBUG - received {!r}'.format(data))
        return data.decode()

    def closeConnection(self):
        if self.debug:
            print('DEBUG - closing socket')
        self.sock.close()
        return True
