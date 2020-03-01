"""
sample proxy program for Part 2
Computer Networks Spring 2020

"""

from socket import *
from urllib.parse import urlparse
from re import *
import select
import sys
import os
import datetime

BUFF_SIZE = 1024
Port = sys.argv[1]

def sendToServer(serverSocket, request, domain):
    # Send GET request to server socket
    # Does not return anything

    ## Your code here ##
    pass 

def receiveFromServer(serverSocket):
    # Receive message from socket
    # Returns a tuple (body, response header)
    # Uses nonblocking select call (timeout=0)

    ## Your code here ##

    # return body, responseLine
    data = b''
    while True:
        packet = serverSocket.recv(BUFF_SIZE)
        if packet:
            data += packet
        else:
            break
    return data

    

def createProxySocket():
    # Create socket to listen on
    # return socket

    ## Your code here ##
    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(('localhost', int(Port)))
    proxySocket.listen(5)
    return proxySocket

def connectSocket(domain, serverPort):
    # Connect to server
    # Return serverSocket

    ## Your code here ##
    try: 
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((domain , serverPort))
    except:
        return None
    return serverSocket

def checkCache(fileName, path, domain, serverPort):
    # Checks cache for file
    # appends index.html to a request for a directory
    # returns the body and response code from the server
  ## Your code here ##

    # Check if the request exists in cache
    if os.path.exists(fileName):
       ## Your code here ## 
        with open(fileName, "rb") as f:
            ## Your code here ##
            f.read('''Your code here''')
    else:
        ## Your code here ##
        directory = domain + '/' + path 
        if not os.path.exists(directory):
            os.makedirs(directory)
        currentDT = datetime.datetime.now()
        with open(fileName, "wb") as f:
            f.write(str(currentDT) + "\n")
            f.write()
    return body, responseLine

def main():
    # Define server socket address
    serverPort = 80
        # Create proxy socket
    proxySocket = createProxySocket()
    while True:
        clientSocket, clientAddr = proxySocket.accept()  # Accept a connection
        readable, _, _ = select.select([clientSocket], [], [], 0)
        if readable:
            # Receive 1024 bytes from client
            clientMessage = clientSocket.recv(BUFF_SIZE).decode(errors='ignore')
            #print("\nClient message : \n****\n" + clientMessage + "\n****\n" )

            # Parse requests
            request2 = clientMessage.split("\r\n")
            referer = None 
            request = clientMessage.split(" ")[1]  # first line is "GET /path HTTP/1.0\r\n" so we want /path/
            request = 'http:/' + request
            url = urlparse(request)

            domain = url.netloc
            path = url.path

            serverSocket = connectSocket(domain, 80)

            #handle server socket error 
            if serverSocket == None: 
                resp = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'
                clientSocket.sendall(resp.encode())
                clientSocket.close()
                continue 

            request_status = 0
                
            request_to_send = "GET {path} HTTP/1.0\r\n\r\n".format(path=path)
            serverSocket.sendall(request_to_send.encode())
            modifiedSentence = receiveFromServer(serverSocket)
            solve = modifiedSentence.partition(b'\r\n\r\n')[1]
            solve = solve.partition(b'\r\n')[0]

            resp = modifiedSentence.decode('utf-8', 'ignore')
            headers = modifiedSentence.partition(b'\r\n\r\n')[0]
            headers = headers.decode()
            print(headers.split(' ')[1] == '301')
            if headers.split(' ')[1] == '301': 
                headers = headers.split('\r\n')
                for item in headers: 
                    if item.split(' ')[0] == "Location:": 
                        new_path = item.split(' ')[1]
                        print(new_path)
                        parse = urlparse(new_path)
                        print(parse.path)
                        serverSocket = connectSocket(parse.netloc, 80)
                        #handle server socket error 
                        if serverSocket == None: 
                            resp = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'
                            clientSocket.sendall(resp.encode())
                            clientSocket.close()
                        request_to_send = "GET {path} HTTP/1.0\r\n\r\n".format(path=parse.path)
                        serverSocket.sendall(request_to_send.encode())
                        modifiedSentence = receiveFromServer(serverSocket)
                        solve = modifiedSentence.partition(b'\r\n\r\n')[1]
                        solve = solve.partition(b'\r\n')[0]
                        resp = modifiedSentence.decode('utf-8', 'ignore')
            print("check completed")
            print(headers)
            resp = resp.split('\r\n\r\n')[1]

                    
            ## Your code here ##
            if 'jpg' in path.split('.') or 'jpeg' in path.split('.') or 'png' in path.split('.'):
                content_type = "image/webp"
                clientSocket.sendall(modifiedSentence)
            else: 
                content_type = "text/html"
                resp = 'HTTP/1.0 200 OK\r\nContent-Length: {length}\r\nContent-Type: {type}; charset=UTF-8\r\n\r\n{sentence}\r\n'.format(
                    length=len(resp.encode()),sentence=resp, type=content_type)
                clientSocket.sendall(resp.encode())
            #body, responseLine = checkCache(sysPath, path, domain, serverPort)
            # Send data back to client​
            #            ## Your code here ##

            clientSocket.close()  # close socket to wait for new request
        else:
            # Or other error handling 
            clientSocket.close()

    proxySocket.close()

if __name__ == "__main__":
    main()
