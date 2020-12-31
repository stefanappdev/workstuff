# Client to implement simplified 'secure' electronic voting algorithm
# and send votes to a server

# Author: 
# Last modified: 2020-10-07
# Version: 0.1.1
#!/usr/bin/python3

import socket
import random
import math
import sys
FORMAT='utf-8'

class NumTheory:
    
        @staticmethod 
        def expMod(b,n,m):
                """Computes the modular exponent of a number"""
                """returns (b^n mod m)"""
                if n==0:
                    return 1
                elif n%2==0:
                    return NumTheory.expMod((b*b)%m, n/2, m)
                else:
                    return(b*NumTheory.expMod(b,n-1,m))%m


        
class PaillierClientSocket:
        
        def __init__(self, host, port):
        # Add code to initialize this class.
                self.host=host #host ip for client
                self.port=port #port for client
                self.sock=None #empty socket for client

                self.start_client(host,port)
            
       #function for starting client 
        def start_client(self,host,port):
            
             try:    
                 
                print("Client of Stefan Mitchell\n") 
                self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                print("socket creation sucessful\n")
                
                print("Connecting to server...\n")  
                self.sock.connect((host,port))
                 
                while True:
                        
                        self.contact_server()

                        if False:
                            print("Unable to connect to server,please try again\n")  
                            exit(-1)

             except socket.error:
                        print("socket creation failed or has been closed\n")
                        exit(-1)
             
        #function to connect client to server
        def contact_server(self):
                   
                    self.comm()

                   
                        
                    

      #send message into the socket
            

        def mysend(self, msg):
    
                data=str(msg)
                self.sock.send(data.encode(FORMAT))
                print("Sending message to server....\n")

         

         # function to read data from the socket(unused function)
        def myreceive(self):
            msg=self.sock.recv(200)
            full_msg=""
            while True:
                if len(msg)<=0:
                    break
                full_msg+=msg.decode(FORMAT)
                print("From Server:" +full_msg+"\n")

    

        def comm(self):

            connected=True
            self.mysend("100 Hello")
            while connected==True:

             #this section formats the message from client 
             msg=self.sock.recv(200)#incoming message from server 
             full_msg=""

             full_msg+=msg.decode(FORMAT)
             print("From Server:" +full_msg+"\n")
             
             if full_msg=="107 Polls Open":
                   self.ProcessMsgs()
             
             
             if full_msg=="terminate":
                    break

            self.sock.close()
            print("Disconnected from server\n")  #closes client connection to server
                        
                          
        def ProcessMsgs(self):

          vote=input("Which candidate do you want to elect? ")
          i=int(input("Please enter candidate ID:"))
          n=int(input("Value of n from 105 message: "))
          g=int(input("Value of g from 105 message: "))

          r=random.randint(0,n)
          a=g**i
          b=r**n
          scrambled_vote=(a*b)%(n**2)
          arr=[]
          arr.append(scrambled_vote)
          
          self.mysend(arr)

              
         
         


'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print ("Please supply a server address and port.")
        sys.exit()
    serverHost = str(args[1])       # The remote host
    serverPort = int(args[2])       # The same port as used by the server
    
    print("Client of ____")
    c = PaillierClientSocket(serverHost, serverPort)
