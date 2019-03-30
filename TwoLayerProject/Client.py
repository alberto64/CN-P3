import SAWClient

exit = False
client = SAWClient.SAWClient('127.0.0.1', True)

while not exit:
    message = input("\nSend message:")
    print('')
    success = client.sendMessage(message)
    if message == "exit" or not success:
        exit = True

client.closeConnection()