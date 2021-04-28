#!/usr/bin/python3
import socket
import os
import time
import fileinput
from ssh2.session import Session  #@UnresolvedImport in eclipse

class ssh_session:
    def __init__(self,user, password, host = "localhost",port=22):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self.s = Session()
        self.s.handshake(sock)
        self.s.userauth_password(user, password)        
        self.chan = self.s.open_session()
        self.chan.pty()
        self.chan.shell()
        self.s.set_blocking(True)  #switch to non-blocking
        self.received_bytes=0

    def read(self,minwait=0.5):   #10 ms wait are enough for localhost  
        buf = b""                  #when you send simple commands
        startread=time.time()
        while True:
            size, data = self.chan.read()
            #if size < 0:
            #  time.sleep(0.01)
            #  continue
            #else:    
            #  print("Size:",size,"DATA:",data.decode())
            if size > 0: 
                buf+=data
                self.received_bytes+=size
                time.sleep(0.01)
            if minwait > 0:  # if we have a larger minwait than wait
                timedelta = time.time()-startread
                if timedelta > minwait: 
                    break    
            else:
                break  # non-blocking return with zero minwait
            #repeat the while loop until minwait       
        return (buf.decode())      
                     
    def write(self,cmd):
        self.chan.write(cmd+"\n")       

user="ap"
passwd="#cisco09"
contime = time.time()    
timedelta = 0            
con1 = ssh_session(user,passwd)   #create connection instance

#skip banner aka os welcome message
#banner should be done after 1 second or more than 200 received Bytes
while timedelta < 0.5 and con1.received_bytes < 200:
    timedelta = time.time() - contime
    print(con1.read())   #just read but do not print
      
#send command to host
for line in fileinput.input():
  con1.write(line)
#  ans = con1.read(0.1)   #you can pass a minimum wait time in seconds here
#  print("Answer:" ,ans)

#receive answer, on localhost connection takes just about 0.3ms
                      #e.g. con1.read(0.8) # wait 0.8 seconds
