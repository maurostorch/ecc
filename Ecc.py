import random
from os import urandom
from fractions import gcd
from gmpy2 import invert
import sys
import hashlib 
from multiprocessing import Pool
from Crypto.Cipher import AES
from Crypto import Random

#Generate a radom prime number 
def prime(size):
	r = random.Random()
	while True:
		r.seed(urandom(16))
		p = r.randint(pow(2, size), pow(2, size + 1) - 1)
		if p % 2 != 0 and pow(2, p - 1, p) == 1:
			return p

def PointList(x,y,a,mod):
	pts = []
	pts.append((x,y))
	i = 2 #starts from 2P until infinite point raised from PointGenerator
	while True:
		try:
			pts.append(PointMultiplication(x,y,a,mod,i))
			i = i + 1
		except:
			break
	return pts

def PointMultiplication(x,y,a,mod,i):
	#print str(i)+"P\n"
	p=(x,y)
	pnew = None
	try:
		for bpos in range(len(bin(i))-3):
			#print "-- bpos = " + str(bpos)
			#print "DOUBLING"
			pnew = PointDoubling(p[0],p[1],a,mod)
			#print pnew
			#pts.append(pnew)
			#print "-- bin(i) = " + bin(i) + " is " + str(bin(i)[bpos+3] == '1')
			if bin(i)[bpos+3] == '1' :
				#print "ADD " + str(pnew) + " + " + str(p)
				pnew = PointAddition(pnew[0],pnew[1],x,y,mod)
				#print pnew
				#pts.append(pnew)
			p = pnew
			#print pnew
	except:
		raise
	return pnew	


def PointAddition(x1,y1,x2,y2,mod):
	try:
		s1 = ((y2-y1)%mod)
		s2 = int(invert(x2-x1,mod))
		s = (s1 * s2) % mod
		x3 = (pow(s,2) - x1 - x2) % mod
		y3 = (s * (x1-x3) - y1) % mod
		return (x3,y3,)
	except:
		raise

def PointDoubling(x1,y1,a,mod):
	try:
		s1 = (3 * pow(x1,2) + a) % mod
		s2 = int(invert(2*y1,mod))
		s = (s1 * s2) % mod
		x3 = (pow(s,2) - x1 - x1) % mod
		y3 = (s * (x1-x3) - y1) % mod
		return (x3,y3,)
	except:
		raise	


#Verify if a point is on curve
def isPointOnCurve(x,y,a,b,mod):
	pc = ((pow(x,3) + (a * x) + b)) % mod
	p  = pow(y,2) 
	return p == pc

#Generate a Eliptic Curve
def CurveGenerate(bitsize):
	while True:
		p=prime(bitsize)
		a=random.randint(100,1000)
		b=random.randint(100,1000)
		pts=[]
		for x in range(1000):
			for y in range(1000):
				if isPointOnCurve(x,y,a,b,p):
					pts.append((x,y))
		if pts.__len__() > 0:
			break
	return p,a,b,pts


#Generate a KeyPair
def KeyPairGen(x,y,a,p):
	while True:
		try:
			d = random.randint(1,p)
			P = PointMultiplication(x,y,a,p,d)
			return d,P
		except:
			pass


#Encrypt using AES
def Encrypt(pk,mod,plaintext):
	#generate a radom integer number
	r = random.randint(1,mod)
	#generate R returns aside the ciphertext
	R = PointMultiplication(5,1,2,mod,r)
	#generate S - Point which x is the syncronous key for AES
	S = PointMultiplication(pk[0],pk[1],2,mod,r)
	#generate K - K is a hash SHA256 of S.x
	K = hashlib.sha256(str(S[0])).digest()
	BLOCK_SIZE = 16
	iv = Random.get_random_bytes(BLOCK_SIZE)
	Obj = AES.new(K, AES.MODE_CBC,iv)
	#MODE_C = obs.Encrypt(plaintext)
	fill =  (BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)) * chr(BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE))
	C = iv + Obj.encrypt(plaintext + fill) 
	return(R,C)


#Decrypt Using AES
def Decrypt(R,ciphertext,d,mod):
	#generate a S
	S = PointMultiplication(R[0],R[1],2,mod,d)
	K = hashlib.sha256(str(S[0])).digest()
	BLOCK_SIZE = 16
	iv = ciphertext[:16]
	ciphertext = ciphertext[16:]
	fill = (BLOCK_SIZE - len(ciphertext) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(ciphertext) % BLOCK_SIZE)
	Obj = AES.new(K, AES.MODE_CBC,iv)
	return Obj.decrypt(ciphertext + fill)[:ciphertext.__len__()-2]



if __name__ == "__main__":
	print "Teste da Curva Eliptica"
	p = prime(160)
	keypair = KeyPairGen(5,1,2,p)
	print "Envia PK"
	print keypair[1]
	print " ------- ENCRYPT -------"
	R,C = Encrypt(keypair[1],p,"TESTE DE CRIPROGRADIA UTILIZANDO CURVAS EPLIPTICAS")
	print R
	print Decrypt(R,C,keypair[0],p)
	