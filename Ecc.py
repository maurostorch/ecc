import random
from os import urandom
from fractions import gcd
from gmpy2 import invert
import sys

'''
def PointGenerator(x,y,a,b,mod):
	pontos = []
	p=(x,y)
	pontos.append(p)
	i = 0
	while True :
		if p[i] == x and p[i+1] == y:
			pnew = PointDoubling(p[0],p[1],a,mod)
		else:
			pnew  = PointAddition(p[0],p[1],x,y,mod)	
		if not pnew:
			break
		print pnew	  
		p = pnew	
		pontos.append(p)
		i = i + 2
	return(pontos)	
'''
'''
N = A
R = O    // Point at infinity
for (bit = 0; bit < bitlength; bit++) {
    if (bitset(k, bit)) {
        R = point_add(R, N)
    }
    N = point_double(N)
}
The inverse of t
'''

def PointGenerator(x,y,a,b,mod):
	pontos = []
	p=(x,y)
	pontos.append(p)
	i = 2
	#while True :
	for i in range(19):
		for b in reversed(range(len(bin(i))-3)):
			pnew = PointDoubling(p[0],p[1],a,mod)
			pontos.append(pnew)
			if i & (b+1):
				pnew = PointAddition(p[0],p[1],pnew[0],pnew[1],mod)
				pontos.append(pnew)
			p = pnew
			print pnew 	
		i=i+1
				

		
	return(pontos)	


def PointAddition(x1,y1,x2,y2,mod):
	try:
		s = ((y2-y1)/(x2-x1)) % mod
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
	if  p == pc:
		print "true" 
	else:
		print "false"	


if __name__ == "__main__":
	print "Teste da Curva Eliptica"
	#isPointOnCurve(5,1,2,2,17)
	print str(PointGenerator(5,1,2,2,17))