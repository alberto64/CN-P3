import multiprocessing
import socket
import random
import threading


class UDPClient:

    def __init__(self, server_address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_address

    def sendMessage(self, message):
        print('sending {!r}'.format(message))
        if random.randint(0, 5) == 0:
            print('\nData did not send!')
        else:
            if random.randint(0, 10) == 0:
                print('\n Sent data twice!')
                self.sock.sendto(str.encode(message), self.server_address)
            self.sock.sendto(str.encode(message), self.server_address)

    def recieveMessage(self):
        print('waiting to receive')
        data, server = self.sock.recvfrom(4096)
        print('received {!r}'.format(data))
        return data.decode()

    def closeConnection(self):
        print('closing socket')
        self.sock.close()


class SAWClient:

    def __init__(self, ip_address):
        self.conn = UDPClient((ip_address, 5000))
        self.index = 0
        self.indexLimit = 10
        self.divider = '!#$'
        self.timeOutTime = 3

    def sendMessage(self, message):
        frame = str(self.index) + self.divider + message
        replied = False
        timeOutLimit = 10
        while not replied:
            self.conn.sendMessage(frame)
            pool = multiprocessing.Pool(processes=1)
            result = pool.apply_async(self.conn.recieveMessage, ())
            try:
                acknowledge = result.get(timeout=self.timeOutTime)
                print('Reply: ' + acknowledge)
                if acknowledge == str(self.index):
                    replied = True
                    self.index = (self.index + 1) % self.indexLimit
                    print("\nAcknowledgement Received")
                    break
            except multiprocessing.context.TimeoutError:
                print('\nAcknowledgement Not Received, Timed Out')
                timeOutLimit = timeOutLimit - 1
                if timeOutLimit == 0:
                    return False

        return True

    def closeConnection(self):
        self.conn.closeConnection()

exit = False
client = SAWClient('127.0.0.1')


while not exit:
    message = input("Send message:")

    success = client.sendMessage(message)
    if message == "exit" or not success:
        exit = True

client.closeConnection()
