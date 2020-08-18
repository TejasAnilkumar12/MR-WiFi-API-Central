# -*- coding: utf-8 -*-
"""
File name:  WiFi_API.py
Created on Thu Aug 13 16:53:23 2020
Description:  MoonRanger Central Computer WiFi API
OS:  Windows or Linux
@author: Tejas Anilkumar P. <tpandara@andrew.cmu.edu>
Carnegie Mellon University
"""

import socket
import sys
from time import *
import argparse
import os


class WiFi_API():
    def __init__(self,server_ip,recv_port,send_port,buffer_size,server):
        self.SERVER_IP = server_ip
        self.RECV_PORT = recv_port
        self.SEND_PORT = send_port
        self.FILE_PORT = 8000
        self.BUFFER_SIZE = buffer_size
        
        #TCP Socket
        self.SERVER_FLAG = server
        self.sock_recv = None
        self.sock_send = None
        self.client_sock_recv = None
        self.client_sock_send = None
        self.file_sock = None
        self.file_sock_client = None
    
        try:
            print("Creating Socket\n")
            #RECEIVE SOCKET
            self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            
            #SEND SOCKET
            self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            
            #FILE SOCKET
            self.file_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.file_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        except socket.error as err:
            print("Creating Socket Failed\n")
            print(err)
            self.sock_recv.close()
            self.sock_send.close()
            self.file_sock.close()
            
        print("Socket Created\n")
        
                
    def startReceiveChannel(self):
        server_recv_address = (self.SERVER_IP,self.RECV_PORT)
        server_send_address = (self.SERVER_IP,self.SEND_PORT)
        
        if self.SERVER_FLAG:    
            print("Server Mode\n")
            print("Server Receive Channel\n")
            self.sock_recv.bind(server_recv_address)
            self.sock_recv.listen(1)
            print("Started Receive Channel at %s:%s\n"%(server_recv_address))
            print("Waiting for Client on Server Receive Channel\n")
            client_sock_send,client_sock_send_addr = self.sock_recv.accept()
            self.client_sock_send = client_sock_send
            print("Client connected to Server Receive Channel %s:%s\n"%(client_sock_send_addr[0],client_sock_send_addr[1]))
        else:
            print("Client Mode\n")
            print("Receive From Server")
            result = self.sock_recv.connect_ex(server_send_address)
            if result == 0:
               print("Connected to Server Send Channel %s:%s\n"%(server_send_address))
            else:
               print("Connecting to Server Send Channel Failed\n")
               self.stop()
    
    def startSendChannel(self):
         server_recv_address = (self.SERVER_IP,self.RECV_PORT)
         server_send_address = (self.SERVER_IP,self.SEND_PORT)
         
         if self.SERVER_FLAG:    
             print("Server Mode\n")
             print("Server Send Channel\n")
             self.sock_send.bind(server_send_address)
             self.sock_send.listen(1)
             print("Started Send Channel at %s:%s\n"%(server_send_address))
             print("Waiting for Client on Server Send Channel\n")
             client_sock_recv,client_sock_recv_addr = self.sock_send.accept()
             self.client_sock_recv = client_sock_recv 
             print("Client connected to Server Send Channel %s:%s\n"%(client_sock_recv_addr[0],client_sock_recv_addr[1]))
         else:
             print("Client Mode\n")
             print("Send to Server")
             result = self.sock_send.connect_ex(server_recv_address)
             if result == 0:
                print("Connected to Server Receive Channel %s:%s\n"%(server_recv_address))
             else:
                print("Connecting to Server Receive Channel Failed\n")
                self.stop()
             
    def startFileChannel(self):
        file_address = (self.SERVER_IP,self.FILE_PORT)
        if self.SERVER_FLAG:
            print("Server Mode\n")
            print("File Channel\n")
            self.file_sock.bind(file_address)
            self.file_sock.listen(1)
            print("Started File Channel at %s:%s\n"%(file_address))
            print("Waiting for Client on File Channel\n")
            file_sock_client,file_sock_client_addr = self.file_sock.accept()
            self.file_sock_client = file_sock_client
            print("Client connected to File Channel %s:%s\n"%(file_sock_client_addr[0],file_sock_client_addr[1]))
        else:
            print("Client Mode\n")
            print("File Channel\n")
            result = self.file_sock.connect_ex(file_address)
            if result == 0:
                print("Connected to File Channel %s:%s\n"%(file_address))
            else:
                print("Connecting to File Channel Failed\n")
                self.stop()
            
            
            
    def receiveData(self):
        if self.SERVER_FLAG:
            data = self.client_sock_send.recv(self.BUFFER_SIZE)
            print("From Client:%s\n"%data)
        else:
            data = self.sock_recv.recv(self.BUFFER_SIZE)
            print("From Server:%s\n"%data)
        
            
    def sendData(self,data):
        if self.SERVER_FLAG:
            self.client_sock_recv.send(data)
        else:
            self.sock_send.send(data)
            
            
    def sendFile(self,file_location):
        if not os.path.isfile(file_location):
            print("File not found/Invalid filename")
        if self.SERVER_FLAG:
            sock = self.file_sock_client
        else:
            sock = self.file_sock
        if(file_location == None):
            file_loc = str(input("Enter File Location: "))
            if not os.path.isfile(file_loc):
                print("File not found/Invalid filename")
        
        print("Sending Start")
        sock.send(b'start')
        ready = sock.recv(5)
        if ready == b'ready':
            print("Socket Ready")
            fileName = os.path.split(file_location)[1]
            fileSize = os.path.getsize(file_location)
            #fileData = f"{fileName}{SEPARATOR}{fileSize}"
            sock.send(fileName.encode())
            recv = sock.recv(7)
            if recv == b'receive': 
                # start sending the file
                print("Sending File")
                with open(file_location, "rb") as f:
                    for _ in range(fileSize):
                        bytes_read = f.read(4096)
                        if not bytes_read:
                        #File Transfer Done
                            break
                        sock.send(bytes_read)
                sock.send("EOF".encode())
                print("File Transfer Done")
        
    def recvFile(self):
        if self.SERVER_FLAG:
            sock = self.file_sock_client
        else:
            sock = self.file_sock
        start = sock.recv(5)
        if start == b'start':
            print("Received Start")
            sock.send(b'ready')
            fileName = sock.recv(20).decode()
            print(fileName)
            sock.send(b'receive')
            done = False
            with open(fileName, "wb") as f:
                while done is not True:
                    bytes_read = sock.recv(4096)
                    if bytes_read[-3:] == b'EOF':
                        print("\nReceived End Character")
                        f.write(bytes_read[:-3])
                        done = True
                        break
                 

                    f.write(bytes_read)
        

        
            
    def stop(self):
        if self.SERVER_FLAG:
            if self.client_sock_recv is not None:
                self.client_sock_recv.close()
            if self.client_sock_send is not None:
                self.client_sock_send.close()
            if self.file_sock_client is not None:
                self.file_sock_client.close()
        if self.file_sock is not None:
            self.file_sock.close()
            
        self.sock_recv.close()
        self.sock_send.close()
        
        sys.exit('\nShutting Down')
       

    
    
    

