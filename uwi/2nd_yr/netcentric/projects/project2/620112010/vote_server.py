# Server to implement simplified RSA algorithm and tally votes from a client.
# The server waits for the client to say Hello. Once the client says hello,
# the server sends the client a public key. The client uses the public key to
# send a session key with confidentiality to the server.

# Author:620112010(Stefan Mitchell)
# Last modified:18/11/2020 
# Version: 0.1
#!/usr/bin/python3

import socket
import random
import math
import hashlib
import time
import sys
import simplified_AES
import NumTheory as nt

class RSAServer(object):
    candidate_1=None
    candidate_2=None
    def __init__(self, port, p, q):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port=int(port)
       
         # The option below is to permit reuse of a socket in less than an MSL
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       
       
        self.lastRcvdMsg = None
        self.sessionKey = None		#For storing the symmetric key
        self.modulus = None		#For storing the server's n in the public/private key
        self.pubExponent = None	#For storing the server's e in the public key
        self.privExponent = None	#For storing the server's d in the private key
        self.nonce = None
        self.connected=False
        
        # Call the methods to compute the public private/key pairs
        publickey,privatekey=self.genKeys(p,q)
        self.modulus,self.pubExponent=publickey
        self.modulus,self.privExponent=privatekey
      
        
        try:
            self.socket.bind((socket.gethostname(),self.port))
            print("Socket binding sucessful\n")
        except socket.error:
            print("Socket binding unsucessful\n")
            exit(-1)
            
        self.socket.listen(5)
        self.clientsock, self.addr = self.socket.accept()
       
        
      
        
        

    def send(self, conn, message):
        conn.send(bytes(message,'utf-8'))
        print("sending message to client\n")



    def read(self):

         try:
            data = self.clientsock.recv(4096).decode('utf-8')
         
         except BlockingIOError:
            pass
        
         else:
            if data:
                self.lastRcvdMsg = data
            else:
                raise RuntimeError("Client is unavailable")

                    
            if "101 Hello" in self.lastRcvdMsg:
                    self.send(self.clientsock, self.clientHelloResp())
                    


            if "103 Sessionkey" in self.lastRcvdMsg:
                lst=self.lastRcvdMsg.split("")
                lt2=lst[1:]
                cryptedsesskey=lt2[1]
                cryptednonce=lt2[2]
                decryptedsesskey=self.RSAdecrypt(cryptedsesskey)
                self.sessionKey=decryptedsesskey
                decryptednonce=self.AESdecrypt(cryptednonce)
                verified=self.nonceVerification(decryptednonce)
                if verified==1:
                    self.handlevotes()
                    
                    # add code for collecting candidate list

                elif verified==-1:
                    self.send(self.clientsock,"400 Error")


                        
                
            elif self.lastRcvdMsg=="terminate":
                self.connected=False
            
         
         
         

    def close(self, conn):
        print("closing server side of connection")
        try:
            conn.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f" {repr(e)}",
            )
        finally:
            # Delete reference to socket object
            conn = None    
            
            
    def primecheck(self,num):
            
        if num > 1:
            for x in range(2,num):
                if (num % x) == 0:
                  print("The number entered is not a prime number",num)
                  print("exitting program...")
                  exit(-1) 
            else:
                print(num,"is a prime number")
        else:
         print("The number entered is not a prime number",num) 
         print("exitting program...")
         exit(-1)    
         
         
        
    def handlevotes(self):
	     

         # Add code to initialize the candidates and their IDs
            candidate_1=input("Please the enter the first name of first candidate\n")
            candidate_2=input("Please the enter the first name of second candidate\n")


            Id_list=[]
            first_msg="105 key "+str(self.modulus)+","+str(self.pubExponent)#first message to client
            self.send(self.clientsock,first_msg)
            print(first_msg)

            for k in range(1,3):
                ID=2**(k)
                print("ID:",ID)
                Id_list.append(ID)

            second_msg="106 "+"{ID:"+str(Id_list[0])+":"+candidate_1+"},"+"{ID:"+str(Id_list[1])+":"+candidate_2+"}"+"\n"#first message to client
            print(second_msg)
            self.send(self.clientsock,second_msg)#second message

            third_msg="107 Polls Open"
            self.send(self.clientsock,third_msg)#third message
            
            if "115"in self.lastRcvdMsg:
                #fix properly after fixing client
                result=self.AESdecrypt(self.lastRcvdMsg)
                print(result)
                win_msg="220 The winner was"+candidate_1
                
                self.send(self.clientsock,win_msg)#third message
            
                


         
         
         
         
      
       
        
    def RSAencrypt(self, msg):
        
        """Encryption side of RSA"""
        """"This function will return (msg^exponent mod modulus) and you must"""
        """ use the expMod() function"""   
        
        
        if len(msg)<self.modulus:
            m=0    
            lst=[]
            cstring=" "
            for ctr in msg:
                    m = ord(ctr)
                    cipher=nt.NumTheory.expMod(m,self.pubExponent,self.modulus)
                    lst.append(cipher)
    
            print(lst)
            for x in lst:
                cstring+=str(x)
            
        return cstring
       
        

             
        

    def RSAdecrypt(self, cText):
        """Decryption side of RSA"""
        """"This function will return (cText^exponent mod modulus) and you must"""
        """ use the expMod() function"""
        
        fullmsg=""
        
        for ele in cText:
            m=nt.NumTheory.expMod(int(ele),self.privExponent,self.modulus)
            msg=chr(m)
            fullmsg+=msg
        
        return fullmsg
        
    
    
    

    def AESdecrypt(self, cText):
        """Decryption side of AES"""
        simplified_AES.keyExp(self.sessionKey)
        return simplified_AES.decrypt(cText)

    def AESencrypt(self, plaintext):
        """Computes the simplified AES encryption of some plaintext"""
        simplified_AES.keyExp(self.sessionKey) # Generating round keys for AES.
        ciphertext = simplified_AES.encrypt(plaintext) # Running simplified AES.
        return ciphertext

    def generateNonce(self):
        """This method returns a 16-bit random integer derived from hashing the
            current time. This is used to test for liveness"""
        hash = hashlib.sha1()
        hash.update(str(time.time()).encode('utf-8'))
        self.nonce = int.from_bytes(hash.digest()[:2], byteorder=sys.byteorder)

    def findE(self, phi):
        """Method to randomly choose a good e given phi"""
        
        e=random.randint(1,phi) 
        print("e value is", e) 
        if nt.NumTheory.gcd_iter(e,phi)==1 and e<phi:
                    print("phi and e are relatively prime")
                    return e
        
        else:
             while True:
                    print("Generating new e value")
                    e=random.randint(1,phi)
                    print("e value is",e)
                    
                    if nt.NumTheory.gcd_iter(e,phi)==1 and e<phi:
                        print("phi and e are relatively prime")
                        break
                    
             return e
            
                

    def genKeys(self, p, q):
        """Generates n, phi(n), e, and d"""
        self.primecheck(p)
        self.primecheck(q)
        n=p*q
        phi=(p-1)*(q-1)
        e=self.findE(phi)
        d=self.findD(e,phi)
        publickey=n,e
        privatekey=n,d
        
        print("the value of n is:",n)
        print("the value of d is:",d)
        print("the value of e is:",e)
        print("the value of phi is:",phi)
        print("publickey is",n,e)
        print("privatekey is",n,d)
        
        return publickey,privatekey
    
    
    
    
    def findD(self,e,phi):
        d=nt.NumTheory.ext_Euclid(e,phi)
        print("d value is:",d)
        
        if (e*d)%phi==1:
            return d
        
        else: 
            while False:
                print("generating new value of d")
                print("d value is:",d)
                d=nt.NumTheory.ext_Euclid(e,phi)
                if (e*d)%phi==1:
                    break
        return d
       
    

    def clientHelloResp(self):
        """Generates response string to client's hello message"""
        self.generateNonce()
        status = "102 Hello AES,RSA16"+" "+str(self.modulus)+" "+str(self.pubExponent)+" "+str(self.nonce)
        return status

    def nonceVerification(self, decryptedNonce):
        """Verifies that the transmitted nonce matches that received
        from the client."""
        if self.nonce==decryptedNonce:
            print("Nonce match verified")
            return (1)
        else:
             print("Nonce match unverified")
             return (-1)


    def start(self):
        """Main sending and receiving loop"""
        """You will need to complete this function"""
       
        print("Server is Starting...\n")
       
        print("connected to client:"+str(self.addr))
        while True:
            self.connected=True
            while self.connected:
                 
                self.read()
               
                if self.connected is False:
                        break
            print("End of transmission\n")
            self.close(self.clientsock)
                    
                    
       

def main():
        """Driver function for the project"""
        args = sys.argv
        if len(args) != 2:
            print ("Please supply a server port.")
            sys.exit()
            
        HOST = ''		# Symbolic name meaning all available interfaces
        PORT = int(args[1])     # The port on which the server is listening
        if PORT < 1023 or PORT > 65535:
            print("Invalid port specified.")
            sys.exit()
            
        print ("Enter prime numbers. One should be between 211 and 281, and\
        the other between 229 and 307")
        p = int(input('Enter P: '))
        q = int(input('Enter Q: '))
        
        server = RSAServer(PORT, p, q)
        server.start()

        
        

if __name__ == "__main__":
        main()
