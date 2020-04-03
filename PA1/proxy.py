from socket import socket,AF_INET, SOCK_STREAM
import sys

BUFF_SIZE = 1024
serverPort = int(sys.argv[1])
serverAddr = ''
serverName = 'localhost'
ourSocket = socket(AF_INET, SOCK_STREAM)
ourSocket.connect(('localhost', 8080))
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(5)
print("listening on localhost")

while True: 
    clientSocket, clientAddr = serverSocket.accept()
    try:
        message = clientSocket.recv(BUFF_SIZE).decode()
        test = message.split()[1][1:]
        ourSocket.sendto(test.encode(), (serverName, serverPort))
        modifiedSentence = ourSocket.recv(1024).decode()
        print("Message from server: ",modifiedSentence)
        resp = 'HTTP/1.0 200 OK\r\nContent-Length: {length}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n{sentence}\r\n'.format(length=len(modifiedSentence.encode()),sentence=modifiedSentence)
        clientSocket.sendall(resp.encode())
        print("Message to client: ", modifiedSentence)
        clientSocket.close()
    except Exception as inst:
        print("Exception")
        print(inst)
        clientSocket.close()
        print("Connection closed")
        break

serverSocket.close()
