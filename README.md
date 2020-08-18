# Wi-Fi API for Central Computer MoonRanger
API prototype for communication and file transfer between MoonRanger Rover and Lander over TCP socket.
![Setup](images/setup.jpg)

### Usage 
```
usage: 1. WiFi_API_Channel_Demo.py [-h] -m MODE -ip SERVER_IP [-rp RECV_PORT] [-sp SEND_PORT] [-bs BUFFER_SIZE]   
       2. WiFi_API_File_Demo.py [-h] -m MODE -ip SERVER_IP [-rp RECV_PORT] [-sp SEND_PORT] [-bs BUFFER_SIZE]
	   
arguments:                                                                                                       
-h, --help            show this help message and exit                                                                  
-m MODE, --mode MODE  MODE: Server or Client                                                                            
-ip SERVER_IP, --server_ip SERVER_IP  SERVER_IP: e.g. 192.168.1.10 or localhost                                                                   
-rp RECV_PORT, --recv_port RECV_PORT  RECEIVE_PORT: e.g. 5051                                                                         
-sp SEND_PORT, --send_port SEND_PORT  SEND_PORT: e.g. 5050                                                                              
-bs BUFFER_SIZE, --buffer_size BUFFER_SIZE  BUFFER_SIZE: e.g. 1024  

-rp,-sp and -bs are optional
```
**Execute the commands in the following Order for File Channel Demo:** 

``` 
1. Start the Server 
2. Start the Client.
3. Select the Receive Files option first on either Server or Client.
4. Send the files via Send files option on the other end.


```
**Note: Check ifconfig on Linux or ipconfig on Windows for the Wi-Fi IP address. Use this IP address as the TCP SERVER_IP** 