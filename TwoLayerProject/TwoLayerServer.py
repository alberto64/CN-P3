import socket


class UDPServer:

    def __init__(self, server_address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('starting up on {} port {}'.format(*server_address))
        self.sock.bind(server_address)
        self.server_address = server_address

    def recieveMessage(self):
        print('\nwaiting to receive message')
        data, self.server_address = self.sock.recvfrom(4096)
        print('received {} bytes from {}'.format(len(data), self.server_address))
        return data.decode()

    def sendMessage(self, data):
        sent = self.sock.sendto(str.encode(str(data)), self.server_address)
        print('sent {} bytes back to {}'.format(sent, self.server_address))

    def closeConnection(self):
        print('closing socket')
        self.sock.close()


class SAWServer:

    def __init__(self, ip_address):
        self.conn = UDPServer((ip_address, 5000))
        self.divider = '!#$'
        self.memoryQueue = list()
        self.memoryQueue.append(-1)
        self.memoryQueue.append(-1)
        self.memoryQueue.append(-1)
        self.memoryQueue.append(-1)
        self.memoryQueue.append(-1)

    def recieveMessage(self):
        exit = False
        while not exit:
            while True:
                frame = self.conn.recieveMessage()
                if frame != '':
                    splt = frame.split(self.divider)
                    n = int(splt[0])
                    message = splt[1]
                    if n not in self.memoryQueue:
                        print(message)
                        self.memoryQueue.insert(0, n)
                        self.memoryQueue.pop()
                        print(self.memoryQueue)
                    self.conn.sendMessage(n)
                    if message == "exit":
                        exit = True
                    break

    def closeConnection(self):
        self.conn.closeConnection()


server = SAWServer('127.0.0.1')

server.recieveMessage()

server.closeConnection()
