import SAWServer

exit = False
server = SAWServer.SAWServer('127.0.0.1', True)

while not exit:
    message = server.recieveMessage()
    print("Recieved: " + message)
    if message == "exit":
        exit = True


server.closeConnection()
