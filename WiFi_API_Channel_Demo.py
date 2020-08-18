# -*- coding: utf-8 -*-
"""
File name:  WiFi_API_Channel_Demo.py
Created on Thu Aug 13 16:53:23 2020
Description:  MoonRanger Central Computer WiFi API Send and ReceiveChannel Usage
OS:  Windows or Linux
@author: Tejas Anilkumar P. <tpandara@andrew.cmu.edu>
Carnegie Mellon University
"""


from WiFi_API_Central import WiFi_API
import argparse
import socket
import threading


def initParser():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode",required=True,help="MODE: Server or Client")
    parser.add_argument("-ip","--server_ip",required=True,help="SERVER_IP: e.g. 192.168.1.10")
    parser.add_argument("-rp","--recv_port",default = 5051,help="RECEIVE_PORT: e.g. 5051")
    parser.add_argument("-sp","--send_port",default = 5050,help="SEND_PORT: e.g. 5050")
    parser.add_argument("-bs","--buffer_size",default = 4096,help="BUFFER_SIZE: e.g. 1024")
    args = parser.parse_args()

#Main
initParser()
server_flag = False
if args.mode == "Server":
    server_flag = True
    
obj = WiFi_API(args.server_ip,args.recv_port,args.send_port,args.buffer_size,server_flag)
if args.mode == "Server":
    threading.Thread(target=obj.startReceiveChannel(),args=()).start()
    threading.Thread(target=obj.startSendChannel(),args=()).start()
elif args.mode == "Client":
    threading.Thread(target=obj.startSendChannel(),args=()).start()
    threading.Thread(target=obj.startReceiveChannel(),args=()).start()
    
    
count = 0
try:
    while True:
        data = "A" + str(count)
        threading.Thread(target=obj.sendData(data.encode()),args=()).start()
        threading.Thread(target=obj.receiveData(),args=()).start()
        count+=1
except KeyboardInterrupt:
    obj.stop()
