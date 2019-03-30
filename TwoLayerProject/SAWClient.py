import UDPClient
import multiprocessing


class SAWClient:

    def __init__(self, ip_address, debug):
        self.conn = UDPClient.UDPClient((ip_address, 5000), debug)
        self.debug = debug
        self.index = 0
        self.indexLimit = 20
        self.divider = '!#$'
        self.timeOutTime = 3

    def sendMessage(self, message):
        frame = str(self.index) + self.divider + message
        replied = False
        timeOutLimit = 10
        pool = multiprocessing.Pool(processes=1)
        result = pool.apply_async(self.conn.recieveMessage, ())
        while not replied:
            self.conn.sendMessage(frame)
            try:
                acknowledge = result.get(timeout=self.timeOutTime)
                if self.debug:
                    print('DEBUG - Reply: ' + acknowledge)
                if acknowledge == str(self.index):
                    replied = True
                    self.index = (self.index + 1) % self.indexLimit
                    if self.debug:
                        print("DEBUG - Acknowledgement Received")
            except multiprocessing.context.TimeoutError:
                if self.debug:
                    print('DEBUG - Acknowledgement Not Received, Timed Out')
                timeOutLimit = timeOutLimit - 1
                if timeOutLimit == 0:
                    if self.debug:
                        print('ERROR - Connection Lost')
                    return False

        return True

    def closeConnection(self):
        self.conn.closeConnection()
