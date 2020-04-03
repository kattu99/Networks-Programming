"""
sample proxy program for Part 2
Computer Networks Spring 2020

"""

from socket import *
import threading
from urllib.parse import urlparse
from re import *
import select
import sys
import os
import datetime

BUFF_SIZE = 1024
Port = sys.argv[1]


# ---- UTIL ----- # 
def parse_url(url):
    if 'http://' in url:
        url_list = url.split("/", 3)
        if (len(url_list) < 4):
            return None, None
        return url_list[2], url_list[3]
    else: 
        url_list = url.split("/", 2)
        if (len(url_list) < 3):
            return None, None
        return url_list[1], url_list[2]

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

def checkCache(fileName, path, domain, serverPort, isFile=False):
    # Checks cache for file
    # appends index.html to a request for a directory
    # returns the body and response code from the server
  ## Your code here ##
    # Check if the request exists in cache
    if os.path.exists(fileName):
       ## Your code here ## 

        if os.path.isdir(fileName):
            fileName += '/index.html'
        with open(fileName, "rb") as f:
            ## Your code here ##
            body = f.read()
            body = body.partition(b'\r\n')[2]
            responseCode = 200
            return body, responseCode
    else:
        ## Your code here ##
        serverSocket = connectSocket(domain, 80)
        if serverSocket == None: 
            return None, 404
        request_to_send = "GET {path} HTTP/1.0\r\n\r\n".format(path=path)
        serverSocket.sendall(request_to_send.encode())
        modifiedSentence = receiveFromServer(serverSocket)

        resp = modifiedSentence.decode('utf-8', 'ignore')
        headers = modifiedSentence.partition(b'\r\n\r\n')[0]
        headers = headers.decode()
        redirect = False
        if headers.split(' ')[1] == '301': 
            headers = headers.split('\r\n')
            for item in headers: 
                if item.split(' ')[0] == "Location:": 
                    new_path = item.split(' ')[1]
                    domain, path = parse_url(new_path)
                    path = '/' + path
                    serverSocket = connectSocket(domain, 80)
                    #handle server socket error 
                    if serverSocket == None: 
                        return None, 404
                    request_to_send = "GET {path} HTTP/1.0\r\n\r\n".format(path=path)
                    serverSocket.sendall(request_to_send.encode())
                    modifiedSentence = receiveFromServer(serverSocket)
                    redirect = True
            

        directory = domain + '/' + path 
        if redirect: 
            fileName = directory + 'index.html'
            directory = directory.rsplit('/', 1)[0]
        elif isFile: 
            directory = directory.rsplit('/', 1)[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        currentDT = datetime.datetime.now()
        with open(fileName, "wb") as f:
            time_string = str(currentDT) + "\r\n"
            if 'jpg' in path.split('.') or 'jpeg' in path.split('.') or 'png' in path.split('.'):
                f.write(time_string.encode())
                f.write(modifiedSentence)
                return modifiedSentence, 200
            else: 
                f.write(time_string.encode())
                f.write(modifiedSentence.partition(b'\r\n\r\n')[2])
        responseCode = 200
        return modifiedSentence.partition(b'\r\n\r\n')[2], responseCode


class ClientThread(threading.Thread):
    def __init__(self,clientsocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientsocket
    
    def run(self):
        serverPort = 80
        readable, _, _ = select.select([self.clientSocket], [], [])
        if readable:
            # Receive 1024 bytes from client
            clientMessage = self.clientSocket.recv(BUFF_SIZE).decode(errors='ignore')
            #print("\nClient message : \n****\n" + clientMessage + "\n****\n" )

            # Parse requests
            request2 = clientMessage.split("\r\n")
            referer = None 
            if len(clientMessage.split(" ")) <= 2:
                self.clientSocket.close()
                return
            request = clientMessage.split(" ")[1]  # first line is "GET /path HTTP/1.0\r\n" so we want /path/
            domain, path = parse_url(request)
            if domain == None:
                self.clientSocket.close()
                return
            path = '/' + path
            isFile = False
            if len(path) > 0 and path[-1] == "/":
                fileName = './' + domain + path + 'index.html'
            else: 
                isFile = True
                fileName = './' + domain + path 

            body, responseCode = checkCache(fileName, path, domain, serverPort, isFile)
            if body == None:
                self.clientSocket.close()
                return 
 
            ## Your code here ##
            if 'jpg' in path.split('.') or 'jpeg' in path.split('.') or 'png' in path.split('.'):
                self.clientSocket.sendall(body)
            else: 

                content_type = "text/html"
                resp = 'HTTP/1.0 200 OK\r\nContent-Length: {length}\r\nContent-Type: {type}; charset=UTF-8\r\n\r\n{sentence}\r\n'.format(
                    length=len(body),sentence=body.decode('utf-8', 'ignore'), type=content_type)
                self.clientSocket.sendall(resp.encode())
            # Send data back to client​
            #            ## Your code here ##

            self.clientSocket.close()
        else:
            # Or other error handling 
            clientSocket.close()



def main():
    # Define server socket address
    serverPort = 80
        # Create proxy socket
    proxySocket = createProxySocket()
    while True:
        clientSocket, clientAddr = proxySocket.accept()  # Accept a connection

        newthread = ClientThread(clientSocket)
        newthread.start()
          # close socket to wait for new request

    proxySocket.close()

if __name__ == "__main__":
    main()
