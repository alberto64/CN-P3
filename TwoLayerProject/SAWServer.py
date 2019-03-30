import UDPServer



class SAWServer:

    def __init__(self, ip_address, debug):
        self.debug = debug
        self.conn = UDPServer.UDPServer((ip_address, 5000), debug)
        self.divider = '!#$'
        self.memoryQueue = list()
        for i in range(0, 10):
            self.memoryQueue.append(-1)

    def recieveMessage(self):
        while True:
            print("\nListening for Client message.\n")
            frame = self.conn.recieveMessage()
            if frame != '':
                splt = frame.split(self.divider)
                n = int(splt[0])
                self.conn.sendMessage(n)
                message = splt[1]
                if n not in self.memoryQueue:
                    self.memoryQueue.insert(0, n)
                    self.memoryQueue.pop()
                    if self.debug:
                        print('DEBUG - {}'.format(self.memoryQueue))
                    return message
                if self.debug:
                    print('DEBUG - Repeated Package')

    def closeConnection(self):
        self.conn.closeConnection()
