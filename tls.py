from Ecc import ECC
from Ecc import prime
import exceptions

HELLO = "HELLO"
CLIENT = "CLIENT"
SERVER = "SERVER"
MODULUS = 2256865727764315119767551662531059625415112605271L
class tls:

	def __init__(self,socket,mode=CLIENT,ecc=None):
		self.socket = socket
		self.mode = mode
		if ecc == None:
			self.ecc = ECC(2,2,MODULUS,(5,1))
	
	def connect(self):
		if self.mode == CLIENT:
			self.handshake_client()
		else:
			self.handshake_server()
	
	def handshake_client(self):
		self.socket.send(HELLO+"__"+str(self.ecc.pk))
		pk = self.socket.recv(1024)
		self.pk = (long(pk[1:pk.index(",")]),long(pk[pk.index(",")+1:pk.index(")")]))
	
	def handshake_server(self):
		msg = self.socket.recv(1024)
		if msg.split("__")[0] == HELLO:
			pk=msg.split("__")[1]
			self.pk = (long(pk[1:pk.index(",")]),long(pk[pk.index(",")+1:pk.index(")")]))
			self.socket.send(str(self.ecc.pk))

	def send_data(self, plaintext):
		C = self.ecc.encrypt(plaintext,self.pk)
		self.socket.send(str(C))
	
	def receive_data(self):
		C = self.socket.recv(4096)
		C = bytes(C)
		plaintext = self.ecc.decrypt(C,self.pk)
		return plaintext
