from Ecc import ECC
from Ecc import prime
import exceptions

HELLO = "HELLO"
CLIENT = "CLIENT"
SERVER = "SERVER"
class tls(object):

	def __init__(self,socket,mode=CLIENT,ecc=None):
		self.socket = socket
		self.mode = mode
		if mode != CLIENT and ecc == None:
			self.ecc = ECC(2,2,prime(160),(5,1))
	
	def connect(self):
		if self.mode == CLIENT:
			self.handshake_client()
		else:
			self.handshake_server()
	
	def handshake_client(self):
		self.socket.send(HELLO)
		pk = self.socket.recv(1024)
		mod = long(pk[pk.index(")")+1:])
		pk = (long(pk[1:pk.index(",")]),long(pk[pk.index(",")+1:pk.index(")")]))
		self.ecc = ECC(2,2,mod,(5,1),0,pk)

	
	def handshake_server(self):
		msg = self.socket.recv(5)
		if msg == HELLO:
			self.socket.send(str(self.ecc.pk)+str(self.ecc.mod))
	def send_data(self, plaintext):
		R,C = self.ecc.encrypt(plaintext)
		self.socket.send(str(R)+str(C))
	
	def receive_data(self):
		C = self.socket.recv(4096)
		R = (long(C[1:C.index(",")]),long(C[C.index(",")+1:C.index(")")]))
		C = bytes(C[C.index(")")+1:])
		plaintext = self.ecc.decrypt(R,C)
		return plaintext
