import random
from os import urandom
from fractions import gcd
from gmpy2 import invert
import sys
from multiprocessing import Pool

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

def isPointOnCurve(x,y,a,b,mod):
	pc = ((pow(x,3) + (a * x) + b)) % mod
	p  = pow(y,2) 
	return p == pc

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

def KeyPairGen(x,y,a,p):
	pl = PointList(x,y,a,p)
	r = random.randint(1,pl.__len__()) + 1
	R = PointGenerator(x,y,a,p,r)
	return r,R

if __name__ == "__main__":
	print "Teste da Curva Eliptica"
	#isPointOnCurve(5,1,2,2,17)
	p,a,b,pts = CurveGenerate(160)
	print p,a,b,pts
	#print str(KeyPairGen(pts[0][0],pts[0][1],a,p))
	#print p,a,b,pts
	#1291 978 178 [(51, 26), (53, 28)]
	#pl = PointList(51,26,978,1291)
	#print str(pl)
	#print len(pl)
