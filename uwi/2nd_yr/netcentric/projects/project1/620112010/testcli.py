from PaillierClientSocket import PaillierClientSocket as pc
from PaillierServerSocket import PaillierServerSocket as ps
import socket

client= pc(socket.gethostname(),8000)
