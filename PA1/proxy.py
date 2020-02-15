from socket import socket,AF_INET, SOCK_STREAM
BUFF_SIZE = 1024
serverPort = 5000
serverAddr = ''
ourSocket = socket(AF_INET, SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)
ourSocket.connect(('localhost', 8888))

serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(5)
print("listening on localhost")

while True: 
    clientSocket, clientAddr = serverSocket.accept()
    while True:
        try:
            message = clientSocket.recv(BUFF_SIZE).decode()
            if message:
                print("Message from client: ", message)

                message = message.upper()
                clientSocket.send(message.encode())
                print("Message to client: ", message)
            else:
                readable, writable, errorable = select([],[], [clientSocket])
                for s in errorable:
                    s.close()
                break
        except:
            clientSocket.close()
            print("Connection closed")
            break

ServerSocket.close()